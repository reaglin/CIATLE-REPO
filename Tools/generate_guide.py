#!/usr/bin/env python3
"""
generate_guide.py  —  AI-powered curriculum guide generator for floridacourserepo.com

Claude searches the web for each course, writes the HTML guide, lets you review
it, then pushes it to the repo API.

Usage:
    python generate_guide.py ETS1010
    python generate_guide.py ETS1010 ETS1020 ETS1030
    python generate_guide.py --file courses.txt
    python generate_guide.py ETS1010 --yes          # skip review prompts
    python generate_guide.py --push-draft ETS1010   # push a saved draft

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
from datetime import datetime, timezone

import anthropic
import requests

BASE_URL = os.environ.get("REPO_BASE_URL", "https://floridacourserepo.com").rstrip("/")
DRAFTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drafts")

SYSTEM_PROMPT = """\
You are a curriculum developer for the Florida Course Repository, a public library of
open educational materials aligned to the Florida Statewide Course Numbering System (SCNS).

Your job: research a given Florida college course and produce a structured curriculum guide.

Use web_search to look up:
- The official SCNS course description (search "Florida SCNS <COURSE_ID>" or the course title)
- Typical learning outcomes at Florida colleges (Valencia, FSCJ, SPC, etc.)
- Standard topics and content areas
- Credit hours and contact hours if not already given
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
- Sections: Course Description, Learning Outcomes, Major Topics, Resources & Tools,
  Career Pathways  (omit any section you cannot verify)
- Use <h2> for section headings
- Use <p> for paragraphs, <ul><li> for lists, <strong> for key terms
- No <html>, <head>, <body>, or <style> tags — inner content only
- Bootstrap classes are available (e.g. class="list-group list-group-flush") but keep markup clean

Be factual and specific to Florida college standards. Omit rather than fabricate.\
"""


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
    # Strip markdown code fences if present
    text = re.sub(r"```(?:json)?\s*", "", text).strip()
    # Find outermost { ... }
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
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
        messages=[{"role": "user", "content": build_prompt(course_id, course_info)}],
    )

    text = "".join(
        block.text for block in response.content if hasattr(block, "text")
    )
    return extract_json(text)


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


def push_guide(
    session: requests.Session, course_id: str, data: dict, token: str
) -> None:
    payload = {
        "title": data["title"],
        "htmlContent": data["html_content"],
        "credits": data.get("credits"),
        "contactHours": data.get("contact_hours"),
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
    print(f"  View: {BASE_URL}/courses/{course_id}/guide")


def process_course(
    course_id: str,
    session: requests.Session,
    token: str | None,
    auto_approve: bool,
) -> str | None:
    """Generate and optionally push a guide. Returns a token if one was obtained."""
    course_id = course_id.upper().strip()
    print(f"\n[{course_id}] Fetching course info from repo...")
    info = get_course_info(session, course_id)
    if not info:
        print("  Course not found in taxonomy — generating from course ID only.")

    data = generate_guide(course_id, info)
    display_guide(course_id, data)
    draft_path = save_draft(course_id, data)
    print(f"\n  Draft saved: {draft_path}")

    if auto_approve:
        choice = "y"
    else:
        choice = input("  Push to site? [y / n / e=edit and push later] ").strip().lower()

    if choice == "y":
        if token is None:
            token = get_token(session)
        push_guide(session, course_id, data, token)
    elif choice == "e":
        print(f"  Edit the draft then run:")
        print(f"    python generate_guide.py --push-draft {course_id}")
    else:
        print("  Skipped.")

    return token


def run_push_draft(course_id: str, session: requests.Session) -> None:
    course_id = course_id.upper().strip()
    path = os.path.join(DRAFTS_DIR, f"{course_id}_guide.json")
    if not os.path.exists(path):
        print(f"No draft found at: {path}")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    display_guide(course_id, data)
    choice = input("  Push to site? [y/N] ").strip().lower()
    if choice == "y":
        session_obj = requests.Session()
        token = get_token(session_obj)
        push_guide(session_obj, course_id, data, token)
    else:
        print("  Aborted.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate AI-powered curriculum guides for floridacourserepo.com",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("courses", nargs="*", metavar="COURSE_ID",
                        help="One or more course IDs (e.g. ETS1010)")
    parser.add_argument("--file", "-f", metavar="FILE",
                        help="Text file with one course ID per line (# for comments)")
    parser.add_argument("--push-draft", metavar="COURSE_ID",
                        help="Push a previously saved draft without regenerating")
    parser.add_argument("--yes", "-y", action="store_true",
                        help="Auto-approve all guides without prompting")
    args = parser.parse_args()

    if args.push_draft:
        run_push_draft(args.push_draft, requests.Session())
        return

    course_ids: list[str] = list(args.courses)
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            course_ids += [
                ln.strip()
                for ln in f
                if ln.strip() and not ln.startswith("#")
            ]

    if not course_ids:
        parser.print_help()
        sys.exit(1)

    print(f"Generating guides for {len(course_ids)} course(s): {', '.join(c.upper() for c in course_ids)}")

    session = requests.Session()
    # Authenticate once up front when auto-approving a batch so we don't re-auth every course
    token: str | None = None
    if args.yes and (os.environ.get("REPO_ADMIN_EMAIL")):
        token = get_token(session)

    for cid in course_ids:
        try:
            token = process_course(cid, session, token, auto_approve=args.yes)
        except KeyboardInterrupt:
            print("\nInterrupted.")
            sys.exit(0)
        except json.JSONDecodeError as exc:
            print(f"  ERROR: Could not parse JSON from model response: {exc}")
        except requests.HTTPError as exc:
            print(f"  ERROR: API call failed: {exc.response.status_code} {exc.response.text[:200]}")
        except Exception as exc:
            print(f"  ERROR: {exc}")


if __name__ == "__main__":
    main()
