#!/usr/bin/env python
"""Parse a UWF CourseLeaf prefix PDF into {course id: entry}.

Written 2026-09-15 (batch 215). The naive approach -- splitting the extracted
text on /RET \\d{4}/ -- MISALIGNS, because each entry is laid out as

    RET 3028 Foundations... College of Health, ... 3 sh ...
    Prerequisite: ...  Co-requisite: RET 3028L
    <the description of RET 3028>

so a split on any course-number-looking token cuts at the COREQUISITE
reference and attaches the description to the wrong course. That produced
three wrong descriptions before it was caught.

Anchor on the full header signature instead -- number, title, then the
college/department line -- and take everything up to the next header as the
body of that entry.

    python uwf_pdf.py uwf_ret.pdf RET3028 RET3884 RET4886
    python uwf_pdf.py uwf_ret.pdf --all
"""
import re
import sys

from pypdf import PdfReader

# The title must be SHORT and contain no sentence period, or the lazy quantifier
# happily spans an entire description to reach the next entry's "College of"
# -- which silently attached three wrong descriptions on the first attempt.
# NOTE UWF abbreviates "College" as "Col" in some entries (e.g. "Col of Arts,
# Soc Sci and Human"), so an entry can be MISSED and silently merged into the
# previous one. Accept the abbreviation.
HEADER = re.compile(
    r'([A-Z]{3})\s(\d{4}[A-Z]?)\s+([^.]{1,90}?)\s+(?:College|Col|School)\s+of\s+\w',
)


def parse(path):
    text = '\n'.join(p.extract_text() or '' for p in PdfReader(path).pages)
    text = re.sub(r'\s+', ' ', text)
    hits = list(HEADER.finditer(text))
    out = {}
    for i, m in enumerate(hits):
        cid = m.group(1) + m.group(2)
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        body = text[m.start():end].strip()
        # keep the LONGEST entry when a number appears more than once
        if cid not in out or len(body) > len(out[cid]['body']):
            out[cid] = {'title': m.group(3).strip(), 'body': body}
    return out


def main():
    path = sys.argv[1]
    entries = parse(path)
    wanted = sys.argv[2:]
    if wanted == ['--all']:
        wanted = sorted(entries)
    for cid in wanted:
        e = entries.get(cid.upper())
        print('=' * 72)
        if not e:
            print('%s  NOT FOUND' % cid)
            continue
        print('%s  %s' % (cid, e['title']))
        print(e['body'][:1100])


if __name__ == '__main__':
    main()
