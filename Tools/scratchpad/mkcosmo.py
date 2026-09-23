# -*- coding: utf-8 -*-
"""Assemble the cosmetology and barbering programme and the cosmetologist career path.

Row 147 of QUEUE.csv (2026-09-23), unblocked by the CIP-seed widening that added 12.04.
Barbers, manicurists and skincare specialists are covered as sections (additionalSocCodes).
"""
import io, json

body = io.open('scratchpad/body_cosmo.html', encoding='utf-8').read()

program = {
  "slug": "cosmetology-and-barbering",
  "name": "Cosmetology, Barbering, Nails and Skin Care",
  "isPublished": True,
  "sortOrder": 650,
  "description": "The licensed personal-appearance trades: cosmetology, barbering, nail care and skin care, taught in Florida as clock-hour certificates whose length is set by statute. About 3,146 certificates a year at 44 public institutions, most of them technical colleges. There is no degree in this family.",
  "degreesNote": "⚠⚠ Every award here is a certificate. Cosmetology (12.0401) is 1,212 a year at 42 institutions, led by Daytona State 86, Sheridan Technical 74 and Palm Beach State 64. Facial treatment and skin care (12.0408) is 1,256 short certificates at 24, and nail technician (12.0410) 456 at 20. ⚠⚠ Barbering (12.0402) is only 208 at 17, although an employed Florida barber's median wage ($49,410) is well above an employed hairdresser's ($29,530). ⚠⚠⚠ The hours are set in law: 1,200 for a cosmetologist licence (s. 477.019, F.S.), 900 for a barber licence (s. 476.114), and 180, 220 or 400 for the nail, facial or combined specialty registrations (s. 477.0201). The state's barbering programme runs 1,200 hours, 300 more than the statute requires, and its nail and facial courses also exceed the minimums. Ask each school which licence each completion point prepares you for, and when you can sit the exam. ⚠ Barbering has its own board and licence under chapter 476; a cosmetology licence does not make you a barber.",
  "cips": [
    { "cipCode": "12.04", "note": "Cosmetology and Related Personal Grooming Services — 3,146 Florida public certificates a year at 44 institutions: cosmetology (12.0401) 1,212 at 42, facial/skin care (12.0408) 1,256 at 24, nail technician (12.0410) 456 at 20, barbering (12.0402) 208 at 17, esthetician (12.0409) 14 at 3." }
  ],
  "related": [
    { "slug": "entrepreneurship", "note": "⚠⚠ BLS reports 80% of barbers and 48% of hairdressers are self-employed, so most people in this trade run a small business: renting a chair or booth, pricing, booking and taxes. The licence teaches the craft; the entrepreneurship courses teach the business.", "isRoute": False },
    { "slug": "business-administration", "note": "⚠ For the salon owner or manager. Most of the trade is self-employed, and the step from working a chair to running a shop is a business step.", "isRoute": False }
  ]
}
io.open('programs/cosmetology-and-barbering.json', 'w', encoding='utf-8').write(json.dumps(program, ensure_ascii=False, indent=2))

courses = [
 ("CSP0009", "Grooming and Salon Services Core, Facials and Nails — 225 hours at 32 public institutions, the shared start of Florida's cosmetology programme. Sanitation, safety, Florida law and rules, and the basics of facials and nails.", None),
 ("COS0002", "Cosmetologist and Hairstylist 1 (1 of 3) — 300 hours at 31 institutions. Cutting, styling, shampooing and the chemistry of hair.", None),
 ("COS0003", "Cosmetologist and Hairstylist 2 (2 of 3) — 300 hours. Colour, permanent waving and chemical relaxing, the services where chemistry and client safety meet.", None),
 ("COS0009", "Cosmetologist and Hairstylist 3 (3 of 3) — 375 hours at 32 institutions. ⚠⚠ It completes the 1,200 hours s. 477.019, F.S. requires for the cosmetologist licence exam. The three hairstylist courses are parts of one course, so the licence comes at the end rather than at intermediate exits.",
  "⚠ Several state colleges package the same hours differently: Daytona State, Eastern Florida and South Florida State as COS0080L–COS0084L salon labs, FSCJ as phases COS0001/COS0007/COS0008 with labs, Indian River and Pensacola State as COS0010 and COS0088. Register by the hours and the licence the sequence leads to."),
 ("COS0150", "Restricted Barber 1 (1 of 3) — 333 hours at 10 institutions, the start of the barbering programme. ⚠⚠ Barbering is a separate licence under chapter 476, F.S., with its own board: a cosmetology licence does not cover barbering.", None),
 ("COS0151", "Restricted Barber 2 (2 of 3) — 333 hours.", None),
 ("COS0152", "Restricted Barber 3 (3 of 3) — 334 hours; with parts 1 and 2 it makes the 1,000-hour completion point A. ⚠⚠ The 2025 statute requires 900 hours for a barber licence and defines no \"restricted barber\" licence, so ask the school what this point qualifies you for.", None),
 ("COS0671", "Barber — completion point B, a further 200 hours at 9 institutions, bringing the programme to 1,200 hours. ⚠ That is 300 hours beyond the statutory minimum (s. 476.114); ask what the extra hours add, and whether you can sit the exam earlier (the statute allows it after 600 school hours).", None),
 ("CSP0015", "Manicurist and Pedicurist — completion point A, 240 hours at 17 institutions. ⚠ The statutory minimum for the manicuring and pedicuring registration is 180 hours (s. 477.0201), and the statute names no exam for it.",
  "⚠ Some state colleges use their own numbers for the same subject: CSP0015C at Pensacola State, CSP0013/CSP0013C at Palm Beach State and Florida Gateway, CSP0016 at Pinellas Technical."),
 ("CSP0265", "Facials/Skin Care Specialist — completion point B, 260 hours at 14 institutions. ⚠ The statutory minimum for the facial specialty is 220 hours. ⚠ BLS: offices of physicians employ 6% of skincare specialists and pay the highest median hourly wage of any setting it lists, $24.81.",
  "⚠ FSCJ and Pinellas Technical carry CSP0266 Facials Specialist; Eastern Florida and Pensacola State CSP0266C."),
 ("CSP0105", "Advanced Skin Care 1 — 150 hours at three technical colleges (Manatee Technical, Orange Technical, Suncoast Technical). Beyond the specialty registration: advanced treatments, and a step toward the physicians' offices BLS lists as the best-paid setting for skincare specialists.", None),
 ("CSP0106", "Advanced Skin Care 2 — 150 hours, the second half of the advanced sequence.", None),
 ("CSP0505", "Ethical Business Practices — four carriers. ⚠⚠ With 80% of barbers and 48% of hairdressers self-employed (BLS), pricing, booth rental, records and taxes are part of the job, and this course addresses them.", None),
]

sources = [
 ("BLS Occupational Outlook Handbook — Barbers, Hairstylists, and Cosmetologists", "https://www.bls.gov/ooh/personal-care-and-service/barbers-hairstylists-and-cosmetologists.htm",
  "Median $18.37 an hour for barbers and $17.21 for hairdressers (2025); 670,800 jobs, +7% for 2025–35, about 80,300 openings a year; 80% of barbers and 48% of hairdressers self-employed; wage data exclude the self-employed and include tips; all states require a licence. No mention of automation or AI."),
 ("BLS Occupational Outlook Handbook — Manicurists and Pedicurists", "https://www.bls.gov/ooh/personal-care-and-service/manicurists-and-pedicurists.htm",
  "$35,760 median (2025), 201,800 jobs, +9%, about 21,900 openings a year, 23% self-employed; postsecondary nondegree award."),
 ("BLS Occupational Outlook Handbook — Skincare Specialists", "https://www.bls.gov/ooh/personal-care-and-service/skincare-specialists.htm",
  "$45,330 median (2025), 104,200 jobs, +9%, about 14,200 openings a year, 29% self-employed; offices of physicians employ 6% at a $24.81 median hourly wage."),
 ("O*NET — Florida wages for 39-5012, 39-5011, 39-5092 and 39-5094", "https://www.onetonline.org/link/localwages/39-5012.00?st=FL",
  "Florida medians: hairdressers $29,530 (US $35,790), barbers $49,410 (US $38,210), manicurists $37,840, skincare specialists $43,880. Employees only."),
 ("s. 477.019, Florida Statutes — cosmetologists", "https://www.flsenate.gov/Laws/Statutes/2025/477.019",
  "A minimum of 1,200 hours of training and a passing grade on the examination; age 16 or a high school diploma; up to 10 hours of continuing education every two years."),
 ("s. 477.0201, Florida Statutes — specialty registration", "https://www.flsenate.gov/Laws/Statutes/2025/477.0201",
  "180 hours for manicuring and pedicuring, 220 for facials, 400 for all three, focused primarily on sanitation and safety."),
 ("s. 476.114, Florida Statutes — barbers", "https://www.flsenate.gov/Laws/Statutes/2025/476.114",
  "A minimum of 900 hours of training; the examination may be taken after 600 school hours. Chapter 476 is a separate board and licence from cosmetology."),
 ("SCNS statewide course file — COS and CSP", "https://flscns.fldoe.org/",
  "Cosmetology: CSP0009 225 hours plus COS0002/0003/0009 at 300, 300 and 375. Barbering: COS0150–0152 (333/333/334, completion point A) and COS0671 (200, point B). Specialties: CSP0015 240 hours (A), CSP0265 260 hours (B)."),
 ("IPEDS completions — Florida, CIP 12.04", "https://nces.ed.gov/ipeds/",
  "3,146 certificates at 44 institutions: cosmetology 1,212, facial/skin care 1,256, nail technician 456, barbering 208, esthetician 14."),
]

path = {
  "slug": "cosmetologist",
  "name": "Cosmetologist, Barber, Nail and Skin Care Specialist",
  "cipCode": "12.04",
  "socCode": "39-5012",
  "additionalSocCodes": ["39-5011", "39-5092", "39-5094"],
  "isPublished": True,
  "sortOrder": 147,
  "description": "⚠⚠ A licensed trade: Florida law sets the training hours, 1,200 for a cosmetologist and 900 for a barber, and both licences need an exam. ⚠⚠⚠ Most people in it work for themselves (BLS: 80% of barbers, 48% of hairdressers), and the wage figures leave them out. Among employees, a Florida hairdresser's median is $29,530 and a barber's $49,410, yet Florida trains six cosmetologists for every barber. This page compares the four licences and what the programmes actually run.",
  "credentialNote": "⚠⚠⚠ LICENSED IN FLORIDA, AND TWO SEPARATE BOARDS. Cosmetologist: 1,200 hours and a passing examination, age 16 or a high school diploma (s. 477.019, F.S.). Barber: a separate licence under chapter 476, 900 hours, with the exam allowed after 600 school hours (s. 476.114). A cosmetology licence does not cover barbering. Nail and facial work need a specialty registration: 180 hours for manicuring and pedicuring, 220 for facials, 400 for all three (s. 477.0201); the statute names no exam for it. ⚠⚠ Florida's barbering programme runs 1,200 hours, 300 more than the statute requires, and its first 1,000-hour point is titled Restricted Barber, a licence the 2025 statute does not define. Ask the school what each completion point qualifies you for before you enrol.",
  "cipCodes": [
    {"cipCode": "52.02", "note": "⚠ Business Administration — named because BLS reports most barbers (80%) and nearly half of hairdressers (48%) are self-employed. The step from working a chair to running a shop is a business step, not more cosmetology."}
  ],
  "programs": [
    {"slug": "cosmetology-and-barbering", "note": "The programme. Read its note first: the hours are set in statute, and the barbering programme runs longer than the law requires."},
    {"slug": "entrepreneurship", "note": "⚠⚠ For the self-employed majority: booth rental, pricing, bookings and taxes.", "isRoute": False},
    {"slug": "business-administration", "note": "⚠ For the salon owner or manager.", "isRoute": False}
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

io.open('career_paths/cosmetologist.json', 'w', encoding='utf-8').write(json.dumps(path, ensure_ascii=False, indent=2))

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
