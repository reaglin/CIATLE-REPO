# -*- coding: utf-8 -*-
"""Batch 254: print the SCNS flat-file rows for the given course ids (run from Tools/)."""
import io
import json
import os
import sys

sys.path.insert(0, 'scratchpad')
import scns

scns.institution_map = lambda o=None: json.load(io.open(os.path.join('scratchpad', 'inst_map.json'),
                                                        encoding='utf-8'))
import list_missing as lm  # noqa: E402

IDS = sys.argv[1:]
for r in scns.parse_flatfile(lm.FLAT):
    c = lm.cid_of(r)
    if c in IDS:
        print(c, json.dumps(r, default=str)[:400])
