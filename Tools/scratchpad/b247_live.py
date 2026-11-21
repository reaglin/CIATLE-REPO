# -*- coding: utf-8 -*-
"""Batch 247: show the live course record (title, credits, offerings) and whether a guide is live.

    python scratchpad/b247_live.py EEL4113 ...      (run from Tools/)
"""
import sys
import requests

BASE = 'https://floridacourserepo.com/api/v1/courses/'
for cid in sys.argv[1:]:
    d = requests.get(BASE + cid, timeout=30).json().get('data') or {}
    offs = d.get('offerings') or []
    g = requests.get(BASE + cid + '/guide', timeout=30)
    gd = (g.json().get('data') or {}) if g.ok else {}
    print('%-9s | %-45s | cr %s | offerings %d %s | guide %s v%s %s' % (
        cid, (d.get('title') or '')[:45], d.get('creditHours'), len(offs),
        [o.get('institution') for o in offs], g.status_code, gd.get('version'),
        (gd.get('title') or '')[:40]))
