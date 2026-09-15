"""Batch 214 metadata -- BOT / BSC.

Contact hours follow Florida's convention: 45 for a 3-credit lecture, 60 for a
3-credit integrated C course. BSC4401L is the exception and is explained in its
own derivation -- it is an L id that is a FULL 3-credit course at UWF and a
1-credit lab at FIU (split family), so the scalar carries the 3-credit reading.

Prerequisites drafted at ~850 chars, shared blocks counted against the budget
(the batch-212 lesson).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
FIU = 'Florida International University'
UCF = 'University of Central Florida'
GCSC = 'Gulf Coast State College'
SFC = 'Santa Fe College'
FAU = 'Florida Atlantic University'

DUAL = ('UWF\'s version is DUAL-LISTED with a graduate course (%s): pace and reading sit above a '
        'typical undergraduate course, but taking the undergraduate version may BLOCK taking the '
        'graduate one for credit later - ask before enrolling if you are considering a UWF '
        'master\'s. This is a UWF Biology departmental pattern, not a quirk of one course.')

NEW = {

  'BOT4734C': {
    'title': 'Plant Biotechnology',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'WARNING: the statewide prerequisite field reads "BOT L010 OR BSC L010, CO: BOT U734L" - '
      'NONE of those is a valid SCNS course id. The L and U appear to mark lower and upper '
      'division, so it means a lower-division botany or general biology course, with an '
      'upper-division lab corequisite. Find the real prerequisite in your own catalogue; in '
      'practice expect general biology with lab at minimum and very likely genetics or cell and '
      'molecular biology, since the course assumes a molecular foundation. ALSO ASK whether you '
      'register for one course or two, since the corequisite notation sits oddly with the C '
      'suffix already implying an integrated lab. Santa Fe is an FCS college teaching a '
      '4000-level course inside a baccalaureate programme, so enrolment may be restricted.'),
    'offering_notes': {
      'summary': ('Two public carriers, both at 3 credits and both using the same title. NEITHER '
                  'catalogue was reachable - Santa Fe returns empty responses to automated '
                  'retrieval and FAU exposes no public catalogue at its catalogue host - so this '
                  'guide is written from the statewide record alone.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("Neither carrier publishes contact hours. 60 is Florida's convention for a "
                     '3-credit integrated lecture+lab (C) course, which is what the queued '
                     'identifier represents. Note tissue culture adds out-of-class time on the '
                     'biology\'s schedule rather than the timetable\'s.'),
      'offerings': [
        {'institution': 'SFC', 'institution_name': SFC,
         'title': 'Plant Biotechnology', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits. Catalogue not reachable by automated retrieval (empty responses). '
                  'An FCS institution carrying a 4000-level course, which in Florida means a '
                  'baccalaureate programme or advanced technical certificate - enrolment may be '
                  'restricted to admitted students, and transfer into a university biology major '
                  'is worth confirming in writing.')},
        {'institution': 'FAU', 'institution_name': FAU,
         'title': 'Plant Biotechnology', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits. FAU does not expose a public course catalogue at catalog.fau.edu '
                  '(the host is registered with Coursedog but has no catalog assigned), so its '
                  'description could not be read.')},
      ],
    },
  },

  'BOT4850': {
    'title': 'Medical and Medicinal Botany',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'Varies sharply by institution: UCF requires NONE, UWF requires BSC 2011/L (majors general '
      'biology with lab). That gate is the clearest signal of depth - UWF works at the level of '
      'biosynthetic pathways and phytochemical classes, UCF builds from the ground up with more '
      'history and ethnobotany. WARNING FOR YOUR DEGREE AUDIT: the statewide TITLE says "w/Lab" '
      'but the statewide DESCRIPTION says "LECTURE ONLY", the number carries no C or L suffix, '
      'UCF records ZERO lab hours, and neither carrier\'s title mentions a lab. THIS COURSE HAS '
      'NO LABORATORY - it will not satisfy a science-with-lab requirement. ' + DUAL % 'BOT 5852'),
    'offering_notes': {
      'summary': ('Both public carriers award 3 credits, but with different centres of gravity: '
                  'UCF teaches history, herbal medicine and traditional practice worldwide with '
                  'no prerequisite; UWF teaches pharmacognosy and phytochemistry gated on majors '
                  'biology. Note NEITHER leads with the toxic/psychoactive material the statewide '
                  'description names first.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture course, and it is consistent with UCF recording '
                     'labStudioFieldWorkHours = 0. The statewide title\'s "w/Lab" is an error - '
                     'the statewide description itself says LECTURE ONLY.'),
      'offerings': [
        {'institution': 'UCF', 'institution_name': UCF,
         'title': 'Medical Botany', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits, no prerequisite, ZERO laboratory/studio/field-work hours recorded. '
                  '"The medicinal properties of plants and their role in both traditional and '
                  'modern medicine; history of herbal medicine and alternative medicinal '
                  'practices around the world." A historical and ethnobotanical treatment, open '
                  'to students outside biology.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Medicinal Botany', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite BSC 2011/L. Leads with '
                  'pharmacognosy: "plant natural products continue to form the basis of many new '
                  'therapeutic treatments... a survey of phytochemicals that have proven useful '
                  'for improving human health beyond the basic use of plants as a food source." '
                  'Offered concurrently with BOT 5852 (graduate students assigned additional '
                  'work). Department of Biology.')},
      ],
    },
  },

  'BSC2311': {
    'title': 'Introduction to Oceanography and Marine Biology',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'None recorded statewide or by either carrier - open to first- and second-year students in '
      'any discipline. TWO THINGS TO CHECK BEFORE YOU COUNT IT: (1) it carries NO LABORATORY (no '
      'C or L suffix, and UWF confirms lecture only), so it satisfies a general-education science '
      'requirement but NOT the laboratory part of one - confirm your programme\'s wording. (2) '
      'UWF states "Credit not granted toward a major in Biology" - this is the general-education '
      'version, NOT the majors course, so a biology major should take the majors sequence '
      'instead. GOOD NEWS FOR DUAL-ENROLLED STUDENTS: this number carries SCIENCE high-school '
      'credit, not the usual elective - rare (24 of 272 BSC numbers) and worth confirming with '
      'your counsellor and district articulation agreement.'),
    'offering_notes': {
      'summary': ('All carriers award 3 credits and all record a natural-sciences '
                  'general-education designation. Gulf Coast State College carries both a '
                  'standard and an honours section. UWF\'s longer title (adding Oceanography) '
                  'matches the statewide DESCRIPTION better than the statewide title does - the '
                  'description leads with the chemical, physical and geological features of the '
                  'ocean.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture course with no laboratory suffix.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Introduction to Oceanography and Marine Biology', 'credits': 3,
         'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "An introduction to the chemical, '
                  'physical and geological features of the world ocean and the major groups of '
                  'living marine organisms that inhabit it." Records BOTH key facts explicitly: '
                  '"Credit not granted toward a major in Biology" and "Meets General Education '
                  'requirement in Natural Sciences." Department of Biology.')},
        {'institution': 'GCSC', 'institution_name': GCSC,
         'title': 'Introduction to Marine Biology', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits, natural-sciences general-education designation. Gulf Coast State '
                  'College carries BOTH a standard section and an HONORS section under this '
                  'number - the honours version typically adds depth, a project or seminar '
                  'discussion rather than different content.')},
      ],
    },
  },

  'BSC4303': {
    'title': 'Biogeography',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'The statewide record names the prerequisite as "ECOLOGY AND EVOLUTION" - a SUBJECT, not a '
      'course number, so you cannot look it up. Find the equivalent in your own catalogue '
      '(typically a general ecology course plus an evolution course, or a combined principles '
      'course in the majors sequence) and ask an adviser; neither carrier publishes a numbered '
      'prerequisite. The requirement is substantive rather than bureaucratic: biogeography '
      'assumes natural selection, speciation, phylogeny and community ecology and spends its time '
      'COMBINING them, so a student without that background is learning three subjects at once. '
      'Normally taken late in a biology degree. ' + DUAL % 'BSC 5305'),
    'offering_notes': {
      'summary': ('Unusually clean for this catalogue: both public carriers award 3 credits and '
                  'both use the statewide title unchanged. No title drift, no credit divergence, '
                  'no suffix disagreement. UWF\'s description is far fuller than FIU\'s, but that '
                  'is a cataloguing habit rather than a narrower course at FIU.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture course with no laboratory suffix.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Biogeography', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "Relates the principles of taxonomy, '
                  'ecology and evolution to the distribution of plants and animals" - covering '
                  'codes of taxonomic nomenclature, species concepts and speciation, paradigms '
                  'of constructing phylogenies, the geologic ages of the earth, modern '
                  'terrestrial and oceanic biodiversity and biogeographic provinces, and human '
                  'impact on extinctions and introductions. Offered concurrently with BSC 5305. '
                  'Department of Biology.')},
        {'institution': 'FIU', 'institution_name': FIU,
         'title': 'Biogeography', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits. "Current issues concerning geographic distribution of plants and '
                  'animals" - matching the statewide description exactly. College of Arts, '
                  'Sciences and Education.')},
      ],
    },
  },

  'BSC4401L': {
    'title': 'Forensic Biology',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'PCB 3063 (genetics) at BOTH carriers - a real gate, since modern forensic biology is '
      'applied molecular genetics and profile interpretation needs comfort with allele '
      'frequencies and population genetics. Revise Hardy-Weinberg and basic probability first. '
      'WARNING, THE BIG ONE: this number means different things at the two carriers. At UWF it is '
      'a COMPLETE 3-credit course. At FIU it is a 1-credit LABORATORY with BSC 4401 (3 cr '
      'lecture) as a COREQUISITE - so FIU students must register for both, for 4 credits and two '
      'grades. Transfer in either direction matches on number and not on content: send the '
      'syllabus and credit value. IF YOU WANT CRIME-LAB WORK: FBI Quality Assurance Standards '
      'require coursework in biochemistry, genetics, molecular biology AND statistics or '
      'population genetics - plan the degree around them and keep syllabi.'),
    'offering_notes': {
      'summary': ('SPLIT FAMILY, and an unusually consequential one. UWF packages the whole '
                  'subject as a single 3-credit course under the L id; FIU splits it into BSC4401 '
                  '(3 cr lecture) plus BSC4401L (1 cr lab, corequisite). Same number, 3 credits '
                  'against 1, whole subject against the practical half. Note the L suffix is NOT '
                  'doing its usual 1-credit-lab job at UWF.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("Neither carrier publishes contact hours. 60 reflects the THREE-CREDIT "
                     'reading - the fuller course, which is what the statewide description '
                     'describes and what the identifier represents at UWF - treated as '
                     'substantially laboratory-based given the L designation and the mock crime '
                     'scene work. An FIU student taking the 1-credit lab should expect far fewer '
                     'hours.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Forensic Biology', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite PCB 3063. The COMPLETE '
                  'course, standing alone with no companion lecture. "For upper level '
                  'undergraduate students interested in learning and developing entry level '
                  'skills required of a forensic serologist and DNA analyst" - collection, '
                  'maintenance and analysis of crime scene evidence; DNA profile development and '
                  'analysis; match probability statistics and interpretation; case file '
                  'maintenance and reporting; professional witness testimony. Offered '
                  'concurrently with BSC 5406L. Department of Biology.')},
        {'institution': 'FIU', 'institution_name': FIU,
         'title': 'Forensic Biology Lab', 'credits': 1, 'contact_hours': None,
         'note': ('1 credit - the LABORATORY ONLY. "Will introduce students to lab techniques and '
                  'processes that are commonly encountered in Molecular or Forensic labs such as '
                  'Chain of Custody, Serology and DNA Analysis." Prerequisite PCB 3063; '
                  'COREQUISITE BSC 4401 or permission of instructor. The paired lecture BSC 4401 '
                  '"Principles of Forensic Biology" is a separate 3-credit course covering the '
                  'molecular techniques and DNA profile generation. College of Arts, Sciences '
                  'and Education.')},
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
    meta.update(NEW)
    with open(META, 'w', encoding='utf-8') as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print('meta.json: %d -> %d entries' % (before, len(meta)))
    for k in sorted(NEW):
        p = NEW[k]['prerequisites'] or ''
        flag = '  <-- OVER 1000' if len(p) > 1000 else ''
        print('  %-9s %d cr  %4d hrs  prereq %4d chars%s'
              % (k, NEW[k]['credits'], NEW[k]['contact_hours'], len(p), flag))


if __name__ == '__main__':
    main()
