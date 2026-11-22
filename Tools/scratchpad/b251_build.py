# -*- coding: utf-8 -*-
"""Batch 251: write the six requested guides to drafts/ (run from Tools/).

    python scratchpad/b251_build.py

Sources (2026-11-22): SCNS flat file (carriers, credits); FIU, FAU and FSU Coursedog catalogues (FSU newly added to
coursedog.py: bulletin.fsu.edu, fsu_peoplesoft); UNF's course API (webappsapi.unf.edu); catalog.ufl.edu/search;
cloud.usf.edu course details; catalog.uwf.edu/search. FGCU (empty 202), SPC, CF and Florida Poly (acalog) not read.
"""
import io
import json
import os

LG = '<ul class="list-group list-group-flush">%s</ul>'


def lg(items):
    return LG % ''.join('<li class="list-group-item">%s</li>' % i for i in items)


def ul(items):
    return '<ul>%s</ul>' % ''.join('<li>%s</li>' % i for i in items)


def table(head, rows):
    h = ''.join('<th>%s</th>' % x for x in head)
    b = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % x for x in r) for r in rows)
    return '<table class="table table-sm table-bordered"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (h, b)


def off(inst, name, title, credits, note, hours=None):
    return {'institution': inst, 'institution_name': name, 'title': title, 'credits': credits,
            'contact_hours': hours, 'note': note}


G = {}

# ---------------------------------------------------------------------------------------------------- COM3120
G['COM3120'] = dict(
    title='Organizational Communication',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("Varies by institution. UF: COM 1000 or SPC 2300 or SPC 2608. UNF: SPC 2608 or SPC 4064. FIU, FAU, "
                   "USF and FSU list no course prerequisite in their catalogues. Upper-division (3000-level): expect "
                   "junior standing or admission to the communication major at some universities, and check whether "
                   "your programme requires a public speaking course (SPC 2608) first."),
    offering_notes={
        'summary': 'Nine Florida public institutions carry COM3120, all at 3 credits: seven universities (FAU, FGCU, '
                   'FIU, FSU, UF, UNF, USF) and two state colleges (St. Petersburg College, College of Central Florida). '
                   'FAU publishes 3 lecture hours a week.',
        'hours_source': 'mixed', 'derived_contact_hours': 45,
        'derivation': 'FAU publishes 3 lecture (contact) hours a week, 45 over a 15-week term; the other carriers '
                      'publish none, and 45 is also Florida\'s convention for a 3-credit lecture course.',
        'offerings': [
            off('FAU', 'Florida Atlantic University', 'Organizational Communication', 3,
                'Theory-centred: micro, institutional and macro analysis; political-economy, critical and '
                'poststructuralist approaches. 3 lecture hours a week.'),
            off('FGCU', 'Florida Gulf Coast University', 'Org Comm Behavior', 3,
                'State file effective August 2026. Catalogue not readable by tooling.'),
            off('FIU', 'Florida International University', 'Organizational Communication', 3,
                'Technology, corporate culture, leadership, teamwork, ethics and diversity.'),
            off('FSU', 'Florida State University', 'Communication for Organizing', 3,
                'Published outcomes: motivation, leadership theories, culture, change, conflict management.'),
            off('UF', 'University of Florida', 'Organizational Communication', 3,
                'Prerequisite COM 1000 or SPC 2300 or SPC 2608.'),
            off('UNF', 'University of North Florida', 'Organizational Communication', 3,
                'Prerequisite SPC 2608 or SPC 4064; required before the COM 4945 senior internship.'),
            off('USF', 'University of South Florida', 'Organizational Communication', 3,
                'Communication concepts that affect organizational effectiveness.'),
            off('SPC', 'St. Petersburg College', 'Organizational Communication', 3,
                'State college carrying the upper-division number. Catalogue not readable by tooling.'),
            off('CF', 'College of Central Florida', 'Organizational Communications', 3,
                'State college carrying the upper-division number. Catalogue not readable by tooling.'),
        ]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>COM3120 Organizational Communication</strong> studies how communication creates, sustains and '
        'changes organizations: how information moves through a structure, how leaders and teams talk, how culture '
        'forms, and how conflict, change and technology are handled. It is an upper-division course in the '
        'communication major, and it is also taken by students in business, management, public administration and '
        'health administration who will spend their careers inside large organizations.</p>'
        '<p>It is one of the more widely carried communication courses in Florida: <strong>nine public institutions, '
        'all at 3 credits</strong> &mdash; Florida Atlantic, Florida Gulf Coast, FIU, Florida State, UF, UNF and USF, '
        'plus two state colleges, St. Petersburg College and the College of Central Florida, which carry the '
        '3000-level number. Catalogue descriptions agree on the core, a survey of theory and research about '
        'communication in organizations, and differ in emphasis:</p>'
        + ul(['<strong>Theory-centred</strong> (FAU, UNF): FAU analyses communication at the individual, '
              'institutional and societal levels and names political-economy, critical and poststructuralist '
              'approaches; UNF surveys theory and research and how communication <em>"shapes and reshapes the '
              'activities of organizing"</em>.',
              '<strong>Applied</strong> (FSU, FIU, UF): FSU\'s published outcomes cover motivation, leadership '
              'theories, culture, change and conflict management; FIU names technology, corporate culture, '
              'leadership, teamwork, ethics and diversity; UF names structures, communication patterns, task and '
              'social roles, motivation and innovation.'])
        + '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
        + lg(['Explain the major perspectives on organizational communication: classical (scientific management, '
              'bureaucracy), human relations and human resources, systems, cultural, and critical approaches.',
              'Describe how formal structure, networks and channels shape the flow of information up, down and '
              'across an organization.',
              'Analyse an organization\'s <strong>culture</strong> &mdash; its values, stories, rituals and '
              'assumptions &mdash; and how members learn it (socialization and assimilation).',
              'Compare leadership theories and explain how leaders communicate vision, decisions and feedback.',
              'Explain how communication affects motivation, participation and teamwork.',
              'Diagnose communication problems in conflict and organizational change, and propose approaches to '
              'manage them.',
              'Evaluate the ethical responsibilities of organizational communication, including diversity, '
              'inclusion and honesty with employees and the public.'])
        + '<h3>Optional Outcomes</h3>'
        + lg(['Apply a critical lens (power, control, voice, identity) to an organization\'s communication (FAU names '
              'political-economy, critical and poststructuralist approaches).',
              'Assess the effect of communication technology &mdash; email, collaboration platforms, remote and '
              'hybrid work &mdash; on organizational life (FIU).',
              'Conduct a communication audit or case analysis of a real organization.',
              'Relate organizational communication to crisis, issues management and public relations.'])
        + '<h2>Major Topics</h2><h3>Required Topics</h3>'
        + lg(['Defining organizations and organizing; communication as constitutive of organizations.',
              'Classical, human relations and human resources approaches.',
              'Systems theory; networks and information flow.',
              'Organizational culture and socialization.',
              'Leadership and superior&ndash;subordinate communication.',
              'Groups and teams; decision making.',
              'Conflict and conflict management.',
              'Organizational change and innovation.',
              'Diversity, ethics and the organization\'s responsibility to its members.'])
        + '<h3>Optional Topics</h3>'
        + lg(['Critical and feminist approaches; power, control and resistance (emphasised at FAU).',
              'Technology and virtual organizing (emphasised at FIU).',
              'Emotion, stress and burnout at work.',
              'Organizational identity and identification.',
              'External communication: corporate image, issues management, stakeholder relations.'])
        + '<h2>Resources &amp; Tools</h2>'
        + ul(['Common texts: Miller and Barbour, <em>Organizational Communication: Approaches and Processes</em>; '
              'Eisenberg, Trethewey, LeGreco and Goodall, <em>Organizational Communication: Balancing Creativity '
              'and Constraint</em>; Modaff, Butler and DeWine, <em>Organizational Communication: Foundations, '
              'Challenges, and Misunderstandings</em>. Instructors choose; check the syllabus.',
              'Journals: <em>Management Communication Quarterly</em>, <em>Journal of Applied Communication '
              'Research</em>, <em>International Journal of Business Communication</em>.',
              'Case material from real organizations, including Florida public agencies, whose internal and external '
              'communication is a public record (Chapter 119, Florida Statutes).'])
        + '<h2>Career Pathways</h2>'
        + ul(['Human resources specialists (SOC 13-1071) and managers (11-3121).',
              'Training and development specialists (13-1151) and managers (11-3131).',
              'Public relations specialists (27-3031), including internal and employee communication roles.',
              'Management analysts and organizational development consultants (13-1111).',
              'Florida employers with large internal-communication functions: the state\'s health systems '
              '(AdventHealth, Orlando Health, BayCare), hospitality and theme-park operators, Publix, NextEra/FPL, '
              'and state and local government.'])
        + '<h2>Special Information</h2><h3>Offering Notes</h3>'
        + table(['Institution', 'Title', 'Credits', 'Notes'], [
            ['Florida Atlantic', 'Organizational Communication', '3', '3 lecture hours a week; theory-centred'],
            ['Florida Gulf Coast', 'Org Comm Behavior', '3', 'state file effective August 2026'],
            ['FIU', 'Organizational Communication', '3', 'no listed prerequisite'],
            ['Florida State', 'Communication for Organizing', '3', 'no listed prerequisite'],
            ['UF', 'Organizational Communication', '3', 'COM 1000 or SPC 2300 or SPC 2608'],
            ['UNF', 'Organizational Communication', '3', 'SPC 2608 or SPC 4064'],
            ['USF', 'Organizational Communication', '3', 'no listed prerequisite'],
            ['St. Petersburg College', 'Organizational Communication', '3', 'state college'],
            ['College of Central Florida', 'Organizational Communications', '3', 'state college']])
        + '<p><strong>All nine carry it at 3 credits.</strong> FAU publishes 3 lecture hours a week (45 over a '
          '15-week term); the others publish no contact-hour figure, and 45 is Florida\'s convention for a 3-credit '
          'lecture course. The FGCU, St. Petersburg and Central Florida catalogues could not be read for this guide, '
          'so their content is not described here.</p>'
        + '<h3>Transfer</h3><p>The shared number means the course transfers between these institutions under the '
          'Statewide Course Numbering System. Because emphasis differs (theory-centred at FAU and UNF, applied at FSU, '
          'FIU and UF), a student moving into a programme whose later courses build on critical theory, or on a '
          'communication audit, may find some ground new. Keep the syllabus. At UNF the course is one of four required '
          'before the senior internship (COM 4945).</p>'
        + '<h3>Upper division at a state college</h3><p>St. Petersburg College and the College of Central Florida are '
          'state colleges with baccalaureate programmes, which is why they carry a 3000-level number. The course '
          'counts as upper-division credit wherever it is taken.</p>'
        + '<h3>Format and workload</h3><p>Expect reading-heavy weeks, case analyses, a team project and at least one '
          'paper that applies a theory to a real organization. Plan on 6&ndash;9 hours a week outside class.</p>'
        + '<h2>AI Integration (Optional)</h2><p>Generative AI is now part of how organizations communicate: drafting '
          'announcements, summarising meetings, answering employee questions through chatbots, and analysing survey '
          'comments. The course gives students the tools to judge it. A tool can draft a change announcement quickly; '
          'it cannot know the history, trust and rumours that decide how employees will read it, and the course\'s '
          'theories of culture, voice and sensemaking explain why a technically accurate message can still fail. '
          'Generated case analyses also tend to apply theories as generic labels rather than to the evidence in the '
          'case &mdash; the very weakness graders look for. Disclose AI use, check every source it cites, and follow '
          'your instructor\'s policy.</p>'),
)

# ---------------------------------------------------------------------------------------------------- COM5235
G['COM5235'] = dict(
    title='Crisis Communication (Graduate Seminar)',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("Graduate standing; Florida State University's catalogue lists no course prerequisite. A graduate "
                   "seminar that reads and critiques original research, so prior coursework in public relations or "
                   "communication theory and research methods is strongly advised. FSU is the only Florida public "
                   "institution that carries COM5235."),
    offering_notes={
        'summary': 'One carrier, Florida State University, at 3 credits (graduate).',
        'hours_source': 'derived', 'derived_contact_hours': 45,
        'derivation': 'FSU\'s catalogue records 3 contact hours a week; 45 over a 15-week term, which is also '
                      'Florida\'s convention for a 3-credit course.',
        'offerings': [off('FSU', 'Florida State University', 'Crisis Communication', 3,
                          'Graduate seminar, School of Communication. CIP 09.0702.')]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>COM5235 Crisis Communication</strong> is a graduate seminar at <strong>Florida State '
        'University</strong>, its only Florida public carrier (3 credits). FSU\'s catalogue description: <em>"a '
        'seminar centered on the theoretical framework used in crisis communication, focuses specifically on the '
        'analysis of research conducted for the main components of a crisis (messages, responses strategies, '
        'publics) during all phases of a crisis (pre, post, during)."</em></p>'
        '<p>It is a research seminar rather than a skills workshop: students learn the main theories of crisis '
        'response, read the studies that test them, and use them to analyse real crises. It serves master\'s and '
        'doctoral students in communication, public relations, emergency management and public administration. '
        'Because one institution teaches it, this guide follows FSU\'s published description and outcomes; the '
        'theories named below are the standard ones in the field\'s research literature, and an instructor\'s '
        'reading list may differ.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3><p>FSU\'s published outcomes:</p>'
        + lg(['Define crisis communication and its main concepts.',
              'Explain the main theoretical frameworks.',
              'Compare and contrast the main theoretical frameworks used in crisis communication.',
              'Identify and evaluate the contingent conditions influential in crisis communication.',
              'Describe and explain the relationships between crisis communication and the public.',
              'Review and analyse original research.',
              'Critically analyse messages and strategies used in crisis communication situations.'])
        + '<h3>Optional Outcomes</h3>'
        + lg(['Design a study that tests a crisis-communication theory (a proposal, pilot study or literature '
              'review of publishable quality).',
              'Prepare a crisis communication plan for an organization, with stakeholder analysis, message maps and '
              'spokesperson roles.',
              'Analyse how social media and misinformation change the speed and shape of a crisis.'])
        + '<h2>Major Topics</h2><h3>Required Topics</h3>'
        + lg(['What a crisis is; crisis types and the stages of a crisis (pre-crisis, acute, post-crisis).',
              'Situational Crisis Communication Theory (Coombs): crisis responsibility, history and reputation, and '
              'matching response strategies to them.',
              'Image repair theory (Benoit): denial, evasion of responsibility, reducing offensiveness, corrective '
              'action, mortification.',
              'Contingency theory of accommodation: when an organization advocates and when it accommodates.',
              'Publics and stakeholders: who is affected, who is watching, and how they respond.',
              'Message strategies and their effects: apology, information, instruction, and their timing.',
              'Research methods in the literature: experiments, content analyses, case studies, surveys.'])
        + '<h3>Optional Topics</h3>'
        + lg(['Social-mediated crisis communication and the role of online influencers.',
              'Crisis and emergency risk communication (CERC) in public health and disasters.',
              'Discourse of renewal and organizational learning after a crisis.',
              'Rumour, misinformation and deepfakes as crisis triggers.',
              'Cultural and international differences in crisis response.'])
        + '<h2>Resources &amp; Tools</h2>'
        + ul(['W. Timothy Coombs, <em>Ongoing Crisis Communication: Planning, Managing, and Responding</em>; Coombs and '
              'Holladay (eds.), <em>The Handbook of Crisis Communication</em>; Austin and Jin (eds.), <em>Social Media '
              'and Crisis Communication</em>. Check the syllabus.',
              'Journals: <em>Public Relations Review</em>, <em>Journal of Public Relations Research</em>, <em>Journal '
              'of Contingencies and Crisis Management</em>, <em>Corporate Communications: An International '
              'Journal</em>.',
              'CDC, <em>Crisis and Emergency Risk Communication (CERC)</em> manual; FEMA public information training; '
              'the Florida Division of Emergency Management\'s hurricane communication.'])
        + '<h2>Career Pathways</h2>'
        + ul(['Public relations specialists (SOC 27-3031) and public relations managers (11-2032).',
              'Public information officers in government, utilities, schools and law enforcement.',
              'Emergency management directors (11-9161) and emergency management staff.',
              'Communication roles in hospitals and health systems, universities, and corporate risk and reputation '
              'teams; crisis consultancies.',
              'Doctoral study and academic research in public relations and crisis communication.'])
        + '<h2>Special Information</h2><h3>Offering Notes</h3>'
        '<p><strong>One carrier: Florida State University, 3 credits, graduate level</strong> (School of '
        'Communication). FSU records 3 contact hours a week, 45 over a term.</p>'
        '<h3>Florida context</h3><p>Florida supplies an unusually rich set of cases: hurricanes every season, the 2021 '
        'collapse of Champlain Towers South in Surfside, red tide, and public-health emergencies. ⚠ For a Florida '
        'public agency, crisis communication happens in public: its email and text messages are public records '
        '(Chapter 119, Florida Statutes) and board discussions fall under the Sunshine Law (Chapter 286). What is '
        'written during a crisis may be published later, which shapes how a public organization should communicate '
        'in the moment.</p>'
        '<h3>Transfer and level</h3><p>A graduate course: it does not count toward an undergraduate degree unless a '
        'university allows it under a combined bachelor\'s/master\'s arrangement. No other Florida public institution '
        'carries COM5235; similar content elsewhere sits under public relations (PUR) numbers. Keep the syllabus.</p>'
        '<h3>Format</h3><p>A seminar: weekly readings of research articles, student-led discussion, critiques, and a '
        'major paper. Expect 9&ndash;12 hours a week outside class.</p>'
        '<h2>AI Integration (Optional)</h2><p>Organizations now use AI to monitor social media during a crisis, to '
        'detect a story early, and to draft holding statements in minutes. The course\'s research explains where '
        'that helps and where it fails. Speed is useful; accuracy and responsibility are what the theories reward, '
        'and a generated statement can attribute or deny responsibility in ways the evidence does not support, which '
        'is the mistake Situational Crisis Communication Theory warns against. Generative AI also creates new crises '
        '(fabricated audio, images and statements attributed to an organization). For the seminar, use AI only as your '
        'instructor allows, and never to summarise a research article you have not read: generated summaries of '
        'studies regularly misstate their methods and findings, and invent citations.</p>'),
)

# ---------------------------------------------------------------------------------------------------- ATR2000
G['ATR2000'] = dict(
    title='Basic Care and Prevention Principles of Athletic Training',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("None listed. Offered at the University of West Florida, its only Florida public carrier, as a "
                   "lower-division course recommended in UWF's Exercise Science B.S. A first course for students "
                   "considering athletic training, which in Florida requires a master's degree from a CAATE-"
                   "accredited programme, BOC certification and a state licence."),
    offering_notes={
        'summary': 'One carrier, the University of West Florida, at 3 credits (state file effective January 2026).',
        'hours_source': 'derived', 'derived_contact_hours': 45,
        'derivation': 'Florida convention of 15 contact hours per credit for a lecture course; UWF publishes none.',
        'offerings': [off('UWF', 'University of West Florida', 'Basic Care and Prevention Principles of Athletic '
                          'Training', 3, 'Department of Movement Sciences and Health. State statewide title: '
                          'Exercise Science and Injury Management.')]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>ATR2000</strong> is an introduction to athletic training at the <strong>University of West '
        'Florida</strong>, its only Florida public carrier (3 credits; new in the state file in January 2026). UWF\'s '
        'catalogue description: <em>"This course provides an overview of the athletic training profession, its role '
        'within sports medicine, and the foundational knowledge and skills necessary for preventing, recognizing, and '
        'managing common injuries and illnesses in physically active populations. Students will explore the history, '
        'scope of practice, professional standards, and collaborative nature of athletic training within the '
        'healthcare team. Emphasis will be placed on injury prevention strategies, emergency management, basic '
        'evaluation techniques, therapeutic interventions, and rehabilitation principles."</em></p>'
        '<p>It is a lower-division survey for students in exercise science, kinesiology, coaching and pre-health '
        'programmes, and for anyone deciding whether to pursue athletic training. It does not by itself qualify '
        'anyone to practise. The state file\'s statewide title for the number is <em>Exercise Science and Injury '
        'Management</em>; UWF\'s description is what this guide follows.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
        + lg(['Describe the athletic training profession: its history, scope of practice, professional standards and '
              'credentials, and its place on the sports medicine team.',
              'Explain how athletic trainers work with physicians, physical therapists, coaches, parents and other '
              'health professionals.',
              'Apply injury-prevention strategies: pre-participation screening, conditioning, protective equipment, '
              'environmental precautions and an emergency action plan.',
              'Recognise common injuries and illnesses in physically active people and the signs that demand '
              'emergency care.',
              'Describe basic evaluation techniques and the first steps of management.',
              'Explain the principles of therapeutic intervention and rehabilitation.'])
        + '<h3>Optional Outcomes</h3>'
        + lg(['Practise basic taping and wrapping.',
              'Recognise heat illness, concussion, sudden cardiac arrest and exertional sickling, and describe the '
              'current emergency response to each.',
              'Plan the route to a career in athletic training, including graduate admission requirements.'])
        + '<h2>Major Topics</h2><h3>Required Topics</h3>'
        + lg(['The athletic training profession and the sports medicine team; legal and ethical considerations.',
              'Pre-participation examination and injury prevention.',
              'Emergency action plans and emergency care.',
              'Tissue response to injury and the healing process.',
              'Injury recognition and basic evaluation by body region.',
              'Introduction to therapeutic modalities and rehabilitation.'])
        + '<h3>Optional Topics</h3>'
        + lg(['Environmental conditions: heat, humidity and lightning, a daily concern in Florida.',
              'Concussion recognition and return-to-play.',
              'Protective equipment fitting; taping and bracing.',
              'Nutrition, hydration and general medical conditions.'])
        + '<h2>Resources &amp; Tools</h2>'
        + ul(['Introductory texts such as Prentice, <em>Principles of Athletic Training: A Guide to Evidence-Based '
              'Clinical Practice</em>, or France, <em>Introduction to Athletic Training</em>. Check the syllabus.',
              'National Athletic Trainers\' Association (NATA) position statements, for example on exertional heat '
              'illness and sudden death in sport.',
              'Board of Certification (BOC) and the Commission on Accreditation of Athletic Training Education '
              '(CAATE) websites for the credential route.'])
        + '<h2>Career Pathways</h2>'
        + ul(['Athletic trainers (SOC 29-9091), after a CAATE-accredited master\'s degree, BOC certification and a '
              'Florida licence.',
              'Related routes this course introduces: physical therapy, occupational therapy, physician assistant, '
              'strength and conditioning, exercise physiology, coaching.',
              'Florida settings: high schools, colleges and universities, professional and spring-training teams, '
              'orthopaedic and sports medicine clinics (AdventHealth, Orlando Health, BayCare, HCA Florida), '
              'industrial and military settings.'])
        + '<h2>Special Information</h2><h3>Offering Notes</h3>'
        '<p><strong>One carrier: the University of West Florida, 3 credits</strong> (Department of Movement Sciences '
        'and Health). UWF publishes no contact-hour figure; the 45 shown are derived from Florida\'s convention of 15 '
        'per credit.</p>'
        '<h3>⚠ The route to practising as an athletic trainer</h3><p>The professional degree in athletic training is '
        'now a <strong>master\'s degree</strong>: CAATE accredits professional programmes only at the master\'s level, '
        'and graduation from one is what makes a candidate eligible for the BOC examination. Florida then requires a '
        'licence from the Board of Athletic Training (Part XIII of Chapter 468, Florida Statutes). Florida public '
        'universities with graduate athletic training courses include UWF, UNF, FIU, USF and UCF. An undergraduate '
        'course such as ATR2000 is preparation and exploration, not part of the credential; check each master\'s '
        'programme\'s prerequisites (typically anatomy and physiology, exercise physiology, kinesiology, chemistry, '
        'physics, psychology and observation hours) early.</p>'
        '<h3>Transfer</h3><p>No other Florida public institution carries ATR2000. Florida State carries ATR2020 First '
        'Aid, a different course. Keep the syllabus if you transfer.</p>'),
)

# ---------------------------------------------------------------------------------------------------- ATR5105C
G['ATR5105C'] = dict(
    title='Foundations of Athletic Training (Athletic Training Techniques)',
    credits=3, contact_hours=60, version='1.0',
    prerequisites=("Admission to a graduate (master's) professional athletic training programme. FIU: admittance to "
                   "the Athletic Training Program, with corequisites ATR 5115C and ATR 5805. UNF, USF and UWF list no "
                   "other prerequisite. Taken in the first term; it is the gate to later clinical courses (at UNF, "
                   "ATR 5217C, 5306C and 5815C require it). Credits differ: 3 at UNF, USF and UWF, 4 at FIU."),
    offering_notes={
        'summary': 'Four Florida public universities carry ATR5105C, each in its graduate athletic training '
                   'programme: UNF, USF and UWF at 3 credits, FIU at 4. Titles differ.',
        'hours_source': 'derived', 'derived_contact_hours': 60,
        'derivation': 'Florida convention for a 3-credit integrated lecture-and-laboratory (C) course; UNF states 2 '
                      'credit hours of lecture and 1 of laboratory. FIU\'s 4-credit form would be about 75 by the '
                      'same convention. No carrier publishes a term contact-hour figure.',
        'offerings': [
            off('UNF', 'University of North Florida', 'Foundations in Athletic Training', 3,
                '2 credits lecture + 1 credit lab. Acute care, risk management, taping and bracing, equipment fitting.'),
            off('FIU', 'Florida International University', 'Principles of Athletic Training with Lab', 4,
                'Admittance to the programme; corequisites ATR 5115C, ATR 5805.'),
            off('USF', 'University of South Florida', 'Athletic Training Techniques', 3,
                'Morsani College of Medicine, School of Physical Therapy and Rehabilitation Sciences.'),
            off('UWF', 'University of West Florida', 'Advanced Principles in Athletic Training', 3,
                'Prevention and risk reduction; tape, braces and orthopaedic devices.'),
        ]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>ATR5105C</strong> is the opening clinical-skills course of a graduate professional athletic '
        'training programme, with an integrated laboratory. Four Florida public universities carry it: '
        '<strong>UNF, USF and UWF at 3 credits, and FIU at 4</strong>. The statewide title is <em>Athletic Training '
        'Techniques</em>, and each university names it differently.</p>'
        + table(['University', 'Its title', 'Its description, in brief'], [
            ['UNF', 'Foundations in Athletic Training', 'acute care, risk management, orthopaedic taping and bracing, '
             'equipment fitting; roles of the certified athletic trainer and sports medicine team'],
            ['FIU', 'Principles of Athletic Training with Lab', 'the profession, risk management, the evaluation '
             'process, medical documentation'],
            ['USF', 'Athletic Training Techniques', 'prevention, recognition, evaluation and immediate care of '
             'athletic injuries'],
            ['UWF', 'Advanced Principles in Athletic Training', 'prevention of acute and chronic conditions, risk '
             'reduction, selecting, fabricating and applying tape, braces and orthopaedic devices']])
        + '<p>The common ground is clear: <strong>the profession, prevention and risk management, and the hands-on '
          'skills of taping, bracing and equipment</strong>, with immediate care and the start of injury evaluation. '
          'It is taken in the first term, before students begin supervised clinical placements.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
        + lg(['Describe the roles and responsibilities of the certified athletic trainer and the sports medicine '
              'team, and the professional, legal and ethical standards that govern practice.',
              'Apply risk-management principles: pre-participation screening, emergency action plans, environmental '
              'monitoring and facility and equipment safety.',
              'Select, fit and apply tape, wraps, braces and protective equipment for prevention and protection.',
              'Recognise acute injuries and illnesses and provide immediate care.',
              'Describe the structure of an injury evaluation and document care in a medical record.'])
        + '<h3>Optional Outcomes</h3>'
        + lg(['Fabricate custom pads and splints (UWF).',
              'Use standardised medical documentation and terminology (FIU).',
              'Manage medical emergencies in sport, with corequisite emergency care training (FIU\'s ATR 5115C).'])
        + '<h2>Major Topics</h2><h3>Required Topics</h3>'
        + lg(['The athletic training profession; BOC, CAATE and state licensure.',
              'Risk management and injury prevention; pre-participation examination.',
              'Emergency action planning and acute care.',
              'Orthopaedic taping, wrapping and bracing (laboratory).',
              'Protective equipment selection and fitting (laboratory).',
              'Introduction to evaluation and documentation.'])
        + '<h3>Optional Topics</h3>'
        + lg(['Environmental illness: heat, humidity and lightning.',
              'Custom orthotic and padding fabrication.',
              'Electronic medical records and injury surveillance.'])
        + '<h2>Resources &amp; Tools</h2>'
        + ul(['Prentice, <em>Principles of Athletic Training</em>; Perrin, <em>Athletic Taping and Bracing</em>. '
              'Check the syllabus.',
              'NATA position statements; BOC <em>Standards of Professional Practice</em>; the current BOC Practice '
              'Analysis, which sets the examination content.',
              'Laboratory supplies: tape, elastic wraps, braces, padding, and protective equipment for fitting; '
              'programmes charge course fees for them (UNF lists $30).'])
        + '<h2>Career Pathways</h2>'
        + ul(['Athletic trainers (SOC 29-9091), after graduation, BOC certification and a Florida licence from the '
              'Board of Athletic Training.',
              'Florida settings: high schools, colleges, professional and spring-training teams, orthopaedic clinics '
              'and hospital outreach (AdventHealth, Orlando Health, BayCare, HCA Florida), performing arts, '
              'industry and the military.'])
        + '<h2>Special Information</h2><h3>Offering Notes</h3>'
        + table(['University', 'Credits', 'Notes'], [
            ['UNF', '3', '2 lecture + 1 laboratory'], ['FIU', '4', 'corequisites ATR 5115C, ATR 5805'],
            ['USF', '3', 'School of Physical Therapy and Rehabilitation Sciences'], ['UWF', '3', '']])
        + '<p>⚠ <strong>FIU carries the course at 4 credits; UNF, USF and UWF at 3.</strong> No carrier publishes a '
          'term contact-hour figure; the 60 shown are derived from Florida\'s convention for a 3-credit integrated '
          'course (FIU\'s 4-credit form would be about 75).</p>'
        '<h3>Professional programme, not an elective</h3><p>This is a course inside a CAATE-accredited master\'s '
        'programme, open only to admitted students, taken in a fixed sequence with its partners. It is not normally '
        'transferable between programmes: a student who moves would be placed by the new programme\'s own review. '
        'Completing the programme makes a graduate eligible for the BOC examination; Florida practice then requires '
        'a licence (Part XIII of Chapter 468, Florida Statutes).</p>'
        '<h3>Before the first term</h3><p>Programmes typically require current emergency cardiac care certification, '
        'immunisations, a background check and liability insurance before clinical work begins. Start these '
        'early.</p>'),
)

# ---------------------------------------------------------------------------------------------------- ATR5305C
G['ATR5305C'] = dict(
    title='Therapeutic Interventions in Athletic Training I',
    credits=4, contact_hours=75, version='1.0',
    prerequisites=("Florida International University only, in its graduate (MS) athletic training programme: "
                   "prerequisites ATR 5105C, ATR 5115C and ATR 5805; corequisites ATR 5217C and ATR 5815L. UNF, USF "
                   "and UCF teach the same subject under a different number, ATR 5306C Therapeutic Interventions I "
                   "(3 or 4 credits), so check which number your programme uses."),
    offering_notes={
        'summary': 'One carrier, Florida International University, at 4 credits. UNF (3), USF (4) and UCF (3) teach '
                   'Therapeutic Interventions I as ATR5306C.',
        'hours_source': 'derived', 'derived_contact_hours': 75,
        'derivation': 'Florida convention for a 4-credit integrated course taken as 3 lecture credits (45 hours) and 1 '
                      'laboratory credit (30 hours); FIU publishes no contact-hour figure or split.',
        'offerings': [off('FIU', 'Florida International University', 'Therapeutic Interventions in Athletic '
                          'Training I', 4, 'Prerequisites ATR 5105C, ATR 5115C, ATR 5805; corequisites ATR 5217C, '
                          'ATR 5815L. State statewide title: Therapeutic Modalities with Lab.')]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>ATR5305C</strong> is the first therapeutic-interventions course in <strong>Florida International '
        'University</strong>\'s graduate athletic training programme, its only Florida public carrier (4 credits, '
        'with a laboratory). FIU\'s description: <em>"Introduction to therapeutic modalities and rehabilitation '
        'techniques encountered in athletic training practice for acute injuries, including application of '
        'associated clinical skills."</em> The statewide title is <em>Therapeutic Modalities with Lab</em>.</p>'
        '<p>It teaches how athletic trainers treat injuries after the acute stage: the physical agents (cold, heat, '
        'ultrasound, electrical stimulation and others) and the early rehabilitation exercise that together move a '
        'patient from injury toward return to activity. Because one university carries the number, this guide follows '
        'FIU\'s description, and draws on the same course at UNF (ATR 5306C), whose catalogue covers <em>"basic '
        'physics, physiological effects, indications, and contraindications for therapeutic modalities"</em>.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
        + lg(['Explain the stages of tissue healing and how therapeutic interventions support each stage.',
              'Describe the physics and physiological effects of cryotherapy, thermotherapy, therapeutic ultrasound, '
              'electrical stimulation, and mechanical modalities such as compression and traction.',
              'Identify the indications, contraindications and precautions for each modality.',
              'Select and safely apply modalities in the laboratory, setting parameters and documenting treatment.',
              'Design early rehabilitation for acute injuries: range of motion, flexibility, neuromuscular control and '
              'strengthening.',
              'Use patient-reported outcomes and clinical measures to evaluate a treatment and adjust it.'])
        + '<h3>Optional Outcomes</h3>'
        + lg(['Apply the evidence for each modality critically, including where it is weak.',
              'Use pain science to explain treatment choices to a patient.',
              'Describe newer interventions (for example, photobiomodulation or blood-flow-restriction training) and '
              'their evidence and regulation.'])
        + '<h2>Major Topics</h2><h3>Required Topics</h3>'
        + lg(['Inflammation and tissue repair; pain and its modulation.',
              'Cryotherapy and thermotherapy.',
              'Therapeutic ultrasound.',
              'Electrical stimulation: currents, parameters, pain control and muscle re-education.',
              'Compression, traction and other mechanical modalities.',
              'Principles of rehabilitation for acute injuries; therapeutic exercise.',
              'Documentation and safety; indications and contraindications.'])
        + '<h3>Optional Topics</h3>'
        + lg(['Evidence-based practice and clinical outcome measures.',
              'Manual therapy techniques introduced before the second course.',
              'Shortwave diathermy, laser and other specialised modalities.'])
        + '<h2>Resources &amp; Tools</h2>'
        + ul(['Starkey, <em>Therapeutic Modalities</em>; Knight and Draper, <em>Therapeutic Modalities: The Art and '
              'Science</em>; Prentice, <em>Rehabilitation Techniques for Sports Medicine and Athletic Training</em>. '
              'Check the syllabus.',
              'Laboratory equipment: ultrasound and electrical stimulation units, hot and cold packs, whirlpool, '
              'compression devices; FIU charges a course fee.',
              'BOC Practice Analysis (therapeutic intervention domain); NATA position statements.'])
        + '<h2>Career Pathways</h2>'
        + ul(['Athletic trainers (SOC 29-9091), after the master\'s degree, BOC certification and a Florida licence.',
              'The same skills are used in physical therapy and sports medicine clinics, hospital outreach and '
              'industrial rehabilitation in Florida (AdventHealth, Orlando Health, BayCare, HCA Florida).'])
        + '<h2>Special Information</h2><h3>Offering Notes</h3>'
        '<p><strong>One carrier: FIU, 4 credits.</strong> FIU publishes no contact-hour figure; the 75 shown are '
        'derived from Florida\'s convention, reading 4 credits as 3 of lecture (45 hours) and 1 of laboratory (30 '
        'hours).</p>'
        '<h3>⚠ The same subject under a neighbouring number</h3>'
        + table(['University', 'Number', 'Title', 'Credits'], [
            ['FIU', 'ATR5305C', 'Therapeutic Interventions in Athletic Training I', '4'],
            ['UNF', 'ATR5306C', 'Therapeutic Interventions I', '3'],
            ['USF', 'ATR5306C', 'Therapeutic Interventions I', '4'],
            ['UCF', 'ATR5306C', 'Therapeutic Interventions in Athletic Training Practice I', '3']])
        + '<p>Course numbers do not match across these programmes, and the credits differ too. Because these are '
          'courses in a fixed, cohort-based professional programme, a transfer between programmes is decided by the '
          'receiving programme\'s review rather than by the number. Keep the syllabus and laboratory competency '
          'records.</p>'
        '<h3>Position in the programme</h3><p>At FIU it follows the first-term courses (ATR 5105C Principles of '
        'Athletic Training, ATR 5115C Management of Medical Emergencies and ATR 5805) and is taken with ATR 5217C and '
        'the clinical course ATR 5815L, so laboratory skills are used in supervised clinical practice the same term.</p>'
        '<h3>Safety</h3><p>Modalities can burn, shock or worsen an injury when applied without checking the '
        'contraindications. Programmes test laboratory competency before students use them on patients. In Florida, '
        'the athletic trainer\'s scope is set by statute and Board of Athletic Training rule (Part XIII of Chapter '
        '468, Florida Statutes).</p>'),
)

# ---------------------------------------------------------------------------------------------------- BME4311
G['BME4311'] = dict(
    title='Molecular Engineering (Molecular Biomedical Engineering)',
    credits=3, contact_hours=45, version='1.0',
    prerequisites=("Varies. UF: BSC 2010 and (CHM 3217 or CHM 2210) and PCB 3713C, each with a minimum grade of C. "
                   "FIU and Florida Polytechnic list none in the catalogue sources read. Expect general biology and "
                   "organic chemistry first. An upper-division course for biomedical engineering juniors and seniors; "
                   "content differs by school (UF: molecular and cell biology; FIU: genetic and protein engineering)."),
    offering_notes={
        'summary': 'Three Florida public universities carry BME4311, each at 3 credits: FIU, UF and Florida '
                   'Polytechnic (state file effective August 2026). Titles and emphasis differ.',
        'hours_source': 'derived', 'derived_contact_hours': 45,
        'derivation': 'Florida convention of 15 contact hours per credit for a lecture course; no carrier publishes '
                      'a term contact-hour figure.',
        'offerings': [
            off('FIU', 'Florida International University', 'Molecular Engineering', 3,
                'Molecular biology, genetic engineering and proteomic engineering.'),
            off('UF', 'University of Florida', 'Molecular Biomedical Engineering', 3,
                'Prerequisites BSC 2010, CHM 3217 or CHM 2210, PCB 3713C (C or better).'),
            off('FLPOLY', 'Florida Polytechnic University', 'Biomolecular Engineering', 3,
                'State file effective August 2026. Catalogue not readable by tooling.'),
        ]},
    html=(
        '<h2>Course Description</h2>'
        '<p><strong>BME4311</strong> brings molecular biology into biomedical engineering: the molecules of the cell, '
        'how genes and proteins work, and how engineers measure and change them. Three Florida public universities '
        'carry it, each at 3 credits, under different titles and with different emphasis:</p>'
        + table(['University', 'Title', 'Emphasis'], [
            ['UF', 'Molecular Biomedical Engineering', 'molecular and cell biology for engineers: the eukaryotic cell, '
             'protein structure and function, enzymes, DNA, organelles, mitochondria and energy, cell communication, '
             'the extracellular matrix'],
            ['FIU', 'Molecular Engineering', 'molecular biology, <strong>genetic engineering</strong> and '
             '<strong>proteomic engineering</strong>'],
            ['Florida Polytechnic', 'Biomolecular Engineering', 'new in the state file (August 2026); no description '
             'could be read for this guide']])
        + '<p>UF\'s course is the foundation: it teaches the vocabulary and current knowledge of the cell that a '
          'biomedical engineer needs. FIU\'s description points further, to engineering the molecules themselves. With '
          'three carriers and two different emphases, students should read their own syllabus; this guide marks what '
          'is common and what depends on the school.</p>'
        '<h2>Learning Outcomes</h2><h3>Required Outcomes</h3>'
        + lg(['Describe the structure and function of proteins, nucleic acids, lipids and carbohydrates.',
              'Explain the central dogma: DNA replication, transcription, translation and gene regulation.',
              'Describe enzyme kinetics and how enzymes are characterised (Michaelis&ndash;Menten).',
              'Explain the organisation of the eukaryotic cell: membranes, organelles, the cytoskeleton, and energy '
              'conversion in mitochondria.',
              'Describe how cells communicate and interact with the extracellular matrix, and why that matters for '
              'tissue engineering and medical devices.',
              'Read the molecular-biology literature with the nomenclature of the field.'])
        + '<h3>Optional Outcomes</h3>'
        + lg(['Explain recombinant DNA methods: cloning, PCR, expression systems, and genome editing with CRISPR '
              '(emphasised at FIU).',
              'Describe protein engineering and proteomics: directed evolution, rational design, mass spectrometry '
              '(emphasised at FIU).',
              'Apply molecular methods to biomedical problems such as biosensors, drug delivery and gene therapy.',
              'Discuss the ethics and regulation of genetic engineering.'])
        + '<h2>Major Topics</h2><h3>Required Topics</h3>'
        + lg(['Biomolecules and protein structure; folding and function.',
              'Enzymes and kinetics.',
              'DNA structure, replication, transcription and translation; gene expression.',
              'Cell structure and organelles; membranes and transport.',
              'Bioenergetics: mitochondria (and chloroplasts, at UF).',
              'Cell signalling and the extracellular matrix.'])
        + '<h3>Optional Topics</h3>'
        + lg(['Genetic engineering tools: restriction enzymes, vectors, PCR, sequencing, CRISPR.',
              'Proteomics and protein engineering.',
              'Molecular diagnostics and biosensors.',
              'Bioinformatics and protein-structure databases.'])
        + '<h2>Resources &amp; Tools</h2>'
        + ul(['Alberts et al., <em>Molecular Biology of the Cell</em>, or Lodish et al., <em>Molecular Cell Biology</em>; '
              'engineering-oriented texts on molecular and protein engineering. Check the syllabus.',
              'Databases: NCBI (GenBank, PubMed), UniProt, the RCSB Protein Data Bank; visualisation in PyMOL or '
              'ChimeraX.',
              'Biomedical Engineering Society (BMES).'])
        + '<h2>Career Pathways</h2>'
        + ul(['Bioengineers and biomedical engineers (SOC 17-2031).',
              'Biochemists and biophysicists (19-1021) and medical scientists (19-1042), usually after graduate '
              'study; medical school.',
              'Biotechnology, diagnostics and pharmaceutical research and manufacturing; Florida centres include '
              'Alachua (UF Innovate | Sid Martin Biotech), Lake Nona Medical City in Orlando, the Jupiter research '
              'campus, and Tampa Bay (Moffitt Cancer Center).'])
        + '<h2>Special Information</h2><h3>Offering Notes</h3>'
        + table(['University', 'Title', 'Credits'], [
            ['FIU', 'Molecular Engineering', '3'], ['UF', 'Molecular Biomedical Engineering', '3'],
            ['Florida Polytechnic', 'Biomolecular Engineering', '3']])
        + '<p><strong>All three carry it at 3 credits.</strong> None publishes a term contact-hour figure; the 45 shown '
          'are derived from Florida\'s convention of 15 per credit. Florida Polytechnic\'s catalogue could not be read '
          'for this guide.</p>'
        '<h3>Transfer</h3><p>The shared number transfers between the three universities, but the content differs: a '
        'student from UF\'s cell-biology course moving to FIU may meet genetic-engineering methods for the first time, '
        'and the reverse. Keep the syllabus.</p>'
        '<h3>Position in the curriculum</h3><p>A junior or senior course. At UF it follows general biology, organic '
        'chemistry and PCB 3713C (physiology), and the gate is a C in each. Molecular biology is not the main FE '
        'exam content for biomedical engineers, but it is the background for later tissue engineering, biomaterials '
        'and biosensor courses.</p>'
        '<h2>AI Integration (Optional)</h2><p>AI has changed this field. Protein-structure prediction (AlphaFold and '
        'its successors) and protein language models now let engineers predict a structure or propose a new protein '
        'in hours; design tools suggest guide RNAs for CRISPR and optimise DNA sequences for expression. The course '
        'teaches the biology needed to judge their output: a predicted structure has confidence scores that matter, a '
        'designed protein must still fold, be expressed and be tested, and a model trained on known proteins is least '
        'reliable on the unusual ones engineers often want. General chat tools also make confident errors about '
        'pathways, kinetics and gene names. Check every claim against a primary source or database, and follow your '
        'instructor\'s policy.</p>'),
)

if __name__ != '__main__':
    G = {}  # imported for the helpers (b251_build2.py): do not rewrite the pushed drafts
os.makedirs('drafts', exist_ok=True)
for cid, g in G.items():
    d = {'title': g['title'], 'html_content': g['html'], 'credits': g['credits'],
         'contact_hours': g['contact_hours'], 'prerequisites': g['prerequisites'], 'version': g['version'],
         'offering_notes': g['offering_notes']}
    path = os.path.join('drafts', '%s_guide.json' % cid)
    with io.open(path, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
    print('%-9s html %5d prereq %4d -> %s' % (cid, len(g['html']), len(g['prerequisites']), path))
