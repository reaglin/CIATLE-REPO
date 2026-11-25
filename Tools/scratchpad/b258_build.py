# -*- coding: utf-8 -*-
"""Batch 258: BME4057C Biomedical Engineering Lab II (USF only).

    python scratchpad/b258_build.py      (run from Tools/)

Sources (fetched 2026-11-25, scratchpad/b258_fetch.py):
  cloud.usf.edu/academic-programs/details/prefix/BME/code/4057C  description, 2 credits, prerequisites
  .../4056C (Lab I), .../3312, .../4232, .../3632                the chain around it
  www.usf.edu/engineering/bme/                                    the department (Medical Engineering)
  ocw.mit.edu/courses/20-109-...-spring-2010/                     a similar course outside Florida
SCNS flat file: USF is the only carrier (carriers.py BME4057C).
"""
import io
import json

CID = 'BME4057C'
USF = 'https://cloud.usf.edu/academic-programs/details/prefix/BME/code/%s'


def li(items):
    return '<ul class="list-group list-group-flush">%s</ul>' % ''.join(
        '<li class="list-group-item">%s</li>' % i for i in items)


html = (
    '<h2>Course Description</h2>'
    '<div class="alert alert-warning"><strong>Limited information.</strong> Only the <em>University of South '
    'Florida</em> offers BME4057C in Florida\'s public colleges and universities, and it publishes a one-sentence '
    'description. This guide sets out what the record shows and what a laboratory course of this kind commonly '
    'covers. Check USF\'s syllabus before relying on it.</div>'
    '<p><strong>BME4057C Biomedical Engineering Lab II</strong> is the second of USF\'s two required senior '
    'laboratory courses in biomedical engineering (Department of Medical Engineering, College of Engineering). '
    'USF describes it as:</p>'
    '<blockquote class="blockquote"><p><em>"Experimental design, testing and analysis of molecular, cellular and '
    'tissue engineering systems, including biomaterials, biomechanics and fluid transport in biological '
    'systems."</em></p></blockquote>'
    '<p>It carries <strong>2 credits</strong>, is open to <strong>majors only</strong> and needs a '
    '<strong>permit</strong>. The "C" suffix means lecture and laboratory are taught together. Its partner, '
    '<a href="/courses/BME4056C">BME4056C Biomedical Engineering Lab I</a>, covers the other half of the field: '
    'biomedical instrumentation and physiological measurement (cardiovascular, respiratory, nervous and muscular '
    'systems). Lab II turns from signals to materials, cells, tissues, forces and flow, so it draws on the three '
    'lecture courses that come before it: molecular and cellular engineering, biomechanics and biomedical '
    'transport.</p>'
    '<h2>Learning Outcomes</h2>'
    '<h3>Required Outcomes</h3>' + li([
        'Design an experiment on a molecular, cellular or tissue engineering system: state the question, choose '
        'controls and replicates, and identify the variables to measure.',
        'Carry out tests on biomaterials and biological tissues and record the results accurately.',
        'Measure the mechanical behaviour of a material or tissue and relate the result to biomechanics theory.',
        'Measure or model fluid transport in a biological system and compare the result with transport theory.',
        'Analyse experimental data with appropriate statistics, including uncertainty, and draw conclusions the '
        'data support.',
    ]) +
    '<h3>Optional Outcomes</h3>'
    '<p>What a senior biomedical engineering laboratory of this kind <em>commonly</em> adds; USF\'s exact '
    'experiments are not published.</p>' + li([
        'Use sterile technique and culture mammalian cells; assess viability, attachment or proliferation on a '
        'material.',
        'Characterise a biomaterial or scaffold (for example its stiffness, degradation, swelling or surface '
        'properties).',
        'Use common bench assays such as spectrophotometry, fluorescence microscopy or protein and DNA '
        'quantification.',
        'Write technical laboratory reports and present results orally, working in a team.',
        'Follow laboratory safety and biosafety rules for biological materials.',
    ]) +
    '<h2>Major Topics</h2>'
    '<h3>Required Topics</h3>' + li([
        'Experimental design, testing and analysis (USF\'s description).',
        'Molecular and cellular engineering systems.',
        'Tissue engineering systems.',
        'Biomaterials.',
        'Biomechanics: mechanical testing and characterisation.',
        'Fluid transport in biological systems.',
    ]) +
    '<h3>Optional Topics</h3>' + li([
        'Cell culture and cell&ndash;material interaction.',
        'Stress&ndash;strain testing of soft and hard tissues or polymers; viscoelasticity.',
        'Diffusion and flow experiments; comparing measured profiles with one-dimensional transport models.',
        'Statistics for laboratory data: replicates, error propagation, hypothesis tests.',
        'Technical writing and the laboratory notebook.',
    ]) +
    '<h2>Resources &amp; Tools</h2>'
    '<ul><li>USF\'s instructional laboratory (the department\'s <em>BME Instructional Lab</em>); the equipment '
    'and experiments are set by the department.</li>'
    '<li>Texts from the prerequisite courses in biomechanics, biomedical transport and molecular and cellular '
    'engineering; a biomaterials text such as Ratner et al., <em>Biomaterials Science</em>. Check the '
    'syllabus.</li>'
    '<li>Data analysis software (MATLAB, Python or a statistics package) and a spreadsheet.</li>'
    '<li>Biomedical Engineering Society (BMES).</li></ul>'
    '<h2>Career Pathways</h2>'
    '<ul><li>Bioengineers and biomedical engineers (SOC 17-2031).</li>'
    '<li>Laboratory and research roles in medical devices, biomaterials, tissue engineering and biotechnology; '
    'medical scientists (19-1042) usually after graduate study; medical school.</li>'
    '<li>Tampa Bay has a medical device and life-science sector, and USF Health and the Moffitt Cancer Center '
    'are nearby research employers.</li></ul>'
    '<h2>Where to Learn More</h2>'
    '<ul><li><a href="' + USF % '4057C' + '">USF\'s course record for BME 4057C</a> (description, credits, '
    'prerequisites).</li>'
    '<li><a href="https://www.usf.edu/engineering/bme/">USF Department of Medical Engineering</a>: curriculum, '
    'advising and the BME Instructional Lab.</li>'
    '<li>The same subject in Florida on this site: <a href="/courses/BME4056C">BME4056C Biomedical Engineering '
    'Lab I</a> (its partner), <a href="/courses/BME3100">BME3100 Biomaterials</a>, '
    '<a href="/courses/BME4503">BME4503 Biomedical Instrumentation</a>.</li>'
    '<li><a href="https://ocw.mit.edu/courses/20-109-laboratory-fundamentals-in-biological-engineering-spring-2010/">'
    'MIT OpenCourseWare 20.109, Laboratory Fundamentals in Biological Engineering</a>: free materials for an '
    'engineering laboratory course on experimental design, data analysis and cell&ndash;biomaterial engineering. '
    'A similar course, not an equivalent for transfer.</li></ul>'
    '<h2>Special Information</h2>'
    '<h3>Offering Notes</h3>'
    '<table class="table table-sm table-bordered"><thead><tr><th>University</th><th>Title</th><th>Credits</th>'
    '</tr></thead><tbody><tr><td>USF</td><td>Biomedical Engineering Lab II</td><td>2</td></tr></tbody></table>'
    '<p><strong>USF is the only carrier, at 2 credits.</strong> USF does not publish contact hours; the 30 '
    'shown are derived from Florida\'s convention of 15 per credit. A laboratory course usually meets for more '
    'clock hours than its credits suggest, so check the schedule.</p>'
    '<h3>Prerequisites at USF</h3>'
    '<p>A C or better in <strong>BME 3312</strong> Molecular and Cellular Engineering, <strong>BME 4056C</strong> '
    'Biomedical Engineering Lab I and <strong>BME 4232</strong> Biomechanics, and <strong>BME 3632</strong> '
    'Biomedical Transport Process (C or better) before or at the same time. Majors only; a departmental permit is '
    'required.</p>'
    '<h3>Transfer</h3>'
    '<p>No other Florida public institution carries BME4057C. A student arriving from another biomedical '
    'engineering programme with a senior laboratory should ask USF\'s department to evaluate it; keep the '
    'syllabus and lab reports.</p>'
    '<h2>AI Integration (Optional)</h2>'
    '<p>AI tools can help plan an experiment, write analysis code or check a statistical test, but they cannot '
    'see the bench. Generated code must be checked against the data it reads, and a tool asked to "explain" an '
    'odd result will often supply a confident reason that was never tested. Record what was actually done in the '
    'notebook, write the conclusions from the data, and follow the instructor\'s policy on AI in lab reports.</p>'
)

guide = {
    'title': 'Biomedical Engineering Lab II',
    'html_content': html,
    'credits': 2,
    'contact_hours': 30,
    'prerequisites': (
        'USF (the only carrier): BME 3312 Molecular and Cellular Engineering, BME 4056C Biomedical Engineering '
        'Lab I and BME 4232 Biomechanics, each with a minimum grade of C; BME 3632 Biomedical Transport Process '
        '(minimum grade C) as a co-prerequisite. Majors only; departmental permit required.'),
    'version': '1.0',
    'offering_notes': {
        'summary': 'Only USF carries BME4057C, at 2 credits; its partner is BME4056C Biomedical Engineering Lab I.',
        'hours_source': 'derived',
        'derived_contact_hours': 30,
        'derivation': "Florida's convention of 15 contact hours per credit; USF publishes no contact-hour figure.",
        'offerings': [{
            'institution': 'USF',
            'institution_name': 'University of South Florida',
            'title': 'Biomedical Engineering Lab II',
            'credits': 2,
            'contact_hours': None,
            'note': 'Majors only, permit required. Prerequisites BME 3312, BME 4056C, BME 4232; co-requisite BME 3632.',
        }],
    },
}

with io.open('drafts/%s_guide.json' % CID, 'w', encoding='utf-8') as f:
    json.dump(guide, f, ensure_ascii=False, indent=2)
print(CID, len(html), len(guide['prerequisites']))
