# -*- coding: utf-8 -*-
"""Audit taxonomy.json prefix parentage + names against the official SCNS handbook map."""
import json, re, sys, collections

ROOT = r"C:\Users\ronal\source\repos\CIATLE-REPO"
tax = json.load(open(ROOT + r"\PreseMakerRepo.Api\Data\Seed\taxonomy.json", encoding="utf-8"))
scns = json.load(open(ROOT + r"\Tools\scns_prefix_map.json", encoding="utf-8"))

def norm(s):
    s = s.upper()
    s = re.sub(r"\(EFF[^)]*\)?", " ", s)
    s = re.sub(r"[^A-Z0-9]+", " ", s)
    return " ".join(s.split())

# --- duplicate discipline keys -------------------------------------------------
keycount = collections.Counter(n["key"] for n in tax["tree"])
dupes = {k: v for k, v in keycount.items() if v > 1}

# --- build current parentage ---------------------------------------------------
cur_parent = {}          # prefix -> (disc_key, disc_name)
cur_name = {}            # prefix -> name
prefix_dupes = collections.Counter()
for d in tax["tree"]:
    for c in d.get("children", []):
        prefix_dupes[c["key"]] += 1
        cur_parent[c["key"]] = (d["key"], d["name"])
        cur_name[c["key"]] = c["name"]

# --- map normalized SCNS discipline -> taxonomy discipline node -----------------
disc_by_norm = {}
for d in tax["tree"]:
    disc_by_norm.setdefault(norm(d["name"]), d)

misparented, unmapped, missing_scns = [], [], []
for pfx, (dk, dn) in sorted(cur_parent.items()):
    rec = scns.get(pfx)
    if not rec:
        missing_scns.append(pfx)
        continue
    want = norm(rec["discipline"])
    if want == norm(dn):
        continue
    target = disc_by_norm.get(want)
    if target is None:
        unmapped.append((pfx, cur_name[pfx], dn, rec["discipline"]))
    else:
        misparented.append((pfx, cur_name[pfx], dn, target["name"], rec["title"]))

print("=" * 100)
print("DUPLICATE DISCIPLINE KEYS (collision from 20-char key truncation)")
print("=" * 100)
for k, v in dupes.items():
    names = [n["name"] for n in tax["tree"] if n["key"] == k]
    print(f"  {k}  x{v}   {names}")
if not dupes:
    print("  none")

print()
print("=" * 100)
print(f"MIS-PARENTED PREFIXES: {len(misparented)}  (SCNS discipline exists in the tree but prefix sits elsewhere)")
print("=" * 100)
print(f"{'PFX':<5} {'CURRENT DISCIPLINE':<44} {'SHOULD BE (SCNS)':<44} PREFIX NAME")
for pfx, pn, cd, td, title in misparented:
    print(f"{pfx:<5} {cd[:43]:<44} {td[:43]:<44} {pn}")

print()
print("=" * 100)
print(f"SCNS DISCIPLINE NOT PRESENT AS A NODE: {len(unmapped)}")
print("=" * 100)
byd = collections.defaultdict(list)
for pfx, pn, cd, sd in unmapped:
    byd[sd].append((pfx, pn, cd))
for sd in sorted(byd):
    print(f"\n  SCNS discipline: {sd}")
    for pfx, pn, cd in byd[sd]:
        print(f"      {pfx:<5} {pn[:44]:<45} currently under: {cd}")

print()
print(f"Prefixes in taxonomy with no SCNS handbook entry: {len(missing_scns)}")
print("  " + ", ".join(missing_scns))
pd = {k: v for k, v in prefix_dupes.items() if v > 1}
print(f"\nPrefixes appearing under more than one discipline: {pd if pd else 'none'}")
print(f"\nTotals: {len(cur_parent)} prefixes in tree, {len(scns)} in SCNS handbook map")
