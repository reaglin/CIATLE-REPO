"""Batch 233 metadata -- PHY (physics), the three queued rows.

Contact hours:
  PHY3106   3 cr / 45   lecture, 1:15 convention
  PHY4445   3 cr / 45   lecture, 1:15 convention
  PHY4822L  3 cr / 90   ⚠ LABORATORY convention (~30 hrs per credit), NOT 1:15.
                        UWF is 3 cr; FSU is 2 cr (~60). No carrier publishes
                        hours anywhere in PHY.

*** HEADLINE: PHY3106 -- a SEQUENCE-POSITION divergence, and the title says it ***

  statewide  "Modern Physics I" -- relativity, EM waves and photons, matter
             waves, quantum theory, atomic structure, quantum mechanics.
             Prereq PHY 2049/2054 AND MAC 2313 (Calculus III).
  FIU        "Modern Physics" -- "special relativity, wave-particle duality,
             origins of quantum mechanics, and the SCHRODINGER WAVE EQUATION".
             ✅ Matches the statewide subject.
  UWF        ⚠⚠ "CALCULUS-BASED PHYSICS III" -- "laws of THERMODYNAMICS, WAVE
             PHENOMENA, breakdown of classical physics, theory of relativity,
             quantization of charge, light, and energy, atomic structure".
             Prereq PHY 2049 ONLY -- no Calculus III.

⚠⚠⚠ The content diverges at BOTH ends: UWF adds thermodynamics and waves
(classical material closing the intro sequence) and does NOT mention quantum
mechanics; FIU reaches the Schrodinger equation. Only relativity overlaps.
⚠⚠ AND THE PREREQUISITE CONFIRMS THE POSITION, which is the cheap check: a
course positioned as the third intro term cannot demand Calculus III because
students have not taken it. One positioned above the sequence can. Recorded as
a drill -- read the prerequisite before the title on this number.

⚠ Connects to the live PHY3107 guide (batch 204) and its sequence-LENGTH
finding: PHY3101 "Elements of Modern Physics" covers the whole field in ONE term
and has TEN public carriers against 2 for the 3106/3107 pair. So the one-term
treatment is five times commoner than the sequence. Both guides now say so.

*** SECOND: PHY4445 -- a statewide prerequisite naming TWO numbers NOBODY carries ***

Statewide prereq: "PHY 3054 OR PHY 3049". ⚠⚠⚠ Checked both: ZERO public
carriers in Florida for either. Well-formed identifiers, so they pass the
batch-209 syntax test; they simply do not exist as offerings.
⚠ This is STRONGER than the batch-219 TPA4021C dangling case, where the named
number belonged to OTHER schools. Here BOTH alternatives are carried by nobody
at all -- the gate is unusable by anyone.
⚠⚠ The real gate at UWF is MAC 2313 AND MAP 2302 AND PHY 2049 with a C- floor.
DIFFERENTIAL EQUATIONS is the one to flag: nothing in the statewide record hints
at it, and laser rate equations and cavity mode analysis are DE problems. The
batch-189 shape (description/course assumes a discipline the state gate omits).

*** AND a scope divergence with an institutional explanation ***
UWF carries the statewide syllabus in full -- a broad PHOTONICS survey (fibre,
detectors, modulation, displays, optical communications). UCF's is "Principles
of laser gain media, properties of resonators and modes, and description of
specific laser systems" -- NARROWER AND DEEPER, laser physics proper.
⚠⚠ The explanation is institutional and worth stating: UCF hosts CREOL, the
College of Optics and Photonics, so the applications material lives in its own
courses and UCF can afford to teach lasers narrowly. An institution without an
optics college puts it all in one survey.
⚠ Handled as a genuine CHOICE for the student (breadth vs depth), not as a
defect -- and the guide says which suits which destination.

*** THIRD: PHY4822L -- the credit divergence is PACKAGING, not depth ***

  UWF  3 cr, NOT repeatable, prereq PHY 3107 AND PHY 3802L
  FSU  2 cr, ⚠⚠ REPEATABLE TO 6 CREDIT HOURS "for special projects arranged in
       advance", prereq PHY 3802L only. Catalogued as PHY 4822Lr -- the r marks
       repeatability in FSU's notation.

⚠⚠⚠ So 2-vs-3 is NOT one course being shallower. FSU runs a smaller REPEATABLE
unit a committed student takes three times; UWF runs one larger block. Different
designs for different students, and the repeatable one is the better route into
a graduate application. Recorded as a caution: before writing a credit
divergence as a depth difference, CHECK FOR A REPEAT ALLOWANCE.

⚠⚠⚠ AND THE BEST SENTENCE IN THE BATCH, from FSU: "Students are expected to
WORK WITHOUT DETAILED INSTRUCTIONS." That is the real discontinuity in a physics
degree -- every prior lab supplies a procedure; this one supplies apparatus and
a question. The guide leads on it, because it is what the course is FOR and it
is what graduate committees and employers actually read this course for.
⚠ Also: an L suffix at 2-3 credits standing alone -- the batch-203 counterexample
to "L means a 1-credit companion", stated in the guide.
⚠ FSU applies a programme rule: no physics or maths course below C- counts
toward the major.
⚠ PHY4823L (Modern Physics Laboratory II) exists at USF alone -- so do not
assume a second lab is available.

*** DISTRIBUTION TEST: discriminating, but not for THESE courses ***
transferable (= hs-credit code) 689 EL / 211 SC across the prefix -- 23%, which
looks like a real split. ⚠ Stratified: LOWER 41% SCIENCE (170/418), UPPER 6%
(15/238). All three targets are UPPER and all read EL.
⚠⚠ So the batch-227 rule applies exactly: stratify by the population the field
applies to (dual enrolment is lower-division). Nothing claimed for these three --
but each guide carries ONE line pointing out that lower-division Florida physics
earns SCIENCE high-school credit 41% of the time, which is genuinely useful to a
dual-enrolled student choosing a physics course.

Prefix: 331 live ids, 207 single-carrier (63%), max 30 carriers.
Sources: UWF PDF (all three), FIU Coursedog, FSU bulletin, UCF Kuali -- ⚠ FOUR
institution sources in one batch, the best coverage in some time.
⚠ FGCU re-probed at session start (bsc): still empty 202. REVIEW_QUEUE 104 open.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
FIU = 'Florida International University'
FSU = 'Florida State University'
UCF = 'University of Central Florida'

# Shared block -- the dual-enrolment pointer. True of all three, and useful to a
# student choosing lower-division physics instead. Kept short: spent 3 times.
DE = ('*** Choosing LOWER-division physics instead? 41% of Florida lower-level PHY offerings earn '
      'high-school SCIENCE credit on dual enrolment, against 6% up here. ')

NEW = {

  'PHY3106': {
    'title': 'Modern Physics I',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'Statewide: PHY 2049 or PHY 2054 AND MAC 2313 (Calculus III). UWF: PHY 2049 ONLY. '
      '*** THE PREREQUISITE IDENTIFIES WHICH VERSION YOU ARE IN, and it is the fastest check. FIU teaches '
      'the statewide subject - relativity through the Schrodinger equation. UWF teaches '
      '"Calculus-Based Physics III", the THIRD TERM of the intro sequence: it adds THERMODYNAMICS and '
      'WAVE PHENOMENA and does not mention quantum mechanics. A course inside the intro sequence '
      'cannot demand Calculus III; one above it can. '
      '*** CHECK BOTH ENDS: did your course do the Schrodinger equation, and did it do thermodynamics? On '
      'transfer send a TOPIC LIST, not the title. '
      '*** AND CHECK A SECOND COURSE EXISTS: only two public institutions carry PHY3107, while TEN '
      'carry PHY3101, which covers the whole field in one term. ' + DE),
    'offering_notes': {
      'summary': ('Two public carriers at 3 credits teaching the course at different curricular '
                  'positions with different content. No institution publishes contact hours anywhere '
                  'in the PHY prefix.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Florida's 1:15 convention on 3 credits; both carriers list 3. Expect well above "
                     'it - modern physics problem sets are slow.'),
      'offerings': [
        {'institution': 'FIU', 'institution_name': FIU,
         'title': 'Modern Physics', 'credits': 3, 'contact_hours': None,
         'note': ('"Development of modern physics. Topics include: special relativity, wave-particle '
                  'duality, origins of quantum mechanics, and the Schrodinger wave equation." MATCHES '
                  'the statewide subject. Paired with PHY3107 Advanced Modern Physics.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Calculus-Based Physics III', 'credits': 3, 'contact_hours': None,
         'note': ('College of Science and Engineering, Department of Physics. "Laws of thermodynamics, '
                  'wave phenomena, breakdown of classical physics, theory of relativity, quantization '
                  'of charge, light, and energy, atomic structure." Prerequisite PHY 2049 only - no '
                  'Calculus III. POSITIONED AS THE THIRD TERM OF THE INTRODUCTORY SEQUENCE, and '
                  'includes classical material the statewide description does not.')},
      ],
    },
  },

  'PHY4445': {
    'title': 'Lasers and Applications',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF: MAC 2313, MAP 2302 AND PHY 2049, C- OR BETTER IN ALL. '
      '*** THE STATEWIDE PREREQUISITE IS UNUSABLE: "PHY 3054 OR PHY 3049" - NEITHER has a single public '
      'carrier anywhere in Florida. Well-formed identifiers naming nothing you can enrol in. '
      '*** DIFFERENTIAL EQUATIONS IS THE REAL GATE and nothing in the state record hints at it - laser '
      'rate equations and cavity analysis are DE problems. '
      '*** THE CARRIERS TEACH IT AT DIFFERENT WIDTHS. UWF carries the statewide syllabus in full - a broad '
      'PHOTONICS survey (fibre, detectors, modulation, displays, optical communications). UCF teaches '
      'laser physics proper - gain media, resonators, modes - because it hosts the College of Optics '
      'and Photonics. For optics graduate study the narrower version is stronger preparation. '
      '*** LASER SAFETY TRAINING IS A REAL PREREQUISITE for any bench work. ' + DE),
    'offering_notes': {
      'summary': ('Two public carriers at 3 credits, one teaching a broad photonics survey and one '
                  'teaching laser physics narrowly and deeply. No contact hours published.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': "Florida's 1:15 convention on 3 credits; both carriers list 3.",
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Lasers and Applications', 'credits': 3, 'contact_hours': None,
         'note': ('College of Science and Engineering, Department of Physics. Carries the statewide '
                  'syllabus in full - nature of light, photons, semiconductor physics, modulation, '
                  'displays, laser principles and design, photodetectors, fibre optics, optical '
                  'communications. Prerequisites MAC 2313 AND MAP 2302 AND PHY 2049, C- or better in '
                  'all. May not be repeated.')},
        {'institution': 'UCF', 'institution_name': UCF,
         'title': 'Lasers', 'credits': 3, 'contact_hours': None,
         'note': ('"Principles of laser gain media, properties of resonators and modes, and description '
                  'of specific laser systems." NARROWER AND DEEPER than the statewide description - '
                  'laser physics proper rather than a photonics survey. UCF hosts the College of Optics '
                  'and Photonics (CREOL), which is why the applications material can live elsewhere.')},
      ],
    },
  },

  'PHY4822L': {
    'title': 'Advanced Physics Laboratory',
    'credits': 3, 'contact_hours': 90, 'version': '1.0',
    'prerequisites': (
      'UWF: PHY 3107 AND PHY 3802L. FSU: PHY 3802L. Statewide names "MODERN PHYSICS" in prose rather '
      'than by number. '
      '*** THIS IS THE COURSE WHERE YOU STOP FOLLOWING INSTRUCTIONS. FSU states it outright: "students '
      'are expected to WORK WITHOUT DETAILED INSTRUCTIONS." Every earlier lab supplies a procedure; '
      'this one supplies apparatus, a question and a deadline. It is the hardest adjustment in the '
      'major and it is why graduate committees and employers read this course. '
      '*** THE CREDIT DIFFERENCE IS PACKAGING, NOT DEPTH: UWF is 3 credits and NOT repeatable; FSU is '
      '2 credits and REPEATABLE TO 6 for special projects arranged in advance. If you are heading to '
      'graduate school, a repeatable advanced lab is the route to a project worth a recommendation. '
      '*** AN L SUFFIX THAT IS NOT A 1-CREDIT ADD-ON - this is a full standalone course and among the '
      'most time-consuming in the degree. Do not pair it with another lab. '
      '*** KEEP YOUR REPORTS: they are the strongest transfer and job evidence you will have.'),
    'offering_notes': {
      'summary': ('Two public carriers, 3 credits at UWF and 2 at FSU where it is repeatable to 6. Both '
                  'call it an advanced lab, broader than the statewide "Modern Physics Laboratory I". '
                  'No contact hours published.'),
      'hours_source': 'derived',
      'derived_contact_hours': 90,
      'derivation': ('Roughly 30 contact hours per credit - the LABORATORY convention, not the 1:15 '
                     'classroom convention, which misdescribes a standalone lab badly. 3 credits at '
                     'UWF gives 90; FSU\'s 2-credit form is about 60. Treat it as a soft floor: '
                     'apparatus misbehaves, runs repeat, and analysis and writing happen afterwards.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Advanced Physics Lab', 'credits': 3, 'contact_hours': None,
         'note': ('College of Science and Engineering, Department of Physics. "Advanced laboratory '
                  'topics are treated. Modern physics laboratory equipment is used to introduce '
                  'students to current laboratory practices." Prerequisites PHY 3107 AND PHY 3802L - '
                  'so you arrive having done the theory these experiments demonstrate. NOT '
                  'repeatable.')},
        {'institution': 'FSU', 'institution_name': FSU,
         'title': 'Advanced Laboratory', 'credits': 2, 'contact_hours': None,
         'note': ('Catalogued as PHY 4822Lr, the r marking repeatability. "Experiments in atomic '
                  'physics, nuclear physics, and other areas of modern physics. Students are expected '
                  'to work without detailed instructions." Prerequisite PHY 3802L only. MAY BE '
                  'REPEATED TO A MAXIMUM OF 6 CREDIT HOURS for special projects arranged in advance. '
                  'FSU also applies a programme rule that no physics or mathematics course below C- '
                  'counts toward the major.')},
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
