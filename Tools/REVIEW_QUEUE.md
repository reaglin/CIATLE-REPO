# Review queue — decisions waiting on Ron

Items the guide pipeline surfaced that **need a human decision before I act**. I add to this file as
findings come up and update the status line when a decision lands. Nothing here is blocking the batch
loop; the loop continues around them.

Two kinds of item live here:

- **Correction candidates** — a guide is already live and I have evidence it is wrong or incomplete.
  Republishing overwrites live content and bumps the version, so it waits for a go-ahead.
- **Scope decisions** — the skip list, queue membership, and similar calls that are Ron's to make.

**Last updated:** 2026-09-03 (batch 94)

---

## Open — awaiting decision
### 1. `ETI4448` — scope gap on a capstone (correction candidate)

| | |
|---|---|
| **Status** | ⏳ Open since 2026-09-02 (found in batch 58 while writing ETI4448C) |
| **Live now** | "Applied Project Management", 3 cr / 45 hrs, published 2026-05-02 |
| **Proposed** | Republish as **v1.1** — keep the credits/hours, add the senior-design half |
| **Risk if left** | Advising harm: a student may miss a graduation date |

Daytona State calls this number **"Project Management and Senior Design I"** — a **capstone** with
prerequisite **EGN3613**, a **$100 lab fee**, a required **working prototype**, a final presentation, and
a **second term implied by the "I"**. The live guide mentions *capstone* only in passing and **never
mentions senior design at all**, so it reads as a project-management elective.

The project-management content is genuine, so this is not a wrong-subject error like MAN3554 — it is a
**scope gap**. It matters because **a capstone generally cannot be satisfied by transfer**, and a student
who does not know a second term follows can miss a graduation date.

**What I'd change:** senior-design half, EGN3613 prerequisite, prototype deliverable, $100 fee, and the
two-term sequence.

---

### 2. `RTE2563C` — credit mismatch and a missing sequence partner (correction candidate)

| | |
|---|---|
| **Status** | ⏳ Open since 2026-09-02 (found in batch 62 while writing RTE2573C) |
| **Live now** | "Advanced Medical Imaging", **3 cr / 60 hrs** |
| **Proposed** | Republish as **v1.1** at the DSC credit value with the I/II pairing named |
| **Risk if left** | A student would not know a second required course follows |

Daytona State publishes the same number as **"Selected Radiographic Special Procedures I" at 5 credits**,
offered summer — techniques *other than* diagnostic radiography: cardiac, nervous, and reproductive
system anatomy, cross-sectional anatomy, and the imaging and therapeutic procedures for those systems.

Its sequel **`RTE2573C` "Selected Radiographic Special Procedures II" is 4 credits** and continues into
surgical imaging, CT, MRI, sonography, radiation therapy, nuclear medicine, and interventional work.

Two problems: a **credit mismatch (3 vs 5)** and a **missing sequence partner** — the live guide never
names RTE2573C. Same pattern as the SON2122C/SON2121C and RTE2844L/RTE2854L cases already fixed.

⚠ Complicating factor: **this number carries four different titles across the state** (statewide
inventory *Advanced Medical Imaging*; Broward *Advanced Image Modalities* 3 cr/48 hr; Valencia
*Principles of Radiography III* 3 cr; DSC *Selected Radiographic Special Procedures I* 5 cr). The live
guide already carries a comparison table. **Decision needed on which institution's credit value leads** —
my recommendation is DSC, consistent with the Tier-0 rule, with the others in the table.

---

### 3. `EET1025C` — contact hours outside the family (correction candidate)

| | |
|---|---|
| **Status** | ⏳ Open since 2026-09-01 (found in batch 80) |
| **Live now** | "A/C Circuits", 3 cr / **90 hrs** |
| **Proposed** | Review toward **3 cr / 60 hrs**, noting MDC carries the number at 4 credits |
| **Risk if left** | Low — an internal-consistency outlier, not an advising hazard |

**90 hours at 3 credits is outside the family** in every direction I can check:

| Reference | Credits | Hours |
|---|---|---|
| Valencia EET1025C | 3 | **60** (2 lec + 2 lab) |
| Miami Dade EET1025C | **4** | — |
| This repo's EET1011C | 3 | 75 |
| This repo's EET1084C | 3 | 60 |
| Valencia's EET C-suffixed family | 3 | 60 (2+2 throughout) |

Nothing found supports 90. Same class as the ASL and ART hour corrections already made — an
internal-consistency outlier rather than a contested external fact.

---

### 4. `TPP2118` / `TPP2119` — catalog prerequisites name a course DSC does not offer (verification candidate)

| | |
|---|---|
| **Status** | ⏳ Open since 2026-09-03 (found in batch 111) |
| **Live now** | Both published v1.0 with the discrepancy disclosed and the reader told to confirm |
| **Proposed** | Ask the DSC theatre department which prerequisite is intended; republish as v1.1 if they confirm |
| **Risk if left** | Low — the guides already disclose it; but a transfer student could be misadvised |

Daytona State publishes the prerequisite for **TPP2118 (Acting 3)** as **THE1036** and for
**TPP2119 (Acting 4)** as **THE2037**. **DSC's own inventory (`daytona_courses.csv`) contains neither** —
its entire THE holding is **THE1000 (Theatre Appreciation)**. What DSC does publish is a complete acting
sequence under TPP: **TPP1110 (Acting 1)** and **TPP1111 (Acting 2)**.

The near-certain reading is carry-over from another institution's numbering or an earlier catalog, and
`SOURCES.md` already records the condition that produces it — Florida carries introductory acting under
**two SCNS numbers** (TPP1110 and TPP2100), a finding that previously forced a v1.1 on TPP2300C.

**No correction was made.** Per standing practice the guides report the discrepancy rather than resolving
it — Tier 0 settles facts, and it does not authorise the guide to correct Tier 0. **This item exists only
because a single email to the department would settle it**, and if they confirm the intended prerequisite
both guides can be republished as v1.1 with the ambiguity removed.

### 5. `PHT2931` — probably not a shell (scope decision)

| | |
|---|---|
| **Status** | ⏸ **Ron gathering 9xx usage data 2026-09-03** — revisit with item 5 |
| **Now** | `skipped` — caught by the standing 9xx-shell rule |
| **Proposed** | **Un-skip and write it** |
| **Institutions** | 14 |

All four catalogs pulled in batch 92 publish it as a **real, consistently-titled course**:

| Institution | Title | Credits | Notes |
|---|---|---|---|
| Seminole State | Trends in Physical Therapy | 1 | |
| Polk State | Trends in Physical Therapy | — | **corequisite of PHT2221C**, fall |
| Gulf Coast State | **Seminar** | 2 | coreqs PHT2810 + PHT2820, $129 fee; content is *clinical research, professional development, licensure, and exam preparation* |

This is a **capstone/licensure-prep seminar taken alongside the terminal clinicals**, not a directed-study
shell. The 9xx rule is correct in general — it has correctly caught dozens of internship and
special-topics shells — but **931 in a licensed allied-health prefix is being used as a seminar slot**,
and the title is stable across institutions, which is the signal that distinguishes a real course.

Un-skipping it would also **complete the PHT prefix** except for PHT1006C (item 6).

⚠ Related pattern, already applied without needing a decision: batch 93 found **RTV2290 "Selected Topics
in Remote Sports Production"** is a real prerequisite-gated course despite its title. That one was
*queued*, not skipped, so I just wrote it. The refined rule now in SOURCES.md: **the 9xx-number test is
reliable; "Seminar" or "Selected Topics" in a title is not** — check prerequisites and offering pattern.

**This has now grown past a single course — see item 5.**

---

### 6. Re-screen the skipped 9xx rows (scope decision) — ⬆ **the highest-value item here**

| | |
|---|---|
| **Status** | ⏸ **Ron gathering 9xx usage data 2026-09-03** — do not re-screen until that lands |
| **Now** | 238 rows skipped; **44 are 9xx numbers whose titles do not read like a shell** |
| **Proposed** | Let me re-screen those 44 and un-skip the ones that are real courses |
| **Estimated real courses recovered** | roughly 6–12 |

The 9xx-shell rule has been correct dozens of times and I am not proposing to drop it. But three batches
in a row have now turned up **9xx numbers carrying fixed, substantive, prerequisite-gated content**, and a
screen of the skip list shows it is not isolated.

**Clearest candidates from the 44:**

| Course | Institutions | Title | Why it looks real |
|---|---|---|---|
| **CCJ2930** | **12** | Cybercrime | A named subject taught at 12 institutions — not a variable-content slot |
| **PHT2931** | **14** | Trends in Physical Therapy | Item 4 above; corequisite of the terminal clinicals |
| **EPI0940C** | **10** | Field Experience | Required educator-prep field component |
| **SLS2940** | 7 | Service Learning | Structured, assessed, widely offered |
| **IND1935** | 5 | Building and Barrier Free Codes | A specific technical subject (accessibility codes) |
| **OTH2933C** | 3 | Leadership and Management | A named subject in the OTA sequence |
| **STS2944C / 2945C / 2946** | 11 / 11 / 2 | Surgical Clinical I–III | ⚠ see below |

⚠⚠ **The STS294x rows are the sharpest illustration.** In batch 94 I published the **PSAV** surgical
technology clinical rotations (STS0255L, STS0256L, STS0257L — 723 hours, the core of the certificate)
because they carry `L` suffixes. **The parallel college-credit rotations STS2944C/2945C/2946 are the same
required clinical sequence** and were skipped purely because they are numbered 29xx. **The same programme
component was published in one track and skipped in the other, on number shape alone.**

The rest of the 44 do look like genuine shells (a large block of "INDIVIDUAL STUDY" at 2905, plus
externships and bridge/transition placeholders), so this is a targeted correction, not an unpicking of
the rule.

**What I'd do if you say yes:** screen all 44 against the refined test (fixed content + prerequisites or
corequisites + stable title across institutions), un-skip the ones that pass, and report the list before
writing any of them.

---

### 7. `PHT1006C` — ✅ CLOSED 2026-09-03: resolved and published (informational)

**Closed.** The guide was built and pushed in batch 117 at 3 cr / 60 hrs, with both contact-hour figures stated. Daytona State does publish it — as **PHT1006 (Introduction to Physical Therapy)**, without the C suffix. The standing 404-on-C rule applies; the queue row is buildable and is scheduled in the remaining work. No decision needed.

| | |
|---|---|
| **Status** | 🔎 Blocked since 2026-09-03 (batch 92) — no decision needed, just visibility |
| **Now** | `queued`, with the ruled-out catalogs recorded in its `notes` field |
| **Institutions** | 2 (per the statewide inventory) |

"Role of PTA with Lab" is the one course standing between the PHT prefix and completion. **Not found** in
Seminole State, Polk State, or Gulf Coast State catalogs; **NWFSC returned 403** and **Santa Fe College
returned an empty body**. Two targeted searches did not surface it.

I deliberately did **not** price it off the PHT C-form family, because **PHT2221C broke that exact pattern
in the same batch** (3 cr, not the 4 cr that PHT1128C and PHT2220C share). That would have been a guess
dressed as an inference.

**No action needed from you** — I'll retry NWFSC (403s are usually bot filters) and try other holders as
they come up. Listed here so it is visible rather than buried in a batch report.

---

### 8. Six requirement-placeholder shells skipped (scope decision — bundle with the 9xx re-screen)

| | |
|---|---|
| **Status** | ⏸ Skipped 2026-09-03; revisit with item 6 |
| **Rows** | `ENC2998A`, `ENC2999A`, `COM2998B`, `COM2999B`, `SPC2999A`, `SSI2997A` |
| **Proposed** | Leave skipped; resurrect via the Request a Curriculum Guide feature if anyone asks |
| **Risk if left** | None — these are not real courses |

Daytona State's catalog pages for these carry **only a number, a placeholder title, and a credit value**
— no description, no prerequisites, no terms. The titles are administrative stubs: *"English"*,
*"Communicatn Req"*, *"Speech Requirmt"*, *"Social Sci Req"*. **Verified by fetching ENC2998A**, which the
catalog returns as a bare placeholder.

These are **transfer/requirement placeholders**, structurally the same as the 9xx shells already skipped,
and a guide for one would have nothing to describe. Marked `skipped` with a note rather than deleted, so
the Request a Curriculum Guide feature can resurrect them. **Grouped here with item 6 so both scope calls
can be settled together.**

### 9. Split-family `C`-suffix rows with no UWF coverage — ✅ **RESOLVED 2026-09-04 (batch 124)**

**Ron's decision:** *"write the lecture halves as orphan additions, and continue with queue."*

**Done, and the rule is now set for the rest of the UWF build.**

**EEL (batch 124).** All 11 UWF lecture/laboratory halves written as orphan additions and pushed —
`EEL3111`, `EEL3211`, `EEL3211L`, `EEL3472`, `EEL3701`, `EEL4635`, `EEL4657`, `EEL4712`, `EEL4713`,
`EEL4744`, `EEL4744L`. The 11 superseded rows were then marked `skipped`, each with a note naming the
pair that covers it. **`EEL4610` was skipped as genuine no-coverage** — UWF has no equivalent.
**EEL is now the first prefix to close with zero residue: 33 pushed, 11 skipped, 0 queued.**

**The standing rule, for PCB / MLS / NUR and every prefix after:**

1. When a queued `C`-suffix row has no UWF entry, check whether UWF publishes the **split family**.
2. If it does, **write the UWF halves as orphan additions** — `reconcile` picks them up automatically
   (`+N orphan draft(s) added to queue`) and `--push-from-queue` pushes them; the API creates the course
   record on demand, so no server work is needed.
3. **Then mark the `C` row `skipped`** with a note naming the covering pair.
4. If UWF publishes **no equivalent at all**, skip as no-source-coverage.

**ANT closed under the same rule (same session).** All six ANT `C`-rows turned out to have their UWF
halves already published — `ANT2100`, `ANT2511` + `ANT2511L`, `ANT3520`, `ANT4115`, `ANT4525` +
`ANT4525L`, `ANT4586` — so **no new writing was needed**; all six were marked `skipped` with a note
naming the covering course. **ANT: 48 pushed, 6 skipped, 0 queued.**

**Both prefixes worked so far now close with zero residue.** The rule is proven and carries forward.

## Standing retry list (no decision needed)

Sources that failed in a way that looks temporary. I retry these opportunistically.

| Source | Failure | First seen |
|---|---|---|
| `fldoe.org` | 403 | long-standing |
| `floridastatecollegecatalog.fscj.edu` | **TLS certificate expired** — distinct from a bot filter | batch ~90 |
| `catalog.nwfsc.edu` | 403 | batch 92 |
| `catalog.sfcollege.edu` | empty response body | batch 92 |

---
## 10. ⚠⚠⚠ `MAN4350` / `MAN4320` — a number COLLISION needing a decision (batch 138)

**The problem.** The statewide inventory and UWF assign different subjects to `MAN4350`, and the subjects
permute across two numbers:

| Number | Statewide inventory | UWF |
|---|---|---|
| `MAN4320` | Human Resource Recruitment and Selection (13 inst) | *not published* |
| `MAN4350` | Training and Development (13 inst) | **Recruitment and Selection** |

UWF folds training and development into `MAN4341 Performance Management` instead.

**Why it needs your decision.** The standing `-SCNS` / `-<INST>` rule assumes one number carrying two
subjects. **This is two numbers whose subjects have swapped**, so the fix may need pages on both. Options:

1. **Treat as a normal split** — publish `MAN4350-SCNS` (Training and Development) and `MAN4350-UWF`
   (Recruitment and Selection) plus a disambiguation page, and leave `MAN4320` alone. Simplest; ignores
   half the permutation.
2. **Treat as a paired split** — do the above *and* cross-reference from `MAN4320`, so a student on either
   number is warned. More complete; more pages.
3. **Leave as published** — the live `MAN4350` guide already carries a prominent collision table naming
   both subjects and both numbers, which may be sufficient.

**Currently:** option 3 is in effect. `MAN4350` and `MAN4341` both carry the collision table.
`MAN4320` is already `pushed` in the master queue and has not been revisited.

**Needs from you:** which option, and whether the `-SCNS` half should wait for the SCNS catalog (as the
NUR cases do).

## 11. ⚠⚠ `MAN4720` — live guide missing UWF's residency and permission requirement (batch 138)

**Found while writing MAN batch 138.** UWF's catalog entry for its BSBA capstone `MAN4720 Strategic
Management` states: **"Senior status and permission is required. Must be taken at UWF."**

**The live guide contains none of this** — verified against the published API response: no match for
residency, senior status, or permission language. It is also **the only "permission is required" marking
anywhere in the MAN prefix**.

**Why it was not fixed unilaterally.** `MAN4720` is a **32-institution** guide, not a UWF-specific one. A
residency clause that is true of UWF is not necessarily true of the other 31, so inserting it could
introduce a different error.

**Options:**
1. **Add a general note** — capstone courses commonly carry residency and senior-standing requirements;
   check your own institution. Safe, less specific. *(The general version is already in the ten new MAN
   guides' shared transfer block.)*
2. **Add a UWF-specific example** citing UWF's wording as an instance of the general pattern. More useful,
   and consistent with how other institution-specific facts appear in multi-institution guides.
3. **Leave as is.**

**Needs from you:** which option, and whether to sweep other already-live capstone guides for the same gap.

## 12. `BCN2405C` - RESOLVED 2026-09-04 (batch 141): title drift, not a subject split

**Question was:** the statewide inventory calls `BCN2405C` "Construction Mechanics" at 13 institutions, but
UWF carries `BCN 2405` *Statics and Strength of Materials* (no `C`) and a *separate* `BCN 3561`
*Construction Mechanics*. Three readings were possible - suffix family, sophomore/junior level pair, or a
genuine one-number-two-subjects split.

**Resolved by fetching four catalogs. It is reading 1 + 2 combined, and it is one subject:**

| Institution | Number | Title | Content |
|---|---|---|---|
| **UF** | `BCN2405C` | Construction Mechanics | "Structural behavior of loads resisting members in buildings. Properties of structural materials." Beams, columns, frames, trusses; axial stress, strain, shear and moment diagrams, deflection. Text: Limbrunner & D'Allaird, *Applied Statics and Strength of Materials* |
| **FGCU** | `BCN2405C` | Construction Mechanics | structural behaviour, properties of structural materials, load-resisting members |
| **UWF** | `BCN2405` | Statics and Strength of Materials | statics of particles, rigid bodies, friction; strengths of wood, steel, concrete |
| **Gulf Coast** | `BCN2405` | Statics and Strength of Materials | statics, shear, bending moments, deflection, moments of inertia, beam and column design |

Two statewide titles for one course. `BCN3561` at UWF is the upper-division level partner - the same
EGN2312 <-> EGN3311 pattern already documented for statics. **Published as one guide** covering both titles,
3 credits / 60 contact hours, with the level-pair and the engineering-boundary warnings in Special
Information. **No `-SCNS` / `-<INST>` split needed.** No decision required from Ron; recorded here because
the question was raised here.

**New accreditation hook found:** UF maps every learning outcome in this course to **ACCE** (American
Council for Construction Education) student learning outcomes - the construction-management analogue of
ABET/FE, and the same "programme accreditation outranks course credit" structure already documented for
nursing, MLS and teacher preparation.

## 13. BLOCKED - four civil/environmental prefixes are missing from the taxonomy (batch 142)

**Found by a push failure, then confirmed by a full queue sweep.** `CES4702C` was drafted, validated clean
and pushed; the server returned **HTTP 422**. The draft is fine - the cause is that the server cannot
resolve the course prefix.

`ExtractCoursePrefix` scans the letters up to the first digit, looks up a taxonomy leaf with that key, and
creates the course under it. **`CES` has no taxonomy node**, so the lookup fails and the guide is rejected.
`https://floridacourserepo.com/api/v1/courses/CES4702C` returns `COURSE_NOT_FOUND`, as does the bare
`CES4702`.

### The sweep: this blocks 14 queued courses, not one

Comparing every `queued` row against the 597 three-letter leaf keys in
`PreseMakerRepo.Api/Data/Seed/taxonomy.json`:

| Prefix | Queued rows blocked | SCNS meaning |
|---|---|---|
| **ENV** | 6 | Environmental Engineering |
| **CWR** | 3 | Civil Engineering: Water Resources |
| **CEG** | 3 | Civil Engineering: Geotechnical |
| **CES** | 2 | Civil Engineering: Structures |

**All four belong to the same parent**, which already exists and already has siblings:

```
"key": "CIVIL_ENVIRONMENTAL_",  "name": "Civil/Environmental Engineering",
  children: [ CCE  "Civil Construction Engineering",
              CGN  "Civil Engineering",
              TTE  "Transportation Engineering" ]
```

So the fix is four leaf nodes added to one existing parent - suggested names: **CES** "Civil Engineering:
Structures", **CEG** "Civil Engineering: Geotechnical", **CWR** "Civil Engineering: Water Resources",
**ENV** "Environmental Engineering".

### Two ways to apply it - Ron's call

1. **Admin taxonomy editor** (`/admin`, added in `a5d6886`). If it can create leaf nodes, this needs **no
   redeploy** and I can retry the push immediately afterwards.
2. **Edit `taxonomy.json` + redeploy.** `TaxonomySeed` is idempotent and runs at startup, so adding the
   four nodes and deploying picks them up. This is the durable fix and should happen either way, so that
   the seed file and the live database agree.

**Status:** `CES4702C` is sitting at `status=error` in `queue.csv` with its draft file intact and validated.
**Nothing needs rewriting** - once the node exists, `python generate_guide.py --push-draft CES4702C --yes`
completes it. The other 12 blocked rows are still `queued` and will hit the same 422 when they come up.

**Needs from you:** add the four nodes (either route), then tell me and I will push CES4702C and re-check.

## Resolved

*(Nothing yet — items move here with the date and what was decided.)*
