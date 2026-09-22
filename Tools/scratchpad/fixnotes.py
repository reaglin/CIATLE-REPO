# -*- coding: utf-8 -*-
import json, io
p='career_paths/graphic-designer.json'
d=json.load(io.open(p,encoding='utf-8'))
d['sources'][3]['note']=("⚠⚠⚠ The clock-hour route, printed in the statewide titles: GRA0026 "
 "GRAPHIC DESIGNER (300 HOURS) is carried by 11 Florida technical colleges, alongside GRA0024 PRODUCTION "
 "ASSISTANT (150 HOURS), GRA0025 DIGITAL ASSISTANT DESIGNER (300) and GRA0027 MEDIA DESIGNER (300). "
 "⚠ The OCP letters are inconsistent across them, so more than one framework uses the prefix. A "
 "parallel ladder runs DIG0081–DIG0084 at 8 technical colleges totalling 1,050 clock hours.")
print(len(d['sources'][3]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
