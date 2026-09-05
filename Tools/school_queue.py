#!/usr/bin/env python3
"""school_queue.py — derive a per-school work queue from the master queue.

The master (`queue.csv`) stays the single source of truth for what is DONE.
This tool answers a different question: *what can I work on at school X right now?*

    python school_queue.py coverage                 # which schools have work, and how much
    python school_queue.py build UNF                # write queue_UNF.csv
    python school_queue.py build UNF --limit 300
    python school_queue.py status                   # per-school queue files on disk

Why this exists (Ron, 2026-09-04): when a school's catalog is bot-blocked we need
another school's work ready to promote, rather than stalling. Build queues for two
or three schools ahead of time and switch when one blocks.

DEDUPLICATION: a course already `pushed` or `skipped` in the master is NOT emitted
for any school. The exception is a deliberate one-number-two-subjects split, which
is handled by publishing `XXXnnnn-<INST>` ids (see Tools/CLAUDE.md) rather than by
re-queueing the bare number.
"""
from __future__ import annotations
import argparse, collections, csv, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(HERE, "queue.csv")
INVENTORY = os.path.join(HERE, "courses_2plus_institutions.csv")
DONE = {"pushed", "skipped"}


def _read(path: str) -> list[dict]:
    with io.open(path, encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def load() -> tuple[dict, dict]:
    master = {r["course_id"]: r for r in _read(MASTER)}
    inv = {}
    for r in _read(INVENTORY):
        insts = {i.strip() for i in (r.get("institutions") or "").split(";") if i.strip()}
        inv[r["course_id"]] = {"title": r.get("title", ""),
                               "num_inst": int(r.get("num_inst") or 0),
                               "institutions": insts}
    return master, inv


def workable(master: dict, inv: dict, school: str) -> list[dict]:
    """Inventory courses offered at `school` that the master has not finished."""
    out = []
    for cid, meta in inv.items():
        if school not in meta["institutions"]:
            continue
        m = master.get(cid)
        if m and m["status"] in DONE:
            continue
        out.append({"course_id": cid, "title": meta["title"],
                    "num_inst": meta["num_inst"],
                    "in_master": "yes" if m else "no",
                    "master_status": m["status"] if m else "",
                    "institutions": ";".join(sorted(meta["institutions"]))})
    out.sort(key=lambda r: (-r["num_inst"], r["course_id"]))
    return out


def cmd_coverage(args) -> None:
    master, inv = load()
    tally, done = collections.Counter(), collections.Counter()
    for cid, meta in inv.items():
        m = master.get(cid)
        finished = bool(m and m["status"] in DONE)
        for i in meta["institutions"]:
            tally[i] += 1
            if finished:
                done[i] += 1
    print(f"{'SCHOOL':8} {'OFFERS':>7} {'DONE':>7} {'WORKABLE':>9}  {'%DONE':>6}")
    for i, n in tally.most_common(args.top):
        rem = n - done[i]
        pct = (done[i] / n * 100) if n else 0
        print(f"{i:8} {n:7} {done[i]:7} {rem:9}  {pct:5.1f}%")


def cmd_build(args) -> None:
    master, inv = load()
    rows = workable(master, inv, args.school)
    if args.limit:
        rows = rows[: args.limit]
    out = os.path.join(HERE, f"queue_{args.school}.csv")
    with io.open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["course_id", "title", "num_inst",
                                           "in_master", "master_status", "institutions"])
        w.writeheader()
        w.writerows(rows)
    already = sum(1 for r in rows if r["in_master"] == "yes")
    print(f"wrote {out}: {len(rows)} workable course(s)")
    print(f"  {already} already in the master queue (queued/error), {len(rows) - already} new to it")
    if rows:
        print("  top of queue:")
        for r in rows[:8]:
            print(f"    {r['course_id']:10} {r['num_inst']:>3} inst  {r['title'][:46]}")


def cmd_status(args) -> None:
    found = False
    for f in sorted(os.listdir(HERE)):
        if f.startswith("queue_") and f.endswith(".csv"):
            n = len(_read(os.path.join(HERE, f)))
            print(f"  {f:24} {n} row(s)")
            found = True
    if not found:
        print("  no per-school queue files yet — run: python school_queue.py build <SCHOOL>")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("coverage", help="per-school workable counts")
    c.add_argument("--top", type=int, default=25)
    c.set_defaults(func=cmd_coverage)
    b = sub.add_parser("build", help="write queue_<SCHOOL>.csv")
    b.add_argument("school")
    b.add_argument("--limit", type=int, default=0)
    b.set_defaults(func=cmd_build)
    s = sub.add_parser("status", help="list per-school queue files")
    s.set_defaults(func=cmd_status)
    a = p.parse_args()
    a.school = getattr(a, "school", "").upper() if hasattr(a, "school") else None
    a.func(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
