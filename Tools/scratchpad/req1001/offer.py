import json, sys
sys.path.insert(0, '.')
import scns
im = {int(k): v for k, v in json.load(open('inst_map.json', encoding='utf-8')).items()}
want = sys.argv[1].split(',')
prefixes = sorted({w[:3] for w in want})
for p in prefixes:
    for r in scns.parse_flatfile('crslist.txt', p):
        code = r['code'] + (r['lab'] if r['lab'] not in ('', ' ') else '')
        cid = r['prefix'] + r['level'] + r['century'] + r['decade'] + r['unit'] + r['lab'].strip()
        if not any(cid.startswith(w) for w in want):
            continue
        name = im.get(int(r['institution']), r['institution'])
        ic = name.split(' - ')[0]
        print('%-9s %-6s %-5s cr=%-5s ch=%-5s %-3s | %-45s | ST: %s | pub=%s' % (cid, ic, scns.sector_of(ic), r['credit'], r['clock_hours'], r['credit_type'], r['inst_title'][:45], r['state_title'][:60], scns.is_public(ic)))
