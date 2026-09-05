# -*- coding: utf-8 -*-
"""
Apply the prefix-name changes Ron approved in TAXONOMY_SCNS_PROPOSAL.md to taxonomy.json.

Parses the two approved tables out of the proposal document itself (rather than re-deriving
from scns_prefix_map.json) so that exactly the rows Ron reviewed are applied -- the proposal
already excludes the two PDF-extraction artifacts (ART, LAW) and the three prefixes absent
from the handbook (FOR, THE, FIT).

Dry run by default; pass --apply to write.
"""
import json, re, shutil, sys, io

ROOT = r"C:\Users\ronal\source\repos\CIATLE-REPO"
PROPOSAL = ROOT + r"\Tools\TAXONOMY_SCNS_PROPOSAL.md"
TAXONOMY = ROOT + r"\PreseMakerRepo.Api\Data\Seed\taxonomy.json"
BAK = TAXONOMY + ".bak4"

ROW = re.compile(r"^\|\s*`([A-Z]{3})`\s*\|(.+?)\|(.+?)\|")

def clean(cell):
    s = cell.strip()
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)   # bold
    s = re.sub(r"\*(.+?)\*", r"\1", s)       # italic
    s = s.replace("`", "").strip()
    return s

def parse():
    section = None
    out = {}          # prefix -> (current, proposed, section)
    for line in io.open(PROPOSAL, encoding="utf-8"):
        if line.startswith("## Substantive"):
            section = "substantive"; continue
        if line.startswith("## Cosmetic"):
            section = "cosmetic"; continue
        if line.startswith("## Extraction") or line.startswith("## Not found"):
            section = None; continue
        if section is None:
            continue
        m = ROW.match(line)
        if not m:
            continue
        pfx, cur, prop = m.group(1), clean(m.group(2)), clean(m.group(3))
        if not prop or prop == cur:
            continue
        out[pfx] = (cur, prop, section)
    return out

def main(apply=False):
    changes = parse()
    subs = sum(1 for v in changes.values() if v[2] == "substantive")
    cos = sum(1 for v in changes.values() if v[2] == "cosmetic")
    print(f"Parsed from proposal: {len(changes)} prefixes ({subs} substantive, {cos} cosmetic)")

    tax = json.load(open(TAXONOMY, encoding="utf-8"))
    applied, drifted, missing = [], [], []
    seen = set()
    for d in tax["tree"]:
        for c in d.get("children", []):
            rec = changes.get(c["key"])
            if not rec:
                continue
            seen.add(c["key"])
            cur, prop, sect = rec
            if c["name"] == prop:
                continue
            if c["name"] != cur:
                # taxonomy.json moved since the proposal was generated (e.g. this session's
                # PGY / ROT corrections). Record it and still apply the approved name.
                drifted.append((c["key"], cur, c["name"], prop))
            applied.append((c["key"], c["name"], prop, sect, d["name"]))
            c["name"] = prop

    missing = sorted(set(changes) - seen)

    print(f"\nNames changed: {len(applied)}")
    for k, a, b, sect, disc in sorted(applied)[:20]:
        print(f"    {k:<5} [{sect[:4]}] {a[:40]:<41} -> {b[:44]:<45} ({disc[:26]})")
    if len(applied) > 20:
        print(f"    ... and {len(applied)-20} more")

    if drifted:
        print(f"\n!! {len(drifted)} row(s) where taxonomy.json no longer matched the proposal's "
              f"'Current' column (applied the approved name anyway):")
        for k, propcur, actual, newname in drifted:
            print(f"    {k:<5} proposal said current={propcur!r}, file had {actual!r} -> {newname!r}")

    if missing:
        print(f"\nProposal prefixes not present in taxonomy.json ({len(missing)}): {', '.join(missing)}")

    if apply:
        shutil.copy2(TAXONOMY, BAK)
        with open(TAXONOMY, "w", encoding="utf-8") as f:
            json.dump(tax, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"\nWROTE {TAXONOMY}\nbackup -> {BAK}")
    else:
        print("\n(dry run -- pass --apply to write)")
    return 0

if __name__ == "__main__":
    sys.exit(main(apply="--apply" in sys.argv))
