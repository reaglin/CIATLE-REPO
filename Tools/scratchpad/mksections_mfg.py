#!/usr/bin/env python3
"""QUEUE.csv rows 162-165 (2026-10-02): add-section rows from the manufacturing gap analysis.

  162 industrial production manager (11-3051)        -> production-supervisor (+ CIP 52.02)
  163 tool and die maker (51-4111)                   -> machinist
  164 CNC programmer (51-9162)                       -> machinist
  165 occupational health and safety specialist (19-5011) -> industrial-engineer

Each section is inserted before the page's "Advice" heading. Idempotent: a section whose
marker is already present is not inserted twice.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PATHS = os.path.join(HERE, '..', 'career_paths')

SECTIONS = {
    'production-supervisor': {
        'marker': 'The rung above: industrial production manager',
        'html': """<h2>&#9888;&#9888; The rung above: industrial production manager</h2>
<p>A supervisor runs a shift or a line. An <strong>industrial production manager</strong> (11-3051) runs the plant's production as a whole: schedules, budgets, staffing, quality and output. BLS: <strong>$126,060 median</strong> (2025), <strong>252,100 jobs</strong>, growth <strong>3%</strong> for 2025&ndash;35, and <strong>about 17,000 openings a year</strong>.</p>
<p>&#9888;&#9888; <strong>This is the one rung where a degree becomes the expectation.</strong> BLS lists a <strong>bachelor's degree</strong> as the typical entry education, usually in business or engineering, plus <strong>five years or more</strong> of related experience. It describes two routes in: <em>&ldquo;Industrial production workers usually advance to supervisory or other leadership positions before eventually becoming industrial production managers,&rdquo;</em> while <em>&ldquo;those with a college degree might begin as a supervisor or lower-level manager.&rdquo;</em> So a supervisor without a degree can reach this job, but the bachelor's shortens the climb. The supervisory courses on this page, and an employer's tuition assistance, are how most people fill the gap.</p>
<table class="table">
<thead><tr><th>Industrial production managers, 2025</th><th>10th</th><th>25th</th><th>Median</th><th>75th</th><th>90th</th></tr></thead>
<tbody>
<tr><td>Florida</td><td>$66,250</td><td>$86,090</td><td>$119,870</td><td>$161,970</td><td>$212,910</td></tr>
<tr><td>United States</td><td>$78,000</td><td>$98,160</td><td>$126,060</td><td>$161,880</td><td>$205,520</td></tr>
</tbody>
</table>
<p>&#9888; <strong>In Florida the floor is lower and the ceiling is higher.</strong> The 10th percentile is about $11,750 below the national figure, and the 90th about $7,390 above it. Florida's large plants pay their top managers well, and smaller operations pay new managers less.</p>
<p>&#9888; <strong>Florida's most-awarded supervisory credential is short and specific.</strong> In 2023 Florida's public institutions awarded about 1,500 credentials in <em>operations management and supervision</em> (CIP 52.0205). Almost all were certificates, and 1,469 came from Valencia College. These are the supervision certificates working supervisors take while employed.</p>
""",
        'socs': ['11-3051'],
        'cips': [{"cipCode": "52.02", "note": "Business administration, management and operations. Florida awarded about 1,500 operations management and supervision credentials (52.0205) in 2023, almost all certificates, 1,469 of them at Valencia College; industrial production managers are typically expected to hold a business or engineering bachelor's (BLS)."}],
        'courses': [],
    },
    'machinist': {
        'marker': 'Tool and die maker and CNC programmer',
        'html': """<h2>&#9888;&#9888;&#9888; Tool and die maker and CNC programmer: the trade splits, and automation decides which way</h2>
<p>Two senior jobs grow out of machining, and federal projections point them in opposite directions:</p>
<table class="table">
<thead><tr><th></th><th>Tool and die maker (51-4111)</th><th>CNC tool programmer (51-9162)</th></tr></thead>
<tbody>
<tr><td>What it is</td><td>Builds the precision tools, jigs and <em>dies</em> that cut, shape and mould metal and plastic (BLS)</td><td>Writes the programs CNC machines run: choosing the operation sequence and cutting tools, computing tool paths, and proving the program on trial runs (O*NET)</td></tr>
<tr><td>Jobs</td><td>56,700 (BLS, 2025)</td><td>28,300 (O*NET, 2024)</td></tr>
<tr><td>Outlook</td><td>&#9888;&#9888; <strong>&minus;9%</strong>, 2025&ndash;35</td><td>&#9989;&#9989; <strong>much faster than average (7% or higher)</strong> to 2034; 3,100 openings a year</td></tr>
<tr><td>Median</td><td>$64,050 (2025)</td><td>$68,120 (2025); Florida $63,970</td></tr>
</tbody>
</table>
<p>BLS gives the reason in one sentence: <em>&ldquo;Employment of tool and die makers is expected to decline as advances in automation, including CNC machine tools, reduce demand for certain tasks.&rdquo;</em> &#9888;&#9888; <strong>The same technology that shrinks the hand-skill trade grows the job that programs it.</strong> On this site that pattern keeps recurring: automation reduces demand for the people who produce the routine work, and increases demand for the people who specify what the machine does.</p>
<p>&#9888; <strong>CNC programming is still mostly learned through work and short training.</strong> O*NET reports that 33% of CNC programmers hold a high school diploma, 31% a postsecondary certificate and 20% some college, and rates the job Job Zone 1&ndash;2. The usual route is machinist or setup operator first, then CAM software (programs that generate tool paths from a 3D model), then programming. Florida's state colleges teach that step for credit in their CNC courses, listed on this page.</p>
<p>Tool and die work is still skilled and well paid, and the people who do it are ageing, so there will be openings. But the trend is clear, and a student choosing where to put the next two years should aim at programming.</p>
""",
        'socs': ['51-4111', '51-9162'],
        'cips': [],
        'courses': [
            {"courseId": "ETI2414C", "reason": "Computer Numerical Control/Manufacturing (4 credits): CNC programming and CAM for credit. The step from running a CNC machine to programming one, which is the growing half of this trade.",
             "variantNote": "Eastern Florida and Pensacola carry ETI2414C, each with the follow-on ETI2419C Advanced Concepts of CNC Machines; College of Central Florida teaches ETI1414 and Polk ETI1414C at 3 credits."},
        ],
    },
    'industrial-engineer': {
        'marker': 'Occupational health and safety specialist',
        'html': """<h2>&#9888; A neighbouring career the same degree reaches: occupational health and safety specialist</h2>
<p>Industrial engineering is partly about designing work so people are not hurt doing it, and some graduates make that the whole job. <strong>Occupational health and safety specialists</strong> (19-5011) <em>&ldquo;inspect or evaluate workplace environments, equipment, or practices to ensure compliance with safety standards and government regulations,&rdquo;</em> <em>&ldquo;investigate accidents to identify causes,&rdquo;</em> and can <em>&ldquo;order suspension of activities that pose threats to workers' health or safety&rdquo;</em> (O*NET).</p>
<p>O*NET: <strong>131,900 employed</strong> (2024), growth <strong>&ldquo;much faster than average (7% or higher)&rdquo;</strong> to 2034, <strong>14,900 openings a year</strong>, median <strong>$90,150</strong> (2025). <strong>74%</strong> report that a bachelor's degree is required (Job Zone Four), and the top industries are <strong>government and manufacturing</strong>.</p>
<p>&#9888; <strong>Florida teaches it inside engineering, not as its own degree.</strong> Florida A&amp;M and Florida State carry <em>Occupational Safety and Hazard Control</em> (<code>EIN 4214</code>), and UF carries <em>Occupational Safety Engineering</em> (<code>EIN 4210C</code>). An industrial engineering student who takes one of them as an elective has the start of this career. The profession's main credential is the Certified Safety Professional (CSP) from the Board of Certified Safety Professionals, earned after the degree and work experience.</p>
""",
        'socs': ['19-5011'],
        'cips': [],
        'courses': [
            {"courseId": "EIN4214", "reason": "Occupational Safety and Hazard Control: the elective that turns an industrial engineering degree toward safety work, one of the fastest-growing neighbours of this career.",
             "variantNote": "Florida A&M and Florida State; UF teaches Occupational Safety Engineering as EIN4210C."},
        ],
    },
}


def main():
    for slug, s in SECTIONS.items():
        p = os.path.join(PATHS, slug + '.json')
        d = json.load(open(p, encoding='utf-8'))
        body = d['bodyHtml']
        if s['marker'] in body:
            print('%-24s section already present' % slug)
        else:
            i = body.find('<h2>Advice</h2>')
            if i < 0:
                raise SystemExit('%s: no <h2>Advice</h2> to insert before' % slug)
            d['bodyHtml'] = body[:i] + s['html'] + '\n' + body[i:]
        extra = d.get('additionalSocCodes') or []
        for soc in s['socs']:
            if soc not in extra:
                extra.append(soc)
        d['additionalSocCodes'] = extra
        cips = d.get('cipCodes') or []
        have = {c['cipCode'] for c in cips}
        for c in s['cips']:
            if c['cipCode'] not in have and c['cipCode'] != d.get('cipCode'):
                cips.append(c)
        d['cipCodes'] = cips
        ids = {c['courseId'] for c in d['courses']}
        for c in s['courses']:
            if c['courseId'] not in ids:
                d['courses'].append(c)
        json.dump(d, open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=2)
        print('%-24s socs=%s cips=%s courses=%d body=%d' % (slug, d['additionalSocCodes'],
              [c['cipCode'] for c in d['cipCodes']], len(d['courses']), len(d['bodyHtml'])))


if __name__ == '__main__':
    main()
