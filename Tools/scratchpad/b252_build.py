# -*- coding: utf-8 -*-
"""Batch 252: write the five writable requested guides to drafts/ (run from Tools/).

    python scratchpad/b252_build.py

Sources (2026-11-23): SCNS flat file (carriers, credits, statewide titles); catalog.ufl.edu/search (EDH 6046);
Seminole State's catalogue page (ACG2360); FAU and FIU Coursedog caches (BME4536, EEL3502, CGN4980); UWF's CEN
prefix PDF (CEN 6030, CEN 6017). Palm Beach State (DNS failure) and State College of Florida (empty 202) not read.
"""
import io
import json
import os
import sys

sys.path.insert(0, 'scratchpad')
from b251_build import lg, ul, table, off  # noqa: E402  (helpers only; importing does not rewrite drafts)

G = {}

# ---------------------------------------------------------------------------------------------------- EDH6046
G['EDH6046'] = dict(
    title='Diversity Issues in Higher Education',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("Graduate standing. UF's catalogue lists no course prerequisite. Usually taken in a master's or "
                   "doctoral programme in higher education administration or student affairs. Only the University of "
                   "Florida carries EDH 6046, so its syllabus is the authority on content; the statewide record for the "
                   "number is titled College Student and Culture. When transferring graduate credit, send the syllabus, "
                   "not just the number."),
    offering_notes={
        'summary': 'One Florida public institution carries EDH6046: the University of Florida, at 3 credits.',
        'hours_source': 'derived', 'derived_contact_hours': 45,
        'derivation': "UF publishes no contact hours; 45 is Florida's convention for a 3-credit lecture or seminar.",
        'offerings': [
            off('UF', 'University of Florida', 'Diversity Issues in Higher Education', 3,
                'Catalogue description: models, theories, and skills for understanding multicultural students at the '
                'postsecondary level. Letter grade.'),
        ]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>EDH6046 Diversity Issues in Higher Education</strong> is a graduate course for people who work, or '
        'will work, with college students. The University of Florida, the only Florida public institution that '
        'carries the number, describes it in one line: <em>models, theories, and skills for understanding '
        'multicultural students at the postsecondary level</em>. The statewide course record calls the same number '
        '<strong>College Student and Culture</strong>. Both point at the same subject: who college students are, how '
        'their backgrounds shape their experience of college, and what staff and faculty can do so that students of '
        'every background can succeed.</p>'
        '<p>The course belongs to the student affairs and higher education administration curriculum (EDH is the '
        'statewide prefix for higher education). It is typically taken alongside courses on student development '
        'theory, the history and organisation of American higher education, and research methods.</p>'
        '<p>Because UF publishes only a one-line description, this guide describes what such a course commonly covers '
        'and marks the institution-specific material as optional. The UF syllabus for the term you take it decides '
        'the actual readings and assignments.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>' + lg([
            'Describe the changing demographics of American and Florida college students (age, race and ethnicity, '
            'first-generation status, income, disability, veteran status, language background, gender and sexuality, '
            'religion) and where to find reliable data on them.',
            'Explain major <strong>models and theories</strong> used to understand students\' identity and development '
            'in college, and the evidence and criticisms attached to each.',
            'Analyse how <strong>campus climate</strong>, institutional policies and everyday practice affect the '
            'belonging, persistence and completion of different groups of students.',
            'Apply theory to a case: identify what a student or group needs, and propose a response that fits the '
            'institution\'s mission, policies and law.',
            'Reflect on one\'s own background and assumptions, and how they shape work with students.',
            'Communicate about difficult topics with students and colleagues in a way that is accurate, respectful and '
            'within professional ethics.',
        ]) + '<h3>Optional Outcomes</h3>' + lg([
            'Design or evaluate a programme or service for a specific student population, with an assessment plan.',
            'Review research on equity gaps in outcomes (access, retention, completion) and critique its methods.',
            'Explain the federal and Florida legal framework that governs student services, including '
            'non-discrimination law and Florida\'s 2023 restrictions on diversity, equity and inclusion spending.',
        ]) +
        '<h2>Major Topics</h2><h3>Required Topics</h3>' + lg([
            'Who today\'s college students are: national (NCES/IPEDS) and Florida data.',
            'Identity development models: racial and ethnic identity, gender and sexual identity, faith, social class, '
            'disability; intersectionality.',
            'College impact and student success frameworks: involvement, integration and persistence, validation, '
            'community cultural wealth, mattering and belonging.',
            'Campus climate: what it is, how it is measured, and how it affects outcomes.',
            'First-generation, low-income, transfer, adult, veteran, international and undocumented students.',
            'Professional competencies and ethics for student affairs work (ACPA/NASPA).',
        ]) + '<h3>Optional Topics</h3>' + lg([
            'Minority-serving institutions, including Florida\'s HBCUs and Hispanic-Serving Institutions.',
            'Students with disabilities: the ADA and Section 504 in higher education.',
            'Law and policy affecting diversity work after the 2023 U.S. Supreme Court admissions decision '
            '(<em>SFFA v. Harvard</em>) and Florida\'s 2023 legislation.',
            'Assessment and evaluation of student programmes.',
        ]) +
        '<h2>Resources &amp; Tools</h2>' + ul([
            'Standard texts in student development theory and college student diversity (the syllabus names the '
            'edition used).',
            'ACPA/NASPA <em>Professional Competency Areas for Student Affairs Educators</em>.',
            'NCES IPEDS and the Florida Board of Governors\' data for student demographics and outcomes.',
            'Journals: <em>Journal of College Student Development</em>, <em>Journal of Student Affairs Research and '
            'Practice</em>, <em>The Review of Higher Education</em>.',
        ]) +
        '<h2>Career Pathways</h2>' + ul([
            'Student affairs professionals: advising, residence life, orientation, student activities, career services, '
            'TRIO and access programmes (SOC 21-1012 Educational, Guidance and Career Counselors and Advisors).',
            'Postsecondary education administrators (SOC 11-9033).',
            'Institutional research and assessment staff.',
        ]) +
        '<h2>Special Information</h2>'
        '<h3>Offering Notes</h3>' + table(['Institution', 'Title', 'Credits', 'Contact hours'], [
            ['University of Florida', 'Diversity Issues in Higher Education', '3', 'not published (45 derived)'],
        ]) +
        '<p>UF is the only Florida public institution with EDH 6046. Other universities teach similar material under '
        'other numbers and titles, so a course from another university will not match by number.</p>'
        '<h3>Florida context</h3><p>Since 2023 (Senate Bill 266, which amended s. 1004.06, Florida Statutes), Florida\'s '
        'public colleges and universities may not spend state or federal funds on programmes or campus activities that '
        'advocate diversity, equity and inclusion, and UF closed its chief diversity office in 2024. The law is about '
        'spending on programmes and activities; this course still appears in UF\'s 2026-2027 catalogue. For a student '
        'planning a career in Florida student affairs, the practical point is that many offices have been renamed or '
        'restructured, and job titles have changed. Work that supports every student\'s success (advising, first-'
        'generation and transfer programmes, disability services, veterans\' services) continues. Read current '
        'job postings and your institution\'s policies rather than older descriptions of the field.</p>'
        '<h3>Position in the curriculum</h3><p>A graduate course, taken in a master\'s programme in student affairs or '
        'higher education administration, or in a doctoral programme. It works best after or with a course on student '
        'development theory.</p>'
        '<h3>Course format</h3><p>Expect a seminar: weekly reading, discussion, reflective writing and a case study or '
        'programme proposal. Reflection assignments can be personal; you choose what you share.</p>'
        '<h2>AI Integration (Optional)</h2><p>AI tools can summarise readings and draft programme proposals, but they '
        'are weak at exactly what this course is about. A model asked about "first-generation students" or any other '
        'group produces a generalisation, while the course teaches you to find out what an individual student needs. '
        'Models also mix up theories and invent citations. Use them for drafting and checking structure, verify every '
        'source, keep student information out of them (FERPA), and follow your instructor\'s policy.</p>'),
)

# ---------------------------------------------------------------------------------------------------- ACG2360
G['ACG2360'] = dict(
    title='Cost Accounting',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("ACG 2021 (Principles of Financial Accounting) and ACG 2071 (Managerial Accounting), each with a "
                   "grade of C or higher (Seminole State; check Palm Beach State and State College of Florida). "
                   "*** LOWER-DIVISION COURSE: it is a 2000-level course in the A.S. accounting programmes. A student "
                   "going on to a bachelor's in accounting will normally still need the university's upper-division "
                   "cost accounting course (ACG 3341, ACG 3361, ACG 4341 or ACG 3343, depending on the university), "
                   "because a 2000-level course cannot supply upper-division hours. Ask the university before "
                   "counting on a substitution."),
    offering_notes={
        'summary': 'Three Florida state colleges carry ACG2360, all at 3 credits: Palm Beach State College, State '
                   'College of Florida (Manatee-Sarasota) and Seminole State College. No university carries it.',
        'hours_source': 'derived', 'derived_contact_hours': 45,
        'derivation': "None of the three publishes contact hours; 45 is Florida's convention for a 3-credit lecture "
                      "course.",
        'offerings': [
            off('PBSC', 'Palm Beach State College', 'Cost Accounting', 3, 'Catalogue not readable by tooling.'),
            off('SCFMS', 'State College of Florida, Manatee-Sarasota', 'Cost Accounting', 3,
                'Catalogue not readable by tooling.'),
            off('SSCF', 'Seminole State College of Florida', 'Cost Accounting', 3,
                'Prerequisites ACG 2021 and ACG 2071 with C or higher. Typically offered in fall. Seminole State '
                'also carries the upper-division ACG 3361.'),
        ]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>ACG2360 Cost Accounting</strong> teaches how a business measures what its products and services '
        'cost. Seminole State College describes it as <em>a study of the fundamentals of cost accounting within an '
        'industrial organization</em>: the accounting for <strong>materials, labour and factory overhead</strong> in '
        'detail, <strong>job order and process costing</strong>, and <strong>standard costs, budgeting and managerial '
        'control</strong>. The statewide record titles the number <em>Basic Cost Accounting, Condensed</em>, which '
        'fits: it is a single-term, lower-division treatment of a subject universities teach at upper division.</p>'
        '<p>Three Florida state colleges carry it (Palm Beach State, State College of Florida and Seminole State), '
        'all at 3 credits, as part of their Associate in Science accounting programmes. It follows the two principles '
        'courses: financial accounting (ACG 2021) and managerial accounting (ACG 2071). With only three carriers, the '
        'outcomes below follow Seminole State\'s published description, and each college\'s syllabus sets the '
        'details.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>' + lg([
            'Classify costs (direct and indirect, product and period, fixed and variable) and explain how each is used.',
            'Account for <strong>materials, labour and factory overhead</strong>, including overhead rates and the '
            'treatment of over- and under-applied overhead.',
            'Prepare cost records under a <strong>job order costing</strong> system.',
            'Prepare a <strong>process costing</strong> production report using equivalent units.',
            'Set <strong>standard costs</strong> and calculate and interpret materials, labour and overhead variances.',
            'Prepare an operating <strong>budget</strong> and use budgets and variances for managerial control.',
        ]) + '<h3>Optional Outcomes</h3>' + lg([
            'Apply activity-based costing and compare it with traditional overhead allocation.',
            'Use cost-volume-profit analysis and relevant costs for short-term decisions.',
            'Build costing schedules in a spreadsheet.',
        ]) +
        '<h2>Major Topics</h2><h3>Required Topics</h3>' + lg([
            'Cost concepts, cost behaviour and the manufacturing cost flow (raw materials, work in process, finished '
            'goods, cost of goods sold).',
            'Materials control and costing; labour costing and payroll-related costs.',
            'Factory overhead: predetermined rates, application, and disposing of variances.',
            'Job order costing.',
            'Process costing: equivalent units, the cost of production report.',
            'Standard costing and variance analysis.',
            'Budgeting and managerial control.',
        ]) + '<h3>Optional Topics</h3>' + lg([
            'Activity-based costing and management.',
            'Joint products and by-products.',
            'Spoilage, rework and scrap.',
            'Cost-volume-profit analysis and relevant costing.',
        ]) +
        '<h2>Resources &amp; Tools</h2>' + ul([
            'A cost accounting textbook (the college names the edition; Seminole State\'s course page links to its '
            'textbook search).',
            'Spreadsheet software (Microsoft Excel).',
            'Institute of Management Accountants (IMA) resources for the CMA certification.',
        ]) +
        '<h2>Career Pathways</h2>' + ul([
            'Cost and accounting clerks, bookkeepers (SOC 43-3031 Bookkeeping, Accounting and Auditing Clerks).',
            'Cost accountants and accountants (SOC 13-2011), usually after a bachelor\'s degree.',
            'Cost estimators (SOC 13-1051) in manufacturing and construction.',
            'Florida employers with manufacturing cost systems: aerospace and defence (Space Coast, Orlando), medical '
            'devices, food processing and boat building.',
        ]) +
        '<h2>Special Information</h2>'
        '<h3>Offering Notes</h3>' + table(['Institution', 'Title', 'Credits', 'Contact hours'], [
            ['Palm Beach State College', 'Cost Accounting', '3', 'not published'],
            ['State College of Florida, Manatee-Sarasota', 'Cost Accounting', '3', 'not published'],
            ['Seminole State College', 'Cost Accounting', '3', 'not published (45 derived)'],
        ]) +
        '<p>All three carry it at 3 credits. Contact hours are derived from Florida\'s convention of 15 per credit.</p>'
        '<h3>Transfer: a lower-division course for a subject universities teach at upper division</h3>'
        '<p>Florida\'s universities teach cost accounting as an upper-division course, under several numbers: '
        '<strong>ACG 3341</strong> Cost Accounting I (Florida Atlantic, Florida Gulf Coast, Florida State, South '
        'Florida, and Chipola, Daytona State and Indian River among the state colleges), <strong>ACG 3361</strong> '
        '(UCF, FAMU, Seminole State), <strong>ACG 4341</strong> (UF at 4 credits, FIU, Eastern Florida, College of '
        'Central Florida) and <strong>ACG 3343</strong> (UWF, Miami Dade). Titles vary: FIU calls its ACG 4341 <em>Management '
        'Accounting</em> and Seminole State calls its ACG 3361 <em>Intermediate Managerial Accounting</em>. Because ACG 2360 is a 2000-level course, it '
        'cannot supply the upper-division hours a bachelor\'s degree requires, so a student who later enters a '
        'bachelor\'s in accounting should expect to take the university\'s course too, and will find much of it '
        'familiar. Get a written answer from the receiving department before assuming a substitution.</p>'
        '<h3>Certification</h3><p>Cost accounting is a core part of Part 1 of the <strong>Certified Management '
        'Accountant (CMA)</strong> exam (IMA), which covers cost management, budgeting and performance measurement. '
        'The CMA requires a bachelor\'s degree, so this course is a foundation rather than direct preparation.</p>'
        '<h3>Position in the curriculum</h3><p>The third accounting course in an A.S. programme, after financial and '
        'managerial accounting. Managerial accounting (ACG 2071) introduces job and process costing briefly; this '
        'course treats them in depth. Seminole State offers it in fall.</p>'
        '<h2>AI Integration (Optional)</h2><p>Spreadsheet assistants and AI tools can build costing schedules and '
        'explain variances quickly, and accounting software computes standard-cost variances automatically. The '
        'course matters because someone must decide which costs belong where: an overhead rate built on the wrong '
        'base, or a variance labelled favourable when it is not, looks just as tidy in generated output. Check '
        'every schedule\'s totals and cost flows by hand on small problems, and follow your instructor\'s policy.</p>'),
)

# ---------------------------------------------------------------------------------------------------- BME4536
G['BME4536'] = dict(
    title='Introduction to Bioimaging',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("EEL 3502 (Signals and Digital Filter Design) with a minimum grade of C, or permission of the "
                   "instructor (Florida Atlantic University, the only Florida public institution with BME 4536). The "
                   "course uses Fourier transforms, convolution, sampling and filtering from the first weeks, so "
                   "review signals and systems before it starts."),
    offering_notes={
        'summary': 'One Florida public institution carries BME4536: Florida Atlantic University, at 3 credits with 3 '
                   'lecture hours a week.',
        'hours_source': 'published', 'derived_contact_hours': 45,
        'derivation': 'FAU publishes 3 lecture (contact) hours a week, 45 over a 15-week term.',
        'offerings': [
            off('FAU', 'Florida Atlantic University', 'Introduction to Bioimaging', 3,
                'Prerequisite EEL 3502 with C or permission of instructor. 3 lecture hours a week.', 45),
        ]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>BME4536 Introduction to Bioimaging</strong> is an upper-division biomedical engineering course at '
        'Florida Atlantic University. FAU describes it as giving students <em>the necessary fundamental concepts to do '
        'research in biomedical imaging</em>: image characteristics, Fourier transforms, image acquisition, image '
        'processing and analysis, convolution, sampling, resolution, contrast and filtering, and the principles of the '
        'main imaging tools: <strong>radiography, CT, ultrasound, MRI and optical imaging</strong>.</p>'
        '<p>The course has two halves that depend on each other. The first is the mathematics of images as signals in '
        'two dimensions. The second is the physics of each modality: how X-rays, sound, magnetic resonance and light '
        'produce an image, and what limits its resolution and contrast. FAU frames it as preparation for research, in '
        'line with its college\'s interdisciplinary goals.</p>'
        '<p>FAU is the only Florida public institution with the number, so this guide follows FAU\'s description. '
        'Other universities teach medical imaging under other numbers (see Special Information).</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>' + lg([
            'Describe an image quantitatively: resolution, contrast, noise, signal-to-noise and contrast-to-noise '
            'ratios, and the point spread function.',
            'Apply the two-dimensional <strong>Fourier transform</strong>, <strong>convolution</strong> and the '
            '<strong>sampling</strong> theorem to imaging systems, including aliasing.',
            'Apply basic image processing and analysis: filtering, enhancement and simple segmentation.',
            'Explain how <strong>radiography and CT</strong> form images, including attenuation and the idea of '
            'reconstruction from projections.',
            'Explain how <strong>ultrasound</strong>, <strong>MRI</strong> and <strong>optical imaging</strong> form '
            'images, and compare the modalities by resolution, contrast mechanism, depth, speed, cost and safety.',
            'Choose a suitable modality for a biomedical question and justify the choice.',
        ]) + '<h3>Optional Outcomes</h3>' + lg([
            'Implement reconstruction or filtering in MATLAB or Python.',
            'Read and present a research paper in biomedical imaging.',
            'Discuss nuclear medicine imaging (PET, SPECT) and radiation safety.',
        ]) +
        '<h2>Major Topics</h2><h3>Required Topics</h3>' + lg([
            'Image characteristics: resolution, contrast, noise, artefacts.',
            'Linear systems in two dimensions: Fourier transforms, convolution, point spread and modulation transfer '
            'functions.',
            'Sampling, aliasing and image acquisition.',
            'Image processing and analysis: filtering in the spatial and frequency domains.',
            'Projection radiography and computed tomography.',
            'Ultrasound imaging.',
            'Magnetic resonance imaging.',
            'Optical imaging and microscopy.',
        ]) + '<h3>Optional Topics</h3>' + lg([
            'Nuclear medicine (PET and SPECT).',
            'Image registration and quantitative image analysis for research.',
            'Radiation dose and safety.',
        ]) +
        '<h2>Resources &amp; Tools</h2>' + ul([
            'A medical imaging textbook such as Prince and Links, <em>Medical Imaging Signals and Systems</em> (the '
            'instructor names the text).',
            'MATLAB (Image Processing Toolbox) or Python with NumPy, SciPy and scikit-image.',
            'ImageJ/Fiji for image analysis; public image sets such as The Cancer Imaging Archive.',
        ]) +
        '<h2>Career Pathways</h2>' + ul([
            'Biomedical engineers (SOC 17-2031) in imaging device design, testing and research.',
            'Imaging scientists and research engineers in university and hospital research groups.',
            'Field and applications engineers for imaging equipment makers.',
            'Graduate study in biomedical engineering, medical physics or medicine.',
            'Florida employers and research: hospital systems (Baptist Health South Florida, Memorial, Cleveland '
            'Clinic Florida, Mayo Clinic in Jacksonville), the National High Magnetic Field Laboratory in Tallahassee, '
            'and the state\'s medical device industry.',
        ]) +
        '<h2>Special Information</h2>'
        '<h3>Offering Notes</h3>' + table(['Institution', 'Title', 'Credits', 'Contact hours'], [
            ['Florida Atlantic University', 'Introduction to Bioimaging', '3', '45 (3 lecture hours a week, published)'],
        ]) +
        '<h3>Course-code variations across Florida</h3><p>BME 4536 is FAU\'s number. Other Florida universities teach '
        'biomedical imaging under different numbers, such as <strong>BME 4531</strong> (carried by FAMU, FIU, FSU, UF and '
        'USF). Different numbers are not equivalent by the statewide system, so a transfer student should send the '
        'syllabus and ask whether one substitutes for the other.</p>'
        '<h3>Position in the curriculum</h3><p>A junior or senior elective or requirement in biomedical engineering. Its '
        'gate, EEL 3502 Signals and Digital Filter Design, covers sampling, the z-transform, digital filters and the '
        'FFT, with image-processing applications in MATLAB; BME 4536 extends that to two dimensions and to imaging '
        'physics. Expect 8 to 10 hours of work a week.</p>'
        '<h3>FE exam</h3><p>The FE exam does not have a biomedical-specific section; most biomedical engineers take the '
        'FE Other Disciplines or Electrical and Computer exam. Signals and systems material in this course supports '
        'the latter.</p>'
        '<h2>AI Integration (Optional)</h2><p>AI is now part of medical imaging itself: deep-learning reconstruction '
        'lets CT and MRI scanners produce usable images from lower dose or faster scans, and AI tools that read images '
        'are cleared as medical devices by the FDA. This course teaches what those tools rest on. A network can '
        'produce a sharp-looking image that contains structures that were never measured, and only someone who '
        'understands sampling, noise and the physics of the modality can judge whether an image is trustworthy. '
        'General AI assistants are useful for code but make confident errors in imaging physics; check against the '
        'text, and follow your instructor\'s policy.</p>'),
)

# ---------------------------------------------------------------------------------------------------- CEN6030
G['CEN6030'] = dict(
    title='Agile Software Engineering',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("COP 6416 (University of West Florida, the only Florida public institution with CEN 6030). UWF "
                   "notes that students without enough academic or professional experience in computer science may "
                   "first have to complete graduate foundations courses in programming or equivalent undergraduate "
                   "coursework. CEN 6030 is in turn the prerequisite (or a same-term corequisite) for UWF's CEN 6017 "
                   "Continuous Software Engineering."),
    offering_notes={
        'summary': 'One Florida public institution carries CEN6030: the University of West Florida, at 3 semester '
                   'hours, not repeatable.',
        'hours_source': 'derived', 'derived_contact_hours': 45,
        'derivation': "UWF publishes no contact hours; 45 is Florida's convention for a 3-credit lecture course.",
        'offerings': [
            off('UWF', 'University of West Florida', 'Agile Software Engineering', 3,
                'Department of Computer Science. Prerequisite COP 6416. Leads to CEN 6017 Continuous Software '
                'Engineering.'),
        ]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>CEN6030 Agile Software Engineering</strong> is a graduate computer science course at the University '
        'of West Florida. UWF describes it as an <em>analysis and overview of concepts in agile software development</em>, '
        'covering <strong>agile principles, methodologies, practices, and artifacts</strong>. Agile development builds '
        'software in short iterations, delivers working software often, and adjusts the plan from feedback, in '
        'contrast to plan-driven methods that fix requirements first.</p>'
        '<p>At UWF the course is part of a graduate sequence: it follows COP 6416 and leads to <strong>CEN 6017 Continuous '
        'Software Engineering</strong> (continuous testing, integration, delivery and deployment), which may be taken '
        'after it or in the same term. UWF is the only Florida public institution that carries CEN 6030, so this guide '
        'follows its description; the syllabus sets the details.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>' + lg([
            'Explain the values and principles of the <strong>Agile Manifesto</strong> and how they differ from '
            'plan-driven development.',
            'Compare agile methodologies, chiefly <strong>Scrum</strong>, <strong>Kanban</strong> and <strong>Extreme '
            'Programming (XP)</strong>, and judge which suits a given team and project.',
            'Apply agile <strong>practices</strong>: user stories and acceptance criteria, backlog refinement, estimation, '
            'sprint planning, daily coordination, reviews and retrospectives.',
            'Produce and use agile <strong>artifacts</strong>: product and sprint backlogs, the increment, definition of '
            'done, burndown charts and task boards.',
            'Apply engineering practices that make short iterations possible: test-driven development, refactoring, '
            'pair programming, continuous integration.',
            'Critically analyse agile in practice: where it works, where it fails, and the evidence for each.',
        ]) + '<h3>Optional Outcomes</h3>' + lg([
            'Work on a team project run in sprints, with the team\'s artifacts as evidence.',
            'Discuss scaling agile across many teams (SAFe, LeSS) and its criticisms.',
            'Relate agile to DevOps and continuous delivery, in preparation for CEN 6017.',
        ]) +
        '<h2>Major Topics</h2><h3>Required Topics</h3>' + lg([
            'History and principles: the Agile Manifesto (2001) and its twelve principles.',
            'Scrum: roles, events and artifacts (the Scrum Guide).',
            'Kanban: visualising work, limiting work in progress, flow metrics.',
            'Extreme Programming: test-driven development, pair programming, small releases, collective ownership.',
            'Requirements in agile: user stories, acceptance criteria, story mapping, prioritisation.',
            'Estimation and planning: story points, velocity, release planning.',
            'Quality and technical debt.',
        ]) + '<h3>Optional Topics</h3>' + lg([
            'Scaling frameworks and agile in regulated or safety-critical settings.',
            'Lean software development.',
            'Distributed and remote agile teams.',
        ]) +
        '<h2>Resources &amp; Tools</h2>' + ul([
            'The Agile Manifesto (agilemanifesto.org) and the Scrum Guide (scrumguides.org), both free.',
            'Issue and board tools such as Jira, GitHub Projects or Azure Boards.',
            'Git and a continuous integration service (GitHub Actions, GitLab CI).',
            'A unit-testing framework for the course\'s programming language.',
        ]) +
        '<h2>Career Pathways</h2>' + ul([
            'Software developers (SOC 15-1252) and software quality assurance analysts and testers (SOC 15-1253).',
            'Scrum masters, agile coaches and project managers (SOC 13-1082 Project Management Specialists).',
            'Product owners and product managers.',
            'Florida employers in defence and aerospace software (Pensacola, Fort Walton Beach and the Space Coast), '
            'finance and health technology.',
        ]) +
        '<h2>Special Information</h2>'
        '<h3>Offering Notes</h3>' + table(['Institution', 'Title', 'Credits', 'Contact hours'], [
            ['University of West Florida', 'Agile Software Engineering', '3', 'not published (45 derived)'],
        ]) +
        '<h3>Certification</h3><p>The course covers much of what entry agile certifications test: Scrum.org\'s '
        '<strong>Professional Scrum Master I</strong>, Scrum Alliance\'s <strong>Certified ScrumMaster</strong>, and, '
        'with project experience, PMI\'s <strong>Agile Certified Practitioner (PMI-ACP)</strong>. A course does not '
        'award these; each has its own exam or training requirement.</p>'
        '<h3>Course-code variations across Florida</h3><p>Other Florida universities teach agile methods inside general '
        'graduate software engineering courses rather than as a course of its own (for example CEN 5035, carried by '
        'FAU, Florida Poly, FSU and UF). When transferring, send the syllabus.</p>'
        '<h3>Position in the curriculum</h3><p>A graduate course after COP 6416, and before or alongside CEN 6017 at UWF. '
        'Students coming from another field may first need UWF\'s graduate foundations courses in programming.</p>'
        '<h2>AI Integration (Optional)</h2><p>AI coding assistants change the speed of an iteration: code and tests are '
        'drafted faster, and tools can write user stories and summarise backlogs. Agile practice is what keeps that '
        'speed safe. Test-driven development, code review, a clear definition of done and continuous integration are '
        'the checks that catch generated code which compiles but does the wrong thing. Treat AI output as a team '
        'member\'s untested pull request, keep employer and client code out of public tools, and follow your '
        'instructor\'s policy.</p>'),
)

# ---------------------------------------------------------------------------------------------------- CGN4980
G['CGN4980'] = dict(
    title='Civil Engineering Seminar',
    credits=1, contact_hours=15, version='1.0',
    prerequisites=("None listed in FIU's catalogue (Florida International University is the only Florida public "
                   "institution with CGN 4980). The description says the seminar is for civil engineering students. "
                   "FIU lists it at 1 credit and allows it to be repeated; check with the department how many times "
                   "it counts toward the degree."),
    offering_notes={
        'summary': 'One Florida public institution carries CGN4980: Florida International University, at 1 credit, '
                   'repeatable.',
        'hours_source': 'derived', 'derived_contact_hours': 15,
        'derivation': "FIU publishes no contact hours; 15 is Florida's convention for a 1-credit lecture or seminar.",
        'offerings': [
            off('FIU', 'Florida International University', 'Civil Engineering Seminar', 1,
                'Repeatable. No prerequisite listed. For civil engineering students.'),
        ]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>CGN4980 Civil Engineering Seminar</strong> is a 1-credit seminar at Florida International '
        'University. FIU describes it as <em>basic principles and applications of civil engineering, including '
        'structural, transportation, environmental, geotechnical, construction, and water resources engineering for '
        'civil engineering students</em>. It is a survey of the whole discipline: one session or block for each '
        'specialty, usually with practising engineers and faculty describing their work.</p>'
        '<p>Its use is to help a student see the specialties side by side before choosing electives, a design project '
        'and a first job. FIU lists it as repeatable, which is typical of a seminar series whose speakers change from '
        'term to term.</p>'
        '<p>FIU is the only Florida public institution that carries the number. Note that the statewide record files '
        'CGN 4980 under a generic label for numbers ending in 98x (dissertation and defence); that label does not '
        'describe FIU\'s course. This guide follows FIU\'s description; the term\'s schedule of speakers sets the '
        'details.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>' + lg([
            'Describe the main specialties of civil engineering (structural, transportation, environmental, '
            'geotechnical, construction, and water resources) and the problems each solves.',
            'Explain how the specialties depend on each other on a real project.',
            'Describe the path to professional licensure: the FE exam, supervised experience, the PE exam.',
            'Identify the professional societies, codes and agencies that govern civil engineering practice in '
            'Florida.',
        ]) + '<h3>Optional Outcomes</h3>' + lg([
            'Write a short summary or reflection on a technical presentation.',
            'Discuss ethics and public safety in civil engineering using a case.',
            'Plan electives and a senior design topic around a chosen specialty.',
        ]) +
        '<h2>Major Topics</h2><h3>Required Topics</h3>' + lg([
            'Structural engineering: buildings and bridges.',
            'Transportation engineering: roads, traffic, transit.',
            'Environmental engineering: water and wastewater treatment, air quality.',
            'Geotechnical engineering: soils and foundations.',
            'Construction engineering and management.',
            'Water resources engineering: hydrology, hydraulics, stormwater and coastal flooding.',
            'Licensure and professional practice.',
        ]) + '<h3>Optional Topics</h3>' + lg([
            'Resilience to hurricanes, storm surge and sea-level rise in South Florida.',
            'Ethics cases and engineering failures.',
            'Careers in the public sector (FDOT, water management districts, counties) and in consulting.',
        ]) +
        '<h2>Resources &amp; Tools</h2>' + ul([
            'American Society of Civil Engineers (ASCE) and its FIU student chapter.',
            'NCEES information on the FE and PE exams; the Florida Board of Professional Engineers.',
            'Florida Department of Transportation and South Florida Water Management District publications.',
        ]) +
        '<h2>Career Pathways</h2>' + ul([
            'Civil engineers (SOC 17-2051) in structural, transportation, geotechnical, water resources and construction '
            'practice.',
            'Environmental engineers (SOC 17-2081).',
            'Employers in South Florida: FDOT District Six, Miami-Dade County, the South Florida Water Management '
            'District, consulting firms and contractors.',
        ]) +
        '<h2>Special Information</h2>'
        '<h3>Offering Notes</h3>' + table(['Institution', 'Title', 'Credits', 'Contact hours'], [
            ['Florida International University', 'Civil Engineering Seminar', '1', 'not published (15 derived)'],
        ]) +
        '<h3>FE exam and licensure</h3><p>The FE Civil exam covers all six specialties this seminar surveys. In Florida, '
        'a PE licence requires an accredited bachelor\'s degree, the FE exam, four years of qualifying experience and '
        'the PE exam (s. 471.013, Florida Statutes). A seminar is the right place to ask practising engineers how '
        'they prepared.</p>'
        '<h3>Course format</h3><p>A 1-credit seminar: attendance, presentations by faculty and practising engineers, '
        'and short written responses are typical. Grading is often based on attendance and participation; check the '
        'syllabus.</p>'
        '<h3>Transfer</h3><p>Seminar credit rarely transfers as a matching course. Other universities run similar '
        'seminars or orientation courses under other numbers.</p>'
        '<h2>AI Integration (Optional)</h2><p>AI tools can summarise a talk or a technical paper, but a summary written '
        'from a title will invent details the speaker never said. If the seminar asks for written responses, write '
        'from your own notes. Ask speakers how AI is used in their practice; civil engineers carry legal responsibility '
        'for sealed work, whatever tool produced the first draft.</p>'),
)

os.makedirs('drafts', exist_ok=True)
for cid, g in G.items():
    d = {'title': g['title'], 'html_content': g['html'], 'credits': g['credits'],
         'contact_hours': g['contact_hours'], 'prerequisites': g['prerequisites'], 'version': g['version'],
         'offering_notes': g['offering_notes']}
    path = os.path.join('drafts', '%s_guide.json' % cid)
    with io.open(path, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
    print('%-9s html %5d prereq %4d -> %s' % (cid, len(g['html']), len(g['prerequisites']), path))
