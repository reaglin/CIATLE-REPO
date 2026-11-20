import json, sys
sys.path.insert(0, '.')
import mkguide
def o(inst, name, title, cr=3, note=None):
    return {"institution": inst, "institution_name": name, "title": title, "credits": cr, "contact_hours": None, "note": note}
DER = "Florida convention: 45 contact hours for a 3-credit course; no carrier publishes a figure."
M = {
 "ACG1001": dict(title="Principles of Accounting I (Financial Accounting I)", credits=3, contact_hours=45,
   prerequisites="None published. ⚠ At Florida SouthWestern, credit is not given for both ACG 1001 and ACG 2021, and ACG 1001 does not meet FSW's business or accounting A.S. requirements for students entering from Fall 2014. ⚠⚠ Business and accounting bachelor's degrees expect ACG 2021 (a state common prerequisite); ACG 1001 is only the first half of it (ACG x001 + ACG x011 = ACG x021).",
   offering_notes=dict(summary="Two public carriers, both at 3 credits. Neither publishes contact hours.", hours_source="derived", derived_contact_hours=45, derivation=DER,
     offerings=[o("FSWSC","Florida SouthWestern State College","Financial Accounting I",note="Not a program requirement for students entering FSW accounting/business A.S. programs from Fall 2014; no credit for both ACG 1001 and ACG 2021."),
                o("SSCF","Seminole State College of Florida","Introduction to Accounting",note="State record: not found in Seminole catalog since 3/16/15. Seminole teaches ACG 2021C.")])),
 "EET0052": dict(title="Fundamentals of Electricity and Basic Materials", credits=3, contact_hours=45,
   prerequisites=None,
   offering_notes=dict(summary="No Florida public carrier. Only CBT Technology Institute (private) carries it, at 3 credits; listed here because a visitor requested the guide.", hours_source="derived", derived_contact_hours=45, derivation=DER, offerings=[])),
 "ATT3811": dict(title="Air Traffic Control Systems", credits=3, contact_hours=45,
   prerequisites="None published (statewide record and UWF catalog). Upper-division course at the University of West Florida; may not be repeated for credit. ⚠ This is a systems survey, not FAA controller training.",
   offering_notes=dict(summary="One carrier: University of West Florida, 3 credits.", hours_source="derived", derived_contact_hours=45, derivation=DER,
     offerings=[o("UWF","University of West Florida","Air Traffic Control Systems",note="Department of Commerce, College of Business.")])),
 "AOM1465C": dict(title="Introduction to Sustainable Agriculture", credits=3, contact_hours=45,
   prerequisites="None (statewide record and Valencia College catalog).",
   offering_notes=dict(summary="One carrier: Valencia College, 3 credits; catalog lists 3 contact and 1 lab hours.", hours_source="derived", derived_contact_hours=45, derivation="Valencia lists 3 weekly contact hours; 3 x 15 weeks = 45.",
     offerings=[o("VC","Valencia College","Introduction to Sustainable Agriculture",note="Required in the Sustainable Agriculture Specialization of the A.S. in Landscape and Horticulture Technology.")])),
 "AOM2012C": dict(title="Types and Systems of Agricultural Operations", credits=3, contact_hours=45,
   prerequisites="None (statewide record and Valencia College catalog). Valencia charges a special fee ($82) and includes field trips.",
   offering_notes=dict(summary="One carrier: Valencia College, 3 credits; catalog lists 3 contact and 1 lab hours.", hours_source="derived", derived_contact_hours=45, derivation="Valencia lists 3 weekly contact hours; 3 x 15 weeks = 45.",
     offerings=[o("VC","Valencia College","Types & Systems of Agriculture Operations",note="Required for all students in the A.S. in Landscape and Horticulture Technology; special fee $82; field trips.")])),
 "AOM2316": dict(title="Agricultural Machinery and Equipment", credits=3, contact_hours=45,
   prerequisites="None (statewide record).",
   offering_notes=dict(summary="All three carriers teach it at 3 credits under the same title. None publishes contact hours.", hours_source="derived", derived_contact_hours=45, derivation=DER,
     offerings=[o("CF","College of Central Florida","Agricultural Machinery and Equipment",note="Agribusiness Management program; ten-unit outline."),
                o("NFC","North Florida College","Agricultural Machinery and Equipment",note="Core course of the A.S. in Agribusiness Management."),
                o("SJRSC","St. Johns River State College","Agricultural Machinery and Equipment")])),
 "AOM2433": dict(title="Introduction to Precision Agriculture", credits=3, contact_hours=45,
   prerequisites="None (statewide record). ⚠ Florida SouthWestern teaches the same course as AOM 2433C with an integrated lab; UF's AOM 4434 Precision Agriculture is the upper-division course (junior standing).",
   offering_notes=dict(summary="College of Central Florida teaches AOM 2433 at 3 credits; Florida SouthWestern teaches AOM 2433C at 3 credits. Neither publishes contact hours.", hours_source="derived", derived_contact_hours=45, derivation=DER,
     offerings=[o("CF","College of Central Florida","Introduction to Precision Agriculture",note="Text: Zaman, Precision Agriculture: Evolution, Insights and Emerging Trends."),
                o("FSWSC","Florida SouthWestern State College","Introduction to Precision Agriculture",note="Taught as AOM 2433C (integrated lab) at the Hendry/Glades Curtis Center from Fall 2026.")])),
 "AOM3073": dict(title="Safety in Agriculture", credits=3, contact_hours=45,
   prerequisites="None in the statewide record. ⚠ Upper-division course in College of Central Florida's B.A.S. (Business and Organizational Management, Agribusiness Specialization); expect admission to the B.A.S. program to be required.",
   offering_notes=dict(summary="One carrier: College of Central Florida, 3 credits.", hours_source="derived", derived_contact_hours=45, derivation=DER,
     offerings=[o("CF","College of Central Florida","Safety in Agriculture",note="Upper division; B.A.S. Agribusiness Specialization.")])),
 "AOM3220": dict(title="Agricultural Construction and Maintenance", credits=3, contact_hours=45,
   prerequisites="Junior standing or higher (University of Florida).",
   offering_notes=dict(summary="One carrier: University of Florida, 3 credits, lecture plus hands-on lab.", hours_source="derived", derived_contact_hours=45, derivation=DER + " The course has a lab component and may meet longer.",
     offerings=[o("UF","University of Florida","Agricultural Construction and Maintenance",note="Semester five of the Agricultural Operations Management B.S.; letter grade.")])),
}
json.dump(M, open('req1001/meta.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
for cid, m in M.items():
    m.setdefault('version','1.0')
    print(mkguide.build(cid, m))
