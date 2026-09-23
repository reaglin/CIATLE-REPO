# -*- coding: utf-8 -*-
import sys, os, collections
sys.path.insert(0,'scratchpad')
import scns
FLAT=os.path.join('scratchpad','crslist.txt')
def cid(r): return (r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip().upper()
def code_of(n): return n.split('-')[0].strip()
imap={k:code_of(v) for k,v in scns.institution_map().items()}
PFX={'EVR','GLY','OCE','SWS','PCB','EVS','GIS','CHM','STA','BSC','MET'}
hits=collections.defaultdict(set); title={}
for r in scns.parse_flatfile(FLAT):
    if r['prefix'] not in PFX: continue
    c=imap.get(r['institution'].lstrip('0') or r['institution'])
    if not c or not scns.is_public(c): continue
    k=cid(r)
    if k[3] not in '1234': continue
    if k[4:7].startswith('9'): continue
    hits[k].add(c); title.setdefault(k,(r.get('state_title') or '').strip())
KEY=('ECOLOG','WETLAND','HYDROLOG','WATER','SOIL','GEOGRAPHIC INFORMATION','REMOTE SENSING',
     'ENVIRONMENTAL','POLLUT','TOXICOL','SUSTAIN','CLIMAT','CONSERVATION','OCEANOG','GEOLOG','STATISTIC')
rows=[(len(v),k,title[k]) for k,v in hits.items() if any(x in title[k].upper() for x in KEY)]
for n,k,t in sorted(rows,reverse=True)[:34]:
    print('%-9s %2d  %-46s %s'%(k,n,t[:46],' '.join(sorted(hits[k]))[:58]))
