# -*- coding: utf-8 -*-
"""Batch 253: send the base data (offerings) for the requested courses.

    python scratchpad/b253_base.py            # dry run
    python scratchpad/b253_base.py --push     (run from Tools/)

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

IDS = ['EDG7365', 'EDG7982']  # EDG1931 is a shell: declined, already listed
HOURS = {'EDG7365': 45, 'EDG7982': 45}
TITLES = {'EDG7365': 'Practitioner Research: Data Collection and Analysis',
          'EDG7982': 'Practitioner Research: Theory and Practice', 'EDG1931': 'Special Topics'}
if len(sys.argv) > 1 and sys.argv[1] not in ('--push',):
    IDS = [a for a in sys.argv[1:] if not a.startswith('--')]

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
