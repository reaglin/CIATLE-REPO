# -*- coding: utf-8 -*-
"""Batch 250: search cached catalogue PDFs (no pypdf) and print the text around each needle. Run from Tools/.

    python -I scratchpad/b250_pdf.py <pdf> <needle> [<needle> ...]
Same stream scrape as b249_pdf.py, but prints only a window round each hit.
"""
import re
import sys
import zlib

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
data = open(sys.argv[1], 'rb').read()
needles = sys.argv[2:]


def strings(stream):
    out = []
    for blk in re.finditer(rb'BT(.*?)ET', stream, re.S):
        body = blk.group(1)
        out.append(b''.join(re.findall(rb'\(((?:\\.|[^\\)])*)\)', body)))
    t = b'\n'.join(out)
    t = re.sub(rb'\\([()\\])', rb'\1', t)
    t = t.replace(b'\\036', b'fi').replace(b'\\037', b'ff').replace(b'\\n', b'')
    return t.decode('latin-1')


texts = []
for m in re.finditer(rb'stream\r?\n', data):
    start = m.end()
    end = data.find(b'endstream', start)
    try:
        raw = zlib.decompress(data[start:end])
    except Exception:
        continue
    if b'Tj' not in raw and b'TJ' not in raw:
        continue
    texts.append(strings(raw))
print('streams with text:', len(texts))
for nd in needles:
    pat = re.compile(re.escape(nd).replace(r'\ ', r'\s*'))
    hits = 0
    for t in texts:
        flat = re.sub(r'\s+', ' ', t)
        for mm in pat.finditer(flat):
            hits += 1
            if hits <= 6:
                print('== %s: %s' % (nd, flat[max(0, mm.start() - 150):mm.start() + 1100]))
    print('-- %s: %d hits' % (nd, hits))
