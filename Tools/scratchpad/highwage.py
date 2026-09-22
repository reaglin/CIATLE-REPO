# -*- coding: utf-8 -*-
import json, io, glob, re
out=set()
pat=re.compile(r'\$(1[5-9][0-9],[0-9]{3}|[2-9][0-9]{2},[0-9]{3})')
for f in sorted(glob.glob('career_paths/*.json')):
    d=json.load(io.open(f,encoding='utf-8'))
    s=(d.get('description') or '')+(d.get('bodyHtml') or '')+(d.get('credentialNote') or '')
    for m in pat.findall(s):
        out.add((m, d['name'][:44]))
for m,n in sorted(out, key=lambda x:-int(x[0].replace(',',''))):
    print('$'+m, '-', n)
