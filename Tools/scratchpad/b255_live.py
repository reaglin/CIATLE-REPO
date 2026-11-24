# -*- coding: utf-8 -*-
"""Batch 255: print the live course records for the requested courses (run from Tools/)."""
import sys
import requests
for c in sys.argv[1:]:
    d = requests.get('https://floridacourserepo.com/api/v1/courses/%s' % c, timeout=30).json().get('data') or {}
    print(c, '|', d.get('title'), '| cr', d.get('creditHours'), '| hrs', d.get('contactHours'))
    for o in d.get('offerings') or []:
        print('    ', o.get('institution'), '|', o.get('title'), '|', o.get('credits'))
