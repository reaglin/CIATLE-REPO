# -*- coding: utf-8 -*-
"""Batch 247: send the base data (offerings) for the requested courses, with two title fixes.

    python scratchpad/b247_base.py            # dry run
    python scratchpad/b247_base.py --push     (run from Tools/)

Builds each course with list_missing.build() (SCNS flat file, public carriers only), then:
  EEL4212   title -> the statewide "Distributed Energy Delivery Systems" (two carriers, two subjects;
            the modal-title rule would pick FIU's "High Voltage Engineering")
  EEL4213L  title -> "Energy Conversion Lab" (FIU's own title; the state file misspells "Convergance")
  stateTitle is set from the flat file's state_title, and contactHours from the guides.
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

IDS = ['EEL4119L', 'EEL4113', 'EEL4206L', 'EEL4210', 'EEL4212', 'EEL4213L', 'EEL4214', 'EEL4215',
       'EEL4217L', 'EEE4351', 'EEL4081', 'PET1170']
TITLES = {'EEL4212': 'Distributed Energy Delivery Systems', 'EEL4213L': 'Energy Conversion Lab'}
HOURS = {'EEL4119L': 45, 'EEL4113': 45, 'EEL4206L': 45, 'EEL4210': 45, 'EEL4212': 45, 'EEL4213L': 45,
         'EEL4214': 45, 'EEL4215': 45, 'EEL4217L': 45, 'EEE4351': 45}

state = {}
for r in scns.parse_flatfile(lm.FLAT):
    c = lm.cid_of(r)
    if c in IDS and r.get('state_title'):
        st = r['state_title'].strip()
        state[c] = st[:-4].strip() if st.endswith('(U)') else st

courses = lm.build(set(IDS))
for c in courses:
    cid = c['courseId']
    if cid in TITLES:
        c['title'] = TITLES[cid]
    if cid in state:
        c['stateTitle'] = state[cid]
    if cid in HOURS:
        c['contactHours'] = HOURS[cid]
    print('%-9s %-40s state=%-42s cr %s hrs %s %s' % (cid, c['title'], c.get('stateTitle'), c['creditHours'],
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
