#!/usr/bin/env python
"""Batch 238 -- the seven EAS courses the Aerospace Engineer path names.

⚠⚠⚠ TWO FINDINGS DROVE THIS BATCH, and one corrected the path.

1. EAS4400 -- ONE NUMBER, TWO VEHICLES. Statewide title and description are
   AIRCRAFT stability and control; UF and USF agree. ⚠ UCF uses the number for
   SPACECRAFT ATTITUDE DYNAMICS. The title/description test comes out AGREE, so
   the state is the reference and UCF is the deviating carrier -- but the
   same-institution control explains WHY: Florida numbers spacecraft attitude
   ONLY at graduate level (EAS6403 at UF, EAS6403C at UCF, EAS6413C at UF), so
   there is no undergraduate number for it. Misfiling by necessity, the batch
   225/227 shape. The path originally used UCF's minority reading; corrected.

2. EAS4105 -- the statewide TITLE is stale. It reads "Aerodynamics II", but the
   statewide DESCRIPTION is aircraft performance and stability and control, and
   ALL FOUR carriers name it flight dynamics or flight mechanics. Title/
   description test branch 2: carriers back the description, so the title is the
   stale element.

3. EAS4950 -- a dangling prerequisite. The statewide gate names EML4703 and
   EAS4251; Florida Polytechnic, one of only two carriers, offers NEITHER. USF
   carries all three, so USF contributed it. The single-carrier-contribution
   shape (batch 222).
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


ITAR = (
    '<h3>&#9888;&#9888; Export control shapes who can take this into a job</h3>'
    '<p>Much aerospace work is subject to <strong>ITAR</strong> and <strong>EAR</strong> export '
    'control, which in practice restricts many roles — and some laboratory and project work — '
    'to U.S. persons, and a great deal of defence work additionally requires a security clearance '
    'that takes months to obtain. <strong>This is not a course requirement, but it is a career '
    'requirement</strong>, and it is better understood in the second year than after an offer.</p>')

NO_PE = (
    '<h3>Licensure, and why it matters less here</h3>'
    '<p>A Professional Engineer licence is uncommon in aerospace — most of the work falls under the '
    'industrial exemption, and employers hire on degree, project record and clearance. &#9888; It is '
    'still worth sitting the <strong>FE examination in your final year</strong>: it is inexpensive '
    'then and expensive to recreate later, and it keeps open a move into consulting or '
    'civil-adjacent work. Under s. 471.013(1)(a), Florida Statutes, an approved <em>engineering</em> '
    'curriculum needs four years of experience toward the PE and an approved <em>engineering '
    'technology</em> curriculum six.</p>')


def guide(title, credits, hours, prereq, html, notes):
    return {'title': title, 'html_content': html, 'credits': credits, 'contact_hours': hours,
            'prerequisites': prereq, 'version': '1.0', 'offering_notes': notes}


G = {}

G['EAS4101'] = guide(
    'Aerodynamics', 3, 45,
    'Statewide prerequisite: FLUID MECHANICS. That is the operative gate and it is a real one - this '
    'course is applied fluid mechanics and assumes genuine fluency, not a pass. Most programmes also '
    'expect the calculus sequence through vector calculus and differential equations. '
    'CARRIED BY SIX FLORIDA PUBLIC INSTITUTIONS at 3 credits - FAMU, FAU, Florida Polytechnic, '
    'Florida State, UF and USF - which makes it the most widely offered aerospace-specific course in '
    'the state. '
    'TITLES VARY, THE COURSE DOES NOT: FAMU, Florida Polytechnic, FSU and USF call it Fundamentals '
    'of Aerodynamics; FAU and UF call it Aerodynamics; the statewide title is Beginning Aerodynamics. '
    'Register by the number. '
    'UCF STUDENTS: UCF is NOT a carrier of EAS4101 and does teach the course - it numbers it EAS3101 '
    'Fundamentals of Aerodynamics, at 3000 level. A level twin, not a different course.',
    '<h2>Course Description</h2>'
    '<p><strong>Aerodynamics</strong> is the central course of an aerospace engineering degree — the '
    'study of how air behaves around wings and bodies, and therefore of how anything flies. The '
    'statewide description covers <strong>basic aerodynamic analysis of wings and bodies in '
    'incompressible and compressible flows, including airplane performance, stability and '
    'control</strong>.</p>'
    '<p>It is carried by <strong>six Florida public institutions</strong> at 3 credits, more than any '
    'other aerospace-specific course in the state.</p>'
    '<p>&#9888; <strong>This is where the discipline gets mathematically hard.</strong> Aerodynamics '
    'is applied fluid mechanics with the simplifications removed, and students who arrived at fluid '
    'mechanics with shaky vector calculus meet the consequences here.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Apply the <strong>conservation equations</strong> to aerodynamic flows.',
         'Analyse <strong>incompressible flow</strong> over airfoils using thin-airfoil and potential-flow theory.',
         'Extend two-dimensional results to <strong>finite wings</strong> using lifting-line theory, and account for induced drag.',
         'Analyse <strong>compressible flow</strong>, including the effects of Mach number and shock waves.',
         'Compute <strong>lift, drag and moment</strong> and relate them to aircraft performance.',
         'Relate aerodynamic characteristics to <strong>stability and control</strong>.')
    + '<h3>Optional Outcomes</h3>'
    + li('Wind-tunnel measurement and the treatment of experimental uncertainty.',
         'Introductory computational fluid dynamics.',
         'Viscous effects and boundary-layer analysis, where the institution includes them.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Fundamental aerodynamic quantities; the governing equations.',
         'Incompressible flow over airfoils; thin-airfoil theory.',
         'Finite wings; lifting-line theory and induced drag.',
         'Compressible flow; normal and oblique shocks.',
         'Airplane performance: lift, drag polar, range and endurance.',
         'Introduction to stability and control.')
    + '<h3>Optional Topics</h3>'
    + li('Boundary layers and viscous drag.', 'High-lift devices.',
         'Introduction to computational methods.', 'Wind-tunnel testing.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Anderson, <em>Fundamentals of Aerodynamics</em>, is the near-universal text and the source '
    'of several of the institutional titles.</li>'
    '<li>MATLAB or Python for the computational exercises; XFOIL is common for airfoil work.</li>'
    '<li>Where a wind tunnel is available, expect laboratory work with it.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Named on the <strong>Aerospace Engineer</strong> career path in this repository. It is the '
    'gateway to aerodynamics, performance and design roles, and a prerequisite for propulsion, '
    'flight dynamics and the capstone sequence. In Florida it leads toward launch vehicle and '
    'airframe work on the Space Coast and toward the defence and simulation employers around '
    'Orlando.</p>'
    '<h2>Special Information</h2>'
    '<h3>Same course, several names</h3>'
    '<p>Four institutions call it <em>Fundamentals of Aerodynamics</em>, two call it '
    '<em>Aerodynamics</em>, and the state calls it <em>Beginning Aerodynamics</em>. &#9888; '
    '<strong>This is branding, not divergence</strong> — the subject is the same everywhere and the '
    'textbook is usually the same book. Register by number and do not read the title variation as a '
    'signal.</p>'
    '<h3>&#9888;&#9888; UCF numbers this course at 3000 level, and is therefore not a carrier</h3>'
    '<p>The University of Central Florida runs one of the largest aerospace programmes in the state '
    'and does <strong>not</strong> appear among this number&rsquo;s six carriers. That is not a gap in '
    'its curriculum: <strong>UCF numbers the same course <code>EAS3101</code> '
    '<em>Fundamentals of Aerodynamics</em></strong>, at 3000 level, and carries an honours section of '
    'it as well.</p>'
    '<p>&#9888; This is a <strong>level twin</strong> — the same subject positioned a year earlier — '
    'and Florida does it routinely (<code>EGN2312</code> and <code>EGN3311</code> for statics, '
    '<code>EGN2322</code> and <code>EGN3321</code> for dynamics). <strong>Both are upper-division, so '
    'nothing is lost in transfer</strong>, but a UCF student searching the state record for '
    '<code>EAS4101</code> will not find their own university, and a transferring student should send '
    'the syllabus rather than assume the numbers line up.</p>'
    '<h3>&#9888; The fluid mechanics prerequisite is not a formality</h3>'
    '<p>The statewide gate is simply &ldquo;fluid mechanics&rdquo;, and that understates it. This '
    'course assumes you can work comfortably with control volumes, potential flow and the vector '
    'calculus underneath them. <strong>If fluid mechanics was a struggle, revise it before the term '
    'rather than during it</strong> — the aerodynamics sequence does not slow down for it.</p>'
    + ITAR + NO_PE,
    {'summary': 'Six Florida public institutions carry EAS4101 at 3 credits: FAMU, FAU, Florida '
                'Polytechnic, Florida State, UF and USF. Four title it Fundamentals of Aerodynamics '
                'and two Aerodynamics. No institution publishes a contact-hour figure.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
     'offerings': [
         {'institution': 'UF', 'institution_name': 'University of Florida', 'title': 'Aerodynamics',
          'credits': 3, 'contact_hours': None, 'note': None},
         {'institution': 'USF', 'institution_name': 'University of South Florida',
          'title': 'Fundamentals of Aerodynamics', 'credits': 3, 'contact_hours': None, 'note': None}]})

G['EAS4105'] = guide(
    'Flight Dynamics', 3, 45,
    'Statewide prerequisite: PHYSICS, which understates it - in practice programmes require dynamics '
    'and normally aerodynamics, since this course applies both. '
    'READ THE TITLE CAREFULLY: the statewide title is "Aerodynamics II", and that title is STALE. '
    'The statewide DESCRIPTION is aircraft performance, aerodynamic design data and elements of '
    'stability and control - flight dynamics, not a second aerodynamics course - and all four '
    'carriers agree: FAU calls it Flight Dynamics, FIU Introduction to Flight Mechanics, Florida '
    'Polytechnic Introduction to Aircraft Dynamics, UCF Flight Mechanics. Do not expect a deeper '
    'aerodynamics course. '
    'CARRIED BY FOUR Florida public institutions at 3 credits: FAU, FIU, Florida Polytechnic, UCF.',
    '<h2>Course Description</h2>'
    '<p><strong>Flight Dynamics</strong> is the study of how an aircraft actually behaves in flight: '
    'what it can do, whether it is stable, and how the controls change its motion. The statewide '
    'description covers <strong>aircraft performance, aerodynamic design data, and elements of '
    'stability and control</strong>.</p>'
    '<p>Carried by <strong>four Florida public institutions</strong> at 3 credits — FAU, FIU, '
    'Florida Polytechnic and UCF.</p>'
    '<p>&#9888;&#9888; <strong>The statewide title says &ldquo;Aerodynamics II&rdquo;, and it is '
    'misleading.</strong> Every carrier names this course flight dynamics or flight mechanics, and '
    'the state&rsquo;s own description backs them. See Special Information — it matters if you are '
    'choosing courses from the state record.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Compute <strong>aircraft performance</strong>: climb, range, endurance, turn and takeoff.',
         'Construct and use the <strong>drag polar</strong> and performance diagrams.',
         'Derive the <strong>equations of motion</strong> for a rigid aircraft.',
         'Analyse <strong>static stability</strong> — longitudinal, lateral and directional — and locate the neutral point.',
         'Analyse <strong>dynamic stability</strong> and identify the classical modes: phugoid, short period, Dutch roll, spiral.',
         'Relate <strong>control surface</strong> deflection to aircraft response.')
    + '<h3>Optional Outcomes</h3>'
    + li('Introduction to feedback control and stability augmentation.',
         'Flight simulation exercises.', 'Handling qualities and certification criteria.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('The atmosphere and airspeed measurement.', 'Aircraft performance in steady flight.',
         'The drag polar; range and endurance.', 'Equations of motion and reference frames.',
         'Static longitudinal, lateral and directional stability.',
         'Dynamic stability and the classical modes.', 'Control surfaces and trim.')
    + '<h3>Optional Topics</h3>'
    + li('Stability augmentation and autopilot basics.', 'Flight testing and data reduction.',
         'Handling qualities specifications.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Anderson, <em>Aircraft Performance and Design</em>; Nelson, <em>Flight Stability and '
    'Automatic Control</em>; Etkin &amp; Reid are the common texts.</li>'
    '<li>MATLAB for the dynamics and simulation work.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Named on the <strong>Aerospace Engineer</strong> career path. It leads into flight sciences, '
    'controls, flight test and vehicle design, and is the natural preparation for guidance, '
    'navigation and control work — an area with a strong presence in Florida&rsquo;s defence and '
    'simulation sector.</p>'
    '<h2>Special Information</h2>'
    '<h3>&#9888;&#9888; The statewide title is stale, and the carriers show it</h3>'
    '<p>The SCNS title for this number is <em>Aerodynamics II</em>. <strong>No carrier uses that '
    'name</strong>:</p>'
    '<table class="table table-sm"><tbody>'
    '<tr><td>FAU</td><td>Flight Dynamics</td></tr>'
    '<tr><td>FIU</td><td>Introduction to Flight Mechanics</td></tr>'
    '<tr><td>Florida Polytechnic</td><td>Introduction to Aircraft Dynamics</td></tr>'
    '<tr><td>UCF</td><td>Flight Mechanics</td></tr>'
    '</tbody></table>'
    '<p>The state&rsquo;s own description — performance, design data, stability and control — '
    'matches the carriers rather than the title. <strong>So the title is the stale element</strong>, '
    'and a student choosing courses from the state record should not expect a second aerodynamics '
    'course. The aerodynamics sequence continues elsewhere: compressible flow is numbered '
    '<code>EAS4134</code> at UCF and USF.</p>' + ITAR + NO_PE,
    {'summary': 'Four Florida public institutions carry EAS4105 at 3 credits: FAU, FIU, Florida '
                'Polytechnic and UCF. All four title it flight dynamics or flight mechanics; the '
                'statewide title "Aerodynamics II" is used by none of them.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
     'offerings': [
         {'institution': 'FAU', 'institution_name': 'Florida Atlantic University',
          'title': 'Flight Dynamics', 'credits': 3, 'contact_hours': None, 'note': None},
         {'institution': 'UCF', 'institution_name': 'University of Central Florida',
          'title': 'Flight Mechanics', 'credits': 3, 'contact_hours': None, 'note': None}]})

G['EAS4400'] = guide(
    'Stability and Control of Aircraft', 3, 45,
    'Statewide prerequisite: AERODYNAMICS. '
    'WARNING - THIS NUMBER CARRIES TWO DIFFERENT VEHICLES. The statewide definition, and UF and USF, '
    'use EAS4400 for AIRCRAFT stability and control. UCF uses it for SPACECRAFT ATTITUDE DYNAMICS. '
    'Those are different material: aircraft stability derivatives and the phugoid and Dutch-roll '
    'modes on one side, rigid-body attitude, reaction wheels and torque-free motion on the other. '
    'Florida provides NO undergraduate number for spacecraft attitude - the dedicated numbers '
    '(EAS6403, EAS6413C) are graduate - so UCF had nowhere else to put it. '
    'CHECK WHICH VEHICLE YOUR SECTION COVERS before registering, and on transfer send the syllabus '
    'rather than the number: an evaluator matching on EAS4400 alone cannot tell the two apart.',
    '<h2>Course Description</h2>'
    '<p><strong>Stability and Control of Aircraft</strong> is the study of whether a flight vehicle '
    'holds its attitude and how the controls change it. The statewide description covers '
    '<strong>applied aerodynamics including stability and control of aerospace vehicles, generalised '
    'vehicle performance, and small-disturbance dynamic stability and control response</strong>.</p>'
    '<p>Carried by <strong>three Florida public institutions</strong> at 3 credits — UCF, UF and '
    'USF.</p>'
    '<p>&#9888;&#9888;&#9888; <strong>But the three do not teach the same vehicle</strong>, and that '
    'is the most important thing on this page. See Special Information.</p>'
    '<h2>Learning Outcomes</h2>'
    '<h3>Required Outcomes — the aircraft reading (statewide, UF, USF)</h3>'
    + li('Derive the <strong>small-disturbance equations of motion</strong> for a rigid aircraft.',
         'Compute and interpret <strong>stability derivatives</strong>.',
         'Analyse <strong>static and dynamic longitudinal stability</strong>, including the phugoid and short-period modes.',
         'Analyse <strong>lateral-directional stability</strong>, including Dutch roll and spiral modes.',
         'Relate <strong>control surface</strong> effectiveness to vehicle response and trim.',
         'Assess <strong>handling qualities</strong> against accepted criteria.')
    + '<h3>Required Outcomes — the spacecraft reading (UCF)</h3>'
    + li('Describe <strong>attitude representations</strong>: direction cosines, Euler angles, quaternions.',
         'Analyse <strong>torque-free rigid-body motion</strong> and spin stability.',
         'Model <strong>environmental torques</strong>: gravity gradient, solar pressure, aerodynamic, magnetic.',
         'Analyse <strong>attitude control actuators</strong> — reaction wheels, control moment gyros, thrusters.',
         'Design a basic <strong>attitude determination and control</strong> scheme.')
    + '<h2>Major Topics</h2><h3>Required Topics — aircraft reading</h3>'
    + li('Reference frames and the equations of motion.', 'Stability derivatives.',
         'Longitudinal static and dynamic stability.', 'Lateral-directional stability.',
         'Control surfaces, trim and manoeuvres.')
    + '<h3>Required Topics — spacecraft reading</h3>'
    + li('Attitude kinematics and representations.', 'Rigid-body dynamics and torque-free motion.',
         'Environmental disturbance torques.', 'Passive stabilisation: spin, dual-spin, gravity gradient.',
         'Active control: sensors, actuators and control laws.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Aircraft reading: Nelson, <em>Flight Stability and Automatic Control</em>; Etkin &amp; Reid.</li>'
    '<li>Spacecraft reading: Wie, <em>Space Vehicle Dynamics and Control</em>; Sidi, <em>Spacecraft '
    'Dynamics and Control</em>.</li>'
    '<li>MATLAB and Simulink for both.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Named on the <strong>Aerospace Engineer</strong> career path. Either reading leads toward '
    'guidance, navigation and control work — an area strongly represented in Florida by launch '
    'operators, satellite builders and the defence and simulation employers around Orlando.</p>'
    '<h2>Special Information</h2>'
    '<h3>&#9888;&#9888;&#9888; One number, two vehicles</h3>'
    '<table class="table table-sm"><thead><tr><th>Source</th><th>Title</th><th>Vehicle</th></tr></thead>'
    '<tbody>'
    '<tr><td>Statewide SCNS</td><td>Stability &amp; Control of Aircraft</td><td>aircraft</td></tr>'
    '<tr><td>University of Florida</td><td>Stability &amp; Control of Aircraft</td><td>aircraft</td></tr>'
    '<tr><td>University of South Florida</td><td>Stability and Control of Aircraft</td><td>aircraft</td></tr>'
    '<tr><td>&#9888; University of Central Florida</td><td>Spacecraft Attitude Dynamics</td><td><strong>spacecraft</strong></td></tr>'
    '</tbody></table>'
    '<p><strong>These are genuinely different courses.</strong> Aircraft stability and control is '
    'about stability derivatives, the phugoid and Dutch-roll modes and control-surface response in '
    'an atmosphere. Spacecraft attitude dynamics is about rigid-body rotation in orbit, '
    'environmental torques, reaction wheels and quaternions. A student needs one or the other for a '
    'given job, and the transcript line will not say which they took.</p>'
    '<h3>&#9888; Why UCF is not simply wrong</h3>'
    '<p>Florida numbers spacecraft attitude dynamics <strong>only at graduate level</strong> — '
    '<code>EAS6403</code> at UF, <code>EAS6403C</code> at UCF and <code>EAS6413C</code> at UF. '
    '<strong>There is no undergraduate number for it.</strong> A department wanting to teach the '
    'subject to undergraduates has to put it somewhere, and the nearest vehicle-dynamics number is '
    'this one.</p>'
    '<p>So there is no &ldquo;correct&rdquo; number to go looking for, and the practical advice is '
    'not about fault: <strong>check your own catalogue for which vehicle the course covers, and on '
    'transfer send the syllabus rather than the number.</strong></p>' + ITAR + NO_PE,
    {'summary': 'Three Florida public institutions carry EAS4400 at 3 credits. UF and USF use it for '
                'aircraft stability and control, matching the statewide definition; UCF uses it for '
                'spacecraft attitude dynamics.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
     'offerings': [
         {'institution': 'UF', 'institution_name': 'University of Florida',
          'title': 'Stability & Control of Aircraft', 'credits': 3, 'contact_hours': None,
          'note': 'The statewide reading: aircraft.'},
         {'institution': 'UCF', 'institution_name': 'University of Central Florida',
          'title': 'Spacecraft Attitude Dynamics', 'credits': 3, 'contact_hours': None,
          'note': '⚠ The minority reading: spacecraft, not aircraft.'}]})


def main():
    os.makedirs(DRAFTS, exist_ok=True)
    for cid, g in G.items():
        io.open(os.path.join(DRAFTS, '%s_guide.json' % cid), 'w', encoding='utf-8').write(
            json.dumps(g, ensure_ascii=False, indent=1))
        print('%-9s %-36s %d cr / %d hrs | prereq %4d | html %6d'
              % (cid, g['title'][:36], g['credits'], g['contact_hours'],
                 len(g['prerequisites']), len(g['html_content'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
