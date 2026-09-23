# -*- coding: utf-8 -*-
import sys, os, collections
sys.path.insert(0,'scratchpad')
import scns
FLAT=os.path.join('scratchpad','crslist.txt')
def cid(r): return (r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip().upper()
def code_of(n): return n.split('-')[0].strip()
imap={k:code_of(v) for k,v in scns.institution_map().items()}
WANT={'CHM1045','CHM2045','CHM1045L','CHM2045L','CHM1046','CHM2046','CHM1046L','CHM2046L',
      'CHM2210','CHM2210C','CHM2210L','CHM1025','CHM1032','CHM1020','CHM3120','CHM4130','CHM3610','CHM4410'}
by=collections.defaultdict(dict); sec={}
for r in scns.parse_flatfile(FLAT):
    k=cid(r)
    if k not in WANT: continue
    c=imap.get(r['institution'].lstrip('0') or r['institution'])
    if not c or not scns.is_public(c): continue
    by[k][c]=r.get('credit'); sec[c]=scns.sector_of(c)
for a,b in [('CHM1045','CHM2045'),('CHM1045L','CHM2045L'),('CHM1046','CHM2046')]:
    A,B=set(by.get(a,{})),set(by.get(b,{}))
    print('%-9s %2d [%s]'%(a,len(A),dict(collections.Counter(sec[c] for c in A))))
    print('   ',' '.join(sorted(A)))
    print('%-9s %2d [%s]'%(b,len(B),dict(collections.Counter(sec[c] for c in B))))
    print('   ',' '.join(sorted(B)))
    print('    overlap:',sorted(A&B) or 'NONE','| union:',len(A|B)); print()
print('SUS on CHM1045:',sorted(c for c in by['CHM1045'] if sec[c]=='SUS'))
print('SUS on CHM2045:',sorted(c for c in by['CHM2045'] if sec[c]=='SUS'))
print()
for k in sorted(WANT):
    if k in by: print('%-9s %2d  credits %s'%(k,len(by[k]),sorted(set(by[k].values()))))
