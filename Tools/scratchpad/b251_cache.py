# -*- coding: utf-8 -*-
"""Batch 251: look up the requested courses in the cached Coursedog catalogues (FIU, FAU). Run from Tools/.

    python scratchpad/b251_cache.py COM3120 BME4311 ...
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
want = [a.upper() for a in sys.argv[1:]]
for name in ('fiu_courses.json', 'fau_courses.json'):
    data = json.load(open(os.path.join('scratchpad', name), encoding='utf-8'))
    rows = data if isinstance(data, list) else list(data.values())
    for c in rows:
        cid = (str(c.get('subjectCode', '')) + str(c.get('courseNumber', ''))).upper().replace(' ', '')
        if cid in want or (c.get('code') or '').upper().replace(' ', '') in want:
            keep = {k: v for k, v in c.items() if k in ('code', 'subjectCode', 'courseNumber', 'name', 'longName',
                                                         'description', 'credits', 'requisites', 'status',
                                                         'effectiveStartDate', 'effectiveEndDate')}
            s = json.dumps(keep, ensure_ascii=False)
            print('==', name, cid, re.sub(r'\s+', ' ', s)[:2500])
