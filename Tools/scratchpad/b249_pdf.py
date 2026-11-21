# -*- coding: utf-8 -*-
"""Batch 249: crude PDF text search without pypdf (Flate streams, Tj/TJ strings). Run from Tools/.

    python -I scratchpad/b249_pdf.py scratchpad/b249/nfc_catalog.pdf BCV
"""
import re
import sys
import zlib

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
data = open(sys.argv[1], 'rb').read()
needle = sys.argv[2]


def strings(stream):
    out = []
    for blk in re.finditer(rb'BT(.*?)ET', stream, re.S):
        body = blk.group(1)
        out.append(b''.join(re.findall(rb'\(((?:\\.|[^\\)])*)\)', body)))
    t = b'\n'.join(out)
    t = re.sub(rb'\\([()\\])', rb'\1', t)
    t = t.replace(b'\\036', b'fi').replace(b'\\037', b'ff').replace(b'\\n', b'')
    return t.decode('latin-1')


n = 0
for m in re.finditer(rb'stream\r?\n', data):
    start = m.end()
    end = data.find(b'endstream', start)
    try:
        raw = zlib.decompress(data[start:end])
    except Exception:
        continue
    if b'Tj' not in raw and b'TJ' not in raw:
        continue
    t = strings(raw)
    if needle in t:
        n += 1
        print('=== stream at', start)
        print(t[:6000])
print('matches', n)
