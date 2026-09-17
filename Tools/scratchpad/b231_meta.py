"""Batch 231 metadata -- PHI (philosophy), the four queued rows.

All four: 3 credits / 45 contact hours, derived by the 1:15 convention. NO
institution publishes a contact-hour figure anywhere in the PHI prefix.

*** AN UNUSUALLY CLEAN PREFIX -- and the batch-199 rule says to SAY SO ***
All four courses: both carriers at 3 credits, titles matching in substance, no
subject collisions, no credit divergence, no misfiling. After several batches of
severe divergence this is worth stating rather than hunting for a problem.
⚠ hs_credit, transferable AND dual_enrollment are 607/607 uniform -- total
boilerplate, correctly dropped, one line per guide saying so.

*** HEADLINE: the GORDON RULE designation is institutional POLICY, and the
    designation RATE varies from 7% to 92% between institutions ***

Every one of the four courses has EXACTLY ONE of its two carriers designating it:

  PHI3200   FGCU designates    UWF does NOT
  PHI3452   UWF designates     FSU does NOT
  PHI3790   UWF designates     UCF does NOT
  PHI3880   UWF designates     UNF does NOT

⚠⚠ Four for four. That is the cleanest demonstration the project has of the
batch-201 rule that designation is made by the INSTITUTION, not the course.

⚠⚠⚠ And one Counter over the prefix quantifies WHY, which is the new part.
Gordon Rule designation rate, undergraduate public PHI (464 rows, 132 designated
= 28% overall):

    IRSC  11/12  92%        FAU    8/44  18%
    GCSC   6/8   75%        UNF    4/39  10%
    UWF   14/24  58%        UCF    6/68   9%
    USF   10/20  50%        FIU    3/40   7.5%
    FGCU   5/17  29%        FSU    2/29   7%

Institutions differ by a factor of THIRTEEN. So the per-course observation is
not four coincidences -- it is institutional policy showing through, and the
batch-230 rule (check whether it is a prefix-wide institutional pattern before
writing it up per-course) applies to DESIGNATIONS as well as to credits.

⚠ PHI3200 is the useful counter-case: UWF designates 58% of its philosophy
courses and FGCU 29%, yet on THIS number it is FGCU that designates and UWF that
does not. So the rate predicts the tendency and NOT the individual course --
which is exactly why the guide has to tell the student to check their own list.

⚠ SFC shows gordon_rule=0 with gordon_writing=4 -- the batch-206 finding that
the two flags are populated independently and inconsistently, confirmed again.

*** VALIDATION WORTH RECORDING: the flat-file flags matched the catalogue 4/4 ***
UWF's PDF carries "Meets College-Level Communication Skills Requirement" on
PHI3452, PHI3790 and PHI3880 and NOT on PHI3200 -- exactly matching the flat
file's gordon_rule/gordon_writing flags. ⚠ The batch-179 rule (that UWF label IS
the Gordon Rule writing designation) and the flag data corroborate each other
independently. Good reason to trust both.

*** SCOPE DIVERGENCES, both modest and both real ***

PHI3790 African Philosophy -- the interesting one.
  UCF: statewide text VERBATIM, "primary emphasis on POST-COLONIAL philosophy in
       SUB-SAHARAN Africa" -- narrow, by period and region
  UWF: "historical developments and trends... logic, epistemology, metaphysics,
       ethics, religion, and political thought" -- broad, by SUBFIELD
⚠ UCF's text = the statewide text, so UCF is almost certainly the contributor:
this is ONE carrier's reading recorded as the state's, not two sources against
one (batch 227 rule).
⚠⚠⚠ AND THE DIVERGENCE MAPS ONTO A REAL DISCIPLINARY DEBATE -- the
ethnophilosophy argument (Tempels, Hountondji, Odera Oruka's trends) about
whether African philosophy means the post-colonial professional discipline or
the whole intellectual tradition. So the two courses are two defensible
positions in a live controversy, and a good section in EITHER puts that argument
on the syllabus. Handled with a two-column test and an explanation, not a
warning -- the divergence is intelligible rather than arbitrary.

PHI3200 -- statewide says "social and political communities" with no tradition
named; UWF says WESTERN twice and names the canon (Hobbes, Locke, Rousseau,
Smith, Marx). A narrowing, and the normal US shape of the course -- but said
plainly, with a pointer to PHI3790 for students wanting non-Western material.

PHI3452 -- UWF's description is the statewide text verbatim (UWF is the likely
contributor); FSU's is independently worded and AGREES on subject. ⚠ The one
difference: UWF/statewide include "the moral/social implications of evolutionary
theory" and FSU's description lists only theoretical problems and names "the
tools of ANALYTIC PHILOSOPHY". So the ethics half may be absent at FSU -- which
is the half students most often assume the course is about. Two-column test.
⚠ Also flagged: no prerequisite anywhere, but the course ASSUMES evolutionary
theory the gate does not require -- the batch-189 "description names a
discipline the prerequisite omits" shape. The guide names what to read first.

PHI3880 -- no divergence found. UNF unreadable. ⚠ Cross-referenced deliberately
to the FIL prefix written in batch 230 (FIL3833, FIL4036, FIL4364), since this
course supplies the conceptual vocabulary those use without justifying. Its AI
section argues generative video is a live test case for Bazinian realism, which
is the course's own central problem rather than a bolt-on.

*** SOURCE CHANGE: FGCU IS NOW BLOCKED -- see REVIEW_QUEUE item 104 ***
catalog.fgcu.edu/courses/<pfx>/<pfx>.pdf returns EMPTY 202 on phi, mue, bsc,
egn, eng -- 6 requests across 2 days and 5 prefixes. The register calls FGCU
"the single most productive cross-check source in the project". ⚠ Recorded as
blocked-as-of-today WITH the batch-183 caution (blocks are rate-triggered) and
an instruction to re-probe, NOT as permanent.

Prefix: 295 live ids, 205 single-carrier (69%), max 37 carriers.
Sources: UWF PDF (all four), FSU bulletin, UCF Kuali. FGCU and UNF unreachable.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
UNF = 'University of North Florida'
UCF = 'University of Central Florida'
FSU = 'Florida State University'
FGCU = 'Florida Gulf Coast University'

# Shared block -- the Gordon Rule split, which is true of all four and is the
# batch's headline. Spent four times, so kept tight.
GR = ('*** THE GORDON RULE DESIGNATION DIFFERS BETWEEN THE CARRIERS - exactly one designates it, and '
      'where designated a grade of C OR HIGHER is required to count. It is set by the INSTITUTION, not '
      'the number: check your own list and confirm it transfers. ')

NEW = {

  'PHI3200': {
    'title': 'Social and Political Philosophy',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE statewide or at either carrier - no prior philosophy required. ' + GR +
      'On THIS number it is FGCU that designates and UWF that does not, which inverts their general '
      'habits (UWF designates 58% of its philosophy courses, FGCU 29%) - so the number cannot be '
      'inferred from the institution. '
      '*** SCOPE: the statewide description does not say WESTERN; UWF says it twice and names the '
      'canon - Hobbes, Locke, Rousseau, Adam Smith, Marx. That is the normal US shape of the course, '
      'but if you want comparative or non-Western political philosophy you will not get it here; look '
      'at PHI3790 African Philosophy instead. '
      '*** THE READING IS THE WORKLOAD and it is not compressible - these texts are read slowly and '
      'twice. Read before the seminar, not after.'),
    'offering_notes': {
      'summary': ('Two public carriers, both 3 credits, titles matching in substance. The Gordon Rule '
                  'designation differs. No institution publishes contact hours anywhere in PHI.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': "Florida's 1:15 convention on 3 credits; both carriers list 3.",
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Social and Political Philosophy', 'credits': 3, 'contact_hours': None,
         'note': ('Department of History and Philosophy. Examines "foundational and contemporary '
                  'theories and ideals that have shaped WESTERN social and political thought" through '
                  'Hobbes, Locke, Rousseau, Smith and Marx, plus contemporary applications; themes '
                  'include the origin of law, political authority and legitimacy, human nature, '
                  'economic relations and social power. NO Gordon Rule designation recorded.')},
        {'institution': 'FGCU', 'institution_name': FGCU,
         'title': 'Social-Political Philosophy', 'credits': 3, 'contact_hours': None,
         'note': ('Matches the statewide title exactly. GORDON RULE WRITING DESIGNATION recorded - C or '
                  'higher required. FGCU\'s catalogue returned no course content when probed for this '
                  'batch, so its own description could not be read; the syllabus is the authority on '
                  'whether it draws the field as broadly as the statewide description does.')},
      ],
    },
  },

  'PHI3452': {
    'title': 'Philosophy of Biology',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE statewide or at either carrier. ' + GR +
      '*** BUT IT ASSUMES BIOLOGY THE GATE DOES NOT REQUIRE. The arguments turn on what selection acts on '
      'and whether a trait is an adaptation, and you cannot follow them without knowing selection, '
      'drift, fitness and inheritance. Coming from philosophy with no biology, read a short evolution '
      'primer before the term starts. '
      '*** CHECK WHETHER YOUR SECTION INCLUDES THE ETHICS. UWF and the state name "the moral/social '
      'implications of evolutionary theory"; FSU\'s description lists only theoretical '
      'problems and names "the tools of analytic philosophy". The implications half - sociobiology, '
      'the naturalistic fallacy, the history of eugenics - is what most assume it is about, and a '
      'theoretical section may not cover it.'),
    'offering_notes': {
      'summary': ('Two public carriers, both 3 credits, identical titles, agreeing on subject from two '
                  'independently worded descriptions. The Gordon Rule designation differs.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Florida's 1:15 convention on 3 credits; both carriers list 3. Expect to read "
                     'papers twice - once for the biology and once for the argument.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Philosophy of Biology', 'credits': 3, 'contact_hours': None,
         'note': ('Department of History and Philosophy. Its description is the STATEWIDE TEXT VERBATIM '
                  '- so UWF is almost certainly the contributor and the state record does not '
                  'independently corroborate it. Includes "the moral/social implications of '
                  'evolutionary theory". GORDON RULE WRITING DESIGNATION - C or higher required.')},
        {'institution': 'FSU', 'institution_name': FSU,
         'title': 'Philosophy of Biology', 'credits': 3, 'contact_hours': None,
         'note': ('"Introduces the major debates in philosophy of biology, including those surrounding '
                  'the extended evolutionary synthesis, laws of evolution, units of selection, '
                  'adaptationism, speciation... brings together the biological sciences and the tools '
                  'of ANALYTIC PHILOSOPHY." Independently worded, and the genuine second source. No '
                  'ethics component stated. No Gordon Rule designation recorded.')},
      ],
    },
  },

  'PHI3790': {
    'title': 'African Philosophy',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'Statewide: JUNIOR STANDING OR CONSENT OF INSTRUCTOR. Neither carrier adds a course '
      'prerequisite, so no prior philosophy is required - the gate is class standing. ' + GR +
      '*** THE CARRIERS DRAW THE FIELD AT DIFFERENT SIZES. UCF (whose text is the statewide text verbatim, '
      'so it is the likely contributor) emphasises POST-COLONIAL philosophy in SUB-SAHARAN Africa; UWF '
      'organises the whole tradition BY SUBFIELD - logic, epistemology, ethics, religion, political '
      'thought. '
      '*** THAT GAP IS A REAL DISCIPLINARY ARGUMENT - the ethnophilosophy debate over '
      'whether African philosophy means the post-colonial discipline or the whole intellectual '
      'tradition. A good section in EITHER puts that argument on the syllabus. Read yours if you need '
      'one of the two specifically.'),
    'offering_notes': {
      'summary': ('Two public carriers, both 3 credits, identical titles, differing in how widely they '
                  'draw the field. The Gordon Rule designation differs.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': "Florida's 1:15 convention on 3 credits; both carriers list 3.",
      'offerings': [
        {'institution': 'UCF', 'institution_name': UCF,
         'title': 'African Philosophy', 'credits': 3, 'contact_hours': None,
         'note': ('"Traditional and contemporary African philosophical thought with primary emphasis on '
                  'post-colonial philosophy in sub-Saharan Africa." This is the STATEWIDE DESCRIPTION '
                  'VERBATIM, so UCF is almost certainly its contributor - the state record repeats UCF '
                  'rather than corroborating it. No Gordon Rule designation recorded.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'African Philosophy', 'credits': 3, 'contact_hours': None,
         'note': ('Department of History and Philosophy. "Examines historical developments and trends in '
                  'African philosophy... Distinctive areas in philosophy covered include logic, '
                  'epistemology, metaphysics, ethics, religion, and political thought." Organised by '
                  'SUBFIELD rather than by period or region, and states no post-colonial or sub-Saharan '
                  'restriction. GORDON RULE WRITING DESIGNATION - C or higher required.')},
      ],
    },
  },

  'PHI3880': {
    'title': 'Philosophy of Film',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE statewide or at either carrier - neither prior philosophy nor prior film study. ' + GR +
      '*** THIS IS A PHILOSOPHY COURSE, NOT A FILM COURSE. It asks what kind of thing a film is and '
      'how it means, and it is assessed by philosophical argument in writing. Florida numbers film '
      'history, genre and production separately under FIL - FIL3833 Film Styles, FIL4036 Film History 1, '
      'FIL4364 Documentary. They complement each other: this course supplies the vocabulary (realism, '
      'formalism) those use without justifying. '
      '*** BUDGET FOR TWO LOADS: philosophical reading is slow and read twice, and screenings are '
      'extra and often feature length. Fall behind on viewing and the papers become impossible - '
      'every claim must anchor to a specific scene.'),
    'offering_notes': {
      'summary': ('Two public carriers, both 3 credits, identical titles, no subject divergence found. '
                  'The Gordon Rule designation differs.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': "Florida's 1:15 convention on 3 credits; both carriers list 3.",
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Philosophy of Film', 'credits': 3, 'contact_hours': None,
         'note': ('Department of History and Philosophy. "Investigates the major theoretical and '
                  'conceptual issues surrounding the art of film. Philosophical concepts underlying '
                  'film theories such as realism, formalism, hermeneutics, and structuralism will be '
                  'examined and applied to cinematography, editing, sound, and mise en scene. Other '
                  'conceptual issues may include perception, representation, narrative, and ideology." '
                  'GORDON RULE WRITING DESIGNATION - C or higher required.')},
        {'institution': 'UNF', 'institution_name': UNF,
         'title': 'Philosophy of Film', 'credits': 3, 'contact_hours': None,
         'note': ("UNF's live catalogue is client-rendered and its archived catalogue PDFs are blocked "
                  'at the host, so its own description could not be read; title and credits are from '
                  'the statewide record. No Gordon Rule designation recorded.')},
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
