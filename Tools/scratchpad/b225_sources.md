
---

## Batch 225 — PET (physical education / coaching), 2026-09-16

Four guides, all live: **PET3344C**, **PET3471**, **PET4434**, **PET4820** — every `queued` row in the
prefix. **4 clean, 0 warnings, 0 blocking**; 0 of 4 prerequisites over the limit. PET was already
listed (297 courses, unchanged).

**Prefix shape**: **344 live ids, 290 single-carrier (84%)** — ⚠ **the highest single-carrier share of
the eighteen prefixes now measured.** Max 11 carriers.

### ⚠⚠⚠ A COHERENT INSTITUTIONAL PAIR SITTING ON TWO MISMATCHED NUMBERS

**UWF's `PET4434` and `PET4820` carry word-for-word identical descriptions, differing only in the age
band:**

> *"designed to prepare physical education teachers and coaches to plan and implement developmentally
> appropriate sport and physical activities for **[children and young adolescents | adolescents]**."*

⚠ **That is a deliberate two-course developmental sequence and it is sound curriculum design.**
**Neither statewide number means anything like it:**

| Number | Statewide subject | What UWF teaches |
|---|---|---|
| `PET4434` | **Curriculum Integration Through Movement** — elementary PE, rhythmic dance, manipulative skills, teaching **academic** skills through movement | **Youth Sport Pedagogy** |
| `PET4820` | **Teaching Team Sports I** — history and teaching methods of **softball, flag football and soccer** | **Adolescent Sport Pedagogy** |

⚠⚠⚠ **And Florida provides no undergraduate number that would fit.** There is no statewide
undergraduate number for developmentally-appropriate sport pedagogy by age band; the nearest,
`PET6206` *Sociological and Psychological Aspects of Youth Sport*, is **graduate**. **UWF needed two
numbers for a real sequence and used two that were available.**

⚠⚠ **This is the `JOU4306`/UF shape again — MISFILING BY NECESSITY, because the scheme has a gap
rather than because the institution is careless.** **Third instance in three batches** (`JOU4306` UF,
and now both halves of this pair), **so the pattern is established and the handling is settled: say
there is no "correct" number to look for, and lead with the transfer advice rather than the
adjudication.**

### ⚠⚠ A PREFIX divergence that explains a dormant number

**`PET4820`'s statewide subject has no carrier — and it has not disappeared, it has moved prefix.**

| Number | Statewide title | Level | Public carriers |
|---|---|---|---|
| `PET4820` | Teaching Team Sports I | UPPER | USF, UWF — ⚠ **neither teaches it** |
| `PET4821` | Teaching Team Sports II | UPPER | ⚠⚠ **none** |
| ⚠⚠⚠ **`PEO2011`** | **Teaching Team Sports I** — *identical title* | **LOWER** | **FAMU, UCF, FAU** |

⚠ **Florida carries the same course title in two prefixes: the `PEO` version is alive with three
carriers, the `PET` version is dormant and its two carriers have put other courses on it.**

⚠⚠ **Two consequences the guide states.** A student who needs "teaching team sports" for a requirement
should be looking at `PEO2011`. **And the level differs — `PEO2011` is lower division and `PET4820`
upper — so they are not interchangeable for upper-division hour requirements even where content
matches.**

**This is the batch-179 PREFIX divergence category, and it is the first instance where identifying the
other prefix EXPLAINED a dormant number rather than merely warning about a mismatch.**

### ⚠⚠ The private-only shape, INVERTED

**Batch 222 found `COM4564C` carried only by a private institution, with a public bare twin.**
⚠ **`PET3344` is the mirror image:**

| Identifier | Carrier | Sector |
|---|---|---|
| **`PET3344C`** | **UWF** | ✅ **public** — the queued id, and the correct one |
| `PET3344` (bare) | one private institution | ⚠ private only |

⚠⚠ **So the batch-222 rule needs stating symmetrically: check which FORM the public carrier uses, in
either direction.** **The instinct that an unsuffixed number is the "default" is wrong as often as it
is right.** ✅ **No substitution was needed here — the queued `C` id is the public one.**

### ⚠⚠ Transferability is NOT boilerplate in `PET` — and the exceptions are coherent

**Stratified to the 122 active undergraduate rows (batch-220 rule): 13 classified NOT AUTOMATICALLY
TRANSFERABLE, about 11%.** ⚠ **Far above `CCJ` (2 of 171) or `INR` (5 of 124), and well past the
batch-221 threshold.**

⚠⚠⚠ **And it is not random. The thirteen cluster:**

| Group | Numbers |
|---|---|
| **Athletic training clinical** | `PET4672`, `PET4673`, `PET4624`, `PET4625`, `PET4627` |
| **Exercise testing and fitness assessment** | `PET4550`, `PET4551`, `PET3385` |
| **Coaching theory** | `PET4765` |
| other | `PET1081`, `PET3312`, `PET4408`, `PET4517` |

⚠ **That is the batch-215 licensed-profession logic showing up in the transferability field: hands-on
clinical and assessment coursework where a receiving programme must attest to competence itself, and
cannot do so on the strength of another institution's credit.** **A genuine, explicable pattern.**

**None of the four written here is among them, and the guides say so — but they tell the reader to
check the classification on any `PET` course before assuming the credit moves.**

### ✅ Alternate-level pair test: a clean NEGATIVE, correctly returned

**`PET2760` and `PET4765` share the identical statewide title — *Theory and Methods of Coaching
Sports* — at LOWER and UPPER level.** ⚠ **That is exactly the surface shape of the batch-212
alternate-level pair.**

**Applying the test:** `grep` for `MUST CHOOSE` across all active `PET` records returns **zero**.

✅ **So it is ordinary number fragmentation, not a formal alternate-level pair.** ⚠ **Worth recording
because the batch-212 rule was explicitly bounded one batch after it was found** (`BCN` has `(U)`
markers and no "must choose" sentence), **and this is a second clean negative — the test is doing its
job of preventing a false positive on a suspicious-looking pair.**

### ⚠ Coaching is the most fragmented subject area measured

**Over twenty active statewide numbers**, including a three-part `PET4181`/`4182`/`4183` series, two
numbers sharing a title at two levels, and separate numbers for philosophy, ethics, strategies,
leadership, technology and advanced issues.

⚠⚠ **The practical consequence for a student is stated in the `PET3344C` guide: a coaching course on a
transcript identifies almost nothing without a syllabus.** **Keep it.**

### ⚠ Dangling prerequisite, again

**`PET3344C`'s statewide prerequisite is `PEO 2011` — carried by FAMU, UCF and FAU, not by UWF, its
only public carrier.** **The batch-222 mechanism, now routine enough that the check runs on every
course.**

### Sources used

| Source | What it gave |
|---|---|
| **SCNS flat file** + `survey.py` | carriers, the private-only inversion, the `PEO2011` discovery |
| **`sw_PET.csv`** | descriptions, the coaching family, the transferability cluster, the "must choose" negative |
| **UWF** `uwf_pet.pdf` | full entries for all four — ⚠ **including the identical-descriptions finding that is the batch's headline** |
| ❌ **USF** | no public course-description path, as recorded — blocks `PET4820`'s second carrier |

### ⚠ A note on how the headline was found

**The paired-description finding came from reading the UWF PDF output directly rather than from any
scripted comparison.** ⚠ **Two entries several lines apart turned out to be identical but for four
words, and nothing in the flat file or the statewide CSV would have surfaced it** — the statewide
titles are completely different, so no title-comparison test would fire.

⚠⚠ **Worth recording as a method note: when one institution carries several courses in a prefix, read
its descriptions against EACH OTHER, not only against the statewide record.** **An institution's
internal coherence is itself evidence, and it is invisible to every test in this file that compares a
carrier to the state.**
