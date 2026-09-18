#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Correct the general-chemistry identifier on every published career path.

⚠⚠⚠ THE ERROR BEING FIXED. Six live paths name CHM2045 (and chemical-engineer
also names CHM2046) as though that were THE Florida identifier for general
chemistry. It is the identifier used by HALF the state.

Measured over the SCNS flat file, Florida public institutions, all four forms
of general chemistry I and II:

    CHM1045 / CHM1045C family   19 institutions
    CHM2045 / CHM2045C family   20 institutions
    institutions carrying BOTH   0

    1000 family: BC CFK DSC EFSC FAMU FGCU FIU FSU GCSC IRSC MDC NFC
                 NWFSC PBSC PESC PSC SJRSC TSC VC
    2000 family: CF FAU FGC FLPOLY FSCJ FSWSC HC LSSC NCF PHSC SCFMS
                 SFC SFSC SPC SSCF UCF UF UNF USF UWF

⚠⚠ FOUR OF FLORIDA'S PUBLIC UNIVERSITIES ARE IN THE 1000 FAMILY -- FSU,
FAMU, FIU and FGCU -- along with Broward, Miami Dade and Valencia, the three
largest state colleges. So the paths were naming an identifier that does not
exist at the institution a large share of their readers attend.

This is PARALLEL NUMBERING FAMILIES (batch 219) on the most-taken college
science course in the state, and it is benign for TRANSFER -- both families
are lower division and the sequences articulate -- but it is a guaranteed
FAILED SEARCH, which is the SPN3410 / ordinal-base shape (batch 203).

⚠ It also interacts with a warning the state prints on the second course of
the sequence: "a SEQUENCE once started should be taken entirely at one
institution ... only the COMPLETED sequence at one institution is equivalent
to a completed sequence at another." So crossing families mid-sequence is
exactly what the state tells students not to do.

The fix is a variantNote on the affected course entries, not a course change:
CHM2045 remains correct for the institutions that use it.
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

W = '⚠'
WW = '⚠⚠'

FAMILY_1000 = ('Florida State, Florida A&M, FIU, FGCU, Broward, Miami Dade, Valencia, '
               'Daytona State, Eastern Florida State, Gulf Coast, Indian River State, '
               'Northwest Florida State, Palm Beach State, Pensacola State, Polk State, '
               'St. Johns River State, Tallahassee State, North Florida and Florida Keys')

NOTE_I = (
    '%s FLORIDA NUMBERS GENERAL CHEMISTRY TWO WAYS, AND NO INSTITUTION CARRIES BOTH. '
    'Twenty public institutions use CHM2045 (or the integrated CHM2045C); nineteen use '
    'CHM1045 (or CHM1045C) — among them %s. '
    'Same course, same lower-division level, and the credit articulates either way — but '
    '%s LOOK UP WHICH FAMILY YOUR INSTITUTION USES BEFORE YOU GO SEARCHING, because the other '
    'number simply does not exist there. '
    '%s Also check the packaging: the bare number is a 3-credit lecture needing a separate '
    'CHM2045L (or CHM1045L) laboratory, while the C form is the integrated lecture-plus-lab at '
    '4 credits and is one registration.' % (WW, FAMILY_1000, WW, W))

NOTE_II = (
    '%s THE SAME TWO-FAMILY SPLIT AS GENERAL CHEMISTRY I — twenty institutions use CHM2046 '
    'or CHM2046C, nineteen use CHM1046 or CHM1046C, and no institution carries both. '
    '%s AND HERE THE STATE ITSELF ADDS A WARNING: the statewide record for this course reads '
    '"a sequence once started should be taken entirely at one institution ... only the completed '
    'sequence at one institution is equivalent to a completed sequence at another." '
    'So the ordinary transfer guarantee is weaker than usual on the second half of a sequence. '
    '%s Finish general chemistry where you started it. '
    '%s One more thing worth knowing if you are dual-enrolled: SCNS records ELECTIVE high-school '
    'credit for general chemistry I and SCIENCE credit for general chemistry II — two halves of '
    'one sequence, two different high-school outcomes.' % (WW, WW, WW, W))


def main():
    changed = []
    for p in sorted(glob.glob(os.path.join(PATHS, '*.json'))):
        doc = json.load(io.open(p, encoding='utf-8'))
        hit = False
        for c in doc.get('courses', []):
            if c['courseId'] == 'CHM2045':
                c['variantNote'] = NOTE_I
                hit = True
            elif c['courseId'] == 'CHM2046':
                c['variantNote'] = NOTE_II
                hit = True
        if hit:
            io.open(p, 'w', encoding='utf-8').write(
                json.dumps(doc, ensure_ascii=False, indent=1))
            changed.append(os.path.basename(p)[:-5])
    print('NOTE_I  %d chars   NOTE_II %d chars   (limit 1000)' % (len(NOTE_I), len(NOTE_II)))
    print('corrected %d path(s): %s' % (len(changed), ', '.join(changed)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
