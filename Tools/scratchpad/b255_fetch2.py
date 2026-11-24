# -*- coding: utf-8 -*-
"""Batch 255: print the body of a catalogue page around a course code (run from Tools/).

    python scratchpad/b255_fetch2.py <url> <needle> [<span>]
Fetched pages are read as text only.
"""
import re
import sys

import requests

UA = {'User-Agent': 'Mozilla/5.0 (course-guide research)'}


def text(h):
    h = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    return re.sub(r'\s+', ' ', h)


url, needle = sys.argv[1], sys.argv[2]
span = int(sys.argv[3]) if len(sys.argv) > 3 else 1800
r = requests.get(url, headers=UA, timeout=40)
t = text(r.text)
hits = [m.start() for m in re.finditer(needle, t)]
print('HTTP', r.status_code, len(r.text), 'hits', hits[:12])
for i in hits[1:4] if len(hits) > 1 else hits:
    print('---')
    print(t[max(0, i - 80):i + span])
