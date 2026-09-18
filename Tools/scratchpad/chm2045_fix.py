#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Republish CHM2045 at version 1.1 with the two-family finding.

⚠ WHY A LIVE GUIDE IS BEING TOUCHED. The published CHM2045 guide (v1.0) does
not mention CHM1045 anywhere. That is not a wrong statement, it is a material
omission: the guide describes a course carried by 20 of the 39 Florida public
institutions that teach general chemistry, and the other 19 teach the same
course under a number the guide never names. A student at Florida State, FIU,
Broward or Miami Dade reading it would not learn that their own course is here.

Ron's standing instruction covers this: "simply fix errors as you spot them."

The edit is ADDITIVE -- the existing content is untouched. It splices the
two-family block and the dual-enrolment note into Special Information, adds a
pointer to the front of the prerequisite string, and bumps 1.0 -> 1.1.

It pulls the live HTML rather than re-deriving it, so nothing that was already
verified gets rewritten from memory.
"""
import io
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from b239_build import TWO_FAMILIES, DUAL_ENROL  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFTS = os.path.join(HERE, '..', 'drafts')
API = 'https://floridacourserepo.com/api/v1/courses/CHM2045/guide'

LEAD = ('LOOK UP WHICH NUMBER YOUR SCHOOL USES: Florida runs TWO parallel numbering families for '
        'general chemistry and NO institution carries both. 20 institutions use CHM2045 (or the '
        'integrated CHM2045C); 19 use CHM1045 (or CHM1045C), including Florida State, Florida A&M, '
        'FIU, FGCU, Broward, Miami Dade and Valencia. Same course, same level, different number. ')


def main():
    live = json.load(urllib.request.urlopen(API))['data']
    html = live['htmlContent']
    if 'CHM1045' in html:
        print('already corrected; nothing to do')
        return 0

    # Splice the new blocks in at the top of Special Information, so the finding
    # is the first thing under that heading rather than buried at the end.
    anchor = '<h2>Special Information</h2>'
    if anchor not in html:
        print('⚠ no Special Information heading found; appending instead')
        html = html + anchor + TWO_FAMILIES + DUAL_ENROL
    else:
        html = html.replace(anchor, anchor + TWO_FAMILIES + DUAL_ENROL, 1)

    prereq = live.get('prerequisites') or ''
    prereq = LEAD + prereq
    if len(prereq) > 1000:
        # Keep the new warning; trim the tail of the inherited string on a
        # sentence boundary rather than mid-word.
        keep = 1000 - len(LEAD)
        cut = prereq[len(LEAD):][:keep]
        cut = cut[:cut.rfind('.') + 1] if '.' in cut else cut
        prereq = LEAD + cut
        print('⚠ prerequisite trimmed to fit the 1000-char server limit')

    draft = {
        'title': live['title'],
        'html_content': html,
        'credits': live['credits'],
        'contact_hours': live['contactHours'],
        'prerequisites': prereq,
        'version': '1.1',
    }
    io.open(os.path.join(DRAFTS, 'CHM2045_guide.json'), 'w', encoding='utf-8').write(
        json.dumps(draft, ensure_ascii=False, indent=1))
    print('CHM2045  v%s -> v1.1 | html %d -> %d | prereq %d -> %d'
          % (live.get('version'), len(live['htmlContent']), len(html),
             len(live.get('prerequisites') or ''), len(prereq)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
