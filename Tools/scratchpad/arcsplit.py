# -*- coding: utf-8 -*-
import sys, os, collections
sys.path.insert(0,'scratchpad')
import scns
FLAT=os.path.join('scratchpad','crslist.txt')
def cid(r): return (r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip().upper()
def code_of(n): return n.split('-')[0].strip()
imap={k:code_of(v) for k,v in scns.institution_map().items()}
by=collections.defaultdict(dict)
for r in scns.parse_flatfile(FLAT):
    if r['prefix']!='ARC': continue
    c=imap.get(r['institution'].lstrip('0') or r['institution'])
    if not c or not scns.is_public(c): continue
    by[cid(r)][c]=(r.get('credit'),(r.get('inst_title') or '').strip())
pairs=[('ARC1301','ARC1301C'),('ARC1302','ARC1302C'),('ARC2303','ARC2303C'),('ARC2304','ARC2304C'),
       ('ARC1701','ARC2701'),('ARC1702','ARC2702')]
for a,b in pairs:
    A=set(by.get(a,{})); B=set(by.get(b,{}))
    print('%-9s %2d  %s'%(a,len(A),' '.join(sorted(A))))
    print('%-9s %2d  %s'%(b,len(B),' '.join(sorted(B))))
    print('   overlap:',sorted(A&B) or 'NONE'); print()
for c in ['ARC1301','ARC1301C','ARC2304','ARC2304C','ARC2461','ARC3463']:
    print(c, sorted(set((k,v[0]) for k,v in by.get(c,{}).items())))
