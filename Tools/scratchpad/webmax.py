# -*- coding: utf-8 -*-
import sys, collections, re
sys.path.insert(0,'scratchpad'); import scns
imap={k:v.split('-')[0].strip() for k,v in scns.institution_map().items()}
car=collections.defaultdict(set); ttl={}; pref=collections.Counter()
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status']!='A': continue
    t=(r.get('state_title') or '').upper()
    if not re.search(r'\bWEB\b|USER EXPERIENCE|USER INTERFACE|HUMAN-COMPUTER|HUMAN COMPUTER', t): continue
    inst=imap.get(r['institution'].lstrip('0'))
    if not inst or not scns.is_public(inst): continue
    cid=(r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip()
    car[cid].add(inst); ttl.setdefault(cid,t); pref[r['prefix']]+=0
for cid,s in sorted(car.items(), key=lambda x:-len(x[1]))[:12]:
    print('%-10s %2d  %s' % (cid, len(s), ttl[cid][:52]))
print()
print('distinct web/UX course ids:', len(car), 'across prefixes:', len({c[:3] for c in car}))
