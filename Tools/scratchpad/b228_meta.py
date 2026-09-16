"""Batch 228 metadata -- BSC1010L and BSC1020L, both VISITOR GUIDE REQUESTS.

Two requests arrived 2026-09-16 and outrank the local queue (MUE deferred).
Both are 1-credit laboratories whose INTEGRATED twins already have live guides
(BSC1010C and BSC1020C were published earlier) -- so the requester had found the
C form and needed the L form. That is the split-family shape, and it is almost
certainly why these two numbers generated requests.

Contact hours are NOT the usual convention here; both are sourced or anchored:
  BSC1020L = 30  -- GCSC PUBLISHES "Lab hours: 2" (2 hrs/wk x 15)
  BSC1010L = 45  -- derived, anchored on GCSC's published 3 lab hours for the
                   equivalent majors lab in the other family (BSC2010L)
⚠ GCSC publishes 2 lab hours for the non-majors lab and 3 for the majors lab, at
the SAME 1 credit. So "1-credit L = 45" is not a safe default; the majors/
non-majors distinction is worth 15 contact hours.

*** THE HEADLINE FOR STUDENTS: the lab is a separate registration, and it is
    what makes the course a LABORATORY SCIENCE ***
The 3-credit lecture alone does not satisfy a "science with laboratory"
requirement. Proof rather than assertion, from IRSC's catalogue: MCB2010
Microbiology for Health Sciences requires "BSC 1020 AND BSC 1020L, or BSC 2010
AND BSC 2010L, or BSC 2085 AND BSC 2085L, all with grade of C or higher." Every
accepted route names a lecture AND its lab. A student holding only BSC1020 is
blocked from microbiology -- and the non-majors route IS accepted, which is good
news worth stating.

*** SECOND: the two BSC1020L carriers run the lab DIFFERENTLY ***
  IRSC -- reciprocal corequisite with BSC1020; neither can be taken alone.
  GCSC -- NO corequisite; "recommended for students with the requirement of a
          science laboratory in their program track."
⚠ So at one carrier the pairing is enforced and at the other nothing stops a
student taking the lecture alone and finding out later. Same number, opposite
protection against the very mistake the number is known for.

*** THIRD: the hs_credit INVERSION, and it is counterintuitive ***
  BSC1020 / BSC1020L (NON-MAJORS)  -> SCIENCE high-school credit
  BSC1010 / BSC1010L / BSC1010C    -> ELECTIVE
  BSC2010 family                   -> ELECTIVE
The EASIER non-majors lab fills a high-school science requirement; the HARDER
majors lab returns an elective. Both guides state it with "confirm with your
counsellor." This is the batch-227 sibling-comparison rule again: the finding
came from comparing family members, not from a prefix distribution.

*** FOURTH: (GE CORE) on the number, but the lab designation is institutional ***
The century-010 statewide title carries (GE CORE) -- the batch-202 strongest-
transfer-fact marker. ⚠ But the batch-202 caution bites exactly here: the
protection attaches to the AREA, not to a laboratory component. And the data
agrees -- only 4 of 7 BSC1010L carriers record ge_nat_sci on the LAB (FAMU, FAU,
FSWSC, PBSC yes; CFK, PESC, SSCF no). Guide says: do not assume the lab inherits
the lecture's status; ask which requirement it fills.

*** FIFTH: number fragmentation at scale on the highest-enrolment science in FL ***
Four introductory-biology families: BSC1005 (36 carriers), BSC1020 (9 lecture /
2 LAB), BSC2010 (23), BSC1010 (9). ⚠ The BSC1020 LAB gap is the student-facing
fact -- 9 institutions teach the lecture and only TWO carry the lab, so at most
institutions BSC1020 does not come with a laboratory at all.
⚠ GCSC's exclusion rule is the batch-207 SPN2210 shape: BSC1020 "cannot be used
to satisfy degree requirements by students who already have credit in BSC2010 or
BSC2011" -- taking two families may not earn credit for both, while both still
count toward Florida excess hours.

*** ANOMALIES recorded honestly rather than explained away ***
- SSCF (SEMINOLE STATE -- not State College of Florida; the batch-215 code trap
  nearly caught me) carries BSC1010L but NOT BSC1010; its majors lecture is the
  integrated BSC2010C. An orphan lab. Guide tells Seminole students to ask what
  it is for rather than guessing at a teach-out.
- VC carries BSC1010 (4cr, "Fundamentals of Biology Honors") AND BSC1010C (4cr).
  ⚠ Both 4 credits, so the suffix is NOT marking lecture-vs-integrated there --
  it is separating honours from standard. A caution on the batch-184 "same
  institution carries both forms" diagnostic: check the CREDITS before reading
  it as two shapes.
- GCSC titles BSC1020L "Human Biology" in the flat file and "Human Biology Lab"
  in its catalogue; its lecture is also "Human Biology". Register by number.

*** SOURCES: two register corrections, both significant ***
⚠⚠ FAU IS NOW A COURSEDOG SCHOOL -- school fau_banner_ethos, catalog
Zm7WidFIJix2TYXQumos, 7,127 courses dumped to fau_courses.json. The register said
"no public Coursedog catalog at that host... Stop attempting FAU." That was true
in batch 173 and is STALE. Re-run discover on a host recorded as unattached.
⚠⚠ IRSC PDF ROUTE WORKS -- catalogue PDFs served from the smartcatalogiq media
path (irsc.smartcatalogiq.com/-/media/institution/irsc/pdf-catalogs-.../Indian
River State College 2024-2025.pdf, 3.2 MB, 303 pp). Register listed IRSC as an
unexercised lead. Full descriptions, prerequisites and corequisites.
⚠ GCSC RECOVERED -- gulfcoast.edu prefix page answers 131 KB and publishes
LECTURE AND LAB HOURS plus lab fees. Second only to Broward for contact hours.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

IRSC = 'Indian River State College'
GCSC = 'Gulf Coast State College'
FAU = 'Florida Atlantic University'
FAMU = 'Florida A&M University'
PBSC = 'Palm Beach State College'
FSWSC = 'Florida SouthWestern State College'
CFK = 'The College of the Florida Keys'
PESC = 'Pensacola State College'
SSCF = 'Seminole State College of Florida'

# Shared block -- the split-family warning, which is the whole reason both of
# these were requested. Spent twice, so kept tight.
SPLIT = ('*** THIS IS THE LAB HALF OF A TWO-PART COURSE AND IT IS WHAT MAKES THE SUBJECT A '
         'LABORATORY SCIENCE: the 3-credit lecture alone does NOT satisfy a "science with lab" '
         'requirement. Two registrations, two grades. ')

NEW = {

  'BSC1010L': {
    'title': 'General Biology I Laboratory',
    'credits': 1, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'Statewide: NONE. Institutions commonly expect college-level reading and writing placement. '
      + SPLIT +
      '*** AT FAU THE PAIRING IS ENFORCED BOTH WAYS - BSC1010 lists BSC1010L and BSC1010L lists '
      'BSC1010, so neither can be taken alone. Where your institution does not enforce it, the '
      'requirement is unchanged; register for both. '
      '*** WHICH NUMBER? Florida runs majors general biology I under TWO families - BSC1010(+L) and the '
      'larger BSC2010(+L) - plus integrated 4-credit C forms of each. Same course; expect the number '
      'to change on transfer. '
      '*** 1 CREDIT, ABOUT 3 SCHEDULED HOURS A WEEK, usually one continuous block, plus prep and '
      'reports. Missing a session often cannot be made up - materials are set out for the day. '
      'Closed-toe shoes are mandatory. Expect a lab fee separate from tuition.'),
    'offering_notes': {
      'summary': ('Seven public carriers, all at 1 credit; none publishes contact hours. Twelve more '
                  'institutions carry the integrated BSC1010C (4 cr) instead, and a parallel family '
                  '(BSC2010/BSC2010L) carries the same subject at 23 more.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ('No carrier of BSC1010L publishes hours. 45 (3 lab hours weekly) is anchored on '
                     "Gulf Coast State College's PUBLISHED 3 lab hours for the equivalent majors lab "
                     'in the other numbering family (BSC2010L) - the same college publishes only 2 '
                     'for the non-majors BSC1020L, so the majors/non-majors distinction is real and '
                     'worth 15 contact hours.'),
      'offerings': [
        {'institution': 'FAU', 'institution_name': FAU,
         'title': 'Biological Principles Lab', 'credits': 1, 'contact_hours': None,
         'note': ('C. E. Schmidt College of Science. "An introduction to general laboratory '
                  'procedures to demonstrate the basic principles of biology. This is a General '
                  'Education course." COREQUISITE BSC1010, and BSC1010 lists this course in return - '
                  'the reciprocal pairing that proves the two are one course. An Honors College '
                  'version runs under the same number. Records a natural-science designation.')},
        {'institution': 'FAMU', 'institution_name': FAMU,
         'title': 'General Biology I Lab', 'credits': 1, 'contact_hours': None,
         'note': 'Records a natural-science designation. Catalogue is acalog and content-blocked.'},
        {'institution': 'PBSC', 'institution_name': PBSC,
         'title': 'Principles of Biology Lab 1', 'credits': 1, 'contact_hours': None,
         'note': 'Records a natural-science designation. Catalogue not reachable.'},
        {'institution': 'FSWSC', 'institution_name': FSWSC,
         'title': 'General Biology I Laboratory', 'credits': 1, 'contact_hours': None,
         'note': 'Records a natural-science designation. Catalogue is acalog and content-blocked.'},
        {'institution': 'CFK', 'institution_name': CFK,
         'title': 'Principles of Biology I Laboratory', 'credits': 1, 'contact_hours': None,
         'note': 'Records NO general-education designation on the lab. Catalogue not reachable.'},
        {'institution': 'PESC', 'institution_name': PESC,
         'title': 'Principles of Biology Laboratory', 'credits': 1, 'contact_hours': None,
         'note': 'Records NO general-education designation on the lab. Catalogue not reachable.'},
        {'institution': 'SSCF', 'institution_name': SSCF,
         'title': 'General Biology I Lab', 'credits': 1, 'contact_hours': None,
         'note': ('ANOMALY: Seminole State carries this laboratory but does NOT carry BSC1010. Its '
                  'majors lecture is the integrated BSC2010C (4 cr), which already contains a lab. '
                  'Students there should ask an adviser what BSC1010L is for before registering - it '
                  'may be a teach-out or programme-specific number. No designation recorded.')},
      ],
    },
  },

  'BSC1020L': {
    'title': 'Human Biology Laboratory',
    'credits': 1, 'contact_hours': 30, 'version': '1.0',
    'prerequisites': (
      'IRSC: college-level English and reading placement; COREQUISITE BSC1020 (and BSC1020 requires this '
      'lab in return). GCSC: none, and NO corequisite. ' + SPLIT +
      '*** PROOF IT MATTERS: IRSC gates Microbiology for Health Sciences on "BSC 1020 AND '
      'BSC 1020L, or BSC 2010 AND BSC 2010L, or BSC 2085 AND BSC 2085L, all with grade of C or higher." '
      'Every route names a lecture AND its lab, so the lecture alone blocks you - and this '
      'non-majors route IS accepted as an equal entry to health programmes. '
      '*** ONLY TWO PUBLIC COLLEGES CARRY THIS LAB against nine teaching the lecture, so at most '
      'institutions BSC1020 has no laboratory at all. '
      '*** Dual enrolment: this earns high-school SCIENCE credit; the majors BSC1010 family earns '
      'ELECTIVE. Confirm with your counsellor. *** GCSC: $47 fee, fall and spring only.'),
    'offering_notes': {
      'summary': ('Only TWO public carriers, both at 1 credit, against nine institutions teaching the '
                  'BSC1020 lecture. One publishes contact hours. Two further institutions package '
                  'lecture and lab as BSC1020C instead.'),
      'hours_source': 'published',
      'derived_contact_hours': 30,
      'derivation': ('SOURCED, not derived: Gulf Coast State College publishes "Credit hours: 1 / Lab '
                     'hours: 2" - 2 hours weekly over a 15-week term. Indian River State College does '
                     'not publish hours. Note the same college publishes 3 lab hours for its MAJORS '
                     'biology lab (BSC2010L), so the non-majors lab is genuinely the shorter one.'),
      'offerings': [
        {'institution': 'IRSC', 'institution_name': IRSC,
         'title': 'Introduction to Human Biology Lab', 'credits': 1, 'contact_hours': None,
         'note': ('"The laboratory component for BSC 1020, Human Biology. Lab experiences include '
                  'microscope technique, basic chemistry, cell structure, genetics and body systems '
                  'terminology." Prerequisite: must score into college-level English and reading. '
                  'COREQUISITE BSC1020, enforced in both directions. Records a natural-science '
                  'general-education designation. Together with BSC1020 it satisfies the prerequisite '
                  'for MCB2010 Microbiology for Health Sciences at a grade of C or higher.')},
        {'institution': 'GCSC', 'institution_name': GCSC,
         'title': 'Human Biology Lab', 'credits': 1, 'contact_hours': 30,
         'note': ('PUBLISHES HOURS: "Credit hours: 1 / Lab hours: 2". $47.00 lab fee. Offered FALL '
                  'AND SPRING ONLY. "Recommended for students with the requirement of a science '
                  'laboratory in their program track. Laboratory activities include the use of the '
                  'microscope, cell and tissue study, chemical aspects of cells and digestion, the '
                  'study of human organ systems with the dissection of the fetal pig, and genetics." '
                  'NO corequisite - nothing stops a student taking the lecture alone. Records NO '
                  'general-education designation on the lab itself. NOTE its lecture BSC1020 states: '
                  '"cannot be used to satisfy degree requirements by students who already have credit '
                  'in BSC2010 or BSC2011."')},
      ],
    },
  },

}


def main():
    meta = json.load(open(META, encoding='utf-8')) if os.path.exists(META) else {}
    before = len(meta)
    overlap = sorted(set(meta) & set(NEW))
    if overlap:
        print('NOTE overwriting existing meta entries: %s' % ', '.join(overlap))
    for cid, m in sorted(NEW.items()):
        n = len(m['prerequisites'])
        print('%-9s prerequisites %4d chars%s' % (cid, n, '   *** OVER 1000 ***' if n > 1000 else ''))
    meta.update(NEW)
    with open(META, 'w', encoding='utf-8') as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print('meta.json: %d -> %d entries' % (before, len(meta)))


if __name__ == '__main__':
    main()
