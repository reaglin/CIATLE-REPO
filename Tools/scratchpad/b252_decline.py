# -*- coding: utf-8 -*-
"""Batch 252: decline the shell-number guide requests with a public reason. Run from Tools/."""
import os
import sys

sys.path.insert(0, 'scratchpad')
import list_missing as lm  # noqa: E402  (loads .env, gives BASE and requests)

DECLINE = {
    'ACG4940': ('ACG4940 is an accounting internship number (FGCU, FIU and USF at 3 credits, Chipola at 1 to 6): '
                'the work is set by the employer and the placement, so each student\'s internship is different and '
                'there is no common course for a curriculum guide to describe. The course stays listed on the site.'),
    'CGS4955': ('CGS4955 is a study abroad number (UCF, variable credit): what is studied depends on the programme '
                'and the host institution each term, so there is no common course for a curriculum guide to '
                'describe. The course stays listed on the site.'),
}

s = lm.requests.Session()
tok = s.post('%s/api/v1/auth/login' % lm.BASE, json={'email': os.environ['REPO_ADMIN_EMAIL'],
                                                     'password': os.environ['REPO_ADMIN_PASSWORD']}, timeout=20)
tok.raise_for_status()
h = {'Authorization': 'Bearer %s' % tok.json()['data']['accessToken']}
for cid, why in DECLINE.items():
    r = s.patch('%s/api/v1/guide-requests/%s/status' % (lm.BASE, cid), json={'status': 'Declined', 'notes': why},
                headers=h, timeout=20)
    print(cid, r.status_code, r.text[:200])
