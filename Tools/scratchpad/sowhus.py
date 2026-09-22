# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0,'scratchpad'); import scns
imap={k:v.split('-')[0].strip() for k,v in scns.institution_map().items()}
sec=collections.defaultdict(lambda: collections.defaultdict(set)); ids=collections.defaultdict(set)
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status']!='A' or r['prefix'] not in ('SOW','HUS'): continue
    inst=imap.get(r['institution'].lstrip('0'))
    if not inst or not scns.is_public(inst): continue
    cid=(r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip()
    sec[r['prefix']][scns.sector_of(inst)].add(inst)
    if int(r['level'])<=4: ids[r['prefix']].add(cid)
for p in ('SOW','HUS'):
    print(p, {k:len(v) for k,v in sorted(sec[p].items())}, ' undergrad ids', len(ids[p]))
    for k in sorted(sec[p]): print('   ',k, ' '.join(sorted(sec[p][k])))
open('scratchpad/sowids.txt','w').write('\n'.join(sorted(i for p in ('SOW','HUS') for i in ids[p])))
