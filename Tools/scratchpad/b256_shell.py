# -*- coding: utf-8 -*-
"""Batch 256: experiential / variable-content guides for nine shell numbers (run from Tools/).

Rule: Tools/CLAUDE.md, "EVERY REQUESTED COURSE GETS A GUIDE" (Ron, 2026-11-24): a guide to how this kind
of course works at the institution that carries it, not an invented syllabus.

Sources (each fetched and read 2026-11-24):
  SCNS flat file (scratchpad/crslist.txt): carriers, titles, credits, statewide titles.
  MDC ARH2990 competency sheet (Updated Fall 2023); MDC Museum Studies ATC page; MDC Museum Studies LibGuide co-op page.
  FAU Coursedog cache (scratchpad/fau_courses.json): ARH2957 description, 1-6 credits, H.L. Wilkes Honors College,
    repeatable, study-abroad attributes. FAU Honors College study abroad page; FAU Education Abroad page.
  GCSC catalogue SOW page (SOW 2949, 1-3 credits, prerequisites, AA cap); GCSC co-op page; GCSC Social Work AA page.
  UCF Experiential Learning overview (career.ucf.edu/el-overview/).
  UCF Burnett Honors College HUT Program Handbook (October 2025).
  UCF Undergraduate Curriculum Handbook v2.0 (Fall 2019): special-topics numbers by level, three offerings, syllabus.
  UCF CECS study abroad page; UCF Financial Aid study abroad page; UCF ECE undergraduate programs page.
  s. 1009.286 F.S. (excess hours, state universities, internship hours excluded); s. 435.04 F.S. (Level 2 screening).
  UCF Kuali catalogue search: none of the UCF numbers here is listed in the current online catalogue.
"""
import io
import json
import os

SITE = 'https://floridacourserepo.com/courses/'
EXCESS = 'http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=1000-1099/1009/Sections/1009.286.html'
SCREEN = 'https://www.flsenate.gov/Laws/Statutes/2025/435.04'
UCF_CURR = 'https://provost.ucf.edu/wp-content/uploads/sites/2/2021/04/Undergraduate-Curriculum-Handbook-Version-2.0.pdf'
UCF_HUT = 'https://honors.ucf.edu/wp-content/uploads/sites/6/2025/10/HUT-Handbook-2025.pdf'
UCF_ECE = 'https://www.ece.ucf.edu/undergraduate-programs/'
UCF_CECS_SA = 'https://www.cecs.ucf.edu/study-abroad-page/'
UCF_FA_SA = 'https://www.ucf.edu/financial-aid/apply/study-abroad/'
UCF_EL = 'https://career.ucf.edu/el-overview/'


def ul(items, group=True):
    if group:
        return '<ul class="list-group list-group-flush">' + ''.join(
            '<li class="list-group-item">%s</li>' % i for i in items) + '</ul>'
    return '<ul>' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'


def a(url, text):
    return '<a href="%s">%s</a>' % (url, text)


def site(cid, title):
    return a(SITE + cid, '%s %s' % (cid, title))


def box(text):
    return '<div class="alert alert-warning"><strong>Variable-content course.</strong> %s</div>' % text


def table(rows):
    h = ('<table class="table table-sm"><thead><tr><th>Institution</th><th>Title</th><th>Credits</th>'
         '<th>Contact hours</th></tr></thead><tbody>')
    return h + ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % r for r in rows) + '</tbody></table>'


def sections(desc, req_out, opt_out, req_top, opt_top, how, careers, learn, special, ai=None):
    h = '<h2>Course Description</h2>' + desc
    h += '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>' + ul(req_out)
    h += '<h3>Optional Outcomes</h3>' + ul(opt_out)
    h += '<h2>Major Topics</h2><h3>Required Topics</h3>' + ul(req_top)
    h += '<h3>Optional Topics</h3>' + ul(opt_top)
    h += '<h2>How This Course Works</h2>' + how
    if careers:
        h += '<h2>Career Pathways</h2>' + ul(careers, False)
    h += '<h2>Where to Learn More</h2>' + ul(learn, False)
    h += '<h2>Special Information</h2>' + special
    if ai:
        h += '<h2>AI Integration (Optional)</h2>' + ai
    return h


UCF_VAR_NOTE = (
    "<p>UCF records the number in the statewide course inventory with a <strong>variable</strong> credit value "
    "(<em>VAR</em>), and UCF's current online catalogue does not list it: it is one of the reserved numbers UCF "
    "keeps in each prefix for work that is arranged section by section. The credit for a registration is set when "
    "the section is created. <strong>Ask what your registration is worth before you register.</strong> The figure "
    "of 3 credits and 45 hours on this page is a placeholder for one typical registration, not a published "
    "value.</p>")

TRANSFER_SHELL = (
    "<h3>Transfer</h3><p>A shell number transfers poorly. Statewide course numbering matches courses by content, "
    "and a number whose content changes from student to student has no fixed content to match, so a receiving "
    "institution usually counts it as elective credit or evaluates it from the paperwork. <strong>Keep the "
    "syllabus, the agreement or learning contract, and a description of the work you did</strong>; they are what "
    "an evaluator reads.</p>")

EXCESS_UNI = (
    "<h3>Florida excess hours</h3><p>At a state university, Florida charges an <strong>excess hour "
    "surcharge</strong> on credit hours beyond a set percentage of what the bachelor's degree requires (120% for "
    "students who entered from summer 2019 on), under " + a(EXCESS, "section 1009.286, Florida Statutes") + ". "
    "Variable-credit and elective registrations count toward that total unless they fall in one of the statute's "
    "exclusions, so register for the credit your degree can use rather than the most the number allows.</p>")

VAR_AID = (
    "<h3>Variable credit, full-time status and aid</h3><p>The credit you register for is what counts toward "
    "full-time enrolment, Bright Futures and federal aid, and veterans' and visa enrolment rules. A 1-credit "
    "registration in a variable number may leave a student below full time even when the work takes many hours a "
    "week; check the total before the add/drop deadline.</p>")

G = {}

# ---------------------------------------------------------------- ARH2990 (MDC)
G['ARH2990'] = {
    'title': 'Museum and Gallery Co-Op Work Experience',
    'credits': 3,
    'contact_hours': 144,
    'prerequisites': (
        "Miami Dade College, the only Florida public carrier, publishes no course prerequisite on its competency "
        "sheet. The course is part of MDC's Museum Studies Advanced Technical Certificate, which also includes "
        "Introduction to Museum Studies and Museum & Gallery Exhibition Design; students normally take it once "
        "they can be placed at a museum or gallery. The placement must be arranged with the programme before the "
        "term: 144 hours of work experience for 3 credits. A placement with children or vulnerable adults (for "
        "example, museum education programmes) may require background screening, which takes time."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries ARH2990: Miami Dade College, at 3 credits with 144 hours '
                   'of work experience, in its Museum Studies Advanced Technical Certificate.',
        'hours_source': 'published',
        'derived_contact_hours': None,
        'derivation': 'MDC\'s competency sheet (Updated Fall 2023) states 3.00 credits and "144 hr. Work '
                      'Experience"; those are workplace hours, not classroom hours.',
        'offerings': [{
            'institution': 'MDC', 'institution_name': 'Miami Dade College',
            'title': 'Museum and Gallery Co-Op Work Experience', 'credits': 3, 'contact_hours': 144,
            'note': '144 hours of work experience. Part of the Museum Studies Advanced Technical Certificate. '
                    'Statewide title: Museum and Gallery Co-Op Work Experience.'}],
    },
}
G['ARH2990']['html_content'] = sections(
    box("ARH2990 is a cooperative education (co-op) course: the student works at a museum or gallery and the "
        "course is built around that placement. What you do depends on the institution that hosts you and the "
        "supervisor there, so no two students' courses are the same. This guide describes how the course works "
        "and what Miami Dade College says it assesses; it is not a syllabus.")
    + "<p><strong>ARH2990 Museum and Gallery Co-Op Work Experience</strong> is offered in Florida's public "
    "colleges and universities only by <strong>Miami Dade College</strong>, at 3 credits. MDC's course competency "
    "sheet (updated Fall 2023) describes it this way: <em>This course offers an exceptional opportunity for "
    "students to further enhance their skills and knowledge in the field of Art and related studies through "
    "practical work experience. The primary focus of this course is to provide students with hands-on training "
    "that complements their academic studies. (144 hr. Work Experience)</em></p>"
    "<p>It belongs to MDC's <strong>Museum Studies Advanced Technical Certificate</strong>, a six-course programme "
    "offered online. MDC's programme page says that in this course students <em>pursue an internship within a "
    "museum or art gallery in Miami</em>, learn about museum and gallery careers, and <em>gain tools for "
    "professional etiquette and resume writing</em>. The programme's library guide lists the museums and "
    "galleries that have hosted MDC interns, from HistoryMiami Museum and the Frost Science Museum to Vizcaya "
    "Museum and Gardens and the Institute of Contemporary Art.</p>",
    [
        "Apply technical skills learned in coursework to real projects at a museum or gallery, and carry out "
        "assigned tasks with increasing independence (MDC Competency 1).",
        "Connect classroom concepts in art history and museum studies to the practice of a professional "
        "art institution, and document that connection (MDC Competency 2).",
        "Communicate with supervisors and colleagues, manage time to meet deadlines, respond to feedback and "
        "show accountability in the workplace (MDC Competency 3).",
        "Build a portfolio of the work done during the placement and assess one's own growth and career goals "
        "(MDC Competency 4).",
    ],
    [
        "Depending on the placement: assist with collections care, registration or cataloguing under supervision.",
        "Depending on the placement: help install an exhibition, write labels, or support public and education "
        "programmes.",
        "Depending on the placement: work on a gallery's sales, marketing, archive or digital collection.",
    ],
    [
        "The work done at the host museum or gallery, as agreed with the supervisor.",
        "Reflection on the placement: what was learned, what skills grew, what to develop next.",
        "Professional behaviour: communication, reliability, taking feedback.",
        "Museum and gallery careers; professional etiquette and résumé writing (named on MDC's programme page).",
        "A portfolio documenting the work.",
    ],
    [
        "Collections management and object handling.",
        "Exhibition design and installation (MDC's certificate also includes Museum &amp; Gallery Exhibition "
        "Design).",
        "Museum education and visitor services.",
        "Commercial galleries and the art market.",
    ],
    "<p><strong>Credit and hours.</strong> 3 credits for <strong>144 hours of work experience</strong> at the host "
    "institution (MDC's figure). Plan the hours across the term from the start: at 15 weeks that is close to ten "
    "hours a week.</p>"
    "<p><strong>Arranging the placement.</strong> MDC does not publish the steps on the pages read for this guide. "
    "In a co-op course the placement is normally approved before the term by the course instructor or programme "
    "coordinator, and the student, the host supervisor and the college agree what the student will do. Ask the "
    "Museum Studies programme how placements are arranged and which sites it works with.</p>"
    "<p><strong>Grading.</strong> MDC's competencies point to what is assessed: the work done (judged with the "
    "host supervisor's input), reflection that connects it to coursework, professional behaviour, and a "
    "portfolio. The syllabus for the term sets the weights.</p>",
    [
        "Museum technicians and conservators (SOC 25-4013) and archivists and curators (SOC 25-4011, 25-4012).",
        "Museum education, visitor services, registration and collections roles.",
        "Gallery assistants and art-market roles in Miami's commercial galleries and art fairs.",
        "A placement is often the route to a first job in this field, where experience counts as much as "
        "coursework.",
    ],
    [
        a('https://www.mdc.edu/asa/documents/competencies/pdf/ARH2990%20Museum%20and%20Gallery%20Co-Op%20Work%20Experience.pdf',
          "MDC course competencies for ARH2990") + " (the description, credits, 144 hours and the four "
        "competencies quoted above).",
        a('https://www.mdc.edu/museumstudiesatc/', "MDC Museum Studies Advanced Technical Certificate") +
        " (the programme this course belongs to).",
        a('https://libraryguides.mdc.edu/museumstudies/co-op', "MDC Museum Studies library guide: Museum/Gallery "
          "Co-op") + " (the museums and galleries that have hosted MDC interns).",
        "Related courses on this site: " + site('ARH2857', 'Introduction to Museum Studies') + ", " +
        site('ARH2051', 'Art History II') + ".",
    ],
    "<h3>Offering Notes</h3>" + table([('Miami Dade College', 'Museum and Gallery Co-Op Work Experience', '3',
                                        '144 hours of work experience (published)')]) +
    "<h3>Background screening</h3><p>Placements that involve children or vulnerable adults, as museum education "
    "programmes often do, may require Florida Level 2 background screening (fingerprints and state and national "
    "records checks, " + a(SCREEN, "section 435.04, Florida Statutes") + ") or the host's own check. Clearance "
    "takes time: ask the host in the first week.</p>"
    + "<h3>Transfer</h3><p>A co-op course transfers as elective credit at best: what a receiving institution sees "
    "is a number whose content was set by one placement. Keep the syllabus, the placement description and your "
    "portfolio. A student continuing to a bachelor's degree in art history should ask the receiving department "
    "whether it counts the course toward an internship requirement.</p>",
)

# ---------------------------------------------------------------- ARH2957 (FAU)
G['ARH2957'] = {
    'title': 'Honors Beginning Study Abroad in Art History',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "Florida Atlantic University, the only Florida public carrier, offers it through its Harriet L. Wilkes "
        "Honors College for students on an approved study abroad programme. The course itself lists no "
        "prerequisite; the requirements are the programme's (admission to the Honors College, the study abroad "
        "programme's eligibility rules, and pre-approval of the courses by the student's faculty advisor and of "
        "the programme by FAU's Education Abroad office). Variable credit, 1 to 6, and repeatable."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries ARH2957: Florida Atlantic University (Wilkes Honors '
                   'College), at 1 to 6 variable credits, repeatable, with a variable title.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': 'FAU records 1-6 credit and contact hours. The guide uses 3 credits (the minimum the Honors '
                      'College requires to be earned abroad) and 45 hours by Florida\'s 15-hours-per-credit '
                      'convention; the real figure is set by the course taken abroad.',
        'offerings': [{
            'institution': 'FAU', 'institution_name': 'Florida Atlantic University',
            'title': 'Honors Beginning Study Abroad in Art History', 'credits': None, 'contact_hours': None,
            'note': '1 to 6 variable credits; variable title; repeatable (FAU records a repeat surcharge limit of '
                    '6). H.L. Wilkes Honors College. Statewide title: Activities/Performances/Publications.'}],
    },
}
G['ARH2957']['html_content'] = sections(
    box("ARH2957 is a study abroad registration number. The course a student actually takes is an art history "
        "course in an approved programme abroad, and its content, place and credit come from that programme. "
        "FAU records the title as variable. This guide explains how the number works; it is not a syllabus.")
    + "<p><strong>ARH2957 Honors Beginning Study Abroad in Art History</strong> is carried in Florida's public "
    "colleges and universities only by <strong>Florida Atlantic University</strong>, through its <strong>Harriet "
    "L. Wilkes Honors College</strong> in Jupiter. FAU's course record describes it this way: <em>Credit for "
    "enrollment in approved beginning art history courses in approved study abroad programs.</em> It carries "
    "<strong>1 to 6 credits</strong>, its title is variable, and it may be repeated.</p>"
    "<p>The number lets an introductory (\"beginning\") art history course taken abroad appear on an FAU "
    "transcript as Honors College credit. The statewide course record gives it the generic title "
    "<strong>Activities/Performances/Publications</strong>, which says nothing about the content; FAU's own title "
    "and description are the ones that apply.</p>",
    [
        "Complete an approved beginning art history course abroad and earn credit for it.",
        "Describe and analyse works of art and architecture seen in their own setting, using the vocabulary of "
        "art history.",
        "Relate the art studied to the history and culture of the host country.",
    ],
    [
        "Depending on the programme: explain the development of a period or region's art (for example the "
        "Renaissance in Italy) from works studied on site.",
        "Depending on the programme: write a site report or visual analysis based on a museum or monument "
        "visit.",
        "Reflect on what studying art in place adds to studying it from reproductions.",
    ],
    [
        "The content of the approved art history course taken abroad.",
        "Visual analysis and description of works seen first-hand.",
        "The historical and cultural context of the host country's art.",
    ],
    [
        "Museum and site visits as primary sources.",
        "Architecture and urban form.",
        "The host country's language, as needed for the visits.",
    ],
    "<p><strong>Who can use it.</strong> FAU places the number in the Wilkes Honors College. The Honors College's "
    "study abroad page says that <em>all study abroad must be coordinated through Education Abroad</em>, that "
    "<em>all coursework taken abroad must be pre-approved by the student's faculty advisor</em>, and that Honors "
    "students who study abroad in fall or spring and do not dual-enrol in Honors College study abroad courses lose "
    "their Honors College scholarship for that term. Numbers like ARH2957 are how that dual enrolment is "
    "recorded.</p>"
    "<p><strong>Credit.</strong> 1 to 6 credits, matched to the course taken abroad. The Honors College counts "
    "study abroad toward its non-classroom learning requirement when the student spends at least four weeks abroad "
    "and earns at least 3 academic credits from FAU or another approved, accredited institution.</p>"
    "<p><strong>Grading.</strong> The grade comes from the course taken abroad, posted to the FAU transcript once "
    "the programme reports it. Ask before you go how a host institution's grades will be converted.</p>",
    None,
    [
        a('https://www.fau.edu/honors/current-students/study-abroad/', "FAU Wilkes Honors College: Studying "
          "Abroad") + " (pre-approval by the faculty advisor, the four-week and 3-credit requirement, dual "
          "enrolment, and Bright Futures).",
        a('https://www.fau.edu/resources/support/global/goabroad/', "FAU Education Abroad") + " (faculty-led, "
        "exchange, direct-enrol and third-party programmes; advising sessions).",
        "Survey courses on this site: " + site('ARH2050', 'Art History I') + ", " + site('ARH2051', 'Art History II')
        + ".",
    ],
    "<h3>Offering Notes</h3>" + table([('Florida Atlantic University (Wilkes Honors College)',
                                        'Honors Beginning Study Abroad in Art History', '1 to 6 (variable)',
                                        'not published separately (1 to 6, matched to credit)')]) +
    "<h3>Repeating the number</h3><p>FAU's record marks ARH2957 as repeatable, with a repeat surcharge limit of 6; "
    "it can carry different courses in different terms. Ask your advisor how many credits under the number your "
    "degree will count.</p>"
    + VAR_AID +
    "<p>The Honors College page adds that Bright Futures can be used for programmes at accredited Florida "
    "institutions but not for programmes run outside Florida; check with FAU's Office of Financial Aid.</p>"
    + EXCESS_UNI + TRANSFER_SHELL,
)

# ---------------------------------------------------------------- SOW2949 (GCSC, UCF)
G['SOW2949'] = {
    'title': 'Cooperative Education in Social Work',
    'credits': 1,
    'contact_hours': 15,
    'prerequisites': (
        "Gulf Coast State College: minimum 2.0 GPA, a meeting with the co-op coordinator, and an available co-op "
        "work experience slot. UCF: arranged through its Experiential Learning office and the student's academic "
        "unit; credit-eligible positions must be approved. START BACKGROUND SCREENING IN WEEK ONE: social service "
        "placements with children, elderly or disabled clients normally require Florida Level 2 screening "
        "(fingerprints, state and FBI records), and clearance can take weeks."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'Two Florida public institutions carry SOW2949: Gulf Coast State College at 1 to 3 credits, '
                   'and the University of Central Florida at variable credit.',
        'hours_source': 'derived',
        'derived_contact_hours': 15,
        'derivation': 'Neither institution publishes workplace hours for the number. The guide uses the minimum '
                      'registration, 1 credit, and 15 hours by Florida\'s 15-hours-per-credit convention; actual '
                      'workplace hours are set with the co-op coordinator and are normally higher.',
        'offerings': [
            {'institution': 'GCSC', 'institution_name': 'Gulf Coast State College',
             'title': 'COOP/Work Experience/Social Services', 'credits': None, 'contact_hours': None,
             'note': '1 to 3 credits. Prerequisite: minimum 2.0 GPA, meeting with the co-op coordinator, available '
                     'slot. Weekly, mid-term and end-of-term online reflections. At most 6 co-op credits count '
                     'toward the A.A.'},
            {'institution': 'UCF', 'institution_name': 'University of Central Florida',
             'title': 'Cooperative Education', 'credits': None, 'contact_hours': None,
             'note': 'Variable credit (VAR); not listed in UCF\'s current online catalogue. Co-op at UCF is paid, '
                     'runs over several semesters, and may be registered for credit or zero credit. Statewide '
                     'title: Internships/Practicums/Clinical Practice.'}],
    },
}
G['SOW2949']['html_content'] = sections(
    box("SOW2949 is a cooperative education (co-op) number: the student works in a social service setting and "
        "earns credit for that work, supervised by the college. What you do is set by the placement and the "
        "agreement made for it, so each student's course is different. This guide explains how the course works "
        "at the two institutions that carry it; it is not a syllabus.")
    + "<p><strong>SOW2949</strong> is carried by two Florida public institutions. <strong>Gulf Coast State "
    "College</strong> lists it as <em>COOP/Work Experience/Social Services</em>, 1 to 3 credit hours, and "
    "describes it this way: <em>Supervised, practical work experience that seeks to combine theories and apply "
    "practical skills</em> to projects in the student's major field of study, with online weekly, mid-term and "
    "end-of-term reflection assignments. The <strong>University of Central Florida</strong> records it as "
    "<em>Cooperative Education</em> at variable credit; it is not listed in UCF's current online catalogue. The "
    "statewide title is <strong>Internships/Practicums/Clinical Practice</strong>.</p>"
    "<p>At Gulf Coast it sits beside the Social Work option of the Associate in Arts, the route to a "
    "bachelor's degree in social work at a university. A co-op does not replace the supervised <strong>field "
    "placement</strong> that an accredited BSW or MSW programme requires; it is earlier, shorter experience that "
    "helps a student decide whether the work suits them and shows a university that they have tried it.</p>",
    [
        "Carry out the tasks agreed for the placement in a social service setting, under supervision.",
        "Connect what was learned in coursework (for example in an introduction to social work) to what happens "
        "in the agency, in written reflections through the term.",
        "Behave professionally: reliability, communication with a supervisor, confidentiality of clients' "
        "information, and knowing the limits of a student's role.",
        "Assess one's own strengths and interests in social work and set next steps.",
    ],
    [
        "Depending on the placement: describe how the agency is organised and funded and which clients it "
        "serves.",
        "Depending on the placement: observe intake, case management or group work and describe the skills "
        "used.",
        "Identify the values in the NASW Code of Ethics as they appear in the agency's practice.",
    ],
    [
        "The agreed work at the placement and the supervisor's evaluation of it.",
        "Reflection that links theory to practice (Gulf Coast's weekly, mid-term and end-of-term "
        "assignments).",
        "Confidentiality, boundaries and mandatory reporting.",
        "Career exploration in social work and human services.",
    ],
    [
        "Agencies in the region: child welfare, aging services, health care, schools, the courts.",
        "Diversity and working with clients unlike oneself.",
        "Self-care in emotionally demanding work.",
    ],
    "<h3>At Gulf Coast State College</h3><p><strong>Before the term:</strong> a minimum 2.0 GPA, a meeting with "
    "the co-op coordinator, and an available co-op slot (the catalogue's prerequisite). The college's co-op page "
    "says co-op earns <em>elective academic credit for work experience via employment, an internship or "
    "volunteering</em>, that the coordinator helps place students, and that students already working on campus "
    "as student assistants or in work-study may use that work. <strong>Credit:</strong> 1 to 3 credits for "
    "SOW2949; co-op courses count toward most A.A. and A.S. programmes, but <strong>at most six co-op credit "
    "hours count toward the A.A.</strong> <strong>Grading:</strong> the work and the reflection assignments, as "
    "the syllabus sets them.</p>"
    "<h3>At the University of Central Florida</h3><p>UCF's Experiential Learning office says co-op <em>is an "
    "academic program that allows students to apply classroom theory in a real-world setting</em>, that co-op "
    "experiences take place over multiple semesters and are always paid, and that students can register each "
    "semester either for credit or for zero credit. Ask the School of Social Work whether it accepts co-op credit "
    "under this number toward your degree before you register.</p>",
    [
        "Social and human service assistants (SOC 21-1093): an entry role open with an associate degree.",
        "Child, family and school social workers (SOC 21-1021); healthcare social workers (SOC 21-1022); mental "
        "health and substance abuse social workers (SOC 21-1023), after a BSW or MSW.",
        "Florida employers include the Department of Children and Families and its community-based care lead "
        "agencies, hospitals, school districts, and non-profit agencies. Clinical social work in Florida requires "
        "an MSW and licensure under Chapter 491, Florida Statutes.",
    ],
    [
        a('https://www.gulfcoast.edu/catalog/current/courses/sow/', "Gulf Coast State College catalogue: Social Work "
          "courses") + " (SOW 2949's description, 1 to 3 credits, prerequisites, and the six-hour A.A. cap).",
        a('https://gulfcoast.edu/current-students/coop/', "Gulf Coast State College: Employment, Internships and "
          "Off Campus Jobs") + " (how co-op works and the co-op coordinator).",
        a('https://www.gulfcoast.edu/academics/programs/social-work-aa/index.html', "Gulf Coast State College: "
          "Social Work Option, A.A.") + " (the transfer route to a bachelor's in social work).",
        a(UCF_EL, "UCF Experiential Learning") + " (co-op at UCF: paid, several semesters, credit or zero "
        "credit).",
        "Related courses on this site: " + site('SOW2020', 'Introduction to Social Work') + ", " +
        site('SOW1054', 'Human Services Experience') + ", " + site('SOW4941', 'Internship') + ".",
    ],
    "<h3>Offering Notes</h3>" + table([
        ('Gulf Coast State College', 'COOP/Work Experience/Social Services', '1 to 3 (variable)', 'not published'),
        ('University of Central Florida', 'Cooperative Education', 'variable (VAR)', 'not published')]) +
    "<p>The page's figures of 1 credit and 15 hours are the minimum registration, not the workplace hours, which "
    "the co-op coordinator sets.</p>"
    "<h3>Background screening, confidentiality and reporting</h3><p>Social service agencies that serve children, "
    "elderly or disabled people generally require <strong>Level 2 background screening</strong> under " +
    a(SCREEN, "section 435.04, Florida Statutes") + ": fingerprints checked against state records through the "
    "Florida Department of Law Enforcement and national records through the FBI. Clearance can take weeks, so "
    "<strong>start it in the first week</strong>, or before the term if the agency allows. Treat everything you "
    "learn about clients as confidential. Anyone in Florida who suspects a child or vulnerable adult is being "
    "abused, neglected or exploited must report it to the Florida Abuse Hotline, 1-800-96-ABUSE (Chapter 39 and "
    "Chapter 415, Florida Statutes); tell your supervisor as well, but telling the supervisor does not replace "
    "the report.</p>"
    + VAR_AID +
    "<p>At UCF a zero-credit co-op registration keeps the experience on the record without adding credit; it "
    "does not count toward full-time enrolment.</p>"
    + EXCESS_UNI.replace("<h3>Florida excess hours</h3>", "<h3>Florida excess hours (UCF)</h3>") +
    "<p>The statute excludes credit hours earned through internship programmes from the count; ask UCF's "
    "registrar whether a co-op registration is treated the same way.</p>" + TRANSFER_SHELL,
)

# ---------------------------------------------------------------- EEL3970 (UCF)
G['EEL3970'] = {
    'title': 'Undergraduate Honors Thesis (Electrical Engineering)',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "UCF records EEL3970 as an honors course at variable credit. Entry to UCF's Honors Undergraduate Thesis "
        "(HUT) programme, run by the Burnett Honors College's Office of Honors Research, requires (October 2025 "
        "handbook) 60 completed credits, 12 completed upper-division credits, a 3.5 UCF GPA and at least two "
        "semesters before graduation, plus a thesis chair and committee. Students do not register themselves: the "
        "Office of Honors Research enrols them after a registration agreement. Note that the handbook names the "
        "4000-level numbers (xxx 4903H Directed Readings, xxx 4970H Honors Thesis); confirm with the Office of "
        "Honors Research which number your thesis is registered under."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries EEL3970: the University of Central Florida, at '
                   'variable credit, as an honors thesis number.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': 'UCF records VAR. The HUT handbook weights each Honors Thesis course at 3 credit hours; 45 is '
                      'Florida\'s 15-hours-per-credit convention. The work itself is independent research and takes '
                      'far longer.',
        'offerings': [{
            'institution': 'UCF', 'institution_name': 'University of Central Florida',
            'title': 'Undergraduate Honors Thesis', 'credits': None, 'contact_hours': None,
            'note': 'Variable credit (VAR); honors. Not listed in UCF\'s current online catalogue; the HUT '
                    'programme now enrols thesis students under xxx 4970H (EEL4970 is also in the inventory). '
                    'Statewide title: Thesis/Thesis Defense.'}],
    },
}
G['EEL3970']['html_content'] = sections(
    box("EEL3970 is an honors thesis number: each student's thesis is an original research or design project "
        "chosen with a faculty chair, so the content is different for every student. This guide explains how "
        "the honors thesis works at UCF; it is not a syllabus.")
    + "<p><strong>EEL3970 Undergraduate Honors Thesis</strong> is carried in Florida's public colleges and "
    "universities only by the <strong>University of Central Florida</strong>, in the electrical engineering "
    "prefix, at variable credit and flagged as an honors course. The statewide title is "
    "<strong>Thesis/Thesis Defense</strong>.</p>"
    + UCF_VAR_NOTE +
    "<p>UCF's honors thesis is run by the <strong>Office of Honors Research</strong> in the <strong>Burnett "
    "Honors College</strong> as the <strong>Honors Undergraduate Thesis (HUT)</strong> programme. Its handbook "
    "(October 2025) describes it as <em>modeled after a master's thesis program</em>, open to qualified juniors "
    "and seniors in any discipline, in which students <em>work over two to four semesters to design and carry out "
    "an honors thesis or project</em> under a faculty committee. Graduates receive one of three distinctions "
    "(Honors in the Major, Honors in Research or Honors in Creative Inquiry), printed on the diploma and final "
    "transcript.</p>"
    "<p>⚠ <strong>A note on the number.</strong> The handbook names the HUT courses as Honors Directed Readings "
    "(<strong>xxx 4903H</strong>) and Honors Thesis (<strong>xxx 4970H</strong>), and the statewide inventory "
    "also carries <strong>EEL4970</strong> Undergraduate Honors Thesis for UCF. EEL3970 is the 3000-level twin. "
    "Which number a given thesis is registered under is the Office of Honors Research's decision; the programme "
    "described below is the same.</p>",
    [
        "Formulate a research or design question in electrical or computer engineering and write a proposal "
        "approved by the whole thesis committee.",
        "Review the published literature on the question.",
        "Carry out the research, design, experiment or analysis independently under a faculty chair's "
        "supervision.",
        "Write a thesis to the programme's format, pass the format review, and defend it orally before the "
        "committee.",
        "Submit the thesis to the UCF library for publication.",
    ],
    [
        "Depending on the project: build and test a prototype circuit, device or system.",
        "Depending on the project: develop a simulation or model and validate it against measurements.",
        "Present the work at a research showcase or conference.",
    ],
    [
        "Choosing a thesis chair and committee; the proposal.",
        "Literature review and research methods in the chosen area.",
        "The research or design work itself.",
        "Technical writing: structure, figures, citation, and the HUT format requirements.",
        "The oral defense and submission to the library.",
    ],
    [
        "Research ethics; IRB approval where a project involves human subjects (the handbook warns this adds "
        "time).",
        "Laboratory safety and equipment training.",
        "Intellectual property where a design may be patentable.",
    ],
    "<p><strong>Admission (HUT handbook, October 2025).</strong> Complete the programme's eligibility form; "
    "decisions are sent the semester before the start. Requirements: 60 completed credits, 12 completed "
    "upper-division (3000/4000-level) credits, a 3.5 UCF GPA, and at least two semesters remaining before "
    "graduation. Students must also speak with an academic success coach about how the thesis fits their "
    "graduation plan.</p>"
    "<p><strong>Courses and credit.</strong> At least two honors courses, each weighted at 3 credit hours: "
    "Honors Directed Readings (the proposal semester) and Honors Thesis. Optional second semesters of each, at 1 or "
    "3 credits, if more time is needed. The programme is a minimum of two semesters; the handbook says most "
    "high-quality theses take three or four.</p>"
    "<p><strong>Registration.</strong> <em>Do not attempt to enroll yourself in HUT courses</em>: a registration "
    "agreement goes to the Office of Honors Research before each semester's deadline, and its coordinator "
    "enrols the student.</p>"
    "<p><strong>Committee.</strong> A UCF faculty thesis chair from the thesis discipline and a second member who "
    "is a subject-matter expert; more may be added.</p>"
    "<p><strong>Grading.</strong> Letter grade or pass/fail (S/U), chosen with the thesis chair before "
    "registering; letter grades count in the GPA. To graduate with the distinction a student needs an A, B or S "
    "in both required courses, an approved proposal, all deadlines met including the format review and oral "
    "defense, the thesis submitted to the library, and an exit UCF GPA of 3.3 or above.</p>",
    [
        "Graduate study in electrical or computer engineering: an honors thesis is evidence of research ability "
        "that admissions committees read closely.",
        "Research and development roles: electrical engineers (SOC 17-2071), electronics engineers (17-2072) "
        "and computer hardware engineers (17-2061), where a thesis shows independent technical work.",
        "Central Florida's research employers include the simulation and defence industry, the space industry "
        "and photonics companies around UCF's CREOL.",
    ],
    [
        a(UCF_HUT, "UCF Burnett Honors College: HUT Program Handbook (October 2025)") + " (admission, courses, "
        "committee, grading, deadlines and distinctions, as summarised above).",
        a(UCF_ECE, "UCF Department of Electrical and Computer Engineering: Undergraduate Programs") + " (the "
        "B.S. in Electrical Engineering and Computer Engineering that a thesis in this prefix sits in).",
        "Related courses on this site: " + site('EEL4914', 'Senior Capstone Design I') + " (the design project "
        "every UCF ECE student completes), " + site('EEL3004C', 'Linear Circuits I') + ".",
    ],
    "<h3>Offering Notes</h3>" + table([('University of Central Florida', 'Undergraduate Honors Thesis',
                                        'variable (VAR); HUT courses weighted at 3', 'not published')]) +
    "<h3>Thesis and senior design</h3><p>An honors thesis is separate from the two-semester senior design "
    "sequence every UCF electrical and computer engineering student completes. Some students build a thesis out "
    "of a design project; ask the department whether thesis credit can count as an elective in your degree, since "
    "the handbook says departments must grant permission for honors coursework to replace other degree "
    "requirements.</p>"
    + VAR_AID + EXCESS_UNI + TRANSFER_SHELL,
    "<p>AI tools can help find and summarise literature, check code and polish prose, but a thesis is a test of "
    "the student's own work. Generated literature summaries routinely cite papers that do not exist; check every "
    "reference against the source. Agree with your thesis chair, in writing, what use of AI is acceptable and say "
    "in the thesis what you used: the thesis must be certified free of plagiarism before it is submitted, and it "
    "is published under your name.</p>",
)

# ---------------------------------------------------------------- study abroad helper (EEL3955, CGS4955)


def study_abroad(cid, prefix_words, level_words, related):
    g = {
        'title': 'Study Abroad (%s)' % prefix_words,
        'credits': 3,
        'contact_hours': 45,
        'prerequisites': (
            "UCF records %s at variable credit; it is a registration number for approved study abroad work, not a "
            "course with its own prerequisites. The requirements are the programme's: approval through UCF Abroad "
            "and, for engineering and computer science students, the College of Engineering and Computer Science "
            "(its exchange programmes ask for a 3.00 cumulative GPA, a CECS major, junior or senior standing, and "
            "meetings with the International Engineering programme manager). Courses taken abroad must be approved "
            "in advance to count toward the degree." % cid),
        'version': '1.0',
        'offering_notes': {
            'summary': 'One Florida public institution carries %s: the University of Central Florida, at variable '
                       'credit.' % cid,
            'hours_source': 'derived',
            'derived_contact_hours': 45,
            'derivation': 'UCF records VAR. The guide uses 3 credits (one typical course) and 45 hours by Florida\'s '
                          '15-hours-per-credit convention; the real figure is set by the course taken abroad.',
            'offerings': [{
                'institution': 'UCF', 'institution_name': 'University of Central Florida',
                'title': 'Study Abroad', 'credits': None, 'contact_hours': None,
                'note': 'Variable credit (VAR). Not listed in UCF\'s current online catalogue. Statewide title: '
                        'Activities/Performances/Publications.'}],
        },
    }
    g['html_content'] = sections(
        box("%s is a study abroad registration number. The course a student takes abroad, its content, place and "
            "credit, comes from the programme: a UCF faculty-led course, a partner university on exchange, or a "
            "third-party programme. This guide explains how the number and the process work; it is not a "
            "syllabus." % cid)
        + "<p><strong>%s Study Abroad</strong> is carried in Florida's public colleges and universities only by the "
        "<strong>University of Central Florida</strong>, in the %s prefix at the %s level. The statewide title is "
        "the generic <strong>Activities/Performances/Publications</strong>, which says nothing about the "
        "content.</p>" % (cid, prefix_words.lower(), level_words)
        + UCF_VAR_NOTE +
        "<p>UCF keeps study abroad numbers at every level in many prefixes; this one lets work done abroad be "
        "recorded in the %s prefix while its equivalence to a regular UCF course is worked out. Where a course "
        "abroad matches a UCF course, it is usually better to have it evaluated as that course, because a named "
        "equivalent counts toward degree requirements and a study abroad number may count only as an elective.</p>"
        % prefix_words.lower(),
        [
            "Complete an approved course of study abroad and earn credit for it.",
            "Apply %s knowledge in a different academic and professional setting." % prefix_words.lower(),
            "Describe how the practice of the discipline differs in the host country (standards, industry, "
            "teaching).",
        ],
        [
            "Depending on the programme: complete a project, laboratory or site visit with a host university or "
            "company.",
            "Work in a team with students from the host country.",
            "Use the host country's language in a technical setting.",
        ],
        [
            "The content of the approved course or courses taken abroad.",
            "Comparison of professional practice in the discipline across countries.",
            "Reflection on the experience abroad.",
        ],
        related['opt_topics'],
        "<p><strong>Kinds of programme.</strong> UCF's College of Engineering and Computer Science lists three: "
        "<strong>reciprocal exchanges</strong> (a fall or spring semester at a partner university, paying UCF "
        "tuition, with financial aid usable), <strong>Global Centers and faculty-led programmes</strong> (short "
        "programmes, usually in summer or a semester break, with one or two courses taught by UCF faculty; Summer "
        "2027 Global Centers are in Barcelona, Rome and Seoul), and <strong>third-party partner programmes</strong> "
        "listed on the UCF Abroad website.</p>"
        "<p><strong>Approval.</strong> For CECS exchanges the college asks students to meet the International "
        "Engineering programme manager (usually about three one-hour meetings), to have a 3.00 cumulative GPA, a "
        "CECS, Data Science or Photonics major, and junior or senior standing, and to be accepted by the host. "
        "<em>Any changes must be approved by the International Engineering advisor</em>, including changes during "
        "the host's add/drop period. Check courses against the CECS course equivalency database before you go.</p>"
        "<p><strong>Grading and credit.</strong> The grade and credit come from the course taken abroad and are "
        "posted to the UCF record once the programme reports them. Ask before you go how the host's grades will be "
        "converted and whether the course will be posted under this number or as a named UCF equivalent.</p>",
        related['careers'],
        [
            a(UCF_CECS_SA, "UCF College of Engineering and Computer Science: Study Abroad") + " (programme types, "
            "eligibility, approvals, and the course equivalency database).",
            a(UCF_FA_SA, "UCF Student Financial Assistance: Study Abroad") + " (which aid applies to which "
            "programme, and the forms).",
        ] + related['learn'],
        "<h3>Offering Notes</h3>" + table([('University of Central Florida', 'Study Abroad', 'variable (VAR)',
                                            'not published')]) +
        "<h3>Financial aid</h3><p>UCF's financial aid page says students should see a study abroad advisor before "
        "contacting financial aid; that most aid requires at least 6 enrolled hours, including approved study "
        "abroad coursework; that short-term and exchange programmes in which students register for UCF courses are "
        "eligible for Bright Futures, federal and Florida aid, while partner programmes qualify only for federal and "
        "private aid; and that some costs (deposits, airfare, visas) may be due before aid is paid.</p>"
        + VAR_AID + EXCESS_UNI + TRANSFER_SHELL,
    )
    return g


G['EEL3955'] = study_abroad('EEL3955', 'Electrical Engineering', 'junior (3000)', {
    'opt_topics': [
        "International engineering standards (IEC as well as IEEE and US codes).",
        "Engineering ethics and regulation in another country.",
        "Visits to host-country industry or research laboratories.",
    ],
    'careers': [
        "Electrical and electronics engineers (SOC 17-2071, 17-2072) in companies that work across borders: "
        "Florida's aerospace, defence, semiconductor and power employers buy, sell and design internationally, "
        "and experience abroad is evidence that a graduate can work that way.",
    ],
    'learn': [
        a(UCF_ECE, "UCF Department of Electrical and Computer Engineering: Undergraduate Programs") + ".",
        "Related course on this site: " + site('EEL3004C', 'Linear Circuits I') + ".",
    ],
})
G['CGS4955'] = study_abroad('CGS4955', 'Computer General Studies', 'senior (4000)', {
    'opt_topics': [
        "Data protection law in the host country (for example the EU's GDPR) and its effect on software and "
        "information systems.",
        "Software and information technology industries in the host country.",
        "Working on a distributed or multinational team.",
    ],
    'careers': [
        "Software developers (SOC 15-1252), computer systems analysts (15-1211) and information security analysts "
        "(15-1212): roles in which teams and clients are often international.",
    ],
    'learn': [
        "Related course on this site: " + site('CGS1060', 'Introduction to Computer Concepts') + ".",
    ],
})

# ---------------------------------------------------------------- EEL1906 (UCF)
G['EEL1906'] = {
    'title': 'Independent Study (Electrical Engineering)',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "UCF records EEL1906 at variable credit with no catalogue entry. Independent study is arranged, not "
        "chosen from the schedule: the student needs a faculty member in Electrical and Computer Engineering who "
        "agrees to supervise, an agreed plan of work, and the department's permission to register, normally "
        "before the term starts. Ask the department for its current form and deadline."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries EEL1906: the University of Central Florida, at '
                   'variable credit.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': 'UCF records VAR. The guide uses 3 credits as a placeholder for one typical registration and '
                      '45 hours by Florida\'s 15-hours-per-credit convention; the real figure is set in the '
                      'agreement with the supervising faculty member.',
        'offerings': [{
            'institution': 'UCF', 'institution_name': 'University of Central Florida',
            'title': 'Independent Study', 'credits': None, 'contact_hours': None,
            'note': 'Variable credit (VAR). Not listed in UCF\'s current online catalogue. Statewide title: '
                    'Directed Reading/Directed Independent Study.'}],
    },
}
G['EEL1906']['html_content'] = sections(
    box("EEL1906 is an independent study number: a student and a faculty member agree a plan of reading or "
        "project work that no scheduled course offers, and the student carries it out under that faculty "
        "member's supervision. The content is different for every student. This guide explains how the number "
        "works; it is not a syllabus.")
    + "<p><strong>EEL1906 Independent Study</strong> is carried in Florida's public colleges and universities "
    "only by the <strong>University of Central Florida</strong>, in the electrical engineering prefix at the "
    "freshman (1000) level. The statewide title is <strong>Directed Reading/Directed Independent "
    "Study</strong>.</p>"
    + UCF_VAR_NOTE +
    "<p>UCF holds independent study numbers at each level in each prefix (in EEL: 1906, 2905, 3905, 4906 and "
    "graduate numbers). A 1000-level independent study is unusual: first-year students have little of the "
    "background that directed work in electrical engineering builds on, and the upper-division number "
    "(<strong>EEL4906</strong> Directed Independent Study) is the one most students use. A first-year student "
    "might use EEL1906 to join a faculty member's laboratory early or to study a topic outside the curriculum at "
    "an introductory level.</p>",
    [
        "Agree with a supervising faculty member a defined plan of work, with goals, readings or tasks, and a "
        "final product.",
        "Work independently on the plan, meeting the supervisor at agreed intervals.",
        "Produce the agreed product (a report, a design, code, a presentation) and explain what was learned.",
    ],
    [
        "Depending on the plan: learn a tool used in the department's laboratories (circuit simulation, "
        "programming a microcontroller, measurement instruments).",
        "Depending on the plan: read and summarise introductory literature on an area of electrical "
        "engineering.",
        "Contribute to a faculty member's research project at a level suited to a first-year student.",
    ],
    [
        "The topic set in the agreement with the supervising faculty member.",
        "Planning and managing independent work.",
        "Technical writing or presentation of the result.",
    ],
    [
        "Laboratory safety and equipment training, where the work is hands-on.",
        "Introductory circuits, electronics or programming, as the plan requires.",
    ],
    "<p><strong>Finding a supervisor.</strong> Approach a faculty member whose area interests you, with a short "
    "written idea of what you want to study and why. UCF's department pages list research areas and laboratories. "
    "Allow time: faculty agree to supervise only a few students, and the agreement has to be in place before "
    "registration.</p>"
    "<p><strong>The agreement.</strong> Expect a written registration agreement or form that "
    "records the plan, the credit, how the work will be graded, and the faculty member's and department's "
    "signatures. Ask Electrical and Computer Engineering for its current form and deadline.</p>"
    "<p><strong>Grading.</strong> Set in the agreement: letter grade or pass/fail, based on the final product and "
    "the work through the term.</p>",
    None,
    [
        a(UCF_ECE, "UCF Department of Electrical and Computer Engineering: Undergraduate Programs") + " (the degrees "
        "independent study in this prefix supports; the department's site lists its research areas and "
        "laboratories).",
        "Related courses on this site: " + site('EEL3004C', 'Linear Circuits I') + ", " +
        site('EEL3111C', 'Circuits I') + ".",
    ],
    "<h3>Offering Notes</h3>" + table([('University of Central Florida', 'Independent Study', 'variable (VAR)',
                                        'not published')]) +
    "<h3>Does it count toward the degree?</h3><p>Independent study credit counts only where the degree has room "
    "for it, usually as a free or technical elective, and often with a limit on how many independent study hours "
    "count. A 1000-level independent study is unlikely to count as an upper-division engineering elective. Ask an "
    "academic advisor before registering.</p>"
    + VAR_AID + EXCESS_UNI + TRANSFER_SHELL,
)

# ---------------------------------------------------------------- special topics helper (EEL1931, EDG1931)
ST_RULE = (
    "<p>UCF's <em>Undergraduate Curriculum Handbook</em> (version 2.0, Fall 2019) explains what these numbers are "
    "for. A special topics course is a <em>new, temporary</em> course, used <em>to gauge student interest in the "
    "topic, to accommodate faculty specialties, and/or respond to emerging trends in the discipline</em>. Each "
    "special topics request must have a <strong>syllabus</strong> and is approved by the university's "
    "curriculum committee (UCRC); once approved it <em>can be offered up to three times</em> (honors special topics "
    "up to four) before the department must propose it again or make it a permanent course. The number depends "
    "only on the level: <strong>1931</strong> at the 1000 level, 2930, 3930, 4932 and so on above it.</p>")


def special_topics(cid, prefix_words, dept_words, related):
    g = {
        'title': 'Special Topics (%s)' % prefix_words,
        'credits': 3,
        'contact_hours': 45,
        'prerequisites': (
            "Set for each section by the approved special-topics syllabus; the number itself has no prerequisite. "
            "UCF records %s at variable credit with no catalogue entry. Read the section's title and notes in the "
            "schedule, and the syllabus, before registering, and ask an advisor whether that topic counts toward "
            "your degree." % cid),
        'version': '1.0',
        'offering_notes': {
            'summary': 'One Florida public institution carries %s: the University of Central Florida, at variable '
                       'credit.' % cid,
            'hours_source': 'derived',
            'derived_contact_hours': 45,
            'derivation': 'UCF records VAR. The guide uses 3 credits and 45 hours (Florida\'s 15-hours-per-credit '
                          'convention) as a placeholder for one typical section; each section\'s approved syllabus '
                          'sets its credit.',
            'offerings': [{
                'institution': 'UCF', 'institution_name': 'University of Central Florida',
                'title': 'Special Topics', 'credits': None, 'contact_hours': None,
                'note': 'Variable credit (VAR). Not listed in UCF\'s current online catalogue. Each section is an '
                        'approved special topics course with its own syllabus, offered up to three times. '
                        'Statewide title: Special Topics/Seminars.'}],
        },
    }
    g['html_content'] = sections(
        box("%s is a special topics number: each section is a different course, on a subject a faculty member "
            "proposes, with its own title and syllabus. The content changes from term to term. This guide explains "
            "how the number works at UCF; it is not a syllabus for any section." % cid)
        + "<p><strong>%s Special Topics</strong> is carried in Florida's public colleges and universities only by "
        "the <strong>University of Central Florida</strong>, in the %s prefix at the 1000 (freshman) level. The "
        "statewide title is <strong>Special Topics/Seminars</strong>.</p>" % (cid, dept_words)
        + UCF_VAR_NOTE + ST_RULE + related['desc'],
        [
            "Meet the learning outcomes stated in the approved syllabus for the section taken.",
            "Explain the section's topic and how it relates to the wider field of %s." % related['field'],
        ],
        related['opt_out'],
        [
            "The topic of the section, as set in its approved syllabus.",
        ],
        related['opt_top'],
        "<p><strong>Finding a section.</strong> A special topics section appears in the class schedule under this "
        "number with its own section title. The title and syllabus, not the number, tell you what the course is. "
        "Because the topic changes, two students with this number on their transcripts may have studied "
        "completely different things.</p>"
        "<p><strong>Credit and grading.</strong> Set by the approved syllabus for the section, like any regular "
        "course: the credit is fixed for that section even though the number is variable in the inventory.</p>"
        "<p><strong>Taking it more than once.</strong> A student may be able to take the number again for a "
        "different topic. Ask the department and the registrar how a second registration under the same number is "
        "treated, because repeating a number can be read as repeating a course.</p>",
        related['careers'],
        [
            a(UCF_CURR, "UCF Undergraduate Curriculum Handbook, version 2.0 (Fall 2019)") + " (what a special "
            "topics course is, the numbers by level, the syllabus and UCRC approval, and the three-offering "
            "limit).",
        ] + related['learn'],
        "<h3>Offering Notes</h3>" + table([('University of Central Florida', 'Special Topics', 'variable (VAR)',
                                            'not published')]) +
        "<h3>Does it count toward the degree?</h3><p>A special topics section counts where the degree has room for "
        "it, usually as an elective. Keep the section title on your record: an advisor or another institution "
        "reading only \"Special Topics\" cannot tell what you studied.</p>"
        + VAR_AID + EXCESS_UNI + TRANSFER_SHELL +
        "<p>When a special topics course proves durable, the department proposes it as a permanent course with its "
        "own number. A topic you took under this number may later exist under another; the two do not become "
        "equivalent automatically.</p>",
    )
    return g


G['EEL1931'] = special_topics('EEL1931', 'Electrical Engineering', 'electrical engineering', {
    'field': 'electrical and computer engineering',
    'desc': "<p>At the 1000 level in electrical engineering a special topics section is most likely an "
            "introduction to an area of the field, a hands-on project course for first-year students, or a "
            "seminar on an emerging technology. The section's syllabus is the authority.</p>",
    'opt_out': [
        "Depending on the section: build and test a simple circuit or embedded project.",
        "Depending on the section: describe the main areas of electrical and computer engineering and the careers "
        "they lead to.",
        "Depending on the section: explain an emerging technology (for example semiconductors, photonics or "
        "renewable power) at an introductory level.",
    ],
    'opt_top': [
        "Introductory circuits, electronics or programming, where the section is hands-on.",
        "Engineering design and teamwork.",
        "Current developments in the field.",
    ],
    'careers': [
        "A first-year topics course is exploratory: it can help a student decide whether electrical or computer "
        "engineering (SOC 17-2071, 17-2072, 17-2061) is the right major.",
    ],
    'learn': [
        a(UCF_ECE, "UCF Department of Electrical and Computer Engineering: Undergraduate Programs") + ".",
        "Related course on this site: " + site('EEL3004C', 'Linear Circuits I') + ".",
    ],
})
G['EDG1931'] = special_topics('EDG1931', 'Education', 'general education (curriculum and teaching)', {
    'field': 'education',
    'desc': "<p>The EDG prefix covers general curriculum and teaching. At the 1000 level a special topics section "
            "is most likely an introductory seminar for students considering teaching or another career in "
            "education, or a course on a current issue in schools. The section's syllabus is the authority.</p>",
    'opt_out': [
        "Depending on the section: describe the work of teachers and other education professionals in Florida.",
        "Depending on the section: discuss a current issue in education with evidence from research and policy.",
        "Depending on the section: observe a classroom or educational setting and reflect on it.",
    ],
    'opt_top': [
        "The teaching profession and routes into it in Florida.",
        "A current issue in education policy or practice.",
        "Learning and development in children and adolescents.",
    ],
    'careers': [
        "Teachers (SOC 25-2021 elementary, 25-2031 secondary) and other education roles: a first-year topics "
        "course is exploratory and does not count toward Florida teacher certification on its own.",
        "Any section with observation in schools may require background screening; see the syllabus.",
    ],
    'learn': [
        "Related course on this site: " + site('EDF1005', 'Introduction to the Teaching Profession') + ", the "
        "standard first course for future teachers in Florida.",
    ],
})

for cid, g in G.items():
    order = ['title', 'html_content', 'credits', 'contact_hours', 'prerequisites', 'version', 'offering_notes']
    out = {k: g[k] for k in order}
    p = os.path.join('drafts', '%s_guide.json' % cid)
    with io.open(p, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print(cid, 'html', len(out['html_content']), 'prereq', len(out['prerequisites']))
