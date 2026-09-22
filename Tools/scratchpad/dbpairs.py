# -*- coding: utf-8 -*-
import sys, os, collections
sys.path.insert(0,'scratchpad')
import scns
FLAT=os.path.join('scratchpad','crslist.txt')
def cid(r): return (r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip().upper()
def code_of(n): return n.split('-')[0].strip()
imap={k:code_of(v) for k,v in scns.institution_map().items()}
WANT={'COP3703','COP4703','COP3710','COP4710','ISM3212','ISM4212','CTS4408','COP2700','CGS1540',
      'CTS2433','CTS2445','CTS2441','CTS2442','CIS4368','CAP4770','CAP4774','CGS2545C','CTS2450'}
by=collections.defaultdict(dict); title={}
for r in scns.parse_flatfile(FLAT):
    k=cid(r)
    if k not in WANT: continue
    c=imap.get(r['institution'].lstrip('0') or r['institution'])
    if not c or not scns.is_public(c): continue
    by[k][c]=r.get('credit'); title.setdefault(k,(r.get('state_title') or '').strip())
core=['COP3703','COP4703','COP3710','COP4710','ISM3212','ISM4212','CTS4408']
allc=set()
print('THE UPPER-DIVISION DATABASE COURSE, by number:')
for k in core:
    s=set(by.get(k,{})); allc|=s
    print('  %-8s %-40s %d  %s'%(k,title.get(k,'')[:40],len(s),' '.join(sorted(s))))
print('  union of institutions:',len(allc))
print()
dup=collections.Counter()
for k in core:
    for c in by.get(k,{}): dup[c]+=1
print('institutions carrying MORE THAN ONE of the seven:',{c:n for c,n in dup.items() if n>1})
print()
for k in sorted(WANT):
    if k in by: print('%-9s %2d carriers  credits %s'%(k,len(by[k]),sorted(set(by[k].values()))))
