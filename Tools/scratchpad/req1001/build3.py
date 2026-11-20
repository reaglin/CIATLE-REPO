import json, sys
sys.path.insert(0, '.')
import mkguide
def o(inst, name, title, cr=3, note=None, ch=None):
    return {"institution": inst, "institution_name": name, "title": title, "credits": cr, "contact_hours": ch, "note": note}
DER = "Florida convention: 45 contact hours for a 3-credit course; no carrier publishes a figure."
M = {
 "CET1178": dict(title="A+ Certification Hardware", credits=3, contact_hours=45,
   prerequisites="None in the statewide record. ⚠ The same course is CET 1178C (integrated lab) at Miami Dade, St. Johns River, Florida Gateway, Seminole State and South Florida State; it has its own guide. The course prepares for CompTIA A+; the exams are taken and paid for separately.",
   offering_notes=dict(summary="Two public carriers of the bare number, both at 3 credits: Indian River State and College of Central Florida. Five more teach CET 1178C.", hours_source="derived", derived_contact_hours=45, derivation=DER,
     offerings=[o("IRSC","Indian River State College","A+ Certification Hardware",note="Broad, both-exam coverage; Meyers All-in-One text."),
                o("CF","College of Central Florida","A+ Fundamentals",note="Software and operating-system emphasis; for beginners; TestOut LabSim.")])),
 "CET2123": dict(title="Microprocessor Fundamentals", credits=3, contact_hours=45,
   prerequisites="None in the statewide record; in practice a digital logic course comes first. ⚠ At FAMU the lab is a separate 1-credit course, CET 2123L: take both. Elsewhere the course is CET 2123C (3-4 credits), which has its own guide.",
   offering_notes=dict(summary="One carrier of the bare number: Florida A&M, 3 credits plus CET 2123L (1 credit). Six colleges teach CET 2123C.", hours_source="derived", derived_contact_hours=45, derivation=DER,
     offerings=[o("FAMU","Florida A&M University","Microprocessor Fundamentals",note="Lecture; lab is CET 2123L (1 credit).")])),
 "CET2118C": dict(title="FPGA Design Using VHDL", credits=3, contact_hours=60,
   prerequisites="CET 2114C or CET 2113C (digital logic) at Valencia College; the statewide record lists CET 2113C or department approval.",
   offering_notes=dict(summary="One carrier: Valencia College, 3 credits, 2 lecture + 2 lab hours a week.", hours_source="derived", derived_contact_hours=60, derivation="Valencia lists 2 lecture + 2 lab hours a week; 4 x 15 weeks = 60.",
     offerings=[o("VC","Valencia College","FPGA Design Using VHDL",note="Special fee $98.")])),
 "CET4663": dict(title="Computer and Network Security", credits=3, contact_hours=45,
   prerequisites="None in the statewide record. Valencia: C or better in EGN 3046 or EGN 3428, and CET 2123C; a C or better is required if the course counts toward its Electrical and Computer Engineering Technology B.S. Miami Dade teaches it as CET 4663C Electronic Security for its electronics engineering technology majors.",
   offering_notes=dict(summary="Two state colleges at 3 credits: Valencia (CET 4663, 3 lecture hours a week) and Miami Dade (CET 4663C).", hours_source="mixed", derived_contact_hours=45, derivation="Valencia lists 3 lecture hours a week; 3 x 15 = 45.",
     offerings=[o("VC","Valencia College","Computer and Network Security",note="3 lecture hours a week; B.S. Electrical and Computer Engineering Technology."),
                o("MDC","Miami Dade College","Electronic Security",note="Taught as CET 4663C with integrated lab.")])),
 "CET4772": dict(title="Cloud Computing Operations and Security", credits=3, contact_hours=45,
   prerequisites="CGS 3763 or COP 4634 or COP 4610 (University of West Florida). The statewide record's prerequisite (\"CET 4XXX (Networks), CET 4XXX (Operating Sys), C- or above\") is an unfilled placeholder.",
   offering_notes=dict(summary="One carrier: University of West Florida, 3 credits.", hours_source="derived", derived_contact_hours=45, derivation=DER,
     offerings=[o("UWF","University of West Florida","Cloud Computing Operations and Security",note="Department of Cybersecurity and Information Technology.")])),
 "EEV0203": dict(title="Solar Thermal System Design, Installation and Maintenance Helper", credits=0, contact_hours=300,
   prerequisites="None published. ⚠ A 300-clock-hour career course (occupational completion point of program X600300). That program no longer appears in Florida's current CTE frameworks: confirm with Okaloosa Technical College that it is enrolling.",
   offering_notes=dict(summary="One public carrier: Okaloosa Technical College, 300 clock hours.", hours_source="published", derived_contact_hours=None, derivation=None,
     offerings=[o("OTC","Okaloosa Technical College","Solar Thermal System Design, Installation and Maintenance Helper",cr=0,ch=300,note="Public district technical college; program no longer in current frameworks.")])),
}
for cid, m in M.items():
    m.setdefault('version','1.0'); print(mkguide.build(cid, m))
# corrections: reuse the published drafts' scalars, bump version, 60 hours
for cid, ver in (("AOM1465C","1.1"),("AOM2012C","1.1"),("ACG2021C","1.2")):
    g=json.load(open('../drafts/%s_guide.json'%cid,encoding='utf-8'))
    on=g.get('offering_notes')
    if on:
        on['derived_contact_hours']=60; on['derivation']="Valencia lists 3 lecture + 1 lab hours a week; 4 x 15 weeks = 60."
        on['summary']=on['summary'].replace('3 contact and 1 lab hours','3 lecture and 1 lab hours a week')
        for r in on['offerings']:
            if r.get('note'): r['note']=r['note'].replace('3 contact and 1 lab hours','3 lecture + 1 lab hours a week')
    meta=dict(title=g['title'],credits=g['credits'],contact_hours=60,prerequisites=g['prerequisites'],version=ver,offering_notes=on)
    print(mkguide.build(cid, meta))
