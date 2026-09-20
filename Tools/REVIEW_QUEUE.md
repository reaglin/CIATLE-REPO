# Review queue — decisions waiting on Ron

Items the guide pipeline surfaced that **need a human decision before I act**. I add to this file as
findings come up and update the status line when a decision lands. Nothing here is blocking the batch
loop; the loop continues around them.

Two kinds of item live here:

- **Correction candidates** — a guide is already live and I have evidence it is wrong or incomplete.
  Republishing overwrites live content and bumps the version, so it waits for a go-ahead.
- **Scope decisions** — the skip list, queue membership, and similar calls that are Ron's to make.

**Last updated:** 2026-09-11 (batch 196)

---

## ⭐ DECISION LIST — everything awaiting Ron, in one pass

⚠⚠ **This index is GENERATED — do not hand-edit it.** Add your item as a numbered
section below, then run `python review_index.py`. The index that used to live here was
maintained by hand and fell 30 batches behind, which defeated the point of the file.

**Ron, 2026-09-16:** *"Keep all unresolved in a file. Once we complete the queue I will be
looking at them."* — that is this table. **Nothing here blocks the batch loop**; the loop
continues around every one of them.

| | Count |
|---|---|
| ⏳ **Awaiting a decision from Ron** | **79** |
| Informational — recorded, no decision needed | 19 |
| ✅ Resolved | 10 |
| **Total items** | **108** |

---

### ⏳ Awaiting a decision (79)

| # | Item |
|---|---|
| **1** | `ETI4448` — scope gap on a capstone (correction candidate) |
| **2** | `RTE2563C` — credit mismatch and a missing sequence partner (correction candidate) |
| **3** | `EET1025C` — contact hours outside the family (correction candidate) |
| **4** | `TPP2118` / `TPP2119` — catalog prerequisites name a course DSC does not offer (verification candidate) |
| **5** | `PHT2931` — probably not a shell (scope decision) |
| **6** | Re-screen the skipped 9xx rows (scope decision) — ⬆ **the highest-value item here** |
| **8** | Six requirement-placeholder shells skipped (scope decision — bundle with the 9xx re-screen) |
| **10** | `MAN4350` / `MAN4320` — a number COLLISION needing a decision (batch 138) |
| **11** | `MAN4720` — live guide missing UWF's residency and permission requirement (batch 138) |
| **13** | BLOCKED - four civil/environmental prefixes are missing from the taxonomy (batch 142) |
| **14** | `PUR3000` — a split candidate with an unusually clear majority (batch 144) |
| **15** | `MUN` ensemble numbers — scope decision (batch 147) |
| **16** | `PEL` / `PEM` / `PEN` activity courses — scope decision (batch 147) |
| **17** | `MVV4640 Vocal Pedagogy` — confirm scope (batch 144) |
| **20** | `LAE3314` — a split candidate where UWF holds the MINORITY reading (batch 156) |
| **21** | Two documented sources DISAGREE on credits — confirm the tie-break rule (batch 163) |
| **25** | `TPA3230C` — THREE subjects under one number, and nobody uses the suffix (batch 173) — **NEEDS A DECISION** |
| **26** | `PUR4801` — pulled from batch 173; the collision CLAUDE.md predicted, now confirmed from the other side |
| **27** | `MMC4601` — statewide says "Video Game Analysis", UWF teaches minorities and mass media (batch 177) |
| **28** | A CLASS of held rows: `C`-suffixed ids that no reachable institution carries — **ONE DECISION COVERS THREE (batches 173–178)** |
| **29** | Retro-sweep candidate: ~a dozen live guides record UWF's Gordon Rule labels without explaining them (batch 179) — *low urgency, your call* |
| **30** | Ten queue rows are blocked by MISSING TAXONOMY NODES, not by content (batch 182) — *needs a server change* |
| **31** | `CJE3674C` joins the C-suffix class decision (item 28) (batch 182) |
| **33** | The C-suffix class (item 28) now has SEVEN members — it is systematic, not anomalous (batch 183) |
| **34** | `DAA2204C` also carries a SEQUENCE-POSITION divergence (batch 183) — needs a decision beyond the suffix |
| **37** | Gordon Rule retro-sweep (item 29) — the case has strengthened (batch 184) — *no new decision needed* |
| **38** | `SPC4680` — split candidate: UWF holds the MINORITY reading again (batch 185) |
| **43** | `TTE3004C` — ninth member of the C-suffix class, with sourcing already done (batch 187) |
| **45** | `APK4200` — a full one-number-two-subjects case; strongest split candidate since `CLP4302` (batch 188) |
| **49** | SCNS is now scriptable — this **retires several open items and enables a retro-sweep** (EEE sweep, 2026-09-09) |
| **50** | `courses_2plus_institutions.csv` overstates institution counts systematically — **retro-sweep candidate** (EEE sweep, 2026-09-09) |
| **54** | Thirteen published guides are for courses SCNS marks DISCONTINUED (2026-09-09) — *needs Ron's view* |
| **55** | `CET2620` — **FIVE different subjects under one number**, and the cause is a vendor curriculum change (batch 190) |
| **56** | `CET1600` — a **VENDOR** divergence: five colleges teach Cisco, one teaches CompTIA (batch 190) |
| **57** | `CET1112C` — republished as v1.1; **contact hours corrected 75 → 60** (batch 190) — *correction candidate, already acted on* |
| **58** | The site holds **133 courses whose `creditHours` are CLOCK HOURS** (batch 190) — *passed to the site session* |
| **59** | The queue holds the MINORITY form of several engineering courses — **needs Ron to queue the majority forms** (batch 191) |
| **60** | LEVEL divergence — a new category of number divergence (batch 191) |
| **61** | The prerequisite ceiling is now the normal failure, not an occasional one (batch 191) |
| **62** | `MUN3323` — the statewide title uses retired vocabulary; **a retro-sweep candidate for the MUN prefix** (batch 192) |
| **63** | `MUN3713` / `MUN4714` — UWF appears to use the two numbers in REVERSE (batch 192) |
| **65** | `ENV3001` / `ENV4001` — SCNS itself carries the same course at two levels (batch 193) |
| **68** | `CET2127C` — a VISITOR-REQUESTED course whose number names a different subject than the college teaches (batch 194) |
| **69** | `EGM3401` — a statewide qualifier that both institutions drop (batch 194) |
| **70** | Palm Beach State and Hillsborough: answering servers, unknown paths (batch 194) |
| **72** | `GRA4154C` — "Introduction" at one institution, "Advanced" at three, on a 4000-level number (batch 196) |
| **73** | `EVR4023` — the statewide definition names a METHOD, and one of two carriers has left it (batch 199) |
| **75** | `EDG4442` — a FIELD EXPERIENCE and a METHODS COURSE on one number (batch 200) — **split candidate, and a new shape** |
| **76** | `ATF1100L` — the statewide TITLE states a credit range and two of three carriers fall outside it (batch 200) |
| **77** | A title inside an SCNS prerequisite string can be an INSTITUTION's title, not the state's (batch 200) |
| **78** | `HFT3271` — FOUR subjects, and the statewide title matches NONE of them (batch 201) — **HELD** |
| **79** | COURSE-TYPE divergence fired again in the very next batch — `JOU4201` (batch 201) |
| **80** | The Gordon Rule designation is now MACHINE-READABLE — and a retro-sweep candidate just got cheap (batch 201) |
| **81** | `CHM1020C` republished at v1.1 over a live May guide — and the process gap that let it happen (batch 202) |
| **82** | The old inventory AGGREGATED suffixed variants — which sent early work to the wrong member of each family (batch 202) |
| **83** | `MUN3483` — three carriers, three ensembles, and the state has dedicated numbers for two of them (batch 203) |
| **86** | `PSY3215` — a misfiling, a sequence-position problem and a credit divergence on one number (batch 205) |
| **87** | An undergraduate title that is the state's GRADUATE title — now twice in two batches (batch 205) |
| **88** | DEPARTMENTAL divergence invisible in the statewide record — `POS3625` (batch 205) |
| **89** | `SPN3400` has a LIVE guide, and UWF appears to teach something else under that number (batch 207) |
| **90** | `SPM4505` Sport Finance (live guide) and `SPM4503` Economic Issues in Sport — a cross-reference worth adding (batch 207) |
| **91** | The studio-prefix contact-hour convention is unsettled — five live `TPA` guides use three conventions (batch 208) |
| **92** | New evidence on held item 25 (`TPA3230C`, costume) — two of its stated facts are wrong (batch 208) |
| **93** | `AMH2010` and `AMH2020` carry ELECTIVE high-school credit, not AMERICAN HISTORY — and both have live guides (batch 210) |
| **94** | NWFSC's `ATF2530L` catalogue entry carries the WRONG course description (batch 212) |
| **95** | Nine live guides in the `ATF`/`ATT` family may now be incomplete — the alternate-level pair (batch 212) |
| **96** | `BOT4850` — the statewide TITLE says "w/Lab" and the statewide DESCRIPTION says "LECTURE ONLY" (batch 214) |
| **97** | The flat file's `transferable` field holds the HIGH-SCHOOL-CREDIT code — batch 212's note corrected (batch 214) |
| **98** | `HFT3271` — FOUR subjects on one number, and NO carrier teaches the statewide one (batch 218) |
| **99** | `HFT4252` — the statewide TITLE and DESCRIPTION contradict each other, and the CARRIERS SPLIT (batch 218) |
| **100** | `CCJ` splits courses by SECTOR across two numbers — two confirmed, and the prefix should be swept (batch 220) |
| **101** | `JOU4306` — two unrelated subjects on one number, and a SPLIT is soundly sourceable (batch 224) |
| **102** | The STUDIO contact-hour convention contradicts itself — and `GRA` now holds three answers |
| **103** | CIP codes are the career-path anchor — and institutions disagree on 7% of them (batch 230) |
| **104** | FGCU's catalogue has stopped returning course content (batch 231) |
| **105** | `PHC4109` (live) tells the reader a masked course number cannot be looked up — it can (batch 234) |
| **106** | 81 PUBLISHED GUIDES SIT ON MINORITY COURSE IDS — including the ENTIRE Florida math gateway (measured 2026-09-17) |
| **107** | FLORIDA NUMBERS GENERAL CHEMISTRY TWO WAYS — and 35 live guides name only one of them (found 2026-09-18) |
| **108** | `ECH3854`'s statewide prerequisite resolves for NOBODY — recorded, not blocking (found 2026-09-18) |

### Informational — no decision needed (19)

| # | Item |
|---|---|
| 18 | `ASC1610C` — cannot be sourced, not a decision (batch 154) |
| 19 | Should the C-suffix contact-hour rule be restated? (batch 154) — *low priority* |
| 22 | `MUT4311` / `MUT3311` — a NUMBER divergence, which defeats articulation (batch 163) |
| 23 | "Tradition divergence" — a new drift category, two instances in consecutive batches |
| 24 | `PHI3500` / `PHI4500` — another number divergence, and this one is deliberate (batch 172) |
| 32 | `BSC1050` published from the only reachable catalog, which holds the NARROWER subject (batch 182) — *informational, no action needed* |
| 35 | `EUH3570` — chronological divergence found, sourcing done, row deferred (batch 183) |
| 39 | `RTV3511` — THREE production courses under one number; craft divergence (batch 185) — *informational, published with a warning* |
| 40 | `PHY3220` — credit-count divergence, a shape with no identifier signal (batch 185) |
| 41 | `SCE4320` — scope divergence against a BANDED certification (batch 186) |
| 42 | Prerequisite strings are approaching the 500-character server limit (batch 186) — *process, no decision needed* |
| 44 | `PHZ3151C` — sourcing failure, left queued (batch 187) |
| 46 | `APK2105C` — the BSC/APK prefix divergence, now evidenced from a catalog line (batch 188) — *informational, but the highest-stakes row written* |
| 48 | `APK3220C`, `APK4114C`, `APK4600C` — sourcing failures, left queued (batch 189) |
| 51 | `EEE4306C` and `EEE4309C` — statewide records that contradict what is taught (EEE sweep) — *informational, published with warnings* |
| 66 | `ENV4351` — credits of 2, 3 AND 4 on one number (batch 193) — *informational, published with the table* |
| 71 | A third contact-hour shape: the STUDIO course (batch 196) — *tooling fixed, no decision needed* |
| 74 | Say so when a number is CLEAN — new handling applied in batch 199 (informational) |
| 84 | NEW SHAPES from batch 203 — recorded for awareness, no decision needed |

### ✅ Resolved (10)

| # | Item |
|---|---|
| 7 | `PHT1006C` — CLOSED 2026-09-03: resolved and published (informational) |
| 9 | Split-family `C`-suffix rows with no UWF coverage — **RESOLVED 2026-09-04 (batch 124)** |
| 12 | `BCN2405C` - RESOLVED 2026-09-04 (batch 141): title drift, not a subject split |
| 36 | RESOLVED — `GRA3112C` and `GRA4154C` are written; SCNS answered what no catalog would (2026-09-11) |
| 47 | The APK anatomy-and-physiology family is COMPLETE (batch 189) — *informational, closes part of item 46* |
| 52 | Item 30 RESOLVED — the seven missing taxonomy prefixes are added (2026-09-09) — *needs a deploy* |
| 53 | Item 50 RESOLVED — inventory counts regenerated from SCNS; **the C-suffix mechanism is proven** (2026-09-09) |
| 64 | RESOLVED — the prerequisite ceiling was raised to 1000 and deployed (2026-09-11) |
| 67 | The 1000-character prerequisite ceiling is doing exactly what it was raised to do (batch 193) |
| 85 | `OCB3108C` — the C-nobody-carries class gains its cleanest case, and this one resolved itself (batch 203) |
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

## 36. ✅ RESOLVED — `GRA3112C` and `GRA4154C` are written; SCNS answered what no catalog would (2026-09-11)

**Both published in batch 196.** The item was parked as a sourcing failure because no institution catalog
answered — and **SCNS statewide, solved two days after this was written, answers both completely**: full
statewide descriptions plus per-institution titles and credits for four institutions each.

⚠⚠ **The general lesson is worth more than the two guides: when a new source lands, re-run the items parked
for want of one.** This sat as "informational" while the thing it was waiting for already existed. **Items
44 and 48 name other parked sourcing failures that should be re-tested against SCNS.**

The original entry follows.

### Original entry (batch 184)

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

## 62. ⚠⚠ `MUN3323` — the statewide title uses retired vocabulary; **a retro-sweep candidate for the MUN prefix** (batch 192)

Statewide title: **"Women's Glee Club — Upper Level."** ⚠ **Not one of the five institutions carrying the
number uses it** — UCF calls it *Soprano/Alto Chorus*, UNF *Osprey Treble Chorus*, FGCU *Bel Canto Choir*,
UF *Chorale*, UWF *Concert Choir*.

The field has moved from naming a choral ensemble by the **gender of its singers** to naming it by **voice
type**. The guide is written to the current vocabulary, explains the change, and warns that searching a
schedule for the old name finds nothing.

**No decision needed on this guide.** The ask is narrower: **are there other MUN and MVK/MVV numbers whose
statewide titles are similarly dated?** The statewide inventory is the SCNS catalog rather than current
practice, and choral and vocal numbering is where the terminology has moved most. A sweep of the music
prefixes for gendered ensemble titles would be cheap from the flat file.

---

## 63. ⚠ `MUN3713` / `MUN4714` — UWF appears to use the two numbers in REVERSE (batch 192)

**Statewide:** `MUN3713` is the large instrumental jazz ensemble; `MUN4714` is the jazz chamber ensemble
(combo). **UWF titles `MUN3713` "Jazz Combo" and `MUN4714` "UWF Jazz Band"** — apparently swapped.

**Published as-is with a warning in both guides**, telling the reader to check their own catalog rather than
infer the format from the statewide title. **Not treated as a split** — the subject is jazz either way; only
the format is exchanged.

**The ask, if any:** whether a probable local numbering error is worth reporting to the institution. The
project has not previously had a route for that, and this is the second case (after `PUR4801`) where an
institution's use of a number looks like a mistake rather than a variation.

---

## 64. ✅ RESOLVED — the prerequisite ceiling was raised to 1000 and deployed (2026-09-11)

**Ron deployed the raise** (`c8f4f37`) the same day this item was written. Verified live: a 552-character
string pushed and read back intact. **Ten guides republished at v1.1 with their trimmed warnings restored**
(`CES3100C`, `CWR3201C`, `CWR4202C`, `CEG3011C`, `MUN3443`, `MUN3713`, `CES4702C`, `MUN3313`, `MUN3323`,
`MUN4714`); `CES4605C` and `MUN3133` were never trimmed and were not republished. Detail in `SOURCES.md`.

⚠ One tooling note worth keeping: **`scratchpad/mkguide.py` still carried the old 500** and would have
blocked long strings locally, looking exactly like the server rejecting them. **When a server limit changes,
grep `Tools/` for the number as well as updating the validator.**

### The original entry, kept for the evidence

**The 500-character prerequisite ceiling failed FIVE of SIX guides, twice running (batch 192)**

| Batch | Over the limit on first write |
|---|---|
| 191 (civil engineering) | **5 of 6** — 531, 535, 537, 538, 515 |
| 192 (music ensembles) | **5 of 6** — 552, 523, 511, 508, 503 |

⚠ **Ten of twelve, in two disciplines with nothing in common.** This is no longer an occasional overflow;
it is the normal outcome for any course with real transfer hazards. What gets trimmed is audition
requirements, credit-spread warnings and the rehearsal-hours warning — **precisely what a student needs
before registering.**

**No decision needed** — the raise to 1000 characters is written up in
`Deployment/PENDING_SERVER_CHANGES.md`. Recorded here as the evidence that it should ship in the next
release rather than continue to drift. **It is now the single highest-value pending server change for
guide quality.**

---

## 65. ⚠⚠ `ENV3001` / `ENV4001` — SCNS itself carries the same course at two levels (batch 193)

**The strongest level-divergence case found, and stronger than `CES3100C`/`CES4100C` (item 60), because the
duplication is in the STATE record rather than only in institutional practice.**

The statewide catalog carries **an identical title and an identical description** for both numbers —
*"Introduction to Environmental Engineering — Majors"* — at the 3000 level and the 4000 level:

| Number | Institutions |
|---|---|
| `ENV3001` | FIU, UCF, UWF (3 credits), **UF (4 credits)** |
| `ENV4001` | FAMU, FSU, USF (3 credits) |

⚠ SCNS equivalency does not cross numbers, so the transfer guarantee does not run between them, and the
level digit additionally affects upper-division and residency credit counts.

**The ask:** none on the guides — the queued row was `ENV3001C` and it is written with the warning. But
**`ENV3001` and `ENV4001` are not in the queue**, between them cover seven institutions, and under the
queue-only rule will never be written. They belong on the same list as item 59.

---

## 66. ⚠⚠ `ENV4351` — credits of 2, 3 AND 4 on one number (batch 193) — *informational, published with the table*

**The widest credit spread on any technical course in the project.** USF 2, FIU 3, UWF 3, **UF 4**.

⚠ FIU also folds hazardous waste (statewide `ENV4330`) into the same course, so its students cover both
subjects less deeply while the transcript line reads identically to everyone else's.

**Published as one guide** naming every institution and its credit value, with the audit consequence stated.
**No decision needed** unless Ron wants a standing practice for courses whose credit value varies by a factor
of two — at that point the two-credit and four-credit versions are arguably different courses.

---

## 67. ✅ The 1000-character prerequisite ceiling is doing exactly what it was raised to do (batch 193)

First batch written under it. **Prerequisite strings ran 860–960 characters and not one would have fitted
before**; nothing was trimmed.

What the room bought: the four-institution credit table on `ENV4351`, the three-packagings explanation on
`ENV3001C`, the five-day BOD warning on `ENV3001L`, and the site-assessment-versus-engineering distinction
on `ENV4330`. **Under the old ceiling each would have lost about half its content.** Recorded as the closing
evidence on items 61 and 64.

---

## 68. `CET2127C` — a VISITOR-REQUESTED course whose number names a different subject than the college teaches (batch 194)

Statewide: **Digital/Microprocessors II**. Palm Beach State College, the only carrier: **Programmable Logic
Controllers**. Different working subjects — embedded design against industrial automation. Published as one
guide covering both, labelled, with a comparison table, and a hardware-safety warning on the PLC half.

Palm Beach State's catalog is unreachable, so the PLC half is written from the subject as standardly taught
rather than from that college's syllabus, and the guide says so.

**The ask:** none urgent. But this is the **second visitor request in a row to land on a number with a
divergence**, after `CET1112`. That is a pattern worth naming: a request queue surfaces exactly the courses
whose numbering confuses people. If Ron agrees, it argues for treating a request as a signal to check the
number's whole family before writing.

---

## 69. `EGM3401` — a statewide qualifier that both institutions drop (batch 194)

Statewide title **Engineering Mechanics — Dynamics Alternative**; the definition says the standard syllabus
**plus** 3-D rigid-body dynamics, gyroscopic motion and orbital mechanics. **UF and UWF both title it simply
"Dynamics."** The extended scope is invisible in a catalog and on a transcript.

Published with the warning. **No decision needed** — recorded because it is a new shape: a statewide
qualifier that institutions systematically drop. Worth watching for wherever a statewide title carries
"Alternative", "Honors", "Accelerated" or similar.

---

## 70. Palm Beach State and Hillsborough: answering servers, unknown paths (batch 194)

Re-probed for two visitor-requested courses. **Catalog subdomains return 000; main domains return 404 with
full bodies** — the servers answer, so this is a wrong-path problem rather than a block, which is a better
position than the register's "curl 000 / 404" entry implies. Neither is a Coursedog school.

Eight probes, then stopped per the burst rule. **No decision needed** — recorded so the next session starts
from "find the path" rather than "assume blocked." Both colleges carry courses the project will meet again.

---

## 71. ⚠⚠ A third contact-hour shape: the STUDIO course (batch 196) — *tooling fixed, no decision needed*

`GRA3112C` and `GRA4154C` tripped the validator at 90 contact hours. ⚠ **The 90 was right and the validator
was wrong** — a 3-credit art or design studio meets about six hours a week, because the work is made in the
room.

| Shape | Ratio | 3 credits |
|---|---|---|
| Lecture | ~1:15 | 45 |
| `C` integrated lecture+lab | ~1:20 | 60 |
| **Studio** | **~1:30** | **90** |

**`validate_drafts.py` now recognises studio prefixes** (`ART`, `ARE`, `GRA`, `PGY`, `CRW`, `DAA`, `DAN`,
`THE`, `TPA`, `TPP`, `MUS`, `IND`, `INT`). ⚠ **Without it the warning would have been noise on every studio
guide the project writes**, which is the condition under which a warning stops being read.

---

## 72. ⚠⚠ `GRA4154C` — "Introduction" at one institution, "Advanced" at three, on a 4000-level number (batch 196)

UCF, UNF and UWF call it **Advanced Illustration**; Florida Atlantic calls it **Introduction to
Illustration**. ⚠ **The 4000-level number is itself a claim that this is senior work**, making FAU the
outlier — and in a studio sequence the consequence is real, because the next course assumes a body of prior
work.

**Published with a diagnostic rather than a guess: check whether your institution enforces the `GRA3512`
prerequisite.** If it does, the course is advanced whatever it is called.

**No decision needed** — recorded because it is a level divergence *inside* a single number rather than
between two, which is a shape items 60 and 65 do not cover.

---

## 73. ⚠⚠ `EVR4023` — the statewide definition names a METHOD, and one of two carriers has left it (batch 199)

Statewide, `EVR4023` is a science course: *physical, chemical and biologic components* of coastal systems,
taught *"based on readings of scientific papers."* **UWF matches it as "Coastal and Marine Environments."**
⚠ **FIU teaches "Coastal Resource Management"** — policy, allocation and stakeholders.

⚠ **Why this is a split candidate rather than title drift: the statewide record specifies the METHOD.** A
course built on primary scientific literature and one built on management case studies are different
preparations for graduate study and for technical hiring, and **nothing on a transcript distinguishes
them.**

⚠ **Two carriers means no majority to appeal to.** The tie-break used was that UWF agrees with the statewide
record, and the guide was published to the science reading with the management version labelled.

**Decision wanted:** is a two-carrier disagreement, where one side matches the statewide definition, enough
for the `-SCNS` / `-FIU` split — or does the split rule want three or more carriers before it fires? **This
is the first time the divergence rule has met a straight one-against-one.**

---

## 74. Say so when a number is CLEAN — new handling applied in batch 199 (informational)

`GEO3421` and `FIN4461` each have three institutions, identical titles and identical credit values. Both
guides now **state the absence of divergence explicitly**: *"no title drift, no credit divergence, nothing
to resolve."*

⚠ **Rationale: after 199 batches, the assumption a careful reader brings to this catalog is that something
diverges.** A guide that simply says nothing leaves them hunting for the catch. **Naming the absence is
information**, and it downgrades the standing carry-a-syllabus advice from necessary to precautionary.

**No decision needed** — recorded so the practice is consistent and so it can be reversed in one place if
Ron would rather guides stayed silent on clean numbers.

---

## 75. ⚠⚠⚠ `EDG4442` — a FIELD EXPERIENCE and a METHODS COURSE on one number (batch 200) — **split candidate, and a new shape**

Statewide title: **Teaching Strategies and Classroom Management**, prerequisite *"program admission."*

| Institution | Its title | What it is |
|---|---|---|
| UWF | Effective Learning Environments | campus methods course |
| UF | Rethinking Discipline and Classroom Management | campus methods course |
| **UNF** | **Elementary Field Experience III** | ⚠⚠ **a supervised school placement** |

⚠⚠ **This is not any divergence shape already in `CLAUDE.md`.** It is not a different subject, a different
title for the same subject, a credit difference, a chronological split, or a terminology era. **It is a
different KIND of course**: two institutions teach classroom management on campus and the third places the
student in a school with a cooperating teacher.

**Why it is more consequential than a title divergence.** A field experience carries **Level 2 background
screening before entry to a building**, the **school district's** calendar during the school day, a
cooperating teacher's evaluation, and a placement a school can terminate. None of that applies to a methods
course, and a student who registers expecting one and gets the other cannot simply work harder.

⚠⚠⚠ **The transfer consequence is the real problem. Florida programme approval specifies required
COURSEWORK and required FIELD HOURS separately.** So `EDG4442` may satisfy one requirement and not the other,
**and nothing in the number distinguishes them.** A student transferring between these three institutions can
arrive with a course that counts for the wrong half.

**Published as one guide** covering the statewide methods subject, with the field-experience reading labelled,
its five logistical consequences spelled out, a two-column test, and the advice to take the syllabus to a
certification officer.

**Decisions wanted:**

1. **Is course-TYPE divergence (placement vs classroom) grounds for the `-SCNS` / `-UNF` split?** It is
   arguably stronger than several candidates already in the table, because the two halves cannot substitute
   for each other in a *state-approved* sequence — which is a harder constraint than a transfer evaluator's
   judgement.
2. ⚠ **Should the divergence taxonomy in `CLAUDE.md` gain "course-type divergence" as a named category?**
   Expect more of it: field experiences, practica, internships and clinicals all get numbered alongside the
   coursework they accompany, so this is unlikely to be the only instance.

---

## 76. ⚠⚠ `ATF1100L` — the statewide TITLE states a credit range and two of three carriers fall outside it (batch 200)

Statewide title: **`PRIVATE PILOT FLIGHT (2 - 3 HOURS) (L)`** — the state wrote the credit range into the
title. Carriers: **NWFSC 1, Polk State 1, UWF 3.**

**The likely explanation, from the prefix family:** `ATF1108` *Primary Flight I (1 hour)* and `ATF1109`
*Primary Flight II (1 hour)* split the certificate into two phases, and ⚠ **`ATF1108`'s own statewide
description says a student completes it and "would then take ATF1100"** — so **`ATF1100` is the whole flight
course at one institution and the second phase at another.** A 1-credit listing fits the phase reading.

**Published at 3 credits** (UWF's, the top of the state's stated range) because the guide describes the
complete certificate, with the phase reading stated in `offering_notes` and in the body, **labelled as an
inference** rather than as a claim about those two colleges' catalogs.

**No decision needed on the guide.** Recorded for two reasons:

1. ⚠ **It is the first case of the STATE's own record containing a credit figure that its carriers contradict**
   — previous credit divergences were between institutions, with the state silent.
2. ⚠ **The `ATF` prefix has more of these.** Several statewide titles carry parenthesised hour figures
   (`ATF1103` "(5 HOURS)", `ATF1108` "(1 HOUR)", `ATF1600` "(1 HOUR)"). **Whoever completes the `ATF` prefix
   should expect to meet this repeatedly** and should read the title as a data field, not a label.

---

## 77. ⚠ A title inside an SCNS prerequisite string can be an INSTITUTION's title, not the state's (batch 200)

`COM4564` *Social Media Management* lists its statewide prerequisite as:

> *"COM4561 **Social Media Content Development** with a grade of C- or above."*

⚠ **But the statewide title of `COM4561` is *Social Media Campaigns*. "Social Media Content Development" is
UWF's local title.**

**Two things follow, and both are reusable:**

- ⚠ **Do not read a title inside a prerequisite string as the statewide title.** The statewide records are
  institution-contributed and a local title can land in a statewide field.
- ⚠ **A prerequisite naming a local title is evidence of which institution contributed the entry** — useful
  when deciding which catalog to check. Here it confirmed `COM4561`→`COM4564` is a real sequence at UWF, with
  an explicit C-minus floor, which went into the guide.

**No decision needed** — recorded as a standing caution for anyone mining `DS_Prerequisites1`.

---

## 78. ⚠⚠⚠ `HFT3271` — FOUR subjects, and the statewide title matches NONE of them (batch 201) — **HELD**

**The most severe divergence in the project to date.** Statewide `HFT3271` is **CONDO/RESORT MANAGEMENT**,
and unlike `TPA3230C` the statewide record carries a **full description**: condominium and resort operation,
planning, development, financial investment, marketing, the condo-hotel concept and timesharing.

| Institution | Its title | What the field actually is |
|---|---|---|
| FIU | **Nightclub Management** | beverage, entertainment and late-night operations |
| FGCU | **Club Management** | private and country club management — a CMAA professional field |
| UWF | **Spa Management** | spa and wellness operations |
| *statewide* | *Condo/Resort Management* | ⚠ **resort and condominium property management — carried by none of them** |

All three at 3 credits.

⚠⚠⚠ **Why this is worse than `TPA3230C`, which is the current benchmark for severity.** There, three
institutions disagreed but the statewide title matched one of them (FGCU's *Costume Design*), so a
`-SCNS` guide had a referent. **Here the statewide description has no carrier at all.** A `-SCNS` page would
have to be written from the statewide description alone, with no institution teaching it — which is close to
the line the project's sourcing rule draws against writing from a title.

⚠ **These are four different hospitality sub-industries, not four framings of one.** Different employers,
different credentials (CMAA for clubs, ISPA for spas, ARDA for timeshare and vacation ownership), different
career paths. A student who took "Spa Management" and transfers into a programme expecting resort property
management has covered nothing the receiving programme wants.

⚠ **A secondary observation worth keeping:** the queue row's own title is **"SPA MANAGEMENT"** — UWF's local
title recorded as though it were the course. **Third instance in two batches of local text occupying a field
that reads as authoritative** (see items 77 and the `HSA3551` prerequisite in batch 201). **The inventory's
titles are not statewide titles.**

**Pulled from batch 201. Status left `queued` with a `HELD` note, per the `TPA3230C` convention.**

**Decisions wanted:**

1. **Is this writable at all, and how?** Options: (a) a four-way disambiguation page at the bare number with
   no content guide, (b) three `-<INST>` guides and a disambiguation stub, with **no** `-SCNS` page because
   nothing carries it, or (c) leave it held.
2. ⚠ **This and `TPA3230C` now make two cases where a number carries three or more subjects.** **Should the
   split rule gain an explicit N-way form**, and should option (b) above — **a disambiguation page with no
   `-SCNS` half** — be permitted when the statewide reading has no carrier?

---

## 79. ⚠⚠ COURSE-TYPE divergence fired again in the very next batch — `JOU4201` (batch 201)

`EDG4442` (item 75, batch 200) named course-type divergence: a campus course at one institution and a
supervised placement at another. ⚠⚠ **`JOU4201` is the second case, one batch later.**

| Institution | Its title | What it is |
|---|---|---|
| USF | News Editing I | classroom editing course, 3 cr |
| UWF | News Editing | classroom editing course, 3 cr |
| **UF** | **News Center Practicum** | ⚠⚠ **supervised newsroom placement, 1–3 VARIABLE credits** |

**Two instances in consecutive batches settles the question item 75 raised: this is a recurring shape, not a
one-off.** The mechanism is the same in both — **a practicum or placement gets numbered alongside the
coursework it accompanies** — and so is the consequence: **accredited programmes count skills coursework and
professional experience as SEPARATE requirements**, so the number satisfies one and not the other, with
nothing in the identifier to say which.

⚠ `JOU4201` additionally carries **variable credit at UF (1–3)** and a quieter scope divergence (statewide
defines a **feature/magazine/book** editing course; both classroom carriers teach **news** editing).

**Published as one guide** covering the classroom editing course, with the practicum reading labelled, its
four logistical consequences stated, and a two-column test.

**No new decision needed beyond item 75** — recorded because it is the evidence that item 75's second
question ("should the taxonomy gain course-type divergence as a named category?") should be answered yes.
The category is already written into `CLAUDE.md`; **what is open is whether these cases warrant splits.**

---

## 80. ⚠⚠ The Gordon Rule designation is now MACHINE-READABLE — and a retro-sweep candidate just got cheap (batch 201)

`CLAUDE.md` has asserted since batch 178 that *"the designation is made by the INSTITUTION, not by the course
number"*, and flagged that **roughly a dozen already-published guides record a UWF Gordon Rule label without
explaining the C-or-higher condition** — noting a retro-sweep as a `REVIEW_QUEUE` candidate.

⚠⚠ **`HIS2050` (batch 201) demonstrated the rule from data for the first time**, and in doing so showed the
sweep is now cheap:

| Institution | Its title | Designation flags in the SCNS flat file |
|---|---|---|
| FAU | Writing History | `gordon_rule`, `gordon_writing`, `ge_com` |
| FSU | The Historian's Craft | `gordon_rule`, `gordon_writing` |
| UWF | Explore History | ⚠ **`ge_soc_sci` only — no Gordon Rule** |

⚠ **The flat file carries per-institution designation flags for EVERY course** (`gordon_rule`,
`gordon_writing`, `ge_com`, `ge_hum`, `ge_math`, `ge_nat_sci`, `ge_soc_sci`, at byte offsets 226–233). They
have been in `scns.FIELDS` all along and were not being read.

**Decision wanted:** ⚠ **is a retro-sweep worth doing now?** One parse of `crslist.txt` can produce, for every
published guide, whether each of its carriers designates the course Gordon Rule writing, Gordon Rule
mathematics, or a general-education category. That would let the sweep be **a report first and a
republish-list second** — rather than the open-ended task it looked like in batch 179.

⚠ **New guides now get this automatically**, since the check is one lookup; the question is only about the
back catalogue. Ron's standing position on retro-work (2026-09-11, on `offering_notes`) was *"a task for much
later"* — **this item exists to record that the cost has dropped a lot, in case that changes the answer.**

---

## 81. ⚠⚠⚠ `CHM1020C` republished at v1.1 over a live May guide — and the process gap that let it happen (batch 202)

**`CHM1020C` already had a live guide, published 2026-05-04** (v1.0, 18 KB, no `offering_notes`, 181-character
prerequisite). ⚠ **I wrote a replacement without checking, because I extended a request-driven batch into the
number's family and checked `hasGuide` only for the two requested numbers.**

**Republished as v1.1**, which is the right call on the merits — it is a material rewrite:

| | v1.0 (May) | v1.1 (batch 202) |
|---|---|---|
| Size | 18 KB | 27 KB |
| `offering_notes` | none | 7 public carriers with per-school notes |
| Credit divergence | not covered | ⚠ the systematic **3-vs-4** split explained (4 = lecture + lab bundled; 3 = same lab work, one credit less) |
| The three forms | not covered | ⚠ `CHM1020` / `CHM1020L` / `CHM1020C` comparison table and a which-to-register-for decision table |
| GE Core | not covered | ⚠⚠ the **(GE CORE)** marker and s. 1007.25 transfer protection |
| Laboratory | brief | safety, dress code, and the **data-fabrication** warning |

**Decision wanted:**

1. ⚠ **Is a v1.1 republish of a pre-flat-file guide acceptable when the course turns up inside a batch you
   are writing anyway?** Ron's standing position (2026-09-11, on `offering_notes`) was that redoing old
   guides is *"a task for much later"* and **"do not start a retro-sweep."** ⚠ **This was not a sweep** — it
   was one course inside a request-driven family — **but it is the first time a live guide has been replaced,
   and the precedent should be deliberate rather than accidental.** Options: (a) allow it when the course
   falls inside a batch's scope, (b) allow it only for guides the batch's own research contradicts, (c) leave
   old guides alone and skip the number.
2. **Should the old v1.0 content be recoverable?** It is not currently — the push overwrote it. ⚠ **If
   replacements are going to happen, a copy of the superseded HTML should be kept somewhere first.**

### ⚠⚠⚠ And the two process failures, which are the reusable part

**Both are now fixed as standing steps in `CLAUDE.md`, but they are worth Ron seeing.**

1. ⚠⚠ **No live-guide check before writing.** `GET /api/v1/courses/{id}/guide` is one call per course and
   answers it definitively. **Now a standing pre-batch step** — the `hasGuide` flag on a *request* does not
   cover courses added to the batch afterwards.
2. ⚠⚠⚠ **`validate_drafts.py` validated a STALE draft and reported it clean.** My `CHM1020C` assembly had
   **failed** on the 1000-character prerequisite ceiling, so no new draft was written — **and the validator
   then passed the May 4 draft, reporting "6 draft(s) checked: 6 clean" when only five were mine.**
   ⚠ **The validator checks what is on disk, not what was just built.** **A failed `mkguide.py` run plus an
   older draft on disk produces a clean validation of the wrong file.**
   **Standing practice now: read the assembler's per-course output, and treat a MISSING assembler line as a
   failure regardless of what the validator says.**

⚠ **Worth considering as a tooling change rather than a habit:** `validate_drafts.py` could warn when a
draft's modification time predates the current session, or `mkguide.py --all` could refuse to leave a stale
file in place. **Recorded as a suggestion, not done.**

---

## 82. ⚠⚠ The old inventory AGGREGATED suffixed variants — which sent early work to the wrong member of each family (batch 202)

**`CHM1020C`'s queue row records "32 institutions."** The SCNS flat file shows **7** public carriers of the
`C` form and **27** of the bare `CHM1020`.

⚠⚠ **So `courses_2plus_institutions.csv` counted the bare, `C` and `L` forms together and attached the total
to one id.** Under the original priority-by-institution-count rule, that made the **`C` id look like the
high-volume course** — and the May-era work took it.

**The observable result in `CHM`:** `CHM1020C`, `CHM1025C`, `CHM1045C`, `CHM1046C`, `CHM1045L` and
`CHM1046L` were all published in May 2026, while ⚠ **`CHM1020` (27 carriers), `CHM1020L`, `CHM1015`,
`CHM1024` and `CHM1025` (18 carriers) had never been written** — including the single most widely offered
chemistry course in the state, which is what prompted a visitor to request it.

⚠⚠⚠ **This is a specific, checkable prediction about where the back catalogue is thin: high-enrolment
GENERAL-EDUCATION families where the bare or `L` form was passed over because the institution count was
attached to the `C`.**

**Decision wanted:** ⚠ **is a targeted check worth running on the other large general-education families —
`BSC`, `PHY`, `AST`, `PSC`, `MAC`, `STA`?** It is cheap now: one flat-file parse gives per-form carrier
counts, and one catalog call per id gives `hasGuide`. **That is a report, not a sweep** — and unlike the
Gordon Rule retro-question (item 80), **what it would surface is MISSING guides on very high-carrier courses
rather than incomplete detail on existing ones**, which is a different and arguably more urgent kind of gap.

⚠ **Supporting evidence that this is not hypothetical: `CHM1020` is carried by 27 Florida public
institutions — more than almost any course this project has written — and it was missing until a visitor
asked for it.**

---

## 83. ⚠⚠⚠ `MUN3483` — three carriers, three ensembles, and the state has dedicated numbers for two of them (batch 203)

Statewide: **Guitar Ensemble – Upper Level**, prerequisite *consent of instructor*.

| Institution | Its title | What it actually is | Credits |
|---|---|---|---|
| UWF | Guitar Ensemble | ✅ the statewide subject | 1 |
| UNF | **Jazz Guitar Ensemble** | ⚠ guitars, different repertoire and technique | 0–1 |
| UCF | **String Ensemble** | ⚠⚠⚠ **violin, viola, cello, bass** | 1 |

⚠⚠⚠ **A guitarist registering for `MUN3483` at UCF joins a string ensemble.** Not an emphasis, not a
narrowing — **a different instrument family.**

**What makes this worse than the `PUR4801` collision, which is the current benchmark for a misfiling:
the state already assigns dedicated numbers to BOTH other readings.**

| What is being taught | Where the state numbers it |
|---|---|
| Jazz guitar ensemble | `MUN3484`, `MUN3486`, `MUN3488` |
| String ensemble | `MUN3413`, `MUN3414`, `MUN3243` |
| String quartet | `MUN3411` |
| Guitar ensemble (alt.) | `MUN3487` |

⚠ **With `PUR4801`, one institution had put a capstone on the wrong number. Here two of three carriers have
misfiled, in two different directions, and a correct number existed for each.**

**Published as one guide** to the statewide subject, with both other readings labelled, the numbering table
above included, and a usable two-question diagnostic (*which instruments does this ensemble contain, and is
the repertoire notated or chart-based?*).

**Decisions wanted:**

1. ⚠ **Is a MISFILING a split candidate at all?** The `-SCNS` / `-<INST>` rule was built for a number
   carrying two genuine subjects. **Here the divergence is arguably an error rather than a reading** — the
   institutions are teaching real courses under the wrong numbers. **Options: (a) split as usual, (b) publish
   the statewide subject with the misfilings labelled (what was done), (c) treat it as a data-quality item
   for the verification pass rather than a content decision.**
2. ⚠⚠ **This is the second case of misfiling-shaped divergence** after `PUR4801` (and arguably `HFT3271`,
   item 78, where no carrier matches the state at all). **Is "misfiling" worth its own row in the divergence
   taxonomy**, distinct from subject divergence? The handling differs: **with a misfiling there is a right
   answer, and the guide can name it.**

---

## 84. ⚠⚠ NEW SHAPES from batch 203 — recorded for awareness, no decision needed

**Three shapes were named and written into `CLAUDE.md` this batch. None needs a decision; they are here so
Ron sees what the taxonomy gained.**

**1. ⚠⚠⚠ ORDINAL-BASE divergence — the same ordinal counted from a different origin.**
`JPN2200` statewide is *"Intermediate Japanese I"*; **UWF calls it "Japanese III"**, counting semesters from
the start of the language rather than within the intermediate year. ⚠ **A student searching a UWF catalog
for "Intermediate Japanese I" will not find it.** **Not title drift** — the same convention applied to a
different base. **Expect it wherever a subject is numbered by ordinal: languages, `I`/`II` pairs, studio and
ensemble levels.**

**2. ⚠⚠⚠ The `MUN` level digit encodes the STUDENT, not the course.**
Florida numbers each ensemble at lower-division, upper-division and graduate level — **and they are
frequently the same ensemble.** The same rehearsal holds players enrolled under three different numbers.
⚠ **And the last three digits change too: the lower-level symphony orchestra is `MUN1210`, not `MUN1213`.**

**3. ⚠⚠ `0–1` credit including ZERO — a third reason for `credits=0`.**
After PSAV clock-hour courses and zero-credit corequisite laboratories, this is **participation without
credit**, used against a degree's ensemble cap and **Florida's excess-hours provisions.** ⚠ **The trade-off
is that a zero-credit course does not count toward full-time enrolment** — aid, athletic eligibility, visa
status.

⚠ **One of these may be worth Ron's attention later rather than now:** the excess-hours point means
**Florida's own credit-accumulation penalty is a reason a course is offered at zero credit** — which is a
student-finance fact the guides had not previously connected to course data, and it may be worth a standing
note wherever repeatable ensemble or activity courses appear.

---

## 85. ⚠ `OCB3108C` — the C-nobody-carries class gains its cleanest case, and this one resolved itself (batch 203)

⚠⚠ **`OCB3108C` is carried by NO institution, and the flat file confirms ABSENCE rather than an unreachable
source** — stronger than `COP3014C` or `INP3004C`, where the register recorded catalogs as unfetchable.

**And unusually, the fix needed no decision: the real ids were already in the queue.**

| Id | Carriers | Credits | Queue status |
|---|---|---|---|
| `OCB3108C` | ⚠ **none** | — | queued (now **HELD**) |
| `OCB3108` | USF *Marine Field Studies* | 4 | not queued |
| `OCB3108L` | UNF, UWF | **3–4** | queued — ⚠ **promoted to 997**, the priority the phantom held |

**Actions taken, both routine:** `OCB3108C`'s note rewritten to HELD with the resolution stated (status left
`queued`, per the `TPA3230C` convention); `OCB3108L` promoted to the phantom's priority so the real course is
written at that position.

⚠ **A sub-finding worth keeping:** the `L` form runs **3–4 credits, not 1** — **a full field and study-abroad
course numbered `L` because it is entirely practical work, not a laboratory attached to a lecture.**
⚠⚠ **So an `L` suffix does not reliably mean "1-credit lab partner."** That assumption is embedded in the
project's contact-hour heuristics and in `validate_drafts.py`'s 1-credit expectation, and **this is the first
counterexample.**

**No new decision wanted** — ⚠ **but this case strengthens REVIEW_QUEUE item 28**, which asks for one
decision covering the whole C-nobody-carries class. **The class now has four members (`TPA3230C`, `COP3014C`,
`INP3004C`, `OCB3108C`) and they are not all alike:** `TPA3230C` also has three competing subjects, while the
other three have a clear subject and only a spurious suffix. ⚠ **A single rule could cover the latter
three: where the flat file confirms no carrier and a real id exists, HOLD the phantom and promote the real
id.** **That is what was done here, and it is offered as the proposed general rule.**

---

## 86. ⚠⚠⚠ `PSY3215` — a misfiling, a sequence-position problem and a credit divergence on one number (batch 205)

**Three independent problems, and the third instance of the misfiling shape.**

| Institution | Its title | Credits |
|---|---|---|
| FIU | **Research Methods and Data Analysis in Psychology** | **4** |
| UWF | **Research Methods in Psychological Science** | **3** |

**1. ⚠⚠⚠ Misfiling.** **FIU's title is the statewide title of `PSY3211`**, a different number whose statewide
prerequisite is a statistics course and whose scope — methods *plus* data analysis — matches FIU's 4 credits.
⚠ **FIU appears to be running under `PSY3215` a course the state numbers `PSY3211`.**

**2. ⚠⚠ Sequence position.** The statewide title carries a **"(CONT)"** marker and the description says
*"complex research projects"*. ⚠ **UWF's title reads as a FIRST, standalone methods course.** **The number
may be the first methods course at one institution and the second at another** — which changes what it
**assumes** rather than what it covers, and a transfer student expecting the basics meets a course that
assumes them.

**3. ⚠ Credits 3 vs 4.** Consistent with data analysis folded in at FIU.

⚠ **Florida numbers research methods in psychology at least EIGHT ways** (`PSY2210`, `PSY3211`, `PSY3213`,
`PSY3215`, `PSY3017`, `PSY3234`, `PSY4320`, plus graduate numbers), and ⚠⚠ **the state flags `PSY3215` as a
LABORATORY course while neither carrier uses an `L` suffix.**

**Published as one guide** to the statewide second-course reading, with all three problems stated and a
two-question diagnostic for the reader.

**Decisions wanted:**

1. ⚠ **Misfiling now has three instances** — `PUR4801` (a capstone on the cases number), `MUN3483` (a string
   ensemble on the guitar number), and this. **Item 83 asked whether misfiling is a split candidate; this
   strengthens the case for an answer**, because the three are not alike: `MUN3483` was a different subject,
   `PUR4801` a different course in the same subject, and `PSY3215` the *same* subject at a different
   sequence position.
2. ⚠⚠ **Is a course whose SEQUENCE POSITION differs between carriers a split candidate, or just a warning?**
   The subject is identical; what differs is whether it is first or second. **This is the mildest of the
   three misfilings and arguably the most common shape in the catalog** — worth a general rule rather than a
   per-course decision.

---

## 87. ⚠⚠ An undergraduate title that is the state's GRADUATE title — now twice in two batches (batch 205)

**`POT4013`:** FAU's undergraduate title **"Ancient Political Thought"** is the statewide title of
**`POT6016`, a GRADUATE course.**

⚠ **Second instance in consecutive batches.** In batch 204, **all three carriers of `PHY4513` used "Thermal
and Statistical Physics"**, which is the title the state assigns to the graduate number `PHY5515`.

**The consequence is identical both times and mild but real:** ⚠ **a transcript line does not identify the
level**, and a graduate admissions reader unfamiliar with Florida numbering could take the course either way.
**Both guides tell the reader to keep the syllabus.**

⚠ **Also recorded on `POT`: the state's own list is internally duplicated** — `POT2010` and `POT2300` are
both *Classical Political Theory*, and at least four numbers cover overlapping ancient-to-modern surveys.

**No decision wanted.** Recorded because **two instances in two batches suggests this is systematic rather
than coincidental**, and it may be worth a line in the verification pass: **a check for undergraduate
courses carrying titles the state assigns to graduate numbers would be one flat-file parse.**

---

## 88. ⚠⚠ DEPARTMENTAL divergence invisible in the statewide record — `POS3625` (batch 205)

**`POS3625` The First Amendment is clean between institutions** — UNF and FSU use the identical title, all
three carriers at 3 credits, nothing to resolve on the number.

⚠⚠ **But the same number is taught in different DEPARTMENTS at different institutions, and the statewide
record does not say which:**

| Political science / public law | Journalism / mass communication |
|---|---|
| all six freedoms; **religion clauses at length**; doctrinal development; case-analysis essays | ⚠ **speech and press**; defamation, privacy, access, shield laws in practical detail; religion clauses lightly |

⚠ **Both are legitimately this course and they are different preparations** — a pre-law student wants the
first, a journalism student the second.

**Why this is worth recording as a distinct shape:** ⚠⚠ **the project has used departmental placement as an
emphasis signal since batch 187** (`SYD4800` sitting in anthropology rather than sociology at UWF). **But
that was read off a catalog's own department line for one institution.** **Here the number moves between
departments ACROSS institutions and the flat file records neither the department nor the consequence.**

⚠ **Added to `CLAUDE.md` with the diagnostic that actually works — look for the religion clauses on the
reading list** — because the department cannot be read from the data and the syllabus can.

**No decision wanted.** ⚠ **But worth flagging for the verification pass: wherever a subject is taught in two
different departments (media law, statistics, technical writing, ethics, research methods), expect this, and
the only available tell is the reading list.**

---

## 89. ⚠⚠⚠ `SPN3400` has a LIVE guide, and UWF appears to teach something else under that number (batch 207)

**The first correction candidate on a published guide since item 81, and the evidence is mechanical.**

| | State's definition | UWF teaches | FAU teaches | FGCU teaches | FIU teaches |
|---|---|---|---|---|---|
| **`SPN3400`** ✅ *live guide* | *Conversation and Composition I* | ⚠⚠ *Advanced Stylistics* | *Advanced Spanish: Conversation* | ✅ *Conversation and Composition I* | — |
| `SPN3410` *(written this batch)* | *Advanced Oral Expression I* | ⚠⚠ *Composition and Conversation* | ⚠ *Advanced Spanish: Conversation* | — | ✅ *Advanced Oral Communication* |

⚠⚠ **UWF appears to have the pair transposed**: it teaches the state's `SPN3400` course under `SPN3410`,
and puts *Advanced Stylistics* — which is a different course, closer to advanced composition and style —
under `SPN3400`. **FAU carries the identical title on both numbers.** FGCU and FIU each match the state on
the number they carry.

**What was done this batch:** the new `SPN3410` guide states the whole picture, names UWF's transposition
and FAU's duplicate title, and tells students to send syllabi rather than transcript lines.

**What is NOT done:** ⚠ **the live `SPN3400` guide was written before this was found and does not carry the
warning.** It is **incomplete rather than wrong** — the statewide subject it describes is correct, and
correct for FGCU.

⚠ **Recommendation (no action taken):** on the verification pass, republish `SPN3400` at v1.1 with a
divergence block naming UWF's *Advanced Stylistics* and FAU's duplicate title. **Not urgent** — no student
is misled about the subject, only about which number carries it at two institutions.

⚠⚠ **The generalisable point, now in `CLAUDE.md`: when a misfiling is found, check what the DISPLACED
number holds at the SAME institution.** If it holds the first number's subject, it is a transposition, both
guides need the warning, and one of them may already be published.

---

## 90. ⚠ `SPM4505` Sport Finance (live guide) and `SPM4503` Economic Issues in Sport — a cross-reference worth adding (batch 207)

**Minor, and recorded only so the verification pass has it.** `SPM4503` was written this batch and draws
the economics/finance distinction explicitly, because the two are routinely confused and their availability
is very different — **`SPM4505` has five Florida public carriers and `SPM4503` has one (UWF).**

⚠ **The live `SPM4505` guide does not point at `SPM4503`.** A student reading the finance guide and needing
the economics course would not learn from it that the economics course exists, that it is a different
course, or that it is available at one school only.

**No decision wanted; no urgency.** A one-paragraph cross-reference at the next republication would close
it. ⚠ **The general practice worth confirming: where a batch writes one half of a commonly-confused pair
and the other half is already live, note it here rather than silently leaving the older guide
one-directional.**

---

## 91. ⚠⚠ The studio-prefix contact-hour convention is unsettled — five live `TPA` guides use three conventions (batch 208)

**Surfaced by a validator WARNING on `TPA3223C`:** *"3 credits with 60 contact hours for a studio prefix
(expected ~90; a 3-credit studio meets about six hours a week)."*

**What is already published in this one prefix:**

| `TPA2000C` | `TPA2200C` | `TPA2232C` | `TPA2248C` | `TPA2290L` | `TPA3223C` (this batch) |
|---|---|---|---|---|---|
| 3cr / 45h | 3cr / **64h** | 3cr / 60h | 2cr / 45h | 1cr / 45h | 3cr / 60h |

⚠⚠ **Three different conventions across five guides, and the validator expects a fourth.**

**What was done this batch:** kept at **60**, with the reasons stated — the batch-189 rule gives the
**integrated (`C`) form's** hours, for which 60 is the Florida convention, and **the closest precedent
agrees** (`TPA2232C`, a 3-credit `C` in the same prefix). **The warning was recorded rather than waved
through.**

**What is NOT decided, and is Ron's call:**

1. **Does a studio/production prefix get its own credit-to-hour convention** (the validator's ~90 for a
   3-credit studio), **or does the `C`-suffix convention (60) govern regardless of prefix?**
2. If the studio convention wins, **the five live `TPA` guides above need republishing**, and the same
   question applies to `MUS`/`MVK`/`ART`/`DAA` studio numbers.

⚠ **No urgency and no student is misled** — every one of these guides states the figure is derived and says
the real commitment is higher. **But the validator's warning currently cannot mean anything**, because the
corpus does not follow the convention the validator encodes. **A decision either way would make it a useful
check again.** Verification-pass item.

### ✅ QUESTION 1 ANSWERED by Ron, 2026-09-15 (batch 219): the SUFFIX convention governs, not the prefix

**Ron's decision, given as the contact-hour rule for the whole TPA batch: `C` suffix = 60 contact hours,
no suffix = 45.** ⚠⚠ **So a studio/production prefix does NOT get its own credit-to-hour
convention** — the `C`-suffix convention wins regardless of prefix, and the batch-189 rule stands
unchanged.

⚠ **Supporting evidence found the same batch:** **UCF's Kuali records publish weekly lab/studio hours,
and its 3-credit `C` courses carry 2 lab hours a week while its plain 3-credit courses carry none.**
`TPA3601C` is the worked case. **Two lab hours a week on top of three lecture-equivalent hours is
consistent with ~60 total contact hours, not ~90** — so the validator's ~90 studio expectation is not
what UCF actually schedules.

**Batch 219 published all seven TPA guides on this rule** (`TPA3022` 45, `TPA3064C` 60, `TPA3601C` 60,
`TPA4021C` 60, `TPA4045C` 60, `TPA4061` 45, `TPA4077C` 60), each stating the derivation and saying the
real commitment runs higher.

### ⚠ What REMAINS open — two live guides are out of line with the settled rule

**Bounded, and now a short list rather than an open question:**

| Live guide | Published | Settled rule says | Action |
|---|---|---|---|
| **`TPA2000C`** | 3cr / **45h** | 60 | ⚠ republish with a version bump |
| **`TPA2200C`** | 3cr / **64h** | 60 | ⚠ republish with a version bump |
| `TPA2232C` | 3cr / 60h | 60 | ✅ already correct |
| `TPA3223C` | 3cr / 60h | 60 | ✅ already correct |
| `TPA2248C` | 2cr / 45h | ⚠ **the rule is stated for 3-credit courses; a 2-credit `C` is not covered** | leave; raise only if a 2-credit `C` recurs |
| `TPA2290L` | 1cr / 45h | ⚠ `L`, not `C` — outside the rule as stated | leave |

⚠ **The validator's studio warning still fires on every TPA guide** (it expects ~90). **Now that the
convention is settled, the warning is the thing that is wrong, not the corpus** — `validate_drafts.py`'s
studio-prefix expectation should be changed or removed. **That is a tooling change, not a content one.**

⚠ **Same question is now settled for `MUS`/`MVK`/`ART`/`DAA` studio numbers too**, since the decision
was about the convention rather than about TPA.

---

## 92. ⚠⚠ New evidence on held item 25 (`TPA3230C`, costume) — two of its stated facts are wrong (batch 208)

**Not a new decision request — evidence bearing on an item already held**, found while pulling the
statewide `TPA` record for `TPA3223C`. ⚠ **Two things recorded in `CLAUDE.md`'s open-cases table and in
item 25 do not match the statewide file:**

| Recorded | ⚠ Actually |
|---|---|
| statewide title is **"Costume Design"** | statewide title is **"THEATRE COSTUMING I"** |
| ⚠⚠ **"NO institution carries the `C` suffix"** | **FAMU carries `TPA3230C`** — *Introduction to Costuming &amp; Wardrobe* |

**And the statewide DESCRIPTION covers BOTH sides of the split the item is held on** — costume cutting
skills and pattern development **and** rendering, colour theory, design concept and portfolio — closing
with *"this is the first course in a two course sequence"* (the partner being `TPA3231`).

**Full public carrier list for bare `TPA3230`:** FAMU *Costume Design*, FGCU *Costume Design*, FIU
*Costume History*, FSU *Costuming I*, UWF *Costume Construction* — **five carriers, four readings.**

⚠⚠ **Why this matters for the held decision: the state defines a course that is genuinely BOTH
construction and design, which explains why institutions emphasise one half — and it means the queued `C`
id is real, so the "id nobody carries" objection to writing it no longer applies.** Applying the batch-208
title/description test: the title (*Costuming I*) and the description **agree** that the course is
construction-led with design elements, so the carriers teaching pure design or pure history are the
deviation.

**No action taken** — item 25 stays held and `TPA3230C` stays in the queue. ⚠ **But `CLAUDE.md`'s
open-cases row for `TPA3230C` should be corrected whenever that table is next touched**, because it
currently records a statewide title and a carrier fact that are both wrong, and a future session would
reason from them.

---

## 93. ⚠⚠⚠ `AMH2010` and `AMH2020` carry ELECTIVE high-school credit, not AMERICAN HISTORY — and both have live guides (batch 210)

**The largest-population instance yet of the `SPN2210` shape** (batch 207), found by running the
distribution test on the `AMH` prefix.

| Number | Statewide title | High-school credit |
|---|---|---|
| `AMH2010` | Introductory Survey to 1877 **(GE CORE)** | ⚠⚠ **ELECTIVE** |
| `AMH2020` | Introductory Survey since 1877 **(GE CORE)** | ⚠⚠ **ELECTIVE** |
| `AMH2041` | Survey of the American Experience I | ✅ **AMERICAN HISTORY** |
| `AMH2042` | Survey of Social and Cultural History since 1865 | ✅ **AMERICAN HISTORY** |

**Only 2 of 271 active `AMH` numbers carry American History high-school credit, and they are not the two
canonical surveys.** ⚠⚠⚠ **`AMH2010` and `AMH2020` are among the most heavily dual-enrolled courses in
Florida** — they are GE Core, they are required for most degrees, and they are exactly what a dual-enrolled
student takes expecting it to cover the high-school American history requirement.

⚠ **Both already have live guides**, written before the distribution test existed.

**Why this needs care rather than immediate action:** the state course record is not the award mechanism.
**The district's dual-enrolment articulation agreement governs what appears on a high-school transcript,
and many districts do grant American History credit for `AMH2010`.** So the honest statement is the one
used in `SPN2210` and `ARH3301`: *the state record says elective; the articulation agreement governs;
confirm with your counsellor before the drop deadline.*

⚠ **Recommendation (no action taken):** on the verification pass, add that paragraph to the live
`AMH2010` and `AMH2020` guides at v1.1. **The guides are incomplete rather than wrong.**

⚠⚠ **Wider question for Ron, since this is now three instances** (`SPN2210`, `ARH3301`, and these two):
**should the dual-enrolment high-school-credit check become a standing item for every guide on a
LOWER-DIVISION course?** The test is one `Counter` over the prefix and it has produced actionable,
student-facing advice every time it fired. Upper-division courses need only the one-line "prefix-level
default" note.

---


## 94. ⚠ NWFSC's `ATF2530L` catalogue entry carries the WRONG course description (batch 212)

**What was found.** Northwest Florida State College's Coursedog catalogue entry for **`ATF2530L`**, titled
*"Certified Flight Instructor Instrument"*, prints the description for the **single-engine airplane CFI**
course — it refers to the *"Certified Flight Instructor Airplane Certificate"* and to the *"Flight
Instructor Airplane Single Engine Practical Exam"*, neither of which belongs to an instrument instructor
rating.

**Assessment.** A copy-and-paste error in NWFSC's catalogue, not a statement about the course. The course
number, the statewide title and the statewide description all identify the instrument instructor rating,
and NWFSC's sibling entries (`ATF2500L`, `ATF2510L`) are correct and distinct.

**What was done.** The `ATF2530L` guide was written to the statewide record and flags the error explicitly,
telling the reader to rely on the course number and their own syllabus. No content was taken from the bad
description.

**Decision wanted from Ron:** whether this is worth reporting to NWFSC. It is a real defect in a public
catalogue that could mislead a student choosing between two similar-sounding ratings, and NWFSC has been
one of the project's more reliable sources. **No action needed on the site either way** — the guide already
handles it.

⚠ **Wider point worth noting: this is the first catalogue-level description error the project has caught at
a Coursedog source.** The previous instances (`ADV4802`'s corrupt prerequisite, `AFR2132`'s forty-year-old
description) were in the **statewide** record. **Institution catalogues are not automatically cleaner than
the state file** — cross-check a description against the course number and the statewide subject whenever
it is the only source for a guide.

## 95. ⚠⚠ Nine live guides in the `ATF`/`ATT` family may now be incomplete — the alternate-level pair (batch 212)

**Not an error, a gap created by a new finding.** Batch 212 identified the **ALTERNATE-LEVEL PAIR** shape
(`CLAUDE.md`): SCNS deliberately builds lower- and upper-division versions of the same course and tells
students they *"must choose"*, and the choice carries an upper-division-credit consequence plus a
**250–500 flight hour** consequence through 14 CFR 61.160's aviation-credit-hour thresholds.

**The nine guides written in batch 212 all carry it. Earlier `ATF`/`ATT` guides do not**, because the shape
had not been identified. The ones worth checking:

| Course | Why |
|---|---|
| `ATF1100L` | published batch 200; the prefix's other live flight guide |
| `ATT1100C`, `ATT1120` | published earlier; ground-school siblings |

⚠ **Probably a small job**: `ATF1100L` and the two `ATT` numbers have **no** `(U)` alternate, so they may
need nothing more than a cross-reference. **The check is one flat-file pass** — look for a sibling number
whose `DS_Course_Intent1` reads `UPPER` against the same subject.

**Decision wanted from Ron:** whether to fold this into the deferred verification pass (2026-09-12
direction) or leave it. **Recommend deferring** — the affected guides are not wrong, and the three numbers
most likely have no alternate at all.


## 96. ⚠⚠ `BOT4850` — the statewide TITLE says "w/Lab" and the statewide DESCRIPTION says "LECTURE ONLY" (batch 214)

**What was found.** Florida's statewide title for `BOT4850` is **"MEDICAL BOTANY W/LAB"**. The statewide
description of the same record ends with the words **"LECTURE ONLY."** The record contradicts itself in a
single row.

**The evidence is one-sided as to which half is wrong** — four independent signals all say there is no
laboratory:

1. the statewide description itself (*"LECTURE ONLY"*);
2. the number carries **no `C` and no `L` suffix**, which is how Florida marks laboratory content;
3. **UCF's Kuali record reports `labStudioFieldWorkHours: 0`** — a structured data point, not an inference;
4. **neither carrier's title mentions a lab** (UCF *Medical Botany*, UWF *Medicinal Botany*).

**Why it is worth your attention rather than just a guide footnote.** ⚠⚠ **This one can cost a student a
graduation requirement.** Many degree programmes require a general-education science course **with a
laboratory**. A student — or an adviser — reading the statewide title would reasonably conclude this
course satisfies that requirement. It does not, and the error is discovered at a degree audit.

**What was done.** The guide states the contradiction prominently, gives all four signals, and tells the
reader the course has no laboratory and will not satisfy a science-with-lab requirement. No content was
taken from the title.

**Decision wanted from Ron:** whether a statewide-record defect of this kind is worth reporting to SCNS.
⚠ **This is the second title/description contradiction the project has found in the state file**
(`SPM3104` was the first, batch 207) and the first where the consequence is a concrete student-facing
error rather than a scope question. **No action needed on the site** — the guide handles it.

## 97. ⚠ The flat file's `transferable` field holds the HIGH-SCHOOL-CREDIT code — batch 212's note corrected (batch 214)

**Batch 212 recorded** that `scns.FIELDS`' `hs_credit` read blank while `transferable` read `'EL'`, against
a statewide CSV saying HS *ELECTIVE* and transferable *"GUARANTEED TRANSFER…"* — and concluded that both
fields were uniform across `ATF`/`ATT` and therefore carried no information.

**`BOT` and `BSC` resolve it.** The flat-file `transferable` field splits **`'EL'` / `'SC'`**, which maps
exactly onto the statewide CSV's **ELECTIVE / SCIENCE** high-school-credit values (`BOT` 116/6, `BSC`
248/24). ⚠ **So the two-character code sitting in the `transferable` slot IS the high-school credit code**,
and the byte offsets for that field pair in `scns.FIELDS` are shifted.

**Practical rule, now recorded in `SOURCES.md`:** read `DS_High_School_Credit1` and `DS_Transferable1`
from the **statewide CSV**, not from the flat file's `hs_credit` / `transferable` fields. The flat file
remains authoritative for carriers, credits, titles and the Gordon Rule / general-education flags.

**Decision wanted from Ron:** whether to **fix the offsets in `scratchpad/scns.py`** or leave the note.
⚠ **Recommend leaving them and relying on the CSV.** Correcting byte offsets on an 80 MB fixed-width file
risks silently shifting every field after the edit, and no guide currently depends on those two fields
from the flat file. **If a future task needs them at scale, fix it then and re-validate against the CSV
for a whole prefix before trusting it.**


## 98. ⚠⚠⚠ `HFT3271` — FOUR subjects on one number, and NO carrier teaches the statewide one (batch 218)

**PULLED from batch 218 and marked `skipped` pending your decision. This is the most severe collision the
project has found — worse than `TPA3230C` (item 25), which was also pulled.**

| Source | Subject |
|---|---|
| **Statewide title AND description** | **Condo/Resort Management** — *"operation of condominium/resort properties&hellip; planning, development, financial investment and marketing&hellip; the condominium hotel concept, time sharing"* |
| **FIU** | ⚠ **Nightclub Management** |
| **FGCU** | ⚠ **Club Management** |
| **UWF** | ⚠ **Spa Management** — *"facial therapies, massage therapies, water therapies, face and body services, salon services, exercise, personal training"* |

⚠⚠⚠ **Four subjects, and the statewide reading has NO carrier at all.** Writing the statewide subject
would describe a course nobody teaches; writing any carrier's subject would misdescribe the number for the
other two.

**The misfiling diagnostic fires hard — Florida numbers every one of these separately:**

| Subject | Dedicated statewide numbers |
|---|---|
| Spa | `HFT2204` Spa Operations and Management, `HFT2209` International Spa Management, `HFT4854` Spa Client Wellness |
| Club | `HFT2100` Introduction to Global Club Management, `HFT4434` Club Management, `HFT2277` Resort and Club Management |
| Condo/resort | `HFT2271` **itself**, plus `HFT2273` Principles of Resort Timesharing, `HFT2276` Resort Management, `HFT2278` Residential Hospitality-Condominium Management |

**So all three carriers are misfiling, in three different directions, onto a number whose own subject is
separately and thoroughly numbered.**

⚠⚠ **The student-facing consequence is concrete and not merely a cataloguing curiosity.** Spa management,
club management and condominium/resort management are **different professional specialisms with different
employers and different career structures** — private club management in particular is a distinct
profession with its own association (CMAA) and certification. **A student transferring this credit, or an
adviser matching it against a degree requirement, cannot tell from the number which of four subjects it
represents.**

**Decision wanted from Ron.** Options as I see them:

1. ⚠ **Leave it skipped** (current state) — honest, and the course simply has no guide.
2. **Write a disambiguation page at the bare number** naming all four subjects and pointing at the
   dedicated numbers above, with no attempt to describe a single course. **This is my recommendation** —
   it is the most useful thing a reader can be given, and it is what the bare-number page in the
   `-SCNS`/`-<INST>` rule is for.
3. **Full split** — `-SCNS` (condo/resort), `-UWF` (spa), `-FGCU` (club), `-FIU` (nightclub) plus a
   disambiguation page. ⚠ **Five pages, and three of the four halves are sourceable** (UWF via its
   catalogue, FIU and FGCU only by title), so this is not currently well-founded.

## 99. ⚠⚠⚠ `HFT4252` — the statewide TITLE and DESCRIPTION contradict each other, and the CARRIERS SPLIT (batch 218)

**A FOURTH configuration of the title/description test, and it defeats the rule as corrected in batch 215.**

| Source | Says the subject is |
|---|---|
| **Statewide TITLE** | *Employees Wellbeing in Hospitality and Tourism* |
| ⚠ **Statewide DESCRIPTION** | *"managerial functions, operating procedures, and competencies [of] hotel and resorts&hellip; management, ownership, franchising"* — **hotel and resort management** |
| **UCF** | *Employees Wellbeing in Hospitality and Tourism* — **backs the TITLE** |
| **Pensacola State** | *Hotel and Resort Management* — **backs the DESCRIPTION** |

**Batch 215 corrected the batch-208 rule to say that when title and description disagree, THE CARRIERS
decide which element is stale.** ⚠⚠⚠ **Here the carriers split one on each side, so the test returns no
answer.** That is a genuinely new outcome and I have recorded it in `CLAUDE.md` as a fourth branch.

⚠ **Both subjects are numbered elsewhere in the prefix** — wellbeing at `HFT2014` *Wellness Management in
Hospitality and Tourism* and `HFT4793`; hotel/resort at `HFT2250`, `HFT2256`, `HFT2276`, `HFT2004`. **So
neither carrier needed this number for what they are teaching.**

**What was done.** The guide was **published covering BOTH readings, each clearly labelled**, with a
two-column syllabus diagnostic, the alternative numbers, and an explicit warning that the course number
does not identify the subject and that transfer must go on the syllabus. **That follows the `CLP4302` and
`APK4200` precedent** for a number carrying two genuinely different subjects where a full split is not
soundly sourceable — Pensacola State's catalogue is unreachable, so a `-PESC` half could only be written
from a title.

**Decision wanted from Ron:** whether to leave the combined guide or split it once Pensacola State becomes
reachable. ⚠ **Recommend leaving it.** The combined guide serves a student at either institution, and a
split would currently rest on one title.

## 100. ⚠⚠ `CCJ` splits courses by SECTOR across two numbers — two confirmed, and the prefix should be swept (batch 220)

**Not a correction request — the finding is already written into the live guides. This is a scope
decision about how far to chase it.**

**What is confirmed.** Florida numbers the same criminal justice course twice, split cleanly along the
FCS/SUS line, in **two** places in this one prefix:

| Subject | FCS number | SUS number |
|---|---|---|
| Introductory criminal justice (batch 182) | `CCJ1020` — Broward, EFSC, Valencia | `CCJ2002` |
| ⚠⚠ **Criminal justice administration** (batch 220) | **`CCJ2452`** — Polk State, Valencia, Florida Gateway, State College of Florida, Tallahassee State (**all five FCS**) | **`CCJ3450`** — UCF, UWF (**both SUS**) |

⚠⚠⚠ **The second is the more damaging, and the reason is the LEVEL.** `CCJ1020`/`CCJ2002` are both
lower-division, so an A.A. completer's protections absorb much of it. **`CCJ2452` is 2000-level and
`CCJ3450` is 3000-level, and a 2000-level course cannot supply upper-division hours toward a Florida
baccalaureate** — so a state-college student who takes the subject may have to take it again at the
university, **not because the content differs but because the level does.** Seven institutions, two
numbers, zero crossover.

**Already done, no action needed on these:**

- ✅ **`CCJ3450`'s live guide** carries the full table, the upper-division-hours consequence and the
  "get a written answer from the receiving department first" instruction, in both the body and the
  prerequisite field.
- ✅ **All four batch-220 guides** carry the prefix-wide "check the number, not just the title" caution.
- ✅ **`CLAUDE.md`** records both rows and the generalised drill.

**Decision wanted from Ron — two questions.**

1. ⚠ **Should `CCJ` be swept for further instances?** Two confirmed in the two numbers we happened to
   look at is a poor sample. The cheap version is one `survey.py`-style pass over the prefix looking
   for **pairs of active numbers sharing a statewide title at different levels with disjoint carrier
   sectors** — perhaps twenty minutes, and it would either produce a list or close the question.
   **My recommendation: yes, and do it as a one-off report rather than course by course.**
2. ⚠ **Does `CCJ2452` deserve its own guide?** It is carried by **five** FCS institutions — more than
   `CCJ3450`'s two — and it is currently listed without a guide. It is not in `queue.csv`. Under the
   2026-09-11 direction a guide-less listed course is a finished outcome, so **the default is to leave
   it**; but a five-carrier lower-division course that half the state's CJ students take is an unusually
   strong candidate if you want one. **My recommendation: leave it unless a visitor requests it** —
   `CCJ3450`'s guide already tells a `CCJ2452` student what they need to know.

⚠ **Generalisable either way:** the drill now in `CLAUDE.md` is *"where a prefix is found to split one
course by sector, check its other high-enrolment numbers before writing any of them."* **If the sweep in
(1) is worth running on `CCJ`, it is probably worth running on every prefix with both FCS and SUS
carriers** — which is most of the vocationally-adjacent ones.

## 101. ⚠⚠⚠ `JOU4306` — two unrelated subjects on one number, and a SPLIT is soundly sourceable (batch 224)

**A `-SCNS` / `-<INST>` split candidate that meets every condition of the 2026-09-04 rule. Published
for now as ONE guide covering both readings, labelled, pending your decision.**

| Institution | Its title | What the course is |
|---|---|---|
| **UWF** | **Writing Critical Reviews** | *"Devoted to writing reviews of books, film, art, and music."* — **arts criticism, a writing course** |
| **UF** | **Advanced Data Journalism** | *"Blends journalism and data science&hellip; learn to **program in R** to replace spreadsheets and databases with **reproducible data analysis**."* — **a programming and statistics course** |

⚠⚠ **They share no content, no skills, no textbook and no career path.** **That is the `EEE4775`
standard** — the case `CLAUDE.md` records as *"the cleanest collision found so far."*

### Why this is unusual even among collisions

⚠⚠⚠ **The statewide record is internally consistent and STILL cannot adjudicate.** Title: *Critical
Journalism*. Description: *"critical thinking and analysis as employed in the profession of
journalism."* **They agree with each other — and both readings fit.** Writing a review is critical
thinking; analysing a dataset is analysis. **Every previous collision was settled by the
title/description test or by a dedicated number. Neither works here.**

**And the dedicated-number tell fails too, in an informative way:**

| Number | Statewide title | Public carriers |
|---|---|---|
| `JOU3305` | Data Journalism | **UF — and only UF** |
| `JOU4305` | Data Journalism | ⚠⚠ **none** |
| `JOU4015` | Journalism Culture and Criticism | ⚠⚠ **none** |

⚠ **Dedicated numbers exist for BOTH readings and BOTH are dormant**, so neither carrier had a live
alternative. **And UF files the introductory data course correctly on `JOU3305`** — what Florida does
not provide is an **advanced** data journalism number, so UF took an available one for a genuine
two-course sequence. **UF is not being careless; it is working around a gap.**

### Both halves are sourceable — which is what the split rule requires

| Half | Source | Quality |
|---|---|---|
| `-UWF` (criticism) | UWF prefix PDF | ✅ full description, Gordon Rule flags confirmed |
| `-UF` (data) | UF CourseLeaf department page | ✅ full description **and** prerequisite chain |
| `-SCNS` | statewide record | ⚠⚠ **this is the problem — see below** |

⚠⚠⚠ **The `-SCNS` half is the obstacle, and it is a new one.** The rule says a `-SCNS` guide needs the
state catalogue's **definition** of the course, not just its title. **Here the statewide definition is
one vague sentence that describes neither carrier distinctly.** **There is no third, state-defined
subject to write.**

### Options as I see them

1. ⚠ **Leave the combined guide** (current state). It covers both readings, labels each, gives a
   prerequisite-based test for telling them apart, and warns explicitly never to transfer this number
   on the number. **Precedent: `CLP4302`, `APK4200`, `HFT4252`.**
2. **Two-page split — `JOU4306-UWF` and `JOU4306-UF`, plus a disambiguation page at the bare number,
   and NO `-SCNS` page.** ⚠⚠ **This is my recommendation if you want a split.** Both institutional
   halves are well sourced; the statewide half has nothing to say. **It departs from the three-page
   shape, and the reason is specific and documented rather than convenience.**
3. **Full three-page split including `-SCNS`.** ⚠ **I would not do this** — the `-SCNS` page would be
   written from a single ambiguous sentence, which is close to inventing content.

**My recommendation: option 1 or 2, and I lean to 1** — the combined guide already tells a student
everything option 2 would, and the collision is genuinely unadjudicable rather than a case of one
institution being wrong. ⚠ **If you want the split, option 2 is the sound shape.**

### Related, and cheap to fix if you ever want it

⚠ **`JOU4305` Data Journalism and `JOU4015` Journalism Culture and Criticism are both dormant
statewide numbers that exactly describe what the two carriers teach.** **If SCNS were ever to be
asked, moving each carrier onto its correct number would dissolve the problem entirely.** Noted
because it is the kind of thing a state articulation officer can actually act on, unlike most findings
in this file.

## 102. The STUDIO contact-hour convention contradicts itself — and `GRA` now holds three answers

**Raised batch 227 (2026-09-16). Needs one decision for the prefix, not five.**

`validate_drafts.py` carries a **studio-prefix rule** (added 2026-09-11) expecting a 3-credit studio
course to run **~90 contact hours** — six hours a week, "because the work is made in the room." It was
added after `GRA3112C` and `GRA4154C` tripped the lecture heuristic at 90, "which was the correct figure
for a studio."

⚠⚠ **That rule now contradicts your 2026-09-15 ruling** (`C` suffix = 60, no suffix = 45), and the
published data shows the collision inside a single prefix:

| Figure | Courses |
|---|---|
| **90** | `GRA3112C`, `GRA4154C` |
| **72** | `GRA2111C`, `GRA2134C`, `GRA2208C`, `GRA3102C` |
| **60** | `GRA2144C`, this batch's five, **and 25+ `ART` studio `C` guides** |

⚠ **No Florida institution publishes contact hours for ANY `GRA` course**, so all three figures are
derived by convention and none is sourced. The prefixes the validator treats as studio are `ART ARE GRA
PGY CRW DAA DAN THE TPA TPP MUS IND INT` — so this reaches well beyond `GRA`.

**What I did in batch 227, and why:** published all five at **60**, following your explicit and more
recent ruling, with the derivation stated in every guide and labelled as derived. **I did not want to
invent a third convention silently**, and the warning is non-blocking.

**The decision I need:**

1. ⚠ **`C` = 60 everywhere, including studio prefixes** — consistent with your ruling and with the large
   majority of published studio guides. **Then the validator's studio rule should be removed or lowered**,
   because it will warn on every studio guide from here on, and a warning that always fires stops being
   read. `GRA3112C` and `GRA4154C` would be the outliers to revisit.
2. **Studio prefixes get 90** — defensible on national studio-accreditation practice (a 3-credit studio
   commonly meets six hours weekly), and it is what the two existing `GRA` guides say. ⚠ **But it would
   make ~30 already-published `ART`/`GRA` guides wrong**, and it contradicts the `C` = 60 ruling.
3. **Something in between** (the 72 figure already in four guides) — I would not recommend this; it has no
   stated basis I can find and would be a third convention.

**My recommendation: option 1**, with the validator rule retired. It matches your ruling, matches most of
what is published, and the honest position is that **none of these numbers is sourced** — every guide says
so, which is the part that actually protects the reader.

⚠ **Whichever you pick, it is a small mechanical sweep**, not a rewrite: the figure lives in one field and
in one sentence of the Special Information section.


## 103. ⚠⚠⚠ CIP codes are the career-path anchor — and institutions disagree on 7% of them (batch 230)

**Raised 2026-09-16, ahead of the career-paths phase. Not blocking; it is a DESIGN input for that build.**

You settled that careers will be bound to CIP codes
(`https://nces.ed.gov/ipeds/cipcode/browse.aspx?y=55`). **Anchoring the CAREER on a CIP is sound** —
that is the end of the mapping where CIP is authoritative. **This item is about the other end: binding
COURSES to it.**

### What is already banked, at no cost

`cip_map.py` (new) harvests course → CIP from the Coursedog caches, the only Florida source that
exposes a per-course `cipCode`. **25,412 courses mapped today** — FIU 25,188, FAU 7,120, NWFSC 708.
⚠ **FSCJ contributes nothing**: 2 rows out of 22,698, both the placeholder `9999999999`.

### ⚠⚠ The measurement you will want before designing the mapping

Over the **1,500 courses carried by two or more of those institutions**:

| | Count | Share |
|---|---|---|
| Institutions **agree** exactly | 763 | 51% |
| Disagree **within the same 2-digit family** | 631 | 42% — benign granularity |
| ⚠⚠ **Disagree across DIFFERENT families** | **106** | **7%** |

**Read it as 93% agreement at family level, not 49% disagreement** — most of the noise is one
institution choosing a finer sub-code.

**But the 7% is severe, and it is the same class of problem this project has spent 200 batches
documenting for course numbers:**

| Course | Classified as |
|---|---|
| ⚠⚠⚠ **`ART1300C`** (Drawing) | FAU **50.0701 Fine Arts** · NWFSC **13.1302 Art Teacher Education** |
| ⚠⚠⚠ **`ART2501C`** | FAU **50.0701 Fine Arts** · NWFSC **36.1096 Leisure and Recreational Activities** |
| `ANT2100` | FAU **45.0201 Anthropology** · NWFSC **30.0000 Multi/Interdisciplinary** |
| `ADV3008` | FAU **52.0101 Business** · FIU **09.0101 Communication** |

**The same drawing course is fine art at one school, teacher education at another and a recreational
activity at a third.** A pathway routing students by course CIP alone would send three students with
identical coursework to three different careers.

### What I would recommend, for your decision

1. **Anchor careers on CIP** — as you specified. No change.
2. ⚠⚠ **Do not derive a COURSE's pathway membership from its institution-assigned CIP alone.** Use
   it as one signal beside the statewide subject and the prerequisite graph, which is what the guides
   already capture.
3. **Where institutions disagree, store BOTH.** The disagreement is a real fact about how the course
   is used, and hiding it would reintroduce exactly the trap the `-SCNS`/`-INST` split exists to avoid.
4. ⚠ **Compare at the 2-digit family first.** Comparing 6-digit codes reports 42% of benign
   granularity as conflict.

⚠ **One thing worth your steer now rather than later:** whether the career-paths data model should
carry a course→CIP edge **per institution** (which the data supports and which is honest) or a single
canonical CIP per course (simpler, and wrong 7% of the time). **That choice is cheap now and expensive
after the schema is built.**

⚠ **This is cross-session:** the career-paths build lives in the root session
(`CAREER_PATHS_PLAN.md`), and this finding comes from the `Tools/` side. **Worth carrying across
before that build starts.**


## 104. ⚠⚠⚠ FGCU's catalogue has stopped returning course content (batch 231)

**Raised 2026-09-17. Not blocking — but it is the loss of the project's best cross-check source, and
you may have a route to it that I do not.**

`catalog.fgcu.edu/courses/<prefix>/<prefix>.pdf` now returns an **empty 202** on every prefix tried:
**`phi`, `mue`, `bsc`, `egn`, `eng` — 6 requests across 2 days.**

⚠ **Why this matters more than an ordinary block.** The source register describes FGCU as *"the single
most productive cross-check source in the project"*: it documents credits explicitly and produced the
divergence a guide turned on in three consecutive batches. **It is also frequently the SECOND carrier
on a two-carrier course**, which is exactly where a guide most needs independent corroboration. Two
guides in the last two batches say so explicitly — `MUE4344` (the misfiling case, where FGCU is the
ONLY carrier) and `PHI3200`.

⚠⚠ **I have NOT recorded it as permanent, deliberately.** The batch-183 rule says state-college
blocks are rate-triggered and warns against concluding from a burst. **Six requests over two days on
five prefixes is past that**, but Broward and Valencia have both gone blocked → recovered → blocked
before. **The register row now says "blocked as of 2026-09-17 — re-probe", and I probe it at session
start.**

**What I would like from you, if either is easy:**

1. **Whether FGCU has another public route** — a Coursedog or Kuali instance, or a catalogue PDF served
   from a different host. I have not found one, but I have only probed the CourseLeaf pattern.
2. ⚠ **Whether it is worth asking FGCU directly.** This is a public state university catalogue and the
   project is building a public student resource for Florida; **a request for access is the kind of
   thing that sometimes simply works**, and it would also settle UNF, which has been blocked at the
   host for longer.

**No decision is needed to keep working** — guides name the gap where FGCU could not be read, which is
the honest handling. This is about recovering a source, not unblocking the queue.


## 105. ⚠⚠ `PHC4109` (live) tells the reader a masked course number cannot be looked up — it can (batch 234)

**Raised 2026-09-17. A correction candidate on a guide I published two batches ago. Small, and mine.**

**What the live guide says.** `PHC4109`, published in batch 232, states that the statewide description's
*"offered concurrently with `PHC 5XX3`"* names a number that is **"not a real course number — the `XX`
is a placeholder that was never filled in, so there is nothing to go and look up."**

⚠ **The first half is right and the second half is wrong.** Batch 234 established that a masked number
in a dual-listing note is usually recoverable, because **the masked number is followed by the course's
actual title.** Searching statewide titles in the same prefix finds it: **`PHC 5XX3 (Scientific Basis of
Public Health)` → `PHC?123`, GRADUATE.**

**Why it matters rather than being a nicety.** The guide also carries the dual-listing warning — that
taking the undergraduate version may block taking the graduate one for credit later. ⚠⚠ **That warning
is much less useful if the student cannot identify which graduate course it applies to**, and the whole
point of the warning is that they should ask before registering.

### The exact fix

Replace the sentence saying there is nothing to look up with one naming the graduate partner:

> *"The statewide record masks the graduate partner's number as `PHC 5XX3`, which is not a real
> identifier — but the course it names is findable: Florida carries **Scientific Basis of Public
> Health** at graduate level under `PHC?123`. Ask your department whether taking this course affects
> your ability to take the graduate version for credit."*

⚠ **I have not republished.** Republishing overwrites live content and bumps the version, which waits
for your go-ahead (the item 81 precedent). **Say the word and it is a one-line edit and a v1.1 push.**

### ⚠ And the same check is worth running across the back catalogue

The scan that produced this found **220 wildcard tokens across 41 statewide prefixes**, and masked
numbers inside "offered concurrently with" notes are a recurring shape (`GEO 5XX3` and `PHC 5XX3` both
turned up). **Any already-published guide that quoted a masked number may have the same understatement.**
**That is a cheap grep over `drafts/` if you want it done as part of the verification pass** rather than
one guide at a time.


## 106. ⚠⚠⚠ 81 PUBLISHED GUIDES SIT ON MINORITY COURSE IDS — including the ENTIRE Florida math gateway (measured 2026-09-17)

**Found while placing prerequisites on the Registered Nurse path; MEASURED while starting the
Mechanical Engineer path, which cannot name a calculus course without hitting it.**

**The site lists a `C`- or `L`-suffixed id, publishes a guide on it, and does NOT list the bare id
that almost every Florida institution actually carries.** A student searching the number their own
college uses finds nothing.

### The measurement

`scratchpad/suffix_audit.py` — the live catalog (20,000 listed courses) against the SCNS flat file
(67,189 active ids with a public carrier):

> **170 listed ids are the minority form of a much better carried twin.**
> ⚠⚠ **81 of them carry a PUBLISHED GUIDE while the majority twin is NOT LISTED AT ALL.**

### ⚠⚠⚠ The worst of it is the gateway sequence every degree in Florida runs through

| Listed (with a guide) | carriers | The id students actually use | carriers | Listed? |
|---|---|---|---|---|
| `MAC2311C` Calculus I | **2** | **`MAC2311`** | **39** | ❌ **NO** |
| `MAC2312C` Calculus II | **1** | **`MAC2312`** | **37** | ❌ **NO** |
| `MAC2313C` Calculus III | **1** | **`MAC2313`** | **36** | ❌ **NO** |
| `MAP2302C` Differential Equations | **1** | **`MAP2302`** | **37** | ❌ **NO** |
| `MAC2233C` Business Calculus | **1** | **`MAC2233`** | **36** | ❌ **NO** |
| `MAC1105C` College Algebra | 10 | **`MAC1105`** | **36** | ❌ **NO** |
| `MAC1140C` / `MAC1114C` | 1 / 1 | `MAC1140` / `MAC1114` | 31 / 33 | ❌ **NO** |
| `MAT1033C` Intermediate Algebra | 4 | `MAT1033` | 30 | ❌ **NO** |
| `ENC1101C` Composition I | 3 | **`ENC1101`** | **39** | ❌ **NO** |
| `STA2023C` Statistics | 1 | **`STA2023`** | **39** | ❌ **NO** |

**Also affected:** `AST1002`, `OCE1001`, the `MUT` music-theory sequence, `CJK0096`/`CJK0340`
(law-enforcement academy), `FRE1120`, `MVK1111`, `MVS2326`. ⚠ **`FFP2120C` has ZERO public
carriers and carries a guide** — that id exists nowhere in Florida.

### Why it matters more than the count suggests

1. ⚠⚠ **These are the highest-enrolment courses in the state.** Calculus I and freshman
   composition are taken by a large fraction of everyone in Florida public higher education.
2. ⚠⚠⚠ **IT BLOCKS THE CAREER PATHS.** Every engineering path names the calculus sequence;
   Registered Nurse and Lawyer already name `STA2023` and `ENC1101`. A path can only render those
   as *"not listed yet"* rather than as links. **The ENG cluster is 10 of the queued 50 and every
   one of them hits this.**
3. **The guides themselves are fine.** This is a filing problem, not a content problem — which is
   why it is cheap to fix and expensive to leave.

### ⚠ What needs deciding — and it is one decision, not 81

**The listing half is ordinary pipeline work and needs no decision:** send base data for the
majority twins so they exist as pages with a Request Guide button. That alone unblocks the career
paths.

⚠⚠ **The guide half is Ron's call, because it republishes live content.** Three options:

| | What happens | Cost |
|---|---|---|
| **A. Move the guide to the majority id** | the guide appears where students look; the `C` id keeps a listing with no guide | 81 republishes, and the `C` guide has to be withdrawn or redirected |
| **B. Publish at BOTH ids** | nobody searches in vain | 81 duplicate guides to keep in step forever |
| **C. List the twin, leave the guides** | cheapest; the majority id gets a page and a Request Guide button | the guide stays on the id 1-3 colleges use |

⚠ **Recommendation: A for the ten gateway rows above, C for the tail.** The gateway courses are
where the harm concentrates, and ten republishes is a small, checkable batch. **The `FFP2120C`
row needs its own answer** — a guide on an id no institution carries.

### ⚠⚠⚠ ROOT CAUSE FOUND (2026-09-17) — the master inventory carries the WRONG FORM

**`courses_2plus_institutions.csv` contains `MAC2311C` and does NOT contain `MAC2311`.** Same for
`STA2023`/`STA2023C`, `ENC1101`/`ENC1101C`, `BSC2085`/`BSC2085C`.

```
  MAC2311    0 rows in the inventory        MAC2311C   1 row
  STA2023    0 rows                          STA2023C   1 row
  ENC1101    0 rows                          ENC1101C   1 row
```

⚠⚠ **So the queue could NEVER have produced a guide on the right id.** Every guide in this item
was written correctly from a defective worklist. **3,571 inventory ids have no bare twin in the
inventory at all** — most legitimately (`C`-only courses), but the subset measured above is not.

⚠ **And it blocks the fix through the normal route:** `queue_mgr.py add` refuses any course absent
from that inventory, so `MAC2311` **cannot be queued** by the standard command. That is why
path-derived demand now comes from `career_paths.py needs` instead, which reads the ids the paths
actually name.

⚠⚠ **Regenerating the inventory from the SCNS flat file is the real repair** and would
prevent recurrence across the remaining ~800 queued rows. **That is a separate decision** — it
changes the worklist the whole project has been running on.

### ⚠ CORRECTION (2026-09-17): the first counts I published were ROWS, not INSTITUTIONS

**The early ad-hoc checks counted flat-file ROWS. An institution can hold several active rows for one
id** — honors sections, campuses — **so the figures overstated by roughly a third.** `suffix_audit.py`
counts distinct institutions and was right; the hand checks that fed this item and two live career
paths were not.

| id | rows | **distinct institutions** |
|---|---|---|
| `STA2023` | 52 | **39** |
| `ENC1101` | 51 | **39** |
| `MAC2311` | 49 | **39** |
| `BSC2085` | 25 | **20** |

✅ **Corrected in `REVIEW_QUEUE`, and both live career paths were re-pushed with the right numbers.**
⚠ **Standing check: count DISTINCT institution codes, never rows.**

### ✅✅ AND A SHAPE THE COUNTS HID: `BSC2085` IS NOT THE SAME COURSE AS `BSC2085C`

**Ron's ruling that `MAC2311` and `MAC2311C` are the same holds for MAC — both are 4 credits. It does
NOT hold for the anatomy sequence, and the credit column says so:**

| | credits | carriers | |
|---|---|---|---|
| `BSC2085` | **3** | 20 | the LECTURE only |
| `BSC2085L` | **1** | 19 | the LABORATORY |
| `BSC2085C` | **4** | 7 | both, integrated |

⚠⚠⚠ **19 institutions carry the bare id AND the `L`; SEVEN carry the `C`; and NO institution
carries both forms.** That is the split-family shape at its cleanest — perfectly disjoint carrier sets.

✅✅ **RESOLVED BY RON, 2026-09-17, and the first framing of this was WRONG:** *"In both cases the
outcomes are the same… For transfer Classroom + Lab (L) = completed just as completing as combined."*
**So this is not a defect and not a transfer risk.** I had written that `BSC2085` alone does not
satisfy a nursing prerequisite; **that overstated it and is corrected on the live path.** The notes now
say the two packagings are equivalent and tell the reader to register for whichever pair their own
catalogue lists. See the PACKAGING IS NOT DIVERGENCE rule in `CLAUDE.md`.

⚠ **So "the bare and the C id are the same course" must be checked against the CREDITS before it is
asserted** — it is true for MAC2311 and false for BSC2085.

### ✅ PROGRESS (2026-09-17)

- **Ron's ruling:** *"MAC2311 and MAC2311C are the same. MAC2311(C) should have a guide. If you run
  into a course that spans a major associated to the career path the rule is to complete the
  guide."*
- ✅ **909 courses LISTED** across `MAC MAP MAT STA ENC` from the flat file (0 failed), so
  `MAC2311`, `MAC2312`, `MAC2313`, `MAP2302`, `STA2023`, `ENC1101`, `MAC1105`, `MAC2233` and
  `MAT1033` now exist as pages with real titles and full offering lists. **Both live career paths
  re-pushed with no unlisted courses remaining.**
- ⏳ **Guides still owed on the four courses published paths name:** `ENC1101` and `STA2023` (each
  on TWO paths), `BSC2085`, `BSC2086`. Run `python career_paths.py needs`.
- ⏳ **Still open:** what happens to the 81 guides sitting on minority ids, and the `FFP2120C`
  guide on an id no institution carries.

## 107. ⚠⚠⚠ FLORIDA NUMBERS GENERAL CHEMISTRY TWO WAYS — and 35 live guides name only one of them (found 2026-09-18)

**The most-taken college science course in Florida is carried under two parallel numbering families,
split almost evenly across the system, and NO institution carries both.**

| Family | Institutions | Who |
|---|---|---|
| `CHM1045`/`CHM1046` (or the `C` forms) | **19** | Broward, Daytona State, EFSC, **FAMU**, **FGCU**, Florida Keys, **FSU**, **FIU**, Gulf Coast, IRSC, **Miami Dade**, North Florida, NWFSC, Palm Beach State, Pensacola State, Polk State, SJRSC, Tallahassee State, **Valencia** |
| `CHM2045`/`CHM2046` (or the `C` forms) | **20** | CF, FAU, Florida Gateway, Florida Poly, FSCJ, FSW, Hillsborough, Lake-Sumter, New College, Pasco-Hernando, SCF, Santa Fe, South Florida State, St. Petersburg, Seminole State, **UCF**, **UF**, **UNF**, **USF**, UWF |
| **both** | **0** | — |

⚠ **The one anomaly: Santa Fe College uses `CHM2045` for the first course and carries BOTH
`CHM1046` and `CHM2046` for the second.**

⚠⚠ **FOUR public universities are in the 1000 family — Florida State, Florida A&M, FIU and FGCU —
along with the three largest state colleges.** This is PARALLEL NUMBERING FAMILIES (batch 219) on the
highest-enrolment science course in the state.

**It is benign for TRANSFER** — both families are lower division and the sequences articulate — **and it
is a guaranteed FAILED SEARCH**, the `SPN3410` ordinal-base shape (batch 203). A student who does not
know two families exist cannot know they are looking in the wrong one.

⚠⚠⚠ **And it collides with a warning the state prints on the SECOND course of the sequence:**
*"a sequence once started should be taken entirely at one institution … only the COMPLETED sequence at
one institution is equivalent to a completed sequence at another."* **Crossing families mid-sequence is
exactly what the state tells students not to do.**

### ⚠⚠⚠ CONFIRMED AS A PATTERN, NOT A CHM QUIRK (2026-09-18, batch 241)

**The same split exists in majors biology, measured the same way:**

| Family | Institutions |
|---|---|
| `BSC1010`/`BSC1011` (or the `C` forms) | **16** |
| `BSC2010`/`BSC2011` (or the `C` forms) | **23** |
| **both** | **0** |

⚠⚠ **Two of two.** Both of Florida's gateway science sequences run under parallel 1000- and
2000-level families with no institution in both. **So this is a property of the gateway sciences,
and any future path or guide naming a gateway science course should give both numbers.**

⚠⚠ **And the SIBLING BEHAVIOUR is identical too:** in both sequences the FIRST course carries the
**`(GE CORE)`** marker and returns **ELECTIVE** high-school credit, and the SECOND carries neither
marker and returns **SCIENCE** credit. **A dual-enrolled student taking the first half of both
gateway sequences may earn no high-school science credit from either.**

✅ `BSC2010` and `BSC2011` were written in batch 241 carrying the finding, so the biology half needs
no sweep. **The open question below is unchanged and still concerns the CHEMISTRY half only.**

### ✅ Already done — no decision needed on these

- **Six live career paths corrected and re-pushed** (aerospace, chemical, civil, electrical,
  industrial, mechanical engineer) with a `variantNote` naming both families, the packaging axis, and
  the sequence warning.
- **`CHM2045` republished at v1.1**, additively: the verified v1.0 content was pulled from the live
  API and kept, with the two-family and dual-enrolment blocks spliced into Special Information.
- **`CHM2046`, `CHM2210`, `CHM2211` written** (batch 239) carrying the finding.

### ⚠ WHAT NEEDS RON — the retro-sweep, and it is one decision, not 35

**35 already-published guides name `CHM2045` or `CHM2046` and never mention the 1000-numbered
family.** They are not WRONG; they are incomplete in the way `CHM2045` v1.0 was, and a reader at Florida
State, FIU, Broward or Miami Dade would not learn that their own course is the one being described.

```
ANT2511L ANT4180L BSC1010C CHM1015 CHM1020 CHM1020C CHM1020L CHM1024 CHM1025
CHM2210C CHM4130C EEE3394 EEE4330 EGN1001C EGN3343C EGN3365 ENV4102 GEO4280C
HUN2201 MCB1000 MCB1000L MCB2010 MCB2010L MCB3020 MCB3020L MCB4203 MCB4276
MLS3194 OCB3108L PCB3103L RET3028 RET3028L RET3493 RET3493L RET3884
```

**The options, cheapest first:**

1. **Do nothing.** The paths and the four chemistry guides now carry the finding, and most of these 35
   mention the prerequisite only in passing.
2. ⚠ **Sweep only where it is load-bearing** — the ones where general chemistry is a stated
   PREREQUISITE rather than a mention. `MCB`, `BSC`, `RET`, `HUN` and `MLS` feed health-professions
   programmes whose students are disproportionately at Miami Dade, Broward and Valencia — **all three
   in the 1000 family** — so those are where the omission actually costs someone.
3. **Sweep all 35** with the same additive splice used on `CHM2045`, which is now tooled
   (`scratchpad/chm2045_fix.py`) and mechanical: pull live, splice, bump version, push.

⚠ **Recommendation: option 2.** ⚠⚠ **`CHM2210C` should be fixed regardless of the decision** — it is
the integrated twin of `CHM2210`, which was published in batch 239 carrying the finding, so the two
halves of one split family now disagree with each other.

---

## 108. ⚠⚠ `ECH3854`'s statewide prerequisite resolves for NOBODY — recorded, not blocking (found 2026-09-18)

**Documented here because it is the clearest instance of a general rule and worth citing, not because
anything is blocked.** The guide published in batch 240 states it fully.

`ECH3854` Chemical Engineering Computations is carried by **FAMU, Florida State and USF**. Its
statewide prerequisite names three courses:

| Named | Who carries it | Resolves for a carrier? |
|---|---|---|
| `ECH3264` | **University of Florida alone** | ⚠ **no — and UF does not carry `ECH3854`** |
| `CGS3460` | ⚠⚠ **no Florida public institution at all** | **no, for anybody in the state** |
| `MAP3305` | FAMU, FAU, Florida Poly, FSU | not at USF |

⚠⚠⚠ **Both dangling numbers are University of Florida numbering, and UF does not teach the
course** — the `JOU3342` shape (batch 224): a prerequisite contributed by a department that does not
teach the course. **Two of the five documented defect shapes in one field.**

⚠ **It is the best available teaching example of the standing rule: a statewide prerequisite is
contributed by ONE institution and is not a promise about yours.** No action needed.


## 109. ⚠⚠⚠ `scns.is_public()` EXCLUDES DISTRICT TECHNICAL COLLEGES — which is the whole CTE sector (found 2026-09-20, automotive path)

**`sector_of()` answers `SUS`, `FCS` or `other`, and every district technical college answers
`other`.** Every tool in this repo filters on `is_public()`, and Ron's 2026-09-11 scope rule —
*"we will only do public institutions"* — has therefore been applied as *state colleges and
universities only*. ⚠ **District technical colleges are PUBLIC**: they are operated by school
districts, they teach the state's own CTE frameworks, and they are where Florida actually trains
technicians.

**The measurement, from the automotive frameworks:**

| | |
|---|---|
| Institutions carrying the nine `AER` automotive courses in SCNS | **~40** |
| Of those, FCS state colleges | **2** (Hillsborough, Indian River State) |
| Of those, district technical colleges | **~37** — Atlantic, Lake, Sheridan, Traviss, Lindsey Hopkins, Erwin, McFatter, Withlacoochee and thirty more |
| Institutions on the SITE before 2026-09-20 | **39, every one FCS or SUS** |
| IPEDS: institutions awarding in CIP 47.06 | **56**, overwhelmingly technical colleges |

⚠⚠ **So the filter that protects the site from private institutions also deletes the sponsor
emphasis.** The whole career-and-technical space — automotive, welding, HVAC, industrial
maintenance, aviation maintenance, practical nursing, paralegal certificates — lives at these
institutions, and ranks 11–27 of the career-path queue are exactly that space.

### ✅✅ ANSWERED BY RON, 2026-09-20 — **“Yes to 1 and 2”** — and both are done

**1. `is_public()` now includes district technical colleges.** `sector_of()` answers a third public
sector, **`TECH`**, kept separate from FCS because a technical college awards clock-hour certificates
rather than degrees and sits outside the A.A. transfer machinery. **44 codes**, derived with evidence
rather than by matching a name (`scratchpad/derive_tech.py`): the SCNS name must read as a district
technical college **and** IPEDS must list an institution of that name in its Florida public file. Two
were added by hand after review — **THTC**, which IPEDS spells *Tom P. Haney*, and **FLTC**, absent
from the 2023 completions file but a Hillsborough district college. **NPTI (New Professions Technical
Institute) was rejected: technical-sounding name, private school.**
⚠ Every tool here inherits the change, `list_courses.py` included, so future offering loads carry
technical colleges without further work.

**2. The back-catalogue sweep is done** (`scratchpad/tech_sweep.py`, scoped to courses that actually
GAIN a technical-college carrier, so the university catalogue could not be disturbed):

| | |
|---|---|
| Courses whose offering list was wrong by omission | **117** |
| Technical-college offerings restored | **1,296** |
| Technical colleges involved | **44** |
| Institutions on the site | **39 → 83** |
| Prefixes affected | EEV 18, CJK 15, ETI 15, TDR 13, AER 9, CTS 9, EER 8, ACR 5, HEV 4, HMV 4, AVS 3, ETC 3 |

⚠ **CJK is the one to notice**: fifteen law-enforcement academy courses had **no offerings at all**
and now carry 13–16 each. The same for EEV electronics. **Those pages told a reader the course was
taught nowhere.**

⚠ **Still open:** institution NAMES come from SCNS and are sometimes poor (`HC - HILLSBOROUGH
COLLEGE`, `HBTC - BREWSTER TECHNICAL COLLEGE`). The load did not overwrite names the site already
had. IPEDS would be a better source if it ever matters.

### The original write-up: what was done on 2026-09-20, and what needed Ron

✅ **Done, because the automotive path could not be honest without it:** 35 district technical
colleges were sent to the site with `sector: "TECH"` (`POST /api/v1/institutions/batch`), and the
twelve `AER` automotive courses with their clock hours and per-institution offerings. The path page
now reads *"38 Florida public institutions teach courses on this path"* instead of two.

⚠ **What needs a decision:**

1. **Should `scns.is_public()` include district technical colleges?** It is a one-line change with a
   wide blast radius — every offering list, every carrier count and every "public institutions
   only" judgement in the guide pipeline shifts. **Recommended: yes, with a separate `TECH` sector
   so the three can still be told apart.**
2. **Should the back catalogue be swept?** Guides and courses published under the old filter list
   FCS/SUS carriers only. ⚠ Not urgent for university-level courses, which technical colleges do
   not teach anyway — but for any PSAV or clock-hour course already on the site, the offering list
   is wrong by omission.
3. **Institution names come from SCNS and are sometimes poor** — `HC - HILLSBOROUGH COLLEGE`,
   `HBTC - BREWSTER TECHNICAL COLLEGE`. The 2026-09-20 load deliberately did **not** overwrite
   names the site already had. A better name source would be IPEDS.


## Resolved

*(Nothing yet — items move here with the date and what was decided.)*
