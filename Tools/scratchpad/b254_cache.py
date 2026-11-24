# -*- coding: utf-8 -*-
"""Batch 254: find the requested courses in the cached catalogues (run from Tools/)."""
import io
import json
import re
import sys

IDS = sys.argv[1:]
pats = [re.compile(r'\b%s\s*%s\b' % (i[:3], i[3:]), re.I) for i in IDS]
for name in ('fiu', 'fau', 'ucf', 'fsu', 'nwfsc', 'fscj', 'unf'):
    path = 'scratchpad/%s_courses.json' % name if name != 'unf' else 'scratchpad/unf_courses_2026-2027.json'
    try:
        data = json.load(io.open(path, encoding='utf-8'))
    except Exception as e:  # noqa: BLE001
        print(name, 'unreadable', e)
        continue
    rows = data if isinstance(data, list) else (data.get('data') or data.get('courses') or list(data.values()))
    for row in rows:
        s = json.dumps(row, ensure_ascii=False)
        for i, p in zip(IDS, pats):
            code = ''
            if isinstance(row, dict):
                code = (str(row.get('code') or row.get('courseNumber') or row.get('id') or '') + ' ' +
                        str(row.get('subjectCode') or '') + str(row.get('courseNumber') or ''))
            if p.search(code.replace(' ', ' ')) or (not code.strip() and p.search(s[:80])):
                print('==', name, i)
                print(s[:2500])
