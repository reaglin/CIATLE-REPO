# -*- coding: utf-8 -*-
"""Batch 252: second round of fetches (run from Tools/). Saves under scratchpad/b252/ (untrusted: text only).

    python scratchpad/b252_fetch2.py [key ...]
FAMU's catalogue serves an incomplete certificate chain, so its pages are read with verification off
(public catalogue text only, nothing sent).
"""
import html
import os
import re
import ssl
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
OUT = os.path.join('scratchpad', 'b252')
URLS = {
    'famu_acg5875': 'https://catalog.famu.edu/search/?P=ACG%205875',
    'famu_acg_courses': 'https://catalog.famu.edu/course-descriptions/acg/',
    'mdc_curricunet': 'https://mdc.curricunet.com/catalog/search?query=AVM%201160',
    'mdc_curricunet2': 'https://mdc.curricunet.com/Report/Course/GetReport?courseNumber=1160&subject=AVM',
    'uf_bcn_grad': 'https://catalog.ufl.edu/graduate/colleges-schools/UGDCP/BCN/',
    'uf_bcn_courses': 'https://catalog.ufl.edu/UGRD/courses/building_construction/',
    'uf_bcn_search': 'https://catalog.ufl.edu/search/?search=BCN+6788',
    'uf_edg7365': 'https://catalog.ufl.edu/search/?P=EDG%207365',
}
NEEDLES = ['6788', '5875', '1160', '6046']
INSECURE = ssl.create_default_context()
INSECURE.check_hostname = False
INSECURE.verify_mode = ssl.CERT_NONE


def text_of(raw):
    raw = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', raw)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', raw))).strip()


for key in sys.argv[1:] or list(URLS):
    url = URLS[key]
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        ctx = INSECURE if 'famu.edu' in url else None
        r = urllib.request.urlopen(req, timeout=40, context=ctx)
        body = r.read()
    except Exception as e:
        print('==', key, 'ERROR', e)
        continue
    open(os.path.join(OUT, key + '.html'), 'wb').write(body)
    t = text_of(body.decode('utf-8', 'replace'))
    print('==', key, r.status, len(body))
    hits = 0
    for n in NEEDLES:
        for m in re.finditer(r'[A-Z]{3}\s?' + n + r'[CL]?\b', t):
            print('  --', t[max(0, m.start() - 100):m.start() + 1500])
            hits += 1
            break
    if not hits:
        print('  ', t[:300])
    time.sleep(1.5)
