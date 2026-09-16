"""Batch 229 metadata -- MUE (music education), the four queued rows.

Credits and contact hours, all no-suffix, Florida 1:15 convention, all derived
(NO institution publishes contact hours anywhere in the MUE prefix):
  MUE3423   2 cr / 30   (UWF's form, which matches the statewide description)
  MUE4344   3 cr / 45   (FGCU, sole carrier)
  MUE4411   4 cr / 60   (FSU's form -- FSU IS the statewide description's author)
  MUE4475   2 cr / 30   (UWF's form, which matches the statewide description)

*** THE PREFIX'S DEFINING PROPERTY: a CODED MATRIX, with a GAP ***

MUE names its methods courses by a systematic scheme -- course type x school
level x specialism -- written as abbreviations, e.g.
    MUS METH/COMP/K-12/ GEN MUSIC          (?344)
    TECH-SKILL-MAT/COMP/K-12/INSTR-ORCH    (?423)
    TECH-SKILL-MAT/COMP/K-12/INSTR-BAND    (?422)
    TECH-SKILL-MAT/COMP/K-12/VOC-CHORAL    (?421)
⚠ These are database field abbreviations, not course names. They are unreadable
to a student and they are what the site would otherwise display.

⚠⚠⚠ THE COMPREHENSIVE-K-12 ROW HAS NO UNDERGRADUATE INSTRUMENTAL METHODS SLOT.
?344 is general music; ?421/?422/?423 are the techniques-skills-materials
numbers; and the instrumental METHODS slot, ?348, is GRADUATE ONLY. So an
institution building an undergraduate instrumental methods course has nowhere
exactly right to put it.

*** HEADLINE: MUE4344 -- a misfiling, with the completest evidence yet ***

FGCU teaches "Teaching Instrumental Music" on the GENERAL MUSIC number. Three
independent pieces of evidence, which is one more than the usual case has:
  1. Statewide TITLE and DESCRIPTION agree with each other (both general music)
     -> branch 1 of the batch-208 test, so the carrier is the deviating party.
  2. ⚠⚠ FSU carries MUE3344 "Teaching General Music K-12" and its catalogue text
     is the statewide description WORD FOR WORD -- FSU both wrote it and uses
     the number correctly. The peer control CONVICTS.
  3. ⚠⚠⚠ UF carries MUE4422 "TEACHING INSTRUMENTAL MUSIC" -- the IDENTICAL
     TITLE at the IDENTICAL 3 credits -- on the instrumental-band number.

⚠⚠ But the CAUSE is the matrix gap above, not carelessness: two institutions hit
the same missing slot and worked around it in DIFFERENT DIRECTIONS (UF onto
?422, FGCU onto ?344). That is a NEW observation worth generalising -- a gap does
not merely displace one course, it FRAGMENTS the subject, because each carrier
picks a different neighbour. Batch 227 had one carrier working around a gap;
this is two, diverging.

*** SECOND: MUE4411 -- a 2x credit divergence EXPLAINED by the prerequisite ***

FSU 4 credits, UWF 2. The largest credit divergence recorded outside flight
training. The prerequisite chains say exactly why, and they are the finding:
  FSU  -- gated on MUE 3491-3492 (a TWO-COURSE choral conducting/literature
          sequence), plus concurrent MUE 3495r. You arrive able to conduct.
  UWF  -- gated on MUT 2117 (theory), COREQUISITE MUG 3104 (first conducting).
          You are learning to conduct at the same time.
⚠ So the two are not unequal versions of one course; they sit at DIFFERENT
POINTS IN THE SEQUENCE. Neither is wrong, and the transfer harm runs one way:
UWF -> FSU arrives 2 credits short AND without the 3491-3492 foundation.
This is the batch-185 prerequisite-as-signal diagnostic firing on POSITION
rather than on depth or subject -- a fourth thing it settles.

*** THIRD: MUE4475 -- two audiences, and the same-institution control EXPLAINS ***

UWF (2 cr) "Percussion Methods and Materials" -- for students "planning to
practice teach in band programs", with school observations. Matches statewide.
FAU (3 cr) "Advanced Percussion Literature and Pedagogy" -- explicitly for
"music majors in PERCUSSION PERFORMANCE", covering solo/ensemble literature and
⚠ "promotion and marketing" (i.e. building a private studio).
⚠⚠ FAU ALSO carries MUE2470 "Percussion Pedagogy and Methods" (1 cr), whose
description IS the school-teaching one. So FAU placed the school course
elsewhere and uses ?475 deliberately for a performance-track course. The
same-institution control (batch 223) EXPLAINS rather than convicts -- its third
distinct outcome after CONVICTS (INR3503) and EXONERATES (JOU4306).
⚠ The tell that separates the two readings is "promotion and marketing": a
school band director never needs it; a studio teacher does.

*** FOURTH: MUE3423 -- a misfiling, and the CONTRIBUTOR drifted from its own text ***

Statewide ?423 = "orchestra materials in a laboratory setting... for school
programs". UWF's "Instrumental Programs: Strings and Orchestra" (2 cr) matches.
USF's "String Techniques" (1 cr) is a PLAYING-technique course, and Florida
numbers that separately at MUE2440, carried by SIX institutions (BC, FAMU, FIU,
UCF, UF, UNF) at the same 1 credit.
⚠⚠⚠ AND THE STATEWIDE DESCRIPTION ENDS WITH "USF" -- the University of South
Florida CONTRIBUTED the description its own course no longer matches. A
contributor can drift away from its own contribution, at which point the state
record stops describing the very institution that wrote it. New observation.
⚠ UWF carries BOTH ?423 and MUE4343 "String Methods and Materials" -- the
same-institution control again, showing the two subjects are distinct.

*** AND: string pedagogy is fragmented across FIVE statewide numbers ***
MUE1440/2440 (techniques), MUE3343/4343 (methods+materials), MUE3423 (this),
MUE3443 (intro to teaching strings), MUE4441 (FAU: string pedagogy+methods).
Five numbers for what is really two courses.

*** EVERY STATEWIDE DESCRIPTION IN THIS BATCH ENDS WITH A CONTRIBUTOR CODE ***
?423 "USF", ?411 "FSU", ?344 "FSU". The batch-208 embedded-institution-list rule
in its SHORTEST form -- a bare institution code rather than a list and a date.
⚠ It identifies the CONTRIBUTOR for free, which is the batch-200 reverse read,
and it is cheap to check: look at the last token of DS_Course.

*** DISTRIBUTION TEST: all three fields are near-universal, correctly dropped ***
hs_credit 403/1, transferable 403/1, dual_enrollment 399/5. survey.py labels all
three "discriminating" on >1 value; the batch-221 threshold rule correctly
rejects them. Nothing about them went in the guides.

Prefix: 273 live ids, 211 single-carrier (77%), max 10 carriers.
Sources: UWF PDF (3 of 4 courses), FSU bulletin, UF CourseLeaf, FAU Coursedog
(reopened batch 228 -- and it supplied the decisive MUE4475 evidence).
⚠ FGCU's CourseLeaf PDF returned an EMPTY 202 on two attempts, so MUE4344's own
description could not be read; the guide says so.
⚠ USF still has no course-description route.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
FSU = 'Florida State University'
FAU = 'Florida Atlantic University'
FGCU = 'Florida Gulf Coast University'
USF = 'University of South Florida'

# Shared block -- Florida's single K-12 music certificate, which is the reason
# every one of these courses is required of students who will never use it.
CERT = ('*** FLORIDA CERTIFIES MUSIC K-12 AS ONE CERTIFICATE - general, choral and instrumental - so '
        'you can be assigned to any of the three. FTCE Music K-12 covers the whole span. ')

NEW = {

  'MUE3423': {
    'title': 'Instrumental Programs: Strings and Orchestra',
    'credits': 2, 'contact_hours': 30, 'version': '1.0',
    'prerequisites': (
      'UWF: MUT 2117 (music theory). USF: not published. '
      '*** THE TWO CARRIERS TEACH DIFFERENT COURSES ON THIS NUMBER. UWF teaches ORCHESTRA PROGRAMME '
      'methods - "methods, curriculum, music, and rehearsal techniques particular to teaching '
      'orchestra in the public schools" - which is what the statewide description says. USF teaches '
      'STRING PLAYING TECHNIQUE, which Florida numbers separately at MUE2440 and which six other '
      'institutions carry there at the same 1 credit. '
      '*** SO CHECK WHICH ONE YOU ARE REGISTERING FOR: playing the instruments, or running the '
      'programme. A student who did one has NOT done the other and the transcript will not say which. '
      '*** CREDITS DIVERGE: UWF 2, USF 1. '
      '*** STRING PEDAGOGY IS SPREAD ACROSS FIVE STATEWIDE NUMBERS (MUE1440/2440, 3343/4343, 3423, '
      '3443, 4441). Register by the DESCRIPTION your institution publishes, not the number or title.'),
    'offering_notes': {
      'summary': ('Two public carriers teaching two different courses at two credit values. No '
                  'institution publishes contact hours anywhere in the MUE prefix.'),
      'hours_source': 'derived',
      'derived_contact_hours': 30,
      'derivation': ("Florida's 1:15 convention applied to UWF's 2-credit form, which is the version "
                     'matching the statewide description. At USF the same identifier is 1 credit, so '
                     '15 hours is the right figure there.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Instrumental Programs: Strings and Orchestra', 'credits': 2, 'contact_hours': None,
         'note': ('Department of Music. "Studies methods, curriculum, music, and rehearsal techniques '
                  'particular to teaching orchestra in the public schools." Prerequisite MUT 2117. '
                  'May not be repeated. MATCHES the statewide description. UWF also carries MUE4343 '
                  '"String Methods and Materials", so it treats programme methods and string teaching '
                  'as distinct courses - the same-institution control.')},
        {'institution': 'USF', 'institution_name': USF,
         'title': 'String Techniques', 'credits': 1, 'contact_hours': None,
         'note': ('Title names PLAYING technique, which the statewide description for this number does '
                  'not cover and which Florida numbers at MUE2440 (six carriers at 1 credit). USF also '
                  'carries MUE3422 "Wind Techniques" at 1 credit, so the pairing looks deliberate. '
                  'NOTE the statewide description ends with the code "USF" - USF contributed the '
                  'description its own course no longer matches. USF exposes no course-description '
                  'route, so its own text could not be read.')},
      ],
    },
  },

  'MUE4344': {
    'title': 'Teaching Instrumental Music',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'Not published by FGCU or statewide; in practice the instrument techniques courses come first. '
      '*** THE STATEWIDE TITLE NAMES A DIFFERENT SPECIALISM: the state defines this number as methods for '
      'GENERAL MUSIC (the classroom music teacher); FGCU teaches band and orchestra. Those are the two '
      'most separated jobs in the field. '
      '*** THE EVIDENCE: statewide title and description agree; FSU carries MUE3344 "Teaching General '
      'Music K-12" with the statewide wording verbatim; and UF carries the IDENTICAL TITLE at 3 '
      'credits on MUE4422. '
      '*** WHY: the state provides NO undergraduate instrumental METHODS number at K-12 level - that '
      'slot is graduate only - so carriers improvise differently. '
      '*** SEND THE SYLLABUS ON TRANSFER: an evaluator matching the number reads general music. ' + CERT),
    'offering_notes': {
      'summary': ('One public carrier. The statewide subject of this number is GENERAL MUSIC methods; '
                  'FGCU teaches instrumental methods on it. No contact hours published.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Florida's 1:15 convention on 3 credits. No institution publishes a contact-hour "
                     'figure anywhere in the MUE prefix.'),
      'offerings': [
        {'institution': 'FGCU', 'institution_name': FGCU,
         'title': 'Teaching Instrumental Music', 'credits': 3, 'contact_hours': None,
         'note': ("FGCU's CourseLeaf PDF returned an empty response on two attempts, so its own "
                  'description could not be read; title and credits are from the statewide record and '
                  'the syllabus is the authority. FGCU also carries MUE3487 "Instrumental Pedagogy" '
                  '(3 cr), MUE3343 "String Methods and Materials" (1 cr) and MUE3475 "Percussion '
                  'Methods & Materials" (2 cr), so this sits inside a built-out instrumental sequence '
                  'rather than standing alone.')},
      ],
    },
  },

  'MUE4411': {
    'title': 'Choral Techniques',
    'credits': 4, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'FSU: MUE 3491-3492 (choral conducting and literature) or instructor permission, AND concurrent '
      'registration in MUE 3495r. UWF: MUT 2117, with COREQUISITE MUG 3104 (conducting). '
      '*** CREDITS DIFFER BY A FACTOR OF TWO - FSU 4, UWF 2 - AND THE PREREQUISITES EXPLAIN IT. FSU gates '
      'on a two-course conducting and choral literature sequence, so you arrive able to conduct; UWF '
      'runs it ALONGSIDE your first conducting course. Different points in the sequence, not unequal '
      'versions. '
      '*** THE TRANSFER HARM RUNS ONE WAY: at FSU with the 2-credit version you are two credits short '
      'AND lack the foundation its course assumes. '
      '*** UWF requires SCHOOL OBSERVATIONS, on a district calendar during the school day. ' + CERT),
    'offering_notes': {
      'summary': ('Two public carriers at 4 and 2 credits - the largest credit divergence recorded '
                  'outside flight training, and the prerequisite chains explain it. No contact hours '
                  'published.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("Florida's 1:15 convention applied to FSU's 4-credit form, which is the version "
                     'the statewide description describes - the statewide text is FSU\'s own, verbatim. '
                     'At UWF the identifier is 2 credits, so 30 hours is the right figure there.'),
      'offerings': [
        {'institution': 'FSU', 'institution_name': FSU,
         'title': 'Choral Techniques', 'credits': 4, 'contact_hours': None,
         'note': ('"Provides students with an understanding of chorus and choral problems: '
                  'organization, rehearsal, repertory, diction, intonation, tone quality, balance, '
                  'blend, and style." Prerequisite MUE 3491-3492 or instructor permission; concurrent '
                  'registration in MUE 3495r required. NOTE this description IS the statewide '
                  'description word for word, and the statewide entry names FSU as contributor - so '
                  'the state record and FSU are ONE source, not two agreeing. FSU also carries '
                  'MUE2410 "Choral Techniques for Non-Voice Principals" (2 cr), a deliberately '
                  'separate course and not a substitute.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Special Methods/Choral Techniques', 'credits': 2, 'contact_hours': None,
         'note': ('Department of Music. "Problems related to choral conducting with practical '
                  'application of applicable choral techniques at all levels, elementary through high '
                  'school. Includes choral and full score study, repertoire for various levels and '
                  'observations in the public schools of choral music classes." Prerequisite MUT 2117; '
                  'COREQUISITE MUG 3104. Carries a school observation component.')},
      ],
    },
  },

  'MUE4475': {
    'title': 'Percussion Methods and Materials',
    'credits': 2, 'contact_hours': 30, 'version': '1.0',
    'prerequisites': (
      'UWF: completion of sophomore year programme requirements. FAU: music major in percussion '
      'performance. '
      '*** THE TWO CARRIERS AIM AT DIFFERENT CAREERS. UWF is for students "planning to practice teach in '
      'band programs", with school observations, and matches the statewide description. FAU prepares '
      '"music majors in PERCUSSION PERFORMANCE" to become percussion educators, covering solo/ensemble '
      'literature and PROMOTION AND MARKETING - building a private studio. '
      '*** THE TELL IS "promotion and marketing": a school band director never needs it. '
      '*** NEITHER IS MISFILED - FAU also carries MUE2470, whose description IS the school-teaching '
      'one, so it uses this number deliberately. '
      '*** CREDITS DIVERGE: UWF 2, FAU 3. Ask which version your section is before add/drop. ' + CERT),
    'offering_notes': {
      'summary': ('Two public carriers at 2 and 3 credits, aimed at different careers - school band '
                  'teaching and private studio teaching. No contact hours published.'),
      'hours_source': 'derived',
      'derived_contact_hours': 30,
      'derivation': ("Florida's 1:15 convention applied to UWF's 2-credit form, which is the version "
                     'matching the statewide description. At FAU the identifier is 3 credits, so 45 '
                     'hours is the right figure there.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Percussion Methods and Materials', 'credits': 2, 'contact_hours': None,
         'note': ('Department of Music. "Percussion instruments, playing techniques, history, '
                  'methodology, pedagogy and literature for solo and ensemble experiences. '
                  'Observations of representative public school programs required of students planning '
                  'to practice teach in band programs." Completion of sophomore year programme '
                  'requirements required. One of a MATCHED SET with MUE4451 (woodwind) and MUE4465 '
                  '(brass), all 2 credits on a common template - a band-teaching student takes all '
                  'three. MATCHES the statewide description.')},
        {'institution': 'FAU', 'institution_name': FAU,
         'title': 'Advanced Percussion Literature and Pedagogy', 'credits': 3, 'contact_hours': None,
         'note': ('Dorothy F. Schmidt College of Arts and Letters. "Prepares music majors in percussion '
                  'performance with the knowledge and skills to become effective percussion educators. '
                  'This class involves a survey of method books, periodicals, historical texts, and '
                  'solo/ensemble literature for percussion, as well as observations and analyses of '
                  'successful teaching techniques, promotion, and marketing." FAU ALSO carries '
                  'MUE2470 "Percussion Pedagogy and Methods" (1 cr) for elementary and secondary '
                  'school teaching, so the two are deliberately different courses there.')},
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
