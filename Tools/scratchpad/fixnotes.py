# -*- coding: utf-8 -*-
import json, io
p='career_paths/early-childhood-educator.json'
d=json.load(io.open(p,encoding='utf-8'))
s=d['sources']
s[3]['note']=("⚠⚠⚠ Subsection (3)(c)1. requires a prekindergarten instructor to hold at minimum a "
 "child development associate credential issued by the National Credentialing Program of the Council for "
 "Professional Recognition, or a credential the Department of Children and Families approves as equivalent "
 "or greater. ⚠ A CDA is a CREDENTIAL, not a degree — which is why Florida's early childhood "
 "training output is almost entirely certificates. Degrees in early childhood or elementary education may "
 "substitute.")
s[4]['note']=("⚠⚠⚠ Two certifications, nearly identical requirements, very different reach. "
 "PRESCHOOL EDUCATION covers BIRTH to AGE 4; PREKINDERGARTEN/PRIMARY EDUCATION covers AGE 3 to GRADE 3. "
 "Both require a bachelor's with 45 semester hours of specialisation — child growth and development, "
 "developmentally appropriate curriculum, family and community involvement, health, nutrition and safety, "
 "assessment, special needs. ⚠ Only the second reaches a public-school classroom.")
for i in (3,4): print(i, len(s[i]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
