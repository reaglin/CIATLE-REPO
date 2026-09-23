# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0, 'scratchpad')
import scns
imap = {k: v.split('-')[0].strip() for k, v in scns.institution_map().items()}
pub = {k for k, c in imap.items() if scns.is_public(c)}
per = collections.defaultdict(set); t = {}; st = {}; hrs = collections.defaultdict(collections.Counter)
KEYS = ('TRUCK', 'TRACTOR', 'COMMERCIAL VEHICLE', 'CDL', 'COMMERCIAL DRIV', 'MOTOR COACH', 'BUS DRIV')
for r in scns.parse_flatfile('scratchpad/crslist.txt'):
    if r['status'] != 'A':
        continue
    ti = ((r.get('inst_title') or '') + ' | ' + (r.get('state_title') or '')).upper()
    if not any(k in ti for k in KEYS):
        continue
    inst = r['institution'].lstrip('0')
    if inst not in pub:
        continue
    cid = (r['prefix'] + r['level'] + r['century'] + r['decade'] + r['unit'] + (r['lab'] or '')).strip()
    per[cid].add(imap[inst]); t.setdefault(cid, (r.get('inst_title') or '').strip())
    st.setdefault(cid, (r.get('state_title') or '').strip())
    hrs[cid][str(r.get('clock_hours') or '').strip() + '/' + str(r.get('credit') or '').strip()] += 1
for c in sorted(per, key=lambda c: -len(per[c])):
    print('%-9s %2d %-34s | %-52s | %s | %s' % (c, len(per[c]), t[c][:34], st[c][:52], dict(hrs[c]),
                                               ' '.join(sorted(per[c]))[:90]))
