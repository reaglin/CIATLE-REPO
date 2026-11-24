# -*- coding: utf-8 -*-
"""Batch 254: USF (cloud.usf.edu), UF search page and UCF Kuali for the requested STA courses (run from Tools/).

Pages are saved under scratchpad/b254_dl/ (untrusted data: read as text only).
"""
import html
import json
import os
import re
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
OUT = os.path.join('scratchpad', 'b254_dl')
os.makedirs(OUT, exist_ok=True)
UCF_CAT = '688b8960ddeb091644d2b1ca'
URLS = {
    'usf_STA2122': 'https://cloud.usf.edu/academic-programs/details/prefix/STA/code/2122',
    'usf_STA3024': 'https://cloud.usf.edu/academic-programs/details/prefix/STA/code/3024',
    'uf_STA3024': 'https://catalog.ufl.edu/search/?P=STA%203024',
}


def text_of(raw):
    raw = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', raw)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', raw))).strip()


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=40).read().decode('utf-8', 'replace')


idx = json.load(open(os.path.join('scratchpad', 'ucf_courses_idx.json'), encoding='utf-8'))
for c in idx:
    if c.get('__catalogCourseId') in ('STA2360', 'STA2023'):
        raw = get('https://ucf.kuali.co/api/v1/catalog/course/%s/%s' % (UCF_CAT, c['pid']))
        open(os.path.join(OUT, 'ucf_%s.json' % c['__catalogCourseId']), 'w', encoding='utf-8').write(raw)
        d = json.loads(raw)
        print('== UCF', c['__catalogCourseId'], d.get('title'))
        for k in ('description', 'prerequisites', 'corequisites', 'credits', 'lectureContactHours',
                  'termsOffered', 'courseTypicallyOffered'):
            if d.get(k):
                print('  ', k, ':', text_of(json.dumps(d[k], ensure_ascii=False))[:900])
        time.sleep(1.0)

for key, url in URLS.items():
    try:
        raw = get(url)
    except Exception as e:  # noqa: BLE001
        print('==', key, 'ERROR', e)
        continue
    open(os.path.join(OUT, key + '.html'), 'w', encoding='utf-8').write(raw)
    t = text_of(raw)
    print('==', key, len(raw), 'bytes')
    num = key[-4:]
    m = re.search(r'STA\s?' + num, t)
    print('  --', t[m.start():m.start() + 1500] if m else t[:1000])
    time.sleep(1.5)
