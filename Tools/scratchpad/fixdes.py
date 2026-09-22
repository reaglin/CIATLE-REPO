# -*- coding: utf-8 -*-
import json, io
p='programs/graphic-and-digital-design.json'
d=json.load(io.open(p,encoding='utf-8'))
d['cips']=[c for c in d['cips'] if c['cipCode'] not in ('50.0102',)]
d['cips'].append({"cipCode":"09.0702","note":"⚠⚠ Digital Communication and Media/Multimedia — 29 Florida public institutions and 797 credentials, 531 of them bachelor's. Florida State 238, FAU 153, FIU 106, Hillsborough 43, Seminole State 37. ⚠ The largest reachable piece of this field, and it is filed under COMMUNICATION rather than design."})
n=d['degreesNote'].replace(
 "⚠ Meanwhile Digital Arts (50.0102) is 16 institutions and 723 credentials with 596 bachelor's, UCF alone awarding 507.",
 "⚠ Meanwhile Digital Arts (50.0102) is 16 institutions and 723 credentials with 596 bachelor's, UCF alone awarding 507 — this site's CIP tree does not yet carry 50.01, so that code is named here rather than claimed.")
d['degreesNote']=n
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print(len(n))
