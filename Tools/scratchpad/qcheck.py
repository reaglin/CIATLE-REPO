# -*- coding: utf-8 -*-
import csv, io, json, re
d=json.load(io.open('scratchpad/ipeds_fl.json',encoding='utf-8'))
seed=io.open('../PreseMakerRepo.Api/Data/Seed/cip.json',encoding='utf-8').read()
def foot(pref):
    sch=set(); n=0
    for c,rows in d.items():
        if c.startswith(pref):
            sch|={r['school'] for r in rows}; n+=sum(r['completions'] for r in rows)
    return len(sch),n
for r in csv.DictReader(io.open('career_paths/QUEUE.csv',encoding='utf-8')):
    if r['status']: continue
    s,n=foot(r['cip'])
    seeded='yes' if ('"%s"'%r['cip']) in seed else 'NO'
    print('%-4s %-34s %-7s seed=%-3s %3d sch %6d' % (r['rank'],r['slug'],r['cip'],seeded,s,n))
