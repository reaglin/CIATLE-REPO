
---

## Batch 229 — MUE (music education), 2026-09-16

Four guides, all live: **MUE3423**, **MUE4344**, **MUE4411**, **MUE4475** — every `queued` row in the
prefix. **4 clean, 0 warnings, 0 blocking**; 0 of 4 prerequisites over the limit after one trim round.

⚠⚠ **264 MUE courses newly LISTED** (272 built, 264 created, 8 updated, 0 failed) — **the first prefix
in three batches that was not already on the site.**

**Prefix shape**: **273 live ids, 211 single-carrier (77%)**, max 10 carriers. ⚠ `hs_credit` 403/1,
transferable 403/1, dual enrolment 399/5 — `survey.py` calls all three "discriminating" on more than one
value; **the batch-221 threshold rule correctly rejects all three, and nothing about them went in the
guides.**

### ⚠⚠⚠ THE PREFIX IS A MATRIX WRITTEN IN ABBREVIATIONS — and it has a hole in it

`MUE` titles its methods numbers with **database abbreviations rather than course names**:

| Statewide title | Expanded |
|---|---|
| `MUS METH/COMP/K-12/ GEN MUSIC` | methods, comprehensive K-12, **general music** |
| `TECH-SKILL-MAT/COMP/K-12/INSTR-ORCH` | techniques/skills/materials, K-12, **orchestra** |
| `TECH-SKILL-MAT/COMP/K-12/INSTR-BAND` | the same, **band** |

⚠ **Unreadable to a student, and it is what the site shows as `stateTitle`.** Every guide expands it.

⚠⚠⚠ **Drawn out as a matrix — course type × level × specialism — the comprehensive-K-12 row has NO
UNDERGRADUATE INSTRUMENTAL METHODS SLOT.** `?344` is general music; `?421`/`?422`/`?423` are the
techniques-skills-materials numbers; and the instrumental *methods* slot, `?348`, is **graduate only**.
**A gap is invisible one row at a time and obvious once the matrix is drawn.**

### ⚠⚠⚠ HEADLINE — `MUE4344`, and a gap FRAGMENTS rather than displaces

**FGCU teaches *Teaching Instrumental Music* on the GENERAL MUSIC number.** Three independent pieces of
evidence, one more than the usual case has:

1. **Statewide title and description agree with each other** — both say general music. Branch 1 of the
   batch-208 test, so the carrier is the deviating party.
2. ⚠⚠ **FSU carries `MUE3344` *Teaching General Music K-12*, and its catalogue text is the statewide
   description WORD FOR WORD.** FSU both wrote the description and uses the number correctly.
3. ⚠⚠⚠ **UF carries `MUE4422` *TEACHING INSTRUMENTAL MUSIC* — the identical title at the identical 3
   credits — on the instrumental-band number.**

⚠⚠ **But the cause is the matrix gap, not carelessness — and this is the new finding: TWO carriers met
the SAME gap and improvised in DIFFERENT DIRECTIONS.** UF went onto `?422`, FGCU onto `?344`.

**Batch 227 had one carrier working around a gap. Two carriers diverging is worse in kind: the subject
becomes unsearchable, because no single number collects it and no two carriers agree.** Recorded as a
drill — *having found a gap, look for other carriers of the same subject under other numbers* — which in
`MUE` turned up `MUE4422`, `MUE4332` and `MUE4493` all carrying instrumental methods under different
statewide subjects. **Each guide lists the alternatives by number, which is the only thing that helps a
student who arrived by searching.**

### ⚠⚠⚠ `MUE4411` — a 2× credit divergence, EXPLAINED by the prerequisite chain

**FSU 4 credits, UWF 2** — the largest credit divergence recorded outside flight training, with nothing
in the identifier to signal it. **The gates say exactly why:**

| | FSU — 4 credits | UWF — 2 credits |
|---|---|---|
| Gate | `MUE 3491`–`3492`, a **two-course** choral conducting and literature sequence | `MUT 2117` (theory) |
| Alongside | concurrent `MUE 3495r` required | ⚠ **corequisite `MUG 3104` — FIRST conducting** |
| Therefore | **arrives able to conduct**; four credits go on harder problems | **learning to conduct at the same time** |

⚠⚠ **They are not unequal versions of one course — they sit at different points in the same sequence**,
and both designs are defensible.

⚠⚠⚠ **This is the prerequisite-as-signal diagnostic firing on SEQUENCE POSITION — a fourth thing it
settles, after subject (175), depth (185) and emphasis (187).** And it exposes an **asymmetric** transfer
harm a credit comparison alone would miss: **UWF → FSU arrives two credits short AND without the
`3491`–`3492` foundation**; the reverse direction simply arrives over-prepared.

**Recorded as a standing drill: whenever two carriers diverge on CREDITS, read both prerequisite chains
before writing it up. A credit difference is frequently a sequence-position difference in disguise.**

### ⚠⚠⚠ `MUE4475` — the same-institution control's THIRD outcome: it EXPLAINS

| Carrier | Course | Audience |
|---|---|---|
| **UWF** (2 cr) | *Percussion Methods and Materials*, with school observations | *"planning to practice teach in band programs"* — ✅ matches statewide |
| ⚠ **FAU** (3 cr) | *Advanced Percussion Literature and Pedagogy* | ⚠⚠ *"music majors in **percussion performance**"* |

⚠⚠⚠ **FAU ALSO carries `MUE2470` *Percussion Pedagogy and Methods* (1 cr), and THAT is the course whose
description reads "teaching percussion instruments on the elementary and secondary school level."** So
FAU placed the statewide subject elsewhere and uses `?475` deliberately for a performance-track course.

**The control neither convicts nor exonerates — it EXPLAINS what the second course is.** Third distinct
outcome after `INR3503` (convicts) and `JOU4306` (exonerates).

⚠ **The tell was a single phrase — FAU's description covers "promotion and marketing."** **A school band
director never needs that; a private studio teacher does.** **Recorded as a technique: read a description
for the one item only one audience would need.**

### ⚠⚠⚠ `MUE3423` — and a CONTRIBUTOR that drifted away from its own contribution

Statewide `?423`: *"a study of orchestra materials in a laboratory setting, appropriate to elementary and
secondary school music programs."* **UWF's *Instrumental Programs: Strings and Orchestra* (2 cr) matches
it.** **USF's *String Techniques* (1 cr) is a playing-technique course** — which Florida numbers separately
at `MUE2440`, carried by **six** public institutions at the same 1 credit.

⚠⚠⚠ **And the statewide description ends with the code `USF` — the University of South Florida
CONTRIBUTED the description its own course no longer matches.** UWF, not the contributor, is the carrier
still teaching the contributed text.

**So a contributor stamp does NOT mean the contributor still teaches what it contributed.** Where they
have parted company the statewide record has quietly stopped describing anybody, and that is invisible
from the record alone.

⚠ **UWF carries BOTH `MUE3423` and `MUE4343` *String Methods and Materials*** — the same-institution
control again, showing programme methods and string teaching are distinct courses.

⚠⚠ **String pedagogy runs across FIVE statewide numbers** for what is really two courses: `MUE1440`/`2440`
(playing technique), `MUE3343`/`4343` (methods and materials), `MUE3423` (this), `MUE3443` (intro to
teaching strings), `MUE4441` (FAU's string pedagogy and methods). **The guide tabulates all five.**

### ⚠ Every statewide description in this batch ends with a contributor code

`?423` → `USF`; `?411` → `FSU`; `?344` → `FSU`. **The batch-208 embedded-institution rule in its shortest
form — no list, no date, just the contributor.** ⚠ **Free evidence, one look at the last token: it names
the institution whose catalogue to check first.**

### Content handling

⚠ **All four guides lead on Florida's single `Music Education K-12` certificate**, because it is the
reason a student takes methods courses in specialisms they will never practise: **the certificate does not
distinguish general, choral and instrumental music, but school postings do, and a certified teacher can be
assigned to any of them.** The FTCE Music K-12 examination covers the whole span — and ⚠ **UF requires a
passing FTCE Music Content score as a PREREQUISITE to part of its methods sequence**, so the exam is not
always something taken at the end.

**Florida-specific context used throughout:** FMEA and its constituent associations (FBA, FVA, FOA), the
District and State **Music Performance Assessment** calendar and graded music lists, ⚠ **marching band
starting in July**, and the standing **shortage of string teachers** relative to band directors.

**The AI sections carry two professional cautions that arrive in a teacher's first month:** ⚠
**copyright** (school photocopying of octavos and parts is routine and unlawful; generated arrangements do
not escape the underlying rights) and ⚠⚠ **recordings of minors are student records under FERPA and
district policy — rehearsal audio and video of school students must not go to external services.** That
applies from the first observation visit.

### Sources used

| Source | What it gave |
|---|---|
| **SCNS flat file** | carriers, the credit divergences, and the whole methods matrix |
| **`sw_MUE.csv`** | the abbreviated titles, all four descriptions, ⚠ the contributor codes |
| **UWF** `uwf_mue.pdf` | three of the four courses, plus `MUE4343` and the woodwind/brass/percussion matched set |
| **FSU** registrar bulletin | ⚠ `MUE4411`'s 4 credits and its two-course gate; `MUE3344` — **the control that convicts** |
| **UF** CourseLeaf | ⚠⚠ `MUE4422` *Teaching Instrumental Music* — **the identical title on another number** |
| ✅ **FAU** Coursedog (reopened batch 228) | ⚠⚠⚠ **the decisive `MUE4475` evidence** — "percussion performance", "promotion and marketing", and `MUE2470` beside it |
| ❌ **FGCU** | ⚠ CourseLeaf PDF returned an **empty 202 on two attempts**, so `MUE4344`'s own description could not be read; the guide says so |
| ❌ **USF** | still no course-description route |

⚠ **Note the payoff timing: FAU was reopened one batch ago and supplied this batch's single most
decisive piece of evidence.** Re-probing a stale negative paid immediately.
