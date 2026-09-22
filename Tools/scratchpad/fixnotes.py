# -*- coding: utf-8 -*-
import json, io
p='career_paths/physician-assistant.json'
d=json.load(io.open(p,encoding='utf-8'))
s=d['sources']
s[1]['note']=("⚠⚠⚠ Licensure requires an ARC-PA accredited programme and a passing NCCPA score, "
 "and anyone MATRICULATING AFTER 31 DECEMBER 2020 must hold a master's. ⚠⚠ A physician may not "
 "supervise more than 10 currently licensed physician assistants at any one time. ⚠ Schedule II "
 "prescribing is limited to a 7-day supply, paediatric psychiatric medication to 14 days. ⚠ A PA may "
 "authenticate any document a physician may, including death certificates and DNR orders.")
s[2]['note']=("⚠⚠⚠ What makes the PA-versus-nurse-practitioner comparison concrete. An APRN may "
 "register for AUTONOMOUS practice with an unencumbered licence, no discipline in five years, 3,000 "
 "clinical hours within five years under physician supervision, and 3 graduate semester hours each in "
 "differential diagnosis and pharmacology. ⚠ Scope is limited to PRIMARY CARE — family medicine, "
 "general paediatrics, general internal medicine — with no surgery except subcutaneous procedures.")
for i in (1,2): print(i, len(s[i]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
