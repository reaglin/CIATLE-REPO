#!/usr/bin/env python
"""Given a course, say whether REVIEW_QUEUE.md already has something on it.

Ron, 2026-09-17, changing the working mode:

    "the plan is to keep track of the items (mark them) that need my attention,
     but our main focus is going to be on requested curriculum guides and we
     will only tackle those courses that have been requested. We will still
     need those notes to handle the situation of one of the marked courses
     being requested."

⚠⚠⚠ THAT LAST SENTENCE IS THE WHOLE POINT OF THIS TOOL. The queue-driven mode
met a flagged course by working steadily toward it, so the note was found in
passing. In request-driven mode a flagged course arrives WITHOUT WARNING, out of
order, from a member of the public -- and REVIEW_QUEUE.md is 105 items of prose.
Finding by eye does not scale and will be missed.

    python review_lookup.py TPA3230C          # one course
    python review_lookup.py --requests        # ⚠ check the LIVE request queue
    python review_lookup.py --all             # every course mentioned anywhere

⚠ --requests is the one to run at the start of every session under the new mode.
It fetches the waiting guide requests and flags any that already carry a note,
so a HELD course is never written by accident.

Matching is deliberately generous: a request for PHY3106 also surfaces notes
filed against PHY3107, because sequence partners and bare/C twins are exactly
where this project's findings live. Related hits are labelled as such.
"""
import io
import json
import os
import re
import sys
import urllib.request

try:                                    # Windows consoles default to cp1252
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, 'REVIEW_QUEUE.md')
API = 'https://floridacourserepo.com/api/v1/queue/guides?status=waiting'

HEAD_RE = re.compile(r'^#{2,3} (\d+)\.\s*(.*)$', re.M)
COURSE_RE = re.compile(r'\b([A-Z]{3})\s?(\d{4})([A-Z])?\b')

RESOLVED = ('resolved', 'closed', '✅')
INFO = ('informational', 'no decision needed', 'awareness', '*process',
        'tooling fixed', 'low priority')
# Words in a heading that mean "do not write this course without asking first".
HELD = ('held', 'pulled', 'not written', 'blocked', 'needs a decision',
        'split candidate', 'collision', 'correction candidate')


def classify(title):
    t = title.lower()
    if any(k in t for k in RESOLVED):
        return 'RESOLVED'
    if any(k in t for k in INFO):
        return 'INFO'
    return 'OPEN'


def is_held(title):
    return any(k in title.lower() for k in HELD)


def load_items():
    """Return [(num, title, status, held, set_of_course_ids)] in file order."""
    s = io.open(PATH, encoding='utf-8').read()
    heads = list(HEAD_RE.finditer(s))
    out = []
    for i, m in enumerate(heads):
        num, title = int(m.group(1)), m.group(2)
        end = heads[i + 1].start() if i + 1 < len(heads) else len(s)
        body = s[m.start():end]
        courses = {a + b + (c or '') for a, b, c in COURSE_RE.findall(body)}
        # ⚠ A course named in the HEADING is what the item is ABOUT; one that
        # only appears in the body is usually a passing example. Without this
        # split, TPA3230C returns 15 lines and the real item is lost in them.
        subject = {a + b + (c or '') for a, b, c in COURSE_RE.findall(title)}
        out.append((num, title, classify(title), is_held(title), courses, subject))
    # keep the first occurrence of each item number
    seen, uniq = set(), []
    for it in out:
        if it[0] not in seen:
            seen.add(it[0])
            uniq.append(it)
    return uniq


def index(items):
    """course id -> list of items mentioning it."""
    idx = {}
    for it in items:
        for c in it[4]:
            idx.setdefault(c, []).append(it)
    return idx


def clean(t):
    return re.sub(r'\s{2,}', ' ', re.sub(r'[⚠✅⏳⭐*`]', '', t)).strip()


def report(course, idx):
    """Print what is known about one course. Return True if anything was found."""
    course = course.upper().strip()
    hits = idx.get(course, [])
    about = [it for it in hits if course in it[5]]
    mentions = [it for it in hits if course not in it[5]]
    # related: same prefix+number, different suffix; and +/-1 on the number
    base = course[:7]
    related = []
    for c, items in idx.items():
        if c == course or not c.startswith(course[:3]):
            continue
        if c[:7] == base:                       # bare / C / L twin
            related += [(c, it, 'twin') for it in items]
        elif c[3:7].isdigit() and base[3:].isdigit() and abs(int(c[3:7]) - int(base[3:])) == 1:
            related += [(c, it, 'sequence partner') for it in items]

    if not (about or mentions or related):
        print('%-10s  no REVIEW_QUEUE note' % course)
        return False

    held = [it for it in about if it[3] and it[2] == 'OPEN']
    print('%-10s%s' % (course, '   ⚠⚠ HELD — ASK RON BEFORE WRITING' if held else ''))
    for it in about:
        print('    ABOUT    item %-4s [%-8s] %s' % (it[0], it[2], clean(it[1])[:78]))
    for it in mentions:
        print('    mentions item %-4s [%-8s] %s' % (it[0], it[2], clean(it[1])[:78]))
    seen = set()
    for c, it, why in related:
        if (c, it[0]) in seen:
            continue
        seen.add((c, it[0]))
        if c in it[5]:                       # only related items ABOUT that twin
            print('    %-8s item %-4s [%-8s] %s — %s'
                  % (why[:8], it[0], it[2], c, clean(it[1])[:58]))
    return True


def main():
    items = load_items()
    idx = index(items)
    args = [a for a in sys.argv[1:]]

    if '--all' in args:
        print('courses mentioned in REVIEW_QUEUE.md: %d (across %d items)'
              % (len(idx), len(items)))
        for c in sorted(idx):
            nums = ','.join(str(i[0]) for i in idx[c])
            held = ' ⚠ HELD' if any(i[3] and i[2] == 'OPEN' for i in idx[c]) else ''
            print('   %-10s items %s%s' % (c, nums, held))
        return 0

    if '--requests' in args:
        try:
            with urllib.request.urlopen(API, timeout=30) as r:
                data = json.load(r)['data']
        except Exception as e:
            print('could not read the request queue: %s' % e)
            return 1
        reqs = data.get('items') or []
        print('waiting guide requests: %d' % data.get('waiting', 0))
        if not reqs:
            print('nothing waiting — no course to check.')
            return 0
        hits = 0
        print()
        for i in reqs:
            if report(i['courseId'], idx):
                hits += 1
        print()
        print('%d of %d requested course(s) already carry a REVIEW_QUEUE note.' % (hits, len(reqs)))
        if hits:
            print('⚠ Read those items BEFORE writing. A HELD course needs Ron first.')
        return 0

    if not args:
        print(__doc__.strip().split('\n\n')[0])
        print('\nusage: review_lookup.py <COURSE> [COURSE ...] | --requests | --all')
        return 2

    for c in args:
        report(c, idx)
    return 0


if __name__ == '__main__':
    sys.exit(main())
