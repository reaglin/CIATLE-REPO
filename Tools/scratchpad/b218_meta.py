"""Batch 218 metadata -- HFT (six of seven queued; HFT3271 PULLED).

HFT3271 was pulled to REVIEW_QUEUE: four subjects on one number and NO carrier
teaches the statewide subject. See the queue note and REVIEW_QUEUE.

Contact hours: 45 for 3-credit lecture, 60 for the 3-credit integrated C
course (HFT3814C).

Prerequisite budget (batch-215 rule): shared blocks counted first. One here,
kept short.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
UCF = 'University of Central Florida'
FAU = 'Florida Atlantic University'
PESC = 'Pensacola State College'

# Near-universal across the HFT prefix -> boilerplate, said once and briefly.
DE = ('The dual-enrolment/elective marking is near-universal across the HFT prefix, so it says '
      'nothing distinctive about this course.')

NEW = {

  'HFT2000': {
    'title': 'Introduction to the Hospitality Industry',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE - this is the gateway course of the degree. TAKE IT EARLY: it is the prerequisite for '
      'several later courses (at UWF, HFT3814C and HFT4753), and Florida\'s record shows HFT4252 '
      'requiring it with a MINIMUM GRADE OF C - a passing grade is not always a sufficient grade in '
      'a sequenced programme. SINGLE PUBLIC CARRIER: only UWF among Florida\'s public institutions '
      '(the other carrier is private and out of scope), so your syllabus governs. USE THE COURSE TO '
      'CHOOSE A SEGMENT - the industry is far wider than hotels and restaurants, and revenue '
      'management, private club management, meetings and cruise operations are all better paid or '
      'less crowded than students expect. ' + DE),
    'offering_notes': {
      'summary': ('One public carrier. UWF\'s description lists the industry segments explicitly - '
                  'lodging, food and beverage, meetings and conventions, recreation and leisure, '
                  'gaming entertainment, cruising, clubs and transportation - which is the course\'s '
                  'main contribution, since students routinely arrive thinking hospitality means '
                  'hotels and restaurants.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("UWF does not publish contact hours. 45 is Florida's convention for a 3-credit "
                     'lecture course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Introduction to the Hospitality Industry', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "Introduction to management career options '
                  'within the hospitality industry; which includes lodging, food and beverage, '
                  'meetings and conventions, recreation and leisure, gaming entertainment, '
                  'cruising, clubs, and transportation. The importance of leadership and service '
                  'culture are also discussed." College of Business, Department of Commerce - so '
                  'hospitality taught as a business discipline rather than a culinary or vocational '
                  'programme.')},
      ],
    },
  },

  'HFT3214': {
    'title': 'Hospitality Safety, Sanitation and Risk Management',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'None recorded. TAKE IT BEFORE ANY FOOD AND BEVERAGE JOB OR INTERNSHIP. THE MOST VALUABLE '
      'THING HERE IS THE CERTIFICATION: students may obtain NRA ServSafe Food Safety and ServSafe '
      'Alcohol certifications. Florida requires licensed food establishments to have certified food '
      'protection managers, so ServSafe Manager is close to a condition of employment in restaurant '
      'management - and it is valid five years, covering your early career. ASK IN WEEK ONE whether '
      'the certification is included, which ones, and whether the exam fee is covered (it is '
      'normally separate from tuition). SINGLE PUBLIC CARRIER: only UWF; the other is private. '
      + DE),
    'offering_notes': {
      'summary': ('One public carrier. The ServSafe certification opportunity is the concretely '
                  'valuable element and is named in the statewide description. NOTE the statewide '
                  'description also includes "developing and maintaining a sustainable facility", '
                  'which UWF\'s published description does not mention.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("UWF does not publish contact hours. 45 is Florida's convention for a 3-credit "
                     'lecture course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Hospitality Safety, Sanitation and Risk Management', 'credits': 3,
         'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "Study of safety and sanitation management '
                  'principles in the hospitality industry related to safe food handling practices '
                  'and responsible alcohol service. Students may obtain National Restaurant '
                  'Association ServSafe Food Safety and ServSafe Alcohol certifications." Does not '
                  'mention the sustainability element the statewide description includes. College '
                  'of Business, Department of Commerce.')},
      ],
    },
  },

  'HFT3814C': {
    'title': 'Management of Food and Beverage Operations',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'HFT 2000 at UWF. SINGLE PUBLIC CARRIER: only UWF, so your syllabus governs. EXPECT MANAGEMENT, '
      'NOT CULINARY ARTS - the course sits in a College of Business and is about why a kitchen loses '
      'money, not how to cook. FIND OUT WHAT THE C-SUFFIX LAB ACTUALLY IS: some programmes run a '
      'production kitchen and others a computer lab for costing work, and they are very different '
      'experiences. The arithmetic is the course and it is unforgiving - prime cost consumes most of '
      'revenue, so get genuinely comfortable with spreadsheets. NOTE the statewide description says '
      'the class is for "future managers who will have to help out in the [operation]" - take that '
      'literally; the hours are evenings, weekends and holidays. ' + DE),
    'offering_notes': {
      'summary': ('One public carrier, using the statewide title unchanged. A C course, so the '
                  'identifier represents the integrated lecture+lab form. Taught as management in a '
                  'College of Business rather than as culinary arts.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("UWF does not publish contact hours. 60 is Florida's convention for a 3-credit "
                     'integrated lecture+lab (C) course, which is what the queued identifier '
                     'represents.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Management of Food and Beverage Operations', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite HFT 2000. "Provides the '
                  'foundation for understanding the various challenges and responsibilities '
                  'involved in food and beverage management... organization, marketing, menus, '
                  'costs and pricing, production, service, safety, and finances." College of '
                  'Business, Department of Commerce.')},
      ],
    },
  },

  'HFT4252': {
    'title': 'Employee Wellbeing / Hotel and Resort Management (one number, two subjects)',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'Florida\'s record names HFT2000 with a MINIMUM GRADE OF C, though neither carrier\'s published '
      'record confirms it - check, because a minimum-grade condition is exactly what students '
      'discover when registration is blocked. READ THIS FIRST: THIS NUMBER CARRIES TWO DIFFERENT '
      'SUBJECTS and Florida\'s own record contradicts itself. The statewide TITLE says Employees '
      'Wellbeing; the statewide DESCRIPTION is entirely hotel and resort management; UCF teaches '
      'wellbeing and Pensacola State teaches hotel and resort management - the carriers split, one '
      'on each side. Both subjects are numbered ELSEWHERE in the prefix (wellbeing at HFT2014, '
      'hotel/resort at HFT2250/HFT2276), so look for those if you need one specifically. Check your '
      'syllabus in week one against the diagnostic in the guide.'),
    'offering_notes': {
      'summary': ('ONE NUMBER, TWO SUBJECTS, and the statewide record is self-contradictory: its '
                  'TITLE says employee wellbeing and its DESCRIPTION is hotel and resort '
                  'management. UCF backs the title, Pensacola State backs the description - the '
                  'carriers split one on each side, so the title/description test is indeterminate '
                  'here. Guide covers BOTH readings, each labelled. Recommended for a split - see '
                  'REVIEW_QUEUE.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture course, and UCF records ZERO laboratory hours, confirming it '
                     'as a lecture course.'),
      'offerings': [
        {'institution': 'UCF', 'institution_name': UCF,
         'title': 'Employees Wellbeing in Hospitality and Tourism', 'credits': 3,
         'contact_hours': None,
         'note': ('3 credits, zero laboratory hours recorded. "Principles of hospitality employees\' '
                  'wellness and emotional regulations. A wide range of topics will be covered on '
                  'employees\' emotions, physical and emotional wellbeing, and mindfulness." Backs '
                  'the statewide TITLE.')},
        {'institution': 'PESC', 'institution_name': PESC,
         'title': 'Hotel and Resort Management', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits. ⚠ A completely different subject from UCF\'s - it backs the statewide '
                  'DESCRIPTION ("managerial functions, operating procedures, and competencies [of] '
                  'hotel and resorts... management, ownership, franchising") rather than the '
                  'statewide title. Catalogue not reachable, so Reading B in the guide is built '
                  'from the statewide description rather than from Pensacola State\'s syllabus.')},
      ],
    },
  },

  'HFT4503': {
    'title': 'Hospitality Marketing and Sales',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'Florida\'s record names "BASIC MARKETING" - a SUBJECT, not a course number, so you cannot look '
      'it up. In practice this means principles of marketing (normally MAR3023 or equivalent); '
      'confirm with an adviser, and note the course genuinely assumes it - segmentation, positioning '
      'and the marketing mix are treated as known rather than taught. CHECK THE SCOPE: FAU titles it '
      'Hospitality/Tourism Marketing (wider - destination and visitor economies) while UWF\'s '
      'description focuses on marketing and sales FOR HOTELS. Both are valuable and they lead to '
      'different jobs. UWF dual-lists with HMG 5506, so taking this version may block the graduate '
      'one later. ' + DE),
    'offering_notes': {
      'summary': ('Both public carriers award 3 credits, but the scope differs: FAU\'s title adds '
                  'TOURISM (destination marketing, attractions, visitor economies) while UWF\'s '
                  'description narrows to marketing and sales for hotels, against a broader '
                  'statewide description covering research, positioning, ethics and a multicultural '
                  'component. FAU\'s catalogue was not retrievable, so the scope question could not '
                  'be settled from source.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Service Marketing for Hospitality Management', 'credits': 3,
         'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "Provides students with management skills '
                  'related to marketing and sales for hotels. The best practices that have proven '
                  'successful in marketing and sales in the hospitality industry are also '
                  'discussed." Narrower than the statewide description. Offered concurrently with '
                  'HMG 5506. College of Business, Department of Commerce.')},
        {'institution': 'FAU', 'institution_name': FAU,
         'title': 'Hospitality / Tourism Marketing', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits. Title explicitly includes TOURISM, suggesting destination and visitor '
                  'economy content beyond property marketing. FAU does not expose a public course '
                  'catalogue, so its description could not be read.')},
      ],
    },
  },

  'HFT4753': {
    'title': 'Convention, Trade Show and Special Event Management',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'HFT 2000 at UWF. SINGLE PUBLIC CARRIER: only UWF; the other is private and out of scope. '
      'SCOPE NOTE: the statewide title is Convention & Trade Show Management, but UWF titles it '
      'Special Event Management and covers the wider field - event design, implementation, '
      'evaluation, legal issues and destination economic impact - with conventions and trade shows '
      'inside it. That is an EXPANSION, not a divergence, and it broadens employability. But ASK HOW '
      'MUCH TRADE SHOW DETAIL your section covers (floor plans, exhibitor sales, general service '
      'contractors) if exhibitions are your target. CONTRACTS ARE WHERE THE MONEY IS LOST - attrition, '
      'cancellation and force majeure clauses carry real liability and are negotiable. ' + DE),
    'offering_notes': {
      'summary': ('One public carrier, and UWF\'s course is BROADER than the statewide title: '
                  'Special Event Management covering conventions, trade shows, CVBs, sponsors and '
                  'venues PLUS event design, evaluation, legal issues and destination economic '
                  'impact. The statewide subject sits inside it - an expansion rather than a '
                  'divergence.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("UWF does not publish contact hours. 45 is Florida's convention for a 3-credit "
                     'lecture course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Special Event Management', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite HFT 2000. "Convention '
                  'facilities, convention and visitors bureaus, sponsors, host venues, '
                  'stakeholders, tradeshow and meeting management are examined. Analysis of the '
                  'methods and techniques of event design, organization, implementation, and '
                  'evaluation. Legal issues and trends are studied. The economic impact of the '
                  'special events business upon destinations is studied." College of Business, '
                  'Department of Commerce.')},
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
    print('shared block DE = %d chars' % len(DE))
    over = 0
    for k in sorted(NEW):
        p = NEW[k]['prerequisites'] or ''
        flag = ''
        if len(p) > 1000:
            flag = '  <-- OVER 1000'
            over += 1
        print('  %-9s %d cr  %3d hrs  prereq %4d chars%s'
              % (k, NEW[k]['credits'], NEW[k]['contact_hours'], len(p), flag))
    print('%d of %d over the limit' % (over, len(NEW)))


if __name__ == '__main__':
    main()
