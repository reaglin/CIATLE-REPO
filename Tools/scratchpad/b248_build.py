#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Batch 248 -- scheduled request check 2026-11-21 (second run of the day).

Requests in rank order after the five held items (EEL2130C, ETI0602, EEL4016, EEL4081, PET1170 --
REVIEW_QUEUE 124-128): EEL4242C, EEL4242, EEL4243, EEL4448, EEL4611, EEL4610, EEL5025, EEL5009,
EEL1603, EEL1906.

  Written    EEL4242C EEL4242 EEL4243 EEL4611 EEL4610 EEL1603
  Declined   EEL1906 (UCF directed independent study): a shell number
  Held       EEL4448 (Florida Poly; no description reachable, only a title and prerequisites)
             EEL5025 (FAMU-FSU graduate; no description reachable, only its place in the M.S. rules)
             EEL5009 (FIU graduate; the only description names no topics)

Sources:
  UF         catalog.ufl.edu/UGRD/courses/electrical_and_computer_engineering/ (EEL4242C, EEL4610, EEL4657C)
  Fla Poly   2019-20 BS EE flowchart (acalog mime/media/13/483) -- EEL4242 core, EEL4448 elective with
             prerequisites; EEL5245 Power Electronics syllabus SP 2026 (catalogue description = UF's EEL4242C)
  FAMU-FSU   scratchpad/b246_famufsu_list.txt (EEL4243); eng.famu.fsu.edu/ece/graduate/courses (EEL5025)
  FIU        Coursedog cache fiu_courses.json (EEL4611, EEL5009, EEL1603)
  UWF        catalog.uwf.edu/courseinformation/courses/eel/eel.pdf (2026-27): EEL4610 ABSENT
  All        SCNS flat file (Sep 2025): carriers, titles, credits, dates
"""
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


def ul(*items):
    return '<ul>' + ''.join('<li>' + i + '</li>' for i in items) + '</ul>'


def sec(h2, req, opt):
    word = h2.split()[-1]
    out = '<h2>%s</h2><h3>Required %s</h3>' % (h2, word) + li(*req)
    if opt:
        out += '<h3>Optional %s</h3>' % word + li(*opt)
    return out


def off(code, name, title, credits, note, hours=None):
    return {'institution': code, 'institution_name': name, 'title': title, 'credits': credits,
            'contact_hours': hours, 'note': note}


DERIVED = ("Florida's convention of 15 contact hours per credit for a lecture course; no carrier "
           'publishes a contact-hour figure for this number.')
DERIVED_C = ("Florida's convention of 60 contact hours for a 3-credit integrated (C) course; UF publishes "
             'no contact-hour figure for this number.')

UF = 'University of Florida'
FLPOLY = 'Florida Polytechnic University'
FAMU = 'Florida Agricultural and Mechanical University'
FSU = 'Florida State University'
FIU = 'Florida International University'
UWF = 'University of West Florida'

# ---------------------------------------------------------------------------------------------
# Shared power-electronics material (EEL4242C, EEL4242, EEL4243)
# ---------------------------------------------------------------------------------------------
PE_NUMBERS = (
    '<h3>Power electronics runs under four numbers in Florida</h3>'
    '<p>The first power electronics course is taught under <strong>four different SCNS numbers</strong>, all at '
    '3 credits, and SCNS equivalence does not cross numbers:</p>'
    '<table class="table table-sm"><thead><tr><th>Number</th><th>Carriers</th></tr></thead><tbody>'
    '<tr><td><strong>EEL4241</strong> Power Electronics</td><td>FIU, UNF, USF; UWF as <em>Advanced Topics in '
    'Power Electronics</em></td></tr>'
    '<tr><td><strong>EEL4242C</strong> Power Electronic Circuits</td><td>UF</td></tr>'
    '<tr><td><strong>EEL4242</strong> Power Electronic Circuits</td><td>Florida Poly</td></tr>'
    '<tr><td><strong>EEL4243</strong> Power Electronics</td><td>FAMU and FSU (the joint FAMU-FSU College of '
    'Engineering)</td></tr></tbody></table>'
    '<p>The subject is the same in all four: switched converters for power conversion. If you transfer, bring '
    'the syllabus; an evaluator matching on the number alone will see four different courses.</p>')

PE_RES = ul(
    '<em>Fundamentals of Power Electronics</em>, Erickson and Maksimovi&#263; (Springer) &mdash; the standard '
    'text for converter analysis, averaged models and control.',
    '<em>Power Electronics: Circuits, Devices and Applications</em>, M. H. Rashid (Pearson) &mdash; Rashid '
    'teaches power electronics at Florida Poly and uses it there.',
    '<em>Power Electronics: Converters, Applications and Design</em>, Mohan, Undeland and Robbins (Wiley).',
    'Simulation: LTspice, PSIM, PLECS or MATLAB/Simulink (Simscape Electrical).',
    'Device data sheets and application notes from the makers of MOSFETs, IGBTs, SiC and GaN switches and '
    'gate drivers.',
    'Bench work, where there is any: an isolated or differential probe, a current probe, and an oscilloscope '
    'rated for the voltages involved.')

PE_CAREERS = ul(
    '<strong>Power electronics engineer</strong> (electrical engineers, SOC 17-2071; electronics engineers, '
    '17-2072): power supplies, motor drives, chargers and inverters.',
    '<strong>Renewable-energy and storage engineer</strong>: every solar plant and battery system connects '
    'through an inverter. Florida Power &amp; Light runs one of the largest utility solar and battery fleets in '
    'the country.',
    '<strong>Electric-vehicle and transportation engineer</strong>: traction inverters, on-board chargers and '
    'charging stations.',
    '<strong>Aerospace and defence</strong>: more-electric aircraft and spacecraft power systems on the Space '
    'Coast and in Central Florida (L3Harris, Lockheed Martin, Northrop Grumman, Collins Aerospace and others).',
    '<strong>Research</strong>: FSU\'s Center for Advanced Power Systems in Tallahassee works on power '
    'electronics for ships and the grid, often through graduate study.')

PE_SAFETY = (
    '<h3>Safety</h3>'
    '<p>Converters store energy in capacitors and inductors and run at voltages that can kill. Where a course has '
    'laboratory work, discharge capacitors before touching a circuit, never float an oscilloscope ground to '
    'measure a switching node (use a differential probe), and follow the laboratory\'s rules exactly.</p>')

PE_AI = (
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain a converter, derive a steady-state relation or help set up a simulation, and they are '
    'useful for that. They are weak exactly where power electronics is hard: they often mix up continuous and '
    'discontinuous conduction, quote the ideal duty-cycle formula where losses matter, and invent device ratings. '
    '<strong>Check every result with a volt-second and charge balance, take ratings from the data sheet, and '
    'simulate before you build.</strong> Follow your instructor\'s policy on AI use.</p>')

PE_OUTCOMES = [
    'Explain how <strong>switched-mode conversion</strong> regulates power, and why it is far more efficient than '
    'a linear regulator.',
    'Analyse the steady state of the basic <strong>DC-DC converters</strong> (buck, boost, buck-boost) using '
    'inductor volt-second balance and capacitor charge balance.',
    'Calculate ripple, component stresses and losses, and choose inductors, capacitors and switches.',
    'Analyse <strong>rectifiers</strong> and <strong>inverters</strong> (DC-AC) and their output waveforms.',
    'Explain <strong>pulse-width modulation</strong> and how duty cycle sets the output.',
    'Simulate a converter and compare the result with hand analysis.']

PE_TOPICS = [
    'Power semiconductor switches: diodes, MOSFETs, IGBTs, thyristors; wide-bandgap SiC and GaN.',
    'Buck, boost and buck-boost converters; continuous and discontinuous conduction.',
    'Isolated converters: flyback and forward.',
    'Rectifiers, single- and three-phase.',
    'Inverters and PWM.',
    'Losses, efficiency and heat.',
    'Simulation of switching circuits.']

# ---------------------------------------------------------------------------------------------
# EEL4242C Power Electronic Circuits -- UF
# ---------------------------------------------------------------------------------------------
EEL4242C_PRE = ('UF, the only carrier: its catalogue prints the prerequisite as "EEL 3308", a number UF does '
                'not carry; it almost certainly means EEE3308C Electronic Circuits 1 (4 credits, itself after '
                'EEL3111C with C or better). Confirm with UF ECE before registering. *** The same subject is '
                'EEL4242 at Florida Poly, EEL4241 at FIU, UNF, USF and UWF, and EEL4243 at FAMU-FSU: SCNS '
                'equivalence does not cross numbers, so bring a syllabus if you transfer.')

EEL4242C_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4242C Power Electronic Circuits</strong> is a senior electrical engineering elective taught by '
    '<strong>one Florida public institution, the University of Florida</strong>, at <strong>3 credits</strong>. '
    'UF\'s catalogue describes it in one line: <em>"Circuit topologies, analysis, design and simulation of '
    'electronic circuits such as power supplies, and motor drives."</em> It appears on UF\'s list of electrical '
    'engineering technical electives.</p>'
    '<p>Power electronics is the part of electrical engineering that converts electric power from one form to '
    'another &mdash; AC to DC, one DC voltage to another, DC to AC at a chosen frequency &mdash; using '
    'semiconductor switches turned on and off thousands of times a second. It is in every phone charger, laptop '
    'supply, motor drive, solar inverter and electric vehicle. The <strong>C</strong> suffix marks an integrated '
    'course: expect design and simulation work alongside the lectures. UF\'s catalogue gives no topic list, so the '
    'outcomes below are the standard content of a first power electronics course; check the syllabus.</p>'
    + sec('Learning Outcomes', PE_OUTCOMES + [
        'Complete a <strong>design project</strong> to a specification, using simulation to check it.'],
        ['Model a converter\'s dynamics (averaged switch model) and design a feedback controller for it.',
         'Analyse a motor drive: a DC chopper or a three-phase inverter feeding an induction or permanent-magnet '
         'motor.',
         'Build and measure a converter on the bench.'])
    + sec('Major Topics', PE_TOPICS + ['Power supplies and motor drives as applications (UF\'s catalogue names '
                                       'both).'],
          ['Averaged models and closed-loop control.', 'Gate drivers, snubbers and magnetics design.',
           'Electromagnetic interference and layout.'])
    + '<h2>Resources &amp; Tools</h2>' + PE_RES
    + '<h2>Career Pathways</h2>' + PE_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: the University of Florida, at 3 credits.</strong> UF publishes no contact '
    'hours; the 60 shown are derived from Florida\'s convention for a 3-credit integrated (C) course. The number '
    'entered the state file under UF in 1998. UF also teaches <strong>EEL4248 Fundamentals of RF and Power '
    'Electronic Devices</strong>, which covers the semiconductor devices themselves rather than the circuits.</p>'
    '<h3>Prerequisites &mdash; a catalogue misprint to check</h3>'
    '<p>UF\'s current catalogue prints the prerequisite as <strong>EEL 3308</strong>. UF carries no course with '
    'that number; its electronics course is <strong>EEE3308C Electronic Circuits 1</strong> (4 credits, after '
    'EEL3111C Circuits 1 with C or better), and older UF catalogues gave EEE3308C as this course\'s prerequisite. '
    'Plan on EEE3308C, and confirm with the department.</p>'
    + PE_NUMBERS
    + '<p><strong>Florida Poly\'s EEL4242</strong> carries the same number without the C and the same title; its '
    'own guide is on this site.</p>'
    + PE_SAFETY + PE_AI)

EEL4242C = {
    'title': 'Power Electronic Circuits',
    'html_content': EEL4242C_HTML,
    'credits': 3,
    'contact_hours': 60,
    'prerequisites': EEL4242C_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, the University of Florida, at 3 credits.',
        'hours_source': 'derived',
        'derived_contact_hours': 60,
        'derivation': DERIVED_C,
        'offerings': [off('UF', UF, 'Power Electronic Circuits', 3,
                          'Technical elective. Catalogue prerequisite printed as "EEL 3308" (read EEE3308C).')],
    },
}

# ---------------------------------------------------------------------------------------------
# EEL4242 Power Electronic Circuits -- Florida Poly
# ---------------------------------------------------------------------------------------------
EEL4242_PRE = ('Florida Poly, the only carrier: its own catalogue entry could not be read for this guide. Expect '
               'electronic circuits and signals and systems, and check the Florida Poly catalogue. In the '
               '2019-20 BS Electrical Engineering plan it is a required senior course. *** The same subject is '
               'EEL4242C at UF, EEL4241 at FIU, UNF, USF and UWF, and EEL4243 at FAMU-FSU: SCNS equivalence does '
               'not cross numbers, so bring a syllabus if you transfer.')

EEL4242_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4242 Power Electronic Circuits</strong> is a senior electrical engineering course taught by '
    '<strong>one Florida public institution, Florida Polytechnic University</strong> in Lakeland, at <strong>3 '
    'credits</strong>. In Florida Poly\'s 2019-20 BS in Electrical Engineering plan it is a <strong>required '
    'senior course</strong> (listed as <em>Power Electronics Circuits</em>), beside EEL4652 Control Theory and '
    'the senior design pair.</p>'
    '<p>Florida Poly\'s own description of EEL4242 could not be read for this guide: its catalogue pages answer '
    'with empty responses to automated requests. Two things point to the content. The number and title are the '
    'same as UF\'s <strong>EEL4242C Power Electronic Circuits</strong>, and Florida Poly\'s graduate '
    '<strong>EEL5245 Power Electronics</strong> uses, word for word, UF\'s description of that course: '
    '<em>"Circuit topologies, analysis, design and simulation of power electronic circuits such as power '
    'supplies and motor drives."</em> Florida Poly\'s power electronics is taught by <strong>Muhammad H. '
    'Rashid</strong>, author of one of the standard textbooks in the field. The outcomes below are the standard '
    'content of a first power electronics course; check the syllabus for your term.</p>'
    + sec('Learning Outcomes', PE_OUTCOMES,
          ['Model a converter\'s dynamics and design a feedback controller for it.',
           'Analyse a motor drive.',
           'Simulate power circuits in SPICE or LTspice to the level of Rashid\'s simulation texts.'])
    + sec('Major Topics', PE_TOPICS,
          ['AC voltage controllers and cycloconverters.', 'Gate drive and protection.',
           'Applications: power supplies, motor drives, renewable-energy inverters.'])
    + '<h2>Resources &amp; Tools</h2>' + PE_RES
    + '<h2>Career Pathways</h2>' + PE_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: Florida Polytechnic University, at 3 credits.</strong> Florida Poly publishes '
    'no contact hours; the 45 shown are derived from Florida\'s convention of 15 per credit for a lecture course. '
    'The number entered the state file under Florida Poly in 2017.</p>'
    '<h3>Prerequisites</h3>'
    '<p>Florida Poly\'s prerequisite for EEL4242 could not be read. Its flowchart places the course in the senior '
    'year after the electronics and signals courses. Check the current catalogue, and note that Florida Poly '
    'states on its syllabi that prerequisites are <strong>strictly enforced</strong>: a student who completes a '
    'course without its prerequisites must retake it.</p>'
    + PE_NUMBERS
    + '<p><strong>UF\'s EEL4242C</strong> carries the same number with a C (integrated) suffix and the same '
    'title; its own guide is on this site. Florida Poly\'s graduate <strong>EEL5245 Power Electronics</strong> '
    '(also at UCF and UWF) is the next course for students who continue.</p>'
    + PE_SAFETY + PE_AI)

EEL4242 = {
    'title': 'Power Electronic Circuits',
    'html_content': EEL4242_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4242_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, Florida Polytechnic University, at 3 credits.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [off('FLPOLY', FLPOLY, 'Power Electronic Circuits', 3,
                          'Required senior course in the 2019-20 BS EE plan. Catalogue entry not readable.')],
    },
}

# ---------------------------------------------------------------------------------------------
# EEL4243 Power Electronics -- FAMU, FSU
# ---------------------------------------------------------------------------------------------
EEL4243_PRE = ('FAMU-FSU College of Engineering: EEE3300 Electronics I and EEL3135 Signals and Systems. *** The '
               'same subject is EEL4241 at FIU, UNF, USF and UWF, EEL4242C at UF and EEL4242 at Florida Poly: '
               'SCNS equivalence does not cross numbers, so bring a syllabus if you transfer.')

EEL4243_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4243 Power Electronics</strong> is a senior electrical engineering elective carried by '
    '<strong>Florida A&amp;M University and Florida State University</strong>, both at 3 credits. The two '
    'universities share one engineering school, the <strong>FAMU-FSU College of Engineering</strong> in '
    'Tallahassee, so the two listings are one course taught to students of both.</p>'
    '<p>The college describes it this way: <em>"This course is designed to develop a basic understanding of '
    'using switched electronic circuits for the conversion and regulation of power. The course focuses on the '
    'basic converters and their steady state analysis. Dynamic modeling analysis, controller design, power '
    'semiconductor device, and simulation also are covered."</em> It is the first of the college\'s power '
    'electronics courses: <strong>EEL4244 Power Conversion and Control</strong> (FAMU\'s listing) and the '
    'graduate <strong>EEE5317 Power Electronics</strong>, a core course in the college\'s graduate programme, '
    'follow.</p>'
    + sec('Learning Outcomes', PE_OUTCOMES + [
        'Build a <strong>dynamic (averaged) model</strong> of a converter and design a simple feedback controller '
        'for it (the college\'s description names both).',
        'Explain the characteristics of <strong>power semiconductor devices</strong> and how they limit a '
        'design.'],
        ['Analyse current-programmed (peak current-mode) control.',
         'Apply converters to renewable energy, storage and electric drives.'])
    + sec('Major Topics', PE_TOPICS + ['Averaged switch models, small-signal transfer functions and controller '
                                       'design.'],
          ['Voltage-source and current-source converter models.',
           'Magnetics design.', 'Electromagnetic interference.'])
    + '<h2>Resources &amp; Tools</h2>' + PE_RES
    + '<h2>Career Pathways</h2>' + PE_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>Two carriers in the state file, FAMU and FSU, both at 3 credits &mdash; one course</strong>, '
    'taught by the joint college. Neither publishes contact hours, so the 45 shown are derived from Florida\'s '
    'convention of 15 per credit for a lecture course. Both entered the number in 2003.</p>'
    '<h3>Prerequisites</h3>'
    '<p><strong>EEE3300 Electronics I</strong> and <strong>EEL3135 Signals and Systems</strong>. The signals '
    'course matters: the dynamic modelling and controller design in the second half use Laplace transforms and '
    'Bode plots. FAMU\'s EEL4244 Power Conversion and Control asks instead for EEE3300 and EEL3112 Circuits II.</p>'
    + PE_NUMBERS + PE_SAFETY + PE_AI)

EEL4243 = {
    'title': 'Power Electronics',
    'html_content': EEL4243_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4243_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'FAMU and FSU, both at 3 credits: one course taught by the joint FAMU-FSU College of '
                   'Engineering.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [
            off('FAMU', FAMU, 'Power Electronics', 3,
                'Joint FAMU-FSU College of Engineering. Prerequisites EEE3300 and EEL3135.'),
            off('FSU', FSU, 'Power Electronics', 3,
                'Joint FAMU-FSU College of Engineering. Prerequisites EEE3300 and EEL3135.')],
    },
}

# ---------------------------------------------------------------------------------------------
# Shared control material (EEL4611, EEL4610)
# ---------------------------------------------------------------------------------------------
CTRL_RES = ul(
    '<em>Modern Control Engineering</em>, Ogata (Pearson); <em>Control Systems Engineering</em>, Nise (Wiley); '
    '<em>Feedback Control of Dynamic Systems</em>, Franklin, Powell and Emami-Naeini (Pearson).',
    'MATLAB with the Control System Toolbox and Simulink, or Python with the <code>control</code> and SciPy '
    'packages.',
    'The text of the first control course, which this one continues.')

CTRL_CAREERS = ul(
    '<strong>Controls engineer</strong> (electrical engineers, SOC 17-2071; also mechanical and aerospace): '
    'motion control, process control, power converters, robotics.',
    '<strong>Guidance, navigation and control (GNC) engineer</strong> in aerospace and defence: the Space Coast '
    'and Central Florida employers (Lockheed Martin, L3Harris, Northrop Grumman, Blue Origin, SpaceX) hire for '
    'flight control.',
    '<strong>Automation and industrial controls engineer</strong> in manufacturing, utilities and water '
    'treatment, often working with PLCs and process instruments.',
    'The <strong>Professional Engineer (PE) licence</strong> in <em>Control Systems</em> or <em>Electrical and '
    'Computer</em>: the FE exam (which tests control topics) comes first (s. 471.013, F.S.).')

# ---------------------------------------------------------------------------------------------
# EEL4611 Control Systems II -- FIU
# ---------------------------------------------------------------------------------------------
EEL4611_PRE = ('FIU, the only carrier: FIU\'s record prints no prerequisite. By its title it follows FIU\'s '
               'EEL3657 Control Systems I (itself after EEL3110C and EEL3135); check with FIU ECE before '
               'registering. Spring term only. *** The statewide title is Analog Control Systems; no other '
               'Florida public institution carries this number.')

EEL4611_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4611 Control Systems II</strong> is a senior electrical engineering course taught by <strong>one '
    'Florida public institution, Florida International University</strong>, at <strong>3 credits</strong>, and '
    'only in the <strong>spring term</strong>. The statewide title is <em>Analog Control Systems</em>.</p>'
    '<p>FIU describes it as <em>"Design by Root-Locus, Bode plot, and Guillemin-Truxal approach; characteristics '
    'of some typical industrial controllers and sensors. Computer simulation and other modern topics are '
    'included."</em> (FIU\'s record spells the name "Guillin-Truxal".) It is the <strong>design</strong> half of '
    'FIU\'s two control courses. <strong>EEL3657 Control Systems I</strong> teaches analysis &mdash; modelling, '
    'time and frequency response, stability, root locus, Bode and Nyquist plots &mdash; and this course uses those '
    'tools to design compensators that meet a specification. FIU also carries a 1-credit <strong>EEL4611L Systems '
    'Laboratory</strong>.</p>'
    + sec('Learning Outcomes', [
        'Translate a performance specification (overshoot, settling time, steady-state error, bandwidth, phase '
        'margin) into a design target.',
        'Design <strong>lead, lag and lead-lag compensators</strong> using the <strong>root locus</strong>.',
        'Design compensators in the frequency domain using <strong>Bode plots</strong> and gain and phase '
        'margins.',
        'Apply the <strong>Guillemin-Truxal</strong> method: choose the closed-loop transfer function first, then '
        'work back to the controller that produces it.',
        'Tune and analyse <strong>PID controllers</strong> of the kind used in industry.',
        'Simulate a closed-loop design and check it against the specification.'],
        ['Describe typical industrial sensors and actuators and how their dynamics enter a design.',
         'Introduce state-space design or digital implementation of a controller.'])
    + sec('Major Topics', [
        'Review: transfer functions, stability, steady-state error.',
        'Root-locus design: lead, lag, PID.',
        'Frequency-response design: Bode, gain and phase margins, Nyquist.',
        'The Guillemin-Truxal (synthesis) method.',
        'Industrial controllers and sensors.',
        'Computer simulation of control systems.'],
        ['State-space methods and pole placement.', 'Digital implementation and sampling.',
         'Robustness and sensitivity.'])
    + '<h2>Resources &amp; Tools</h2>' + CTRL_RES
    + '<h2>Career Pathways</h2>' + CTRL_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: Florida International University, at 3 credits</strong>, spring term only. '
    'FIU publishes no contact hours; the 45 shown are derived from Florida\'s convention of 15 per credit for a '
    'lecture course. The number entered the state file under FIU in 2005.</p>'
    '<h3>Prerequisites</h3>'
    '<p>FIU\'s course record carries <strong>no prerequisite text</strong>. By its title and description it follows '
    '<strong>EEL3657 Control Systems I</strong>, whose prerequisites are EEL3110C and EEL3135. Confirm with the '
    'department, and plan for a spring-only course: missing it costs a year.</p>'
    '<h3>Second control courses elsewhere</h3>'
    '<p>Other Florida universities number their control courses differently, so this number will not match on '
    'transfer: the first course is <strong>EEL4657</strong> at UNF, USF and UWF (EEL4657C at UF), <strong>EEL4652'
    '</strong> at FAMU-FSU and Florida Poly; second courses include <strong>EEL4612</strong> Control System Design '
    '(Florida Poly), <strong>EEL4612C</strong> Modern and Robust Control (UCF) and <strong>EEL4610</strong> '
    'State Variable Methods (UF). Bring the syllabus.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain a root-locus rule or write the MATLAB or Python for a Bode plot, and that saves time. '
    'They are unreliable on the design itself: they often place a lead compensator\'s zero and pole the wrong way '
    'round, misread phase margin, or claim a design meets a specification it does not. <strong>Simulate the closed '
    'loop and check every number against the specification.</strong> Follow your instructor\'s policy on AI use.'
    '</p>')

EEL4611 = {
    'title': 'Control Systems II',
    'html_content': EEL4611_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4611_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, Florida International University, at 3 credits, spring term only.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [off('FIU', FIU, 'Control Systems II', 3,
                          'Spring term only. FIU\'s record carries no prerequisite text; follows EEL3657.')],
    },
}

# ---------------------------------------------------------------------------------------------
# EEL4610 State Variables and Control -- UF (UWF in the state file, not in its 2026-27 catalogue)
# ---------------------------------------------------------------------------------------------
EEL4610_PRE = ('UF: EEL4657C Linear Control Systems. UWF also carries the number in the state file but does not '
               'list it in its 2026-27 catalogue (state-space design is part of UWF\'s EEL4657 there). Expect '
               'linear algebra (matrices, eigenvalues) and differential equations from earlier courses.')

EEL4610_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4610</strong> is a senior control course. The statewide title is <em>State Variables and '
    'Control</em>. The <strong>University of Florida</strong> teaches it as <strong>State Variable Methods in '
    'Linear Systems</strong>, at <strong>3 credits</strong>: <em>"Development of state-variable approach to '
    'linear continuous-time and discrete-time systems with emphasis on the design of feedback control '
    'systems."</em> The <strong>University of West Florida</strong> also carries the number in the state file, as '
    '<em>State Variables and Control</em>, but it is not in UWF\'s 2026-27 catalogue (see below).</p>'
    '<p>A first control course describes a system by a transfer function, one input to one output. This course '
    'describes it by a set of first-order differential (or difference) equations in matrix form, '
    '<strong>x&#775; = Ax + Bu, y = Cx + Du</strong>. That form handles many inputs and outputs, shows what is '
    'happening inside the system, and is the basis of modern control: pole placement, observers, optimal control '
    'and the Kalman filter. At UF it follows <strong>EEL4657C Linear Control Systems</strong>.</p>'
    + sec('Learning Outcomes', [
        'Write <strong>state-space models</strong> of physical systems and convert between state-space and '
        'transfer-function forms.',
        'Solve the state equations using the <strong>state-transition matrix</strong>, for continuous-time and '
        'discrete-time systems.',
        'Test <strong>controllability</strong> and <strong>observability</strong> and explain what they mean '
        'physically.',
        'Analyse stability from eigenvalues, and by Lyapunov methods.',
        'Design <strong>state-feedback controllers by pole placement</strong>.',
        'Design <strong>state observers</strong> (estimators) and combine them with state feedback.'],
        ['Introduce optimal control: the linear-quadratic regulator (LQR).',
         'Introduce the Kalman filter.',
         'Discretise a continuous design for a digital controller.'])
    + sec('Major Topics', [
        'State variables, state-space models and canonical forms.',
        'Linear algebra for systems: eigenvalues, eigenvectors, similarity transforms.',
        'Solution of state equations; the matrix exponential.',
        'Discrete-time state-space systems.',
        'Controllability, observability, realisations.',
        'Pole placement and observer design; the separation principle.'],
        ['Lyapunov stability.', 'LQR.', 'Kalman filtering.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('<em>Linear System Theory and Design</em>, Chen (Oxford) &mdash; a common text for this course.',
         '<em>Modern Control Engineering</em>, Ogata, and <em>Modern Control Systems</em>, Dorf and Bishop '
         '(Pearson).',
         'MATLAB (Control System Toolbox: <code>ss</code>, <code>place</code>, <code>ctrb</code>, '
         '<code>obsv</code>, <code>lqr</code>) or Python (<code>control</code>, NumPy, SciPy).',
         'Your linear algebra text: this course uses it constantly.')
    + '<h2>Career Pathways</h2>' + CTRL_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<table class="table table-sm"><thead><tr><th>Institution</th><th>Its title</th><th>Credits</th><th>Status'
    '</th></tr></thead><tbody>'
    '<tr><td>University of Florida</td><td>State Variable Methods in Linear Systems</td><td>3</td><td>In UF\'s '
    'current catalogue; prerequisite EEL4657C</td></tr>'
    '<tr><td>University of West Florida</td><td>State Variables and Control</td><td>3</td><td>In the state file '
    'since 2007, <strong>not in UWF\'s 2026-27 catalogue</strong></td></tr></tbody></table>'
    '<p>Both carry it at 3 credits. Neither publishes contact hours, so the 45 shown are derived from Florida\'s '
    'convention of 15 per credit for a lecture course.</p>'
    '<h3>At UWF</h3>'
    '<p>UWF\'s current catalogue has no EEL4610. Its <strong>EEL4657 Linear Control Systems</strong> (3 credits, '
    'after EEL3112) now <em>"introduces State Space Methods for controller and observer design"</em>, and its '
    'discrete-time control course is offered concurrently with the graduate EEL5630. A UWF student who wants this '
    'material should ask the department whether EEL4610 is still scheduled.</p>'
    '<h3>Prerequisites</h3>'
    '<p>At UF, <strong>EEL4657C Linear Control Systems</strong> (4 credits). Beyond that, the course leans hard on '
    '<strong>linear algebra</strong> &mdash; eigenvalues, matrix exponentials, rank &mdash; and students who have '
    'forgotten it struggle in the first weeks. Review it before the term.</p>'
    '<h3>Graduate study</h3>'
    '<p>State-space methods are the starting point of graduate control (linear systems theory, optimal and robust '
    'control, estimation). This course is good preparation for a master\'s in control or for GNC work.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain controllability or set up a pole-placement problem in MATLAB or Python, and they '
    'help with that. They make mistakes in exactly the matrix algebra this course teaches: wrong dimensions, a '
    'controllability matrix built in the wrong order, or a canonical form that does not match the transfer '
    'function. <strong>Check every model by converting it back, and check every design by simulating the closed '
    'loop.</strong> Follow your instructor\'s policy on AI use.</p>')

EEL4610 = {
    'title': 'State Variable Methods in Linear Systems',
    'html_content': EEL4610_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4610_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'UF and UWF in the state file, both at 3 credits; UWF does not list it in its 2026-27 '
                   'catalogue.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [
            off('UF', UF, 'State Variable Methods in Linear Systems', 3, 'Prerequisite EEL4657C.'),
            off('UWF', UWF, 'State Variables and Control', 3,
                'In the state file since 2007; not in UWF\'s 2026-27 catalogue.')],
    },
}

# ---------------------------------------------------------------------------------------------
# EEL1603 Introduction to Robotic Systems, Instrumentation, and Control for ECE -- FIU
# ---------------------------------------------------------------------------------------------
EEL1603_PRE = ('FIU, the only carrier: no prerequisite. A first-year course for electrical and computer '
               'engineering students, fall term only, new in 2025. *** Its statewide title is "Robotics-Mechanics '
               'and Controls", the same as Northwest Florida State\'s EEL2603C, but that is a different number '
               'and SCNS equivalence does not cross numbers.')

EEL1603_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL1603 Introduction to Robotic Systems, Instrumentation, and Control for Electrical and Computer '
    'Engineers</strong> is a first-year course taught by <strong>one Florida public institution, Florida '
    'International University</strong>, at <strong>3 credits</strong>, in the <strong>fall term only</strong>. It '
    'is new: it entered the state file in August 2025.</p>'
    '<p>FIU describes it as follows: <em>"This course will introduce robotic systems, covering essential robotic '
    'system components and application implementation. Students will participate in hands-on lessons about basic '
    'robotic components, sensors, control systems, visual recognition, and other emerging technologies."</em> FIU\'s '
    'proposal for the course says robotics is a focus area of its College of Engineering and Computing, that the '
    'ECE department plans a series of robotics courses, and that this entry-level course is meant to <em>"spark '
    'students\' interest in robotics and prepare them for more advanced robotics courses."</em></p>'
    '<p>FIU publishes no topic list beyond that description, so the outcomes below follow it; expect them to '
    'change as the course settles. Check the syllabus.</p>'
    + sec('Learning Outcomes', [
        'Name the parts of a robotic system &mdash; mechanism, actuators, sensors, controller, power, software '
        '&mdash; and explain how they work together.',
        'Connect and read basic <strong>sensors</strong> (distance, light, inertial, encoders) from a '
        'microcontroller and interpret the measurements.',
        'Drive <strong>motors and actuators</strong> and explain the idea of <strong>feedback control</strong>.',
        'Use a camera and simple <strong>visual recognition</strong> to let a robot respond to what it sees.',
        'Build and program a small robot to complete a task, working in a team.'],
        ['Explain how robotics connects to later ECE courses (circuits, embedded systems, control, machine '
         'learning).',
         'Describe emerging robotics technologies and their uses.'])
    + sec('Major Topics', [
        'Robotic system components.', 'Sensors and basic instrumentation.', 'Motors, actuators and drivers.',
        'Introduction to feedback control.', 'Microcontroller programming for robots.',
        'Visual recognition.', 'Team projects.'],
        ['Emerging technologies (for example autonomous navigation, AI in robotics).', 'Robot safety.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('A microcontroller or educational robot kit (Arduino, Raspberry Pi or similar) &mdash; FIU sets the kit.',
         'A programming language: Python or C/C++ as used with the kit.',
         'A computer-vision library such as OpenCV, or a vision module that does recognition on board.',
         'Basic bench tools: multimeter, breadboard, power supply.')
    + '<h2>Career Pathways</h2>'
    + ul('It is a first course, so it points to careers rather than preparing for one directly.',
         '<strong>Robotics and automation engineer</strong> (electrical engineers, SOC 17-2071; robotics also '
         'draws on mechanical and computer engineering): manufacturing, logistics, medical devices, defence.',
         '<strong>Embedded systems and controls engineer</strong>.',
         'South Florida has growing robotics and drone employers, and the Space Coast\'s aerospace firms use '
         'robotic systems in manufacturing and in space.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: Florida International University, at 3 credits</strong>, fall term only, new '
    'in 2025. FIU records it as a lecture course and publishes no contact hours; the 45 shown are derived from '
    'Florida\'s convention of 15 per credit. Expect hands-on work in class, as FIU\'s description says.</p>'
    '<h3>Prerequisites</h3>'
    '<p>None are listed. It is written for first-year ECE students; no programming or circuits background is '
    'assumed, though either helps.</p>'
    '<h3>A shared statewide title</h3>'
    '<p>The state file gives this number the statewide title <em>Robotics-Mechanics and Controls</em>, the same '
    'title as <strong>EEL2603C</strong>, which Northwest Florida State College carries. They are different numbers '
    'and SCNS equivalence does not cross numbers, so do not assume one substitutes for the other on transfer. '
    'Bring the syllabus.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools are good at writing starter code for a sensor or motor and at explaining an error message, and '
    'they can help a first-year student get unstuck. They do not know your kit\'s exact wiring or library version, '
    'and their code often uses the wrong pins or a function that does not exist. <strong>Read the code before you '
    'run it, test one part at a time, and power down before changing wiring.</strong> Follow your instructor\'s '
    'policy on AI use.</p>')

EEL1603 = {
    'title': 'Introduction to Robotic Systems, Instrumentation, and Control for Electrical and Computer Engineers',
    'html_content': EEL1603_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL1603_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, Florida International University, at 3 credits, fall term only (new 2025).',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [off('FIU', FIU, 'Introduction to Robotic Systems, Instrumentation, and Control for '
                          'Electrical and Computer Engineers', 3, 'Fall term only. No prerequisite. New 2025.')],
    },
}

ALL = (('EEL4242C', EEL4242C), ('EEL4242', EEL4242), ('EEL4243', EEL4243), ('EEL4611', EEL4611),
       ('EEL4610', EEL4610), ('EEL1603', EEL1603))

for cid, g in ALL:
    path = os.path.join(DRAFTS, '%s_guide.json' % cid)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(g, fh, ensure_ascii=False, indent=1)
    print('wrote', cid, len(g['html_content']), 'chars; prereq', len(g['prerequisites']))
