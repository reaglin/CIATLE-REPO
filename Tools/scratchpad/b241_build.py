#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Batch 241 -- the majors biology pair the Biomedical Engineer path owes.

BSC2010 at 21 institutions and BSC2011 at 21: alongside the batch-239
chemistry guides these are the highest-carrier courses written in months, and
they gate every biology, pre-health and biomedical engineering student in
Florida.

⚠⚠⚠ FINDING 1 -- THE TWO-FAMILY SPLIT IS NOT A CHM QUIRK. It repeats
here, which makes it a property of Florida's GATEWAY SCIENCE SEQUENCES:

    BSC1010 / BSC1010C family   16 institutions
    BSC2010 / BSC2010C family   23 institutions
    institutions carrying BOTH   0

    1000 family: CFK DSC EFSC FAMU FAU FGCU FSWSC LSSC NFC NWFSC PBSC
                 PESC PSC SFSC UNF VC
    2000 family: BC CF FGC FIU FLPOLY FSCJ FSU GCSC HC IRSC MDC NCF PHSC
                 SCFMS SFC SJRSC SPC SSCF TSC UCF UF USF UWF

⚠ TWO INSTANCES MAKES IT A PATTERN. Both of Florida's gateway science
sequences -- general chemistry and majors biology -- run under two parallel
families at 1000 and 2000 level with no institution in both. REVIEW_QUEUE 107
covers the chemistry half.

⚠⚠ FINDING 2 -- IDENTICAL SIBLING BEHAVIOUR TO CHEMISTRY, and this is
the striking one. In BOTH sequences:

    first course   carries the (GE CORE) marker;  hs_credit = ELECTIVE
    second course  does NOT carry it;             hs_credit = SCIENCE

BSC lower-division distribution 40 ELECTIVE / 23 SCIENCE -- discriminating.

⚠⚠⚠ FINDING 3 -- IN THIS PREFIX THE `C` SUFFIX MEANS TWO DIFFERENT
THINGS, AND THE CREDIT CHECK (batch 228) IS WHAT SEPARATES THEM:

    Valencia   BSC1010 Fundamentals of Biology HONORS 4cr  vs BSC1010C 4cr
    UCF        BSC2010 General Biology HONORS 4cr          vs BSC2010C 4cr
      -> EQUAL credits, so the suffix separates HONOURS from standard
    SPC        BSC2010 3cr + BSC2010L 1cr  vs BSC2010C Honors ... with lab 4cr
    FGCU       BSC1010C 4cr integrated
      -> DIFFERENT credits, so the suffix separates lecture from integrated

⚠⚠ FINDING 4 -- FGCU SWITCHES PACKAGING MID-SEQUENCE: BSC1010C integrated
at 4 credits, then BSC1011 lecture at 3 with a SEPARATE BSC1011L at 1. A
student who took one registration for the first course must remember to make
two for the second.

⚠ CORRECTED DURING RESEARCH, and worth recording because it was nearly
published: Seminole State LOOKED like it crossed the two families (it carries
BSC2010C and BSC1011). Reading the credits and the whole set shows its live
sequence is BSC2010C -> BSC2011C; the 1000-numbers are leftovers. NO
institution crosses families. The near-miss is the batch-225 lesson: read one
institution's entries against EACH OTHER before calling a pattern.

⚠⚠ AND A BLOCK THAT WAS NOT REUSED: CHM2046, CHM2210 and CHM2211 all carry
the statewide "***WARNING: THIS IS THE (2) PART OF A SEQUENCE***" text.
BSC2011 DOES NOT -- 11 BSC numbers carry it and 010/011 are not among them.
The finished guides therefore do NOT claim a state sequence warning here.
Checked before writing, precisely because reusing it would have been an
invented citation.

⚠ CREDIT DIVERGENCE (resolve the range):
    BSC2010   3 credits at 21 institutions; 4 at New College and UCF
              (UCF's 3-credit form does not exist -- its standard is BSC2010C at 4)
    BSC2011   3 credits at ALL 21 -- state the uniformity explicitly
    BSC2010L  1 credit at 18; ⚠ 2 at Miami Dade and State College of Florida
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


FAM_1000 = ('Daytona State, Eastern Florida State, Florida A&amp;M, FAU, Florida Gulf Coast, '
            'Florida Keys, Florida SouthWestern, Lake-Sumter, North Florida College, Northwest '
            'Florida State, Palm Beach State, Pensacola State, Polk State, South Florida State, '
            'UNF and Valencia')
FAM_2000 = ('Broward, College of Central Florida, Florida Gateway, FIU, Florida Polytechnic, '
            'FSCJ, Florida State, Gulf Coast, Hillsborough, Indian River State, Miami Dade, New '
            'College, Pasco-Hernando, State College of Florida, Santa Fe, St. Johns River State, '
            'St. Petersburg, Seminole State, Tallahassee State, UCF, UF, USF and UWF')

TWO_FAMILIES = (
    '<h3>&#9888;&#9888;&#9888; Florida numbers majors biology TWO ways, and no institution '
    'carries both</h3>'
    '<p>This is the single most useful thing on this page for anyone transferring, dual-enrolled, '
    'or simply trying to find their own course in a catalogue.</p>'
    '<table class="table table-sm"><thead><tr><th>Family</th><th>Institutions</th>'
    '<th>Who uses it</th></tr></thead><tbody>'
    '<tr><td><code>BSC1010</code> / <code>BSC1011</code><br>(or the <code>C</code> forms)</td>'
    '<td><strong>16</strong></td><td>%s</td></tr>'
    '<tr><td><code>BSC2010</code> / <code>BSC2011</code><br>(or the <code>C</code> forms)</td>'
    '<td><strong>23</strong></td><td>%s</td></tr>'
    '</tbody></table>'
    '<p>&#9888;&#9888; <strong>Zero institutions carry both first courses.</strong> Same subject, '
    'same lower-division level, same majors sequence, and the credit articulates either way — '
    '<strong>but the other number does not exist at your school</strong>, so a student searching a '
    'catalogue or a degree audit for the wrong one finds nothing and concludes something has gone '
    'wrong.</p>'
    '<p>&#9888;&#9888;&#9888; <strong>And this is not a quirk of biology.</strong> Florida&rsquo;s '
    'other gateway science sequence does exactly the same thing: general chemistry runs as '
    '<code>CHM1045</code>/<code>CHM1046</code> at nineteen institutions and '
    '<code>CHM2045</code>/<code>CHM2046</code> at twenty, again with no overlap. <strong>Two of '
    'two.</strong> If you are planning a science-heavy first two years, expect to look up the '
    'local number for every gateway sequence rather than assuming the one you have seen '
    'quoted.</p>'
) % (FAM_1000, FAM_2000)

C_SUFFIX = (
    '<h3>&#9888;&#9888;&#9888; In this prefix the <code>C</code> suffix means TWO different '
    'things — check the CREDITS</h3>'
    '<p>Normally a <code>C</code> marks an integrated lecture-plus-laboratory course. In majors '
    'biology it sometimes marks that and sometimes marks <strong>honours</strong>, and the credit '
    'value is what tells them apart:</p>'
    '<table class="table table-sm"><thead><tr><th>Institution</th><th>Bare number</th>'
    '<th><code>C</code> form</th><th>What the suffix is doing</th></tr></thead><tbody>'
    '<tr><td>University of Central Florida</td><td><em>General Biology Honors</em>, <strong>4 '
    'cr</strong></td><td><em>Biology I</em>, <strong>4 cr</strong></td>'
    '<td>&#9888; <strong>equal credits → honours vs standard</strong>, not lecture vs '
    'integrated</td></tr>'
    '<tr><td>Valencia</td><td><em>Fundamentals of Biology Honors</em>, <strong>4 cr</strong></td>'
    '<td><em>General Biology I</em>, <strong>4 cr</strong></td>'
    '<td>&#9888; <strong>equal credits → honours vs standard</strong></td></tr>'
    '<tr><td>St. Petersburg College</td><td>3 cr + a separate 1-credit <code>BSC2010L</code></td>'
    '<td><em>Honors Biology I &hellip; with Lab</em>, <strong>4 cr</strong></td>'
    '<td>different credits → <strong>integrated</strong> (and honours as well)</td></tr>'
    '</tbody></table>'
    '<p>&#9888;&#9888; <strong>So do not read a <code>C</code> here as automatically meaning '
    '&ldquo;lecture plus lab in one registration&rdquo;.</strong> Compare the credit value with '
    'the bare number at the same institution: <strong>equal credits means the suffix is doing '
    'something else</strong>, and at UCF and Valencia that something else is honours. Getting this '
    'wrong means either missing a laboratory you needed or enrolling in an honours section you did '
    'not intend.</p>'
)

MIDSEQ = (
    '<h3>&#9888;&#9888; One institution changes the PACKAGING between the two courses</h3>'
    '<p><strong>Florida Gulf Coast University</strong> runs the first course as '
    '<code>BSC1010C</code>, integrated, <strong>4 credits, one registration</strong> — and the '
    'second as <code>BSC1011</code> at <strong>3 credits with a separate 1-credit '
    '<code>BSC1011L</code></strong>.</p>'
    '<p>&#9888; <strong>A student who needed one registration in the autumn needs two in the '
    'spring</strong>, and nothing announces the change. It is a small thing that costs a term when '
    'missed, because the laboratory is required and fills early. <strong>Check the packaging of '
    'the second course separately from the first, at any institution.</strong></p>'
)

DUAL_ENROL = (
    '<h3>&#9888;&#9888; Dual-enrolled students: the two halves earn DIFFERENT high-school credit</h3>'
    '<table class="table table-sm"><tbody>'
    '<tr><td>Majors Biology I (<code>BSC2010</code> / <code>BSC1010</code>)</td>'
    '<td>&#9888; <strong>ELECTIVE</strong></td></tr>'
    '<tr><td>Majors Biology II (<code>BSC2011</code> / <code>BSC1011</code>)</td>'
    '<td><strong>SCIENCE</strong></td></tr>'
    '</tbody></table>'
    '<p>&#9888; <strong>The college credit is unaffected.</strong> What differs is the high-school '
    'requirement it fills — so a student taking the first course expecting to clear a high-school '
    '<em>science</em> requirement may receive elective credit instead. Across the 63 active '
    'lower-division <code>BSC</code> numbers the field splits 40 elective to 23 science, so it '
    'genuinely discriminates and is worth checking rather than assuming.</p>'
    '<p>&#9888;&#9888; <strong>And general chemistry does exactly the same thing</strong> — '
    '<code>CHM2045</code> elective, <code>CHM2046</code> science. <strong>A dual-enrolled student '
    'taking the first half of both gateway sequences may earn no high-school science credit from '
    'either.</strong> Confirm with your counsellor and your district&rsquo;s articulation '
    'agreement before you enrol, not after.</p>'
)

GORDON = (
    '<h3>&#9888; General-education and Gordon Rule designations are set by your institution</h3>'
    '<p>Twenty-two of the 23 carriers record a <strong>natural-science general-education</strong> '
    'designation on this course, and a handful additionally record a Gordon Rule designation. '
    '&#9888; The flags in the state file reliably say that <em>a</em> designation exists without '
    'reliably saying <em>which</em>, so <strong>read your own institution&rsquo;s general-education '
    'list.</strong> Where a Gordon Rule designation does apply, remember the condition that catches '
    'people: <strong>a grade of C or higher is required for it to count, and a C&minus; does '
    'not</strong> at most institutions.</p>'
)


def guide(title, credits, hours, prereq, html, notes):
    return {'title': title, 'html_content': html, 'credits': credits, 'contact_hours': hours,
            'prerequisites': prereq, 'version': '1.0', 'offering_notes': notes}


def offs(rows):
    return [{'institution': c, 'institution_name': n, 'title': t, 'credits': cr,
             'contact_hours': ch, 'note': nt} for c, n, t, cr, ch, nt in rows]


G = {}

G['BSC2010'] = guide(
    'General Biology I (Majors)', 3, 45,
    'The statewide prerequisite field reads NONE, and in practice institutions require college-level '
    'reading and writing placement and often college algebra or a chemistry corequisite. '
    'THIS IS THE MAJORS COURSE. The separate non-majors biology sequence uses different numbers '
    'and will NOT substitute for it. '
    'WARNING - LOOK UP WHICH NUMBER YOUR SCHOOL USES. Florida numbers majors biology in TWO '
    'parallel families and NO institution carries both: 23 institutions use BSC2010 (or BSC2010C) '
    'and 16 use BSC1010 (or BSC1010C), among them Florida A&M, FAU, FGCU, UNF and Valencia. '
    'REGISTER FOR THE LABORATORY. Most carriers run a 3-credit lecture with a SEPARATE 1-credit '
    'BSC2010L, and every programme requiring this course requires the laboratory with it. '
    'CHECK THE CREDITS BEFORE READING A "C" AS INTEGRATED: at UCF and Valencia the bare number and '
    'the C form are BOTH 4 credits, because there the suffix separates HONOURS from standard rather '
    'than lecture from lab.',
    '<h2>Course Description</h2>'
    '<p><strong>General Biology I</strong> is the first course of the majors biology sequence and '
    'the gateway to every life-science degree in Florida. The statewide description covers '
    '<strong>molecular biology, cellular biology, genetics, metabolism and replication</strong>, '
    'taught through the application of the scientific method.</p>'
    '<p>Carried by <strong>23 Florida public institutions</strong>, 21 of them at 3 credits with a '
    'separate 1-credit laboratory.</p>'
    '<p>&#9888;&#9888; <strong>This is the majors course, and the distinction matters more than it '
    'sounds.</strong> Florida runs a parallel non-majors biology sequence for general-education '
    'students, and the two are not interchangeable: a programme that names this course will not '
    'accept the other, and discovering that after a year is expensive. <strong>If you intend any '
    'life-science, pre-health or biomedical engineering degree, this is the one to take.</strong></p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Articulate and apply the <strong>scientific method</strong>, and distinguish a hypothesis '
         'from a conclusion.',
         'Describe the <strong>chemical basis of life</strong> — water, macromolecules, and the '
         'properties that follow from structure.',
         'Describe <strong>cell structure and function</strong> in prokaryotes and eukaryotes, and '
         'the role of membranes.',
         'Explain <strong>metabolism and energy transfer</strong>: enzymes, cellular respiration '
         'and photosynthesis.',
         'Explain <strong>cell division</strong>, mitosis and meiosis, and their consequences for '
         'inheritance.',
         'Apply the principles of <strong>Mendelian and molecular genetics</strong>.',
         'Describe <strong>DNA replication, transcription and translation</strong>, and the '
         'regulation of gene expression.')
    + '<h3>Optional Outcomes</h3>'
    + li('Biotechnology techniques and their applications.',
         'An introduction to evolution, where the institution places it in the first term.',
         'Bioinformatics and genomics.',
         'Quantitative and statistical treatment of biological data.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('The scientific method and experimental design.',
         'Chemistry of life; water, carbon and the macromolecules.',
         'Cell structure, membranes and transport.',
         'Enzymes and metabolism; cellular respiration and photosynthesis.',
         'The cell cycle, mitosis and meiosis.',
         'Mendelian genetics and chromosomal inheritance.',
         'Molecular genetics: replication, transcription, translation, gene regulation.')
    + '<h3>Optional Topics</h3>'
    + li('Recombinant DNA and biotechnology.', 'Genomics and bioinformatics.',
         'Introduction to evolutionary mechanisms.', 'Cell signalling.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Campbell <em>Biology</em> is the near-universal text and is what most Florida programmes '
    'mean by &ldquo;the textbook&rdquo;; Freeman <em>Biological Science</em> and Raven are the '
    'common alternatives, and several colleges use the free OpenStax <em>Biology 2e</em>.</li>'
    '<li>Online homework (Mastering Biology, Achieve, Connect) is near-universal and carries an '
    'access fee separate from the book. Budget for it.</li>'
    '<li>&#9888; The laboratory has its own manual, usually written in-house, and it is the '
    'operative document for that half of the course.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>This course is named on the <strong>Biomedical Engineer</strong> career path in this '
    'repository, where it is the requirement that distinguishes that degree from every other '
    'engineering major — and it gates far more than that. Majors biology is the first course of '
    'the sequence leading to medicine, dentistry, veterinary medicine, pharmacy, physician '
    'assistant and nursing programmes, and to degrees in biology, biochemistry, microbiology, '
    'marine science and environmental science. In Florida it also feeds clinical and forensic '
    'laboratory science, biotechnology and pharmaceutical manufacturing, and the state&rsquo;s '
    'large environmental and marine research sector.</p>'
    '<h2>Special Information</h2>'
    + TWO_FAMILIES + C_SUFFIX +
    '<h3>&#9888;&#9888; The statewide title carries the &ldquo;(GE CORE)&rdquo; marker</h3>'
    '<p>The statewide title of this course ends <strong>&ldquo;(GE CORE)&rdquo;</strong>, '
    'identifying it as a Florida <strong>General Education Core</strong> course under s. 1007.25, '
    'Florida Statutes. &#9888;&#9888; <strong>That is a materially stronger transfer protection '
    'than the ordinary line</strong>: a core course satisfies its general-education subject area '
    'at <em>every</em> Florida public college and university, where the usual guarantee only '
    'promises credit at an institution offering the same course.</p>'
    '<p>&#9888; <strong>Two cautions.</strong> The protection attaches to the general-education '
    '<em>area</em>, not to the laboratory: whether a programme&rsquo;s &ldquo;science with '
    'laboratory&rdquo; requirement is satisfied is that programme&rsquo;s rule. And <strong>the '
    'second course of the sequence does not carry the marker</strong> — exactly as in general '
    'chemistry.</p>'
    '<h3>&#9888; Credits, named by school</h3>'
    '<p>Twenty-one carriers run the lecture at <strong>3 credits</strong>. <strong>New College of '
    'Florida and UCF carry it at 4.</strong> &#9888; UCF is the case to understand: its 4-credit '
    '<code>BSC2010</code> is the <em>honours</em> section and its standard course is the 4-credit '
    '<code>BSC2010C</code> — <strong>so UCF has no 3-credit version of this course at all</strong>, '
    'and a transfer student arriving there with 3 credits should ask early how it is counted.</p>'
    '<h3>&#9888; The laboratory is not uniformly one credit either</h3>'
    '<p><code>BSC2010L</code> runs at <strong>1 credit at eighteen institutions</strong> and at '
    '<strong>2 at Miami Dade College and the State College of Florida</strong>. A 1-credit '
    'laboratory typically meets for three hours a week, so it already consumes far more scheduled '
    'time than its credit value suggests; a 2-credit one more still. <strong>Plan the term around '
    'the hours, not the credits.</strong></p>'
    '<h3>Titles vary and the course does not</h3>'
    '<p>Carriers call it <em>General Biology I</em>, <em>Integrated Principles of Biology I</em> '
    '(UF and the College of Central Florida), <em>Biological Science I</em> (Florida State), '
    '<em>Biology I &ndash; Cellular Processes</em> (Hillsborough, St. Petersburg, USF), '
    '<em>Principles of Biology</em> (Miami Dade), <em>Fundamentals of Biology</em> (State College '
    'of Florida) and <em>Biology for Science Majors I</em> (Gulf Coast, Tallahassee State). '
    '&#9888; <strong>On a 23-carrier gateway course that is branding, not divergence</strong> — '
    'if your catalogue calls it something this guide does not mention, it is still this course. '
    'Register by the number.</p>' + DUAL_ENROL + GORDON,
    {'summary': 'Twenty-three Florida public institutions carry BSC2010 — 21 at 3 credits with a '
                'separate BSC2010L laboratory, and New College and UCF at 4. A further 16 '
                'institutions teach the same course as BSC1010 or BSC1010C, and no institution '
                'carries both families. No carrier publishes a contact-hour figure for the '
                'lecture.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the 3-credit value '
                   'carried by 21 of the 23. ⚠ Gulf Coast State College, one of the few '
                   'Florida institutions publishing laboratory hours, gives 3 lab hours weekly for '
                   'the equivalent majors laboratory, which supports the separate 1-credit / 45-hour '
                   'figure for BSC2010L. At New College and UCF the lecture is 4 credits and '
                   'approximately 60 contact hours.',
     'offerings': offs([
         ('UF', 'University of Florida', 'Integrated Principles of Biology I', 3, None, None),
         ('USF', 'University of South Florida', 'Biology I Cellular Processes', 3, None, None),
         ('UCF', 'University of Central Florida', 'General Biology Honors', 4, None,
          '⚠ Four credits, and it is the HONOURS section; UCF’s standard course is the '
          '4-credit BSC2010C. UCF has no 3-credit form.'),
         ('UWF', 'University of West Florida', 'Biology I', 3, None, None),
         ('FSU', 'Florida State University', 'Biological Science I', 3, None, None),
         ('FIU', 'Florida International University', 'General Biology I', 3, None, None),
         ('FLPOLY', 'Florida Polytechnic University', 'Biology 1', 3, None, None),
         ('NCF', 'New College of Florida', 'General Biology I', 4, None, '⚠ Four credits.'),
         ('BC', 'Broward College', 'General Biology', 3, None, None),
         ('MDC', 'Miami Dade College', 'Principles of Biology', 3, None,
          '⚠ Its laboratory, BSC2010L, is 2 credits rather than 1.'),
         ('SPC', 'St. Petersburg College', 'Biology I - Cellular Processes', 3, None,
          'Also carries a 4-credit BSC2010C, which is the honours section with its laboratory '
          'integrated.'),
         ('HC', 'Hillsborough Community College', 'Biology I Cellular Processes', 3, None, None),
         ('GCSC', 'Gulf Coast State College', 'Biology for Science Majors I', 3, None,
          'Also runs an honours section under the same number, and publishes its laboratory hours.'),
         ('IRSC', 'Indian River State College', 'General Biology I', 3, None, None),
         ('SFC', 'Santa Fe College', 'General Biology I', 3, None, None),
         ('TSC', 'Tallahassee State College', 'Biology for Sci Major I', 3, None, None),
         ('SJRSC', 'St. Johns River State College', 'General Biology I', 3, None,
          'Also runs an honours section under the same number.'),
         ('SCFMS', 'State College of Florida, Manatee-Sarasota', 'Fundamentals of Biology', 3,
          None, '⚠ Its laboratory, BSC2010L, is 2 credits rather than 1.'),
         ('CF', 'College of Central Florida', 'Integrated Principles of Biology I', 3, None, None),
         ('PHSC', 'Pasco-Hernando State College', 'Biology I', 3, None, None),
     ])})

G['BSC2011'] = guide(
    'General Biology II (Majors)', 3, 45,
    'General Biology I with a minimum grade of C, and its laboratory, at essentially every '
    'institution. The statewide prerequisite field is blank, which is a gap in the record rather '
    'than an open door. '
    'LOOK UP WHICH NUMBER YOUR SCHOOL USES. Florida numbers majors biology in TWO parallel families '
    'and no institution carries both first courses: 23 institutions use the BSC2010/BSC2011 family '
    'and 16 use BSC1010/BSC1011, among them Florida A&M, FAU, FGCU, UNF and Valencia. '
    'ALL 21 CARRIERS RUN IT AT 3 CREDITS, most with a separate 1-credit BSC2011L laboratory that '
    'is also required. '
    'CHECK THE SECOND COURSE PACKAGING SEPARATELY FROM THE FIRST. Florida Gulf Coast runs an '
    'INTEGRATED 4-credit first course and then a SPLIT second course, so one registration becomes '
    'two, and nothing announces the change. '
    'FINISH THE SEQUENCE WHERE YOU STARTED IT: an audit matching identifiers will not recognise '
    'a half-and-half sequence across the two families.',
    '<h2>Course Description</h2>'
    '<p><strong>General Biology II</strong> completes the majors sequence, and it changes scale. '
    'Where the first course is molecules and cells, this one is organisms, populations and the '
    'history that produced them. The statewide description covers <strong>regulation of cell '
    'metabolism, comparative plant and animal physiology, developmental biology, population biology '
    'and ecology, evolutionary biology, and applications to the clinical sciences</strong>.</p>'
    '<p>Carried by <strong>21 Florida public institutions, every one of them at 3 credits</strong>.</p>'
    '<p>&#9888; <strong>Students who did well in the first course sometimes do worse in this '
    'one</strong>, and the reason is worth knowing in advance: the first term rewards mechanism and '
    'problem-solving, and this term rewards breadth, comparison and synthesis across a very large '
    'amount of material. It is a different kind of studying, not an easier or harder one.</p>'
    '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
    + li('Explain the <strong>mechanisms of evolution</strong> — selection, drift, gene flow, '
         'speciation — and interpret phylogenetic trees.',
         'Describe the <strong>diversity of life</strong> across the domains and major kingdoms, '
         'and the characters that define the principal groups.',
         'Compare <strong>plant structure and physiology</strong>: transport, nutrition, '
         'reproduction and growth regulation.',
         'Compare <strong>animal structure and physiology</strong> across the major organ systems.',
         'Explain <strong>developmental biology</strong> from fertilisation through differentiation.',
         'Apply the principles of <strong>ecology</strong> at population, community and ecosystem '
         'level.',
         'Relate biological principles to <strong>clinical and applied contexts</strong>, which the '
         'statewide description names explicitly.')
    + '<h3>Optional Outcomes</h3>'
    + li('Conservation biology and biodiversity loss.',
         'Animal behaviour.',
         'Florida-specific ecology — wetlands, coastal and marine systems, invasive species.',
         'Quantitative ecology and population modelling.')
    + '<h2>Major Topics</h2><h3>Required Topics</h3>'
    + li('Evolutionary mechanisms; natural selection and population genetics.',
         'Phylogeny, systematics and the tree of life.',
         'Survey of biological diversity: bacteria, archaea, protists, fungi, plants, animals.',
         'Plant form, function and reproduction.',
         'Animal form and function; the organ systems.',
         'Animal development.',
         'Population, community and ecosystem ecology.')
    + '<h3>Optional Topics</h3>'
    + li('Conservation and biodiversity.', 'Animal behaviour.',
         'Global change biology.', 'Florida ecosystems and invasive species.')
    + '<h2>Resources &amp; Tools</h2><ul>'
    '<li>Campbell <em>Biology</em> continues from the first course — this term is generally the '
    'back two-thirds of the same book, which is worth knowing before selling it.</li>'
    '<li>Online homework systems continue and usually carry the same access code.</li>'
    '<li>&#9888; The laboratory is frequently more field- and specimen-based than the first '
    'term&rsquo;s, and at several Florida institutions includes work outdoors.</li>'
    '</ul>'
    '<h2>Career Pathways</h2>'
    '<p>Completing the full year is what actually satisfies the requirement. This course is named '
    'on the <strong>Biomedical Engineer</strong> career path, and the sequence gates medicine, '
    'dentistry, veterinary medicine, pharmacy, physician assistant and nursing programmes, and '
    'degrees in biology, biochemistry, microbiology, marine science and environmental science.</p>'
    '<p>&#9888; <strong>In Florida this is also the term that connects directly to the state&rsquo;s '
    'largest research and employment sector in the life sciences.</strong> Ecology, marine biology, '
    'fisheries, wetland science, invasive species management and conservation are unusually large '
    'employers here, and this is the course where a student first finds out whether that work '
    'interests them.</p>'
    '<h2>Special Information</h2>'
    + TWO_FAMILIES + MIDSEQ +
    '<h3>&#9888; Uniform credits, for once</h3>'
    '<p><strong>All 21 carriers run this course at 3 credits</strong> — worth stating plainly, '
    'because it is unusual in this catalogue and because the first course of the same sequence is '
    '<em>not</em> uniform (New College and UCF carry it at 4). Most carriers add a separate '
    '1-credit <code>BSC2011L</code>.</p>'
    '<h3>&#9888; This course does NOT carry the &ldquo;(GE CORE)&rdquo; marker</h3>'
    '<p>The first course of the sequence does; this one does not, and the same is true of general '
    'chemistry. <strong>Do not read that as a warning</strong> — fifteen of the 21 carriers record '
    'a natural-science general-education designation on it. What it means is that <strong>the '
    'statewide core protection attaching to the first course is not automatically inherited by the '
    'second</strong>, so check your own institution&rsquo;s list rather than assuming the sequence '
    'travels as a unit.</p>'
    '<h3>Titles vary and the course does not</h3>'
    '<p><em>General Biology II</em>, <em>Integrated Principles of Biology II</em> (UF, College of '
    'Central Florida), <em>Biological Science II</em> (Florida State), <em>Biology II '
    'Biodiversity</em> (Hillsborough), <em>Biodiversity</em> (USF), <em>Biology II — Organisms and '
    'Ecology</em> (St. Petersburg), <em>Principles of Biology 2</em> (Miami Dade). &#9888; '
    '<strong>Branding, not divergence</strong>, and several of the titles are more informative than '
    'the state&rsquo;s own <em>General Biology (cont.)</em>. Register by the number.</p>'
    + DUAL_ENROL +
    '<h3>&#9888; General-education and Gordon Rule designations are set by your institution</h3>'
    '<p>Fifteen of the 21 carriers record a natural-science general-education designation on this '
    'course. The state file&rsquo;s flags reliably say that <em>a</em> designation exists without '
    'reliably saying <em>which</em>, so <strong>read your own institution&rsquo;s '
    'general-education list.</strong> Where a Gordon Rule designation applies, <strong>a grade of '
    'C or higher is required for it to count and a C&minus; is not enough</strong> at most '
    'institutions.</p>',
    {'summary': 'Twenty-one Florida public institutions carry BSC2011, ALL of them at 3 credits, '
                'most with a separate 1-credit BSC2011L laboratory. A further 16 institutions '
                'teach the same course as BSC1011 or BSC1011C, and no institution carries both '
                'families of the first course. No carrier publishes a contact-hour figure.',
     'hours_source': 'derived', 'derived_contact_hours': 45,
     'derivation': 'Florida convention of 15 contact hours per credit at the uniform 3-credit '
                   'value, corroborated by Gulf Coast State College, which publishes 3 lecture '
                   'hours weekly for the equivalent majors biology course.',
     'offerings': offs([
         ('UF', 'University of Florida', 'Integrated Principles of Biology II', 3, None, None),
         ('USF', 'University of South Florida', 'Biodiversity', 3, None, None),
         ('UWF', 'University of West Florida', 'Biology II', 3, None, None),
         ('FSU', 'Florida State University', 'Biological Science II', 3, None, None),
         ('FIU', 'Florida International University',
          'General Biology II: Diversity of Life, Organisms', 3, None,
          '⚠ FIU also carries BSC1011 from the other numbering family.'),
         ('FLPOLY', 'Florida Polytechnic University', 'Biology 2', 3, None, None),
         ('BC', 'Broward College', 'Introduction to Biology II', 3, None,
          '⚠ Broward also carries BSC1011C from the other family, and its BSC2011L laboratory '
          'is recorded at 3 credits — check the schedule before planning the term.'),
         ('MDC', 'Miami Dade College', 'Principles of Biology 2', 3, None, None),
         ('SPC', 'St. Petersburg College', 'Biology II - Organisms and Ecology', 3, None, None),
         ('HC', 'Hillsborough Community College', 'Biology II Biodiversity', 3, None,
          'Also runs an honours section under the same number.'),
         ('GCSC', 'Gulf Coast State College', 'Biology for Science Majors II', 3, None,
          'Also runs an honours section under the same number.'),
         ('IRSC', 'Indian River State College', 'General Biology II', 3, None, None),
         ('SFC', 'Santa Fe College', 'General Biology 2', 3, None, None),
         ('TSC', 'Tallahassee State College', 'Biology for Science Majors II', 3, None, None),
         ('SJRSC', 'St. Johns River State College', 'General Biology II', 3, None,
          'Also runs an honours section under the same number.'),
         ('SCFMS', 'State College of Florida, Manatee-Sarasota', 'Fundamentals of Biology II', 3,
          None, None),
         ('CF', 'College of Central Florida', 'Integrated Principles of Biology II', 3, None, None),
         ('PHSC', 'Pasco-Hernando State College', 'Biology II', 3, None, None),
     ])})


def main():
    for cid, g in G.items():
        io.open(os.path.join(DRAFTS, '%s_guide.json' % cid), 'w', encoding='utf-8').write(
            json.dumps(g, ensure_ascii=False, indent=1))
        print('%-9s %-28s %d cr / %d hrs | prereq %4d | html %6d | %2d offering(s)'
              % (cid, g['title'][:28], g['credits'], g['contact_hours'],
                 len(g['prerequisites']), len(g['html_content']),
                 len(g['offering_notes']['offerings'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
