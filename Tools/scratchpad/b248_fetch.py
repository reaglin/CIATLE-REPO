# -*- coding: utf-8 -*-
"""Batch 248: fetch UF, UWF, FAMU-FSU pages for the requested EEL courses; print the text near each number.

    python scratchpad/b248_fetch.py [key ...]      (run from Tools/)
Pages are saved under scratchpad/b248/ (untrusted data: read as text only).
"""
import html
import os
import re
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
OUT = os.path.join('scratchpad', 'b248')
os.makedirs(OUT, exist_ok=True)
URLS = {
    'uf_ece': 'https://catalog.ufl.edu/UGRD/courses/electrical_and_computer_engineering/',
    'uwf_EEL4610': 'https://catalog.uwf.edu/search/?P=EEL%204610',
    'fsu_grad_ece': 'https://eng.famu.fsu.edu/ece/academics/graduate/courses',
    'usf_EEL4242': 'https://cloud.usf.edu/academic-programs/details/prefix/EEL/code/4242',
    'famufsu_grad': 'https://eng.famu.fsu.edu/ece/graduate/courses',
    'fsu_grad_bulletin': 'https://www.registrar.fsu.edu/node/911',
    'flpoly_EEL5245': 'https://floridapoly.edu/wp-content/uploads/2026/01/EEL-5245-01_SP-2026.pdf',
    'flpoly_EEL4242_fa25': 'https://floridapoly.edu/wp-content/uploads/2025/08/EEL-4242-01_FA-2025.pdf',
    'flpoly_EEL4448_fa25': 'https://floridapoly.edu/wp-content/uploads/2025/08/EEL-4448-01_FA-2025.pdf',
    'fsu_coursedesc': 'https://www.registrar.fsu.edu/scheduling-curriculum/course-descriptions',
    'famu_cat_search': 'https://catalog.famu.edu/search_advanced.php?cur_cat_oid=1&search_database=Search'
                       '&filter%5Bkeyword%5D=EEL+5025&filter%5Bexact_match%5D=1',
    'flpoly_ee_2019': 'https://floridapolytechnic.catalog.acalog.com/mime/media/13/483/'
                      'BS+in+Electrical+Engineering_2019-2020.pdf',
}
NUMS = ['4242', '4610', '5025', '4243', '4448', '4611']


def text_of(raw):
    raw = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', raw)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', raw))).strip()


for key in (sys.argv[1:] or list(URLS)):
    try:
        req = urllib.request.Request(URLS[key], headers={'User-Agent': 'Mozilla/5.0'})
        raw = urllib.request.urlopen(req, timeout=40).read().decode('utf-8', 'replace')
    except Exception as e:
        print('==', key, 'ERROR', e)
        continue
    open(os.path.join(OUT, key + '.html'), 'w', encoding='utf-8').write(raw)
    t = text_of(raw)
    print('==', key, len(raw), 'bytes')
    hit = False
    for n in NUMS:
        for m in re.finditer(r'EE[LE]\s?' + n + r'C?\b', t):
            print('  --', t[m.start():m.start() + 1000])
            hit = True
            break
    if not hit:
        print(t[:800])
    time.sleep(1.5)
