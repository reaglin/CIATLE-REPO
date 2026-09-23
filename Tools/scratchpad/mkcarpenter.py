# -*- coding: utf-8 -*-
"""Assemble the carpentry programme and the carpenter career path (QUEUE row 149)."""
import io, json

body = io.open('scratchpad/body_carpenter.html', encoding='utf-8').read()

program = {
  "slug": "carpentry",
  "name": "Carpentry and Building Construction Technology",
  "isPublished": True,
  "sortOrder": 650,
  "description": "Rough framing, forms, finish carpentry and building construction, taught in Florida as clock-hour career certificates at technical colleges. ⚠⚠ A small programme: about 150 credentials a year across two codes, for an occupation most people enter through a job or a registered apprenticeship.",
  "degreesNote": "⚠⚠ Carpentry (46.0201) produces 57 certificates a year at 15 Florida public institutions: Atlantic Technical 12, Erwin Technical 12, Fort Myers Technical 10, Pensacola State 6. Building Construction Technology (46.0415) adds 97 certificates at 15, led by Manatee Technical 21 and Pinellas Technical 12. No associate or bachelor's degree is awarded in either code. ⚠ The clock-hour courses are titled after jobs (Carpenter Helper, Carpenter Rough, Trim and Finish Carpenter, Building Construction Technician), but colleges carry different versions of the ladder, so ask which courses and how many hours make up the certificate. ⚠⚠ Florida licenses the contractor, not the carpenter: the certified contractor exam needs four years of experience including one as foreman, and college credit in building construction can replace up to three of those years (s. 489.111, F.S.). A registered apprenticeship in carpentry also exists.",
  "cips": [
    { "cipCode": "46.0201", "note": "Carpentry/Carpenter — 57 certificates a year at 15 Florida public institutions (Atlantic Technical 12, Erwin Technical 12, Fort Myers Technical 10, Pensacola State 6, Suncoast Technical 5, Florida Panhandle Technical 5). The clock-hour Carpentry career certificate." },
    { "cipCode": "46.0415", "note": "Building Construction Technology — 97 certificates at 15 institutions (Manatee Technical 21, Pinellas Technical 12, Lively Technical 9, Okaloosa Technical 9). Claimed because its ladder (Building Construction Helper, then Technician 1 and 2) teaches carpentry alongside the other building trades." }
  ],
  "related": [
    { "slug": "construction-management", "note": "⚠⚠ The college route that shortens the way to a contractor's licence. Florida lets college credit replace up to three of the four experience years for the certified contractor exam, and a building construction bachelor's leaves one year (s. 489.111). The step a carpenter takes to work for themselves." },
    { "slug": "drafting-and-design-technology", "note": "⚠ Reading and producing construction drawings. Blueprint reading is part of a lead carpenter's job.", "isRoute": False },
    { "slug": "electrical-technology", "note": "⚠ The neighbouring building trade, taught at many of the same technical colleges. Unlike carpentry, electrical work is licensed at the contractor level under a separate part of chapter 489.", "isRoute": False }
  ]
}
io.open('programs/carpentry.json', 'w', encoding='utf-8').write(json.dumps(program, ensure_ascii=False, indent=2))

courses = [
 ("BCV0107", "Carpenter Helper — completion point A, 300 hours, at six technical colleges. Tools, safety, materials and measuring. ⚠ The first hireable exit.", None),
 ("BCV0122", "Carpenter Rough — 450 hours, eight carriers. Framing floors, walls and roofs: the structural half of the trade, and the half that falls under contractor licensing when you work for yourself.", None),
 ("BCV0111", "Trim and Finish Carpenter — completion point B, 300 hours, seven carriers. Doors, windows, trim, stairs and cabinets. ⚠ Since 2021, Florida bars local governments from licensing cabinetry and similar finish trades that have no state contractor category (s. 489.117(4)).",
  "⚠ BCV0128 Carpenter is also labelled completion point B (150 hours) at six colleges, so ask which version your college teaches."),
 ("BCV0128", "Carpenter — 150 hours, six carriers, the course named after the occupation and the end of the ladder at the colleges that carry it.", None),
 ("BCV0123", "Foundations and Forms — Miami Dade and Palm Beach State, 150 hours. Trenching, excavation, footings and concrete forms. The statewide record says it prepares students for NCCER certification.",
  "⚠ These two colleges run a separate 150-hour sequence that starts with BCV0112 Introduction to Carpentry, which the statewide file classifies not automatically transferable."),
 ("BCV0131", "Residential Carpentry I — Indian River and Santa Fe: safety, tools, materials, fasteners and construction math.",
  "⚠ BCV0132 Residential Carpentry II follows it: windows, doors and stairs."),
 ("BCV0400", "Building Construction Helper — completion point A, 450 hours, seven carriers. The Building Construction Technology ladder covers carpentry alongside the other building trades.",
  "⚠ BCV0401 and BCV0402 Building Construction Technician 1 and 2 (300 hours each) are its completion point B."),
 ("BCV0243", "Cabinetmaker — completion point D, 450 hours, at three technical colleges. ⚠ A specialism a finish carpenter can move into, and one no Florida local government may license (s. 489.117(4)).", None),
 ("BCN1272", "Blueprint Reading — eight carriers. ⚠⚠ Reading plans is a lead carpenter's skill. The course is also college credit, which counts toward the contractor exam's experience requirement (s. 489.111).",
  "⚠ Hillsborough, Santa Fe, Seminole State and Tallahassee State teach BCN2272 Blueprint Reading."),
 ("BCN1001", "Building Construction — seven carriers. The survey of how buildings go together, and the usual first college-credit course in building construction.", None),
 ("BCN1210", "Building Construction Materials — Daytona State, Hillsborough, Santa Fe and UF. Wood, concrete, masonry and steel: what each is used for and why.",
  "⚠ Broward, FGCU, FSCJ and UNF teach BCN1210C Construction Materials with an integrated lab; FAMU and others teach BCN2230 Materials and Methods."),
 ("BCN2280", "Surveying and Construction Layout — FIU, FSCJ and State College of Florida. ⚠ Layout decides whether everything framed after it is square and where the plans say.", None),
 ("BCN3730", "Construction Safety — FIU, St. Petersburg, Seminole State and UF. ⚠ BLS says every carpenter must pass the OSHA 10-hour course, and falls are among the injuries it names. A foreman is responsible for a crew's safety.", None),
 ("BCN4612C", "Advanced Construction Estimating — FGCU, St. Petersburg, Seminole State and UF. ⚠⚠ The skill a contractor needs and a carpenter usually lacks: pricing a job so that it makes money.", None),
]

sources = [
 ("BLS Occupational Outlook Handbook — Carpenters", "https://www.bls.gov/ooh/construction-and-extraction/carpenters.htm",
  "$60,580 median (2025), 889,700 jobs, +4% for 2025–35, about 62,800 openings a year; entry with a high school diploma and apprenticeship; 25% self-employed, and the pay figures exclude them. Modular and prefabricated components reduce the need for carpenters; OSHA 10-hour course required."),
 ("O*NET — Carpenters (47-2031.00)", "https://www.onetonline.org/link/summary/47-2031.00",
  "Job Zone One to Two; 52% of respondents report a high school diploma and 21% a postsecondary certificate; faster than average growth (5% to 6%) for 2024–34 and about 74,100 openings a year."),
 ("O*NET — Florida wages for 47-2031.00", "https://www.onetonline.org/link/localwages/47-2031.00?st=FL",
  "Florida median $49,870 against $60,580 national; the gap grows from −$3,500 at the 10th percentile to −$29,960 at the 90th ($69,950 against $99,910)."),
 ("s. 489.111, Florida Statutes — contractor exam eligibility", "https://www.flsenate.gov/Laws/Statutes/2025/489.111",
  "Four years of experience with at least one as foreman, or combinations replacing up to three years with college credits, or a bachelor's in engineering, architecture or building construction plus one year."),
 ("s. 489.105, Florida Statutes — contractor definitions", "https://www.flsenate.gov/Laws/Statutes/2025/489.105",
  "Defines contractor, and general, building (up to three stories) and residential (up to two habitable stories) contractors."),
 ("s. 489.103, Florida Statutes — exemptions", "https://www.flsenate.gov/Laws/Statutes/2025/489.103",
  "Employees working within a licensed contractor's scope are exempt; jobs under an aggregate $2,500 are exempt unless part of a larger operation or advertised as contracting."),
 ("s. 489.117, Florida Statutes — local licensing", "https://www.flsenate.gov/Laws/Statutes/2025/489.117",
  "Local governments may not require a licence for a job scope that does not substantially correspond to a state contractor category; painting, flooring, cabinetry and handyman services are among those listed."),
 ("CPALMS-CTE — Florida carpentry programmes (CIP 46.02)", "https://ctepreview.cpalms.org/",
  "Carpentry clock-hour career certificate, a secondary Carpentry programme, and Carpentry - APPR, a registered apprenticeship."),
 ("SCNS statewide course file — BCV and BCN", "https://flscns.fldoe.org/",
  "BCV0107 Carpenter Helper OCP A (300 hours), BCV0111 Trim and Finish Carpenter OCP B (300), BCV0128 Carpenter OCP B (150), BCV0122 Carpenter Rough (450), BCV0400–0402 Building Construction Helper and Technician; carrier counts for every course named."),
 ("IPEDS completions — Florida, CIP 46.0201 and 46.0415", "https://nces.ed.gov/ipeds/",
  "Carpentry 57 certificates at 15 institutions; Building Construction Technology 97 at 15. No degrees."),
]

path = {
  "slug": "carpenter",
  "name": "Carpenter",
  "cipCode": "46.02",
  "socCode": "47-2031",
  "isPublished": True,
  "sortOrder": 149,
  "description": "⚠⚠⚠ Florida carpenters earn a median $49,870, $10,710 below the national figure, and the gap grows to $29,960 at the 90th percentile. The way up in Florida is to become the contractor. ⚠⚠ Florida licenses contractors, not carpenters: the contractor exam needs four years of experience including one as foreman, and college credit can replace up to three of them. Florida trains only about 150 carpenters a year in programmes; most learn on the job or through apprenticeship.",
  "credentialNote": "⚠⚠ NO STATE LICENCE TO WORK AS A CARPENTER. An employee of a licensed contractor is exempt (s. 489.103(2), F.S.). Taking jobs yourself is contracting: the certified residential, building and general contractor licences cover it (s. 489.105), and the exam needs four years of experience, at least one as foreman. College credit can replace up to three of those years, and a bachelor's in building construction leaves one (s. 489.111). ⚠ Jobs under $2,500 are exempt unless part of a larger operation (s. 489.103(9)). ⚠⚠ Since 2021 local governments may not license job scopes outside the state categories, and the statute names cabinetry, flooring and painting among them (s. 489.117(4)). ⚠ BLS: all carpenters must pass the OSHA 10-hour safety course.",
  "cipCodes": [
    {"cipCode": "46.04", "note": "⚠ Building/Construction Finishing, Management and Inspection — where Florida files Building Construction Technology (46.0415, 97 certificates at 15 institutions), a ladder that teaches carpentry alongside the other building trades."},
    {"cipCode": "52.20", "note": "⚠⚠ Construction Management — the college route that shortens the way to a contractor's licence, since s. 489.111 lets college credit replace up to three of the four experience years."}
  ],
  "programs": [
    {"slug": "carpentry", "note": "The programme. ⚠ Read its note: small, clock-hour, and assembled from job-titled courses that vary from college to college."},
    {"slug": "construction-management", "note": "⚠⚠ The step from carpenter to contractor. College credit in building construction counts toward the contractor exam's experience requirement."},
    {"slug": "drafting-and-design-technology", "note": "⚠ Construction drawings, the skill a lead carpenter needs.", "isRoute": False},
    {"slug": "electrical-technology", "note": "⚠ The neighbouring building trade at the same technical colleges.", "isRoute": False}
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

io.open('career_paths/carpenter.json', 'w', encoding='utf-8').write(json.dumps(path, ensure_ascii=False, indent=2))

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
