# -*- coding: utf-8 -*-
"""Assemble the chemistry programme and career path."""
import io, json

body = io.open('scratchpad/body_chem.html', encoding='utf-8').read()

program = {
  "slug": "chemistry",
  "name": "Chemistry and Biochemistry",
  "isPublished": True,
  "sortOrder": 597,
  "description": "The central science — analysis, synthesis, materials and the measurement everything else relies on. ⚠⚠⚠ The shape of Florida's output is the thing to notice: 670 credentials a year and 126 of them are DOCTORATES, 19% of the total. Chemistry is a field where nearly a third of working chemists report a doctorate as required, and the decision to pursue one has to be made in the second undergraduate year, not the fourth.",
  "degreesNote": "⚠⚠ TEN FLORIDA PUBLIC INSTITUTIONS, 670 CREDENTIALS, AND AN UNUSUAL LEVEL MIX: 467 bachelor's, 77 master's and 126 doctorates. UF 162 bachelor's and 46 doctorates; FIU 85/21/21; USF 63 bachelor's and 11 doctorates; UCF 55/8/14; FAU 38; UNF 18; UWF 15; FAMU 12. ⚠⚠⚠ AND READ THE FLORIDA STATE ROW BEFORE APPLYING: 15 bachelor's against 29 master's and 31 doctorates — four graduate degrees for every bachelor's, the profile of a research department rather than a teaching one. That is an advantage if you want undergraduate research and a doctoral route, and a question to ask if you want a large undergraduate cohort. ⚠ THERE IS NO LICENCE AND NO CONVENTIONAL ACCREDITOR. What exists is the American Chemical Society approval programme, and the distinction bites: the ACS approves the DEPARTMENT, while the individual STUDENT earns an ACS-CERTIFIED degree by completing foundation coursework in all five sub-disciplines (analytical, biochemistry, inorganic, organic, physical), four in-depth courses, mathematics and physics, and at least 400 hours of laboratory beyond general chemistry. ⚠⚠ A student can graduate from an approved department WITHOUT the certified degree. Ask in the first year what your track delivers. ⚠ Biochemistry sits alongside as its own course family (BCH) and is the commonest bridge from chemistry into the health professions.",
  "cips": [
    { "cipCode": "40.05", "note": "Chemistry — 10 Florida public institutions and 670 credentials: 467 bachelor's, 126 doctorates and 77 master's. UF 216 across all levels, FIU 127, USF 74, UCF 77, Florida Atlantic 38, Florida State 75, UNF 18, UWF 15, FAMU 12. ⚠⚠ The 19% doctoral share is the highest of any programme family on this site and is the single most informative fact about the field." }
  ],
  "related": [
    { "slug": "chemical-engineering", "note": "⚠⚠ The comparison students most often get wrong. A chemist studies what substances are and do; a chemical engineer designs the plant that makes them at scale. ⚠ Engineering carries the FE exam and PE licensure, a far heavier mathematics load, and a higher bachelor's-level ceiling — chemistry's ceiling is reached mainly through the doctorate instead.", "isRoute": False },
    { "slug": "medicine", "note": "⚠⚠ A route a large share of chemistry majors are actually taking, whether or not the department says so. The organic sequence and biochemistry are medical, dental and pharmacy prerequisites, and CHM2210 is carried by 29 Florida public institutions largely because of it. ⚠ If this is your plan, say so early — the course order differs from a chemist's." },
    { "slug": "environmental-science", "note": "⚠ The largest employer of bachelor's-level chemistry in Florida, and it is not obvious from either department. Environmental and clinical laboratories run on analytical chemistry — CHM3120 and CHM4130 are the courses that get someone hired — and Florida's water-quality programmes are permanent work." },
    { "slug": "medical-laboratory-science", "note": "⚠⚠ Named because it is the licensed, credentialled version of laboratory work, and chemistry graduates frequently discover it late. Florida licenses clinical laboratory personnel; an unlicensed chemistry graduate cannot do the same bench work in a hospital that an MLS graduate can.", "isRoute": False },
    { "slug": "materials-engineering", "note": "⚠ Named for the materials scientist row: $117,790 median, the highest in this family, on only 8,600 jobs nationally. ⚠⚠ In Florida the materials programmes are small — four institutions, two at bachelor's — so the realistic route is chemistry or mechanical first and specialisation later.", "isRoute": False }
  ]
}
io.open('programs/chemistry.json', 'w', encoding='utf-8').write(json.dumps(program, ensure_ascii=False, indent=2))

courses = [
 ("CHM2045", "General Chemistry I — the gateway to everything. Sixteen public carriers including UF, USF, UNF, UWF, FAU, Florida Polytechnic and New College. ⚠⚠⚠ Register by NUMBER: Florida carries this course under two identifiers that share no institution at all.",
  "⚠⚠⚠ CHM1045 is the SAME course at 15 other institutions — FAMU, FGCU, FIU and Florida State among the universities, plus 11 state colleges. THIRTY-ONE carriers, ZERO overlap, and the split does NOT follow the sector line. Both are lower division so no baccalaureate credit is at risk, but SCNS equivalency does not cross numbers and an automated transfer match finds nothing."),
 ("CHM1045", "The same General Chemistry I under the identifier FAMU, FGCU, FIU, Florida State and eleven state colleges use. ⚠ Listed separately because a student will only ever find one of the two, and because this is the most consequential numbering split in the Florida catalogue — it gates chemistry, biology, pre-medicine, pre-pharmacy, nursing, engineering and environmental science simultaneously.",
  "⚠ Its laboratory is CHM1045L, and the second semester is CHM1046. The whole family splits the same way; only Santa Fe carries both forms of anything."),
 ("CHM2045L", "The General Chemistry I laboratory — sixteen carriers, matching the CHM2045 lecture exactly. ⚠ Enrol in BOTH halves: they are usually corequisites and the registration is the one thing a student has to get right.",
  "⚠ CHM1045L is the twin at the fifteen CHM1045 institutions. Credits run 1 at most carriers and 2 at a few."),
 ("CHM2046", "General Chemistry II — seventeen carriers. Equilibrium, thermodynamics, kinetics and electrochemistry, and the course that decides whether organic chemistry will be survivable.",
  "⚠ CHM1046 is the twin at fifteen institutions. Santa Fe is the ONLY institution in Florida carrying both forms of this course."),
 ("CHM2210", "Organic Chemistry I — TWENTY-NINE public carriers, the most widely carried upper-level chemistry course in Florida and, unlike general chemistry, settled on ONE number. ⚠⚠ It is the gate to the whole discipline and to medicine, dentistry and pharmacy, and it is where chemistry majors are made and unmade. Reckon on eight to twelve hours a week.",
  "⚠ An integrated CHM2210C combining lecture and laboratory runs at seven more institutions — Daytona State, FSCJ, Lake-Sumter, Northwest Florida, Polk State, Seminole State and Valencia — at 4 or 5 credits. Equivalent packaging, not a different course."),
 ("CHM2210L", "Organic Chemistry I Laboratory — twenty-six carriers. ⚠⚠ Where technique is actually learned: separation, purification, recrystallisation, spectroscopy. ⚠ It also counts toward the 400 hours of laboratory beyond general chemistry that an ACS-certified degree requires, so keep a record from the start.",
  None),
 ("CHM2211", "Organic Chemistry II — twenty-nine carriers, matching the first semester exactly. Synthesis, mechanism and spectroscopic identification. ⚠ This is the semester whose content medical and pharmacy admissions tests draw on most heavily.",
  None),
 ("CHM3120", "Analytical Chemistry — eleven carriers: Daytona State, FAMU, FAU, FGCU, FIU, Florida Polytechnic, Florida State, UCF, UF, UNF and UWF. ⚠⚠⚠ THE MOST EMPLOYABLE COURSE ON THIS PAGE for a bachelor's-level career. Quantitative method, calibration, error and quality control are what an environmental, clinical or manufacturing laboratory actually hires on.",
  None),
 ("CHM3120L", "The analytical chemistry laboratory — ten carriers. ⚠ Documented quantitative technique with real error analysis. ⚠⚠ In a job interview this is the work you will be asked to describe, because it is the only undergraduate experience that resembles a production laboratory.",
  None),
 ("CHM4130", "Instrumental Analysis — FAMU, FGCU, FIU, Florida State, UCF, UF, UNF and UWF. Chromatography, mass spectrometry and the spectroscopies. ⚠⚠ Named instruments on a CV are what gets a laboratory interview; 'chemistry degree' is not. Learn which instruments your department actually lets undergraduates run.",
  "⚠ CHM4130L, the paired laboratory, runs at the same eight institutions. Take both."),
 ("CHM3610", "Inorganic Chemistry — FAMU, FGCU, FIU, Miami Dade, UF, UNF and USF. One of the five foundation areas an ACS-certified degree requires, and the one most easily left out of a track built around pre-medical requirements.",
  "⚠ CHM4610 is an upper version of the same subject at other institutions. Check which your degree audit names."),
 ("CHM4410", "Physical Chemistry I — thermodynamics, quantum mechanics and kinetics from first principles. ⚠⚠ The hardest course in the major and the one that most reliably predicts whether a doctoral programme will admit you. ⚠ It assumes calculus and calculus-based physics, so sequence those first.",
  None),
 ("BCH4033", "Biochemistry I — FAMU, FGCU, UNF and USF. The fifth ACS foundation area, and the bridge from chemistry into the health professions and the pharmaceutical industry. ⚠ Also the single most useful chemistry course for anyone whose real destination is medicine or pharmacy.",
  "⚠ BCH3033 General Biochemistry (Broward, FAU, FIU, UWF) and BCH4024 Molecular Biology and Biochemistry (six carriers) are parallel numbers for approximately this subject."),
 ("MAC2311", "Calculus I — required for physical chemistry and for the ACS-certified degree's mathematics component. ⚠ Chemistry needs real calculus, unlike architecture or the life-science majors, and the students who defer it are the ones who meet physical chemistry unprepared in their third year.",
  None),
 ("PHY2048", "General Physics with Calculus I — the calculus-based sequence, not the algebra-based one. ⚠⚠ The ACS-certified degree requires two semesters of physics, and physical chemistry assumes the calculus-based treatment. Taking PHY2053 instead is a common and expensive substitution.",
  "⚠ PHY2053 College Physics I is the ALGEBRA-based course. It satisfies pre-health requirements but is not the right preparation for physical chemistry."),
 ("CHM1025", "Introductory Chemistry — seventeen carriers. The preparatory course for students who are not ready for General Chemistry I. ⚠ Taking it is not a setback; arriving in general chemistry without the algebra and stoichiometry it teaches is. ⚠⚠ It does not count toward a chemistry major, so build it into the plan rather than discovering it in week three.",
  None),
]

sources = [
 ("BLS Occupational Outlook Handbook — Chemists and Materials Scientists", "https://www.bls.gov/ooh/life-physical-and-social-science/chemists-and-materials-scientists.htm",
  "Chemists $91,240 and 84,900 jobs at +6%; materials scientists $117,790 and 8,600 jobs at +8%; 6,500 combined annual openings. Source of the industry tables and of the statement that a master's or PhD may be needed for research positions. No AI claim is made."),
 ("BLS Occupational Outlook Handbook — Chemical Technicians", "https://www.bls.gov/ooh/life-physical-and-social-science/chemical-technicians.htm",
  "$60,390 median, 60,000 jobs, +5% for 2025-35, and about 7,600 annual openings — more than chemists and materials scientists combined, on an associate degree."),
 ("O*NET — Chemists (19-2031.00)", "https://www.onetonline.org/link/summary/19-2031.00",
  "The education distribution this page turns on: 56% bachelor's, 30% DOCTORAL, 10% master's. 86,800 employed in 2024, 6,300 annual openings, Job Zone Four."),
 ("O*NET — Chemists (19-2031.00), Florida wages", "https://www.onetonline.org/link/localwages/19-2031.00?st=FL",
  "Florida below national throughout by roughly $8,000-$9,000, except $16,910 at the 75th percentile. A far smaller gap than environmental science's $21,390 at the median."),
 ("ACS — guidelines for bachelor's degree programs and program approval", "https://www.acs.org/education/policies/acs-approval-program/guidelines.html",
  "The certified-degree requirement quoted here: foundation coursework in analytical, biochemistry, inorganic, organic and physical chemistry, four in-depth courses, two semesters each of mathematics and physics, and at least 400 hours of laboratory beyond general chemistry."),
 ("ACS — approved chemistry programs", "https://www.acs.org/education/policies/acs-approval-program/approved-programs.html",
  "The list to check before enrolling. ⚠ Approval attaches to the DEPARTMENT; the certified degree is earned by the individual student, so confirm both."),
 ("IPEDS completions — Florida, CIP 40.05", "https://nces.ed.gov/ipeds/",
  "670 credentials at 10 Florida public institutions: 467 bachelor's, 126 doctorates, 77 master's. Source of the institution table, including Florida State's 15 bachelor's against 60 graduate degrees."),
 ("SCNS statewide course file — CHM and BCH carrier counts", "https://flscns.fldoe.org/",
  "Source of the General Chemistry measurement — CHM1045 at 15 institutions and CHM2045 at 16 with zero overlap, 31 in total — and of the contrast with CHM2210 Organic Chemistry I, settled on one number at 29 carriers."),
]

path = {
  "slug": "chemist",
  "name": "Chemist and Chemical Technician",
  "cipCode": "40.05",
  "socCode": "19-2031",
  "isPublished": True,
  "sortOrder": 139,
  "description": "⚠⚠⚠ The question this page answers is whether you need a doctorate, and the data is unusually clear: 30% of working chemists report one as required — the highest doctoral share of any occupation on this site — while 56% report a bachelor's. They are two different careers and the choice has to be made in the second undergraduate year. ⚠⚠ Also here: the chemical TECHNICIAN route has 7,600 annual openings on an associate degree, more than chemists and materials scientists combined.",
  "credentialNote": "⚠⚠ NO LICENCE AND NO CONVENTIONAL ACCREDITOR — what chemistry has instead is the American Chemical Society, and the distinction catches people out. ⚠⚠⚠ THE ACS APPROVES THE DEPARTMENT; THE STUDENT EARNS THE CERTIFIED DEGREE, and you can graduate from an approved department without one. A certified degree requires foundation coursework in all five sub-disciplines — analytical, biochemistry, inorganic, organic and physical — plus four in-depth courses, two semesters each of mathematics and physics, and AT LEAST 400 HOURS OF LABORATORY beyond general chemistry. ⚠ That 400-hour figure is the closest thing to a credential in this field and it is checkable, so ask the department in your FIRST year whether your intended track delivers it. ⚠⚠ For the doctoral route the real credential is undergraduate research plus letters, and both take about two years to build — which is why the decision belongs in year two. ⚠ O*NET puts chemists in Job Zone Four: a four-year degree plus several years of experience. The associate-level chemical technician role is the genuine early entry point and is not a lesser version of the work.",
  "cipCodes": [
    {"cipCode": "40.06", "note": "⚠ Geological and Earth Sciences — named because analytical chemistry is the shared skill: Florida's environmental and groundwater laboratories run on the same instruments, and geochemistry is a real destination for a chemistry bachelor's. ⚠⚠ It also leads to the Professional Geologist licence under chapter 492, F.S., one of the few checkable credentials near this field."},
    {"cipCode": "26.02", "note": "⚠⚠ Biochemistry and Molecular Biology — the fifth ACS foundation area and the commonest bridge out of chemistry, into the health professions and the pharmaceutical industry. BCH4033, BCH3033 and BCH4024 carry the subject under three competing numbers across ten Florida institutions."},
    {"cipCode": "14.07", "note": "⚠ Chemical Engineering — named because students confuse the two and the difference is structural: a chemist studies what substances do, an engineer designs the plant that makes them. ⚠⚠ Engineering reaches its ceiling through the PE licence; chemistry reaches its ceiling through the doctorate."}
  ],
  "programs": [
    {"slug": "chemistry", "note": "The programme — 10 Florida institutions, and the note there carries the level mix, the Florida State research-department shape, and what the ACS-certified degree actually requires."},
    {"slug": "chemical-engineering", "note": "⚠ A different decision rather than a harder version of the same one: heavier mathematics, the FE exam and PE licensure, and a higher bachelor's-level ceiling. Four Florida institutions award it.", "isRoute": False},
    {"slug": "environmental-science", "note": "⚠⚠ Where a large share of Florida's bachelor's-level chemistry work actually is — environmental and water-quality laboratories, which run on analytical chemistry. ⚠ Worth knowing that those laboratories pay on the environmental scale, which is $21,390 below national at the median in Florida.", "isRoute": False},
    {"slug": "medicine", "note": "⚠⚠ Named because the organic and biochemistry sequence is a medical, dental and pharmacy prerequisite, and a substantial share of chemistry majors are on that route. ⚠ Declare it early: the course ORDER differs from a chemist's."},
    {"slug": "medical-laboratory-science", "note": "⚠⚠ The licensed version of laboratory work, and chemistry graduates find it late. Florida licenses clinical laboratory personnel, so a chemistry degree alone does not open hospital bench work.", "isRoute": False}
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

io.open('career_paths/chemist.json', 'w', encoding='utf-8').write(
    json.dumps(path, ensure_ascii=False, indent=2))

print('prog degreesNote', len(program['degreesNote']), 'desc', len(program['description']))
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
