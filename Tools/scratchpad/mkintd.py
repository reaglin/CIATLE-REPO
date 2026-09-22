# -*- coding: utf-8 -*-
"""Assemble career_paths/interior-designer.json."""
import io, json

body = io.open('scratchpad/body_intd.html', encoding='utf-8').read()

courses = [
 ("IND1020", "Introduction to Interior Design — the first course, at Indian River State, Miami Dade and UF. Space, proportion, colour, light and the vocabulary of the field. Take it early: it is the course that tells you whether you actually want the work rather than the idea of it.",
  "⚠⚠ FSCJ and Hillsborough carry the SAME statewide subject as ARC-style integrated IND1020C, and no institution carries both. Identical statewide title, two identifiers — name both when you transfer."),
 ("IND1020C", "The same introductory course under the integrated identifier FSCJ and Hillsborough use. Listed separately because no institution carries both forms, so a student will only ever find one of them.",
  "⚠ Integrated lecture-and-studio packaging. Florida articulation treats it as equivalent to the bare IND1020; the cost is identifier matching, not content."),
 ("IND1233C", "Design Studio I — Palm Beach State and Seminole State. The first real studio: a brief, a plan, a critique. ⚠ Studio work is where your portfolio comes from, and the portfolio is what gets you the internship that starts your NCIDQ hours.",
  None),
 ("IND2100", "History of Interiors I — Indian River State, Palm Beach State and UF. Not decoration trivia: it is the shared reference every client conversation and every design rationale draws on.",
  "⚠⚠ The SAME statewide title sits on IND1100 at FSCJ, Miami Dade and Seminole State, with NO institution carrying both. One subject, two numbers, one name — an automated transfer match finds nothing."),
 ("IND2130", "History of Interiors II — Palm Beach State, Seminole State and UF. The modern period, which is where a working designer's actual vocabulary comes from.",
  "⚠ Its twin is IND1130 at FSCJ and Miami Dade. Same split as the first history course."),
 ("IND1420", "Materials and Sources — FSCJ, Hillsborough and Indian River State. What things are made of, how they wear, what they cost and where they come from. ⚠ Specification is the part of the job that gets audited, and it is where an inexperienced designer loses money.",
  "⚠⚠ IND2420 Materials and Methods for Interior Architecture is the same statewide subject at FIU and Palm Beach State — again with no overlap. IND1423 Survey of Materials and Resources is a third variant at Indian River and Seminole State."),
 ("IND1429", "Textiles for Commercial and Residential Interiors — Daytona State and Indian River State. ⚠ More consequential than it sounds on the commercial side: flammability, abrasion ratings and cleanability are specification decisions with code and liability behind them, not taste.",
  None),
 ("IND2307C", "Visual Communications — FSCJ, Palm Beach State and Seminole State. Hand drawing, rendering and presentation. ⚠ The skill that survives the software changing, and the one a client actually watches you use in a meeting.",
  None),
 ("IND2460C", "Interior Design Computer-Aided Drafting and Design — FSCJ, Palm Beach State and UF. ⚠⚠ BLS says most interior designers use CAD for most of their drawings, so this is not an elective skill. Find out whether the course teaches AutoCAD, Revit or both, and learn Revit somewhere if it does not.",
  None),
 ("IND2461", "Building Systems — Palm Beach State and Seminole State. ⚠⚠⚠ This is the course that teaches the boundary in s. 481.2131: mechanical, plumbing, HVAC, electrical and vertical transport are OUTSIDE what a registered interior designer may seal. You have to coordinate with them without signing for them.",
  None),
 ("IND1935", "Building and Barrier-Free Codes — five public carriers, the joint-widest course in the prefix. Accessibility, egress and the Florida Building Code. ⚠⚠⚠ On the nonresidential side this is the most directly employable course on this list: code knowledge is what separates a decorator from a designer an architect will hire.",
  "⚠ It carries a 9xx statewide number, which is normally the special-topics range, but it has a settled specific title at five institutions and is a real course. Register by number."),
 ("IND2500", "Professional Principles and Practices — five public carriers, tied for the widest in the prefix. Contracts, scope, fees and business practice. ⚠⚠ Section 481.2131 makes this legally loaded: you must disclose how ALL compensation is paid, including markups, and may not take supplier compensation without the client's knowledge. 26% of interior designers are self-employed and will need every hour of this.",
  None),
 ("IND2608", "Sustainable Design — Indian River State, Miami Dade, Palm Beach State and Seminole State. Materials, indoor air quality, daylight and the certification systems clients now ask about by name.",
  None),
 ("IND2210", "Interior Design 3 — Daytona State, Indian River State and Miami Dade. The upper studio in the associate sequence, and usually where a commercial project first appears in the brief. ⚠ Treat the output as portfolio, not coursework.",
  None),
 ("IND2941", "Interior Design Internship — Indian River State, Palm Beach State and Seminole State. ⚠⚠⚠ The single highest-leverage course on this page. CIDQ allows up to 1,760 hours of interior design work experience EARNED BEFORE GRADUATION to count toward the NCIDQ requirement — half the bachelor's total. ⚠ Take it, and make sure the supervision and the record-keeping are set up so the hours will actually count.",
  "⚠ Confirm with your institution and with CIDQ what documentation is required BEFORE the placement starts. Hours that were not recorded properly at the time are very hard to reconstruct."),
]

sources = [
 ("Florida Statutes s. 481.229 — exceptions and exemptions from licensure", "http://www.leg.state.fl.us/Statutes/index.cfm?App_mode=Display_Statute&Search_String=&URL=0400-0499/0481/Sections/0481.229.html",
  "Subsection (6)(a) exempts interior design and interior decorator services for ANY residential application, listing single-family homes, multifamily, townhouses, apartments and condominiums. (6)(b) exempts retail employees. (5)(a) lets a registered architect do interior design and use the title."),
 ("Florida Statutes s. 481.2131 — interior design practice and compensation", "http://www.leg.state.fl.us/Statutes/index.cfm?App_mode=Display_Statute&Search_String=&URL=0400-0499/0481/Sections/0481.2131.html",
  "Sets what a registered interior designer may seal and what is excluded — structural, mechanical, plumbing, HVAC, electrical, vertical transport, and life-safety elements. Also the compensation-disclosure duty and the bar on undisclosed supplier compensation."),
 ("Florida Statutes s. 481.209 — examinations", "http://www.leg.state.fl.us/Statutes/index.cfm?App_mode=Display_Statute&Search_String=&URL=0400-0499/0481/Sections/0481.209.html",
  "Requires an interior design applicant to show written proof of passing the qualification examination prescribed by the Council for Interior Design Qualification, or an equivalent the department accepts."),
 ("CIDQ — NCIDQ examination eligibility", "https://www.cidq.org/for-exam-candidates/eligibility/",
  "The eligibility table quoted on this page: 3,520 hours for a bachelor's or master's in interior design, 5,280 for an associate, certificate or diploma or for a NAAB architecture degree, 7,040 otherwise; 60 semester (90 quarter) interior design credit hours; up to 1,760 pre-graduation hours may count."),
 ("BLS Occupational Outlook Handbook — Interior Designers", "https://www.bls.gov/ooh/arts-and-design/interior-designers.htm",
  "$67,190 median, 97,100 jobs, +3% for 2025-35, about 7,700 annual openings, 26% self-employed. Discusses CAD and BIM and makes no AI claim about employment — the contrast with the graphic design page is drawn on this page."),
 ("O*NET — Interior Designers (27-1025.00), Florida wages", "https://www.onetonline.org/link/localwages/27-1025.00?st=FL",
  "Florida against national at every percentile: $2,370 below at the 10th and $17,210 below at the 90th."),
 ("CIDA — Council for Interior Design Accreditation", "https://accredit-id.org/",
  "The accreditor. Florida public programmes accredited as of 2026: UF (Bachelor of Design, since 1974), Florida State (B.S.), Seminole State College (B.A.S.), Florida International (Master of Interior Architecture)."),
 ("University of Florida — Interior Design accreditation", "https://dcp.ufl.edu/interior/accreditation/",
  "Names the Bachelor of Design as the accredited degree and states the programme has been accredited since 1974, among the first to receive it."),
 ("Seminole State College — Interior Design B.A.S. earns CIDA accreditation", "https://www.seminolestate.edu/newsroom/article/5961/seminole-state-s-interior-design-program-earns-cida-accreditation",
  "The source for the claim that Seminole State is the only CIDA-accredited state college in Florida. Its B.A.S. is the accredited degree; its certificates and associate degrees are not the same credential."),
 ("FIU — CIDA accreditation, Department of Interior Architecture", "https://carta.fiu.edu/interiors/academics/cida-accreditation/",
  "Confirms the Master of Interior Architecture is CIDA-accredited — the programme that is invisible under the interior design CIP code because FIU's degrees are counted in the architecture family."),
]

path = {
  "slug": "interior-designer",
  "name": "Interior Designer",
  "cipCode": "50.04",
  "socCode": "27-1025",
  "isPublished": True,
  "sortOrder": 135,
  "description": "Interior designers plan the inside of buildings — space, light, materials, furniture and the codes that govern all of it. ⚠⚠⚠ The decision this page exists to answer is not which major but WHICH MARKET: in Florida ALL RESIDENTIAL work is exempt from registration by statute, while nonresidential work runs through a 60-credit education floor, up to 5,280 supervised hours and a national exam. ⚠⚠ And the credential LEVEL is worth a year — an associate or certificate needs three years of work experience where a bachelor's needs two, for the identical exam.",
  "credentialNote": "⚠⚠⚠ RESIDENTIAL WORK NEEDS NO CREDENTIAL IN FLORIDA. s. 481.229(6)(a) exempts interior design services for any residential application — houses, townhouses, apartments and condominiums alike. Registration exists for NONRESIDENTIAL work and for the protected title. ⚠⚠ The route: 60 semester hours of interior design credit, then supervised experience, then the NCIDQ examination (s. 481.209). The hours depend on your DEGREE LEVEL, not on accreditation — 3,520 (two years) for a bachelor's or master's in interior design, CIDA-accredited or not; ⚠ 5,280 (THREE years) for an associate degree, certificate or diploma, and the same for an NAAB architecture degree; 7,040 for a non-accredited architecture degree. ⚠ What CIDA accreditation does is satisfy the 60-credit requirement automatically. ⚠⚠⚠ Up to 1,760 hours earned BEFORE graduation may count — half a bachelor's requirement — so start logging supervised work as a student. ⚠ And know the limit of the seal: s. 481.2131 excludes structural, mechanical, plumbing, HVAC, electrical and vertical-transport systems and every life-safety element.",
  "cipCodes": [
    {"cipCode": "04.09", "note": "⚠⚠⚠ Architectural Sciences and Technology — claimed because FIU's CIDA-ACCREDITED Master of Interior Architecture is filed HERE, not under Interior Design. FIU awards nothing at all under 50.0408 despite running a Department of Interior Architecture, so a list built from the obvious code omits one of Florida's four accredited public programmes. ⚠ An NAAB architecture degree is also an NCIDQ education route, at 5,280 hours."}
  ],
  "programs": [
    {"slug": "interior-design", "note": "The programme itself — 9 Florida public institutions, and the note there sets out which specific DEGREES are CIDA-accredited, because the college is not the credential."},
    {"slug": "architecture", "note": "⚠⚠ A genuine route, not a neighbour: an NAAB-accredited architecture degree qualifies you for the NCIDQ exam at 5,280 hours, and a registered architect may perform interior design and use the title with no separate registration at all (s. 481.229(5)(a))."},
    {"slug": "graphic-and-digital-design", "note": "⚠ Named because students weigh these against each other and the federal projections diverge sharply — graphic design −2% with AI named as a cause, interior design +3% with no AI claim made. Shared studio training, different exposure.", "isRoute": False},
    {"slug": "construction-management", "note": "⚠ Named because the seal boundary in s. 481.2131 is a coordination problem on every real fit-out, and because construction management is offered at 30 Florida institutions against interior design's 9.", "isRoute": False}
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

io.open('career_paths/interior-designer.json', 'w', encoding='utf-8').write(
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
