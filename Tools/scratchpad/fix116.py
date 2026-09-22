# -*- coding: utf-8 -*-
import io
p='REVIEW_QUEUE.md'
s=io.open(p,encoding='utf-8').read()
old="| ⚠⚠ **01.83** Veterinary/Animal Health Technologies | `veterinary-technician` | **10** | **293** |\n"
assert old in s
s=s.replace(old, old +
 "| ⚠ **51.15** Mental and Social Health Services | *(no path blocked — see below)* | 9 | **1,164 MSW** |\n")
old2="**What it takes:** add the seven groups to `EXTRA_GROUPS`"
assert old2 in s
s=s.replace(old2,
 "⚠⚠ **`51.15` is a DIFFERENT KIND of entry and blocks no path** (added 2026-09-22). The\n"
 "`social-worker` path published normally on `44.07`. But **Florida's MSW output is SPLIT**: 368 master's\n"
 "under `44.0701` and **796 under `51.1503` Clinical/Medical Social Work** — FSU 431, FAU 143, UWF 120,\n"
 "FIU 74, UNF 28, four of which record NO master's under the social work code at all. ⚠ The\n"
 "`social-work` programme therefore claims `44.0701` only and states the split in its `degreesNote`.\n"
 "**Seeding `51.15` would let it claim both and would also open mental health counselling (`51.1508`) and\n"
 "the 10-institution state-college human services tier (`51.1599`) to the programme layer.** Low urgency;\n"
 "fold it in with the rest.\n\n"
 "**What it takes:** add the groups to `EXTRA_GROUPS`")
io.open(p,'w',encoding='utf-8').write(s)
print('ok')
