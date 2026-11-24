# -*- coding: utf-8 -*-
"""Batch 256 (EEL/PLC): limited-information guides for seven requests previously held
(Ron's rule of 2026-11-24: every requested course gets a guide). Run from Tools/.

  EEL2130C  LIMITED INFORMATION  Florida Poly only; title and credits only; two SCNS rows (one discontinued
                                 2025-07-11); not on the 2019-20 BS EE plan nor the current EE programme page.
  EEL4448   LIMITED INFORMATION  Florida Poly only; title, credits, and the 2019-20 BS EE plan's line
                                 "EEL 4448 Optoelectronics (3, EEL 3470 and EEE 4351)" (cached PDF, scratchpad/b248/).
  EEL5025   LIMITED INFORMATION  FAMU-FSU College of Engineering (FAMU and FSU rows); FSU Coursedog record
                                 (fsu_courses.json): description, one outcome, 3 contact hours, Fall.
  EEL5009   LIMITED INFORMATION  FIU only; one-sentence description (fiu_courses.json; catalog.fiu.edu/courses/0360811).
  EEL4081   LIMITED INFORMATION  UNF only, new 2026-08-16; UNF 2026-27 course API lists EEL 4081C, prereq EEL 3111,
                                 one-paragraph description (unf_courses_2026-2027.json).
  EET2525C  LIMITED INFORMATION  SCF only; title and credits; statewide title Industrial Motor Control Lab (L).
  ETS3543L  LIMITED INFORMATION  FAMU only; FAMU BS EET programme page lists it (1 hr) with ETS 3543 (3 hr),
                                 fall of year 4, in both the 124-hour and the fall-2025 120-hour plans.

Sources: SCNS flat file (crslist.txt) for carriers, titles, credits, dates; caches above;
floridacourserepo.com API for every linked course and career path (checked 2026-11-24).
Outside links fetched and read 2026-11-24 (WebFetch):
  floridapoly.edu BS EE page; eng.famu.fsu.edu/ece/graduate/courses; catalog.fiu.edu/courses/0360811;
  cec.fiu.edu MS EE page; famu.edu BS EET page; scf.edu Engineering Technology page;
  digitalcommons.unf.edu/unf_faculty_publications/2063; ece.gatech.edu/courses/ece2040; ece.vt.edu ECE 3134;
  ece.umd.edu ENEE484; utep.edu EE 5301; catalog.csun.edu ECE 309; uwb.edu ECE Foundations certificate;
  pdx.edu ECE bridge; torontomu.ca BME 705 (2026-27); montgomery.edu ELC-128 and ELC-117; uml.edu ETEC.3450;
  MIT OCW 6.002, 6.003, 6.772, 6.336J, 6.811, 18.085; LibreTexts Fiore DC circuits; OpenStax University
  Physics Vol. 3; control.com textbook PLC chapter.
"""
import io
import json
import os

LG = '<ul class="list-group list-group-flush">'
SITE = 'https://floridacourserepo.com'


def li(items):
    return LG + ''.join('<li class="list-group-item">%s</li>' % x for x in items) + '</ul>'


def ul(items):
    return '<ul>' + ''.join('<li>%s</li>' % x for x in items) + '</ul>'


def c(cid, title=None):
    t = '%s %s' % (cid, title) if title else cid
    return '<a href="%s/courses/%s">%s</a>' % (SITE, cid, t)


def path(slug, title):
    return '<a href="%s/careers/%s">%s</a>' % (SITE, slug, title)


def ext(url, text):
    return '<a href="%s">%s</a>' % (url, text)


def table(rows):
    h = ('<table class="table table-sm"><thead><tr><th>Institution</th><th>Title</th><th>Credits</th>'
         '<th>Contact hours</th></tr></thead><tbody>')
    return h + ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % x for x in r) for r in rows) + '</tbody></table>'


def box(text):
    return '<div class="alert alert-warning"><strong>Limited information.</strong> %s</div>' % text


SIMILAR = ' <em>(a similar course, not an equivalent for transfer)</em>'

G = {}

# =============================================================== EEL2130C
G['EEL2130C'] = {
    'title': 'Circuits Analysis',
    'credits': 3,
    'contact_hours': 60,
    'prerequisites': (
        "Florida Polytechnic University, the only Florida public institution with this number, publishes no "
        "prerequisite that could be read for this guide. A first circuits course with a laboratory is commonly "
        "taken after or alongside Calculus I (MAC 2311) and calculus-based Physics II, electricity and magnetism "
        "(PHY 2049 with its lab), with differential equations soon after. Check Florida Poly's current catalogue "
        "and confirm with its Electrical and Computer Engineering department that the course is still offered: "
        "Florida Poly's electrical engineering degree teaches circuits as EEL 3111 and EEL 3112, and EEL2130C may "
        "no longer be scheduled."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries EEL2130C: Florida Polytechnic University, at 3 credits. '
                   'The statewide file holds two Florida Poly records for it (both effective August 2022), one '
                   'active and one discontinued on 11 July 2025.',
        'hours_source': 'derived',
        'derived_contact_hours': 60,
        'derivation': 'Florida Poly publishes no contact hours; 60 is Florida\'s convention for a 3-credit integrated '
                      'lecture and laboratory (C) course.',
        'offerings': [{
            'institution': 'FLPOLY', 'institution_name': 'Florida Polytechnic University',
            'title': 'Circuits Analysis', 'credits': 3, 'contact_hours': None,
            'note': 'Statewide title: Circuits Analysis (L). Not found on Florida Poly\'s current electrical '
                    'engineering programme page or degree plans; possibly dormant.'}],
    },
}
G['EEL2130C']['html_content'] = (
    "<h2>Course Description</h2>"
    + box("Only <em>Florida Polytechnic University</em> offers EEL2130C in Florida's public colleges and "
          "universities, and it publishes only a title and credits. The course may no longer be taught: see "
          "<em>Is it still offered?</em> below. This guide sets out what the record shows and what a first circuits "
          "course with a laboratory commonly covers. Check Florida Poly's syllabus before relying on it.") +
    "<p><strong>EEL2130C Circuits Analysis</strong> is a lower-division (2000-level) electrical engineering course "
    "carrying 3 credits. The <code>C</code> suffix and the statewide title, <strong>Circuits Analysis (L)</strong>, "
    "both mark it as a course with an integrated laboratory. Florida Polytechnic University in Lakeland is the only "
    "Florida public institution that lists the number; it entered the statewide course file in August 2022.</p>"
    "<p>A course of this title is an engineering student's first systematic treatment of electric circuits: the "
    "laws that govern current and voltage in a network of components, the techniques for solving such networks, "
    "and, in the laboratory, building circuits and measuring them with a multimeter, power supply and "
    "oscilloscope. Everything below that goes beyond the title is what such courses commonly cover, not a "
    "statement of Florida Poly's syllabus.</p>"
    "<h3>Is it still offered?</h3>"
    "<p>The statewide course file (September 2025) holds <strong>two</strong> Florida Poly records for EEL2130C with "
    "the same dates, one active and one <strong>discontinued on 11 July 2025</strong>. The number does not appear on "
    "Florida Poly's 2019–20 electrical engineering degree plan, and Florida Poly's electrical engineering degree "
    "plans checked for this site teach circuits as <strong>EEL 3111</strong> and <strong>EEL 3112</strong>, with "
    "EEL 3110 <em>Principles of Electrical Engineering</em> as a service course. EEL2130C may be dormant. A student "
    "who sees it on a transcript or schedule should ask Florida Poly's registrar what it was used for.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>" + li([
        "Define charge, current, voltage, power and energy, and apply the passive sign convention.",
        "Apply <strong>Ohm's law and Kirchhoff's current and voltage laws</strong> to resistive circuits, including "
        "series and parallel combinations and voltage and current division.",
        "Analyse circuits systematically by <strong>nodal and mesh analysis</strong>, including circuits with "
        "dependent sources.",
        "Use superposition, source transformation and <strong>Thévenin and Norton equivalents</strong> to simplify "
        "a circuit, and find the load for maximum power transfer.",
        "In the laboratory, build circuits from a schematic and measure voltage, current and resistance safely, "
        "comparing measurements with calculated values.",
    ]) +
    "<h3>Optional Outcomes</h3>" + li([
        "Analyse ideal operational-amplifier circuits (inverting, non-inverting, summing, difference amplifiers).",
        "Describe capacitors and inductors and find the transient response of first-order RC and RL circuits.",
        "Analyse circuits in sinusoidal steady state with phasors and impedance, and calculate AC power.",
        "Simulate a circuit with SPICE (for example LTspice) and compare the simulation with measurement.",
        "Use an oscilloscope and function generator to observe time-varying signals.",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>" + li([
        "Circuit variables and elements; independent and dependent sources.",
        "Ohm's law, Kirchhoff's laws, series and parallel resistance, voltage and current division.",
        "Nodal analysis and mesh analysis.",
        "Linearity, superposition, source transformation, Thévenin and Norton equivalents, maximum power transfer.",
        "Laboratory practice: instruments, breadboards, measurement error, laboratory safety and reports.",
    ]) +
    "<h3>Optional Topics</h3>" + li([
        "Operational amplifiers.",
        "Capacitors, inductors and first-order transients; possibly second-order (RLC) circuits.",
        "Sinusoids, phasors, impedance and AC power.",
        "Circuit simulation software.",
    ]) +
    "<h2>Resources &amp; Tools</h2>" + ul([
        "A circuits textbook such as Alexander and Sadiku, <em>Fundamentals of Electric Circuits</em>, or Nilsson "
        "and Riedel, <em>Electric Circuits</em>; the course syllabus names the text used.",
        "A scientific calculator that handles complex numbers, and MATLAB or Python for solving simultaneous "
        "equations.",
        "SPICE circuit simulation (LTspice is free).",
        "Laboratory: digital multimeter, DC power supply, function generator, oscilloscope, breadboard and "
        "components.",
    ]) +
    "<h2>Career Pathways</h2>" + ul([
        "Electrical engineers (SOC 17-2071) and electronics engineers (SOC 17-2072): circuit analysis underlies "
        "every later electrical engineering course.",
        "Computer hardware engineers (SOC 17-2061).",
        "Electrical and electronic engineering technicians (SOC 17-3023).",
        "Florida employers include the utilities (Duke Energy Florida, Tampa Electric, Florida Power &amp; Light) and "
        "the aerospace and defence firms of Central Florida and the Space Coast.",
    ]) +
    "<h2>Where to Learn More</h2>" + ul([
        ext('https://floridapoly.edu/academics/programs/undergraduate/electrical-engineering/',
            "Florida Polytechnic University: B.S. in Electrical Engineering") + " — the programme page, with a link "
        "to Florida Poly's course catalogue.",
        c('EEL3111', 'Circuit Analysis I') + " — the first circuits course for engineering majors at FAMU, FAU, "
        "Florida Poly, FSU, UNF and UWF.",
        c('EEL3112', 'Circuit Analysis II') + " — the second course (AC power, three-phase, frequency response).",
        c('EEL3111C', 'Circuits I') + " — the University of Florida's circuits course with an integrated lab.",
        c('EET1015C', 'DC Circuits') + " and " + c('EET1025C', 'AC Circuits') + " — the engineering technology "
        "circuits courses taught at about ten Florida state colleges.",
        path('electrical-engineer', 'Electrical Engineer') + " — the career path these courses lead to.",
        ext('https://ece.gatech.edu/courses/ece2040', 'Georgia Tech ECE 2040 Circuit Analysis') + SIMILAR +
        ": basic DC and AC circuit theory, network theorems, op-amps, first- and second-order circuits and AC "
        "power.",
        ext('https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/',
            'MIT OpenCourseWare 6.002 Circuits and Electronics') + " — free lecture videos, notes, problem sets and "
        "exams.",
        ext('https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Electronics/'
            'DC_Electrical_Circuit_Analysis_-_A_Practical_Approach_(Fiore)',
            'Fiore, <em>DC Electrical Circuit Analysis: A Practical Approach</em>') + " — a free open textbook "
        "(LibreTexts, CC BY-NC-SA).",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>" + table([
        ['Florida Polytechnic University', 'Circuits Analysis', '3',
         'not published (60 by Florida\'s convention for a 3-credit C course)']]) +
    "<p>Statewide title: <em>Circuits Analysis (L)</em>. One of Florida Poly's two records for the number was "
    "discontinued on 11 July 2025.</p>"
    "<h3>FE exam</h3><p>Circuit analysis, DC and AC steady state, is a major topic area of the NCEES Fundamentals of "
    "Engineering (FE) Electrical and Computer exam, the first step toward Professional Engineer licensure.</p>"
    "<h3>Transfer</h3><p>No other Florida institution carries EEL2130C, so a receiving university will evaluate it "
    "against its own first circuits course (EEL 3111 or EEL 3111C) from the syllabus. Keep the syllabus and the "
    "laboratory reports.</p>"
    "<h2>AI Integration (Optional)</h2>"
    "<p>AI tools can explain a method or check algebra, but they make sign errors and misread circuit diagrams "
    "described in words. Verify any answer with a second method (nodal against mesh, or a SPICE simulation) and with "
    "measurement in the lab. Follow the instructor's rules on AI use for each assignment.</p>"
)

# =============================================================== EEL4448
G['EEL4448'] = {
    'title': 'Optoelectronics',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "Florida Polytechnic University, the only Florida public institution with this number, listed the "
        "prerequisites in its 2019-20 B.S. in Electrical Engineering plan as EEL 3470 (Electromagnetic Fields and "
        "Applications) and EEE 4351 (Electronic Devices). No later statement could be read for this guide, so check "
        "Florida Poly's current catalogue. In practice the course assumes electromagnetic waves (Maxwell's "
        "equations, plane waves) and semiconductor device physics (energy bands, the p-n junction). It is an "
        "upper-division elective, normally taken in the senior year."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries EEL4448: Florida Polytechnic University, at 3 credits '
                   '(statewide record effective 2020).',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': 'Florida Poly publishes no contact hours; 45 is Florida\'s convention for a 3-credit lecture '
                      'course.',
        'offerings': [{
            'institution': 'FLPOLY', 'institution_name': 'Florida Polytechnic University',
            'title': 'Optoelectronics', 'credits': 3, 'contact_hours': None,
            'note': 'Programme elective in the 2019-20 B.S. EE plan; prerequisites EEL 3470 and EEE 4351. '
                    'Statewide title: Optoelectronics (U).'}],
    },
}
G['EEL4448']['html_content'] = (
    "<h2>Course Description</h2>"
    + box("Only <em>Florida Polytechnic University</em> offers EEL4448 in Florida's public colleges and "
          "universities, and it publishes only a title, credits and prerequisites. This guide sets out what the record "
          "shows and what an undergraduate optoelectronics course commonly covers. Check Florida Poly's syllabus "
          "before relying on it.") +
    "<p><strong>EEL4448 Optoelectronics</strong> is a 3-credit upper-division electrical engineering course at "
    "Florida Polytechnic University in Lakeland, the only Florida public institution with the number. The statewide "
    "title is the same, <em>Optoelectronics (U)</em>. Florida Poly's 2019–20 B.S. in Electrical Engineering plan "
    "lists it as a programme elective with prerequisites <strong>EEL 3470</strong> (Electromagnetic Fields and "
    "Applications) and <strong>EEE 4351</strong> (Electronic Devices); that is the most specific statement Florida "
    "Poly has published about it. Florida Poly also lists a graduate <em>Advanced Optoelectronics</em> "
    "(EEL5457).</p>"
    "<p>Optoelectronics is the study of devices that convert between electrical signals and light: light-emitting "
    "diodes, semiconductor lasers, photodetectors and solar cells, and the optical fibres and components that carry "
    "light between them. The two prerequisites show the course's two foundations, light as an electromagnetic wave "
    "and the physics of semiconductor devices. What follows is what such a course commonly covers, not a statement "
    "of Florida Poly's syllabus.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>" + li([
        "Relate the wavelength, frequency and photon energy of light, and describe light both as an electromagnetic "
        "wave and as photons.",
        "Explain how semiconductors absorb and emit light: band gap, direct and indirect gaps, absorption, "
        "<strong>spontaneous and stimulated emission</strong>.",
        "Describe the operation and main characteristics of <strong>light-emitting diodes</strong> (efficiency, "
        "spectrum, current–light relation).",
        "Explain how a <strong>semiconductor laser</strong> works: population inversion, optical gain, the resonant "
        "cavity, threshold current and output characteristics.",
        "Describe <strong>photodetectors</strong> (p-n and p-i-n photodiodes, avalanche photodiodes) and calculate "
        "responsivity and quantum efficiency.",
    ]) +
    "<h3>Optional Outcomes</h3>" + li([
        "Describe guided light in slab waveguides and optical fibres: modes, numerical aperture, attenuation and "
        "dispersion.",
        "Analyse a simple optical link and its power budget.",
        "Explain photovoltaic cells and their efficiency limits.",
        "Describe optical modulators and displays.",
        "Use computer-aided design to model photonic components or photonic integrated circuits.",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>" + li([
        "Nature of light; review of electromagnetic waves; photons.",
        "Optical properties of semiconductors; absorption and emission; rate equations.",
        "Light-emitting diodes.",
        "Semiconductor lasers.",
        "Photodetectors; noise and responsivity.",
    ]) +
    "<h3>Optional Topics</h3>" + li([
        "Optical fibres and waveguides.",
        "Solar cells.",
        "Modulators, optical amplifiers, displays.",
        "Photonic integrated circuits; quantum-well devices and emerging materials.",
    ]) +
    "<h2>Resources &amp; Tools</h2>" + ul([
        "An optoelectronics or photonics textbook, such as Kasap, <em>Optoelectronics and Photonics: Principles and "
        "Practices</em>, or Saleh and Teich, <em>Fundamentals of Photonics</em>; the syllabus names the text used.",
        "MATLAB or Python for device calculations.",
        "Laboratory or demonstration equipment where offered: laser diodes, LEDs, photodiodes, optical power "
        "meters, spectrometers.",
    ]) +
    "<h2>Career Pathways</h2>" + ul([
        "Electrical and electronics engineers (SOC 17-2071, 17-2072) working on optical and sensing systems.",
        "Photonics engineers (O*NET 17-2199.07).",
        "Engineers in optical communications, lidar and imaging, lighting, displays and solar energy.",
        "Florida has a large optics and photonics industry centred on Orlando, around UCF's College of Optics and "
        "Photonics (CREOL), with defence and aerospace employers across Central Florida.",
    ]) +
    "<h2>Where to Learn More</h2>" + ul([
        ext('https://floridapoly.edu/academics/programs/undergraduate/electrical-engineering/',
            "Florida Polytechnic University: B.S. in Electrical Engineering") + " — the programme page, with a link "
        "to Florida Poly's course catalogue.",
        c('EEL5457', 'Advanced Optoelectronics') + " — Florida Poly's graduate course in the same subject.",
        c('EEL3470', 'Electromagnetic Fields') + " — the electromagnetics prerequisite (FAU, Florida Poly, UCF).",
        c('EEL4440') + " — FAMU titles this number <em>Optoelectronics and Optical Systems</em>; UF and UNF teach "
        "optical fibre communications under it.",
        c('ETS3222', 'Optoelectronics and Fiber Optics') + " — FAMU's engineering technology course.",
        c('EEL4458', 'Fundamentals of Photonics') + " — the University of Florida's photonics course.",
        c('ETS2210C', 'Introduction to Photonics') + " — the photonics technician course at Hillsborough College "
        "and Valencia College.",
        ext('https://ece.vt.edu/undergrad/courses/3134', 'Virginia Tech ECE 3134 Introduction to Optoelectronics') +
        SIMILAR + ": photons, spontaneous and stimulated emission, LEDs and lasers, photodetectors and solar cells.",
        ext('https://ece.umd.edu/course-schedule/course/ENEE484', 'University of Maryland ENEE 484 Optoelectronic '
            'Devices') + SIMILAR + ": the physics of lasers, solar cells, LEDs and photodetectors.",
        ext('https://ocw.mit.edu/courses/6-772-compound-semiconductor-devices-spring-2003/',
            'MIT OpenCourseWare 6.772 Compound Semiconductor Devices') + " — free graduate-level notes, including "
        "photodiodes and laser diodes.",
        ext('https://openstax.org/details/books/university-physics-volume-3', 'OpenStax <em>University Physics '
            'Volume 3</em>') + " — a free textbook covering optics, photons and condensed matter physics.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>" + table([
        ['Florida Polytechnic University', 'Optoelectronics', '3',
         'not published (45 by Florida\'s convention)']]) +
    "<p>An elective, so it may not run every year. Ask the department when it is next scheduled before building a "
    "plan around it.</p>"
    "<h3>Transfer and course numbers</h3><p>Optoelectronics is taught in Florida under several numbers and "
    "prefixes (EEL, ETS and, at UCF, OSE), and no other institution carries EEL4448. A receiving programme will "
    "evaluate it from the syllabus.</p>"
)

# =============================================================== EEL5025
G['EEL5025'] = {
    'title': 'Computational Electrical Engineering',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "FSU's catalogue record lists no prerequisite and no special consent; FAMU's catalogue could not be read for "
        "this guide. It is a graduate course in the Department of Electrical and Computer Engineering of the "
        "FAMU-FSU College of Engineering, so graduate standing (or the department's permission) is expected. The "
        "description assumes undergraduate calculus, differential equations, linear algebra, and the core electrical "
        "engineering subjects it applies the methods to: circuits, signals and electromagnetics. Students write their "
        "own code, so working knowledge of a programming language such as MATLAB, Python or C helps. FSU lists it as "
        "typically offered in the fall."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'Two Florida public institutions carry EEL5025, Florida A&M University and Florida State '
                   'University, both at 3 credits; it is one course of their joint FAMU-FSU College of Engineering.',
        'hours_source': 'mixed',
        'derived_contact_hours': 45,
        'derivation': 'FSU publishes 3 contact hours a week (45 over a 15-week term); FAMU publishes none that could '
                      'be read, and 45 is Florida\'s convention for a 3-credit lecture.',
        'offerings': [
            {'institution': 'FAMU', 'institution_name': 'Florida A&M University',
             'title': 'Computational Electrical Engineering', 'credits': 3, 'contact_hours': None,
             'note': 'Statewide record since 2005. FAMU\'s catalogue could not be read.'},
            {'institution': 'FSU', 'institution_name': 'Florida State University',
             'title': 'Computational Electrical Engineering', 'credits': 3, 'contact_hours': 45,
             'note': '3 contact hours a week; typically offered Fall; letter graded; no prerequisite listed.'}],
    },
}
G['EEL5025']['html_content'] = (
    "<h2>Course Description</h2>"
    + box("EEL5025 is taught only at the <em>FAMU-FSU College of Engineering</em>, which Florida A&amp;M University "
          "and Florida State University run together; both universities list the number. FSU publishes a "
          "one-paragraph description and one learning outcome; no syllabus, prerequisites or texts could be read. "
          "This guide sets out what the record shows and what a course of this kind commonly covers. Check the "
          "department's syllabus before relying on it.") +
    "<p><strong>EEL5025 Computational Electrical Engineering</strong> is a 3-credit graduate course in the Department "
    "of Electrical and Computer Engineering of the FAMU-FSU College of Engineering in Tallahassee. FSU's catalogue "
    "describes it this way: <em>This course covers a broad range of computational methods and their applications to "
    "electrical engineering. Methods include solution of equations, matrices, differentiation, integration, solution "
    "of differential equations, Fourier analysis, and boundary-value problems. Applications include circuit analysis, "
    "signal analysis, signal processing, electromagnetics, and optics.</em> Its stated learning outcome is that "
    "students <em>apply mathematical concepts to engineering problems and make abundant use of computational "
    "techniques in which they will be writing the codes.</em> FSU lists it as typically offered in the "
    "<strong>fall</strong>, letter graded, with 3 contact hours a week.</p>"
    "<p>The department's graduate course page lists EEL5025 under <strong>math-equivalent courses (only for M.S. "
    "students)</strong>: an M.S. student must take at least 3 credit hours of advanced mathematics, and EEL5025 is "
    "one of two named courses that satisfy it (the other is EEE 5542 Random Processes), or a department-approved "
    "mathematics course.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>" + li([
        "Solve linear systems and nonlinear equations numerically, and use matrix methods (factorisation, "
        "eigenvalues) on engineering problems.",
        "Compute derivatives and integrals numerically and estimate the error.",
        "Solve ordinary differential equations numerically (initial-value problems), for example the transient "
        "response of a circuit.",
        "Apply <strong>Fourier analysis</strong>, including the discrete Fourier transform and FFT, to signals.",
        "Solve <strong>boundary-value problems</strong> numerically, for example electrostatic potential problems.",
        "<strong>Write their own code</strong> to implement these methods and apply them to circuits, signals, "
        "electromagnetics and optics.",
    ]) +
    "<h3>Optional Outcomes</h3>" + li([
        "Analyse the accuracy, stability and cost of a numerical method.",
        "Apply finite-difference (including finite-difference time-domain) or finite-element methods to "
        "electromagnetic fields.",
        "Use optimisation and least-squares fitting.",
        "Compare their own code with library routines in MATLAB, Python (NumPy and SciPy) or similar.",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>" + li([
        "Floating-point arithmetic and error.",
        "Roots of equations; linear systems; matrix computations.",
        "Numerical differentiation and integration.",
        "Numerical solution of ordinary differential equations.",
        "Fourier series, the discrete Fourier transform and the FFT.",
        "Boundary-value problems.",
        "Applications: circuits, signals and signal processing, electromagnetics, optics.",
    ]) +
    "<h3>Optional Topics</h3>" + li([
        "Interpolation and curve fitting.",
        "Partial differential equations; finite differences, FDTD, finite elements.",
        "Optimisation.",
        "Programming-language choice and performance.",
    ]) +
    "<h2>Resources &amp; Tools</h2>" + ul([
        "A numerical methods text; the syllabus names the one used.",
        "MATLAB, or Python with NumPy, SciPy and Matplotlib; possibly C or Julia.",
        "FSU's research computing resources, where the course uses them.",
    ]) +
    "<h2>Career Pathways</h2>" + ul([
        "Electrical and electronics engineers (SOC 17-2071, 17-2072), especially in simulation, signal processing, "
        "electromagnetics and photonics.",
        "Graduate research in electrical engineering; in Tallahassee, for example, at the National High Magnetic "
        "Field Laboratory.",
        "Software and data roles that rely on numerical computing.",
    ]) +
    "<h2>Where to Learn More</h2>" + ul([
        ext('https://eng.famu.fsu.edu/ece/graduate/courses', 'FAMU-FSU College of Engineering: ECE graduate '
            'courses') + " — the M.S. course requirements, with EEL5025 among the math-equivalent courses.",
        c('EEL6025') + " — the University of South Florida's <em>Math I for Professionals</em>, filed under the same "
        "statewide course title, Computational Electrical Engineering.",
        c('EEL6020', 'Numerical Analysis of Electrical Devices') + " — FIU and USF.",
        c('EGN5455', 'Numerical Methods in Engineering') + " — FAMU and FIU.",
        c('EEL6481', 'Numerical Techniques in Electromagnetics') + " — UCF.",
        path('electrical-engineer', 'Electrical Engineer') + " — the career path.",
        ext('https://www.utep.edu/catalogs/grad/classes/ee5301.htm', 'University of Texas at El Paso EE 5301 '
            'Advanced Mathematics for Engineers II') + SIMILAR + ": numerical methods for electrical engineering, "
        "including boundary-value problems and finite-difference and finite-element methods.",
        ext('https://catalog.csun.edu/ece-309', 'California State University, Northridge ECE 309 Numerical Methods in '
            'Electrical Engineering') + " — an undergraduate course" + SIMILAR + ", using MATLAB.",
        ext('https://www.ocw.mit.edu/courses/18-085-computational-science-and-engineering-i-fall-2008',
            'MIT OpenCourseWare 18.085 Computational Science and Engineering I') + " — free video lectures by "
        "Gilbert Strang: linear algebra, boundary-value problems, Fourier series and the DFT.",
        ext('https://ocw.mit.edu/courses/6-336j-introduction-to-numerical-simulation-sma-5211-fall-2003/',
            'MIT OpenCourseWare 6.336J Introduction to Numerical Simulation') + " — free graduate lecture notes on "
        "sparse solvers, Newton's method and ODE and PDE discretisation.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>" + table([
        ['Florida A&amp;M University', 'Computational Electrical Engineering', '3', 'not published'],
        ['Florida State University', 'Computational Electrical Engineering', '3', '3 a week (45 a term)']]) +
    "<p>The two rows are one course taught at the joint college; a student enrolls through his or her home "
    "university. FSU lists it as typically offered in the fall.</p>"
    "<h3>Transfer</h3><p>Graduate credit transfers at the receiving programme's discretion, not by statewide course "
    "number. A student moving to another Florida graduate programme should bring the syllabus.</p>"
    "<h2>AI Integration (Optional)</h2>"
    "<p>The course asks students to write their own code. AI coding assistants can produce a working FFT or ODE "
    "solver quickly, which is exactly the skill the course is building, so follow the instructor's rules on whether "
    "and how they may be used. Where they are allowed, test generated code against problems with known answers and "
    "check its error behaviour: generated numerical code often runs but is wrong.</p>"
)

# =============================================================== EEL5009
G['EEL5009'] = {
    'title': 'Concepts in Electrical and Computer Engineering',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "Permission of the instructor (FIU's catalogue). Florida International University, the only Florida public "
        "institution with this number, describes it as covering topics required to pursue a master's degree in "
        "electrical and computer engineering, so it is aimed at students starting a master's programme. FIU's M.S. "
        "in Electrical Engineering admits graduates in engineering, the physical sciences, computer science or "
        "mathematics; a student whose bachelor's degree is not in electrical engineering should ask the graduate "
        "adviser whether this course is expected and whether it counts toward the 30 credits of the degree."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries EEL5009: Florida International University, at 3 credits '
                   '(statewide record effective 2015).',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': 'FIU publishes no contact hours; 45 is Florida\'s convention for a 3-credit lecture course.',
        'offerings': [{
            'institution': 'FIU', 'institution_name': 'Florida International University',
            'title': 'Concepts in Electrical and Computer Engineering', 'credits': 3, 'contact_hours': None,
            'note': 'Prerequisite: permission of the instructor. Graded; not repeatable. No term published.'}],
    },
}
G['EEL5009']['html_content'] = (
    "<h2>Course Description</h2>"
    + box("Only <em>Florida International University</em> offers EEL5009 in Florida's public colleges and "
          "universities, and it publishes a one-sentence description that names no topics. This guide sets out what "
          "the record shows and what a course of this kind commonly covers. Check FIU's syllabus before relying on "
          "it.") +
    "<p><strong>EEL5009 Concepts in Electrical and Computer Engineering</strong> is a 3-credit graduate course in "
    "FIU's Department of Electrical and Computer Engineering. FIU's whole description reads: <em>The course covers a "
    "broad range of topics and concepts required to pursuing a Master's Degree in Electrical and Computer "
    "Engineering. Prerequisite: Permission of the instructor.</em> It is graded and may not be repeated for credit. "
    "FIU does not say which topics it covers, when it is offered, or whether it counts toward a degree.</p>"
    "<p>Read at face value, it is a preparatory or bridge course for students entering a master's programme in "
    "electrical or computer engineering: a review of the undergraduate core that graduate courses assume. FIU's "
    "M.S. in Electrical Engineering admits graduates in engineering, the physical sciences, computer science and "
    "mathematics, and a course like this helps students who arrive without parts of that core. Everything below "
    "the required outcomes is a description of what such courses commonly cover, not of FIU's course.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>" + li([
        "Review and apply the core concepts of electrical and computer engineering that master's-level courses "
        "assume.",
        "Identify gaps in their own preparation for graduate study in the field.",
    ]) +
    "<h3>Optional Outcomes</h3>" + li([
        "Analyse DC and AC circuits (Kirchhoff's laws, nodal and mesh analysis, phasors).",
        "Describe continuous- and discrete-time signals and linear time-invariant systems, with the Fourier and "
        "Laplace transforms.",
        "Apply linear algebra, probability and random variables to engineering problems.",
        "Explain the operation of diodes, transistors and operational amplifiers.",
        "Design simple combinational and sequential digital logic, and describe a computer's organisation.",
        "Write programs in a language used in graduate coursework (MATLAB, Python or C).",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>" + li([
        "The foundations a master's programme in electrical and computer engineering assumes (FIU does not publish "
        "which).",
    ]) +
    "<h3>Optional Topics</h3>" + li([
        "Circuit analysis.",
        "Signals and systems; transforms.",
        "Engineering mathematics: linear algebra, differential equations, probability.",
        "Electronics.",
        "Digital logic and computer organisation.",
        "Electromagnetics.",
        "Programming for engineers.",
    ]) +
    "<h2>Career Pathways</h2>" + ul([
        "The course prepares for graduate study; the M.S. in electrical or computer engineering leads to work as "
        "electrical, electronics and computer hardware engineers (SOC 17-2071, 17-2072, 17-2061).",
        "South Florida employers include the region's power utility, telecommunications, health-technology and "
        "aerospace firms.",
    ]) +
    "<h2>Where to Learn More</h2>" + ul([
        ext('https://catalog.fiu.edu/courses/0360811', 'FIU catalogue: EEL5009') + " — FIU's own entry.",
        ext('https://cec.fiu.edu/degrees-programs/graduate/ms-in-electrical-engineering/',
            'FIU: Master\'s in Electrical Engineering') + " — admission and credit requirements (it does not "
        "mention EEL5009).",
        c('EEL3111', 'Circuit Analysis I') + " — the undergraduate circuits course such a review starts from.",
        path('electrical-engineer', 'Electrical Engineer') + " — the career path.",
        ext('https://www.uwb.edu/stem/graduate/certificate-electrical-computer-engineering-foundations',
            'University of Washington Bothell: Graduate Certificate in Electrical &amp; Computer Engineering '
            'Foundations') + " — a similar arrangement, not an equivalent for transfer: six courses (circuits, "
        "digital logic, electronic devices, signals, embedded systems) as a bridge to its M.S.",
        ext('https://www.pdx.edu/electrical-computer-engineering/bridge', 'Portland State University: ECE bridge '
            'programme') + " — a similar arrangement, not an equivalent for transfer, for graduates of other fields.",
        ext('https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/', 'MIT OpenCourseWare 6.002 '
            'Circuits and Electronics') + " and " +
        ext('https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/', '6.003 Signals and Systems') +
        " — free undergraduate core courses with lecture videos, for self-study before or alongside the course.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>" + table([
        ['Florida International University', 'Concepts in Electrical and Computer Engineering', '3',
         'not published (45 by Florida\'s convention)']]) +
    "<p>Entry is by permission of the instructor. FIU publishes no regular term.</p>"
    "<h3>Does it count toward the degree?</h3><p>FIU's M.S. in Electrical Engineering page lists the non-thesis "
    "requirements (engineering mathematics, artificial intelligence, two areas of interest and electives) without "
    "naming EEL5009. Ask the graduate programme in writing whether the credit counts toward the 30 credits or is "
    "taken in addition, because that changes the cost and length of the degree.</p>"
)

# =============================================================== EEL4081
G['EEL4081'] = {
    'title': 'Topics on Rehabilitation Engineering',
    'credits': 3,
    'contact_hours': 60,
    'prerequisites': (
        "EEL 3111 (Circuit Analysis I), per the University of North Florida's 2026-27 catalogue. UNF, the only "
        "Florida public institution with this number, lists it in its Electrical Engineering department. The course "
        "is hands-on design, fabrication and testing of assistive devices, so experience with basic electronics, "
        "microcontroller programming and shop or prototyping tools helps, though UNF does not require them. Despite "
        "the word \"Topics\" in the title, UNF publishes a fixed description, not a variable-content shell. It is new "
        "(statewide record effective August 2026), so check the schedule for when it runs."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries EEL4081: the University of North Florida, at 3 credits '
                   '(statewide record effective 16 August 2026). UNF\'s catalogue lists it as EEL 4081C.',
        'hours_source': 'derived',
        'derived_contact_hours': 60,
        'derivation': 'UNF publishes no contact hours. Its catalogue lists the course as EEL 4081C and calls it '
                      'hands-on, so 60, Florida\'s convention for a 3-credit integrated lecture and laboratory course, '
                      'is used; the statewide record has no C suffix, which would mean 45.',
        'offerings': [{
            'institution': 'UNF', 'institution_name': 'University of North Florida',
            'title': 'Topics on Rehabilitation Engineering', 'credits': 3, 'contact_hours': None,
            'note': 'Listed as EEL 4081C in UNF\'s 2026-27 catalogue. Prerequisite EEL 3111.'}],
    },
}
G['EEL4081']['html_content'] = (
    "<h2>Course Description</h2>"
    + box("Only the <em>University of North Florida</em> offers EEL4081 in Florida's public colleges and "
          "universities. It is a new course (2026), and UNF publishes a one-paragraph description and a "
          "prerequisite. This guide sets out what the record shows and what a course of this kind commonly covers. "
          "Check UNF's syllabus before relying on it.") +
    "<p><strong>EEL4081 Topics on Rehabilitation Engineering</strong> is a 3-credit upper-division course in UNF's "
    "Electrical Engineering department (College of Computing, Engineering, and Construction). UNF's 2026–27 "
    "catalogue lists it as <strong>EEL 4081C</strong>, with prerequisite EEL 3111, and describes it this way: "
    "<em>This course is an introduction to the multiple facets of design, fabrication, and testing of adaptive and "
    "assistive devices for rehabilitation applications. It provides students with the unique opportunity to work at "
    "the interface of people and technology, exposing them to challenging engineering questions that require complex "
    "interdisciplinary solutions. This is a hands-on course where students apply engineering principles to practical "
    "applications focused on design, fabrication and testing of equipment.</em></p>"
    "<p>Rehabilitation engineering applies engineering to help people with disabilities move, communicate, work and "
    "live independently: mobility aids, seating and positioning, adapted controls and switches, communication "
    "devices, prosthetics and orthotics. Despite <em>Topics</em> in its title, UNF describes a fixed course built "
    "around hands-on design projects. UNF has taught rehabilitation engineering before: its faculty have published on "
    "an earlier community-based course in which engineering students and UNF physical therapy students designed "
    "devices for children with disabilities. UNF does not say that EEL4081 continues that course.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>" + li([
        "Describe the range of adaptive and assistive devices used in rehabilitation and the needs they meet.",
        "Apply an engineering <strong>design process</strong> to an assistive device: define the user's need, set "
        "requirements, generate and select concepts.",
        "<strong>Fabricate</strong> a prototype device using appropriate tools and components.",
        "<strong>Test</strong> a device against its requirements and with attention to the user's safety and "
        "comfort.",
        "Work across disciplines, communicating with people outside engineering about technical choices.",
    ]) +
    "<h3>Optional Outcomes</h3>" + li([
        "Work with a client or clinician (for example a physical or occupational therapist) to define a problem.",
        "Integrate sensors, microcontrollers and actuators into an assistive device.",
        "Apply principles of universal design and accessibility.",
        "Discuss the ethics, cost and policy context of assistive technology.",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>" + li([
        "Disability, rehabilitation and the role of the rehabilitation engineer.",
        "Categories of assistive technology: mobility, seating and positioning, access and control, communication, "
        "daily living.",
        "Design process and requirements for devices used by people.",
        "Fabrication and prototyping.",
        "Testing and evaluation of equipment.",
    ]) +
    "<h3>Optional Topics</h3>" + li([
        "Human factors and biomechanics of movement.",
        "Electronics for assistive devices: switches, sensors, microcontrollers, motor control.",
        "Prosthetics and orthotics.",
        "Standards, regulation and funding of assistive technology.",
    ]) +
    "<h2>Resources &amp; Tools</h2>" + ul([
        "A rehabilitation engineering text, such as Cooper, Ohnabe and Hobson, <em>An Introduction to Rehabilitation "
        "Engineering</em>; the syllabus names what is used.",
        "Prototyping tools: 3D printing, hand and shop tools, electronics bench equipment, microcontroller boards.",
        "RESNA (the Rehabilitation Engineering and Assistive Technology Society of North America) and its "
        "professional resources.",
    ]) +
    "<h2>Career Pathways</h2>" + ul([
        "Bioengineers and biomedical engineers (SOC 17-2031), including rehabilitation engineers.",
        "Assistive technology professionals; RESNA offers the Assistive Technology Professional (ATP) and "
        "Rehabilitation Engineering Technologist credentials for practitioners.",
        "Electrical and mechanical engineers in medical-device design.",
        "In Jacksonville, rehabilitation hospitals and clinics, the Mayo Clinic campus and medical-device firms; "
        "statewide, Florida's assistive technology programme and vocational rehabilitation services.",
    ]) +
    "<h2>Where to Learn More</h2>" + ul([
        ext('https://digitalcommons.unf.edu/unf_faculty_publications/2063', 'UNF Digital Commons: Lundy and Aceros, '
            '"A community-based, interdisciplinary rehabilitation engineering course" (IEEE EMBC 2016)') +
        " — an earlier UNF course pairing engineering and physical therapy students.",
        c('BME3891', 'Fundamentals of Rehabilitation Engineering') + " — UCF's and Florida Poly's rehabilitation "
        "engineering course.",
        c('EEL3111', 'Circuit Analysis I') + " — the prerequisite.",
        path('biomedical-engineer', 'Biomedical Engineer') + " — the career path.",
        ext('https://www.torontomu.ca/calendar/2026-2027/courses/biomedical-engineering/BME/705/',
            'Toronto Metropolitan University BME 705 Rehabilitation Engineering') + SIMILAR + ": design and use of "
        "devices for persons with disabilities, with fabrication and design techniques.",
        ext('https://ocw.mit.edu/courses/6-811-principles-and-practice-of-assistive-technology-fall-2014/',
            'MIT OpenCourseWare 6.811 Principles and Practice of Assistive Technology') + " — a free project-based "
        "course in which student teams design for a client with a disability.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>" + table([
        ['University of North Florida', 'Topics on Rehabilitation Engineering (EEL 4081C in UNF\'s catalogue)', '3',
         'not published (60 by Florida\'s convention for a hands-on C course)']]) +
    "<p>The statewide record files the number without the <code>C</code> suffix UNF's catalogue uses. A student "
    "should register under whatever number UNF's schedule shows.</p>"
    "<h3>Transfer</h3><p>No other Florida institution carries the number. UCF and Florida Poly teach the subject as "
    "BME 3891; a receiving programme would compare syllabi.</p>"
)

# =============================================================== EET2525C
G['EET2525C'] = {
    'title': 'Programmable Logic Controllers',
    'credits': 3,
    'contact_hours': 60,
    'prerequisites': (
        "State College of Florida, Manatee-Sarasota, the only Florida public institution with this number, publishes "
        "no prerequisite that could be read for this guide. Introductory PLC courses in Florida's state colleges "
        "commonly expect DC and AC circuits and an introduction to digital logic first, and sometimes a motor "
        "controls course; some admit students with no prerequisite. Check SCF's current catalogue or the "
        "Engineering Technology programme adviser. Note that the statewide course record files EET2525C under the "
        "title Industrial Motor Control Lab, a different subject from SCF's own title; ask SCF which it teaches "
        "before counting on it for transfer."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries EET2525C: State College of Florida, Manatee-Sarasota, at '
                   '3 credits (since 2013; SCF carried the same course as EET2525 in 2012-13).',
        'hours_source': 'derived',
        'derived_contact_hours': 60,
        'derivation': 'SCF publishes no contact hours that could be read; 60 is Florida\'s convention for a 3-credit '
                      'integrated lecture and laboratory (C) course.',
        'offerings': [{
            'institution': 'SCFMS', 'institution_name': 'State College of Florida, Manatee-Sarasota',
            'title': 'Programmable Logic Controllers', 'credits': 3, 'contact_hours': None,
            'note': 'Statewide title: Industrial Motor Control Lab (L). SCF\'s catalogue could not be read.'}],
    },
}
G['EET2525C']['html_content'] = (
    "<h2>Course Description</h2>"
    + box("Only <em>State College of Florida, Manatee-Sarasota</em> offers EET2525C in Florida's public colleges "
          "and universities, and it publishes only a title and credits. The statewide record gives the number a "
          "different title. This guide sets out what the record shows and what a course under each name commonly "
          "covers. Check SCF's syllabus before relying on it.") +
    "<p><strong>EET2525C Programmable Logic Controllers</strong> is a 3-credit lower-division engineering technology "
    "course with an integrated laboratory at State College of Florida, Manatee-Sarasota (SCF), the only Florida "
    "public institution with the number. SCF has carried it since 2013 (as EET2525 for a year before that). SCF's "
    "Engineering Technology A.S. programme page pictures a student working with a programmable logic controller, but "
    "the course description itself could not be read for this guide.</p>"
    "<h3>Two names for one number</h3>"
    "<p>⚠ The statewide course record files EET2525C under the title <strong>Industrial Motor Control Lab</strong>, "
    "not SCF's title. The two subjects are related but not the same:</p>"
    "<ul><li><strong>Programmable logic controllers</strong> (SCF's title): the industrial computers that run "
    "machines and processes, programmed mainly in ladder logic.</li>"
    "<li><strong>Industrial motor control</strong> (the statewide title): starting, stopping, reversing and protecting "
    "electric motors with contactors, motor starters, overloads, pilot devices and relay ladder diagrams.</li></ul>"
    "<p>They meet in the ladder diagram and in motor-control circuits, which PLC courses commonly program. SCF's own "
    "title is the better guide to what it teaches, so this guide treats the course as a PLC course and lists the "
    "motor-control reading separately.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes (programmable logic controllers, SCF's title)</h3>" + li([
        "Describe the parts of a PLC system: processor, power supply, discrete and analogue input and output modules, "
        "programming device, and the scan cycle.",
        "Use number systems and Boolean logic as they apply to PLC addressing and programming.",
        "Write, enter, test and document <strong>ladder logic</strong> programs using contacts, coils, latches, "
        "<strong>timers and counters</strong>.",
        "Wire field devices (push buttons, limit switches, sensors, pilot lights, relays) to PLC inputs and outputs.",
        "Troubleshoot a PLC-controlled system using the program, status indicators and online monitoring.",
        "Follow electrical safety practice, including lockout/tagout, in the laboratory.",
    ]) +
    "<h3>Optional Outcomes</h3>" + li([
        "<em>Motor-control reading (the statewide title):</em> read and wire relay ladder diagrams for motor "
        "starting, stopping, jogging and reversing, with overload protection.",
        "Program a PLC to run a motor-control circuit and compare it with the hard-wired version.",
        "Use comparison, math and data-move instructions, sequencers and analogue I/O.",
        "Build a simple operator interface (HMI) and use industrial networks.",
        "Program in IEC 61131-3 languages other than ladder (function block, structured text).",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics (programmable logic controllers)</h3>" + li([
        "PLC hardware and the scan cycle.",
        "Number systems, logic and addressing.",
        "Ladder logic: contacts, coils, latching and seal-in circuits.",
        "Timers and counters.",
        "Input and output wiring; sensors and field devices.",
        "Troubleshooting and documentation; electrical safety.",
    ]) +
    "<h3>Optional Topics</h3>" + li([
        "<em>Motor-control reading:</em> contactors, motor starters, overloads, pilot devices, control "
        "transformers, start/stop and forward/reverse circuits.",
        "Data handling, sequencers, analogue I/O.",
        "HMIs and industrial communication.",
        "Other IEC 61131-3 languages.",
    ]) +
    "<h2>Resources &amp; Tools</h2>" + ul([
        "A PLC textbook, such as Petruzella, <em>Programmable Logic Controllers</em>; the syllabus names the text.",
        "PLC trainers and programming software from the manufacturer the college uses (for example Allen-Bradley or "
        "Siemens), and simulation software.",
        "Motor-control trainers with contactors, starters and pilot devices.",
        "Digital multimeter and the NFPA 70E electrical safety practices.",
    ]) +
    "<h2>Career Pathways</h2>" + ul([
        "Electrical and electronic engineering technicians (SOC 17-3023) and electro-mechanical and mechatronics "
        "technicians (SOC 17-3024).",
        "Industrial machinery mechanics and maintenance workers (SOC 49-9041, 49-9071).",
        "Electricians (SOC 47-2111) doing industrial controls work.",
        "Manufacturers, water and wastewater utilities, and distribution centres in the Manatee-Sarasota and Tampa Bay "
        "area use PLC-controlled equipment.",
    ]) +
    "<h2>Where to Learn More</h2>" + ul([
        ext('https://www.scf.edu/programs/engineering-technology/', 'State College of Florida: Engineering '
            'Technology A.S.') + " — SCF's engineering technology programme page, with a link to its catalogue.",
        c('ETS1542C', 'Introduction to Programmable Logic Controllers') + " — the most common Florida number for a "
        "first PLC course (nine state colleges).",
        c('ETS2542C', 'Programmable Logic Controllers') + " — six state colleges.",
        c('ETS1542', 'Introduction to Programmable Logic Controllers') + " — the lecture form at five colleges.",
        c('ETS2544C', 'Programmable Logic Controllers II') + " — the second PLC course.",
        path('mechatronics-technician', 'Manufacturing and Mechatronics Technician') + " and " +
        path('industrial-maintenance-technician', 'Industrial Maintenance Technician') + " — career paths that use "
        "PLCs.",
        ext('https://www.montgomery.edu/course/elc-128-introduction-to-programmable-logic-controller',
            'Montgomery Community College (N.C.) ELC-128 Introduction to Programmable Logic Controller') + SIMILAR +
        ": ladder logic, I/O modules and interfacing, 3 credits with 3 lab hours a week.",
        ext('https://www.montgomery.edu/course/elc-117-motors-and-controls', 'Montgomery Community College (N.C.) '
            'ELC-117 Motors and Controls') + SIMILAR + " to the statewide <em>Industrial Motor Control</em> title: "
        "ladder diagrams, pilot devices, contactors and motor starters.",
        ext('https://control.com/textbook/programmable-logic-controllers/', '<em>Lessons in Industrial '
            'Automation</em>: Basics of Programmable Logic Controllers') + " — a free chapter by Tony R. Kuphaldt "
        "(CC BY 4.0) on I/O, addressing and ladder diagram programming.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>" + table([
        ['State College of Florida, Manatee-Sarasota', 'Programmable Logic Controllers', '3',
         'not published (60 by Florida\'s convention for a 3-credit C course)']]) +
    "<h3>Transfer and course numbers</h3><p>Florida's state colleges teach the first PLC course mostly as ETS 1542, "
    "ETS 1542C or ETS 2542C, which share a statewide course and transfer as equivalents. EET2525C is filed under a "
    "<em>different</em> statewide course (Industrial Motor Control Lab), so a receiving college may not match it to "
    "its own PLC course automatically. Keep the syllabus and ask in writing how it will count.</p>"
    "<h2>AI Integration (Optional)</h2>"
    "<p>AI tools can explain ladder logic and suggest programs, but they confuse manufacturers' instruction sets and "
    "addressing, and a program that looks right can run a machine unsafely. Test every program on a trainer or in "
    "simulation, never first on live equipment, and follow the instructor's rules on AI use.</p>"
)

# =============================================================== ETS3543L
G['ETS3543L'] = {
    'title': 'Introduction to Programmable Logic Controllers Lab',
    'credits': 1,
    'contact_hours': 45,
    'prerequisites': (
        "Florida A&M University, the only Florida public institution with this number, places it in the fall of the "
        "fourth year of its B.S. in Electronic Engineering Technology, in the same term as the lecture ETS 3543 "
        "Programmable Logic Controls. FAMU's catalogue could not be read for this guide, so its formal requisites "
        "are unknown; a laboratory of this kind is normally taken together with (or after) its lecture, after "
        "courses in circuits, electronic devices and digital logic. Check FAMU's current catalogue or the "
        "Engineering Technology programme coordinator before registering."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries ETS3543L: Florida A&M University, at 1 credit (statewide '
                   'record effective 2019), the laboratory of its 3-credit ETS 3543.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': 'FAMU publishes no laboratory hours that could be read; a 1-credit engineering laboratory '
                      'commonly meets 2 to 3 hours a week (30 to 45 a term), and 45 is used.',
        'offerings': [{
            'institution': 'FAMU', 'institution_name': 'Florida A&M University',
            'title': 'Introduction to Programmable Logic Controllers Lab', 'credits': 1, 'contact_hours': None,
            'note': 'FAMU programme page title: Programmable Logic Controls Lab. Fall of year 4, B.S. Electronic '
                    'Engineering Technology, with ETS 3543 (3 cr). Statewide title: Programmable Logic '
                    'Controllers (U).'}],
    },
}
G['ETS3543L']['html_content'] = (
    "<h2>Course Description</h2>"
    + box("Only <em>Florida A&amp;M University</em> offers ETS3543L in Florida's public colleges and universities, "
          "and it publishes only a title, credits and the course's place in its degree plan. This guide sets out "
          "what the record shows and what a PLC laboratory commonly covers. Check FAMU's syllabus before relying on "
          "it.") +
    "<p><strong>ETS3543L Introduction to Programmable Logic Controllers Lab</strong> is the 1-credit laboratory of "
    "FAMU's 3-credit lecture <strong>ETS 3543</strong>. FAMU's B.S. in <strong>Electronic Engineering "
    "Technology</strong>, accredited by the Engineering Technology Accreditation Commission of ABET, lists the pair "
    "as <em>Programmable Logic Controls</em> (3) and <em>Programmable Logic Controls Lab</em> (1) in the "
    "<strong>fall of the fourth year</strong>, in both its 124-hour plan and the 120-hour plan for students starting "
    "in fall 2025. FAMU describes the programme's laboratories as including the use of microprocessors and "
    "programmable logic controllers (PLCs). The statewide course is <em>Programmable Logic Controllers (U)</em>.</p>"
    "<p>In a PLC laboratory students wire inputs and outputs, enter and test programs on a real controller, and "
    "troubleshoot small automated systems. FAMU's catalogue could not be read, so what follows is what such a "
    "laboratory commonly covers, not a statement of FAMU's syllabus.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>" + li([
        "Connect discrete input devices (switches, push buttons, sensors) and output devices (lamps, relays, "
        "motor starters) to a PLC safely.",
        "Create, download, run and monitor <strong>ladder logic</strong> programs on a PLC with the manufacturer's "
        "software.",
        "Implement latching circuits, <strong>timers and counters</strong> in working programs.",
        "Test and <strong>troubleshoot</strong> a PLC-controlled system and document the program and wiring.",
        "Record and report laboratory work.",
    ]) +
    "<h3>Optional Outcomes</h3>" + li([
        "Program sequential processes (traffic lights, conveyors, mixing or filling stations) or work with a "
        "simulated process.",
        "Use comparison, math and data-handling instructions.",
        "Read analogue inputs and control analogue outputs.",
        "Build a simple HMI screen or connect the PLC to a network.",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>" + li([
        "Laboratory safety and PLC trainer hardware.",
        "Programming software, addressing and the scan.",
        "Basic ladder logic and latching.",
        "Timers and counters.",
        "Troubleshooting and documentation.",
    ]) +
    "<h3>Optional Topics</h3>" + li([
        "Sequencing and process control projects.",
        "Data handling and analogue I/O.",
        "HMIs and industrial communication.",
    ]) +
    "<h2>Resources &amp; Tools</h2>" + ul([
        "PLC trainers and the manufacturer's programming software (for example Allen-Bradley or Siemens).",
        "The lecture course's textbook; the syllabus names it.",
        "Digital multimeter and wiring tools.",
    ]) +
    "<h2>Career Pathways</h2>" + ul([
        "Electrical and electronic engineering technologists and technicians (SOC 17-3023) and mechatronics "
        "technicians (SOC 17-3024).",
        "Controls and automation roles in manufacturing, utilities and water treatment.",
        "Field service and commissioning for automation equipment.",
    ]) +
    "<h2>Where to Learn More</h2>" + ul([
        ext('https://famu.edu/academics/all-programs/saet/electronic-eng-technology-bs.php',
            'FAMU: Electronic Engineering Technology, B.S.') + " — the programme page with the year-by-year plan.",
        c('ETS3543', 'Introduction to Programmable Logic Controllers') + " — the lecture this laboratory goes with.",
        c('ETS3543C', 'Programmable Logic Applications and Device and Lab') + " — Daytona State's integrated form "
        "of the same statewide course.",
        c('ETS4543C', 'Applied Programmable Logic Controllers') + " — UNF's PLC course.",
        c('ETS2542C', 'Programmable Logic Controllers') + " and " + c('ETS1542C') + " — the state colleges' "
        "first PLC courses.",
        path('electronics-engineering-technician', 'Electronics Engineering Technician') + " — the career path.",
        ext('https://www.uml.edu/catalog/courses/ETEC/3450', 'UMass Lowell ETEC.3450 Programmable Logic Controllers '
            'and Lab I') + SIMILAR + ": PLC programming with laboratory sessions and simulation.",
        ext('https://www.montgomery.edu/course/elc-128-introduction-to-programmable-logic-controller',
            'Montgomery Community College (N.C.) ELC-128 Introduction to Programmable Logic Controller') + SIMILAR +
        ".",
        ext('https://control.com/textbook/programmable-logic-controllers/', '<em>Lessons in Industrial '
            'Automation</em>: Basics of Programmable Logic Controllers') + " — a free chapter (CC BY 4.0).",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>" + table([
        ['Florida A&amp;M University', 'Introduction to Programmable Logic Controllers Lab', '1',
         'not published (30–45 by convention for a 1-credit lab; 45 used)']]) +
    "<p>Taken with ETS 3543 (3 credits) in the fall of the fourth year. The same statewide course is taught as a "
    "3-credit integrated course at Daytona State (ETS 3543C) and UNF (ETS 4543C), and the statewide file also lists "
    "UWF for ETS 3543.</p>"
    "<h3>Transfer</h3><p>A 1-credit laboratory transfers most cleanly together with its lecture. A student moving "
    "to a college that teaches PLCs as one integrated course should present both and the syllabi.</p>"
)

# ----------------------------------------------------------------- write
for cid, g in G.items():
    order = ['title', 'html_content', 'credits', 'contact_hours', 'prerequisites', 'version', 'offering_notes']
    out = {k: g[k] for k in order}
    p = os.path.join('drafts', '%s_guide.json' % cid)
    with io.open(p, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print(cid, 'html', len(out['html_content']), 'prereq', len(out['prerequisites']))
