
---

## Batch 224 — JOU (journalism), 2026-09-16

Four guides, all live: **JOU3314**, **JOU3342**, **JOU4306**, **JOU4313C** — every `queued` row in the
prefix. **4 clean, 0 warnings, 0 blocking**; 0 of 4 prerequisites over the limit. JOU was already
listed (231 courses, unchanged).

**Prefix shape**: **241 live ids, 193 single-carrier (80%)**, max 9 carriers.

### ⚠⚠⚠ `JOU4306` — two unrelated subjects, and the FIRST collision the usual tests cannot adjudicate

| Institution | Title | What it is |
|---|---|---|
| **UWF** | Writing Critical Reviews | *"reviews of books, film, art, and music"* — **a writing course** |
| **UF** | Advanced Data Journalism | *"program in **R**&hellip; reproducible data analysis"* — **a programming course** |

**No shared content, skills, textbook or career path.** ⚠ **That is the `EEE4775` standard.**
**Published as one guide covering both readings, labelled, with a prerequisite-based test; split
recommendation in `REVIEW_QUEUE.md` item 101.**

⚠⚠⚠ **What makes it genuinely new is that every standing test fails to settle it.**

**1. The title/description test returns a fifth outcome.** The statewide title (*Critical Journalism*)
and the statewide description (*"critical thinking and analysis as employed in the profession of
journalism"*) **agree with each other — and still admit both readings.** Writing a review is critical
thinking; analysing a dataset is analysis.

> ⚠⚠ **So the test's four recorded branches need a fifth: TITLE AND DESCRIPTION AGREE, AND THE
> AGREED-ON WORDING IS TOO VAGUE TO DISCRIMINATE.** **An internally consistent statewide record is not
> automatically a usable one.**

**2. The dedicated-number tell fails because the dedicated numbers are DORMANT.**

| Number | Statewide title | Public carriers |
|---|---|---|
| `JOU3305` | Data Journalism | **UF only** |
| `JOU4305` | Data Journalism | ⚠⚠ **none** |
| `JOU4015` | Journalism Culture and Criticism | ⚠⚠ **none** |

⚠ **Numbers exist for BOTH readings and neither is carried**, so neither institution had a live
alternative to move to. **The batch-203 tell — "a dedicated statewide number exists for what they are
teaching" — is much weaker when that number is dormant, and this is the case that shows it.**

**3. ⚠⚠⚠ The same-institution control (batch 223) works in BOTH directions — this is the refinement.**

| Case | What the control showed |
|---|---|
| **`INR3503`** (batch 223) | **FAMU carries both `INR3502` and `INR3503` and files them correctly** → ✅ **CONVICTS** — proves the subjects are distinct and the state's assignment workable |
| ⚠⚠ **`JOU4306`** (batch 224) | **UF carries `JOU3305` Data Journalism and files the INTRO course correctly** → ⚠ **EXONERATES** — UF is not careless; Florida provides no *advanced* data number, so UF took an available one for a real two-course sequence |

> ⚠⚠ **The control is not a misfiling detector. It is a test of whether the carrier is working the
> state's scheme.** **A carrier that files everything else correctly and deviates on one number is
> telling you the scheme has a gap, not that the carrier is sloppy.** **Run it before writing a
> misfiling warning.**

⚠ **Recorded conclusion: neither carrier is at fault here, and the guide says so.** **The student's
problem is real regardless of fault, which is why the transfer advice leads.**

### ⚠⚠⚠ `JOU3342` — the worst dangling prerequisite found so far

**Statewide prerequisite: `JOU 3101` AND `RTV 4301`.**

| Carrier | `JOU3101`? | `RTV4301`? |
|---|---|---|
| **UWF** | ✅ | ⚠ **no** |
| **UNF** | ⚠ **no** | ⚠ **no** |

⚠⚠ **One carrier can satisfy half; the other can satisfy none.** **`RTV4301` is carried by FAU and UF;
`JOU3101` by USF, FAU, UWF and UF.** ⚠⚠⚠ **So the two institutions that COULD satisfy the prerequisite
— FAU and UF — do not carry `JOU3342` at all.**

**The prerequisite was contributed by a department that does not teach the course.** ⚠ **That is the
batch-222 mechanism (institution-contributed, resolves only where the contributor is) in its most
extreme form, and it is worth adding to the five-shapes table as the worst case rather than as a new
shape.**

### ⚠⚠ Institutional signature, third prefix

**`JOU4313C` is carried by UF; the bare `JOU4313` by UWF. No institution carries both.** Same title,
same credits, both describing sports reporting. ⚠ **Batch-219 shape, now seen in `TPA`, `COM` and
`JOU`** — **it is a general property of the catalogue, not a `TPA` quirk.**

### ⚠ Number fragmentation on environmental journalism

| Number | Public carriers |
|---|---|
| **`JOU3314`** | FIU, UWF |
| `JOU4314` | FAU, UF |

**Four institutions, two numbers, one subject, split cleanly at the 3000/4000 boundary.**

### ⚠⚠ A statewide description carrying one institution's REGIONAL scope

**`JOU3314`'s statewide description specifies *"emphasis on the Everglades and the rest of South
Florida's ecosystem."*** ⚠ **That is FIU's scope in a statewide field** — the same shape as batch 200's
local-TITLE finding, but applied to **scope** rather than to a title.

⚠ **The guide says so and generalises the three competencies the description names** — writing about
nature, working agency and activist sources, obtaining government data — **which transfer to any
Florida ecosystem.** **A Panhandle student gets Apalachicola and the springs, not the Everglades.**

### ⚠ A guide that failed the structure check, and why

**`JOU4306` initially validated with two warnings — no `Learning Outcomes` section, no `Major
Topics` section.** ⚠ **Correctly.** The two-subject layout had put each reading's outcomes and topics
under per-reading `<h2>` headings, so the canonical sections did not exist.

✅ **Fixed by restructuring rather than by renaming**: each reading's prose moved into Course
Description as an `<h3>`, then both outcome lists grouped under one `<h2>Learning Outcomes</h2>` and
both topic lists under one `<h2>Major Topics</h2>`, with Reading A / Reading B labels retained on every
list. **Re-validated clean.**

⚠⚠ **Worth recording as a standing note: a two-subject guide still owes the canonical section
structure.** **Label the readings inside the sections, not instead of them.** The validator caught it,
which is what it is for.

### Sources used

| Source | What it gave |
|---|---|
| **SCNS flat file** + `survey.py` | carriers — including the dormant `JOU4305`/`JOU4015` and the `JOU3305` control |
| **`sw_JOU.csv`** | descriptions, and the `JOU3342` prerequisite |
| **UWF** `uwf_jou.pdf` | `JOU3314`, `JOU4306`, `JOU4313` — full entries |
| ✅ **UF CourseLeaf** `catalog.ufl.edu/UGRD/courses/journalism/` | `JOU4306`, `JOU4313C`, `JOU4318` — descriptions **and** prerequisite chains |
| **FIU Coursedog cache** | `JOU3314` |
| ❌ **UNF** | unreachable, as recorded — blocks `JOU3342`'s second carrier |
| ⚠ **UWF for `JOU3342`** | **carried per the flat file but absent from BOTH the prefix PDF and the search route** — second instance after `COM4764` |

⚠⚠ **`JOU3342` is therefore the first guide in a long while written with NEITHER carrier's own
description available.** **The guide states that plainly and flags the emphasis table as an inference
to check rather than a finding.**

### ⚠ UF CourseLeaf: the department slug

`catalog.ufl.edu/UGRD/courses/**journalism**/` returns 200 with the full department listing.
`journalism_and_communications` 404s. ⚠ **The register already says UF slugs are descriptive; this one
is the short form despite the college being the College of Journalism and Communications.**
