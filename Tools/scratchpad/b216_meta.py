"""Batch 216 metadata -- EME, completing the prefix queue (8 courses).

All eight are 3-credit lecture courses, so contact hours are Florida's
convention: 45.

Prerequisite budget (batch-215 lesson): count the SUM of shared blocks first,
then write the course-specific text into what remains. Only ONE shared block
here, deliberately kept under 200 chars.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
UNF = 'University of North Florida'
FAU = 'Florida Atlantic University'

# Every EME record carries the dual-enrolment marking (401 of 409), so it is
# prefix-wide boilerplate -- said once, briefly.
DE = ('The dual-enrolment/elective marking on this number is near-universal across the EME prefix, '
      'so it says nothing distinctive about this course.')

NEW = {

  'EME2620': {
    'title': 'Digital Literacy in a Globally Connected World',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE - stated explicitly in Florida\'s record, and the course is designed for students in any '
      'discipline at any stage. The 2000-level number marks it lower division, NOT remedial. '
      'WARNING WORTH CHECKING BEFORE YOU COUNT IT: general-education designation is INSTITUTION-'
      'SPECIFIC and the two carriers differ - FAU records a SOCIAL SCIENCES general-education '
      'designation for this course and UWF records NONE. Check your own institution\'s '
      'general-education list before relying on it to fill a requirement, and check the receiving '
      'institution\'s too if you transfer: a course can transfer as credit without carrying the '
      'category you expected. No Gordon Rule designation at either. ' + DE),
    'offering_notes': {
      'summary': ('Both public carriers award 3 credits and teach the same course - FAU shortens the '
                  'title, UWF uses the statewide one. The interesting difference is not the title '
                  'but the DESIGNATION: FAU records a social-sciences general-education designation, '
                  'UWF records none.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Digital Literacy in a Globally Connected World', 'credits': 3,
         'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Description matches the statewide record: '
                  'students "learn how to access, evaluate, apply, participate, and interact within '
                  'the educational and professional digital environments as they solve complex '
                  'problems within a technology-rich world." NO general-education designation '
                  'recorded. School of Education, Department of Instructional Design and '
                  'Technology.')},
        {'institution': 'FAU', 'institution_name': FAU,
         'title': 'Digital Literacy', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits. ⚠ Records a SOCIAL SCIENCES general-education designation, which UWF '
                  'does not - the same course filling a general-education requirement at one '
                  'institution and not the other. Catalogue not retrieved for this guide.')},
      ],
    },
  },

  'EME3312': {
    'title': 'Technology Supported Learning',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'None recorded statewide or by UWF. SINGLE PUBLIC CARRIER: only UWF carries this number among '
      'Florida\'s public institutions (the other carrier is private and out of scope), so this guide '
      'hedges accordingly and your syllabus governs. SCOPE WARNING: the statewide description is '
      'about integrating technology INTO THE CLASSROOM, while UWF\'s course is broader - distance '
      'learning, mobile learning and INFORMAL learning - which fits its Instructional Design and '
      'Technology department serving corporate, military and healthcare training too. If you are '
      'taking it as preparation for classroom teaching, check it covers what you need. THIS IS NOT A '
      'TEACHER CERTIFICATION COURSE: Florida certification runs through a state-approved teacher '
      'preparation programme, which an ID&T degree is not. ' + DE),
    'offering_notes': {
      'summary': ('Only ONE public carrier. Real scope divergence: the statewide title and '
                  'description are classroom-teaching focused ("Educational Technology for 21st '
                  'Century Teaching"), while UWF drops "teaching" from the title and adds distance, '
                  'mobile and informal learning - a broader course serving a design profession '
                  'rather than teacher preparation.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("UWF does not publish contact hours. 45 is Florida's convention for a 3-credit "
                     'lecture course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Technology Supported Learning', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "Examines the use of current and emerging '
                  'technologies to facilitate learning. Topics covered will include distance '
                  'learning, formal and informal technology based learning and mobile learning. '
                  'Strategies for integrating technology in educational settings will be explored." '
                  'Broader than the statewide classroom-integration framing. School of Education, '
                  'Department of Instructional Design and Technology.')},
      ],
    },
  },

  'EME3351': {
    'title': 'Introduction to Instructional and Performance Technology',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'None recorded statewide or by UWF - and it should be taken EARLY, because the whole sequence '
      'assumes its vocabulary and its central distinction (instructional technology asks how to '
      'teach something well; human performance technology asks whether teaching is the right '
      'intervention at all). WARNING: UNF appears to teach a DIFFERENT SUBJECT under this number - '
      'its title is "Adult Learning Theory and Curriculum Development", against a statewide '
      'description about the instructional-technology/performance-technology distinction, and UWF '
      'matches the statewide description verbatim. UNF\'s catalogue was not retrievable so only the '
      'title is known. If you are transferring between UNF and UWF, raise this number with an '
      'adviser and send the syllabus, not the course number. ' + DE),
    'offering_notes': {
      'summary': ('Both public carriers award 3 credits, but UNF\'s TITLE suggests a different '
                  'subject: "Adult Learning Theory and Curriculum Development" against the statewide '
                  '(and UWF) "Introduction to Instructional and Performance Technology". Related '
                  'material, but not the same course. FLAGGED rather than resolved - UNF\'s '
                  'catalogue could not be read, and a title is weaker evidence than a description.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Introduction to Instructional and Performance Technology', 'credits': 3,
         'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Description matches the statewide record '
                  'verbatim: "The distinct purposes of instructional technology and human '
                  'performance technology are explored in depth... The similarities and differences '
                  'will be compared to include the historical basis, models, major tasks, and '
                  'desired outcomes." School of Education, Department of Instructional Design and '
                  'Technology.')},
        {'institution': 'UNF', 'institution_name': UNF,
         'title': 'Adult Learning Theory and Curriculum Development', 'credits': 3,
         'contact_hours': None,
         'note': ('3 credits. ⚠ Title indicates a different subject from the statewide description - '
                  'adult learning theory and curriculum development are foundational to the field '
                  'but are not the instructional-technology/performance-technology distinction this '
                  'number is defined around. UNF\'s catalogue is client-rendered and its archived '
                  'catalogue PDFs are blocked to automated retrieval, so its description could not '
                  'be read and the divergence could not be resolved.')},
      ],
    },
  },

  'EME3624': {
    'title': 'Training Needs Assessment',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'None recorded statewide or by UWF, though the sequence assumes EME3351 first - this course '
      'operationalises that one\'s argument. The statewide description is explicit that needs '
      'assessment happens PRIOR TO design, to determine "who needs to learn what and why". TWO '
      'CAUTIONS FROM THE METHODS LITERATURE: people cannot reliably report their own training needs '
      '(ask what stops them doing their job, not what training they want), and what people say they '
      'do differs systematically from what they do - which is why observation and triangulation are '
      'required rather than optional. Expect the hard part to be professional nerve rather than '
      'method: a needs assessment that concludes the requested training would not help is a finding '
      'somebody does not want. ' + DE),
    'offering_notes': {
      'summary': ('Unusually clean: both public carriers use the statewide title UNCHANGED, both at '
                  '3 credits, and UWF\'s description matches the statewide one almost word for word. '
                  'No title drift, no credit divergence, no suffix disagreement.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Training Needs Assessment', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Matches the statewide description: '
                  '"Examines the role of training needs assessment in instructional design... '
                  'techniques used to collect and analyze data to identify and clarify training '
                  'needs... to determine who needs to learn what and why prior to engaging in the '
                  'design and development of instructional materials." School of Education, '
                  'Department of Instructional Design and Technology.')},
        {'institution': 'UNF', 'institution_name': UNF,
         'title': 'Training Needs Assessment', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits, statewide title unchanged. UNF\'s catalogue is client-rendered and its '
                  'archived catalogue PDFs are blocked to automated retrieval, so its description '
                  'could not be read - though the matching title makes divergence unlikely here.')},
      ],
    },
  },

  'EME4043': {
    'title': 'Instructional Technology Leadership',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'None recorded statewide or by UWF; taken late in the sequence, after the design and '
      'development courses have shown what the work involves. READ THE STATEWIDE DESCRIPTION '
      'LITERALLY: it names FIVE settings - education, training, military, public sector and '
      'non-profits - so this is deliberately NOT a school-technology-leadership course, and the '
      'sectors differ in procurement rules, funding constraints and data obligations. The course\'s '
      'actual content is SYSTEMS THINKING, not a survey of technologies: technology fails for '
      'organisational reasons rather than technical ones. Pairs naturally with EME4083, since making '
      'an evidence-based case for an investment needs evaluation evidence. ' + DE),
    'offering_notes': {
      'summary': ('Both public carriers use the statewide title unchanged at 3 credits, and UWF\'s '
                  'description matches the statewide one almost word for word. Note the statewide '
                  'description deliberately spans five sectors and names systems thinking '
                  'explicitly.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Instructional Technology Leadership', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Matches the statewide description: '
                  'students "examine the role of the technology leader in effective integration, '
                  'management and use of technology in a variety of settings, including education, '
                  'training, military, public sector and non-profits... Special attention is paid to '
                  'the role of systems thinking in effective technology leadership." School of '
                  'Education, Department of Instructional Design and Technology.')},
        {'institution': 'UNF', 'institution_name': UNF,
         'title': 'Instructional Technology Leadership', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits, statewide title unchanged. Catalogue not retrievable (client-rendered; '
                  'archived PDFs blocked), so its description could not be read.')},
      ],
    },
  },

  'EME4083': {
    'title': 'Program Evaluation in Instructional Design and Technology',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'None recorded statewide or by UWF, though the sequence assumes EME3351, EME3624 and usually '
      'EME4674 first. NOTE WHAT THE COURSE IS ORGANISED AROUND: MODEL SELECTION, not a single method '
      '- different evaluation questions need genuinely different designs, and choosing the wrong '
      'model produces a competent answer to a question nobody asked. Pairs closely with EME3624: '
      'needs assessment and evaluation use substantially the same methods at opposite ends of a '
      'project, and students who see them as one skill applied twice understand the field better. '
      'Expect Kirkpatrick to be central AND expect to learn its limits - most organisations stop at '
      'level one, where the data is least informative. ' + DE),
    'offering_notes': {
      'summary': ('Both public carriers use the statewide title unchanged at 3 credits, and UWF\'s '
                  'description matches the statewide one almost word for word. The statewide '
                  'description emphasises selecting the appropriate MODEL and developing a '
                  'comprehensive evaluation PLAN.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Program Evaluation in Instructional Design and Technology', 'credits': 3,
         'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Matches the statewide description: students '
                  '"develop skills used in selecting the appropriate model for conducting various '
                  'types of evaluations... Development of a comprehensive evaluation plan will '
                  'provide students with the opportunity to align an evaluation model with data '
                  'collection strategies and techniques for a specific evaluation purpose." School '
                  'of Education, Department of Instructional Design and Technology.')},
        {'institution': 'UNF', 'institution_name': UNF,
         'title': 'Program Evaluation in Instructional Design and Technology', 'credits': 3,
         'contact_hours': None,
         'note': ('3 credits, statewide title unchanged. Catalogue not retrievable (client-rendered; '
                  'archived PDFs blocked), so its description could not be read.')},
      ],
    },
  },

  'EME4674': {
    'title': 'Development of Instructional Materials',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'None recorded statewide or by UWF, though the sequence deliberately places EME3351 and '
      'EME3624 first - you cannot reach development without having been taught to ask whether '
      'anything should be developed. ASK BEFORE YOU REGISTER: which authoring tools does this '
      'section use? A course built around Articulate Storyline produces different portfolio '
      'artefacts and different marketable skills than one built around documents and presentations. '
      'Neither is wrong - the principles transfer - but the tool experience is what job listings '
      'name. EXPECT COUNTER-INTUITIVE RESEARCH: adding engaging but irrelevant material reduces '
      'learning, and narrating text already on screen is worse than either alone. Treat every '
      'assignment as a portfolio piece; this field hires on portfolio. ' + DE),
    'offering_notes': {
      'summary': ('Both public carriers use the statewide title unchanged at 3 credits, and UWF\'s '
                  'description matches the statewide one almost word for word. The statewide '
                  'description is organised around "instructional messages" and message design '
                  'principles, and names the logistical constraints of time and cost explicitly.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Development of Instructional Materials', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Matches the statewide description: "The '
                  'pedagogical, technical, and logistical aspects of instructional messages will '
                  'provide the foundation... Message design principles and individual preferences '
                  'are considered... Media and technology aspects relating to effective message '
                  'delivery will be addressed and related to the logistical constraints of time and '
                  'cost." School of Education, Department of Instructional Design and Technology.')},
        {'institution': 'UNF', 'institution_name': UNF,
         'title': 'Development of Instructional Materials', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits, statewide title unchanged. Catalogue not retrievable (client-rendered; '
                  'archived PDFs blocked), so its description could not be read.')},
      ],
    },
  },

  'EME4684': {
    'title': 'Instructional Design and Technology Capstone',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'PERMISSION IS REQUIRED at UWF - find out what your programme requires and when the deadline '
      'falls A FULL TERM before you intend to take it, because missing capstone permission delays '
      'graduation by a term and is among the most avoidable delays in any degree. Follows the whole '
      'sequence (EME3351, EME3624, EME4674, EME4083, EME4043), all of which it draws on. TWO '
      'DELIVERABLES: a capstone project and an electronic portfolio mapped to programme-level '
      'learning outcomes - read your capstone handbook and rubric at the START. SCOPE THE PROJECT TO '
      'FINISH IT: the commonest capstone failure is unfinished ambitious work, and a complete modest '
      'project demonstrates the whole design process where a fragment cannot. ' + DE),
    'offering_notes': {
      'summary': ('Both public carriers award 3 credits and are plainly the same course. UWF '
                  'requires PERMISSION to enrol. Note the title difference - UNF says "Learning '
                  'Design", UWF "Instructional Design" - which reflects a real vocabulary shift in '
                  'the field rather than a disagreement about content; search job listings for '
                  'both.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Instructional Design and Technology Capstone', 'credits': 3,
         'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. ⚠ PERMISSION IS REQUIRED. "The capstone is '
                  'designed to enable students to demonstrate mastery of the Instructional Design '
                  'and Technology knowledge, skills, and abilities developed during the academic '
                  'program. Students will identify, propose, and complete a capstone project and '
                  'develop an electronic portfolio highlighting their attainment of the program '
                  'level learning outcomes." School of Education, Department of Instructional Design '
                  'and Technology.')},
        {'institution': 'UNF', 'institution_name': UNF,
         'title': 'Learning Design and Technology Capstone', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits. Uses "Learning Design" where UWF and the statewide title use '
                  '"Instructional Design" - both terms are current in the field. Catalogue not '
                  'retrievable (client-rendered; archived PDFs blocked).')},
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
    over = 0
    print('shared block DE = %d chars' % len(DE))
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
