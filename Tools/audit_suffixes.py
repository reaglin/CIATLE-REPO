import csv, re
dsc = {}
with open('daytona_courses.csv', encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        dsc[r['course_id'].strip().upper()] = r['title'].strip()

rows = []
with open('queue.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

def variants(cid):
    if cid.endswith('C') or cid.endswith('L'):
        return cid[:-1]
    return None

mismatch = []
for r in rows:
    cid = r['course_id'].strip().upper()
    if cid in dsc:
        continue
    base = variants(cid)
    cands = []
    if base and base in dsc:
        cands.append(base)
    for suf in ('C','L'):
        if cid+suf in dsc:
            cands.append(cid+suf)
    if base:
        for suf in ('C','L'):
            if base+suf in dsc and base+suf != cid:
                cands.append(base+suf)
    if cands:
        mismatch.append((cid, r['status'], r['title'], cands[0], dsc[cands[0]]))

print(f"Queue rows: {len(rows)}   DSC courses: {len(dsc)}")
print(f"Queue ids absent from DSC but present under a different C/L suffix: {len(mismatch)}\n")
from collections import Counter
print(Counter(m[1] for m in mismatch))
print()
for cid, st, qt, d, dt in sorted(mismatch, key=lambda x: (x[1], x[0])):
    print(f"{cid:<10} [{st:<7}] queue={qt[:42]:<42} -> DSC {d:<10} {dt[:46]}")
