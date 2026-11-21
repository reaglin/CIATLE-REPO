# -*- coding: utf-8 -*-
"""Batch 249: print every SCNS flat-file row for the requested ids (run from Tools/).

    python scratchpad/b249_rows.py EEL2161 EEL3003 ...
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, 'scratchpad')
import scns

imap = json.load(io.open(os.path.join('scratchpad', 'inst_map.json'), encoding='utf-8'))
IDS = set(a.upper() for a in sys.argv[1:])
SKIP = ('prefix', 'level', 'century', 'decade', 'unit', 'lab')
for r in scns.parse_flatfile(os.path.join('scratchpad', 'crslist.txt')):
    c = (r['prefix'] + r['level'] + r['century'] + r['decade'] + r['unit'] + (r['lab'] or '')).strip().upper()
    if c in IDS:
        fields = dict((k, v) for k, v in r.items() if v and k not in SKIP)
        key = fields.get('inst') or fields.get('institution') or ''
        print(c, imap.get(key, ''), fields)
