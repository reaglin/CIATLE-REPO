# -*- coding: utf-8 -*-
"""Batch 254: write the four requested STA guides to drafts/ (run from Tools/).

    python scratchpad/b254_build.py

Sources (2026-11-23): SCNS flat file (carriers, credits, statewide titles); FIU, FAU and FSU Coursedog caches
(STA2122, STA3123, STA3024); UCF Kuali (STA2360, STA2023); UWF STA prefix PDF (STA2360, STA2023); Gulf Coast's
STA catalogue page (STA2122, STA2023); cloud.usf.edu (STA2122, STA3024); UF course-search API (STA3024 title).
Not read: FGCU (JS-rendered), Tallahassee State, FAMU, Eastern Florida (no fetchable route); coursicle 429;
catalog.usf.edu 403; catalog.ufl.edu search page timed out.
"""
import io
import json
import os
import sys

sys.path.insert(0, 'scratchpad')
from b251_build import lg, ul, table, off  # noqa: E402  (helpers only; importing does not rewrite drafts)

G = {}

STAT_AI = (
    '<h2>AI Integration (Optional)</h2><p>AI assistants are good at explaining a test in plain words, writing the '
    'code for an analysis in R, Python or SAS, and checking a hand calculation. They are poor at the judgement this '
    'course teaches: whether the data meet a test\'s assumptions, whether a sample can support the claim being made, '
    'and whether a correlation is being read as a cause. A model will usually run whatever test you name and report a '
    'p-value with confidence, including on data that do not justify it. Treat its output as a draft: check the '
    'assumptions yourself, rerun the numbers in the course software, and write the interpretation in your own words. '
    'Follow your instructor\'s policy on AI use in homework and exams.</p>')

# ---------------------------------------------------------------------------------------------------- STA2122
G['STA2122'] = dict(
    title='Social Science Statistics',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("Varies by institution. Gulf Coast State: a satisfactory math placement score or MAT 1033 with a C "
                   "or better; a TI-83/84 graphing calculator is required. FSU, USF, FGCU and Tallahassee State: check "
                   "the catalogue (college algebra readiness is the usual expectation). CREDITS DIFFER: 3 credits at "
                   "FGCU, FSU and USF; 4 at Gulf Coast State and Tallahassee State. GEN ED: at Gulf Coast State, STA "
                   "2023 and STA 2122 together do not meet the six-hour mathematics requirement, so taking both does "
                   "not finish it. STA 2122 is not the statewide core statistics course (that is STA 2023); if a "
                   "programme you plan to enter names STA 2023, ask whether it accepts STA 2122."),
    offering_notes={
        'summary': ('Five Florida public institutions carry STA2122: FGCU, Florida State and USF at 3 credits; Gulf '
                    'Coast State College and Tallahassee State College at 4.'),
        'hours_source': 'mixed', 'derived_contact_hours': 45,
        'derivation': ("Gulf Coast State publishes 4 lecture hours a week (60 a term). FSU's catalogue record gives 3 "
                       "contact hours a week (45). The others publish none; 45 is Florida's convention for a 3-credit "
                       "lecture."),
        'offerings': [
            off('FGCU', 'Florida Gulf Coast University', 'Social Science Statistics', 3,
                'Catalogue not readable by tooling; title and credits from the statewide course file.'),
            off('FSU', 'Florida State University', 'Introduction to Applied Statistics', 3,
                'Normal distributions to multiple regression, ANOVA and chi-square; aimed at natural-science '
                'students; counts toward FSU Liberal Studies Quantitative and Logical Thinking.', 45),
            off('GCSC', 'Gulf Coast State College', 'Statistical Applications in Social Sciences I', 4,
                'Offered spring. Described as more in-depth than STA 2023. 4 lecture hours a week.', 60),
            off('TSC', 'Tallahassee State College', 'Introduction to Applied Statistics', 4,
                'Catalogue not readable by tooling; title and credits from the statewide course file.'),
            off('USF', 'University of South Florida', 'Social Science Statistics', 3,
                'Taught by the Department of Sociology and Interdisciplinary Social Sciences; counts toward USF '
                'general education mathematics and the state computation requirement.'),
        ]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>STA2122</strong> is a first course in statistics taught with the social and behavioural sciences '
        'in mind. The statewide course record calls it <strong>Statistical Applications in Social Science I</strong>; '
        'five Florida public institutions carry it, under three titles: <em>Social Science Statistics</em> (FGCU, '
        'USF), <em>Introduction to Applied Statistics</em> (Florida State, Tallahassee State) and <em>Statistical '
        'Applications in Social Sciences I</em> (Gulf Coast State).</p>'
        '<p>The published descriptions agree on the core: describing data, probability and the normal distribution, '
        'sampling, confidence intervals and hypothesis tests, correlation and regression, chi-square tests, analysis '
        'of variance and an introduction to non-parametric methods. USF\'s description stresses vocabulary, '
        'running analyses and drawing conclusions about research questions; Gulf Coast State calls its version a '
        'more in-depth study than STA 2023; Florida State aims its version at students heading into the natural '
        'sciences and puts weight on interpreting results in context.</p>'
        '<p>It is an alternative to <strong>STA 2023</strong>, the general statistics course that most Florida '
        'programmes name. The two cover much of the same ground, which is why FIU retired its own STA 2122 in 2026 as '
        'redundant to STA 2023. The difference is the examples and the reach: STA 2122 spends more time on the '
        'methods social-science research uses, such as ANOVA and contingency tables.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>' + lg([
            'Summarise data with tables, graphs and descriptive statistics (mean, median, standard deviation, '
            'percentiles), and choose the right summary for the type of variable.',
            'Use the normal distribution and sampling distributions to find probabilities and explain the central '
            'limit theorem in words.',
            'Construct and interpret confidence intervals for means and proportions.',
            'Carry out and interpret hypothesis tests (one- and two-sample t tests, tests for proportions, chi-square '
            'tests of independence), including what a p-value does and does not mean.',
            'Fit and interpret correlation and simple linear regression, and explain why correlation does not show '
            'causation.',
            'Run a one-way analysis of variance and interpret the result.',
            'Read the statistics reported in a social-science article and judge whether the conclusions follow.',
        ]) + '<h3>Optional Outcomes</h3>' + lg([
            'Two-way ANOVA and multiple regression (Florida State).',
            'Non-parametric alternatives when assumptions fail (Gulf Coast State, Florida State).',
            'Use statistical software (SPSS, R, Excel or a graphing calculator) to run the analyses.',
            'Write a short report of an analysis for a non-specialist reader.',
        ]) +
        '<h2>Major Topics</h2><h3>Required Topics</h3>' + lg([
            'Variables, levels of measurement, samples and populations, study design (surveys, experiments, '
            'observational studies).',
            'Descriptive statistics and graphs.',
            'Probability, the normal distribution and sampling distributions.',
            'Confidence intervals; hypothesis testing; type I and type II errors.',
            't tests; chi-square tests; correlation and simple regression; one-way ANOVA.',
        ]) + '<h3>Optional Topics</h3>' + lg([
            'Two-way ANOVA; multiple regression.',
            'Non-parametric tests (sign, Wilcoxon, Mann-Whitney, Kruskal-Wallis).',
            'Effect size and statistical power.',
            'Survey sampling and questionnaire data.',
        ]) +
        '<h2>Resources &amp; Tools</h2>' + ul([
            'An introductory statistics text for the social or behavioural sciences (the syllabus names the edition).',
            'A TI-83/84 graphing calculator (required at Gulf Coast State) or statistical software: SPSS, R, Excel.',
            'Public data for practice: U.S. Census Bureau, the General Social Survey, Florida CHARTS (health data).',
        ]) +
        '<h2>Career Pathways</h2>' + ul([
            'A required or recommended course for majors in sociology, psychology, criminology, political science, '
            'social work and public health.',
            'Leads toward research assistant, survey and market research (SOC 19-3022 Survey Researchers, 13-1161 '
            'Market Research Analysts) and social science research roles.',
        ]) +
        '<h2>Special Information</h2>'
        '<h3>Offering Notes</h3>' + table(['Institution', 'Title', 'Credits', 'Contact hours'], [
            ['Florida Gulf Coast University', 'Social Science Statistics', '3', 'not published (45 derived)'],
            ['Florida State University', 'Introduction to Applied Statistics', '3', '3 a week (45)'],
            ['Gulf Coast State College', 'Statistical Applications in Social Sciences I', '4', '4 lecture a week (60)'],
            ['Tallahassee State College', 'Introduction to Applied Statistics', '4', 'not published (60 derived)'],
            ['University of South Florida', 'Social Science Statistics', '3', 'not published (45 derived)'],
        ]) +
        '<p>A student who takes the 4-credit version at Gulf Coast State or Tallahassee State and transfers to a '
        'university that carries it at 3 credits brings one credit more than the course it is matched to; the '
        'reverse leaves a student one credit short. Check the extra credit against your degree\'s total.</p>'
        '<h3>STA 2122 and STA 2023</h3><p>STA 2023 is the statistics course in Florida\'s general education core; '
        'STA 2122 is not. Both count as mathematics at some institutions (USF and Florida State list STA 2122 in '
        'their general education), but they overlap so much that Gulf Coast State does not let the pair complete '
        'its six-hour mathematics requirement. Many programmes in business, nursing and the health professions name '
        'STA 2023 as a prerequisite. If yours does, ask before taking STA 2122 instead.</p>'
        '<h3>Next course</h3><p>The second course in the sequence is <strong>STA 3123</strong> (statewide title '
        'Statistical Applications in Social Science II), carried at FIU, or a research methods course in the major.</p>'
        + STAT_AI),
)

# ---------------------------------------------------------------------------------------------------- STA3123
G['STA3123'] = dict(
    title='Statistics for Behavioral and Social Sciences II',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("A first statistics course: STA 2023, or STA 2122 where it is still offered; check FIU's "
                   "catalogue for the exact rule and minimum grade. FIU is the only Florida public institution with "
                   "an active STA 3123 (3 credits). The statewide course file also lists FAU at 4 credits under the "
                   "title Statistics in Behavioral Analysis, but FAU's current catalogue does not include the course. "
                   "Upper-division (3000-level)."),
    offering_notes={
        'summary': ('FIU carries STA3123 at 3 credits. The statewide course file also lists FAU (4 credits, Statistics '
                    'in Behavioral Analysis), but the course is not in FAU\'s current catalogue.'),
        'hours_source': 'derived', 'derived_contact_hours': 45,
        'derivation': "FIU publishes no contact hours; 45 is Florida's convention for a 3-credit lecture.",
        'offerings': [
            off('FIU', 'Florida International University', 'Statistics for Behavioral and Social Sciences II', 3,
                'Small-sample inference, t, chi-square and F distributions, ANOVA, regression, correlation, '
                'non-parametric tests, goodness of fit and independence. Offered fall, spring and summer.'),
            off('FAU', 'Florida Atlantic University', 'Statistics in Behavioral Analysis', 4,
                'Listed in the statewide course file (last changed 1999) but not in FAU\'s current catalogue.'),
        ]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>STA3123</strong> is the second course in statistics for students in the behavioural and social '
        'sciences. The statewide course record calls it <strong>Statistical Applications in Social Science II</strong>, '
        'the sequel to STA 2122. Florida International University teaches it as <em>Statistics for Behavioral and '
        'Social Sciences II</em> and describes it as: small sample statistical inference for means and variances; the '
        't, chi-square and F distributions; analysis of variance, regression and correlation; basic non-parametric '
        'tests; goodness-of-fit tests and tests of independence.</p>'
        '<p>FIU is the only Florida public institution with an active STA 3123, so its catalogue is the authority on '
        'content. Where this guide goes beyond FIU\'s one-paragraph description, it says so.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>' + lg([
            'Choose between large-sample and small-sample methods, and use the t distribution for inference about '
            'one mean and about two means (independent and paired samples).',
            'Make inferences about variances with the chi-square and F distributions.',
            'Carry out and interpret one-way analysis of variance, including checking its assumptions.',
            'Fit and interpret simple linear regression and correlation, including tests on the slope and the '
            'correlation coefficient.',
            'Carry out chi-square goodness-of-fit tests and tests of independence on categorical data.',
            'Choose and apply a basic non-parametric test when the assumptions of a t test or ANOVA do not hold.',
        ]) + '<h3>Optional Outcomes</h3>' + lg([
            'Multiple comparisons after ANOVA (Tukey, Bonferroni).',
            'Introduction to multiple regression.',
            'Report an analysis in APA style, as psychology and social-science journals expect.',
            'Use SPSS, R or another package for every analysis in the course.',
        ]) +
        '<h2>Major Topics</h2><h3>Required Topics</h3>' + lg([
            'Review of sampling distributions, confidence intervals and hypothesis testing.',
            't procedures: one sample, two independent samples, paired samples.',
            'Chi-square and F distributions; inference about variances.',
            'One-way ANOVA.',
            'Correlation and simple linear regression.',
            'Chi-square goodness of fit and tests of independence.',
            'Non-parametric tests (sign, Wilcoxon signed-rank, Mann-Whitney, Kruskal-Wallis).',
        ]) + '<h3>Optional Topics</h3>' + lg([
            'Two-way ANOVA and interaction.',
            'Multiple regression.',
            'Effect size and power.',
        ]) +
        '<h2>Resources &amp; Tools</h2>' + ul([
            'An applied statistics text for the behavioural sciences (the syllabus names the edition).',
            'Statistical software: SPSS is common in psychology and the social sciences; R and Excel are used too.',
        ]) +
        '<h2>Career Pathways</h2>' + ul([
            'A methods course for psychology, sociology, criminal justice and social work majors, and preparation '
            'for graduate study in those fields, where statistics is a core requirement.',
            'Research assistant, survey researcher (SOC 19-3022) and market research analyst (13-1161) roles.',
        ]) +
        '<h2>Special Information</h2>'
        '<h3>Offering Notes</h3>' + table(['Institution', 'Title', 'Credits', 'Contact hours'], [
            ['Florida International University', 'Statistics for Behavioral and Social Sciences II', '3',
             'not published (45 derived)'],
            ['Florida Atlantic University', 'Statistics in Behavioral Analysis', '4',
             'not in the current catalogue'],
        ]) +
        '<p>The statewide course file still lists FAU, at 4 credits, but FAU\'s current catalogue has no STA 3123. A '
        'student with an older FAU transcript showing the course has 4 credits for it; a student planning to take it '
        'now should look at FIU.</p>'
        '<h3>Where it sits</h3><p>The course follows a first statistics course. Its partner first course, STA 2122, '
        'was retired at FIU in 2026 as redundant to STA 2023, so at FIU students now usually reach STA 3123 from STA '
        '2023. At other universities the same material is taught under other numbers, for example a second '
        'statistics course in the psychology department (PSY prefix) or STA 3024 Introductory Statistics II at UF and '
        'USF. A course with a different number will not match STA 3123 automatically; bring the syllabus.</p>'
        + STAT_AI),
)

# ---------------------------------------------------------------------------------------------------- STA2360
G['STA2360'] = dict(
    title='Introduction to Data Science',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("None at UWF: no prior programming or statistics experience is needed. UCF's catalogue lists no "
                   "prerequisite either; check the current schedule. 3 credits at both. At UWF it meets the general "
                   "education mathematics requirement and the college-level computation skills requirement; at UCF "
                   "check how it counts before relying on it for general education."),
    offering_notes={
        'summary': 'Two Florida public institutions carry STA2360, both at 3 credits: UCF and UWF.',
        'hours_source': 'derived', 'derived_contact_hours': 45,
        'derivation': "Neither publishes contact hours; 45 is Florida's convention for a 3-credit lecture.",
        'offerings': [
            off('UCF', 'University of Central Florida', 'Introduction to Data Science', 3,
                'Exploratory data analysis, data visualisation and prediction, basic data science tools and machine '
                'learning.'),
            off('UWF', 'University of West Florida', 'Introduction to Data Science', 3,
                'Data ethics and the data science cycle: wrangling, exploratory analysis, visualisation, predictive '
                'modelling, communicating results, reproducible research. Meets general education mathematics.'),
        ]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>STA2360 Introduction to Data Science</strong> is a first course in data science, open to '
        'students with no programming or statistics background. Two Florida universities carry it, both at 3 '
        'credits and under the same title: the University of Central Florida and the University of West Florida. It '
        'is a recent number (both records were created in the 2020s), so expect the course to keep changing.</p>'
        '<p>UWF describes the whole <strong>data science cycle</strong>: data wrangling, exploratory data analysis, '
        'data visualisation, predictive modelling and communicating results, with data ethics and an emphasis on '
        '<strong>reproducible research</strong>. UCF\'s shorter description names exploratory data analysis, '
        'visualisation and prediction, basic data science tools and machine learning. The two agree on the core; UWF '
        'adds ethics and reproducibility explicitly.</p>'
        '<p>Because only two institutions carry it, the outcomes below separate what both describe (required) from '
        'what one names (optional).</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>' + lg([
            'Describe the stages of a data science project, from a question through data collection, cleaning, '
            'analysis and modelling to communicating the result.',
            'Import, clean and reshape a real data set (wrangling) with a data science tool.',
            'Explore data with summary statistics and graphs, and use visualisation to find patterns and problems.',
            'Build and evaluate a simple predictive model (for example linear regression or a classifier) and explain '
            'what its accuracy means.',
            'Explain basic ideas of machine learning: training and test data, overfitting, prediction error.',
            'Communicate findings in writing and with graphics to a non-specialist audience.',
        ]) + '<h3>Optional Outcomes</h3>' + lg([
            'Identify ethical issues in data work: privacy, consent, bias in data and models, and misleading graphics '
            '(UWF names data ethics).',
            'Produce a reproducible analysis, for example a notebook or script that someone else can rerun to get the '
            'same result (UWF).',
            'Write short programs in R or Python to automate an analysis.',
        ]) +
        '<h2>Major Topics</h2><h3>Required Topics</h3>' + lg([
            'What data science is; the data science cycle.',
            'Data types, tidy data, importing and cleaning data.',
            'Exploratory data analysis and visualisation.',
            'Introduction to prediction and machine learning.',
            'Communicating results.',
        ]) + '<h3>Optional Topics</h3>' + lg([
            'Data ethics and privacy.',
            'Reproducible research: notebooks, scripts, version control.',
            'Basic statistical inference as it applies to data science.',
        ]) +
        '<h2>Resources &amp; Tools</h2>' + ul([
            'R with RStudio and the tidyverse, or Python with Jupyter notebooks and pandas (the syllabus names the '
            'language).',
            'Free texts often used at this level: <em>R for Data Science</em> (Wickham, Cetinkaya-Rundel and '
            'Grolemund) and <em>Introduction to Modern Statistics</em> (OpenIntro).',
            'Public data: data.gov, U.S. Census Bureau, Florida Geographic Data Library, Kaggle data sets.',
        ]) +
        '<h2>Career Pathways</h2>' + ul([
            'A first step toward majors and minors in data science, statistics, computer science, business analytics '
            'and the sciences.',
            'Data scientists (SOC 15-2051), data analysts and operations research analysts (15-2031) all start from '
            'these skills; the jobs themselves usually require a bachelor\'s degree.',
            'Florida employers that hire data analysts include health systems, banks and insurers, the space and '
            'defence industry, and state agencies.',
        ]) +
        '<h2>Special Information</h2>'
        '<h3>Offering Notes</h3>' + table(['Institution', 'Title', 'Credits', 'Contact hours'], [
            ['University of Central Florida', 'Introduction to Data Science', '3', 'not published (45 derived)'],
            ['University of West Florida', 'Introduction to Data Science', '3', 'not published (45 derived)'],
        ]) +
        '<h3>General education</h3><p>At UWF the course meets the general education mathematics requirement and '
        'the college-level computation skills requirement. It is not one of the courses in Florida\'s statewide '
        'general education core, so another institution may count it only as an elective. Check before relying on '
        'it to complete your mathematics.</p>'
        '<h3>Transfer</h3><p>Only UCF and UWF carry STA 2360. Most Florida state colleges do not have an equivalent '
        'course yet; a student arriving with data science from elsewhere should bring the syllabus.</p>'
        '<h2>AI Integration (Optional)</h2><p>AI coding assistants are now part of data science work, and this '
        'course is a good place to learn to use them well. They write data-cleaning and plotting code quickly; they '
        'also invent column names, drop missing values without saying so, and choose a model without checking '
        'whether it fits the question. Read every line of generated code, rerun it yourself, and check the output '
        'against the data. Reproducibility (UWF\'s emphasis) is the protection: a script you can rerun and explain '
        'is yours, wherever the first draft came from. Do not paste private or personal data into a public AI tool, '
        'and follow your instructor\'s policy.</p>'),
)

# ---------------------------------------------------------------------------------------------------- STA3024
G['STA3024'] = dict(
    title='Introductory Statistics II / SAS for Data and Statistical Analyses',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("STA 2023 with a C or better at FAU and USF; USF also requires a calculus or finite math course "
                   "(MAC 2233, MAC 2241, MAC 2281 or MAC 2311, C or better) or AP Calculus or AP Statistics. Check "
                   "UF, FSU, FAMU and Eastern Florida. *** ONE NUMBER, TWO COURSES: at UF, USF, FAMU and Eastern "
                   "Florida (and in the statewide title) STA 3024 is a second statistics course; at FAU and Florida "
                   "State it is SAS for Data and Statistical Analyses, a SAS programming course. Credit can transfer "
                   "under the number while the content does not match. Upper-division (3000-level); 3 credits "
                   "everywhere."),
    offering_notes={
        'summary': ('Six Florida public institutions carry STA3024, all at 3 credits. UF, USF, FAMU and Eastern '
                    'Florida State teach a second statistics course; FAU and Florida State teach SAS programming.'),
        'hours_source': 'mixed', 'derived_contact_hours': 45,
        'derivation': ("FAU publishes 3 lecture hours and FSU 3 contact hours a week (45 a term); the others publish "
                       "none, and 45 is Florida's convention for a 3-credit course."),
        'offerings': [
            off('EFSC', 'Eastern Florida State College', 'Statistics 2 for Data Scientists', 3,
                'Statistics II reading. Catalogue not readable by tooling; title and credits from the statewide '
                'course file.'),
            off('FAMU', 'Florida A&M University', 'Introduction to Probability and Statistics II', 3,
                'Statistics II reading; the statewide course file\'s title. Catalogue not read.'),
            off('FAU', 'Florida Atlantic University', 'SAS for Data and Statistical Analyses', 3,
                'SAS reading. Lab-based introduction to the SAS language; prerequisite STA 2023 (C).', 45),
            off('FSU', 'Florida State University', 'SAS for Data and Statistical Analysis', 3,
                'SAS reading. Counts toward FSU\'s Digital Literacy requirement. Fall and spring.', 45),
            off('UF', 'University of Florida', 'Introduction to Statistics 2', 3,
                'Statistics II reading (title confirmed in UF\'s course search).'),
            off('USF', 'University of South Florida', 'Introductory Statistics II', 3,
                'Statistics II reading. Two-sample inference, ANOVA, regression, categorical data, non-parametrics.'),
        ]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>STA3024</strong> carries <strong>two different courses</strong> in Florida, and which one you '
        'get depends on the institution. Check your own catalogue before reading further.</p>'
        + table(['Reading', 'Where', 'What it is'], [
            ['<strong>Introductory Statistics II</strong> (the statewide title: Introduction to Probability and '
             'Statistics II)', 'UF, USF, FAMU, Eastern Florida State', 'the second course of a two-semester '
             'statistics sequence: two-sample inference, ANOVA, regression, categorical data, non-parametric '
             'methods'],
            ['<strong>SAS for Data and Statistical Analyses</strong>', 'FAU, Florida State', 'a lab-based programming '
             'course in the SAS language for managing and analysing data'],
        ]) +
        '<h3>Reading 1: Introductory Statistics II</h3>'
        '<p>USF describes it as hypothesis testing, inferences based on two samples, analysis of variance, linear and '
        'multiple regression, categorical data analysis and non-parametric statistics, with applications. UF titles '
        'it <em>Introduction to Statistics 2</em>, FAMU <em>Introduction to Probability and Statistics II</em> and '
        'Eastern Florida State <em>Statistics 2 for Data Scientists</em>. It follows STA 2023.</p>'
        '<h3>Reading 2: SAS for Data and Statistical Analyses</h3>'
        '<p>FAU and Florida State describe the same course in nearly the same words: an introduction to the '
        '<strong>SAS programming language</strong> in a lab-based format, developing programming and statistical '
        'computing skills for data management and analysis, with a survey of common statistical tools and strategies '
        'for choosing the right method. Florida State\'s outcomes add reading raw data from external files, subsets, '
        'if-then-else structures and loops, SAS functions, descriptive statistics with graphics, estimation and '
        'testing, and statistical modelling of qualitative and quantitative data.</p>'
        '<p>The two readings overlap in the statistical methods they reach, but one teaches the methods and the other '
        'teaches the software. A student who took one has not taken the other.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
        '<p><strong>Both readings:</strong></p>' + lg([
            'Choose an appropriate statistical method for a given question and type of data.',
            'Carry out and interpret two-sample comparisons, analysis of variance and regression.',
            'Analyse categorical data with chi-square methods.',
            'Report the results of an analysis clearly and with its assumptions stated.',
        ]) +
        '<p><strong>Reading 1, Introductory Statistics II (UF, USF, FAMU, Eastern Florida):</strong></p>' + lg([
            'Make inferences comparing two means and two proportions (independent and paired samples).',
            'Carry out one-way (and often two-way) ANOVA and multiple comparisons.',
            'Fit, test and check simple and multiple linear regression models, including residual analysis.',
            'Apply non-parametric tests when assumptions fail.',
        ]) +
        '<p><strong>Reading 2, SAS (FAU, Florida State):</strong></p>' + lg([
            'Read raw data from external files into SAS data sets; create subsets and new variables.',
            'Write SAS programs with conditional logic (if-then-else), loops, and numeric, character and probability '
            'functions.',
            'Produce descriptive statistics and graphics with SAS procedures.',
            'Run estimation, hypothesis tests and statistical models in SAS and interpret the output.',
        ]) + '<h3>Optional Outcomes</h3>' + lg([
            'Logistic regression or an introduction to experimental design (Statistics II).',
            'Macros, SQL in SAS (PROC SQL) and data reporting (SAS).',
            'Preparation for the SAS Certified Specialist: Base Programming exam (SAS).',
        ]) +
        '<h2>Major Topics</h2><h3>Required Topics</h3>'
        '<p><strong>Reading 1:</strong></p>' + lg([
            'Review of sampling distributions and hypothesis testing.',
            'Two-sample inference for means and proportions.',
            'Analysis of variance.',
            'Simple and multiple linear regression.',
            'Categorical data analysis; non-parametric statistics.',
        ]) +
        '<p><strong>Reading 2:</strong></p>' + lg([
            'The SAS environment; DATA step and PROC step.',
            'Reading, cleaning, combining and subsetting data.',
            'Programming structures and functions.',
            'Descriptive statistics and graphics (PROC MEANS, FREQ, SGPLOT).',
            'Inference and modelling procedures (PROC TTEST, ANOVA/GLM, REG, chi-square in FREQ).',
        ]) + '<h3>Optional Topics</h3>' + lg([
            'Logistic regression; design of experiments (Reading 1).',
            'SAS macros, PROC SQL, output delivery and reports (Reading 2).',
        ]) +
        '<h2>Resources &amp; Tools</h2>' + ul([
            'Reading 1: an applied statistics text (the syllabus names it), with R, Minitab, JMP or SPSS.',
            'Reading 2: SAS OnDemand for Academics (free for students and teachers through SAS Institute) or SAS '
            'Studio on campus; SAS\'s own documentation and the <em>Little SAS Book</em> are common references.',
        ]) +
        '<h2>Career Pathways</h2>' + ul([
            'Statistics, data science, actuarial science, economics, biology, public health and business analytics '
            'majors use it as their second statistics course (Reading 1).',
            'SAS remains common in pharmaceutical and clinical research, insurance, banking and government; SAS '
            'skills are asked for in statistical programmer and clinical SAS programmer jobs (Reading 2).',
            'Related occupations: statisticians (SOC 15-2041), data scientists (15-2051), operations research '
            'analysts (15-2031).',
        ]) +
        '<h2>Special Information</h2>'
        '<h3>One number, two subjects</h3><p>Florida\'s common course numbering is meant to make the same number '
        'mean the same course. Here it does not. A transfer evaluator matching on the number alone cannot tell the '
        'two apart, so a student moving from FAU or Florida State to UF or USF (or the other way) may receive credit '
        'for STA 3024 and still be missing the content the next course expects. If your next course needs Statistics '
        'II (regression, ANOVA) and you took the SAS course, or needs SAS and you took Statistics II, ask the '
        'department, and bring the syllabus.</p>'
        '<h3>Offering Notes</h3>' + table(['Institution', 'Title', 'Reading', 'Credits', 'Contact hours'], [
            ['Eastern Florida State College', 'Statistics 2 for Data Scientists', 'Statistics II', '3',
             'not published (45 derived)'],
            ['Florida A&amp;M University', 'Introduction to Probability and Statistics II', 'Statistics II', '3',
             'not published (45 derived)'],
            ['Florida Atlantic University', 'SAS for Data and Statistical Analyses', 'SAS', '3', '3 lecture a week (45)'],
            ['Florida State University', 'SAS for Data and Statistical Analysis', 'SAS', '3', '3 a week (45)'],
            ['University of Florida', 'Introduction to Statistics 2', 'Statistics II', '3', 'not published (45 derived)'],
            ['University of South Florida', 'Introductory Statistics II', 'Statistics II', '3',
             'not published (45 derived)'],
        ]) +
        '<p>All six carry it at 3 credits. Eastern Florida State College is a state college; its 3000-level '
        'courses belong to its bachelor\'s programmes.</p>'
        '<h3>Prerequisites</h3><p>FAU requires STA 2023 with a C or better. USF requires STA 2023 (C) and one of MAC '
        '2233, MAC 2241, MAC 2281 or MAC 2311 (C), or AP Calculus or AP Statistics with a score of 3. Check the '
        'others in their catalogues.</p>'
        + STAT_AI),
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
