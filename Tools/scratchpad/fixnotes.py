# -*- coding: utf-8 -*-
import json, io
p='career_paths/medical-assistant.json'
d=json.load(io.open(p,encoding='utf-8'))
d['sources'][2]['note']=("⚠⚠⚠ The statute this page turns on. A medical assistant assists in all "
  "aspects of medical practice under the direct supervision and responsibility of a physician; permitted "
  "tasks include venipunctures, injections and administering medication as directed. ⚠ No licence or "
  "certificate is required to do the work — but the TITLE certified medical assistant requires "
  "certification from an NCCA-accredited programme, a national or state medical association, or an entity "
  "the board approves.")
print(len(d['sources'][2]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
