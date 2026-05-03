#!/usr/bin/env python3
"""
generate_guide.py  —  AI-powered curriculum guide generator for floridacourserepo.com

Claude searches the web for each course, writes the HTML guide, lets you review
it, then pushes it to the repo API.

Usage:
    python generate_guide.py ETS1010
    python generate_guide.py ETS1010 ETS1020 ETS1030
    python generate_guide.py --file courses.txt
    python generate_guide.py ETS1010 --yes              # skip review prompts
    python generate_guide.py ETS1010 --auto             # same as --yes
    python generate_guide.py --push-draft ETS1010       # push a saved draft
    python generate_guide.py --push-draft-file list.txt # batch push saved drafts

Required env vars:
    ANTHROPIC_API_KEY

Required to push (optional for generate-only):
    REPO_ADMIN_EMAIL
    REPO_ADMIN_PASSWORD

Optional:
    REPO_BASE_URL   default: https://floridacourserepo.com
    GUIDE_MODEL     default: claude-opus-4-7
"""

import argparse
import json
import os
import re
import sys
import textwrap
import time
from datetime import datetime, timezone

import anthropic
import requests

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
except ImportError:
    pass

BASE_URL = os.environ.get("REPO_BASE_URL", "https://floridacourserepo.com").rstrip("/")
DRAFTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drafts")
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generate_guide.log")
QUEUE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "queue.csv")
ACTIVITY_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "activity.log")


def log_event(course_id: str, event: str, status: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{ts} [{course_id}] {event}: {status}\n")


def log_activity(actor: str, message: str) -> None:
    """Append one line to activity.log if it exists. Silent no-op if not."""
    if not os.path.exists(ACTIVITY_LOG):
        return
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(ACTIVITY_LOG, "a", encoding="utf-8") as f:
        f.write(f"{ts}  {actor:<8}  {message}\n")


def update_queue_state(course_id: str, new_state: str) -> bool:
    """Update queue.csv to reflect a status change. Silent no-op if no queue.

    Returns True if a row was updated, False otherwise.
    """
    if not os.path.exists(QUEUE_FILE):
        return False
    import csv
    with open(QUEUE_FILE, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []
    if not rows:
        return False

    cid = course_id.upper()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    updated = False
    for r in rows:
        if r.get("course_id", "").upper() == cid:
            r["status"] = new_state
            if new_state == "drafted" and not r.get("drafted_utc"):
                r["drafted_utc"] = ts
            elif new_state == "pushed" and not r.get("pushed_utc"):
                r["pushed_utc"] = ts
            updated = True
            break

    if updated:
        with open(QUEUE_FILE, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
    return updated


def read_queue_course_ids(state: str) -> list[str]:
    """Return course IDs in queue.csv with the given state, in file order."""
    if not os.path.exists(QUEUE_FILE):
        return []
    import csv
    with open(QUEUE_FILE, encoding="utf-8-sig", newline="") as f:
        return [r["course_id"] for r in csv.DictReader(f)
                if r.get("status") == state]


SYSTEM_PROMPT = """\
You are a curriculum developer for the Florida Course Repository, a public library of
open educational materials aligned to the Florida Statewide Course Numbering System (SCNS).

Your job: research a given Florida college course and produce a structured curriculum guide.

Use web_search to look up:
- The official SCNS course description (search "Florida SCNS <COURSE_ID>" or the course title)
- Typical learning outcomes at Florida colleges (Valencia, FSCJ, SPC, etc.)
- Learning Outcomes should be categorized as required (where they are common among all schools) and optional (can be covered, but not required
- Standard topics and content areas. Give required topics based on common coverage of identified offerings and option coverage.
- Credit hours and contact hours
- Typical prerequisites or co-requisites

Then return ONLY a raw JSON object — no explanation, no markdown fences — with exactly
these fields:

{
  "title": "Short descriptive guide title, e.g. 'Introduction to Electronics Technology'",
  "html_content": "<full HTML content — see format below>",
  "credits": 3,
  "contact_hours": 45,
  "prerequisites": "MAT 0028 or equivalent" or null,
  "version": "1.0"
}

HTML content format:
- Sections:
   Course Description,
   Learning Outcomes (required and optional),
   Major Topics (required and optional),
   Resources & Tools,
   Career Pathways  (omit any section you cannot verify)
   Special Information (Certificaton Preperation, specific job preparation)
- Use <h2> for section headings
- Use <p> for paragraphs, <ul><li> for lists, <strong> for key terms
- No <html>, <head>, <body>, or <style> tags — inner content only
- Bootstrap classes are available (e.g. class="list-group list-group-flush") but keep markup clean

Be factual and specific to Florida college standards. Omit rather than fabricate.\
"""


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def get_course_info(session: requests.Session, course_id: str) -> dict | None:
    try:
        resp = session.get(f"{BASE_URL}/api/v1/courses/{course_id}", timeout=10)
    except requests.RequestException as exc:
        print(f"  Warning: could not reach API ({exc}). Generating from ID only.")
        return None
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json().get("data")


def check_guide_on_site(session: requests.Session, course_id: str) -> bool:
    """Returns True if the course already has a curriculum guide URL on the site.

    Note: curriculumGuideUrl is only populated once the course has published
    modules. For guide-only courses, this returns False even when a guide
    exists — callers should also check was_guide_pushed() via the log.
    """
    try:
        resp = session.get(f"{BASE_URL}/api/v1/courses/{course_id}", timeout=10)
    except requests.RequestException:
        return False
    if resp.status_code != 200:
        return False
    data = resp.json().get("data") or {}
    return bool(data.get("curriculumGuideUrl"))


def was_guide_pushed(course_id: str) -> bool:
    """Returns True if the guide was previously pushed successfully.

    Checks the draft file's pushed_utc stamp first (written after every
    successful push), then falls back to the log file for entries written
    before the stamp feature existed.
    """
    path = os.path.join(DRAFTS_DIR, f"{course_id}_guide.json")
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8-sig") as f:
                data = json.load(f)
            if data.get("pushed_utc"):
                return True
        except Exception:
            pass
    if not os.path.exists(LOG_FILE):
        return False
    marker = f"[{course_id}] PUSH: Success"
    with open(LOG_FILE, encoding="utf-8") as f:
        return any(marker in line for line in f)


def mark_draft_pushed(course_id: str) -> None:
    """Stamp the draft JSON with the push timestamp so future batches skip it."""
    path = os.path.join(DRAFTS_DIR, f"{course_id}_guide.json")
    if not os.path.exists(path):
        return
    try:
        with open(path, encoding="utf-8-sig") as f:
            data = json.load(f)
        data["pushed_utc"] = datetime.now(timezone.utc).isoformat()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def verify_guide(session: requests.Session, course_id: str) -> None:
    """Confirm the guide is visible on the site after a push; always logs the result.

    The push already confirmed success via the PUT response. This GET check
    upgrades the log to 'Success (URL confirmed)' when curriculumGuideUrl is
    present, but does not downgrade it — the URL is only populated once the
    course has published modules.
    """
    try:
        resp = session.get(f"{BASE_URL}/api/v1/courses/{course_id}", timeout=10)
    except requests.RequestException as exc:
        # Can't reach the API, but the push already succeeded.
        log_event(course_id, "VERIFY", "Success (guide saved; GET check unreachable)")
        return
    if resp.status_code == 404:
        log_event(course_id, "VERIFY", "Success (guide saved; course not yet browsable — no published modules)")
        return
    if resp.status_code != 200:
        log_event(course_id, "VERIFY", f"Success (guide saved; GET returned HTTP {resp.status_code})")
        return
    data = resp.json().get("data") or {}
    if data.get("curriculumGuideUrl"):
        print("  Verified: guide URL is live on site.")
        log_event(course_id, "VERIFY", "Success (URL confirmed)")
    else:
        print("  Guide saved. URL will appear once the course has published modules.")
        log_event(course_id, "VERIFY", "Success (guide saved; URL pending published modules)")


def get_token(session: requests.Session) -> str:
    email = os.environ.get("REPO_ADMIN_EMAIL")
    password = os.environ.get("REPO_ADMIN_PASSWORD")
    if not email or not password:
        print("Error: REPO_ADMIN_EMAIL and REPO_ADMIN_PASSWORD are required to push.")
        sys.exit(1)
    resp = session.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    resp.raise_for_status()
    token = resp.json()["data"]["accessToken"]
    print("  Authenticated as admin.")
    return token


def push_guide(session: requests.Session, course_id: str, data: dict, token: str) -> None:
    credits = data.get("credits")
    if credits is None or not (0 <= int(credits) <= 12):
        raise ValueError(
            f"credits={credits!r} is outside the valid range 0–12. "
            f"Edit the draft at drafts/{course_id}_guide.json and push with --push-draft."
        )
    contact_hours = data.get("contact_hours")
    payload = {
        "title": data["title"],
        "htmlContent": data["html_content"],
        "credits": int(credits),
        "contactHours": int(contact_hours) if contact_hours else None,
        "prerequisites": data.get("prerequisites"),
        "version": data.get("version"),
        "generatedUtc": datetime.now(timezone.utc).isoformat(),
    }
    resp = session.put(
        f"{BASE_URL}/api/v1/courses/{course_id}/guide",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    resp.raise_for_status()
    msg = (resp.json().get("data") or {}).get("message", "Saved.")
    print(f"  {msg}")


def _push_with_token_refresh(
    session: requests.Session,
    course_id: str,
    data: dict,
    token: str,
) -> str:
    """Push guide, refreshing the token once on 401. Returns the (possibly new) token."""
    try:
        push_guide(session, course_id, data, token)
        log_event(course_id, "PUSH", "Success")
        mark_draft_pushed(course_id)
        update_queue_state(course_id, "pushed")
        log_activity("push", f"PUSHED {course_id}")
        verify_guide(session, course_id)
    except requests.HTTPError as exc:
        if exc.response.status_code == 401:
            print("  Token expired — re-authenticating...")
            token = get_token(session)
            try:
                push_guide(session, course_id, data, token)
                log_event(course_id, "PUSH", "Success")
                mark_draft_pushed(course_id)
                update_queue_state(course_id, "pushed")
                log_activity("push", f"PUSHED {course_id} (after re-auth)")
                verify_guide(session, course_id)
            except Exception as exc2:
                log_event(course_id, "PUSH", f"ERROR: {exc2}")
                update_queue_state(course_id, "error")
                log_activity("push", f"ERROR {course_id}: {exc2}")
                raise
        else:
            log_event(course_id, "PUSH", f"ERROR: HTTP {exc.response.status_code}")
            update_queue_state(course_id, "error")
            log_activity("push", f"ERROR {course_id}: HTTP {exc.response.status_code}")
            raise
    except Exception as exc:
        log_event(course_id, "PUSH", f"ERROR: {exc}")
        update_queue_state(course_id, "error")
        log_activity("push", f"ERROR {course_id}: {exc}")
        raise
    return token


# ---------------------------------------------------------------------------
# Guide generation
# ---------------------------------------------------------------------------

def build_prompt(course_id: str, info: dict | None) -> str:
    if info:
        path = info.get("taxonomyPath") or {}
        names = [
            (path.get("level1") or {}).get("name", ""),
            (path.get("level2") or {}).get("name", ""),
            (path.get("level3") or {}).get("name", ""),
        ]
        taxonomy = " > ".join(n for n in names if n)
        return (
            f"Generate a curriculum guide for this Florida college course:\n\n"
            f"Course ID: {course_id}\n"
            f"Title: {info.get('title', course_id)}\n"
            f"Credit Hours: {info.get('creditHours') or 'unknown'}\n"
            f"Taxonomy: {taxonomy or 'unknown'}\n\n"
            f"Search for authoritative information about this course, then return the JSON guide."
        )
    return (
        f"Generate a curriculum guide for Florida college course: {course_id}\n\n"
        f"Search the Florida SCNS system and college catalogs for this course, "
        f"then return the JSON guide."
    )


def extract_json(text: str) -> dict:
    text = re.sub(r"```(?:json)?\s*", "", text).strip()
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError(
            f"No JSON object found in model response.\n\nModel output:\n{text[:800]}"
        )
    return json.loads(match.group())


def generate_guide(course_id: str, course_info: dict | None) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable is required.")
        sys.exit(1)

    model = os.environ.get("GUIDE_MODEL", "claude-opus-4-7")
    print(f"  Researching with {model} + web search...")

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
        messages=[{"role": "user", "content": build_prompt(course_id, course_info)}],
    )

    text = "".join(
        block.text for block in response.content if hasattr(block, "text")
    )
    return extract_json(text)


# ---------------------------------------------------------------------------
# Display / persistence
# ---------------------------------------------------------------------------

def display_guide(course_id: str, data: dict) -> None:
    sep = "=" * 70
    print(f"\n{sep}")
    print(f"  GUIDE: {course_id}")
    print(sep)
    print(f"  Title         : {data.get('title', '—')}")
    print(f"  Credits       : {data.get('credits', '—')}")
    print(f"  Contact Hours : {data.get('contact_hours', '—')}")
    print(f"  Prerequisites : {data.get('prerequisites') or '—'}")
    print(f"  Version       : {data.get('version', '—')}")
    print()
    plain = re.sub(r"<[^>]+>", " ", data.get("html_content", ""))
    plain = re.sub(r"\s+", " ", plain).strip()
    preview = plain[:900] + ("..." if len(plain) > 900 else "")
    for line in textwrap.wrap(preview, width=68, initial_indent="  ", subsequent_indent="  "):
        print(line)
    print(sep)


def save_draft(course_id: str, data: dict) -> str:
    os.makedirs(DRAFTS_DIR, exist_ok=True)
    path = os.path.join(DRAFTS_DIR, f"{course_id}_guide.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path


# ---------------------------------------------------------------------------
# Processing modes
# ---------------------------------------------------------------------------

def process_course(
    course_id: str,
    session: requests.Session,
    token: str | None,
    auto_approve: bool,
) -> str | None:
    """Single-course mode: always regenerate, then prompt to push."""
    course_id = course_id.upper().strip()
    print(f"\n[{course_id}] Fetching course info from repo...")
    info = get_course_info(session, course_id)
    if not info:
        print("  Course not found in taxonomy — generating from course ID only.")
        log_event(course_id, "TAXONOMY", "Not found in repo — guide generated from course ID only")

    try:
        data = generate_guide(course_id, info)
    except Exception as exc:
        log_event(course_id, "GENERATE", f"ERROR: {exc}")
        raise

    log_event(course_id, "GENERATE", "Success")
    display_guide(course_id, data)
    draft_path = save_draft(course_id, data)
    print(f"\n  Draft saved: {draft_path}")
    update_queue_state(course_id, "drafted")
    log_activity("local", f"DRAFT {course_id} → drafts/{course_id}_guide.json")

    if auto_approve:
        choice = "y"
    else:
        choice = input("  Push to site? [y / n / e=edit and push later] ").strip().lower()

    if choice == "y":
        if token is None:
            token = get_token(session)
        token = _push_with_token_refresh(session, course_id, data, token)
    elif choice == "e":
        print(f"  Edit the draft then run:")
        print(f"    python generate_guide.py --push-draft {course_id}")
    else:
        print("  Skipped.")

    return token


def process_course_batch(
    course_id: str,
    session: requests.Session,
    token: str | None,
    auto_approve: bool,
) -> tuple[str | None, bool]:
    """
    Smart batch mode (used with --file):
      1. Draft exists + guide on site  → skip (already done)
      2. Draft exists + guide not on site → push existing draft
      3. No draft → generate then push

    Returns (token, api_called) where api_called is False only when the course
    was skipped entirely — no delay needed before the next course in that case.
    """
    course_id = course_id.upper().strip()
    print(f"\n[{course_id}] Processing...")

    draft_path = os.path.join(DRAFTS_DIR, f"{course_id}_guide.json")

    generated = False  # True only when the Anthropic API was called

    if os.path.exists(draft_path):
        log_event(course_id, "DRAFT", "Draft file exists")
        print(f"  Draft found: {draft_path}")

        if check_guide_on_site(session, course_id) or was_guide_pushed(course_id):
            log_event(course_id, "SITE", "Guide exists on site — skipping")
            print("  Guide already on site. Skipping.")
            return token, False

        # Draft present but guide not yet pushed — load and push (no generation)
        try:
            with open(draft_path, encoding="utf-8-sig") as f:
                data = json.load(f)
        except Exception as exc:
            print(f"  ERROR reading draft: {exc}")
            log_event(course_id, "PUSH", f"ERROR reading draft: {exc}")
            return token, False

        display_guide(course_id, data)

        if auto_approve:
            choice = "y"
        else:
            choice = input("  Push existing draft? [y/N] ").strip().lower()

        if choice != "y":
            print("  Skipped.")
            return token, False

    else:
        # No draft: generate from scratch (Anthropic API call)
        print("  No draft found — generating...")
        info = get_course_info(session, course_id)
        if not info:
            print("  Course not found in taxonomy — generating from course ID only.")
            log_event(course_id, "TAXONOMY", "Not found in repo — guide generated from course ID only")

        try:
            data = generate_guide(course_id, info)
        except Exception as exc:
            log_event(course_id, "GENERATE", f"ERROR: {exc}")
            raise

        generated = True
        log_event(course_id, "GENERATE", "Success")
        display_guide(course_id, data)
        save_draft(course_id, data)
        print(f"  Draft saved: {draft_path}")
        update_queue_state(course_id, "drafted")
        log_activity("local", f"DRAFT {course_id} → drafts/{course_id}_guide.json")

        if auto_approve:
            choice = "y"
        else:
            choice = input("  Push to site? [y / n / e=edit and push later] ").strip().lower()

        if choice == "e":
            print(f"  Edit the draft then run:")
            print(f"    python generate_guide.py --push-draft {course_id}")
            return token, generated
        elif choice != "y":
            print("  Skipped.")
            return token, generated

    # Shared push path (draft-was-present or freshly generated)
    if token is None:
        token = get_token(session)
    token = _push_with_token_refresh(session, course_id, data, token)
    return token, generated


def run_push_draft(course_id: str, session: requests.Session) -> None:
    """Push a single saved draft interactively."""
    course_id = course_id.upper().strip()
    path = os.path.join(DRAFTS_DIR, f"{course_id}_guide.json")
    if not os.path.exists(path):
        print(f"No draft found at: {path}")
        sys.exit(1)
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)
    display_guide(course_id, data)
    choice = input("  Push to site? [y/N] ").strip().lower()
    if choice == "y":
        token = get_token(session)
        _push_with_token_refresh(session, course_id, data, token)
    else:
        print("  Aborted.")


def run_push_draft_batch(
    file_path: str, session: requests.Session, auto_approve: bool, delay: int
) -> None:
    """Batch-push saved drafts listed in a file.

    Note: --delay is ignored here. The delay exists to throttle Anthropic API
    calls during generation; pushes hit only your repo's API and don't need it.
    """
    with open(file_path, encoding="utf-8-sig") as f:
        course_ids = [
            ln.strip().upper()
            for ln in f
            if ln.strip() and not ln.startswith("#")
        ]
    if not course_ids:
        print("No course IDs found in file.")
        return

    print(f"Pushing drafts for {len(course_ids)} course(s): {', '.join(course_ids)}")

    token: str | None = None
    if auto_approve and os.environ.get("REPO_ADMIN_EMAIL"):
        token = get_token(session)

    for course_id in course_ids:
        path = os.path.join(DRAFTS_DIR, f"{course_id}_guide.json")
        if not os.path.exists(path):
            print(f"\n[{course_id}] No draft found at: {path}")
            log_event(course_id, "PUSH", "ERROR: Draft file not found")
            continue

        try:
            with open(path, encoding="utf-8-sig") as f:
                data = json.load(f)
        except Exception as exc:
            print(f"\n[{course_id}] ERROR reading draft: {exc}")
            log_event(course_id, "PUSH", f"ERROR reading draft: {exc}")
            continue

        print(f"\n[{course_id}] Pushing draft...")
        display_guide(course_id, data)

        if auto_approve:
            choice = "y"
        else:
            choice = input("  Push to site? [y/N] ").strip().lower()

        if choice != "y":
            print("  Skipped.")
            continue

        if token is None:
            token = get_token(session)

        try:
            token = _push_with_token_refresh(session, course_id, data, token)
        except Exception as exc:
            print(f"  ERROR: {exc}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate AI-powered curriculum guides for floridacourserepo.com",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("courses", nargs="*", metavar="COURSE_ID",
                        help="One or more course IDs (e.g. ETS1010)")
    parser.add_argument("--file", "-f", metavar="FILE",
                        help="Text file with one course ID per line (# for comments); "
                             "uses smart batch logic (skip if guide already on site)")
    parser.add_argument("--push-draft", metavar="COURSE_ID",
                        help="Push a previously saved draft without regenerating")
    parser.add_argument("--push-draft-file", metavar="FILE",
                        help="Text file with course IDs to push from saved drafts (# for comments)")
    parser.add_argument("--from-queue", action="store_true",
                        help="Generate the next N queued courses from queue.csv "
                             "(uses --queue-n, default 5). Equivalent to "
                             "'queue_mgr.py next-batch | xargs python generate_guide.py'.")
    parser.add_argument("--push-from-queue", action="store_true",
                        help="Push every drafted course from queue.csv (no Anthropic API calls).")
    parser.add_argument("--queue-n", type=int, default=5, metavar="N",
                        help="With --from-queue: how many courses to generate this run (default 5)")
    parser.add_argument("--yes", "-y", "--auto", action="store_true",
                        help="Auto-approve all guides without prompting")
    parser.add_argument("--delay", "-d", type=int, default=60, metavar="SECONDS",
                        help="Seconds to wait between courses during generation only "
                             "(default: 60). Ignored for push-only batches.")
    args = parser.parse_args()

    if args.push_draft:
        run_push_draft(args.push_draft, requests.Session())
        return

    if args.push_draft_file:
        run_push_draft_batch(args.push_draft_file, requests.Session(), args.yes, args.delay)
        return

    if args.push_from_queue:
        # Push every course in 'drafted' state from queue.csv.
        ids = read_queue_course_ids("drafted")
        if not ids:
            print("No drafted courses in queue. Nothing to push.")
            return
        # Reuse the batch path by writing a temp list file
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as tf:
            tf.write("\n".join(ids))
            tmp_path = tf.name
        try:
            run_push_draft_batch(tmp_path, requests.Session(), args.yes, args.delay)
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        return

    if args.from_queue:
        # Generate the next N queued courses.
        ids = read_queue_course_ids("queued")[:args.queue_n]
        if not ids:
            print("No queued courses found. Use 'queue_mgr.py add' to populate.")
            return
        print(f"From queue, drafting next {len(ids)} course(s): {', '.join(ids)}")
        # Treat them like file-supplied IDs so we get the smart batch routing
        # (skip if already drafted/pushed).
        args.courses = []  # ensure we don't double up if user also passed positionals
        # Fall through to the main loop below with file_ids = ids
        file_ids = ids
        direct_ids = []
        course_ids = ids
    else:
        # Collect course IDs; flag which came from --file for smart routing
        direct_ids = [c.upper().strip() for c in args.courses]
        file_ids = []
        if args.file:
            with open(args.file, encoding="utf-8-sig") as f:
                file_ids = [
                    ln.strip().upper()
                    for ln in f
                    if ln.strip() and not ln.startswith("#")
                ]

        course_ids = direct_ids + file_ids
        if not course_ids:
            parser.print_help()
            sys.exit(1)

    print(f"Processing {len(course_ids)} course(s): {', '.join(course_ids)}")

    session = requests.Session()
    token: str | None = None
    if args.yes and os.environ.get("REPO_ADMIN_EMAIL"):
        token = get_token(session)

    api_called_last = False
    for i, cid in enumerate(course_ids):
        if i > 0 and args.delay > 0 and api_called_last:
            print(f"  Waiting {args.delay}s before next course...")
            time.sleep(args.delay)
        try:
            # Use smart batch logic for file-sourced IDs; always-regenerate for CLI IDs
            if cid in file_ids:
                token, api_called_last = process_course_batch(cid, session, token, auto_approve=args.yes)
            else:
                token = process_course(cid, session, token, auto_approve=args.yes)
                api_called_last = True
        except KeyboardInterrupt:
            print("\nInterrupted.")
            sys.exit(0)
        except json.JSONDecodeError as exc:
            print(f"  ERROR: Could not parse JSON from model response: {exc}")
            api_called_last = True
        except requests.HTTPError as exc:
            print(f"  ERROR: API call failed: {exc.response.status_code} {exc.response.text[:200]}")
            # HTTPError always comes from the repo API (push/auth), never from Anthropic
            api_called_last = cid not in file_ids
        except Exception as exc:
            print(f"  ERROR: {exc}")
            # Local errors (validation, file I/O) don't consume Anthropic tokens
            api_called_last = cid not in file_ids


if __name__ == "__main__":
    main()
