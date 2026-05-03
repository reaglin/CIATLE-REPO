#!/usr/bin/env python3
"""
Extract Florida SCNS courses offered at 2+ institutions from the statewide inventory.

Rules:
- Course IDs match ABC1234, ABC1234C, or ABC1234L (3 letters + 4 digits, optional C or L suffix).
- ABC1234 and ABC1234C are the SAME course (combined-lecture-and-lab variant of the same SCNS code).
  They are merged into a single record. The output label uses the C-form if ANY institution offers it,
  otherwise the bare form.
- ABC1234L (standalone lab) is treated as a SEPARATE course.
- Output: only courses offered by 2 or more distinct institutions.
"""
import csv
import re
from collections import defaultdict, Counter

SRC = "/mnt/project/All_StatewideInventory_clean1.csv"
DST = "/home/claude/courses_2plus_institutions.csv"

course_pat = re.compile(r"^([A-Z]{3})(\d{4})([CL]?)$")

# key = (prefix, number, kind) where kind in {"course", "lab"}
# value = {"institutions": set, "has_c_form": bool, "titles": set}
groups = defaultdict(lambda: {"institutions": set(), "has_c_form": False, "titles": Counter()})

skipped_no_inst = 0
skipped_bad_id = 0
matched = 0

with open(SRC, encoding="iso-8859-1", newline="") as f:
    for row in csv.reader(f):
        if len(row) < 4:
            continue
        inst = row[0].strip()
        cid_raw = row[2].strip()
        title = row[3].strip()

        if not inst:
            skipped_no_inst += 1
            continue

        cid = cid_raw.replace(" ", "").upper()
        m = course_pat.match(cid)
        if not m:
            skipped_bad_id += 1
            continue

        prefix, number, suffix = m.group(1), m.group(2), m.group(3)
        kind = "lab" if suffix == "L" else "course"
        key = (prefix, number, kind)

        g = groups[key]
        g["institutions"].add(inst)
        if suffix == "C":
            g["has_c_form"] = True
        if title:
            g["titles"][title] += 1
        matched += 1

# Build output rows
out_rows = []
for (prefix, number, kind), g in groups.items():
    n_inst = len(g["institutions"])
    if n_inst < 2:
        continue
    if kind == "lab":
        course_id = f"{prefix}{number}L"
    else:
        course_id = f"{prefix}{number}C" if g["has_c_form"] else f"{prefix}{number}"

    # Pick the most common title across institutions; tiebreak with shorter length (more canonical)
    if g["titles"]:
        max_count = max(g["titles"].values())
        candidates = [t for t, c in g["titles"].items() if c == max_count]
        primary_title = min(candidates, key=lambda t: (len(t), t))
    else:
        primary_title = ""

    # Replace commas with " - " for safer parsing in tools that split on commas
    # (Excel, awk, etc.) without losing semantic meaning. Python's csv module
    # would handle quoted commas correctly, but downstream tooling often doesn't.
    # Use regex to collapse 'comma + any surrounding whitespace' into a single ' - '.
    primary_title = re.sub(r"\s*,\s*", " - ", primary_title)

    out_rows.append({
        "course_id": course_id,
        "title": primary_title,
        "num_inst": n_inst,
        "institutions": ";".join(sorted(g["institutions"])),
        "_kind": kind,  # internal only — used for sort order, not written to CSV
    })

# Sort: courses first then labs, then by course_id
out_rows.sort(key=lambda r: (r["_kind"], r["course_id"]))

with open(DST, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(
        f,
        fieldnames=["course_id", "title", "num_inst", "institutions"],
        extrasaction="ignore",  # silently drops _kind
    )
    w.writeheader()
    w.writerows(out_rows)

# Summary
n_courses = sum(1 for r in out_rows if r["_kind"] == "course")
n_labs = sum(1 for r in out_rows if r["_kind"] == "lab")
print(f"Source rows scanned          : {matched + skipped_no_inst + skipped_bad_id:,}")
print(f"  Skipped (no institution)   : {skipped_no_inst:,}  (taxonomy/master rows)")
print(f"  Skipped (id didn't match)  : {skipped_bad_id:,}  (admin codes etc.)")
print(f"  Matched institution rows   : {matched:,}")
print(f"Distinct course groups       : {len(groups):,}")
print(f"  ... offered at 2+ schools  : {len(out_rows):,}")
print(f"      Courses (incl. C form) : {n_courses:,}")
print(f"      Standalone labs (L)    : {n_labs:,}")
print(f"\nWrote {DST}")
