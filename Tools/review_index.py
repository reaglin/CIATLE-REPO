#!/usr/bin/env python
"""Rebuild the DECISION LIST index at the top of REVIEW_QUEUE.md.

Ron, 2026-09-16: "Keep all unresolved in a file. Once we complete the queue I
will be looking at them."

REVIEW_QUEUE.md had grown to 100+ numbered items while its hand-written index
still stopped at batch 196 -- so the one thing Ron asked for (everything
unresolved, in one pass) was the one thing the file no longer delivered.

This regenerates that index from the item headings themselves, so it cannot go
stale again. Run it after adding an item:

    python review_index.py            # rewrite the index in place
    python review_index.py --check    # non-zero exit if the index is stale

Headings are '### N. ...' for items 1-9 and '## N. ...' for 10 onward; both are
matched. An item is classified from its heading text:

    RESOLVED  -- 'resolved' or 'closed' or a check mark
    INFO      -- 'informational', 'no decision needed', 'awareness', 'process'
    OPEN      -- everything else, i.e. it still wants a decision

⚠ Classification is deliberately conservative: anything ambiguous lands in OPEN,
because an item wrongly listed as open costs Ron a glance and an item wrongly
listed as resolved gets silently lost.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, 'REVIEW_QUEUE.md')

START = '## ⭐ DECISION LIST — everything awaiting Ron, in one pass'
HEAD_RE = re.compile(r'^#{2,3} (\d+)\.\s*(.*)$', re.M)

RESOLVED = ('resolved', 'closed', '✅')
INFO = ('informational', 'no decision needed', 'awareness', '*process',
        'tooling fixed', 'low priority')


def classify(title):
    t = title.lower()
    if any(k in t for k in RESOLVED):
        return 'RESOLVED'
    if any(k in t for k in INFO):
        return 'INFO'
    return 'OPEN'


def clean(title):
    """Strip decoration so the index table stays readable."""
    t = re.sub(r'[⚠✅⏳⭐]', '', title)
    t = re.sub(r'\s*—\s*\*informational\*\s*$', '', t, flags=re.I)
    t = t.replace('|', r'\|').strip()
    return re.sub(r'\s{2,}', ' ', t)


def build(items):
    opens = [(n, t) for n, t, k in items if k == 'OPEN']
    infos = [(n, t) for n, t, k in items if k == 'INFO']
    done = [(n, t) for n, t, k in items if k == 'RESOLVED']

    L = [START, '']
    L.append('⚠⚠ **This index is GENERATED — do not hand-edit it.** Add your item as a numbered')
    L.append('section below, then run `python review_index.py`. The index that used to live here was')
    L.append('maintained by hand and fell 30 batches behind, which defeated the point of the file.')
    L.append('')
    L.append('**Ron, 2026-09-16:** *"Keep all unresolved in a file. Once we complete the queue I will be')
    L.append('looking at them."* — that is this table. **Nothing here blocks the batch loop**; the loop')
    L.append('continues around every one of them.')
    L.append('')
    L.append('| | Count |')
    L.append('|---|---|')
    L.append('| ⏳ **Awaiting a decision from Ron** | **%d** |' % len(opens))
    L.append('| Informational — recorded, no decision needed | %d |' % len(infos))
    L.append('| ✅ Resolved | %d |' % len(done))
    L.append('| **Total items** | **%d** |' % len(items))
    L.append('')
    L.append('---')
    L.append('')
    L.append('### ⏳ Awaiting a decision (%d)' % len(opens))
    L.append('')
    L.append('| # | Item |')
    L.append('|---|---|')
    for n, t in opens:
        L.append('| **%s** | %s |' % (n, clean(t)))
    L.append('')
    L.append('### Informational — no decision needed (%d)' % len(infos))
    L.append('')
    L.append('| # | Item |')
    L.append('|---|---|')
    for n, t in infos:
        L.append('| %s | %s |' % (n, clean(t)))
    L.append('')
    L.append('### ✅ Resolved (%d)' % len(done))
    L.append('')
    L.append('| # | Item |')
    L.append('|---|---|')
    for n, t in done:
        L.append('| %s | %s |' % (n, clean(t)))
    L.append('')
    return '\n'.join(L)


def main():
    s = io.open(PATH, encoding='utf-8').read()
    items = []
    for m in HEAD_RE.finditer(s):
        n, title = m.group(1), m.group(2)
        items.append((int(n), title, classify(title)))
    # keep the first occurrence of each number, ordered numerically
    seen, uniq = set(), []
    for n, t, k in sorted(items, key=lambda x: x[0]):
        if n not in seen:
            seen.add(n)
            uniq.append((n, t, k))

    assert START in s, 'index heading not found'
    head, rest = s.split(START, 1)
    # the index block ends at the next top-level '## ' heading
    m = re.search(r'^## (?!⭐)', rest, re.M)
    assert m, 'could not find the end of the index block'
    tail = rest[m.start():]

    new = head + build(uniq) + tail

    if '--check' in sys.argv:
        if new != s:
            print('STALE — run: python review_index.py')
            return 1
        print('index is current (%d items)' % len(uniq))
        return 0

    io.open(PATH, 'w', encoding='utf-8').write(new)
    o = sum(1 for _, _, k in uniq if k == 'OPEN')
    i = sum(1 for _, _, k in uniq if k == 'INFO')
    r = sum(1 for _, _, k in uniq if k == 'RESOLVED')
    print('REVIEW_QUEUE.md index rebuilt: %d items — %d awaiting Ron, %d informational, %d resolved'
          % (len(uniq), o, i, r))
    return 0


if __name__ == '__main__':
    sys.exit(main())
