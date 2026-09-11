#!/usr/bin/env python3
"""
review_resources.py  —  work the course-resource review queue on floridacourserepo.com

Visitors and vendors suggest websites, videos and products on a course's Resources page.
This client reads that queue and applies the reviewer's decisions over the admin API.
The rules for deciding live in APPROVAL_RULES.md; the API contract is ../RESOURCE_API.md.

Usage (run from Tools/resources/):

    python review_resources.py check                      # API reachable + admin login works
    python review_resources.py queue                      # pending suggestions, oldest first
    python review_resources.py queue --status decided --json
    python review_resources.py show <submissionId>

    # The normal path: write decisions.json, look it over, apply it in one call.
    python review_resources.py apply decisions.json
    python review_resources.py apply decisions.json --yes

    # One-off equivalents (fine for short text; summaries are easier in a file)
    python review_resources.py approve <submissionId> --title T --summary S [--also EET1015C,EEE3300] [--note N]
    python review_resources.py reject  <submissionId> --note "Not related to the course."
    python review_resources.py add --url U --title T --summary S --courses EEE3300,EEE3308C

    # Corrections — each listing belongs to ONE course
    python review_resources.py listings --course EEE3300
    python review_resources.py listings --url https://example.org/page
    python review_resources.py edit <listingId> [--title T] [--summary S]
    python review_resources.py remove <listingId>     # hide it (reversible)
    python review_resources.py restore <listingId>
    python review_resources.py delete <listingId>     # permanent

decisions.json — a list of actions, in any order:

    [
      {"action": "approve", "id": "<submissionId>",
       "title": "All About Circuits — online textbook",
       "summary": "Free online textbook covering DC and AC circuit analysis ... No account needed.",
       "note": null,
       "alsoFor": [{"courseId": "EET1015C"},
                   {"courseId": "EEE3300L", "summary": "Summary written for this course ..."}]},
      {"action": "reject", "id": "<submissionId>", "note": "Not related to the course."},
      {"action": "add", "url": "https://ocw.mit.edu/...", "title": "...", "summary": "...",
       "courses": [{"courseId": "EEE3300"}, {"courseId": "EEE4314C", "summary": "..."}]}
    ]

Credentials (same as the guide pipeline, read from Tools/.env or the environment):
    REPO_ADMIN_EMAIL, REPO_ADMIN_PASSWORD
Optional:
    REPO_BASE_URL   default https://floridacourserepo.com   (or --base-url for a local server)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.dirname(SCRIPT_DIR)
LOG_FILE = os.path.join(SCRIPT_DIR, "review_resources.log")

try:
    from dotenv import load_dotenv
    # Credentials live in Tools/.env alongside the guide pipeline; a local .env wins if present.
    load_dotenv(os.path.join(TOOLS_DIR, ".env"))
    load_dotenv(os.path.join(SCRIPT_DIR, ".env"))
except ImportError:
    pass

# Summaries carry en dashes and other non-cp1252 characters; never let the Windows console
# encoding abort a run mid-batch (the lesson from generate_guide.py).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

TIMEOUT = 30


def log(message: str) -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{stamp}  {message}\n")


class Api:
    """Thin wrapper over the site's REST API. Raises Fail with the server's own message."""

    class Fail(Exception):
        pass

    def __init__(self, base_url: str):
        self.base = base_url.rstrip("/")
        self.session = requests.Session()
        self.token = None

    def login(self) -> None:
        email = os.environ.get("REPO_ADMIN_EMAIL")
        password = os.environ.get("REPO_ADMIN_PASSWORD")
        if not email or not password:
            raise Api.Fail("REPO_ADMIN_EMAIL and REPO_ADMIN_PASSWORD are required (Tools/.env).")
        r = self.session.post(f"{self.base}/api/v1/auth/login",
                              json={"email": email, "password": password}, timeout=TIMEOUT)
        if r.status_code != 200:
            raise Api.Fail(f"Login failed (HTTP {r.status_code}). Check the credentials in Tools/.env.")
        self.token = r.json()["data"]["accessToken"]

    def call(self, method: str, path: str, *, params=None, body=None, auth=False):
        if auth and not self.token:
            self.login()
        headers = {"Authorization": f"Bearer {self.token}"} if auth else {}
        r = self.session.request(method, f"{self.base}{path}", params=params, json=body,
                                 headers=headers, timeout=TIMEOUT)
        try:
            payload = r.json()
        except ValueError:
            raise Api.Fail(f"HTTP {r.status_code} from {path} (no JSON body).")
        if r.status_code >= 400 or not payload.get("success", False):
            error = payload.get("error") or {}
            fields = error.get("details") or []
            detail = "; ".join(f"{f.get('field')}: {f.get('message')}" for f in fields)
            raise Api.Fail(f"HTTP {r.status_code} {error.get('code', '')}: {error.get('message', '')}"
                           + (f" ({detail})" if detail else ""))
        return payload.get("data")


# ── printing ─────────────────────────────────────────────────────────────────

def print_queue(items, as_json: bool, limit: int) -> None:
    if as_json:
        print(json.dumps(items[:limit] if limit else items, indent=2))
        return
    if not items:
        print("Nothing in the queue.")
        return
    for item in (items[:limit] if limit else items):
        print(f"\n{item['id']}")
        print(f"  course     {item['courseId']} — {item['courseTitle']}")
        print(f"  link       [{item['type']}] {item['url']}")
        if item.get("description"):
            print(f"  submitter  {item['description']}")
        print(f"  submitted  {item['submittedUtc'][:19].replace('T', ' ')} UTC   status {item['status']}")
        if item.get("decisionNote"):
            print(f"  note       {item['decisionNote']}")


def print_listings(rows) -> None:
    if not rows:
        print("No listings.")
        return
    for r in rows:
        flag = "" if r["status"] == "Active" else f"  [{r['status']}]"
        print(f"\n{r['id']}{flag}")
        print(f"  course   {r['courseId']}   ({r['source']})")
        print(f"  link     [{r['type']}] {r['url']}")
        print(f"  title    {r['title']}")
        print(f"  summary  {r['summary'][:300]}{'…' if len(r['summary']) > 300 else ''}")
        if r["alsoForCourseIds"]:
            print(f"  also on  {', '.join(r['alsoForCourseIds'])}")


def print_results(results) -> None:
    for r in results:
        mark = "+" if r["outcome"] == "created" else ("~" if r["outcome"] == "updated" else "!")
        print(f"    {mark} {r['courseId']}: {r['outcome']}")


# ── actions ──────────────────────────────────────────────────────────────────

def do_approve(api: Api, action: dict) -> str:
    body = {"title": action.get("title"), "summary": action.get("summary"),
            "note": action.get("note"), "alsoFor": action.get("alsoFor") or []}
    data = api.call("POST", f"/api/v1/resource-submissions/{action['id']}/approve", body=body, auth=True)
    print(f"  approved {action['id']}: {data['message']}")
    print_results(data["results"])
    unknown = [r["courseId"] for r in data["results"] if r["outcome"] == "unknownCourse"]
    if unknown:
        print(f"    ⚠ not listed on the site, nothing written: {', '.join(unknown)}")
    return f"approve {action['id']} -> {data['message']}"


def do_reject(api: Api, action: dict) -> str:
    data = api.call("POST", f"/api/v1/resource-submissions/{action['id']}/reject",
                    body={"note": action.get("note")}, auth=True)
    print(f"  rejected {action['id']}: {data['message']}")
    return f"reject {action['id']} -> {action.get('note')}"


def do_add(api: Api, action: dict) -> str:
    body = {"url": action.get("url"), "title": action.get("title"),
            "summary": action.get("summary"), "courses": action.get("courses") or []}
    data = api.call("POST", "/api/v1/resources", body=body, auth=True)
    print(f"  listed {data['url']}")
    print_results(data["results"])
    return f"add {data['url']} -> {len(data['results'])} course(s)"


ACTIONS = {"approve": do_approve, "reject": do_reject, "add": do_add}


def run_apply(api: Api, path: str, assume_yes: bool) -> int:
    with open(path, encoding="utf-8-sig") as f:
        actions = json.load(f)
    if isinstance(actions, dict):
        actions = [actions]

    print(f"{len(actions)} action(s) from {path}:")
    for a in actions:
        kind = a.get("action")
        if kind == "approve":
            extra = ", ".join(c.get("courseId", "?") for c in (a.get("alsoFor") or []))
            print(f"  approve {a.get('id')}  “{(a.get('title') or '')[:60]}”"
                  + (f"  also: {extra}" if extra else ""))
        elif kind == "reject":
            print(f"  reject  {a.get('id')}  note: {(a.get('note') or '')[:60]}")
        elif kind == "add":
            courses = ", ".join(c.get("courseId", "?") for c in (a.get("courses") or []))
            print(f"  add     {a.get('url')}  for: {courses}")
        else:
            print(f"  ⚠ unknown action: {kind!r}")

    if not assume_yes:
        answer = input("\nApply these? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Nothing applied.")
            return 1

    failures = 0
    for a in actions:
        handler = ACTIONS.get(a.get("action"))
        if handler is None:
            print(f"  ! skipped unknown action {a.get('action')!r}")
            failures += 1
            continue
        try:
            log(handler(api, a))
        except Api.Fail as e:
            failures += 1
            print(f"  ! {a.get('action')} {a.get('id') or a.get('url')}: {e}")
            log(f"FAILED {a.get('action')} {a.get('id') or a.get('url')}: {e}")
    print(f"\nDone. {len(actions) - failures} applied, {failures} failed.")
    return 1 if failures else 0


def courses_arg(value: str):
    return [{"courseId": c.strip().upper()} for c in value.split(",") if c.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-url", default=os.environ.get("REPO_BASE_URL", "https://floridacourserepo.com"))
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="API reachable and admin login works")

    p_queue = sub.add_parser("queue", help="Suggestions waiting for review")
    p_queue.add_argument("--status", default="pending", choices=["pending", "decided", "all"])
    p_queue.add_argument("--limit", type=int, default=0)
    p_queue.add_argument("--json", action="store_true")

    p_show = sub.add_parser("show", help="One suggestion")
    p_show.add_argument("submission_id")

    p_apply = sub.add_parser("apply", help="Apply a decisions.json file")
    p_apply.add_argument("file")
    p_apply.add_argument("--yes", action="store_true", help="skip the confirmation prompt")

    p_ok = sub.add_parser("approve", help="Approve one suggestion")
    p_ok.add_argument("submission_id")
    p_ok.add_argument("--title", required=True)
    p_ok.add_argument("--summary", required=True)
    p_ok.add_argument("--also", default="", help="other course ids, comma-separated")
    p_ok.add_argument("--note")

    p_no = sub.add_parser("reject", help="Reject one suggestion (the note is public)")
    p_no.add_argument("submission_id")
    p_no.add_argument("--note", required=True)

    p_add = sub.add_parser("add", help="List a link you found yourself")
    p_add.add_argument("--url", required=True)
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--summary", required=True)
    p_add.add_argument("--courses", required=True, help="course ids, comma-separated")

    p_list = sub.add_parser("listings", help="Listings for a course or a link")
    p_list.add_argument("--course")
    p_list.add_argument("--url")
    p_list.add_argument("--json", action="store_true")

    p_edit = sub.add_parser("edit", help="Edit one course's listing")
    p_edit.add_argument("listing_id")
    p_edit.add_argument("--title")
    p_edit.add_argument("--summary")

    for name, help_text in [("remove", "Hide one listing"), ("restore", "Show it again"), ("delete", "Delete it permanently")]:
        p = sub.add_parser(name, help=help_text)
        p.add_argument("listing_id")

    args = parser.parse_args()
    api = Api(args.base_url)

    try:
        if args.command == "check":
            queue = api.call("GET", "/api/v1/queue/resources", params={"status": "pending"})
            api.login()
            print(f"{args.base_url}: API reachable, admin login OK, {queue['pending']} suggestion(s) pending.")
            return 0

        if args.command == "queue":
            data = api.call("GET", "/api/v1/queue/resources", params={"status": args.status})
            if not args.json:
                print(f"{data['pending']} pending · {data['decidedRecently']} decided in the last 30 days")
            print_queue(data["items"], args.json, args.limit)
            return 0

        if args.command == "show":
            data = api.call("GET", "/api/v1/queue/resources", params={"status": "all"})
            item = next((i for i in data["items"] if i["id"] == args.submission_id), None)
            if item is None:
                print(f"Submission {args.submission_id} not found in the queue.")
                return 1
            print(json.dumps(item, indent=2))
            return 0

        if args.command == "apply":
            return run_apply(api, args.file, args.yes)

        if args.command == "approve":
            log(do_approve(api, {"id": args.submission_id, "title": args.title, "summary": args.summary,
                                 "note": args.note, "alsoFor": courses_arg(args.also)}))
            return 0

        if args.command == "reject":
            log(do_reject(api, {"id": args.submission_id, "note": args.note}))
            return 0

        if args.command == "add":
            log(do_add(api, {"url": args.url, "title": args.title, "summary": args.summary,
                             "courses": courses_arg(args.courses)}))
            return 0

        if args.command == "listings":
            if bool(args.course) == bool(args.url):
                print("Give exactly one of --course or --url.")
                return 2
            rows = (api.call("GET", f"/api/v1/courses/{args.course.strip().upper()}/resources") if args.course
                    else api.call("GET", "/api/v1/resources", params={"url": args.url}))
            print(json.dumps(rows, indent=2)) if args.json else print_listings(rows)
            return 0

        if args.command in ("edit", "remove", "restore", "delete"):
            if args.command == "delete":
                api.call("DELETE", f"/api/v1/resources/{args.listing_id}", auth=True)
                print(f"Deleted {args.listing_id}.")
            else:
                body = {"title": getattr(args, "title", None), "summary": getattr(args, "summary", None),
                        "status": {"remove": "removed", "restore": "active"}.get(args.command)}
                data = api.call("PATCH", f"/api/v1/resources/{args.listing_id}",
                                body={k: v for k, v in body.items() if v is not None}, auth=True)
                print(f"{args.command}: {data['courseId']} — {data['title']} [{data['status']}]")
            log(f"{args.command} {args.listing_id}")
            return 0

    except Api.Fail as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
