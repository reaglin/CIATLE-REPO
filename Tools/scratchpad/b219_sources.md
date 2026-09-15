
---

## Batch 219 — TPA (design and craft), 2026-09-15

Seven guides, all live: **TPA3022**, **TPA3064C**, **TPA3601C**, **TPA4021C**, **TPA4045C**,
**TPA4061**, **TPA4077C**. `TPA3230C` remains **HELD** (`REVIEW_QUEUE.md` item 25).
All seven are 3 credits. Contact hours settled by Ron **by suffix**: `C` = 60, no suffix = 45.

**Prefix shape** (flat file): **420 live ids, 327 single-carrier (78%), max 10 carriers.**
`hs_credit` **discriminates** — 559 elective / 48 performing-fine-arts across the prefix — but all
seven of these are elective. `IN_Dual_Enrollment1` is `Y` on all 607 offering rows: boilerplate.

### Sources used

| Source | What it gave |
|---|---|
| **SCNS flat file** + `survey.py` | carriers, per-institution titles and credits, flags, single-carrier baseline |
| **`sw_TPA.csv`** (statewide report) | full statewide descriptions, prerequisites, transferability, hs_credit |
| **UWF** `uwf_tpa.pdf` via `uwf_pdf.py` | full entries for `TPA3022`, `TPA3064`, `TPA4021C`, `TPA4045`, `TPA4046`, `TPA4061`, `TPA4077C`, `TPA3601`, `TPA3230`, `TPA3223` |
| **UCF Kuali** (`ucf_tpa3601.json`) | `TPA3601C` — description, 2 weekly lab hours, prerequisite, Spring-only, Gordon Rule flags |
| **FIU Coursedog cache** | `TPA4061`, `TPA3060`, `TPA3230` descriptions |
| ❌ **FAU** | no public catalogue at its catalogue host — blocks `TPA3064C` entirely and half of `TPA3022` |
| ❌ **USF** | acalog, content-blocked — blocks `TPA4045C` entirely |

### ⚠⚠⚠ THE BATCH'S HEADLINE: in `TPA` the `C` SUFFIX IS AN INSTITUTIONAL SIGNATURE, not a description

**Five of the seven queued `C` ids have a BARE TWIN carried by DIFFERENT institutions.** Not one
institution carries both forms.

| `C` identifier | Carried by | Bare twin | Carried by |
|---|---|---|---|
| `TPA3064C` Scenic Design 1 | **FAU** | `TPA3064` | **UWF** |
| `TPA3601C` Stage Management | **UCF** | `TPA3601` | **USF, UWF** |
| `TPA4021C` Lighting Design II | **UWF** | `TPA4021` | **FSU, UF** |
| `TPA4045C` Costume Design | **USF** | `TPA4045` | **UWF, FSU** |
| `TPA4077C` Scene Painting | **UWF** | `TPA4077` | **FSU (3 cr), USF (2 cr)** |

⚠⚠ **This is a FOURTH shape for the batch-183 "three shapes behind a `C` suffix" table**, and it is
distinct from all three:

- **not split family** — there is no `L` partner anywhere in the prefix for these
- **not suffix divergence** — the subject is the same on both sides; only the packaging differs
- **not "a `C` nobody carries"** — ⚠ **every one of these `C` ids IS carried.** All seven queued
  `C` ids in this batch are real.

⚠ **What it actually is: two institutions filing the same course differently, and the state
recording both.** **The practical consequence is mild for content and real for evaluation** — a
transfer evaluator matching on the identifier sees a mismatch where there is none. **Say in the
guide that the twin exists and who carries it.**

⚠⚠ **Diagnostic, and it is one flat-file pass: before writing any `C` id, look up the bare number.**
Batch 184 established that an institution carrying BOTH forms means a course run in two shapes.
**This batch establishes the opposite signature — DIFFERENT institutions carrying the two forms
means one course filed two ways.**

### ⚠⚠⚠ PARALLEL NUMBERING FAMILIES — number fragmentation applied to a SEQUENCE

**Batch 207 measured number fragmentation on a single level of Spanish. `TPA` shows the same shape
running through an entire two-course SEQUENCE, so the fragmentation compounds.**

| | Family A | Family B |
|---|---|---|
| **Lighting Design I** | **`TPA3022`** — FAU, UWF | **`TPA4020`** — FSU, UF |
| **Lighting Design II** | **`TPA4021C`** — UWF | **`TPA4021`** — FSU, UF |
| **Scene Design I** | **`TPA3064`** (UWF) / **`TPA3064C`** (FAU) | **`TPA3060`** — FIU, UF |
| **Scene Design II** | **`TPA4061`** — FIU, UWF | (none — FIU crosses families) |

⚠⚠ **Note the two anomalies the table exposes.** The second lighting course is **one number with two
suffixes across two families** — so the suffix, not the number, is what separates them. And
**`TPA4061` is carried by FIU, whose first course is `TPA3060` from the OTHER family** — so the
families are not clean institutional blocs either.

⚠ **The institutions know.** **UWF writes its own prerequisites to span the fragmentation:**
`TPA4021C` requires *"TPA 3020 OR TPA 3022"* and `TPA4061` requires *"TPA 3060 OR TPA 3064."*
**An institution hedging its own prerequisite across two statewide families is the strongest
available evidence that the families are the same course** — stronger than any title comparison.

### ⚠⚠⚠ A DANGLING statewide prerequisite — the reference is valid, the target is absent

**`TPA4021C`'s statewide prerequisite reads `TPA 4020 LIGHTING DESIGN I`. ⚠⚠ UWF, the ONLY carrier
of `TPA4021C`, does not offer `TPA4020`.** So **the state describes a prerequisite chain that does
not exist at the institution teaching the course.**

⚠⚠⚠ **And it is worse in the other direction: UWF's own alternative, `TPA 3020`, is carried by NO
Florida public institution at all.** So of the three numbers naming the gate, **one is carried by
the wrong institutions and one is carried by nobody.** The real gate is `TPA3022`.

⚠ **This is a NEW sub-shape of the batch-209 prerequisite-field check.** That check tests a token
against `^[A-Z]{3}\s?\d{4}[A-Z]?$` and catches **syntactic** corruption (`ADV U101C`). **This token
is perfectly well formed and names a real, active course — it is simply the wrong one for the
institution.**

**Standing check, and it is cheap once the flat file is loaded: for every course-looking token in
`DS_Prerequisites1`, ask whether the CARRIER of the course being written actually offers it.**
A syntactically valid prerequisite naming a number the carrier does not have is a **dangling
reference**, and it should be named in the guide with the real gate beside it.

### ⚠⚠ A statewide DESCRIPTION can be COPIED between numbers — check the siblings

**`TPA4045` (Styles in Costume Design) and `TPA3230` (Theatre Costuming I) share EIGHT of their TEN
statewide competency items verbatim.** Only item 8 differs (`TPA3230`: *"tracing of historical
costume designs"*; `TPA4045`: *"understanding of colour as it relates to the costume"*).

⚠⚠ **The consequence is substantive, not cosmetic: the DESIGN number's competency list contains
CONSTRUCTION competencies** — *"costume cutting skills"* and *"high level skills in development of
patterns"* — **because they were carried over from the construction course.** ⚠ **So Florida's own
record blurs the designer/draper division at the level of the written competencies**, which is the
same design/craft conflation already recorded on `TPA3223C` (batch 208) and `TPA3230C`
(`REVIEW_QUEUE.md` item 25), now found a third way.

⚠ **Drill: when a statewide description is a NUMBERED COMPETENCY LIST, diff it against the sibling
numbers in the family before treating any item as evidence about that specific course.** Four
numbers in this prefix carry lists in the identical 1980s register — `TPA3601`, `TPA4020`,
`TPA4045`, `TPA3060`, `TPA3230` — and they are visibly a single drafting exercise.

### ⚠⚠ `IN_Lab` = `Y` on an identifier with NO suffix (`TPA4061`)

**Confirms and extends the batch-200 finding that `IN_Lab` is unreliable.** There it disagreed with
the title's own `(L)` marker; **here it flags laboratory instruction on a number that carries no
suffix at all, and both carriers describe bench work** (FIU: *"rendering techniques and model
making"*; statewide: *"lectures and in-class design work"*).

⚠ **Handling under Ron's by-suffix rule: publish 45 and say in the guide that it is a FLOOR**, with
the three independent reasons. **Do not quietly inflate a figure the rule settles** — say why the
rule understates it.

### ⚠⚠ A Gordon Rule designation on an upper-division PRODUCTION course (`TPA3601C`, UCF)

**UCF records both `gordon_rule` and `gordon_writing` on Stage Management: Techniques.** Coherent —
stage management is a documentation discipline and rehearsal and performance reports are frequent,
deadline-bound writing — but **unexpected in this prefix, and it carries the C-or-higher condition.**

⚠ Written with the batch-206 caution intact: **the flags reliably say a designation is recorded and
are NOT a safe guide to which component it satisfies.** The guide says so and sends the reader to
UCF's own list.

⚠ **UCF's Kuali record also supplied the batch's only published scheduling data**: **2 weekly
lab/studio hours** on a 3-credit `C` course, and **Spring-only**. **A once-a-year course costs a
year, not a term** — put it in the prerequisite field.

### Credit divergence found

| Number | Carriers | Credits |
|---|---|---|
| **`TPA4077`** (bare) | **USF 2**, FSU 3 | ⚠ **a transfer student is a credit short against a 3-credit requirement** |
| `TPA4061` at FIU | — | ⚠ FIU's system carries a **stale duplicate record at 3.33 credits** beside the active 3-credit one; the 3-credit row is the one with a college and a description (batch-167 rule) |

### Blocked sources, re-confirmed

- **FAU** — no public catalogue at its catalogue host. **`TPA3064C` was written entirely from the
  statewide record**, which for that number is unusually detailed (it names the four deliverables),
  cross-read against UWF's and FIU's descriptions of the same course under their own numbers.
- **USF** — acalog, content-blocked. **`TPA4045C` likewise written from the statewide record plus
  UWF and FSU under the bare twin.** ⚠ Both guides say so explicitly.

### Where the `C` suffix is EARNED — and how to tell

⚠ **Three of the seven have independent corroboration that the integrated reading is right**, which
is worth recording because this project has met so many spurious `C` ids:

| Number | Corroboration |
|---|---|
| `TPA3064C` | ⚠ **the statewide description opens *"classroom and LABORATORY study"* and requires SCALE MODELS** |
| `TPA3601C` | ⚠ **UCF publishes 2 weekly lab/studio hours** |
| `TPA4021C`, `TPA4077C` | UWF's descriptions are built on *"light lab projects"* and *"practice in various techniques"* respectively |

**So the derived 60 is not a bare convention on these — say which evidence supports it.**
