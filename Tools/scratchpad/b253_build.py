# -*- coding: utf-8 -*-
"""Batch 253: write the one writable requested guide (EDG7365) to drafts/ (run from Tools/).

    python scratchpad/b253_build.py

Sources (2026-11-23): SCNS flat file (UF the only carrier, 3 cr; statewide title PRACTITIONER RESEARCH IN SCHOOLS AND
THE COMMUNITY); catalog.ufl.edu/search/?P=EDG%207365 and ?P=EDG%207982 (descriptions, prerequisite). UF's catalogue
lists no programme page referencing either course.
"""
import io
import json
import os
import sys

sys.path.insert(0, 'scratchpad')
from b251_build import lg, ul, table, off  # noqa: E402  (helpers only)

G = {}

G['EDG7365'] = dict(
    title='Practitioner Research: Data Collection and Analysis',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("UF: EDG 7982 Practitioner Research: Theory and Practice, or instructor approval. A doctoral "
                   "(7000-level) course, normally taken in a practitioner doctorate in education after EDG 7982. Only "
                   "the University of Florida carries EDG 7365. Before collecting any data from students, colleagues or "
                   "families, expect to need approval from UF's Institutional Review Board AND from your school "
                   "district's research office; start both early, because data collection cannot begin until both are "
                   "granted. When transferring graduate credit, send the syllabus, not just the number."),
    offering_notes={
        'summary': 'One Florida public institution carries EDG7365: the University of Florida, at 3 credits.',
        'hours_source': 'derived', 'derived_contact_hours': 45,
        'derivation': "UF publishes no contact hours; 45 is Florida's convention for a 3-credit lecture or seminar.",
        'offerings': [
            off('UF', 'University of Florida', 'Practitioner Research: Data Collection and Analysis', 3,
                'Prerequisite EDG 7982 or instructor approval. Letter grade. Statewide title: Practitioner Research '
                'in Schools and the Community.'),
        ]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>EDG7365 Practitioner Research: Data Collection and Analysis</strong> is a doctoral course for '
        'working educators who study their own practice. The University of Florida, the only Florida public '
        'institution that carries the number, describes it this way: graduate students <em>continue to cultivate the '
        'skills of scholarship through advanced study of practitioner research and its utility within their daily '
        'work as educators. Multiple data collection and analysis processes will be explored through experiential '
        'learning.</em> The statewide course record titles the number <strong>Practitioner Research in Schools and the '
        'Community</strong>; the subject is the same.</p>'
        '<p><strong>Practitioner research</strong> (also called practitioner inquiry, teacher inquiry or action '
        'research) is research a teacher, coach or administrator carries out in their own classroom, school or '
        'district, on a question that comes from their own work, in order to improve it. EDG7365 is the second course '
        'of a pair. Its prerequisite, <strong>EDG 7982 Practitioner Research: Theory and Practice</strong>, builds the '
        'theory: why practitioner inquiry matters as professional development and how it supports school '
        'improvement. EDG7365 is the hands-on half: how to gather evidence in a working school and how to make sense '
        'of it.</p>'
        '<p>The 7000 level places it in doctoral study. Practitioner research is the usual basis for the '
        '<strong>dissertation in practice</strong> found in many Doctor of Education (EdD) programmes, so the course '
        'often prepares the data collection and analysis plan for that study. UF publishes only a short description '
        'and does not list in its catalogue the programmes that require the course, so this guide describes what such '
        'a course commonly covers and marks the rest as optional. The UF syllabus for the term decides the readings '
        'and assignments.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>' + lg([
            'Turn a question from your own practice into an <strong>inquiry question</strong> that data can answer, '
            'and match each kind of data to the part of the question it addresses.',
            'Plan and carry out several <strong>data collection methods</strong> suited to a working school: '
            'observation and field notes, interviews and focus groups, surveys, student work and other artefacts, '
            'documents, existing assessment data and a reflective research journal.',
            'Analyse <strong>qualitative data</strong> by coding, grouping codes into categories and themes, and '
            'checking emerging findings against the whole data set.',
            'Summarise <strong>quantitative classroom data</strong> (scores, counts, attendance, survey responses) '
            'with descriptive statistics and simple displays, and say what such data from one setting can and cannot '
            'show.',
            'Use <strong>triangulation</strong>, member checking, peer debriefing and an audit trail to make findings '
            'trustworthy, and explain why these matter when the researcher is also the teacher.',
            'Carry out the study <strong>ethically</strong>: informed consent and assent, protecting student records '
            '(FERPA), the power a teacher holds over the students being studied, and the approvals a university and '
            'a school district require.',
            'Write up findings so that colleagues can use them, with the claims limited to what the evidence '
            'supports.',
        ]) +
        '<h3>Optional Outcomes</h3>' + lg([
            'Draft the methods chapter, or the data collection and analysis plan, for a dissertation in practice.',
            'Use qualitative analysis software to organise and code a data set.',
            'Run a full inquiry cycle (plan, act, collect, analyse, reflect, revise) during the term and present it '
            'to peers.',
            'Combine qualitative and quantitative evidence in a simple mixed-methods design.',
        ]) +
        '<h2>Major Topics</h2><h3>Required Topics</h3>' + lg([
            'From wondering to inquiry question: narrowing, refining and making a question researchable.',
            'Designing a data collection plan: which evidence answers which part of the question, when and how often '
            'to collect it, and how much is enough.',
            'Observation and field notes; audio and video recording in classrooms.',
            'Interviews and focus groups with students, colleagues and families: writing protocols, asking follow-up '
            'questions, transcription.',
            'Surveys and questionnaires: writing items, small samples, response rates.',
            'Student work, artefacts, documents and existing data (assessment results, attendance, discipline records).',
            'The researcher journal and reflective memos as data.',
            'Qualitative analysis: first-cycle and second-cycle coding, codebooks, categories, themes, constant '
            'comparison, looking for disconfirming evidence.',
            'Descriptive statistics and displays for classroom-scale quantitative data.',
            'Trustworthiness: credibility, triangulation, member checking, peer debriefing, audit trail, positionality.',
            'Ethics and approvals: Institutional Review Board review, school district research approval, consent and '
            'assent, FERPA, confidentiality, storing data securely.',
            'Reporting findings and implications for practice.',
        ]) +
        '<h3>Optional Topics</h3>' + lg([
            'Qualitative data analysis software (NVivo, ATLAS.ti, MAXQDA, Dedoose).',
            'Simple mixed-methods designs.',
            'Collaborative inquiry with a team of teachers or a professional learning community.',
            'Visual and arts-based data; photo elicitation.',
            'Writing the methods section of a dissertation in practice.',
        ]) +
        '<h2>Resources &amp; Tools</h2>' + ul([
            'Texts commonly used for practitioner research (the syllabus sets the actual list): Dana and '
            'Yendol-Hoppey, <em>The Reflective Educator\'s Guide to Classroom Research</em> (Corwin); Herr and '
            'Anderson, <em>The Action Research Dissertation</em> (SAGE); Mertler, <em>Action Research: Improving '
            'Schools and Empowering Educators</em> (SAGE).',
            'For analysis: Saldaña, <em>The Coding Manual for Qualitative Researchers</em> (SAGE); Miles, Huberman and '
            'Saldaña, <em>Qualitative Data Analysis: A Methods Sourcebook</em> (SAGE).',
            'Qualitative analysis software (NVivo, ATLAS.ti, MAXQDA, Dedoose); a spreadsheet or SPSS/R for descriptive '
            'statistics.',
            'UF\'s Institutional Review Board guidance and forms, and your school district\'s research application.',
            'The U.S. Department of Education\'s guidance on FERPA (studentprivacy.ed.gov).',
            'The Carnegie Project on the Education Doctorate (CPED), whose framework describes the dissertation in '
            'practice.',
        ]) +
        '<h2>Career Pathways</h2>' + ul([
            'Classroom teachers who lead improvement in their school or district.',
            'Instructional coaches and curriculum specialists (Instructional Coordinators, SOC 25-9031).',
            'School and district administrators (Education Administrators, Kindergarten through Secondary, SOC '
            '11-9032).',
            'Teacher educators and professional development leaders in colleges and districts.',
            'Programme evaluators and research staff in Florida school districts and education agencies.',
        ]) +
        '<h2>Special Information</h2>'
        '<h3>Offering Notes</h3>' + table(['Institution', 'Title', 'Credits', 'Contact hours'], [
            ['University of Florida', 'Practitioner Research: Data Collection and Analysis', '3',
             'not published (45 derived)'],
        ]) +
        '<p>UF is the only Florida public institution that carries EDG7365. The 45 contact hours are derived from '
        'Florida\'s convention for a 3-credit course; UF does not publish a figure.</p>'
        '<h3>Position in the curriculum</h3><p>Take <strong>EDG 7982</strong> first, unless the instructor approves '
        'otherwise. EDG 7982 builds the reasons for practitioner inquiry; EDG7365 builds the methods. In a '
        'practitioner doctorate the pair normally comes before the dissertation in practice, so the study you plan '
        'here may become your dissertation study.</p>'
        '<h3>Approvals take time</h3><p>Research with students, colleagues or families normally needs '
        '<strong>Institutional Review Board</strong> approval from the university and, separately, approval from the '
        '<strong>school district</strong> where the data is collected; Florida districts run their own research '
        'application processes. Data collected before approval usually cannot be used. Ask the instructor in the '
        'first week whether course assignments count as research needing approval, and start the applications for '
        'your real study early.</p>'
        '<h3>Studying your own students</h3><p>A teacher who studies their own class holds power over the people being '
        'studied. Students may feel they must take part, or answer in the way they think the teacher wants. Expect the '
        'course to ask how consent is gathered, who sees identifiable data, and how participation is kept separate '
        'from grades. Student records are protected by FERPA; keep data on secure storage and remove names before '
        'sharing it with classmates.</p>'
        '<h3>Transfer</h3><p>Doctoral credit transfers only by petition to the receiving programme, which usually '
        'limits how many credits may come from elsewhere. Keep the syllabus and your inquiry plan; the number alone '
        'will not tell another university what you studied.</p>'
        '<h2>AI Integration (Optional)</h2>'
        '<p>AI tools are now offered for two jobs in this course: <strong>transcribing</strong> interviews and '
        '<strong>coding</strong> qualitative data. Both raise questions the course itself teaches you to ask.</p>'
        '<p><strong>Transcription.</strong> Recordings of students are protected data. Uploading them to an online '
        'service sends them to a third party, which your IRB approval and district agreement may not allow. Check '
        'what your approved protocol says before using any tool, and prefer one that runs on your own computer or '
        'one your university has approved.</p>'
        '<p><strong>Coding and summarising.</strong> A model can suggest codes and themes quickly, which can help a '
        'first pass. But a model leans toward the most common pattern in the data, and in practitioner research the '
        'student who does not fit the pattern is often the most important finding. The researcher must read every '
        'transcript, own every code, record in the audit trail where a tool was used, and check every suggested theme '
        'against the data. Follow your instructor\'s and programme\'s policy on AI use in assignments and in the '
        'dissertation.</p>'),
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
