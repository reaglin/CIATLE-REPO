
---

## Batch 231 — PHI (philosophy), 2026-09-17

Four guides, all live: **PHI3200**, **PHI3452**, **PHI3790**, **PHI3880** — every `queued` row in the
prefix. **4 clean, 0 warnings, 0 blocking.** PHI already fully listed (281 courses, 0 created).

**Prefix shape**: 295 live ids, 205 single-carrier (69%), max **37** carriers.

### ✅ An unusually CLEAN prefix — and the batch-199 rule says to say so

**All four: both carriers at 3 credits, titles matching in substance, no subject collision, no credit
divergence, no misfiling.** After several batches of severe divergence this is worth stating plainly
rather than hunting for a problem that is not there.

⚠ `hs_credit`, `transferable` **and** `dual_enrollment` are all **607/607 uniform** — total boilerplate,
correctly dropped, with one line per guide saying it says nothing about these courses.

### ⚠⚠⚠ HEADLINE — the Gordon Rule designation rate varies by a factor of THIRTEEN

**Every one of the four courses has exactly ONE of its two carriers designating it:**

| Course | Designates | Does NOT |
|---|---|---|
| `PHI3200` | **FGCU** | UWF |
| `PHI3452` | **UWF** | FSU |
| `PHI3790` | **UWF** | UCF |
| `PHI3880` | **UWF** | UNF |

**Four for four** — the cleanest demonstration the project has of the batch-201 rule that designation is
institutional. ⚠⚠⚠ **And one `Counter` over the prefix explains why**, which is the new part. Public
undergraduate `PHI`, 464 rows, 132 designated (28% overall):

| Institution | Rate | Institution | Rate |
|---|---|---|---|
| **IRSC** | **11/12 — 92%** | FAU | 8/44 — 18% |
| GCSC | 6/8 — 75% | UNF | 4/39 — 10% |
| **UWF** | 14/24 — 58% | UCF | 6/68 — 9% |
| USF | 10/20 — 50% | FIU | 3/40 — 7.5% |
| FGCU | 5/17 — 29% | **FSU** | **2/29 — 7%** |

⚠⚠ **So this is institutional policy showing through, not four coincidences** — and it is the
**batch-230 pattern rule applied to DESIGNATIONS**: count the institution's whole prefix before writing
a designation difference up per-course, or one policy gets reported as N separate divergences.

⚠ **But the rate predicts the TENDENCY and not the course, and `PHI3200` is the counter-case.** UWF
designates 58% of its philosophy courses and FGCU 29% — **yet on that number it is FGCU that designates
and UWF that does not.** **Never infer an individual course's designation from the institution's habit.**

✅ **A validation worth recording: the flat-file flags matched the catalogue 4 for 4.** UWF's PDF carries
*"Meets College-Level Communication Skills Requirement"* on exactly the three courses the flat file flags
and not on the fourth. **The batch-179 label rule and the flag data corroborate each other
independently.** ⚠ Separately, **SFC shows `gordon_rule`=0 with `gordon_writing`=4** — the batch-206
independent-and-inconsistent flag finding, confirmed again.

### ⚠⚠ `PHI3790` — a scope divergence that maps onto a real disciplinary argument

| | UCF | UWF |
|---|---|---|
| Scope | ⚠ **post-colonial, sub-Saharan** | the whole tradition |
| Organised by | period and region | ⚠ **philosophical subfield** — logic, epistemology, metaphysics, ethics, religion, political thought |

⚠ **UCF's description is the statewide text verbatim**, so UCF is almost certainly its contributor —
**one carrier's reading recorded as the state's, not two sources against one** (batch-227 rule).

⚠⚠⚠ **And the gap is not carelessness: it is the ethnophilosophy debate.** Whether African philosophy
means the professional post-colonial discipline or the entire intellectual tradition is a live argument
in the field — Tempels, Hountondji's critique, Odera Oruka's trends. **Both courses are defensible
positions in it, and a good section in either puts the argument on the syllabus.**

**Handled with a two-column syllabus test and an explanation rather than a warning.** ⚠ **Where a
divergence tracks a genuine disciplinary controversy, explaining the controversy serves the student far
better than flagging the inconsistency** — the divergence becomes intelligible instead of arbitrary.

### ⚠ Two further scope notes, both modest and both real

- **`PHI3200`** — the statewide description says "social and political communities" with no tradition
  named; **UWF says WESTERN twice** and names the canon (Hobbes, Locke, Rousseau, Smith, Marx). That is
  the normal US shape of the course, **said plainly, with a pointer to `PHI3790` for students wanting
  non-Western material.**
- **`PHI3452`** — UWF's description is the statewide text verbatim (UWF the likely contributor); **FSU's
  is independently worded and agrees on subject.** ⚠ The one difference: UWF and the state name *"the
  moral/social implications of evolutionary theory"*; **FSU lists only theoretical problems and names
  "the tools of analytic philosophy."** The implications half — sociobiology, the naturalistic fallacy,
  eugenics — **is what most students assume the course is about, and may be absent.**
  ⚠ Also the batch-189 shape: **no prerequisite anywhere, but the course assumes evolutionary theory the
  gate does not require.** The guide names what to read first.

### ⚠ Deliberate cross-prefix linking

**`PHI3880` Philosophy of Film is cross-referenced to the `FIL` guides written in batch 230** —
`FIL3833`, `FIL4036`, `FIL4364` — because this course supplies the conceptual vocabulary (realism,
formalism) those use without justifying, and students arrive at the number from both directions. ⚠
**Writing two adjacent prefixes in consecutive batches makes this linking cheap; it is worth doing
deliberately.**

### ⚠⚠⚠ SOURCE LOSS: FGCU has stopped returning course content

`catalog.fgcu.edu/courses/<pfx>/<pfx>.pdf` returns an **empty 202** on **`phi`, `mue`, `bsc`, `egn`,
`eng` — 6 requests across 2 days and 5 prefixes.**

⚠⚠ **The register called FGCU "the single most productive cross-check source in the project"**, and it
is frequently the *second* carrier on a two-carrier course — exactly where a guide most needs
independent corroboration. Two guides in two batches now name the gap (`MUE4344`, where FGCU is the only
carrier, and `PHI3200`).

⚠ **Recorded as blocked-as-of-today with an instruction to re-probe, NOT as permanent.** The batch-183
rule warns that state-college blocks are rate-triggered, and Broward and Valencia have both gone
blocked → recovered → blocked before. **Raised as `REVIEW_QUEUE` item 104**, which asks Ron two things:
whether FGCU has another public route, and whether it is worth approaching FGCU (and UNF) directly.

### Sources used

| Source | What it gave |
|---|---|
| **SCNS flat file** | carriers, credits, ⚠ **the Gordon Rule designation rates that are the batch's headline** |
| **`sw_PHI.csv`** | all four descriptions — recent, argued register, usable directly |
| **UWF** `uwf_phi.pdf` | all four courses, and the Gordon Rule labels that validated the flag data |
| **FSU** registrar bulletin | `PHI3452`'s independently worded description — the genuine second source |
| **UCF** Kuali | `PHI3790` — ⚠ statewide text verbatim, identifying UCF as contributor |
| ❌ **FGCU** | ⚠⚠ **newly blocked — see above** |
| ❌ **UNF** | bepress 403 on archived PDFs, as recorded |
