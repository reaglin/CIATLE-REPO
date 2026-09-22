# -*- coding: utf-8 -*-
import json, io
p='career_paths/health-information-technician.json'
d=json.load(io.open(p,encoding='utf-8'))
d['sources'][5]['note']=("⚠⚠ The three routes, measured. Health information management (51.0707 + "
  "51.0706): 31 Florida public institutions, 296 credentials, 109 associate and 127 bachelor's. Billing "
  "and coding (51.0714): 37 institutions, 416 credentials, ALL certificates. Office administration "
  "(51.0716 + 51.0705 + 51.0710 + 51.0702): 36 institutions, 242, all certificates. ⚠ Health care "
  "ADMINISTRATION (51.0701) is separate and far larger — 24 institutions, 1,293 credentials, mostly "
  "bachelor's and master's.")
print(len(d['sources'][5]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
