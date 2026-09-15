#!/usr/bin/env python
"""survey.py -- pre-batch survey for a set of course ids.

Written 2026-09-15 (batch 213) as a reusable replacement for the per-batch
b2NN_survey.py scripts. Answers, in one pass, the questions Tools/CLAUDE.md
says to ask BEFORE drafting:

  * which PUBLIC institutions carry the exact id, with each one's own title,
    credits and clock hours              (RESOLVE THE RANGE)
  * the statewide title, and whether it agrees with the institution titles
                                          (title/description test, batch 208)
  * Gordon Rule and general-education flags, per institution
                                          (institution-specific, batch 201)
  * hs_credit / transferable / dual-enrolment, WITH the prefix distribution
    so you can tell a signal from boilerplate       (batch 207)
  * the prefix's single-carrier percentage           (batch 207-210 baseline)
  * whether a guide is ALREADY LIVE on the site      (batch 202 -- check EVERY
    course in the batch, not only the requested ones)

    python survey.py BCN2210 BCN2251C BCN3281C
    python survey.py --prefix BCN            # whole prefix summary only
    python survey.py --no-live BCN2210       # skip the network check

*** TWO TRAPS THIS SCRIPT EXISTS TO AVOID ***

 1. scns.is_public() wants an institution CODE ('UWF'), not the flat file's
    zero-padded institution ID ('0000082'). Passing the id makes EVERY carrier
    read as private -- which nearly skipped batch 212 entirely. inst_map.json
    keys are UNPADDED, so the lookup needs str(int(id)).
 2. The flag values are 'Y'/'N' STRINGS, so `if r.get(k)` is true for 'N' and
    reports every course as carrying every designation. Test == 'Y'.
"""
import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scns

# Windows consoles default to cp1252 and institution titles are arbitrary data,
# so reconfigure stdout rather than hoping every title is ASCII.
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
FLAT = os.path.join(HERE, 'crslist.txt')
INST_MAP = os.path.join(HERE, 'inst_map.json')
SITE = 'https://floridacourserepo.com'

FLAGS = ['gordon_rule', 'gordon_writing', 'ge_com', 'ge_hum', 'ge_math',
         'ge_nat_sci', 'ge_soc_sci']

_inst = json.load(open(INST_MAP, encoding='utf-8'))


def inst_of(instid):
    """Flat-file ids are zero-padded; inst_map keys are not. Returns (code, name)."""
    s = instid.strip()
    v = _inst.get(str(int(s))) if s.isdigit() else None
    if not v:
        return s, '(unknown)'
    code = v.split(' - ')[0].strip()
    name = v.split(' - ', 1)[1].strip() if ' - ' in v else v
    return code, name


def load_prefix(pfx, cache={}):
    if pfx not in cache:
        rows = list(scns.parse_flatfile(FLAT, prefix=pfx, active_only=True))
        by = collections.defaultdict(list)
        for r in rows:
            by[r['code']] = by[r['code']] + [r]
        cache[pfx] = (rows, by)
    return cache[pfx]


def prefix_summary(pfx):
    rows, by = load_prefix(pfx)
    ids = sorted(by)
    counts = {c: len({r['institution'] for r in by[c]}) for c in ids}
    singles = sum(1 for c in ids if counts[c] == 1)
    print('### %s - %d live ids, %d single-carrier (%d%%), max carriers %d'
          % (pfx, len(ids), singles,
             round(100 * singles / max(len(ids), 1)),
             max(counts.values()) if counts else 0))
    for field in ('hs_credit', 'transferable', 'dual_enrollment'):
        c = collections.Counter(r[field] or '(blank)' for r in rows)
        verdict = 'BOILERPLATE' if len(c) == 1 else 'discriminating'
        print('    %-16s %-46s %s' % (field, str(dict(c.most_common(6)))[:46], verdict))


def live_guide(cid):
    try:
        import requests
        r = requests.get('%s/api/v1/courses/%s/guide' % (SITE, cid), timeout=20)
        return 'GUIDE_NOT_FOUND' not in r.text
    except Exception as exc:
        return '? (%s)' % exc


def survey(cid, check_live=True):
    pfx = cid[:3]
    rows, by = load_prefix(pfx)
    rs = by.get(cid, [])
    print('=' * 78)
    hdr = 'TARGET %s' % cid
    if check_live:
        hdr += '   [guide already live: %s]' % live_guide(cid)
    print(hdr)
    if not rs:
        print('   !! NO ACTIVE CARRIER IN THE FLAT FILE for this exact id')
        near = [c for c in by if c.startswith(cid[:7])]
        if near:
            print('   nearby ids in the family: %s' % ', '.join(sorted(near)))
        return
    pub = [r for r in rs if scns.is_public(inst_of(r['institution'])[0])]
    print('   carriers %d (public %d)' % (len(rs), len(pub)))
    print('   STATE TITLE: %s' % rs[0]['state_title'])
    titles = set()
    for r in sorted(rs, key=lambda x: (x['institution'], x['inst_title'])):
        code, name = inst_of(r['institution'])
        ispub = scns.is_public(code)
        flags = [k for k in FLAGS if r.get(k) == 'Y']
        if ispub:
            titles.add(r['inst_title'].upper())
        print('     %-6s %-7s %-40s cr=%-6s clk=%-6s %s'
              % (code, scns.sector_of(code) if ispub else 'PRIVATE',
                 r['inst_title'][:40], r['credit'], r['clock_hours'],
                 ','.join(flags)))
    creds = {(r['credit'] or '').strip() for r in rs
             if scns.is_public(inst_of(r['institution'])[0])}
    norm = {str(float(c)) for c in creds if c.replace('.', '').isdigit()}
    if len(norm) > 1:
        print('   !! CREDIT DIVERGENCE across public carriers: %s' % sorted(creds))
    if len(titles) > 1:
        print('   !! %d distinct public institution titles - run the title/description test'
              % len(titles))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('courses', nargs='*')
    ap.add_argument('--prefix', nargs='*', default=[])
    ap.add_argument('--no-live', action='store_true')
    a = ap.parse_args()
    for p in sorted({p.upper() for p in a.prefix} |
                    {c[:3].upper() for c in a.courses}):
        prefix_summary(p)
    print()
    for c in a.courses:
        survey(c.upper(), check_live=not a.no_live)


if __name__ == '__main__':
    main()
