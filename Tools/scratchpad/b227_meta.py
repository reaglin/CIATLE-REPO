"""Batch 227 metadata -- GRA (graphic design), the four queued rows plus GRA3887C.

All five are C identifiers, so contact hours are 60 throughout (Ron, 2026-09-15:
C = 60, no suffix = 45). All five carry 3 credits at every public carrier, and
NO carrier publishes a contact-hour figure anywhere in the prefix.

GRA3887C was ADDED to the batch. It was not queued, but it is the evidentiary
control for the batch's headline (below) and it completes UWF's comics cluster.

*** THE BATCH'S HEADLINE: A TITLE DIVERGENCE THAT DISSOLVES, BESIDE ONE THAT
    DOES NOT -- AND THE TEST THAT SEPARATES THEM ***

The survey looked like a clean misfiling finding: UWF appeared to be running a
comics PAIR on two statewide numbers that mean something else (GRA3881C
"Semantics of Design", GRA4882C "Analysis of Trends and Styles"). That is the
batch-225 PET4434/PET4820 shape, and it was the working hypothesis.

Reading the DESCRIPTIONS against each other broke it in both directions:

  GRA3881C -- NOT a divergence. Statewide says semiotics ("the general field of
  semiotics ... aspects linked to MEANING in visual communication"). FIU says
  "signs, codes, and cultural MEANING in design ... semiotic principles". UWF
  says "how SIGNS, SYMBOLS, and sequence are used to create MEANING in
  sequential art". All three name the same subject. UWF teaches semiotics
  THROUGH comics -- the medium is the vehicle, not the subject. The titles look
  like two unrelated courses; the descriptions agree completely.

  GRA4882C -- a REAL divergence. Statewide title and description agree with each
  other (an analysis/appraisal course); UWF teaches advanced comics PRODUCTION.
  Branch 1 of the title/description test, so the carrier is the deviating party.

*** AND THE EXPLANATION FOR GRA4882C IS NOT CARELESSNESS ***

GRA3887C is the control, and it is decisive. Florida provides exactly ONE
comics/cartoon number -- GRA?887, whose statewide description explicitly names
"COMIC STRIPS, COMIC BOOKS, GRAPHIC NOVELS". UWF CARRIES IT, matches the
statewide title WORD FOR WORD, and adds only a sentence about stop motion. So
UWF demonstrably knows the state's scheme and files to it when a number exists.

The state numbers comics ONCE. UWF teaches it as a THREE-COURSE SEQUENCE. The
third course has nowhere correct to go. That is MISFILING BY NECESSITY
(batch 225) with a NEW CAUSE: not a subject the state failed to number, but a
SEQUENCE LENGTH the state's single number cannot accommodate. Sequence-length
divergence (batch 204) and misfiling colliding.

I nearly published the opposite of this. The survey's titles pointed one way and
the descriptions pointed another, and only reading one institution's entries
against each other (batch 225) surfaced the control that settled it.

*** SECOND: a SINGLE-CARRIER course where statewide agreement is NOT evidence ***

GRA3887C's statewide description and UWF's are the SAME TEXT. With one carrier,
that is not two sources agreeing -- it is one source quoted twice, almost
certainly contributed by UWF. The guide says so. This generalises: on a
single-carrier course, carrier/statewide agreement corroborates NOTHING. It does
carry a mild positive signal (the text is current and written by people who
teach the course), but the hedging must not be relaxed on the strength of it.

*** THIRD: a statewide prerequisite that dangles at EVERY carrier ***

GRA3881C and GRA4882C both list GRA 3194C statewide. NEITHER UWF NOR FIU carries
GRA3194C or the bare GRA3194 -- those are UF and Pensacola State, neither of
which teaches either course. Same shape as JOU3342 (batch 224): the gate cannot
be satisfied by any carrier, and the contributing institutions do not teach the
course.

*** FOURTH: a prerequisite CHAIN that cannot be completed outside one school ***

GRA4882C requires ART 3312C AND GRA 3151C AND GRA 3881C. ART3312C and GRA3151C
have NO other Florida public carrier. So the chain is unreproducible anywhere
else in the state -- a transfer student cannot arrive gate-ready, and it can cost
a term. This is a sharper consequence than the usual single-carrier hedge and it
goes in the prerequisite field.

*** FIFTH: a new prerequisite-defect shape -- PROSE INSTEAD OF AN IDENTIFIER ***

GRA2508C's statewide prerequisite reads "BASIC DESIGN OR CONSENT OF INSTRUCTOR".
That is a SUBJECT DESCRIPTION, not a course identifier, and the batch-209 syntax
test does not flag it because there is no course-looking token to test. Sixth
shape in the defective-prerequisite taxonomy. The real gate at UWF is
DIG 2000C OR DIG 3001C.

*** SIXTH: the distribution test, stratified to the population the FIELD applies to ***

hs_credit across the prefix looked marginal: 46 FA / 462 EL over public
undergraduate rows (9%), which by the batch-225 threshold reads "near-universal
with exceptions". But high-school credit only applies to DUAL ENROLMENT, which
is a LOWER-DIVISION phenomenon -- and restricted to levels 1-2 the split is
43/267 (14%), with 17 of the 20 FINE ARTS numbers lower-division.

The refinement: stratify by the population the FIELD APPLIES TO, not by course
level generically. And the FINDING did not come from the distribution at all --
it came from comparing SIBLINGS AT ONE INSTITUTION: UWF carries GRA2111C (FINE
ARTS) and GRA2508C (ELECTIVE), two adjacent required foundation courses in one
programme returning different high-school credit. The distribution test only
established that the field was worth looking at.

*** ALSO: the private-carrier title in the inventory, THIRD instance ***

GRA4882C's queue row title is "Analysis of Trends and Styles" -- the statewide
title, which in Florida only a PRIVATE institution actually uses. After COM2713
(batch 222) and CNT3112 (batch 226). Also GRA2508's bare form is private-only,
the PET3344 shape inverted (there the bare was private and the C public -- same
here).

*** AND: a stale statewide record proved rather than inferred ***

GRA2508C's statewide description ends "INSTITUTIONS: FAMU 1988" and FAMU does
NOT carry the number today -- UWF does. The batch-208 embedded-institution-list
rule with direct proof rather than inference. Its title also carries "(RES
2008)", an administrative marker appearing on exactly three GRA numbers, all
stamped the same year. Not explained; not guessed at in the guide.

Prefix: 387 live ids, 269 single-carrier (70%), max 11 carriers.
UWF PDF route worked (uwf_gra.pdf, 50 KB). FIU from the Coursedog cache.
UNF unreadable (bepress 403, as recorded); FAMU unreadable (acalog).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
UNF = 'University of North Florida'
FIU = 'Florida International University'
FAMU = 'Florida A&M University'

# Shared block -- the dangling statewide gate, which is identical on the two
# courses that carry it. Kept short: it is spent twice.
DANGLE = ('*** THE STATEWIDE GATE DANGLES: it names GRA 3194C, which NEITHER carrier offers - UF and '
          'Pensacola State carry those numbers and teach neither course. Ignore it. ')

# Shared block -- the repeat allowance, which UWF attaches to four of the five.
REPEAT = ('*** REPEATABLE to 9 sh at UWF: content varies by term, so the transcript says little about '
          'what you covered. Keep the work, and check how many repeats your degree counts.')

NEW = {

  'GRA2508C': {
    'title': 'Color Theory',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'UWF: DIG 2000C OR DIG 3001C. '
      '*** THE STATEWIDE PREREQUISITE IS NOT A COURSE. It reads "BASIC DESIGN OR CONSENT OF '
      'INSTRUCTOR" - a subject description, not an identifier. There is no course called Basic Design '
      'to find; take a foundational design or digital-media course first and read your OWN '
      'catalogue for the gate. '
      '*** SOLE PUBLIC CARRIER is UWF. The bare GRA2508 is carried in Florida only by a private '
      'institution, so among public institutions the C form is the only form of this course. '
      '*** DUAL-ENROLLED STUDENTS, CHECK BEFORE YOU REGISTER: this earns ELECTIVE high-school credit, '
      'but 14% of lower-division GRA numbers earn FINE ARTS instead - including GRA2111C, which UWF '
      'carries alongside it in the same programme. Two adjacent foundation courses, different '
      'high-school credit. Confirm with your counsellor. '
      '*** The statewide description ends "INSTITUTIONS: FAMU 1988" and is demonstrably stale - FAMU '
      'does not carry this number today and UWF does.'),
    'offering_notes': {
      'summary': ('One public carrier (UWF) at 3 credits. No institution publishes contact hours. The '
                  'bare GRA2508 is private-only, so the C form is the only public form.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("Florida's convention for a 3-credit integrated C course (Ron, 2026-09-15). No "
                     'Florida institution publishes a contact-hour count anywhere in the GRA prefix.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Color Theory', 'credits': 3, 'contact_hours': None,
         'note': ('Sole public carrier. College of Arts, Social Sciences and Humanities, Department of '
                  'Art and Design. Prerequisite DIG 2000C OR DIG 3001C. May NOT be repeated for credit '
                  '- the exception in this batch. Material and supply fees are assessed across this '
                  'programme. Required in the Graphic Design BFA and named as a prerequisite on the '
                  'Senior Design Studio (GRA4874C). Earns ELECTIVE high-school credit on dual '
                  'enrolment, where its sibling GRA2111C earns FINE ARTS.')},
      ],
    },
  },

  'GRA3139C': {
    'title': 'Time-Based Design',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'NONE - UWF and the statewide record both list none. '
      '*** BUT THE DESCRIPTION ASSUMES PRIOR WORK THE GATE DOES NOT REQUIRE. UWF opens "A further '
      'articulation of the techniques and components of time-based media design" - second-course '
      'language on an open gate. Arrive with Adobe competence and a grounding in composition '
      'and typography, or you meet the software and the temporal thinking at once. '
      '*** ONE SUBJECT, TWO NUMBERS: UNF and UWF carry GRA3139C, FAMU the bare GRA3139. No '
      'institution carries both - the signature of one course filed two ways, so an evaluator matching '
      'on the identifier sees a mismatch where there is none. Say so and send the syllabus. '
      '*** UWF titles it "Motion Graphics", which is NARROWER than its own description: the course '
      'is full time-based design. The statewide name fits better than UWF\'s does. ' + REPEAT),
    'offering_notes': {
      'summary': ('Two public carriers of this identifier (UNF, UWF) and a third institution (FAMU) '
                  'carrying the same subject under the unsuffixed GRA3139. All three at 3 credits; no '
                  'institution publishes contact hours.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("Florida's convention for a 3-credit integrated C course (Ron, 2026-09-15). No "
                     'carrier publishes a figure. Expect the real commitment to exceed it - rendering '
                     'is slow and every revision has to be re-watched in real time.'),
      'offerings': [
        {'institution': 'UNF', 'institution_name': UNF,
         'title': 'Time-Based Media', 'credits': 3, 'contact_hours': None,
         'note': ("Matches the statewide subject name. UNF's live catalogue is client-rendered and its "
                  'archived catalogue PDFs are blocked at the host, so UNF\'s own description and '
                  'prerequisite could not be read; title and credits are from the statewide record.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Motion Graphics', 'credits': 3, 'contact_hours': None,
         'note': ('Department of Art and Design. NO prerequisite. May be repeated for up to 9 sh. '
                  'NOTE the title is narrower than the description, which covers narrative ordering, '
                  'moving-image editing and sound-image relations as well as motion graphics.')},
        {'institution': 'FAMU', 'institution_name': FAMU,
         'title': 'Time Based Design', 'credits': 3, 'contact_hours': None,
         'note': ('Carries the UNSUFFIXED number GRA3139, not this identifier - listed here because it '
                  'is the same course and the number difference is the transfer trap. FAMU runs on '
                  'acalog, which serves its front pages but returns empty responses for course '
                  'content, so its description could not be read.')},
      ],
    },
  },

  'GRA3881C': {
    'title': 'Semantics of Design: Semiotics and Sequential Art',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'FIU: GRA 2111C. UWF: NONE. ' + DANGLE +
      '*** READ THE DESCRIPTIONS, NOT THE TITLES. FIU calls this "Design: Semiotics" and UWF calls it '
      '"Comics: Sequential Art and Design" - and both descriptions, and the statewide one, name SIGNS '
      'and the making of MEANING as the content. It is the SAME SUBJECT; what differs is the material '
      'it is taught through. FIU teaches semiotics across design contexts, UWF teaches it through '
      'making comics. '
      '*** THE TRANSFER RISK IS THE TITLE, NOT THE CONTENT: an evaluator comparing those two titles '
      'will reasonably conclude they are different courses, and be wrong. Send the syllabus and '
      'point at the descriptions - a one-line note from you can prevent a transfer loss here. '
      '*** If you cannot draw, ask which version you are in BEFORE registering: UWF\'s requires you to '
      'make comics. It is also the required gate for GRA4882C.'),
    'offering_notes': {
      'summary': ('Two public carriers (FIU, UWF), both at 3 credits, whose titles look like different '
                  'subjects and whose descriptions agree completely. No institution publishes contact '
                  'hours. The unsuffixed GRA3881 is carried by nobody, public or private.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("Florida's convention for a 3-credit integrated C course (Ron, 2026-09-15). "
                     'Neither carrier publishes a figure. Note the course is simultaneously a reading '
                     'course and a studio course, which surprises students arriving expecting either.'),
      'offerings': [
        {'institution': 'FIU', 'institution_name': FIU,
         'title': 'Design: Semiotics', 'credits': 3, 'contact_hours': None,
         'note': ('College of Communication, Architecture + The Arts. Prerequisite GRA 2111C. Teaches '
                  '"signs, codes, and cultural meaning in design" across design contexts generally.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Comics: Sequential Art and Design', 'credits': 3, 'contact_hours': None,
         'note': ('Department of Art and Design. NO prerequisite. May be repeated for up to 9 sh. '
                  'Teaches "how signs, symbols, and sequence are used to create meaning in sequential '
                  'art" - the same semiotic subject, delivered through making comics and reading '
                  'historical examples. Required prerequisite for GRA4882C.')},
      ],
    },
  },

  'GRA3887C': {
    'title': 'Traditional Methods in Cartoon Design',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'UWF: DIG 2000C OR DIG 3001C; statewide lists NONE. Note DIG 3001C is a UWF-only '
      'course, so students arriving from elsewhere clear the gate through DIG 2000C (five other public '
      'carriers). '
      '*** THIS IS NOT A DRAWING COURSE. "Traditional methods" means the physical, pre-digital '
      'animation techniques - object-motion, cutout, silhouette, claymation and pixilation - alongside '
      'the history of the cartoon. '
      '*** BUDGET THE TIME HONESTLY: 12 to 24 exposures buy ONE SECOND, each a separate physical '
      'adjustment. A finished minute is a project, not an assignment, and unfinished work is the '
      'commonest outcome - scope small and shoot a test first. '
      '*** SHOOT FULLY MANUAL. Automatic exposure and white balance change between frames and make the '
      'result flicker. You also need a space where the setup can stay untouched for days. ' + REPEAT),
    'offering_notes': {
      'summary': ('One public carrier (UWF) at 3 credits, whose title matches the statewide title '
                  'exactly. No contact hours published. The unsuffixed GRA3887 is carried by nobody.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("Florida's convention for a 3-credit integrated C course (Ron, 2026-09-15). "
                     'Treat it as a soft floor: stop motion is among the most time-expensive '
                     'techniques in the visual arts.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Traditional Methods in Cartoon Design', 'credits': 3, 'contact_hours': None,
         'note': ('Sole public carrier. Department of Art and Design. Prerequisite DIG 2000C OR '
                  'DIG 3001C. May be repeated for up to 9 sh. Its description is the statewide '
                  'description VERBATIM plus one sentence on stop-motion practice - so the statewide '
                  'record almost certainly came FROM UWF and does not independently corroborate it. '
                  'This course is the evidence that UWF files cartoon courses on the state number '
                  'when one exists, which is why GRA4882C sits where it does.')},
      ],
    },
  },

  'GRA4882C': {
    'title': 'Advanced Sequential Art and Design',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'UWF: ART 3312C, GRA 3151C AND GRA 3881C. '
      '*** TWO OF THE THREE GATES ARE UWF-ONLY. ART3312C and GRA3151C have no other Florida public '
      'carrier, SO THIS CHAIN CANNOT BE COMPLETED ANYWHERE ELSE IN THE STATE - a transfer student '
      'must generally clear them at UWF first, which can add a term. Ask an adviser about '
      'substitutions BEFORE you enrol. ' + DANGLE +
      '*** THE NUMBER DOES NOT NAME THE COURSE. Statewide this is "Analysis of Trends and Styles", an '
      'analysis and appraisal course; UWF teaches advanced COMICS PRODUCTION. Some inventories show '
      'the statewide title, which in Florida only a private school uses. Register by number, and on '
      'transfer send the syllabus and finished pages. ' + REPEAT),
    'offering_notes': {
      'summary': ('One public carrier (UWF) at 3 credits, teaching a different subject from the '
                  'statewide record. No contact hours published. A private institution carries the '
                  'statewide subject under the unsuffixed GRA4882.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("Florida's convention for a 3-credit integrated C course (Ron, 2026-09-15). "
                     'Expect well beyond it - finished comics pages are slow and the page count is '
                     'usually what binds the grade.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Advanced Comics: The Advanced Practice of Sequential Art and Design',
         'credits': 3, 'contact_hours': None,
         'note': ('Sole public carrier. Department of Art and Design. Prerequisites ART 3312C AND '
                  'GRA 3151C AND GRA 3881C - two of which are UWF-only, so the chain is not '
                  'reproducible elsewhere in Florida. May be repeated for up to 9 sh. Teaches visual '
                  'narrative applied to sequential art: character construction and individualisation, '
                  'integration into graphic environments, page layout, panel design and working from '
                  'scripts. This is NOT the statewide subject, and the reason is that Florida numbers '
                  'comics ONCE (GRA3887C, which UWF already uses correctly) while UWF teaches it as a '
                  'three-course sequence - so the third course has no number that fits.')},
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
