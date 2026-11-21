# -*- coding: utf-8 -*-
"""Batch 250: send the base data (offerings) for the seven requested courses.

    python scratchpad/b250_base.py            # dry run
    python scratchpad/b250_base.py --push     (run from Tools/)

Built with list_missing.build() (SCNS flat file, public carriers only); stateTitle from the flat file, and
contactHours from the guides (none for the held ETS3543L). Titles are the institutions' own.
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

IDS = ['EML4328C', 'ETS1542', 'ETS2542', 'ETS2544', 'ETS4543C', 'ETS3543L', 'ECH3702']
HOURS = {'EML4328C': 60, 'ETS1542': 45, 'ETS2542': 45, 'ETS2544': 45, 'ETS4543C': 60, 'ECH3702': 45}
TITLES = {'ECH3702': 'Instrument Systems I', 'EML4328C': 'Applied Programmable Logic Controllers for ME',
          'ETS1542': 'Introduction to Programmable Logic Controllers', 'ETS2542': 'Programmable Logic Controllers I',
          'ETS2544': 'Programmable Logic Controllers II', 'ETS4543C': 'Applied Programmable Logic Controllers',
          'ETS3543L': 'Introduction to Programmable Logic Controllers Lab'}

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
    if cid in TITLES:
        c['title'] = TITLES[cid]
    print('%-9s %-45s state=%-40s cr %s hrs %s %s' % (cid, c['title'][:45], c.get('stateTitle'), c['creditHours'],
                                                    c['contactHours'], [(o['institution'], o.get('credits'))
                                                                        for o in c['offerings']]))

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
