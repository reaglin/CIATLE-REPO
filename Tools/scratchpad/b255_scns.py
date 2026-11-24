# -*- coding: utf-8 -*-
"""Batch 255: pull SCNS course-description reports (institution's own text, and the statewide record)
for the requested courses, and print the matching rows (run from Tools/).

Reports are saved under scratchpad/b255_dl/ as CSV data; nothing there is executed.
"""
import csv
import io
import os
import sys

sys.path.insert(0, 'scratchpad')
import scns  # noqa: E402

OUT = os.path.join('scratchpad', 'b255_dl')
os.makedirs(OUT, exist_ok=True)

# (prefix, numeric institution id or '' for statewide, course numbers to show)
JOBS = [
    ('ACG', '102', ['2061']), ('ACG', '48', ['2072']), ('CJE', '89', ['2540']),
    ('EUH', '101', ['6612']), ('HUN', '89', ['2202']), ('HFT', '17', ['1102']), ('DIG', '55', ['2040']),
    ('ACG', '', ['2061', '2072']), ('CJE', '', ['2540']), ('EUH', '', ['6612']), ('HUN', '', ['2202']),
    ('HFT', '', ['1102']), ('DIG', '', ['2040']),
]
if len(sys.argv) > 1:
    JOBS = [j for j in JOBS if j[0] + (j[1] or 'S') in sys.argv[1:]]

for prefix, inst, nums in JOBS:
    path = os.path.join(OUT, '%s_%s.csv' % (prefix, inst or 'state'))
    if not os.path.exists(path):
        try:
            scns.report_csv(prefix, kind='CourseDescriptions' if inst else 'StatewideCourse',
                            institution=inst, out=path)
        except BaseException as e:  # noqa: BLE001
            print('==', prefix, inst or 'state', 'ERR', e)
            continue
    raw = io.open(path, encoding='utf-8-sig', errors='replace').read()
    print('==', prefix, inst or 'state', len(raw), 'chars')
    for row in csv.reader(io.StringIO(raw)):
        line = ' | '.join(row)
        if any((prefix + n) in line.replace(' ', '') for n in nums):
            print('  ', line[:2500])
