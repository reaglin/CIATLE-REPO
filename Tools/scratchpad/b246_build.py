#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Batch 246 -- scheduled request check 2026-11-20 (second run of the day).

Requests in rank order after the two held items (EEL2130C, ETI0602 -- REVIEW_QUEUE 124, 125):
CEN4020, EEL4030, EEL4062, EEL4021, EEL4016, EEL4010, EEL4005, EEL3970, EEL3955, EEL4070.

  Written    CEN4020 EEL4030 EEL4062 EEL4021 EEL4010 EEL4005 EEL4070
  Declined   EEL3970 (UCF honours thesis) and EEL3955 (UCF study abroad): shell numbers
  Held       EEL4016 (REVIEW_QUEUE 126): FIU, the only carrier, inactivated it in its own
             catalogue in 2004; SCNS still shows it active

Sources:
  USF        cloud.usf.edu/academic-programs/details/prefix/<PFX>/code/<NUM> -- NEW, answers 200 with
             description, credit hours and prerequisites (CEN4020, EEL4010, EEL4030)
  FAMU-FSU   eng.famu.fsu.edu ECE course lists (Undergraduate-Course-List.pdf, undated; and
             ECE_Undergraduate-Courses-Sp24.pdf) -- EEL4005, EEL4021, EEL4070
  FIU        Coursedog cache (fiu_courses.json) -- EEL4005, EEL4062, EEL4933, EEL4016
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


DERIVED = ("Florida's convention of 15 contact hours per credit for a lecture course; no carrier "
           'publishes a contact-hour figure for this number.')

# --------------------------------------------------------------------------
# CEN4020 Software Engineering -- FSU, USF
# --------------------------------------------------------------------------
CEN4020_PRE = ('USF: COP4530 Data Structures with a minimum grade of C; USF marks it a One USF Capstone '
               'course. FSU (Software Engineering I): prerequisite not confirmed for this guide; expect data '
               'structures and object-oriented programming, and check FSU\'s bulletin. *** Most Florida '
               'universities teach this subject as CEN4010, a different number: SCNS equivalence does not '
               'cross numbers, so bring a syllabus if you transfer.')

CEN4020_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>CEN4020 Software Engineering</strong> is an upper-division computer science course taught by '
    '<strong>two Florida public universities: Florida State University</strong> (as <em>Software Engineering '
    'I</em>) and the <strong>University of South Florida</strong> (as <em>Software Engineering</em>), both at '
    '3 credits. It teaches how working software is produced by a team: gathering and writing requirements, '
    'designing and modelling a system, managing a project, testing, and maintaining code that other people '
    'will read.</p>'
    '<p>USF\'s catalogue describes it as <em>"An overview of software engineering techniques for producing high '
    'quality software. Student will participate in a software development team."</em> It sits in USF\'s '
    'Bellini College of Artificial Intelligence, Cybersecurity, and Computing and carries the <strong>One USF '
    'Capstone</strong> attribute, so for many USF students it is the team-project course near the end of the '
    'degree. At FSU it is the first of a pair: <strong>CEN4020 Software Engineering I</strong> is followed by '
    '<strong>CEN4021 Software Engineering II</strong>, and FSU also carries a 1-credit <strong>CEN4090L Software '
    'Engineering Capstone Project</strong>. FSU\'s own description could not be read for this guide, so the '
    'outcomes below are the shared core of a first software engineering course; check the syllabus.</p>'
    + sec('Learning Outcomes', [
        'Elicit, analyse and write <strong>requirements</strong> (user stories, use cases, acceptance criteria) '
        'that a team can build and test against.',
        'Compare <strong>software process models</strong> &mdash; plan-driven, iterative and agile (Scrum, '
        'Kanban) &mdash; and work within one on a team project.',
        'Produce a <strong>design</strong> with UML class, sequence and state diagrams, and apply design '
        'principles (cohesion, coupling, SOLID) and common design patterns.',
        'Use <strong>version control</strong> (Git), code review, issue tracking and continuous integration '
        'as a team.',
        'Plan and carry out <strong>testing</strong>: unit, integration, system and acceptance tests, with '
        'test coverage and regression testing.',
        'Estimate, schedule and track work, and communicate progress in writing and in presentations.',
        'Recognise professional and ethical responsibilities (the ACM/IEEE-CS Software Engineering Code of '
        'Ethics), including security and privacy.'],
        [
        'Deliver a working product to a real or simulated client over a full term (USF\'s capstone use).',
        'Apply software metrics, refactoring and technical-debt management to an existing code base.',
        'Introduce DevOps, containers and cloud deployment (USF now also carries CEN4056 Hands-On DevOps and '
        'CEN4072 Software Testing as separate courses).',
        'Formal specification or model checking (more likely in FSU\'s two-course sequence).'])
    + sec('Major Topics', [
        'Software life cycle and process models; agile methods.',
        'Requirements engineering.',
        'Object-oriented analysis and design; UML.',
        'Architecture and design patterns.',
        'Configuration management and version control.',
        'Verification and validation; testing strategies.',
        'Project management, estimation and teamwork.',
        'Professional ethics.'],
        [
        'Software maintenance, refactoring and reverse engineering.',
        'DevOps and continuous delivery.',
        'Usability and user-centred design.',
        'Software quality standards (for example ISO/IEC 25010).'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul(
        '<em>Software Engineering</em>, Ian Sommerville (Pearson) and <em>Software Engineering: A '
        'Practitioner\'s Approach</em>, Pressman and Maxim (McGraw-Hill) &mdash; the two standard texts.',
        'The <strong>SWEBOK Guide</strong> (IEEE Computer Society), free online.',
        'Git with GitHub or GitLab; an issue tracker or board (GitHub Projects, Jira, Trello).',
        'A UML tool (PlantUML, draw.io, Lucidchart) and an IDE with a unit-testing framework (JUnit, pytest).',
        'The ACM/IEEE-CS <em>Software Engineering Code of Ethics and Professional Practice</em>.')
    + '<h2>Career Pathways</h2>'
    + ul(
        '<strong>Software developer</strong> (SOC 15-1252) &mdash; the occupation this course most directly '
        'prepares for.',
        '<strong>Software quality assurance analyst and tester</strong> (SOC 15-1253).',
        '<strong>Project and product roles</strong> on software teams (scrum master, product owner) after '
        'some experience.',
        'Florida employers range from defence and aerospace software (Lockheed Martin, L3Harris, Northrop '
        'Grumman) to finance and insurance in Tampa Bay and Jacksonville, health systems, simulation and '
        'training around Orlando, and a large consulting sector.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>Both carriers run it at 3 credits</strong>: FSU as <em>Software Engineering I</em> and USF as '
    '<em>Software Engineering</em>. Neither publishes contact hours, so the 45 shown are derived from '
    'Florida\'s convention of 15 per credit for a lecture course. The University of Central Florida '
    '(<em>Component-Based Engineering Software</em>, discontinued 2012) and the University of West Florida '
    '(<em>Software Engineering I</em>, discontinued 1995) once carried the number.</p>'
    '<h3>⚠ The usual Florida number for this subject is CEN4010</h3>'
    '<p><strong>CEN4010</strong> is carried by five public institutions &mdash; Daytona State College, '
    'Florida Atlantic University, FIU, FSU and the University of North Florida. CEN4020 and CEN4010 are '
    'different numbers, so Florida\'s course numbering system does <strong>not</strong> treat them as '
    'equivalent automatically, even though the subject overlaps heavily. FSU carries both: its CEN4010 is '
    '<em>Software Engineering Principles and Practice</em>. If you transfer, bring the syllabus and ask the '
    'receiving department to evaluate it.</p>'
    '<h3>Prerequisites and preparation</h3>'
    '<p>USF requires <strong>COP4530 Data Structures with a C or better</strong>. Come able to write and debug '
    'a program of several hundred lines in an object-oriented language. FSU\'s prerequisite could not be '
    'confirmed for this guide.</p>'
    '<h3>What the course is like</h3>'
    '<p>Most of the grade usually comes from a <strong>team project</strong> with documents, demonstrations '
    'and peer evaluation. The hard part is not the code but coordinating with teammates on a schedule. '
    'Expect 8&ndash;12 hours a week outside class, more near deliverables.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI coding assistants (GitHub Copilot, ChatGPT, Claude and others) are now part of professional '
    'software work, and this course is the natural place to learn to use them responsibly. They are good at '
    'boilerplate, test scaffolding, explaining unfamiliar code and drafting documentation. They are poor at '
    'the things this course grades: understanding what the client actually needs, keeping a design consistent '
    'across a team, and knowing when generated code is subtly wrong or insecure. Treat AI output like a pull '
    'request from a stranger &mdash; review it, test it, and be able to explain every line. Follow your '
    'instructor\'s and team\'s policy on AI use, and say in your documentation where you used it.</p>'
)

CEN4020 = {
    'title': 'Software Engineering',
    'html_content': CEN4020_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': CEN4020_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'Two public carriers, FSU (Software Engineering I) and USF (Software Engineering), both at '
                   '3 credits. Most Florida institutions teach the subject as CEN4010 (Daytona State, FAU, '
                   'FIU, FSU, UNF).',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [
            {'institution': 'FSU', 'institution_name': 'Florida State University',
             'title': 'Software Engineering I', 'credits': 3, 'contact_hours': None,
             'note': 'First of CEN4020/CEN4021; FSU also carries CEN4090L Capstone Project (1 cr) and '
                     'CEN4010. Description and prerequisite not confirmed.'},
            {'institution': 'USF', 'institution_name': 'University of South Florida',
             'title': 'Software Engineering', 'credits': 3, 'contact_hours': None,
             'note': 'Prerequisite COP4530 (min grade C). One USF Capstone attribute. Bellini College of AI, '
                     'Cybersecurity, and Computing.'}],
    },
}

# --------------------------------------------------------------------------
# EEL4030 Electrical Systems Environments -- USF
# --------------------------------------------------------------------------
EEL4030_PRE = ('USF, the only carrier: MAP2302 Differential Equations AND PHY2049 Physics II '
               '(calculus-based). No electrical engineering course is required, but circuits (EEL3100 or '
               'equivalent) helps. Check that USF is scheduling it in your term: it is an elective and the '
               'number dates from 2001.')

EEL4030_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4030 Electrical Systems Environments</strong> is an upper-division electrical engineering '
    'course taught by <strong>one Florida public institution, the University of South Florida</strong>, at 3 '
    'credits. USF\'s catalogue describes it as <em>"Dynamics, vibration, thermodynamics, and heat transfer in '
    'electrical, electronic, and electromechanical systems and their environments."</em></p>'
    '<p>In other words, it is the <strong>mechanical side of electronic hardware</strong>: why circuit boards '
    'and power electronics overheat and how to cool them, how vibration and shock break solder joints and '
    'connectors, and how temperature and the operating environment set how long a product lasts. Electrical '
    'engineering curricula rarely teach heat transfer or vibration otherwise, and this course fills that gap '
    'for students heading into electronics packaging, power electronics, aerospace and defence hardware.</p>'
    '<p>Because only USF teaches it and its description is a single sentence, the outcomes and topics below '
    'are the standard content of such a course. Treat them as its expected shape and check the syllabus for '
    'your term.</p>'
    + sec('Learning Outcomes', [
        'Apply the first law of thermodynamics to energy balances in electronic and electromechanical equipment.',
        'Model <strong>conduction, convection and radiation</strong> and use <strong>thermal resistance '
        'networks</strong> to estimate component and junction temperatures.',
        'Size <strong>heat sinks</strong>, fans and other cooling methods for a given power dissipation.',
        'Model <strong>vibration</strong> of simple structures (single- and multi-degree-of-freedom systems), '
        'including natural frequency, damping and resonance.',
        'Assess the effect of <strong>shock and vibration</strong> on boards, components and mounts.',
        'Relate operating temperature and environment to <strong>reliability</strong> and expected life.'],
        [
        'Use thermal or structural simulation software (finite-element or CFD) on an electronic assembly.',
        'Read and apply environmental test standards such as MIL-STD-810 and the JEDEC test methods.',
        'Consider humidity, corrosion and contamination as environmental stresses.'])
    + sec('Major Topics', [
        'Review of dynamics and of thermodynamics.',
        'Steady and transient heat conduction; thermal resistance and capacitance.',
        'Natural and forced convection; fans and air flow.',
        'Radiation heat transfer.',
        'Heat sinks, interface materials and board-level thermal design.',
        'Free and forced vibration; damping; resonance.',
        'Shock and random vibration in electronic equipment.'],
        [
        'Reliability and temperature (Arrhenius-type acceleration).',
        'Liquid cooling and two-phase cooling for high-power electronics.',
        'Environmental qualification testing.',
        'Numerical simulation (FEA and CFD).'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul(
        '<em>Cooling Techniques for Electronic Equipment</em>, Dave S. Steinberg (Wiley), and <em>Vibration '
        'Analysis for Electronic Equipment</em>, Steinberg (Wiley) &mdash; the classic pair for exactly this '
        'subject.',
        'A heat transfer text such as <em>Fundamentals of Heat and Mass Transfer</em>, Incropera et al. (Wiley).',
        'MATLAB or Python for models; thermal and structural simulation tools (for example ANSYS, '
        'SOLIDWORKS Simulation, or an electronics-cooling CFD package).',
        'Standards worth knowing by name: <strong>MIL-STD-810</strong> (environmental engineering '
        'considerations and laboratory tests) and the <strong>JEDEC</strong> thermal and reliability test '
        'methods.')
    + '<h2>Career Pathways</h2>'
    + ul(
        '<strong>Electronics packaging and thermal engineer</strong> (often classed as electrical, electronics '
        'or mechanical engineer: SOC 17-2072, 17-2141).',
        '<strong>Hardware reliability and test engineer</strong> running environmental qualification.',
        '<strong>Aerospace and defence electronics</strong>: Tampa Bay has a large defence and electronics '
        'manufacturing base (Jabil is headquartered in St. Petersburg), and the Space Coast and Orlando have '
        'many more.',
        '<strong>Power electronics</strong> for electric vehicles, solar inverters and data centres, where '
        'cooling limits the design.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: the University of South Florida, at 3 credits.</strong> USF publishes no '
    'contact-hour figure, so the 45 hours shown are derived from Florida\'s convention of 15 per credit for a '
    'lecture course. The statewide title is <em>Electrical Systems Environment</em>.</p>'
    '<h3>Prerequisites and preparation</h3>'
    '<p>USF requires <strong>MAP2302 Differential Equations and PHY2049 Physics II</strong>. The course '
    'assumes no prior heat transfer or vibration, but it moves quickly through mechanical-engineering '
    'material that electrical engineering students have not seen since physics. Review energy, '
    'Newton\'s second law and first-order and second-order differential equations before it starts.</p>'
    '<h3>Is it still taught?</h3>'
    '<p>The number entered the state course file in 2001 and was last changed in 2007, and USF lists it as '
    'an elective. Check USF\'s schedule for the term you want it; electives of this kind are not offered '
    'every semester.</p>'
    '<h3>Related courses</h3>'
    '<p>No other Florida public institution carries this number. Students elsewhere usually take the '
    'subject piecemeal through mechanical engineering heat transfer and vibrations courses, which are '
    'different numbers and do not substitute for it automatically.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain a concept, set up the algebra of a thermal resistance network, or write a script '
    'that sweeps fan speed or heat-sink size. They are unreliable on units and on which correlation applies: '
    'they mix W/m&middot;K with W/m&sup2;&middot;K, use a forced-convection correlation for natural convection, '
    'or ignore that a resonance falls inside the excitation band. <strong>Check every number with a simple '
    'energy balance and an order-of-magnitude estimate</strong>, and follow your instructor\'s policy on AI use.</p>'
)

EEL4030 = {
    'title': 'Electrical Systems Environments',
    'html_content': EEL4030_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4030_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, the University of South Florida, at 3 credits.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [{
            'institution': 'USF', 'institution_name': 'University of South Florida',
            'title': 'Electrical Systems Environments', 'credits': 3, 'contact_hours': None,
            'note': 'Prerequisites MAP2302 and PHY2049. Catalogue: "Dynamics, vibration, thermodynamics, and '
                    'heat transfer in electrical, electronic, and electromechanical systems and their '
                    'environments."'}],
    },
}

# --------------------------------------------------------------------------
# EEL4062 Engineering Business Plan Development -- FIU
# --------------------------------------------------------------------------
EEL4062_PRE = ('FIU, the only carrier: EEL4933 Engineering Entrepreneurship, FIU\'s first course in the '
               'pair. Take EEL4933 first; this course builds the business plan for a venture idea. No '
               'business course is required, but basic accounting helps with the financial projections.')

EEL4062_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4062 Engineering Business Plan Development</strong> is an upper-division course in the '
    'Department of Electrical and Computer Engineering at <strong>Florida International University</strong>, '
    'the only Florida public institution that carries it, at 3 credits. FIU describes it in one sentence: '
    '<em>"This course is designed to help students develop an effective implementation plan for a new '
    'business venture."</em></p>'
    '<p>It is the second half of a pair. FIU\'s prerequisite, <strong>EEL4933 Engineering '
    'Entrepreneurship</strong>, uses <em>"lectures, case studies, and seminars"</em> given by engineers, '
    'business people and specialists to introduce starting a technology business; EEL4062 then has the '
    'student turn an idea into a written <strong>business plan</strong>. Because FIU publishes so little, the '
    'outcomes and topics below are the standard content of an engineering business-plan course. Treat them as '
    'its expected shape and check the syllabus.</p>'
    + sec('Learning Outcomes', [
        'Define a <strong>customer problem</strong> and a product or service that solves it, and test the idea '
        'by talking to potential customers (customer discovery).',
        'Size a <strong>market</strong> and analyse competitors.',
        'Choose a <strong>business model</strong> and pricing, using a tool such as the Business Model Canvas.',
        'Build simple <strong>financial projections</strong>: costs, revenue, cash flow and break-even.',
        'Identify <strong>intellectual property</strong> (patents, trade secrets, licensing) and regulatory '
        'requirements for a technical product.',
        'Plan the operations, team and milestones needed to launch.',
        'Write a complete business plan and present it as a pitch.'],
        [
        'Explore funding routes: bootstrapping, grants (SBIR/STTR), angel and venture investment.',
        'Enter a business-plan or pitch competition.',
        'Prepare an intrapreneurship plan for a new product inside an existing company.'])
    + sec('Major Topics', [
        'Opportunity recognition and customer discovery.',
        'Market analysis and competition.',
        'Business models and the Business Model Canvas.',
        'Financial statements and projections for a start-up.',
        'Intellectual property and technology commercialisation.',
        'Operations, team and legal structure.',
        'Writing the plan; the pitch.'],
        [
        'Federal SBIR/STTR programmes for technical start-ups.',
        'Equity, valuation and term sheets.',
        'Manufacturing and supply chain for a hardware product.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul(
        '<em>Business Model Generation</em>, Osterwalder and Pigneur (Wiley), source of the Business Model '
        'Canvas.',
        '<em>The Startup Owner\'s Manual</em>, Blank and Dorf, and <em>The Lean Startup</em>, Eric Ries.',
        'A spreadsheet for financial projections.',
        'The U.S. Patent and Trademark Office search tools, and the SBIR.gov site for federal small-business '
        'research funding.',
        'The Florida Small Business Development Center network (Florida SBDC), which advises new businesses '
        'at no cost.')
    + '<h2>Career Pathways</h2>'
    + ul(
        '<strong>Founder</strong> of a technology start-up.',
        '<strong>Product manager</strong> or technical product owner in an established company.',
        '<strong>Business development and technical sales engineer</strong> (SOC 41-9031 sales engineers).',
        '<strong>Technology transfer and commercialisation</strong> roles at universities and research '
        'laboratories.',
        'Any engineering career: understanding cost, market and customer makes an engineer more effective '
        'and more promotable.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: Florida International University, at 3 credits.</strong> FIU publishes no '
    'contact-hour figure, so the 45 hours shown are derived from Florida\'s convention of 15 per credit for '
    'a lecture course. The number entered the state course file in 2018.</p>'
    '<h3>The sequence</h3>'
    '<p>Take <strong>EEL4933 Engineering Entrepreneurship</strong> first; it is FIU\'s stated prerequisite. '
    'At FIU the pair is an elective option for engineering students, so check how many credits of it your '
    'degree will count.</p>'
    '<h3>Related courses elsewhere in Florida</h3>'
    '<p>No other public institution carries EEL4062. The University of Florida teaches <strong>EGN4641 '
    'Engineering Entrepreneurship</strong>, and business colleges teach new-venture planning under '
    '<strong>ENT</strong> numbers (for example ENT4113 at FIU). These are different numbers and are evaluated '
    'case by case on transfer.</p>'
    '<h3>What the course is like</h3>'
    '<p>Expect a term-long project rather than examinations: interviews with potential customers, drafts of '
    'each section of the plan, and a final pitch. The work is less mathematical than most engineering '
    'courses but takes steady time, often 6&ndash;10 hours a week.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can help draft sections of a plan, suggest competitors to look into, and build a first '
    'spreadsheet model. They cannot do the part that matters most: <strong>talking to real customers</strong>. '
    'Market sizes, prices and competitor facts produced by a chatbot are often invented or out of date, so '
    'every number in the plan needs a source you can name. Investors and judges notice generic, AI-written '
    'prose. Follow your instructor\'s policy on AI use and say where you used it.</p>'
)

EEL4062 = {
    'title': 'Engineering Business Plan Development',
    'html_content': EEL4062_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4062_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, Florida International University, at 3 credits; second course after '
                   'EEL4933 Engineering Entrepreneurship.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [{
            'institution': 'FIU', 'institution_name': 'Florida International University',
            'title': 'Engineering Business Plan Development', 'credits': 3, 'contact_hours': None,
            'note': 'Prerequisite EEL4933. Catalogue: "This course is designed to help students develop an '
                    'effective implementation plan for a new business venture."'}],
    },
}

# --------------------------------------------------------------------------
# EEL4021 Statistical Topics in Electrical Engineering -- FAMU, FSU
# --------------------------------------------------------------------------
EEL4021_PRE = ('FAMU-FSU College of Engineering: MAS3105 Linear Algebra and EEL3112 Advanced Circuits '
               '(the Spring 2024 course list also accepts EEL3003; an undated list gives EEL3112 and MAP3306 '
               'or MAS3105). Check the current bulletin. *** It is a prerequisite or corequisite (C- or '
               'better for EEL4515) for the college\'s communications, radar, sonar and AI electives, so '
               'take it by the start of senior year.')

EEL4021_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4021 Statistical Topics in Electrical Engineering</strong> is the probability and '
    'statistics course of the <strong>FAMU-FSU College of Engineering</strong> in Tallahassee, the joint '
    'college of Florida A&amp;M University and Florida State University. Both universities list it in the '
    'state course file at 3 credits, but it is one course taught by one department. The college describes '
    'it as <em>"the use of probability and statistical concepts in electrical engineering applications"</em>.</p>'
    '<p>The catalogue lists its content: <em>elementary probability</em> (sets, sample spaces, axioms, joint '
    'and conditional probability); <em>random variables</em> (distribution and density functions); '
    '<em>operations on random variables</em> (expectation, moments, transformations); <em>multiple random '
    'variables</em>; an <em>introduction to random processes</em>; and <em>elements of statistics</em> '
    '(parameter estimation and hypothesis testing). It is the foundation for noise, detection and '
    'communication theory, which is why so many later electives require it.</p>'
    + sec('Learning Outcomes', [
        'Compute probabilities using the axioms, <strong>conditional probability</strong>, independence and '
        'Bayes\' theorem.',
        'Work with discrete and continuous <strong>random variables</strong> through their distribution and '
        'density functions, including the binomial, Poisson, uniform, exponential and Gaussian.',
        'Compute <strong>expectations, moments</strong> and the distribution of a function of a random '
        'variable.',
        'Analyse <strong>multiple random variables</strong>: joint and marginal densities, correlation, '
        'covariance and sums of random variables (central limit theorem).',
        'Describe <strong>random processes</strong> with mean, autocorrelation and power spectral density, '
        'and model noise in electrical systems.',
        'Estimate parameters and carry out <strong>hypothesis tests</strong> on engineering data.'],
        [
        'Pass a random process through a linear system and compute the output spectrum.',
        'Apply probability to bit-error rates, detection and reliability.',
        'Simulate random experiments in MATLAB or Python (Monte Carlo).'])
    + sec('Major Topics', [
        'Sets, sample spaces and the axioms of probability.',
        'Conditional probability, independence and Bayes\' theorem.',
        'Random variables; CDFs and PDFs; common distributions.',
        'Expectation, moments and transformations of random variables.',
        'Multiple random variables; correlation; the central limit theorem.',
        'Introduction to random processes; stationarity; autocorrelation and power spectral density.',
        'Parameter estimation and hypothesis testing.'],
        [
        'White and Gaussian noise; signal-to-noise ratio.',
        'Confidence intervals and regression.',
        'Markov chains.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul(
        '<em>Probability, Random Variables, and Random Signal Principles</em>, Peebles (McGraw-Hill), and '
        '<em>Probability and Random Processes for Electrical and Computer Engineers</em>, Gubner (Cambridge) '
        '&mdash; texts written for exactly this course.',
        '<em>Probability, Statistics, and Random Processes for Electrical Engineering</em>, Leon-Garcia '
        '(Pearson).',
        'MATLAB (Statistics and Machine Learning Toolbox) or Python (NumPy, SciPy) for simulation.')
    + '<h2>Career Pathways</h2>'
    + ul(
        '<strong>Communications and signal-processing engineer</strong> (SOC 17-2071, 17-2072): wireless, '
        'radar, sonar and satellite systems, where noise and detection are probability problems.',
        '<strong>Machine learning and data roles</strong> in engineering: the course is the mathematical '
        'base of the college\'s AI and machine learning electives.',
        '<strong>Reliability, quality and test engineering</strong>.',
        'Florida\'s defence and aerospace employers (L3Harris, Lockheed Martin, Northrop Grumman, the Naval '
        'Surface Warfare Center Panama City) hire heavily in radar, sonar and communications.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>Two carriers in the state file, FAMU and FSU, both at 3 credits &mdash; one course</strong>, '
    'taught by the joint FAMU-FSU College of Engineering. Neither publishes contact hours, so the 45 shown '
    'are derived from Florida\'s convention of 15 per credit for a lecture course. The statewide title is '
    '<em>Statistical Topics</em>.</p>'
    '<h3>Prerequisites</h3>'
    '<p>Two of the college\'s course lists give different prerequisites: the Spring 2024 list gives '
    '<strong>MAS3105 Linear Algebra and EEL3112 (or EEL3003)</strong>; an undated list gives <strong>EEL3112 '
    'and MAP3306 or MAS3105</strong>. Both expect calculus through multivariable integration, which you need '
    'for joint densities. Check the bulletin for your catalogue year.</p>'
    '<h3>Why to take it on time</h3>'
    '<p>In the college\'s lists EEL4021 is a <strong>prerequisite or corequisite</strong> for EEL4515 Digital '
    'Communication Systems (with a C- or better), EEL4566 Optical Fiber Communications, EEL4595 Wireless '
    'Communications and Networking, EEL4596 Advanced Topics in Communications, EEE4550 Radar, EEL4415 Sonar '
    'and EEE4872 Artificial Intelligence. Leaving it late can block a whole cluster of senior electives.</p>'
    '<h3>The same subject under other numbers</h3>'
    '<p>Most Florida universities teach engineering probability as <strong>STA3032 Probability and '
    'Statistics for Engineers</strong> (Florida Poly, FSU, UCF, UF and UNF). The University of Florida also '
    'carries EEL3850 <em>Data Science for ECE</em>. These are different numbers and do not substitute '
    'automatically; STA3032 usually covers less on random processes, so ask before assuming it satisfies '
    'EEL4021 if you transfer to Tallahassee.</p>'
    '<h3>FE exam relevance</h3>'
    '<p>Probability and statistics is a section of the NCEES <strong>FE Electrical and Computer</strong> exam, '
    'and random processes underlie its communications questions.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI assistants are useful for explaining a concept another way, checking an integral, and writing '
    'Monte Carlo simulations. They make predictable mistakes in probability: confusing a PDF with a CDF, '
    'treating dependent events as independent, dropping the Jacobian when transforming a random variable, and '
    'stating results with confidence that a short simulation disproves. <strong>Check an analytic answer with '
    'a simulation, and a simulation with an analytic limit.</strong> Follow your instructor\'s policy on AI use.</p>'
)

EEL4021 = {
    'title': 'Statistical Topics in Electrical Engineering',
    'html_content': EEL4021_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4021_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'FAMU and FSU, both at 3 credits: one course taught by the joint FAMU-FSU College of '
                   'Engineering. Elsewhere the subject is usually STA3032.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [
            {'institution': 'FAMU', 'institution_name': 'Florida Agricultural and Mechanical University',
             'title': 'Statistical Topics in Electrical Engineering', 'credits': 3, 'contact_hours': None,
             'note': 'Taught by the joint FAMU-FSU College of Engineering.'},
            {'institution': 'FSU', 'institution_name': 'Florida State University',
             'title': 'Statistical Topics in Electrical Engineering', 'credits': 3, 'contact_hours': None,
             'note': 'Taught by the joint FAMU-FSU College of Engineering. Prerequisites MAS3105 and EEL3112 '
                     'or EEL3003 (Spring 2024 list).'}],
    },
}

# --------------------------------------------------------------------------
# EEL4010 MAKE Hands-On Engineering Design -- USF
# --------------------------------------------------------------------------
EEL4010_PRE = ('USF, the only carrier: no prerequisite is listed in USF\'s catalogue. Some programming and a '
               'first circuits course make it much easier, and USF may restrict seats to engineering '
               'students; check before registering.')

EEL4010_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4010 MAKE Hands-On Engineering Design</strong> is a project course in the Department of '
    'Electrical and Computer Engineering at the <strong>University of South Florida</strong>, the only Florida '
    'public institution that carries it, at 3 credits. USF\'s catalogue says its primary objective is '
    '<em>"to introduce students to the creative design of devices following the engineering design '
    'process"</em>, teaching <em>"the essential design skills needed for the design of ‘mechatronic’ '
    'devices (i.e. devices incorporating electronic, mechanical and software based components)."</em> '
    'Students leave with <em>"basic knowledge in computer aided design, electronic circuit development, '
    'programming concepts and control systems."</em></p>'
    '<p>"MAKE" points to the maker movement: students design, build and test working gadgets. The outcomes '
    'below follow USF\'s description; the specific projects, platforms and tools vary by instructor, so check '
    'the syllabus.</p>'
    + sec('Learning Outcomes', [
        'Follow the <strong>engineering design process</strong>: define a need, set requirements, generate and '
        'choose concepts, prototype, test and iterate.',
        'Model parts and assemblies in <strong>computer-aided design</strong> (CAD) and make them by 3D '
        'printing or laser cutting.',
        'Build and debug simple <strong>electronic circuits</strong> with sensors, actuators and a power '
        'supply.',
        'Program a <strong>microcontroller</strong> to read sensors and drive motors and displays.',
        'Apply basic <strong>control</strong> (on-off and PID) to make a device behave as intended.',
        'Integrate mechanical, electronic and software parts into one working device, and document and present '
        'it.'],
        [
        'Design a printed circuit board.',
        'Work in a team with defined roles and a schedule.',
        'Use wireless connectivity (Bluetooth, Wi-Fi) or a single-board computer.'])
    + sec('Major Topics', [
        'The engineering design process and requirements.',
        'CAD and rapid prototyping (3D printing, laser cutting).',
        'Basic circuits, sensors, motors and drivers.',
        'Microcontroller programming.',
        'Introductory feedback control.',
        'System integration, testing and documentation.'],
        [
        'PCB design.',
        'Wireless and Internet-of-Things devices.',
        'Design for manufacture and cost.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul(
        'A microcontroller platform such as Arduino, ESP32 or Raspberry Pi Pico.',
        'CAD software such as Autodesk Fusion or SOLIDWORKS; a slicer for 3D printing.',
        'Breadboards, multimeter, oscilloscope and bench power supply.',
        'Circuit and PCB tools such as KiCad or Tinkercad Circuits.',
        '<em>Make:</em> magazine and its project books, and <em>Practical Electronics for Inventors</em>, '
        'Scherz and Monk (McGraw-Hill).')
    + '<h2>Career Pathways</h2>'
    + ul(
        '<strong>Mechatronics and product design engineer</strong> (SOC 17-2199.05, mechatronics engineers).',
        '<strong>Embedded systems engineer</strong> and <strong>electrical engineer</strong> (SOC 17-2071).',
        '<strong>Robotics and automation</strong> in manufacturing, medical devices and defence around Tampa Bay.',
        'Start-ups building hardware products, where one person often does CAD, electronics and code.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: the University of South Florida, at 3 credits.</strong> USF publishes no '
    'contact-hour figure, so the 45 hours shown are derived from Florida\'s convention of 15 per credit for a '
    'lecture course. A hands-on course of this kind often has more scheduled lab or studio time than that; '
    'check the schedule. The number entered the state course file in 2021.</p>'
    '<h3>Who it is for</h3>'
    '<p>USF lists no prerequisite, and the description reads as an introduction, so it may suit students '
    'early in the major as well as seniors. It is <strong>not</strong> USF\'s senior design sequence, which '
    'is EEL4906 ECE Design 1 and EEL4914 ECE Design 2. Ask the department how EEL4010 counts in your '
    'degree.</p>'
    '<h3>Costs and time</h3>'
    '<p>Project courses sometimes ask students to buy parts or a kit; ask early. Building and debugging take '
    'longer than planned: allow 8&ndash;10 hours a week, more before demonstrations.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI assistants are useful in maker work: they write first-draft microcontroller code, explain a data '
    'sheet and suggest wiring. They also invent pin numbers and library functions, ignore current limits, and '
    'produce code that compiles but never reads the sensor correctly. <strong>Check every connection against '
    'the data sheet before powering a circuit</strong>, test code one piece at a time, and follow your '
    'instructor\'s policy on AI use.</p>'
)

EEL4010 = {
    'title': 'MAKE Hands-On Engineering Design',
    'html_content': EEL4010_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4010_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, the University of South Florida, at 3 credits; no prerequisite listed.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [{
            'institution': 'USF', 'institution_name': 'University of South Florida',
            'title': 'MAKE Hands-On Engineering Design', 'credits': 3, 'contact_hours': None,
            'note': 'Design of mechatronic devices: CAD, electronic circuits, programming and control. No '
                    'prerequisite listed in the catalogue.'}],
    },
}

# --------------------------------------------------------------------------
# EEL4005 Measurements and Instrumentation -- FAMU, FIU, FSU, UNF
# --------------------------------------------------------------------------
EEL4005_PRE = ('FAMU-FSU College of Engineering: EEL3112 Advanced Circuits. FIU: EEL3110C Circuit Analysis and '
               'Lab and EEL2880 C Programming for Embedded Systems. UNF: not confirmed for this guide. All four '
               'carriers run it at 3 credits. Check your own institution\'s catalogue for grade requirements.')

EEL4005_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4005</strong> is an upper-division electrical engineering course in <strong>measurement '
    'and instrumentation</strong>, carried by <strong>four Florida public universities</strong> &mdash; FAMU '
    'and FSU (through their joint FAMU-FSU College of Engineering), Florida International University and the '
    'University of North Florida &mdash; all at 3 credits. The statewide title is <em>Introduction to '
    'Instrumentation</em>; FAMU-FSU and FIU call it <em>Measurements and Instrumentation for</em> (or <em>in</em>) '
    '<em>Electrical Engineering</em>.</p>'
    '<p>The two published descriptions agree on the core. FAMU-FSU: <em>"various measurement methods and '
    'instrumentation techniques used in electrical engineering practice and research."</em> FIU: '
    '<em>"various measurements, data acquisition and control using the software packages commonly used in '
    'the electrical engineering practice and research"</em> &mdash; so FIU leans further toward computer-based '
    'data acquisition. UNF\'s description could not be read for this guide.</p>'
    + sec('Learning Outcomes', [
        'Describe a <strong>measurement system</strong> (sensor, signal conditioning, conversion, display) and '
        'its static and dynamic characteristics: accuracy, precision, resolution, range, linearity, response '
        'time.',
        'Analyse <strong>measurement error and uncertainty</strong>, and combine uncertainties correctly.',
        'Select and use <strong>sensors and transducers</strong> for temperature, strain, force, pressure, '
        'position and light.',
        'Design <strong>signal conditioning</strong>: bridges, instrumentation amplifiers and filters.',
        'Explain <strong>sampling and analog-to-digital conversion</strong> (sampling rate, aliasing, '
        'quantisation) and build a <strong>data acquisition</strong> system in software.',
        'Use laboratory instruments correctly and reduce <strong>noise</strong> through grounding and '
        'shielding.'],
        [
        'Close a simple control loop from acquired data (emphasised at FIU).',
        'Calibrate an instrument and explain traceability to national standards.',
        'Apply statistics to repeated measurements.'])
    + sec('Major Topics', [
        'Measurement fundamentals, units and standards.',
        'Errors, uncertainty and statistics of measurement.',
        'Sensors and transducers.',
        'Bridges, amplifiers and filters for signal conditioning.',
        'Sampling, ADCs and DACs; data acquisition hardware and software.',
        'Oscilloscopes, meters and other bench instruments.',
        'Noise, grounding and shielding.'],
        [
        'Computer control of instruments (for example SCPI over USB or Ethernet).',
        'Industrial instrumentation and process control loops.',
        'Calibration and metrology.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul(
        '<em>Measurement and Instrumentation: Theory and Application</em>, Morris and Langari (Academic Press), '
        'and <em>Introduction to Engineering Experimentation</em>, Wheeler and Ganji (Pearson).',
        'LabVIEW or MATLAB (Data Acquisition and Instrument Control toolboxes), or Python with NumPy and '
        'PyVISA.',
        'Data-acquisition hardware (National Instruments DAQ, Analog Discovery or similar) and microcontroller '
        'boards.',
        'NIST\'s guidance on expressing measurement uncertainty, and the international <em>Guide to the '
        'Expression of Uncertainty in Measurement</em> (GUM).')
    + '<h2>Career Pathways</h2>'
    + ul(
        '<strong>Test engineer</strong> and <strong>instrumentation and controls (I&amp;C) engineer</strong> '
        '(SOC 17-2071, 17-2072) in power generation, manufacturing and aerospace.',
        '<strong>Electrical and electronic engineering technician</strong> roles in test and calibration '
        '(SOC 17-3023).',
        '<strong>Research engineer</strong> in university and government laboratories &mdash; in Tallahassee, '
        'the National High Magnetic Field Laboratory and FSU\'s Center for Advanced Power Systems.',
        'Florida\'s aerospace and defence test ranges and launch operations on the Space Coast, and utility '
        'plant instrumentation.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>All four public carriers run it at 3 credits:</strong> FAMU and FSU (one course, the joint '
    'FAMU-FSU College of Engineering), FIU and UNF. None publishes a contact-hour figure, so the 45 shown are '
    'derived from Florida\'s convention of 15 per credit for a lecture course. If your section includes a '
    'scheduled laboratory, the real hours are higher; check the schedule.</p>'
    '<table class="table table-sm"><thead><tr><th>Institution</th><th>Title</th><th>Credits</th>'
    '<th>Prerequisite</th></tr></thead><tbody>'
    '<tr><td>FAMU / FSU</td><td>Measurements and Instrumentation for Electrical Engineers</td><td>3</td>'
    '<td>EEL3112</td></tr>'
    '<tr><td>FIU</td><td>Measurements and Instrumentation in Electrical Engineering</td><td>3</td>'
    '<td>EEL3110C, EEL2880</td></tr>'
    '<tr><td>UNF</td><td>Introduction to Instrumentation</td><td>3</td><td>not confirmed</td></tr>'
    '</tbody></table>'
    '<h3>Transfer</h3>'
    '<p>Because all four use the same number, the course is equivalent across them under Florida\'s numbering '
    'system. FIU\'s version leans more toward software-based data acquisition and control, so a student moving '
    'into a FIU follow-on course from elsewhere should be comfortable with a programming language.</p>'
    '<h3>FE exam relevance</h3>'
    '<p>Measurement, instrumentation, sensors and signal conditioning appear on the NCEES <strong>FE '
    'Electrical and Computer</strong> exam.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI assistants can draft data-acquisition scripts, explain a data sheet and help with uncertainty '
    'calculations. They often get sampling and units wrong &mdash; ignoring aliasing, mixing peak and RMS '
    'values, or combining uncertainties by simple addition instead of in quadrature &mdash; and they will '
    'happily report a measurement to more digits than the instrument can resolve. <strong>A measurement is '
    'only as good as its stated uncertainty</strong>; check AI-assisted work against the instrument\'s '
    'specifications, and follow your instructor\'s policy on AI use.</p>'
)

EEL4005 = {
    'title': 'Measurements and Instrumentation for Electrical Engineers',
    'html_content': EEL4005_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4005_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'All four public carriers run it at 3 credits: FAMU and FSU (one course, the joint FAMU-FSU '
                   'College of Engineering), FIU and UNF.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [
            {'institution': 'FAMU', 'institution_name': 'Florida Agricultural and Mechanical University',
             'title': 'Measurements and Instrumentation for Electrical Engineers', 'credits': 3,
             'contact_hours': None, 'note': 'Joint FAMU-FSU College of Engineering. Prerequisite EEL3112.'},
            {'institution': 'FIU', 'institution_name': 'Florida International University',
             'title': 'Measurements and Instrumentation in Electrical Engineering', 'credits': 3,
             'contact_hours': None, 'note': 'Prerequisites EEL3110C, EEL2880. Emphasises data acquisition and '
                                            'control in software.'},
            {'institution': 'FSU', 'institution_name': 'Florida State University',
             'title': 'Measurements and Instrumentation for Electrical Engineers', 'credits': 3,
             'contact_hours': None, 'note': 'Joint FAMU-FSU College of Engineering. Prerequisite EEL3112.'},
            {'institution': 'UNF', 'institution_name': 'University of North Florida',
             'title': 'Introduction to Instrumentation', 'credits': 3, 'contact_hours': None,
             'note': 'Description and prerequisite not confirmed (catalogue not readable).'}],
    },
}

# --------------------------------------------------------------------------
# EEL4070 Introduction to Energy Storage -- FAMU, FSU
# --------------------------------------------------------------------------
EEL4070_PRE = ('FAMU-FSU College of Engineering: EEL3003 Introduction to Electrical Engineering (the course '
               'for non-electrical majors) OR EEL3111 Introductory Circuit Analysis. Because EEL3003 is '
               'accepted, mechanical and chemical engineering students can take it. General chemistry helps '
               'with the electrochemistry.')

EEL4070_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL4070 Introduction to Energy Storage</strong> is an upper-division elective of the '
    '<strong>FAMU-FSU College of Engineering</strong> in Tallahassee. Both FAMU and FSU list it in the state '
    'course file at 3 credits, but it is one course taught by the joint college. Its catalogue description: '
    '<em>"This course introduces students to energy storage technologies and devices with major focus on '
    'electrochemical storages including advanced rechargeable batteries, electrochemical capacitors, and fuel '
    'cells."</em></p>'
    '<p>Batteries now sit at the centre of electric vehicles, phones, grid storage paired with solar, and '
    'backup power, and this course explains how they work, how they fail and how they are used. Its '
    'prerequisite accepts the non-majors\' electrical course, so it is open to mechanical and chemical '
    'engineering students as well as electrical ones. The outcomes below follow the catalogue\'s three named '
    'technologies; the system-level topics vary by instructor, so check the syllabus.</p>'
    + sec('Learning Outcomes', [
        'Explain the <strong>electrochemistry</strong> of a cell: electrodes, electrolyte, redox reactions, '
        'open-circuit voltage and the Nernst equation.',
        'Compare battery chemistries &mdash; lead-acid, nickel-metal hydride, <strong>lithium-ion</strong> '
        '(and its cathode families) and emerging types &mdash; on energy, power, life, cost and safety.',
        'Use battery ratings and models: capacity, C-rate, energy and power density, efficiency, '
        '<strong>state of charge</strong> and <strong>state of health</strong>, and equivalent-circuit models.',
        'Explain how <strong>electrochemical capacitors</strong> (supercapacitors) store energy and when they '
        'suit an application better than a battery.',
        'Explain how <strong>fuel cells</strong> work, their types, and their efficiency and losses.',
        'Describe battery degradation and the causes and prevention of <strong>thermal runaway</strong>.'],
        [
        'Describe a battery management system: cell balancing, protection and estimation.',
        'Size storage for an application (an electric vehicle, a home with solar, a grid project).',
        'Compare non-electrochemical storage: pumped hydro, flywheels, compressed air, thermal.',
        'Discuss recycling, supply chains and cost trends.'])
    + sec('Major Topics', [
        'Why energy storage: applications and metrics.',
        'Electrochemistry fundamentals.',
        'Rechargeable battery chemistries; lithium-ion in depth.',
        'Cell characterisation, modelling, ageing and safety.',
        'Electrochemical capacitors.',
        'Fuel cells and hydrogen.'],
        [
        'Battery management systems and power electronics.',
        'Grid-scale storage and integration with solar and wind.',
        'Other storage technologies.',
        'Codes and standards for storage installations.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul(
        '<em>Linden\'s Handbook of Batteries</em> (McGraw-Hill) &mdash; the standard reference.',
        '<em>Battery Systems Engineering</em>, Rahn and Wang (Wiley), for modelling and management.',
        '<em>Fuel Cell Fundamentals</em>, O\'Hayre et al. (Wiley).',
        'MATLAB/Simulink (Simscape Battery) or Python (for example the open-source PyBaMM battery modelling '
        'package).',
        'Safety standards worth knowing by name: <strong>UL 9540</strong> and <strong>UL 9540A</strong> '
        '(energy storage systems and fire testing) and <strong>NFPA 855</strong> (installation of stationary '
        'energy storage systems).')
    + '<h2>Career Pathways</h2>'
    + ul(
        '<strong>Battery and energy storage engineer</strong> (often classed as electrical, chemical or '
        'materials engineer: SOC 17-2071, 17-2041, 17-2131).',
        '<strong>Electric-vehicle and power-electronics engineer</strong>.',
        '<strong>Utility and renewable-energy engineer</strong>: Florida Power &amp; Light has built large '
        'battery storage alongside its solar fleet, including the Manatee Energy Storage Center in Manatee '
        'County.',
        '<strong>Research</strong> in energy storage at the FAMU-FSU College of Engineering, FSU\'s Center for '
        'Advanced Power Systems and national laboratories, often through graduate study.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>Two carriers in the state file, FAMU and FSU, both at 3 credits &mdash; one course</strong>, '
    'taught by the joint FAMU-FSU College of Engineering. Neither publishes contact hours, so the 45 shown are '
    'derived from Florida\'s convention of 15 per credit for a lecture course. No other Florida public '
    'institution carries the number.</p>'
    '<h3>Prerequisites and who can take it</h3>'
    '<p>The prerequisite is <strong>EEL3003 or EEL3111</strong>. EEL3003 is the college\'s electrical course '
    'for non-electrical majors (not accepted toward the electrical or computer engineering degrees), so '
    'taking it opens this elective to mechanical, chemical and materials students. Ask your department '
    'whether EEL4070 counts as a technical elective in your major.</p>'
    '<h3>Safety</h3>'
    '<p>If the course includes laboratory work with lithium cells, follow the laboratory\'s handling rules '
    'exactly: a damaged or abused lithium-ion cell can vent, catch fire and re-ignite.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain electrochemistry and help write battery models and data-analysis scripts. They '
    'are weak on numbers that change fast &mdash; costs per kilowatt-hour, energy densities of particular '
    'cells, and the newest chemistries &mdash; and often quote out-of-date or invented figures. '
    '<strong>Take specifications from data sheets and current sources</strong>, check that energy and power '
    'calculations balance, and follow your instructor\'s policy on AI use.</p>'
)

EEL4070 = {
    'title': 'Introduction to Energy Storage',
    'html_content': EEL4070_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL4070_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'FAMU and FSU, both at 3 credits: one course taught by the joint FAMU-FSU College of '
                   'Engineering.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [
            {'institution': 'FAMU', 'institution_name': 'Florida Agricultural and Mechanical University',
             'title': 'Introduction to Energy Storage', 'credits': 3, 'contact_hours': None,
             'note': 'Joint FAMU-FSU College of Engineering. Prerequisite EEL3003 or EEL3111.'},
            {'institution': 'FSU', 'institution_name': 'Florida State University',
             'title': 'Introduction to Energy Storage', 'credits': 3, 'contact_hours': None,
             'note': 'Joint FAMU-FSU College of Engineering. Prerequisite EEL3003 or EEL3111.'}],
    },
}

ALL = (('CEN4020', CEN4020), ('EEL4030', EEL4030), ('EEL4062', EEL4062), ('EEL4021', EEL4021),
       ('EEL4010', EEL4010), ('EEL4005', EEL4005), ('EEL4070', EEL4070))

for cid, g in ALL:
    path = os.path.join(DRAFTS, '%s_guide.json' % cid)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(g, fh, ensure_ascii=False, indent=1)
    print('wrote', cid, len(g['html_content']), 'chars; prereq', len(g['prerequisites']))
