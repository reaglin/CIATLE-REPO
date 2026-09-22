# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0,'scratchpad'); import scns
imap={k:v.split('-')[0].strip() for k,v in scns.institution_map().items()}
lev=collections.defaultdict(lambda: collections.defaultdict(set))
ids=collections.defaultdict(set)
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status']!='A': continue
    if r['prefix'] not in ('PHC','HSC'): continue
    inst=imap.get(r['institution'].lstrip('0'))
    if not inst or not scns.is_public(inst): continue
    cid=(r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip()
    band = 'grad(5-6)' if r['level'] in '56' else ('upper(3-4)' if r['level'] in '34' else 'lower(0-2)')
    lev[r['prefix']][band].add(cid)
    ids[r['prefix']].add(cid)
for p in ('PHC','HSC'):
    print(p, {k:len(v) for k,v in sorted(lev[p].items())}, 'total', len(ids[p]))
# HSC4500 sector
sec=set()
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status']!='A': continue
    cid=(r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip()
    if cid!='HSC4500': continue
    inst=imap.get(r['institution'].lstrip('0'))
    if inst and scns.is_public(inst): sec.add((scns.sector_of(inst), inst))
print('HSC4500:', sorted(sec))
open('scratchpad/phcids.txt','w').write('\n'.join(sorted(i for p in ('PHC','HSC') for i in ids[p] if i[3] in '01234')))
