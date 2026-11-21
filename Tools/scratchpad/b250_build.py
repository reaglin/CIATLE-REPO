#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Batch 250 -- scheduled request check 2026-11-21 (fourth run of the day).

Requests in rank order after the four held items (EEL4448, EEL5025, EEL5009, EET2525C -- REVIEW_QUEUE 130-132, 134):
EML4328C, ETS1542, ETS2542, ETS2544, ETS4543C, ETS3543L, ECH3702.

  Written    EML4328C ETS1542 ETS2542 ETS2544 ETS4543C ECH3702
  Held       ETS3543L (FAMU only; catalog.famu.edu fails the TLS check for every route tried, no description)

Sources:
  UNF        webappsapi.unf.edu/cascade/api/v1/catalog/GetCourses/course?year=2026-2027 (NEW: the JSON behind the
             script-rendered www.unf.edu/catalog/courses/; 3,503 courses with prerequisite and description) --
             EML4328C and ETS4543C carry the SAME description and prerequisite; the 2026-27 Advanced Manufacturing
             Engineering BS lists ETS4543C as a technical elective (www.unf.edu/catalog/programs/ug/ccec/CCEC-BSCADM.html)
  PHSC       phsc.smartcatalogiq.com 2026-2027 ETS 1542 (description, "45 class hours", lab fee)
  IRSC       irsc.smartcatalogiq.com 2025-2026 ETS 2542, ETS 2544 (the 2026-27 catalogue is not yet up)
  USF        cloud.usf.edu/academic-programs/details/prefix/ECH/code/3702; the department's program-of-study page
  All        SCNS flat file: carriers, titles, credits, statewide course records
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


DERIVED = ("Florida's convention of 15 contact hours per credit for a lecture course; no carrier publishes a term "
           'contact-hour figure for this number.')
DERIVED_C = ("Florida's convention of 60 contact hours for a 3-credit integrated lecture-and-laboratory (C) course; "
             'no carrier publishes a term contact-hour figure for this number.')

UNF = 'University of North Florida'
USF = 'University of South Florida'
PHSC = 'Pasco-Hernando State College'
SFSC = 'South Florida State College'
CF = 'College of Central Florida'
NFC = 'North Florida College'
HC = 'Hillsborough College'
SFC = 'Santa Fe College'
IRSC = 'Indian River State College'

# ---------------------------------------------------------------------------------------------
# Shared PLC material
# ---------------------------------------------------------------------------------------------
PLC_RESOURCES = ul(
    'A PLC trainer: most Florida programmes use Allen-Bradley (Rockwell Automation) MicroLogix, CompactLogix or '
    'Micro800 controllers; some use Siemens S7-1200. Ask which one your college uses before buying any book.',
    'Programming software: Rockwell <em>Studio 5000 Logix Designer</em>, <em>RSLogix 500</em> or the free '
    '<em>Connected Components Workbench</em> (Micro800); Siemens <em>TIA Portal</em>. Simulators such as '
    '<em>LogixPro</em> let you practise ladder logic at home.',
    'Common textbooks: <em>Programmable Logic Controllers</em>, Frank D. Petruzella (McGraw-Hill); '
    '<em>Programmable Logic Controllers</em>, James A. Rehg and Glenn J. Sartori (Pearson); '
    '<em>Introduction to Programmable Logic Controllers</em>, Gary Dunning (Cengage).',
    'Standards: <strong>IEC 61131-3</strong> (the five PLC programming languages), <strong>NFPA 79</strong> '
    '(electrical standard for industrial machinery) and <strong>NFPA 70E</strong> (electrical safety in the '
    'workplace, including lockout/tagout).',
    'A digital multimeter, and the safety glasses your lab requires.')

PLC_CAREERS = ul(
    '<strong>Industrial machinery mechanics and maintenance technicians</strong> (SOC 49-9041, 49-9071) &mdash; the '
    'largest group of people who troubleshoot PLC-controlled equipment every day.',
    '<strong>Electrical and electronics engineering technicians</strong> (17-3023) and '
    '<strong>electro-mechanical and mechatronics technicians</strong> (17-3024).',
    '<strong>Industrial electricians</strong> (47-2111) working in plants, water and wastewater utilities, and '
    'distribution centres.',
    '<strong>Automation and controls technicians</strong>, and with a bachelor\'s degree, <strong>controls '
    'engineers</strong> (often classed under electrical, 17-2071, or industrial engineers, 17-2112).',
    'Florida employers include food and beverage plants, aerospace manufacturing on the Space Coast and in '
    'Jacksonville, distribution and logistics automation (conveyors and sortation in Central Florida and Tampa Bay), '
    'phosphate and chemical processing in Polk County, power generation, and municipal water and wastewater.')

PLC_CERTS = (
    '<h3>Certifications this course supports</h3>'
    '<p>No licence is needed to program a PLC in Florida. Industry credentials that build on this course include the '
    '<strong>Siemens Mechatronic Systems Certification (SMSCP)</strong>, the <strong>ETA International</strong> '
    'industrial electronics certifications, the <strong>ISA Certified Automation Professional (CAP)</strong> for '
    'experienced practitioners, and vendor training from Rockwell Automation. Ask your programme which ones it '
    'prepares students for &mdash; Florida colleges choose different ones.</p>')

AI_PLC = (
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI assistants can explain an instruction, describe a ladder rung in words, draft Structured Text, and help '
    'read a fault code, and PLC vendors are adding AI helpers to their programming software. They are also '
    'confidently wrong in ways that matter on a machine: they mix up Allen-Bradley and Siemens instruction names and '
    'addressing, forget the scan cycle (an output written twice in one scan takes the <em>last</em> value), assume '
    'inputs are wired normally open when the safety device is normally closed, and leave out the seal-in or '
    'interlock that keeps a motor from restarting by itself. <strong>Never download AI-written logic to real '
    'equipment you have not traced rung by rung and tested in simulation first, and never let any program &mdash; '
    'yours or a tool\'s &mdash; replace a hard-wired emergency stop.</strong> Follow your instructor\'s policy on AI '
    'use.</p>')

SCNS_EQUIV = (
    '<p>In Florida\'s Statewide Course Numbering System, two courses with the <strong>same prefix and the same last '
    'three digits</strong> are treated as the same course, whatever the first digit. So <strong>ETS1542, '
    'ETS2542 and their C forms all sit on the statewide course <em>Programmable Logic Controllers 1</em></strong>, '
    'and ETS2544 and ETS2544C on <em>Programmable Logic Controllers 2</em>. Whether a lecture-only form or an '
    'integrated lecture-and-laboratory (C) form is used is a packaging choice each college makes; the content is '
    'meant to be the same. Still, carry your syllabus when you transfer and ask the receiving programme to confirm '
    'in writing.</p>')

# ---------------------------------------------------------------------------------------------
# ETS1542 Introduction to Programmable Logic Controllers
# ---------------------------------------------------------------------------------------------
ETS1542_PRE = (
    'None listed by Pasco-Hernando State College, the one carrier whose catalogue could be read. Other colleges may '
    'require a DC/AC circuits course first (for example EET 1015C/EET 1025C) or program admission; check your '
    'catalogue. Many colleges teach the same course as ETS 1542C (with lab) or ETS 2542; these are equivalent in '
    'SCNS, so do not take two of them for credit.')

ETS1542_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>ETS1542</strong> is a first course in <strong>programmable logic controllers (PLCs)</strong>, the '
    'industrial computers that run machines, conveyors, pumps and process lines. Students learn how a PLC is built '
    'and how it scans its program, write ladder logic with contacts, coils, timers and counters, use it to control '
    'motors and sequences, connect a PLC and an operator screen over Ethernet, and troubleshoot a working system.</p>'
    '<p>Five Florida College System institutions carry the number, all at 3 credits: Pasco-Hernando State, South '
    'Florida State, College of Central Florida, Hillsborough College and North Florida College. Pasco-Hernando\'s '
    '2026&ndash;27 catalogue describes it this way: <em>"The course covers PLC operation and basic program '
    'instructions, PLC project elements, PLC motor control, PLC event sequencing, counter and timer instructions, '
    'PLC Ethernet operation, HMI Ethernet operation, and component and system troubleshooting. Lab fee required. 45 '
    'class hours."</em> The other four catalogues could not be read for this guide, so the outcomes below follow '
    'Pasco-Hernando and the content common to first PLC courses across Florida; use Optional Outcomes for where your '
    'college may differ.</p>'
    '<p>⚠ The same statewide course, <em>Programmable Logic Controllers 1</em>, is taught at nine more colleges as '
    '<strong>ETS1542C</strong> (integrated lecture and laboratory) and at six as <strong>ETS2542C</strong> or two '
    'as <strong>ETS2542</strong> &mdash; see Special Information.</p>'
    + sec('Learning Outcomes', [
        'Explain what a PLC is, why it replaced relay panels, and how the <strong>scan cycle</strong> (read inputs, '
        'run the program, write outputs) decides what the machine does.',
        'Identify PLC hardware: power supply, processor, discrete input and output modules, and communication ports, '
        'and read a wiring diagram for field devices.',
        'Write, enter, download and monitor <strong>ladder logic</strong> using examine-if-closed, examine-if-open and '
        'output instructions, including <strong>seal-in</strong> and interlock rungs.',
        'Program <strong>timers and counters</strong> to solve timing and counting problems.',
        'Control a motor with a PLC (start/stop, forward/reverse) and sequence a series of events.',
        'Organise a PLC project: tags or addresses, program files and documentation.',
        'Set up Ethernet communication between a PLC, a programming computer and an <strong>HMI</strong> (operator '
        'touch screen).',
        'Troubleshoot a PLC system using status indicators, online monitoring and a meter, and work safely around '
        'energised equipment.'],
        ['Use number systems (binary, hexadecimal, BCD) and Boolean logic in PLC addressing.',
         'Use compare, move and math instructions.',
         'Wire sinking and sourcing inputs and outputs.',
         'Read or write simple programs in a second IEC 61131-3 language such as Function Block Diagram or '
         'Structured Text.'])
    + sec('Major Topics', [
        'Industrial control before and after the PLC; relay logic and ladder diagrams.',
        'PLC hardware, power supplies and discrete I/O; field devices (push buttons, limit switches, proximity and '
        'photoelectric sensors, pilot lights, motor starters).',
        'The scan cycle, memory and addressing (Allen-Bradley tags or file addresses, depending on the controller).',
        'Bit instructions, latching and unlatching, seal-in circuits and interlocks.',
        'On-delay and off-delay timers, retentive timers, up and down counters.',
        'PLC motor control and event sequencing.',
        'Ethernet networking for PLCs and HMIs.',
        'Component and system troubleshooting; lockout/tagout and electrical safety.'],
        ['Number systems and Boolean algebra.', 'Data handling: compare, move, math.',
         'Analog signals (4&ndash;20 mA, 0&ndash;10 V) as a preview of the second course.'])
    + '<h2>Resources &amp; Tools</h2>' + PLC_RESOURCES
    + '<h2>Career Pathways</h2>' + PLC_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    + table(['Institution', 'Its title', 'Credits', 'Contact hours'], [
        ['Pasco-Hernando State College', 'Introduction to Programmable Logic', '3', '<strong>45 class hours</strong> '
         '(published); lab fee'],
        ['South Florida State College', 'Introduction to Programmable Logic Controllers', '3', 'not published'],
        ['College of Central Florida', 'Introduction to PLC\'s', '3', 'not published'],
        ['Hillsborough College', 'Introduction to Programmable Logic Controllers', '3', 'not published'],
        ['North Florida College', 'Introduction to Programmable Logic Controllers', '3', 'not published; ⚠ not '
         'found in NFC\'s 2026&ndash;27 catalogue']])
    + '<p><strong>All five carry it at 3 credits.</strong> The 45 contact hours in this guide are Pasco-Hernando\'s '
    'published figure. ⚠ North Florida College is listed as a carrier in the state course file, but its '
    '2026&ndash;27 catalogue lists no ETS courses, so check with NFC before planning on it.</p>'
    '<h3>Same course, other numbers</h3>' + SCNS_EQUIV
    + table(['Number', 'Form', 'Public carriers'], [
        ['ETS1542', 'lecture (labs included in the hours at some colleges)', 'PHSC, SFSC, CF, HC, NFC'],
        ['ETS1542C', 'integrated lecture and lab', 'Eastern Florida, FSCJ, Lake-Sumter, Northwest Florida, Polk, '
         'St. Johns River, St. Petersburg, Seminole State, Tallahassee State'],
        ['ETS2542 / ETS2542C', 'sophomore-numbered', 'Indian River, Santa Fe (2542); Broward, Chipola, Daytona '
         'State (4 cr), Gulf Coast, Pensacola, Valencia (2542C)']])
    + '<h3>Position in the curriculum</h3>'
    '<p>This is the first PLC course in A.S. degrees and college credit certificates in engineering technology, '
    'electronics, advanced manufacturing and mechatronics. It leads to a second PLC course (Programmable Logic '
    'Controllers 2: ETS2544 or ETS2544C), and to robotics, motor control and process-control courses. As a career and '
    'technical course it is not a general-education course; it transfers into A.S.-to-B.A.S. and B.S. Engineering '
    'Technology pathways rather than into an engineering B.S.</p>'
    + PLC_CERTS + AI_PLC)

ETS1542 = {
    'title': 'Introduction to Programmable Logic Controllers',
    'html_content': ETS1542_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': ETS1542_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'Five Florida College System carriers, all at 3 credits. Pasco-Hernando publishes 45 class hours; '
                   'the others publish none. North Florida College is in the state file but not in its 2026-27 '
                   'catalogue.',
        'hours_source': 'mixed',
        'derived_contact_hours': 45,
        'derivation': 'Pasco-Hernando State College publishes 45 class hours; the other carriers publish none.',
        'offerings': [
            off('PHSC', PHSC, 'Introduction to Programmable Logic', 3, 'Lab fee. No prerequisite listed.', 45),
            off('SFSC', SFSC, 'Introduction to Programmable Logic Controllers', 3, 'Catalogue not readable.'),
            off('CF', CF, "Introduction to PLC's", 3, 'Catalogue not readable.'),
            off('HC', HC, 'Introduction to Programmable Logic Controllers', 3, 'Catalogue not readable.'),
            off('NFC', NFC, 'Introduction to Programmable Logic Controllers', 3,
                'In the SCNS file since 2017, but not in the 2026-27 NFC catalogue.')],
    },
}

# ---------------------------------------------------------------------------------------------
# ETS2542 Programmable Logic Controllers I
# ---------------------------------------------------------------------------------------------
ETS2542_PRE = (
    'Indian River State College: EET 2141C Electronic Devices I, which may be taken before or in the same term. Santa '
    'Fe College\'s prerequisite could not be read; check your catalogue. Equivalent in SCNS to ETS 1542, ETS 1542C '
    'and ETS 2542C (Programmable Logic Controllers 1), so do not take two of them for credit.')

ETS2542_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>ETS2542</strong> is the first of a two-course sequence in <strong>programmable logic controllers '
    '(PLCs)</strong>, the computers that control industrial machines and processes. Two Florida College System '
    'institutions carry this number, both at 3 credits: <strong>Indian River State College</strong> '
    '(<em>Programmable Logic Controllers I</em>) and <strong>Santa Fe College</strong> (<em>Programmable Logic '
    'Controller (PLC) I</em>).</p>'
    '<p>Indian River\'s 2025&ndash;26 catalogue: <em>"In this course, students learn the basic operational concepts '
    'common to PLCs, focusing on PLC principles, programming, numbering systems, data manipulation, math, and '
    'sequencer instructions. This programmable logic controllers (PLC) course is designed for students preparing '
    'for careers in electronics, manufacturing, electrical or industrial technology."</em> It carries a lab fee. Santa '
    'Fe\'s catalogue could not be read for this guide, so the outcomes follow Indian River and the content common to '
    'first PLC courses in Florida; read the Optional lists against your own syllabus.</p>'
    '<p>Unlike some first PLC courses, Indian River\'s goes past bits, timers and counters into '
    '<strong>number systems, data manipulation, math and sequencer instructions</strong> &mdash; material other '
    'colleges hold back for the second course.</p>'
    + sec('Learning Outcomes', [
        'Explain PLC hardware and the <strong>scan cycle</strong>, and how the controller reads inputs, solves logic '
        'and updates outputs.',
        'Convert between <strong>binary, octal, hexadecimal and BCD</strong>, and use them in PLC addressing and data.',
        'Write and troubleshoot <strong>ladder logic</strong> with contacts, coils, latches, seal-in and interlock '
        'rungs.',
        'Program <strong>timers and counters</strong> for timing and counting tasks.',
        'Use <strong>data manipulation</strong> (move, copy, compare) and <strong>math</strong> instructions.',
        'Program <strong>sequencer</strong> instructions to step a machine through a fixed cycle.',
        'Wire discrete inputs and outputs to a PLC and test them with the programming software online.'],
        ['Control a motor (start/stop, jog, forward/reverse) with interlocks.',
         'Set up communication between a PLC, a programming computer and an operator screen (HMI).',
         'Read simple programs in a second IEC 61131-3 language.'])
    + sec('Major Topics', [
        'PLCs and industrial automation; relay logic and ladder diagrams.',
        'PLC hardware: power supply, processor, discrete I/O; field devices.',
        'Number systems and codes; Boolean logic.',
        'Memory organisation and addressing.',
        'Bit instructions, latching, seal-in and interlocks.',
        'Timers and counters.',
        'Data manipulation and math instructions.',
        'Sequencer instructions.',
        'Electrical safety in the PLC laboratory.'],
        ['Shift registers.', 'Program control (jumps, subroutines).', 'Introduction to HMIs and Ethernet.'])
    + '<h2>Resources &amp; Tools</h2>' + PLC_RESOURCES
    + '<h2>Career Pathways</h2>' + PLC_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    + table(['Institution', 'Its title', 'Credits', 'Notes'], [
        ['Indian River State College', 'Programmable Logic Controllers I', '3', 'pre/corequisite EET 2141C; lab '
         'fee; followed by ETS 2544'],
        ['Santa Fe College', 'Programmable Logic Controller (PLC) I', '3', 'catalogue not readable for this guide']])
    + '<p><strong>Both carry it at 3 credits.</strong> Neither publishes a term contact-hour figure; the 45 shown '
    'are derived from Florida\'s convention of 15 per credit. Both colleges charge a lab fee or run laboratory '
    'work inside the course, so expect hands-on time beyond the lecture.</p>'
    '<h3>Same course, other numbers</h3>' + SCNS_EQUIV
    + '<p>Most Florida colleges number this course <strong>ETS1542C</strong> (nine colleges) or '
    '<strong>ETS2542C</strong> (Broward, Chipola, Daytona State at 4 credits, Gulf Coast, Pensacola, Valencia); five '
    'more use <strong>ETS1542</strong>.</p>'
    '<h3>Position in the curriculum</h3>'
    '<p>At Indian River it sits in the electronics engineering technology sequence after DC/AC circuits, alongside '
    'Electronic Devices I, and leads to <strong>ETS2544 Programmable Logic Controllers II</strong>. It is a career and '
    'technical course for A.S. degrees and certificates; it does not count toward general education.</p>'
    + PLC_CERTS + AI_PLC)

ETS2542 = {
    'title': 'Programmable Logic Controllers I',
    'html_content': ETS2542_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': ETS2542_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'Two Florida College System carriers, both at 3 credits. No carrier publishes contact hours.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [
            off('IRSC', IRSC, 'Programmable Logic Controllers I', 3, 'Pre/corequisite EET 2141C. Lab fee $20.'),
            off('SFC', SFC, 'Programmable Logic Controller (PLC) I', 3, 'Catalogue not readable.')],
    },
}

# ---------------------------------------------------------------------------------------------
# ETS2544 Programmable Logic Controllers II
# ---------------------------------------------------------------------------------------------
ETS2544_PRE = (
    'Indian River State College: ETS 2542 Programmable Logic Controllers I, which its catalogue allows to be taken '
    'before or in the same term (taking it first is the safer plan). Equivalent in SCNS to ETS 2544C '
    '(Programmable Logic Controllers 2) at St. Johns River, Lake-Sumter and Valencia.')

ETS2544_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>ETS2544</strong> is the second course in programmable logic controllers. In the state course file '
    'only <strong>Indian River State College</strong> carries this number (<em>Programmable Logic Controllers '
    'II</em>, 3 credits); three other colleges teach the same statewide course, <em>Programmable Logic Controllers '
    '2</em>, as <strong>ETS2544C</strong>.</p>'
    '<p>⚠ <strong>Indian River\'s current (2025&ndash;26) catalogue gives this course almost the same description as '
    'the first course</strong>: <em>"students learn the basic operational concepts common to programmable logic '
    'controllers (PLCs), focusing on PLC principles, programming, numbering systems, data manipulation, math, and '
    'sequencer instructions. This second PLC course is designed for students preparing for careers in electronics, '
    'manufacturing, electrical or industrial technology."</em> Earlier Indian River catalogues (2019&ndash;20) '
    'described it as building on ETS 2542 with <strong>program control, data manipulation, math, sequencer and '
    'shift-register instructions, PLC installation and troubleshooting, and process control</strong>. This guide '
    'follows that fuller description and what second PLC courses teach elsewhere in Florida; ask your instructor '
    'for the syllabus, because the current catalogue wording does not separate the two courses.</p>'
    + sec('Learning Outcomes', [
        'Use <strong>program control</strong> instructions: jumps, subroutines, master control reset and immediate '
        'I/O.',
        'Write programs with <strong>data manipulation and math</strong> instructions, and scale values.',
        'Program <strong>sequencers and shift registers</strong> to track parts and step machines through cycles.',
        'Configure and program <strong>analog</strong> inputs and outputs (4&ndash;20 mA, 0&ndash;10 V) and use them '
        'for <strong>process control</strong>, including an introduction to PID loops.',
        'Plan a PLC <strong>installation</strong>: enclosure, power, grounding, wiring and documentation.',
        'Troubleshoot a PLC system systematically, using diagnostics, forcing (safely) and test equipment.'],
        ['Build an operator screen (HMI) and connect it over Ethernet.',
         'Use Function Block Diagram, Sequential Function Chart or Structured Text.',
         'Network PLCs (EtherNet/IP, Modbus) and control a variable frequency drive.'])
    + sec('Major Topics', [
        'Review of PLC hardware, scan cycle and basic instructions.',
        'Program control instructions.',
        'Data manipulation, math and comparison; scaling.',
        'Sequencers and shift registers.',
        'Analog I/O and process control; PID.',
        'PLC installation practices and wiring standards (NFPA 79).',
        'Troubleshooting and diagnostics; electrical safety and lockout/tagout (NFPA 70E).'],
        ['HMI design.', 'Industrial networks.', 'Variable frequency drives and motion.',
         'IEC 61131-3 languages beyond ladder.'])
    + '<h2>Resources &amp; Tools</h2>' + PLC_RESOURCES
    + '<h2>Career Pathways</h2>' + PLC_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One carrier: Indian River State College, 3 credits</strong>, lab fee. Indian River publishes no '
    'contact-hour figure; the 45 shown are derived from Florida\'s convention of 15 per credit.</p>'
    '<h3>Same course, other numbers</h3>' + SCNS_EQUIV
    + table(['Number', 'Carrier', 'Credits'], [
        ['ETS2544', 'Indian River State College', '3'],
        ['ETS2544C', 'St. Johns River State College', '3'],
        ['ETS2544C', 'Valencia College', '3'],
        ['ETS2544C', 'Lake-Sumter State College (<em>Advanced PLCs</em>)', '⚠ 2']])
    + '<p>⚠ Lake-Sumter carries the C form at 2 credits, so a student moving between Lake-Sumter and the others is a '
    'credit short or long against a degree requirement. Check the credit value on your own transcript.</p>'
    '<h3>Position in the curriculum</h3>'
    '<p>The second PLC course in electronics and engineering technology A.S. degrees and certificates. At Indian River '
    'it follows ETS 2542; the catalogue lets the two be taken together, but the second course assumes the first '
    'course\'s ladder logic, timers and counters, so taking them in order is the safer plan.</p>'
    + PLC_CERTS + AI_PLC)

ETS2544 = {
    'title': 'Programmable Logic Controllers II',
    'html_content': ETS2544_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': ETS2544_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One carrier, Indian River State College, at 3 credits. No contact hours published.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [
            off('IRSC', IRSC, 'Programmable Logic Controllers II', 3,
                'Pre/corequisite ETS 2542. Lab fee $20. The 2025-26 description nearly repeats ETS 2542\'s.')],
    },
}

# ---------------------------------------------------------------------------------------------
# ETS4543C / EML4328C Applied Programmable Logic Controllers (UNF) -- one course, two numbers
# ---------------------------------------------------------------------------------------------
UNF_DESC = (
    '"This course introduces students to the hardware and programming utilized to control processes in modern '
    'manufacturing settings. The course begins with a survey of the operating principles of hardware including '
    'programmable logic controllers (PLCS), sensors, motion control, temperature control, pressure control, and '
    'others. The course introduces the fundamentals and application of two-position and PID control. The course then '
    'transitions to hands-on laboratories utilizing modern PLC hardware and software to perform specific tasks '
    'pertinent to manufacturing processes."')

UNF_OUT = sec('Learning Outcomes', [
    'Explain how a <strong>PLC</strong> is built and how its scan cycle reads inputs, solves logic and writes '
    'outputs, and how it differs from a microcontroller or a PC.',
    'Describe the operating principles of the <strong>sensors and actuators</strong> used in manufacturing: discrete '
    'sensors (limit, proximity, photoelectric), temperature and pressure sensors, motors and drives.',
    'Write, test and document <strong>ladder logic</strong> with timers, counters, comparisons and math for '
    'manufacturing tasks.',
    'Apply <strong>two-position (on/off) control</strong>, including hysteresis, and explain when it is good enough.',
    'Apply <strong>PID control</strong>: the effect of proportional, integral and derivative action, and tuning a '
    'loop on real hardware.',
    'Use <strong>motion, temperature and pressure control</strong> hardware with a PLC in the laboratory.',
    'Work safely with energised industrial equipment.'],
    ['Build an operator screen (HMI) and connect devices over an industrial network.',
     'Program in Structured Text or Function Block Diagram (IEC 61131-3).',
     'Relate PLC control to the Laplace-domain controller design of a controls course.'])

UNF_TOP = sec('Major Topics', [
    'Process control in manufacturing; the PLC and its alternatives.',
    'PLC hardware, I/O and the scan cycle.',
    'Sensors and transducers: discrete, temperature, pressure.',
    'Actuators: motors, drives, valves; motion control.',
    'Ladder logic: bits, timers, counters, compare and math.',
    'Two-position control.',
    'PID control and tuning.',
    'Hands-on laboratories with modern PLC hardware and software on manufacturing tasks.'],
    ['HMIs and industrial networks.', 'IEC 61131-3 languages beyond ladder.', 'Safety circuits and standards '
     '(NFPA 79, NFPA 70E).'])

UNF_RES = ul(
    'UNF\'s laboratory PLC platform and software (ask the department which vendor is used; Rockwell Studio 5000 and '
    'Siemens TIA Portal are the two most common in Florida industry).',
    '<em>Programmable Logic Controllers</em>, Frank D. Petruzella (McGraw-Hill), or <em>Programmable Logic '
    'Controllers</em>, Rehg and Sartori (Pearson), for ladder logic; a process-control text such as '
    '<em>Process Control Instrumentation Technology</em>, Curtis D. Johnson (Pearson), for sensors and PID.',
    'Standards: IEC 61131-3, NFPA 79, NFPA 70E; ISA-5.1 for instrumentation symbols.',
    'MATLAB/Simulink or a PID simulator for trying tuning before touching hardware.')

UNF_CAREERS = ul(
    '<strong>Manufacturing engineers</strong> and <strong>industrial engineers</strong> (SOC 17-2112), who specify '
    'and improve automated lines.',
    '<strong>Mechanical engineers</strong> (17-2141) in machine design, where a working knowledge of the controller '
    'is expected.',
    '<strong>Controls and automation engineers</strong>, often classed as electrical engineers (17-2071).',
    'Northeast Florida employers with automated production include aerospace and defence manufacturers, medical '
    'device makers, food and beverage plants, the Port of Jacksonville\'s logistics operations, and paper and '
    'chemical processing.')

UNF_FE = (
    '<h3>FE exam</h3>'
    '<p>The FE Mechanical and FE Electrical and Computer exams both include <strong>measurement, instrumentation and '
    'controls</strong> (sensors, block diagrams, feedback and PID). This course gives a hands-on view of the same '
    'material; the exam still expects the analytical treatment from a controls course.</p>')

UNF_TWO = (
    '<h3>⚠ One course, two numbers</h3>'
    '<p>UNF\'s 2026&ndash;27 catalogue gives <strong>ETS4543C</strong> <em>Applied Programmable Logic Controllers</em> '
    '(Electrical Engineering department) and <strong>EML4328C</strong> <em>Applied Programmable Logic Controllers '
    'for ME</em> (Mechanical Engineering department) <strong>the same description and the same prerequisite, EEL '
    '3111</strong>, both at 3 credits. Register for the number your degree names: the <strong>Advanced Manufacturing '
    'Engineering B.S.</strong> lists ETS4543C among its technical electives, and EML4328C is the mechanical '
    'engineering listing. Do not take both for credit.</p>'
    '<p>For transfer, the two numbers behave differently. <strong>ETS4543C</strong> sits on the statewide course '
    '<em>Programmable Logic Controllers</em> (upper division), the same statewide course as Daytona State\'s ETS3543C '
    'and FAMU\'s ETS3543 + ETS3543L (and University of West Florida\'s ETS3543 in older catalogues), because SCNS treats '
    'the same prefix and last three digits as one course. <strong>EML4328C is its own statewide course</strong> '
    'and has no equivalent elsewhere in Florida.</p>')

ETS4543C_PRE = (
    'EEL 3111 Circuit Analysis I (UNF). An upper-division engineering elective: UNF\'s engineering majors are '
    'selective-admission, with a C or higher required in engineering prerequisites. The same course is listed as '
    'EML 4328C for mechanical engineering; do not take both for credit.')

ETS4543C_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>ETS4543C</strong> <em>Applied Programmable Logic Controllers</em> is an upper-division, integrated '
    'lecture-and-laboratory course at the <strong>University of North Florida</strong> (3 credits), its only carrier. '
    'It is taught by UNF\'s School of Engineering and listed as a technical elective in the <strong>Advanced '
    'Manufacturing Engineering B.S.</strong>. UNF\'s 2026&ndash;27 catalogue:</p>'
    '<p><em>' + UNF_DESC + '</em></p>'
    '<p>Unlike a two-year PLC course, which centres on ladder logic and wiring, this engineering course pairs the PLC '
    'with the <strong>sensors, actuators and control strategies</strong> (on/off and PID) of a manufacturing process, '
    'and assumes a circuits course. The same course is listed as <strong>EML4328C</strong> for mechanical engineering '
    '(see Special Information).</p>'
    + UNF_OUT + UNF_TOP
    + '<h2>Resources &amp; Tools</h2>' + UNF_RES
    + '<h2>Career Pathways</h2>' + UNF_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One carrier: the University of North Florida, 3 credits</strong>, new in the state file in 2024. UNF '
    'publishes no contact-hour figure; the 60 shown are derived from Florida\'s convention for a 3-credit integrated '
    'lecture-and-laboratory course.</p>'
    + UNF_TWO + UNF_FE + AI_PLC)

ETS4543C = {
    'title': 'Applied Programmable Logic Controllers',
    'html_content': ETS4543C_HTML,
    'credits': 3,
    'contact_hours': 60,
    'prerequisites': ETS4543C_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One carrier, the University of North Florida, at 3 credits. Same course as UNF\'s EML4328C.',
        'hours_source': 'derived',
        'derived_contact_hours': 60,
        'derivation': DERIVED_C,
        'offerings': [
            off('UNF', UNF, 'Applied Programmable Logic Controllers', 3,
                'Electrical Engineering department. Prerequisite EEL 3111. Technical elective in the Advanced '
                'Manufacturing Engineering B.S. Same description as EML 4328C.')],
    },
}

EML4328C_PRE = (
    'EEL 3111 Circuit Analysis I (UNF). An upper-division mechanical engineering elective: UNF\'s engineering majors '
    'are selective-admission, with a C or higher required in engineering prerequisites. The same course is listed as '
    'ETS 4543C; do not take both for credit.')

EML4328C_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>EML4328C</strong> <em>Applied Programmable Logic Controllers for ME</em> is an upper-division, '
    'integrated lecture-and-laboratory course in the Mechanical Engineering department of the <strong>University of '
    'North Florida</strong> (3 credits), its only carrier. UNF\'s 2026&ndash;27 catalogue:</p>'
    '<p><em>' + UNF_DESC + '</em></p>'
    '<p>For a mechanical engineer this is the bridge between the machine and the computer that runs it: the '
    '<strong>sensors, actuators, motion, temperature and pressure control</strong> of a manufacturing process, '
    'on/off and PID control, and enough PLC programming to make real hardware do a job. It assumes a circuits course. '
    'The same course is listed as <strong>ETS4543C</strong> by UNF\'s Electrical Engineering department (see '
    'Special Information).</p>'
    + UNF_OUT + UNF_TOP
    + '<h2>Resources &amp; Tools</h2>' + UNF_RES
    + '<h2>Career Pathways</h2>' + UNF_CAREERS
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One carrier: the University of North Florida, 3 credits</strong>, new in the state file in 2024. UNF '
    'publishes no contact-hour figure; the 60 shown are derived from Florida\'s convention for a 3-credit integrated '
    'lecture-and-laboratory course.</p>'
    + UNF_TWO
    + '<h3>Related courses</h3>'
    '<p>No other Florida university carries a PLC course under an EML number; mechanical engineers elsewhere usually '
    'meet PLCs, if at all, inside a mechatronics, measurements or controls course. If you transfer, bring this '
    'course\'s syllabus: the number has no statewide equivalent, so the receiving department will judge it by '
    'content.</p>'
    + UNF_FE + AI_PLC)

EML4328C = {
    'title': 'Applied Programmable Logic Controllers for Mechanical Engineering',
    'html_content': EML4328C_HTML,
    'credits': 3,
    'contact_hours': 60,
    'prerequisites': EML4328C_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One carrier, the University of North Florida, at 3 credits. Same course as UNF\'s ETS4543C.',
        'hours_source': 'derived',
        'derived_contact_hours': 60,
        'derivation': DERIVED_C,
        'offerings': [
            off('UNF', UNF, 'Applied Programmable Logic Controllers for ME', 3,
                'Mechanical Engineering department. Prerequisite EEL 3111. Same description as ETS 4543C.')],
    },
}

# ---------------------------------------------------------------------------------------------
# ECH3702 Instrument Systems I (USF)
# ---------------------------------------------------------------------------------------------
ECH3702_PRE = (
    'USF: MAP 2302 Differential Equations or EGN 3433 Modeling and Analysis of Engineering Systems, AND EGN 3343 '
    'Thermodynamics I, AND ECH 3023 Material and Energy Balances. ⚠ USF\'s department course schedule does not list '
    'it and the state course file ends USF\'s offering on 1 August 2027; ask the department whether it will run '
    'before you plan on it.')

ECH3702_HTML = (
    '<h2>Course Description</h2>'
    '<p><strong>ECH3702</strong> is an electrical-and-instrumentation course for chemical engineering students at the '
    '<strong>University of South Florida</strong>, its only Florida carrier (3 credits; USF titles it <em>Instrument '
    'Systems I</em>, the state file <em>Instrument Systems</em>). USF\'s catalogue description in full: <em>"Basic '
    'concepts of electric circuits and their applications. Resistors, capacitors, inductors, logic operations, '
    'junction devices. Programmable Logic controllers, ladder diagrams."</em></p>'
    '<p>It gives a chemical engineer the electrical background to understand how a plant is measured and controlled: '
    'circuits, the components inside sensors and signal conditioners, digital logic, and the <strong>programmable '
    'logic controllers</strong> that run discrete steps in a process (valves, pumps, interlocks and batch sequences). '
    'It is taught by the Department of Chemical, Biological and Materials Engineering, after material and energy '
    'balances and thermodynamics, and comes before process dynamics and control.</p>'
    '<p>⚠ <strong>Check that it is offered.</strong> The department\'s current program-of-study list does not '
    'include it, and the state course file records USF\'s offering as ending on 1 August 2027. A guide is published '
    'because the course is in USF\'s catalogue and was requested; see Special Information.</p>'
    + sec('Learning Outcomes', [
        'Analyse DC circuits with Ohm\'s and Kirchhoff\'s laws, series and parallel combinations, and power.',
        'Describe how <strong>resistors, capacitors and inductors</strong> store and dissipate energy, and analyse '
        'simple time-dependent (RC, RL) and AC circuits.',
        'Explain how <strong>junction devices</strong> (diodes and transistors) work and where they appear in '
        'instruments and power supplies.',
        'Use <strong>logic operations</strong> (AND, OR, NOT; truth tables; Boolean algebra) to describe control '
        'decisions.',
        'Read and write <strong>ladder diagrams</strong>, and explain how a <strong>PLC</strong> executes them to '
        'run valves, pumps, motors and interlocks in a process plant.',
        'Connect these ideas to process instrumentation: how a sensor\'s signal becomes a number a controller can '
        'use.'],
        ['Use operational amplifiers for signal conditioning.',
         'Describe 4&ndash;20 mA current loops and analog-to-digital conversion.',
         'Read a piping and instrumentation diagram (P&amp;ID) and its ISA-5.1 symbols.'])
    + sec('Major Topics', [
        'Charge, current, voltage, power; Ohm\'s and Kirchhoff\'s laws.',
        'Resistive circuits and network analysis.',
        'Capacitors and inductors; transient and AC behaviour.',
        'Semiconductor junction devices: diodes and transistors.',
        'Digital logic: logic operations, truth tables, Boolean algebra.',
        'Programmable logic controllers and ladder diagrams.'],
        ['Op-amps and signal conditioning.', 'Sensors and transducers for temperature, pressure, flow and level.',
         'Process safety interlocks.'])
    + '<h2>Resources &amp; Tools</h2>'
    + ul('An introductory electrical engineering text for non-majors, such as <em>Electrical Engineering: Principles '
         'and Applications</em>, Allan R. Hambley (Pearson), which also covers digital logic and PLCs.',
         'A circuit simulator: LTspice (free) or Multisim.',
         'A PLC simulator or trainer for ladder diagrams.',
         'ISA-5.1 (instrumentation symbols) and an introductory process-control text for the plant context.')
    + '<h2>Career Pathways</h2>'
    + ul('<strong>Chemical engineers</strong> (SOC 17-2041) in process and plant engineering, where reading '
         'instrumentation and control logic is part of the job.',
         '<strong>Process control and automation engineers</strong> in chemical, pharmaceutical, food and '
         'semiconductor plants.',
         'Florida employers include phosphate and fertiliser processing in Polk and Hillsborough counties, power '
         'generation, water and wastewater treatment, pharmaceuticals and specialty chemicals, and food and '
         'beverage manufacturing.')
    + '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<p><strong>One carrier: the University of South Florida, 3 credits</strong>, in the state file since 2005. USF '
    'publishes no contact-hour figure; the 45 shown are derived from Florida\'s convention of 15 per credit.</p>'
    '<h3>⚠ Is it still taught?</h3>'
    '<p>Three facts, read together: USF\'s catalogue page for ECH 3702 is current (with prerequisites); the '
    'department\'s program-of-study page, which lists every course it schedules and the terms, does <strong>not</strong> '
    'include it; and the state course file records USF\'s offering as <strong>discontinued effective 1 August '
    '2027</strong>. Chemical engineering students at USF now meet circuits through the curriculum the department '
    'lists, and process control in <strong>ECH 4323 Process Dynamics and Control</strong>. If you need this course, '
    'ask the department before planning a term around it.</p>'
    '<h3>Transfer</h3>'
    '<p>No other Florida institution carries ECH3702. Chemical engineering programmes elsewhere cover the same '
    'ground in an electrical engineering service course (for example EEL3003 at UF, FAMU and FSU) and in process '
    'control (ECH4323 at FAMU, FSU, UF and USF). Bring the syllabus if you transfer.</p>'
    '<h3>FE exam</h3>'
    '<p>The FE Chemical exam includes <strong>process control</strong> and <strong>instrumentation</strong>; the '
    'circuits and logic here are background for it rather than a large share of it.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can explain a circuit law, check algebra and describe a ladder rung in words. They make '
    'characteristic errors in this material: wrong sign conventions, mixed-up peak and RMS values, answers without '
    'units, and ladder logic that ignores how a PLC scans or how a fail-safe valve is wired. <strong>Check every '
    'answer with units and a simulation, and learn to solve by hand &mdash; exams and the FE are taken without the '
    'tool.</strong> In a plant, interlock logic is safety-critical and is reviewed by people; it is never accepted '
    'because a tool wrote it. Follow your instructor\'s policy on AI use.</p>')

ECH3702 = {
    'title': 'Instrument Systems I',
    'html_content': ECH3702_HTML,
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': ECH3702_PRE,
    'version': '1.0',
    'offering_notes': {
        'summary': 'One carrier, the University of South Florida, at 3 credits. The state file ends USF\'s offering '
                   'on 1 August 2027, and the department\'s program-of-study page does not list it.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': DERIVED,
        'offerings': [
            off('USF', USF, 'Instrument Systems I', 3,
                'Prerequisites MAP 2302 or EGN 3433, EGN 3343 and ECH 3023. SCNS discontinuation date 2027-08-01.')],
    },
}

ALL = (('ETS1542', ETS1542), ('ETS2542', ETS2542), ('ETS2544', ETS2544), ('ETS4543C', ETS4543C),
       ('EML4328C', EML4328C), ('ECH3702', ECH3702))

for cid, g in ALL:
    path = os.path.join(DRAFTS, '%s_guide.json' % cid)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(g, fh, ensure_ascii=False, indent=1)
    print('wrote', cid, len(g['html_content']), 'chars; prereq', len(g['prerequisites']))
