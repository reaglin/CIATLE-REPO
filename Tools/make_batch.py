#!/usr/bin/env python3
"""
make_batch.py — Build course-ID batch files for generate_guide.py

Filters the master CSV (courses_2plus_institutions.csv) and emits a list of
course IDs, one per line, ready to feed into:
    python generate_guide.py --file <output> --yes

Filters are combinable:
- Within a single filter, values are OR'd      (--prefix ETS TDR  → ETS or TDR)
- Across different filters, values are AND'd   (--prefix ETS --min-inst 5)

Examples:
    # Every ETS course at 5+ schools, write to ets.txt
    python make_batch.py --prefix ETS --min-inst 5 -o ets.txt

    # Just count how many that would be
    python make_batch.py --prefix ETS --min-inst 5 --count

    # Every course offered at Valencia, with titles for review
    python make_batch.py --institution VC --with-titles

    # Three specific courses, skipping any already pushed
    python make_batch.py --course ETS1010 ETS1020 ETS1030 --skip-existing -o batch.txt

    # All Engineering Tech prefixes at 3+ schools, no labs, skip already-done
    python make_batch.py --prefix ETS EET EEV EGN EGS TDR \\
        --min-inst 3 --no-labs --skip-existing -o eng_tech.txt
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(SCRIPT_DIR, "courses_2plus_institutions.csv")
DRAFTS_DIR = os.path.join(SCRIPT_DIR, "drafts")
LOG_FILE = os.path.join(SCRIPT_DIR, "generate_guide.log")


# ---------------------------------------------------------------------------
# Already-pushed detection (mirrors generate_guide.py logic, batched)
# ---------------------------------------------------------------------------

def load_pushed_course_ids() -> set[str]:
    """Return the set of course IDs that have already been pushed to the site.

    Mirrors generate_guide.py.was_guide_pushed():
      1. Drafts with a pushed_utc stamp count as pushed.
      2. Courses with a "[CID] PUSH: Success" line in the log count as pushed.
    """
    pushed: set[str] = set()

    if os.path.isdir(DRAFTS_DIR):
        for fname in os.listdir(DRAFTS_DIR):
            if not fname.endswith("_guide.json"):
                continue
            cid = fname[:-len("_guide.json")].upper()
            path = os.path.join(DRAFTS_DIR, fname)
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("pushed_utc"):
                    pushed.add(cid)
            except Exception:
                continue

    if os.path.exists(LOG_FILE):
        push_re = re.compile(r"\[([A-Z0-9]+)\] PUSH: Success")
        with open(LOG_FILE, encoding="utf-8") as f:
            for line in f:
                m = push_re.search(line)
                if m:
                    pushed.add(m.group(1).upper())

    return pushed


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def parse_institutions(field: str) -> set[str]:
    return {s.strip() for s in field.split(";") if s.strip()}


def matches(
    row: dict,
    *,
    courses: set[str] | None,
    prefixes: list[str] | None,
    institutions: set[str] | None,
    min_inst: int | None,
    max_inst: int | None,
    no_labs: bool,
    labs_only: bool,
) -> bool:
    cid = row["course_id"]

    if courses is not None and cid not in courses:
        return False

    if prefixes and not any(cid.startswith(p) for p in prefixes):
        return False

    if institutions is not None:
        row_insts = parse_institutions(row["institutions"])
        if institutions.isdisjoint(row_insts):
            return False

    n = int(row["num_inst"])
    if min_inst is not None and n < min_inst:
        return False
    if max_inst is not None and n > max_inst:
        return False

    is_lab = cid.endswith("L")
    if no_labs and is_lab:
        return False
    if labs_only and not is_lab:
        return False

    return True


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def render(rows: list[dict], with_titles: bool, header_lines: list[str]) -> str:
    out: list[str] = []
    for line in header_lines:
        out.append(f"# {line}")
    out.append("")

    for r in rows:
        if with_titles:
            out.append(f"# {r['course_id']} — {r['title']} ({r['num_inst']} inst)")
        out.append(r["course_id"])
        if with_titles:
            out.append("")

    return "\n".join(out).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Filter the master course CSV and emit a batch file for generate_guide.py.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    p_filter = parser.add_argument_group("Filters (combinable)")
    p_filter.add_argument("--course", nargs="+", metavar="ID",
                          help="Specific course ID(s) — case-insensitive")
    p_filter.add_argument("--prefix", nargs="+", metavar="ABC",
                          help="Course prefix(es), e.g. ETS, TDR, EET")
    p_filter.add_argument("--institution", nargs="+", metavar="CODE",
                          help="Institution code(s), e.g. VC, MDC, FSCJ — courses offered at ANY of them")
    p_filter.add_argument("--min-inst", type=int, metavar="N",
                          help="Minimum number of institutions offering the course")
    p_filter.add_argument("--max-inst", type=int, metavar="N",
                          help="Maximum number of institutions offering the course")
    p_filter.add_argument("--no-labs", action="store_true",
                          help="Exclude standalone lab courses (course IDs ending in L)")
    p_filter.add_argument("--labs-only", action="store_true",
                          help="Only standalone lab courses (course IDs ending in L)")
    p_filter.add_argument("--skip-existing", action="store_true",
                          help="Skip courses that already have a pushed guide "
                               "(checks drafts/*.json pushed_utc and generate_guide.log)")

    p_io = parser.add_argument_group("Input / output")
    p_io.add_argument("--csv", default=DEFAULT_CSV, metavar="PATH",
                      help=f"Source CSV (default: {os.path.basename(DEFAULT_CSV)} next to this script)")
    p_io.add_argument("-o", "--output", metavar="FILE",
                      help="Write to FILE (default: stdout)")
    p_io.add_argument("--with-titles", action="store_true",
                      help="Include each course's title as a comment line above its ID")
    p_io.add_argument("--count", action="store_true",
                      help="Print only the match count to stdout; do not emit course IDs")

    args = parser.parse_args()

    if args.no_labs and args.labs_only:
        parser.error("--no-labs and --labs-only are mutually exclusive")

    if not os.path.exists(args.csv):
        parser.error(f"CSV not found: {args.csv}\n"
                     f"Run extract_courses.py first, or pass --csv PATH.")

    courses = {c.upper() for c in args.course} if args.course else None
    prefixes = [p.upper() for p in args.prefix] if args.prefix else None
    institutions = {i.upper() for i in args.institution} if args.institution else None

    pushed = load_pushed_course_ids() if args.skip_existing else set()

    matched: list[dict] = []
    skipped_pushed = 0

    with open(args.csv, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if not matches(
                row,
                courses=courses,
                prefixes=prefixes,
                institutions=institutions,
                min_inst=args.min_inst,
                max_inst=args.max_inst,
                no_labs=args.no_labs,
                labs_only=args.labs_only,
            ):
                continue
            if args.skip_existing and row["course_id"].upper() in pushed:
                skipped_pushed += 1
                continue
            matched.append(row)

    # Build a header describing what produced this list (helpful when re-reading old batches)
    criteria: list[str] = []
    if courses: criteria.append(f"courses={','.join(sorted(courses))}")
    if prefixes: criteria.append(f"prefixes={','.join(prefixes)}")
    if institutions: criteria.append(f"institutions={','.join(sorted(institutions))}")
    if args.min_inst is not None: criteria.append(f"min_inst={args.min_inst}")
    if args.max_inst is not None: criteria.append(f"max_inst={args.max_inst}")
    if args.no_labs: criteria.append("no_labs")
    if args.labs_only: criteria.append("labs_only")
    if args.skip_existing: criteria.append(f"skip_existing (excluded {skipped_pushed})")
    criteria_str = "; ".join(criteria) if criteria else "no filters (entire CSV)"

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    header_lines = [
        f"Generated by make_batch.py at {ts}",
        f"Filters: {criteria_str}",
        f"Matches: {len(matched)} course(s)",
    ]

    # --count mode: write summary to stdout, nothing else
    if args.count:
        print(f"Matches: {len(matched)}")
        if args.skip_existing:
            print(f"Excluded (already pushed): {skipped_pushed}")
        return

    body = render(matched, args.with_titles, header_lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(body)
        # Status to stderr so it doesn't contaminate piped output
        print(f"Wrote {len(matched)} course ID(s) → {args.output}", file=sys.stderr)
        if args.skip_existing and skipped_pushed:
            print(f"Excluded {skipped_pushed} already-pushed course(s).", file=sys.stderr)
    else:
        sys.stdout.write(body)


if __name__ == "__main__":
    main()
