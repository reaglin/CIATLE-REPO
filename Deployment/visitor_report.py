#!/usr/bin/env python3
"""Visitor report for floridacourserepo.com, read from Nginx access logs.

Nginx writes one line per request in its default "combined" format. This script counts:

  * visitors     -- distinct people, approximated as a distinct (IP address, browser) pair.
                    A visitor is counted once per day in the daily table, and once in the
                    period total however many days they came back.
  * page views   -- successful (200/304) GETs of a public page. Not counted: images, CSS
                    and script files, the API, /admin, and every request from a crawler,
                    bot, monitoring service or script (our own tools included).

IP addresses are only used in memory, as a hash, to tell visitors apart. None are written
to the report.

USAGE
    python visitor_report.py access.log [more logs...] [--out report.md] [--days 30 | --month 2026-11]
    zcat -f access.log* | python3 visitor_report.py -     # '-' reads the log from standard input

Normally run through visitor-report.ps1, which runs it on the server, so only the report travels.
"""
import argparse
import array
import collections
import datetime
import hashlib
import io
import re
import sys
from urllib.parse import urlsplit

SITE_HOSTS = ('floridacourserepo.com', 'www.floridacourserepo.com')

LINE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+)[^"]*" (?P<status>\d{3}) \S+ '
    r'"(?P<ref>[^"]*)" "(?P<ua>[^"]*)"')

BOT = re.compile(
    r'bot|crawl|spider|slurp|scrap|fetch|curl|wget|python|httpclient|http-client|okhttp|'
    r'java/|go-http|libwww|axios|node-fetch|powershell|headless|phantom|lighthouse|'
    r'facebookexternalhit|preview|monitor|uptime|pingdom|semrush|ahrefs|mj12|dotbot|'
    r'bytespider|gptbot|chatgpt-user|oai-searchbot|claude|anthropic|ccbot|perplexity|'
    r'dataforseo|petalbot|yandex|baidu|zgrab|masscan|nmap|nikto|censys|expanse|scan',
    re.I)

STATIC = re.compile(
    r'\.(css|js|map|png|jpe?g|gif|svg|ico|webp|avif|woff2?|ttf|eot|txt|xml|json|zip|pdf|'
    r'php|asp|aspx|env|git|bak|sql|ini|cgi)$', re.I)

SECTIONS = [
    (re.compile(r'^/$'), 'Home page'),
    (re.compile(r'^/browse'), 'Browse (subject tree)'),
    (re.compile(r'^/courses/[^/]+/guide$'), 'Curriculum guides'),
    (re.compile(r'^/courses/[^/]+/resources$'), 'Course resources'),
    (re.compile(r'^/courses/[^/]+$'), 'Course pages'),
    (re.compile(r'^/careers'), 'Career paths'),
    (re.compile(r'^/programs'), 'Programmes'),
    (re.compile(r'^/queue/'), 'Request queues'),
    (re.compile(r'^/request-guide'), 'Request a guide'),
    (re.compile(r'^/(modules|materials)/'), 'Modules and materials'),
    (re.compile(r'^/account/'), 'Accounts'),
]

COURSE = re.compile(r'^/courses/([A-Za-z]{3}\d{4}[A-Za-z]?(?:-[A-Za-z]{2,5})?)(?:/|$)')


def section_of(path):
    for rx, name in SECTIONS:
        if rx.search(path):
            return name
    return 'Other pages'


def visitor_id(ip, ua):
    """A 60-bit number from a hash of IP + browser: tells visitors apart without keeping the address."""
    return int(hashlib.sha256(('%s|%s' % (ip, ua)).encode('utf-8', 'replace')).hexdigest()[:15], 16)


def ref_domain(ref):
    if not ref or ref == '-':
        return None
    try:
        host = (urlsplit(ref).hostname or '').lower()
    except ValueError:
        return None
    if not host or host in SITE_HOSTS:
        return None
    return host[4:] if host.startswith('www.') else host


def open_log(p):
    """A log file as text; '-' is standard input (how visitor-report.ps1 feeds it on the server)."""
    if p == '-':
        return io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
    with open(p, 'rb') as probe:
        bom = probe.read(2)
    # Windows PowerShell 5.1 writes "> file" as UTF-16; PowerShell 7 as UTF-8.
    enc = 'utf-16' if bom in (b'\xff\xfe', b'\xfe\xff') else 'utf-8'
    return open(p, encoding=enc, errors='replace')


# A real browser fetches the page's stylesheet and scripts; most unannounced scrapers fetch only the HTML.
# A visitor (IP + browser) who fetched one of these in the period is "browser-confirmed".
ASSET = re.compile(r'^/(css/site\.css|js/site\.js|lib/bootstrap/)')


def parse(paths, days, month=None):
    """Read the logs once. Page views are kept as compact parallel arrays (millions of rows), so the
    figures can be worked out both for every visitor and for browser-confirmed visitors only.
    month: (first_day, last_day) to keep only that calendar month, or None."""
    cutoff = None
    if days:
        cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    r = {
        'lines': 0, 'unparsed': 0, 'bot_requests': 0, 'api_requests': 0,
        'bot_agents': collections.Counter(),
        'vid': array.array('q'), 'ts': array.array('q'), 'path': array.array('i'), 'ref': array.array('i'),
        'paths': [], 'refs': ['-', 'other'],      # ref 0: no referrer; 1: our own site or unreadable
        'confirmed': set(),
    }
    path_ids, ref_ids = {}, {'-': 0, 'other': 1}
    for p in paths:
        with open_log(p) as fh:
            for raw in fh:
                r['lines'] += 1
                m = LINE.match(raw)
                if not m:
                    r['unparsed'] += 1
                    continue
                try:
                    t = datetime.datetime.strptime(m['time'], '%d/%b/%Y:%H:%M:%S %z')
                except ValueError:
                    r['unparsed'] += 1
                    continue
                if cutoff and t < cutoff:
                    continue
                if month and not (month[0] <= t.date() <= month[1]):
                    continue
                ua = m['ua']
                path = m['path'].split('?', 1)[0].split('#', 1)[0]
                if path.startswith('/api/'):
                    r['api_requests'] += 1
                    continue
                if not ua or ua == '-' or BOT.search(ua):
                    r['bot_requests'] += 1
                    r['bot_agents'][ua[:60] or '(no user agent)'] += 1
                    continue
                if m['method'] != 'GET' or m['status'] not in ('200', '304'):
                    continue
                if ASSET.match(path):
                    r['confirmed'].add(visitor_id(m['ip'], ua))
                    continue
                if STATIC.search(path) or path.startswith(('/admin', '/lib/', '/css/', '/js/', '/_')):
                    continue
                if len(path) > 1:
                    path = path.rstrip('/')

                pid = path_ids.get(path)
                if pid is None:
                    pid = path_ids[path] = len(r['paths'])
                    r['paths'].append(path)
                ref = m['ref']
                if not ref or ref == '-':
                    rid = 0
                else:
                    dom = ref_domain(ref)
                    if dom is None:
                        rid = 1
                    else:
                        rid = ref_ids.get(dom)
                        if rid is None:
                            rid = ref_ids[dom] = len(r['refs'])
                            r['refs'].append(dom)
                # Days are the server log's own local days, as before.
                local = t.replace(tzinfo=None)
                r['vid'].append(visitor_id(m['ip'], ua))
                r['ts'].append(int((local - EPOCH).total_seconds()))
                r['path'].append(pid)
                r['ref'].append(rid)
    return r


EPOCH = datetime.datetime(1970, 1, 1)


def aggregate(r, keep=None, totals_only=False):
    """The report's figures from the page views in r, for every visitor or only those in keep.
    totals_only: just visitors and views by day and week (the comparison column), to save memory."""
    s = {
        'day_visitors': collections.defaultdict(set), 'day_views': collections.Counter(),
        'week_visitors': collections.defaultdict(set), 'week_views': collections.Counter(),
        'all_visitors': set(), 'views': 0,
        'section_views': collections.Counter(), 'section_visitors': collections.defaultdict(set),
        'page_views': collections.Counter(), 'page_visitors': collections.defaultdict(set),
        'course_visitors': collections.defaultdict(set),
        'referrers': collections.Counter(), 'direct': 0,
        'first': None, 'last': None,
    }
    sections = [section_of(p) for p in r['paths']]
    courses = [(COURSE.match(p).group(1).upper() if COURSE.match(p) else None) for p in r['paths']]
    landing = {}                                   # (vid, day) -> (time, ref) of the day's first page
    for vid, ts, pid, rid in zip(r['vid'], r['ts'], r['path'], r['ref']):
        if keep is not None and vid not in keep:
            continue
        day = EPOCH.date() + datetime.timedelta(days=ts // 86400)
        iso = day.isocalendar()
        week = '%d-W%02d' % (iso[0], iso[1])
        s['first'] = day if s['first'] is None or day < s['first'] else s['first']
        s['last'] = day if s['last'] is None or day > s['last'] else s['last']
        s['views'] += 1
        s['all_visitors'].add(vid)
        s['day_visitors'][day].add(vid)
        s['day_views'][day] += 1
        s['week_visitors'][week].add(vid)
        s['week_views'][week] += 1
        if totals_only:
            continue
        sec = sections[pid]
        s['section_views'][sec] += 1
        s['section_visitors'][sec].add(vid)
        path = r['paths'][pid]
        s['page_views'][path] += 1
        s['page_visitors'][path].add(vid)
        if courses[pid]:
            s['course_visitors'][courses[pid]].add(vid)
        # Where a visitor came from: their first page view of the day (the logs are not read in order).
        key = (vid, day)
        prev = landing.get(key)
        if prev is None or ts < prev[0]:
            landing[key] = (ts, rid)
    for _, rid in landing.values():
        if rid == 0:
            s['direct'] += 1
        elif rid > 1:
            s['referrers'][r['refs'][rid]] += 1
    return s


def render(r, sources):
    out = []
    w = out.append
    today = datetime.date.today().isoformat()
    w('# floridacourserepo.com - visitor report')
    w('')
    a = aggregate(r, totals_only=True)     # everything that did not announce itself as a bot
    s = aggregate(r, r['confirmed'])       # of those, visitors whose browser also loaded the page's CSS or scripts
    if not a['views']:
        w('No human page views were found in the logs read (%d lines).' % r['lines'])
        w('')
        w('Of those lines, %d were not in the expected Nginx format, %d were bots or scripts and %d were API calls.'
          % (r['unparsed'], r['bot_requests'], r['api_requests']))
        if r['lines'] and r['unparsed'] > r['lines'] / 2:
            w('Most lines could not be read: the log file is probably in another format or text encoding.')
        return '\n'.join(out) + '\n'
    if not s['views']:
        s = aggregate(r)                   # an old log with no asset lines: fall back rather than report nothing
    days = (a['last'] - a['first']).days + 1
    w('Made %s from the server\'s Nginx access logs, covering **%s to %s** (%d days).'
      % (today, a['first'], a['last'], days))
    w('')
    w('| | Browser-confirmed | Everything not marked as a bot |')
    w('|---|---:|---:|')
    w('| **Visitors** (distinct, whole period) | **{:,}** | {:,} |'.format(len(s['all_visitors']), len(a['all_visitors'])))
    w('| Average visitors a day | **{:,.1f}** | {:,.1f} |'.format(
        sum(len(v) for v in s['day_visitors'].values()) / days, sum(len(v) for v in a['day_visitors'].values()) / days))
    w('| **Page views** | **{:,}** | {:,} |'.format(s['views'], a['views']))
    w('| Pages per visitor | {:.1f} | {:.1f} |'.format(
        s['views'] / max(1, len(s['all_visitors'])), a['views'] / max(1, len(a['all_visitors']))))
    w('')
    w('| Not counted in either column | Requests |')
    w('|---|---:|')
    w('| Crawlers, bots and scripts that say what they are | {:,} |'.format(r['bot_requests']))
    w('| API requests (the desktop client and our tools) | {:,} |'.format(r['api_requests']))
    w('')
    w('**Browser-confirmed** visitors are the ones whose browser also fetched the site\'s stylesheet or '
      'scripts, as every real browser does on its first visit. Scrapers that pretend to be browsers usually '
      'fetch only the page, so the right-hand column includes them; the rest of this report uses the left. '
      'A visitor is one IP address with one browser: two people behind one school network on the same '
      'browser count as one, and one person on a phone and a laptop counts as two. '
      'The figures are a good guide to the trend rather than an exact head count.')
    w('')

    w('## By day')
    w('')
    w('| Day | Visitors | Page views | Not confirmed (visitors) |')
    w('|---|---:|---:|---:|')
    for d in sorted(a['day_visitors']):
        w('| %s %s | %d | %d | %d |' % (d.isoformat(), d.strftime('%a'), len(s['day_visitors'].get(d, ())),
                                         s['day_views'][d], len(a['day_visitors'][d]) - len(s['day_visitors'].get(d, ()))))
    w('')
    if len(a['week_visitors']) > 1:
        w('## By week')
        w('')
        w('| Week | Visitors | Page views | Not confirmed (visitors) |')
        w('|---|---:|---:|---:|')
        for k in sorted(a['week_visitors']):
            w('| %s | %d | %d | %d |' % (k, len(s['week_visitors'].get(k, ())), s['week_views'][k],
                                         len(a['week_visitors'][k]) - len(s['week_visitors'].get(k, ()))))
        w('')

    w('## What people looked at')
    w('')
    w('| Part of the site | Visitors | Page views |')
    w('|---|---:|---:|')
    for sec, n in s['section_views'].most_common():
        w('| %s | %d | %d |' % (sec, len(s['section_visitors'][sec]), n))
    w('')

    w('## Most-visited courses (course page, guide or resources)')
    w('')
    w('| Course | Visitors |')
    w('|---|---:|')
    for c, v in sorted(s['course_visitors'].items(), key=lambda kv: (-len(kv[1]), kv[0]))[:20]:
        w('| [%s](https://floridacourserepo.com/courses/%s) | %d |' % (c, c, len(v)))
    w('')

    w('## Most-viewed pages')
    w('')
    w('| Page | Visitors | Views |')
    w('|---|---:|---:|')
    for pth, n in sorted(s['page_views'].items(), key=lambda kv: (-len(s['page_visitors'][kv[0]]), -kv[1]))[:25]:
        w('| `%s` | %d | %d |' % (pth.replace('|', '%7C'), len(s['page_visitors'][pth]), n))
    w('')

    w('## Where visitors came from')
    w('')
    w('Counted once per visitor per day, from the first page they opened.')
    w('')
    w('| Source | Arrivals |')
    w('|---|---:|')
    w('| Typed the address, a bookmark, or an app that sends no source | %d |' % s['direct'])
    for dom, n in s['referrers'].most_common(20):
        w('| %s | %d |' % (dom, n))
    w('')

    w('## Crawlers and bots (most active, not counted as visitors)')
    w('')
    w('| User agent (first 60 characters) | Requests |')
    w('|---|---:|')
    for ua, n in r['bot_agents'].most_common(10):
        w('| %s | %d |' % (ua.replace('|', '/'), n))
    w('')
    w('---')
    w('Read %d log lines (%d not in the expected format) from %d file(s).'
      % (r['lines'], r['unparsed'], len(sources)))
    return '\n'.join(out) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('logs', nargs='+', help='Nginx access log file(s), uncompressed')
    ap.add_argument('--out', help='write the Markdown report here as well as to the screen')
    ap.add_argument('--days', type=int, default=0, help='only the last N days (default: everything)')
    ap.add_argument('--month', help='only one calendar month, as YYYY-MM (e.g. 2026-11)')
    a = ap.parse_args()
    month = None
    if a.month:
        try:
            first = datetime.datetime.strptime(a.month, '%Y-%m').date()
        except ValueError:
            ap.error('--month must look like 2026-11')
        nxt = (first.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
        month = (first, nxt - datetime.timedelta(days=1))
    report = render(parse(a.logs, a.days, month), a.logs)
    if a.out:
        with open(a.out, 'w', encoding='utf-8') as fh:
            fh.write(report)
    sys.stdout.reconfigure(encoding='utf-8')
    print(report)


if __name__ == '__main__':
    main()
