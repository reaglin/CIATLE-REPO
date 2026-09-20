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
            'II', 'III', 'IV', 'I', 'V', 'VI'}


def titlecase(s):
    words = s.split()
    out = []
    for i, w in enumerate(words):
        low = w.lower()
        if w.upper() in ACRONYMS:
            out.append(w.upper())
        elif low in SMALL and i not in (0, len(words) - 1):
            out.append(low)
        else:
            out.append(w.capitalize())
    return ' '.join(out)


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
                rows[c].append((inst, (r.get('inst_title') or '').strip(), r.get('credit')))

    courses = []
    for cid in ids:
        rs = rows.get(cid, [])
        if not rs:
            print('%-10s NO PUBLIC CARRIER -- not sending' % cid)
            continue
        titles = collections.Counter(t for _, t, _ in rs if t)
        creds = collections.Counter()
        for _, _, cr in rs:
            try:
                creds[int(float(cr))] += 1
            except (TypeError, ValueError):
                pass
        offerings = []
        for inst, t, cr in sorted(set(rs)):
            o = {"institution": inst, "title": t or None}
            try:
                o["credits"] = int(float(cr))
            except (TypeError, ValueError):
                pass
            offerings.append(o)
        courses.append({
            "courseId": cid,
            "title": titlecase(titles.most_common(1)[0][0]),
            "stateTitle": titles.most_common(1)[0][0],
            "creditHours": creds.most_common(1)[0][0] if creds else None,
            "offerings": offerings,
            "replaceOfferings": True,
        })
        print('%-10s %-44s %d cr, %d carrier(s): %s'
              % (cid, courses[-1]['title'][:44], courses[-1]['creditHours'] or 0,
                 len(offerings), ' '.join(o['institution'] for o in offerings)))
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
    r = s.post('%s/api/v1/courses/batch' % BASE, json={'courses': courses}, headers=h, timeout=120)
    print('HTTP', r.status_code)
    print(json.dumps(r.json(), ensure_ascii=False)[:1500])
    return 0 if r.status_code == 200 else 1


if __name__ == '__main__':
    sys.exit(main())
