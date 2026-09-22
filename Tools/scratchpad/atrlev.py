# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0,'scratchpad'); import scns
imap={k:v.split('-')[0].strip() for k,v in scns.institution_map().items()}
c=collections.defaultdict(set)
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status']!='A' or r['prefix']!='ATR': continue
    inst=imap.get(r['institution'].lstrip('0'))
    if not inst or not scns.is_public(inst): continue
    cid=(r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip()
    c[cid].add(inst)
ug=[k for k in c if k[3] in '01234']; gr=[k for k in c if k[3] in '56']
print('ATR ids: undergrad %d, graduate %d' % (len(ug),len(gr)))
big=[k for k,v in c.items() if len(v)>=2]
print('>=2 carriers: %d total, %d graduate, undergrad: %s' % (len(big), len([k for k in big if k[3] in '56']), sorted(k for k in big if k[3] in '01234')))
