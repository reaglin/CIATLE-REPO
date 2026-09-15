
---

## Batch 220 — CCJ (criminal justice), 2026-09-15

Four guides, all live: **CCJ3193**, **CCJ3450**, **CCJ3691**, **CCJ4141** — the four `queued` rows in
`queue.csv`. All four are 3 credits, no suffix, **45 contact hours**, and **none has a prerequisite**.

⚠⚠ **456 CCJ courses newly LISTED** (473 built, 456 created, 17 updated) — the site held **13**
CCJ courses before this batch. **The largest listing gain in several batches**, and it came free with
the flat-file parse.

**Prefix shape**: **486 live ids, 311 single-carrier (64%)**, max **31** carriers. ⚠ **64% ties `AFR`
for the LOWEST single-carrier share of the fifteen prefixes now measured** (the norm is ~75%), so `CCJ`
is comparatively well shared — its introductory numbers reach 31 institutions.

### ⚠⚠⚠ THE METHOD FINDING: stratify the distribution test by COURSE LEVEL before believing it

**This nearly went into four guides as a headline finding and it is wrong.**

`DS_Transferable1` across all **356 ACTIVE** `CCJ` rows:

| | count |
|---|---|
| `NOT AUTOMATICALLY TRANSFERABLE` | **186** |
| `GUARANTEED TRANSFER…` | **170** |

⚠⚠ **A near 50/50 split, which by the batch-207 `Counter` test reads as strongly discriminating** — and
in a prefix where the batch-202/204 rule says to read the field on every course, that looked like the
batch's story.

**Cross-tabulated against `DS_Course_Intent1` it collapses completely:**

| Intent | GUARANTEED | NOT-AUTO |
|---|---|---|
| LOWER | 50 | 0 |
| UPPER | **119** | 2 |
| UPPER/LOWER | 1 | 0 |
| ⚠ GRADUATE | 0 | **130** |
| ⚠ VARIABLE | 0 | **54** |

⚠⚠⚠ **Of 171 active UNDERGRADUATE rows, 169 are guaranteed.** The split is entirely an artefact of
graduate and variable-credit rows, which are non-transferable as a class. **For the courses this project
actually writes, the field is boilerplate.**

**The rule, and it applies to every field the batch-207 test is run on:**

> ⚠⚠ **Run the distribution over the rows you are WRITING ABOUT — active, undergraduate, non-shell —
> not over every active row.** One `groupby` on `DS_Course_Intent1` is the whole cost, and it is the
> difference between a finding and an artefact.

⚠ **The two genuine undergraduate exceptions are worth keeping**: **`CCJ4615`** *Criminal Behavior
Systems (U)* and **`CCJ4662`** *Minority Community* are the only active undergraduate `CCJ` numbers
classified NOT AUTOMATICALLY TRANSFERABLE. Neither is in this batch; both are worth the batch-204
treatment if they come up.

⚠ `hs_credit` (**356/356 ELECTIVE**) and `IN_Dual_Enrollment1` (**356/356 `Y`**) are plain boilerplate
in `CCJ` and were stated once per guide as such.

### ⚠⚠⚠ SECTOR NUMBER DIVERGENCE — a SECOND instance in the same prefix, so it is a pattern

**`CCJ3450` / `CCJ2452`, and the sector line is perfectly clean:**

| Number | Level | Carriers | Sector |
|---|---|---|---|
| **`CCJ3450`** | UPPER | UCF, UWF | ⚠ **both SUS** |
| **`CCJ2452`** | LOWER | Polk State, Valencia, Florida Gateway, State College of Florida, Tallahassee State | ⚠ **all five FCS** |

**Same statewide title (*Criminal Justice Administration*), near-identical statewide descriptions, seven
institutions, two numbers, zero crossover.**

⚠⚠ **`CLAUDE.md` already records `CCJ1020` (FCS) vs `CCJ2002` (SUS) for the introductory course from
batch 182. Two instances in one prefix makes it a `CCJ` property rather than a coincidence** — and the
guides now say so and tell the reader to check the number on anything in this prefix.

⚠⚠⚠ **Why this one bites harder than the intro-course case.** `CCJ1020`/`CCJ2002` are both
lower-division, so an A.A. completer's general-education and elective protections absorb much of the
damage. **Here the two numbers sit at DIFFERENT LEVELS**, and **a 2000-level course cannot supply
upper-division hours toward a Florida baccalaureate.** So a Valencia student who takes `CCJ2452` and
transfers to UCF may have to take the subject again — **not because the content differs but because the
level does.** **Get a written answer from the receiving department before taking it.**

⚠ **Generalised drill: where a prefix is found to split ONE course by sector, check its other
high-enrolment numbers for the same shape before writing any of them.** It cost one `survey.py` call here
and produced the batch's strongest student-facing finding.

#### ⚠ But the sector does NOT determine the LEVEL — `CCJ3691` is the counter-case

**`CCJ3691` is a 3000-level number carried by UWF (SUS) and St. Johns River State College (FCS).**
⚠ **Florida College System institutions offer upper-division coursework where they hold baccalaureate
authority**, and several do. **So "FCS ⇒ lower division" is a tendency the sector rule exploits, not a
fact to rely on** — check the carriers rather than inferring from the sector.

### ⚠⚠ The flat file lags a CURRENT catalogue title — UCF renamed the course

| Source | `CCJ3450` at UCF |
|---|---|
| SCNS flat file | *The Criminal Justice Manager* |
| ⚠ **UCF Kuali catalogue (current)** | ***Criminal Justice Management and LIABILITY Issues*** |

⚠ **The rename is substantive, not cosmetic.** UCF's description adds *"fundamental liability concepts
regarding criminal justice practices"* and narrows to **first-line** management. §1983, qualified
immunity and failure-to-train material follow from it; UWF's version instead spans **police, courts and
corrections**. **The guide gives a two-column test.**

⚠ **Also from Kuali: `CCJ3450` at UCF is FALL ONLY** — a once-a-year course on a degree plan costs a
year rather than a term, which goes in the prerequisite field.

### ⚠ UCF Kuali corroborates the by-suffix contact-hour rule again

**`CCJ3450` and `CCJ3024` both publish `labStudioFieldWorkHours: "0"`** — plain 3-credit courses with no
scheduled lab. **That is the second independent corroboration in two batches** (batch 219's `TPA3601C`
published **2** lab hours on a 3-credit `C` course). ⚠ **UCF remains the only Florida source publishing
lab hours as a structured field, and it is now the cheapest available check on whether a suffix is
real.**

### Sources used

| Source | What it gave |
|---|---|
| **SCNS flat file** + `survey.py` | carriers, titles, credits, flags, the 64% single-carrier baseline |
| **`sw_CCJ.csv`** (statewide report, downloaded this batch) | descriptions, prerequisites, transferability, course intent — ⚠ **and the cross-tab above, which the flat file could not have produced** |
| **UWF** `uwf_ccj.pdf` via `uwf_pdf.py` | full entries for all four targets plus `CCJ3024` |
| **UCF Kuali** | `CCJ3450` rename, Fall-only, 0 lab hours, department/college |
| **FIU Coursedog cache** | `CCJ3193` (a materially different emphasis from UWF's) |
| ❌ **FAU** | no public catalogue — blocks `CCJ4141`'s second carrier |
| ❌ **St. Johns River State (SJRSC)** | ⚠ **NEWLY PROBED — acalog, content-blocked** (below) |
| ❌ **Valencia, Broward** | empty 202s again — the batch-183 rate-triggered pattern, not a new block |

### ⚠⚠ St. Johns River State College — acalog, content-blocked (NEW register row)

**Probed 2026-09-15.** `catalog.sjrstate.edu` root answers **200 (49 KB)**; the page markup contains
**33 acalog references and 21 `content.php` links**; a `content.php` probe returns an **empty 202**.

⚠⚠⚠ **Seventh institution in the acalog pattern** — after FSW, TSC, CF, Polk State, Santa Fe and FAMU.
**The platform-level presumption from batch 215 held exactly**: identifying the platform answered the
question in two requests instead of a hopeful probing session. **Identify the platform first.**

### ⚠ Valencia and Broward: the rate-triggered block, confirmed again

Both returned **empty 202s on `ccj`** in this batch, having answered fully in earlier sessions. ⚠
**Recorded and moved on per the batch-183 rule — not re-probed in a loop, and not recorded as a new
block.** Both remain listed as working sources.

### Content-handling notes

Two of the four are **mental-health- and violence-adjacent** and were written under the `CLAUDE.md`
sanity-check rule that such guides must be supportive and resource-pointing:

- **`CCJ3193`** carries **988** and **211**, and explains Florida's **Baker Act** and **Marchman Act**
  rather than referring to them in passing. ⚠ Its most distinctive content is the statewide
  description's own last clause — ***"the mental health of criminal justice actors"*** — occupational
  mental health for the workforce the degree feeds, which is easy to read past and is one of the more
  useful things in the course.
- **`CCJ3691`** opens with a plain content note and carries **RAINN 1-800-656-HOPE**, **988** and the
  Florida Council Against Sexual Violence. ⚠ Its intellectual core is written as the **evidence-versus-
  policy gap**, with Florida as the case study — the Jimmy Ryce Act, lifetime registration, and the
  local residency ordinances that produced the Julia Tuttle Causeway encampment. **Both the harm to
  victims and the weakness of the evidence for residency restrictions are stated; neither is used to
  qualify the other.**

### ⚠ A graduate number whose title and description do not match

**`CCJ6142` is titled *COMMUNITY ORIENTED POLICING* statewide, and its statewide description is entirely
about restorative and community justice** — *"emerging policy, theory, and research in restorative and
community justice."* ⚠ Graduate, so out of scope for a guide, **but `CCJ4141`'s guide warns the reader
not to rely on that title if they meet it as a continuation.**

### Prefix completeness

⚠ **`CCJ` is NOT complete and is not being treated as a target.** 486 live ids; **17 now carry guides**
(13 before this batch plus the four written here). Under Ron's 2026-09-11 direction a guide-less listed
course is a finished outcome, and **all 473 workable CCJ courses are now LISTED**, which is what the
career-paths phase needs. **The four written here were the four `queued` rows.**
