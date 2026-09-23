# -*- coding: utf-8 -*-
"""Assemble the marine biology programme and career path."""
import io, json

body = io.open('scratchpad/body_marine.html', encoding='utf-8').read()

program = {
  "slug": "marine-biology",
  "name": "Marine Biology and Ecology",
  "isPublished": True,
  "sortOrder": 599,
  "description": "The ocean sciences — marine biology, biological oceanography, ecology, evolution and population biology. ⚠⚠⚠ The fact to start with: the state with the second-longest coastline in the country awards 98 marine biology bachelor's a year, at THREE public institutions. Almost everyone doing this work in Florida arrived through a general biology or environmental science degree with marine coursework instead.",
  "degreesNote": "⚠⚠⚠ THE NAMED DEGREE BARELY EXISTS. Marine Biology and Biological Oceanography (26.1302) is awarded at three Florida public institutions and produces 98 bachelor's a year — UWF 40, USF 32, FIU 26. ⚠ The wider ecology and evolution family (26.13) adds 41 more credentials, and they are almost all GRADUATE: UF doctorates and master's in ecology (26.1301), USF and UCF in evolutionary biology (26.1307), USF doctorates in ecology other. ⚠⚠ So the undergraduate footprint is tiny and the graduate footprint is where the research careers are, which is consistent with what BLS says: zoologists and wildlife biologists \"typically need a master's degree for higher level jobs\" and \"a Ph.D. to lead research projects.\" ⚠⚠⚠ THE PRACTICAL CONCLUSION IS TO STOP LOOKING FOR THE DEGREE TITLE. A biology degree at an institution with marine faculty, a field station and boat access is a better preparation than a marine-titled degree without them — ask what research is running and who is running it. FAU (Harbor Branch), UF, Florida State, UCF and New College all support marine work without awarding a named marine bachelor's. ⚠ And check the courses rather than the catalogue: 65 of the 72 live undergraduate OCB identifiers are carried by exactly ONE institution, because marine courses are built around the water a particular campus can reach.",
  "cips": [
    { "cipCode": "26.13", "note": "Ecology, Evolution, Systematics and Population Biology — 139 credentials at 6 Florida public institutions. ⚠⚠ Marine Biology and Biological Oceanography (26.1302) is 98 bachelor's at three: UWF 40, USF 32, FIU 26. The rest is graduate — UF ecology (26.1301) 14, USF and UCF evolutionary biology (26.1307) 13, UF conservation biology (26.1309) 8, USF doctorates 6. ⚠ A small undergraduate footprint over a graduate-weighted research family." }
  ],
  "related": [
    { "slug": "biology", "note": "⚠⚠⚠ Where almost everyone actually comes from. Florida awards about 5,000 biology bachelor's a year against 98 marine ones, and a biology degree at a campus with marine faculty and a field station is the commoner and frequently better route. ⚠ It is also far more crowded, which is the trade." },
    { "slug": "environmental-science", "note": "⚠⚠ The paid version of a similar interest, and worth weighing seriously: 745 credentials at 16 Florida institutions against 98 at three, and a Florida median $8,000 higher. ⚠ Water quality, estuaries, seagrass and coastal resilience are the same coastline from the regulatory side." },
    { "slug": "environmental-engineering", "note": "⚠ Named for the coastal work specifically — restoration, shoreline stabilisation, stormwater and water-quality infrastructure are engineering projects that marine scientists advise on. ⚠⚠ Engineers on those projects hold a licence and earn roughly double the Florida marine biology median.", "isRoute": False },
    { "slug": "public-health", "note": "⚠ An unexpected and real Florida destination: harmful algal blooms, shellfish sanitation, beach water quality and vibrio surveillance sit between marine biology and public health, and the public health side is better funded and better paid.", "isRoute": False }
  ]
}
io.open('programs/marine-biology.json', 'w', encoding='utf-8').write(json.dumps(program, ensure_ascii=False, indent=2))

courses = [
 ("BSC2010", "General Biology I, majors sequence — twenty carriers. ⚠ There is no marine shortcut around it: every marine programme and every graduate committee expects the full majors biology sequence, and the non-majors survey does not satisfy the prerequisites that follow.",
  "⚠⚠ BSC1010 is the same course at seven other institutions, including FAMU and FAU, with ZERO carrier overlap. Register by number and keep the syllabus."),
 ("OCE1001", "Introduction to Oceanography — TWENTY-ONE public carriers and (GE CORE), so it satisfies a general-education science area at every Florida public institution. ⚠⚠ Physical oceanography is what makes marine biology make sense: currents, stratification, upwelling and tides decide where organisms are and why.",
  "⚠ OCE2001 is the same course at seven other institutions — FAU, FSCJ, Indian River, New College, Pasco-Hernando, St Petersburg and USF — with no overlap. OCE1001C is an integrated form at three more."),
 ("OCB1000", "Survey of Marine Biology — six carriers: Florida Keys, Florida SouthWestern, Indian River, St Johns River, Seminole State and Valencia. The lower-division introduction, and the cheapest way to find out whether the subject is what you imagine it to be.",
  "⚠⚠⚠ FIVE statewide numbers carry introductory marine biology across TWO prefixes and FOUR levels: OCB1000 (1000), BSC1311 (1000), OCB2000 (2000), BSC3312 (3000) and OCB4633 (4000), 18 institutions in total. The same subject is a freshman survey at some institutions and a senior course at others. Check where yours places it."),
 ("BSC3312", "Marine Biology at upper division — Florida State, Indian River, St Johns River, UCF and USF. ⚠ The majors treatment rather than the survey, and the one that assumes the general biology sequence. ⚠⚠ Indian River and St Johns River carry BOTH this and OCB1000, which is the clean signal that the two really are different courses rather than one course numbered twice.",
  None),
 ("PCB3043", "General Ecology — seven carriers. ⚠⚠ The most important non-marine course on this page. Marine ecology is ecology, and graduate committees and consultancies both read this course as the evidence that you understand populations, communities and energy flow rather than just charismatic animals.",
  "⚠ PCB4043 Ecological Processes covers approximately the same subject at Broward, FAMU, FAU and Indian River."),
 ("PCB4315", "Marine Ecology — FAMU, USF and UWF. Productivity, trophic structure and community dynamics in marine systems. ⚠ Three carriers, which is typical of this field: almost every upper marine course in Florida is taught at one to four institutions.",
  "⚠ UWF's version is a Bahamas field course narrower than the statewide subject — an excellent course, and not the same coverage. Read the syllabus."),
 ("ZOO3205C", "Invertebrate Zoology — FGCU, FIU and USF, integrated with laboratory. ⚠⚠ Most marine animals are invertebrates, and most marine survey and monitoring work is invertebrate identification. ⚠ It is the least glamorous course on this list and the one that appears most often in an actual job description.",
  None),
 ("ZOO4454C", "Ichthyology — FGCU, Florida State and UNF. Fish diversity, anatomy, physiology and identification, with laboratory. ⚠ The core course for fisheries work, and fisheries is where the state jobs are.",
  "⚠⚠⚠ A DOCUMENTED TRAP. The bare ZOO4454 is carried by FIU, USF and UWF with no overlap — but UWF teaches ELASMOBRANCH BIOLOGY on it: sharks, rays and skates only, about 1,200 species against ichthyology's 35,000. A UWF graduate has not covered the teleosts, which are every fish a Florida fisheries biologist handles. Excellent shark course, wrong label. Check the syllabus."),
 ("ZOO4407", "Biology of Sharks and Rays — FAU, FIU, Florida State and UNF. ⚠ Included because it is real, well taught and genuinely a Florida specialism. ⚠⚠ Take it as an addition to ichthyology rather than instead of it: a shark course alone narrows you at exactly the point you need to look broad.",
  None),
 ("ZOO4485", "Marine Mammal Biology — UF, UNF, USF and UWF. Manatees, dolphins and whales. ⚠⚠ Be clear-eyed: marine mammal work is the most oversubscribed corner of an already oversubscribed field, and Florida's manatee programmes are state-funded. ⚠ It is a strong course; it is not a hiring advantage on its own.",
  None),
 ("ZOO4405", "Sea Turtle Biology and Conservation — FAU, FGCU and UF. ⚠ Florida hosts the largest loggerhead nesting aggregation in the western hemisphere, so this is genuine local specialism rather than a novelty. ⚠⚠ Nesting-season survey work is also one of the few reliable entry points into paid field experience here.",
  None),
 ("CHM2210", "Organic Chemistry I — twenty-nine carriers. ⚠ Named because marine biology students routinely try to avoid it and graduate programmes routinely require it. Ocean chemistry, physiology and toxicology all sit on it, and so does the veterinary route if that becomes the plan.",
  None),
 ("STA2023", "Statistical Methods I — thirty-nine carriers and (GE CORE). ⚠⚠⚠ Population assessment, survey design, mark-recapture and stock estimation are statistics. ⚠ This is the single clearest line between a seasonal field technician and a scientist, and consulting — the $84,570 row — hires on it.",
  None),
 ("GIS2040", "Fundamentals of Geographic Information Systems — ten carriers. ⚠⚠ Habitat mapping, seagrass extent, nesting distributions and survey design all end up in a GIS, and very few biology graduates can produce one. ⚠ One course, and it is the cheapest differentiation available in this field.",
  None),
 ("BSC4910", "Directed Independent Research — FAU, Florida State, Indian River, St Johns River, UF and USF. ⚠⚠⚠ THE MOST IMPORTANT ROW ON THIS PAGE. With 1,400 national openings a year, what separates applicants is research experience and a named advisor who will write for you — and a funded master's place turns on exactly those two things. ⚠ Start in year two; do not wait to be asked.",
  "⚠ The transcript line says nothing about what you did, so keep the project description, the methods, the data and any poster or presentation. That record is what a graduate committee actually reads."),
 ("OCE3008", "Oceanography at upper division — Broward, FAU, UCF and UNF. The majors treatment of physical, chemical and geological oceanography. ⚠ Worth taking if your degree is biology rather than marine science, because it is the context the biology sits in and the part a general biology curriculum leaves out.",
  None),
]

sources = [
 ("BLS Occupational Outlook Handbook — Zoologists and Wildlife Biologists", "https://www.bls.gov/ooh/life-physical-and-social-science/zoologists-and-wildlife-biologists.htm",
  "$76,780 median, 19,500 jobs, +4% for 2025-35 and about 1,400 annual openings. Source of the master's and PhD statements, the industry table, and the explicit warning that demand \"may be limited by budgetary constraints\" because the funding is governmental. No AI claim."),
 ("O*NET — Zoologists and Wildlife Biologists (19-1023.00), Florida wages", "https://www.onetonline.org/link/localwages/19-1023.00?st=FL",
  "The wage table on this page. Florida's median of $52,750 is below the national 25th percentile, and the gap runs $9,200 at the 10th to $30,930 at the 75th — wider than any other occupation measured on this site."),
 ("IPEDS completions — Florida, CIP 26.13", "https://nces.ed.gov/ipeds/",
  "Marine Biology and Biological Oceanography: 98 bachelor's at three institutions — UWF 40, USF 32, FIU 26. The wider ecology and evolution family adds 41, almost all graduate, at UF, USF and UCF."),
 ("SCNS statewide course file — OCB, OCE, ZOO and PCB carrier counts", "https://flscns.fldoe.org/",
  "Source of the five-number introductory measurement across 18 institutions, the 90% single-carrier rate on the OCB prefix (65 of 72 live undergraduate ids), and the OCE1001/OCE2001 gateway split with zero overlap."),
 ("Florida Fish and Wildlife Research Institute", "https://myfwc.com/research/",
  "The state's principal marine research employer, in St Petersburg. Named because it runs the monitoring programmes — fisheries, manatee, sea turtle, harmful algal bloom — that most Florida marine careers pass through, and because volunteering there as a student is one of the few reliable ways in."),
 ("Tools/SOURCES.md — the ZOO4454 divergence (batch 165)", "https://floridacourserepo.com/courses/ZOO4454",
  "This project's own finding: the statewide subject is Ichthyology, and UWF teaches Elasmobranch Biology on the number — about 1,200 species against 35,000, with the teleosts absent. Recorded when the course was written and repeated here because it has a direct career consequence."),
]

path = {
  "slug": "marine-biologist",
  "name": "Marine Biologist and Wildlife Biologist",
  "cipCode": "26.13",
  "socCode": "19-1023",
  "isPublished": True,
  "sortOrder": 141,
  "description": "⚠⚠⚠ The numbers first, because nobody puts them in front of Florida students: 19,500 zoologists and wildlife biologists nationally, about 1,400 openings a year across all fifty states, and a FLORIDA median of $52,750 against $76,780 nationally — the widest gap this site has measured. ⚠⚠ Florida awards 98 marine biology bachelor's a year at three institutions, and roughly 5,000 biology bachelor's, many of whom want the same jobs. This page is about what to do with that, not about talking you out of it.",
  "credentialNote": "⚠⚠⚠ BLS LISTS A BACHELOR'S AS ENTRY AND THEN SAYS THE PART THAT MATTERS: zoologists and wildlife biologists \"typically need a master's degree for higher level jobs\" and \"typically need a Ph.D. to lead research projects.\" With 1,400 openings a year the bachelor's-only route runs into SEASONAL TECHNICIAN WORK — real and often enjoyable, but frequently temporary, sometimes unpaid at the start, and paid at the bottom of the wage table. ⚠⚠ Plan for the master's from year one, or plan deliberately for an exit. ⚠ What wins a funded master's place is not grades: it is RESEARCH EXPERIENCE and an advisor who will write for you, and both take two years to build. ⚠⚠ There is no licence. What functions as a credential in the field is practical: scientific diver certification, small-boat handling and a boating safety card, species identification you can demonstrate, and statistics and GIS. ⚠⚠⚠ AND READ THE FUNDING WARNING IN BLS'S OWN WORDS — demand \"may be limited by budgetary constraints, as a substantial portion of the funding… originates from various governmental agencies.\" Your salary is a line in a budget.",
  "cipCodes": [
    {"cipCode": "26.01", "note": "⚠⚠⚠ Biology, General — named because this is where almost everyone in this career actually comes from. Florida awards about 5,000 biology bachelor's a year against 98 marine ones, and a biology degree at a campus with marine faculty, a field station and boat access beats a marine-titled degree without them."},
    {"cipCode": "03.01", "note": "⚠⚠ Natural Resources and Conservation — the better-paid neighbour on the same coastline. Environmental science is 745 Florida credentials at 16 institutions against 98 at three, and its Florida median is about $8,000 higher. Estuaries, seagrass and water quality are the same water from the regulatory side."},
    {"cipCode": "40.06", "note": "⚠ Geological and Earth Sciences — named for the oceanography half. Physical, chemical and geological oceanography decide where organisms are, and OCE1001 at 21 Florida institutions is the shared course. ⚠⚠ Marine GEOLOGY and coastal processes are also a less crowded corner of the same coastline."}
  ],
  "programs": [
    {"slug": "marine-biology", "note": "The programme — three Florida public institutions award the named bachelor's, and the note there explains why choosing the department rather than the degree title is the better move."},
    {"slug": "biology", "note": "⚠⚠ The realistic route for most people: 5,000 Florida bachelor's a year, marine coursework available at many more campuses than the three awarding a marine degree, and the same graduate programmes open at the end of it."},
    {"slug": "environmental-science", "note": "⚠⚠ Weigh this one seriously before committing. Same coastline, sixteen institutions instead of three, a Florida median about $8,000 higher, and permanent state-funded work in water quality and restoration."},
    {"slug": "public-health", "note": "⚠ An unexpected Florida destination — harmful algal blooms, shellfish sanitation and beach water quality sit between the two fields, and the public health side is better funded.", "isRoute": False},
    {"slug": "environmental-engineering", "note": "⚠ Named because coastal restoration and shoreline work are engineering projects marine scientists advise on, at roughly double this occupation's Florida median.", "isRoute": False}
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

io.open('career_paths/marine-biologist.json', 'w', encoding='utf-8').write(
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
