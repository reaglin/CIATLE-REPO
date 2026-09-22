# -*- coding: utf-8 -*-
"""Find catalog courses that sit under no taxonomy node (unreachable by browsing)."""
import json, io, re, collections, sys, requests

BASE = 'https://floridacourserepo.com'

tree = json.load(io.open('scratchpad/tax.json', encoding='utf-8'))['data']['tree']
known = set()
for n in tree:
    for c in (n.get('children') or []):
        known.add(c['key'].upper())
print('prefixes in taxonomy tree:', len(known))

ids = []
page = 1
while True:
    r = requests.get(BASE + '/api/v1/courses/catalog',
                     params={'pageSize': 1000, 'page': page}, timeout=120)
    d = r.json()['data']
    ids += [i['courseId'] for i in d['items']]
    if page >= d['totalPages']:
        break
    page += 1
    if page % 10 == 0:
        print('  page', page, len(ids), flush=True)

print('catalog ids fetched:', len(ids))
io.open('scratchpad/catalog_ids.txt', 'w', encoding='utf-8').write('\n'.join(ids))

def pfx(cid):
    m = re.match(r'^([A-Z]{3})', cid.upper())
    return m.group(1) if m else '?'

bad = [c for c in ids if pfx(c) not in known]
print()
print('courses whose PREFIX is not in the taxonomy tree:', len(bad))
cnt = collections.Counter(pfx(c) for c in bad)
for p, n in cnt.most_common(40):
    ex = [c for c in bad if pfx(c) == p][:4]
    print('  %-5s %5d   %s' % (p, n, ' '.join(ex)))
print()
print('distinct missing prefixes:', len(cnt))
