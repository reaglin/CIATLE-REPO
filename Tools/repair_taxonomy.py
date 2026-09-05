# -*- coding: utf-8 -*-
"""
Taxonomy hierarchy repair.

Applies only the UNAMBIGUOUS fixes:
  1. Two colliding discipline keys (20-char truncation collision) -> distinct keys.
  2. Prefixes parented under a semantically unrelated discipline -> correct discipline.
     Every move below is corroborated by the official SCNS handbook map.
  3. PGY: name AND parent both wrong (it is Photography, not Plant Pathology) -- corroborated
     by the eight PGY photography guides already published in this repository.

Deliberately NOT applied (left for Ron's review):
  - The 295 cosmetic + 93 substantive NAME changes in TAXONOMY_SCNS_PROPOSAL.md.
  - ~110 foreign-language prefixes the handbook flattens into "Foreign Language Education";
    the current finer-grained grouping is better and is kept.
  - Cases where the current tree is more specific than the handbook (Education: Exceptional
    Child, Education: Counseling Services, Mechanics: Auto/Bod/..., Engineering: General/Support).
"""
import json, shutil, sys, collections

PATH = r"C:\Users\ronal\source\repos\CIATLE-REPO\PreseMakerRepo.Api\Data\Seed\taxonomy.json"
BAK = PATH + ".bak3"

# --- discipline key collisions: (old_key, discipline_name) -> new_key --------------
KEY_FIXES = {
    ("FOREIGN_LANGUAGE__AM", "Foreign Language: American Sign Language And Interpreting"):
        "FOREIGN_LANGUAGE__ASL",
    ("FOREIGN_LANGUAGE__CA", "Foreign Language: Catalan Language And Literature"):
        "FOREIGN_LANGUAGE__CATALAN",
}

# --- prefix -> destination discipline NAME ----------------------------------------
REPARENT = {
    # E-prefixes swept under the alphabetically preceding heading (same bug class as
    # the CJJ/CJK/CJL-under-DENTISTRY defect already noted in TaxonomySeed.cs).
    "ECP": "Economics",
    "ECS": "Economics",
    "EDS": "Education: Administration And Supervision",
    "EGI": "Education: Exceptional Child",
    "EHD": "Education: Exceptional Child",
    "ELD": "Education: Exceptional Child",
    "EMR": "Education: Exceptional Child",
    "EPD": "Education: Exceptional Child",
    "EPH": "Education: Exceptional Child",
    "EVI": "Education: Exceptional Child",
    "EML": "Mechanical Engineering",
    "EGS": "Engineering: General/Support",
    "EMA": "Computer Math/Materials Engineering",
    # engine repair prefixes stranded under Economics
    "MTE": "Mechanics: Auto/Bod/Diesel/Marine/Sm.Eng.",
    "SER": "Mechanics: Auto/Bod/Diesel/Marine/Sm.Eng.",
    # geography prefixes stranded under Mechanics
    "GEO": "Geography",
    "GIS": "Geography",
    # medical records prefixes stranded under Geography
    "MRE": "Health Information Management",
    "MTS": "Health Information Management",
    # interdisciplinary prefixes stranded under Family And Consumer Sciences
    "GLS": "Interdisciplinary Studies And Honors",
    "IDH": "Interdisciplinary Studies And Honors",
    "IDS": "Interdisciplinary Studies And Honors",
    "SLA": "English As A Second Language/Teaching Esl",
    # misc single strays
    "CMC": "Mass Communication",
    "SON": "Medical Imaging And Radiation Therapy",
    "ROT": "Medical Imaging And Radiation Therapy",
    "FFP": "Fire Science",
    "HSC": "Health Sciences/Resources",
    "DEC": "Business Education",
    # applied-music prefixes stranded under Speech Pathology
    "MVH": "Music - Applied",
    "MVJ": "Music - Applied",
    "MVK": "Music - Applied",
    "MVO": "Music - Applied",
    # PGY is Photography, not Plant Pathology -- needs a new discipline node
    "PGY": "Photography",
}

# --- prefix name corrections (factually wrong, not stylistic) ----------------------
RENAME = {
    "PGY": "Photography",
    "ROT": "Reactor Operator Technology",
}

NEW_DISCIPLINES = [
    {"key": "PHOTOGRAPHY", "name": "Photography"},
]

def main(apply=False):
    tax = json.load(open(PATH, encoding="utf-8"))
    tree = tax["tree"]

    # 1. key collisions
    key_changes = []
    for node in tree:
        newk = KEY_FIXES.get((node["key"], node["name"]))
        if newk:
            key_changes.append((node["key"], newk, node["name"], len(node.get("children", []))))
            node["key"] = newk

    # 2. add any missing destination discipline nodes
    by_name = {}
    for n in tree:
        by_name.setdefault(n["name"], n)
    added = []
    for nd in NEW_DISCIPLINES:
        if nd["name"] not in by_name:
            node = {"key": nd["key"], "name": nd["name"], "children": []}
            tree.append(node)
            by_name[nd["name"]] = node
            added.append(nd["name"])

    missing_targets = sorted({d for d in REPARENT.values() if d not in by_name})
    if missing_targets:
        print("ERROR: destination discipline(s) not found:", missing_targets)
        return 1

    # 3. re-parent
    moves, notfound = [], []
    for pfx, dest_name in REPARENT.items():
        src = None
        child = None
        for n in tree:
            for c in n.get("children", []):
                if c["key"] == pfx:
                    src, child = n, c
                    break
            if src:
                break
        if child is None:
            notfound.append(pfx)
            continue
        if src["name"] == dest_name:
            continue
        src["children"].remove(child)
        by_name[dest_name].setdefault("children", []).append(child)
        moves.append((pfx, child["name"], src["name"], dest_name))

    # 4. renames
    renames = []
    for n in tree:
        for c in n.get("children", []):
            if c["key"] in RENAME and c["name"] != RENAME[c["key"]]:
                renames.append((c["key"], c["name"], RENAME[c["key"]]))
                c["name"] = RENAME[c["key"]]

    # 5. keep each discipline's children alphabetical by key
    for n in tree:
        if n.get("children"):
            n["children"].sort(key=lambda c: c["key"])

    # --- report ---
    print(f"Discipline key collisions resolved: {len(key_changes)}")
    for old, new, name, nch in key_changes:
        print(f"    {old}  ->  {new}    ({name}, {nch} prefixes)")
    print(f"\nNew discipline nodes added: {added or 'none'}")
    print(f"\nPrefixes re-parented: {len(moves)}")
    for pfx, pn, a, b in sorted(moves):
        print(f"    {pfx:<5} {pn[:40]:<41} {a[:36]:<37} ->  {b}")
    print(f"\nPrefix names corrected: {len(renames)}")
    for k, a, b in renames:
        print(f"    {k:<5} {a!r} -> {b!r}")
    if notfound:
        print(f"\n!! prefixes not found in tree: {notfound}")

    # --- integrity checks ---
    kc = collections.Counter(n["key"] for n in tree)
    dup_disc = {k: v for k, v in kc.items() if v > 1}
    pc = collections.Counter(c["key"] for n in tree for c in n.get("children", []))
    dup_pfx = {k: v for k, v in pc.items() if v > 1}
    total = sum(len(n.get("children", [])) for n in tree)
    print(f"\nIntegrity: {len(tree)} disciplines, {total} prefixes")
    print(f"  duplicate discipline keys: {dup_disc or 'none'}")
    print(f"  duplicate prefix keys:     {dup_pfx or 'none'}")
    if dup_disc or dup_pfx:
        print("ABORT: duplicates remain")
        return 1

    if apply:
        shutil.copy2(PATH, BAK)
        with open(PATH, "w", encoding="utf-8") as f:
            json.dump(tax, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"\nWROTE {PATH}\nbackup -> {BAK}")
    else:
        print("\n(dry run -- pass --apply to write)")
    return 0

if __name__ == "__main__":
    sys.exit(main(apply="--apply" in sys.argv))
