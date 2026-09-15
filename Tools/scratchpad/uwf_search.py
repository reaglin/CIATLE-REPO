"""UWF catalog course lookup via the SEARCH route.

Found 2026-09-15 (batch 212). The project's workhorse UWF route is the prefix PDF
(catalog.uwf.edu/courseinformation/courses/<pfx>/<pfx>.pdf). That route 404s for
prefixes UWF does not list on its course-information index -- ATF and ATT among
them, even though UWF is an active SCNS carrier of both.

This route answers for those:

    https://catalog.uwf.edu/search/?P=<PREFIX>%20<NUMBER>

and returns the course block with the full description, credits and prerequisite.
"""
import html
import re
import sys
import time

import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch(course):
    """course like 'ATT 1110' or 'ATT1110'."""
    c = course.strip().upper()
    if ' ' not in c:
        c = c[:3] + ' ' + c[3:]
    url = "https://catalog.uwf.edu/search/?P=" + c.replace(' ', '%20')
    r = requests.get(url, headers=UA, timeout=60)
    r.raise_for_status()
    return r.text


def clean(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def parse(body):
    """Pull out every courseblock on the page."""
    # NOTE the element is <article class="searchresult search-courseresult">,
    # not a <div>. Page results use search-pageresult and are ignored.
    out = []
    for blk in re.findall(
            r'<article class="searchresult search-courseresult">(.*?)</article>',
            body, re.S):
        out.append(clean(blk))
    return out


def main():
    for course in sys.argv[1:]:
        print('=' * 70)
        print('UWF ' + course)
        try:
            blocks = parse(fetch(course))
        except Exception as exc:
            print('   ERROR %s' % exc)
            continue
        if not blocks:
            print('   (no course block parsed)')
        for b in blocks:
            print('   ' + b[:1800])
        time.sleep(1.0)


if __name__ == '__main__':
    main()
