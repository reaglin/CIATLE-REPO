"""Batch 215 metadata -- RET, completing the prefix queue (12 courses).

Contact hours:
  * lecture 3 cr -> 45, 2 cr -> 30 (Florida convention)
  * 1-credit LAB -> 30 (the 2-3 contact hours/week convention, lower end)
  * CLINICAL PRACTICUM -> ~3 contact hours per credit per week, so 3 cr -> 135
    and 4 cr -> 180. The classroom convention would give 45/60 and badly
    misdescribe a full clinical rotation; the batch-200 rule (where a real
    measurement governs, use it rather than the credit convention) applies.

Prerequisites: the batch-184 rule puts the Level 2 screening / certification
warning in the PREREQUISITE field for every placement course, since that is
what a queue reader sees first. Drafted at ~850 chars.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
FAMU = 'Florida A&M University'
SSCF = 'Seminole State College of Florida'
FSWSC = 'Florida SouthWestern State College'

# NOTE these shared blocks count against the ~850-char prerequisite target for
# EVERY course that uses them (the batch-212 lesson). With three blocks in play
# the arithmetic bites harder: keep them short.
CRED = ('CREDENTIAL WARNING: NBRC exam eligibility runs through completing a CoARC-accredited '
        'programme, NOT through accumulating credit - and CoARC accredits entry-into-practice and '
        'degree-advancement programmes separately. Confirm your programme\'s status and type.')

PLACE = ('CLINICAL PLACEMENT - START EARLY: Florida Level 2 fingerprint screening, immunisations, TB '
         'and drug screening, health insurance and BLS are required BEFORE you can enter a facility, '
         'and screening is not instant. Expect 8-12 h shifts including nights and weekends, travel '
         'at your own cost, and near-absolute attendance. HIPAA applies from shift one. ')

SEQ = ('The four practica are strictly ordered and run annually in a cohort, so failing one delays '
       'every later one by about a YEAR. ')

NEW = {

  'RET3028': {
    'title': 'Foundations of Respiratory Therapy',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF requires BSC 1085/L AND BSC 1086/L (anatomy and physiology I and II with labs) AND '
      'CHM 2045/L (general chemistry) AND MCB 2010/L (microbiology) - four sciences with four labs, '
      'normally completed BEFORE admission to the professional sequence, so plan backwards two to '
      'three terms. NOTE Florida numbers A&P under two competing prefixes (BSC vs APK) and '
      'health-professions prerequisites name the BSC numbers - check the exact numbers your '
      'programme requires. COREQUISITE RET3028L, reciprocally enforced: register for both '
      '(4 credits, two grades) and expect to repeat BOTH if you fail either. Cohort-sequenced, so '
      'a failure costs about a year, not a term. ' + CRED),
    'offering_notes': {
      'summary': ('Both public carriers award 3 credits; Fundamentals (FAMU, matching the statewide '
                  'title) and Foundations (UWF) are the same course. Taken with the corequisite '
                  'lab RET3028L. Part of an ENTRY-INTO-PRACTICE baccalaureate, not a '
                  'degree-completion one.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture; the lab hours sit in the corequisite RET3028L. NOTE the '
                     'statewide DESCRIPTION for this number is a placeholder that merely repeats '
                     'the title, so UWF\'s description is the only substantive source.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Foundations of Respiratory Therapy', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "A comprehensive introduction to the '
                  'respiratory care profession... theory and application of physics, chemistry, '
                  'basic therapeutics, and disease management", plus infection control, therapeutic '
                  'devices, patient assessment skills, medical gas administration, aerosol drug '
                  'delivery and medical terminology. Prerequisite BSC 1085/L, BSC 1086/L, '
                  'CHM 2045/L, MCB 2010/L; corequisite RET 3028L. College of Health, Department of '
                  'Health Sciences and Administration.')},
        {'institution': 'FAMU', 'institution_name': FAMU,
         'title': 'Fundamentals of Respiratory Therapy', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits, matching the statewide title. Catalogue not reachable by automated '
                  'retrieval (acalog, empty responses), so FAMU\'s own description could not be '
                  'read.')},
      ],
    },
  },

  'RET3028L': {
    'title': 'Foundations of Respiratory Therapy Laboratory',
    'credits': 1, 'contact_hours': 30, 'version': '1.0',
    'prerequisites': (
      'Same as the lecture: at UWF, BSC 1085/L AND BSC 1086/L AND CHM 2045/L AND MCB 2010/L. '
      'COREQUISITE RET3028, reciprocally enforced - neither can be taken alone, so register for '
      'both (4 credits, two grades) and expect to repeat BOTH if you fail either. WARNING ON TIME: '
      'a 1-credit lab carries 2-3 CONTACT HOURS A WEEK plus out-of-class practice, because '
      'competencies are assessed on performance rather than attendance - budget for it like a '
      '3-credit course. Cohort-sequenced, so a failed competency can cost about a year. Most '
      'programmes require students to supply their own stethoscope. ' + CRED),
    'offering_notes': {
      'summary': ('Both public carriers award 1 credit. NOTE Florida\'s statewide record gives this '
                  'LAB the same title as its lecture, with no separate description, so the state '
                  'record cannot distinguish the two halves at all - both institutions do in their '
                  'own catalogues.'),
      'hours_source': 'derived',
      'derived_contact_hours': 30,
      'derivation': ('Neither carrier publishes contact hours. A 1-credit laboratory in Florida '
                     'conventionally carries 2-3 contact hours a week, so roughly 30-45 hours a '
                     'term; 30 is the lower end of that convention.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Foundations of Respiratory Therapy Lab', 'credits': 1, 'contact_hours': None,
         'note': ('1 sh, may not be repeated for credit. "Reinforces understanding of the role of '
                  'the respiratory care practitioner within the clinical setting. Emphasis is '
                  'placed on correct setup and application of equipment, techniques, and therapies" '
                  '- medical gas administration, patient assessment skills, respiratory '
                  'therapeutics, patient safety techniques, blood gas analysis and airway care. '
                  'Corequisite RET 3028. Department of Health Sciences and Administration.')},
        {'institution': 'FAMU', 'institution_name': FAMU,
         'title': 'Fundamentals of Respiratory Therapy Lab', 'credits': 1, 'contact_hours': None,
         'note': ('1 credit. Catalogue not reachable by automated retrieval.')},
      ],
    },
  },

  'RET3493': {
    'title': 'Cardiopulmonary Patient Assessment',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF requires BSC 1085/L AND BSC 1086/L AND CHM 2045/L AND MCB 2010/L. Anatomy and physiology '
      'matters most here of any course in the sequence - chest examination, blood gas interpretation '
      'and haemodynamics all assume it fluently. COREQUISITE RET3493L, reciprocally enforced: '
      'register for both (4 credits, two grades); failing either normally means repeating both, and '
      'in a cohort programme that costs about a year. WATCH FOR: FAMU titles this course "Health '
      'Assessments AND INTERVENTIONS", which may mean it also covers therapy selection - ask, since '
      'FAMU\'s description was not retrievable. Blood gas interpretation is where students '
      'separate; work problems continuously from week one. ' + CRED),
    'offering_notes': {
      'summary': ('Both public carriers award 3 credits. Three different titles: statewide '
                  '"Respiratory Disease Assessment", UWF "Patient Assessment", FAMU "Health '
                  'Assessments and Interventions". The first two are the same course; FAMU\'s '
                  '"Interventions" may signal additional therapeutic content - flagged rather than '
                  'resolved, since FAMU\'s catalogue was unreachable.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit lecture; lab hours sit in the corequisite RET3493L.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Patient Assessment', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Covers "the fundamentals of cardiopulmonary '
                  'assessment" and the practitioner\'s role in "promoting a positive patient '
                  'encounter"; skills supporting a complete examination through evaluation of '
                  'medical records, physical findings, laboratory data, pulmonary function testing, '
                  'imaging and hemodynamic monitoring. Prerequisite BSC 1085/L, BSC 1086/L, '
                  'CHM 2045/L, MCB 2010/L; corequisite RET 3493L.')},
        {'institution': 'FAMU', 'institution_name': FAMU,
         'title': 'Health Assessments and Interventions', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits. The title implies assessment PLUS therapeutic intervention, a broader '
                  'scope than the statewide "Respiratory Disease Assessment". Catalogue not '
                  'reachable, so the scope question could not be resolved. FAMU uses the SAME title '
                  'for its lecture and its lab - register by number.')},
      ],
    },
  },

  'RET3493L': {
    'title': 'Cardiopulmonary Patient Assessment Laboratory',
    'credits': 1, 'contact_hours': 30, 'version': '1.0',
    'prerequisites': (
      'Same as the lecture: at UWF, BSC 1085/L AND BSC 1086/L AND CHM 2045/L AND MCB 2010/L - '
      'anatomy and physiology is used from the first session for chest landmarks and lung lobe '
      'positions. COREQUISITE RET3493, reciprocally enforced: register for both (4 credits, two '
      'grades); failing either normally means repeating both. TIME WARNING: a 1-credit lab is 2-3 '
      'contact hours a week plus practice - budget like a 3-credit course. YOU WILL EXAMINE '
      'CLASSMATES: chest examination needs access to the chest wall, participation as a subject is '
      'voluntary with an alternative available, and findings about classmates are private and are '
      'not diagnostic. Bring your own stethoscope - buy a decent one. ' + CRED),
    'offering_notes': {
      'summary': ('Both public carriers award 1 credit. Florida\'s statewide record gives this lab '
                  'the same title as its lecture with no separate description. NOTE FAMU uses one '
                  'title ("Health Assessments and Interventions") for BOTH its lecture and its lab, '
                  'so within FAMU they are distinguished only by number and credit value.'),
      'hours_source': 'derived',
      'derived_contact_hours': 30,
      'derivation': ('Neither carrier publishes contact hours. A 1-credit laboratory conventionally '
                     'carries 2-3 contact hours a week, so roughly 30-45 hours a term; 30 is the '
                     'lower end.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Patient Assessment Lab', 'credits': 1, 'contact_hours': None,
         'note': ('1 sh, may not be repeated for credit. "Reinforces the role of the respiratory '
                  'care practitioner throughout a cardiopulmonary assessment. Emphasis is placed on '
                  'correct clinical skills that support a complete patient examination" - assessment '
                  'of medical records, physical findings, laboratory data, pulmonary function tests, '
                  'medical images and hemodynamic monitoring data. Corequisite RET 3493.')},
        {'institution': 'FAMU', 'institution_name': FAMU,
         'title': 'Health Assessments and Interventions', 'credits': 1, 'contact_hours': None,
         'note': ('1 credit. Same title as FAMU\'s lecture section of this subject. Catalogue not '
                  'reachable by automated retrieval.')},
      ],
    },
  },

  'RET3884': {
    'title': 'Clinical Practicum I: Entry-Level Respiratory Care',
    'credits': 3, 'contact_hours': 135, 'version': '1.0',
    'prerequisites': (
      'UWF requires BSC 1085/L AND BSC 1086/L AND CHM 2045/L AND MCB 2010/L. ' + PLACE + SEQ +
      'This is the FIRST placement, so every clearance has to be obtained from scratch - ask your '
      'clinical coordinator for the full list IN WRITING and keep copies, you will be asked for '
      'them again in all four practica.'),
    'offering_notes': {
      'summary': ('Credit divergence: UWF 3, FAMU 4 - in a clinical course that usually means '
                  'different required clinical hours. All FOUR practica share ONE statewide title '
                  '("Clinical Practice"), distinguishable only by their descriptions. This is the '
                  'entry-level rotation: basic therapeutics, "novice proficiency".'),
      'hours_source': 'derived',
      'derived_contact_hours': 135,
      'derivation': ('Neither carrier publishes contact hours. Clinical practicum credit is '
                     'conventionally about THREE contact hours per credit per week, so 3 credits '
                     'over 15 weeks is roughly 135 hours of clinical time. The 45-hour '
                     'classroom convention would badly misdescribe a rotation. FAMU\'s 4 credits '
                     'imply proportionally more. An order of magnitude - get your programme\'s '
                     'actual requirement.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Clinical Practicum I', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh. "Focuses on the application of basic therapeutic techniques and '
                  'procedures... supervised entry-level clinical experience via assigned rotations '
                  'at medical facilities." Competencies: clinical documentation, patient '
                  'assessment, patient safety techniques, respiratory therapeutics and diagnostics, '
                  'blood gas analysis, medical gas and medication administration, airway care. '
                  'Students demonstrate "clinical competence and novice proficiency".')},
        {'institution': 'FAMU', 'institution_name': FAMU,
         'title': 'Clinical Process and Interventions I', 'credits': 4, 'contact_hours': None,
         'note': ('4 credits - one more than UWF for the same statewide course. Catalogue not '
                  'reachable by automated retrieval.')},
      ],
    },
  },

  'RET3885': {
    'title': 'Clinical Practicum II: Critical Care',
    'credits': 3, 'contact_hours': 135, 'version': '1.0',
    'prerequisites': (
      'RET3884 (UWF). ' + PLACE + 'Clearances must be MAINTAINED and are frequently renewed - annual '
      'influenza vaccination and repeat TB screening commonly fall due mid-sequence, and a lapse '
      'stops you entering a facility. ICU rotations often require ACLS; book it early. ' + SEQ +
      'Expect 12-hour shifts more often than on general wards. This is the rotation where most '
      'students first see a patient die - that is normal, and talking to your preceptor or '
      'counselling services is a professional norm, not a weakness.'),
    'offering_notes': {
      'summary': ('Credit divergence: UWF 3, FAMU 4. FAMU\'s title adds the word "Critical", '
                  'independently confirming that the critical care transition happens at this point '
                  'in the sequence at both institutions. Statewide description calls this the '
                  'INTERMEDIATE stage, adding clinical conferences and emphasising problem-solving.'),
      'hours_source': 'derived',
      'derived_contact_hours': 135,
      'derivation': ('Neither carrier publishes contact hours. Clinical practicum credit is '
                     'conventionally about three contact hours per credit per week, so 3 credits '
                     'over 15 weeks is roughly 135 hours. FAMU\'s 4 credits imply more.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Clinical Practicum II', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh. Prerequisite RET 3884. "Further develops both basic and advanced skills '
                  'required in the intensive care of the cardiopulmonary patient... supervised '
                  'clinical experience in the critical care units via assigned rotations." Topics: '
                  'continuing Practicum I duties, airway care, mechanical ventilation management, '
                  'patient stabilisation, invasive and noninvasive monitoring, haemodynamic '
                  'evaluations, cardiopulmonary diagnostics. Students also BEGIN developing '
                  'neonatal-paediatric critical care skills.')},
        {'institution': 'FAMU', 'institution_name': FAMU,
         'title': 'Clinical Process and Critical Interventions II', 'credits': 4,
         'contact_hours': None,
         'note': ('4 credits. Title adds "Critical" relative to its Practicum I. Catalogue not '
                  'reachable by automated retrieval.')},
      ],
    },
  },

  'RET4886': {
    'title': 'Clinical Practicum III: Neonatal and Pediatric Care',
    'credits': 4, 'contact_hours': 180, 'version': '1.0',
    'prerequisites': (
      'RET3885 (UWF). MOST TIME-CRITICAL: this rotation normally requires NRP certification and '
      'often PALS BEFORE you can enter the unit - provider courses fill up, and an uncertified '
      'student cannot attend deliveries or work in the NICU. ' + PLACE + SEQ + 'WARNING: Florida\'s '
      'statewide description of this number (home and non-traditional care) does NOT match UWF\'s '
      'course (neonatal-paediatric) - the sequences differ in ORDER, so transfer on competency '
      'records, not course numbers.'),
    'offering_notes': {
      'summary': ('Both carriers award 4 credits, up from 3 at the first two practica. MAJOR '
                  'DIVERGENCE: the statewide description places home and non-traditional care at '
                  'this number while UWF places NEONATAL-PAEDIATRIC here and extended care at '
                  'RET4887. Both sequences cover the ground by the end, in a different order - which '
                  'matters for a MID-SEQUENCE transfer.'),
      'hours_source': 'derived',
      'derived_contact_hours': 180,
      'derivation': ('Neither carrier publishes contact hours. Clinical practicum credit is '
                     'conventionally about three contact hours per credit per week, so 4 credits '
                     'over 15 weeks is roughly 180 hours of clinical time.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Clinical Practicum III', 'credits': 4, 'contact_hours': None,
         'note': ('4 sh. Prerequisite RET 3885. "Provides an opportunity for students to acquire '
                  'respiratory care experience with neonatal and pediatric patients... supervised '
                  'clinical experience in the neonatal and pediatric areas of medical facilities." '
                  'Competencies: continuing Practicum I and II duties plus neonatal-paediatric '
                  'assessment, labour and delivery assistance, resuscitation methods, '
                  'pharmacological interventions and specialty diagnostics. Adult critical care '
                  'skills further developed.')},
        {'institution': 'FAMU', 'institution_name': FAMU,
         'title': 'Clinical Process / Diagnostics and Interventions III', 'credits': 4,
         'contact_hours': None,
         'note': ('4 credits. Title adds "Diagnostics", aligning with the statewide description\'s '
                  'emphasis on advanced diagnostic skills. Catalogue not reachable.')},
      ],
    },
  },

  'RET4887': {
    'title': 'Clinical Practicum IV: Entry-Level Competency Completion',
    'credits': 4, 'contact_hours': 180, 'version': '1.0',
    'prerequisites': (
      'RET4886 (UWF). ' + PLACE + SEQ + 'DEFINING REQUIREMENT: ALL entry-level competencies must be '
      'completed - a competency list, not an hours total, and some items depend on meeting a '
      'particular patient or procedure. TRACK YOUR OWN LIST FROM DAY ONE, tell your preceptor what '
      'you still need, and raise a gap with six weeks left rather than in the final fortnight, when '
      'it can delay graduation, licensure and a job start date. Start your NBRC exams and Florida '
      'licensure application BEFORE you graduate.'),
    'offering_notes': {
      'summary': ('Both carriers award 4 credits. The terminal clinical course: all entry-level '
                  'competencies must be completed. UWF covers adult, paediatric and neonatal '
                  'populations in acute critical care PLUS extended care settings (sub-acute, sleep, '
                  'home health, pulmonary rehabilitation); the statewide description instead '
                  'emphasises specialty areas.'),
      'hours_source': 'derived',
      'derived_contact_hours': 180,
      'derivation': ('Neither carrier publishes contact hours. Clinical practicum credit is '
                     'conventionally about three contact hours per credit per week, so 4 credits '
                     'over 15 weeks is roughly 180 hours. A 4-credit lecture convention would give '
                     '60, which badly misdescribes a full-time clinical rotation.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Clinical Practicum IV', 'credits': 4, 'contact_hours': None,
         'note': ('4 sh. Prerequisite RET 4886. "Provides an opportunity for students to advance '
                  'their respiratory care expertise with adult, pediatric, and neonatal patient '
                  'populations... supervised clinical experience on the critical care units of acute '
                  'care hospitals. Extended care settings such as (but not limited to) sub-acute '
                  'care, sleep, home health, and pulmonary rehabilitation will also be integrated." '
                  'ALL clinical competencies expected of new graduates for entry into practice must '
                  'be completed.')},
        {'institution': 'FAMU', 'institution_name': FAMU,
         'title': 'Clinical Process and Interventions IV', 'credits': 4, 'contact_hours': None,
         'note': ('4 credits. Catalogue not reachable by automated retrieval.')},
      ],
    },
  },

  'RET4050': {
    'title': 'Evidence-Based Practice and Research Methods in Respiratory Care',
    'credits': 2, 'contact_hours': 30, 'version': '1.0',
    'prerequisites': (
      'UWF requires HSC 4050 (health sciences research methods) - which explains the credit '
      'difference below: UWF\'s RET4050 is a 2-credit APPLIED FOLLOW-ON to a separate methods '
      'course, while Florida SouthWestern\'s 3-credit "Research Methods" reads as the standalone '
      'version teaching the methods itself. Florida\'s statewide record lists the prerequisite as '
      '"admission to the cardiopulmonary sciences program", a PROGRAMME-ADMISSION gate - you may not '
      'be able to register at all without being admitted, whatever coursework you hold. At UWF this '
      'course is also a prerequisite (with HSC 4050) for the capstone RET 4950. ' + CRED),
    'offering_notes': {
      'summary': ('Credit divergence 2 vs 3, and the PREREQUISITE explains it: UWF gates this on '
                  'HSC 4050 and teaches a 2-credit applied evidence-based-practice follow-on; '
                  'Florida SouthWestern teaches a 3-credit standalone research methods course. Both '
                  'arrive at the same place, dividing the work differently - which a receiving '
                  'programme needs to know.'),
      'hours_source': 'derived',
      'derived_contact_hours': 30,
      'derivation': ("Neither carrier publishes contact hours. 30 is Florida's convention for a "
                     "2-credit lecture, matching UWF's credit value; FSWSC's 3 credits imply "
                     'about 45.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Evidence-Based Practice in Respiratory Care', 'credits': 2, 'contact_hours': None,
         'note': ('2 sh, may not be repeated for credit. Prerequisite HSC 4050. "Focuses on the '
                  'concept of evidence-based practice and the role research plays in the field of '
                  'respiratory care. Students will acquire the skills necessary to incorporate '
                  'evidence and best practices into their professional work." An applied follow-on '
                  'to a separate research methods course.')},
        {'institution': 'FSWSC', 'institution_name': FSWSC,
         'title': 'Research Methods', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits, matching the statewide title - one more than UWF, and apparently the '
                  'standalone methods course rather than an applied follow-on. Catalogue not '
                  'retrieved for this guide.')},
      ],
    },
  },

  'RET4277': {
    'title': 'Adult Critical Care Management',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'RET3885 (UWF) - the ICU rotation this course explains. COREQUISITE RET4277L at UWF, a '
      'separate registration and a separate grade carrying the practical ventilator work; register '
      'for both. WARNING ON THE STATE RECORD: Florida\'s statewide DESCRIPTION of this number '
      'describes a survey of the profession\'s specialty areas, NOT adult critical care - but the '
      'statewide TITLE and BOTH carriers say critical care, so the description is the stale element. '
      'Read the institution\'s description, not the state\'s. Best taken alongside clinical rotation '
      'where your programme allows; waveform analysis is built by repetition, so look at the '
      'graphics on every ventilated patient. ' + CRED),
    'offering_notes': {
      'summary': ('Both public carriers award 3 credits and both titles say critical care. NOTE the '
                  'statewide description does not match its own title - it describes a specialty '
                  'survey - and THREE of four sources (title, UWF, Seminole State) agree against it, '
                  'so the DESCRIPTION is stale here rather than the title. UWF pairs a separate lab, '
                  'RET4277L.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     "3-credit lecture; the practical hours sit in UWF's corequisite RET4277L."),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Critical Care Management', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite RET 3885; corequisite '
                  'RET 4277L. "Focuses on the theory and clinical application of adult critical care '
                  'management techniques. Emphasis is placed on advanced methods of information '
                  'gathering and decision making." Topics include disease management in the '
                  'intensive care unit, invasive and non-invasive patient monitoring, haemodynamic '
                  'assessment and pharmacology.')},
        {'institution': 'SSCF', 'institution_name': SSCF,
         'title': 'Adult Critical Care', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits, matching the statewide title. Catalogue not reachable by automated '
                  'retrieval (acalog, empty responses).')},
      ],
    },
  },

  'RET4616': {
    'title': 'Respiratory Care Leadership, Administration and Education',
    'credits': 2, 'contact_hours': 30, 'version': '1.0',
    'prerequisites': (
      'RET3885 (UWF) - taken late enough that students have seen a department function. WATCH THE '
      'TITLES: the statewide title is "General Department Management" and its description lists '
      'budgets, supplies, spatial arrangements, medical-legal problems and in-service education; '
      'UWF reframes the same ground as leadership, administration and education. FAMU\'s "Advanced '
      'Seminar in Respiratory Therapy" describes a FORMAT, not a subject, and could hold a capstone '
      'review, a professional-issues survey or exam preparation - ask what it covers and KEEP THE '
      'SYLLABUS, because a generic title is the hardest kind of course to transfer. Do not '
      'underestimate this course: clinical skills get you hired, these determine where you are in '
      'ten years. ' + CRED),
    'offering_notes': {
      'summary': ('Both public carriers award 2 credits, but the three titles diverge sharply. The '
                  'statewide title and description agree on departmental administration; UWF '
                  'reframes it as leadership/administration/education - a genuine vocabulary shift '
                  'in the field rather than drift. FAMU\'s generic "Advanced Seminar" title could '
                  'not be resolved against a description.'),
      'hours_source': 'derived',
      'derived_contact_hours': 30,
      'derivation': ("Neither carrier publishes contact hours. 30 is Florida's convention for a "
                     '2-credit lecture course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Professional Healthcare Presence: Leadership, Administration, & Education',
         'credits': 2, 'contact_hours': None,
         'note': ('2 sh, may not be repeated for credit. Prerequisite RET 3885. "Explores leadership '
                  'qualities, administrative skills, and educational techniques appropriate to the '
                  'advancement of the respiratory therapist. It introduces students to leadership '
                  'theories and perspectives." The current framing of what the statewide record '
                  'calls General Department Management.')},
        {'institution': 'FAMU', 'institution_name': FAMU,
         'title': 'Advanced Seminar in Respiratory Therapy', 'credits': 2, 'contact_hours': None,
         'note': ('2 credits. A GENERIC title describing a format rather than a subject - it could '
                  'be departmental management, a capstone review, a professional-issues survey or '
                  'credentialing exam preparation. Catalogue not reachable, so the content could '
                  'not be determined. Students should keep the syllabus for transfer.')},
      ],
    },
  },

  'RET4718': {
    'title': 'Neonatal and Pediatric Respiratory Care',
    'credits': 2, 'contact_hours': 30, 'version': '1.0',
    'prerequisites': (
      'RET3885 (UWF) - adult critical care experience comes first, deliberately, since much of the '
      'neonatal material is taught by contrast with adult practice. COREQUISITE RET4718L at UWF, a '
      'separate registration and grade. PAIR IT WITH RET4886, the neonatal-paediatric clinical '
      'practicum, where your programme allows - the theory is abstract on a page and immediate at an '
      'incubator. TWO THINGS THAT CATCH ADULT-TRAINED STUDENTS: weight-based dosing has NO margin '
      '(a decimal error is a tenfold overdose, which is why units use independent double-checks), '
      'and EXCESS OXYGEN HARMS NEWBORNS - neonatal saturation targets have an upper bound as well as '
      'a lower one. ' + CRED),
    'offering_notes': {
      'summary': ('Credit divergence: UWF 2 (with a separate corequisite lab RET4718L), Seminole '
                  'State 3 - which may incorporate the practical component. Seminole State and the '
                  'statewide title both say "Critical Care" where UWF says "Respiratory Care", so '
                  'UWF\'s may extend beyond the critically ill child. The theoretical partner of the '
                  'RET4886 clinical rotation.'),
      'hours_source': 'derived',
      'derived_contact_hours': 30,
      'derivation': ("Neither carrier publishes contact hours. 30 is Florida's convention for a "
                     "2-credit lecture, matching UWF's credit value; lab hours sit in the "
                     "corequisite RET4718L. Seminole State's 3 credits imply about 45."),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Neonatal-Pediatric Respiratory Care', 'credits': 2, 'contact_hours': None,
         'note': ('2 sh, may not be repeated for credit. Prerequisite RET 3885; corequisite '
                  'RET 4718L. "Focuses on the theoretical application of clinical care specific to '
                  'neonatal and pediatric patients. Students will utilize evidence-based knowledge '
                  'and critical thinking skills in the comprehensive respiratory care" of that '
                  'population.')},
        {'institution': 'SSCF', 'institution_name': SSCF,
         'title': 'Neonatal Pediatric Critical Care', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits, matching the statewide title - one more than UWF, possibly '
                  'incorporating the practical component UWF registers separately. Catalogue not '
                  'reachable by automated retrieval.')},
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
    for k in sorted(NEW):
        p = NEW[k]['prerequisites'] or ''
        flag = ''
        if len(p) > 1000:
            flag = '  <-- OVER 1000'
            over += 1
        print('  %-9s %d cr  %4d hrs  prereq %4d chars%s'
              % (k, NEW[k]['credits'], NEW[k]['contact_hours'], len(p), flag))
    print('%d of %d over the limit' % (over, len(NEW)))


if __name__ == '__main__':
    main()
