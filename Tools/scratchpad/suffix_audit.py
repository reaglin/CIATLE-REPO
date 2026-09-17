#!/usr/bin/env python
"""Which LISTED course ids are the MINORITY form of a bare/C/L twin?

REVIEW_QUEUE item 106 found two: the site lists STA2023C (1 public carrier) and
ENC1101C (3) while STA2023 (52) and ENC1101 (51) are not listed at all. Building
the Mechanical Engineer career path hit three more on the calculus sequence, so
the question "is this systematic?" -- item 106's third open point -- has stopped
being hypothetical and is now blocking the engineering cluster.

This answers it. For every course the site lists, count the PUBLIC carriers of
that exact id and of its bare/C/L twins in the SCNS flat file, and report the
ones where the site is showing a form far less carried than a twin.

    python suffix_audit.py            # the ranked report
    python suffix_audit.py --guides   # only ids that carry a published guide
"""
import collections
import json
import sys
import urllib.request

import scns

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

API = 'https://floridacourserepo.com/api/v1/courses/catalog?pageSize=1000&page=%d'
# Below this ratio the listed form is a rounding error against its twin.
RATIO = 3


def listed_courses():
    """course id -> hasGuide, for everything the site lists."""
    out, page = {}, 1
    while True:
        with urllib.request.urlopen(API % page, timeout=120) as r:
            d = json.load(r)['data']
        for i in d['items']:
            out[i['courseId']] = bool(i.get('hasGuide'))
        if len(d['items']) < 1000:
            break
        page += 1
        if page > 20:
            break
    return out


def carriers():
    """exact course id -> set of PUBLIC institution codes."""
    m = scns.institution_map()
    out = collections.defaultdict(set)
    for r in scns.parse_flatfile('crslist.txt'):
        if r['status'].strip() != 'A':
            continue
        cid = (r['prefix'] + r['level'] + r['century'] + r['decade']
               + r['unit'] + r['lab'].strip())
        name = m.get(r['institution'].lstrip('0')) or ''
        code = name.split(' - ')[0] if name else ''
        if code and scns.is_public(code):
            out[cid].add(code)
    return out


def main():
    only_guides = '--guides' in sys.argv
    print('reading the live catalog...')
    listed = listed_courses()
    print('  %d courses listed' % len(listed))
    print('parsing the SCNS flat file...')
    car = carriers()
    print('  %d active ids with a public carrier' % len(car))

    rows = []
    for cid, has_guide in listed.items():
        if '-' in cid:                      # -SCNS / -INST variants are deliberate
            continue
        base = cid[:7]
        if len(cid) < 7 or not cid[3:7].isdigit():
            continue
        twins = {base, base + 'C', base + 'L'} - {cid}
        mine = len(car.get(cid, ()))
        best, best_n = None, 0
        for t in twins:
            n = len(car.get(t, ()))
            if n > best_n:
                best, best_n = t, n
        if best and best_n >= RATIO * max(mine, 1) and best_n >= 8:
            rows.append((best_n - mine, cid, mine, best, best_n,
                         has_guide, best in listed))

    rows.sort(reverse=True)
    if only_guides:
        rows = [r for r in rows if r[5]]

    print()
    print('%-10s %5s   %-10s %5s  %-7s %s'
          % ('LISTED', 'carr', 'BETTER TWIN', 'carr', 'guide?', 'twin listed?'))
    for _, cid, mine, twin, tn, has_guide, twin_listed in rows[:40]:
        print('%-10s %5d   %-10s %5d  %-7s %s'
              % (cid, mine, twin, tn, 'YES' if has_guide else '-',
                 'yes' if twin_listed else '⚠ NO'))

    worst = [r for r in rows if r[5] and not r[6]]
    print()
    print('%d listed id(s) are the minority form of a much-better-carried twin.' % len(rows))
    print('⚠⚠ %d of those carry a PUBLISHED GUIDE while the majority twin is NOT LISTED '
          'at all -- a student searching the number their own college uses finds nothing.'
          % len(worst))
    return 0


if __name__ == '__main__':
    sys.exit(main())
