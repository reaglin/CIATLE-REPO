# -*- coding: utf-8 -*-
import json, io, sys
d=json.load(io.open('scratchpad/ipeds_fl.json',encoding='utf-8'))
pref=sys.argv[1]
out=[]
for c,rows in d.items():
    if not c.startswith(pref): continue
    out.append((c,len({r['school'] for r in rows}),sum(r['completions'] for r in rows)))
for c,s,n in sorted(out,key=lambda x:-x[2]):
    print('%-10s %3d schools %6d' % (c,s,n))
