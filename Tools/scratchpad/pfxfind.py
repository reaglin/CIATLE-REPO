# -*- coding: utf-8 -*-
import sys, os, collections
sys.path.insert(0,'scratchpad')
import scns
FLAT=os.path.join('scratchpad','crslist.txt')
pats=[p.upper() for p in sys.argv[1:]]
hits=collections.defaultdict(collections.Counter)
for r in scns.parse_flatfile(FLAT):
    if r['status']!='A': continue
    t=(r.get('state_title') or r.get('inst_title') or '').upper()
    if any(p in t for p in pats):
        hits[r['prefix']][t]+=1
for p in sorted(hits, key=lambda k:-sum(hits[k].values()))[:12]:
    print('%-4s %4d  %s' % (p, sum(hits[p].values()), '; '.join(t for t,_ in hits[p].most_common(3))[:110]))
