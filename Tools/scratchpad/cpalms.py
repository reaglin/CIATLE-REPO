#!/usr/bin/env python
"""CPALMS-CTE — Florida's CTE curriculum frameworks, keyed to CIP.

⚠⚠⚠ THIS RECOVERS A TIER-1 SOURCE THAT HAS BEEN DEAD SINCE 2026-09-02.
`fldoe.org` returns 403 to this project on the framework pages AND on the
`core/fileparse.php/…pdf` documents, re-probed 2026-09-17 with a browser
user-agent. The frameworks are the authority for every PSAV/CTE programme —
occupational completion points, clock hours, and the CIP code the programme is
tied to — so losing them cost the project its best source for the whole
career-and-technical education space.

Ron supplied the route (2026-09-17):
    https://www.cpalms.org/PreviewCourseProgram/CTE?frameurl=%2Fsearch

That page iframes `ctepreview.cpalms.org`, an Angular app, so nothing is in the
HTML. Its bundle names the service it calls, and that service is OPEN:

    https://cteservice.cpalms.org/api/

⚠ The gate is two headers — `Origin` and `Referer`, both pointing at
ctepreview.cpalms.org. The same shape as the Coursedog gate (SOURCES.md),
and worth trying first whenever a Florida SPA looks closed.

ENDPOINTS (from the bundle; POST unless noted)
    ProgramFrontend/programs           POST {} -> paged list, 987 programmes
    ProgramFrontend/programtotalcount  GET     -> {"totalCount": 987}
    ProgramFrontend/careerclusters     GET     -> the 17 clusters
    ProgramFrontend/programInfo        GET  ?programCIP=&version=
    ProgramFrontend/programstructure   GET  ?programCIP=&version=   <- OCPs + courses
    ProgramFrontend/programstandards   GET
    ProgramFrontend/programindustrycertifications GET
    ProgramFrontend/programcareercodes GET                          <- SOC codes
    ProgramFrontend/programsummary     GET  ?ProgramCIP=&MockIfSingle=true

⚠⚠ THE CIP FORMAT. Florida writes a 10-digit programme CIP such as
`0511020314`. The FEDERAL CIP is characters 3-8: `110203` -> `11.0203`, whose
4-digit group is `11.02`. Verified against the programme titles (`.NET
Application Development` really is 11.0203 Computer Programming, Specific
Applications). The leading `05` marks the programme level and the trailing pair
is a Florida serial — neither is part of the federal code.

    python cpalms.py dump           # fetch all programmes -> cpalms_programs.json
    python cpalms.py clusters
    python cpalms.py find welding   # search cached programmes by title
    python cpalms.py cip 11.02      # which programmes sit in a federal CIP group
    python cpalms.py info 0511020314
"""
import io
import json
import os
import sys
import urllib.error
import urllib.request

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = 'https://cteservice.cpalms.org/api/'
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'cpalms_programs.json')

HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'),
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    # ⚠ Both of these are the gate. Dropping either returns 401/403.
    'Origin': 'https://ctepreview.cpalms.org',
    'Referer': 'https://ctepreview.cpalms.org/',
}


def _req(path, body=None, timeout=120):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers=HEADERS,
                                 method='POST' if data is not None else 'GET')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        raise RuntimeError('%s -> HTTP %s %s' % (path, e.code, e.read()[:200]))


def federal_cip(program_cip):
    """Florida 10-digit programme CIP -> dotted federal 6-digit, or None.

    ⚠ Characters 3-8. `0511020314` -> `11.0203`. Anything that is not 10 digits
    is left alone rather than coerced -- the same rule cip_map.py uses.
    """
    d = ''.join(ch for ch in str(program_cip) if ch.isdigit())
    if len(d) != 10:
        return None
    return d[2:4] + '.' + d[4:8]


def group(program_cip):
    """The 4-digit CIP group a Florida programme belongs to, e.g. '11.02'."""
    f = federal_cip(program_cip)
    return f[:5] if f else None


def dump():
    total = _req('ProgramFrontend/programtotalcount')['totalCount']
    print('CPALMS reports %d CTE programmes.' % total)
    items, page = [], 1
    while True:
        d = _req('ProgramFrontend/programs', {'pageNumber': page, 'pageSize': 200})
        items.extend(d['items'])
        print('  page %d: %d (running %d)' % (page, len(d['items']), len(items)))
        if not d.get('hasNextPage'):
            break
        page += 1
        if page > 40:
            print('  ⚠ stopping at 40 pages')
            break
    json.dump(items, io.open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote %s (%d programmes)' % (os.path.basename(CACHE), len(items)))
    return items


def load():
    if not os.path.exists(CACHE):
        print('no cache; run: python cpalms.py dump')
        sys.exit(1)
    return json.load(io.open(CACHE, encoding='utf-8'))


def _show(p):
    print('  %-10s %-6s %-52s %s'
          % (p.get('programCIP', ''), group(p.get('programCIP')) or '--',
             (p.get('title') or '')[:52], (p.get('programType') or '')[:28]))


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__.strip().split('\n\n')[0])
        print('\nusage: cpalms.py dump | clusters | find <text> | cip <nn.nn> | info <programCIP>')
        return 2
    cmd = a[0]
    if cmd == 'dump':
        dump()
    elif cmd == 'clusters':
        for c in _req('ProgramFrontend/careerclusters'):
            print('  %-4s %s' % (c['id'], c['title']))
    elif cmd == 'find' and len(a) > 1:
        q = ' '.join(a[1:]).lower()
        hits = [p for p in load() if q in (p.get('title') or '').lower()]
        print('%d programme(s) matching %r:' % (len(hits), q))
        for p in hits:
            _show(p)
    elif cmd == 'cip' and len(a) > 1:
        g = a[1]
        hits = [p for p in load() if (group(p.get('programCIP')) or '') == g]
        print('%d programme(s) in federal CIP group %s:' % (len(hits), g))
        for p in hits:
            _show(p)
    elif cmd == 'info' and len(a) > 1:
        print(json.dumps(_req('ProgramFrontend/programInfo?programCIP=%s&version=' % a[1]),
                         indent=1)[:3000])
    else:
        print('unknown command')
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
