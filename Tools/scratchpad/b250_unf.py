# -*- coding: utf-8 -*-
"""Batch 250: UNF's catalogue course API (found behind www.unf.edu/catalog/courses/, course-API-data.js).

    python scratchpad/b250_unf.py EML4328C ETS4543C      (run from Tools/)
Saves the whole year's list to scratchpad/unf_courses_2026-2027.json (untrusted data: read as text only).
"""
import json
import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
YEAR = '2026-2027'
CACHE = os.path.join('scratchpad', 'unf_courses_%s.json' % YEAR)
if not os.path.exists(CACHE):
    url = 'https://webappsapi.unf.edu/cascade/api/v1/catalog/GetCourses/course?year=%s' % YEAR
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    raw = urllib.request.urlopen(req, timeout=90).read().decode('utf-8', 'replace')
    open(CACHE, 'w', encoding='utf-8').write(raw)
courses = json.load(open(CACHE, encoding='utf-8'))
print('courses:', len(courses), 'keys:', sorted(courses[0].keys()) if courses else None)
want = [a.upper().replace(' ', '') for a in sys.argv[1:]]
for c in courses:
    blob = json.dumps(c, ensure_ascii=False)
    flat = blob.upper().replace(' ', '')
    if any(w in flat for w in want):
        print(json.dumps(c, ensure_ascii=False, indent=1)[:3000])
