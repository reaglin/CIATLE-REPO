#!/usr/bin/env python3
"""Preflight validator for curriculum guide drafts.

Mirrors the server-side rules in
PreseMakerRepo.Api/Validators/PublishValidators.cs
(UpsertCurriculumGuideRequestValidator) plus the local push guard in
generate_guide.py, so a draft that passes here will not come back as an
HTTP 400 from the push.

Usage:
    python validate_drafts.py                 # every file in drafts/
    python validate_drafts.py EEV0140 ACR0045 # named courses only
    python validate_drafts.py --drafted       # only queue rows in 'drafted'
    python validate_drafts.py --errors        # only queue rows in 'error'
    python validate_drafts.py --quiet         # print failures only

Exit code 0 when everything checked is publishable, 1 otherwise.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
DRAFTS = TOOLS / "drafts"
QUEUE = TOOLS / "queue.csv"

REQUIRED_KEYS = {
    "title",
    "html_content",
    "credits",
    "contact_hours",
    "prerequisites",
    "version",
}

# Keys the pipeline itself adds to a draft after a successful push
# (generate_guide.mark_draft_pushed) — present by design, not a schema violation.
STAMP_KEYS = {"pushed_utc"}

# Optional keys: valid in a draft, not required.
#
# offering_notes (Ron, 2026-09-11) — per-school offering data: what each institution
# calls the course, its INTEGER credit value, its contact hours, and any note. The
# server does not carry this field yet (PUT /courses/{id}/guide takes the six scalars
# and drops anything else), so a draft carrying it publishes fine and the field simply
# does not reach the site until the server change lands. See
# Deployment/PENDING_SERVER_CHANGES.md. Until then the same content is also written
# into the guide HTML as an "Offering Notes" section.
OPTIONAL_KEYS = {"offering_notes"}

# Server-side bounds (PublishValidators.cs lines 103-107).
MAX_TITLE = 300
MAX_PREREQ = 1000          # raised from 500 on 2026-09-11; mirrors the server rule
MAX_VERSION = 50
CREDITS_RANGE = (0, 12)
CONTACT_HOURS_RANGE = (0, 1500)

# Document-level tags the schema forbids: html_content is inner content only.
FORBIDDEN_TAGS = ("<html", "<head", "<body", "<style", "<!doctype")

COURSE_ID_RE = re.compile(r"^[A-Z]{3}[0-9]{4}[CL]?(?:-(?:SCNS|[A-Z]{2,5}))?$")

CANONICAL_SECTIONS = (
    "Course Description",
    "Learning Outcomes",
    "Major Topics",
)


def load_queue() -> dict[str, dict]:
    if not QUEUE.exists():
        return {}
    with QUEUE.open(encoding="utf-8-sig", newline="") as fh:
        return {r["course_id"]: r for r in csv.DictReader(fh)}


def check(path: Path) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for one draft file."""
    errors: list[str] = []
    warnings: list[str] = []

    course_id = path.name[: -len("_guide.json")]
    if not COURSE_ID_RE.match(course_id):
        warnings.append(f"filename course id {course_id!r} is not a standard SCNS code")

    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return [f"not valid JSON: {exc}"], warnings

    if not isinstance(data, dict):
        return ["top level is not a JSON object"], warnings

    keys = set(data)
    missing = REQUIRED_KEYS - keys
    extra = keys - REQUIRED_KEYS - STAMP_KEYS - OPTIONAL_KEYS
    if missing:
        errors.append(f"missing key(s): {', '.join(sorted(missing))}")
    if extra:
        warnings.append(f"unexpected key(s): {', '.join(sorted(extra))}")

    # --- offering_notes (optional) -----------------------------------------
    notes = data.get("offering_notes")
    if notes is not None:
        if not isinstance(notes, dict):
            errors.append("offering_notes is not a JSON object")
        else:
            rows = notes.get("offerings")
            if not isinstance(rows, list) or not rows:
                errors.append("offering_notes.offerings is missing or empty")
            else:
                for i, row in enumerate(rows):
                    where = f"offering_notes.offerings[{i}]"
                    if not isinstance(row, dict):
                        errors.append(f"{where} is not an object")
                        continue
                    inst = row.get("institution")
                    if not isinstance(inst, str) or not inst.strip():
                        errors.append(f"{where}.institution is empty")
                    elif len(inst) > 10:
                        errors.append(f"{where}.institution {inst!r} is over 10 chars")
                    t = row.get("title")
                    if t is not None and (not isinstance(t, str) or len(t) > 300):
                        errors.append(f"{where}.title is not a string of <= 300 chars")
                    cr = row.get("credits")
                    # Ron, 2026-09-11: credit hours are INTEGERS. 3.0 is a formatting
                    # artefact of the SCNS flat file, not a different value.
                    if cr is not None and not isinstance(cr, int):
                        errors.append(
                            f"{where}.credits is {cr!r} — credit hours must be integers"
                        )
                    elif isinstance(cr, int) and not 0 <= cr <= 20:
                        errors.append(f"{where}.credits {cr} is outside 0-20")
                    ch = row.get("contact_hours")
                    if ch is not None and (not isinstance(ch, int) or not 0 <= ch <= 3000):
                        errors.append(f"{where}.contact_hours is not an integer in 0-3000")
            src = notes.get("hours_source")
            if src is not None and src not in ("published", "derived", "mixed"):
                errors.append(
                    "offering_notes.hours_source must be published, derived or mixed"
                )
            elif src is None:
                warnings.append(
                    "offering_notes has no hours_source — say whether hours are "
                    "published by the institutions or derived by convention"
                )

    # --- title -------------------------------------------------------------
    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append("title is empty or not a string")
    elif len(title) > MAX_TITLE:
        errors.append(f"title is {len(title)} chars (server max {MAX_TITLE})")

    # --- html_content ------------------------------------------------------
    html = data.get("html_content")
    if not isinstance(html, str) or not html.strip():
        errors.append("html_content is empty or not a string")
    else:
        lowered = html.lower()
        for tag in FORBIDDEN_TAGS:
            if tag in lowered:
                errors.append(f"html_content contains a document-level tag: {tag}>")
        for section in CANONICAL_SECTIONS:
            if section.lower() not in lowered:
                warnings.append(f"no '{section}' section found")
        if len(html) < 1500:
            warnings.append(f"html_content is only {len(html)} chars — unusually thin")

    # --- credits -----------------------------------------------------------
    credits = data.get("credits")
    lo, hi = CREDITS_RANGE
    if credits is None:
        # generate_guide.push_guide rejects None outright, before the server sees it.
        errors.append("credits is null (push_guide requires an int 0-12)")
    elif isinstance(credits, bool) or not isinstance(credits, int):
        errors.append(f"credits={credits!r} is not an integer")
    elif not (lo <= credits <= hi):
        errors.append(f"credits={credits} is outside the valid range {lo}-{hi}")

    # --- contact_hours -----------------------------------------------------
    hours = data.get("contact_hours")
    lo_h, hi_h = CONTACT_HOURS_RANGE
    if hours is None:
        warnings.append("contact_hours is null — the site will show no hour count")
    elif isinstance(hours, bool) or not isinstance(hours, int):
        errors.append(f"contact_hours={hours!r} is not an integer")
    elif not (lo_h <= hours <= hi_h):
        errors.append(
            f"contact_hours={hours} is outside the server range {lo_h}-{hi_h}"
        )

    # --- prerequisites / version ------------------------------------------
    prereq = data.get("prerequisites")
    if prereq is not None:
        if not isinstance(prereq, str):
            errors.append(f"prerequisites={prereq!r} is neither a string nor null")
        elif len(prereq) > MAX_PREREQ:
            errors.append(f"prerequisites is {len(prereq)} chars (server max {MAX_PREREQ})")

    version = data.get("version")
    if version is not None and not isinstance(version, str):
        errors.append(f"version={version!r} is not a string")
    elif isinstance(version, str) and len(version) > MAX_VERSION:
        errors.append(f"version is {len(version)} chars (server max {MAX_VERSION})")

    # --- cross-field sanity ------------------------------------------------
    if isinstance(credits, int) and isinstance(hours, int):
        if credits > 0 and credits == hours:
            warnings.append(
                f"credits == contact_hours == {credits}: looks like the clock-hour "
                f"count was copied into credits (PSAV courses want credits=0)"
            )
        elif credits == 3 and not (40 <= hours <= 70):
            warnings.append(f"3 credits with {hours} contact hours (expected ~45, or ~60 for a C course)")
        elif credits == 1 and not (15 <= hours <= 50):
            warnings.append(f"1 credit with {hours} contact hours (expected ~30-45 for an L course)")

    if course_id.endswith("C") and isinstance(credits, int) and credits == 3 and isinstance(hours, int) and hours < 55:
        warnings.append(f"'{course_id}' is an integrated lecture+lab (C) course but has only {hours} contact hours")

    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("courses", nargs="*", help="course ids to check (default: all drafts)")
    ap.add_argument("--drafted", action="store_true", help="check only queue rows with status=drafted")
    ap.add_argument("--errors", action="store_true", help="check only queue rows with status=error")
    ap.add_argument("--quiet", action="store_true", help="print failures only")
    args = ap.parse_args()

    if not DRAFTS.is_dir():
        print(f"No drafts directory at {DRAFTS}", file=sys.stderr)
        return 1

    if args.courses:
        paths = [DRAFTS / f"{c.upper()}_guide.json" for c in args.courses]
    elif args.drafted or args.errors:
        want = "drafted" if args.drafted else "error"
        queue = load_queue()
        ids = [cid for cid, row in queue.items() if row.get("status") == want]
        paths = [DRAFTS / f"{cid}_guide.json" for cid in sorted(ids)]
        if not paths:
            print(f"No queue rows with status={want}.")
            return 0
    else:
        paths = sorted(DRAFTS.glob("*_guide.json"))

    n_ok = n_warn = n_fail = 0
    missing_files: list[str] = []

    for path in paths:
        if not path.exists():
            missing_files.append(path.name)
            n_fail += 1
            continue
        errors, warnings = check(path)
        course_id = path.name[: -len("_guide.json")]
        if errors:
            n_fail += 1
            print(f"FAIL  {course_id}")
            for e in errors:
                print(f"        error:   {e}")
            for w in warnings:
                print(f"        warning: {w}")
        elif warnings:
            n_warn += 1
            if not args.quiet:
                print(f"WARN  {course_id}")
                for w in warnings:
                    print(f"        warning: {w}")
        else:
            n_ok += 1
            if not args.quiet:
                print(f"OK    {course_id}")

    if missing_files:
        print("\nMissing draft file(s):")
        for name in missing_files:
            print(f"  {name}")

    total = len(paths)
    print(f"\n{total} draft(s) checked: {n_ok} clean, {n_warn} clean-with-warnings, {n_fail} blocking.")
    if n_fail:
        print("Blocking drafts will be rejected by the push. Fix them before running --push-from-queue.")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
