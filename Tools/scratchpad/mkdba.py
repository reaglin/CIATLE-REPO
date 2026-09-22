# -*- coding: utf-8 -*-
"""Assemble career_paths/database-administrator.json."""
import io, json

body = io.open('scratchpad/body_dba.html', encoding='utf-8').read()

courses = [
 ("COP2700", "Introduction to Database Management — NINE public carriers, the widest database course in Florida: Daytona State, Eastern Florida, Florida SouthWestern, Gulf Coast, Indian River, Lake-Sumter, Northwest Florida, Palm Beach State and USF. ⚠ Start here whatever degree you are in. It is the cheapest way to find out whether you actually like this work before you spend electives on it.",
  None),
 ("CGS1540", "Database Fundamentals — FIU, Hillsborough, Indian River, St Johns River and USF. The same entry point under a general-computing prefix. ⚠ Note the credit value moves: some carriers run it at 1 credit and others at 3, so check what you are registering for.",
  "⚠ A one-credit version is an orientation, not the introductory course. If yours is 1 credit, plan on COP2700 or an equivalent as well."),
 ("CTS2445", "SQL Programming — six carriers: Florida Gateway, Hillsborough, Miami Dade, State College of Florida, Santa Fe and Seminole State. ⚠⚠ SQL is the one skill in this whole field that transfers between every employer, every platform and both halves of the occupation. Learn it properly and separately from any one vendor.",
  "⚠ CTS2433 is the same subject at Miami Dade, Pensacola State, Polk State, State College of Florida, St Petersburg and Tallahassee State. Credits run 3 at some carriers and 4 at others."),
 ("CTS2441", "Oracle Database Administration I — Eastern Florida, Hillsborough, Miami Dade and Seminole State. The hands-on platform course: installation, storage, users, backup. ⚠ This is the fastest route in Florida to an actual paid database job, and it is the ADMINISTRATOR half — the one BLS projects at 0% growth. Take it for the job, then keep moving.",
  None),
 ("CTS2442", "Oracle Database Administration II — Hillsborough, Miami Dade, Polk State and Seminole State. Backup and recovery, performance, the things that get you called at 2am. ⚠⚠ Recovery is the skill employers actually test for in an interview, because it is the one that has consequences.",
  None),
 ("COP3703", "Database Concepts at upper division — EFSC, FAMU, St Johns River, Seminole State and UNF. The computer science treatment: the relational model, normalisation, query processing, transactions. ⚠⚠ This is the course that points at the ARCHITECT half of the occupation.",
  "⚠⚠⚠ SEVEN statewide numbers carry this subject: COP3703, COP4703, COP3710, COP4710 (computer science), ISM3212, ISM4212 (business) and CTS4408 (applied). No institution carries all of them and seven carry more than one — so they are genuinely different courses, not one course filed seven ways. Check which your programme names."),
 ("COP4710", "Database Design and Architecture — FIU, FSU, UCF, USF and UWF. ⚠⚠⚠ If you are aiming at database architect, this is the course: schema design, physical design, distribution, the decisions the job consists of. Take it even if your degree does not require it. The architect half pays a $139,500 median against administration's $104,620 and is projected at +9% against 0%.",
  "⚠ COP3710 is the same subject at FAMU, FGCU, Florida Polytechnic and Polk State — a 3000-level twin with no carrier overlap."),
 ("ISM4212", "Database Concepts and Administration — six carriers and the widest of the seven: Central Florida, FAU, FSU, State College of Florida, St Petersburg and USF. ⚠⚠ The BUSINESS-school treatment — data as something an organisation decides with rather than a system to be optimised. ⚠ Not a substitute for the computer science course, and better preparation than it for analytics and reporting work.",
  "⚠ ISM3212 is the 3000-level twin at FGCU, Florida Polytechnic, Indian River and Palm Beach State. FSU, FAU and USF carry an ISM number AND a COP number — evidence these are different courses for different students."),
 ("CTS4408", "Database Administration at upper division — FIU, Florida SouthWestern and Santa Fe. The applied-technology version of the upper course, and the closest match to what a working administrator does day to day.",
  None),
 ("CAP4770", "Data Mining — NINE public carriers, the widest upper-division course in this family: EFSC, FAU, FGCU, FIU, Florida Polytechnic, St Petersburg, UF, UNF and UWF. ⚠⚠ It is the bridge to the analytics side and it is unusually well distributed for a 4000-level course — most subjects at this level reach three or four institutions.",
  "⚠ CAP4767 (FGCU, Miami Dade, UNF) and CAP3770 (FAMU, Miami Dade, Polk State) are the same subject under two more numbers."),
 ("CAP4774", "Data Warehousing — Gulf Coast, Polk State and UWF. Dimensional modelling, ETL and the analytical store. ⚠ This is the named subject of Florida's only live database degree (UWF's master's, 11.0802), which tells you where the state thinks the specialism lives.",
  None),
 ("CIS4368", "Database Security and Audits — FAMU, FGCU, USF and UWF. ⚠⚠ Where database work meets the auditors, and a genuine differentiator: a database professional who can answer an auditor is paid differently from one who cannot. BLS names security explicitly in what it expects architects to be critical for.",
  None),
 ("CEN4083", "Introduction to Cloud Computing — FGCU, FIU, Florida Polytechnic, Santa Fe and UNF. ⚠⚠ Nearly every new database is somebody's managed service now, and the platform knowledge is no longer optional. Kubernetes is the single most-cited hot technology on the O*NET database administrator profile.",
  "⚠ CTS2145 Cloud Essentials (Florida Gateway, Indian River, Lake-Sumter, Northwest Florida, Seminole State) and CTS2375 Cloud Infrastructure and Services are the state-college entry points to the same material."),
 ("COP3530", "Data Structures — the course the design half assumes you have had. ⚠ Indexes, trees and hashing are not database trivia; they are why one query plan is a thousand times faster than another. ⚠⚠ If your degree is information systems rather than computer science you will probably not be required to take this. Take it anyway if you are aiming at architect.",
  None),
 ("STA2023", "Elementary Statistics — the most widely carried statistics course in Florida. ⚠ Named because the data-mining and warehousing courses assume it, and because the boundary between this path and data science is largely a statistics boundary. It is also a general-education course at most institutions, so it costs you nothing to have.",
  None),
]

sources = [
 ("BLS Occupational Outlook Handbook — Database Administrators and Architects", "https://www.bls.gov/ooh/computer-and-information-technology/database-administrators.htm",
  "The split this page is built on: administrators $104,620 and 0% growth, architects $139,500 and +9% with 6,500 new jobs; 144,500 jobs combined and about 7,300 annual openings. Source of the quoted sentence naming AI adoption as the reason architects will be critical."),
 ("O*NET — Database Administrators (15-1242.00)", "https://www.onetonline.org/link/summary/15-1242.00",
  "78,000 employed, 3,800 annual openings, outlook recorded as Decline (-1% or lower) for 2024-34. Education: 89% bachelor's, 4% post-baccalaureate certificate, 3% associate. Job Zone Four. Kubernetes, MongoDB, Oracle PL/SQL, MySQL and Snowflake lead the hot-technology list."),
 ("O*NET — Database Architects (15-1243.00)", "https://www.onetonline.org/link/summary/15-1243.00",
  "66,900 employed, 4,000 annual openings, outlook Much faster than average (7% or higher) for 2024-34. Education: 76% bachelor's and 14% MASTER'S — the graduate figure that does not appear on the administrator side. Job Zone Four."),
 ("O*NET — Database Administrators, Florida wages", "https://www.onetonline.org/link/localwages/15-1242.00?st=FL",
  "Florida essentially at national parity: median $104,120 against $104,620, and the 75th percentile ABOVE national at $136,240 against $135,460."),
 ("O*NET — Database Architects, Florida wages", "https://www.onetonline.org/link/localwages/15-1243.00?st=FL",
  "Florida median $138,320 against $139,500 national, and the 90th percentile $206,410 against $204,000 — above the national figure, which is rare in the Florida wage data this site has measured."),
 ("SCNS statewide course file — carrier counts for the database prefixes", "https://flscns.fldoe.org/",
  "Source of the seven-number measurement: COP3703 5 carriers, COP4703 3, COP3710 4, COP4710 5, ISM3212 4, ISM4212 6, CTS4408 3 — 21 institutions in total, with FIU and USF each carrying three of the seven."),
 ("IPEDS completions — Florida, CIP 11.0802", "https://nces.ed.gov/ipeds/",
  "Data Modeling/Warehousing and Database Administration: 62 credentials at 5 Florida public institutions, of which UWF's master's is 61. Daytona State, Miami Dade and Florida Polytechnic record programmes that awarded nothing in the year measured."),
]

path = {
  "slug": "database-administrator",
  "name": "Database Administrator and Database Architect",
  "cipCode": "11.08",
  "socCode": "15-1242",
  "isPublished": True,
  "sortOrder": 136,
  "description": "⚠⚠⚠ One job title and two occupations, moving in opposite directions. Database ADMINISTRATORS earn a $104,620 median and are projected at 0% growth over 2025-35; database ARCHITECTS earn $139,500 and are projected at +9% — with FEWER people and MORE annual openings. ⚠⚠ And Florida has no undergraduate database degree at all: the dedicated code produces 62 credentials a year and 61 are one UWF master's. So the specialism is assembled from courses, under seven competing statewide numbers in three different colleges.",
  "credentialNote": "⚠⚠ NO LICENCE, NO ACCREDITED PROGRAMME, AND NO DEGREE IN THE SUBJECT. Nothing in Florida law regulates database work, and there is no accreditor standing between you and the job — which is genuinely good news, and it means the burden of choosing coursework falls entirely on you. ⚠ O*NET puts both halves in JOB ZONE FOUR: a four-year degree plus several years of experience. Neither is an entry-level role, so plan the first job as an on-ramp — support, development, reporting or analysis — and expect to arrive here after a few years. ⚠⚠ Reported education differs between the halves and it is the actionable difference: administrators 89% bachelor's with no master's figure recorded, architects 76% bachelor's and 14% MASTER'S. Graduate study shows up on the design side. ⚠⚠⚠ What substitutes for a credential here is demonstrable platform work plus SQL, and vendor certification is the currency — Florida's state colleges teach the Oracle and SQL Server certificate tier at four to six institutions each, and those courses are directly hireable.",
  "cipCodes": [
    {"cipCode": "11.07", "note": "⚠⚠ Computer Science — named because this is where the DESIGN courses live. COP3710 and COP4710 Database Design/Architecture are computer science numbers at nine institutions between them, and the architect half of the occupation is the one paying $139,500 and growing at 9%. 16 Florida institutions award computer science against one live database programme."},
    {"cipCode": "52.12", "note": "⚠ Management Information Systems — the business-school route, and a real one rather than a consolation. ISM3212 and ISM4212 carry the same subject at ten Florida institutions, taught as data an organisation decides with. ⚠⚠ FSU, FAU and USF each carry BOTH an ISM number and a COP number, which is the evidence they are different courses for different students."},
    {"cipCode": "11.10", "note": "⚠ Computer/Information Systems Security and Networking — named for the overlap that actually pays: CIS4368 Database Security and Audits runs at FAMU, FGCU, USF and UWF, and BLS names security among the things it expects database architects to be critical for."}
  ],
  "programs": [
    {"slug": "database-and-data-management", "note": "The programme, such as it is — and the note there explains why 'such as it is' is the honest phrasing: 62 credentials a year at five institutions, 61 of them one UWF master's."},
    {"slug": "computer-science", "note": "⚠⚠ The route to the better-paid half. The design courses sit in this college, and the architect role reports 14% master's against the administrator role's none — so this is also the degree that leads somewhere afterwards."},
    {"slug": "information-technology", "note": "⚠ The widest route — 39 Florida institutions — and the one the Oracle and SQL Server certificate tier attaches to. Fastest way into a database job; slowest way to the growing half. Enter here, aim past it."},
    {"slug": "management-information-systems", "note": "⚠⚠ The third route and the one students overlook: the same subject from the business side, at ten Florida institutions, and the better preparation for analytics, reporting and governance work."},
    {"slug": "data-science", "note": "⚠ The adjacent destination rather than a route in. A data scientist builds models from the data; an architect builds what the data lives in. They share SQL, mining and warehousing, and diverge on statistics.", "isRoute": False},
    {"slug": "cybersecurity", "note": "⚠ Named for the same reason as the CIS4368 course row — database security and audit is a genuine specialism, and it is where the two fields meet in Florida's course catalogue.", "isRoute": False}
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

io.open('career_paths/database-administrator.json', 'w', encoding='utf-8').write(
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
print("body", len(body), "courses", len(path["courses"]))
