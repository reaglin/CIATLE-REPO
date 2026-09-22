# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0,'scratchpad'); import scns
imap={k:v.split('-')[0].strip() for k,v in scns.institution_map().items()}
pairs=[('JOU1100','JOU2100'),('ADV3300','ADV4300')]
want={x for p in pairs for x in p}
car=collections.defaultdict(lambda: collections.defaultdict(set)); ids=set()
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status']!='A' or r['prefix'] not in ('JOU','PUR','ADV'): continue
    inst=imap.get(r['institution'].lstrip('0'))
    if not inst or not scns.is_public(inst): continue
    cid=(r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip()
    ids.add(cid)
    if cid in want: car[cid][scns.sector_of(inst)].add(inst)
for a,b in pairs:
    A=set().union(*car[a].values()) if car[a] else set()
    B=set().union(*car[b].values()) if car[b] else set()
    print('%-8s %s  vs %-8s %s   overlap: %s' % (a,{k:len(v) for k,v in sorted(car[a].items())},b,{k:len(v) for k,v in sorted(car[b].items())},' '.join(sorted(A&B)) or 'NONE'))
open('scratchpad/jouids.txt','w').write('\n'.join(sorted(ids)))
print('ids',len(ids))
