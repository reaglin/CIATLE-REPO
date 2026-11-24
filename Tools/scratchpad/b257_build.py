# -*- coding: utf-8 -*-
"""Batch 257: CJK0031 First Aid for Criminal Justice Officers (visitor request), run from Tools/.

Sources: SCNS flat file (24 public carriers of CJK0031, 8 of CJK0031C, 2 of CJK0032, each with clock hours);
FSCJ Coursedog cache (description and the CJSTC objectives HL211-HL245, curriculum proposal 2025-12);
NWFSC Coursedog cache (description, 48 clock hours, academy-only enrolment).
Also writes CJK0031C v1.1 from the same content: same course filed under the C number (no institution carries
both), and its May 2026 guide claimed CPR/AED and other skills the CJSTC objectives do not include.
"""
import io
import json

CARRIERS = [  # (code, name, own title, clock hours) -- SCNS flat file, active rows
    ('CF', 'College of Central Florida', 'First Aid for Criminal Justice Officers', 40),
    ('CFK', 'The College of the Florida Keys', 'CMS First Aid for Criminal Justice', 40),
    ('DSC', 'Daytona State College', 'CMS First Aid for Criminal Justice Officers', 40),
    ('EFSC', 'Eastern Florida State College', 'First Aid for Criminal Justice Officers', 40),
    ('FMTC', 'Fort Myers Technical College', 'CMS First Aid for Criminal Justice Officer', 40),
    ('FSCJ', 'Florida State College at Jacksonville', 'First Aid for Criminal Justice Officers', 40),
    ('GSTC', 'George Stone Technical College', 'CMS First Aid for Criminal Justice Officer', 40),
    ('IRSC', 'Indian River State College', 'First Aid for Criminal Justice Officers', 40),
    ('LTC', 'Lake Technical College', 'CMS First Aid for Criminal Justice Officer', 40),
    ('MDC', 'Miami Dade College', 'CMS First Aid for Criminal Justice Officers', 40),
    ('MTI', 'Manatee Technical College', 'CMS First Aid for Criminal Justice Officer', 40),
    ('NFC', 'North Florida College', 'Criminal Justice CPR and First Aid', 40),
    ('NWFSC', 'Northwest Florida State College', 'First Aid for Criminal Justice Officers', 48),
    ('PBSC', 'Palm Beach State College', 'CMS First Aid for Criminal Justice Officers', 40),
    ('PHSC', 'Pasco-Hernando State College', 'First Aid for Criminal Justice Officers', 40),
    ('PSC', 'Polk State College', 'CMS First Aid for Criminal Justice Officers', 40),
    ('SCTI', 'Suncoast Technical College', 'CMS First Aid for Criminal Justice Officer', 40),
    ('SFSC', 'South Florida State College', 'First Aid for Criminal Justice Officers', 40),
    ('SJRSC', 'St. Johns River State College', 'First Aid for Criminal Justice Officers', 40),
    ('SPC', 'St. Petersburg College', 'CMS First Aid for Criminal Justice Officers', 39),
    ('TECO', 'Osceola Technical College', 'CMS First Aid for Criminal Justice Officer', 40),
    ('TSC', 'Tallahassee State College', 'First Aid for Criminal Justice Officers', 40),
    ('WHTC', 'Florida Panhandle Technical College', 'CMS First Aid for Criminal Justice Officer', 40),
    ('WTI', 'Withlacoochee Technical College', 'CMS First Aid for Criminal Justice Officer', 40),
]
C_CARRIERS = [
    ('BC', 'Broward College', 'First Aid for Criminal Justice Officers', 40),
    ('CC', 'Chipola College', 'First Aid for Criminal Justice Officers', 40),
    ('FGC', 'Florida Gateway College', 'First Aid for Criminal Justice Officers', 40),
    ('GCSC', 'Gulf Coast State College', 'Law Enforcement CMS First Aid for Criminal Justice Officers', 40),
    ('HC', 'Hillsborough College', 'CMS First Aid', 40),
    ('SFC', 'Santa Fe College', 'CMS First Aid Criminal Justice Officers', 39),
    ('SSCF', 'Seminole State College of Florida', 'First Aid for Criminal Justice', 40),
    ('VC', 'Valencia College', 'First Aid for Criminal Justice Officers', 40),
]


def li(items):
    return '<ul class="list-group list-group-flush">' + ''.join(
        '<li class="list-group-item">%s</li>' % i for i in items) + '</ul>'


def table(rows):
    return ('<table class="table table-sm"><thead><tr><th>Institution</th><th>Its title</th><th>Clock hours</th>'
            '</tr></thead><tbody>' + ''.join(
                '<tr><td>%s</td><td>%s</td><td>%d</td></tr>' % (n, t, h) for _, n, t, h in rows) +
            '</tbody></table>')


def build(cid, twin, own, other):
    html = (
        "<h2>Course Description</h2>"
        "<p><strong>%s First Aid for Criminal Justice Officers</strong> is the first-aid course of Florida's "
        "basic recruit training for criminal justice officers. It is a <strong>40-clock-hour</strong> career and "
        "technical (PSAV) course: it carries no college credit, and its content is set statewide by the "
        "<strong>Criminal Justice Standards and Training Commission (CJSTC)</strong>, so a recruit at any academy "
        "works to the same objectives. The statewide course record titles it <em>CMS First Aid for Criminal "
        "Justice Officers</em>.</p>"
        "<p>Florida State College at Jacksonville describes it this way: <em>This course introduces students to the "
        "basics of rendering first aid in a variety of situations, including during mass casualty incidents, and "
        "has a practical skills demonstration component.</em> Northwest Florida State College adds that it is "
        "<em>a component of the Law Enforcement and Correctional Officer Academy</em>, combines classroom "
        "instruction with hands-on practical demonstration, and <em>is open only to students admitted to the Law "
        "Enforcement or the Correctional Officer Academy.</em></p>"
        "<p>The course treats the officer as the person who is often first on scene before emergency medical "
        "services (EMS) arrive: deciding whether a scene is safe, assessing a patient, stopping major bleeding, "
        "moving a patient safely, and handling the medical emergencies officers meet on patrol and in "
        "corrections, including overdose and naloxone. It is offered at <strong>32 Florida public "
        "institutions</strong>: %d carry it as %s and %d as %s, with no institution carrying both "
        "(see Special Information).</p>"
    ) % (cid, len(own), cid, len(other), twin)

    html += "<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>" + li([
        "Describe the duties of a criminal justice first-aid provider within the EMS system, and the officer's "
        "responsibilities for emergency first aid under CJSTC standards.",
        "Explain the legal and ethical responsibilities of the officer as first-aid provider: duty to act, standard "
        "of care, Florida's Good Samaritan Act, abandonment, negligence, consent, do-not-resuscitate orders "
        "(DNR/DNRO), medical alerts and HIPAA; and recognise that every call for emergency medical care can be a "
        "crime scene.",
        "Communicate with patients who have special considerations.",
        "Describe the functions and main parts of the respiratory, circulatory, skeletal, muscular and nervous "
        "systems and the skin, as the basis for assessment.",
        "Prevent infection when giving first aid: universal and standard precautions, body substance isolation, "
        "hand hygiene, putting on and removing gloves, other PPE, handling biohazard material, and the "
        "transmission of hepatitis A, B and C, HIV, MRSA, COVID-19 and airborne pathogens.",
        "Size up a scene: whether it is safe to enter, trauma or medical patient, how many victims, and when more "
        "or specialised help is needed.",
        "Carry out a primary assessment (level of consciousness and AVPU; massive hemorrhage, airway, "
        "respirations, circulation, hypothermia and head injury), a secondary assessment (DOTS; pulse, motor and "
        "sensory function; medical history; pulse and breathing rates) and an ongoing assessment, and report to "
        "EMS.",
        "Lift and move patients safely (recovery position, walking assist, emergency drag, extremity lift, SEAL "
        "Team 3 carry, log roll, loading into a vehicle) and explain the factors that contribute to "
        "<strong>positional asphyxia</strong>.",
        "Act as the first officer at a mass casualty incident, triage, and work within a multi-agency response; "
        "distinguish direct threat, indirect threat and evacuation care.",
        "Recognise and treat shock; control bleeding, including <strong>tourniquet</strong> use on an extremity and "
        "junctional bleeding; and treat soft-tissue injuries, impaled objects, bites and gunshot wounds.",
        "Treat injuries to the head, neck and spine (including traumatic brain injury in adults, children and "
        "infants), eyes, chest (including an improvised chest seal), abdomen and pelvis; fractures, dislocations, "
        "sprains and amputations; and thermal, inhalation, chemical and electrical burns.",
        "Respond to medical emergencies: overdose and <strong>naloxone</strong>, fentanyl exposure, substance "
        "withdrawal, diabetic emergencies, seizures, severe asthma, stroke, heart attack, heat and cold injuries, "
        "acute abdominal pain, poisoning and anaphylaxis.",
    ])
    html += "<h3>Optional Outcomes</h3>" + li([
        "Earn a CPR/AED or basic life support certificate, where the academy schedules one alongside the course. "
        "⚠ CPR is not among the CJSTC first-aid objectives listed for this course, so ask the academy whether and "
        "where it is taught.",
        "Earn a Stop the Bleed or similar bleeding-control certificate, where the academy offers it.",
    ])

    html += "<h2>Major Topics</h2><h3>Required Topics</h3>" + li([
        "The officer's role in the EMS system; CJSTC first-aid standards.",
        "Legal and ethical issues: duty to act, standard of care, Good Samaritan Act, abandonment, negligence, "
        "consent, DNR/DNRO orders, medical alerts, HIPAA, the medical scene as a crime scene.",
        "Communicating with patients with special considerations.",
        "Body systems: respiratory, circulatory (the four major arteries), skeletal, muscular, nervous, skin.",
        "Infection control: precautions, hand hygiene, gloves and PPE, biohazard handling, bloodborne and "
        "airborne pathogens.",
        "Scene size-up; primary, secondary and ongoing assessment; communicating with EMS.",
        "Lifts, carries and moves; recovery position; positional asphyxia.",
        "Mass casualty incidents and triage; direct threat, indirect threat and evacuation care.",
        "Shock; bleeding control and tourniquets; soft-tissue injuries; impaled objects, bites, gunshot wounds.",
        "Head, neck, spine, eye, chest, abdominal, pelvic and genital injuries; fractures and amputations; burns.",
        "Overdose, naloxone and fentanyl exposure; withdrawal; diabetic emergencies and seizures; asthma, stroke "
        "and heart attack; heat and cold injuries; abdominal distress, poisoning and anaphylaxis.",
        "Practical skills demonstrations, assessed alongside written examinations.",
    ])
    html += "<h3>Optional Topics</h3>" + li([
        "CPR and AED, where the academy schedules them with this course.",
        "Additional scenario training run by the academy or a sponsoring agency.",
    ])

    html += (
        "<h2>Resources &amp; Tools</h2><ul>"
        "<li>The CJSTC basic recruit curriculum materials for first aid, which the academy issues; FDLE's "
        "Curriculum Section maintains the curriculum (Florida State College at Jacksonville's course record "
        "gives its address as Curriculum@fdle.state.fl.us).</li>"
        "<li>Training equipment for the practical demonstrations: tourniquets and bleeding-control trainers, "
        "dressings and chest-seal materials, gloves and PPE, naloxone trainers, and patient-movement "
        "equipment.</li>"
        "<li>Chapter 943, Florida Statutes, and Florida Administrative Code Chapter 11B-35, which govern basic "
        "recruit training.</li></ul>"
        "<h2>Career Pathways</h2><ul>"
        "<li>Police and sheriff's patrol officers (SOC 33-3051), after the full law enforcement academy and the "
        "State Officer Certification Examination: see the "
        "<a href=\"https://floridacourserepo.com/careers/police-officer\">Police Officer</a> career path.</li>"
        "<li>Correctional officers (SOC 33-3012), after the correctional officer academy and certification.</li>"
        "<li>The course is not an EMS credential. Anyone drawn to the medical side of public safety should look at "
        "the <a href=\"https://floridacourserepo.com/careers/paramedic\">Paramedic</a> career path, which starts "
        "with EMT training.</li></ul>"
        "<h2>Where to Learn More</h2><ul>"
        "<li><a href=\"https://floridacourserepo.com/courses/%s\">%s</a>: the same course under its other "
        "number.</li>"
        "<li><a href=\"https://floridacourserepo.com/courses/CJK0032\">CJK0032 First Aid for Criminal Justice "
        "Officers Proficiency</a>: an 8-hour proficiency course (Eastern Florida State and Pasco-Hernando "
        "State).</li>"
        "<li><a href=\"https://floridacourserepo.com/careers/police-officer\">Police Officer career path</a>: the "
        "whole route to certification, including the academy.</li></ul>"
    ) % (twin, twin)

    html += (
        "<h2>Special Information</h2>"
        "<h3>Who can take it</h3><p>This is an academy course, not an open-enrolment class. Northwest Florida State "
        "College states that it is open only to students admitted to its Law Enforcement or Correctional Officer "
        "Academy; Florida State College at Jacksonville runs it in its correctional officer programme. Admission to "
        "a Florida basic recruit academy has its own requirements (age, background, medical and fitness), set by "
        "the academy and the Commission.</p>"
        "<h3>Certification</h3><p>Passing this course does not certify anyone. It is one part of a "
        "Commission-approved basic recruit training programme; certification as a law enforcement or correctional "
        "officer follows completion of the whole programme and the State Officer Certification Examination "
        "(Chapter 943, Florida Statutes). The course carries no college credit and does not transfer as "
        "academic credit.</p>"
        "<h3>Two numbers, one course</h3><p>%d institutions carry the course as <strong>%s</strong> and %d as "
        "<strong>%s</strong>, and none carries both: the suffix is a filing choice, not a different course. All "
        "work to the same CJSTC objectives and the same 40-hour standard.</p>"
        "<h3>Offering Notes</h3><p>Clock hours as each institution records them in the statewide course file. "
        "All give 40 hours except Northwest Florida State College (48), and St. Petersburg College and Santa Fe College (39).</p>"
    ) % (len(CARRIERS), 'CJK0031', len(C_CARRIERS), 'CJK0031C')
    html += "<p><strong>Carried as CJK0031</strong></p>" + table(CARRIERS)
    html += "<p><strong>Carried as CJK0031C</strong></p>" + table(C_CARRIERS)
    html += (
        "<h3>What changed recently</h3><p>The objectives in this guide are the ones Florida State College at "
        "Jacksonville records for the course after its 2025 curriculum update. They include current material "
        "such as fentanyl exposure, naloxone, tourniquets and junctional bleeding, positional asphyxia and "
        "care under threat. Older outlines of the course may differ, so check the academy's current "
        "syllabus.</p>"
    )

    offerings = [{'institution': c, 'institution_name': n, 'title': t, 'credits': 0, 'contact_hours': h,
                  'note': 'Clock-hour course; recorded in the statewide course file.'} for c, n, t, h in own]
    for o in offerings:
        if o['institution'] == 'NWFSC':
            o['note'] = ('48 clock hours; offered as needed; open only to students admitted to the Law '
                         'Enforcement or Correctional Officer Academy.')
    return {
        'title': 'First Aid for Criminal Justice Officers',
        'html_content': html,
        'credits': 0,
        'contact_hours': 40,
        'prerequisites': (
            "Admission to a Florida Criminal Justice Standards and Training Commission basic recruit academy (law "
            "enforcement or correctional officer); the course is not open to other students. The academy sets its "
            "own admission requirements, including background, medical and fitness standards. This is a "
            "40-clock-hour course with no college credit; it does not by itself certify anyone. CPR is not among "
            "the course's CJSTC objectives, so ask the academy whether CPR/AED certification is part of the "
            "programme. The same course is numbered %s at some institutions." % twin),
        'version': '1.0' if cid == 'CJK0031' else '1.1',
        'offering_notes': {
            'summary': ('%d Florida public institutions carry %s, at 40 clock hours%s. %d more carry the same '
                        'course as %s.' % (len(own), cid, ''.join(
                            ' (%s: %d)' % (n, h) for _, n, _, h in own if h != 40), len(other), twin)),
            'hours_source': 'published',
            'offerings': offerings,
        },
    }


for cid, twin, own, other in (('CJK0031', 'CJK0031C', CARRIERS, C_CARRIERS),
                              ('CJK0031C', 'CJK0031', C_CARRIERS, CARRIERS)):
    g = build(cid, twin, own, other)
    with io.open('drafts/%s_guide.json' % cid, 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(cid, len(g['html_content']), len(g['prerequisites']))
