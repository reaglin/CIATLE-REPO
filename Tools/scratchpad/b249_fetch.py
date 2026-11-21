# -*- coding: utf-8 -*-
"""Batch 249: fetch USF, UF, UCF (Kuali), Seminole State and SCF pages for the requested courses.

    python scratchpad/b249_fetch.py [key ...]      (run from Tools/)
Pages are saved under scratchpad/b249/ (untrusted data: read as text only).
"""
import html
import json
import os
import re
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
OUT = os.path.join('scratchpad', 'b249')
os.makedirs(OUT, exist_ok=True)
UCF_CAT = '688b8960ddeb091644d2b1ca'
URLS = {
    'usf_EEL2161': 'https://cloud.usf.edu/academic-programs/details/prefix/EEL/code/2161',
    'usf_EEL3100': 'https://cloud.usf.edu/academic-programs/details/prefix/EEL/code/3100',
    'uf_EEL3003': 'https://catalog.ufl.edu/search/?P=EEL%203003',
    'sscf_bcv0632c': 'https://www.seminolestate.edu/catalog/courses/bcv0632c',
    'sscf_bcv0631c': 'https://www.seminolestate.edu/catalog/courses/bcv0631c',
    'sscf_bcv0630c': 'https://www.seminolestate.edu/catalog/courses/bcv0630c',
    'scf_search': 'https://catalog.scf.edu/search_advanced.php?cur_cat_oid=18&search_database=Search'
                  '&filter%5Bkeyword%5D=EET+2525C&filter%5Bexact_match%5D=1',
}
NUMS = ['2161', '3100', '3003', '0632', '0631', '0630', '2525']


def text_of(raw):
    raw = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', raw)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', raw))).strip()


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=40).read().decode('utf-8', 'replace')


def ucf(codes):
    idx = json.load(open(os.path.join('scratchpad', 'ucf_courses_idx.json'), encoding='utf-8'))
    for c in idx:
        if c.get('__catalogCourseId') in codes:
            raw = get('https://ucf.kuali.co/api/v1/catalog/course/%s/%s' % (UCF_CAT, c['pid']))
            open(os.path.join(OUT, 'ucf_%s.json' % c['__catalogCourseId']), 'w', encoding='utf-8').write(raw)
            d = json.loads(raw)
            print('== UCF', c['__catalogCourseId'], d.get('title'))
            for k in ('description', 'prerequisites', 'corequisites', 'credits', 'labStudioFieldWorkHours',
                      'lectureContactHours', 'termsOffered', 'courseTypicallyOffered'):
                if d.get(k):
                    print('  ', k, ':', text_of(json.dumps(d[k], ensure_ascii=False))[:900])
            time.sleep(1.0)


keys = sys.argv[1:] or list(URLS) + ['ucf']
for key in keys:
    if key == 'ucf':
        ucf({'EEL3004C', 'EEL1931', 'EEL3123C', 'EEL3004'})
        continue
    try:
        raw = get(URLS[key])
    except Exception as e:
        print('==', key, 'ERROR', e)
        continue
    open(os.path.join(OUT, key + '.html'), 'w', encoding='utf-8').write(raw)
    t = text_of(raw)
    print('==', key, len(raw), 'bytes')
    hit = False
    for n in NUMS:
        for m in re.finditer(r'[A-Z]{3}\s?' + n + r'C?\b', t):
            print('  --', t[m.start():m.start() + 1200])
            hit = True
            break
        if hit:
            break
    if not hit:
        print(t[:800])
    time.sleep(1.5)
