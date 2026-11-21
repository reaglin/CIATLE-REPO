# -*- coding: utf-8 -*-
"""Batch 247: fetch the USF, UWF and UNF course pages for the requested EEL courses and print the text.

    python scratchpad/b247_fetch.py          (run from Tools/)
Pages are saved under scratchpad/b247/ (untrusted data: read as text only).
"""
import html
import os
import re
import sys
import time
import urllib.request

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

OUT = os.path.join('scratchpad', 'b247')
os.makedirs(OUT, exist_ok=True)

URLS = {
    'usf_EEL4206L': 'https://cloud.usf.edu/academic-programs/details/prefix/EEL/code/4206L',
    'usf_EEL4212': 'https://cloud.usf.edu/academic-programs/details/prefix/EEL/code/4212',
    'usf_EEL4214': 'https://cloud.usf.edu/academic-programs/details/prefix/EEL/code/4214',
    'usf_EEL4213': 'https://cloud.usf.edu/academic-programs/details/prefix/EEL/code/4213',
    'usf_EEL4205': 'https://cloud.usf.edu/academic-programs/details/prefix/EEL/code/4205',
    'usf_EEL3212': 'https://cloud.usf.edu/academic-programs/details/prefix/EEL/code/3212',
    'uwf_EEL4210': 'https://catalog.uwf.edu/search/?P=EEL%204210',
    'unf_EEL4081': 'https://www.unf.edu/catalog/search/?P=EEL%204081',
    'usf_EGN3374': 'https://cloud.usf.edu/academic-programs/details/prefix/EGN/code/3374',
    'usf_EGN3375': 'https://cloud.usf.edu/academic-programs/details/prefix/EGN/code/3375',
    'usf_EEL4241': 'https://cloud.usf.edu/academic-programs/details/prefix/EEL/code/4241',
    'unf_EEL4081b': 'https://catalog.unf.edu/search/?P=EEL%204081',
    'unf_EEL4081c': 'https://www.unf.edu/catalog/courses/eel/',
    'mdc_PET1170': 'https://mdc.curricunet.com/catalog/search?query=PET%201170',
    'uwf_EEL3211':'https://catalog.uwf.edu/search/?P=EEL%203211',
}


def text_of(raw):
    raw = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', raw)
    t = re.sub(r'(?s)<[^>]+>', ' ', raw)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()


want = sys.argv[1:] or list(URLS)
for key in want:
    url = URLS[key]
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        raw = urllib.request.urlopen(req, timeout=40).read().decode('utf-8', 'replace')
    except Exception as e:
        print('==', key, 'ERROR', e)
        continue
    open(os.path.join(OUT, key + '.html'), 'w', encoding='utf-8').write(raw)
    t = text_of(raw)
    m = re.search(r'(Course Description|Description)', t)
    start = max(0, (m.start() - 300) if m else 0)
    print('==', key, len(raw), 'bytes')
    print(t[start:start + 1600])
    time.sleep(1.5)
