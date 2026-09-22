# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0,'scratchpad'); import scns
imap={k:v.split('-')[0].strip() for k,v in scns.institution_map().items()}
cred=collections.defaultdict(collections.Counter); car=collections.defaultdict(set); ids=set()
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status']!='A' or r['prefix'] not in ('FIL','RTV'): continue
    inst=imap.get(r['institution'].lstrip('0'))
    if not inst or not scns.is_public(inst): continue
    cid=(r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip()
    ids.add(cid)
    if cid in ('FIL1030','FIL2030','FIL1420','FIL1420C'): car[cid].add(inst)
    if r['prefix']=='FIL' and r['level'] in '1234':
        c=(r.get('credit') or '').strip()
        try: cred[inst][int(float(c))]+=1
        except Exception: cred[inst]['VAR']+=1
print('FIL1030 vs FIL2030 overlap:', sorted(car['FIL1030']&car['FIL2030']) or 'NONE')
print('FIL1420 vs FIL1420C overlap:', sorted(car['FIL1420']&car['FIL1420C']) or 'NONE')
print()
for inst in sorted(cred, key=lambda k:-sum(cred[k].values()))[:8]:
    tot=sum(cred[inst].values())
    print('%-7s n=%-4d %s' % (inst, tot, dict(cred[inst].most_common())))
open('scratchpad/filids.txt','w').write('\n'.join(sorted(ids)))
print('\nFIL/RTV ids', len(ids))
