# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0,'scratchpad'); import scns
imap={k:v.split('-')[0].strip() for k,v in scns.institution_map().items()}
want={'ISM3011','ISM4011'}
car=collections.defaultdict(lambda: collections.defaultdict(set)); ids=set()
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status']!='A' or r['prefix']!='ISM': continue
    inst=imap.get(r['institution'].lstrip('0'))
    if not inst or not scns.is_public(inst): continue
    cid=(r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip()
    ids.add(cid)
    if cid in want: car[cid][scns.sector_of(inst)].add(inst)
a=set().union(*car['ISM3011'].values()); b=set().union(*car['ISM4011'].values())
for c in sorted(want): print(c, {k:len(v) for k,v in sorted(car[c].items())})
print('overlap:', sorted(a & b) or 'NONE')
open('scratchpad/ismids.txt','w').write('\n'.join(sorted(ids)))
print('ISM ids', len(ids))
