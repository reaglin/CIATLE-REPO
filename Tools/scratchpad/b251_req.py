# -*- coding: utf-8 -*-
"""Batch 251: print the requisite text of a course from a Coursedog cache (run from Tools/).

    python scratchpad/b251_req.py fsu COM5235 COM3120
"""
import json
import re
import sys

sys.path.insert(0, 'scratchpad')
import coursedog  # noqa: E402

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
key = sys.argv[1]
for code in sys.argv[2:]:
    for c in coursedog.find(key, code)[:1]:
        blob = json.dumps(c.get('requisites') or {}, ensure_ascii=False)
        texts = re.findall(r'"(?:freeformText|description|value|name)":\s*"([^"]{3,})"', blob)
        print('==', key, code, c.get('name'), '| repeat', (c.get('credits') or {}).get('repeatable'))
        print('   requisites:', '; '.join(dict.fromkeys(texts))[:800] or blob[:400])
        for k in ('prerequisites', 'corequisites', 'customFields', 'notes'):
            if c.get(k):
                print('  ', k, json.dumps(c[k], ensure_ascii=False)[:600])
