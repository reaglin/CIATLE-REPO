# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0,'scratchpad'); import scns
imap={k:v.split('-')[0].strip() for k,v in scns.institution_map().items()}
pairs=[('ENT1000','ENT2000'),('ENT3003','ENT3004'),('SBM1000','SBM2000')]
want={x for p in pairs for x in p}
car=collections.defaultdict(set); ids=set()
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status']!='A' or r['prefix'] not in ('ENT','SBM'): continue
    inst=imap.get(r['institution'].lstrip('0'))
    if not inst or not scns.is_public(inst): continue
    cid=(r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip()
    ids.add(cid)
    if cid in want: car[cid].add(inst)
for a,b in pairs:
    ov=car[a]&car[b]
    print('%-8s %2d  vs %-8s %2d   overlap: %s' % (a,len(car[a]),b,len(car[b]), ' '.join(sorted(ov)) or 'NONE'))
open('scratchpad/entids.txt','w').write('\n'.join(sorted(ids)))
print('ENT/SBM ids', len(ids))
