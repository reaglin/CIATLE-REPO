# -*- coding: utf-8 -*-
"""Batch 250: fetch catalogue pages for the requested PLC courses and ECH3702.

    python scratchpad/b250_fetch.py [key ...]      (run from Tools/)
Pages are saved under scratchpad/b250/ (untrusted data: read as text only).
"""
import html
import os
import re
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
OUT = os.path.join('scratchpad', 'b250')
os.makedirs(OUT, exist_ok=True)
IRSC = 'https://irsc.smartcatalogiq.com/en/%s/catalog/courses/ets-engineering-technology/2000/%s'
PHSC = 'https://phsc.smartcatalogiq.com/en/%s/catalog-and-student-handbook/courses/ets-engineering-technology-specialty/1000/ets-1542'
URLS = {
    'irsc_2542_2526': IRSC % ('2025-2026', 'ets-2542'),
    'irsc_2544_2526': IRSC % ('2025-2026', 'ets-2544'),
    'irsc_2542_2627': IRSC % ('2026-2027', 'ets-2542'),
    'irsc_2544_2627': IRSC % ('2026-2027', 'ets-2544'),
    'phsc_1542_2526': PHSC % '2025-2026',
    'phsc_1542_2627': PHSC % '2026-2027',
    'phsc_1542_2021': PHSC % '2020-2021',
    'usf_ECH3702': 'https://cloud.usf.edu/academic-programs/details/prefix/ECH/code/3702',
    'uwf_ETS3543': 'https://catalog.uwf.edu/search/?P=ETS%203543',
    'unf_cat1': 'https://catalog.unf.edu/search/?P=EML%204328C',
    'unf_cat2': 'https://www.unf.edu/catalog/courses/eml/',
    'famu_search': 'https://catalog.famu.edu/search_advanced.php?cur_cat_oid=1&search_database=Search'
                   '&filter%5Bkeyword%5D=ETS+3543&filter%5Bexact_match%5D=1',
    'sscf_ets1542c': 'https://www.seminolestate.edu/catalog/courses/ets1542c',
    'lssc_ets': 'https://lssc-public.courseleaf.com/courses/ets/',
    'unf_bscadm': 'https://www.unf.edu/catalog/programs/ug/ccec/CCEC-BSCADM.html',
    'usf_chbme': 'https://www.usf.edu/engineering/chbme/undergraduate/courses-offered.aspx',
    'unf_apidata': 'https://www.unf.edu/velocity/sites/catalog/course-API-data.js',
    'unf_search_js': 'https://www.unf.edu/velocity/sites/catalog/course-search.js',
    'unf_bsme':'https://www.unf.edu/catalog/programs/ug/ccec/CCEC-BSME.html',
}
NEEDLES = ['2542', '2544', '1542', '3702', '3543', '4328', '4543']


def text_of(raw):
    raw = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', raw)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', raw))).strip()


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    r = urllib.request.urlopen(req, timeout=40)
    return r.status, r.read().decode('utf-8', 'replace')


for key in sys.argv[1:] or list(URLS):
    try:
        st, raw = get(URLS[key])
    except Exception as e:
        print('==', key, 'ERROR', e)
        continue
    open(os.path.join(OUT, key + '.html'), 'w', encoding='utf-8').write(raw)
    t = text_of(raw)
    print('==', key, st, len(raw), 'bytes')
    shown = 0
    for n in NEEDLES:
        for m in re.finditer(r'[A-Z]{3}\s?' + n + r'[CL]?\b', t):
            print('  --', t[m.start():m.start() + 1500])
            shown += 1
            break
        if shown:
            break
    if not shown:
        print('  ', t[:600])
    time.sleep(1.5)
