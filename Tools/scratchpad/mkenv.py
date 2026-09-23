# -*- coding: utf-8 -*-
"""Assemble career_paths/environmental-scientist.json."""
import io, json

body = io.open('scratchpad/body_envsci.html', encoding='utf-8').read()

courses = [
 ("EVR1001", "Introduction to Environmental Science — TWENTY-TWO public carriers, 17 of them state colleges. The entry point to the whole field, and it carries (GE CORE) in its statewide title, so it satisfies a general-education science area at every Florida public institution and carries that status in transfer.",
  "⚠⚠⚠ FOUR identifiers for this course across 37 institutions: EVR1001 (lecture, 22), EVR1001L (its lab, 6 — all of which also carry the lecture), EVR1001C (integrated, 8) and EVR2001 (the same course at 2000 LEVEL, 8, including UF, USF and UWF). ⚠ EVR1001 and EVR2001 share NO carrier. Register by number."),
 ("EVR2001", "The same introductory course at 2000 level — Daytona State, Florida Polytechnic, New College, Pensacola State, South Florida State, UF, USF and UWF. ⚠ Listed separately because it is the number the three largest universities on this list use, and a student will only ever find one of the two.",
  "⚠⚠ Both are lower division, so no baccalaureate credit is at risk — but SCNS equivalency does not cross numbers, so an automated transfer match between EVR1001 and EVR2001 finds nothing. Also (GE CORE)."),
 ("EVR1001L", "The laboratory half, at Central Florida, FAMU, Florida Gateway, FIU, Florida State and North Florida College. ⚠ All six also carry the lecture, so this is the clean split-family pair: lecture plus lab completes exactly as the integrated EVR1001C does. ⚠⚠ Where your institution splits it, enrol in BOTH halves — that is the only thing you have to get right.",
  None),
 ("CHM2045", "General Chemistry I — the course that decides which half of this field is open to you. ⚠⚠ Laboratory, consulting and monitoring work screens on chemistry, and an environmental STUDIES programme may not require it. ⚠ Take it anyway if you want to work in a laboratory or for a consultancy; it is very hard to add later.",
  None),
 ("BSC2010", "General Biology I — the majors sequence, not the non-majors survey. ⚠ It is the prerequisite the ecology courses assume, and taking the non-majors version instead is the commonest way Florida students find themselves blocked out of PCB3043 two years later.",
  "⚠ Check which biology your programme requires BEFORE registering: Florida runs majors and non-majors sequences under different numbers, and they are not substitutes."),
 ("STA2023", "Statistical Methods I — THIRTY-NINE public carriers, the widest course in the Florida catalogue outside health-care CTE, and (GE CORE). ⚠⚠ Environmental conclusions are statistical conclusions, and the ones that get challenged in a permit hearing or a lawsuit are challenged on the statistics. Take it seriously rather than as a requirement to clear.",
  None),
 ("EVR1001C", "The integrated lecture-and-laboratory form, at FGCU, Florida SouthWestern, Hillsborough, Northwest Florida, Pensacola State, St Johns River, St Petersburg and Santa Fe. Three or four credits depending on the institution.",
  "⚠ Only Santa Fe carries both this and the bare EVR1001, and there the credits differ — the signature of one institution running the course in two shapes. Everywhere else the two forms are alternatives."),
 ("OCE1001", "Introduction to Oceanography — TWENTY-ONE public carriers and (GE CORE). ⚠⚠ In Florida this is not an elective curiosity: coastal water quality, red tide and harmful algal blooms, estuaries, sea-level rise and beach management are a large share of the state's environmental employment, and almost all of it is coastal.",
  None),
 ("GLY2010", "Physical Geology — nine carriers, (GE CORE). Aquifers, karst, sinkholes and groundwater movement. ⚠⚠ Florida drinks from a limestone aquifer and its springs, sinkholes and saltwater intrusion are geological problems, so this is closer to core than it looks.",
  "⚠⚠ Geology is fragmented SIX ways — GLY1010, GLY1010C, GLY1010L, GLY2010, GLY2010C and GLY2010L are all live at four to nine institutions each. Register by number, not by title."),
 ("PCB3043", "General Ecology — FIU, Florida State, Miami Dade, St Johns River, St Petersburg, USF and UWF. ⚠ The course where environmental science and biology are genuinely the same subject: populations, communities, energy and nutrient flow. ⚠⚠ It is also the course a habitat, wetland or restoration employer expects to see.",
  "⚠ PCB4043 Ecological Processes is a 4000-level version at Broward, FAMU, FAU and Indian River — a different number for approximately the same subject."),
 ("PCB3043L", "The ecology laboratory — FIU, Florida State, St Johns River, St Petersburg, USF and UWF. ⚠⚠ This is where sampling design, quadrats, transects, identification and data recording are actually learned, and those are the skills a field job tests in the first week.",
  None),
 ("BSC3052", "Conservation Biology — FAU, Florida State, St Petersburg, UCF and UNF. Habitat loss, fragmentation, invasive species and restoration. ⚠ In Florida this is applied rather than theoretical: invasive species management and Everglades restoration are ongoing, funded programmes with permanent staff.",
  None),
 ("GIS2040", "Fundamentals of Geographic Information Systems — ten public carriers. ⚠⚠⚠ THE MOST DIRECTLY HIREABLE COURSE ON THIS PAGE. Nearly every environmental job produces a map, most graduates cannot make one, and GIS appears in more environmental adverts than any other single named skill. ⚠ One course, and it changes the screening outcome.",
  "⚠ GIS1040 is the same subject at FAMU, Florida SouthWestern, Miami Dade and Santa Fe."),
 ("SWS1102", "Soils and Fertilizers — Florida Gateway, Hillsborough, Indian River and Palm Beach State. ⚠ Named because Florida's dominant water-quality problem is nutrient loading, and nutrient loading is a soils-and-fertiliser problem before it is a water problem. Springs, estuaries and lake restoration all come back to it.",
  None),
 ("EVR2861", "Introduction to Environmental Policy — Daytona State, FGCU and USF. ⚠⚠ The course that makes a science graduate legible to an agency. Almost all environmental work is done because a rule requires it, and a scientist who cannot name the rule is at a disadvantage against one who can.",
  None),
 ("EVR2647", "Environmental Site Assessment — Daytona State and Miami Dade. ⚠⚠⚠ Short, specific and directly hireable: Phase I environmental site assessments are a standing revenue line in Florida consulting, done on almost every commercial property transaction. ⚠ Two carriers only, so if it is not at your institution, look for it as a certificate or a continuing-education course.",
  None),
 ("EVR2630", "Hazardous Materials Risk Analysis — Daytona State, FSCJ and Miami Dade. ⚠ Contaminated sites, remediation and the regulatory framework around them. Together with site assessment this is the compliance half of the field, and it is where the consulting jobs are.",
  None),
 ("EVR4940", "Environmental Internship — FGCU, UCF, UNF and USF. ⚠⚠ Do it with an agency, a water management district or a consultancy rather than as a laboratory rotation, so you finish with regulatory vocabulary as well as technique. ⚠ It is also the cheapest way to find out whether you want field work, which is hot, wet and full of insects for much of the Florida year.",
  None),
]

sources = [
 ("BLS Occupational Outlook Handbook — Environmental Scientists and Specialists", "https://www.bls.gov/ooh/life-physical-and-social-science/environmental-scientists-and-specialists.htm",
  "$82,220 median, 93,400 jobs, +6% for 2025-35, about 7,300 annual openings, bachelor's entry. Source of the industry table quoted on this page — federal government $116,110 against consulting's $79,320 — and of the note that some employers prefer certification."),
 ("BLS Occupational Outlook Handbook — Environmental Science and Protection Technicians", "https://www.bls.gov/ooh/life-physical-and-social-science/environmental-science-and-protection-technicians.htm",
  "$55,090 median, 36,400 jobs, +7% for 2025-35 (2,500 new jobs), about 5,300 annual openings, associate entry. The two-year route into the same work."),
 ("O*NET — Environmental Scientists and Specialists (19-2041.00), Florida wages", "https://www.onetonline.org/link/localwages/19-2041.00?st=FL",
  "The wage table on this page. Florida is below the national figure at every percentile, by $9,920 at the 10th, $21,390 at the median and $30,720 at the 90th — the largest gap this site has measured so far."),
 ("IPEDS completions — Florida, CIP 03", "https://nces.ed.gov/ipeds/",
  "Environmental Science (03.0104) 456 credentials at 14 institutions; Environmental Studies (03.0103) 225 at five; plus the adjacent codes this site cannot yet browse — Forestry 130, Wildlife and Wildlands 113, Natural Resources Management 69, Fishery Sciences 40, almost all at UF."),
 ("SCNS statewide course file — EVR, GLY, OCE, PCB, SWS carrier counts", "https://flscns.fldoe.org/",
  "Source of the four-identifier measurement for introductory environmental science across 37 institutions, the six-way geology split, and the (GE CORE) markers in the statewide titles."),
 ("Florida Statutes s. 1007.25 — general education core course options", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=1000-1099/1007/Sections/1007.25.html",
  "The provision behind the (GE CORE) marker: a core course satisfies its general-education subject area at every Florida public college and university and carries that status in transfer."),
 ("Florida Statutes ch. 492 — Professional Geology", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0400-0499/0492/0492ContentsIndex.html",
  "Florida licenses professional geologists. Named because groundwater and contaminated-site work frequently requires a licensed geologist's sign-off, and it is one of the few checkable credentials available in this otherwise unregulated field."),
]

path = {
  "slug": "environmental-scientist",
  "name": "Environmental Scientist and Specialist",
  "cipCode": "03.01",
  "socCode": "19-2041",
  "additionalSocCodes": ["19-4042"],
  "isPublished": True,
  "sortOrder": 138,
  "description": "Measuring and protecting water, air, soil and habitat, and making the case in front of a regulator. ⚠⚠⚠ Two things a Florida student should know before choosing the major. FIRST, environmental SCIENCE and environmental STUDIES are different degrees leading to different jobs, and the state's largest producer teaches the studies one. SECOND, Florida pays this occupation $21,390 below the national median — the largest gap this site has measured — so choosing the employer matters more here than almost anywhere else.",
  "credentialNote": "⚠⚠ THERE IS NO LICENCE AND NO PROGRAMME ACCREDITOR, which is not the good news it sounds like. Nothing external validates your preparation, so employers screen on coursework and demonstrated method, and the burden of assembling both falls on you. BLS puts it mildly: \"Some employers prefer or require that candidates… have certification related to the work they will do.\" ⚠ Entry is a bachelor's for the scientist role and an ASSOCIATE for the technician role (19-4042, $55,090, +7%), which is a real two-year route into the same field rather than a lesser one. ⚠⚠ TWO FLORIDA CREDENTIALS DO EXIST AND ARE WORTH KNOWING: geological work is licensed under chapter 492, F.S. (Professional Geologist), which matters for groundwater and contaminated sites; and drinking-water and wastewater treatment plant operators are licensed by the Department of Environmental Protection. ⚠⚠⚠ Where nothing is regulated, the specific courses do the work a credential would — GIS, statistics, chemistry, documented field method and the regulatory vocabulary. Those five are the whole argument of the course list below.",
  "cipCodes": [
    {"cipCode": "26.01", "note": "⚠ Biology, General — named because the ecology sequence is genuinely shared: PCB3043 General Ecology and its laboratory and BSC3052 Conservation Biology are biology numbers, and habitat, wetland and restoration employers hire from both degrees. ⚠⚠ A biology degree with the environmental electives is a stronger preparation for field ecology than an environmental studies degree with none."},
    {"cipCode": "14.14", "note": "⚠⚠ Environmental Engineering — named as the adjacent destination with the licence. An environmental engineer can sit the FE, become a PE and seal designs; an environmental scientist cannot, whatever their experience. Seven Florida institutions award it against this family's sixteen, the mathematics load is far heavier, and the wage ceiling is much higher."},
    {"cipCode": "40.06", "note": "⚠ Geological and Earth Sciences — named because Florida's water problems are geological ones: a limestone aquifer, springs, sinkholes and saltwater intrusion. ⚠⚠ It is also the route to the one directly relevant Florida licence, the Professional Geologist under chapter 492, F.S."}
  ],
  "programs": [
    {"slug": "environmental-science", "note": "The programme — 19 Florida institutions, and the note there sets out the science-versus-studies split and the four adjacent codes (forestry, wildlife, fisheries, resource management) that the tree does not yet carry."},
    {"slug": "environmental-engineering", "note": "⚠⚠ Not the same path and worth deciding between deliberately: engineering carries the calculus sequence, the FE exam and PE licensure, and a ceiling this occupation does not reach. ⚠ If the mathematics is manageable, it is the better-paid version of a similar interest.", "isRoute": False},
    {"slug": "public-health", "note": "⚠⚠ A genuine route and an underadvertised one. The SOC title is literally 'Environmental Scientists and Specialists, INCLUDING HEALTH', and environmental health — water and air quality, vector control, hazardous materials — is a named public health specialism that Florida county health departments staff."},
    {"slug": "civil-engineering", "note": "⚠ Named for the Florida-specific reason: stormwater, coastal resilience and water resources are civil engineering projects that environmental scientists are staffed onto constantly, and the five water management districts employ both.", "isRoute": False},
    {"slug": "data-science", "note": "⚠ Named for the skill that most changes employability here: monitoring produces large spatial and time-series datasets, GIS2040 and STA2023 are the shared courses, and environmental data work is paid closer to the computing market than the environmental one.", "isRoute": False}
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

io.open('career_paths/environmental-scientist.json', 'w', encoding='utf-8').write(
    json.dumps(path, ensure_ascii=False, indent=2))

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
