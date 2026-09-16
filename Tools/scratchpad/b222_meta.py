"""Batch 222 metadata -- COM, five queued rows plus one substitution.

*** THE SUBSTITUTION, stated plainly ***
COM4564C was queued. Its ONLY carrier is Keiser University -- PRIVATE. Zero
public carriers, and the visitor guide-request queue is empty, so the
2026-09-11 override does not apply. Under Ron's public-institution scope
rule the queued id is unwritable.

The BARE number COM4564 is carried by UWF (public) under the SAME statewide
title and the same statewide description -- it is the course the queue row
named. So COM4564C is marked SKIPPED with its reason and COM4564 is written
instead. This is not a silent substitution: same subject, same statewide
record, different suffix, and the guide explains the suffix to the reader.

This is a FIFTH outcome for the batch-219 C-suffix diagnostic, which had
three: same institution carries both / different institutions carry the two
forms / nobody carries one of them. The new one is PRIVATE-ONLY C FORM --
the id is real, it just has no carrier this project may write from.

All six are 3 credits, no suffix -> 45 contact hours. UCF publishes 0 lab
hours on COM4110, COM4120 and COM3311, corroborating it a fourth batch
running.

*** DEFECTIVE STATEWIDE PREREQUISITES, three different ways in one prefix ***
  COM4301  "COM 2XXX INTRODUCTION TO COMMUNICATION STUDIES" -- 2XXX is a
           PLACEHOLDER, not an identifier. Second instance of the batch-209
           corrupt-token shape after ADV4802's "ADV U101C".
  COM4120  names COM 3311, carried by UCF ALONE -- and UCF does not require
           it. Dangles at UWF, which does not carry the number at all.
           NOTE this is NOT the batch-221 sector mechanism: both carriers
           are SUS. Simpler cause -- one carrier contributed it.
  COM4564  names "COM4561 Social Media Content Development" -- that is
           UWF's LOCAL title; the statewide title is Social Media Campaigns.
           Confirms the batch-200 finding with the carrier list behind it.

Stratified distribution test (batch-220 rule): hs_credit, transferable and
dual enrolment are all uniform across the prefix. Pure boilerplate; said
once per guide and briefly.

Prefix: 370 live ids, 308 single-carrier (83%) -- the HIGHEST single-carrier
share of the sixteen prefixes measured. Max 10 carriers.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
UCF = 'University of Central Florida'
FIU = 'Florida International University'
UNF = 'University of North Florida'

# Shared block -- the Gordon Rule grade condition. Two of the six carry a
# designation, and the C-or-higher trap is the part students do not know.
GORDON = ('GORDON RULE at UWF: a grade of C or HIGHER is required for it to satisfy the writing '
          'requirement - a C-minus passes the course and does not count. Designation is made by the '
          'INSTITUTION, not the number, so confirm against your own school list.')

NEW = {

  'COM2713': {
    'title': 'Writing for the Communication Professions',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF: ENC 1101 AND ENC 1102 (both halves of freshman composition). Florida statewide: none. '
      'Take the gate as a signal - the grammar component moves fast and the AP Style material '
      'assumes it. '
      '*** TAKE IT EARLY. At UWF this starts a FOUR-COURSE CHAIN: COM2713 -> COM3471 -> COM4561 -> '
      'COM4564, each naming the last as its prerequisite, and COM4564 additionally requires 75 '
      'completed credit hours. Starting this in the junior year leaves no room. *** THE PORTABLE '
      'SKILL IS AP STYLE - arbitrary, detailed, non-negotiable in the workplace, and an editor reads '
      'copy that ignores it as evidence you have never worked in the field. *** ' + GORDON),
    'offering_notes': {
      'summary': ('One public carrier (UWF) at 3 credits. A private institution also carries the '
                  'number and is excluded under the public-institution scope rule. THREE different '
                  'titles attach to this one number (statewide, UWF, and the private carrier) but '
                  'the descriptions agree almost word for word - three names, one course.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("UWF publishes no contact hours. 45 is Florida's convention for a 3-credit "
                     'course with no C or L suffix (Ron, 2026-09-15). Expect more: a writing course '
                     'is assessed on produced work and the revision cycles take the time.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Introduction to the Communication Professions', 'credits': 3,
         'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite: ENC 1101 AND ENC 1102. '
                  'Writing for advertising, public relations and journalism; grammar; newswriting, '
                  'PR writing and advertising copy; ASSOCIATED PRESS STYLE. "Meets College-Level '
                  'Communication Skills Requirement" = the Gordon Rule WRITING half, and the flat '
                  'file confirms gordon_rule + gordon_writing. Department of Communication, Col of '
                  'Arts, Soc Sci and Human. NOTE the statewide title is Writing for the '
                  'Communication Professions; UWF renamed it.')},
      ],
    },
  },

  'COM3471': {
    'title': 'Social Media and Communication',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF: COM 2713. FIU: none, and the statewide record also says NONE - take your own school gate. '
      '*** SAME COURSE, DIFFERENT FUNCTION, and the prerequisite chain is what shows it. At UWF this '
      'is STEP 2 OF A FOUR-COURSE PROFESSIONAL TRACK (it gates COM4561 and COM4564, and the word '
      '"Fundamentals" in UWF\'s title is a statement about position). At FIU it is a STANDALONE '
      'ELECTIVE on effects with nothing published behind it. If you want the track, take it early; '
      'if you are transferring, do not assume a follow-on course exists. *** EXPECT THEORY, NOT '
      'MARKETING - affordances, self-presentation, context collapse, networks, algorithmic curation. '
      'Campaign execution is COM4561; running a team is COM4564. *** The (U) in the statewide title '
      'means upper division and nothing more.'),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits. Same subject; what differs is the role it plays in '
                  'the degree - foundational at UWF, terminal at FIU. FIU uses the statewide '
                  'description almost verbatim; UWF\'s is broader, adding history, technology and '
                  'organisational/cultural implications.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit unsuffixed course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Fundamentals of Social Media Communication', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite: COM 2713. "Introduction to '
                  'the history, theory, technology, and uses of social media... the role of '
                  'individual choice, social influence, technological influence... implications of '
                  'social media for personal relationships, organizations, and culture." GATES '
                  'COM4561 and COM4564. Department of Communication.')},
        {'institution': 'FIU', 'institution_name': FIU,
         'title': 'Social Media Impact on Communication', 'credits': 3, 'contact_hours': None,
         'note': ('"This course will examine social media from a communication perspective; with a '
                  'focus on how media technologies influence the way we communicate (verbally and '
                  'nonverbally) with others" - the statewide description almost verbatim. No '
                  'prerequisite published. College of Communication, Architecture + The Arts.')},
      ],
    },
  },

  'COM4110': {
    'title': 'Business and Professional Communication',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      '*** UCF RESTRICTS THIS COURSE TO LISTED MAJORS AND MINORS - Communication, Human '
      'Communication, Advertising/PR, Communication and Conflict, Media Production and Management or '
      'Radio-TV majors, or Communication, Human Communication or Strategic Communication minors, '
      'plus a further course requirement. A major restriction is INVISIBLE until registration fails. '
      'If you are a business, engineering or science student - exactly who benefits most - you '
      'cannot simply enrol. Ask the Nicholson School, or look at UCF\'s SPC public speaking numbers, '
      'which are usually open. *** UWF requires SPC 3301 and publishes no major restriction. The '
      'statewide record says "consent of instructor", which matches neither carrier and is the least '
      'reliable of the three. *** THE TWO VERSIONS DIFFER: UCF is PRESENTATIONAL SPEAKING (and '
      'agrees with the statewide description); UWF is BROADER workplace communication. Syllabus '
      'test: count the graded speeches.'),
    'offering_notes': {
      'summary': ('Two SUS carriers, three catalogue records - UCF lists both a standard and an '
                  'HONORS section at this number. UCF publishes 0 lab hours and offers it Fall and '
                  'Spring. Statewide title and statewide description agree with each other and with '
                  'UCF; UWF is a broader superset rather than a different subject.'),
      'hours_source': 'mixed',
      'derived_contact_hours': 45,
      'derivation': ('Neither publishes a total, but UCF publishes 0 weekly lab/studio hours. 45 is '
                     'the convention for a 3-credit unsuffixed course and agrees with it.'),
      'offerings': [
        {'institution': 'UCF', 'institution_name': UCF,
         'title': 'Business and Professional Communication', 'credits': 3, 'contact_hours': None,
         'note': ('"Theoretical and practical training in effective PRESENTATIONAL SPEAKING for '
                  'business and professions." RESTRICTED to listed majors/minors plus a further '
                  'course requirement. Offered Fall and Spring. 0 lab hours. An HONORS section runs '
                  'under the same number - smaller, so more speaking time per student. Nicholson '
                  'School of Communication and Media.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Business and Professional Communication', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite: SPC 3301. "Practical '
                  'understanding of communication practices affecting the workplace. Emphasis on '
                  'managing work relationships, listening, organizational interviews, professional '
                  'presentations, communication technologies and multi-cultural diversity" - six '
                  'components, of which presenting is one. Department of Communication.')},
      ],
    },
  },

  'COM4120': {
    'title': 'Organizational Communication',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NEITHER carrier publishes one. '
      '*** THE STATEWIDE PREREQUISITE DOES NOT RESOLVE. Florida names COM 3311 (Quantitative Methods '
      'in Communication Research) - a number carried by UCF ALONE, and UCF does not require it. UWF '
      'does not carry COM3311 at all. Take your own catalogue, not the state record. The state\'s '
      'instinct is still sound: this course goes better after a research methods course. *** DO NOT '
      'CONFUSE IT WITH COM4110. That course is about YOUR communication performance - presenting, '
      'interviewing, listening. This one is about the ORGANISATION as a communication system - '
      'structure, networks, culture, power, change. They complement each other and neither '
      'substitutes for the other. *** Mild divergence: UCF and the state are INTERNAL (hierarchies, '
      'systems, networks); UWF adds STAKEHOLDERS and works from case studies.'),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits under the IDENTICAL title - no title divergence at '
                  'all, which is worth noting positively in a prefix that is 83% single-carrier. '
                  'UCF publishes 0 lab hours and offers it Fall and Spring.'),
      'hours_source': 'mixed',
      'derived_contact_hours': 45,
      'derivation': ('Neither publishes a total, but UCF publishes 0 weekly lab/studio hours. 45 is '
                     'the convention for a 3-credit unsuffixed course.'),
      'offerings': [
        {'institution': 'UCF', 'institution_name': UCF,
         'title': 'Organizational Communication', 'credits': 3, 'contact_hours': None,
         'note': ('"A study of communication functions and problems within the contexts of '
                  'hierarchies." No prerequisite published. Fall and Spring. 0 lab hours. Nicholson '
                  'School of Communication and Media. NOTE UCF is the ONLY Florida public carrier of '
                  'COM3311, the number the statewide record names as this course\'s prerequisite.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Organizational Communication', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit, no prerequisite. "Examines the dynamics of '
                  'communicating within organizations AND WITH STAKEHOLDERS. Students analyze case '
                  'studies of actual organizations and build skills related to teamwork, motivation, '
                  'morale-building, leadership, decision-making, and more." Department of '
                  'Communication.')},
      ],
    },
  },

  'COM4301': {
    'title': 'Communication Theory and Research Methods',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NEITHER carrier publishes one. '
      '*** THE STATEWIDE PREREQUISITE CONTAINS A PLACEHOLDER, NOT A COURSE: it reads "COM 2XXX '
      'INTRODUCTION TO COMMUNICATION STUDIES" - and COM 2XXX is not a valid SCNS identifier. Do not '
      'go looking for it. The intent (an intro communication course plus SPC 2600) is good advice, '
      'but the operative answer is your own catalogue. *** ACADEMIC OR INDUSTRY? UNF matches the '
      'statewide title - theory and methods, for GRADUATE SCHOOL. UWF teaches APPLIED research for '
      'the "converged communication industry". If grad school is possible, finish with a real '
      'project and a written report. Syllabus test: APA research report, or client insights deck? '
      '*** TAKE IT JUNIOR YEAR - you need a project and a referee before applications. ' + GORDON),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits teaching materially different versions - academic '
                  'methods at UNF, industry-applied research at UWF. UNF\'s catalogue is unreachable, '
                  'so its title (which matches the statewide one) is the evidence for its '
                  'characterisation.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit unsuffixed course. Expect more - methods courses are front-loaded '
                     'with reading and back-loaded with data collection and writing.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Applied Communication Research', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "Details the rationale and types of methods '
                  'and research conducted in the CONVERGED COMMUNICATION INDUSTRY... qualitative and '
                  'quantitative research methods commonly used in communication. Students will learn '
                  'how INDUSTRY research methods inform communication strategies and organizational '
                  'development." "Meets College-Level Communication Skills Requirement" = Gordon '
                  'Rule writing; flat file confirms gordon_rule + gordon_writing. Department of '
                  'Communication.')},
        {'institution': 'UNF', 'institution_name': UNF,
         'title': 'Communication Theory and Research Methods', 'credits': 3, 'contact_hours': None,
         'note': ('Carried at 3 credits under the statewide title. UNF\'s live catalogue is '
                  'client-rendered and returns no course content, and its archived catalogue PDFs '
                  'are served by a repository that refuses automated download, so its description '
                  'and prerequisite could not be read.')},
      ],
    },
  },

  'COM4564': {
    'title': 'Social Media Management',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF: (COM 3003) AND (COM 4561 OR COM 4566), plus COMPLETION OF 75 CREDIT HOURS - a standing '
      'requirement that is invisible in a prerequisite list and blocks registration outright. '
      '*** COM 3003 IS A SPLIT NUMBER carrying two subjects in Florida: statewide it is Human '
      'Communication (a theory survey), but AT UWF it is Integrated Advertising and Public Relations '
      'Concepts - and the UWF reading is the one this prerequisite means. Separate guides exist for '
      'both readings. *** THE FULL CHAIN IS FOUR TERMS: COM2713 -> COM3471 -> COM4561 -> COM4564. '
      'Decide in the first or second year or you cannot get here. *** DO NOT REGISTER FOR COM4564C - '
      'its only carrier is a PRIVATE institution and no Florida public college or university offers '
      'it. The unsuffixed number is what UWF teaches and what this guide describes.'),
    'offering_notes': {
      'summary': ('One public carrier (UWF) at 3 credits. The suffixed COM4564C is carried ONLY by a '
                  'private institution, so it is outside this repository\'s public-institution scope '
                  'and carries no meaning for a Florida public student - the subject is fully '
                  'covered at the unsuffixed number.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("UWF publishes no contact hours. 45 is Florida's convention for a 3-credit "
                     'course with no C or L suffix. Expect more - a live content calendar and a '
                     'reporting cycle impose a rhythm rather than deadlines.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Social Media Management', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite: (COM 3003) AND (COM 4561 OR '
                  'COM 4566); 75 credit hours completed. "Explores the day-to-day operations of a '
                  'social media communication team... overarching strategies, content calendars, '
                  'obtain and interpret social media analytics, and be able to WRITE METRIC REPORTS '
                  'FOR SENIOR MANAGEMENT... budgeting, workflow procedures, working '
                  'cross-departmentally, and managing special initiatives." Department of '
                  'Communication. NOTE the statewide prerequisite names "COM4561 Social Media '
                  'Content Development" - that is UWF\'s LOCAL title; the statewide title of '
                  'COM4561 is Social Media Campaigns, and UNF calls it Strategic Social Media.')},
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
    print('shared block: GORDON=%d chars' % len(GORDON))
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
