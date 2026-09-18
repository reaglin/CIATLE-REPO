#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Career path 8: Chemical Engineer (CIP 14.07, SOC 17-2041).

A DIRECT path -- the major is named after the career -- but with the most
constrained supply side of any engineering path written so far, and that is
the finding the page is built around.

EVIDENCE GATHERED FOR THIS PATH

IPEDS C2023_A, CIP 14.0701, Florida public institutions, first-major
bachelor's completions:

    University of Florida            110
    University of South Florida       73
    Florida State University          27
    Florida A&M University             4

FOUR institutions -- and FAMU and FSU are ONE PHYSICAL COLLEGE, the joint
FAMU-FSU College of Engineering in Tallahassee. So chemical engineering in
Florida is taught in THREE places: Gainesville, Tampa and Tallahassee.

⚠⚠ UCF AND FIU AWARD NONE. They are the two largest universities in the
state by enrolment. UCF carries no ECH course at all; FIU carries three
(ECH3271, ECH4504, ECH4826) as service and elective courses while awarding
degrees in seven OTHER 14.xx codes. A student in Orlando or Miami cannot
study chemical engineering at their own state university, and nothing a
prospective student normally reads says so.

⚠⚠⚠ THE DANGLING PREREQUISITE ON ECH3854 IS THE WORST SINGLE STRING FOUND
IN THIS PROJECT. The statewide gate reads "ECH 3264, CGS 3460, MAP 3305 &
numerical solution of non-linear systems of equations". Carriers of ECH3854
are FAMU, FSU and USF. Against that:

    ECH3264   carried by UF ALONE        -> dangles at all three carriers
    CGS3460   ZERO public carriers       -> dangles for everybody (batch 233)
    MAP3305   FAMU, FAU, FLPOLY, FSU     -> dangles at USF

TWO of the five documented defect shapes in one field, and the contributor
(UF, whose numbering ECH3264 and CGS3460 both are) DOES NOT CARRY THE
COURSE -- the JOU3342 shape from batch 224.

⚠⚠ PARALLEL NUMBERING FAMILIES run through the whole transport sequence.
UF splits transport into ECH3264 / ECH3203 / ECH3223 / ECH4403; FAMU, FSU
and USF use ECH3266 / ECH4267. Same subject, two numbering schemes, and UF
is alone on one of them.

Title/description test on ECH3023: statewide TITLE is "Introduction to
Chemical Engineering", statewide DESCRIPTION is "the conservation laws of
mass and energy applied to the solution of industrial chemical process
problems" -- and all four carriers title it Mass/Material and Energy
Balances. Carriers back the DESCRIPTION, so the TITLE is the stale element
(branch 2).

O*NET 17-2041 (2024-2034): 21,600 employed, growth "average (3% to 4%)",
about 1,100 openings, median $125,040.
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
OUT = os.path.join(HERE, '..', 'career_paths', 'chemical-engineer.json')

W = '⚠'
WW = '⚠⚠'
WWW = '⚠⚠⚠'
DASH = '—'

COURSES = [
    ('MAC2311', 'Calculus I — the gate on the degree, and on every course below it.',
     '%s Transfer is guaranteed only on the COMPLETED calculus sequence. Finish it at one '
     'institution where you can.' % W),
    ('MAC2312', 'Calculus II — integration and series. Chemical engineering uses integration '
     'harder than most branches, because balances are integrals.', None),
    ('MAC2313', 'Calculus III — multivariable calculus, which transport phenomena is written in.',
     None),
    ('MAP2302', 'Differential Equations — every unsteady balance, every reactor, every control '
     'loop is an ODE.', None),
    ('PHY2048', 'Physics I with calculus — mechanics; the prerequisite chain for fluid flow.',
     None),
    ('PHY2049', 'Physics II with calculus — electricity and magnetism; required for instrumentation '
     'and process control.', None),
    ('CHM2045', 'General Chemistry I — and for this degree it is a major course, not a service '
     'course.',
     '%s Register by the right identifier: sixteen institutions carry CHM2045 with a separate '
     'CHM2045L laboratory, and four (UCF, FSCJ, Lake-Sumter, Seminole State) carry the integrated '
     'CHM2045C instead. Both are complete; they are packaged differently.' % W),
    ('CHM2046', 'General Chemistry II — equilibrium, kinetics and thermodynamics, which is where '
     'chemical engineering starts.', None),
    ('CHM2210', 'Organic Chemistry I — %s THE COURSE THAT SEPARATES THIS DEGREE FROM EVERY OTHER '
     'ENGINEERING MAJOR. No other Florida engineering degree requires it.' % WW,
     '%s Carried by 29 Florida public institutions, so it is widely available and widely failed. '
     'It rewards a different kind of study from calculus — pattern recognition and mechanism, not '
     'procedure — and students who study it like a mathematics course struggle.' % W),
    ('CHM2211', 'Organic Chemistry II — the second term, and the one most programmes also require.',
     None),
    ('ENC1101', 'English Composition I — Gordon Rule writing, and required by every Florida degree.',
     None),
    ('ENC1102', 'English Composition II — the second writing course.', None),
    ('ECH3023', '%s THE GATEWAY COURSE OF THE MAJOR. Material and energy balances — if you can do '
     'this you can do the degree, and programmes treat it as the screen.' % WW,
     '%s Two things to know. The statewide TITLE says "Introduction to Chemical Engineering" and '
     'every carrier calls it Mass or Material and Energy Balances — the title is stale, the '
     'carriers and the statewide description agree. And the CREDIT VALUE DIVERGES: FSU and UF carry '
     'it at 4 credits, FAMU and USF at 3. FAMU and FSU additionally run a second term, ECH3024, '
     'that UF and USF do not.' % WW),
    ('ECH3854', 'Chemical Engineering Computations — numerical methods, and in practice the course '
     'that teaches you to program as a chemical engineer.',
     '%s ITS STATEWIDE PREREQUISITE DOES NOT RESOLVE ANYWHERE. It names ECH3264 (carried by UF '
     'alone, and UF does not carry this course), CGS3460 (carried by NO Florida public institution) '
     'and MAP3305 (not carried by USF). Read the gate from your own catalogue and ignore the state '
     'record on this number.' % WWW),
    ('ECH3101', 'Chemical Engineering Thermodynamics — the first of two, and the conceptual spine '
     'of the degree.',
     '%s The statewide prerequisite field reads NONE, which is a gap in the record rather than a '
     'statement about the course. UF titles it Process Thermodynamics.' % W),
    ('ECH4123', 'Phase and chemical equilibria — thermodynamics of mixtures, and what every '
     'separation is designed from.',
     '%s Carried by UF (Phase and Chemical Equilibria) and USF (Chemical Engineering '
     'Thermodynamics II). Same subject, named by topic at one and by position in the sequence at '
     'the other.' % W),
    ('ECH3266', 'Transport Phenomena I — momentum, heat and mass transfer, the analysis that '
     'chemical engineers own.',
     '%s CARRIED BY FAMU, FSU AND USF ONLY, because UF uses a DIFFERENT NUMBERING FAMILY for the '
     'same material: ECH3264 Elementary Transport Phenomena, ECH3203 Fluid and Solid Operations '
     'and ECH3223 Energy Transfer Operations. Same subject, split three ways. On transfer, send '
     'the topic list.' % WW),
    ('ECH4267', 'Transport Phenomena II — the differential treatment: boundary layers, convective '
     'mass transfer, turbulent transport.',
     '%s Same three carriers, same parallel-family caveat. FSU titles it Advanced Transport '
     'Phenomena.' % W),
    ('ECH3418', 'Separations Processes — distillation, absorption and extraction, which is what a '
     'great deal of the profession actually does.',
     '%s Carried as ECH3418 by FAMU and FSU. UF numbers the same material ECH4403 Separation and '
     'Mass Transfer Operations and USF numbers it ECH4418 Separation Process. THREE NUMBERS, ONE '
     'SUBJECT.' % WW),
    ('ECH4504', '%s Kinetics and reactor design — the most widely carried chemical engineering '
     'course in Florida, and the one the profession is named for.' % W,
     '%s FIVE carriers, which makes it the only ECH number FIU shares with the degree-granting '
     'institutions. Titles vary and the subject does not: FAMU and FSU Kinetics and Reactor '
     'Design, UF Chemical Kinetics and Reactor Design (at 4 credits, against 3 elsewhere), USF '
     'Kinetics and Reaction Engineering, FIU Introduction to Chemical Reaction Engineering.' % W),
    ('ECH4323', 'Process Control — dynamics, feedback and tuning; the course that connects the '
     'degree to a plant.', None),
    ('ECH4323L', 'Process Control Laboratory — the hardware half of control.',
     '%s Carried at 1 credit by FAMU, FSU and UF. UF titles it Chemical Engineering Lab 5, which '
     'is its own sequence naming rather than a different course.' % W),
    ('ECH4404L', 'Unit Operations Laboratory — the signature laboratory of the degree: real '
     'equipment, real data, and a report that reads like industry.',
     '%s THE SCOPE AND THE CREDIT DIFFER. FAMU and FSU run it as the general unit operations '
     'laboratory at 3 credits; UF runs it at 2 credits as the laboratory for separations and mass '
     'transfer, which is what the statewide description actually specifies. Expect a substantially '
     'bigger time commitment at Tallahassee.' % WW),
    ('ECH4604', 'Process design and economics — the capstone-facing course: what a plant costs and '
     'whether it should be built.',
     '%s FAMU and FSU carry it at 4 credits as Chemical Engineering Process Design; UF carries it '
     'at 3 as Process Economics and Optimization. FAMU and FSU continue into ECH4615 and USF runs '
     'its own design sequence at ECH4605 and ECH4615C.' % W),
    ('ECH4714', 'Chemical Process Safety — %s hazard analysis, relief sizing and the case '
     'histories. Safety is not an add-on in this profession; it is the profession.' % WW,
     '%s ONLY TWO FLORIDA PROGRAMMES NUMBER IT AS A STANDALONE COURSE, AND UNDER DIFFERENT '
     'NUMBERS: UF as ECH4714 Chemical Process Safety, USF as ECH4715 Chemical Process Safety and '
     'Ethics. The FAMU-FSU programme carries neither, distributing the material through the design '
     'sequence instead. ABET requires the content either way — but if you are choosing electives, '
     'this is the one to take, and employers ask about it.' % WWW),
]

BODY = (
    '<h2>What the work actually is</h2>'
    '<p>O*NET&rsquo;s task statements for chemical engineers: <em>develop safety procedures to be '
    'employed by workers operating equipment or working in close proximity to ongoing chemical '
    'reactions; troubleshoot problems with chemical manufacturing processes; evaluate chemical '
    'equipment and processes to identify ways to optimise performance or to ensure compliance with '
    'safety and environmental regulations; determine most effective arrangement of operations such '
    'as mixing, crushing, heat transfer, distillation and drying; and perform tests and monitor '
    'performance of processes throughout production.</em></p>'
    '<p>&#9888; <strong>Read that list again and notice what is first.</strong> The defining task of '
    'the profession is safety, and the second is troubleshooting a process that is already running. '
    'Students arrive expecting to design new plants; most chemical engineers spend their careers '
    'making an existing plant run better and more safely, which is harder and considerably more '
    'consequential.</p>'
    '<h2>Projected need</h2>'
    '<p>O*NET, on federal projections: <strong>21,600 chemical engineers employed</strong> (2024), '
    'growth projected <strong>average, 3&ndash;4% through 2034</strong>, about <strong>1,100 '
    'openings</strong>, median pay <strong>$125,040</strong>. A bachelor&rsquo;s degree is the '
    'entry credential — 91% of employers surveyed require one.</p>'
    '<p>&#9888;&#9888; <strong>Put the pay next to the size and read both.</strong> The median is '
    'among the highest of any bachelor&rsquo;s-level occupation. But 21,600 people is a '
    '<strong>small occupation</strong> — mechanical engineering is roughly fifteen times larger, '
    'civil roughly fourteen — and a small occupation means fewer employers, fewer postings, and '
    'far more sensitivity to where you are willing to live. <strong>This degree pays well and has '
    'narrow doors.</strong> That is the honest trade, and it should be made deliberately.</p>'
    '<h2>&#9888;&#9888;&#9888; Where you can actually study it in Florida — three places</h2>'
    '<p>Federal completions data (IPEDS, CIP 14.0701, first-major bachelor&rsquo;s degrees at '
    'Florida public institutions):</p>'
    '<table class="table table-sm"><thead><tr><th>Institution</th><th>Bachelor&rsquo;s degrees</th>'
    '<th>Where</th></tr></thead><tbody>'
    '<tr><td>University of Florida</td><td><strong>110</strong></td><td>Gainesville</td></tr>'
    '<tr><td>University of South Florida</td><td><strong>73</strong></td><td>Tampa</td></tr>'
    '<tr><td>Florida State University</td><td>27</td><td>Tallahassee</td></tr>'
    '<tr><td>Florida A&amp;M University</td><td>4</td><td>Tallahassee</td></tr>'
    '</tbody></table>'
    '<p>&#9888;&#9888; <strong>Those are four institutions but three locations.</strong> Florida '
    'State and Florida A&amp;M share the <strong>FAMU-FSU College of Engineering</strong>, a single '
    'joint college in Tallahassee — the only engineering college in the country operated by two '
    'universities together. Its chemical engineering students sit in the same classrooms and its '
    'course records are identical down to the title, which is why the two appear as a matched pair '
    'throughout the course list below. <strong>You apply to one university or the other and you '
    'attend the same college.</strong></p>'
    '<h3>&#9888;&#9888;&#9888; UCF and FIU award none</h3>'
    '<p>The two largest universities in Florida by enrolment — the University of Central Florida '
    'and Florida International University — <strong>do not award a chemical engineering '
    'degree.</strong> UCF carries no <code>ECH</code> course at all. FIU carries three as service '
    'and elective courses while awarding degrees in seven other engineering CIP codes.</p>'
    '<p>&#9888;&#9888; <strong>A student in Orlando or Miami cannot study chemical engineering at '
    'their own state university, and almost nothing a prospective student reads says so.</strong> '
    'It is the single most useful fact on this page: it is discovered late, it is expensive to '
    'discover late, and the remedy — planning a transfer to Gainesville, Tampa or Tallahassee '
    'from the start — is easy if it is planned and painful if it is not.</p>'
    '<h3>What to do if you are at a state college</h3>'
    '<p>The route works and is well travelled: complete the <strong>A.A. with the calculus, '
    'physics, general chemistry and organic chemistry sequences finished</strong>, then transfer '
    'into one of the three programmes. <strong>Organic chemistry is the part to get right</strong> '
    '— 29 Florida public institutions carry <code>CHM2210</code> and <code>CHM2211</code>, so it '
    'is available almost everywhere, and it is the prerequisite most likely to be missing when a '
    'transfer application is assessed. &#9888; Nothing with an <code>ECH</code> prefix is offered '
    'below the junior year at any Florida institution, so there is no way to start the major '
    'early — and no need to.</p>'
    '<h2>&#9888;&#9888; The Florida employment picture, stated honestly</h2>'
    '<p><strong>Florida has no petroleum refineries.</strong> The oil, gas and petrochemical sector '
    'is the largest single employer of chemical engineers in the United States, and it is '
    'concentrated on the Texas and Louisiana Gulf Coast, not here. <strong>A graduate who wants '
    'refinery or petrochemical work will almost certainly leave the state</strong>, and it is far '
    'better to know that in the second year than in the final one.</p>'
    '<p>What Florida does have is real and worth naming:</p>'
    '<ul>'
    '<li><strong>Phosphate and fertiliser</strong> — central Florida is one of the world&rsquo;s '
    'major phosphate districts, and Mosaic, headquartered in Tampa, is the largest chemical '
    'process employer in the state.</li>'
    '<li><strong>Pharmaceutical and biotechnology manufacturing</strong> — growing, and the '
    'sector where the bioprocess electives pay off.</li>'
    '<li><strong>Semiconductor and electronic materials</strong> — process engineering in fabs, '
    'which hires chemical engineers preferentially.</li>'
    '<li><strong>Water and wastewater treatment</strong>, and environmental consulting — large in '
    'Florida for obvious reasons, and one of the few chemical engineering routes where the PE '
    'licence genuinely matters.</li>'
    '<li><strong>Power generation</strong>, food and beverage processing, citrus and sugar '
    'processing, specialty chemicals, and aerospace propellants and life support on the Space '
    'Coast.</li>'
    '</ul>'
    '<p>&#9888; <strong>The practical consequence for course choice:</strong> the Florida-facing '
    'electives are the bioprocess, environmental, polymer and materials ones, not the petroleum '
    'ones — although the FAMU-FSU college carries <code>ECH4803</code> Petroleum Science and '
    'Technology for students heading out of state.</p>'
    '<h2>&#9888;&#9888; Two structural traps in the course numbering</h2>'
    '<h3>UF numbers the transport sequence differently from everybody else</h3>'
    '<p>Transport phenomena is the analytical core of the degree, and Florida numbers it two ways:</p>'
    '<table class="table table-sm"><thead><tr><th>FAMU, FSU, USF</th><th>University of Florida</th>'
    '</tr></thead><tbody>'
    '<tr><td><code>ECH3266</code> Transport Phenomena I</td><td><code>ECH3264</code> Elementary '
    'Transport Phenomena</td></tr>'
    '<tr><td rowspan="2"><code>ECH4267</code> Transport Phenomena II</td><td><code>ECH3203</code> '
    'Fluid and Solid Operations</td></tr>'
    '<tr><td><code>ECH3223</code> Energy Transfer Operations</td></tr>'
    '<tr><td><code>ECH3418</code> Separations Processes</td><td><code>ECH4403</code> Separation and '
    'Mass Transfer Operations</td></tr>'
    '</tbody></table>'
    '<p>&#9888; <strong>Same material, two schemes, and no number in common.</strong> This matters '
    'to anyone transferring between Florida programmes mid-degree, which is uncommon but not rare. '
    '<strong>Send a topic list and a syllabus, not a course number</strong> — an evaluator '
    'matching on identifiers will find nothing to match.</p>'
    '<h3>&#9888;&#9888;&#9888; One statewide prerequisite that resolves nowhere</h3>'
    '<p><code>ECH3854</code> Chemical Engineering Computations is carried by FAMU, FSU and USF. Its '
    'statewide prerequisite names three courses:</p>'
    '<table class="table table-sm"><thead><tr><th>Named</th><th>Who carries it</th><th>Resolves '
    'at?</th></tr></thead><tbody>'
    '<tr><td><code>ECH3264</code></td><td>University of Florida alone</td><td>&#9888; <strong>none '
    'of the three carriers</strong></td></tr>'
    '<tr><td><code>CGS3460</code></td><td>&#9888;&#9888; <strong>no Florida public institution at '
    'all</strong></td><td><strong>nobody in the state</strong></td></tr>'
    '<tr><td><code>MAP3305</code></td><td>FAMU, FAU, Florida Polytechnic, FSU</td><td>not USF</td></tr>'
    '</tbody></table>'
    '<p>The explanation is visible in the numbers themselves: <code>ECH3264</code> and '
    '<code>CGS3460</code> are <strong>University of Florida numbering</strong>, and UF does not '
    'carry <code>ECH3854</code>. <strong>The prerequisite was contributed by an institution that '
    'does not teach the course.</strong> &#9888; It is recorded here because it is the clearest '
    'possible demonstration of a general rule this repository has learned the hard way: <strong>a '
    'statewide prerequisite is contributed by one institution and is not a promise about '
    'yours.</strong> Read the gate from your own catalogue, every time.</p>'
    '<h2>Licensure — the minority case, and where it is not</h2>'
    '<p>Most chemical engineers never become licensed. Process plants are covered by the '
    '<strong>industrial exemption</strong>, so manufacturing employers hire on the degree. '
    '&#9888;&#9888; <strong>But two Florida-relevant routes are the exception:</strong> '
    '<strong>environmental and water engineering consulting</strong>, where work is sealed for '
    'public clients and the PE is effectively mandatory, and any move into forensic or expert '
    'work.</p>'
    '<p>&#9888; <strong>Sit the FE examination in your final year regardless.</strong> It is '
    'inexpensive as a student, expensive to recreate later, and the chemical FE is written for '
    'exactly the curriculum you have just finished — it will never be easier than the term you '
    'graduate. Under s. 471.013(1)(a), Florida Statutes, an approved <em>engineering</em> '
    'curriculum needs four years of qualifying experience toward the PE.</p>'
    '<h2>&#9888; Check ABET accreditation, and check it by name</h2>'
    '<p>All four Florida programmes are ABET-accredited under the Engineering Accreditation '
    'Commission, which is what makes graduates eligible for the standard four-year PE route and is '
    'what most employers screen on. <strong>Accreditation attaches to a named programme at a named '
    'institution, not to a course list</strong> — so verify the specific programme in ABET&rsquo;s '
    'own search rather than assuming it from the university&rsquo;s reputation.</p>'
)

DOC = {
    'name': 'Chemical Engineer',
    'cipCode': '14.07',
    'socCode': '17-2041',
    'isPublished': True,
    'sortOrder': 85,
    'description':
        'Chemical engineers design and run the processes that turn raw materials into products at '
        'scale — reactors, separations, heat and mass transfer, and the control and safety '
        'systems around them. It is the engineering discipline built on chemistry, and the only '
        'one that requires organic chemistry. ⚠⚠ In Florida it is taught at just FOUR '
        'institutions in THREE cities, and neither UCF nor FIU awards the degree — which makes '
        'where you start your degree the most consequential decision on this page.',
    'credentialNote':
        'A Professional Engineer licence is the minority case: chemical process plants fall under '
        'Florida’s industrial exemption and manufacturers hire on the degree. ⚠⚠ THE '
        'EXCEPTIONS THAT MATTER IN FLORIDA are environmental and water engineering consulting, '
        'where work is sealed for public clients and the PE is effectively required. '
        '⚠ WHAT EVERY EMPLOYER DOES SCREEN ON is ABET accreditation of the specific programme, '
        'and it attaches to a named programme at a named institution — not to the courses. '
        '⚠ Sit the FE examination in your final year whichever route you expect to take; the '
        'chemical FE is written for the curriculum you have just completed and will never be '
        'easier.',
    'bodyHtml': BODY,
    'programs': [
        {'slug': 'mechanical-engineering',
         'note': '⚠ Worth reading BEFORE you commit, and especially if you live in Orlando or '
                 'Miami. Mechanical engineering is offered at every Florida public university, is '
                 'roughly fifteen times larger as an occupation, and overlaps chemical engineering '
                 'substantially in thermodynamics, fluids and heat transfer. It is the realistic '
                 'alternative for a student who cannot relocate.'},
    ],
    'courses': [
        dict([('courseId', c), ('reason', r)] + ([('variantNote', v)] if v else []))
        for c, r, v in COURSES
    ],
    'sources': [
        {'label': 'O*NET — Chemical Engineers (17-2041.00)',
         'url': 'https://www.onetonline.org/link/summary/17-2041.00',
         'note': 'Tasks, technology skills, wages and the employment projections quoted on this '
                 'page (21,600 employed, 3–4% growth, ~1,100 openings, $125,040 median).'},
        {'label': 'U.S. Bureau of Labor Statistics — Chemical Engineers',
         'url': 'https://www.bls.gov/ooh/architecture-and-engineering/chemical-engineers.htm',
         'note': 'Federal wage, employment and outlook detail for SOC 17-2041.'},
        {'label': 'IPEDS — Completions (C2023_A)',
         'url': 'https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx',
         'note': 'The source of the four-institution degree table: CIP 14.0701 first-major '
                 'bachelor’s completions at Florida public institutions.'},
        {'label': 'FAMU-FSU College of Engineering',
         'url': 'https://eng.famu.fsu.edu/',
         'note': 'The joint college in Tallahassee shared by Florida A&M and Florida State — '
                 'why those two institutions appear as a matched pair throughout.'},
        {'label': 'ABET — Accredited Program Search',
         'url': 'https://amspub.abet.org/aps/name-search?searchType=institution',
         'note': 'Verify the specific chemical engineering programme, by institution and by name.'},
        {'label': 'AIChE — American Institute of Chemical Engineers',
         'url': 'https://www.aiche.org/',
         'note': 'The professional society; student chapters exist at all four Florida programmes, '
                 'and its Center for Chemical Process Safety is the standard reference for the '
                 'safety material.'},
        {'label': 'Florida Board of Professional Engineers — Licensure',
         'url': 'https://fbpe.org/licensure/',
         'note': 'The FE and PE route, and s. 471.013 Florida Statutes on qualifying curricula.'},
        {'label': 'Florida Industrial and Phosphate Research Institute',
         'url': 'https://fipr.floridapoly.edu/',
         'note': 'Context for the phosphate and fertiliser sector, the largest chemical process '
                 'industry in Florida.'},
        {'label': 'NCES — Classification of Instructional Programs (CIP 2020)',
         'url': 'https://nces.ed.gov/ipeds/cipcode/browse.aspx?y=55',
         'note': 'CIP 14.07 Chemical Engineering, the anchor for this path.'},
    ],
}


def main():
    io.open(OUT, 'w', encoding='utf-8').write(
        json.dumps(DOC, ensure_ascii=False, indent=1))
    print('wrote %s' % os.path.normpath(OUT))
    print('  %d course(s), %d source(s), %d program link(s), body %d chars'
          % (len(DOC['courses']), len(DOC['sources']), len(DOC['programs']), len(BODY)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
