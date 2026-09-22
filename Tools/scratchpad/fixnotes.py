# -*- coding: utf-8 -*-
import json, io
p='career_paths/journalist.json'
d=json.load(io.open(p,encoding='utf-8'))
d['sources'][5]['note']=("⚠⚠⚠ PUR3000: UF and FGCU teach the general introduction to public "
 "relations — history of the profession, ethics, the PR process — while UWF teaches INTRODUCTION TO "
 "PUBLIC AFFAIRS, government and nonprofit policy communication. A UWF student misses PR history, media "
 "relations and campaigns. ⚠⚠ PUR4801: statewide it is Public Relations CASES, but UWF runs its "
 "campaigns CAPSTONE on it. ⚠ JOU4306: UWF teaches arts criticism, UF data journalism in R.")
print(len(d['sources'][5]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
