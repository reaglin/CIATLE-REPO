# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0,'scratchpad'); import scns
imap={k:v.split('-')[0].strip() for k,v in scns.institution_map().items()}
want={'MAR2011','MAR3023'}
sec=collections.defaultdict(lambda: collections.defaultdict(set))
ids=set()
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status']!='A' or r['prefix'] not in ('MAR','MKA'): continue
    inst=imap.get(r['institution'].lstrip('0'))
    if not inst or not scns.is_public(inst): continue
    cid=(r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip()
    ids.add(cid)
    if cid in want: sec[cid][scns.sector_of(inst)].add(inst)
for c in sorted(want):
    print(c, {k:len(v) for k,v in sorted(sec[c].items())})
    for k in sorted(sec[c]): print('   ',k,' '.join(sorted(sec[c][k])))
open('scratchpad/marids.txt','w').write('\n'.join(sorted(ids)))
print('ids',len(ids))
