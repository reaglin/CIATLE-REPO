# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0,'scratchpad'); import scns
imap={k:v.split('-')[0].strip() for k,v in scns.institution_map().items()}
hit=collections.defaultdict(lambda:[set(),set()])
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status']!='A': continue
    t=(r.get('state_title') or '').upper()
    if 'PHLEBOTOM' not in t: continue
    inst=imap.get(r['institution'].lstrip('0'))
    if not inst or not scns.is_public(inst): continue
    cid=(r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip()
    hit[cid][0].add(inst); hit[cid][1].add(t)
for cid,(s,t) in sorted(hit.items(), key=lambda x:-len(x[1][0])):
    print('%-10s %3d  %s' % (cid, len(s), ' | '.join(sorted(t))[:80]))
