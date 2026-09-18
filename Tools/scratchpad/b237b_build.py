#!/usr/bin/env python
"""Batch 237b -- ESI3215, EIN3000, EIN3240.

⚠ ALL THREE ARE SINGLE-CARRIER COURSES, and they get the single-institution
treatment CLAUDE.md prescribes: explicit hedging, written as a custom guide for
that school, no pretence of statewide consensus.

⚠⚠ And the batch-227 rule applies to every one of them: where a course has ONE
carrier and the statewide description matches the carrier's closely, that is not
two sources agreeing -- it is one source quoted twice. The statewide entry was
almost certainly contributed by the only institution that teaches it. These
guides say so rather than claiming corroboration.

  ESI3215  FIU only (UF carries ESI3215C, 4 credits, a different packaging)
  EIN3000  FIU only -- and ONE credit, not three
  EIN3240  Florida Polytechnic only ⚠ whose catalogue is acalog and unreadable
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


def single(carrier, extra=''):
    return ('<h3>&#9888;&#9888; One institution carries this number</h3>'
            '<p>This course is offered by <strong>%s</strong> and by no other Florida public '
            'institution. Two things follow, and both matter more than they sound.</p>'
            '<p><strong>First, this guide describes that institution&rsquo;s course</strong>, not a '
            'statewide consensus, because there is no consensus to describe. <strong>Second, the '
            'statewide SCNS record was almost certainly written by the same institution</strong> '
            '&mdash; so where the two agree, that is one source quoted twice rather than '
            'independent corroboration. Nothing here should be read as more strongly established '
            'than a single department&rsquo;s practice.</p>'
            '<p>&#9888; <strong>On transfer, expect to send the syllabus.</strong> A receiving '
            'institution that does not offer the number has nothing to match against, so the '
            'decision will be made on content and hours.%s</p>' % (carrier, extra))


def guide(title, credits, hours, prereq, html, notes):
    return {'title': title, 'html_content': html, 'credits': credits, 'contact_hours': hours,
            'prerequisites': prereq, 'version': '1.0', 'offering_notes': notes}


G = {}

G['ESI3215'] = guide(
    'Evaluation of Engineering Data', 3, 45,
    'PREREQUISITE - AND THE SOURCES DISAGREE: the statewide SCNS record says MAC 2312 (Calculus II). '
    'FIU, the only institution carrying this number, states in its own catalogue "MAC 2311 or '
    'MAC 2281, or instructor permission" - Calculus I rather than Calculus II. Take the '
    'institution\'s own requirement as the operative one and confirm with an adviser. '
    'ONE CARRIER: FIU alone offers ESI3215, at 3 credits. UF carries a related course as ESI3215C '
    '(Data Analysis for Industrial Applications) at FOUR credits, which is a different packaging '
    'with an integrated laboratory component. No other Florida public institution carries either. '
    'This is the applied-statistics course that the quality control, simulation and operations '
    'research courses all assume, so treat it as load-bearing rather than as a survey.',
    '<h2>Course Description</h2>'
    '<p><strong>Evaluation of Engineering Data</strong> is the applied statistics course of an '
    'industrial engineering programme. The statewide description is brief &mdash; <em>&ldquo;analysis '
    'of industrial data and subsequent characterization of industrial processes&rdquo;</em> &mdash; '
    'and that brevity is itself informative: the course is defined by what it is <em>for</em> rather '
    'than by a topic list.</p>'
    '<p>What it is for is the rest of the degree. <strong>Quality control, simulation and operations '
    'research all assume that a student can fit a distribution, test a hypothesis and read a '
    'regression.</strong> This is where that happens, on industrial data rather than textbook data.</p>'
    '<p>&#9888; It is carried by <strong>FIU alone</strong> at 3 credits; UF carries '
    '<code>ESI3215C</code>, <em>Data Analysis for Industrial Applications</em>, at <strong>4 '
    'credits</strong>.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Summarise and visualise <strong>industrial data</strong>, and identify what the data collection can and cannot support.',
         'Fit and assess <strong>probability distributions</strong> to observed process data.',
         'Construct <strong>confidence intervals</strong> and carry out hypothesis tests on process parameters.',
         'Apply <strong>regression</strong> to model relationships between process variables.',
         'Use <strong>analysis of variance</strong> to attribute variation to its sources.',
         'Characterise a process statistically and state the limits of that characterisation.')
    + '<h3>Optional Outcomes</h3>'
    + li('Design of experiments as an introduction to the quality control course.',
         'Statistical software: Minitab, JMP, R or Python.',
         'Non-parametric methods where distributional assumptions fail.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Descriptive statistics and graphical methods for process data.',
         'Probability distributions common in engineering: normal, exponential, Weibull, Poisson, binomial.',
         'Sampling distributions and the Central Limit Theorem.',
         'Estimation and confidence intervals.', 'Hypothesis testing.',
         'Simple and multiple regression.', 'Analysis of variance.')
    + '<h3>Optional Topics</h3>'
    + li('Goodness-of-fit testing and distribution selection.',
         'Introduction to design of experiments.', 'Reliability data and censored observations.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Montgomery &amp; Runger, <em>Applied Statistics and Probability for Engineers</em>, is the '
    'standard text for this course across the discipline.</li>'
    '<li>Minitab, JMP, R or Python for the analysis. Check which your section uses.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Named on the <strong>Industrial Engineer</strong> career path. It is preparation rather than '
    'a destination &mdash; but it is the preparation that decides whether the quality, reliability '
    'and analytics work later in the degree is understood or merely performed.</p>'
    '<h2>Special Information</h2>'
    + single('Florida International University',
             ' UF&rsquo;s <code>ESI3215C</code> is the nearest equivalent and carries an extra credit.')
    + '<h3>&#9888;&#9888; The prerequisite is recorded differently by the state and by the carrier</h3>'
    '<p>The statewide record gives the prerequisite as <strong>MAC 2312</strong> (Calculus II). '
    'FIU&rsquo;s own catalogue gives it as <strong>MAC 2311 or MAC 2281, or instructor '
    'permission</strong> &mdash; Calculus I, or the business-calculus alternative.</p>'
    '<p><strong>Take the institution&rsquo;s own requirement as operative</strong>, since it is the '
    'institution that enforces registration. The discrepancy is worth knowing because a student '
    'planning from the state record would delay this course by a term for no reason.</p>'
    '<h3>Four credits at UF, three at FIU</h3>'
    '<p><code>ESI3215C</code> at UF carries <strong>4 credits</strong> against FIU&rsquo;s 3. The '
    '<code>C</code> indicates an integrated laboratory or computing component. &#9888; <strong>Check '
    'the credit value against your degree audit</strong> if you are moving between them &mdash; a '
    'one-credit difference in a tightly budgeted engineering programme surfaces at the final '
    'audit.</p>',
    {'summary': 'FIU alone carries ESI3215, at 3 credits. UF carries ESI3215C, Data Analysis for '
                'Industrial Applications, at 4 credits. No other Florida public institution carries '
                'either form.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at FIU’s 3-credit value. '
                   'UF’s 4-credit C form runs about 60.',
     'offerings': [
         {'institution': 'FIU', 'institution_name': 'Florida International University',
          'title': 'Evaluation of Engineering Data I', 'credits': 3, 'contact_hours': None,
          'note': 'Prerequisite in FIU’s own catalogue: MAC 2311 or MAC 2281, or instructor '
                  'permission — which differs from the statewide record’s MAC 2312.'},
         {'institution': 'UF', 'institution_name': 'University of Florida',
          'title': 'Data Analysis for Industrial Applications', 'credits': 4, 'contact_hours': None,
          'note': 'Carries the ESI3215C form at 4 credits.'}]})

G['EIN3000'] = guide(
    'Introduction to Industrial and Systems Engineering', 1, 15,
    'No prerequisite. '
    'NOTE THE CREDIT VALUE: this is a ONE-CREDIT course, not the three-credit survey the title might '
    'suggest. It is a short professional orientation - career planning, ethics, teamwork, industry '
    'site visits and guest speakers - with some introductory problem-solving method. It is not a '
    'technical survey of the discipline and does not substitute for one. '
    'ONE CARRIER: FIU alone offers this number. Several other Florida institutions run their own '
    'introduction to the discipline under different numbers, so if you are not at FIU, look for the '
    'equivalent in your own catalogue rather than for this number. '
    'WORTH TAKING EARLY: the site visits and speakers are the cheapest way to find out whether the '
    'field suits you, and that is more useful in the first year than in the third.',
    '<h2>Course Description</h2>'
    '<p><strong>Introduction to Industrial and Systems Engineering</strong> is a professional '
    'orientation course rather than a technical one. The statewide description lists <strong>an '
    'introduction to and overview of the profession, including career planning, professionalism and '
    'communication, ethics, teamwork, industry site visits, industrial speakers, and selected '
    'solution methods for problems in coordination and planning</strong>.</p>'
    '<p>&#9888;&#9888; <strong>It carries ONE credit.</strong> That is the most important thing to '
    'know about it: the title sounds like a survey of the discipline, and it is not. It is a short '
    'course designed to orient a new student to the profession and to the department.</p>'
    '<p>Carried by <strong>FIU alone</strong> among Florida public institutions.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Describe what <strong>industrial and systems engineers do</strong>, and the range of industries that employ them.',
         'Explain the <strong>ethical obligations</strong> of the engineering profession.',
         'Work effectively in a <strong>team</strong> and communicate technical ideas in writing and speech.',
         'Apply <strong>selected solution methods</strong> to introductory problems in coordination and planning.',
         'Plan a course of study and the first steps of a <strong>career</strong>, including internships.')
    + '<h3>Optional Outcomes</h3>'
    + li('Reflect on site visits and practitioner talks.',
         'Use introductory software the department expects later in the programme.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('The profession: history, scope, and the industries it serves.',
         'Professional ethics and responsibility.',
         'Communication and teamwork for engineers.',
         'Career planning, internships and the co-operative education route.',
         'Introductory problem-solving in coordination and planning.')
    + '<h3>Optional Topics</h3>'
    + li('Industry site visits.', 'Guest speakers from practice.',
         'Introduction to the professional society and student chapter.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Usually no textbook, or a short professional-orientation reader.</li>'
    '<li>&#9888; <strong>IISE</strong> &mdash; the Institute of Industrial and Systems Engineers '
    '&mdash; runs student chapters, and this course is the natural moment to join one. Student '
    'membership is inexpensive and is where internships often surface.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Named on the <strong>Industrial Engineer</strong> career path as the entry point. Its '
    'practical value is diagnostic: <strong>it is the cheapest honest test of whether the discipline '
    'suits you</strong>, taken at one credit in the first year rather than discovered at the third.</p>'
    '<h2>Special Information</h2>'
    + single('Florida International University')
    + '<h3>&#9888; One credit, and what that means for planning</h3>'
    '<p>A one-credit course carries roughly one contact hour a week. It will not move a full-time '
    'enrolment total much, and it is not a substitute for a technical survey course. <strong>Do not '
    'count it as a major technical requirement</strong> unless your own degree audit says so.</p>'
    '<h3>If you are not at FIU</h3>'
    '<p>Most Florida industrial engineering programmes run some form of introduction to the '
    'discipline, under their own numbers &mdash; the subject is common, the number is not. '
    '<strong>Search your catalogue by title rather than by this number.</strong></p>',
    {'summary': 'FIU alone carries EIN3000, at ONE credit. No other Florida public institution '
                'carries the number.',
     'hours_source': 'derived', 'derived_contact_hours': 15,
     'derivation': 'Florida convention of 15 contact hours per credit at 1 credit — about one '
                   'contact hour a week over a 15-week term.',
     'offerings': [
         {'institution': 'FIU', 'institution_name': 'Florida International University',
          'title': 'Introduction to Industrial and Systems Engineering', 'credits': 1,
          'contact_hours': None, 'note': 'The only Florida public carrier of this number.'}]})

G['EIN3240'] = guide(
    'Human Factors and Ergonomics', 3, 45,
    'No statewide prerequisite is recorded. '
    'ONE CARRIER: Florida Polytechnic University alone offers this number among Florida public '
    'institutions. Other programmes teach the subject under their own numbers, so search your '
    'catalogue by title rather than by this number if you are elsewhere. '
    'WHY IT MATTERS MORE THAN IT SOUNDS: this is the course that connects engineering design to the '
    'people who have to work inside it. Workplace injury, usability failures and the quiet '
    'resistance that kills a process improvement all trace back to designs that ignored the human. '
    'It also carries the OSHA and regulatory material that a manufacturing or warehouse employer '
    'will expect you to know. '
    'SOURCING NOTE: Florida Polytechnic publishes its catalogue on a platform this project cannot '
    'read, so this guide is written from the statewide SCNS record and from standard practice in the '
    'field. Confirm details against the institution\'s own catalogue.',
    '<h2>Course Description</h2>'
    '<p><strong>Human Factors and Ergonomics</strong> is the study of how people interact with the '
    'systems engineers design. The statewide description is unusually specific: <strong>human '
    'interaction with workspaces and process design, including anthropometry of tools and '
    'workspaces, human cognitive loading in process design, the basics of workplace health and '
    'safety including the role of regulatory agencies such as OSHA, and the process of analysis and '
    'improvement of the ergonomics of a workspace for both manufacturing and service sectors</strong>.</p>'
    '<p>&#9888; Note the last clause. <strong>This is not only a factory subject</strong> &mdash; the '
    'service sector is named explicitly, and in Florida that means hospitals, hotels, call centres, '
    'distribution and theme parks as much as it means manufacturing.</p>'
    '<p>Carried by <strong>Florida Polytechnic University alone</strong> at this number, 3 credits.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Apply <strong>anthropometric</strong> data to the design of tools, workstations and workspaces.',
         'Assess <strong>physical workload</strong> and identify risk factors for musculoskeletal injury.',
         'Analyse <strong>cognitive loading</strong> in process and interface design.',
         'Apply the basics of <strong>workplace health and safety</strong>, including the role of OSHA.',
         'Carry out an <strong>ergonomic analysis</strong> of a workspace and propose improvements.',
         'Justify design changes in terms a manager and a worker will both accept.')
    + '<h3>Optional Outcomes</h3>'
    + li('Use standard assessment instruments such as NIOSH lifting equation, RULA or REBA.',
         'Human-computer interaction and interface design.',
         'Accessibility and design for a range of physical abilities.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Anthropometry and workspace design.',
         'Biomechanics of work; manual handling and lifting.',
         'Cumulative trauma and musculoskeletal disorders.',
         'Cognitive ergonomics: attention, workload, error and display design.',
         'Workplace health and safety; OSHA and the regulatory framework.',
         'Ergonomic analysis and improvement method.')
    + '<h3>Optional Topics</h3>'
    + li('Environmental factors: noise, lighting, heat and vibration. &#9888; Heat stress is a '
         'live Florida concern in outdoor and un-conditioned work.',
         'Shift work and fatigue.', 'Human-computer interaction.',
         'Accessibility and universal design.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Standard texts include Chaffin, Andersson &amp; Martin, <em>Occupational Biomechanics</em>, '
    'and Salvendy&rsquo;s <em>Handbook of Human Factors and Ergonomics</em>.</li>'
    '<li>Assessment instruments: the NIOSH lifting equation, RULA and REBA.</li>'
    '<li><strong>OSHA</strong> publishes its ergonomics guidance and standards free, and they are '
    'the documents an employer will actually cite.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Named on the <strong>Industrial Engineer</strong> career path. It leads into ergonomics and '
    'safety roles, and it is directly useful in manufacturing, warehousing, healthcare and any '
    'operation with a workers-compensation exposure. &#9888; <strong>It is also the course that most '
    'often prevents a process improvement from failing</strong>: a change that ignores the people '
    'doing the work does not survive contact with them.</p>'
    '<h2>Special Information</h2>'
    + single('Florida Polytechnic University')
    + '<h3>&#9888; A sourcing limitation, stated plainly</h3>'
    '<p>Florida Polytechnic publishes its catalogue on a platform that does not serve course content '
    'to automated retrieval, so this guide is written from the statewide SCNS record and from '
    'standard practice in the field rather than from the institution&rsquo;s own text. <strong>It '
    'should be read as a description of the subject as Florida defines it</strong>, and confirmed '
    'against the catalogue before you rely on any detail.</p>'
    '<h3>Why a single Florida carrier is not a judgement on the subject</h3>'
    '<p>Human factors is a mature and required part of industrial engineering everywhere; ABET '
    'programmes cover it. That only one Florida institution uses <em>this number</em> reflects '
    'Florida&rsquo;s numbering practice, not the standing of the subject. <strong>Look for it under '
    'another number rather than concluding your programme omits it.</strong></p>',
    {'summary': 'Florida Polytechnic University alone carries EIN3240, at 3 credits. No other '
                'Florida public institution carries the number.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the 3-credit value.',
     'offerings': [
         {'institution': 'FLPOLY', 'institution_name': 'Florida Polytechnic University',
          'title': 'Human Factors and Ergonomics', 'credits': 3, 'contact_hours': None,
          'note': 'The only Florida public carrier. ⚠ Its catalogue platform is not readable by '
                  'this project, so per-institution detail could not be confirmed.'}]})


def main():
    os.makedirs(DRAFTS, exist_ok=True)
    for cid, g in G.items():
        io.open(os.path.join(DRAFTS, '%s_guide.json' % cid), 'w', encoding='utf-8').write(
            json.dumps(g, ensure_ascii=False, indent=1))
        print('%-9s %-44s %d cr / %2d hrs | prereq %4d | html %6d'
              % (cid, g['title'][:44], g['credits'], g['contact_hours'],
                 len(g['prerequisites']), len(g['html_content'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
