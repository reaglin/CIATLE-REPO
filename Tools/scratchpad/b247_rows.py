# -*- coding: utf-8 -*-
"""Batch 247: dump the SCNS flat-file rows for the requested courses. Run from Tools/."""
import io
import json
import sys

sys.path.insert(0, 'scratchpad')
import scns

imap = json.load(io.open('scratchpad/inst_map.json', encoding='utf-8'))
want = set(a.upper() for a in sys.argv[1:])
SKIP = ('prefix', 'level', 'century', 'decade', 'unit', 'lab')
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    cid = (r['prefix'] + r['level'] + r['century'] + r['decade'] + r['unit'] + (r['lab'] or '')).strip().upper()
    if cid in want:
        code = imap.get(str(int(r['institution'])), '').split('-')[0].strip()
        print('%-9s %-6s %-4s | %-40s | %-40s | eff %s chg %s' % (
            cid, code, r['credit'], r['inst_title'], r.get('state_title', ''), r['dt_effective'], r['dt_changed']))
