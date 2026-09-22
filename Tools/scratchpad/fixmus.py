# -*- coding: utf-8 -*-
import json, io
p='career_paths/film-video-editor.json'
d=json.load(io.open(p,encoding='utf-8'))
for c in d['courses']:
    if c['courseId']=='MUS1360':
        c['reason']=("Introduction to Music Technology — 7 Florida institutions. ⚠ Named deliberately: "
          "sound is half the finished product and the half most self-taught editors are weakest at, and this "
          "is the most widely carried audio-technology course in the state.")
        c['variantNote']=("⚠ It is a MUSIC course rather than a post-production one. Florida has no widely "
          "carried film-audio course — check whether your institution runs audio post under DIG, RTV or MUS.")
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('ok')
