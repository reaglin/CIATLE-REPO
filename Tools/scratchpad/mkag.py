# -*- coding: utf-8 -*-
"""Assemble the agricultural business programme and the agricultural manager career path."""
import io, json

body = io.open('scratchpad/body_ag.html', encoding='utf-8').read()

program = {
  "slug": "agricultural-business",
  "name": "Agricultural Business and Food and Resource Economics",
  "isPublished": True,
  "sortOrder": 610,
  "description": "Running the business side of farming, ranching and the food system: agricultural economics, marketing, finance, commodity risk and farm management. ⚠⚠ A small degree in Florida — about 150 credentials a year, two-thirds of them at the University of Florida — and a business degree with an agricultural subject, which leads to lending, insurance, food companies and hired farm management as often as to a farm.",
  "degreesNote": "⚠⚠ UF's Food and Resource Economics (01.0103) is the degree in Florida: 88 bachelor's and 11 master's a year, with specialisations in agribusiness marketing and management and in international food and resource economics. FAMU adds 10 agribusiness bachelor's (01.0102) and 29 in general agricultural sciences (01.0000). ⚠ College of Central Florida (6) and Florida Gateway (5) award the associate degree in agricultural business (01.0101). ⚠⚠⚠ THIS PROGRAMME IS THE SMALL END OF FLORIDA AGRICULTURE. The production degrees around it are four times its size and this site cannot list them yet: horticulture and landscape (01.06) 204 a year at ten state and technical colleges, Valencia 127; animal sciences (01.09) 178, UF 155 and Santa Fe 23; plant sciences (01.11) 134 at UF; equine studies (01.05) 67 at Central Florida; soil science (01.12) 56 at UF; production operations (01.03) 18 at four state colleges. ⚠ Choose the production field by the operation you want to run — ranch, grove, nursery — and take the business courses as the common ground. ⚠⚠ The transfer route to UF runs through general courses every college teaches: the state-assigned common prerequisites are MAC2233, STA2023, ACG2021 and ECO2013. ⚠ FGCU teaches agribusiness courses but recorded no agriculture degree in 2023.",
  "cips": [
    { "cipCode": "01.01", "note": "Agricultural Business and Management — 120 credentials a year at four Florida public institutions. ⚠⚠ UF 99 (Food and Resource Economics, 01.0103, bachelor's and master's), FAMU 10 (Agribusiness, 01.0102), and the associate degree at College of Central Florida (6) and Florida Gateway (5) under 01.0101." },
    { "cipCode": "01.00", "note": "Agriculture, General — FAMU's Agricultural Sciences, 29 a year at bachelor's and master's, plus one associate at Indian River. ⚠ Claimed because FAMU's agribusiness students are split between this code and 01.0102, and a reader looking for FAMU's agriculture programme would otherwise miss it." }
  ],
  "related": [
    { "slug": "business-administration", "note": "⚠⚠ The broader and far more portable version of the same training. BLS lists business alongside agriculture as a degree field for farm managers, and 45 Florida institutions award business against a handful awarding agribusiness. ⚠ The agribusiness degree adds commodity markets, agricultural finance and farm law, which a general business degree will not teach." },
    { "slug": "entrepreneurship", "note": "⚠ Two-thirds of farmers are self-employed, so a farm is a small business before it is anything else — and the entrepreneurship courses cover the part agricultural programmes treat lightly: starting one from nothing.", "isRoute": False },
    { "slug": "environmental-science", "note": "⚠ The land-stewardship neighbour. Soil, water and natural-resource management are daily farm decisions in Florida, and the forestry and wildlife programmes at UF sit in the same family.", "isRoute": False },
    { "slug": "logistics-and-supply-chain", "note": "⚠ Where a food and resource economics graduate often ends up: moving perishable product from field to shelf. The marketing and finance courses are the shared ground.", "isRoute": False }
  ]
}
io.open('programs/agricultural-business.json', 'w', encoding='utf-8').write(json.dumps(program, ensure_ascii=False, indent=2))

courses = [
 ("ECO2023", "Microeconomics — 39 carriers. ⚠⚠ Agricultural economics IS applied microeconomics: supply, price, cost of production and what a farm should grow. Every AEB course after it assumes it.", None),
 ("ACG2021", "Financial Accounting — 32 carriers, and a state-assigned common prerequisite for UF's Food and Resource Economics degree. ⚠⚠ Two-thirds of this occupation run their own business, and a farm that cannot read its own balance sheet cannot borrow.", None),
 ("STA2023", "Elementary Statistics — 39 carriers and a common prerequisite. ⚠ Yield trials, price series and risk are statistics; so is every claim a seed or chemical salesperson makes.", None),
 ("ECO2013", "Macroeconomics — 38 carriers and the fourth common prerequisite. ⚠ Interest rates, exchange rates and trade policy set the price of what a Florida grower sells and the cost of the loan that planted it.", None),
 ("AEB2104", "Economics of Agriculture — Central Florida, FAMU and FGCU. The introduction to agricultural markets, farm prices and policy, and flagged as a common prerequisite in the statewide file.",
  "⚠⚠ UF teaches this introduction as AEB3103 Principles of Food and Resource Economics, and UF is its ONLY carrier. Both numbers are flagged as common prerequisites. Take whichever your college offers, and confirm with UF which it accepts before assuming."),
 ("AEB3133", "Principles of Agribusiness Management — FAMU, FGCU and UF. Planning, organising and controlling an agricultural firm: the core management course of the degree, and required at UF.",
  "⚠⚠⚠ SAME TITLE, DIFFERENT COURSE: AEB2102 Principles of Agribusiness Management is taught at Central Florida, Florida SouthWestern, North Florida and St. Johns River. It is a lower-division course with its own number, and taking it does not excuse AEB3133 at a university. The statewide record for AEB3133 names a principles-of-economics prerequisite."),
 ("AEB2192", "Farm Records and Accounts — College of Central Florida. ⚠⚠ The most practical course on this list for someone who will run their own operation: enterprise records, cost of production and the books a lender will ask to see.",
  "⚠ FAMU teaches the upper-division version as AEB3191 Farm Records and Accounts."),
 ("AEB3300", "Marketing Agricultural Products — four carriers (Central Florida, FAMU, FGCU, UF). ⚠ Most Florida farms sell under $10,000 a year; the gap between growing something and being paid for it is marketing.", None),
 ("AEB3144", "Agribusiness Finance — FGCU and UF. Credit, capital budgeting, land and equipment decisions. ⚠⚠ Capital, not knowledge, is what keeps most people out of farming, and this is the course about it.", None),
 ("AEB4085", "Agricultural Risk Management and the Law — UF. Crop insurance, contracts, liability and the legal frame around weather and price risk. ⚠ BLS: farm incomes \"vary from year to year because prices of farm products fluctuate with weather conditions and other factors.\"", None),
 ("AEB4424", "Human Resource Management in Agribusiness — UF. ⚠ Only 26% of Florida farms hire labour, but an operation large enough to employ a salaried manager usually employs a crew too, and managing it is much of what that manager does.", None),
 ("SWS2000", "Introduction to Soil Science — Central Florida, North Florida and St. Johns River. ⚠⚠ Florida's sandy soils hold little water or nutrient, which is why fertiliser and irrigation on Florida farms are managed under state best-management-practice programmes.",
  "⚠ The university version is SWS3022 The Nature and Properties of Soil at FAMU and UF, with SWS3022L as its lab. SWS1102 Soils and Fertilizers (four state colleges) is the applied version."),
 ("ANS3006", "Introductory Animal Science — FAMU, St. Petersburg, UF and USF. ⚠ Florida has 1.57 million head of cattle; for anyone heading toward a ranch, this is the entry course to the animal sciences degree, which is larger than agribusiness at UF.",
  "⚠ College of Central Florida teaches ANS1003 Introduction to Animal Science at the lower division."),
 ("ORH2251C", "Nursery Operation and Management — Eastern Florida State and Valencia. ⚠⚠⚠ Nursery, greenhouse, floriculture and sod are 34% of all Florida farm sales, second in the nation, and more than all Florida livestock combined. \"Nursery Manager\" is one of O*NET's own titles for this occupation.", None),
 ("ORH2260C", "Greenhouse Operations and Management — Eastern Florida State and Valencia. ⚠ Controlled-environment production is where the hired-manager jobs in Florida horticulture concentrate.",
  "⚠ ORH1260 Greenhouse Operations is a shorter version at Central Florida and North Florida."),
 ("AOM2316", "Agricultural Machinery and Equipment — Central Florida, North Florida and St. Johns River. ⚠ BLS: \"Tractors, tools, and other farm machinery and equipment can cause serious injury.\" Operation, maintenance and the cost of owning versus hiring equipment.", None),
 ("AOM2433", "Introduction to Precision Agriculture — College of Central Florida. GPS guidance, variable-rate application, sensors and drones. ⚠⚠ This is the productivity technology BLS names as the reason fewer, larger farms need fewer managers — which makes it the skill that the surviving managers have.",
  "⚠ Florida SouthWestern teaches it as AOM2433C with an integrated lab; UF teaches AOM4434 Precision Agriculture at the upper division."),
 ("AOM3333", "Pesticide Application Technology — UF. ⚠⚠ Applying restricted-use pesticides outdoors in Florida requires an FDACS licence under Chapter 487, F.S., and s. 487.044 requires an examination. The course does not grant the licence; it is the preparation for it.", None),
]

sources = [
 ("BLS Occupational Outlook Handbook — Farmers, Ranchers, and Other Agricultural Managers", "https://www.bls.gov/ooh/management/farmers-ranchers-and-other-agricultural-managers.htm",
  "$89,900 median (May 2025), 788,700 jobs, −3% for 2025–35 and about 70,800 annual openings, all from replacement. Entry-level education HIGH SCHOOL DIPLOMA with 5 years or more of related experience; 67% self-employed. ⚠ The pay figures exclude self-employed workers. Source of the consolidation and technology sentences; AI is not named."),
 ("O*NET — Farmers, Ranchers, and Other Agricultural Managers (11-9013.00)", "https://www.onetonline.org/link/summary/11-9013.00",
  "Job Zone Four — most positions require a bachelor's degree — which disagrees with BLS because O*NET's sample titles (farm, ranch, nursery, greenhouse, hatchery manager) describe the hired third. Projected decline, about 85,500 openings a year for 2024–34."),
 ("O*NET — Florida wages for 11-9013.00", "https://www.onetonline.org/link/localwages/11-9013.00?st=FL",
  "Florida median $87,080 against $89,900 national, but the 75th percentile $141,370 (+$22,510) and 90th $186,940 (+$26,920). These are salaried managers only."),
 ("USDA NASS — 2022 Census of Agriculture, Florida state profile", "https://www.nass.usda.gov/Publications/AgCensus/2022/Online_Resources/County_Profiles/Florida/cp99012.pdf",
  "44,703 farms; 63% sell under $10,000 a year and 14% sell $100,000 or more; 40% of producers are 65 or over and 7% under 35; 26% of farms hire labour. Nursery, greenhouse, floriculture and sod $3.48 billion — 34% of Florida sales, 2nd in the U.S."),
 ("7 CFR 764.152 — Farm Service Agency farm ownership loan experience requirements", "https://www.law.cornell.edu/cfr/text/7/764.152",
  "Three years of participation in a farm's business operations out of the last ten, with listed alternatives that include \"not less than 16 credit hours of post-secondary education in an agriculture-related field.\""),
 ("ASFMRA — Accredited Farm Manager designation", "https://www.asfmra.org/credentials/accredited-farm-manager",
  "Requires a four-year college degree or approved equivalent, four years of farm or ranch management experience, 82 hours of ASFMRA coursework, membership and a demonstration farm management plan."),
 ("FDACS — Pesticide licensing, and s. 487.044, Florida Statutes", "https://www.fdacs.gov/Business-Services/Pesticide-Licensing",
  "A licence under Chapter 487 is required to apply restricted-use pesticides outdoors other than for structural or public-health pest control; s. 487.044 requires applicants to pass an examination."),
 ("UF Undergraduate Catalog — Food and Resource Economics B.S.", "https://catalog.ufl.edu/UGRD/colleges-schools/UGAGL/FRE_BS/",
  "Two specialisations; state-assigned common prerequisites MAC2233, STA2023, ACG2021 and ECO2013 with minimum grades of C; core includes AEB3103, AEB3133, AEB3144 and AEB3300."),
 ("IPEDS completions — Florida, CIP 01", "https://nces.ed.gov/ipeds/",
  "01.01 agribusiness 120 a year (UF 99); 01.00 general 30 (FAMU 29); and the production fields the site cannot yet list — horticulture 204 at ten colleges (Valencia 127), animal sciences 178, plant sciences 134, equine 67, soil 56."),
 ("SCNS statewide course files — AEB, AOM, ORH and ANS", "https://flscns.fldoe.org/",
  "Every undergraduate AEB, AOM and ORH number is guaranteed transfer to an institution offering the same course. AEB2102 and AEB3133 share a title; AEB3103 has one carrier (UF); UF and FAMU share 7 of their 38 and 26 upper-division AEB numbers."),
]

path = {
  "slug": "agricultural-manager",
  "name": "Farmer, Rancher and Agricultural Manager",
  "cipCode": "01.01",
  "socCode": "11-9013",
  "isPublished": True,
  "sortOrder": 143,
  "description": "⚠⚠⚠ 67% of this occupation is self-employed, and BLS puts the entry-level education at a HIGH SCHOOL DIPLOMA plus five or more years of experience. For most farmers the entry requirement is land and capital, not a qualification. ⚠⚠ The degree leads to the other third: the hired farm, ranch, grove, nursery and greenhouse managers, who are the only people the $89,900 median describes — and who in Florida earn $141,370 at the 75th percentile. This page explains what the degree is actually for.",
  "credentialNote": "⚠⚠ NO LICENCE TO FARM, AND NO LICENCE TO MANAGE A FARM. What is regulated is specific work: applying restricted-use pesticides outdoors in Florida requires an FDACS licence under Chapter 487, F.S., with an examination under s. 487.044. ⚠ The profession's voluntary credential is the ASFMRA Accredited Farm Manager, which requires a four-year degree, four years of management experience and 82 hours of coursework — the clearest case where the degree is required. ⚠⚠⚠ AND THE ONE MOST PEOPLE MISS: for a USDA Farm Service Agency farm ownership loan, the applicant needs three years of farm business experience in the last ten, and 7 CFR 764.152 accepts 16 credit hours of agriculture-related postsecondary education as one of the alternatives for part of it. About five courses count toward the loan that a would-be farmer most needs.",
  "cipCodes": [
    {"cipCode": "01.00", "note": "Agriculture, General — FAMU's Agricultural Sciences degree, 29 a year, where part of FAMU's agribusiness training is recorded."},
    {"cipCode": "03.01", "note": "⚠ Natural Resources Conservation — the land-stewardship side of farm management: soil, water and habitat decisions made under Florida's water-management districts and best-management-practice rules."},
    {"cipCode": "52.02", "note": "⚠⚠ Business Administration and Management — BLS names business alongside agriculture as a degree field for this occupation, and it is taught at far more Florida institutions than agribusiness."}
  ],
  "programs": [
    {"slug": "agricultural-business", "note": "The programme. ⚠⚠ Read its note first: agribusiness is the SMALL end of Florida agriculture, and the horticulture, animal and plant science programmes around it are four times its size."},
    {"slug": "business-administration", "note": "⚠⚠ A legitimate route in, and the portable one. A salaried farm manager's job is mostly budgets, labour and marketing; add AEB2104 and AEB3300 to a business degree for the agricultural half."},
    {"slug": "entrepreneurship", "note": "⚠ Two-thirds of the occupation runs its own business. The entrepreneurship courses cover starting one from nothing, which agricultural programmes treat lightly.", "isRoute": False},
    {"slug": "environmental-science", "note": "⚠ The land-stewardship neighbour, and where UF's forestry, wildlife and natural-resource programmes sit.", "isRoute": False},
    {"slug": "logistics-and-supply-chain", "note": "⚠ Where many food and resource economics graduates actually work: getting perishable product from field to shelf.", "isRoute": False}
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

io.open('career_paths/agricultural-manager.json', 'w', encoding='utf-8').write(
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
