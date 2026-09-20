# -*- coding: utf-8 -*-
"""Send Florida's DISTRICT TECHNICAL COLLEGES and the AER automotive courses. Run from Tools/.

⚠⚠ THE FINDING BEHIND THIS SCRIPT. `scns.is_public()` answers SUS or FCS only, so district
technical colleges come back "other" and every tool in this repo has been filtering them out.
They are public institutions — district-operated career centres — and they are where Florida
actually teaches automotive, welding, HVAC and the rest of the CTE space: 40 of them carry the
AER automotive courses, against two state colleges. The site knew 39 institutions, all FCS or
SUS, and none of the technical colleges.

    python scratchpad/push_auto_data.py            # dry run
    python scratchpad/push_auto_data.py --push
"""
import sys, os, collections, json
sys.path.insert(0, 'scratchpad')
import scns, requests

try:
    from dotenv import load_dotenv
    load_dotenv('.env')
except ImportError:
    pass

FLAT = os.path.join('scratchpad', 'crslist.txt')
BASE = os.environ.get('REPO_BASE_URL', 'https://floridacourserepo.com').rstrip('/')

# The nine OCP courses of Master Automotive Service Technology (CIP 0647060405) plus the
# Maintenance and Light Repair framework (0647060422), from CPALMS-CTE.
WANT = ['AER0014', 'AER0110', 'AER0257', 'AER0274', 'AER0453', 'AER0418', 'AER0360',
        'AER0172', 'AER0503', 'AER0025', 'AER0027', 'AER0028']

SMALL = {'and', 'or', 'of', 'the', 'for', 'to', 'in', 'with', 'a', 'an', 'on', 'at'}
ACRONYMS = {'HVAC', 'CNG', 'LPG', 'EV', 'AC', 'I', 'II', 'III', 'IV'}


def _word(w, first_or_last):
    if w.upper() in ACRONYMS:
        return w.upper()
    if '.' in w and len(w) <= 5:          # dotted initials: D.A., H.B.
        return w.upper()
    if w.lower() in SMALL and not first_or_last:
        return w.lower()
    if w.upper().startswith('MC') and len(w) > 2:
        return 'Mc' + w[2:].capitalize()
    return w.capitalize()


def titlecase(s):
    ws = s.split()
    out = []
    for i, w in enumerate(ws):
        first_or_last = i in (0, len(ws) - 1)
        # ⚠ Capitalise after a hyphen too: "COLLEGE-ST PETERSBURG" is a campus name,
        # and "-st petersburg" reads as a typo on a page.
        out.append('-'.join(_word(part, first_or_last) for part in w.split('-')))
    return ' '.join(out)


def clean_name(raw):
    """"ATC - ATLANTIC TECHNICAL COLLEGE" -> ("ATC", "Atlantic Technical College")."""
    code, _, name = raw.partition('-')
    return code.strip(), titlecase(name.strip())


def cid_of(r):
    return (r['prefix'] + r['level'] + r['century'] + r['decade'] + r['unit'] + (r['lab'] or '')).strip().upper()


def build():
    imap = scns.institution_map()
    rows = collections.defaultdict(list)
    for r in scns.parse_flatfile(FLAT):
        if r['prefix'] != 'AER' or r['status'] != 'A':
            continue
        cid = cid_of(r)
        if cid in WANT:
            raw = imap.get(r['institution'].lstrip('0'))
            if raw:
                rows[cid].append((raw, (r.get('inst_title') or '').strip(),
                                  r.get('credit'), r.get('clock_hours')))

    institutions, courses = {}, []
    for cid in WANT:
        rs = rows.get(cid, [])
        if not rs:
            print('%-9s no active carrier -- skipped' % cid)
            continue
        titles = collections.Counter(t for _, t, _, _ in rs if t)
        hours = collections.Counter()
        offerings = []
        for raw, t, cr, ch in sorted(set(rs)):
            code, name = clean_name(raw)
            sector = scns.sector_of(code)
            if sector == 'other':
                # ⚠ Not private: these are district technical colleges, and "TECH" is the
                # sector this site did not have until now.
                if 'TECHNICAL' in raw.upper() or 'TECH ' in raw.upper() or raw.upper().endswith('TECH'):
                    sector = 'TECH'
                else:
                    continue          # genuinely out of scope (private or out of state)
            institutions[code] = {"code": code, "name": name, "sector": sector}
            o = {"institution": code, "title": t or None}
            try:
                o["clockHours"] = int(float(ch))
                hours[int(float(ch))] += 1
            except (TypeError, ValueError):
                pass
            try:
                o["credits"] = int(float(cr))
            except (TypeError, ValueError):
                o["credits"] = 0
            offerings.append(o)
        courses.append({
            "courseId": cid,
            "title": titlecase(titles.most_common(1)[0][0]),
            "stateTitle": titles.most_common(1)[0][0],
            # ⚠ PSAV clock-hour course: credits 0, the real measure is contact hours.
            "creditHours": 0,
            "contactHours": hours.most_common(1)[0][0] if hours else None,
            "offerings": offerings,
            "replaceOfferings": True,
        })
        print('%-9s %-48s %4s hrs, %2d carrier(s)'
              % (cid, courses[-1]['title'][:48], courses[-1]['contactHours'], len(offerings)))
    return institutions, courses


def main():
    push = '--push' in sys.argv
    institutions, courses = build()
    tech = [i for i in institutions.values() if i['sector'] == 'TECH']
    print('\n%d institution(s), %d of them district technical colleges; %d course(s)'
          % (len(institutions), len(tech), len(courses)))
    if not push:
        print('dry run -- pass --push')
        return 0

    # ⚠ Never overwrite an institution the site already carries: its name there was set
    # deliberately and the SCNS spelling is sometimes worse ("HILLSBOROUGH COLLEGE").
    known = set()
    try:
        d0 = requests.get('%s/api/v1/institutions' % BASE, timeout=60).json()['data']
        known = {i['code'] for i in (d0 if isinstance(d0, list) else d0.get('items', []))}
    except Exception as e:
        print('could not read existing institutions (%s) -- sending all' % str(e)[:60])
    new = [i for i in institutions.values() if i['code'] not in known]
    print('sending %d new institution(s); leaving %d existing ones alone'
          % (len(new), len(institutions) - len(new)))

    s = requests.Session()
    tok = s.post('%s/api/v1/auth/login' % BASE,
                 json={'email': os.environ['REPO_ADMIN_EMAIL'],
                       'password': os.environ['REPO_ADMIN_PASSWORD']}, timeout=20)
    tok.raise_for_status()
    h = {'Authorization': 'Bearer %s' % tok.json()['data']['accessToken']}

    r = s.post('%s/api/v1/institutions/batch' % BASE,
               json={'institutions': new}, headers=h, timeout=120)
    print('institutions HTTP', r.status_code, json.dumps(r.json().get('data'), ensure_ascii=False)[:300])

    r = s.post('%s/api/v1/courses/batch' % BASE, json={'courses': courses}, headers=h, timeout=180)
    d = r.json().get('data') or {}
    print('courses HTTP', r.status_code,
          {k: d.get(k) for k in ('created', 'updated', 'unchanged', 'failed')})
    for res in (d.get('results') or []):
        if res.get('outcome') not in ('created', 'updated', 'unchanged'):
            print('  FAILED', res)
    return 0


if __name__ == '__main__':
    sys.exit(main())
