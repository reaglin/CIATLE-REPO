#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Batch 240 -- the thirteen ECH guides the Chemical Engineer path owes.

Written data-driven because all thirteen sit in ONE landscape and share the
same four institutions, so the context blocks are identical and only the
subject matter changes. Spelling each out longhand would duplicate 60% of the
text and let the shared facts drift apart between guides.

⚠⚠ THE LANDSCAPE, and it governs the hedging on every guide here.
Chemical engineering is awarded by FOUR Florida public institutions in THREE
cities (UF 110 bachelor's, USF 73, FSU 27, FAMU 4 -- IPEDS C2023_A, CIP
14.0701), because FAMU and FSU share the joint FAMU-FSU College of
Engineering. FIU carries three ECH numbers as service courses and awards no
chemical engineering degree; UCF carries none at all.

So: every course here has TWO TO FIVE carriers. Under the hedging rules that
is explicit-hedging territory throughout, and the single-carrier baseline
caution applies -- but with a twist specific to this prefix. FAMU and FSU are
ONE COLLEGE, so a course showing "2 carriers: FAMU, FSU" is really ONE
programme's course, and a course showing 3 (FAMU, FSU, USF) is really TWO.
⚠ Carrier counts in this prefix overstate independence, and the guides say so.

⚠⚠⚠ PARALLEL NUMBERING FAMILIES run the whole transport and separations
sequence, with UF alone on one side:

    FAMU / FSU / USF              University of Florida
    ECH3266 Transport I           ECH3264 Elementary Transport Phenomena
    ECH4267 Transport II          ECH3203 Fluid and Solid Operations
                                  ECH3223 Energy Transfer Operations
    ECH3418 Separations           ECH4403 Separation and Mass Transfer Ops
                                  (USF numbers separations ECH4418)

⚠⚠⚠ ECH3854 CARRIES THE WORST STATEWIDE PREREQUISITE STRING FOUND IN THIS
PROJECT. It names ECH 3264 (UF alone -- and UF does not carry ECH3854),
CGS 3460 (ZERO public carriers in the state) and MAP 3305 (not at USF), while
its carriers are FAMU, FSU and USF. Two of the five documented defect shapes
in one field, from a contributor that does not teach the course.

⚠⚠ ECH4714 IS CONTRIBUTOR DRIFT (batch 229). Statewide title is "Safety &
Experimental Evaluation-Upper" and the statewide description ends "integrated
with ECH 4224L" -- which is UF's laboratory number, so UF contributed the
record. UF now titles the course "Chemical Process Safety". The contributor
has drifted from its own contribution.

⚠ ECH4404L IS A SCOPE DIVERGENCE, not a subject one. Statewide is "Chemical
Engineering Operations Lab 2 ... laboratory work in unit operations involving
MASS TRANSFER", which is exactly UF's 2-credit reading. FAMU and FSU run it as
the general unit operations laboratory at 3 credits. Both are real; the time
commitment differs by half again.

⚠ ECH3101's and ECH3418's and ECH4504's statewide prerequisite fields are
blank or prose ("THE THERMODYNAMICS, TRANSPORT PHENOMENA"), so none of them
names a course. The batch-227 prose shape: no course-looking token at all, so
the syntax test never fires while the field tells the reader nothing.
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
    'FIU': 'Florida International University',
}


def li(*items):
    return LG + ''.join(LI + i + '</li>' for i in items) + '</ul>'


def sec(h2, req, opt, req_label='Required', opt_label='Optional'):
    out = '<h2>%s</h2><h3>%s %s</h3>' % (h2, req_label, h2.split()[-1])
    out += li(*req)
    if opt:
        out += '<h3>%s %s</h3>' % (opt_label, h2.split()[-1]) + li(*opt)
    return out


LANDSCAPE = (
    '<h3>%s Only four Florida institutions teach this, and two of them are one college</h3>'
    '<p>Chemical engineering is awarded by <strong>four Florida public institutions in three '
    'cities</strong>: the University of Florida (110 bachelor&rsquo;s degrees a year), the '
    'University of South Florida (73), Florida State (27) and Florida A&amp;M (4). <strong>Florida '
    'State and Florida A&amp;M share the FAMU-FSU College of Engineering</strong>, a single joint '
    'college in Tallahassee, which is why their records for this prefix are identical down to the '
    'title.</p>'
    '<p>%s <strong>So a carrier count in this prefix overstates how many independent programmes '
    'exist.</strong> A course carried by &ldquo;FAMU and FSU&rdquo; is one programme&rsquo;s course, '
    'not two institutions agreeing. Read the hedging on this page accordingly, and treat anything '
    'stated about content as a description of a small number of specific curricula rather than a '
    'Florida-wide norm.</p>'
    '<p>%s <strong>Neither UCF nor FIU awards a chemical engineering degree</strong> — the two '
    'largest universities in the state by enrolment. See the '
    '<a href="/careers/chemical-engineer">Chemical Engineer</a> career path for what that means if '
    'you live in Orlando or Miami.</p>'
) % (WW, WW, W)

UF_FAMILY = (
    '<h3>%s UF numbers the transport and separations sequence differently from everyone else</h3>'
    '<p>Florida runs two parallel numbering families through the analytical core of this degree, '
    'and the University of Florida is alone on one side of it:</p>'
    '<table class="table table-sm"><thead><tr><th>FAMU, FSU, USF</th><th>University of Florida</th>'
    '</tr></thead><tbody>'
    '<tr><td><code>ECH3266</code> Transport Phenomena I</td><td><code>ECH3264</code> Elementary '
    'Transport Phenomena</td></tr>'
    '<tr><td><code>ECH4267</code> Transport Phenomena II</td><td><code>ECH3203</code> Fluid and '
    'Solid Operations<br><code>ECH3223</code> Energy Transfer Operations</td></tr>'
    '<tr><td><code>ECH3418</code> Separations Processes (USF: <code>ECH4418</code>)</td>'
    '<td><code>ECH4403</code> Separation and Mass Transfer Operations</td></tr>'
    '</tbody></table>'
    '<p>%s <strong>Same material, two schemes, and no number in common.</strong> Nothing in the '
    'identifier signals it, so an evaluator matching on course numbers finds nothing to match. '
    '<strong>On transfer between Florida chemical engineering programmes, send a topic list and a '
    'syllabus rather than a course number.</strong></p>'
) % (WWW, W)

ABET_FE = (
    '<h3>Accreditation and licensure</h3>'
    '<p>All four Florida programmes are accredited by ABET&rsquo;s <strong>Engineering '
    'Accreditation Commission</strong>, which is what employers screen on and what carries the '
    'four-year route to Professional Engineer licensure under s. 471.013(1)(a), Florida Statutes. '
    '%s <strong>Accreditation attaches to a named programme at a named institution, not to a course '
    'list</strong> — verify the specific programme in ABET&rsquo;s own search.</p>'
    '<p>Most chemical engineers never license: process plants fall under the industrial exemption. '
    '%s <strong>The Florida exceptions are environmental and water engineering consulting</strong>, '
    'where work is sealed for public clients. <strong>Sit the FE examination in your final year '
    'regardless</strong> — the chemical FE is written for the curriculum you have just finished and '
    'will never be easier.</p>'
) % (W, W)

# ---------------------------------------------------------------------------
# (id, title, credits, hours, carriers[(code, title, credits, note)], prereq,
#  lede paragraphs, outcomes, opt outcomes, topics, opt topics, resources,
#  career, extra special blocks, offering summary, derivation)
# ---------------------------------------------------------------------------
SPEC = []


def add(**kw):
    SPEC.append(kw)


add(
    cid='ECH3023', title='Material and Energy Balances', credits=4, hours=60,
    carriers=[('FAMU', 'Mass and Energy Balances I', 3, None),
              ('FSU', 'Mass and Energy Balances I', 4, None),
              ('UF', 'Material and Energy Balances', 4, None),
              ('USF', 'Material and Energy Balances', 3, None)],
    prereq=(
        'General chemistry with laboratory and the calculus sequence; programmes normally require '
        'CHM2046 (or CHM1046 - Florida uses both numbers) with a minimum grade of C, and calculus '
        'through MAC2313. The statewide prerequisite field is BLANK, which is a gap in the record '
        'rather than an open door. '
        'THIS IS THE GATEWAY COURSE OF THE MAJOR and programmes treat it as the screen: it is where '
        'students find out whether chemical engineering suits them. '
        'CREDITS DIVERGE AND SO DOES THE STRUCTURE. UF and FSU carry it at 4 credits; FAMU and USF '
        'at 3. FAMU and FSU run a SECOND term, ECH3024 Mass and Energy Balances II, which UF and '
        'USF do not - so the same material is one course at two institutions and two at the other. '
        'WATCH THE STATEWIDE TITLE: it reads "Introduction to Chemical Engineering", and no carrier '
        'uses that name. The statewide DESCRIPTION and all four carriers agree it is mass and '
        'energy balances.'),
    lede=('<strong>Material and Energy Balances</strong> is the first course of the chemical '
          'engineering major and the one the whole degree is built on. The statewide description is '
          'short and exact: <strong>the conservation laws of mass and energy applied to the '
          'solution of industrial chemical process problems</strong>.',
          '%s <strong>Every chemical engineer remembers this course.</strong> It is not '
          'mathematically difficult — there is little beyond algebra and a systematic accounting of '
          'what goes in and what comes out — and it is nonetheless where a substantial share of '
          'intending majors change their minds. The difficulty is that problems arrive as a '
          'paragraph of prose about a real process and you must decide for yourself what the system '
          'is, what crosses its boundary, and which equations are independent. Nothing earlier in '
          'the curriculum asks that.' % WW),
    outcomes=['Define a <strong>system and its boundary</strong> for a process, and draw a labelled '
              'flow diagram from a prose description.',
              'Carry out a <strong>degree-of-freedom analysis</strong> and determine whether a '
              'problem is solvable before attempting it.',
              'Solve <strong>steady-state material balances</strong> on single and multiple units, '
              'with and without reaction.',
              'Handle <strong>recycle, bypass and purge</strong> streams.',
              'Apply <strong>energy balances</strong>, using enthalpy, heat capacity and latent '
              'heat data.',
              'Combine material and energy balances on <strong>reactive systems</strong>, including '
              'heats of reaction and adiabatic flame temperature.',
              'Use <strong>phase equilibrium data</strong> — Raoult’s and Henry’s '
              'laws, humidity, psychrometric charts.'],
    opt_outcomes=['Transient (unsteady-state) balances.',
                  'Process simulation software — Aspen Plus, HYSYS or ChemCAD.',
                  'Statistical treatment of process data.',
                  'An introduction to process economics.'],
    topics=['Units, dimensions and process variables.',
            'Process flow diagrams and the general balance equation.',
            'Material balances without reaction; degree-of-freedom analysis.',
            'Multiple-unit processes; recycle, bypass and purge.',
            'Material balances with chemical reaction.',
            'Single-phase and multiphase systems; vapour-liquid equilibrium.',
            'Energy balances on non-reactive and reactive processes.'],
    opt_topics=['Unsteady-state balances.', 'Process simulation.',
                'Combustion calculations in depth.'],
    resources=['Felder, Rousseau &amp; Bullard, <em>Elementary Principles of Chemical Processes</em>, '
               'is close to universal — the "Felder and Rousseau" every chemical engineer means.',
               'Himmelblau &amp; Riggs is the common alternative.',
               'A spreadsheet, and often MATLAB or Python, for the simultaneous equations; '
               'process simulators appear where the institution introduces them early.'],
    career=('Named on the <strong>Chemical Engineer</strong> career path, where it is the entry '
            'point to the major. Beyond that its skill — accounting rigorously for what enters and '
            'leaves a process — is the daily work of a process engineer in any plant, and it is '
            'what an internship interviewer will ask you to demonstrate.'),
    extra=(
        '<h3>%s The statewide title is stale, and the carriers prove it</h3>'
        '<p>SCNS titles this number <em>Introduction to Chemical Engineering</em>. <strong>No '
        'carrier uses that name:</strong> FAMU and FSU call it <em>Mass and Energy Balances I</em>, '
        'UF and USF <em>Material and Energy Balances</em>. The statewide <em>description</em> — the '
        'conservation laws of mass and energy — agrees with the carriers, not the title, so the '
        'title is the stale element.</p>'
        '<p>%s It matters practically: <strong>several Florida institutions run a genuine '
        '&ldquo;introduction to chemical engineering&rdquo; survey course under a different '
        'number</strong> — <code>ECH3002</code> at USF, <code>ECH2934</code> at UF — and those are '
        'one- or two-credit orientation courses, not this. Do not substitute one for the other on '
        'the strength of the title.</p>'
        '<h3>%s One course here, two courses there</h3>'
        '<table class="table table-sm"><thead><tr><th>Institution</th><th>Credits</th>'
        '<th>Structure</th></tr></thead><tbody>'
        '<tr><td>University of Florida</td><td><strong>4</strong></td><td>one term</td></tr>'
        '<tr><td>Florida State</td><td><strong>4</strong></td><td>%s followed by '
        '<code>ECH3024</code></td></tr>'
        '<tr><td>Florida A&amp;M</td><td>3</td><td>%s followed by <code>ECH3024</code> (4 credits)'
        '</td></tr>'
        '<tr><td>University of South Florida</td><td>3</td><td>one term</td></tr>'
        '</tbody></table>'
        '<p>%s <strong>This is sequence-length divergence</strong> (the same field taught as one '
        'course at some institutions and two at others) <strong>colliding with a credit '
        'divergence.</strong> A student transferring into UF or USF with only the first half of the '
        'FAMU-FSU sequence has covered the material balances and possibly not the reactive energy '
        'balances. <strong>Send the topic list; the titles are no help, because both halves are '
        'called the same thing.</strong></p>' % (WWW, W, WW, WW, WW, WWW)),
    summary=('Four Florida public institutions carry ECH3023. Credits diverge: UF and Florida '
             'State at 4, FAMU and USF at 3. FAMU and Florida State follow it with a second term, '
             'ECH3024, which UF and USF do not run. No institution publishes a contact-hour figure.'),
    derivation=('Florida convention of 15 contact hours per credit at the 4-credit value. ⚠ The '
                'scalar describes the 4-credit form carried by UF and Florida State, which between '
                'them award the majority of the state’s chemical engineering degrees; at FAMU '
                'and USF the course is 3 credits and approximately 45 contact hours.'),
)

add(
    cid='ECH3101', title='Chemical Engineering Thermodynamics', credits=3, hours=45,
    carriers=[('FAMU', 'Chemical Engineering Thermodynamics', 3, None),
              ('FSU', 'Chemical Engineering Thermodynamics', 3, None),
              ('UF', 'Process Thermodynamics', 4, '⚠ Four credits, and a different title.'),
              ('USF', 'Chemical Engineering Thermodynamics', 3, None)],
    prereq=(
        'Material and energy balances (ECH3023) and general chemistry; the calculus sequence and '
        'usually differential equations. THE STATEWIDE PREREQUISITE FIELD READS "NONE", which is a '
        'defect in the record rather than a statement about the course - no Florida programme '
        'allows a student into chemical engineering thermodynamics without the balances course '
        'first. Read your own catalogue. '
        'CARRIED BY ALL FOUR Florida chemical engineering programmes: FAMU, FSU and USF at 3 '
        'credits, UF at 4 and under the title Process Thermodynamics. '
        'THIS IS THE FIRST OF TWO. The second is ECH4123 (UF Phase and Chemical Equilibria, USF '
        'Chemical Engineering Thermodynamics II), and at FAMU and FSU the mixture material is '
        'distributed differently. Find out where your programme teaches phase equilibrium.'),
    lede=('<strong>Chemical Engineering Thermodynamics</strong> is the conceptual spine of the '
          'degree: what energy is available, which direction a process will go, and how far. The '
          'statewide description covers <strong>the principles of classical and statistical '
          'thermodynamics and their application to systems of constant composition</strong>.',
          '%s <strong>This is not the thermodynamics a mechanical engineer takes.</strong> A power '
          'cycle deals with one substance changing phase; a chemical process deals with mixtures '
          'whose composition changes, and almost everything difficult in this subject follows from '
          'that. Expect fugacity, activity and departure functions — abstractions with no '
          'mechanical analogue, and the reason this course has the reputation it does.' % WW),
    outcomes=['Apply the <strong>first law</strong> to open and closed systems, and to flow '
              'processes with shaft work.',
              'Apply the <strong>second law</strong>, and use entropy to determine feasibility and '
              'lost work.',
              'Use <strong>equations of state</strong> — ideal gas, virial, cubic (van der Waals, '
              'Redlich-Kwong, Peng-Robinson) — and know when each is adequate.',
              'Compute <strong>departure functions</strong> and use generalised correlations to get '
              'property values for real fluids.',
              'Analyse <strong>power and refrigeration cycles</strong> in a process context.',
              'Determine <strong>thermodynamic properties</strong> from tables, charts and '
              'correlations, and estimate them where data are missing.'],
    opt_outcomes=['An introduction to solution thermodynamics and phase equilibrium, where the '
                  'institution places it in the first term.',
                  'Statistical thermodynamics, which the statewide description names explicitly.',
                  'Thermodynamic analysis of separation and reaction processes.'],
    topics=['Scope, definitions and the PVT behaviour of pure fluids.',
            'The first law for closed and open systems.',
            'Volumetric properties and equations of state.',
            'Heat effects; standard heats of reaction and formation.',
            'The second law; entropy and entropy balances.',
            'Thermodynamic properties of fluids; departure functions and residual properties.',
            'Power and refrigeration cycles; liquefaction.'],
    opt_topics=['Introduction to solution thermodynamics.',
                'Statistical thermodynamics.', 'Exergy and availability analysis.'],
    resources=['Smith, Van Ness &amp; Abbott, <em>Introduction to Chemical Engineering '
               'Thermodynamics</em> — the standard, and the one most Florida programmes use.',
               'Koretsky and Sandler are the common alternatives.',
               'Steam tables and thermodynamic charts; MATLAB, Python or a spreadsheet for the '
               'cubic equations of state, which do not solve by hand pleasantly.'],
    career=('Named on the <strong>Chemical Engineer</strong> career path. Thermodynamics is what '
            'decides whether a process is possible before anyone designs the equipment, and it is '
            'the analytical basis of separations, reactor design and energy integration. It is also '
            'the most heavily weighted subject on the chemical FE examination.'),
    extra=(
        '<h3>%s The statewide prerequisite says NONE</h3>'
        '<p>It does, and it is wrong in the only sense that matters: <strong>no Florida programme '
        'admits a student to this course without material and energy balances</strong>, and the '
        'course is unworkable without it. %s <strong>Read the gate from your own catalogue and do '
        'not plan a term around the state record here.</strong></p>'
        '<h3>UF carries it at four credits, and calls it something else</h3>'
        '<p>UF titles the course <em>Process Thermodynamics</em> and runs it at <strong>4 '
        'credits</strong> against 3 at FAMU, FSU and USF. %s <strong>The extra credit is real '
        'content, not accounting</strong> — it is roughly where the mixture and phase-equilibrium '
        'material begins to appear — so a transfer student arriving at UF with the 3-credit version '
        'is a credit short and may also be short the topic. <strong>Ask which institution’s '
        'thermodynamics sequence your degree audit expects.</strong></p>'
        '<h3>Where is the second term?</h3>'
        '<p>Thermodynamics of <em>mixtures</em> — fugacity in solution, activity coefficients, phase '
        'and chemical equilibrium — is the other half of the subject, and Florida places it '
        'differently. UF numbers it <code>ECH4123</code> <em>Phase and Chemical Equilibria</em>; USF '
        'numbers the same course <code>ECH4123</code> and titles it <em>Chemical Engineering '
        'Thermodynamics II</em>. %s <strong>Neither FAMU nor FSU carries <code>ECH4123</code></strong>, '
        'distributing the material through the separations and design sequence instead. '
        '<strong>Find out where your programme teaches phase equilibrium, because everything in '
        'separations assumes it.</strong></p>' % (WW, W, W, WW)),
    summary=('All four Florida chemical engineering programmes carry ECH3101. FAMU, Florida State '
             'and USF run it at 3 credits under the statewide title; UF runs it at 4 credits as '
             'Process Thermodynamics. No institution publishes a contact-hour figure.'),
    derivation=('Florida convention of 15 contact hours per credit at the 3-credit value carried by '
                'three of the four programmes. ⚠ At UF the course is 4 credits and '
                'approximately 60 contact hours.'),
)

add(
    cid='ECH3266', title='Transport Phenomena I', credits=3, hours=45,
    carriers=[('FAMU', 'Introductory Transport Phenomena I', 3, None),
              ('FSU', 'Transport Phenomena I', 3, None),
              ('USF', 'Transport Phenomena I', 3, None)],
    prereq=(
        'Material and energy balances and the calculus sequence; differential equations is normally '
        'required or taken alongside. The statewide prerequisite field is blank. '
        'CARRIED BY FAMU, FSU AND USF AT 3 CREDITS - and because FAMU and FSU are one joint '
        'college, that is TWO independent programmes, not three. '
        'THE UNIVERSITY OF FLORIDA DOES NOT CARRY THIS NUMBER. UF teaches the same material under a '
        'different numbering family: ECH3264 Elementary Transport Phenomena, ECH3203 Fluid and '
        'Solid Operations and ECH3223 Energy Transfer Operations. Same subject, no number in '
        'common - so on transfer send a topic list, not a course number.'),
    lede=('<strong>Transport Phenomena I</strong> is the analysis chemical engineers own: how '
          'momentum, heat and mass move, and how to size the equipment that moves them. The '
          'statewide description is unusually concrete — <strong>integral balance equations for '
          'conservation of momentum, energy and mass; application to chemical processes involving '
          'fluid flow and heat and mass transfer; estimation of friction factors and heat and mass '
          'transfer coefficients; pump selection and sizing; piping network analysis; design of '
          'heat exchangers</strong>.',
          '%s <strong>Note what that list contains: pumps, pipes and heat exchangers.</strong> This '
          'is the first course in the degree whose output is a piece of equipment with a size, and '
          'that makes it the most directly employable course in the first half of the major. The '
          'second term, <code>ECH4267</code>, is where it becomes differential and abstract; this '
          'one stays close to things you can point at.' % W),
    outcomes=['Apply <strong>integral (macroscopic) balances</strong> of momentum, energy and mass '
              'to flow systems.',
              'Analyse <strong>pipe flow</strong>: friction factors, the Moody chart, minor losses '
              'and the mechanical energy balance.',
              'Select and <strong>size a pump</strong>, and check it against NPSH.',
              'Analyse <strong>piping networks</strong> and flow measurement devices.',
              'Compute <strong>heat transfer</strong> by conduction, convection and radiation, and '
              'use correlations for convective coefficients.',
              'Design and rate a <strong>heat exchanger</strong> using LMTD and effectiveness-NTU '
              'methods.',
              'Estimate <strong>mass transfer coefficients</strong> and apply the analogies between '
              'momentum, heat and mass transfer.'],
    opt_outcomes=['Introduction to boundary-layer theory.',
                  'Non-Newtonian fluids and slurry flow.',
                  'Introduction to computational fluid dynamics.',
                  'Compressible flow in pipes.'],
    topics=['Fluid statics and the integral balances.',
            'Laminar and turbulent pipe flow; friction factors.',
            'The mechanical energy balance; pumps, NPSH and pump curves.',
            'Piping networks, valves, fittings and flow measurement.',
            'Conduction, convection and radiation.',
            'Convective heat transfer correlations.',
            'Heat exchanger design and rating.',
            'Introduction to mass transfer and the transport analogies.'],
    opt_topics=['Boundary layers.', 'Non-Newtonian flow.', 'Flow past immersed bodies; packed beds.',
                'Introduction to CFD.'],
    resources=['Welty, Rorrer &amp; Foster, <em>Fundamentals of Momentum, Heat and Mass '
               'Transfer</em>; Geankoplis, <em>Transport Processes and Separation Process '
               'Principles</em>; and Bird, Stewart &amp; Lightfoot, which is the reference every '
               'chemical engineer eventually owns.',
               'The Moody chart and standard correlation tables; MATLAB, Python or a spreadsheet '
               'for iterative friction-factor and exchanger calculations.',
               'Manufacturer pump curves — real ones, which are freely available and make the '
               'sizing exercises concrete.'],
    career=('Named on the <strong>Chemical Engineer</strong> career path. Fluid flow and heat '
            'transfer are what a plant process engineer works on daily, and the pump and exchanger '
            'skills are immediately usable in an internship. In Florida the same analysis carries '
            'into water and wastewater treatment, power generation, food and beverage processing, '
            'and the phosphate industry.'),
    extra=UF_FAMILY,
    summary=('Three Florida public institutions carry ECH3266, all at 3 credits: FAMU, Florida '
             'State and USF. ⚠ FAMU and Florida State share one joint college, so that is two '
             'independent programmes. UF does not carry the number, teaching the material under '
             'ECH3264, ECH3203 and ECH3223. No institution publishes a contact-hour figure.'),
    derivation='Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
)

add(
    cid='ECH4267', title='Transport Phenomena II', credits=3, hours=45,
    carriers=[('FAMU', 'Transport Phenomena II', 3, None),
              ('FSU', 'Advanced Transport Phenomena', 3, None),
              ('USF', 'Transport Phenomena II', 3, None)],
    prereq=(
        'Transport Phenomena I (ECH3266) and differential equations; vector calculus is assumed '
        'throughout. The statewide prerequisite field is blank. '
        'CARRIED BY FAMU, FSU AND USF AT 3 CREDITS, and since FAMU and FSU are one joint college '
        'that is two independent programmes. FSU titles it Advanced Transport Phenomena. '
        'THE UNIVERSITY OF FLORIDA DOES NOT CARRY THIS NUMBER - it uses ECH3203 and ECH3223 for the '
        'same material. Send a topic list on transfer, not a number. '
        'THIS IS THE DIFFERENTIAL TREATMENT, not more of the same. Where Transport I took control '
        'volumes and correlations, this course derives the shell balances and solves the partial '
        'differential equations. It is the most mathematically demanding course in the major.'),
    lede=('<strong>Transport Phenomena II</strong> is where the subject stops using correlations and '
          'starts deriving them. The statewide description: <strong>molecular mechanisms for '
          'momentum, heat and mass transport; differential balance equations for conservation of '
          'momentum, energy and mass; application to steady and unsteady-state chemical processes '
          'involving diffusive and convective mass transfer in solids, liquids and gases; '
          'interphase transfer mechanisms; boundary layer theory and turbulent transport</strong>.',
          '%s <strong>This is the hardest mathematics in the degree.</strong> Shell balances become '
          'partial differential equations, and the work is in choosing a coordinate system, '
          'identifying the boundary conditions and knowing which terms may honestly be dropped. '
          'Students who arrive without fluency in differential equations and vector calculus meet '
          'the consequences in week three.' % WW),
    outcomes=['Derive <strong>differential balance equations</strong> from shell balances in '
              'rectangular, cylindrical and spherical coordinates.',
              'Apply the <strong>equations of change</strong> — continuity, Navier-Stokes, energy '
              'and species — and simplify them defensibly for a given problem.',
              'Solve <strong>steady and unsteady conduction and diffusion</strong> problems, '
              'analytically and numerically.',
              'Apply <strong>boundary-layer theory</strong> to momentum, heat and mass transfer.',
              'Analyse <strong>turbulent transport</strong> and the basis of the empirical '
              'correlations used in the first course.',
              'Analyse <strong>interphase mass transfer</strong>, including two-film theory and '
              'transfer with chemical reaction.'],
    opt_outcomes=['Numerical solution of the transport equations.',
                  'Transport in porous media.',
                  'Introduction to computational fluid dynamics.',
                  'Biological or biomedical transport applications.'],
    topics=['Molecular mechanisms of momentum, heat and mass transport.',
            'Shell balances and the equations of change.',
            'Solutions for laminar flow, conduction and diffusion.',
            'Unsteady-state transport.',
            'Boundary layer theory.',
            'Turbulent transport and time-smoothed equations.',
            'Interphase transport; mass transfer with reaction.'],
    opt_topics=['Numerical methods for transport problems.', 'Porous media.',
                'Multicomponent diffusion.', 'Bio-transport.'],
    resources=['Bird, Stewart &amp; Lightfoot, <em>Transport Phenomena</em> — at this level it is '
               'the text rather than a reference.',
               'Deen, <em>Analysis of Transport Phenomena</em>, is the common alternative.',
               'MATLAB or Python for the numerical solutions; symbolic tools are genuinely useful '
               'here.'],
    career=('Named on the <strong>Chemical Engineer</strong> career path. This course is the '
            'gateway to graduate study in chemical engineering — a doctoral programme assumes it '
            'from day one — and industrially it underpins reactor design, membrane and separation '
            'technology, and any modelling or simulation role.'),
    extra=UF_FAMILY,
    summary=('Three Florida public institutions carry ECH4267, all at 3 credits: FAMU and Florida '
             'State (which share one joint college, Florida State titling it Advanced Transport '
             'Phenomena) and USF. UF does not carry the number. No institution publishes a '
             'contact-hour figure.'),
    derivation='Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
)

add(
    cid='ECH3418', title='Separations Processes', credits=3, hours=45,
    carriers=[('FAMU', 'Separations Processes', 3, None),
              ('FSU', 'Separations Processes', 3, None)],
    prereq=(
        'Thermodynamics and transport phenomena, and in practice phase equilibrium - which is the '
        'thing to check, because Florida programmes teach phase equilibrium in different places. '
        'The statewide prerequisite field is blank. '
        'CARRIED AS ECH3418 BY FAMU AND FSU ONLY, at 3 credits - and those two share one joint '
        'college, so this number represents ONE programme. Hedge everything on this page '
        'accordingly. '
        'THE SAME SUBJECT EXISTS UNDER TWO OTHER NUMBERS: USF numbers it ECH4418 Separation Process '
        'and UF numbers it ECH4403 Separation and Mass Transfer Operations. THREE NUMBERS, ONE '
        'SUBJECT, and the state defines all of them from one record. Search by subject, not number.'),
    lede=('<strong>Separations Processes</strong> is, in industrial terms, most of what a chemical '
          'plant does. The statewide description: <strong>principles of equilibrium and '
          'transport-controlled separations; analysis and design of stagewise and continuous '
          'separation processes including distillation, absorption, extraction, filtration and '
          'membrane separations</strong>.',
          '%s <strong>Distillation alone is one of the largest single consumers of industrial '
          'energy in the world</strong>, which is why this course spends so long on it and why '
          'improving a separation is one of the highest-value things a process engineer does.'
          % W),
    outcomes=['Apply <strong>phase equilibrium</strong> — VLE, LLE, relative volatility — to '
              'separation design.',
              'Analyse <strong>equilibrium-stage</strong> processes using mass balances and '
              'operating lines.',
              'Design <strong>binary distillation</strong> columns by the McCabe-Thiele method, and '
              'determine reflux ratio, stages and feed location.',
              'Analyse <strong>absorption and stripping</strong> columns.',
              'Analyse <strong>liquid-liquid extraction</strong>.',
              'Size <strong>packed columns</strong> using HTU-NTU and mass transfer coefficients.',
              'Describe and select among <strong>membrane, adsorption and filtration</strong> '
              'processes.'],
    opt_outcomes=['Multicomponent and azeotropic distillation.',
                  'Batch distillation.',
                  'Crystallisation and drying.',
                  'Process simulation of separation trains.'],
    topics=['Phase equilibrium for separations.',
            'Single-stage and multistage equilibrium processes.',
            'Binary distillation; McCabe-Thiele and Ponchon-Savarit.',
            'Column internals, efficiency and hydraulics.',
            'Gas absorption and stripping.',
            'Liquid-liquid extraction.',
            'Rate-based separations: membranes, adsorption, filtration.'],
    opt_topics=['Multicomponent distillation and shortcut methods.',
                'Azeotropic and extractive distillation.', 'Crystallisation, drying, leaching.',
                'Simulation with Aspen or HYSYS.'],
    resources=['Wankat, <em>Separation Process Engineering</em>; Seader, Henley &amp; Roper, '
               '<em>Separation Process Principles</em>; Geankoplis.',
               'Process simulators (Aspen Plus, HYSYS) are common here — a column converged in a '
               'simulator is a genuinely marketable skill.',
               'Graph paper, or a plotting script, for McCabe-Thiele constructions.'],
    career=('Named on the <strong>Chemical Engineer</strong> career path. Separations is where a '
            'large share of process engineering jobs actually sit, and in Florida it carries '
            'directly into water treatment and desalination, pharmaceutical purification, '
            'phosphate and specialty chemicals processing, and food and beverage production.'),
    extra=(
        '<h3>%s One subject, three numbers</h3>'
        '<table class="table table-sm"><thead><tr><th>Number</th><th>Title</th><th>Carrier</th>'
        '</tr></thead><tbody>'
        '<tr><td><code>ECH3418</code></td><td>Separations Processes</td><td>FAMU, Florida State '
        '(one joint college)</td></tr>'
        '<tr><td><code>ECH4418</code></td><td>Separation Process</td><td>University of South '
        'Florida</td></tr>'
        '<tr><td><code>ECH4403</code></td><td>Separation and Mass Transfer Operations</td>'
        '<td>University of Florida</td></tr>'
        '</tbody></table>'
        '<p>%s <strong>Every Florida chemical engineering programme teaches this and no two agree '
        'on the number.</strong> Note also the LEVEL: FAMU and Florida State number it at 3000 and '
        'the other two at 4000. Both are upper division, so nothing is lost in transfer — but a '
        'degree audit matching identifiers will not find it, and <strong>a student searching a '
        'catalogue for &ldquo;ECH3418&rdquo; at UF or USF will conclude, wrongly, that the course '
        'does not exist there.</strong></p>'
        '<h3>%s Check where your programme taught you phase equilibrium</h3>'
        '<p>This course assumes it. UF and USF teach it as <code>ECH4123</code>; FAMU and Florida '
        'State do not carry that number and distribute the material through this course and the '
        'design sequence. <strong>If you are transferring in, confirm you have had fugacity, '
        'activity coefficients and VLE before you arrive</strong> — the course will not stop to '
        'supply them.</p>' % (WWW, WW, W)),
    summary=('Carried as ECH3418 by FAMU and Florida State at 3 credits — two institutions '
             'sharing one joint college, so one programme. USF numbers the same subject ECH4418 and '
             'UF numbers it ECH4403. No institution publishes a contact-hour figure.'),
    derivation='Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
)

add(
    cid='ECH3854', title='Chemical Engineering Computations', credits=4, hours=60,
    carriers=[('FAMU', 'Chemical Engineering Computations', 4, None),
              ('FSU', 'Chemical Engineering Computations', 4, None),
              ('USF', 'Engineering Computations', 3, '⚠ Three credits, and a broader title.')],
    prereq=(
        'IGNORE THE STATEWIDE PREREQUISITE - IT RESOLVES NOWHERE. It names ECH 3264, CGS 3460 and '
        'MAP 3305. This course is carried by FAMU, FSU and USF. ECH3264 is carried by the '
        'University of Florida ALONE, and UF does not carry this course. CGS3460 is carried by NO '
        'Florida public institution at all. MAP3305 is not carried by USF. Both dangling numbers '
        'are UF numbering, so the gate was contributed by an institution that does not teach the '
        'course. '
        'THE REAL GATE is material and energy balances plus the calculus sequence, with '
        'differential equations required or concurrent. Read your own catalogue. '
        'CARRIED AT 4 CREDITS by FAMU and FSU (one joint college) and at 3 by USF, which titles it '
        'Engineering Computations. '
        'EXPECT TO PROGRAM. This is where chemical engineering students learn to write code, and '
        'students who have never programmed find that harder than the numerical methods.'),
    lede=('<strong>Chemical Engineering Computations</strong> teaches the numerical methods that '
          'chemical engineering problems actually require, and in practice it is the course where '
          'the discipline learns to program. The statewide description: <strong>an introduction to '
          'the central concepts of practical numerical techniques using computers for solving '
          'chemical engineering problems</strong>.',
          '%s <strong>Almost nothing in the rest of the degree solves in closed form.</strong> '
          'Cubic equations of state, multicomponent flash calculations, reactor design equations '
          'and the transport partial differential equations are all numerical problems, and this is '
          'the course that makes them tractable. Taken seriously it makes the rest of the major '
          'noticeably easier.' % W),
    outcomes=['Write, debug and document <strong>programs</strong> in the language the institution '
              'uses — MATLAB, Python or both.',
              'Solve <strong>systems of linear equations</strong> and understand conditioning.',
              'Solve <strong>non-linear equations and systems</strong> by bisection, '
              'Newton-Raphson and quasi-Newton methods.',
              'Perform <strong>interpolation, curve fitting and regression</strong> on process data.',
              'Carry out <strong>numerical differentiation and integration</strong>.',
              'Solve <strong>ordinary differential equations</strong> and initial-value problems '
              'numerically.',
              'Apply these to <strong>chemical engineering problems</strong> — equations of state, '
              'flash calculations, reactor equations, unsteady balances.'],
    opt_outcomes=['Boundary-value problems and partial differential equations.',
                  'Optimisation methods.',
                  'Statistical analysis and design of experiments.',
                  'Process simulation software alongside the hand-written code.'],
    topics=['Programming fundamentals in MATLAB or Python.',
            'Errors, precision and conditioning.',
            'Linear systems and matrix methods.',
            'Roots of non-linear equations and systems.',
            'Regression and curve fitting.',
            'Numerical integration and differentiation.',
            'Numerical solution of ODEs.',
            'Applications to chemical engineering problems.'],
    opt_topics=['PDEs and boundary-value problems.', 'Optimisation.',
                'Statistics and experimental design.', 'Symbolic computation.'],
    resources=['Chapra &amp; Canale, <em>Numerical Methods for Engineers</em>, is the common text; '
               'Cutlip &amp; Shacham, <em>Problem Solving in Chemical Engineering with Numerical '
               'Methods</em>, is the discipline-specific one.',
               'MATLAB is the usual environment; Python with NumPy and SciPy is increasingly used '
               'and is free, which matters after graduation.',
               'Polymath appears in some Florida programmes, particularly alongside reactor design.'],
    career=('Named on the <strong>Chemical Engineer</strong> career path. Programming is now '
            'assumed of process engineers — for data analysis, for plant historian work, and for '
            'the modelling that sits under any optimisation project. %s <strong>It is also the most '
            'transferable skill in the degree</strong>, and the one that opens data and simulation '
            'roles to chemical engineers who want them.' % W),
    extra=(
        '<h3>%s The statewide prerequisite resolves nowhere, and here is the arithmetic</h3>'
        '<p>SCNS records the gate as <strong><code>ECH 3264</code>, <code>CGS 3460</code>, '
        '<code>MAP 3305</code></strong>. The carriers of this course are FAMU, Florida State and '
        'USF. Against that:</p>'
        '<table class="table table-sm"><thead><tr><th>Named course</th><th>Who carries it</th>'
        '<th>Resolves for a carrier of this course?</th></tr></thead><tbody>'
        '<tr><td><code>ECH3264</code> Elementary Transport Phenomena</td><td>University of Florida '
        '<strong>alone</strong></td><td>%s <strong>no — and UF does not carry this course</strong>'
        '</td></tr>'
        '<tr><td><code>CGS3460</code></td><td>%s <strong>no Florida public institution</strong></td>'
        '<td><strong>no — for anybody in the state</strong></td></tr>'
        '<tr><td><code>MAP3305</code> Engineering Mathematics</td><td>FAMU, FAU, Florida '
        'Polytechnic, Florida State</td><td>yes at FAMU and Florida State; <strong>not at USF'
        '</strong></td></tr>'
        '</tbody></table>'
        '<p>%s <strong>Both dangling numbers are University of Florida numbering</strong> — '
        '<code>ECH3264</code> is UF’s transport course and <code>CGS3460</code> is the shape of '
        'UF’s programming-for-engineers numbering. <strong>The prerequisite was contributed by '
        'an institution that does not teach the course.</strong></p>'
        '<p>%s It is worth knowing as a general lesson and not only about this number: <strong>a '
        'statewide prerequisite is contributed by one institution and is not a promise about '
        'yours.</strong> Read the gate from your own catalogue, every time.</p>'
        '<h3>Credits, and what the extra one buys</h3>'
        '<p>FAMU and Florida State carry it at <strong>4 credits</strong>; USF at <strong>3</strong>, '
        'under the broader title <em>Engineering Computations</em>. %s The difference is usually a '
        'scheduled computer laboratory session rather than additional theory. <strong>A transfer '
        'student moving from USF to the FAMU-FSU college is a credit short against the '
        'requirement</strong>, which is the sort of thing that surfaces in a final audit.</p>'
        % (WWW, W, WW, WW, W, W)),
    summary=('Three Florida public institutions carry ECH3854: FAMU and Florida State at 4 credits '
             '(one joint college) and USF at 3, titled Engineering Computations. ⚠ Its '
             'statewide prerequisite names three courses, none of which resolves at all three '
             'carriers and one of which has no public carrier in Florida.'),
    derivation=('Florida convention of 15 contact hours per credit at the 4-credit value carried by '
                'the FAMU-FSU college. ⚠ At USF the course is 3 credits and approximately 45 '
                'contact hours.'),
)

add(
    cid='ECH4123', title='Phase and Chemical Equilibria', credits=3, hours=45,
    carriers=[('UF', 'Phase and Chemical Equilibria', 3, None),
              ('USF', 'Chemical Engineering Thermodynamics II', 3, None)],
    prereq=(
        'Statewide prerequisite: ECH3101 Chemical Engineering Thermodynamics. That is the real gate '
        'and it is enforced - this course is the second half of thermodynamics and assumes the '
        'first half fluently. '
        'CARRIED BY UF AND USF ONLY, both at 3 credits. Neither FAMU nor FSU carries the number: '
        'the FAMU-FSU college distributes the mixture material through its separations and design '
        'sequence instead. So a student at one programme takes a dedicated course in this and a '
        'student at the other meets the same material inside other courses. '
        'TWO TITLES, ONE SUBJECT: UF names it by topic (Phase and Chemical Equilibria) and USF by '
        'position in the sequence (Chemical Engineering Thermodynamics II). The statewide title is '
        'Phase Equilibria.'),
    lede=('<strong>Phase and Chemical Equilibria</strong> is thermodynamics of mixtures — the half '
          'of the subject that matters most to chemical engineers, because real processes are '
          'mixtures whose composition changes. The statewide description: <strong>application of '
          'thermodynamic principles to systems of variable composition, including the study of '
          'phase and chemical equilibria</strong>.',
          '%s <strong>This is the course that makes separations possible.</strong> Every '
          'distillation column, every extraction, every flash drum is designed from phase '
          'equilibrium data, and the reason chemical engineering thermodynamics has a difficult '
          'reputation — fugacity, activity, excess properties — is concentrated here.' % WW),
    outcomes=['Apply <strong>partial molar properties</strong> and the Gibbs-Duhem equation.',
              'Compute <strong>fugacity and fugacity coefficients</strong> for pure species and in '
              'mixtures.',
              'Use <strong>activity coefficient models</strong> — Margules, van Laar, Wilson, NRTL, '
              'UNIQUAC, UNIFAC — and choose among them.',
              'Construct and read <strong>vapour-liquid equilibrium</strong> diagrams, and perform '
              'bubble-point, dew-point and flash calculations.',
              'Analyse <strong>azeotropes</strong> and liquid-liquid equilibrium.',
              'Compute <strong>chemical reaction equilibrium</strong>, including multiple '
              'simultaneous reactions.'],
    opt_outcomes=['Electrolyte solutions.',
                  'Solid-liquid equilibrium and crystallisation.',
                  'Equation-of-state approaches to mixtures at high pressure.',
                  'Thermodynamic property estimation software.'],
    topics=['Partial molar properties; the chemical potential.',
            'Fugacity and fugacity coefficients.',
            'Ideal and non-ideal solutions; excess properties.',
            'Activity coefficient models and parameter estimation.',
            'Vapour-liquid equilibrium; bubble, dew and flash calculations.',
            'Azeotropy; liquid-liquid and vapour-liquid-liquid equilibrium.',
            'Chemical reaction equilibrium.'],
    opt_topics=['Electrolytes.', 'Solid-liquid equilibrium.', 'High-pressure phase behaviour.',
                'Membrane and osmotic equilibria.'],
    resources=['Smith, Van Ness &amp; Abbott, continuing from the first course; Prausnitz, '
               'Lichtenthaler &amp; de Azevedo, <em>Molecular Thermodynamics of Fluid-Phase '
               'Equilibria</em>, for the serious treatment.',
               'MATLAB or Python for the iterative flash and activity-coefficient calculations — '
               'they are not hand calculations.',
               'Aspen Plus or HYSYS property packages, where the institution introduces them: '
               'choosing the right property method is a genuinely employable judgement.'],
    career=('Named on the <strong>Chemical Engineer</strong> career path. Phase equilibrium is the '
            'basis of every separation, and in industry the ability to choose and validate a '
            'thermodynamic property package in a simulator is a specific and well-paid skill — '
            'getting it wrong is one of the commonest causes of a process design that does not work '
            'when built.'),
    extra=(
        '<h3>%s Two of the four programmes have no course for this, and that is not a gap</h3>'
        '<p><strong>UF and USF carry <code>ECH4123</code>; FAMU and Florida State do not.</strong> '
        'The FAMU-FSU college distributes the mixture and phase-equilibrium material through its '
        'separations and design sequence rather than giving it a dedicated course.</p>'
        '<p>%s <strong>Both approaches are legitimate and the consequence is a transfer '
        'question, not a quality one.</strong> A student moving <em>into</em> UF or USF from the '
        'FAMU-FSU college may be asked to show this specific course and will not have it under this '
        'number; a student moving the other way will find the material already assumed. <strong>Take '
        'the topic list, not the transcript line.</strong></p>'
        '<h3>Named by topic at one, by sequence position at the other</h3>'
        '<p>UF calls it <em>Phase and Chemical Equilibria</em>; USF calls it <em>Chemical '
        'Engineering Thermodynamics II</em>; the state calls it <em>Phase Equilibria</em>. %s '
        '<strong>Three names, one course.</strong> USF’s naming is the more informative if you '
        'are planning a sequence and UF’s if you are looking for a topic; neither signals a '
        'difference in content.</p>' % (WW, WW, W)),
    summary=('Two Florida public institutions carry ECH4123, both at 3 credits: UF as Phase and '
             'Chemical Equilibria and USF as Chemical Engineering Thermodynamics II. FAMU and '
             'Florida State do not carry the number. No institution publishes a contact-hour '
             'figure.'),
    derivation='Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
)

add(
    cid='ECH4504', title='Kinetics and Reactor Design', credits=3, hours=45,
    carriers=[('FAMU', 'Kinetics and Reactor Design', 3, None),
              ('FIU', 'Introduction to Chemical Reaction Engineering', 3,
               '⚠ FIU carries the course but awards no chemical engineering degree — it '
               'is a service and elective offering.'),
              ('FSU', 'Kinetics and Reactor Design', 3, None),
              ('UF', 'Chemical Kinetics and Reactor Design', 4, '⚠ Four credits.'),
              ('USF', 'Kinetics and Reaction Engineering', 3, None)],
    prereq=(
        'Thermodynamics and transport phenomena. The statewide prerequisite field contains PROSE - '
        '"THE THERMODYNAMICS, TRANSPORT PHENOMENA" - rather than course numbers, so it names no '
        'course you can look up. Read your own catalogue. '
        'THE MOST WIDELY CARRIED CHEMICAL ENGINEERING COURSE IN FLORIDA: five carriers, and the '
        'only ECH number shared with FIU, which teaches it without awarding the degree. '
        'CREDITS: 3 at FAMU, FIU, FSU and USF; 4 at UF. '
        'FOUR TITLES, ONE SUBJECT - Kinetics and Reactor Design (FAMU, FSU), Chemical Kinetics and '
        'Reactor Design (UF), Kinetics and Reaction Engineering (USF), Introduction to Chemical '
        'Reaction Engineering (FIU). Register by the number.'),
    lede=('<strong>Kinetics and Reactor Design</strong> is the course the profession is named for: '
          'the reactor is the one piece of equipment that makes a chemical plant chemical, and this '
          'is where you learn to size it. The statewide description covers <strong>elementary, '
          'complex and catalytic kinetics as applied to the engineering design of batch and backmix '
          'reactors</strong>.',
          '%s <strong>It is the most widely carried chemical engineering course in the state</strong> '
          '— five institutions, including FIU, which teaches it although it awards no chemical '
          'engineering degree. That breadth is unusual in this prefix and makes this one of the few '
          'ECH numbers a student is likely to find wherever they are.'),
    outcomes=['Determine <strong>rate laws</strong> from experimental data by differential and '
              'integral methods.',
              'Apply the <strong>design equations</strong> for batch, CSTR, PFR and packed-bed '
              'reactors.',
              'Size <strong>reactors in series and parallel</strong>, and choose a configuration '
              'for a given conversion.',
              'Analyse <strong>multiple reactions</strong> and optimise for selectivity and yield, '
              'not only conversion.',
              'Apply <strong>energy balances to reactors</strong>, including adiabatic and '
              'non-isothermal operation, and assess <strong>thermal runaway</strong>.',
              'Analyse <strong>catalytic reactions</strong>: mechanisms, adsorption isotherms, '
              'rate-limiting steps and deactivation.',
              'Assess <strong>diffusion limitations</strong> in catalyst particles — the Thiele '
              'modulus and effectiveness factor.'],
    opt_outcomes=['Non-ideal flow and residence-time distribution analysis.',
                  'Bioreactors and enzyme kinetics.',
                  'Polymerisation reaction engineering.',
                  'Reactor simulation in Polymath, MATLAB or Aspen.'],
    topics=['Mole balances and the reactor design equations.',
            'Conversion and reactor sizing; reactors in series.',
            'Rate laws, stoichiometry and data analysis.',
            'Isothermal reactor design.',
            'Multiple reactions; selectivity and yield.',
            'Energy balances and non-isothermal reactors; multiple steady states.',
            'Catalysis, catalytic reactors and deactivation.',
            'Diffusion and reaction; the Thiele modulus.'],
    opt_topics=['Residence-time distribution and non-ideal reactors.',
                'Bioreactors and enzyme kinetics.', 'Polymerisation reactors.',
                'Reactor safety and runaway analysis in depth.'],
    resources=['Fogler, <em>Elements of Chemical Reaction Engineering</em> — close to universal, '
               'and its companion website and Polymath problems are part of how most programmes '
               'teach it.',
               'Levenspiel, <em>Chemical Reaction Engineering</em>, is the classic alternative.',
               'Polymath, MATLAB or Python for the coupled differential equations; the reactor '
               'design equations are solved numerically almost from the start.'],
    career=('Named on the <strong>Chemical Engineer</strong> career path. Reaction engineering leads '
            'into process design, catalysis research, pharmaceutical and specialty chemicals '
            'manufacturing, and any role where yield and selectivity are the commercial question. '
            '%s <strong>The thermal-runaway material is also safety material</strong> — it is the '
            'analysis behind several of the industry’s worst accidents, and employers notice '
            'students who can discuss it.' % W),
    extra=(
        '<h3>Four titles, one subject</h3>'
        '<table class="table table-sm"><tbody>'
        '<tr><td>FAMU, Florida State</td><td>Kinetics and Reactor Design</td></tr>'
        '<tr><td>University of Florida</td><td>Chemical Kinetics and Reactor Design</td></tr>'
        '<tr><td>University of South Florida</td><td>Kinetics and Reaction Engineering</td></tr>'
        '<tr><td>FIU</td><td>Introduction to Chemical Reaction Engineering</td></tr>'
        '</tbody></table>'
        '<p>%s <strong>Branding, not divergence.</strong> All five teach the Fogler curriculum and '
        'the statewide description covers all of them. Register by the number.</p>'
        '<h3>%s FIU teaches this and awards no chemical engineering degree</h3>'
        '<p>FIU carries three <code>ECH</code> numbers — this one, <code>ECH3271</code> and '
        '<code>ECH4826</code> — while awarding degrees in seven <em>other</em> engineering CIP '
        'codes and none in chemical engineering. %s <strong>So an FIU student can take reaction '
        'engineering and cannot major in the field.</strong> It is a useful elective for '
        'environmental, biomedical and materials students there; it is not the start of a chemical '
        'engineering degree, and a student intending that degree should read the '
        '<a href="/careers/chemical-engineer">Chemical Engineer</a> path before planning around '
        'it.</p>'
        '<h3>UF carries it at four credits</h3>'
        '<p>Four of the five carriers run it at <strong>3 credits</strong>; <strong>UF at '
        '4</strong>. The additional credit generally reflects a heavier computational component. '
        '%s A student transferring into UF with the 3-credit version is a credit short against the '
        'requirement.</p>' % (W, WW, WW, W)),
    summary=('Five Florida public institutions carry ECH4504 — the most widely carried chemical '
             'engineering course in the state. FAMU, FIU, Florida State and USF run it at 3 '
             'credits and UF at 4. ⚠ FIU carries it without awarding a chemical engineering '
             'degree. No institution publishes a contact-hour figure.'),
    derivation=('Florida convention of 15 contact hours per credit at the 3-credit value carried by '
                'four of the five. ⚠ At UF the course is 4 credits and approximately 60 '
                'contact hours.'),
)

add(
    cid='ECH4323', title='Process Control', credits=3, hours=45,
    carriers=[('FAMU', 'Process Control', 3, None),
              ('FSU', 'Process Control', 3, None),
              ('UF', 'Process Control Theory', 3, None),
              ('USF', 'Process Dynamics and Control', 3, None)],
    prereq=(
        'Differential equations, transport phenomena and thermodynamics; Laplace transforms are '
        'assumed from the first week and are the thing to revise beforehand. The statewide '
        'prerequisite reads "PROCESS SYSTEMS ANALYSIS" - prose naming a subject rather than a '
        'course number, so there is nothing to look up. Read your own catalogue. '
        'CARRIED BY ALL FOUR Florida chemical engineering programmes at 3 credits: FAMU, FSU, UF '
        '(Process Control Theory) and USF (Process Dynamics and Control). '
        'CHECK WHETHER A SEPARATE LABORATORY IS REQUIRED. FAMU, FSU and UF also carry ECH4323L, a '
        '1-credit process control laboratory. USF does not.'),
    lede=('<strong>Process Control</strong> is what connects the degree to a working plant. Every '
          'other course assumes steady state; this one asks what happens when the feed composition '
          'changes at three in the morning. The statewide description: <strong>the analysis and '
          'automatic control of simple process systems in chemical engineering</strong>.',
          '%s <strong>It is the course that most resembles electrical engineering</strong>, and '
          'that surprises people: Laplace transforms, transfer functions, block diagrams, Bode '
          'plots and stability criteria are the working vocabulary. Students who disliked '
          'differential equations find this the least chemical course in the major; students who '
          'enjoy it often end up in control and automation careers.' % WW),
    outcomes=['Derive <strong>dynamic models</strong> of process units from unsteady balances, and '
              'linearise them.',
              'Use <strong>Laplace transforms and transfer functions</strong> to analyse first- and '
              'second-order process response.',
              'Construct and reduce <strong>block diagrams</strong> of a controlled process.',
              'Describe the behaviour of <strong>P, PI and PID controllers</strong> and select '
              'among them.',
              'Assess <strong>closed-loop stability</strong> by the Routh, root-locus and frequency '
              'response (Bode, Nyquist) methods.',
              '<strong>Tune a controller</strong> using Ziegler-Nichols, IMC or equivalent rules.',
              'Describe the <strong>instrumentation</strong>: sensors, transmitters, final control '
              'elements and control valves.'],
    opt_outcomes=['Cascade, feedforward and ratio control.',
                  'Multivariable control and interaction analysis.',
                  'Model predictive control.',
                  'Distributed control systems and plant-wide control strategy.'],
    topics=['Process dynamics; unsteady-state modelling and linearisation.',
            'Laplace transforms and transfer functions.',
            'First-, second- and higher-order response; dead time.',
            'Feedback control and controller modes.',
            'Block diagrams and closed-loop transfer functions.',
            'Stability analysis; root locus and frequency response.',
            'Controller tuning.',
            'Sensors, final control elements and control valves.'],
    opt_topics=['Cascade, feedforward and ratio control.', 'Multivariable and decoupling control.',
                'Model predictive control.', 'Plant-wide control and safety instrumented systems.'],
    resources=['Seborg, Edgar, Mellichamp &amp; Doyle, <em>Process Dynamics and Control</em> — '
               'the standard, and the source of USF’s title.',
               'Marlin and Riggs are common alternatives.',
               'MATLAB with the Control System Toolbox and Simulink; Simulink in particular makes '
               'the closed-loop behaviour visible in a way the algebra does not.'],
    career=('Named on the <strong>Chemical Engineer</strong> career path. Control and automation is '
            'one of the most reliable employment routes out of the degree and one of the least '
            'sensitive to the commodity cycle — every plant needs its controls maintained and '
            'improved whatever the market is doing. In Florida it carries into power generation, '
            'water treatment, phosphate processing, food and beverage, and pharmaceutical '
            'manufacturing, where validated control systems are a regulatory requirement.'),
    extra=(
        '<h3>%s Is the laboratory a separate registration?</h3>'
        '<p>It depends where you are. <strong>FAMU, Florida State and UF carry a separate 1-credit '
        '<code>ECH4323L</code> process control laboratory; USF does not.</strong> %s If your '
        'programme runs the laboratory as its own course, <strong>register for both</strong> — '
        'they are usually corequisites, and missing one can mean repeating the other.</p>'
        '<h3>Four titles and a useful signal in one of them</h3>'
        '<p>FAMU and Florida State call it <em>Process Control</em>, UF <em>Process Control '
        'Theory</em>, USF <em>Process Dynamics and Control</em>. %s <strong>USF’s is the most '
        'descriptive</strong> — roughly the first third of every version of this course is process '
        '<em>dynamics</em> with no controller in sight, and students who expect to start with '
        'controllers find that disorienting. UF’s &ldquo;Theory&rdquo; is a fair warning in the '
        'other direction.</p>'
        '<h3>%s Revise Laplace transforms before the term starts</h3>'
        '<p>This course uses them from the first week and does not teach them. Most students last '
        'met them in differential equations, possibly two years earlier. <strong>A few hours spent '
        'on transforms, partial fractions and inversion before the term is the highest-return '
        'preparation available for any course in this major.</strong></p>' % (WW, W, W, WW)),
    summary=('All four Florida chemical engineering programmes carry ECH4323 at 3 credits. FAMU, '
             'Florida State and UF also carry a separate 1-credit laboratory, ECH4323L; USF does '
             'not. No institution publishes a contact-hour figure.'),
    derivation='Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
)

add(
    cid='ECH4323L', title='Process Control Laboratory', credits=1, hours=45,
    carriers=[('FAMU', 'Process Control Lab', 1, None),
              ('FSU', 'Process Control Laboratory', 1, None),
              ('UF', 'Chemical Engineering Lab 5', 1,
               '⚠ UF names its laboratories by position in its own sequence rather than by '
               'subject.')],
    prereq=(
        'Process control (ECH4323), normally as a corequisite rather than a prerequisite - check '
        'which, because if the two are reciprocal corequisites then failing either means repeating '
        'both. '
        'CARRIED BY FAMU, FSU AND UF AT 1 CREDIT. USF does not carry a separate process control '
        'laboratory. Since FAMU and FSU share one joint college, this is TWO independent '
        'programmes. '
        'ONE CREDIT, THREE HOURS A WEEK. A laboratory consumes far more scheduled time than its '
        'credit value suggests, and the reports consume more again. Plan the term around the hours, '
        'not the credits. '
        'UF CALLS IT "CHEMICAL ENGINEERING LAB 5" - a sequence name, not a different subject.'),
    lede=('<strong>Process Control Laboratory</strong> is where the transfer functions meet real '
          'equipment that does not behave the way the model says. Students tune controllers on '
          'physical processes — typically level, flow, temperature and pressure loops — and learn '
          'that identification, noise and valve behaviour matter as much as the mathematics.',
          '%s <strong>This is the most directly employable single credit in the degree.</strong> '
          'Tuning a real loop, reading a trend, and recognising a saturating valve are things '
          'employers ask about at interview and that no lecture can teach.'),
    outcomes=['Identify a <strong>process model</strong> experimentally from step and pulse tests.',
              'Implement and <strong>tune P, PI and PID controllers</strong> on physical processes '
              'and evaluate the result.',
              'Compare <strong>measured response with predicted response</strong> and account for '
              'the difference.',
              'Operate and calibrate <strong>instrumentation</strong>: sensors, transmitters and '
              'control valves.',
              'Work safely with pressurised, heated and moving equipment.',
              'Write a <strong>professional laboratory report</strong> with an honest treatment of '
              'experimental uncertainty.'],
    opt_outcomes=['Cascade or feedforward control implemented on real equipment.',
                  'Work on a distributed control system or PLC interface.',
                  'Data acquisition and programming for instrumentation.'],
    topics=['Laboratory and process safety.',
            'Instrumentation, calibration and signal conditioning.',
            'Experimental process identification; step testing.',
            'Feedback loop implementation and tuning.',
            'Level, flow, temperature and pressure control experiments.',
            'Data acquisition and analysis.',
            'Technical reporting.'],
    opt_topics=['Advanced control structures on real equipment.',
                'DCS or PLC programming.', 'Control valve characterisation.'],
    resources=['The lecture text — usually Seborg — plus the institution’s own laboratory '
               'manual, which is the operative document.',
               'MATLAB or the vendor’s software for data acquisition and analysis; LabVIEW '
               'appears at some institutions.',
               'A bound laboratory notebook, where required — several programmes assess it, and '
               'keeping one properly is itself a professional skill.'],
    career=('Named on the <strong>Chemical Engineer</strong> career path. Hands-on control '
            'experience distinguishes a graduate applying for a plant process or controls role, and '
            'it is the sort of thing to put on a r&eacute;sum&eacute; specifically rather than '
            'leaving inside a course title.'),
    extra=(
        '<h3>%s One credit is not one hour</h3>'
        '<p>A 1-credit laboratory typically meets for <strong>three hours a week</strong>, and the '
        'report writing generally takes at least as long again. <strong>Students plan their terms '
        'around credits and are caught by hours.</strong> Treat this as a three-to-six hour '
        'commitment, not a one-hour one.</p>'
        '<h3>%s Check whether it is a reciprocal corequisite</h3>'
        '<p>Where a lecture and its laboratory each list the other as a corequisite, <strong>neither '
        'can be taken alone and failing either means repeating both.</strong> That is a cohort '
        'problem rather than a term problem in a small programme where the course runs once a year. '
        '<strong>Ask before you register.</strong></p>'
        '<h3>USF has no separate laboratory under this number</h3>'
        '<p>USF carries <code>ECH4323</code> without a matching <code>ECH4323L</code>; its '
        'laboratory work sits in <code>ECH3240L</code> and <code>ECH4241L</code>. %s <strong>This '
        'is packaging, not a missing requirement</strong> — but it does mean a transfer student '
        'can arrive with a control course and no control laboratory, or the reverse, and a degree '
        'audit will notice.</p>' % (WW, WW, W)),
    summary=('Three Florida public institutions carry ECH4323L at 1 credit: FAMU, Florida State '
             '(one joint college) and UF, which titles it Chemical Engineering Lab 5. USF does not '
             'carry a separate process control laboratory. No institution publishes a contact-hour '
             'figure.'),
    derivation=('Anchored on the Florida laboratory convention of three scheduled hours a week for '
                'a 1-credit laboratory over a 15-week term. ⚠ Gulf Coast State College, one of '
                'the few Florida institutions that publishes laboratory hours, gives "Credit hours: '
                '1 / Lab hours: 3" for its 1-credit science laboratories, which supports the '
                'figure; no ECH carrier publishes hours directly.'),
)

add(
    cid='ECH4404L', title='Unit Operations Laboratory', credits=3, hours=90,
    carriers=[('FAMU', 'Unit Operations Lab', 3, None),
              ('FSU', 'Unit Operations Laboratory', 3, None),
              ('UF', 'Separation and Mass Transfer Operations Laboratory', 2,
               '⚠ Two credits, and narrower in scope — the mass-transfer laboratory rather '
               'than the general unit operations laboratory.')],
    prereq=(
        'Transport phenomena and separations, and normally senior standing. The statewide '
        'prerequisite reads "CH E OPERATIONS LAB" - prose naming a previous laboratory rather than '
        'a course number, so there is nothing to look up. Read your own catalogue. '
        'THE SCOPE AND THE CREDIT DIFFER, AND SO DOES THE WORKLOAD. FAMU and FSU run it as the '
        'general unit operations laboratory at 3 credits. UF runs it at 2 credits as the laboratory '
        'for separations and mass transfer, which is what the statewide description actually '
        'specifies. Expect a substantially larger time commitment at the FAMU-FSU college. '
        'THIS IS THE SIGNATURE LABORATORY OF THE DEGREE: real industrial-scale equipment, real '
        'data, and reports written to industry standard. It is also where most of the term goes.'),
    lede=('<strong>Unit Operations Laboratory</strong> is the course chemical engineering graduates '
          'remember and the one employers ask about. Students run pilot-scale equipment — '
          'distillation columns, heat exchangers, pumps, dryers, absorbers — take real data from '
          'processes that leak, drift and refuse to reach steady state, and write it up as a '
          'professional engineer would. The statewide description is narrower: <strong>laboratory '
          'work in unit operations involving mass transfer</strong>.',
          '%s <strong>Budget for it honestly.</strong> This is routinely the heaviest course in the '
          'curriculum relative to its credit value: the laboratory sessions are long, the equipment '
          'does not cooperate, and the reports are the real assessment. Students who treat it as a '
          '3-credit course rather than a term-defining one are the ones who fall behind.' % WWW),
    outcomes=['Plan an <strong>experiment</strong> against an objective, including what to measure '
              'and how precisely.',
              'Operate <strong>pilot-scale process equipment</strong> safely and competently.',
              'Acquire and reduce <strong>real process data</strong>, including recognising and '
              'handling bad data.',
              'Compare <strong>measured performance with theoretical prediction</strong> and '
              'explain the discrepancy rather than apologising for it.',
              'Carry out a rigorous <strong>uncertainty and error analysis</strong>.',
              'Write a <strong>professional technical report</strong> and deliver an oral '
              'presentation on it.',
              'Work effectively in a <strong>laboratory team</strong> with divided responsibilities.'],
    opt_outcomes=['Statistical design of experiments.',
                  'Process optimisation from experimental data.',
                  'Computer data acquisition and instrumentation programming.',
                  'Economic evaluation of the process studied.'],
    topics=['Laboratory and process safety; hazard assessment before each experiment.',
            'Experimental design and measurement planning.',
            'Distillation column operation and efficiency.',
            'Heat exchanger performance.',
            'Absorption, extraction or membrane separation experiments.',
            'Fluid flow, pumps and pressure drop.',
            'Drying, filtration or evaporation, depending on the equipment available.',
            'Error and uncertainty analysis; technical reporting and presentation.'],
    opt_topics=['Reaction engineering experiments.', 'Process control experiments.',
                'Design of experiments and response-surface methods.'],
    resources=['The institution’s own laboratory manual is the operative document; no textbook '
               'governs this course.',
               'Geankoplis and Perry’s <em>Chemical Engineers’ Handbook</em> for the '
               'correlations and property data the analysis needs.',
               'A style guide for technical reports, and spreadsheet or MATLAB tooling for the '
               'data reduction and error propagation.'],
    career=('Named on the <strong>Chemical Engineer</strong> career path, and it is the strongest '
            'item on an entry-level r&eacute;sum&eacute; after the capstone. %s <strong>Name the '
            'specific equipment you operated</strong> — a graduate who has run a distillation '
            'column and can discuss why the tray efficiency came out at 60%% is a materially '
            'different candidate from one who has only calculated one.' % W),
    extra=(
        '<h3>%s Three credits here, two credits there — and a different scope</h3>'
        '<table class="table table-sm"><thead><tr><th>Institution</th><th>Credits</th>'
        '<th>What it covers</th></tr></thead><tbody>'
        '<tr><td>FAMU, Florida State</td><td><strong>3</strong></td><td>the <strong>general unit '
        'operations</strong> laboratory — flow, heat transfer, separations</td></tr>'
        '<tr><td>University of Florida</td><td><strong>2</strong></td><td>the <strong>separations '
        'and mass transfer</strong> laboratory specifically</td></tr>'
        '</tbody></table>'
        '<p>%s <strong>The statewide description sides with UF</strong> — it says &ldquo;laboratory '
        'work in unit operations involving <em>mass transfer</em>&rdquo; and titles the number '
        '&ldquo;Chemical Engineering Operations Lab 2&rdquo;, implying a sequence. So UF is running '
        'the number as defined and the FAMU-FSU college is running something broader on it.</p>'
        '<p>%s <strong>Neither is wrong and the difference is real work.</strong> Half again the '
        'credit is half again the laboratory time and the reports. A student transferring in with '
        'the 2-credit version is a credit short; one transferring out with the 3-credit version may '
        'find a credit with nowhere to go. <strong>Send the list of experiments performed</strong> — '
        'it is the only document that says what was actually covered.</p>'
        '<h3>%s Safety is assessed here, not just mentioned</h3>'
        '<p>This is the first time most students operate equipment that can genuinely hurt them: '
        'steam, pressure, rotating machinery, hot surfaces and chemicals in quantity. Expect a '
        'hazard assessment to be required <em>before</em> each experiment and to be graded. '
        '<strong>Treat it as the professional habit it is meant to become</strong> — it is the '
        'same procedure a plant requires before any non-routine operation.</p>' % (WWW, W, WW, WW)),
    summary=('Three Florida public institutions carry ECH4404L. FAMU and Florida State (one joint '
             'college) run it at 3 credits as the general unit operations laboratory; UF runs it at '
             '2 credits as the separations and mass transfer laboratory, which is the scope the '
             'statewide description specifies. No institution publishes a contact-hour figure.'),
    derivation=('Anchored on the Florida laboratory convention of two to three scheduled hours per '
                'credit: a 3-credit unit operations laboratory typically meets for six hours a week '
                'over a 15-week term. ⚠ The figure describes SCHEDULED laboratory time only; '
                'report writing on this course routinely takes as long again, and at UF the course '
                'is 2 credits and proportionally fewer hours.'),
)

add(
    cid='ECH4604', title='Process Design and Economics', credits=4, hours=60,
    carriers=[('FAMU', 'Chemical Engineering Process Design', 4, None),
              ('FSU', 'Chemical Engineering Process Design', 4, None),
              ('UF', 'Process Economics and Optimization', 3,
               '⚠ Three credits, and named for the economics rather than the design.')],
    prereq=(
        'The transport, separations, kinetics and thermodynamics sequence, and normally senior '
        'standing. The statewide prerequisite reads "CHEMICAL ENGINEERING OPERATIONS" - prose '
        'naming a subject rather than a course number. Read your own catalogue. '
        'CARRIED AT 4 CREDITS by FAMU and FSU as Chemical Engineering Process Design, and at 3 by '
        'UF as Process Economics and Optimization. Since FAMU and FSU share one joint college, this '
        'is TWO independent programmes. '
        'THIS IS THE CAPSTONE-FACING COURSE. FAMU and FSU continue into ECH4615; USF runs its own '
        'design sequence at ECH4605 and ECH4615C and does not carry this number at all. '
        'THE SUBJECT IS MONEY AS MUCH AS ENGINEERING - capital cost estimation, profitability and '
        'optimisation - and students who expected more analysis are frequently surprised.'),
    lede=('<strong>Process Design and Economics</strong> is where the degree stops asking whether '
          'something can be built and starts asking whether it should be. The statewide '
          'description: <strong>investment requirements, cost estimates and profitability analyses '
          'of chemical processes for design and development</strong>.',
          '%s <strong>It is the course that most resembles the actual job.</strong> Practising '
          'process engineers spend far more time on capital estimates, payback periods and '
          'debottlenecking economics than on differential equations, and this is usually the first '
          'time a chemical engineering student is asked to defend a technical decision on financial '
          'grounds.' % WW),
    outcomes=['Estimate <strong>equipment and capital costs</strong> using published correlations, '
              'cost indices and scaling exponents.',
              'Estimate <strong>operating costs</strong> and construct a full cost of production.',
              'Evaluate <strong>profitability</strong> using payback period, net present value, '
              'discounted cash flow and rate of return.',
              'Apply the <strong>time value of money</strong>, depreciation and taxation to project '
              'evaluation.',
              'Carry out <strong>process optimisation</strong>, including sensitivity analysis on '
              'the economic assumptions.',
              'Synthesise and evaluate <strong>alternative process routes</strong> to the same '
              'product.',
              'Apply <strong>heat integration</strong> and pinch analysis to reduce utility cost.'],
    opt_outcomes=['Process simulation with costing modules (Aspen Economic Evaluation).',
                  'Risk analysis and project uncertainty.',
                  'Safety and environmental cost in project evaluation.',
                  'Linear programming and formal optimisation methods.'],
    topics=['Cost indices, scaling and capital cost estimation.',
            'Estimating fixed capital investment and working capital.',
            'Operating cost and cost of production.',
            'Time value of money; depreciation and taxes.',
            'Profitability measures and project selection.',
            'Optimisation and sensitivity analysis.',
            'Process synthesis and flowsheet alternatives.',
            'Heat integration and pinch analysis.'],
    opt_topics=['Simulation-based costing.', 'Risk and uncertainty analysis.',
                'Environmental and safety economics.', 'Linear and non-linear programming.'],
    resources=['Turton et al., <em>Analysis, Synthesis and Design of Chemical Processes</em>; '
               'Peters, Timmerhaus &amp; West, <em>Plant Design and Economics for Chemical '
               'Engineers</em> — both standard, and both with the cost correlations the '
               'assignments need.',
               'Aspen Plus or HYSYS with the economic evaluation modules, where available.',
               'Spreadsheets, seriously — discounted cash flow work is spreadsheet work, and doing '
               'it cleanly is a marketable habit.'],
    career=('Named on the <strong>Chemical Engineer</strong> career path. This is the course that '
            'points at the roles chemical engineers actually get promoted into — project '
            'engineering, process economics, technical management and consulting — and the '
            'vocabulary it teaches is what lets an engineer make a case to people who control '
            'budgets.'),
    extra=(
        '<h3>%s Named for the design at one college and for the economics at the other</h3>'
        '<table class="table table-sm"><thead><tr><th>Institution</th><th>Title</th><th>Credits</th>'
        '</tr></thead><tbody>'
        '<tr><td>FAMU, Florida State</td><td>Chemical Engineering Process Design</td>'
        '<td><strong>4</strong></td></tr>'
        '<tr><td>University of Florida</td><td>Process Economics and Optimization</td>'
        '<td><strong>3</strong></td></tr>'
        '</tbody></table>'
        '<p>%s <strong>The titles are a real signal here, not branding.</strong> The statewide '
        'description is entirely economic — investment, cost estimates, profitability — which is '
        'UF’s reading. The FAMU-FSU college carries a fourth credit and calls it design, which '
        'suggests the flowsheet synthesis and equipment design work is inside this course rather '
        'than only in the sequel. <strong>Ask for the week-by-week schedule if you need to know '
        'how much design as against economics you will get.</strong></p>'
        '<h3>Where the sequence goes next, and USF is different again</h3>'
        '<p>FAMU and Florida State continue into <code>ECH4615</code>. %s <strong>USF does not '
        'carry <code>ECH4604</code> at all</strong>, running its own design sequence as '
        '<code>ECH4605</code> <em>Product and Process Systems Engineering</em> and '
        '<code>ECH4615C</code> <em>Product and Process Design</em>, with <code>ECH4680C</code> '
        '<em>Product Development</em> alongside. <strong>So three of the four Florida programmes '
        'take three different routes through design</strong>, and a transfer at this point in the '
        'degree is genuinely difficult. <strong>If you are considering one, raise it with both '
        'departments before the junior year, not during the senior one.</strong></p>' % (WW, WW, W)),
    summary=('Three Florida public institutions carry ECH4604. FAMU and Florida State (one joint '
             'college) run it at 4 credits as Chemical Engineering Process Design; UF runs it at 3 '
             'as Process Economics and Optimization. USF does not carry the number, running its own '
             'design sequence instead. No institution publishes a contact-hour figure.'),
    derivation=('Florida convention of 15 contact hours per credit at the 4-credit value carried by '
                'the FAMU-FSU college. ⚠ At UF the course is 3 credits and approximately 45 '
                'contact hours.'),
)

add(
    cid='ECH4714', title='Chemical Process Safety', credits=3, hours=45,
    carriers=[('UF', 'Chemical Process Safety', 3, None)],
    prereq=(
        'Transport phenomena, thermodynamics and reaction engineering; normally senior standing. '
        'The statewide prerequisite field is blank. '
        'CARRIED BY THE UNIVERSITY OF FLORIDA ALONE. This is a SINGLE-INSTITUTION course and '
        'everything on this page should be read as a description of UF practice rather than a '
        'Florida norm. '
        'USF TEACHES THE SAME SUBJECT UNDER A DIFFERENT NUMBER: ECH4715 Chemical Process Safety and '
        'Ethics, a corequisite of its design course ECH4605. The FAMU-FSU college carries neither, '
        'distributing the material through its design sequence. So only two of the four Florida '
        'programmes teach process safety as a standalone course. '
        'THE STATEWIDE TITLE IS STALE: it reads "Safety & Experimental Evaluation-Upper" and says '
        'the course is "integrated with ECH 4224L". UF, which contributed that record, now titles '
        'it Chemical Process Safety.'),
    lede=('<strong>Chemical Process Safety</strong> is the course that separates chemical '
          'engineering from every other discipline’s treatment of safety, because the hazards are '
          'not incidental to the process — they are the process, held under control. The statewide '
          'description covers <strong>laboratory and process safety and analysis with emphasis on '
          'prevention and mitigation, and experiment design, evaluation and presentation of '
          'results</strong>.',
          '%s <strong>Safety is not a compliance topic in this profession; it is the profession.</strong> '
          'Bhopal, Flixborough, Texas City and Piper Alpha are all chemical process failures, and '
          'each is taught here not as history but as an analysis a competent engineer could have '
          'done beforehand. %s <strong>Employers ask about this course by name.</strong>' % (WW, W)),
    outcomes=['Apply the <strong>fundamentals of toxicology and industrial hygiene</strong>, '
              'including exposure limits and routes of entry.',
              'Analyse <strong>fires and explosions</strong>: flammability limits, flash points, '
              'autoignition, deflagration and detonation, dust explosions.',
              'Estimate <strong>source terms and dispersion</strong> for a release.',
              'Design and size <strong>pressure relief systems</strong>.',
              'Carry out a <strong>hazard identification study</strong> — HAZOP, what-if, '
              'checklist — on a process.',
              'Apply <strong>risk assessment</strong> methods including fault trees, event trees '
              'and layers of protection analysis.',
              'Analyse <strong>runaway reactions</strong> and the thermal stability of a process.',
              'Explain the <strong>regulatory framework</strong>: OSHA Process Safety Management, '
              'EPA Risk Management Program, and the role of the CSB.'],
    opt_outcomes=['Safety instrumented systems and SIL determination.',
                  'Inherently safer design principles.',
                  'Case study analysis of major incidents in depth.',
                  'Management of change and process safety culture.'],
    topics=['Toxicology, industrial hygiene and exposure assessment.',
            'Flammability, fires and explosions.',
            'Source models and dispersion of releases.',
            'Relief system design and sizing.',
            'Hazard identification: HAZOP and related methods.',
            'Quantitative risk assessment; fault and event trees.',
            'Reactive chemical hazards and runaway reactions.',
            'OSHA PSM, EPA RMP and the regulatory framework.',
            'Case histories.'],
    opt_topics=['Inherently safer design.', 'Safety instrumented systems.',
                'Human factors and process safety culture.', 'Emergency planning and response.'],
    resources=['Crowl &amp; Louvar, <em>Chemical Process Safety: Fundamentals with '
               'Applications</em> — the standard text, and effectively the syllabus.',
               'The AIChE <strong>Center for Chemical Process Safety</strong> guideline series, '
               'which is what industry actually uses.',
               'The <strong>U.S. Chemical Safety Board</strong> investigation reports and animated '
               'reconstructions — free, authoritative, and the best case material available.'],
    career=('Named on the <strong>Chemical Engineer</strong> career path. %s <strong>Process safety '
            'is a career in itself</strong>, and a well-paid one: process safety engineer, risk '
            'analyst, and the HAZOP-facilitation work that consultancies sell. In Florida it '
            'applies directly at the phosphate and fertiliser plants, pharmaceutical and '
            'biotechnology manufacturing, power generation, and anywhere ammonia refrigeration or '
            'chlorine is handled — water treatment included. Even for a graduate who never '
            'specialises, <strong>it is the course that makes you useful in your first week</strong>, '
            'because a new engineer who understands a relief valve is trusted with more.' % WW),
    extra=(
        '<h3>%s Only two of the four Florida programmes teach this as a course</h3>'
        '<table class="table table-sm"><thead><tr><th>Programme</th><th>Process safety course</th>'
        '</tr></thead><tbody>'
        '<tr><td>University of Florida</td><td><code>ECH4714</code> Chemical Process Safety</td></tr>'
        '<tr><td>University of South Florida</td><td><code>ECH4715</code> Chemical Process Safety '
        'and Ethics — a corequisite of its design course</td></tr>'
        '<tr><td>FAMU-FSU College of Engineering</td><td>%s <strong>neither</strong> — '
        'distributed through the design sequence</td></tr>'
        '</tbody></table>'
        '<p>%s <strong>ABET requires the content either way, so this is not an accreditation '
        'gap.</strong> But a dedicated course covers relief sizing, HAZOP facilitation and '
        'quantitative risk assessment in a depth that a few weeks inside a design course cannot, '
        'and the transcript line is visible to an employer where distributed coverage is not. '
        '<strong>If your programme offers it as an elective, take it</strong>; if it does not, the '
        'AIChE and CCPS student resources and the CSB reports are the realistic substitute, and '
        'they are free.</p>'
        '<h3>%s A single-carrier course, and the statewide record is UF’s own</h3>'
        '<p>UF is the only carrier, and the statewide description ends <em>&ldquo;integrated with '
        '<code>ECH 4224L</code>&rdquo;</em> — which is <strong>UF’s own laboratory '
        'number</strong>. So the state record was contributed by UF and is not independent '
        'corroboration of anything on this page.</p>'
        '<p>%s <strong>And the contributor has since drifted from its own contribution.</strong> '
        'The statewide title is <em>Safety &amp; Experimental Evaluation-Upper</em>, pairing safety '
        'with experimental design; UF now titles the course <em>Chemical Process Safety</em>, which '
        'reads as safety having grown into a course of its own. <strong>Treat the statewide record '
        'as the older description and the UF catalogue as the current one.</strong></p>'
        % (WWW, WW, WW, WW, W)),
    summary=('The University of Florida is the only Florida public carrier of ECH4714, at 3 '
             'credits. USF teaches the same subject as ECH4715 Chemical Process Safety and Ethics; '
             'the FAMU-FSU College of Engineering carries neither number. UF publishes no '
             'contact-hour figure.'),
    derivation='Florida convention of 15 contact hours per credit at UF’s 3-credit value.',
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
    html += '<h2>Special Information</h2>' + s['extra'] + LANDSCAPE + ABET_FE
    return {
        'title': s['title'], 'html_content': html, 'credits': s['credits'],
        'contact_hours': s['hours'], 'prerequisites': s['prereq'], 'version': '1.0',
        'offering_notes': {
            'summary': s['summary'],
            'hours_source': 'derived',
            'derived_contact_hours': s['hours'],
            'derivation': s['derivation'],
            'offerings': [{'institution': c, 'institution_name': NAMES[c], 'title': t,
                           'credits': cr, 'contact_hours': None, 'note': nt}
                          for c, t, cr, nt in s['carriers']],
        },
    }


def main():
    bad = 0
    for s in SPEC:
        g = build(s)
        io.open(os.path.join(DRAFTS, '%s_guide.json' % s['cid']), 'w', encoding='utf-8').write(
            json.dumps(g, ensure_ascii=False, indent=1))
        flag = ' <<< OVER' if len(g['prerequisites']) > 1000 else ''
        bad += 1 if flag else 0
        print('%-9s %-34s %d cr /%4d hrs | prereq %4d%s | html %6d | %d carrier(s)'
              % (s['cid'], g['title'][:34], g['credits'], g['contact_hours'],
                 len(g['prerequisites']), flag, len(g['html_content']), len(s['carriers'])))
    print('\n%d draft(s) written, %d over the prerequisite limit' % (len(SPEC), bad))
    return 0


if __name__ == '__main__':
    sys.exit(main())
