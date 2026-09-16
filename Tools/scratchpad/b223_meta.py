"""Batch 223 metadata -- INR, the five queued rows. Completes the prefix's queue
(INR2002, INR4102, INR4334, INR4403 were pushed earlier).

All five are 3 credits, no suffix -> 45 contact hours. UCF publishes 0 lab
hours on INR4060, INR4224 and INR4502 -- a fifth consecutive batch.

*** THE BATCH'S HEADLINE: MISFILING, and the cleanest instance yet ***
INR3503 is statewide MODEL UNITED NATIONS, and the statewide DESCRIPTION
agrees with the title ("prepares students to represent an assigned country
in a national Model United Nations"). FAMU matches. UWF teaches
INTERNATIONAL ORGANIZATIONS on it.

Three independent things make it misfiling rather than a judgement call:
  1. statewide title and description AGREE (batch-208 test -> state is the
     reference)
  2. Florida numbers International Organizations separately TWICE, and NINE
     public institutions use those numbers:
        INR3502  FAMU, FIU, FAU, FSU, UF
        INR4502  USF, UCF, FGCU
  3. *** FAMU CARRIES BOTH INR3502 AND INR3503 AND FILES THEM CORRECTLY ***
     -- which proves the two are distinct courses and the distinction is
     workable. That is the strongest misfiling evidence this project has
     found: an institution demonstrating the correct filing on the same
     two numbers.

NOTE the honest qualification, which is in the guide: UWF's course DOES
contain the Model UN skills (position papers, committee procedure,
extemporaneous speaking, a simulation). What differs is the frame -- at UWF
the simulation serves a course about institutions; at FAMU the course serves
the simulation.

*** SECOND FINDING: the SPM3104 shape, in INR4061 ***
Statewide title "Conflict, Security AND PEACE STUDIES in INR"; statewide
description promises "conflict resolution and post-conflict reconstruction".
Both carriers deliver conflict/war (UWF the bargaining model; FGCU
"International Armed Conflicts"). And the missing half IS separately
numbered -- INR4062 "War, Peace and Conflict Resolution" -- which is
classified GRADUATE and has NO Florida public carrier at all. So peace
studies has no undergraduate home in this prefix. The guide says so and
sends the reader to other prefixes.

*** THRESHOLD TEST, third confirmation (batch 221 rule) ***
survey.py called hs_credit, transferable AND dual enrolment "discriminating"
in INR -- on counts of 477 vs 1. Stratified to 124 active undergraduate
rows: hs_credit 124/124 elective; transferable 119 GUAR / 5 NOT-AUTO. All
boilerplate. The five NOT-AUTO rows are worth keeping though, and two are
student-facing: INR4270 Study Abroad and INR4927 ADVANCED MODEL UNITED
NATIONS. The INR3503 guide names the latter.

Prefix: 306 live ids, 226 single-carrier (74%), max 30 carriers (INR2002).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
UCF = 'University of Central Florida'
FSU = 'Florida State University'
FGCU = 'Florida Gulf Coast University'
FAMU = 'Florida A&M University'

# Shared block -- INR2002 is carried by 30 public institutions, more than any
# other number in the prefix, and every one of these courses assumes it.
INTRO = ('TAKE INR2002 FIRST even where not required - it is assumed background, and thirty Florida '
         'public institutions carry it.')

NEW = {

  'INR3503': {
    'title': 'Model United Nations',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'Neither carrier publishes one; the statewide record lists none. '
      '*** THE TWO CARRIERS TEACH DIFFERENT COURSES AND ONE IS USING THE WRONG NUMBER. Statewide title '
      'AND description both say MODEL UNITED NATIONS ("prepares students to represent an assigned '
      'country in a national Model UN"), and FAMU matches. UWF teaches INTERNATIONAL ORGANIZATIONS on '
      'it - though its version does include position papers, committee procedure and a simulation. '
      'Florida numbers International Organizations separately TWICE (INR3502: FAMU, FIU, FAU, FSU, UF; '
      'INR4502: USF, UCF, FGCU) - nine institutions - and FAMU CARRIES BOTH NUMBERS AND FILES THEM '
      'CORRECTLY. *** IF YOU WANT COMPETITION EXPERIENCE, JOIN THE MODEL UN TEAM; the course alone may '
      'not supply it. *** Conference travel can mean several days out of state - ask about dates and '
      'cost. NOTE INR4927 Advanced Model UN is NOT automatically transferable.'),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits teaching materially different courses on one number. '
                  'FAMU matches the statewide record; UWF teaches International Organizations. FAMU '
                  'also carries INR3502 International Organizations separately, which is what makes '
                  'this misfiling rather than ambiguity.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit course with no C or L suffix (Ron, 2026-09-15). Expect more in the '
                     'simulation version - conference preparation is substantial and a conference '
                     'runs several days.'),
      'offerings': [
        {'institution': 'FAMU', 'institution_name': FAMU,
         'title': 'Model United Nations', 'credits': 3, 'contact_hours': None,
         'note': ('Matches the statewide title and description. FAMU runs on a platform that serves '
                  'its front pages but returns empty responses for course content, so its own '
                  'description and prerequisite could not be read. ALSO CARRIES INR3502 '
                  'International Organizations as a separate course.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'International Organizations', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "Modern international organizations are a '
                  'solution... This course will examine international organizations through '
                  'readings, briefings, and simulations... With a particular focus on the United '
                  'Nations, students then research and write position papers as well as practice '
                  'extemporaneous speaking and committee procedures... students will spend time in a '
                  'committee simulation." So the Model UN skills ARE present, inside a course about '
                  'institutions. Department of Government.')},
      ],
    },
  },

  'INR4060': {
    'title': 'Causes of War',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UCF: ENC 1102 or POS 2041 or consent of instructor - note UCF accepts FRESHMAN COMPOSITION, '
      'which effectively opens the course to students outside the major. UWF: none published. '
      'Statewide: POS 2041 or INR 2002 or C.I. '
      '*** SCOPE DIFFERS. UCF uses the statewide description verbatim - the research literature on '
      'MILITARIZED INTERSTATE CONFLICT, a term of art that excludes civil war and terrorism. UWF is '
      'broader, adding IRREGULAR WAR AND TERRORISM, the ETHICS of war, and the "new wars" and '
      'future-of-war debates. Syllabus test: do terrorism and just war theory get their own units? '
      '*** AT UWF THIS IS ONE OF THREE DISTINCT WAR COURSES: INR4060 broad and historical, INR4061 '
      'the rationalist bargaining model, INR4224 that theory applied to East Asia. They overlap less '
      'than the titles suggest. *** UCF offers it "OCCASIONAL" - not a fixed pattern, so take it when '
      'it appears. ' + INTRO),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits under the IDENTICAL title. UCF publishes 0 lab hours '
                  'and uses the statewide description verbatim; UWF is a superset adding irregular '
                  'war, ethics and the future of war. Not a divergence - scope breadth.'),
      'hours_source': 'mixed',
      'derived_contact_hours': 45,
      'derivation': ('Neither publishes a total, but UCF publishes 0 weekly lab/studio hours. 45 is '
                     'the convention for a 3-credit unsuffixed course and agrees with it.'),
      'offerings': [
        {'institution': 'UCF', 'institution_name': UCF,
         'title': 'Causes of War', 'credits': 3, 'contact_hours': None,
         'note': ('"The primary theoretical and empirical research explaining militarized interstate '
                  'conflict" - the statewide description verbatim. Prerequisite ENC 1102 or POS 2041 '
                  'or C.I. Offered OCCASIONAL. 0 lab hours. School of Politics, Security, and '
                  'International Affairs - a security-forward department with a large IR catalogue '
                  'including intelligence, cyberwarfare and space policy.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Causes of War', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit, no prerequisite published. "Causes and '
                  'evolution of war... war\'s origins and evolution; theories about the causes and '
                  'nature of war; arguments for a contemporary world of new wars; and theories about '
                  'the future of war," with WWI, the Cold War and Iraq as cases, plus "terrorism and '
                  'irregular war; and the moral/ethical dimensions of war." Department of '
                  'Government.')},
      ],
    },
  },

  'INR4061': {
    'title': 'International Conflict',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'None - neither carrier publishes one and the statewide record says NONE. '
      '*** THE NUMBER PROMISES PEACE STUDIES AND NEITHER CARRIER DELIVERS IT. Statewide title is '
      '"Conflict, Security AND PEACE STUDIES in INR" and the statewide description promises "conflict '
      'resolution and post-conflict reconstruction". UWF teaches the bargaining theory of war onset '
      'and termination; FGCU calls its version International Armed Conflicts. The dedicated number '
      'for the missing half, INR4062, is classified GRADUATE and has NO Florida public carrier - so '
      'peace studies has no undergraduate home in this prefix. Look to communication, sociology, '
      'criminal justice or psychology for mediation and conflict resolution. *** EXPECT FORMAL '
      'REASONING: this is the bargaining model (private information, commitment problems, '
      'indivisibility). Logical rather than computational - do not be put off. ' + INTRO),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits, no prerequisites. Both appear to deliver the '
                  'conflict half of a statewide record that promises conflict AND peace studies. '
                  'FGCU\'s catalogue was unreachable, so its title is the only evidence of emphasis.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit unsuffixed course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'International Conflict', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "Examines some of the primary theories of '
                  'the ORIGINS AND TERMINATION of interstate war... Do leaders start war to divert '
                  'attention from domestic problems? Does trade promote peace? Do alliances deter or '
                  'entrap?... Given that war is costly, why are the contending sides unable to reach '
                  'a settlement short of the major use of armed force? The course concludes with a '
                  'discussion of the termination of war." The bargaining model, taught properly, and '
                  'the attention to TERMINATION is unusual and valuable. Department of Government.')},
        {'institution': 'FGCU', 'institution_name': FGCU,
         'title': 'International Armed Conflicts', 'credits': 3, 'contact_hours': None,
         'note': ('Carried at 3 credits. FGCU\'s course-information service returned empty responses '
                  'across every prefix tested, including ones it certainly carries, so this is a '
                  'service-wide condition rather than evidence about the course - but its own '
                  'description could not be read.')},
      ],
    },
  },

  'INR4124': {
    'title': 'Statecraft',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'FSU: INR 2002. UWF: none published. '
      '*** THE TITLE MISLEADS. "Statecraft" suggests diplomacy, negotiation and the machinery of '
      'foreign policy. This is SECURITY STUDIES: competing visions of US GRAND STRATEGY, DETERRENCE '
      '(conventional and nuclear), COERCIVE DIPLOMACY, the tools of coercion, and the ETHICS OF USING '
      'FORCE. FSU says so outright - "introduces students to the field of security studies". If you '
      'want diplomacy as such, look at a diplomacy course (UCF carries INR4030). *** THE KEY '
      'DISTINCTION is deterrence (stopping someone starting) versus compellence (making someone stop '
      'or undo) - they sound alike and differ profoundly, because compellence demands a visible, '
      'verifiable concession. Almost every argument about sanctions and ultimatums turns on it. '
      + INTRO),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits under the identical title, both describing the same '
                  'course - an unusually clean pairing. UWF\'s entry names all three of the statewide '
                  'description\'s goals; FSU\'s catalogue entry covers the first, which is more likely '
                  'a difference in how much each catalogue prints than in what is taught.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit unsuffixed course.'),
      'offerings': [
        {'institution': 'FSU', 'institution_name': FSU,
         'title': 'Statecraft', 'credits': 3, 'contact_hours': None,
         'note': ('"Prerequisite: INR 2002. This course introduces students to the field of SECURITY '
                  'STUDIES. Provides an introduction to the competing visions of the place of the '
                  'U.S. in the world, the theoretical arguments behind each approach, and how the '
                  'various perspectives differ on central policy issues." NOTE the statewide '
                  'description is a three-goal syllabus written in the first person plural and '
                  'matches this closely - FSU appears to have contributed it, and by the prose-register '
                  'test it is a RECENT and reliable entry rather than the usual 1980s telegraphese.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Statecraft', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit, no prerequisite published. "Fundamental '
                  'questions, theoretical arguments and concepts in the area of foreign policy '
                  'analysis and decision making... core topics in statecraft such as DETERRENCE '
                  '(conventional and nuclear), COERCIVE DIPLOMACY, TOOLS OF COERCION, and the ETHICS '
                  'OF USING FORCE," plus several prominent cases. Reaches goals two and three of the '
                  'statewide description. Department of Government.')},
      ],
    },
  },

  'INR4224': {
    'title': 'East Asian Foreign Policies',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UCF: ENC 1102 or POS 2041 or consent of instructor. UWF: none published. '
      '*** THREE DIFFERENT SCOPES ATTACH TO THIS NUMBER. Statewide: East AND SOUTHEAST Asia, '
      'political, military and economic. UCF: contemporary foreign policies of Asian powers, China '
      'and Japan foremost. UWF: East Asian history since the late 19th century used to TEST THE '
      'THEORY OF WAR - uncertainty, commitment problems, war termination. One is a region course '
      'using theory; the other is a theory course using the region. Syllabus test: does the reading '
      'list open with a journal article on the causes of war, or a country survey? *** SOUTHEAST ASIA '
      'IS THE LIKELY GAP - ASEAN and the South China Sea claimants are where most of the region\'s '
      'diplomacy happens. Check the syllabus. *** LANGUAGE IS THE CAREER DIFFERENTIATOR: Mandarin, '
      'Japanese and Korean are State Department critical languages with funded study. Start early.'),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits teaching materially different courses - a '
                  'contemporary regional survey at UCF, a theory-and-history course at UWF. The '
                  'statewide description promises East AND Southeast Asia and political, military and '
                  'economic aspects; neither carrier foregrounds Southeast Asia.'),
      'hours_source': 'mixed',
      'derived_contact_hours': 45,
      'derivation': ('Neither publishes a total, but UCF publishes 0 weekly lab/studio hours. 45 is '
                     'the convention for a 3-credit unsuffixed course.'),
      'offerings': [
        {'institution': 'UCF', 'institution_name': UCF,
         'title': 'Contemporary International Politics of Asia', 'credits': 3, 'contact_hours': None,
         'note': ('"Examinations of the foreign policies of major and secondary powers in Asia, with '
                  'particular attention to China and Japan." Prerequisite ENC 1102 or POS 2041 or '
                  'C.I. Offered OCCASIONAL. 0 lab hours. School of Politics, Security, and '
                  'International Affairs.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'War and Peace in East Asia', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "Uses East Asian international history since '
                  'the late 19th Century to explore some of the most enduring questions about '
                  'international politics... We begin in Part I by introducing two critical '
                  'components of the modern theory of war - UNCERTAINTY AND COMMITMENT PROBLEMS... '
                  'Part II begins with the Sino-Japanese War of 1894-1895." Shares its apparatus with '
                  'UWF\'s INR4060 and INR4061. Department of Government.')},
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
    print('shared block: INTRO=%d chars' % len(INTRO))
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
