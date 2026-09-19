#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Career path 9: Biomedical Engineer (CIP 14.05, SOC 17-2031).

A DIRECT path whose honest content is closer to a CHOICE path, because the
decision this degree actually forces on a student is not "which major" but
"what comes after the bachelor's" -- and the data says that loudly.

EVIDENCE GATHERED

IPEDS C2023_A, CIP 14.0501, Florida public institutions:

    BACHELOR'S        UF 115 | FIU 79 | FSU 36 | USF 29 | FGCU 21 | FAMU 4
    GRADUATE ONLY     ⚠ UCF (11 master's, 3 doctorate) and FAU (16 master's)
                        award NO bachelor's in the field

⚠⚠ Six bachelor's programmes, but FSU and FAMU share the joint FAMU-FSU
College of Engineering, so five locations. And TWO universities offer the
graduate degree without an undergraduate one -- which is a fact about the
DISCIPLINE, not about those two universities.

O*NET 17-2031 (2024-2034): 22,200 employed, "faster than average (5% to 6%)",
about 1,300 openings, median $109,370. ⚠⚠⚠ AND THE EDUCATION FIGURE IS THE
ONE THAT MATTERS: only 43% of employers say a bachelor's is required; 26% say
master's and 13% doctoral. That is by far the highest graduate expectation of
any engineering path written so far.

⚠⚠⚠ THE ARITHMETIC THE PAGE IS BUILT AROUND. ~1,300 openings a year
nationally, against 284 bachelor's degrees a year from FLORIDA ALONE. Florida
is about 6.6% of the U.S. population, so a proportionate share of those
openings is roughly 86 a year. The state produces more than three times that.
This is stated carefully -- graduates move, and many work in adjacent
engineering and regulated-industry roles -- but the shape is real and no
prospective student reads it anywhere.

⚠⚠⚠ THE PREFIX HAS THE WORST PREREQUISITE DATA MEASURED IN THIS PROJECT.
Of 100 active undergraduate BME rows, 75 name at least one course token in
DS_Prerequisites1, and FIFTEEN of those 75 -- ONE IN FIVE -- name a course
with ZERO public carriers anywhere in Florida:

    BME?009 -> BSC2012        BME?503 -> EGN3374C      BME?740 -> EGN1100
    BME?230 -> BME3032/3701   BME?506 -> EGN1006L      BME?746 -> BME4303
    BME?260 -> BME3032/3701   BME?507 -> EGN3373C      BME?760 -> COP2271C
    BME?311 -> BME3032        BME?776 -> BME4303       BME?800 -> BME3710
    BME?881 -> BME4090        BME?884 -> EGN3641C/EGN3374C   BME?885 -> BME4410

Against ~2% in CCJ and the single instance in ECH. The likeliest cause is
that biomedical engineering is Florida's newest and fastest-growing
engineering discipline: programmes were built recently and renumbered as they
matured, and the statewide record kept the numbers that were proposed or
retired along the way.

OTHER FINDINGS

⚠ BME1008's statewide description says "lectures will be given by faculty of
the biomedical engineering department at the UNIVERSITY OF FLORIDA" -- a
contributor stamp inside the text. UF carries the BARE BME1008; the integrated
BME1008C is carried by FIU and ST PETERSBURG COLLEGE.

⚠⚠ SPC is the ONLY Florida College System institution in the entire BME
prefix -- a real and otherwise invisible transfer route.

⚠ FOUR numbers for the introductory course, at THREE different levels:
BME1008/1008C (1000), BME3009 and BME3060 (3000), BME4007 (4000). FAMU and
FSU carry BOTH BME3009 and BME4007.

⚠ UNF carries BME4211 (as "Mechanics of the Human Body") and awards no
biomedical engineering degree -- the FIU/ECH shape.

⚠ Florida Polytechnic's title for BME4503C reads "BIOLOGICAL SCIENCE" where
every other carrier and the state say biomedical instrumentation. Recorded,
not published as a finding -- one anomalous title in a flat file is more
likely a data-entry error than a curricular fact, and it is not worth a
student-facing warning.
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
OUT = os.path.join(HERE, '..', 'career_paths', 'biomedical-engineer.json')

W, WW, WWW = '⚠', '⚠⚠', '⚠⚠⚠'

COURSES = [
    ('MAC2311', 'Calculus I — the gate on the degree and on everything below it.',
     '%s Transfer is guaranteed only on the COMPLETED calculus sequence. Finish it at one '
     'institution where you can.' % W),
    ('MAC2312', 'Calculus II — integration and series.', None),
    ('MAC2313', 'Calculus III — multivariable calculus, which biotransport and biomechanics are '
     'written in.', None),
    ('MAP2302', 'Differential Equations — physiological systems are differential equations, and '
     'this degree models them from the third year on.', None),
    ('PHY2048', 'Physics I with calculus — mechanics, the basis of biomechanics.', None),
    ('PHY2049', 'Physics II with calculus — electricity and magnetism, and the basis of '
     'bioinstrumentation and imaging.', None),
    ('CHM2045', 'General Chemistry I.', None),
    ('CHM2046', 'General Chemistry II — equilibrium and kinetics, which biomaterials and cell '
     'engineering build on.', None),
    ('BSC2010', '%s General Biology I for majors — the course that makes this degree biomedical '
     'rather than mechanical, and the one engineering students most often underestimate.' % WW,
     '%s WATCH THE STATE RECORD HERE. The statewide prerequisite for BME3009 names "BSC 2012", '
     'and NO Florida public institution carries that number. The real majors biology sequence is '
     'BSC2010 and BSC2011, carried by about twenty institutions each, with separate BSC2010L and '
     'BSC2011L laboratories. Register for the laboratory: every programme requires it.' % WWW),
    ('BSC2011', 'General Biology II for majors — the second term, and where most programmes place '
     'the physiology and systems material.', None),
    ('ENC1101', 'English Composition I — Gordon Rule writing, required by every Florida degree.',
     None),
    ('ENC1102', 'English Composition II. %s Worth more here than the requirement suggests: O*NET '
     'lists "prepare technical reports, data summaries or research articles for publication" as '
     'the SECOND task of the occupation, ahead of designing anything.' % W, None),
    ('BME3009', 'Introduction to Biomedical Engineering — the entry point to the major: cell '
     'physiology and modelling, bioinstrumentation, biomaterials, tissue engineering, imaging.',
     '%s FOUR NUMBERS, THREE LEVELS. Florida runs the introductory course as BME1008 or BME1008C '
     '(1000 level), BME3009 and BME3060 (3000), and BME4007 (4000) — and FAMU and Florida State '
     'carry BOTH BME3009 and BME4007. Find out which one your programme means before you register; '
     'the level alone is a two-year difference in where it sits in the degree.' % WW),
    ('BME3100', 'Biomaterials — what implants and devices are made of, and why bodies reject '
     'things.',
     '%s Carried as BME3100 by FAMU, Florida State and Florida Polytechnic; FAU and FIU number the '
     'same subject BME4100 Biomaterials Science, a thousand higher. Both are upper division.' % W),
    ('BME4409', 'Quantitative Physiology — %s physiology taught as systems and equations rather '
     'than as memorisation. It is the course that makes an engineer useful in a hospital.' % W,
     '%s Its statewide prerequisite reads "PCB 3XXX Cell and System Physiology" — a MASKED number, '
     'and unlike most such cases the title does not resolve to any Florida course. The nearest real '
     'numbers are PCB3203 and PCB3204 Cell Physiology. Read your own catalogue; the state record is '
     'no help on this one.' % WW),
    ('BME4211', 'Biomechanics — forces, materials and motion applied to the musculoskeletal '
     'system; the route into orthopaedics, prosthetics and rehabilitation engineering.',
     '%s Its statewide prerequisite names BME4100, which is carried only by FAU and FIU — so it '
     'DOES NOT RESOLVE at FAMU, Florida State or UNF, three of its four carriers. %s Also note UNF '
     'carries this course, as "Mechanics of the Human Body", while awarding no biomedical '
     'engineering degree.' % (WW, W)),
    ('BME4503', 'Biomedical Instrumentation — biopotential electrodes and amplifiers, patient '
     'monitoring, clinical laboratory instruments, electrical safety. %s The most directly '
     'employable course in the degree.' % WW,
     '%s TWO PACKAGINGS AND A DEAD PREREQUISITE. FAMU, Florida State, USF and Florida Polytechnic '
     'carry BME4503 at 3 credits; FAU, FGCU, FIU, UF and Florida Polytechnic carry BME4503C, the '
     'integrated form, at 3 to 4. And the statewide prerequisite names EGN3374C "Signals and '
     'Systems for Bioengineers" — a course NO Florida public institution carries at all.' % WWW),
    ('BME4508', 'Biosignals and Systems — signal processing applied to physiological data: ECG, '
     'EEG, EMG, filtering, transforms.',
     '%s Where your programme does not carry it, the material usually sits in the electrical '
     'engineering signals course. Ask; it is assumed by the imaging and instrumentation '
     'sequence.' % W),
    ('BME4531', '%s Medical Imaging — X-ray, CT, ultrasound, MRI, PET and SPECT, and optical '
     'imaging. THE MOST WIDELY CARRIED BIOMEDICAL ENGINEERING COURSE IN FLORIDA.' % W,
     'Five carriers — FAMU, FIU, Florida State, UF and USF — all at 3 credits, and all but USF '
     'using the identical title. Unusually clean for this prefix.'),
    ('BME4332', 'Cell and Tissue Engineering — growing and engineering living tissue; the '
     'research-facing heart of the discipline.',
     '%s FAMU and Florida State carry a matching 1-credit laboratory, BME4332L; FAU and FIU do '
     'not. FAU titles the lecture "Tissue Engineering: Basic Concepts".' % W),
    ('BME4361', 'Neural Engineering — interfacing devices with the nervous system: '
     'electrophysiology, stimulation, brain-computer interfaces.',
     '%s Carried by FAMU, FAU, Florida State and UF, all at 3 credits and all under the identical '
     'title — rare agreement in this prefix.' % W),
    ('BME4581', 'BioMEMS and microfluidics — lab-on-a-chip, microfabrication, point-of-care '
     'diagnostics.',
     '%s Carried by FAMU, FAU, Florida State and USF at 3 credits. FAU titles it "Introduction to '
     'Microfluidics and BioMEMS", which is the more descriptive name for the same course.' % W),
    ('BME4801', 'Biomedical Engineering Process Design — the capstone: design to a requirement, '
     'under the regulatory regime the products actually ship under.',
     '%s FAMU and Florida State run it as a TWO-TERM sequence, BME4801 then BME4802. UF and USF '
     'run BME4882, FIU and FGCU run BME4800C. %s Four programmes, four capstone structures — so '
     'a transfer in the final year is genuinely difficult. Raise it before the junior year.' % (WW, W)),
]

BODY = (
    '<h2>What the work actually is</h2>'
    '<p>O*NET&rsquo;s task statements: <em>evaluate the safety, efficiency and effectiveness of '
    'biomedical equipment; prepare technical reports, data summaries or research articles for '
    'publication; design or develop medical diagnostic and clinical instrumentation using '
    'engineering and biobehavioural science principles; conduct research on engineering aspects of '
    'biological systems; and adapt or design computer hardware or software for medical science '
    'applications.</em></p>'
    '<p>&#9888;&#9888; <strong>Read the first two again.</strong> The top task is <em>evaluating</em> '
    'equipment and the second is <em>writing</em> — not designing. That is what regulated '
    'industry looks like: a medical device is a documented device, and the evidence that it works '
    'is as much of the job as making it work. Students arrive expecting to invent prosthetics, and '
    'a great deal of the profession is verification, validation and the paper trail that lets a '
    'device be sold.</p>'
    '<h2>&#9888;&#9888;&#9888; Projected need — and the arithmetic every applicant should see</h2>'
    '<p>O*NET, on federal projections: <strong>22,200 bioengineers and biomedical engineers '
    'employed</strong> (2024), growth <strong>&ldquo;faster than average&rdquo;, 5&ndash;6% through '
    '2034</strong>, about <strong>1,300 openings a year</strong>, median pay '
    '<strong>$109,370</strong>.</p>'
    '<p>Now put the Florida supply beside it. <strong>Florida&rsquo;s six public programmes award '
    'about 284 bachelor&rsquo;s degrees a year.</strong> Florida is roughly 6.6% of the United '
    'States by population, so a proportionate share of 1,300 national openings is around '
    '<strong>86 a year</strong>.</p>'
    '<p>&#9888;&#9888;&#9888; <strong>This is the most important thing on the page, and it is not '
    'an argument against the degree.</strong> Graduates move between states, many openings are '
    'filled by people from adjacent disciplines, and a large share of biomedical engineering '
    'graduates do excellent work under other job titles — quality and regulatory affairs, '
    'manufacturing and process engineering, clinical engineering in hospitals, medical device '
    'sales engineering, software, and research. <strong>But the arithmetic is real, it is not '
    'printed on any programme page, and it should inform how you spend your electives.</strong></p>'
    '<h3>&#9888;&#9888; The education requirement says the same thing in a different way</h3>'
    '<p>O*NET asks employers what a new hire needs. For this occupation:</p>'
    '<table class="table table-sm"><thead><tr><th>Credential named</th><th>Share of employers</th>'
    '</tr></thead><tbody>'
    '<tr><td>Bachelor&rsquo;s degree</td><td><strong>43%</strong></td></tr>'
    '<tr><td>&#9888; Master&rsquo;s degree</td><td><strong>26%</strong></td></tr>'
    '<tr><td>&#9888; Doctoral degree</td><td><strong>13%</strong></td></tr>'
    '</tbody></table>'
    '<p>&#9888;&#9888;&#9888; <strong>Fewer than half of employers treat the bachelor&rsquo;s as '
    'sufficient.</strong> No other engineering discipline in this repository comes close to that. '
    '<strong>Biomedical engineering is, in practice, a discipline where the bachelor&rsquo;s is '
    'frequently a first degree rather than a terminal one</strong>, and the honest planning '
    'question is not <em>which major</em> but <em>what comes after it</em>.</p>'
    '<h3>Florida&rsquo;s own provision confirms it</h3>'
    '<p>&#9888;&#9888; <strong>The University of Central Florida and Florida Atlantic University '
    'award biomedical engineering degrees at master&rsquo;s and doctoral level and award NO '
    'bachelor&rsquo;s in the field.</strong> Two of the state&rsquo;s largest universities have '
    'built the graduate end of this discipline without the undergraduate end — which tells you '
    'something about where the discipline sits, and it is also useful news: <strong>they are places '
    'to continue, not places to start.</strong></p>'
    '<h2>Where you can study it in Florida</h2>'
    '<table class="table table-sm"><thead><tr><th>Institution</th><th>Bachelor&rsquo;s</th>'
    '<th>Master&rsquo;s</th><th>Doctorate</th></tr></thead><tbody>'
    '<tr><td>University of Florida</td><td><strong>115</strong></td><td>37</td><td>11</td></tr>'
    '<tr><td>Florida International University</td><td><strong>79</strong></td><td>12</td><td>6</td></tr>'
    '<tr><td>Florida State University</td><td>36</td><td>6</td><td>1</td></tr>'
    '<tr><td>University of South Florida</td><td>29</td><td>21</td><td>8</td></tr>'
    '<tr><td>Florida Gulf Coast University</td><td>21</td><td>&mdash;</td><td>&mdash;</td></tr>'
    '<tr><td>Florida A&amp;M University</td><td>4</td><td>2</td><td>&mdash;</td></tr>'
    '<tr><td>&#9888; University of Central Florida</td><td><strong>none</strong></td><td>11</td>'
    '<td>3</td></tr>'
    '<tr><td>&#9888; Florida Atlantic University</td><td><strong>none</strong></td><td>16</td>'
    '<td>&mdash;</td></tr>'
    '</tbody></table>'
    '<p>Six bachelor&rsquo;s programmes in <strong>five cities</strong> — Florida State and Florida '
    'A&amp;M share the <strong>FAMU-FSU College of Engineering</strong>, one joint college in '
    'Tallahassee, which is why they appear as a matched pair throughout the course list.</p>'
    '<h3>&#9888; Starting at a state college: there is exactly one door, and it is not the only route</h3>'
    '<p><strong>St. Petersburg College is the only Florida College System institution that carries '
    'any <code>BME</code> course at all</strong> — <code>BME1008C</code>, the introductory course. '
    'Everything else in the prefix is at a university.</p>'
    '<p>&#9888;&#9888; <strong>That is not a barrier, because the first two years of this degree '
    'are not biomedical engineering.</strong> They are calculus, physics, chemistry, majors biology '
    'and composition — all available at every state college in Florida. <strong>The A.A. route '
    'works: finish the calculus sequence through differential equations, both physics, both '
    'general chemistry and the majors biology sequence with laboratories, then transfer.</strong> '
    '&#9888; <strong>Biology is the part transfer applicants most often lack</strong>, because it is '
    'the requirement that distinguishes this degree from every other engineering major and it is '
    'easy to leave out of an engineering-shaped plan.</p>'
    '<h2>&#9888;&#9888;&#9888; A warning about this prefix&rsquo;s course records</h2>'
    '<p>This repository checks every course-looking token in a statewide prerequisite against who '
    'actually carries that course. <strong>The <code>BME</code> prefix returns the worst result '
    'measured anywhere in Florida.</strong></p>'
    '<p>Of <strong>100 active undergraduate <code>BME</code> records</strong>, 75 name at least one '
    'course in their prerequisite field. <strong>Fifteen of those 75 — one in five — name a course '
    'that NO Florida public institution carries.</strong> For comparison, the same test on criminal '
    'justice returns about 2%.</p>'
    '<p>Named examples a student will actually meet:</p>'
    '<table class="table table-sm"><thead><tr><th>Course</th><th>Its statewide prerequisite names</th>'
    '<th>Reality</th></tr></thead><tbody>'
    '<tr><td><code>BME3009</code> Introduction to BME</td><td><code>BSC2012</code></td>'
    '<td>&#9888; no carrier in Florida; the real sequence is <code>BSC2010</code>/<code>BSC2011</code></td></tr>'
    '<tr><td><code>BME4503</code> Biomedical Instrumentation</td><td><code>EGN3374C</code></td>'
    '<td>&#9888; no carrier in Florida</td></tr>'
    '<tr><td><code>BME4211</code> Biomechanics</td><td><code>BME4100</code></td>'
    '<td>&#9888; FAU and FIU only — so it fails at three of this course&rsquo;s four carriers</td></tr>'
    '<tr><td><code>BME4409</code> Quantitative Physiology</td><td>&ldquo;<code>PCB 3XXX</code> Cell '
    'and System Physiology&rdquo;</td><td>&#9888; a masked number whose title matches nothing</td></tr>'
    '</tbody></table>'
    '<p>&#9888;&#9888; <strong>The likeliest cause is age, not carelessness.</strong> Biomedical '
    'engineering is Florida&rsquo;s newest and fastest-growing engineering discipline. Its '
    'programmes were built recently and renumbered as they matured, and the statewide record kept '
    'the numbers that were proposed, used briefly, or retired along the way.</p>'
    '<p>&#9888;&#9888;&#9888; <strong>The consequence for you is simple and worth taking '
    'seriously: in this prefix, read the prerequisite from YOUR OWN institution&rsquo;s catalogue, '
    'every time.</strong> The state record will send you looking for courses that do not exist. '
    'That is true to some degree everywhere in Florida; here it is true one time in five.</p>'
    '<h2>Choosing electives so the degree keeps doors open</h2>'
    '<p>Given the arithmetic above, the single most useful thing a biomedical engineering student '
    'can do is <strong>make the degree legible to more than one kind of employer</strong>. The '
    'course list below is grouped so this is visible:</p>'
    '<ul>'
    '<li><strong>The electrical route</strong> — <code>BME4503</code> instrumentation, '
    '<code>BME4508</code> biosignals, <code>BME4531</code> imaging. This is the most employable '
    'cluster at bachelor&rsquo;s level, and it reads to electronics and instrumentation employers '
    'outside medicine as well as inside it.</li>'
    '<li><strong>The mechanical route</strong> — <code>BME4211</code> biomechanics, biomaterials, '
    'and the statics and mechanics-of-materials courses your programme requires. It leads toward '
    'orthopaedics and prosthetics, and it reads to mechanical employers.</li>'
    '<li><strong>The research route</strong> — <code>BME4332</code> cell and tissue engineering, '
    '<code>BME4361</code> neural engineering, <code>BME4581</code> BioMEMS. &#9888; <strong>These '
    'are the most interesting courses in the degree and the ones that most assume graduate '
    'study.</strong> Take them because you intend to continue, not instead of the employable '
    'cluster.</li>'
    '<li>&#9888;&#9888; <strong>The one nobody mentions: regulatory affairs and quality.</strong> '
    'FDA submissions, design controls under 21 CFR 820, ISO 13485 and IEC 62304 are how medical '
    'devices actually reach patients, the work is plentiful, and a graduate who can discuss design '
    'history files is unusual. If your programme offers anything in this area, take it.</li>'
    '</ul>'
    '<h2>Licensure, and why it is the minority case</h2>'
    '<p>Very few biomedical engineers hold a Professional Engineer licence — medical device '
    'manufacturing falls under the industrial exemption and employers hire on the degree and the '
    'project record. &#9888; The exception worth knowing is <strong>clinical engineering in '
    'hospitals and healthcare facility design</strong>, where sealed work sometimes arises.</p>'
    '<p>&#9888; <strong>Sit the FE examination in your final year anyway.</strong> It is inexpensive '
    'as a student and expensive to recreate later. Under s. 471.013(1)(a), Florida Statutes, an '
    'approved <em>engineering</em> curriculum needs four years of qualifying experience toward the '
    'PE. &#9888;&#9888; <strong>And check the ABET commission: biomedical engineering programmes '
    'should be accredited by the ENGINEERING Accreditation Commission</strong>, which is what '
    'carries the four-year route; an engineering technology accreditation adds two years.</p>'
)

DOC = {
    'name': 'Biomedical Engineer',
    'cipCode': '14.05',
    'socCode': '17-2031',
    'isPublished': True,
    'sortOrder': 90,
    'description':
        'Biomedical engineers apply engineering to medicine — instrumentation and imaging, '
        'biomaterials and implants, biomechanics, and the tissue and neural engineering at the '
        'research frontier. It is the fastest-growing and newest engineering discipline in '
        'Florida. ⚠⚠ It is also the one where the bachelor’s degree is least often '
        'the end of the story: only 43% of employers treat it as sufficient, and two Florida '
        'universities award the degree at graduate level ONLY. Read the projected-need section '
        'before you commit — the arithmetic is not on any programme page.',
    'credentialNote':
        '⚠⚠ THE CREDENTIAL QUESTION HERE IS NOT LICENSURE, IT IS THE DEGREE LEVEL. O*NET '
        'reports that 43% of employers require a bachelor’s, 26% a master’s and 13% a '
        'doctorate — by far the highest graduate expectation of any engineering discipline in '
        'this repository, and Florida’s own provision agrees: UCF and FAU award biomedical '
        'engineering at master’s and doctoral level and no bachelor’s at all. '
        '⚠ A Professional Engineer licence is uncommon; device manufacturing falls under the '
        'industrial exemption. The exception is clinical engineering and healthcare facility work. '
        '⚠ What employers do screen on is ABET accreditation under the ENGINEERING commission '
        '— verify the specific programme by name — and, increasingly, whether you can talk '
        'about design controls and FDA submissions.',
    'bodyHtml': BODY,
    # ⚠ PENDING_AFTER_DEPLOY: the 'chemical-engineering' link below is commented out
    # because that programme is added in PreseMakerRepo.Api/Data/Seed/programs.json and is NOT
    # SEEDED LIVE YET -- the push returns 422 "Unknown programme slug(s)". Ron deploys
    # 2026-09-19. AFTER THE DEPLOY: uncomment it, re-run this builder, and re-push. The same
    # applies to the 'biomedical-engineering' programme added in the same commit.
    'programs': [
        {'slug': 'mechanical-engineering',
         'note': '⚠ Worth reading before you choose, and not as a consolation. Mechanical '
                 'engineering is offered at every Florida public university, the occupation is '
                 'roughly fifteen times larger, and it feeds the orthopaedic and device industry '
                 'heavily — many biomedical roles are filled by mechanical graduates. If you '
                 'want device work at bachelor’s level rather than research, compare the two '
                 'honestly.'},
        # {'slug': 'chemical-engineering',
        #  'note': 'The other adjacent degree, and the relevant one if biomaterials, drug delivery '
        #          'or bioprocess manufacturing is what interests you. ⚠ Offered at only four '
        #          'Florida institutions in three cities — read its path before assuming it is '
        #          'available where you are.'},
    ],
    'courses': [
        dict([('courseId', c), ('reason', r)] + ([('variantNote', v)] if v else []))
        for c, r, v in COURSES
    ],
    'sources': [
        {'label': 'O*NET — Bioengineers and Biomedical Engineers (17-2031.00)',
         'url': 'https://www.onetonline.org/link/summary/17-2031.00',
         'note': 'Tasks, technology skills, wages, the employment projections and the '
                 'education-required percentages quoted on this page (22,200 employed, 5–6% '
                 'growth, ~1,300 openings, $109,370 median, 43/26/13 bachelor’s/master’s/'
                 'doctorate).'},
        {'label': 'U.S. Bureau of Labor Statistics — Bioengineers and Biomedical Engineers',
         'url': 'https://www.bls.gov/ooh/architecture-and-engineering/biomedical-engineers.htm',
         'note': 'Federal wage, employment and outlook detail for SOC 17-2031.'},
        {'label': 'IPEDS — Completions (C2023_A)',
         'url': 'https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx',
         'note': 'The source of the degree table: CIP 14.0501 completions by award level at '
                 'Florida public institutions, including the two universities that award only '
                 'graduate degrees.'},
        {'label': 'ABET — Accredited Program Search',
         'url': 'https://amspub.abet.org/aps/name-search?searchType=institution',
         'note': 'Verify the specific biomedical engineering programme, and confirm it is '
                 'accredited by the Engineering Accreditation Commission.'},
        {'label': 'BMES — Biomedical Engineering Society',
         'url': 'https://www.bmes.org/',
         'note': 'The professional society; student chapters exist at the Florida programmes, and '
                 'its annual meeting is where graduate recruitment happens.'},
        {'label': 'FDA — Medical Devices',
         'url': 'https://www.fda.gov/medical-devices',
         'note': 'Design controls (21 CFR 820), premarket submissions and device classification '
                 '— the regulatory framework the profession actually works inside, and the '
                 'elective area that most improves employability.'},
        {'label': 'FAMU-FSU College of Engineering',
         'url': 'https://eng.famu.fsu.edu/',
         'note': 'The joint college in Tallahassee shared by Florida A&M and Florida State — '
                 'why those two appear as a matched pair throughout the course list.'},
        {'label': 'Florida Board of Professional Engineers — Licensure',
         'url': 'https://fbpe.org/licensure/',
         'note': 'The FE and PE route, and s. 471.013 Florida Statutes on qualifying curricula.'},
        {'label': 'NCES — Classification of Instructional Programs (CIP 2020)',
         'url': 'https://nces.ed.gov/ipeds/cipcode/browse.aspx?y=55',
         'note': 'CIP 14.05 Biomedical/Medical Engineering, the anchor for this path.'},
    ],
}


def main():
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(DOC, ensure_ascii=False, indent=1))
    print('wrote %s' % os.path.normpath(OUT))
    print('  %d course(s), %d source(s), %d program link(s), body %d chars'
          % (len(DOC['courses']), len(DOC['sources']), len(DOC['programs']), len(BODY)))
    longest = max(DOC['courses'], key=lambda c: len(c.get('variantNote') or ''))
    print('  longest variantNote: %s at %d chars (limit 1000)'
          % (longest['courseId'], len(longest.get('variantNote') or '')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
