#!/usr/bin/env python
"""Batch 235 -- build the four guides the career paths generated.

ENC1101, STA2023, BSC2085, BSC2086. Ron's rule (2026-09-17): a course that spans
a major associated with a career path gets a guide. These four are named by the
published Registered Nurse and Lawyer paths and had none.

All four are the BARE majority form. Ron, same day: the bare and C forms are the
same course, lecture+lab completes exactly as the combined form does, and the
packaging difference is a NOTATION, not a warning.

Sources used, all fetched this session:
  * SCNS statewide report (sw_ENC.csv, sw_STA.csv, sw_bsc.csv) -- titles with the
    (GE CORE) marker, full descriptions with the state's own learning outcomes,
    prerequisites, transferability, high-school credit.
  * SCNS flat file -- carriers, per-institution credits and titles, Gordon Rule
    and general-education flags.
  * Gulf Coast State College -- PUBLISHED contact hours, corequisites, fees.
"""
import io
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


# ── shared blocks ───────────────────────────────────────────────────────────
# ⚠ Budget: all shared blocks together ~400 chars in the PREREQUISITE field
# (batch 215 rule). These are BODY blocks, which have no limit.

GE_CORE = (
    '<h3>This is a Florida General Education Core course</h3>'
    '<p>The statewide title carries the <strong>(GE CORE)</strong> marker, which identifies a course on '
    'Florida&rsquo;s limited General Education Core list under s. 1007.25, Florida Statutes. '
    '<strong>A core course satisfies its general-education subject area at every Florida public college '
    'and university, and carries that status in transfer.</strong> That is materially stronger than the '
    'ordinary &ldquo;guaranteed transfer to an institution offering the same course&rdquo; promise, which '
    'only protects you where the receiving school happens to offer it.</p>'
    '<p>&#9888; The protection attaches to the <em>subject area</em>. Whether a particular programme&rsquo;s '
    'own requirement is met is a programme rule, so a competitive admissions list can still name a '
    'specific course.</p>')

GORDON = (
    '<h3>Gordon Rule, and the grade that actually counts</h3>'
    '<p>Florida requires designated writing and mathematics coursework for an associate or baccalaureate '
    'degree (State Board of Education Rule 6A-10.030). <strong>&#9888; A grade of C or higher is required '
    'for a Gordon Rule course to count &mdash; a C-minus does not satisfy it at most institutions</strong>, '
    'which is stricter than the ordinary passing standard and is a common and expensive surprise.</p>'
    '<p>&#9888; <strong>The designation is made by the institution, not by the course number.</strong> The '
    'SCNS record shows the designation flags populated inconsistently across carriers, so the honest '
    'statement is that <em>a</em> designation is recorded for most of them &mdash; not which component it '
    'satisfies. Check your own institution&rsquo;s Gordon Rule list.</p>')

PACKAGING = (
    '<h3>Two ways Florida packages this course, and they are equivalent</h3>'
    '<p>Some institutions teach the lecture and the laboratory as two registrations; others combine them '
    'into a single course with a <code>C</code> suffix. <strong>The outcomes are the same and transfer '
    'works either way: lecture plus laboratory completes exactly as the combined course does.</strong> '
    'Institutions are given this leeway deliberately, so that departments can vary their approach.</p>'
    '<p>&#9888; <strong>The one thing to get right is the registration.</strong> Where your institution '
    'splits the course, enrol in <em>both</em> halves &mdash; they are normally corequisites. Gulf Coast '
    'State College, for example, lists &ldquo;Corequisite: BSC2085L or consent of the Natural Sciences '
    'division chair&rdquo; on the lecture.</p>')

TITLES = (
    '<h3>If your catalog calls it something else, it is still this course</h3>'
    '<p>Institutions name this course many different ways. That variation is branding rather than '
    'curriculum: on a high-enrolment general-education course carried by dozens of institutions, many '
    'titles mean one course, not many courses. <strong>Register by the course number.</strong></p>')


def guide(title, credits, hours, prereq, html, notes, version='1.0'):
    return {
        'title': title,
        'html_content': html,
        'credits': credits,
        'contact_hours': hours,
        'prerequisites': prereq,
        'version': version,
        'offering_notes': notes,
    }


GUIDES = {}

# ── ENC1101 ─────────────────────────────────────────────────────────────────
GUIDES['ENC1101'] = guide(
    'English Composition I',
    3, 45,
    'No statewide prerequisite. Most institutions require placement: completion of developmental '
    'writing, a qualifying placement score, or a state exemption (Gulf Coast State College states '
    'exactly that). '
    'IMPORTANT: this is a Florida General Education Core course, so it satisfies the communication '
    'area at every Florida public institution. It is also a Gordon Rule writing course at nearly '
    'every carrier, and a Gordon Rule course needs a grade of C or HIGHER to count - a C-minus does '
    'not, which is stricter than passing. '
    'Register by NUMBER: 39 Florida public institutions carry ENC1101 at 3 credits under 33 '
    'different titles, and three carry ENC1101C at 4 credits. The titles are branding; the course '
    'is the same.',
    '<h2>Course Description</h2>'
    '<p><strong>English Composition I</strong> is the writing course nearly every degree in Florida '
    'begins with, and the one most often named as a prerequisite by everything that follows. The '
    'statewide description is recent and specific: the course introduces <strong>rhetorical concepts '
    'and audience-centered approaches to writing</strong>, including composing processes, language '
    'conventions and style, and critical analysis and engagement with written texts and other forms '
    'of communication.</p>'
    '<p>It is carried by <strong>39 Florida public institutions</strong> at 3 credits, which makes it '
    'one of the most widely offered courses in the state. Three institutions instead carry '
    '<code>ENC1101C</code> at 4 credits.</p>'
    '<p>&#9888;&#9888; <strong>The statewide title carries the (GE CORE) marker</strong>, and that is '
    'the single most useful fact about this course &mdash; see Special Information.</p>'

    '<h2>Learning Outcomes</h2>'
    '<h3>Required Outcomes</h3>'
    '<p>These are the state&rsquo;s own learning outcomes, carried in the SCNS record:</p>'
    + li('Apply <strong>rhetorical knowledge</strong> to communicate for a range of audiences and purposes.',
         'Employ <strong>critical thinking</strong> to analyse forms of communication.',
         'Engage in <strong>writing processes</strong> that involve drafting, revising and reflecting.') +
    '<h3>Optional Outcomes</h3>'
    + li('Conduct and document source-based research, where the institution places research in the first course rather than the second.',
         'Produce multimodal or digital compositions alongside conventional essays.',
         'Reflect on writing as a portfolio, where the course is portfolio-assessed.') +

    '<h2>Major Topics</h2>'
    '<h3>Required Topics</h3>'
    + li('Rhetorical situation: audience, purpose, context, genre.',
         'The composing process &mdash; invention, drafting, revision, editing &mdash; treated as recursive rather than linear.',
         'Critical reading and analysis of written and non-written texts.',
         'Language conventions, style, and editing for clarity.',
         'Argument: claim, reasoning, evidence, and addressing objections.') +
    '<h3>Optional Topics</h3>'
    + li('Source evaluation, citation and academic integrity (often held for Composition II).',
         'Research methods and the documented essay.',
         'Visual and multimodal rhetoric.',
         'Collaborative writing and peer review protocols.') +

    '<h2>Resources &amp; Tools</h2>'
    '<ul>'
    '<li>A rhetoric and a handbook are the usual pairing; many Florida institutions have moved to '
    'open educational resources, so confirm before buying.</li>'
    '<li>Institutional writing centres &mdash; free, and the single most under-used resource on any campus.</li>'
    '<li>Citation guidance: MLA, APA or Chicago, depending on the department.</li>'
    '<li>&#9888; Gulf Coast State College publishes a <strong>$5.00 lab fee</strong> on this course; fees vary by institution.</li>'
    '</ul>'

    '<h2>Career Pathways</h2>'
    '<p>This course does not point at one occupation; it is a prerequisite for almost all of them. '
    'Writing appears in every職 professional standard, and it is the skill employers most often report '
    'as missing. It is placed deliberately on two career paths in this repository:</p>'
    '<ul>'
    '<li><strong>Lawyer</strong> &mdash; the LSAT tests reading comprehension and argument, and law school tests both harder.</li>'
    '<li><strong>Registered Nurse</strong> &mdash; documentation is a legal record, and a general-education writing requirement gates the nursing sequence.</li>'
    '</ul>'

    '<h2>Special Information</h2>'
    + GE_CORE + GORDON + TITLES +
    '<h3>Dual enrolment: check what the high-school credit actually is</h3>'
    '<p>SCNS marks this course available for dual enrolment, and records the high-school credit earned '
    'as <strong>ELECTIVE</strong>. &#9888; Ten numbers in the <code>ENC</code> prefix carry LANGUAGE ARTS '
    'instead, so the field does discriminate within the prefix &mdash; <strong>a dual-enrolled student '
    'taking this course for a high-school language-arts requirement may receive elective credit toward '
    'graduation instead.</strong> The college credit is unaffected. Confirm with your counsellor and '
    'your district articulation agreement.</p>'
    '<h3>The 4-credit variant</h3>'
    '<p>Three institutions carry <code>ENC1101C</code> at <strong>4 credits</strong> rather than 3. '
    'Same subject; the extra credit reflects additional scheduled instruction. If you are transferring '
    'in either direction, the credit count is what to check against your degree audit.</p>'

    '<h2>AI Integration</h2>'
    '<p>No course in the catalogue has been changed more by generative AI than first-year composition, '
    'and you should expect your institution to have an explicit policy. <strong>Read it in week one and '
    'take it literally</strong> &mdash; policies range from prohibition to required use with disclosure, '
    'and they differ between sections of the same course.</p>'
    '<p>&#9888;&#9888; <strong>The tool&rsquo;s characteristic failure is exactly what this course '
    'teaches you to avoid.</strong> A language model produces fluent, average, audience-neutral prose: '
    'confident sentences with no particular reader in mind. This course is about the '
    '<em>rhetorical situation</em> &mdash; writing for a specific audience and purpose. Generated text '
    'is competent at the sentence level and vacant at exactly the level being assessed, which is why '
    'it so often earns a mediocre grade even when it is not detected.</p>'
    '<p>Where AI use is permitted, the defensible uses are the ones that leave the thinking with you: '
    'brainstorming counter-arguments, explaining a comment you did not understand, checking whether a '
    'paragraph delivers what its topic sentence promises. <strong>You remain answerable for every '
    'sentence you submit, including its facts.</strong></p>',

    {
        'summary': '39 Florida public institutions carry ENC1101 at 3 credits under 33 distinct titles; '
                   'three carry ENC1101C at 4 credits. Gulf Coast State College publishes 3 lecture '
                   'hours per week.',
        'hours_source': 'published',
        'derived_contact_hours': 45,
        'derivation': 'Gulf Coast State College publishes 3 credit hours and 3 lecture hours per week, '
                      'which is 45 contact hours over a 15-week term and matches the Florida convention '
                      'for a 3-credit lecture course.',
        'offerings': [
            {'institution': 'GCSC', 'institution_name': 'Gulf Coast State College',
             'title': 'English Composition I', 'credits': 3, 'contact_hours': 45,
             'note': 'Publishes 3 lecture hours per week and a $5.00 lab fee. Offered fall, spring and summer.'},
            {'institution': 'FSCJ', 'institution_name': 'Florida State College at Jacksonville',
             'title': 'Freshman Communication Skills I', 'credits': 4, 'contact_hours': None,
             'note': 'Carries the 4-credit ENC1101C form rather than the 3-credit bare number.'},
        ],
    })

# ── STA2023 ─────────────────────────────────────────────────────────────────
GUIDES['STA2023'] = guide(
    'Statistical Methods I',
    3, 45,
    'No statewide prerequisite, but institutions gate on mathematics placement: completion of '
    'developmental mathematics, a qualifying placement score, or a state exemption. '
    'IMPORTANT: this is a Florida General Education Core course and satisfies the MATHEMATICS area at '
    'every Florida public institution. A Gordon Rule designation is recorded at most carriers, and a '
    'Gordon Rule course needs a grade of C or HIGHER to count - a C-minus does not. '
    'PRACTICAL: a graphing calculator is usually required and the permitted model may be restricted - '
    'Gulf Coast State College allows only the TI-83/84 on test days. Check before buying. '
    'Register by NUMBER: 39 Florida public institutions carry STA2023 at 3 credits under 22 different '
    'titles; one carries STA2023C.',
    '<h2>Course Description</h2>'
    '<p><strong>Statistical Methods I</strong> is Florida&rsquo;s standard introductory statistics '
    'course and, for most students, the mathematics course that actually gets used later. The statewide '
    'description is recent and specific: students <strong>use descriptive and inferential statistical '
    'methods in contextual situations, with technology as appropriate</strong>, to build problem-solving '
    'ability and data interpretation. The state adds that it is <em>&ldquo;appropriate for students in a '
    'wide range of disciplines and programs&rdquo;</em> &mdash; which is the point of it.</p>'
    '<p>It is carried by <strong>39 Florida public institutions</strong> at 3 credits under 22 distinct '
    'titles &mdash; Elementary Statistics, Statistical Methods, Statistics, Honors Elementary Statistics '
    'and others.</p>'
    '<p>&#9888;&#9888; <strong>The statewide title carries the (GE CORE) marker.</strong></p>'

    '<h2>Learning Outcomes</h2>'
    '<h3>Required Outcomes</h3>'
    '<p>The state&rsquo;s own outcomes, from the SCNS record:</p>'
    + li('<strong>Visualise and summarise data</strong> using descriptive statistics.',
         'Apply <strong>basic probability concepts</strong> to draw reasonable conclusions.',
         'Employ <strong>random variables, sampling distributions and the Central Limit Theorem</strong> to analyse and interpret representations of data.',
         'Choose an appropriate method of <strong>inferential statistics</strong> &mdash; including confidence intervals and hypothesis testing &mdash; to make broader decisions from sample data.',
         'Model linear relationships between quantitative variables using <strong>correlation and linear regression</strong>.') +
    '<h3>Optional Outcomes</h3>'
    + li('Use a statistical package (R, Minitab, SPSS, Excel) rather than a calculator alone.',
         'Carry out and report a small project on real data.',
         'Extend to chi-square tests or one-way ANOVA where the institution has time.') +

    '<h2>Major Topics</h2>'
    '<h3>Required Topics</h3>'
    + li('Sampling, study design, and the difference between an observational study and an experiment.',
         'Descriptive statistics: centre, spread, shape; boxplots and histograms.',
         'Probability, random variables, and the normal distribution.',
         'Sampling distributions and the Central Limit Theorem.',
         'Confidence intervals and hypothesis testing for means and proportions.',
         'Correlation and simple linear regression.') +
    '<h3>Optional Topics</h3>'
    + li('Chi-square tests of independence and goodness of fit.',
         'One-way analysis of variance.',
         'Non-parametric alternatives.',
         'Type I and Type II error and statistical power, treated quantitatively.') +

    '<h2>Resources &amp; Tools</h2>'
    '<ul>'
    '<li>&#9888;&#9888; <strong>A graphing calculator is normally required, and the model may be '
    'restricted.</strong> Gulf Coast State College permits <strong>only the TI-83/84 on test days</strong>. '
    'Check your section&rsquo;s rule before buying &mdash; this is a real and avoidable expense.</li>'
    '<li>Many institutions now use open resources such as <em>OpenIntro Statistics</em> or OpenStax '
    '<em>Introductory Statistics</em>.</li>'
    '<li>Software varies: Excel, StatCrunch, Minitab, SPSS or R, depending on the department.</li>'
    '</ul>'

    '<h2>Career Pathways</h2>'
    '<p>Statistics is a prerequisite rather than a destination, and it is named on career paths in this '
    'repository for concrete reasons:</p>'
    '<ul>'
    '<li><strong>Registered Nurse</strong> &mdash; baccalaureate nursing requires it, and it is what makes '
    'evidence-based practice coursework readable rather than recited.</li>'
    '<li><strong>Lawyer</strong> &mdash; expert evidence, sampling and significance appear in employment '
    'discrimination, antitrust and toxic-tort litigation.</li>'
    '<li>Psychology, sociology, education, public health, business analytics and every laboratory '
    'science require it or a successor course.</li>'
    '</ul>'

    '<h2>Special Information</h2>'
    + GE_CORE + GORDON + TITLES +
    '<h3>&#9888; This is not the calculus-based statistics course</h3>'
    '<p>Programmes in engineering, economics and mathematics frequently require a calculus-based '
    'statistics course instead, numbered separately in Florida. <strong>If your degree names a specific '
    'statistics number, take that one</strong> &mdash; the credit for this course will transfer, but it '
    'may not satisfy that requirement.</p>'
    '<h3>Dual enrolment</h3>'
    '<p>SCNS marks the course available for dual enrolment with <strong>ELECTIVE</strong> high-school '
    'credit. The college credit is unaffected, but a student expecting it to fill a high-school '
    'mathematics graduation requirement should confirm with their counsellor first.</p>'

    '<h2>AI Integration</h2>'
    '<p>Statistics is a field where AI tools are genuinely useful and characteristically wrong in the '
    'same breath. A language model will produce a confident, well-formatted hypothesis test &mdash; and '
    'will frequently choose the wrong test, ignore whether its assumptions hold, or interpret a p-value '
    'as the probability that the hypothesis is true.</p>'
    '<p>&#9888;&#9888; <strong>That last error is the one this course exists to prevent</strong>, and it '
    'is the most common misstatement in published work as well. If you cannot say what the p-value is '
    'the probability <em>of</em>, you cannot check the tool.</p>'
    '<p>Defensible uses: explaining output you already produced, generating practice problems, writing '
    'the code for an analysis you have already specified. <strong>Deciding which test to run is the '
    'course.</strong></p>',

    {
        'summary': '39 Florida public institutions carry STA2023 at 3 credits under 22 distinct titles; '
                   'one carries STA2023C. No institution in the checked set publishes a contact-hour '
                   'figure for this course.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': 'Florida convention for a 3-credit lecture course: 45 contact hours over a '
                      '15-week term. Gulf Coast State College publishes the course but not its hours.',
        'offerings': [
            {'institution': 'GCSC', 'institution_name': 'Gulf Coast State College',
             'title': 'Statistics', 'credits': 3, 'contact_hours': None,
             'note': 'Prerequisite: developmental completion, placement score or state exemption. '
                     'Graphing calculator required; only the TI-83/84 permitted on test days.'},
            {'institution': 'UNF', 'institution_name': 'University of North Florida',
             'title': 'Introductory Statistics with Recitation', 'credits': 3, 'contact_hours': None,
             'note': 'Carries the STA2023C form; the only public carrier of that id.'},
        ],
    })


def _anatomy(num, roman, which, desc_html, outcomes, topics, notes, extra=''):
    return guide(
        'Anatomy and Physiology %s' % roman,
        3, 45,
        'No statewide prerequisite, though many institutions require a prior biology or chemistry '
        'course, or placement. '
        'REGISTRATION, and this is the thing to get right: 19 Florida public institutions teach this as '
        'a 3-credit LECTURE paired with BSC%sL, a 1-credit laboratory, while 7 others teach a single '
        '4-credit integrated course, BSC%sC. No institution carries both forms. The outcomes are the '
        'same and transfer works either way - lecture plus laboratory completes exactly as the combined '
        'course does - but where your institution splits it you must enrol in BOTH halves. They are '
        'normally corequisites. '
        'Health-professions programmes name these courses by number, and some Florida institutions '
        'teach the same subject under APK2100C/APK2105C instead. Check the exact numbers your target '
        'programme lists.' % (num, num),
        desc_html
        + '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>' + outcomes
        + '<h3>Optional Outcomes</h3>'
        + li('Perform dissection or work with prosected material, where the laboratory includes it.',
             'Use physiology data-acquisition equipment for muscle, nerve or cardiovascular recording.',
             'Apply clinical correlations and case studies, common where the course serves health programmes.')
        + '<h2>Major Topics</h2><h3>Required Topics</h3>' + topics
        + '<h3>Optional Topics</h3>'
        + li('Clinical case correlation and pathophysiology previews.',
             'Histology beyond the core tissue types.',
             'Imaging and anatomical visualisation software.')
        + '<h2>Resources &amp; Tools</h2><ul>'
        '<li>A major A&amp;P text with an atlas; Florida institutions commonly use Marieb, Tortora or '
        'OpenStax <em>Anatomy and Physiology</em>, which is free.</li>'
        '<li>Laboratory: models, prosected specimens or dissection material, microscopes, and often a '
        'physiology data-acquisition system.</li>'
        '<li>&#9888; Laboratory fees are common and are charged separately from tuition.</li>'
        '</ul>'
        '<h2>Career Pathways</h2>'
        '<p>This is the gateway science for the health professions in Florida, and it is the course '
        'competitive admission most often turns on:</p><ul>'
        '<li><strong>Registered Nurse</strong> &mdash; named on the Registered Nurse path in this repository.</li>'
        '<li>Respiratory therapy, radiography, dental hygiene, physical and occupational therapy assisting, '
        'paramedic, surgical technology, medical laboratory science.</li>'
        '<li>Pre-professional preparation for medicine, dentistry, physician assistant and physical therapy programmes.</li>'
        '<li>Exercise science, athletic training and kinesiology.</li>'
        '</ul>'
        '<h2>Special Information</h2>' + PACKAGING + extra
        + '<h3>&#9888; The other prefix family</h3>'
        '<p>Florida teaches this subject under <strong>two prefix families</strong>: '
        '<code>BSC2085</code>/<code>BSC2086</code> and <code>APK2100C</code>/<code>APK2105C</code>. '
        '<strong>BSC is what nearly every health-professions prerequisite list actually names.</strong> '
        'The credit articulates either way, but a requirement stated by course number may not. If your '
        'institution offers the APK family and your target programme names BSC, get the substitution in '
        'writing before you register.</p>'
        '<h3>What this course demands</h3>'
        '<p>A&amp;P has a reputation for volume, and it is deserved: the vocabulary load in the first '
        'weeks is closer to a language course than a science one. Students who treat it as a memorisation '
        'exercise tend to stall at the physiology. <strong>Plan 8&ndash;12 hours a week outside class</strong>, '
        'and use the laboratory time actively &mdash; it is where the structures become memorable.</p>',
        notes)


# ── BSC2085 ─────────────────────────────────────────────────────────────────
GUIDES['BSC2085'] = _anatomy(
    '2085', 'I', 'first',
    '<h2>Course Description</h2>'
    '<p><strong>Anatomy and Physiology I</strong> is the first half of the two-semester sequence that '
    'gates admission to almost every health programme in Florida. The statewide description is recent '
    'and detailed: students examine human anatomy and physiology <strong>through a systems approach '
    'based on the interaction between form and function</strong>, from the microscopic components of '
    'cells and tissues to the organismal level, with emphasis on <strong>histology and the integumentary, '
    'skeletal, muscular and nervous systems</strong>.</p>'
    '<p>Twenty Florida public institutions carry <code>BSC2085</code> as a 3-credit lecture; seven carry '
    'the integrated 4-credit <code>BSC2085C</code>. Twenty-three of twenty-five records carry a '
    '<strong>natural science</strong> general-education designation.</p>'
    '<p>&#9888;&#9888; <strong>The statewide title carries the (GE CORE) marker</strong> &mdash; see below.</p>',
    li('Identify <strong>cell structures</strong> and describe their functions.',
       'Distinguish <strong>tissues</strong> by structure and location, and contrast their normal physiology.',
       'Demonstrate understanding of <strong>anatomical organisation</strong> &mdash; cavities, planes and directional terms.',
       'Identify and describe structures of the <strong>integumentary, skeletal, muscular and nervous systems</strong>.',
       'Interpret the <strong>functions</strong> of those four systems.',
       'Explain how the components of the human body maintain <strong>homeostasis</strong>.',
       'Analyse and interpret <strong>physiological data</strong>.'),
    li('Anatomical terminology, body organisation, planes and cavities.',
       'Chemistry and cell biology as they bear on physiology.',
       'Histology: epithelial, connective, muscle and nervous tissue.',
       'The integumentary system.',
       'The skeletal system, bone tissue and articulations.',
       'The muscular system and the physiology of muscle contraction.',
       'The nervous system: neurons, central and peripheral organisation, and the special senses.',
       'Homeostasis as the organising principle throughout.'),
    {
        'summary': 'Twenty Florida public institutions carry BSC2085 as a 3-credit lecture, 19 of them '
                   'pairing it with the 1-credit BSC2085L; seven carry the integrated 4-credit '
                   'BSC2085C. No institution carries both forms.',
        'hours_source': 'published',
        'derived_contact_hours': 45,
        'derivation': 'Gulf Coast State College publishes 3 credit hours and 3 lecture hours per week '
                      'for the lecture (45 contact hours), and 1 credit with 2 laboratory hours per '
                      'week for BSC2085L (30 contact hours).',
        'offerings': [
            {'institution': 'GCSC', 'institution_name': 'Gulf Coast State College',
             'title': 'Human Anatomy and Physiology I', 'credits': 3, 'contact_hours': 45,
             'note': 'Publishes 3 lecture hours per week. Corequisite: BSC2085L, or consent of the '
                     'Natural Sciences division chair. BSC2085L is 1 credit at 2 laboratory hours per week.'},
            {'institution': 'UCF', 'institution_name': 'University of Central Florida',
             'title': 'Anatomy and Physiology I', 'credits': 4, 'contact_hours': None,
             'note': 'Carries the integrated 4-credit BSC2085C form.'},
        ],
    },
    extra=GE_CORE +
    '<h3>&#9888;&#9888; The two halves are not recorded the same way &mdash; and it affects dual enrolment</h3>'
    '<p>This is worth knowing because nothing a student reads says it. The statewide records for the two '
    'halves of this sequence are visibly of different vintages:</p>'
    '<ul>'
    '<li><strong>BSC2085</strong> carries the <strong>(GE CORE)</strong> marker, a recently written '
    'description and seven explicit learning outcomes &mdash; and records <strong>ELECTIVE</strong> '
    'high-school credit for dual enrolment.</li>'
    '<li><strong>BSC2086</strong> carries none of that: an older one-sentence description, no GE Core '
    'marker &mdash; and records <strong>SCIENCE</strong> high-school credit.</li>'
    '</ul>'
    '<p>&#9888; So a dual-enrolled high-school student may earn <em>elective</em> credit for the first '
    'half and <em>science</em> credit for the second, on two halves of one sequence. The college credit '
    'is unaffected in both cases. <strong>Confirm with your counsellor and your district articulation '
    'agreement before relying on either.</strong></p>')

# ── BSC2086 ─────────────────────────────────────────────────────────────────
GUIDES['BSC2086'] = _anatomy(
    '2086', 'II', 'second',
    '<h2>Course Description</h2>'
    '<p><strong>Anatomy and Physiology II</strong> completes the two-semester sequence begun in '
    '<code>BSC2085</code>, carrying the systems approach through the remaining organ systems. Where the '
    'first course concentrates on histology and the integumentary, skeletal, muscular and nervous '
    'systems, the second takes up the <strong>endocrine, cardiovascular, lymphatic and immune, '
    'respiratory, digestive, urinary and reproductive systems</strong>, together with fluid, electrolyte '
    'and acid&ndash;base balance.</p>'
    '<p>Nineteen Florida public institutions carry <code>BSC2086</code> as a 3-credit lecture; seven '
    'carry the integrated 4-credit <code>BSC2086C</code>.</p>'
    '<p>&#9888; <strong>The statewide record for this half is thin.</strong> Where the record for '
    '<code>BSC2085</code> was rewritten recently with explicit learning outcomes, this one still reads '
    '<em>&ldquo;human anatomy and physiology for health science majors with no prerequisites and offered '
    'as second of two semester courses&rdquo;</em> and nothing more. The outcomes and topics below are '
    'therefore drawn from what Florida institutions actually teach in the second half, and from the '
    'structure the first course&rsquo;s record establishes &mdash; they are not quoted from the state.</p>',
    li('Identify and describe the structures of the <strong>endocrine, cardiovascular, lymphatic, respiratory, digestive, urinary and reproductive systems</strong>.',
       'Interpret the <strong>functions</strong> of those systems and their interactions.',
       'Explain <strong>fluid, electrolyte and acid&ndash;base balance</strong> and the mechanisms that maintain them.',
       'Trace the path of <strong>blood, air, nutrients and filtrate</strong> through their respective systems.',
       'Explain how the systems covered contribute to <strong>homeostasis</strong>.',
       'Analyse and interpret <strong>physiological data</strong>, including cardiovascular and respiratory measurements.'),
    li('The endocrine system and hormonal control.',
       'Blood, the heart, and the vasculature; cardiac cycle and haemodynamics.',
       'The lymphatic system and immunity.',
       'The respiratory system and gas exchange.',
       'The digestive system, metabolism and nutrition.',
       'The urinary system, and fluid, electrolyte and acid&ndash;base balance.',
       'The reproductive systems and, usually, development and heredity.'),
    {
        'summary': 'Nineteen Florida public institutions carry BSC2086 as a 3-credit lecture, paired '
                   'with the 1-credit BSC2086L; seven carry the integrated 4-credit BSC2086C.',
        'hours_source': 'published',
        'derived_contact_hours': 45,
        'derivation': 'Gulf Coast State College publishes 3 credit hours and 3 lecture hours per week '
                      'for the lecture (45 contact hours), and 1 credit at 2 laboratory hours per week '
                      'for BSC2086L (30 contact hours).',
        'offerings': [
            {'institution': 'GCSC', 'institution_name': 'Gulf Coast State College',
             'title': 'Human Anatomy and Physiology II', 'credits': 3, 'contact_hours': 45,
             'note': 'Publishes 3 lecture hours per week; BSC2086L is 1 credit at 2 laboratory hours per week.'},
            {'institution': 'UCF', 'institution_name': 'University of Central Florida',
             'title': 'Anatomy and Physiology II', 'credits': 4, 'contact_hours': None,
             'note': 'Carries the integrated 4-credit BSC2086C form.'},
        ],
    },
    extra='<h3>&#9888;&#9888; This half of the sequence has NOT been revised, and it shows</h3>'
    '<p>The statewide record for <code>BSC2085</code> was rewritten recently: a full description, seven '
    'learning outcomes, and the <strong>(GE CORE)</strong> marker identifying it as a Florida General '
    'Education Core course. <strong>The record for this course carries none of those.</strong> Its title '
    'is still the older <em>&ldquo;Anatomy &amp; Physiology (2 of 2) (HS Maj.) No Prereq&rdquo;</em> and '
    'its description is a single sentence.</p>'
    '<p>Two practical consequences:</p>'
    '<ul>'
    '<li>&#9888; <strong>Do not assume this half carries General Education Core protection because the '
    'first half does.</strong> If you are relying on it to satisfy a general-education natural-science '
    'requirement after transfer, confirm it with the receiving institution.</li>'
    '<li>The high-school credit recorded for dual enrolment is <strong>SCIENCE</strong> here, where the '
    'first half records <strong>ELECTIVE</strong> &mdash; the opposite of what the markers would lead you '
    'to expect. The college credit is unaffected.</li>'
    '</ul>'
    '<p>&#9888; None of this reflects on the teaching. Florida institutions teach the second half as a '
    'full partner to the first; it is the <em>state record</em> that is out of date, and it is worth '
    'knowing so that you check rather than assume.</p>')


def main():
    os.makedirs(DRAFTS, exist_ok=True)
    for cid, g in GUIDES.items():
        p = os.path.join(DRAFTS, '%s_guide.json' % cid)
        io.open(p, 'w', encoding='utf-8').write(
            json.dumps(g, ensure_ascii=False, indent=1))
        print('%-9s %-34s %d cr / %d hrs | prereq %4d chars | html %6d bytes'
              % (cid, g['title'][:34], g['credits'], g['contact_hours'],
                 len(g['prerequisites']), len(g['html_content'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
