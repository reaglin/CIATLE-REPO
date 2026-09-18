#!/usr/bin/env python
"""Batch 238, part 2 -- the remaining four EAS courses.

Findings added in this half:

4. EAS4101 -- UCF IS MISSING FROM THE CARRIER LIST FOR A REASON. Six institutions
   carry EAS4101 and UCF is not one of them, because UCF numbers the same course
   EAS3101 "Fundamentals of Aerodynamics" at 3000 level. A LEVEL TWIN, the
   EGN2312/EGN3311 shape.

5. EAS4200 -- SPLIT FAMILY, and the STATE's own description is the tell. The
   statewide description ends "LECTURE, LAB, AND PROBLEM SOLVING SESSIONS" on a
   number carrying NO C and NO L suffix. UF resolves it by carrying a separate
   EAS4201L Aerospace Structures Laboratory; the other three carry the lab, if any,
   inside the 3-credit course. Surfaced from the statewide description rather than
   from a suffix.

6. EAS4505 -- the statewide prerequisite field is EMPTY, on a course that cannot
   be taken without dynamics and differential equations. The batch-189 shape
   inverted: there the description named a discipline the gate omitted; here the
   gate names nothing at all.

7. EAS4950 -- a SHELL NUMBER THAT HAS BECOME TITLED. x950 is on the skip list, and
   this one is exempt under the "has it become titled?" rule: both carriers name it
   Aerospace Capstone Design I, the statewide description is specific, and EAS4951
   exists as its second half at the same two institutions. Also carries the
   dangling prerequisite documented in b238_build.py.
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

G['EAS4200'] = guide(
    'Aerospace Structures', 3, 45,
    'Statewide prerequisite: DYNAMICS. In practice programmes also require mechanics of materials '
    '(EGN3331 or equivalent), which is the course this one actually builds on - the statewide gate '
    'names only half of what is needed. '
    'CARRIED BY FOUR Florida public institutions, all at 3 credits: FIU (Introduction to Design and '
    'Analysis of Aerospace Structures), UCF (Analysis and Design of Aerospace Structures), UF and USF '
    '(Aerospace Structures). Florida Polytechnic teaches the subject at 3000 level as EAS3200 '
    'Introduction to Aerospace Structures - a level twin, not a different course. '
    'WATCH THE LAB: the statewide description ends "lecture, lab, and problem solving sessions", but '
    'the number carries no C and no L suffix. UF packages the laboratory separately as EAS4201L; the '
    'other three carry whatever laboratory work they include inside the 3-credit course. Check which '
    'shape your institution uses BEFORE registering, or you may be one registration short.',
    '<h2>Course Description</h2>'
    '<p><strong>Aerospace Structures</strong> is where mechanics of materials meets the aircraft: the '
    'analysis of thin-walled, lightweight structures that carry flight loads with as little mass as '
    'possible. The statewide description covers <strong>types of flight structures, flight and '
    'dynamic loads, and bending and shear analysis of flight structures</strong>.</p>'
    '<p>Carried by <strong>four Florida public institutions</strong>, all at 3 credits.</p>'
    '<p>&#9888; <strong>Aerospace structures is not civil structures with different vocabulary.</strong> '
    'A building is designed with generous margins; an airframe is designed to be as light as it can '
    'be and still survive, which is why thin-walled theory, buckling and fatigue dominate the course '
    'and why the safety factors are small enough to be frightening.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Identify the <strong>structural elements of a flight vehicle</strong> — spars, ribs, '
         'stringers, skin, frames, longerons — and say what each one carries.',
         'Determine <strong>flight and ground loads</strong>, and construct and read a <strong>V-n '
         'diagram</strong>.',
         'Analyse <strong>bending of thin-walled beams</strong>, including unsymmetric sections.',
         'Compute <strong>shear flow</strong> in open and closed sections and locate the <strong>shear '
         'centre</strong>.',
         'Analyse <strong>torsion</strong> of thin-walled closed and multi-cell sections.',
         'Assess <strong>buckling and crippling</strong> of columns, plates and stiffened panels.')
    + '<h3>Optional Outcomes</h3>'
    + li('Introduction to finite element analysis of structures.',
         'Composite laminate analysis, where the institution includes it.',
         'Fatigue, damage tolerance and fail-safe design.',
         'Laboratory measurement with strain gauges and load frames.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Flight vehicle structural configurations and load paths.',
         'Flight loads, load factors and the V-n diagram.',
         'Unsymmetric bending of thin-walled beams.',
         'Shear flow, shear centre, and the idealised boom model.',
         'Torsion of single- and multi-cell closed sections.',
         'Column, plate and stiffened-panel buckling; crippling.')
    + '<h3>Optional Topics</h3>'
    + li('Composite materials and classical lamination theory.',
         'Introduction to the finite element method.',
         'Fatigue and damage tolerance.', 'Structural testing.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Megson, <em>Aircraft Structures for Engineering Students</em>, and Sun, <em>Mechanics of '
    'Aircraft Structures</em>, are the common texts; Bruhn is the classic reference.</li>'
    '<li>MATLAB for the analysis work; a finite element package (ANSYS, Abaqus or Nastran) where the '
    'course includes FEA.</li>'
    '<li>The FAA Federal Aviation Regulations Part 23 and Part 25 define the load cases the V-n '
    'diagram comes from, and are worth reading once.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Named on the <strong>Aerospace Engineer</strong> career path. Structures is one of the largest '
    'employment areas in aerospace and one of the most portable — the same analysis serves launch '
    'vehicles, airframes, satellites and pressure vessels. In Florida it leads toward the Space Coast '
    'launch and payload employers and toward airframe and structural work statewide.</p>'
    '<h2>Special Information</h2>'
    '<h3>&#9888;&#9888; The laboratory is packaged differently, and the state record says so</h3>'
    '<p>The statewide description ends <em>&ldquo;lecture, <strong>lab</strong>, and problem solving '
    'sessions&rdquo;</em> — on a number that carries no <code>C</code> and no <code>L</code>.</p>'
    '<table class="table table-sm"><thead><tr><th>Institution</th><th>Packaging</th></tr></thead>'
    '<tbody>'
    '<tr><td>University of Florida</td><td>3 credits, <strong>plus a separate '
    '<code>EAS4201L</code></strong> Aerospace Structures Laboratory</td></tr>'
    '<tr><td>FIU, UCF, USF</td><td>3 credits, any laboratory work carried inside the course</td></tr>'
    '</tbody></table>'
    '<p>&#9888; <strong>This is packaging, not divergence.</strong> Florida gives institutions leeway '
    'in how they split a course into registrations, and a lecture plus a separate lab is as complete '
    'as an integrated course. But it changes what you must register for and how many credits you end '
    'up with — <strong>so check your own catalogue rather than assuming the 3-credit course is the '
    'whole thing.</strong></p>'
    '<h3>Florida Polytechnic numbers it at 3000 level</h3>'
    '<p>Florida Polytechnic does not carry <code>EAS4200</code>; it carries <code>EAS3200</code> '
    '<em>Introduction to Aerospace Structures</em>. That is a <strong>level twin</strong> — the same '
    'subject positioned a year earlier in the curriculum — and it is a normal Florida pattern '
    '(compare <code>EGN2312</code> and <code>EGN3311</code> for statics). Both are upper-division, so '
    'the transfer exposure is small; the scheduling consequence is not, because the course sits in a '
    'different year of the degree plan.</p>'
    '<h3>&#9888; The prerequisite names dynamics; the course runs on mechanics of materials</h3>'
    '<p>The statewide gate is &ldquo;dynamics&rdquo;. <strong>The working prerequisite is mechanics '
    'of materials</strong> — stress, strain, bending, torsion and Mohr&rsquo;s circle — because this '
    'course is that material applied to thin-walled sections. Dynamics matters for the load cases. '
    '<strong>If mechanics of materials was a struggle, revise bending and shear before the term '
    'starts.</strong></p>' + ITAR + NO_PE,
    {'summary': 'Four Florida public institutions carry EAS4200, all at 3 credits: FIU, UCF, UF and '
                'USF. UF additionally carries a separate laboratory, EAS4201L. Florida Polytechnic '
                'teaches the subject at 3000 level as EAS3200. No institution publishes a '
                'contact-hour figure.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
     'offerings': [
         {'institution': 'UF', 'institution_name': 'University of Florida',
          'title': 'Aerospace Structures', 'credits': 3, 'contact_hours': None,
          'note': '⚠ Carries a separate laboratory, EAS4201L.'},
         {'institution': 'UCF', 'institution_name': 'University of Central Florida',
          'title': 'Analysis & Design of Aerospace Structures', 'credits': 3, 'contact_hours': None,
          'note': None},
         {'institution': 'FIU', 'institution_name': 'Florida International University',
          'title': 'Introduction to Design and Analysis of Aerospace Structures', 'credits': 3,
          'contact_hours': None, 'note': None},
         {'institution': 'USF', 'institution_name': 'University of South Florida',
          'title': 'Aerospace Structures', 'credits': 3, 'contact_hours': None, 'note': None}]})

G['EAS4300'] = guide(
    'Aerospace Propulsion', 3, 45,
    'Statewide prerequisite: THERMODYNAMICS. That is the real gate and it is the whole course - '
    'propulsion is applied thermodynamics and gas dynamics. Programmes normally expect fluid '
    'mechanics as well, and compressible flow is either a prerequisite or covered in the first weeks. '
    'CARRIED BY FOUR Florida public institutions at 3 credits, and THE TITLES TELL YOU WHAT EACH '
    'EMPHASISES: USF "Jet Propulsion" (air-breathing), UCF "Aerothermodynamics of Propulsion '
    'Systems", UF "Aerospace Propulsion", Florida Polytechnic "Principles of Flight Vehicle '
    'Propulsion". The statewide title is Propulsion Systems and its description covers BOTH '
    'air-breathing engines (turbojet, ramjet) AND rockets. '
    'CHECK THE BALANCE at your institution: a course weighted toward jet engines and one weighted '
    'toward rockets prepare for different employers, and on the Space Coast that difference matters.',
    '<h2>Course Description</h2>'
    '<p><strong>Aerospace Propulsion</strong> is the study of how flight vehicles are pushed: '
    'air-breathing engines that take their oxidiser from the atmosphere, and rockets that carry it. '
    'The statewide description covers <strong>supersonic diabatic flow, the turbojet, the ramjet, '
    'rocket performance criteria, rocket fuels, the design of liquid- and solid-fuelled rockets, and '
    'high-performance systems for aerospace propulsion</strong>.</p>'
    '<p>Carried by <strong>four Florida public institutions</strong>, all at 3 credits.</p>'
    '<p>&#9888; <strong>This is the most thermodynamics-intensive course in the aerospace '
    'curriculum.</strong> Cycle analysis is unforgiving of a shaky grasp of enthalpy, entropy and '
    'stagnation properties, and the compressible-flow relations arrive early and never leave.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Apply <strong>compressible flow</strong> relations — isentropic, normal shock, Rayleigh and '
         'Fanno — to propulsion flow paths.',
         'Analyse the <strong>ideal and real Brayton cycle</strong> and compute thrust, specific fuel '
         'consumption and efficiencies for a turbojet.',
         'Extend the analysis to the <strong>turbofan, turboprop and ramjet</strong>, and say where '
         'each is the right choice.',
         'Analyse <strong>inlets, compressors, combustors, turbines and nozzles</strong> as components.',
         'Compute <strong>rocket performance</strong>: specific impulse, characteristic velocity, '
         'thrust coefficient, and the rocket equation.',
         'Compare <strong>liquid, solid and hybrid</strong> rocket propellants and configurations.')
    + '<h3>Optional Outcomes</h3>'
    + li('Electric and advanced propulsion — ion, Hall-effect, nuclear thermal.',
         'Combustion chemistry and chemical equilibrium.',
         'Engine laboratory or test-stand measurement.',
         'Scramjets and hypersonic air-breathing propulsion.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Review of compressible flow and stagnation properties.',
         'Thrust equation and propulsive, thermal and overall efficiency.',
         'The Brayton cycle; turbojet cycle analysis, ideal and with losses.',
         'Turbofan, turboprop and ramjet cycles.',
         'Engine components: inlets, compressors, combustors, turbines, nozzles.',
         'Rocket fundamentals: the rocket equation, specific impulse, nozzle flow.',
         'Liquid and solid propellant systems.')
    + '<h3>Optional Topics</h3>'
    + li('Electric propulsion.', 'Combustion and propellant chemistry.',
         'Hypersonic and scramjet propulsion.', 'Engine testing and instrumentation.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Hill &amp; Peterson, <em>Mechanics and Thermodynamics of Propulsion</em>; Mattingly, '
    '<em>Elements of Propulsion</em>; Sutton &amp; Biblarz, <em>Rocket Propulsion Elements</em>, for '
    'the rocket half.</li>'
    '<li>MATLAB for cycle analysis; NASA CEA for chemical equilibrium and rocket performance; gas '
    'tables or their software equivalents throughout.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Named on the <strong>Aerospace Engineer</strong> career path, and in Florida it is close to a '
    'local specialism. The Space Coast is a launch-vehicle economy, and propulsion is the discipline '
    'that economy is built on — engines, propellant feed systems, test stands and launch operations. '
    'The air-breathing half leads toward engine manufacturers and toward the gas-turbine work that '
    'also appears in power generation.</p>'
    '<h2>Special Information</h2>'
    '<h3>&#9888; Jet engines or rockets? The titles say which way each institution leans</h3>'
    '<table class="table table-sm"><thead><tr><th>Institution</th><th>Its title</th><th>What the '
    'title signals</th></tr></thead><tbody>'
    '<tr><td>University of South Florida</td><td><strong>Jet Propulsion</strong></td><td>weighted '
    'toward air-breathing engines</td></tr>'
    '<tr><td>University of Central Florida</td><td>Aerothermodynamics of Propulsion Systems</td>'
    '<td>the thermodynamic analysis, both families</td></tr>'
    '<tr><td>University of Florida</td><td>Aerospace Propulsion</td><td>both families</td></tr>'
    '<tr><td>Florida Polytechnic</td><td>Principles of Flight Vehicle Propulsion</td><td>both '
    'families</td></tr>'
    '</tbody></table>'
    '<p>&#9888;&#9888; <strong>The statewide description promises both halves and one term is not '
    'much time for either.</strong> This is a difference of emphasis rather than of subject, and no '
    'institution is misdescribing its course — but a student aiming at launch-vehicle work should '
    'find out how many weeks go to rockets, and a student aiming at engines should ask the same '
    'question the other way round. <strong>Ask for the week-by-week schedule, not the title.</strong> '
    'Where the balance is wrong for your plans, the usual remedy is a technical elective: Florida '
    'numbers compressible flow separately as <code>EAS4134</code> (USF <em>Compressible Flow</em>, UCF '
    '<em>High-Speed Aerodynamics</em>).</p>' + ITAR + NO_PE,
    {'summary': 'Four Florida public institutions carry EAS4300 at 3 credits: Florida Polytechnic, '
                'UCF, UF and USF. All four use different titles, and USF’s ("Jet Propulsion") '
                'signals an air-breathing emphasis. No institution publishes a contact-hour figure.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
     'offerings': [
         {'institution': 'UF', 'institution_name': 'University of Florida',
          'title': 'Aerospace Propulsion', 'credits': 3, 'contact_hours': None, 'note': None},
         {'institution': 'USF', 'institution_name': 'University of South Florida',
          'title': 'Jet Propulsion', 'credits': 3, 'contact_hours': None,
          'note': '⚠ The title signals an air-breathing emphasis.'},
         {'institution': 'UCF', 'institution_name': 'University of Central Florida',
          'title': 'Aerothermodynamics of Propulsion Systems', 'credits': 3, 'contact_hours': None,
          'note': None},
         {'institution': 'FLPOLY', 'institution_name': 'Florida Polytechnic University',
          'title': 'Principles of Flight Vehicle Propulsion', 'credits': 3, 'contact_hours': None,
          'note': None}]})

G['EAS4505'] = guide(
    'Orbital Mechanics', 3, 45,
    'THE STATEWIDE PREREQUISITE FIELD IS EMPTY, and that is a data gap, not an open door. This course '
    'cannot be taken without dynamics (particle kinetics in three dimensions) and differential '
    'equations, and programmes gate it accordingly; vector calculus and comfort with numerical '
    'methods are assumed throughout. Read your own catalogue for the real gate. '
    'CARRIED BY FOUR Florida public institutions at 3 credits, under two names for one subject: FIU '
    '"Introduction to Astrodynamics" and USF "Astrodynamics"; UCF and Florida Polytechnic "Orbital '
    'Mechanics". ASTRODYNAMICS AND ORBITAL MECHANICS ARE THE SAME FIELD - register by the number. '
    'EXPECT TO PROGRAM: almost nothing in this course closes in a form you can evaluate by hand, and '
    'students who are weak in MATLAB or Python find it hard for reasons unrelated to orbits.',
    '<h2>Course Description</h2>'
    '<p><strong>Orbital Mechanics</strong> — equally called astrodynamics — is the motion of '
    'spacecraft under gravity, and how to change it. The statewide description covers the '
    '<strong>two-body problem, orbital equations, orbital transfer, and Earth satellite '
    'operation</strong>.</p>'
    '<p>Carried by <strong>four Florida public institutions</strong>, all at 3 credits.</p>'
    '<p>&#9888; <strong>It is the most mathematical course most aerospace students take</strong>, and '
    'the one whose results are least intuitive: spending fuel to slow down raises your orbit, and '
    'catching a satellite ahead of you means dropping behind it first.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Derive and apply the <strong>two-body equation of motion</strong> and the orbit equation.',
         'Classify orbits by <strong>conic section</strong> and compute their geometry and energy.',
         'Convert between <strong>position and velocity vectors and the six classical orbital '
         'elements</strong>, in both directions.',
         'Solve <strong>Kepler’s equation</strong> for time of flight, including the hyperbolic case.',
         'Design <strong>orbital transfers</strong>: Hohmann, bi-elliptic, plane change, and combined '
         'manoeuvres, and compute the &#916;v each costs.',
         'Analyse <strong>rendezvous</strong> and relative motion, and explain the phasing problem.',
         'Describe the principal <strong>perturbations</strong> — J2 oblateness, drag, third body, '
         'solar radiation pressure — and their operational consequences.')
    + '<h3>Optional Outcomes</h3>'
    + li('Interplanetary trajectories and the patched-conic method; gravity assists.',
         'Lambert’s problem and preliminary orbit determination.',
         'The restricted three-body problem and libration points.',
         'Numerical propagation and mission-design software.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('The two-body problem; conservation of energy and angular momentum.',
         'Conic-section orbits and orbit geometry.',
         'Classical orbital elements and coordinate frames.',
         'Kepler’s equation and time of flight.',
         'Impulsive manoeuvres; Hohmann and bi-elliptic transfers; plane changes.',
         'Rendezvous, phasing and relative motion.',
         'Orbital perturbations; sun-synchronous and frozen orbits.')
    + '<h3>Optional Topics</h3>'
    + li('Interplanetary transfer and gravity assist.', 'Lambert’s problem.',
         'Three-body dynamics and libration points.', 'Orbit determination from observations.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Curtis, <em>Orbital Mechanics for Engineering Students</em>, and Vallado, <em>Fundamentals of '
    'Astrodynamics and Applications</em>, are the standard texts; Bate, Mueller &amp; White remains in '
    'use and is inexpensive.</li>'
    '<li>MATLAB or Python throughout — most of the assignments are code. <code>poliastro</code>, '
    '<code>astropy</code> and NASA SPICE are worth knowing; GMAT and STK appear in mission-design '
    'work.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Named on the <strong>Aerospace Engineer</strong> career path, and in Florida it is the course '
    'that points most directly at local employment. Orbit design, launch windows, rendezvous and '
    'station-keeping are daily work for the Space Coast launch operators and satellite builders, and '
    'the same skills carry into guidance, navigation and control roles and into Space Force and its '
    'contractors.</p>'
    '<h2>Special Information</h2>'
    '<h3>&#9888;&#9888; The state records no prerequisite, and it should</h3>'
    '<p>The statewide prerequisite field for this number is <strong>blank</strong>. That is a gap in '
    'the record, not a statement that the course is open: <strong>orbital mechanics is not takeable '
    'without dynamics and differential equations</strong>, and every programme carrying it gates it. '
    '&#9888; <strong>Read your own catalogue for the real prerequisite</strong>, and do not plan a '
    'term around the state record here.</p>'
    '<h3>Astrodynamics and orbital mechanics are the same subject</h3>'
    '<table class="table table-sm"><tbody>'
    '<tr><td>FIU</td><td>Introduction to Astrodynamics</td></tr>'
    '<tr><td>University of South Florida</td><td>Astrodynamics</td></tr>'
    '<tr><td>University of Central Florida</td><td>Orbital Mechanics</td></tr>'
    '<tr><td>Florida Polytechnic</td><td>Orbital Mechanics</td></tr>'
    '</tbody></table>'
    '<p>Two names, one field. <em>Astrodynamics</em> is the term of art in the profession and '
    '<em>orbital mechanics</em> is the one the state uses. &#9888; <strong>If a catalogue or a job '
    'posting uses one and you learned the other, they are asking for the same thing.</strong></p>'
    '<h3>Expect to program</h3>'
    '<p>Almost nothing in this course closes in a form you can evaluate by hand — Kepler&rsquo;s '
    'equation is solved numerically, and every transfer problem becomes a script. <strong>Students '
    'who are weak programmers find this course hard for reasons that have nothing to do with '
    'orbits.</strong> If MATLAB or Python is shaky, fix that before the term rather than during '
    'it.</p>' + ITAR + NO_PE,
    {'summary': 'Four Florida public institutions carry EAS4505 at 3 credits: FIU, Florida '
                'Polytechnic, UCF and USF. FIU and USF title it astrodynamics; UCF and Florida '
                'Polytechnic use the statewide title, orbital mechanics. No institution publishes a '
                'contact-hour figure, and the statewide prerequisite field is empty.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
     'offerings': [
         {'institution': 'UCF', 'institution_name': 'University of Central Florida',
          'title': 'Orbital Mechanics', 'credits': 3, 'contact_hours': None, 'note': None},
         {'institution': 'USF', 'institution_name': 'University of South Florida',
          'title': 'Astrodynamics', 'credits': 3, 'contact_hours': None, 'note': None},
         {'institution': 'FIU', 'institution_name': 'Florida International University',
          'title': 'Introduction to Astrodynamics', 'credits': 3, 'contact_hours': None,
          'note': None},
         {'institution': 'FLPOLY', 'institution_name': 'Florida Polytechnic University',
          'title': 'Orbital Mechanics', 'credits': 3, 'contact_hours': None, 'note': None}]})

G['EAS4950'] = guide(
    'Aerospace Capstone Design I', 3, 45,
    'CARRIED BY TWO Florida public institutions at 3 credits - USF (Aerospace Capstone Design I) and '
    'Florida Polytechnic (Aerospace Engineering Design Senior Capstone 1). It is the FIRST HALF of a '
    'two-term sequence; the second half is EAS4951 at both institutions. Plan for both terms. '
    'WARNING - THE STATEWIDE PREREQUISITE DOES NOT RESOLVE AT BOTH CARRIERS. It reads "EML4703 AND '
    'EAS4101 AND EAS4251, all minimum grade C-". USF carries all three. FLORIDA POLYTECHNIC CARRIES '
    'NEITHER EML4703 NOR EAS4251 - only EAS4101 - so the state describes a chain that does not exist '
    'there. Read your own catalogue for the real gate; in practice it is senior standing plus the '
    'aerodynamics, structures and propulsion sequence. '
    'START THE TEAM AND SPONSOR LOGISTICS IN WEEK ONE: capstone projects are frequently '
    'industry-sponsored, and ITAR restrictions on a sponsored project can determine who may join '
    'which team.',
    '<h2>Course Description</h2>'
    '<p><strong>Aerospace Capstone Design I</strong> is the first half of the two-term senior design '
    'sequence — the course in which everything in the degree gets used at once, on a real problem, '
    'in a team. The statewide description is unusually specific: students are <strong>formed into '
    'teams, given a design topic, and tasked with creating a design solution</strong>, with the '
    'deliverable a <strong>full report containing a design description, engineering specifications '
    'and drawings</strong>, and with explicit discussion of the <strong>engineering code of '
    'ethics</strong> and of <strong>sustainability, ethics in the workplace, testing and data '
    'management</strong>.</p>'
    '<p>Carried by <strong>two Florida public institutions</strong> — USF and Florida Polytechnic — '
    'both at 3 credits, and at both the sequence continues into <code>EAS4951</code>.</p>'
    '<p>&#9888; <strong>This course is assessed differently from every other course in the '
    'degree.</strong> There is no problem set with an answer at the back; there is a design, a report, '
    'a presentation and a team, and the grade depends substantially on things that are not '
    'technical.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Translate a <strong>mission requirement into engineering specifications</strong>, and '
         'defend the translation.',
         'Execute the <strong>iterative conceptual design process</strong> — requirements, '
         'trade study, sizing, refinement.',
         'Integrate <strong>aerodynamics, structures, propulsion and control</strong> into a single '
         'coherent design, and resolve the conflicts between them.',
         'Produce <strong>engineering drawings and a full design report</strong> to a professional '
         'standard.',
         'Work effectively in a <strong>team</strong>, with defined roles, schedule and accountability.',
         'Apply the <strong>engineering code of ethics</strong> to decisions in the project, including '
         'sustainability, testing honesty and data management.',
         'Present and defend the design orally to a technical audience.')
    + '<h3>Optional Outcomes</h3>'
    + li('Work to an external sponsor’s requirements and review schedule.',
         'Use of design and analysis software (CAD, CFD, FEA) at project scale.',
         'Cost estimation and project management.',
         'Preparation for a design competition — AIAA Design/Build/Fly, NASA Student Launch, '
         'SAE Aero Design.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('The design process; requirements capture and the requirements document.',
         'Trade studies and decision matrices.',
         'Conceptual and preliminary sizing.',
         'Systems integration and interface control.',
         'Engineering ethics, sustainability and professional responsibility.',
         'Technical writing: the design report, specifications and drawings.',
         'Team organisation, scheduling and design reviews.')
    + '<h3>Optional Topics</h3>'
    + li('Sponsor management and external design reviews.',
         'Cost and manufacturability analysis.',
         'Risk assessment and failure modes.',
         'Test planning for the second term.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Raymer, <em>Aircraft Design: A Conceptual Approach</em>, and Wertz &amp; Larson, <em>Space '
    'Mission Analysis and Design</em>, depending on the project.</li>'
    '<li>CAD (SolidWorks, CATIA or NX), and whatever analysis tools the project needs — this is '
    'usually where students first use MATLAB, CFD and FEA together on one problem.</li>'
    '<li>The <strong>NSPE Code of Ethics for Engineers</strong>, which the statewide description '
    'explicitly names.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Named on the <strong>Aerospace Engineer</strong> career path, and it is the single most '
    'useful course on an entry-level r&eacute;sum&eacute;. A capstone project is the thing '
    'interviewers ask about: it is the only evidence most graduates have of working in a team, to a '
    'requirement, under a schedule. &#9888; <strong>Choose the project with the job in mind</strong> — '
    'a launch-vehicle project reads very differently to a Space Coast employer than a generic one, '
    'and a sponsored project comes with a named industry contact.</p>'
    '<h2>Special Information</h2>'
    '<h3>&#9888;&#9888; The statewide prerequisite does not resolve at Florida Polytechnic</h3>'
    '<p>The state records the gate as <strong><code>EML4703</code> and <code>EAS4101</code> and '
    '<code>EAS4251</code>, all with a minimum grade of C&minus;</strong>. Against the carriers:</p>'
    '<table class="table table-sm"><thead><tr><th>Named course</th><th>USF</th>'
    '<th>Florida Polytechnic</th></tr></thead><tbody>'
    '<tr><td><code>EML4703</code> Mechanics of Compressible Fluids</td><td>carries it</td>'
    '<td>&#9888; <strong>does not</strong></td></tr>'
    '<tr><td><code>EAS4101</code> Aerodynamics</td><td>carries it</td><td>carries it</td></tr>'
    '<tr><td><code>EAS4251</code> Structural Vibration</td><td>carries it</td>'
    '<td>&#9888; <strong>does not</strong></td></tr>'
    '</tbody></table>'
    '<p>&#9888;&#9888; <strong>USF carries all three and Florida Polytechnic carries one</strong>, '
    'which is the signature of a statewide prerequisite contributed by a single carrier. It is a '
    'known defect shape, not a claim that Florida Polytechnic&rsquo;s students are under-prepared: '
    'that university gates its capstone on its own sequence. <strong>Read the gate from your own '
    'catalogue.</strong></p>'
    '<h3>A shell number that has become a real course</h3>'
    '<p>Numbers ending <code>950</code> are normally special-topics shells, and this repository skips '
    'them for that reason. <strong>This one is an exception and the evidence is clear</strong>: both '
    'carriers give it a specific, matching title, the statewide description names concrete '
    'deliverables, and <code>EAS4951</code> exists as its second half at the same two institutions. '
    'It is a capstone sequence that happens to sit on a shell number. &#9888; The statewide record '
    'still classifies its course intent as <em>variable</em>, which is a leftover of the number '
    'family rather than a description of the course.</p>'
    '<h3>&#9888; ITAR can decide which team you join</h3>'
    '<p>Capstone projects are frequently sponsored by industry, and aerospace sponsors are frequently '
    'ITAR-controlled. <strong>An international student may be ineligible for particular '
    'projects</strong>, and that is discovered at team formation in the first week, not at the point '
    'of choosing. &#9888; Ask before the term which projects carry export-control restrictions — '
    'there are almost always unrestricted projects, and knowing early means choosing rather than '
    'being assigned.</p>'
    '<h3>Plan both terms together</h3>'
    '<p>This course does little on its own: the design produced here is built, tested and reported in '
    '<code>EAS4951</code>. &#9888; <strong>A schedule that puts the two halves anywhere other than '
    'consecutive terms will not work</strong>, because the team disperses. Confirm both are offered '
    'in the terms you plan, and treat a graduation date as depending on the pair.</p>' + ITAR + NO_PE,
    {'summary': 'Two Florida public institutions carry EAS4950 at 3 credits: USF (Aerospace Capstone '
                'Design I) and Florida Polytechnic (Aerospace Engineering Design Senior Capstone 1). '
                'Both continue the sequence in EAS4951. No institution publishes a contact-hour '
                'figure. The statewide record classifies the course intent as VARIABLE.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the uniform 3-credit value. '
                   '⚠ A design course distributes its hours differently from a lecture course '
                   '— team meetings and project work dominate — so the figure describes the '
                   'credit value rather than scheduled classroom time.',
     'offerings': [
         {'institution': 'USF', 'institution_name': 'University of South Florida',
          'title': 'Aerospace Capstone Design I', 'credits': 3, 'contact_hours': None,
          'note': 'Carries all three courses named in the statewide prerequisite.'},
         {'institution': 'FLPOLY', 'institution_name': 'Florida Polytechnic University',
          'title': 'Aerospace Eng. Design Senior Capstone 1', 'credits': 3, 'contact_hours': None,
          'note': '⚠ Carries neither EML4703 nor EAS4251, so the statewide prerequisite does '
                  'not resolve here.'}]})


def main():
    for cid, g in G.items():
        io.open(os.path.join(DRAFTS, '%s_guide.json' % cid), 'w', encoding='utf-8').write(
            json.dumps(g, ensure_ascii=False, indent=1))
        print('%-9s %-34s %d cr / %d hrs | prereq %4d | html %6d'
              % (cid, g['title'][:34], g['credits'], g['contact_hours'],
                 len(g['prerequisites']), len(g['html_content'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
