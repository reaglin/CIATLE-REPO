# -*- coding: utf-8 -*-
"""Batch 256 (misc): limited-information guides for six requests previously held or declined
(Ron's rule of 2026-11-24: every requested course gets a guide). Run from Tools/.

  CET1112   NO PUBLIC CARRIER  only CBT Technology Institute (private); public colleges teach CET1112C.
  CET4668   RETIRED            Daytona State only; dropped from DSC's catalogue (site editor, 2026-10-02).
  EEL4016   RETIRED            FIU only; FIU Coursedog record: inactivated 28-JUL-2004.
  ETI0602   RETIRED            Manatee Technical College only; programme I150603 daggered 2023-24,
                               last reportable year 2024-25 (CPALMS, cached row + REVIEW_QUEUE 125).
  EUH6612   LIMITED INFORMATION UF only, graduate, 4 cr; not found in UF's current graduate catalogue.
  DIG2040C  LIMITED INFORMATION Florida Gateway only; statewide title Survey of Game Development.

Sources: SCNS flat file (crslist.txt, Sep 2025) for carriers, titles, credits, clock hours, dates;
fiu_courses.json (FIU Coursedog) for EEL4015/EEL4016; cpalms_programs.json for I150603;
floridacourserepo.com API for every linked course and career path (checked 2026-11-24).
Outside links fetched 2026-11-24: IU Bloomington MSCH-C 215, George Mason GAME 230,
CUNY Graduate Center HIST 70540, Queens College HIST 734, MIT OCW 6.858.
"""
import io
import json
import os

LG = '<ul class="list-group list-group-flush">'
SITE = 'https://floridacourserepo.com'


def li(items):
    return LG + ''.join('<li class="list-group-item">%s</li>' % x for x in items) + '</ul>'


def ul(items):
    return '<ul>' + ''.join('<li>%s</li>' % x for x in items) + '</ul>'


def c(cid, title=None):
    t = '%s %s' % (cid, title) if title else cid
    return '<a href="%s/courses/%s">%s</a>' % (SITE, cid, t)


def path(slug, title):
    return '<a href="%s/careers/%s">%s</a>' % (SITE, slug, title)


def ext(url, text):
    return '<a href="%s">%s</a>' % (url, text)


def table(rows):
    h = ('<table class="table table-sm"><thead><tr><th>Institution</th><th>Title</th><th>Credits</th>'
         '<th>Contact hours</th></tr></thead><tbody>')
    return h + ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % x for x in r) for r in rows) + '</tbody></table>'


G = {}

# ---------------------------------------------------------------- CET1112 (no public carrier)
G['CET1112'] = {
    'title': 'Digital Electronics & Microprocessors (no public carrier — see CET1112C)',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "No Florida public college or university carries CET1112. The only institution listing it is a private "
        "career college, CBT Technology Institute, which sets its own admission and prerequisites. At Florida's "
        "public colleges the subject is taught as CET1112C (integrated lecture and laboratory, 3 credits), whose "
        "prerequisites are set by each college, commonly a DC/AC circuits course and college-level mathematics."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'No Florida public institution carries CET1112. The only active record is at CBT Technology '
                   'Institute (private, 3 credits), which is outside the public-only offering list. Daytona State '
                   'College once listed CET1112 Digital Fundamentals; that record was discontinued in 2016. Five '
                   'public colleges teach the subject as CET1112C.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': 'No contact hours are published; 45 is Florida\'s convention for a 3-credit lecture course '
                      '(the bare number, without the C, is the lecture-only form).',
        'offerings': [],
    },
}
G['CET1112']['html_content'] = (
    "<h2>Course Description</h2>"
    "<div class=\"alert alert-warning\"><strong>No public carrier.</strong> No Florida public college or "
    "university offers CET1112. The only institution that lists the number is a private career college. Florida's "
    "public colleges teach this subject as <strong>" + c('CET1112C') + "</strong>, which has its own full guide. "
    "This page says what the record shows and points you there; it describes nothing about the private "
    "institution's course beyond its title and credits.</div>"
    "<p>The statewide course record for CET1112 is <strong>Digital Fundamentals (digital codes, logic circuits, "
    "Boolean algebra)</strong>. The only active listing is at <strong>CBT Technology Institute</strong>, a private "
    "institution, under the title <em>Digital Electronics &amp; Microprocessors</em> at 3 credits; this site's "
    "course title came from that listing. Daytona State College once carried a CET1112 <em>Digital "
    "Fundamentals</em>, but that record was discontinued in 2016.</p>"
    "<p>The number without a suffix is the lecture-only form. The <strong>C</strong> in CET1112C marks an "
    "integrated lecture and laboratory course, and that is the form Florida's public colleges use: Daytona State, "
    "Gulf Coast State, Hillsborough, Indian River State and Pensacola State all carry CET1112C at 3 credits. A "
    "digital course without bench work does not prepare a student for the microprocessor and troubleshooting "
    "courses that follow, so a receiving programme may ask whether a CET1112 course included laboratory hours.</p>"
    "<h2>Learning Outcomes</h2>"
    "<p>The statewide title fixes the subject; the outcomes below are only what that title makes certain. For the "
    "full set taught at Florida's public colleges, see the " + c('CET1112C') + " guide.</p>"
    "<h3>Required Outcomes</h3>" + li([
        "Convert between binary, octal, hexadecimal and decimal number systems and use common digital codes such as "
        "BCD and ASCII.",
        "Describe the logic gates and write their truth tables.",
        "Simplify logic expressions with <strong>Boolean algebra</strong> and Karnaugh maps.",
        "Analyse and design simple combinational logic circuits.",
    ]) +
    "<h3>Optional Outcomes</h3>" + li([
        "Describe flip-flops, counters and registers (sequential logic), commonly covered in a digital fundamentals "
        "course.",
        "Describe the parts of a microprocessor system, as the private carrier's title suggests; at public colleges "
        "this is the subject of a separate course such as " + c('CET2123C', 'Microprocessors') + ".",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>" + li([
        "Number systems and codes.",
        "Logic gates and truth tables.",
        "Boolean algebra, De Morgan's theorems, Karnaugh maps.",
        "Combinational logic circuits.",
    ]) +
    "<h3>Optional Topics</h3>" + li([
        "Sequential logic: latches, flip-flops, counters, shift registers.",
        "Introduction to microprocessors.",
    ]) +
    "<h2>Career Pathways</h2>" + ul([
        "Electronics engineering technicians (SOC 17-3023): see the " +
        path('electronics-engineering-technician', 'Electronics Engineering Technician') + " career path.",
    ]) +
    "<h2>Where to Learn More</h2>" + ul([
        c('CET1112C', 'Digital and Computer Circuits') + " — the course Florida's public colleges teach, with a full "
        "guide and each college's own title.",
        c('CET2112C', 'Digital Systems I') + " — Valencia College's digital course under another number.",
        c('CET2123C', 'Microprocessors') + " — the microprocessor course that usually follows digital fundamentals "
        "(six public colleges).",
        path('electronics-engineering-technician', 'Electronics Engineering Technician') + " — the career path these "
        "courses lead to.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>"
    "<p>No Florida public institution carries CET1112, so there is no public offering to list. The only active "
    "record is CBT Technology Institute (private), <em>Digital Electronics &amp; Microprocessors</em>, 3 credits. "
    "The 45 contact hours at the top of this page are Florida's convention for a 3-credit lecture course, not a "
    "published figure.</p>"
    "<h3>Transfer</h3><p>Credit from a private institution is accepted at a public college under the "
    "receiving institution's own transfer rules. If you hold CET1112 credit, keep the syllabus and ask the "
    "receiving programme in writing whether it counts for CET1112C, and whether laboratory hours are needed.</p>"
)

# ---------------------------------------------------------------- CET4668 (retired)
G['CET4668'] = {
    'title': 'Practice of Information Security (retired — see CET4663)',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "The course is no longer offered. Daytona State College, the only Florida public institution with the number, "
        "has dropped it from its catalogue. The statewide course record named CET4663 Computer and Network Security "
        "as its prerequisite; CET4663 is still taught (Valencia College, and as CET4663C at Miami Dade College)."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'Retired. Daytona State College, the only public carrier, has dropped CET4668 from its '
                   'catalogue, although the SCNS file (September 2025) still lists it as active at 3 credits '
                   '(effective 2010). UCF also listed it briefly (2010-2011, discontinued).',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': 'No contact hours were published; 45 is Florida\'s convention for a 3-credit lecture course.',
        'offerings': [{
            'institution': 'DSC', 'institution_name': 'Daytona State College',
            'title': 'Practice of Information Security', 'credits': 3, 'contact_hours': None,
            'note': 'No longer in Daytona State\'s catalogue (confirmed by the site editor, 2026-10-02); still '
                    'active in the SCNS file.'}],
    },
}
G['CET4668']['html_content'] = (
    "<h2>Course Description</h2>"
    "<div class=\"alert alert-warning\"><strong>Retired course.</strong> No Florida public college or university "
    "teaches CET4668 today. <em>Daytona State College</em>, the only one that listed it, has dropped it from its "
    "catalogue. If you want this subject, take <strong>" + c('CET4663', 'Computer and Network Security') +
    "</strong> or one of the courses listed under Where to Learn More.</div>"
    "<p><strong>CET4668 Practice of Information Security</strong> was an upper-division (3 credits) course in the "
    "computer engineering technology prefix. The statewide course record names <strong>CET4663 Computer and "
    "Network Security</strong> as its prerequisite, so it was the applied, second course in a two-course security "
    "sequence for engineering technology students. Daytona State College carried it from 2010, and the University "
    "of Central Florida listed it briefly from 2010 to 2011.</p>"
    "<p>The state's course file still shows Daytona State's record as active, but the course is no longer in "
    "Daytona State's catalogue. No description of what it taught is published, so this guide does not set out "
    "outcomes or topics for it. The courses below teach the subject today.</p>"
    "<h2>Learning Outcomes</h2>"
    "<p>No current outcomes are published for this retired course. For outcomes in this subject, see the "
    + c('CET4663') + " guide (computer and network security for engineering technology students) and the "
    + c('CIS4361') + " guide (information security at seven public institutions).</p>"
    "<h2>Major Topics</h2>"
    "<p>From the title and its place after CET4663, the course applied security principles in practice. Its "
    "published topics are not available; see the replacement courses' guides.</p>"
    "<h2>Career Pathways</h2>" + ul([
        "Information security analysts (SOC 15-1212) and related roles: see the " +
        path('cybersecurity-analyst', 'Cybersecurity Analyst') + " career path, which explains that this is not an "
        "entry-level field and that experience and certifications carry a lot of weight.",
    ]) +
    "<h2>Where to Learn More</h2>" + ul([
        c('CET4663', 'Computer and Network Security') + " — the course that came before CET4668, still taught at "
        "Valencia College (3 credits, with a full guide).",
        c('CET4663C', 'Electronic Security') + " — Miami Dade College's version of CET4663, with an integrated lab.",
        c('CIS4361', 'Applied Security') + " — the upper-division information security course at seven Florida "
        "public institutions.",
        c('CTS1120', 'Fundamentals of Cybersecurity') + " — a lower-division starting point.",
        path('cybersecurity-analyst', 'Cybersecurity Analyst') + " — the career path, with Florida programmes.",
        ext('https://ocw.mit.edu/courses/6-858-computer-systems-security-fall-2014/',
            'MIT OpenCourseWare 6.858 Computer Systems Security') + " — free lecture videos, notes, labs and exams "
        "from MIT's graduate course on attacks, threat models and defences (more advanced than CET4668).",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>" + table([
        ['Daytona State College', 'Practice of Information Security', '3',
         'not published (45 by Florida\'s convention); no longer in the catalogue'],
    ]) +
    "<h3>If you have CET4668 on a transcript</h3><p>Credit already earned stays on your transcript. If a programme "
    "asks how it counts, give it the syllabus from the term you took it and point to CET4663 or CIS4361 as the "
    "nearest current courses.</p>"
)

# ---------------------------------------------------------------- EEL4016 (retired)
G['EEL4016'] = {
    'title': 'Electrical Design in Building II (retired — see EEL4015)',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "The course is no longer offered. Florida International University, the only Florida public institution "
        "with the number, inactivated it in 2004. Its first half, EEL4015 Electrical Design in Buildings I, is "
        "still taught at FIU; check FIU's catalogue for that course's prerequisites."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'Retired. FIU, the only carrier, inactivated EEL4016 in 2004 (its own catalogue record: '
                   '"Cleanup of Course Catalog occurred on 28-JUL-2004. Course was inactivated."). The SCNS file '
                   '(September 2025) still lists it as active at 3 credits.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': 'No contact hours were published; 45 is Florida\'s convention for a 3-credit lecture course.',
        'offerings': [{
            'institution': 'FIU', 'institution_name': 'Florida International University',
            'title': 'Electrical Design in Building II', 'credits': 3, 'contact_hours': None,
            'note': 'Inactive in FIU\'s catalogue since 2004; still active in the SCNS file. Statewide title: '
                    'Electrical Design II.'}],
    },
}
G['EEL4016']['html_content'] = (
    "<h2>Course Description</h2>"
    "<div class=\"alert alert-warning\"><strong>Retired course.</strong> No Florida public college or university "
    "teaches EEL4016 today. <em>Florida International University</em>, the only one that listed it, retired it in "
    "2004. Its first half, <strong>" + c('EEL4015', 'Electrical Design in Buildings I') + "</strong>, is still "
    "taught at FIU.</div>"
    "<p><strong>EEL4016 Electrical Design in Building II</strong> was the second of a two-course sequence in "
    "building electrical design in FIU's Department of Electrical and Computer Engineering (3 credits; statewide "
    "title <em>Electrical Design II</em>). FIU's own catalogue record for it reads: <em>Cleanup of Course Catalog "
    "occurred on 28-JUL-2004. Course was inactivated.</em> The state's course file still lists the number as "
    "active, which is why it appears on this site.</p>"
    "<p>The first course, EEL4015, remains active at FIU, typically offered in spring and fall, and FIU describes "
    "it this way: <em>Application of electrical codes and regulations. Design of loads, circuits, surge "
    "protectors, feeders, panels, and breakers.</em> No description of the retired second course survives, so this "
    "guide does not set out outcomes or topics for it.</p>"
    "<h2>Learning Outcomes</h2>"
    "<p>No outcomes are published for this retired course. For building electrical design today, take EEL4015 at "
    "FIU.</p>"
    "<h2>Major Topics</h2>"
    "<p>Not published. The surviving first course covers electrical codes and regulations and the design of loads, "
    "circuits, surge protection, feeders, panels and breakers.</p>"
    "<h2>Career Pathways</h2>" + ul([
        "Electrical engineers (SOC 17-2071), including those who design power systems for buildings: see the " +
        path('electrical-engineer', 'Electrical Engineer') + " career path.",
    ]) +
    "<h2>Where to Learn More</h2>" + ul([
        c('EEL4015', 'Electrical Design in Buildings I') + " — FIU's surviving building electrical design course.",
        path('electrical-engineer', 'Electrical Engineer') + " — the career path, with Florida programmes and "
        "licensure.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>" + table([
        ['Florida International University', 'Electrical Design in Building II', '3',
         'not published (45 by Florida\'s convention); inactive since 2004'],
    ]) +
    "<h3>If you have EEL4016 on a transcript</h3><p>Credit earned before 2004 stays on your transcript. If a "
    "programme or licensing board asks what it covered, the course syllabus from that time is the only "
    "evidence; FIU's Department of Electrical and Computer Engineering may be able to help.</p>"
)

# ---------------------------------------------------------------- ETI0602 (retired, PSAV)
G['ETI0602'] = {
    'title': 'Industrial Technician Assistant 1 (retired programme)',
    'credits': 0,
    'contact_hours': 250,
    'prerequisites': (
        "The course belonged to Florida's Industrial Technology career certificate programme (I150603), which the "
        "state ended: it was marked for deletion in 2023-24 and 2024-25 was its last reportable year. Manatee "
        "Technical College, the only carrier, no longer lists the programme. It was occupational completion point C "
        "of the programme, after ETI0600 Drafting Assistant Machining and ETI0601 Cost Control Assistant, and was "
        "followed by ETI0603 Industrial Technician Assistant 2. It is a 250-clock-hour course with no college credit."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'Retired. One public institution carried ETI0602: Manatee Technical College, a district technical '
                   'college, at 250 clock hours (no credit). Its programme, Industrial Technology (I150603), was '
                   'daggered in 2023-24 with 2024-25 its last reportable year, and Manatee Technical College no '
                   'longer lists it. The SCNS file (September 2025) still shows the course as active.',
        'hours_source': 'published',
        'derived_contact_hours': None,
        'derivation': None,
        'offerings': [{
            'institution': 'MTI', 'institution_name': 'Manatee Technical College',
            'title': 'Industrial Technician Assistant 1', 'credits': 0, 'contact_hours': 250,
            'note': 'Clock-hour course, OCP C (1 of 2) of Industrial Technology I150603. Programme ended after '
                    '2024-25; no longer listed by the college.'}],
    },
}
G['ETI0602']['html_content'] = (
    "<h2>Course Description</h2>"
    "<div class=\"alert alert-warning\"><strong>Retired course.</strong> Florida ended the <em>Industrial "
    "Technology</em> career certificate programme this course belonged to: it was marked for deletion in 2023-24, "
    "and 2024-25 was its last reportable year. <em>Manatee Technical College</em>, the only school that offered "
    "ETI0602, no longer lists the programme. For manufacturing training today, see Where to Learn More.</div>"
    "<p><strong>ETI0602 Industrial Technician Assistant 1</strong> was a 250-clock-hour course in a Florida "
    "postsecondary career certificate programme (a clock-hour programme, so it carries no college credit). The "
    "programme, <strong>Industrial Technology</strong> (programme number I150603, federal CIP 15.0612), ran "
    "1,600 hours in four occupational completion points:</p>"
    "<table class=\"table table-sm\"><thead><tr><th>Point</th><th>Course</th><th>Hours</th></tr></thead><tbody>"
    "<tr><td>A</td><td>ETI0600 Drafting Assistant Machining</td><td>300</td></tr>"
    "<tr><td>B</td><td>ETI0601 Cost Control Assistant</td><td>300</td></tr>"
    "<tr><td>C</td><td><strong>ETI0602 Industrial Technician Assistant 1</strong>; " + c('ETI0603') +
    " Industrial Technician Assistant 2</td><td>250 + 250</td></tr>"
    "<tr><td>D</td><td>ETI0604 and ETI0605 Industrial Engineering Technician 1 and 2</td><td>250 + 250</td></tr>"
    "</tbody></table>"
    "<p>The state framework gave ETI0602 one standard, <em>Identify manufacturing control procedures</em>. It named "
    "no industry certification and no occupation codes for it. The state's course file still lists the course as "
    "active at Manatee Technical College, which is why it appears on this site.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>" + li([
        "Identify manufacturing control procedures (the framework's only standard for this course).",
    ]) +
    "<h2>Major Topics</h2>"
    "<p>The framework's benchmarks under that standard are not reproduced here; the programme has ended. The "
    "replacement courses below each have a full guide.</p>"
    "<h2>Career Pathways</h2>" + ul([
        "Industrial engineering technicians (SOC 17-3026), the work of process, quality data and production "
        "control that this programme pointed toward: see the " +
        path('industrial-engineering-technician', 'Industrial Engineering Technician') + " career path.",
        "Production technicians and assemblers (SOC 51-2092): see the " +
        path('production-technician', 'Production Technician and Assembler') + " career path.",
        "Industrial maintenance technicians (SOC 49-9041): see the " +
        path('industrial-maintenance-technician', 'Industrial Maintenance Technician') + " career path.",
    ]) +
    "<h2>Where to Learn More</h2>"
    "<p>Florida's technical colleges still teach manufacturing in clock-hour courses. These are on this site with "
    "guides:</p>" + ul([
        c('ETI0481', 'Production Worker') + " — 150 hours, at Manatee Technical College and three other technical "
        "colleges.",
        c('ETI0482', 'Assembler') + " — 150 hours.",
        c('ETI0484', 'Process Assistant') + " — 150 hours.",
        c('ETI0485', 'Automation and Production Technology') + " — 150 hours.",
        c('ETI1110', 'Introduction to Quality Assurance') + " — a college-credit course on quality, taught at about "
        "16 Florida colleges.",
        path('industrial-engineering-technician', 'Industrial Engineering Technician') + ", " +
        path('production-technician', 'Production Technician and Assembler') + " and " +
        path('industrial-maintenance-technician', 'Industrial Maintenance Technician') + " — career paths with "
        "the Florida programmes that lead to each.",
    ]) +
    "<p>The state's current manufacturing frameworks include a newer clock-hour <em>Industrial Engineering "
    "Technology</em> career certificate (J200500, introduced 2025) in the same federal CIP group; ask a technical "
    "college whether it offers it.</p>"
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>" + table([
        ['Manatee Technical College', 'Industrial Technician Assistant 1', '0 (clock-hour course)',
         '250; programme ended after 2024-25'],
    ]) +
    "<h3>Teach-out and completed hours</h3><p>A student who completed ETI0602 before the programme ended keeps the "
    "occupational completion point on their record. A student partway through should ask Manatee Technical "
    "College how its hours can count toward a current programme. Clock-hour courses do not carry college credit; "
    "some state colleges award credit for a completed career certificate under the state's articulation "
    "agreements, so ask the college you are going to.</p>"
)

# ---------------------------------------------------------------- EUH6612 (limited information)
G['EUH6612'] = {
    'title': 'Gender and Power in Europe & Mediterranean',
    'credits': 4,
    'contact_hours': 60,
    'prerequisites': (
        "A graduate course at the University of Florida, the only Florida public institution that lists it. UF "
        "publishes no current prerequisite for it, and the course was not found in UF's current graduate catalogue. "
        "Graduate history courses normally require admission to a graduate programme or the instructor's permission; "
        "check with UF's Department of History."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries EUH6612: the University of Florida, at 4 credits, '
                   'graduate. The SCNS record dates from 1997 (changed 2005); the course was not found in UF\'s '
                   'current graduate catalogue and may be dormant.',
        'hours_source': 'derived',
        'derived_contact_hours': 60,
        'derivation': 'UF publishes no contact hours; 60 is Florida\'s 15-hours-per-credit convention for a '
                      '4-credit course.',
        'offerings': [{
            'institution': 'UF', 'institution_name': 'University of Florida',
            'title': 'Gender and Power in Europe & Mediterranean', 'credits': 4, 'contact_hours': None,
            'note': 'Graduate. Statewide title: Gender and Power in the West (Graduate). Not found in UF\'s current '
                    'graduate catalogue or in the History Department\'s graduate listings for Fall 2020 to Fall '
                    '2022.'}],
    },
}
G['EUH6612']['html_content'] = (
    "<h2>Course Description</h2>"
    "<div class=\"alert alert-warning\"><strong>Limited information.</strong> Only the <em>University of "
    "Florida</em> offers EUH6612 in Florida's public colleges and universities, and it publishes only a title and "
    "credits. The course was not found in UF's current graduate catalogue, so it may not have been taught for some "
    "years. This guide sets out what the record shows and what a graduate course of this kind commonly covers. "
    "Check with UF's Department of History before relying on it.</div>"
    "<p><strong>EUH6612 Gender and Power in Europe &amp; Mediterranean</strong> is a graduate history course (4 "
    "credits) in the European history prefix. The statewide course record titles it <strong>Gender and Power in "
    "the West (Graduate)</strong>; UF's title narrows that to Europe and the Mediterranean. The record dates from "
    "1997 and was last changed in 2005. UF's course search returned no current section, and the History "
    "Department's graduate course listings for Fall 2020 to Fall 2022 do not show it.</p>"
    "<p>A graduate seminar with this title commonly studies how gender has shaped, and been shaped by, power in "
    "European and Mediterranean societies: who held authority in households, churches, courts and states, how "
    "ideas of masculinity and femininity were made and enforced, and how historians have used gender as a "
    "category of analysis. The period covered depends on the instructor; the items below are labelled "
    "accordingly.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>" + li([
        "Analyse the relationship between gender and power in European and Mediterranean history.",
        "Read and assess the historiography of gender: how historians have used gender as a category of analysis.",
        "Write graduate-level historical analysis grounded in primary and secondary sources.",
    ]) +
    "<h3>Optional Outcomes</h3>" + li([
        "Compare gender and authority across Christian, Jewish and Muslim societies of the Mediterranean "
        "(commonly covered where the course takes the Mediterranean frame).",
        "Lead a seminar discussion and produce a historiographical essay or research paper.",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>" + li([
        "Gender as a category of historical analysis.",
        "Gender, family and household authority.",
        "Gender, law and the state.",
    ]) +
    "<h3>Optional Topics</h3>" + li([
        "Religion, gender and power (commonly covered).",
        "Sexuality, honour and the body (commonly covered).",
        "Gender in ancient, medieval, early modern or modern Europe, as the instructor chooses.",
    ]) +
    "<h2>Where to Learn More</h2>"
    "<p>Florida courses on this site in the same subject:</p>" + ul([
        c('EUH4610', 'Women and Gender in Europe, 1750–Present') + " — upper-division, at FIU, UCF and UF.",
        c('EUH5178', 'Medieval Women') + " — a graduate course at the University of West Florida.",
    ]) +
    "<p>Similar courses outside Florida (each is <em>a similar course, not an equivalent for transfer</em>):</p>" + ul([
        ext('https://gc.catalog.cuny.edu/courses/1539571', 'HIST 70540 Premodern Gender and Sexuality') +
        " — The Graduate Center, City University of New York (3 credits): gender roles and sexuality from the "
        "ancient world through the Renaissance.",
        ext('https://qc-graduate.catalog.cuny.edu/courses/0098711', 'HIST 734 Women in Modern European History') +
        " — Queens College, City University of New York (3 credits): European women's history from the French "
        "Revolution to the 1980s.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>" + table([
        ['University of Florida', 'Gender and Power in Europe &amp; Mediterranean', '4',
         'not published (60 by Florida\'s 15-hours-per-credit convention)'],
    ]) +
    "<p>Graduate history seminars at UF are sometimes offered under a variable-topics number rather than a fixed one, "
    "so a course on this subject may run under another number in a given term. Ask the Department of History "
    "what is scheduled.</p>"
)

# ---------------------------------------------------------------- DIG2040C (limited information)
G['DIG2040C'] = {
    'title': 'History of Video Games',
    'credits': 3,
    'contact_hours': 60,
    'prerequisites': (
        "Florida Gateway College, the only Florida public carrier, sets the prerequisites; its catalogue could not "
        "be read for this guide, so check the current Florida Gateway catalogue. As a lower-division course it "
        "commonly has none beyond college admission. The statewide course record titles the number Survey of Game "
        "Development, so a receiving institution may read it as a game development course rather than a history "
        "course: keep the syllabus."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries DIG2040C: Florida Gateway College, at 3 credits '
                   '(effective 2015).',
        'hours_source': 'derived',
        'derived_contact_hours': 60,
        'derivation': 'Florida Gateway publishes no contact hours that could be read; 60 is Florida\'s convention '
                      'for a 3-credit integrated lecture-and-laboratory (C) course.',
        'offerings': [{
            'institution': 'FGC', 'institution_name': 'Florida Gateway College',
            'title': 'History of Video Games', 'credits': 3, 'contact_hours': None,
            'note': 'Statewide title: Survey of Game Development. Catalogue not readable for this guide.'}],
    },
}
G['DIG2040C']['html_content'] = (
    "<h2>Course Description</h2>"
    "<div class=\"alert alert-warning\"><strong>Limited information.</strong> Only <em>Florida Gateway "
    "College</em> offers DIG2040C in Florida's public colleges and universities, and its catalogue could not be "
    "read for this guide, so only the title and credits are confirmed. This guide sets out what the record shows "
    "and what a course of this kind commonly covers. Check the college's syllabus before relying on it.</div>"
    "<p><strong>DIG2040C</strong> is a lower-division digital media course (3 credits). Florida Gateway College "
    "titles it <strong>History of Video Games</strong> and has carried it since 2015. ⚠ The statewide course "
    "record titles the same number <strong>Survey of Game Development</strong>. The two names point to "
    "overlapping but different courses: a history of the medium, and a survey of how games are made and of the "
    "industry that makes them. Many courses do both, tracing how game design and technology developed over time. "
    "This guide covers both readings and labels each.</p>"
    "<p>The <strong>C</strong> suffix marks an integrated lecture-and-laboratory course, so students commonly "
    "play, analyse or build games as part of the work. Florida Gateway also carries "
    + c('DIG1711C', 'Game Design &amp; Gameplay') + " and DIG2721C (its title: <em>Applied Game Design I</em>).</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>" + li([
        "<em>Both readings:</em> describe the development of video games from early experiments through arcade, "
        "home console, personal computer, online and mobile games.",
        "<em>Both readings:</em> explain how changes in technology and platforms shaped the games that were made.",
        "<em>Both readings:</em> describe the structure of the game industry and the roles in a game "
        "development team.",
    ]) +
    "<h3>Optional Outcomes</h3>" + li([
        "<em>History reading:</em> analyse games as cultural works and discuss their social effects, including "
        "representation, violence, regulation and intellectual property (commonly covered).",
        "<em>Game development reading:</em> describe the stages of game production, from concept and design "
        "documents through prototyping, testing and release.",
        "<em>Game development reading:</em> build a simple game or prototype in a game engine (the C suffix makes "
        "hands-on work likely).",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>" + li([
        "Early computer and arcade games.",
        "Home consoles and the console generations.",
        "Personal computer gaming.",
        "Online, mobile and social games.",
        "The game industry: developers, publishers, platforms, roles.",
    ]) +
    "<h3>Optional Topics</h3>" + li([
        "<em>History reading:</em> games and society: ratings and regulation, representation, game criticism.",
        "<em>Game development reading:</em> the game development pipeline and game engines.",
        "<em>Game development reading:</em> genres and game design elements.",
    ]) +
    "<h2>Resources &amp; Tools</h2>" + ul([
        "A history of video games text. UCF's DIG 3043 Evolution of Video Games uses Charlie Fish, <em>The History "
        "of Video Games</em> (2021); Florida Gateway's syllabus names its own.",
        "Playable examples from different eras, through the college's lab or legal emulation and re-releases.",
    ]) +
    "<h2>Career Pathways</h2>" + ul([
        "Software developers (SOC 15-1252), including game programmers: see the " +
        path('software-developer', 'Software Developer') + " career path.",
        "Special effects artists and animators (SOC 27-1014), game designers, producers and testers. In Florida, "
        "game studios and simulation companies cluster in Central Florida.",
    ]) +
    "<h2>Where to Learn More</h2>"
    "<p>Florida courses on this site in the same subject:</p>" + ul([
        c('DIG3043', 'Evolution of Video Games') + " — upper-division, University of Central Florida.",
        c('SYP3323', 'Video Games in Society') + " — University of Central Florida.",
        c('AMH4641', 'Video Games and American History') + " — Florida Polytechnic and the University of West "
        "Florida (with a full guide).",
        c('DIG1711C', 'Game Design &amp; Gameplay') + " — Florida Gateway College.",
    ]) +
    "<p>Similar courses outside Florida (each is <em>a similar course, not an equivalent for transfer</em>):</p>" + ul([
        ext('https://academics.iu.edu/courses/bloomington/msch-c-215-history-of-videogames.html',
            'MSCH-C 215 History of Videogames') + " — Indiana University Bloomington (3 credits): the origin and "
        "development of the videogame, its platforms, social and cultural effects, and new gaming trends.",
        ext('https://cehd.gmu.edu/courses/GAME-230', 'GAME 230 History of Computer Game Design') + " — George Mason "
        "University (3 credits): the history of game design and the trends and constraints behind how game "
        "development evolved; close to both readings of this number.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>" + table([
        ['Florida Gateway College', 'History of Video Games', '3',
         'not published (60 by Florida\'s convention for a C course)'],
    ]) +
    "<h3>Transfer</h3><p>Because the statewide title is <em>Survey of Game Development</em>, a receiving "
    "institution may treat DIG2040C as a game development course. If you want it to count as a history or "
    "humanities course, keep the syllabus and ask the receiving department in writing.</p>"
)

for cid, g in G.items():
    order = ['title', 'html_content', 'credits', 'contact_hours', 'prerequisites', 'version', 'offering_notes']
    # CET1112 has no PUBLIC offering, and the validator refuses an empty offerings list,
    # so its offering_notes is left out (the HTML Offering Notes section says why).
    out = {k: g[k] for k in order if not (k == 'offering_notes' and not g[k]['offerings'])}
    p = os.path.join('drafts', '%s_guide.json' % cid)
    with io.open(p, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print(cid, 'html', len(out['html_content']), 'prereq', len(out['prerequisites']))

