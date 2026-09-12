# Review queue — decisions waiting on Ron

Items the guide pipeline surfaced that **need a human decision before I act**. I add to this file as
findings come up and update the status line when a decision lands. Nothing here is blocking the batch
loop; the loop continues around them.

Two kinds of item live here:

- **Correction candidates** — a guide is already live and I have evidence it is wrong or incomplete.
  Republishing overwrites live content and bumps the version, so it waits for a go-ahead.
- **Scope decisions** — the skip list, queue membership, and similar calls that are Ron's to make.

**Last updated:** 2026-09-11 (batch 191)

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

## 23. ⚠ "Tradition divergence" — a new drift category, two instances in consecutive batches — *informational*

Recording a pattern, not asking for a decision yet. **Two courses one batch apart turned out to carry one
subject taught through two different scholarly methodologies**, with titles that give no hint of it:

| Number | Version A | Version B |
|---|---|---|
| `PHI3130` Logic (batch 171) | UWF **"Modern Logic"** — symbolic: propositional + predicate calculus, natural deduction | FGCU **"Logic"** — critical reasoning: categorical logic, **fallacies**, argument reconstruction |
| `SPC4540` Persuasion (batch 172) | FSU **"Persuasion"** — social-scientific: attitude change, ELM, experimental evidence | UWF **"Propaganda and Persuasion"** — rhetorical/critical: campaigns, movements, advertising |

**Why this is its own category.** It is not a one-number-two-subjects split (both really are logic; both
really are persuasion), and it is not ordinary title drift (the content genuinely differs). It sits
between them: **same subject, different methodology, and the descriptions differ in their VERBS rather
than their NOUNS** — "theories tested against evidence" versus "explores how it works". The reliable tell
is the **assigned textbook**, which belongs unambiguously to one tradition (Perloff vs Jowett &amp; O'Donnell;
a symbolic-logic text vs a critical-thinking text).

**Handling so far:** single guide, comparison table in Special Information, and outcome subsections
per version. That treatment works and both guides are live. **Credit articulates either way**, so there is
no transfer damage — the cost is a student enrolling expecting one and getting the other.

**Why it is on your radar:** two instances in consecutive batches from unrelated prefixes suggests this is
common rather than exceptional, and **it is invisible to any matching on number or title**. Likely places
to meet it again: research methods, ethics, media studies, and anywhere a subject is taught in both a
social-science and a humanities department. Relevant to `CAREER_PATHS_PLAN.md` for the same reason item 22
is. **No action needed now.**

## 24. ⚠ `PHI3500` / `PHI4500` — another number divergence, and this one is deliberate (batch 172) — *informational*

Second instance of the item-22 pattern. **FSU numbers metaphysics `PHI4500`; FAMU, FIU, UF, UNF and UWF
use `PHI3500`.** Same subject, same description in substance.

What makes this one worth adding rather than just logging: **FSU's degree requirements show the choice is
deliberate.** `PHI 4500 Metaphysics` sits under "Contemporary Metaphysics and Epistemology" alongside
`PHI 3300 Knowledge and Belief` — so FSU places metaphysics a level above epistemology while the other
five institutions place them side by side at 3000. **The number is carrying a curricular judgement**,
which is why these divergences persist instead of being corrected toward each other.

**Consequence is the same as item 22:** SCNS articulates on the number, so a student moving to or from FSU
files a substitution. Noted prominently in the live guide. **No action needed.**

## 25. ⚠⚠⚠ `TPA3230C` — THREE subjects under one number, and nobody uses the suffix (batch 173) — **NEEDS A DECISION**

**Pulled from batch 173, not written.** This is the most severe divergence this project has found, and it is the
first with **three** readings rather than two.

| Institution | Code carried | Title | What it teaches |
|---|---|---|---|
| **Statewide (SCNS)** | `TPA3230C` | **Costume Design** | — |
| UWF | `TPA3230` (no C) | **Costume Construction** | patterning, cutting, fitting, draping, construction |
| FSU | `TPA3230` (no C) | **Costuming I** | costume sewing; "the craft of sewing costumes for theatre" |
| FGCU | `TPA3230` (no C) | **Costume Design** | "theoretical and practical approach to costume design including make-up" |
| FIU | `TPA3230` (no C) | **Costume History** | "Fashion from Ancient to Modern Times in correlation to society and theatrical styles" |

**Three genuinely different subjects.** Construction/sewing (UWF, FSU) is a majority of 2; design (FGCU)
matches the statewide title; history (FIU) matches nothing. **Construction versus design is not a variant —
it is the real professional division in this field**: the draper/technician builds, the designer conceives,
and they are different jobs with different career paths. UWF underlines the point by placing design
separately at `TPA4045`/`TPA4046`.

⚠ **A second, independent problem: no institution carries the `C` suffix.** All four carry bare
`TPA3230`. The queued ID `TPA3230C` may not correspond to a course that currently exists anywhere — which
means even a correctly written guide might be filed under a code nobody can match.

**Why I did not just write it.** Following the `LAE3314` precedent (item 20): writing a single guide would
publish one subject under a number that means something else at three of the four institutions, and the
statewide title points at the reading held by only one of them. **The `-SCNS` / `-<INST>` rule was designed
for two subjects and does not obviously extend to three.**

**Options as I see them:**

- **(a)** Publish a **disambiguation page at the bare number** plus per-subject guides — the split rule
  generalised to three (`TPA3230-SCNS`, `TPA3230-UWF`, `TPA3230-FIU`, or similar). Most faithful, most work.
- **(b)** Publish **one guide covering all three readings explicitly**, as was done for `CLP4302`. Cheaper,
  and it worked there — but `CLP4302` had two readings, not three.
- **(c)** **Resolve the suffix first.** If `TPA3230C` is a dead code, the queue row may simply be wrong and
  should be replaced with `TPA3230`.
- **(d)** Skip it.

**Needs from you:** which of these, and whether the suffix question changes the answer. **Row left `queued`
with an explanatory note**, so it will not be silently re-picked.

## 26. ⚠⚠ `PUR4801` — pulled from batch 173; the collision CLAUDE.md predicted, now confirmed from the other side

`CLAUDE.md` already flagged this: *"The project will meet this again from the other side when PUR4801 comes
up in the queue."* It came up. **I pulled it rather than writing it, and I think that was right, but it is
your call.**

**What the sources show:**

- **Statewide `PUR4801` = "Public Relations Cases"** (FAMU, UCF, UNF, USF, UWF).
- **UWF's `PUR4801` = "Public Relations Campaigns"** — a capstone, *"applying communication and public
  relations research and theory for a real client"*, prereq (COM 3003 OR PUR 3000) AND PUR 3100.
- **FGCU numbers the campaigns capstone `PUR4800`** ("PR Campaigns/Capstone"); **FSU also carries `PUR4800`,
  not `PUR4801`**; **FIU carries `PUR4800`** ("P.R. Campaigns").
- ⚠ **`PUR4800C` "Public Relations Campaigns" (7 institutions, including UWF) is ALREADY PUBLISHED here.**

**So writing `PUR4801` from UWF alone would republish, under a different number, a subject this repository
already covers — while leaving the subject four other institutions actually teach under that number
(Public Relations Cases) undocumented.** That is the `LAE3314` failure mode exactly.

⚠ **One extra piece of evidence worth having:** UWF's own catalog says *"Credit may not be received in both
PUR 4801 and PUR 4802."* So UWF runs two campaigns-capstone numbers as alternates, neither of which is the
statewide reading.

**Needs from you:** (a) write `PUR4801` as *Public Relations Cases* from a non-UWF source once one is
reachable (UCF/UNF/USF are all currently unfetchable — this is the blocker); (b) treat it as a
`-SCNS`/`-UWF` split; or (c) skip. **Row left `queued` with an explanatory note.**

## 27. ⚠⚠ `MMC4601` — statewide says "Video Game Analysis", UWF teaches minorities and mass media (batch 177)

**Pulled from batch 177, not written.** Third instance of the `LAE3314` shape, and the starkest yet.

| | Statewide (SCNS) | UWF |
|---|---|---|
| Title | **VIDEO GAME ANALYSIS** | **Minorities and the Mass Media** |
| Institutions | FAMU, FIU, STU, UWF | — |
| Subject | — (not sourceable) | *"Concerns of mass media as they pertain to minority issues; review of mass media portrayals of minorities; problems of minority access to mass media; prospects for mass media and cultural diversity."* |

**These are not two wordings of one subject.** Game studies and media representation of minority groups are
different fields with different literatures.

**Why I pulled it rather than writing it.** Writing from UWF alone would publish one subject under a number
that means something else at three other institutions — the `LAE3314` failure mode exactly. **And unlike
`COM3003` (batch 175, split completed), the `-SCNS` half is NOT sourceable**: the FIU Coursedog cache has no
description for this number, and FAMU and STU are unreachable.

**Needs from you:** (a) hold until a source for the statewide reading is reachable, then split as `COM3003`
was; (b) publish the UWF reading alone with a prominent warning; or (c) skip. **Row left `queued` with an
explanatory note.**

⚠ **Worth noting the pattern across three batches:** `LAE3314`, `PUR4801` and now `MMC4601` are all cases
where **UWF holds a minority reading and the majority reading cannot be sourced.** `COM3003` was the one case
where it could be, and that one got split immediately. **The binding constraint on executing your split rule
is source reachability, not judgement** — which is why the Coursedog recoveries in batch 173 matter beyond
the courses they directly unlocked.

## 28. ⚠⚠ A CLASS of held rows: `C`-suffixed ids that no reachable institution carries — **ONE DECISION COVERS THREE (batches 173–178)**

**Three rows are now held for the same reason, and holding them one at a time is not serving you.** Asking
once, about the class, is better.

| Row | Statewide id &amp; title | What institutions actually carry |
|---|---|---|
| `TPA3230C` | Costume Design | **UWF, FSU, FGCU, FIU all carry `TPA3230`** (no `C`) — and three different subjects |
| `COP3014C` | Programming 2 | **UWF carries `COP3014`** (no `C`), "Algorithm and Program Design"; FAMU/FAU unreachable |
| `INP3004C` | Industrial Psychology | **UWF and FIU both carry `INP3004`** (no `C`); FIU 3 cr, "Intro. Ind/Org Psy" |

**The pattern is systematic, not coincidental.** In each case `courses_2plus_institutions.csv` records a
`C`-suffixed number that **no institution I can reach actually uses**. Combined with the five
institution-list errors already documented (batch 176), the likeliest explanation is that **the inventory
reflects the SCNS catalog rather than current institutional offerings** — SCNS may well hold a `C`-suffixed
number that institutions have since dropped or never adopted.

⚠ **`TPA3230C` is different from the other two and should stay held regardless** — it has a genuine
three-way subject divergence (item 25), which is a separate problem from the suffix.

**For `COP3014C` and `INP3004C` the subject is NOT in doubt.** Programming 2 and industrial/organisational
psychology are consistently described everywhere they appear. **Only the suffix is questionable.**

**Options as I see them:**

- **(a)** **Write them at the queued `C` id**, with a prominent note that the reachable institutions carry
  the bare number. The guide is findable at the id the queue and any SCNS-derived system uses, and the
  student is warned. **My recommendation for `COP3014C` and `INP3004C`.**
- **(b)** **Write them at the bare number** (`COP3014`, `INP3004`) and skip the `C` rows. Matches reality;
  loses anyone searching the `C` id.
- **(c)** **Write both** — a full guide at the bare number and a short pointer at the `C` id. Most complete,
  most work, and the mechanism already exists (it is what the `COM3003` disambiguation page does).
- **(d)** Keep holding.

**Needs from you:** one choice, applied to the class. **All three rows are left `queued` with explanatory
notes.** ⚠ **This will keep recurring** — the inventory has ~400 rows left and `C` suffixes are common.

## 29. ⚠ Retro-sweep candidate: ~a dozen live guides record UWF's Gordon Rule labels without explaining them (batch 179) — *low urgency, your call*

**Not a correction — an incompleteness.** Batch 178 identified the Gordon Rule; batch 179 established that
**UWF's two catalog labels are its two halves**:

- *"Meets College-Level **Communication** Skills Requirement"* = the **writing** component
- *"Meets College-Level **Computation** Skills Requirement"* = the **mathematics** component

**Guides written before batch 179 faithfully recorded whichever label UWF carried and correctly said the
designation is institution-specific and may not transfer — but did not say what the designation IS, and did
not state the grade consequence.** Affected guides include (at least) `PHH3400`, `PHI3130`, `PHI3400`,
`PHI3800`, `ARH4470`, `MHF3202`, `AML3604` and `INR4102`.

⚠ **What the reader misses:** that **a C− does not satisfy a Gordon Rule course at most institutions.** A
student who read one of those guides learned the course carried a designation; they did not learn that
passing it below C would fail to satisfy the requirement it was designated for.

**Options:** (a) sweep them on a version bump when convenient; (b) leave them — they are incomplete, not
wrong, and new guides now handle it; (c) sweep only the ones most likely to be taken FOR the requirement
(the 2000-level and general-education ones).

**Needs from you:** whether to spend a batch's worth of effort on the sweep. **My recommendation is (c)** —
the general-education courses are where students actually rely on the designation. **Nothing is blocked
either way; new guides already state it.**

## 30. ⚠⚠ Ten queue rows are blocked by MISSING TAXONOMY NODES, not by content (batch 182) — *needs a server change*

**Confirmed 2026-09-08 by retrying `CES4702C`** (the standing one-line retry): still **HTTP 422**. The cause
is now pinned down — the taxonomy seed has **no node for the prefixes `CES`, `CWR`, `CEG` or `ENV`**:

```
grep -c '"CES"' PreseMakerRepo.Api/Data/Seed/taxonomy.json   -> 0
```

`TTE`, `ASC`, `MUN`, `PEL`, `MVV` and `MUG` all return 1, so those rows are workable.

**Rows blocked:** `CES3100C`, `CES4605C`, **`CES4702C` (status=error, draft written and validated)**,
`CWR3201C`, `CWR4202C`, `CEG3011C`, `CEG4801C`, `ENV3001C`, `ENV4351`, `ENV4514C`.

⚠ **These sit at the HEAD of the priority order**, which is why the queue's top has not moved for several
batches and each batch has to reach further down. They are civil, water-resources and environmental
engineering — a coherent block, and exactly the kind of content the repository's engineering audience wants.

**Needs from you:** whether to add the four taxonomy nodes (a `taxonomy.json` edit plus a deploy, since
`TaxonomySeed` is idempotent and runs at startup). **Once deployed, `CES4702C` pushes with a one-line
retry and the other nine become writable.** **My recommendation: yes** — it is a small server change that
unblocks ten priority rows.

## 31. ⚠ `CJE3674C` joins the C-suffix class decision (item 28) (batch 182)

Queued as **`CJE3674C`**; **UWF carries bare `CJE 3674` "Introduction to the Forensic Sciences"**, no suffix.
Three of the four inventory institutions are private (Keiser and two others). **Fourth member of the class
covered by item 28**, alongside `TPA3230C`, `COP3014C` and `INP3004C`. **Pulled from batch 182 rather than
guessing at the id.**

⚠ Also recorded for whenever it is written: UWF's entry carries an exclusion — *credit may not be received
in both `CJE 3674` and `CJE 3670`.*

**Needs from you:** nothing new — this is another instance of item 28, and the recommendation there
(write at the queued `C` id with a note) still stands.

## 32. ⚠ `BSC1050` published from the only reachable catalog, which holds the NARROWER subject (batch 182) — *informational, no action needed*

Statewide title **Environmental Science**; **UWF's is Fundamentals of Ecology** — a component of it, not a
synonym. **Three of four institutions are private or small colleges outside catalog reach**, so UWF is the
only verified description.

**Published as a single guide from UWF's reading with a divergence block at the top**, per the `EEX4474`
precedent — writing an environmental-science guide from the statewide title alone would be inventing
content. **Added to the open-cases table in `CLAUDE.md`.**

⚠ **Likely cause worth knowing:** the number sits on a prefix boundary. Florida numbers introductory
environmental science **`EVR1001`** and majors-level ecology **`PCB3043`**; a non-majors course spanning both
lands in the general `BSC` prefix and leans whichever way the institution does.

**Flagging it only so you know a live guide carries a narrower subject than its statewide title implies.**

## 33. ⚠⚠ The C-suffix class (item 28) now has SEVEN members — it is systematic, not anomalous (batch 183)

Three more queued `C` ids were found where **no institution carries the suffix**:

| Queued id | What institutions actually carry |
|---|---|
| **`CTS4348C`** | UWF `CTS 4348` "Linux System Administration"; FIU `CTS 4348` "Unix Sys Admin" |
| **`DAA2204C`** | UF bare `DAA 2204`; FIU bare `DAA 2204` |
| **`EEE3396C`** | UWF bare `EEE 3396`; UF bare `EEE 3396` |

**Full class: `TPA3230C`, `COP3014C`, `INP3004C`, `CJE3674C`, `CTS4348C`, `DAA2204C`, `EEE3396C`.**

⚠ **Seven rows is no longer a handful of anomalies.** It is consistent with the inventory recording SCNS
catalog identifiers rather than institutional offerings. **A single decision on the class unblocks all
seven.** The recommendation in item 28 — **(a) write at the queued `C` id with a note** — still stands, and
these three are all cleanly sourced and ready to write the moment it lands.

⚠ `CTS4348C` is worth doing first: UWF's prerequisite is `COP 4634 OR COP 4610 OR CGS 3763`, and this
repository published **`CGS3763` in batch 181** — the guides would link.

**Needs from you:** the item 28 decision. Nothing else is blocked by it.

## 34. ⚠⚠ `DAA2204C` also carries a SEQUENCE-POSITION divergence (batch 183) — needs a decision beyond the suffix

| Source | Title |
|---|---|
| Statewide | **Ballet I** |
| UF | **Contemporary Ballet Practices 1** |
| **FIU** | ⚠⚠ **Ballet Tech II** — *"Continuation of Ballet Techniques I…"* |

**Statewide and UF number this as the FIRST course in the sequence; FIU numbers it as the SECOND.**

⚠ **Ninth sequence-position divergence and the most consequential kind**: a student who took `DAA2204`
elsewhere and transfers to FIU is placed a level away from where they were taught — **and in a technique
course, level placement is the whole point.**

**Needs from you:** whether this row should be written at all once item 28 is decided, or held. **My
recommendation: write it, and lead with the placement warning** — the divergence is exactly the thing a
student needs told, and no other source will tell them.

## 35. ⚠ `EUH3570` — chronological divergence found, sourcing done, row deferred (batch 183) — *informational*

| Source | Title | Span |
|---|---|---|
| Statewide | **Modern Russia** | — |
| **UWF** | **Russia to 1917** | ⚠ **ends where "modern" begins**; `EUH 3576` "Soviet Union since 1917" is the partner course |
| **FIU** | **Russian History** | *"from the time of tribal Slavs until today"* — the whole span in one course |

**Three different chronological scopes under one number.** ⚠ A student taking the statewide "Modern Russia"
at UWF gets **pre-1917 Russia**, which is close to the opposite of what the title promises.

**No decision needed** — the row is queued and workable, and the sourcing is recorded here so it is not
re-derived. **Flagging it because a live guide written from the title alone would have been wrong.**

## 36. ⚠ `GRA3112C` and `GRA4154C` — sourcing failure, not a suffix problem (batch 184) — *informational*

Both were probed and pulled from batch 184. **Neither appears at UWF (no `gra` catalog entry), at UF, in
FSU's art bulletin, or in the FIU cache** — and the inventory lists FAU, FSU, UCF, UNF and UWF between
them, none of which publishes a fetchable description for these numbers.

⚠ **Deliberately NOT added to the C-suffix class (items 28 and 33)** — the problem here is that no catalog
answered, not that the `C` is spurious. **They remain queued and workable if a source opens up.**

**Studio art courses are a systematic gap**: the institutions that carry them are the ones whose catalogs
this project cannot currently reach. **Worth noting if a new source ever becomes available.**

## 37. ⚠ Gordon Rule retro-sweep (item 29) — the case has strengthened (batch 184) — *no new decision needed*

**Six live guides now carry the full Gordon Rule explanation** (`ENG3010`, `ECO3303`, `PHI4633` and three
earlier), against roughly a dozen older ones that record UWF's label without saying what it is or that a
C-minus does not satisfy it.

⚠ **The label keeps appearing** — it has now surfaced in three of the last four batches, across English,
economics, philosophy and criminal justice prefixes. **The gap between the newer and older guides is
widening rather than closing.**

**Nothing is blocked**; new guides handle it correctly. **Recommendation from item 29 stands: option (c),
sweep the general-education and 2000-level ones only.** Flagging only that the population of correct guides
is now large enough to make the inconsistent older ones more visible.

## 38. ⚠⚠ `SPC4680` — split candidate: UWF holds the MINORITY reading again (batch 185)

| Source | Title | Subject |
|---|---|---|
| Statewide | **Rhetorical Criticism** | analysis of rhetorical texts |
| **FSU** | **Methods of Rhetorical Criticism** | *"methods for the practice of doing criticism of rhetorical discourse… Aristotelian, Metaphor, narrative, post-modern, and cultural approaches to the analysis of texts"* |
| **UF** | **Rhetorical Criticism** | confirmed |
| **UWF** | ⚠ **Rhetoric, Media, and Civic Life** | applied — leadership, advocacy, civic engagement, media change |

⚠⚠ **Second case where UWF holds the minority reading**, after `LAE3314` (item 20) — **and the strongest,
because FSU and UF agree with each other AND with the statewide title.**

**Published as a single guide written to the majority (methods) reading, with UWF's emphases as a labelled
variant, and a two-column syllabus test so a student can tell which version they are in.**

⚠ **Why it may deserve a split rather than a warning:** **a methods course and an applied advocacy course
are different preparations.** **The methods version is what graduate programmes in rhetoric expect as a
writing sample and as background**; the applied version prepares for public affairs and advocacy work.
**A transfer student moving between them has a real gap, in one direction or the other.**

**Needs from you:** whether this joins the split queue. **My recommendation: treat it as a stronger `PUR3000`
— a genuine candidate, below `LAE3314` in urgency because both readings are legitimate upper-division
rhetoric courses and neither leaves a student with nothing.**

## 39. ⚠ `RTV3511` — THREE production courses under one number; craft divergence (batch 185) — *informational, published with a warning*

| Source | Title | Craft |
|---|---|---|
| Statewide / **UWF** | Video Storytelling | **single-camera FIELD production** |
| **FIU** | Video Studio Production | **multi-camera STUDIO production** |
| **UF** | Fundamentals of Production | general foundation |

⚠⚠ **Field and studio production are different crafts** — different equipment, crew roles, job titles and
failure modes. **A graduate trained on one does not walk into the other.**

**Published as a single guide following the statewide/UWF reading, with the studio material as a labelled
variant and an instruction to ask what equipment the section uses.**

⚠ **Also captured for the record: FIU gates this course on five prerequisite courses AND a 2.85 cumulative
GPA.** **Production sequences run on fixed rotations, so a miss delays a degree by a year rather than a
term.**

**No decision needed** — flagging it because **if the split queue is ever worked, this is a stronger case
than several already in the open-cases table**, and the sourcing is done.

## 40. ⚠ `PHY3220` — credit-count divergence, a shape with no identifier signal (batch 185) — *informational*

**UWF lists this course at 4 semester hours; the statewide title and most institutions carry 3.**

⚠ **No laboratory, no second registration — the same course with a different credit value.** **Unlike the
split-family, suffix and phantom-`C` cases, nothing in the identifier signals it.**

**Consequence:** a transfer student is a credit short or long against a degree requirement, and **physics
degrees have tight credit budgets, so it surfaces in the final audit.** **The guide states the credit value
explicitly and tells the reader to check their own.**

⚠ **Worth knowing for the queue generally: if credit counts diverge silently on one number, they will on
others.** **The inventory carries no credit field, so this is only ever visible from a catalog.**

## 41. ⚠ `SCE4320` — scope divergence against a BANDED certification (batch 186) — *informational*

| | Title | Range |
|---|---|---|
| Statewide | **Special Methods: Middle Grades Science** | middle grades |
| **UWF** | **Teaching Science in Middle and Secondary Schools** | ⚠ **6–12** |

⚠⚠ **This matters more than ordinary title drift because Florida science certification is banded.**
**Middle Grades General Science 5–9 and the secondary single-subject certificates (Biology, Chemistry,
Physics, Earth-Space 6–12) are different certificates with different subject-area examinations** — **so a
methods course aimed only at middle grades may not fully serve a secondary candidate.**

**Published with the scope difference stated in the guide and in the prerequisite field.** ⚠ **Also an
inventory error: FSU is listed and its teacher education bulletin carries no `SCE 4320`.**

**No decision needed** — recorded because **methods courses are the least portable coursework in a teacher
preparation programme**, and this is the first case where a title divergence maps onto a certification
boundary rather than onto content.

## 42. ⚠ Prerequisite strings are approaching the 500-character server limit (batch 186) — *process, no decision needed*

**`SCE4320` failed the validator at 546 characters** — the first blocking failure in eleven batches.
⚠ **Three of the last twelve prerequisite strings have landed within 30 characters of the ceiling**
(`PHY3220` at 499, `CLP4110` at exactly 500 in batch 181, `PHI4633` at 493).

**Cause: the prerequisite field has become the place where the most consequential warnings go**, because it
is what a queue reader and the course page show first — concurrency traps, exclusions, GPA gates,
screening deadlines, accreditation warnings.

✅ **RESOLVED as a decision — Ron directed 2026-09-08 that the ceiling be raised in the next site publish.**
**A full development note is now in `Deployment/PENDING_SERVER_CHANGES.md`**: raise `Prerequisites` from
**500 to 1000** in BOTH `PublishValidators.cs` and the EF column configuration (the latter needs a
migration — SQLite tolerates the widened column, PostgreSQL will not), plus the client-side mirror in
`validate_drafts.py` and the limits tables in `Tools/CLAUDE.md` and the `/guide` skill.

⚠ **Also flagged in that note:** the `/guide` skill's limits table still records `contact_hours` as
**0–300** when the server has been **0–1500** since the PSAV fix — worth correcting in the same pass.

**Nothing is blocked in the meantime**: `validate_drafts.py` catches over-length strings before the push,
and guides continue to be written to the 500-character limit until the change deploys.

## 43. ⚠ `TTE3004C` — ninth member of the C-suffix class, with sourcing already done (batch 187)

**UWF carries bare `TTE 3004`; FSU carries bare `TTE 3004`.** ⚠ **Neither has the `C`.**

**Class now stands at nine**: `TPA3230C`, `COP3014C`, `INP3004C`, `CJE3674C`, `CTS4348C`, `DAA2204C`,
`EEE3396C`, `GIS4035C`-adjacent cases aside, and now **`TTE3004C`**.

⚠ **Sourcing is complete and recorded so it is not re-derived when the class decision lands:**

| Institution | Emphasis | Prerequisites |
|---|---|---|
| **UWF** | transportation modes, interaction between modes, facility design, planning, economics, public policy | `EGS 3441*` |
| **FSU** | ⚠ highway and traffic engineering, planning and design, construction, operation, management, safety | `CEG 2202`, `CEG 2202L`, `STA 2122` |

⚠ **A real emphasis divergence — systems-and-policy versus highway-and-traffic — worth a labelled variant
section when the row is written.** **`TTE` has a taxonomy node, so unlike the CES/CWR/CEG/ENV cluster this
row is pushable the moment the suffix question is settled.**

**Needs from you:** nothing new — this is another instance of item 28.

## 44. ⚠ `PHZ3151C` — sourcing failure, left queued (batch 187) — *informational*

**Computational physics.** ⚠ **Not at UWF despite being listed** (nineteenth inventory error), **and FAU,
Florida Polytechnic and UCF publish no fetchable descriptions.**

⚠ **Deliberately NOT added to the C-suffix class** — the problem is that no catalog answered, not that the
suffix is spurious. **Left queued and workable if a source opens up.**

**Same shape as `GRA3112C`/`GRA4154C` (item 36): a small cluster of rows whose institutions are exactly the
ones this project cannot currently reach.**

## 45. ⚠⚠⚠ `APK4200` — a full one-number-two-subjects case; strongest split candidate since `CLP4302` (batch 188)

| Source | Title | Subject |
|---|---|---|
| Statewide / **FIU** | **Motor Development** | how movement skills are acquired across the lifespan |
| **UWF** | ⚠⚠ **Neuromechanics of Human Movement** | how the nervous system produces and controls movement |

⚠⚠ **Different fields, not different emphases.** **Different literatures, different prerequisites, different
professional audiences** — motor development for teachers, adapted-activity specialists and early childhood
professionals; neuromechanics for exercise scientists, biomechanists and rehabilitation science.

⚠ **The prerequisite settled it before the descriptions did**: **UWF gates on `APK 3110L`, an exercise
physiology LABORATORY.** **No developmental course requires that.**

⚠⚠ **The concrete harm is checkable and specific: a student who needs motor development for a Florida
teaching or adapted-physical-activity certification and takes the neuromechanics course has not covered the
required material, and the transcript will not show it.**

**Published as one guide covering both readings in labelled sections, with the divergence leading the
prerequisite field.** **Added to the open-cases table.**

**Needs from you:** whether this joins the split queue. ⚠ **My recommendation: yes, and high in it** —
**this is a cleaner case than several already in the table, because a named certification requirement is at
stake rather than an emphasis a student might not notice.**

## 46. ⚠⚠ `APK2105C` — the BSC/APK prefix divergence, now evidenced from a catalog line (batch 188) — *informational, but the highest-stakes row written*

**CLAUDE.md has recorded this as "the most damaging case found" since batch 179.** ⚠ **UWF's own
prerequisite is the evidence: `APK 2100C` OR `BSC 1085/L` OR `APK 2100/L`.**

**The institution treats the prefixes as equivalent for its own admission — which is not the question.**
⚠⚠ **Nearly every competitive Florida health-professions programme writes its prerequisite list naming
`BSC` numbers, because that is what most Florida College System institutions teach.** **A student completing
the `APK` sequence holds an equivalent course under a number the application form does not list.**

⚠ **Compounded by a split family**: UF carries integrated `APK 2105C`; UWF requires `APK 2105L` as a
separate co-requisite registration — **and health prerequisites specify A&P WITH LABORATORY.** **Two
independent transfer problems on one number.**

**The guide's instruction is procedural**: get the target programme's published list, ask admissions in
writing if the prefix differs, save the reply, keep the syllabus — **before the sequence, because the fix
afterwards is two more semesters.**

**No decision needed.** ⚠ **Flagging it because this is the row most likely to prevent a real, expensive
mistake, and because `APK2100C`, `APK2100L` and `APK2105L` are still in the queue** — **the same warning
belongs on each of them.**

## 47. ✅ The APK anatomy-and-physiology family is COMPLETE (batch 189) — *informational, closes part of item 46*

**Item 46 flagged that the `BSC`/`APK` prefix warning belonged on `APK2100C`, `APK2100L` and `APK2105L` as
well as `APK2105C`.** ✅ **Done.**

| Guide | Status |
|---|---|
| `APK2000C` gateway survey | ✅ batch 189 |
| `APK2100C` A&P I integrated | ✅ earlier — **checked live, already carries the warning** |
| `APK2100L` A&P I laboratory | ✅ batch 189 |
| `APK2105C` A&P II integrated | ✅ batch 188 |
| `APK2105L` A&P II laboratory | ✅ batch 189 |

**All five carry the prefix warning and the register-for-both-halves warning, and they cross-reference each
other.** ⚠ **The split-family rule executed deliberately rather than incidentally**, as with
`BCH3033`/`BCH3033L`/`BCH3034`.

**No decision needed.** ⚠ **`APK2105L`'s prerequisite line is now the repository's cleanest evidence for the
prefix problem** — UWF stating in its own catalog that `APK 2100C`, `BSC 1085/L` and `APK 2100/L` are
interchangeable — **and the guides are explicit that an institution accepting either prefix for its own
admission is a different question from a nursing programme accepting `APK` on a form that names `BSC`.**

## 48. ⚠ `APK3220C`, `APK4114C`, `APK4600C` — sourcing failures, left queued (batch 189) — *informational*

**None is at UWF** — ⚠ **two of them list UWF in the inventory** (nineteenth through twenty-first
discrepancies) — **and UF publishes a title only for `APK3220C`, with UCF, USF and Florida Polytechnic
unreachable.**

⚠ **Deliberately NOT added to the C-suffix class (items 28, 33, 43)** — the problem is that no catalog
answered, not that the suffix is spurious.

**Same shape as `GRA3112C`/`GRA4154C` (item 36) and `PHZ3151C` (item 44).** ⚠ **That set is now seven rows
across four prefixes, and it will not shrink without a new source** — **worth noting collectively, because
individually each looks like an anomaly and together they are a coverage gap.**

## 49. ⚠⚠⚠ SCNS is now scriptable — this **retires several open items and enables a retro-sweep** (EEE sweep, 2026-09-09)

**`flscns.fldoe.org` is fully queryable** via `Tools/scratchpad/scns.py`: an ~80 MB flat file of every
course at every Florida institution, and a per-prefix statewide description CSV. Details in
`SOURCES.md` Tier 3.

**Why this needs Ron's attention rather than just a note:** it changes what several standing items are
waiting on.

| Open item | What SCNS now supplies |
|---|---|
| **Item 30** — 10 rows blocked by missing taxonomy nodes (`CES`, `CWR`, `CEG`, `ENV`) | Unaffected — still a server-side change. |
| **Items 28 / 33 / 43** — the **C-suffix class** (does the queued `C` id exist anywhere?) | ⚠⚠ **Answered mechanically now.** The flat file lists the exact suffixed id per institution. **The whole class can be resolved in one pass instead of case by case.** |
| **Item 29 / 37** — **Gordon Rule retro-sweep** | ⚠⚠ `gordon_rule` and `gordon_writing` are **data fields** in the flat file, plus the five gen-ed category flags. **No more inferring designation from UWF label text.** |
| **Items 36 / 44 / 48** — the **seven sourcing-failure rows** across four prefixes | ⚠ **Partly answered.** `scns.py institution <PREFIX> <id>` returns an institution's own catalog text — a route into schools that are bot-blocked or have no static pattern. Worth re-trying all seven. |
| **`-SCNS` split halves marked "⏸ needs catalog"** (`NUR4286`, `NUR4826`, `LAE3314`) | ⚠⚠ **Unblocked.** `Tools/CLAUDE.md` records that a `-SCNS` guide needs the state's definition and that Ron would need to supply it. **The statewide CSV is that definition** — description, prerequisites, corequisites, transferability. |

**Decision needed from Ron:** which of these to run, and in what order. My recommendation, cheapest and
highest-value first:

1. **Resolve the C-suffix class (items 28/33/43)** — one pass over the flat file settles nine rows.
2. **Write the three blocked `-SCNS` halves** (`NUR4286`, `NUR4826`, `LAE3314`) now that the source exists.
3. **Gordon Rule retro-sweep** — mechanical, and it corrects roughly a dozen already-published guides.
4. **Re-try the seven sourcing-failure rows** through the institution report.

---

## 50. ⚠⚠⚠ `courses_2plus_institutions.csv` overstates institution counts systematically — **retro-sweep candidate** (EEE sweep, 2026-09-09)

The inventory's institution list has been described as *"a HYPOTHESIS, not evidence — five confirmed
errors in four batches."* **The EEE sweep makes it much worse than that, and identifies the mechanism.**

**10 of 29 queued EEE courses were single-institution in SCNS** while the inventory claimed 2–4
(`EEE3396C` 4→1, `EEE4314C` 3→1, `EEE4351C` 3→1, `EEE4376C` 3→1, `EEE4260C` 2→1, `EEE4306C` 2→1,
`EEE4309C` 2→1, `EEE4330` 2→1, `EEE4377` 2→1, `EEE4450` 2→1). That is **a third of the prefix.**

**The mechanism is now certain:** the inventory counts institutions carrying the **bare or
differently-suffixed** number against the **suffixed** id. It records the SCNS *catalog*, not current
*offerings*.

⚠⚠ **Why this matters beyond accuracy.** Institution count drives two things in this project:
**queue priority** (`priority = 1000 - num_inst`) and **the hedging level a guide is written at**
(8+ institutions = confident; 2–3 = explicit hedging; 1 = treat as a custom guide). **Both have been
wrong wherever the count was inflated** — courses have been prioritised above their real reach, and
some single-institution courses have been written with more confidence than the evidence supports.

**Decision needed from Ron:**

- **(a) Correct the inventory in place** — regenerate `num_inst` for all rows from the flat file. Mechanical,
  one pass, and fixes priority ordering going forward. ⚠ Will reshuffle the queue order noticeably.
- **(b) Leave the inventory and check per-course at drafting time** — no disruption, but the priority
  ordering stays wrong and it depends on the drafter remembering.
- **(c) Correct the inventory AND audit published guides** that asserted an institution count. Largest
  effort; the only option that fixes already-live text.

**My recommendation: (a) now, (c) opportunistically** — regenerate the counts so priority and hedging are
right going forward, and correct published assertions when a guide is next touched for another reason.
A standalone audit of ~2,196 pushed guides is not proportionate, but a wrong count in a *published* guide
is a factual error, so it should be fixed whenever one is revisited.

---

## 51. ⚠⚠ `EEE4306C` and `EEE4309C` — statewide records that contradict what is taught (EEE sweep) — *informational, published with warnings*

Two cases where the SCNS statewide record and the teaching institutions disagree, handled under the
batch-183 rule (**two agreeing catalogs outrank a statewide title**) and recorded here because they are
evidence that the statewide *titles* are less reliable than the statewide *descriptions*.

- **`EEE4306C`** — statewide title *Semiconductor Devices I*, description device physics. **UF and UWF
  both teach *Electronic Circuits 2***. Wrote to the institutions; recorded the divergence in the guide
  so an evaluator reading the statewide title is not misled.
- **`EEE4309C`** — UCF's *Electronics II* is **digital/mixed-signal**; the statewide description for that
  number is **analogue**. ⚠ **A UCF graduate with "Electronics II" on the transcript has not covered
  feedback amplifier theory in a second-course treatment.** Published with a two-column syllabus test.

**No decision needed** unless Ron wants the `-SCNS`/`-<INST>` split applied to either. **My reading is
that neither warrants a split**: for `EEE4306C` no institution teaches the statewide reading, so a
`-SCNS` page would describe a course nobody offers; for `EEE4309C` the divergence is of emphasis within
second-course electronics rather than of subject. Both are flagged in-guide instead.

---

## 52. ✅ Item 30 RESOLVED — the seven missing taxonomy prefixes are added (2026-09-09) — *needs a deploy*

`PreseMakerRepo.Api/Data/Seed/taxonomy.json` now carries all seven prefixes that had active
undergraduate courses but no node, so pushes to them will no longer return **HTTP 422**:

| Prefix | Name | Placed under |
|---|---|---|
| `CEG` | Civil Geotechnical Engineering | `CIVIL_ENVIRONMENTAL_` |
| `CES` | Civil Engineering Structures | `CIVIL_ENVIRONMENTAL_` |
| `CWR` | Civil Water Resources | `CIVIL_ENVIRONMENTAL_` |
| `EES` | Environmental Engineering Science | `CIVIL_ENVIRONMENTAL_` |
| `ENV` | Engineering: Environmental | `CIVIL_ENVIRONMENTAL_` |
| `ETE` | Education: Technology Education | `EDUCATION__CAREER_TE` |
| `EVT` | Education: Vocational/Technical | `EDUCATION__CAREER_TE` |

Placement was taken from the **SCNS discipline code**, not guessed: all five civil prefixes are
discipline **028**, the same as the `CCE`/`CGN`/`TTE` already under that node; `ETE` and `EVT` are
discipline **025**, the same as `ECT`/`ECW`. Names are SCNS's own prefix names. The diff is **28
insertions, 0 deletions** — purely additive, no reformatting.

⚠ **A full statewide audit was run, so this is now known to be complete**: these were the *only*
seven prefixes in the entire SCNS catalog with active undergraduate courses and no taxonomy node.

**⚠ ACTION FOR RON: this takes effect on the next deploy.** `TaxonomySeed.UpsertNodeAsync` is a
true per-node upsert with no "table already populated" early return, so the new nodes insert against
the existing production database — no reset, no migration. **Until it is deployed, the 196
outstanding civil/environmental engineering courses remain unpushable**, and that is now the single
largest blocker to the engineering-first direction.

---

## 53. ✅ Item 50 RESOLVED — inventory counts regenerated from SCNS; **the C-suffix mechanism is proven** (2026-09-09)

`courses_2plus_institutions.csv` has been regenerated against the SCNS flat file. **3,442 of 16,650
rows had a wrong `num_inst` or institution list — 20% of the inventory.**

| Result | Rows |
|---|---|
| Already correct | 13,151 |
| **Overstated** | **3,255** |
| Understated | 164 |
| No active SCNS record (left untouched) | 80 |

⚠⚠⚠ **949 rows overstated by three or more institutions**, and the mechanism is now proven rather
than inferred:

| Course | Inventory claimed | SCNS actual | The bare number |
|---|---|---|---|
| **`ACG2071C`** | **44** | **1** (Valencia) | `ACG2071` = **45** |
| `ACG2021C` | 39 | 3 | `ACG2021` = 39 |
| `CES4605C` | 9 | 1 | — |
| `TPA3230C` | 5 | 1 | — |

**The inventory assigned the BARE number's institution count to the C-suffixed id.** `ACG2071C` is
the clean proof: 45 institutions carry `ACG2071`, exactly one carries `ACG2071C`, and the inventory
recorded 44 against the suffixed row.

⚠⚠ **This is the same defect behind the C-suffix class (items 28, 33, 43).** Those items ask whether
a queued `C` id is carried by anybody; **the flat file answers it directly for every one of them, and
the answer is now in the inventory.** Item 33 called the class "systematic, not anomalous" — it is,
and this is why.

**Consequences already applied:**

- **Queue priorities re-derived** for `queued` rows (`priority = 1000 - num_inst`). 63 rows moved;
  manual sub-929 tiers (faculty requests) were preserved, and `pushed`/`skipped` history was not
  rewritten. ⚠ **The head of the queue changed materially** — `CES4605C` was the top item at a
  claimed 9 institutions and has **one**; `CWR3201C` and `CWR4202C` went 9 → 2.
- ⚠ **Hedging level in already-published guides is the part NOT fixed.** The hedging rules key off
  institution count (8+ confident, 2–3 explicit hedging, 1 custom guide), so guides written against
  an inflated count may be more confident than the evidence supports. `EEE3308C`, published before
  this session, is a concrete instance: **1 institution (UF), not the 4 the inventory claimed.**
  Per the item-50 decision this is fixed opportunistically when a guide is next touched, not by a
  standalone audit of 2,196 pages.

---

## 54. ⚠ Thirteen published guides are for courses SCNS marks DISCONTINUED (2026-09-09) — *needs Ron's view*

Cross-checking the inventory against the flat file surfaced **80 inventory rows with no active SCNS
record — all discontinued, none fabricated**. Of those, **13 already have published guides**:

`APK4119C`, `COS0009C`, `DAA1500C`, `EGN1006C`, `MUT1122C`, `MUT2126C`, `MUT2127C`, `OTA0030C`,
`OTA0040C`, `OTA0041C`, `OTA0043C`, `OTA0631C`, and one further row.

⚠ **This is not necessarily an error.** The project deliberately uses DSC's archived catalogs for
discontinued courses (Tier 0, 2026-09-02), and `Tools/CLAUDE.md` notes that older transcripts still
carry content under superseded numbers — so a guide for a discontinued course can genuinely serve a
student holding that credit.

**The question for Ron is whether these pages should say so.** A student reading a guide for
`OTA0041C` has no way to know the course is no longer offered anywhere in Florida.

**Options:**

- **(a) Add a discontinued banner** to those 13 pages — a short block stating that SCNS records the
  course as discontinued, that it may still appear on older transcripts, and pointing at the current
  equivalent where one exists. **My recommendation**; it is 13 pages and it converts a silent
  inaccuracy into useful information.
- **(b) Leave them** — the content is still correct about what the course *was*.
- **(c) Unpublish** — my view is that this is wrong: the guides serve exactly the students least well
  served elsewhere.

⚠ **Going forward, the flat file makes this checkable before drafting** — `status != 'A'` is one
field. Worth adding to the pre-draft checks alongside the taxonomy-prefix check.

---

## 55. ⚠⚠⚠ `CET2620` — **FIVE different subjects under one number**, and the cause is a vendor curriculum change (batch 190)

**The most severe number divergence found so far — worse than `TPA3230C` (three subjects), because there are
five and two of them are different FIELDS.**

| Institution | Its title for `CET2620` |
|---|---|
| State College of Florida, Manatee-Sarasota | **CCNA4 Connecting Networks** |
| St. Petersburg College | **Enterprise Core Technologies** |
| Santa Fe College | **Cisco Network Security** |
| Tallahassee State College | **The Internet of Things** |
| Hillsborough Community College | **Cisco Network Project Based Learning** |

⚠⚠ **The cause is documented and mechanical, which makes this the most explainable divergence in the
project.** Cisco replaced its **four**-course CCNA academy curriculum with a **three**-course one (Introduction
to Networks; Switching, Routing and Wireless Essentials; Enterprise Networking, Security and Automation). The
CCNA blueprint is now complete at the end of `CET2615`. **Florida's fourth number was left with no course to
hold, and each college filled the empty slot with something different.**

**Why it matters:** network security and the Internet of Things are different fields with different
laboratory equipment and different jobs. A transfer evaluator matching on the number cannot tell them apart,
and neither can an employer reading a transcript.

**What was done:** published as **one guide** with the table above at the top, a labelled optional-outcome
block per variant, and instructions to read the local course description before registering. **Not split**,
because the evidence is institutional TITLES from the SCNS flat file — no course descriptions were
reachable for four of the five.

**The ask:** (a) is a five-way split worth doing, and if so what does the bare number hold? (b) Cheaper
alternative — leave the single guide and treat this as the worked example of **vendor-driven divergence**,
a category distinct from institutional drift. ⚠ **Expect more of these wherever a course number is pinned to
a vendor certification track that the vendor then reorganises** (CompTIA, Microsoft, AWS, Cisco).

---

## 56. ⚠⚠ `CET1600` — a **VENDOR** divergence: five colleges teach Cisco, one teaches CompTIA (batch 190)

`CET1600`'s statewide definition explicitly names the **Cisco CCNA** track. Five of the six colleges follow
it. **Daytona State College titles the course "Network Plus"** — CompTIA's vendor-neutral **Network+**.

⚠ **A new category, adjacent to but distinct from subject divergence.** The *theory* overlaps almost
completely (OSI, media, topologies, IPv4 addressing, troubleshooting). **The hands-on skill does not**: a
Cisco section spends its laboratory time in the Cisco command line, which Network+ neither teaches nor
assesses. **And the student pays for the wrong exam voucher if they assume.**

**Published with a warning** telling the reader to confirm which examination their section prepares them for
before booking. **The ask:** is "which certification does this number target?" worth adding as a standing
check for every course whose statewide description names a vendor credential? There are many in `CET`, `CTS`,
`CIS` and `CNT`.

---

## 57. ⚠ `CET1112C` — republished as v1.1; **contact hours corrected 75 → 60** (batch 190) — *correction candidate, already acted on*

The live v1.0 guide (title *"Basic Digital Systems"*, pushed 2026-05-04 in the Daytona era) carried **75
contact hours** for a 3-credit integrated course, was **7 KB**, and had **no prerequisite string at all**.

**Replaced with an 18 KB v1.1** carrying: the five institutions and their differing titles from the SCNS flat
file; **Gulf Coast State College's verified prerequisite** (`MAC1105` **and** `EET1084C` with minimum grade C)
and its **spring-only** offering; the `CET1112`/`CET1112C` suffix divergence; and the BSEE/`EEL3701C`
articulation warning.

⚠ **The contact-hour change is derived, not sourced.** 60 hours is the project's standing convention for a
3-credit `C` course; the previous 75 was equally derived and is not supported by any catalog the project can
reach (Gulf Coast publishes the prerequisite and the description but **no hours**). **Flagging rather than
hiding it: if Ron prefers the higher figure, it is a one-line change.**

---

## 58. ⚠⚠ The site holds **133 courses whose `creditHours` are CLOCK HOURS** (batch 190) — *passed to the site session*

Measured against the live catalog: of the **806 guide-less courses**, **133 carry `creditHours` above 20**,
running as high as **667**. **132 of the 133 are PSAV `0xxx` courses** — the clock-hours-as-credits mistake
this pipeline guards against, sitting in production data. `contactHours` is **null on all 806**.

⚠ **It is also a blocker, not just a cosmetic fault:** the new course API caps `creditHours` at **20**, so
**those rows cannot be refreshed through `PUT /api/v1/courses/{id}` until the value is corrected.**

**Recorded in `Deployment/PENDING_SERVER_CHANGES.md`** with the prefix breakdown and two options (correct
them over the API while working each prefix — the cheap path, since every one of these courses needs titles
and offerings anyway — or a one-off migration). **No decision needed from Ron unless he prefers the
migration.**

---

## 59. ⚠⚠⚠ The queue holds the MINORITY form of several engineering courses — **needs Ron to queue the majority forms** (batch 191)

**The most actionable item in this file.** Working the queued civil-engineering rows revealed that for three
of them, the queue holds the id **almost nobody uses**, and the id most of Florida uses **is not in the queue
at all**:

| Queued and now written | Public institutions | Not queued, no guide | Public institutions |
|---|---|---|---|
| `CES4605C` | 1 | **`CES4605`** | **8** |
| `CES4702C` | 3 | **`CES4702`** | **8** |
| `CWR3201C` | 2 | **`CWR3201`** | **7** |

⚠ **Under the rule that guides are produced only from a queue, these will never be written unless they are
queued.** They are among the highest-coverage engineering courses in the state — steel design, reinforced
concrete design and fluid mechanics at every public engineering school in Florida.

**225 such courses** were found across the four prefixes this session touched, listed in
**`Tools/guideless_found.csv`** with institution counts and titles.

**The ask: which of them to add to `queue.csv`.** A reasonable first cut would be the 4-or-more-institution
rows, which is about a dozen courses and covers the entire structural and geotechnical core.

---

## 60. ⚠⚠ LEVEL divergence — a new category of number divergence (batch 191)

**The same subject at the 3000 level at some institutions and the 4000 level at others.** Instances found:

| Subject | 3000-level | 4000-level |
|---|---|---|
| Structural analysis | `CES3100C` (FGCU), `CES3100` (5 others) | `CES4100C` (UCF) |
| Soil mechanics | `CEG3011C` (FAU, FGCU, Florida Poly, UNF) | `CEG4011C` (UCF) |

⚠ **Two harms.** The transfer guarantee applies only between institutions sharing a number, so credit is
evaluated. **And the level digit has its own consequences** — programmes cap transferable upper-division
credit and impose residency minimums, so a course that is junior-level at one institution and senior-level
at another can disturb a credit count even where the content is accepted without argument.

**Published with a warning in both guides. No decision needed** unless Ron wants these treated as split
candidates; the content is genuinely the same, so a single guide with the warning looks right.

---

## 61. ⚠⚠ The prerequisite ceiling is now the normal failure, not an occasional one (batch 191)

**Five of six guides in this batch exceeded 500 characters on the first write** (531, 535, 537, 538, 515);
only one was clean. Batch 190 had one overflow. Batch 186 had the first.

⚠ **The overflowing strings were not padded** — they carried a credit divergence, a minority-suffix warning,
minimum-grade conditions and a major-restricted enrolment note, all of which a student needs before
registering. **The guides most worth reading are the ones whose prerequisite strings do not fit.**

**No decision needed from Ron** — the raise to 1000 characters is already queued in
`Deployment/PENDING_SERVER_CHANGES.md`. Recorded here as the evidence that it should ship in the next
release rather than drift.

---

## Resolved

*(Nothing yet — items move here with the date and what was decided.)*
