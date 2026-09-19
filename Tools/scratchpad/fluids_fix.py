#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Correct the fluid mechanics and hydraulics identifiers on the live paths.

⚠⚠⚠ THE ERROR. Fluid mechanics is one of the most fragmented subjects in the
Florida catalogue, and the published paths each name ONE number for it without
saying so. Measured over the SCNS flat file, public institutions:

    EGN3353C    1  UF                              <- named on THREE paths
    EGN3353     1  USF
    CWR3201     7  FAMU FIU FSU UCF UF UNF UWF
    CWR3201C    2  FAU FGCU                        <- named on civil-engineer
    EML3701     3  FAU UCF USF

    CWR4202     7  FAMU FAU FLPOLY FSU UF USF UWF
    CWR4202C    2  UCF UNF                         <- named on civil-engineer

So aerospace-engineer, civil-engineer and mechanical-engineer all present
EGN3353C -- a ONE-CARRIER identifier -- as "Fluid Mechanics", and
civil-engineer additionally names the two-carrier forms of both hydraulics
courses while seven-carrier forms of each exist.

⚠ Every one of these ids is REAL and every one is LISTED on the site, so
nothing was fabricated and no link is broken. The defect is that a reader at
any of the other institutions looks up the named number, does not find it, and
has no way to learn that their own number is the same course.

THE FIX, and it is deliberately conservative:

1. SWAP the two civil-engineer ids to the MAJORITY form -- CWR3201C -> CWR3201
   and CWR4202C -> CWR4202 -- because in both cases one form has seven carriers
   and the other two, and the majority form is plainly the better page to send
   a reader to.

2. DO NOT swap EGN3353C. There is no majority number to swap to: the subject
   genuinely runs under five identifiers across two prefixes and no single one
   is the Florida answer. Instead every affected entry gets a variantNote
   giving the whole family with its carriers, so the reader can find their own.

⚠ This is the PACKAGING-IS-NOT-DIVERGENCE rule doing its work in reverse: the
C and bare forms are the same course and the credit articulates, so the issue
is not that a student would learn the wrong thing -- it is that they cannot
FIND the right page. That makes it a search problem, and the fix is to name
every number rather than to warn about any of them.
"""
import glob
import io
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
PATHS = os.path.join(HERE, '..', 'career_paths')

W, WW = '⚠', '⚠⚠'

FLUIDS = (
    '%s FLUID MECHANICS IS THE MOST FRAGMENTED NUMBER IN FLORIDA ENGINEERING, and this identifier '
    'is carried by ONE institution. The same course runs under five numbers across two prefixes: '
    'EGN3353C (UF), EGN3353 (USF), CWR3201 (FAMU, FIU, Florida State, UCF, UF, UNF, UWF), '
    'CWR3201C (FAU, Florida Gulf Coast) and EML3701 (FAU, UCF, USF). '
    '%s Broadly, CWR is the civil and environmental route, EML the mechanical route and EGN the '
    'general-engineering one — but several institutions carry more than one, and UF carries both '
    'EGN3353C and CWR3201. The C suffix marks the integrated lecture-plus-laboratory form; it is '
    'the same course, packaged as one registration instead of two. '
    'LOOK UP WHICH NUMBER YOUR PROGRAMME USES rather than searching for this one, and on transfer '
    'send the syllabus, because an evaluator matching identifiers across these five will find '
    'nothing to match.' % (WW, W))

HYDRAULICS = (
    '%s TWO NUMBERS, AND THIS IS THE ONE SEVEN INSTITUTIONS USE. CWR4202 is carried by FAMU, FAU, '
    'Florida Polytechnic, Florida State, UF, USF and UWF; UCF and UNF carry the integrated '
    'CWR4202C instead, and no institution carries both. '
    'Same course — the C form simply packages the laboratory into one registration — so the '
    'credit articulates either way. %s But an evaluator or degree audit matching on the identifier '
    'reads the two as different courses, so say which form you took and send the syllabus.' % (WW, W))

HYDRAULICS_1 = (
    '%s FIVE NUMBERS FOR THIS SUBJECT ACROSS FLORIDA, and this is the one seven institutions use: '
    'CWR3201 at FAMU, FIU, Florida State, UCF, UF, UNF and UWF. FAU and Florida Gulf Coast carry '
    'the integrated CWR3201C; UF also carries EGN3353C, USF carries EGN3353, and FAU, UCF and USF '
    'carry EML3701 on the mechanical side. '
    '%s The titles vary as much as the numbers — Hydraulics at Florida State, Fluid Mechanics at '
    'FIU and UNF, Engineering Fluid Mechanics at UCF, Hydrodynamics at UF, Water Resource '
    'Engineering at UWF — and the statewide description is plain fluid mechanics throughout. '
    'Register by the number your own programme names.' % (WW, W))

SWAPS = {'CWR3201C': ('CWR3201', HYDRAULICS_1), 'CWR4202C': ('CWR4202', HYDRAULICS)}


def main():
    changed = []
    for p in sorted(glob.glob(os.path.join(PATHS, '*.json'))):
        doc = json.load(io.open(p, encoding='utf-8'))
        hit = []
        for c in doc.get('courses', []):
            cid = c['courseId']
            if cid == 'EGN3353C':
                c['variantNote'] = FLUIDS
                hit.append('EGN3353C note')
            elif cid in SWAPS:
                new, note = SWAPS[cid]
                c['courseId'] = new
                c['variantNote'] = note
                hit.append('%s -> %s' % (cid, new))
        if hit:
            io.open(p, 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False, indent=1))
            changed.append('%s: %s' % (os.path.basename(p)[:-5], ', '.join(hit)))
    print('FLUIDS       %d chars' % len(FLUIDS))
    print('HYDRAULICS   %d chars' % len(HYDRAULICS))
    print('HYDRAULICS_1 %d chars  (limit 1000)' % len(HYDRAULICS_1))
    for c in changed:
        print('  ' + c)
    return 0


if __name__ == '__main__':
    sys.exit(main())
