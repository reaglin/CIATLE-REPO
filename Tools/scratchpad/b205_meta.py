"""Batch 205 metadata. Offerings built from the flat file (batch 202 pattern)."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, TOOLS)
import scns
from list_courses import smart_title

imap = json.load(open(os.path.join(HERE, 'inst_map.json'), encoding='utf-8'))


def entry(num):
    v = imap.get(str(int(num)), '')
    if ' - ' in v:
        c, n = v.split(' - ', 1)
        return c.strip(), smart_title(n.strip())
    return v.strip(), smart_title(v.strip())


IDS = ('OCB3108L', 'PLA4607', 'POS3625', 'POT4013', 'PSY3215', 'PSY4832')
fam = {}
for pfx in ('OCB', 'PLA', 'POS', 'POT', 'PSY'):
    for r in scns.parse_flatfile(os.path.join(HERE, 'crslist.txt'), prefix=pfx):
        if r['code'] in IDS:
            fam.setdefault(r['code'], []).append(r)

NOTES = {
    'OCB3108L': {
        'UNF': 'Titled FIELD STUDIES IN MARINE SCIENCE - the same course described more plainly. '
               'Credits are a RANGE WITHIN the institution (3-4), set with the department; ask '
               'what determines it before registering.',
        'UWF': 'Matches the statewide title. Credits 3-4, a range within the institution. Note the '
               'related identifiers: OCB3108 (bare) is carried by USF at 4 credits, and OCB3108C '
               'is carried by NO institution at all.',
    },
    'PLA4607': {
        'UCF': 'Titled ESTATES AND TRUSTS - dropping "wills" from the title may signal more weight '
               'on trusts and administration and less on will drafting. Worth confirming, because '
               'drafting is the skill an employer tests at interview.',
        'SPC': 'Titled ESTATE PLANNING AND ADMINISTRATION - the practice framing (client intake, '
               'document assembly, probate forms and filings). Arguably the most immediately '
               'employable version, and consistent with an A.S. paralegal programme. The Florida '
               'College System carrier, so this is the FCS-to-SUS transfer case.',
        'UWF': 'Matches the statewide title exactly - the balanced doctrinal treatment.',
    },
    'POS3625': {
        'UNF': 'Identical title to FSU.',
        'FSU': 'Identical title to UNF.',
        'UWF': 'Titled FIRST AMENDMENT FREEDOM - the same course; the singular "Freedom" is '
               'stylistic, though the Amendment contains six freedoms and the plural would be '
               'more accurate.',
    },
    'POT4013': {
        'FAU': 'Titled ANCIENT POLITICAL THOUGHT - Greece and Rome only, so Augustine, Aquinas, '
               'the church-state material AND Machiavelli may all be absent. WARNING: "Ancient '
               'Political Thought" is also the statewide title of POT6016, a GRADUATE course, so '
               'a transcript line does not identify the level. Keep the syllabus.',
        'UWF': 'Titled ANCIENT POLITICAL PHILOSOPHY - same shape as FAU. "Thought" versus '
               '"Philosophy" is not a signal; the chronological stop is.',
        'UF': 'Titled GREAT POLITICAL THINKERS: ANCIENT & MEDIEVAL - the only title telling you '
              'Augustine and Aquinas are in. Still stops short of Machiavelli, whom the statewide '
              'title names as the endpoint.',
    },
    'PSY3215': {
        'FIU': 'Titled RESEARCH METHODS AND DATA ANALYSIS IN PSYCHOLOGY at FOUR credits. WARNING: '
               'that is the statewide title of a DIFFERENT number, PSY3211, whose statewide '
               'prerequisite is a statistics course and whose scope matches the 4-credit value. '
               'So FIU appears to be running under PSY3215 a course the state numbers PSY3211 - a '
               'misfiling with transfer consequences.',
        'UWF': 'Titled RESEARCH METHODS IN PSYCHOLOGICAL SCIENCE at THREE credits. WARNING: that '
               'reads as a FIRST, standalone methods course, while the statewide title carries a '
               '"(CONT)" marker meaning a continuation. So this number may be the first methods '
               'course here and the second elsewhere, which changes what it assumes you know.',
    },
    'PSY4832': {
        'UWF': 'The only public carrier, at the exact statewide title - and the title matters: '
               'both private carriers drop "exercise", which halves the scope. Sport psychology '
               'serves athletes and performance; exercise psychology serves the general '
               'population and behaviour change, and the latter has the wider application and the '
               'larger job market.',
    },
}


def offerings(cid):
    rows = []
    for r in sorted(fam[cid], key=lambda x: int(x['institution'])):
        code, name = entry(r['institution'])
        if not scns.is_public(code):
            continue
        cr = r['credit'].strip()
        try:
            c = float(cr)
            c = int(c) if c == int(c) else c
        except ValueError:
            c = None                  # 'VAR' or a range such as '3-4'
        rows.append({'institution': code, 'institution_name': name,
                     'title': smart_title(r['inst_title']), 'credits': c,
                     'contact_hours': None, 'note': NOTES.get(cid, {}).get(code)})
    return rows


def notes(cid, summary, derived, derivation):
    return {'summary': summary, 'hours_source': 'derived',
            'derived_contact_hours': derived, 'derivation': derivation,
            'offerings': offerings(cid)}


D3 = ('Derived, not published. No Florida institution publishes an hour figure for this '
      'number; 45 contact hours is the Florida convention for a 3-credit lecture course.')

meta = json.load(open(os.path.join(HERE, 'meta.json'), encoding='utf-8'))

meta['OCB3108L'] = {
    'title': 'OCB3108L Marine Field Studies (Study Abroad in Florida) - Curriculum Guide',
    'credits': 3,
    'contact_hours': 60,
    'prerequisites': (
        'Statewide: CHM2045, CHM2046, BSC2010 AND BSC2011, each with a grade of C or better, or '
        'permission of the instructor - two years of introductory chemistry and biology with a '
        'grade condition. Sequence it deliberately: to take this the summer after your second '
        'year all four must be done, and chemistry is the one students defer. WARNING - '
        'this is a FIVE-WEEK RESIDENTIAL FIELD INTENSIVE and cannot be combined with a job or '
        'another course. It almost certainly runs in summer, so plan for lost earnings, check '
        'summer aid, and confirm housing. Registration is capped by vessel berths and often opens '
        'the previous autumn. WARNING - the statewide description says "some '
        'field activities will be physically demanding": long days in Florida summer heat, time '
        'on vessels, wading in soft mud and mangrove, hauling gear, snorkelling, tide-driven '
        'early starts. Raise swimming ability, seasickness, heat tolerance, medication and '
        'accommodation needs with the instructor EARLY and privately; all are routine.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'OCB3108L',
        'Two public carriers, both SUS, both at a 3-4 credit RANGE WITHIN the institution rather '
        'than between them. Same subject at both. Note two things about the identifier: the L '
        'suffix does NOT mean a 1-credit laboratory here - it means the course is ENTIRELY '
        'practical work, with no lecture partner - and a third identifier, OCB3108C, is carried by '
        'no institution at all. The bare OCB3108 is carried by USF at 4 credits.',
        60,
        'Derived, not published, and derived unusually: the ordinary credit-to-hour convention is '
        'meaningless for a five-week residential field course. A field intensive of this kind '
        'occupies most of the working day for five weeks - realistically well over 150 hours once '
        'travel, sampling, laboratory work and evening data sessions are counted. The 60 figure is '
        'a conservative lower bound chosen for comparability with other 3-4 credit courses; treat '
        'the real commitment as full-time for five weeks.'),
}

meta['PLA4607'] = {
    'title': 'PLA4607 Wills, Estates and Trusts - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'No statewide prerequisite - unusual for a 4000-level applied law course, and a contrast '
        'with PLA3240, which has a three-course statewide gate. Institutions normally expect an '
        'introduction to the paralegal profession and legal research or civil litigation, often '
        'business law; check your catalog. Take the ethics and UPL course FIRST if you can. '
        'WARNING - estate work is the most dangerous unauthorised-practice-of-law territory for a '
        'non-lawyer in Florida, and the Bar has litigated it about will preparation specifically. '
        'The line is between TYPING what a client dictates and ADVISING on what their documents '
        'should say. A frightened elderly client will ask a friendly paralegal what to do; '
        'answering is UPL. WARNING - read Article X section 4 of the Florida Constitution. Florida '
        'homestead cannot be freely devised where a spouse or minor child survives, so a valid '
        'will can fail entirely as to the most valuable asset, and out-of-state wills routinely '
        'get it wrong.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'PLA4607',
        'One Florida College System institution and two State University System institutions, all '
        'at 3 credits - no credit divergence and the same subject at all three. The divergence is '
        'one of FRAMING, and the statewide description contains all three framings: UWF the '
        'balanced doctrinal treatment, UCF weighted toward trusts and administration, St. '
        'Petersburg College the practice version (intake, documents, probate forms). The syllabus '
        'test is whether the course requires you to DRAFT a will and complete real probate FORMS.',
        45, D3 + ' Expect the drafting and forms work to consume more out-of-class time than the '
        'reading, because a document either works or it does not.'),
}

meta['POS3625'] = {
    'title': 'POS3625 The First Amendment - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'Statewide prerequisite: NONE, and the course is available for dual enrolment (elective '
        'high-school credit). The "(U)" marker makes it upper division, and some sections are '
        'restricted to majors and minors. RECOMMENDED even though not required: take American '
        'national government (POS2041) or an introduction to the judicial process first - the '
        'course assumes you know how a case reaches the Supreme Court, what precedent does and '
        'what incorporation means. WARNING - the divergence here is by DEPARTMENT rather than '
        'institution, and the number does not record it. A political-science version covers all '
        'six freedoms with the religion clauses at length; a journalism version emphasises speech '
        'and press with defamation, privacy, access and shield laws. The syllabus test: look for '
        'the religion clauses. WARNING - recent doctrine has moved materially on the Establishment '
        'and Free Exercise Clauses, so older notes may state the law incorrectly.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'POS3625',
        'Three State University System institutions, all at 3 credits, and UNF and FSU use the '
        'IDENTICAL title - nothing to resolve on this number. UWF\'s "First Amendment Freedom" is '
        'the same course. What does vary is not recorded in the number at all: whether the course '
        'is taught in political science (doctrinal, all six freedoms, religion clauses at length) '
        'or in journalism and mass communication (speech and press, with defamation, privacy, '
        'access and shield laws in practical detail).',
        45, D3 + ' The scheduled hours describe the load poorly: reading judicial opinions is '
        'slow, a major case with dissents can take two hours, and the assessment is writing. Look '
        'at the case list on the syllabus, not the meeting pattern.'),
}

meta['POT4013'] = {
    'title': 'POT4013 Political Theory to Machiavelli - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'No statewide prerequisite. Institutions normally expect upper-division standing and an '
        'introduction to political science or political theory; some restrict it to majors. '
        'RECOMMENDED: a logic or argumentation course first - the work is reconstructing and '
        'evaluating arguments, and a student who can already identify a valid form and build a '
        'counterexample starts weeks ahead. WARNING - THE THREE CARRIERS STOP IN THREE DIFFERENT '
        'PLACES. The statewide span is Plato to Aquinas to MACHIAVELLI plus the church-state '
        'struggle; UF stops at Ancient & Medieval (no Machiavelli); FAU and UWF title it ANCIENT, '
        'so Augustine, Aquinas, the whole church-state problem AND Machiavelli may all be absent. '
        'Machiavelli is the standard dividing line of the field, so a student taking an "ancient" '
        'first half and a "modern" second half beginning with Hobbes has a gap where the hinge '
        'should be. Read the syllabus reading list, not the title, and ask one question: does this '
        'course read Aquinas and Machiavelli?'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'POT4013',
        'Three State University System institutions at 3 credits - no credit divergence, but none '
        'uses the statewide title and all three are NARROWER than the statewide span, in three '
        'different degrees. A clean chronological divergence with three endpoints. Note also that '
        'FAU\'s undergraduate title "Ancient Political Thought" is the statewide title of POT6016, '
        'a GRADUATE course - the second instance of that shape after PHY4513 - and that the '
        'state\'s own POT list contains duplicated titles (POT2010 and POT2300 both "Classical '
        'Political Theory") and at least four overlapping ancient-to-modern surveys.',
        45, D3 + ' The scheduled hours describe this course badly: primary philosophical text is '
        'slow reading - thirty pages of the Republic read properly is a two-hour job - and the '
        'assessment is essays.'),
}

meta['PSY3215'] = {
    'title': 'PSY3215 Principles of Research Methodology II - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'No statewide prerequisite is listed, which given the "(CONT)" marker is almost certainly '
        'an omission. Sibling numbers show what is normally required: introductory psychology '
        '(PSY2012) with a minimum grade, and STATISTICS - PSY3211, PSY3213 and PSY3017 all require '
        'it explicitly. Whether statistics is a prerequisite, a corequisite or folded in is the '
        'single most useful thing to establish about your section. WARNING - THIS NUMBER IS DOING '
        'THREE DIFFERENT JOBS. The statewide "(CONT)" marker says second methods course; UWF\'s '
        'title reads as a first, standalone one; and FIU\'s title is the statewide title of a '
        'DIFFERENT number (PSY3211), at 4 credits rather than 3. Before registering ask the '
        'department two questions: is this the first or second research methods course in the '
        'major, and is statistics a prerequisite, corequisite or built in? WARNING - find out in '
        'week one how long IRB approval takes; it is the most common reason a course project runs '
        'out of term.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'PSY3215',
        'Only two public carriers, and they differ on credits, on title, and on which position in '
        'the sequence the number occupies. Florida numbers research methods in psychology at least '
        'EIGHT ways. FIU\'s title is the statewide title of PSY3211 - a misfiling, third instance '
        'of that shape after PUR4801 and MUN3483 - and its 4 credits match PSY3211\'s combined '
        'methods-and-analysis scope. UWF\'s title reads as a first methods course while the state '
        'marks this number "(CONT)". The state also flags the number as a LABORATORY course while '
        'neither carrier uses an L suffix, consistent with scheduled computer or laboratory '
        'sessions inside the hours. One private institution carries it as "Research Methods II", '
        'which is the reading closest to the statewide marker.',
        45, D3 + ' For FIU\'s 4-credit version expect about 60. Treat either figure as '
        'understating the load: the course project - design, IRB approval, data collection, '
        'analysis and an APA report - is the real commitment. Budget ten to twelve hours a week.'),
}

meta['PSY4832'] = {
    'title': 'PSY4832 Sport and Exercise Psychology - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'No statewide prerequisite; the "(U)" marker makes it upper division. Institutions normally '
        'expect introductory psychology and upper-division standing, and where the course sits in '
        'an exercise-science or sport-management department rather than psychology, expect a MAJOR '
        'RESTRICTION instead - invisible until registration fails. Two things are functionally '
        'required even where not stated: introductory psychology (the course uses motivation, '
        'learning, attention and stress concepts as vocabulary), and enough RESEARCH LITERACY to '
        'read a study, because this field mixes well-supported findings with widely repeated '
        'claims that have not held up. WARNING - you cannot practise '
        'sport psychology with a bachelor\'s degree. Applied practice needs a graduate degree plus '
        'either the AASP Certified Mental Performance Consultant credential (performance work, NOT '
        'psychotherapy) or psychology licensure. The course teaches you to REFER: 988 Suicide and '
        'Crisis Lifeline, and your institution counselling service.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'PSY4832',
        'ONE public carrier, at the exact statewide title. Two private institutions also carry the '
        'number and are not listed here under the public-institution scope rule - but the '
        'exclusion is informative: both drop "exercise" from the title, and that halves the scope. '
        'Sport psychology serves athletes and performance; exercise psychology serves the general '
        'population and health behaviour change, and the latter has the wider application and the '
        'larger job market. With one public carrier there is no second public catalog to check '
        'content against, so your syllabus is the authority on emphasis.',
        45, D3),
}

json.dump(meta, open(os.path.join(HERE, 'meta.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('meta.json now holds %d entries' % len(meta))
for cid in IDS:
    n = meta[cid]['offering_notes']
    print('  %-9s %d public offerings, prereq %d chars'
          % (cid, len(n['offerings']), len(meta[cid]['prerequisites'])))
