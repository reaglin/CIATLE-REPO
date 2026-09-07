# Review queue — decisions waiting on Ron

Items the guide pipeline surfaced that **need a human decision before I act**. I add to this file as
findings come up and update the status line when a decision lands. Nothing here is blocking the batch
loop; the loop continues around them.

Two kinds of item live here:

- **Correction candidates** — a guide is already live and I have evidence it is wrong or incomplete.
  Republishing overwrites live content and bumps the version, so it waits for a go-ahead.
- **Scope decisions** — the skip list, queue membership, and similar calls that are Ron's to make.

**Last updated:** 2026-09-05 (batch 148)

---

## ⭐ DECISION LIST — everything awaiting Ron, in one pass

Ron asked (2026-09-05) for the open items collected so they can be reviewed together. **This is the index;
the detail is in the numbered sections below.** Items are ordered by how much they unblock.

### A. Blocking work right now

| # | Item | The ask | What it unblocks |
|---|---|---|---|
| **13** | **Four taxonomy nodes missing** (`CES`, `CEG`, `CWR`, `ENV`) | Add four leaf nodes under the existing `CIVIL_ENVIRONMENTAL_` parent — via the admin taxonomy editor (no redeploy) and/or `taxonomy.json` + deploy. Copy-paste JSON is in `Deployment/PENDING_SERVER_CHANGES.md`. | **`CES4702C` (written, validated, sitting at `status=error`) plus 13 more queued rows.** Nothing else in the pipeline is blocked. |

### B. Scope calls — whole course families, cheap to decide, large effect on the queue

| # | Item | The ask | Notes |
|---|---|---|---|
| **15** | **`MUN` ensembles** (`MUN3313 Concert Choir`, 9 inst, + siblings) | In scope or skip? | Audition-based participation; repertoire set per term by the director. **But** batch 148 established that ensemble credit is *not* interchangeable with methods-course credit, so these are genuinely distinct from the `MV*` applied instruction already skipped. |
| **16** | **`PEL`/`PEM`/`PEN` activity courses** (`PEL1341 Beginning Tennis`, 9 inst, + siblings) | In scope or skip? | Physical activity instruction. Unlike applied music these have defined statewide skill outcomes, so a guide is writable — the question is whether it is worth writing. |
| **17** | **`MVV4640 Vocal Pedagogy`** | Confirm it stays in scope. | Held back deliberately when the 40 applied-music rows were skipped (batch 144): it carries the voice prefix but is a **classroom course about teaching singing**, not studio instruction. Currently still `queued`. |
| **5, 6, 8** | The pre-existing scope items (`PHT2931`; re-screen the skipped 9xx rows; six requirement-placeholder shells) | Unchanged from before this session. | **Item 6 remains the highest-value item on this page.** |

### C. Correction candidates — live guides, need a go-ahead before republishing

| # | Item | The ask |
|---|---|---|
| **10** | `MAN4350` / `MAN4320` number collision | Two-number treatment — how? |
| **11** | `MAN4720` missing UWF residency/permission requirement | Which of three options; and whether to sweep other live capstone guides |
| **14** | **`PUR3000`** split candidate | Split into `-SCNS` / `-UWF` / bare, or leave as one guide? **Better evidenced than the other candidates** — UF *and* FGCU confirm the majority reading from their own catalogs, so unlike the NUR cases this does not need the SCNS catalog to proceed. |
| **1, 2, 3, 4** | `ETI4448`, `RTE2563C`, `EET1025C`, `TPP2118`/`TPP2119` | Unchanged from before this session. |

### Closed since this list was started

**12** `BCN2405C` — resolved without needing a decision (title drift, not a subject split; published as one
guide, batch 141). **7** `PHT1006C` and **9** split-family `C`-suffix rows — closed earlier.

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
| `fldoe.org` | 403 (Akamai) — **re-confirmed batch 153**; matters beyond one batch, it is the primary source for every PSAV curriculum framework | long-standing |
| `floridastatecollegecatalog.fscj.edu` | **TLS certificate expired** — distinct from a bot filter | batch ~90 |
| `catalog.nwfsc.edu` | 403 | batch 92 |
| `catalog.sfcollege.edu` | empty response body | batch 92 |
| `www.pensacolastate.edu/coursesearch.php` | 213-byte stub for every query — JS-driven | batch 154 |
| `catalog.phsc.edu`, `catalog.mdc.edu` | connection failure (curl 000) | batch 154 |
| `catalog.palmbeachstate.edu` | connection failure (curl 000) | batch 155 |
| `www.unf.edu/catalog/courses/?level=ug` | 200 / 151 KB but **nav chrome only**, client-side rendered. Lead: `digitalcommons.unf.edu/course_catalogs/` | batch 153 |

**✅ Recovered — do not treat as blocked:** `catalog.broward.edu/course-descriptions/<prefix>/` returned
full content again in **batch 154** after being recorded as bot-blocked on 2026-09-04. Second
regression-then-recovery for Broward. **Re-probe at session start rather than assuming either state.**

---

## 18. `ASC1610C` — cannot be sourced, not a decision (batch 154) — *informational*

Queue row is **`ASC1610C` "Aircraft Systems and Components"** (BC;FSCJ;MDC;NWFSC;PHSC;PSC;UWF).
**Broward — the only reachable institution — lists `ASC1610` WITHOUT the `C`**, titled *Aircraft Engines,
Structures, and Systems*, 3 credits. UWF has no `ASC` prefix at all.

Open question: same course under a suffix disagreement, or two different courses? **No second reachable
source exists to settle it** — PSC is JS-only, PHSC and MDC fail to connect, NWFSC is 403, FSCJ needs a
numeric id. Left `queued`, no draft written, **no decision needed from Ron** — this is a sourcing block
that clears itself when one of those catalogs comes back. Retry alongside the standing list above.

---

## 20. ⚠⚠ `LAE3314` — a split candidate where UWF holds the MINORITY reading (batch 156)

**Statewide title: "Children's Literature." UWF's LAE 3314: "Literacy for the Emergent Learner."**

Not variant wordings. Children's literature is the study of a body of literature — genres, history,
authors, selection, reader response. UWF's course is early-literacy *instruction* — development from birth
through primary grades, phonological awareness, word identification, fluency, comprehension. **Different
disciplines; they do not substitute in either direction.**

**Confirming evidence from inside UWF's own catalog:** UWF carries **`LAE 5468` "Literature for Children
and Young Adults"** at graduate level — so UWF does teach the children's-literature subject, under a
different number. The divergence is real, not a catalog abbreviation.

**⚠ What makes this different from every prior split candidate: UWF is the outlier.** In ISM4320, PUR3000
and the rest, UWF's reading was one of two live readings. Here the statewide title reads Children's
Literature across CC, FAMU, FLAC, FSWSC, KU and SFSC, and UWF stands alone. **Publishing a single guide
from the UWF description would put the minority subject under a number most institutions use for something
else** — exactly the trap the split rule exists to prevent.

**Action taken:** pulled from batch 156, **no draft written**, row left `queued`. Sourcing attempted and
failed for the majority reading — FGCU has no LAE3314, Broward's `lae` page 404s, Chipola fails to
connect, South Florida State has no per-prefix course route, FSW is still an empty 202.

**What I need from you:** this is the case the **SCNS catalog** you offered would settle. With it I can
write `LAE3314-SCNS` (children's literature), `LAE3314-UWF` (emergent literacy) and the bare-number
disambiguation page. Without it, writing the `-SCNS` half would be inventing content, which the rule
forbids.

---

## 19. Should the C-suffix contact-hour rule be restated? (batch 154) — *low priority*

The working rule from batches 149–151 is **"C dominant → 60 hours; C minority → 45."** It was applied to
CES4702C (kept 45), COP2830C (changed to 60) and TPA2000C (kept 45).

**`BOT4503C` was published at 60 in deliberate departure from it.** By institution count the split form is
the majority (BOT4503L is listed at four institutions), so the rule says 45 — but **FGCU's catalog documents
BOT4503C as genuinely integrated lecture+lab**, and UWF's split form carries a real 1-credit lab with a
material fee. Publishing 45 would have described a lab-bearing course as a lecture.

**Suggested restatement:** *the deciding question is whether the `C` form documentably carries a lab, not
how many institutions use the suffix.* Institution count is a proxy to fall back on when the catalog is
silent. **No action needed unless you want the rule changed in `CLAUDE.md`** — flagging it because the two
readings will keep diverging.

---

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

## 14. `PUR3000` — a split candidate with an unusually clear majority (batch 144)

**Found while writing PUR3000.** Two Florida institutions confirm the statewide reading and one teaches a
different subject under the same number.

| Institution | Title | What it actually covers |
|---|---|---|
| **UF** | Principles of Public Relations | "Nature and role of public relations in a democratic society, activities of public relations professionals... ethics and professional development... Emphasizes management functions and developing effective public relations strategies." Prereq: sophomore standing |
| **FGCU** | Principles of Public Relations | "An introduction to the field and study of public relations. Explores the history of the profession, the nature of public relations, its established code of ethics, and the responsibilities and duties of public relations professionals." Prereq: ENC1102 |
| **UWF** | **Introduction to Public Affairs** | "How communication shapes the relationship between government, nonprofit organizations, the media, and the public... strategic messaging, advocacy, and public relations in influencing policy debates... how public affairs professionals communicate with diverse audiences, manage issues, and represent organizational interests in the public sphere." No prereq listed |

**Why this is a stronger candidate than most on the list.** Public affairs is a *subfield* of public
relations, so the overlap is real — but a UWF student completing PUR3000 will not have covered the history
of the profession, the four-step PR process, media relations, campaign planning, or corporate and agency
practice, which is the entire substance of the course at UF and FGCU. **And the next course in the sequence
assumes them**: FGCU makes PUR3000 the explicit prerequisite for PUR3100 (PR Writing), and UWF has its own
PUR3100 (*Writing for Public Relations*).

**Unlike most entries in the open-cases table, the majority reading here is confirmed at two institutions,
not inferred** — so a `-SCNS` guide would not be written from a title alone. That removes the usual blocker
recorded for the NUR cases.

**Published as a single guide** (the UF/FGCU subject), with the divergence quoted at the top of the Course
Description and repeated in Special Information under transfer risk. Added to the open-cases table in
`Tools/CLAUDE.md`.

**Needs from you:** whether to split this one into `PUR3000-SCNS` / `PUR3000-UWF` / `PUR3000`. It is a
better-evidenced candidate than the ART/HSC/PCB entries already on the list, and unlike the NUR cases it
does not need the SCNS catalog to proceed.

## 15. `MUN` ensemble numbers — scope decision (batch 147)

**Surfaced by** `MUN3313 Concert Choir` (9 institutions) reaching the head of the queue, with other `MUN`
numbers behind it.

**Why it is a question.** These are performing-ensemble courses: students audition, rehearse and perform,
and the repertoire is chosen by the director each term. In that respect they resemble the `MV*` applied
studio instruction already skipped (batch 144, 40 rows) — a statewide guide cannot say what the content
will be.

**Why it is not obviously the same thing.** Batch 148 turned up a relevant distinction while writing
`MUE4480`: **participating in an ensemble under an `MUN` number is not the same as the methods course, and
programmes do not accept ensemble credit for methods requirements.** Ensembles carry real, assessable
musicianship outcomes — sight-reading, blend, intonation, rehearsal literacy — and they are degree
requirements every term in music degrees, not electives. A guide could usefully cover audition
expectations, the every-term requirement, how ensemble credit accumulates, and the Florida MPA structure,
without pretending to know the repertoire.

**Needs from you:** skip the `MUN` family, or write them with that framing?

## 16. `PEL` / `PEM` / `PEN` activity courses — scope decision (batch 147)

**Surfaced by** `PEL1341 Beginning Tennis` (9 institutions) reaching the head of the queue.

Physical activity instruction. These differ from applied music in that they have **defined skill outcomes**
that are reasonably stable statewide — a beginning tennis course teaches the same strokes everywhere — so a
guide is genuinely writable. The question is whether it is worth writing: they are typically 1 credit,
elective, and carry no articulation complexity.

**Needs from you:** in scope or skip? If skipped, the same bulk-mark treatment used for `MV*` applies.

## 17. `MVV4640 Vocal Pedagogy` — confirm scope (batch 144)

Held back deliberately when the applied-music family was skipped. It carries the `MVV` voice prefix but is
a **classroom course about teaching singing** — pedagogy, vocal anatomy, repertoire selection for students —
not individual studio instruction. Left `queued` rather than assumed.

**Needs from you:** confirm it stays in scope (I write it), or skip it with the rest of the prefix.

## 21. Two documented sources DISAGREE on credits — confirm the tie-break rule (batch 163)

**Surfaced by** `MUE3311 Public School Music`, where **FGCU documents 3 credits and UWF documents 2** for
the same SCNS number. This is the first case in the project where two catalogs give different credit
values for the *same* number and both are legible sources — previous credit questions were "one source, is
it right?" rather than "two sources, which one?"

**What I did, pending your call.** Published at **3**, on two grounds:

1. FGCU documents 3 for **this same number**, and 3 is the national norm for a course of this scope.
2. **UWF's music department applies 2-semester-hour values broadly** — its conducting, form-and-analysis
   and instrumentation courses are all 2 — so the 2 reads as a **departmental convention** rather than a
   statewide value for this particular course.

The guide states **both** values prominently and says which it used, per the standing "show the
disagreement" rule.

**The general question, which is what actually needs deciding.** When two catalogs disagree on credits:

- **(a) Publish the majority/national norm** and flag the outlier — what I did here.
- **(b) Publish the lower value**, on the conservative reasoning that a student who plans for fewer credits
  is never short.
- **(c) Publish neither number as authoritative** — state the range in the guide and set the JSON to the
  more common value purely as a required field.

**Note this is not hypothetical going forward:** the same UWF 2-hour convention produced `MUT4311` at 2
credits this batch, where **FGCU's equivalent course is 3 but carries a different number** (MUT3311), so
the tie-break did not apply and UWF governed by default. **A rule here would settle a recurring music-prefix
case and any others like it.**

### ⚠ Update (batch 164): a SECOND case, and it resolves the OPPOSITE way under the same rule

`PSY2023 Careers in Psychology` — **FSU and FGCU both document 1 credit; UWF documents 3.** Published at
**1**, i.e. the *lower* value, where MUE3311 took the *higher*. **Both were decided by rule (a) — majority
of documented sources — which is evidence that (a) is the rule that generalises**, since it handled two
cases that pull in opposite directions without special pleading. In both, UWF was the outlier.

**A transfer consequence surfaced that applies to every case of this kind:** a student who completes a
1-credit version and transfers where 3 is required is **short two credits toward the requirement**, even
though the number is identical and the credit transfers automatically. **Credit transfers; credit *hours*
do not multiply.** Whatever rule you pick, the guides should keep stating both values so a student can see
the gap coming.

**Needs from you:** (a), (b), (c), or something else.

## 22. ⚠ `MUT4311` / `MUT3311` — a NUMBER divergence, which defeats articulation (batch 163) — *informational*

Recording the pattern rather than asking for a decision. **FGCU teaches this course as `MUT3311`
"Orchestration and Arranging" (3 cr); UWF and the statewide inventory use `MUT4311` (2 cr at UWF).** Same
subject; the digit is a level marker (3 = junior, 4 = senior).

**Why it belongs on your radar: SCNS equivalency operates on the NUMBER.** A title drift still articulates
automatically; **a number divergence does not** — a student moving between those two institutions needs a
departmental course substitution. This is a *third* distinct transfer-risk pattern alongside the
one-number-two-subjects splits and the suffix cases, and **it is invisible to anything that matches on
course code.**

**Relevant to the career-pathways feature** (`CAREER_PATHS_PLAN.md`): a pathway assembled by number would
silently drop FGCU students out of an orchestration requirement they have in fact completed. Logged in
`SOURCES.md` batch 163. **No action needed now** — flagged so the pathway data model accounts for it.

## Resolved

*(Nothing yet — items move here with the date and what was decided.)*
