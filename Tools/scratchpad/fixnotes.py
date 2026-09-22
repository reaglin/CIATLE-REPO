# -*- coding: utf-8 -*-
import json, io
p='career_paths/phlebotomist.json'
d=json.load(io.open(p,encoding='utf-8'))
d['sources'][1]['note']=("⚠⚠⚠ The statute this page turns on. Clinical laboratory personnel means a "
  "director, supervisor, technologist, blood gas analyst or technician who performs or is responsible for "
  "laboratory test procedures — and the definition expressly excludes trainees, blood bank and "
  "plasmapheresis screeners, PHLEBOTOMISTS, and persons employed to perform manual pretesting duties. "
  "⚠ So the Florida Board of Clinical Laboratory Personnel licenses the two rungs above and names "
  "this one out.")
print(len(d['sources'][1]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
