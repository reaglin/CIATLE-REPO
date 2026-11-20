#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Batch 245 -- scheduled request check 2026-11-20: EEL4205 and EEL4664.

Requests in rank order were EEL2130C, EEL4205, ETI0602, EEL4664. Two were
skipped for Ron (REVIEW_QUEUE 124, 125):

  EEL2130C  Florida Poly's only record has a discontinued twin (dt 2025-07-11),
            the course is on no 2025-26 Florida Poly flowchart, and no
            description could be read anywhere (catalog content-blocked, SCNS
            403 this session). Publish, or decline as no longer taught?
  ETI0602   The CPALMS framework for Industrial Technology (I150603, CIP
            15.0612) is TERMINATED -- daggered 2023-24, last reportable year
            2024-25 -- and Manatee Tech, the only carrier, no longer lists it.
            Is a terminated programme's course a decline reason?

So EEL4664 (rank 4) was taken up as the third course.

Sources:
  EEL4205  UCF Kuali 2026-2027 undergraduate catalogue (description, prereq
           with grade, Fall/Spring, labStudioFieldWorkHours 0); UCF ECE
           Power & Renewable Energy track flowchart, Fall 2026 catalog.
  EEL4664  Florida Poly B.S. EE flowchart 2025-2026 (last modified
           03/21/2025): Robotics concentration list. Catalog course page not
           readable (acalog, empty 202) -- the description and prerequisite
           are NOT confirmed, and the guide says so.
  Both     SCNS flat file (Sep 2025) for carriers, titles, dates.
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


# --------------------------------------------------------------------------
# EEL4205 Electric Machinery -- UCF
# --------------------------------------------------------------------------
EEL4205_PRE = ('UCF, the only carrier: EEL3004C Linear Circuits I with a minimum grade of C. '
               'UCF offers it in Fall and Spring only. It sits on the Power & Renewable Energy '
               'track as a senior elective, beside EEL4216 Fundamentals of Electric Power Systems; '
               'EEL3123C Linear Circuits II and EGN3420 Engineering Analysis are not required for '
               'it but make the AC and phasor work much easier.')

EEL4205_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4205 Electric Machinery</strong> is an upper-division electrical engineering course '
    'taught by <strong>one Florida public institution, the University of Central Florida</strong>, at '
    '3 credits. UCF\'s catalogue describes it in one line: <em>"Fundamentals of DC and AC electric '
    'machines."</em> In practice that means the devices that convert between electrical and mechanical '
    'energy &mdash; <strong>transformers</strong>, <strong>DC machines</strong>, <strong>induction '
    'motors</strong> and <strong>synchronous generators and motors</strong> &mdash; and the magnetic '
    'circuits and energy-conversion principles underneath all of them.</p>'
    '<p>Because only UCF teaches this number, this guide describes UCF\'s course. UCF publishes a short '
    'description, so the outcomes and topics below are the standard content of a first course in '
    'electric machines, as set out in the textbooks named under Resources. Treat them as the expected '
    'shape of the course and check the syllabus for the term you take it.</p>'
    '<p>At UCF it is a <strong>senior elective on the Power &amp; Renewable Energy track</strong> of the '
    'B.S. in Electrical Engineering (Fall 2026 catalogue flowchart), alongside EEL4216 Fundamentals of '
    'Electric Power Systems, EEL4294 Introduction to Smart Grid and approved graduate power courses. '
    'UCF\'s catalogue lists <strong>0 laboratory hours</strong>: it is a lecture course, and it is '
    'offered <strong>Fall and Spring only</strong>, so plan around the summer gap.</p>'
    '<p>The statewide (SCNS) title for <strong>EEL x205</strong> is <em>Electrical Machinery</em>. '
    'Other Florida universities teach the same subject under different numbers &mdash; see '
    'Special Information.</p>'
    + sec('Learning Outcomes', [
        'Analyse <strong>magnetic circuits</strong>: reluctance, flux, flux linkage, inductance, and '
        'the effects of saturation, hysteresis and eddy-current loss in ferromagnetic cores.',
        'Model a single-phase and three-phase <strong>transformer</strong> with its equivalent circuit, '
        'refer quantities between windings, and compute voltage regulation and efficiency from '
        'open-circuit and short-circuit test data.',
        'Explain <strong>electromechanical energy conversion</strong> from energy and co-energy, and '
        'derive force and torque in simple singly and doubly excited systems.',
        'Analyse <strong>DC machines</strong> (separately excited, shunt, series, compound) as motors '
        'and generators: EMF and torque equations, speed control, and torque&ndash;speed '
        'characteristics.',
        'Model a three-phase <strong>induction motor</strong> with its per-phase equivalent circuit; '
        'compute slip, torque, power flow, losses and efficiency; and explain starting and speed '
        'control.',
        'Analyse a <strong>synchronous machine</strong> as a generator and as a motor with the '
        'synchronous-reactance model and phasor diagrams, including power angle, excitation control '
        'and power-factor correction.',
        'Use per-unit quantities and nameplate data to solve practical machine problems.'],
        [
        'Describe how <strong>power-electronic drives</strong> (rectifiers, choppers, inverters, '
        'variable-frequency drives) control DC and AC machines.',
        'Introduce <strong>permanent-magnet</strong>, brushless DC, stepper and switched-reluctance '
        'machines, especially as used in electric vehicles and robotics.',
        'Relate machine behaviour to the power system: generator capability, parallel operation, '
        'and motor loads on a distribution feeder.'])
    + sec('Major Topics', [
        'Review of three-phase circuits, phasors, real, reactive and apparent power.',
        'Magnetic circuits and magnetic materials; core losses.',
        'Transformers: ideal and real, equivalent circuit, tests, per-unit system, autotransformers, '
        'three-phase connections.',
        'Principles of electromechanical energy conversion; rotating magnetic fields.',
        'DC machines: construction, commutation, characteristics, starting and speed control.',
        'Induction machines: construction, equivalent circuit, torque&ndash;speed curve, NEMA design '
        'classes, starting methods.',
        'Synchronous machines: generator operation, voltage regulation, synchronous motors, '
        'capability curves.'],
        [
        'Variable-frequency drives and motor control.',
        'Single-phase induction motors.',
        'Permanent-magnet and brushless machines; machines for electric vehicles and wind turbines.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul(
        '<em>Electric Machinery Fundamentals</em>, Stephen J. Chapman (McGraw-Hill) &mdash; the most '
        'widely used undergraduate text for this course.',
        '<em>Fitzgerald &amp; Kingsley\'s Electric Machinery</em>, Umans (McGraw-Hill) &mdash; the '
        'classic, more theoretical treatment.',
        '<em>Principles of Electric Machines and Power Electronics</em>, P. C. Sen (Wiley) &mdash; '
        'strong on drives.',
        'MATLAB/Simulink (with Simscape Electrical) for torque&ndash;speed curves and machine '
        'simulation; UCF provides MATLAB to its students.',
        'Standards worth knowing by name: <strong>NEMA MG 1</strong> (motors and generators), '
        '<strong>IEEE Std 112</strong> (testing polyphase induction motors), <strong>IEEE Std '
        '115</strong> (testing synchronous machines), the <strong>IEEE C57</strong> transformer '
        'series, and <strong>NFPA 70 (National Electrical Code) Article 430</strong> on motors.')
    + '<h2>Career Pathways</h2>'
    + ul(
        '<strong>Electrical engineer, power</strong> (SOC 17-2071) at Florida utilities &mdash; Florida '
        'Power &amp; Light, Duke Energy Florida, Tampa Electric and the Orlando Utilities Commission '
        '&mdash; working on generation, substations and motor loads.',
        '<strong>Generator and turbine engineering</strong>: Orlando is a centre for the power '
        'generation industry, including Siemens Energy\'s large Orlando operation.',
        '<strong>Motor, drive and electric-vehicle engineering</strong>: traction motors, inverters '
        'and motor control.',
        '<strong>Industrial and facilities engineering</strong>: motor selection, protection and '
        'energy efficiency in plants, theme parks, hospitals and water utilities.',
        '<strong>Power systems consulting</strong> and design for the <strong>PE Power</strong> '
        'licence, where rotating machines and transformers are a major part of the exam.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: the University of Central Florida, at 3 credits.</strong> UCF does '
    'not publish contact hours; its catalogue lists 0 laboratory hours, so the 45 hours shown here are '
    'derived from Florida\'s convention of 15 contact hours per credit for a lecture course. Offered '
    'Fall and Spring only.</p>'
    '<h3>Prerequisites and preparation</h3>'
    '<p>UCF requires <strong>EEL3004C Linear Circuits I with a grade of C or better</strong>. That is '
    'the minimum. A machines course runs on AC steady-state analysis, phasors and three-phase power, '
    'so students who have also taken <strong>EEL3123C Linear Circuits II</strong> usually find it '
    'easier. Come comfortable with complex numbers, phasor diagrams and basic electromagnetics '
    '(PHY2049 Physics II).</p>'
    '<h3>The same subject under other numbers in Florida</h3>'
    '<p>No other public institution carries EEL4205, but several teach electric machines under '
    'another number. Credit between them is <strong>not</strong> automatic, because the numbers do not '
    'match; bring a syllabus if you transfer:</p>'
    + ul(
        '<strong>EEL4220 Electric Machines</strong> &mdash; University of North Florida (3 credits); '
        'Florida Atlantic University carries the number as <em>Electrical Machines</em> at 2 credits. '
        'The statewide title for EEL x220 is <em>Electromechanics I</em>.',
        '<strong>EEL4224 Electric Machines and Drives</strong> &mdash; University of South Florida, '
        'with a graduate counterpart EEL6227.',
        '<strong>EEL3211 Electric Machines and Energy Conversion</strong> &mdash; Florida Polytechnic '
        'University (statewide title <em>Basic Electric Energy Engineering</em>; a guide is live for '
        'EEL3211).',
        '<strong>EET4513L Electrical Machinery Lab</strong> &mdash; Florida A&amp;M, the laboratory '
        'side of the subject in an engineering technology programme.')
    + '<h3>Time commitment</h3>'
    '<p>Expect 8&ndash;10 hours a week outside class. The difficulty is less the mathematics than '
    'keeping the models straight: each machine has its own equivalent circuit, sign conventions and '
    'phasor diagram, and the homework is long, multi-step numerical work.</p>'
    '<h3>FE and PE exam relevance</h3>'
    '<p>The NCEES <strong>FE Electrical and Computer</strong> exam includes power topics such as '
    'transformers, three-phase power and rotating machines, and the <strong>PE Electrical and Computer: '
    'Power</strong> exam gives rotating machines and transformers substantial weight. This course is '
    'the main preparation for both in a power-track curriculum.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI assistants can explain a concept such as slip or armature reaction in another way, check '
    'algebra, and help write MATLAB scripts that plot torque&ndash;speed or efficiency curves. They are '
    'unreliable at the numerical problems this course is graded on: they often mix line and phase '
    'quantities, forget a factor of three or the square root of three in three-phase power, or use '
    'the wrong sign convention for motor and generator operation. <strong>Check every AI-produced '
    'number against a power balance</strong> (input = output + losses), and follow your instructor\'s '
    'policy on AI use for homework and exams.</p>'
)

EEL4205 = {
    'title': 'Electric Machinery',
    'html_content': EEL4205_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4205_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, the University of Central Florida, at 3 credits, Fall and '
                   'Spring only. UNF and FAU (EEL4220), USF (EEL4224) and Florida Poly (EEL3211) '
                   'teach electric machines under other numbers.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': "Florida's convention of 15 contact hours per credit for a lecture course; UCF "
                      'publishes 0 laboratory hours for EEL4205 and no contact-hour figure.',
        'offerings': [{
            'institution': 'UCF', 'institution_name': 'University of Central Florida',
            'title': 'Electric Machinery', 'credits': 3, 'contact_hours': None,
            'note': 'Senior elective, Power & Renewable Energy track of the B.S. in Electrical '
                    'Engineering. Fall and Spring only. Prerequisite EEL3004C, minimum grade C. '
                    'Catalogue: "Fundamentals of DC and AC electric machines."'}],
    },
}

# --------------------------------------------------------------------------
# EEL4664 Kinematics and Control of Robotic Systems -- Florida Poly
# --------------------------------------------------------------------------
EEL4664_PRE = ('Florida Poly, the only carrier: not confirmed (its online catalogue could not be read '
               'for this guide). Expect calculus III, differential equations, linear algebra and a '
               'controls background: on Florida Poly\'s B.S. EE flowchart it is a senior Robotics '
               'concentration elective beside EEL4612 Control System Design and EEL4660 Autonomous '
               'Robotic Systems. Check Florida Poly\'s catalogue for the exact prerequisite and grade '
               'before registering. *** The statewide title for EEL x664 is \'Autonomous Robotic '
               'Systems\', which Florida Poly teaches as EEL4660; send a syllabus on transfer.')

EEL4664_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4664 Kinematics and Control of Robotic Systems</strong> is an upper-division '
    'electrical engineering course taught by <strong>one Florida public institution, Florida '
    'Polytechnic University</strong> in Lakeland, at 3 credits. As its title says, it covers the two '
    'halves of making a robot arm do what you want: <strong>kinematics</strong> &mdash; the geometry '
    'that relates joint angles to where the tool is and how fast it moves &mdash; and '
    '<strong>control</strong> &mdash; the feedback that makes the joints follow a planned motion '
    'despite gravity, friction and load.</p>'
    '<p>⚠ <strong>Florida Poly\'s catalogue description could not be read for this guide</strong>: its '
    'online catalogue does not serve course pages to automated tools. The outcomes and topics below '
    'are the standard content of an undergraduate robot kinematics and control course, as set out in '
    'the textbooks named under Resources. Treat them as the expected shape of the course and check '
    'the syllabus for the term you take it.</p>'
    '<p>At Florida Poly it is one of five electives in the <strong>Robotics concentration</strong> of '
    'the B.S. in Electrical Engineering (2025&ndash;2026 flowchart), from which students choose four '
    '(12 credits): EEL4665 Autonomous Perception Systems, EEL4220 Electronic Motor Control, EEL4664, '
    'EEL4660 Autonomous Robotic Systems and EEL4612 Control System Design. It also counts toward the '
    'Advanced Topics option. The number entered the state course file in 2023.</p>'
    + sec('Learning Outcomes', [
        'Describe position and orientation with <strong>rotation matrices</strong>, Euler angles and '
        '<strong>homogeneous transformations</strong>, and compose frames.',
        'Assign frames with the <strong>Denavit&ndash;Hartenberg</strong> convention and derive the '
        '<strong>forward kinematics</strong> of serial manipulators.',
        'Solve the <strong>inverse kinematics</strong> of common arms analytically and numerically, '
        'and recognise multiple solutions and workspace limits.',
        'Derive the manipulator <strong>Jacobian</strong>, use it for velocity and static force '
        'analysis, and identify <strong>singularities</strong>.',
        'Plan joint-space and Cartesian <strong>trajectories</strong> (for example cubic and quintic '
        'polynomials).',
        'Design and simulate <strong>joint controllers</strong> (independent-joint PID) and explain '
        'how manipulator dynamics affect tracking.'],
        [
        'Derive manipulator dynamics with the <strong>Euler&ndash;Lagrange</strong> method and apply '
        'computed-torque (inverse-dynamics) control.',
        'Introduce force and impedance control for contact tasks.',
        'Program kinematics on a real or simulated robot, for example with ROS 2 or a robotics '
        'toolbox.',
        'Extend the methods to mobile robots: differential-drive kinematics and path following.'])
    + sec('Major Topics', [
        'Rigid motions and homogeneous transformations.',
        'Forward kinematics and the Denavit&ndash;Hartenberg convention.',
        'Inverse kinematics.',
        'Velocity kinematics, the Jacobian and singularities.',
        'Trajectory generation.',
        'Independent-joint control of DC-motor-driven joints.'],
        [
        'Manipulator dynamics (Lagrangian formulation).',
        'Computed-torque and multivariable control.',
        'Force control.',
        'Mobile-robot kinematics.',
        'Simulation and robot software (MATLAB, Python, ROS 2).'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul(
        '<em>Robot Modeling and Control</em>, Spong, Hutchinson and Vidyasagar (Wiley) &mdash; the '
        'standard text for this pairing of kinematics and control.',
        '<em>Introduction to Robotics: Mechanics and Control</em>, John J. Craig (Pearson).',
        '<em>Modern Robotics: Mechanics, Planning, and Control</em>, Lynch and Park (Cambridge) '
        '&mdash; free online with accompanying videos and code.',
        'MATLAB with the Robotics System Toolbox, or Peter Corke\'s Robotics Toolbox (MATLAB and '
        'Python); Gazebo and ROS 2 for simulation.',
        'Safety standards worth knowing by name: <strong>ISO 10218</strong> (industrial robots) and '
        '<strong>ISO/TS 15066</strong> (collaborative robots).')
    + '<h2>Career Pathways</h2>'
    + ul(
        '<strong>Robotics engineer</strong> and <strong>electrical engineer</strong> (SOC 17-2071) '
        'designing and programming robot arms, automated test and assembly cells.',
        '<strong>Controls and automation engineer</strong> in manufacturing, distribution and '
        'warehouse automation &mdash; a large employer around the I-4 corridor between Tampa and '
        'Orlando, where Lakeland sits.',
        '<strong>Defence and aerospace</strong> robotics and autonomous systems (Lockheed Martin, '
        'L3Harris and others in Florida).',
        '<strong>Medical robotics</strong> and rehabilitation devices.',
        'Graduate study in robotics, controls or mechatronics.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: Florida Polytechnic University, at 3 credits.</strong> Florida Poly '
    'does not publish contact hours, and the statewide record marks no laboratory, so the 45 hours '
    'shown here are derived from Florida\'s convention of 15 contact hours per credit for a lecture '
    'course. The University of Central Florida once carried EEL4664; that record was discontinued in '
    '2009.</p>'
    '<h3>⚠ The number carries a different statewide title</h3>'
    '<p>In Florida\'s Statewide Course Numbering System (SCNS), courses are matched on the prefix and '
    'the last three digits, and the statewide title for <strong>EEL x664</strong> is <em>Autonomous '
    'Robotic Systems</em>. Florida Poly teaches a separate course with that title as '
    '<strong>EEL4660</strong>, and titles EEL4664 <em>Kinematics and Control of Robotic Systems</em>. '
    'A receiving institution reading only the number may expect autonomy (perception, planning, '
    'navigation) rather than manipulator kinematics. <strong>If you transfer, take the syllabus.</strong></p>'
    '<h3>Prerequisites and preparation</h3>'
    '<p>Florida Poly\'s prerequisite could not be confirmed. Come in comfortable with '
    '<strong>linear algebra</strong> (matrices, rotations), <strong>differential equations</strong>, '
    'Laplace-domain feedback control and some programming in MATLAB or Python. Students who have '
    'taken a controls course such as EEL4652 Control Theory or EEL4612 Control System Design will '
    'find the control half much easier. Check Florida Poly\'s catalogue before registering.</p>'
    '<h3>Related courses elsewhere in Florida</h3>'
    '<p>No other public institution teaches this number, but robot kinematics and control is taught '
    'in mechanical engineering under <strong>EML4806</strong>: FIU as <em>Modeling and Control of '
    'Robots</em> and UNF as <em>Robotics Engineering</em>, both at 3 credits. Credit between different numbers is '
    'evaluated case by case.</p>'
    '<h3>Time commitment</h3>'
    '<p>Expect 8&ndash;12 hours a week outside class. Kinematic derivations are long and error-prone, '
    'and simulation assignments take time to debug.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI coding assistants are genuinely useful here for writing simulation code, plotting '
    'trajectories and setting up ROS 2 nodes. They are unreliable at the derivations: they mix '
    'Denavit&ndash;Hartenberg conventions (standard versus modified), transpose rotation matrices, and '
    'produce inverse-kinematics solutions that miss branches or fail near singularities. '
    '<strong>Verify every kinematic result numerically</strong> &mdash; run the forward kinematics on '
    'the inverse solution and check you get back the target pose. On real hardware, never run '
    'unverified AI-generated motion code on a robot without limits and an emergency stop. Follow your '
    'instructor\'s policy on AI use.</p>'
)

EEL4664 = {
    'title': 'Kinematics and Control of Robotic Systems',
    'html_content': EEL4664_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4664_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, Florida Polytechnic University, at 3 credits. The statewide '
                   'title for EEL x664 is Autonomous Robotic Systems, which Florida Poly teaches as '
                   'EEL4660. UCF carried EEL4664 until 2009.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': "Florida's convention of 15 contact hours per credit for a lecture course; Florida "
                      'Poly does not publish hours and the statewide record marks no laboratory.',
        'offerings': [{
            'institution': 'FLPOLY', 'institution_name': 'Florida Polytechnic University',
            'title': 'Kinematics and Control of Robotic Systems', 'credits': 3, 'contact_hours': None,
            'note': 'Robotics concentration elective of the B.S. in Electrical Engineering '
                    '(2025-2026 flowchart: choose four of EEL4665, EEL4220, EEL4664, EEL4660, EEL4612). '
                    'Description and prerequisite not confirmed (catalogue not readable).'}],
    },
}

for cid, g in (('EEL4205', EEL4205), ('EEL4664', EEL4664)):
    path = os.path.join(DRAFTS, '%s_guide.json' % cid)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(g, fh, ensure_ascii=False, indent=1)
    meta = {cid: {k: v for k, v in g.items() if k != 'html_content'}}
    with open(os.path.join(HERE, 'b245_%s_meta.json' % cid), 'w', encoding='utf-8') as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print('wrote', path, len(g['html_content']), 'chars; prereq', len(g['prerequisites']))
