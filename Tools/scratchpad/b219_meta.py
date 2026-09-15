"""Batch 219 metadata -- TPA, the seven writable design/craft numbers.

TPA3230C remains HELD (REVIEW_QUEUE item 25: three subjects, and no carrier
uses the C suffix). Not in this batch.

Contact hours settled by Ron 2026-09-15: BY SUFFIX. C = 60, no suffix = 45.
UCF's Kuali data supports it -- its 3-credit C courses publish 2 weekly
lab/studio hours and its plain 3-credit courses publish none.

  TPA3022   45   TPA3064C  60   TPA3601C  60   TPA4021C  60
  TPA4045C  60   TPA4061   45   TPA4077C  60

*** THE BATCH'S HEADLINE FINDING ***
Five of the seven queued C ids have a BARE TWIN carried by DIFFERENT
institutions -- so in TPA the suffix is largely an institutional signature,
not a description of the course. And lighting design I / scene design I each
run under TWO OR THREE competing statewide numbers. See SOURCES.md batch 219.

Prerequisite budget (batch-215 / batch-209 rules): two shared blocks, both
short, counted first; each prerequisite drafted to ~850 chars.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
UCF = 'University of Central Florida'
USF = 'University of South Florida'
FAU = 'Florida Atlantic University'
FIU = 'Florida International University'
FSU = 'Florida State University'
UF = 'University of Florida'

# Shared block 1 -- the prefix-level transfer reality. 78% single-carrier.
FRAG = ('TRANSFER ON PORTFOLIO AND SYLLABUS, NOT ON THE NUMBER: about 78% of TPA identifiers are '
        'carried by exactly ONE Florida public institution, and design courses are placed on work '
        'anyway.')

# NOTE on hs_credit: TPA DOES discriminate on that field (559 elective /
# 48 performing-fine-arts across the prefix), but all seven of these numbers
# are ELECTIVE, so it is stated once in each guide's transfer section rather
# than spent out of the prerequisite budget.

# Shared block 2 -- the design/craft axis. TPA-wide, per CLAUDE.md batch 208.
CRAFT = ('DESIGN vs CRAFT: different jobs, different unions (USA 829 designers, IATSE technicians). '
         'Learn both - the craft side pays first.')

NEW = {

  'TPA3022': {
    'title': 'Lighting Design I',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF: TPA 2200 OR TPA 2200C (technical theatre). Florida statewide: TPA 2000, 2200. '
      'FAU\'s own prerequisite could not be read - FAU exposes no public course catalogue. '
      '*** FLORIDA HAS TWO "LIGHTING DESIGN I" NUMBERS AND BOTH ARE ACTIVE: TPA3022 (FAU, UWF - '
      'this course) and TPA4020 (FSU, UF). A third, TPA3020, is named in UWF\'s own prerequisite '
      'for TPA4021C and is carried by NO Florida public institution. *** ' + CRAFT +
      ' This is the DESIGN course; TPA3223C is lighting TECHNOLOGY (equipment, dimmers, control) '
      'and a different career. 45 hours is the unsuffixed convention; '
      'unsuffixed course; UWF\'s light lab and production work push the real commitment '
      'well past it. ' + FRAG),
    'offering_notes': {
      'summary': ('Two public carriers, both SUS, both 3 credits, same title. Neither publishes '
                  'contact hours. FAU\'s catalogue is unreachable, so the guide is written from '
                  'UWF plus the statewide record.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit course with no C or L suffix. Ron settled the prefix-wide rule '
                     '2026-09-15: C = 60, plain = 45.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Lighting Design I', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite: TPA 2200 OR TPA 2200C. '
                  '"Introduction to the work of the lighting designer through theoretical design '
                  'projects and light lab projects... The light lab projects build the student\'s '
                  'ability to understand light and how to use light in a theatre situation." '
                  'Col of Arts, Soc Sci and Human, Department of Theatre.')},
        {'institution': 'FAU', 'institution_name': FAU,
         'title': 'Lighting Design 1', 'credits': 3, 'contact_hours': None,
         'note': ('Carried at 3 credits under the statewide title. FAU does not expose a public '
                  'course catalogue at its catalogue host, so its description, prerequisite and '
                  'any material fee could not be read.')},
      ],
    },
  },

  'TPA3064C': {
    'title': 'Scenic Design I',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'Florida statewide: TPA 2000 (introduction to theatrical design) and TPA 2200 (stagecraft). '
      'FAU is the only carrier and its catalogue is unreachable, so CONFIRM FAU\'S OWN GATE WITH '
      'THE DEPARTMENT. A stagecraft foundation is assumed either way. '
      '*** FLORIDA NUMBERS SCENE DESIGN I THREE WAYS: TPA3064C (FAU - this course), TPA3064 '
      '(UWF), TPA3060 (FIU, UF). UWF writes its own second-course prerequisite as "TPA 3060 OR '
      'TPA 3064", accepting either family - which is the clearest evidence they are the same '
      'course. *** THE C SUFFIX IS EARNED HERE: the statewide description opens "classroom and '
      'LABORATORY study" and requires SCALE MODELS, so 60 hours is right and the bench work is '
      'real. BUDGET FOR MATERIALS - board, foam core, blades and adhesives cost money across a '
      'term. ' + FRAG),
    'offering_notes': {
      'summary': ('One public carrier (FAU), 3 credits. Its catalogue is unreachable, so the '
                  'guide is written from the statewide record - which for this number is unusually '
                  'detailed - cross-read against UWF and FIU under their own numbers.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ('No carrier publishes contact hours. 60 is the convention for a 3-credit '
                     'integrated C course, and it is corroborated by the statewide description\'s '
                     'explicit reference to laboratory study and scale-model production.'),
      'offerings': [
        {'institution': 'FAU', 'institution_name': FAU,
         'title': 'Scenic Design 1', 'credits': 3, 'contact_hours': None,
         'note': ('Sole public carrier of this exact identifier, at 3 credits, under the statewide '
                  'title. FAU exposes no public course catalogue, so its description, prerequisite '
                  'and term pattern could not be read.')},
      ],
    },
  },

  'TPA3601C': {
    'title': 'Stage Management',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'UCF: a grade of C (2.0) or better in TPA 2600. *** OFFERED IN SPRING ONLY AT UCF - a '
      'once-a-year course costs a YEAR, not a term, if you miss it or clear the prerequisite '
      'late. Plan it a year ahead. *** UCF RECORDS A GORDON RULE DESIGNATION on this course, '
      'including the writing flag - so A GRADE OF C OR HIGHER IS REQUIRED for it to satisfy the '
      'requirement; a C-minus passes and does not count. Gordon Rule designation is made by the '
      'INSTITUTION, not the number, and Florida\'s two flags are entered independently, so '
      'confirm against UCF\'s own published list which component it satisfies. The unsuffixed '
      'TPA3601 at USF and UWF is a lecture course with no lab hours; UWF gates it on THE 2000 '
      'only, a much lower bar. GET FIRST AID AND CPR CERTIFIED - the statewide competency list '
      'names first aid and employers notice it.'),
    'offering_notes': {
      'summary': ('One public carrier of the C identifier (UCF), 3 credits, with 2 published '
                  'weekly lab/studio hours - the clearest evidence in this batch that a TPA C '
                  'suffix is real rather than a filing artefact. The unsuffixed TPA3601 is carried '
                  'by USF and UWF, both 3 credits, both without a lab component.'),
      'hours_source': 'mixed',
      'derived_contact_hours': 60,
      'derivation': ('UCF publishes 2 weekly lab/studio hours but no total contact-hour figure. '
                     '60 is the convention for a 3-credit integrated C course and agrees with the '
                     'published lab hours.'),
      'offerings': [
        {'institution': 'UCF', 'institution_name': UCF,
         'title': 'Stage Management: Techniques', 'credits': 3, 'contact_hours': None,
         'note': ('"Paperwork, structure, and tools used by Stage Managers." 2 weekly lab/studio '
                  'hours. Prerequisite: C (2.0) or better in TPA 2600. OFFERED SPRING ONLY. '
                  'GORDON RULE designation recorded, including the writing flag. School of '
                  'Performing Arts, College of Arts and Humanities.')},
      ],
    },
  },

  'TPA4021C': {
    'title': 'Lighting Design II',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'UWF: TPA 3020 OR TPA 3022. *** THE STATE RECORD\'S PREREQUISITE FOR THIS COURSE IS BROKEN. '
      'Florida names TPA 4020 Lighting Design I - a number UWF, the only carrier, DOES NOT OFFER '
      '(FSU and UF do). And TPA3020, named in UWF\'s own alternative, is carried by NO Florida '
      'public institution. THE REAL GATE AT UWF IS TPA3022. *** Florida runs two parallel '
      'lighting-design families: TPA3022 -> TPA4021C (FAU/UWF) and TPA4020 -> TPA4021 (FSU/UF) - '
      'same second number, different suffix, different first course, so an evaluator matching on '
      'identifiers can err in either direction. ' + CRAFT + ' Light lab, hang and focus sessions '
      'run when the theatre is free, often at night. ' + FRAG),
    'offering_notes': {
      'summary': ('One public carrier (UWF), 3 credits. The unsuffixed TPA4021 is carried by FSU '
                  'and UF, both 3 credits, both titled Lighting Design II - the second half of the '
                  'other numbering family.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ('No carrier publishes contact hours. 60 is the convention for a 3-credit '
                     'integrated C course, corroborated by UWF\'s description, which builds the '
                     'course on light lab projects alongside theoretical ones.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Lighting Design II', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite: TPA 3020 OR TPA 3022. '
                  '"Advances the study of the design process involved in lighting design... '
                  'Theoretical projects in a variety of design venues and types of theatre with '
                  'lab projects that further build the designer\'s resources." Col of Arts, Soc '
                  'Sci and Human, Department of Theatre.')},
      ],
    },
  },

  'TPA4045C': {
    'title': 'Costume Design I',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'Florida statewide: "PREVIOUS COURSES IN COSTUME" - named by SUBJECT, not by number, so the '
      'gate is a departmental judgement rather than a checkable rule. USF is the only carrier and '
      'its catalogue exposes no public course-description path, so CONTACT THE DEPARTMENT. The '
      'unsuffixed TPA4045 at UWF REQUIRES DEPARTMENTAL PERMISSION and lists TPA 2200 or TPA 2200C; '
      'a permission requirement is invisible until registration fails, so ask early. '
      '*** DESIGN OR CONSTRUCTION? Florida\'s competency list for this DESIGN number contains '
      'construction competencies (cutting, pattern development) and shares eight of its ten items '
      'with TPA3230, a construction course. Designer and draper are different jobs; LEARN BOTH. '
      '*** The statewide title promises a period survey no carrier describes; check the syllabus. '
      + FRAG),
    'offering_notes': {
      'summary': ('One public carrier (USF), 3 credits, whose catalogue is unreachable. The '
                  'unsuffixed TPA4045 is carried by UWF (Costume Design I, permission required) '
                  'and FSU (Costume Design for the Stage), both 3 credits. All three describe a '
                  'design studio; the statewide record describes a period survey with construction '
                  'content, and reads as a much older entry.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ('No carrier publishes contact hours. 60 is the convention for a 3-credit '
                     'integrated C course, and a costume design studio - rendering, swatching, '
                     'cutting - is bench work.'),
      'offerings': [
        {'institution': 'USF', 'institution_name': USF,
         'title': 'Design Studio: Costume Design', 'credits': 3, 'contact_hours': None,
         'note': ('Sole public carrier of this exact identifier, at 3 credits. USF\'s catalogue '
                  'host exposes no public course-description path, so its description, '
                  'prerequisite, term pattern and any material fee could not be read. Its title '
                  'names a design STUDIO and drops the historical survey the statewide title '
                  'foregrounds.')},
      ],
    },
  },

  'TPA4061': {
    'title': 'Scene Design II',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF: TPA 3060 OR TPA 3064 - an institution deliberately writing around a numbering problem, '
      'since Florida numbers scene design I three ways (TPA3060 at FIU/UF, TPA3064 at UWF, '
      'TPA3064C at FAU). FIU publishes no prerequisite. Florida\'s statewide prerequisite reads '
      '"PREVIOUS COURSE IN TECHNICAL" - apparently truncated, and in any case named by subject '
      'rather than number, so the gate is a departmental judgement. '
      '*** THE 45 HOURS UNDERSTATES THIS COURSE. Florida\'s own record FLAGS THIS NUMBER AS '
      'CARRYING LABORATORY INSTRUCTION even though the identifier has no C; the statewide '
      'description says the class consists of "lectures and IN-CLASS DESIGN WORK"; and FIU makes '
      'MODEL MAKING a core emphasis. Plan for studio hours well beyond the scheduled ones, and '
      'for material costs. *** ' + FRAG),
    'offering_notes': {
      'summary': ('Two public carriers, both SUS, both 3 credits, neither publishing contact '
                  'hours. UWF emphasises breadth of design problem and communication to the '
                  'director; FIU emphasises rendering technique and model making. Both are in the '
                  'statewide description.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit course with no C or L suffix (Ron, 2026-09-15). NOTE the statewide '
                     'record flags this number as carrying laboratory instruction despite the '
                     'absent suffix, so the derived figure is a floor.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Scene Design II', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite: TPA 3060 OR TPA 3064. '
                  '"Advanced projects in scene design examine the challenges involved in designing '
                  'in a variety of different venues and types of production. Expands the '
                  'designer\'s tools to communicate their design idea to the director." Col of '
                  'Arts, Soc Sci and Human, Department of Theatre.')},
        {'institution': 'FIU', 'institution_name': FIU,
         'title': 'Scenic Design II', 'credits': 3, 'contact_hours': None,
         'note': ('"Advanced skills in setting the mood of, and creating movement through a '
                  'theatrical space. Emphasis will be placed upon rendering Techniques and model '
                  'making." College of Communication, Architecture + The Arts. DATA NOTE: FIU\'s '
                  'course system also carries a stale duplicate record for this number showing '
                  '3.33 credits; the 3-credit record is the current one.')},
      ],
    },
  },

  'TPA4077C': {
    'title': 'Scene Painting',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'NONE - the statewide record and UWF both list no prerequisite. FOR A 4000-LEVEL COURSE '
      'THAT IS UNUSUAL AND WORTH ACTING ON: the course is open to students who have not worked '
      'through a design sequence, including students from other majors. Confirm with the '
      'department anyway, since an institution can impose a local permission or major '
      'restriction the state record does not show. '
      '*** CREDIT DIVERGES: UWF 3 (this identifier), FSU 3, USF 2 (both under the unsuffixed '
      'TPA4077). Two credits against a three-credit requirement leaves you short, and it surfaces '
      'at the final audit. *** UWF ASSESSES A MATERIAL AND SUPPLY FEE. SAFETY IS REAL - solvents, '
      'pigments, aerosols, foam dust; if a respirator is required, get it FIT TESTED. ' + CRAFT +
      ' The most directly employable course in the prefix.'),
    'offering_notes': {
      'summary': ('One public carrier of the C identifier (UWF), 3 credits, with a material and '
                  'supply fee. The unsuffixed TPA4077 is carried by FSU at 3 credits and USF at '
                  '2. No subject divergence anywhere - statewide title, statewide description and '
                  'every carrier agree; only the credit value and the suffix vary.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ('No carrier publishes contact hours. 60 is the convention for a 3-credit '
                     'integrated C course, and scene painting is almost entirely bench work.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Scene Painting', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. No prerequisite. "Practice in various '
                  'techniques of scene painting. Consideration of pigments, colour mixing, kinds '
                  'of paints, paint equipment and its care. MATERIAL AND SUPPLY FEE WILL BE '
                  'ASSESSED." Col of Arts, Soc Sci and Human, Department of Theatre.')},
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
    shared = len(FRAG) + len(CRAFT)
    print('shared blocks: FRAG=%d  CRAFT=%d  TOTAL=%d chars'
          % (len(FRAG), len(CRAFT), shared))
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
