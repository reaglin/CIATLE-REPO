# -*- coding: utf-8 -*-
import json, io
p='programs/social-work.json'
d=json.load(io.open(p,encoding='utf-8'))
n=d['degreesNote']
n=n.replace("The 368 master's recorded under the social work code are not the whole picture: a further 796 are "
            "coded under CLINICAL/MEDICAL SOCIAL WORK (51.1503) — Florida State 431, FAU 143, UWF 120, "
            "FIU 74, UNF 28 — and FSU, UWF, FIU and UNF record no master's under the social work code at "
            "all. ⚠ Florida's real MSW output is 1,164 a year, not 368. The school list is the same nine "
            "either way; only the counts differ. (This site's CIP tree does not yet carry 51.15, so the "
            "programme claims the social work code alone.)",
            "A further 796 master's are coded under CLINICAL/MEDICAL SOCIAL WORK (51.1503) — FSU 431, "
            "FAU 143, UWF 120, FIU 74, UNF 28 — and four of those record no master's under the social "
            "work code at all. ⚠ Florida's real MSW output is 1,164 a year, not 368. Same nine schools "
            "either way; only the counts differ.")
n=n.replace(" ⚠ CSWE notes that the extent of advanced standing varies by programme, so ask each one directly.",
            " ⚠ The extent of advanced standing varies by programme — ask each one.")
d['degreesNote']=n
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print(len(n))
