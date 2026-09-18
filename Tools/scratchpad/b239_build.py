#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Batch 239 -- the general and organic chemistry guides the Chemical Engineer path owes.

These are the highest-carrier courses this project has written in a long time:
CHM2046 at 20 institutions, CHM2210 and CHM2211 at 29 each. They serve every
pre-health, biology, chemistry and chemical engineering student in Florida, so
the findings below reach far past the path that surfaced them.

⚠⚠⚠ FINDING 1 -- TWO PARALLEL NUMBERING FAMILIES FOR GENERAL CHEMISTRY, and
NO institution carries both. Measured over the flat file, all four forms:

    CHM1045/1045C  19 institutions   CHM2045/2045C  20 institutions
    CHM1046/1046C  19               CHM2046/2046C  20
    both families:  0

Four public universities are in the 1000 family -- FSU, FAMU, FIU, FGCU --
with Broward, Miami Dade and Valencia. Benign for transfer (both lower
division); a guaranteed FAILED SEARCH otherwise. This also required correcting
six live career paths, done separately.

⚠ The ONE anomaly: Santa Fe College carries CHM2045 for the first course and
BOTH CHM1046 and CHM2046 for the second.

⚠⚠⚠ FINDING 2 -- THE STATE CONTRADICTS ITS OWN TRANSFER BOILERPLATE ON THE
SECOND HALF OF A SEQUENCE. CHM2046, CHM2210 and CHM2211 all carry
DS_Transferable1 = "GUARANTEED TRANSFER TO INSTITUTION OFFERING SAME COURSE"
AND, in the description, this:

    "***WARNING: THIS IS THE (2) PART OF A SEQUENCE OF (2) COURSES.*** A
    'SEQUENCE' ONCE STARTED SHOULD BE TAKEN ENTIRELY AT ONE INSTITUTION. THE
    ORDER OF TOPICS MAY VARY FROM SCHOOL TO SCHOOL. ONLY THE COMPLETED
    SEQUENCE AT ONE INSTITUTION IS EQUIVALENT TO A COMPLETED SEQUENCE AT
    ANOTHER. INDIVIDUAL COURSES WITHIN A SEQUENCE ARE NOT NECESSARILY
    EQUIVALENT, AND MUST BE EVALUATED BY A RECEIVING INSTITUTION ON AN
    INDIVIDUAL BASIS."

11 CHM numbers carry it -- 031 040 041 046 050 051 096 210 211 400 401, every
one the later half of a sequence. So it is an SCNS convention for sequences,
not a one-off, and it is the strongest qualification of the transfer guarantee
this project has found stated by the state itself.

⚠⚠ FINDING 3 -- THE DUAL-ENROLMENT SPLIT INSIDE ONE SEQUENCE. hs_credit is
ELECTIVE on CHM2045 and SCIENCE on CHM2046, CHM2210 and CHM2211. Distribution
test, stratified to LOWER division where dual enrolment can apply: 22 ELECTIVE
/ 19 SCIENCE across 41 rows -- genuinely discriminating, not boilerplate. The
finding is the SIBLING comparison (batch 227): two halves of one sequence,
two different high-school outcomes.

⚠⚠ FINDING 4 -- ORGANIC CHEMISTRY IS A BARE/C SPLIT WITH ZERO OVERLAP.
29 institutions carry CHM2210 + a separate CHM2210L; 7 carry the integrated
CHM2210C at 4 credits (Polk State 5). No institution carries both. The
batch-219 INSTITUTIONAL SIGNATURE: one course filed two ways, both ids real,
and an evaluator matching on the identifier sees a mismatch where there is
none. Per batch 228 this also predicts a future guide request on the C ids.

CONTACT HOURS ARE PUBLISHED, not derived: Gulf Coast State College gives
"Credit hours 3 / Lecture hours 3" for CHM2210 and CHM2211 -> 45.

CREDIT DIVERGENCE (resolve the range):
    CHM2210  3 credits at 26 institutions; 4 at FIU, Florida SouthWestern, Hillsborough
    CHM2211  3 credits at 27; 4 at Florida SouthWestern and Hillsborough
    ⚠ FIU is 4 for Organic I and 3 for Organic II -- asymmetric inside one institution
    CHM2046  3 credits at ALL 20 -- state the uniformity explicitly
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


FAM_1000 = ('Broward, Daytona State, Eastern Florida State, Florida A&amp;M, Florida Gulf Coast, '
            'Florida Keys, Florida State, FIU, Gulf Coast, Indian River State, Miami Dade, North '
            'Florida, Northwest Florida State, Palm Beach State, Pensacola State, Polk State, '
            'St. Johns River State, Tallahassee State and Valencia')
FAM_2000 = ('College of Central Florida, FAU, Florida Gateway, Florida Polytechnic, FSCJ, Florida '
            'SouthWestern, Hillsborough, Lake-Sumter, New College, Pasco-Hernando, State College '
            'of Florida, Santa Fe, South Florida State, St. Petersburg, Seminole State, UCF, UF, '
            'UNF, USF and UWF')

TWO_FAMILIES = (
    '<h3>&#9888;&#9888;&#9888; Florida numbers general chemistry TWO ways, and no institution '
    'carries both</h3>'
    '<p>This is the single most useful thing on this page for a student who is transferring, '
    'dual-enrolled, or simply looking their own course up.</p>'
    '<table class="table table-sm"><thead><tr><th>Family</th><th>Institutions</th>'
    '<th>Who uses it</th></tr></thead><tbody>'
    '<tr><td><code>CHM1045</code> / <code>CHM1046</code><br>(or <code>CHM1045C</code> / '
    '<code>CHM1046C</code>)</td><td><strong>19</strong></td><td>%s</td></tr>'
    '<tr><td><code>CHM2045</code> / <code>CHM2046</code><br>(or <code>CHM2045C</code> / '
    '<code>CHM2046C</code>)</td><td><strong>20</strong></td><td>%s</td></tr>'
    '</tbody></table>'
    '<p>&#9888;&#9888; <strong>Zero institutions carry both.</strong> Same course, same '
    'lower-division level, same content, and the credit articulates either way — <strong>but the '
    'other number simply does not exist at your school</strong>, so a student searching a catalogue '
    'or a degree audit for the wrong one finds nothing and concludes something is wrong.</p>'
    '<p>&#9888; <strong>Look up which family your institution uses before you go looking for the '
    'course.</strong> The one anomaly worth knowing: <strong>Santa Fe College</strong> uses '
    '<code>CHM2045</code> for the first course and carries <em>both</em> <code>CHM1046</code> and '
    '<code>CHM2046</code> for the second.</p>'
    '<h3>&#9888; And check the packaging, which is a second axis</h3>'
    '<p>Within each family the course is sold two ways. <strong>The bare number is a 3-credit '
    'lecture and needs a separate 1-credit <code>L</code> laboratory</strong> — two registrations, '
    'two grades, 4 credits. <strong>The <code>C</code> form is the integrated lecture-plus-lab at '
    '4 credits</strong> — one registration, one grade. Daytona State, FSCJ, Lake-Sumter, '
    'Northwest Florida State, Polk State, Seminole State and Valencia use the <code>C</code> form. '
    '<strong>Both are complete and both transfer; they are packaged differently, and packaging is '
    'not divergence.</strong> What matters is that if your institution uses the bare number and you '
    'register for the lecture alone, <strong>you have not taken the laboratory</strong>, and every '
    'programme that requires this course requires the laboratory with it.</p>'
) % (FAM_1000, FAM_2000)

SEQUENCE_WARNING = (
    '<h3>&#9888;&#9888;&#9888; The state qualifies its own transfer guarantee on this course</h3>'
    '<p>The statewide record carries the usual line — <em>&ldquo;guaranteed transfer to '
    'institution offering same course&rdquo;</em> — and then, in the course description itself, '
    'this:</p>'
    '<blockquote class="blockquote"><p>&ldquo;<strong>WARNING: THIS IS THE (2) PART OF A SEQUENCE '
    'OF (2) COURSES.</strong> A &lsquo;sequence&rsquo; once started should be taken entirely at one '
    'institution. The order of topics may vary from school to school. <strong>Only the completed '
    'sequence at one institution is equivalent to a completed sequence at another institution. '
    'Individual courses within a sequence are not necessarily equivalent</strong>, and must be '
    'evaluated by a receiving institution on an individual basis.&rdquo;</p></blockquote>'
    '<p>&#9888;&#9888; <strong>Read that as what it is: the state telling you the guarantee is '
    'weaker here than it looks.</strong> It appears on eleven <code>CHM</code> numbers, every one '
    'of them the later half of a sequence, so it is a deliberate SCNS convention rather than a note '
    'about this course in particular.</p>'
    '<p><strong>The practical rule is short: finish the sequence where you started it.</strong> '
    'Where that is genuinely impossible — a mid-year transfer, a move — take the syllabus and the '
    'topic list to the receiving department <em>before</em> registering and get the equivalence in '
    'writing. The reason the state hedges is real: the order of topics varies, so half a sequence '
    'at one school is not necessarily the same half at another, and the gap does not show up until '
    'the second course assumes something you were never taught.</p>'
)

DUAL_ENROL = (
    '<h3>&#9888;&#9888; Dual-enrolled students: the two halves earn DIFFERENT high-school credit</h3>'
    '<p>SCNS records what a dual-enrolled high-school student earns, and it is not the same across '
    'the sequence:</p>'
    '<table class="table table-sm"><tbody>'
    '<tr><td>General Chemistry I (<code>CHM2045</code> / <code>CHM1045</code>)</td>'
    '<td>&#9888; <strong>ELECTIVE</strong></td></tr>'
    '<tr><td>General Chemistry II (<code>CHM2046</code> / <code>CHM1046</code>)</td>'
    '<td><strong>SCIENCE</strong></td></tr>'
    '<tr><td>Organic Chemistry I and II</td><td><strong>SCIENCE</strong></td></tr>'
    '</tbody></table>'
    '<p>&#9888; <strong>The college credit is unaffected either way.</strong> What differs is the '
    'high-school requirement it fills — so a student taking general chemistry I expecting to clear '
    'a high-school <em>science</em> requirement may receive elective credit instead. This is not a '
    'quirk of the prefix: across the 41 active lower-division <code>CHM</code> numbers the field '
    'splits 22 elective to 19 science, so it genuinely discriminates and is worth checking rather '
    'than assuming. <strong>Confirm with your counsellor and your district&rsquo;s articulation '
    'agreement before you enrol, not after.</strong></p>'
)

GORDON = (
    '<h3>&#9888; General-education and Gordon Rule designations are set by your institution</h3>'
    '<p>A designation is recorded for this course at some Florida institutions and not others, and '
    'the flags in the state file reliably say that <em>a</em> designation exists without reliably '
    'saying <em>which</em>. <strong>Read your own institution&rsquo;s general-education list.</strong> '
    'And where a Gordon Rule designation does apply, remember the condition that catches people: '
    '<strong>a grade of C or higher is required for it to count, and a C&minus; does not '
    'satisfy it</strong> at most institutions — stricter than the ordinary passing standard.</p>'
)


def guide(title, credits, hours, prereq, html, notes):
    return {'title': title, 'html_content': html, 'credits': credits, 'contact_hours': hours,
            'prerequisites': prereq, 'version': '1.0', 'offering_notes': notes}


def offs(rows):
    return [{'institution': c, 'institution_name': n, 'title': t, 'credits': cr,
             'contact_hours': ch, 'note': nt} for c, n, t, cr, ch, nt in rows]


G = {}

G['CHM2046'] = guide(
    'General Chemistry II', 3, 45,
    'General Chemistry I with a minimum grade of C, and its laboratory, at essentially every '
    'institution; college algebra or higher is normally required alongside. The statewide '
    'prerequisite field is blank, which is a gap in the record rather than an open door. '
    'WARNING - LOOK UP WHICH NUMBER YOUR SCHOOL USES. Florida runs TWO parallel numbering families '
    'for general chemistry and NO institution carries both: 20 institutions use CHM2046 (or the '
    'integrated CHM2046C) and 19 use CHM1046 (or CHM1046C), including Florida State, Florida A&M, '
    'FIU, FGCU, Broward, Miami Dade and Valencia. '
    'AND THE STATE QUALIFIES ITS OWN TRANSFER GUARANTEE HERE: the statewide description says a '
    'sequence "once started should be taken entirely at one institution" and that only the '
    'COMPLETED sequence is equivalent. FINISH GENERAL CHEMISTRY WHERE YOU STARTED IT. '
    'ALL 20 CARRIERS RUN IT AT 3 CREDITS, with a separate 1-credit CHM2046L laboratory that every '
    'programme requiring the course also requires.',
    '<h2>Course Description</h2>'
    '<p><strong>General Chemistry II</strong> is the second half of the majors general chemistry '
    'sequence, and it is where the subject turns from structure to behaviour: what reactions do, '
    'how fast, how far, and why. The statewide record is explicit that it is the '
    '<strong>last course in the sequence</strong> begun in General Chemistry I.</p>'
    '<p>Carried by <strong>20 Florida public institutions, every one of them at 3 credits</strong>, '
    'with a separate 1-credit laboratory.</p>'
    '<p>&#9888; <strong>This is the course that decides a lot of careers</strong>, and not because '
    'it is the hardest. Equilibrium, kinetics and thermodynamics are the foundation of organic '
    'chemistry, biochemistry, chemical engineering and every health-professions prerequisite chain '
    'in the state — so a weak pass here is felt for three more years.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Determine <strong>reaction rates and rate laws</strong>, and use the integrated rate '
         'equations and the Arrhenius relation.',
         'Apply the <strong>equilibrium constant</strong> to gaseous and aqueous systems, and '
         'predict the effect of a disturbance.',
         'Solve <strong>acid-base equilibrium</strong> problems, including buffers, titration '
         'curves and polyprotic systems.',
         'Apply <strong>solubility and complex-ion equilibria</strong>.',
         'Use <strong>enthalpy, entropy and Gibbs free energy</strong> to predict spontaneity, and '
         'relate &#916;G&deg; to the equilibrium constant.',
         'Balance and analyse <strong>redox reactions</strong>, and compute cell potentials using '
         'the Nernst equation.',
         'Describe the <strong>properties of solutions</strong>, including colligative properties.')
    + '<h3>Optional Outcomes</h3>'
    + li('Nuclear chemistry: decay, half-life, fission and fusion.',
         'Coordination chemistry and transition-metal complexes.',
         'Introductory organic and biochemistry, where the institution includes a preview.',
         'Descriptive chemistry of the main-group elements.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Intermolecular forces, liquids, solids and solutions; colligative properties.',
         'Chemical kinetics: rate laws, mechanisms, catalysis.',
         'Chemical equilibrium and Le Ch&acirc;telier&rsquo;s principle.',
         'Acids, bases, buffers and titrations.',
         'Solubility and complex-ion equilibria.',
         'Thermodynamics: entropy, free energy, spontaneity.',
         'Electrochemistry: galvanic and electrolytic cells, the Nernst equation.')
    + '<h3>Optional Topics</h3>'
    + li('Nuclear chemistry.', 'Coordination compounds and crystal field theory.',
         'Main-group descriptive chemistry.', 'An introduction to organic functional groups.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Brown, LeMay &amp; Bursten <em>Chemistry: The Central Science</em>, Zumdahl, Chang, and '
    'Tro are the widely adopted texts; several Florida colleges use OpenStax <em>Chemistry</em>, '
    'which is free.</li>'
    '<li>A scientific calculator with logarithms is assumed from the first week — equilibrium and '
    'pH problems are unworkable without fluency in logs and exponents.</li>'
    '<li>Online homework systems (ALEKS, Mastering Chemistry, WebAssign) are near-universal and '
    'usually carry an access fee separate from the textbook. Budget for it.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>This course sits on the <strong>Chemical Engineer</strong> career path in this repository, '
    'and it is a prerequisite far beyond it. General chemistry II gates organic chemistry, and '
    'organic chemistry gates medicine, dentistry, pharmacy, veterinary medicine, biochemistry, '
    'chemistry and chemical engineering. In Florida it also feeds environmental and water-quality '
    'work, pharmaceutical and biotechnology manufacturing, the phosphate and fertiliser industry, '
    'and forensic and clinical laboratory science.</p>'
    '<h2>Special Information</h2>'
    + TWO_FAMILIES + SEQUENCE_WARNING + DUAL_ENROL +
    '<h3>&#9888; General Chemistry I carries a &ldquo;(GE CORE)&rdquo; marker and this course does '
    'not</h3>'
    '<p>The statewide title of <code>CHM2045</code> ends <strong>&ldquo;(GE CORE)&rdquo;</strong>, '
    'identifying it as a Florida General Education Core course under s. 1007.25, F.S. — which '
    'means it satisfies its general-education subject area at <em>every</em> Florida public college '
    'and university, a materially stronger protection than the ordinary transfer line. <strong>The '
    'statewide title of this course does not carry that marker</strong>; it reads &ldquo;General '
    'Chem II (last course in sequence)&rdquo;.</p>'
    '<p>&#9888; <strong>Do not read that as a warning, but do check it rather than assume.</strong> '
    'Twelve of the twenty carriers record a natural-science general-education designation on this '
    'course. What the marker&rsquo;s absence means is that the guarantee attaching to the first '
    'course is not automatically inherited by the second, and <strong>a programme requiring a '
    '&ldquo;science with laboratory&rdquo; is applying its own rule, not a state one.</strong></p>'
    '<h3>Titles vary and the course does not</h3>'
    '<p>Twelve institutions call it <em>General Chemistry II</em>. UCF calls it <em>Chemistry '
    'Fundamentals II</em>, Santa Fe <em>College Chemistry 2</em>, Florida Polytechnic '
    '<em>Chemistry 2</em>, and Pasco-Hernando <em>General Chemistry and Qualitative Analysis II</em>. '
    'Several institutions also run an <em>Honors</em> section under the same number. &#9888; '
    '<strong>That is branding, not divergence</strong> — on a high-carrier general-education-adjacent '
    'number, many titles mean the same required course named twenty different ways. Register by the '
    'number.</p>' + GORDON,
    {'summary': 'Twenty Florida public institutions carry CHM2046, ALL of them at 3 credits, with a '
                'separate 1-credit CHM2046L laboratory. A further 19 institutions teach the same '
                'course as CHM1046 or CHM1046C; no institution carries both families. No carrier '
                'publishes a contact-hour figure for this number.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the uniform 3-credit '
                   'value, and corroborated by Gulf Coast State College, which publishes "Credit '
                   'hours 3 / Lecture hours 3" for the equivalent course in the 1000-numbered '
                   'family.',
     'offerings': offs([
         ('UF', 'University of Florida', 'General Chemistry II', 3, None, None),
         ('USF', 'University of South Florida', 'General Chemistry II', 3, None, None),
         ('UCF', 'University of Central Florida', 'Chemistry Fundamentals II', 3, None,
          '⚠ A different title for the same course; UCF also runs an Honors section.'),
         ('UNF', 'University of North Florida', 'General Chemistry II', 3, None, None),
         ('UWF', 'University of West Florida', 'General Chemistry II', 3, None, None),
         ('FAU', 'Florida Atlantic University', 'General Chemistry 2', 3, None,
          'Also runs Honors General Chemistry II under the same number.'),
         ('FLPOLY', 'Florida Polytechnic University', 'Chemistry 2', 3, None, None),
         ('SFC', 'Santa Fe College', 'College Chemistry 2', 3, None,
          '⚠ Santa Fe carries BOTH CHM1046 and CHM2046 — the only institution in the '
          'state that does.'),
         ('SPC', 'St. Petersburg College', 'General Chemistry II', 3, None, None),
         ('PHSC', 'Pasco-Hernando State College',
          'General Chemistry and Qualitative Analysis II', 3, None, None),
         ('HC', 'Hillsborough Community College', 'General Chemistry II', 3, None, None),
         ('FSWSC', 'Florida SouthWestern State College', 'General Chemistry II', 3, None, None),
         ('SSCF', 'Seminole State College of Florida', 'General Chemistry II', 3, None,
          'Seminole State also carries the integrated CHM2046C.'),
         ('CF', 'College of Central Florida', 'General Chemistry II', 3, None, None),
         ('FGC', 'Florida Gateway College', 'General Chemistry II', 3, None, None),
         ('SCFMS', 'State College of Florida, Manatee-Sarasota', 'General Chemistry II', 3, None,
          None),
         ('SFSC', 'South Florida State College', 'General Chemistry II', 3, None,
          'Also runs an Honors section under the same number.'),
     ])})

ORG_COMMON_RESOURCES = (
    '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Klein <em>Organic Chemistry</em>, Carey &amp; Giuliano, Smith, and Bruice are the widely '
    'adopted texts; Klein&rsquo;s <em>Organic Chemistry as a Second Language</em> is the most '
    'commonly recommended supplement in Florida and is worth buying early rather than in week '
    'ten.</li>'
    '<li><strong>A molecular model kit.</strong> Stereochemistry is a three-dimensional subject '
    'taught on two-dimensional paper, and students who build the molecules do measurably better '
    'than students who try to rotate them mentally.</li>'
    '<li>Online homework (Sapling, ACE Organic, Mastering) is near-universal and carries its own '
    'access fee.</li>'
    '<li>The <strong>American Chemical Society</strong> publishes standardised final examinations '
    'used by several Florida institutions; ACS study guides are the right practice material where '
    'yours does.</li>'
    '</ul>')

G['CHM2210'] = guide(
    'Organic Chemistry I', 3, 45,
    'General Chemistry II with a minimum grade of C, and its laboratory. The statewide prerequisite '
    'field is blank; the real gate is universal and institutions enforce it. NOTE THE NUMBER YOUR '
    'SCHOOL USES FOR THAT PREREQUISITE: 20 institutions call it CHM2046 and 19 call it CHM1046, and '
    'no institution carries both. '
    'THIS IS A LECTURE COURSE. 29 institutions carry CHM2210 at 3 credits with a SEPARATE 1-credit '
    'CHM2210L laboratory - two registrations - while 7 (Daytona State, FSCJ, Lake-Sumter, Northwest '
    'Florida State, Polk State, Seminole State, Valencia) carry the INTEGRATED CHM2210C at 4 '
    'credits instead. NO INSTITUTION CARRIES BOTH FORMS. Register for the laboratory: every '
    'programme that requires organic chemistry requires it. '
    'CREDITS: 3 at 26 institutions; 4 at FIU, Florida SouthWestern State and Hillsborough. '
    'PLAN THE TIME HONESTLY - 10 to 15 hours a week outside class is the normal figure, and this '
    'course rewards daily practice rather than revision before an examination.',
    '<h2>Course Description</h2>'
    '<p><strong>Organic Chemistry I</strong> is the study of carbon compounds: their structure, '
    'their three-dimensional shape, and the mechanisms by which they react. The statewide record '
    'states plainly that <strong><code>CHM2210</code> + <code>CHM2211</code> = one year of '
    'organic</strong>, and lists the content as classes of organic compounds, atomic and molecular '
    'structure, resonance, aromaticity, thermodynamics applied to organic reactions, '
    'stereochemistry and acid-base theory.</p>'
    '<p>Carried by <strong>29 Florida public institutions</strong> — one of the most widely '
    'offered courses in the state.</p>'
    '<p>&#9888;&#9888; <strong>It has a reputation and the reputation is earned, but it is earned '
    'for a reason worth understanding.</strong> Organic chemistry is not harder arithmetic than '
    'general chemistry; it is a <em>different kind of subject</em>. There is very little to '
    'calculate and a great deal to understand — patterns, mechanisms, and why electrons move where '
    'they move. <strong>Students who study it the way they studied calculus, by working problems '
    'to a formula, are the ones who struggle.</strong> Students who learn to push arrows and '
    'explain mechanisms out loud generally do not.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Name and draw organic structures using <strong>IUPAC nomenclature</strong>, and convert '
         'between condensed, skeletal and three-dimensional representations.',
         'Explain <strong>structure and bonding</strong>: hybridisation, molecular orbitals, '
         'resonance and inductive effects.',
         'Analyse <strong>stereochemistry</strong> — chirality, R/S assignment, enantiomers, '
         'diastereomers, and conformational analysis of alkanes and cyclohexanes.',
         'Apply <strong>acid-base theory</strong> to organic molecules and rank acidity from '
         'structure.',
         'Predict products and write <strong>curved-arrow mechanisms</strong> for substitution and '
         'elimination (S<sub>N</sub>1, S<sub>N</sub>2, E1, E2), and choose between them.',
         'Predict products and mechanisms for <strong>addition reactions of alkenes and '
         'alkynes</strong>, including regiochemistry and stereochemistry.',
         'Interpret basic <strong>spectroscopy</strong> — IR and mass spectrometry, and usually an '
         'introduction to NMR.')
    + '<h3>Optional Outcomes</h3>'
    + li('Radical reactions and radical halogenation.',
         'Alcohols, ethers and epoxides, where the institution places them in the first term.',
         'Introduction to synthesis and multi-step retrosynthetic analysis.',
         'Extended NMR interpretation, where the institution places it here rather than in the '
         'second term.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Structure, bonding and hybridisation; drawing conventions.',
         'Functional groups and IUPAC nomenclature.',
         'Acids and bases in organic systems.',
         'Alkanes and conformational analysis.',
         'Stereochemistry and chirality.',
         'Substitution and elimination: S<sub>N</sub>1, S<sub>N</sub>2, E1, E2.',
         'Alkenes and alkynes: addition reactions, regiochemistry, stereochemistry.',
         'Introduction to spectroscopy: IR, mass spectrometry, NMR.')
    + '<h3>Optional Topics</h3>'
    + li('Free-radical reactions.', 'Alcohols, ethers and epoxides.',
         'Organometallic reagents.', 'Introductory synthesis design.')
    + ORG_COMMON_RESOURCES +
    '<h2>Career Pathways</h2>'
    '<p>&#9888; <strong>Organic chemistry is the gatekeeping course of the health professions.</strong> '
    'Medicine, dentistry, pharmacy, veterinary medicine, optometry and physician assistant '
    'programmes all require the full year, and admissions committees read the grade closely because '
    'it is the closest undergraduate analogue to the volume and pace of professional school. It is '
    'also required for chemistry, biochemistry, biology and — alone among the engineering '
    'disciplines — <strong>chemical engineering</strong>, whose path in this repository names it '
    'for exactly that reason.</p>'
    '<p>In Florida it leads into pharmaceutical and biotechnology manufacturing, the phosphate and '
    'specialty chemicals industry, environmental and water-quality laboratories, forensic chemistry, '
    'and agricultural chemistry.</p>'
    '<h2>Special Information</h2>'
    '<h3>&#9888;&#9888;&#9888; Two packagings, and no institution carries both</h3>'
    '<table class="table table-sm"><thead><tr><th>Form</th><th>Credits</th><th>Institutions</th>'
    '</tr></thead><tbody>'
    '<tr><td><code>CHM2210</code> lecture + separate <code>CHM2210L</code> laboratory</td>'
    '<td>3 + 1</td><td><strong>29</strong></td></tr>'
    '<tr><td><code>CHM2210C</code> integrated lecture and laboratory</td><td><strong>4</strong> '
    '(Polk State 5)</td><td><strong>7</strong> — Daytona State, FSCJ, Lake-Sumter, Northwest '
    'Florida State, Polk State, Seminole State, Valencia</td></tr>'
    '</tbody></table>'
    '<p>&#9888;&#9888; <strong>Both identifiers are real and no institution carries both.</strong> '
    'This is one course filed two ways, and the consequence falls on transfer: <strong>an evaluator '
    'matching on the identifier sees <code>CHM2210C</code> against a requirement for '
    '<code>CHM2210</code> and reads a mismatch where there is none.</strong> If you are moving '
    'between a <code>C</code> institution and a bare-number institution, say so explicitly and send '
    'the syllabus — it is a one-line problem that becomes an expensive one if nobody raises it.</p>'
    '<p>&#9888; <strong>And whichever form your school uses, you must end up with the laboratory.</strong> '
    'At a bare-number institution that means two separate registrations, and the laboratory is '
    'frequently the one that fills first.</p>'
    '<h3>&#9888; Credits: three at most institutions, four at three of them</h3>'
    '<p>Twenty-six institutions carry the lecture at <strong>3 credits</strong>. Three carry it at '
    '<strong>4</strong>: <strong>FIU, Florida SouthWestern State College and Hillsborough Community '
    'College</strong>. A transfer student moving from a 4-credit institution to a 3-credit one '
    'arrives with a credit that has nowhere to go, and one moving the other way may be a credit '
    'short against a degree requirement. &#9888; Note also that <strong>FIU carries Organic I at 4 '
    'credits and Organic II at 3</strong> — asymmetric within its own sequence, which is unusual '
    'and worth checking against your audit.</p>'
    '<h3>Honours sections share the number</h3>'
    '<p>College of Central Florida, FAU, Gulf Coast, South Florida State and UCF run an '
    '<em>Honors</em> section under the same identifier. The content is the statewide content; the '
    'pace and the assessment are heavier. <strong>It is the same course for transfer and audit '
    'purposes</strong>, and the honours designation is your institution&rsquo;s, not the '
    'state&rsquo;s.</p>'
    + SEQUENCE_WARNING.replace('this course', 'the organic chemistry sequence') + DUAL_ENROL +
    '<h3>&#9888;&#9888; Plan the hours before the term, not after the first examination</h3>'
    '<p>Ten to fifteen hours a week outside class is the normal figure, and unlike most courses '
    '<strong>the time cannot be compressed into the days before an examination</strong>: mechanisms '
    'have to become automatic, and that only happens with daily repetition. The single most '
    'reliable predictor of a good grade is whether a student worked problems every day from week '
    'one. &#9888; If you are working long hours, taking this alongside another heavy science '
    'course, or both, <strong>consider a summer term where the course runs on its own</strong> — '
    'many Florida institutions offer it, and it is a legitimate strategy rather than an '
    'admission of weakness.</p>' + GORDON,
    {'summary': 'Twenty-nine Florida public institutions carry CHM2210 as a lecture with a separate '
                'CHM2210L laboratory — 26 at 3 credits, and FIU, Florida SouthWestern State and '
                'Hillsborough at 4. A further seven carry the integrated CHM2210C at 4 credits '
                '(Polk State at 5) and no institution carries both forms.',
     'hours_source': 'published', 'derived_contact_hours': 45,
     'derivation': 'PUBLISHED, not derived: Gulf Coast State College gives "Credit hours: 3 / '
                   'Lecture hours: 3" for CHM2210, which is 45 contact hours over a 15-week term '
                   'and matches the Florida convention. Gulf Coast separately publishes "Credit '
                   'hours: 1 / Lab hours: 3" for CHM2210L.',
     'offerings': offs([
         ('GCSC', 'Gulf Coast State College', 'Organic Chemistry', 3, 45,
          'Publishes its hours explicitly: 3 lecture hours weekly. Also runs an Honors section.'),
         ('UF', 'University of Florida', 'Organic Chemistry 1', 3, None, None),
         ('USF', 'University of South Florida', 'Organic Chemistry I', 3, None, None),
         ('UCF', 'University of Central Florida', 'Organic Chemistry I', 3, None, None),
         ('UNF', 'University of North Florida', 'Organic Chemistry I', 3, None, None),
         ('UWF', 'University of West Florida', 'Organic Chemistry I', 3, None, None),
         ('FSU', 'Florida State University', 'Organic Chemistry I', 3, None, None),
         ('FAMU', 'Florida A&M University', 'Organic Chemistry I', 3, None, None),
         ('FGCU', 'Florida Gulf Coast University', 'Organic Chemistry I', 3, None, None),
         ('FAU', 'Florida Atlantic University', 'Organic Chemistry I', 3, None,
          'Also runs Honors Organic Chemistry I under the same number.'),
         ('FLPOLY', 'Florida Polytechnic University', 'Organic Chemistry 1', 3, None, None),
         ('FIU', 'Florida International University', 'Organic Chemistry I', 4, None,
          '⚠ FOUR credits — and FIU carries Organic II at three.'),
         ('FSWSC', 'Florida SouthWestern State College', 'Organic Chemistry I', 4, None,
          '⚠ Four credits.'),
         ('HC', 'Hillsborough Community College', 'Organic Chemistry I', 4, None,
          '⚠ Four credits.'),
         ('BC', 'Broward College', 'Organic Chemistry I', 3, None, None),
         ('MDC', 'Miami Dade College', 'Organic Chemistry 1', 3, None, None),
         ('SPC', 'St. Petersburg College', 'Organic Chemistry I', 3, None, None),
         ('SFC', 'Santa Fe College', 'Organic Chemistry I', 3, None, None),
         ('IRSC', 'Indian River State College', 'Organic Chemistry I', 3, None, None),
         ('EFSC', 'Eastern Florida State College', 'Organic Chemistry 1', 3, None, None),
         ('PBSC', 'Palm Beach State College', 'Organic Chemistry I', 3, None, None),
         ('PESC', 'Pensacola State College', 'Organic Chemistry I', 3, None, None),
         ('TSC', 'Tallahassee State College', 'Organic Chemistry I', 3, None, None),
         ('SJRSC', 'St. Johns River State College', 'Organic Chemistry I', 3, None, None),
         ('SCFMS', 'State College of Florida, Manatee-Sarasota', 'Organic Chemistry I', 3, None,
          None),
         ('SFSC', 'South Florida State College', 'Organic Chemistry I', 3, None,
          'Also runs an Honors section.'),
         ('CF', 'College of Central Florida', 'Organic Chemistry I', 3, None,
          'Also runs an Honors section.'),
         ('FGC', 'Florida Gateway College', 'Organic Chemistry I', 3, None, None),
         ('NFC', 'North Florida College', 'Organic Chemistry I', 3, None, None),
     ])})

G['CHM2211'] = guide(
    'Organic Chemistry II', 3, 45,
    'Statewide prerequisite: CHM2210 Organic Chemistry I, and institutions require a minimum grade '
    'of C. The laboratory is normally required alongside or before. '
    'THE SAME TWO PACKAGINGS AS ORGANIC I, AND THE SAME ZERO OVERLAP: 29 institutions carry '
    'CHM2211 at 3 credits with a separate 1-credit CHM2211L laboratory; SEVEN carry the '
    'integrated CHM2211C at 4 credits instead, and NO institution carries both. '
    'CREDITS: 3 everywhere except Florida SouthWestern State and Hillsborough, which carry it at 4. '
    'Note FIU runs Organic I at 4 credits and this course at 3. '
    'FINISH THE SEQUENCE WHERE YOU STARTED IT. The statewide record warns explicitly that a '
    'sequence "once started should be taken entirely at one institution", that the ORDER OF TOPICS '
    'VARIES BY SCHOOL, and that only the COMPLETED sequence is equivalent - so a student who takes '
    'Organic I at one college and Organic II at another can meet material the first course never '
    'covered and miss material it did.',
    '<h2>Course Description</h2>'
    '<p><strong>Organic Chemistry II</strong> completes the year. Where the first term builds the '
    'toolkit — structure, stereochemistry, mechanism, substitution and addition — the second term '
    'spends it: aromatic chemistry, carbonyl chemistry, and the multi-step syntheses that combine '
    'everything. The statewide record treats the pair as a unit: <strong><code>CHM2210</code> + '
    '<code>CHM2211</code> = one year of organic</strong>.</p>'
    '<p>Carried by <strong>29 Florida public institutions</strong>.</p>'
    '<p>&#9888; <strong>Most students find this term more manageable than the first, and the reason '
    'is worth knowing.</strong> Organic I asks you to learn a new way of thinking; Organic II asks '
    'you to apply it to more reactions. The volume is larger and the conceptual jump is '
    'smaller — <em>provided</em> the mechanisms from the first term became automatic. Where they '
    'did not, this is the term that finds out.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Explain <strong>aromaticity</strong> and apply H&uuml;ckel&rsquo;s rule, including to '
         'heterocycles and charged rings.',
         'Predict products and mechanisms for <strong>electrophilic aromatic substitution</strong>, '
         'and use substituent effects to predict regiochemistry.',
         'Predict products and mechanisms for <strong>nucleophilic addition to carbonyls</strong> — '
         'aldehydes and ketones.',
         'Predict products and mechanisms for <strong>nucleophilic acyl substitution</strong> — '
         'carboxylic acids and their derivatives.',
         'Apply <strong>enolate chemistry</strong>: alpha-substitution, aldol, Claisen and related '
         'condensations.',
         'Work with <strong>amines</strong> and nitrogen-containing compounds.',
         'Interpret <strong>NMR spectra</strong> (<sup>1</sup>H and <sup>13</sup>C) alongside IR '
         'and mass spectrometry to determine a structure.',
         'Design <strong>multi-step syntheses</strong> using retrosynthetic analysis.')
    + '<h3>Optional Outcomes</h3>'
    + li('Biomolecules: carbohydrates, amino acids, peptides, lipids and nucleic acids.',
         'Pericyclic reactions and Diels-Alder chemistry, where not covered in the first term.',
         'Polymers and polymerisation mechanisms.',
         'Organometallic and transition-metal-catalysed coupling reactions.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Aromaticity and the chemistry of benzene.',
         'Electrophilic aromatic substitution; substituent effects and directing.',
         'Aldehydes and ketones: nucleophilic addition.',
         'Carboxylic acids and derivatives: nucleophilic acyl substitution.',
         'Enols, enolates and condensation reactions.',
         'Amines and their reactions.',
         'Structure determination by NMR, IR and mass spectrometry.',
         'Multi-step synthesis and retrosynthetic analysis.')
    + '<h3>Optional Topics</h3>'
    + li('Carbohydrates, amino acids and proteins.', 'Lipids and nucleic acids.',
         'Pericyclic reactions.', 'Polymer chemistry.',
         'Transition-metal-catalysed cross-coupling.')
    + ORG_COMMON_RESOURCES +
    '<h2>Career Pathways</h2>'
    '<p>Completing the full year is what actually satisfies the requirement. <strong>Medicine, '
    'dentistry, pharmacy, veterinary medicine, optometry and physician assistant programmes '
    'require both terms</strong>, and most require both laboratories. It is also required for '
    'chemistry, biochemistry, biology and <strong>chemical engineering</strong> — the only '
    'engineering discipline that requires organic chemistry, and the reason this course appears '
    'on the Chemical Engineer career path in this repository.</p>'
    '<p>&#9888; <strong>The second term is the one that carries the most professional weight</strong>, '
    'because carbonyl chemistry and spectroscopy are what pharmaceutical, biotechnology and '
    'analytical laboratory work actually use. In Florida that means pharmaceutical and '
    'biotechnology manufacturing, environmental and water-quality laboratories, forensic chemistry '
    'and the specialty chemicals industry.</p>'
    '<h2>Special Information</h2>'
    + SEQUENCE_WARNING +
    '<h3>&#9888;&#9888; Why the sequence warning bites harder here than anywhere else</h3>'
    '<p>The state says the <strong>order of topics may vary from school to school</strong>, and on '
    'organic chemistry that is not a formality. Institutions genuinely differ on where they place '
    'alcohols and ethers, radical reactions, NMR, and the Diels-Alder reaction — some in the first '
    'term, some in the second.</p>'
    '<p>&#9888;&#9888; <strong>So a student who takes Organic I at one college and Organic II at '
    'another can arrive in a course that assumes NMR they were never taught, while having already '
    'covered carbonyl material the new institution is about to repeat.</strong> The credit will '
    'usually transfer; the preparation is what does not. <strong>If you must split the sequence, '
    'get the second institution&rsquo;s first-term topic list and compare it with what you actually '
    'covered</strong> — not the course titles, which are identical and tell you nothing.</p>'
    '<h3>Two packagings, and no institution carries both</h3>'
    '<table class="table table-sm"><thead><tr><th>Form</th><th>Credits</th><th>Institutions</th>'
    '</tr></thead><tbody>'
    '<tr><td><code>CHM2211</code> lecture + separate <code>CHM2211L</code> laboratory</td>'
    '<td>3 + 1</td><td><strong>29</strong></td></tr>'
    '<tr><td><code>CHM2211C</code> integrated lecture and laboratory</td><td><strong>4</strong> '
    '(Polk State 5)</td><td><strong>7</strong></td></tr>'
    '</tbody></table>'
    '<p>&#9888; Same as Organic I, and it matters for the same reason: <strong>an evaluator '
    'matching identifiers reads <code>CHM2211C</code> against a <code>CHM2211</code> requirement as '
    'a mismatch when it is the same course.</strong> Say so and send the syllabus.</p>'
    '<h3>&#9888; Credits, named by school</h3>'
    '<p>Twenty-seven institutions carry it at <strong>3 credits</strong>; <strong>Florida '
    'SouthWestern State College and Hillsborough Community College</strong> carry it at '
    '<strong>4</strong>. &#9888; <strong>FIU carries Organic I at 4 credits and this course at '
    '3</strong>, so a student completing the year at FIU has 7 lecture credits where a student '
    'elsewhere has 6 — check how your degree audit counts it.</p>'
    '<h3>Titles, and one typographical trap</h3>'
    '<p>Twenty-three institutions call it <em>Organic Chemistry II</em>, five use the Arabic '
    '<em>Organic Chemistry 2</em>, and several run <em>Honors</em> sections under the same number. '
    '&#9888; Tallahassee State College&rsquo;s catalogue records the title as '
    '<em>&ldquo;Organic Chemisty II&rdquo;</em> — a typing error in the state record, not a '
    'different course. <strong>Register by the number.</strong></p>'
    + DUAL_ENROL + GORDON,
    {'summary': 'Twenty-nine Florida public institutions carry CHM2211 as a lecture with a separate '
                'CHM2211L laboratory — 27 at 3 credits, Florida SouthWestern State and '
                'Hillsborough at 4. A further seven carry the integrated CHM2211C at 4 credits '
                '(Polk State at 5), and no institution carries both forms.',
     'hours_source': 'published', 'derived_contact_hours': 45,
     'derivation': 'PUBLISHED, not derived: Gulf Coast State College gives "Credit hours: 3 / '
                   'Lecture hours: 3" for CHM2211, which is 45 contact hours over a 15-week term. '
                   'Gulf Coast separately publishes "Credit hours: 1 / Lab hours: 3" for CHM2211L.',
     'offerings': offs([
         ('GCSC', 'Gulf Coast State College', 'Organic Chemistry II', 3, 45,
          'Publishes its hours explicitly: 3 lecture hours weekly.'),
         ('UF', 'University of Florida', 'Organic Chemistry 2', 3, None, None),
         ('USF', 'University of South Florida', 'Organic Chemistry II', 3, None, None),
         ('UCF', 'University of Central Florida', 'Organic Chemistry II', 3, None,
          'Also runs Honors Organic Chemistry II under the same number.'),
         ('UNF', 'University of North Florida', 'Organic Chemistry II', 3, None, None),
         ('UWF', 'University of West Florida', 'Organic Chemistry II', 3, None, None),
         ('FSU', 'Florida State University', 'Organic Chemistry II', 3, None, None),
         ('FAMU', 'Florida A&M University', 'Organic Chemistry II', 3, None, None),
         ('FGCU', 'Florida Gulf Coast University', 'Organic Chemistry II', 3, None, None),
         ('FAU', 'Florida Atlantic University', 'Organic Chemistry 2', 3, None,
          'Also runs an Honors section under the same number.'),
         ('FLPOLY', 'Florida Polytechnic University', 'Organic Chemistry 2', 3, None, None),
         ('FIU', 'Florida International University', 'Organic Chemistry II', 3, None,
          '⚠ Three credits here, but FOUR for Organic I — asymmetric within FIU’s own '
          'sequence.'),
         ('FSWSC', 'Florida SouthWestern State College', 'Organic Chemistry II', 4, None,
          '⚠ Four credits.'),
         ('HC', 'Hillsborough Community College', 'Organic Chemistry II', 4, None,
          '⚠ Four credits.'),
         ('BC', 'Broward College', 'Organic Chemistry II', 3, None, None),
         ('MDC', 'Miami Dade College', 'Organic Chemistry 2', 3, None, None),
         ('SPC', 'St. Petersburg College', 'Organic Chemistry II', 3, None, None),
         ('SFC', 'Santa Fe College', 'Organic Chemistry II', 3, None, None),
         ('IRSC', 'Indian River State College', 'Organic Chemistry II', 3, None, None),
         ('EFSC', 'Eastern Florida State College', 'Organic Chemistry 2', 3, None, None),
         ('PBSC', 'Palm Beach State College', 'Organic Chemistry II', 3, None, None),
         ('PESC', 'Pensacola State College', 'Organic Chemistry II', 3, None, None),
         ('TSC', 'Tallahassee State College', 'Organic Chemistry II', 3, None,
          '⚠ The state record spells the title "Organic Chemisty II" — a typing error, not '
          'a different course.'),
         ('SJRSC', 'St. Johns River State College', 'Organic Chemistry II', 3, None, None),
         ('SCFMS', 'State College of Florida, Manatee-Sarasota', 'Organic Chemistry II', 3, None,
          None),
         ('SFSC', 'South Florida State College', 'Organic Chemistry II', 3, None,
          'Also runs an Honors section.'),
         ('CF', 'College of Central Florida', 'Organic Chemistry II', 3, None,
          'Also runs an Honors section.'),
         ('FGC', 'Florida Gateway College', 'Organic Chemistry II', 3, None, None),
         ('NFC', 'North Florida College', 'Organic Chemistry II', 3, None, None),
     ])})


def main():
    for cid, g in G.items():
        io.open(os.path.join(DRAFTS, '%s_guide.json' % cid), 'w', encoding='utf-8').write(
            json.dumps(g, ensure_ascii=False, indent=1))
        print('%-9s %-26s %d cr / %d hrs | prereq %4d | html %6d | %2d offering(s)'
              % (cid, g['title'][:26], g['credits'], g['contact_hours'],
                 len(g['prerequisites']), len(g['html_content']),
                 len(g['offering_notes']['offerings'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
