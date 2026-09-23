# -*- coding: utf-8 -*-
import sys, os, collections
sys.path.insert(0,'scratchpad')
import scns
FLAT=os.path.join('scratchpad','crslist.txt')
def cid(r): return (r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip().upper()
def code_of(n): return n.split('-')[0].strip()
imap={k:code_of(v) for k,v in scns.institution_map().items()}
WANT={'OCB1000','OCB2000','OCB4633','BSC1311','BSC3312','OCE1001','OCE2001','OCE1001C','OCE3008',
      'ZOO4454','ZOO4454C','ZOO4485','ZOO4407','ZOO4405','PCB4315','ZOO3205C','OCB2000L','OCB3043'}
by=collections.defaultdict(dict); sec={}
for r in scns.parse_flatfile(FLAT):
    k=cid(r)
    if k not in WANT: continue
    c=imap.get(r['institution'].lstrip('0') or r['institution'])
    if not c or not scns.is_public(c): continue
    by[k][c]=r.get('credit'); sec[c]=scns.sector_of(c)
intro=['OCB1000','OCB2000','BSC1311','BSC3312','OCB4633']
print('THE INTRODUCTORY MARINE BIOLOGY COURSE, by number:')
u=set()
for k in intro:
    s=set(by.get(k,{})); u|=s
    print('  %-9s %2d  %s'%(k,len(s),' '.join(sorted(s))))
print('  union:',len(u),'| any institution carrying 2+:',
      {c:n for c,n in collections.Counter(c for k in intro for c in by.get(k,{})).items() if n>1})
print()
for a,b in [('OCE1001','OCE2001'),('ZOO4454','ZOO4454C')]:
    A,B=set(by.get(a,{})),set(by.get(b,{}))
    print('%-9s %2d %s'%(a,len(A),' '.join(sorted(A))[:64]))
    print('%-9s %2d %s'%(b,len(B),' '.join(sorted(B))[:64]))
    print('   overlap:',sorted(A&B) or 'NONE'); print()
