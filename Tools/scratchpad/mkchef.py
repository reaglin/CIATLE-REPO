# -*- coding: utf-8 -*-
"""Assemble the culinary arts programme and the chef / cook / baker career path.

Row 146 of QUEUE.csv, written 2026-09-23 in answer to the first two visitor requests
(35-2014 Cooks, Restaurant and 51-3011 Bakers, both asked from 12.05), which the page
covers as sections through additionalSocCodes.
"""
import io, json

body = io.open('scratchpad/body_chef.html', encoding='utf-8').read()

program = {
  "slug": "culinary-arts",
  "name": "Culinary Arts, Baking and Culinary Management",
  "isPublished": True,
  "sortOrder": 640,
  "description": "Cooking, baking and pastry, and running a kitchen, taught in Florida as clock-hour certificates at technical colleges and as college-credit certificates and associate degrees at state colleges. ⚠⚠ About 1,255 credentials a year at 46 public institutions, and no bachelor's degree anywhere: the four-year route is hospitality management.",
  "degreesNote": "⚠⚠ Three programmes share this classification. Culinary Arts / Chef Training (12.0503) is the largest, 620 credentials a year at 44 institutions, nearly all certificates: Valencia 87, Miami Dade 52, Atlantic Technical 49, McFatter Technical 36. Baking and Pastry Arts (12.0501) is 352 at 12, and ⚠⚠ Valencia alone awards 234 of them, two thirds of the state. Restaurant, Culinary and Catering Management (12.0504) is 280 at 12, 146 of them associate degrees, led by Valencia 78 and Miami Dade 76. ⚠⚠⚠ Florida's clock-hour programme, Commercial Foods and Culinary Arts, is 1,200 hours in four 300-hour courses named after jobs: Food Preparation, Cook (Restaurant), Chef/Head Cook and Food Service Management. The baking programme is 600 hours: Pastry Cook/Baker, then Pastry Chef/Head Baker. Each completion point is a place to stop and be hired, so ask whether the college awards a certificate there. ⚠ Clock hours are not college credit: moving from a technical-college certificate to an A.S. depends on an articulation agreement between the two schools. ⚠ None of these jobs requires the programme to start. What the programme buys is a structured start, the Florida food-safety certificates, baking, and the management rung.",
  "cips": [
    { "cipCode": "12.05", "note": "Culinary Arts and Related Services — 1,255 Florida public credentials a year at 46 institutions: Culinary Arts/Chef Training (12.0503) 620 at 44, Baking and Pastry Arts (12.0501) 352 at 12 (Valencia 234), and Restaurant, Culinary and Catering Management (12.0504) 280 at 12. No bachelor's degree." }
  ],
  "related": [
    { "slug": "hospitality-management", "note": "⚠⚠ The four-year route, and where the management rung leads. Florida awards no bachelor's in culinary arts; a hospitality management degree trains people to run restaurants, hotels and food service rather than to cook. A culinary A.S. followed by a hospitality bachelor's combines the kitchen and the management." },
    { "slug": "entrepreneurship", "note": "⚠ Many cooks aim at their own restaurant, food truck, bakery or catering business. The kitchen skills are necessary but not sufficient: costing, cash flow and leases decide whether the business lasts, and the entrepreneurship courses cover them.", "isRoute": False },
    { "slug": "dietetics-and-nutrition", "note": "⚠ The licensed neighbour. Hospital and school food service, special diets and menu planning for health all meet dietetics, and nutrition advice beyond general guidance is regulated in Florida.", "isRoute": False }
  ]
}
io.open('programs/culinary-arts.json', 'w', encoding='utf-8').write(json.dumps(program, ensure_ascii=False, indent=2))

courses = [
 ("HMV0100", "Food Preparation — 300 hours, at all 34 institutions that run Florida's clock-hour culinary programme, and its first completion point. Knife work, cooking methods, kitchen equipment and sanitation.", None),
 ("HMV0170", "Cook, Restaurant — 300 hours, a completion point named after the job. ⚠⚠ Restaurant cooking has about 250,700 openings a year (O*NET) and needs no credential to enter, so this is where the programme and the job market meet.", None),
 ("HMV0171", "Chef/Head Cook — 300 hours, a completion point, and the state course record ties it to SOC 35-1011. ⚠⚠ The course teaches the job; being hired as a chef still takes years in kitchens. BLS lists five years or more of experience.", None),
 ("HMV0126", "Food Service Management — 300 hours; the state record ties it to food service managers (SOC 11-9051). ⚠ Menus, costing, staffing and ordering. It is the rung where the pay changes, and Florida requires a manager's food-protection certificate within 30 days of taking a management job.", None),
 ("FSS0090", "Pastry Cook/Baker — completion point A of the clock-hour baking programme, 300 hours, at six technical colleges. ⚠⚠ The baker occupation, taught as a hireable exit.",
  "⚠ The college-credit equivalent is Baking and Pastries I (FSS1246C) at six state colleges; see below."),
 ("FSS0091", "Pastry Chef/Head Baker — completion point B, a further 300 hours: laminated doughs, plated desserts, cakes and production planning.", None),
 ("FOS2201", "Food Safety and Sanitation — eight carriers. ⚠⚠ The course behind the certificates Florida law requires: food handler certification within 60 days of employment (s. 509.049, F.S.) and the manager's food-protection test within 30 days (s. 509.039).",
  "⚠ Daytona State, FSCJ and Hillsborough teach it as FOS1201 Sanitation and Safety Management; Miami Dade and Palm Beach State as HFT1212 Safety and Sanitation."),
 ("FSS1202C", "Food Production I — Daytona State, FSCJ, Gulf Coast and Miami Dade. The foundations of cooking on the college-credit route: methods, stocks and sauces, and station work.",
  "⚠ Broward, the College of the Florida Keys, Indian River and Valencia call their version FSS1203C Quantity Food Production I. The same statewide course (Basic Food Preparation) is also packaged as a lecture plus a lab: Miami Dade's FSS1202, Northwest Florida State's FSS1202L, and UNF's FSS1202 with FSS1202L, which UNF titles Food Fundamentals and teaches in its nutrition programme. Lecture plus lab completes the course the same way the combined C version does."),
 ("FSS1240C", "Classical Cuisine — five carriers. The French foundations — mother sauces, classical cuts and preparations — that kitchens still use as a common language.", None),
 ("FSS2248C", "Garde Manger — seven carriers, the widest culinary course at the state colleges. The cold kitchen: charcuterie, salads, cold sauces, buffet and platter work. ⚠ Catering and banquet kitchens hire for it.", None),
 ("FSS2242C", "International Cuisine — five carriers. ⚠ In a Florida kitchen, the Latin American and Caribbean repertoire is not an elective topic. Ask which cuisines the course covers.",
  "⚠ The College of the Florida Keys and Northwest Florida State teach FSS2241C International and Regional Cuisine."),
 ("FSS1246C", "Baking and Pastries I — six carriers (Broward, Florida Keys, Indian River, Miami Dade, Northwest Florida State, Valencia). ⚠ The college-credit start for the baker career.",
  "⚠ Daytona State, Gulf Coast, Hillsborough and Pensacola State teach FSS1063C Food Service Specialties - Baking; Palm Beach State and Valencia also offer FSS1050C Basic Baking. Valencia runs a full pastry sequence of its own (artisan breads, cakes, chocolates and confections)."),
 ("FSS2247C", "Baking and Pastries II — five carriers. Advanced doughs, cakes and plated desserts: the baking a restaurant pastry station actually needs.", None),
 ("HUN1203", "Culinary Nutrition — Daytona State, FSCJ and Indian River. ⚠ Allergens, special diets and menu labelling are daily kitchen work, and hospital, school and senior-living kitchens run on them.", None),
 ("FSS2500", "Food Service Costing and Controls — six carriers. ⚠⚠ Food cost, portion control and inventory. It is what separates a cook from someone who can run a kitchen: food service margins are thin, and costing decides whether a kitchen makes money.", None),
 ("FSS2251", "Food and Beverage Management — five carriers. Purchasing, beverage service and front-of-house operations: the management half of the A.S.", None),
 ("FSS2942", "Culinary Management Internship I — FSCJ, Indian River, Northwest Florida State and Valencia. ⚠⚠ Every year in a kitchen counts toward the five years BLS says a chef needs. Choose the placement for the kind of kitchen you want to work in: hotel, restaurant, catering or institutional.",
  "⚠ Gulf Coast and Hillsborough call it FSS1942 Culinary Externship."),
]

sources = [
 ("BLS Occupational Outlook Handbook — Chefs and Head Cooks", "https://www.bls.gov/ooh/food-preparation-and-serving/chefs-and-head-cooks.htm",
  "$62,470 median (2025), 220,300 jobs, +7% for 2025–35, about 25,200 openings a year. Entry: high school diploma and 5 years or more of related experience; 7% self-employed. No mention of automation or AI."),
 ("BLS Occupational Outlook Handbook — Cooks", "https://www.bls.gov/ooh/food-preparation-and-serving/cooks.htm",
  "Restaurant cooks $17.98 an hour (2025); 2.7 million cooks, +7%, about 393,200 openings a year. Most learn on the job and \"no formal education is typically required\". No mention of automation, AI or robots."),
 ("BLS Occupational Outlook Handbook — Bakers", "https://www.bls.gov/ooh/production/bakers.htm",
  "$37,160 median (2025), 262,400 jobs, +6%, about 36,500 openings a year; no formal educational credential, with moderate-term on-the-job training of up to a year; 10% self-employed."),
 ("O*NET — Cooks, Restaurant (35-2014.00)", "https://www.onetonline.org/link/summary/35-2014.00",
  "Job Zone One to Two; 47% of respondents report a high school diploma and 34% less; 1,460,200 employed and about 250,700 openings a year projected for 2024–34."),
 ("O*NET — Florida wages for chefs (35-1011), restaurant cooks (35-2014) and bakers (51-3011)", "https://www.onetonline.org/link/localwages/35-2014.00?st=FL",
  "Florida medians: chefs $58,240, restaurant cooks $37,020, bakers $35,870. The restaurant-cook band runs $29,710 to $46,450 from the 10th to the 90th percentile."),
 ("s. 509.049, Florida Statutes — food service employee training", "https://www.flsenate.gov/Laws/Statutes/2025/509.049",
  "Food service employees must receive certification within 60 days after employment; it remains valid for 3 years."),
 ("s. 509.039, Florida Statutes — food service managers", "https://www.flsenate.gov/Laws/Statutes/2025/509.039",
  "All managers must pass an approved food-protection test, within 30 days after employment."),
 ("CPALMS-CTE — Florida culinary and baking curriculum frameworks (CIP 12.05)", "https://ctepreview.cpalms.org/",
  "Seventeen culinary and baking programmes, among them Professional Culinary Arts & Hospitality (clock hour), Baking and Pastry Arts (clock hour), Culinary Management A.S., Baking & Pastry Management A.S., and three registered apprenticeships."),
 ("SCNS statewide course file — HMV and FSS", "https://flscns.fldoe.org/",
  "HMV0100, HMV0170 and HMV0171 are occupational completion points of the 1,200-hour Commercial Foods and Culinary Arts programme (SOC 35-1011 on the chef course, 11-9051 on management); FSS0090/FSS0091 are baking completion points A and B. All are guaranteed transfer."),
 ("IPEDS completions — Florida, CIP 12.05", "https://nces.ed.gov/ipeds/",
  "12.0503: 620 at 44 institutions; 12.0501: 352 at 12 (Valencia 234); 12.0504: 280 at 12 (146 associate). No bachelor's."),
]

path = {
  "slug": "chef",
  "name": "Chef, Cook and Baker",
  "cipCode": "12.05",
  "socCode": "35-1011",
  "additionalSocCodes": ["35-2014", "51-3011"],
  "isPublished": True,
  "sortOrder": 146,
  "description": "⚠⚠⚠ No kitchen job needs a credential to start: restaurant cooks and bakers learn on the job, and a chef needs a high school diploma plus five or more years of experience. ⚠⚠ The pay step is from cook ($37,020 Florida median) to chef or head cook ($58,240), and it takes experience rather than a certificate. Florida's 1,200-hour culinary programme is built from courses named after the jobs (Cook, Restaurant, then Chef/Head Cook), and this page explains what it is worth.",
  "credentialNote": "⚠⚠ NO LICENCE TO COOK, BUT TWO FLORIDA CERTIFICATES. Every food service employee who stores, prepares or serves food must be certified in food handling within 60 days of being hired, valid for 3 years (s. 509.049, F.S.). Every manager must pass an approved food-protection test within 30 days of being hired (s. 509.039). ⚠ The manager's certificate is the one that matters for moving from cook to kitchen manager or chef. Both are regulated by DBPR's Division of Hotels and Restaurants. ⚠ Beyond those, what an employer checks is experience. BLS lists five years or more for a chef, and no programme replaces that.",
  "cipCodes": [
    {"cipCode": "52.09", "note": "⚠⚠ Hospitality Administration/Management — the four-year route, since Florida awards no bachelor's in culinary arts. It leads to running restaurants, hotels and food service; the Hospitality Manager path covers food service managers (SOC 11-9051), the rung the clock-hour programme's last course points at."}
  ],
  "programs": [
    {"slug": "culinary-arts", "note": "The programme — read its note for the clock-hour versus college-credit split and why Valencia dominates baking."},
    {"slug": "hospitality-management", "note": "⚠⚠ The bachelor's route, and the management side of the same industry. Pairs naturally with a culinary A.S."},
    {"slug": "entrepreneurship", "note": "⚠ For the cook who wants their own restaurant, bakery, food truck or catering business, where costing and cash flow decide survival more than the food does.", "isRoute": False},
    {"slug": "dietetics-and-nutrition", "note": "⚠ The licensed neighbour, for hospital, school and special-diet food service.", "isRoute": False}
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

io.open('career_paths/chef.json', 'w', encoding='utf-8').write(json.dumps(path, ensure_ascii=False, indent=2))

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
