# -*- coding: utf-8 -*-
import json, io
p='career_paths/mis-analyst.json'
d=json.load(io.open(p,encoding='utf-8'))
d['sources'][3]['note']=("⚠⚠⚠ Measured over the whole file: ISM3011 is carried by 12 Florida "
 "public institutions (7 state colleges, 5 universities) and ISM4011, the same subject, by 10 (9 state "
 "colleges, 1 university) — with ZERO overlap. ⚠⚠ Both are upper division, so unlike the "
 "MAR2011/MAR3023 pair no credit is lost; the risk is purely transfer matching. ⚠ The shape recurs on "
 "systems analysis (ISM3113 at 7, ISM4113 at 6). Security sits inside the prefix too: ISM4323 at 10, "
 "ISM4324 at 6.")
print(len(d['sources'][3]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
