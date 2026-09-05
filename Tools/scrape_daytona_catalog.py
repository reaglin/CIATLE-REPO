#!/usr/bin/env python3
"""Scrape the Daytona State College catalog course list.

The catalog's course-descriptions page is an index of subject-prefix pages;
each prefix page lists its courses as:

    <li><a href="..."><span>AST1002</span> Astronomy</a></li>

This walks the index, fetches each prefix page, and writes course_id/title/prefix
to a CSV. Polite by default: one request at a time with a delay between them.

Usage:
    python scrape_daytona_catalog.py
    python scrape_daytona_catalog.py --out daytona_courses.csv --delay 0.5
    python scrape_daytona_catalog.py --limit 5        # smoke test on 5 prefixes

Output feeds compare_daytona.py, which diffs it against the queue and the
statewide inventory to find courses only Daytona offers.
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
import time
from pathlib import Path

import requests

TOOLS = Path(__file__).resolve().parent
BASE = "https://daytonastate.smartcatalogiq.com"
INDEX = f"{BASE}/en/2025-2026/college-catalog/course-descriptions"

# Prefix-page links off the index: .../course-descriptions/<slug> (one path segment).
PREFIX_RE = re.compile(
    r'href="(/en/[^"]*?/course-descriptions/([a-z0-9][a-z0-9\-]*))"', re.I
)
# Course entries: <span>ABC1234C</span> Title
COURSE_RE = re.compile(
    r"<span>\s*([A-Z]{3}\s?\d{4}[A-Z]?)\s*</span>\s*([^<]*)", re.I
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; FloridaCourseRepo/1.0; +https://floridacourserepo.com)"
}


def get(session: requests.Session, url: str, retries: int = 3) -> str | None:
    for attempt in range(retries):
        try:
            r = session.get(url, timeout=30)
            if r.status_code == 200:
                return r.text
            if r.status_code == 404:
                return None
            print(f"    HTTP {r.status_code} for {url}", file=sys.stderr)
        except requests.RequestException as exc:
            print(f"    {type(exc).__name__} on {url} (attempt {attempt+1})", file=sys.stderr)
        time.sleep(2 * (attempt + 1))
    return None


def clean_title(raw: str) -> str:
    t = html.unescape(raw).replace(" ", " ")
    t = re.sub(r"\s+", " ", t).strip(" -–—\t")
    return t.strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(TOOLS / "daytona_courses.csv"))
    ap.add_argument("--delay", type=float, default=0.5, help="seconds between requests")
    ap.add_argument("--limit", type=int, help="only scrape the first N prefix pages")
    args = ap.parse_args()

    session = requests.Session()
    session.headers.update(HEADERS)

    print(f"Fetching index: {INDEX}")
    index_html = get(session, INDEX)
    if not index_html:
        print("Could not fetch the catalog index.", file=sys.stderr)
        return 1

    # Dedupe prefix pages, preserving order. Skip the index itself.
    seen, prefixes = set(), []
    for path, slug in PREFIX_RE.findall(index_html):
        if slug.lower() == "course-descriptions" or path in seen:
            continue
        seen.add(path)
        prefixes.append(path)

    if args.limit:
        prefixes = prefixes[: args.limit]
    print(f"Found {len(prefixes)} subject-prefix pages.\n")

    courses: dict[str, tuple[str, str]] = {}   # course_id -> (title, slug)
    empty: list[str] = []

    for i, path in enumerate(prefixes, 1):
        slug = path.rsplit("/", 1)[-1]
        page = get(session, BASE + path)
        if page is None:
            print(f"  [{i}/{len(prefixes)}] {slug}: FETCH FAILED", file=sys.stderr)
            continue
        found = 0
        for code, title in COURSE_RE.findall(page):
            cid = code.replace(" ", "").upper()
            title = clean_title(title)
            if not title:
                continue
            if cid not in courses:
                courses[cid] = (title, slug)
                found += 1
        if found == 0:
            empty.append(slug)
        print(f"  [{i}/{len(prefixes)}] {slug}: {found} course(s)")
        time.sleep(args.delay)

    out = Path(args.out)
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["course_id", "title", "prefix", "subject_page"])
        for cid in sorted(courses):
            title, slug = courses[cid]
            w.writerow([cid, title, cid[:3], slug])

    print(f"\nWrote {out} with {len(courses)} unique course(s) from {len(prefixes)} prefix page(s).")
    if empty:
        print(f"{len(empty)} page(s) yielded no courses: {', '.join(empty[:12])}"
              + (" ..." if len(empty) > 12 else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
