# -*- coding: utf-8 -*-
"""List courses a career path names but the catalog does not carry. Run from Tools/.

    python scratchpad/list_missing.py COP3530 CDA4102 ...        # dry run
    python scratchpad/list_missing.py --push COP3530 CDA4102 ...

Builds each course from the SCNS flat file: the modal institution title (title-cased),
the modal integer credit, and every PUBLIC carrier as an offering with its own title and
credits. ⚠ Public institutions only, per Ron's 2026-09-11 scope rule.
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

SMALL = {'and', 'or', 'of', 'the', 'for', 'to', 'in', 'with', 'a', 'an', 'on', 'at'}


# ⚠ An ALL-CAPS source carries no case signal, so an "is it upper?" acronym heuristic
# fires on every word. Use an explicit list instead, and keep it short.
ACRONYMS = {'VLSI', 'CPU', 'GPU', 'GIS', 'CAD', 'CAM', 'AI', 'HVAC', 'RF', 'DC', 'AC', 'IT',
            'II', 'III', 'IV', 'I', 'V', 'VI',
            # welding and metalwork processes -- they are initialisms, not words
            'SMAW', 'GMAW', 'FCAW', 'GTAW', 'GTA', 'MIG', 'TIG', 'CNC', 'NDT', 'EV', 'CNG', 'LPG',
            'HVAC', 'R', 'AC', 'EPA', 'ASE', 'OSHA', 'FAA', 'A&P', 'NEC', 'MSSC', 'CPT', 'PLC',
            # health professions -- credentials and modalities that are initialisms
            'PTA', 'OTA', 'RDH', 'MLS', 'MLT', 'RRT', 'CRT', 'EKG', 'ECG', 'EEG', 'IV', 'CPR',
            'ACLS', 'BLS', 'PALS', 'NRP', 'ABG', 'PT', 'OT', 'ADL', 'ROM', 'TENS', 'PPE',
            'EMT', 'EMR', 'AEMT', 'EMS', 'ALS', 'NREMT', 'CPAT', 'ARRT', 'NBRC'}


def _word(w, edge):
    # ⚠ Strip surrounding punctuation before the acronym test: the source writes
    # "(EMT)" and "(A&P)", and a bare `in ACRONYMS` misses them -> "(emt)".
    bare = w.strip('(),.:;/-').upper()
    if bare in ACRONYMS:
        return w.replace(bare.lower(), bare).replace(bare.capitalize(), bare) if bare.lower() in w.lower() else w.upper()
    if w.upper().strip(',') in ACRONYMS:
        return w.upper()
    if '.' in w and len(w) <= 5:
        return w.upper()
    if w.lower() in SMALL and not edge:
        return w.lower()
    if w.upper().startswith('MC') and len(w) > 2:
        return 'Mc' + w[2:].capitalize()
    return _cap(w)


def _cap(w):
    # ⚠ str.capitalize() uppercases the FIRST CHARACTER, so "(PROVISIONAL" becomes
    # "(provisional". Capitalise the first LETTER instead.
    for i, ch in enumerate(w):
        if ch.isalpha():
            return w[:i] + ch.upper() + w[i + 1:].lower()
    return w


def _part(w, edge):
    # ⚠ Split on the hyphen AND the slash: "GAS-METAL ARC" and "HVAC/R" are each
    # several tokens to a reader, and "Hvac/r" is how it looks when they are not.
    return '/'.join('-'.join(_word(q, edge) for q in p.split('-')) for p in w.split('/'))


def titlecase(s):
    ws = s.split()
    return ' '.join(_part(w, i in (0, len(ws) - 1)) for i, w in enumerate(ws))


def cid_of(r):
    return (r['prefix'] + r['level'] + r['century'] + r['decade'] + r['unit'] + (r['lab'] or '')).strip().upper()


def build(ids):
    imap = {k: v.split('-')[0].strip() for k, v in scns.institution_map().items()}
    rows = collections.defaultdict(list)
    for r in scns.parse_flatfile(FLAT):
        if r['status'] != 'A':
            continue
        c = cid_of(r)
        if c in ids:
            inst = imap.get(r['institution'].lstrip('0'))
            if inst and scns.is_public(inst):
                rows[c].append((inst, (r.get('inst_title') or '').strip(),
                                r.get('credit'), r.get('clock_hours')))

    courses = []
    for cid in ids:
        rs = rows.get(cid, [])
        if not rs:
            print('%-10s NO PUBLIC CARRIER -- not sending' % cid)
            continue
        titles = collections.Counter(t for _, t, _, _ in rs if t)
        creds, hours = collections.Counter(), collections.Counter()
        offerings = []
        for inst, t, cr, ch in sorted(set(rs)):
            o = {"institution": inst, "title": t or None}
            try:
                o["credits"] = int(float(cr)); creds[o["credits"]] += 1
            except (TypeError, ValueError):
                pass
            # ⚠ A PSAV course is measured in CLOCK HOURS, not credits, and the whole CTE
            # catalogue is PSAV. Dropping them publishes a course with no measure at all.
            try:
                o["clockHours"] = int(float(ch)); hours[o["clockHours"]] += 1
            except (TypeError, ValueError):
                pass
            offerings.append(o)
        courses.append({
            "courseId": cid,
            "title": titlecase(titles.most_common(1)[0][0]),
            "stateTitle": titles.most_common(1)[0][0],
            "creditHours": creds.most_common(1)[0][0] if creds else 0,
            "contactHours": hours.most_common(1)[0][0] if hours else None,
            "offerings": offerings,
            "replaceOfferings": True,
        })
        print('%-10s %-44s %s cr / %s hrs, %d carrier(s)'
              % (cid, courses[-1]['title'][:44], courses[-1]['creditHours'],
                 courses[-1]['contactHours'], len(offerings)))
    return courses


def main():
    args = sys.argv[1:]
    push = '--push' in args
    ids = [a.upper() for a in args if not a.startswith('--')]
    courses = build(set(ids))
    if not push:
        print('\ndry run -- pass --push to send %d course(s) to %s' % (len(courses), BASE))
        return 0

    s = requests.Session()
    tok = s.post('%s/api/v1/auth/login' % BASE,
                 json={'email': os.environ['REPO_ADMIN_EMAIL'],
                       'password': os.environ['REPO_ADMIN_PASSWORD']}, timeout=20)
    tok.raise_for_status()
    h = {'Authorization': 'Bearer %s' % tok.json()['data']['accessToken']}
    # ⚠ The server refuses a batch over 500 (BATCH_TOO_LARGE) and rejects the WHOLE thing,
    # so chunk here rather than making the caller remember. Hit on PHT, 601 courses, 2026-09-21.
    CHUNK = 500
    rc, total = 0, {'created': 0, 'updated': 0, 'unchanged': 0, 'failed': 0}
    for i in range(0, len(courses), CHUNK):
        part = courses[i:i + CHUNK]
        r = s.post('%s/api/v1/courses/batch' % BASE, json={'courses': part}, headers=h, timeout=300)
        print('HTTP %s  (courses %d-%d of %d)' % (r.status_code, i + 1, i + len(part), len(courses)))
        body = r.json()
        if r.status_code == 200 and body.get('success'):
            for k in total:
                total[k] += body['data'].get(k, 0)
            for res in body['data'].get('results', []):
                if res.get('outcome') == 'failed':
                    print('  FAILED %s: %s' % (res['courseId'], res.get('message')))
        else:
            rc = 1
            print(json.dumps(body, ensure_ascii=False)[:800])
    print(json.dumps(total))
    return rc


if __name__ == '__main__':
    sys.exit(main())
