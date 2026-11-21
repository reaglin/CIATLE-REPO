#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Batch 247 -- scheduled request check 2026-11-21.

Requests in rank order after the three held items (EEL2130C, ETI0602, EEL4016 -- REVIEW_QUEUE 124-126):
EEL4081, EEL4119L, EEL4113, EEL4206L, EEL4210, EEL4212, EEL4213L, EEL4214, EEL4215, EEL4217L, PET1170, EEE4351.

  Written    EEL4119L EEL4113 EEL4206L EEL4210 EEL4212 EEL4213L EEL4214 EEL4215 EEL4217L EEE4351
  Skipped    EEL4081 (UNF, new 2026-08-16: no description reachable) and PET1170 (Miami Dade only:
             every MDC catalogue route failed). Left waiting; REVIEW_QUEUE 127.

Sources:
  USF        cloud.usf.edu/academic-programs/details/prefix/<PFX>/code/<NUM> (EEL4206L, EEL4212,
             EEL4213, EEL4214, EEL4241, EGN3374, EGN3375)
  UWF        catalog.uwf.edu/search/?P=EEL%204210 and EEL%203211
  FAMU-FSU   eng.famu.fsu.edu ECE course list (scratchpad/b246_famufsu_list.txt): EEL4113, EEL4217L, EEE4351
  FIU        Coursedog cache fiu_courses.json: EEL4212, EEL4213, EEL4213L, EEL4214, EEL4215, EEL3110C
  FAU        Coursedog cache fau_courses.json: EEL4119L and its prerequisites
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
DERIVED_LAB = ('The convention this site uses for a 1-credit engineering laboratory (one three-hour session a '
               'week, 45 hours a term); no carrier publishes a contact-hour figure for this number.')

FAMU = 'Florida Agricultural and Mechanical University'
FSU = 'Florida State University'
FIU = 'Florida International University'
USF = 'University of South Florida'
UWF = 'University of West Florida'
FAU = 'Florida Atlantic University'

JOINT = ('<p>FAMU and FSU share one engineering school, the <strong>FAMU-FSU College of Engineering</strong> in '
         'Tallahassee, so the two listings are one course taught to students of both universities, not two '
         'separate courses.</p>')

POWER_CAREERS = ul(
    '<strong>Power systems engineer</strong> at an electric utility (electrical engineers, SOC 17-2071): '
    'Florida Power &amp; Light (the largest utility in the state), Duke Energy Florida, Tampa Electric, the '
    'Jacksonville Electric Authority, Orlando Utilities Commission, and the municipal utilities and electric '
    'co-operatives.',
    '<strong>Protection, planning and distribution engineer</strong> at a utility, or at a consulting firm '
    'that designs substations and interconnections for them.',
    '<strong>Renewable-energy and interconnection engineer</strong>: Florida has one of the fastest-growing '
    'utility-scale solar fleets in the country, and every plant needs grid studies.',
    '<strong>Power engineer in industry</strong>: data centres, hospitals, ports, manufacturing plants and '
    'theme parks all run large electrical systems.',
    'The <strong>Professional Engineer (PE) licence</strong>: power engineers who sign drawings need it. The '
    'route is the FE exam, four years of qualifying experience, and the PE <em>Electrical and Computer: '
    'Power</em> exam (s. 471.013, F.S.).')


# --------------------------------------------------------------------------
# EEL4119L Electronics Laboratory 2 -- FAU
# --------------------------------------------------------------------------
EEL4119L_PRE = ('FAU, the only carrier: EEE4361C Electronics 2 and Lab and EEL3118L Electronics Laboratory 1, '
                'both with C or better; and EEL3470 Electromagnetic Fields and Waves and EEL4656 Analysis of '
                'Linear Systems, taken before or at the same time, with C or better. *** A 3-credit '
                'laboratory: FAU runs its electronics labs at 3 credits, where most universities run a lab at '
                '1. Count it at 3 in a degree plan.')

EEL4119L_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4119L Electronics Laboratory 2</strong> is a senior electrical engineering laboratory taught '
    'by <strong>one Florida public institution, Florida Atlantic University</strong>, at <strong>3 '
    'credits</strong>. FAU\'s catalogue describes it in one line: <em>"Experiments and projects to supplement '
    'the theoretical work in core courses."</em> The statewide title is simply <em>Laboratory II</em>.</p>'
    '<p>It is the second of FAU\'s two electronics laboratories. The first, <strong>EEL3118L Electronics '
    'Laboratory 1</strong>, teaches test equipment and measurement on passive, op-amp, diode and transistor '
    'circuits. This one comes after <strong>EEE4361C Electronics 2</strong> (multi-transistor amplifiers) and '
    'alongside electromagnetics (EEL3470) and linear systems (EEL4656), and its experiments and projects draw '
    'on all of those courses: amplifiers and their frequency response, filters and signals, and transmission '
    'lines and high-frequency measurement.</p>'
    '<p>Because the catalogue gives no list of experiments, the outcomes and topics below are the expected '
    'shape of a senior electronics laboratory built on those courses. Check the syllabus for your term.</p>'
    + sec('Learning Outcomes', [
        'Design, build and test <strong>multi-stage transistor amplifiers</strong> and measure gain, bandwidth '
        'and input and output impedance.',
        'Use the oscilloscope, function generator, spectrum analyser and network or impedance analyser '
        'correctly, including probe loading and grounding.',
        'Compare measured results with <strong>hand analysis and circuit simulation</strong> (FAU uses ADS and '
        'PSPICE-type tools) and explain the differences.',
        'Measure the <strong>frequency response</strong> of filters and systems and relate it to transfer '
        'functions from linear systems.',
        'Carry out a small design project from specification to working circuit.',
        'Write <strong>laboratory reports</strong> that state method, data, uncertainty and conclusions.'],
        [
        'Make transmission-line and high-frequency measurements (reflection, matching) linked to EEL3470.',
        'Use a microcontroller or data-acquisition system to automate a measurement.',
        'Lay out and assemble a printed circuit board.'])
    + sec('Major Topics', [
        'Laboratory safety and measurement practice.',
        'Differential and multi-stage BJT and MOSFET amplifiers.',
        'Feedback, stability and frequency response.',
        'Active filters and oscillators.',
        'Simulation versus measurement.',
        'A design project and its report.'],
        [
        'Transmission lines, standing waves and impedance matching.',
        'Data converters and mixed-signal circuits.',
        'Power supplies and regulators.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul(
        'The electronics text from EEE4361C, typically <em>Microelectronic Circuits</em>, Sedra and Smith '
        '(Oxford), and the instructor\'s laboratory handouts.',
        'Simulation: Keysight ADS, LTspice or another SPICE program.',
        'Bench instruments: oscilloscope, function generator, DC supplies, digital multimeter, spectrum or '
        'network analyser.',
        'Component data sheets &mdash; reading them is part of the work.')
    + '<h2>Career Pathways</h2>'
    + ul(
        '<strong>Electronics and hardware engineer</strong> (SOC 17-2072): design and test of analog and '
        'mixed-signal circuits.',
        '<strong>Test and validation engineer</strong> in electronics manufacturing.',
        'South Florida and the Space Coast have many electronics and defence employers (for example L3Harris, '
        'Raytheon, Pratt &amp; Whitney, Siemens and many smaller design firms), and bench skills are what they '
        'test in interviews.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: Florida Atlantic University, at 3 credits.</strong> FAU\'s record lists '
    '<strong>3 laboratory hours a week</strong> (about 45 a term) and no lecture hours, so the 45 contact hours '
    'shown come from FAU. The number entered the state file under FAU in 2007 and was last changed in 2015.</p>'
    '<h3>A 3-credit laboratory</h3>'
    '<p>Most Florida universities sell an electronics laboratory at 1 credit (FAMU-FSU\'s EEE3300L, for '
    'example). FAU runs <strong>both</strong> of its electronics laboratories, EEL3118L and EEL4119L, at 3 '
    'credits. That is a permitted choice, not a fault, but it matters on transfer: a 1-credit laboratory from '
    'elsewhere will not fill a 3-credit requirement on its own, and FAU\'s 3 credits may count only as 1 at a '
    'school whose lab is 1 credit. Bring the syllabus and lab manual if you transfer either way.</p>'
    '<h3>Prerequisites</h3>'
    '<p>FAU requires <strong>EEE4361C Electronics 2 and Lab</strong> and <strong>EEL3118L Electronics '
    'Laboratory 1</strong>, both with C or better, and <strong>EEL3470 Electromagnetic Fields and Waves</strong> '
    'and <strong>EEL4656 Analysis of Linear Systems</strong> either before or at the same time, also with C or '
    'better. It is therefore a last-year course.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain a circuit, suggest component values or help write a data-analysis script. They '
    'cannot see your bench: a model will happily explain why a measurement "should" match theory when the real '
    'cause is a loading probe, a ground loop or a wrong component. <strong>Trust the measurement, find the '
    'cause, and write up what you actually observed.</strong> Laboratory data must be your own; follow your '
    'instructor\'s policy on AI use in reports.</p>'
)

EEL4119L = {
    'title': 'Electronics Laboratory 2',
    'html_content': EEL4119L_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4119L_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, Florida Atlantic University, at 3 credits (3 laboratory hours a week).',
        'hours_source': 'published',
        'offerings': [off('FAU', FAU, 'Electronics Laboratory 2', 3,
                          'FAU lists 3 laboratory hours a week. Prerequisites EEE4361C and EEL3118L (C or better); '
                          'EEL3470 and EEL4656 before or with it (C or better).')],
    },
}

# --------------------------------------------------------------------------
# EEL4113 Advanced Linear Networks -- FAMU, FSU
# --------------------------------------------------------------------------
EEL4113_PRE = ('FAMU-FSU College of Engineering: EEL3135 Signals and Linear System Analysis. Expect circuits '
               '(EEL3111, EEL3112) and differential equations before that. It is an elective; check that it is '
               'scheduled in your term.')

EEL4113_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4113 Advanced Linear Networks</strong> is an upper-division electrical engineering elective '
    'taught by <strong>Florida A&amp;M University and Florida State University</strong>, both at 3 credits. The '
    'statewide title is <em>Circuits III</em>: it is the third circuits course, after introductory circuit '
    'analysis and advanced circuits.</p>'
    + JOINT +
    '<p>The College\'s course list describes it as covering <em>"synthesis of LC one-port networks, synthesis '
    'of LC two-port networks; operational amplifier applications; active filters; approximation methods; '
    'switched-capacitor filters."</em> Where earlier circuits courses ask what a given circuit does, this one '
    'asks the reverse question &mdash; <strong>given the response you want, what circuit produces it?</strong> '
    'That is network synthesis, and its main practical use is <strong>filter design</strong>.</p>'
    + sec('Learning Outcomes', [
        'Describe a network by its <strong>driving-point and transfer functions</strong>, poles and zeros.',
        'Test whether a function is realisable as a passive network and <strong>synthesise LC one-port '
        'networks</strong> (Foster and Cauer forms).',
        'Synthesise simple <strong>LC two-port networks</strong> such as ladder filters.',
        'Choose a filter <strong>approximation</strong> (Butterworth, Chebyshev, elliptic, Bessel) to meet a '
        'magnitude or delay specification, and find its order.',
        'Design <strong>active filters</strong> with operational amplifiers (Sallen-Key, multiple-feedback, '
        'state-variable) and scale them in frequency and impedance.',
        'Explain how <strong>switched-capacitor filters</strong> work and why they suit integrated circuits.'],
        [
        'Analyse the sensitivity of a filter to component tolerance.',
        'Verify designs in circuit simulation.'])
    + sec('Major Topics', [
        'Network functions, poles and zeros, positive-real functions.',
        'Synthesis of LC one-ports: Foster and Cauer realisations.',
        'Two-port parameters and LC ladder synthesis.',
        'Filter approximations and frequency transformations.',
        'Operational-amplifier applications and active RC filters.',
        'Switched-capacitor filters.'],
        [
        'Sensitivity and tolerance analysis.',
        'Computer-aided filter design.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul(
        'A network-synthesis or filter-design text, for example <em>Design of Analog Filters</em>, Schaumann, '
        'Xiao and Van Valkenburg (Oxford), or Van Valkenburg\'s <em>Analog Filter Design</em>.',
        'MATLAB (Signal Processing Toolbox) or Python (SciPy) for approximations and responses.',
        'A SPICE simulator such as LTspice; filter-design tools from Texas Instruments or Analog Devices.')
    + '<h2>Career Pathways</h2>'
    + ul(
        '<strong>Analog and mixed-signal circuit designer</strong> (electronics engineers, SOC 17-2072).',
        '<strong>Communications and RF hardware engineer</strong>: filters set what a receiver hears.',
        '<strong>Audio, instrumentation and sensor-interface design</strong>.',
        'Graduate study in circuits and systems.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>FAMU and FSU both carry it at 3 credits</strong>, and it is one course at the joint College. '
    'Neither publishes contact hours; the 45 shown are derived from Florida\'s convention of 15 per credit for '
    'a lecture course.</p>'
    '<h3>An older number</h3>'
    '<p>The number has been on the state file since the late 1980s and was last changed in 2006, and no other '
    'Florida public university carries it. Most programmes now teach filter design inside signals, electronics '
    'or communications courses instead. Check the College\'s schedule for the term you want it.</p>'
    '<h3>Prerequisite</h3>'
    '<p>The College lists <strong>EEL3135 Signals and Linear System Analysis</strong>. Laplace transforms, '
    'transfer functions and frequency response from that course are used from the first week.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools and filter-design software can produce a filter in seconds. The course is about knowing why '
    'that design works and when it will not: a generated circuit may use unrealistic component values, ignore '
    'op-amp bandwidth, or quote the wrong formula for a filter type. <strong>Check every design by simulation '
    'and by hand at a few frequencies</strong>, and follow your instructor\'s policy on AI use.</p>'
)

EEL4113 = {
    'title': 'Advanced Linear Networks',
    'html_content': EEL4113_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4113_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'FAMU and FSU, both at 3 credits: one course taught by the joint FAMU-FSU College of '
                   'Engineering.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [off('FAMU', FAMU, 'Advanced Linear Networks', 3, 'Joint FAMU-FSU College. Prerequisite EEL3135.'),
                      off('FSU', FSU, 'Advanced Linear Networks', 3, 'Joint FAMU-FSU College. Prerequisite EEL3135.')],
    },
}

# --------------------------------------------------------------------------
# EEL4206L Electromechanical Energy System Lab -- USF
# --------------------------------------------------------------------------
EEL4206L_PRE = ('USF, the only carrier: EGN3374 Introduction to Electrical Systems II (minimum grade C), and '
                'EGN3375 Electromechanical Systems taken before or at the same time (minimum grade C). Majors '
                'restrictions may apply; check USF\'s schedule.')

EEL4206L_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4206L Electromechanical Energy System Lab</strong> is a 1-credit electrical engineering '
    'laboratory taught by <strong>one Florida public institution, the University of South Florida</strong>. '
    'USF describes it as providing <em>"hands-on experience related to Electric Mechanical Conversion '
    'Systems."</em></p>'
    '<p>It is the laboratory for USF\'s <strong>EGN3375 Electromechanical Systems</strong>, which covers '
    '<em>"transformers, transducers, DC motors and generators, AC motors and alternators."</em> In the lab '
    'students connect, run and test those machines: they measure how a transformer behaves under load, start '
    'and control motors, and run generators.</p>'
    '<p>USF publishes only the one-line description, so the outcomes and topics below follow the lecture '
    'course\'s content and the standard machines-lab experiments. Check the lab manual for your term.</p>'
    + sec('Learning Outcomes', [
        'Work safely with <strong>high-current and rotating equipment</strong>: lockout, guarding, and safe '
        'wiring and measurement.',
        'Perform <strong>open-circuit and short-circuit tests</strong> on a transformer and find its equivalent '
        'circuit, regulation and efficiency.',
        'Test <strong>DC machines</strong> as motors and generators and measure torque-speed behaviour.',
        'Test <strong>three-phase induction motors</strong> (no-load and locked-rotor tests) and relate the '
        'results to the equivalent circuit.',
        'Run a <strong>synchronous machine</strong> as a generator and observe excitation and power factor.',
        'Measure three-phase power and write reports that compare measurement with theory.'],
        [
        'Control motor speed with a variable-frequency drive.',
        'Synchronise a generator to the supply.'])
    + sec('Major Topics', [
        'Laboratory safety for power equipment.',
        'Single- and three-phase power measurement.',
        'Transformers: tests, equivalent circuit, efficiency.',
        'DC motors and generators.',
        'Induction motors: tests and torque-speed curves.',
        'Synchronous generators and motors.'],
        [
        'Variable-frequency drives and power electronics.',
        'Transducers and sensors for speed and torque.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul(
        'The EGN3375 text, typically <em>Electric Machinery Fundamentals</em>, Chapman (McGraw-Hill), or '
        'Fitzgerald and Kingsley\'s <em>Electric Machinery</em>.',
        'USF\'s laboratory manual and machine sets (motor-generator stations, power analysers).',
        'Safety: NFPA 70E is the U.S. standard for electrical safety in the workplace.')
    + '<h2>Career Pathways</h2>'
    + POWER_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: the University of South Florida, at 1 credit.</strong> USF publishes no '
    'contact-hour figure; the 45 hours shown follow the convention this site uses for a 1-credit engineering '
    'laboratory (one three-hour session a week). The number dates from 2017 at USF and was last changed in '
    '2024.</p>'
    '<h3>Take it with EGN3375</h3>'
    '<p>USF lists <strong>EGN3375 Electromechanical Systems</strong> as a co-prerequisite: it may be taken '
    'before the lab or in the same term, and the experiments follow its topics. Most students take the two '
    'together. The lecture does not require the lab, so check whether your degree plan needs it.</p>'
    '<h3>Same subject, other numbers</h3>'
    '<p>Other Florida universities number their machines laboratory differently: FAMU-FSU teach '
    '<strong>EEL4217L Power and Energy Lab</strong>, and FIU <strong>EEL4213L Energy Conversion Lab</strong>. '
    'The subject is close, but SCNS equivalence does not cross numbers, so bring the lab manual if you '
    'transfer.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain machine theory and help process data. They cannot tell you whether a circuit is '
    'safe to energise. <strong>Never wire or energise power equipment on the strength of a generated answer</strong>; '
    'follow the lab manual and the instructor. Reports must use your own data, under your instructor\'s '
    'policy on AI use.</p>'
)

EEL4206L = {
    'title': 'Electromechanical Energy System Lab',
    'html_content': EEL4206L_HTML,
    'credits': 1,
    'contact_hours': 45,
    'prerequisites': EEL4206L_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, the University of South Florida, at 1 credit.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED_LAB,
        'offerings': [off('USF', USF, 'Electromechanical Energy System Lab', 1,
                          'Prerequisite EGN3374 (C); EGN3375 before or with it (C).')],
    },
}

# --------------------------------------------------------------------------
# EEL4210 Smart Distribution Systems -- UWF
# --------------------------------------------------------------------------
EEL4210_PRE = ('UWF, the only carrier: EEL3211 Basic Electric Energy Engineering (which needs EEL3111 with a C). '
               'Offered together with graduate EEL5291: graduate students do extra work, and taking this '
               'version may affect taking EEL5291 for credit later at UWF; ask before registering.')

EEL4210_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4210 Smart Distribution Systems</strong> is an upper-division power engineering course taught '
    'by <strong>one Florida public institution, the University of West Florida</strong>, at 3 credits. UWF '
    'describes it as covering <em>"theory and practical application methods available in the industry for the '
    'protection of distribution systems and includes smart grid applications for protection and control,"</em> '
    'with <em>"a broad range of topics related to developments and trends in smart distribution technologies '
    'including automatic restoration, data management, cybersecurity, interoperability and standards, and '
    'future vision."</em></p>'
    '<p>The <strong>distribution system</strong> is the part of the grid that runs from the substation to '
    'customers. It is where most outages happen and where solar panels, batteries and electric-vehicle '
    'chargers connect, so it is changing fastest. The course covers how distribution circuits are protected '
    'from faults and how sensors, communications and automation now let a utility find a fault and restore '
    'service automatically.</p>'
    + sec('Learning Outcomes', [
        'Describe the structure of a distribution system: substations, feeders, laterals and service.',
        'Calculate fault currents and apply <strong>protective devices</strong> &mdash; relays, reclosers, '
        'sectionalisers and fuses &mdash; and coordinate them.',
        'Explain <strong>fault location, isolation and service restoration (FLISR)</strong> and other '
        'distribution automation.',
        'Describe smart-grid sensing and communication, from smart meters to SCADA and distribution management '
        'systems.',
        'Identify <strong>cybersecurity</strong> risks to grid control systems and the standards that address '
        'them.',
        'Explain how <strong>interoperability standards</strong> (for example IEC 61850 and IEEE 1547) let '
        'equipment and distributed energy resources work together.'],
        [
        'Analyse the effect of rooftop solar and batteries on protection and voltage.',
        'Use distribution analysis software for a protection study.'])
    + sec('Major Topics', [
        'Distribution system structure and components.',
        'Fault calculation and overcurrent protection.',
        'Protective device coordination.',
        'Distribution automation and automatic restoration.',
        'Smart-grid data and communications.',
        'Cybersecurity of grid control systems.',
        'Standards and interoperability; future trends.'],
        [
        'Distributed energy resources and microgrids.',
        'Storm hardening and reliability indices (SAIDI, SAIFI).'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul(
        '<em>Electric Power Distribution System Engineering</em>, Gonen (CRC), or <em>Electric Power '
        'Distribution Handbook</em>, Short (CRC).',
        'Standards worth knowing by name: <strong>IEEE 1547</strong> (interconnection of distributed energy '
        'resources), <strong>IEC 61850</strong> (substation communication), <strong>NERC CIP</strong> '
        '(critical infrastructure protection).',
        'Distribution analysis software such as OpenDSS (free), CYME or ETAP.')
    + '<h2>Career Pathways</h2>'
    + POWER_CAREERS
    + ul('Gulf Power, now part of Florida Power &amp; Light, serves the Pensacola area where UWF is, and '
         'Florida\'s hurricane exposure keeps distribution automation and storm hardening in demand.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: the University of West Florida, at 3 credits.</strong> UWF publishes no '
    'contact hours; the 45 shown are derived from Florida\'s convention of 15 per credit for a lecture course. '
    'The number was added in 2021.</p>'
    '<h3>Taught with a graduate course</h3>'
    '<p>UWF offers it <strong>concurrently with EEL5291</strong>: undergraduate and graduate students share the '
    'classroom and graduate students do extra work. If you may continue to a UWF master\'s degree, ask whether '
    'taking EEL4210 stops you from taking EEL5291 for credit later.</p>'
    '<h3>Prerequisite</h3>'
    '<p>UWF requires <strong>EEL3211 Basic Electric Energy Engineering</strong> (transformers and machines). '
    'No other Florida public university carries this number; utility distribution is taught at USF as '
    'EEL4214 <em>Electric (Utility) Distribution Systems</em>.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI is already used in distribution operations, for outage prediction, fault location and load '
    'forecasting, and the course\'s cybersecurity topic applies to it too. Chat tools are unreliable on '
    'protection settings and on what a specific standard requires: they invent clause numbers and settings. '
    '<strong>Take settings from calculations and standards from the standard itself</strong>, and follow your '
    'instructor\'s policy on AI use.</p>'
)

EEL4210 = {
    'title': 'Smart Distribution Systems',
    'html_content': EEL4210_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4210_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, the University of West Florida, at 3 credits.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [off('UWF', UWF, 'Smart Distribution Systems', 3,
                          'Prerequisite EEL3211. Offered concurrently with graduate EEL5291.')],
    },
}

# --------------------------------------------------------------------------
# EEL4212 -- two subjects: USF Energy Delivery Systems / FIU High Voltage Engineering
# --------------------------------------------------------------------------
EEL4212_PRE = ('Depends on the school, because the number carries two different subjects. USF (Energy Delivery '
               'Systems): EEL4241 Power Electronics; majors only. FIU (High Voltage Engineering): EEL3110C '
               'Circuit Analysis and EEL4213 Power Systems I. *** Check which course your school teaches '
               'before you plan around it.')

EEL4212_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4212</strong> is an upper-division power engineering number carried by <strong>two Florida '
    'public universities, at 3 credits each &mdash; and they teach two different subjects under it.</strong> '
    'The statewide title is <em>Distributed Energy Delivery Systems</em>.</p>'
    '<table class="table table-sm"><thead><tr><th>School</th><th>Its title</th><th>What it teaches</th></tr></thead><tbody>'
    '<tr><td>University of South Florida</td><td>Energy Delivery Systems</td><td>the power delivery system and '
    'how distributed energy resources such as solar are integrated into it &mdash; <strong>matches the '
    'statewide title</strong></td></tr>'
    '<tr><td>Florida International University</td><td>High Voltage Engineering</td><td>high-voltage engineering '
    'and the measurements used to characterise electrical insulation</td></tr>'
    '</tbody></table>'
    '<h3>USF: Energy Delivery Systems</h3>'
    '<p>USF: <em>"The course provides the students the fundamentals and analysis of the electric power delivery '
    'system to facilitate the integration of distributed energy resources, e.g. solar energy."</em> Its '
    'prerequisite is <strong>EEL4241 Power Electronics</strong>, the technology that connects solar panels and '
    'batteries to the grid.</p>'
    '<h3>FIU: High Voltage Engineering</h3>'
    '<p>FIU: <em>"Introduction to concepts of high voltage engineering, various measurements used in '
    'characterizing electrical insulation materials and systems for power engineering applications."</em> Its '
    'prerequisites are circuit analysis and <strong>EEL4213 Power Systems I</strong>. FIU moved this course to '
    'the number in 2022.</p>'
    '<p>Both are power engineering electives, but they share little content, so the outcomes and topics below '
    'are labelled by school.</p>'
    + '<h2>Learning Outcomes</h2>'
    '<h3>Required Outcomes &mdash; USF, Energy Delivery Systems</h3>'
    + li('Describe the structure of transmission and distribution systems.',
         'Model feeders and calculate power flow and voltage drop.',
         'Analyse how <strong>distributed energy resources</strong> (solar, batteries) change voltage, power '
         'flow and protection.',
         'Apply interconnection requirements such as <strong>IEEE 1547</strong>.')
    + '<h3>Required Outcomes &mdash; FIU, High Voltage Engineering</h3>'
    + li('Describe how high voltages are <strong>generated and measured</strong> in the laboratory (AC, DC and '
         'impulse).',
         'Explain <strong>breakdown</strong> in gases, liquids and solids and the factors that govern it.',
         'Describe tests that characterise <strong>insulation</strong>: dielectric loss, partial discharge, '
         'withstand and impulse tests.',
         'Relate insulation coordination and lightning to the design of power equipment.')
    + '<h3>Optional Outcomes</h3>'
    + li('USF: use power-flow software to study a feeder with high solar penetration.',
         'FIU: follow a high-voltage laboratory test procedure and its safety rules.')
    + '<h2>Major Topics</h2>'
    '<h3>Required Topics &mdash; USF</h3>'
    + li('Transmission and distribution system structure.', 'Feeder models, power flow and voltage regulation.',
         'Inverter-based resources and their grid integration.', 'Interconnection standards and hosting capacity.')
    + '<h3>Required Topics &mdash; FIU</h3>'
    + li('Generation and measurement of high voltages.', 'Electric fields and breakdown mechanisms.',
         'Insulating materials and their testing.', 'Overvoltages, lightning and insulation coordination.')
    + '<h3>Optional Topics</h3>'
    + li('USF: microgrids and storage.', 'FIU: cables, bushings and outdoor insulators.')
    + '<h2>Resources &amp; Tools</h2>'
    + ul('USF reading: <em>Power System Analysis and Design</em>, Glover, Overbye and Sarma (Cengage), and '
         'IEEE 1547; software such as OpenDSS (free).',
         'FIU reading: <em>High Voltage Engineering: Fundamentals</em>, Kuffel, Zaengl and Kuffel (Newnes).',
         'Standards: IEEE 1547 (distributed resources); IEEE Std 4 (high-voltage test techniques).')
    + '<h2>Career Pathways</h2>'
    + POWER_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>One number, two subjects</h3>'
    '<p>⚠ <strong>A transfer evaluator matching on the number alone cannot tell these two courses apart.</strong> '
    'A student with FIU\'s high-voltage course has not studied distributed-energy integration, and the reverse. '
    'If you transfer with EEL4212, send the syllabus and say which subject it was. USF holds the reading that '
    'matches the statewide title.</p>'
    '<h3>Offering Notes</h3>'
    '<p><strong>Both carriers list it at 3 credits</strong> and neither publishes contact hours; the 45 shown are '
    'derived from Florida\'s convention of 15 per credit for a lecture course.</p>'
    '<h3>Part of a scrambled family</h3>'
    '<p>The power numbers EEL4212&ndash;EEL4215 do not mean the same thing across Florida. EEL4213 is '
    '<em>Power Systems I</em> at FAMU, FIU and FSU but industrial power distribution at USF and protection and '
    'control at UCF; EEL4214 is <em>Power Systems II</em> at FIU but utility distribution at USF. Read each '
    'school\'s description, not the number.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain concepts and help with calculations. On both subjects they are weakest on '
    'specifics: test voltages, clearances and interconnection limits are set by standards that a model will '
    'misquote. <strong>Take numbers from the standard and the data sheet</strong>, and follow your instructor\'s '
    'policy on AI use.</p>'
)

EEL4212 = {
    'title': 'Distributed Energy Delivery Systems (USF) / High Voltage Engineering (FIU)',
    'html_content': EEL4212_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4212_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'Two public carriers, both at 3 credits, teaching two different subjects: USF Energy Delivery '
                   'Systems (matches the statewide title) and FIU High Voltage Engineering.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [off('USF', USF, 'Energy Delivery Systems', 3, 'Prerequisite EEL4241. Majors only.'),
                      off('FIU', FIU, 'High Voltage Engineering', 3,
                          'Prerequisites EEL3110C and EEL4213. On this number since 2022.')],
    },
}

# --------------------------------------------------------------------------
# EEL4213L Energy Conversion Lab -- FIU
# --------------------------------------------------------------------------
EEL4213L_PRE = ('FIU, the only carrier: taken with or after EEL4213 Power Systems I, FIU\'s machines course. '
                'FIU\'s catalogue record does not print the prerequisite; check FIU\'s schedule or your '
                'adviser before registering.')

EEL4213L_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4213L Energy Conversion Lab</strong> is a 1-credit electrical engineering laboratory taught '
    'by <strong>one Florida public institution, Florida International University</strong>. FIU describes it '
    'as: <em>"Operation, testing, and applications of energy conversion machines including AC and DC motors and '
    'generators. Experiments on magnetic circuits and transformers."</em> FIU offers it in fall, spring and '
    'summer.</p>'
    '<p>It is the laboratory for FIU\'s <strong>EEL4213 Power Systems I</strong>, which at FIU is a course on '
    'power system components: <em>"transformers, induction machines, synchronous machines, direct current '
    'machines, and special machines."</em></p>'
    '<p>⚠ The state course file spells the title <em>Energy Convergance Lab</em>; FIU\'s own title is '
    '<em>Energy Conversion Lab</em>, which is what the course is.</p>'
    + sec('Learning Outcomes', [
        'Work safely with power and rotating equipment.',
        'Measure the behaviour of <strong>magnetic circuits</strong>: flux, saturation and hysteresis.',
        'Test <strong>transformers</strong> (open- and short-circuit tests) and find their equivalent circuit, '
        'regulation and efficiency.',
        'Operate and test <strong>DC motors and generators</strong>.',
        'Operate and test <strong>AC induction and synchronous machines</strong> as motors and generators.',
        'Write reports that compare measured performance with theory.'],
        [
        'Control machine speed with power-electronic drives.',
        'Measure three-phase power and power factor correction.'])
    + sec('Major Topics', [
        'Laboratory safety.',
        'Magnetic circuits.',
        'Single- and three-phase transformers.',
        'DC machines.',
        'Induction machines.',
        'Synchronous machines.'],
        ['Special machines (stepper, permanent-magnet) and drives.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('The EEL4213 text, typically <em>Electric Machinery Fundamentals</em>, Chapman (McGraw-Hill).',
         'FIU\'s laboratory manual and machine stations.',
         'NFPA 70E for electrical safety in the workplace.')
    + '<h2>Career Pathways</h2>'
    + POWER_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: Florida International University, at 1 credit.</strong> FIU publishes no '
    'contact-hour figure; the 45 hours shown follow the convention this site uses for a 1-credit engineering '
    'laboratory. The course has been on FIU\'s books since 2005.</p>'
    '<h3>The lecture-and-lab pair</h3>'
    '<p>EEL4213 and EEL4213L are the lecture and laboratory halves of FIU\'s machines course. Register for both '
    'if your degree plan lists both; taken together they complete the same thing as a combined lecture-and-lab '
    'course elsewhere.</p>'
    '<h3>⚠ EEL4213 means different things at different schools</h3>'
    '<p>At FIU, EEL4213 <em>Power Systems I</em> is about machines. At FAMU and FSU, EEL4213 <em>Power Systems '
    'I</em> is about power-flow and fault analysis; at USF it is industrial power distribution; at UCF, '
    'protection and control; at UWF, electric energy systems. <strong>This laboratory belongs with FIU\'s '
    'machines course.</strong> The nearest laboratories elsewhere are USF\'s EEL4206L and FAMU-FSU\'s EEL4217L, '
    'under different numbers.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain machine theory and help process data, but they cannot tell you whether a circuit '
    'is safe to energise. <strong>Follow the lab manual and the instructor, never a generated answer, when wiring '
    'power equipment.</strong> Reports must use your own data, under your instructor\'s policy on AI use.</p>'
)

EEL4213L = {
    'title': 'Energy Conversion Lab',
    'html_content': EEL4213L_HTML,
    'credits': 1,
    'contact_hours': 45,
    'prerequisites': EEL4213L_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, Florida International University, at 1 credit.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED_LAB,
        'offerings': [off('FIU', FIU, 'Energy Conversion Lab', 1,
                          'State file spells it "Energy Convergance Lab". Laboratory for FIU EEL4213 (machines). '
                          'Offered fall, spring and summer.')],
    },
}

# --------------------------------------------------------------------------
# EEL4214 -- FIU Power Systems II / USF Electric (Utility) Distribution Systems
# --------------------------------------------------------------------------
EEL4214_PRE = ('Depends on the school, because the number carries two different courses. FIU (Power Systems '
               'II): follows EEL4213 Power Systems I; FIU\'s record does not print the prerequisite. USF '
               '(Electric Utility Distribution Systems): EGN3375 Electromechanical Systems and EEL4213 '
               'Industrial Power Distribution 1; majors only. *** Check which course your school teaches.')

EEL4214_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4214</strong> is an upper-division power engineering number carried by <strong>two Florida '
    'public universities at 3 credits each, which teach two different courses under it.</strong> The statewide '
    'title is <em>Electric Energy Power Systems II</em>.</p>'
    '<table class="table table-sm"><thead><tr><th>School</th><th>Its title</th><th>What it teaches</th></tr></thead><tbody>'
    '<tr><td>Florida International University</td><td>Power Systems II</td><td>transmission lines, load flow '
    'and economic dispatch &mdash; the <strong>second course of a power systems analysis sequence</strong>, '
    'matching the statewide title</td></tr>'
    '<tr><td>University of South Florida</td><td>Electric (Utility) Distribution Systems</td><td>the design and '
    'calculation of utility distribution systems</td></tr>'
    '</tbody></table>'
    '<h3>FIU: Power Systems II</h3>'
    '<p>FIU: <em>"Transmission line models, the bus admittance matrix, load flow studies and solution techniques, '
    'economic dispatch with and without losses, and computer applications related to power system '
    'operations."</em> It sits between FIU\'s EEL4213 Power Systems I (machines) and EEL4215 Power Systems III '
    '(faults and stability). FIU offers it in spring and fall.</p>'
    '<h3>USF: Electric (Utility) Distribution Systems</h3>'
    '<p>USF: <em>"Familiarizes the student with electric utility power distribution systems. Modeling loads; '
    'distribution transformers; subtransmission lines, substations, and distribution primary and secondary; '
    'power system calcs, voltage regulation, protection methods."</em> It follows USF\'s EEL4213 Industrial '
    'Power Distribution 1.</p>'
    + '<h2>Learning Outcomes</h2>'
    '<h3>Required Outcomes &mdash; FIU, Power Systems II</h3>'
    + li('Model <strong>transmission lines</strong> (short, medium and long) and calculate their parameters.',
         'Build the <strong>bus admittance matrix</strong> of a network.',
         'Formulate and solve the <strong>load-flow (power-flow) problem</strong> by Gauss-Seidel and '
         'Newton-Raphson methods.',
         'Solve <strong>economic dispatch</strong> with and without transmission losses.',
         'Use power-system software to study an operating network.')
    + '<h3>Required Outcomes &mdash; USF, Utility Distribution</h3>'
    + li('Model <strong>loads</strong> and estimate demand for a distribution system.',
         'Size and connect <strong>distribution transformers</strong>.',
         'Analyse subtransmission lines, substations and primary and secondary distribution circuits.',
         'Calculate voltage drop and apply <strong>voltage regulation</strong> (regulators, capacitors).',
         'Apply distribution <strong>protection methods</strong>.')
    + '<h3>Optional Outcomes</h3>'
    + li('FIU: optimal power flow and unit commitment.', 'USF: reliability indices and distributed generation.')
    + '<h2>Major Topics</h2>'
    '<h3>Required Topics &mdash; FIU</h3>'
    + li('Transmission line models.', 'Network matrices.', 'Load-flow formulation and solution.',
         'Economic dispatch.', 'Computer methods for power system operation.')
    + '<h3>Required Topics &mdash; USF</h3>'
    + li('Load characteristics and modelling.', 'Distribution transformers.', 'Subtransmission and substations.',
         'Primary and secondary circuits.', 'Voltage regulation.', 'Protection.')
    + '<h3>Optional Topics</h3>'
    + li('Software for power-flow and distribution analysis (PowerWorld, OpenDSS, ETAP, CYME).')
    + '<h2>Resources &amp; Tools</h2>'
    + ul('FIU reading: <em>Power System Analysis and Design</em>, Glover, Overbye and Sarma (Cengage), or '
         '<em>Power System Analysis</em>, Grainger and Stevenson (McGraw-Hill).',
         'USF reading: <em>Distribution System Modeling and Analysis</em>, Kersting (CRC), or <em>Electric Power '
         'Distribution System Engineering</em>, Gonen (CRC).',
         'Software: PowerWorld Simulator (free educational version), MATLAB, OpenDSS (free).')
    + '<h2>Career Pathways</h2>'
    + POWER_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>One number, two courses</h3>'
    '<p>⚠ <strong>A transfer evaluator matching on the number cannot tell these apart.</strong> FIU\'s course is '
    'transmission-level analysis (load flow and dispatch); USF\'s is distribution design. Both are core power '
    'engineering and both appear on the FE and PE Power exams, but they do not cover the same topics. Send the '
    'syllabus with any transfer request.</p>'
    '<h3>Offering Notes</h3>'
    '<p><strong>Both carriers list it at 3 credits</strong>; neither publishes contact hours, so the 45 shown are '
    'derived from Florida\'s convention of 15 per credit for a lecture course.</p>'
    '<h3>Part of a scrambled family</h3>'
    '<p>The EEL4212&ndash;EEL4215 power numbers mean different things at different universities. FIU runs a '
    'three-course sequence (EEL4213 machines, EEL4214 load flow, EEL4215 faults and stability). FAMU-FSU teach '
    'power-flow and faults together in their EEL4213; USF\'s EEL4213 and EEL4214 are industrial and utility '
    'distribution. Read each description.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain methods and help write a power-flow or dispatch script. They make errors that are '
    'hard to see: per-unit bases mixed up, admittance signs wrong, an iteration that "converges" to a wrong '
    'answer. <strong>Check results against a commercial or open-source solver and against a power balance</strong>, '
    'and follow your instructor\'s policy on AI use.</p>'
)

EEL4214 = {
    'title': 'Power Systems II (FIU) / Electric Utility Distribution Systems (USF)',
    'html_content': EEL4214_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4214_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'Two public carriers, both at 3 credits, teaching two different courses: FIU Power Systems II '
                   '(load flow and dispatch) and USF Electric (Utility) Distribution Systems.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [off('FIU', FIU, 'Power Systems II', 3, 'Transmission lines, load flow, economic dispatch. '
                          'Spring and fall.'),
                      off('USF', USF, 'Electric (Utility) Distribution Systems', 3,
                          'Prerequisites EGN3375 and EEL4213. Majors only.')],
    },
}

# --------------------------------------------------------------------------
# EEL4215 Power Systems III -- FIU
# --------------------------------------------------------------------------
EEL4215_PRE = ('FIU, the only carrier: follows EEL4214 Power Systems II (load flow) in FIU\'s three-course power '
               'sequence. FIU\'s record does not print the prerequisite; check FIU\'s schedule or your adviser.')

EEL4215_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4215 Power Systems III</strong> is the third course of the power systems sequence at '
    '<strong>Florida International University</strong>, the only Florida public institution that carries the '
    'number, at 3 credits. FIU describes it as: <em>"Short circuit calculations, symmetrical and unsymmetrical '
    'fault analysis, transient stability and dynamic studies as well as power system control. Computer '
    'applications."</em> FIU offers it in fall, spring and summer.</p>'
    '<p>Where Power Systems II studies the grid in normal operation, this course studies what happens when '
    'something goes wrong: a short circuit, the loss of a line, or a generator swinging out of step. Those '
    'calculations set the ratings of breakers and the settings of protective relays, and they decide whether '
    'the grid stays together after a fault.</p>'
    + sec('Learning Outcomes', [
        'Calculate <strong>symmetrical (three-phase) fault</strong> currents using the bus impedance matrix.',
        'Apply <strong>symmetrical components</strong> and sequence networks.',
        'Calculate <strong>unsymmetrical faults</strong>: single line-to-ground, line-to-line and double '
        'line-to-ground.',
        'Use the results to choose circuit breaker ratings and to explain protective relaying.',
        'Analyse <strong>transient stability</strong> with the swing equation and the equal-area criterion.',
        'Describe frequency and voltage control of a power system and run stability studies on a computer.'],
        [
        'Model generator excitation and governor controls.',
        'Use commercial power-system software for fault and stability studies.'])
    + sec('Major Topics', [
        'Per-unit system and network matrices (review).',
        'Symmetrical faults.',
        'Symmetrical components and sequence networks.',
        'Unsymmetrical faults.',
        'Power system stability: swing equation, equal-area criterion, numerical solution.',
        'Power system control: load-frequency and voltage control.'],
        ['Protective relaying principles.', 'Small-signal stability.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('<em>Power System Analysis and Design</em>, Glover, Overbye and Sarma (Cengage), or <em>Power System '
         'Analysis</em>, Grainger and Stevenson (McGraw-Hill).',
         'MATLAB/Simulink; PowerWorld Simulator; PSS/E or ETAP where available.',
         'IEEE Std C37 series (circuit breakers and relays) and IEEE Std 399 (power system analysis).')
    + '<h2>Career Pathways</h2>'
    + POWER_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: Florida International University, at 3 credits.</strong> FIU publishes no '
    'contact hours; the 45 shown are derived from Florida\'s convention of 15 per credit for a lecture '
    'course.</p>'
    '<h3>FIU\'s three-course sequence</h3>'
    '<p>FIU spreads power systems over three courses: <strong>EEL4213</strong> (machines and components), '
    '<strong>EEL4214</strong> (transmission lines, load flow, dispatch) and <strong>EEL4215</strong> (faults, '
    'stability, control). Other Florida universities cover fault analysis and stability in a single power '
    'systems course under other numbers &mdash; at FAMU-FSU, for example, it is part of their EEL4213. So '
    'EEL4215 has no partner elsewhere: transfer it with a syllabus.</p>'
    '<h3>FE and PE exams</h3>'
    '<p>Fault calculation, symmetrical components and stability are on the FE Electrical and Computer exam and '
    'are central to the PE Power exam.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain symmetrical components or the equal-area criterion, and help write a simulation. '
    'They often mix up sequence-network connections for a fault type or get transformer phase shifts wrong. '
    '<strong>Check fault currents against a hand calculation and a solver</strong>, and follow your instructor\'s '
    'policy on AI use.</p>'
)

EEL4215 = {
    'title': 'Power Systems III',
    'html_content': EEL4215_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4215_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, Florida International University, at 3 credits.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [off('FIU', FIU, 'Power Systems III', 3,
                          'Third course of FIU\'s power sequence. Fall, spring and summer.')],
    },
}

# --------------------------------------------------------------------------
# EEL4217L Power and Energy Lab -- FAMU, FSU
# --------------------------------------------------------------------------
EEL4217L_PRE = ('FAMU-FSU College of Engineering: EEL3216 Fundamentals of Power Systems (energy conversion, '
                'transformers, rotating machines, transmission lines).')

EEL4217L_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4217L Power and Energy Lab</strong> is a 1-credit electrical engineering laboratory taught '
    'by <strong>Florida A&amp;M University and Florida State University</strong>.</p>'
    + JOINT +
    '<p>The College describes it as: <em>"intended to give the student practical experience with motors, '
    'generators, transformers and power system instrumentation equipment. Students learn the principles of '
    'electromechanical energy conversion by connecting, operating, and controlling induction, synchronous, and '
    'dc machines. Transport of electrical energy through transmission lines is also explored."</em></p>'
    + sec('Learning Outcomes', [
        'Work safely with power and rotating equipment.',
        'Use <strong>power system instrumentation</strong>: power analysers, current and voltage transformers.',
        'Test <strong>transformers</strong> and determine their equivalent circuit and efficiency.',
        'Connect, operate and control <strong>induction, synchronous and DC machines</strong>.',
        'Study <strong>energy transport through transmission lines</strong>: voltage drop, losses and reactive '
        'power, on a line model.',
        'Write reports that compare measured results with theory.'],
        ['Synchronise a generator to the supply.', 'Use a variable-frequency drive.'])
    + sec('Major Topics', [
        'Laboratory safety.',
        'Power measurement and instrumentation.',
        'Transformers.',
        'Induction machines.',
        'Synchronous machines.',
        'DC machines.',
        'Transmission line models.'],
        ['Power-electronic drives.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('The EEL3216 text and the College\'s laboratory manual; <em>Electric Machinery Fundamentals</em>, '
         'Chapman (McGraw-Hill), is a standard reference.',
         'Machine stations, transmission-line simulators and power analysers.',
         'NFPA 70E for electrical safety in the workplace.')
    + '<h2>Career Pathways</h2>'
    + POWER_CAREERS
    + ul('In Tallahassee, the City of Tallahassee Utilities and the National High Magnetic Field Laboratory '
         'employ power engineers, and the College hosts the Center for Advanced Power Systems (CAPS).')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>FAMU and FSU both carry it at 1 credit</strong>, as one course at the joint College. Neither '
    'publishes contact hours; the 45 shown follow the convention this site uses for a 1-credit engineering '
    'laboratory. The number was last changed in 2024&ndash;2025.</p>'
    '<h3>Prerequisite</h3>'
    '<p>The College lists <strong>EEL3216 Fundamentals of Power Systems</strong>: energy conversion, power '
    'system structure, transformers, rotating machines and transmission lines. Unlike many laboratories it is '
    'not tied to a lecture taken in the same term.</p>'
    '<h3>Same subject, other numbers</h3>'
    '<p>USF\'s <strong>EEL4206L</strong> and FIU\'s <strong>EEL4213L</strong> are machines laboratories under '
    'other numbers. This one adds transmission lines. SCNS equivalence does not cross numbers, so bring the lab '
    'manual if you transfer.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain machine theory and help process data, but they cannot tell you whether a circuit '
    'is safe to energise. <strong>Follow the lab manual and the instructor, never a generated answer, when '
    'wiring power equipment.</strong> Reports must use your own data, under your instructor\'s policy on AI '
    'use.</p>'
)

EEL4217L = {
    'title': 'Power and Energy Lab',
    'html_content': EEL4217L_HTML,
    'credits': 1,
    'contact_hours': 45,
    'prerequisites': EEL4217L_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'FAMU and FSU, both at 1 credit: one laboratory taught by the joint FAMU-FSU College of '
                   'Engineering.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED_LAB,
        'offerings': [off('FAMU', FAMU, 'Power and Energy Lab', 1, 'Joint FAMU-FSU College. Prerequisite EEL3216.'),
                      off('FSU', FSU, 'Power and Energy Lab', 1, 'Joint FAMU-FSU College. Prerequisite EEL3216.')],
    },
}

# --------------------------------------------------------------------------
# EEE4351 Solid-State Electronic Devices -- FAMU, FSU
# --------------------------------------------------------------------------
EEE4351_PRE = ('FAMU-FSU College of Engineering: EEE3300 Electronics and EEE3300L Electronics Laboratory. '
               'Calculus-based physics and differential equations are assumed.')

EEE4351_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEE4351 Solid-State Electronic Devices</strong> is an upper-division electrical engineering '
    'elective taught by <strong>Florida A&amp;M University and Florida State University</strong>, both at 3 '
    'credits.</p>'
    + JOINT +
    '<p>The College describes it as covering <em>"solid-state physics as applied to electronic devices. The '
    'course focuses on semiconductor materials, conduction process in solids, device fabrication, diffusion '
    'processes, and negative conduction devices."</em> Where Electronics treats a transistor as a circuit '
    'element with a model, this course explains <strong>why the device behaves as it does</strong>: energy '
    'bands, electrons and holes, doping, and how a pn junction, a bipolar transistor and a MOSFET work '
    'inside.</p>'
    + sec('Learning Outcomes', [
        'Describe crystal structure and <strong>energy bands</strong> in semiconductors.',
        'Calculate carrier concentrations using the Fermi level, with and without <strong>doping</strong>.',
        'Analyse carrier transport by <strong>drift and diffusion</strong>, and generation and '
        'recombination.',
        'Explain the <strong>pn junction</strong> in equilibrium and under bias, and derive its current-voltage '
        'relationship.',
        'Explain the operation of <strong>bipolar transistors and MOSFETs</strong> from device physics.',
        'Describe the main <strong>fabrication</strong> steps, including diffusion and ion implantation.'],
        [
        'Describe <strong>negative-resistance devices</strong> (tunnel diodes, Gunn devices), which the College '
        'lists.',
        'Describe optoelectronic devices: LEDs, photodiodes and solar cells.'])
    + sec('Major Topics', [
        'Crystal structure and quantum basics.',
        'Energy bands and carrier statistics.',
        'Drift, diffusion and continuity.',
        'The pn junction.',
        'Bipolar junction transistors.',
        'MOS capacitors and MOSFETs.',
        'Fabrication and diffusion processes.'],
        ['Negative-conductance devices.', 'Optoelectronic devices.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('<em>Semiconductor Physics and Devices</em>, Neamen (McGraw-Hill), or <em>Solid State Electronic '
         'Devices</em>, Streetman and Banerjee (Pearson).',
         'MATLAB or Python for band diagrams and device curves.',
         'Device simulators such as the free tools on nanoHUB.org.')
    + '<h2>Career Pathways</h2>'
    + ul('<strong>Semiconductor device and process engineer</strong> (electronics engineers, SOC 17-2072).',
         '<strong>Semiconductor processing technician</strong> roles in Florida pay above the national median: '
         'the state has a growing chip industry, including NeoCity in Osceola County and SkyWater Technology '
         'in Kissimmee.',
         '<strong>Graduate study</strong> in microelectronics, photonics or materials.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>FAMU and FSU both carry it at 3 credits</strong>, as one course at the joint College. Neither '
    'publishes contact hours; the 45 shown are derived from Florida\'s convention of 15 per credit for a lecture '
    'course. On the state file since 2008.</p>'
    '<h3>Prerequisite and preparation</h3>'
    '<p>The College requires <strong>EEE3300 Electronics and its laboratory EEE3300L</strong>. The course uses '
    'more physics than most electrical engineering courses; review modern physics (the electron as a wave, '
    'energy levels) before it starts.</p>'
    '<h3>Related courses</h3>'
    '<p>The College also teaches <strong>EEE4330 Microelectronics Engineering</strong> (fabrication) and '
    'EEE4313 digital integrated-circuit design. Other Florida universities teach device physics under other '
    'numbers, and SCNS equivalence does not cross numbers, so transfer it with a syllabus.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools are useful for explaining band diagrams and checking derivations. They often give wrong '
    'numerical constants (intrinsic carrier concentration, mobilities) or mix up sign conventions for '
    'electrons and holes. <strong>Use values from your textbook\'s tables and check units</strong>, and follow '
    'your instructor\'s policy on AI use.</p>'
)

EEE4351 = {
    'title': 'Solid-State Electronic Devices',
    'html_content': EEE4351_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEE4351_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'FAMU and FSU, both at 3 credits: one course taught by the joint FAMU-FSU College of '
                   'Engineering.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [off('FAMU', FAMU, 'Solid State Electronic Devices', 3,
                          'Joint FAMU-FSU College. Prerequisites EEE3300 and EEE3300L.'),
                      off('FSU', FSU, 'Solid-State Electronic Devices', 3,
                          'Joint FAMU-FSU College. Prerequisites EEE3300 and EEE3300L.')],
    },
}

ALL = (('EEL4119L', EEL4119L), ('EEL4113', EEL4113), ('EEL4206L', EEL4206L), ('EEL4210', EEL4210),
       ('EEL4212', EEL4212), ('EEL4213L', EEL4213L), ('EEL4214', EEL4214), ('EEL4215', EEL4215),
       ('EEL4217L', EEL4217L), ('EEE4351', EEE4351))

for cid, g in ALL:
    path = os.path.join(DRAFTS, '%s_guide.json' % cid)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(g, fh, ensure_ascii=False, indent=1)
    print('wrote', cid, len(g['html_content']), 'chars; prereq', len(g['prerequisites']))
