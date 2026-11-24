# -*- coding: utf-8 -*-
"""Batch 255: list public carriers whose institution title matches a pattern, within a prefix (run from Tools/).

    python scratchpad/b255_titles.py CJE "POLICE ADMIN|POLICE ORGAN|PATROL"
"""
import io
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, 'scratchpad')
import scns  # noqa: E402

scns.institution_map = lambda o=None: json.load(io.open(os.path.join('scratchpad', 'inst_map.json'),
                                                        encoding='utf-8'))
import list_missing as lm  # noqa: E402

prefix, pat = sys.argv[1], re.compile(sys.argv[2], re.I)
imap = scns.institution_map()
hits = defaultdict(list)
for r in scns.parse_flatfile(lm.FLAT, prefix=prefix):
    if pat.search(r['inst_title']) or pat.search(r.get('state_title') or ''):
        short = (imap.get(str(int(r['institution']))) or '?').split(' - ')[0]
        if not scns.is_public(short):
            continue
        hits[lm.cid_of(r)].append('%s:%s:%s' % (short, r['inst_title'].strip(), r['credit'].strip()))
        hits[lm.cid_of(r) + ' state'] = [r.get('state_title', '').strip()]
for k in sorted(hits):
    print(k, hits[k])
