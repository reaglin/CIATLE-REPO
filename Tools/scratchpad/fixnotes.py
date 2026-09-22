# -*- coding: utf-8 -*-
import json, io
p='career_paths/nurse-practitioner.json'
d=json.load(io.open(p,encoding='utf-8'))
s=d['sources']
s[4]['note']=("⚠⚠⚠ The source for the limit nobody reports: \"All APRN specialties are eligible "
 "for autonomous practice, however, only certified midwives are currently authorized to practice any "
 "specific functions related to their specialty area without an established physician protocol.\" Also the "
 "uptake: 11,201 APRNs registered for autonomous practice, and 3,458 psychiatric nurses of whom 1,093 hold "
 "primary-care autonomous registration. ⚠ The bill DIED in subcommittee on 8 March 2024.")
s[5]['note']=("⚠⚠ NONPF committed on 20 April 2018 to move all entry-level NP education to the DNP by "
 "2025 and reaffirmed it in 2023. Its trend data: DNP NP programmes 124 in 2014 to 254 in 2021; BSN-to-DNP "
 "graduates 934 in 2015 to 3,327 in 2021; MSN NP entry has levelled. ⚠⚠⚠ But NONPF is an "
 "association of FACULTIES — the commitment carries no regulatory force, AANP and ANCC still certify "
 "master's-prepared NPs, and only state boards set the licensure degree.")
for i in (4,5): print(i, len(s[i]['note']))
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
