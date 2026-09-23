# -*- coding: utf-8 -*-
"""Assemble the commercial truck driving programme and the truck driver career path (QUEUE row 145)."""
import io, json

body = io.open('scratchpad/body_truck.html', encoding='utf-8').read()

program = {
  "slug": "commercial-truck-driving",
  "name": "Commercial Truck Driving (CDL)",
  "isPublished": True,
  "sortOrder": 650,
  "description": "Training for a commercial driver's licence: tractor-trailer (Class A) and heavy straight truck (Class B), taught in Florida as short clock-hour certificates at technical and state colleges. ⚠⚠ Since 7 February 2022 federal law requires first-time Class A and B applicants to train with a provider on the FMCSA Training Provider Registry.",
  "degreesNote": "⚠⚠ All short certificates: 1,038 credentials in 2023 at 19 Florida public institutions, 929 of them 12-week-to-one-year certificates. Sheridan Technical 198, Indian River State 149, FSCJ 107, Marion Technical 81, Orange Technical 80, Miami Lakes Technical 73, Pensacola State 63. ⚠⚠ The Class A course is TRA0080 Tractor Trailer Truck Driver, 320 clock hours at 12 institutions; Class B is TRA0084, 150 hours. FSCJ splits the 320 hours into four 80-hour courses. ⚠⚠⚠ Ask whether the programme is listed on the FMCSA Training Provider Registry, for which class, because training from an unlisted provider does not satisfy 49 CFR 380.609. ⚠ Get the DOT medical certificate before paying for training, and note that Florida restricts CDL holders under 21 to intrastate driving.",
  "cips": [
    { "cipCode": "49.0205", "note": "Truck and Bus Driver/Commercial Vehicle Operator and Instructor — 1,038 Florida public credentials in 2023 at 19 institutions, all certificates: Sheridan Technical 198, Indian River State 149, FSCJ 107, Marion Technical 81, Orange Technical 80." }
  ],
  "related": [
    { "slug": "logistics-and-supply-chain", "note": "⚠ Where a driver's career goes off the road: dispatch, fleet management and supply chain. Miami Dade's TRA1420 Introduction to Trucking Operations is a college-credit bridge from the cab to the office.", "isRoute": False }
  ]
}
io.open('programs/commercial-truck-driving.json', 'w', encoding='utf-8').write(json.dumps(program, ensure_ascii=False, indent=2))

courses = [
 ("TRA0080", "Tractor Trailer Truck Driver — occupational completion point A, 320 clock hours, at 12 Florida public institutions. ⚠⚠ The Class A course. Ask whether the programme is on the FMCSA Training Provider Registry, because 49 CFR 380.609 requires first-time Class A applicants to train with a listed provider.",
  "⚠ Pensacola State carries it as TRA0080C, and FSCJ splits the same 320 hours into four 80-hour courses: TRA0081, TRA0082, TRA0083 and TRA0089."),
 ("TRA0084", "Truck Driver Heavy, Florida Class B — completion point A of the Class B route, 150 clock hours, at 8 institutions. ⚠ The shorter route, for straight trucks rather than tractor-trailers; Class B also requires registry training for first-time applicants.", None),
 ("TRA0086", "Tractor Operator — completion point B, 150 hours, at Miami Lakes Technical and Withlacoochee Technical. ⚠ Offered by two institutions only, so check before planning around it.", None),
 ("TRA0082", "Commercial Vehicle Driver Test Preparation — FSCJ, 80 hours. Preparation for the CDL knowledge and skills tests. ⚠ A learner's permit must be held 14 days before the skills test (49 CFR 383.25).", None),
 ("TRA0083", "Commercial Vehicle Driving Training/Experiences — FSCJ, 80 hours: straight-line and offset backing, parallel parking and alley docking, the basic control skills the CDL skills test examines.", None),
 ("TRA0089", "Commercial Vehicle Driving IV — FSCJ, 80 hours: urban, rural and expressway driving on public roads, toward the standard the CDL skills test requires.", None),
 ("TRA1420", "Introduction to Trucking Operations — Miami Dade, 3 credits. ⚠ DOT requirements, shipping documents, tracking, scheduling and equipment management. The college-credit step toward dispatch, fleet management and logistics.", None),
]

sources = [
 ("BLS Occupational Outlook Handbook — Heavy and Tractor-Trailer Truck Drivers", "https://www.bls.gov/ooh/transportation-and-material-moving/heavy-and-tractor-trailer-truck-drivers.htm",
  "$58,640 median (2025), 2,221,200 jobs, +4% for 2025–35, about 214,500 openings a year; entry-level education postsecondary nondegree award; 7% self-employed; paid mostly by the mile. No mention of automation, self-driving trucks or AI."),
 ("O*NET — Heavy and Tractor-Trailer Truck Drivers (53-3032.00)", "https://www.onetonline.org/link/summary/53-3032.00",
  "Job Zone One to Two; 54% of respondents report a high school diploma; average growth (3% to 4%) for 2024–34 and about 237,600 openings a year."),
 ("O*NET — Florida wages for 53-3032.00", "https://www.onetonline.org/link/localwages/53-3032.00?st=FL",
  "Florida median $50,640 against $58,640 nationally, and below national at every percentile."),
 ("49 CFR 380.609 — Entry-level driver training", "https://www.law.cornell.edu/cfr/text/49/380.609",
  "First-time Class A or B CDL applicants, and upgrades, must complete training from a provider on the Training Provider Registry; applies from 7 February 2022."),
 ("49 CFR 383.25 — Commercial learner's permit", "https://www.law.cornell.edu/cfr/text/49/383.25",
  "A CLP holder may not take the CDL skills test in the first 14 days after the permit is issued; the permit is valid for up to one year."),
 ("49 CFR 391.11 and 391.45 — Driver qualification and medical certificates", "https://www.law.cornell.edu/cfr/text/49/391.11",
  "An interstate commercial driver must be at least 21 and physically qualified; the medical examiner's certificate lasts at most 24 months, less for some conditions."),
 ("FLHSMV — Commercial motor vehicle drivers", "https://www.flhsmv.gov/driver-licenses-id-cards/commercial-motor-vehicle-drivers/",
  "Florida CDL applicants must be at least 18; applicants under 21 are restricted to intrastate operation only."),
 ("SCNS statewide course file — TRA", "https://flscns.fldoe.org/",
  "TRA0080 Tractor Trailer Truck Driver OCP A (320 hours) at 12 public institutions; TRA0084 Class B OCP A (150) at 8; TRA0086 Tractor Operator OCP B (150) at 2; FSCJ's TRA0081–0089 at 80 hours each. All guaranteed transfer."),
 ("IPEDS completions — Florida, CIP 49.0205", "https://nces.ed.gov/ipeds/",
  "1,038 credentials in 2023 at 19 public institutions, all certificates, led by Sheridan Technical 198 and Indian River State 149."),
]

path = {
  "slug": "truck-driver",
  "name": "Commercial Truck Driver",
  "cipCode": "49.02",
  "socCode": "53-3032",
  "isPublished": True,
  "sortOrder": 145,
  "description": "⚠⚠ A federally licensed job with about 214,500 openings a year and a training requirement that became federal law in 2022: first-time Class A and B CDL applicants must train with a provider on the FMCSA Training Provider Registry. Florida's public Class A course is 320 clock hours. ⚠ Florida pays $50,640 at the median against $58,640 nationally, and drivers under 21 may drive only within Florida.",
  "credentialNote": "⚠⚠⚠ THE CDL IS FEDERAL. First-time Class A and B applicants must complete entry-level driver training from a provider on the FMCSA Training Provider Registry (49 CFR 380.609, from 7 February 2022), so ask any school whether it is listed and for which class. ⚠⚠ The steps: a DOT medical certificate (49 CFR 391, valid up to 24 months), a commercial learner's permit held at least 14 days (49 CFR 383.25), registry training, then the skills test. ⚠ Florida issues a CDL at 18 but restricts drivers under 21 to intrastate operation (FLHSMV); crossing state lines requires 21 (49 CFR 391.11). Drivers are subject to random drug and alcohol testing, and a hazardous materials endorsement adds a knowledge test and a background check.",
  "cipCodes": [
    {"cipCode": "52.02", "note": "⚠ Business Administration and Management — the route off the road into dispatch, fleet and transport management, which the logistics programmes also serve."}
  ],
  "programs": [
    {"slug": "commercial-truck-driving", "note": "The programme — read its note for the Training Provider Registry question and where Florida's public programmes are."},
    {"slug": "logistics-and-supply-chain", "note": "⚠ Where a driver's career can go off the road: dispatch, fleet management and supply chain.", "isRoute": False}
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

io.open('career_paths/truck-driver.json', 'w', encoding='utf-8').write(json.dumps(path, ensure_ascii=False, indent=2))
for k in ("description", "credentialNote"):
    print(k, len(path[k]))
print('prog', len(program['description']), len(program['degreesNote']), 'body', len(body))
