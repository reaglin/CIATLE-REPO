#!/usr/bin/env python3
"""Row 157 of career_paths/QUEUE.csv (2026-10-02): Semiconductor Technician.

From the manufacturing gap analysis Ron approved on 2026-10-02. Written as a pair with
production-technician (row 155), which shares CIP 15.06.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'career_paths', 'semiconductor-technician.json')

body = """<h2>What the work actually is</h2>
<p>Semiconductor technicians make microchips and the components around them. The work happens inside a <strong>cleanroom</strong>, a room where particles in the air are counted and controlled, and where everyone wears a full-body gown. O*NET's task list describes the job: <em>&ldquo;clean semiconductor wafers using cleaning equipment&rdquo;</em>; <em>&ldquo;place semiconductor wafers in processing containers or equipment holders&rdquo;</em>; <em>&ldquo;manipulate valves, switches, and buttons to start semiconductor processing cycles&rdquo;</em>; <em>&ldquo;inspect materials, components, or products for surface defects and measure circuitry&rdquo;</em>; and <em>&ldquo;inspect equipment for leaks, diagnose malfunctions, and request repairs.&rdquo;</em></p>
<p>The process steps have names a student will meet in the courses: <strong>photolithography</strong> (printing a pattern onto the wafer with light), <strong>etching</strong> (often with plasma), <strong>deposition</strong> in vacuum chambers, and <strong>packaging</strong> (turning a finished die into a part that can go on a circuit board). O*NET's sample job titles include <em>Wafer Fabrication Operator, Diffusion Operator, Probe Operator, Process Technician</em> and <em>Manufacturing Technician</em>.</p>

<h2>Projected need</h2>
<p>O*NET, for semiconductor processing technicians (51-9141): <strong>31,900 employed</strong> (2024), growth <strong>&ldquo;much faster than average (7% or higher)&rdquo;</strong> to 2034, <strong>3,900 openings a year</strong>, and a national median of <strong>$51,430</strong> (2025). &#9888; It is a small occupation, but it is growing fast, because of national investment in domestic chip production since the 2022 CHIPS and Science Act.</p>

<h2>&#9888;&#9888;&#9888; Florida pays more than the national rate</h2>
<table class="table">
<thead><tr><th>Semiconductor processing technicians, 2025</th><th>10th</th><th>25th</th><th>Median</th><th>75th</th><th>90th</th></tr></thead>
<tbody>
<tr><td>Florida</td><td>$39,980</td><td>$49,950</td><td><strong>$62,330</strong></td><td>$67,370</td><td>$80,390</td></tr>
<tr><td>United States</td><td>$37,690</td><td>$45,640</td><td>$51,430</td><td>$65,010</td><td>$82,540</td></tr>
<tr><td>Difference</td><td>+$2,290</td><td>+$4,310</td><td>&#9989; <strong>+$10,900</strong></td><td>+$2,360</td><td>&minus;$2,150</td></tr>
</tbody>
</table>
<p>&#9888; <strong>Florida's median is almost $11,000 above the national figure, and its floor is higher too.</strong> On most technical occupations Florida pays less than the national rate. Only the 90th percentile here falls slightly below. For comparison, Florida pays general assemblers <em>below</em> the national median (see the Production Technician path); moving from the assembly line into the cleanroom is one of the clearest raises in Florida manufacturing.</p>

<h2>&#9888;&#9888; Most people in this job hold only a high school diploma. What is the college for?</h2>
<p>O*NET reports that <strong>84%</strong> of semiconductor processing technicians have a high school diploma, <strong>12%</strong> less than that, and only <strong>2%</strong> an associate degree; it rates the job <strong>Job Zone 1&ndash;2</strong> (little to some preparation). Fabs have long trained operators on the job. So why take Florida's college programmes?</p>
<ul>
<li><strong>To be hired in Florida at all.</strong> Florida has few fabs, and the employers that exist helped design the local programmes. Valencia College names <strong>SkyWater Technology, Lockheed Martin, Draper and L3Harris</strong> as partners shaping its curriculum.</li>
<li><strong>To start on the technician side rather than the operator side.</strong> An operator loads and runs the tools; a technician keeps them running and works out why a process drifted. That is the pay difference inside the table above, and it is what the degree courses (vacuum systems, plasma, devices and circuits) are for.</li>
<li><strong>To keep the bachelor's route open.</strong> See the next section.</li>
</ul>

<h2>&#9888;&#9888; Florida's programmes: a short certificate inside a demanding degree</h2>
<p>Florida's career frameworks define two programmes, both filed under CIP 15.0616:</p>
<ul>
<li><strong>Semiconductor Cleanroom Operator</strong>, a college credit certificate of <strong>18 credits</strong>: <em>&ldquo;electrical and digital circuits, installation and programming of robotic systems and silicon and wafer fabrication to include photolithography, plasma etching and advanced packaging.&rdquo;</em> At Valencia it can be finished in a year or less, and is open to high school dual-enrollment students.</li>
<li><strong>Semiconductor Engineering Technology</strong>, a <strong>60-credit A.S.</strong> that contains the certificate. Valencia describes itself as the first Florida college to offer it.</li>
</ul>
<p>&#9888;&#9888;&#9888; <strong>Read the A.S. requirements before you start.</strong> Valencia's degree requires <strong>Calculus I and II</strong> (<code>MAC 2311</code>, <code>MAC 2312</code>) and <strong>calculus-based physics</strong> (<code>PHY 2048C</code>), which few career A.S. degrees ask for. That is a real hurdle, and also an advantage: a graduate has the mathematics an engineering bachelor's degree expects, so this A.S. can lead on to one instead of ending there. The certificate asks only for <em>Mathematics for Engineering Technology</em>, so a student who is not ready for calculus can start there and still be hired.</p>
<p>&#9888; <strong>The programmes are new and spreading.</strong> In the statewide course file, Valencia carries the most semiconductor courses (cleanroom operation, vacuum systems, fabrication, packaging). <strong>Miami Dade</strong> adds lithography and plasma courses for its own semiconductor programme. <strong>St. Petersburg College</strong> added a Cleanroom Operator certificate through its state-funded SMART Tech programmes. <strong>Tallahassee State</strong> carries the fundamentals course. The 2023 federal completions data predates all of them, so the programme pages on this site do not list them by name yet.</p>

<h2>What the cleanroom asks of you</h2>
<ul>
<li><strong>Gowning and contamination discipline.</strong> Full-body suits, strict entry procedures, and no cosmetics or loose particles. A single careless step can scrap a batch of wafers.</li>
<li><strong>Shift work.</strong> Fabs run around the clock, and many use long rotating shifts. Ask an employer for its schedule before you assume a nine-to-five job.</li>
<li><strong>Chemical and gas safety.</strong> The processes use hazardous chemicals and gases, handled under strict procedures.</li>
<li><strong>Attention to procedure and data.</strong> The work is precise and repetitive, and you will log measurements and catch the moment a process starts to drift.</li>
</ul>

<h2>Necessary skills</h2>
<ul>
<li><strong>Basic electronics</strong>: circuits, digital systems, and how a semiconductor device works.</li>
<li><strong>Vacuum, plasma and process equipment</strong>: what the tools do, and how to tell when they are not doing it.</li>
<li><strong>Measurement and inspection</strong>, including microscopes and metrology tools.</li>
<li><strong>Robotics and automation</strong>. Fabs move wafers by robot, and the framework includes robotic systems.</li>
<li><strong>Mathematics</strong>: algebra and engineering-technology maths for the certificate, calculus for the degree.</li>
</ul>

<h2>Advice</h2>
<ul>
<li><strong>Start with the 18-credit certificate</strong> if you need to work soon; it stacks into the degree, so nothing is lost.</li>
<li><strong>Begin the maths early</strong> if you want the A.S. Calculus I and II are the courses most likely to slow you down, and they also open the door to an engineering bachelor's.</li>
<li><strong>Ask a programme which employers hire its completers</strong>, and whether internships are arranged with them. In a field this small, those relationships are the main thing a programme can offer.</li>
<li><strong>If you are coming from assembly or production work</strong>, the cleanroom is a natural next step. Valencia gives transfer credit for its short Accelerated Skills Training in robotics and semiconductors (9 credits toward the degree).</li>
<li><strong>For the design and engineering side</strong>, look at electrical, computer or materials engineering. UCF teaches <em>Principles of Semiconductor Manufacturing</em> (<code>EMA 4411</code>), and several universities teach semiconductor device courses.</li>
</ul>"""

doc = {
    "slug": "semiconductor-technician",
    "name": "Semiconductor Technician",
    "cipCode": "15.06",
    "socCode": "51-9141",
    "isPublished": True,
    "sortOrder": 195,
    "description": "Semiconductor technicians make microchips: they work in cleanrooms, running and maintaining the tools that pattern, etch, deposit and package silicon. ⚠ A small occupation growing much faster than average, and Florida pays it almost $11,000 above the national median. Florida's programmes are new: an 18-credit cleanroom certificate that stacks into a calculus-based A.S.",
    "credentialNote": "⚠ No licence governs this work, and most people in the occupation (84%, O*NET) hold only a high school diploma. In Florida the college programmes are how employers hire. The Semiconductor Cleanroom Operator college credit certificate (18 credits) stacks into the Semiconductor Engineering Technology A.S. (60 credits). Employers including SkyWater, Lockheed Martin, Draper and L3Harris helped shape Valencia's version. ⚠ The A.S. requires Calculus I and II and calculus-based physics; the certificate does not.",
    "cipCodes": [
        {"cipCode": "15.03", "note": "Electrical/electronic engineering technologies. Valencia's Semiconductor Engineering Technology A.S. is built on its electronics courses: circuits (EET2036C), digital systems (CET2114C), and semiconductor devices and circuits (EET2141C)."},
    ],
    "programs": [
        {"slug": "industrial-production-technology", "note": "Florida files both semiconductor programmes under CIP 15.0616, inside this group: the Semiconductor Cleanroom Operator certificate and the Semiconductor Engineering Technology A.S. ⚠ They are newer than the 2023 completions data, so they do not yet appear in this programme's school list."},
        {"slug": "electronics-engineering-technology", "note": "The neighbouring degree. Its circuits and digital courses are the foundation of the semiconductor A.S., and an electronics technician is qualified for equipment-maintenance roles in a fab."},
        {"slug": "advanced-manufacturing-technology", "note": "⚠ Robotics and automation: fabs move wafers by robot, and the semiconductor framework includes installing and programming robotic systems."},
        {"slug": "electrical-engineering", "isRoute": False, "note": "The bachelor's degree above this path, for chip design and process engineering. ⚠ Valencia's calculus-based A.S. is unusually well placed to continue into it."},
        {"slug": "materials-engineering", "isRoute": False, "note": "Where semiconductor manufacturing is studied as materials science; UCF teaches Principles of Semiconductor Manufacturing (EMA4411)."},
    ],
    "courses": [
        {"courseId": "ETS2160C", "reason": "Semiconductor Manufacturing Fundamentals: the whole process from wafer to chip, and the first course of the certificate.",
         "variantNote": "Valencia, Miami Dade and Tallahassee State."},
        {"courseId": "ETS2161C", "reason": "Introduction to Cleanroom Operation: gowning, contamination control, protocols and safety. The cleanroom operator's core course.",
         "variantNote": "⚠ Valencia only in the statewide course file. Other colleges cover cleanroom practice inside their fundamentals course."},
        {"courseId": "ETS2163C", "reason": "Semiconductor Fabrication Process: photolithography, etching, deposition and the sequence that builds a device layer by layer.",
         "variantNote": "Valencia, Miami Dade and St. Petersburg."},
        {"courseId": "ETS2165C", "reason": "Semiconductor Packaging Fundamentals: turning a finished die into a usable part. ⚠ Advanced packaging is the focus of SkyWater's Florida facility.",
         "variantNote": "Valencia, Miami Dade and St. Petersburg. Miami Dade titles its version Semiconductor Characterization and Packaging."},
        {"courseId": "ETS2167C", "reason": "Semiconductor Vacuum Systems and Applications: the pumps, chambers and gauges most fab tools depend on. Knowing them is the step from operator to technician.",
         "variantNote": "⚠ Valencia only; Valencia also teaches Introduction to Cleanroom Vacuum Systems (ETS2162C)."},
        {"courseId": "ETS2114C", "reason": "Lithography Methods in Semiconductor Manufacturing: the patterning step, which sets how small a chip's features can be.",
         "variantNote": "⚠ Miami Dade only (4 credits)."},
        {"courseId": "ETS2168C", "reason": "Semiconductor Plasma Techniques: plasma etching and cleaning, among the most equipment-intensive fab processes.",
         "variantNote": "⚠ Miami Dade only (4 credits)."},
        {"courseId": "EET2141C", "reason": "Semiconductor Devices and Circuits: how diodes and transistors work, which is the product the cleanroom is making.",
         "variantNote": "The state titles it Electronic Devices & Circuits I; Valencia, Indian River and Pensacola carry it. ⚠ Valencia uses the semiconductor title."},
        {"courseId": "CET2114C", "reason": "Digital Systems: the digital-logic foundation in both the certificate and the degree.",
         "variantNote": "⚠ The state titles it Digital Fundamentals; only Valencia and South Florida State carry this number. Most colleges teach digital logic under other numbers."},
        {"courseId": "MTB1329", "reason": "Mathematics for Engineering Technology: the maths requirement of the cleanroom certificate, and the right place to start for a student not ready for calculus.",
         "variantNote": "Valencia and Seminole State."},
        {"courseId": "ETS1603C", "reason": "Fundamentals of Robotics and Simulation: wafers move by robot, and the semiconductor framework includes installing and programming robotic systems.",
         "variantNote": "Nine state colleges, the most widely available course on this page."},
        {"courseId": "ETS2210C", "reason": "Principles of Photonics: light and optics, the physics behind lithography and much of fab metrology. Required in Valencia's A.S.",
         "variantNote": "Valencia and Hillsborough."},
        {"courseId": "MAC2311", "reason": "Calculus I. ⚠ Required, with Calculus II and calculus-based physics, in Valencia's Semiconductor Engineering Technology A.S. It is the hardest requirement of the degree and what keeps the bachelor's route open."},
        {"courseId": "EMA4411", "reason": "Principles of Semiconductor Manufacturing, at the bachelor's level, for a technician who continues into materials or electrical engineering.",
         "variantNote": "⚠ University of Central Florida only."},
    ],
    "sources": [
        {"label": "O*NET — Semiconductor Processing Technicians (51-9141.00)", "url": "https://www.onetonline.org/link/summary/51-9141.00",
         "note": "Tasks and sample titles quoted on this page; 31,900 employed (2024); much faster than average (7% or higher) to 2034; 3,900 openings a year; $51,430 median (2025); 84% high school diploma, 2% associate; Job Zone 1–2."},
        {"label": "O*NET — Florida wages for Semiconductor Processing Technicians", "url": "https://www.onetonline.org/link/localwages/51-9141.00?st=FL",
         "note": "Florida median $62,330 against $51,430 national (2025); 10th–90th percentile $39,980–$80,390 against $37,690–$82,540."},
        {"label": "Florida CTE frameworks via CPALMS — Semiconductor Cleanroom Operator (0615061601) and Semiconductor Engineering Technology (1615061600)", "url": "https://www.cpalms.org/PreviewCourseProgram/CTE?frameurl=%2Fsearch",
         "note": "18-credit certificate inside a 60-credit A.S.; content quoted on this page (circuits, robotics, wafer fabrication, photolithography, plasma etching, advanced packaging)."},
        {"label": "Valencia College catalog — Semiconductor Engineering Technology, A.S.", "url": "https://catalog.valenciacollege.edu/degrees/associateinscience/engineeringtechnology/semiconductorengineering/",
         "note": "Full course list, including MAC 2311, MAC 2312 and PHY 2048C; the 18-credit Cleanroom Operator certificate; 9 credits for Accelerated Skills Training."},
        {"label": "Valencia College — Semiconductor Engineering Technology programme page", "url": "https://valenciacollege.edu/future-students/semiconductor-engineering-technology-as.php",
         "note": "Names SkyWater Technology, Lockheed Martin, Draper and L3Harris as curriculum partners."},
        {"label": "Spectrum News 13 — Valencia College first in Florida to offer semiconductor technician degree (20 November 2025)", "url": "https://mynews13.com/fl/orlando/news/2025/11/20/valencia-college-is-first-in-florida-to-offer-semiconductor-technician-degree",
         "note": "Valencia as the first Florida college to offer the degree."},
        {"label": "St. Petersburg College — SMART Tech programme grows with launch of semiconductor certificate", "url": "https://www.spcollege.edu/spc-newsroom/smart-tech-program-grows-with-launch-of-semiconductor-certificate",
         "note": "18-credit Semiconductor Cleanroom Operator certificate; SMART Tech supported by $7.2 million in state workforce grants."},
        {"label": "SkyWater Technology — Department of Commerce grant to the Florida Semiconductor Coalition (2022)", "url": "https://www.businesswire.com/news/home/20220906005431/en/SkyWater-to-Leverage-36.5M-Department-of-Commerce-Grant-to-the-Florida-Semiconductor-Coalition-to-Expand-its-Advanced-Packaging-Facility-Operations-in-Florida",
         "note": "$36.5 million to expand SkyWater's advanced packaging facility operations in Florida (Osceola County)."},
        {"label": "Florida Statewide Course Numbering System — public carriers of every course named", "url": "https://flscns.fldoe.org/",
         "note": "Carrier counts from the SCNS course inventory (September 2026)."},
    ],
    "bodyHtml": body,
}

json.dump(doc, open(OUT, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=2)
print('wrote', os.path.relpath(OUT), len(body), 'chars of body')
