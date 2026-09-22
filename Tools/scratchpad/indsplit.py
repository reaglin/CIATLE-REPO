# -*- coding: utf-8 -*-
import sys, os, collections
sys.path.insert(0,'scratchpad')
import scns
FLAT=os.path.join('scratchpad','crslist.txt')
def cid(r): return (r['prefix']+r['level']+r['century']+r['decade']+r['unit']+(r['lab'] or '')).strip().upper()
def code_of(n): return n.split('-')[0].strip()
imap={k:code_of(v) for k,v in scns.institution_map().items()}
by=collections.defaultdict(dict); title={}
for r in scns.parse_flatfile(FLAT):
    if r['prefix']!='IND': continue
    c=imap.get(r['institution'].lstrip('0') or r['institution'])
    if not c or not scns.is_public(c): continue
    by[cid(r)][c]=r.get('credit')
    title.setdefault(cid(r), (r.get('state_title') or '').strip())
live=[k for k in by if k[3] in '1234' and not k[4:7].startswith('9')]
single=[k for k in live if len(by[k])==1]
print('live undergrad IND ids:',len(live),' single-carrier:',len(single),'(%d%%)'%(100*len(single)/len(live)))
print()
pairs=[('IND1100','IND2100'),('IND1130','IND2130'),('IND1020','IND1020C'),
       ('IND1420','IND1423'),('IND1420','IND2420'),('IND1200','IND2200')]
for a,b in pairs:
    A=set(by.get(a,{})); B=set(by.get(b,{}))
    if not A and not B: continue
    print('%-9s %-42s %d  %s'%(a,title.get(a,'')[:42],len(A),' '.join(sorted(A))))
    print('%-9s %-42s %d  %s'%(b,title.get(b,'')[:42],len(B),' '.join(sorted(B))))
    print('   overlap:',sorted(A&B) or 'NONE'); print()
