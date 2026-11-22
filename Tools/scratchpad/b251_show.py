# -*- coding: utf-8 -*-
"""Batch 251: show the text around a word in a saved page (run from Tools/).

    python scratchpad/b251_show.py sscf_acg2100.html Prerequisite 1500
"""
import html
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
t = open(os.path.join('scratchpad', 'b251', sys.argv[1]), encoding='utf-8', errors='replace').read()
t = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', t)
t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t)))
n = int(sys.argv[3]) if len(sys.argv) > 3 else 800
for m in list(re.finditer(re.escape(sys.argv[2]), t))[:3]:
    print('--', t[max(0, m.start() - n):m.start() + 600])
