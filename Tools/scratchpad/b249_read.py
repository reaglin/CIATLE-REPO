# -*- coding: utf-8 -*-
"""Batch 249: print the relevant text from the saved pages in scratchpad/b249/ (run from Tools/)."""
import html
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
D = os.path.join('scratchpad', 'b249')


def text(raw):
    raw = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', raw)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', raw)))


def page(name):
    return text(open(os.path.join(D, name), encoding='utf-8').read())


t = page('uf_EEL3003.html')
for m in re.finditer('EEL 3003', t):
    print('UF>', t[max(0, m.start() - 300):m.start() + 300])
    print()

for k, code in (('sscf_bcv0632c.html', 'BCV0632C'), ('sscf_bcv0631c.html', 'BCV0631C')):
    t = page(k)
    hits = [m.start() for m in re.finditer(code, t)]
    print(k, len(hits), 'hits')
    if hits:
        s = hits[-1]
        print(t[s - 200:s + 1800])
    print()

for c in ('EEL3004C', 'EEL1931'):
    p = os.path.join(D, 'ucf_%s.json' % c)
    if not os.path.exists(p):
        continue
    d = json.load(open(p, encoding='utf-8'))
    print(c, 'keys:', sorted(d.keys()))
    for k in ('prerequisites', 'corequisites', 'termsOffered', 'lectureContactHours', 'labStudioFieldWorkHours',
              'description', 'title'):
        if k in d:
            print('  ', k, ':', text(json.dumps(d[k], ensure_ascii=False))[:2500])
