# -*- coding: utf-8 -*-
"""Assemble career_paths/architect.json from the body file and the course table."""
import io, json

body = io.open('scratchpad/body_arch.html', encoding='utf-8').read()

courses = [
 ("ARC1301", "The first design studio, and the gate to everything else. Carried by FAMU, FAU, FIU, Hillsborough, Miami Dade, UF and USF. Studio is where architecture is actually taught: you work at a desk in a shared room, you pin work on a wall, and strangers criticise it out loud. Expect far more hours than the credit value suggests.",
  "⚠⚠⚠ TWO IDENTIFIERS, NO OVERLAP. The state colleges plus UCF and Valencia carry ARC1301C instead — same course, integrated packaging, and not one institution carries both. ⚠ Credits diverge too: 3 at FIU and State College of Florida, 4 at most, 6 at USF. Name both numbers when you transfer."),
 ("ARC1301C", "The same first studio under the identifier the state colleges, UCF and Valencia use. ⚠⚠ If you are on the Valencia–UCF–UF 2+2+2 route this is your number: UCF's own admission page selects students competitively before they may enrol in ARC1301C. ⚠ Listed separately from ARC1301 because no institution carries both and a student will only ever find one of them.",
  "⚠ Carried by Broward, Gulf Coast, Palm Beach State, St Petersburg, State College of Florida, UCF and Valencia. Integrated lecture-and-studio packaging; Florida articulation treats it as equivalent to the bare form."),
 ("ARC1302", "Design 2 — the second studio, where the work moves from abstract composition toward building. Eight carriers, the widest of the sequence. Take it in the term immediately after Design 1: studios are gated and offered once a year in most programmes.",
  "⚠ ARC1302C is the same course at Broward, Gulf Coast, Palm Beach State, UCF and Valencia."),
 ("ARC2303", "Design 3 — the first studio most programmes treat as evidence of whether you can do this. Portfolio pieces from here and Design 4 are what graduate architecture admission reads.",
  "⚠ ARC2303C at Broward, Gulf Coast, Palm Beach State, St Petersburg, UCF and Valencia."),
 ("ARC2304", "Design 4 — the end of the lower-division sequence and the transfer point. ⚠⚠ This is the portfolio review that decides admission to an upper-division or graduate architecture programme, so treat the work as an application, not a course.",
  "⚠ Credit divergence is largest here: 3 at FIU, 4 at FAU and Miami Dade, 5 at FAMU, Hillsborough and UF, 6 at USF. ARC2304C is the same course at six other institutions."),
 ("ARC2201", "Theory of Architecture — nine public carriers, the most widely carried course in the prefix. Why buildings are made the way they are: ideas, movements, and the arguments architects have with each other. It is also the course that teaches you to talk about your own work, which is what a critique demands.",
  None),
 ("ARC1701", "History of Architecture I — antiquity through the pre-modern world. Seven carriers: Broward, Hillsborough, Palm Beach State, St Petersburg, UCF, UF and Valencia.",
  "⚠⚠ The SAME subject is numbered ARC2701 at FAMU, FIU, Miami Dade and USF, with NO overlap — a number split rather than a suffix split. Check which number your institution uses before assuming the course is missing."),
 ("ARC2702", "History of Architecture II — the modern period, which is where a practising architect's working vocabulary comes from. Six carriers: FAMU, FIU, Miami Dade, UCF, USF and Valencia.",
  "⚠ Its twin is ARC1702, carried by Palm Beach State, St Petersburg and UF. Same split as the first history course, running the other way."),
 ("ARC2461", "Materials and Methods of Construction — eight carriers, and the course where design meets what a building is actually made of. ⚠ Architects who cannot describe an assembly cannot produce documents anyone can build from, and documentation is 1,520 of the 3,740 experience hours.",
  "⚠ An upper-division version, ARC3463, runs at FAMU, FAU, UCF and UF. They are not substitutes — check which your programme requires."),
 ("ARC2180C", "Introduction to Digital Architecture — Revit, AutoCAD, Rhino and SketchUp, all named as in-demand technologies for this occupation. ⚠⚠ BIM is the tool BLS says is making the work more efficient, and the same paragraph says that efficiency is being absorbed into a wider role rather than fewer architects. Learn it early and deeply.",
  "⚠ Carried as ARC2180C at Miami Dade, Palm Beach State, UCF and Valencia; as bare ARC2180 at Gulf Coast, UF and USF."),
 ("ARC2501", "Architectural Structures 1 — how a building stands up: loads, reactions, and the behaviour of beams and columns. Carried by FAMU, Hillsborough, Palm Beach State and St Petersburg.",
  "⚠ A parallel number, ARC2580 Structures, runs at Broward, FAU and Miami Dade. Same subject, different identifier."),
 ("ARC3503", "Structures One at the upper-division level — FAU, UCF, UF and USF. ⚠ This is where the algebra-based physics from the lower division is actually used. It is demanding, and it is not calculus-based engineering mechanics.",
  None),
 ("ARC3610", "Environmental Technology 1 — climate, daylight, heat, ventilation and energy. ⚠⚠ In Florida this is not a general-education topic: humidity, hurricane loading, solar gain and the state energy code drive real design decisions, and this is the course that teaches them. FAU, UCF and UF.",
  "⚠ Environmental Technology 2 (ARC4620) continues it at the same three institutions."),
 ("ARC3463", "Materials and Methods of Construction at upper division — FAMU, FAU, UCF and UF. Assemblies, detailing and specification, at the level a construction document needs.",
  None),
 ("ARC4220", "Architectural Theory 2 — FAMU, UCF and UF. The upper-division theory course, and usually where the thesis or capstone argument is formed.",
  None),
 ("MAC1147", "Precalculus Algebra and Trigonometry. ⚠⚠⚠ THIS, NOT CALCULUS, IS WHAT UF ASKS ARCHITECTURE TRANSFER APPLICANTS FOR — either MAC1147, or MAC1140 with MAC1114. Students who avoid architecture because of mathematics are usually thinking of the engineering requirement, which is a different and much heavier one.",
  "⚠ MAC1140 Precalculus Algebra plus MAC1114 Trigonometry is the accepted alternative. Confirm your own institution's list."),
 ("PHY2053", "College Physics I — the ALGEBRA-BASED physics course, and the one UF names for architecture transfer applicants (PHY2004 Applied Physics is the alternative). It is the preparation the structures sequence assumes.",
  "⚠⚠ Do NOT take the calculus-based PHY2048 unless your programme asks for it: it is a different and harder course built for engineering majors, and architecture does not require it."),
]

sources = [
 ("Florida Statutes ch. 481 Part I — Architecture and Interior Design", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0400-0499/0481/0481PARTIContentsIndex.html",
  "The licensure chapter. s. 481.209 requires a degree from an NAAB-accredited programme; s. 481.211 requires an approved internship of diversified architectural experience. Architecture and interior design share one board; landscape architecture is Part II."),
 ("NAAB — accredited architecture programmes in the United States", "https://www.naab.org/accreditation/accredited-programs",
  "The authoritative list. Florida: FAMU (B.Arch, M.Arch), FAU (B.Arch), FIU (M.Arch), UF (M.Arch), USF (M.Arch), University of Miami (B.Arch, M.Arch). UCF does not appear."),
 ("NCARB — Architectural Experience Program requirements", "https://www.ncarb.org/gain-axp-experience/experience-requirements",
  "3,740 hours across six areas: Practice Management 160, Project Management 360, Programming and Analysis 260, Project Planning and Design 1,080, Project Development and Documentation 1,520, Construction and Evaluation 360. NCARB reports candidates take four to five years."),
 ("BLS Occupational Outlook Handbook — Architects", "https://www.bls.gov/ooh/architecture-and-engineering/architects.htm",
  "$99,280 median, 124,600 jobs, +4% for 2025-35, about 6,900 annual openings. Source of the AI and BIM passage quoted on this page."),
 ("BLS Occupational Outlook Handbook — Drafters", "https://www.bls.gov/ooh/architecture-and-engineering/drafters.htm",
  "Drafters overall +1%; architectural and civil drafters $66,150, 104,100 jobs, +5%. Source of the statement that CAD and BIM let engineers and architects do work drafters used to do."),
 ("BLS Occupational Outlook Handbook — Landscape Architects", "https://www.bls.gov/ooh/architecture-and-engineering/landscape-architects.htm",
  "$79,870 median, 23,500 jobs, +4% for 2025-35, about 1,700 annual openings."),
 ("O*NET — Architects (17-1011.00), Florida wages", "https://www.onetonline.org/link/localwages/17-1011.00?st=FL",
  "Florida against national at every percentile. The gap is $2,310 at the 10th and $23,190 at the 90th."),
 ("UCF — Bachelor of Design in Architecture", "https://www.ucf.edu/degree/bachelor-of-design-in-architecture-bdes/",
  "The 2+2+2 with Valencia College and UF, the CityLab Orlando M.Arch endpoint, competitive selection into ARC1301C, and the joint-use University Center location."),
 ("University of Florida — architecture transfer prerequisites", "https://dcp.ufl.edu/architecture/undergraduate/",
  "Names PHY 2053 or PHY 2004, and MAC 1147 or MAC 1140 with MAC 1114. The evidence that architecture asks for precalculus and algebra-based physics."),
 ("FAMU School of Architecture and Engineering Technology — accreditation", "https://saet.famu.edu/about/accreditation.php",
  "Confirms the B.Arch (4+1) and both M.Arch tracks are NAAB-accredited, and carries NAAB's own statement that only three degree types are recognised."),
]

path = {
  "slug": "architect",
  "name": "Architect and Landscape Architect",
  "cipCode": "04.02",
  "socCode": "17-1011",
  "isPublished": True,
  "sortOrder": 134,
  "description": "Architects design buildings and take legal responsibility for them. ⚠⚠⚠ The fact that governs everything else: Florida licenses architects BY STATUTE on a degree from an NAAB-accredited programme, and only five Florida public institutions hold one — FAMU, FAU, FIU, UF and USF. ⚠⚠ UCF is the state's second-largest producer of architecture bachelor's and is NOT on that list, because its degree is the middle third of a deliberate 2+2+2 with Valencia and UF. This page covers three roles in one family and the three different entry levels they take.",
  "credentialNote": "⚠⚠⚠ THE ACCREDITED DEGREE IS THE WHOLE QUESTION. s. 481.209, F.S. requires a graduate of a programme accredited by the National Architectural Accrediting Board, with no experience-only alternative. NAAB accredits only the B.Arch, M.Arch and D.Arch — NOT the ordinary four-year B.A. or B.S. in architecture, which is a pre-professional degree. ⚠⚠ In Florida: FAMU holds B.Arch and M.Arch, FAU holds B.Arch, and FIU, UF and USF hold M.Arch only — so at three of the five the licence route runs through a master's. ⚠ Then s. 481.211 requires an approved internship of diversified experience: NCARB's 3,740-hour AXP, which candidates typically take four to five years to complete because the hours must fall in the right categories. Then the six-division Architect Registration Examination. ⚠⚠⚠ Reckon on five to eight years from starting the degree to holding the licence, and verify any programme at naab.org BEFORE enrolling.",
  "cipCodes": [
    {"cipCode": "04.09", "note": "⚠⚠⚠ Architectural Sciences and Technology — claimed because FAU's accredited B.Arch (61 bachelor's) and FIU's accredited M.Arch (152 master's) are FILED HERE, not under 04.02. A path anchored on the obvious code alone would miss two of Florida's five public architecture schools. ⚠ It also holds Architectural Technology (04.0901), the associate-level drafting route at 8 state colleges."},
    {"cipCode": "04.06", "note": "⚠ Landscape Architecture — a separately licensed profession under chapter 481 PART II, covered as a section of this page. Two Florida public institutions award it: UF (14 bachelor's, 3 master's) and FIU (19 master's). Median $79,870, 23,500 jobs, 1,700 annual openings."}
  ],
  "programs": [
    {"slug": "architecture", "note": "The programme itself, covering all three routes: the accredited professional degrees, the architectural technology associate, and landscape architecture."},
    {"slug": "construction-management", "note": "⚠⚠ The honest alternative for someone who wants to make buildings happen rather than author them: 30 Florida institutions against architecture's 6, no accredited-degree statute, and a $114,990 median.", "isRoute": False},
    {"slug": "drafting-and-design-technology", "note": "⚠ Where the architectural technology associate leads, and a common way to work in an architecture office while finishing a degree.", "isRoute": False},
    {"slug": "civil-engineering", "note": "⚠ Named for the mathematics comparison that changes who applies: civil engineering needs the calculus sequence, architecture at UF asks for precalculus.", "isRoute": False}
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

io.open('career_paths/architect.json', 'w', encoding='utf-8').write(
    json.dumps(path, ensure_ascii=False, indent=2))

for k in ("description", "credentialNote"):
    print(k, len(path[k]))
for c in path["courses"]:
    if len(c["reason"]) > 500 or len(c.get("variantNote", "")) > 1000:
        print("LONG", c["courseId"], len(c["reason"]), len(c.get("variantNote", "")))
for s in path["sources"]:
    if len(s["note"]) > 500:
        print("LONG SRC", s["label"], len(s["note"]))
for c in path["cipCodes"]:
    if len(c["note"]) > 500:
        print("LONG CIP", c["cipCode"], len(c["note"]))
for p in path["programs"]:
    if len(p["note"]) > 500:
        print("LONG PROG", p["slug"], len(p["note"]))
print("body", len(body))
