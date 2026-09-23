# -*- coding: utf-8 -*-
"""Assemble the urban and regional planning programme and the urban planner career path."""
import io, json

body = io.open('scratchpad/body_urp.html', encoding='utf-8').read()

program = {
  "slug": "urban-and-regional-planning",
  "name": "Urban and Regional Planning",
  "isPublished": True,
  "sortOrder": 630,
  "description": "Land use, growth management, transportation, housing and resilience: how communities decide what gets built where. ⚠⚠ In Florida this is a MASTER'S programme. Five universities hold PAB accreditation, all at master's level, and they award about 104 planning master's a year against 13 bachelor's.",
  "degreesNote": "⚠⚠⚠ THE ACCREDITED DEGREE IS A MASTER'S. PAB accredits five Florida programmes, all master's: UF's Master of Urban and Regional Planning (41 a year, campus and online), FSU's Master of Science in Planning (29), UCF's M.S. in Urban and Regional Planning (12), USF's MURP (12) and FAU's MURP (10). ⚠ UF's listed accreditation term ends 31 December 2026, so check the PAB site for its current status. ⚠ FAU also awards the only planning bachelor's in the state (13 a year), which is not on the PAB list, and UF adds 12 postbaccalaureate certificates. ⚠⚠ So the undergraduate major is a choice: public administration, geography, sustainability studies, architecture, economics and political science all feed planning master's programmes, and BLS names architecture, social science and business. Take GIS, statistics, state and local government and writing whatever the major. ⚠ Florida does not license planners; the professional credential is AICP.",
  "cips": [
    { "cipCode": "04.03", "note": "City/Urban, Community and Regional Planning — 129 Florida public credentials a year: master's at UF 41, FSU 29, UCF 12, USF 12 and FAU 10 (all PAB-accredited), FAU's 13 bachelor's, and UF's 12 postbaccalaureate certificates." }
  ],
  "related": [
    { "slug": "architecture", "note": "⚠ BLS names architecture as a feeder, and urban design and site planning are shared ground. The difference is scale and client: an architect designs a building for an owner; a planner writes the rules every building in the jurisdiction must meet.", "isRoute": False },
    { "slug": "civil-engineering", "note": "⚠ The planner's closest colleague on transportation, stormwater and infrastructure. Transportation planning (URP6711) and transportation engineering (TTE4004) meet at the metropolitan planning organisation.", "isRoute": False },
    { "slug": "environmental-science", "note": "⚠ Florida comprehensive plans carry conservation and coastal management elements, and resilience planning is now routine, so environmental science graduates move into planning master's programmes.", "isRoute": False },
    { "slug": "real-estate", "note": "⚠ The other side of the zoning table: developers and their consultants hire planners to navigate the same comprehensive plans and land-development codes.", "isRoute": False }
  ]
}
io.open('programs/urban-and-regional-planning.json', 'w', encoding='utf-8').write(json.dumps(program, ensure_ascii=False, indent=2))

courses = [
 ("POS2112", "State and Local Government — twenty carriers. ⚠⚠ Three in four planners work for local government, and this is the course about how counties, cities, commissions and boards actually decide.", None),
 ("ECO2023", "Microeconomics — thirty-nine carriers. ⚠ Land markets, housing affordability and development feasibility are microeconomics, and planning master's programmes assume it.", None),
 ("STA2023", "Elementary Statistics — thirty-nine carriers. ⚠ Population projections, travel surveys and census data are the raw material of a comprehensive plan.", None),
 ("GIS2040", "Fundamentals of Geographic Information Systems — ten carriers. ⚠⚠ GIS is named by BLS among the core of accredited planning programmes, and it is the skill most likely to open an entry-level planning post to a bachelor's graduate.",
  "⚠ The universities teach the principles course as GIS3043 (UF, UNF, College of the Florida Keys) or GIS4043 with GIS4043L (FSU, UWF). GIS3043 and GIS4043 are the same statewide course with a different level digit; GIS2040 is a different, lower-division course."),
 ("GEO3602", "Urban Geography — FIU, UF and USF. The spatial organisation of cities, their history and economics, and current urban problems. ⚠ The closest undergraduate course to the substance of planning outside a planning department.",
  "⚠ FAMU, FAU and FSU carry the same statewide course as GEO4602; the level digit is the institution's choice."),
 ("URP3000", "Introduction to Urban Planning and Design — FAU and FSU. The survey of the field: communities and regions, planning history, planning systems and methods. ⚠ The one undergraduate planning course worth taking before applying to a master's, to find out whether you like it.", None),
 ("PAD3003", "Public Administration — ten carriers. ⚠ Budgets, boards, public records and public process: the machinery a planning department works inside.", None),
 ("URP4710", "Introduction to Transportation Planning — FAU and FSU. Funding, legislation and methods. ⚠ Transportation is a major planning specialism, and Florida's metropolitan planning organisations are built around it.", None),
 ("URP4741", "Housing Policy and Planning — FAU and FSU. Housing markets, the history of housing policy, and community development. ⚠ Housing affordability is a recurring subject of Florida comprehensive-plan amendments and commission votes.", None),
 ("URP6100", "Planning Theory and History — UF and USF. BLS names planning theory among the core of accredited programmes: what planning is for, and the political setting of comprehensive planning.", None),
 ("URP5125", "Land Use Law — FSU and USF. Zoning, subdivision regulation, takings and due process. ⚠⚠ The law course is what separates a planner from a GIS analyst, and BLS names land use law as core to accredited programmes.",
  "⚠ FAU and UF teach the subject as URP6131 Legal Aspects of Planning. ⚠ The statewide record for URP?125 is titled Plan Implementation; read the carrier's title."),
 ("URP5312", "Growth Management and Comprehensive Planning — FGCU and FSU. ⚠⚠⚠ The Florida-specific course: the comprehensive plan every local government must maintain under s. 163.3167, and its seven-year evaluation under s. 163.3191.",
  "⚠ The statewide record for URP?312 is titled Local Land Use Planning; FSU and FGCU both teach it as growth management."),
 ("URP6270", "Introduction to GIS in Planning — FAU and UF. GIS applied to land-use analysis, suitability mapping and plan making. ⚠ BLS names GIS for planning as core to accredited programmes.", None),
 ("URP6711", "Multimodal Transportation Planning — FAU, UCF, UF and USF, four of the five accredited programmes. ⚠ The most widely carried planning course in the state.", None),
 ("URP6439", "Disaster Resilient Community — FAU and USF. ⚠⚠ Hazard mitigation and post-disaster redevelopment: in a hurricane state, routine planning work rather than a specialism.", None),
 ("URP6743", "Planning for Affordable Housing — UF and USF. Finance tools, inclusionary policy and the regulatory barriers to supply.", None),
 ("URP6277", "Urban Design: 3D and AI Applications — FAU and UF. ⚠ The only course on this path with AI in its title: 3D modelling and AI tools applied to urban design.", None),
 ("URP6920", "Planning Workshop — FAU and UF. ⚠⚠ A studio project, typically for a real client such as a local government or community group. It gives a planning graduate something concrete to show an employer.", None),
]

sources = [
 ("BLS Occupational Outlook Handbook — Urban and Regional Planners", "https://www.bls.gov/ooh/life-physical-and-social-science/urban-and-regional-planners.htm",
  "$89,320 median (2025), 45,800 jobs, +4% for 2025–35 and about 3,200 openings a year; entry-level education master's degree; 74% in local government; undergraduate backgrounds in architecture, social science or business; licensure only in New Jersey."),
 ("O*NET — Urban and Regional Planners (19-3051.00)", "https://www.onetonline.org/link/summary/19-3051.00",
  "Job Zone Five; 56% of respondents say a master's is required and 40% a bachelor's; average growth (3% to 4%) for 2024–34."),
 ("O*NET — Florida wages for 19-3051.00", "https://www.onetonline.org/link/localwages/19-3051.00?st=FL",
  "Florida median $80,720 against $89,320 national, and $5,000–$9,000 below national at every percentile."),
 ("Planning Accreditation Board — accredited programmes", "https://www.planningaccreditationboard.org/accredited-programs/all/",
  "Five Florida programmes, all master's: FAU (through 2030), FSU (2029), UCF (2032), UF (2026) and USF (2032)."),
 ("s. 163.3167, Florida Statutes — comprehensive plans", "https://www.flsenate.gov/Laws/Statutes/2025/163.3167",
  "\"Each local government shall maintain a comprehensive plan of the type and in the manner set out in this part.\""),
 ("s. 163.3191, Florida Statutes — evaluation and appraisal", "https://www.flsenate.gov/Laws/Statutes/2025/163.3191",
  "Each local government must evaluate its comprehensive plan at least once every 7 years; one that fails to may not initiate or adopt publicly initiated plan amendments until it complies."),
 ("American Planning Association — AICP certification", "https://www.planning.org/certification/",
  "AICP combines education, professional planning experience and an exam; \"members may take the AICP exam while completing their planning experience.\""),
 ("IPEDS completions — Florida, CIP 04.03 and neighbouring fields", "https://nces.ed.gov/ipeds/",
  "04.0301: 104 master's (UF 41, FSU 29, UCF 12, USF 12, FAU 10), 13 bachelor's at FAU and 12 UF postbaccalaureate certificates. Also the feeder fields: public administration (44.04), geography (45.07) and sustainability studies (30.33)."),
 ("SCNS statewide course file — URP, GIS and GEO", "https://flscns.fldoe.org/",
  "Carrier counts for every course named; statewide titles for URP?125 (Plan Implementation) and URP?312 (Local Land Use Planning) that the carriers have renamed; GIS?043 and GEO?602 carried at two level digits."),
]

path = {
  "slug": "urban-planner",
  "name": "Urban and Regional Planner",
  "cipCode": "04.03",
  "socCode": "19-3051",
  "isPublished": True,
  "sortOrder": 150,
  "description": "⚠⚠ The planning degree is a master's: all five PAB-accredited programmes in Florida are master's, and they award about 104 a year against 13 planning bachelor's (FAU only). So the undergraduate major is a choice, and this page compares the routes. ⚠ Florida law requires every county and city to maintain a comprehensive plan and review it every seven years, which is why 74% of planners work for local government. Median pay $89,320 nationally, $80,720 in Florida.",
  "credentialNote": "⚠ FLORIDA DOES NOT LICENSE PLANNERS — BLS names New Jersey as the only state that does. ⚠⚠ What matters is (1) a master's from a PAB-accredited programme — in Florida, UF, FSU, UCF, USF or FAU — and (2) the AICP certification from the American Planning Association, which combines education, years of professional planning experience (the number depends on the degree held) and an exam that may be taken before the experience is complete. ⚠ O*NET's respondents split 56% master's, 40% bachelor's: a bachelor's with GIS skills can get an entry-level planning post, and the master's can follow.",
  "cipCodes": [
    {"cipCode": "44.04", "note": "⚠⚠ Public Administration — the closest undergraduate route to the employer, since 74% of planners work for local government (BLS). Taught at bachelor's level at UCF, FIU, FAU, Indian River and St. Petersburg among others."},
    {"cipCode": "45.07", "note": "⚠⚠ Geography — BLS names social science as a feeder, and geography supplies GIS, which BLS lists as core to accredited planning programmes. Bachelor's at FSU, USF, UF and FIU."},
    {"cipCode": "04.02", "note": "⚠ Architecture — named by BLS as a feeder background, and the source of urban design and site-planning skills."},
    {"cipCode": "52.02", "note": "⚠ Business Administration — named by BLS as a feeder background: development finance, budgets and economic development are business skills."}
  ],
  "programs": [
    {"slug": "urban-and-regional-planning", "note": "The programme — at master's level everywhere it is accredited in Florida. Read its note for the five programmes and their accreditation terms."},
    {"slug": "architecture", "note": "⚠ A feeder BLS names. It suits someone drawn to urban design and the physical form of places.", "isRoute": False},
    {"slug": "environmental-science", "note": "⚠ A feeder for resilience, conservation and coastal planning, which Florida comprehensive plans require.", "isRoute": False},
    {"slug": "civil-engineering", "note": "⚠ The planner's colleague on transportation and infrastructure, not a route into planning itself.", "isRoute": False},
    {"slug": "real-estate", "note": "⚠ The development side of the same decisions: a planner working for a developer navigates the plan from outside.", "isRoute": False}
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

io.open('career_paths/urban-planner.json', 'w', encoding='utf-8').write(
    json.dumps(path, ensure_ascii=False, indent=2))

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
