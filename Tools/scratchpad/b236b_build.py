#!/usr/bin/env python
"""Batch 236b -- PHY2048, PHY2049, CHM2045.

The science half of the engineering gateway. All three are split-family: a
lecture with a separate laboratory, or a single integrated C course, and the two
packagings are equivalent (Ron, 2026-09-17).
"""
import io
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFTS = os.path.join(HERE, '..', 'drafts')
LG = '<ul class="list-group list-group-flush">'
LI = '<li class="list-group-item">'


def li(*items):
    return LG + ''.join(LI + i + '</li>' for i in items) + '</ul>'


GE_CORE = (
    '<h3>A Florida General Education Core course</h3>'
    '<p>The statewide title carries the <strong>(GE CORE)</strong> marker, identifying a course on '
    'Florida&rsquo;s limited General Education Core list (s. 1007.25, F.S.). <strong>It satisfies '
    'its general-education subject area at every Florida public college and university and carries '
    'that status in transfer.</strong> &#9888; The protection attaches to the subject area, not to '
    'a laboratory component &mdash; whether a programme&rsquo;s &ldquo;science with laboratory&rdquo; '
    'requirement is met is a programme rule.</p>')

DUAL = (
    '<h3>&#9888; Dual enrolment: the high-school credit runs opposite to expectation</h3>'
    '<p>Across this gateway the recently revised General Education Core entries record '
    '<strong>ELECTIVE</strong> high-school credit, while their unrevised second halves record the '
    'subject credit. Physics with Calculus I records ELECTIVE; <strong>Physics with Calculus II '
    'records SCIENCE</strong>. The same inversion appears in the anatomy sequence and in calculus. '
    '<strong>So the first course &mdash; the one most likely taken in high school &mdash; carries '
    'the weaker high-school credit.</strong> The college credit is unaffected. Confirm with your '
    'counsellor and district articulation agreement before relying on it.</p>')


def packaging(subject, bare, lab, integ, n_bare, n_lab, n_int, extra=''):
    return ('<h3>Two packagings, and they are equivalent</h3>'
            '<p>Florida teaches %s both ways. <strong>%d institutions</strong> run <code>%s</code> '
            'as a lecture alongside <code>%s</code>, a separate laboratory carried by %d; '
            '<strong>%d</strong> run <code>%s</code>, one integrated course. <strong>The outcomes '
            'are the same and transfer works either way &mdash; lecture plus laboratory completes '
            'exactly as the combined course does.</strong> Institutions are given this latitude '
            'deliberately.</p>'
            '<p>&#9888; <strong>Get the registration right:</strong> where your institution splits '
            'the course, enrol in <em>both</em> halves. They are normally corequisites, and an '
            'engineering or science programme that requires a laboratory will not accept the '
            'lecture alone.%s</p>' % (subject, n_bare, bare, lab, n_lab, n_int, integ, extra))


def guide(title, credits, hours, prereq, html, notes):
    return {'title': title, 'html_content': html, 'credits': credits, 'contact_hours': hours,
            'prerequisites': prereq, 'version': '1.0', 'offering_notes': notes}


G = {}

G['PHY2048'] = guide(
    'General Physics with Calculus I', 4, 60,
    'No statewide prerequisite is recorded, but this is the CALCULUS-BASED physics course: '
    'institutions normally require Calculus I first or alongside. '
    'TAKE THE RIGHT ONE: Florida also runs an algebra-based general physics sequence under '
    'different numbers. Engineering, physics and most physical-science degrees require the '
    'calculus-based version, and the algebra-based one will not substitute. Check the number your '
    'programme names. '
    'REGISTRATION: 25 Florida public institutions carry PHY2048 as a lecture, 24 of them alongside '
    'the 1-credit PHY2048L laboratory; 14 carry the integrated PHY2048C instead. Lecture plus lab '
    'completes exactly as the combined course does - but enrol in BOTH halves where your school '
    'splits them, because a programme requiring a laboratory will not accept the lecture alone. '
    'Credit values differ: roughly 12 institutions at 3 credits and 15 at 4.',
    '<h2>Course Description</h2>'
    '<p><strong>General Physics with Calculus I</strong> is the first half of the calculus-based '
    'physics sequence taken by engineering and physical-science majors. The statewide description '
    'is recent and specific: a calculus-based course covering <strong>kinematics, dynamics, energy, '
    'momentum, rotational motion, fluid dynamics, oscillatory motion and waves</strong>, designed '
    'for science and engineering majors and integrating critical thinking, analytical skills and '
    'real-world applications.</p>'
    '<p>It is carried by <strong>25 Florida public institutions</strong> as a lecture, with a '
    'further 14 running the integrated <code>PHY2048C</code>.</p>'
    '<p>&#9888;&#9888; The statewide title carries the <strong>(GE CORE)</strong> marker.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Solve analytical problems describing <strong>motion</strong> in one and two dimensions.',
         'Apply <strong>Newton&rsquo;s laws</strong> to systems of forces, including friction and circular motion.',
         'Apply conservation of <strong>energy and momentum</strong>, including collisions.',
         'Analyse <strong>rotational motion</strong>: torque, moment of inertia, angular momentum.',
         'Apply the principles of <strong>fluid statics and dynamics</strong>.',
         'Describe <strong>oscillatory motion and waves</strong>, including simple harmonic motion.')
    + '<h3>Optional Outcomes</h3>'
    + li('Carry out laboratory measurement with uncertainty analysis (in the laboratory half).',
         'Use computational tools for modelling, where the institution includes them.',
         'Thermodynamics, where the institution places it in the first course.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Measurement, units and vectors.', 'Kinematics in one and two dimensions.',
         'Newton&rsquo;s laws and applications.', 'Work, energy and conservation of energy.',
         'Momentum, impulse and collisions.', 'Rotational kinematics and dynamics; angular momentum.',
         'Static equilibrium; fluids.', 'Oscillations and mechanical waves.')
    + '<h3>Optional Topics</h3>'
    + li('Gravitation and orbital motion.', 'Temperature, heat and the laws of thermodynamics, '
         'where placed here rather than in the second course.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Halliday, Resnick &amp; Walker; Serway; Young &amp; Freedman are the widely adopted texts. '
    'OpenStax <em>University Physics</em> is free and in growing use.</li>'
    '<li>Online homework systems (WebAssign, Mastering Physics) are common and are often a '
    'required purchase separate from the text &mdash; check before the term.</li>'
    '<li>The laboratory half uses standard mechanics apparatus and data-acquisition software.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Required by every engineering discipline and by physics, and named on the '
    '<strong>Mechanical Engineer</strong> path in this repository. Statics and dynamics are the '
    'direct successors of this course, and students who arrive there without fluency in free-body '
    'diagrams meet the gap immediately.</p>'
    '<h2>Special Information</h2>' + GE_CORE
    + packaging('the calculus-based physics sequence', 'PHY2048', 'PHY2048L', 'PHY2048C', 25, 24, 14)
    + '<h3>&#9888;&#9888; Calculus-based, not algebra-based &mdash; and the two are not interchangeable</h3>'
    '<p>Florida runs both an algebra-based and a calculus-based general physics sequence, under '
    'different numbers. <strong>Engineering and physical-science degrees require the calculus-based '
    'version.</strong> The algebra-based sequence is a perfectly good course for health-science and '
    'general-education purposes and will <em>not</em> substitute for this one. If your programme '
    'names a number, take that number.</p>'
    '<h3>&#9888; Credit values differ</h3>'
    '<p>Roughly 12 institutions carry the lecture at <strong>3 credits</strong> and 15 at '
    '<strong>4</strong>; the integrated form runs 4 or 5. Gulf Coast State College publishes 3 '
    'credits with 3 lecture hours, and 1 credit with 3 laboratory hours for <code>PHY2048L</code>. '
    '<strong>Check the value your degree audit expects.</strong></p>' + DUAL,
    {'summary': '25 Florida public institutions carry PHY2048 as a lecture (12 at 3 credits, 15 at '
                '4), 24 alongside the 1-credit PHY2048L; 14 carry the integrated PHY2048C at 4 or 5 '
                'credits. 27 records carry a natural-science general-education designation.',
     'hours_source': 'published', 'derived_contact_hours': 60,
     'derivation': 'Gulf Coast State College publishes 3 credit hours with 3 lecture hours for the '
                   'lecture (45) and 1 credit with 3 laboratory hours for PHY2048L (45). The '
                   'scalar here uses the modal 4-credit value at the Florida 1:15 convention.',
     'offerings': [
         {'institution': 'GCSC', 'institution_name': 'Gulf Coast State College',
          'title': 'General Physics with Calculus I', 'credits': 3, 'contact_hours': 45,
          'note': 'Publishes 3 lecture hours per week; PHY2048L is 1 credit at 3 laboratory hours.'}]})

G['PHY2049'] = guide(
    'General Physics with Calculus II', 3, 45,
    'Statewide prerequisite: CALCULUS. In practice institutions require PHY2048 and normally '
    'Calculus II, since this course uses integration heavily. '
    'REGISTRATION: 26 Florida public institutions carry PHY2049 as a lecture, 24 alongside the '
    '1-credit PHY2049L laboratory; 13 carry the integrated PHY2049C. Lecture plus lab completes '
    'exactly as the combined form does - enrol in BOTH halves where your school splits them. '
    'Credit values differ: about 15 institutions at 3 credits and 13 at 4. '
    'DUAL ENROLMENT: unlike the first course, this one records SCIENCE high-school credit rather '
    'than ELECTIVE. The college credit is unaffected either way; confirm with your counsellor.',
    '<h2>Course Description</h2>'
    '<p><strong>General Physics with Calculus II</strong> completes the calculus-based physics '
    'sequence. The statewide record describes a continued study of <em>mechanics, heat, sound, '
    'light, electricity and magnetism</em> as the second of a two-semester sequence &mdash; in '
    'current Florida practice the course is dominated by <strong>electricity and magnetism</strong>, '
    'with optics and modern-physics topics where time allows.</p>'
    '<p>It is carried by <strong>26 Florida public institutions</strong> as a lecture, with 13 '
    'running the integrated <code>PHY2049C</code>.</p>'
    '<p>&#9888; <strong>The statewide entry for this half is thin and old</strong> &mdash; a single '
    'sentence, where the first course was rewritten recently with explicit learning outcomes. The '
    'outcomes and topics below therefore reflect what Florida institutions actually teach in the '
    'second course rather than quoting the state.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Apply <strong>Coulomb&rsquo;s law</strong> and the concept of the electric field.',
         'Use <strong>Gauss&rsquo;s law</strong> and electric potential to analyse charge distributions.',
         'Analyse <strong>DC circuits</strong>: resistance, capacitance, Kirchhoff&rsquo;s rules, RC behaviour.',
         'Analyse <strong>magnetic fields</strong> and forces, and apply Amp&egrave;re&rsquo;s law.',
         'Apply <strong>Faraday&rsquo;s law</strong> of induction and analyse inductance and AC circuits.',
         'Describe <strong>electromagnetic waves</strong> and apply the principles of optics.')
    + '<h3>Optional Outcomes</h3>'
    + li('Introductory modern physics &mdash; relativity, photons, atomic structure.',
         'Laboratory measurement with uncertainty analysis (in the laboratory half).')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Electric charge, field and Gauss&rsquo;s law.', 'Electric potential and capacitance.',
         'Current, resistance and DC circuits.', 'Magnetic fields and sources of magnetic field.',
         'Faraday&rsquo;s law, inductance and AC circuits.',
         'Maxwell&rsquo;s equations and electromagnetic waves.')
    + '<h3>Optional Topics</h3>'
    + li('Geometric and physical optics.', 'Thermodynamics, where not covered in the first course.',
         'Introductory relativity and quantum ideas.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>The same text as the first course; OpenStax <em>University Physics</em> Volume 2 is the '
    'free option.</li>'
    '<li>Online homework systems are common and often a separate purchase.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Required by every engineering discipline. &#9888; <strong>It matters most to electrical and '
    'computer engineering</strong>, where it is the direct foundation of circuits, electronics and '
    'electromagnetics &mdash; a student heading that way should treat this course as a major course '
    'rather than a general-education requirement.</p>'
    '<h2>Special Information</h2>'
    + packaging('the calculus-based physics sequence', 'PHY2049', 'PHY2049L', 'PHY2049C', 26, 24, 13)
    + '<h3>&#9888; Credit values differ</h3>'
    '<p>About 15 institutions carry the lecture at <strong>3 credits</strong> and 13 at '
    '<strong>4</strong>; the integrated form runs 4 or 5. &#9888; Gulf Coast State College publishes '
    '<strong>4</strong> credits here against <strong>3</strong> for the first course &mdash; so the '
    'two halves are not always the same size even within one institution. <strong>Check both '
    'against your degree audit.</strong></p>' + DUAL,
    {'summary': '26 Florida public institutions carry PHY2049 as a lecture (about 15 at 3 credits, '
                '13 at 4), 24 alongside the 1-credit PHY2049L; 13 carry the integrated PHY2049C.',
     'hours_source': 'published', 'derived_contact_hours': 45,
     'derivation': 'Modal 3-credit value at the Florida 1:15 convention. Gulf Coast State College '
                   'publishes 4 credits and 4 lecture hours for its own offering, and 1 credit at '
                   '3 laboratory hours for PHY2049L.',
     'offerings': [
         {'institution': 'GCSC', 'institution_name': 'Gulf Coast State College',
          'title': 'General Physics with Calculus II', 'credits': 4, 'contact_hours': 60,
          'note': 'Publishes 4 lecture hours per week - one more than its own first course. '
                  'PHY2049L is 1 credit at 3 laboratory hours.'}]})

G['CHM2045'] = guide(
    'General Chemistry I', 3, 45,
    'No statewide prerequisite is recorded; institutions normally require college algebra or higher '
    'and often a chemistry placement or a preparatory course. '
    'THIS IS THE MAJORS COURSE. Florida also runs a one-term general-education chemistry course '
    'under a different number for non-majors, and it will not substitute where a programme names '
    'this one. The statewide description says this course is "designed for students pursuing '
    'careers in the sciences or who need a more rigorous presentation of chemical concepts". '
    'REGISTRATION: 16 Florida public institutions carry CHM2045 as a lecture, with the 1-credit '
    'CHM2045L laboratory carried by 16; 4 carry the integrated CHM2045C at 4 credits. Lecture plus '
    'lab completes exactly as the combined form does - enrol in BOTH halves where your school '
    'splits them, because programmes requiring a laboratory science will not accept the lecture '
    'alone.',
    '<h2>Course Description</h2>'
    '<p><strong>General Chemistry I</strong> is the first half of the majors-level general '
    'chemistry sequence. The statewide description is recent and explicit about its audience: the '
    'course is <em>&ldquo;designed for students pursuing careers in the sciences or who need a more '
    'rigorous presentation of chemical concepts than is offered in an introductory course&rdquo;</em>, '
    'and covers <strong>atomic theory, electronic and molecular structure, measurement, '
    'stoichiometry, bonding and periodicity</strong>.</p>'
    '<p>It is carried by <strong>16 Florida public institutions</strong> as a lecture at 3 credits, '
    'with a further 4 running the integrated <code>CHM2045C</code> at 4.</p>'
    '<p>&#9888;&#9888; The statewide title carries the <strong>(GE CORE)</strong> marker.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Apply <strong>measurement, units and significant figures</strong> correctly in calculation.',
         'Carry out <strong>stoichiometric</strong> calculations, including limiting reagent and percent yield.',
         'Describe <strong>atomic structure</strong> and electron configuration, and relate them to periodic trends.',
         'Predict <strong>molecular structure and bonding</strong> using Lewis structures, VSEPR and hybridisation.',
         'Apply the <strong>gas laws</strong> and the kinetic molecular theory.',
         'Apply <strong>thermochemistry</strong>: enthalpy, calorimetry, Hess&rsquo;s law.',
         'Describe solutions and carry out solution <strong>concentration</strong> calculations.')
    + '<h3>Optional Outcomes</h3>'
    + li('Laboratory technique, data treatment and uncertainty (in the laboratory half).',
         'Introductory kinetics or equilibrium, where the institution places them in the first course.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Matter, measurement and dimensional analysis.', 'Atoms, molecules and ions; nomenclature.',
         'Stoichiometry and reactions in solution.', 'Thermochemistry.',
         'Electronic structure of atoms; periodic properties.',
         'Chemical bonding; molecular geometry and bonding theories.', 'Gases.')
    + '<h3>Optional Topics</h3>'
    + li('Intermolecular forces and properties of liquids and solids.',
         'Introductory kinetics and equilibrium.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Brown &amp; LeMay, Zumdahl and Tro are the widely adopted texts; OpenStax '
    '<em>Chemistry</em> is free and in growing use.</li>'
    '<li>A scientific calculator; online homework systems are common and often a separate purchase.</li>'
    '<li>The laboratory half carries a fee at most institutions and requires eye protection and '
    'closed footwear &mdash; the safety rules are enforced strictly and a student without them is '
    'usually turned away.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Required by most ABET-accredited engineering programmes, and named on the '
    '<strong>Mechanical Engineer</strong> path in this repository, where it underpins the materials '
    'sequence &mdash; corrosion, bonding and phase behaviour. It is also the gateway to chemistry, '
    'biology, biomedical and environmental degrees and to the health professions.</p>'
    '<h2>Special Information</h2>' + GE_CORE
    + packaging('general chemistry', 'CHM2045', 'CHM2045L', 'CHM2045C', 16, 16, 4)
    + '<h3>&#9888;&#9888; This is the majors sequence, not the general-education course</h3>'
    '<p>Florida numbers a one-term general-education chemistry course separately for non-majors. '
    'The statewide description of <em>this</em> course says plainly that it is for students '
    'pursuing careers in the sciences or needing a more rigorous treatment. <strong>Where a '
    'programme names this number, the non-majors course will not substitute</strong> &mdash; and '
    'the reverse substitution, taking this one to satisfy a general-education requirement, is '
    'usually fine but is worth confirming.</p>'
    '<h3>Dual enrolment</h3>'
    '<p>SCNS records <strong>ELECTIVE</strong> high-school credit for this course, in common with '
    'the other revised General Education Core entries. The college credit is unaffected; confirm '
    'with your counsellor before relying on it for a high-school science requirement.</p>',
    {'summary': '16 Florida public institutions carry CHM2045 as a 3-credit lecture, with the '
                '1-credit CHM2045L laboratory carried by 16; 4 carry the integrated CHM2045C at 4 '
                'credits. 17 records carry a natural-science general-education designation.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the uniform 3-credit '
                   'lecture value. The separate laboratory adds 30-45 hours.',
     'offerings': [
         {'institution': 'GCSC', 'institution_name': 'Gulf Coast State College',
          'title': 'General Chemistry I', 'credits': 3, 'contact_hours': None,
          'note': 'Carries the lecture and CHM2045L separately.'}]})


def main():
    os.makedirs(DRAFTS, exist_ok=True)
    for cid, g in G.items():
        io.open(os.path.join(DRAFTS, '%s_guide.json' % cid), 'w', encoding='utf-8').write(
            json.dumps(g, ensure_ascii=False, indent=1))
        print('%-9s %-34s %d cr / %d hrs | prereq %4d | html %6d'
              % (cid, g['title'][:34], g['credits'], g['contact_hours'],
                 len(g['prerequisites']), len(g['html_content'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
