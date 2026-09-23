# -*- coding: utf-8 -*-
"""Assemble the plumbing technology programme and the plumber career path (QUEUE row 148)."""
import io, json

body = io.open('scratchpad/body_plumber.html', encoding='utf-8').read()

program = {
  "slug": "plumbing-technology",
  "name": "Plumbing and Pipefitting Technology",
  "isPublished": True,
  "sortOrder": 650,
  "description": "Plumbing, pipefitting and fire sprinkler fitting, taught in Florida as clock-hour certificates at technical and state colleges and as the classroom half of registered apprenticeships. ⚠⚠ About 189 credentials a year at 22 public institutions: most Florida plumbers learn through apprenticeships and on-the-job hours, which these counts do not include.",
  "degreesNote": "⚠⚠ Plumbing Technology (46.0503) produces 144 credentials a year at 21 institutions, all certificates: Orange Technical West 25, Fort Myers Technical 19, Sheridan Technical 13, Hillsborough 12, Daytona State 12, Pinellas Technical 12. Pipefitting and Sprinkler Fitting (46.0502) adds 45 at five: Lively Technical 17, Seminole State 17, Hillsborough 7. ⚠⚠⚠ The clock-hour programme is four occupational completion points named after jobs, 960 hours in all: Helper, Plumber, Pipefitter (A, 360 hours), Residential Plumber (B, 240), Commercial Plumber (C, 240) and Plumber (D, 120). It is offered at about ten public institutions. ⚠ Apprenticeship classes run as Plumbing Apprenticeship I-VIII (BCA0450-BCA0457) at six state colleges, and fire sprinkler apprenticeships at Hillsborough, Miami Dade and Seminole State. ⚠ Florida's journeyman provision (s. 489.1455, F.S.) counts a registered and state-approved apprenticeship, or at least 12,000 hours of on-the-job training, so ask whether a programme is registered.",
  "cips": [
    { "cipCode": "46.05", "note": "Plumbing and Related Water Supply Services — 189 Florida public credentials a year at 22 institutions: Plumbing Technology (46.0503) 144 at 21, Pipefitting and Sprinkler Fitting (46.0502) 45 at 5. All certificates; no degrees." }
  ],
  "related": [
    { "slug": "electrical-technology", "note": "⚠ The sister trade, built the same way: a clock-hour certificate of completion points, or a paid apprenticeship. The electrician helper course is at 26 public institutions against about ten for plumbing. ⚠ Florida's journeyman reciprocity provision (s. 489.1455) names plumbing, pipe fitting, mechanical and HVAC, but not electrical." },
    { "slug": "hvac-technology", "note": "⚠ Shares the mechanical side of a building and the same journeyman reciprocity provision (s. 489.1455), which names HVAC alongside plumbing and pipe fitting. Pipefitting skills carry across." },
    { "slug": "construction-management", "note": "⚠ Where a plumber who wants to run jobs rather than work them goes. Florida's contractor exam can also be reached with college credit plus a year as a foreman (s. 489.111).", "isRoute": False }
  ]
}
io.open('programs/plumbing-technology.json', 'w', encoding='utf-8').write(json.dumps(program, ensure_ascii=False, indent=2))

courses = [
 ("BCV0508", "Helper, Plumber, Pipefitter — occupational completion point A, 360 hours, at ten public institutions. ⚠⚠ A hireable exit named after the job: a plumber's helper can start work here and continue into an apprenticeship.",
  "⚠ Pensacola State teaches it as BCV0508C, the same completion point with the lab integrated."),
 ("BCV0540", "Residential Plumber — completion point B, 240 hours, at eleven institutions. Houses: water supply, drain-waste-vent systems, fixtures and water heaters.",
  "⚠ Pensacola State: BCV0540C."),
 ("BCV0562", "Commercial Plumber — completion point C, 240 hours, at eleven institutions. Larger systems, commercial fixtures and code requirements for public buildings.",
  "⚠ Pensacola State: BCV0562C."),
 ("BCV0592", "Plumber — completion point D, 120 hours, at eight institutions, and the end of the 960-hour ladder. ⚠ Ask whether the college awards a certificate at each point, since not every school issues the intermediate ones.", None),
 ("BCV0596", "Plumbing Applications — 240 hours at Miami Dade, Palm Beach State and Pinellas Technical. ⚠ Applied practice beyond the four completion points; check where it sits in your college's sequence.",
  "⚠ Pensacola State: BCV0596C."),
 ("BCA0450", "Plumbing Apprenticeship I — the first of the classroom courses that run alongside a paid registered apprenticeship, at the College of the Florida Keys, Indian River, Miami Dade, Santa Fe and South Florida State. ⚠⚠ This is the route most plumbers take: BLS describes a 4- or 5-year apprenticeship with about 2,000 paid hours of work a year.",
  "⚠ Hours per course differ widely between colleges (about 33 to 99 for the same number). Daytona State pairs each level with a separate on-the-job lab (BCA0450L onward)."),
 ("BCA0451", "Plumbing Apprenticeship II — six carriers, including Daytona State.", None),
 ("BCA0452", "Plumbing Apprenticeship III — six carriers.", None),
 ("BCA0453", "Plumbing Apprenticeship IV — five carriers. ⚠ Around the middle of the sequence. The journeyman provision in s. 489.1455 counts a completed registered apprenticeship, or at least 12,000 hours of on-the-job training.", None),
 ("BCA0454", "Plumbing Apprenticeship V — six carriers.", None),
 ("BCA0455", "Plumbing Apprenticeship VI — six carriers.", None),
 ("BCA0456", "Plumbing Apprenticeship VII — four carriers.", None),
 ("BCA0457", "Plumbing Apprenticeship VIII — five carriers, the last level in the common sequence. ⚠ Completing a registered and state-approved apprenticeship is one of the routes to a journeyman licence that other Florida counties and municipalities must recognise (s. 489.1455).", None),
 ("BCV0568", "Industrial Pipefitter Helper — completion point A of the industrial pipefitter programme, 300 hours, at Hillsborough and Manatee Technical. ⚠ Process piping in plants and industrial sites, a branch of the same SOC occupation.", None),
 ("BCV0569", "Industrial Pipefitter — completion point B, 300 hours, at the same two institutions.", None),
 ("BCA0470", "Fire Sprinkler Apprenticeship I — Hillsborough, Miami Dade and Seminole State, the first of a sequence that continues through BCA0477 and advanced levels. ⚠⚠ Sprinklerfitters are part of this occupation, and BLS expects their employment to grow because of building codes in all states that require fire suppression systems.", None),
]

sources = [
 ("BLS Occupational Outlook Handbook — Plumbers, Pipefitters, and Steamfitters", "https://www.bls.gov/ooh/construction-and-extraction/plumbers-pipefitters-and-steamfitters.htm",
  "$63,800 median (2025), 510,600 jobs, +7% for 2025–35, about 42,000 openings a year, 8% self-employed. Entry: high school diploma and an apprenticeship of 4 or 5 years with about 2,000 paid hours a year. No mention of automation or AI."),
 ("O*NET — Plumbers, Pipefitters, and Steamfitters (47-2152.00)", "https://www.onetonline.org/link/summary/47-2152.00",
  "43% of respondents report a postsecondary certificate, 35% a high school diploma, 9% an associate degree; faster than average growth (5% to 6%) for 2024–34."),
 ("O*NET — Florida wages for 47-2152.00", "https://www.onetonline.org/link/localwages/47-2152.00?st=FL",
  "Florida median $52,910 against $63,800 national; 75th percentile $62,820 against $85,110; 90th $73,610 against $108,420. Employees only."),
 ("s. 489.1455, Florida Statutes — journeyman reciprocity", "https://www.flsenate.gov/Laws/Statutes/2025/489.1455",
  "Counties and municipalities issue journeyman licences, and must recognise a journeyman licence in plumbing, pipe fitting, mechanical or HVAC issued by another Florida county or municipality; conditions include a proctored examination, a registered apprenticeship or 12,000 hours of on-the-job training, and Florida Building Commission coursework."),
 ("s. 489.105, Florida Statutes — definitions", "https://www.flsenate.gov/Laws/Statutes/2025/489.105",
  "Defines the plumbing contractor's scope and the difference between a certified contractor (any jurisdiction) and a registered contractor (only the jurisdictions of registration)."),
 ("s. 489.111, Florida Statutes — contractor examination eligibility", "https://www.flsenate.gov/Laws/Statutes/2025/489.111",
  "Routes to the contractor exam, including 4 years of experience learned through an apprenticeship with at least 1 year as a foreman; 2,000 person-hours count as a full-time year."),
 ("SCNS statewide course file — BCV and BCA plumbing courses", "https://flscns.fldoe.org/",
  "BCV0508/0540/0562/0592 are plumbing completion points A-D (360, 240, 240 and 120 hours); BCA0450-0457 are Plumbing Apprenticeship I-VIII; BCA047x are fire sprinkler apprenticeship courses."),
 ("IPEDS completions — Florida, CIP 46.05", "https://nces.ed.gov/ipeds/",
  "46.0503 Plumbing Technology 144 at 21 institutions; 46.0502 Pipefitting and Sprinkler Fitting 45 at 5; 189 in total at 22, all certificates."),
]

path = {
  "slug": "plumber",
  "name": "Plumber, Pipefitter and Sprinkler Fitter",
  "cipCode": "46.05",
  "socCode": "47-2152",
  "isPublished": True,
  "sortOrder": 148,
  "description": "⚠⚠ A paid-apprenticeship trade: BLS describes 4 to 5 years of apprenticeship with about 2,000 paid hours a year, on a high school diploma. ⚠⚠⚠ Florida pays well below the national figure ($52,910 median against $63,800), and the gap widens to $34,810 at the 90th percentile. Florida's journeyman licence is issued locally but recognised in every county and city, and the contractor licence is the step that changes income.",
  "credentialNote": "⚠⚠⚠ TWO LEVELS OF LICENCE. The JOURNEYMAN licence is issued by counties and municipalities, and under s. 489.1455, F.S. every other Florida county and municipality must recognise it. The conditions include a proctored journeyman examination, a registered and state-approved apprenticeship or at least 12,000 hours of on-the-job training, and Florida Building Commission coursework. ⚠ The CONTRACTOR licence is state-issued under chapter 489: certified (any Florida jurisdiction) or registered (only where registered). To sit the certification exam, one route is 4 years of experience through an apprenticeship with at least 1 year as a foreman (s. 489.111). ⚠ A school certificate does not replace the hours. Choose a registered apprenticeship if you can, because it counts directly toward the journeyman licence.",
  "cipCodes": [
    {"cipCode": "46.03", "note": "⚠ Electrical and Power Transmission Installers — the sister trade, built the same way (completion points or a paid apprenticeship), but outside Florida's plumbing and HVAC journeyman reciprocity provision (s. 489.1455)."},
    {"cipCode": "15.05", "note": "⚠ HVAC/R Engineering Technology — where Florida files HVAC; shares piping skills and the same journeyman reciprocity provision as plumbing (s. 489.1455)."}
  ],
  "programs": [
    {"slug": "plumbing-technology", "note": "The programme — the four completion points, the apprenticeship classes, and where Florida teaches them."},
    {"slug": "hvac-technology", "note": "⚠ A neighbouring mechanical trade with the same journeyman reciprocity provision.", "isRoute": False},
    {"slug": "electrical-technology", "note": "⚠ The sister trade, more widely taught in Florida, with its own licensing.", "isRoute": False},
    {"slug": "construction-management", "note": "⚠ For a plumber heading toward running jobs or a contracting business.", "isRoute": False}
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

io.open('career_paths/plumber.json', 'w', encoding='utf-8').write(json.dumps(path, ensure_ascii=False, indent=2))

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
