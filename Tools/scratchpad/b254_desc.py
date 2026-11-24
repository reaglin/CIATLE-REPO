# -*- coding: utf-8 -*-
"""Batch 254: print description, prerequisites, credits and outcomes of cached catalogue rows (run from Tools/)."""
import io
import json
import sys

IDS = set(sys.argv[1:])
for name, path in (('fiu', 'fiu_courses.json'), ('fau', 'fau_courses.json'), ('ucf', 'ucf_courses.json'),
                   ('fsu', 'fsu_courses.json')):
    data = json.load(io.open('scratchpad/' + path, encoding='utf-8'))
    rows = data if isinstance(data, list) else (data.get('data') or data.get('courses') or list(data.values()))
    for row in rows:
        if not isinstance(row, dict) or row.get('code') not in IDS:
            continue
        cf = row.get('customFields') or {}
        print('==', name, row.get('code'), row.get('longName') or row.get('name') or cf.get('_effectiveLongTitle'),
              '| eff', row.get('effectiveStartDate'), 'end', row.get('effectiveEndDate'),
              '| status', row.get('status'), '| cr', (row.get('credits') or {}).get('creditHours'))
        print('  desc:', (row.get('description') or '')[:1200])
        for k in ('requisites', 'prerequisites', 'requirementGroup'):
            if row.get(k):
                print('  ', k, json.dumps(row.get(k), ensure_ascii=False)[:800])
        for k, v in cf.items():
            if isinstance(v, str) and len(v) > 25 and not v.startswith('<p>This Course Inactivation'):
                print('   cf', k, ':', v[:900].replace('\n', ' '))
