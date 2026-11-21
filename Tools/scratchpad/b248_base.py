# -*- coding: utf-8 -*-
"""Batch 248: send the base data (offerings) for the ten requested courses.

    python scratchpad/b248_base.py            # dry run
    python scratchpad/b248_base.py --push     (run from Tools/)

Builds each course with list_missing.build() (SCNS flat file, public carriers only); stateTitle from the
flat file's state_title, and contactHours from the guides (EEL4242C 60, the others 45; none for the held or
declined numbers).
"""
import io
import json
import os
import sys

sys.path.insert(0, 'scratchpad')
import scns

scns.institution_map = lambda o=None: json.load(io.open(os.path.join('scratchpad', 'inst_map.json'),
                                                        encoding='utf-8'))
import list_missing as lm  # noqa: E402

IDS = ['EEL4242C', 'EEL4242', 'EEL4243', 'EEL4448', 'EEL4611', 'EEL4610', 'EEL5025', 'EEL5009', 'EEL1603',
       'EEL1906']
HOURS = {'EEL4242C': 60, 'EEL4242': 45, 'EEL4243': 45, 'EEL4611': 45, 'EEL4610': 45, 'EEL1603': 45}

state = {}
for r in scns.parse_flatfile(lm.FLAT):
    c = lm.cid_of(r)
    if c in IDS and r.get('state_title'):
        st = r['state_title'].strip()
        for tag in ('(U)', '(G)', '(L)'):
            if st.endswith(tag):
                st = st[:-len(tag)].strip()
        state[c] = st

courses = lm.build(set(IDS))
for c in courses:
    cid = c['courseId']
    if cid in state:
        c['stateTitle'] = state[cid]
    if cid in HOURS:
        c['contactHours'] = HOURS[cid]
    print('%-9s %-45s state=%-42s cr %s hrs %s %s' % (cid, c['title'][:45], c.get('stateTitle'), c['creditHours'],
                                                    c['contactHours'], [o['institution'] for o in c['offerings']]))

if '--push' not in sys.argv:
    print('dry run')
    sys.exit(0)

s = lm.requests.Session()
tok = s.post('%s/api/v1/auth/login' % lm.BASE, json={'email': os.environ['REPO_ADMIN_EMAIL'],
                                                     'password': os.environ['REPO_ADMIN_PASSWORD']}, timeout=20)
tok.raise_for_status()
h = {'Authorization': 'Bearer %s' % tok.json()['data']['accessToken']}
r = s.post('%s/api/v1/courses/batch' % lm.BASE, json={'courses': courses}, headers=h, timeout=120)
body = r.json()
print('HTTP', r.status_code, json.dumps({k: body.get('data', {}).get(k) for k in
                                         ('created', 'updated', 'unchanged', 'failed')}))
for res in (body.get('data') or {}).get('results', []):
    if res.get('outcome') == 'failed':
        print('  FAILED', res['courseId'], res.get('message'))
