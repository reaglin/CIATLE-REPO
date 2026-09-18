#!/usr/bin/env python
"""Batch 237 -- the industrial engineering courses the Industrial Engineer path names.

Ron's rule (2026-09-17): a course that spans a major on a career path gets a
guide. These six are what the path needs after it was corrected.

⚠⚠⚠ THE CORRECTION THAT PRODUCED THIS BATCH. The path originally named FIU's
3000-level numbers for quality control and simulation. The flat file shows those
are the MINORITY forms:

    quality control   ESI4221 (FLPOLY, UCF, USF) + ESI4221C (UF, UNF) = 5
                      ESI3221 (FIU)                                   = 1
    simulation        ESI4523 (FAMU, FSU, UCF, UF, USF)               = 5
                      ESI3523 (FIU)                                   = 1

Same class of error as REVIEW_QUEUE item 106, caught before it was published
rather than after. The path now names the 4000-level forms and carries the
divergence as a variant note; these guides are written for the numbers most
students will actually see.

⚠⚠ AND A PREFIX-WIDE PATTERN: ESI splits by LEVEL across four subjects --
quality, simulation, operations research (ESI3312 vs ESI4312) and engineering
data (ESI3215 vs ESI3215C at 4 credits). This is the batch-207 number-
fragmentation shape running through one prefix, and the guides say so.
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


LEVEL_SPLIT = (
    '<h3>&#9888;&#9888; This prefix splits the same subject across two levels</h3>'
    '<p><code>ESI</code> numbers several subjects at both 3000 and 4000 level, and which one you see '
    'depends entirely on where you study:</p>'
    '<table class="table table-sm"><thead><tr><th>Subject</th><th>3000 level</th><th>4000 level</th>'
    '</tr></thead><tbody>'
    '<tr><td>Quality control</td><td><code>ESI3221</code> &mdash; FIU</td>'
    '<td><code>ESI4221</code> &mdash; Florida Poly, UCF, USF; <code>ESI4221C</code> &mdash; UF, UNF</td></tr>'
    '<tr><td>Simulation</td><td><code>ESI3523</code> &mdash; FIU</td>'
    '<td><code>ESI4523</code> &mdash; FAMU, FSU, UCF, UF, USF</td></tr>'
    '<tr><td>Deterministic operations research</td><td><code>ESI3312</code> &mdash; FIU, Florida Poly, UF</td>'
    '<td><code>ESI4312</code> &mdash; Daytona State, UCF, USF</td></tr>'
    '<tr><td>Engineering data analysis</td><td><code>ESI3215</code> &mdash; FIU; <code>ESI3215C</code> &mdash; UF</td>'
    '<td>&mdash;</td></tr>'
    '</tbody></table>'
    '<p>&#9888;&#9888; <strong>The level difference is not a difference in content, but it is a real '
    'transfer problem.</strong> A 2000-level course cannot supply upper-division hours toward a Florida '
    'baccalaureate; a 3000-level one can, so both forms here are safe on that count. What is not safe '
    'is assuming the numbers match: <strong>an evaluator matching on the identifier will see a '
    'mismatch where there is none.</strong> Send the syllabus, not the number.</p>')

ABET = (
    '<h3>Where this sits in an accredited programme</h3>'
    '<p>ABET-accredited industrial engineering programmes are required to cover the design, '
    'improvement and installation of integrated systems of people, materials, information, equipment '
    'and energy, drawing on the mathematical, physical and social sciences. <strong>This course is '
    'part of how a programme meets that requirement</strong>, which is why its content is fairly '
    'consistent even where the number is not.</p>'
    '<p>&#9888; For Professional Engineer licensure in Florida, what matters is that the degree is '
    'accredited under ABET&rsquo;s <em>Engineering</em> commission: s. 471.013(1)(a), Florida '
    'Statutes, requires four years of experience for an engineering curriculum and six for an '
    'engineering technology curriculum.</p>')


def guide(title, credits, hours, prereq, html, notes):
    return {'title': title, 'html_content': html, 'credits': credits, 'contact_hours': hours,
            'prerequisites': prereq, 'version': '1.0', 'offering_notes': notes}


G = {}

G['ESI4221'] = guide(
    'Industrial Quality Control', 3, 45,
    'Statewide prerequisite: STATISTICS. In practice an introductory statistics course is the floor '
    'and most programmes expect the engineering-statistics course as well, because this course uses '
    'sampling distributions, hypothesis testing and regression from the first weeks. '
    'REGISTER BY NUMBER, and check the level: Florida numbers this subject twice. ESI4221 is carried '
    'by Florida Polytechnic, UCF and USF; ESI4221C by UF and UNF (the C form carries a laboratory); '
    'and ESI3221, at 3000 level, by FIU alone. Same subject, five institutions on the 4000-level '
    'forms against one on the 3000-level. A transfer evaluator matching on the number alone will see '
    'a mismatch where there is none, so send the syllabus. '
    'This is the most directly employable single course in an industrial engineering degree for '
    'manufacturing work, and it maps onto the ASQ certifications employers recognise.',
    '<h2>Course Description</h2>'
    '<p><strong>Industrial Quality Control</strong> is the application of statistical technique to '
    'the control of industrial processes. The statewide description names the content directly: '
    '<strong>control charts, acceptance sampling, design of experiments, analysis of variance and '
    'regression</strong>.</p>'
    '<p>It is the course where the statistics an industrial engineer has been taking becomes the '
    'daily work of the job. &#9888; <strong>It is also the most immediately employable course in the '
    'degree for manufacturing</strong> &mdash; the vocabulary of control charts, capability indices '
    'and sampling plans is what a quality department actually speaks.</p>'
    '<p>Carried by <strong>five Florida public institutions across two numbers</strong> at 3 credits: '
    '<code>ESI4221</code> at Florida Polytechnic, UCF and USF, and <code>ESI4221C</code> at UF and '
    'UNF. FIU carries the same subject at <code>ESI3221</code>.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Construct and interpret <strong>control charts</strong> for variables and attributes, and distinguish common-cause from special-cause variation.',
         'Assess <strong>process capability</strong> and interpret capability indices against specification.',
         'Design and evaluate <strong>acceptance sampling</strong> plans, and state their risks to producer and consumer.',
         'Apply <strong>analysis of variance</strong> to identify sources of variation.',
         'Design and analyse simple <strong>experiments</strong>, including factorial designs.',
         'Apply <strong>regression</strong> to model and predict process behaviour.')
    + '<h3>Optional Outcomes</h3>'
    + li('Reliability analysis and life testing.',
         'Measurement system analysis (gauge repeatability and reproducibility).',
         'Six Sigma method and the DMAIC structure, where the institution frames the course that way.',
         'Laboratory exercises with real measurement data &mdash; the <code>C</code> form at UF and UNF includes these.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Variation, and the statistical basis of process control.',
         'Shewhart control charts for variables (X-bar, R, S) and for attributes (p, np, c, u).',
         'Process capability analysis.',
         'Acceptance sampling: single, double and sequential plans; operating characteristic curves.',
         'Analysis of variance.', 'Design of experiments; factorial and fractional factorial designs.',
         'Regression and correlation applied to process data.')
    + '<h3>Optional Topics</h3>'
    + li('Reliability and life-cycle testing.', 'Measurement system analysis.',
         'Total quality management, Six Sigma and lean method.',
         'ISO 9001 and industry-specific quality standards.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Montgomery, <em>Introduction to Statistical Quality Control</em>, is the near-universal text.</li>'
    '<li>Minitab, JMP, R or Python for the analysis; Excel for basic charting. Check which your '
    'section uses before buying anything.</li>'
    '<li>&#9888; <strong>ASQ</strong> (the American Society for Quality) publishes the bodies of '
    'knowledge for the Certified Quality Engineer and the Six Sigma belts. This course covers a '
    'substantial part of the CQE body of knowledge, and those certifications carry real weight with '
    'manufacturing employers.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Named on the <strong>Industrial Engineer</strong> career path in this repository. It leads '
    'directly to quality engineer, process engineer, reliability engineer and manufacturing '
    'engineering roles, and is the technical basis of the continuous-improvement function that now '
    'exists in Florida hospitals, distribution centres and service operations as well as in '
    'factories.</p>'
    '<h2>Special Information</h2>' + LEVEL_SPLIT
    + '<h3>The <code>C</code> form at UF and UNF</h3>'
    '<p><code>ESI4221C</code> carries an integrated laboratory: UF&rsquo;s catalogue describes '
    'laboratory exercises illustrating the techniques. <strong>The content is the same subject</strong>; '
    'the laboratory makes the measurement and charting hands-on. &#9888; Where a programme requires '
    'the laboratory component, the bare number will not substitute &mdash; check which your own '
    'catalogue lists.</p>' + ABET,
    {'summary': 'Five Florida public institutions carry this subject at 4000 level and 3 credits: '
                'ESI4221 at Florida Polytechnic, UCF and USF, and ESI4221C at UF and UNF. FIU '
                'carries the same subject as ESI3221. No institution publishes a contact-hour figure.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
     'offerings': [
         {'institution': 'UCF', 'institution_name': 'University of Central Florida',
          'title': 'Quality Engineering', 'credits': 3, 'contact_hours': None, 'note': None},
         {'institution': 'UF', 'institution_name': 'University of Florida',
          'title': 'Industrial Quality Control', 'credits': 3, 'contact_hours': None,
          'note': 'Carries the ESI4221C form, with laboratory exercises illustrating the techniques.'}]})

G['ESI4523'] = guide(
    'Industrial Systems Simulation', 3, 45,
    'No statewide prerequisite is recorded, but in practice programmes require probability and '
    'statistics first: simulation is applied probability, and a student without distributions and '
    'confidence intervals cannot interpret the output. Many programmes also expect programming. '
    'REGISTER BY NUMBER: ESI4523 is carried by FAMU, FSU, UCF, UF and USF at 3 credits; FIU carries '
    'the same subject as ESI3523. Five institutions on the 4000-level number against one on the '
    '3000-level. '
    'ASK WHICH SOFTWARE: the statewide description and several catalogues still name GPSS, a '
    'simulation language first released in 1961. Current Florida practice uses Arena, Simio, '
    'AnyLogic, FlexSim or Python SimPy. The method is what transfers; the package is what you will '
    'be asked about in an interview, so find out which one your section teaches.',
    '<h2>Course Description</h2>'
    '<p><strong>Industrial Systems Simulation</strong> teaches how to model a system you cannot '
    'experiment on. The statewide description covers <strong>simulation methodology and languages, '
    'the design and analysis of simulation experiments, and applications to industrial and service '
    'system problems</strong>.</p>'
    '<p>That last phrase is the reason the course matters: you rarely get to rearrange a live '
    'factory, hospital or airport to see what happens. <strong>A simulation model is how a proposal '
    'gets tested before anyone spends money</strong>, and building one credibly is among the most '
    'marketable things an industrial engineering graduate can do.</p>'
    '<p>Carried by <strong>five Florida public institutions</strong> &mdash; FAMU, Florida State, '
    'UCF, UF and USF &mdash; at 3 credits, with FIU carrying the subject as <code>ESI3523</code>.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Formulate a <strong>discrete-event simulation model</strong> of an industrial or service system.',
         'Select and fit <strong>input probability distributions</strong> from observed data.',
         'Implement a model in a simulation package and <strong>verify and validate</strong> it.',
         'Design simulation <strong>experiments</strong>: run length, warm-up, replications, variance reduction.',
         'Analyse output <strong>statistically</strong>, with confidence intervals rather than single runs.',
         'Compare alternative system configurations and make a defensible recommendation.')
    + '<h3>Optional Outcomes</h3>'
    + li('Optimisation via simulation.', 'Agent-based or continuous simulation alongside discrete-event.',
         'Animation and visualisation for presenting results to non-technical decision-makers.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Systems, models and the discrete-event world view.',
         'Random number and random variate generation.',
         'Input modelling: distribution fitting and goodness of fit.',
         'Model building in a simulation package.',
         'Verification and validation.',
         'Output analysis: terminating versus steady-state, replication, confidence intervals.',
         'Comparing alternative designs.')
    + '<h3>Optional Topics</h3>'
    + li('Variance reduction techniques.', 'Simulation optimisation.',
         'Queueing theory as the analytical counterpart to simulation.',
         'Agent-based and hybrid models.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Banks, Carson, Nelson &amp; Nicol, <em>Discrete-Event System Simulation</em>, and Law, '
    '<em>Simulation Modeling and Analysis</em>, are the standard texts.</li>'
    '<li>&#9888;&#9888; <strong>Software varies and the catalogues are out of date about it.</strong> '
    'The statewide description and several institutional entries still name <strong>GPSS</strong>, a '
    'language first released in 1961. What Florida programmes actually teach is Arena, Simio, '
    'AnyLogic, FlexSim or Python&rsquo;s SimPy. <strong>Ask before the term starts</strong> &mdash; '
    'some packages need a student licence and a machine that will run it.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Named on the <strong>Industrial Engineer</strong> career path. Simulation skill is sought in '
    'manufacturing and logistics, and in Florida particularly in <strong>theme-park and attraction '
    'operations</strong> (queueing and throughput at very large scale), <strong>port and cruise '
    'logistics</strong>, distribution along the I-4 corridor, and hospital patient-flow work. It is '
    'also a common route into operations research and analytics roles.</p>'
    '<h2>Special Information</h2>' + LEVEL_SPLIT
    + '<h3>&#9888; The dated tooling is a tell worth reading</h3>'
    '<p>When a course description names a specific product, check whether the product is current. '
    'Here both the statewide record and institutional catalogues carry GPSS forward, which tells you '
    'the <em>description</em> has not been revised &mdash; not that the teaching has not. '
    '<strong>Judge the course by the syllabus issued in week one, not by the catalogue.</strong> The '
    'simulation <em>method</em> is stable and transfers; only the package changes.</p>' + ABET,
    {'summary': 'Five Florida public institutions carry ESI4523 at 3 credits: FAMU, Florida State, '
                'UCF, UF and USF. FIU carries the same subject as ESI3523. No institution publishes '
                'a contact-hour figure.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
     'offerings': [
         {'institution': 'UF', 'institution_name': 'University of Florida',
          'title': 'Industrial Systems Simulation', 'credits': 3, 'contact_hours': None,
          'note': 'Catalogue description still names GPSS as the simulation language.'},
         {'institution': 'FSU', 'institution_name': 'Florida State University',
          'title': 'Simulation of Industrial Engineering Systems', 'credits': 3,
          'contact_hours': None, 'note': None}]})

G['ESI3312'] = guide(
    'Deterministic Operations Research', 3, 45,
    'No statewide prerequisite is recorded; in practice programmes require calculus and normally '
    'linear algebra, because the simplex method is linear algebra in applied form. '
    'REGISTER BY NUMBER: ESI3312 is carried by FIU, Florida Polytechnic and UF; the same subject is '
    'numbered ESI4312 at Daytona State, UCF and USF. Three institutions on each. Neither is the '
    '"right" number - register by what YOUR catalogue prints and send a syllabus on transfer. '
    'NOTE FOR READERS OF THE STATE RECORD: the statewide description contains a typographical error, '
    'listing "SUALITY" where it means DUALITY - the dual formulation of a linear program, which is a '
    'core topic and not a course nobody teaches.',
    '<h2>Course Description</h2>'
    '<p><strong>Deterministic Operations Research</strong> is the optimisation half of industrial '
    'engineering: finding the best decision when the relationships are known and the difficulty is '
    'scale rather than uncertainty. The statewide description lists <strong>classical optimisation '
    'by Lagrange multipliers, Kuhn-Tucker conditions, linear programming, the simplex algorithm, '
    'sensitivity analysis, duality, transportation and assignment problems, network flows and '
    'integer programming</strong>.</p>'
    '<p>Carried by <strong>three Florida public institutions</strong> at this number &mdash; FIU, '
    'Florida Polytechnic and UF &mdash; and by three more as <code>ESI4312</code>.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Formulate a decision problem as a <strong>linear program</strong>, identifying variables, objective and constraints.',
         'Solve linear programs using the <strong>simplex algorithm</strong> and interpret each step.',
         'Interpret the <strong>dual</strong> and use shadow prices to value a constraint.',
         'Carry out <strong>sensitivity analysis</strong> and state how far a solution can be trusted.',
         'Model and solve <strong>transportation, assignment and network flow</strong> problems.',
         'Formulate and solve <strong>integer programming</strong> problems, and explain why integrality is hard.')
    + '<h3>Optional Outcomes</h3>'
    + li('Non-linear optimisation with Lagrange multipliers and Kuhn-Tucker conditions.',
         'Dynamic programming.', 'Use of a solver: Gurobi, CPLEX, Excel Solver or Python PuLP.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Linear programming formulation and geometry.', 'The simplex method.',
         'Duality and sensitivity analysis.', 'Transportation and assignment problems.',
         'Network models: shortest path, maximum flow, minimum spanning tree.',
         'Integer and mixed-integer programming; branch and bound.')
    + '<h3>Optional Topics</h3>'
    + li('Classical constrained optimisation; Lagrange multipliers and Kuhn-Tucker conditions.',
         'Dynamic programming.', 'Goal and multi-objective programming.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Hillier &amp; Lieberman, <em>Introduction to Operations Research</em>, and Winston, '
    '<em>Operations Research</em>, are the standard texts.</li>'
    '<li>A solver is normally part of the course: Excel Solver for small problems, then Gurobi, '
    'CPLEX, AMPL or Python (PuLP, Pyomo). Academic licences are usually free &mdash; ask early.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Named on the <strong>Industrial Engineer</strong> career path. Optimisation is the technical '
    'core of supply-chain planning, scheduling, routing, network design and revenue management, and '
    'it is one of the clearest bridges from industrial engineering into analytics and data science '
    'roles.</p>'
    '<h2>Special Information</h2>' + LEVEL_SPLIT
    + '<h3>&#9888; A typographical error in the state record</h3>'
    '<p>The statewide description lists <em>&ldquo;SUALITY&rdquo;</em> among the topics. It means '
    '<strong>DUALITY</strong> &mdash; the dual formulation of a linear program, and one of the most '
    'important ideas in the course. It is recorded here only so that a reader searching the state '
    'record is not misled by it.</p>'
    '<h3>Deterministic, and what that excludes</h3>'
    '<p>&ldquo;Deterministic&rdquo; means the data is treated as known. The companion course &mdash; '
    'usually called stochastic operations research or probabilistic models &mdash; handles '
    'uncertainty: queueing, Markov chains, inventory under random demand. <strong>Most programmes '
    'require both</strong>, and a student who has taken only this one should say so rather than '
    'claiming operations research generally.</p>' + ABET,
    {'summary': 'Three Florida public institutions carry ESI3312 at 3 credits (FIU, Florida '
                'Polytechnic, UF) and three carry the same subject as ESI4312 (Daytona State, UCF, '
                'USF). Institution titles vary: Deterministic Operations Research, Operations '
                'Research 1, Operations Research I: Deterministic Models.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the uniform 3-credit value.',
     'offerings': [
         {'institution': 'UF', 'institution_name': 'University of Florida',
          'title': 'Operations Research I: Deterministic Models', 'credits': 3,
          'contact_hours': None, 'note': None},
         {'institution': 'FIU', 'institution_name': 'Florida International University',
          'title': 'Deterministic Operations Research', 'credits': 3, 'contact_hours': None,
          'note': None}]})


def main():
    os.makedirs(DRAFTS, exist_ok=True)
    for cid, g in G.items():
        io.open(os.path.join(DRAFTS, '%s_guide.json' % cid), 'w', encoding='utf-8').write(
            json.dumps(g, ensure_ascii=False, indent=1))
        print('%-9s %-34s %d cr / %d hrs | prereq %4d | html %6d'
              % (cid, g['title'][:34], g['credits'], g['contact_hours'],
                 len(g['prerequisites']), len(g['html_content'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
