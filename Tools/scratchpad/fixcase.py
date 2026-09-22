# -*- coding: utf-8 -*-
"""Re-case acronyms that got title-cased into words in stored course titles.

Title-only update: replaceOfferings is FALSE so nothing else is touched.
"""
import io, json, os, re, sys, requests

try:
    from dotenv import load_dotenv
    load_dotenv('.env')
except ImportError:
    pass

BASE = os.environ.get('REPO_BASE_URL', 'https://floridacourserepo.com').rstrip('/')
FIX = {'Sql': 'SQL', 'Mysql': 'MySQL', 'Nosql': 'NoSQL', 'Pl/sql': 'PL/SQL',
       'Etl': 'ETL', 'Olap': 'OLAP', 'Dba': 'DBA'}

bad = json.load(io.open('scratchpad/badtitles.json', encoding='utf-8'))

edits = {}
for cid, title in bad.items():
    new = title
    for a, b in FIX.items():
        new = re.sub(r'(?<![A-Za-z])%s(?![a-z])' % re.escape(a), b, new)
    if new != title:
        edits[cid] = (title, new)

print('%d title(s) to correct' % len(edits))
for cid, (o, n) in sorted(edits.items()):
    print('  %-9s %-46s -> %s' % (cid, o[:46], n))

if '--push' not in sys.argv:
    print('\ndry run -- pass --push')
    raise SystemExit

s = requests.Session()
tok = s.post('%s/api/v1/auth/login' % BASE,
             json={'email': os.environ['REPO_ADMIN_EMAIL'],
                   'password': os.environ['REPO_ADMIN_PASSWORD']}, timeout=20)
tok.raise_for_status()
h = {'Authorization': 'Bearer %s' % tok.json()['data']['accessToken']}

ok = fail = 0
for cid, (o, n) in sorted(edits.items()):
    r = s.put('%s/api/v1/courses/%s' % (BASE, cid),
              json={'courseId': cid, 'title': n, 'replaceOfferings': False},
              headers=h, timeout=60)
    if r.status_code == 200 and r.json().get('success'):
        ok += 1
    else:
        fail += 1
        print('  FAILED %s  HTTP %s  %s' % (cid, r.status_code, r.text[:160]))
print('updated %d, failed %d' % (ok, fail))
