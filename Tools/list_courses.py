#!/usr/bin/env python3
"""list_courses.py -- LIST courses on floridacourserepo.com, with no guide.

Ron's direction, 2026-09-11:

    "A top priority will be picking up any courses we see at institutions along the
     way and list them (no guide)."

Writing a guide means reading SCNS, and that reading surfaces hundreds of courses the
site does not hold. This turns that byproduct into catalog data: it builds course rows
from the SCNS flat file and pushes them over POST /api/v1/courses/batch.

    python list_courses.py --prefix CET EET --dry-run     # see what would be sent
    python list_courses.py --prefix CET EET --yes         # send it
    python list_courses.py --institutions --yes           # send the institution list first

Contract: Tools/COURSE_API.md.  Rules: the course-catalog section of Tools/CLAUDE.md.

*** THE THREE THINGS THAT GO WRONG ***

 1. replaceOfferings defaults to TRUE on the server. This sends a course's FULL public
    offering list every time, which is what makes that safe.
 2. A course upsert DOES overwrite an existing title. That is wanted -- most courses on
    the site carry the course id as a placeholder -- but it means the title sent must be
    a real one, never the id.
 3. PSAV clock-hour courses carry their hours in the credit field in some records. A
    credit value over 20 is not a credit value; it becomes contact hours with credits 0.
"""
import argparse
import collections
import json
import os
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'scratchpad'))
from scns import parse_flatfile, is_public, sector_of      # noqa: E402

BASE = 'https://floridacourserepo.com'
BATCH = 400                      # server cap is 500; leave headroom
SHELL = {'900', '905', '910', '920', '930', '940', '941', '945', '949',
         '950', '951', '971', '973', '980', '981', '990', '991'}

SMALL = {'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'in', 'of', 'on', 'or',
         'the', 'to', 'with', 'per', 'vs'}
KEEP_UPPER = {'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'PC', 'CCNA',
              'CCNP', 'LAN', 'WAN', 'IT', 'AC', 'DC', 'CAD', 'CADD', 'UNIX', 'OSHA',
              'HVAC', 'CNC', 'PLC', 'IOS', 'IP', 'TCP', 'RF', 'US', 'USA', 'GPS', 'CIS',
              'CBT', 'FSU', 'UWF', 'UCF', 'FIU', 'FAMU', 'FGCU', 'UNF', 'USF', 'UF',
              'GIS', 'CPR', 'EMT', 'MRI', 'ASL', 'TV', 'AI', 'ML', 'UX', 'UI', 'HTML',
              'SQL', 'PHP', 'CSS', 'API', 'STEM', 'MIDI', 'NCLEX', 'FE', 'PE'}


def smart_title(s):
    """Title-case an ALL-CAPS catalog title without mangling it.

    The SCNS export is entirely upper-case, so str.title() yields 'Digital Fundamentals
    And Lab' and 'Ccna2'.  Order matters: the small-word test must come BEFORE any
    "looks like an acronym" heuristic, because an all-caps source carries no case signal
    and such a rule fires on AND, THE, TO and OF.
    """
    words = s.split()
    out = []
    for i, w in enumerate(words):
        core = w.strip('()[],.:;/&\'"')
        if core.upper() in KEEP_UPPER:
            out.append(w.upper())
        elif len(core) > 1 and core.lower() in SMALL and i not in (0, len(words) - 1):
            out.append(w.lower())
        elif any(ch.isdigit() for ch in core):
            out.append(w.upper())
        else:
            # Capitalise after an internal separator too. SCNS writes compound titles as
            # "SPECIAL TOPICS/SEMINARS" and "CO-OP", and a plain w[0].upper() leaves
            # "Topics/seminars" and "Co-op".
            out.append(_cap_parts(w))
    return ' '.join(out)


def _cap_one(part):
    if not part:
        return part
    if part.upper() in KEEP_UPPER or any(c.isdigit() for c in part):
        return part.upper()
    return part[:1].upper() + part[1:].lower()


def _cap_parts(w):
    res, start = [], 0
    for i, ch in enumerate(w):
        if ch in '/-&':
            res.append(_cap_one(w[start:i]) + ch)
            start = i + 1
    res.append(_cap_one(w[start:]))
    return ''.join(res)


def num(raw):
    """SCNS credit/clock field -> float, or None for blank and variable-credit ranges."""
    raw = (raw or '').strip()
    if not raw or '-' in raw:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def api(path, payload=None, token=None, method=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        BASE + path, data=data, method=method or ('POST' if data else 'GET'),
        headers={'Content-Type': 'application/json', 'User-Agent': 'list_courses',
                 **({'Authorization': 'Bearer ' + token} if token else {})})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'replace')[:600]
        raise SystemExit('HTTP %s on %s\n%s' % (e.code, path, body))


def login():
    from dotenv import load_dotenv
    load_dotenv(os.path.join(HERE, '.env'))
    r = api('/api/v1/auth/login', {'email': os.environ['REPO_ADMIN_EMAIL'],
                                   'password': os.environ['REPO_ADMIN_PASSWORD']})
    return r['data']['accessToken']


def institution_rows(inst_map):
    rows = []
    for code_id, label in sorted(inst_map.items(), key=lambda kv: kv[1]):
        if ' - ' not in label or 'INACTIVE' in label:
            continue
        code, name = label.split(' - ', 1)
        if not is_public(code):
            continue
        rows.append({'code': code, 'name': smart_title(name),
                     'sector': sector_of(code), 'scnsId': str(code_id)})
    return rows


def course_rows(flat_path, prefixes, inst_map, keep_shell=True):
    """Build one course row per SCNS id, with every PUBLIC institution as an offering."""
    by_int = {int(k): v for k, v in inst_map.items()}
    short = lambda i: by_int.get(int(i), '?').split(' - ')[0]           # noqa: E731

    codes = collections.defaultdict(list)
    for p in prefixes:
        for r in parse_flatfile(flat_path, prefix=p):
            if is_public(short(r['institution'])):
                codes[r['code']].append(r)

    rows, skipped = [], collections.Counter()
    for code, recs in sorted(codes.items()):
        if not keep_shell and code[4:7] in SHELL:
            skipped['shell'] += 1
            continue

        titles = collections.Counter(r['inst_title'].strip() for r in recs if r['inst_title'].strip())
        if not titles:
            skipped['no title'] += 1
            continue
        title = smart_title(titles.most_common(1)[0][0])[:300]

        state = next((r['state_title'].strip() for r in recs if r['state_title'].strip()), '')
        state_title = smart_title(state)[:300] if state else None

        # Credits: the modal value across institutions, as an integer.
        vals = [num(r['credit']) for r in recs]
        vals = [v for v in vals if v is not None]
        credits = contact = None
        if vals:
            modal = collections.Counter(vals).most_common(1)[0][0]
            if modal > 20:
                # Not a credit value -- a PSAV clock-hour count in the credit field.
                credits, contact = 0, min(int(modal), 3000)
            else:
                credits = int(round(modal))

        offerings = []
        for r in sorted(recs, key=lambda r: short(r['institution'])):
            cr = num(r['credit'])
            ck = num(r['clock_hours'])
            if cr is not None and cr > 20:          # same clock-hour trap, per offering
                ck, cr = cr, None
            o = {'institution': short(r['institution'])[:10], 'isActive': True}
            if r['inst_title'].strip():
                o['title'] = smart_title(r['inst_title'].strip())[:300]
            if cr is not None and 0 <= cr <= 99:
                o['credits'] = round(cr, 2)
            if ck is not None and 0 <= ck <= 3000:
                o['clockHours'] = int(ck)
            offerings.append(o)

        row = {'courseId': code, 'title': title, 'isActive': True,
               'offerings': offerings[:250], 'replaceOfferings': True}
        if state_title and state_title.lower() != title.lower():
            row['stateTitle'] = state_title
        if credits is not None:
            row['creditHours'] = credits
        if contact is not None:
            row['contactHours'] = contact
        rows.append(row)
    return rows, skipped


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--prefix', nargs='*', default=[], help='SCNS prefixes to list')
    ap.add_argument('--flat', default=None, help='path to crslist.txt')
    ap.add_argument('--inst-map', default=None, help='path to inst_map.json')
    ap.add_argument('--institutions', action='store_true', help='push the institution list')
    ap.add_argument('--no-shell', action='store_true', help='omit x9xx shell numbers')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--yes', action='store_true')
    a = ap.parse_args()

    sp = os.path.join(HERE, 'scratchpad')
    flat = a.flat or os.path.join(sp, 'crslist.txt')
    imap = a.inst_map or os.path.join(sp, 'inst_map.json')
    if not os.path.exists(flat):
        raise SystemExit('no flat file at %s -- run: python scratchpad/scns.py flatfile %s' % (flat, flat))
    inst_map = json.load(open(imap, encoding='utf-8'))

    token = None if a.dry_run else login()

    if a.institutions:
        rows = institution_rows(inst_map)
        print('institutions: %d public' % len(rows))
        if a.dry_run:
            for r in rows[:5]:
                print('  ', r)
        else:
            r = api('/api/v1/institutions/batch', {'institutions': rows}, token)
            print('  ->', json.dumps(r.get('data'))[:300])

    if not a.prefix:
        return 0

    rows, skipped = course_rows(flat, [p.upper() for p in a.prefix], inst_map,
                                keep_shell=not a.no_shell)
    print('courses built: %d  (offerings %d)  skipped %s'
          % (len(rows), sum(len(r['offerings']) for r in rows), dict(skipped) or '{}'))
    if a.dry_run:
        for r in rows[:4]:
            print('  ', json.dumps(r)[:260])
        return 0
    if not a.yes:
        raise SystemExit('refusing to push without --yes')

    tot = collections.Counter()
    for i in range(0, len(rows), BATCH):
        chunk = rows[i:i + BATCH]
        r = api('/api/v1/courses/batch', {'courses': chunk}, token)
        d = r['data']
        for k in ('created', 'updated', 'unchanged', 'failed'):
            tot[k] += d.get(k, 0)
        print('  batch %-3d %-4d sent | created %-4d updated %-4d unchanged %-4d failed %d'
              % (i // BATCH + 1, len(chunk), d.get('created', 0), d.get('updated', 0),
                 d.get('unchanged', 0), d.get('failed', 0)))
        for res in d.get('results', []):
            if res.get('outcome') == 'failed':
                print('    FAILED %s: %s %s' % (res.get('courseId'), res.get('errorCode'),
                                                (res.get('message') or '')[:120]))
    print('TOTAL created %d  updated %d  unchanged %d  failed %d'
          % (tot['created'], tot['updated'], tot['unchanged'], tot['failed']))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
