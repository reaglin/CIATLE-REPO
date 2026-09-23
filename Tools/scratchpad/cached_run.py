# -*- coding: utf-8 -*-
"""Run a scratchpad tool with scns.institution_map() served from inst_map.json.

The live SCNS institution dropdown returned HTTP 500 on 2026-09-23. The map changes rarely,
so the cached copy is a safe stand-in.

    python scratchpad/cached_run.py carriers.py --prefix COS
    python scratchpad/cached_run.py list_missing.py --push COS0001 ...
"""
import io, json, os, runpy, sys

sys.path.insert(0, 'scratchpad')
import scns

_CACHE = os.path.join('scratchpad', 'inst_map.json')
scns.institution_map = lambda o=None: json.load(io.open(_CACHE, encoding='utf-8'))

script = sys.argv[1]
sys.argv = [os.path.join('scratchpad', script)] + sys.argv[2:]
runpy.run_path(os.path.join('scratchpad', script), run_name='__main__')
