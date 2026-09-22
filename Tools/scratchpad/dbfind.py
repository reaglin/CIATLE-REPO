# -*- coding: utf-8 -*-
import sys, os, collections
sys.path.insert(0,'scratchpad')
import scns
FLAT=os.path.join('scratchpad','crslist.txt')
def cid(r): return (r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip().upper()
def code_of(n): return n.split('-')[0].strip()
imap={k:code_of(v) for k,v in scns.institution_map().items()}
hits=collections.defaultdict(set); title={}
KEY=('DATABASE','DATA BASE','SQL','DATA WAREHOUS','DATA MANAGEMENT','BIG DATA','DATA MODEL','DATA MINING','CLOUD')
for r in scns.parse_flatfile(FLAT):
    c=imap.get(r['institution'].lstrip('0') or r['institution'])
    if not c or not scns.is_public(c): continue
    st=(r.get('state_title') or '').upper()
    it=(r.get('inst_title') or '').upper()
    if any(k in st or k in it for k in KEY):
        k=cid(r)
        if k[3] not in '1234': continue
        hits[k].add(c); title.setdefault(k,(r.get('state_title') or '').strip())
for k,v in sorted(hits.items(), key=lambda x:-len(x[1]))[:30]:
    print('%-9s %2d  %-44s %s'%(k,len(v),title[k][:44],' '.join(sorted(v))[:70]))
