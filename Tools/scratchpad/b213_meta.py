"""Batch 213 metadata -- BCN, completing that prefix's queue.

Contact hours: Florida's convention, since these are classroom/studio courses
(unlike batch 212's flight courses). 45 for a 3-credit lecture, 60 for a
3-credit integrated C course -- and for a queued C id the C form's hours are
what the identifier represents (batch 189).

Prerequisites drafted at ~850 chars per the batch-209 rule, counting any shared
block against the budget (the batch-212 lesson).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
FIU = 'Florida International University'
UF = 'University of Florida'
FGCU = 'Florida Gulf Coast University'
FAMU = 'Florida A&M University'
SSCF = 'Seminole State College of Florida'

ACCE = ('Construction management accreditation (ACCE) is PROGRAMMATIC, not course-by-course, '
        'so transferable courses do not by themselves make an accredited degree - confirm in '
        'writing with a receiving programme.')

NEW = {

  'BCN2210': {
    'title': 'Construction Materials',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'None recorded statewide and none listed by either carrier, so the course is accessible '
      'early - and it should be taken early, because estimating, scheduling and structures all '
      'assume it. NOTE the same subject runs under THREE Florida numbers: BCN1210 (lecture, '
      'lower division), BCN1210C (integrated lab, the most common form) and BCN2210 (this '
      'course). All three are lower division, so credit transfers transparently; what varies is '
      'requirement matching and whether a LABORATORY component is included, which a non-C '
      'version does not have. Keep your syllabus and raise the match with an adviser rather '
      'than at a graduation audit. ' + ACCE),
    'offering_notes': {
      'summary': ('Both public carriers award 3 credits and teach the same course. UWF organises '
                  'it around the 16 CSI MasterFormat divisions and the "means and methods" '
                  'framing; FIU works material by material. A difference of organising '
                  'principle, not of subject.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture course with no C or L suffix.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Construction Materials', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Organised around the 16 divisions of '
                  'the Construction Specifications Institute; explicitly covers changing '
                  'materials, methods and technologies and the "means and methods" of '
                  'construction. Department of Civil Engineering and Construction Management, '
                  'College of Science and Engineering.')},
        {'institution': 'FIU', 'institution_name': FIU,
         'title': 'Construction Materials and Methods', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits. "The origins, production and uses of construction materials such '
                  'as concrete, steel, aluminum, wood, brick, and stone", examining structural '
                  'and non-structural, interior and exterior materials and assemblies. College '
                  'of Engineering and Computing.')},
      ],
    },
  },

  'BCN2251C': {
    'title': 'Construction Drawings',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'None recorded statewide or by either carrier. Take it early - estimating depends entirely '
      'on drawing literacy. WARNING: the STATEWIDE description is visibly out of date (it names '
      'drafting instruments and freehand lettering, and is residential in emphasis); UWF\'s own '
      'description is current and commercial, framing the purpose as interpreting commercial '
      'construction documents. ASK WHETHER YOUR SECTION INCLUDES CAD - Florida programmes '
      'differ, and if it does not, learn Bluebeam and basic AutoCAD independently because '
      'employers assume both. The same subject also runs as BCN1251 and BCN1251C at fourteen '
      'other institutions; all are lower division so credit transfers, but check whether a '
      'receiving programme expects the LABORATORY component. ' + ACCE),
    'offering_notes': {
      'summary': ('Both public carriers award 3 credits. Seminole State\'s title "Building '
                  'Construction Documents" is arguably the most accurate of the three, since '
                  'the contract documents include the specifications the drawings reference. '
                  'Seminole State also carries BCN1251, suggesting it runs the subject in two '
                  'shapes.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("Neither carrier publishes contact hours. 60 is Florida's convention for a "
                     '3-credit integrated lecture+lab (C) course, which is what the queued '
                     'identifier represents. Expect roughly four hours a week of class and '
                     'studio, not three.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Construction Drawings', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "Provides basic working knowledge of '
                  'architectural graphics, practice in instrumental drawing and experience in '
                  'free hand sketching", with the stated purpose of accurately interpreting '
                  'COMMERCIAL construction documents; addresses drawing quality, drafting '
                  'techniques, and drawing literacy and information retrieval. Department of '
                  'Civil Engineering and Construction Management.')},
        {'institution': 'SSCF', 'institution_name': SSCF,
         'title': 'Building Construction Documents', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits. Catalogue description not retrieved for this guide. Seminole State '
                  'also carries BCN1251 (lecture-only, lower division).')},
      ],
    },
  },

  'BCN3281C': {
    'title': 'Construction Surveying and Building Layout',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'UWF requires MAC 1114 (trigonometry) OR MAC 2233 OR MAC 2311; UF requires junior standing. '
      'THE MATHEMATICS GATE IS REAL - surveying IS applied trigonometry (traverse computation, '
      'latitudes and departures, bearings, indirect elevation), so acquire trigonometry even '
      'where it is not required. Calculus is NOT what this course needs. Normally follows '
      'construction drawings, since layout is performed from documents. UWF states credit cannot '
      'be received for both BCN 3281C and BCN 3282C. WARNING: UF awards 2 credits against UWF\'s '
      '3 - check the value your programme expects. This course does NOT lead to Professional '
      'Surveyor and Mapper licensure; boundary work is reserved by statute to licensed '
      'surveyors.'),
    'offering_notes': {
      'summary': ('All carriers teach SURVEYING, but UF\'s title does not say so: UF calls it '
                  '"Construction Methods Laboratory" while its own catalogue description is the '
                  'statewide surveying text verbatim. A title problem, not a subject divergence. '
                  'Real divergence is in CREDITS - UF 2, UWF 3. FIU carries the subject as '
                  'BCN3281 without the C suffix.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("Neither carrier publishes contact hours. 60 is Florida's convention for a "
                     '3-credit integrated lecture+lab (C) course, matching UWF\'s credit value '
                     'and the queued identifier. A field course takes more scheduled time than '
                     'its credits suggest.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Construction Survey and Building Layout', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite MAC 1114 OR MAC 2233 OR '
                  'MAC 2311. "Application of surveying skills required in the field of '
                  'construction, including building layout, indirect determination of elevation '
                  'and distance, referencing, establishment of grade, and topographic mapping." '
                  'Instruments include transit and automatic level. Credit cannot be received '
                  'for both BCN 3281C and BCN 3282C. Department of Civil Engineering and '
                  'Construction Management.')},
        {'institution': 'UF', 'institution_name': UF,
         'title': 'Construction Methods Laboratory', 'credits': 2, 'contact_hours': None,
         'note': ('2 credits - one fewer than UWF. Prerequisite junior status or higher. '
                  'WARNING: the TITLE misdescribes the course. UF\'s own description reads '
                  '"Construction aspects of surveying with field and classroom exercises in the '
                  'use of transit, level, chain, and related equipment" - the statewide '
                  'surveying description word for word. A UF student scanning for a surveying '
                  'requirement may not realise they have taken it; send the description, not '
                  'the title.')},
      ],
    },
  },

  'BCN3590': {
    'title': 'Sustainable Construction',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'None recorded statewide or by UWF, so it is accessible across the upper division, though '
      'it makes more sense after construction materials and alongside the estimating and project '
      'management sequence. WORTH KNOWING BEFORE YOU REGISTER: the statewide description says '
      'the course includes preparatory lectures for the LEED professional accreditation exam. '
      'LEED Green Associate is the realistic student-level credential, requires only the exam, '
      'and is a genuine differentiator on an entry-level resume - but the GBCI exam fee is '
      'separate from tuition (check the reduced student rate) and booking it is your own step. '
      'Sit it while the material is fresh. ASK WHICH LEED VERSION is taught and which the '
      'current exam tests; they differ during transitions. ' + ACCE),
    'offering_notes': {
      'summary': ('Both public carriers award 3 credits and the titles differ only in phrasing. '
                  'The statewide description names LEED exam preparation explicitly. The same '
                  'subject also runs as BCN4590 at the 4000 level (Florida SouthWestern State '
                  'College); both are upper division, so this is a requirement-matching question '
                  'rather than a transfer barrier.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture course with no suffix.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Sustainable Construction', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "Overview of Sustainable Construction, '
                  'the basic philosophical premises and concepts, the cutting edge in design and '
                  'construction, methods of assessment, project delivery, economics, and green '
                  'building evaluation systems, such as LEED and Green Globes." Department of '
                  'Civil Engineering and Construction Management.')},
        {'institution': 'FGCU', 'institution_name': FGCU,
         'title': 'Sustainable Approach to Construction', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits. FGCU\'s catalogue was NOT REACHABLE when this guide was written '
                  '(its course PDF route returned an empty response), so its own description '
                  'could not be read. FGCU students should treat their syllabus as governing.')},
      ],
    },
  },

  'BCN3731C': {
    'title': 'Construction Safety and OSHA Standards',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'None recorded statewide. SINGLE-INSTITUTION NUMBER: only Florida A&M carries BCN3731C, and '
      'its catalogue was not reachable, so this guide is built from the statewide record and '
      'UWF\'s description of the related BCN3731 - your syllabus governs. WARNING, AND ASK BEFORE '
      'YOU REGISTER: the STATEWIDE definition of this number is INDUSTRIAL safety (29 CFR 1910) '
      'while both carriers appear to teach CONSTRUCTION safety (29 CFR 1926) - different '
      'standards, different requirements, and OSHA certifies against one or the other. The '
      'diagnostic is simple: check which CFR part the syllabus cites. Also confirm whether the '
      '"OSHA Certification" in the title is the 10-hour or 30-hour card, and whether it is the '
      'Construction or General Industry version; employers care which.'),
    'offering_notes': {
      'summary': ('Single public carrier. The statewide record is internally consistent in '
                  'saying INDUSTRIAL (title and description agree), but Florida already numbers '
                  'construction safety separately at BCN730, 732, 735, 737 and 738 - and both '
                  'institutions using 731 teach construction safety. Most likely a stale '
                  'statewide record on a construction-prefix number that drifted toward what its '
                  'students need.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("FAMU does not publish contact hours. 60 is Florida's convention for a "
                     '3-credit integrated lecture+lab (C) course, which is what the queued '
                     'identifier represents.'),
      'offerings': [
        {'institution': 'FAMU', 'institution_name': FAMU,
         'title': 'Construction Safety and OSHA Certification', 'credits': 3,
         'contact_hours': None,
         'note': ('3 credits. The only Florida public carrier of the C form. Catalogue '
                  'description not retrieved. Title indicates CONSTRUCTION safety plus an OSHA '
                  'outreach card, against a statewide record that defines the number as '
                  'INDUSTRIAL safety. Note UWF carries the bare BCN3731 as "Construction '
                  'Safety", focused on 29 CFR 1926 Construction Industry Regulations, site risk '
                  'aversion, insurance, documentation, maintenance of traffic, cost, scheduling '
                  'and job hazard analysis - a different identifier from this one.')},
      ],
    },
  },

  'BCN4564': {
    'title': 'Construction Mechanics II: Building Electrical and Systems',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'Construction Mechanics I - NOTE the statewide record names the prerequisite by TITLE, not '
      'by number, so identify the actual first course in your own catalogue (UWF\'s is BCN3561; '
      'elsewhere the subject is numbered BCN560, BCN561, BCN591 or BCN201). There is no active '
      'BCN4563, so do not derive the first course by arithmetic. READ THE TITLE CAREFULLY: '
      '"construction mechanics" in Florida means BUILDING SERVICES (HVAC, plumbing, fire '
      'protection, electrical), NOT structural mechanics - that is BCN2405 and BCN3431C. '
      'SINGLE-INSTITUTION NUMBER: only FIU carries it, and FIU\'s stated scope is the ELECTRICAL '
      'half while the statewide description covers all of MEP. Ask whether your section covers '
      'HVAC and plumbing too, and if not, which course does.'),
    'offering_notes': {
      'summary': ('Single public carrier. FIU titles it "Environmental Control in Buildings II", '
                  'a clearer name for the same subject. The statewide description covers HVAC, '
                  'plumbing, fire protection and electrical; FIU\'s own description is the '
                  'ELECTRICAL half plus code provisions and cost estimates - coherent for a '
                  'course numbered II, but a real scope question for a student.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("FIU does not publish contact hours for this course. 45 is Florida's "
                     'convention for a 3-credit lecture course with no suffix.'),
      'offerings': [
        {'institution': 'FIU', 'institution_name': FIU,
         'title': 'Environmental Control in Buildings II', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits. "Concepts and practices of electrical systems in the construction '
                  'of residential and commercial buildings, including code provisions and cost '
                  'estimates." College of Engineering and Computing. NOTE this is narrower than '
                  "the statewide description, which also covers HVAC, plumbing and piping and "
                  'fire protection, and which specifies that a construction site visit is '
                  'included.')},
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
