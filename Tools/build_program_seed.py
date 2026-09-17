#!/usr/bin/env python
"""Build the Programs seed and the IPEDS award cross-reference.

Ron's definition (2026-09-17): a PROGRAM is "a major that supports a career path
and is being offered by a Florida school", and it sits ONE LEVEL ABOVE a degree:

    Nursing AS   (major) -> Nursing (program)
    Nursing BSN  (major) -> Nursing (program)
    Mechanical Engineering (major) = Mechanical Engineering (program)

And the inclusion rule, which is what forces the shape:

    "If a school has an LPN degree, they have a nursing program... I do not want
     a school to be excluded from being listed because their offerings are
     limited."

⚠⚠⚠ THAT IS WHY A PROGRAM SPANS SEVERAL CIP CODES. LPN is CIP 51.39 and RN is
51.38. Measured against IPEDS: Nursing defined as 51.38 alone finds 39 Florida
public institutions and MISSES 39 more -- and every single one of those 39 is a
TECHNICAL COLLEGE, which is exactly the population the rule protects. Both
series together find 78.

Ron, same day, on the other two questions:
  * a program is its own entity (not a CIP node) -- hence the student-facing
    name, "Nursing" rather than the federal "Registered Nursing, Nursing
    Administration, Nursing Research and Clinical Nursing";
  * programs sit ALONGSIDE CIP codes, and MANY CIP CODES ARE SUPPORTED BY
    MULTIPLE PROGRAMS -- so the mapping is many-to-many in both directions and
    no CIP code is owned by one programme;
  * completion counts are "handy, but not required" -- carried, but never used
    to rank schools.

⚠ Programs own NO school list. "I am going to decouple programs from schools."
Which schools offer a programme is DERIVED at read time by matching the
programme's CIP prefixes against the award table.

    python build_program_seed.py             # write both seed files
    python build_program_seed.py --report    # show what it would emit
"""
import io
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
IPEDS = os.path.join(HERE, 'scratchpad', 'ipeds_fl.json')
SEED = os.path.join(HERE, '..', 'PreseMakerRepo.Api', 'Data', 'Seed')
IPEDS_YEAR = 2023

# ── The curated programmes ──────────────────────────────────────────────────
# ⚠ cips are PREFIXES. "51.38" covers every 6-digit code beneath it, so a
# programme never has to enumerate the federal taxonomy.
PROGRAMS = [
    {
        'slug': 'nursing',
        'name': 'Nursing',
        'sortOrder': 10,
        'description': 'Nursing programmes prepare people to care for patients across every '
                       'setting Florida has, from a practical-nursing certificate at a technical '
                       'college through an associate degree leading to RN licensure to a '
                       'baccalaureate and beyond. One programme, several entry points.',
        'degreesNote': 'Nursing encompasses several degrees, and the level you enter at is the '
                       'real decision. A PRACTICAL NURSING certificate leads to LPN licensure and '
                       'is the fastest route into paid clinical work. An ASSOCIATE degree leads to '
                       'RN licensure through NCLEX-RN. A BACCALAUREATE (BSN) leads to the same '
                       'licence by a longer route, and is what many hospitals prefer and what '
                       'graduate study requires. ⚠ An RN-to-BSN programme is for nurses who are '
                       'ALREADY licensed and does not lead to initial licensure. Many Florida '
                       'institutions offer more than one of these.',
        'cips': [
            ('51.38', 'Registered nursing, nursing administration, research and clinical nursing '
                      '— the A.S. and BSN routes to RN licensure.'),
            ('51.39', 'Practical and vocational nursing, and nursing assistants — the LPN and CNA '
                      'routes. ⚠ Included deliberately: a school with only an LPN programme has a '
                      'nursing programme.'),
        ],
    },
    {
        'slug': 'engineering-technology',
        'name': 'Engineering Technology',
        'sortOrder': 20,
        'description': 'Engineering technology programmes prepare technicians and technologists '
                       'who build, install, test and maintain what engineers design — electronics, '
                       'mechanical systems, industrial automation, quality, drafting and civil '
                       'works. It is the largest applied-technical family in the Florida College '
                       'System.',
        'degreesNote': 'Engineering Technology is mostly an ASSOCIATE-level family in Florida, '
                       'with a smaller number of BACHELOR degrees and a large number of short '
                       'certificates that stack toward them. ⚠⚠ It is NOT the same as an '
                       'ENGINEERING degree, and the difference is worth two years: under '
                       's. 471.013(1)(a), Florida Statutes, a graduate of an approved engineering '
                       'curriculum needs four years of experience before the PE examination, while '
                       'a graduate of an approved engineering technology curriculum needs six. If a '
                       'PE licence is your goal, read the Mechanical Engineer career path first.',
        'cips': [('15.', 'The whole Engineering Technologies series — 32 CIP codes are awarded in '
                         'Florida, from sub-year certificates to master’s degrees.')],
    },
    {
        'slug': 'mechanical-engineering',
        'name': 'Mechanical Engineering',
        'sortOrder': 30,
        'description': 'Mechanical engineering programmes teach the analysis of forces, motion, '
                       'energy and materials, and the design of the machines and systems that use '
                       'them. It is the broadest engineering discipline and the one that closes '
                       'the fewest doors.',
        'degreesNote': 'Here the programme and the major are the same thing: a Bachelor of Science '
                       'in Mechanical Engineering, with master’s and doctoral degrees above it. '
                       '⚠ For Professional Engineer licensure the degree must come from a '
                       'programme accredited by ABET’s ENGINEERING commission — check before '
                       'enrolling, because an engineering TECHNOLOGY accreditation adds two years '
                       'to the experience requirement.',
        'cips': [('14.19', 'Mechanical Engineering — the degree itself.'),
                 ('14.01', 'General engineering, where several Florida institutions place a first '
                           'year common to all engineering majors.')],
    },
]


def load_awards():
    if not os.path.exists(IPEDS):
        print('missing %s -- run: python scratchpad/ipeds.py dump' % IPEDS)
        sys.exit(1)
    return json.load(io.open(IPEDS, encoding='utf-8'))


def schools_for(prefixes, awards):
    """Distinct institutions awarding anything under any of these CIP prefixes."""
    out = {}
    for cip, rows in awards.items():
        if not any(cip.startswith(p) for p in prefixes):
            continue
        for r in rows:
            k = r['unitid'] if 'unitid' in r else r['school']
            e = out.setdefault(k, {'school': r['school'], 'awards': set(), 'completions': 0})
            e['awards'].add(r['award'])
            e['completions'] += r['completions']
    return out


def main():
    awards = load_awards()

    programs = []
    for p in PROGRAMS:
        prefixes = [c for c, _ in p['cips']]
        found = schools_for(prefixes, awards)
        programs.append({
            'slug': p['slug'], 'name': p['name'], 'description': p['description'],
            'degreesNote': p['degreesNote'], 'sortOrder': p['sortOrder'],
            'cips': [{'cipCode': c, 'note': n} for c, n in p['cips']],
        })
        print('%-26s %-22s %3d Florida public institutions, award levels: %s'
              % (p['name'], ','.join(prefixes), len(found),
                 ', '.join(sorted({a for v in found.values() for a in v['awards']}))[:70]))

    # The award cross-reference, flattened for seeding.
    rows = []
    for cip, v in awards.items():
        for r in v:
            rows.append({'unitId': r['unitid'], 'institutionName': r['school'],
                         'cipCode': cip, 'awardLevel': r['award'],
                         'completions': r['completions'], 'year': IPEDS_YEAR})
    print('\naward rows: %d across %d CIP codes' % (len(rows), len(awards)))

    if '--report' in sys.argv:
        return 0

    os.makedirs(SEED, exist_ok=True)
    json.dump({'note': 'Programmes are curated. CIP codes are PREFIXES and are matched as such; '
                       'many CIP codes are supported by more than one programme.',
               'programs': programs},
              io.open(os.path.join(SEED, 'programs.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    json.dump({'source': 'IPEDS completions C%d_A, Florida PUBLIC institutions, first majors only'
                         % IPEDS_YEAR,
               'year': IPEDS_YEAR, 'awards': rows},
              io.open(os.path.join(SEED, 'institution_awards.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('wrote programs.json and institution_awards.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
