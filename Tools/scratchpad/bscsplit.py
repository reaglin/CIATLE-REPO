# -*- coding: utf-8 -*-
import sys, os, collections
sys.path.insert(0,'scratchpad')
import scns
FLAT=os.path.join('scratchpad','crslist.txt')
def cid(r): return (r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip().upper()
def code_of(n): return n.split('-')[0].strip()
imap={k:code_of(v) for k,v in scns.institution_map().items()}
WANT={'BSC1010','BSC2010','BSC1010L','BSC2010L','BSC1010C','BSC2010C','BSC1011','BSC2011','BSC1011L','BSC2011L',
      'BSC2085','BSC2085C','MCB2010','MCB2010C','MCB3020','PCB3063','PCB3023','PCB4674','BSC3312','ZOO3713C','BOT3015'}
by=collections.defaultdict(dict); sec={}
for r in scns.parse_flatfile(FLAT):
    k=cid(r)
    if k not in WANT: continue
    c=imap.get(r['institution'].lstrip('0') or r['institution'])
    if not c or not scns.is_public(c): continue
    by[k][c]=r.get('credit'); sec[c]=scns.sector_of(c)
for a,b in [('BSC1010','BSC2010'),('BSC1010L','BSC2010L'),('BSC1011','BSC2011'),('MCB2010','MCB2010C')]:
    A,B=set(by.get(a,{})),set(by.get(b,{}))
    print('%-9s %2d [%s] %s'%(a,len(A),dict(collections.Counter(sec[c] for c in A)),' '.join(sorted(A))[:76]))
    print('%-9s %2d [%s] %s'%(b,len(B),dict(collections.Counter(sec[c] for c in B)),' '.join(sorted(B))[:76]))
    print('    overlap:',sorted(A&B) or 'NONE','| union:',len(A|B)); print()
print('SUS on BSC1010:',sorted(c for c in by.get('BSC1010',{}) if sec[c]=='SUS'))
print('SUS on BSC2010:',sorted(c for c in by.get('BSC2010',{}) if sec[c]=='SUS'))
print()
for k in sorted(WANT):
    if k in by: print('%-9s %2d  credits %s'%(k,len(by[k]),sorted(set(by[k].values()))))
