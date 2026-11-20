import json, sys
sys.path.insert(0, '.')
import scns, mkguide
im = {int(k): v for k, v in json.load(open('inst_map.json', encoding='utf-8')).items()}
NOTES = {'UF': '4 credits (the only carrier above 3).', 'FIU': 'Titled Accounting for Decisions; user/decision emphasis.',
         'FAU': 'Also an Honors section (3 credits).', 'HC': 'Also an Honors section (3 credits).',
         'SSCF': 'ACG 2021 is the Honors section; the regular course is ACG 2021C.',
         'MDC': 'Companion 1-credit computerised lab, ACG 2021L.', 'FAMU': 'Also lists ACG 2021L (3 credits) and ACG 2022.'}
seen = {}
for r in scns.parse_flatfile('crslist.txt', 'ACG'):
    cid = r['prefix']+r['level']+r['century']+r['decade']+r['unit']+r['lab'].strip()
    if cid != 'ACG2021': continue
    full = im.get(int(r['institution']), '?'); code, name = full.split(' - ', 1)
    if not scns.is_public(code): continue
    t = mkguide  # noqa
    title = r['inst_title']
    if code in seen and 'HONORS' in title: continue
    if code in seen and 'HONORS' in seen[code]['title'].upper(): pass
    seen[code] = {"institution": code, "institution_name": name.title().replace(' Of ', ' of ').replace(' At ', ' at ').replace("A & M", "A&M"),
                  "title": title.title().replace(' Of ', ' of ').replace(' To ', ' to ').replace(' For ', ' for '),
                  "credits": int(float(r['credit'])), "contact_hours": None, "note": NOTES.get(code)}
offs = sorted(seen.values(), key=lambda x: x['institution'])
print(len(offs), [(o['institution'], o['credits'], o['title']) for o in offs if o['institution'] in ('FAU','HC','SSCF','UF')])
meta = dict(title="Principles of Financial Accounting", credits=3, contact_hours=45, version="1.0",
  prerequisites="None in the statewide record; some colleges expect college-level math readiness (placement, or MAT 1033). ⚠ A state common prerequisite for business bachelor's degrees, where universities usually require a C or better. UF teaches it at 4 credits. Florida SouthWestern gives no credit for both ACG 1001 and ACG 2021. Palm Beach State teaches the four-credit ACG 2022 instead; confirm acceptance with the receiving university.",
  offering_notes=dict(summary="32 public carriers: 31 at 3 credits, the University of Florida at 4. None publishes contact hours. ACG 2021C (St. Johns River, Seminole State, Valencia) and ACG 2022 (Palm Beach State, FAMU) are related numbers.",
     hours_source="derived", derived_contact_hours=45, derivation="Florida convention: 45 contact hours for a 3-credit lecture course (about 60 for UF's 4 credits).", offerings=offs))
print(mkguide.build('ACG2021', meta))
