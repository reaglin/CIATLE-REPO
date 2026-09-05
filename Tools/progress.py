#!/usr/bin/env python3
"""Progress report for the curriculum guide project.

Reports the running totals: how many guides are live, how much of the queue
remains, and how the Daytona State priority is tracking. Reads queue.csv and
activity.log; no network calls.

Usage:
    python progress.py
    python progress.py --since 2026-08-30    # count pushes on/after a date
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from datetime import date
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
QUEUE = TOOLS / "queue.csv"
ACTIVITY = TOOLS / "activity.log"

DSC_NOTES = ("Daytona State College project",)


def load_queue() -> list[dict]:
    with QUEUE.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def bar(done: int, total: int, width: int = 32) -> str:
    if total <= 0:
        return ""
    filled = round(width * done / total)
    return "[" + "#" * filled + "-" * (width - filled) + f"] {done/total:5.1%}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--since", help="count pushes on or after this ISO date (YYYY-MM-DD)")
    args = ap.parse_args()

    rows = load_queue()
    status = Counter(r["status"] for r in rows)
    pushed = status["pushed"]
    queued = status["queued"]
    skipped = status["skipped"]
    errors = status["error"]

    # Work in scope = everything we intend to publish (pushed + queued + any errors)
    in_scope = pushed + queued + errors

    print("=" * 62)
    print(" Florida Course Repository - curriculum guide progress")
    print("=" * 62)
    print(f"  Guides live on the site   {pushed:>6}")
    print(f"  Still queued              {queued:>6}")
    if errors:
        print(f"  Errors to resolve         {errors:>6}")
    print(f"  Skipped (deliberate)      {skipped:>6}")
    print(f"  {'-'*56}")
    print(f"  Queue total               {len(rows):>6}")
    print()
    print(f"  Overall  {bar(pushed, in_scope)}   {pushed}/{in_scope}")

    # Daytona State priority
    dsc = [r for r in rows if any(r["notes"].startswith(n) for n in DSC_NOTES)]
    if dsc:
        d_pushed = sum(1 for r in dsc if r["status"] == "pushed")
        d_queued = sum(1 for r in dsc if r["status"] == "queued")
        d_skipped = sum(1 for r in dsc if r["status"] == "skipped")
        d_scope = d_pushed + d_queued
        print(f"  Daytona  {bar(d_pushed, d_scope)}   {d_pushed}/{d_scope}"
              f"   ({d_skipped} skipped)")

    # Push activity from the audit log
    if ACTIVITY.exists():
        pushes = re.findall(r"^(\d{4}-\d{2}-\d{2})T[\d:]+Z\s+push\s+PUSHED ",
                            ACTIVITY.read_text(encoding="utf-8", errors="replace"), re.M)
        if pushes:
            by_day = Counter(pushes)
            print()
            print("  Recent push activity:")
            for day in sorted(by_day)[-7:]:
                print(f"    {day}   {by_day[day]:>4} guide(s)")
            if args.since:
                n = sum(v for d, v in by_day.items() if d >= args.since)
                print(f"\n  Pushed since {args.since}: {n}")
            print(f"  Total push events logged: {len(pushes)}")

    # What is left, by how widely offered
    if queued:
        nums = [int(r["num_inst"]) for r in rows
                if r["status"] == "queued" and r["num_inst"].isdigit()]
        if nums:
            print()
            print(f"  Remaining queued span {min(nums)}-{max(nums)} institutions;"
                  f" next up is {max(nums)}-institution work.")
    print("=" * 62)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
