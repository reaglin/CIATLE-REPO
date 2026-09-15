"""Batch 220 metadata -- CCJ, the four queued upper-division electives.

All four are 3 credits, no suffix -> 45 contact hours under Ron's 2026-09-15
by-suffix rule. UCF's Kuali record for CCJ3450 publishes ZERO lab hours,
which corroborates the plain-suffix reading.

*** THE BATCH'S HEADLINE ***
CCJ3450 / CCJ2452 is a clean SECTOR NUMBER DIVERGENCE -- the upper-division
number is carried by UCF and UWF (both SUS) and the lower-division twin by
Polk State, Valencia, Florida Gateway, State College of Florida and
Tallahassee State (all five FCS). Second instance in this one prefix after
CCJ1020/CCJ2002, so it is a CCJ pattern rather than a coincidence.

*** A DISTRIBUTION-TEST CORRECTION ***
DS_Transferable1 across all ACTIVE CCJ rows reads 186 NOT-AUTO / 170
guaranteed, which looks strongly discriminating. Stratified by
DS_Course_Intent1 it collapses: the NOT-AUTO rows are 130 GRADUATE + 54
VARIABLE, and of 171 active UNDERGRADUATE rows, 169 are guaranteed. So the
field is boilerplate for the courses we actually write. See SOURCES.md 220.

hs_credit: 356/356 ELECTIVE and dual-enrolment 356/356 Y -- both boilerplate
in this prefix, so neither is spent out of the prerequisite budget.

Prerequisite budget: two short shared blocks, counted first; each field
drafted to ~850 characters (batch-209 rule).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
UCF = 'University of Central Florida'
FIU = 'Florida International University'
FAU = 'Florida Atlantic University'
SJRSC = 'St. Johns River State College'

# NOTE: the prefix-wide "check the number, not the title" caution (CCJ1020 vs
# CCJ2002, CCJ2452 vs CCJ3450) started as a shared block but only CCJ3450 had
# room for it, so it is written inline there and carried in every guide's HTML
# rather than spent out of three prerequisite budgets.

# Shared block -- the confidentiality limit. Every course in this prefix
# leads to work with protected records; the habit should start in school.
CONF = ('NEVER put case, victim, offender or personnel information into a consumer AI chat tool - '
        'it is a disclosure, and the habit has to start before your first internship.')

NEW = {

  'CCJ3193': {
    'title': 'Mental Health and Criminal Justice',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE - unusual for a 3000-level course, and it makes this genuinely open to non-majors '
      '(social work, psychology, nursing, education). '
      '*** THE TWO CARRIERS EMPHASISE DIFFERENT HALVES. UWF is SYSTEMS AND PRACTICE: prevalence in '
      'corrections, practitioner interaction, treatment programmes, and the mental health of '
      'criminal justice workers. FIU is FORENSIC-LEGAL: competency to stand trial, diminished '
      'capacity, insanity, community alternatives. SYLLABUS TEST - if competency and the insanity '
      'defence take more than a week you are in the FIU version. *** KNOW THE BAKER ACT (ch. 394) '
      'and MARCHMAN ACT (ch. 397); they do most of the work here. '
      'CONTENT NOTE: psychiatric crisis, incarceration and suicide. 988 Suicide and Crisis Lifeline '
      '(call or text); 211 for Florida crisis services; your counselling centre is free. ' + CONF),
    'offering_notes': {
      'summary': ('Two SUS carriers, both 3 credits, neither publishing contact hours, neither '
                  'requiring a prerequisite. The statewide description matches UWF almost verbatim, '
                  'so the state record is one carrier\'s reading rather than a neutral referee.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit course with no C or L suffix (Ron, 2026-09-15).'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Mental Health and Criminal Justice', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit, no prerequisite. "Explores the relationship '
                  'between mental health and the criminal justice system... prevalence of mental '
                  'illness in the correctional population, criminal justice professionals\' '
                  'interaction with individuals with mental illness, treatment programs and THE '
                  'MENTAL HEALTH OF CRIMINAL JUSTICE ACTORS." Dept. of Criminal Justice, Col of '
                  'Arts, Soc Sci and Human.')},
        {'institution': 'FIU', 'institution_name': FIU,
         'title': 'Crime and Mental Illness', 'credits': 3, 'contact_hours': None,
         'note': ('"Overview of major issues related to mental illness and crime and the role of '
                  'MENTAL HEALTH LAW AND PROCEDURE... from interactions with first responders, to '
                  'COMPETENCY TO STAND TRIAL, DIMINISHED CAPACITY and NOT GUILTY BY REASON OF '
                  'INSANITY defenses to sentencing and/or treatment and community-based '
                  'alternatives to incarceration." Green School of International and Public '
                  'Affairs. A materially different emphasis from UWF\'s.')},
      ],
    },
  },

  'CCJ3450': {
    'title': 'Criminal Justice Administration',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE published - but take the majors\' intro (CCJ3024) '
      'first; the course assumes you know what police, courts and corrections each do. '
      '*** SECTOR NUMBER DIVERGENCE, AND IT HITS THE STANDARD FLORIDA PATHWAY. CCJ3450 is carried '
      'ONLY by UCF and UWF (both SUS); the lower-division twin CCJ2452 by Polk State, Valencia, '
      'Florida Gateway, State College of Florida and Tallahassee State (ALL FCS). Same statewide '
      'title, same subject - but a 2000-level course CANNOT supply upper-division hours, so a '
      'transfer student may have to take it again. GET A WRITTEN ANSWER FROM THE RECEIVING '
      'DEPARTMENT FIRST. *** UCF IS FALL ONLY and has renamed it Criminal Justice Management and '
      'LIABILITY Issues: expect 42 USC 1983 and failure-to-train material. Florida supervisors also '
      'need Fla. Stat. 768.28 (sovereign '
      'immunity), 112.532 (officers\' rights) and ch. 119 (public records).'),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits. UCF publishes ZERO weekly lab/studio hours, '
                  'confirming a lecture course. The lower-division twin CCJ2452 is carried by five '
                  'FCS institutions under four different titles - title variation at that scale on '
                  'a shared number is branding, not divergence.'),
      'hours_source': 'mixed',
      'derived_contact_hours': 45,
      'derivation': ('Neither carrier publishes a total contact-hour figure, but UCF publishes 0 '
                     'weekly lab/studio hours. 45 is the convention for a 3-credit unsuffixed '
                     'course and agrees with that.'),
      'offerings': [
        {'institution': 'UCF', 'institution_name': UCF,
         'title': 'Criminal Justice Management and Liability Issues', 'credits': 3,
         'contact_hours': None,
         'note': ('"FIRST-LINE management processes affecting criminal justice agencies. '
                  'Familiarizes students with FUNDAMENTAL LIABILITY CONCEPTS regarding criminal '
                  'justice practices." 0 lab hours. OFFERED FALL ONLY. Dept. of Criminal Justice, '
                  'College of Community Innovation and Education. NOTE the flat file still records '
                  'the older title "The Criminal Justice Manager" - the catalogue is current, the '
                  'state record lags.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Criminal Justice Management and Organization', 'credits': 3,
         'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit, no prerequisite. "Acquaints student with '
                  'the basic management processes affecting criminal justice agencies, develops '
                  'the student\'s ability to analyze management problems and apply effective '
                  'interventions to those problems in POLICE DEPARTMENTS, COURTS, AND CORRECTIONS '
                  'AGENCIES." Broader across the three components than UCF\'s liability-framed '
                  'version.')},
      ],
    },
  },

  'CCJ3691': {
    'title': 'Sex Offenses and the Offender',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE recorded by the state or by either carrier. Take it after the majors\' intro (CCJ3024); '
      'it pairs best with victimology and criminal law. '
      '*** CONTENT NOTE, STATED PLAINLY: this course deals directly with sexual violence, including '
      'offences against children, and classes reliably include survivors. RAINN National Sexual '
      'Assault Hotline 1-800-656-HOPE (4673); 988 Suicide and Crisis Lifeline (call or text); every '
      'Florida county has a certified rape crisis centre via the Florida Council Against Sexual '
      'Violence. You may step out of a class and seek support without explaining yourself. *** '
      'FLORIDA IS THE CASE STUDY: registration (943.0435, 775.21), residency restrictions (775.215 '
      'plus far stricter LOCAL ordinances), and the JIMMY RYCE ACT civil commitment framework '
      '(ch. 394 Part V). Read the statutes. ' + CONF),
    'offering_notes': {
      'summary': ('Two carriers, one SUS and one FCS, both using the statewide title at 3 credits '
                  'with no prerequisite. St. Johns River State\'s catalogue is unreachable, so the '
                  'guide is written from UWF and the statewide record, which agree closely.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit course with no C or L suffix.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Sex Offenses and the Offender', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit, no prerequisite. "Comprehensive overview '
                  'of psychological, sociological and legal issues related to sex offenses. '
                  'Additionally, the sexual offenders and different typologies of the sex offender '
                  'will be discussed." Dept. of Criminal Justice, Col of Arts, Soc Sci and Human.')},
        {'institution': 'SJRSC', 'institution_name': SJRSC,
         'title': 'Sex Offenses and the Offender', 'credits': 3, 'contact_hours': None,
         'note': ('Carried at 3 credits under the statewide title. St. Johns River State runs on '
                  'acalog, which serves its front pages but returns empty responses for course '
                  'content, so its description, term pattern and any local prerequisite could not '
                  'be read. NOTE this is a 3000-level course at a Florida College System '
                  'institution - FCS schools offer upper-division work where they hold '
                  'baccalaureate authority.')},
      ],
    },
  },

  'CCJ4141': {
    'title': 'Restorative Justice',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE - unusual for a 4000-level course, and it makes this genuinely open to education, '
      'social work, psychology and conflict resolution students. '
      '*** IT INCLUDES PRACTICE, NOT ONLY READING. UWF: "hands on instruction in the use of '
      'restorative practices will be given" - circle process, facilitation and role play, assessed '
      'by demonstration. Attendance matters; you cannot make up a circle from notes, and role-play '
      'scenarios carry real emotional content. *** IT POINTS AT A REAL FLORIDA CREDENTIAL: Florida '
      'Supreme Court MEDIATOR CERTIFICATION through the Dispute Resolution Center, where county '
      'mediation has the most accessible requirements. Start logging facilitation hours now. '
      '*** Check that the syllabus EVALUATES rather than advocates: the evidence on victim '
      'satisfaction is strong, the evidence on reoffending more modest. ' + CONF),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits, neither publishing contact hours, neither '
                  'requiring a prerequisite. FAU titles it Restorative COMMUNITY Justice, which '
                  'suggests a community-capacity emphasis against UWF\'s dialogue-and-facilitation '
                  'emphasis - but FAU\'s catalogue is unreachable, so that is inferred from the '
                  'title and should be checked against the syllabus.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit course with no C or L suffix. Given the practical component, expect '
                     'the scheduled time to be used intensively.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Restorative Justice', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit, no prerequisite. "Introduces the '
                  'philosophy of restorative justice. Students critically analyze and compare '
                  'retributive justice with restorative justice. Explores various restorative '
                  'justice methodologies AND EVALUATION OF THOSE METHODOLOGIES. HANDS ON '
                  'INSTRUCTION in the use of restorative practices will be given." Dept. of '
                  'Criminal Justice, Col of Arts, Soc Sci and Human.')},
        {'institution': 'FAU', 'institution_name': FAU,
         'title': 'Restorative Community Justice', 'credits': 3, 'contact_hours': None,
         'note': ('Carried at 3 credits. FAU does not expose a public course catalogue at its '
                  'catalogue host, so its description, prerequisite and term pattern could not be '
                  'read. The word COMMUNITY in its title is the only evidence of emphasis and is '
                  'treated in the guide as an inference to verify, not a finding.')},
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
    print('shared block: CONF=%d chars' % len(CONF))
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
