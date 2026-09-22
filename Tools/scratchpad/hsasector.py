# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0,'scratchpad'); import scns
imap={k:v.split('-')[0].strip() for k,v in scns.institution_map().items()}
sec=collections.defaultdict(set)
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status']!='A': continue
    if r['prefix']!='HSA': continue
    if r['level'] not in '34': continue
    inst=imap.get(r['institution'].lstrip('0'))
    if not inst or not scns.is_public(inst): continue
    sec[scns.sector_of(inst)].add(inst)
for k in sorted(sec): print('%-6s %2d  %s' % (k, len(sec[k]), ' '.join(sorted(sec[k]))))
