
---

## Batch 232 — PHC (public health), 2026-09-17

Three guides, all live: **PHC4109**, **PHC4140**, **PHC4464** — every `queued` row in the prefix.
**3 clean, 0 warnings, 0 blocking.** PHC already fully listed (590 courses, 0 created).

**Prefix shape**: 599 live ids, 452 single-carrier (75%), ⚠ **max 6 carriers** — note the low maximum:
**no `PHC` course is widely carried in Florida**, which is itself worth knowing when setting the hedging
level.

### ⚠⚠⚠ HEADLINE — `PHC4140` is a branch-4 collision, and this time the MECHANISM is visible

| | |
|---|---|
| statewide **TITLE** | *Public Health Planning and Analysis* |
| statewide **DESCRIPTION** | ⚠⚠ entirely **GIS** — *"an introduction to Geographic Information Systems (GIS)… buffering, layering, and spatial queries"* |
| **UWF** | *Public Health Planning and Analysis* — planning, implementation, evaluation, needs assessment. **Zero GIS.** Backs the **title**. |
| **USF** | *Introduction to Public Health Geographic Information Systems*. Backs the **description**. |

**The carriers split one on each side** — branch 4 of the title/description test, the `HFT4252` shape:
**the test returns no answer and the number carries two subjects.**

⚠⚠ **What is new is that the mechanism is legible.** On `HFT4252` the contradiction was unexplained.
**Here the statewide description names its own author** — it calls the course *"a required course in the
**PROPOSED** public health major in the **Bachelor of Science in Health Sciences [BSHS]** degree
program."* That is one institution's degree, described while it was still being proposed.

⚠⚠⚠ **So the likeliest history is that a carrier contributed a description of ITS OWN course onto a
number whose title already belonged to a different subject, and nobody reconciled the two.** The record
is internally contradictory **because it was assembled from two sources**, not because either half went
stale.

**Recorded as a drill:** when title and description disagree, **read the description for signs of a
single author** — a named degree programme, a delivery mode (*"this online course"*), a word like
*"proposed"*, an institution code. **Where you find one you have identified which carrier the
description belongs to, and the title preserves the other carrier's reading.**

⚠ **And the displaced subject had nowhere to go.** Florida provides **three** upper-division planning
numbers (`PHC?140`, `?142`, `?143`) and its only GIS-in-public-health number, **`PHC?194`, is
GRADUATE** — so an undergraduate GIS course has no correct home. **Misfiling by necessity underneath a
branch-4 collision**, and the guide says plainly that there is no right number to look for.

### ⚠⚠ `PHC4109` — a title divergence that dissolves, proved by a shared phrase

Statewide *Scientific Basis of Public Health* against UWF *Diseases in Human Populations* reads like a
divergence. It is not:

| Statewide | UWF |
|---|---|
| "overview of **scientific principles** of public health and their application to public health problems with significant **state, national and international** impact" | "overview of the **biological basis** of public health and the implications of major communicable and non-communicable diseases of public health significance at the **state, national, and international** levels" |

⚠ **The scope phrase is word for word identical.** UWF's title is simply the more informative one.
**Handled as reassurance**, per the batch-227 shape.

⚠⚠ **And the obvious wrong reading was checked rather than assumed.** *Diseases in Human Populations*
reads like epidemiology — **it is not.** This course asks *what* the diseases are; epidemiology asks
*how you find out*. **Florida numbers epidemiology at least four ways at undergraduate level**
(`PHC?030`, `?024`, `?040`, `?048`), and the guide points students needing it at those.

**Two further notes on this one:**

- ⚠ **The state calls the college-science background a RECOMMENDATION and UWF calls it a REQUIREMENT** —
  same sentence, different force. No formal course prerequisite is recorded either way, so registration
  may not stop a student the course is built to exclude.
- ⚠⚠ **The statewide description says it is "offered concurrently with `PHC 5XX3`"** — the batch-186
  dual-listing rule, with **two defects in one sentence**: `PHC 5XX3` is a **placeholder** (the
  batch-222/226 shape, ⚠ **appearing in the DESCRIPTION rather than the prerequisite field — a new
  location for it**), and **UWF's current entry does not mention the arrangement at all.** The guide
  states both consequences of dual-listing and hedges on whether it still applies.

### ⚠ `PHC4464` — clean, but one carrier's title is unsearchable

| Source | Title |
|---|---|
| Statewide | *Introduction to Health Disparities and Social Determinants* |
| UWF | *Understanding **Health Equity** and Health Disparities* |
| ⚠ USF | *Breaking Barriers: Drivers to Public Health Solutions* |

**No subject divergence found.** But ⚠ **USF's title names neither disparities nor determinants**, so a
student searching a catalogue will not find it and a transfer evaluator will not recognise it. **Stated
as a practical problem with an otherwise fine course.**

⚠⚠ **UWF's "health equity" is a terminology-era signal (batch 187), and a benign one:** *disparity*
names a measured difference, *equity* names the goal, and the field has moved toward equity language
over the last decade. **The guide says learn both**, because both appear in the literature and in job
adverts.

### ⚠⚠ SOURCE: USF identified as acalog and CONTENT-BLOCKED — the NINTH institution

The register said *"root 200 but no course-description path exposed… not yet a route"*, which invited
re-probing. **Probed properly:** `catalog.usf.edu` root answers **200 (75 KB) with acalog markers**;
`content.php` returns an **empty 202**; the Coursedog bootstrap says the host *"does not exists"*.

⚠ **So USF joins the acalog content-blocked pattern** — FSW, TSC, CF, Polk State, Santa Fe, FAMU, St.
Johns River State, Florida Polytechnic and now USF. **That converts an unidentified lead into a settled
negative**, which per the batch-215 platform rule saves future sessions from probing hopefully. ⚠⚠ **USF
was a carrier on two of this batch's three courses**, so it cost real evidence here.

⚠ **FGCU re-probed at session start (`bsc`): still an empty 202.** `REVIEW_QUEUE` item 104 stays open.

### ⚠ The distribution test, and why nothing was claimed

`hs_credit` is **825/825 blank** — pure boilerplate. `transferable` reads **824 EL / 1 NY** and
`dual_enrollment` **788 Y / 36 N**; `survey.py` flags both "discriminating" on more than one value, but
at **0.1% and 4%** these are near-universal by the batch-221 threshold rule, **and none of the three
targets is among the exceptions.** Nothing claimed in the guides.

### Content notes

All three guides lead students to ⚠ **FLHealthCHARTS**, the Florida Department of Health's county-level
data portal — free, public, and the right source for any Florida-focused assignment in this field.
Florida context used throughout: **a county health department in all 67 counties** (collectively the
largest employer of public health graduates in the state), an ageing population's chronic disease
burden, vector-borne disease in a subtropical climate, hurricane-related health effects, rural access
gaps, and migrant and seasonal farmworker health.

⚠⚠ **`PHC4464`'s AI section treats algorithmic inequity as COURSE CONTENT rather than as a cheating
warning** — a model trained on historical health data learns the patterns produced by unequal access and
under-treatment, so a system predicting "need" from "past spending" rates an under-served group as
needing less. **That is the course's own mechanism, running inside a tool**, and it is documented rather
than hypothetical.

### Sources used

| Source | What it gave |
|---|---|
| **SCNS flat file** | carriers, credits, full institution titles (⚠ the survey truncates at 40 chars — the full USF titles were the finding) |
| **`sw_PHC.csv`** | all three descriptions, ⚠ **the GIS/planning contradiction and the BSHS tell**, the placeholder `PHC 5XX3`, and the family scan that found `PHC?194` is graduate |
| **UWF** `uwf_phc.pdf` | all three courses — the decisive evidence on every one |
| ❌ **USF** | ⚠⚠ **newly identified as acalog and content-blocked** |
| ❌ **FGCU** | still blocked, re-probed at session start |
