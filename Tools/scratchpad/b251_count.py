# -*- coding: utf-8 -*-
"""Batch 251: public carriers per course id from the SCNS flat file, with the cached institution map (run from Tools/).

    python scratchpad/b251_count.py ACG2021 ACG3101 ...
"""
import io
import json
import os
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, 'scratchpad')
import scns

imap = json.load(io.open(os.path.join('scratchpad', 'inst_map.json'), encoding='utf-8'))
IDS = [a.upper() for a in sys.argv[1:]]
hits = defaultdict(list)
for r in scns.parse_flatfile(os.path.join('scratchpad', 'crslist.txt')):
    c = (r['prefix'] + r['level'] + r['century'] + r['decade'] + r['unit'] + (r['lab'] or '')).strip().upper()
    if c in IDS:
        code = imap.get(r['institution'].lstrip('0'), '').split('-')[0].strip()
        if scns.is_public(code):
            hits[c].append('%s:%s' % (code, str(r.get('credit')).rstrip('0').rstrip('.')))
for c in IDS:
    print('%-9s %3d  %s' % (c, len(hits[c]), ' '.join(sorted(set(hits[c])))))
