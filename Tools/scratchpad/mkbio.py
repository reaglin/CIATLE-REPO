# -*- coding: utf-8 -*-
"""Assemble the biology programme and career path."""
import io, json

body = io.open('scratchpad/body_bio.html', encoding='utf-8').read()

program = {
  "slug": "biology",
  "name": "Biology and Biomedical Sciences",
  "isPublished": True,
  "sortOrder": 598,
  "description": "The largest science degree in Florida by a very wide margin — about 5,000 bachelor's a year at 15 public institutions. ⚠⚠⚠ Two degrees live inside it and the difference decides your career: Biology (26.0101) is the research science, Biomedical Sciences (26.0102) is an explicitly pre-health track. At USF two-thirds of the output is the second one, at UCF more than half, and the department name does not tell you which you are applying to.",
  "degreesNote": "⚠⚠⚠ 5,274 CREDENTIALS A YEAR AT 15 INSTITUTIONS, AND 4,997 OF THEM ARE BACHELOR'S — against 183 master's and 66 doctorates, a doctoral share of 1.3%. (Chemistry's, in the same state, is 19%.) ⚠ That does not mean biology needs the doctorate less; it means the bachelor's is being used as a general-purpose science credential by an enormous number of students who are leaving for professional school, teaching or something else. ⚠⚠ THE SPLIT THAT MATTERS: Biology General (26.0101) is 3,787 credentials at 14 institutions — FIU 943, UF 616, FAU 434, USF 407, Florida State 392, UCF 383. Biomedical Sciences (26.0102) is 1,487 at eight — USF 800, UCF 487, UWF 68, FAU 40, FSCJ 28, FIU 26, Florida State 20, UNF 18. ⚠⚠⚠ SO AT USF THE BIOMEDICAL TRACK IS TWICE THE SIZE OF THE BIOLOGY ONE, at UCF it is larger, and at UWF it is a majority. Those are pre-health degrees structured around admissions tests and professional-school prerequisites, not around research. Read the required-course list rather than the department name. ⚠ There is no licence and no programme accreditor in general biology, so nothing external distinguishes one graduate from another — which in a field producing 5,000 a year puts the entire burden of differentiation on specific courses and specific research experience.",
  "cips": [
    { "cipCode": "26.01", "note": "Biology, General — 5,274 credentials at 15 Florida public institutions, 4,997 of them bachelor's. ⚠⚠ Two codes inside it: Biology General (26.0101) 3,787 at 14 institutions, led by FIU 943, UF 616 and FAU 434; and Biomedical Sciences (26.0102) 1,487 at eight, led by USF 800 and UCF 487. ⚠ The second is an explicitly pre-health track, and at Florida's two largest producers it is the bigger of the two." }
  ],
  "related": [
    { "slug": "medicine", "note": "⚠⚠⚠ The real destination of a large share of this degree, and the data says so: 1,487 of Florida's 5,274 biology credentials are BIOMEDICAL SCIENCES, an explicitly pre-health track. ⚠ Florida's six public medical schools admit a few hundred students a year against that; the arithmetic is worth doing before committing." },
    { "slug": "medical-laboratory-science", "note": "⚠⚠⚠ The finding biology graduates meet too late. Florida LICENSES clinical laboratory personnel, so a general biology degree does not open hospital bench work that an MLS graduate walks into — and MLS pays better than the biological technician role most biology graduates actually enter. Look at it before the third year, not after graduation." },
    { "slug": "chemistry", "note": "⚠⚠ The instructive contrast. Chemistry awards 19% of its Florida credentials at doctoral level against biology's 1.3%, on a tenth of the volume. ⚠ The organic sequence (CHM2210, 29 carriers) and biochemistry are shared, and a biology student who takes chemistry seriously is competing against far fewer people.", "isRoute": False },
    { "slug": "environmental-science", "note": "⚠ A genuine destination for the ecology and field half of a biology degree — PCB3043 General Ecology and BSC3052 Conservation Biology are the shared courses, and Florida's water-quality, restoration and invasive-species programmes are permanent work. ⚠⚠ Note the wages: Florida pays environmental science $21,390 below the national median.", "isRoute": False },
    { "slug": "public-health", "note": "⚠ An underadvertised exit that uses the degree rather than discarding it: epidemiology, environmental health and infectious disease all read as biology, the master's is a common next step, and the CHES credential is coursework-based rather than major-based.", "isRoute": False }
  ]
}
io.open('programs/biology.json', 'w', encoding='utf-8').write(json.dumps(program, ensure_ascii=False, indent=2))

courses = [
 ("BSC2010", "General Biology I, majors sequence — TWENTY public carriers including FIU, Florida Polytechnic, Florida State, New College, UCF, UF, USF and UWF. The gate to the whole degree. ⚠⚠⚠ Take the MAJORS sequence, not the non-majors survey: the survey does not satisfy the prerequisite for genetics, cell biology or ecology, and students discover that in their third year.",
  "⚠⚠⚠ BSC1010 is the SAME course at seven other institutions — FAMU and FAU among the universities — and the two share NO carrier at all. Twenty-seven institutions, two numbers, zero overlap, and the laboratories split identically. Integrated four-credit forms exist as BSC1010C (10 carriers) and BSC2010C (5). Register by number."),
 ("BSC1010", "The same first majors biology course under the identifier FAMU, FAU and five state colleges use. ⚠ Listed separately because a student will only ever find one of the two numbers, and because this is the course almost every science and pre-health student in Florida takes.",
  "⚠ Both are lower division, so no baccalaureate credit is at risk — but SCNS equivalency does not cross numbers, so an automated transfer match between BSC1010 and BSC2010 finds nothing."),
 ("BSC2010L", "The General Biology I laboratory — eighteen carriers, matching the BSC2010 lecture. ⚠ Enrol in BOTH halves; they are usually corequisites and the registration is the only thing you have to get right. ⚠⚠ It is also where technique starts, and technique is what a laboratory job actually tests.",
  "⚠ BSC1010L is the twin at the seven BSC1010 institutions. Where an institution carries the integrated BSC1010C or BSC2010C instead, that single four-credit course covers both halves."),
 ("BSC2011", "General Biology II — eighteen carriers. Organismal diversity, evolution and ecology, and the half of the sequence that decides whether the ecological or the molecular side of the field appeals to you.",
  "⚠ BSC1011 is the twin at nine institutions. FIU is the ONLY Florida institution carrying both forms of this course."),
 ("CHM2210", "Organic Chemistry I — twenty-nine public carriers. ⚠⚠⚠ The real filter on every professional-school route out of a biology degree, and the course medical, dental, pharmacy and veterinary admissions weight most heavily. ⚠ Reckon on eight to twelve hours a week and do not take it in the same term as another laboratory course if you can avoid it.",
  None),
 ("PCB3063", "Genetics — sixteen public carriers, the widest upper-division biology course in the state. ⚠⚠ It is the conceptual spine of modern biology and the prerequisite most often named by the courses that follow. ⚠ It is also quantitative in a way that surprises students who chose biology to avoid mathematics.",
  None),
 ("PCB3023", "Cell Biology — seven carriers. Membrane transport, signalling, the cytoskeleton and the cell cycle. ⚠ The course that most directly underlies biomedical research, cancer biology and pharmacology, and the one a laboratory interview will probe.",
  None),
 ("MCB2010", "Microbiology — sixteen carriers. ⚠⚠ The single most employable lower-division course in this family: clinical, environmental, food-safety and pharmaceutical laboratories all run on it, and microbiologists post an $87,990 median against a biological technician's $57,510.",
  "⚠ MCB2010C is the integrated three-or-four-credit form at twelve other institutions, and only St Petersburg carries both. MCB3020 is an upper-division treatment at eight institutions."),
 ("PCB3043", "General Ecology — seven carriers. Populations, communities, energy and nutrient flow. ⚠ The bridge to environmental and conservation work, and the course that Florida's restoration, water-quality and invasive-species employers expect to see.",
  "⚠ PCB4043 Ecological Processes is a 4000-level version at Broward, FAMU, FAU and Indian River — approximately the same subject under a different number."),
 ("PCB4674", "Evolution — eight carriers. ⚠⚠ The framework that makes the rest of biology one subject rather than a list of facts, and the course most often missing from a pre-health track built purely around prerequisites. ⚠ Graduate committees notice its absence.",
  None),
 ("BOT3015", "Plant Biology — six carriers. ⚠ Named because it is the part of biology Florida actually pays for: agriculture is a major state industry, invasive plant management is a permanent programme, and plant science graduates compete against far fewer people than animal-focused ones.",
  None),
 ("ZOO3713C", "Comparative Vertebrate Anatomy — eight carriers, integrated with dissection laboratory. ⚠ A standard requirement for veterinary and several medical routes, and the course that makes gross anatomy manageable later. ⚠⚠ Check whether your professional-school target names it specifically; several do.",
  None),
 ("BSC3312", "Marine Biology — five carriers. ⚠ Named here because it is the subject that brings most students to a Florida biology department, and because it deserves its own page rather than a line in this one. ⚠⚠ Take it, and read the marine biologist path before planning a career on it.",
  None),
 ("BSC2085", "Anatomy and Physiology I — twenty carriers. ⚠⚠ The prerequisite that almost every Florida health-professions programme names BY THIS NUMBER, which matters because the same subject is also taught under the APK prefix and health programmes do not accept the substitute readily. ⚠ If a health profession is anywhere in your plan, take the BSC version.",
  "⚠ BSC2085C is the integrated four-credit form at seven institutions — equivalent packaging, and no institution carries both. The APK2100C/APK2105C sequence is the same subject under a different prefix and is NOT reliably accepted in its place."),
 ("STA2023", "Statistical Methods I — thirty-nine public carriers and General Education Core. ⚠⚠⚠ Modern biology is data analysis, and the graduates who can actually do it are not competing with the other 5,000. ⚠ This is the cheapest single way out of the crowd, and it costs nothing because it is a general-education requirement anyway.",
  None),
 ("BSC4933", "Selected Topics in Biology — the number departments use for a research seminar, a special topic or a directed project. ⚠⚠ Named deliberately: RESEARCH EXPERIENCE is the highest-return decision in this degree, and this is frequently the number it is registered under. ⚠ Ask a faculty member in your second year; do not wait to be invited.",
  "⚠ The transcript line says nothing about what was covered, so keep the project description, the methods and any poster or write-up — that record is what a graduate committee or employer will actually read."),
]

sources = [
 ("BLS Occupational Outlook Handbook — Biochemists and Biophysicists", "https://www.bls.gov/ooh/life-physical-and-social-science/biochemists-and-biophysicists.htm",
  "$127,410 median, 35,200 jobs, +12% for 2025-35, about 2,900 annual openings — and an entry-level education of DOCTORAL or professional degree. BLS: they \"need a Ph.D. to work in independent research-and-development positions.\""),
 ("BLS Occupational Outlook Handbook — Microbiologists", "https://www.bls.gov/ooh/life-physical-and-social-science/microbiologists.htm",
  "$87,990 median, 20,100 jobs, +6% for 2025-35, about 1,500 annual openings. Growth attributed to pharmaceutical and biotechnology development, biofuels and public health. No AI claim."),
 ("BLS Occupational Outlook Handbook — Biological Technicians", "https://www.bls.gov/ooh/life-physical-and-social-science/biological-technicians.htm",
  "$57,510 median, 74,400 jobs, +7% for 2025-35 and about 9,400 annual openings — two-thirds of the openings in this family, at the lowest wage, on a bachelor's entry. The realistic first destination."),
 ("O*NET — Biological Technicians (19-4021.00), Florida wages", "https://www.onetonline.org/link/localwages/19-4021.00?st=FL",
  "Florida median $48,700 against $57,510 national, and a 25th percentile of $38,240 against $48,130 — the wage a Florida biology bachelor's is most likely to meet first."),
 ("IPEDS completions — Florida, CIP 26.01", "https://nces.ed.gov/ipeds/",
  "5,274 credentials at 15 institutions, 4,997 bachelor's, 183 master's, 66 doctorates. Source of the Biology-versus-Biomedical Sciences table, including USF's 407 against 800 and UCF's 383 against 487."),
 ("SCNS statewide course file — BSC, MCB, PCB, ZOO, BOT carrier counts", "https://flscns.fldoe.org/",
  "Source of the gateway measurement: BSC1010 at 7 institutions and BSC2010 at 20 with zero overlap, the identical split on the laboratories and on BSC1011/BSC2011, and MCB2010 against MCB2010C overlapping only at St Petersburg."),
]

path = {
  "slug": "biologist",
  "name": "Biologist and Biological Technician",
  "cipCode": "26.01",
  "socCode": "19-1029",
  "additionalSocCodes": ["19-1021", "19-1022", "19-4021"],
  "isPublished": True,
  "sortOrder": 140,
  "description": "⚠⚠⚠ Begin with the arithmetic. Florida awards about 5,000 biology bachelor's a year; the biological-scientist occupations hire roughly 13,800 people a year NATIONALLY, and two-thirds of those openings are technician roles at a $57,510 median. ⚠⚠ That is not an argument against the degree — it is an argument for knowing what it is FOR. In practice a Florida biology bachelor's is a preparation for professional school, a research doctorate, teaching or a laboratory career that starts at technician level, and the state's own enrolment data already shows it.",
  "credentialNote": "⚠⚠ NO LICENCE AND NO PROGRAMME ACCREDITOR in general biology, which in a field producing 5,000 graduates a year is a problem rather than a freedom: nothing external distinguishes one graduate from another, so the specific courses and the specific research experience carry the whole burden. ⚠⚠⚠ THE RESEARCH CAREER IS PhD-GATED even though Florida's doctoral share is only 1.3%. BLS classifies biochemists and biophysicists at DOCTORAL entry level and says they \"need a Ph.D. to work in independent research-and-development positions\"; microbiologists enter at bachelor's but employers \"prefer to hire candidates who have a master's degree or Ph.D.\" ⚠ So decide early, because a doctoral application needs two years of undergraduate research, a supervisor and letters. ⚠⚠ AND THE CREDENTIALLED ALTERNATIVE IS NEXT DOOR: Florida LICENSES clinical laboratory personnel, so medical laboratory science opens hospital bench work that a general biology degree does not, and pays better than the biological technician role. Look at it before the third year.",
  "cipCodes": [
    {"cipCode": "51.10", "note": "⚠⚠⚠ Clinical/Medical Laboratory Science — named because it is the licensed version of the work most biology graduates end up doing, and they find it too late. Florida licenses clinical laboratory personnel; a general biology degree does not qualify. ⚠ It is a smaller, credentialled market rather than a crowded uncredentialled one."},
    {"cipCode": "26.13", "note": "⚠ Ecology, Evolution, Systematics and Population Biology — the field half of this degree, and the anchor of the marine biologist path on this site. PCB3043, PCB4674 and BSC3052 are shared. ⚠⚠ Read that page before planning a career on marine biology; the Florida arithmetic there is harsher than here."},
    {"cipCode": "51.22", "note": "⚠ Public Health — an exit that uses the degree rather than discarding it. Epidemiology, infectious disease and environmental health all read as biology, the master's is the standard next step, and the job market is far less crowded than the research one."}
  ],
  "programs": [
    {"slug": "biology", "note": "The programme — 15 Florida institutions, and the note there carries the Biology-versus-Biomedical Sciences split that decides what the degree is actually preparing you for."},
    {"slug": "medical-laboratory-science", "note": "⚠⚠ The licensed alternative, and the most actionable link on this page. Florida licenses clinical laboratory personnel; MLS graduates do hospital bench work a biology graduate cannot, and are paid more than biological technicians."},
    {"slug": "medicine", "note": "⚠⚠ Where 1,487 of Florida's 5,274 biology credentials are explicitly pointed — the Biomedical Sciences track. ⚠ Declare it early; the course order for a pre-health route differs from a biologist's."},
    {"slug": "chemistry", "note": "⚠ Named as the instructive contrast and a genuine option: 19% doctoral share against biology's 1.3%, on a tenth of the volume, and the organic and biochemistry sequence is shared.", "isRoute": False},
    {"slug": "environmental-science", "note": "⚠ The ecology and field destination. PCB3043 and BSC3052 are the shared courses and Florida's restoration and water-quality programmes are permanent — but the Florida wages there are $21,390 below national at the median.", "isRoute": False},
    {"slug": "public-health", "note": "⚠ An underadvertised exit that uses the biology rather than discarding it, and one where a master's is the normal and sufficient credential.", "isRoute": False}
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

io.open('career_paths/biologist.json', 'w', encoding='utf-8').write(
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
