"""Batch 225 metadata -- PET, the four queued rows.

Contact hours: 60 for PET3344C (C suffix), 45 for the three unsuffixed.

*** THE BATCH'S HEADLINE: A COHERENT INSTITUTIONAL PAIR ON TWO MISMATCHED NUMBERS ***
UWF's PET4434 and PET4820 carry WORD-FOR-WORD IDENTICAL descriptions
differing only in the age band:
  "designed to prepare physical education teachers and coaches to plan and
   implement developmentally appropriate sport and physical activities for
   [children and young adolescents | adolescents]"
It is a deliberate two-course developmental sequence. Neither statewide
number means anything like it:
  PET4434 statewide = Curriculum Integration Through Movement (elementary,
          teaching ACADEMIC skills through movement)
  PET4820 statewide = Teaching Team Sports I (softball, flag football,
          soccer methods)
And Florida provides NO undergraduate number for developmentally-appropriate
sport pedagogy by age band -- the nearest, PET6206, is graduate. So this is
the JOU4306/UF shape again: MISFILING BY NECESSITY, because the scheme has a
gap. Third instance in three batches; the pattern is now well established.

*** SECOND: a PREFIX divergence that explains a dormant number ***
PET4820's statewide subject (Teaching Team Sports I) is NOT taught by either
carrier, and PET4821 (Teaching Team Sports II) has NO carrier at all. But
PEO2011 carries the IDENTICAL statewide title and IS taught by FAMU, UCF and
FAU. The subject is alive; it moved prefix. Note the level difference too --
PEO2011 is LOWER and PET4820 UPPER, so they are not interchangeable for
upper-division hour requirements even where content matches.

*** THIRD: the private-only shape, INVERTED (batch 222) ***
COM4564C was a private-only C form with a public bare twin. PET3344 is the
mirror: the BARE number is carried only by a private institution and the C
form (PET3344C) is the public one. So the batch-222 rule needs stating
symmetrically -- check which FORM the public carrier uses, in either
direction. No substitution needed here; the queued C id is correct.

*** FOURTH: transferability is NOT boilerplate in PET ***
Stratified to 122 active undergraduate rows: 13 NOT AUTOMATICALLY
TRANSFERABLE, about 11% -- far above CCJ (2/171) or INR (5/124). And it is
NOT random: athletic training clinical courses (PET4672, PET4673, PET4624,
PET4625, PET4627), exercise testing and fitness assessment (PET4550,
PET4551, PET3385), plus PET4765. That is the batch-215 licensed-profession
logic -- hands-on clinical/assessment work a receiving programme must attest
to itself. A genuine, explicable pattern above the batch-221 threshold.
None of the four written here is among them.

*** Alternate-level pair test: NEGATIVE ***
PET2760 and PET4765 share the identical statewide title at two levels, which
looks like the batch-212 shape. grep for "MUST CHOOSE" over active PET rows
returns ZERO. So it is ordinary number fragmentation, not a formal pair.
The test correctly returns negative -- worth recording as a clean negative.

*** DANGLING PREREQUISITE, again ***
PET3344C's statewide prereq is PEO 2011 -- carried by FAMU, UCF and FAU, NOT
by UWF, its only public carrier.

Coaching is the most fragmented subject area measured: 20+ active statewide
numbers. Prefix: 344 live ids, 290 single-carrier (84%) -- the highest share
of any prefix measured. hs_credit and dual enrolment uniform.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
USF = 'University of South Florida'

# Shared block -- the two Florida safety issues that recur across every
# coaching and pedagogy course in this prefix.
SAFETY = ('FLORIDA SAFETY: heat illness is the year-round risk, and on concussion a coach RECOGNISES AND '
          'REMOVES - never diagnoses or clears. The NFHS courses are free.')

NEW = {

  'PET3344C': {
    'title': 'Fundamentals of Athletic Coaching',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'UWF publishes none. The STATEWIDE prerequisite names PEO 2011 - carried by FAMU, UCF and FAU, '
      'NOT by UWF, its only public carrier - so it does not resolve. Take your own catalogue. '
      '*** THE C SUFFIX IS THE PUBLIC FORM HERE. PET3344C is UWF; the BARE PET3344 is carried only by '
      'a private institution. If a document names PET3344, the course a Florida public student takes '
      'is PET3344C. *** COACHING IS THE MOST FRAGMENTED SUBJECT IN THIS CATALOGUE - over twenty active '
      'statewide numbers, including PET2760 and PET4765 sharing one title at two levels. KEEP YOUR '
      'SYLLABUS; it is the only thing identifying what you covered. Note PET4765 is classified NOT '
      'AUTOMATICALLY TRANSFERABLE. *** ' + SAFETY),
    'offering_notes': {
      'summary': ('One public carrier (UWF) of the C identifier at 3 credits; the bare PET3344 is '
                  'private-only and out of scope. UWF houses it in a College of Health rather than '
                  'education, which predicts a performance-science rather than teacher-preparation '
                  'emphasis.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("UWF publishes no contact hours. 60 is Florida's convention for a 3-credit "
                     'integrated C course (Ron, 2026-09-15); for a coaching methods course the '
                     'practical component is gymnasium or field time.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Athletic Coaching Methods', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit, no prerequisite published. "Specific methods '
                  'on how to effectively coach in athletic AND FITNESS settings. Emphasis is placed '
                  'on UNDERSTANDING ATHLETES, developing a clear COACHING PHILOSOPHY, planning for '
                  'practices, games and seasons, player development, managing the athletic or fitness '
                  'setting, and evaluating performance before, during, and between sport seasons." '
                  'College of Health, Department of Movement Sciences and Health.')},
      ],
    },
  },

  'PET3471': {
    'title': 'Sports Officiating',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE - neither UWF nor the statewide record lists one, so the course is open to any major. '
      '*** THIS IS ONE OF THE FEW COURSES IN A DEGREE THAT LEADS TO PAID WORK WITHIN MONTHS. '
      'Registration with a local association, a rules exam and a mechanics clinic is often the whole '
      'barrier; games pay per contest and the schedule fits around study. Officiating is short of '
      'officials nationally. GET REGISTERED WHILE TAKING THE COURSE: contact your FHSAA-listed local '
      'association, attend a clinic, sit the exam, work youth games first, and GET INSURANCE (NASO or '
      'your association). *** THE ABUSE PROBLEM IS REAL and is the leading reason officials quit. '
      'De-escalation is a teachable skill, ejection and reporting procedures exist, a mentor helps, '
      'and you may decline an assignment. *** If the section includes officiating real contests, '
      'expect evenings, weekends and travel beyond the scheduled hours.'),
    'offering_notes': {
      'summary': ('One public carrier (UWF) at 3 credits, no prerequisite. UWF\'s description is the '
                  'statewide description VERBATIM - institution and state agree completely, which is '
                  'comparatively rare in this catalogue.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("UWF publishes no contact hours. 45 is Florida's convention for a 3-credit "
                     'course with no C or L suffix. If supervised officiating of real contests is '
                     'included, treat it as a floor.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Sports Officiating', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit, no prerequisite. "An overview into sports '
                  'and experiences related to the world and PROFESSION of sports officiating. The '
                  'principles, practices, responsibilities, techniques, and methods employed in '
                  'sports officiating will be presented. OPPORTUNITIES FOR EMPLOYMENT in sports '
                  'officiating will be discussed" - the statewide description verbatim. College of '
                  'Health, Department of Movement Sciences and Health.')},
      ],
    },
  },

  'PET4434': {
    'title': 'Youth Sport Pedagogy',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'None published by UWF or by the state. '
      '*** THE NUMBER AND THE COURSE DO NOT MATCH. Statewide this number is CURRICULUM INTEGRATION '
      'THROUGH MOVEMENT - elementary PE, rhythmic dance, manipulative skills, and teaching ACADEMIC '
      'skills through movement. UWF teaches YOUTH SPORT PEDAGOGY - developmentally appropriate sport '
      'for children and young adolescents. NEVER TRANSFER THIS NUMBER ON THE NUMBER. *** TAKE IT '
      'WITH PET4820: UWF\'s two descriptions are '
      'identical except for the age band, and a nine-year-old differs from a sixteen-year-old in '
      'maturity, abstraction and injury risk. *** YOUTH SAFETY: early specialisation '
      'raises overuse injury and drop-out, and resistance training IS appropriate when supervised. '
      'Safeguarding applies - Florida abuse hotline 1-800-96-ABUSE. '
      + SAFETY),
    'offering_notes': {
      'summary': ('One public carrier (UWF) at 3 credits teaching a different subject from the one '
                  'the statewide title names. Half of a matched pair with PET4820 - the two UWF '
                  'descriptions are word-for-word identical apart from the age band. Florida provides '
                  'no undergraduate number for sport pedagogy by age band, so the mismatch is a gap '
                  'in the scheme rather than institutional carelessness.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("UWF publishes no contact hours. 45 is Florida's convention for a 3-credit "
                     'unsuffixed course. NOTE the statewide record flags this number as carrying '
                     'laboratory instruction despite the absent suffix - treat 45 as a floor, '
                     'especially if a teaching practicum is included.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Youth Sport Pedagogy', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit, no prerequisite. "Designed to prepare '
                  'physical education teachers and coaches to plan and implement DEVELOPMENTALLY '
                  'APPROPRIATE sport and physical activities for CHILDREN AND YOUNG ADOLESCENTS." '
                  'College of Health, Department of Movement Sciences and Health - not a college of '
                  'education, which is consistent with the sport pedagogy reading rather than the '
                  'statewide elementary-curriculum one.')},
      ],
    },
  },

  'PET4820': {
    'title': 'Teaching Team Sports I',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'None published by either carrier or by the state. '
      '*** THREE READINGS ON ONE NUMBER, AND THE STATEWIDE ONE HAS NO CARRIER. Statewide: TEACHING '
      'TEAM SPORTS I - teaching softball, flag football and soccer. USF: SPORTS SKILLS PROFICIENCY - '
      'your own execution. UWF: ADOLESCENT SPORT PEDAGOGY. Neither carrier teaches the statewide '
      'subject, and PET4821 has no carrier at all. *** THE STATEWIDE SUBJECT MOVED PREFIX: PEO2011 carries the IDENTICAL title and IS '
      'taught by FAMU, UCF and FAU. If you need "teaching team sports" for a requirement, look there '
      '- but note PEO2011 is LOWER division and this is UPPER. *** Test which reading you are in by '
      'what is GRADED: your own skill = proficiency; lesson plans and a teaching episode = pedagogy; '
      'sport-by-sport progressions = methods. *** Take it with PET4434. ' + SAFETY),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits teaching two different courses, NEITHER of which is '
                  'the statewide subject. Half of a matched UWF pair with PET4434. The statewide '
                  'subject is alive under a different prefix at PEO2011 (FAMU, UCF, FAU), and the '
                  'statewide sequel PET4821 has no carrier.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit unsuffixed course. Treat as a floor if a teaching practicum or '
                     'gymnasium time is involved.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Adolescent Sport Pedagogy', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit, no prerequisite. "Designed to prepare '
                  'physical education teachers and coaches to plan and implement DEVELOPMENTALLY '
                  'APPROPRIATE sport and physical activities for ADOLESCENTS" - identical to UWF\'s '
                  'PET4434 apart from the age band. College of Health, Department of Movement '
                  'Sciences and Health.')},
        {'institution': 'USF', 'institution_name': USF,
         'title': 'Sports Skills Proficiency', 'credits': 3, 'contact_hours': None,
         'note': ('Carried at 3 credits. USF exposes no public course-description path, so its '
                  'description, prerequisite and term pattern could not be read and the title is the '
                  'only evidence of content. A proficiency reading assesses the student\'s own skill '
                  'execution rather than their teaching of it - a third distinct subject on this '
                  'number, and an inference to verify against the syllabus.')},
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
    meta.update(NEW)
    with open(META, 'w', encoding='utf-8') as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print('meta.json: %d -> %d entries' % (before, len(meta)))
    print('shared block: SAFETY=%d chars' % len(SAFETY))
    over = 0
    for k in sorted(NEW):
        p = NEW[k]['prerequisites'] or ''
        flag = ''
        if len(p) > 1000:
            flag = '  <-- OVER 1000'
            over += 1
        print('  %-9s %d cr  %3d hrs  prereq %4d chars%s'
              % (k, NEW[k]['credits'], NEW[k]['contact_hours'], len(p), flag))
    print('%d of %d over the limit' % (over, len(NEW)))


if __name__ == '__main__':
    main()
