# -*- coding: utf-8 -*-
"""Batch 255: confirm the guides are live and count the waiting requests (run from Tools/)."""
import requests

BASE = 'https://floridacourserepo.com/api/v1'
for c in ('CJE2540', 'HUN2202', 'HFT1102'):
    d = requests.get('%s/courses/%s/guide' % (BASE, c), timeout=30).json()
    g = d.get('data') or {}
    print(c, d.get('success'), g.get('title'), g.get('credits'), g.get('contactHours'), len(g.get('htmlContent') or ''))
q = requests.get('%s/queue/guides?status=waiting' % BASE, timeout=30).json()
items = (q.get('data') or {}).get('items') if isinstance(q.get('data'), dict) else q.get('data')
print('waiting:', len(items or []), [(i.get('courseId'), i.get('status')) for i in (items or [])])
