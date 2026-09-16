"""Batch 224 metadata -- JOU, the four queued rows.

Contact hours: 45 for the three unsuffixed, 60 for JOU4313C.

*** THE BATCH'S HEADLINE: JOU4306 CARRIES TWO UNRELATED SUBJECTS ***
  UWF  Writing Critical Reviews  -- books, film, art, music. A writing course.
  UF   Advanced Data Journalism  -- "program in R... reproducible data
                                     analysis". A programming course.
They share no content, no skills and no textbook. That is the EEE4775
standard, and it is a -SCNS/-INST split candidate. See REVIEW_QUEUE.

*** WHY THE USUAL TESTS CANNOT ADJUDICATE IT -- and this is new ***
1. Title/description test: statewide title "Critical Journalism", statewide
   description "critical thinking and analysis as employed in the profession
   of journalism". They AGREE with each other and STILL FAIL TO
   DISCRIMINATE: arts criticism is critical thinking, data analysis is
   analysis. First case where an internally consistent statewide record
   admits BOTH readings.
2. Dedicated-number tell: dedicated numbers exist for BOTH readings and
   BOTH ARE DORMANT --
       JOU4305 Data Journalism              -- no carrier
       JOU4015 Journalism Culture/Criticism -- no carrier
   So neither carrier had a live alternative. The batch-203 tell is much
   weaker when the dedicated number is dormant.
3. Same-institution control (batch 223): applied here it EXPLAINS rather
   than convicts. UF carries JOU3305 Data Journalism and files the intro
   course correctly; what Florida lacks is an ADVANCED data number, so UF
   took an available one for a real two-course sequence.
   *** So the control works in BOTH directions -- at FAMU it proved a
   misfiling, at UF it exonerates one. Worth recording. ***

*** SECOND FINDING: the worst dangling prerequisite yet, JOU3342 ***
Statewide prereq is "JOU 3101 AND RTV 4301".
  UWF  carries JOU3101, NOT RTV4301   -> can satisfy half
  UNF  carries NEITHER                 -> can satisfy none
RTV4301 is carried by FAU and UF; JOU3101 by USF, FAU, UWF, UF. The two
institutions that COULD satisfy it (FAU, UF) do not carry JOU3342 at all.
So the prerequisite was contributed by a department that does not teach the
course.

*** THIRD: institutional signature (batch 219) ***
JOU4313C is carried by UF; the bare JOU4313 by UWF. No institution carries
both. Same course, two filings.

*** FOURTH: number fragmentation on environmental journalism ***
JOU3314 (FIU, UWF) and JOU4314 (FAU, UF) -- four institutions, two numbers,
one subject, split at the 3000/4000 boundary.

Stratified distribution test: hs_credit, transferable and dual enrolment all
uniform. Boilerplate.

Prefix: 241 live ids, 193 single-carrier (80%), max 9 carriers.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
UF = 'University of Florida'
UNF = 'University of North Florida'
FIU = 'Florida International University'

# Shared block -- Florida's open-government law is the reporter's single
# biggest practical advantage in this state, and it applies to every beat.
RECORDS = ('FLORIDA PUBLIC RECORDS: access is a CONSTITUTIONAL right here (Art. I s.24) plus ch. 119 '
           'and the ch. 286 Sunshine Law - among the broadest in the country. Learn to write a records '
           'request; it is the most transferable skill on any Florida journalism syllabus.')

NEW = {

  'JOU3314': {
    'title': 'Environmental Journalism',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF: JOU 3100 OR JOU 3101, and PERMISSION IS REQUIRED - a gate invisible until registration '
      'fails, so contact the department early. Statewide: JOU 3101. FIU explicitly welcomes students '
      'from other disciplines. '
      '*** THIS IS A PRODUCTION COURSE: UWF students COVER AN ENVIRONMENTAL BEAT for the semester. '
      'Sources answer when they answer and meetings are at night, so 45 hours is a floor. *** THE '
      'STATEWIDE DESCRIPTION IS FIU-SPECIFIC - it names "the Everglades and the rest of South '
      'Florida\'s ecosystem". Elsewhere in Florida the beat is springs, Apalachicola, red tide or '
      'coastal development; the competencies transfer, the ecosystem does not. *** Florida numbers '
      'this TWICE: JOU3314 (FIU, UWF) and JOU4314 (FAU, UF). ' + RECORDS),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits. The statewide description carries FIU\'s regional '
                  'scope. UWF is beat-based and digital-platform oriented and requires departmental '
                  'permission; FIU is open to non-majors.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit course with no C or L suffix (Ron, 2026-09-15). NOTE the statewide '
                     'record flags this number as carrying laboratory instruction despite the absent '
                     'suffix, and a semester-long beat is not contained by scheduled hours - treat '
                     '45 as a floor.'),
      'offerings': [
        {'institution': 'FIU', 'institution_name': FIU,
         'title': 'Environmental Journalism', 'credits': 3, 'contact_hours': None,
         'note': ('"Designed to bring science, the environment and journalism together, so that '
                  'STUDENTS FROM A VARIETY OF DISCIPLINES can develop news stories about issues '
                  'regarding the environment." College of Communication, Architecture + The Arts. '
                  'The statewide description\'s Everglades/South Florida emphasis appears to be '
                  'FIU\'s contribution.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Environmental Reporting', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite JOU 3100 OR JOU 3101. '
                  'PERMISSION IS REQUIRED. "Techniques required to research, report and write '
                  'environmental news stories for digital platforms. Students COVER AN ENVIRONMENTAL '
                  'BEAT during the semester... reporting ethics, the role of environmental reporters '
                  'in the community, the history of environmental journalism and utilization of both '
                  'government databases and the Internet... public health, public land management, '
                  'restoration of endangered species, and eco-activism." Department of '
                  'Communication.')},
      ],
    },
  },

  'JOU3342': {
    'title': 'Multimedia Journalism',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      '*** THE STATEWIDE PREREQUISITE CANNOT BE SATISFIED AT EITHER CARRIER. Florida names "JOU 3101 '
      'AND RTV 4301". UWF carries JOU3101 but NOT RTV4301 - half. UNF carries NEITHER. RTV4301 is '
      'carried by FAU and UF and JOU3101 by USF, FAU, UWF and UF - so the two institutions that could '
      'satisfy it do not teach this course at all. Take your own catalogue. The INTENT is sound: a '
      'reporting course first, and broadcast exposure if available. *** EXPECT A PRODUCTION COURSE - '
      'the deliverable is finished multimedia work. Check what equipment is provided, budget for an '
      'external microphone (audiences forgive poor pictures, not poor sound), and note DaVinci '
      'Resolve and Audacity are free. Your first video package will take three times as long as you '
      'plan. *** NEITHER carrier description was retrievable - read your syllabus.'),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits whose titles name the two halves of the statewide '
                  'description - UNF the craft (Multimedia Storytelling), UWF the phenomenon (Media '
                  'Convergence). NEITHER carrier\'s own course description could be read, which is '
                  'unusual and is stated in the guide.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit unsuffixed course. For a production course treat it as a floor - '
                     'editing time is not classroom time.'),
      'offerings': [
        {'institution': 'UNF', 'institution_name': UNF,
         'title': 'Multimedia Storytelling', 'credits': 3, 'contact_hours': None,
         'note': ('Carried at 3 credits. UNF\'s live catalogue is client-rendered and returns no '
                  'course content, and its archived catalogue PDFs are served by a repository that '
                  'refuses automated download, so its description could not be read. The title '
                  'points at the craft half of the statewide description.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Media Convergence', 'credits': 3, 'contact_hours': None,
         'note': ('Carried at 3 credits per Florida\'s course file, but the entry appears in NEITHER '
                  'UWF\'s published prefix listing NOR its catalogue search - both routes were '
                  'tried. The title points at the industry-phenomenon half. NOTE UWF\'s own JOU3101 '
                  'is titled "Digital and Multimedia Journalism", so UWF already teaches multimedia '
                  'in its reporting course - which suggests this number leans further toward '
                  'analysis. Department of Communication.')},
      ],
    },
  },

  'JOU4306': {
    'title': 'Critical Journalism',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      '*** THIS NUMBER CARRIES TWO UNRELATED COURSES. UWF: Writing Critical Reviews - reviews of '
      'books, film, art and music, a WRITING course, no prerequisite, and it carries a GORDON RULE '
      'writing designation (C or higher required; a C-minus passes and does not count). UF: Advanced '
      'Data Journalism - "program in R... reproducible data analysis", a PROGRAMMING course, '
      'prerequisite JOU 3305 or JOU 4318. They share no content, skills or textbook. *** THE '
      'PREREQUISITE IS THE TELL: if your catalogue gates this on a data journalism course you are in '
      'the data version; if it gates on nothing you are almost certainly in criticism. *** NEVER '
      'TRANSFER THIS NUMBER ON THE NUMBER - an evaluator cannot tell them apart. Send the syllabus '
      'and the work. *** Do not attempt the UF version without the prerequisite; it moves straight '
      'into R.'),
    'offering_notes': {
      'summary': ('Two SUS carriers teaching entirely different subjects at 3 credits each. The '
                  'statewide title and description agree with each other and still admit both '
                  'readings ("critical thinking and analysis as employed in the profession of '
                  'journalism"). Dedicated numbers exist for both readings - JOU4305 Data Journalism '
                  'and JOU4015 Journalism Culture and Criticism - and BOTH ARE DORMANT, so neither '
                  'carrier had a live alternative. A -SCNS/-INST split candidate; see REVIEW_QUEUE.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit unsuffixed course. Treat as a floor in both readings - the statewide '
                     'record flags laboratory instruction despite the absent suffix.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Writing Critical Reviews', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit, no prerequisite. "Devoted to writing reviews '
                  'of books, film, art, and music. Meets College-Level Communication Skills '
                  'Requirement" - the Gordon Rule WRITING half, and the flat file confirms '
                  'gordon_rule + gordon_writing. Department of Communication.')},
        {'institution': 'UF', 'institution_name': UF,
         'title': 'Advanced Data Journalism', 'credits': 3, 'contact_hours': None,
         'note': ('"Hands-on approach which blends journalism and data science to equip students to '
                  'be a full-time data journalist. Learn to PROGRAM IN R to replace spreadsheets and '
                  'databases with REPRODUCIBLE data analysis, and to clearly communicate results to '
                  'peers and lay audiences." Prerequisite JOU 3305 or JOU 4318. College of '
                  'Journalism and Communications. NOTE UF ALSO carries JOU3305 Data Journalism and '
                  'files it correctly - Florida simply provides no ADVANCED data journalism number, '
                  'so UF took an available one for a genuine two-course sequence.')},
      ],
    },
  },

  'JOU4313C': {
    'title': 'Sports Reporting',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'UF: JOU 3101. UWF (bare number): JOU 3100 OR JOU 3101. Statewide names "BASIC REPORTING" by '
      'subject rather than by number. The gate is right - this course adds a beat to reporting skills '
      'it assumes you have. '
      '*** THE C SUFFIX IS AN INSTITUTIONAL SIGNATURE: UF carries JOU4313C, UWF carries the bare '
      'JOU4313, and NO institution carries both. Same course, two filings - an evaluator will see a '
      'mismatch where there is none. *** STOP BEING A FAN IN PRINT. The people you cover are sources, '
      'not your team, and the beat\'s serious stories are concussion, compensation, abuse in youth '
      'sport, doping and stadium finance. *** SPORT RUNS ON ITS OWN SCHEDULE - night games, weekend '
      'fixtures, non-negotiable post-game deadlines, travel. Plan the term around it. *** If numbers '
      'interest you, UF also carries JOU4318 Sports Data Journalism - a smaller, better-paid route.'),
    'offering_notes': {
      'summary': ('One public carrier of the C identifier (UF); UWF carries the bare JOU4313. Same '
                  'title, same credits, both describing sports reporting - a filing difference, not '
                  'a course difference. UWF\'s description is broader, adding opinion writing, '
                  'contemporary issues and the history of American sports coverage.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ('UF publishes no contact hours. 60 is the convention for a 3-credit integrated C '
                     'course, and for a reporting course the "laboratory" is production time - '
                     'covering events, filing copy, being edited. Expect more: post-game deadlines '
                     'and away travel do not fit a timetable.'),
      'offerings': [
        {'institution': 'UF', 'institution_name': UF,
         'title': 'Sports Reporting', 'credits': 3, 'contact_hours': None,
         'note': ('"Instruction and practice in reporting sports with special emphasis on game '
                  'coverage and interviewing techniques. Includes features, sidebars, advances and '
                  'press conference coverage. Opportunities for publication of stories" - the '
                  'statewide description verbatim. Prerequisite JOU 3101. College of Journalism and '
                  'Communications. ALSO carries JOU4318 Sports Data Journalism.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Sports Reporting', 'credits': 3, 'contact_hours': None,
         'note': ('Carries the BARE number JOU4313, not the C form. 3 sh, may not be repeated for '
                  'credit. Prerequisite JOU 3100 OR JOU 3101. "Advanced writing and reporting course '
                  'that offers students a comprehensive exploration of the many facets and platforms '
                  'of sports journalism... original articles and OPINION PIECES... CONTEMPORARY '
                  'ISSUES facing sports and sports journalism as well as HISTORICAL PERSPECTIVES on '
                  'the coverage of sports in the United States." Department of Communication.')},
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
    print('shared block: RECORDS=%d chars' % len(RECORDS))
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
