# -*- coding: utf-8 -*-
"""Back-catalogue sweep: restore the district-technical-college offerings the old
`is_public()` filter dropped. Ron, 2026-09-20 (REVIEW_QUEUE item 109). Run from Tools/.

    python scratchpad/tech_sweep.py                 # measure only
    python scratchpad/tech_sweep.py --push          # send institutions + course offerings

⚠ SCOPE. Only courses that ACTUALLY GAIN a technical-college carrier are touched — the
offering list there is wrong by omission. A course with no TECH carrier is left alone, so
the sweep cannot disturb the university-level catalogue.

⚠ Offerings are REPLACED, and they are rebuilt from the same source the pipeline has always
used: the SCNS flat file, with each institution's own title, credits and clock hours.
"""
import sys, os, io, json, collections
sys.path.insert(0, 'scratchpad')
import scns, requests

try:
    from dotenv import load_dotenv
    load_dotenv('.env')
except ImportError:
    pass

FLAT = os.path.join('scratchpad', 'crslist.txt')
BASE = os.environ.get('REPO_BASE_URL', 'https://floridacourserepo.com').rstrip('/')
SMALL = {'and', 'or', 'of', 'the', 'for', 'to', 'in', 'with', 'a', 'an', 'on', 'at'}
ACRONYMS = {'HVAC', 'CNG', 'LPG', 'EV', 'AC', 'DC', 'CAD', 'GIS', 'VLSI', 'I', 'II', 'III', 'IV'}


def _word(w, edge):
    if w.upper() in ACRONYMS:
        return w.upper()
    if '.' in w and len(w) <= 5:
        return w.upper()
    if w.lower() in SMALL and not edge:
        return w.lower()
    if w.upper().startswith('MC') and len(w) > 2:
        return 'Mc' + w[2:].capitalize()
    return w.capitalize()


def titlecase(s):
    ws = s.split()
    return ' '.join('-'.join(_word(p, i in (0, len(ws) - 1)) for p in w.split('-'))
                    for i, w in enumerate(ws))


def cid_of(r):
    return (r['prefix'] + r['level'] + r['century'] + r['decade'] + r['unit'] + (r['lab'] or '')).strip().upper()


def live_catalog():
    """Every course the site carries: id -> offeringCount."""
    out, page = {}, 1
    while True:
        d = requests.get('%s/api/v1/courses/catalog' % BASE,
                         params={'page': page, 'pageSize': 500}, timeout=120).json()['data']
        for c in d['items']:
            out[c['courseId']] = c.get('offeringCount') or 0
        if page >= d['totalPages']:
            break
        page += 1
        if page % 10 == 0:
            print('   ... %d courses' % len(out))
    return out


def scns_carriers():
    """course id -> [(code, sector, title, credit, clock)] for PUBLIC carriers, TECH included."""
    # ⚠ Resolve the institution map ONCE. Calling institution_map() inside the row loop
    # re-fetched it per row and turned a two-minute parse into an hour.
    raw_map = scns.institution_map()
    imap = {k: v.split('-')[0].strip() for k, v in raw_map.items()}
    sector = {code: scns.sector_of(code) for code in set(imap.values())}
    names = {code: titlecase(raw.partition('-')[2].strip())
             for key, raw in raw_map.items()
             for code in [imap[key]] if sector.get(code) == 'TECH'}

    per = collections.defaultdict(list)
    for r in scns.parse_flatfile(FLAT):
        if r['status'] != 'A':
            continue
        code = imap.get(r['institution'].lstrip('0'))
        sec = sector.get(code)
        if sec not in ('SUS', 'FCS', 'TECH'):
            continue
        per[cid_of(r)].append((code, sec, (r.get('inst_title') or '').strip(),
                               r.get('credit'), r.get('clock_hours')))
    return per, names


def build_course(cid, rows):
    titles = collections.Counter(t for _, _, t, _, _ in rows if t)
    creds, hours = collections.Counter(), collections.Counter()
    offerings = []
    for code, _sec, t, cr, ch in sorted(set(rows)):
        o = {"institution": code, "title": t or None}
        try:
            o["credits"] = int(float(cr)); creds[o["credits"]] += 1
        except (TypeError, ValueError):
            pass
        try:
            o["clockHours"] = int(float(ch)); hours[o["clockHours"]] += 1
        except (TypeError, ValueError):
            pass
        offerings.append(o)
    c = {"courseId": cid, "offerings": offerings, "replaceOfferings": True}
    if titles:
        c["title"] = titlecase(titles.most_common(1)[0][0])
        c["stateTitle"] = titles.most_common(1)[0][0]
    if creds:
        c["creditHours"] = creds.most_common(1)[0][0]
    if hours:
        c["contactHours"] = hours.most_common(1)[0][0]
    return c


def main():
    push = '--push' in sys.argv
    print('reading the live catalog...')
    live = live_catalog()
    print('   %d courses live' % len(live))
    print('reading the SCNS flat file...')
    per, tech_names = scns_carriers()
    print('   %d course ids with public carriers' % len(per))

    touched, added_rows, tech_hits = [], 0, collections.Counter()
    for cid, count in live.items():
        rows = per.get(cid)
        if not rows:
            continue
        techs = {c for c, s, *_ in rows if s == 'TECH'}
        if not techs:
            continue                      # nothing was dropped for this course
        touched.append(build_course(cid, rows))
        added_rows += len(techs)
        for t in techs:
            tech_hits[t] += 1

    print()
    print('courses on the site that LOST technical-college carriers: %d' % len(touched))
    print('technical-college offerings to restore:                   %d' % added_rows)
    print('technical colleges involved:                              %d' % len(tech_hits))
    for code, n in tech_hits.most_common(8):
        print('   %-8s %-44s %d course(s)' % (code, tech_names.get(code, '')[:44], n))
    byprefix = collections.Counter(c['courseId'][:3] for c in touched)
    print('top prefixes:', ', '.join('%s %d' % kv for kv in byprefix.most_common(12)))

    if not push:
        print('\nmeasure only -- pass --push to send')
        return 0

    s = requests.Session()
    tok = s.post('%s/api/v1/auth/login' % BASE,
                 json={'email': os.environ['REPO_ADMIN_EMAIL'],
                       'password': os.environ['REPO_ADMIN_PASSWORD']}, timeout=20)
    tok.raise_for_status()
    h = {'Authorization': 'Bearer %s' % tok.json()['data']['accessToken']}

    known = {i['code'] for i in requests.get('%s/api/v1/institutions' % BASE, timeout=60).json()['data']}
    new = [{"code": c, "name": n, "sector": "TECH"} for c, n in sorted(tech_names.items())
           if c not in known]
    if new:
        r = s.post('%s/api/v1/institutions/batch' % BASE, json={'institutions': new},
                   headers=h, timeout=120)
        print('institutions: HTTP %s, %d sent' % (r.status_code, len(new)))

    sent = collections.Counter()
    for i in range(0, len(touched), 400):
        chunk = touched[i:i + 400]
        r = s.post('%s/api/v1/courses/batch' % BASE, json={'courses': chunk}, headers=h, timeout=300)
        d = r.json().get('data') or {}
        for k in ('created', 'updated', 'unchanged', 'failed'):
            sent[k] += d.get(k) or 0
        for res in (d.get('results') or []):
            if res.get('outcome') not in ('created', 'updated', 'unchanged'):
                print('  FAILED %s %s' % (res.get('courseId'), res.get('message')))
        print('   batch %d-%d: HTTP %s %s' % (i, i + len(chunk), r.status_code, dict(sent)))
    print('done:', dict(sent))
    return 0


if __name__ == '__main__':
    sys.exit(main())
