# -*- coding: utf-8 -*-
"""Batch 250: print a draft's scalars and its HTML as text (run from Tools/).

    python scratchpad/b250_show.py ETS1542C [--full]
"""
import html
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
full = '--full' in sys.argv
for cid in [a for a in sys.argv[1:] if not a.startswith('--')]:
    d = json.load(open('drafts/%s_guide.json' % cid, encoding='utf-8'))
    print('=====', cid, '|', d['title'], '| cr', d['credits'], '| hrs', d['contact_hours'], '| v', d['version'],
          '| pushed', d.get('pushed_utc'))
    print('PREREQ:', d.get('prerequisites'))
    h = d['html_content']
    t = re.sub(r'<(h2|h3)>', r'\n\n## ', h)
    t = re.sub(r'<li[^>]*>', '\n - ', t)
    t = re.sub(r'<tr[^>]*>', '\n | ', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    t = re.sub(r'[ \t]+', ' ', t)
    print(t if full else t[:3500])
    if d.get('offering_notes'):
        print('OFFERING_NOTES:', json.dumps(d['offering_notes'], ensure_ascii=False)[:1500])
