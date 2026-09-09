#!/usr/bin/env python3
"""Assemble drafts/{ID}_guide.json from a plain HTML body + a metadata row.

Authoring guide HTML directly inside JSON means escaping every quote in a 25 KB
document, which is where hand-built drafts go wrong. Write the body as plain HTML in
scratchpad/html/{ID}.html instead, put the scalar fields in scratchpad/meta.json, and
let this build the draft.

    python scratchpad/mkguide.py EEE3342C          # one
    python scratchpad/mkguide.py --all             # everything in meta.json

meta.json is {"EEE3342C": {"title":..., "credits":3, "contact_hours":60,
"prerequisites": null|str, "version":"1.0"}, ...}

It re-checks the four server limits that cause an HTTP 400 before writing, so a clean
run here means validate_drafts.py has nothing structural left to find.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
HTML = os.path.join(HERE, 'html')
DRAFTS = os.path.join(TOOLS, 'drafts')

LIMITS = (('title', 300), ('prerequisites', 500), ('version', 50))


def build(cid, meta):
    src = os.path.join(HTML, cid + '.html')
    body = open(src, encoding='utf-8').read().strip()
    g = {
        'title': meta['title'],
        'html_content': body,
        'credits': meta['credits'],
        'contact_hours': meta['contact_hours'],
        'prerequisites': meta.get('prerequisites'),
        'version': meta.get('version', '1.0'),
    }
    errs = []
    if not g['html_content']:
        errs.append('html_content empty')
    for f, lim in LIMITS:
        v = g.get(f)
        if v and len(v) > lim:
            errs.append('%s %d chars > %d' % (f, len(v), lim))
    if not isinstance(g['credits'], int) or not 0 <= g['credits'] <= 12:
        errs.append('credits %r out of 0-12' % g['credits'])
    if not isinstance(g['contact_hours'], int) or not 0 <= g['contact_hours'] <= 1500:
        errs.append('contact_hours %r out of 0-1500' % g['contact_hours'])
    if errs:
        raise SystemExit('%s: %s' % (cid, '; '.join(errs)))
    out = os.path.join(DRAFTS, cid + '_guide.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(g, fh, ensure_ascii=False, indent=1)
    pre = g['prerequisites']
    return '%-10s %2d cr %4d hrs  %6.1f KB  prereq %s' % (
        cid, g['credits'], g['contact_hours'], len(body) / 1024,
        ('%d chars' % len(pre)) if pre else 'null')


if __name__ == '__main__':
    meta = json.load(open(os.path.join(HERE, 'meta.json'), encoding='utf-8'))
    ids = sorted(meta) if sys.argv[1:2] == ['--all'] else sys.argv[1:]
    if not ids:
        raise SystemExit(__doc__)
    os.makedirs(DRAFTS, exist_ok=True)
    for cid in ids:
        if cid not in meta:
            raise SystemExit('%s missing from meta.json' % cid)
        print(build(cid, meta[cid]))
