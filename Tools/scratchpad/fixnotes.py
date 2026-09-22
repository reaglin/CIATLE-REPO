# -*- coding: utf-8 -*-
import json, io
p='career_paths/athletic-trainer.json'
d=json.load(io.open(p,encoding='utf-8'))
d['sources'][4]['note']=("⚠⚠ The migration measured in the course catalogue: Florida carries 101 GRADUATE "
 "ATR course numbers against 46 undergraduate, and of the 26 ATR courses carried by two or more public "
 "institutions, 22 are graduate. ⚠ The only undergraduate ATR numbers with more than one carrier are "
 "ATR2010C, ATR3102, ATR3132 and a special-topics shell. The professional curriculum now sits at the 5000 "
 "level — ATR5217C is the most widely carried course in the prefix, at five institutions.")
print(len(d['sources'][4]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
