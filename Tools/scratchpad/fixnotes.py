# -*- coding: utf-8 -*-
import json, io
p='career_paths/entrepreneur.json'
d=json.load(io.open(p,encoding='utf-8'))
d['sources'][4]['note']=("⚠⚠ Measured over the whole file: ENT1000 Introduction to Entrepreneurship is "
 "carried by 11 Florida public institutions and ENT2000, the same title, by 7 — with NO overlap. SBM2000 "
 "Small Business Management is carried by 14 and SBM1000 by 3, again no overlap. ⚠ All four are lower "
 "division, so no baccalaureate credit is at risk; the cost is transfer matching. ✅ USF carries BOTH "
 "ENT3003 and ENT3004, evidence those two are genuinely different courses.")
print(len(d['sources'][4]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
