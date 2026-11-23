# -*- coding: utf-8 -*-
"""Batch 252: fetch catalogue pages for the requested courses.

    python scratchpad/b252_fetch.py [key ...]      (run from Tools/)
Pages are saved under scratchpad/b252/ (untrusted data: read as text only).
"""
import html
import os
import re
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
OUT = os.path.join('scratchpad', 'b252')
os.makedirs(OUT, exist_ok=True)
USF = 'https://cloud.usf.edu/academic-programs/details/prefix/%s/code/%s'
URLS = {
    'uf_EDH6046': 'https://catalog.ufl.edu/search/?P=EDH%206046',
    'uf_BCN6788': 'https://catalog.ufl.edu/search/?P=BCN%206788',
    'uwf_CEN6030': 'https://catalog.uwf.edu/search/?P=CEN%206030',
    'sscf_acg2360': 'https://www.seminolestate.edu/catalog/courses/acg2360',
    'famu_acg5875': 'https://catalog.famu.edu/search/?P=ACG%205875',
    'mdc_avm1160': 'https://www.mdc.edu/catalog/courses/avm1160',
    'fiu_cgn4980': 'https://catalog.fiu.edu/search/?P=CGN%204980',
    'fau_bme4536': 'https://catalog.fau.edu/search/?P=BME%204536',
    'uf_EDH_dept': 'https://catalog.ufl.edu/graduate/courses/edh/',
    'uf_BCN_dept': 'https://catalog.ufl.edu/graduate/courses/bcn/',
    'pbsc_acg2360': 'https://catalog.palmbeachstate.edu/search/?P=ACG%202360',
    'scf_acg2360': 'https://catalog.scf.edu/search_advanced.php?search_database=Search&search_db=Search&ecpage=1&ppage=1&spage=1&tpage=1&location=33&filter%5Bkeyword%5D=ACG+2360',
    'mdc_avm_search': 'https://www.mdc.edu/catalog/search/?P=AVM%201160',
    'uwf_cen_pdf': 'https://catalog.uwf.edu/courseinformation/courses/cen/cen.pdf',
}
NEEDLES = ['6046', '6788', '6030', '2360', '5875', '1160', '4980', '4536']


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
            print('  --', t[m.start():m.start() + 1400])
            hits += 1
            break
    if not hits:
        print('  ', t[:400])
    time.sleep(1.5)
