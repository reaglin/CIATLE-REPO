# -*- coding: utf-8 -*-
"""Batch 251 (second half): the four accounting requests that arrived during the run. Writes drafts/ (run from Tools/).

    python scratchpad/b251_build2.py

Sources (2026-11-22): SCNS flat file (b251_count.py, b250_rows.py); NWFSC, FSCJ, FIU, FAU, FSU Coursedog caches;
UNF course API; catalog.ufl.edu; cloud.usf.edu; seminolestate.edu/catalog; phsc.smartcatalogiq.com; Florida Board
of Accountancy education requirements (myfloridalicense.com) and Rule 61H1-27.002, F.A.C.
"""
import io
import json
import os
import sys

sys.path.insert(0, 'scratchpad')
from b251_build import lg, ul, table, off  # noqa: E402  (the helpers only; importing also rewrites the first six)

NAMES = {
    'BC': 'Broward College', 'CC': 'Chipola College', 'CF': 'College of Central Florida',
    'CFK': 'The College of the Florida Keys', 'DSC': 'Daytona State College', 'EFSC': 'Eastern Florida State College',
    'FAMU': 'Florida A&M University', 'FAU': 'Florida Atlantic University', 'FGC': 'Florida Gateway College',
    'FGCU': 'Florida Gulf Coast University', 'FIU': 'Florida International University',
    'FLPOLY': 'Florida Polytechnic University', 'FSCJ': 'Florida State College at Jacksonville',
    'FSU': 'Florida State University', 'FSWSC': 'Florida SouthWestern State College',
    'GCSC': 'Gulf Coast State College', 'HC': 'Hillsborough College', 'IRSC': 'Indian River State College',
    'LSSC': 'Lake-Sumter State College', 'MDC': 'Miami Dade College', 'NFC': 'North Florida College',
    'NWFSC': 'Northwest Florida State College', 'PBSC': 'Palm Beach State College', 'PESC': 'Pensacola State College',
    'PHSC': 'Pasco-Hernando State College', 'PSC': 'Polk State College', 'SCFMS': 'State College of Florida',
    'SFC': 'Santa Fe College', 'SFSC': 'South Florida State College', 'SJRSC': 'St. Johns River State College',
    'SPC': 'St. Petersburg College', 'SSCF': 'Seminole State College', 'TSC': 'Tallahassee State College',
    'UCF': 'University of Central Florida', 'UF': 'University of Florida', 'UNF': 'University of North Florida',
    'USF': 'University of South Florida', 'UWF': 'University of West Florida'}

AI_ACG = ('<h2>AI Integration (Optional)</h2><p>AI is changing accounting work quickly: tools now read invoices, '
          'suggest journal entries, reconcile accounts and draft analysis, and the large firms use them in audit. '
          'That makes the judgement this course teaches more valuable, not less. A chat tool will produce a confident '
          'journal entry or cost calculation that is wrong &mdash; debits and credits reversed, a period-end '
          'adjustment missed, an arithmetic slip carried through &mdash; and only someone who knows the double-entry '
          'logic will catch it. Use AI to explain a concept or check your reasoning, then work every problem yourself; '
          'exams, and the CPA exam, are taken without it. Follow your instructor\'s policy.</p>')

G = {}

# ---------------------------------------------------------------------------------------------------- ACG2001
FA_COLLEGES = ['BC', 'GCSC', 'IRSC', 'MDC', 'NWFSC', 'PESC', 'SFC', 'SFSC', 'TSC']
TITLES_2001 = {'BC': 'Principles of Accounting I', 'GCSC': 'Principles of Financial Accounting I (honors section '
               'also)', 'IRSC': 'Financial Accounting I', 'MDC': 'Principles of Accounting 1', 'NWFSC': 'Accounting I',
               'PESC': 'Accounting I', 'SFC': 'Principles of Accounting I', 'SFSC': 'Financial Accounting I',
               'TSC': 'Principles of Accounting I'}
TITLES_2011 = {'BC': 'Principles of Accounting II', 'GCSC': 'Principles of Financial Accounting II',
               'IRSC': 'Financial Accounting II', 'MDC': 'Principles of Accounting 2', 'NWFSC': 'Accounting II',
               'PESC': 'Accounting II', 'SFC': 'Principles of Accounting II', 'SFSC': 'Financial Accounting II',
               'TSC': 'Principles of Accounting II'}
ALSO_2021 = {'MDC', 'NWFSC', 'PESC', 'SFC', 'SFSC', 'TSC'}

TWO_TERM = (
    '<h3>⚠ Two courses that together equal ACG2021</h3>'
    '<p>Most Florida institutions teach introductory financial accounting in <strong>one</strong> 3-credit course, '
    '<strong>ACG2021</strong> (35 public institutions). Nine state colleges also, or instead, teach it over '
    '<strong>two</strong> terms: <strong>ACG2001</strong> then <strong>ACG2011</strong>, 3 credits each. Northwest '
    'Florida State says so directly: <em>"ACG 2021 Financial Accounting is a combination of ACG 2001 Accounting I and '
    'ACG 2011 Accounting II."</em> Universities accept the pair in place of ACG2021: USF\'s Intermediate Financial '
    'Accounting I lists its prerequisite as <em>"ACG X021 OR ACG X021C OR ACG X001 AND ACG X011"</em>.</p>'
    + ul(['<strong>Take both.</strong> ACG2001 alone is half of the financial-accounting prerequisite; a university or '
          'business programme that requires ACG2021 will want ACG2011 as well.',
          '<strong>Six credits, not three.</strong> The pair carries 6 credits for what ACG2021 does in 3. The extra '
          'three are elective credit; they do not replace ACG2071 Managerial Accounting, which every business degree '
          'still requires.',
          'At Broward, Gulf Coast and Indian River the two-term sequence is the only financial-accounting route in the '
          'state file; Miami Dade, Northwest Florida, Pensacola, Santa Fe, South Florida and Tallahassee carry ACG2021 '
          'as well, so a student there can choose.',
          'Do not mix routes: a student who has ACG2001 and then transfers should finish with ACG2011 if the new '
          'institution offers it, or ask the department how ACG2021 will be counted. Taking ACG2021 after ACG2001 '
          'repeats half the content.']))

TWO_TERM_TABLE = lambda titles: table(['Institution', 'Its title', 'Credits', 'Also carries ACG2021?'], [
    [NAMES[c], titles[c], '3', 'yes' if c in ALSO_2021 else 'no'] for c in FA_COLLEGES])

G['ACG2001'] = dict(
    title='Principles of Accounting I (Financial Accounting I)',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("Usually none beyond college-level reading and math readiness; check your college. ⚠ The first of a "
                   "TWO-course sequence (ACG 2001 then ACG 2011, 3 credits each) that together equal ACG 2021 "
                   "Financial Accounting. Take both: ACG 2001 alone does not satisfy a programme or university "
                   "prerequisite of ACG 2021. Offered at nine Florida state colleges."),
    offering_notes={
        'summary': 'Nine Florida public institutions carry ACG2001, all state colleges and all at 3 credits: Broward, '
                   'Gulf Coast, Indian River, Miami Dade, Northwest Florida, Pensacola, Santa Fe, South Florida and '
                   'Tallahassee. With ACG2011 it equals ACG2021.',
        'hours_source': 'derived', 'derived_contact_hours': 45,
        'derivation': 'Florida convention of 15 contact hours per credit for a lecture course; no carrier publishes a '
                      'term contact-hour figure.',
        'offerings': [off(c, NAMES[c], TITLES_2001[c], 3,
                          'Also carries ACG2021.' if c in ALSO_2021 else 'Two-term sequence is its only route.')
                      for c in FA_COLLEGES]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>ACG2001</strong> is the first half of introductory financial accounting taught over two terms. It '
        'covers the language and mechanics of accounting: the accounting equation, double-entry bookkeeping and the '
        'full accounting cycle, the four financial statements, and the first groups of assets. Northwest Florida '
        'State\'s description is typical: the fundamental concepts of double-entry accounting and <em>"the full '
        'accounting cycle&mdash;from analyzing transactions and applying the accounting equation to journalizing, '
        'posting, adjusting, and closing entries"</em>, preparing and interpreting the financial statements, and '
        'internal controls, cash, receivables and inventory.</p>'
        '<p>Nine Florida state colleges carry it, all at 3 credits. It is taken by business, accounting and '
        'accounting-technology students, and by anyone who needs to read financial statements. It continues in '
        '<strong>ACG2011</strong>, and the two together equal the one-term <strong>ACG2021</strong>.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
        + lg(['Explain the purpose of financial accounting, its users, and the role of generally accepted accounting '
              'principles (GAAP) and the FASB.',
              'Analyse business transactions with the accounting equation and record them with double-entry '
              'journal entries.',
              'Complete the accounting cycle: journalize, post, prepare a trial balance, adjust, prepare statements, '
              'close.',
              'Prepare and interpret the income statement, statement of retained earnings, balance sheet and an '
              'introductory statement of cash flows.',
              'Account for merchandising operations and inventory (perpetual and periodic; FIFO, LIFO, average cost).',
              'Apply internal controls and account for cash (bank reconciliation) and receivables (bad debts).'])
        + '<h3>Optional Outcomes</h3>'
        + lg(['Use accounting software (QuickBooks or a publisher\'s system) for the cycle.',
              'Compute basic ratios from the statements.',
              'Describe ethics in financial reporting and the consequences of fraud.'])
        + '<h2>Major Topics</h2><h3>Required Topics</h3>'
        + lg(['The accounting equation and the double-entry system.', 'Recording transactions; the journal and '
              'ledger.', 'Adjusting entries and accrual accounting.', 'Financial statements and closing.',
              'Merchandising operations and inventory costing.', 'Internal control and cash.', 'Receivables.'])
        + '<h3>Optional Topics</h3>'
        + lg(['Accounting information systems and special journals.', 'Payroll basics.',
              'Introduction to long-lived assets (where the college moves it from the second course).'])
        + '<h2>Resources &amp; Tools</h2>'
        + ul(['Common texts: Horngren\'s <em>Financial &amp; Managerial Accounting</em>; Weygandt, Kimmel and Kieso, '
              '<em>Accounting Principles</em>; the free OpenStax <em>Principles of Accounting, Volume 1: Financial '
              'Accounting</em>.',
              'Online homework systems (Connect, MyLab Accounting, WileyPLUS) and spreadsheet software.'])
        + '<h2>Career Pathways</h2>'
        + ul(['Bookkeeping, accounting and auditing clerks (SOC 43-3031).',
              'Accountants and auditors (13-2011), after a bachelor\'s degree; CPA licensure through the Florida Board '
              'of Accountancy.',
              'A foundation course for every business career: management, finance, marketing, entrepreneurship.'])
        + '<h2>Special Information</h2><h3>Offering Notes</h3>'
        + TWO_TERM_TABLE(TITLES_2001)
        + '<p><strong>All nine carry it at 3 credits.</strong> No carrier publishes a contact-hour figure; the 45 shown '
          'are derived from Florida\'s convention of 15 per credit. Gulf Coast also runs an honors section under the '
          'same number.</p>'
        + TWO_TERM
        + '<h3>Workload</h3><p>Accounting is learned by doing problems. Plan on 6&ndash;9 hours a week outside class, '
          'and do not fall behind: each topic builds on the last.</p>'
        + AI_ACG),
)

G['ACG2011'] = dict(
    title='Principles of Accounting II (Financial Accounting II)',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("ACG 2001 Principles of Accounting I (most colleges require a grade of C or better). ⚠ The second of a "
                   "TWO-course sequence that together equals ACG 2021 Financial Accounting. This is FINANCIAL "
                   "accounting continued, not managerial accounting: it does not replace ACG 2071, which business "
                   "degrees still require. Offered at nine Florida state colleges."),
    offering_notes={
        'summary': 'Nine Florida public institutions carry ACG2011, all state colleges and all at 3 credits (the same '
                   'nine that carry ACG2001). With ACG2001 it equals ACG2021.',
        'hours_source': 'derived', 'derived_contact_hours': 45,
        'derivation': 'Florida convention of 15 contact hours per credit for a lecture course; no carrier publishes a '
                      'term contact-hour figure.',
        'offerings': [off(c, NAMES[c], TITLES_2011[c], 3,
                          'Also carries ACG2021.' if c in ALSO_2021 else 'Two-term sequence is its only route.')
                      for c in FA_COLLEGES]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>ACG2011</strong> is the second half of introductory financial accounting taught over two terms, '
        'following ACG2001. Northwest Florida State\'s description: it <em>"continues the study of financial '
        'accounting with an emphasis on long-lived assets, liabilities, stockholders\' equity, the statement of cash '
        'flows, and financial statement analysis"</em>, including depreciation and amortization, bonds and leases, '
        'stock issues, dividends and treasury stock, and the cash-flow statement by both the direct and indirect '
        'methods.</p>'
        '<p>The same nine state colleges carry it, all at 3 credits. Completing ACG2001 and ACG2011 equals the one-term '
        '<strong>ACG2021 Financial Accounting</strong> taught at most Florida institutions. ⚠ Despite the title '
        '<em>Principles of Accounting II</em>, it is not managerial accounting: at Florida Atlantic, '
        '<em>Principles of Accounting 2</em> is the title of ACG2071 Managerial Accounting, a different course.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
        + lg(['Account for the acquisition, depreciation, disposal and impairment of property, plant and equipment, '
              'and for intangible assets.',
              'Record and report current liabilities, payroll liabilities and long-term liabilities, including bonds '
              '(premium and discount) and an introduction to leases.',
              'Account for corporate equity: issuing stock, dividends, treasury stock, and retained earnings.',
              'Prepare the statement of cash flows by the indirect method and explain the direct method.',
              'Analyse financial statements with horizontal, vertical and ratio analysis.'])
        + '<h3>Optional Outcomes</h3>'
        + lg(['Account for investments in debt and equity securities.', 'Explain partnership accounting.',
              'Use the time value of money in bond pricing.'])
        + '<h2>Major Topics</h2><h3>Required Topics</h3>'
        + lg(['Long-lived assets: cost, depreciation methods, disposal; intangibles.', 'Current and long-term '
              'liabilities; bonds.', 'Corporations and stockholders\' equity.', 'The statement of cash flows.',
              'Financial statement analysis.'])
        + '<h3>Optional Topics</h3>'
        + lg(['Investments.', 'Partnerships.', 'Present value and the time value of money.', 'Leases.'])
        + '<h2>Resources &amp; Tools</h2>'
        + ul(['The same text as ACG2001, continued; the free OpenStax <em>Principles of Accounting, Volume 1</em>.',
              'Online homework systems and spreadsheet software.'])
        + '<h2>Career Pathways</h2>'
        + ul(['Bookkeeping, accounting and auditing clerks (SOC 43-3031).',
              'Accountants and auditors (13-2011), financial analysts (13-2051) and loan officers (13-2072), after a '
              'bachelor\'s degree.'])
        + '<h2>Special Information</h2><h3>Offering Notes</h3>'
        + TWO_TERM_TABLE(TITLES_2011)
        + '<p><strong>All nine carry it at 3 credits.</strong> No carrier publishes a contact-hour figure; the 45 shown '
          'are derived from Florida\'s convention of 15 per credit.</p>'
        + TWO_TERM
        + '<h3>What comes next</h3><p>ACG2071 Managerial Accounting follows at most colleges, and then, for accounting '
          'students, Intermediate Accounting (ACG2100 at some state colleges; ACG3101 or ACG3103 at universities).</p>'
        + AI_ACG),
)

# ---------------------------------------------------------------------------------------------------- ACG2071
MGR = ['BC', 'CC', 'CF', 'CFK', 'DSC', 'EFSC', 'FAMU', 'FAU', 'FGC', 'FGCU', 'FIU', 'FLPOLY', 'FSCJ', 'FSU', 'FSWSC',
       'GCSC', 'HC', 'IRSC', 'LSSC', 'MDC', 'NFC', 'NWFSC', 'PBSC', 'PESC', 'PHSC', 'PSC', 'SCFMS', 'SFC', 'SFSC',
       'SJRSC', 'SPC', 'SSCF', 'TSC', 'UCF', 'UF', 'UNF', 'USF', 'UWF']
MGR_TITLE = {'FAU': 'Principles of Accounting II (honors section also)', 'UF': 'Introduction to Managerial Accounting',
             'FSU': 'Introduction to Managerial Accounting', 'HC': 'Managerial Accounting (honors section also)',
             'LSSC': 'Management Accounting', 'FAMU': 'Managerial Accounting Principles'}
G['ACG2071'] = dict(
    title='Managerial Accounting',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("ACG 2021 Financial Accounting, or ACG 2001 and ACG 2011 (both), usually with a C or better. Some "
                   "universities set more: FIU and UNF also require MAC 1105 College Algebra; ⚠ Florida State requires "
                   "accounting majors to earn a B in this course to go on to 3000-level accounting, and UF requires a B "
                   "in ACG 2021 and ACG 2071 plus competency assessments before ACG 3101. UF carries it at 4 credits; "
                   "every other public institution at 3."),
    offering_notes={
        'summary': '38 Florida public institutions carry ACG2071: every state university that teaches business and '
                   'nearly every state college. All at 3 credits except the University of Florida (4).',
        'hours_source': 'derived', 'derived_contact_hours': 45,
        'derivation': 'Florida convention of 15 contact hours per credit for a lecture course (60 for UF\'s 4 credits); '
                      'no carrier publishes a term contact-hour figure.',
        'offerings': [off(c, NAMES[c], MGR_TITLE.get(c, 'Managerial Accounting / Principles of Managerial Accounting'),
                          4 if c == 'UF' else 3, '4 credits' if c == 'UF' else '') for c in MGR]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>ACG2071 Managerial Accounting</strong> is the second introductory accounting course in every '
        'Florida business degree. Financial accounting (ACG2021) reports to people outside a business; managerial '
        'accounting supplies managers inside it with the cost and performance information they need to plan, control '
        'and decide. Florida Atlantic puts it in questions: <em>"How much do I have to sell before I start making a '
        'profit? Should I make a product or buy it from someone else? How much did it cost to manufacture this item? '
        'How do I prepare a budget and determine if I stayed within the budget?"</em></p>'
        '<p>It is one of the most widely carried courses in the state: <strong>38 public institutions</strong>, every '
        'state university that teaches business and nearly every state college. It is a common prerequisite for the '
        'business major at universities, so it is usually taken in the second year of an A.A. or the first two years '
        'of a bachelor\'s.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
        + lg(['Distinguish managerial from financial accounting, and classify costs by behaviour (variable, fixed, '
              'mixed) and by function (product and period).',
              'Compute product costs in job-order and process costing systems, with overhead applied by a '
              'predetermined rate.',
              'Perform cost-volume-profit analysis: contribution margin, break-even and target profit.',
              'Prepare a master budget and flexible budgets, and analyse variances from standard costs.',
              'Use relevant costs for short-term decisions: make or buy, special orders, keep or drop, constrained '
              'resources.',
              'Evaluate capital investments with payback, net present value and internal rate of return.',
              'Measure the performance of responsibility centres.'])
        + '<h3>Optional Outcomes</h3>'
        + lg(['Apply activity-based costing.', 'Compare variable and absorption costing.',
              'Use the balanced scorecard and non-financial measures.', 'Set transfer prices.',
              'Build budgets and CVP models in a spreadsheet.'])
        + '<h2>Major Topics</h2><h3>Required Topics</h3>'
        + lg(['Cost concepts and classifications.', 'Job-order costing.', 'Process costing.',
              'Cost behaviour and cost-volume-profit analysis.', 'Budgeting.', 'Standard costs and variances.',
              'Relevant costs and decision making.', 'Capital budgeting.'])
        + '<h3>Optional Topics</h3>'
        + lg(['Activity-based costing and management.', 'Variable versus absorption costing.',
              'Segment reporting and decentralization.', 'Lean operations and the cost of quality.'])
        + '<h2>Resources &amp; Tools</h2>'
        + ul(['Common texts: Garrison, Noreen and Brewer, <em>Managerial Accounting</em>; Horngren\'s <em>Financial '
              '&amp; Managerial Accounting</em>; the free OpenStax <em>Principles of Accounting, Volume 2: Managerial '
              'Accounting</em>.', 'Online homework systems; Excel for budgets and CVP.',
              'Institute of Management Accountants (IMA) and its CMA credential.'])
        + '<h2>Career Pathways</h2>'
        + ul(['Cost accountants and management accountants; accountants and auditors (SOC 13-2011).',
              'Budget analysts (13-2031) and financial analysts (13-2051).',
              'Every management career: operations, supply chain and general managers use these tools daily.',
              'Credentials: Certified Management Accountant (CMA, IMA); CPA through the Florida Board of '
              'Accountancy.'])
        + '<h2>Special Information</h2><h3>Offering Notes</h3>'
        '<p><strong>All 38 public carriers run it at 3 credits except the University of Florida, at 4</strong> (UF '
        'titles it <em>Introduction to Managerial Accounting</em>). A UF student who transfers out carries a credit more '
        'than the requirement elsewhere; a student transferring into UF\'s Fisher School of Accounting with a 3-credit '
        'version should ask how the difference is handled. No carrier publishes contact hours; 45 is Florida\'s '
        'convention for 3 credits (60 for UF\'s 4).</p>'
        + table(['Institution', 'Title', 'Credits'], [[NAMES[c], MGR_TITLE.get(c, 'Managerial Accounting (or '
                                                       'Principles of / Introduction to Managerial Accounting)'),
                                                       '4' if c == 'UF' else '3'] for c in MGR])
        + '<h3>⚠ Grades that gate the accounting major</h3><p>For accounting majors this course is a gate, not just a '
          'requirement. <strong>Florida State</strong>: accounting majors must earn at least a <strong>B</strong> to '
          'proceed to required 3000-level accounting courses. <strong>UF</strong>: ACG3101 requires a B in both ACG2021 '
          'and ACG2071 and 70% on the Fisher School\'s financial and managerial competency assessments. A C transfers '
          'as credit but may not open the major. Check the receiving university\'s rule before you register.</p>'
          '<h3>⚠ The title "Principles of Accounting II"</h3><p>Florida Atlantic titles ACG2071 <em>Principles of '
          'Accounting 2</em>, while nine state colleges use <em>Principles of Accounting II</em> for ACG2011, the second '
          'half of financial accounting. They are different courses. Match on the number, not the title.</p>'
          '<h3>Prerequisite</h3><p>ACG2021 Financial Accounting, or the two-term ACG2001 and ACG2011. FIU accepts ACG3024 '
          'for its Health Services Administration students; FIU and UNF also require MAC1105.</p>'
        + AI_ACG),
)

# ---------------------------------------------------------------------------------------------------- ACG2100
INT = ['BC', 'EFSC', 'IRSC', 'NFC', 'PBSC', 'PHSC', 'PSC', 'SCFMS', 'SFSC', 'SSCF']
INT_TITLE = {'PHSC': 'Intermediate Accounting I', 'SSCF': 'Intermediate Accounting Fundamentals',
             'IRSC': 'Intermediate Accounting', 'PBSC': 'Intermediate Accounting', 'PSC': 'Intermediate Accounting',
             'EFSC': 'Intermediate Accounting 1'}
G['ACG2100'] = dict(
    title='Intermediate Accounting I (Lower Division)',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("Varies. Pasco-Hernando: ACG 2071. Seminole State: ACG 2021 with a C or better, ACG 2071 as a "
                   "corequisite. Expect financial and managerial accounting first. ⚠ A 2000-level course offered only at "
                   "state colleges; universities teach intermediate accounting as ACG 3101 or ACG 3103. If you plan a "
                   "bachelor's in accounting or the CPA, ask the receiving university and check the Board of "
                   "Accountancy rule before relying on it (see the guide)."),
    offering_notes={
        'summary': 'Ten Florida public institutions carry ACG2100, all state colleges and all at 3 credits: Broward, '
                   'Eastern Florida, Indian River, North Florida, Palm Beach, Pasco-Hernando, Polk, State College of '
                   'Florida, South Florida and Seminole State. No university carries it.',
        'hours_source': 'derived', 'derived_contact_hours': 45,
        'derivation': 'Florida convention of 15 contact hours per credit for a lecture course; no carrier publishes a '
                      'term contact-hour figure.',
        'offerings': [off(c, NAMES[c], INT_TITLE.get(c, 'Intermediate Accounting I'), 3, '') for c in INT]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>ACG2100</strong> is a first course in intermediate financial accounting taught at the lower '
        'division, carried by <strong>ten Florida state colleges</strong>, all at 3 credits. It takes the financial '
        'accounting of ACG2021 deeper and puts it in the conceptual framework of GAAP. Pasco-Hernando State: <em>"an '
        'in-depth examination of financial accounting and reporting. Specific topics include the accounting procedures '
        'and financial statement presentation of cash, receivables, inventories, property, plant and equipment and '
        'intangible assets. The conceptual framework of accounting and the time value of money are also examined."</em> '
        'Seminole State describes it as expanding on ACG2021 <em>"within a conceptual framework determined by generally '
        'accepted accounting principles"</em>, and uses Spiceland\'s <em>Intermediate Accounting</em>, a text '
        'universities also use.</p>'
        '<p>It serves students in the A.S. in Accounting Technology and similar programmes, who go to work as '
        'accounting technicians and staff accountants, and students who want a head start on the accounting major.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
        + lg(['Explain the FASB conceptual framework: objectives, qualitative characteristics, elements, and '
              'recognition and measurement.',
              'Review and apply the accounting cycle at an intermediate level, including adjustments and corrections.',
              'Prepare the income statement and balance sheet in full GAAP form, with comprehensive income.',
              'Apply time value of money to accounting measurements.',
              'Account for cash and receivables, including the allowance method and transfers of receivables.',
              'Measure inventories: cost flow assumptions, lower of cost or net realizable value, estimation methods.',
              'Account for property, plant and equipment and intangible assets: acquisition, depreciation, impairment '
              'and disposal.'])
        + '<h3>Optional Outcomes</h3>'
        + lg(['Recognise revenue under the five-step model of ASC 606.', 'Complete a manual or computerised practice '
              'set.', 'Compare U.S. GAAP with IFRS.'])
        + '<h2>Major Topics</h2><h3>Required Topics</h3>'
        + lg(['The conceptual framework and standard setting.', 'The accounting cycle reviewed.',
              'The income statement and balance sheet.', 'Time value of money.', 'Cash and receivables.',
              'Inventories.', 'Property, plant and equipment; intangible assets.'])
        + '<h3>Optional Topics</h3>'
        + lg(['Revenue recognition.', 'Statement of cash flows (introduction).', 'IFRS comparisons.'])
        + '<h2>Resources &amp; Tools</h2>'
        + ul(['Spiceland, Nelson and Thomas, <em>Intermediate Accounting</em>; Kieso, Weygandt and Warfield, '
              '<em>Intermediate Accounting</em>.', 'The FASB Accounting Standards Codification (free basic view).',
              'Spreadsheets for present-value and depreciation schedules.'])
        + '<h2>Career Pathways</h2>'
        + ul(['Bookkeeping, accounting and auditing clerks (SOC 43-3031) and staff accountants.',
              'Accountants and auditors (13-2011), after a bachelor\'s degree; CPA licensure through the Florida Board of '
              'Accountancy.'])
        + '<h2>Special Information</h2><h3>Offering Notes</h3>'
        + table(['Institution', 'Title', 'Credits'], [[NAMES[c], INT_TITLE.get(c, 'Intermediate Accounting I'), '3']
                                                     for c in INT])
        + '<p><strong>All ten carry it at 3 credits.</strong> No carrier publishes a contact-hour figure; the 45 shown are '
          'derived from Florida\'s convention of 15 per credit.</p>'
          '<h3>⚠ The universities teach this subject at the upper division</h3>'
          '<p>No Florida university carries ACG2100. Universities teach Intermediate Accounting I as <strong>ACG3101</strong> '
          '(Florida State, FAMU, UF at 4 credits, UWF, and four state colleges with bachelor\'s programmes) or '
          '<strong>ACG3103</strong> (FGCU, UNF, USF, Miami Dade), and the accounting major is built on those numbers. '
          'Two consequences:</p>'
        + ul(['<strong>Transfer.</strong> A 2000-level course does not supply upper-division hours toward a bachelor\'s '
              'degree, and universities admit students to intermediate accounting on their own rules (UF requires a B '
              'in ACG2021 and ACG2071 and competency assessments). Expect to take ACG3101 or ACG3103 at the university '
              'even after ACG2100; it will feel familiar, which is useful, but plan the credits. Get a written answer '
              'from the receiving department before counting on anything else.',
              '<strong>The CPA.</strong> Florida\'s Board of Accountancy requires the accounting hours for the CPA '
              'examination to be at the <strong>upper-division</strong> level (Rule 61H1-27.002, F.A.C.). The current '
              'rule defines upper division as courses above the principal introductory level, and the Board reviews '
              'courses (its Course Guide); an older version of the rule excluded community-college courses outright. '
              'Do not assume a 2000-level course will count: confirm with the Board before relying on it.'])
        + '<h3>When it is the right course</h3><p>For an A.S. in Accounting Technology, a working bookkeeper, or a '
          'student who wants a strong foundation before the university\'s intermediate sequence, ACG2100 is valuable in '
          'its own right: intermediate accounting is where most students first find accounting hard.</p>'
        + AI_ACG),
)

for cid, g in G.items():
    d = {'title': g['title'], 'html_content': g['html'], 'credits': g['credits'],
         'contact_hours': g['contact_hours'], 'prerequisites': g['prerequisites'], 'version': g['version'],
         'offering_notes': g['offering_notes']}
    path = os.path.join('drafts', '%s_guide.json' % cid)
    with io.open(path, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
    print('%-9s html %5d prereq %4d -> %s' % (cid, len(g['html']), len(g['prerequisites']), path))
