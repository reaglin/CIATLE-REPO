# -*- coding: utf-8 -*-
"""Assemble the kinesiology programme and the fitness career path."""
import io, json

body = io.open('scratchpad/body_fit.html', encoding='utf-8').read()

program = {
  "slug": "kinesiology-and-sport",
  "name": "Kinesiology, Exercise Science and Sport Management",
  "isPublished": True,
  "sortOrder": 600,
  "description": "Human movement, exercise and the business of sport. ⚠⚠⚠ Two quite different degrees share this classification and the BIGGER one is business: Sport and Fitness Administration is 833 Florida credentials a year against Kinesiology and Exercise Science's 711 — and UF and Florida State, the two largest producers, award only the management one.",
  "degreesNote": "⚠⚠⚠ READ THE REQUIRED-COURSE LIST, NOT THE DEPARTMENT NAME. Sport and Fitness Administration (31.0504) produces 833 credentials at 8 Florida public institutions — UF 335, Florida State 268, UNF 57, UWF 24 — and it is a BUSINESS degree: marketing, finance, facility operations, event management, sport law. Kinesiology and Exercise Science (31.0505) produces 711 at six — UCF 360, FAU 188, FGCU 70, UWF 64, USF 23, FIU 5 — and it is the movement science: exercise physiology, biomechanics, anatomy, assessment. ⚠⚠ Neither is a lesser version of the other, and UF and Florida State award no exercise science bachelor's under 31.0505 at all. ⚠ Health and Physical Education General (31.0501) adds 58 at UWF and FAMU — the teacher-preparation end. ⚠⚠⚠ AND THE ROW ALMOST NOBODY TAKES IS THE MOST DIRECTLY VOCATIONAL: Physical Fitness Technician (31.0507) is an ASSOCIATE degree at Northwest Florida State, Chipola, Tallahassee and Pensacola State, and it produces 27 graduates a year for an occupation with 68,000 annual openings nationally whose entry-level education is a high school diploma. ⚠ There is no licence and no programmatic accreditor in this family. What employers check is an NCCA-accredited CERTIFICATION, which the degree does not confer — so a degree here has to be chosen for what it opens afterwards (clinical exercise physiology, graduate school, or management), not for access to the entry-level job.",
  "cips": [
    { "cipCode": "31.05", "note": "Sports, Kinesiology and Physical Education/Fitness — 1,629 credentials at 11 Florida public institutions across four codes. ⚠⚠ Sport and Fitness Administration (31.0504) 833 at eight, led by UF 335 and Florida State 268 — a business degree. Kinesiology and Exercise Science (31.0505) 711 at six, led by UCF 360 and FAU 188 — the movement science. Health and PE General (31.0501) 58. ⚠ Physical Fitness Technician (31.0507), the vocational associate, just 27 at four state colleges." }
  ],
  "related": [
    { "slug": "athletic-training", "note": "⚠⚠ The credentialled neighbour, and a common destination for kinesiology graduates. Athletic training moved to MASTER'S-level entry, is programmatically accredited and is licensed in Florida — so an undergraduate PET or APK course does not accumulate toward it. ⚠ Work backwards from a target programme's prerequisite list rather than assuming your degree covers it." },
    { "slug": "physical-therapy", "note": "⚠⚠⚠ Where a large share of exercise science students are actually heading, whether or not the department frames it that way. ⚠ The prerequisite that decides it is anatomy and physiology BY NUMBER: DPT programmes name the BSC2085C/BSC2086C sequence, and the APK2100C/APK2105C version taught in kinesiology departments is not reliably accepted." },
    { "slug": "dietetics-and-nutrition", "note": "⚠ The pairing clients ask for and degrees rarely deliver. Nutrition advice beyond general guidance is REGULATED in Florida — dietetics is licensed — so a trainer without that credential has a legal limit on what they may say. ⚠⚠ APK4163 Nutrition for Sport and Exercise Science is the shared course." },
    { "slug": "business-administration", "note": "⚠ Named because the management half of this family IS business, and because the earners at the top of the fitness wage table are running facilities or their own practice. ⚠⚠ 45 Florida institutions award business against six awarding exercise science.", "isRoute": False },
    { "slug": "public-health", "note": "⚠ A route out that uses the training: worksite wellness, chronic disease prevention and community physical-activity programmes are public health work, the CHES credential is coursework-based, and the funding is institutional rather than client-by-client.", "isRoute": False }
  ]
}
io.open('programs/kinesiology-and-sport.json', 'w', encoding='utf-8').write(json.dumps(program, ensure_ascii=False, indent=2))

courses = [
 ("BSC2085", "Anatomy and Physiology I — twenty carriers. ⚠⚠⚠ TAKE THIS NUMBER, not the kinesiology-department alternative. Nearly every Florida health-professions programme names the BSC sequence in its prerequisites, and a large share of exercise science students end up applying to one.",
  "⚠⚠⚠ The same subject is taught as APK2100C/APK2105C in kinesiology departments, and this site has recorded that divergence as the most damaging in Florida: the APK version is NOT reliably accepted where BSC is named. ⚠ BSC2085C is the equivalent integrated four-credit packaging at seven institutions."),
 ("BSC2086", "Anatomy and Physiology II — the second half, and the one covering cardiovascular, respiratory and renal systems. ⚠ That is the physiology exercise science is actually built on, and the half a student who stops after the first course is missing.",
  None),
 ("APK3110", "Exercise Physiology I — FIU, USF and UWF. ⚠⚠ The core science of the degree: how the body responds to and adapts to exercise, energy systems, cardiovascular and respiratory response, training adaptation. ⚠ It is what separates an exercise science graduate from a certified trainer, and it is what the clinical roles read.",
  None),
 ("APK4112", "Exercise Physiology II — FGCU, FIU, UCF and UF. The advanced treatment: environmental physiology, ergogenic aids, special populations, chronic disease. ⚠⚠ This is the course that points at the EXERCISE PHYSIOLOGIST role — $59,460 median, +13% growth, the fastest in this family.",
  None),
 ("APK4125", "Exercise Prescription — FIU, UNF and UWF. Designing programmes for real people with real limitations, against published guidelines. ⚠ It is the single most directly employable course in the APK prefix, and the one a cardiac rehabilitation or corporate wellness employer will ask about.",
  None),
 ("PET4550", "Exercise Testing — FAU, UNF and USF. Graded exercise testing, VO2 assessment, body composition, interpretation. ⚠⚠ The hands-on assessment course, and the skill that justifies a clinical wage.",
  "⚠⚠⚠ NOT AUTOMATICALLY TRANSFERABLE — one of 13 PET numbers out of 122 that carry that statewide classification, against roughly 2% in a typical prefix. A receiving programme must attest to your competence itself. ⚠ Take it at the institution you will graduate from."),
 ("PET4551", "Physical Fitness Assessment and Exercise Prescription — the assessment-plus-prescription pairing under the PET prefix. ⚠ Where APK4125 is the science of prescription, this is the applied protocol version, and it is the closer match to what a fitness facility actually does.",
  "⚠⚠ Also NOT AUTOMATICALLY TRANSFERABLE, and PET3551 is a 3000-level twin of the same subject. Check which your programme names and take it late rather than early."),
 ("APK4163", "Nutrition for Sport and Exercise Science — FIU, UCF and UWF. ⚠⚠⚠ Nutrition is the first question every client asks and the one a trainer is most likely to answer unlawfully. Dietetics is LICENSED in Florida, so there is a legal limit on advice beyond general guidance. ⚠ Take this course to learn where the limit is as much as to learn the content.",
  None),
 ("HUN2201", "Fundamentals of Human Nutrition — the lower-division nutrition course, widely carried and usually transferable. ⚠ Named as the accessible alternative where APK4163 is not offered, and because it is a prerequisite for several dietetics and health-professions routes.",
  None),
 ("PET2622", "Care and Prevention of Athletic Injuries — NINE public carriers, the widest course in this family. Recognition, first response, taping, return-to-activity judgement. ⚠ Practical, immediately useful, and the course that makes you employable in a school, club or team setting while still a student.",
  "⚠ PET2622C is the integrated form at Central Florida, Florida State, Tallahassee and Valencia — equivalent packaging, and no institution carries both."),
 ("APK4400", "Sport Psychology — FIU, Florida State and USF. Motivation, adherence, goal setting and behaviour change. ⚠⚠ Adherence is the actual problem in this profession: the technical programme is rarely what fails, and the clients who stay are what a self-employed trainer's income is made of.",
  "⚠ PET2210 Sport Psychology is a lower-division treatment at FSCJ, Lake-Sumter and Tallahassee."),
 ("APK4050", "Research and Evaluation in Kinesiology — FGCU, FIU and UF. Reading the literature, evaluating a claim, designing an assessment. ⚠⚠ The fitness industry runs on unevidenced claims, and the ability to tell a real study from a marketing one is a genuine professional differentiator — and the course a graduate programme looks for.",
  None),
 ("STA2023", "Statistical Methods I — thirty-nine carriers and (GE CORE). ⚠ Assessment is measurement: body composition, VO2, strength testing and progress tracking are all statistics, and so is every claim made about a training programme. ⚠⚠ It is a general-education requirement anyway, so it costs nothing to take it seriously.",
  None),
 ("PSY2012", "General Psychology — widely carried and (GE CORE) at most institutions. ⚠ Named because behaviour change is the job, and because it is a prerequisite for the sport psychology and health behaviour courses as well as for most health-professions graduate programmes.",
  None),
 ("PET4401", "Organization and Administration of Physical Education and Sport — FAMU, FIU, UCF and USF. Budgets, staffing, risk management, facility operations. ⚠⚠ The people earning the 75th and 90th percentile wages in this occupation are mostly managing or self-employed, and this is the only course on the list that addresses that directly.",
  None),
 ("PET4946", "Sports and Fitness Internship — FAU, FIU and USF. ⚠⚠ In a field where the entry-level job needs no degree, demonstrated experience is what a degree-holder has to bring. ⚠ Choose the placement for the setting you want to work in — clinical, collegiate, commercial or corporate — because they hire from each other far less than students expect.",
  None),
]

sources = [
 ("BLS Occupational Outlook Handbook — Exercise Trainers and Group Fitness Instructors", "https://www.bls.gov/ooh/personal-care-and-service/fitness-trainers-and-instructors.htm",
  "$47,160 median, 388,400 jobs, +7% for 2025-35 and about 68,000 annual openings — on an entry-level education of HIGH SCHOOL DIPLOMA. Source of the certification statement, the industry table, and the 55% fitness-centre / 15% self-employed split. No AI claim."),
 ("BLS Occupational Outlook Handbook — Exercise Physiologists", "https://www.bls.gov/ooh/healthcare/exercise-physiologists.htm",
  "$59,460 median, 21,200 jobs, +13% for 2025-35 — the fastest growth in this family — and about 1,400 annual openings, bachelor's entry. Licensure exists in Louisiana only; elsewhere the gate is employer requirement and certification."),
 ("O*NET — Exercise Trainers and Group Fitness Instructors (39-9031.00), Florida wages", "https://www.onetonline.org/link/localwages/39-9031.00?st=FL",
  "Florida median $38,800 against $47,160 national. ⚠ The Florida 25th percentile of $28,970 is below a full-time year at the state minimum wage, which reflects how much of this occupation is part-time rather than an hourly rate that low."),
 ("IPEDS completions — Florida, CIP 31.05", "https://nces.ed.gov/ipeds/",
  "Sport and Fitness Administration 833 at eight institutions; Kinesiology and Exercise Science 711 at six; Health and PE General 58; Physical Fitness Technician 27 associate degrees at four state colleges. Source of the finding that UF and Florida State award only the management degree."),
 ("SCNS statewide course file — PET transferability and PET/APK carrier counts", "https://flscns.fldoe.org/",
  "13 of 122 active undergraduate PET numbers are classified NOT AUTOMATICALLY TRANSFERABLE — about 11% against roughly 2% in a typical prefix — and they cluster on exercise testing, fitness assessment, athletic training clinicals and biomechanics."),
 ("Tools/CLAUDE.md — the BSC/APK anatomy and physiology prefix divergence", "https://floridacourserepo.com/courses/BSC2085",
  "This project's own finding, recorded as the most damaging prefix divergence in Florida: health-professions prerequisites name BSC2085C/BSC2086C, while kinesiology departments teach the same subject as APK2100C/APK2105C, which is not reliably accepted in its place."),
]

path = {
  "slug": "fitness-professional",
  "name": "Fitness Professional and Exercise Physiologist",
  "cipCode": "31.05",
  "socCode": "39-9031",
  "additionalSocCodes": ["29-1128"],
  "isPublished": True,
  "sortOrder": 142,
  "description": "⚠⚠⚠ The entry-level education for this occupation is a HIGH SCHOOL DIPLOMA, and it has about 68,000 openings a year — one of the largest figures on this site. What the job requires is a CERTIFICATION, not a degree. ⚠⚠ So a Florida student in a kinesiology degree needs an answer to a direct question: what is the degree for? There are three good ones — clinical exercise physiology ($59,460, +13%), graduate school in a health profession, or management — and this page is organised around them.",
  "credentialNote": "⚠⚠⚠ NO FLORIDA LICENCE FOR PERSONAL TRAINING AND NO PROGRAMMATIC ACCREDITOR FOR THE DEGREE. What employers and insurers check is a CERTIFICATION, and the recognised mark is that the certifying body itself is NCCA-accredited — ACSM, NASM, ACE and NSCA among them. BLS: \"personal trainers usually must be certified before they begin working with clients.\" ⚠⚠ So a four-year graduate and a certified trainer with no degree compete for the same floor job, and the certification is the part that is checked. ⚠ THE DEGREE PAYS OFF ONE LEVEL UP — clinical exercise physiology, cardiac rehabilitation, collegiate strength and conditioning, corporate wellness design, and graduate school. Those roles do read the transcript. ⚠⚠ Exercise physiology is licensed in only one state (Louisiana), so in Florida the clinical gate is the employer's requirement; ask which certification they want BEFORE choosing an exam. ⚠⚠⚠ AND KNOW THE LEGAL EDGE OF THE JOB: dietetics is LICENSED in Florida, so nutrition advice beyond general guidance is regulated, whatever your certification says.",
  "cipCodes": [
    {"cipCode": "51.09", "note": "⚠⚠ Allied Health Diagnostic and Treatment Professions — named because athletic training lives here and is the credentialled neighbour: master's-level entry, programmatically accredited and LICENSED in Florida. ⚠ An undergraduate PET or APK course does not accumulate toward it, so work backwards from a target programme's prerequisite list."},
    {"cipCode": "51.23", "note": "⚠⚠⚠ Rehabilitation and Therapeutic Professions — where a large share of exercise science students are actually heading. ⚠ The decisive prerequisite is anatomy BY NUMBER: DPT programmes name BSC2085C/BSC2086C, and the APK version taught in kinesiology departments is not reliably accepted in its place."},
    {"cipCode": "51.31", "note": "⚠ Dietetics and Clinical Nutrition — named for a legal reason rather than a thematic one. Nutrition is the first thing a client asks about and dietetics is licensed in Florida, so a trainer has a statutory limit on the advice they may give."}
  ],
  "programs": [
    {"slug": "kinesiology-and-sport", "note": "The programme — and the note there is the one to read first, because the LARGER of the two degrees sharing this classification is sport MANAGEMENT, a business degree, and UF and Florida State award only that one."},
    {"slug": "athletic-training", "note": "⚠⚠ The credentialled version of the sideline role: master's entry, accredited, and licensed in Florida. A genuine destination for kinesiology graduates and one that must be planned for from the first year."},
    {"slug": "physical-therapy", "note": "⚠⚠⚠ The commonest graduate destination out of exercise science. ⚠ Take the BSC anatomy sequence, not the APK one, or the application may fail on a prerequisite technicality."},
    {"slug": "dietetics-and-nutrition", "note": "⚠ Named because it is licensed in Florida and therefore marks the legal boundary of what a fitness professional may advise — and because the two credentials together are a much stronger practice than either alone.", "isRoute": False},
    {"slug": "public-health", "note": "⚠ A salaried route out that uses the training: worksite wellness, chronic-disease prevention and community physical activity, funded institutionally rather than client by client.", "isRoute": False},
    {"slug": "business-administration", "note": "⚠ Named because the top of this occupation's wage table is management and self-employment, and because the larger degree in this family is already a business degree.", "isRoute": False}
  ],
  "courses": [],
  "sources": [{"label": t, "url": u, "note": n} for t, u, n in sources],
  "bodyHtml": body,
}

for i, (cid, reason, vnote) in enumerate(courses, start=1):
    row = {"courseId": cid, "sortOrder": i, "reason": reason}
    if vnote:
        row["variantNote"] = vnote
    path["courses"].append(row)

io.open('career_paths/fitness-professional.json', 'w', encoding='utf-8').write(
    json.dumps(path, ensure_ascii=False, indent=2))

print('prog desc', len(program['description']), 'degreesNote', len(program['degreesNote']))
for c in program['cips']:
    if len(c['note'])>500: print('LONG PROGCIP', c['cipCode'], len(c['note']))
for r in program['related']:
    if len(r['note'])>500: print('LONG PROGREL', r['slug'], len(r['note']))
for k in ("description", "credentialNote"):
    print(k, len(path[k]))
for c in path["courses"]:
    if len(c["reason"]) > 500 or len(c.get("variantNote", "")) > 1000:
        print("LONG", c["courseId"], len(c["reason"]), len(c.get("variantNote", "")))
for s in path["sources"]:
    if len(s["note"]) > 500: print("LONG SRC", s["label"], len(s["note"]))
for c in path["cipCodes"]:
    if len(c["note"]) > 500: print("LONG CIP", c["cipCode"], len(c["note"]))
for p in path["programs"]:
    if len(p["note"]) > 500: print("LONG PROG", p["slug"], len(p["note"]))
print("body", len(body), "courses", len(path["courses"]))
