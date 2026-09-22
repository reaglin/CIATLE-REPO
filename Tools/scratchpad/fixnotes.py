# -*- coding: utf-8 -*-
import json, io
p='career_paths/public-health-professional.json'
d=json.load(io.open(p,encoding='utf-8'))
n=d['sources'][4]['note']
d['sources'][4]['note']=n.replace("at least 25 semester credits (37 quarter hours) of coursework at C or better addressing",
                                  "at least 25 semester credits of coursework at C or better addressing")
print(len(d['sources'][4]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
