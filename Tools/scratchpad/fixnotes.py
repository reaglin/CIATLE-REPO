# -*- coding: utf-8 -*-
import json, io
p='career_paths/film-video-editor.json'
d=json.load(io.open(p,encoding='utf-8'))
s=d['sources']
s[0]['note']=("⚠⚠ Film and video editors $75,420 and camera operators $74,990 (2025), 72,000 jobs, "
 "about 5,600 annual openings, 35% self-employed, typical entry a bachelor's in film, broadcasting, "
 "communications or a related field. Employment \"projected to grow 3 percent from 2025 to 2035\". "
 "⚠⚠⚠ The page discusses technology — digital cameras changing camera assistant work, "
 "robotic cameras letting one operator control several — but makes NO claim about AI.")
s[3]['note']=("⚠⚠ Two institutional signatures, measured over the whole file. FLORIDA ATLANTIC runs 11 "
 "of its 21 undergraduate film courses at FOUR credits while UCF runs 78 of 103 at three, USF 25 of 25, UNF "
 "24 of 25. ⚠⚠⚠ FLORIDA STATE runs 45 of its 70 at VARIABLE credit, UCF 22. ⚠ Numbering: "
 "FIL2030 (4 carriers) and FIL1030 (3) share the title History of Motion Pictures with no overlap, and "
 "FIL1420 and FIL1420C carry DIFFERENT titles.")
s[4]['note']=("⚠⚠⚠ This project's own catalogue work. FIL4036 Film History 1 runs to 1959 "
 "statewide, to the 1940s at Florida Atlantic, and has no boundary at all at UWF where no part 2 exists "
 "— and FAU's catalogue says part 2 \"may be taken before\" part 1 while the state record requires the "
 "order. ⚠ Two decades of film history sit inside the course at one institution and outside it at "
 "another. ⚠⚠ FIL4037 is Film History 2 statewide but USF carries it as History of Video Art.")
for i in (0,3,4): print(i, len(s[i]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
