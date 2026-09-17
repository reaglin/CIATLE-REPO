#!/usr/bin/env python
"""Batch 235 research: ENC1101, STA2023, BSC2085, BSC2086.

The four courses published career paths name that have no guide (Ron's rule,
2026-09-17: a course that spans a major on a career path gets a guide).

All four are the BARE majority form whose C-twin already carries a guide
(REVIEW_QUEUE item 106), so this also has to say what the relationship is.
"""
import collections
import csv
import io
import os
import sys

import scns

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
TARGETS = ['ENC1101', 'STA2023', 'BSC2085', 'BSC2086']
FLAGS = ['gordon_rule', 'gordon_writing', 'ge_com', 'ge_hum', 'ge_math',
         'ge_nat_sci', 'ge_soc_sci']


def flat():
    """exact id -> list of rows (public only), plus the institution code."""
    m = scns.institution_map()
    out = collections.defaultdict(list)
    for r in scns.parse_flatfile(os.path.join(HERE, 'crslist.txt')):
        if r['status'].strip() != 'A':
            continue
        cid = (r['prefix'] + r['level'] + r['century'] + r['decade']
               + r['unit'] + r['lab'].strip())
        name = m.get(r['institution'].lstrip('0')) or ''
        code = name.split(' - ')[0] if name else ''
        if code and scns.is_public(code):
            r['_code'] = code
            out[cid].append(r)
    return out


def statewide(prefix):
    p = os.path.join(HERE, 'sw_%s.csv' % prefix)
    if not os.path.exists(p):
        p = os.path.join(HERE, 'sw_%s.csv' % prefix.lower())
    if not os.path.exists(p):
        return []
    return scns.read_report_csv(p)


def main():
    f = flat()
    print('=' * 78)
    for cid in TARGETS:
        pfx = cid[:3]
        rows = f.get(cid, [])
        twin = cid + 'C'
        trows = f.get(twin, [])
        print('\n### %s   (%d public carriers)   vs %s (%d)'
              % (cid, len(rows), twin, len(trows)))

        creds = collections.Counter(r['credit'].strip() for r in rows)
        print('  credits: %s' % dict(creds))
        titles = collections.Counter(r['inst_title'].strip() for r in rows)
        print('  %d distinct institution titles; commonest:' % len(titles))
        for t, n in titles.most_common(4):
            print('      %-52s %d' % (t[:52], n))

        # ⚠ 'Y'/'N' STRINGS -- never test for truthiness (batch 207).
        for k in FLAGS:
            yes = [r['_code'] for r in rows if r.get(k) == 'Y']
            if yes:
                print('  %-14s %2d/%d  %s' % (k, len(yes), len(rows), ' '.join(sorted(yes)[:14])))

        sw = [r for r in statewide(pfx)
              if r.get('ID_Century', '') and r.get('CourseStatus') == 'ACTIVE']
        me = [r for r in sw if (pfx + r['ID_Century'][:1] + r['ID_Century'][1:]).startswith(cid[:3])
              and r.get('ID_Century', '')[:4] == cid[3:7]]
        for r in me[:1]:
            print('  statewide title : %s' % r.get('ID_CourseTitle', '')[:70])
            print('  transferable    : %s' % (r.get('DS_Transferable1', '') or '')[:66])
            print('  hs credit       : %s' % (r.get('DS_High_School_Credit1', '') or '')[:40])
            print('  prerequisite    : %s' % (r.get('DS_Prerequisites1', '') or '(none)')[:66])
            d = (r.get('DS_CourseDescription1') or '')
            print('  description     : %s' % d[:300].replace('\n', ' '))

        # Stratified distribution test over the population the field applies to.
        und = [r for r in sw if r.get('DS_Course_Intent1') in ('LOWER', 'UPPER')]
        for fld in ('DS_High_School_Credit1', 'DS_Transferable1'):
            c = collections.Counter((r.get(fld) or '').strip()[:34] for r in und)
            if len(c) > 1:
                print('  %s across %d undergrad rows: %s'
                      % (fld[3:-1], len(und), dict(c.most_common(3))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
