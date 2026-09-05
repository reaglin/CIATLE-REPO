#!/usr/bin/env python3
"""Render draft guides to a single local HTML page for review.

Writes a self-contained file (Bootstrap from CDN) showing each guide as it
will appear on the site, with its metadata in a header card. Nothing is
published and nothing is sent anywhere -- this is a local review aid.

Usage:
    python preview_drafts.py CJK0330 CJK0335        # named courses
    python preview_drafts.py --drafted              # everything staged to push
    python preview_drafts.py --drafted --open       # ...and open it in a browser

Default output is preview.html in this directory (gitignored).
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import sys
import webbrowser
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
DRAFTS = TOOLS / "drafts"
QUEUE = TOOLS / "queue.csv"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Curriculum guide preview</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
  body {{ background:#f6f7f9; }}
  .guide {{ background:#fff; border-radius:.5rem; padding:2rem 2.5rem; margin-bottom:2.5rem;
            box-shadow:0 1px 3px rgba(0,0,0,.08); }}
  .guide h2 {{ margin-top:2rem; padding-bottom:.35rem; border-bottom:2px solid #e9ecef;
               font-size:1.5rem; }}
  .guide h2:first-of-type {{ margin-top:1rem; }}
  .guide h3 {{ margin-top:1.25rem; font-size:1.15rem; color:#495057; }}
  .meta {{ background:#eef2f7; border-left:4px solid #0d6efd; padding:1rem 1.25rem;
           border-radius:.25rem; margin-bottom:1rem; }}
  .toc {{ position:sticky; top:1rem; }}
  code {{ font-size:.85em; }}
</style>
</head>
<body>
<div class="container py-4">
  <h1 class="mb-1">Curriculum guide preview</h1>
  <p class="text-muted">{count} guide(s) &mdash; local review copy, nothing published.</p>
  <div class="alert alert-secondary py-2"><strong>Contents:</strong> {toc}</div>
  {body}
</div>
</body>
</html>
"""


def load_queue_ids(state: str) -> list[str]:
    if not QUEUE.exists():
        return []
    with QUEUE.open(encoding="utf-8-sig", newline="") as fh:
        return sorted(r["course_id"] for r in csv.DictReader(fh) if r.get("status") == state)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("courses", nargs="*", help="course ids (default: all drafts)")
    ap.add_argument("--drafted", action="store_true", help="preview queue rows with status=drafted")
    ap.add_argument("--errors", action="store_true", help="preview queue rows with status=error")
    ap.add_argument("-o", "--out", default=str(TOOLS / "preview.html"), help="output file")
    ap.add_argument("--open", dest="open_browser", action="store_true", help="open in the default browser")
    args = ap.parse_args()

    if args.courses:
        ids = [c.upper() for c in args.courses]
    elif args.drafted or args.errors:
        ids = load_queue_ids("drafted" if args.drafted else "error")
    else:
        ids = sorted(p.name[: -len("_guide.json")] for p in DRAFTS.glob("*_guide.json"))

    if not ids:
        print("Nothing to preview.", file=sys.stderr)
        return 1

    sections, toc_parts = [], []
    for cid in ids:
        path = DRAFTS / f"{cid}_guide.json"
        if not path.exists():
            print(f"  skipping {cid}: no draft file", file=sys.stderr)
            continue
        d = json.loads(path.read_text(encoding="utf-8-sig"))
        credits = d.get("credits")
        hours = d.get("contact_hours")
        prereq = d.get("prerequisites")
        # PSAV courses carry credits=0; label them rather than showing "0 credit hours".
        credit_label = (
            f"{credits} credit hours" if isinstance(credits, int) and credits > 0
            else "PSAV clock-hour course (0 credits)"
        )
        meta = (
            f'<div class="meta">'
            f'<div class="fw-bold fs-5">{html.escape(cid)} &mdash; {html.escape(str(d.get("title","")))}</div>'
            f'<div class="mt-2"><span class="badge bg-primary">{html.escape(credit_label)}</span> '
            f'<span class="badge bg-secondary">{hours} contact hours</span> '
            f'<span class="badge bg-light text-dark border">v{html.escape(str(d.get("version","")))}</span> '
            f'<span class="badge bg-light text-dark border">{len(d.get("html_content",""))} chars</span></div>'
            f'<div class="mt-2 small"><strong>Prerequisites:</strong> '
            f'{html.escape(prereq) if prereq else "<em>none</em>"}</div>'
            f"</div>"
        )
        sections.append(f'<div class="guide" id="{html.escape(cid)}">{meta}{d.get("html_content","")}</div>')
        toc_parts.append(f'<a href="#{html.escape(cid)}">{html.escape(cid)}</a>')

    out = Path(args.out)
    out.write_text(
        PAGE.format(count=len(sections), toc=" &middot; ".join(toc_parts), body="\n".join(sections)),
        encoding="utf-8",
    )
    print(f"Wrote {out} ({len(sections)} guide(s))")
    if args.open_browser:
        webbrowser.open(out.resolve().as_uri())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
