# -*- coding: utf-8 -*-
"""Assemble the Doctor of Pharmacy programme and the pharmacist career path (QUEUE row 115)."""
import io, json

body = io.open('scratchpad/body_pharm.html', encoding='utf-8').read()

program = {
  "slug": "pharmacy",
  "name": "Pharmacy (Doctor of Pharmacy)",
  "isPublished": True,
  "sortOrder": 650,
  "description": "The Pharm.D., the professional doctorate that leads to licensure as a pharmacist. Three Florida public universities award it (UF, FAMU and USF), about 412 a year. ⚠⚠ Admission turns on two or more years of prerequisite science, not on a bachelor's degree: UF's minimum is an associate degree.",
  "degreesNote": "⚠⚠ The Pharm.D. (CIP 51.2001) is the only degree that leads to the pharmacist licence exams. In 2023 UF awarded 237, FAMU 100 and USF 75. UF also awarded 25 post-master's certificates under the same code. ⚠⚠ Do not confuse it with the pharmaceutical sciences master's (51.2099), about 300 a year at UF, 26 at USF and 7 at FAMU. Those are research and industry degrees, not a licence route. ⚠ Pharmacy technician is a separate, short programme, covered by Pharmacy Technology. ⚠⚠ Admission: BLS says programmes typically require at least two years of prerequisite undergraduate courses, and UF's minimum is an A.A. or A.S. AACP's 2023-24 figures show that 39% of applications nationally came from bachelor's holders and more than half from people without one. ⚠ The prerequisite numbers compete in Florida: CHM2045 against CHM1045, BSC2010 against BSC1010, MCB3020 against MCB2010. UF accepts the state's common-prerequisite equivalents, but check each target school's list literally.",
  "cips": [
    { "cipCode": "51.2001", "note": "Pharmacy (Pharm.D.) — 412 first professional doctorates in 2023 at Florida's three public colleges of pharmacy: UF 237, FAMU 100, USF 75 (IPEDS). Claimed alone because the rest of 51.20 is pharmaceutical science research degrees, not a licence route." }
  ],
  "related": [
    { "slug": "chemistry", "note": "⚠ The prerequisite core — general and organic chemistry, often biochemistry — is chemistry, so a chemistry major covers most of it inside the degree. It also leads to the pharmaceutical-industry careers that the Pharm.D. does not require.", "isRoute": False },
    { "slug": "biology", "note": "⚠ The other major that absorbs most pre-pharmacy prerequisites: general biology, microbiology, anatomy and physiology. ⚠ AACP publishes no data on entrants' majors, so neither is shown to be better.", "isRoute": False },
    { "slug": "pharmacy-technology", "note": "⚠⚠ A different job, not a first step on the same ladder. The technician programme is short and leads to board registration; it earns no credit toward a Pharm.D., though pharmacy work experience helps an application.", "isRoute": False },
    { "slug": "medicine", "note": "⚠ The other prescriber-side health doctorate. The science prerequisites overlap heavily.", "isRoute": False }
  ]
}
io.open('programs/pharmacy.json', 'w', encoding='utf-8').write(json.dumps(program, ensure_ascii=False, indent=2))

courses = [
 ("CHM2045", "General Chemistry I — 16 carriers, including UF, USF, UNF, UWF and FAU. The first course on UF's pre-pharmacy critical-tracking list, and the start of the chemistry sequence the whole Pharm.D. builds on.",
  "⚠⚠ Fifteen other institutions, including FAMU, Florida State, FIU and FGCU, number the same course CHM1045 (and CHM1046 for part II); the two families barely overlap. UF accepts state common-prerequisite equivalents for transfer students, but read your target school's list literally."),
 ("CHM2046", "General Chemistry II — 17 carriers. Equilibrium, kinetics, acids and bases: the chemistry behind how a drug dissolves, is absorbed and is stored.",
  "⚠ CHM1046 at the CHM1045 institutions."),
 ("BSC2010", "General Biology I — 20 carriers, and on UF's pre-pharmacy list with its lab (BSC2010L).",
  "⚠ BSC1010 at seven institutions, including FAMU and FAU. The subject is the same, but the numbers differ."),
 ("BSC2011", "General Biology II — 18 carriers, with its lab. Organisms and physiology: the ground that pharmacology and anatomy build on.",
  "⚠ BSC1011 at nine institutions."),
 ("CHM2210", "Organic Chemistry I — 29 carriers under one number, the settled course in the sequence. ⚠⚠ Drug structure is organic chemistry. UF names it on its critical-tracking list.", None),
 ("CHM2211", "Organic Chemistry II — 29 carriers, with its lab (CHM2211L on UF's list). Reactions and synthesis, completing the chemistry that medicinal chemistry in the Pharm.D. assumes.", None),
 ("MCB3020", "Microbiology — eight carriers, mostly universities; UF names it. Pathogens and antimicrobials, the scientific ground for anti-infective therapy.",
  "⚠⚠ The state and technical colleges teach microbiology as MCB2010 (16 carriers) or MCB2010C (12). UF's catalogue says equivalent courses under the State of Florida Common Course Prerequisites may be used by transfer students, so confirm which your target programme accepts."),
 ("BSC2085", "Human Anatomy and Physiology I — 20 carriers. BLS names anatomy and physiology among typical Pharm.D. prerequisites.",
  "⚠ BSC2085C is the combined lecture-and-lab form at seven institutions and completes the course the same way. ⚠ The APK-numbered anatomy taught in kinesiology departments is not reliably accepted where BSC is named."),
 ("BSC2086", "Human Anatomy and Physiology II — 19 carriers: the cardiovascular, respiratory and renal systems, where most drug actions and dosing adjustments happen.", None),
 ("PHY2053", "General Physics I — 19 carriers. BLS names physics among typical Pharm.D. prerequisites. The algebra-based sequence is the usual pre-health choice.",
  "⚠ PHY2053C is the combined form at ten institutions."),
 ("STA2023", "Elementary Statistics — 39 carriers, and on UF's critical-tracking list. BLS names statistics among typical prerequisites. Reading a drug trial is statistics.", None),
 ("MAC2311", "Calculus I — 39 carriers. Some Pharm.D. programmes require calculus. ⚠ Check whether yours does, and whether it accepts business calculus (MAC2233) instead.", None),
 ("ECO2023", "Microeconomics — 39 carriers. Some programmes list an economics course among their prerequisites; confirm on your target programme's list. ⚠ Drug pricing, insurance formularies and pharmacy benefit management are daily economics in the profession.", None),
 ("PHA3003", "Pharmaceutical Science I — FAMU and Florida Polytechnic. ⚠ One of the few undergraduate PHA courses: a look at pharmaceutical science before committing to a four-year doctorate. The professional PHA courses are Pharm.D.-level and are taken after admission.", None),
]

sources = [
 ("BLS Occupational Outlook Handbook — Pharmacists", "https://www.bls.gov/ooh/healthcare/pharmacists.htm",
  "$140,910 median (2025), 325,200 jobs, +5% for 2025–35, about 12,500 openings a year; doctoral or professional entry; 37% in pharmacies and drug retailers, 32% in hospitals. Retail demand \"expected to be limited\" as the industry consolidates and prescriptions move online or to mail. No mention of AI."),
 ("O*NET — Pharmacists (29-1051.00)", "https://www.onetonline.org/link/summary/29-1051.00",
  "Job Zone Five; 78% of respondents report a doctoral degree required; faster than average growth for 2024–34."),
 ("O*NET — Florida wages for 29-1051.00", "https://www.onetonline.org/link/localwages/29-1051.00?st=FL",
  "Florida median $135,970 against $140,910 national; Florida 10th percentile $56,000 against $99,290, which the source does not explain."),
 ("AACP — Profile of Pharmacy Students, Fall 2024", "https://www.aacp.org/node/3902",
  "36,833 applications for 2023-24; by applicants' previous college: 39% bachelor's, 31% three or more years with no degree, 8% associate, 12% no college. Pharm.D. degrees awarded fell to 11,386 in 2024 from 12,639; class-of-2024 attrition 19.7%. Florida application counts: UF 633, USF 349, FAMU 190."),
 ("UF Catalog — Pharmacy, preprofessional", "https://catalog.ufl.edu/UGRD/academic-programs/UGPHM/PHA_NOD/",
  "63–66 preprofessional credits; critical tracking includes CHM2045/2046, BSC2010/2011, STA2023, CHM2210/2211 and MCB3020; state common-prerequisite equivalents accepted for transfer students."),
 ("UF College of Pharmacy — Pharm.D. admission requirements", "https://admissions.pharmacy.ufl.edu/steps-to-apply/application-requirements/",
  "Minimum A.A. or A.S., or the preprofessional courses plus 36 hours of state general education; preferred minimum science GPA 2.5; prerequisites complete by the August before entry."),
 ("s. 465.007, Florida Statutes — licensure by examination", "https://www.flsenate.gov/Laws/Statutes/2025/465.007",
  "Degree from an accredited school or college of pharmacy, a board-approved internship of no more than 2,080 hours, age 18 or over, and the board's examination."),
 ("IPEDS completions — Florida, CIP 51.20", "https://nces.ed.gov/ipeds/",
  "Pharm.D. (51.2001): UF 237, FAMU 100, USF 75 in 2023. Pharmaceutical sciences (51.2099): UF 301 master's, USF 26, FAMU 7."),
]

path = {
  "slug": "pharmacist",
  "name": "Pharmacist",
  "cipCode": "51.20",
  "socCode": "29-1051",
  "isPublished": True,
  "sortOrder": 115,
  "description": "⚠⚠ One route: the Doctor of Pharmacy, awarded in Florida's public system by UF, FAMU and USF (about 412 a year). ⚠⚠ Admission turns on two or more years of prerequisite science, not a bachelor's degree: UF's minimum is an associate degree, and more than half of Pharm.D. applications nationally come from people without a bachelor's. Median pay is $140,910 nationally and $135,970 in Florida. BLS expects retail demand to be limited as prescriptions move online and by mail.",
  "credentialNote": "⚠⚠⚠ LICENSED IN FLORIDA (ch. 465, F.S.). Section 465.007 requires a degree from an accredited school or college of pharmacy (ACPE is the accreditor), a board-approved internship of no more than 2,080 hours, an age of 18 or over, and passing the board's examination, which is built on the National Association of Boards of Pharmacy's. BLS: \"must pass two exams to get a license.\" ⚠⚠ Only the Pharm.D. qualifies. A pharmaceutical sciences master's does not, and neither does the pharmacy technician credential, which is a separate registration.",
  "cipCodes": [
    {"cipCode": "40.05", "note": "⚠ Chemistry — general and organic chemistry make up the largest block of pre-pharmacy prerequisites on UF's critical-tracking list (CHM2045/2046, CHM2210/2211). AACP publishes no data on entrants' majors, so this records where the prerequisites sit, not a proven best major."},
    {"cipCode": "26.01", "note": "⚠ Biology — general biology and microbiology are on UF's critical-tracking list (BSC2010/2011, MCB3020), and BLS names anatomy and physiology. The same caution applies: AACP does not report majors."}
  ],
  "programs": [
    {"slug": "pharmacy", "note": "The programme — the Pharm.D. at UF, FAMU and USF. Read its note on the pharmaceutical sciences master's, which is not a licence route."},
    {"slug": "chemistry", "note": "⚠ A major that contains most of the prerequisites. It is a route to applying, not a substitute for the Pharm.D.", "isRoute": False},
    {"slug": "biology", "note": "⚠ The other major that contains most of the prerequisites.", "isRoute": False},
    {"slug": "pharmacy-technology", "note": "⚠⚠ A different job. Technician work is useful experience for an application, but it earns no Pharm.D. credit. See the Medical Assistant and Pharmacy Technician path.", "isRoute": False}
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

io.open('career_paths/pharmacist.json', 'w', encoding='utf-8').write(json.dumps(path, ensure_ascii=False, indent=2))

print('prog desc', len(program['description']), 'degreesNote', len(program['degreesNote']))
for c in program['cips'] + program['related']:
    if len(c['note']) > 500: print('LONG PROG NOTE', len(c['note']))
for k in ("description", "credentialNote"):
    print(k, len(path[k]))
for c in path["courses"]:
    if len(c["reason"]) > 500 or len(c.get("variantNote", "")) > 1000:
        print("LONG", c["courseId"], len(c["reason"]), len(c.get("variantNote", "")))
for s in path["sources"]:
    if len(s["note"]) > 500: print("LONG SRC", s["label"], len(s["note"]))
for c in path["cipCodes"] + path["programs"]:
    if len(c["note"]) > 500: print("LONG NOTE", len(c["note"]))
print("body", len(body), "courses", len(path["courses"]))
