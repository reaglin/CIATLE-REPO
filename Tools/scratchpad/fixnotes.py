# -*- coding: utf-8 -*-
import json, io
p='career_paths/school-counselor.json'
d=json.load(io.open(p,encoding='utf-8'))
d['sources'][2]['note']=("⚠⚠⚠ A Department of EDUCATION certification, not a chapter 491 licence. "
 "Plan One: a master's or higher with a graduate major in guidance and counseling or school counseling, "
 "including a minimum of 600 CLOCK HOURS of supervised internship serving school-aged students. "
 "⚠⚠ Plan Three: 300 clock hours for a current full-time teacher with 5+ years and effective or "
 "highly effective ratings in the last 3. Plan Two substitutes two years of district mentoring. "
 "⚠ Amended effective 21 December 2025.")
print(len(d['sources'][2]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
