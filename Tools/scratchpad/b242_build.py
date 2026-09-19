#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Batch 242 -- the eleven BME guides the Biomedical Engineer path owes.

Data-driven for the same reason as batch 240: all eleven sit in ONE landscape
with the same six programmes, so the context blocks are identical and only the
subject changes.

⚠⚠ THE LANDSCAPE, which sets the hedging on every guide here.
Biomedical engineering is awarded at bachelor's level by SIX Florida public
institutions in FIVE cities (UF 115, FIU 79, FSU 36, USF 29, FGCU 21, FAMU 4
-- IPEDS C2023_A, CIP 14.0501), because FSU and FAMU share the joint FAMU-FSU
College of Engineering. ⚠ UCF and FAU award the degree at MASTER'S AND
DOCTORAL LEVEL ONLY. UNF and Florida Polytechnic carry BME courses without
awarding the degree at all, and St Petersburg College is the only Florida
College System institution anywhere in the prefix.

So every course here has ONE TO FIVE carriers, and -- as in ECH -- the count
overstates independence, because a course carried by "FAMU and FSU" is one
programme's course.

⚠⚠⚠ THE PREREQUISITE DATA IS THE WORST MEASURED IN THIS PROJECT, and it is
quantified rather than asserted. Of 100 active undergraduate BME rows, 75
name a course token in DS_Prerequisites1 and FIFTEEN of those 75 -- ONE IN
FIVE -- name a course with ZERO public carriers in Florida. The same test on
CCJ returns about 2%.

Four of the fifteen land on courses in this batch:

    BME3009  -> BSC2012    no carrier; the real sequence is BSC2010/BSC2011
    BME4503  -> EGN3374C   no carrier anywhere in the state
    BME4211  -> BME4100    FAU and FIU only, so it fails at 3 of its 4 carriers
    BME4409  -> "PCB 3XXX Cell and System Physiology"  masked AND unresolvable

⚠ The BME4409 case is the one worth noting methodologically. The batch-234
rule says a masked number followed by a title is usually RECOVERABLE by
searching statewide titles in the named prefix. Run on this one it FAILS --
no PCB title matches "Cell and System Physiology"; the nearest are PCB?203
and PCB?204 Cell Physiology. So the guide says the gate is unusable and names
the nearest real numbers, rather than inventing a resolution.

⚠ RECORDED BUT NOT PUBLISHED: Florida Polytechnic's flat-file title for
BME4503C reads "BIOLOGICAL SCIENCE" where the state and every other carrier
say biomedical instrumentation. One anomalous title in a fixed-width export
is far more likely a data-entry error than a curricular fact, and a
student-facing misfiling warning would not be honest on that evidence.
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

W, WW, WWW = '&#9888;', '&#9888;&#9888;', '&#9888;&#9888;&#9888;'

NAMES = {
    'UF': 'University of Florida', 'USF': 'University of South Florida',
    'FSU': 'Florida State University', 'FAMU': 'Florida A&M University',
    'FIU': 'Florida International University', 'FAU': 'Florida Atlantic University',
    'FGCU': 'Florida Gulf Coast University', 'UNF': 'University of North Florida',
    'FLPOLY': 'Florida Polytechnic University', 'UCF': 'University of Central Florida',
}


def li(*items):
    return LG + ''.join(LI + i + '</li>' for i in items) + '</ul>'


def sec(h2, req, opt):
    out = '<h2>%s</h2><h3>Required %s</h3>' % (h2, h2.split()[-1]) + li(*req)
    if opt:
        out += '<h3>Optional %s</h3>' % h2.split()[-1] + li(*opt)
    return out


LANDSCAPE = (
    '<h3>%s Where this degree exists in Florida, and where it does not</h3>'
    '<p>Biomedical engineering is awarded at bachelor&rsquo;s level by <strong>six Florida public '
    'institutions in five cities</strong>: UF (115 degrees a year), FIU (79), Florida State (36), '
    'USF (29), Florida Gulf Coast (21) and Florida A&amp;M (4). <strong>Florida State and Florida '
    'A&amp;M share the FAMU-FSU College of Engineering</strong>, one joint college in Tallahassee, '
    'which is why their records in this prefix are identical down to the title.</p>'
    '<p>%s <strong>UCF and FAU award biomedical engineering at master&rsquo;s and doctoral level '
    'and no bachelor&rsquo;s at all</strong>, and UNF and Florida Polytechnic carry courses in the '
    'prefix without awarding the degree. <strong>St. Petersburg College is the only Florida '
    'College System institution carrying any <code>BME</code> course.</strong></p>'
    '<p>%s <strong>So a carrier count in this prefix overstates how many independent programmes '
    'exist</strong> — a course carried by &ldquo;FAMU and FSU&rdquo; is one programme&rsquo;s '
    'course. Read anything stated here about content as a description of a small number of '
    'specific curricula rather than a Florida-wide norm. The '
    '<a href="/careers/biomedical-engineer">Biomedical Engineer</a> career path sets out what this '
    'means for choosing where to study.</p>'
) % (WW, WW, W)

PREREQ_WARNING = (
    '<h3>%s Read the prerequisite from YOUR catalogue — in this prefix the state record is '
    'unusually unreliable</h3>'
    '<p>This repository checks every course-looking token in a statewide prerequisite against who '
    'actually carries that course. <strong>The <code>BME</code> prefix returns the worst result '
    'measured anywhere in Florida:</strong> of 100 active undergraduate records, 75 name at least '
    'one course in their prerequisite field, and <strong>fifteen of those 75 — one in five — name '
    'a course that no Florida public institution carries.</strong> The same test on criminal '
    'justice returns about 2%%.</p>'
    '<p>%s <strong>The likeliest cause is age, not carelessness.</strong> Biomedical engineering is '
    'Florida&rsquo;s newest and fastest-growing engineering discipline; its programmes were built '
    'recently and renumbered as they matured, and the statewide record kept the numbers that were '
    'proposed, used briefly or retired along the way. <strong>The practical consequence is simply '
    'that in this prefix you should read the gate from your own institution&rsquo;s catalogue every '
    'time.</strong></p>'
) % (WW, WW)

CAREER_TAIL = (
    '<p>%s <strong>And a word about level, because it applies to every course in this prefix.</strong> '
    'O*NET reports that only <strong>43%% of employers treat a bachelor&rsquo;s as sufficient</strong> '
    'for this occupation, against 26%% naming a master&rsquo;s and 13%% a doctorate — by a wide '
    'margin the highest graduate expectation of any engineering discipline. <strong>Choose your '
    'upper-level courses with that in mind:</strong> the instrumentation, signals and imaging '
    'cluster is the most employable at bachelor&rsquo;s level, while the tissue, neural and BioMEMS '
    'cluster largely assumes you intend to continue.</p>' % WW
)

ABET_FE = (
    '<h3>Accreditation and licensure</h3>'
    '<p>%s <strong>Check that your programme is accredited by ABET&rsquo;s ENGINEERING Accreditation '
    'Commission</strong>, not the engineering technology commission — the difference is two extra '
    'years of experience toward a Professional Engineer licence, and accreditation attaches to a '
    'named programme at a named institution rather than to a course list.</p>'
    '<p>Few biomedical engineers license: device manufacturing falls under the industrial '
    'exemption. %s The exception is <strong>clinical engineering in hospitals and healthcare '
    'facility work</strong>. <strong>Sit the FE examination in your final year regardless</strong> '
    '— it is inexpensive as a student and expensive to recreate later. Under s. 471.013(1)(a), '
    'Florida Statutes, an approved engineering curriculum needs four years of qualifying '
    'experience toward the PE.</p>'
) % (WW, W)

SPEC = []


def add(**kw):
    SPEC.append(kw)


add(
    cid='BME3009', title='Introduction to Biomedical Engineering', credits=3, hours=45,
    carriers=[('FAMU', 'Introduction to Biomedical Engineering', 3, None),
              ('FSU', 'Introduction to Biomedical Engineering', 3, None),
              ('USF', 'Biomedical Engineering', 3, None)],
    prereq=(
        'IGNORE ONE NAME IN THE STATEWIDE PREREQUISITE. It reads "BSC 2012, MAC 2312, PHY 2048C", '
        'and BSC2012 IS CARRIED BY NO FLORIDA PUBLIC INSTITUTION. The real majors biology sequence '
        'is BSC2010 and BSC2011 (or BSC1010 and BSC1011 - Florida uses two numbering families and '
        'no institution carries both), each with a separate laboratory. Calculus II and '
        'calculus-based physics are the other two gates and those are real. '
        'CARRIED BY FAMU, FSU AND USF at 3 credits - and because FAMU and FSU share one joint '
        'college that is TWO independent programmes, not three. '
        'FOUR NUMBERS AND THREE LEVELS FOR THIS COURSE. Florida runs the introduction as BME1008 '
        'or BME1008C (1000 level), BME3009 and BME3060 (3000) and BME4007 (4000), and FAMU and FSU '
        'carry BOTH BME3009 and BME4007. Find out which one your programme means before you '
        'register: the level alone is a two-year difference in where it sits in the degree.'),
    lede=('<strong>Introduction to Biomedical Engineering</strong> is the entry point to the major '
          'and the course that shows a student what the discipline actually contains. The '
          'statewide description covers <strong>cell physiology and modelling, bioinstrumentation, '
          'biomaterials, tissue engineering and bioimaging</strong>, built on prior coursework in '
          'biological science, physics and calculus.',
          '%s <strong>Its real job is a decision, not a survey.</strong> Biomedical engineering '
          'spans electronics, mechanics, materials and cell biology, and almost nobody does all '
          'four. This is where a student finds out which of them they want, and that choice shapes '
          'every elective and, in this discipline more than most, whether they go on to graduate '
          'study.' % WW),
    outcomes=['Describe the <strong>major subdisciplines</strong> of biomedical engineering and '
              'what each does.',
              'Apply <strong>engineering analysis to a physiological system</strong> at an '
              'introductory level.',
              'Describe <strong>cell physiology</strong> in terms a quantitative model can use.',
              'Explain the operating principles of common <strong>biomedical instruments</strong>.',
              'Describe the main classes of <strong>biomaterial</strong> and the biological '
              'response to them.',
              'Explain the <strong>regulatory and ethical framework</strong> that medical devices '
              'and human research operate inside.'],
    opt_outcomes=['Introductory programming or computational modelling in MATLAB or Python.',
                  'Team design exercises.',
                  'Literature searching and technical presentation.',
                  'Careers and graduate-study orientation.'],
    topics=['What biomedical engineering is; the subdisciplines and who employs them.',
            'Cell physiology and introductory modelling.',
            'Bioinstrumentation: sensors, signals, electrical safety.',
            'Biomaterials and the foreign-body response.',
            'Tissue engineering and regenerative medicine.',
            'Medical imaging modalities.',
            'Regulation, ethics and the device lifecycle.'],
    opt_topics=['Introductory MATLAB or Python.', 'Design exercises and teamwork.',
                'Research methods and literature review.'],
    resources=['Enderle &amp; Bronzino, <em>Introduction to Biomedical Engineering</em>, and '
               'Saltzman, <em>Biomedical Engineering: Bridging Medicine and Technology</em>, are '
               'the usual texts.',
               'MATLAB, where the institution introduces it here.',
               '%s The <strong>FDA medical devices</strong> pages and the <strong>Biomedical '
               'Engineering Society</strong> are worth reading early rather than late — the '
               'regulatory material in particular is what distinguishes a graduate in '
               'interviews.' % W],
    career=('Named on the <strong>Biomedical Engineer</strong> career path, where it is the entry '
            'point to the major. ' + CAREER_TAIL),
    extra=(
        '<h3>%s Its statewide prerequisite names a course that does not exist</h3>'
        '<p>The state records the gate as <strong><code>BSC 2012</code>, <code>MAC 2312</code>, '
        '<code>PHY 2048C</code></strong>. Calculus II and calculus-based physics are real and '
        'enforced. <strong><code>BSC2012</code> is carried by no Florida public institution at '
        'all.</strong></p>'
        '<p>The course the state means is the <strong>majors biology sequence</strong>, and '
        'Florida numbers it two ways with no institution in both:</p>'
        '<table class="table table-sm"><tbody>'
        '<tr><td><code>BSC2010</code> / <code>BSC2011</code> (or the <code>C</code> forms)</td>'
        '<td><strong>23 institutions</strong></td></tr>'
        '<tr><td><code>BSC1010</code> / <code>BSC1011</code> (or the <code>C</code> forms)</td>'
        '<td><strong>16 institutions</strong>, including Florida A&amp;M, FAU, FGCU, UNF and '
        'Valencia</td></tr>'
        '</tbody></table>'
        '<p>%s <strong>Register for the laboratories too.</strong> Most carriers split the biology '
        'course into a 3-credit lecture and a separate 1-credit <code>L</code>, and every '
        'biomedical engineering programme requires the laboratory.</p>'
        '<h3>%s Four numbers, three levels, one introductory course</h3>'
        '<table class="table table-sm"><thead><tr><th>Number</th><th>Level</th><th>Carriers</th>'
        '</tr></thead><tbody>'
        '<tr><td><code>BME1008</code></td><td>1000</td><td>University of Florida</td></tr>'
        '<tr><td><code>BME1008C</code></td><td>1000</td><td>FIU, St. Petersburg College</td></tr>'
        '<tr><td><code>BME3009</code></td><td>3000</td><td>FAMU, Florida State, USF</td></tr>'
        '<tr><td><code>BME3060</code></td><td>3000</td><td>UF, USF</td></tr>'
        '<tr><td><code>BME4007</code></td><td>4000</td><td>FAMU, Florida State</td></tr>'
        '</tbody></table>'
        '<p>%s <strong>FAMU and Florida State carry both <code>BME3009</code> and '
        '<code>BME4007</code></strong>, so within one college there are two courses with '
        'introductory titles at different levels. And the level matters more than the title: a '
        '1000-level introduction is a first-year orientation course, while a 3000-level one '
        'assumes biology, calculus and physics and is a genuine engineering course. <strong>Do not '
        'assume a transfer credit for &ldquo;Introduction to Biomedical Engineering&rdquo; will '
        'substitute across that gap.</strong></p>'
        '<h3>%s A route in from a state college</h3>'
        '<p><strong>St. Petersburg College is the only Florida College System institution carrying '
        'any <code>BME</code> course</strong> — <code>BME1008C</code>. That is not a barrier, '
        'because the first two years of this degree are calculus, physics, chemistry, majors '
        'biology and composition, all available everywhere. <strong>Finish those, with the '
        'laboratories, and transfer.</strong> %s Biology is the requirement transfer applicants '
        'most often lack, because it is what distinguishes this degree from every other '
        'engineering major.</p>' % (WWW, W, WW, WW, W, W)),
    summary=('Three Florida public institutions carry BME3009 at 3 credits: FAMU, Florida State '
             '(one joint college) and USF. Florida numbers the introductory course five ways '
             'across three levels. No institution publishes a contact-hour figure.'),
    derivation='Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
)

add(
    cid='BME3100', title='Biomaterials', credits=3, hours=45,
    carriers=[('FAMU', 'Biomaterials', 3, None),
              ('FSU', 'Biomaterials', 3, None),
              ('FLPOLY', 'Biomedical Materials', 3,
               '⚠ Florida Polytechnic carries the course and awards no biomedical engineering '
               'degree.')],
    prereq=(
        'General chemistry and an introductory materials or biomedical engineering course; the '
        'statewide prerequisite field for the biomaterials numbers is blank, which is a gap in the '
        'record rather than an open door. Read your own catalogue. '
        'CARRIED AS BME3100 BY FAMU, FSU AND FLORIDA POLYTECHNIC at 3 credits - and since FAMU and '
        'FSU share one joint college, that is two independent programmes. '
        'THE SAME SUBJECT IS NUMBERED BME4100 AT FAU AND FIU, a thousand higher and titled '
        'Biomaterials Science. Both are upper division so nothing is lost in transfer, but an '
        'audit matching identifiers will not find it, and a student searching for BME3100 at FAU '
        'or FIU will wrongly conclude the course is not offered there.'),
    lede=('<strong>Biomaterials</strong> is the study of what implants and devices are made of, and '
          'of what a living body does to them. The statewide description for the subject covers '
          '<strong>materials used in prostheses for skin and soft tissue, vascular implant '
          'devices, bone repair and artificial joints, and the structure-property relationships of '
          'biological tissue</strong>.',
          '%s <strong>The defining idea of the course is that no material is inert.</strong> '
          'Everything implanted is attacked, encapsulated, corroded or colonised, and most device '
          'failures are biological rather than mechanical. That is why the course spends as much '
          'time on the host response as on the material.' % W),
    outcomes=['Classify <strong>biomaterials</strong> — metals, ceramics, polymers, composites and '
              'materials of biological origin — and relate structure to property.',
              'Explain the <strong>host response</strong> to an implanted material: protein '
              'adsorption, inflammation, the foreign-body reaction, encapsulation.',
              'Assess <strong>biocompatibility</strong> and the testing regime that establishes '
              'it, including ISO 10993.',
              'Analyse <strong>degradation and failure</strong>: corrosion, wear, fatigue, '
              'hydrolysis and the debris they generate.',
              'Describe the <strong>mechanical properties of biological tissue</strong> and the '
              'problem of matching an implant to it.',
              'Select a material for a stated <strong>clinical application</strong> and defend the '
              'choice.'],
    opt_outcomes=['Tissue engineering scaffolds and degradable polymers.',
                  'Drug-delivery materials.',
                  'Surface modification and coatings.',
                  'Laboratory characterisation of materials.'],
    topics=['Classes of biomaterial and their structure-property relationships.',
            'Protein adsorption and the biological response to materials.',
            'Biocompatibility and its assessment; ISO 10993.',
            'Corrosion, wear, fatigue and degradation in vivo.',
            'Mechanical behaviour of hard and soft tissue.',
            'Orthopaedic, cardiovascular, dental and soft-tissue applications.',
            'Sterilisation and its effect on materials.'],
    opt_topics=['Scaffolds and regenerative materials.', 'Drug delivery.',
                'Surface engineering.', 'Nanomaterials in medicine.'],
    resources=['Ratner et al., <em>Biomaterials Science: An Introduction to Materials in '
               'Medicine</em>, is the standard; Temenoff &amp; Mikos is the common alternative.',
               'ISO 10993 (biological evaluation of medical devices) and ASTM F-series standards '
               'govern the testing this course describes.',
               '%s FDA guidance on materials in device submissions is worth reading once — it is '
               'how these decisions actually get defended.' % W],
    career=('Named on the <strong>Biomedical Engineer</strong> career path. Biomaterials leads into '
            'orthopaedic and cardiovascular device work, dental materials, drug delivery and '
            'regenerative medicine, and it is one of the better bridges from this degree into '
            'materials and manufacturing roles outside medicine. ' + CAREER_TAIL),
    extra=(
        '<h3>%s One subject, two numbers a thousand apart</h3>'
        '<table class="table table-sm"><thead><tr><th>Number</th><th>Title</th><th>Carriers</th>'
        '</tr></thead><tbody>'
        '<tr><td><code>BME3100</code></td><td>Biomaterials / Biomedical Materials</td>'
        '<td>FAMU, Florida State, Florida Polytechnic</td></tr>'
        '<tr><td><code>BME4100</code></td><td>Biomaterials Science</td><td>FAU, FIU</td></tr>'
        '</tbody></table>'
        '<p>%s <strong>Both are upper division, so nothing is lost in transfer</strong> — but the '
        'numbers have nothing in common, so an evaluator or degree audit matching identifiers will '
        'not connect them, and a student searching a catalogue for the wrong one concludes the '
        'course is not taught there. <strong>Search by subject.</strong></p>'
        '<p>%s <strong>And the split has a second consequence worth knowing</strong>: '
        '<code>BME4211</code> Biomechanics names <code>BME4100</code> as its statewide '
        'prerequisite, which means that gate does not resolve at the three institutions using '
        '<code>BME3100</code>. See that course&rsquo;s guide.</p>' % (WW, W, WW)),
    summary=('Three Florida public institutions carry BME3100 at 3 credits: FAMU and Florida State '
             '(one joint college) and Florida Polytechnic, which awards no biomedical engineering '
             'degree. FAU and FIU number the same subject BME4100. No institution publishes a '
             'contact-hour figure.'),
    derivation='Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
)

add(
    cid='BME4211', title='Biomechanics', credits=3, hours=45,
    carriers=[('FAMU', 'Biomechanics', 3, None),
              ('FSU', 'Biomechanics', 3, None),
              ('FIU', 'Orthopaedic Biomechanics', 3, None),
              ('UNF', 'Mechanics of the Human Body', 3,
               '⚠ UNF carries the course and awards no biomedical engineering degree.')],
    prereq=(
        'THE STATEWIDE PREREQUISITE DOES NOT RESOLVE AT MOST CARRIERS. It names BME4100 '
        'Biomaterials Science, which is carried by FAU and FIU ONLY - so it fails at FAMU, Florida '
        'State and UNF, three of this course four carriers. Those three number biomaterials '
        'BME3100 instead. '
        'THE REAL GATE is statics and mechanics of materials plus an anatomy or physiology course; '
        'read your own catalogue. '
        'CARRIED BY FAMU, FSU, FIU AND UNF at 3 credits. Since FAMU and FSU share one joint '
        'college, that is three independent programmes - and UNF awards no biomedical engineering '
        'degree, carrying the course as Mechanics of the Human Body for other majors. '
        'CHECK THE SCOPE: FIU titles it Orthopaedic Biomechanics, and the statewide description is '
        'musculoskeletal throughout. If you need cardiovascular or fluid biomechanics, that is a '
        'different course.'),
    lede=('<strong>Biomechanics</strong> applies statics, dynamics and mechanics of materials to '
          'the human body. The statewide description is explicitly musculoskeletal: <strong>the '
          'fundamentals of human musculoskeletal physiology and anatomy, and the computation of '
          'mechanical forces as applied to orthopaedic biomechanics</strong>.',
          '%s <strong>It is the most approachable of the biomedical engineering specialisms for a '
          'student with a mechanical background, and the least approachable for one without.</strong> '
          'Free-body diagrams of a hip joint are still free-body diagrams; what is new is that the '
          'geometry is irregular, the materials are anisotropic and alive, and the loads are '
          'estimated rather than given.' % W),
    outcomes=['Apply <strong>statics and dynamics</strong> to the musculoskeletal system, '
              'including joint reaction and muscle forces.',
              'Describe the <strong>structure and mechanical behaviour of bone</strong>, '
              'cartilage, ligament and tendon.',
              'Analyse <strong>joint mechanics</strong> at the hip, knee, spine and shoulder.',
              'Apply <strong>viscoelasticity</strong> to soft tissue behaviour.',
              'Analyse <strong>gait and human motion</strong>, and interpret motion-capture or '
              'force-plate data.',
              'Evaluate <strong>orthopaedic implants</strong> mechanically, including fixation and '
              'stress shielding.'],
    opt_outcomes=['Finite element analysis of musculoskeletal structures.',
                  'Cardiovascular or fluid biomechanics, where the institution includes it.',
                  'Injury mechanics and tissue failure.',
                  'Laboratory measurement of human movement.'],
    topics=['Review of statics, dynamics and mechanics of materials in a biological context.',
            'Musculoskeletal anatomy for engineers.',
            'Mechanical properties of bone; remodelling.',
            'Soft tissue mechanics and viscoelasticity.',
            'Joint mechanics and free-body analysis of the limbs and spine.',
            'Gait analysis and human motion measurement.',
            'Orthopaedic implants, fixation and stress shielding.'],
    opt_topics=['Finite element modelling.', 'Injury biomechanics.',
                'Cardiovascular biomechanics.', 'Ergonomics and occupational biomechanics.'],
    resources=['Ozkaya, Nordin &amp; Goldsheyder, <em>Fundamentals of Biomechanics</em>; Mow &amp; '
               'Huiskes, <em>Basic Orthopaedic Biomechanics</em>, for the orthopaedic reading.',
               'MATLAB for the analysis; OpenSim is free, widely used for musculoskeletal '
               'modelling, and worth learning independently if the course does not cover it.',
               'Where a motion-capture laboratory is available, expect to use it.'],
    career=('Named on the <strong>Biomedical Engineer</strong> career path. Biomechanics is the '
            'route into orthopaedic and prosthetic device work, rehabilitation engineering, sports '
            'and ergonomics consulting, and injury and forensic analysis. %s It is also the '
            'cluster that reads most clearly to <strong>mechanical</strong> employers, which '
            'matters given how small the biomedical occupation is. ' % W + CAREER_TAIL),
    extra=(
        '<h3>%s Its statewide prerequisite fails at three of its four carriers</h3>'
        '<p>The state records the gate as <strong><code>BME4100</code></strong>, the biomaterials '
        'number used by <strong>FAU and FIU only</strong>. This course is carried by FAMU, Florida '
        'State, FIU and UNF.</p>'
        '<table class="table table-sm"><thead><tr><th>Carrier of this course</th>'
        '<th>Carries <code>BME4100</code>?</th></tr></thead><tbody>'
        '<tr><td>FIU</td><td>yes</td></tr>'
        '<tr><td>FAMU</td><td>%s no — numbers biomaterials <code>BME3100</code></td></tr>'
        '<tr><td>Florida State</td><td>%s no — numbers biomaterials <code>BME3100</code></td></tr>'
        '<tr><td>UNF</td><td>%s no — carries no biomaterials course in this prefix</td></tr>'
        '</tbody></table>'
        '<p>%s <strong>FIU contributed the prerequisite and it describes FIU&rsquo;s curriculum.</strong> '
        'That is a known and common defect shape, not a claim that the other programmes are '
        'under-gated — they gate this course on statics, mechanics of materials and anatomy '
        'instead. <strong>Read the gate from your own catalogue.</strong></p>'
        '<h3>%s UNF teaches it and does not award the degree</h3>'
        '<p>UNF carries this number as <em>Mechanics of the Human Body</em> while awarding no '
        'biomedical engineering degree. %s <strong>That makes it a genuinely useful elective for a '
        'UNF mechanical engineering student</strong> — and it is not the start of a biomedical '
        'engineering degree there. A student intending that degree should read the '
        '<a href="/careers/biomedical-engineer">Biomedical Engineer</a> path before planning around '
        'it.</p>' % (WWW, W, W, W, WW, WW, W)),
    summary=('Four Florida public institutions carry BME4211 at 3 credits: FAMU and Florida State '
             '(one joint college), FIU as Orthopaedic Biomechanics, and UNF as Mechanics of the '
             'Human Body — UNF awarding no biomedical engineering degree. No institution '
             'publishes a contact-hour figure.'),
    derivation='Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
)

add(
    cid='BME4409', title='Quantitative Physiology', credits=3, hours=45,
    carriers=[('UF', 'Quantitative Physiology', 3, None),
              ('USF', 'Engineering Physiology', 3, None)],
    prereq=(
        'THE STATEWIDE PREREQUISITE CANNOT BE LOOKED UP. It reads "PCB 3XXX CELL AND SYSTEM '
        'PHYSIOLOGY, MAP2302". MAP2302 Differential Equations is real and is genuinely required. '
        'The first is a MASKED number, and unlike most masked numbers its title does not match any '
        'Florida course - the nearest real numbers are PCB3203 and PCB3204 Cell Physiology. Read '
        'your own catalogue for the physiology gate. '
        'CARRIED BY UF AND USF ONLY, both at 3 credits; USF titles it Engineering Physiology. Two '
        'carriers means explicit hedging - treat this page as a description of two specific '
        'courses rather than a Florida-wide standard. '
        'THIS COURSE ASSUMES DIFFERENTIAL EQUATIONS FLUENTLY, not just a pass. Physiological '
        'systems are modelled as coupled differential equations from the first weeks.'),
    lede=('<strong>Quantitative Physiology</strong> is physiology rewritten as systems and '
          'equations. The statewide description covers <strong>quantitative modelling of organ '
          'system physiology — the nervous system, the cardiovascular system and the respiratory '
          'system — with students working quantitative problems</strong>.',
          '%s <strong>This is the course that makes an engineer useful in a hospital or a device '
          'company.</strong> A physiologist describes what the heart does; this course asks you to '
          'predict it from a compartment model and a set of boundary conditions, which is what '
          'designing a ventilator, a pacemaker or a dialysis machine actually requires.' % WW),
    outcomes=['Model <strong>cell membrane transport</strong> and the Nernst and '
              'Goldman-Hodgkin-Katz relations.',
              'Derive and analyse the <strong>Hodgkin-Huxley model</strong> of the action '
              'potential and its propagation.',
              'Apply <strong>compartmental modelling</strong> to physiological distribution and '
              'clearance.',
              'Model the <strong>cardiovascular system</strong> — pressure, flow, compliance and '
              'resistance — with lumped-parameter methods.',
              'Model <strong>respiratory mechanics and gas exchange</strong>.',
              'Analyse <strong>feedback and homeostatic control</strong> in physiological systems.',
              'Solve the resulting systems <strong>numerically</strong> and judge whether the '
              'result is physiologically plausible.'],
    opt_outcomes=['Renal and endocrine system modelling.',
                  'Muscle mechanics and models of contraction.',
                  'Pharmacokinetics.',
                  'Model validation against experimental or clinical data.'],
    topics=['Cell membranes, transport and electrochemical potential.',
            'Excitable membranes; the Hodgkin-Huxley model; propagation.',
            'Compartmental models and their solution.',
            'Cardiovascular mechanics and lumped-parameter circulation models.',
            'Respiratory mechanics and gas exchange.',
            'Physiological control systems and feedback.',
            'Numerical solution and model validation.'],
    opt_topics=['Renal and endocrine modelling.', 'Muscle models.',
                'Pharmacokinetics and drug distribution.', 'Sensitivity analysis.'],
    resources=['Keener &amp; Sneyd, <em>Mathematical Physiology</em>, for the rigorous treatment; '
               'Enderle &amp; Bronzino covers it at course level.',
               'A standard physiology text — Guyton &amp; Hall or Boron &amp; Boulpaep — as the '
               'biological reference.',
               'MATLAB or Python throughout; almost nothing here solves analytically.'],
    career=('Named on the <strong>Biomedical Engineer</strong> career path. %s <strong>It is the '
            'single best preparation in the degree for graduate study</strong>, and for the '
            'modelling and simulation work that device companies and clinical research groups '
            'actually hire for. ' % W + CAREER_TAIL),
    extra=(
        '<h3>%s The masked prerequisite, and why this one could not be resolved</h3>'
        '<p>The statewide gate reads <strong>&ldquo;<code>PCB 3XXX</code> Cell and System '
        'Physiology, <code>MAP2302</code>&rdquo;</strong>. A masked number like '
        '<code>3XXX</code> usually <em>can</em> be recovered, because the writer normally follows '
        'it with the course&rsquo;s real title. <strong>Searching every statewide <code>PCB</code> '
        'title for &ldquo;Cell and System Physiology&rdquo; returns nothing.</strong> The closest '
        'real numbers are <code>PCB3203</code> and <code>PCB3204</code>, both titled <em>Cell '
        'Physiology</em>.</p>'
        '<p>%s <strong>So the honest position is that this gate cannot be looked up, and the guide '
        'will not invent a resolution.</strong> Differential equations (<code>MAP2302</code>) is '
        'real and is enforced. For the physiology requirement, <strong>read your own '
        'catalogue</strong>.</p>'
        '<h3>%s Two carriers, two titles, one course</h3>'
        '<p>UF calls it <em>Quantitative Physiology</em> and USF <em>Engineering Physiology</em>. '
        'Same subject, and USF&rsquo;s title is arguably the more descriptive — this is physiology '
        'taught for engineers rather than a mathematics course about the body. <strong>With only '
        'two carriers, plan on sending a syllabus rather than a course number if you '
        'transfer.</strong></p>'
        '<h3>%s Revise differential equations before the term, not during it</h3>'
        '<p>The course uses them from the first weeks and does not teach them. Most students last '
        'met them a year or more earlier. <strong>A few hours on systems of first-order equations, '
        'eigenvalues and numerical solution is the highest-return preparation available for this '
        'course.</strong></p>' % (WWW, WW, W, WW)),
    summary=('Two Florida public institutions carry BME4409, both at 3 credits: UF as Quantitative '
             'Physiology and USF as Engineering Physiology. No institution publishes a '
             'contact-hour figure, and the statewide prerequisite names a masked number that '
             'cannot be resolved.'),
    derivation='Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
)

add(
    cid='BME4503', title='Biomedical Instrumentation', credits=3, hours=45,
    carriers=[('FAMU', 'Bioinstrumentation', 3, None),
              ('FSU', 'Bioinstrumentation', 3, None),
              ('USF', 'Biomedical Instrumentation', 3, None),
              ('FLPOLY', 'Biomedical Devices', 3,
               '⚠ Florida Polytechnic carries the course and awards no biomedical engineering '
               'degree.')],
    prereq=(
        'THE STATEWIDE PREREQUISITE NAMES A COURSE NOBODY CARRIES. It reads "EGN3374C Signals and '
        'Systems for Bioengineers with a minimum grade of C", and EGN3374C IS CARRIED BY NO '
        'FLORIDA PUBLIC INSTITUTION. The real gate is circuits plus a signals and systems course - '
        'at FAMU and FSU that is BME4508 Biosignals and Systems. Read your own catalogue. '
        'CARRIED AS BME4503 BY FAMU, FSU, USF AND FLORIDA POLYTECHNIC at 3 credits. '
        'THE INTEGRATED FORM IS A DIFFERENT NUMBER AND MOSTLY DIFFERENT SCHOOLS: BME4503C is '
        'carried by FAU, FGCU, FIU, UF and Florida Polytechnic at 3 to 4 credits. If your '
        'institution uses the C form you get the laboratory in one registration; if it uses the '
        'bare number, find out where the laboratory lives. '
        'THIS IS THE MOST DIRECTLY EMPLOYABLE COURSE IN THE DEGREE at bachelor level - take it '
        'seriously and keep the laboratory work you can show.',
        ),
    lede=('<strong>Biomedical Instrumentation</strong> is how you measure a living system without '
          'harming it. The statewide description covers <strong>the design and application of '
          'biomedical instruments and devices: biopotential electrodes and amplifiers, '
          'cardiovascular and respiratory measurements, clinical laboratory instruments, '
          'therapeutic and diagnostic devices, medical imaging systems and electrical '
          'safety</strong>.',
          '%s <strong>Electrical safety is not a footnote here; it is a central topic and it is '
          'the reason this course exists in the form it does.</strong> An instrument connected to a '
          'patient is a conductive path to the heart, and leakage currents that are harmless at the '
          'skin are lethal at a catheter tip. Students are frequently surprised how much of the '
          'course is about not killing anyone.' % WW),
    outcomes=['Analyse <strong>biopotential electrodes</strong> — the half-cell potential, the '
              'electrode-electrolyte interface, motion artefact.',
              'Design and analyse <strong>biopotential amplifiers</strong>, including instrumentation '
              'amplifiers, common-mode rejection and isolation.',
              'Apply <strong>filtering and noise reduction</strong> to physiological signals.',
              'Describe the measurement of <strong>cardiovascular and respiratory</strong> '
              'variables: ECG, blood pressure, flow, spirometry, pulse oximetry.',
              'Describe <strong>clinical laboratory and diagnostic instruments</strong>.',
              'Apply <strong>electrical safety</strong> principles, including leakage current '
              'limits, isolation and the distinction between macroshock and microshock.',
              'Specify a <strong>sensor and signal chain</strong> for a stated clinical '
              'measurement.'],
    opt_outcomes=['Therapeutic devices: pacemakers, defibrillators, stimulators.',
                  'Microcontroller or data-acquisition implementation of a measurement.',
                  'Medical device standards — IEC 60601 and the safety framework.',
                  'Laboratory construction and testing of an instrument.'],
    topics=['Origins of biopotentials; electrodes and the electrode interface.',
            'Instrumentation amplifiers, common-mode rejection, isolation.',
            'Noise, interference and filtering in physiological measurement.',
            'ECG, EEG and EMG measurement.',
            'Blood pressure, flow, respiration and pulse oximetry.',
            'Clinical laboratory and diagnostic instruments.',
            'Electrical safety; leakage currents, macroshock and microshock.',
            'Therapeutic and imaging devices in outline.'],
    opt_topics=['Pacemakers and defibrillators.', 'Embedded implementation and data acquisition.',
                'IEC 60601 and regulatory testing.', 'Wearable and ambulatory monitoring.'],
    resources=['Webster, <em>Medical Instrumentation: Application and Design</em>, is the standard '
               'and has been for decades; Enderle &amp; Bronzino covers it at course level.',
               'LabVIEW, MATLAB or a microcontroller platform for the laboratory work.',
               '%s <strong>IEC 60601</strong> is the medical electrical equipment safety standard '
               'the whole industry works to, and being able to name it is a small thing that reads '
               'well in an interview.' % W],
    career=('Named on the <strong>Biomedical Engineer</strong> career path, and %s <strong>it is '
            'the single most employable course in the degree at bachelor&rsquo;s level.</strong> '
            'It leads into medical device design and test, clinical engineering in hospitals, '
            'field service engineering, and quality and regulatory work — and because the skills '
            'are ordinary electronics applied to an unusual domain, it also reads to electronics '
            'and instrumentation employers outside medicine. ' % WW + CAREER_TAIL),
    extra=(
        '<h3>%s Its statewide prerequisite names a course that exists nowhere</h3>'
        '<p>The state records the gate as <strong><code>EGN3374C</code> Signals and Systems for '
        'Bioengineers, minimum grade C</strong>. <strong>No Florida public institution carries '
        '<code>EGN3374C</code>.</strong> Not a different institution — none.</p>'
        '<p>%s <strong>The real gate is circuits plus signals and systems</strong>, and where your '
        'institution teaches those varies: at FAMU and Florida State the signals course is '
        '<code>BME4508</code> <em>Biosignals and Systems</em>; elsewhere it is an electrical '
        'engineering number. <strong>Read the gate from your own catalogue.</strong></p>'
        '<h3>%s Two numbers for the two packagings, and mostly different schools</h3>'
        '<table class="table table-sm"><thead><tr><th>Number</th><th>What it is</th>'
        '<th>Carriers</th></tr></thead><tbody>'
        '<tr><td><code>BME4503</code></td><td>lecture, 3 credits</td>'
        '<td>FAMU, Florida State, USF, Florida Polytechnic</td></tr>'
        '<tr><td><code>BME4503C</code></td><td>integrated lecture and laboratory, 3–4 credits</td>'
        '<td>FAU, FGCU, FIU, UF, Florida Polytechnic</td></tr>'
        '</tbody></table>'
        '<p>%s <strong>Both identifiers are real and the two carrier lists barely overlap.</strong> '
        'This is one course filed two ways, and the consequence falls on transfer: an evaluator '
        'matching identifiers reads <code>BME4503C</code> against a <code>BME4503</code> '
        'requirement as a mismatch when it is the same course. <strong>Say so explicitly and send '
        'the syllabus.</strong></p>'
        '<p>%s <strong>And whichever form your institution uses, make sure you end up doing the '
        'laboratory.</strong> The hands-on work is what an interviewer asks about, and on the bare '
        'number it is a separate arrangement you have to find.</p>' % (WWW, WW, WW, WW, W)),
    summary=('Four Florida public institutions carry BME4503 at 3 credits: FAMU and Florida State '
             '(one joint college), USF, and Florida Polytechnic, which awards no biomedical '
             'engineering degree. FAU, FGCU, FIU, UF and Florida Polytechnic carry the integrated '
             'BME4503C instead. No institution publishes a contact-hour figure.'),
    derivation=('Florida convention of 15 contact hours per credit at the 3-credit lecture value. '
                '⚠ The integrated BME4503C form runs at 3 to 4 credits and correspondingly '
                'more contact hours.'),
)

add(
    cid='BME4508', title='Biosignals and Systems', credits=3, hours=45,
    carriers=[('FAMU', 'Biosignals and Systems', 3, None),
              ('FSU', 'Biosignals & Systems', 3, None),
              ('USF', 'Biomedical Signals and Systems Analysis', 3, None)],
    prereq=(
        'Differential equations and circuits; Laplace and Fourier transforms are assumed from the '
        'first weeks and are the thing to revise beforehand. Read your own catalogue for the exact '
        'gate - the statewide prerequisite data in this prefix is unusually unreliable. '
        'CARRIED BY FAMU, FSU AND USF at 3 credits, which is TWO independent programmes because '
        'FAMU and FSU share one joint college. '
        'WHERE YOUR PROGRAMME DOES NOT CARRY IT, THE MATERIAL IS STILL REQUIRED - it normally sits '
        'in the electrical engineering signals and systems course. Ask, because the instrumentation '
        'and imaging sequence assumes it.'),
    lede=('<strong>Biosignals and Systems</strong> is signal processing taught on the signals the '
          'body actually produces — the ECG, EEG, EMG and the rest — which are weak, noisy, '
          'non-stationary and mixed with interference from everything nearby.',
          '%s <strong>It is the most mathematical course in the instrumentation sequence and the '
          'one that most resembles electrical engineering.</strong> Students who enjoy it tend to '
          'end up in signal processing, imaging or device firmware; students who do not should '
          'still take it seriously, because everything downstream assumes it.' % W),
    outcomes=['Classify signals and systems, and apply <strong>linearity and time '
              'invariance</strong>.',
              'Apply <strong>convolution</strong> and the impulse response.',
              'Apply the <strong>Fourier series and transform</strong>, and interpret a spectrum of '
              'a physiological signal.',
              'Apply the <strong>Laplace transform</strong> and transfer functions to system '
              'analysis.',
              'Apply <strong>sampling</strong> and the Nyquist criterion, and recognise aliasing in '
              'real data.',
              'Design and apply <strong>digital filters</strong> to remove baseline wander, mains '
              'interference and motion artefact.',
              'Characterise the principal <strong>biosignals</strong> — ECG, EEG, EMG — and their '
              'frequency content.'],
    opt_outcomes=['The z-transform and discrete-time system analysis.',
                  'Time-frequency and wavelet analysis of non-stationary signals.',
                  'Feature extraction and classification of physiological signals.',
                  'Laboratory acquisition and processing of real signals.'],
    topics=['Signals, systems, linearity and time invariance.',
            'Convolution and impulse response.',
            'Fourier series, Fourier transform and spectral analysis.',
            'Laplace transforms and transfer functions.',
            'Sampling, quantisation and aliasing.',
            'Digital filter design; FIR and IIR.',
            'Characteristics of the ECG, EEG and EMG.',
            'Noise, artefact and interference removal.'],
    opt_topics=['The z-transform.', 'Wavelets and time-frequency methods.',
                'Feature extraction and pattern classification.',
                'Introduction to machine learning on physiological data.'],
    resources=['Oppenheim &amp; Willsky, <em>Signals and Systems</em>, for the theory; Semmlow, '
               '<em>Signals and Systems for Bioengineers</em>, and Rangayyan, <em>Biomedical '
               'Signal Analysis</em>, for the biomedical application.',
               'MATLAB with the Signal Processing Toolbox, or Python with SciPy.',
               '%s <strong>PhysioNet</strong> publishes large archives of real, annotated '
               'physiological recordings, free — the best practice material available, and '
               'working with it independently is a genuinely distinguishing thing to have '
               'done.' % W],
    career=('Named on the <strong>Biomedical Engineer</strong> career path. It leads into medical '
            'device firmware and algorithms, imaging, neurotechnology, and physiological monitoring '
            '— and %s <strong>it is the course in this degree that transfers most readily into '
            'data and software roles</strong>, which matters given how small the biomedical '
            'occupation is. ' % W + CAREER_TAIL),
    extra=(
        '<h3>%s If your programme does not carry this number, you still have to do the material</h3>'
        '<p>Only FAMU, Florida State and USF carry <code>BME4508</code>. The other programmes '
        'require the same content through their electrical engineering signals and systems course, '
        'and the biomedical instrumentation and imaging courses assume it either way.</p>'
        '<p>%s <strong>The statewide record makes this confusing rather than clear.</strong> '
        '<code>BME4503</code> Biomedical Instrumentation names a prerequisite called '
        '&ldquo;Signals and Systems for Bioengineers&rdquo; under the number '
        '<code>EGN3374C</code> — <strong>which no Florida public institution carries.</strong> '
        'So the state describes a signals prerequisite that cannot be found, while the real one '
        'sits under a number that varies by campus. <strong>Ask your adviser which course fills '
        'this slot in your degree; do not go looking for the number.</strong></p>'
        '<h3>%s Revise the transforms before the term starts</h3>'
        '<p>Laplace and Fourier transforms are used from the first weeks and are not taught here. '
        'Most students last met them in differential equations. <strong>A few hours on transforms, '
        'partial fractions and inversion is the highest-return preparation available for this '
        'course</strong>, and it pays again in instrumentation and imaging.</p>' % (WW, WWW, WW)),
    summary=('Three Florida public institutions carry BME4508 at 3 credits: FAMU and Florida State '
             '(one joint college) and USF. The other programmes cover the same material through '
             'their electrical engineering signals course. No institution publishes a contact-hour '
             'figure.'),
    derivation='Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
)

add(
    cid='BME4531', title='Medical Imaging', credits=3, hours=45,
    carriers=[('FAMU', 'Medical Imaging', 3, None),
              ('FSU', 'Medical Imaging', 3, None),
              ('FIU', 'Medical Imaging', 3, None),
              ('UF', 'Medical Imaging', 3, None),
              ('USF', 'Introduction to Medical Imaging', 3, None)],
    prereq=(
        'Signals and systems, and physics through electricity and magnetism; linear algebra and '
        'Fourier analysis are used throughout. The statewide prerequisite reads "PERMISSION OF THE '
        'INSTRUCTOR", which names no course - read your own catalogue for the real gate. '
        'THE MOST WIDELY CARRIED BIOMEDICAL ENGINEERING COURSE IN FLORIDA: five carriers - FAMU, '
        'FSU, FIU, UF and USF - all at 3 credits, and four of the five using the identical title. '
        'That is unusually clean agreement for this prefix. '
        'FAMU AND FSU ALSO CARRY A 1-CREDIT LABORATORY, BME4531L. The other three do not, so check '
        'whether a separate registration is expected.'),
    lede=('<strong>Medical Imaging</strong> is how the inside of a living body is turned into a '
          'picture. The statewide description covers <strong>the fundamentals of the major imaging '
          'modalities: X-ray radiology, X-ray computed tomography, ultrasonography, magnetic '
          'resonance imaging, nuclear imaging (PET and SPECT) and optical imaging</strong>.',
          '%s <strong>It is the most widely carried course in the prefix and the one with the '
          'clearest agreement across Florida</strong> — five institutions, the same three credits, '
          'four of them using the same title. In a prefix where almost nothing else lines up, that '
          'is worth knowing: this is the <code>BME</code> course most likely to transfer without '
          'argument.',
          '%s The course is also a genuine physics and mathematics course. Reconstruction is the '
          'inverse Radon transform, MRI is Fourier space made physical, and the reason images look '
          'the way they do is always a trade between resolution, noise, dose and time.' % W),
    outcomes=['Explain the <strong>physical basis</strong> of each major modality and what tissue '
              'property it measures.',
              'Analyse <strong>X-ray production, attenuation and detection</strong>, and the '
              'formation of a projection radiograph.',
              'Explain <strong>computed tomography</strong> and image reconstruction from '
              'projections.',
              'Explain <strong>ultrasound</strong>: propagation, reflection, transducers, and '
              'Doppler measurement.',
              'Explain <strong>magnetic resonance imaging</strong> — spin, relaxation, k-space, and '
              'the origin of contrast.',
              'Explain <strong>nuclear imaging</strong>, PET and SPECT, and radiotracer principles.',
              'Analyse <strong>image quality</strong>: resolution, contrast, signal-to-noise, '
              'artefacts, and the dose trade-off.'],
    opt_outcomes=['Image processing and reconstruction implemented in software.',
                  'Optical and molecular imaging.',
                  'Radiation safety and dosimetry in depth.',
                  'Clinical case interpretation alongside the physics.'],
    topics=['Imaging system fundamentals; resolution, contrast and noise.',
            'X-ray production, interaction with tissue, and detection.',
            'Computed tomography and reconstruction from projections.',
            'Ultrasound physics, transducers and Doppler.',
            'Magnetic resonance: spin physics, pulse sequences, k-space.',
            'Nuclear medicine: PET, SPECT, radiotracers.',
            'Optical imaging.',
            'Image quality, artefacts, dose and safety.'],
    opt_topics=['Reconstruction algorithms in code.', 'Molecular and functional imaging.',
                'Image registration and segmentation.', 'Radiation protection.'],
    resources=['Prince &amp; Links, <em>Medical Imaging Signals and Systems</em>, is the standard; '
               'Bushberg et al., <em>The Essential Physics of Medical Imaging</em>, is the '
               'reference the clinical world uses.',
               'MATLAB or Python for reconstruction exercises.',
               '%s Public DICOM datasets and open reconstruction toolkits make it easy to work '
               'with real images independently, which is worth doing — handling real DICOM data '
               'is a practical skill employers recognise.' % W],
    career=('Named on the <strong>Biomedical Engineer</strong> career path. Imaging leads into the '
            'imaging manufacturers, clinical and hospital physics, image-analysis and AI roles in '
            'radiology, and research. %s <strong>It is also one of the strongest routes into '
            'graduate study</strong>, and medical physics is an adjacent profession worth knowing '
            'about — it requires a graduate degree from an accredited programme and a residency, '
            'and it pays well. ' % W + CAREER_TAIL),
    extra=(
        '<h3>Unusually clean agreement — and it is worth saying so</h3>'
        '<p>Five carriers, all at <strong>3 credits</strong>, and four using the identical title '
        '<em>Medical Imaging</em>; USF adds &ldquo;Introduction to&rdquo;. %s <strong>In a prefix '
        'where the introductory course has four numbers across three levels and one prerequisite '
        'in five points at a course nobody carries, this is the number that behaves.</strong> If '
        'you are transferring, this is the one least likely to cause an argument.</p>'
        '<h3>%s Check whether a separate laboratory is expected</h3>'
        '<p><strong>FAMU and Florida State carry a 1-credit <code>BME4531L</code> Medical Imaging '
        'Laboratory; FIU, UF and USF do not.</strong> Where it exists it is usually a corequisite, '
        'so register for both — and where it does not, the laboratory content is generally folded '
        'into the lecture course rather than omitted.</p>'
        '<h3>&ldquo;Permission of the instructor&rdquo; is not a prerequisite</h3>'
        '<p>The statewide prerequisite field for this number reads exactly that, which names no '
        'course and tells a planning student nothing. %s In practice programmes gate it on signals '
        'and systems and on physics through electricity and magnetism. <strong>Read your own '
        'catalogue.</strong> It is a mild example of a problem this prefix has badly — see any '
        'other <code>BME</code> guide for the measured version.</p>' % (WW, WW, W)),
    summary=('Five Florida public institutions carry BME4531, all at 3 credits: FAMU, FIU, Florida '
             'State, UF and USF — the most widely carried biomedical engineering course in the '
             'state. FAMU and Florida State add a 1-credit laboratory, BME4531L. No institution '
             'publishes a contact-hour figure.'),
    derivation='Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
)

add(
    cid='BME4332', title='Cell and Tissue Engineering', credits=3, hours=45,
    carriers=[('FAMU', 'Cell and Tissue Engineering', 3, None),
              ('FSU', 'Cell and Tissue Engineering', 3, None),
              ('FIU', 'Cell and Tissue Engineering', 3, None),
              ('FAU', 'Tissue Engineering: Basic Concepts', 3, None)],
    prereq=(
        'Cell biology or majors biology, biomaterials, and normally transport phenomena; read your '
        'own catalogue, because the statewide prerequisite data in this prefix is unusually '
        'unreliable. '
        'CARRIED BY FAMU, FSU, FIU AND FAU at 3 credits - three independent programmes, since FAMU '
        'and FSU share one joint college. FAU titles it Tissue Engineering: Basic Concepts. '
        'FAMU AND FSU CARRY A MATCHING 1-CREDIT LABORATORY, BME4332L; FIU and FAU do not. Check '
        'whether a second registration is expected. '
        'A NOTE ON LEVEL, AND IT IS NOT A CRITICISM OF THE COURSE: this is the part of biomedical '
        'engineering that most assumes graduate study. O*NET reports only 43% of employers in this '
        'occupation treat a bachelor degree as sufficient. Take it because you intend to continue, '
        'not instead of the instrumentation and signals cluster.'),
    lede=('<strong>Cell and Tissue Engineering</strong> is the attempt to build living replacement '
          'tissue — cells, scaffolds and the signals that persuade them to organise into something '
          'that works. It is the research frontier of the discipline and the part of it that '
          'appears in the news.',
          '%s <strong>It is also the part where the honest picture is furthest from the '
          'headlines.</strong> A handful of engineered tissues are in clinical use; most of the '
          'field is laboratory research, and the course should be taken with that in mind. That is '
          'a reason to plan on graduate study if this is what interests you, not a reason to avoid '
          'it.' % WW),
    outcomes=['Describe <strong>cell sources</strong> — primary, stem and induced pluripotent '
              'cells — and the trade-offs between them.',
              'Apply the principles of <strong>cell culture</strong> and describe the conditions '
              'cells require.',
              'Analyse <strong>scaffold design</strong>: materials, porosity, degradation rate, '
              'mechanical match.',
              'Explain the role of <strong>growth factors and signalling</strong> in '
              'differentiation and tissue formation.',
              'Analyse <strong>mass transport</strong> in engineered tissue, and explain why '
              'vascularisation is the central unsolved problem.',
              'Describe <strong>bioreactor design</strong> and the role of mechanical stimulation.',
              'Discuss the <strong>regulatory and ethical framework</strong> for cell-based '
              'therapies.'],
    opt_outcomes=['Bioprinting and additive manufacturing of tissue.',
                  'Organ-on-a-chip and microphysiological systems.',
                  'Specific tissue targets — skin, cartilage, bone, vasculature, neural.',
                  'Laboratory cell culture technique.'],
    topics=['Cell sources, stem cells and cell expansion.',
            'Cell culture principles and practice.',
            'Scaffold materials, fabrication and degradation.',
            'Cell-matrix and cell-cell interactions; growth factors.',
            'Mass transport limits and vascularisation.',
            'Bioreactors and mechanical conditioning.',
            'Immune response to engineered tissue.',
            'Regulation, ethics and translation to the clinic.'],
    opt_topics=['Bioprinting.', 'Organ-on-a-chip systems.',
                'Gene delivery and gene-modified cells.', 'Specific tissue case studies.'],
    resources=['Lanza, Langer &amp; Vacanti, <em>Principles of Tissue Engineering</em>, is the '
               'reference; Saltzman, <em>Tissue Engineering</em>, is a course-level text.',
               'The primary literature is unusually important here, because the field moves fast '
               'and textbooks lag it.',
               '%s FDA guidance on regenerative medicine advanced therapies is worth reading — it '
               'is where the gap between what is possible and what is approved becomes '
               'concrete.' % W],
    career=('Named on the <strong>Biomedical Engineer</strong> career path. It leads into '
            'regenerative medicine and cell-therapy companies, pharmaceutical and biotechnology '
            'research, and academic research — and it is the most common reason biomedical '
            'engineering graduates go on to a doctorate. ' + CAREER_TAIL),
    extra=(
        '<h3>%s Check whether the laboratory is a separate registration</h3>'
        '<p><strong>FAMU and Florida State carry a 1-credit <code>BME4332L</code> Cell and Tissue '
        'Engineering Laboratory; FIU and FAU do not.</strong> Where it exists it is normally a '
        'corequisite, so register for both — and the laboratory is the valuable half here, because '
        'aseptic technique and cell culture are hands-on skills that cannot be learned from a '
        'lecture and that employers and graduate supervisors both look for.</p>'
        '<h3>Same course, one different title</h3>'
        '<p>FAMU, Florida State and FIU use the statewide title; FAU calls it <em>Tissue '
        'Engineering: Basic Concepts</em>. %s Branding rather than divergence — but FAU&rsquo;s '
        '&ldquo;basic concepts&rdquo; is a fair signal that its version is a survey, so if you are '
        'choosing electives for graduate preparation, ask how much laboratory work is '
        'involved.</p>' % (WW, W)),
    summary=('Four Florida public institutions carry BME4332 at 3 credits: FAMU and Florida State '
             '(one joint college), FIU, and FAU as Tissue Engineering: Basic Concepts. FAMU and '
             'Florida State add a 1-credit laboratory, BME4332L. No institution publishes a '
             'contact-hour figure.'),
    derivation='Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
)

add(
    cid='BME4361', title='Neural Engineering', credits=3, hours=45,
    carriers=[('FAMU', 'Neural Engineering', 3, None),
              ('FSU', 'Neural Engineering', 3, None),
              ('FAU', 'Neural Engineering', 3, None),
              ('UF', 'Neural Engineering', 3, None)],
    prereq=(
        'Signals and systems, and a physiology or neuroscience course; differential equations '
        'throughout. Read your own catalogue for the exact gate - the statewide prerequisite data '
        'in this prefix is unusually unreliable. '
        'CARRIED BY FAMU, FSU, FAU AND UF at 3 credits, ALL FOUR under the identical title - rare '
        'agreement in this prefix. Because FAMU and FSU share one joint college, that is three '
        'independent programmes. '
        'A NOTE ON LEVEL: this is one of the courses that most assumes graduate study. O*NET '
        'reports 26% of employers in this occupation naming a master degree and 13% a doctorate. '
        'Take it because it interests you and you intend to continue, alongside rather than instead '
        'of the instrumentation and signals cluster.'),
    lede=('<strong>Neural Engineering</strong> is the engineering of interfaces with the nervous '
          'system — recording from neurons, stimulating them, and building devices that do '
          'something useful with the result. Cochlear implants, deep brain stimulation, '
          'neuroprosthetics and brain-computer interfaces all sit here.',
          '%s <strong>It is one of the few areas where the discipline delivers what the public '
          'imagines it does.</strong> Cochlear implants and deep brain stimulators are in routine '
          'clinical use and have changed lives at scale, which makes this a course where the '
          'engineering and the motivation are unusually easy to connect.' % W),
    outcomes=['Describe the <strong>electrophysiology of neurons</strong> — membrane potential, '
              'action potentials, propagation and synaptic transmission.',
              'Model excitable membranes, including the <strong>Hodgkin-Huxley</strong> and '
              'cable models.',
              'Analyse <strong>neural recording</strong>: electrode types, signal amplitude and '
              'bandwidth, noise, and spike sorting.',
              'Analyse <strong>neural stimulation</strong>: charge balance, safe charge density, '
              'electrode-tissue damage limits.',
              'Describe the design and operation of <strong>clinical neural devices</strong> — '
              'cochlear implants, deep brain stimulators, functional electrical stimulation.',
              'Describe <strong>brain-computer interface</strong> architectures and decoding.',
              'Discuss the <strong>biocompatibility and chronic stability</strong> problem for '
              'implanted neural electrodes.'],
    opt_outcomes=['Neural signal decoding and machine learning.',
                  'Optogenetics and emerging stimulation methods.',
                  'Neural prosthetics for sensory or motor restoration.',
                  'Neuroethics.'],
    topics=['Neuroanatomy and neurophysiology for engineers.',
            'Membrane biophysics; Hodgkin-Huxley and cable theory.',
            'Electrodes and the neural interface.',
            'Recording: amplification, noise, spike detection and sorting.',
            'Stimulation: waveforms, charge balance, safety limits.',
            'Clinical neural devices and their design constraints.',
            'Brain-computer interfaces and decoding.',
            'Chronic implant failure and the foreign-body response in neural tissue.'],
    opt_topics=['Optogenetics.', 'Machine learning for neural decoding.',
                'Sensory prosthetics.', 'Neuroethics and the regulation of neural devices.'],
    resources=['Durand and the <em>Journal of Neural Engineering</em> are the field&rsquo;s '
               'reference points; Dayan &amp; Abbott, <em>Theoretical Neuroscience</em>, for the '
               'modelling.',
               'MATLAB or Python for the modelling and decoding work; NEURON for compartmental '
               'simulation where the course uses it.',
               '%s Open neural datasets are plentiful and free, and working with one independently '
               'is among the most distinguishing things an undergraduate in this area can '
               'do.' % W],
    career=('Named on the <strong>Biomedical Engineer</strong> career path. It leads into the '
            'neuromodulation industry — a substantial and growing device sector — and into '
            'neuroscience and neuroengineering research. %s It is also one of the most '
            'graduate-school-oriented courses in the degree, and the research groups that hire in '
            'this area recruit heavily from students who have done undergraduate research. ' % W
            + CAREER_TAIL),
    extra=(
        '<h3>Four carriers, one title, no divergence</h3>'
        '<p>FAMU, Florida State, FAU and UF all carry this number at 3 credits under the identical '
        'title <em>Neural Engineering</em>. %s <strong>That is rare agreement in a prefix where '
        'almost nothing else lines up</strong>, and it makes this course unusually safe to plan '
        'around and to transfer.</p>'
        '<h3>%s Charge balance is the part to take seriously</h3>'
        '<p>Of everything in this course, <strong>the safe-stimulation material is the part with '
        'immediate professional consequence.</strong> Charge density limits, charge balance and '
        'electrode dissolution are what separate a stimulator that works for fifteen years from '
        'one that damages tissue, and they are governed by well-established limits that a device '
        'engineer is expected to know. <strong>If you take one thing from this course into an '
        'interview, make it this.</strong></p>' % (W, WW)),
    summary=('Four Florida public institutions carry BME4361 at 3 credits under the identical '
             'title: FAMU and Florida State (one joint college), FAU and UF. No institution '
             'publishes a contact-hour figure.'),
    derivation='Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
)

add(
    cid='BME4581', title='BioMEMS and Microfluidics', credits=3, hours=45,
    carriers=[('FAMU', 'Introduction to BioMEMS', 3, None),
              ('FSU', 'Introduction to BioMEMS', 3, None),
              ('USF', 'Fundamentals of BioMEMS', 3, None),
              ('FAU', 'Introduction to Microfluidics and BioMEMS', 3, None)],
    prereq=(
        'Transport phenomena or fluid mechanics, and materials; read your own catalogue, because '
        'the statewide prerequisite data in this prefix is unusually unreliable. '
        'CARRIED BY FAMU, FSU, USF AND FAU at 3 credits - three independent programmes, since FAMU '
        'and FSU share one joint college. '
        'FAU TITLES IT MOST ACCURATELY: "Introduction to Microfluidics and BioMEMS". The '
        'microfluidics half is the larger half at every carrier, and a student searching for a '
        'microfluidics course will otherwise not find this one. '
        'THE PHYSICS IS THE POINT: at these scales viscosity dominates inertia, flow is laminar, '
        'mixing happens only by diffusion and surface effects govern everything. Intuition built '
        'on ordinary fluid mechanics actively misleads.'),
    lede=('<strong>BioMEMS and microfluidics</strong> is engineering at the scale of cells: '
          'lab-on-a-chip devices, microfabricated sensors, and the point-of-care diagnostics that '
          'put a laboratory test in a clinic or a pocket.',
          '%s <strong>The defining fact of the subject is that small is qualitatively different, '
          'not just smaller.</strong> At micron scale the Reynolds number is tiny, so flow is '
          'always laminar and two streams meeting in a channel do not mix except by diffusion; '
          'surface tension and surface chemistry dominate over gravity and inertia. <strong>Most '
          'of the early difficulty of this course is unlearning intuition from ordinary fluid '
          'mechanics.</strong>' % WW),
    outcomes=['Apply <strong>scaling laws</strong> and explain which forces dominate at '
              'microscale.',
              'Analyse <strong>low-Reynolds-number flow</strong> in microchannels, including '
              'pressure-driven and electrokinetic transport.',
              'Analyse <strong>diffusion-limited mixing</strong> and design around it.',
              'Describe <strong>microfabrication</strong> processes: photolithography, etching, '
              'soft lithography and PDMS moulding.',
              'Describe <strong>microscale sensing and actuation</strong> for biological '
              'measurands.',
              'Design a <strong>lab-on-a-chip</strong> device for a stated assay.',
              'Discuss <strong>point-of-care diagnostics</strong> and the constraints of use '
              'outside a laboratory.'],
    opt_outcomes=['Cleanroom fabrication practice.',
                  'Droplet microfluidics and digital microfluidics.',
                  'Organ-on-a-chip systems.',
                  'Paper-based and low-cost diagnostics for resource-limited settings.'],
    topics=['Scaling laws and dominant forces at microscale.',
            'Microfluidic flow: laminar regimes, pressure-driven and electrokinetic.',
            'Diffusion, mixing and separation in microchannels.',
            'Microfabrication: photolithography, etching, soft lithography, PDMS.',
            'Materials and surface chemistry for BioMEMS.',
            'Microscale biosensors and transduction.',
            'Lab-on-a-chip and total analysis systems.',
            'Point-of-care diagnostics and their design constraints.'],
    opt_topics=['Droplet and digital microfluidics.', 'Organ-on-a-chip.',
                'Cleanroom practice.', 'Paper microfluidics and global health applications.'],
    resources=['Nguyen, Wereley &amp; Shaegh, <em>Fundamentals and Applications of '
               'Microfluidics</em>; Folch, <em>Introduction to BioMEMS</em>.',
               'COMSOL or equivalent for microscale flow simulation, where the course uses it.',
               '%s Where a cleanroom or soft-lithography facility is available, the hands-on '
               'fabrication is the part worth pursuing — having actually made and tested a chip '
               'is uncommon at bachelor&rsquo;s level.' % W],
    career=('Named on the <strong>Biomedical Engineer</strong> career path. It leads into '
            'diagnostics and point-of-care device companies, the semiconductor-adjacent '
            'microfabrication industry, and pharmaceutical screening. %s <strong>The '
            'microfabrication skills read well outside medicine</strong> — to sensor and '
            'semiconductor employers — which is a useful second door from a small occupation. '
            % W + CAREER_TAIL),
    extra=(
        '<h3>%s Look for it under microfluidics as well as BioMEMS</h3>'
        '<p>Three carriers title it BioMEMS; <strong>FAU calls it <em>Introduction to '
        'Microfluidics and BioMEMS</em>, which is the more accurate name</strong>, because '
        'microfluidics is the larger half of the course everywhere. %s <strong>A student searching '
        'a catalogue for &ldquo;microfluidics&rdquo; will find this course at one institution out '
        'of four and miss it at the other three.</strong> Search for both terms.</p>'
        '<h3>Where it is not offered, the subject still exists nearby</h3>'
        '<p>Only four of the six Florida bachelor&rsquo;s programmes carry this number. Where yours '
        'does not, the material is frequently available through mechanical engineering (MEMS), '
        'electrical engineering (microfabrication) or chemical engineering (microscale transport). '
        '%s <strong>Ask rather than assuming the subject is unavailable</strong> — the batch of '
        'skills is the same wherever it is taught.</p>' % (WW, WW, W)),
    summary=('Four Florida public institutions carry BME4581 at 3 credits: FAMU and Florida State '
             '(one joint college) as Introduction to BioMEMS, USF as Fundamentals of BioMEMS, and '
             'FAU as Introduction to Microfluidics and BioMEMS. No institution publishes a '
             'contact-hour figure.'),
    derivation='Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
)

add(
    cid='BME4801', title='Biomedical Engineering Process Design', credits=3, hours=45,
    carriers=[('FAMU', 'Biomedical Engineering Process Design', 3, None),
              ('FSU', 'Biomedical Engineering Process Design', 3, None)],
    prereq=(
        'Senior standing and the biomedical engineering core; read your own catalogue for the exact '
        'gate. '
        'CARRIED BY FAMU AND FSU ONLY, at 3 credits - and those two share ONE joint college, so '
        'this number represents a SINGLE programme. Everything on this page should be read as a '
        'description of the FAMU-FSU College of Engineering capstone rather than a Florida norm. '
        'IT IS THE FIRST HALF OF A TWO-TERM SEQUENCE: BME4801 then BME4802. Plan both terms '
        'consecutively - the team disperses otherwise, and a graduation date depends on the pair. '
        'EVERY FLORIDA PROGRAMME RUNS A DIFFERENT CAPSTONE STRUCTURE: UF and USF use BME4882, FIU '
        'and FGCU use BME4800C, FAMU and FSU use this two-term sequence. A transfer in the final '
        'year is genuinely difficult; raise it before the junior year.',
        ),
    lede=('<strong>Biomedical Engineering Process Design</strong> is the capstone: a real design '
          'problem, in a team, to a requirement, under the regulatory regime that medical devices '
          'actually ship under.',
          '%s <strong>What makes a biomedical capstone different from every other engineering '
          'capstone is the regulatory dimension.</strong> A device is not finished when it works; '
          'it is finished when there is documented evidence that it works, that its risks have '
          'been analysed, and that the design was controlled. Design history files, risk analysis '
          'and verification and validation are part of the assessment, and they are the part '
          'employers ask about.' % WW),
    outcomes=['Translate a <strong>clinical need into engineering requirements</strong>, and '
              'defend the translation.',
              'Execute a <strong>controlled design process</strong>: requirements, concept '
              'generation, selection, detailed design, verification.',
              'Apply <strong>risk management</strong> to a medical device, in the ISO 14971 sense.',
              'Plan and interpret <strong>verification and validation</strong> testing.',
              'Produce <strong>design documentation</strong> to a professional standard.',
              'Work effectively in a <strong>team</strong>, with roles, schedule and '
              'accountability.',
              'Apply <strong>engineering ethics</strong>, and the specific obligations that arise '
              'when the user is a patient.'],
    opt_outcomes=['Work with a clinical sponsor or a real end user.',
                  'Prototyping and fabrication.',
                  'Regulatory pathway analysis — 510(k), De Novo, PMA.',
                  'Intellectual property and business case.'],
    topics=['Clinical needs finding and requirements capture.',
            'Design controls and the design history file.',
            'Concept generation, trade studies and selection.',
            'Risk management; ISO 14971 and failure modes.',
            'Verification and validation planning.',
            'Standards: IEC 60601, ISO 10993, ISO 13485 in outline.',
            'Technical writing, design reviews and presentation.',
            'Engineering ethics and human subjects considerations.'],
    opt_topics=['Regulatory pathway selection.', 'Prototyping and manufacture.',
                'Intellectual property.', 'Reimbursement and the business case.'],
    resources=['The institution&rsquo;s own capstone handbook is the operative document.',
               'Ulrich &amp; Eppinger, <em>Product Design and Development</em>; the FDA design '
               'control guidance; ISO 14971 for risk management.',
               '%s The <strong>FDA device databases</strong> — 510(k), MAUDE adverse events, '
               'recalls — are free and are the best possible source of design requirements and '
               'cautionary examples for a capstone project.' % W],
    career=('Named on the <strong>Biomedical Engineer</strong> career path, and it is the strongest '
            'single item on an entry-level r&eacute;sum&eacute;. %s <strong>Name the regulatory '
            'work explicitly</strong> — a graduate who can say they wrote a risk analysis and a '
            'verification plan is applying for quality and regulatory roles as well as design '
            'roles, and those roles are more numerous. ' % WW + CAREER_TAIL),
    extra=(
        '<h3>%s Four programmes, four capstone structures</h3>'
        '<table class="table table-sm"><thead><tr><th>Programme</th><th>Capstone</th></tr></thead>'
        '<tbody>'
        '<tr><td>FAMU-FSU College of Engineering</td><td><code>BME4801</code> then '
        '<code>BME4802</code> — two terms</td></tr>'
        '<tr><td>UF and USF</td><td><code>BME4882</code></td></tr>'
        '<tr><td>FIU and FGCU</td><td><code>BME4800C</code></td></tr>'
        '</tbody></table>'
        '<p>%s <strong>No two of Florida&rsquo;s biomedical engineering programmes number their '
        'capstone the same way</strong>, and a capstone is the hardest course in any degree to '
        'transfer because it is assessed on team work done over two terms at one institution. '
        '<strong>If you are considering a transfer, raise it before the junior year, not '
        'during the senior one.</strong></p>'
        '<h3>%s A single-programme course, and this page says so plainly</h3>'
        '<p>FAMU and Florida State are the only carriers and they are <strong>one joint '
        'college</strong>. So this is not two institutions agreeing — it is one curriculum, '
        'described once. <strong>Treat everything here as specific to the FAMU-FSU College of '
        'Engineering</strong>, and read the outcomes and topics as that college&rsquo;s capstone '
        'rather than a Florida standard.</p>'
        '<h3>%s Plan both terms together</h3>'
        '<p>The design produced in this course is built, tested and reported in '
        '<code>BME4802</code>. <strong>A schedule that separates them will not work</strong>, '
        'because the team disperses. Confirm both are offered in the terms you plan, and treat a '
        'graduation date as depending on the pair.</p>' % (WW, WW, WWW, W)),
    summary=('FAMU and Florida State carry BME4801 at 3 credits — two institutions sharing one '
             'joint college, so a single programme. It is the first half of a two-term sequence '
             'with BME4802. UF and USF run BME4882 and FIU and FGCU run BME4800C instead. No '
             'institution publishes a contact-hour figure.'),
    derivation=('Florida convention of 15 contact hours per credit at the 3-credit value. ⚠ A '
                'design course distributes its hours differently from a lecture course — team '
                'meetings, prototyping and documentation dominate — so the figure describes the '
                'credit value rather than scheduled classroom time.'),
)


def build(s):
    html = '<h2>Course Description</h2>'
    for p in s['lede']:
        html += '<p>%s</p>' % p
    n = len(s['carriers'])
    html += ('<p>Carried by <strong>%s Florida public institution%s</strong>.</p>'
             % ({1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}[n], '' if n == 1 else 's'))
    html += sec('Learning Outcomes', s['outcomes'], s['opt_outcomes'])
    html += sec('Major Topics', s['topics'], s['opt_topics'])
    html += '<h2>Resources &amp; Tools</h2><ul>' + ''.join(
        '<li>%s</li>' % r for r in s['resources']) + '</ul>'
    html += '<h2>Career Pathways</h2><p>%s</p>' % s['career']
    html += '<h2>Special Information</h2>' + s['extra'] + LANDSCAPE + PREREQ_WARNING + ABET_FE
    prereq = s['prereq'] if isinstance(s['prereq'], str) else s['prereq'][0]
    return {
        'title': s['title'], 'html_content': html, 'credits': s['credits'],
        'contact_hours': s['hours'], 'prerequisites': prereq, 'version': '1.0',
        'offering_notes': {
            'summary': s['summary'], 'hours_source': 'derived',
            'derived_contact_hours': s['hours'], 'derivation': s['derivation'],
            'offerings': [{'institution': c, 'institution_name': NAMES[c], 'title': t,
                           'credits': cr, 'contact_hours': None, 'note': nt}
                          for c, t, cr, nt in s['carriers']],
        },
    }


def main():
    over = 0
    for s in SPEC:
        g = build(s)
        io.open(os.path.join(DRAFTS, '%s_guide.json' % s['cid']), 'w', encoding='utf-8').write(
            json.dumps(g, ensure_ascii=False, indent=1))
        flag = ' <<< OVER' if len(g['prerequisites']) > 1000 else ''
        over += 1 if flag else 0
        print('%-9s %-36s %d cr /%3d hrs | prereq %4d%s | html %6d | %d carrier(s)'
              % (s['cid'], g['title'][:36], g['credits'], g['contact_hours'],
                 len(g['prerequisites']), flag, len(g['html_content']), len(s['carriers'])))
    print('\n%d draft(s) written, %d over the prerequisite limit' % (len(SPEC), over))
    return 0


if __name__ == '__main__':
    sys.exit(main())
