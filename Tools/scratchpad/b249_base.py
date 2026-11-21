# -*- coding: utf-8 -*-
"""Batch 249: send the base data (offerings) for the ten requested courses.

    python scratchpad/b249_base.py            # dry run
    python scratchpad/b249_base.py --push     (run from Tools/)

Builds each course with list_missing.build() (SCNS flat file, public carriers only); stateTitle from the
flat file's state_title, and contactHours from the guides (none for the held or declined numbers).
⚠ EEL2603C, EEL2880 and EET2525C carry SCNS statewide titles for other courses; the title sent is the
institution's own (list_missing's modal title).
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

IDS = ['EEL1931', 'EEL2161', 'EEL2603C', 'EEL2880', 'EEL3000', 'EEL3003', 'EEL3004C', 'EEL3100', 'BCV0632C',
       'EET2525C']
HOURS = {'EEL2161': 45, 'EEL2603C': 60, 'EEL2880': 45, 'EEL3000': 30, 'EEL3003': 45, 'EEL3004C': 60,
         'EEL3100': 45, 'BCV0632C': 150}

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
    # UCF files Linear Circuits I and its Honors section under one number: one offering per institution.
    seen, uniq = set(), []
    for o in c['offerings']:
        if o['institution'] not in seen:
            seen.add(o['institution'])
            uniq.append(o)
    c['offerings'] = uniq
    if cid == 'BCV0632C':
        c['title'] = 'Residential Electrician III'
    print('%-9s %-45s state=%-42s cr %s hrs %s %s' % (cid, c['title'][:45], c.get('stateTitle'), c['creditHours'],
                                                    c['contactHours'], [(o['institution'], o.get('credits'),
                                                                         o.get('clockHours'))
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
