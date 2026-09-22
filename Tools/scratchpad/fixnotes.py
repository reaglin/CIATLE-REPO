# -*- coding: utf-8 -*-
import json, io
p='career_paths/social-worker.json'
d=json.load(io.open(p,encoding='utf-8'))
d['sources'][1]['note']=("⚠⚠ Requires a master's degree in social work from a graduate school accredited "
 "by the Council on Social Work Education (or an accredited doctorate), and at least 2 years of clinical "
 "social work experience SUBSEQUENT to the graduate degree, supervised by a licensed clinical social worker "
 "or the equivalent, plus a theory and practice examination. ⚠ In private practice a licensed mental "
 "health professional must be on the premises when a registered intern provides clinical services.")
print(len(d['sources'][1]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
