#!/usr/bin/env python
"""Batch 236 -- the engineering gateway: MAC2311/2312/2313, MAP2302, PHY2048/2049, CHM2045.

Ron's rule (2026-09-17): a course that spans a major on a career path gets a
guide. Mechanical Engineer names all seven and the whole ENG cluster shares them.

⚠⚠⚠ THE HEADLINE, and it is in the state's own words. The statewide descriptions
of MAC2311, MAC2312 and MAC2313 are ONE SHARED TOPIC LIST -- MAC2312 and MAC2313
are byte-identical, 980 characters each -- and it ends:

    "THE ABOVE TOPICS APPLY TO THE ENTIRE CALCULUS WITH ANALYTIC GEOMETRY
     SEQUENCE. THE ORDER OF TOPICS MAY VARY IN THE TOTAL CALCULUS WITH ANALYTIC
     GEOMETRY SEQUENCE. THEREFORE, TRANSFERABILITY IS GUARANTEED ONLY IF THE
     ENTIRE SEQUENCE HAS BEEN COMPLETED."

So the identical text is DELIBERATE, not the batch-219 copied-description defect.
And it carries a warning that CONTRADICTS the record's own DS_Transferable1
field, which reads "GUARANTEED TRANSFER TO INSTITUTION OFFERING SAME COURSE."
⚠ Transferring after Calculus II -- extremely common -- is exactly the case the
prose excludes and the field appears to promise.

⚠⚠ SECOND FINDING, across 11 courses now: every RECENTLY REVISED statewide entry
carries the (GE CORE) marker and records ELECTIVE high-school credit, while its
UNREVISED partner records the SUBJECT credit:

    revised + GE CORE + ELECTIVE : ENC1101 STA2023 BSC2085 MAC2311 PHY2048 CHM2045
    1980s, no marker, SUBJECT    : BSC2086(SCIENCE) MAC2312/2313(MATHEMATICS) PHY2049(SCIENCE)

That inverts what a student would expect: the FIRST course of each sequence --
the one most likely taken in high school -- gives the WEAKER high-school credit.
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
    'Florida&rsquo;s limited General Education Core list (s. 1007.25, F.S.). <strong>A core course '
    'satisfies its general-education subject area at every Florida public college and university '
    'and carries that status in transfer</strong> &mdash; stronger than the ordinary '
    '&ldquo;guaranteed transfer to an institution offering the same course&rdquo; promise.</p>')

GORDON = (
    '<h3>Gordon Rule: the grade that counts is a C</h3>'
    '<p>Florida requires designated mathematics coursework for a degree (Rule 6A-10.030). '
    '<strong>&#9888; A grade of C or higher is required for a Gordon Rule course to count &mdash; a '
    'C-minus does not</strong>, which is stricter than passing and catches people out. The '
    'designation is made by the institution rather than by the number, so check your own '
    'institution&rsquo;s list.</p>')

SEQ_WARNING = (
    '<h3>&#9888;&#9888;&#9888; Transfer is guaranteed only if you finish the whole sequence</h3>'
    '<p>This is the most important thing on this page, and it is in the state&rsquo;s own words. '
    'The SCNS record for the calculus sequence carries <strong>one shared topic list across '
    '<code>MAC2311</code>, <code>MAC2312</code> and <code>MAC2313</code></strong> &mdash; the '
    'descriptions for the second and third courses are identical &mdash; and it ends:</p>'
    '<blockquote><p>&ldquo;The above topics apply to the entire Calculus with Analytic Geometry '
    'sequence. The order of topics may vary in the total Calculus with Analytic Geometry sequence. '
    '<strong>Therefore, transferability is guaranteed only if the entire sequence has been '
    'completed.</strong>&rdquo;</p></blockquote>'
    '<p>&#9888;&#9888; <strong>Note what that excludes.</strong> The same record&rsquo;s '
    'transferability field reads &ldquo;guaranteed transfer to institution offering same '
    'course&rdquo; &mdash; but the prose says the guarantee attaches to the <em>completed '
    'sequence</em>, because institutions order the topics differently. <strong>Transferring after '
    'Calculus I or Calculus II is exactly the case the guarantee does not cover</strong>, and it is '
    'a very common thing to do.</p>'
    '<p><strong>What to do about it:</strong> if you expect to transfer mid-sequence, finish the '
    'sequence at one institution where you can. Where you cannot, take the syllabus and a topic '
    'list to the receiving department <em>before</em> you enrol in the next course, and get the '
    'placement in writing. A student who has done series but not multivariable material, or the '
    'reverse, is the case this warning exists for.</p>')

DUAL = (
    '<h3>&#9888; Dual enrolment: the high-school credit is not what you would guess</h3>'
    '<p>SCNS records what a dual-enrolled high-school student earns, and across this gateway it '
    'runs <em>opposite</em> to expectation. The recently revised General Education Core entries '
    '&mdash; Calculus I, Physics with Calculus I, General Chemistry I, Composition I, Statistics, '
    'Anatomy and Physiology I &mdash; all record <strong>ELECTIVE</strong> high-school credit. '
    'Their unrevised second halves &mdash; Calculus II and III, Physics II, Anatomy and Physiology '
    'II &mdash; record <strong>MATHEMATICS</strong> or <strong>SCIENCE</strong>.</p>'
    '<p><strong>So the first course of the sequence, the one most likely taken in high school, '
    'carries the weaker high-school credit.</strong> The college credit is unaffected either way. '
    '&#9888; If you are relying on this to fill a high-school graduation requirement, confirm it '
    'with your counsellor and your district articulation agreement first.</p>')


def split_family(bare, lab, integrated, n_bare, n_lab, n_int, subject):
    return (
        '<h3>Two packagings, and they are equivalent</h3>'
        '<p>Florida teaches %s both ways: <strong>%d institutions</strong> run <code>%s</code> as a '
        'lecture paired with <code>%s</code>, a separate laboratory carried by %d; '
        '<strong>%d</strong> run <code>%s</code>, a single integrated course. '
        '<strong>The outcomes are the same and transfer works either way &mdash; lecture plus '
        'laboratory completes exactly as the combined course does.</strong> Institutions are given '
        'this latitude deliberately.</p>'
        '<p>&#9888; <strong>The one thing to get right is the registration:</strong> where your '
        'institution splits the course, enrol in <em>both</em> halves. They are normally '
        'corequisites, and a science requirement that expects a laboratory will not be met by the '
        'lecture alone.</p>' % (subject, n_bare, bare, lab, n_lab, n_int, integrated))


def guide(title, credits, hours, prereq, html, notes):
    return {'title': title, 'html_content': html, 'credits': credits,
            'contact_hours': hours, 'prerequisites': prereq, 'version': '1.0',
            'offering_notes': notes}


G = {}

CALC_PRE = (
    'No statewide prerequisite is recorded for Calculus I; institutions gate on placement '
    '(precalculus, a qualifying score, or a state exemption). MAC2312 and MAC2313 each suggest the '
    'preceding course. '
    'IMPORTANT - TRANSFER: the SCNS record states that because the order of topics varies between '
    'institutions, "transferability is guaranteed only if the ENTIRE sequence has been completed". '
    'Transferring after Calculus I or II is NOT covered by that guarantee, which is what the '
    'course-level transferability field appears to promise. Finish the sequence at one institution '
    'where you can; otherwise take a topic list to the receiving department and get placement in '
    'writing BEFORE enrolling in the next course. '
    'A Gordon Rule designation is recorded at most carriers - a C or higher is required for it to '
    'count, and a C-minus does not.'
)

CALC_NOTE_TAIL = (
    '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Stewart is the most widely adopted text in Florida; OpenStax <em>Calculus</em> is free and '
    'increasingly used.</li>'
    '<li>Graphing calculator or CAS where permitted &mdash; policies differ sharply by section, so '
    'check before buying.</li>'
    '<li>Institutional tutoring and mathematics labs. Calculus is the most heavily supported course '
    'on most campuses, and the support is free.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>The calculus sequence is not a destination; it is the gate on most quantitative degrees in '
    'Florida. It is named on the <strong>Mechanical Engineer</strong> path in this repository and '
    'is required by every engineering discipline, physics, chemistry, computer science, economics, '
    'statistics and actuarial work. <strong>More students leave engineering over this sequence than '
    'over anything in the major</strong>, which is the honest reason to take it seriously early.</p>')

G['MAC2311'] = guide(
    'Calculus I', 4, 60, CALC_PRE,
    '<h2>Course Description</h2>'
    '<p><strong>Calculus I</strong> is the gateway to every quantitative degree in Florida and, by '
    'a wide margin, the course that decides whether students continue in them. The statewide '
    'description is recent and specific: students <strong>develop problem-solving skills, critical '
    'thinking, computational proficiency and contextual fluency</strong> through limits, '
    'derivatives, and definite and indefinite integrals of functions of one variable &mdash; '
    'algebraic, exponential, logarithmic and trigonometric &mdash; and their applications.</p>'
    '<p>It is carried by <strong>39 Florida public institutions</strong>. &#9888; <strong>The credit '
    'value is not settled</strong>: 31 carry it at 4 credits and 16 at 5 &mdash; see Offering Notes, '
    'because it affects your degree audit.</p>'
    '<p>&#9888;&#9888; The statewide title carries the <strong>(GE CORE)</strong> marker.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Evaluate <strong>limits</strong> and determine continuity.',
         'Differentiate algebraic and transcendental functions, and interpret the derivative as a <strong>rate of change</strong>.',
         'Apply differentiation to <strong>optimisation</strong>, related rates and curve sketching.',
         'Evaluate definite and indefinite <strong>integrals</strong> and apply the Fundamental Theorem of Calculus.',
         'Use calculus to model and solve <strong>applied problems</strong> in context.')
    + '<h3>Optional Outcomes</h3>'
    + li('Use a computer algebra system or graphing technology as part of the work.',
         'Extend to numerical integration or differential-equation previews where time allows.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Limits and continuity.', 'The derivative: definition, rules, chain rule, implicit differentiation.',
         'Applications of the derivative: rates, optimisation, the Mean Value Theorem, curve sketching.',
         'Antiderivatives and the definite integral.', 'The Fundamental Theorem of Calculus; substitution.',
         'Transcendental functions: exponential, logarithmic, trigonometric and their inverses.')
    + '<h3>Optional Topics</h3>'
    + li('Areas between curves and volumes of revolution, where the institution places them here.',
         'L&rsquo;H&ocirc;pital&rsquo;s rule and indeterminate forms.')
    + CALC_NOTE_TAIL
    + '<h2>Special Information</h2>' + GE_CORE + SEQ_WARNING + GORDON + DUAL
    + '<h3>&#9888; Four credits or five?</h3>'
    '<p>Thirty-one institutions award <strong>4 credits</strong> and sixteen award <strong>5</strong>. '
    'The state&rsquo;s own record says &ldquo;credits: 4-5 semester hours&rdquo;. The five-credit '
    'versions generally carry extra scheduled contact time rather than extra content. '
    '<strong>Check the number your degree audit expects</strong> &mdash; in tightly budgeted majors '
    'a one-credit difference surfaces late, at the final audit.</p>',
    {'summary': '39 Florida public institutions carry MAC2311; 31 at 4 credits and 16 at 5. '
                'The statewide record itself states 4-5 semester hours.',
     'hours_source': 'derived', 'derived_contact_hours': 60,
     'derivation': 'Florida convention of 15 contact hours per credit applied to the modal '
                   '4-credit value. A 5-credit offering runs about 75.',
     'offerings': [
         {'institution': 'GCSC', 'institution_name': 'Gulf Coast State College',
          'title': 'Calculus I', 'credits': None, 'contact_hours': None,
          'note': 'Gulf Coast publishes this prefix but its hours were not extractable in this pass.'},
         {'institution': 'UCF', 'institution_name': 'University of Central Florida',
          'title': 'Calculus with Analytic Geometry I', 'credits': 4, 'contact_hours': None,
          'note': 'Also carries the MAC2311C form.'}]})

for cid, name, ordinal, desc, outs, tops, ncar in [
    ('MAC2312', 'Calculus II', 'second',
     'takes up techniques of integration, applications of the integral, and the theory of infinite '
     'sequences and series',
     ('Apply <strong>techniques of integration</strong> &mdash; parts, trigonometric substitution, partial fractions.',
      'Evaluate <strong>improper integrals</strong> and recognise convergence.',
      'Determine convergence of <strong>sequences and series</strong> using standard tests.',
      'Represent functions as <strong>power and Taylor series</strong>.',
      'Work with <strong>parametric equations and polar coordinates</strong>.'),
     ('Techniques of integration.', 'Applications of integration: volume, arc length, surface area, work.',
      'Improper integrals.', 'Sequences and series; convergence tests.',
      'Power series, Taylor and Maclaurin series.', 'Parametric equations and polar coordinates.'), 37),
    ('MAC2313', 'Calculus III', 'third',
     'extends calculus to functions of several variables: vectors, partial derivatives, multiple '
     'integrals and vector fields',
     ('Work with <strong>vectors</strong> in the plane and in three-space.',
      'Compute <strong>partial derivatives</strong>, directional derivatives and gradients.',
      'Find extrema of functions of several variables, including <strong>Lagrange multipliers</strong>.',
      'Evaluate <strong>multiple integrals</strong> in rectangular, cylindrical and spherical coordinates.',
      'Apply the theorems of <strong>vector calculus</strong> &mdash; line and surface integrals, Green, Stokes, divergence.'),
     ('Vectors and the geometry of three-space.', 'Vector-valued functions; curvature.',
      'Partial derivatives, gradients, directional derivatives.',
      'Optimisation of functions of several variables.',
      'Double and triple integrals; change of coordinates.',
      'Vector fields, line and surface integrals; Green, Stokes and divergence theorems.'), 36),
]:
    G[cid] = guide(
        name, 4, 60, CALC_PRE,
        '<h2>Course Description</h2>'
        '<p><strong>%s</strong> is the %s course of Florida&rsquo;s calculus sequence. It %s.</p>'
        '<p>It is carried by <strong>%d Florida public institutions</strong>, most at 4 credits and '
        'a substantial minority at 5.</p>'
        '<p>&#9888;&#9888; <strong>The statewide record does not describe this course on its own.</strong> '
        'SCNS carries one shared topic list for the whole sequence, and the entries for Calculus II '
        'and Calculus III are <em>identical</em>. That is deliberate &mdash; institutions order the '
        'topics differently &mdash; but it means the outcomes and topics below are drawn from what '
        'Florida institutions actually teach at this point in the sequence, not quoted from the '
        'state. It also carries a transfer consequence that is the most important thing on this '
        'page.</p>' % (name, ordinal, desc, ncar)
        + '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>' + li(*outs)
        + '<h3>Optional Outcomes</h3>'
        + li('Use a computer algebra system for symbolic or numerical work.',
             'Applications drawn from the institution&rsquo;s served majors &mdash; engineering, physics, economics.')
        + '<h2>Major Topics</h2><h3>Required Topics</h3>' + li(*tops)
        + '<h3>Optional Topics</h3>'
        + li('Topics the institution moves between the second and third courses &mdash; series and '
             'polar coordinates are the usual movers.')
        + CALC_NOTE_TAIL
        + '<h2>Special Information</h2>' + SEQ_WARNING + GORDON + DUAL
        + '<h3>&#9888; Topic order varies, and that is the point of the warning</h3>'
        '<p>Because Florida does not fix where series, polar coordinates or vectors sit in the '
        'sequence, two students who have both &ldquo;finished Calculus II&rdquo; may have covered '
        'materially different material. <strong>That is why the state guarantees transfer only on '
        'the completed sequence</strong>, and why a topic list settles a placement question that a '
        'course number cannot.</p>',
        {'summary': '%d Florida public institutions carry %s, most at 4 credits with a substantial '
                    'minority at 5.' % (ncar, cid),
         'hours_source': 'derived', 'derived_contact_hours': 60,
         'derivation': 'Florida convention of 15 contact hours per credit at the modal 4 credits.',
         'offerings': [{'institution': 'UCF', 'institution_name': 'University of Central Florida',
                        'title': name, 'credits': 4, 'contact_hours': None,
                        'note': 'Representative of the 4-credit majority.'}]})

G['MAP2302'] = guide(
    'Differential Equations', 3, 45,
    'Statewide the suggested preparation is the calculus sequence (MAC2311-MAC2313 range); most '
    'institutions require Calculus II at minimum and many require Calculus III. '
    'IMPORTANT: this course is where the calculus sequence starts paying off, and it is unforgiving '
    'of gaps - integration technique especially. If you struggled with techniques of integration or '
    'series, revise them BEFORE the term starts rather than during it. '
    'A Gordon Rule designation is recorded at most carriers; a C or higher is required for it to '
    'count, and a C-minus does not. '
    'REGISTER BY NUMBER: 37 Florida public institutions carry MAP2302, almost all at 3 credits.',
    '<h2>Course Description</h2>'
    '<p><strong>Differential Equations</strong> is where calculus becomes the language of physical '
    'systems. The statewide record lists methods of solution of ordinary differential equations; '
    'linear equations and systems of linear equations; operators, undetermined coefficients, '
    'variation of parameters, Laplace transforms and series solutions; and boundary value '
    'problems.</p>'
    '<p>It is carried by <strong>37 Florida public institutions</strong>, almost all at 3 '
    'credits.</p>'
    '<p>&#9888; The statewide entry is an older numbered list rather than a recently written '
    'description, so it should be read as a definition of the subject rather than a statement of '
    'any institution&rsquo;s current syllabus.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Classify differential equations by order, linearity and type.',
         'Solve <strong>first-order</strong> equations: separable, linear, exact.',
         'Solve <strong>higher-order linear</strong> equations with constant coefficients, using undetermined coefficients and variation of parameters.',
         'Apply <strong>Laplace transforms</strong> to initial-value problems, including discontinuous forcing.',
         'Solve <strong>systems</strong> of linear differential equations.',
         'Model and interpret applied problems &mdash; growth and decay, mixing, circuits, mechanical vibration.')
    + '<h3>Optional Outcomes</h3>'
    + li('Series solutions about ordinary and singular points.',
         'Numerical methods (Euler, Runge-Kutta) and software such as MATLAB or Python.',
         'Boundary value problems and Fourier series, where the institution includes them.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('First-order equations and applications.',
         'Linear equations of higher order; the characteristic equation.',
         'Undetermined coefficients and variation of parameters.',
         'Laplace transforms.', 'Systems of linear differential equations.')
    + '<h3>Optional Topics</h3>'
    + li('Series solutions.', 'Numerical methods.', 'Boundary value problems and Fourier series.',
         'Phase-plane and qualitative analysis.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Boyce &amp; DiPrima and Zill are the widely adopted texts; open alternatives exist.</li>'
    '<li>MATLAB, Python (SciPy) or Maple, where the institution includes numerical work.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Required by every engineering discipline and by physics; named on the '
    '<strong>Mechanical Engineer</strong> path in this repository. Vibration, control systems and '
    'transient heat transfer are all differential equations in different clothing, so this is the '
    'course those later courses assume.</p>'
    '<h2>Special Information</h2>' + GORDON
    + '<h3>&#9888; The calculus sequence warning reaches this course too</h3>'
    '<p>Because Florida guarantees transfer on the <em>completed</em> calculus sequence rather than '
    'on its individual courses, a student who arrives here having taken calculus at more than one '
    'institution may have gaps &mdash; series and techniques of integration are the usual ones, and '
    'both are used heavily. <strong>Check your own coverage against this course&rsquo;s '
    'prerequisites rather than assuming the course numbers line up.</strong></p>'
    '<h3>Dual enrolment</h3>'
    '<p>SCNS records <strong>ELECTIVE</strong> high-school credit, which is unsurprising: '
    'differential equations is not a high-school subject. The college credit is unaffected.</p>',
    {'summary': '37 Florida public institutions carry MAP2302, almost all at 3 credits. Gulf Coast '
                'State College publishes 3 lecture hours per week.',
     'hours_source': 'published', 'derived_contact_hours': 45,
     'derivation': 'Gulf Coast State College publishes 3 credit hours and 3 lecture hours per week, '
                   'which is 45 contact hours over a 15-week term.',
     'offerings': [{'institution': 'GCSC', 'institution_name': 'Gulf Coast State College',
                    'title': 'Differential Equations', 'credits': 3, 'contact_hours': 45,
                    'note': 'Publishes 3 lecture hours per week.'}]})


def main():
    os.makedirs(DRAFTS, exist_ok=True)
    for cid, g in G.items():
        io.open(os.path.join(DRAFTS, '%s_guide.json' % cid), 'w', encoding='utf-8').write(
            json.dumps(g, ensure_ascii=False, indent=1))
        print('%-9s %-28s %d cr / %d hrs | prereq %4d | html %6d'
              % (cid, g['title'][:28], g['credits'], g['contact_hours'],
                 len(g['prerequisites']), len(g['html_content'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
