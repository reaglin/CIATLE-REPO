#!/usr/bin/env python
"""IPEDS completions — which Florida schools actually AWARD which programmes.

⚠⚠⚠ THIS IS THE MISSING SOURCE FOR THE PROGRAM LAYER. The site holds COURSES and
their offerings, which answers "where can I take this course". It has never held
PROGRAMME data, so it could not answer "which schools offer this major" — the
cross-reference Ron asked for on 2026-09-17.

IPEDS answers it federally, for every institution, keyed to CIP:

    C<year>_A.csv   completions by UNITID x CIPCODE x AWLEVEL, with counts
    HD<year>.csv    the institution directory: name, state, control, sector

Both download without a gate from nces.ed.gov (the CIP browse pages are the same
host, already used for the taxonomy). ⚠ Read them with encoding='utf-8-sig' —
the first column name carries a BOM and a plain utf-8 read silently loses it,
which looks like a missing UNITID column.

⚠⚠ AND IT CONFIRMS RON'S DEFINITION OF A PROGRAM. He wrote: "Nursing AS (the
major) = Nursing (the program) and Nursing BSN (the major) = Nursing (the
program). Nursing programs will encompass nursing degrees." That is exactly the
shape of the data: Broward College under CIP 51.3801 shows an ASSOCIATE (413
completions) and a BACHELOR'S (64) — two majors, one programme, one school.

    python ipeds.py fetch                # download the two files
    python ipeds.py cip 51.3801          # which FL schools award it, at what level
    python ipeds.py school "Valencia"    # what one school awards
    python ipeds.py dump                 # cache FL public rows -> ipeds_fl.json
"""
import collections
import csv
import io
import json
import os
import sys
import urllib.request
import zipfile

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
YEAR = 2023
COMP = os.path.join(HERE, 'C%d_A.zip' % YEAR)
DIRY = os.path.join(HERE, 'HD%d.zip' % YEAR)
CACHE = os.path.join(HERE, 'ipeds_fl.json')
UA = {'User-Agent': 'Mozilla/5.0'}

# IPEDS AWLEVEL -> the award a student actually receives. This is the "major"
# level in Ron's terms; the CIP above it is the "programme".
AWARD = {
    # ⚠ Verified against the official C2023_A dictionary (Frequencies sheet), NOT guessed.
    # An earlier hand-written map had 20 and 21 SWAPPED and mislabelled 4, 6 and 8.
    '1':  'Certificate (<1 year)',
    '2':  'Certificate (1-2 years)',
    '3':  "Associate",
    '4':  'Certificate (2-4 years)',
    '5':  "Bachelor's",
    '6':  'Postbaccalaureate certificate',
    '7':  "Master's",
    '8':  "Post-master's certificate",
    '17': "Doctorate (research/scholarship)",
    '18': 'Doctorate (professional practice)',
    '19': 'Doctorate (other)',
    '20': 'Certificate (<12 weeks)',
    '21': 'Certificate (12 weeks-1 year)',
}
# ⚠⚠ AGGREGATE rows. 12 "Degrees total", 13 "Certificates below the baccalaureate total",
# 14 "Certificates above the baccalaureate total", 15 "Degrees/certificates total" are SUMS
# of the rows above. They are absent from the 2023 file, but including one would double-count
# every completion at that institution, so they are refused explicitly rather than trusted.
AGGREGATE = {'12', '13', '14', '15'}

# CONTROL: 1 public, 2 private not-for-profit, 3 private for-profit.
# ⚠ The project's scope rule is PUBLIC INSTITUTIONS ONLY (Ron, 2026-09-11).
PUBLIC = '1'


def fetch():
    for url, path in [
        ('https://nces.ed.gov/ipeds/datacenter/data/C%d_A.zip' % YEAR, COMP),
        ('https://nces.ed.gov/ipeds/datacenter/data/HD%d.zip' % YEAR, DIRY),
    ]:
        if os.path.exists(path):
            print('have %s' % os.path.basename(path))
            continue
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=300) as r, open(path, 'wb') as fh:
            fh.write(r.read())
        print('downloaded %s (%d bytes)' % (os.path.basename(path), os.path.getsize(path)))


def _rows(zpath, member):
    with zipfile.ZipFile(zpath) as z:
        name = member if member in z.namelist() else z.namelist()[0]
        # ⚠ utf-8-sig, not utf-8: the header carries a BOM.
        for r in csv.DictReader(io.TextIOWrapper(z.open(name), encoding='utf-8-sig',
                                                 errors='replace')):
            yield r


def schools():
    """UNITID -> {name, control, public} for Florida only."""
    out = {}
    for r in _rows(DIRY, 'HD%d.csv' % YEAR):
        if r.get('STABBR') == 'FL':
            out[r['UNITID']] = {'name': r['INSTNM'], 'control': r.get('CONTROL', ''),
                                'public': r.get('CONTROL') == PUBLIC}
    return out


def completions(fl):
    """(cip, unitid) -> [(award level label, completions)] for Florida institutions.

    ⚠ MAJORNUM == '1' only. A second-major row double-counts the student, which
    would inflate every programme that is commonly taken as a double major.
    """
    out = collections.defaultdict(list)
    for r in _rows(COMP, 'C%d_a.csv' % YEAR):
        u = r['UNITID']
        if u in fl and r.get('MAJORNUM') == '1' and r['AWLEVEL'] not in AGGREGATE:
            out[r['CIPCODE']].append(
                (u, AWARD.get(r['AWLEVEL'], 'level ' + r['AWLEVEL']),
                 int(r.get('CTOTALT') or 0)))
    return out


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__.strip().split('\n\n')[0])
        print('\nusage: ipeds.py fetch | cip <nn.nnnn> | school <text> | dump')
        return 2
    if a[0] == 'fetch':
        fetch()
        return 0
    if not (os.path.exists(COMP) and os.path.exists(DIRY)):
        print('missing data; run: python ipeds.py fetch')
        return 1

    fl = schools()
    comp = completions(fl)

    if a[0] == 'cip' and len(a) > 1:
        key = a[1]
        hits = [(fl[u]['name'], lvl, n, fl[u]['public'])
                for c, v in comp.items() if c.startswith(key) for u, lvl, n in v]
        pub = [h for h in hits if h[3]]
        print('CIP %s: %d Florida award rows, %d at PUBLIC institutions'
              % (key, len(hits), len(pub)))
        for name, lvl, n, _ in sorted(pub, key=lambda x: (-x[2], x[0])):
            print('   %-50s %-30s %5d' % (name[:50], lvl, n))
    elif a[0] == 'school' and len(a) > 1:
        q = ' '.join(a[1:]).lower()
        ids = [u for u, v in fl.items() if q in v['name'].lower()]
        for c, v in sorted(comp.items()):
            for u, lvl, n in v:
                if u in ids and n > 0:
                    print('   %-9s %-30s %-46s %5d' % (c, lvl, fl[u]['name'][:46], n))
    elif a[0] == 'dump':
        out = {}
        for c, v in comp.items():
            rows = [{'unitid': u, 'school': fl[u]['name'], 'award': lvl, 'completions': n}
                    for u, lvl, n in v if fl[u]['public']]
            if rows:
                out[c] = rows
        json.dump(out, io.open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('wrote %s: %d CIP codes with Florida PUBLIC award rows'
              % (os.path.basename(CACHE), len(out)))
    else:
        print('unknown command')
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
