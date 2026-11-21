#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Batch 249 -- scheduled request check 2026-11-21 (third run of the day).

Requests in rank order after the three held items (EEL4448, EEL5025, EEL5009 -- REVIEW_QUEUE 130-132):
EEL1931, EEL2161, EEL2603C, EEL2880, EEL3000, EEL3003, EEL3004C, EEL3100, BCV0632C, EET2525C.

  Written    EEL2161 EEL2603C EEL2880 EEL3000 EEL3003 EEL3004C EEL3100 BCV0632C
  Declined   EEL1931 (UCF special topics, variable credit): a shell number
  Held       EET2525C (SCF only; catalog.scf.edu refuses automated requests, and the SCNS statewide title is
             a different course, Industrial Motor Control Lab)

Sources:
  USF        cloud.usf.edu/academic-programs/details/prefix/EEL/code/<n> (EEL2161, EEL3100); b247 EGN3374
  FAU        Coursedog cache fau_courses.json (EEL2161 "C for Engineers": C++ and MATLAB, 3 lecture hours)
  NWFSC      Coursedog cache nwfsc_courses.json (EEL2603C: 2 lecture + 2 lab hours, fall, prerequisite ETS 1542C)
  FIU        Coursedog cache fiu_courses.json (EEL2880; EEL3004 and EEL3004L for comparison)
  UF         catalog.ufl.edu ECE course page (EEL3000) and /search/?P=EEL%203003 (EEL3003)
  FAMU-FSU   scratchpad/b246_famufsu_list.txt (EEL3003, EEL3003L, EEL3135)
  UCF        Kuali 2026-27 catalogue (EEL3004C, EEL3123C)
  NFC        2026-27 College Catalog PDF (Electrician, programme 5065, CIP 46.0302, 1500 clock hours)
  Seminole   seminolestate.edu/catalog/courses/bcv0632c, bcv0631c (75 hours each)
  All        SCNS flat file: carriers, titles, credits, clock hours
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


def table(head, rows):
    h = ''.join('<th>%s</th>' % c for c in head)
    b = ''.join('<tr>' + ''.join('<td>%s</td>' % c for c in r) + '</tr>' for r in rows)
    return '<table class="table table-sm"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (h, b)


def off(code, name, title, credits, note, hours=None):
    return {'institution': code, 'institution_name': name, 'title': title, 'credits': credits,
            'contact_hours': hours, 'note': note}


DERIVED = ("Florida's convention of 15 contact hours per credit for a lecture course; no carrier "
           'publishes a term contact-hour figure for this number.')

UF = 'University of Florida'
USF = 'University of South Florida'
FAU = 'Florida Atlantic University'
FAMU = 'Florida Agricultural and Mechanical University'
FSU = 'Florida State University'
FIU = 'Florida International University'
UCF = 'University of Central Florida'
NWFSC = 'Northwest Florida State College'
NFC = 'North Florida College'
SSC = 'Seminole State College of Florida'

AI_CODE = (
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI assistants write C quickly and explain compiler errors well, and a beginner can learn from asking them '
    'why a line is wrong. They are also confidently wrong in exactly the places C punishes: off-by-one loops, '
    'buffers that are too small, pointers to memory that no longer exists, and integer overflow. Code that compiles '
    'and runs once is not code that is correct. <strong>Write the program yourself first, test it with inputs at '
    'the edges (zero, negative, the largest value), and use AI to explain, not to submit.</strong> Most engineering '
    'departments treat submitted AI-written code as an academic-integrity matter unless the instructor allows it; '
    'follow the syllabus.</p>')

AI_CIRCUITS = (
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain a theorem, check algebra and set up a simulation, and circuit simulators (LTspice, '
    'Multisim, PSpice) have long been part of this subject. Language models make characteristic circuit errors: '
    'they mix up passive sign conventions, drop the phase of a phasor, confuse peak and RMS values, and state an '
    'answer with no units. <strong>Check every answer three ways &mdash; a sign-convention check, a units check and '
    'a simulation &mdash; and learn to solve by hand, because exams and the FE exam are taken without the '
    'tool.</strong> Follow your instructor\'s policy on AI use.</p>')

# ---------------------------------------------------------------------------------------------
# EEL2161 Programming with C (USF) / C for Engineers (FAU)
# ---------------------------------------------------------------------------------------------
EEL2161_PRE = (
    'None listed by USF or FAU in the records read; check your department. Two different courses share this number: '
    'USF teaches C for electrical engineering students; FAU\'s "C for Engineers" teaches C++ and MATLAB. Neither '
    'is the same as COP2220 Programming in C, the number most Florida colleges use for a first C course.')

EEL2161_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL2161</strong> is a lower-division programming course taught inside electrical engineering '
    'departments. Two Florida public universities carry it, both at 3 credits, and the SCNS statewide title is the '
    'generic <em>Computer Methods &ndash; Lower Level</em>. ⚠ <strong>The two carriers do not teach the same '
    'language</strong>, so read which one you are in:</p>'
    + table(['', 'USF &mdash; <em>Programming with C</em>', 'FAU &mdash; <em>C for Engineers</em>'], [
        ['What the catalogue says', '"An introductory course to provide the fundamentals of computer language for '
         'electrical engineering students. Skills on syntax, functions, data, input and output, algorithm, and '
         'creating solutions for engineering problems using C."',
         '"Introduces the fundamental capabilities of C++ and MATLAB. Illustrates the numerical problem-solving '
         'process, testing and interpretation of results through a variety of engineering examples and '
         'applications."'],
        ['Language', '<strong>C</strong>', '<strong>C++ and MATLAB</strong>, despite the title'],
        ['Hours', '3 credits; USF publishes no weekly hours', '3 credits, 3 lecture hours a week']])
    + '<p>Both are a first programming course for engineers: problem solving, writing and testing small programs, '
    'and applying them to engineering calculations. The outcomes below are what the two share, with the '
    'language-specific parts marked.</p>'
    + sec('Learning Outcomes', [
        'Break an engineering problem into steps and write it as an <strong>algorithm</strong> before coding.',
        'Write, compile, run and debug programs using variables, data types, operators and expressions.',
        'Use <strong>selection</strong> (if/else, switch) and <strong>repetition</strong> (for, while) correctly.',
        'Write and call <strong>functions</strong> with parameters and return values.',
        'Store and process data in <strong>arrays</strong>, and read and write data from the keyboard and files.',
        'Test a program with chosen inputs, including edge cases, and judge whether its results are reasonable.'],
        ['(USF) Use C pointers, strings and structures, and explain how C stores data in memory.',
         '(FAU) Write C++ programs, and solve numerical problems in MATLAB with vectors, matrices and plots.'])
    + sec('Major Topics', [
        'The engineering problem-solving process; pseudocode and flowcharts.',
        'Program structure, compiling, syntax and run-time errors.',
        'Data types, arithmetic, operator precedence, type conversion.',
        'Conditionals and loops.', 'Functions and scope.', 'Arrays.', 'Input/output and files.',
        'Engineering applications: unit conversions, series, simple numerical methods.'],
        ['(USF) Pointers, strings, structures, memory.',
         '(FAU) C++ classes and streams; MATLAB scripts, vectors, matrices and plotting.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('A C or C++ compiler: gcc/clang, or an IDE such as Visual Studio Code, Code::Blocks or Visual Studio.',
         'MATLAB (FAU) &mdash; universities license it for students; GNU Octave runs most beginner scripts.',
         '<em>C Programming: A Modern Approach</em>, K. N. King (Norton), or <em>Engineering Problem Solving with '
         'C</em>, D. M. Etter (Pearson); for FAU\'s version, an engineering C++/MATLAB text such as Etter\'s '
         '<em>Engineering Problem Solving with MATLAB</em>.',
         'A debugger (gdb or the IDE\'s) &mdash; learning to step through code saves hours.')
    + '<h2>Career Pathways</h2>'
    + ul('A first course, so it supports every electrical and computer engineering career rather than one.',
         'C remains the language of <strong>embedded systems</strong> &mdash; the firmware in medical devices, '
         'vehicles, aircraft and consumer electronics (electrical engineers, SOC 17-2071; electronics engineers, '
         '17-2072; computer hardware engineers, 17-2061).',
         'MATLAB is standard in signal processing, controls and power analysis; Florida\'s aerospace and defence '
         'employers (L3Harris, Lockheed Martin, Northrop Grumman, Collins Aerospace) use both heavily.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>Both carriers run it at 3 credits</strong>: University of South Florida (<em>Programming with C</em>) '
    'and Florida Atlantic University (<em>C for Engineers</em>, 3 lecture hours a week). No term contact-hour figure '
    'is published; the 45 shown are derived from Florida\'s convention of 15 per credit.</p>'
    '<h3>Transfer and course-number notes</h3>'
    '<p>Most Florida colleges teach a first C course as <strong>COP2220</strong> <em>Programming in C</em> (Daytona '
    'State, FAU, Northwest Florida State, Pasco-Hernando, St. Johns River, St. Petersburg, Tallahassee State, UNF); '
    'UF and Florida Poly use <strong>COP2271</strong> <em>Computer Programming for Engineers</em>. SCNS equivalence '
    'does not cross numbers, so a college C course does not automatically satisfy EEL2161 &mdash; ask the receiving '
    'department, in writing, before you transfer. ⚠ And because FAU\'s EEL2161 is C++/MATLAB, a student moving '
    'between USF and FAU should not assume the same number means the same language. Bring the syllabus.</p>'
    '<h3>Workload</h3>'
    '<p>Programming is learned by writing programs. Expect 6&ndash;9 hours a week outside class, most of it at the '
    'keyboard, and start each assignment early: debugging takes longer than writing.</p>'
    + AI_CODE)

EEL2161 = {
    'title': 'Programming with C (USF) / C for Engineers (FAU)',
    'html_content': EEL2161_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL2161_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'Two public carriers, both at 3 credits. USF teaches C; FAU teaches C++ and MATLAB.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED + ' FAU records 3 lecture hours a week.',
        'offerings': [
            off('USF', USF, 'Programming with C', 3, 'C for electrical engineering students.'),
            off('FAU', FAU, 'C for Engineers', 3, 'Teaches C++ and MATLAB; 3 lecture hours a week.')],
    },
}

# ---------------------------------------------------------------------------------------------
# EEL2603C Robotics-Mechanics and Controls (NWFSC)
# ---------------------------------------------------------------------------------------------
EEL2603C_PRE = (
    'Northwest Florida State College lists ETS 1542C Introduction to Programmable Logic Controllers. Offered fall '
    'only. A college credit course in NWFSC\'s engineering technology area; 2 lecture and 2 laboratory hours a week.')

EEL2603C_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL2603C</strong> <em>Robotics-Mechanics and Controls</em> is a 3-credit lecture-and-laboratory '
    'course carried by one Florida public institution, <strong>Northwest Florida State College</strong> (Niceville), '
    'in its engineering technology area (CIP 15.0303, electrical and electronic engineering technology). NWFSC '
    'describes it in one sentence: <em>"This course introduces the student to robotics. Instructional topics will '
    'include robot classifications, applications, Input/Output (I/O) and sensor interfacing."</em></p>'
    '<p>It follows NWFSC\'s introductory PLC course, so the robotics here is the <strong>industrial</strong> kind: '
    'robot arms and work cells controlled alongside PLCs, as in manufacturing and automation. NWFSC publishes no '
    'outline beyond the sentence above, so the outcomes below follow its four named topics and the usual content '
    'of an industrial robotics course at this level; check the syllabus.</p>'
    + sec('Learning Outcomes', [
        'Classify robots by <strong>configuration</strong> (articulated, SCARA, Cartesian/gantry, cylindrical, delta, '
        'collaborative) and explain what each suits.',
        'Describe industrial <strong>applications</strong> &mdash; pick-and-place, palletising, welding, painting, '
        'machine tending, inspection &mdash; and the safety measures each needs.',
        'Explain the robot\'s parts: manipulator, joints and axes, end-of-arm tooling, drives, controller and teach '
        'pendant.',
        'Wire and configure <strong>digital and analogue I/O</strong> between a robot controller, a PLC and field '
        'devices.',
        'Interface <strong>sensors</strong> (proximity, photoelectric, limit switches, encoders, vision) and use '
        'their signals to start, stop or redirect a robot program.',
        'Write and run a simple robot program using points, frames and I/O commands, and work safely in a robot '
        'cell.'],
        ['Explain how a PLC and a robot hand off a task (handshaking) in a work cell.',
         'Describe industry robot-programming certifications offered by robot makers.'])
    + sec('Major Topics', [
        'Robot classifications and work envelopes.', 'Industrial applications.',
        'Robot components, axes, coordinate frames and end effectors.',
        'Robot controller I/O; interfacing with PLCs.', 'Sensors and sensor interfacing.',
        'Basic robot programming and teach pendant operation.', 'Robot safety (guarding, interlocks, ANSI/RIA R15.06).'],
        ['Machine vision.', 'Collaborative robots.', 'Simulation of a robot cell.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('An educational industrial robot or arm with a teach pendant (makers such as FANUC, ABB, Yaskawa or '
         'Universal Robots supply training cells) &mdash; NWFSC sets the equipment.',
         'A PLC trainer, as used in ETS 1542C.',
         'ANSI/RIA R15.06 (ISO 10218) industrial robot safety standard.',
         '<em>Industrial Robotics Fundamentals</em>, Fuller (Goodheart-Willcox), or a similar technician-level text.')
    + '<h2>Career Pathways</h2>'
    + ul('<strong>Robotics and automation technician</strong> (electro-mechanical and mechatronics technologists '
         'and technicians, SOC 17-3024); <strong>industrial machinery mechanic</strong> (49-9041).',
         '<strong>Electrical and electronic engineering technician</strong> (17-3023) in manufacturing.',
         'In Northwest Florida: aerospace and defence manufacturing around Eglin AFB and Hurlburt Field, and '
         'manufacturers in the Okaloosa-Walton area.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: Northwest Florida State College, at 3 credits</strong>, fall term only. NWFSC '
    'records <strong>2 lecture and 2 laboratory hours a week (4 contact hours)</strong>; over a 15-week term that '
    'is about 60, the figure shown.</p>'
    '<h3>Prerequisite</h3>'
    '<p>NWFSC\'s record names <strong>ETS 1542C</strong> <em>Introduction to Programmable Logic Controllers</em> '
    '(also fall only at NWFSC), so plan the two in consecutive years or ask whether they may be taken together.</p>'
    '<h3>A shared statewide title</h3>'
    '<p>The state file also gives the title <em>Robotics-Mechanics and Controls</em> to FIU\'s <strong>EEL1603</strong> '
    '<em>Introduction to Robotic Systems</em>, a first-year course for engineering majors. They are different '
    'numbers and SCNS equivalence does not cross numbers. EEL2603C is a technology course; whether it counts toward '
    'a university engineering degree is the receiving department\'s decision.</p>'
    '<h3>Safety</h3>'
    '<p>An industrial robot can move fast and without warning. Never enter a robot\'s working space while it is '
    'powered unless the cell\'s safety system allows it, and follow the laboratory\'s lockout rules.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain robot types and help draft a program or a ladder rung, but they do not know your '
    'robot\'s controller, its I/O map or its safety configuration, and robot makers\' languages differ. '
    '<strong>Check every generated program in simulation or at reduced speed, with the pendant\'s enabling switch '
    'in hand.</strong> Follow your instructor\'s policy on AI use.</p>')

EEL2603C = {
    'title': 'Robotics-Mechanics and Controls',
    'html_content': EEL2603C_HTML,
    'credits': 3,
    'contact_hours': 60,
    'prerequisites': EEL2603C_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, Northwest Florida State College, at 3 credits, fall only.',
        'hours_source': 'derived',
        'derived_contact_hours': 60,
        'derivation': 'NWFSC records 2 lecture and 2 laboratory hours a week; 4 x 15 weeks = 60.',
        'offerings': [off('NWFSC', NWFSC, 'Robotics-Mechanics and Controls', 3,
                          'Fall only. Prerequisite ETS 1542C. 2 lecture + 2 lab hours a week.')],
    },
}

# ---------------------------------------------------------------------------------------------
# EEL2880 C Programming for Embedded Systems (FIU)
# ---------------------------------------------------------------------------------------------
EEL2880_PRE = (
    'FIU\'s record lists no prerequisite. Calculus I and some exposure to programming help. Check FIU\'s ECE '
    'curriculum for where it sits in your degree. Offered fall, spring and summer.')

EEL2880_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL2880</strong> <em>C Programming for Embedded Systems</em> is a 3-credit lower-division course '
    'carried by one Florida public institution, <strong>Florida International University</strong>, in its '
    'Department of Electrical and Computer Engineering, every term. FIU describes it as: <em>"Engineering problem '
    'solving process, overview of a generalized computing system, software development, real-life engineering '
    'applications, computational implications."</em></p>'
    '<p>That description could fit any first programming course; the title is what says the language is '
    '<strong>C</strong> and the setting is <strong>embedded systems</strong> &mdash; small computers built into '
    'devices. The outcomes below combine the two. FIU publishes no topic list, so treat the optional items as '
    'likely rather than certain, and check the syllabus.</p>'
    + sec('Learning Outcomes', [
        'Apply the engineering problem-solving process: define the problem, design an algorithm, code, test.',
        'Describe a generalized computing system &mdash; processor, memory, input/output, buses &mdash; and how a '
        'program runs on it.',
        'Write, compile and debug C programs using data types, operators, control flow, functions and arrays.',
        'Explain how C represents data in memory (bits, bytes, integer sizes, pointers) and why that matters on '
        'a small device.',
        'Follow a software development process: requirements, modular design, testing and documentation.',
        'Solve real engineering problems in C and reason about their computational cost.'],
        ['Use bitwise operators to set, clear and test individual bits, as embedded code does with hardware '
         'registers.',
         'Write and run C on a microcontroller board.',
         'Use pointers and structures.'])
    + sec('Major Topics', [
        'Engineering problem solving and algorithm design.', 'Computer organisation overview.',
        'C syntax, types, operators, control structures.', 'Functions and modular programs.',
        'Arrays and strings.', 'Data representation and memory.', 'Software development and testing.',
        'Engineering applications and computational efficiency.'],
        ['Bit manipulation and fixed-width integer types.', 'Pointers and structures.',
         'Introduction to microcontroller programming.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('A C compiler and IDE (gcc/clang with Visual Studio Code, or the IDE FIU assigns).',
         'A microcontroller development board, if the section uses one (Arduino, MSP430, STM32 or similar).',
         '<em>C Programming: A Modern Approach</em>, K. N. King; for the embedded side, <em>Making Embedded Systems'
         '</em>, Elecia White (O\'Reilly).',
         'A debugger &mdash; gdb or the IDE\'s.')
    + '<h2>Career Pathways</h2>'
    + ul('<strong>Embedded software and firmware engineer</strong> (computer hardware engineers, SOC 17-2061; '
         'software developers, 15-1252; electrical and electronics engineers, 17-2071/17-2072).',
         'South Florida employers in medical devices, telecommunications, aviation and defence electronics hire '
         'embedded engineers; C is still the main language of that work.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: Florida International University, at 3 credits</strong>, fall, spring and summer. '
    'FIU records it as a lecture course and publishes no contact hours; the 45 shown are derived from Florida\'s '
    'convention of 15 per credit.</p>'
    '<h3>A statewide title that does not match</h3>'
    '<p>The state file gives this number the statewide title <em>Applied Software Engineering Techniques</em>; FIU\'s '
    'own title and description are what it teaches. The number is FIU\'s alone, so on transfer the receiving '
    'department decides what it counts as &mdash; usually against its own first C course (<strong>COP2220</strong> '
    'at many Florida colleges, <strong>EEL2161</strong> at USF). Bring the syllabus.</p>'
    '<h3>Workload</h3>'
    '<p>Expect 6&ndash;9 hours a week outside class writing and debugging programs.</p>'
    + AI_CODE)

EEL2880 = {
    'title': 'C Programming for Embedded Systems',
    'html_content': EEL2880_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL2880_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, Florida International University, at 3 credits, every term.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [off('FIU', FIU, 'C Programming for Embedded Systems', 3,
                          'Fall, spring and summer. No prerequisite in FIU\'s record.')],
    },
}

# ---------------------------------------------------------------------------------------------
# EEL3000 Introduction to Electrical Engineering (UF, 2 credits)
# ---------------------------------------------------------------------------------------------
EEL3000_PRE = (
    'UF: MAC 2311 with a minimum grade of C (or an appropriate AP/IB score), and Electrical Engineering majors '
    'only. Not the same course as EEL 3003, which UF and FAMU-FSU teach to non-majors and FAMU-FSU also titles '
    '"Introduction to Electrical Engineering".')

EEL3000_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL3000</strong> <em>Introduction to Electrical Engineering</em> is a <strong>2-credit</strong> course '
    'carried by one Florida public institution, the <strong>University of Florida</strong>, for its electrical '
    'engineering majors. UF\'s description: <em>"Introduces the profession of electrical engineering. Presents '
    'career development and enhancement, professional codes of conduct, ethics, entrepreneurship, intellectual '
    'property, professional societies. Projects provide hands-on experience with soldering, MATLAB programming, and '
    'microcontrollers."</em></p>'
    '<p>It is an introduction to the <strong>profession</strong>, not to circuit theory: half of it is about being '
    'an engineer (ethics, careers, intellectual property, professional societies) and half is hands-on projects '
    'that build the practical skills later courses assume.</p>'
    + sec('Learning Outcomes', [
        'Describe the fields of electrical engineering and the careers and further study they lead to.',
        'Apply a <strong>professional code of conduct</strong> (IEEE, NSPE) to ethical cases an engineer meets.',
        'Explain the basics of <strong>intellectual property</strong> (patents, copyright, trade secrets) and of '
        'entrepreneurship in engineering.',
        'Describe the professional societies and the route to licensure (FE exam, PE).',
        'Solder components to a board neatly and safely, and inspect the joints.',
        'Write short <strong>MATLAB</strong> programs to compute and plot engineering quantities.',
        'Program a <strong>microcontroller</strong> to read an input and drive an output in a small project.'],
        ['Plan a career and the experiences (internships, research, co-op) that support it.',
         'Work in a team on a project and present the result.'])
    + sec('Major Topics', [
        'The electrical engineering profession and its fields.', 'Career development and enhancement.',
        'Professional codes of conduct and engineering ethics.', 'Entrepreneurship and intellectual property.',
        'Professional societies (IEEE and others) and licensure.', 'Soldering and electronics assembly.',
        'MATLAB programming.', 'Microcontroller projects.'],
        ['Laboratory safety and test equipment.', 'Technical communication.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('MATLAB (UF licenses it for students).',
         'A microcontroller board and kit as UF assigns, a soldering station, multimeter and breadboard.',
         'IEEE Code of Ethics and the NSPE Code of Ethics for Engineers.',
         'UF Career Connections Center and the IEEE student branch.')
    + '<h2>Career Pathways</h2>'
    + ul('Supports every electrical engineering career (SOC 17-2071, 17-2072) rather than one: power, electronics, '
         'communications, controls, computing, devices.',
         'The FE exam is the first step to PE licensure in Florida (ch. 471, F.S.); the course explains the route.',
         'Florida employers named on UF\'s career pages include utilities, aerospace and defence firms, and '
         'semiconductor and electronics companies.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: University of Florida, at 2 credits.</strong> UF publishes no contact hours; the '
    '30 shown are derived from Florida\'s convention of 15 per credit. Expect some of the time to be project '
    'work.</p>'
    '<h3>Three courses called "Introduction to Electrical Engineering"</h3>'
    + table(['Number', 'Who', 'What it is'], [
        ['<strong>EEL3000</strong> (this course)', 'UF, 2 cr', 'the profession, for EE majors'],
        ['EEL3003', 'FAMU-FSU (titled <em>Introduction to Electrical Engineering</em>); UF (<em>Elements of '
         'Electrical Engineering</em>)', 'circuits and machines for <strong>non-majors</strong>, 3 cr'],
        ['EEL1603', 'FIU (statewide title differs)', 'a first-year robotics course for ECE majors']])
    + '<p>Same words, different courses. A transcript showing "Introduction to Electrical Engineering" does not say '
    'which; the number does.</p>'
    '<h3>Transfer</h3>'
    '<p>Few other institutions have a matching course, so a transfer student entering UF\'s EE programme may be '
    'asked to take it. Ask the department early.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>The ethics half of this course is where AI raises new questions: who is responsible for an AI-assisted '
    'design, when its use must be disclosed, and how intellectual property applies to generated code. In the '
    'MATLAB and microcontroller projects AI can help with syntax, but check every result and follow the '
    'instructor\'s policy.</p>')

EEL3000 = {
    'title': 'Introduction to Electrical Engineering (the profession, UF)',
    'html_content': EEL3000_HTML,
    'credits': 2,
    'contact_hours': 30,
    'prerequisites': EEL3000_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, University of Florida, at 2 credits; EE majors only.',
        'hours_source': 'derived',
        'derived_contact_hours': 30,
        'derivation': DERIVED,
        'offerings': [off('UF', UF, 'Introduction to Electrical Engineering', 2,
                          'MAC 2311 (C) and EE majors only. Soldering, MATLAB and microcontroller projects.')],
    },
}

# ---------------------------------------------------------------------------------------------
# EEL3003 Elements / Introduction to Electrical Engineering (FAMU, FSU, UF) -- non-majors
# ---------------------------------------------------------------------------------------------
EEL3003_PRE = (
    'FAMU-FSU: MAC 2312 and PHY 2049C, each C- or better; the 1-credit lab EEL 3003L is a corequisite with the first '
    'enrolment. UF: MAC 2313 and PHY 2049. For students NOT majoring in electrical engineering: FAMU-FSU says it is '
    'not accepted for credit toward the BSEE or BSCpE.')

EEL3003_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL3003</strong> is the electrical engineering course for <strong>engineers in other majors</strong> '
    '&mdash; mechanical, industrial, biomedical, chemical and others. Three Florida public universities carry it, '
    'all at 3 credits: the <strong>University of Florida</strong> as <em>Elements of Electrical Engineering</em> (the '
    'statewide title), and <strong>Florida A&amp;M</strong> and <strong>Florida State</strong>, which share the joint '
    'FAMU-FSU College of Engineering, as <em>Introduction to Electrical Engineering</em>.</p>'
    + table(['', 'UF', 'FAMU-FSU'], [
        ['Description', '"Introduces the theory and practice of electrical engineering for those not majoring in '
         'electrical engineering. Discusses circuits, machines, electronics and systems."',
         '"An introduction to electrical engineering concepts for non-electrical engineering majors. The course '
         'focuses on circuit theory for interfacing sensors and actuators. Operational Amplifiers are included."'],
        ['Emphasis', 'a survey: circuits, machines, electronics, systems',
         'circuits for <strong>sensors and actuators</strong>, op-amps'],
        ['Laboratory', 'none listed', '<strong>EEL 3003L</strong> (1 cr), taken with the first enrolment'],
        ['Prerequisites', 'MAC 2313 and PHY 2049', 'MAC 2312 and PHY 2049C, C- or better']])
    + '<p>Both cover the core of circuit analysis compressed into one term, then apply it; UF ranges more widely '
    '(machines, electronics), FAMU-FSU goes deeper into the instrumentation a mechanical or industrial engineer '
    'wires up.</p>'
    + sec('Learning Outcomes', [
        'Apply Ohm\'s law, Kirchhoff\'s laws and the passive sign convention to DC circuits.',
        'Analyse circuits with node and mesh methods and with Thevenin and Norton equivalents.',
        'Describe capacitors and inductors and the transient response of first-order circuits.',
        'Analyse AC circuits with <strong>phasors</strong> and impedance, and calculate real, reactive and apparent '
        'power.',
        'Analyse and design simple <strong>operational-amplifier</strong> circuits (amplifiers, buffers, filters).',
        'Connect sensors and actuators to measurement and control circuits.'],
        ['(UF) Explain transformers, DC and AC motors and generators.',
         '(UF) Describe diodes and transistors and basic electronic and digital systems.',
         '(FAMU-FSU lab) Use multimeters, power supplies, function generators and oscilloscopes to build and '
         'measure circuits.',
         'Explain three-phase power and electrical safety.'])
    + sec('Major Topics', [
        'Circuit variables and elements; sign conventions.', 'DC analysis: nodal, mesh, superposition, Thevenin/Norton.',
        'Capacitance, inductance, first-order transients.', 'Sinusoidal steady state, phasors, impedance, AC power.',
        'Operational amplifiers.', 'Sensors, signal conditioning and actuators.'],
        ['Transformers and electric machines (UF).', 'Semiconductor devices and digital logic (UF).',
         'Three-phase systems.', 'Electrical safety and grounding.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('<em>Electrical Engineering: Principles and Applications</em>, A. R. Hambley (Pearson) &mdash; the standard '
         'text for this non-majors course; or Rizzoni, <em>Principles and Applications of Electrical Engineering</em> '
         '(McGraw-Hill).',
         'Circuit simulation: LTspice, Multisim or PSpice.',
         'Laboratory instruments (FAMU-FSU\'s EEL 3003L): DMM, power supply, function generator, oscilloscope.',
         'NCEES <em>FE Reference Handbook</em> &mdash; the electricity and magnetism section.')
    + '<h2>Career Pathways</h2>'
    + ul('It serves engineers in other fields who will work with electrical systems: <strong>mechanical</strong> '
         '(SOC 17-2141), <strong>industrial</strong> (17-2112), <strong>biomedical</strong> (17-2031) and '
         '<strong>chemical</strong> (17-2041) engineers who specify motors, sensors, instruments and controls.',
         '<strong>FE exam</strong>: the FE Mechanical, Industrial and Other Disciplines exams include electricity '
         'and magnetism, which this course covers.',
         'Florida manufacturing, aerospace and utilities all need non-electrical engineers who can read a circuit.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    + table(['Institution', 'Title', 'Credits', 'Contact hours'], [
        ['University of Florida', 'Elements of Electrical Engineering', '3', 'not published'],
        ['Florida A&amp;M University', 'Introduction to Electrical Engineering', '3',
         'not published; plus EEL 3003L (1 cr)'],
        ['Florida State University', 'Introduction to Electrical Engineering', '3',
         'not published; plus EEL 3003L (1 cr)']])
    + '<p><strong>All three carry it at 3 credits.</strong> No carrier publishes contact hours; the 45 shown are '
    'derived from Florida\'s convention of 15 per credit. At FAMU-FSU the corequisite laboratory makes the package 4 '
    'credits &mdash; register for both.</p>'
    '<h3>Which majors take it</h3>'
    '<p>UF\'s catalogue names EEL 3003 among required courses in its <strong>Biomedical Engineering</strong> and '
    '<strong>Industrial and Systems Engineering</strong> programmes (minimum grade C in ISE). Check your own '
    'programme\'s list.</p>'
    '<h3>Not for EE majors &mdash; with one oddity</h3>'
    '<p>FAMU-FSU\'s bulletin says EEL 3003 is "not accepted for credit toward BSEE and BSCpE"; electrical majors take '
    'the <strong>EEL3111/EEL3112</strong> circuits sequence instead (UF: EEL3111C). ⚠ Yet the same bulletin lists '
    'EEL 3003 as an additional prerequisite of <strong>EEL 3135</strong> <em>Signal and Linear System Analysis</em> for '
    'Computer Engineering majors. If you are a FAMU-FSU computer engineering student, ask the department in writing '
    'which applies to you before you register.</p>'
    '<h3>Same title, different course</h3>'
    '<p>UF\'s <strong>EEL3000</strong> is also called <em>Introduction to Electrical Engineering</em>, but it is a '
    '2-credit introduction to the EE profession for majors. Go by the number.</p>'
    '<h3>Workload</h3>'
    '<p>It compresses two terms of circuit theory into one. Expect 8&ndash;10 hours a week outside class, mostly '
    'problem sets.</p>'
    + AI_CIRCUITS)

EEL3003 = {
    'title': 'Elements of Electrical Engineering (for non-majors)',
    'html_content': EEL3003_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL3003_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'Three public carriers, all at 3 credits: UF, FAMU and FSU (joint college). FAMU-FSU adds a '
                   '1-credit corequisite lab, EEL 3003L.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [
            off('UF', UF, 'Elements of Electrical Engineering', 3, 'Prerequisite MAC 2313 and PHY 2049.'),
            off('FAMU', FAMU, 'Introduction to Electrical Engineering', 3,
                'Joint FAMU-FSU college. MAC 2312 and PHY 2049C (C-); corequisite EEL 3003L.'),
            off('FSU', FSU, 'Introduction to Electrical Engineering', 3,
                'Joint FAMU-FSU college. MAC 2312 and PHY 2049C (C-); corequisite EEL 3003L.')],
    },
}

# ---------------------------------------------------------------------------------------------
# EEL3004C Linear Circuits I (UCF)
# ---------------------------------------------------------------------------------------------
EEL3004C_PRE = (
    'UCF, each with a minimum grade of C: MAC 2311C, MAC 2312 and MAC 2313; PHY 2048C (or PHY 2048 and 2048L); PHY '
    '2049C (or PHY 2049 and 2049L); CHS 1440C or CHM 2045C. Open to Electrical Engineering, Computer Engineering and '
    'Photonic Science and Engineering students only. An Honors section exists under the same number.')

EEL3004C_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL3004C</strong> <em>Linear Circuits I</em> is the first circuit analysis course for electrical, '
    'computer and photonic science and engineering majors at the <strong>University of Central Florida</strong>, its '
    'only Florida public carrier, at 3 credits. UCF\'s description: <em>"Analysis of linear circuits, AC analysis, '
    'power calculations, first order RL, RC circuits, three phase circuits. Includes recitation and exploration '
    'within electrical and computer engineering."</em> UCF records <strong>2 hours a week of laboratory/studio '
    'work</strong> beside the lectures &mdash; the recitation the description mentions. It leads to '
    '<strong>EEL3123C</strong> <em>Linear Circuits II</em> (second-order circuits, Laplace transforms, frequency '
    'response, Fourier series, two-port networks).</p>'
    + sec('Learning Outcomes', [
        'Define voltage, current, power and energy, and apply the <strong>passive sign convention</strong>.',
        'Analyse resistive circuits with Ohm\'s and Kirchhoff\'s laws, <strong>nodal and mesh analysis</strong>, '
        'superposition, source transformation, and Thevenin and Norton equivalents.',
        'Analyse ideal <strong>operational-amplifier</strong> circuits.',
        'Find the natural and step response of <strong>first-order RL and RC</strong> circuits.',
        'Analyse circuits in sinusoidal steady state with <strong>phasors</strong> and impedance.',
        'Calculate average, reactive and complex <strong>power</strong>, power factor and maximum power transfer.',
        'Analyse balanced <strong>three-phase</strong> circuits.'],
        ['Use a circuit simulator to check hand analysis.',
         'Explore the fields of electrical and computer engineering in the recitation.'])
    + sec('Major Topics', [
        'Circuit variables, elements and sign conventions.', 'Kirchhoff\'s laws; series/parallel reduction.',
        'Nodal and mesh analysis.', 'Network theorems: superposition, Thevenin, Norton, maximum power transfer.',
        'Operational amplifiers.', 'Capacitors, inductors, first-order transients.',
        'Sinusoids, phasors, impedance, AC steady-state analysis.', 'AC power and power factor.',
        'Three-phase circuits.'],
        ['Magnetically coupled circuits and transformers.', 'SPICE simulation.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('<em>Electric Circuits</em>, Nilsson and Riedel (Pearson), or <em>Fundamentals of Electric Circuits</em>, '
         'Alexander and Sadiku (McGraw-Hill) &mdash; the two standard texts.',
         'LTspice, Multisim or PSpice for simulation.',
         'NCEES <em>FE Reference Handbook</em> (circuit analysis section).')
    + '<h2>Career Pathways</h2>'
    + ul('The foundation of every electrical and computer engineering career (electrical engineers, SOC 17-2071; '
         'electronics, 17-2072; computer hardware, 17-2061).',
         '<strong>FE Electrical and Computer exam</strong>: circuit analysis is one of its largest sections.',
         'Central Florida employers &mdash; Lockheed Martin, L3Harris, Siemens Energy, Duke Energy, the simulation '
         'and photonics industries around Orlando &mdash; recruit heavily from UCF\'s ECE programme.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: University of Central Florida, at 3 credits</strong>, with an Honors section '
    '(<em>Honors Linear Circuits I</em>) under the same number. UCF records 2 laboratory/studio hours a week and '
    'publishes no term total; the 60 shown follow Florida\'s convention for a 3-credit <code>C</code> course.</p>'
    '<h3>The first circuits course runs under many numbers</h3>'
    + table(['Number', 'Carriers'], [
        ['<strong>EEL3004C</strong> Linear Circuits I', 'UCF'],
        ['EEL3111 Circuit Analysis I', 'FAMU, FAU, Florida Poly, FSU, UNF, UWF'],
        ['EEL3111C Circuits I (4 cr)', 'UF'],
        ['EGN3373 Electrical Systems I', 'USF (and UCF, for non-EE majors)']])
    + '<p>SCNS equivalence does not cross numbers. The subject is the same, but a transfer student should send the '
    'syllabus and ask the receiving department in writing how it counts; UCF\'s version also covers three-phase '
    'circuits, which some first courses leave to the second.</p>'
    '<h3>Not the same as EEL3004</h3>'
    '<p>The bare number <strong>EEL3004</strong> (FIU, <em>Circuit Analysis for Mechanical Engineers</em>, with lab '
    'EEL3004L) shares the statewide title <em>Network Analysis and Electrical Machines</em> but is a course for '
    '<strong>non-EE majors</strong>. UCF\'s EEL3004C is the majors\' course. Do not treat them as substitutes.</p>'
    '<h3>Restricted enrolment and workload</h3>'
    '<p>Only EE, CpE and Photonic Science and Engineering students may enrol, and the prerequisite list runs through '
    'Calculus III and both physics courses, so plan it for the junior year. Expect 8&ndash;12 hours a week outside '
    'class; this course decides how easy every later EE course will be.</p>'
    + AI_CIRCUITS)

EEL3004C = {
    'title': 'Linear Circuits I',
    'html_content': EEL3004C_HTML,
    'credits': 3,
    'contact_hours': 60,
    'prerequisites': EEL3004C_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, UCF, at 3 credits (with an Honors section under the same number).',
        'hours_source': 'derived',
        'derived_contact_hours': 60,
        'derivation': "Florida's convention of 60 contact hours for a 3-credit integrated (C) course; UCF records "
                      '2 laboratory/studio hours a week and publishes no term total.',
        'offerings': [off('UCF', UCF, 'Linear Circuits I', 3,
                          'EE, CpE and Photonic Science and Engineering majors only. Honors section exists.')],
    },
}

# ---------------------------------------------------------------------------------------------
# EEL3100 Network Analysis and Design (USF)
# ---------------------------------------------------------------------------------------------
EEL3100_PRE = (
    'USF: EGN 3420 Engineering Analysis (minimum grade C) and EGN 3374 Introduction to Electrical Systems II '
    '(minimum grade B, not C). EGN 3374 itself follows EGN 3373 and needs MAP 2302 (differential equations).')

EEL3100_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EEL3100</strong> <em>Network Analysis and Design</em> is the <strong>third course in USF\'s circuit '
    'sequence</strong> for electrical engineering, carried in Florida only by the <strong>University of South '
    'Florida</strong>, at 3 credits. USF\'s description: <em>"A third course in linear circuit analysis and design. '
    'Transient and steady-state responses of passive RLC networks to various functions."</em></p>'
    '<p>At USF the sequence is <strong>EGN3373</strong> <em>Electrical Systems I</em> &rarr; <strong>EGN3374</strong> '
    '<em>Introduction to Electrical Systems II</em> (AC/DC steady state, transients, power) &rarr; <strong>EEL3100'
    '</strong>. Having done the basics twice, this course turns to the systematic, transform-based treatment of '
    'networks: second-order and higher RLC circuits, responses to step, impulse, ramp and sinusoidal inputs, and '
    'the design of simple networks and filters.</p>'
    '<p>USF publishes no topic list beyond its description; the outcomes below are the usual content of a third '
    'circuits course built on that description. Check the syllabus.</p>'
    + sec('Learning Outcomes', [
        'Find the complete (natural plus forced) <strong>transient response</strong> of second-order RLC circuits, '
        'and classify it as over-, critically or under-damped.',
        'Use the <strong>Laplace transform</strong> to analyse circuits with initial conditions and with step, '
        'impulse, ramp and exponential inputs.',
        'Derive and use <strong>transfer functions</strong>; locate poles and zeros and relate them to the response.',
        'Find <strong>frequency response</strong>, draw Bode plots, and design simple passive and active filters.',
        'Analyse <strong>two-port networks</strong> with z, y, h and transmission parameters.',
        'Check analysis and designs by simulation.'],
        ['Use Fourier series to find the steady-state response to periodic non-sinusoidal inputs.',
         'Use convolution and the impulse response.', 'Analyse magnetically coupled circuits.'])
    + sec('Major Topics', [
        'Second-order RLC circuits: natural and step response.', 'Laplace transform methods in circuit analysis.',
        'Transfer functions, poles and zeros, stability.', 'Impulse response and convolution.',
        'Frequency response, resonance and Bode plots.', 'Passive and active filters.', 'Two-port networks.'],
        ['Fourier series.', 'Mutual inductance and transformers.', 'Network synthesis basics.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('<em>Electric Circuits</em>, Nilsson and Riedel, or <em>Fundamentals of Electric Circuits</em>, Alexander '
         'and Sadiku &mdash; the later chapters (Laplace, frequency response, two-ports).',
         'MATLAB for transfer functions and Bode plots; LTspice or Multisim for transient and AC simulation.',
         'NCEES <em>FE Reference Handbook</em>.')
    + '<h2>Career Pathways</h2>'
    + ul('Underpins signal processing, controls, communications and analog electronics (electrical engineers, '
         'SOC 17-2071; electronics engineers, 17-2072).',
         '<strong>FE Electrical and Computer exam</strong>: transient analysis, Laplace methods, frequency response '
         'and two-ports all appear.',
         'Tampa Bay employers in defence electronics, medical devices, utilities and semiconductors.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One public carrier: University of South Florida, at 3 credits.</strong> USF publishes no contact '
    'hours; the 45 shown are derived from Florida\'s convention of 15 per credit.</p>'
    '<h3>⚠ A grade of B in the prerequisite</h3>'
    '<p>USF requires a <strong>B</strong> in EGN 3374, not the usual C. A student with a C in EGN 3374 cannot '
    'register for EEL3100 and may have to repeat EGN 3374 &mdash; which can delay graduation by a term. Treat EGN '
    '3374 as a course to do well in, not just to pass.</p>'
    '<h3>Transfer</h3>'
    '<p>No other Florida institution uses EEL3100. Elsewhere this material sits in the second circuits course '
    '(EEL3112 at FAMU, Florida Poly, FSU, UF, UNF and UWF; EEL3123C at UCF) or in a signals and systems course. A '
    'student transferring into USF with two circuits courses should ask whether they cover EGN 3373&ndash;3374, '
    'EEL3100, or both. Bring the syllabi.</p>'
    '<h3>Workload</h3>'
    '<p>Mathematically the heaviest of the circuits courses. Keep differential equations and complex numbers '
    'fresh; expect 8&ndash;12 hours a week outside class.</p>'
    + AI_CIRCUITS)

EEL3100 = {
    'title': 'Network Analysis and Design',
    'html_content': EEL3100_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': EEL3100_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One public carrier, University of South Florida, at 3 credits.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [off('USF', USF, 'Network Analysis and Design', 3,
                          'Prerequisites EGN 3420 (C) and EGN 3374 (B).')],
    },
}

# ---------------------------------------------------------------------------------------------
# BCV0632C Residential Electrician III (NFC 150 h, Seminole State 75 h) -- PSAV
# ---------------------------------------------------------------------------------------------
BCV0632C_PRE = (
    'Clock-hour career certificate course (no college credit). North Florida College: the third of three '
    'Residential Electrician courses (after BCV 0641C and BCV 0631C) in its 1500-hour Electrician programme. '
    'Seminole State: prerequisites or corequisites BCV 0611C and BCV 0601C. The two schools teach different '
    'content under this number; see the guide.')

BCV0632C_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>BCV0632C</strong> <em>Residential Electrician III</em> is a clock-hour (PSAV) course in Florida\'s '
    '<strong>Electricity</strong> career certificate. Two Florida public colleges carry it: <strong>North Florida '
    'College</strong> (Madison) at <strong>150 clock hours</strong> and <strong>Seminole State College</strong> '
    '(Sanford) at <strong>75 clock hours</strong>. It carries no college credit.</p>'
    '<p>The state framework builds the Electricity programme as occupational completion points: <strong>OCP A</strong> '
    '<em>Electrician Helper</em> (BCV0603), <strong>OCP B</strong> <em>Residential Electrician</em> (BCV0640), '
    '<strong>OCP C</strong> <em>Commercial Electrician</em> (BCV0652) and, at some schools, <strong>OCP D</strong> '
    '<em>Industrial Electrician</em> (BCV0667). Most of Florida\'s technical colleges teach OCP B as the single course '
    'BCV0640; the two state colleges here split it into numbered parts, and <strong>BCV0632C is part III</strong>.</p>'
    '<p>⚠ <strong>The two carriers do not teach the same thing under this number</strong>:</p>'
    + table(['', 'North Florida College', 'Seminole State College'], [
        ['Hours', '<strong>150</strong>', '<strong>75</strong>'],
        ['What it covers', '"Students will learn how to lay out lighting with a laser alignment tool, install the '
         'lighting to meet all building codes and manufactures specifications. Students will understand the '
         'different types of duplex receptacle and their uses and the locations they will be used, as well as NFPA '
         '72 and how it relates to the type of smoke detectors to be used, and how they must be installed. Students '
         'will learn about service entrance meters and the associated requirements to meet the Florida Building Code '
         'when installing service entrance equipment."',
         '"Classroom/lab study of the fundamentals of the electrical trade. Areas of study include demonstrating '
         'alternating-current (AC) circuit skills, the use of high voltage testing equipment and identification of '
         'AC sources. Lab fee required."'],
        ['Where it sits', 'last of three residential courses; completes OCP B',
         'one of a series of 75-hour modules (Residential II, BCV0631C, covers boxing out, wiring and continuity '
         'testing of a residential unit)']])
    + '<p>The outcomes below are labelled by school where they differ.</p>'
    + sec('Learning Outcomes', [
        'Work safely on residential electrical systems: lockout/tagout, verifying de-energisation, PPE.',
        'Apply the <strong>National Electrical Code</strong> (NFPA 70) and the Florida Building Code to residential '
        'installations.',
        'Use test equipment correctly and safely, and interpret the readings.'],
        ['(NFC) Lay out and install lighting with a laser alignment tool to code and to the manufacturer\'s '
         'instructions.',
         '(NFC) Select and install duplex receptacles (including GFCI, AFCI, tamper-resistant and weather-resistant '
         'types) in the locations the NEC requires.',
         '(NFC) Select and install smoke alarms under <strong>NFPA 72</strong> and the building code.',
         '(NFC) Install service entrance equipment and meter bases to meet the Florida Building Code and the '
         'utility\'s requirements.',
         '(Seminole) Demonstrate <strong>AC circuit</strong> skills: voltage, current, impedance and power in AC '
         'circuits.',
         '(Seminole) Use <strong>high-voltage testing equipment</strong> and identify AC sources.'])
    + sec('Major Topics', [
        'Electrical safety (OSHA, NFPA 70E basics).', 'NEC requirements for dwellings.', 'Test equipment.'],
        ['(NFC) Lighting layout and installation.', '(NFC) Receptacle types and required locations.',
         '(NFC) NFPA 72 smoke alarms.', '(NFC) Service entrances, meters and the Florida Building Code.',
         '(Seminole) AC circuit fundamentals.', '(Seminole) High-voltage testing and identifying AC sources.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('<em>National Electrical Code</em> (NFPA 70), current Florida-adopted edition; NFPA 72 (fire alarm and '
         'signalling); the <em>Florida Building Code</em>.',
         'NCCER <em>Electrical</em> curriculum (levels 1&ndash;2) or Mullin and Simmons, <em>Electrical Wiring '
         'Residential</em> (Cengage).',
         'Multimeter, non-contact tester, insulation and voltage testers; a laser level (NFC).',
         'OSHA 10 (NFC offers it earlier in the programme).')
    + '<h2>Career Pathways</h2>'
    + ul('<strong>Electrician</strong> (SOC 47-2111) and <strong>electrician\'s helper</strong> (47-3013), '
         'beginning in residential construction.',
         'Florida licenses electrical <strong>contractors</strong> (ch. 489, Part II, F.S.; the Electrical '
         'Contractors\' Licensing Board), not journeyman electricians statewide; some counties and cities issue '
         'their own journeyman cards. A certificate does not license you; it prepares you for work under a licensed '
         'contractor and counts toward the experience a later licence needs. Ask your county.',
         'Registered apprenticeships (for example through IEC, ABC or the IBEW/NECA joint councils) combine paid '
         'work with classroom hours and lead to journeyman status.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    + table(['Institution', 'Title', 'Clock hours', 'Programme'], [
        ['North Florida College', 'Residential Electrician III', '<strong>150</strong>',
         'Electrician, programme 5065, CIP 46.0302, 1500 hours'],
        ['Seminole State College of Florida', 'Electrician &ndash; Residential III', '<strong>75</strong>',
         'Electricity career certificate; fall, spring and summer']])
    + '<p>The guide\'s figure of 150 is North Florida College\'s; Seminole State runs the course at half that. Both '
    'are published figures (NFC\'s catalogue, Seminole State\'s course page and the SCNS file agree).</p>'
    '<h3>What you can stop with</h3>'
    '<p>At North Florida College, finishing Residential Electrician I, II and III (450 hours, after the 300-hour '
    'Electrician Helper courses) earns <strong>OCP B, Residential Electrician</strong> &mdash; a point at which you can '
    'leave, work, and come back for the commercial and industrial courses. Ask whether the college will issue a '
    'certificate at that point; the state builds the programme around it, but not every college awards one.</p>'
    '<h3>Transfer and the number</h3>'
    '<p>Because the two schools teach different content and hours under BCV0632C, a student moving between them '
    'should not assume part III at one school completes part III at the other. Florida\'s technical colleges use '
    'BCV0640 for the whole residential stage. Bring your hours and competencies record.</p>'
    '<h3>Safety</h3>'
    '<p>Treat every conductor as live until you have tested it with a tester you have just proved works on a known '
    'source. Residential voltages kill. Follow the laboratory\'s lockout rules exactly.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain a code article or a circuit, but they quote NEC sections from the wrong edition, '
    'invent article numbers and miss local amendments. <strong>Look every requirement up in the adopted code book; '
    'an inspector will not accept "the AI said".</strong></p>')

BCV0632C = {
    'title': 'Residential Electrician III',
    'html_content': BCV0632C_HTML,
    'credits': 0,
    'contact_hours': 150,
    'prerequisites': BCV0632C_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'Two public carriers: North Florida College at 150 clock hours and Seminole State College at 75, '
                   'teaching different content under the number.',
        'hours_source': 'published',
        'offerings': [
            off('NFC', NFC, 'Residential Electrician III', 0,
                'Third residential course; completes OCP B in the 1500-hour Electrician programme.', 150),
            off('SSCF', SSC, 'Electrician - Residential III', 0,
                'AC circuits, high-voltage testing, AC sources. Pre/coreq BCV 0611C and BCV 0601C. Lab fee.', 75)],
    },
}

ALL = (('EEL2161', EEL2161), ('EEL2603C', EEL2603C), ('EEL2880', EEL2880), ('EEL3000', EEL3000),
       ('EEL3003', EEL3003), ('EEL3004C', EEL3004C), ('EEL3100', EEL3100), ('BCV0632C', BCV0632C))

for cid, g in ALL:
    path = os.path.join(DRAFTS, '%s_guide.json' % cid)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(g, fh, ensure_ascii=False, indent=1)
    print('wrote', cid, len(g['html_content']), 'chars; prereq', len(g['prerequisites']))
