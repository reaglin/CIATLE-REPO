# -*- coding: utf-8 -*-
"""Batch 251: fetch catalogue pages for the six requested courses.

    python scratchpad/b251_fetch.py [key ...]      (run from Tools/)
Pages are saved under scratchpad/b251/ (untrusted data: read as text only).
"""
import html
import os
import re
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
OUT = os.path.join('scratchpad', 'b251')
os.makedirs(OUT, exist_ok=True)
USF = 'https://cloud.usf.edu/academic-programs/details/prefix/%s/code/%s'
URLS = {
    'uf_COM3120': 'https://catalog.ufl.edu/search/?P=COM%203120',
    'uf_BME4311': 'https://catalog.ufl.edu/search/?P=BME%204311',
    'usf_COM3120': USF % ('COM', '3120'),
    'usf_ATR5105C': USF % ('ATR', '5105C'),
    'uwf_ATR2000': 'https://catalog.uwf.edu/search/?P=ATR%202000',
    'uwf_ATR5105C': 'https://catalog.uwf.edu/search/?P=ATR%205105C',
    'fsu_comm_ug': 'https://registrar.fsu.edu/bulletin/undergraduate-departments/communication',
    'fsu_comm_gr': 'https://registrar.fsu.edu/bulletin/graduate-departments/communication',
    'fsu_new_root': 'https://bulletin.fsu.edu/',
    'fsu_new_5235': 'https://bulletin.fsu.edu/search/?P=COM%205235',
    'fsu_new_3120': 'https://bulletin.fsu.edu/search/?P=COM%203120',
    'fsu_ribbit_5235': 'https://bulletin.fsu.edu/ribbit/?page=getcourse.rjs&code=COM%205235',
    'fsu_ribbit_3120': 'https://bulletin.fsu.edu/ribbit/?page=getcourse.rjs&code=COM%203120',
    'fsu_courses_com': 'https://bulletin.fsu.edu/courses/com/',
    'uf_ACG2071': 'https://catalog.ufl.edu/search/?P=ACG%202071',
    'uf_ACG3101': 'https://catalog.ufl.edu/search/?P=ACG%203101',
    'usf_ACG2071': USF % ('ACG', '2071'),
    'usf_ACG3103': USF % ('ACG', '3103'),
    'sscf_acg2100': 'https://www.seminolestate.edu/catalog/courses/acg2100',
    'phsc_acg2100': 'https://phsc.smartcatalogiq.com/en/2026-2027/catalog-and-student-handbook/courses/'
                    'acg-accounting-general/2000/acg-2100',
    'irsc_acg2100': 'https://irsc.smartcatalogiq.com/en/2026-2027/catalog/courses/acg-accounting-general/2000/acg-2100',
    'irsc_acg2001': 'https://irsc.smartcatalogiq.com/en/2026-2027/catalog/courses/acg-accounting-general/2000/acg-2001',
    'irsc_acg2011': 'https://irsc.smartcatalogiq.com/en/2026-2027/catalog/courses/acg-accounting-general/2000/acg-2011',
    'fgcu_com_pdf': 'https://catalog.fgcu.edu/courses/com/com.pdf',
    'fiu_bme_ug': 'https://catalog.fiu.edu/search/?P=BME%204311',
}
NEEDLES = ['3120', '5235', '2000', '5105', '5305', '4311', '2071', '2100', '2001', '2011', '3101', '3103']


def text_of(raw):
    raw = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', raw)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', raw))).strip()


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    r = urllib.request.urlopen(req, timeout=40)
    return r.status, r.read()


for key in sys.argv[1:] or list(URLS):
    try:
        st, body = get(URLS[key])
    except Exception as e:
        print('==', key, 'ERROR', e)
        continue
    ext = '.pdf' if body[:4] == b'%PDF' else '.html'
    open(os.path.join(OUT, key + ext), 'wb').write(body)
    print('==', key, st, len(body), 'bytes', ext)
    if ext == '.pdf':
        continue
    t = text_of(body.decode('utf-8', 'replace'))
    hits = 0
    for n in NEEDLES:
        for m in re.finditer(r'[A-Z]{3}\s?' + n + r'[CL]?\b', t):
            print('  --', t[m.start():m.start() + 1200])
            hits += 1
            break
    if not hits:
        print('  ', t[:400])
    time.sleep(1.5)
