# -*- coding: utf-8 -*-
"""Assemble the professional pilot programme and the commercial pilot career path."""
import io, json

body = io.open('scratchpad/body_pilot.html', encoding='utf-8').read()

program = {
  "slug": "professional-pilot",
  "name": "Professional Pilot and Aviation Science",
  "isPublished": True,
  "sortOrder": 620,
  "description": "Flight training toward the FAA certificates a working pilot needs: private, instrument, commercial, multi-engine and flight instructor, taught at Florida state colleges as an associate degree, a certificate or an aviation-science bachelor's. ⚠⚠ The cost is flight time, not tuition: Pasco-Hernando State publishes $64,579.80 in flight fees against $4,838.28 in in-state tuition.",
  "degreesNote": "⚠⚠ Small and entirely at the state colleges: about 140 credentials a year, and no Florida state university awards a pilot degree under these codes. Professional pilot (49.0102) produces 81 — Broward 45, Miami Dade 19, Polk State 14, FSCJ 3 — with Northwest Florida State, Palm Beach State, Pasco-Hernando and Santa Fe also offering it. The aviation-science bachelor's (49.0101) adds 57 at Broward (31) and Polk State (26). ⚠⚠⚠ THE QUESTION TO ASK EVERY PROGRAMME: does it hold an FAA letter of authorisation for the restricted-privileges ATP, and for which hour figure? An authorised associate degree with 30 aviation credits cuts the airline minimum from 1,500 hours to 1,250; an authorised bachelor's with 60 cuts it to 1,000 — but only when the flying was done in the institution's Part 141 curriculum. ⚠ Public colleges often contract the flying to a private Part 141 school (Broward uses Phoenix East Aviation), so ask who owns the aircraft and sets the schedule. ⚠ Get the FAA medical certificate before paying for any flight training.",
  "cips": [
    { "cipCode": "49.0102", "note": "Airline/Commercial/Professional Pilot and Flight Crew — 81 credentials in 2023: Broward 45 (associate and certificate), Miami Dade 19, Polk State 14, FSCJ 3; Northwest Florida State, Palm Beach State, Pasco-Hernando and Santa Fe offer it but recorded none that year." },
    { "cipCode": "49.0101", "note": "Aeronautics/Aviation/Aerospace Science and Technology — the bachelor's: Broward 31 and Polk State 26. ⚠ A bachelor's with 60 aviation credits at an FAA-authorised institution is what reaches the 1,000-hour restricted ATP." }
  ],
  "related": [
    { "slug": "aviation-maintenance-technology", "note": "⚠ The other federally certificated aviation career, taught at many of the same colleges. It costs a fraction of flight training because the student is not paying by the hour for an aircraft, and it is a common way into an airline for people who later learn to fly.", "isRoute": False },
    { "slug": "aerospace-engineering", "note": "⚠ BLS says airlines want a bachelor's in any field and names engineering among them. An engineering degree plus separate flight training is a legitimate route, but it does not count toward the restricted ATP, which needs aviation coursework at an authorised institution.", "isRoute": False },
    { "slug": "logistics-and-supply-chain", "note": "⚠ Where aviation management graduates often end up: air cargo, airport and airline operations. A route into aviation for someone who wants the industry without the flight-training bill.", "isRoute": False }
  ]
}
io.open('programs/professional-pilot.json', 'w', encoding='utf-8').write(json.dumps(program, ensure_ascii=False, indent=2))

courses = [
 ("ATT1100", "Private Pilot Flight Theory — seven carriers, the widest course in aviation. The ground school for the FAA private pilot knowledge test: aerodynamics, weather, navigation, regulations. ⚠ Take it before or alongside the first flight course, since flight hours are cheaper when the theory is already done.",
  "⚠ FSCJ splits it into ATT1102 and ATT1103; Gulf Coast teaches ATT1100C with an integrated lab."),
 ("ATF1100L", "Private Pilot Flight — Northwest Florida State, Polk State and UWF. The first certificate. ⚠⚠ The FAA minimum is 35 hours under Part 141 and 40 under Part 61, and most students fly more, paying by the hour.",
  "⚠⚠ Florida numbers this five ways: ATF1100L here, ATF1100C at Broward, ATF1108L + ATF1109L as two phases at FSCJ, and ATF1114L accelerated at Miami Dade. The statewide title says 2-3 credits and most carriers award 1. Register by what the course delivers: does it end with the private pilot checkride?"),
 ("ASC1210", "Aviation Meteorology — seven carriers. ⚠ Weather decisions are among the hardest judgements in flying, and in Florida summer they mean afternoon thunderstorms that build faster than a training aircraft can climb over them.", None),
 ("ASC1610", "Aircraft Systems and Components — six carriers. Engines, electrical, hydraulic and flight-control systems. ⚠ The course that makes a checklist make sense rather than a list to be recited.", None),
 ("ATT1120", "Instrument Pilot Ground School — FSCJ, Northwest Florida State, Pasco-Hernando and UWF. Preparation for the FAA instrument rating knowledge test.",
  "⚠ Broward, Miami Dade and Polk State carry the same statewide course as ATT2120. The level digit is the institution's choice; they are one course."),
 ("ATF2305", "Instrument Pilot Flight — Broward, FSCJ, Miami Dade and Pasco-Hernando. ⚠⚠ The rating that makes a pilot employable: no charter, air ambulance or airline job is flown without it.",
  "⚠ Northwest Florida State and Polk State teach it as ATF2305L."),
 ("ATT2110", "Commercial Pilot Ground School — five carriers. Preparation for the FAA commercial knowledge test: performance, weight and balance, advanced navigation, physiology of flight.",
  "⚠ FSCJ and UWF carry the same statewide course as ATT1110."),
 ("ATF2201", "Commercial Pilot I — FSCJ and Pasco-Hernando, the first of three. ⚠⚠ This is where the 250-hour commercial minimum is built, and where the programme's cost is concentrated: Pasco-Hernando prices its commercial flight courses at $23,273.90.",
  "⚠⚠ Florida packages commercial flight four ways: ATF2201-2203 (FSCJ, Pasco-Hernando), ATF2201L-2203L (Northwest Florida State), ATF2204 (Broward) and ATF2204L (UWF). Finish the certificate before changing programme; partial Part 141 stages do not reliably carry over."),
 ("ATF2400", "Multi-Engine Flight — Broward, FSCJ, Miami Dade and Pasco-Hernando. ⚠ Every airline aircraft has more than one engine, and airlines look for multi-engine time in the logbook.", None),
 ("ATT2131", "Certified Flight Instructor Ground School — FSCJ, Miami Dade and Northwest Florida State. The fundamentals of instruction and the flight instructor knowledge tests. ⚠⚠ The instructor certificate is how most pilots are paid while building from 250 hours toward 1,500.",
  "⚠ Polk State teaches the fundamentals as ATT2130, and Polk State and UWF offer an upper-division version, ATT3134, which adds the FAA Advanced Ground Instructor certificate. The state lets a student choose the lower or upper version, and the upper one counts toward a bachelor's."),
 ("ATF2500", "Certified Flight Instructor — Broward and FSCJ. The flight training for the CFI certificate. ⚠⚠ Most new commercial pilots' first paid flying job.",
  "⚠⚠ Same FAA certificate, different credit values: ATF2500L is 1 credit at Northwest Florida State and Polk State, and the upper-division ATF3502L is 1 credit at Polk State and 3 at UWF. Because the restricted ATP counts aviation CREDIT HOURS, the lower credit values can leave a student short of the 30 or 60 needed."),
 ("ASC1310", "Aviation Regulations — FSCJ, Pasco-Hernando and Polk State. 14 CFR Parts 61, 91, 121 and 135: what a pilot may and may not do, and what an operator must. ⚠ The law is examined on every FAA knowledge test and checkride.",
  "⚠ Broward and Miami Dade cover the subject as ASC2320 Aviation Law and Regulations."),
 ("ASC2870", "Aviation Safety — five carriers. Accident causation, safety management systems and reporting culture. ⚠ Federal rules already require a safety management system of airlines, and the same framework is being extended to charter operators.", None),
 ("ASC1550", "Aerodynamics — Broward, Miami Dade and Polk State. Lift, drag, stability and performance beyond what the private pilot course covers. ⚠ It explains the performance charts a commercial pilot is tested on.", None),
 ("ASC4460", "Crew Resource Management — Polk State and UWF. Communication, workload and decision-making on a two-pilot flight deck. ⚠⚠ Airline interviews test it directly, and it is the part of airline flying a single-pilot trainer never practises.",
  "⚠ Northwest Florida State and Polk State teach a lower-division version as ASC2473 Human Factors and Resource Management."),
 ("ASC4671", "Transport Category Aircraft Operations — Broward and Polk State. Jet systems, high-altitude operations and airline procedures. ⚠ The bridge from training aircraft to the aircraft an airline flies.", None),
 ("ATT2640", "Advanced Aircraft: Turboprop and Turbine — FSCJ and Pasco-Hernando. ⚠ Turbine knowledge is what charter, cargo and regional operators look for in a low-time pilot.", None),
]

sources = [
 ("BLS Occupational Outlook Handbook — Airline and Commercial Pilots", "https://www.bls.gov/ooh/transportation-and-material-moving/airline-and-commercial-pilots.htm",
  "Airline pilots $232,140 and commercial pilots $123,220 median (2025); 154,900 jobs, +7% for 2025–35, about 16,400 openings a year; retirement at 65; the flight-instructor and charter route to building hours; commercial-pilot industries (nonscheduled 38%, schools 11%, health care 10%). No mention of automation or AI."),
 ("O*NET — Commercial Pilots (53-2012.00)", "https://www.onetonline.org/link/summary/53-2012.00",
  "Job Zone Three (vocational training or an associate degree); faster than average growth (5% to 6%) for 2024–34 and about 6,600 openings a year; Air Transport Pilot is a registered apprenticeship title."),
 ("O*NET — Florida wages, commercial pilots and airline pilots", "https://www.onetonline.org/link/localwages/53-2012.00?st=FL",
  "Commercial: Florida median $121,890 vs $123,220, 90th $229,110 vs $266,620. Airline (53-2011): Florida median $225,020 vs $232,140, 90th $356,680 vs $463,830."),
 ("14 CFR 61.160 — Restricted-privileges airline transport pilot", "https://www.law.cornell.edu/cfr/text/14/61.160",
  "750 hours for military pilots; 1,000 for a bachelor's with an aviation major and 60 aviation credits; 1,250 for an associate with 30, or a bachelor's with 30–59; only at institutions with a letter of authorisation under § 61.169, with the flying done in an approved Part 141 curriculum."),
 ("14 CFR 61.129 — Commercial pilot aeronautical experience", "https://www.law.cornell.edu/cfr/text/14/61.129",
  "250 hours of flight time, including 100 hours as pilot in command and 20 hours of training on the areas of operation."),
 ("14 CFR 61.23 — Medical certificates", "https://www.law.cornell.edu/cfr/text/14/61.23",
  "At least a second-class medical to exercise commercial pilot privileges; first-class for pilot-in-command privileges of an ATP certificate."),
 ("Pasco-Hernando State College — Professional Pilot Technology", "https://phsc.edu/academics/programs/transportation/pilot",
  "Total flight fees $64,579.80 against in-state tuition of $4,838.28, with per-certificate costs, and the warning that hours and prices could be more depending on how much training a student needs."),
 ("Broward College — Emil Buehler Aviation Institute", "https://www.broward.edu/academics/programs/aviation/index.html",
  "Part 141 Professional Pilot Technology, flight training in partnership with Phoenix East Aviation, and a $3,500 minimum flight-account deposit."),
 ("Polk State College — Aerospace", "https://www.polk.edu/aerospace/",
  "Professional Pilot Science A.S., Aerospace Sciences B.S. with a professional pilot concentration, and a Republic Airways cadet programme."),
 ("IPEDS completions — Florida, CIP 49.01", "https://nces.ed.gov/ipeds/",
  "49.0102 professional pilot: 81 credentials at Broward, Miami Dade, Polk State and FSCJ; 49.0101 aviation science bachelor's: 57 at Broward and Polk State."),
]

path = {
  "slug": "commercial-pilot",
  "name": "Commercial and Airline Pilot",
  "cipCode": "49.01",
  "socCode": "53-2012",
  "isPublished": True,
  "sortOrder": 144,
  "description": "⚠⚠ The commercial certificate (250 hours) lets you be paid to fly, but airlines need 1,500, and nearly everyone fills the gap by working as a flight instructor or charter pilot. ⚠⚠⚠ The cost is flight time, not tuition: one Florida college publishes $64,579.80 in flight fees against $4,838.28 in tuition. A qualifying aviation degree cuts the airline minimum to 1,250 or 1,000 hours. Median pay: $123,220 for commercial pilots, $232,140 for airline pilots.",
  "credentialNote": "⚠⚠⚠ THE CREDENTIALS ARE FAA CERTIFICATES, NOT DEGREES: private, instrument, commercial (250 hours, 14 CFR 61.129), multi-engine, flight instructor, then the airline transport pilot certificate at 1,500 hours. ⚠⚠ An aviation degree from an institution with an FAA letter of authorisation qualifies for the restricted ATP (14 CFR 61.160): 1,250 hours with an associate and 30 aviation credits, 1,000 with a bachelor's and 60 — but only if the flying was done in that institution's Part 141 curriculum. Ask for the letter before enrolling. ⚠⚠ A second-class FAA medical is needed to fly commercially and a first-class one to captain an airliner (14 CFR 61.23). Get it before paying for flight training. ⚠ What transfers between programmes is the certificate, not the course number, so finish a certificate before moving.",
  "cipCodes": [
    {"cipCode": "52.02", "note": "⚠ Business Administration — BLS: airline pilots \"typically need a bachelor's degree in any field, including transportation, engineering, or business.\" A business degree with separate flight training is a real route, though it does not reduce the ATP hours."}
  ],
  "programs": [
    {"slug": "professional-pilot", "note": "The programme. ⚠⚠ Read its note first: ask every school for its FAA restricted-ATP letter of authorisation, and who actually runs the flying."},
    {"slug": "business-administration", "note": "⚠ BLS names business among the degrees airlines accept. It is the portable choice if flying does not work out, but it does not shorten the ATP hours and the flight training is paid for separately."},
    {"slug": "aerospace-engineering", "note": "⚠ Named by BLS among acceptable degrees. An engineering degree plus separate flight training is a legitimate route to an airline, but it does not count toward the restricted ATP.", "isRoute": False},
    {"slug": "aviation-maintenance-technology", "note": "⚠ The other federally certificated aviation career, taught at many of the same colleges, without the per-hour flight bill.", "isRoute": False}
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

io.open('career_paths/commercial-pilot.json', 'w', encoding='utf-8').write(
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
