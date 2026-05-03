#!/usr/bin/env python3
"""
queue_mgr.py -- Manage the curriculum-guide generation queue.

Tracks every course's progress through the pipeline:
    queued -> drafted -> pushed
              \\-> skipped / error

State lives in two files alongside this script:
    queue.csv      -- current state of every course in the pipeline
    activity.log   -- append-only timestamped event history

Workflows:

    # Add courses to the queue
    python queue_mgr.py add --course MAC1105C ENC1101C
    python queue_mgr.py add --prefix EGN --min-inst 5
    python queue_mgr.py add --top 11                      # next N priority not yet queued
    python queue_mgr.py add --institution VC --min-inst 10

    # See where everything stands
    python queue_mgr.py status                            # summary counts + next 10 by state
    python queue_mgr.py status --state queued             # full list of queued courses
    python queue_mgr.py list --state drafted              # course IDs only, one per line

    # Manage existing entries
    python queue_mgr.py mark COURSE_ID --state STATE [--note "..."]
    python queue_mgr.py reconcile                         # update from drafts/ folder + log
    python queue_mgr.py remove COURSE_ID

    # Hand-off to generate_guide.py
    python queue_mgr.py next-batch [--n 5]                # course IDs ready to draft
    python queue_mgr.py ready-to-push                     # course IDs ready to push

Reconcile is the source-of-truth restoration command. It walks drafts/ and
generate_guide.log and brings queue.csv into agreement with what's actually
on disk. Any draft file whose course ID is NOT yet in the queue is added
automatically -- no separate `add` step is needed before importing a ZIP.
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
QUEUE_FILE = os.path.join(SCRIPT_DIR, "queue.csv")
LOG_FILE = os.path.join(SCRIPT_DIR, "activity.log")
DRAFTS_DIR = os.path.join(SCRIPT_DIR, "drafts")
MASTER_CSV = os.path.join(SCRIPT_DIR, "courses_2plus_institutions.csv")
GEN_LOG = os.path.join(SCRIPT_DIR, "generate_guide.log")

QUEUE_FIELDS = [
    "course_id", "title", "num_inst",
    "status",                  # queued | drafted | pushed | skipped | error
    "priority",                # int; lower = higher priority. Default = 1000 - num_inst.
    "added_utc", "drafted_utc", "pushed_utc",
    "notes",
]

VALID_STATES = {"queued", "drafted", "pushed", "skipped", "error"}

# Course IDs look like ABC1234, ABC1234C (lab integrated), or ABC1234L (lab separate)
COURSE_ID_RE = re.compile(r"^[A-Z]{3}\d{4}[CL]?$")


# ---------------------------------------------------------------------------
# Time + log helpers
# ---------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def file_mtime_iso(path: str) -> str:
    """Return the file's mtime in the same ISO format used elsewhere."""
    mtime = os.path.getmtime(path)
    return datetime.fromtimestamp(mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(actor: str, message: str) -> None:
    """Append one line to activity.log. actor in {user, claude, push, queue}."""
    line = f"{now_iso()}  {actor:<8}  {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)


# ---------------------------------------------------------------------------
# Queue I/O
# ---------------------------------------------------------------------------

def load_queue() -> list[dict]:
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save_queue(rows: list[dict]) -> None:
    # Sort by priority (asc), then status (queued first), then course_id
    state_order = {"queued": 0, "drafted": 1, "pushed": 2, "error": 3, "skipped": 4}
    rows.sort(key=lambda r: (
        int(r.get("priority") or 1000),
        state_order.get(r.get("status", ""), 99),
        r["course_id"],
    ))
    with open(QUEUE_FILE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=QUEUE_FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            # Backfill any missing keys with empty strings for clean output
            row = {k: r.get(k, "") for k in QUEUE_FIELDS}
            w.writerow(row)


def queue_index(rows: list[dict]) -> dict[str, dict]:
    return {r["course_id"]: r for r in rows}


# ---------------------------------------------------------------------------
# Master CSV + draft JSON access
# ---------------------------------------------------------------------------

def load_master() -> list[dict]:
    """Load master CSV; hard-exit if missing (used by add command)."""
    if not os.path.exists(MASTER_CSV):
        sys.exit(f"Master CSV not found: {MASTER_CSV}\nRun extract_courses.py first.")
    with open(MASTER_CSV, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_master_indexed() -> dict[str, dict]:
    """Load master CSV as id-indexed dict; return empty dict if not available.

    Used by reconcile, which should not fail just because the master is
    missing -- orphan drafts can still be added with whatever metadata is
    available in the JSON.
    """
    if not os.path.exists(MASTER_CSV):
        return {}
    try:
        with open(MASTER_CSV, encoding="utf-8-sig", newline="") as f:
            return {r["course_id"]: r for r in csv.DictReader(f)}
    except Exception as exc:
        print(f"  WARNING: could not read master CSV ({exc}); proceeding without it.")
        return {}


def read_draft_safe(path: str) -> dict | None:
    """Read a draft JSON; return None and print a warning on any failure."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        print(f"  WARNING: {os.path.basename(path)} is not valid JSON ({exc}); skipping.")
        return None
    except Exception as exc:
        print(f"  WARNING: could not read {os.path.basename(path)} ({exc}); skipping.")
        return None

    if not isinstance(data, dict):
        print(f"  WARNING: {os.path.basename(path)} is not a JSON object; skipping.")
        return None
    if "title" not in data:
        print(f"  WARNING: {os.path.basename(path)} missing 'title' field; skipping.")
        return None
    return data


def matches_filter(
    row: dict, *,
    courses: set[str] | None,
    prefixes: list[str] | None,
    institutions: set[str] | None,
    min_inst: int | None,
    max_inst: int | None,
) -> bool:
    cid = row["course_id"]
    if courses is not None and cid not in courses:
        return False
    if prefixes and not any(cid.startswith(p) for p in prefixes):
        return False
    if institutions is not None:
        row_insts = {s.strip() for s in row["institutions"].split(";") if s.strip()}
        if institutions.isdisjoint(row_insts):
            return False
    n = int(row["num_inst"])
    if min_inst is not None and n < min_inst:
        return False
    if max_inst is not None and n > max_inst:
        return False
    return True


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_add(args) -> None:
    rows = load_queue()
    existing = queue_index(rows)
    master = load_master()
    master_idx = {r["course_id"]: r for r in master}

    courses = {c.upper() for c in args.course} if args.course else None
    prefixes = [p.upper() for p in args.prefix] if args.prefix else None
    institutions = {i.upper() for i in args.institution} if args.institution else None

    not_in_master: list[str] = []

    if args.top:
        # Top-N by num_inst, excluding anything already queued
        sorted_master = sorted(master, key=lambda r: -int(r["num_inst"]))
        candidates = [r for r in sorted_master if r["course_id"] not in existing][:args.top]
    elif courses:
        # Explicit ID list: check each against master and surface misses
        candidates = []
        for cid in sorted(courses):
            if cid in master_idx:
                candidates.append(master_idx[cid])
            else:
                not_in_master.append(cid)
    else:
        candidates = [
            r for r in master
            if matches_filter(r, courses=None, prefixes=prefixes,
                              institutions=institutions,
                              min_inst=args.min_inst, max_inst=args.max_inst)
        ]

    if not candidates and not not_in_master:
        print("No courses matched the criteria.")
        return

    added = 0
    skipped_existing = 0
    for c in candidates:
        cid = c["course_id"]
        if cid in existing:
            skipped_existing += 1
            continue
        rows.append({
            "course_id": cid,
            "title": c["title"],
            "num_inst": c["num_inst"],
            "status": "queued",
            # higher num_inst = lower priority number = sooner
            "priority": str(1000 - int(c["num_inst"])),
            "added_utc": now_iso(),
            "drafted_utc": "",
            "pushed_utc": "",
            "notes": args.note or "",
        })
        added += 1

    save_queue(rows)

    # Log + report
    criteria = []
    if courses: criteria.append(f"courses={','.join(sorted(courses))}")
    if prefixes: criteria.append(f"prefix={','.join(prefixes)}")
    if institutions: criteria.append(f"institution={','.join(sorted(institutions))}")
    if args.min_inst is not None: criteria.append(f"min_inst={args.min_inst}")
    if args.max_inst is not None: criteria.append(f"max_inst={args.max_inst}")
    if args.top: criteria.append(f"top={args.top}")
    crit_str = " ".join(criteria) if criteria else "(no criteria)"

    log("user", f"ADD {crit_str} -> +{added} queued ({skipped_existing} already in queue, "
                f"{len(not_in_master)} not in master)")
    print(f"Added {added} course(s) to queue.")
    if skipped_existing:
        print(f"Skipped {skipped_existing} course(s) already in queue.")
    if not_in_master:
        print(f"NOT ADDED -- not found in master CSV: {', '.join(not_in_master)}")
        print("  If the inventory is out of date, re-run extract_courses.py.")
        print("  If the course exists but isn't in the inventory, drop a")
        print("  matching draft into drafts/ and run 'reconcile' -- it will")
        print("  pick the orphan draft up automatically.")


def cmd_status(args) -> None:
    rows = load_queue()
    if not rows:
        print("Queue is empty. Use 'queue_mgr.py add' to populate.")
        return

    # Summary counts
    counts = {s: 0 for s in VALID_STATES}
    for r in rows:
        counts[r.get("status", "queued")] = counts.get(r.get("status", "queued"), 0) + 1

    print(f"Queue: {QUEUE_FILE}")
    print(f"Total: {len(rows)} course(s)")
    print()
    for state in ("queued", "drafted", "pushed", "error", "skipped"):
        if counts.get(state):
            print(f"  {state:<10} {counts[state]:>4}")
    print()

    # Filter for display
    if args.state:
        rows = [r for r in rows if r.get("status") == args.state]
        title = f"All '{args.state}' courses ({len(rows)}):"
        limit = None
    else:
        title = "Next 10 by priority (per state):"
        limit = 10

    if args.state:
        print(title)
        print(f"  {'COURSE_ID':<12} {'NUM':>4}  TITLE")
        for r in rows:
            print(f"  {r['course_id']:<12} {r.get('num_inst',''):>4}  {r.get('title','')[:60]}")
    else:
        for state in ("queued", "drafted"):
            state_rows = [r for r in rows if r.get("status") == state]
            if not state_rows:
                continue
            print(f"Next {min(limit, len(state_rows))} '{state}' (of {len(state_rows)}):")
            print(f"  {'COURSE_ID':<12} {'NUM':>4}  TITLE")
            for r in state_rows[:limit]:
                print(f"  {r['course_id']:<12} {r.get('num_inst',''):>4}  {r.get('title','')[:60]}")
            print()


def cmd_list(args) -> None:
    """Plain output -- course IDs only, one per line. Pipeable."""
    rows = load_queue()
    if args.state:
        rows = [r for r in rows if r.get("status") == args.state]
    for r in rows:
        print(r["course_id"])


def cmd_mark(args) -> None:
    if args.state not in VALID_STATES:
        sys.exit(f"Invalid state: {args.state}. Must be one of: {', '.join(sorted(VALID_STATES))}")

    rows = load_queue()
    idx = queue_index(rows)
    cid = args.course_id.upper()
    if cid not in idx:
        sys.exit(f"Course not in queue: {cid}")

    row = idx[cid]
    old_state = row.get("status", "")
    row["status"] = args.state
    if args.state == "drafted" and not row.get("drafted_utc"):
        row["drafted_utc"] = now_iso()
    if args.state == "pushed" and not row.get("pushed_utc"):
        row["pushed_utc"] = now_iso()
    if args.note:
        row["notes"] = args.note

    save_queue(rows)
    log("user", f"MARK {cid} {old_state}->{args.state}" + (f" note='{args.note}'" if args.note else ""))
    print(f"Marked {cid}: {old_state} -> {args.state}")


def cmd_remove(args) -> None:
    rows = load_queue()
    cid = args.course_id.upper()
    new_rows = [r for r in rows if r["course_id"] != cid]
    if len(new_rows) == len(rows):
        sys.exit(f"Course not in queue: {cid}")
    save_queue(new_rows)
    log("user", f"REMOVE {cid}")
    print(f"Removed {cid} from queue.")


def cmd_reconcile(args) -> None:
    """Sync queue.csv with what's actually in drafts/ and the push log.

    Walks drafts/ once, then walks generate_guide.log once. For each draft:
      - If not in the queue at all, ADD it as a new entry (orphan pickup).
        Status becomes 'pushed' if the JSON has a pushed_utc stamp,
        otherwise 'drafted'.
      - If in the queue as 'queued', upgrade to 'drafted'.
      - If the JSON has a pushed_utc stamp and the queue says otherwise,
        upgrade to 'pushed'.

    Then for each "PUSH: Success" line in generate_guide.log: if the queue
    entry exists but isn't yet 'pushed', upgrade it. (This is the legacy
    path for entries that pre-date the pushed_utc stamp feature.)

    Malformed or unreadable draft files are reported and skipped.
    """
    rows = load_queue()
    idx = queue_index(rows)
    master_idx = load_master_indexed()

    added_orphans: list[str] = []
    added_orphans_pushed: list[str] = []   # subset of added_orphans
    marked_drafted: list[str] = []
    marked_pushed_via_stamp: list[str] = []
    marked_pushed_via_log: list[str] = []
    skipped_invalid = 0
    skipped_bad_id = 0

    if os.path.isdir(DRAFTS_DIR):
        for fname in sorted(os.listdir(DRAFTS_DIR)):
            if not fname.endswith("_guide.json"):
                continue
            cid = fname[: -len("_guide.json")].upper()
            if not COURSE_ID_RE.match(cid):
                print(f"  WARNING: filename '{fname}' does not match course-ID pattern; skipping.")
                skipped_bad_id += 1
                continue

            path = os.path.join(DRAFTS_DIR, fname)
            data = read_draft_safe(path)
            if data is None:
                skipped_invalid += 1
                continue

            pushed_utc = data.get("pushed_utc") or ""

            if cid not in idx:
                # ORPHAN: build a queue entry from master CSV (if available)
                # plus whatever the draft JSON tells us.
                master_row = master_idx.get(cid, {})
                num_inst = master_row.get("num_inst", "")
                title = master_row.get("title") or data.get("title") or cid
                priority = (1000 - int(num_inst)) if num_inst else 1000
                drafted_utc = file_mtime_iso(path)
                new_row = {
                    "course_id": cid,
                    "title": title,
                    "num_inst": num_inst,
                    "status": "pushed" if pushed_utc else "drafted",
                    "priority": str(priority),
                    "added_utc": now_iso(),
                    "drafted_utc": drafted_utc,
                    "pushed_utc": pushed_utc,
                    "notes": "(added by reconcile from orphan draft)",
                }
                rows.append(new_row)
                idx[cid] = new_row
                added_orphans.append(cid)
                if pushed_utc:
                    added_orphans_pushed.append(cid)
                continue

            # Existing entry: maybe upgrade status
            row = idx[cid]
            current = row.get("status", "queued")

            if current == "queued":
                row["status"] = "drafted"
                if not row.get("drafted_utc"):
                    row["drafted_utc"] = file_mtime_iso(path)
                marked_drafted.append(cid)
                current = "drafted"

            if pushed_utc and current != "pushed":
                row["status"] = "pushed"
                row["pushed_utc"] = pushed_utc
                marked_pushed_via_stamp.append(cid)

    # generate_guide.log fallback for entries that pre-date pushed_utc stamps
    if os.path.exists(GEN_LOG):
        push_re = re.compile(r"\[([A-Z0-9]+)\] PUSH: Success")
        with open(GEN_LOG, encoding="utf-8") as f:
            for line in f:
                m = push_re.search(line)
                if not m:
                    continue
                cid = m.group(1)
                if cid not in idx:
                    continue
                if idx[cid].get("status") != "pushed":
                    idx[cid]["status"] = "pushed"
                    if not idx[cid].get("pushed_utc"):
                        idx[cid]["pushed_utc"] = now_iso()
                    marked_pushed_via_log.append(cid)

    save_queue(rows)

    total_changes = (
        len(added_orphans)
        + len(marked_drafted)
        + len(marked_pushed_via_stamp)
        + len(marked_pushed_via_log)
    )

    log("queue",
        f"RECONCILE -> +{len(added_orphans)} orphan(s) "
        f"({len(added_orphans_pushed)} already pushed), "
        f"{len(marked_drafted)} ->drafted, "
        f"{len(marked_pushed_via_stamp)} ->pushed via stamp, "
        f"{len(marked_pushed_via_log)} ->pushed via log, "
        f"{skipped_invalid} invalid, {skipped_bad_id} bad ID")

    if total_changes == 0 and skipped_invalid == 0 and skipped_bad_id == 0:
        print("Reconciled. No changes -- queue already matches the filesystem.")
        return

    print(f"Reconciled. {total_changes} change(s):")
    if added_orphans:
        n_pushed = len(added_orphans_pushed)
        suffix = f" ({n_pushed} already had pushed_utc stamp)" if n_pushed else ""
        print(f"  +{len(added_orphans)} orphan draft(s) added to queue{suffix}")
        _print_id_sample(added_orphans)
    if marked_drafted:
        print(f"  {len(marked_drafted)} marked drafted (matching file in drafts/)")
        _print_id_sample(marked_drafted)
    if marked_pushed_via_stamp:
        print(f"  {len(marked_pushed_via_stamp)} marked pushed (via pushed_utc stamp)")
        _print_id_sample(marked_pushed_via_stamp)
    if marked_pushed_via_log:
        print(f"  {len(marked_pushed_via_log)} marked pushed (via generate_guide.log)")
        _print_id_sample(marked_pushed_via_log)
    if skipped_invalid:
        print(f"  {skipped_invalid} draft file(s) skipped (invalid JSON or missing 'title')")
    if skipped_bad_id:
        print(f"  {skipped_bad_id} file(s) skipped (filename did not match course-ID pattern)")


def _print_id_sample(ids: list[str], cap: int = 10) -> None:
    """Print the IDs inline for small lists, summarize for large ones."""
    if len(ids) <= cap:
        print(f"      {', '.join(ids)}")
    else:
        head = ", ".join(ids[:cap])
        print(f"      {head}, ... ({len(ids) - cap} more)")


def cmd_next_batch(args) -> None:
    """Print course IDs ready to draft, in priority order."""
    rows = load_queue()
    queued = [r for r in rows if r.get("status") == "queued"]
    queued.sort(key=lambda r: int(r.get("priority") or 1000))
    for r in queued[:args.n]:
        print(r["course_id"])


def cmd_ready_to_push(args) -> None:
    """Print course IDs ready to push (drafted but not pushed)."""
    rows = load_queue()
    for r in rows:
        if r.get("status") == "drafted":
            print(r["course_id"])


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Manage the curriculum-guide generation queue.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="cmd", required=True, metavar="COMMAND")

    p_add = sub.add_parser("add", help="Add courses to the queue")
    p_add.add_argument("--course", nargs="+", metavar="ID")
    p_add.add_argument("--prefix", nargs="+", metavar="ABC")
    p_add.add_argument("--institution", nargs="+", metavar="CODE")
    p_add.add_argument("--min-inst", type=int, metavar="N")
    p_add.add_argument("--max-inst", type=int, metavar="N")
    p_add.add_argument("--top", type=int, metavar="N",
                       help="Add the top-N priority courses not already queued")
    p_add.add_argument("--note", metavar="TEXT", help="Optional note attached to added rows")
    p_add.set_defaults(func=cmd_add)

    p_status = sub.add_parser("status", help="Show queue summary")
    p_status.add_argument("--state", choices=sorted(VALID_STATES))
    p_status.set_defaults(func=cmd_status)

    p_list = sub.add_parser("list", help="Print course IDs (pipeable)")
    p_list.add_argument("--state", choices=sorted(VALID_STATES))
    p_list.set_defaults(func=cmd_list)

    p_mark = sub.add_parser("mark", help="Set the status of one course")
    p_mark.add_argument("course_id")
    p_mark.add_argument("--state", required=True, choices=sorted(VALID_STATES))
    p_mark.add_argument("--note", metavar="TEXT")
    p_mark.set_defaults(func=cmd_mark)

    p_rm = sub.add_parser("remove", help="Remove a course from the queue")
    p_rm.add_argument("course_id")
    p_rm.set_defaults(func=cmd_remove)

    p_rec = sub.add_parser("reconcile",
                           help="Sync queue with drafts/ folder and generate_guide.log; "
                                "auto-adds orphan drafts as new queue entries.")
    p_rec.set_defaults(func=cmd_reconcile)

    p_next = sub.add_parser("next-batch",
                            help="Print next N course IDs to draft (default 5)")
    p_next.add_argument("--n", type=int, default=5)
    p_next.set_defaults(func=cmd_next_batch)

    p_push = sub.add_parser("ready-to-push",
                            help="Print all course IDs ready to push (drafted state)")
    p_push.set_defaults(func=cmd_ready_to_push)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # Triggered when stdout is piped to head/etc. and the reader closes early.
        # Standard idiom: redirect stderr to /dev/null to silence the secondary error.
        try:
            sys.stdout.close()
        except Exception:
            pass
        try:
            sys.stderr.close()
        except Exception:
            pass
