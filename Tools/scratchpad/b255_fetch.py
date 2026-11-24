# -*- coding: utf-8 -*-
"""Batch 255: fetch catalogue entries for the requested courses (run from Tools/).

Downloads are read as text only; nothing fetched is executed.
"""
import json
import re

import requests

UA = {'User-Agent': 'Mozilla/5.0 (course-guide research)'}


def text(html):
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', html, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t)


def show(label, url, needles, span=1500):
    try:
        r = requests.get(url, headers=UA, timeout=40)
    except Exception as e:  # noqa: BLE001
        print('==', label, 'ERR', e)
        return
    t = text(r.text)
    print('==', label, r.status_code, len(r.text))
    for n in needles:
        i = t.find(n)
        if i >= 0:
            print('  --', n, ':', t[i:i + span])
            return
    print('  (no needle found)', t[:300])


show('SSCF CJE2540', 'https://www.seminolestate.edu/catalog/courses/cje2540', ['CJE 2540', 'CJE2540', 'Police'])
show('SSCF HUN2202', 'https://www.seminolestate.edu/catalog/courses/hun2202', ['HUN 2202', 'HUN2202', 'Nutrition'])
show('VC HUN', 'https://catalog.valenciacollege.edu/coursedescriptions/coursesoffered/hun/', ['HUN 2202', 'HUN2202'])

# UF course search API
for code in ('EUH 6612',):
    try:
        r = requests.post('https://catalog.ufl.edu/course-search/api/?page=fose&route=search',
                          json={'other': {'srcdb': ''}, 'criteria': [{'field': 'keyword', 'value': code}]},
                          headers=UA, timeout=30)
        res = [x for x in r.json().get('results', []) if x.get('code') == code]
        print('UF', code, json.dumps(res)[:600])
        if res:
            r2 = requests.post('https://catalog.ufl.edu/course-search/api/?page=fose&route=details',
                               json={'group': 'code:' + code, 'key': '', 'srcdb': res[0].get('srcdb', ''),
                                     'matched': 'crn:' + str(res[0].get('crn', ''))},
                               headers=UA, timeout=30)
            print('UF details', text(json.dumps(r2.json()))[:1500])
    except Exception as e:  # noqa: BLE001
        print('UF', code, 'ERR', e)
show('UF GRAD EUH', 'https://catalog.ufl.edu/GRAD/courses/history/', ['EUH 6612', 'EUH6612'])
