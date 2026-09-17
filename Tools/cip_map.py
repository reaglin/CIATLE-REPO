#!/usr/bin/env python
"""Harvest course -> CIP code from the Coursedog caches.

Ron, 2026-09-16: "Once we complete the queue we are going to look at career
paths. All the careers will be bound to CIP codes
https://nces.ed.gov/ipeds/cipcode/browse.aspx?y=55 and that will be the anchor
for the career paths."

CIP is the anchor, so this captures the CIP data the project ALREADY holds
rather than waiting for the career-paths phase to start from nothing. The
Coursedog schools carry a per-course `cipCode` field that no other Florida
source exposes, and the caches are already on disk.

    python cip_map.py                 # build scratchpad/cip_map.json + report
    python cip_map.py --prefix EGN    # what CIP codes a prefix maps to

⚠⚠ TWO FORMAT TRAPS, both real in the data:

1. FIU writes CIP DOTTED ("16.1101"); FAU and NWFSC write it UNDOTTED
   ("240101"). Both are the same 6-digit code. Normalised here to dotted.
2. FSCJ's field is populated on 2 rows out of 22,698, both with the placeholder
   "9999999999". ⚠ A 10-digit value is NOT a CIP code -- treat any value that is
   not 6 digits as absent rather than coercing it.

⚠ A course's CIP is the INSTITUTION's classification of that course, so two
institutions can classify the same SCNS number differently. That disagreement is
data, not error -- it is recorded, not resolved, and the career-paths phase will
want to see it.
"""
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, 'scratchpad')
OUT = os.path.join(SCRATCH, 'cip_map.json')

CACHES = {
    'FIU': 'fiu_courses.json',
    'FAU': 'fau_courses.json',
    'FSCJ': 'fscj_courses.json',
    'NWFSC': 'nwfsc_courses.json',
}

COURSE_RE = re.compile(r'^[A-Z]{3}\d{4}[A-Z]?$')


def normalise(raw):
    """Return a dotted 6-digit CIP, or None if the value is not one."""
    if not raw:
        return None
    d = re.sub(r'\D', '', str(raw))
    if len(d) != 6:          # 9999999999 placeholders and short junk
        return None
    if d == '999999':
        return None
    return d[:2] + '.' + d[2:]


def load():
    out = defaultdict(dict)          # course -> {inst: cip}
    stats = {}
    for inst, fn in CACHES.items():
        p = os.path.join(SCRATCH, fn)
        if not os.path.exists(p):
            stats[inst] = (0, 0)
            continue
        d = json.load(io.open(p, encoding='utf-8'))
        recs = d if isinstance(d, list) else list(d.values())
        good = 0
        for x in recs:
            if not isinstance(x, dict):
                continue
            code = (x.get('code') or '').replace(' ', '').upper()
            if not COURSE_RE.match(code):
                continue
            cip = normalise(x.get('cipCode'))
            if cip:
                out[code][inst] = cip
                good += 1
        stats[inst] = (len(recs), good)
    return out, stats


def main():
    m, stats = load()

    if '--prefix' in sys.argv:
        pfx = sys.argv[sys.argv.index('--prefix') + 1].upper()
        c = Counter()
        for course, by in sorted(m.items()):
            if course.startswith(pfx):
                for inst, cip in by.items():
                    c[cip] += 1
        print('%s — CIP codes seen (%d distinct):' % (pfx, len(c)))
        for cip, n in c.most_common():
            print('   %-9s %d' % (cip, n))
        return 0

    print('cache                 rows    with usable CIP')
    for inst, (rows, good) in sorted(stats.items()):
        print('  %-8s %10d %10d' % (inst, rows, good))

    disagree = {k: v for k, v in m.items() if len(set(v.values())) > 1}
    two_plus = {k: v for k, v in m.items() if len(v) > 1}

    print()
    print('courses with at least one CIP : %d' % len(m))
    print('courses seen at 2+ institutions: %d' % len(two_plus))
    print('  of those, institutions DISAGREE on the CIP: %d (%.0f%%)'
          % (len(disagree), 100.0 * len(disagree) / max(1, len(two_plus))))

    fam = Counter(cip.split('.')[0] for by in m.values() for cip in by.values())
    print()
    print('top CIP families (2-digit) across all mapped courses:')
    for f, n in fam.most_common(12):
        print('   %s   %d' % (f, n))

    with io.open(OUT, 'w', encoding='utf-8') as fh:
        json.dump({k: v for k, v in sorted(m.items())}, fh, ensure_ascii=False, indent=0)
    print()
    print('wrote %s (%d courses)' % (OUT, len(m)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
