# -*- coding: utf-8 -*-
"""Batch 250: print the text round a pattern in a saved page (run from Tools/).

    python scratchpad/b250_read.py scratchpad/b250/irsc_2542_2526.html "ETS 2542 Prog" [chars]
"""
import html
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
raw = open(sys.argv[1], encoding='utf-8').read()
raw = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', raw)
t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', raw))).strip()
n = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
for m in list(re.finditer(sys.argv[2], t))[:3]:
    print('--', t[m.start():m.start() + n])
