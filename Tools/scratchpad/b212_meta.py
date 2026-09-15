"""Batch 212 metadata -- the ATF/ATT flight-instructor family.

Merges nine entries into scratchpad/meta.json, preserving what is already there.

Contact-hour policy for this batch, stated once here and explained in every guide:
  * ATT (classroom) courses -- Florida's 3-credit convention, 45 hours. FSCJ
    PUBLISHES 45 for ATT1110 and for the related ATT2131, so this is corroborated.
  * ATF (flight) courses -- hours are hours in an aircraft, sold by the hour, so
    the Florida 1:15 convention is meaningless (the batch-200 ATF1100L precedent).
    Use the documented flight + ground training totals where a source states them.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
PSC = 'Polk State College'
NWFSC = 'Northwest Florida State College'
FSCJ = 'Florida State College at Jacksonville'

CHOICE = ('WARNING: a lower-level alternate (%s) exists and the state record says students '
          'MUST CHOOSE. This upper-division version earns upper-division credit a bachelor '
          'degree requires, plus more aviation credit hours — the quantity 14 CFR 61.160 uses '
          'for reduced restricted-ATP thresholds (1,000 hrs with 60 credits, 1,250 with 30, '
          'vs 1,500).')

NEW = {

  'ATF3502L': {
    'title': 'Certified Flight Instructor: Flight (CFI) — Upper-Level Course',
    'credits': 3, 'contact_hours': 31, 'version': '1.0',
    'prerequisites': (
      'FAA Commercial Pilot Certificate required to enrol; current FAA medical certificate; the '
      'flight instructor spin training endorsement is required for an airplane instructor '
      'rating. Ground half (ATT3134, or ATT2130/ATT2131) first or concurrent: the FAA '
      'Fundamentals of Instructing and Flight Instructor-Airplane knowledge tests gate the '
      'practical test. Non-US citizens must obtain TSA Alien Flight Student Program clearance '
      'BEFORE flight training begins — start it early. Flight hours are FAA syllabus MINIMUMS; '
      'additional hours are billed to the student, not covered by the course fee. '
      + CHOICE % 'ATF2500/ATF2500L'),
    'offering_notes': {
      'summary': ('Two public carriers, and they diverge 3:1 on credit. UWF awards 3 credits '
                  'and requires a minimum of 25 hours of logged flight training; Polk State '
                  'awards 1. The FAA requirement is identical at both. Polk State also carries '
                  'the lower-level alternate ATF2500L, at 1 credit, so the state-mandated '
                  'choice is live there.'),
      'hours_source': 'derived',
      'derived_contact_hours': 31,
      'derivation': ('Neither carrier publishes contact hours. 25 hours of flight training '
                     '(UWF states this minimum explicitly) plus approximately 6 hours of '
                     'ground and briefing time, which NWFSC (25 + 6) and FSCJ (25 + 6.25) '
                     'both document for the identical FAA course. A floor, not an estimate: '
                     'FAA syllabus minimums are routinely exceeded.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Certified Flight Instructor: Flight', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Built to 14 CFR Part 141 Appendix F '
                  'and the Flight Instructor ACS. Minimum 25 hours of flight training logged; '
                  'all FAR-required training in an FAA Part 141 flight school. Commercial '
                  'Pilot Certificate required to enrol. Housed in the College of Business, '
                  'Department of Commerce.')},
        {'institution': 'PSC', 'institution_name': PSC,
         'title': 'Advanced Flight Instructor – Airplane', 'credits': 1, 'contact_hours': None,
         'note': ('1 credit — one third of UWF\'s award for the same FAA certificate. Polk '
                  'State also carries the lower-level alternate ATF2500L at 1 credit, so the '
                  'upper-level version costs the same credit there and differs only in '
                  'division and added coursework. Polk State\'s catalogue does not serve '
                  'course descriptions to automated retrieval, so its own description could '
                  'not be read.')},
      ],
    },
  },

  'ATF3511L': {
    'title': 'Multiengine Flight Instructor (MEI) — Upper-Level Course',
    'credits': 3, 'contact_hours': 20, 'version': '1.0',
    'prerequisites': (
      'FAA Commercial Pilot Certificate WITH a multi-engine rating, plus an existing Certified '
      'Flight Instructor Certificate (UWF states both); current FAA medical certificate. '
      'Normally follows ATF3502L or ATF2500/ATF2500L. Non-US citizens must obtain TSA Alien '
      'Flight Student Program clearance BEFORE flight training begins. Flight hours are FAA '
      'syllabus MINIMUMS and additional hours are billed to the student; twin time is the most '
      'expensive flying in the curriculum, so a small overrun costs more here. Check whether '
      'the practical test is included — for the lower-level alternate the state record says it '
      'is not. ' + CHOICE % 'ATF2510L'),
    'offering_notes': {
      'summary': ('Two public carriers, diverging 3:1 on credit: UWF 3, Polk State 1. The '
                  'flight requirement also differs — UWF requires a minimum of 15 hours where '
                  'the lower-level alternate is built on 10 hours dual. Polk State carries '
                  'both versions at 1 credit each.'),
      'hours_source': 'derived',
      'derived_contact_hours': 20,
      'derivation': ('Neither carrier publishes contact hours for this number. Florida\'s '
                     'statewide record for the lower-level alternate states "20 contact hours; '
                     '1.0 credits" (10 h dual + 10 h ground, confirmed by NWFSC); UWF\'s '
                     'upper-level version raises the flight minimum to 15 hours. 20 is the '
                     'documented figure for the course family and is a floor.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Multiengine Flight Instructor', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Built to 14 CFR Part 141 and the '
                  'Airman Certification Standards. Minimum 15 hours of flight training logged. '
                  'Requires a Commercial Pilot Certificate with multi-engine rating AND a '
                  'Certified Flight Instructor Certificate. College of Business, Department of '
                  'Commerce.')},
        {'institution': 'PSC', 'institution_name': PSC,
         'title': 'Advanced Flight Instructor – Multi-Engine', 'credits': 1,
         'contact_hours': None,
         'note': ('1 credit. Polk State also carries the lower-level alternate ATF2510L at 1 '
                  'credit. Catalogue content is not reachable by automated retrieval; title '
                  'and credit value are from the SCNS flat file.')},
      ],
    },
  },

  'ATF3531L': {
    'title': 'Instrument Flight Instructor: Flight (CFII) — Upper-Level Course',
    'credits': 3, 'contact_hours': 20, 'version': '1.0',
    'prerequisites': (
      'FAA Commercial Pilot Certificate and an existing Certified Flight Instructor Certificate '
      'required to enrol (UWF states both); instrument rating and current FAA medical '
      'certificate. Built to 14 CFR Part 141 Appendix G. The ground half (ATT3134, or ATT2130 / '
      'ATT2131) and the FAA Flight Instructor Instrument knowledge test come first. Non-US '
      'citizens must obtain TSA Alien Flight Student Program clearance BEFORE training begins. '
      'Flight hours are FAA syllabus MINIMUMS and extra hours are billed to the student — but '
      'ask how much may be flown in an approved training device, which changes the cost '
      'materially. ' + CHOICE % 'ATF2530L'),
    'offering_notes': {
      'summary': ('Two public carriers diverging 3:1 on credit: UWF 3 (minimum 15 hours of '
                  'logged flight training), Polk State 1. Polk State carries the lower-level '
                  'alternate ATF2530L at 1 credit as well.'),
      'hours_source': 'derived',
      'derived_contact_hours': 20,
      'derivation': ('No Florida institution publishes contact hours for either version of this '
                     'course — the weakest derivation in this batch, and labelled as such in '
                     'the guide. Combines UWF\'s stated 15-hour flight minimum with roughly 5 '
                     'hours of ground and briefing time, following the flight:ground proportion '
                     'NWFSC and FSCJ document for the sibling flight-instructor courses. A '
                     'floor.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Instrument Flight Instructor: Flight', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Built to 14 CFR Part 141 Appendix G '
                  'and the Airman Certification Standards. Minimum 15 hours of flight training '
                  'logged. Commercial Pilot Certificate AND Flight Instructor Certificate '
                  'required to enrol. College of Business, Department of Commerce.')},
        {'institution': 'PSC', 'institution_name': PSC,
         'title': 'Advanced Flight Instructor – Instrument', 'credits': 1, 'contact_hours': None,
         'note': ('1 credit. Also carries the lower-level alternate ATF2530L at 1 credit. '
                  'Catalogue content not reachable by automated retrieval.')},
      ],
    },
  },

  'ATT1110': {
    'title': 'Commercial Pilot Ground School',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'No formal prerequisite is stated in Florida\'s course record, but the course assumes '
      'private pilot knowledge and normally follows the private pilot ground school (ATT1100, '
      'ATT1102/ATT1103 or ATT2100). FSCJ requires students to be enrolled in, or to have '
      'completed, this course BEFORE beginning commercial flight training (ATF2201-2203, '
      'ATF2204L/ATF2205L or ATF2214L). NOTE the course prepares for the FAA Commercial '
      'Pilot-Airplane Knowledge Test but does not include it: the test is taken separately, for '
      'a fee, and the result EXPIRES — if the practical test is not completed within the '
      'validity window the knowledge test must be retaken. Ask whether a passing result is '
      'required for course credit. The same statewide course is numbered ATT2110 at five other '
      'Florida public institutions.'),
    'offering_notes': {
      'summary': ('Both public carriers agree completely — 3 credits, and the identical title '
                  '"Commercial Pilot Ground School" at each. FSCJ publishes 45 contact hours. '
                  'Note the statewide title is the older "Commercial Pilot Flight Theory"; the '
                  'carriers use the industry name for the same course.'),
      'hours_source': 'published',
      'derived_contact_hours': None,
      'derivation': ('FSCJ publishes 45 contact hours, matching Florida\'s convention for a '
                     '3-credit lecture course. UWF does not publish a figure. Published, not '
                     'derived.'),
      'offerings': [
        {'institution': 'FSCJ', 'institution_name': FSCJ,
         'title': 'Commercial Pilot Ground School', 'credits': 3, 'contact_hours': 45,
         'note': ('Publishes 45 contact hours, 3 academic-progress hours and 3 financial-aid '
                  'hours. Classroom instruction required for Commercial Pilot flight training '
                  'and the FAA Commercial Pilot-Airplane Knowledge Test; students must be '
                  'enrolled in or have completed it before beginning commercial flight '
                  'training.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Commercial Pilot Ground School', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Built to 14 CFR Part 141 Appendix D. '
                  'Covers aviation decision making and risk management, aerodynamics, aircraft '
                  'systems, FAR parts 61 and 91, NTSB 430, advanced weather, navigation, '
                  'weight and balance, safety management systems and aircraft performance. '
                  'College of Business, Department of Commerce.')},
      ],
    },
  },

  'ATT3134': {
    'title': 'Certified Flight Instructor: Ground — Upper-Level Course',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'FAA Commercial Pilot Certificate required to enrol. Follows the commercial ground school '
      '(ATT1110/ATT2110) and usually the instrument one (ATT1120/ATT2120); normally taken with '
      'or just before the flight half (ATF3502L, or ATF2500/ATF2500L). Prepares for the FAA '
      'Fundamentals of Instructing and Flight Instructor-Airplane knowledge tests, and the state '
      'record says students also obtain FAA ADVANCED GROUND INSTRUCTOR certification — a '
      'permanent credential needing no medical and no aircraft. Tests are taken separately for a '
      'fee and results EXPIRE. ' + CHOICE % 'ATT2130'),
    'offering_notes': {
      'summary': ('Both public carriers agree at 3 credits. The statewide description is the '
                  'lower-level course\'s description word for word plus two sentences adding '
                  'mentorship/coached practice and FAA Advanced Ground Instructor '
                  'certification. Polk State carries both versions at 3 credits each, so the '
                  'upper-level version costs no extra credit there and adds a federal '
                  'credential.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ('Neither carrier publishes contact hours. 45 is Florida\'s convention for '
                     'a 3-credit classroom course, corroborated by the 45 FSCJ publishes for '
                     'the closely related ATT2131 flight-instructor ground school.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Certified Flight Instructor: Ground', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Built to 14 CFR Part 141 Appendix F. '
                  'Covers aviation decision making and risk management, aerodynamics, aircraft '
                  'systems, FAR parts 61 and 91, NTSB 430, weather, navigation, weight and '
                  'balance, performance, and fundamentals of instruction and learning. '
                  'Commercial Pilot Certificate required to enrol. College of Business, '
                  'Department of Commerce.')},
        {'institution': 'PSC', 'institution_name': PSC,
         'title': 'Applications in Aviation Instruction', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits, following the statewide title. Also carries the lower-level '
                  'alternate ATT2130 at 3 credits. Catalogue content not reachable by '
                  'automated retrieval.')},
      ],
    },
  },

  'ATF2500L': {
    'title': 'Certified Flight Instructor: Flight (CFI) — Lower-Level Course',
    'credits': 1, 'contact_hours': 31, 'version': '1.0',
    'prerequisites': (
      'FAA Commercial Pilot Certificate and a current FAA medical certificate; the flight '
      'instructor spin training endorsement is required for an airplane instructor rating. The '
      'ground half (ATT2130 or ATT2131) is normally taken first or concurrently, because the '
      'FAA Fundamentals of Instructing and Flight Instructor-Airplane knowledge tests are '
      'prerequisites to the practical test. Non-US citizens must obtain TSA Alien Flight Student '
      'Program clearance BEFORE flight training begins. NWFSC expects students to fly at least '
      'three times a week and states that flight hours are FAA syllabus MINIMUMS whose overrun '
      'is NOT covered by the course fee. WARNING: this is the LOWER-LEVEL alternate — an '
      'upper-division version (ATF3502L) exists, earns upper-division credit that a bachelor '
      'degree requires, and carries 3 credits at UWF against 1 here.'),
    'offering_notes': {
      'summary': ('Both public carriers award 1 credit. NWFSC documents the training precisely: '
                  '25 hours of dual flight instruction plus 6 hours of ground. The same FAA '
                  'certificate is awarded 2 credits under ATF2500 at Broward and FSCJ, and 3 '
                  'credits under ATF3502L at UWF — four credit values, one federal requirement '
                  'of 25 flight hours.'),
      'hours_source': 'published',
      'derived_contact_hours': None,
      'derivation': ('NWFSC documents 25 hours of dual flight instruction plus 6 hours of '
                     'ground instruction and pre-/post-flight briefings = 31. FSCJ documents '
                     '25 + 6.25 for the equivalent ATF2500. A published floor: NWFSC states '
                     'explicitly that students often exceed FAA syllabus minimums.'),
      'offerings': [
        {'institution': 'NWFSC', 'institution_name': NWFSC,
         'title': 'Certified Flight Instructor I', 'credits': 1, 'contact_hours': 31,
         'note': ('1 credit. 25 hours dual flight instruction + 6 hours ground instruction and '
                  'briefings with an FAA-approved instructor. Course requirements met when the '
                  'student earns the CFI certificate for airplanes. States that hours are '
                  'FAA-syllabus minimums, that students often exceed them, and that the cost of '
                  'additional flight hours is NOT covered by the course fee. Students expected '
                  'to fly at least three times a week, not counting Sundays. The roman numeral '
                  'in the title is a local naming habit — this is not part of a sequence.')},
        {'institution': 'PSC', 'institution_name': PSC,
         'title': 'Flight Instructor', 'credits': 1, 'contact_hours': None,
         'note': ('1 credit, following the statewide title. Polk State also carries the '
                  'upper-level alternate ATF3502L, also at 1 credit. Catalogue content not '
                  'reachable by automated retrieval.')},
      ],
    },
  },

  'ATF2510L': {
    'title': 'Flight Instructor: Multi-Engine (MEI) — Lower-Level Course',
    'credits': 1, 'contact_hours': 20, 'version': '1.0',
    'prerequisites': (
      'FAA Commercial Pilot Certificate with a multi-engine rating, an existing Certified Flight '
      'Instructor Certificate, and a current FAA medical certificate. Florida\'s course record '
      'lists ATF2501 and ATT2131 as co-requisites at some institutions; normally follows '
      'ATF2500L or ATF2500. Non-US citizens need TSA Alien Flight Student Program clearance '
      'BEFORE training begins. WARNING: the state record states this course DOES NOT INCLUDE '
      'THE CHECKRIDE — scheduling and paying for the MEI practical test is the student\'s '
      'responsibility, so the course can be completed without the rating being obtained. Flight '
      'hours are FAA minimums and overruns are billed to the student; twin time is the most '
      'expensive flying in the curriculum. An upper-division alternate (ATF3511L) exists, '
      'requires 15 rather than 10 flight hours, and carries 3 credits at UWF.'),
    'offering_notes': {
      'summary': ('Both public carriers award 1 credit, and this is one of the few flight '
                  'courses in the Florida catalogue whose contact hours the STATE publishes: '
                  '"20 contact hours; 1.0 credits". NWFSC\'s breakdown of 10 hours dual plus 10 '
                  'hours ground matches exactly.'),
      'hours_source': 'published',
      'derived_contact_hours': None,
      'derivation': ('Florida\'s statewide course record states "20 CONTACT HOURS; 1.0 CREDITS" '
                     'explicitly, and NWFSC documents 10 hours dual instruction + 10 hours '
                     'ground instruction. Published and corroborated — but still an FAA '
                     'syllabus minimum, routinely exceeded.'),
      'offerings': [
        {'institution': 'NWFSC', 'institution_name': NWFSC,
         'title': 'Certified Flight Instructor Multiengine', 'credits': 1, 'contact_hours': 20,
         'note': ('1 credit. 10 hours dual instruction from an FAA-approved instructor in a '
                  'four-place airplane + 10 hours ground instruction. Offered fall, spring and '
                  'summer. After completion the student is eligible for the FAA Flight '
                  'Instructor Multiengine checkride — the course does NOT include it. States '
                  'that hours are FAA-syllabus minimums and that additional flight-hour cost is '
                  'not covered by the course fee.')},
        {'institution': 'PSC', 'institution_name': PSC,
         'title': 'Flight Instructor: Multi-Engine', 'credits': 1, 'contact_hours': None,
         'note': ('1 credit, following the statewide title. Also carries the upper-level '
                  'alternate ATF3511L at 1 credit. Catalogue content not reachable by '
                  'automated retrieval.')},
      ],
    },
  },

  'ATF2530L': {
    'title': 'Flight Instructor: Instrument (CFII) — Lower-Level Course',
    'credits': 1, 'contact_hours': 20, 'version': '1.0',
    'prerequisites': (
      'FAA Commercial Pilot Certificate with an instrument rating, an existing Certified Flight '
      'Instructor Certificate, and a current FAA medical certificate. Built to 14 CFR Part 141 '
      'Appendix G. The ground half (ATT2130 or ATT2131) and the FAA Flight Instructor Instrument '
      'knowledge test come first. Non-US citizens need TSA Alien Flight Student Program '
      'clearance BEFORE training begins. Flight hours are FAA syllabus MINIMUMS and overruns are '
      'billed to the student — but ask how much may be flown in an approved training device, '
      'which changes the cost materially. NOTE: NWFSC\'s catalogue entry for this course carries '
      'the WRONG description (it prints the single-engine CFI text); rely on the course number '
      'and your own syllabus. An upper-division alternate (ATF3531L) exists and carries 3 '
      'credits at UWF against 1 here.'),
    'offering_notes': {
      'summary': ('Both public carriers award 1 credit. No Florida institution publishes contact '
                  'hours for either version. NWFSC\'s catalogue description for this number is '
                  'erroneous — it reproduces the single-engine CFI text — so the course is '
                  'identified from its number and the statewide record.'),
      'hours_source': 'derived',
      'derived_contact_hours': 20,
      'derivation': ('No published figure exists for either version. Follows the shape the '
                     'state and NWFSC document for the multi-engine instructor course at the '
                     'same credit value (state: "20 contact hours; 1.0 credits"), and is '
                     'consistent with UWF\'s 15-hour flight minimum for the upper-level '
                     'alternate. The weakest derivation in this batch, and labelled as such in '
                     'the guide.'),
      'offerings': [
        {'institution': 'NWFSC', 'institution_name': NWFSC,
         'title': 'Certified Flight Instructor Instrument', 'credits': 1, 'contact_hours': None,
         'note': ('1 credit. ⚠ DATA-QUALITY NOTE: the catalogue entry under this title prints '
                  'the description for the single-engine airplane CFI course, referring to the '
                  '"Certified Flight Instructor Airplane Certificate" and the "Flight Instructor '
                  'Airplane Single Engine Practical Exam". Treated as a copy-and-paste error in '
                  'the catalogue, not a statement about the course.')},
        {'institution': 'PSC', 'institution_name': PSC,
         'title': 'Flight Instructor – Instrument', 'credits': 1, 'contact_hours': None,
         'note': ('1 credit, following the statewide title. Also carries the upper-level '
                  'alternate ATF3531L at 1 credit. Catalogue content not reachable by '
                  'automated retrieval.')},
      ],
    },
  },

  'ATT2130': {
    'title': 'Fundamentals of Aviation Instruction — Lower-Level Course',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'Florida\'s course record states no formal prerequisite, but the course assumes commercial '
      'pilot knowledge and the related courses elsewhere require an FAA Commercial Pilot '
      'Certificate. Follows the commercial ground school (ATT1110 or ATT2110) and usually the '
      'instrument ground school (ATT1120 or ATT2120); normally taken with or immediately before '
      'the flight half (ATF2500L or ATF2500). Prepares for the FAA Fundamentals of Instructing '
      'and Flight Instructor-Airplane knowledge tests, which are taken separately for a fee and '
      'whose results EXPIRE. SINGLE-INSTITUTION COURSE: only Polk State College carries it, and '
      'its catalogue was not reachable, so treat this guide as an account of the statewide '
      'course rather than of Polk State\'s syllabus. An upper-division alternate (ATT3134) '
      'exists at the SAME 3 credits and additionally confers FAA Advanced Ground Instructor '
      'certification.'),
    'offering_notes': {
      'summary': ('A single-institution course: Polk State College only, at 3 credits. Polk '
                  'State also carries the upper-level alternate ATT3134 at the same 3 credits, '
                  'and that version additionally confers the FAA Advanced Ground Instructor '
                  'certificate — so the choice between them costs no credit and the upper-level '
                  'version adds a permanent federal credential plus upper-division standing.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ('Polk State does not publish contact hours and its catalogue does not serve '
                     'course descriptions to automated retrieval. 45 is Florida\'s convention '
                     'for a 3-credit classroom course, corroborated by the 45 FSCJ publishes '
                     'for the closely related ATT2131 flight-instructor ground school.'),
      'offerings': [
        {'institution': 'PSC', 'institution_name': PSC,
         'title': 'Fundamentals of Aviation Instruction', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits, matching the statewide title. The only Florida public carrier. '
                  'Catalogue content not reachable by automated retrieval, so the guide is '
                  'written from Florida\'s statewide course record and the closely related '
                  'ATT2131 at FSCJ, MDC and NWFSC. Polk State\'s aviation programme is at '
                  'Lakeland Linder International Airport.')},
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
    print('meta.json: %d -> %d entries (+%d)' % (before, len(meta), len(meta) - before))
    for k in sorted(NEW):
        p = NEW[k]['prerequisites']
        flag = '  <-- OVER 1000' if p and len(p) > 1000 else ''
        print('  %-9s %d cr  %4d hrs  prereq %4d chars%s'
              % (k, NEW[k]['credits'], NEW[k]['contact_hours'], len(p or ''), flag))


if __name__ == '__main__':
    main()
