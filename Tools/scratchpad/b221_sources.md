
---

## Batch 221 — PLA (paralegal / legal studies), 2026-09-15

Six guides, all live: **PLA3464**, **PLA3613**, **PLA3806**, **PLA4191**, **PLA4554**, **PLA4764** —
every `queued` row in the prefix. All 3 credits, no suffix, **45 contact hours**. **6 clean, 0
warnings, 0 blocking**; 0 of 6 prerequisites over the limit.

**Prefix shape**: **286 live ids, 190 single-carrier (66%)**, max **21** carriers. PLA was already
listed on the site (262 courses, unchanged).

### ⚠⚠⚠ THE A.S.-TO-BS LADDER — a DIFFERENT shape from sector number divergence, and the difference decides the handling

**Batch 220 found a sector number divergence in `CCJ` and generalised the drill: where a prefix splits
one course by sector, check its other numbers.** ⚠⚠ **Run on `PLA` it fired on four of six queued
courses — and then the diagnosis came out different, which is the finding.**

**Measured, not assumed:**

| Subject | FCS numbers | SUS numbers |
|---|---|---|
| **Family law** | **`PLA2800`** — ⚠ **18 public carriers, ALL FCS** | **`PLA3806`** (FGCU, UWF); **`PLA4806`** (UCF, + SPC) |
| **Law office management** | **`PLA2763`** — **10 public carriers, ALL FCS** | **`PLA4764`** (UCF, UWF) |
| **Property / real estate** | `PLA2610` (FCS) | `PLA3613` (UWF); `PLA3615` (UCF) |
| **Bankruptcy** | `PLA2460` (FCS) | `PLA3464` (UWF); `PLA4464` (UCF) |
| Intro to law | `PLA1003` — **19 carriers, 18 FCS + FGCU** | — |
| Civil litigation | `PLA2203` — **8 carriers, ALL FCS** | — |

⚠⚠⚠ **The structural explanation, and it is not a defect:** **Florida's A.S. in Paralegal Studies is
overwhelmingly a FLORIDA COLLEGE SYSTEM credential using `PLA1xxx`/`PLA2xxx`; the BS in Legal Studies
is a STATE UNIVERSITY SYSTEM credential using `PLA3xxx`/`PLA4xxx`.** **The universities renumber the
same subjects at upper division because a baccalaureate requires upper-division hours.**

⚠⚠ **Compare with `CCJ2452`/`CCJ3450` (batch 220), which looks identical in the data and is NOT the
same thing:**

| | `CCJ` (batch 220) | `PLA` (batch 221) |
|---|---|---|
| Shape in the data | one course, two numbers, disjoint sectors | **the same, on four subjects at once** |
| What it is | ⚠ **a DEFECT** — the same course numbered twice | ⚠ **deliberate ARTICULATION DESIGN** |
| Evidence | **two** numbers in the whole prefix; near-identical statewide descriptions | **a whole-prefix pattern across four subjects**, with the upper descriptions visibly DEEPER (`PLA2460` *"an introduction into the purpose"* vs `PLA3464` chapters *"in detail"*; `PLA2800` a numbered topic list vs `PLA3806` adding **Florida statutes** and **practical drafting**) |
| Harm to the student | ⚠ **a lost credit** — a 2000-level course cannot supply upper-division hours, so they may retake it | ⚠ **REPEATED CONTENT and Florida EXCESS HOURS** — the retake is the design, not an accident |
| What the guide says | *get a written answer from the receiving department before taking the lower version* | *expect familiar ground at greater depth; ask about substitution* |

**The test that separates them, and it is cheap:**

> ⚠⚠ **Count how many SUBJECTS in the prefix show the split, and compare the two statewide
> DESCRIPTIONS for depth.** **One subject with matching descriptions is a numbering defect. Several
> subjects with visibly deeper upper descriptions is a degree-ladder design** — and the two need
> opposite warnings.

⚠ **Expect the ladder shape in every prefix carrying an A.S.-to-BS articulation**: paralegal studies,
nursing, respiratory care, radiography, dental hygiene, health information management, and the
Engineering Technology BAS prefixes. **It is the batch-206 "licensure ladder" observation showing up
in the NUMBERING rather than in the scope.**

#### ⚠ Two counter-cases, kept because they stop the rule being over-applied

1. ⚠⚠ **The sector does NOT determine the level.** **St. Petersburg College (FCS) carries `PLA4554`
   and `PLA4806` at 4000 level.** **Florida College System institutions offer upper-division work
   where they hold baccalaureate authority.** Second instance this session after St. Johns River
   State carrying `CCJ3691`. **Check the carriers; never infer the level from the sector.**
2. **`PLA4191` and `PLA4554` have NO lower-division twin** — legal reasoning and environmental law are
   bachelor's-level offerings in Florida. **So the ladder is a property of some subjects in the
   prefix, not of the prefix as a whole.**

### ⚠⚠⚠ DANGLING PREREQUISITES — twice more, and now the MECHANISM is known

**Batch 219 found the shape on `TPA4021C` (a well-formed prerequisite naming a course the only carrier
does not offer) and could not explain WHY. `PLA` supplies two more instances and the explanation.**

| Course | Statewide prerequisite | Resolves? |
|---|---|---|
| **`PLA4554`** | **`PLA 1003` AND `PLA 2203`** | ⚠⚠ **UCF carries NEITHER** — its real gate is **`ENC 1102`**. ✅ SPC carries both. |
| **`PLA3806`** | **`PLA 1003`** | ⚠ **FGCU carries it; UWF does NOT.** |

⚠⚠⚠ **The mechanism: statewide prerequisites are institution-contributed, and in a prefix that splits
by SECTOR the prerequisite gets written from the side that has the lower-division numbers.** `PLA1003`
and `PLA2203` are carried almost entirely by state colleges. **At a university with no lower-division
`PLA` numbers at all, the statewide prerequisite names courses that are not on the menu.**

⚠⚠ **So the batch-219 check is now a targeted one rather than a general caution:**

> **Whenever a prefix is found to split by sector, expect its statewide prerequisites to dangle on the
> other side of the split.** **Check the prerequisite against the CARRIER, not against the state
> record, and name the real gate in the guide.**

⚠ **Useful corollary: a dangling prerequisite is itself EVIDENCE of a sector split**, so the two
findings confirm each other. It is also a reason the real gate is often something like freshman
composition — **which tells you the course is open to students outside the major**, a genuinely useful
student-facing fact.

### ⚠⚠ The distribution test needs a THRESHOLD, not just "more than one value"

**`survey.py` reported `dual_enrollment` as *discriminating* in `PLA` because it saw two values
(573 `Y` / 25 `N` across offerings).** ⚠ **Stratified to active undergraduate rows it is
155 `Y` / 9 `N` — 94% to 6%.**

**That is not a discriminating field; it is a near-universal default with a handful of exceptions**,
and writing it up as a finding would have been the error the batch-207 rule exists to prevent.

⚠ **Refinement to the batch-207 / batch-220 test: a field is only worth writing about when the split
is substantial** — `SPN`'s `hs_credit` at 24/178 was; `CCJ`'s transferable at 169/171 was not; this is
not. **A lopsided split means "near-universal, with exceptions worth listing separately," and the
exceptions are what to capture.** The nine `N` rows here are recorded in the batch notes.

**Stratified results for `PLA`** (164 active undergraduate rows): transferable **162 GUAR / 2
NOT-AUTO**, `hs_credit` **164/164 ELECTIVE**, dual enrolment **155 Y / 9 N**. **All boilerplate; all
six courses carry the common value.**

### ⚠⚠ Departmental divergence, cleanly observed (batch-205 shape)

| | **UWF** | **UCF** |
|---|---|---|
| Department | ⚠ **Criminal Justice** | ⚠ **Legal Studies** (dedicated) |
| Upper-division `PLA` catalogue | small | ⚠⚠ **64 courses**, including **moot court, an undergraduate law journal, legal scholarship, trial advocacy, mediation practicum** |
| What it predicts | justice-system-oriented context | **a recognisable law-school pipeline** |

⚠ **This extends the batch-187 note**, which had recorded only `PLA4885` and `PLA4263` as sitting in
criminal justice at UWF. **It is the whole upper-division `PLA` set.** **The guides tell a law-school-
bound reader to weigh the surrounding course list as heavily as the single course.**

### ⚠⚠ A genuine emphasis divergence worth the two-column treatment: `PLA4191`

| **UWF** — *Legal Reasoning* | **UCF** — *Thinking Like a Lawyer* |
|---|---|
| ⚠ *"Special emphasis will be placed on questions students might face on the **LAW SCHOOL ADMISSION TEST**"* | ⚠ reasoning methods *"applicable to legal **and non-legal** problems"* |
| an LSAT-preparation course inside a paralegal prefix | a transferable-method course |

**Neither is a misfiling** — the statewide description (*"legal analysis and critical thinking"*)
supports both. ⚠ **But the choice materially changes what the student gets**, so the guide leads with
a two-column test and tells LSAT-bound readers to **check LSAC directly for the current test format**,
which has been revised.

### Sources used

| Source | What it gave |
|---|---|
| **SCNS flat file** + `survey.py` | carriers, sectors, titles, credits — ⚠ **the sector disjunction, which is the whole batch** |
| **`sw_PLA.csv`** (downloaded this batch) | descriptions, the dangling prerequisites, the depth comparison, the stratified distributions |
| **UWF** `uwf_pla.pdf` via `uwf_pdf.py` | full entries for 4 of 6, plus the departmental placement |
| **UCF Kuali** | descriptions, real prerequisites, Fall-only, 0 lab hours, and the 64-course Legal Studies catalogue that confirmed the ladder |
| ⚠ **UWF search route** | tried for `PLA4764`; returned no course block — see below |
| ❌ **FGCU** | ⚠ **service-wide empty 202s** — see below |
| ❌ **St. Petersburg College** | not probed; no route in the register |

### ⚠ FGCU returned empty 202s across every prefix — a service-wide condition, correctly diagnosed

`catalog.fgcu.edu/courses/pla/pla.pdf` returned **202, 0 bytes**. ⚠ **Rather than record FGCU as
blocked on one probe (the batch-183 caution), a control probe was run on `psy` and `ccj` — prefixes
FGCU certainly carries. Both also returned empty 202s.**

✅ **So this is a service-wide condition, not evidence that FGCU lacks `PLA`** — which is exactly what
the batch-164 probe rule is for, and it changed what the `PLA3806` guide says. **Recorded, not
retried. FGCU remains a working source in the register.**

### ⚠ `PLA4764` is missing from UWF's published course listing

**The flat file records UWF as a carrier at 3 credits under the statewide title, but the course appears
in neither the prefix PDF nor the catalogue search route.** ⚠ **Both UWF routes were tried.** The
guide says so and tells UWF students to confirm with the department. **Consistent with the batch-212
finding that UWF's course-information index does not cover everything UWF carries.**

### Florida-specific content the guides carry

⚠ **These are what make the batch worth more than six summaries**, and all are verifiable primary law:

- **`PLA3464`** — Florida **opted out of the federal exemption scheme** (§222.20), and the **homestead
  exemption is unlimited in value** and capped by acreage (Art. X, §4); **11 U.S.C. §110** regulates
  non-lawyer bankruptcy petition preparers specifically.
- **`PLA3613`** — ⚠⚠ **homestead is THREE doctrines** (creditor protection, tax exemption, and
  **restriction on devise and alienation**), and the third is where transactions fail; plus the
  **closing wire-fraud** warning, which is the practical hazard of the practice area.
- **`PLA3806`** — ⚠⚠⚠ **Florida's 2023 reforms** (permanent alimony eliminated; equal time-sharing
  presumption added), and ⚠ **the statewide description still says *"custody, visitation,"* which
  Florida law abandoned** — a clean terminology-era instance (batch 187) in a field where the
  legislature has acted (batch 206). **Specific caps and standards deliberately NOT stated; the guide
  sends the reader to the current statute.**
- **`PLA4554`** — the **five water management districts** (ch. 373), the **Environmental Resource
  Permit**, and a **constitutional conservation policy** (Art. II, §7). ⚠ **The wetlands permitting
  authority question is flagged as contested and changing, with the reader sent to DEP and the Corps
  rather than given an answer.**
- **`PLA4764`** — ⚠⚠ **trust accounting under Florida Bar Chapter 5 and IOTA**, named as a leading
  route to discipline and often a bookkeeping failure rather than dishonesty; **docket control** as a
  leading malpractice cause; **Rule 4-5.3** making the supervising lawyer answerable for the
  paralegal.
- **All six** — ⚠ **Florida has NO paralegal licence**; Florida Registered Paralegal (Bar Chapter 20)
  is a **voluntary registration**, and the binding constraint is the **UPL prohibition**, which Florida
  enforces actively through Bar Chapter 10.
