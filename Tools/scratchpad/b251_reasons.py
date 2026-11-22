# -*- coding: utf-8 -*-
"""Plan 12.4 (2026-11-22): public reasons for guide requests. Run from Tools/.

    python scratchpad/b251_reasons.py declined   # reword the reasons of courses already declined (works now)
    python scratchpad/b251_reasons.py hold       # put the five waiting courses on hold (after the Phase 12 deploy)

A decline's reason is shown publicly from the Phase 12 deploy on, so every one is worded for the visitor:
about the course, never naming the editor, a REVIEW_QUEUE item or the visitor.
"""
import sys

sys.path.insert(0, '.')
import guide_requests as gr  # noqa: E402

AGAIN = ' If that changes, the course can be requested again.'

DECLINED = {
    'CET1112': 'Only a private career college carries CET1112. Florida public colleges teach this subject as CET1112C, '
               'which has a curriculum guide.',
    'ARH2990': 'ARH2990 is a cooperative work experience number: its content is the student\'s own placement, so there '
               'is no common course for a curriculum guide to describe.',
    'ARH2957': 'ARH2957 is an honors study-abroad number (1 to 6 variable credits) whose content is set by each trip, so '
               'there is no common course for a curriculum guide to describe.',
    'SOW2949': 'SOW2949 is a cooperative work experience number: its content is the student\'s own placement, so there '
               'is no common course for a curriculum guide to describe.',
    'EEL2130C': 'Florida Polytechnic, the only college that lists EEL2130C, appears to have stopped teaching it: it is on '
                'none of its current degree plans and no description is published.' + AGAIN,
    'ETI0602': 'ETI0602 belongs to the Industrial Technology programme, which the state ended after the 2024-25 school '
               'year, and the only technical college that offered it no longer does.',
    'EEL4016': 'FIU, the only institution that lists EEL4016, retired the course in 2004, so there is no current course '
               'to describe. Its first half, EEL4015 Electrical Design in Buildings I, is still taught at FIU.',
    'EEL4081': 'EEL4081 is a new topics course at UNF, the only university that offers it, and UNF does not yet publish '
               'a description of what it covers.' + AGAIN,
    'PET1170': 'Miami Dade College, the only college that offers PET1170, does not publish a course description that '
               'could be read, so there is nothing to base a guide on.' + AGAIN,
}

HOLD = {
    'EEL4448': 'Florida Polytechnic, the only university that offers EEL4448, does not publish a description or syllabus '
               'for it, so there is nothing to base a curriculum guide on.' + AGAIN,
    'EEL5025': 'EEL5025 is a graduate course at the FAMU-FSU College of Engineering, which does not publish a '
               'description of what it covers, so there is nothing to base a curriculum guide on.' + AGAIN,
    'EEL5009': 'FIU, the only university that offers EEL5009, describes it only as covering "a broad range of topics" for '
               'entering master\'s students and does not say which, so a guide would have to invent its content.' + AGAIN,
    'EET2525C': 'State College of Florida, the only college that offers EET2525C, does not publish a description that '
                'could be read, and the statewide record files the number under a different course (Industrial Motor '
                'Control Lab), so it is not clear what the course covers.' + AGAIN,
    'ETS3543L': 'FAMU, the only university that offers ETS3543L, does not publish a description of this laboratory that '
                'could be read, so there is nothing to base a curriculum guide on.' + AGAIN,
}


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else ''
    if which not in ('declined', 'hold'):
        sys.exit(__doc__)
    site = gr.Site()
    for course, reason in (DECLINED if which == 'declined' else HOLD).items():
        assert 20 <= len(reason) <= 1000, course
        try:
            print(course, site.set(course, 'Declined' if which == 'declined' else 'Held', reason))
        except RuntimeError as e:
            print(e)


if __name__ == '__main__':
    main()
