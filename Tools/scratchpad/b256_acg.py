# -*- coding: utf-8 -*-
"""Batch 256 (ACG and single-carrier group): limited-information and experiential guides for seven requested
courses that had been held or declined (run from Tools/).

    python scratchpad/b256_acg.py

Kinds (Tools/CLAUDE.md, "EVERY REQUESTED COURSE GETS A GUIDE", Ron 2026-11-24):
  ACG2061, ACG2072, ACG5875, PET1170, BCN6788, AVM1160 - limited information (one carrier)
  ACG4940                                               - experiential (internship)

Sources read 2026-11-24 (every outside link in Where to Learn More was fetched in this session):
  SCNS flat file (scratchpad/crslist.txt) - carriers, credits, statewide titles, effective dates.
  Hillsborough College 2025-2026 catalogue PDF (hccfl.edu/media/14324) - ACG2061 description and programmes.
  Polk State catalogue 2025-2026 (catoid=54, coid=87005) - ACG2072 description; the 2026-27 entry shows the title only.
  FGCU catalogue ACG course list - ACG4940; USF course details + Bellini Center internship page - ACG4940;
  Chipola archived syllabus page + PDF - ACG4940; FIU Coursedog cache (scratchpad/fiu_courses.json) - ACG4940, BCN6788C.
  Miami Dade competency PDFs (PET1170, AVM1160), MDC Aviation Maintenance Management page and course sequence guide.
  UF Rinker School BCN 6785 syllabi (Spring 2025, Fall 2025). UF's catalogue (catalog.ufl.edu) refused connection.
  Florida Statutes 473.306, 473.308, 1009.286, 1012.55 (2026). 14 CFR 91.409 and 121.367 (LII). FAA AC 120-16D.
"""
import io
import json
import os

REPO = 'https://floridacourserepo.com/courses/'


def c(cid, title):
    return '<a href="%s%s">%s %s</a>' % (REPO, cid, cid, title)


def ext(url, text):
    return '<a href="%s">%s</a>' % (url, text)


def ul(items):
    return '<ul>' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'


def lg(items):
    return '<ul class="list-group list-group-flush">' + ''.join(
        '<li class="list-group-item">%s</li>' % i for i in items) + '</ul>'


def box(kind, text):
    return '<div class="alert alert-warning"><strong>%s</strong> %s</div>' % (kind, text)


def table(rows):
    h = ('<table class="table table-sm"><thead><tr><th>Institution</th><th>Title</th><th>Credits</th>'
         '<th>Contact hours</th></tr></thead><tbody>')
    return h + ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % r for r in rows) + '</tbody></table>'


G = {}

# ====================================================================== ACG2061
G['ACG2061'] = {
    'title': 'Computers and Accounting',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "Hillsborough College, the only Florida public carrier, lists ACG 2021 (Financial Accounting) as the "
        "prerequisite and ACG 2071 (Managerial Accounting) as a co-requisite, and states that college-level reading, "
        "writing and math skills are required. It is a separate course from Hillsborough's ACG 2450 Microcomputers in "
        "Accounting (prerequisites ACG 2021, ACG 2071 and CGS 1000), which the Accounting Technology A.S. places in the "
        "term before it. ACG 2061 is itself a prerequisite of ACG 2960 Comprehensive Examination - Financial Option, the "
        "capstone of that degree, so a student in the Financial Option cannot skip it."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries ACG2061: Hillsborough College, at 3 credits.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': "Hillsborough publishes no contact hours for the course; 45 is Florida's convention for a "
                      "3-credit lecture course (15 hours per credit).",
        'offerings': [{
            'institution': 'HC', 'institution_name': 'Hillsborough College',
            'title': 'Computers and Accounting', 'credits': 3, 'contact_hours': None,
            'note': 'Prerequisite ACG 2021; co-requisite ACG 2071. Listed as "Computers in Accounting" in the '
                    'Accounting Technology A.S. (Financial Option), year II, first term; also in the Accounting '
                    'Technology Management certificate and as an elective in the A.A. Accounting Pathway '
                    '(2025-2026 catalogue).'}],
    },
}
G['ACG2061']['html_content'] = (
    "<h2>Course Description</h2>"
    + box('Limited information.',
          "Only <em>Hillsborough College</em> offers ACG2061 in Florida's public colleges and universities, and it "
          "publishes a one-sentence description. This guide sets out what the record shows and what a course of this "
          "kind commonly covers. Check the college's syllabus before relying on it.") +
    "<p><strong>ACG2061 Computers and Accounting</strong> is a 3-credit lower-division accounting course. Hillsborough "
    "College's 2025-2026 catalogue describes it in one sentence: <em>This course teaches various computerized accounting "
    "applications, including the use of Excel, to prepare accounting records and reports and interpret accounting "
    "information.</em> It requires ACG 2021 Financial Accounting first and ACG 2071 Managerial Accounting alongside or "
    "before it.</p>"
    "<p>Hillsborough uses the course in three places: the <strong>Accounting Technology A.S., Financial Option</strong> "
    "(60 credits), where it sits in the first term of the second year under the name <em>Computers in Accounting</em>; "
    "the <strong>Accounting Technology Management</strong> college credit certificate; and the list of electives in the "
    "<strong>A.A. Accounting Pathway</strong>. In the A.S. it follows <strong>ACG 2450 Microcomputers in "
    "Accounting</strong>, Hillsborough's general course on using computers to prepare and analyse accounting records, "
    "and it is a prerequisite of the programme's capstone, ACG 2960.</p>"
    "<p>Beyond the one sentence, Hillsborough publishes no outline. The description's emphasis on <strong>Excel</strong> "
    "and on <em>interpreting</em> accounting information suggests a spreadsheet-centred course that builds on the "
    "bookkeeping software of ACG 2450; the outcomes below are what a course of that description commonly covers, with the "
    "guesses about emphasis marked optional.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>"
    + lg([
        "Use computerized accounting applications to record transactions and prepare accounting records.",
        "Use <strong>Excel</strong> to prepare accounting records and reports, including financial statements and "
        "supporting schedules.",
        "Interpret the accounting information that the records and reports produce.",
    ]) +
    "<h3>Optional Outcomes</h3>"
    + lg([
        "Build spreadsheet models with formulas, cell references and functions commonly used in accounting "
        "(SUM, IF, lookup functions, financial functions such as PMT and depreciation functions).",
        "Prepare managerial schedules in a spreadsheet: budgets, cost-volume-profit analyses, variance reports "
        "(in step with the co-requisite ACG 2071).",
        "Analyse data with sorting, filtering, PivotTables and charts.",
        "Reconcile accounts and check a spreadsheet for errors.",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>"
    + lg([
        "Computerized accounting applications and the accounting cycle.",
        "Spreadsheets for accounting records and reports.",
        "Reading and interpreting the reports produced.",
    ]) +
    "<h3>Optional Topics</h3>"
    + lg([
        "Spreadsheet design, formulas and functions; templates.",
        "Financial statement preparation and analysis (ratios, trends) in a spreadsheet.",
        "Payroll, depreciation and loan schedules.",
        "Budgets and managerial analyses.",
        "Data tools: PivotTables, charts, what-if analysis.",
        "Commercial accounting software, if the section pairs it with Excel.",
    ]) +
    "<h2>Resources &amp; Tools</h2>"
    + ul([
        "Microsoft Excel (Hillsborough's description names it).",
        "A financial and managerial accounting text for the underlying accounting; the syllabus names any "
        "spreadsheet workbook used.",
    ]) +
    "<h2>Career Pathways</h2>"
    + ul([
        "Bookkeeping, accounting and auditing clerks (SOC 43-3031).",
        "Accountants and auditors (SOC 13-2011), after a bachelor's degree.",
        "Payroll and timekeeping clerks (SOC 43-3051) and other accounting support roles.",
    ]) +
    "<h2>Where to Learn More</h2>"
    + ul([
        ext('https://www.hccfl.edu/media/14324', "Hillsborough College 2025-2026 catalogue (PDF)") + " - the course "
        "description and the programmes that use ACG 2061 (search the PDF for <em>ACG 2061</em>).",
        c('ACG2450', 'Microcomputers in Accounting') + " - the computerized accounting course most Florida colleges "
        "teach, the nearest relative of ACG2061 under another number.",
        c('ACG2021', 'Financial Accounting') + " - the prerequisite.",
        c('ACG2071', 'Managerial Accounting') + " - the co-requisite.",
        ext('https://ccbcmd.edu/Programs-and-Courses-Finder/course/ACCT/133.html',
            'Community College of Baltimore County, ACCT 133 Excel for Accounting and Business') + " - a similar "
        "course, not an equivalent for transfer.",
        ext('https://openstax.org/books/principles-financial-accounting/pages/1-why-it-matters',
            'OpenStax, <em>Principles of Accounting, Volume 1: Financial Accounting</em>') + " - a free textbook for "
        "the accounting the spreadsheets record.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>"
    + table([('Hillsborough College', 'Computers and Accounting', '3',
              "not published (45 by Florida's 15-hours-per-credit convention)")]) +
    "<p>Hillsborough's catalogue uses two names for the course: <em>Computers and Accounting</em> in the course "
    "descriptions (and in the statewide record) and <em>Computers in Accounting</em> in the A.S. programme listing. "
    "They are the same course.</p>"
    "<h3>Transfer</h3><p>No other Florida public institution carries the number, so a receiving college will usually "
    "count ACG2061 as an accounting elective, or compare it with ACG 2450. A.S. graduates who continue to a bachelor's "
    "degree should keep the syllabus.</p>"
    "<h2>AI Integration (Optional)</h2>"
    "<p>AI assistants built into spreadsheets now write formulas, explain errors and draft charts. They help with the "
    "mechanics, but the accountant is responsible for the numbers: check every generated formula on a case worked by "
    "hand, and never paste a client's or employer's financial records into a public AI tool. Follow the instructor's "
    "rules on AI use for each assignment.</p>"
)

# ====================================================================== ACG2072
G['ACG2072'] = {
    'title': 'Accounting for Professionals',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "Polk State College, the only Florida public carrier, requires completion of MAT 1033 (Intermediate Algebra) "
        "or MAT 1100, or an appropriate placement examination score. No accounting course is required first: the "
        "course starts with debits, credits and journal entries. Polk marks it \"AA Elective: No\", so it does not "
        "count as an elective in the Associate in Arts. It is not a substitute for ACG 2021 Financial Accounting or "
        "ACG 2071 Managerial Accounting, the two principles courses a business transfer student needs, so check with "
        "an adviser before taking it in their place."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries ACG2072: Polk State College, at 3 credits (3 hours lecture).',
        'hours_source': 'published',
        'derived_contact_hours': 45,
        'derivation': 'Polk publishes 3 hours of lecture a week; 45 over a 15-week term.',
        'offerings': [{
            'institution': 'PSC', 'institution_name': 'Polk State College',
            'title': 'Accounting for Professionals', 'credits': 3, 'contact_hours': 45,
            'note': '3 hours lecture a week. Prerequisite MAT 1033 or MAT 1100, or placement score. Not an A.A. '
                    'elective. Statewide title: Cost Accounting for Business.'}],
    },
}
G['ACG2072']['html_content'] = (
    "<h2>Course Description</h2>"
    + box('Limited information.',
          "Only <em>Polk State College</em> offers ACG2072 in Florida's public colleges and universities, and it "
          "publishes a short description. This guide sets out what the record shows and what a course of this kind "
          "commonly covers. Check the college's syllabus before relying on it.") +
    "<p><strong>ACG2072 Accounting for Professionals</strong> is a 3-credit lower-division course at Polk State "
    "College. Polk's 2025-2026 catalogue describes it this way: <em>This is a survey course of financial accounting "
    "that emphasizes the study of cost accounting for manufacturing and non-manufacturing entities. Students study "
    "debits, credits, and journal entries, as well as preparation of financial statements. The course provides a study "
    "of cost accounting that concentrates on cost terminology and concepts, as well as cost analyses for management "
    "decision making.</em> It meets for 3 hours of lecture a week.</p>"
    "<h3>The two names for the number</h3>"
    "<p>The statewide course record titles ACG2072 <strong>Cost Accounting for Business</strong>; Polk calls it "
    "<strong>Accounting for Professionals</strong>. The two names describe the same course from different sides. "
    "<em>Cost Accounting for Business</em> names its subject: a first course in cost accounting for students who are "
    "not accounting majors. <em>Accounting for Professionals</em> names its audience: people who will use accounting "
    "in their work (in a trade, a health or technical field, a small business) rather than prepare it for a living. "
    "Polk's description covers both: a quick survey of financial accounting, then cost accounting for decisions.</p>"
    "<p>This is a <strong>survey</strong>, not the two principles courses. A student heading for a business degree "
    "takes ACG 2021 Financial Accounting and ACG 2071 Managerial Accounting, which cover the same ground in two terms "
    "and are the common prerequisites for transfer; ACG2072 compresses parts of both into one.</p>"
    "<p>⚠ Polk's 2026-2027 catalogue lists the course by title only, with no description; the 2025-2026 text is the "
    "most recent published. Confirm with Polk that the course is still scheduled.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>"
    + lg([
        "Record business transactions with <strong>debits, credits and journal entries</strong>.",
        "Prepare basic <strong>financial statements</strong>: income statement, balance sheet and the link between "
        "them.",
        "Use <strong>cost terminology and concepts</strong>: direct and indirect costs, fixed and variable costs, "
        "product and period costs.",
        "Apply cost accounting to <strong>manufacturing and non-manufacturing</strong> (service and merchandising) "
        "organisations.",
        "Carry out <strong>cost analyses for management decisions</strong>.",
    ]) +
    "<h3>Optional Outcomes</h3>"
    + lg([
        "Compute product costs by job order costing, and recognise when process costing applies.",
        "Use cost-volume-profit analysis to find a break-even point and a target profit.",
        "Prepare a simple budget and compare results with it.",
        "Make short-term decisions with relevant costs (make or buy, special orders, pricing).",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>"
    + lg([
        "The accounting equation, debits and credits, journals and ledgers.",
        "Financial statements.",
        "Cost terminology and cost behaviour.",
        "Costing in manufacturing and non-manufacturing entities.",
        "Cost analysis for management decision making.",
    ]) +
    "<h3>Optional Topics</h3>"
    + lg([
        "Job order and process costing; overhead allocation.",
        "Cost-volume-profit analysis.",
        "Budgeting.",
        "Relevant costs and short-term decisions.",
    ]) +
    "<h2>Resources &amp; Tools</h2>"
    + ul([
        "A survey or managerial accounting textbook; the Polk syllabus names the one used.",
        "A spreadsheet for cost schedules and break-even analyses.",
    ]) +
    "<h2>Career Pathways</h2>"
    + ul([
        "Accounting is a support skill here rather than the career: the course suits students in technical, health, "
        "trade and management programmes who will run budgets or price work.",
        "First-line supervisors and managers who are responsible for costs, and owners of small businesses.",
        "Bookkeeping, accounting and auditing clerks (SOC 43-3031), with further accounting courses.",
    ]) +
    "<h2>Where to Learn More</h2>"
    + ul([
        ext('https://catalog.polk.edu/preview_course_nopop.php?catoid=54&coid=87005',
            'Polk State College catalogue 2025-2026: ACG 2072') + " - the description, credits and prerequisites "
        "quoted above.",
        c('ACG2021', 'Financial Accounting') + " and " + c('ACG2071', 'Managerial Accounting') + " - the two "
        "principles courses that cover this ground in full at every Florida college.",
        c('ACG3341', 'Cost Accounting') + " - the upper-division cost accounting course for accounting majors.",
        ext('https://openstax.org/books/principles-managerial-accounting/pages/2-why-it-matters',
            'OpenStax, <em>Principles of Accounting, Volume 2: Managerial Accounting</em>') + " - a free textbook; "
        "chapter 2 covers cost behaviour and chapter 4 job order costing.",
        ext('https://openstax.org/books/principles-financial-accounting/pages/1-why-it-matters',
            'OpenStax, <em>Principles of Accounting, Volume 1: Financial Accounting</em>') + " - the financial "
        "accounting half: transactions, journal entries and statements.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>"
    + table([('Polk State College', 'Accounting for Professionals', '3', '3 a week lecture (45 a term)')]) +
    "<p>Polk marks the course <strong>AA Elective: No</strong>: it does not count toward the electives of the "
    "Associate in Arts.</p>"
    "<h3>Transfer</h3><p>No other Florida public institution carries ACG2072. A receiving college will compare it "
    "with ACG 2021 and ACG 2071 and will usually not accept one survey course for both. Keep the syllabus.</p>"
)

# ====================================================================== ACG5875
G['ACG5875'] = {
    'title': 'Development of Accounting Thought',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "Florida A&M University, the only Florida public carrier, publishes no prerequisites that could be read for "
        "this guide. As a 5000-level graduate accounting course it normally requires admission to a graduate "
        "accounting or business programme, or the department's permission, and assumes the undergraduate accounting "
        "core (intermediate financial accounting in particular). Check FAMU's School of Business and Industry for the "
        "current requirement and whether the course is scheduled."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries ACG5875: Florida A&M University, at 3 graduate credits.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': "FAMU publishes no contact hours; 45 is Florida's convention for a 3-credit lecture or "
                      "seminar course.",
        'offerings': [{
            'institution': 'FAMU', 'institution_name': 'Florida A&M University',
            'title': 'Development of Accounting Thought', 'credits': 3, 'contact_hours': None,
            'note': 'Graduate. Statewide title: Grad History of Accounting. Record effective 1990, last changed 2006.'}],
    },
}
G['ACG5875']['html_content'] = (
    "<h2>Course Description</h2>"
    + box('Limited information.',
          "Only <em>Florida A&amp;M University</em> offers ACG5875 in Florida's public colleges and universities, and "
          "it publishes only a title and credits. This guide sets out what the record shows and what a course of this "
          "kind commonly covers. Check the university's syllabus before relying on it.") +
    "<p><strong>ACG5875 Development of Accounting Thought</strong> is a 3-credit graduate accounting course at "
    "Florida A&amp;M University. The statewide course record titles it <strong>Grad History of Accounting</strong>. "
    "The record has been active since 1990 and was last changed in 2006; FAMU's description could not be read for this "
    "guide, so whether and how often the course is scheduled now is not known.</p>"
    "<p>Courses with this title, at other universities, study accounting's ideas over time: how double-entry "
    "bookkeeping arose, how theories of income and asset valuation developed, how standard setting came about, and why "
    "today's rules are the way they are. They ask <em>why</em> accounting is done as it is, where earlier courses taught "
    "<em>how</em>. What follows is what such a course commonly covers.</p>"
    "<p>The same statewide course is taught elsewhere in Florida under a different number and with a different "
    "emphasis: the University of South Florida's <strong>ACG6875 Financial Reporting and Professional Issues</strong>. "
    "Florida International University taught it as ACG6875 Evolution of Accounting Thought until 2024.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>"
    + lg([
        "Trace the <strong>historical development of accounting</strong> and accounting thought, from early record "
        "keeping and double-entry bookkeeping to the present.",
        "Explain how economic, legal and institutional change shaped accounting practice and theory.",
    ]) +
    "<h3>Optional Outcomes</h3>"
    + lg([
        "Compare the main schools of accounting theory (income determination, asset valuation, the decision-usefulness "
        "approach) and the criteria for choosing between them.",
        "Explain the origins of the US standard-setting bodies and the conceptual framework.",
        "Evaluate a current reporting controversy in the light of its history.",
        "Write a research paper using historical sources.",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>"
    + lg([
        "Early accounting and the spread of double-entry bookkeeping.",
        "The development of accounting thought and theory over time.",
    ]) +
    "<h3>Optional Topics</h3>"
    + lg([
        "The rise of the corporation, auditing and the accounting profession.",
        "Theories of income and capital; historical cost and current value.",
        "Standard setting in the United States and internationally; the conceptual framework.",
        "Accounting failures and the regulation that followed them.",
    ]) +
    "<h2>Career Pathways</h2>"
    + ul([
        "Accountants and auditors (SOC 13-2011) completing a master's degree, including the hours Florida requires for "
        "CPA licensure.",
        "Doctoral study and teaching in accounting (postsecondary business teachers, SOC 25-1011).",
    ]) +
    "<h2>Where to Learn More</h2>"
    + ul([
        c('ACG6875', 'Financial Reporting and Professional Issues') + " - the same statewide course at the University "
        "of South Florida, with a different emphasis.",
        ext('https://utpb.smartcatalogiq.com/en/2024-2025/2024-2025-graduate-catalog/courses/acct-accountancy/6000/acct-6312',
            'University of Texas Permian Basin, ACCT 6312 Accounting Theory') + " - historical development of "
        "accounting theory; a similar course, not an equivalent for transfer.",
        ext('https://ccsu.smartcatalogiq.com/en/current/undergraduate-graduate-catalog/all-courses/ac-accounting/500/ac-551',
            'Central Connecticut State University, AC 551 Evolution of Modern Accounting') + " - accounting from "
        "double-entry bookkeeping to the present; a similar course, not an equivalent for transfer.",
        ext('https://egrove.olemiss.edu/aah_notebook/', "<em>The Accounting Historians Notebook</em>") + " - a "
        "publication of the Academy of Accounting Historians, held free in the University of Mississippi's eGrove "
        "repository.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>"
    + table([('Florida A&amp;M University', 'Development of Accounting Thought', '3',
              "not published (45 by Florida's convention)")]) +
    "<h3>CPA licensure</h3><p>Florida licenses CPAs after 150 semester hours of college education, with a "
    "concentration in accounting and business (s. 473.308, Florida Statutes), and graduate accounting courses are a "
    "common way to complete them. Whether this course counts toward the Board of Accountancy's accounting hours depends "
    "on the Board's rule; ask FAMU's accounting department.</p>"
)

# ====================================================================== ACG4940
G['ACG4940'] = {
    'title': 'Accounting Internship',
    'credits': 3,
    'contact_hours': 120,
    'prerequisites': (
        "Set by each institution. FGCU: ACG 3113 and ACG 3401, prior approval of the Accounting Internship "
        "Coordinator, departmental approval. USF: at least 80 credits, admission to the accounting major, a 2.75 GPA "
        "in business courses (the catalogue; the Bellini Center page says 2.5), C or better in the major's foundation "
        "course, a secured internship, and for accounting majors one completed semester in the major. FIU: "
        "permission of the instructor. Chipola: an approved placement under an industry professional, a faculty "
        "adviser and the internship director. All require the internship to be arranged before registration; none "
        "gives credit for past work."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'Four Florida public institutions carry ACG4940. FGCU, FIU and USF at 3 credits; Chipola College at '
                   '1 to 6 credits (variable).',
        'hours_source': 'mixed',
        'derived_contact_hours': 120,
        'derivation': 'An internship has on-site hours rather than class hours. USF publishes a minimum of 120 hours '
                      'on site for 3 credits (10 a week); Chipola publishes at least 35 hours on the job per credit '
                      '(105 for 3). FGCU and FIU publish no hours. 120 is USF\'s published figure.',
        'offerings': [
            {'institution': 'FGCU', 'institution_name': 'Florida Gulf Coast University',
             'title': 'Accounting Internship', 'credits': 3, 'contact_hours': None,
             'note': 'S/U only. Prerequisites ACG 3113 and ACG 3401; departmental approval; prior approval of the '
                     'Accounting Internship Coordinator; written report at the end.'},
            {'institution': 'FIU', 'institution_name': 'Florida International University',
             'title': 'Accounting Internship', 'credits': 3, 'contact_hours': None,
             'note': 'Instructor consent required. Graded. Repeatable. Fall, Spring and Summer.'},
            {'institution': 'USF', 'institution_name': 'University of South Florida',
             'title': 'Accounting Internship Course', 'credits': 3, 'contact_hours': 120,
             'note': 'At least 120 hours on site (10 a week) plus an academic professional-development component. '
                     '80 credits, admitted to the major, 2.75 business GPA (catalogue). Fall, Spring and Summer.'},
            {'institution': 'CC', 'institution_name': 'Chipola College',
             'title': 'Accounting Internship', 'credits': None, 'contact_hours': None,
             'note': '1 to 6 credits (variable). At least 35 hours on the job per credit. Bachelor\'s-level course '
                     'in Chipola\'s business programme.'}],
    },
}
G['ACG4940']['html_content'] = (
    "<h2>Course Description</h2>"
    + box('Experiential course.',
          "ACG4940 is an <em>internship</em>: the credit is earned for supervised work in accounting, and what is "
          "learned depends on the placement. This guide explains how an accounting internship course works at the "
          "four Florida public institutions that carry the number. It is not a syllabus; each institution's "
          "internship office sets the requirements.") +
    "<p><strong>ACG4940 Accounting Internship</strong> is the upper-division internship number in accounting. The "
    "statewide record files it as <em>Internships/Practicums/Clinical Practice</em>, the general shell for supervised "
    "work experience. Four Florida public institutions carry it: <strong>Florida Gulf Coast University</strong>, "
    "<strong>Florida International University</strong> and the <strong>University of South Florida</strong> at 3 "
    "credits, and <strong>Chipola College</strong> at 1 to 6.</p>"
    "<p>What each publishes:</p><ul>"
    "<li><strong>FGCU:</strong> <em>Supervised work experience in accounting. Students must obtain prior approval from "
    "the Accounting Internship Coordinator and submit a written report at the end of the internship.</em> Graded S/U "
    "only; departmental approval required; prerequisites ACG 3113 and ACG 3401. FGCU's B.S. in Accounting lists it "
    "among the major's restricted electives.</li>"
    "<li><strong>USF:</strong> a course with an academic component on professional development skills and an on-site "
    "component of at least 120 hours (10 hours a week). It must be taken while doing the internship; credit is not "
    "given for past internships. USF's Bellini Center for Talent Development runs the application.</li>"
    "<li><strong>FIU:</strong> 3 credits, instructor's consent required, graded, offered in fall, spring and summer, "
    "and repeatable. FIU's record carries the statewide shell's wording, <em>practical application in a clinical "
    "setting of knowledge acquired in the classroom</em>.</li>"
    "<li><strong>Chipola College:</strong> hands-on experience in accounting through on-the-job practice, under an "
    "approved industry professional, a faculty adviser and the internship director, with <strong>at least 35 hours on "
    "the job for each semester hour of credit</strong>; 1 to 6 credits. Its syllabus asks students to compare the work "
    "with the management theory they have studied and to bring together the concepts of their other business "
    "courses.</li></ul>" +
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>"
    + lg([
        "Apply accounting knowledge from the classroom to the work of an accounting office, under supervision.",
        "Demonstrate professional conduct: communication, reliability, appearance and ethical behaviour in the "
        "workplace.",
        "Reflect on the experience in the written work the institution requires (FGCU's end-of-internship report, "
        "USF's professional development assignments, Chipola's assignments).",
    ]) +
    "<h3>Optional Outcomes</h3>"
    + lg([
        "Relate the placement's work to the professional standards and ethics rules of public accounting.",
        "Assess one's fit with a field of accounting (audit, tax, advisory, corporate, government) before choosing a "
        "first job or a master's programme.",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>"
    + lg([
        "Finding and securing an approved placement; the learning agreement with the employer and faculty supervisor.",
        "The work itself, which depends on the placement.",
        "Evaluation: the site supervisor's evaluation, the faculty supervisor's review of the written work, and the "
        "grade (S/U at FGCU; graded at FIU).",
    ]) +
    "<h3>Optional Topics</h3>"
    + lg([
        "Professional development sessions: résumé, interviewing, workplace communication (USF's academic component).",
        "The path to CPA licensure in Florida.",
    ]) +
    "<h2>Career Pathways</h2>"
    + ul([
        "Accountants and auditors (SOC 13-2011): public accounting firms, corporations, government and non-profits. "
        "Internships are the usual route into a first audit or tax position.",
        "Tax examiners and preparers, financial analysts and internal auditors.",
    ]) +
    "<h2>Where to Learn More</h2>"
    + ul([
        ext('https://catalog.fgcu.edu/courses/acg/', 'FGCU catalogue, Accounting (ACG) courses') + " - the ACG 4940 "
        "entry quoted above.",
        ext('https://cloud.usf.edu/academic-programs/details/prefix/ACG/code/4940', 'USF course details, ACG 4940') +
        " - credits, description and eligibility.",
        ext('https://www.usf.edu/business/talent-development/internships-types.aspx',
            'USF Bellini Center for Talent Development: internship types') + " - how the 3-credit 4940 internship "
        "works: eligibility, hours, terms and pay.",
        ext('https://www.chipola.edu/archived-course-syllabi/acg4940/', 'Chipola College ACG 4940 syllabus page') +
        " - credits (1-6) and the 35-hours-per-credit rule.",
        c('ACG2949', 'Internship in Accounting') + " - the lower-division internship at the state colleges.",
        ext('http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0400-0499/0473/Sections/0473.306.html',
            's. 473.306, Florida Statutes') + " - the 120 semester hours required to sit for the CPA examination.",
        ext('http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0400-0499/0473/Sections/0473.308.html',
            's. 473.308, Florida Statutes') + " - the 150 semester hours and one year of experience required for "
        "licensure.",
        ext('http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=1000-1099/1009/Sections/1009.286.html',
            's. 1009.286, Florida Statutes') + " - the excess-hour surcharge, which does not count internship credit "
        "hours.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>"
    + table([
        ('Florida Gulf Coast University', 'Accounting Internship', '3', 'not published'),
        ('Florida International University', 'Accounting Internship', '3', 'not published'),
        ('University of South Florida', 'Accounting Internship Course', '3', 'at least 120 on site'),
        ('Chipola College', 'Accounting Internship', '1-6 (variable)', 'at least 35 on the job per credit'),
    ]) +
    "<h3>Enrolment</h3><p>At every carrier the placement comes first: the student finds (or is matched with) an "
    "approved internship, gets it approved by the department, then registers. USF requires the internship to be "
    "underway in the term of registration and does not give credit for past work. Apply early; firms recruit accounting "
    "interns a semester or more ahead, especially for the spring tax season.</p>"
    "<h3>Grading</h3><p>FGCU grades it S/U only; FIU and USF assign a grade. A pass/fail course can satisfy an "
    "elective but does not raise a GPA, which matters to students applying to graduate programmes.</p>"
    "<h3>CPA licensure in Florida</h3><p>Florida lets a candidate sit for the CPA examination after 120 semester hours "
    "with a concentration in accounting and business (s. 473.306) and licenses after <strong>150 semester hours</strong> "
    "and <strong>one year of work experience</strong> verified by a licensed CPA (s. 473.308). An internship does not by "
    "itself satisfy the experience requirement. Whether its credit counts toward the Board of Accountancy's accounting "
    "or business hours depends on the Board's rule: ask the department before counting on it.</p>"
    "<h3>Excess hours</h3><p>At the state universities (FGCU, FIU, USF), Florida's excess-hour surcharge does not count "
    "internship credit hours (s. 1009.286), so an internship does not push a student toward the surcharge. The rule "
    "does not apply at Chipola College.</p>"
    "<h3>Transfer</h3><p>An internship is credit for work done at one institution and rarely transfers as a course. A "
    "receiving university will usually count it as an elective, if at all. Chipola's credit is variable, so the transcript "
    "shows how many credits were earned.</p>"
)

# ====================================================================== PET1170
G['PET1170'] = {
    'title': 'Fundamentals of Athletic Coaching and Management',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "Miami Dade College, the only Florida public carrier, lists no prerequisite in the competency document for the "
        "course (updated Fall 2025). It is a lower-division course created in 2024 together with PET 1173 Strategies "
        "of Coaching and Competition. The course does not by itself qualify anyone to coach in a Florida public "
        "school: a district-employed coach needs a teaching or athletic coaching certificate and current CPR, first aid "
        "and AED certification (s. 1012.55(2), Florida Statutes)."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries PET1170: Miami Dade College, at 3 credits.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': "Miami Dade publishes no contact hours; 45 is Florida's convention for a 3-credit lecture "
                      "course.",
        'offerings': [{
            'institution': 'MDC', 'institution_name': 'Miami Dade College',
            'title': 'Fundamentals of Athletic Coaching and Management', 'credits': 3, 'contact_hours': None,
            'note': 'Record effective January 2024. Competency document updated Fall 2025. No prerequisite listed.'}],
    },
}
G['PET1170']['html_content'] = (
    "<h2>Course Description</h2>"
    + box('Limited information.',
          "Only <em>Miami Dade College</em> offers PET1170 in Florida's public colleges and universities. It publishes "
          "a course description and five competencies, quoted below, but no syllabus. This guide sets out what the "
          "record shows and what a course of this kind commonly covers. Check the college's syllabus before relying "
          "on it.") +
    "<p><strong>PET1170 Fundamentals of Athletic Coaching and Management</strong> is a 3-credit lower-division course "
    "at Miami Dade College, added to the statewide course record in 2024. Miami Dade describes it this way: <em>This course will introduce "
    "students to the basic principles of athletic coaching and team management. Students will discuss the fundamentals "
    "of developing an individual athlete and team, effective athlete training programming, and factors which impact "
    "the operations of athletic organizations. Students will develop an understanding of how policy and coaching "
    "decisions influence an organization at all levels.</em></p>"
    "<p>Its companion is <strong>PET 1173 Strategies of Coaching and Competition</strong>, created at Miami Dade at the "
    "same time. The course is for students who want to coach, in schools, clubs or colleges, or to work in the "
    "management of sport.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>"
    "<p>Miami Dade's five competencies, in its words:</p>"
    + lg([
        "Identify the basic concepts of effective <strong>training programming</strong>: the principles of structuring "
        "and managing a training programme, the challenges of planning and executing it, and best practices that use "
        "management principles and functions.",
        "Discuss the differences between <strong>coaching individuals and teams</strong>: individual athletes' needs, "
        "challenges and best practices at various levels, and strategies for a positive and cohesive team culture.",
        "Determine the <strong>factors that affect athlete and team performance</strong>: the coach's role and the "
        "coach-athlete relationship, internal and external factors, and learning from past performances.",
        "Analyse <strong>coaching methodologies and philosophies</strong>: coaching concepts, behaviour and learning "
        "styles; helping coaches and athletes handle stress; theories, motivational techniques and ethical "
        "responsibilities applied to real coaching situations.",
        "Integrate <strong>policies, regulations and resources</strong> into a team management plan: sport policy and "
        "the governance of intercollegiate, professional, private and public sport; key policies and resources; "
        "evaluating rules against the needs of the community and the athlete.",
    ]) +
    "<h3>Optional Outcomes</h3>"
    + lg([
        "Write a personal coaching philosophy.",
        "Plan a season: practice plans, periodisation, scheduling and budget.",
        "Describe a coach's legal duties and risk management, including emergency action plans.",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>"
    + lg([
        "Principles of athletic coaching and team management.",
        "Designing and managing athlete training programmes.",
        "Coaching individuals and teams; team culture.",
        "The coach-athlete relationship and the factors in performance.",
        "Coaching philosophies, motivation, stress and ethics.",
        "Sport policy, governance and the operation of athletic organisations.",
    ]) +
    "<h3>Optional Topics</h3>"
    + lg([
        "Florida's rules for school coaches: certification, CPR/first aid/AED, the Florida High School Athletic "
        "Association.",
        "NCAA, NJCAA and club governance.",
        "Budgets, fundraising and facilities.",
    ]) +
    "<h2>Career Pathways</h2>"
    + ul([
        "Coaches and scouts (SOC 27-2022): school, club, college and recreation coaching.",
        "Recreation workers and athletic programme staff.",
        "A starting point for degrees in sport management, physical education or exercise science.",
    ]) +
    "<h2>Where to Learn More</h2>"
    + ul([
        ext('https://www.mdc.edu/asa/documents/competencies/pdf/PET1170%20Fundamentals%20of%20Athletic%20Coaching%20and%20Management.pdf',
            'Miami Dade College, PET 1170 course competencies (PDF)') + " - the description and competencies quoted "
        "above.",
        c('PET1173', 'Strategies of Coaching and Competition') + " - Miami Dade's companion coaching course.",
        c('SPM2000', 'Introduction to Sport Management') + " - the management side of sport, at Florida colleges.",
        ext('http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=1000-1099/1012/Sections/1012.55.html',
            's. 1012.55, Florida Statutes') + " - subsection (2): what a coach employed by a Florida school district "
        "must hold.",
        ext('https://gcsu.smartcatalogiq.com/en/2024-2025/undergraduate-catalog/course-descriptions/kins-kinesiology/3000/kins-3413',
            'Georgia College &amp; State University, KINS 3413 Principles of Coaching') + " - a similar course, not an "
        "equivalent for transfer.",
        ext('https://unco.smartcatalogiq.com/en/current/undergraduate-catalog/course-descriptions/kin-kinesiology/300/kin-335',
            'University of Northern Colorado, KIN 335 Principles of Coaching') + " - a similar course, not an "
        "equivalent for transfer.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>"
    + table([('Miami Dade College', 'Fundamentals of Athletic Coaching and Management', '3',
              "not published (45 by Florida's convention)")]) +
    "<h3>Coaching in Florida schools</h3><p>A person employed as an athletic coach by a Florida school district must "
    "hold a temporary or professional educator certificate or an athletic coaching certificate, and current "
    "certification in CPR, first aid and the use of an AED (s. 1012.55(2)(a), Florida Statutes). Unpaid volunteer coaches "
    "not employed by a district are exempt. A college course in coaching supports this career but is not the "
    "certificate; the school district explains its route.</p>"
    "<h3>Transfer</h3><p>No other Florida public institution carries PET1170, so a receiving college will usually count "
    "it as an elective. Keep the competency document.</p>"
)

# ====================================================================== BCN6788
G['BCN6788'] = {
    'title': 'Construction Information Systems',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "The University of Florida, the only Florida public carrier of BCN6788, publishes no current prerequisites for "
        "it. UF's Rinker School teaches construction information systems under BCN 6785: its Spring 2025 syllabus "
        "required BCN 3255 Computer Graphic Communications or the professor's consent, and its Fall 2025 syllabus "
        "requires graduate standing only. Expect a graduate construction management course to require admission to a "
        "graduate programme. Before registering, confirm with the Rinker School which number is scheduled."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries BCN6788: the University of Florida, at 3 graduate credits. '
                   'UF now teaches the subject as BCN 6785; FIU carries BCN6788C, a different course on AI in '
                   'construction management.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': "No contact hours are published for BCN6788. UF's BCN 6785 syllabus states three lecture hours a "
                      "week, which is 45 a term, the same as Florida's convention for 3 credits.",
        'offerings': [{
            'institution': 'UF', 'institution_name': 'University of Florida',
            'title': 'Construction Information Systems', 'credits': 3, 'contact_hours': None,
            'note': 'Graduate. State record effective 1997, last changed 2005. UF teaches the subject now as BCN 6785 '
                    '(Construction Information Systems in Spring 2025; Advanced Construction Information Technology '
                    'from Fall 2025).'}],
    },
}
G['BCN6788']['html_content'] = (
    "<h2>Course Description</h2>"
    + box('Limited information.',
          "Only the <em>University of Florida</em> carries BCN6788 in Florida's public colleges and universities, and "
          "the number may no longer be scheduled: UF teaches its construction information systems course under "
          "<strong>BCN 6785</strong>. This guide sets out what the record shows and what UF's current course covers. "
          "Check with UF's Rinker School before relying on it.") +
    "<p><strong>BCN6788 Construction Information Systems</strong> is a 3-credit graduate course in construction "
    "management. The statewide course record lists the University of Florida as its only public carrier; the record "
    "dates from 1997 and was last changed in 2005. UF's catalogue could not be reached for this guide, and the course "
    "did not appear in UF's 2026-2027 catalogue when it was checked for the original request.</p>"
    "<p>UF's M.E. Rinker, Sr. School of Construction Management teaches the subject under another number. Its Spring "
    "2025 syllabus is headed <strong>BCN 6785 Construction Information Systems</strong> (3 credits): <em>This course "
    "will cover the fundamental principles and practices of Building Information Modeling (BIM) and Virtual Design "
    "and Construction (VDC). Additional lectures may also be supplemented to present the use of information systems "
    "in the construction context.</em> From Fall 2025 the same instructor's syllabus titles BCN 6785 "
    "<strong>Advanced Construction Information Technology</strong>: <em>Concepts of computer-aided construction, "
    "with a focus on the application of BIM-driven emerging information technologies used in the planning and "
    "management of construction projects.</em> The statewide record now shows that title for UF's BCN 6785.</p>"
    "<p>Florida International University carries a related number, <strong>BCN6788C Artificial Intelligence "
    "Applications in Construction Management</strong> (3 credits, spring term only): <em>a study of the concepts, "
    "techniques, and applications of AI technology in the construction management domain</em>. It shares the "
    "statewide course but teaches a different subject.</p>"
    "<p>What follows is what a graduate construction information systems course commonly covers, drawn from UF's "
    "BCN 6785 syllabi.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>"
    + lg([
        "Explain how information systems are used in construction management, and the principles of "
        "<strong>Building Information Modeling (BIM)</strong> and <strong>Virtual Design and Construction "
        "(VDC)</strong>.",
        "Create functional 3D models, with the necessary embedded information, from construction documents.",
        "Evaluate a model for modelling quality and reporting accuracy.",
        "Visualise and communicate construction concepts with 2D and 3D applications.",
    ]) +
    "<h3>Optional Outcomes</h3>"
    + lg([
        "Develop a BIM execution plan and manage the project information it governs.",
        "Produce quantity takeoffs and link a schedule to the model (4D).",
        "Coordinate models from different disciplines and resolve clashes in a coordination meeting.",
        "Use reality capture (laser scanning, photogrammetry) and cloud collaboration platforms.",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>"
    + lg([
        "Information systems in the construction industry.",
        "BIM and VDC: concepts, models and their information.",
        "Model quality and reporting.",
        "Visual communication of construction.",
    ]) +
    "<h3>Optional Topics</h3>"
    + lg([
        "BIM execution planning and standards.",
        "Clash detection and model coordination.",
        "Takeoffs, 4D scheduling and simulation.",
        "Common data environments and cloud collaboration.",
        "Emerging technologies, including AI in construction management.",
    ]) +
    "<h2>Resources &amp; Tools</h2>"
    + ul([
        "UF's BCN 6785 syllabi name Autodesk Revit, Navisworks Manage, Autodesk Construction Cloud, ReCap Pro, "
        "Twinmotion, Assemble Systems and cmBuilder; the Autodesk tools are free to students through the Autodesk "
        "Education Community.",
        "The National BIM Standard-United States (NBIMS-US).",
    ]) +
    "<h2>Career Pathways</h2>"
    + ul([
        "Construction managers (SOC 11-9021), project engineers and project managers.",
        "BIM and VDC coordinators and managers in general contractors and design-build firms.",
        "Cost estimators (SOC 13-1051) working from models.",
    ]) +
    "<h2>Where to Learn More</h2>"
    + ul([
        ext('https://dcp.ufl.edu/wp-content/uploads/2025/01/BCN6785-Construction-Information-Systems.pdf',
            'UF Rinker School, BCN 6785 Construction Information Systems syllabus (Spring 2025, PDF)') + " - the "
        "course UF teaches on this subject.",
        ext('https://dcp.ufl.edu/wp-content/uploads/2025/08/BCN-6785_FA2025.pdf',
            'UF Rinker School, BCN 6785 Advanced Construction Information Technology syllabus (Fall 2025, PDF)'),
        c('BCN6785', 'Advanced Construction Information Technology') + " - the number UF teaches it under (the site "
        "may show FIU's title for the same number, an estimating course).",
        c('BCN6788C', 'Artificial Intelligence Applications in Construction Management') + " - FIU's related course.",
        ext('https://engineering.purdue.edu/CCE/Academics/Undergraduate/Courses/CourseInfo/CCE522-Computer-Applications-in-Construction',
            'Purdue University, CCE 52200 Computer Applications in Construction') + " - a BIM course in a master's "
        "programme; a similar course, not an equivalent for transfer.",
        ext('https://www.nibs.org/nbims', 'National Institute of Building Sciences: National BIM Standard-United '
            'States') + " - the consensus standard for BIM uses, planning and information exchange.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>"
    + table([('University of Florida', 'Construction Information Systems', '3',
              "not published (45 by convention; UF's BCN 6785 meets three hours a week)")]) +
    "<h3>Is the course still taught?</h3><p>The statewide record still lists BCN6788 as active at UF, but the subject is "
    "taught under BCN 6785, and BCN6788 was not found in UF's 2026-2027 catalogue. Treat BCN6788 as possibly "
    "dormant: a student or adviser looking for this course should ask the Rinker School about BCN 6785.</p>"
    "<h2>AI Integration (Optional)</h2>"
    "<p>Construction information systems are where AI is arriving fastest in the industry: automated clash grouping, "
    "takeoffs from drawings, schedule generation and site-progress tracking from images. FIU now teaches a course on "
    "it (BCN6788C). The construction manager stays responsible for what the model and its tools report, so check "
    "generated quantities and schedules against the documents, and keep project data within the platforms the "
    "project's contracts allow.</p>"
)

# ====================================================================== AVM1160
G['AVM1160'] = {
    'title': 'Aviation Maintenance Programs and Inspections',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "Miami Dade College, the only Florida public carrier, lists no prerequisite for the course in its Aviation "
        "Maintenance Management A.S. course sequence guide (effective Fall 2024), where it is taken in the third "
        "semester with AVM 2510 Airline Management and AVM 2515 Airline Marketing. The degree is designed for holders "
        "of the FAA Airframe and Powerplant (A&P) certificate, who are awarded 45 semester hours for it; Miami Dade "
        "strongly encourages students to hold the A&P before enrolling. The course is a management course, not an "
        "A&P training course."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries AVM1160: Miami Dade College, at 3 credits.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': "Miami Dade publishes no contact hours; 45 is Florida's convention for a 3-credit lecture "
                      "course.",
        'offerings': [{
            'institution': 'MDC', 'institution_name': 'Miami Dade College',
            'title': 'Aviation Maintenance Programs and Inspections', 'credits': 3, 'contact_hours': None,
            'note': 'Aviation Maintenance Management A.S. (83 credits), semester 3. Competency document updated '
                    'Fall 2025.'}],
    },
}
G['AVM1160']['html_content'] = (
    "<h2>Course Description</h2>"
    + box('Limited information.',
          "Only <em>Miami Dade College</em> offers AVM1160 in Florida's public colleges and universities. It publishes "
          "a course description and competencies, quoted below, but no syllabus. This guide sets out what the record "
          "shows and what a course of this kind commonly covers. Check the college's syllabus before relying on it.") +
    "<p><strong>AVM1160 Aviation Maintenance Programs and Inspections</strong> is a 3-credit course in Miami Dade "
    "College's <strong>Aviation Maintenance Management A.S.</strong> Miami Dade describes it this way: <em>This course "
    "provides an in-depth study of aircraft inspection programs and maintenance scheduling procedures. Students will "
    "learn national and international regulations governing aircraft inspection, maintenance evaluation, and the "
    "required procedures to update airline and governmental maintenance technical manuals.</em></p>"
    "<p>The degree (83 credits) is built for aviation maintenance technicians who already hold the FAA "
    "<strong>Airframe and Powerplant (A&amp;P)</strong> certificate: Miami Dade awards 45 semester hours for it, and the "
    "student completes 38 more in management, airline operations and general education. AVM1160 is taken in the third "
    "semester with AVM 2510 Airline Management and AVM 2515 Airline Marketing, and is followed by AVM 1162 (MRO "
    "interactions with airline operations) and AVM 1163 (policies and procedures for airline maintenance programmes). "
    "It looks at maintenance from the airline's and the maintenance manager's side: the programme that decides what "
    "is inspected, when, by whom and at what cost.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>"
    "<p>Miami Dade's competencies, summarised:</p>"
    + lg([
        "Identify the <strong>national and international regulations</strong> for maintaining commercial aircraft: "
        "airworthiness criteria, required maintenance records (content, format, archiving), the regulatory "
        "inspection process, and how airline and government maintenance manuals are updated.",
        "Identify the principles of an effective <strong>aviation maintenance programme</strong>: chronological and "
        "cycle-based inspection criteria, system and component reliability, non-destructive inspection, the "
        "Comprehensive Maintenance Management Program (CMMP), and predictive versus reactive maintenance intervals.",
        "Plan the <strong>people</strong> a maintenance programme needs: workforce size, qualifications, testing for "
        "hiring and advancement, job descriptions with initial and continuing training, and the maintenance safety "
        "team.",
        "Explain the <strong>financial benefits</strong> of an effective programme: part and engine life cycles, "
        "facilities and equipment, programmed maintenance that limits aircraft downtime, and the cost-effectiveness "
        "of training (including manufacturers' update seminars).",
        "Determine the content of <strong>pre-flight, post-flight, cycle, annual and progressive inspections</strong> "
        "and how well each finds problems in aircraft components.",
    ]) +
    "<h3>Optional Outcomes</h3>"
    + lg([
        "Compare an air carrier's continuous airworthiness maintenance programme with the general-aviation inspection "
        "options of 14 CFR 91.409.",
        "Read a maintenance planning document and build a check schedule (A-, C- and heavy checks).",
        "Explain reliability programmes and how their data change inspection intervals.",
    ]) +
    "<h2>Major Topics</h2><h3>Required Topics</h3>"
    + lg([
        "US (FAA) and international regulation of aircraft maintenance and inspection.",
        "Airworthiness, maintenance records and technical manuals.",
        "Inspection programmes: chronological, cycle-based, annual, 100-hour, progressive, pre- and post-flight.",
        "Reliability, non-destructive inspection and maintenance intervals.",
        "Staffing, qualification and training of maintenance personnel; the maintenance safety team.",
        "The economics of maintenance programmes and aircraft downtime.",
    ]) +
    "<h3>Optional Topics</h3>"
    + lg([
        "Air carrier maintenance programmes under 14 CFR Part 121 and FAA Advisory Circular 120-16.",
        "International rules (EASA, ICAO) for airlines and repair stations in South Florida's international market.",
        "Maintenance tracking software.",
    ]) +
    "<h2>Career Pathways</h2>"
    + ul([
        "Aircraft mechanics and service technicians (SOC 49-3011) moving into lead, inspector and supervisory roles.",
        "First-line supervisors of mechanics, installers and repairers (SOC 49-1011).",
        "Maintenance planners, controllers and quality assurance staff at airlines and repair stations (MROs).",
        "Miami International Airport and its cargo airlines, MROs and parts suppliers are a large employer base in "
        "South Florida.",
    ]) +
    "<h2>Where to Learn More</h2>"
    + ul([
        ext('https://www.mdc.edu/asa/documents/competencies/pdf/AVM1160%20Aviation%20Maintenance%20Programs%20and%20Inspections.pdf',
            'Miami Dade College, AVM 1160 course competencies (PDF)') + " - the description and competencies quoted "
        "above.",
        ext('https://www.mdc.edu/aviationmaintenance/', 'Miami Dade College, Aviation Maintenance Management A.S.') +
        " - the programme, and the 45 credits awarded for the A&amp;P certificate.",
        ext('https://cuv.mdc.edu/academics/programs/csg/AS_AviationMaintenanceManagement_csg.pdf',
            'Miami Dade College, Aviation Maintenance Management course sequence guide (PDF)') + " - where AVM 1160 "
        "sits in the degree.",
        c('AVM1162', 'Maintenance Repair and Overhaul (MRO) Interactions with Commercial Airline Operations') +
        " and " + c('AVM1163', 'Policies and Procedures for Commercial Airlines Maintenance Programs') + " - the "
        "courses that follow it at Miami Dade.",
        c('ASC2320', 'Aviation Law and Regulations') + " - the regulation course in the same degree.",
        ext('https://catalog.siu.edu/programs/avt/courses.php', 'Southern Illinois University, Aviation Technologies '
            'courses') + " - AVT 470 Reliability, Maintainability, and Fault Prediction and Analysis and AVT 485 "
        "(aerospace maintenance shop operations) are similar courses, not equivalents for transfer.",
        ext('https://www.law.cornell.edu/cfr/text/14/91.409', '14 CFR 91.409, Inspections') + " - annual, 100-hour and "
        "progressive inspections (Legal Information Institute).",
        ext('https://www.law.cornell.edu/cfr/text/14/121.367', '14 CFR 121.367') + " - every air carrier must have "
        "an inspection programme and a maintenance programme.",
        ext('https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC120-16D.pdf',
            'FAA Advisory Circular 120-16D, Air Carrier Maintenance Programs (2003, PDF)') + " - the elements of an "
        "air carrier maintenance programme; check the FAA's list for a later revision.",
    ]) +
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>"
    + table([('Miami Dade College', 'Aviation Maintenance Programs and Inspections', '3',
              "not published (45 by Florida's convention)")]) +
    "<h3>The A&amp;P certificate</h3><p>This course does not train or certify a mechanic. The FAA Airframe and "
    "Powerplant certificate comes from an FAA-approved aviation maintenance technician school (or documented "
    "experience) and FAA examinations. Miami Dade's degree builds management on top of it, and a student without the "
    "certificate must earn it elsewhere and transfer it back.</p>"
    "<h3>Transfer</h3><p>The Aviation Maintenance Management A.S. is a pathway to Miami Dade's B.A.S. in Supervision and "
    "Management. No other Florida public institution carries AVM1160, so elsewhere it will usually count as an "
    "elective.</p>"
)

ORDER = ['title', 'html_content', 'credits', 'contact_hours', 'prerequisites', 'version', 'offering_notes']
for cid, g in G.items():
    out = {k: g[k] for k in ORDER}
    p = os.path.join('drafts', '%s_guide.json' % cid)
    with io.open(p, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print(cid, 'html', len(out['html_content']), 'prereq', len(out['prerequisites']))
