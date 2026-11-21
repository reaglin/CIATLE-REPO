# -*- coding: utf-8 -*-
"""Batch 250: print every SCNS flat-file row for the requested ids (run from Tools/).

    python scratchpad/b250_rows.py EML4328C ETS1542 ...
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
KEEP = ('inst', 'inst_title', 'state_title', 'credit', 'clock_hours', 'eff_date', 'end_date', 'status')
for r in scns.parse_flatfile(os.path.join('scratchpad', 'crslist.txt')):
    c = (r['prefix'] + r['level'] + r['century'] + r['decade'] + r['unit'] + (r['lab'] or '')).strip().upper()
    if c in IDS:
        name = imap.get(r['institution'].lstrip('0'), '')
        code = name.split('-')[0].strip()
        pub = scns.is_public(code)
        print('%-9s %-45s %-7s cr %-5s clk %-5s eff %s disc %s | %s | state: %s' % (
            c, name[:45], 'PUBLIC' if pub else 'priv', r.get('credit'), r.get('clock_hours') or '',
            r.get('dt_effective'), r.get('dt_discontinued') or '', r.get('inst_title'), r.get('state_title')))
