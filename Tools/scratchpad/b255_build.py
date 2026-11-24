# -*- coding: utf-8 -*-
"""Batch 255: write the drafts for the requested courses (run from Tools/).

Sources: Seminole State catalogue (CJE2540, HUN2202), FIU Coursedog cache (HFT1102), Valencia's course
listing (HUN2202 credits and contact hours), SCNS flat file (carriers, credits, statewide titles).
"""
import io
import json
import os

G = {}

# ---------------------------------------------------------------- CJE2540
G['CJE2540'] = {
    'title': 'Police Organization and Administration',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "Seminole State College, the only Florida public carrier, lists no prerequisite; it is a lower-division "
        "criminal justice course offered in the summer term. This course does not lead to law enforcement "
        "certification: in Florida that comes only from a Criminal Justice Standards and Training Commission "
        "basic recruit academy and the State Officer Certification Examination. Florida colleges teach police "
        "administration under several numbers (CJE1300, CJE2300, CJE2302 and CJE2540), and the statewide "
        "record titles CJE2540 The Patrol Function, so a transfer evaluator may not recognise it by number: "
        "keep the syllabus."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries CJE2540: Seminole State College of Florida, at 3 credits, '
                   'typically in the summer term.',
        'hours_source': 'derived',
        'derived_contact_hours': 45,
        'derivation': 'Seminole State publishes no contact hours; 45 is Florida\'s convention for a 3-credit '
                      'lecture course (15 hours per credit).',
        'offerings': [{
            'institution': 'SSCF', 'institution_name': 'Seminole State College of Florida',
            'title': 'Police Organization and Administration', 'credits': 3, 'contact_hours': None,
            'note': 'Terms typically offered: Summer. No prerequisite listed. Statewide title: The Patrol '
                    'Function.'}],
    },
}
G['CJE2540']['html_content'] = (
    "<h2>Course Description</h2>"
    "<p><strong>CJE2540 Police Organization and Administration</strong> is a lower-division criminal justice "
    "course about how police agencies are organised and run. Seminole State College of Florida, the only Florida "
    "public institution that carries the number, describes it this way: <em>This course provides an overview of "
    "police administration and management. It examines various approaches to police organization and supervision. "
    "This course emphasizes the difference between management and leadership. Stress is placed on organization and "
    "individual values in order to accomplish common goals.</em> It carries 3 credits and is typically offered in "
    "the summer term.</p>"
    "<p>The course looks at a police department from the inside: how it is structured, who decides what, how "
    "officers are supervised, and how an agency's values become the everyday conduct of its people. Students "
    "planning a career in law enforcement, corrections or another public safety agency take it to understand the "
    "organisation they will join, and serving officers take it as a first step toward supervision.</p>"
    "<p>⚠ <strong>A note on the number.</strong> The statewide course record titles CJE2540 <strong>The Patrol "
    "Function</strong>, a different subject from the administration course Seminole State teaches under it. "
    "Seminole State's catalogue is the authority for what its course covers, and this guide follows it. Other "
    "Florida colleges teach police organisation and administration under other numbers: <strong>CJE1300</strong> "
    "(Pasco-Hernando State, State College of Florida, Gulf Coast State, Florida SouthWestern State and Palm Beach "
    "State), <strong>CJE2300</strong> (South Florida State, Indian River State, North Florida College and "
    "Hillsborough College) and <strong>CJE2302</strong> (Lake-Sumter State). Seminole State also carries an "
    "upper-division <strong>CJE4310 Police Administration</strong> for its bachelor's students.</p>"
    "<p>Because only one institution carries the number and it publishes a short description, this guide sets out "
    "what an introductory police administration course commonly covers, with the institution-specific material "
    "marked optional. The Seminole State syllabus for the term decides the readings and assignments.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3><ul class=\"list-group list-group-flush\">"
    "<li class=\"list-group-item\">Describe how a police agency is organised: the chain of command, span of "
    "control, unity of command, divisions and units, line and staff functions, and the differences between a "
    "municipal police department, a sheriff's office and a state agency.</li>"
    "<li class=\"list-group-item\">Compare approaches to police organisation, from the traditional bureaucratic "
    "(paramilitary) model to flatter, problem-oriented and community-policing structures, and say what each is "
    "good and bad at.</li>"
    "<li class=\"list-group-item\">Explain the <strong>difference between management and leadership</strong>, and "
    "apply both to situations a police supervisor meets.</li>"
    "<li class=\"list-group-item\">Describe the work of a police supervisor: assigning and directing work, "
    "evaluating performance, coaching, discipline and the first-line sergeant's role.</li>"
    "<li class=\"list-group-item\">Explain how <strong>organisational and individual values</strong>, policy, "
    "training and accountability shape officers' conduct, and how an agency aligns them toward common goals.</li>"
    "<li class=\"list-group-item\">Outline the main administrative functions of an agency: planning, budgeting, "
    "personnel (recruitment, selection, training, promotion), policy and records.</li></ul>"
    "<h3>Optional Outcomes</h3><ul class=\"list-group list-group-flush\">"
    "<li class=\"list-group-item\">Describe accreditation of law enforcement agencies and what it requires.</li>"
    "<li class=\"list-group-item\">Use crime and workload data to justify a staffing or deployment decision.</li>"
    "<li class=\"list-group-item\">Analyse a case of misconduct or a crisis in a police agency and identify the "
    "organisational failures behind it.</li></ul>"
    "<h2>Major Topics</h2><h3>Required Topics</h3><ul class=\"list-group list-group-flush\">"
    "<li class=\"list-group-item\">The development of police administration in the United States; the political, "
    "reform and community eras.</li>"
    "<li class=\"list-group-item\">Organisational structure: hierarchy, chain of command, span of control, "
    "specialisation, line and staff, organisation charts.</li>"
    "<li class=\"list-group-item\">Types of agencies in Florida: municipal police, county sheriffs (elected "
    "constitutional officers), the Florida Highway Patrol, the Florida Department of Law Enforcement and others.</li>"
    "<li class=\"list-group-item\">Management and leadership: theories of leadership, motivation, decision making, "
    "communication within the agency.</li>"
    "<li class=\"list-group-item\">Supervision: the sergeant's role, performance evaluation, discipline, early "
    "intervention.</li>"
    "<li class=\"list-group-item\">Values, ethics and integrity; policy and general orders; internal affairs and "
    "accountability.</li>"
    "<li class=\"list-group-item\">Human resources: recruitment, selection, field training, promotion, labour "
    "relations.</li>"
    "<li class=\"list-group-item\">Planning, budgeting and resource allocation; patrol deployment and "
    "workload.</li>"
    "<li class=\"list-group-item\">Community policing and problem solving as organisational strategies.</li></ul>"
    "<h3>Optional Topics</h3><ul class=\"list-group list-group-flush\">"
    "<li class=\"list-group-item\">Agency accreditation (the Commission for Florida Law Enforcement Accreditation and "
    "the national CALEA programme).</li>"
    "<li class=\"list-group-item\">Data-driven management (CompStat and similar approaches).</li>"
    "<li class=\"list-group-item\">Technology in administration: records systems, body-worn cameras, computer-aided "
    "dispatch.</li>"
    "<li class=\"list-group-item\">Patrol operations, if the course follows the statewide Patrol Function title more "
    "closely.</li></ul>"
    "<h2>Resources &amp; Tools</h2><ul>"
    "<li>A police administration textbook, such as titles by Swanson, Territo and Taylor (<em>Police "
    "Administration: Structures, Processes, and Behavior</em>) or Peak (<em>Policing America</em>); the course "
    "syllabus names the text used.</li>"
    "<li>Chapter 943, Florida Statutes, and the Criminal Justice Standards and Training Commission rules, which "
    "govern officer certification and discipline in Florida.</li>"
    "<li>The Florida Department of Law Enforcement's Uniform Crime Report data for Florida agencies.</li>"
    "<li>The Commission for Florida Law Enforcement Accreditation standards manual.</li>"
    "<li>Published general orders and annual reports of Florida agencies, for case work.</li></ul>"
    "<h2>Career Pathways</h2><ul>"
    "<li>Police and sheriff's patrol officers (SOC 33-3051), after completing a basic recruit academy.</li>"
    "<li>First-line supervisors of police and detectives (SOC 33-1012): the role the course looks toward.</li>"
    "<li>Correctional officers and supervisors, and other public safety agency staff.</li>"
    "<li>Civilian roles in police agencies: crime analysis, planning and research, records, budget.</li>"
    "<li>Florida employers include the county sheriffs' offices, municipal police departments, the Florida Highway "
    "Patrol, the Florida Department of Law Enforcement and the Florida Department of Corrections.</li></ul>"
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>"
    "<table class=\"table table-sm\"><thead><tr><th>Institution</th><th>Title</th><th>Credits</th><th>Contact "
    "hours</th></tr></thead><tbody><tr><td>Seminole State College of Florida</td><td>Police Organization and "
    "Administration</td><td>3</td><td>not published (45 by Florida's 15-hours-per-credit convention)</td></tr>"
    "</tbody></table>"
    "<p>Seminole State lists the course as typically offered in the <strong>summer term</strong>, so plan for it; a "
    "student who needs it to finish a programme may have to wait a year if a summer is missed.</p>"
    "<h3>Certification</h3><p>This course does <strong>not</strong> certify anyone as a law enforcement officer. "
    "In Florida that requires completing a basic recruit training programme approved by the Criminal Justice "
    "Standards and Training Commission and passing the State Officer Certification Examination (Chapter 943, "
    "Florida Statutes). A college course like this one supports promotion and an associate or bachelor's degree "
    "in criminal justice; it is not a substitute for the academy.</p>"
    "<h3>Transfer and course numbers</h3><p>Police administration is spread across several numbers in Florida "
    "(CJE1300, CJE2300, CJE2302, CJE2540), and the statewide title for CJE2540 names a different subject (patrol). "
    "A receiving college that teaches the subject under another number may not match CJE2540 automatically. "
    "Keep the syllabus and ask the receiving department in writing how it will count the course.</p>"
    "<h2>AI Integration (Optional)</h2>"
    "<p>Students may use AI tools to summarise readings, draft policy memos or outline organisation charts. Two "
    "cautions belong to this subject. First, a general-purpose model knows national generalities, not the law and "
    "structure of a particular Florida agency; sheriffs are elected constitutional officers and police chiefs are "
    "appointed, and that difference changes how an agency is run. Check any claim against Chapter 943, Florida "
    "Statutes, and the agency's own documents. Second, police administration is increasingly shaped by data and "
    "software (predictive deployment, early-warning systems for officer conduct), and a supervisor is accountable "
    "for decisions made with them. A course on management is a good place to ask what a tool's output does and "
    "does not justify. Follow the instructor's rules on AI use for each assignment.</p>"
)

# ---------------------------------------------------------------- HUN2202
G['HUN2202'] = {
    'title': 'Essentials of Nutrition and Diet Therapy',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        "Seminole State: BSC 2010C, or HUN 1201, or BSC 2093C or BSC 2094C (Anatomy and Physiology I or II), each "
        "with a grade of C or higher. Valencia College sets its own prerequisites, normally a biology or anatomy and "
        "physiology course; check its current catalogue. Both colleges carry the course at 3 credits as a lecture "
        "course with no laboratory. Students in nursing and other health programmes should confirm that their "
        "programme accepts this course as its nutrition requirement before registering, because some name HUN 1201 "
        "instead."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'Two Florida public institutions carry HUN2202, both at 3 credits: Seminole State College of '
                   'Florida and Valencia College.',
        'hours_source': 'mixed',
        'derived_contact_hours': 45,
        'derivation': 'Valencia lists 3 contact hours a week and no laboratory (45 over a 15-week term); Seminole '
                      'State publishes no contact hours, and 45 is Florida\'s convention for a 3-credit lecture.',
        'offerings': [
            {'institution': 'SSCF', 'institution_name': 'Seminole State College of Florida',
             'title': 'Human Nutrition and Diet Therapy', 'credits': 3, 'contact_hours': None,
             'note': 'Fall, Spring and Summer. Prerequisite BSC 2010C, HUN 1201, BSC 2093C or BSC 2094C with a C '
                     'or higher.'},
            {'institution': 'VC', 'institution_name': 'Valencia College',
             'title': 'Essentials of Nutrition and Diet Therapy', 'credits': 3, 'contact_hours': 45,
             'note': '3 contact hours a week, no laboratory. Check the current catalogue for prerequisites.'}],
    },
}
G['HUN2202']['html_content'] = (
    "<h2>Course Description</h2>"
    "<p><strong>HUN2202</strong> is a lower-division course in normal nutrition and its clinical application, "
    "written for students heading into nursing and the other health professions. Two Florida public institutions "
    "carry it, both at 3 credits: <strong>Seminole State College of Florida</strong> (<em>Human Nutrition and Diet "
    "Therapy</em>) and <strong>Valencia College</strong> (<em>Essentials of Nutrition and Diet Therapy</em>). The "
    "statewide course record titles it <strong>Principles of Nutrition, Diet, and Disease</strong>.</p>"
    "<p>Seminole State describes the course this way: <em>This course focuses on the scientific principles of normal "
    "nutrition, including specific nutrients, digestion, absorption, metabolism and nutritional requirements of "
    "different age groups. This course has a special focus on the application of nutrition principles to physical "
    "health. Emphasis is placed on the interdisciplinary team approach to disease prevention and health "
    "restoration.</em> Valencia's title names the same two halves, essentials of nutrition and diet therapy, and "
    "the two colleges carry the number at the same credit value; Valencia's catalogue was not readable for this "
    "guide, so check its course outline for any difference in emphasis.</p>"
    "<p>The course has two halves. The first is the science of normal nutrition: what the nutrients are and what the "
    "body does with them. The second is <strong>diet therapy</strong>: how diets are modified to prevent and treat "
    "disease, and how nurses and other clinicians work with registered dietitians in caring for patients. It "
    "differs from an introductory nutrition course such as HUN 1201, which covers the first half and little of the "
    "second, and Seminole State accepts HUN 1201 as one route into this course.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3><ul class=\"list-group list-group-flush\">"
    "<li class=\"list-group-item\">Identify the six classes of nutrients and describe the functions, food sources, "
    "and effects of deficiency and excess of the major vitamins and minerals.</li>"
    "<li class=\"list-group-item\">Explain the <strong>digestion, absorption, transport and metabolism</strong> of "
    "carbohydrates, lipids and proteins, and the basis of energy balance.</li>"
    "<li class=\"list-group-item\">Use the Dietary Reference Intakes, the Dietary Guidelines for Americans, MyPlate "
    "and food labels to evaluate and plan a diet.</li>"
    "<li class=\"list-group-item\">Describe nutritional needs across the life cycle: pregnancy and lactation, "
    "infancy, childhood, adolescence and older adulthood.</li>"
    "<li class=\"list-group-item\">Carry out the parts of <strong>nutrition screening and assessment</strong> a nurse "
    "or allied health worker performs, and recognise when to refer to a registered dietitian.</li>"
    "<li class=\"list-group-item\">Describe the therapeutic diets used for common conditions, including diabetes, "
    "cardiovascular disease, hypertension, kidney disease, gastrointestinal disorders, obesity, and the needs of "
    "surgery, cancer and critical illness.</li>"
    "<li class=\"list-group-item\">Explain enteral and parenteral nutrition and modified-consistency diets, and the "
    "nurse's role in feeding and monitoring patients.</li>"
    "<li class=\"list-group-item\">Describe the <strong>interdisciplinary team</strong> in disease prevention and "
    "health restoration, and the parts played by the physician, nurse, registered dietitian and others.</li></ul>"
    "<h3>Optional Outcomes</h3><ul class=\"list-group list-group-flush\">"
    "<li class=\"list-group-item\">Analyse a personal food record with diet-analysis software.</li>"
    "<li class=\"list-group-item\">Recognise drug-nutrient interactions in common medications.</li>"
    "<li class=\"list-group-item\">Adapt dietary advice to a patient's culture, budget and food access.</li></ul>"
    "<h2>Major Topics</h2><h3>Required Topics</h3><ul class=\"list-group list-group-flush\">"
    "<li class=\"list-group-item\">Nutrition standards and guidelines: DRIs, Dietary Guidelines, MyPlate, food "
    "labels.</li>"
    "<li class=\"list-group-item\">Carbohydrates, fibre, lipids and proteins.</li>"
    "<li class=\"list-group-item\">Vitamins, minerals and water; fluid and electrolyte balance.</li>"
    "<li class=\"list-group-item\">Digestion, absorption, metabolism and energy balance; weight management.</li>"
    "<li class=\"list-group-item\">Life-cycle nutrition.</li>"
    "<li class=\"list-group-item\">Nutrition screening and assessment; anthropometrics, intake, laboratory values.</li>"
    "<li class=\"list-group-item\">Hospital diets and diet progression; enteral and parenteral nutrition.</li>"
    "<li class=\"list-group-item\">Medical nutrition therapy for diabetes, cardiovascular disease, renal disease, "
    "gastrointestinal and liver disorders, cancer, and metabolic stress.</li>"
    "<li class=\"list-group-item\">The health-care team and the scope of each role in nutrition care.</li></ul>"
    "<h3>Optional Topics</h3><ul class=\"list-group list-group-flush\">"
    "<li class=\"list-group-item\">Food safety and food-borne illness.</li>"
    "<li class=\"list-group-item\">Dietary supplements and their regulation.</li>"
    "<li class=\"list-group-item\">Sports nutrition.</li>"
    "<li class=\"list-group-item\">Food insecurity and community nutrition programmes in Florida.</li></ul>"
    "<h2>Resources &amp; Tools</h2><ul>"
    "<li>A nutrition and diet therapy textbook. Seminole State's Spring 2027 section lists Rolfes, Pinna and "
    "Whitney, <em>Understanding Normal and Clinical Nutrition</em> (12th edition) with MindTap; other common texts "
    "are Grodner, <em>Nutritional Foundations and Clinical Applications: A Nursing Approach</em>, and "
    "Williams' <em>Basic Nutrition and Diet Therapy</em>.</li>"
    "<li>The Dietary Guidelines for Americans and the Dietary Reference Intakes (National Academies).</li>"
    "<li>USDA FoodData Central and a diet-analysis program for food records.</li>"
    "<li>The Academy of Nutrition and Dietetics' public materials on medical nutrition therapy.</li></ul>"
    "<h2>Career Pathways</h2><ul>"
    "<li>Registered nurses (SOC 29-1141) and licensed practical nurses (SOC 29-2061): the largest group that takes "
    "the course, since nursing programmes require nutrition.</li>"
    "<li>Dietetic technicians (SOC 29-2051) and, after a degree, dietitians and nutritionists (SOC 29-1031). In "
    "Florida dietitians and nutritionists are licensed under Part X of Chapter 468, Florida Statutes.</li>"
    "<li>Other health professions in which patients' diets matter: respiratory therapy, radiography, physical "
    "therapist assisting, health science.</li>"
    "<li>Florida employers include the large hospital systems (AdventHealth, Orlando Health, HCA Florida, BayCare), "
    "long-term care, and county health departments.</li></ul>"
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>"
    "<table class=\"table table-sm\"><thead><tr><th>Institution</th><th>Title</th><th>Credits</th><th>Contact "
    "hours</th></tr></thead><tbody>"
    "<tr><td>Seminole State College of Florida</td><td>Human Nutrition and Diet Therapy</td><td>3</td><td>not "
    "published (45 by Florida's convention)</td></tr>"
    "<tr><td>Valencia College</td><td>Essentials of Nutrition and Diet Therapy</td><td>3</td><td>3 a week, no "
    "laboratory (45 a term)</td></tr></tbody></table>"
    "<p>Both carry it at <strong>3 credits</strong> as a lecture course with no laboratory. Seminole State offers it "
    "in fall, spring and summer, including online.</p>"
    "<h3>Prerequisites</h3><p>Seminole State requires one of BSC 2010C (General Biology I), HUN 1201, or BSC 2093C or "
    "BSC 2094C (Anatomy and Physiology I or II), each with a grade of C or higher. Valencia sets its own "
    "prerequisites; check its current catalogue before registering.</p>"
    "<h3>Which nutrition course your programme wants</h3><p>Florida nursing and health programmes name their "
    "nutrition requirement by course number, and the numbers differ: some name <strong>HUN 1201</strong> (an "
    "introductory nutrition course), others HUN2202 or a similar diet-therapy course. Broward College teaches the "
    "same statewide subject as <strong>HUN 1202</strong>. Seminole State and Valencia also carry a one-credit "
    "<strong>HUN 2015 Diet Therapy for Health Care Professionals</strong>, which some programmes pair with an "
    "introductory nutrition course. Read the requirement of the programme you are applying to literally, and if "
    "you are moving between colleges, ask the receiving programme in writing whether HUN2202 meets it.</p>"
    "<h3>A note on scope</h3><p>This course teaches what a nurse or allied health worker needs to know to support a "
    "patient's nutrition care. It does not qualify anyone to prescribe therapeutic diets, which in Florida is the "
    "work of licensed dietitians and nutritionists and of physicians.</p>"
    "<h2>AI Integration (Optional)</h2>"
    "<p>AI tools can explain metabolic pathways, quiz you on nutrient functions and draft sample meal plans. Use them "
    "with care in this subject. A general model will produce a confident diet for \"a patient with kidney disease\" "
    "that ignores the stage of the disease, the laboratory values and the medications, which is exactly the "
    "category-based answer that clinical nutrition teaches you to replace with individual assessment. Generated "
    "nutrient figures are often wrong; check them against USDA FoodData Central or the course text. Never enter "
    "real patient information into a public AI tool: in clinical settings that is a breach of patient privacy "
    "under HIPAA. Follow the instructor's rules on AI use for each assignment.</p>"
)

# ---------------------------------------------------------------- HFT1102
G['HFT1102'] = {
    'title': 'Foundations & Pathways in Global Sustainable Tourism',
    'credits': 1,
    'contact_hours': 15,
    'prerequisites': (
        "None. Florida International University, the only Florida public carrier, offers it as a one-credit seminar "
        "for students in their first term in its Global Sustainable Tourism (GST) programme, in the spring term "
        "only. It is graded pass/fail. The statewide course record titles HFT1102 Sustainable Tourism Assessment and "
        "Development, a fuller subject than this orientation seminar, so it will not substitute for a 3-credit "
        "tourism course at another college."),
    'version': '1.0',
    'offering_notes': {
        'summary': 'One Florida public institution carries HFT1102: Florida International University, at 1 credit, '
                   'pass/fail, spring term only.',
        'hours_source': 'derived',
        'derived_contact_hours': 15,
        'derivation': 'FIU publishes no contact hours; 15 is Florida\'s convention for a 1-credit lecture or '
                      'seminar.',
        'offerings': [{
            'institution': 'FIU', 'institution_name': 'Florida International University',
            'title': 'Foundations & Pathways in Global Sustainable Tourism', 'credits': 1, 'contact_hours': None,
            'note': 'Chaplin School of Hospitality and Tourism Management. Spring term only; pass/fail; no '
                    'prerequisite. Statewide title: Sustainable Tourism Assessment and Development.'}],
    },
}
G['HFT1102']['html_content'] = (
    "<h2>Course Description</h2>"
    "<p><strong>HFT1102 Foundations &amp; Pathways in Global Sustainable Tourism</strong> is a one-credit seminar "
    "for students starting Florida International University's Global Sustainable Tourism (GST) programme in its "
    "Chaplin School of Hospitality and Tourism Management. FIU, the only Florida public institution that carries the "
    "number, describes it this way: <em>Seminar course for first-term GST students provides important foundations of "
    "sustainable tourism and tourism industry. Course helps students create individual paths through the program "
    "to maximize opportunities for personal growth and professional success.</em></p>"
    "<p>It is an orientation seminar with two jobs. The first is to introduce the field: what tourism is as an "
    "industry and why its environmental, social and economic effects matter. The second is to help each student "
    "plan a route through the degree and toward a career, using the electives, study abroad, internships and "
    "certifications the programme offers. FIU offers it in the <strong>spring term only</strong>, graded "
    "<strong>pass/fail</strong>, with no prerequisite. Its counterpart at the end of the programme is "
    "<strong>HFT4737 Senior Seminar in Global Sustainable Tourism</strong>.</p>"
    "<p>The statewide course record titles HFT1102 <strong>Sustainable Tourism Assessment and Development</strong>, "
    "a fuller subject than FIU's seminar; FIU's 3-credit HFT3103 Global Sustainable Tourism Development in Natural "
    "Resources is closer to that title. Because one institution carries this number and publishes a short "
    "description, the guide below sets out what such a seminar commonly covers; the FIU syllabus decides the "
    "assignments.</p>"
    "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3><ul class=\"list-group list-group-flush\">"
    "<li class=\"list-group-item\">Describe the tourism industry and its main sectors: transport, lodging, food and "
    "beverage, attractions, events, and the destination organisations that market them.</li>"
    "<li class=\"list-group-item\">Define <strong>sustainable tourism</strong> and explain its three dimensions "
    "(environmental, social and cultural, economic), with the international frameworks that describe it.</li>"
    "<li class=\"list-group-item\">Identify the positive and negative effects of tourism on destinations and "
    "communities, using Florida and international examples.</li>"
    "<li class=\"list-group-item\">Describe the career paths open to GST graduates and the skills, experience and "
    "credentials each requires.</li>"
    "<li class=\"list-group-item\">Prepare an individual plan through the programme: courses, electives, "
    "internships, study abroad and co-curricular activities matched to a career goal.</li></ul>"
    "<h3>Optional Outcomes</h3><ul class=\"list-group list-group-flush\">"
    "<li class=\"list-group-item\">Begin a professional portfolio and résumé.</li>"
    "<li class=\"list-group-item\">Research one sustainable tourism certification or award scheme.</li></ul>"
    "<h2>Major Topics</h2><h3>Required Topics</h3><ul class=\"list-group list-group-flush\">"
    "<li class=\"list-group-item\">The scale and structure of the tourism industry, worldwide and in Florida.</li>"
    "<li class=\"list-group-item\">Sustainable development and sustainable tourism: definitions, the UN Sustainable "
    "Development Goals, and the Global Sustainable Tourism Council (GSTC) criteria.</li>"
    "<li class=\"list-group-item\">Tourism's impacts: environment, communities and culture, local economies; "
    "overtourism.</li>"
    "<li class=\"list-group-item\">Career paths in sustainable tourism: destination management, ecotourism, "
    "hospitality operations, events, tour operation, non-profit and government work.</li>"
    "<li class=\"list-group-item\">Academic and career planning: the GST curriculum, advising, internships, study "
    "abroad, professional associations.</li></ul>"
    "<h3>Optional Topics</h3><ul class=\"list-group list-group-flush\">"
    "<li class=\"list-group-item\">Florida case studies: the Everglades, the Keys, coral reefs and coastal tourism, "
    "theme-park tourism in Central Florida, cruise tourism at PortMiami.</li>"
    "<li class=\"list-group-item\">Climate change and tourism.</li>"
    "<li class=\"list-group-item\">Guest speakers from the industry.</li></ul>"
    "<h2>Resources &amp; Tools</h2><ul>"
    "<li>The Global Sustainable Tourism Council criteria for destinations and for industry.</li>"
    "<li>UN Tourism (formerly the World Tourism Organization) reports and statistics.</li>"
    "<li>Visit Florida research on visitor numbers and economic impact.</li>"
    "<li>FIU's programme map for the GST degree, and its career services.</li></ul>"
    "<h2>Career Pathways</h2><ul>"
    "<li>Destination management and marketing, in organisations such as Florida's county tourist development "
    "councils and convention and visitors bureaus.</li>"
    "<li>Ecotourism and nature-based tourism, tour operation and guiding.</li>"
    "<li>Sustainability roles in hotels, resorts, cruise lines and theme parks.</li>"
    "<li>Meeting, convention and event planners (SOC 13-1121).</li>"
    "<li>Lodging managers (SOC 11-9081) and other hospitality management roles.</li>"
    "<li>Government, non-profit and international development work in tourism planning.</li></ul>"
    "<h2>Special Information</h2>"
    "<h3>Offering Notes</h3>"
    "<table class=\"table table-sm\"><thead><tr><th>Institution</th><th>Title</th><th>Credits</th><th>Contact "
    "hours</th></tr></thead><tbody><tr><td>Florida International University</td><td>Foundations &amp; Pathways in "
    "Global Sustainable Tourism</td><td>1</td><td>not published (15 by Florida's convention)</td></tr>"
    "</tbody></table>"
    "<p>Spring term only, pass/fail, no prerequisite. Students who begin the programme in the fall take it in their "
    "first spring.</p>"
    "<h3>Transfer</h3><p>This is a programme orientation seminar. A pass/fail credit may not count toward a degree "
    "requirement elsewhere, and because the statewide title names a fuller subject, a transfer evaluator should "
    "not treat it as a 3-credit sustainable tourism course. Students transferring into FIU's GST programme should "
    "ask their adviser whether they need to take it.</p>"
    "<h2>AI Integration (Optional)</h2>"
    "<p>AI tools can help draft a degree plan or résumé, but they do not know FIU's current requirements, course "
    "rotation or internship partners. Check every plan against the FIU catalogue and an adviser. Sustainability "
    "claims are also a known weak point of generated text: models repeat marketing language and invent "
    "certifications, so verify any certification against the Global Sustainable Tourism Council's list of "
    "recognised standards.</p>"
)

for cid, g in G.items():
    order = ['title', 'html_content', 'credits', 'contact_hours', 'prerequisites', 'version', 'offering_notes']
    out = {k: g[k] for k in order}
    p = os.path.join('drafts', '%s_guide.json' % cid)
    with io.open(p, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print(cid, 'html', len(out['html_content']), 'prereq', len(out['prerequisites']))
