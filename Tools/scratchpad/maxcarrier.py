# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0,'scratchpad'); import scns
imap={k:v.split('-')[0].strip() for k,v in scns.institution_map().items()}
c=collections.defaultdict(set); t={}
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status']!='A': continue
    inst=imap.get(r['institution'].lstrip('0'))
    if not inst or not scns.is_public(inst): continue
    cid=(r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip()
    c[cid].add(inst); t.setdefault(cid,(r.get('state_title') or '').strip())
for cid,s in sorted(c.items(), key=lambda x:-len(x[1]))[:15]:
    print('%-10s %3d  %s' % (cid, len(s), t[cid][:55]))
