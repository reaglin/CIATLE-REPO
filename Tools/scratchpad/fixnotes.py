# -*- coding: utf-8 -*-
import json, io
p='career_paths/ux-designer.json'
d=json.load(io.open(p,encoding='utf-8'))
s=d['sources']
s[0]['note']=("⚠⚠ Web and digital interface designers $104,000 and web developers $92,650 (2025), "
 "132,700 jobs, about 8,000 annual openings, 13% of designers self-employed, typical entry a bachelor's. "
 "Employment \"projected to grow 5 percent from 2025 to 2035, faster than the average\". "
 "⚠⚠⚠ On AI: \"increasing use of artificial intelligence (AI) for web development may soften "
 "the employment growth of these workers… it may also allow some workers in other occupations to do "
 "basic web development tasks.\"")
s[3]['note']=("⚠⚠⚠ Measured over the whole file: 181 distinct active course identifiers carry "
 "\"web\", \"user interface\", \"user experience\" or \"human-computer\" in their statewide titles, across 25 "
 "DIFFERENT PREFIXES — and none reaches more than 13 carriers. The widest is CTS0085 Web Security "
 "Specialist (150 clock hours) at 13 technical colleges, then COP2830 and DIG0083 at 8. ⚠ Compare "
 "HSC0003 at 55 carriers: this subject has no settled home in the catalogue.")
for i in (0,3): print(i, len(s[i]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
