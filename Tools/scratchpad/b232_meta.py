"""Batch 232 metadata -- PHC (public health), the three queued rows.

All three: 3 credits / 45 contact hours, derived by the 1:15 convention. NO
institution publishes a contact-hour figure anywhere in the PHC prefix.

*** HEADLINE: PHC4140 is a BRANCH-4 case -- and this time the MECHANISM is
    visible in the record ***

  statewide TITLE        "Public Health Planning and Analysis"
  statewide DESCRIPTION  entirely GIS -- "an introduction to Geographic
                         Information Systems (GIS)... buffering, layering, and
                         spatial queries"
  UWF                    "Public Health Planning and Analysis" -- programme
                         planning, implementation, evaluation, needs
                         assessment. ZERO GIS. Backs the TITLE.
  USF                    "Introduction to Public Health Geographic Information
                         Systems". Backs the DESCRIPTION.

⚠⚠⚠ The carriers SPLIT, one on each side = branch 4 of the batch-208/215
title/description test (the HFT4252 shape, batch 218): the test returns NO
ANSWER and the number carries TWO SUBJECTS.

⚠⚠ WHAT IS NEW: on HFT4252 the mechanism was invisible. Here the statewide
DESCRIPTION names its own author -- it calls the course "a required course in
the PROPOSED public health major in the Bachelor of Science in Health Sciences
[BSHS] degree program". That is one institution's degree, described while it was
still being proposed. So the likeliest history is that a carrier contributed a
description of ITS course onto a number whose TITLE already belonged to a
different subject, and the two were never reconciled.
⚠ Recorded as a NAMED MECHANISM for branch 4: a contributed description can
overwrite the record of a differently-titled course, leaving the state record
internally contradictory rather than merely stale. The tell is a description
that names a specific institution's degree programme.

*** AND THE GIS COURSE HAD NOWHERE BETTER TO GO ***
PHC?194 "Geographic Information Systems in Public Health" EXISTS -- and is
GRADUATE. Meanwhile Florida provides THREE upper-division planning numbers
(?140, ?142, ?143). So there is no undergraduate GIS-in-public-health number at
all. Misfiling by necessity again (batches 227/229), and the guide says there is
no "correct" number to look for.

*** SECOND: PHC4109 -- a title divergence that DISSOLVES, proved by a shared phrase ***
statewide "Scientific Basis of Public Health" vs UWF "Diseases in Human
Populations" looks like a divergence. It is not:
  statewide: "overview of SCIENTIFIC PRINCIPLES of public health and their
              application to public health problems with significant STATE,
              NATIONAL AND INTERNATIONAL impact"
  UWF:       "overview of the BIOLOGICAL BASIS of public health and the
              implications of major communicable and non-communicable diseases
              of public health significance at the STATE, NATIONAL, AND
              INTERNATIONAL levels"
⚠ The scope phrase is word-for-word identical. UWF's title is simply the more
informative one. Handled as REASSURANCE (batch 227 shape).
⚠⚠ AND I CHECKED THE OBVIOUS WRONG READING: "Diseases in Human Populations"
reads like epidemiology, and it is NOT -- Florida numbers epidemiology at least
four ways at undergraduate level (?030, ?024, ?040, ?048). The guide states the
distinction (what the diseases are vs how you study them) and points students
needing epidemiology at those numbers.
⚠ Statewide says the college-science background is RECOMMENDED; UWF says
students MUST have it. Same sentence, different force -- stated.
⚠⚠ Statewide says "OFFERED CONCURRENTLY WITH PHC 5XX3... graduate students will
be assigned additional work" -- the batch-186 dual-listing rule. TWO defects in
that one sentence: "PHC 5XX3" is a PLACEHOLDER (the batch-222/226 shape, but
appearing in the DESCRIPTION rather than the prerequisite field -- a new
location for it), and UWF's current entry does not mention the arrangement at
all. Guide states both consequences of dual-listing and hedges on whether it
still applies.

*** THIRD: PHC4464 -- clean, but USF's title is unsearchable ***
statewide "Introduction to Health Disparities & Social Determinants"; UWF
"Understanding Health Equity and Health Disparities"; USF ⚠ "Breaking Barriers:
Drivers to Public Health Solutions".
⚠ No subject divergence. But USF's is a recruitment-style title naming NEITHER
disparities NOR determinants -- so a student searching a catalogue will not find
it and a transfer evaluator will not recognise it. Stated as a practical problem
with an otherwise fine course.
⚠⚠ UWF's "health equity" addition is a TERMINOLOGY-ERA signal (batch 187), and a
benign one: disparity names a measured difference, equity names the goal, and
the field has moved toward equity language. Guide says learn both.

*** SOURCE: USF IDENTIFIED AS ACALOG AND CONTENT-BLOCKED -- NINTH institution ***
The register said "root 200 but no course-description path exposed; not yet a
route". Probed properly: catalog.usf.edu root answers 200 (75 KB) with acalog
markers; content.php returns an EMPTY 202; Coursedog bootstrap says the host
"does not exists". ⚠ So USF joins the acalog content-blocked pattern -- FSW,
TSC, CF, Polk State, Santa Fe, FAMU, St. Johns River State, Florida Poly, USF.
⚠⚠ That converts an "unidentified lead" into a settled negative, which per the
batch-215 platform rule saves future sessions from probing hopefully. USF is a
carrier on 2 of this batch's 3 courses, so it matters.

⚠ FGCU re-probed at session start (bsc): still empty 202. REVIEW_QUEUE 104 open.

*** DISTRIBUTION TEST ***
hs_credit 825/825 blank = boilerplate. transferable 824 EL / 1 NY and
dual_enrollment 788 Y / 36 N -- survey flags both "discriminating" but at 0.1%
and 4% these are near-universal by the batch-221 threshold rule. None of the
three targets is an exception. Nothing claimed in the guides.

Prefix: 599 live ids, 452 single-carrier (75%), max 6 carriers -- ⚠ note the
LOW maximum: no PHC course is widely carried, which is itself worth knowing.
Sources: UWF PDF (all three), statewide CSV. USF unreadable (acalog).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
USF = 'University of South Florida'

# Shared block -- the Florida data portal, which is the right source for any
# Florida-focused assignment in all three courses.
FL = ('*** FOR ANY FLORIDA-FOCUSED ASSIGNMENT USE FLHealthCHARTS, the Department of Health county-level '
      'data portal - free, public, and the right source. ')

NEW = {

  'PHC4109': {
    'title': 'Diseases in Human Populations',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'No formal course prerequisite is recorded. ⚠ BUT THE STATE CALLS THE SCIENCE BACKGROUND A '
      'RECOMMENDATION AND THE CARRIER CALLS IT A REQUIREMENT: UWF says students "MUST have at least one '
      'semester of a college science such as biology" before enrolling. Registration may not stop you; '
      'the course is built on it. Get college biology first. '
      '*** THE TITLE DIVERGENCE IS NOT ONE. Statewide "Scientific Basis of Public Health" and UWF '
      '"Diseases in Human Populations" share their scope phrase word for word - UWF simply has the more '
      'informative title. '
      '*** IT IS NOT EPIDEMIOLOGY. This course asks WHAT the diseases are; epidemiology asks HOW YOU '
      'FIND OUT. Florida numbers epidemiology at least four ways at undergraduate level (PHC?030, ?024, '
      '?040, ?048) - take one of those if that is what you need. '
      '*** THE STATE SAYS IT MAY BE DUAL-LISTED with a graduate course, so taking it may block taking '
      'the graduate version for credit later. Ask before registering if you plan an MPH here.'),
    'offering_notes': {
      'summary': ('One public carrier (UWF) at 3 credits. No institution publishes contact hours '
                  'anywhere in the PHC prefix.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': "Florida's 1:15 convention on 3 credits.",
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Diseases in Human Populations', 'credits': 3, 'contact_hours': None,
         'note': ('Sole public carrier. College of Health, Department of Public Health. "Overview of the '
                  'biological basis of public health and the implications of major communicable and '
                  'non-communicable diseases of public health significance at the state, national, and '
                  'international levels. Diseases contributing to national and global health '
                  'disparities and strategies for reducing disease burden are discussed." States the '
                  'college-science background as a REQUIREMENT where the statewide record calls it a '
                  'recommendation. Its current entry does NOT mention the concurrent graduate offering '
                  'the statewide description describes. No Gordon Rule designation recorded.')},
      ],
    },
  },

  'PHC4140': {
    'title': 'Public Health Planning and Analysis',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE statewide or at either carrier. '
      '*** THIS NUMBER CARRIES TWO DIFFERENT COURSES AND THE STATE RECORD DOES NOT SETTLE WHICH. The '
      'statewide TITLE says public health PLANNING; the statewide DESCRIPTION is entirely GIS. UWF '
      'teaches planning, implementation, evaluation and needs assessment, with NO GIS. USF teaches '
      '"Introduction to Public Health Geographic Information Systems". The carriers split, one on each '
      'side. '
      '*** ASK BEFORE ADD/DROP, AND ASK ABOUT SOFTWARE: the GIS version needs ArcGIS or QGIS and a '
      'machine that runs it; the planning version needs a word processor. '
      '*** THERE IS NO "CORRECT" NUMBER TO LOOK FOR: Florida has three upper-division planning numbers and '
      'its only GIS-in-public-health number, PHC?194, is GRADUATE. '
      '*** ON TRANSFER say in one sentence which course it was; the transcript will not. ' + FL),
    'offering_notes': {
      'summary': ('Two public carriers at 3 credits teaching two different subjects - programme '
                  'planning and public health GIS. The statewide title backs one and the statewide '
                  'description backs the other.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Florida's 1:15 convention on 3 credits. The statewide description says the course "
                     'is ONLINE, which describes one carrier\'s delivery rather than the number. Budget '
                     'more than the hours if you are in the GIS version - learning software is slow.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Public Health Planning and Analysis', 'credits': 3, 'contact_hours': None,
         'note': ('College of Health, Department of Public Health. "Overview of public health planning '
                  'with an emphasis on the use of public health principles and theories of program '
                  'planning, implementation, and evaluation. Students will gain an understanding of the '
                  'complex factors that impact needs assessment. Case studies will be analyzed using '
                  'examples of national, state, or local health programs and interventions." MATCHES '
                  'THE STATEWIDE TITLE and contains no GIS.')},
        {'institution': 'USF', 'institution_name': USF,
         'title': 'Introduction to Public Health Geographic Information Systems',
         'credits': 3, 'contact_hours': None,
         'note': ('MATCHES THE STATEWIDE DESCRIPTION, which appears to be USF\'s own text - it calls the '
                  'course "a required course in the PROPOSED public health major in the Bachelor of '
                  'Science in Health Sciences [BSHS] degree program". USF runs on acalog, which serves '
                  'its front pages but returns empty responses for course content, so its own entry '
                  'could not be read; the syllabus is the authority.')},
      ],
    },
  },

  'PHC4464': {
    'title': 'Health Disparities and Social Determinants of Health',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE statewide (the field reads "NONE") or at either carrier - open to students outside public '
      'health. '
      '*** THREE TITLES, ONE COURSE. Statewide "Introduction to Health Disparities & Social '
      'Determinants"; UWF "Understanding Health Equity and Health Disparities"; USF "Breaking Barriers: '
      'Drivers to Public Health Solutions". No subject divergence was found. '
      '*** BUT USF\'S TITLE NAMES NEITHER DISPARITIES NOR DETERMINANTS, so a student searching a '
      'catalogue will not find it and a transfer evaluator will not recognise it. Send the syllabus and '
      'say what the course covers. '
      '*** "EQUITY" AND "DISPARITY" ARE NOT INTERCHANGEABLE: a disparity is a measured difference, '
      'equity is the goal. The field has moved toward equity language; learn both terms because you '
      'will meet both in the literature and in job adverts. ' + FL),
    'offering_notes': {
      'summary': ('Two public carriers at 3 credits, same subject under three different titles. No '
                  'contact hours published.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': "Florida's 1:15 convention on 3 credits; both carriers list 3.",
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Understanding Health Equity and Health Disparities', 'credits': 3,
         'contact_hours': None,
         'note': ('College of Health, Department of Public Health. "Introduces students to social '
                  'determinants of health, health equity, and health disparities in the United '
                  'States... the societal impacts of racism, poverty, and inequity... Students will '
                  'explore sources of data for health disparities analysis... the role of major '
                  'national stakeholders and programs... implementing evidence-based strategies for '
                  'eliminating health inequalities." NOTE the scope is THE UNITED STATES, where the '
                  'statewide description does not specify.')},
        {'institution': 'USF', 'institution_name': USF,
         'title': 'Breaking Barriers: Drivers to Public Health Solutions', 'credits': 3,
         'contact_hours': None,
         'note': ('A recruitment-style title naming neither disparities nor determinants, though '
                  '"drivers" is a reasonable synonym for determinants. USF runs on acalog and returns '
                  'empty responses for course content, so its own description could not be read; title '
                  'and credits are from the statewide record.')},
      ],
    },
  },

}


def main():
    meta = json.load(open(META, encoding='utf-8')) if os.path.exists(META) else {}
    before = len(meta)
    overlap = sorted(set(meta) & set(NEW))
    if overlap:
        print('NOTE overwriting existing meta entries: %s' % ', '.join(overlap))
    for cid, m in sorted(NEW.items()):
        n = len(m['prerequisites'])
        print('%-9s prerequisites %4d chars%s' % (cid, n, '   *** OVER 1000 ***' if n > 1000 else ''))
    meta.update(NEW)
    with open(META, 'w', encoding='utf-8') as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print('meta.json: %d -> %d entries' % (before, len(meta)))


if __name__ == '__main__':
    main()
