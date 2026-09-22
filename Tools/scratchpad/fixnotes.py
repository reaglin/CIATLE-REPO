# -*- coding: utf-8 -*-
import json, io
p='career_paths/mental-health-counselor.json'
d=json.load(io.open(p,encoding='utf-8'))
d['sources'][1]['note']=d['sources'][1]['note'].replace(
  "university-sponsored supervised practicum, internship or field experience including",
  "university-sponsored supervised practicum or internship including")
print(len(d['sources'][1]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
