# -*- coding: utf-8 -*-
import json, io
p='career_paths/hospitality-manager.json'
d=json.load(io.open(p,encoding='utf-8'))
d['sources'][4]['note']=("⚠⚠⚠ This project's own catalogue work found HFT among Florida's most "
 "confused prefixes. HFT4274: statewide title Resort Management, but FGCU teaches Vacation Ownership and "
 "Timeshare and FIU Short-Term Rental — two carriers agreeing against the state label. HFT4252: title "
 "says employee wellbeing, description is hotel management, carriers split one each. ⚠ HFT3271: "
 "statewide Condo/Resort Management, carriers teach nightclub, club and spa management — four readings, "
 "none the statewide one.")
print(len(d['sources'][4]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
