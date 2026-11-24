# -*- coding: utf-8 -*-
"""Batch 254: fetch UWF's STA PDF and query UF's course search for the requested courses (run from Tools/).

Downloads go to scratchpad/b254_dl/ (data only; nothing there is executed).
"""
import io
import os
import re

import pypdf
import requests

OUT = os.path.join('scratchpad', 'b254_dl')
os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (course-guide research)'}

# UF course search API (title + existence only)
for code in ('STA 3024', 'STA 2122', 'STA 3123', 'STA 2360'):
    try:
        r = requests.post('https://catalog.ufl.edu/course-search/api/?page=fose&route=search',
                          json={'other': {'srcdb': ''}, 'criteria': [{'field': 'keyword', 'value': code}]},
                          headers=UA, timeout=30)
        res = [(x.get('code'), x.get('title')) for x in r.json().get('results', []) if x.get('code') == code]
        print('UF', code, res)
    except Exception as e:  # noqa: BLE001
        print('UF', code, 'ERR', e)

# UWF prefix PDF
p = os.path.join(OUT, 'uwf_sta.pdf')
r = requests.get('https://catalog.uwf.edu/courseinformation/courses/sta/sta.pdf', headers=UA, timeout=60)
print('UWF pdf', r.status_code, len(r.content))
open(p, 'wb').write(r.content)
t = '\n'.join(pg.extract_text() or '' for pg in pypdf.PdfReader(p).pages)
for code in ('STA 2360', 'STA 2023', 'STA 3024', 'STA 2122', 'STA 3123'):
    for m in re.finditer(re.escape(code), t):
        print('---- UWF', code)
        print(t[m.start():m.start() + 1100])
        break

# Gulf Coast STA page
r = requests.get('https://www.gulfcoast.edu/catalog/current/courses/sta/index.html', headers=UA, timeout=60)
txt = re.sub(r'<[^>]+>', ' ', r.text)
txt = re.sub(r'\s+', ' ', txt)
print('GCSC', r.status_code)
for code in ('STA2122', 'STA 2122', 'STA2023', 'STA 2023'):
    i = txt.find(code)
    if i >= 0:
        print('---- GCSC', code)
        print(txt[i:i + 1200])
