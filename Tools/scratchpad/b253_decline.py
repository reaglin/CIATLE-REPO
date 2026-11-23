# -*- coding: utf-8 -*-
"""Batch 253: decline the shell-number guide request with a public reason. Run from Tools/."""
import os
import sys

sys.path.insert(0, 'scratchpad')
import list_missing as lm  # noqa: E402  (loads .env, gives BASE and requests)

DECLINE = {
    'EDG1931': ('EDG1931 is a special topics number (UCF, variable credit; statewide title Special Topics/Seminars): '
                'the subject changes from term to term and section to section, so there is no common course for a '
                'curriculum guide to describe. The course stays listed on the site.'),
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
