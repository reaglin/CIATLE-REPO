import sys
sys.path.insert(0, '.')
import mkguide
def o(inst, name, title, cr=3, note=None):
    return {"institution": inst, "institution_name": name, "title": title, "credits": cr, "contact_hours": None, "note": note}
M = {
 "ETM2315": dict(title="Hydraulics and Pneumatics", credits=3, contact_hours=45,
   prerequisites="Algebra (statewide record). ⚠ Most Florida colleges teach this course as ETM 2315C with an integrated lab (13 public colleges; it has its own guide). Hillsborough pairs ETM 2315 with a separate 1-credit lab, ETM 2315L; take both.",
   offering_notes=dict(summary="Three public carriers of the bare number, all at 3 credits: Hillsborough (plus ETM 2315L lab), Pasco-Hernando (lab within the course), South Florida State (also ETM 2314C, 4 credits with lab).", hours_source="derived", derived_contact_hours=45,
     derivation="Florida convention: 45 contact hours for a 3-credit lecture course; no carrier publishes a figure.",
     offerings=[o("HC","Hillsborough College","Hydraulic and Pneumatic Systems",note="Separate 1-credit lab ETM 2315L."),
                o("PHSC","Pasco-Hernando State College","Hydraulics and Pneumatics",note="Laboratory described within the course."),
                o("SFSC","South Florida State College","Hydraulics and Pneumatics",note="Lecture; ETM 2314C is the 4-credit lab version.")])),
 "ETM2310C": dict(title="Fluid Mechanics I", credits=3, contact_hours=60,
   prerequisites="Algebra (statewide record). ⚠ FAMU, the only carrier, also lists a separate 1-credit Fluid Mechanics Lab (ETM 2310L). Not a substitute for calculus-based engineering fluid mechanics (EML 3701, CWR 3201, EGN 3353C) in transfer.",
   offering_notes=dict(summary="One carrier: Florida A&M University, 3 credits, with a separate 1-credit lab ETM 2310L.", hours_source="derived", derived_contact_hours=60,
     derivation="Florida convention: 60 contact hours for a 3-credit C course; FAMU publishes no figure.",
     offerings=[o("FAMU","Florida A&M University","Fluid Mechanics I",note="Sequel ETM 3311C not in FAMU's catalog since 2005; ETM 3316 Hydraulics follows.")])),
 "ETM3316": dict(title="Hydraulics (Hydrostatic Forces)", credits=4, contact_hours=60,
   prerequisites="ETG 2502 Statics (FAMU). ⚠ Civil-engineering hydraulics (hydrostatic forces, pipe networks, open channels), not fluid power. FAMU's companion lab ETM 3316L carries 0 credits: real hours that do not count toward full-time enrolment. An older FAMU catalog lists the course at 3 credits; check the current one.",
   offering_notes=dict(summary="One carrier: Florida A&M University, 4 credits in the state file, with a 0-credit lab ETM 3316L.", hours_source="derived", derived_contact_hours=60,
     derivation="Florida convention: 60 contact hours for a 4-credit course; the zero-credit lab adds its own hours.",
     offerings=[o("FAMU","Florida A&M University","Hydraulics",cr=4,note="0-credit lab ETM 3316L; prerequisite ETG 2502 Statics; older catalog lists 3 credits.")])),
 "ETM2317C": dict(title="Drive and Pump Systems", credits=3, contact_hours=60,
   prerequisites="MAT 1033 and EST 1521 in the statewide record. ⚠ EST 1521 is no longer an active course number, so check Florida State College at Jacksonville's catalog for the prerequisite it enforces.",
   offering_notes=dict(summary="One carrier: Florida State College at Jacksonville, 3 credits.", hours_source="derived", derived_contact_hours=60,
     derivation="Florida convention: 60 contact hours for a 3-credit C course; FSCJ publishes no figure.",
     offerings=[o("FSCJ","Florida State College at Jacksonville","Drive and Pump Systems",note="Maintenance-focused outline: pumps, valves, heat exchangers, hands-on testing.")])),
}
for cid, m in M.items():
    m.setdefault('version','1.0'); print(mkguide.build(cid, m))
