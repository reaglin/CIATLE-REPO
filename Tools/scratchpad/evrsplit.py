# -*- coding: utf-8 -*-
import sys, os, collections
sys.path.insert(0,'scratchpad')
import scns
FLAT=os.path.join('scratchpad','crslist.txt')
def cid(r): return (r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip().upper()
def code_of(n): return n.split('-')[0].strip()
imap={k:code_of(v) for k,v in scns.institution_map().items()}
WANT={'EVR1001','EVR1001C','EVR1001L','EVR2001','EVR2001L','EVR2861','EVR2630','EVR1328'}
by=collections.defaultdict(dict); sec={}
for r in scns.parse_flatfile(FLAT):
    k=cid(r)
    if k not in WANT and r['prefix']!='EVR': continue
    c=imap.get(r['institution'].lstrip('0') or r['institution'])
    if not c or not scns.is_public(c): continue
    if k in WANT:
        by[k][c]=r.get('credit'); sec[c]=scns.sector_of(c)
for k in ['EVR1001','EVR1001C','EVR1001L','EVR2001','EVR2001L']:
    s=set(by.get(k,{}))
    bysec=collections.Counter(sec.get(c) for c in s)
    print('%-9s %2d  %-28s %s'%(k,len(s),dict(bysec),' '.join(sorted(s))))
A,C,L,T=set(by.get('EVR1001',{})),set(by.get('EVR1001C',{})),set(by.get('EVR1001L',{})),set(by.get('EVR2001',{}))
print()
print('lecture+lab pairs (carry BOTH 1001 and 1001L):',sorted(A&L))
print('1001 and 1001C overlap :',sorted(A&C) or 'NONE')
print('1001 and 2001 overlap  :',sorted(A&T) or 'NONE')
print('1001C and 2001 overlap :',sorted(C&T) or 'NONE')
print('union of all four      :',len(A|C|L|T))
print()
print('credits EVR1001 :',sorted(set(by['EVR1001'].values())))
print('credits EVR1001C:',sorted(set(by['EVR1001C'].values())))
print('credits EVR2001 :',sorted(set(by['EVR2001'].values())))
