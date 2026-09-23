#!/usr/bin/env python
"""Build the CIP -> occupation seed for request-driven career paths.

Ron, 2026-09-23: "The paths will be listed under the CIP code section with a 'Request'
button. The queue of request will be available for view." Each CIP area page therefore needs
the occupations a reader could ask a path to be written for. This builds that list.

SOURCE
  CIP2020_SOC2018_Crosswalk.xlsx -- the NCES CIP 2020 / SOC 2018 crosswalk,
      https://nces.ed.gov/ipeds/cipcode/Files/CIP2020_SOC2018_Crosswalk.xlsx
      (sheet "CIP-SOC"). Titles are the federal file's own words.

WHAT IT DOES
  * rolls 6-digit programmes up to the 4-DIGIT groups the browse tree shows, keeping one
    row per (group, SOC);
  * keeps only groups in the seeded tree (Data/Seed/cip.json), because an occupation hangs
    off a node that must exist;
  * drops "99-9999 NO MATCH" rows;
  * ⚠ drops the 25-1xxx "... Teachers, Postsecondary" family. The crosswalk maps almost every
    programme to its own postsecondary-teacher SOC, so leaving them in would put a
    "Business Teachers, Postsecondary" row under business, "Nursing Instructors" under
    nursing, and so on across all 183 groups -- 207 rows of noise on a page meant for
    students choosing a career. It is a rule, not an edit, and it is recorded here.

Anything else that reads oddly on a page is hidden by an admin (CipOccupation.IsHidden),
which the seed never overwrites.

    python build_cip_soc_seed.py            # writes PreseMakerRepo.Api/Data/Seed/cip_soc.json
    python build_cip_soc_seed.py --report   # counts only
"""
import io
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'scratchpad', 'CIP2020_SOC2018_Crosswalk.xlsx')
CIP_SEED = os.path.join(HERE, '..', 'PreseMakerRepo.Api', 'Data', 'Seed', 'cip.json')
OUT = os.path.join(HERE, '..', 'PreseMakerRepo.Api', 'Data', 'Seed', 'cip_soc.json')

# SOC families excluded by rule, with the reason on the record.
EXCLUDE_SOC_PREFIXES = {
    '25-1': 'postsecondary teachers -- mapped to nearly every programme; noise on a student page',
}


def build():
    try:
        import openpyxl
    except ImportError:
        sys.exit('pip install openpyxl')
    if not os.path.exists(XLSX):
        sys.exit('missing %s -- download it from NCES (URL in the docstring)' % XLSX)

    groups = {n['code'] for n in json.load(io.open(CIP_SEED, encoding='utf-8'))['nodes']
              if len(n['code']) == 5}

    wb = openpyxl.load_workbook(XLSX, read_only=True)
    rows = list(wb['CIP-SOC'].iter_rows(values_only=True))[1:]

    pairs = defaultdict(dict)
    dropped = defaultdict(int)
    for cip, _ct, soc, soc_title in rows:
        cip, soc = (cip or '').strip(), (soc or '').strip()
        if not cip or not soc or soc == '99-9999':
            continue
        g = cip[:5]
        if g not in groups:
            dropped['group not in seeded tree'] += 1
            continue
        rule = next((p for p in EXCLUDE_SOC_PREFIXES if soc.startswith(p)), None)
        if rule:
            dropped['excluded family ' + rule] += 1
            continue
        pairs[g][soc] = (soc_title or '').strip()

    occ = [{'cipCode': g, 'socCode': s, 'socTitle': t}
           for g in sorted(pairs) for s, t in sorted(pairs[g].items())]
    return occ, groups, dropped


def main():
    occ, groups, dropped = build()
    covered = {o['cipCode'] for o in occ}
    print('seeded 4-digit groups : %d' % len(groups))
    print('groups with occupations: %d' % len(covered))
    print('occupation rows       : %d  (%d distinct SOC codes)'
          % (len(occ), len({o['socCode'] for o in occ})))
    for k, n in sorted(dropped.items()):
        print('dropped %-40s %d' % (k, n))
    if '--report' in sys.argv:
        return
    doc = {
        'source': 'NCES CIP 2020 / SOC 2018 crosswalk, sheet CIP-SOC',
        'note': 'Rolled up to 4-digit CIP groups in the seeded tree; 25-1xxx postsecondary '
                'teachers excluded by rule (Tools/build_cip_soc_seed.py).',
        'occupations': occ,
    }
    with io.open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    print('\nwrote %s' % os.path.normpath(OUT))


if __name__ == '__main__':
    main()
