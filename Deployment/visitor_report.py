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
    return hashlib.sha256(('%s|%s' % (ip, ua)).encode('utf-8', 'replace')).hexdigest()[:16]


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


def parse(paths, days, month=None):
    """month: (first_day, last_day) to keep only that calendar month, or None."""
    cutoff = None
    if days:
        cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    s = {
        'lines': 0, 'unparsed': 0, 'bot_requests': 0, 'api_requests': 0,
        'bot_agents': collections.Counter(),
        'day_visitors': collections.defaultdict(set), 'day_views': collections.Counter(),
        'week_visitors': collections.defaultdict(set), 'week_views': collections.Counter(),
        'all_visitors': set(), 'views': 0,
        'section_views': collections.Counter(), 'section_visitors': collections.defaultdict(set),
        'page_views': collections.Counter(), 'page_visitors': collections.defaultdict(set),
        'course_visitors': collections.defaultdict(set),
        'referrers': collections.Counter(), 'landings': 0, 'direct': 0,
        'first': None, 'last': None,
    }
    seen_landing = set()
    for p in paths:
        with open_log(p) as fh:
            for raw in fh:
                s['lines'] += 1
                m = LINE.match(raw)
                if not m:
                    s['unparsed'] += 1
                    continue
                try:
                    t = datetime.datetime.strptime(m['time'], '%d/%b/%Y:%H:%M:%S %z')
                except ValueError:
                    s['unparsed'] += 1
                    continue
                if cutoff and t < cutoff:
                    continue
                if month and not (month[0] <= t.date() <= month[1]):
                    continue
                ua = m['ua']
                path = m['path'].split('?', 1)[0].split('#', 1)[0]
                if path.startswith('/api/'):
                    s['api_requests'] += 1
                    continue
                if not ua or ua == '-' or BOT.search(ua):
                    s['bot_requests'] += 1
                    s['bot_agents'][ua[:60] or '(no user agent)'] += 1
                    continue
                if m['method'] != 'GET' or m['status'] not in ('200', '304'):
                    continue
                if STATIC.search(path) or path.startswith(('/admin', '/lib/', '/css/', '/js/', '/_')):
                    continue
                if len(path) > 1:
                    path = path.rstrip('/')

                vid = visitor_id(m['ip'], ua)
                day = t.date()
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
                sec = section_of(path)
                s['section_views'][sec] += 1
                s['section_visitors'][sec].add(vid)
                s['page_views'][path] += 1
                s['page_visitors'][path].add(vid)
                cm = COURSE.match(path)
                if cm:
                    s['course_visitors'][cm.group(1).upper()].add(vid)

                # Where a visitor came from: their first page view of the day.
                key = (vid, day)
                if key not in seen_landing:
                    seen_landing.add(key)
                    s['landings'] += 1
                    dom = ref_domain(m['ref'])
                    if dom:
                        s['referrers'][dom] += 1
                    elif not m['ref'] or m['ref'] == '-':
                        s['direct'] += 1
    return s


def render(s, sources):
    out = []
    w = out.append
    today = datetime.date.today().isoformat()
    w('# floridacourserepo.com - visitor report')
    w('')
    if not s['views']:
        w('No human page views were found in the logs read (%d lines).' % s['lines'])
        w('')
        w('Of those lines, %d were not in the expected Nginx format, %d were bots or scripts and %d were API calls.'
          % (s['unparsed'], s['bot_requests'], s['api_requests']))
        if s['lines'] and s['unparsed'] > s['lines'] / 2:
            w('Most lines could not be read: the log file is probably in another format or text encoding.')
        return '\n'.join(out) + '\n'
    days = (s['last'] - s['first']).days + 1
    w('Made %s from the server\'s Nginx access logs, covering **%s to %s** (%d days).'
      % (today, s['first'], s['last'], days))
    w('')
    w('| | |')
    w('|---|---|')
    w('| **Visitors** (distinct, whole period) | **%d** |' % len(s['all_visitors']))
    w('| Average visitors a day | %.1f |' % (sum(len(v) for v in s['day_visitors'].values()) / days))
    w('| **Page views** | **%d** |' % s['views'])
    w('| Pages per visitor | %.1f |' % (s['views'] / max(1, len(s['all_visitors']))))
    w('| Requests from crawlers, bots and scripts (not counted above) | %d |' % s['bot_requests'])
    w('| API requests (the desktop client and our tools; not counted above) | %d |' % s['api_requests'])
    w('')
    w('A visitor is one IP address with one browser, so two people behind one school network on the '
      'same browser count as one, and one person on a phone and a laptop counts as two. '
      'The figures are a good guide to the trend rather than an exact head count.')
    w('')

    w('## By day')
    w('')
    w('| Day | Visitors | Page views |')
    w('|---|---:|---:|')
    for d in sorted(s['day_visitors']):
        w('| %s %s | %d | %d |' % (d.isoformat(), d.strftime('%a'), len(s['day_visitors'][d]), s['day_views'][d]))
    w('')
    if len(s['week_visitors']) > 1:
        w('## By week')
        w('')
        w('| Week | Visitors | Page views |')
        w('|---|---:|---:|')
        for k in sorted(s['week_visitors']):
            w('| %s | %d | %d |' % (k, len(s['week_visitors'][k]), s['week_views'][k]))
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
    for ua, n in s['bot_agents'].most_common(10):
        w('| %s | %d |' % (ua.replace('|', '/'), n))
    w('')
    w('---')
    w('Read %d log lines (%d not in the expected format) from %d file(s).'
      % (s['lines'], s['unparsed'], len(sources)))
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
