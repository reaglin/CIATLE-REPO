
---

## Batch 234 — GEO (geography), 2026-09-17

Three guides, all live: **GEO4251**, **GEO4280C**, **GEO4357** — every `queued` row in the prefix.
**3 clean, 0 warnings, 0 blocking.** GEO already fully listed (285 courses, 0 created).

**Prefix shape**: 287 live ids, 229 single-carrier (80%), max 7 carriers. ⚠ `hs_credit`, `transferable`
and `dual_enrollment` all **385/385 uniform** — pure boilerplate, nothing claimed.

### ⚠⚠⚠ HEADLINE — a correction to my own batch-222 rule, and a better handling

`GEO4251`'s statewide description says *"offered concurrently with **`GEO 5XX3`**"* — **the identical
shape as `PHC4109`'s `PHC 5XX3` from batch 232**, two batches and a different prefix apart. That
prompted a scan of **all 41 statewide CSVs on disk: 220 wildcard tokens.**

⚠⚠ **Read in context, two different things are wearing the same shape:**

| What you see | What it is |
|---|---|
| ✅ *"**ANY** 1XXX OR 2XXX COURSE WITH PREFIX CCJ, CJC, CJE, CJL, CJJ, PLA"* | **genuine LEVEL NOTATION** — the word *ANY*, or a prefix list, is the tell |
| ⚠⚠ *"HFT 3XXX **GOLF PLANNING & OPERATIONS II**"* · *"BCN 3XXX **INTRODUCTION TO THE CONCRETE INDUSTRY**"* · *"GEO 5XX3 **(ADVANCED CLIMATOLOGY AND CLIMATE CHANGE)**"* | ⚠⚠⚠ **a PLACEHOLDER — and the masked number is followed by the course's ACTUAL TITLE** |

⚠⚠⚠ **In every placeholder case the writer knew which course they meant and named it. So the title
recovers the number.** Tested on four, **three recovered**:

| Masked | Recovered |
|---|---|
| `GEO 5XX3` (Advanced Climatology and Climate Change) | ✅ **`GEO?256`, GRADUATE** |
| `PHC 5XX3` (Scientific Basis of Public Health) | ✅ **`PHC?123`, GRADUATE** |
| `BCN 3XXX` (Introduction to the Concrete Industry) | ✅ **`BCN?443`** |
| `HFT 3XXX` (Golf Planning & Operations II) | ✗ not found |

⚠⚠ **And UWF's catalogue confirmed it independently and more easily:** its `GEO4251` entry reads
*"Offered concurrently with **GEO 5256** Advanced Climatology and Climate Change"* — **the exact number
the title search predicted.** **The state record masks what the carrier prints in full**, so the first
move is to read the carrier's own entry.

**Batch 222 recorded the handling as *"state the intent, say the number does not exist."* That is now
corrected in `CLAUDE.md`** — and ⚠ **the masked numbers cluster inside "offered concurrently with"
dual-listing notes**, where identifying the graduate partner is exactly what makes the repeat-restriction
warning usable.

⚠ **Consequence for a live guide:** `PHC4109` (batch 232) tells the reader there is nothing to look up.
**Raised as `REVIEW_QUEUE` item 105** with the exact one-line fix, since republishing needs a go-ahead.

### ⚠⚠⚠ `GEO4280C` — three carriers taking three different halves of one subject

The statewide description is a six-item list spanning **hydrology** (items 1, 5, 6 — water/soil-rock
interrelationships, precipitation-infiltration-runoff-evaporation, analytical techniques) and **water
resources** (items 2, 3, 4 — distribution, quality, groundwater development). **The carriers split it:**

| Institution | Number | Title | What it covers |
|---|---|---|---|
| **FAU** | `GEO4280C` | *Water Resources* | ⚠ **the MANAGEMENT half** — use, allocation, wetland degradation, pollution |
| **UWF** | `GEO4280` | *Basic Hydrology* | ⚠ **the SCIENCE half** — water budget, stream flow, evapotranspiration |
| **FSU** | `GEO4280` | *Geography of Water Resources* | ✅ **both halves** |

⚠ **None is misfiled — the statewide description licenses all three.** But a student gets a genuinely
different course depending on where they take it, **and neither half is a subset of the other.**

⚠⚠ **And the subject is filed three ways at two levels:** `GEO4280C` (FAU), `GEO4280` (FSU, UWF —
the batch-219 institutional signature), and **`GEO3280` at UF (⚠ **4 credits**) and USF (3)**. **Five
institutions, three numbers, two levels, one suffix and a credit divergence, for one subject.**

⚠ **The `C` suffix is not a lab signal here:** UWF's *unsuffixed* `GEO4280` states a *"material and
supply fee will be assessed for corresponding lab"*, and the statewide record marks the number
`IN_Lab=Y` regardless of suffix. **The suffix is pure filing.**

### ⚠⚠ `GEO4357` — two intellectual traditions on one number

| | FSU | UWF |
|---|---|---|
| Title | *Environmental Conflict and Economic Development* | *Environment and Economy* |
| Description | ⚠ **the statewide sentence verbatim** — "controversies over the use, transformation, and destruction of nature, including **political ecology**" | reconciling environment and economy; "environmental action that is economically feasible"; ⚠ **how environmental projects are funded in the US and how to gain funding** |
| Frame | **the fights** | ⚠ **reconciliation, plus grant-writing** |

⚠⚠⚠ **UWF's description never uses the words conflict, controversy, destruction or political ecology.**
Political ecology is a named field in critical human geography about power, access and who bears the
cost; UWF's course is environmental economics with a funding component. **Different traditions, and
different destinations** — advocacy and graduate human geography against consulting and the grant-funded
non-profit sector. **Two-column syllabus test given.**

⚠ **The departmental signal corroborates it:** UWF places the course in **Earth and Environmental
Sciences**, not Geography or Economics.

### ⚠ Three smaller record findings

- ⚠⚠ **The flat file's institution title and the institution's own catalogue disagree.** For `GEO4251`,
  the flat file records FSU's title as *"Climate Chaos: The Science Behind the Stories"*; **FSU's
  catalogue publishes *Geography of Climate Change and Storms*.** A cousin of the batch-222/226
  inventory-title problem, but **inside a public carrier's own record.** The guide gives both so a
  searching student finds the course either way.
- ⚠ **A typo in the statewide title:** `ADVANCED CLLIMATOLOGY AND CLIMATE CHANGE`, with a doubled L.
  Harmless except that it defeats a catalogue search; the guide says to search on "climat".
- ⚠ **`GEO4251`'s statewide prerequisite field is empty; UWF requires `GEO 4250` Climatology** — which
  is what "advanced" in the title means. **It is the second climatology course, not an entry point.**

⚠ **Both `GEO4251` and `GEO4357` are dual-listed at UWF** (`GEO 5256`, `GEO 5358`), so both guides carry
the repeat-restriction warning.

### Sources used

| Source | What it gave |
|---|---|
| **SCNS flat file** | carriers, credits, ⚠ the three-number two-level spread on `GEO4280`, the FSU title discrepancy |
| **all 41 `sw_*.csv`** | ⚠⚠⚠ **the 220-token wildcard scan that corrected the batch-222 rule**, and the title lookups that recovered three masked numbers |
| **UWF** `uwf_geo.pdf` | `GEO4251`, `GEO4357` and the bare `GEO4280` — ⚠ **and `GEO 5256` in full, confirming the recovery method** |
| **FAU** Coursedog | `GEO4280C` — the management-half reading |
| **FSU** registrar bulletin | all three FSU entries, including the catalogue title that differs from the flat file |
| ❌ **FGCU** | re-probed at session start: still an empty 202. `REVIEW_QUEUE` 104 open |
