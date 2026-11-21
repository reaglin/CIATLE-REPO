# -*- coding: utf-8 -*-
"""Batch 249: confirm each guide is live and count the requests still waiting. Run from Tools/."""
import json
import sys
import urllib.request

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
BASE = 'https://floridacourserepo.com/api/v1'
IDS = ['EEL2161', 'EEL2603C', 'EEL2880', 'EEL3000', 'EEL3003', 'EEL3004C', 'EEL3100', 'BCV0632C']


def get(path):
    return json.loads(urllib.request.urlopen(BASE + path, timeout=30).read().decode('utf-8'))


for cid in IDS:
    d = get('/courses/%s/guide' % cid).get('data') or {}
    print('%-9s %-60s cr %s hrs %s v%s html %d' % (cid, (d.get('title') or '')[:60], d.get('credits'),
                                                   d.get('contactHours'), d.get('version'),
                                                   len(d.get('htmlContent') or '')))
w = get('/queue/guides?status=waiting')['data']
items = w if isinstance(w, list) else w.get('items', [])
print('waiting', len(items), [i['courseId'] for i in items])
