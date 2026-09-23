# -*- coding: utf-8 -*-
"""Assemble the veterinary technology programme and the veterinary technician career path.

Row 105 of QUEUE.csv, unblocked by the 2026-09-23 seed widening (01.83). ⚠ Florida files
veterinary technology under 01.83 (Agriculture), not 51.0808, which has no Florida rows.
"""
import io, json

body = io.open('scratchpad/body_vettech.html', encoding='utf-8').read()

program = {
  "slug": "veterinary-technology",
  "name": "Veterinary Technology and Veterinary Assisting",
  "isPublished": True,
  "sortOrder": 650,
  "description": "Animal nursing, anaesthesia, laboratory, imaging and dental work under a veterinarian's supervision. ⚠⚠ Florida files two different credentials under one code: the associate degree that leads to veterinary technician, and short clock-hour veterinary assisting certificates, which are the majority of awards.",
  "degreesNote": "⚠⚠⚠ CHECK WHICH ONE YOU ARE ENROLLING IN. About 293 Florida public credentials a year sit under CIP 01.8301. Roughly 178 are certificates of under a year, mostly veterinary assisting at technical colleges (Aparicio-Levy 90, Orange Technical 27, Lake Technical 19, Lorenzo Walker 16, Cape Coral 15), on the ATE0006/ATE0072 clock-hour ladder. These lead to veterinary assistant work. About 98 are associate degrees, the credential BLS gives for veterinary technicians: St. Petersburg 50, Hillsborough 16, Miami Dade 12, Pensacola State 12, Eastern Florida State 8. St. Petersburg also awards 17 bachelor's. ⚠⚠ The national technician exam (VTNE) and Florida's voluntary Certified Veterinary Technician credential both require graduation from a programme accredited by the AVMA's CVTEA, so check the AVMA's current list. ⚠ Florida does not license veterinary technicians (ch. 474, F.S.); bills to do so died in 2025 and 2026. ⚠ This is not a pre-veterinary route: the DVM is a separate professional degree with its own science prerequisites.",
  "cips": [
    { "cipCode": "01.83", "note": "Veterinary/Animal Health Technologies — about 293 Florida public credentials a year, all under 01.8301. Roughly 98 associate degrees and 17 bachelor's (the veterinary technician route) and roughly 178 short certificates, mostly veterinary assisting at technical colleges. ⚠ Florida files this here, in agriculture; 51.0808 has no Florida rows." }
  ],
  "related": [
    { "slug": "biology", "note": "⚠ The usual undergraduate route to veterinary school, which veterinary technology is not. A student who wants to become a veterinarian needs a science degree's prerequisites, and technology courses are not designed to meet them.", "isRoute": False },
    { "slug": "medical-laboratory-science", "note": "⚠ The human-medicine counterpart of the veterinary clinical pathology work in this programme, with a state licence behind it in Florida, which veterinary technology does not have.", "isRoute": False },
    { "slug": "agricultural-business", "note": "⚠ The large-animal side: Florida's cattle and equine operations employ technicians too, and the animal-science and agribusiness programmes share the agricultural classification.", "isRoute": False }
  ]
}
io.open('programs/veterinary-technology.json', 'w', encoding='utf-8').write(json.dumps(program, ensure_ascii=False, indent=2))

courses = [
 ("ATE1001", "Introduction to Veterinary Technology — Eastern Florida State, FAMU and Hillsborough. The profession, its scope under supervision, and the path to the national exam. ⚠ Ask here whether the programme is AVMA CVTEA accredited, because the exam and the Florida CVT both require it.", None),
 ("ATE1741", "Veterinary Medical Terminology — FAMU, Hillsborough and St. Petersburg. The vocabulary of every chart, prescription and lab report.", None),
 ("ATE1110", "Animal Anatomy — five carriers, with its lab ATE1110L. The body systems of the species a Florida practice sees, from cats and dogs to horses and cattle.",
  "⚠ Take the lab ATE1110L alongside; the two are corequisites at the carriers."),
 ("ATE1211", "Animal Physiology — Eastern Florida State, Hillsborough, Miami Dade and St. Petersburg. How the systems work, which is what anaesthesia monitoring and emergency care depend on.", None),
 ("ATE2638", "Veterinary Clinical Pathology — five carriers, with lab ATE2638L. Blood work, urinalysis, parasitology and cytology, the laboratory half of the job.",
  "⚠ ATE2639/ATE2639L Animal Laboratory Procedures 2 continues the sequence at four carriers."),
 ("ATE2634", "Animal Pharmacology — Hillsborough, Pensacola State and St. Petersburg. ⚠⚠ Dosage calculation and drug handling. A technician prepares and gives medication a veterinarian has prescribed, and an error here is the most dangerous kind.",
  "⚠ The bachelor's level has ATE3615 Veterinary Pharmacology at FAMU and St. Petersburg."),
 ("ATE2631", "Small Animal Nursing I — Hillsborough, Miami Dade and St. Petersburg. Restraint, patient assessment, fluid therapy and nursing care. ⚠ Nearly nine in ten technicians work in veterinary services, and most of that is companion-animal practice.",
  "⚠ ATE2612 Small Animal Nursing 2 follows at Miami Dade and St. Petersburg."),
 ("ATE1652L", "Introduction to Anesthesia, Surgery and Dentistry — Eastern Florida State and Hillsborough. ⚠⚠ Anaesthesia monitoring and surgical assisting are the skills that most separate a credentialed technician from an assistant.",
  "⚠ FAMU and St. Petersburg teach ATE3658 Anesthesia and Surgical Nursing at the bachelor's level."),
 ("ATE2710", "Animal Emergency Medicine — five carriers. Triage, shock, trauma and critical care. ⚠ Emergency and specialty hospitals are where technician work is most intensive; ask employers there how they pay credentialed technicians."),
 ("ATE1636", "Large Animal Clinical and Nursing Skills — Eastern Florida State, Pensacola State and St. Petersburg. Horses and livestock. ⚠ Florida has large equine and cattle industries, and large-animal practice is part of the technician's training.",
  "⚠ ATE2661 Large Animal Diseases continues it at four carriers."),
 ("ATE1943", "Veterinary Work Practicum I — Eastern Florida State, Hillsborough and St. Petersburg, the first of four. ⚠⚠ Clinical hours in a working veterinary hospital. Ask how placements are arranged before enrolling, because the programme cannot be finished without them.",
  "⚠ ATE1944, ATE2945 and ATE2946 are practicums II to IV at the same three colleges."),
 ("ATE4317", "Introduction to Veterinary Hospital Management — Eastern Florida State, FAMU and St. Petersburg. ⚠ The bachelor's-level route to practice manager, with ATE3344 Supervision and ATE3316 Finance for the Veterinary Manager.", None),
 ("ATE0006", "Veterinary Assistants and Laboratory Animal Caretakers 1 — 450 clock hours, a completion point at seven institutions, most of them technical colleges. ⚠⚠ This is the ASSISTING route. It leads to veterinary assistant work (Florida median $37,830), not to veterinary technician, and it does not qualify anyone for the national technician exam.",
  "⚠ ATE0072 Veterinary Assistant (150 hours) is the next completion point, at the same seven institutions."),
]

sources = [
 ("BLS Occupational Outlook Handbook — Veterinary Technologists and Technicians", "https://www.bls.gov/ooh/healthcare/veterinary-technologists-and-technicians.htm",
  "$47,380 median (2025), 131,400 jobs, +9% for 2025–35, about 13,400 openings a year. Entry: associate degree (technicians), usually a bachelor's (technologists); most states require registration, licensure or certification; 89% in veterinary services. No mention of AI or automation."),
 ("O*NET — Veterinary Assistants and Laboratory Animal Caretakers (31-9096.00)", "https://www.onetonline.org/link/summary/31-9096.00",
  "78% of respondents report a high school diploma; much faster than average growth for 2024–34 and about 22,200 openings a year."),
 ("O*NET — Florida wages for 29-2056 and 31-9096", "https://www.onetonline.org/link/localwages/29-2056.00?st=FL",
  "Veterinary technicians: Florida median $46,380 against $47,380 national, $8,050 below at the 75th percentile. Veterinary assistants: Florida median $37,830."),
 ("s. 474.202, Florida Statutes — definitions", "https://www.flsenate.gov/Laws/Statutes/2025/474.202",
  "Defines responsible and immediate supervision of unlicensed personnel by a licensed veterinarian. It neither defines nor licenses veterinary technicians."),
 ("Florida Senate — SB 898 (2025) and SB 796 (2026), practice of veterinary medicine", "https://www.flsenate.gov/Session/Bill/2026/796",
  "Bills to require licensure or registration of veterinary technicians. SB 898 died in committee on 16 June 2025; SB 796 died on the calendar and its House companion HB 805 died in Rules on 13 March 2026."),
 ("Florida Veterinary Technician Association — certification", "https://thefvta.net/online-certification-application/",
  "The voluntary Florida CVT: graduation from an AVMA-accredited programme and the national examination; renewed every two years with 15 RACE-approved CE credits."),
 ("AVMA — veterinary technology programmes accredited by the CVTEA", "https://www.avma.org/education/center-for-veterinary-accreditation/veterinary-technology-programs-accredited-avma-cvtea",
  "The authoritative list of accredited programmes; check a programme's current status here before enrolling."),
 ("IPEDS completions — Florida, CIP 01.8301", "https://nces.ed.gov/ipeds/",
  "About 293 a year: associate degrees at St. Petersburg 50, Hillsborough 16, Miami Dade 12, Pensacola State 12, Eastern Florida State 8; 17 bachelor's at St. Petersburg; about 178 certificates of under a year, mostly at technical colleges."),
 ("SCNS statewide course file — ATE", "https://flscns.fldoe.org/",
  "ATE0006 (450 hours) and ATE0072 (150 hours) are occupational completion points of the veterinary assisting programme; every active undergraduate ATE course but one independent-study number is guaranteed transfer."),
]

path = {
  "slug": "veterinary-technician",
  "name": "Veterinary Technician",
  "cipCode": "01.83",
  "socCode": "29-2056",
  "additionalSocCodes": ["31-9096"],
  "isPublished": True,
  "sortOrder": 105,
  "description": "⚠⚠⚠ Two jobs share this field in Florida, and most of the state's certificates lead to the lower-paid one. Veterinary technicians need an associate degree from an AVMA-accredited programme (Florida median $46,380); veterinary assistants train on the job or in a short clock-hour certificate ($37,830). ⚠⚠ Florida does not license veterinary technicians, and bills to change that died in 2025 and 2026, so the accredited programme and the voluntary CVT are the credentials that count.",
  "credentialNote": "⚠⚠⚠ FLORIDA DOES NOT LICENSE VETERINARY TECHNICIANS. Chapter 474, F.S. defines no technician; everyone but the veterinarian works as unlicensed personnel under the veterinarian's responsible supervision (s. 474.202). Bills to create licensure or registration died in 2025 (SB 898) and 2026 (SB 796, HB 805). ⚠⚠ What exists is the voluntary Florida Certified Veterinary Technician (CVT): graduation from an AVMA CVTEA-accredited programme plus the national exam (VTNE), renewed every two years with 15 continuing-education credits. ⚠ Because the exam and the CVT both require an accredited programme, a veterinary ASSISTING certificate does not lead to either. Check the programme on the AVMA's accredited list before enrolling.",
  "cipCodes": [
    {"cipCode": "01.09", "note": "⚠ Animal Sciences — the university animal science degree (UF 155 a year, Santa Fe 23) covers livestock and companion-animal biology, and is a route into research-animal and large-animal work, though not into the technician credential itself."}
  ],
  "programs": [
    {"slug": "veterinary-technology", "note": "The programme. ⚠⚠ Read its note first: most Florida awards under this code are short veterinary ASSISTING certificates, not the technician degree."},
    {"slug": "biology", "note": "⚠ The route to veterinary SCHOOL, which this is not. A science degree's prerequisites lead to the DVM; technology courses do not.", "isRoute": False},
    {"slug": "medical-laboratory-science", "note": "⚠ The human-medicine counterpart of veterinary laboratory work, and licensed in Florida.", "isRoute": False}
  ],
  "courses": [],
  "sources": [{"label": t, "url": u, "note": n} for t, u, n in sources],
  "bodyHtml": body,
}

for i, row in enumerate(courses, start=1):
    cid, reason = row[0], row[1]
    vnote = row[2] if len(row) > 2 else None
    r = {"courseId": cid, "sortOrder": i, "reason": reason}
    if vnote:
        r["variantNote"] = vnote
    path["courses"].append(r)

io.open('career_paths/veterinary-technician.json', 'w', encoding='utf-8').write(json.dumps(path, ensure_ascii=False, indent=2))

print('prog desc', len(program['description']), 'degreesNote', len(program['degreesNote']))
for k in ("description", "credentialNote"):
    print(k, len(path[k]))
for c in path["courses"]:
    if len(c["reason"]) > 500 or len(c.get("variantNote", "")) > 1000:
        print("LONG", c["courseId"], len(c["reason"]))
for s in path["sources"]:
    if len(s["note"]) > 500: print("LONG SRC", s["label"])
print("body", len(body), "courses", len(path["courses"]))
