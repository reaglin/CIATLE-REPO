# -*- coding: utf-8 -*-
"""Batch 251: send the base data (offerings) for the six requested courses.

    python scratchpad/b251_base.py            # dry run
    python scratchpad/b251_base.py --push     (run from Tools/)

Built with list_missing.build() (SCNS flat file, public carriers only); stateTitle from the flat file, and
contactHours from the guides. Titles are the institutions' own.
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

IDS = ['COM3120', 'COM5235', 'ATR2000', 'ATR5105C', 'ATR5305C', 'BME4311']
HOURS = {'COM3120': 45, 'COM5235': 45, 'ATR2000': 45, 'ATR5105C': 60, 'ATR5305C': 75, 'BME4311': 45}
TITLES = {'COM3120': 'Organizational Communication', 'COM5235': 'Crisis Communication',
          'ATR2000': 'Basic Care and Prevention Principles of Athletic Training',
          'ATR5105C': 'Foundations in Athletic Training',
          'ATR5305C': 'Therapeutic Interventions in Athletic Training I', 'BME4311': 'Molecular Engineering'}
if '--acg' in sys.argv:  # the four requests that arrived during the run
    IDS = ['ACG2001', 'ACG2011', 'ACG2071', 'ACG2100']
    HOURS = {c: 45 for c in IDS}
    TITLES = {'ACG2001': 'Principles of Accounting I', 'ACG2011': 'Principles of Accounting II',
              'ACG2071': 'Managerial Accounting', 'ACG2100': 'Intermediate Accounting I'}

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
    seen, uniq = set(), []  # honors sections give one institution two rows; keep the first (standard) one
    for o in c['offerings']:
        if o['institution'] not in seen:
            seen.add(o['institution'])
            uniq.append(o)
    c['offerings'] = uniq
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
