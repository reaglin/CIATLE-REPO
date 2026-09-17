#!/usr/bin/env python
"""Build the CIP taxonomy seed for the Career Paths / Programs browse tree.

Ron, 2026-09-17: career paths are "all centered on CIP codes and the CIP codes
become the framework for that page", laid out as at
https://nces.ed.gov/ipeds/cipcode/browse.aspx?y=55

Decisions taken with Ron the same day:
  * tree depth  -- down to 4-DIGIT, limited to groups Florida actually teaches
  * course link -- CURATED ONLY. ⚠⚠⚠ The institution-assigned course CIP data is
                   an AUTHORING AID and is NEVER published as fact. It is used
                   here for ONE purpose: deciding which branches of the tree to
                   show. It never becomes "these courses are classified here".
  * one tree    -- Programs and Career Paths both hang off the same CIP nodes.

SOURCES
  cip2020.csv   the authoritative NCES CIP 2020 file (titles, definitions,
                cross-references, examples) --
                https://nces.ed.gov/ipeds/cipcode/Files/CIPCode2020.csv
                ⚠ Titles and definitions are copied verbatim. We do not write
                our own: these are the federal taxonomy's own words.
  cip_map.json  course -> {institution: cip}, from the Coursedog caches
                (scratchpad/cip_map.json, built by cip_map.py).
  crslist.txt   the SCNS flat file -- every course at every Florida public
                institution, used to widen 3-institution CIP evidence to
                statewide coverage via the course PREFIX.

⚠⚠ WHAT THE PREFIX STEP DOES -- AND WHAT IT CANNOT DO. The CIP evidence covers
three institutions (FIU, FAU, NWFSC). I first built the prefix step believing it
would WIDEN that to statewide coverage. It does not, and the numbers said so:
adding the flat-file filter produced FEWER groups (157) than the raw evidence
(161), because it can only INTERSECT with prefixes already carrying CIP
evidence. A prefix no institution has tagged cannot be mapped by a map built
from tags. So the step's real job is narrower and still worth doing: it drops
groups whose only evidence comes from prefixes Florida no longer actively
carries.

⚠⚠⚠ THE CONSEQUENCE, STATED HONESTLY: 4-digit coverage is bounded by what three
institutions have classified. CIP series 10, 12, 39 and 41 have no evidenced
groups -- 39 (Theology) is a real absence at public institutions, but 41
(Science Technologies) is almost certainly a coverage gap, not a Florida gap.
The LEVEL-2 tree is therefore built from the full taxonomy rather than from
evidence, so the framework is complete and the gaps are visible as empty
branches inviting curation, rather than invisible as missing ones.

⚠⚠⚠ AND THE PREFIX MAP IS NOT SAFE FOR ANYTHING ELSE. Measured: a dominant CIP
accounts for >=60% of votes in 337 of 417 prefixes -- excellent for narrow
prefixes (ACG 100%, PHY 100%, PHI 99%) and poor for broad ones (PHC 27%,
FIL 32%, NUR 49%), because those genuinely span several CIP codes. Good enough
to decide "does Florida teach anything in this group"; nowhere near good enough
to tell a student a course belongs to a programme.

    python build_cip_seed.py            # write PreseMakerRepo.Api/Data/Seed/cip.json
    python build_cip_seed.py --report   # show what it would emit, write nothing
"""
import csv
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, 'scratchpad')
CIP_CSV = os.path.join(SCRATCH, 'cip2020.csv')
CIP_MAP = os.path.join(SCRATCH, 'cip_map.json')
FLAT = os.path.join(SCRATCH, 'crslist.txt')
OUT = os.path.join(HERE, '..', 'PreseMakerRepo.Api', 'Data', 'Seed', 'cip.json')

# A dominant CIP below this share of a prefix's votes is too mixed to trust even
# for scoping, so the prefix contributes ALL its observed CIP groups instead of
# just the winner. Broad prefixes genuinely span several groups.
DOMINANT = 0.60

# CIP series that exist in the taxonomy but are not postsecondary programmes a
# Florida college teaches. Excluded deliberately rather than by absence of
# evidence, so the reason is on the record.
EXCLUDE_SERIES = {
    '21': 'reserved by NCES',
    '55': 'reserved by NCES',
    '32': 'basic skills / developmental, not a programme',
    '33': 'citizenship activities, not a programme',
    '34': 'health-related knowledge and skills, not a programme',
    '35': 'interpersonal and social skills, not a programme',
    '36': 'leisure and recreational activities, not a programme',
    '37': 'personal awareness and self-improvement, not a programme',
    '53': 'high school diplomas and certificates, not postsecondary',
    '60': 'health professions residency/fellowship, post-degree',
    '61': 'medical residency/fellowship, post-degree',
}


def norm(c):
    return (c or '').strip().strip('="').strip()


def load_cip():
    """code -> {title, definition, examples, crossrefs}. Verbatim from NCES."""
    out = {}
    with io.open(CIP_CSV, encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            c = norm(r['CIPCode'])
            if not c:
                continue
            out[c] = {
                'title': (r['CIPTitle'] or '').strip().rstrip('.'),
                'definition': (r['CIPDefinition'] or '').strip(),
                'examples': (r['Examples'] or '').strip(),
                'crossrefs': (r['CrossReferences'] or '').strip(),
            }
    return out


def prefix_cip():
    """SCNS prefix -> set of 4-digit CIP groups it plausibly belongs to."""
    m = json.load(io.open(CIP_MAP, encoding='utf-8'))
    votes = defaultdict(Counter)
    for course, by in m.items():
        for cip in by.values():
            votes[course[:3]][cip[:5]] += 1
    out = {}
    for p, c in votes.items():
        top, n = c.most_common(1)[0]
        total = sum(c.values())
        # A clear winner scopes to itself; a mixed prefix contributes every
        # group it was seen in, because it genuinely spans them.
        out[p] = {top} if n / total >= DOMINANT else set(c)
    return out


def florida_prefixes():
    """Every prefix carried by a Florida public institution, from the flat file."""
    if not os.path.exists(FLAT):
        return None
    seen = set()
    with open(FLAT, 'rb') as fh:
        for line in fh:
            # ⚠ status occupies bytes 26-29 and is RIGHT-justified (b'  A'),
            # so testing line[26:27] reads a space and silently matches nothing.
            if len(line) > 29 and line[26:29].strip() == b'A':        # ACTIVE
                seen.add(line[10:13].decode('latin1'))
    return seen


def build():
    cip = load_cip()
    pmap = prefix_cip()
    fl = florida_prefixes()

    groups = set()
    if fl:
        for p in fl:
            groups |= pmap.get(p, set())
        scope = 'statewide (SCNS flat file prefixes x prefix->CIP map)'
    else:
        for s in pmap.values():
            groups |= s
        scope = 'three-institution CIP evidence only (flat file not found)'

    groups = {g for g in groups if g in cip and g[:2] not in EXCLUDE_SERIES}
    # ⚠ Level 2 is the COMPLETE taxonomy minus the deliberately excluded
    # non-programme series -- not merely the series we have evidence for. Ron
    # scoped the 4-DIGIT level to "where we have courses"; the framework itself
    # should still look like NCES, with unpopulated branches visible.
    series = sorted(c for c in cip if len(c) == 2 and c not in EXCLUDE_SERIES)

    nodes = []
    for s in series:
        meta = cip.get(s, {})
        kids = sorted(g for g in groups if g.startswith(s + '.'))
        nodes.append({
            'code': s,
            'level': 2,
            'title': meta.get('title', ''),
            'definition': meta.get('definition', ''),
            'parent': None,
            'childCount': len(kids),
        })
        for g in kids:
            gm = cip.get(g, {})
            # ⚠ 4-digit definitions in the NCES file are usually the placeholder
            # "Instructional content for this group is defined in codes X - Y".
            # Carry it anyway but flag it so the page can prefer child titles.
            d = gm.get('definition', '')
            placeholder = bool(re.match(r'(?i)\s*instructional content .* defined in code', d))
            nodes.append({
                'code': g,
                'level': 4,
                'title': gm.get('title', ''),
                'definition': '' if placeholder else d,
                'examples': gm.get('examples', ''),
                'parent': s,
                'childCount': 0,
            })
    return nodes, series, groups, scope, cip


def main():
    if not os.path.exists(CIP_CSV):
        print('missing %s -- download CIPCode2020.csv from NCES first' % CIP_CSV)
        return 1
    nodes, series, groups, scope, cip = build()

    print('scope basis      : %s' % scope)
    empty = sorted(s for s in series if not any(n['parent'] == s for n in nodes))
    print('CIP series       : %d of 50 (%d excluded by policy as non-programme)'
          % (len(series), len(EXCLUDE_SERIES)))
    print('4-digit groups   : %d of 473 (evidence-scoped)' % len(groups))
    print('total seed nodes : %d' % len(nodes))
    if empty:
        print('series with no evidenced groups yet: %s' % ', '.join(empty))

    if '--report' in sys.argv:
        print()
        for s in series:
            kids = [n for n in nodes if n['parent'] == s]
            print('  %-4s %-58s %2d groups' % (s, cip[s]['title'][:58], len(kids)))
        return 0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, 'w', encoding='utf-8') as fh:
        json.dump({
            'source': 'NCES CIP 2020 (CIPCode2020.csv); titles and definitions verbatim',
            'scope': scope,
            'note': ('4-digit groups are limited to those Florida public institutions have '
                     'course evidence for. Course-to-CIP association is NOT published: paths '
                     'and programmes attach courses by curation only.'),
            'nodes': nodes,
        }, fh, ensure_ascii=False, indent=1)
    print('\nwrote %s' % os.path.normpath(OUT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
