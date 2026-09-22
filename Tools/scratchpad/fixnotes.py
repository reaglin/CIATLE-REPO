# -*- coding: utf-8 -*-
import json, io
p='career_paths/physician.json'
d=json.load(io.open(p,encoding='utf-8'))
d['sources'][1]['note']=("⚠⚠⚠ Subsection (8)(e) allows certification WITHOUT an approved residency "
 "where the applicant holds an active unencumbered licence to practise medicine in a foreign country, has "
 "actively practised during the ENTIRE 4-YEAR PERIOD preceding application, completed a residency or "
 "substantially similar postgraduate training recognised in that jurisdiction, holds a valid ECFMG "
 "certificate, and ⚠⚠ has AN OFFER FOR FULL-TIME EMPLOYMENT as a physician from a Florida health "
 "care provider.")
print(len(d['sources'][1]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
