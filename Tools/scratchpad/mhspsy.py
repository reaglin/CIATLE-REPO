# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0,'scratchpad'); import scns
imap={k:v.split('-')[0].strip() for k,v in scns.institution_map().items()}
lev=collections.defaultdict(lambda: collections.defaultdict(set)); insts=collections.defaultdict(lambda: collections.defaultdict(set)); ids=collections.defaultdict(set)
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status']!='A' or r['prefix'] not in ('MHS','PSY','CLP','SOP','DEP','EXP','PPE','INP'): continue
    inst=imap.get(r['institution'].lstrip('0'))
    if not inst or not scns.is_public(inst): continue
    cid=(r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip()
    band='grad' if r['level'] in '56' else 'ug'
    lev[r['prefix']][band].add(cid); insts[r['prefix']][scns.sector_of(inst)].add(inst)
    if int(r['level'])<=4: ids[r['prefix']].add(cid)
for p in ('MHS','PSY','CLP','SOP','DEP','EXP','PPE','INP'):
    print('%-4s ug=%-4d grad=%-4d  sectors=%s' % (p, len(lev[p]['ug']), len(lev[p]['grad']), {k:len(v) for k,v in sorted(insts[p].items())}))
open('scratchpad/psyids.txt','w').write('\n'.join(sorted(i for p in ids for i in ids[p])))
print('undergrad ids total', sum(len(v) for v in ids.values()))
