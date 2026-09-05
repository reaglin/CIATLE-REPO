#!/usr/bin/env python3
"""Diff the scraped Daytona catalog against the queue and the statewide inventory.

Identifies which Daytona courses are not yet accounted for, and in particular
the "Daytona-only" ones: courses absent from courses_2plus_institutions.csv
because fewer than two Florida institutions offer them.

Matching note: extract_courses.py merges ABC1234 and ABC1234C into the C-form
(keeping ABC1234L separate), so a catalog's "OCE1001" is the inventory's
"OCE1001C". Comparison is therefore done on a normalized key that folds a
trailing C but preserves a trailing L.

Usage:
    python compare_daytona.py
    python compare_daytona.py --write-queue      # append Daytona-only courses to queue.csv
"""

from __future__ import annotations

import argparse
import csv
import datetime
import re
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SCRAPED = TOOLS / "daytona_courses.csv"
INVENTORY = TOOLS / "courses_2plus_institutions.csv"
QUEUE = TOOLS / "queue.csv"

NOTE = "Daytona State College project - DSC-only"
PRIORITY = 960  # below the 930-950 DSC main band, above the 978+ general queue

SHELL_CODE = re.compile(r"[A-Z]{3}\d?(9\d{2})[CL]?$")
SHELL_KW = ("INTERNSHIP", "COOPERATIVE", "SPECIAL TOPICS", "INDEPENDENT STUDY",
            "DIRECTED STUDY", "DIRECTED INDIVIDUAL", "THESIS", "DISSERTATION",
            "SUPERVISED RESEARCH")


def norm(cid: str) -> str:
    """Fold a trailing C (merged by extract_courses.py); keep a trailing L distinct."""
    return cid[:-1] if cid.endswith("C") else cid


def is_shell(cid: str, title: str) -> bool:
    return bool(SHELL_CODE.search(cid)) or any(k in title.upper() for k in SHELL_KW)


def is_applied_music(cid: str) -> bool:
    return cid[:2] == "MV" or cid[:3] == "MUN"


def load(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write-queue", action="store_true", help="append Daytona-only courses to queue.csv")
    args = ap.parse_args()

    scraped = load(SCRAPED)
    inventory = load(INVENTORY)
    queue = load(QUEUE)

    inv_by_norm = {norm(r["course_id"]): r for r in inventory}
    queue_norm = {norm(r["course_id"]) for r in queue}
    queue_ids = {r["course_id"] for r in queue}

    in_queue, in_inventory_only, daytona_only = [], [], []
    for r in scraped:
        cid, title = r["course_id"], r["title"]
        n = norm(cid)
        if n in queue_norm:
            in_queue.append(r)
        elif n in inv_by_norm:
            in_inventory_only.append(r)
        else:
            daytona_only.append(r)

    print(f"Scraped Daytona catalog:        {len(scraped)}")
    print(f"  already in queue.csv:         {len(in_queue)}")
    print(f"  in statewide inventory only:  {len(in_inventory_only)}  (2+ institutions, not yet queued)")
    print(f"  DAYTONA-ONLY (not in inv.):   {len(daytona_only)}")

    shell = [r for r in daytona_only if is_shell(r["course_id"], r["title"])]
    music = [r for r in daytona_only if not is_shell(r["course_id"], r["title"]) and is_applied_music(r["course_id"])]
    keep = [r for r in daytona_only if r not in shell and r not in music]
    print(f"\n  of the Daytona-only set:")
    print(f"     shell courses:             {len(shell)}")
    print(f"     applied music/ensemble:    {len(music)}")
    print(f"     queueable:                 {len(keep)}")

    from collections import Counter
    pre = Counter(r["prefix"] for r in keep)
    print("\n  top Daytona-only prefixes: " + ", ".join(f"{k}({v})" for k, v in pre.most_common(12)))

    # The "inventory only" group is a stale-data finding worth acting on: Daytona's
    # current catalog lists these, but the statewide inventory does not name DSC among
    # their institutions. They are multi-institution courses, so they earn the main
    # DSC band (930 + 22 - num_inst) rather than the Daytona-only priority.
    if in_inventory_only:
        print("\n  Daytona teaches these but the inventory does not list DSC (stale inventory):")
        for r in in_inventory_only:
            m = inv_by_norm[norm(r["course_id"])]
            print(f"     {r['course_id']:<10} inst={m['num_inst']:<3} {r['title'][:44]}")

    if not args.write_queue:
        print("\n(dry run - pass --write-queue to append these to queue.csv)")
        return 0

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fields = list(queue[0].keys())
    shell_ids = {id(r) for r in shell}
    music_ids = {id(r) for r in music}
    added = n_queued = n_skipped = 0

    with QUEUE.open("a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)

        for r in keep + shell + music:
            if r["course_id"] in queue_ids:
                continue
            skipped = id(r) in shell_ids or id(r) in music_ids
            reason = "shell course" if id(r) in shell_ids else "applied music/ensemble"
            w.writerow({
                "course_id": r["course_id"], "title": r["title"], "num_inst": "1",
                "status": "skipped" if skipped else "queued",
                "priority": str(PRIORITY), "added_utc": now,
                "drafted_utc": "", "pushed_utc": "",
                "notes": NOTE + (f" - skipped: {reason}" if skipped else ""),
            })
            queue_ids.add(r["course_id"]); added += 1
            n_skipped += skipped; n_queued += not skipped

        for r in in_inventory_only:
            if r["course_id"] in queue_ids:
                continue
            m = inv_by_norm[norm(r["course_id"])]
            n = int(m["num_inst"]) if m.get("num_inst") else 2
            w.writerow({
                "course_id": r["course_id"], "title": r["title"], "num_inst": m["num_inst"],
                "status": "queued", "priority": str(930 + max(0, 22 - n)),
                "added_utc": now, "drafted_utc": "", "pushed_utc": "",
                "notes": "Daytona State College project - in catalog, inventory missing DSC",
            })
            queue_ids.add(r["course_id"]); added += 1; n_queued += 1

    print(f"\nAppended {added} row(s) to queue.csv: {n_queued} queued, {n_skipped} skipped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
