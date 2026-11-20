import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
import scns
imap = json.load(open(os.path.join(os.path.dirname(__file__), 'inst_map.json'), encoding='utf-8'))
want = sys.argv[1:]
pfx = {w[:3] for w in want}
for p in sorted(pfx):
    for r in scns.parse_flatfile(os.path.join(os.path.dirname(__file__), 'crslist.txt'), prefix=p):
        base = r['code'][:7]
        for w in want:
            if r['code'] == w or (r['code'][3:7][1:] == w[4:7] and r['code'][:3] == w[:3]):
                key = str(int(r['institution']))
                name = imap.get(key, key)
                code = name.split('-')[0].strip()
                print(w, '|', r['code'], '|', name, '|', scns.sector_of(code), '|', r['inst_title'], '|', r['credit'], '|', r['clock_hours'], '|', r['state_title'], '|', r['dt_discontinued'])
