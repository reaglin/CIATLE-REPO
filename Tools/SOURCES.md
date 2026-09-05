# Research sources for curriculum guides

Where to look when researching a course, ranked by how much they can be trusted and how often
they have actually produced the answer. Read alongside `Generate_Guides_and_Push_Process.md`
(the process) and `CLAUDE.md` (the content standard).

**Ron adds sources here as he finds them.** Anything in the "Contributed" section came from
him and should be tried early.

---

## ⚠ STANDING TO-DO (Ron, 2026-09-02): course drift from original definitions

> *"As you have probably seen, there is a lot of drift in the courses from their original
> (and common) beginnings."*

Ron has asked that this be tracked as a **named theme**, not scattered per-course flags. It is
the most consistent finding across the whole project and already underpins rules 14, 15, 17,
19, 20 and 21. The forms it takes:

| Drift type | Example |
|---|---|
| **Title drift** | `MEA0334C` queue "Medical Office Procedures" vs DSC "Coding for Medical Assisting and Lab" |
| **Content drift** | `CGS2821C` — server-side programming at DSC, web *design* at FSCJ, multimedia elsewhere |
| **Scope drift** | `HIM2283C` is advanced **CPT** at DSC, not advanced coding generally |
| **Credit drift** | HIM coding courses: 3 credits in one family, 4 in another |
| **Parallel numbering families** | DAA, ASL, RTE, PMT, FSS, HIM, BCA all run two or more families for one progression |
| **Sequence-position drift** | `RTE2844L` is "V" at some institutions and "IV" at others |
| **Wrong-subject guides** (our own drift) | MAN3554, HIM2283C, MUM2603 — all corrected |

**Proposed next step, not yet started:** `scns_prefix_map.json` now holds the official SCNS
prefix definitions parsed from the 2023-2024 handbook. That makes a **systematic drift
analysis** possible — compare what SCNS says a prefix *is* against what institutions
actually teach under it, prefix by prefix. It would convert scattered flags into a documented
account of how far Florida course content has moved from its common origins, which is
precisely what Ron is describing. Propose it to him before starting; it is a substantial
piece of work.

---

## Tier 0 — Daytona State College catalog (canonical for this project)

**Standing decision (Ron, 2026-09-02):** *"We will stick with providing guides for the DSC version, noting
that the Valencia versions differ with notes on the differences."* DSC is the **canonical institution** for
this repository. Where other Florida institutions differ, that is **noted as a difference inside the guide**,
not treated as equal-weight competing data. DSC is also the standing content priority.

### The DSC catalog is directly fetchable — use it first, always

`daytona_courses.csv` carries a **`subject_page`** value for **all 1,266 DSC courses**, which means a catalog
URL can be constructed for every course on the priority list:

```
https://daytonastate.smartcatalogiq.com/en/2024-2025/college-catalog/course-descriptions/<subject_page>/<level>/<coursenum>/
```

- `<subject_page>` — taken verbatim from `daytona_courses.csv` (e.g. `him-health-information`,
  `ind-interior-design`, `mea-medical-assisting`, `deh-dental-hygiene`).
- `<level>` — the first digit of the course number followed by `000` (HIM2800 → `2000`;
  MEA0334C → `0000`).
- `<coursenum>` — the course id **lowercased**, C/L suffix included (`him2283c`).

> **⚠ The `<level>` segment is not universal — drop it if the URL 404s (found 2026-09-02).**
> `.../esi-industrial-systems-engineering/4000/esi4312/` returns **404**, while
> `.../esi-industrial-systems-engineering/esi4312/` returns the full course page. The prefix index
> listed the course either way, so **an individual-page 404 is not evidence the course is absent** —
> fetch the prefix index, which exposes the real href, before concluding anything. Small prefixes
> (one or two courses) appear to be the ones flattened.

Dropping the final path element returns the **whole prefix index**, which is the fastest way to see DSC's real
titles for a family. Verified working across multiple prefixes (HIM, IND). Individual pages give
**title, credit hours, prerequisites, description, term offered, and lab fee**; they usually do *not* give
contact-hour breakdowns, so contact hours still come from family consistency or a Tier-2 catalog.

**This removes the web-search dependency for the entire Daytona priority list.**

### ⚠ DSC's **archived catalog years** are fetchable — use them for discontinued courses (found 2026-09-02)

The biggest single retrieval win so far. Substituting an older catalog year into the same URL works:

```
https://daytonastate.smartcatalogiq.com/en/2019-2020/college-catalog/course-descriptions/<subject_page>/<level>/<coursenum>
```

**Why this matters:** a course absent from the current catalog is not necessarily absent from DSC — it may
have been **discontinued**, and the archived year still carries the full entry (title, credits, description,
term offered). Batch 70 resolved **HUS1421, HUS1423, and HUS2050** this way after all three were missing
from `daytona_courses.csv`, from the 2024-2025 catalog, and from Broward's and Valencia's listings.

**Use it whenever a queue ID looks like a DSC course but the current catalog 404s.** The queue was built
from a statewide inventory that includes courses colleges have since dropped, so this will recur. Say in the
guide that availability varies by institution and year when the only source is an archived catalog.

Known-good year slugs: `2019-2020`, `2024-2025`, **`2025-2026`**.

> **⚠ The catalog-year trick works FORWARD as well as backward (found 2026-09-02).** Batch 75 hit
> **RTE3253** and **RTE4474** 404ing at every 2024-2025 URL form — with level segment, without it, and on
> the prefix index — while `daytona_courses.csv` listed both. Both returned complete entries from
> **`2025-2026`**. They belong to DSC's **B.S. in Radiologic and Imaging Sciences**, an upper-division
> programme newer than the 2024-2025 catalog.
>
> **So the year slug is a two-way tool:** older years recover **discontinued** courses; the newer year
> recovers **newly-added** ones. When a course is in the CSV but 404s in the working catalog year, try
> `2025-2026` before concluding anything — this will recur for every recently-launched B.A.S./B.S.
> programme at DSC.

### `daytona_courses.csv` under-reports — treat a CSV miss as coverage, not as a defect

**Ron's framing (2026-09-02), and it is the right one:** *"Missing courses in the queue that might be
offered at a college but did not show up in the queue is not a crucial error. The plan is to work college
by college, picking up courses that exist in each of their catalogs. It is expected that the number of
courses added to the queue will decrease for each school as many of the courses will have been published.
If a course is missed at a college, there is a good chance it will be picked up as we refresh the queue
with courses from other colleges."*

So this is a **coverage** property of a single scrape, not an integrity problem, and the college-by-college
refresh closes it without special handling. Do not chase it.

The one genuinely useful operational consequence: **absence from the CSV is not proof the course does not
exist at DSC.** The CSV holds 1,266 courses across 195 prefixes and has gaps at the course level as well as
the prefix level (`MGF2106` is absent though DSC teaches it as "Survey in Mathematics"; `HUS` is missing as
a prefix entirely). Since the URL is constructible from **any** sibling row's `subject_page` slug, one
WebFetch settles it — and a **404 is the only trustworthy negative**.

```
https://daytonastate.smartcatalogiq.com/en/2024-2025/college-catalog/course-descriptions/<slug>/<level>/<coursenum>/
```

Checked on the four courses ruled out by CSV lookup in recent batches: `MGF2106` exists; `SLS1570`,
`FFP2604`, and `DAA1504C` returned genuine 404s. Worth the single fetch when the course looks like it
should be there; not worth auditing the CSV.

### Why this matters — it caught real errors immediately

Anchoring to DSC exposed that **queue titles are not DSC titles**, and the differences change course scope:

| Course | Queue title | Actual DSC title | Consequence |
|---|---|---|---|
| `HIM2283C` | Advanced Coding | **Advanced CPT Coding and Lab** | Guide had been written around ICD-10-PCS and inpatient MS-DRGs; DSC's course is **outpatient CPT, revenue cycle, and EHR**. Wrong scope. |
| `HIM2442` | Coder Biller Pharmacology | **Pharmacology and Lab** | Published at **3 credits; DSC is 1**, and the scope includes **laboratory tests**, not only drugs. |
| `HIM2800` | Professional Practice Experience I | **Coding Professional Practice Experience I** | Coding-specific practicum, **1 credit**, prereq HIM2253C — which resolved the 2-vs-3 ambiguity that had caused it to be deferred. |
| `MEA0334C` | Medical Office Procedures | **Coding for Medical Assisting and Lab** | Different subject entirely — a rule-17 case. |
| `DEH1602` | (none) | **Periodontology** | Confirms the inference drawn from Gulf Coast's DEH2602. |

**Operational rule going forward:** before writing any DSC course, **fetch its DSC page (or the prefix index)
first**. Use the DSC title, credits, and scope. Then add differences at other institutions as notes. Do not
price a DSC course from another institution's family — see the cross-family warning below.

### ⚠ Cross-family evidence is not evidence about a number

Recorded because it nearly produced an error. Valencia runs an **entirely different HIM numbering family**
(HIM1012, HIM1110, HIM2222C and HIM2729C at 4 credits, practicum as L-suffixed HIM1800L/2810L/2820L). Its
credit values say nothing about DSC's HIM2283C or HIM2800. When two institutions use **different numbers**,
they are describing different courses, and one cannot be used to price the other — which is exactly why
the DSC-canonical rule resolves so much ambiguity.

---

## ⚠ HTTP 403s are probably bot filtering — retry them, do not treat them as permanent

**Standing guidance (Ron, 2026-09-02):** *"It is possible the non-working fetches flagged on bot filters.
It is possible they will reset."*

Several sources in this file are recorded as 403 dead ends. **That framing is too strong.** A 403 to an
automated fetch is far more likely to be **rate limiting or bot detection** than a deliberate block of the
content, and those filters commonly reset — by time window, by IP, or by traffic pattern. The content is
public in every one of these cases.

**Sources currently 403-ing, in priority order for retry:**

| Source | What it unblocks | Why it matters |
|---|---|---|
| **fldoe.org** | The **Tier 1 curriculum frameworks** — OCP structures and clock hours for every PSAV programme | The single highest-value recovery. Would resolve the DIM transit, ACR/HVAC, AVS aviation, and AAE clusters |
| **catalog.fscj.edu** | Academy clock hours; a large course inventory | Was ✅ until 2026-09-02 |
| **hccfl.edu / hcfl.edu** | Hillsborough programme pages | Redirect chain then 403 |
| **catalog.nwfsc.edu** | Northwest Florida State programmes | Long-standing 403 |

> **First retry result (2026-09-02): FSCJ recovered within the same session; fldoe.org did not.** That is
> direct evidence for the bot-filter reading — the same client, minutes apart, blocked on one host and
> served on the other. Keep retrying.

**Practical rule going forward:**
1. **Retry a 403 source at the start of each session** before assuming a course is unresolvable — one fetch
   is cheap and the payoff is a whole cluster.
2. **Deferred courses are provisional, not closed.** Every deferral recorded in this file names its blocking
   source; when a source recovers, `queue_mgr.py` still holds those IDs at priority 99xx and they can be
   pulled back.
3. **Do not re-describe these as "dead" in guides or notes** — say the source was unreachable at the time.

---

## Tier 1 — Authoritative, use whenever the course is PSAV

### FLDOE Curriculum Frameworks
The single best source for any **PSAV / clock-hour** course. Each framework gives the program
number, CIP code, total clock hours, and a table of every Occupational Completion Point with
its SCNS course number, title, and hours — plus regulatory notes no catalog carries.

Search: `FLDOE curriculum framework "<program name>" occupational completion point`
Frameworks are published as `.rtf` or `.pdf`, often mirrored on district college sites
(`fctc.edu`, `miamilakes.edu`, `bay.k12.fl.us` have all served copies).

> **⚠ fldoe.org now returns HTTP 403 to WebFetch (observed 2026-09-02).** A direct fetch of
> `https://www.fldoe.org/core/fileparse.php/.../1920-Transportation.pdf` was refused. This matters
> because the frameworks are the Tier 1 source for every PSAV course. Two workarounds that still
> function: **web search returns the OCP structure and hour values in result snippets** (this is how
> the DIM08xx transit hours were obtained in batch 66), and frameworks are frequently **mirrored on
> district college and technical centre sites**, which are not blocked. Note that college program
> pages are themselves inconsistent — `hccfl.edu` redirects to `hcfl.edu`, which then returns 403.
> When neither works, **reconcile the OCP hours by summing them against the stated program total**
> and say the value is derived.

**When the PDF will not extract**, save it and parse locally — this has worked twice where
WebFetch returned nothing useful:

```python
from pypdf import PdfReader
r = PdfReader(path)
for i, pg in enumerate(r.pages):
    t = pg.extract_text() or ""
    if "OCP" in t or "Program Number" in t:
        print(f"--- page {i+1} ---"); print(t[:2000])
```

Frameworks confirmed useful so far:
- **H170694** Patient Care Technician — 600 hrs, 7 OCPs (gave MEA0580=100, PRN0094=60)
- **E300100** Early Childhood Education — 600 hrs, 4 OCPs of 150 (gave the whole HEV ladder)
- **I470605** Diesel Systems Technician — gave DIM0102=300, DIM0104=300
- **J400410** Advanced Welding Technology — gave PMT0076=150
- **Bus Transit Technician (DIM08xx)** — partially recovered from search snippets and college
  program pages after fldoe.org went 403. **Technician I = 620 hrs and its five courses sum to
  exactly 620** (DIM0810=200, DIM0811=120, DIM0812=60, DIM0813=120, DIM0814=120), which validates
  the sum-against-stated-total method. **Technician II = 620 hrs** with DIM0820=60, DIM0821=120,
  DIM0822=120 confirmed and **DIM0823 + DIM0824 = 320 combined, split unknown**. **Technician III
  (DIM0830–DIM0834) could not be recovered at all.** The seven unrecoverable courses were deferred
  rather than derived: the published family spread runs 60–200 hrs, so a split cannot be inferred.

> **⚠ The DIM prefix holds two unrelated programs.** The `DIM08xx` transit series above and the
> general diesel series (`DIM0101C`/`DIM0102C`/`DIM0104C`/`DIM0105C`, 150–300 hrs) share a prefix
> and share nothing else. Do not reason from one family's hour values to the other's — the same
> caution as the "cross-family evidence" rule in Tier 0.

### FDLE / CJSTC
Authoritative for criminal justice academy courses, but the FDLE site itself is hard to
extract from. **College program pages have been more productive than FDLE directly.**

**Broward's full CJK prefix page** (`catalog.broward.edu/course-descriptions/cjk/`) is the
single best CJK reference found — it lists *every* CJK course with credits and total contact
hours in one table, across law enforcement, corrections, correctional probation, and
crossover programs. Fetch it whenever a CJK number needs hours.

⚠ **Multiple curriculum versions are in circulation, in both disciplines.** Same titles,
different numbers, different hours. They are **not** equivalent, and title-matching produces
wrong equivalency decisions.

*Corrections:* a 420-hour sequence (CJK0300/0305/0330/0335…) and a revised 445-hour sequence
(CJK0301/0306/0326/0336…). CJK0330 (20 hrs) ≠ CJK0326 (25 hrs); CJK0335 (16) ≠ CJK0336 (20).

*Law enforcement:* the 770-hour program documented by Santa Fe uses CJK0002/0018/0019/0063/
0079/0093/0400–0403. Broward's catalog carries a parallel series covering the same subjects
at different hours:

| Parallel series | Hours | 770-hour series | Hours |
|---|---|---|---|
| CJK0001 Introduction to Law Enforcement | 10 | CJK0002 | 12 |
| CJK0012 Legal | 62 | CJK0018 | 64 |
| CJK0014 Interviewing and Report Writing | 56 | CJK0019 | 56 |
| CJK0064 Fundamentals of Patrol | 35 | CJK0063 | 40 |
| CJK0065 Calls for Service | 36 | *(no direct counterpart)* |  |
| CJK0013 Interactions in a Diverse Community | 40 | *(cf. CJK0021 Serving Your Community)* | 34 |
| CJK0078 Crime Scene to Courtroom | 35 | CJK0079 Crime Scene Follow Up | 34 |
| CJK0087 Traffic Stops | 30 | CJK0401 | 24 |
| CJK0088 Traffic Crash Inv. Terms and Legal | 32 | CJK0402 Traffic Crash Investigations | 30 |
| CJK0084 DUI Traffic Stops | 24 | CJK0403 | 24 |
| CJK0092 Critical Incidents | 44 | CJK0093 | 44 |

Always confirm which version a transcript or source describes, and compare **numbers and
hours**, never titles.

### Florida State Fire College / Bureau of Fire Standards and Training
`myfloridacfo.com/division/sfm/bfst/training/course-syllabi` — publishes syllabi for fire
courses as `BFST####`, which map to the college `FFP####` numbers. Gives hours, required
text, and certification linkage.

---

## Tier 2 — College catalogs, by how reliably they have answered

Florida has 28 state colleges. These are the ones that have actually produced clean data.

| Source | Why it is good | Best for |
|---|---|---|
| **Santa Fe College** (`sfcollege.edu`) | Publishes **full program course lists with contact hours**, which almost no one else does | Academy programs, program structure |
| **Broward College** (`catalog.broward.edu`) | Lists **credit hours AND total contact hours AND lecture/lab split**, plus prerequisites and corequisites, and fees | Anything where contact hours matter |
| **Gulf Coast State** (`gulfcoast.edu/catalog`) | Clean prefix-level tables showing whole course sequences with prereq/coreq | Course sequences and pairings |
| **Tallahassee State** (`catalog.tsc.fl.edu`) | Explicit about clock hours vs occupational credit on PSAV courses | PSAV credit reporting |
| **Florida SouthWestern** (`catalog.fsw.edu`) | Reliable prerequisites and clear descriptions | Prerequisites |
| **Seminole State** (`seminolestate.edu/catalog`) | Clean single-course pages, easy to fetch | Quick credit/prereq checks |
| **FSCJ** (`catalog.fscj.edu`) | Gives clock hours on academy courses | Academy course hours |
| **Valencia, Miami Dade, Daytona State** | Useful, and MDC publishes competency PDFs | Cross-checking |

**Santa Fe's full-program listings are the single most useful catalog find so far** — its
Law Enforcement Officer C.C. page gave all 20 academy courses with hours, summing exactly to
the stated 770. Broward's corrections program page did the same for the 445-hour sequence.

### How to verify a program table
Sum the course hours and compare to the stated program total. Both the 770-hour LE table and
the 445-hour corrections table summed exactly, which is strong evidence against transcription
error. Do this every time.

---

### Direct URL patterns — use these before spending a web search

Added 2026-09-01 after this session hit the **200-call web-search cap** mid-batch. **WebFetch is not subject
to that cap**, so a known URL pattern is worth more than a search. Verdicts below are what actually happened
in production batches, not what should work.

| Institution | Pattern (substitute the 3-letter prefix) | Fetchable? |
|---|---|---|
| **Broward** | `https://catalog.broward.edu/course-descriptions/<prefix>/` | ✅ best first stop; full prefix listing. 404 = prefix not taught there, itself a fast signal |
| **Valencia** | `https://catalog.valenciacollege.edu/coursedescriptions/coursesoffered/<prefix>/` | ✅ **the only pattern that reliably gives lecture/lab/clinical hour splits** |
| **Gulf Coast** | `https://www.gulfcoast.edu/catalog/current/courses/<prefix>/index.html` | ✅ lecture/lab splits |
| **Miami Dade** | `https://www.mdc.edu/<program-slug>/courses.aspx` | ✅ **program-of-study view** — number + title + credits *in context* |
| **FSCJ** | `https://catalog.fscj.edu/courses/<numeric-id>` **and** `https://www.fscj.edu/academics/programs/cc/<n>` | ✅ **recovered 2026-09-02 after a same-day 403** — confirming Ron's read that these are bot filters, not blocks. The `/courses/<id>` page gives **clock hours directly** (ACR0012 = "125 clock hours of lecture"); the **`/academics/programs/cc/<n>` programme page is the better find** — it lists a whole PSAV sequence with hours in one fetch. ids not guessable; capture them when a search surfaces one |
| **Eastern Florida State** | `https://catalog.easternflorida.edu/course-descriptions-information/<prefix>/` | ❌ JS-rendered, returns empty; the `.pdf` variant is empty too |
| **Northwest Florida State** | `catalog.nwfsc.edu/preview_program.php?...` | ❌ HTTP 403, blocks WebFetch |
| **Acalog / Modern Campus** (SCF, FSW, TCC, Pensacola, FAMU) | `.../preview_course_nopop.php?catoid=<n>&coid=<n>` | ⚠ precise but ids not guessable — capture the URL whenever a search surfaces one |
| **Palm Beach State** | `https://palmbeachstate.smartcatalogiq.com/en/current/Catalog/Courses/<PREFIX-NAME>/<level>/<COURSEID>` | ✅ **smartcatalogiq, like DSC but a different path shape** — note `/Catalog/Courses/`, the UPPERCASE prefix folder (`IND-INTERIOR-DESIGN`), the UPPERCASE course id, and `current` in place of a year. Confirmed 2026-09-02. Its own `palmbeachstate.edu/catalog/...aspx` URLs **302-redirect here**, so go straight to smartcatalogiq |
| **Seminole State** | `https://www.seminolestate.edu/catalog/courses/<courseid-lowercase>` | ✅ clean, guessable, one course per page (`.../courses/ind1233c`). Gives credits, description, term, and progression grade requirements; **does not publish contact-hour splits**. A miss 404s cleanly |
| **Polk State** | `https://catalog.polk.edu/preview_course_nopop.php?catoid=<n>&coid=<n>` | ✅ **publishes the lecture/lab hour split**, which DSC does not. Confirmed 2026-09-02: `catoid=41&coid=61417` gave ENC0055L as "1 hour Lab, 1 credit, corequisite ENC1101" — the value DSC's page could not supply. ids not guessable; capture them when a search surfaces one |
| **Florida Gulf Coast (FGCU)** | `https://catalog.fgcu.edu/courses/<prefix>/` and `.../<prefix>/<prefix>.pdf` | ❌ **WebFetch returns empty for both** (JS-rendered; the PDF does not extract either). **But the pages index well** — a web search scoped to `catalog.fgcu.edu` returns course title + credits in the result snippet. Treat FGCU as *search-readable, not fetch-readable*. Added 2026-09-02 |

> **Standing rule (Ron, 2026-09-02):** *"If we do run websearch and discover new resources that can be
> used (have fetchable URL patterns) they should be added to that list."* Add the pattern to this table
> the moment it is confirmed — and record **dead ends** here too, so they are not retried. Verify a new
> pattern with a second prefix before recording it as fetchable; FGCU is the cautionary case (a real,
> constructible, *correct* URL that WebFetch nonetheless cannot read).

Which source answers which question: **credits only** → Broward. **Credits *and* contact-hour split** →
Valencia, then Gulf Coast — these are the sources that catch the credit/contact-hour errors, the most common
defect class in this repo. **Is this credit value plausible?** → Miami Dade program pages; this is the
mechanism behind rule 21, because a program listing shows number, title, and credits *together* where a
course-description search does not.

### WebSearch as the fallback when WebFetch comes up short (Ron, 2026-09-02)

> *"If the session counter for WebSearch has remaining available calls, and if Fetch fails to retrieve
> sufficient results, use WebSearch and log any finding that can assist in the work."*

WebFetch remains **first choice** — it is uncapped and returns the full page. But when no fetchable
catalog carries a value, **search rather than derive**, and log what comes back. Two batch-56 cases show
why this is worth the call:

| Course | What fetching gave | What search gave | Consequence |
|---|---|---|---|
| `SLS1570` | absent from DSC and Broward; FGCU pages unreadable | **FGCU publishes it at 2 credits** | the SLS family would have supported a *3*-credit derivation. Search prevented a wrong value. |
| `RTE1111L` | DSC gave 1 credit, no hours; not at Valencia | **1 credit, 32 contact hours (32 lab)**, corroborated across DSC/Broward/Gulf Coast/CF/NWFSC | turned a family-derived estimate into a sourced value |
| `RTV1510` | DSC gave 4 credits | **SCF publishes the same number at 3 credits**, titled as an *introduction* | credit drift that only a second institution could expose |

**Search result snippets often carry credits and contact hours directly**, so a search can answer the
question even when every candidate URL is unreadable. Always try to convert a search hit into a
**fetchable URL** and record the pattern here — that is the compounding part.

### Fetchability re-tested 2026-09-02 — corrections to the table above

| Source | Result | Note |
|---|---|---|
| **State College of Florida (SCF)** | ✅ **CONFIRMED fetchable** | `https://catalog.scf.edu/preview_course_nopop.php?catoid=<n>&coid=<n>` returns full course detail. Verified on RTV1510 (`catoid=18&coid=27867`, current catalog; `catoid=10` is an older one). This is the **first Acalog site confirmed working** — the ids still are not guessable, so capture them from search hits. SCF also publishes program pages such as `scf.edu/Academics/Radiography/coursedescriptions.asp`. |
| **Northwest Florida State** | ❌ still 403 | The block is **domain-wide**, not just `preview_program.php` — `preview_course_nopop.php` returns 403 too. Do not retry any `catalog.nwfsc.edu` URL. |
| **College of Central Florida** | ❌ empty | `catalog.cf.edu/preview_program.php` returns nothing to WebFetch. Its Acalog course URLs are untested. |
| **FSCJ** | ⚠ mixed | `catalog.fscj.edu/courses/<numeric-id>` works (already recorded); `catalog.fscj.edu/preview_program.php` and `floridastatecollegecatalog.fscj.edu/preview_*` return **403**. |
| **Tallahassee State** | ❌ empty | `catalog.tsc.fl.edu/preview_program.php` returns nothing. |
| **Broward program maps** | untested, promising | `catalog.broward.edu/programs-study/<program-slug>/<program-slug>.pdf` — program maps with credits in context. Worth trying when a program-level view is needed. |
| **Florida SouthWestern (FSW)** | ✅ **CONFIRMED fetchable 2026-09-02** | `https://catalog.fsw.edu/preview_course_nopop.php?catoid=<n>&coid=<n>` returned FFP2610 in full (credits, prerequisite, description). **Second Acalog site confirmed working**, after SCF — the Acalog platform is fetchable in general; the blockers elsewhere (NWFSC 403, CF/TSC empty) are site configuration, not the platform. ids still not guessable: capture from search. |
| **Polk State** | ✅ **CONFIRMED fetchable 2026-09-02** | `https://catalog.polk.edu/preview_course_nopop.php?catoid=<n>&coid=<n>` returned CAP3744 in full, including the **contact-hour line** ("3 hours Lecture"). **Third working Acalog site** after SCF and FSW — at this point treat Acalog *course* URLs as fetchable by default. |
| **Florida International (FIU)** | ✅ **CONFIRMED fetchable 2026-09-02** | `https://catalog.fiu.edu/courses/<numeric-id>` returned HSC4553 in full. Same shape as the FSCJ `/courses/<numeric-id>` pattern; **id is not guessable**, so surface it with a search scoped to `catalog.fiu.edu`. Valuable because FIU carries upper-division health-science and professional courses the state colleges do not. |
| **Pasco-Hernando (PHSC)** | ❌ TLS certificate mismatch | `info.phsc.edu/course-schedule/course/<coursenum>` is a clean, **guessable** URL pattern — but WebFetch aborts on a certificate error (the host is served from Pantheon and the cert does not cover `info.phsc.edu`). A third distinct failure mode alongside 403 and empty-render. Do not retry. |
| **Florida Gateway (FGC)**, **College of Central Florida (CF)**, **Tallahassee State (TSC)** | ❌ empty | `preview_program.php` returns nothing to WebFetch at all three. Their `preview_course_nopop.php` course URLs are untested and, given SCF and FSW, may well work — try one before giving up on these institutions. |

> **⚠ Refinement worth generalizing (2026-09-02):** on Acalog installs, **`preview_course_nopop.php` works
> and `preview_program.php` does not.** FSW proves the split on a single domain — its course URL returned
> FFP2610 in full while its program URL returned nothing — and FSCJ shows the same shape (`/courses/<id>`
> fetchable, `preview_program.php` a 403). So a "dead" Acalog institution is usually only dead at the
> *program* view. **Always try a course URL before writing an institution off**, and don't spend calls on
> program URLs. The corollary: program-level views (which show credits *in context*, per rule 21) have to
> come from Miami Dade, Santa Fe, or Broward's program-map PDFs instead.

**Rule for adding a source here:** verify a candidate pattern on **two different prefixes** before recording
it as fetchable. FGCU is the cautionary case — a real, correct, constructible URL whose HTML *and* PDF both
return empty to WebFetch, while indexing perfectly well for search.

### When a value cannot be verified, defer the course

Standing guidance from Ron (2026-09-01): document reliable sources and **skip what cannot be verified until
the search budget renews**, rather than guessing. The test:

- **Safe to derive** — values effectively invariant across institutions (3-credit/45-hour upper-division
  lecture courses in CS, business, social sciences), or confirmed by an *internally consistent published
  family* here. Firearms at **80 clock hours** across both CJK0040C and CJK0570 is what supported CJK0255.
- **Not safe — defer** — anything whose published family already shows real spread: **PSAV clock-hour**,
  **clinical**, **studio/lab**, and health-program courses. Guessing these is how DES1100C/DES1200C went out
  wrong on both credits and hours.

Leave deferred courses `queued` and list them here so they are picked up rather than silently dropped.

**Deferred pending verification (updated 2026-09-02):** `STS1323C`, `MUS2360C`, `OTH2300C`, `IND2500`.

**Cleared 2026-09-02 by Tier 0 (DSC catalog fetch)** — three deferrals resolved in minutes once the DSC
page was fetched, which is the strongest argument for the Tier-0-first rule:

| Was deferred | DSC page gave | Outcome |
|---|---|---|
| `DEH1602` | **Periodontology, 3 cr**, prereq DES1840 + DEH1002C, spring | written at 3 cr / 48 hrs (DEH family runs 16 hrs/credit) |
| `DES0103C` | **Dental Materials and Laboratory Procedures, 90 clock hrs**, prereq DES0002, coreq DEA0020C, $99 lab fee | written at 0 cr / 90 hrs — the deferral was right, the derived guess would have been wrong |
| `MEA0334C` | **Coding for Medical Assisting and Lab, 60 clock hrs**, prereq MEA0005 | written at 0 cr / 60 hrs |

⚠ **`MUS2360C` and `OTH2300C` were deferred as "not DSC courses" — that was wrong.** DSC carries
**`MUS2360`** ("Learning Basic Music Using the Computer") and **`OTH2300`** ("Psychosocial Occupational
Therapy") *without the C suffix*. See rule 22. `STS1323C` is likewise `STS1323` at DSC. They stay
deferred pending a decision on how to treat the suffix mismatch, not for lack of data.

**Earlier note:** `STS1323C` (Surgical Procedures I) — its own family runs 2/45, 3/60 and
4/90; pair STS2324C is 4/90 but Procedures I could legitimately be 3 credits.

---

## Tier 3 — Statewide references

- **SCNS** (`flscns.fldoe.org`) — the authority on course numbering and equivalency. Hard to
  query programmatically; useful for confirming a number exists and at what level.
- **Online Sunshine** (`leg.state.fl.us`) — Florida Statutes, free and authoritative. Used
  constantly for the regulatory content that makes guides Florida-specific.
- **Florida Administrative Code** — rules (65C-22 child care, Chapter 33 corrections,
  6A-6.054 reading intervention, 6A-4.02451 ESOL).
- **FLDOE program pages** — Just Read Florida, ESOL endorsement, BEESS, ECPC guidelines.
- Licensing boards: **Florida Board of Nursing**, **Board of Dentistry**, **Board of
  Respiratory Care**, **DOH Bureau of Radiation Control**, **DBPR**.

---

## Contributed sources

*Sources Ron has found and wants used. Add them here with a note on what they are good for.*

<!-- Format:
### <Name> — <URL>
What it gives, and when to reach for it.
-->

*(none yet)*

---

> ### ⚠ CORRECTION TO A STANDING RULE — Florida course levels and transfer (Ron, 2026-09-01)
>
> Guides in this repository repeatedly used the formula *"SCNS equivalency applies to the same number at the
> same level, never across numbers"* in a way that implied the **1000 vs 2000 boundary blocks transfer**.
> **It does not.** Ron's correction:
>
> - **The first digit denotes the YEAR of offering** — 1 = first year, 2 = second, 3 = third, 4 = fourth
>   — **not transferability**.
> - **1000- and 2000-level courses transfer transparently** between Florida public institutions.
> - **2000 → 3000 is the problematic step** — the lower-division to upper-division boundary is the real
>   one, because upper-division credit generally must be earned at the upper-division level.
> - **3000 → 4000 is fine** — both are upper division.
> - **PSAV (0-level) does not transfer as college credit** at all; that runs through articulation, not
>   transfer.
>
> **What remains true, and must be stated separately:** SCNS equivalency is keyed to the **course number**. A
> program requiring a specific number is satisfied by that number from any participating institution. A
> *different* number with similar content **still transfers as credit**, but the receiving program decides
> whether it fills that requirement or counts as elective. That is a **curriculum** question, not a transfer
> barrier — and conflating the two is exactly the error that was made.
>
> **Corrected 2026-09-01 (7 guides, republished):** ART1500C, ART2500C, CGS1570, DAA2105, DAA2205, PGY1800C,
> TPP1111. **Verified still correct:** EEX4265, which says a 1000- or 2000-level ESE course will not satisfy
> a **4000-level** requirement — that genuinely crosses the division boundary.
>
> **Going forward:** reserve level-based transfer warnings for **2000 → 3000** and for **PSAV → credit**.
> For same-division number differences, frame the issue as *which number a program requires*, never as
> whether the credit transfers.

## Recurring findings worth checking every time

These have each caught a real error or produced a real finding more than once:

1. **Credit values vary across institutions** for the same SCNS number — MAS3105 is 3 credits
   at three institutions and 4 at UNF; RTE2782 is 2 at Santa Fe and 3 at FSCJ; RTE1418C is 3
   at FSCJ and 5 at SCF. Always check two or three catalogs and document the variation.
2. **Different SCNS numbers for the same subject** are not interchangeable — FIN3400/FIN3403,
   BUL2241/BUL3130, CCJ1010/CCJ2010, MAN2021/MAN3025, MAS3105/MAS4105, PLA2800/PLA1800C.
   SCNS equivalency applies to the same number at the same level, never across numbers. This
   is the single most useful thing a guide can warn a transferring student about.
3. **`C`-suffix courses are not always 60 contact hours.** Fire service and education courses
   commonly carry `C` at 45 hours because the state certification module is 45. The validator
   warns; explain rather than inflate the number.
4. **PSAV courses take `credits: 0`.** The clock-hour count goes in `contact_hours`. Some
   catalogs report the clock hours in a field labelled "credit hours" (Seminole's CJK0421
   showed "4.00 credit hours" for a 4-clock-hour course) — cross-check before trusting it.
5. **Lecture and clinical/lab are usually separate courses** in health programs, and the
   credit count badly understates the time — DEH1800 is 2 credits with DEH1800L at 128
   clinical hours; DEH2804L is 4 credits at 192; NUR1020 is 3 cr/48 hr with NUR1020L at
   2 cr/112 hr. Confirmed in both dental hygiene and nursing, so treat it as the default
   for any health program: **find the split before writing the combined `C` course**, and
   compare contact hours, not credits. It runs **both ways** — a combined `C` clinical
   course hides 160–200 hours, while a 1-credit `L` lab is ~32 hours (≈2 hr per credit),
   small on the transcript and large on the calendar. Same rule, opposite direction.
   It is **not only health programs**: AFROTC/ROTC courses carry 1 credit against a
   zero-credit Leadership Laboratory plus PT (~5–7 hr/wk), and studio courses (dance,
   directing) run ~2 contact hours per credit plus unscheduled rehearsal. Whenever a
   course has a required zero- or low-credit companion, state the **real weekly
   commitment** in the guide.
6. **A `C` suffix does not always mean lecture+lab.** Beyond the fire/education 45-hour
   cases, ENC0027C carries `C` because SB 1720 *integrated reading and writing* into one
   course — it is 3 lecture hours, ~45 contact. Read the suffix in the discipline's own
   terms before assuming 60 hours.
7. **The same *subject* can live in two number families, with a third that looks similar
   but is not equivalent.** Algebra-based physics is PHY1053/1054 *and* PHY2053/2054;
   calculus-based is PHY2048/2049. Business capstone is GEB4891 *and* GEB4890 *and*
   MAN4720. Before writing, check whether a second number family exists — and say which
   audience each serves, because picking wrong can cost a student a year.
8. **The same number can carry four different titles.** RTE2563/RTE2563C is the worst case
   found so far (see the table below). When titles diverge this far, the content diverges
   too — hedge hard, use Optional generously, and put a comparison table in the guide.
9. **Some college courses are simultaneously state certification courses.** FFP1510 is
   BFST1510/ATPC1510; the required "textbook" is the Florida Fire Prevention Code itself and
   delivery mode is dictated by the state syllabus. Check whether a course has a Bureau of
   Fire Standards / FDLE / FLDOE counterpart before writing the Resources section.
10. **Florida-specific law is what makes a guide worth reading — but it must pass a
    relevance test.** Include a Florida fact only if it changes what *a student taking
    this course* should do, know, or expect. A true Florida fact that serves no one in
    the room is padding, and it dilutes the flags that matter. Caught in review of
    batch 24: FIN1100 carried Florida's half-credit high-school financial literacy
    requirement (SB 1054) as a flag — accurate, but it is K-12 policy that tells a
    college personal-finance student nothing, and the "career angle for education
    students" framing was a stretch, since education students are not this course's
    audience. It was removed. Ask: *who in this class acts differently because of this?*
11. **Verify currency on any live legal claim — Florida law moves.** Two errors reached
    a finished draft in batch 24, both caught only on a challenge:
    - **FCRA filing deadlines**: the guide described a pre-amendment ambiguity as
      current. **HB 1407 (2026), effective July 1, 2026**, revised the Ch. 760
      procedural framework to resolve a court split. (Correct figures: **365 days**
      FCHR charge window vs **300 days** EEOC — the *state* window is the longer one.)
    - **Non-competes**: the guide stopped at § 542.335 and missed the **CHOICE Act**,
      effective **July 3, 2025** — non-compete and garden leave up to **four years**,
      presumption of enforceability, mandatory preliminary injunctions for covered
      employers.
    Search for amendments before asserting a statutory rule, especially in employment,
    insurance, condominium, and education law.
12. **Draft `prerequisites` at ~450 characters, not ~500.** The server cap is 500 and drafts have
    exceeded it in nearly every batch — five of eight in batch 32 — costing a validate/trim/revalidate
    round trip each time. The field is a *pointer*, not a summary: name the gate, the key numbers, and
    the one caution that would change enrolment, and let the guide body carry the rest. If a
    prerequisite needs three sentences of nuance, that nuance belongs in Special Information.
13. **Distinguish catalog-verified numbers from inferred ones.** Contact hours derived
    from a suffix convention, or from an *analogous* course at a college that does not
    offer the target number, are estimates. Say so in the guide rather than presenting
    them with the same confidence as a figure read off a catalog.
13. **Florida-specific law is what makes a guide worth reading.** The Consent Decree (ESOL),
   the 85% sentencing rule, § 316.066 crash report privilege, § 92.70 eyewitness ID, no
   Medicaid expansion, DCF child care approval, state licensure separate from national
   certification (radiography, respiratory care). Look for it every time.

---

## Course-level findings from production batches

Specific traps confirmed while writing guides. Each one changed what a guide said; check the
list before writing a course in the same family.

| Course | Finding |
|---|---|
| **RTE2563C** | Four titles for one number: *Advanced Medical Imaging* (statewide inventory), *Advanced Image Modalities, Procedures & Pathologies* (Broward, 3 cr/48 hr), *Principles of Radiography III* (Valencia, 3 cr), *Selected Radiographic Special Procedures I* (Daytona State, **5 cr**). Guide uses 3/60 and carries a comparison table. |
| **DEH2806C** | Credits understate time ~4×. Broward splits it: DEH2806 = 1 cr/16 hr lecture + DEH2806L = 4 cr/**192** clinical hr. Hillsborough carries combined DEH2806C at 4 cr. Guide uses 4/208 and prints the whole clinical ladder (DEH1800L 2/128, DEH1802L 4/192, DEH2804L 4/192, DEH2806L 4/192). |
| **CJK0013** | Parallel-series course, 40 hr. Counterpart in the 770-hour series is **CJK0021 Serving Your Community at 34 hr** — not equivalent. See the CJK version table above. |
| **ENC0027C** | Institutional (non-degree) credit. `C` = integrated reading+writing, not lecture+lab; 3 lecture hr. Appears as ENC0027 *and* ENC0027C under six different titles across FL. Prereq numbering varies (ENC0017 / ENC0025 / REA-prefixed). |
| **FFP1510** | = BFST1510 / ATPC1510 at the Florida State Fire College. 45 hr, no prereq, **traditional classroom delivery required** by state syllabus, required text is the tabbed Florida Fire Prevention Code + FS633/FAC69A. Satisfies part of Fire Inspector I pre-certification — but only if the section is state-approved for the cert track. |
| **EDF4430** | Four titles: *Classroom Assessment* (DSC, FSU), *Measurement, Evaluation, and Assessment in Education* (Seminole), *Measurement for Teachers* (USF), *Educational Tests and Measurements*. Florida content must reflect **B.E.S.T. Standards** and the FSA→**FAST** progress-monitoring shift; pre-change material describes a system Florida no longer uses. |
| **CJJ2002** | CJJ / CCJ / CJK are distinct prefixes, not interchangeable. Florida hooks: civil citation (§ 985.12) and **direct file** — Florida long led the nation in prosecutorial transfer of juveniles to adult court. |
| **BCN1251C** | DSC titles it *Architectural Drawing I and Lab*. Florida drawing sets show wind speed/exposure/risk category, HVHZ impact requirements + Notice of Acceptance product approvals (Miami-Dade/Broward), and flood elevations — content northern sets lack. |
| **PLA2600 / PLA2610** | Santa Fe offers PLA2600 **spring only** and PLA2610 **fall only**. Single-term offerings are common across paralegal practice courses and can add a year — say so in Prerequisites. |
| **PET2622C** | Athletic training is now **master's-entry**; bachelor's professional programs were phased out. Exertional heat stroke standard of care is **cool first, transport second** (cold water immersion). |
| **MSL3201C** | MS III enrollment normally requires **contracting** and a service obligation; the basic course does not. Carried as MSL3201C or MSL3201 + MSL3201L. |
| **NUR1020C** | Same pattern as DEH2806C, second discipline. Broward splits it: NUR1020 = 3 cr/48 lecture hr + NUR1020L = 2 cr/**112 clinical hr**. FSW and FSCJ carry combined NUR1020C at 5 cr. Guide uses 5/160. Florida hooks: Board *approval* ≠ ACEN/CCNE *accreditation*; Level 2 screening (Ch. 435); **Florida is a Nurse Licensure Compact state**. |
| **GEB4891** | Live credit-loss trap: **USF uses GEB4890** for the identically-titled capstone, and FIU and others use **MAN4720**. Three numbers, one title, no SCNS equivalency across them — a transfer student can be made to repeat a capstone. |
| **ITA1120C / ITA1121C** | Credits vary **3 → 4** and it changes a degree outcome: many FL B.A. degrees need 8–10 credits of one world language, so two 3-cr courses can leave a student short. Broward 4 cr/64 hr; Santa Fe ITA1120 3 cr (incl. 1 required lab hr); MDC ITA1121 4 lecture hr. Here `C` = **language lab** — a third distinct meaning of the suffix. |
| **MSL3202C / MSL4302C** | Credits **3 (FSU) vs 4 (UCF)**. Two titles each: MSL3202 = *Leadership in Changing Environments* (FSCJ) / *Leadership and Ethics*; MSL4302 = *Leadership in a Complex World* (FSCJ) / *Officership* (UCF, FSU). Content is consistent anyway because **USACC directs the POI centrally** — say so rather than hedging. Contracting/service-obligation warning carries across all advanced-course MSL guides. |
| **MMC1000** | Four titles statewide; **MMC1000 ≠ MMC1009**. Florida hook: Government-in-the-Sunshine + Ch. 119 public records, among the broadest access regimes in the country. Textbook media statistics go stale faster than editions — send students to Pew / Reuters Institute. |
| **HUS1001** | Florida credential ladder runs through the **Florida Certification Board** (CBHT → CAP), not a state license at entry. Child welfare is **privatized** to community-based care lead agencies; no Medicaid expansion; Ch. 39/415 mandatory reporting attaches to the worker personally. |
| **PHY1054C** | The **algebra-based** sequence carries two numbers: PHY1053/**PHY1054** at some institutions, **PHY2053/PHY2054** at Broward (3 cr + 1 cr lab). Separately PHY2048/**PHY2049** is the **calculus-based** sequence (4–5 cr). Wrong pick costs a pre-health student a term and an engineering student a **full retaken year**. Guide carries a three-row comparison table. |
| **RTE1513L** | The **inverse** of the combined-clinical pattern. FL health labs run **~2 contact hours per credit**: RTE1513 = 3 cr/48 hr, **RTE1513L = 1 cr/32 hr**, and the same 1:32 ratio holds for RTE1111L, RTE1418L, RTE1503L, RTE1523L, RTE2112L. Small on the transcript, large on the calendar. Same rule as the `C` courses, opposite direction. |
| **SCE3310** | **Florida science is not B.E.S.T.** B.E.S.T. covers **ELA and mathematics only**; science runs on the **Next Generation Sunshine State Standards for Science**, and Florida has **not** adopted NGSS — so NGSS-aligned national lesson banks do not map to FL benchmarks. Use **CPALMS**. Grade-5 science assessment is cumulative over grades 3–5. |
| **WOH2012** | Does **not** satisfy Florida's civic literacy requirement (§ 1007.25) — that needs **POS2041** or **AMH2020**. WOH (world) / EUH (Western civ) / AMH (US) are three non-interchangeable sequences. |
| **ACG4401C** | Numbering varies: ACG4401 / **ACG3401** / ISM numbers. Current hook: the restructured CPA Exam has an **Information Systems and Controls (ISC)** discipline section this course maps onto. Florida licensure needs **150 semester hours**; the rules for *sitting* vs *licensure* differ and are widely confused. |
| **SBM2000** | The most Florida-actionable business guide so far: **Sunbiz** registration + **May 1** annual report deadline (steep non-waivable late fee), no state personal income tax, DOR sales tax, **county and municipal** business tax receipts, DBPR trade licensing, the free **Florida SBDC** network, and hurricane continuity (business interruption coverage ≠ property coverage; SBA disaster loans have short windows). |
| **THE1000 / TPP2300C** | Florida's live-performance economy is unusually large — theme parks and cruise lines employ performers and technicians at a scale few states match; convention/corporate events absorb technical talent. THE1000 performance attendance has **fixed dates** and a ticket cost. TPP2300C: performance **rights** are required for any showing outside the class. |
| **AFR1101C / AFR2130C** | New extreme on credit-to-hour ratio. UWF lists **AFR1101L / AFR2130L as 0-semester-hour** Leadership Laboratory corequisites: 1 cr of class + ~2 hr/wk LLAB + expected PT = realistically **5–7 hr/wk for one credit**. ⚠ Do **not** copy Army MSL contracting language: the AFROTC **GMC carries no service obligation**; obligation attaches at **Field Training / POC entry**. AFR (Air Force) / MSL (Army) / NSC (Navy) are distinct programs. AFROTC also commissions into the **Space Force**. |
| **BSC1085C** | Three configurations statewide: **BSC1085C**, **BSC2085C**, and split **BSC2085 + BSC2085L** (3+1). Highest-stakes prerequisite in FL allied health — limited-access programs admit on prerequisite GPA, retake policies differ, and withdrawing has a deadline. Some programs impose a 5–7 year **recency** requirement. |
| **FFP0030C** | PSAV, **191 clock hours, 0 credit**. Firefighter I alone is a *partial* credential: FL certification needs **Firefighter I + II + state exam**, and most FL departments hire **Firefighter/Paramedics** — plan the EMT/paramedic path alongside, not after. College-credit fire courses are the FFP1xxx/FFP2xxx numbers. |
| **DEH2702C** | Broward carries the same content as **DEH2701C** (2 cr / 44 hr = 32 lecture + 12 lab). Found by checking the split *before* writing, per recurring item 5. FL hooks: fluoridation coverage varies by county and several municipalities have recently voted to discontinue it; dental HPSAs cover much of rural FL; limited adult Medicaid dental, no expansion. |
| **DEH2400** | Compact lecture course: **2 cr / 32 hr**. Organizing principle is the scope line — the hygienist does not diagnose, but *notices, describes precisely, refers*. HPV-associated oropharyngeal cancer breaks the traditional tobacco/alcohol risk profile, so screening cannot be limited to traditional risk groups. |
| **ACG4501** | Fund accounting requires **unlearning** corporate intuitions (no owners' equity; expenditures ≠ expenses; budget entries are recorded). FL-specific credential worth naming: the **CGFO** (Florida GFOA) — realistic for municipal finance without a CPA. FL has 67 counties, 400+ municipalities, 67 school districts, 1,000+ special districts, all publishing ACFRs. |
| **DAA2610C** | **2 credits**, not 3 — studio contact hours exceed the credit line before counting outside rehearsal. Same logistical failure mode as TPP2300C: cast and book studio early. |
| **MAN4402** | Two currency errors caught only on challenge (see recurring item 11). Correct FL overlay: right-to-work (Art. I §6); **FCRA** Ch. 760 — 15+ employees, adds **marital status**, **365-day** FCHR charge window vs **300-day** EEOC, framework revised by **HB 1407 eff. 7/1/2026**; **no state FMLA**; workers' comp **1 / 4 / 6** employees (construction / non-construction / agricultural); non-competes under **§ 542.335(1)(g)1** (courts *shall not* weigh employee hardship) **plus the CHOICE Act eff. 7/3/2025** (non-compete + garden leave up to **4 years**, presumption of enforceability). |
| **MAN4320** | **Florida E-Verify**: private employers with **25+** employees, § 448.095 (SB 1718), eff. 7/1/2023 — distinct from and additional to the universal federal Form I-9. Under 25 employees: I-9 documentation only. Course content hook: structured interviews substantially outperform unstructured ones. |
| **FIN1100** | Richest FL personal-finance overlay: homestead exemption + **Save Our Homes** cap (identical neighboring houses carry different tax bills; buyers must estimate on *their* assessment), portability, **March 1** filing deadline; highest-in-nation homeowners premiums with **Citizens** as insurer of last resort (national-average premiums break any FL affordability model); flood is **separate** coverage; constitutional homestead **creditor** protection; constitutionally-set minimum wage above federal. ⚠ Relevance lesson: SB 1054's HS financial-literacy requirement was **removed** — true, but K-12 policy irrelevant to this course's students (recurring item 10). |
| **PHY1053C** | First half of the pair; reuses the PHY1053/1054 vs PHY2053/2054 vs PHY2048/2049 table from PHY1054C. Health-professions programs require the **full year**. |
| **HIM2253C** | **The credential outranks the credits**: AAPC **CPC** (physician/outpatient, where CPT lives) or AHIMA **CCS/CCS-P**; **CPC-A** apprentice designation until 2 years' experience (or 1 year + approved education). **Current-year** code books mandatory — CPT revises annually eff. Jan 1 and the cert exam is open-book with the current edition. Broward carries no HIM2253C (splits across HIM1253C / HIM2232C / HIM2728C). |
| **HSC1000C** | Practical gate content: **Level 2 background screening** (Ch. 435) plus drug screen, immunizations, physical, provider CPR, liability insurance — weeks of lead time, and a Level 2 can **disqualify**, which is far better learned before investing in a limited-access program. |
| **MSL4301C** | Completes the Army sequence: **MSL3201C → 3202C → [Cadet Summer Training] → 4301C → 4302C**. MS IV inverts the role — cadets run the battalion. Content is heavily **staff process** and **training management**, which is what a new lieutenant actually does. |
| **OST1100C** | Honest framing: typing speed matters less every year, **document formatting competence does not**. Self-taught fast typists typically see speed *drop* 2–3 weeks while relearning touch technique — quitting during that dip is the main failure mode. MOS Word certification is worth pursuing. |
| **FFP0030C / FFP0031C** | ⚠ **Corrected a live guide.** Minimum Standards totals **492 clock hours**, not ~400: FFP0030C = **191**, FFP0031C = **301**. The halves are *not* even — Firefighter II is ~60% of the program and carries most live fire, extrication, and survival work. FFP0030C republished as **v1.1**. Found only because the second half was verified against a catalog instead of inferred. |
| **FFP1810C** | Fire-service `C`-at-45 exception (recurring item 3) — 3 cr / **45 hrs** because **BFST1810 / ATPC1810** is a 45-hour state module; the `C` marks applied work, not a lab schedule. Same as FFP1510. Satisfies part of **Fire Officer I** pre-certification *only if the section is state-approved for the cert track* — ask the coordinator. Current-content hook: **UL FSRI flow-path research** has revised tactical doctrine, so pre-2010 material teaches tactics the evidence no longer supports. |
| **Fire track split (general)** | The `0` in the thousands position is the tell. **FFP0xxx** = PSAV, **0 credit**, clock hours → *Firefighter* certification. **FFP1xxx / FFP2xxx** = 3 credits, 45 hrs → A.S. Fire Science **and** Fire Officer I / Inspector I. Minimum Standards hours reach a degree only via *local* articulation, never statewide SCNS. |
| **BSC1020C** | ⚠ **Does not substitute for A&P.** Non-majors one-semester survey; FL nursing/allied health require BSC1085C/1086C or BSC2085C/2086C (or split BSC2085 + BSC2085L). Students take it intending to apply to nursing every term and lose a semester. The `C` is what earns *laboratory* science gen-ed credit. |
| **SPN2221C** | ⚠ **Heritage speakers should ask about a separate track** (commonly **SPN2340**) — more relevant in FL than almost anywhere; heritage students in second-language courses are bored orally and unprepared for written accent/orthography. Also: CLEP/placement can grant the whole sequence. Credits 3–4 (Broward SPN2220 = 4 cr / 64 hr) decides whether an 8–10 credit world language requirement clears. |
| **ASL2160C** | **ASL satisfies the FL world language requirement** — confirm acceptance for the specific degree and the credit count (**4** at Seminole/Broward, **3** at SCF). ⚠ Three courses of ASL does not make an interpreter: requires an **ITP** (e.g. FSCJ's Sign Language Interpretation A.S.) plus **RID** certification. Deaf culture is examined content, not background; community-event attendance is usually required. |
| **BCH3023C** | **3000-level = upper division.** A.A. transfer students must confirm the receiving university accepts state-college upper-division credit *toward the major*; majors' sequences use different numbers (BCH4024+) that are not equivalent. Prereqs (CHM2211 + BSC2010 at USF) are enforced for cause — the course opens on amino acid ionization. |
| **BUL2242** | ⚠ Live credit-loss trap: **BUL2241/BUL2242** (lower division) vs **BUL3130** Legal Environment of Business (upper division, required by many FL bachelor's programs). SCNS crosses neither numbers nor levels. Business Law **II** is the half carrying CPA **Regulation** content — agency, debtor-creditor, business structures, securities. FL enacts the UCC at **Ch. 670–680**; entities at **605 / 607 / 620**. |
| **DAN2100** | Gen-ed humanities, non-majors; distinct from studio technique and **DAA2610C** composition, neither substituting for the other. Performance attendance has **fixed dates** and a cost — same trap as THE1000. |
| **PHY3101C** | Closes the physics-sequence problem: prereq is **PHY2049 + MAC2312** (coreq MAC2313) — the **calculus** track. Neither algebra sequence (PHY1053/1054 *or* PHY2053/2054) reaches it; a student who took the algebra track for a health plan and switches to engineering **retakes the full calculus year**. Also 3000-level → A.A. transfer students must confirm the receiving university accepts state-college upper-division credit toward the major. Split config exists (PHY3101 3 cr + PHY3101L 1 cr, Florida Poly). |
| **HSA4383 / MAN4520** | ⚠ **Same toolkit, two prefixes, not substitutes.** Deming/variation/PDSA/SPC/Lean/Six Sigma in a *clinical + CMS/accreditation* context (HSA) vs a *general operations* context (MAN). Both 4000-level; SCNS crosses neither. Guides cross-reference each other with a comparison table. FL hooks for HSA4383: **AHCA** licensure, **FloridaHealthFinder** facility-level public data, and Florida's **licensed health care risk manager** requirement (Ch. 395) — a credentialed FL career path straight out of this course. Credential hook for MAN4520: **ASQ** ladder (CQIA → Green/Black Belt → CQE/CMQ-OE). |
| **FFP2111** | 3 cr / **45 hrs**, **no prerequisite**, state syllabus published by BFST. ⚠ Seminole titles it **Hazardous Materials Chemistry I** — an accurate signal that much of the content is hazmat, not just structure-fire combustion. Third course confirming the fire credit-track table (FFP**0**xxx = 0 credit PSAV; FFP**1**/**2**xxx = 3 cr college credit). |
| **NUR4169C** | RN-to-BSN upper division; requires program admission and an active FL RN license — not open enrollment. The `C` reflects an **applied EBP project**, not a clinical lab, so hours track a standard 3-credit course (validator warns; explained in-guide). Core idea worth flagging: **statistical vs clinical significance**. Also teaches the research / EBP / QI distinction, which determines whether IRB review is needed. |
| **HFT2500** | Best FL-specific hook in the batch: every county funds destination marketing through the **tourist development tax** (§ 125.0104, F.S.) with statutorily limited permitted uses — explains where DMO budgets come from and what a CVB may spend on. **VISIT FLORIDA** and county CVB research are free assignment data. 2000-level: does **not** satisfy upper-division marketing (MAR3023 is a different number/level). |
| **MAN4120** | B.A.S. Supervision & Management core. Most-used content is the **former-peer supervision** transition and **defensible documentation** (pairs with MAN4402). Worth stating honestly: popular leadership style inventories have weak predictive validity — useful as reflection prompts, poor as diagnoses. |
| **GIS2040C** | Credits **3–4** (3 at TSC/FSU/EFSC, **4 at PHSC**), three titles. Strong FL market — every county property appraiser, WMD, utility, and EM office runs GIS, and these are stable public-sector jobs open at certificate/A.S. level. FL data is free: **FGDL**, county parcel viewers, DEP/FWC/WMDs, FEMA flood layers. Teach **State Plane FL** + **UTM 16/17**; projection mismatch is the #1 beginner time sink. Recommend learning **QGIS** alongside ArcGIS Pro — student licenses expire, QGIS does not. |
| **RTE1111C / RTE1503L / RTE1523C** | Broward's RTE table gives the whole curriculum's ratios exactly: **lecture ≈16 contact hr/credit, lab ≈32, clinical far higher** — RTE1111 3 cr/48, RTE1111L 1 cr/32, RTE1503L & RTE1523L 1 cr/**32** each, and clinicals **RTE1804/1814/1824 at 2 cr / 256 hrs each**. That 2-credit/256-hour clinical is the most extreme case found anywhere in the inventory. Positioning content is distributed across Procedures I/II/III **differently by institution** — RTE1503L material at one college may be RTE1513L at another. Skull/cranial positioning (RTE1523C) is the hardest content in the radiography curriculum. |
| **SON2171C** | **Fourth discipline confirming the split rule** (after dental hygiene, nursing, radiography): SON2171 3 cr + SON2171L 1 cr. Credential-driven like the others but with a twist — **Florida does not license sonographers**, so the **ARDMS RVT** (SPI + Vascular Technology exams) *is* the credential; CAAHEP accreditation gates eligibility. Technical flag: **Doppler angle ≤60°** — velocity depends on cos(angle), stenosis grading depends on velocity, so angle error becomes diagnostic error. Also: work-related musculoskeletal injury is a documented career-ender in sonography; ergonomics is real content. |
| **PSC1121C** | ⚠ Same trap as BSC1020C, different discipline: Broward's **PSC1121 is 3 cr / 48 hrs with ZERO lab hours**. A lecture-only physical science satisfies a *general* science requirement but **not a laboratory** science requirement. Also carries a real, often-unexpected **math prerequisite** (Broward: MAT1033/MGF1131/STA2023/MAC1105+ at C). Non-majors survey — does not substitute for PHY/CHM/GLY/AST. |
| **STS1302C** | **2 credits** at MDC for the lecture version. Credential is **NBSTSA CST**, gated on **CAAHEP/ABHES** accreditation; Florida does not license surgical technologists. Worth stating plainly in-guide: long standing, cold room, call requirements, minimal patient interaction — students should self-select early. Sterile technique is **absolute**, not a judgment call, and the norm of announcing your own contamination is taught explicitly. |
| **PLA2763** | **Four titles** across FL — *Law Office Management* (inventory), *Law Office Procedures and Management* (TSC), *Law Office Management and Technology* (Seminole), *Legal Technology* (DSC) — and the title genuinely predicts content weighting (software vs management). Read the local syllabus. FL hooks: statewide **Florida Courts E-Filing Portal** (paralegals do the filing), **Ch. 5 Rules Regulating The Florida Bar** trust accounting (a leading discipline source). Current: generative AI **fabricates citations** — courts have sanctioned filings citing nonexistent cases; verify every authority. |
| **SSE3312** | Social studies counterpart to SCE3310, same schedule-squeeze problem and same answer (literacy integration, which is evidence-supported since comprehension depends on background knowledge). FL is distinctive here: **§ 1003.42, F.S.** mandates specific required instruction by statute, civics carries a middle-grades **EOC**, and requirements have been **amended repeatedly** — work from current statute, not a textbook. Free FL primary sources via **Florida Memory**. |
| **TPP1110 / TPP2100** | ⚠ **Corrected a live guide (3rd time).** Florida carries introductory acting under **two SCNS numbers**: **TPP1110** "Acting 1" (EFSC, Valencia, Pensacola State, DSC, FIU) and **TPP2100** "Acting I" (FGCU, UNF, Palm Beach State, FIU — which carries both). Both 3 cr, near-identical titles, same content. **TPP2300C** (batch 22) named only TPP2100 as the acting prerequisite → republished as **v1.1** with both numbers and a table. |
| **CHM3120L** | Extends the small-credit/large-hours rule **outside health programs**: 1 cr, 3–4 hr weekly block, plus data reduction and formal reports (students report reports take longer than bench work). Unusual grading — **accuracy against a known unknown value**, so technique errors are graded errors regardless of report quality. The real subject is error propagation and defensible uncertainty, which is what transfers to QC/environmental/forensic work. |
| **DAA1500C** | **Widest single-course credit spread found: 1 to 3.** 1 cr at Gulf Coast State; 3 at EFSC, FSU, FGCU. DAA prefix = "Dance, emphasis on **Activity**" (participatory technique, not lecture). Jazz's African American vernacular origins (Dunham, Cole) are content, not preface. |
| **DEH1002C** | Completes the dental hygiene ladder from the **preclinical** end: DEH1002/1002L ~96 hr combined (credits vary — Broward 2+2, Gulf Coast State 3+3) → DEH1800L 128 → DEH1802L 192 → DEH2804L 192 → DEH2806L 192. Key in-guide point: instrumentation habits formed here are hard to unlearn, and **dull instruments require more force** — sharpening is a safety practice, not housekeeping. Career-ending musculoskeletal injury is a documented occupational reality. |
| **BSC1086C** | Same three-configuration warning as BSC1085C (BSC1086C / BSC2086C / split BSC2086+L). Distinct pedagogical flag: term 2 shifts from **anatomical memorization to physiological reasoning**, so the flashcard method that carried students through A&P I often fails here — concept maps and feedback-loop diagrams work better. |
| **STS2324C** | 4 cr (TCC, HCC). Organizing skill is **anticipation** — memorizing procedures in sequence. **Preference cards** are the real working document and vary by surgeon for the same operation; reading and pulling from one is directly employable. Orthopedics is instrumentation-heavy with vendor trays and reps in the room — worth deliberate focus given FL joint-replacement volume. |
| **CRW2100** | Workshop pedagogy — author often silent during discussion of their own work, because the writer won't be present to explain the story to real readers. Titles vary (*Fiction Writing* / *Introduction to Fiction Writing* / DSC *Creative Writing*). Distinct from CRW2001 (multi-genre) and CRW2300 (poetry). Note: Burroway's standard textbook comes from **FSU**, whose creative writing program is nationally prominent. |
| **CTS2321C** | Rare course practicable **entirely for free** — VirtualBox + any distro, break and restore from snapshots. Guide pushes a home lab hard. Certification ladder: Linux+ → **RHCSA (performance-based, not multiple choice)** → LPIC-1; several FL colleges wrap this into a **College Credit Certificate**. Title signals depth: *Introduction to Linux* (TSC) vs *Linux System Administration* (SCF, SPC, Valencia). CTS2322 continues the sequence. |
| **HSA4502** | ⭐ **Strongest FL credential find so far.** Two statutes: **§ 395.0197** requires every licensed facility to run an internal risk management program *and hire a risk manager licensed under s. 395.10974*; **§ 395.10974** provides that a state license is required to perform as a health care risk manager. Licensing agency is **AHCA**. Demand created **by statute**, not market preference, and reachable via an education-or-experience pathway rather than a graduate degree. National credential (CPHRM) complements but does not replace the FL license. Pairs with HSA4383 (same events, liability side vs quality side). |
| **EEX4070 / EEX4221** | ⚠ **Different audiences, not substitutes.** EEX4070 = **general education** majors (FAU titles it *Inclusive Education for General Educators* and restricts it); EEX4221 = **ESE majors only**, with a 4-course prereq chain (EEX2091 + EEX4050 + EEX4101 + EEX4751). Both guides carry the comparison table. Key in-guide points: implementing an IEP accommodation is a **legal obligation** for the general ed teacher; **accommodations change access, modifications change expectations** (and quietly lower a student's ceiling); **gifted is ESE in Florida** (Rule 6A-6, EP not IEP). EEX4221: grade-equivalent scores are the most misused number in the field. |
| **EAP1520C** | Institutional-credit question again, plus a wrinkle the developmental guides lacked: **F-1 visa holders** must confirm with the DSO how EAP enrollment counts toward full-course-of-study. **EAP ≠ developmental ed** — EAP students are often highly educated in their first language; the constraint is English, not ability. At level 5 the binding constraint is **vocabulary breadth** (Academic Word List), and comprehension failures are often **cultural rather than linguistic**. EAP placement rarely transfers; expect reassessment. |
| **EMS1431C** | Clinical pattern extends to EMS: **2 cr / ~96 hrs**, scheduled in 8–12 hr shifts plus **documented patient-contact minimums** across age groups and complaint categories — a slow shift counts for less, so extra shifts may be required. Connects to the fire guides: most FL departments hire **Firefighter/EMT or Firefighter/Paramedic**, so plan EMS alongside FFP0030C/0031C, not after. FL certification = NREMT cognitive + DOH Bureau of Emergency Medical Oversight (Ch. 401, Rule 64J). |
| **EEC2401** | ⚠ FL **mandatory reporting attaches personally** under Ch. 39 — not satisfied by telling a supervisor, and an employer may not prevent a report; good-faith immunity, penalties for failure. FL early learning structure worth naming: **VPK** is free to all 4-year-olds regardless of income (constitutional entitlement, unusual among states), **School Readiness** subsidies via regional **Early Learning Coalitions**, licensing under **Rule 65C-22**, and **Early Steps** for under-3 referrals. Framing flag: families are rarely "hard to reach" — programs are often hard to reach. |
| **GEB2430** | Best-supported content is **behavioral ethics**: failures are systemic, not villainous — ordinary people, incremental decisions, cultures and incentives that normalize the wrong choice. "I would never do that" is a weak defense. Free high-quality resources: **Markkula Center**, **Ethics Unwrapped** (UT). Data/algorithmic ethics belongs in a current version (connects to ISM4011 and MAN4320's AI screening). 2000-level — does not satisfy upper-division; PHI ethics courses are different courses. |
| **ISM4011** | Management course *about* technology, not a technical course — business majors often mis-expect programming. Core finding: **most IT project failure is organizational, not technical** (unclear requirements, absent sponsorship, scope creep, treating transformation as installation). Excel competence is assumed and interview-tested. Security is a **management** responsibility — "IT handles security" is not defensible. Watch numbering: CGS1000/CGS2100 are lower-division and don't satisfy it; some institutions use **ISM3011**. |
| **RTE1457C** | Credits **2–4** (4 GCSC, 2 EFSC) across three titles (*Radiographic Imaging II* / *Principles of Radiographic Exposure II* / *Principles of Radiographic Imaging 2*). ⚠ **RTE1457 ≠ RTE2457** — first-year exposure/image production vs Broward's second-year *Imaging II*. Best modern content point: digital receptors **rescale the histogram**, so an overexposed image can look fine while delivering excess dose — the **exposure indicator** is the only check, and the failure mode is **dose creep**. |
| **SON2122C** | Same 3+1 split as SON2171C. ⚠ Carries emotional weight the other specialties don't: the OB sonographer is routinely first to see a fetal demise or lethal anomaly **with the patient watching the screen**, and may not disclose a diagnosis — programs teach a protocol for that moment and it belongs in the guide. Measurement accuracy has direct clinical consequence (BPD plane error → weight → percentile → management). No FL license for sonographers; **ARDMS RDMS (OB/GYN)** + CAAHEP accreditation is the path. |
| **TPP2190C** | **Largest time-to-credit mismatch in the repository**: a 1–2 credit practicum consumes 15–25 hr/wk during tech week and performances. Credits **1–3** (FGCU 1, Lake-Sumter 3) and **repeatable** — confirm the repeat limit *and* how many repetitions a receiving institution accepts, since practicum credit transfers less predictably than academic coursework. Technical roles employ more people than performance, especially in FL (parks, cruise, conventions). |
| **SLS1122** | Credits **1–3** (CF 1, DSC 3) — and the scope changes with it (1 cr = study skills seminar; 3 cr adds career, financial literacy, transfer). Most FL-actionable guide in its batch: **FloridaShines**, the **A.A. admission guarantee**, statewide **common prerequisites**, and the **excess hours surcharge** at state universities. Evidence flag worth stating plainly: **rereading and highlighting are among the weakest study methods**; retrieval practice and spacing win, and feel harder, which is why students abandon them. |
| **PGY1800C** | ✅ **Related-course check passed, no correction needed.** PGY1800C (1000-level: camera, optics, foundational workflow) and **PGY2801C** (2000-level: adds substantial Photoshop darkroom) are genuinely different levels — the published PGY2801C guide already said so. Titles vary: *Digital Photography* / *Introduction to Digital Photography* (FSW) / *Digital Art Photography 1* (Santa Fe). Credits 3–4. PGY1801C is Advanced. |
| **LAE3414** | ⚠ Florida's **instructional materials and book objection process** has been amended repeatedly and districts implement it differently — the guide directs candidates to **current statute and current district policy** rather than stating specifics that will age. Professional framing used: know your district's selection/challenge policy, keep a documented rationale, follow the process. Free FL-relevant sources: **CCBC** representation data, **We Need Diverse Books**. Related numbers: LAE4414/LAE4416. |
| **NUR3655** | RN-to-BSN core alongside NUR4169C. Hardest-edged content: **language access is a legal obligation** — qualified interpreters at no cost; using family (especially children) produces documented omission/substitution errors and is often impermissible. **Implicit bias** has measured effects on clinical decisions, notably **pain treatment**, among clinicians who reject bias — so countermeasures are structural (protocols, standardized tools, auditing by demographic group), not intentions. FL: ~⅓ speak a language other than English at home; no Medicaid expansion shapes access. |
| **MHF4404** | Pedagogical payoff is the reason ed programs require it: negative numbers, irrationals, zero, and imaginaries were each **resisted by capable mathematicians for good reasons**, and calculus worked for ~200 years before limits were rigorous — which makes a teacher patient with students meeting them. Correct the Greek-to-Europe narrative: place value and zero via India, algebra systematized in the Islamic world, Chinese negative numbers well before European acceptance. Expect **substantial writing**, which surprises math students. |
| **EPI0030** | ⭐ The `0`-level number was the tell. **Educator Preparation Institute** = Florida's state-authorized alternative route to the Professional Educator Certificate for holders of a bachelor's in *any* discipline; ~21 credit hours, competency-based, delivered at state colleges. Heavy use by career changers and by people already teaching on a **temporary certificate** (which has a time limit) who must complete an approved program to convert it. **Non-degree credit** — certificate of completion + certification eligibility, not a degree. Guide lays out all four FL certification routes. Candidates should get an **FLDOE statement of eligibility** early. |
| **COP2220C** | ⚠ **Real numbering trap**: most FL institutions teach **C** under COP2220, but **St. Petersburg College lists it as "Programming in C++"**. Different languages, different idioms; a course in one does not prepare for a follow-on assuming the other. Restates the general lesson — **SCNS guarantees the number transfers, not that the content matches expectation**. Pedagogical flag: pointers are the universal wall; students who *draw memory* get through, students who memorize syntax do not. |
| **COP2700** | SQL is the most durable skill in a computing curriculum (standard since the 1970s, crosses job families). Beginners struggle at **joins**, not syntax — accidental cross joins, left-joins silently becoming inner joins via a WHERE on the null side, fan-out duplicates. ⚠ **SQL injection** is the security topic every student must leave understanding: parameterized queries, never string concatenation. Everything needed is free (PostgreSQL/MySQL/SQLite). |
| **DIG2500C** | ⚠ **Accessibility is a legal requirement**, not an enhancement — ADA and Section 508, with FL public institutions subject and litigation growing. Learnable baseline: contrast, never color-only, keyboard operability, alt text, headings, focus indicators, labeled fields. Second discipline flag: UX hiring is **portfolio-driven** and wants **case studies** (problem → research → alternatives → testing → outcome), not screenshots. Figma has a free education plan. |
| **ART2752C** | ⚠ **Crystalline silica** in dry clay and glazes causes irreversible **silicosis** — never sweep dry, wet-clean, no eating in studio. This is a health matter, not studio fussiness. Expectation-setting that matters: **centering takes weeks**; students conclude they lack talent when they lack repetitions, so **open studio hours** are the variable to ask about before enrolling. ⚠ **ART2751C** is a *different number* with similar content (FAU: *Ceramics: Beginning Wheel*, **4 credits**); ART2752C credits vary 3–4. Four titles statewide. |
| **DIG2030C** | Four titles statewide. Two reliable predictions about a first video course: **audio is where student work actually fails** (external mic, close, monitor with headphones while recording, capture room tone), and students return from shoots **without enough coverage to cut**. ⚠ **Music licensing** is where student work gets taken down — platform detection is automatic, fair use is far narrower than assumed. **DaVinci Resolve** is free and professional-grade (edit + color + audio), so no student is blocked by software cost. |
| **ACG3341** | Conceptual shift: **there is no GAAP for internal reporting** — cost accounting is choosing which distortions to accept for the question at hand. Best behavioral finding: **absorption costing lets a manager inflate income by overproducing** (fixed overhead defers into inventory), which is why variable costing is common internally. Variance analysis has predictable side effects — price variance in isolation encourages cheap inputs → unfavorable quantity variance; connects to MAN4520/Deming on numerical quotas. **CMA** (IMA) is the industry-side credential vs CPA. |
| **EAP1640C** | Pairs with EAP1520C; same institutional-credit + **F-1 full-course-of-study** caution. Advanced-level insight: persistent errors are **systematic, not random**, and depend on first language — articles are the classic case for speakers of article-less languages. So **targeted self-editing beats general grammar review** at this level. Also worth naming: **US academic writing conventions are conventions**, not a monopoly on clarity — students often write competently in a different tradition and receive feedback reading as "disorganized." **Corpus tools (COCA)** answer collocation questions grammar books cannot. |
| **RTE1814L** | ⭐ **The extreme case, now documented directly**: **2 credits / 256 contact hours** (128 hr/credit) — and all three clinical courses (RTE1804/1814/1824) match. Compare: lecture ≈16 hr/cr, lab ≈32. In practice ~2–3 full clinical days per week on the *facility's* schedule, plus travel. **A radiography student cannot reliably hold full-time work during clinical terms.** Structural flag: **ARRT clinical competencies**, not the course grade, gate examination eligibility — track them personally. ⚠ The **repeat rule**: any repeat exposure requires *direct* supervision regardless of competency level. |
| **PRN0090C** | PSAV, **120 clock hours = 80 classroom/lab + 40 clinical**, FLDOE framework **H170602** (Nursing Assistant, Long Term Care), OCP A. Shortest route into FL health care employment and the on-ramp for a great many later clinicians. Certification = **Prometric** written + **skills test**, then FL Board of Nursing registry; the skills test is **strictly scored** (omitting hand hygiene or privacy fails an otherwise competent candidate) and Prometric publishes the checklists free. Ch. 415 reporting duty attaches personally. |
| **RET1264C** | Fifth health discipline confirming the contact-hour pattern. **Florida licenses respiratory therapists** (Ch. 468 Pt. V) *in addition* to NBRC credentialing — and the NBRC structure is worth naming: the **TMC cut score** determines whether you may sit the Clinical Simulation Exam for **RRT** vs settle for **CRT**; aim at the higher score. CoARC accreditation gates eligibility. Four titles statewide. Clinical hook: **ARDSNet low tidal volume by predicted body weight** is a mortality-reducing, evidence-based practice students must be able to calculate. |
| **SON1100C** | First scanning course; credits vary (**2 at GCSC**, 3 elsewhere), four titles, and **SON1000 / SON1214** carry related content at other institutions. ⚠ **Ergonomics is career-preservation content and starts here** — WRMSD is a documented career-ender in sonography, and habits form in the first scanning course. Also: **start ultrasound physics early** — the ARDMS **SPI** is a separate exam and the one candidates most often retake. |
| **HSA4170** | Core concept: **charges are not prices** — chargemaster, negotiated rate, Medicare administered rate, and patient responsibility are four different numbers for one service. ⚠ Title spread signals real emphasis difference: *Healthcare Revenue Cycle Management* (DSC) vs *Financial Management in Health Care* (FGCU). FL context that changes the analysis: **no Medicaid expansion** (payer mix, uncompensated care), **larger Medicare share** than most states, and **FloridaHealthFinder** facility-level open data. Accessible credential: HFMA **CRCR**, no experience prerequisite. |
| **MKA2021** | ⚠ **The SCNS title is dated and misleads students.** *Salesmanship* evokes scripted pitches and pressure closes — precisely what the course now teaches against; DSC's *Building Selling Relationships* describes the content. Assessed skill is **discovery, not presenting** (SPIN research: consequence questions correlate with success). FL angle: insurance (DFS), real estate (DBPR), and securities (FINRA) sales all require **licensure separate from the degree**. Students should learn to read a **compensation plan** — a "draw" can leave a new rep owing money. |
| **MAS4203** | First real proof course for many students — objects are familiar (integers) so **all the difficulty is the reasoning**, which is why programs place it here. Method that works: **compute → conjecture → prove**, using free tools (SageMath, Python, **OEIS**). **RSA** is the hook that makes modular arithmetic concrete. Teacher payoff is specific: divisibility, primes, GCD/LCM and modular reasoning appear throughout secondary curriculum as *procedures*; this course supplies the *why*. |
| **FRE2220C** | ⚠ **Underappreciated FL relevance**: Florida has one of the largest **Haitian communities** in the US, and Haitian Creole is among the most spoken languages in the state. Handle carefully and honestly — **Creole is a distinct language, not a French dialect**, and speakers of one do not automatically understand the other — but French is official in Haiti, vocabularies overlap, and many Haitian Floridians are educated in French. Genuinely useful for healthcare/education/social services in South Florida. Credits 3–4 decide whether the 8–10 credit world-language requirement clears. |
| **SOP2002** | ⚠ **Two number families, and the difference is level, not content.** State colleges use **SOP2002**; universities frequently number social psychology **SOP3004** as an upper-division major course. Both are current. SCNS guarantees SOP2002→SOP2002, but it does **not** satisfy an SOP3004 major requirement — a psychology-bound student should check before assuming. Second flag: the **replication crisis** is now part of an honest treatment of this field — core findings (conformity, dissonance, attribution, bystander) replicated; several flashy priming/ego-depletion effects did not, and the Stanford Prison Experiment is increasingly taught as a research-conduct cautionary tale rather than as a result. |
| **CHD1220** | ⚠ **Two parallel systems students confuse constantly.** College credit (CHD1220, SCNS-transferable) and **DCF-mandated child care training** (licensing requirement, competency exam) are *not* interchangeable in either direction, though Florida articulates some credit for the **CDA**. Second: sections requiring field observation need a **Level 2 background screening** (FDLE/FBI, fee, weeks of lead time) — and a disqualifying offense bars placement *and* the career, with a slow exemption process. Referral pathway is a real competency: **Early Steps** under age 3, district ESE at 3+. |
| **BCN1210C** | ⚠ **The textbook is written for the wrong climate.** National texts assume a heating climate with outward vapor drive; Florida's drive is **inward** most of the year, so an interior vapor barrier — correct in Minnesota — traps moisture and grows mold here. Also Florida-specific: statewide **Florida Building Code** (not local adoption), the **High-Velocity Hurricane Zone** (Miami-Dade + Broward, stricter protocols and its own testing), and the **Florida Product Approval** database — many products need an approval number or Miami-Dade NOA before installation. Residential construction here is **reinforced CMU**, not stick framing, so masonry carries more exam weight than page count suggests. |
| **BOT1010C** | Florida is genuinely one of the best places in the country to study this: ~**4,700 species**, subtropical peninsula spanning temperate and Caribbean flora, and near-national-leading **endemism** (Lake Wales Ridge scrub). ⚠ Flip side: worst invasive plant problem in the continental US, and **FDACS maintains a noxious weed list** — possessing or moving listed species can require a permit or be prohibited, which bears directly on collection assignments. Pedagogical flag worth keeping: **alternation of generations** is the concept students most reliably fail to consolidate, because the dominant generation *reverses* across groups (moss = gametophyte; fern/pine/oak = sporophyte). |
| **COP4610** | The course students describe as making everything else legible — and the one where **concurrency** is genuinely, non-negotiably hard, because the bugs are *non-deterministic* and debugging-by-observation partly stops working. Worth stating outright in the guide: **<em>Operating Systems: Three Easy Pieces</em> is free online and is better for learning than most assigned texts**; recommending it costs the student nothing. Prerequisite chain is real and quiet — weak C/pointer skills produce crashes, not compiler errors. |
| **CTS2375C** | ⚠ **Billing is the practical hazard.** Cloud free tiers are bounded and students have incurred real charges by leaving instances, volumes, or load balancers running — often in a forgotten region. Guide should say: set a **billing alert on day one**, tag resources, and **destroy rather than stop**. Concept employers actually test: the **shared responsibility model**, and that nearly all publicized cloud breaches were *customer misconfiguration*, not provider failure. Vendor-neutral Cloud+ is the right foundation but hiring is provider-specific — pair with an AWS/Azure associate cert; Cloud+ also carries **DoD 8570/8140** weight, which matters for Florida's defense sector. |
| **ASL2150C** | See the correction table below — Florida runs ASL under **two number families** and this course is why. ASL2140→ASL2150→ASL2160 (FGCU and others) parallels ASL1140→ASL1150→ASL2160; in the 2000-level family ASL2150 is "American Sign Language II" and carries its own **ASL2150L** lab corequisite. Credits differ across the same number: **3 at FGCU, 4 at UNF**. |
| **DES1840** | **DES (dental assisting) and DEH (dental hygiene) are separate occupations with separate programs** — assisting does not ladder automatically into hygiene, and students conflate them. Preventive scope (fluoride, sealants) is set by **state law on expanded functions**, so what an assistant may legally perform is a Florida question, not a textbook one. Clinical placement gates: Level 2 screening under **Ch. 435, F.S.**, hepatitis B immunization, physical, CPR. 2 credits / 32 contact hours (2:1 — lecture-weighted, catalog-confirmed). |
| **EAP1500C**, **EAP1620C** | ✅ **Verified structural rule, now documented.** Florida EAP numbering is a grid: hundreds digit = level, tens digit = skill. Level 5 → EAP1500 speech/listening, 1520 reading, 1540 writing, 1560 grammar; Level 6 → EAP1600/1620/1640/1660. All 3 credits; `C` = integrated lab. Skills are taken **independently**, so a student can be Level 5 in speech and Level 6 in reading. Also verified: institutions that allow EAP toward a degree often **cap** it (FSCJ = 6 hours). Two flags kept from the sibling guides: EAP is **not** developmental education (different population, different problem than ENC0027C), and F-1 students must confirm how EAP counts toward full course of study. |
| **EEX4601** | ⚠ **Florida restraint/seclusion law is course content, not a footnote.** § 1003.573, F.S. **prohibits seclusion** of students with disabilities and confines restraint to imminent-serious-injury emergencies — never punishment, never a planned BIP element — with same-day parent notification and state reporting. The Legislature has revised this repeatedly, so the guide tells students to **verify the current statute** rather than trust any course material. Second: field experience ⇒ Level 2 screening on district timelines. Conceptual core worth keeping: **the same consequence has opposite effects depending on function** — hallway removal rewards escape-motivated behavior and punishes attention-motivated behavior. |
| **EMS2603C** | ✅ **Catalog-verified, unusually well.** DSC: EMS2603C = **12 credits**, first of a 4-semester / **42-credit** paramedic certificate (2603C 12 → 2604C 12 + 2666 1 → 2605C 11 + 2667 2 → 2659 internship 4). Contact hours 300 are **inferred** from the EMT precedent (EMS0110C 12 cr / 300 hrs), not catalog-confirmed. ⚠ Two hard flags: 12 credits in one term exceeds a full-time load and students who keep full-time shift work are the ones who fail; and **medication math** carries a 90%+ competency exam with limited retakes at most programs. Also: **verify CoAEMSP/CAAHEP accreditation before enrolling** — NREMT eligibility depends on it. |
| **FIN2000** | ⚠ **The expensive misunderstanding this guide exists to prevent:** FIN2000 (lower division) vs **FIN3400/FIN3403** (upper division) cover the same territory, but SCNS carries equivalence only at the same level — FIN2000 does **not** satisfy a university's FIN3403 major requirement, and at most Florida universities it does not substitute. Prereq genuinely varies: none at FSCJ, **ACG2021 with a C** at EFSC. Pedagogical flag: bond price, stock price, NPV and a loan payment are all **one idea** (time value) in different clothes — students who consolidate it early find the rest to be substitution. |
| **GLY2100C** | ⚠ **Credit-value trap caught by related-course research.** GLY2100C is **4 credits** (verified UF + Seminole State), while the already-published GLY2010C is 4 at UF and **3** at FAMU and several state colleges — so the two-course sequence can total 7 rather than 8. Matters where a program specifies credit totals. Florida angle is stronger than it looks: the peninsula is a carbonate platform on basement rock that **once belonged to Africa** (a Pangaea rift fragment), and it is among the richest **vertebrate fossil** regions in North America. ⚠ Practical: a **Florida Museum of Natural History Fossil Permit** is required for vertebrate fossils on state land and in state waters (river bottoms included); invertebrates and shark teeth are exempt. |
| **HFT1410** | The course title undersells it: the money is in **revenue management**, and rooms are a *perishable* inventory — tonight's unsold room is revenue that never comes back, which is why variable pricing, overbooking and length-of-stay controls exist. RevPAR = occupancy × ADR is the number the industry manages to, and a property can raise occupancy while lowering RevPAR. ⚠ Florida-specific legal layer: **Ch. 509, F.S.** innkeeper statutes and DBPR lodging licensing; **hurricane/emergency procedure** (front office is the communication hub); and Florida-required **human trafficking awareness training** for lodging employees. Career-practical: **night audit** is the fastest route from entry level to supervisor, and naming a specific PMS (Opera, Cloudbeds, Mews) beats "computer skills" on an application. |
| **MAN3353** | ⚠ **Four numbers, one subject** — the clearest rule-7 case yet. MAN2021 (lower division), **MAN3025**, **MAN3303**, **MAN3353** (all upper division) all survey the same four functions. SCNS transfers MAN3353 as MAN3353; whether it satisfies a receiving institution's MAN3025 requirement is articulation, not guarantee — get substitutions **in writing**. FSCJ additionally pairs it with a **GEB3213** prereq/coreq. Worth keeping: management is a *contested* field, several widely taught ideas have weak evidence (strict Maslow sequence, learning styles, some hiring personality instruments) while well-supported ones (structured interviews, specific difficult goals) get less attention — so the transferable skill is evaluating a management claim. |
| **RTE1804L**, **RTE2844L** | ✅ **Rule 5 confirmed against the catalog, and the ratio is now pinned.** Daytona State: RTE1804L = **1 credit**, RTE1814L = **2** (prereq RTE1804L — matches the published guide), RTE2844L = **3**. Applying the verified RTE1814L ratio (2 cr / 256 hrs) gives a clean clinical progression of roughly **8 → 16 → 24 clinical hours per week**, i.e. **~128 hrs per clinical credit**. Hours are derived from that ratio, not separately catalog-confirmed. ⚠ Widest credit spread seen in any course type: RTE1804L is 1 cr (DSC), 2 (EFSC), 3 as "Radiology Practicum I" (FSW), and **4 with 12 clinical hrs/wk** as "Radiographic Clinic I" (FSCJ); RTE2844L is 3 (DSC/Broward/EFSC) and 2 (Tallahassee State). One institution even numbers **RTE1814L as Clinical Education *I*** rather than II. Mitigating fact worth stating in every clinical guide: **radiography clinical coursework does not transfer mid-sequence anyway** — competencies are tracked against one JRCERT-accredited plan. Two hard safety flags: **any repeat exposure is direct-supervision only, regardless of competency** (JRCERT standard, common dismissal cause), and **MRI Zone IV screening** — the magnet is never off. |
| **PPE2001** | ⚠ **The instruments students have heard of are the weak ones.** MBTI has poor test-retest reliability and imposes dichotomies on continuous traits; Enneagram/DISC/color systems fare no better; projectives have their own long validity debate. The **Five-Factor Model**, which most students have never heard of, replicates cross-culturally and predicts job performance, health, and longevity. Teaching students *why* — reliability, validity, dimensional vs categorical — is the transferable skill. Second flag: **heritability is a population statistic**, not "half of me is fixed"; the shared environment explains surprisingly little adult variance, and personality still changes systematically into middle age. Also surfaced: **PSY1012 vs PSY2012** is the same General Psychology at two levels and appears as a prerequisite either way. |
| **SOP2772** | ⚠ **Mandatory-reporting flag — this is the one that could actually hurt a student.** Course content prompts disclosures of assault or abuse; Florida **§ 39.201, F.S.** requires any person who suspects abuse/neglect of a child or vulnerable adult to report, and institutions carry Title IX/Clery duties. Guide tells students to **ask about an instructor's reporting status before disclosing**, or use confidential counseling. Florida specifics verified: minors may consent to their own STD testing/treatment under **§ 384.30, F.S.**; age of consent is **18**, with the 16–17 / under-24 exception in **§ 794.05, F.S.** (stricter than most states and widely unknown). Applied-skill flag: contraception must be read on the **typical-use** column, not perfect-use. Florida law here moves — rule 11 applies. |
| **RED3309C** | ⚠ **Florida legislates early reading more than almost any state**, and it changes session to session: universal screening including **dyslexia characteristics**, third-grade retention with good-cause exemptions, B.E.S.T. ELA standards, and state requirements on instructional materials. Guide tells students to verify against current statute rather than course material. Substantive flag: **the reading wars are over** and three-cueing (guessing from pictures/first letters) is specifically contraindicated — a student may be placed in a classroom still using it. Credential flag worth planning around: the **K-12 Reading Endorsement** is 5 competencies (~60 hrs each; Comp 1 as micro-credential + Comps 2–5 literacy matrix) and many RED courses are aligned to it — ask the advisor. Hardest content is **linguistic**: teachers who cannot segment *box* into four phonemes cannot teach a child to. |
| **SON1000C** | ⚠ **Widest credit variation of any course in this repository so far: 1 to 4 credits** for the same SCNS number (Gulf Coast 1, Polk 2, Valencia 3, combined lecture-lab forms 4). Recorded at the representative 3 cr / 60 hr `C` form. ⚠ **Verify CAAHEP accreditation on the CAAHEP site before enrolling** — the primary ARDMS pathway requires it, non-accredited programs advertise, and graduates discover ineligibility after paying tuition. Two flags students dismiss and shouldn't: **physics (the ARDMS SPI exam) is the gatekeeper** and is cumulative — start Edelman in term one; and **ergonomics is a career-length hazard** — SDMS surveys find ~80% of working sonographers scan in pain, and habits must be built in the first lab because they cannot be retrofitted. Defining property of the field: ultrasound is **operator-dependent** — the study is constructed in real time and exists only in the images the sonographer chose to save. |
| **TPA2200C** | Rule-8 case: same subject as **TPA2200**, **TPA2200C titled "Stagecraft"** (Broward), and **TPA2210** (SCF); some institutions split scenery/lighting/sound into separate numbers instead. Contact hours **64 (32 lecture + 32 lab)** are Broward-catalog-verified. The Florida argument is unusually strong and specific: **themed entertainment** (Disney, Universal, SeaWorld) turns seasonal theatre skills into full-time benefited year-round work, plus the cruise industry out of four Florida ports and the Orlando/Miami convention business. Skills that transfer to that market are **automation, show control, networking, rigging, audio** — not scenic carpentry — plus ETCP certification, Vectorworks, QLab. ⚠ Real physical risk (falls, suspended loads, table saws); OSHA 10 increasingly expected. |
| **TPP1111** | ✅ **Extends the batch-28 TPP2300C correction and confirms it.** Florida runs beginning acting in **two parallel families**: TPP1110 → TPP1111 (1000 level) and TPP2100 → TPP2110 (2000 level). Both current; institutions pick one. That is exactly why TPP2300C's prerequisite had to name both TPP1110 and TPP2100. Core technical flag worth keeping in every acting guide: **play the action, not the emotion** — if a student cannot state the objective as an active infinitive aimed at the partner, the scene will not work. ⚠ Current-practice flag: **intimacy choreography** is now the standard (choreographed, consented, rehearsed identically, de-roled) and **emotional recall using personal trauma has fallen out of favor** in favor of imaginative substitution — students are entitled to expect both, and this is professional practice, not fragility. |
| **ACG3101** | ⚠ **Florida's CPA licensure rules changed in 2026 — rule 11 applies hard here.** The traditional 150-hour requirement is being supplemented in Florida (and many states) by **additional pathways** pairing a bachelor's with a longer experience period, and the exam now follows the **CPA Evolution** Core-plus-Discipline structure. Guide tells students to verify with the Florida Board of Accountancy and NASBA rather than trust a prior cohort, a textbook, or this guide — the difference is a year of tuition. Also flagged: **ASC 606** and **CECL** are the current standards, so older editions and old tutoring videos are substantively (not cosmetically) wrong. Career-timing flag: public accounting recruits internships **12–18 months ahead**, so a student taking this in junior-year fall is already in the cycle. |
| **ACG4632** | ⚠ **Independence violations end careers, and the traps are mundane** — a small stock holding (including inside a retirement account), a spouse's job at a client, a client-bank loan, gifts above nominal. New associates are expected to divest *before* a start date. Conceptual core: auditing is **evidence and inference**, not more accounting; the right exam answer is usually "what evidence would resolve this, and how much is enough." Worth keeping: the **expectation gap** — an audit gives *reasonable*, not absolute, assurance — alongside the ACFE finding that **tips, not audits, uncover most occupational fraud**. Florida angle: unusually deep public-sector audit market (Auditor General, agency IGs, county Clerk/Comptroller offices, and a very large number of special districts driving single-audit work). |
| **ACR0001C** | ✅ **Catalog-verified PSAV structure.** 250 clock hours, the middle course of the **750-hour HVAC/R 1** program (ACR0000 → ACR0001 → ACR0012, 250 each). 0 credits — the thousands-position `0` marks non-degree instruction. ⚠ **EPA Section 608 is federally required to purchase or handle refrigerant** — no employer hires without it; take the **Universal** level, not a single type. Current-practice flag that dates a program instantly: the **AIM Act** HFC phase-down has moved new residential equipment to **R-454B / R-32, classified A2L (mildly flammable)**, requiring different leak detection, tools, and handling — while the installed base is still R-410A and R-22. A program teaching only legacy refrigerants is behind, and A2L training is a hiring differentiator. Trade-practice flag: **a low charge means a leak** — topping off without repair is bad practice and often a regulatory problem. |
| **BCA0350** | **A genuinely different pathway shape, worth naming as such: you are hired first, then enrolled.** Florida registered electrical apprenticeship = ~**8,000 OJT hours** paid + ~**576 supplemental classroom hours** over four years, delivered as BCA0350–0357 (two per year) plus co-op numbers for the OJT. Hours here (**72**) are **derived** from 576 ÷ 8, not catalog-confirmed. The apprentice earns from week one, pays little or no tuition, and finishes with no debt — the financial comparison against a degree over a decade is closer than most advising suggests. ⚠ Requires a **sponsor** (IBEW/NECA JATC, ABC, IEC) with limited competitive application windows. Florida-specific licensing flag: **journeyworker licensing is *local*** (county/municipal exams, not portable), while **contractor** licensure is state-level through DBPR as Certified (statewide) or Registered (local only). Tell apprentices to keep their own hour records from year one — the experience requirement is verified. |
| **APA1111C** | ⚠ **APA is not ACG, and picking wrong costs a semester.** APA (Applied Accounting) is practitioner-focused for bookkeeping careers and applied A.S. degrees; **ACG2021** is the transfer sequence for a business degree. APA generally does **not** substitute for ACG2021, and SCNS does not cross prefixes. The advising question is simply: *bookkeeping job, or bachelor's in business?* Contact hours **48 (36 lecture + 12 lab)** are Broward-catalog-verified. Florida payroll specifics a national text gets wrong: **no state income tax withholding**, but employers do owe **reemployment tax** (Form RT-6), and **sales tax carries county discretionary surtaxes** so the rate depends on where the sale occurs. Also flagged: **worker misclassification** (1099 vs employee) is common in Florida construction, landscaping, and hospitality and carries real penalty exposure. Title variant: "Office Accounting I" at Seminole. |
| **ASL2140C** | ✅ **Confirms the ASL2160C correction from batch 33 and completes the picture.** The two families are **ASL1140→ASL1150→ASL2160→ASL2170** and **ASL2140→ASL2150→ASL2160→ASL2170** — they *converge* at ASL2160, which is why the original single-sequence claim looked plausible. FGCU carries ASL2140 at **3 credits + 1-credit ASL2140L**; institutions that integrate carry ASL2140C at **4**. Pedagogical flags worth keeping in every ASL guide: **facial expression is obligatory grammar**, not decoration (a neutral face is ungrammatical, not polite); **voice-off classrooms** are standard and deliberate; and **receptive skill lags expressive** — fingerspelling is read as whole-word shapes, never letter by letter. Professional boundary flag: **fluency is not interpreting**, and offering to interpret at course level can cause real harm in medical or legal settings. |
| **CPO2001** | The course's value is the **method, not the country tour** — exams reward systematic comparison along one dimension, so students should study by building comparison tables (regime type, executive format, electoral system, party system, federal/unitary) rather than memorizing country facts. Highest-value single mechanism: **electoral systems shape everything downstream** — single-member plurality tends toward two parties and clear accountability at the cost of proportionality; PR produces coalitions and closer vote-seat correspondence at the cost of direct accountability. Florida angle that is genuinely distinctive: the state contains large populations with **lived experience** of the systems the course studies analytically (Cuban, Venezuelan, Haitian, Colombian, Nicaraguan, Brazilian, Puerto Rican) — a resource to use, and to handle with care. Backsliding material should be framed analytically, applying the same criteria regardless of who benefits. |
| **DAA1520C** | Tap is **percussion as much as dance** — the sound is the product, so the practice advice is record your *audio* (not just video), use a metronome from day one, and practice slowly, since speed hides errors and slow work exposes them. Technique flag beginners always need: **sound comes from a relaxed ankle**, not from driving the leg — less effort produces more and cleaner sound, and aching shins mean working too hard rather than too much. ⚠ Equipment matters more than students expect: a snug fit is required for articulation, and oversized or cheap-tap shoes actively prevent learning. ⚠ **History flag handled honestly**: tap is a syncretic West African plus Irish/British American form that developed substantially through **minstrelsy** — teaching the technique without that context teaches half the form, and it is why the Hines/Glover rhythm-tap revival was explicitly about reclaiming Black American lineage. Studio credit varies **1–3** across Florida. |
| **EMS2604C**, **EMS2605C** | ✅ **Completes the DSC paramedic sequence with catalog-verified credits** (12 and 11), hours derived at the EMS2603C ratio. Curricular shape worth recording: Paramedic I = foundation (A&P, pharm, assessment, airway); **II = the medical patient** (cardiology is roughly a third of it); **III = trauma, special populations, operations**. ⚠ EMS2604C flags: **Florida's Baker Act (§ 394.463) and Marchman Act (Ch. 397)** govern involuntary examination and are daily paramedic knowledge a national text omits; and **prone restraint / prolonged struggle is dangerous** — restraint-associated death is documented and scrutinized. ⚠ EMS2605C flags: **weight-based pediatric dosing is where fatal medication errors happen** (length-based tape, every time, independent double-check), children **compensate then collapse suddenly**, and **spinal motion restriction changed** — selective SMR replaced routine backboarding, so older instructors and texts diverge. Florida operational realities: hurricane deployment, regional trauma triage, and drowning as a *routine* pediatric call here. |
| **EUH2000**, **EUH2001** | ⚠ **Two number families, and the published EUH1000 guide had missed it** (see the correction table). EUH1000/EUH1001 and EUH2000/EUH2001 are both current and cover the same territory at 3 credits; UCF, USF, Seminole State and Gulf Coast use the 2000 family. Second flag, useful for advising: **EUH does not satisfy Florida's civic literacy requirement** — POS2041 or AMH2020 plus the assessment does — and institutions generally advise taking the **EUH sequence or the WOH sequence, not both**, since they are alternatives covering the same span through different geographic lenses. Intellectual flag worth keeping: "Western civilization" is itself a **contested category** assembled largely in the 19th–20th centuries; classical learning reached medieval Europe substantially **through Arabic translation**, and good courses teach both the narrative and the critique. |
| **EVR2001** | ⚠ **The `C` suffix decides whether it counts.** EVR2001 (lecture-only) does **not** satisfy a laboratory-science general education requirement; EVR1001C/EVR2001C do, and some institutions use a separate EVR2001L. Discovered in the queue only because the already-published guide was EVR1001C — see the correction table. Florida is unusually strong as the case study here: **Everglades restoration (CERP)**, the **Floridan Aquifer and springs** (nitrate loading, reduced flows, karst), **harmful algal blooms** (red tide, Lake Okeechobee), **sea level rise** in Miami-Dade and the Keys as a budget line rather than a projection, and the worst **invasive species** problem in the continental US. Pedagogical flag: teach students to separate the **empirical** question (what is happening) from the **normative** one (what to do) — confusing them produces bad reasoning in both directions. |
| **DIG2251C** | Rule-8 case with four titles on one number: **Digital Audio I**, **Sound for Digital Media** (Gulf Coast), **Audio Production I** (Seminole), **Digital Audio Fundamentals** (IRSC) — all 3 credits, with emphasis shifting between broadcast, sound-for-picture, and general production. Two flags with real teeth: **signal flow is the concept everything depends on** (nearly every audio fault is diagnosed by tracing the chain, and students who learn software procedures instead are helpless when something breaks); and **"fix it in post" is mostly a myth** — clipping is permanent, room reverb cannot be convincingly removed, and thirty seconds of room tone at every location is the most commonly forgotten thing in production. Florida market is stronger than its reputation: themed entertainment show audio, cruise, and the Orlando/Miami convention AV business all hire continuously. |
| **FSS2284C** | ⚠ **Florida licensing flag students planning a business get wrong:** caterers must generally operate from a **licensed commercial kitchen or commissary** (DBPR Division of Hotels and Restaurants); Florida's **cottage food** law permits certain shelf-stable products from a home kitchen but does **not** authorize catering and excludes exactly the temperature-controlled foods catering is built on. Alcohol adds DBPR ABT licensure plus **dram shop exposure (§ 768.125, F.S.)**. Technical flag: **recipes do not scale linearly** — seasoning scales less than proportionally, equipment capacity binds before arithmetic does, so the method is scale → test → adjust. Business flag specific to this course: **the guarantee** (committed headcount) is the number that determines profitability, and late headcount changes, not bad cooking, are how catering jobs lose money. |
| **HIM2652C** | ⚠ **Every access is logged, and audit reports are automatic** — people are fired every year for viewing a family member's, neighbor's, or celebrity's chart, discovered by audit rather than complaint. Students on practicum are held to the same standard. ⚠ **Never delete; amend** — destroying the audit trail looks indistinguishable from concealment in litigation. Documentation-integrity flag: **copy-forward** propagates stale and contradictory data and is a recurring audit and fraud finding. Credential flag: **RHIT requires a CAHIIM-accredited program** — verify on CAHIIM's directory, not the school's marketing; and RHIT/RHIA (HIM) are distinct from CCS/CCA/CPC (coding), complementary rather than interchangeable. Career flag worth stating plainly: **name the EHR** (Epic, Oracle Health/Cerner, MEDITECH) on the résumé — Epic certification is obtained *through an employer*, which is why getting hired into any role at an Epic shop is the known route into the far better-paid analyst track. Interoperability/information-blocking rules are live and moving — rule 11 applies. |
| **PHT2810**, **PHT2820** | ⚠ **The sharpest title-vs-number trap found so far.** PHT2810 is "Clinical Experience II" locally but **"PTA Clinical Practicum 2"** elsewhere; PHT2820 is "PTA Clinic II" locally but **"PTA Clinical Practicum 3"** — i.e. *a course whose local title says II is the third and final rotation*, with PHT2810 as its prerequisite. **Sequence by SCNS number and prerequisite chain, never by the roman numeral in the local title.** Both are **2 credits** (catalog-verified) but are **full-time 6–8 week rotations** — hours (240/280) are derived, and this is rule 5 again at ~120–140 hrs/credit. Accreditation flag: **CAPTE** accreditation is required for NPTE-PTA eligibility and Florida licensure (Ch. 486, F.S.). Scope flag: a PTA **may not evaluate, establish, or alter a plan of care** — Florida sets supervision rules that differ from other states and have been amended, so verify. |
| **PHT1300** | ✅ **Cleanest example yet of the title tracking the credit value.** "**Survey of Pathological Deficits**" = **4 credits** (Broward, College of Central Florida); "**Pathology for the Physical Therapist Assistant**" = **3 credits** (FSCJ, EFSC) — same SCNS number, broader scope carrying the extra credit. Course purpose worth naming: this is **where precautions and contraindications come from**, so the study frame is three questions per condition — what may I not do, what makes me stop mid-session, what makes me call the PT now. Florida-weighted content: **diabetes** above all (inspect the feet; neuropathy means the patient cannot feel a hot modality), plus cardiovascular disease, osteoporosis and fall fracture, stroke, and dementia — the actual Florida caseload. |
| **SON2061** | ⚠ **The SPI is a separate exam and it is what stops people.** No RDMS or RVT credential is awarded until **both** the specialty exam *and* the Sonography Principles and Instrumentation exam are passed — a candidate can ace abdomen and hold nothing. ARDMS permits sitting for SPI early, and programs with strong pass rates recommend taking it while physics is fresh rather than saving it for last. Credit spread is wide again (**1 Broward / 2 EFSC / 3 Polk and HCC**) — in a 1-credit version most of the review burden is the student's to organize. Structural note worth recording: **SON2061 occupies the same terminal registry-review slot as RTE2061** in radiography — the x2061 seminar appears to be a recurring SCNS pattern across imaging prefixes. |
| **MAE4326** | ⚠ **Teacher math anxiety is course content, not a private matter** — research indicates it transmits to students, measurably and in some studies disproportionately to girls. Most of it comes from having learned procedures without understanding, which is exactly what this course remedies. Highest-leverage content: **fractions**, which predict later mathematics achievement more strongly than almost any other elementary topic and where teachers' own conceptual gaps concentrate. Distinctive skill: **read the error, don't just mark it** — children's wrong answers are systematic (302−178=276 is a coherent rule: always take smaller from larger), so re-explaining the procedure does not help and asking the child how they got it does. Florida specifics: **B.E.S.T. math standards**, **CPALMS** as the state's own free repository, and the FTCE K-6 **mathematics subtest**, commonly reported as the hardest of the four. Requires 15 field hours ⇒ Level 2 screening. |
| **MET2010C** | ⚠ **The hurricane cone is the most misread forecast product in the country, and this is the flag with the highest stakes in the batch.** The cone shows the probable path of the **center**, about two-thirds of the time — **not** storm size and **not** where impacts occur. Being outside the cone is not safety (surge, wind, rain and tornadoes routinely extend beyond it), and the cone says nothing about intensity. Two corrections that follow: **storm surge kills more people than wind**, and the **Saffir-Simpson category describes wind only** — a slow Category 1 can be catastrophic. Evacuate on your **zone and county order**, not the line on the map. Florida is the ideal lab: colliding **sea breezes** from both coasts drive near-daily summer thunderstorms, and the state leads the US in lightning fatalities. Same `C`-suffix lab trap as EVR: MET2010 alone is lecture-only. |
| **OST1110C** | Speed is what is advertised, **accuracy is what gets you hired** — a document with errors is worthless regardless of production speed, which is why programs score net speed with an error penalty. Motor-learning flag: **10–15 focused minutes daily beats one long weekly session**, and watching your hands caps you early. ⚠ Occupational-health flag worth taking seriously in a course that has students keying for hours: **repetitive strain injury ends office careers**, and the preventive habits (wrists floating not resting, monitor at eye level, breaks every 20–30 min) are formed early and hard to change later. Employable specifics: learn **styles, not manual formatting**; get the **MOS certification** (cheap, verifiable, and named in job postings); and build **Excel beyond the basics**, which raises the ceiling on the role more than added typing speed. |
| **RMI2212** | ⚠ **The exclusions are the coverage** — read them first, then the definitions, then the endorsements. In Florida the costliest instance is that **flood is excluded** from standard property forms, which is why the NFIP exists separately and why "my house flooded and I have homeowners" is the state's most common coverage misunderstanding. ⚠ **Florida hurricane deductibles are a percentage of dwelling coverage**, not a flat amount — 5% on a $400,000 home is $20,000 before the insurer pays, against perhaps $1,000 all-other-perils; applies once per season, and statutory requirements have been repeatedly amended. Florida market features with no close analogue elsewhere: **Citizens** (state insurer of last resort, with depopulation), the **Hurricane Catastrophe Fund**, recent litigation/AOB reform, and **wind mitigation credits** that many homeowners never claim. Career flag: **college RMI coursework can carry a DFS prelicensing exemption** for the 2-20 or 4-40 license — ask, because getting licensed before graduating makes a student immediately employable. |

**Rule 14 (title-number-credit correlation).** When the same SCNS number carries more than one title,
check whether the **credit value tracks the title** before assuming either. Confirmed cases: **PHT1300**
("Survey of Pathological Deficits" = 4 cr; "Pathology for the PTA" = 3 cr) and, less cleanly,
**GLY2010C** (3 or 4). Worse, the *local* title can contradict the sequence: **PHT2820** is titled
"PTA Clinic II" but is the **third** rotation, with PHT2810 as prerequisite. Sequence courses by
**SCNS number and prerequisite chain**, never by a roman numeral in a local title, and record which
title the recorded credit value belongs to.
| **CGS2820C** | ⚠⚠ **The strongest content-divergence case found so far, and a new failure mode: the number is stable while the *subject* is not.** CGS2820 is "Web Design" at NWFSC (3 cr), "Web Site Design and Development" at FSCJ (**4 cr**, with a prerequisite and authoring tools), and "**Web Programming (JavaScript, Ajax, ASP.Net)**" at **Daytona State** (3 cr) — the queue title from DSC reads simply "HTML". A student expecting introductory markup could land in a programming course, or the reverse. SCNS equivalency does not help here: the number matches and the content does not. Guide leads with a read-the-description warning. Substantive flags: **hand-code before using a tool** (a developer who cannot read generated markup cannot fix it), and **web accessibility is a legal requirement** — the ADA has been applied to commercial sites and **Florida's Southern District is among the most active web-accessibility litigation jurisdictions in the country**. |
| **BCA0351**, **BCA0353**, **BCA0354** | ✅ **Applies the BCA0350 framework from batch 36 consistently** — 0 credits, **72 hours derived** from 576 supplemental instruction hours ÷ 8 courses. Title variation continues inside the same family ("Electricity 2/4/5" here vs "Electrical Apprenticeship I" and "Apprenticeship in Residential Wiring 1" at BCA0350). Year-level content shape recorded: **year 1 residential** (AC theory, load calcs, service, grounding), **year 2 commercial/industrial** (three-phase, transformers, motors, motor control), **year 3 systems and specialization** (VFDs, PLCs, fire alarm, Art. 517 health care, PV, testing). Career flag worth keeping: **motor control is the gateway to the best-paid work** in the trade, because troubleshooting a control circuit requires reasoning that many electricians never get comfortable with. Conceptual flag: **grounding ≠ bonding** — the most persistent conceptual error in the trade, and Article 250 is a large share of inspection failures. |
| **STS2365C** | The reason a "soft skills" course sits in a surgical curriculum: analyses of surgical adverse events repeatedly find someone noticed and did not say it clearly enough. ⚠ **Speaking up is taught as a graded protocol**, not bravado — question, then stated concern, then direct challenge, framed on patient safety. ⚠ **Counts are a legal obligation**: a retained surgical item is a never event, and the failure happens under closing-time pressure, so the correct response to "it's probably fine" is to say so out loud and document it. Reputation flag: **anticipation** is what surgeons notice — review the procedure beforehand, learn preference cards, keep a personal notebook. Credential flag: **CST via NBSTSA requires a CAAHEP- or ABHES-accredited program**; Florida does not license surgical technologists but employers overwhelmingly require certification. Prefix ratio runs ~22–30 contact hrs/credit (STS1302C 2/45, STS2324C 4/90). |
| **AFR3220C** | ⚠ **The POC is a contract** — the credit jump from 1 (GMC years, AFR1101C/AFR2130C) to **3** marks the point where entering normally means **contracting**: commission plus an active duty service commitment, typically four years and substantially longer for rated fields. The first two years carry no obligation; this one does, and withdrawal consequences can include repayment or enlisted service. Load flag: a 3-credit line is realistically **8+ hours weekly** once Leadership Laboratory, physical training, and cadet wing duties are counted. Same **`C` vs separate-`L`** split seen in EVR/MET/ASL — UF carries AFR3220 plus AFR3220L. Florida angle: **Patrick SFB and Cape Canaveral SFS** make the Space Force pathway locally concrete, and Space Force accessions favor technical majors. Hours (75 = 45 class + 30 LLAB) are **derived**. |
| **ART2540C** | Rule-14 case with four titles: "Watercolor," "**Aqueous Painting**" (FSCJ, 3 cr, **2 lecture + 4 lab** — the source of the 90 contact hours), "Water Color I" (NWFSC, 3 cr), "Honors Watercolor" (FAU, **4 cr**). Materials flag that genuinely changes outcomes: **buy 100% cotton 140 lb paper** — cheap paper makes techniques fail that would otherwise work, so a beginner on bad paper concludes they cannot paint. Pedagogical note worth keeping across studio guides: the medium **cannot be corrected**, which forces planning, light-to-dark sequence, and decisiveness — a discipline that transfers to every other medium. Transfer flag: **B.F.A. admission requires a portfolio review regardless of transferred credits** — credits and portfolio are two separate gates. |
| **TPP2120C** | Another clean rule-14 case: "**Improvisation for the Actor**" = **3 credits** (UCF); "**Creative Improvisation**" = **2 credits** with 2 lecture + 1 lab (TCC). Core correction the guide leads with: **it is not about being funny**, and trying to be is the most common failure mode — comedy is a byproduct of commitment and truth. Nuance worth recording: **"yes, and" is agreement between the *actors* about the world, not between the characters** — characters can argue violently; students who conflate these produce scenes where everyone is pleasant and nothing happens. ⚠ Current-practice flag paralleling the TPP1111 entry: **consent and physical safety in improvisation** — right to decline contact, to edit a scene, and the same choreography expectations for improvised intimacy and violence as scripted. Florida market: Central Florida themed entertainment hires improvisers year-round with benefits. |

**Rule 15 (content divergence under a stable number).** Rule 14 covers a number whose *credit value* moves
with its title. Worse and rarer: a number whose **subject** moves. **CGS2820** is introductory web
design at Northwest Florida State (3 cr), site design and development at FSCJ (4 cr), and
**web programming in JavaScript/Ajax/ASP.NET** at Daytona State (3 cr) — the same SCNS number teaching
markup at one institution and server-side programming at another. SCNS equivalency cannot resolve this,
because the number genuinely matches. When a course's title is generic enough to cover several subjects
("Web Design," "Special Topics," "Applications"), **read the institution's own description and prerequisite
before recording credits or asserting what transfers**, and say so in the guide.
| **EEC2523**, **EEC2527** | ✅ **Credential-alignment finding worth carrying across the whole early childhood prefix.** Completing EEC2523 satisfies **one educational requirement for the Foundational Level Florida Child Care and Education Administrator (Director) Credential** and **one of three course requirements for the Advanced Level** — at institutions whose courses are approved for it. That is a real dollar saving versus separate DCF training, and it is **institution-specific**, so the guide tells students to ask before building a plan on it. Reinforces the CHD1220 flag: **college credit and DCF training are two parallel systems**, articulated in places (CDA, FCCPC) but not interchangeable. Management flags: **staff turnover is the central operational problem** (and continuity of caregiver is a child-outcome variable, not just an HR cost); **ratios are inspected and break during breaks, naps, and transitions**; the director's **§ 39.201 reporting duty is personal and non-delegable**. EEC2527 economics flag: personnel is ~2/3 of budget and margins are thin, so the wage lever that would fix turnover collides directly with what families can pay. ⚠ **Abuse and molestation coverage is frequently excluded or sublimited** on a standard policy — the exposure most likely to end a child care business, and the one operators least often check. |
| **DAA1104C**, **DAA1204C** | ⚠ **Would have been wrong by inference.** I would have taken 3 credits from the published DAA1500C (jazz) and DAA1520C (tap); Florida sources place **DAA1104 and DAA1204 at 2 credits**. Confirms and sharpens the studio-credit flag written in DAA1520C: technique credit runs **1–3 across Florida** and does not follow the subject. Pedagogical flags worth reusing across studio guides: **modern is the least codified major technique** (two "Modern 1" classes may be structurally different — teach principles, not exercises) and is often *more* accessible to beginners than ballet, while **ballet students must never force turnout from knees or feet** — the most common beginner injury mechanism, driven by an aesthetic that rewards the appearance of rotation. Transfer flag common to both: **B.F.A./B.A. admission requires an audition regardless of transferred credits** — credits and audition are separate gates. |
| **DEP2402** | The course exists to contradict what students believe, and the corrections are well-replicated: **emotional well-being generally improves with age** (socioemotional selectivity), **dementia is disease, not normal aging**, cognitive change is **uneven rather than uniform** (fluid declines, crystallized holds or improves), and **variability increases with age** so population averages describe almost no individual. ⚠ Flag with teeth: **internalized age stereotypes have measurable effects on memory, functional health, and survival** — so "what did you expect at your age" is a clinical error, not kindness. Florida is the **single best labor market in the country** for this content, and the guide names the actual service system (Elder Affairs, AAAs, ADRCs, Elder Helpline, Long-Term Care Ombudsman, AHCA facility search). ⚠ **§ 415.1034, F.S.** vulnerable-adult reporting is personal, and **financial exploitation** is a particular Florida exposure. |
| **CTS2370C** | Rule-14/15 territory again: **3 credits** at Seminole and EFSC, **4** at FSCJ (which adds a CTS1334C prerequisite), and EFSC retitles it "**Virtual Infrastructure — Planning and Design**," a different emphasis. ⚠ **Snapshots are not backups** — the most damaging misconception in virtualization administration; they grow, degrade performance, and a full datastore stops every VM on it. Concept that separates admin from operator: **overcommitment** works because workloads do not peak together, and the failure modes differ by resource (CPU → ready time; memory → ballooning then swapping; storage → thin-provisioned datastore fills), so the skill is diagnosing *which* resource is constrained. Career flags: **build a home lab** (nested virtualization or free Proxmox/XCP-ng/Hyper-V; RAM is the binding constraint), and note the **post-Broadcom VMware licensing shift** pushing some employers toward alternatives — argue for principles over one vendor's menus. |
| **EMS2666** | ✅ Completes the DSC paramedic sequence (12 + 12 + 1 + 11 + 2 + 4 = 42 credits, all catalog-verified except derived hours). ⚠ **1 credit, 96 derived hours**, and it runs *concurrently with the 12-credit EMS2604C* — the real weekly load is far above what the transcript shows. The specific value of a **hospital** rotation over a field one, worth keeping: in the ED you learn **what was actually wrong**, because the diagnosis arrives while you are still there. Best habit in the guide: **write your impression down before you know the answer, then find out** — being wrong is the point, and fifty repetitions calibrate judgment the field cannot. ⚠ Behavioral flag: **nobody hands you skills** — tell the charge nurse at shift start exactly what competencies you need, or reach the end of the program short. Failure mode specific to clinicals: requirements **expiring** mid-rotation, not failing to obtain them. |
| **FSS1240C** | Contact hours differ meaningfully in *balance*, not just total: Broward **56 (40 lecture + 16 lab)** versus another version at **64 (32 + 32)** — a very different classroom-to-kitchen ratio for the same course. NWFSC carries comparable content as **FSS2240L**, a different number *and* suffix. Organizing insight worth reusing: classical cuisine is a **generative system, not a recipe list** — five mother sauces yield dozens of derivatives, so learn ratios and technique, then derivations, then named dishes. ⚠ Practical-exam flag: students fail on **mise en place and organization**, not technique — sequence backward from plate-up, prep before firing, clean as you go. ⚠ Safety: dull knives cause cuts, **wet towels transmit heat instantly**, and a Florida kitchen in August with the line fired is a genuine heat-illness risk. Honest industry note: the distinction between **demanding and abusive** kitchen culture is real and students should know they can report the latter. |
| **MUT1122C** | ⚠ **Two-family case with a new wrinkle: the families have different credit totals per semester.** Florida runs first-year theory as the **integrated** MUT1121→1122→2126→2127 ("Music Theory and Musicianship," 3 cr each, written + aural in one course) and as the **split** MUT1111→1112→2116→2117 (3 cr) paired with MUT1241→1242→2246→2247 sight singing/ear training (1 cr). A semester is **3 credits integrated vs 3 + 1 = 4 split**. The clinching evidence they are parallel tracks: MUT1122's prerequisite reads "**MUT1121, or MUT1111 and MUT1241**" — an explicit bridge between architectures. ⚠ Second flag that outranks credits: **transfer into a music degree is by placement exam and audition, not transcript** — a student can transfer four semesters of theory and still be placed into second-semester theory. Aural skills are the harder half and cannot be crammed. |
| **MUM2600C** | Rule-14/15 again on a music number: **3 credits** as "Sound Recording I" (Gulf Coast) and "Basic Audio Recording Technique" (FSW, as MUM2600C), **2 credits** as "**Professional Digital Audio Workstation**" (SCF) — software-focused rather than microphone-focused. Also a genuine **prefix-boundary** observation worth recording: MUM (music business/technology) and DIG (digital media) teach overlapping audio content from different sides — MUM emphasizes capturing acoustic performance and working with musicians, DIG emphasizes sound for picture and design. Some programs require both; some treat them as alternatives. Craft flag: **microphone placement is the skill, everything else is adjustment** — moving a mic six inches changes more than any EQ, and it costs nothing. ⚠ **Phase problems** are the invisible failure — check mono, use the 3:1 rule; no plugin fixes it afterward. |
| **HIM1273C** | **Billing and coding are different jobs even when one person does both** — coding is clinical translation, billing is rules-and-process; small practices combine them, hospitals separate them completely, and the certifications diverge (CPC/CCA/CCS vs CPB). ⚠ Operational insight worth carrying: **most denials are front-end failures** — eligibility not verified, authorization not obtained, demographics wrong, filed late — very few are about the clinical care, and **timely filing deadlines are absolute** (a late claim is generally unpayable *and* cannot be billed to the patient). ⚠ Compliance: billing errors are **False Claims Act** territory, patterns that consistently favor the provider draw scrutiny regardless of intent, and "my supervisor told me to" is not a defense. Florida specifics: **Medicare dominance**, Medicaid managed care under AHCA, out-of-state snowbird plans, and a real **PIP (auto no-fault)** billing niche employers hire for. Credits are prefix-consistent, not individually catalog-verified. |
| **HSA4340** | ⚠ **Credentialing is the health-care-specific HR skill and getting it wrong is a compliance event** — primary source verification (from the issuing board, not the applicant's copy) plus **OIG LEIE exclusion checks**, because employing an excluded individual can make every associated claim improper. It is a **recurring** obligation, not a hiring-day task, and credentialing specialist is a career track in itself. ⚠ **Staffing is a patient safety issue**, not only a budget line — nurse staffing and skill mix are associated with mortality, failure to rescue, and infections, so the cost/quality tension is clinical. ⚠ **Burnout is an organizational problem** driven by workload, documentation burden, and lack of schedule control — resilience training and wellness apps do not address the cause and are resented. Evidence flag reusable in any HR guide: **structured interviews outperform the unstructured ones everyone prefers**. Florida law flags: at-will with the exceptions being where litigation lives, FCRA filing windows, Ch. 435 screening, and the **CHOICE Act (eff. 7/3/2025)** on non-competes — ties back to the MAN4402 correction from batch 24. |
| **HUS2500** | ⚠ **Boundary violations are the leading cause of discipline in the helping professions, and they are gradual** — they begin as defensible small crossings (session runs long, a ride home, a social media connection) and the pattern is the problem. Best professional test in the guide: **notice the exception you are making and ask why**, and treat the impulse to keep something from a supervisor as the warning sign. Refinement worth keeping: **dual relationships are unavoidable in small communities** — codes distinguish overlapping roles from exploitative ones, so the answer is anticipate-and-discuss, not pretend. ⚠ Florida confidentiality limits students underestimate: **§ 39.201** (children) and **§ 415.1034** (vulnerable adults) are **personal and non-delegable**; duty to warn; and **42 CFR Part 2** protects substance use records *more strictly than HIPAA*. Framing that makes the course tractable: **a dilemma is a conflict between goods, not a temptation** — most "dilemmas" students bring have a clear answer that merely requires courage. Florida's licensing boards publish disciplinary cases free — the most instructive reading available. |
| **GEO2420** | **Florida is one of the most interesting cultural geographies in the US** and the guide uses it throughout: Miami functioning as a Latin American/Caribbean city inside the US; a sharp internal cultural boundary (north Florida is culturally Deep South, south Florida is not); **toponymy recording layered Seminole, Spanish, and Anglo settlement**; and simultaneous domestic, international, seasonal, and post-storm migration. ⚠ Disciplinary-honesty flag: geography's history with **environmental determinism** means the course must teach describing *patterns* rather than asserting essential traits — attend to scale, internal variation, and correlation vs cause. Career flag that converts the subject into a job: **learn GIS** — QGIS is free, ArcGIS Online has a free tier, and Florida counties, water management districts, and emergency management all hire GIS staff. |
| **HFT3700** | ⚠ **The bed tax is how destination marketing actually gets funded, and it is statutorily restricted** — county Tourist Development Tax under **§ 125.0104, F.S.**, with permitted uses defined by statute (marketing, convention centers, certain sports facilities, beach renourishment). Two consequences: it explains why TDCs and DMOs exist at all, and their budgets **fall exactly when marketing is most needed**; and permitted-use fights (stadiums, convention centers) are recurring Florida politics a graduate should be able to read. ⚠ Analytical flag with wide transfer: **tourism economic impact numbers are routinely inflated** — optimistic multipliers, understated leakage, ignored displacement, omitted public costs; the professional question is "what multiplier, what leakage, compared to what?" Crisis unit is not theoretical here — **hurricane recovery marketing** must convey "open" without appearing callous, and statewide booking suppression follows national coverage even where no damage occurred. |
| **JOU1100** | ⚠ **One factual error fails the assignment** — misspelled name, wrong title, wrong number — regardless of writing quality, because that is how the profession works. The habits it builds (spell names back letter by letter, read quotes back, verify titles independently) are the actual curriculum. ⚠ **Florida's Sunshine Law and public records law are among the broadest in the country**, with access in the **state constitution (Art. I, § 24)**: presumption of openness, **no requirement to state a reason or identify yourself**, oral requests permitted, and open-meeting rules that reach two members of a board. The Florida First Amendment Foundation publishes free sample request language — students should file a real request during the course. ⚠ Libel is real for student journalists; note that **Florida defamation law has been under active legislative attention**, so rule 11 applies. Honest-industry flag: newsroom employment has contracted sharply, and the durable asset is the skill set (find, interview, verify, write fast), which transfers to PR, comms, government PIO, and law. |
| **MUT2126C**, **MUT2127C** | ✅ Completes the integrated theory sequence documented at MUT1122C — all four at 3 cr / 60 hrs, internally consistent with the split family's MUT2116C/2117C. Pedagogical flags worth reusing: **chromaticism is where theory starts explaining why music moves you** (the German augmented sixth, modal mixture, the Neapolitan are nameable devices with characteristic effects — listen while analyzing, don't just label); **form analysis is a different skill from harmonic analysis** and is worked top-down; and the twentieth-century material **requires a different kind of listening** — three semesters train the ear to hear function, and post-tonal music frequently has none. Practical flag classical-track students ignore: **do not skip the jazz/popular harmony unit** — most working musicians read chord symbols far more often than figured bass, and it is the same theory in different notation. |
| **OCB2000C** | ✅ **Fourth confirmed instance of the `C`-suffix lab trap**, now a reliable pattern: OCB2000C = **4 credits, 3 lecture + 3 lab** (FSCJ) and satisfies a laboratory science requirement; OCB2000 without the C = **3 credits, lecture-only** (FIU) and does not. Same shape as EVR2001, MET2010, and the PHY/BSC sequences. Florida-as-laboratory case is unusually strong: the **Florida Reef Tract** (only barrier reef in the continental US, and one of the most closely studied reef declines anywhere — stony coral tissue loss disease), seagrass loss tied directly to **manatee** mortality, red tide, mangroves, and a very large managed fishery. ⚠ Honest-career flag: marine biology is **competitive and graduate-degree gated**, and what distinguishes candidates is not passion but **quantitative skills (statistics, R/Python, GIS)**, early field experience, and scientific diving. |
| **PHT2220C** | ⚠ **Lab-format flag not previously recorded and worth carrying to every hands-on health program: students practice on each other.** That means clothing exposing the treated region, being touched by classmates and instructors, and touching others — so **consent and communication are graded skills**, injuries must be disclosed rather than worked through, and students with religious or personal concerns should raise them with the program early. Assessment flag: **skill check-offs are pass/fail with automatic-failure safety items** (failing to guard, failing to lock a wheelchair) — practice against the check-off sheet, not the memory of the demonstration, and say everything out loud because the verbal component is graded. Evidence flag: **therapeutic exercise has a substantially stronger evidence base than most passive modalities**, and patients prefer the modalities — so the PTA's real work is explaining why the exercise matters. Rule-14: FSCJ carries comparable content as **PHT2224C at 3 credits**. |
| **PHY3513** | Rule-14 with three titles on one number: "Heat and Thermodynamics," "**Thermal Physics**" (UF), "**Thermodynamics**" (FIU) — all 3 cr, all lecture-only. ⚠ **The difficulty is multivariable calculus, not new physics** — thermodynamics is largely partial-derivative manipulation, and both UF and FIU require **MAC2313**, often as a corequisite, with the catalogs noting it is used *extensively*. Guide tells students to review partial derivatives and exact vs inexact differentials **before the term starts**. Conceptual flag: **entropy is taught twice in different languages** (thermodynamic ratio, then microstate counting) and the course's real work is reconciling them — and **"entropy is disorder" is a misleading shorthand** worth avoiding. Career note worth keeping: statistical mechanics maps onto **machine learning** (Boltzmann distributions, softmax, max-entropy models) more directly than students expect, which is part of why physics graduates get recruited into data roles. |
| **OST2501C** | ⚠ **FLSA classification is where small offices get in trouble** — exempt status depends on *actual duties and salary level*, not job title, so calling someone an "office manager" and paying a salary does not make them exempt; plus **1099 misclassification** (common in Florida construction, landscaping, hospitality) and **off-the-clock work** being compensable whether or not authorized. Thresholds have been under repeated rulemaking — rule 11 applies. ⚠ **Records retention: keeping records too long is a real exposure**, not just clutter (discoverable, and breach risk), so a defensible schedule *with actual destruction* beats keeping everything — and if the office is a public agency or contractor for one, **Ch. 119, F.S.** applies. Role flag: the hard transition is **from doing the work to getting it done through others**, and the predictable failure is the promoted top performer who keeps producing, avoids confronting underperformance, and becomes the bottleneck. |
| **PLA2303** | ⚠ **UPL is the boundary that defines the career**, and criminal practice tempts violation constantly because frightened families ask direct legal questions ("should he take the plea?"). Florida specifics: the Supreme Court of Florida regulates UPL, **§ 454.23, F.S. makes it a criminal offense**, and Florida licenses no paralegals generally — the **Florida Registered Paralegal (FRP)** designation is voluntary and is not a license. ✅ **Genuine Florida distinctive most national texts miss: Florida permits discovery depositions in criminal cases**, which is unavailable federally and rare elsewhere — so Florida criminal discovery generates real volume, and deposition coordination and summarizing are core paralegal work here. ⚠ Deadlines are frequently **jurisdictional** (speedy trial day counts, appellate deadlines), making calendar management a malpractice-prevention function. Study method that works: read the **Florida Standard Jury Instructions** — they state the elements in the exact language a jury hears. |
| **QMB1001** | ⚠ **The advising flag with the most expensive consequence in this batch: QMB1001 is applied business math and generally does NOT satisfy a general education mathematics requirement** — MAC1105, MGF1106/1107, or STA2023 do. A student in an applied certificate or A.S. may need only this; one transferring to a business bachelor's still needs College Algebra and often statistics and MAC2233. **Equivalency does not make a course satisfy a requirement it was never designed for** — this is a distinct failure mode from the C-suffix lab trap and from rule 15's content divergence. ⚠ Content flag that costs real money in practice: **markup on cost ≠ margin on selling price** — intending a 40% margin but applying a 40% markup yields roughly 29% margin, invisible per item and substantial across a year. Florida arithmetic: **no state income tax withholding**, but reemployment tax is owed; **county discretionary sales surtaxes**; homestead exemption and Save Our Homes in property tax; percentage hurricane deductibles in insurance. |

**Rule 16 (a course can transfer and still not count).** Rules 14 and 15 concern the same number carrying
different credits or different content. A separate failure mode: the number transfers cleanly, the content is
what it claims, and the course still **does not satisfy the requirement the student needed**. Three confirmed
shapes so far — (a) the **`C`-suffix lab trap**: EVR2001, MET2010, OCB2000 and the PHY/BSC sequences all have
lecture-only and lecture-plus-lab forms, and only the `C`/`L` form satisfies a laboratory-science requirement;
(b) the **applied-vs-general-education trap**: **QMB1001** business math does not substitute for MAC1105,
MGF1106/1107, or STA2023, and **APA1111C** does not substitute for ACG2021; (c) the **level trap**:
FIN2000 ≠ FIN3403, SOP2002 ≠ SOP3004, a 2000-level tourism course ≠ HFT3700. Write the requirement question
into the guide, not just the transfer question: *what does this course count for, and for whom?*
| **RTE1824L**, **RTE2834L** | ✅ **Completes the DSC radiography clinical sequence, all five terms catalog-verified:** 1804L = 1 cr, 1814L = 2, and **1824L, 2834L, and 2844L all = 3**. Hours derived at the verified ~128 hrs/credit ratio give 128 → 256 → 384 → 384 → 384, i.e. roughly **8 → 16 → 24 clinical hrs/week, plateauing for the last three terms** — about 1,536 total clinical hours, consistent with JRCERT program norms. Curricular shape recorded: I–II high-volume basics; **III adds the axial skeleton, contrast studies, and fluoroscopy**; **IV is trauma, portables, and surgery** (DSC's stated emphasis). ⚠ New content flags: **contrast reactions** are the highest-acuity emergency a radiography student meets (screening questions, don't leave the patient, know where the crash cart is); **the OR has rules you must arrive knowing** (sterile field, C-arm draping, communicate in the surgeon's frame of reference); and **radiation protection matters most where controls are weakest** — portables and surgery put you and others in the room, so distance does most of the work. Trauma principle worth keeping: **move the equipment, not the patient**, which only works if positioning was learned as geometry rather than as body positions. |
| **RET1026C**, **RET2350** | First RET-prefix guides with a full credential map. ✅ **NBRC ladder recorded:** the **TMC** exam yields **CRT** at the lower cut score and eligibility for the **Clinical Simulation Exam** → **RRT** at the higher one — so the guide tells students to *aim for the higher cut score*, because many Florida hospitals hire only RRTs. **CoARC** accreditation gates exam eligibility; Florida licenses separately under **Ch. 468 Part V, F.S.** ⚠ RET1026C flags: **oxygen is a drug and more is not better** — hyperoxia is associated with worse outcomes in several conditions, and the COPD "hypoxic drive" teaching is oversimplified (V/Q mismatch and Haldane effect is the better account); titrate to target saturation. **Inhaler technique is where therapy silently fails** — watch the patient use the device rather than asking. ⚠ RET2350 flag with the highest stakes: **paralysis is not sedation** — neuromuscular blockers provide no sedation, analgesia, or amnesia, and inadequate sedation under paralysis is a recognized never-event the bedside therapist is positioned to catch. Note RET2350 has **no `C`** — lecture only, unusual in this prefix. |
| **SON1113C**, **SON2111C** | Conceptual flag worth carrying to every sectional-imaging guide: **you are not identifying organs, you are identifying relationships** — in a slice many structures look alike, and what identifies them is what lies next to them, which is why so much of a sonographic anatomy course is *vascular* anatomy even though the targets are not vessels. ⚠ **Orientation errors are the beginner's characteristic failure and they are documented** — a reversed probe produces a mirror image that can place pathology on the wrong side; confirm orientation by tapping the marker, and label plane, side, and structure on every image. Technique flag: learn **echogenicity as a hierarchy**, because reporting is comparative (liver vs right kidney) and gain changes absolute brightness while preserving relationships. ⚠ SON2111C professional-weight flag: **the sonographer decides what the physician sees** — unlike CT, a sonographic study contains only what was found and saved, so scan beyond protocol when something is abnormal. Also: know the **critical-findings policy** before you need it (large AAA, free fluid in trauma, ectopic, absent transplant flow). |
| **RED4844** | ✅ **Practicum-specific finding: Reading Endorsement Competency 5 is "demonstration of accomplishment," and a practicum is what satisfies it** — so the guide tells students to ask, in writing, whether their institution's practicum is approved toward it. That completes the endorsement picture started at RED3309C. Central skill flag: **"struggling reader" is not a diagnosis** — the breakdown is at phonological awareness, decoding, fluency, vocabulary/knowledge, or comprehension monitoring, and the interventions have almost nothing in common. The **Simple View of Reading** localizes it in about fifteen minutes: can they read the words, and do they understand the passage when it is read *to* them. ⚠ Assessment-fidelity flag unique to practicum: **the instinct to help is right as a teacher and wrong as an assessor** — prompting, repeating, or extending time destroys the data. Career note: **private structured-literacy tutoring is a real income stream** in Florida, partly funded through scholarship programs for students with unique abilities. |
| **RMI2110** | ⚠ **Florida's no-fault auto system is the flag with the most direct consequence for any Floridian.** PIP pays a portion of *your own* medical costs regardless of fault, historically capped at **$10,000** (lower without an emergency medical condition) — and **Florida does not require bodily injury liability coverage** the way most states do, so the driver who hits you may carry nothing for your injuries. Consequently **uninsured/underinsured motorist coverage matters more here than almost anywhere**, given one of the country's highest uninsured-driver rates — and it is optional and routinely declined to lower a premium. Repeal/reform has been attempted repeatedly; rule 11 applies. Reinforces the RMI2212 flags (**flood excluded**, **percentage hurricane deductibles**) from the personal side. Organizing principle worth reusing: **insure what you cannot absorb** — take higher deductibles on the payable, buy higher liability limits and an umbrella, and note that the most underinsured exposures for working people are **liability, disability, and life**. |
| **ART2754C** | ⚠⚠ **New failure mode, and the sharpest one yet: the queue title actively misidentifies the subject.** The queue carries ART2754C as "SCULPTURE 1." It is a **ceramics** course — "Ceramics II and Lab" at Daytona State (prereq ART2752C), "**Ceramics: Hand-Building**" at Broward (3 cr, **32 lecture + 64 lab = 96 hrs**), "Ceramics: Handbuilding I" at FAU. General sculpture is **ART2701C**, a different medium and a different course. Rules 14 and 15 cover titles that vary or content that drifts; this is a title that is simply *wrong for the subject*, and only the number is reliable. Guide published under the corrected title with the discrepancy flagged. ⚠ Safety flag: **silica dust causes silicosis** and the exposure is from *dry* clay — never sweep a ceramics studio dry, wet-mop or HEPA, and wear a fitted respirator for dry glaze materials. Failure flag worth keeping: five predictable causes (uneven walls, trapped air/solid mass, bad joints, fast drying, insufficiently dry greenware) account for nearly all lost work. |
| **ART1500C** | ✅ **Rule-16 level trap in its cleanest form: same title, same credits, different level.** ART1500C is "Painting I" at the **1000 level** with typically **no prerequisite**; ART2500C is "Painting I" at the **2000 level**, frequently requiring ART1300C and ART1201C. Both 3 credits, both 2 lecture + 4 studio. SCNS carries neither into the other. Also the finding that corrected ART2500C's hours (see the correction table). ⚠ Studio-safety flag reusable across painting guides: **solvent vapor** is the real hazard, and **oil-soaked rags can spontaneously combust** — a documented studio fire cause, not a myth. Craft flag: **"mud" is usually a value problem, not a color problem** — value collapse or overworking wet paint, diagnosable in seconds by squinting or converting a photo to grayscale. |
| **ASL2200C** | ✅ Completes the ASL numbering map and prompted the third revision of ASL2160C. Full shape: **ASL1140→ASL1150** and **ASL2140→ASL2150** converge at **ASL2160** (III), then **diverge again at IV** between **ASL2170** and **ASL2200**. Level-IV content flag worth keeping: the jump from III to IV is **discourse, not vocabulary** — sustaining extended narrative with consistent spatial referents, role shift, and register is categorically different from conversational exchange. ⚠ Professional-boundary flag restated at the level where students start volunteering: **fluency is not interpreting**, and offering to interpret in medical, legal, or mental health settings can cause real harm. Cultural flag: at this level Deaf culture means engaging with **contested questions** (cochlear implants, oralism's legacy, mainstreaming, audism) where a hearing student's role is to listen rather than adjudicate. |
| **ACG3113** | Rule-14 case in accounting: Florida carries Intermediate II as both **ACG3111** and **ACG3113**, and some institutions use ACG3103 for the first course rather than ACG3101. ⚠ **Currency flag with teeth: ASC 842 structurally changed lease accounting** — nearly all leases now sit on the balance sheet as a right-of-use asset and lease liability, where the old standard kept operating leases off entirely. An older edition or an old tutoring video teaches the wrong model, and "off-balance-sheet financing" is now discussed in the past tense. Study-method flag: **deferred taxes, pensions, and leases** are consistently named the hardest undergraduate accounting material, and each rewards a specific approach — separate book/tax columns, use the pension worksheet, and let classification drive the lease mechanics. |
| **AFR2131C** | ✅ **Completes the AFROTC obligation picture started at AFR3220C, from the other side.** The **GMC years (1 credit) carry no service obligation** and can be taken out of interest; the **POC (3 credits) normally means contracting**. So the sophomore year is the decision year — and more importantly the **selection** year: Field Training is the gate, and grades, fitness, and the AFOQT are **largely fixed by the time the board meets**, which a cadet learning this in the junior year has already lost the chance to act on. Load flag consistent with AFR3220C: a **1-credit line is realistically 5–7 hours weekly** once Leadership Laboratory, PT, and cadet wing duties are counted. |
| **BCA0356** | ✅ Extends the BCA apprenticeship framework to year four; 0 credits, **72 hours derived** (576 ÷ 8), consistent with BCA0350/0351/0353/0354. Fourth-year shape recorded: **integration and specialization** — multi-article code problems, VFDs and PLCs, fire alarm and Art. 517 health care, PV and storage, plus the professional layer (documentation, estimating, supervision). ⚠ Licensing-exam flag that is the point of the year: **Florida journeyworker exams are open-book and timed**, so they test *navigation speed and calculation fluency*, not memory — practice timed code-lookup drills with the same tabbed book you will bring, and confirm **which code edition** your jurisdiction uses, since studying the wrong one is a self-inflicted failure. Career flag: **controls and instrumentation is where the ceiling is**, and in Florida that means utilities, water treatment, ports, aerospace, **theme park ride and show control**, and data centers. |
| **STS1307C** | Rule-14: **3 credits** as "Surgical Equipment and Instrumentation," **4 credits** at FSCJ as "**Surgical Sciences and Instrumentation**" with a different lecture/lab/clinical split. Prefix ratio runs ~22–30 contact hrs/credit. Honest-method flag: instrument identification is **pure volume** with no shortcut — photograph-based flashcards daily, handle the real instruments in open lab, learn by *set* as well as individually, and learn the **naming logic** (eponyms and tip descriptors) so an unfamiliar instrument is still identifiable. ⚠ Two equipment-safety flags: **sharps injuries** are how OR staff get hurt (neutral zone, announce sharps, never reach blindly), and **electrosurgery burns** have predictable mechanisms — dispersive pad placement, active electrode left on drapes, and capacitive coupling in laparoscopic instruments, plus the OR **surgical fire triangle**. Career flag: **sterile processing is a job a student can hold now**, in the same department, and it builds instrument knowledge faster than any classroom. |
| **TPP2250** | ⚠ **Read the description before registering** — institutions teach this as a lecture survey, as a performance course for majors, or as a combination, and the difference determines whether you write papers or sing in front of the class. The absence of a `C` suffix usually signals the survey form. Analytical key worth reusing in any musical theatre guide: **ask why the character sings** — song happens when emotional pressure exceeds what speech can carry, which explains the "I want" song's early placement and the eleven o'clock number's late one. ⚠ **Minstrelsy is in the form's foundations** and honest courses say so — it shapes the music, the comic conventions, and casting practice well into the twentieth century, and it is why the current debates about casting, revision, and revival are a continuation rather than a novelty. Practical flag: **a film adaptation is a different work** — use filmed *stage* productions, widely available through college library databases. |

**Rule 17 (the title can be wrong, not merely variable).** Rule 14 covers a number whose credit value moves
with its title; rule 15 covers a number whose *subject* drifts between institutions. Worse than either: a
local or scraped title that **misidentifies the subject outright**. **ART2754C** entered the queue as
"Sculpture 1" and is a **ceramics hand-building** course — Florida catalogs title it "Ceramics II and Lab,"
"Ceramics: Hand-Building," and "Ceramics: Handbuilding I," while general sculpture is the separate
**ART2701C**. A student following the queue title would register for the wrong medium. Practical
consequence: **the SCNS number is the reliable identifier and the title is not**. When a queue title and the
number's catalog block disagree — here, a "sculpture" title sitting inside the ART275x *ceramics* block —
trust the number, verify against a real catalog, and publish under the corrected title with the discrepancy
flagged in the guide.
| **BCA0357** | ✅ Closes the electrical apprenticeship sequence (year 4, term 2); 0 credits, **72 hours derived**, consistent with BCA0350–0356. Content flag: the final term is **consolidation and transition** — comprehensive code review, calculations to exam standard, plus the professional layer (estimating, documentation, supervision) that the first seven terms never touch. ⚠ Exam flag restated where it matters most: **Florida journeyworker exams are open-book and timed**, so candidates fail on *navigation speed* and *calculation fluency*, not memory — both fixable, and this is the term to fix them. ⚠ Licensing-geography flag: **journeyworker is local, contractor is state** — county-issued journeyman cards may not be honored across jurisdictions, while DBPR **Certified** electrical contractor is statewide and **Registered** is not. Transition flag worth keeping: what changes at journeyworker is *accountability*, and the three habits are look it up, say when you don't know, and teach the apprentice. |
| **BCA0451, BCA0452, BCA0454, BCA0455** | ✅ **New trade in the BCA prefix: plumbing.** Four related-instruction terms (year 1 term 2 through year 3 term 2), 0 credits / **72 hours** each, same derivation as the electrical block (Florida plumbing apprenticeship: 4 years, 8,000+ OJT hours, min. 144 classroom hrs/yr). Sequence shape recorded: **materials and joining → DWV/supply sizing and code → commercial and specialized systems → diagnosis, service, and exam prep**. ⚠ Public-health framing flag: the code exists because **cholera and typhoid** did — traps, vents, and backflow prevention each have a specific historical reason, and an apprentice who knows the *why* installs correctly in situations the code doesn't cover. ⚠ Highest-stakes technical flag: **cross-connection control** — hazard assessment drives device selection, a device chosen for the wrong hazard level is not protection, and the **air gap** is the most reliable which is why the code specifies it wherever practical. Conceptual flag: **venting has a single purpose — keep the trap seal intact** — and every distance limit and wet-vent rule follows from it; students who memorize configurations can't reason through unusual arrangements, which is most of real work. ⚠ Biological-hazard flag distinct from other trades: **sewage pathogen exposure**, plus trench collapse and confined-space atmospheres. Florida flags: **hard carbonate-aquifer water**, **slab-on-grade** rough-in (errors are expensive to fix), and a very large **septic/onsite system** population now regulated through DEP. Career flag: **medical gas (ASSE 6010)** and **backflow testing** are certifications that raise the earning ceiling; **service work is a different job from installation** — diagnosis, not following a print. |
| **BCN2560** | ✅ Fills a real gap in construction management: **trade literacy without trade competence**. What the role needs is vocabulary, sequence, scope boundaries, quality recognition, and duration/manpower feel — so study each trade's *interfaces*, not its techniques. ⚠ Money flag: **MEP coordination is where projects lose money**, because mechanical, electrical, plumbing, and fire protection drawings are produced independently and therefore conflict; discovering it after ductwork is hung means change orders. Prevention is clash detection *before* installation, with a rough priority convention (gravity systems win, conduit yields) — the point being to decide in advance rather than in the ceiling. ⚠ Florida-specific flags a national textbook won't carry: **Florida Product Approval / Miami-Dade NOA** (many roofing, glazing, and exterior products need an approval number, and Miami-Dade/Broward form the **High-Velocity Hurricane Zone** with its own protocols), **threshold buildings and special inspectors**, and **hot-humid building science** where the vapor drive is *inward* most of the year — which inverts national vapor-retarder assumptions. Sequencing flag: some errors cost time, others cost demolition — for every scope ask what must finish before it and what it blocks. |
| **CAI4002** | Rule-14 title variant: "Introduction to Artificial Intelligence" and "**Foundations of AI**" (FGCU) under the same number. ⚠ **Prerequisites are real** — COP3530 + STA2023 at FGCU; this is a CS course assuming programming fluency and probability, and the most common preparation gap is **conditional probability / Bayes' rule**. Framing flag: the course spans **two eras** — symbolic AI (search, logic, CSP) and statistical/learned methods — and students wrongly write off the first half, though A* runs in every navigation app. ⚠ **Evaluation is where beginners fool themselves**, and the failure modes are specific: training on the test set (including indirectly, via hyperparameter tuning — hence the validation split), **data leakage**, **accuracy on imbalanced data** (99% by predicting the majority class), and **distribution shift**. The real skill is explaining *why the reported number is trustworthy*. ⚠ Ethics-as-technical-content flag: bias enters through **data collection, labeling, feature selection, and objective choice** — not just intent; **fairness has multiple formal definitions that are mathematically incompatible**, so "make it fair" is not a specification; dropping a protected attribute doesn't remove its influence because correlated features proxy for it; and **evaluation must be disaggregated by subgroup**. Career flags: tutorial-reproduction portfolios signal nothing (everyone has them) and you must be able to **defend your own design choices**; and the underrated market is **data engineering and ML ops**, not modeling. |
| **CCJ2650** | ⚠ **Currency flag with lives attached: fentanyl changed the risk calculus** — potency by weight means a user frequently doesn't know what they're taking, and dose variability within one batch can be lethal. Two operational points: **naloxone** is available in Florida under a standing order and is carried by many agencies, and the widely repeated claim that **incidental skin contact causes responder overdose is not supported by toxicological evidence** — medical and toxicology bodies have addressed it directly, and panic responses have *delayed care to actual overdose victims*. A course teaching current evidence over received wisdom does real good here. ⚠ Florida-law flag that surprises students: under **Ch. 893 F.S.**, "trafficking" is defined by **weight, not by evidence of sale** — threshold quantities carry **mandatory minimums**, the weight generally includes the whole mixture, and some thresholds are reachable by personal-use quantities. Cannabis/hemp status is **repeatedly revised**; verify current statute rather than any textbook edition. Intellectual-discipline flag worth reusing: separate **what the substance does** (empirical), **what the law says** (factual), and **what we should do** (contested) — scheduling reflects legal-political judgment, not a danger ranking, which is why alcohol and tobacco sit outside the schedules entirely. Evidence flag: treatment beats incarceration on cost-effectiveness, **MAT substantially reduces overdose death and is still underused and stigmatized**, drug courts and naloxone distribution show positive outcomes — while mandatory-minimum deterrence and supply-side interdiction remain genuinely contested. |

**Rule 18 (a suffix can mean something different inside one prefix — and one prefix can hold several
trades).** Across this repository the **L** suffix denotes a scheduled classroom laboratory section. Inside
the **BCA** (Building Construction Apprenticeship) prefix it does not: **BCA0350L** is "Electrical Apprentice
1 **Lab-OJT** (Non-Union)," and the L companion records the **paid on-the-job hours** an apprentice works for
their employer. An apprentice is normally enrolled in *both* the related-instruction number and its L
companion each term, and the L companion is what documents the hours the credential rests on. The same
prefix also holds **more than one trade and more than one sponsorship track**: BCA033x/034x is the
*Electrical Academy Union Apprentice* block, BCA035x the non-union electrical block, and BCA043x/045x is
**plumbing**. Practical consequence, and the reason this rule exists: an inference drawn from one course in a
prefix **must not be generalized to the prefix** — doing exactly that put a fabricated "BCA0358 co-op
block" into five published guides. Before writing about a number family, **list the prefix's actual number
range from the queue** and read the titles; the structure is frequently visible there and costs one query.
| **CGS2821C** | ⚠⚠ **The strongest rule-15 case in the repository, and it revealed why the divergence happens.** One number, three real courses: **"Advanced Web Programming (XML, ASP.NET, SQL Server)"** at Daytona State (3 cr, server-side programming), **"Advanced Web Site Design and Development"** at FSCJ (**4 cr**, design/production), and a **multimedia systems** variant elsewhere. Credit value differs too, so a 3-credit version cannot fill a 4-credit requirement. **The new insight:** neighboring **CGS2820C** diverges *identically at the same institutions* — Daytona programming, FSCJ design, NWFSC intro design. So the divergence tracks **the program the number block sits in**, not the individual course: a web sequence housed in a programming department teaches both numbers as programming; one in a digital media program teaches both as design. Practical payoff — identify how your institution treats *one* number in a block and you can predict its neighbors, and expect the receiving institution to have made the opposite choice. |
| **CIS4360** | ⚠ **The prerequisites identify the course far better than the title does.** UF: "Computer and Information Security," prereq **CDA3101** (computer organization). UNF: "Introduction to Computer Security," prereq **COP3503**. Daytona State: "**Applied Cybersecurity**," prereqs **(CTS2321 or CTS3348) and (CET1600 or CNT3104)** — Linux admin *plus* networking. Same number, two genuinely different courses: the CS variant reasons about memory, protocols, and crypto constructions; the IT variant configures, hardens, and monitors real systems. The two backgrounds are **not interchangeable**. ⚠ Legal flag stated plainly: unauthorized testing is a crime under the federal CFAA **and Ch. 815 F.S.**, and "I was practicing for class" is not a defense — employer and college networks included. Use sanctioned environments (TryHackMe, HTB, OverTheWire) or your own isolated lab, always. ⚠ Reality flag: **most breaches are not clever** — phishing, unpatched known vulnerabilities, misconfiguration, and excessive privilege dominate, which is why the highest-value defensive work is unglamorous. Career honesty: **security is a specialization, not an entry point** — you cannot secure what you don't understand, so the realistic path runs through help desk, sysadmin, or development first. |
| **COP4813** | ⚠ Prerequisite *and platform* vary sharply — Java/Spring (FSU COP3252), OOP (Seminole COP2805/3330), COP3503+COP3855 (UNF), CGS4854 (FIU). Concepts are identical; the term's work is not interchangeable, so confirm the stack before it starts. ⚠ The one habit to internalize: **never build a query by concatenating strings** — parameterized queries prevent SQL injection completely, and the generalization is *validate input, encode output, never trust the client* (client-side validation is a UX convenience, not a security control). ⚠ Secrets flag: a credential pushed to a public repo is compromised **within minutes** because bots scan for exactly that — `.gitignore` before the first commit, not after. And passwords need bcrypt/scrypt/Argon2, never plain SHA-256, which is far too fast to resist offline cracking. Conceptual key: **statelessness** is what the whole course rests on — cookies, sessions, tokens, and CSRF all exist to reconstruct continuity over a protocol that has none. |
| **CTS2302C** | ⚠ Diagnostic heuristic worth keeping for any Windows guide: **when Active Directory breaks, check DNS first** — AD depends on DNS totally (domain controllers publish SRV records; clients locate, authenticate, and apply policy by lookup), and DNS failures surface as logon, replication, GPO, and trust errors that never announce themselves as DNS. ⚠ Security flag: **AD is the highest-value target in the organization** — compromising it compromises everything, which is why ransomware operations aim at it directly; the defenses that matter most are administrative (separate admin accounts from daily-use, near-empty Domain Admins, delegation over broad privilege, MFA, tested offline backups). Learning flag: this material is **nearly impossible to learn from reading** — Windows Server evaluation editions are free for 180 days, so build a 4-VM lab and deliberately break things. ⚠ Naming-churn flag: Microsoft renamed Azure AD to **Entra ID** and moved the certification path into the Azure/M365 tracks, so search current product names or you miss the live documentation — and neighboring **CTS2358C "Identity with Windows Server"** covers overlapping ground under the newer terminology. |
| **CGS1570** | ✅ Rule-16 level trap: **CGS1570 and CGS2100C are both "Computer Applications"** at different levels, with CGS1060C, CGS1100C, and CGS1002 as further overlapping variants — and several Florida university business programs name **CGS2100C specifically**. Also a useful **negative** finding: the numeric cross-check flagged CGS2100C at 45 hours against a family at 60, but verification **cleared it** — Valencia lists CGS1060C and CGS2100C as **2 lecture + 1 lab** (45 hrs). So within CGS the **C suffix does not imply a fixed contact-hour ratio**, and 45 or 60 are both legitimate for 3 credits. Career flag worth keeping: **spreadsheet skill is the part with real labor-market value**, and most professional spreadsheet disasters trace to **data structure** (one row per record, no merged cells, no formatting carrying meaning) rather than to formulas. |
| **DAA1000** | ⚠ **Registration trap, and my initial hypothesis was wrong.** The absent C suffix suggested a lecture survey; it is not — SCF describes a participatory overview of jazz, tap, ballet, modern/lyrical and ballroom, and UF titles the number **"Fundamentals of Dance Technique."** **DAA = Dance *Activities*** and these are studio courses; the academic version lives under the **DAN** prefix. **The C suffix is applied inconsistently across DAA and signals nothing here** — DAA2105 and DAA2205 are studio courses with no C. ⚠ Fragmentation flag: jazz alone runs as **DAA1500C / DAA1504C / DAA2501C / DAA2505** — two parallel numbering families for one progression, mirrored in modern (DAA1104C/DAA2105) and ballet (DAA1204C/DAA2205), with credit values of 2 *or* 3 at the same 60 contact hours. Rivals ASL for most fragmented family. Injury flag: dance injuries are overwhelmingly **overuse**, and **forcing turnout from the knees and feet instead of the hips** is the classic beginner cause of knee and ankle injury. Skill flag: **counting music** is what separates students who progress from those who stall — learn the counts before polishing the movement. Florida career flag: theme parks and the cruise industry hire multi-style dancers continuously and audition year-round. |
| **DEA0801C** | ⚠ **Rule-17 title error plus an enormous hour divergence under one number.** Queue title "Clinical Practice II"; **Daytona State lists DEA0801C as "Chairside Assisting II and Lab" at 105 clock hours**, while **Gulf Coast splits it into DEA0801 (≈58 lecture hrs) + DEA0801L (≈198 lab hrs) ≈ 256 hours** under the matching "Clinical Practice II" title. Same number, different title, and a **2.4× difference in delivered hours** — so programs **cannot be compared course by course**; compare total program and total clinical hours, and confirm CODA accreditation. (Gulf Coast also titles DEA0850L "Clinical Practice III" where the queue says "Externship I" — the divergence runs through the whole prefix.) Skill flag: the course really teaches **anticipation** — having the next instrument already in position — so learn procedures as *sequences*, not instrument lists. ⚠ Materials flag distinctive to chairside: **working and setting times do not wait**, and are affected by heat and humidity, which is a genuine Florida operatory consideration. |
| **DES0205C** | ⚠ **The single highest-value course in a Florida dental assisting certificate**, because Florida law bars an assistant from exposing radiographs without board-approved training — Florida does not license dental assistants generally, but *this* is a hard credential gate. ⚠ Hours diverge again: **90 clock hours at Daytona State** ("Dental Radiology and Lab") versus **30 + 90 = 120 split across DES0205 and DES0205L at NWFSC** (two registrations). Useful **contrast to Rule 18**: here the **L suffix carries its ordinary meaning** — a genuine supervised laboratory — unlike the BCA prefix where L records paid OJT. The L's meaning is prefix-dependent and must be checked. Ethics flag: **every exposure must be justified and optimized (ALARA)**, which makes **retakes a patient-safety issue** rather than a matter of pride — the best dose reduction available is getting it right the first time — and the assistant is often the last person positioned to catch a wrong prescription or possible pregnancy. Digital-era flag: enhancement software may adjust display, but **altering a diagnostic image is falsification of a legal record**. Panoramic flag: every positioning error has a **signature artifact** (too far forward → narrow blurred anteriors; chin too high → flattened occlusal plane; tongue off palate → dark shadow over maxillary apices), so read the artifact backwards to the cause. |

**Rule 19 (divergence is a property of the block, not the course — and the prerequisites name the
variant).** Rule 15 established that one SCNS number can carry different content at different institutions.
Batch 46 found the mechanism. **CGS2821C** is server-side programming at Daytona State, web *design* at FSCJ
(and 4 credits there rather than 3), and multimedia elsewhere — and its neighbor **CGS2820C** splits the
same way at the same institutions. The divergence therefore follows **the program the number block sits
in**: a web sequence housed in a programming department teaches the whole block as programming; one housed in
digital media teaches it as design. Two practical consequences. First, **identifying how an institution
treats one number in a block predicts its neighbors**, which is cheaper than researching each course. Second,
when the title is ambiguous, **the prerequisites identify the variant more reliably than the title does**:
**CIS4360** is a computer-science course where the prerequisite is CDA3101 or COP3503, and an information-
technology course where it is Linux administration plus networking (Daytona State) — same number, same
nominal subject, incompatible entry assumptions. Read the prerequisite chain before the description.
| **GRA2144C** | ⚠⚠ **Rule 19 confirmed from the other side, and it produced a reusable navigation key.** Web design is scattered across Florida prefixes according to **which department houses it**, and the prefix predicts the approach: **GRA** = graphic-arts, design-first (this course, plus GRA2134C interactive design); **CGS** = varies wildly by institution (CGS2820C/2821C — intro design, site design, or ASP.NET server-side programming); **COP** = programming (COP4813, COP4834); **CTS** = certification-oriented (CTS1851C CIW); **DIG** = interactive/multimedia. Same subject, genuinely different courses, and none substitute automatically. This is the cleanest practical payoff yet from the block-divergence mechanism. Method flag worth reusing in design guides: **design first, code second** — sketch on paper, then wireframe (which forces you to solve hierarchy before style can disguise that you haven't), then visual design, then build. ⚠ Accessibility flag with a designer-specific list: contrast ratios (light grey on white routinely fails), **never color alone** to convey information, and **visible focus indicators** — which designers frequently remove for looking unattractive. |
| **EDF4603** | ⚠ **Same content, different prefix AND different level** — EDF4603 at most institutions (UCF titles it "Analysis and Application of Ethical, Legal, and Safety Issues in Schools"), but **EDG3410** "Classroom Management, School Safety, Law, and Ethics" at Northwest Florida State: a **3000-level** course under the general-methods prefix rather than educational foundations. Does not substitute automatically. ⚠ Career-ending flag: read **State Board Rule 6A-10.081** (Florida's Principles of Professional Conduct) as actual text, then read FDOE's published **disciplinary actions** — the real pattern is **boundary violations (very often beginning with private electronic communication), testing irregularities, failure to report, and leaving students unsupervised**. Almost none involve instructional incompetence. ⚠ Mandatory-reporting flag with teeth: in Florida the duty is **personal** and is generally **not discharged by telling a principal**; the standard is reasonable suspicion, not proof; failure to report can carry criminal penalties. ⚠ IEPs bind **general education teachers too** — "I didn't know they had an IEP" is not a defense. Research flag: **management is prevention, not response**, established in the first two weeks, and a large share of apparent behavior problems are **instruction problems**. Disproportionality flag handled directly: disparities concentrate in **subjective categories** like "defiance" and "disrespect," so the actionable self-check is examining your own referral data by student group. |
| **EEX4265** | ⚠ **Accommodation vs modification is the distinction with diploma consequences** — accommodations change how a student accesses content, modifications change what is measured, and in Florida that can determine which diploma is earned, which in turn gates college admission and some employment and military pathways. Decisions made in sixth grade quietly foreclose options by eleventh, so the professional duty is explaining the trade-off *early*. ⚠ **The cliff flag families are blindsided by: entitlement ends at graduation.** IDEA services stop; adult services are eligibility-based, waitlisted, and must be applied for (Florida APD has had substantial waits). Postsecondary institutions run on **504/ADA, not IDEA** — the student must self-identify, document, and request; IEPs do not transfer and nobody approaches them. Highest-leverage instruction: **teach self-advocacy explicitly via student-led IEPs**, because after graduation no adult is assigned to identify their needs. Transition-research flag: **paid work experience during high school** is among the strongest predictors of post-school employment. Adolescent flag: supports that stigmatize go unused — students often prefer to fail rather than look different — so prefer **invisible or universal** accommodations and let the student choose. Co-teaching flag: it degrades into aide-work for **structural** reasons (no common planning time, too many content areas), so name them early. Numbering: **EEX1600 and EEX4601 are both "Behavior Management"** at 1000 and 4000 level, and intro ESE exists at three levels (EEX2010/2080/4034). |
| **EMS2667** | ✅ Completes the paramedic clinical sequence and triggered the EMS2666 correction. ⚠ **The OR is the highest-value rotation in the entire program** — the only setting where you manage airways on fasted, pre-oxygenated, fully monitored patients under direct anesthesia supervision *with time to be corrected*; every career intubation afterward is worse conditions. So ask for critique of **technique**, not just whether the tube went in, and practice **BVM ventilation** deliberately, since it saves more lives than intubation and is more often done badly. ⚠ Administrative flag that actually fails students: CoAEMSP accreditation requires documented **minimum patient contacts by category**, so students finish their hours and discover they are short on **pediatric or obstetric contacts** — enter contacts the same day and audit running totals against the requirement every few weeks. ⚠ Mental-health flag: EMS has documented elevated PTSD, depression, and suicide rates, and the culture historically discouraged discussing it — identify *who you will talk to* before you need them. Numbering: the clinical sequence is inconsistently numbered (FSCJ EMS2666/2667, SPC EMS2665), but it matters less than usual because **paramedic programs are not assemblable from courses at different institutions** — accreditation, medical direction, and skill tracking are all program-level. |
| **HFT4253** | ⚠ **Structural fact students conflate constantly: ownership, brand, and operator are three different parties.** A Hilton-branded hotel is very often not owned *or* operated by Hilton. This explains who your actual employer is when you take a hotel job (frequently a management company whose name is not on the building), why a GM is caught between an owner preserving capital and a brand demanding renovation, and why properties leave a flag — modern branded lodging is closer to real estate with a licensing layer than to hospitality that happens to own buildings. ⚠ Metric flag: **RevPAR is the industry's language** because occupancy alone can be bought by cutting rate and ADR alone by leaving rooms empty — 95% occupancy almost certainly means underpricing. Add **GOPPAR** (cost of the business you took) and the **index measures**, since performance is judged relative to a competitive set. ⚠ Profit flag: **distribution cost is where hotel profit quietly goes** — two identical room nights at the same rate can differ materially in profitability by channel, which is why a hotel can **raise RevPAR while lowering profit**. Career flag: hospitality is **promote-from-operations**, so a degree without hotel work places you below a non-graduate with three years at the desk. Florida flags: severe *regional* seasonality (South Florida winter, Panhandle summer, Orlando school/convention calendars), **hurricane business continuity** as a real competency, and short-term rentals as a structural competitor. |
| **EAP1600** | ✅ **Validated the EAP numbering grid published in batch 37** — the grid predicted Speech/Listening Level 6 at EAP1600, 3 credits, and the queue title and catalogs match exactly. Also confirms the grid's C-suffix note: EAP1500**C** carries an integrated lab (60 hrs) while EAP1600 does not (45 hrs), at the same 3 credits. ⚠ Bridge flag that defines the level: earlier EAP uses **graded input** — instructors slow down, repeat, simplify — and a mainstream lecture does none of it, which is why this course prioritizes **note-taking while listening**, a dual task that is hard even in a first language. Practice with authentic lectures at **full speed**, using transcripts to check rather than to follow. ⚠ Pronunciation flag that contradicts student instinct: **stress and rhythm matter far more than individual sounds** for intelligibility — a noticeable accent with accurate stress is easily understood, accurate sounds with wrong stress are not — so learn the stress pattern with every new word. And the goal is intelligibility, **not accent elimination**. Advising flag: institutions **cap** how much EAP counts toward a degree (FSCJ: 6 credits), so ask about the cap, financial aid interaction, and the exit requirement early. |
| **DES1010** | ✅ Verified at **2 credits / 2 lecture hours** — notable as a **negative** result immediately after the DES1100C/DES1200C correction: having just found two DES guides wrong at 2 credits, the temptation was to assume 3 here. Verification said 2. The lesson is that a corrected assumption is not a new rule. ⚠ Workload flag: widely considered the **hardest course of the first year**, and the difficulty is **volume, not concept** — 2 credits of head and neck anatomy demands more study time than 3 credits of most lecture courses. Study-method flag: reading produces **recognition**, examinations demand **recall**, so print blank diagrams and label from memory, trace nerve pathways aloud, and physically handle the skull. ⚠ Emergency flag that deserves more attention than it usually gets: odontogenic infections travel along **fascial planes**, and **Ludwig's angina** can obstruct the airway — recognizable warning signs are difficulty swallowing or breathing, tongue elevation, trismus, rapidly spreading facial swelling, and periorbital swelling. Payoff flag: learning the **trigeminal nerve** properly is what makes local anesthesia comprehensible rather than memorized injection sites, including why injections *fail* (accessory and cross-innervation, anatomical variation). |
| **FRE2221C** | ✅ Completes the four-course French sequence at **4 credits**, consistent with FRE1120C/1121C/2220C. ⚠ Numbering divergence: **FIU and FSCJ use FRE2200** for Intermediate French I where others use FRE2220, and **FAMU lists FRE2221 in a 3-credit configuration** against the more common 4 — which matters because a 3-credit course does not fill a 4-credit B.A. language requirement. Grammar flag: the **subjunctive** is the hurdle, and the useful reframing is that it is not about factual uncertainty but the **speaker's relationship to the clause** (*je pense qu'il vient* vs *je ne pense pas qu'il vienne*) — learn the categories, not a list of a hundred triggers. Transition flag: this is the term to **stop translating** — switch to a French-French dictionary, read for gist first, learn collocations rather than single words. Honest diagnosis: four semesters produce students who read adequately and **freeze when speaking**, because comprehension is practiced constantly and production for minutes per class. Florida flag: French is more practical here than students expect — large Quebecois and French tourist inflows, plus a substantial Haitian community (French is not Haitian Creole, but is a real head start toward it). |

**Rule 20 (the prefix is a department, so the prefix predicts the pedagogy).** The natural extension of rule
19, and the most directly useful navigation rule so far. Where a subject is taught by more than one
department, Florida gives each department's version its **own prefix**, and the prefix reliably predicts the
approach even when the titles are identical. Web design is the clearest case: **GRA** (graphic arts) teaches
it design-first with code as production; **COP** (computer programming) teaches it as application
development; **CTS** teaches it toward vendor certification; **DIG** teaches it as interactive media; and
**CGS** varies by institution because that prefix is itself a general-studies catch-all. The same shape
recurs across the repository: **EDF4603** and **EDG3410** carry one body of content under educational
*foundations* and general *methods* prefixes at different levels; **DAA** is dance *activities* (studio) while
**DAN** is dance *academics* (lecture); **DES/DEA 0xxx** is PSAV clock-hour instruction while **DES 1xxx** is
college credit. Practical use: when a student asks which course to take, **read the prefix as a statement
about the teaching department**, and check whether the receiving program wants that department's version
— because **SCNS equivalency applies to the same number at the same level, never across numbers**, and
these never substitute automatically.
| **PMT0121C, PMT0134C** | ⚠⚠ **The most fragmented prefix found yet — worse than BCA.** PMT holds **two trades**: welding (PMT001x–017x) and **precision machining** (PMT020x–072x — manual machining, CNC mill and lathe, EDM, CAD/CAM). And welding alone is numbered in **three parallel families** describing the same PSAV program at different granularities: **PMT007x** occupational/OCP titles in ~150-hour blocks ("Welder – Assistant 1," "Welder – SMAW 1," "Welder"), **PMT010x–017x** finer process-named courses of 50–90 hours ("SMAW Principles," "GTAW Principles," "GMAW," "Pipe Welding"), and a **PMT001x** block elsewhere ("Welder, Shielded Metal Arc"). ✅ **Important negative result:** the six published PMT007x guides at 150 hours each looked wrong against the 50–75 hour values verified here — but 7 × 150 = **1050 hours, exactly the full PSAV program**, so they are the OCP-block granularity and are correct. *Different granularity is not an error.* ⚠ Title flag: **PMT0121C is "Introductory SMAW" at NWFSC and "Welding 8" at Seminole State** — a process name at one institution, a sequence number at another. Practical rule: **compare welding programs by total clock hours, never course by course.** ⚠ Technical flag worth keeping: **GMAW is easy to learn and easy to do badly** — in short-circuit transfer a beginner can lay a beautiful bead that has barely fused (**cold lap**), invisible from outside and structurally worthless; stick welding is safer for beginners precisely because a bad weld usually *looks* bad. Cut and etch practice coupons. ⚠ **E7018 is hygroscopic** — absorbed moisture becomes hydrogen and causes *delayed* cracking hours after a weld passes visual inspection, which is why rod ovens exist and why the rules are enforced hard in humid Florida. Certification flag: it is **per-process, per-position, per-material, and it lapses** — certify in the hard positions (vertical, overhead, **6G** pipe) because they cover the easy ones. |
| **MAN4597 / MAN3593** | ⚠ **Incoterms are the highest-value practical content**: they define who arranges transport, who pays what, and — critically — **at what precise point risk of loss transfers**, and cost transfer and risk transfer are *not always the same point*. Under FOB, damage after loading is the buyer's problem even though the seller arranged the loading. They are also **periodically revised** (Incoterms 2020), so contracts must name the version. ⚠ Sourcing flag: **the cheapest unit price is regularly the most expensive decision** — total landed cost adds freight, duties, brokerage, and then the costs that usually dominate: pipeline and safety stock from long lead times, quality failure, minimum order quantities, and the **cost of inflexibility** when demand changes and your inventory is on a ship. This, not sentiment, is the honest explanation for **nearshoring** — and that trade flows through Florida's ports. ⚠ Compliance flag: the **importer of record** is responsible for classification, valuation, and country of origin, and "our broker handled it" is not a defense — the legal standard is *reasonable care*. Forced-labor enforcement has expanded into a documentation requirement. Logistics flags: **total cost** thinking (optimizing any single component reliably makes the system worse), and **safety stock is about variability, not average demand** — with **lead time variability usually the bigger driver**, which is why a cheaper supplier with erratic transit can cost more than it saves. Florida flag: the state is a **primary U.S. gateway to Latin America and the Caribbean**, and Spanish or Portuguese is a stated hiring requirement in Miami's forwarding and brokerage community. |
| **PHY3221** | ⚠ **This is the course where physics changes character**, and students who did well by pattern-matching to worked examples often struggle here for the first time. Introductory problems arrive pre-formulated; here you must *construct* the problem — choose coordinates, identify constraints, write the equations of motion, then solve differential equations. The adjustment is real and is not a signal of unsuitability. ⚠ Prerequisite flag that is genuinely load-bearing: **the subject IS differential equations applied to physical systems** — take MAP2302 *before* rather than as a corequisite if at all possible, and be comfortable with complex exponentials, since physicists work in e^(iωt) and convert to sines and cosines only at the end. ⚠ Transfer trap: the **algebra-based sequence (PHY2053C/2054C) does not prepare you for this course** — a student who took it for a health-science requirement and later switched to physics must repeat the calculus-based sequence. Payoff flag: **Lagrangian mechanics is why the course exists** — constraint forces simply disappear, and the formulation generalizes to fields, relativity, and quantum mechanics; do not let it get rushed into the last two weeks. Professional-habit flag: check **dimensions, limiting cases, signs, and magnitudes** before accepting any result. |
| **PHY4424** | ✅ **The most directly employable course in the physics major**, and worth saying plainly because students pick electives on interest and are then surprised by the job market: most upper-division physics prepares you for graduate school, **optics prepares you for a job** — photonics hires at bachelor's and master's level across telecom, semiconductors, medical devices, and defense. Florida-specific advantage: **CREOL at UCF** is one of the country's leading optics institutions, with an Orlando industry base plus Space Coast optical payloads. Take the lab (hands-on alignment is valued and scarce), learn a ray-tracing package, join SPIE/Optica. ⚠ Conceptual key: **coherence** unlocks the middle of the course — it explains why Young's experiment needs the first slit, why soap films show colors and window panes don't, and why a Michelson loses fringes as an arm moves (which is how coherence length is measured, and how OCT images tissue). ⚠ **The diffraction limit is physics, not engineering** — λ/D cannot be manufactured away, which is why telescopes are large, why light microscopy hit a wall that drove electron and super-resolution methods, and why lithography chased shorter wavelengths. The transferable lesson: **distinguish limits imposed by physics from limits imposed by engineering.** |
| **MUM2601C** | ⚠ Registration flag specific to this prefix: **both MUM2600C/2601C (integrated) and MUM2600L/2601L (separate lab) exist**, so the same material means **one enrollment or two** depending on institution — the same shape as DES0205C vs DES0205+DES0205L. Verified at **3 credits, 36 lecture + 36 lab = 72 hours** (titled "Advanced Recording Engineering" at some institutions). ⚠ Craft flag: **fix it at the source** — the order of leverage is performance, then instrument and room, then mic choice and placement, then gain staging, and only then processing; moving a microphone a few inches routinely accomplishes what an hour of EQ cannot. ⚠ Best technical flag: **phase is the invisible problem** — multi-mic recordings fail with no obvious defect, just a mix that sounds thin or hollow while every individual track sounds fine, and beginners respond by adding EQ, which cannot help. Check mono compatibility; cancellation becomes obvious instantly. ⚠ Hearing flag: noise-induced loss and tinnitus are **permanent and cumulative** in a profession whose entire value is hearing accurately — mix at moderate levels, break hourly, get a baseline test now. Career honesty: **studio careers are a small and shrinking niche everywhere**; the employment is in live sound and AV, **Orlando themed entertainment**, broadcast, post, houses of worship, and game audio. |
| **HIM1222C** | ⚠ **Buy the current-year code book** — ICD-10-CM updates every October 1, so an older edition actively teaches codes that no longer exist, and certification exams are keyed to a specific code-set year. ⚠ Procedural rule that fails more students than any other: **never code from the Alphabetic Index alone** — the Tabular List holds the instructional notes, excludes notes, and specificity requirements. The distinction carrying the most weight: **Excludes1 = mutually exclusive, never code both; Excludes2 = separate condition, both may be coded.** Reversing them produces denials and audit findings. ⚠ Ethical/legal flag: **code only what is documented** — a coder may not infer a diagnosis from lab values or medications however obvious, and the correct instrument is a **non-leading query**. Upcoding is fraud under the False Claims Act and coders have been personally implicated; "I was told to" is not a defense. Diagnosis flag experienced coders offer: **anatomy and pathophysiology limit accuracy more than index skill** — students who struggle are usually struggling with the medicine, not the code book. Automation flag: computer-assisted coding produces **suggestions** that fail predictably on negation and context, shifting the role from assigning toward **validating** — which needs more expertise, not less. |

**Rule 21 (before trusting a number's subject, check the number against a real program listing — and
treat an outlier guide length as a warning).** Rules 14–17 covered titles that vary, drift, or misname a
subject. **MAN3554** is the worst case: a published guide that was about **the wrong subject entirely**
— "Operations and Production Management, 3 credits" for a number that is **"Safety and Risk Management,
1 credit"** in Miami Dade's Supply Chain Management B.A.S. The adjacent numbers **MAN3504** and
**MAN3506** genuinely do carry operations and production, which is how the conflation happened. Two
defenses, both cheap. First, **verify a number inside a published program of study**, not only against a
course-description search — a program listing shows the number, title, and credit value together and in
context, which is what exposed this. Second, **guide length is a usable signal**: the wrong-subject guide
was **8,755 characters against an 18,000–22,000 norm**, because a guide written from a mistaken premise
runs out of things to say. When a finished guide comes in far short of the family norm, re-verify the
premise before publishing. The corollary from the same batch runs the other way and matters just as much:
**an unexpected value is not automatically an error**. The six PMT welding guides at 150 hours looked wrong
beside newly verified 50–75 hour courses, but 7 × 150 = the full 1050-hour PSAV program — they
describe the same instruction at a coarser **occupational-completion-point** granularity. Check whether a
discrepancy is a mistake or a different unit of description before "correcting" it.
| **RTE2854L / RTE2844L** | ⚠⚠ **A direct number collision: the roman numeral is institution-specific.** Some Florida programs run RTE1804L/1814L/1824L/2834L/**2844L** as Clinical Education I–V, making **2844L the fifth** (3 cr, ~384 hrs). **NWFSC runs 2844L as IV and 2854L as V, both at 5 credits.** So the same number is "V" at one institution and "IV" at another, with credit values differing by nearly 2×. This is Rule 14's hazard ("sequence by number and prerequisite chain, never by the roman numeral in a local title") in its purest form — and it generalizes: **compare clinical programs by total clinical hours, never course by course.** Mitigating structural fact: JRCERT programs are not assemblable across institutions anyway. |
| **SON2112C / SON2121C** | ⚠ Sonography credit values are inconsistent across the family — SON2111C at 4 cr in some programs, SON2112C at 3 in others; TCC lists SON2121C at **3 cr, 30 lecture + 45 lab**, while other programs carry OB/GYN at 4. ⚠ Credential-structure flag: **ARDMS is per-specialty** — SPI (physics, once) *plus* a specialty exam — and most general sonographers hold **SPI + AB + OB/GYN**, which is why these two sequences run in parallel. Sit SPI while the physics course is fresh. ⚠ Clinical flag: **ectopic pregnancy** is the finding first-trimester scanning exists to catch, and the **pseudogestational sac** is the classic trap. ⚠ Safety flag: **spectral Doppler produces much higher acoustic output than B-mode** and is advised against routinely in the first trimester — document early cardiac activity with **M-mode or a clip**, not spectral. ⚠ Occupational flag with career-ending stakes: sonography has an unusually high rate of **work-related musculoskeletal injury**, and the countermeasures (arm below ~30° abduction, move the patient toward you, light grip) must become habit *during training*. |
| **RET1450C / RET2877** | ⚠ **Pulse oximetry lies in knowable ways** — most dangerously in **carbon monoxide poisoning**, where carboxyhemoglobin reads as oxyhemoglobin and saturation looks normal while the patient is severely hypoxic; also severe anemia, where saturation can be 100% while oxygen *content* is critically low. And it says **nothing about ventilation**. ⚠ Best clinical habit in critical care: **troubleshoot the patient before the ventilator** — disconnect and manually ventilate to separate patient from machine problem — with **DOPES** (Displacement, Obstruction, Pneumothorax, Equipment, Stacked breaths) as the sequence. ⚠ Discrimination worth memorizing: **peak up with plateau unchanged = resistance** (secretions, kink, bronchospasm); **both up = compliance** (edema, consolidation, pneumothorax). Credential flag: the **TMC cut score decides CRT vs. eligibility for the CSE and RRT**, and many Florida hospitals hire RRT-required — aim for the higher score from the start. Configuration flag: Valencia runs **RET1450 as 3 credits, 3 lecture, no lab**, and clinicals as **RET2877L**; the numbers appear with and without C/L suffixes across programs. |
| **RED4511** | ⚠ **Background knowledge drives comprehension more than strategies do** — the most counterintuitive finding in reading research, and it reframes instructional time: strategies are quickly learned and hit diminishing returns, while knowledge and vocabulary are what predict understanding. This is the strongest argument against disconnected leveled passages on unrelated topics. ⚠ Diagnostic flag: **"struggling reader" is not a diagnosis** — word recognition, fluency, vocabulary/knowledge, language comprehension, and engagement produce the same low score and need different instruction; the **Simple View of Reading** organizes it. Underused lever: **morphology** is generative where word-by-word vocabulary teaching cannot scale, and morphological boundaries are usually syllable boundaries, so it doubles as multisyllabic decoding. Florida flag: the **Reading Endorsement** competencies often map to courses students are already taking — ask which, and keep the documentation. |
| **RTV2100C** | ⚠ Craft flag that is the whole method: **read every script aloud and time it** — reading rate is ~150–160 wpm, so ~25 words per 10 seconds. Copy never spoken aloud is untested work. ⚠ Style flag that trips print-trained writers: **attribution comes first** in broadcast, because the listener has already accepted the claim before learning the source and cannot look back — the same logic drives rounding numbers, titles before names, and pronouncers. ⚠ Legal flag: **Florida generally requires all-party consent** to record private conversations, stricter than federal law and directly relevant to interviewing. Craft flag for video: **complement, don't duplicate** — never describe what the viewer can already see. |
| **RTE2473C** | ⚠ **Digital imaging hid overexposure, and dose creep is the result** — with film, overexposure was self-correcting (the image went dark); digital normalizes, so an overexposed image can look *better* because more photons means less noise. This is exactly why the **exposure indicator** exists and why monitoring it is a QC duty rather than a formality. ⚠ Organizational flag: **repeat analysis works only if reporting is honest** — where technologists believe the data will be used against them individually, repeats get deleted quietly and the department loses its best quality signal while believing all is well. Analyze patterns and systems, not individuals. Licensure flag: **Florida licensure is separate from ARRT certification** — apply early, since you cannot work on ARRT alone. |
| **DAA2105 / DAA2205** | ⚠⚠ **DAA is now confirmed the most fragmented prefix in the repository — three parallel families, and they disagree about *level*.** Modern runs **DAA1104C→DAA2105** at some institutions and **DAA1100C→DAA1101C→DAA2102C** at Broward; ballet runs **DAA1204C→DAA2205** versus Broward's **DAA2280C/2281C/2282C** — which places **Ballet I at the 2000 level where others place it at 1000**. That is worse than a numbering mismatch: a content-identical course sits at a different *level*, so it can fail to transfer into a major even where equivalence seems obvious. All technique courses verified at **2 credits** across both families. Confirms and extends the batch-46 finding that **the C suffix signals nothing in this prefix** — Broward applies it to nearly every technique course. ⚠ Technique flag: **turnout comes from the hips**, and forcing it from the feet causes pronation, knee torsion, and the classic ballet-student injuries. Modern flag: it is *not* "ballet without rules" — the floor work is where the difficulty is, and hedging the descent makes it harder and more dangerous than committing. |
| **DEA0020C / DES0501 / DES1832L** | ✅ **Gulf Coast State independently confirmed both batch-46 corrections**: DES1100C at **3 credits, 1 lecture + 3 lab**, and DES1200 + DES1200L summing to **3 credits / 75 hours** — exactly the values those guides were corrected to. Also confirmed batch-47's DES1010 at 2 credits. ⚠ **New structural finding: institutions report the 0xxx block inconsistently.** Some carry DES0xxx/DEA0xxx as pure PSAV clock hours with *zero* college credit; Gulf Coast lists DES0501 and DES0844 **with credit values in the same table as DES1xxx courses**. So a "credit" against a 0xxx course may be a **vocational credit**, not a transferable one — which complicates the clean PSAV/credit split recorded in batch 46. ⚠ Caught an assumption before it shipped: **DES0501 is 1 credit**, not the 3 a management course suggests. Configuration flag recurs: Gulf Coast splits **DES1832 + DES1832L** (two registrations) where others use one C course, same as its DES1200/DES1200L split — so **compare programs by total hours and credits, never by course count**. |
| **EAP1660** | ✅ **Second consecutive validation of the EAP numbering grid** published in batch 37 — the grid predicted Grammar Level 6 at EAP1660, 3 credits, and it holds. New wrinkle worth recording: some institutions **do not run a separate grammar course at this level at all**, folding it into **EAP1685** (advanced writing *and* grammar), so the grid has empty cells rather than universal coverage. ⚠ Best flag: **keep an error log** — advanced learners do not make random errors but repeat a small set of patterns, usually first-language-traceable, so targeting three or four issues beats studying grammar generally. ⚠ Honest flag: **articles are genuinely among the last structures acquired**, and speakers of article-less languages face a system with no L1 equivalent — persistent article errors are not carelessness. Register flag: by Level VI the issue is no longer correctness but **academic register** — nominalization, hedging, and complex noun phrases — and these are conventions that vary by discipline, not laws. |
| **HIM2283C / HIM2442** | ⚠⚠ **Florida runs at least two parallel HIM numbering families, with different credit values.** One family: HIM1000C, HIM1222C, HIM2253C, **HIM2283C**, HIM1273C, HIM2442, HIM2652C, HIM2800. Valencia runs a different set entirely — HIM1012, HIM1110, HIM1211, HIM1430, **HIM2222C and HIM2729C at 4 credits (3 lec + 3 lab)**, with practicum as **L-suffixed** HIM1800L/2810L/2820L at 2–3 credits and 6–9 lab hours weekly. So coding courses are **3 credits in one family and 4 in the other**. Methodological note worth keeping: Valencia's data could not be used to price HIM2283C *because it is a different family* — cross-family evidence is not evidence about a number. ⚠ Technical flag: **PCS root operation selection is where audits land**, because root operations are defined by *intent and outcome*, not the surgeon's terminology — read the body of the operative report, not the header, and query rather than guess. ⚠ Reimbursement flag: coding drives **MS-DRGs**, so a CC/MCC can move a case into a much higher-paying group — which is why under-coding loses legitimate revenue *and* over-coding is fraud, and the professional position is neither. ⚠ Drug-billing flag: **J-code units are defined by the code descriptor, not the dose administered** — billing 40 units where 4 are correct is a tenfold overcharge and a standard audit sample. |
| **HUS1400** | ⚠ **Evidence flag where practice most diverges from research: medication for opioid use disorder works**, and is underused partly because of stigma *within* the treatment field ("substituting one drug for another"). The distinction that matters clinically is **physical dependence vs. addiction** — someone stabilized on a prescribed medication and functioning is in recovery by any outcome measure. ⚠ Safety flag that surprises students: **alcohol and sedative withdrawal can kill** (seizures, delirium tremens) while opioid withdrawal usually does not — the opioid danger comes *after*, when tolerance has fallen and a previous dose becomes fatal, which is why overdose deaths cluster after release from incarceration or discharge from treatment. ⚠ Language flag that is clinical rather than polite: stigmatizing terms measurably **change how clinicians judge and treat** the same case. Career flag: Florida Certification Board credentialing combines coursework with **thousands of supervised hours** — find employment providing qualified supervision, since students routinely discover a year of work did not count. |
| **ITA2220 / GER2220** | ✅ **The world-language pattern is now verified across three languages**: FRE, GER, and ITA intermediate courses all carry **4 credits**, with Broward listing **64 contact hours** for both GER and ITA beginning courses. This is a genuinely reliable family for deriving values. ⚠ Recurring **C-suffix inconsistency**: Broward runs GER1120/1121/2220 and ITA1120/1121 *without* the C where other Florida institutions use GER1120C/GER1121C and ITA1120C/ITA1121C — same credits, different contact hours. Grammar flag worth reusing: the **passato prossimo / imperfetto** distinction is about **aspect, not time** — how the speaker views the action, not when it happened — and Spanish and French speakers have a head start while English speakers have nothing to map onto. Career honesty: Italian is not a general business language, but it is a **working requirement** in art history, conservation, classical and operatic music, and classics — where graduate programs frequently require reading knowledge. |
| **MAN4741** | ⚠ **The metric warning that generalizes well beyond agile: velocity is a forecasting tool, not a performance measure.** The moment it is used to evaluate or compare teams it stops being honest — story points are relative and team-specific, so cross-team comparison is meaningless by construction, and a team measured on velocity inflates estimates while delivering identical work. This is the same dynamic as the KPI-gaming flag from CTS2450 and the repeat-analysis flag from RTE2473C: **a measure used as a target stops measuring what it did**. ⚠ Failure-point flag: **the product owner role is where agile most often fails** — organizations supply someone lacking decision authority, availability, or domain knowledge, and a backlog that is a wish list rather than an ordered list is the same as having no priorities. The underlying point: agile requires **organizational change, not just team practice**. Career honesty: certification is cheap signalling in a crowded market; employers assess whether you have actually worked on a team using these methods. |

**Rule 22 (the `C`/`L` suffix is part of the number, and it diverges across Florida more often than
anything else).** Rules 14, 15 and 17 concern a number whose credits, subject, or title move. This is
narrower and far more common: **the same course exists at different institutions with and without its
`C` or `L` suffix**, and the suffix is what encodes the lecture/lab structure — so it changes the contact
hours, and sometimes the credits, while the subject stays identical.

A systematic audit (`Tools/audit_suffixes.py`, output in `Tools/SUFFIX_AUDIT.txt`) compared all 1,889 queue
ids against the 1,266-course DSC catalog. **246 queue ids — 13% — do not exist at DSC under the id we
carry, but do exist there under the opposite `C`/`L` suffix.** Breakdown: **155 already pushed**, 61 still
queued, 29 skipped, 1 drafted.

Most of these are *not* data errors. `MAC1105` and `MAC1105C` are both real SCNS numbers; DSC simply
teaches one of them. But the audit exposes a real defect risk, and one confirmed pattern:

⚠ **A `C`-suffixed guide carrying exactly the lecture-only profile (3 cr / 45 hrs) is the signature of a
guide written from the *non*-`C` course.** Spot-checked published examples sitting at 3 cr / 45 hrs under
an integrated-lab number: `MAC1105C`, `STA2023C`, `ENC1101C`, `BSC1005C`, `ACG2021C`, `HSC1531C`. A
C-suffixed course should be ~60 hours; these carry the profile of their non-suffixed twin. Compare the
correctly-written `OTH1014C` and `RET1485C`, both 3 cr / **60** hrs.

**Operational rules:**
1. Before writing any course whose id ends in `C` or `L`, **check whether DSC carries it with the opposite
   suffix** — `audit_suffixes.py` answers this for the whole queue at once.
2. If DSC has only the non-`C` form, **do not price the `C` course from DSC's hours.** Get the C-suffixed
   value from an institution that actually publishes it, or say so in the guide.
3. `validate_drafts.py` already warns on "C course with only 45 contact hours" — **treat that warning as a
   finding, not noise.** It fired correctly on `RET2244C` in batch 55.
4. Never treat `X` and `XC` as equivalent for transfer. **SCNS equivalency does not cross numbers, and the
   suffix is part of the number.**

Worked cases from batch 55: `RET2244C` (inventory id) is `RET2244` at both DSC *and* Valencia and is absent
from Broward and Gulf Coast — three catalogs, zero instances of the C form. `RET1025C` is C-suffixed at DSC
but `RET1025` (3-0-0 lecture, labs broken out as `RET1274L`) at Valencia. `RET2876` is `RET2876L` at
Valencia. `PLA2201` is `PLA1201C` at Broward — suffix *and* level differ.

**Related: three parallel RET numbering families.** DSC integrates (`RET1025C`, `RET1026C`, `RET1264C`),
Valencia splits lecture from L-labs (`RET1025` + `RET1274L`/`RET2283L`/`RET2284L`), and Broward and Gulf
Coast use entirely different numbers (`RET1024`, `RET1832L`). Respiratory care is now the clearest
parallel-family case in the repository, ahead of HIM.

**Also from batch 55 — credit drift at 3×.** `DEH1602` is **Periodontology, 3 credits** at DSC and
**"Periodontology I", 1 credit** at Valencia, which splits the content across `DEH1602` + `DEH2604` +
`DEH2605` (1+1+1). Same number, one third the content. The largest single-number credit divergence found
so far.

### Batch 67: EAP is 6 credits where every other EAP course is 3 — and the suffix changes the hours

Two findings from the same family, and together they are the clearest live illustration of Rule 22
(the C/L suffix is part of the number) yet found.

**EAP1585C and EAP1685 are 6-credit courses at DSC.** Every other EAP course in the repository is 3.
This is not an error in the catalog — it is **intensive English program (IEP) design**, where the
writing-and-grammar core is built as one large integrated block rather than as separate small courses.
Anyone diffing an EAP sequence against a 3-credit assumption will read these as data errors; they are not.

**The two 6-credit courses have different contact hours, and the suffix is why:**

| Course | Suffix | Credits | Hrs/cr | Contact hours |
|---|---|---|---|---|
| EAP1585C High-Intermediate Writing and Grammar | **C** (combined lecture + lab) | 6 | **20** | 120 |
| EAP1685 Advanced Writing and Grammar | none | 6 | **15** | 90 |

**So the EAP prefix carries two contact-hour conventions side by side: 15 hrs/cr for non-suffixed
courses, 20 hrs/cr for C-suffixed ones.** Same credit value, 30 hours of difference, and the only
thing signalling it is the suffix. Check the suffix before deriving contact hours for any EAP number.

**Practical consequence worth carrying into the guides:** a 6-credit EAP course has no clean
equivalent at an institution whose EAP writing courses are 3 credits, so transfer is unusually
unpredictable — and EAP credit is frequently institutional-credit-only or capped as elective anyway.
Both guides flag the financial-aid and excess-hour-surcharge exposure prominently.

### Batch 67: two more title-drift cases, and a 1000/4000 parallel-numbering trap

**Title drift** — the queue title and the catalog title disagree, both times harmlessly but in a way
that would defeat a title-match lookup:

| Course | Queue / inventory title | Published title | Institution |
|---|---|---|---|
| DSC4725 | Response and Recovery | **Disaster Recovery** | FSU (Emergency Management) |
| EEX1600 | Behavior Management | **Classroom Management (Early Childhood)** | DSC |
| EEX3280 | Career/Vocational Assessment and Planning | **Transition Planning** / Transition to Adult Life | Broward, FIU |

**The parallel-numbering trap: EEX1600 vs the already-published EEX4601.** Both are titled around
behaviour management and the subject genuinely overlaps, but EEX1600 is a **1000-level** course inside
an A.S. in Early Childhood Education and EEX4601 is a **4000-level** course inside a teacher-preparation
baccalaureate. **Lower-division credit does not satisfy an upper-division requirement**, so a student who
completed EEX1600 will still need EEX4601. This is the same shape as the TAX2000C/TAX3001 and
CAP2741C/CAP3744 traps already documented — the title similarity is the hazard, and both guides now
cross-reference each other explicitly.

**EEX3280 also 404s at DSC** and was resolved from Broward and FIU via search. A 404 at DSC is the one
trustworthy negative (per the Tier 0 rule) — it means DSC does not offer the number, not that the
number is wrong.

### Batch 68: two more C-suffix pairs, both already published in this repository

Rule 22 confirmed twice more, and this time **both halves of each pair are in the repository**, which
makes the divergence checkable rather than inferred:

| Non-suffixed (published) | C-suffixed (batch 68) | Divergence |
|---|---|---|
| **ETS3543** Programmable Logic Controllers — **4 cr / 80 hrs** | **ETS3543C** — **3 cr / 60 hrs** | a full credit and 20 contact hours |
| **ETD2390** 3D AutoCAD / Revit — **3 cr / 45 hrs** | **ETD2390C** Introduction to Revit Architecture **and Lab** — **3 cr / 60 hrs** | same credits, 15 more contact hours |

**Practical rule reinforced:** when a batch course carries a C or L suffix, **grep the drafts directory
for the un-suffixed number before writing.** Both of these were found that way and both became a
cross-reference in the new guide. It costs one command.

### Batch 68: the PLC family is a 2000-vs-3000 transfer trap, not just a naming mess

Florida teaches programmable logic controller content under **at least six numbers**, and the spread
crosses the one boundary that actually blocks transfer:

| Number | Credits / hours | Where |
|---|---|---|
| ETS1542C | 3 / 60 | published |
| **ETS2542C** | 3 / 64 (48 lec + 16 lab) | **Broward — 2000-level, inside an A.S.** |
| ETS2544C Advanced PLCs | 2 / 60 | published |
| ETS2673C | 4 / 80 | published |
| **ETS3543C** | 3 / 60 | **DSC — 3000-level, inside a B.S.** |
| ETS3543 | 4 / 80 | published |

⚠ **Broward's ETS2542C will not satisfy DSC's ETS3543C** — lower-division credit does not satisfy an
upper-division requirement, and A.S. graduates moving into the B.S. in Engineering Technology are
exactly the population that hits this. Same subject, same lab content, wrong side of the 2000/3000 line.

### Batch 68: Florida splits introductory environmental science two ways, and the lab is the casualty

Verified across four catalogs in one pass:

| Institution | Structure | Lab? |
|---|---|---|
| **Daytona State** | **EVR2001** (3 cr) + **EVR2001L** (1 cr) as corequisites | yes, separately numbered |
| Broward | **EVR1001**, 3 cr, 48 contact hrs | **no — 0 lab hours** |
| Valencia | **EVR1001**, 3 cr, 3 lec / 0 lab | **no** |
| Gulf Coast | **EVR1001**, 3 cr, 3 lecture | **no** |
| (elsewhere) | **EVR1001C** combined | yes, integrated |

⚠ **This is a general-education problem, not a cosmetic one.** Most Florida degrees require a
*laboratory* science, and **EVR1001 without a lab does not satisfy it**. A student arriving with
EVR1001 may still owe a lab; a student leaving DSC with EVR2001 + EVR2001L may find the receiving
institution has nowhere to map the extra credit. The level also differs (1000 vs 2000), which defeats
a search by number. Same subject, three different structures, one of which fails a graduation audit.

### Batch 68: ESI4312 is the messiest single-number title spread found so far

Four institutions, one number, four different answers — and one of them does not carry the number at all:

| Institution | Number | Title |
|---|---|---|
| Daytona State | ESI4312 | Operations Research |
| UCF | ESI4312 | **Deterministic Methods for** Operations Research |
| USF | ESI4312 | **Foundations of Optimization** (formerly Deterministic Operations Research) |
| **University of Florida** | **ESI3312 + ESI4313** | Operations Research 1 / **2** — **no ESI4312 exists** |

Two usable conclusions. The UCF and USF titles establish that **ESI4312 is normally the deterministic
half** (linear/integer programming), with stochastic methods in a separate course — useful when writing
scope for any institution that publishes only a bare title. And **UF's split into 3312 + 4313 means
there is no clean mapping in either direction**, which is a real advising problem, not a naming quibble.

### Batch 68: FFP2801 is DSC-shaped; Valencia teaches the same role under a different number

FFP2801 "Introduction to Command" is **absent from Valencia's FFP listing**, which covers company-level
command as **FFP2720 Company Officer** and tactics as **FFP2810/2811**. Broward's Fire Science program
map does carry FFP2801. Useful negative: Valencia's FFP page is complete and well structured, so
**a course missing from it is genuinely not taught there** — one of the few catalogs where absence is
informative rather than ambiguous. Also confirmed: **the whole DSC FFP family runs 3 cr / 45 hrs**,
which prices any DSC fire-science number without further lookup.

### Batch 69: a third HIM numbering family, and the C-suffix trap fires again

**HIM2400C → Daytona State publishes HIM2400, without the C.** Another instance of the 246-of-1,889
pattern. Neither Broward nor Valencia carries the number in either form.

More significant: **Florida runs at least three parallel HIM numbering families**, not the two this file
previously documented. Broward is a distinct third:

| Family | Representative numbers | Distinguishing feature |
|---|---|---|
| **A — Daytona State** | HIM1000C, HIM1222C, HIM1273/1273L, HIM2253C, HIM2283C, **HIM2400**, HIM2430, HIM2442, HIM2652, HIM2800 | coding at 3 cr; C-suffixed |
| **B — Valencia** | HIM1012, HIM1110, HIM1211, HIM1430, HIM1453, HIM2222C, HIM2253, HIM2729C, HIM1800L/2810L/2820L | **ICD coding at 4 cr** (3 lec + 3 lab); practicum L-suffixed |
| **C — Broward** *(new)* | HIM1000, HIM1110C, **HIM1253C / HIM2232C / HIM2728C** (Coding I/II/III), HIM1260, HIM2112C, HIM2214, HIM2433, HIM2930 | coding as a numbered **I/II/III ladder**; HIM1000 at 3 cr / 48 hrs |

Note the collisions that make title-matching dangerous here: **HIM1110 is 3 cr lecture-only at Valencia
and HIM1110C at Broward**; **HIM2253 is CPT coding at Valencia (3 cr) and HIM2253C at DSC**; and
**HIM1000 is 2 cr at Valencia, 3 cr at Broward, and HIM1000C at DSC**. Same three digits, three
institutions, three different courses. The standing rule holds: **cross-family evidence is not evidence
about a number.**

### Batch 69: Broward's GRA prefix runs 24 contact hours per credit

A contact-hour convention well outside the usual range, verified across Broward's whole GRA listing:

- **Most GRA courses: 3 cr / 72 contact hrs** (typically 32 lecture + 40 lab)
- **GRA2190C and GRA2191C: 3 cr / 96 contact hrs** (32 + 64)
- **GRA2134C** (batch 69): 3 cr / **72 hrs — 30 lecture + 42 lab**
- GRA2940C Internship: 1 cr / 272 hrs

That is **24 hrs/credit as the family norm and 32 for two courses**, against this repository's usual
60-hour figure for a 3-credit C course. It is a **studio model** — more than half the scheduled time is
production work. `validate_drafts.py` flags 72 as a warning against the 45/60 expectation; **the warning
is correct to fire and the value is correct to keep**, because Broward publishes the split explicitly.
Worth remembering that a receiving institution's 60-hour equivalent is a genuinely smaller course.

### Batch 69: GER is a clean in-family demonstration of what the C suffix costs

Rare case where one prefix at one institution shows the suffix difference with everything else held constant:

| Course | Suffix | Credits | Contact hours |
|---|---|---|---|
| GER1120C, GER1121C (elementary) | **C** | 4 | **~75** |
| GER2220, GER2221 (intermediate) | none | 4 | **~64** |

Same institution, same prefix, same credit value, **11 contact hours apart** — the elementary courses
carry a required language-laboratory component the intermediate ones drop. Useful as the textbook
example when explaining Rule 22 to a reader: the suffix is not cosmetic and it is not about difficulty.

### Batch 69: the DSC HFT family prices without a lookup

Confirmed across nine published guides plus four more in batch 69, spanning the 1000 to 4000 levels:
**every non-suffixed Daytona State HFT course is 3 credits / 45 contact hours**, and the C-suffixed ones
(HFT2750C, HFT2867C) are **3 credits / 60**. No exceptions found in thirteen courses.

That makes HFT one of the few prefixes where a DSC number can be priced from the family alone. It also
means DSC teaches **upper-division hospitality (HFT3373, HFT4809, HFT3700, HFT4064, HFT4253, HFT4277)**
at the same 45-hour shape as its lower-division courses — the level changes the depth, not the contact time.

**Negative results from this batch, worth not re-checking:** Valencia carries **no FFP2801, no ETD2390C,
and no HIM2400/2400C**; Broward carries **no GRA2144C and no HIM2400C**; Gulf Coast's HIM listing holds
**only HIM2949**. Valencia's and Broward's prefix pages are complete enough that **absence is informative**
in those two catalogs — one of the few places a negative can be trusted.

### Batch 70: IND1233C carries a suffix divergence *and* a credit divergence at once

The first course found where both hazards fire on the same number:

| Institution | Number | Credits | Note |
|---|---|---|---|
| **Daytona State** | **IND1233** — no C | 3 | "Studio I-Fundamentals of Interiors", $110.50 lab fee |
| Seminole State | **IND1233C** | 3 | "Studio I", min grade C to progress |
| Palm Beach State | **IND1233C** | **4** | "Design Studio 1", coreq IND1401C |

So a transferring student can arrive with 3 credits against a 4-credit requirement **for the identical
course number**. The whole DSC interior design sequence publishes without suffixes — **IND1233, IND1429,
IND2210, IND2500** — where other Florida institutions carry C forms, so this is a prefix-wide pattern at
DSC rather than a one-off. `IND1429C` in the same batch is the same case (DSC publishes IND1429, 3 cr,
$15 lab fee, fall).

**Studio contact hours:** written at **3 cr / 90 hrs** (~6 studio hrs weekly), matching this repository's
published **IND2210C at 3/90**. `validate_drafts.py` warns against the 45/60 expectation; the warning is
correct to fire and the value is correct to keep — studio courses run ~30 hrs/credit.

### Batch 70: three HUS courses that exist nowhere current — resolved from DSC's 2019-2020 catalog

**HUS1421, HUS1423, and HUS2050 are absent** from `daytona_courses.csv`, from DSC's 2024-2025 catalog,
from Broward's HUS listing (17 courses, none of them these), and from Valencia (which has **no HUS prefix
page at all — 404**). All three came back cleanly from **DSC's archived 2019-2020 catalog**:

| Course | Title | Credits | Note |
|---|---|---|---|
| HUS1421 | Assessment and Treatment Planning in Addictions | 3 | also current at **Palm Beach State**, in an Addiction Studies CCC |
| HUS1423 | Group Counseling in Substance Abuse | 3 | fall/spring |
| HUS2050 | Introduction to Case Management | 3 | **corequisite HUS1001** |

**Broward teaches case management as HUS2415** (3 cr / 48 hrs) — a different number for the same subject,
worth recording so it is not re-researched. The published DSC HUS family is uniformly **3 cr / 45 hrs**
across seven courses now, which prices any DSC HUS number.

### Batch 70: negatives confirmed, and Valencia's prefix coverage has real holes

Worth recording so these are not re-checked:

- **Valencia has no HUS and no IND prefix page** — both 404, not empty. Valencia's catalog is complete
  *within* the prefixes it carries, but it does not carry every prefix, so **a Valencia 404 means "not
  taught here", not "fetch failed"**.
- **Broward has no IND prefix page** (404) — no interior design programme.
- **Broward's HUS listing is 17 courses at a uniform 3 cr / 48 hrs**, with practicum courses broken out at
  138 and 122 total hours (48 or 32 lecture + 90 "other"). A clean family for pricing.

### Batch 71: ⚠⚠ **Proof of what the C suffix means — the arithmetic closes exactly**

The most important methodological finding in this file. Rule 22 has until now rested on inference; this
is direct evidence, and it reconciles to the hour.

| Number | Title | Clock hours |
|---|---|---|
| **MSS0803** | Massage Theory and Clinical Practicum I | **62.5** |
| **MSS0803L** | …and Clinical Practicum I **Lab** (corequisite) | **75.5** |
| | **pair total** | **138.0** |
| **MSS0803C** | the combined form — *already published in this repository* | **138** ✓ |

**The C-suffixed course is the non-suffixed lecture course plus its L lab, hour for hour.** Same programme,
same institution, same content, three distinct SCNS numbers. This simultaneously **validates the published
MSS0803C guide** and gives Rule 22 a worked proof rather than an argument.

**Use this as the standing explanation of the suffix** when writing any C or L guide, and check for the
sibling numbers before writing either half — DSC's MSS listing shows the same split for **MSS0804 /
MSS0804L**, so the pattern repeats within the prefix.

### Batch 71: DSC publishes clock hours directly for PSAV courses — no framework lookup needed

Worth recording prominently because it changes the research path for every 0-level DSC course.

The DSC catalog page reports the hour value in the credits field for PSAV courses, e.g. **MEA0204C = "150
clock hours"**, **MEA0230C = "120 clock hours"**, **MSS0803L = "75.5 clock hours"**. That means **the Tier 1
FLDOE framework lookup is unnecessary whenever the course exists at DSC** — which matters a great deal now
that **fldoe.org returns 403**.

Two cautions:
- **Hours vary sharply between adjacent numbers.** MEA0230C is 120 hrs and **MEA0231C is 180** — neighbouring
  numbers, 60 hours apart. Never infer an hour value from an adjacent number in the same prefix.
- **Fractional hours occur.** MSS0803L is **75.5**. `validate_drafts.py` **blocks non-integer contact_hours**,
  so the field must be rounded; state the exact catalog figure in the guide text and say the field is rounded,
  since students count these hours toward a licensure requirement.

### Batch 71: the C-suffix contact-hour consequence is set per-prefix, even inside one institution

A refinement to Rule 22 that prevents over-generalizing. Two DSC language sequences behave differently:

| Prefix | Elementary (C-suffixed) | Intermediate (no suffix) |
|---|---|---|
| **GER** | GER1120C / 1121C — 4 cr / **~75 hrs** | GER2220 / 2221 — 4 cr / **~64 hrs** |
| **ITA** | ITA1120C / 1121C — 4 cr / **~60 hrs** | ITA2220 / 2221 — 4 cr / **~60 hrs** |

So in German the suffix carries an 11-hour difference and in Italian it carries none — **at the same
institution, in the same discipline area, at the same credit value.** The suffix is still part of the number
and still blocks equivalency; what varies is the *contact-hour consequence*, which is set locally.
**Do not price a C course by analogy to another prefix's C courses.**

### Batch 71: MAE2801 vs MAE4326 — content and methods are different courses

Another 2000/4000 parallel-numbering trap for the collection, in the same shape as TAX2000C/TAX3001,
CAP2741C/CAP3744, and EEX1600/EEX4601:

- **MAE2801 Elementary School Mathematics (2000)** — mathematics **content** for prospective teachers.
- **MAE4326 (4000, already published)** — **methods**: how to teach it.

Both are normally required; the lower-division course does not reduce the upper-division requirement.
Worth flagging in any MAE guide because the prefix and the titles both suggest interchangeability.

### Batch 72: two more suffix pairs, and a fieldwork family that prices itself

**MUS1010L → the repository already holds MUS1010** (0 cr / 15 hrs). DSC's current catalog carries **only
the L form**; the non-suffixed number 404s there. Same title, same structure, two SCNS numbers. Another
instance of the 246-of-1,889 pattern, and the second one this session where **both halves were already in
the drafts directory** — the grep-before-writing habit paid off again.

**OTH2841 prices exactly from its published sibling.** OTH2840 (published, 5 cr / 320 hrs) and OTH2841 are
both **"eight weeks of full-time fieldwork"** at **5 credits** — structurally identical, differing only in
the required *diagnostic population*. 8 weeks × 40 hrs = 320, and the catalog language confirms it rather
than requiring derivation. **Level II OT fieldwork is 16 weeks total under ACOTE**, which is why the
programme splits it into two eight-week courses.

### Batch 72: substantial title drift in the OST prefix — the inventory name is actively misleading

| Course | Inventory / queue title | DSC published title | Comment |
|---|---|---|---|
| OST2401 | Office Procedures | **Basic Office Procedures** | "Basic" matters — it is the generalist feeder to the legal and medical specializations |
| OST2431 | **Legal Operations** | **Legal Office Procedures** | ⚠ **the worst drift found so far** |

**OST2431 is the sharpest case in this file.** "Legal operations" in current professional usage means legal
*department management* — budgeting, technology, process design. The actual course is legal secretarial
procedure: pleadings, dockets, e-filing, transcription. A student selecting from the inventory title alone
would get an entirely different subject than expected. **Never write a guide from an inventory title.**

### Batch 72: the OST prefix diverges more than almost any other across Florida

Three institutions, three largely disjoint number sets — and **the batch's two DSC numbers exist at neither
of the others**:

| Institution | Characteristic numbers | Contact hours |
|---|---|---|
| **Daytona State** | OST1100/1110/1141 keyboarding, **OST2401/2431/2461** procedures, OST2501 mgmt | 3 cr / 45 (procedures), 3 cr / 60 (C-suffixed keyboarding) |
| **Broward** | OST1100C, OST1103C, OST1355C Records Mgmt, OST2455C/2456C med billing, OST2764C | uniform **3 cr / 48** |
| **Valencia** | OST1257C, OST1355C, OST1611C/2612C med transcription, OST2756C/2836C/2858C software | uniform **3 cr, 3/3 lec/lab** |

**Neither Broward nor Valencia carries OST2401 or OST2431.** Broward's OST family is uniformly 48 contact
hours for 3 credits; DSC's procedures courses are 45. Treat OST transfer as requiring written evaluation
in every case.

### Batch 72: OST1711 deferred — genuinely unreachable

Checked and found absent from **six** sources: DSC current (2024-2025) and archived (2019-2020) catalogs,
Broward (14 OST courses), Valencia (20 OST courses), Gulf Coast (1 OST course), and Seminole State; web
search returns no Florida instance of the number. **No title, credit value, or description could be
established.** Deferred rather than guessed. Recorded here so the same six lookups are not repeated.

**Useful negative confirmed:** Gulf Coast's OST listing holds **only OST2949**, and its EVR listing held
only two courses — Gulf Coast's prefix pages are thin, so **absence there is weak evidence** compared with
Broward's or Valencia's, whose listings are complete within the prefixes they carry.

### Batch 73: ⚠ **PGY is a whole prefix published without suffixes at DSC** — and the CSV agrees

Three of eight courses in this batch were suffix divergences, and two of them are part of a **prefix-wide
pattern** rather than isolated cases:

| Queue ID | DSC publishes | Credits | Note |
|---|---|---|---|
| PGY1100C | **PGY1100** Analog Photography | 3 | $40 lab fee |
| PGY2750C | **PGY2750** Introduction to Video Production | **4** | $35 lab fee |
| PHT1128C | **PHT1128** Kinesiology of PTA | 4 | prereq BSC1085C |

**DSC's entire PGY listing is unsuffixed** — PGY1100, PGY1101, PGY1201, PGY1800, PGY2210, PGY2470, PGY2650,
PGY2750, PGY2801 and the rest — while this repository's four already-published PGY guides all carry the C
form. **`daytona_courses.csv` itself lists `PGY1100`**, which is a useful independent confirmation: the CSV
mirrors the catalog, not the statewide inventory.

**Prefixes now confirmed as DSC-publishes-unsuffixed: PGY (photography), IND (interior design), and largely
PHT.** When a batch course from any of these 404s at `/<level>/<id>c/`, **drop the C and refetch** before
concluding anything.

### Batch 73: DSC's PHT prefix splits lecture from lab — same structure as MSS

DSC publishes **paired numbers**: PHT1251 + PHT1251L, PHT2140 + PHT2140L, PHT2211 + PHT2211L, PHT2214 +
PHT2214L, PHT2220 + PHT2220L, PHT2221 + PHT2221L, PHT2235 + PHT2235L. Other institutions publish the
combined C forms, and this repository's published **PHT2220C (4 cr / 75 hrs)** is one of them.

This is the **second prefix** showing the structure that the MSS0803 / MSS0803L / MSS0803C arithmetic proved
exactly (62.5 + 75.5 = 138). **PHT1128 is one of the few DSC PHT courses with no paired L number**, which
suggests an integrated lab — worth noting rather than assuming a missing sibling.

### Batch 73: PCB3060 vs PCB3063C — same subject, different credits, and one has no lab

| Number | Title | Credits | Lab? |
|---|---|---|---|
| **PCB3060** (this batch) | Introduction to Genetics | **3** | **no** |
| **PCB3063C** (published) | Genetics | **4** / 75 hrs | **yes**, C-suffixed |

Both **upper division**, both genetics, **different credit values**, and only one satisfies a laboratory
requirement. A student holding the 3-credit lecture form against a degree requiring the lab-bearing form has
a real gap. Adds to the collection alongside ETS3543/ETS3543C and ETD2390/ETD2390C.

### Batch 73: OTH Level I vs Level II fieldwork prices differently — do not average the family

The OTH practicum family spans a 5× credit range and the ratio is not constant:

| Course | Level | Credits | Hours | Structure |
|---|---|---|---|---|
| **OTH1800** (this batch) | **Level I** | **1** | ~45 derived | part-time, integrated with coursework |
| OTH2840 (published) | Level II | 5 | 320 | 8 weeks **full-time** |
| OTH2841 (published) | Level II | 5 | 320 | 8 weeks **full-time**, different population |

**Level I has no ACOTE minimum hour requirement**; Level II has a hard 16-week total. So the 64 hrs/credit
ratio from the Level II courses **must not be applied to the Level I course** — 1 credit × 64 would be
wrong. Derive Level I practicum hours from the integrated part-time convention (~45), and say it is derived.

**Related pricing note:** DSC publishes clock/contact values inconsistently across health programmes.
Compare PHT2810 (2 cr / 240 hrs = 120 hrs/cr, full-time clinical) with OTH2840 (5 cr / 320 = 64 hrs/cr,
also full-time). **Full-time clinical is not one ratio** — check the stated week count and multiply, rather
than reusing a ratio from an adjacent programme.

### Batch 74: ⚠ **the lecture+lab identity is structural, not numerical** — three PHT pairs, three different totals

This corrects an over-generalization from the MSS0803 finding. That case closed **exactly** (62.5 + 75.5 =
138), and it was tempting to treat the arithmetic as a rule. **It is not.** Three DSC PHT pairs, all
verified from the catalog in one batch:

| DSC lecture | DSC lab | Pair total | Combined C form | Closes? |
|---|---|---|---|---|
| PHT1251 — 2 cr | PHT1251L — 2 cr | **4 cr** | PHT1251C — 4 cr | ✅ |
| PHT2211 — 2 cr | PHT2211L — 1 cr | **3 cr** | *(none published here)* | n/a |
| PHT2220 — 3 cr | PHT2220L — 2 cr | **5 cr** | PHT2220C — **4 cr** | ❌ **off by one credit** |

**The revised rule: the C-suffixed course is structurally the lecture plus its lab, but the credit value is
set locally and cannot be derived from the other form.** Three distinct SCNS numbers exist per pairing —
lecture, lab, and combined — and a student holding the split pair against a requirement written for the
combined form may face a genuine credit discrepancy, not merely a paperwork one.

**Practical instruction for future batches:** when a queue ID is a C or L form in PHT, MSS, or any
split-publishing prefix, **fetch all three numbers** before writing. Do not compute one from the others.

### Batch 74: DSC PHT contact-hour conventions, now pinned

Enough of the family is verified to price it:

- **Lecture: 15 hrs/credit** — PHT1300 (published) 4 cr / 60 hrs confirms it; PHT2211 at 2 cr → 30 hrs.
- **Lab: ~30 hrs/credit** — PHT2211L 1 cr → 30; PHT2220L 2 cr → 60.
- **Combined C form: ~75 hrs at 4 credits** — PHT1128C and PHT2220C both published at 4/75.

Note the consequence: **the combined form's 75 hours is *less* than the split pair's implied total**
(PHT2220 45 + PHT2220L 60 = 105). The two structures are genuinely different courses in contact time as
well as credit, which is further reason not to derive one from the other.

### Batch 74: DSC publishes PSAV clock hours to the half-hour

**PRN0004C = 457.5 clock hours.** Second fractional PSAV value found (after MSS0803L at 75.5), which makes
it a pattern rather than a one-off. `validate_drafts.py` **blocks non-integer contact_hours**, so the field
must be rounded — 458 here — with the exact catalog figure stated in the guide text, since students count
these hours toward programme completion and licensure.

Also worth recording: **PRN0004C at 457.5 hours is the largest single course in this repository**, ahead of
NUR2731C (10 cr / 320 hrs) and the PSAV nursing blocks PRN0091/0092/0096 (450 each). When a PSAV course
looks implausibly large, check the catalog rather than assuming a transcription error.

### Batch 74: lab fees are a useful signal of consumable-heavy courses

Not a numbering finding, but a practical one for guide content. This batch's DSC lab fees span three orders
of magnitude and track consumables closely:

| Course | Lab fee | What it reflects |
|---|---|---|
| PHT2220L | $6.00 | minimal consumables |
| PHT2211L | $9.00 | modality supplies |
| RET1265C | $32.00 | circuits and supplies |
| PRN0004C | $205.50 | nursing lab consumables |
| **PMT0161C** | **$433.02** | **pipe, electrodes, shielding gas** |

Worth mentioning in a guide where the fee is high, because **students routinely assume the lab fee covers
their materials and it frequently does not** — PGY1100's $40 fee covers facility access while film and
paper are bought separately. Where the catalog publishes a fee, state it and say what it does and does not
cover.

### Batch 75: ⚠ **the "prefix publishes unsuffixed" generalization is too strong** — RET and RTE are mixed

Batch 73 recorded PGY and IND as prefixes DSC publishes entirely without suffixes. **RET and RTE do not
behave that way** — they are mixed *within* the prefix, at the same institution, in the same catalog:

| Prefix | DSC publishes **with** C | DSC publishes **without** C |
|---|---|---|
| **RET** | RET1025C, RET1026C, RET1264C, RET1265C | **RET1450, RET1485, RET2244, RET2714** *(repo published all four as C forms)* |
| **RTE** | RTE1457C, RTE1503C, RTE1513C, RTE1523C, RTE2563C, RTE2573C | **RTE1000, RTE1111, RTE1418, RTE2385, RTE2613, RTE2623, RTE2782** *(repo published several as C forms)* |

**Revised rule: suffix behaviour is per-course, not per-prefix.** PGY and IND happen to be uniform; RET and
RTE are not. **Always check the specific number against the prefix index** rather than generalizing from a
sibling. The prefix index is one fetch and it settles the whole family at once.

### Batch 75: DSC health-programme clinical ratios differ by programme — a third data point

Adding respiratory care to the collection, which now shows three distinct full-time clinical conventions at
one institution:

| Programme | Course | Credits / hours | Ratio |
|---|---|---|---|
| **Respiratory care** | RET2876 (published), RET1874 | 4 / 240 | **60 hrs/cr** |
| | RET2877 (published), RET1875 | 3 / 180 | **60 hrs/cr** |
| **Occupational therapy** | OTH2840, OTH2841 | 5 / 320 | **64 hrs/cr** |
| **Radiography** | RTE1804L / 1814L / 1824L | 1/128, 2/256, 3/384 | **128 hrs/cr** |
| **Physical therapy** | PHT2810, PHT2820 | 2/240, 2/280 | **120–140 hrs/cr** |

**Never carry a clinical ratio across programmes.** RET is exactly half of RTE. `validate_drafts.py` warned
on RET1875 at 3 cr / 180 hrs — the warning is correct to fire and the value is correct to keep, since it
matches the published RET2877 exactly.

**RTE lecture convention pinned at 16 hrs/credit** — RTE2061 (1/16), RTE2613 (2/32), RTE2385C (3/48) all
agree, so RTE1001 at 1 credit prices to 16, not the usual 15.

### Batch 75: RET2483 resolved from Eastern Florida State via search snippet

**RET2483 "Patient Assessment and Interaction", 2 credits** — absent from DSC's RET listing (25 courses,
verified), and recovered from **Eastern Florida State College's** A.S. in Respiratory Care through a search
snippet. EFSC remains **search-readable but not fetch-readable** (its catalog is JS-rendered and its PDF
variant is empty), consistent with the earlier finding — so scope a web search to `catalog.easternflorida.edu`
rather than attempting WebFetch.

**Also confirmed: DSC's RET prefix has no RET2483 equivalent** — its assessment content is distributed
across other courses rather than carried as a discrete number. Worth recording so it is not re-checked.

### Batch 76: two deferrals, and a new Tier-1 dead end

**AAE0100 and AAE0200 deferred.** `AAE` is **Applied Academics for Adult Education** — the July 2011
redesignation of "vocational-preparatory instruction." The obstacle is structural rather than a lookup
failure: **FLDOE's AAAE curriculum framework uses program S990001 / course S990041-Comprehensive, not
AAE01xx numbering at all**, so the statewide inventory number and the framework number do not correspond.
Absent from DSC current and archived catalogs and from `daytona_courses.csv`; fldoe.org 403s.

> **⚠ New dead end: `catalog.fscj.edu` now returns HTTP 403** to WebFetch, on both the
> `/courses/<numeric-id>` form and `preview_course_nopop.php`. FSCJ was previously ✅ in the URL-pattern
> table for academy clock hours. It still **indexes well**, so scope a web search to the domain instead.
> Table updated.

**Replacement selection tip that saved time:** rather than researching the next queued courses blind, the
efficient move was to pull `next-batch --n 20` and **cross-check the candidates against
`daytona_courses.csv` first**, then pick replacements that are present. Four consecutive ACR/AER PSAV
candidates were all absent from DSC and would each have cost several failed lookups.

### Batch 76: DSC publishes explicit meeting schedules for some studio courses

A rare and useful find. **ART1501C's catalog entry states "Four studio hours weekly"** — an explicit
contact-hour statement, which DSC almost never provides outside the PSAV clock-hour courses.

That gives **3 cr / 60 hrs** directly, and it is worth noting that this **conflicts with the ART family's
published pattern in this repository**, where ART1500C, ART2500C, ART2501C and ART2540C all sit at
**3 cr / 90 hrs** (six studio hours weekly). Both are defensible; the catalog statement is the stronger
evidence for this specific number.

**Practical instruction: check the catalog entry for a meeting-schedule line before deriving studio hours
from the family.** Contact hours vary *within* the ART prefix, so the family ratio is not reliable here.

### Batch 76: RTV is another mixed-suffix prefix, and the third clinical ratio confirmed

**RTV2600C → DSC publishes RTV2600** (3 cr, "Acting for the Lens and Camera"). DSC's RTV listing is
**mixed** in the same way as RET and RTE — it carries RTV1000, RTV1510, RTV2600 unsuffixed while this
repository holds RTV1510C and RTV2100C as C forms. Consistent with the batch-75 correction: **suffix
behaviour is per-course, not per-prefix.**

**Sonography clinical ratio pinned at 120 hrs/credit** — SON1804L and SON1814L (published, 2/240) and
SON2834L (published, 4/480) all agree, so SON2824L at 4 credits prices to **480**. Adding it to the
collection of DSC health-programme clinical conventions, which now stands at five distinct ratios:

| Programme | Ratio |
|---|---|
| Respiratory care (RET) | **60** hrs/cr |
| Occupational therapy (OTH, Level II) | **64** hrs/cr |
| Sonography (SON) | **120** hrs/cr |
| Physical therapy (PHT) | **120–140** hrs/cr |
| Radiography (RTE) | **128** hrs/cr |

**Never carry a clinical ratio across programmes** — the spread is more than two-fold.

### ⚠ ACR deferral — partially recoverable now that FSCJ is back (2026-09-02)

Retrying after the FSCJ recovery found that **FSCJ carries `ACR0002` (Air Conditioning and Refrigeration
Theory II)** — the queue's `ACR0002C` under the usual suffix divergence. Its HVAC/R programme page lists a
clean sequence:

| Course | Hours | Course | Hours |
|---|---|---|---|
| ACR0000 / ACR0000L | 125 each | ACR0001 / ACR0001L | 125 each |
| ACR0012 / ACR0012L | 125 each | ACR0013 / ACR0013L | 125 each |
| ACR0045 / ACR0045L | 175 each | | |

**FSCJ's ACR family runs 125 hours (175 for the advanced course), paired lecture + L lab** — the same
split-publishing structure documented for MSS and PHT. **ACR0062C and ACR0601C were still not found**, so
the cluster remains partially blocked, but `ACR0002C` is now researchable and should be pulled back from
deferral when the queue next reaches it.

### Batch 77: the queue has reached a non-DSC stretch — screen candidates before researching

A workflow finding worth recording, because this will now recur. Of the **first 20 queued IDs**, only
**7 were present in `daytona_courses.csv`**; the rest were PSAV/aviation numbers (ACR, AER, AVS) and
prefixes DSC does not carry.

**The efficient procedure, now standard:**

```
python queue_mgr.py next-batch --n 20     # pull wide
# cross-check every ID against daytona_courses.csv FIRST
# research only the DSC-present ones; defer the rest as a group
```

Screening 20 candidates costs one local script and no web calls. Researching four absent PSAV numbers
costs a dozen failed fetches and produces nothing.

**Eight courses deferred as a group this batch:**
- **ACR0002C, ACR0062C, ACR0601C, AER0033C** — absent from DSC (current + archived), Broward has no ACR
  prefix page (404), Seminole 404s, and **Eastern Florida State's ACR listing carries ACR0022/0060/0061/
  0106/0107 but none of these numbers**. fldoe.org 403s; FSCJ 403s.
- **ART2759, AVS0681, AVS0684, AVS0685** — not at DSC; AVS0xxx are PSAV aviation maintenance numbers
  dependent on FLDOE frameworks.

> **Useful for future ACR work:** EFSC publishes an **HVAC/R Career Technical Certificate totalling 1,350
> clock hours**, with individual courses of **90–150 hours**. That gives a defensible range if a Tier 1
> source ever recovers.

### Batch 77: the 2025–2026 catalog delivered again — and DSC has a new **CAI** prefix

**CAI1320 "AI Application & Prompt Engineering", 3 cr, prereq COP1000** — 404 in 2024-2025, complete entry
in **2025-2026**. Third confirmation of the forward catalog-year technique after RTE3253 and RTE4474.

**`CAI` = Computing and Artificial Intelligence**, subject page `cai-computing-artificial-intel`. It is a
**brand-new DSC prefix**, and `daytona_courses.csv` lists **CAI1320 without the C** while the queue carries
CAI1320C — the usual divergence. Expect more CAI numbers in the queue; **go straight to 2025-2026 for this
prefix** rather than trying the working year first.

**Standing rule now firm:** when a course is in `daytona_courses.csv` but 404s in 2024-2025, try
**2025-2026 before anything else**. It has resolved three of three.

### Batch 77: ART contact hours vary *within* the prefix — do not use a family ratio

Confirmed across six DSC ART courses now, and it contradicts the usual approach:

| Course | Credits | Hours |
|---|---|---|
| ART1500C, ART2500C, ART2501C, ART2540C, **ART2754C**, **ART2755C** | 3 | **90** |
| **ART1501C** (catalog states "Four studio hours weekly"), **ART2752C**, **ART2753C** | 3 | **60** |

**Two distinct studio conventions coexist in one prefix at one institution**, and the only reliable signal
is the catalog's own meeting-schedule line where it exists. `validate_drafts.py` warns on both 60 and 90
against its 45/60 expectation; the warnings are correct to fire and both values are correct to keep.

**Practical instruction: for ART, price each number individually** — check for a meeting-schedule statement,
then fall back to the direct prerequisite's published value (ART2753C follows ART2752C at 60; ART2755C
follows ART2754C at 90), never to a prefix-wide average.

### Batch 77: AFR — a mandatory lab without a C suffix

**AFR3221 is published unsuffixed at 3 credits** and its description states **"a weekly leadership
laboratory is mandatory."** Its sequence partner **AFR3220C is published in this repository at 3 cr / 75
hrs**, so AFR3221 prices to 75 as well.

Worth recording as a caution: **the absence of a C suffix does not mean the absence of a laboratory
component.** The suffix is a numbering convention, not a reliable description of course structure — check
the description for a stated lab or meeting requirement before assuming a plain lecture ratio.

### Batch 79: the 2025–2026 catalog technique is now 5-for-5

**`DIG2510` "Business Practices for Creative Industries"** does not exist in DSC's 2024–2025 catalog and
**is published in 2025–2026** at 3 credits, fall and spring, with a description that explicitly names
**NFTs**. That makes the running score for the forward-catalog technique **5/5**: RTE3253, RTE4474,
CAI1320, DIG2510, and the CAI prefix as a whole.

**Standing procedure confirmed:** when a queue ID returns nothing from the current DSC catalog year,
try **both directions before deferring** — `2019-2020` for discontinued courses, `2025-2026` for
newly-added ones. Two extra fetches; a 100% recovery rate so far on the forward direction.

Content note worth keeping for any future guide that touches tokenized assets: the honest account is
neither hype nor dismissal. **An NFT is a token pointing at an asset; buying one does not by itself
transfer copyright**, the speculative market collapsed after the early-2020s peak, and the durable
teaching is the *evaluation* skill — who takes custody, what rights actually transfer, what happens if
the platform closes, how you get paid, what the fees are. Those questions apply to every new creative
marketplace, which is what makes the topic worth teaching at all.

### Batch 79: when a family is mixed, price from the **direct prerequisite**, not the family average

**`DES1054` "Pain Control and Anesthesia"** is published at DSC at **2 credits** with prerequisite
**DES1010**, and DES1010 is published at **2 cr / 30 hrs**. The DES prefix is *not* uniform — this
repository has already corrected **DES1100C to 3 cr / 60 hrs** and **DES1200C to 3 cr / 75 hrs**
(batch 46), both lecture-plus-lab. Averaging the prefix would have produced a wrong number.

**Rule:** in a mixed prefix, the **stated prerequisite is the closest structural relative** — it is by
definition in the same programme, the same term sequence, and usually the same delivery format. Prefer
it over a family ratio whenever both are available. This is a narrower and more reliable version of the
"fetch the family" habit, and it is consistent with the batch-74 correction that the lecture+lab identity
is structural rather than numerical.

**`DEH1133` was priced the other way** — the DEH family is genuinely uniform at **16 hrs/credit**
(published DEH1602 = 3 cr / 48 hrs), so 3 cr → 48. Use a family ratio **only after checking that the
family actually is one**.

### Batch 79: the COS PSAV lab block is flat at 240 hours

**COS0083L and COS0084L** (Cosmetology IV and V Lab) resolve to **0 credits / 240 clock hours** each,
matching the already-published **COS0080L, COS0081L, and COS0082L** — five consecutive labs at the same
value, each carrying a **$110.75 lab fee**. This is the cleanest flat family found in a PSAV prefix so
far; contrast the PHT and DES cases above, where within-prefix variation is the norm.

Licensure framing to reuse for any Chapter 477 course: **the hours are the licensure requirement**, not
merely a credit-equivalence convention. A cosmetology student who misses hours does not lose credit —
they lose eligibility, because the Florida Board of Cosmetology counts the clock. That makes attendance
a regulatory matter rather than a policy matter, and guides for 0-credit PSAV courses should say so.

### Batch 80: ⚠⚠ **EET4732C vs EET4732 — different subjects under the same digits**

The sharpest number-versus-title trap found so far in a technical prefix, and cleanly documented
from two catalogs:

| Institution | Number | Title | Credits |
|---|---|---|---|
| **Miami Dade** | **EET4732C** | **Signals and Systems** | 4 |
| **Miami Dade** | **EET4730C** | **Feedback Control Systems** | 4 |
| **Daytona State** | **EET4732** (no suffix) | **Feedback Control Systems** | 3 (+ EET4732L) |
| **Valencia** | **EET3732** | **Linear Control Systems** | 3 |

So **4732 means signals-and-systems at one college and feedback-control at another**, and the
college that uses 4732 for signals reserves **4730C** for control. These are genuinely different
subjects — signals/systems is convolution, Fourier, sampling; feedback control is root locus,
compensation, gain and phase margin — sharing only the transfer function.

**Rule 22 is what permits this without either institution being wrong**: the suffix is part of the
course number and SCNS equivalency does not cross it. **Identify a course by its catalog
description, never by its number or by a repository guide's title.**

Same batch, same prefix, three more divergences:
- **EET3716C** = "Advanced System Analysis," **4 cr** (MDC, prereqs EET1025C + MAC2312) vs
  **EET3716** = "Network Analysis," **3 cr** (DSC). Title, credits, and prerequisite chain all differ.
- **EET3086C** = "Circuit Analysis," **4 cr, 3 lec + 2 lab** (Valencia) vs **EET3086** =
  "Principles of Electrical Circuits," **3 cr** (DSC).
- **EGS1000** = "Professional Performance for Technicians," **3 cr** (DSC) vs
  "Introduction to Engineering Technology I," **1 cr** (FAMU). **A 3:1 credit ratio on one number** —
  the widest relative spread recorded here.

### Batch 80: MDC and Valencia program-sheet PDFs are a high-yield source — extract them locally

`WebFetch` returns MDC's program sheets as raw PDF bytes and the summarizing model correctly
refuses to guess. **The fix is to read the saved file with `pypdf` locally**, which is installed:

```
r = pypdf.PdfReader(saved_path)
text = '\n'.join(p.extract_text() or '' for p in r.pages)
```

One PDF (`mdc.edu/academics/programs/ps/S9100.pdf`) yielded **the entire ECET B.S. course list with
titles, credits, and prerequisites** — seventeen courses in one fetch, including the EET4730C/4732C
distinction above that no HTML catalog page would have shown. WebFetch already saves the binary and
prints the path; use it.

**Added to the source registry:**

| Source | Pattern | Status |
|---|---|---|
| Miami Dade program sheets | `mdc.edu/academics/programs/ps/<CODE>.pdf` | ✅ PDF — extract locally |
| Miami Dade course sequence guides | `www3.mdc.edu/academics/programs/csg/<NAME>_csg.pdf` | ✅ PDF — extract locally |
| Seminole State | `seminolestate.edu/catalog/courses/<courseid-lowercase>` | ✅ (confirmed again) |
| Valencia | `catalog.valenciacollege.edu/coursedescriptions/coursesoffered/<prefix>/` | ✅ **publishes explicit lecture/lab hour splits** |

**Valencia is now the preferred source for contact hours.** Its prefix pages give credits *and* the
lecture/lab split per course, which means hours can be **read rather than derived** — EET3086C's 75
hours came from its published `3 lec + 2 lab`, not from a ratio.

### Batch 80: the direct-prerequisite pricing rule fired again, immediately

Recorded in batch 79; used twice here.

- **EET1021C** (DSC, 3 cr, "Advanced Electrical Circuits and Lab") prices from its published
  prerequisite **EET1011C, live in this repository at 3 cr / 75 hrs** — same prefix, same programme,
  same "and Lab" structure, same college. → **75**. The validator warns on 3 cr/75 hrs and the
  warning is correct to ignore here: the number is the family's, not a derivation.
- **EET3716C and EET4732C** price from **EET4158C**, live at **4 cr / 80 hrs**, which sits in the
  *same MDC prerequisite chain* (EET3716C → EET4158C, and EET3716C → EET4732C). → **80**.

**Generalization worth keeping:** the best hour source, in order, is
**(1) a catalog's own published lecture/lab split**, **(2) an already-published guide for a course in
the same prerequisite chain at the same institution**, **(3) a prefix ratio — only after confirming
the prefix is actually uniform.** Batch 79 established (3)'s caveat; this batch establishes that (2)
beats (3) whenever a prerequisite or immediate successor is already live.

### Batch 80 — open correction candidate: `EET1025C`

Published here as **"A/C Circuits," 3 credits / 90 contact hours**. Two independent catalogs
disagree with the hours, in different directions:

- **Valencia**: EET1025C = **3 credits, 2 lecture + 2 lab → 60 contact hours**.
- **Miami Dade**: EET1025C = **4 credits** ("Alternating Current Circuits," prereq EET1015C).

**90 hours at 3 credits is outside the family**: the repository's own EET1011C is 3/75, EET1084C is
3/60, and Valencia's whole EET C-suffixed family runs 3 cr at 2+2 = 60. Nothing found supports 90.
Recommend reviewing toward **3 cr / 60 hrs** with a stated note that Miami Dade carries the number at
4 credits. Same class as the ASL and ART hour corrections — an internal-consistency outlier, not an
external fact. Awaiting Ron's go-ahead.

### Batch 81: the corequisite is as good a pricing anchor as the prerequisite

Batch 79 established "price from the direct prerequisite"; batch 80 refined the hierarchy. This batch
adds the **corequisite** to the same tier, and it produced the tightest match yet:

- **FSS1222C** lists **FOS1201 and FSS1202C as corequisites**, and **FSS1202C is live at 3 cr / 60 hrs**.
  Same college, same prefix, same term, same integrated lecture-plus-lab structure. → **60**.
- **FOS1142 / FOS2147** price against the live **FSS1063C "Baking," 3 cr / 60 hrs** — the same bakeshop,
  the same credit value, the same **$150 lab fee**. → **60**; **FOS2161** at 4 cr scales to **80**.
- **EVS2026C** (4 cr, C-suffixed) prices against the live pair **EVR2001 (3/45) + EVR2001L (1/45)** —
  **the same college's own lecture-plus-lab split at the same total credit value**. → **90**.

That last one is worth naming as a technique in its own right: **when a C-suffixed course has no
published hour split, look for the same institution's unsuffixed lecture + L lab pair at the same
total credits and add them.** It is the batch-74 "structural not numerical" rule used in the
direction it *does* work — not to derive one number from another within a family, but to price an
integrated course against a same-college split pair of identical credit value.

**Lab fees are a usable signal of course type.** Every FOS/FSS production course in this batch carries
an identical **$150** fee, which confirms they are the same kind of course before a single description
is read. EVS2026C's **$88.29** — an oddly precise figure — marks a consumables-based science lab.
Extends the batch-74 lab-fee finding.

### Batch 81: `FSS1242` is queued unsuffixed; DSC publishes `FSS1242C`

Another Rule-22 case, and the reverse direction from batch 80's: here the **statewide inventory carries
the unsuffixed number** while **Daytona State publishes the C-suffixed one** ("International Cuisine and
lab," 3 cr, prereq FSS1222C, $150 fee). The guide is filed under the queue's `FSS1242` with the
divergence flagged in the guide body.

Running tally of suffix divergences in the last two batches: **EET3085C/EET3085+L, EET3086C/EET3086,
EET3716C/EET3716, EET4732C/EET4732, ETG3533C/ETG3533+L, FSS1242/FSS1242C.** Six in sixteen courses.
The screening script's `alt:` column is now the most valuable thing it prints — **it predicts which
guides will need a suffix flag before any research happens.**

### Batch 81: EVR2647 is the most job-shaped 2000-level course found so far

**Environmental Site Assessment** teaches a defined professional deliverable performed to a published
standard: **ASTM E1527** Phase I in conformance with EPA's **All Appropriate Inquiries rule
(40 CFR Part 312)**, and **ASTM E1903** Phase II. Its prerequisite set is unusually specific —
**CHM1025C + EVR2001 + EVR2001L + GIS2040C** — and each is genuinely used.

**Two things worth carrying to any future guide in this space:**

1. **Rule 11 fires hard here.** The Phase I standard has been revised repeatedly (**E1527-13 →
   E1527-21**) and EPA rulemaking governs which version satisfies AAI. **A report to the wrong version
   does not support the CERCLA landowner liability defence** — which is the entire point of doing it.
   Verify the current version and EPA's recognition of it before relying on anything.
2. **The "environmental professional" definition at 40 CFR 312.10 is a scope boundary students must be
   told about.** Completing this course does not make anyone an EP; the definition requires a PE/PG
   licence plus experience, or a relevant degree plus specified years. Same class of scope flag as the
   DES1054 dental-assistant delegation boundary and the Ch. 471 "engineer" boundary in EGS1000.

**Florida-specific sources added to the registry** (all free, all fetchable):

| Source | What it gives |
|---|---|
| `floridadep.gov` — **Ch. 62-777 F.A.C.** | **Cleanup Target Levels** — the numbers Florida results are compared against, not the federal ones |
| `floridadep.gov` — **Ch. 62-780 F.A.C.** | contaminated site cleanup process |
| `floridadep.gov` — **Ch. 62-302 F.A.C.** | surface water quality standards and classifications |
| **DEP OCULUS** / **DEP Map Direct** | document + GIS portals — the working records-review tools |
| **DEP WIN/STORET** | Florida monitoring data |
| **UF Aerial Photography: Florida (APF)** | historical aerials — Florida coverage is unusually good |
| **FWC Fish and Wildlife Research Institute** | red tide / HAB status |
| **Florida LAKEWATCH** (UF/IFAS) | volunteer monitoring — real experience, résumé-visible |

Florida's **karst + shallow water table + petroleum-tank legacy + drycleaning solvent programme** make
site assessment and water chemistry genuinely distinctive here, and that local knowledge is the
employable part. Worth reusing in any EVR/EVS/GLY guide.

### Batch 82: ⚠⚠ the SmartCatalog "Credit Hours" field lies on 0000-level courses

**The most important operational finding in a while, and it is a live trap for this pipeline.**

Daytona State's SmartCatalog pages render a field labelled **"Credit Hours"** for every course. On
**0000-level PSAV courses that field contains clock hours**, not credits:

| Course | Page says | Truth |
|---|---|---|
| **HCP0750C** Phlebotomy Technician | "Credit Hours: **75**" | **0 credits / 75 clock hours** |
| **HSC0005** Healthcare Concepts for the Massage Therapist | "Credit Hours: **55**" | **0 credits / 55 clock hours** |

Taken at face value these become `credits: 75` and `credits: 55` — **both above the validator's 0–12
ceiling**, so `validate_drafts.py` would have caught them. But the same trap at a *plausible* value
(a 3-credit-looking "Credit Hours: 3" that is really 3 clock hours, or an 8) **would pass validation
silently.** `Tools/CLAUDE.md` already warns that this exact mistake "stalled 11 guides for months."

**Standing rule, now explicit:** *any* course whose SCNS number is **0000-level is PSAV**. Set
`credits: 0` and put the catalog's number in `contact_hours`, **regardless of what the field is
labelled.** Do not reason from the label; reason from the number's first digit.

### Batch 82: the PSAV block is now a reusable component

Both PSAV guides share a standing block covering what a 0-credit clock-hour course means for the
student: **hours are a completion requirement not a policy**, **PSAV does not transfer as general
education**, **articulated credit toward a related A.S. exists at some colleges and must be asked for
in writing**, **financial aid is calculated differently for clock-hour programmes**, and **the
credential rather than the transcript is the point.** Reuse it for every 0000-level guide.

### Batch 82: "does Florida license this?" is a question with a surprising answer often enough to always ask

Three health-adjacent courses in one batch, three completely different regulatory answers:

- **Phlebotomy (HCP0750C): Florida does NOT license phlebotomists.** Unlike California, no state
  licence is required to draw blood here. **But certification is what employers screen on** —
  PBT(ASCP), CPT(NHA), RPT(AMT) — so the practical advice is the opposite of what the legal answer
  suggests. A guide that stopped at "no licence required" would mislead.
- **Massage therapy (HSC0005): licensed under Ch. 480 F.S.**, Board-approved school required, MBLEx
  examination, background screening, **and Florida-specific human-trafficking awareness training and
  establishment signage requirements** — the trafficking angle is why this profession carries
  regulatory scrutiny others do not, and it belongs in the guide.
- **Sports nutrition (HUN1270): Ch. 468 Part X F.S. licenses dietitians**, so the *course* is
  unrestricted but *acting on it* is bounded — individualized medical nutrition therapy is a licensed
  activity and an online "sports nutrition certification" confers no authority.

**Rule to keep: never assume the licensure answer from the occupation's clinical seriousness.**
Ask the specific question for each Florida profession, and state both the legal answer and the
practical employer answer, because they diverge.

### Batch 82: a recurring cross-guide pattern is now worth naming — the **scope boundary flag**

Six guides in three batches have carried a version of the same warning, and it is the same shape
every time: *here is the thing this course qualifies you to do, and here is the line past which you
need a different credential.*

| Guide | The boundary |
|---|---|
| **DES1054** (b79) | Florida dental assistants may not administer anesthesia; Ch. 466 delegation rules |
| **EGS1000** (b80) | Only a licensed PE may offer engineering services (Ch. 471) |
| **EVR2647** (b81) | 40 CFR 312.10 "environmental professional" requires PE/PG + experience |
| **HCP0750C** (b82) | Phlebotomists do not interpret results — refer to the provider |
| **HSC0005** (b82) | Massage therapists do not diagnose, prescribe, or advise against treatment |
| **HIM2430** (b82) | **Coders do not diagnose** — never code from a lab value; use a non-leading query |
| **HUN1270** (b82) | Only licensed dietitians may provide individualized nutrition therapy |

**Write this flag into every guide for a course that sits below a licensed profession.** It is the
single most consequential thing an applied-programme guide can tell a student, and it is exactly what
programme marketing tends to leave out.

### Batch 82 — HIM2430 and the honest automation framing

Worth reusing wherever a course trains for work that software is encroaching on. Computer-assisted
and AI-assisted coding are in wide use; **the honest framing is that routine coding is being automated
while complex inpatient coding, CDI, auditing, and analytics are not** — so the guide points students
at the judgement-requiring parts rather than either ignoring the shift or catastrophizing it. Same
approach as the DIG2151 treatment of AI and content writing (b79) and the DIG2510 treatment of NFTs.

### Batch 83: the validator caught a reasoning error, not a typo — worth recording

`IND2410C` was drafted at **3 cr / 45 hrs**, priced from Daytona State's **unsuffixed IND2410**
(3 cr, prereq IND2408, summer, $15 fee). `validate_drafts.py` flagged it:

```
WARN  IND2410C
        warning: 'IND2410C' is an integrated lecture+lab (C) course but has only 45 contact hours
```

**The warning was right and the reasoning was wrong.** The guide is filed under the *C-suffixed*
number, and the C suffix is precisely the marker of an integrated laboratory. Pricing it from the
unsuffixed sibling imported the one property the suffix exists to distinguish. Corrected to **60**,
with the guide body now stating that the estimate reflects the integrated studio rather than DSC's
unsuffixed listing.

**Rule this generalizes to:** when the queue ID and the DSC entry differ by suffix, **the DSC entry is
evidence about content, not about structure.** Take title, prerequisites, terms, and subject matter
from it; take **credit-and-hour structure from what the queue's own suffix implies**, or defer.

This is the first time the validator has caught a *judgement* error rather than a field-format error,
and it is a good argument for never pushing past a warning without reading it.

### Batch 83: design-studio hours are not derivable — say so in the guide

DSC publishes IND credit values with **no lecture/studio hour split**, and the prefix is internally
inconsistent in exactly the way batch 77 documented for ART. Three data points from one college:

| Course | Credits | Lab fee | Character |
|---|---|---|---|
| **IND1300** Graphics of Interior Design I | 3 | **$132** | materials-intensive rendering studio |
| **IND2220** Commercial Interior Design | 3 | $15 | project/documentation studio |
| **IND2410** Kitchen and Bath Design I | 3 | $15 | project studio |
| **IND2500** Professional Practices (already live) | 3 | — | **3/45 — lecture** |

The **$132 vs $15** split is the signal (batch-81 lab-fee finding again): IND1300 consumes markers,
board and paper; the others do not. Priced IND1300 at **60**, the project courses at **45**, and the
C-suffixed number at **60**.

**New reusable block added to the guides:** a standing *"check the scheduled studio hours"* warning
stating plainly that **the repository's figure is an estimate for planning, not a published number**,
that studios meet more hours per week than their credit value implies, and that students should read
the section schedule before registering. Honest hedging beats a confident wrong number, and this is
the right pattern wherever a catalog publishes credits without a split.

### Batch 83: a certification named in a catalog may not be one a student can sit

**MAN4535** states it "prepares students for the internationally recognized Professional in Business
Analysis (PMI-PBA) certification exam by Project Management Institute **based on experience**."

That last clause matters: **PMI-PBA requires several thousand documented hours of business analysis
experience**, so a student finishing this course is prepared for the *content* and generally **not yet
eligible to sit the exam**. The guide says so plainly and points to **IIBA's ECBA**, which has **no
work-experience requirement** and is the credential a student can actually obtain now.

**Standing check for any guide naming a certification:** verify the *eligibility* requirements, not
only that the exam exists. Same class of finding as the batch-82 phlebotomy result — the legal or
formal answer and the practically useful answer diverge, and the guide should give both. Recurring
cases so far: **PMI-PBA (experience-gated), NCIDQ (CIDA-accredited degree required — an A.S. will not
satisfy it), RHIT (CAHIIM accreditation required), CDA/CCS, NKBA AKBD (no degree required — the
unusually accessible one).**

### Batch 83: FSCJ is unreachable again — new failure mode, not a 403

```
https://floridastatecollegecatalog.fscj.edu/... → certificate has expired
```

Distinct from the bot-filter 403s documented above: **this is a TLS certificate expiry on the catalog
host**, which is an operational fault at FSCJ rather than a block against us. It is likely to be fixed
without any action on our part. **Retry it next session** — same standing guidance as the 403s: not a
permanent dead end, and deferred courses stay provisional.

Source-registry status updated: `catalog.fscj.edu` ✅ (recovered batch 78) but
`floridastatecollegecatalog.fscj.edu` ⚠ **expired certificate as of 2026-09-02**.

Also confirmed this batch: **`catalog.valenciacollege.edu/coursedescriptions/coursesoffered/<prefix>/`
returns 404 for prefixes Valencia does not teach** (`/ind/` 404s) — a clean negative, not an outage.
Useful: a 404 there is reliable evidence the prefix is absent rather than a fetch failure.

### Batch 84: the clock-hour trap is now confirmed *in the catalog's own prose*

Batch 82 inferred that SmartCatalog's **"Credit Hours"** field carries clock hours on 0000-level
courses. This batch found the catalog saying so explicitly. **MEA0801** renders as
**"Credit Hours: 240"**, and its description reads:

> *"They will be responsible for **240 hours** of hands-on practical in physician's offices, clinic
> settings and urgent care facilities."*

**The prose and the field agree, and the prose says "hours."** That closes the question. Seven of this
batch's eight courses were 0000-level, with field values of **189, 120, 240, 70, 40, 18, and 62.5** —
every one a clock-hour count, every one written as `credits: 0`.

**Two of those would have passed the validator if taken literally.** `18` and `40` are inside the
0–12… no — `18` and `40` exceed 12 and would have been caught. **But `62.5` would have failed on the
integer rule, and a value of 8 or 10 would have sailed through silently.** The screening rule stands
and is now evidence-backed: **first digit 0 ⇒ PSAV ⇒ `credits: 0`, regardless of the field label.**

### Batch 84: MSS0804 is a third half-hour PSAV figure — the pattern is systematic

**62.5 clock hours**, published exactly. Third confirmed instance after **MSS0803L (75.5)** and
**PRN0004C (457.5)**, and the second in the MSS prefix.

**Handling, now standard:** round to the integer for the `contact_hours` field, and **state the exact
catalog figure in the guide body with an instruction to use it for licensure hour-counting.** In a
licensed clock-hour profession the half-hours genuinely add up — Florida's Board of Massage Therapy
sets a total programme hour requirement, and a therapist totalling their transcript needs the real
number, not the rounded one.

**Generalization worth keeping:** in PSAV health programmes the hours are **the licensure
requirement**, not a credit-equivalence convention. The PSAV block in these guides now says so
directly for MSS courses, which is a stronger claim than the generic version used for MEA (where
Florida licenses nobody).

### Batch 84: two CSV title errors found — `daytona_courses.csv` is a screening index, not a source

| Course | `daytona_courses.csv` says | 2025–2026 catalog says |
|---|---|---|
| **MSS0157** | "Anatomy and Physiology Massage Therapist **I**" | "…Massage Therapist **II**" (prereq **MSS0156** confirms) |
| **MEA0310C** | "Clerical Procedures for Medical Assisting" | "Clerical Procedures for Medical Assisting **and Lab**" |

Neither is fatal — the CSV's job is the `IN`/`--` screening decision, which it did correctly both
times — but **titles from the CSV must never be written into a guide unverified.** The MSS0157 case is
the dangerous shape: a I/II error would have produced a guide describing the wrong course in a
sequence, which is the **MAN3554 wrong-subject failure mode** in miniature.

**The reliable disambiguator is the prerequisite chain**, exactly as recorded for the PHT2810/2820
roman-numeral trap: *sequence by SCNS number and prerequisite, never by the numeral in a title.*
MSS0157 lists **MSS0156** as its prerequisite, so it is unambiguously the second course.

**Procedure update:** the CSV is authoritative for *presence*; the catalog is authoritative for
*title, credits, hours, prerequisites, and terms.* Never skip the fetch because the CSV title looks
sufficient.

### Batch 84: the "does Florida license this?" question, twice more — opposite answers in one batch

Continuing the batch-82 finding, this batch put the two answers side by side:

- **Medical assisting (MEA): NOT licensed in Florida.** Medical assistants work purely on delegation
  from a licensed practitioner. **Scope is set by what is delegated, not by the certificate** — so a
  credential does not expand scope, and "I'm certified" is not authority. The employer-facing answer
  is still that certification matters: **CMA (AAMA) requires a CAAHEP- or ABHES-accredited
  programme**, which is a decision that must be checked *before* enrolling and cannot be fixed after.
- **Massage therapy (MSS): licensed under Ch. 480 F.S.**, Board-approved school required, MBLEx,
  background screening, mandatory human-trafficking CE and establishment signage.

**Same batch, same college, same PSAV level, opposite regulatory regimes.** The rule holds: never
infer the licensure answer from how clinical the work looks.

### Batch 84 — MGF2130 and a general-education trap worth flagging in every MGF/MAT guide

**MGF is quantitative-reasoning general education, and it is *not* a prerequisite for anything.**
MGF2130 satisfies a mathematics requirement for many A.A./A.S. programmes and **does not lead to
MAC1105, STA2023, or the calculus sequence.** A student who takes it and later moves to business,
nursing, engineering, or a science starts the mathematics sequence from the beginning — a lost term
or more.

Second Florida-specific item: **developmental education is optional for many Florida students** under
the state's developmental-education statute (recent Florida public high school graduates and
active-duty military among the exempt), so the published MAT0022/MAT0028C/MAT0056L prerequisites are
**bypassable by a large share of enrollees**. Guides for MGF/MAT/STA courses should say both things:
*exempt means you may choose, not that you are prepared*, and **co-requisite support is usually the
better option than a separate developmental sequence.**

Also noted: MGF2130's **$63 fee is courseware, not laboratory materials** — the guide tells students
to find out what the fee includes before buying a separate textbook, since these fees typically bundle
an e-text. New use for the lab-fee signal: **on a lecture course, a fee in the $50–$100 range usually
means online courseware.**

### Batch 85: the MSS half-hour figures are a *pattern*, not scattered oddities

Fourth confirmed half-hour PSAV figure, and the MSS practicum pairs now resolve completely:

| Course | Catalog hours | Role |
|---|---|---|
| **MSS0803** | (theory) | first practicum term |
| **MSS0803L** | **75.5** | first practicum lab |
| **MSS0804** | **62.5** | second practicum term |
| **MSS0804L** | **75.5** | second practicum lab |

**The two laboratories carry the identical 75.5**, and in both terms **the lab is larger than its theory
partner** — 75.5 against 62.5, for a 138-hour pair. That proportion is correct for a psychomotor
profession and is worth stating in the guides, because it tells students where the work actually is.

**Standing handling, now settled:** round for the `contact_hours` field, and **state the exact catalog
figure in the guide body with an instruction to use it for licensure hour-counting.** In a licensed
clock-hour profession the half-hours accumulate against a Board-set programme total, so the rounded
number is the wrong one for a student totalling a transcript.

### Batch 85: guide-to-guide prerequisite links are now appearing inside the corpus

**NUR1005C lists `MGF2130` as a prerequisite** — a course written and pushed in the *previous batch*.
That is the first time a newly-written guide's prerequisite chain has pointed at another guide written
in this session, and it is a useful confirmation: **the MGF2130 guide warns at length that the course
does not lead to College Algebra or Statistics and that students must check what their programme
requires.** DSC's nursing programme accepts it as the mathematics prerequisite — which is exactly the
kind of programme-specific answer that guide tells readers to go and get.

**Worth watching for deliberately.** As the corpus fills, prerequisite chains increasingly resolve to
guides that already exist, and cross-referencing them makes both guides better. The related-course
check (see the pattern section below) should now include: **does this course's prerequisite or
corequisite already have a live guide, and do the two agree?**

### Batch 85: nursing contact-hour ratio pinned at 32 hrs/credit

**NUR1020C** is live at **5 cr / 160 hrs**. **NUR1005C** at **8 credits** therefore prices to **256**.

That is a **32 hours-per-credit** ratio — much higher than the 15 (lecture) or 20 (integrated C) norms,
and correct for a course combining lecture, skills laboratory, and clinical placement. It slots into
the clinical-ratio table alongside the five already recorded (RET 60, OTH 64, SON 120, PHT 120–140,
RTE 128) as **the lowest of the clinical-bearing ratios** — which makes sense, since NUR1005C is
mostly classroom and laboratory with clinical attached, rather than a pure clinical rotation.

**The standing warning still applies: never carry a clinical ratio across programmes.** This is a
same-college, same-prefix, same-structure derivation, which is the only kind that holds.

### Batch 85: `OCE1001L` — a catalog that tells you a course is *optional*

Unusual and worth recording. DSC's description states the laboratory **"serves as an optional component
for OCE1001,"** aimed at A.A. transfer tracks in marine science, marine biology, environmental science,
and ocean engineering.

**That single word changes the advice a guide should give**, and it cuts both ways:

1. **Many Florida general education requirements specify a *laboratory* science** — so for a student
   using oceanography as their gen-ed science, the lab may not be optional at all.
2. **Receiving institutions frequently require the lab for a science major** — and adding it after
   transfer is more expensive and more disruptive.
3. **Under SCNS, `OCE1001` and `OCE1001L` are distinct courses.** A transcript showing only the lecture
   has not satisfied a requirement for the lab.
4. **DSC offers it spring only**, so a missed year is a real cost.

The guide's advice is therefore *take it unless you have written confirmation you don't need it.*
**Generalizable: whenever a catalog describes a component as optional, the guide's job is to identify
who it is not optional for.**

### Batch 85: a third "no C suffix but a lab is required" case — the pattern is now established

**MUM1622** ("Outside lab/field work is required") and **MUM2611** ("Field work required") both state a
laboratory requirement in prose while carrying no `C` suffix. Priced at **60** rather than a
lecture-equivalent 45; **MUM2607**, which states no such requirement, stayed at **45**.

Running list of this pattern: **AFR3221** (batch 77, "a weekly leadership laboratory is mandatory"),
**FSS1287** (batch 82, "learn in the classroom and lab"), and now **MUM1622** and **MUM2611**.

**Standing rule, now four cases deep:** *the absence of a C suffix is not evidence of the absence of a
laboratory.* **Read the description for a stated lab, field, studio, or clinical requirement before
applying a lecture ratio** — the suffix is a numbering convention and the description is the
description. The inverse also holds (batch 83's `IND2410C`): **a C suffix is evidence a lab exists even
when the local catalog publishes the unsuffixed sibling.**

### Batch 85 — deploy verified, pending queue now empty

Ron deployed 2026-09-02 (second deploy of the day). The **`v@Model.Guide.Version`** literal-render fix
is confirmed live: `ACG2021C`, `PRN0090C`, and `MSS0804` guide pages all render **`v1.0`**, and
`grep -c 'v@Model'` returns **0** on each. `Deployment/PENDING_SERVER_CHANGES.md` now reads
**"Nothing is currently pending."**

### Batch 86: the scope-boundary flag now has a *shape*, and it repeats across professions

Batch 82 named the pattern. This batch produced three instances in one push, and they are close to
identical in structure — which makes the flag a template rather than a per-guide judgement:

| Guide | Who evaluates / decides | Who implements | Statute |
|---|---|---|---|
| **OTH1114C, OTH2261C, OTH2520C** | the **OT** evaluates, interprets, establishes the plan of care | the **OTA** contributes to evaluation and implements | Ch. 468 Pt III, F.S. |
| **PHT1251L** | the **PT** evaluates, interprets, establishes the plan of care | the **PTA** implements; data collection yes, interpretation no | Ch. 486, F.S. |
| **OST1435** | only a **member of The Florida Bar** may advise, select documents, set fees, represent | non-lawyers may do substantial work **under attorney supervision** | UPL rules, Fla. Sup. Ct. |

**The template, now explicit:** *X evaluates and decides; Y contributes data and implements; Y may not
initiate, alter, or terminate; supervision requirements are set by rule and by payer and differ by
setting; "my employer told me to" is not a defence.*

**Two additions this batch worth carrying:**

1. **The credential does not expand the scope.** Stated in the MEA guides (batch 84) and it generalizes:
   certification proves competence, delegation confers authority, and students conflate them.
2. **UPL has a Florida-specific sharpener.** Florida has **no intermediate "legal document preparer"
   licence** of the kind some states have, so the boundary is harder here than elsewhere — and the
   **"notario" problem** (a Florida notary public is not a lawyer; the term means something different
   in other legal traditions) is an active Florida enforcement area worth naming in any legal-support
   guide.

### Batch 86: ⚠⚠ correcting the traditional "body mechanics" advice in patient-handling guides

**A substantive content correction, not a data one.** Rehabilitation and nursing programmes have
traditionally taught that correct body mechanics make manual patient lifting safe. **The evidence does
not support that**, and the guides written here now say so directly:

> *"Body mechanics alone are not sufficient protection… no amount of correct lifting technique makes
> manually lifting an adult human safe. The weight simply exceeds what a spine tolerates."*

The guides therefore lead with **equipment** — mechanical lifts, sit-to-stand devices, slide boards,
friction-reducing sheets, gait belts — and treat body mechanics as necessary-but-insufficient. Also
recorded: **never catch a falling patient**; guide the controlled descent instead. Attempting to arrest
a fall injures the clinician and frequently injures the patient worse.

**Why this matters for the corpus:** musculoskeletal injury from patient handling is the leading
occupational injury in these fields and the classic career-ender. **Reuse this block for every OTH,
PHT, NUR, HCP, and MSS guide involving patient transfer.** It is one of the few places where a guide
can be more useful than the textbook the student was assigned.

### Batch 86: PGY is confirmed unsuffixed at DSC — and the studio-hours estimate needs saying out loud

Batch 73 recorded that **PGY is a whole prefix published without suffixes at DSC**. This batch confirms
it across three more numbers (**PGY1101, PGY2270, PGY2650** — all unsuffixed) while the lab fees say
plainly what kind of course each is:

| Course | Credits | Lab fee | Read as |
|---|---|---|---|
| **PGY1101** Photography as an Art Form | 3 | **$75** | materials-intensive studio |
| **PGY2650** Photography II: Concept and Narrative | 3 | **$90** — highest in prefix | production-intensive studio |
| **PGY2270** Field Survey | 2 | none listed | survey/orientation — **priced at 30, lecture ratio** |
| **PGY2801C** (already live) | 3 | — | **3 / 60** — the C-suffixed benchmark |

Priced the two studios at **60** against the live PGY2801C, and the survey at **30**. The
**"no C suffix but a lab exists"** list is now six deep: **AFR3221, FSS1287, MUM1622, MUM2611, PGY1101,
PGY2650** — and the lab-fee signal has correctly predicted every one.

Added a reusable **PGY suffix block** stating that the figure is an estimate benchmarked against
PGY2801C, that studios meet more hours than credits imply, and that **SCNS equivalency does not cross
the suffix** so `PGY####` and `PGY####C` are distinct courses with portfolio review likely on transfer.

### Batch 86: accreditation is the gate, and it belongs above transfer in every allied-health guide

Third and fourth instances of the same structure, now consistent enough to state as a rule:

| Field | Accreditor | Then | Then |
|---|---|---|---|
| Occupational therapy assisting | **ACOTE** | **NBCOT** exam | Ch. 468 Pt III licence |
| Physical therapist assisting | **CAPTE** | **NPTE-PTA** | Ch. 486 licence |
| Health information (b82) | **CAHIIM** | **RHIT** | — |
| Medical assisting (b84) | **CAAHEP/ABHES** | **CMA (AAMA)** | *no Florida licence* |
| Nursing (b85) | **Board approval + ACEN/CCNE** | **NCLEX-RN** | Ch. 464 licence |

**Standing instruction for allied-health guides:** the accreditation sentence goes *above* the transfer
discussion, because **breaking the first link makes everything after it unreachable and it cannot be
fixed retroactively.** Two practical additions the guides now carry: **check the programme's published
examination pass rate** (public, and the single most informative number about a programme), and
**resolve any background-screening history with the Board *before* investing in a programme** — the
mistake that costs students the most.

### Batch 86: OTH2520C — paediatric practice runs on education law, not health law

Worth recording because it changes what a guide must cover. School-based and early-intervention OT is
delivered under **IDEA**, not under a medical-necessity frame:

- **"Educational relevance" is the governing standard**, and it is **narrower than medical necessity** —
  a child may have a real need a school is not obliged to address.
- **The IEP is a legal document**; services are delivered as written.
- **Part C (birth to three)** works differently again — an **IFSP**, family-centred, in **natural
  environments**, delivered in Florida through **Early Steps** on a **coaching model**: *you are largely
  teaching the caregiver, not treating the child.* That is a genuine shift for clinicians trained in
  direct hands-on intervention and it belongs in the guide.
- **Ch. 39 mandatory reporting** applies with particular force here: OT staff see the child undressed
  for positioning, repeatedly over time, and with the family. Third guide this session to carry the
  Florida universal-reporter flag (**HSC1421**, **MSS0601**, now **OTH2520C**).

One honesty note the guide carries: **sensory-based interventions have a contested literature**, and a
clinician who can distinguish well-supported from merely customary practice is more trustworthy than
one who cannot. Same treatment as the AI, NFT, and craft-beer-market sections — say what the evidence
actually supports.

### Batch 87: `PLA2872 Artificial Intelligence and the Law` — the most Rule-11-exposed guide in the corpus

A genuinely new DSC course (3 cr, spring), and the one where this repository's standing "verify primary
sources" instruction matters most. **Court rules, bar ethics opinions, regulatory frameworks, case law,
and the tools themselves are all changing on a timescale of months.**

The guide is built so the durable content survives that: **what these systems do, how they fail, which
professional duties apply, and how to verify.** Specifics are explicitly marked as of-their-time.

**Four items worth carrying to any future AI-adjacent guide:**

1. **Fabricated citations are a documented, sanctioned failure** — not a hypothetical. Lawyers have been
   fined and referred to disciplinary authorities for filing AI-invented cases, and **"the AI said so"
   has been rejected consistently.** The guide points students at the actual sanctions orders as the
   best teaching material available.
2. **"Legal-specific" ≠ verified.** Independent research (Stanford HAI) has found meaningful error rates
   even in purpose-built legal AI products. Grounded/retrieval tools reduce the problem; they do not
   remove the verification duty.
3. **Confidentiality is the quiet risk.** Entering client matter into a consumer tool may disclose it to
   a third party and may waive privilege. **Consumer and enterprise tiers have entirely different
   terms** — read them before the tool touches a matter.
4. **A specific judge's standing orders are now part of filing practice.** Individual judges have issued
   their own AI disclosure requirements — a genuinely new thing to check, and worth naming.

The guide also treats the **access-to-justice tension honestly** rather than resolving it: most people
with legal problems cannot afford a lawyer, and the conflict between protecting the public from bad
legal advice and denying them any help at all is the real debate.

### Batch 87: ⚠ level I vs level II clinical pricing — the OTH finding now confirmed in PHT

Batch 73 recorded that **OTH level I and level II fieldwork price differently and must not be
averaged.** This batch produced the same structure in physical therapy, and the arithmetic makes the
point sharply:

| Course | Type | Credits | Hours | Ratio |
|---|---|---|---|---|
| **PHT2810** (live) | level II rotation | 2 | **240** | ~120 hrs/cr |
| **PHT2820** (live) | level II rotation | 2 | **280** | ~140 hrs/cr |
| **PHT2804** (this batch) | **level I** experience | 3 | **120 (estimated)** | ~40 hrs/cr |

**Applying the level II ratio would have produced 360–420 hours for a level I course** — implausible on
its face, and exactly the error the OTH finding warns against. DSC publishes no hour count, so the guide
states plainly that **120 is an estimate**, shows the level II figures as the contrast, and tells
students to get the real number from the programme's clinical education handbook.

`validate_drafts.py` flagged it (`3 credits with 120 contact hours`) and the warning is correct to
override here — but **only because the guide body explains the derivation.** That is the standard: a
warning may be overridden when the reasoning is written down for the reader, never silently.

**Standing rule, now two disciplines deep:** *integrated/level I clinical experiences and terminal/level
II rotations are priced separately. Never derive one from the other, and never average the family.*

### Batch 87: the largest PSAV figures yet — and the largest fees in the corpus

**PMT0077C Advanced Welder 1A: 375 clock hours, $1,505.90 lab fee.**
**PMT0078C Advanced Welder 1B: 225 clock hours, $1,176.65 lab fee.**

**600 clock hours across two consecutive terms**, and **$2,682.55 in fees** — both records for this
repository by a wide margin. The fee is consumables, gas, and equipment time rather than administration,
and the guides tell students to ask exactly what it covers before buying anything separately.

**The lab-fee-as-signal finding (batch 81) reaches its extreme here.** The running scale is now:

| Fee range | Reads as |
|---|---|
| **$4–$15** | nominal / project course with minimal consumables |
| **$40–$90** | studio or science lab with real materials |
| **$50–$100 on a *lecture* course** | online courseware, not lab materials (batch 84) |
| **$150** | food-production lab (the flat FOS/FSS rate, batch 81) |
| **$390** | nursing skills lab with clinical supplies (batch 85) |
| **$1,100–$1,500** | **welding — gas, filler, and hundreds of hours of arc time** |

### Batch 87: welding safety is a guide-writing obligation, not a section to skim

Two hazards deserve naming because they are permanent, cumulative, and routinely under-taught:

- **Manganese in welding fume** is associated with a permanent neurological condition resembling
  Parkinson disease.
- **Hexavalent chromium** — produced whenever stainless steel is welded — is a **known human carcinogen**
  with a very low OSHA permissible exposure limit and its own standard. **PMT0078C introduces stainless,
  which is precisely where this becomes relevant.**

Plus the ones that kill quickly: **confined spaces** (shielding gas displaces oxygen with no warning
sign, and the classic fatality is the second person entering to help), **welding on a container that
held flammable material**, and **chlorinated solvents near an arc forming phosgene**. Same class of
content as the batch-86 patient-handling correction: **a guide that leads with the real hazard is more
useful than the textbook chapter the student was assigned.**

Career note worth reusing for any trades guide: **the money is in the difficult work** — pipe, out of
position, code work, outages, travel — and the honest second act is **AWS Certified Welding Inspector**,
which pays well and is far easier on the body than thirty years in a booth.

### Batch 87: PGY is now fully characterized — six numbers, all unsuffixed at DSC

With `PGY1802` and `PGY2806` added, the pattern first recorded in batch 73 is settled: **DSC publishes
its photography prefix unsuffixed while the statewide inventory carries the C-suffixed form.** Six
numbers documented, and the "no C suffix but a lab exists" list now stands at **eight**:

**AFR3221, FSS1287, MUM1622, MUM2611, PGY1101, PGY2650, PGY1802, PGY2806.**

**The lab fee has correctly predicted course type in every one.** The reusable PGY suffix block now
states the estimate's basis (benchmarked to the live PGY2801C at 3 cr / 60 hrs), warns that SCNS
equivalency does not cross the suffix, and tells students to expect a **portfolio review** on transfer —
which is the real gate for studio courses regardless of what the number says.

One content note worth keeping from **PGY1802C**: *asset management is the professional skill students
skip.* Naming conventions, embedded copyright metadata, and a tested 3-2-1 backup are what a photographer
still uses in twenty years, and **they are almost impossible to adopt retroactively** — the editing
techniques get relearned every few years anyway.

### Batch 88: `EML3000` could not be substantiated — recording the evidence trail

Ron asked for **EML3000** in this batch. **It does not appear to exist.** Recording the search so the
ground is not re-covered:

| Source | Result |
|---|---|
| `courses_2plus_institutions.csv` | **150 EML rows, no EML3000** |
| `daytona_courses.csv` | DSC has **no EML subject page at all** — it does not teach the prefix |
| Live API `/courses/EML3000` | `COURSE_NOT_FOUND` |
| **UWF** catalog (32 EML courses) | absent |
| **UF** catalog | absent — jumps **EML2023 → EML3005 → EML3100** |
| 3 web searches | nothing |

**Nearest real numbers:** UF's **EML3005** (Mechanical Engineering Design 1, 3 cr) and the FAMU/FSU
block **EML3004 / 3011 / 3013**.

**Asked rather than guessed**, per the standing "never silently substitute" rule — Ron chose the
verified **EML3000–3022 block** instead, which is what this batch became. *If EML3000 turns up later
with a source, the number is still unwritten.*

### Batch 88: ⚠⚠ **EML3015 and EML3016 denote different subjects at different SUS universities**

**The most consequential collision found in this repository so far**, because it sits in a
transfer-critical engineering core sequence rather than in an elective.

| | **EML3015 / 3015C** | **EML3016** |
|---|---|---|
| **FAMU-FSU College of Engineering** | **Thermal-Fluids I: *Fluid Mechanics*** (4 cr, C-suffixed) | **Thermal-Fluids II: *Heat Transfer*** (3 cr) |
| **University of West Florida** | **Thermal Fluid Systems I: *Thermodynamics*** (3 cr, unsuffixed) | **Thermal Fluid Systems II: *Fluid Mechanics*** (3 cr) |

**Three subjects, two numbers, two institutions — and the titles are nearly identical.** "Thermal
Fluid Systems II" and "Thermal-Fluids II" differ by a hyphen and denote *fluid mechanics* at one
school and *heat transfer* at the other. A student transferring UWF's EML3016 into an FSU-shaped
programme has taken fluid mechanics and is expected to know heat transfer.

**Worse than the batch-80 EET4732C case**, which was at least between two different suffixes. Here the
suffix *also* differs (FSU 3015C integrated/4 cr; UWF 3015 unsuffixed/3 cr with a separate 3016L lab),
so the SCNS numbers are formally distinct in a way that conceals rather than reveals the problem.

**Rule reaffirmed and strengthened:** *identify a course by its catalog description, never by its
number and never by its title.* And for transfer: **give the receiving department the description, not
the course number.**

### Batch 88: the first non-Daytona batch — and the SUS engineering ratios

Every prior batch this session screened against `daytona_courses.csv` first. **This batch had no DSC
involvement at all** — these are State University System courses (FAMU/FSU joint college, UWF, UCF,
USF, Florida Poly, UNF). Ratios confirmed from already-live guides rather than from DSC:

| Shape | Published anchor | Ratio |
|---|---|---|
| Unsuffixed SUS engineering lecture | **EGN3311** 3/45, **EGN3321** 3/45, **EGN2312** 3/45, **EGN3613** 3/45 | **15 hrs/cr** |
| C-suffixed SUS engineering | **EGN3331C** 3/60, **EGN3353C** 3/60 | **20 hrs/cr** |

Applied: 45 for the four unsuffixed, 60 for EML3014C and EML3022C, **80 for the 4-credit EML3015C**.
Clean, and it needed no DSC data — **the live corpus is now large enough to anchor ratios on its own.**

**New standing content for SUS engineering guides** (three reusable blocks written this batch):
1. **FE/PE block** — A.B.E.T.-EAC → FE → experience → PE under **Ch. 471 F.S.**, and the explicit
   contrast with engineering technology, where the route is longer. Plus: **the NCEES FE Reference
   Handbook is free and is the only reference allowed in the exam — start using it in the course.**
2. **EGN/EML numbering block** — the same subject is taught under both prefixes, the **2000/3000
   sophomore-junior pairing** is the trap, and Florida's 2+2 guarantees *admission* with junior
   standing, **not that a lower-division course satisfies an upper-division requirement**.
3. **Workload honesty block** — 8–12 hrs/week, cannot be crammed, draw the diagram every time, state
   the assumptions.

### Batch 88 — operational finding: guides push successfully for courses with **no server-side course record**

All eight EML numbers returned `COURSE_NOT_FOUND` from `/api/v1/courses/{id}` before the push. **The
guide upsert succeeded anyway**, and `/courses/{id}/guide` now returns each one correctly.

`generate_guide.py` already handles this deliberately — `get_course_info()` returns `None` on 404 and
the verify step logs *"guide saved; course not yet browsable — no published modules."*

**Consequence worth knowing:** a guide can be published ahead of its course record, and it is reachable
by API immediately. It will not appear in `/browse/` until the course exists with published modules.
**This makes it safe to write guides for courses outside the DSC-derived queue** — which is what made
this batch possible at all.

`queue_mgr.py reconcile` added the eight as **orphan drafts**, the documented path for courses entering
outside the normal queue, and the progress denominator moved 1651 → 1659.

### Batch 88: the `pypdf` extraction technique, third successful use

**UWF publishes its full EML catalog as a PDF** (`catalog.uwf.edu/courseinformation/courses/eml/eml.pdf`)
and WebFetch returns raw bytes. Extracting locally recovered **complete entries — title, credit hours,
prerequisites, and full description — for every EML course in one fetch**, which is what surfaced the
EML3015/3016 collision above.

Running tally for this technique: **MDC program sheets (batch 80), MDC course sequence guides (batch
80), UWF catalog (this batch).** It is now the standard response to a PDF catalog, not a fallback.

**Source registry addition:**

| Source | Pattern | Status |
|---|---|---|
| **UWF course catalog** | `catalog.uwf.edu/courseinformation/courses/<prefix>/<prefix>.pdf` — **prefix MUST be lowercase** (`.../courses/ant/ant.pdf`); uppercase 404s | ✅ **PDF has full descriptions — extract locally** |
| **FSU undergraduate bulletin** | `registrar.fsu.edu/bulletin/undergraduate-departments/<department>` | ✅ HTML, authoritative for the **FAMU-FSU joint college** |
| **FAMU catalog** | `catalog.famu.edu/preview_entity.php?...` | ✅ reachable |

### ⭐ Standing procedure (Ron, 2026-09-02): a full-prefix PDF extraction may be completed in place

> *"When we find a full catalog of a prefix in a pdf extraction it is OK to divert and complete all the
> courses that exist in that extraction (as found in the UWF pdf file)."*

**When a single PDF fetch yields a complete prefix catalog, stop screening the queue and write out the
prefix.** The economics are decisive: one fetch produces title, credits, prerequisites, and full
description for every course in the prefix, so the marginal research cost per additional guide is
**zero**. Screening the queue for the next eight courses costs more fetches than writing sixteen from
an extraction already in hand.

**Procedure:**
1. Extract the whole PDF locally with `pypdf` (see the batch-80 technique).
2. Split on the course-code boundary and list every entry.
3. **Filter out** shells (`9xx` — directed study, internship, co-op) per `Tools/CLAUDE.md`, and
   **graduate levels** (`5xxx`/`6xxx`).
4. Write the remainder in batches of 8 until the prefix is exhausted.
5. `queue_mgr.py reconcile` picks them up as **orphan drafts**; the denominator grows accordingly.

**First application — UWF `EML`:** one PDF → **17 writable courses**. Batch 88 took four; batch 89 took
eight; the rest follow. **No further fetching was required for any of them.**

### Batch 89: UWF EML prefix completion, part 1

Eight guides written entirely from the batch-88 PDF extraction. **Zero web fetches this batch.**

| Course | cr | hrs | Note |
|---|---|---|---|
| **EML3015** Thermal Fluid Systems I | 3 | 45 | **thermodynamics** — the other half of the collision |
| **EML3016L** Thermal Fluid Systems II Lab | 1 | 45 | equipment fee; "design of engineering experiments" |
| **EML3172L** Mechanics of Materials Lab | 1 | 45 | equipment fee; **prerequisite for Machine Design** |
| **EML3500** Machine Design | 3 | 45 | prereqs EGM3401 + EML3011 + **EML3172L** |
| **EML3703** Thermal Systems 3 | 3 | 45 | heat transfer + **thermal system design** |
| **EML3960** CSWP Exam Prep | 3 | 45 | vendor-certification course — treated honestly |
| **EML4081** Non-Destructive Evaluation | 3 | 45 | prereq EML3011 + PHY2048 |
| **EML4083** Introduction to Exterior Ballistics | 3 | 45 | prereqs **EEL4834 (programming)** + MAP2302 |

**`EML3015` completes the collision pair.** Batch 88 wrote FSU's **EML3015C = fluid mechanics**; this
batch writes UWF's **EML3015 = thermodynamics**. Both guides carry the full collision table. Under
SCNS these are legitimately distinct numbers, so **two guides is the correct outcome, not a
duplication** — and having both live is the clearest possible statement of the problem for a student
comparing catalogs.

**Ratio note:** 1-credit engineering laboratories priced at **45 hrs**, consistent with the live
EVR2001L (1/45) and OCE1001L (1/45) science-laboratory precedent, rather than the 30 used for the
allied-health PTA laboratories (PHT2211L, PHT2140L). **Engineering and science labs run 45; clinical
skills labs run 30.**

### Batch 89: three courses that are unusual enough to be worth naming

**`EML3960` — a credit-bearing vendor certification course.** Three semester hours built entirely
around the SolidWorks CSWP examination. The guide gives the honest two-sided assessment: **the
credential has real market value** (employers list CSWA/CSWP by name and it is one of very few
credentials an undergraduate engineer can hold), **and** three credits is a large allocation to one
vendor's software. The resolution offered is to leave with **transferable modelling discipline** —
design intent, constraint strategy, feature-tree structure, ASME Y14.5 drawing standards — rather than
memorized click sequences. Practical additions: *sit the exam while the course is fresh*, and **ask
about the institutional voucher**, which students routinely never discover.

**`EML4081` — NDE, and the probability-of-detection idea.** The flag worth reusing anywhere inspection
appears: **"inspected and found sound" does not mean "defect-free."** Probability of detection rises
with defect size and never reaches certainty; the **a90/95** convention is what damage-tolerant
inspection intervals are actually built on, which is the direct link to fracture mechanics. Plus the
reporting-integrity flag — **falsified inspection records have contributed to fatal accidents**, and
schedule pressure to pass parts is real and predictable.

**`EML4083` — exterior ballistics, a genuinely rare undergraduate course.** Its presence at UWF
reflects the **Florida Panhandle's defence research concentration (Eglin AFB, AFRL Munitions
Directorate)**. Two carries: the **modelling hierarchy** (vacuum → point mass → modified point
mass/NATO 4DOF → 6DOF) is an unusually clean lesson in *choosing model fidelity to the decision*, which
generalizes across all engineering; and **⚠⚠ ITAR/EAR export control**, which has practical
consequences in a university setting — restricted datasets, limits on what international students may
access, and the real risk of posting controlled technical data to a public code repository. **New flag
class for this repository: export control.**

### ⭐⭐ Standing procedure, generalized (Ron, 2026-09-02): complete a prefix whenever it costs no extra fetches

> *"If we pull any other classes from UWF and pull the catalog, we should go ahead and do all classes
> for the prefix that exist in the pulled catalog. In fact when the opportunity arises to complete a
> prefix without having to do multiple fetches, we should go ahead and do that."*

**This supersedes the narrower PDF-only version recorded in batch 89.** The rule is now about
*marginal fetch cost*, not about file format:

> **Whenever a single fetch — PDF, HTML prefix page, program sheet, or catalog section — yields the
> full set of courses for a prefix, write out the whole prefix before returning to the queue.**

**Why this dominates queue-order work:**

| | Queue-order batch | Prefix completion |
|---|---|---|
| Fetches per 8 guides | **6–10** (screen, then fetch each) | **0** after the first |
| Research per additional guide | one fetch | **zero** |
| Risk of a stale/missing entry | per-course | resolved once for the prefix |
| Cross-references available | scattered | **the whole prefix is in hand** — prerequisites, sequences, and collisions resolve immediately |

**That last row is the underrated benefit.** Holding an entire prefix at once surfaced the
**EML3015/EML3016 subject collision**, the **EML3011 → EML3172L → EML3500** prerequisite chain, and the
**EML3015 → EML3016 → EML3703** thermal sequence — none of which is visible one course at a time.

**Sources that reliably yield a whole prefix in one fetch:**

| Source | Pattern | Notes |
|---|---|---|
| **UWF** | `catalog.uwf.edu/courseinformation/courses/<prefix>/<prefix>.pdf` — **lowercase prefix required** | **PDF carries full descriptions** — extract with `pypdf` |
| **Valencia** | `catalog.valenciacollege.edu/coursedescriptions/coursesoffered/<prefix>/` | HTML, **includes lecture/lab hour splits** |
| **Broward** | `catalog.broward.edu/course-descriptions/<prefix>/` | HTML, includes contact hours |
| **Eastern Florida** | `catalog.easternflorida.edu/course-descriptions-information/<prefix>/` | HTML |
| **Miami Dade** | `mdc.edu/academics/programs/ps/<CODE>.pdf` | program sheet — whole degree, not prefix |
| **Daytona State** | `daytonastate.smartcatalogiq.com/.../<subject-page>/` | ⚠ **listing only — no descriptions**; requires one fetch per course |

**Note the DSC exception.** SmartCatalog's prefix pages list numbers and titles but not descriptions, so
DSC work remains one fetch per course. **That is precisely why the non-DSC prefix sources are worth
preferring when a choice exists.**

**Procedure:** extract → split on the course-code boundary → filter **9xx shells** (directed study,
internship, co-op) and **5xxx/6xxx graduate** per `Tools/CLAUDE.md` → write in batches of 8 until the
prefix is exhausted → `reconcile` adds them as orphan drafts.

### Batch 90: UWF `EML` prefix COMPLETE — 20 courses, one fetch

Nine guides in this batch, closing the prefix. **All 20 writable UWF EML courses are live and
API-verified.**

| Batch | Courses |
|---|---|
| **88** | EML3011, EML3016, EML3022C *(+ the FSU-side EML3004, 3012, 3013, 3014C, 3015C)* |
| **89** | EML3015, EML3016L, EML3172L, EML3500, EML3703, EML3960, EML4081, EML4083 |
| **90** | EML4225, EML4230, EML4321, EML4542, EML4575, EML4722, EML4804, EML4804L, EML4961 |

**Excluded, correctly:** EML3905 / EML4905 (Directed Study), EML4940 (Internship), EML4948 (Co-Op) —
shells per `Tools/CLAUDE.md`; EML5086 / 5546 / 5570 / 5905 / 6237 / 6805 / 6905 / 6938 — graduate.
**Also skipped: unsuffixed `EML3022`**, since the batch-88 `EML3022C` guide covers the UWF course
explicitly and a separate guide would be a near-duplicate — noted here so the decision is not
re-litigated.

**Total EML work across batches 88–90: 25 guides from two fetches** (UWF PDF + FSU bulletin).

### Batch 90: four flags worth reusing beyond this prefix

**1. `EML4575` — the fracture-mechanics ↔ NDE loop closes.** This is the clearest cross-guide
connection in the corpus. **NDE gives you the smallest crack you can reliably detect (a90/95); fracture
mechanics gives you the critical crack size; the Paris law fills the gap and yields an inspection
interval.** That is the whole logic of damage-tolerant design and of why aircraft are inspected on a
schedule rather than merely built conservatively. **The EML4081 and EML4575 guides now reference each
other explicitly.**

**2. `EML4722` — the third "simulation lies" flag, and the strongest.** Following the FEA warnings in
EML3011 and ETG3533C, the CFD guide states it plainly: *the software always produces a result, it is
always rendered attractively, and nothing in the output distinguishes a validated solution from
nonsense.* Added the **verification vs validation** distinction (did I solve the equations right / did
I solve the right equations), **grid independence**, and the free public validation sets (NASA
Turbulence Modeling Resource, ERCOFTAC). **This is now a standing flag class: any guide for a course
that teaches simulation gets it.**

**3. `EML4804`/`EML4804L` — software errors become physical motion.** A distinct safety class from
anything previously recorded: **a bug becomes a motor spinning.** The operative rule is that
**an emergency stop must cut actuator power in hardware — a stop that depends on the code running is
not a stop.** Reusable for robotics, automation, and any embedded-control guide.

**4. `EML4961` — a licensure-exam course, and the timing advice that matters.** The honest framing:
**pass rates are markedly higher near graduation**, the FE is offered year-round which paradoxically
makes it easy to postpone forever, and **the single best predictor of passing is having a date in the
calendar.** Also: **the NCEES Reference Handbook is free and is the only permitted reference — use it
as the working reference from the first week**, because candidates lose real marks on navigation alone.
Same shape as the batch-89 CSWP finding and the batch-83 PMI-PBA finding: **for any exam-prep course,
check eligibility and tell the student to book the test.**

### Batch 91: DSC `ARR` prefix COMPLETE — 10 courses, and a catalog error found

All 10 writable ARR courses are live. Excluded correctly: **ARR0905** (Directed Study) and **ARR0949**
(Cooperative Education) as shells per `Tools/CLAUDE.md`.

**The prefix has a structure worth recording, because it is not a linear sequence.** Three parallel
tracks are taken as **corequisite triples**, one triple per term:

| Term | Refinishing | Collision repair | Unibody / frame |
|---|---|---|---|
| **1** (fall/spring) | ARR0121C | ARR0241C | ARR0381C |
| **2** (spring/summer) | ARR0122C | ARR0242C | ARR0382C |
| **3** (summer/fall) | ARR0123C | ARR0243C + ARR0244C | — |
| **+** | **ARR0021 Estimating** (75 hrs, summer) | | |

**⚠ The cross-track prerequisites are the non-obvious part.** ARR0122C's prerequisite is **ARR0381C**,
and ARR0123C's is **ARR0382C** — so **the refinishing sequence is gated by the unibody sequence**, not
by the previous refinishing course. That enforces cohort progression: a student cannot advance in one
track while failing another. **Nine courses at 120 clock hours plus 75 = 1,155 clock hours.**

**Every ARR course publishes an explicit "C or better to continue / to graduate" gate.** That is
unusual to state so plainly in a catalog and it is worth flagging in guides — in a trade where work is
inspected and warranted, a marginal pass is a real problem.

### ⚠⚠ Batch 91 — catalog error found: `ARR0382C` carries `ARR0244C`'s description

**Daytona State's published description for ARR0382C "Intermediate Unibody and Frame and Lab" is
verbatim the description published for ARR0244C** — plastic repair and adhesive bonding, under a
unibody and frame title.

**Every other published field contradicts it.** The title, the position between ARR0381C and the rest
of the structural track, the corequisite (ARR0122C, matching the second-term block), and — decisively —
**its role as the stated prerequisite for ARR0123C**, exactly mirroring how ARR0381C gates ARR0122C.

**The guide was written to the structural role and carries an explicit flag** describing the
discrepancy, the evidence for the structural reading, and an instruction to confirm with the programme.

**This is the fourth instance of the same principle**, and it is now firmly established:

> **The prerequisite chain is a more reliable indicator of a course's role than its title or its
> published description.**

Prior instances: **PHT2810/2820** (a course titled "II" that is the third rotation, resolved by
prerequisite), **MSS0157** (CSV said "I", catalog said "II", prerequisite MSS0156 settled it), and
**EET4732C vs EET4732** (identical digits, opposite subjects, resolved by description). **ARR0382C is
the first case where the *description itself* is the corrupted field** — which is why the prerequisite
chain had to carry the whole determination.

### ⚠ Batch 91 — process failure: an existing published guide was overwritten

**`ARR0021` already had a live guide**, pushed by this pipeline at **2026-09-02T18:56Z**. Completing the
ARR prefix wrote a new draft to the same path and pushed it at **01:30Z**, **replacing the published
version without checking**. The local draft was overwritten too, so the prior text is not recoverable.

**Cause:** the prefix-completion procedure builds a draft for every course in the prefix. `ARR0021` was
outside the batch's queue selection but inside the prefix, and **nothing in the flow checks whether a
guide already exists before writing the draft file.** `queue_mgr.py reconcile` reported "9 marked
drafted" rather than 10 — that discrepancy was the available signal and it was not investigated at the
time.

**Handled:** the replacement was republished as **v1.1** so the version field reflects that it is a
revision rather than an original, and Ron has been told.

**Ron's ruling (2026-09-03): overwriting is acceptable.** Prefix completion may replace an
already-published guide rather than skipping it — the later guide is written with the whole prefix in
hand and is normally the better one.

**The remaining obligation is bookkeeping, not permission:**

> **When a prefix completion replaces a published guide, increment the version** (v1.0 -> v1.1) so the
> field records that it is a revision, **and say so in the batch report.** Do not leave a replacement
> mislabelled as an original.

`queue_mgr.py reconcile` gives the signal for free — a "marked drafted" count lower than the number of
drafts written means one or more were already `pushed`. **Read that number.**

### Batch 91: four content flags worth reusing

**1. Isocyanates — a permanent, career-ending sensitization risk.** Two-component clearcoats and
primers cause **occupational asthma**, sensitization is **permanent and dose-independent once
established**, and **a cartridge respirator is not adequate — supplied air is the standard of care.**
This belongs in any refinishing, coatings, or spray-application guide.

**2. "Follow the OEM repair procedure" is now the industry's governing standard.** The single biggest
change in collision repair in two decades: the manufacturer's published procedure specifies what may be
repaired, what must be replaced, where sectioning is permitted, what may not be heated, which fasteners
are single-use, and what must be recalibrated. **Departing from it carries liability**, and litigation
has established that following it is the standard of care.

**3. ADAS calibration has changed the trade — and the estimate.** Cameras, radar, and sensors require
recalibration after operations that seem unrelated (windscreen, alignment, bumper removal, structural
repair). **A vehicle returned with an uncalibrated system is a safety and liability problem, not an
unfinished job**, and pre- and post-repair scanning is a billable line item routinely omitted by
inexperienced estimators. **Rule 11 applies with force** — this is the fastest-moving part of the trade.

**4. Ultra-high-strength steel cannot be heated.** The processing that makes it strong is destroyed by
heat, so many manufacturers prohibit heating structural components outright and require replacement
rather than straightening. **The mild-steel intuition that metal can always be worked back is now
actively dangerous**, and it connects directly to this repository's welding and materials guides.

### Batch 92: the DSC **PHT** prefix completed — 12 courses, and the C-form 4/75 pattern breaks

Twelve guides pushed (11 DSC + PHT2221C from Polk State), taking the prefix from 9 live to **25 of 27
queued rows**. The prefix is now effectively complete: the only remaining rows are **PHT2931**
(deliberately skipped) and **PHT1006C** (holder institution not identified — see below).

| Course | Title | cr | hrs | Term | Note |
|---|---|---|---|---|---|
| PHT1006 | Introduction to Physical Therapy | 3 | 45 | F/Sp/Su | |
| PHT1128 | Kinesiology of PTA | 4 | 60 | Spring | prereq BSC1085C |
| PHT1251 | Patient Care Skills | 2 | 30 | Spring | |
| PHT2129 | Neuroscience for PTA | 2 | 30 | Summer | catalog: "continuation of PHT1128" |
| PHT2214 | Modalities II | 1 | 15 | Fall | |
| PHT2214L | Modalities II Lab | 1 | 30 | Fall | $42 fee |
| PHT2220 | Therapeutic Exercise I | 3 | 45 | Spring | |
| PHT2221 | Therapeutic Exercise II | 4 | 60 | Summer | largest lecture in the programme |
| PHT2221L | Therapeutic Exercise II Lab | 2 | 60 | Summer | largest lab in the programme |
| PHT2235 | Therapeutic Exercise III | 4 | 60 | ⚠ not stated | catalog omits the term for the lecture |
| PHT2235L | Therapeutic Exercise III Lab | 2 | 60 | Fall | $9 fee |
| **PHT2221C** | Therapeutic Exercises in PT II | **3** | **60** | Summer | **Polk State — 2 lec + 2 lab** |

Both PHT lecture (15 hrs/cr) and lab (30 hrs/cr) ratios held across all eleven DSC courses without
exception, which is the first prefix in this project where **every** course priced cleanly off the
pinned ratios with no catalog-stated split needed.

### ⚠⚠ Batch 92: the PHT "C form = 4 cr / 75 hrs" pattern is **not** a rule — it broke on the third case

SOURCES.md recorded at batch 74 that DSC-adjacent **combined C forms sit at ~75 hours and 4 credits**,
on the evidence of PHT1128C and PHT2220C both published here at 4/75. That inference was about to be
applied to PHT2221C. **It would have been wrong.**

| C form | Institution | Credits | Structure |
|---|---|---|---|
| PHT1128C | (published here) | 4 | ~75 hrs |
| PHT2220C | (published here) | 4 | ~75 hrs |
| **PHT2221C** | **Polk State** | **3** | **2 lec + 2 lab = 60 hrs** |

**Two concurring data points did not establish a family.** The generalisable instruction: *a ratio
pinned from two members of a family is a hypothesis, not a convention — and the cost of testing it is
one search.* The hour-source hierarchy already ranks "a catalog's own published split" above "a family
ratio"; this is the first case where following that ranking **changed the published number** rather than
merely confirming it. Where a C form belongs to an institution not already in the corpus, **go find its
catalog before pricing it off siblings.**

### ⚠⚠ Batch 92: C forms and split forms **do not divide the content the same way** — the deepest Rule 22 case yet

Rule 22 has been recorded here many times as a formal point: the C/L suffix is part of the number, so
equivalency does not cross it. PHT2221C shows the **substantive** reason that rule exists.

| Form | Credits | Content |
|---|---|---|
| **PHT2221C** (Polk) | **3** | orthopaedic + balance + cardiovascular exercise **plus amputee rehab, orthotics/prosthetics, and gait training** |
| **PHT2221 + PHT2221L** (DSC) | **6** | orthopaedic + balance + cardiovascular exercise, and manual muscle testing — **gait, amputation, and prosthetics live in PHT2235** |

So Polk's single 3-credit PHT2221C spans roughly **DSC's PHT2221 *and* part of PHT2235**, at half the
credit. This is not a rounding difference in how a course was packaged; **the topic boundaries between
consecutive course numbers move between institutions.** Previous C-vs-split findings in this project
were about credit arithmetic (PHT2220C off by one against PHT2220 + PHT2220L). This one is about
**scope**, and it is the stronger caution: a student may find a topic covered twice, or not at all.

Practical rule now: **when writing a C form whose split counterparts are already live (or vice versa),
read both descriptions and state the mapping explicitly in the guide.** Do not let a reader infer
equivalence from adjacent numbers.

### Batch 92: PHT numbering is institution-specific to an unusual degree — four catalogs, four schemes

Chasing PHT1006C surfaced full PHT listings at four institutions. **Almost nothing lines up.**

| Institution | Numbering scheme | Notable |
|---|---|---|
| **Daytona State** | paired lecture + `L` lab throughout (PHT2220/2220L …) | the corpus baseline |
| **Polk State** | almost entirely `C` combined forms (PHT1250C, PHT1128C, PHT1213C, PHT2252C, PHT2253C) | clinicals are `L`-suffixed: PHT1801L, PHT2810L, PHT2820L |
| **Gulf Coast State** | paired lecture + `L` lab, but a **wholly different topic decomposition** — PHT1102/1102L Applied Anatomy, PHT1124/1124L Functional Human Motion, PHT1131/1131L Assessment, PHT2224/2225/2226 by disability type | its PHT2810/2820 are **4 credits** each, against DSC's 2 |
| **Seminole State** | paired lecture + `L`, third scheme again — PHT1120 Musculoskeletal I, PHT2253 Neurorehab I, PHT2304C Pathophysiology | PHT1800L / PHT2810L clinicals at **6 credits** each |

**PHT is now the clearest example in this project of a prefix where the SCNS number carries far less
cross-institutional meaning than usual.** The programme-level pattern is what generalises (a PTA
curriculum always contains kinesiology, patient care skills, modalities, a therapeutic exercise
sequence, and two or three full-time clinicals), while the numbers attached to those blocks do not.
Guides in this prefix should lead with the **programme role** of a course and treat the number as a
local label — which is the opposite of the approach that works for, say, general-education prefixes.

⚠ Related discrepancy worth carrying: **clinical-rotation credit values vary by a factor of three** for
the same 6–8 week full-time rotation — DSC PHT2810 at **2 cr / 240 hrs**, Gulf Coast PHT2810 at **4 cr**,
Seminole PHT2810L at **6 cr**. The published `120–140 hrs/cr` PHT clinical ratio recorded at batch 87 is
a **Daytona State** figure, not a prefix-wide one. Gulf Coast's own catalog states the rotation as
"40 hours/week, 7 weeks" (= 280 hrs) at 4 credits — **70 hrs/cr** — and Seminole's at 6 credits would be
~47 hrs/cr. Do not apply the DSC clinical ratio outside DSC.

### Batch 92: ⚠ PHT2931 — a "931" number that is **not** a shell at any institution checked

`PHT2931` was skipped by the standing 9xx-shell rule. All four catalogs pulled this batch publish it as
a **real, consistently-titled course**:

- Seminole State — "Trends in Physical Therapy", **1 credit**
- Polk State — "Trends in Physical Therapy", fall, **corequisite of PHT2221C**
- Gulf Coast State — "**Seminar**", **2 credits**, corequisites PHT2810 + PHT2820, $129 fee; content is *clinical research, professional development, licensure, and exam preparation*

Fourteen institutions carry it. **This is a capstone/licensure-prep seminar taken alongside the terminal
clinicals, not a directed-study shell.** The 9xx skip rule is correct in general (it has correctly caught
dozens of internship and special-topics shells) but **931 in a licensed allied-health prefix deserves a
look before skipping** — the number is being used as a seminar slot, and the title is stable across
institutions, which is the signal that distinguishes a real course from a shell.

**Left as skipped pending Ron's call** rather than un-skipped unilaterally, since the skip list is a
deliberate scope decision. Flagged here as a correction candidate alongside ETI4448, RTE2563C, and
EET1025C.

### Batch 92: PHT1006C — prefix completion blocked, and the blocker recorded rather than guessed

`PHT1006C` ("Role of PTA with Lab", 2 institutions) is the one course standing between this prefix and
completion. **It was not found** in Seminole State, Polk State, or Gulf Coast State catalogs;
**NWFSC returned 403** and **Santa Fe College returned an empty body** through WebFetch. Two targeted
searches did not surface it either.

The tempting move was to price it off the PHT C-form family at 4 cr / 75 hrs. **Given that PHT2221C had
just broken that exact pattern in this same batch, that would have been a guess dressed as an
inference.** It was left queued with the ruled-out institutions written into its `notes` field, so the
next attempt starts from four eliminated catalogs rather than from zero.

Standing practice this reinforces: **when prefix completion is blocked by a missing source, write what
was ruled out into the queue row.** The cost is one line; it converts a dead end into progress.

New sources confirmed fetchable this batch:

| Source | URL pattern | Yield |
|---|---|---|
| **Polk State catalog** | `catalog.polk.edu/preview_course_nopop.php?catoid=<n>&coid=<n>` | ✅ full entry incl. lecture/lab split, prereqs, coreqs |
| **Polk State programme** | `polk.edu/<program-slug>/program-curriculum/` | ✅ full course list by term (no credits) |
| **Gulf Coast State** | `gulfcoast.edu/catalog/current/courses/<prefix>/index.html` | ✅✅ **entire prefix in one fetch**, with credits, lec/lab split, prereqs, coreqs, and lab fees |
| **Seminole State** | `seminolestate.edu/catalog/programs/<slug>` | ✅ full programme course list with credits |
| NWFSC | `catalog.nwfsc.edu/preview_program.php?...` | ❌ 403 (bot filter — retry later) |
| Santa Fe College | `catalog.sfcollege.edu/preview_program.php?...` | ❌ empty body |

⚠⚠ **`gulfcoast.edu/catalog/current/courses/<prefix>/index.html` is the highest-value pattern found in
several batches** — it returns a *whole prefix* with credits and lecture/lab splits in a single fetch,
which is exactly the marginal-fetch-cost condition for prefix completion. **Try it first for any prefix
Gulf Coast is likely to carry.** (It is already listed in this file as a fetchable institution, but the
per-prefix course-index URL shape was not recorded.)

### Batch 93: DSC **RTV** prefix completed — 10 courses, and a clean prefix-ratio derivation

Ten guides pushed, all v1.0 first publishes, all validated clean and verified live. The RTV prefix is
now **14 of 16 queued rows live**, the remaining two being RTV2940 and RTV2949 (both correctly skipped
as internship/co-op shells). **The prefix is complete.**

| Course | Title | cr | hrs | Terms | Prereq / coreq |
|---|---|---|---|---|---|
| RTV1251 | Digital Video Editing | 4 | 80 | Fall | — |
| RTV1520C | Video Field Production | 4 | 80 | F/Sp | ⚠ suffix divergence, below |
| RTV1613 | Digital Video Effects | 3 | 60 | Spring | — |
| RTV1670 | Television Directing | 3 | 60 | F/Sp | pre RTV1000, **co RTV1510** |
| RTV2104 | Broadcast Research/Newswriting/Presentation | 3 | 60 | Spring | pre ENC1101 |
| RTV2241 | Producing for Television | 3 | 60 | F/Sp | pre RTV1000 + RTV1510 |
| RTV2290 | Selected Topics in Remote Sports Production | 3 | 60 | F/Sp | pre RTV1000 + RTV1510 |
| RTV2534 | Electronic Field Production | 3 | 60 | F/Sp | pre RTV1000 + RTV1510, **co RTV2540** |
| RTV2540 | Workshop in Studio Production | 3 | 60 | F/Sp | pre RTV1000 + RTV1510, **co RTV2534**, $4.60 fee |
| RTV2541 | Team Media Production | 4 | 80 | F/Sp | pre RTV1000 + RTV1510; "level III" |

### Batch 93: ✅ the cleanest prefix-ratio derivation yet — the live corpus priced the whole batch

**Daytona State publishes no lecture/lab split for any RTV course**, and none of the ten fetched pages
carried contact hours. The hours above came entirely from **tier 2 of the hour-source hierarchy — the
already-live corpus at the same institution**:

| Live guide | cr | hrs | ratio |
|---|---|---|---|
| RTV1000 | 4 | 80 | 20.0 |
| RTV1510C | 4 | 80 | 20.0 |
| RTV2100C | 3 | 60 | 20.0 |
| RTV2600C | 3 | 60 | 20.0 |

**Four for four at exactly 20 hrs/credit** — the uniformity test the hierarchy requires before a prefix
ratio may be used, passed without a single outlier. This is the strongest instance yet of the batch-91
observation that **the live corpus is now large enough to anchor its own ratios**: no catalog data, no
external source, and no estimate was needed for ten courses. **New pinned ratio: DSC RTV = 20 hrs/cr**
(studio/lab-weighted, notably higher than the DSC lecture convention of 15).

### ⚠ Batch 93: RTV1520C vs RTV1520 — the suffix divergence, handled per the batch-83 rule

The queue carries **RTV1520C "Video Field Production"** (2 institutions). Daytona State publishes
**RTV1520 "Broadcast Videography"** — different suffix *and* different title. Applying the rule
established at batch 83 (*when the queue ID and the DSC entry differ by suffix, the DSC entry is
evidence about content, not structure*), the DSC description — camera construction, composition, lens
function, sequencing, shooting for the edit — is exactly field videography, so the content mapping is
sound; the C suffix indicates a formally integrated lecture-and-laboratory structure. Published at
4 cr / 80 hrs matching DSC's RTV1520, **with the distinction written into the guide for the reader**
rather than silently equated.

⚠ Related, already handled correctly in an earlier batch and worth recording: **RTV2600C is live as
"Acting for the Lens and Camera"** (the DSC title) while the *queue* title says "RADIO AND TV
ANNOUNCING". A previous batch used the catalog over the queue index. This is another instance of the
standing finding that **`daytona_courses.csv` and the queue titles are a screening index, not a source.**

### ⚠⚠ Batch 93: a **mutual corequisite pair** — RTV2534 ↔ RTV2540, a structure not previously recorded

RTV2534 (Electronic Field Production) lists RTV2540 as its corequisite, and **RTV2540 lists RTV2534 as
its corequisite.** Each is the other's.

This is structurally different from every corequisite relationship recorded in this project so far,
which have all been **lecture + its own laboratory** (PHT2221/2221L, MSS pairs, and so on) — a
dependent pair sharing one subject. Here the two courses cover **the two halves of production practice,
field and studio**, taught in the same term so students work in both environments simultaneously.
Neither is subordinate to the other.

**Practical consequence worth flagging in guides:** a transfer bringing one of a mutual pair **cannot
satisfy the other's corequisite**, because the corequisite is the co-enrolment itself. Both guides say
so explicitly. When a corequisite is encountered in future batches, **check whether it is reciprocal
before describing it as a lab pairing.**

Note also **RTV1670 ← RTV1000 (prereq) + RTV1510 (coreq)**: directing is taught alongside studio
production because it cannot be learned in the abstract. A one-directional coreq, unlike the pair above.

### Batch 93: ⚠ RTV2290 — "Selected Topics" in the title, a substantive gated course in fact

`RTV2290` is titled **"Selected Topics in Remote Sports Production"** and would read as a variable-content
shell on title alone. It is not: it carries **RTV1000 and RTV1510 as hard prerequisites**, has a fixed
subject, and is offered every fall and spring.

This is the **second shell-detection finding in two batches**, after PHT2931. Together they refine the
rule: the 9xx-number test is reliable, but **"Selected Topics" / "Special Topics" / "Seminar" in a
*title* is not** — check the prerequisites and the offering pattern. **A course with hard prerequisites
and a fixed term pattern is a real course whatever its title says.** (The converse also held here:
RTV2940 "Practicum" and RTV2949 "Cooperative Education" are genuine shells and stayed skipped.)

### Batch 93: source-pattern results — Gulf Coast's one-fetch prefix index tested and scoped

The `gulfcoast.edu/catalog/current/courses/<prefix>/index.html` pattern recorded in batch 92 was tested
against three queued prefixes. **The pattern works perfectly; the institution was the wrong holder.**

| Prefix | Gulf Coast has the prefix | Overlap with queued IDs |
|---|---|---|
| STS | ✅ (STS1310, 1340C, 1940C, 2323, 2330C, 2335/2336, 2361, 2370, 2953/2954) | ❌ **none** — queued block is STS0xxx PSAV |
| PMT | ✅ (PMT2250C, PMT2254C only) | ❌ none — queued block is PMT02xx machining |
| RTV | ✅ (RTV2949 only) | ❌ none |

**The generalisable lesson: a one-fetch prefix source is only worth the fetch if that institution holds
the queued course numbers.** Gulf Coast carries 150+ prefixes but its *numbers* within a prefix are its
own. **Confirm the holder before spending the fetch** — a targeted web search on one distinctive queued
course number costs less than a prefix fetch and answers the question directly. That is what identified
Daytona as the RTV holder here (searching `"RTV2290" "Remote Sports Production"`), which turned a
guessing problem into a ten-fetch certainty.

✅ **`gulfcoast.edu/catalog/current/courses/index.html` is itself high-value** — it returns the complete
list of ~150 prefixes Gulf Coast carries with their URL slugs, in one fetch. Useful as a *screening*
step: it says instantly whether Gulf Coast is even a candidate holder for a prefix. **Gulf Coast does
not carry ACR, BCA, DIM, HUS, or CHD**, among the currently-queued prefixes; it does carry CET, CTS,
ETI, FOS, HFT, OST, PGY, PMT, RET, RTV, SLS, and STS.

⚠ Fetch-prompt note: asking a catalog page for content **"verbatim"** and **"complete"** now sometimes
triggers a reproduction refusal from the fetch summariser (it did for Gulf Coast STS). **Ask instead for
the specific fields** — number, title, credits, lecture/lab hours, prerequisites, terms, fees — which
returns the same usable data without tripping it.

### Batch 93: content-domain findings worth carrying to any media, journalism, or production prefix

Three flags were written into all ten guides and generalise to RTV, DIG, GRA, JOU, MMC, PGY, and TPA:

- **⚠⚠ Florida is an all-party consent state for recording** (Fla. Stat. § 934.03). Most states require
  one party's consent; Florida requires everyone's where there is a reasonable expectation of privacy,
  and violation is criminal. **This is a genuinely Florida-specific legal fact that students trained on
  national material get wrong**, and it applies to every interview, phone call, and field recording.
  Rule 11 flagged.
- **⚠⚠ Copyright and music licensing** is the trap that destroys student portfolios — commercial music
  cannot be used, fair use is a defence rather than a permission, "royalty-free" is not free, and
  Content ID finds it permanently. Paired with appearance releases (parent signature for minors) and
  location permissions.
- **⚠ The reel is the credential, not the transcript.** Hiring in production is portfolio-driven and
  referral-driven, which makes clearing rights *at the time* a career matter rather than a course
  requirement.

Also recorded: **FAA Part 107** is a concrete, cheap, directly marketable certificate for anyone doing
aerial work — worth naming in any production or surveying guide.

### Batch 94: DSC **STS** prefix completed — a whole PSAV certificate programme in one batch

Eleven guides pushed, all v1.0, all validated clean, all verified live. **The STS prefix is complete**:
25 of 25 queued rows resolved (21 live, 4 deliberately skipped — STS1931 seminar and STS2944C/2945C/2946
clinicals).

Ten of the eleven are **0000-level PSAV clock-hour courses** forming a single surgical technology career
certificate — **the first time this project has published an entire PSAV programme as a coherent unit**,
rather than PSAV courses encountered one at a time inside a mixed batch.

| Term | Course | Clock hrs | Credits |
|---|---|---|---|
| Fall | STS0003 Introduction to Surgical Technology | 60.9 | **0** |
| Fall | STS0120 Surgical Specialities I | 66 | **0** |
| Fall | STS0155 Surgical Techniques and Procedures | 96 | **0** |
| Fall | STS0155L …Lab | 111 | **0** |
| Fall | STS0255L Surgical Procedures Clinical I | 192 | **0** |
| Spring | STS0008 Pharmacology for Surgical Technology | 45 | **0** |
| Spring | STS0121 Surgical Specialities II | 88.2 | **0** |
| Spring | STS0256L Surgical Procedures Clinical II | **375** | **0** |
| Summer | STS0122 Surgical Specialities III | 34.8 | **0** |
| Summer | STS0257L Surgical Procedures Clinical III | 156 | **0** |
| — | **STS-prefix total** | **1,224.9** | |
| Spring | STS1323C Surgical Procedures I (college credit) | 60 hrs | 3 |

### ⚠⚠ Batch 94: the 0000-level "Credit Hours" trap, confirmed at scale

The batch-82 rule (*any 0000-level number is PSAV — set `credits: 0`, reason from the first digit, never
from the label*) was previously established on two courses, HCP0750C and HSC0005. **This batch is the
decisive confirmation: all ten 0-level STS courses render their clock-hour figure under a "Credit Hours"
heading**, and the values are 60.9, 45, 66, 88.2, 34.8, 96, 111, 192, 375, and 156.

**STS0256L would have been published as a 375-credit course.** The absurdity of the largest values is
what makes the rule easy to apply here — but note that **STS0008 renders as "45" and STS0120 as "66"**,
values that are absurd for credits yet not *obviously* so at a glance, and **STS0155L's page rendered as
"1 credit hour (111 clock hours)"** — the only one of the ten to show both figures. That inconsistency
is the real hazard: a page that displays a plausible small number invites the wrong reading.

**The rule stands and needs no exception: reason from the leading zero, never from the label.**

Non-integer clock hours (60.9, 88.2, 34.8) were handled by the standing practice from the MSS batches:
**round the `contact_hours` field, and state the exact catalog figure in the guide body with an
instruction to use it for programme hour-counting.**

### ✅ Batch 94: the programme total as a self-consistency check

Summing the ten courses gives **1,224.9 STS-prefix clock hours**, with BSC0070 and HSC1531 as additional
prerequisites outside the prefix. The arithmetic is worth doing on any PSAV block for two reasons:

1. **It validates the extraction.** A term-by-term total that lands near a plausible programme length is
   evidence every course was read correctly; a wild total would have signalled a misread figure.
2. **It is genuinely useful to the reader**, who needs to know the shape of the commitment — and here the
   shape is striking: **723 of 1,224.9 hours (59%) are clinical rotation**, and **STS0256L alone is 375
   hours, ~30% of the whole programme, in a single spring term alongside two classroom courses.**

⚠ I did **not** assert a state framework total. Florida PSAV programmes are defined by DOE curriculum
frameworks with a specified total, but the framework figure was not verified in this batch, so the guides
give the computed prefix total and tell readers to confirm the programme total with the institution.
**Deriving a regulatory total by subtraction would have been a guess.**

### ⚠⚠ Batch 94: DSC runs two parallel STS programmes with near-identical course titles

The clearest instance yet of a pattern worth naming generally.

| PSAV (clock hours, 0 credit) | College credit | Shared/parallel title |
|---|---|---|
| **STS0003** | **STS1302** | *both* "Introduction to Surgical Technology" |
| STS0120 / 0121 / 0122 "Surgical Specialities I–III" | STS1323 / STS2324 "Surgical Procedures I–II" | parallel specialty sequences |
| STS0155 + STS0155L | STS1304L / STS1327L | laboratory technique |
| STS0255L / 0256L / 0257L | STS2944 / 2945 / 2946 | clinical rotations |

**STS0003 and STS1302 share a title exactly and are different courses at different levels with different
outcomes.** A student searching by title alone cannot distinguish them. Both routes can reach the same
job and CST eligibility; the difference is cost, duration, and whether the student finishes holding
credit that counts toward a degree.

**Generalisable instruction:** in any prefix where an institution runs both a PSAV certificate and a
credit degree — allied health especially (STS, PHT, HCP, MSS, PRN, DEA) — **check whether the title you
are writing about exists at two levels before assuming which course the queue ID refers to.** The leading
digit settles it; the title never does. This is a fifth instance of the standing principle that *the
number and the prerequisite chain are more reliable than the title.*

### Batch 94: STS1323C priced from the only same-credit C form in the prefix

DSC publishes the unsuffixed **STS1323 at 3 credits** with no hour split. The queue ID is the **C form**
(6 institutions). Applying the batch-83 rule (*a suffix difference makes the DSC entry evidence about
content, not structure*), the hours had to come from the C-form family, not from the lecture convention.

| Live STS guide | cr | hrs | ratio |
|---|---|---|---|
| STS1303, STS1308, STS2340, STS2179 (unsuffixed lecture) | — | — | **15.0, 4/4 uniform** |
| STS1304L, STS1327L, STS2365C (labs) | — | — | 30.0 |
| STS1302C | 2 | 45 | 22.5 |
| STS2324C | 4 | 90 | 22.5 |
| **STS1307C** | **3** | **60** | **20.0** |

Two candidate anchors existed: the **same-series** sibling STS2324C ("Surgical Procedures II", 22.5 ratio
→ 67.5 hrs at 3 credits) and the **same-credit-value** C form STS1307C (3/60). **Chose 60**, because
3 × 22.5 = 67.5 is not a real published value anywhere in the family, whereas 3/60 is, and because 60 is
also the validator's established floor for a 3-credit C course (the IND2410C correction at batch 83).

**Refinement to the hour-source hierarchy worth recording: when two tier-2 anchors compete, prefer the
one that matches the *credit value* over the one that matches the *series*.** A ratio carried across
credit values produces a number nobody publishes; a same-credit sibling produces one that exists.

### Batch 94: content flags for any surgical, sterile-processing, or perioperative prefix

Six blocks written into all eleven guides, generalising to STS, SUR, HSC, PRN, NUR, and DEA:

- **⚠⚠ Surgical conscience** — the profession's defining value: *if you break sterility and nobody saw,
  you say so.* Sterility is absolute, not probabilistic; "when in doubt, it is contaminated." This is
  the single most important thing in the prefix and it is an ethical teaching, not a technical one.
- **⚠⚠ Counts and retained surgical items** — a "never event." Defined count points, audible two-person
  counting, and **a discrepancy stops the process** (recount, search, notify, X-ray). Concentration
  lapses at closure, which is exactly when retained items happen.
- **⚠⚠ Sharps and bloodborne pathogens** — the scrub handles more sharps than anyone in the room.
  **Neutral zone / hands-free technique** is the standard of practice; never recap by hand; report every
  exposure immediately because **students under-report out of embarrassment** and prophylaxis is
  time-critical.
- **⚠⚠ Medication labelling on the sterile field** — the field is where surgical medication errors
  overwhelmingly occur, because unlabelled clear solutions are indistinguishable. Label container *and*
  syringe with **name and concentration** at the moment of receipt; discard anything unlabelled.
- **⚠⚠ CST / NBSTSA certification gated by CAAHEP or ABHES accreditation** — structurally identical to
  the CAPTE trap recorded for PHT: **unrecoverable after the fact, so verify before enrolling.** Plus a
  **documented case log** (commonly cited as 120 cases across specialty categories) that must be kept
  from day one — audit it against the requirement early, since missing categories can be arranged in
  week four and cannot in week fourteen.
- **⚠ Speaking up to senior staff** — written into the clinical guides: state the observation not the
  judgement, say it immediately, escalate if dismissed. This is surgical conscience applied to other
  people, and it is the hardest thing the programme teaches.

⚠ Regulatory items were deliberately hedged. **Florida's licensure status for surgical technologists**
(not historically licensed as a distinct profession, unlike nurses or PTAs) and the **120-case figure**
are both stated with Rule 11 verify-instructions rather than as settled fact, since neither was verified
against a primary source in this batch.

### Batch 95: DSC **HFT** prefix completed — 10 courses, and a craft-brewing programme inside a hospitality prefix

Ten guides pushed, all v1.0, all clean, all live. **The HFT prefix is complete**: 24 pushed, 5 skipped,
0 queued. All ten were 3 credits / 45 contact hours, and **all ten IDs matched the DSC index exactly** —
no suffix or title divergence anywhere in the batch, which is unusual and made it the cleanest extraction
of the run.

| Course | Title | Terms |
|---|---|---|
| HFT1021 | Beer, Wine and Beverage Service | Spring |
| HFT1213 | Beverage Sanitation and Safety | Fall, Spring |
| HFT1287 | Introduction to Craft Beer Production | Spring |
| HFT2009 | Hospitality Professionalism | Spring |
| HFT2282 | Hospitality Supervision | **Fall, Spring, Summer** |
| HFT2671 | Event Risk Management | Fall, Spring |
| HFT2780 | Introduction to Gaming Operations | Fall, Spring |
| HFT2804 | Introduction to Beverage Science | Fall |
| HFT2822 | Brewery Operations | Spring |
| HFT2860 | Beverage Service Management | ⚠ **not stated** |

### ✅ Batch 95: third consecutive prefix priced entirely from the live corpus

**No DSC HFT page publishes contact hours.** All ten values came from tier 2 of the hour-source hierarchy,
and the split is the cleanest yet recorded:

| Form | Live sample | Ratio |
|---|---|---|
| **Unsuffixed** (HFT1000, 1410, 1860, 2276, 2454, 2500, 3373, 3700, 4064, 4253, 4277, 4809) | **12 courses** | **15.0 hrs/cr — 12/12, no exception** |
| **C-suffixed** (HFT2750C, HFT2867C) | 2 courses | 20.0 hrs/cr — 2/2 |

Twelve concurring data points is the largest uniformity sample this project has used to anchor a ratio.
**New pinned ratios: DSC HFT unsuffixed = 15 hrs/cr, C-suffixed = 20 hrs/cr.**

Worth noting alongside RTV (20 hrs/cr) and STS: **the DSC ratio is prefix-specific, not institution-wide.**
RTV's unsuffixed courses run at 20 where HFT's run at 15. **Never carry a DSC ratio across prefixes** —
derive it from the prefix's own live corpus each time.

### ⚠⚠ Batch 95: "lab in the description, no lab in the number" — the inverse of the RTV1520C case

Four of the ten courses **describe laboratory or production work in the catalog text** while being
published as **unsuffixed** three-credit courses:

| Course | Catalog wording |
|---|---|
| HFT1021 | "classroom activity, discussion **and lab**" |
| HFT1287 | "learn in the classroom **and lab** … prepare pilot and quantity batches of beer" |
| HFT2822 | "class lectures **and lab time** will focus on operating a professional brewery" |
| HFT2804 | students "manage yeast used to brew commercial quantities of beer" |

This is the **mirror image** of the RTV1520C finding in batch 93, where the *queue* carried a C form and
DSC published the number unsuffixed. Here the *description* carries lab content and the *number* does not.

**Resolution, consistent with Rule 22: the number governs.** These were priced at the unsuffixed
convention (45 hrs), with the practical work delivered inside the standard hours rather than as a
separately timetabled laboratory. A **⚠ block was written into all four guides** explaining that the
absence of a C is not cosmetic and that **a receiving institution carrying the same subject as a
C-suffixed course is carrying a different SCNS number**, so equivalency does not automatically cross.

**Generalisable instruction: read the description for content and the number for structure, and when they
disagree, say so in the guide rather than silently reconciling them.** Both directions of this mismatch
have now been seen within three batches, so it is a recurring pattern rather than a one-off.

### ⚠ Batch 95: HFT2860 — a catalog entry with a title and a credit value and no description

`HFT2860 Beverage Service Management` publishes **title and credits only**; the description field is
empty. This is a first for the project — previous gaps have been missing *hours* or missing *terms*, not
a missing description.

**Handled by writing the gap into the guide rather than around it.** The guide states plainly that the
catalog publishes no description, that the outcomes and topics are **indicative of the subject rather than
transcribed from a published outline**, and that the reader should confirm the syllabus with the
instructor. Content was derived from three defensible anchors: the course title, its credit value, and
**its position in a sequence whose neighbours are all live** — above HFT1021 and HFT1860, below the
upper-division HFT4064 (Bar and Beverage Management).

**Standing practice this establishes: when a catalog field is empty, the guide says so.** Inventing a
description and presenting it as the institution's would be the failure mode; declining to write the
course would leave a prefix incomplete for a recoverable reason. Say what is known, name what is not.

### Batch 95: a craft-brewing programme sitting inside the hospitality prefix

Six of the ten courses form a **commercial brewing sequence** — HFT1213 (sanitation) → HFT1287
(production) → HFT2804 (fermentation science / yeast management) → HFT2822 (operations), with HFT1021 and
HFT2860 on the service side. This is a genuine technical programme carried under a hospitality prefix, and
it needed content flags that no previous HFT or hospitality batch has required.

**⚠⚠ Brewery hazards — an industrial environment, not a kitchen.** Written into four guides:

- **Carbon dioxide is the one that kills** — heavier than air, odourless, collects in cellars and tanks,
  displaces oxygen without warning. Monitors, ventilation, never alone in a low space.
- **Confined space entry** (tanks, vessels) requires permit, testing, and an attendant — **vessel entry
  has killed experienced brewery workers.**
- **Caustic and acid burns** — the characteristic injury; alkali burns keep damaging tissue after contact
  and may not hurt immediately. **Always chemical into water, never the reverse; never mix chemistries**
  (acid + chlorine sanitiser produces chlorine gas, which has killed people in food service).
- Plus scalds, pressurised vessels, combustible grain dust, lockout-tagout, and packaging-hall noise.

**⚠⚠ Commercial brewing is federally licensed.** TTB Brewer's Notice *plus* Florida DBPR/ABT licensing
*plus* local zoning — all three before a drop is sold; federal excise tax with real recordkeeping burden;
TTB label approval; Florida's three-tier system with its brewpub and taproom exceptions. And the point
students most often miss: **home brewing is legal within limits and is not a licence to sell.** Flagged
Rule 11 emphatically — Florida's taproom, growler, and distribution law has changed repeatedly.

### ⚠⚠ Batch 95: Florida alcohol law — the server-liability rule is *narrower* than most states'

Written into every beverage guide, and it is a genuinely Florida-specific fact that national material
gets wrong:

- Under **§ 768.125, Florida Statutes**, a seller is generally **not** liable for injury caused by an
  intoxicated *adult* patron — **unlike the broad dram shop liability most states impose.**
- **But liability does attach for serving a person not of lawful drinking age, and for knowingly serving
  a person habitually addicted to alcohol.** Those two exceptions are the whole of the exposure, which is
  why **checking identification is the single most consequential thing a server does.**
- **Florida's Responsible Vendor programme** (§ 561.705) gives trained licensees protection against
  certain penalties — cheap, and employers value it.
- **⚠ Florida's minimum age to sell or serve alcohol is separate from the 21 drinking age**, which has
  direct consequences for tasting components of beverage and brewing courses. Every relevant guide tells
  students to confirm with the programme what someone under 21 may do. **Deliberately not stated as a
  specific age** — the rules differ by role and setting and were not verified against the statute here.

**⚠⚠ Florida gaming law (HFT2780) got the strongest Rule 11 flag in the repository.** Tribal gaming under
IGRA and state compacts, separate from pari-mutuel and cardroom activity; compact arrangements, sports
betting authority, and permitted game scope **repeatedly litigated and repeatedly changed**; constitutional
amendment constraints unique to Florida. The guide says explicitly that **any specific statement about
what is currently lawful has a real chance of being out of date** and directs readers to the Florida
Gaming Control Commission. Also flagged: **gaming employment requires occupational licensing and
background screening, and a criminal record can disqualify** — worth knowing before investing in the
pathway.

### Batch 95: Florida-specific event risk (HFT2671) — weather is the real content

**Florida has the highest lightning density in the United States**, and outdoor events here plan for it as
routine. The guide gives the practical shape: **set lightning thresholds and a stop rule in advance, in
writing**, because nobody makes a good decision about stopping a show with ten thousand people watching.
Plus heat illness (staff in costume are at particular risk and are routinely overlooked), near-daily
summer afternoon thunderstorms, **hurricane season overlapping the autumn event calendar** (force majeure
clauses, a defined cancellation trigger, a named decision-maker), and wind loading on temporary structures
— **a tent is a sail.**

This is the clearest case yet of a course whose generic national content becomes substantially more useful
when written for Florida specifically.

### Batch 96: DSC **PGY** prefix completed — and the first prefix whose hour ratio is *split*, not uniform

Eight guides pushed, all v1.0, all clean, all live. **The PGY prefix is complete**: 20 pushed, 4 skipped,
0 queued. Four prefixes completed in four consecutive batches (PHT, RTV, STS, HFT, PGY).

| Course | Title | cr | hrs | Lab fee | Basis |
|---|---|---|---|---|---|
| PGY1201C | Studio and Location Lighting | 3 | 60 | $95 | studio 20 |
| PGY1209 | Intermediate Studio and Location Lighting | 2 | 40 | $35 | studio 20 |
| PGY1850 | Multimedia Production | 2 | 40 | $30 | studio 20 |
| PGY2107 | Commercial/Illustration Photography | 4 | 80 | — | studio 20 |
| PGY2116 | Color and Design | 2 | 40 | $30 | studio 20 |
| **PGY2160** | **Camera Culture** | **3** | **45** | **none** | **lecture 15** |
| PGY2207 | Lens-Based Practices: Art and Commerce | 4 | 80 | $100 | studio 20 |
| **PGY2273** | **Professional Strategies for Photographers** | **3** | **45** | **none** | **lecture 15** |

### ⚠⚠ Batch 96: PGY is the first prefix found to run **two** hour conventions — and the lab fee is the tell

Batches 93–95 each derived a single uniform prefix ratio from the live corpus (RTV 20, HFT 15/20 by
suffix, STS 15/30 by suffix). **PGY breaks that shape: the split is not by suffix.**

| Convention | Live evidence | Ratio |
|---|---|---|
| **Studio / production** | PGY1100C, **PGY1101**, PGY1800C, PGY1802C, PGY2210C, PGY2470C, **PGY2650**, PGY2750C, PGY2801C, PGY2806C | **20 hrs/cr** |
| **Survey / lecture** | **PGY2000** (3/45), **PGY2270** (2/30) | **15 hrs/cr** |

Note that **PGY1101 and PGY2650 are unsuffixed and run at 20**, while **PGY2000 and PGY2270 are also
unsuffixed and run at 15**. So the C suffix does *not* predict the ratio here — it is the *nature of the
course* that does.

**⚠⚠ The discriminator that actually works: the laboratory fee.** Every studio-convention course in this
prefix carries a lab fee; **PGY2000 and PGY2270 carry none, and neither do PGY2160 and PGY2273**, the two
courses in this batch priced at 15. The fee is the institution's own signal that a course consumes
studio, lighting, or lab resources.

**New standing heuristic: when a prefix's live ratio is split and the suffix does not explain it, check
the laboratory fee.** A fee means hands-on and the higher rate; no fee, plus a description built on
lecture, seminar, guest speakers, or survey content, means the lower rate. Both courses priced at 15 in
this batch were confirmed independently by their descriptions — PGY2160 is critical theory, PGY2273 is
business practice delivered through "guest lectures, field trips and professional seminars".

**Also worth carrying: a prefix ratio must be tested for uniformity before use, not assumed.** Had the 20
figure been applied prefix-wide from the majority of the sample, PGY2160 and PGY2273 would each have been
published 15 hours over.

### ⚠⚠ Batch 96: PGY2107 and PGY2207 carry **identical description text** — the fifth catalog copy-paste

Daytona State publishes the *same* description verbatim for two different 4-credit courses:

> "Concepts, techniques and applications for commercial illustrative photography emphasizing advanced
> lighting and creative problem solving for portraiture, architecture, landscape and still life
> photography in the studio and on location."

| Course | Prerequisites | Coreq | Terms | Fee |
|---|---|---|---|---|
| **PGY2107** Commercial/Illustration | **PGY2210 + PGY2650** | — | Spring | — |
| **PGY2207** Lens-Based Practices: Art and Commerce | PGY1800 + PGY2650 | **DIG2030** | Fall, Spring | $100 |

**Resolved by prerequisite chain**, as with ARR0382C. PGY2107 requires **PGY2210 Professional Studio
Portraiture** (an advanced 4-credit studio course); PGY2207 requires only the introductory PGY1800.
**PGY2107 therefore sits later in the chain and is the advanced commercial studio course**; PGY2207 is
the earlier course, paired with digital media via its DIG2030 corequisite, and its *title* — "Art and
Commerce" — names the subject the shared description fails to capture.

This is the **fifth** instance of *the prerequisite chain is a more reliable indicator of a course's role
than its title or description* (after PHT2810/2820, MSS0157, EET4732C, ARR0382C), and the **second** where
the description itself is the duplicated field. Both guides carry the comparison table and tell the
reader to confirm the syllabus with the instructor, since the catalog cannot settle it.

### ⚠⚠ Batch 96: PGY2107's prerequisite has a *higher* number than the course

**PGY2107 requires PGY2210.** The prerequisite's number is 103 higher than the course that depends on it.

This is a cleaner instance than the PHT2810/2820 case recorded at batch ~73 (where a course titled "II"
was the third rotation). Here the *numeric order is simply reversed* against the actual sequence. A
⚠ block was added to the level-transfer section of **every guide in this batch** stating that **in this
prefix the number does not indicate sequence — sequence by the prerequisite chain**.

Generalisable: **never infer course order from numeric order within a prefix.** The SCNS first digit
carries year-of-offering meaning; the remaining three digits carry none.

### Batch 96: content flags for photography, and two that are Florida-specific

**⚠⚠ Copyright registration is the photographer's decisive business fact.** Copyright vests automatically
at the moment of capture — but **registering with the U.S. Copyright Office *before* an infringement
unlocks statutory damages and attorney's fees.** Without timely registration a photographer is generally
limited to actual damages, which for a single image are usually too small to make litigation viable —
**so the infringement simply goes unremedied.** Most photographers learn this too late. Paired with:
group registration in batches, work-for-hire clauses that transfer ownership permanently, and the
principle that **you license usage, you do not sell photographs** — so pricing follows usage.

**⚠⚠ Model and property releases protect against right-of-publicity and privacy claims, not copyright
ones** — photographers conflate these constantly. Commercial use of a recognisable person generally needs
a release; **editorial use generally does not**, which is why the same photograph can run in a news story
and not in an advertisement. Minors need a guardian's signature.

**⚠⚠ Two Florida-specific rules, written into the relevant guides:**

- **Florida is an all-party consent state for audio recording** (§ 934.03) — carried over from batch 93's
  RTV work, and it becomes live in **PGY1850 Multimedia Production**, where a photography course starts
  capturing interview audio. Most states require one party's consent; photographers trained on national
  material get this wrong, and violation is criminal.
- **⚠⚠ Florida restricts drone surveillance specifically** — the **Freedom from Unwarranted Surveillance
  Act (§ 934.50)** limits using a drone to record people or private property where there is a reasonable
  expectation of privacy, and creates a **private right of action**. This sits *on top of* FAA Part 107,
  not instead of it. First time this statute has appeared in the corpus; it belongs in any photography,
  surveying, real-estate, or media guide touching aerial work.

**⚠ Florida sales tax on photographers** (PGY2273) — sales of tangible items such as prints are generally
taxable, and the treatment of services, digital delivery, and bundled charges is more complicated.
Flagged as a common and expensive new-photographer mistake, with Rule 11 and a direction to the Florida
Department of Revenue. Also noted: **Florida has no state personal income tax, but federal
self-employment tax still applies** with quarterly estimated payments.

**⚠⚠ Image manipulation standards differ by context** (PGY2160) — photojournalism permits global
adjustments and forbids adding or removing elements, with photographers dismissed and awards withdrawn
over a single removed object; advertising permits extensive manipulation. **The claim made about an image
is what matters, not the compositing itself.** Flagged Rule 11 because generative imagery has made this
urgent and publications and competitions are actively revising their rules.

### Batch 97: DSC **OTH** prefix completed — and the lab-fee heuristic gets its first real test

Seven guides pushed, all v1.0, all clean, all live. **The OTH prefix is complete**: 16 pushed, 1 skipped,
0 queued. **Six consecutive prefix completions** (PHT, RTV, STS, HFT, PGY, OTH).

| Course | cr | hrs | Fee | Basis for hours |
|---|---|---|---|---|
| OTH1003C | 3 | 60 | — | C-form convention (20/cr) |
| OTH1006 | 2 | 30 | none | lecture convention (15/cr) |
| **OTH1802** | 2 | **90** | $11 | **level I fieldwork (45/cr) from OTH1800** |
| OTH2264C | 3 | 60 | $17 | C-form; matches its own prerequisite OTH2261C exactly |
| OTH2300C | 4 | 80 | $5 | C-form convention |
| **OTH2410** | 3 | **45** | **$64.99** | **lecture convention despite the largest fee in the prefix** |
| **OTH2704C** | 4 | **80** | **none** | **C-form convention despite no fee** |

### ⚠⚠ Batch 97: the lab-fee heuristic is a *tiebreaker*, not a rule — two courses proved it

Batch 96 established from PGY that **when a prefix's ratio splits and the suffix does not explain it,
the laboratory fee discriminates hands-on from lecture.** This batch contained the two cases that test
that heuristic in both directions, and both broke it:

| Course | Fee | Suffix | Description | Priced at |
|---|---|---|---|---|
| **OTH2410** Conditions in OT | **$64.99** — largest in the prefix | none | pure pathology lecture: *"etiology, diagnosis, detection, medical management and prognosis"* — no lab language at all | **lecture, 15/cr** |
| **OTH2704C** Advanced Practice | **none** | **C** | clinical scenarios, integration lab work | **C-form, 20/cr** |

**Resolution, and the corrected hierarchy:**

1. **The suffix governs first.** OTH2704C carries a C in Daytona State's own number, so it is an
   integrated lecture-and-laboratory course whatever the fee schedule says. Rule 22 again: the suffix is
   part of the number, and a fee is not.
2. **The fee is consulted only when the number is unsuffixed and the description is ambiguous.**
3. **⚠ And the fee's *shape* matters, not merely its presence.** The other OTH fees are **$5, $11, $17** —
   small round amounts consistent with laboratory consumables. **$64.99 is a retail price point**,
   consistent with required courseware or a digital licence rather than lab materials. Reading it as a
   lab signal would have published OTH2410 fifteen hours over.

**Standing refinement recorded: suffix → description → fee, in that order — and a fee ending in .99 is
courseware, not consumables.** Both guides state the reasoning for the reader and tell them to confirm
with the programme, per the standing rule that a convention may be overridden only when the reasoning is
written into the guide.

### ✅ Batch 97: level I vs level II fieldwork pricing, confirmed a third time

OTH1802 was priced from **OTH1800 (1 cr / 45 hrs)** — its own direct prerequisite, the strongest anchor
in the hierarchy. That gives 2 cr → **90 hours**, and it sits cleanly between the two clinical rates
already pinned in this prefix:

| Course | Type | cr | hrs | Ratio |
|---|---|---|---|---|
| OTH1800 (live) | level I fieldwork | 1 | 45 | **45** |
| **OTH1802** (this batch) | level I fieldwork | 2 | **90** | **45** |
| OTH2840 / OTH2841 (live) | level II fieldwork | 5 | 320 | **64** |

This confirms the **batch-87 finding** (level I and level II clinical hours are priced differently) for a
third prefix, after OTH and PHT. **The generalisation now holds across three institutions' worth of
evidence: within one allied-health prefix, expect at least two distinct clinical ratios**, and check
which tier a fieldwork course belongs to before applying either.

Full OTH ratio set now pinned: **C-form skills 20, lecture 15, level I fieldwork 45, level II clinical
64.** Four conventions in one prefix — the most of any prefix recorded.

### Batch 97: two suffix divergences, handled per the standing rule

**OTH1003C** and **OTH2300C** are queue C forms where Daytona State publishes the number unsuffixed
(OTH1003, OTH2300). Handled as at batches 83/93/95 — the DSC entry is evidence about *content*, the
suffix about *structure*; priced at the C-form convention with the distinction written into the guide.

Worth noting for OTH2300: **the DSC description itself says "Labs provide opportunities to observe and
practise specific techniques"** while the number is unsuffixed and the fee is $5. This is the batch-95
"lab in the description, no lab in the number" pattern appearing a third time. It is now common enough
to treat as expected rather than remarkable.

### Batch 97: content flags for occupational therapy and allied health generally

**⚠⚠ ACOTE → NBCOT → Florida licensure.** Structurally identical to the CAPTE trap (PHT) and CAAHEP trap
(STS) already recorded — **eligibility for the COTA examination requires graduation from an ACOTE-accredited
programme, and it is unrecoverable after the fact.** This is now the **third** allied-health prefix where
the same accreditation-gates-certification-gates-licensure chain applies, and it should be written into
every allied-health guide as standard. Added here: **ACOTE sets a time limit for completing level II
fieldwork after coursework ends** — a student who interrupts study between the two can find the pathway
closed, which is a failure mode students do not anticipate.

**⚠⚠ "Skilled care" is what documentation must demonstrate** (OTH1006). The sharpest formulation found so
far, and it generalises to every reimbursed therapy prefix: *"Client performed 10 repetitions" documents
an activity; "Client required verbal and tactile cueing for sequencing; cues faded to intermittent verbal
by third trial" documents skill.* A payer asks one question — **did this require the skill of a therapy
practitioner?** — and if the documented activity could have been supervised by a family member, it is not
reimbursable whatever actually happened in the room.

Paired with the legal framing: **the record is evidence read years later by people who were not there**;
never document in advance or alter retrospectively; **fraud exposure is personal**, with individual
practitioners prosecuted, **particularly in Florida therapy settings which have been a sustained
enforcement focus.**

**⚠⚠ Physical agent modalities are the most regulation-sensitive content in the OTA curriculum**
(OTH2264C). What you are taught is not automatically what you may do — jurisdictions impose additional
training, documented service competency, or supervision conditions before an OTA may apply modalities,
and **a classroom demonstration is not authorisation.** Flagged Rule 11 hard, with the profession's own
position noted: modalities are *preparatory to occupation*, not an intervention in themselves.

**⚠⚠ Florida's Baker Act (§ 394.463) and Marchman Act (Chapter 397)** (OTH2300C) — first appearance in
the corpus. Involuntary examination for mental illness and substance-related intervention respectively.
**Initiating these is not the OTA's role; recognising a situation and escalating it is** — and
understanding the framework lets a practitioner explain to a frightened client and family what is
happening. Belongs in any Florida mental health, nursing, human services, or criminal justice guide.
Paired with: **asking directly about suicidal thoughts does not plant the idea** — a persistent myth
worth contradicting explicitly — and **do not agree to keep safety information secret.**

**⚠⚠ Productivity pressure is the ethical problem practitioners actually face** (OTH2704C). Being
pressured to bill time not spent, treat clients who no longer need therapy, or document more than
occurred — all three are fraud with personal exposure. Written with the practical advice to **ask about
productivity expectations at interview**, since the answer characterises the employer.

### Batch 98: DSC **CET** — 10 courses, 50 of 52 now live, and the first upper-division BAS batch

Ten guides pushed, all v1.0, all clean, all live. **CET is now 50 pushed / 1 skipped / 1 queued** — the
remaining `CET3383C` (Software Engineering, 2 institutions) is **not in the Daytona State index** and
needs a different holder identified.

| Course | cr | hrs | Level | Basis |
|---|---|---|---|---|
| CET2154C | 4 | 90 | lower | 4-cr C form, subject family |
| CET2850 | 3 | 45 | lower | unsuffixed 15/cr |
| CET3116 | 4 | 60 | **upper** | unsuffixed 15/cr |
| CET3198 | 2 | 30 | **upper** | unsuffixed 15/cr |
| CET3198L | 1 | 30 | **upper** | L-suffix 30/cr |
| CET4138C | 3 | 60 | **upper** | 3-cr C form 20/cr |
| CET4860 / 4861 / 4862 / 4884 | 3 | 45 | **upper** | unsuffixed 15/cr |

### ✅ Batch 98: the cleanest unsuffixed-ratio evidence in the project

The live CET corpus gave **eight unsuffixed 3-credit courses all published at exactly 45 hours** —
CET1588, CET2544, CET2691, CET2792, CET2793, CET2794, CET3505, CET4542 — with **no exception anywhere in
the prefix**. That is the largest single-value sample used to anchor a ratio so far, and it held across
the 1000-to-4000 level range, which is itself worth noting: **the unsuffixed convention did not shift at
the lower-division / upper-division boundary.**

Full CET ratio set now pinned: **unsuffixed 15, three-credit C form 20, L-suffixed 30, four-credit C form
75 or 90.**

⚠ The four-credit C forms are the one genuinely split case: CET1020C, CET1113C, CET1114C and CET2113C are
75 hours; CET1110C, CET1171C, CET1172C and CET2114C are 90. **CET2154C was priced at 90 on a
subject-family anchor** — CET1171C and CET1172C ("Computer Service & Support: PC Systems") are the
nearest subject match and both are 4/90. Reasoning written into the guide.

### ⚠⚠ Batch 98: CET2154 — suffix *and* title both diverge, in opposite directions

The most tangled identity case since the EML3015/3016 collision.

| Source | Number | Title |
|---|---|---|
| Statewide inventory (queue) | **CET2154C** | **"A+: Computer Operating Systems"** |
| Daytona State catalog | **CET2154** | **"Computer Hardware & Software"** |

The catalog **description** settles the substance and it favours the *statewide* title: the content is
Windows installation and configuration, an introduction to Linux, anti-virus and firewall software, and
explicit preparation for the **A+ Software examination**. Daytona State's own title ("Hardware &
Software") is the broader and less accurate of the two.

**This is the first case where the DSC title is the weaker description of the course.** The standing
Tier-0 rule (DSC catalog is authoritative) has generally meant taking the DSC title over the queue title
— as an earlier batch correctly did for RTV2600C. Here the DSC title was retained for consistency with
that rule, **but the guide states both titles explicitly and tells the reader that the description, not
either title, is what determines equivalency.**

**Refinement worth recording: Tier 0 settles *facts* (credits, prerequisites, terms, description), not
necessarily the *best label*. When the two published titles disagree and the description favours the
non-DSC one, say so in the guide rather than silently picking a side.**

### Batch 98: "hands-on in the description, unsuffixed in the number" — fourth instance

CET4860, CET4861 and CET4862 are all described as hands-on (CET4861: *"a hands-on learning experience"*;
CET4862: *"This hands-on course…"*) while being **unsuffixed** courses. Priced at the unsuffixed
convention per Rule 22, consistent with the resolution used at batches 93, 95 and 97.

This pattern has now appeared in **four consecutive prefixes** (RTV, HFT, OTH, CET) in both directions.
It is fully routine and needs no further special handling — **read the description for content, the
number for structure.**

### ⚠⚠ Batch 98: two Florida statutes new to the corpus

**Chapter 815, Florida Statutes — the Florida Computer Crimes Act.** Written into every security guide in
this batch. Unauthorised access is an offence under **state** law independently of the federal Computer
Fraud and Abuse Act, and **a student who assumes only federal law applies is wrong.** Paired with the
practical framing that curiosity and good intent are not defences, that scope must be in writing before
any authorised engagement, and that the programme's isolated lab exists precisely so techniques that
would be unlawful elsewhere can be practised lawfully.

**§ 501.171, Florida Statutes — the Florida Information Protection Act.** Breach notification to affected
individuals, and above a threshold to the Department of Legal Affairs, within a statutory period. Written
into CET4862 (incident response) with the observation that **the notification clock is a legal exposure
technical responders routinely overlook** — the incident is being worked while a statutory deadline runs.
Rule 11 flagged; the specific day-count was deliberately not stated.

Both belong in any future CIS, CTS, CCJ, CGS, or ISM guide touching security or investigation.

### Batch 98: content flags for forensics, incident response, and security management

**⚠⚠ Chain of custody and admissibility** — written into all four forensics and security guides. *An
analysis that cannot be defended in a hearing is an analysis that did not happen.* Never work on the
original; write-block; hash before and after and record the values in your own notes, not only the tool's
log; document custody continuously because **a single unexplained gap can exclude the evidence entirely**;
contemporaneous notes are the deliverable because you may testify years later. Plus: **report findings
that do not support the theory you were asked about** — selective reporting is how examiners are
discredited. Noted that **Florida's expert-testimony standard has changed in recent years**, with Rule 11
rather than a claim about the current test.

**⚠⚠ Containment versus evidence preservation** (CET4862) — the two goals of incident response conflict
directly, and **the organisation decides the priority in advance, in the plan, not the responder under
pressure.** Network isolation is often better containment than powering off because it preserves memory.
And: **assume the attacker is reading your internal communications if they still have access — use
out-of-band channels.**

**⚠⚠ Memory forensics and the power-off decision** (CET4861) — a great deal of modern intrusion activity
never touches disk, and **encryption keys live in memory while a volume is mounted**, so powering down an
encrypted machine can make the disk permanently unreadable. One of the most consequential on-scene
decisions in the field. Also flagged: **live acquisition alters the system you are acquiring from**, and
the resolution is documentation rather than avoidance.

**⚠ Mobile forensics honesty** — a locked modern device may be unrecoverable by any lawful means
available, and **the guide says so plainly rather than implying otherwise.** Isolate immediately
(Faraday bag) because **a connected phone can be remotely wiped**, which has destroyed evidence in real
cases.

**⚠ CET4884's prerequisite is a writing course** (GEB3213 or ENC2210), not a technical one — which
identifies it as the **management and governance** course of the sequence. The guide leads with that
inference: *executives decide on risk, cost and consequence, not on vulnerabilities*, and **get risk
acceptance in writing.** This is another instance of the standing principle that **the prerequisite chain
tells you what a course actually is** — here, an unusually clean one, since the prerequisite's *subject*
rather than its level carried the signal.

### Batch 99: DSC **ACR** (HVAC/R) — a second complete PSAV trade programme

Seven guides pushed, all v1.0, all clean, all live. **ACR is now 16 pushed / 1 skipped / 3 queued** —
the three remaining (ACR0002C, ACR0062C, ACR0601C) are **not in the Daytona State index**, consistent
with the earlier note in this file that they "were still not found".

| Course | Clock hrs | Lab fee | Prereq | Coreq |
|---|---|---|---|---|
| ACR0550C Introduction to HVAC | 187.5 | $328.70 | — | ⚠ ACR0551C |
| ACR0551C Fundamentals of HVAC | 187.5 | $385.68 | ⚠ ACR0550C | — |
| ACR0561C Residential Air Conditioning II | 187.5 | **$406.81** | ACR0560C | — |
| ACR0613C Advanced Technology | 150 | $365.37 | ACR0561C | ACR0810C |
| ACR0810C Advanced Service Practice | 150 | $314.86 | ACR0613C | (of 0613C) |
| ACR0744C Commercial Refrigeration I | 150 | $347.04 | ACR0561C | ACR0746C |
| ACR0746C Commercial Refrigeration II | 150 | $372.68 | ACR0744C | (of 0744C) |

All seven are **0000-level PSAV**, `credits: 0`, with DSC again rendering clock hours under a
"Credit Hours" heading — 187.5 and 150. The batch-82 rule applied cleanly for the second complete trade
programme after STS.

### ⚠⚠ Batch 99: a genuine catalog contradiction — ACR0550C and ACR0551C are each other's dependency

**Daytona State lists ACR0551C as ACR0550C's corequisite, while also listing ACR0550C as ACR0551C's
prerequisite.** Those cannot both be true: a corequisite is taken alongside, a prerequisite before.

This is **structurally different from the mutual corequisite pair found at batch 93** (RTV2534 ↔ RTV2540),
which was coherent — two peer courses each requiring the other's co-enrolment. Here the two statements
are **logically inconsistent with each other**, not merely unusual.

Resolved by reading the evidence that agrees: **the course titles (Introduction, then Fundamentals) and
the prerequisite direction both indicate a sequence**, so the sequential reading is the likely intent and
the corequisite entry is likely the error. **Both guides state the contradiction explicitly and tell the
reader to confirm the enrolment requirement with the programme** rather than silently picking one.

**New check worth running: when a course lists a corequisite, look up the named course and confirm the
relationship is reciprocal or absent — not contradictory.** This is the first inconsistency of this kind
found, and it was only visible because the whole prefix was fetched in one batch. **Prefix-completion
batches surface catalog self-contradictions that single-course work cannot.**

### ⚠⚠ Batch 99: the lab fees are the real cost of this programme, and they are large

| Course | Fee |
|---|---|
| ACR0550C | $328.70 |
| ACR0551C | $385.68 |
| ACR0561C | $406.81 |
| ACR0613C | $365.37 |
| ACR0744C | $347.04 |
| ACR0746C | $372.68 |
| ACR0810C | $314.86 |
| **Total across these seven** | **$2,521.14** |

**Over $2,500 in laboratory fees alone**, before tuition, tools, textbooks, or certification examination
fees — and this is a programme marketed on low tuition. Every guide carries a **⚠⚠ budgeting block**
telling students to obtain a complete cost sheet before enrolling rather than discovering the fees term
by term, and noting that tools are an additional personal cost employers expect you to arrive with.

**Generalisable: for PSAV trade programmes, the published fee is material information and belongs in the
guide.** Contrast the OTH and PGY prefixes where fees were $5–$100 and largely incidental. **A fee over
roughly $300 per course changes the enrolment decision and should be stated with its total.**

### Batch 99: certifications embedded in the coursework — the strongest case yet for naming them

Unusually, this programme's catalog descriptions **name the certifications each course carries**:

| Course | Certifications available |
|---|---|
| ACR0550C | **OSHA 10 Construction Site Safety**, ESCO Brazing and Soldering |
| ACR0551C | ESCO System Recovery and Evacuation |
| ACR0561C | **EPA 608 Refrigerant Handling** |
| ACR0613C | ESCO Gas Heat, ESCO Heat Pump |

**⚠⚠ EPA Section 608 is a legal requirement, not a credential.** Under the Clean Air Act, certification is
required to service equipment containing regulated refrigerants **and to purchase refrigerant at all** —
without it a technician cannot lawfully do the central task of the trade. It does not expire, which makes
it unusually good value. **Venting regulated refrigerant is a federal violation with the obligation
falling on the individual technician as well as the employer.**

This is a different shape from the accreditation traps recorded for PHT/STS/OTH (CAPTE, CAAHEP, ACOTE),
where the *programme's* accreditation gates the examination. Here **the certification is the licence to
perform the work itself**, earned inside the coursework. Worth distinguishing the two patterns when
writing any career-certificate guide.

### ⚠⚠ Batch 99: the refrigerant transition — a live regulatory change written into the guides

Refrigerants are being phased down under federal law and **many replacements are classified as mildly
flammable**, which changes service procedures, tooling, leak detection, ventilation, and ignition-source
precautions from what the trade has assumed for decades. Written into ACR0746C with the practical
framing: **do not apply old habits to new equipment**; recovery equipment, detectors and gauges may need
to be rated for the refrigerant class; read the equipment literature and the safety data sheet as a
routine step rather than a precaution. Flagged Rule 11 emphatically, with **no specific phasedown dates
or refrigerant designations asserted** — the schedules are actively changing and were not verified here.

Noted as a genuine employability point: **training on the new refrigerants is an advantage right now
because the existing workforce broadly has not had it.**

### Batch 99: trade-safety content that generalises to any Florida building-trades prefix

- **⚠⚠ Refrigerant hurts you three ways** — *asphyxiation* (heavier than air, displaces oxygen in crawl
  spaces and machine rooms; **people have died without feeling short of breath**, because it is not toxic
  and gives no warning), *frostbite* (liquid flashing to gas, permanent eye injury), and *pressure*
  (never heat a cylinder, never exceed 80% fill, **always use a regulator on nitrogen — a full cylinder
  connected directly will rupture a system explosively and this has killed technicians**).
- **⚠⚠ Capacitors store a lethal charge after the power is off.** Electrocution is a leading cause of
  death in this trade, and the run capacitor is the specific hazard technicians underestimate. Paired
  with: test the meter, test the circuit, test the meter again; one hand in a pocket; the disconnect may
  not de-energise control circuits and crankcase heaters.
- **⚠⚠ Florida attics exceed 130°F and approach 150°F**, and a large share of residential HVAC work
  happens in them. **Heat stroke — confusion, hot dry skin, no sweating — is a medical emergency**, and
  *confusion in a hot attic is an emergency, not tiredness*. Work attics early; never alone without
  someone knowing; **the person suffering heat illness is frequently the last to recognise it.** This is
  the clearest Florida-specific occupational hazard found in any trade prefix so far and belongs in
  BCT, BCN, ELE, PMT, and roofing-adjacent guides too.
- **⚠⚠ Carbon monoxide (ACR0613C)** — the one fault that kills the customer rather than the equipment.
  **Shut down and red-tag an unsafe appliance and do not restore it because the customer objects**; a
  technician who leaves a known unsafe appliance in service carries personal responsibility.

### ⚠⚠ Batch 99: Florida contractor licensing — Chapter 489, and the distinction students get wrong

**Working as a technician for a licensed contractor requires no licence of your own; contracting on your
own account does.** Air conditioning contracting is regulated under **Chapter 489, Florida Statutes**
through DBPR and the Construction Industry Licensing Board, and **unlicensed contracting is an offence
with escalating penalties.** Licensure requires documented years of experience, an examination, financial
responsibility evidence, and insurance — **which is why the realistic sequence is certificate → employment
→ licence, not certificate → business.** Licence classes and their capacity limits were deliberately not
stated numerically; Rule 11 with a direction to DBPR.

Belongs in every future BCT, BCN, ELE, PMT, and building-trades guide.

### Batch 100: DSC **PMT** (Precision Metals) — 11 courses, a third complete PSAV trade programme

Eleven guides pushed, all v1.0, all clean, all live. **PMT is now 23 pushed / 1 skipped / 1 queued** —
the remaining `PMT0211C` (Precision Machining I, 2 institutions) is **not in the Daytona State index**.

Two distinct sub-programmes in one prefix:

| Welding | Hours | Fee | | Machining | Hours | Fee |
|---|---|---|---|---|---|---|
| PMT0106C Intro to Welding I | 90 | **$463.42** | | PMT0202C Intro to Machining | 150 | $190.25 |
| PMT0154C Welding IV (Plasma/MIG) | 90 | $392.32 | | PMT0215C Manual Machining | **280** | $80.00 |
| PMT0109C Intro to Welding II | 90 | $422.32 | | PMT0251C CNC Mill | 150 | $133.25 |
| PMT0171C Welding VIII (TIG/Pipe) | 95 | $393.12 | | PMT0720C CNC Lathe | 150 | $133.25 |
| | | | | PMT0260C CAD/CAM | 150 | $108.25 |
| | | | | PMT0228C EDM | 130 | $76.55 |
| | | | | PMT0265C CNC Multi-Axis | **280** | $80.00 |

All eleven are 0000-level PSAV, `credits: 0`. **Welding fees total $1,671.18; machining $801.55.**

### ⚠⚠ Batch 100: the roman numerals in the welding titles do not track the sequence at all

The most extreme title-versus-sequence inversion found in the project.

| Course | Title | Prerequisite | Corequisite |
|---|---|---|---|
| PMT0106C | Introduction to Welding **I** | — | — |
| PMT0154C | Welding **IV** | — | **PMT0106C** |
| PMT0109C | Introduction to Welding **II** | **PMT0154C** | — |
| PMT0171C | Welding **VIII** | — | PMT0134C |

**"Welding IV" is a corequisite of "Introduction to Welding I", and both precede "Introduction to
Welding II".** The numerals are not merely a poor guide to the order — they actively contradict it.

Previous instances of this principle (PHT2820 titled "II" but the third rotation; PGY2107 requiring the
higher-numbered PGY2210) involved a *single* inversion. Here **an entire title series is decoupled from
the enrolment chain.** A sequence table was written into all four welding guides, and this is now the
strongest available evidence for the standing rule: **sequence by the prerequisite and corequisite
chain, never by numerals in titles or by numeric order.**

### ⚠⚠ Batch 100: PMT0215C carries PMT0251C's description — sixth catalog copy-paste

**Daytona State's entry for PMT0215C "Manual Machining and Lab" describes CNC programming for vertical
milling machines** — substantially the same text published for **PMT0251C "CNC Mill and Lab"**.

Resolved by three converging pieces of evidence, all pointing the same way:

1. **The title** is unambiguous — "Manual Machining".
2. **The prerequisite chain** fits: PMT0202C (saws, drill press, layout, measurement) → conventional
   lathe and mill.
3. **⚠ The hours and the fee fit** — 280 hours is a long foundational course consistent with building
   manual skill, and the **$80 fee is far below the $133.25 charged for each CNC course**, whose tooling
   and inserts cost more.

**That third signal is new.** Previous wrong-description cases (ARR0382C, PGY2107/2207) were resolved on
the prerequisite chain alone. Here **the lab fee acted as independent corroborating evidence about what
a course actually is** — a use for the fee beyond the hour-ratio tiebreaker established at batches 96–97.

**Refinement: the published fee is evidence about a course's content and resource profile, not only its
contact hours.** A course whose fee is out of line with its claimed subject is worth a second look.

Guide written to describe manual machining, with the discrepancy stated plainly and the reader told to
confirm the syllabus with the instructor.

### Batch 100: certification structures — two different shapes in one prefix

**⚠⚠ Welder qualification is per-process, per-position, per-material, and it lapses.** This is a genuinely
different credential structure from anything else in the corpus:

- A welder is **never certified in general** — qualification binds to a process (SMAW/GMAW/GTAW/FCAW), a
  position (1G–6G), a material and thickness range, and a welding procedure specification.
- **⚠ It lapses if the process is not used** within a defined recent period (commonly cited as six
  months), so **a welder returning after time off the tools may find their qualification invalid.**
- It is typically **employer-held and code-specific** — AWS D1.1 for structural, ASME BPVC for pressure,
  API for pipeline — so changing employer usually means retesting, and that is normal.
- **6G pipe is the qualification that opens the best-paid work.**

**NIMS credentials (machining) are the opposite shape** — they do not expire, and they combine a written
examination with a **performance test where you make a part and it is measured**. That combination is
precisely why employers value them: the credential certifies you can hold a tolerance, not describe how.

Contrast both with the two patterns already recorded: **programme-accreditation gates** (CAPTE/CAAHEP/
ACOTE — the *programme's* status gates examination eligibility) and **legal-requirement certifications**
(EPA 608 — the certification *is* the licence to do the work). **Four distinct credential structures now
documented; worth identifying which applies before writing any career-certificate guide.**

### Batch 100: trade-safety content, and the one rule that matters most

**⚠⚠ Rotating machinery — never wear gloves, long sleeves, jewellery, or loose hair near a lathe.**
Entanglement is the classic fatal machining accident: it is fast, and nothing done afterwards helps.
Paired with: never clear chips by hand (razor-sharp and hot); stop the machine before measuring; remove
the chuck key before starting; know where the emergency stop is *before* you start.

**⚠⚠ Welding fume is the hazard that harms you over years and the one students ignore.** Manganese
neurological effects; **stainless produces hexavalent chromium, a known carcinogen**; galvanised coating
produces zinc fume and metal fume fever. Local exhaust, head out of the plume. Plus: **never weld or cut
on a container that held anything flammable, even one that appears empty** — residual vapour explodes and
has killed people repeatedly; **hot work needs a fire watch because the fire frequently starts after the
welder has gone home**; **never exceed 15 psi on acetylene.**

**⚠⚠ CNC prove-out** — a machine will drive a tool through a vice at full rapid without hesitation. Single
block, low overrides, hand on feed hold, every new program. **A wrong tool length offset is the most
common cause of a crash**, and on multi-axis machines **you cannot visualise the collision** — full
machine simulation including fixture and clamps becomes mandatory rather than advisable.

Two craft observations worth carrying to any welding or machining guide: **MIG's danger is that a bad
weld looks good** (cold lap produces a smooth, evenly rippled, structurally worthless bead — break your
practice coupons), and **in pipe welding the root pass is the weld**, where nearly all test rejections
originate.

### Batch 100: milestone — 100 batches

This is the hundredth recorded batch. Six prefixes were completed in the preceding seven batches
(PHT, RTV, STS, HFT, PGY, OTH), and three complete PSAV trade programmes are now published as coherent
units (STS surgical technology, ACR HVAC/R, PMT precision metals). **The live corpus has been the sole
source of contact-hour ratios for every batch since 93** — no external hour data has been needed for
eight consecutive batches.

### Batch 101: DSC **BCA** — starting the 56-course apprenticeship block (9 pushed)

Nine guides pushed, all v1.0, all clean, all live. **BCA is now 20 pushed / 47 queued** — this batch
opens the largest single remaining block in the queue.

**What BCA actually is:** a **registered apprenticeship** prefix — electrical (union *and* non-union
tracks) and plumbing, numbered as sequential terms, each classroom course paired with a `L` **Lab-OJT**
course carrying on-the-job training hours. All 0000-level PSAV, `credits: 0`.

This batch covers the **union electrical classroom sequence**, all at **99 clock hours**:

| Course | Level | Term | Content |
|---|---|---|---|
| BCA0330 | 1 | Fall | Basic electricity, installation methods, first aid, DC theory |
| BCA0331 | 2 | Spring | Job safety and OSHA, basic wiring, calculations, materials, blueprint symbols |
| BCA0332 | **3** ⚠ | not stated | ⚠ **no description published** |
| BCA0333 | 4 | Fall | Resistors, inductors, capacitors, transformers, vectors |
| BCA0334 | 5 | Spring | AC theory, NEC interpretation, transformers, CPR |
| BCA0336 | 7 | Fall | Grounding and bonding, NEC application, test instruments |
| BCA0337 | 8 | Spring | Transformers, fire alarm, telephone/security, structured cabling |
| BCA0338 | 9 | Summer | Lightning protection, motors and controls, automation, photovoltaics, power quality |
| BCA0339 | 10 | Summer | Advanced electricity, raceways, wiring, equipment |

### ⚠⚠ Batch 101: BCA0332 — a duplicate title corrected from two independent signals

**Daytona State titles BCA0332 "Electrical Academy Union Apprentice 2", duplicating BCA0331 exactly**,
and publishes **no description and no term** for it.

Two independent pieces of evidence establish it is **level 3**:

1. **The course-number-to-level offset holds for every other course in the series** — BCA033*n* is level
   *n*+1, confirmed across eight titles (0330→1, 0331→2, 0333→4, 0334→5, 0336→7, 0337→8, 0338→9,
   0339→10).
2. **The paired laboratory BCA0332L is titled "Electrical Academy Union Apprentice 3 Lab-OJT."**

Published as **level 3**, with both the duplicate title and the missing description stated plainly in the
guide and a direction to confirm with the programme. Outcomes and topics are labelled **indicative**,
derived from the course's position between BCA0331 and BCA0333 — the same honest treatment given to
HFT2860 at batch 95.

**Generalisable: a sequential series with a consistent number-to-level offset is itself evidence**, and a
paired L-course's title is independent corroboration. **Where a whole series is fetched together, an
error in one member becomes visible against the pattern of the others** — the third finding in three
batches (after the ACR0550C/0551C contradiction and the PMT0215C misplaced description) that
**prefix-block fetching surfaces catalog errors single-course work cannot.**

### Batch 101: the apprenticeship structure — a course type new to the corpus

Registered apprenticeship is genuinely different from every other programme type documented here, and
the guides lead with it:

- **The student is a paid employee first.** Apprentices work full time for a contractor and attend
  classroom instruction alongside it, typically evenings. **Earn while you learn, no student debt.**
- **Wages step up on a schedule** as a percentage of the journeyman rate, so advancement is directly
  financial.
- **Two mandatory components** — related classroom instruction (these courses) and **OJT hours** (the
  paired `L` courses). **Neither substitutes for the other**, and the OJT component is far larger:
  **BCA0330L alone is published at 679.8 clock hours** against the classroom course's 99.
- **Sponsor-run and competitive.** A joint labour-management committee or contractor association
  controls entry; there are typically far more applicants than places, and **reapplying is normal.**
- **Four to five years**, and the people who complete are the ones who kept attending class after a full
  day on site.
- **Portable across states** through DOL/Florida DOE registration, unlike a local certificate.

**This is a fifth distinct credential structure**, after programme-accreditation gates (CAPTE/CAAHEP/
ACOTE), legal-requirement certifications (EPA 608), per-process lapsing qualifications (AWS welding), and
non-expiring performance credentials (NIMS).

### ⚠⚠ Batch 101: Florida electrical licensing — journeyman is *county*, contracting is *state*

A genuinely non-obvious Florida fact, written into all nine guides:

- **Journeyman electrician licensing in Florida is generally handled at county or municipal level**, not
  by the state. Requirements, examinations, and reciprocity vary between jurisdictions, and **a journeyman
  card from one county may not be recognised in the next.**
- **Electrical *contracting* is state-licensed** under **Chapter 489, Part II, Florida Statutes**, through
  DBPR and the Electrical Contractors' Licensing Board, with certified (statewide) and registered (local)
  categories differing in where you may work.
- Working as an electrician for a licensed contractor requires no licence of your own; **contracting on
  your own account without one is an offence.**

Consequence written into BCA0339: **completing the apprenticeship and passing the journeyman examination
are separate achievements**, and the candidate must find out *which jurisdiction's* examination applies.

### ⚠⚠ Batch 101: arc flash — the electrical hazard that is not shock

Written into all nine guides, and it is the one apprentices underestimate:

- **An arcing fault is an explosion**, not a shock — temperatures several times hotter than the surface of
  the sun, a pressure blast, molten metal, and sound loud enough to cause permanent hearing damage.
  **It burns through ordinary clothing instantly and synthetic fabric melts into skin.**
- **Arc-rated clothing is not optional** near energised equipment, and **cotton is not arc-rated**.
  **NFPA 70E** governs boundaries, risk assessment, and protection.
- **Test the meter on a known live source, test the conductor, then test the meter again** — a failed
  meter reading zero has killed people.
- **De-energise wherever possible**; working energised requires justification, and **schedule pressure is
  not one — that pressure is exactly when incidents happen.**

### Batch 101: the NEC as a career-long tool

**The NEC is adopted into the Florida Building Code with state amendments**, so what governs here is the
NEC *as Florida has adopted it*. Revised on a three-year cycle, **and jurisdictions adopt editions at
different times — the edition in force where you are working is the one that governs**, frequently not
the newest.

The framing that matters for students: **nobody memorises the NEC; the skill is navigation.** Journeyman
examinations are **open-book and timed**, so they test lookup speed — *an apprentice who knows the answer
but takes four minutes to find the article will fail.* Tab the book, learn the chapter structure, and
practise against a clock.

### Remaining BCA work

47 queued, in three further blocks: **union electrical Lab-OJT (12)**, **non-union electrical (13)**, and
**plumbing (22)**. The Lab-OJT courses carry the large OJT hour figures (679.8 for BCA0330L) and will
need their own fetches — the hours vary by level and cannot be assumed.

### Batch 102: DSC **BCA** — the union electrical Lab-OJT block (12 pushed)

Twelve guides pushed, all v1.0, all clean, all live. **BCA is now 32 pushed / 35 queued** — the union
electrical track (classroom + OJT) is complete.

| Course | Level | Term | Clock hours | Description published |
|---|---|---|---|---|
| BCA0330L | 1 | Fall | 679.8 | ✅ specific |
| BCA0331L | 2 | Spring | 679.8 | ✅ specific |
| BCA0332L | 3 | Summer | 639.9 | boilerplate only |
| BCA0333L | 4 | Fall | 679.8 | ✅ specific |
| BCA0334L | 5 | Spring | 679.8 | ✅ specific |
| BCA0335L | 6 | Summer | 639.9 | boilerplate only |
| BCA0336L | 7 | Fall | 679.8 | ✅ specific |
| BCA0337L | 8 | Spring | 679.8 | ✅ specific |
| BCA0338L | 9 | Summer | 639.9 | boilerplate only |
| BCA0339L | 10 | Summer | **679.8** ⚠ | ✅ specific |
| BCA0390L | 11 | Spring | 679.8 | ✅✅ **substantive new content** |
| BCA0391L | 12 | Spring | **639.9** ⚠ | boilerplate only |

### ✅ Batch 102: BCA0332L confirms the batch-101 title correction

Batch 101 published **BCA0332 as level 3** against its catalog title of "Apprentice 2", on the strength of
the number-to-level offset and the paired lab's title. **This batch fetched that lab directly and Daytona
State titles it "Electrical Academy Union Apprentice 3 Lab-OJT"** — confirming the correction from the
primary source rather than by inference.

**Worth naming as a method: when a catalog error is suspected in one member of a series, the paired
L-course is an independent witness.** Classroom and laboratory titles are maintained as separate records
and an error in one does not automatically propagate to the other.

### ⚠ Batch 102: OJT hours track the *term*, not the level — with two exceptions

A clean pattern, and a genuinely new kind of hour convention for this corpus:

- **Fall and spring terms: 679.8 clock hours**
- **Summer terms: 639.9 clock hours**

The figure reflects **term length**, which makes sense for on-the-job training — the hours are what an
apprentice accrues working through the term, and summer terms are shorter.

**⚠ The pattern holds for ten of twelve.** **BCA0339L** is published at 679.8 despite being a summer term,
and **BCA0391L** at 639.9 despite being spring. Both figures are the catalog's own and were published as
found; the sequence table in every guide shows all twelve so a reader can see the exceptions.

**Instruction recorded: state the pattern, publish the catalog's figures, and show the exceptions rather
than smoothing them.** An apparent rule that holds for 10 of 12 is a useful observation, not a licence to
correct the outliers.

### ⚠⚠ Batch 102: OJT hours are the binding constraint — the framing these guides lead with

The single most useful thing a prospective apprentice can understand, and it is written into all twelve:

- **You can pass every class and still not complete the apprenticeship.** The classroom course is 99
  hours; **the OJT course is 640–680.** The hours on the job are the bulk of the programme.
- **Hours accrue only while employed by a participating contractor.** **⚠ If you are laid off, your hours
  stop** — a real risk in a cyclical trade. Tell the sponsor immediately; re-placement is part of what
  they exist for.
- **⚠⚠ Breadth is required, not just total hours.** Apprenticeship standards specify **work processes** —
  categories you must actually be exposed to. **Three years doing only one task does not satisfy the
  requirement however many hours it produces**, and *nobody will notice the gap for you*. The guides tell
  apprentices to audit this at the midpoint (level 5) and again before completion.
- **Keep your own copy of the hour record.** Employers change, sponsor staff change, records are lost.

### Batch 102: how to write an OJT course honestly when the catalog gives boilerplate

Four courses (0332L, 0335L, 0338L, 0391L) carry only the standard wording — *"apply knowledge gained in
class related instruction and knowledge gained on-the-job"* — with no topics named.

**Rather than treating that as a gap to be filled by invention, the guides name it and reframe it
accurately:** the content of an OJT term genuinely *is* the work the apprentice is assigned, under a
journeyman, on live projects, and it varies by contractor and by what is being built. So the outcomes
describe **the obligations and competencies common to every OJT term** — safety, working from drawings,
receiving direction, recording hours and work processes, progression of independence — plus the paired
classroom level's content where the catalog names it.

**This is the third distinct honest-gap treatment in the corpus**, after HFT2860 (no description at all)
and BCA0332 (duplicate title, no description). The common rule: **say what the catalog publishes, say what
it does not, label derived content as indicative, and point the reader at who can confirm.**

### ⚠⚠ Batch 102: BCA0390L names the Journeyman Block Exam — and two high-stakes specialities

The only OJT course in the sequence with substantive published content beyond applying its classroom term.
It covers **NEC use in daily installations, Journeyman Block Exam preparation, electrical calculations,
hazardous locations, and health care facilities.**

The two named specialities are exactly where installation requirements are most stringent:

- **Hazardous locations** — classified by what is present and how often. **The classification determines
  the wiring method and is not a site judgement.** Seals, explosion-proof fittings, and listed equipment
  form a protection scheme that a single substituted fitting defeats. *"It fits" is not the test.*
- **Health care facilities** — redundant equipment grounding in patient care spaces exists **because
  patients may be directly connected to equipment and are far more vulnerable to small currents than a
  healthy person**; essential electrical systems must keep life-safety equipment running through a
  utility failure.

And the examination framing, which generalises to every open-book trade licensing examination:
**it tests navigation speed, not memory.** *An apprentice who knows the answer but takes four minutes to
find the article will fail.* Tab the book the same way every time, learn the chapter structure rather than
the contents, and drill calculations against a clock.

### Remaining BCA work

35 queued: **non-union electrical (13)** and **plumbing (22)**. The non-union track uses BCA0340–0343 and
BCA0350L–0357L; plumbing uses BCA0431–0435 and BCA0450L–0459L. Both will need their own fetches — the
non-union track's hour figures are not assumed to match the union track's, and **the live corpus already
shows non-union classroom courses at 72 hours against the union track's 99.**

### Batch 103: DSC **BCA** — the non-union electrical track (15 pushed)

Fifteen guides pushed, all v1.0, all clean, all live. **BCA is now 47 pushed / 20 queued** — **both
electrical tracks are complete**, leaving only the plumbing block.

| Level | Classroom | OJT | OJT hrs | Term |
|---|---|---|---|---|
| 1–2 | BCA0350/0351 (72, live) | BCA0350L / 0351L | 679.8 | Fall / Spring |
| 3 | BCA0352 | BCA0352L | 639.9 | Summer |
| 4–5 | BCA0353/0354 (72, live) | BCA0353L / 0354L | 679.8 | Fall / Spring |
| 6 | BCA0355 | BCA0355L | **639** ⚠ | Summer |
| 7–8 | BCA0356/0357 (72, live) | BCA0356L / 0357L | 679.8 | Fall / Spring |
| **9** | **BCA0340 (99)** ⚠ | BCA0340L | 639.9 | Summer |
| 10 | BCA0341 (99) | BCA0341L | 679.8 | Fall |
| 11 | BCA0342 (99) | BCA0342L | 679.8 | Spring |
| 12 | — | BCA0343L | 639.9 | Spring |

### ⚠⚠ Batch 103: BCA0340 titled "(Union)" in the non-union range — the paired-lab method again

**Daytona State titles BCA0340 "Electrical Apprentice 9 (Union)"**, publishes **no description and no
term**, and places it in the middle of the non-union number range.

Three pieces of evidence establish it belongs to the **non-union** track:

1. **Its own paired laboratory BCA0340L is titled "Electrical Apprentice 9 Lab-OJT (Non-Union)."**
2. **BCA0341 and BCA0342 are both explicitly "(Non-Union)"** and sit immediately after it.
3. **The union track uses an entirely separate number range** — BCA0330–0339 and BCA0390–0391.

Published as **"Electrical Apprentice 9 (Non-Union)"** with the discrepancy stated in the guide.

**This is the second use of the paired-L-course method in three batches** (after BCA0332), and it worked
identically both times. **Naming it as a technique: when a classroom course's title is doubtful, its
paired laboratory is an independent record.** The two are maintained separately, so an error in one does
not propagate — which is exactly what makes the lab a witness rather than an echo.

Both cases also shared a second symptom: **the course with the wrong title was also the one with no
published description.** Worth treating a missing description as a prompt to check the title.

### ⚠ Batch 103: BCA0355L is published at 639, not 639.9

Every other summer term across the entire BCA prefix — union and non-union, twelve instances — is
published at **639.9** clock hours. **BCA0355L alone is published at 639.**

Published as found, with a note in the guide stating that every comparable course uses 639.9 and directing
the reader to confirm with the sponsor. **Consistent with the batch-102 instruction: state the pattern,
publish the catalog's figure, show the exception rather than smoothing it.**

### ⚠⚠ Batch 103: the two apprenticeship tracks share early content and diverge at level 7

A genuinely useful structural finding, and the first direct comparison of two parallel tracks in the
corpus.

| Level | Union track | Non-union track |
|---|---|---|
| 1 | Basic electricity, installation, first aid, DC theory | **same** |
| 2 | Job safety/OSHA, basic wiring, calculations, materials, blueprints | **same** |
| 4 | Resistors, inductors, capacitors, transformers, vectors | **same** |
| 5 | Advanced theory, DC and AC complex circuits | **same** |
| **7** | **Grounding and bonding, NEC application, test instruments** | **Fire alarm, NEC, hazardous locations, auxiliary power** |
| **8** | **Transformers, fire alarm, telephone/security, structured cabling** | **Auxiliary power, generators, special occupancies/equipment/conditions** |
| 11 | NEC daily use, **Journeyman Block Exam prep**, hazardous locations, health care | Blueprint reading, **motor and transformer calculations**; OJT adds **effective foremanship** |

**Levels 1–5 are effectively identical; from level 7 the emphasis diverges and neither track is a subset
of the other.** Both cover the material eventually, in a different order. Written into every guide, with
the note that **a transfer between tracks would need the sponsor's assessment** rather than a
level-for-level swap.

**Also structural: classroom hours change partway through the non-union track** — levels 1–8 at **72**
clock hours, levels 9–11 at **99**. The union track is 99 throughout.

### Batch 103: writing about union and non-union tracks even-handedly

Both tracks are **registered apprenticeships** recognised through the Florida DOE and U.S. DOL, and both
produce a portable completion credential. The guides set out what actually differs — sponsor, employment
arrangement, wage structure — without advocating:

- **Union apprentices are generally dispatched to signatory contractors through the local; non-union
  apprentices are generally employed directly by a single contractor.**
- **⚠ That difference has a practical consequence the guides flag repeatedly: in the non-union track your
  hours depend on one employer**, so losing that job can stall the apprenticeship entirely — and **if the
  contractor specialises, you may accumulate hours in a narrow band and fail the work-process breadth
  requirement.** The level-5 guide tells apprentices to audit this at the midpoint specifically.
- **The licence does not distinguish between the tracks.** What matters is documented hours, completion,
  and the examination.
- Advice given: **choose on the specifics available to you** — which sponsor is accepting, which
  contractors are hiring, the wage progression, the training quality — **and ask to speak to current
  apprentices in either programme.**

### ⚠⚠ Batch 103: generator backfeed — a Florida-specific hazard worth carrying

Written into BCA0357L (auxiliary power, generators, special occupancies):

**A generator connected without proper transfer equipment can energise the utility supply, putting lethal
voltage onto lines utility workers believe are dead.** The transfer switch exists to make that
mechanically impossible, and **must never be defeated or bypassed.**

**⚠ Improvised generator connections are a recurring Florida problem after storms** — suicide cords and
unauthorised backfeeding through a receptacle have killed both homeowners and line workers. The guide
tells apprentices to say so plainly when they see one. Also flagged: **generators produce carbon
monoxide**, so siting, exhaust routing, and ventilation are safety-critical.

Belongs in any future guide touching standby power, emergency systems, or storm recovery work.

### Batch 103: "effective foremanship" — the only leadership content in the sequence

**BCA0342L (level 11) names "effective foremanship"**, and it is the only leadership content anywhere in
either apprenticeship track. The placement is deliberate — an eleventh-level apprentice is about to
become a journeyman, and journeymen run crews.

The guide treats it as the gap it is: **the industry promotes on technical skill and then expects
leadership to appear, which it does not.** Content covers planning the day before it starts (*most lost
productivity is planning failure, not effort failure*), confirming understanding rather than asking for
questions, genuine delegation (*a foreman doing the work themselves is a foreman not running the job* —
the commonest failure among newly promoted tradespeople), and **safety set by example: a crew watches
what the foreman actually does, and a corner cut once becomes the standard.**

### Remaining BCA work

**20 queued — the plumbing block:** BCA0431, 0431L, 0432, 0432L, 0433L, 0434, 0434L, 0435, 0435L, and
BCA0450L–0459L. The live corpus already shows plumbing classroom courses at **72** hours and BCA0431 was
fetched at **123** — so the plumbing track's hour conventions differ again and must be fetched, not
assumed.

### Batch 104: DSC **BCA** completed — the plumbing/pipefitting track (20 pushed)

Twenty guides pushed, all v1.0, all clean, all live. **BCA is now 67 pushed / 0 queued / 0 skipped —
the entire prefix is complete.** It was the largest single block in the queue at 56 courses when batch
101 opened it, and it took four batches: union electrical classroom (9), union electrical OJT (12),
non-union electrical (15), and plumbing (20).

**Classroom courses all at 123 clock hours**; OJT courses at 639.9, 640, 679.8, or 680.

### ⚠⚠ Batch 104: this is a fifteen-level programme, and it is pipefitting as much as plumbing

**Two structural facts a prospective apprentice needs and would not guess:**

1. **Fifteen levels, against twelve for both electrical tracks at the same institution** — roughly a
   five-year commitment.
2. **The content is heavily mechanical piping, not fixtures and drains.** Across the levels: hydronic
   heating and cooling, steam systems, refrigeration and air conditioning, pumps, chilled water,
   building automation and pneumatic controls, instrumentation and process control, plus **oxy-fuel
   cutting, shielded metal arc welding, and gas tungsten arc welding**.

Written into every guide: **read the level descriptions before assuming what the trade involves.** The
catalog's own language — "related to the piping industry", "labor history" in the level-2 lab — indicates
a **United Association-style combined plumbing and pipefitting apprenticeship.**

### ⚠⚠ Batch 104: medical gas piping requires a separate certification — the sharpest credential flag yet

**BCA0459L (level 10) includes medical gas piping installation.** This is the most tightly regulated work
a plumber can do, and the guide flags it hard:

- **Medical gas systems deliver oxygen and other gases directly to patients**, including in operating
  theatres and intensive care. **A cross-connected or contaminated system can kill patients, and has.**
- **⚠⚠ Under NFPA 99, installation and brazing must be performed by personnel qualified to the applicable
  ASSE 6000-series standards.** This is a **distinct credential from a plumbing qualification**, and
  **you may not lawfully do this work without it.**
- **Verification is performed by an independent party, not the installer** — precisely because
  self-certification is inadequate where patient lives are at stake.
- **Brazing must be done under continuous nitrogen purge**; without it copper oxide forms inside the pipe
  and particulate reaches patient outlets. **A patient safety requirement, not a quality preference.**
- **Oil or grease in an oxygen system is a fire and explosion hazard**, and hydrocarbon contamination of
  oxygen piping has caused fatal fires.

This is a **sixth distinct credential structure** for the corpus: a certification that is *narrower* than
the trade licence and gates one specific high-consequence activity within it. Distinct from
programme-accreditation gates (CAPTE/CAAHEP/ACOTE), whole-trade legal requirements (EPA 608), per-process
lapsing qualifications (AWS welding), non-expiring performance credentials (NIMS), and registered
apprenticeship itself.

### ⚠⚠ Batch 104: backflow and cross-connection control — public health, and a marketable certification

**BCA0434/0434L** cover backflow prevention, and the guides treat it as the public-health work it is:

- **A cross connection is any point where the potable supply can be contaminated**; backflow is what
  happens when pressure reverses and pulls that contamination into the drinking water. **Back-siphonage
  and backpressure incidents have contaminated public water supplies and caused mass illness.**
- **The air gap is the only absolute protection** — mechanical assemblies can fail; a physical air gap
  cannot be defeated by a pressure reversal.
- **Assembly type must match the hazard**, and selecting a lesser device for a high hazard is a serious
  error.
- **⚠ Testing backflow assemblies requires a certified tester**, on a schedule set by the utility and
  local jurisdiction. **This is a distinct and genuinely marketable credential with recurring demand** —
  assemblies must be retested, which creates ongoing work.

**Plumbing is a public health profession before it is a construction trade**, and the guides lead the
code block with that framing: trap seals, venting, and air gaps exist to keep sewer gas out of buildings
and contamination out of drinking water.

### ⚠⚠ Batch 104: trench collapse and confined space — the hazards that actually kill plumbers

Written into all twenty guides:

- **⚠⚠ Trench collapse.** **A cubic yard of soil weighs roughly as much as a small car**, and a collapse
  buries a worker faster than anyone can react — **you cannot dig someone out in time.** Protective
  systems are required at depth and spoil must be kept back from the edge. **Never enter an unprotected
  trench, whatever the schedule pressure and however briefly.**
- **⚠⚠ Confined spaces** — sewers, manholes, tanks, pits. **Hydrogen sulphide is lethal and deadens your
  sense of smell at dangerous concentrations, so you cannot rely on the smell warning you.** Permit,
  atmospheric testing, ventilation, and an attendant — and **never enter to rescue someone without
  proper equipment**, because would-be rescuers are a large share of confined-space deaths.
- **Steam: the leak you cannot see is the one that cuts you.** A steam leak is invisible near the
  orifice; the visible plume begins further away, and the invisible jet between will cut skin. **Never
  search for a steam leak with your hand.**
- Plus water heater relief valves (**never cap, plug, or omit a discharge**), fuel gas testing, sewage
  pathogens, and lead and asbestos in old buildings.

### Batch 104: a craft detail worth carrying — over-sloped drainage also blocks

A genuinely counter-intuitive point written into the level-4 lab guide: **under-sloped drainage does not
carry solids and they settle; over-sloped drainage lets the water outrun the solids, leaving them
behind.** Both block. **More slope is not better** — which surprises apprentices and is exactly the kind
of thing a guide should say plainly.

### ⚠ Batch 104: the catalog publishes the same nominal hours two ways

Across the plumbing block, **four courses are published as rounded values where the rest use decimals**:
BCA0454L and BCA0431L and BCA0432L at **680** against the usual **679.8**, and BCA0459L at **640**
against the usual **639.9**.

Combined with **BCA0355L at 639** found in batch 103, that is **five rounding inconsistencies across the
BCA prefix**. All published as found, with a note in each affected guide and the full sequence table so a
reader can see the pattern and the exceptions. **Consistent with the standing instruction: state the
pattern, publish the catalog's figure, show the exception rather than smoothing it.**

### The BCA prefix, completed — what four batches established

| Track | Levels | Classroom hrs | Courses |
|---|---|---|---|
| Union electrical | 12 | 99 | 21 |
| Non-union electrical | 12 | 72 (L1–8), 99 (L9–11) | 15 + live classroom |
| Plumbing / pipefitting | **15** | 123 | 20 |

**Three catalog errors were found and corrected**, all by the same method — **the paired L-course is an
independent witness to a classroom course's identity**:

- **BCA0332** titled "Apprentice 2" (duplicating BCA0331); its lab is titled "Apprentice 3". Published as
  level 3.
- **BCA0340** titled "(Union)" in the non-union range; its lab is titled "(Non-Union)". Published as
  non-union.
- Both had a **second shared symptom: no published description.** **A missing description is a prompt to
  check the title.**

**And the observation that made all three batches productive: prefix-block fetching surfaces catalog
self-contradictions that single-course work cannot.** An error in one member of a series is only visible
against the pattern of the others — which is an argument for continuing to work by block wherever the
queue allows it.

### Batch 105: queue policy change, and two prefixes completed (ETI + MSL, 12 pushed)

Twelve guides pushed, all v1.0, all clean, all live. **ETI is complete at 62 pushed / 0 queued** and
**MSL at 9 pushed / 0 queued.** The corpus passed **90% overall.**

### ⚠⚠ Standing policy change (Ron, 2026-09-03): no guides for courses without DSC coverage

**Ron's decision, and the reasoning behind it, changes how the remaining queue is treated:**

> "We will not produce a guide for those classes that have no DSC coverage. The plan is to move on to
> building for the next school (likely UWF, since they have easy to read courses well organized). Once we
> have solid coverage of the major schools, not 100% - just good coverage, we will generate guides upon
> request."

**44 queued courses were marked `skipped`** on this basis — every remaining queued course with no entry
in the Daytona State catalog index, and therefore no Tier-0 source. They were **marked, not deleted**,
with a note recording the reason and that they are deferred rather than abandoned. That keeps them
recoverable for the request-driven queue described below.

**The strategic shift this represents is worth naming.** Until now the queue has been
**catalog-driven** — build everything an institution offers, in priority order. Ron's plan is
**breadth across institutions first, then demand-driven depth**: good coverage of the major schools, then
guides generated from actual requests. **Chasing a single institution's long tail has a worse return than
starting the next institution's core**, and courses with no Tier-0 source are exactly that long tail.

⚠ **Two of the 44 are worth remembering: MEA0002C and MEA0520C, offered at 22 institutions each**
(Introduction to Medical Assisting; Phlebotomist). They are the strongest candidates in that set for
resurrection under the request feature, and were flagged as such in `FEATURE_BACKLOG.md`.

**Effect on the queue: 211 queued → 167**, and the denominator changed too — overall progress moved from
87.4% to 89.8% without a single guide being written, because the target set is now what is actually
buildable.

### Batch 105: "Request a Curriculum Guide" captured in FEATURE_BACKLOG.md as item 4

Ron's planned website feature was added to the backlog with its rationale, integration shape, and open
questions. **The key design point recorded there: the cleanest integration is an API endpoint the queue
tool reads**, adding open requests as queue rows with a priority derived from request volume — so
`queue_mgr.py` and the generation loop stay exactly as they are and **only the source of the queue
changes.** Precedent noted for the security shape (hashed reporter IP, rate limiting) from the existing
`ContentFlag` handling.

### Batch 105: ETI completed — a prefix spanning PSAV to bachelor's

ETI runs from **0000-level PSAV clock-hour certificates through to 4000-level BAS coursework**, an
unusually wide range for one prefix, and every guide in this batch carries a block explaining the three
tiers and warning that **a lower-division course does not substitute for its upper-division counterpart**
(ETI1420C vs ETI3421 being the live example).

| Course | cr | hrs | Note |
|---|---|---|---|
| ETI1851C Aerospace Mechanics and Mechanical Systems | 3 | 60 | C form; $20 fee |
| ETI2122 Product Testing and Quality Control | 3 | 45 | $18.30 fee, unsuffixed |
| ETI3421 Materials and Processes | 3 | 45 | upper division |
| ETI3690 Technical Sales | 3 | 45 | upper division |
| ETI4635 Technical Administration | 3 | 45 | upper division |
| ETI4640 Operations Management | 3 | 45 | upper division |
| ETI4704 Occupational Safety | 3 | 45 | ⚠ prereq is a *writing* course |

**ETI ratios pinned: unsuffixed 15 hrs/cr, C-suffixed 20 hrs/cr** (ETI1000/1411/1628/1644 all 3/45;
ETI1110C/1701C/1810C/1830C all 3/60).

⚠ **ETI2122 carries an $18.30 lab fee but is unsuffixed** — priced at the unsuffixed convention per the
batch-97 hierarchy (**suffix → description → fee**), with four live unsuffixed ETI courses at 45 hours
confirming it. **A fee does not override a suffix.**

⚠ **ETI4704's prerequisite is GEB3213, a business communications course** — the same signal that
identified CET4884 as a management course at batch 98. It marks this as a **policy and management
treatment of occupational safety, not hazard recognition**, and the guide says so and points students at
an OSHA 10/30 card as the separate practical credential. **Second instance of the prerequisite's
*subject* rather than its level identifying what a course actually is.**

### ⚠⚠ Batch 105: MSL — the ROTC obligation fact that stops people enrolling

**MSL1001C, MSL1002C, MSL2101C and MSL2102C are offered at 22 institutions each** — the most widely
offered courses remaining in the queue when this batch ran.

The most valuable content written into all five guides:

> **Taking a basic-course ROTC class does not commit you to military service.**

- **The basic course (first- and second-year MSL) is generally open to any enrolled student and carries
  no service obligation.** Students take it for the leadership content or to find out whether the pathway
  suits them, and then do not continue — **a normal and expected outcome, not a failure.**
- **The obligation attaches when you *contract*** — typically on entering the advanced course, or on
  accepting a scholarship. **⚠ Accepting scholarship money is a contracting event.**
- **Medical disqualification is the most common obstacle**, so establish eligibility in year one.
- Rule 11 flagged — ROTC obligations and eligibility are federal regulation and change.

**MSL3203 sits at the 3000 level and is therefore advanced-course**, so its guide carries the opposite
warning: enrolment there normally *does* require contracting.

### ⚠ Batch 105: MSL — 404 on the C-suffixed URL, and two titles per course

**All four C-suffixed MSL URLs returned 404; dropping the C worked immediately** — the standing rule from
the earlier SmartCatalog work, applied and confirmed again.

More interesting, **the statewide and Daytona titles differ for two of the four**:

| Number | Statewide inventory | Daytona State |
|---|---|---|
| MSL1001C | **Foundations of Officership** | Basic Military Science I |
| MSL2101C | **Individual Leadership Studies** | Basic Military Leadership I |
| MSL1002C / MSL2102C | Basic Leadership / Leadership and Teamwork | *same* |

**Published under the statewide titles**, departing from the CET2154C precedent at batch 98 (where the
DSC title was retained). The reasoning, recorded here so the inconsistency is deliberate rather than
accidental: **the statewide titles are the standard national Army ROTC curriculum names**, they are what a
student at any of the other 21 institutions will see, and **for a course offered at 22 institutions the
statewide label is the more useful identifier.** Both titles are tabulated in every guide.

**Refined instruction: prefer the DSC title by default (Tier 0), but prefer the statewide title where the
course is widely offered and the statewide name is the recognised national one.** State both either way.

⚠ **MSL3203 publishes no description, prerequisite, or term** — handled with the standing honest-gap
treatment: content labelled **indicative**, derived from the title and the 3000-level placement, with a
direction to confirm with the programme. Fourth instance after HFT2860, BCA0332, and BCA0340.

### Batch 105: content worth carrying

- **⚠⚠ Flight hardware discipline (ETI1851C)** — traceability is absolute, configuration control governs
  change, and **aerospace culture depends on people reporting mistakes nobody else saw.** Written for a
  Space Coast audience where the employers described are an hour's drive away.
- **⚠⚠ Control limits are not specification limits (ETI2122)** — the commonest misreading of a control
  chart. **Control limits come from the process; specification limits come from the customer**, and a
  process can be in control and still produce out-of-specification parts. Plus **tampering**: reacting to
  common-cause variation makes a process worse.
- **⚠⚠ Improving anything other than the bottleneck improves nothing (ETI4640)** — and **local efficiency
  measures drive the wrong behaviour**, because measuring every machine on utilisation makes operators run
  parts nobody needs.
- **⚠⚠ The hierarchy of controls, and why PPE gets the most effort (ETI4704)** — it is the least effective
  control and the cheapest, and it transfers responsibility to the worker. Also: **a low injury rate can
  coexist with severe process safety risk**, which several major industrial disasters demonstrated.
- **⚠⚠ Heat illness as a leader responsibility (MSL2102C)** — *confusion or odd behaviour in the heat is
  an emergency, not attitude*, and **the affected person is the last to recognise it.** Directly
  transferable to civilian outdoor work in Florida, and the third prefix in which this flag has been
  written (after ACR and PMT).
- **⚠ Technical sales is frequently the best-paid route out of a technical education (ETI3690)**, and
  students overlook it. The advantage a technical person brings is **diagnosis, not persuasion.**

### Batch 106: DSC **COS** barbering (6) + **CHD** early childhood (5) — both prefixes completed

Eleven guides pushed, all v1.0, all clean, all live. **COS is complete at 14 pushed / 2 skipped / 0
queued** and **CHD at 10 pushed / 1 skipped / 0 queued.**

| Barbering (PSAV, credits 0) | Clock hrs | Fee |
|---|---|---|
| COS0013L Barbering I Lab | 225 | **$863.51** ⚠ |
| COS0512L Barbering II Lab | 225 | $92.87 |
| COS0561L Barbering III Lab | 225 | $92.87 |
| COS0562L Barbering Lab Bridge: Shaves/Beards/Mustaches | 225 | $55.36 |
| COS0571L Barbering IV Lab | 225 | $91.19 |
| COS0580L Barbering Lab — Level V | 240 | $49.00 |

| Early childhood | cr | hrs |
|---|---|---|
| CHD1820 Introduction to ECE II | 3 | 45 |
| CHD2333 Creative Activities | 3 | 45 |
| CHD2335 Music and Motor Activities | 3 | 45 |
| CHD2338 Math and Science | 3 | 45 |
| **CHD2440 Child Development Practicum** | **6** | **270** ⚠ derived |

### ⚠⚠ Batch 106: COS0580L's prerequisites are one digit off the sequence

**Daytona State lists COS0580L's prerequisites as COS0012L, COS0511L, COS0560L and COS0570L.** The
barbering sequence — established from the catalog's own prerequisite chains on the other five courses —
runs **COS0013L → COS0512L → COS0561L → COS0571L**.

**Every one of the four listed prerequisites is exactly one digit lower than its counterpart in the
sequence.** A consistent offset across all four suggests either a superseded numbering series whose
references were never updated, or a parallel set of numbers.

**It cannot be resolved from the catalog alone**, so it was published as found with the discrepancy stated
plainly in the guide and a direction to confirm with the programme before planning a term around it.

**This is the fourth catalog self-contradiction found by fetching a whole prefix together**, after the
ACR0550C/0551C prerequisite-corequisite loop, PMT0215C's misplaced description, and the two BCA title
errors. **Consistent offsets are themselves evidence** — a single mismatched number could be a typo;
four in the same direction is a systematic artefact.

### ⚠⚠ Batch 106: the fee on the first barbering course is ten times the others

**$863.51 for COS0013L against $49–$93 for every subsequent course.** That distribution is consistent
with a **student kit** — clippers, shears, razors, supplies — rather than a term's consumables, and it
concentrates a large cost in the first term.

Written into the guide as a budgeting flag with the instruction to **ask exactly what the fee covers and
whether the kit is the student's to keep** before enrolling. **This extends the batch-99/100 practice
(publish the fee when it is material) with a new observation: the fee's *distribution across a sequence*
is itself informative.** A single outsized fee at the entry point almost always means equipment, and a
student budgeting term by term needs to know that before term one rather than during it.

### ⚠ Batch 106: CHD2440 — contact hours derived, and the derivation stated in the guide

**No CHD course provides an anchor for a practicum.** Every published CHD course is a 3-credit classroom
course at 45 hours (15 hrs/cr), and pricing a 6-credit supervised internship at the lecture convention
gives **90 hours — implausibly low.**

Priced at **270 hours**, from the **level I supervised fieldwork convention pinned at batch 97**
(Daytona State's OTH1800 is 1 credit / 45 hours), which also coincides with the common internship
convention of roughly three hours per week per credit across a term. **Two independent routes to the same
figure.**

**The guide states explicitly that this is a reasoned estimate rather than a published figure**, sets out
the derivation, and tells the reader to confirm with the programme. **This is the first time a contact-hour
figure has been derived across prefixes rather than within one**, and the standing rule that a convention
may be overridden only when the reasoning is written into the guide applies with extra force here.

### ⚠⚠ Batch 106: in Florida, *everyone* is a mandatory reporter of child abuse

The most important content in the CHD guides, and a genuinely Florida-specific fact:

- **Florida law requires *any person* who knows or has reasonable cause to suspect that a child is
  abused, abandoned, or neglected to report it.** Unlike many states, **the duty is not limited to
  designated professions — it applies to everyone.**
- **Florida Abuse Hotline: 1-800-96-ABUSE.**
- **⚠ You report suspicion, not proof.** Investigating is not the reporter's job and **attempting to
  investigate can compromise a later inquiry and put a child at greater risk.**
- **⚠ Telling a supervisor does not discharge the personal legal duty.** If you have the suspicion, the
  obligation is yours.
- Failure to report is an offence; good-faith reporters are protected.

Paired with **⚠⚠ Level 2 background screening**: fingerprint-based state and federal checks are required
before working with children in Florida, and **certain offences are permanently disqualifying** — so
eligibility should be established *before* investing in the programme. The same shape as the CAPTE/CAAHEP/
ACOTE accreditation traps: **unrecoverable if discovered late.**

Also flagged honestly in every CHD career list: **pay in early childhood is low relative to the
responsibility and training required.** That is well documented, students deserve to know it before
committing, and the guides name the routes that improve it (credentials, age-group specialisation, public
school, director roles).

### ⚠⚠ Batch 106: barbering breaks skin — which is why the trade is licensed

- **Barbering is regulated under Chapter 476, Florida Statutes, by the Barbers' Board; cosmetology
  separately under Chapter 477.** Different licences, different scopes, different hour requirements —
  and **holding one does not authorise the full scope of the other**, which is exactly why COS0562L
  exists as a bridge for licensed cosmetologists.
- **Sanitation is the most inspected and most consequential part of practice**, because razors and
  clippers nick skin and **blood exposure means hepatitis B, hepatitis C, and HIV risk.** Contact time on
  disinfectant is the most commonly violated requirement — *a wipe-and-go does not disinfect.*
- **⚠ Recognise and refer, but do not diagnose.** A barber must decline service on a contagious condition
  — servicing an infectious scalp spreads it through the implements — while **saying "that looks like
  ringworm" is a diagnosis and outside scope.** The guides give the wording that stays on the right side
  of both.
- **⚠⚠ The straight razor is the highest-risk service in the trade** (COS0562L) — an open blade over
  arteries. Single-use blades, absolute blade control, skin stretching, and a written nick procedure
  known before it is needed.
- **⚠⚠ Patch tests detect allergies that develop after years of uneventful use** (COS0571L). A client who
  has coloured their hair for a decade can react severely next time — **which is precisely why the test is
  required every time, not once.**

### Batch 106: craft content worth carrying

- **Speed comes from efficiency, not from rushing** (COS0561L) — have everything ready, work in a
  consistent order, do not re-cut what is already right. And the commercial point: **in a booth-rental
  trade the difference between forty minutes and twenty-five is the difference between two very different
  livings.**
- **Protect your body from day one** (COS0013L) — *raise the chair rather than lowering yourself* is the
  single most useful sentence for a trade whose practitioners are injured slowly.
- **Say what you see, not whether you like it** (CHD2333) — *"That's beautiful!" teaches a child to work
  for your approval*; describing what they did keeps the work theirs.
- **Use music for transitions** (CHD2335) — the most practical classroom tool in early childhood, and
  **singing rather than raising your voice** brings a room together more reliably than volume.
- **Resist answering the question** (CHD2338) — *"how could we find out?"* beats supplying the answer, and
  **wrong predictions are the valuable ones.**
- **⚠⚠ Food experiences are excellent learning and a real allergy risk** — check allergies at the
  *planning* stage so no child is excluded on the day, and treat cross-contamination as sufficient for a
  severe reaction.

### Batch 107: DSC **EET** (5) + **ETC** (5) — both prefixes completed

Ten guides pushed, all v1.0, all clean, all live. **EET is complete at 41 pushed / 0 queued** and
**ETC at 10 pushed / 0 queued.** Nine prefixes have now been finished in the last six batches.

| Course | cr | hrs | Basis |
|---|---|---|---|
| EET1607C Electronics Assembly and Cabling | 3 | 60 | C form 20/cr; $102 fee |
| EET3085L Electricity and Electronics Lab | 1 | 30 | ⚠ derived |
| EET4158L Linear Integrated Circuits Lab | 1 | 30 | ⚠ derived; **no description published** |
| EET4329C Communications Systems and Lab | 4 | 80 | C form 20/cr |
| EET4732L Feedback Control Systems Lab | 1 | 30 | ⚠ derived |
| ETC2245 Construction Methods | 3 | 45 | unsuffixed 15/cr |
| ETC4241 Construction Materials and Methods | 2 | 30 | unsuffixed 15/cr |
| ETC4241L …Lab | 1 | 30 | 1-credit lab convention |
| ETC4206 Construction Estimating | 3 | 45 | unsuffixed 15/cr; ⚠ **offered every two years** |
| ETC4415C Structural Concrete Design and Lab | 3 | 60 | C form 20/cr |

**Ratios pinned: EET C-suffixed = 20 hrs/cr** (eleven live courses at 3/60 and eight at 4/80 — the largest
C-form sample in the corpus). **ETC unsuffixed = 15, C-suffixed = 20.**

### ✅ Batch 107: a derived lab figure corroborated from inside the same prefix

**No live EET laboratory exists to anchor the three L-suffixed courses**, so the institution-wide
one-credit laboratory convention of **30 hours** was applied (CET1114L, CET3198L, PHT2211L, PHT2214L are
all 1/30).

**What makes this case stronger than a bare convention transfer is an internal check.** Daytona State
publishes the combined **EET3085C at 3 credits and 60 hours**. A split pair of a **2-credit lecture at the
15-hour convention (30 hours) plus a 1-credit laboratory at 30 hours** reproduces exactly 3 credits and
60 hours. **The combined course's published figures validate the derived split.**

**Worth naming as a technique: where a prefix publishes both a combined C form and a split lecture-plus-L
pair for the same subject, the C form's published total can be used to check a derived laboratory
figure.** All three EET L guides state the derivation and direct the reader to confirm.

### ⚠ Batch 107: three EET L-courses and their combined C-form twins — a Rule 22 cluster

Each of the three EET laboratories has a combined counterpart published by the same institution:

| Split pair | Combined form |
|---|---|
| EET3085 + EET3085L | **EET3085C** (3 cr / 60 hrs) |
| EET4158 + EET4158L | **EET4158C** (4 cr / 80 hrs) |
| EET4732 + EET4732L | **EET4732C** (4 cr / 80 hrs) |

**Under Rule 22 the split pair and the combined course are distinct SCNS numbers**, and a transfer
bringing one does not satisfy the other. Every guide says so. **This is the same structural situation as
the PHT prefix's paired numbers versus other institutions' C forms**, recorded at batch 74 — but here
*one institution publishes both structures simultaneously*, which is a first for the corpus.

⚠ **EET4732L reactivates a recorded finding.** SOURCES.md already documents that **EET4732 carries
substantially different subjects at different Florida institutions** — signals and systems at one,
feedback control at another. Daytona State publishes the combined **EET4732C as "Signals and Systems"**
while this laboratory is titled **"Feedback Control Systems Lab."** The guide flags that **the title alone
is an unreliable guide to content on this number** and tells the reader to read the description.

⚠ **EET4158L publishes no description** — handled with the standing honest-gap treatment: content labelled
indicative, derived from the title and its pairing with EET4158, with a direction to confirm. Fifth
instance after HFT2860, BCA0332, BCA0340, and MSL3203.

### ⚠⚠ Batch 107: ETC4206 is offered every two years

**Daytona State states explicitly that Construction Estimating is offered every two years.** This is the
first course in the corpus with a stated multi-year offering cycle, and it has real advising
consequences: **missing an offering delays graduation by two years rather than one term**, and the course
sits behind a prerequisite chain (ETC4241 and MAC1114) that must itself be timed.

Flagged prominently in the guide with an instruction to plan the degree around it and confirm the next
offering with an advisor.

**Generalisable: a stated offering frequency below once per year is advising-critical information and
belongs high in the guide, not in a footnote.** Worth watching for in other low-enrolment upper-division
courses.

### ⚠⚠ Batch 107: Florida's building code is shaped by wind — the strongest Florida-specific engineering content yet

Written into all five ETC guides:

- **Florida's wind design requirements are among the most demanding in the United States**, following
  directly from hurricane experience — Hurricane Andrew drove a fundamental revision of how buildings are
  designed and inspected here.
- **Wind load frequently governs rather than gravity load**, and **uplift is the characteristic problem**:
  wind lifts roofs off buildings.
- **⚠⚠ The continuous load path is the central concept** — roof to wall, wall to floor, floor to
  foundation — and **a single missing connection in that chain defeats every other connection in it.**
  Straps, hold-downs, and anchors exist for that reason.
- **High-Velocity Hurricane Zones** have their own requirements, with product approval required for
  windows, doors, and roofing before use.

Paired with the durability counterpart in ETC4241: **reinforced concrete in coastal Florida fails
principally through chloride-induced corrosion of the reinforcing steel.** Steel in sound concrete is
protected by alkalinity; chloride from salt spray destroys that protection; **corroding steel expands,
cracks the cover, admits more chloride, and the process becomes self-reinforcing.** Cover, low
permeability, and curing are the defences — and **in Florida heat, concrete that dries before it hydrates
is permanently more permeable.**

### Batch 107: engineering content worth carrying

- **⚠⚠ Under-reinforced design is deliberate** (ETC4415C) — steel must yield before concrete crushes,
  because **steel yielding is ductile and announces itself while concrete crushing is brittle and
  sudden.** An over-reinforced section is *stronger on paper and far more dangerous in reality*, which is
  why codes cap reinforcement ratios. And **bars in the wrong face is the classic catastrophic error** —
  reinforcement belongs where the tension is.
- **⚠⚠ An estimating error is discovered after you are contractually committed** (ETC4206) — the
  asymmetry that defines the discipline. **Omissions are more dangerous than arithmetic errors**, and
  **beware the winner's curse: the lowest bid frequently belongs to whoever made the largest mistake.**
  Also flagged: **Florida heat measurably reduces labour productivity**, so national average data
  under-prices summer work here.
- **⚠⚠ Solder fume causes occupational asthma** (EET1607C) — rosin flux fume is a recognised respiratory
  sensitiser, **sensitisation is permanent, and it can end a career in electronics assembly.** The fume is
  mostly flux, not lead, which is the part students get wrong.
- **⚠⚠ Oscilloscope grounds are earthed** (EET3085L) — clipping the ground lead to a point not at earth
  potential shorts through the instrument. One of the most common laboratory accidents, and worth knowing
  before the first probe.
- **⚠ Electrostatic discharge damage is latent** (EET1607C) — the device works, then fails weeks later in
  service. **Because nothing appears to go wrong at the bench, the discipline feels unnecessary** — which
  is precisely why manufacturers enforce it and hobbyists do not.
- **⚠⚠ Delay is the enemy of stability** (EET4732L) — enough phase shift turns negative feedback into
  positive feedback, which is why fast sensors and short loops matter. Plus the practical warning that a
  control loop driving a motor **can move violently during tuning.**
- **⚠⚠ Radio spectrum is regulated** (EET4329C) — laboratory work goes into a dummy load, not an antenna,
  and **an amateur radio licence is an inexpensive lawful route to hands-on transmitter experience.**

### Batch 108: DSC **FOS** baking/pastry (5) + **IND** interior design (5) — both prefixes completed

Ten guides pushed, all v1.0, all clean, all live. **FOS is complete at 9 pushed / 0 queued** and
**IND at 12 pushed / 2 skipped / 0 queued.** Eleven prefixes finished in the last seven batches.

| Course | cr | hrs | Fee | Basis |
|---|---|---|---|---|
| FOS1141 Introduction to Cakes | 3 | 60 | $150 | production 20/cr |
| FOS1151 Nutritional Baking | 3 | 60 | $150 | production 20/cr |
| FOS2140 Chocolate and Confections | 3 | 60 | $150 | production 20/cr |
| FOS2145 Dessert Production and Presentation | 4 | 80 | $150 | production 20/cr |
| FOS2146 Advanced Cakes | 3 | 60 | $150 | production 20/cr |
| IND1211 History of Architecture & Interiors | 3 | 45 | none | lecture 15/cr |
| IND1432 Lighting for Interior Design | 3 | 45 | $15 | lecture 15/cr |
| IND2408 Specialized Software | 3 | 60 | **$95** | applied 20/cr |
| IND2411 Materials and Estimating for Kitchen and Bath | 3 | 45 | $15 | lecture 15/cr |
| IND2414 Kitchen and Bath Design II | 3 | 60 | $15 | applied 20/cr |

### ✅ Batch 108: FOS reproduces the PGY split exactly — and the fee is again the discriminator

**FOS runs two conventions and neither is signalled by a suffix**: production courses at **20 hrs/cr**
(FOS1142 and FOS2147 at 3/60, FOS2161 at 4/80) and lecture at **15** (FOS1201, Sanitation and Safety, at
3/45). **All of these are unsuffixed**, exactly as in PGY at batch 96.

**And the discriminator is the same: every production course in the prefix carries a $150 laboratory
fee.** All five courses in this batch carry it; the lecture course does not. **This is the third
independent confirmation of the batch-96 heuristic** (after PGY and the OTH refinement), and the cleanest
— a single uniform fee value across every production course in a prefix.

### ⚠⚠ Batch 108: IND runs *three* conventions — the first three-way split in the corpus

| Convention | Live evidence | Ratio |
|---|---|---|
| **Studio** | IND1233C, IND2210C (both 3 cr / 90 hrs) | **30 hrs/cr** |
| **Graphics, software, applied project** | IND1300, IND1429C, IND2410C (all 3/60) | **20 hrs/cr** |
| **Lecture** | IND2220, IND2500 (both 3/45) | **15 hrs/cr** |

Every prefix documented until now has had one or two conventions. **IND has three**, and again **the
suffix does not reliably signal which** — IND1300 is unsuffixed at 20, IND2220 is unsuffixed at 15.

Resolved by the batch-97 hierarchy (**suffix → description → fee**) with the description carrying the
weight: IND1211 (history survey) and IND2411 (study of construction systems) are lecture; IND2408
(software instruction and projects) and IND2414 (*"complete design projects using industry standard CAD
program"*) are applied.

⚠ **The fee was informative only at the extremes here.** IND2408's **$95** is by far the highest in the
prefix and consistent with software licensing; **but $15 appears on three courses of quite different
character**, which makes it a token materials charge rather than a signal. **Refinement worth recording:
a fee discriminates only when it varies meaningfully across the prefix.** A flat nominal fee applied
broadly carries no information, and reading one as a lab signal would have mispriced two courses here.

### ⚠⚠ Batch 108: interior design is regulated in Florida — and students discover it late

**The most important content in the IND guides**, written into all five:

- **Florida is one of a minority of states that regulates interior design**, under **Chapter 481, Part I,
  Florida Statutes** — the same chapter that governs architecture — through DBPR and the **Board of
  Architecture and Interior Design**.
- **⚠ The regulation distinguishes residential from non-residential work**, and what a person may lawfully
  do — particularly in commercial interiors and particularly where drawings go for permit — depends on
  registration status.
- **The NCIDQ examination** is the recognised qualifying examination; **CIDA** accredits programmes, and
  **education requirements frequently reference accreditation** — the same unrecoverable trap already
  recorded for CAPTE, CAAHEP, and ACOTE in allied health.
- **An associate degree may not by itself satisfy the education requirement**, so the full pathway needs
  planning from the start.

Flagged Rule 11 emphatically: **this is a contested area of regulation in several states** and titles,
scopes, and requirements all change.

Paired with the substantive reason regulation exists: **interior design decisions are life-safety
decisions in commercial space.** Egress, fire ratings on finishes, and ADA accessibility all constrain
layout, and **a layout that blocks or lengthens egress is a defect, not a style choice.** That framing —
*the distinction between decoration and design is code compliance* — is the one worth carrying to any
future IND, ARC, or BCN guide.

### Batch 108: craft content worth carrying

- **⚠⚠ A bakery is close to a worst case for allergen management** (FOS1151) — wheat, egg, milk, nuts, and
  sesame are all routine, **flour becomes airborne and settles on everything**, and **cooking does not
  destroy most food allergens**. The operative concept is **cross-contact, not cross-contamination**: a
  shared sieve or a rack above a nut product is enough. And the professional instruction: **if you cannot
  be certain, say so plainly — an honest "I can't guarantee that" is professional; a hopeful yes is
  dangerous.**
- **⚠⚠ Tempering is temperature control, not technique** (FOS2140) — every method does the same thing
  (melt fully, cool to form crystals, warm to melt out the unstable ones). And **a single drop of water
  seizes chocolate irreversibly**, which is the failure students meet first. Plus: **molten sugar sticks
  to skin and keeps burning**, which makes it among the worst kitchen injuries.
- **⚠⚠ A tiered cake is a structure** (FOS2146) — cake compresses, so without internal support the lower
  tiers are crushed. **Assemble tall cakes at the venue, not the bakery.** And a genuinely Florida point:
  **heat and humidity are a structural problem** — buttercream softens, fondant sweats, gumpaste droops.
- **⚠ Design the plated dessert so it can be made the fiftieth time as well as the first** (FOS2145) — the
  design decision is *what can be prepared in advance*, and **a dessert with nine components will not
  survive a busy Saturday.**
- **⚠⚠ What is behind the wall determines what the design can cost** (IND2411) — **drainage constrains far
  more than supply**, because waste must fall at slope to an existing stack. And the Florida specific:
  **a great deal of Florida housing is slab-on-grade**, so relocating drainage means cutting and
  repouring the slab.
- **⚠ A rendering is a promise** (IND2408) — clients read one literally, and **the difference between the
  image and the built result is where disputes start.** Render what is specified, not a better-looking
  stand-in.
- **⚠ Check clearances with doors and drawers open, not closed** (IND2414) — the commonest failure in a
  student kitchen design, and obvious once built. Paired with the demographic point that **ageing-in-place
  design is a substantial and growing Florida market.**

### Batch 108: an honest career caution written into FOS

Every FOS career list closes with: **bakery work means very early starts, physical demands, and modest
starting pay; the progression is real but earned over years.** Same practice as the early-childhood pay
caution at batch 106 — **where a field's entry conditions are materially worse than a prospective student
would assume, the guide says so before they commit.**

### Batch 109: DSC **RET** (4) + **RTE** (4) + **CTS** (4) — three prefixes, all completed

Twelve guides pushed, all v1.0, all clean, all live. **RET is complete at 20 pushed / 0 queued**,
**RTE at 23 pushed / 0 queued**, **CTS at 24 pushed / 0 queued.** Fourteen prefixes finished in the
last eight batches.

| Course | cr | hrs | Basis |
|---|---|---|---|
| RET1021 Respiratory Care Introduction | 3 | 45 | unsuffixed lecture 15/cr |
| RET3041 Cardiopulmonary Education and Promotion | 3 | 45 | unsuffixed lecture 15/cr |
| RET4245 Advanced Life Support | 3 | 45 | unsuffixed 15/cr; corroborated by live RET2244C 3/45 |
| RET4354 Advanced Pharmacology | 3 | 45 | ⚠⚠ **detail page unreachable**; derived from RET2350 3/45 |
| RTE2623 Radiation Physics II | 2 | 30 | unsuffixed didactic ~15/cr |
| RTE3116 Advanced Patient Care | 3 | 45 | unsuffixed didactic; ⚠ no prereq or terms published |
| RTE3213 Radiology Information Systems | 3 | 45 | unsuffixed didactic |
| RTE4574 Advanced Imaging Modalities | 3 | 45 | unsuffixed didactic |
| CTS1851C Internet Web Foundations | 3 | 60 | C form 20/cr; ⚠ suffix **and** title divergence |
| CTS2308 Installing and Configuring Windows Workstation OS | 3 | 45 | unsuffixed 15/cr |
| CTS2353C Networking with Windows Server | 3 | 60 | C form 20/cr; ⚠ suffix **and** title divergence |
| CTS3348 Linux Administration | 3 | 45 | unsuffixed 15/cr |

**Ratios pinned this batch:**

- **RET runs three conventions**: unsuffixed lecture **15** (RET1295, RET2350 at 3/45; RET2483 at 2/30),
  C-suffixed **20** (RET1025C, RET1026C, RET1264C, RET1450C all at 3/60), and clinical **60**
  (RET1874 at 4/240, RET1875 at 3/180).
- **RTE runs four**: C-suffixed **~20**, L-suffixed laboratory **32** (RTE1111L, RTE1503L, RTE1513L all
  at 1/32), clinical **128** (RTE1804L at 1/128), and unsuffixed didactic **~15–16** (RTE1001 at 1/16).
  **⚠ RTE's L convention is 32 hours, not the institution-wide 30** — the first prefix in the corpus
  whose one-credit laboratory departs from the 30-hour figure used across CET, PHT, and ETC. Do not
  transfer the 30-hour convention into RTE.
- **CTS runs two**: C-suffixed **20** (CTS2302C, CTS2303C, CTS2321C, CTS2358C, CTS2370C, CTS2375C all at
  3/60 — a clean six-member sample) and unsuffixed **15** (CTS2214 at 3/45).

### ⚠⚠ Batch 109: the sixth honest-gap case, and the first where the *catalog page itself* is unreachable

**RET4354 (Advanced Pharmacology) appears in Daytona State's course index with that title, but its
catalog detail page does not resolve** — at `/ret4354/` or at `/ret4354c/`. This is distinct from the five
prior honest-gap cases (HFT2860, BCA0332, BCA0340, MSL3203, EET4158L), **all of which were published
pages carrying no description**. Here the page is absent entirely, so *credits, prerequisites, and terms
of offering are unknown as well as the description*.

Treatment applied, and worth recording as the extended form of the pattern:

1. **State plainly that the index confirms the number and title but the detail page could not be retrieved.**
2. **Derive from the nearest live counterpart in the same prefix and chain** — here RET2350
   (Cardiopulmonary Pharmacology, 3 cr / 45 hrs), the lower-division course of the same subject — and
   **say so explicitly.**
3. **Label the credit value and contact hours as an estimate**, not just the outcomes.
4. **Repeat the caution in the closing paragraph as well as the description**, because a reader arriving
   at the hours figure from a table will not have read the opening.

**Generalisable: when a page is missing rather than merely thin, the uncertainty extends to the numeric
fields, and the guide must say so in both places a reader looks.**

### ⚠⚠ Batch 109: two CTS numbers carry suffix *and* title divergence simultaneously

| Queue (statewide inventory) | Daytona State |
|---|---|
| **CTS1851C** — "CIW Web Foundations" | **CTS1851** — "Internet Web Foundations (HTML, CSS)" |
| **CTS2353C** — "Configuring Windows Server" | **CTS2353** — "Networking with Windows Server" |

Both resolved by the standing **404-on-C rule** (drop the C, refetch) and the **batch-98 refinement**
(*Tier 0 settles facts, not necessarily the best label*): both titles are stated in the guide, and the
reader is told **the description, not either title, determines equivalency.**

**⚠ CTS1851C's divergence is informative rather than merely cosmetic.** The statewide title *"CIW Web
Foundations"* names a **certification vendor**; Daytona State's title names the **technologies**. That is
a signal that the course is aligned to a certification examination — so the guide adds an instruction the
generic treatment would have missed: **ask the programme whether it prepares for and offers the
certification examination, because that materially changes the value of the course.**

**Generalisable: where a statewide title carries a vendor or certification name that the local title
drops, treat it as evidence of certification alignment and tell the reader to ask.** Same shape as the
NIMS and AWS credential structures already documented — the course number does not carry the credential,
but the title sometimes points at it.

**⚠ CTS2353C's divergence runs the other way**: Daytona State's local title (*"Networking with Windows
Server"*) is **more accurate than the statewide one** (*"Configuring Windows Server"*), because the
published description is entirely about networking services — DNS, DHCP, IPAM, VPN, NPS, DFS, BranchCache,
SDN. Recorded as the second clear instance of **the local title being the better label**, after the
batch-98 case.

### Batch 109: a seventh credential structure — the *post-primary* certification

The six credential structures already documented (programme-accreditation gates, whole-trade legal
requirements, per-process lapsing qualifications, non-expiring performance credentials, registered
apprenticeship, narrower-than-the-licence activity gates) do not cover what ARRT operates in radiography.

**Post-primary certification** is a distinct shape: **a primary credential establishes the profession,
and separate additional certifications each add a modality to the holder's practisable scope** — CT, MR,
mammography, interventional, bone densitometry. Characteristics worth naming:

- **The primary credential is a prerequisite for the post-primary ones**, so the sequence is fixed.
- **Each post-primary certification is earned separately**, with its own eligibility, documented clinical
  experience, and examination.
- **They are the principal earnings mechanism in the profession** — advancement is by adding modalities
  rather than by promotion, which is unlike most of the fields covered so far.

This was written into all four RTE guides, and it changes the career-pathway advice materially: **the
useful thing to tell a radiography student is not "seek promotion" but "plan which modality to add."**

### ⚠⚠ Batch 109: MRI safety is the strongest single hazard note written into the corpus

Written into RTE4574 (Advanced Imaging Modalities), and the reason it matters is that **it is
counter-intuitive in a way the other hazards are not**:

- **The magnet is always on.** It does not switch off when the scanner is idle, when the power is off, or
  overnight. Every other hazard in the corpus is present only while something is running.
- **Ferromagnetic objects become projectiles** — cylinders, poles, chairs, tools, floor polishers have all
  been pulled into magnets, **and people have been killed and injured by them.**
- **The people harmed are frequently not the patient**, but staff, cleaners, engineers, and porters —
  **precisely the people who were not trained because they were "only going in for a moment."**
- Plus RF heating and burns from cable positioning, acoustic noise, implant screening, and the quench
  procedure.

Paired with the CT counterpart in the same guide: **CT delivers many times the dose of a comparable
radiograph**, paediatric patients are considerably more radiosensitive, and **suggesting ultrasound or MRI
where they answer the same question is a professional contribution, not overstepping.**

**Generalisable framing worth carrying: where a hazard is *permanently present* rather than
*activity-associated*, say so explicitly and early** — the whole reason MRI incidents happen is that
people apply activity-associated intuitions to a permanent field.

### Batch 109: allied-health and systems content worth carrying

- **⚠⚠ Neuromuscular blockade paralyses without sedating** (RET4354) — given to an inadequately sedated
  patient it produces **complete paralysis with full awareness and no ability to breathe or signal**.
  These are high-alert medications with independent double-check requirements *because of documented fatal
  errors*, and **a paralysed patient cannot demonstrate distress**, which is why sedation must be assessed
  by a method that does not rely on movement.
- **⚠⚠ Do not over-ventilate during a code** (RET4245) — the classic error: excessive rate or volume raises
  intrathoracic pressure, impedes venous return, and **actively reduces the blood flow the compressions are
  producing.** Paired with **incomplete chest recoil**, the fault people do not notice themselves doing,
  and **the compressor is always the last to notice fatigue** — hence rotation every two minutes.
- **⚠⚠ Resuscitation failures are communication failures** (RET4245) — reviews rarely find a knowledge gap;
  they find unclear roles and orders nobody acknowledged. **"Someone get the drug" means nobody will.**
- **⚠⚠ Teach-back, not "any questions?"** (RET3041) — and specifically: **a patient using an inhaler
  incorrectly is receiving no treatment while believing they are.** Technique degrades over time, so it is
  checked every time, including on long-term users. Frame it as checking your own explanation.
- **⚠ Home oxygen education is a safety intervention** (RET3041) — oxygen does not burn but makes
  everything else burn readily, **smoking is the cause of home oxygen fires**, and it must be addressed
  directly and without moralising. Plus: **patients turn oxygen up when breathless**, which in some
  conditions is harmful — explain the prescription, not just the number.
- **⚠⚠ Photoelectric absorption makes contrast; Compton scattering destroys it** (RTE2623) — almost every
  technique decision in radiography follows from that one sentence, and it explains why **collimation is
  one of the few genuinely free improvements available**: less tissue irradiated, less scatter, better
  image, lower dose. And **the single most effective patient dose reduction is not repeating the
  examination**, which makes technical competence itself a radiation protection measure.
- **⚠⚠ Data integrity starts at the modality** (RTE3213) — **use the worklist rather than typing patient
  data**; manual entry is the largest source of mismatched studies, and a study attached to the wrong
  patient is **both a safety incident and a privacy breach**. **A wrong-side marker can lead to wrong-side
  treatment.**
- **⚠⚠ Never photograph a screen or a patient with a personal device** (RTE3213) — the commonest serious
  HIPAA breach in imaging departments. Paired with: **systems log every access, and looking up a
  colleague, a neighbour, or a public figure is detected and dismissible.**
- **⚠⚠ Imaging informatics is a real route off the console** (RTE3213) — the CIIP credential, and the
  practical advice to **shadow the department's PACS administrator** as the cheapest way to test the fit.
  A technologist who understands both the clinical work and the systems is rare enough to be valuable.
- **⚠⚠ When something is broken, suspect DNS** (CTS2353C) — a joke because it is true. **Domain-joined
  clients must use internal DNS**; pointing one at a public resolver breaks directory services in ways
  that look like everything except DNS. Test resolution directly rather than inferring it from whether an
  application works.
- **⚠⚠ An untested backup is not a backup** (CTS3348) — jobs report success and produce unrestorable media.
  **Keep at least one copy offline or immutable, because ransomware deliberately encrypts the backups it
  can reach** — a backup on a share the compromised account can write to is not protection.
- **⚠⚠ The shell has no undo** (CTS3348) — and **never solve a permissions problem by making something
  world-writable**: it works, and it is a vulnerability. Paired with **read the logs and the man pages**,
  framed as the actual thing that separates an administrator from someone searching for commands to copy.
- **⚠⚠ Administrative privilege has a blast radius** (CTS2308, CTS2353C, CTS3348) — **use a separate
  administrative account**, because browsing or reading mail as an administrator turns one phishing click
  into a domain compromise. And **check which machine you are on**: running the right command on the wrong
  server is one of the commonest serious incidents in the field. Plus the honest one: **an error reported
  at once is usually recoverable; one concealed for an hour frequently is not.**
- **⚠ Build a lab and break things in it** (CTS2308) — snapshots are what make a virtual lab far more
  useful than physical hardware, and **deliberately breaking and repairing a system without reinstalling
  is exactly the skill employers are buying.**
- **⚠ Accessibility is easiest built in from the start** (CTS1851C) — semantic HTML does most of the work
  for free, **a page built from unlabelled generic containers gives assistive technology nothing**, and
  retrofitting is far more expensive — which is the argument that actually persuades employers.

### Batch 110: DSC **SLS** (5) + **MAR** (4) + **BCV** (4) — three prefixes, all completed

Thirteen guides pushed, all v1.0, all clean, all live. **SLS is complete at 7 pushed / 0 queued**,
**MAR at 8 pushed / 0 queued**, **BCV at 4 pushed / 0 queued.** Seventeen prefixes finished in the
last nine batches.

| Course | cr | hrs | Basis |
|---|---|---|---|
| SLS1127 Faculty Peer Mentoring Experience (Marine/Env Sci) | **0** | — | ⚠⚠ zero credit at a **credit-level** number |
| SLS1130L DSC Basics | **0** | — | ⚠⚠ same |
| SLS2301 Career Development | 3 | 45 | lecture 15/cr (live SLS1122 3/45) |
| SLS2505 Critical Thinking | 3 | 45 | lecture 15/cr; ⚠ **Gordon Rule** course |
| SLS3355L Orientation to Education Programs Lab | **0** | — | ⚠⚠ same |
| MAR2011 Principles of Global Marketing | 3 | 45 | business-family 15/cr |
| MAR2101 Social Media Marketing | 3 | 45 | business-family 15/cr |
| MAR2321 Advertising | 3 | 45 | business-family 15/cr |
| MAR2720 Digital Marketing | 3 | 45 | business-family 15/cr; ⚠ **fall only** |
| BCV0080L Building Construction Assistant I Lab | **0** | **375** | PSAV clock hours; $468.75 fee |
| BCV0084L Building Construction Assistant II Lab | **0** | **75** | PSAV clock hours; $21.25 fee |
| BCV0081L Carpentry and Masonry Technician Lab | **0** | **150** | PSAV clock hours; $21.25 fee |
| BCV0082L Electrical and Plumbing Technician Lab | **0** | **150** | PSAV clock hours; $21.25 fee |

**MAR has no live prefix anchor** — the ratio was taken from the business family instead (**GEB1011** and
**MAN2021**, both live at 3 credits / 45 hours). **Worth naming: where a prefix has no live member, the
nearest anchor is the same institution's same-discipline family, not a same-prefix guess from another
college.** MAR is entirely unsuffixed lecture, so the family transfer is safe here; it would not be for a
prefix mixing lecture and studio conventions.

### ⚠⚠ Batch 110: a genuinely new structure — **zero-credit courses at credit-level numbers**

**Three of the five SLS courses are published at 0 credit hours: SLS1127 (1000 level), SLS1130L (1000),
and SLS3355L (3000).** This is **not** the 0000-level PSAV clock-hour case already documented at length in
this file. **The course numbers are at credit levels and the credit value is still zero.**

The corpus now holds **two distinct routes to `credits: 0`**, and they must not be conflated:

| | **PSAV clock-hour** | **Zero-credit at credit level** |
|---|---|---|
| Number | leading **0** (BCV0080L) | 1000/2000/3000 (SLS1130L) |
| Published figure | **clock hours**, rendered under a "Credit Hours" heading | **nothing** — no hour figure at all |
| What it produces | workforce certificate, job-ready skill | a programme requirement, no credential |
| `contact_hours` | the clock-hour figure (375, 150, 75) | **0** |

**⚠ Implementation note worth recording:** `generate_guide.push_guide` computes
`int(contact_hours) if contact_hours else None`, so **`contact_hours: 0` is pushed as null and the site
displays no hour count** — which is exactly right for these, and it also validates clean (0 is inside
`CONTACT_HOURS_RANGE`), whereas a literal `null` draft raises a validator warning. **For a course whose
contact hours are genuinely unpublished, `0` is the correct draft value, not `null`.** Confirmed live:
SLS1127 and SLS3355L both return `contactHours: null`.

**The advising content this generated is the substantive part**, written into all three as a standard block:

- **It contributes nothing toward a degree** — not the 60 A.A. credits, not an A.S., not general education.
- **⚠⚠ Financial aid enrolment status is computed from credit hours**, so a zero-credit course generally
  does not count toward full-time or half-time status. **Building a schedule around one can quietly drop a
  student below the aid threshold.**
- **It can still carry fees and it still appears on the transcript**, and it is still a distinct SCNS
  number under Rule 22.
- **It is frequently a programme requirement even though it is not a degree requirement** — which is
  precisely why students are caught out by it.
- **Transferability is effectively nil**, since there is no credit to carry and the content is
  institution-specific.

### ⚠⚠ Batch 110: BCV reproduces the clock-hour trap, and the fee scale confirms the reading

All four BCV courses are 0000-level PSAV. **Daytona State renders 375, 150, 150, and 75 under a heading
reading "Credit Hours"** — the trap already documented here, and the largest numbers it has produced.
Handled as standing practice: `credits: 0`, `contact_hours` = the clock-hour figure, and an explicit note
in the guide that the catalog heading is a rendering artefact.

**⚠ New corroborating signal: the fee scales with the hours on exactly one course.** BCV0080L's fee is
**$468.75**, which is **375 × $1.25 exactly**; the other three carry a flat **$21.25**. That is a
per-clock-hour charge, and **a fee that is an exact multiple of the published figure is independent
evidence that the figure is hours rather than credits.** Worth checking whenever a 0000-level number looks
ambiguous — no credit-hour reading of "375" would produce that fee.

### ⚠⚠ Batch 110: Roman numerals contradict the enrolment structure again — and the hours prove it

**BCV0080L ("Assistant I") and BCV0084L ("Assistant II") list each other as corequisites and are both
offered in spring.** They are **co-enrolled in the same term, not sequential.** And the sizes invert the
implication entirely: **"I" is 375 clock hours; "II" is 75.**

This is the **second instance** of the pattern first recorded for **PMT welding** at batch 101 —
*Roman numerals in titles can actively contradict the enrolment sequence.* **What is new here is that the
published hour figures made the contradiction visible.** A title-only reading gives a five-course
progression; the numbers and the corequisites give a large course with a small companion.

**Generalisable, and now confirmed twice: treat a Roman numeral as a label, not as evidence of sequence.
The corequisite field and the hour figures are the evidence.** Both guides state the pairing explicitly
and tell the reader to confirm the enrolment pattern with the programme.

### ⚠ Batch 110: the BCV programme spans a full year, and the terms do not overlap

**Assistant courses (BCV0080L, BCV0084L) are spring-only; Technician courses (BCV0081L, BCV0082L) are
fall-only**, and BCV0081L requires BCV0084L. **The sequence therefore runs spring → fall, spanning a year,
and missing a term costs a year rather than a term.**

Same advising shape as **ETC4206's every-two-years offering** at batch 107, and reinforcing that finding:
**a stated offering pattern that constrains completion by more than one term is advising-critical and
belongs high in the guide.** Flagged prominently in BCV0081L and BCV0084L.

### ⚠⚠ Batch 110: MAR is the fastest-moving regulatory content in the corpus

Written as a shared block into all four MAR guides, and it is the most Rule-11-sensitive material written
anywhere in this repository so far:

- **FTC substantiation: evidence must exist *before* the claim runs.** Assembling it afterwards is not a
  defence, and **"the client said it was true" does not protect whoever wrote the advertisement.**
- **⚠⚠ Material-connection disclosure must be clear and conspicuous where the endorsement is** — not in a
  bio, not behind a "more" link, not the last of thirty hashtags, and **not only in a caption when the
  claim is made in the video.** Plain words work; **"sp", "collab", "thanks to", and "ambassador" do not.**
- **⚠⚠ Fake, incentivised, and suppressed reviews carry federal exposure** under the FTC's review rules.
- **Florida adds its own layer independently of federal law**: **FDUTPA (Chapter 501, Part II, F.S.)**
  with a private right of action, plus **Florida's Digital Bill of Rights** for consumer data.
- **CAN-SPAM for email; ⚠ the TCPA for text messaging**, where per-message statutory damages have produced
  very large settlements — **text is far more tightly regulated than email**, which students assume the
  reverse of.
- **⚠ Advertising for regulated professions is separately restricted in Florida** under each licensing
  chapter — legal, medical, dental, contracting. **Check the board's rules before writing for a licensee.**
- **⚠⚠ FCPA exposure attaches to marketing activity specifically** (MAR2011) — entertainment, gifts,
  travel, sponsorships, and payments to local agents are the routes by which a well-meaning marketer
  creates liability. **"It is normal practice there" is not a defence**, and third-party agents transfer
  exposure to the company that engaged them.

**Generalisable: where a field's regulation is both active and individually enforceable against the
practitioner rather than only the employer, the regulatory block belongs in every guide in the prefix,
not just the one whose title names it.**

### Batch 110: content worth carrying

- **⚠⚠ Attribution is a model, not a measurement** (MAR2720) — **last-click systematically over-credits
  branded search and under-credits whatever created the demand**, so **budget decisions made on last-click
  routinely defund the channels that were working.** Paired with: **do not stop an A/B test when it looks
  good** — early stopping on a favourable reading is the commonest source of false results, and **summing
  conversions across ad platforms double-counts**, because each claims by its own rules.
- **⚠⚠ Bought followers are worse than none** (MAR2101) — they depress engagement rate, corrupt targeting,
  and are visible to anyone who looks. And the professionalism point: **saying what a number cannot tell
  you is a strength; overclaiming precision is how marketers lose internal credibility.**
- **⚠ Puffery is lawful; a factual claim you cannot substantiate is not** (MAR2321) — the line is whether a
  reasonable consumer takes it as factual. And: **the overall impression governs, not the literal words**,
  so **fine print does not cure a misleading headline.** Plus the review discipline: **judge creative
  against the brief, not against whether you like it** — "I don't like the blue" is not feedback, and it
  is why a great deal of work is made worse in review.
- **⚠⚠ Motivated reasoning is not something other people do** (SLS2505) — **reasoning ability does not
  protect against bias and frequently makes it worse**, because a capable reasoner builds better
  justifications for what they already believed. The practical test offered: **do you check a claim you
  dislike more carefully than one you like?** And **generative AI output is not a source** — fluent,
  frequently correct, confidently wrong in hard-to-detect ways.
- **⚠⚠ Withdrawal is not free** (SLS1130L) — it counts as attempted credit, **attempted-versus-completed
  ratios drive satisfactory academic progress, which drives aid eligibility**, and Florida charges
  substantially more for a third attempt. Deadlines are the part that costs money.
- **⚠⚠ You can complete the coursework and still not be certifiable** (SLS3355L) — Florida teacher
  certification is administered by FLDOE, not the college. **Background screening blocks field placement
  and therefore programme completion**, and it is discovered far too late if not raised at the start.
  **Leaving all the FTCE examinations to the end is the commonest cause of delayed certification.**
- **⚠ Check what the credential actually costs and returns** (SLS2301) — **look at entry-level pay, not the
  median**, count the income not earned while studying, and **check accreditation where eligibility depends
  on it.** This repository now records that unrecoverable trap for **CAPTE, CAAHEP, ACOTE, CoARC, JRCERT,
  and CIDA** — the SLS2301 guide names all six, which makes the career course the natural place to
  aggregate them.
- **⚠⚠ Verify de-energisation with a tester you have just proved works** (BCV0082L) — test the tester on a
  known live source, test the circuit, test the tester again. **A dead tester reads the same as a dead
  circuit**, and that mistake has killed experienced electricians.
- **⚠⚠ EPA 608 is a legal gate on the activity, not an employer preference** (BCV0082L) — unlawful to
  handle refrigerant without it regardless of skill or supervision. **It does not expire**, it is cheap,
  and in Florida air conditioning work is close to recession-proof — so **get it early**. Also flagged: the
  transition to lower-GWP refrigerants, some **mildly flammable** with different handling requirements.
- **⚠⚠ A strap installed with the wrong nails is rated at nothing** (BCV0081L) — the continuous load path
  finding from ETC at batch 107, now stated at the installer's level rather than the designer's.
  **Connector substitution is not a field decision.**
- **⚠⚠ Silica damage is silent and permanent** (BCV0081L) — no immediate symptom, cumulative, presents
  years later, **which is exactly why the controls get skipped.** And **a hardware-store dust mask is not
  respiratory protection against silica.**
- **⚠⚠ Heat illness is the Florida-specific construction killer** (all four BCV) — and **the
  highest-risk worker is the new one in their first week**, before acclimatisation.
- **⚠ Unlicensed contracting carries increased penalties during a declared state of emergency**
  (all four BCV) — **which in Florida means after every hurricane**, exactly when unlicensed work is most
  tempting and most harmful. Paired with the distinction graduates most need: **working as an employee of
  a licensed contractor is lawful; holding yourself out as a contractor is not.**
- **⚠ Keep a record of the work you have done and who you did it for** (BCV0084L) — **licensure later
  requires documented experience, and reconstructing it years afterwards is genuinely difficult.** A small
  point with a large payoff, and one no catalog will tell a student.

### Batch 111: DSC **AMH** (3) + **TPP** (3) + **MUM** (3) + **DAN** (2) + **DAA** (1) — five prefixes, all completed

Twelve guides pushed, all v1.0, all clean, all live. **AMH complete at 8 pushed / 0 queued**, **TPP at
10 / 0**, **MUM at 7 / 0**, **DAN at 3 / 0**, **DAA at 12 / 0.** Twenty-two prefixes finished in the last
ten batches.

| Course | cr | hrs | Basis |
|---|---|---|---|
| AMH2057 The American Civil War | 3 | 45 | lecture 15/cr (live AMH2010, AMH2020) |
| AMH2058 World War II | 3 | 45 | same |
| AMH2059 The Vietnam War | 3 | 45 | same |
| TPP1200C Healthcare Theater | 3 | 60 | studio 20/cr (live TPP1110 3/60) |
| TPP2118 Acting 3 | 3 | 60 | same; ⚠⚠ **prerequisite names a course DSC does not offer** |
| TPP2119 Acting 4 | 3 | 60 | same; ⚠⚠ same; repeatable once |
| MUM1610 Survey of Recording Technology | 3 | 60 | studio 20/cr (live MUM1622 3/60) |
| MUM1634 The Digital Audio Workstation | 3 | 60 | same |
| MUM2716 Automated Show Control | 3 | 60 | same; $60 fee |
| DAN1100 Dance Appreciation | 3 | 45 | ⚠ catalog says **lecture-based** → 15/cr |
| DAN2740 Stretch and Conditioning | 3 | 60 | ⚠ **derived**; studio 20/cr |
| DAA2640 Rehearsal & Performance | 1 | 30 | ⚠ **derived**; 1-credit lab convention |

### ⚠⚠ Batch 111: a published prerequisite naming a course the institution does not offer

**Daytona State publishes the prerequisite for TPP2118 (Acting 3) as THE1036 and for TPP2119 (Acting 4)
as THE2037.** A grep of `daytona_courses.csv` shows **DSC's entire THE inventory is a single course,
THE1000 (Theatre Appreciation)** — there is no THE1036 and no THE2037. What DSC *does* publish is a
complete acting sequence under TPP: **TPP1110 (Acting 1), TPP1111 (Acting 2)**, then these two.

**The near-certain reading is that the prerequisite text carries numbering from another institution or an
earlier catalog**, and the intended prerequisites are the preceding TPP courses. **SOURCES.md line ~635
already documents exactly the condition that produces this**: Florida carries introductory acting under
**two SCNS numbers** (TPP1110 "Acting 1" and TPP2100 "Acting I"), and that finding previously forced a
v1.1 correction to TPP2300C.

**Treatment — and this is the point worth generalising.** The guides do **not** silently substitute the
plausible prerequisite. They state what the catalog publishes, state that DSC's own inventory contains no
such course while it does contain Acting 1 and Acting 2 under TPP, note the Rule 22 consequence (a
prerequisite satisfied by one number is not automatically satisfied by another, which matters most to a
transfer student), and **tell the reader to confirm with the department before registering.**

**Generalisable: when a catalog's prerequisite field names a number absent from the same catalog's own
inventory, report the discrepancy rather than resolving it.** Tier 0 settles facts; it does not authorise
the guide to correct Tier 0. This is the **third distinct class of catalog self-contradiction** now
recorded, after copy-pasted descriptions (six instances) and contradictory prereq/coreq loops
(ACR0550C/0551C).

**⚠ Method note:** this was found by a **one-command local grep of `daytona_courses.csv`**, not a fetch.
The inventory file is a cheap cross-check on any prerequisite that looks unfamiliar, and it should be run
routinely rather than only when something looks wrong.

### ⚠⚠ Batch 111: a *three-course* mutual corequisite block — and the programme's only annual entry point

**MUM1610, MUM1634, and MUM1622 each list the other two as corequisites, and all three are offered fall
only.** The corpus has recorded two-way mutual corequisite pairs before (RTV2534 ↔ RTV2540, BCV0080L ↔
BCV0084L at batch 110); **this is the first three-way block.**

**The consequence is an advising fact, not a curiosity: the entry point to the programme runs once a
year.** A student who misses the fall intake waits a full year, because no member of the block can be
taken alone. Flagged prominently in both guides, with an instruction to confirm the current pattern.

This is now the **third batch running** to turn up an offering pattern that constrains completion by more
than one term — **ETC4206's two-year cycle (107), BCV's spring→fall year-long sequence (110), and this.**
The pattern is common enough that it deserves a standing check: **whenever a course is offered in a single
term, ask what else is locked to that term with it.**

### ⚠ Batch 111: two Tier-2 catalogs returned empty bodies for DAN and DAA

**Broward (`catalog.broward.edu/course-descriptions/{daa,dan}/`) and Valencia
(`catalog.valenciacollege.edu/coursedescriptions/coursesoffered/{daa,dan}/`) both returned empty bodies.**
Most likely neither institution teaches those prefixes; a 404 or an absent prefix returns nothing rather
than an error. **Recorded so the next dance batch does not spend the same two fetches.**

Resolved by deriving from the live corpus, which has been the sole ratio source since batch 93:

- **DAN1100 → 3/45.** The catalog explicitly calls it **lecture-based**, and it carries Gordon Rule
  writing credit — the same character as live AMH2010/AMH2020 at 3/45. **The description settled this, per
  the batch-97 hierarchy (suffix → description → fee).** High confidence; not labelled derived.
- **DAN2740 → 3/60** and **DAA2640 → 1/30**, both **labelled derived in the guide**, with the anchors
  named (TPP1110 and MUM1622 for the studio ratio; CET1114L/PHT2211L/ETC4241L for the one-credit lab
  convention) and the reader directed to confirm.

**⚠ DAA2640 carries an extra caution the arithmetic does not capture**, and it is the more useful half:
**a one-credit ensemble course does not cost one credit of time.** Rehearsal calls, technical rehearsals,
and performance dates are fixed by the production, and **the load is heavily back-loaded into performance
week**, arriving alongside every other course's deadlines. The guide tells students to get the calendar at
the start and plan other coursework around it. **Generalisable to any rehearsal, ensemble, practicum, or
production course: where credit value understates time cost, say so explicitly.**

### Batch 111: content worth carrying

- **⚠⚠ Consistency, not performance, is the skill in standardized patient work** (TPP1200C) — the encounter
  is frequently **a graded examination for the student across the table**, so **giving one student a fuller
  answer or a warmer manner than another makes the assessment unfair and the data useless.** Answer what
  is asked, not what you wish had been asked — volunteering information the student failed to elicit
  removes exactly what was being measured. Plus **confidentiality applies to learner performance**, and
  **de-roling is occupational hygiene, not fussiness.** ⚠ And a career note students miss entirely: **SP
  work is paid, local, continuously in demand wherever health professions are taught, and rarely
  advertised — ask the simulation centre directly.**
- **⚠⚠ Stage violence is choreography, and improvising it is how people get hurt** (TPP2119) — **adding
  something because it felt right removes your partner's ability to protect themselves; they are defending
  against choreography, not against you.** Eye contact is the primary safety mechanism. **The receiver
  controls distance and reaction; the deliverer controls the target.** Rehearse every time, at reduced
  speed, on the actual set, in the actual shoes. SAFD certification named as the credential.
- **⚠ Repeatable-for-credit is not the same as repeating a course** (TPP2119) — a distinct provision from
  Florida's attempt limit and third-attempt surcharge, and worth confirming with an advisor for aid and
  transfer purposes. First time the corpus has had to draw that line.
- **⚠⚠ Your hearing is the instrument, and the damage is permanent, cumulative, and painless** (all three
  MUM) — **loud monitoring is not more accurate, it is more flattering**, and it produces mixes that fall
  apart quietly. **Custom musician's earplugs attenuate evenly** and cost about what a cable set costs.
  **Get a baseline hearing test now**, while young, because it is the only way to detect the change early.
- **⚠⚠ Credit is not a licence** (all three MUM) — the single most common student misunderstanding.
  A recording carries **two separate copyrights** (composition and sound recording), sampling needs both,
  and **"no copyright infringement intended" changes nothing.** Paired with the practical one: **agree
  splits in writing before the session, not after the song works** — almost every serious collaborator
  dispute is about ownership everyone assumed was obvious.
- **⚠⚠ Automated systems move heavy things over people** (MUM2716) — **never test automation with people
  in the movement path**, know how to take manual control of every subsystem, and **know the failure state
  of every device**: what a motor or lift does on loss of signal or power is a design decision you must
  know. Rigging is ETCP-certified work. **"Stop the show" is always defensible.** Plus the networking half:
  **keep the show network separate from everything else**, and **change nothing on show day** — the classic
  incident is a small improvement made an hour before doors.
- **⚠⚠ Stretching is not warming up** (DAN2740) — prolonged static stretching before activity can
  temporarily **reduce force production**, the opposite of what a performer wants. Dynamic warm-up before,
  static after. **Never bounce, never stretch to pain**, and **hypermobility without strength is a
  documented injury risk** — which is exactly the position dancers selected for flexibility are in.
- **⚠⚠ Working through pain is not discipline** (all performing arts guides) — **the overuse injuries that
  end performing careers are almost always ones that were felt, ignored, and worked through.** Paired with
  a consent-and-boundaries block (contact choreographed and agreed in advance; **you may decline**;
  de-role deliberately) reflecting the profession's changed standards, and an **honest careers block**:
  performance work is intermittent and most people also do other things — **that is the normal shape of
  the career, not a sign of failure** — with Florida's theme park and cruise sector named as the real,
  steady employer that students overlook.
- **⚠⚠ History is an argument from evidence, not a list of what happened** (all three AMH) — ask **who
  produced a source and why** before asking what it says; **absence from the archive is not absence from
  history**; and **generative AI produces plausible citations to works that do not exist.** For AMH2057
  specifically: **the gap between what happened and how it has been remembered is itself the subject**,
  and **the contemporaneous secession documents settle a great deal that later commentary muddied.**
- **⚠ Florida's WWII record is deep, digitised, and under-researched at this level** (AMH2058) — the state
  was among the most heavily militarised in the country, **German submarines sank shipping within sight of
  the Florida coast in 1942**, and Florida Memory plus local newspapers make an original undergraduate
  research paper genuinely achievable. **Where local archives make original work possible at this level,
  say so** — it is better work than another paper off the same secondary accounts.
- **⚠⚠ Recent history has living participants in the room** (AMH2059) — veterans and refugees **are not
  exhibits**, memory and history are different and both are evidence, and **a course on this war conducted
  entirely from American sources is studying American politics, not the war.**

### Batch 112: DSC engineering technology — **EIN** (1) + **ETD** (1) + **ETG** (2) + **ETM** (3) + **ETP** (3) + **ETS** (2)

Twelve guides pushed, all v1.0, all clean, all live — **eleven queue rows plus one bonus course**
(ETP4240, drafted as the split-pair partner and picked up by `reconcile` as an orphan draft, which added
it to the queue). **EIN, ETD, ETG, ETM, ETP and ETS are all complete at 0 queued.** Twenty-eight prefixes
finished in the last eleven batches.

| Course | cr | hrs | Basis |
|---|---|---|---|
| EIN3314 Work Design and Measurement | 3 | 45 | lecture 15/cr; ⚠ spring only |
| ETD2465C Tool Design and Lab | 3 | 60 | C form 20/cr; $60 fee; ⚠ spring only |
| ETG3541 Applied Mechanics and Physics | 3 | 45 | lecture 15/cr; ⚠ **summer only** |
| ETG3533L Engineering Strength of Materials Lab | 1 | 30 | ⚠ **derived**; coreq ETG3533 |
| ETM4220 Energy Systems | 3 | 45 | lecture 15/cr; ⚠ spring only |
| ETM4331 Applied Fluid Mechanics | 3 | 45 | lecture 15/cr; ⚠ **prereq timing trap** |
| ETM4512 Design of Machine Elements | 3 | 45 | lecture 15/cr; ⚠ spring only |
| ETP4240 Power Systems | 3 | 45 | lecture 15/cr; coreq ETP4240L |
| ETP4240L Power Systems Lab | 1 | 30 | ⚠ **derived**; $21 fee |
| ETP4240C Power Systems and Lab | 4 | 75 | ⚠⚠ **not a DSC number**; derived from the split pair |
| ETS2540C Fundamentals of Robotics and Automation | 3 | 60 | C form 20/cr; ⚠ spring only |
| ETS4502C Metrology and Instrumentation and Lab | 3 | 60 | C form 20/cr |

**Ratios pinned across six prefixes from two live anchors each**: **unsuffixed engineering technology
lecture = 15 hrs/cr** (ETG2520 and EGN3311, both 3/45) and **C-suffixed = 20** (ETD2320C 4/80; ETD2364C,
ETS2542C, ETS3543C all 3/60). **ETM and ETP have no live members at all**, and were priced from the
ETG/EGN lecture convention — same institution, same discipline, same unsuffixed lecture character.
**Second confirmation of the batch-110 principle: where a prefix has no live anchor, the nearest evidence
is the same institution's same-discipline family, not a same-prefix figure from another college.**

### ⚠⚠ Batch 112: writing a guide for a course the canonical institution does not offer

**The queue carries ETP4240C. Daytona State does not publish that number** — it publishes the **split
pair ETP4240 (3 cr) + ETP4240L (1 cr)**, corequisites in fall. This is the **mirror image of the batch-107
EET situation**, where DSC published *both* structures simultaneously; here the statewide inventory has
the combined form and DSC has only the split.

Treatment, and it is worth recording as the standing method for this case:

1. **Say plainly, in the description, that the canonical institution does not publish the number**, and
   say what it publishes instead.
2. **Derive the combined values by summing the published split** — 3+1 credits, 45+30 hours — and
   **label both figures derived**.
3. **Give the competing derivation too.** The prefix family's C-form convention of 20 hrs/cr would give
   **80** rather than 75. Stating both is more useful than picking one silently, because a reader
   reconciling against another catalog needs to know which basis produced the number.
4. **Flag Rule 22 explicitly**: ETP4240C is not ETP4240, and it is not ETP4240 + ETP4240L. Equivalency
   does not cross the suffix in either direction.
5. **Tell the reader to confirm with the institution that actually offers it.**

**⚠ Method note worth keeping:** drafting ETP4240 alongside it was not planned — it was written because
the split pair had to be described accurately. **`queue_mgr.py reconcile` detected it as an orphan draft
and added it to the queue**, which is how the batch produced twelve guides from eleven rows. **When a
queued C-form resolves to a split pair, drafting both halves is nearly free and the tooling absorbs the
extra row automatically.**

### ⚠⚠ Batch 112: a prerequisite timing trap that only appears when you read the block together

**ETM4331 (Applied Fluid Mechanics) is offered fall.** One of its alternative prerequisites, **ETG3541
(Applied Mechanics and Physics), is offered summer only.** A student relying on that route has **exactly
one opportunity per year** to satisfy it in time, and missing the summer offering pushes ETM4331 back a
full year. (The alternative prerequisite, PHY2048C, is more frequently offered — which is the escape
hatch, and the guide says so.)

**This is invisible from either course's own page.** ETG3541's entry does not know what depends on it;
ETM4331's entry does not say when its prerequisite runs. **Only fetching the block surfaces it** — which
is the fourth distinct instance of *prefix-block fetching surfaces what single-course work cannot*.

**Nine of the twelve courses in this batch are single-term offerings.** That is a strong enough
concentration to name as a property of upper-division engineering technology: **low-enrolment
upper-division courses run once a year, so the prerequisite chains have almost no slack.** Every guide in
this batch flags its own term, and the two with chain consequences flag the chain.

### Batch 112: the ⚠⚠ safety content, which is the substance of these guides

Engineering technology is the most hazard-dense discipline group in the corpus, and a shared
**stored-energy** framing was written across the batch — *loaded specimens, pressurised systems, charged
capacitors, energised circuits, springs, and rotating masses all hold energy that can be released
suddenly, and almost every serious laboratory injury is a stored-energy release.*

- **⚠⚠ Arc flash is the hazard electrical students most underestimate** (ETP4240, ETP4240L, ETP4240C) —
  it **injures and kills more people in industrial electrical incidents than shock does**, reaches
  temperatures several times hotter than the sun's surface, and is over in thousandths of a second.
  **Ordinary clothing ignites; synthetics melt onto skin.** NFPA 70E named. And the connection that makes
  this course's analysis a safety subject: **the available fault current and the protective device
  clearing time determine the incident energy — a slower breaker means a bigger arc flash.**
- **⚠⚠ Never be inside the work envelope of an energised robot** (ETS2540C) — and the non-obvious half:
  **the recorded fatalities overwhelmingly involve maintenance, teaching, jam-clearing and
  troubleshooting, not normal automatic operation.** The hazard concentrates exactly where people assume
  the risk is lower. **A robot at rest may simply be waiting for a signal.** Plus: **a collaborative robot
  is not automatically safe** — safety is a property of the application, and a cobot holding a knife, a
  hot part, or a heavy load is not a collaborative application.
- **⚠⚠ Fatigue is why machines break, and static strength does not predict it** (ETM4512) — most
  components that fail in service fail **below yield strength**, at stress concentrations, after millions
  of cycles. **Generous radii are free strength.** **Steel has an endurance limit; aluminium does not**,
  which changes design philosophy entirely. And **fatigue gives little warning** — the crack grows
  invisibly and then the remaining section goes.
- **⚠⚠ Pneumatic pressure is far more dangerous than hydraulic at the same pressure** (ETM4331) because
  gas is compressible and stores far more energy. Plus **high-pressure injection injuries are surgical
  emergencies that look trivial** — never check for a leak with your hand. And **water hammer**: closing a
  valve rapidly generates surges far above operating pressure.
- **⚠⚠ A loaded specimen releases its energy at fracture** (ETG3533L) — stay behind the guard;
  **buckling columns release sideways and unpredictably**, torsion specimens whip.
- **⚠⚠ Musculoskeletal injury is cumulative and the job design causes it** (EIN3314) — **fit the job to
  the person, not the person to the job**; training someone to lift correctly does not fix a task
  requiring a bad lift. **Design for the range of people who will do the work, not for an average that
  describes nobody.**

### Batch 112: professional-judgement content worth carrying

- **⚠⚠ An engineering answer is a number, a unit, and a judgement about whether it is plausible** (shared
  across all twelve) — **carry units through the calculation** rather than appending them, estimate before
  calculating, and **software output is not verification**: analysis packages return confident,
  well-formatted answers to badly posed problems.
- **⚠⚠ Engineering technology and engineering are different pathways, and it matters for PE licensure**
  (shared) — **ABET accredits them under separate commissions with different criteria**, and an
  engineering technology degree may not qualify a graduate for licensure on the same terms, or in some
  states at all. **Establish the route before enrolling, in writing.** This is the *same unrecoverable
  trap* already recorded for CAPTE, CAAHEP, ACOTE, CoARC, JRCERT and CIDA — **the seventh field, and the
  first outside health and design.** Balanced with the honest counterweight: **the industry exemption is
  why many engineering technology graduates have full technical careers without a licence.**
- **⚠⚠ Time study is measurement of people** (EIN3314) — the discipline has **a genuinely bad history and
  workers know it**. Never study someone without their knowledge; **performance rating is a judgement and
  is the weakest link in the method** — be honest about that rather than presenting a standard time as a
  measurement. And: **a standard used punitively stops being useful**, because the data becomes theatre
  and the organisation loses the ability to measure anything.
- **⚠⚠ Be straight about automation's workforce effects** (ETS2540C) — it removes some tasks, creates
  others needing different skills, and **the transition falls unevenly on real people**; pretending
  otherwise damages the credibility of everyone involved. Paired with the practical point that **operators
  know the failure modes and the workarounds**, and their cooperation determines whether an installation
  succeeds.
- **⚠⚠ A measurement without an uncertainty is not a measurement** (ETS4502C) — the organising idea of
  metrology. **Consistency is not accuracy**; an instrument that has drifted reads confidently and
  wrongly. **When an instrument is found out of calibration, everything measured with it since the last
  good calibration is in question** — which is why calibration findings trigger recalls. **Temperature
  dominates precision dimensional measurement** (standards defined at 20 °C; parts warm from machining
  read differently). And the counter-intuitive one: **reacting to common-cause variation as if it were
  special makes the process worse** — do not tamper.
- **⚠⚠ Geometric tolerancing is not decorated plus-or-minus** (ETD2465C) — **the datum reference frame is
  the foundation**, and choosing datums badly produces a drawing that is precise, inspectable, and
  describes the wrong thing. **A position tolerance is a circular zone, larger than the square one implied
  by equivalent ± dimensions**, so GD&T frequently allows *more* manufacturing freedom while controlling
  function better. Plus the workholding rule: **locate first, then clamp** — a clamp that moves the part
  has destroyed the location it was meant to preserve.
- **⚠⚠ Bernoulli is the most misapplied equation in engineering** (ETM4331) — applying it across a pump, a
  valve, a bend, or a long run gives an answer that is **confidently wrong**. **Head loss goes with
  velocity squared**, so oversizing a pump "to be safe" can produce a system that delivers less than a
  smaller one would.
- **⚠⚠ The second law rules things out, and knowing that saves you from nonsense** (ETM4220) — **Carnot
  efficiency is an absolute ceiling set by temperatures alone**, waste heat is a requirement rather than a
  design failure, and **any over-unity claim is wrong without needing to find the error.** Engineers are
  approached with these regularly; being able to say why, briefly and without arrogance, is a real
  professional skill. Plus: **an efficiency claim without a stated boundary is not a figure** — which is
  how misleading energy marketing is constructed.
- **⚠ The per-unit system is a built-in sanity check, not bookkeeping** (ETP) — **it makes transformers
  disappear**, which is the entire reason a network spanning several voltage levels can be analysed as one
  circuit; and because similar equipment falls in similar per-unit ranges regardless of size, **a per-unit
  value that looks wrong usually is wrong.** The commonest fault-calculation error named: **manufacturer
  impedance is given on the equipment's own base and must be converted.**
- **⚠ The free-body diagram is the course; everything else is arithmetic** (ETG3541) — almost every wrong
  answer in mechanics is a wrong free-body diagram, and **students who skip it here pay for it in every
  course after.**
- **⚠ When the measurement disagrees with the calculation, that is the interesting part** (ETG3533L) —
  and **never adjust data toward the expected answer.** Stated as both a coursework standard and a
  professional one.
- **⚠⚠ Florida's grid is a hurricane grid** (ETP) — hardening and restoration are continuing engineering
  programmes, **undergrounding is a genuine trade-off rather than an improvement** (removes wind exposure,
  adds flooding and salt, far slower to repair), and **backfeed from generators and rooftop solar can
  energise a line crews believe is dead — this has killed line workers.** Paired with the Florida energy
  points in ETM4220: **demand is dominated by air conditioning**, the state has **no significant
  hydro and limited wind**, and **an oversized air conditioner cools without dehumidifying and produces a
  cold, damp, mouldy building** — a common and expensive Florida design error.

### Batch 113: DSC health block — **NUR** (3) + **HSC** (3) + **HSA** (2) + **DEA** (2) + **PRN** (2) + **HIM** (1)

Thirteen guides pushed, all v1.0, all clean, all live. **NUR, HSC, HSA, DEA, PRN and HIM are all complete
at 0 queued.** Thirty-four prefixes finished in the last twelve batches.

| Course | cr | hrs | Basis |
|---|---|---|---|
| NUR1230C Nursing Process III and Lab | 7 | **224** | NUR C form **32 hrs/cr**; $364.49 fee |
| NUR1423C Nursing Process II and Lab | 4 | **128** | same; coreq of NUR1230C |
| NUR1322 Maternal Child Nursing (transition track) | 3 | 45 | ⚠ **unsuffixed**, no clinical → lecture 15/cr |
| HSC3730 Research Methods for Health Professions | 3 | 45 | lecture 15/cr; ⚠ **URL level-segment anomaly** |
| HSC4550 Pathophysiology for Health Care | 3 | 45 | lecture 15/cr; ⚠ no prereq published |
| HSC4645 Legal and Ethical Aspects of Health Care | 3 | 45 | lecture 15/cr |
| HSA4107 Health Services Administration | 3 | 45 | lecture 15/cr |
| HSA4353 Organizational Behavior | 3 | 45 | lecture 15/cr |
| HIM1273L Billing and Reimbursement Methods Lab | 1 | 30 | ⚠ derived, **cross-checked**; ⚠⚠ obsolete form named |
| DEA0000 Introduction to Dental Assisting | 0 | **30** | PSAV clock hours |
| DEA0851L Externship II | 0 | **240** | PSAV clock hours; $37.50 fee |
| PRN0042C Neuromuscular Sensory Nursing and Lab | 0 | **174** | PSAV clock hours; $186 fee |
| PRN0207C Medical-Surgical Nursing I and Lab | 0 | **455** | PSAV clock hours; $252 fee |

### ⚠⚠ Batch 113: the NUR ratio is 32 hrs/cr — the highest credit-bearing convention in the corpus

**Two live anchors agree exactly across very different course sizes**: **NUR1020C at 5 credits / 160
hours** and **NUR1005C at 8 credits / 256 hours** — both **32 contact hours per credit**. That is more
than double the lecture convention and above every C-form ratio recorded so far (20), because
**a nursing C course bundles classroom, skills laboratory and clinical placement into one enrolment.**

**NUR1230C at 7 credits / 224 hours is now the largest credit-bearing course in this repository.**
(PRN0207C at 455 clock hours is larger in hours but carries zero credit.)

**⚠ The prefix splits on the suffix, and the description confirms it.** **NUR1322 is unsuffixed**, and its
catalog description says the work is *"online discussions and assignments"* rather than clinical
placement — so it was priced at the **lecture convention of 15**, not at 32. **Suffix and description
agreeing is the strong case under the batch-97 hierarchy**; had they disagreed, the description would
have governed.

**Generalisable and worth stating plainly: a credit number in a clinical prefix does not mean what it
means elsewhere.** Seven nursing credits consume more of a week than four ordinary courses. Every NUR and
PRN guide in this batch carries an explicit "this is not N credits of time" block telling students to
plan employment, childcare and finances a term ahead — because **the students who plan around the credit
number rather than the contact hours are the ones who fail out.**

### ⚠⚠ Batch 113: the level segment in a SmartCatalog URL reflects catalog grouping, not the course number

**HSC3730 returned 404 at `/3000/hsc3730/` and 404 again with the level segment dropped.** The prefix
index resolved it: **the working href is `/4000/hsc3730/`** — a **3000-level course filed under the 4000
segment**. The index also exposed an entry pointing at `/3000/hsc4644`, the same mismatch in reverse.

SOURCES.md already records *"the `<level>` segment is not universal — drop it if the URL 404s"* and *"fetch
the prefix index, which exposes the real href."* **This extends that finding materially:** the level
segment is not merely *sometimes absent* — **it can be present and simply not match the course number**,
because it reflects how the catalog groups pages rather than what the number is.

**Revised rule: on a 404, try dropping the level segment; if that also 404s, fetch the prefix index and
read the real href rather than concluding the course is absent.** Two failed direct fetches are not
evidence of absence — the index is the authority on the path.

### ⚠⚠ Batch 113: the catalog names a claim form retired in 2007

**HIM1273L's published description tells students they will complete "UB-92 and CMS-1500 claims."**
**The UB-92 was replaced by the UB-04 (CMS-1450) in 2007** and has not been an accepted institutional
claim form since. The CMS-1500 named alongside it remains current.

Handled without over-claiming: the guide states what the catalog says, states plainly that the form was
retired, **assumes the course as taught uses current forms** — no billing programme could place graduates
otherwise — and tells the reader to confirm with the department. It then turns the finding into the point:
**this is exactly the currency drift that matters in a field where forms, code sets and payer rules change
every year**, which is why the guide's resources section insists on **current-year code books** and the
official annually-updated guidelines.

**New class of catalog defect for the corpus.** The existing classes are copy-pasted descriptions (six
instances), contradictory prereq/coreq loops, and prerequisites naming non-existent courses (batch 111).
**This is the fourth: content that was accurate when written and has since gone stale.** It is the hardest
class to detect, because nothing internal to the catalog is inconsistent — **it requires knowing the
domain.** Worth watching for wherever a course names a specific form, standard, code set, or product
version.

### ✅ Batch 113: a derived lab figure corroborated from inside the prefix — second instance

**HIM1273L publishes no contact hours.** The institution-wide one-credit laboratory convention gives 30.
That figure can be *checked* here: **the combined form HIM1273C is live at 3 credits / 60 hours**, and a
split of **2 credits lecture at 15 (30 hours) + 1 credit lab at 30** reproduces exactly 3 credits and 60
hours. **The combined course's published total validates the derived laboratory figure.**

This is the **second instance** of the technique first recorded at batch 107 for the EET laboratories
(where ETG3085C's published 3/60 validated a 2-credit lecture plus 1-credit lab split). **Now confirmed
across two unrelated prefixes, it is a reliable method rather than a one-off:** *where a prefix publishes
both a combined C form and a split lecture-plus-L pair for the same subject, the C form's published total
checks the derived laboratory figure.*

### Batch 113: clinical and regulatory content worth carrying

- **⚠⚠ Postpartum haemorrhage and preeclampsia are the two that kill, and both are catchable** (NUR1423C)
  — the US maternal mortality rate is substantially worse than comparable countries' and **a large share
  of those deaths are judged preventable**. **Outcomes are markedly worse for Black women, and the
  disparity persists after adjusting for income and education**; a documented contributor is that women's
  reports of symptoms are taken less seriously — **believing the patient is a clinical intervention.**
  Plus the physiology that traps people: **visual estimation of blood loss consistently underestimates
  it**, and **a young healthy woman compensates well and then decompensates suddenly**, so normal vital
  signs are not reassurance during ongoing bleeding. And **postpartum eclampsia can present after
  discharge** — teach the warning signs before the patient leaves.
- **⚠⚠ Paediatric dosing is where decimal points kill** (NUR1423C) — **a misplaced decimal is a tenfold
  error**. Both conventions stated with their reason: **always a leading zero, never a trailing one**,
  because each exists because of deaths. And **children compensate then crash** — a child holds blood
  pressure until late, so **hypotension is a very late and ominous sign**, not an early one.
- **⚠⚠ Neurovascular checks: a limb can be lost while everything looks stable** (PRN0042C) — compartment
  syndrome is detected by nursing observation, and **the earliest reliable sign is pain out of proportion,
  unrelieved by analgesia**. The sharp professional point: **escalating analgesia requests are a warning,
  not drug-seeking behaviour — treating them as the latter has cost people limbs.** And **the classic late
  signs are late**; a present pulse does not rule it out.
- **⚠⚠ Neurological change is measured against the last assessment** (PRN0042C) — **do the assessment
  rather than copying the previous entry**; carrying forward a stale assessment is a documented cause of
  missed deterioration and is exactly what happens on a busy shift. **A change in level of consciousness
  is the earliest sign and the easiest to attribute to tiredness or the hour.**
- **⚠⚠ Psychological safety: teams with high psychological safety report *more* errors, not fewer**
  (HSA4353) — the counter-intuitive finding that is the whole point. They are surfacing errors, not making
  them, and **low reporting is a warning sign rather than a success measure.** Paired with the management
  half in HSA4107: **punitive responses to error destroy reporting, and an organisation that cannot see
  its errors cannot prevent them.**
- **⚠⚠ The Stark Law is strict liability** (HSA4107) — **good intentions are not a defence and a technical
  violation is a violation**, which is the point healthcare managers most often get wrong. Alongside the
  Anti-Kickback Statute (intent-based, criminal, "anything of value" read broadly) and the False Claims
  Act with its whistleblower provision.
- **⚠⚠ Under-coding is not the safe option either** (HIM1273L) — it loses legitimate revenue, misrepresents
  acuity, and distorts risk adjustment. **The professional position is accuracy, not caution in one
  direction** — the same framing already recorded for HIM2283C, and worth keeping as the standing line on
  coding ethics. Plus: **pressure to code a particular way is a compliance concern, not a management
  instruction.**
- **⚠⚠ Three misreadings that do the most damage in clinical practice** (HSC3730) — correlation presented
  as causation; **a p-value is not the probability the finding is true**, and a significant result from a
  large study can describe a difference too small to matter; and **relative risk without absolute risk is
  the standard way to make a small effect sound large.** Plus **surrogate outcomes**: drugs that improved
  a laboratory value while harming patients are a real and repeated history.
- **⚠⚠ Florida's own legal furniture, named** (HSC4645) — **the Baker Act (Ch. 394)** and **Marchman Act
  (Ch. 397)**; **mandatory abuse reporting under Ch. 39 and Ch. 415, where the obligation attaches to
  suspicion rather than proof and failing to report is itself an offence**; advance directives under
  Ch. 765; EMTALA. Flagged as **among the fastest-moving content in the repository**, with an explicit
  statement that nothing in the guide is legal advice.
- **⚠⚠ Florida does not license general dental assistants — but specific duties are separately regulated**
  (DEA) — expanded functions and **taking radiographs** each require Board-approved qualification under
  Ch. 466. **"The dentist told me to" is not a defence**, and the guide tells students to hold the line
  during externship. Paired with **sterilisation must be monitored, not assumed**: an autoclave can run a
  full cycle, display success, and fail to sterilise — **only the spore test detects it.**
- **⚠⚠ The LPN scope difference is not about skill** (PRN) — **independent nursing assessment and the
  judgements following from it are reserved to the RN**, and IV therapy in particular carries specific
  Florida restrictions. **Never rely on what a workplace tells you is normal — read the rule.** Paired
  with the honest career note that **hospital LPN roles have narrowed** as systems hire predominantly RNs,
  which is worth knowing before planning a hospital career on the credential.
- **⚠ Transitioning is harder than it looks** (NUR1322) — for LPNs, paramedics and medics bridging to RN,
  **the difficulty is not the skills, it is the reframing**, and **answering examination questions as your
  prior role would is the single most common source of difficulty** — the right answer usually involves
  assessing or escalating rather than doing.

### Batch 114: DSC computing and office — **CAI** (1) + **CEN** (2) + **CNT** (1) + **COP** (3) + **DIG** (1) + **OST** (3)

Eleven guides pushed, all v1.0, all clean, all live. **CAI, CEN, CNT, COP, DIG and OST are all complete at
0 queued.** Forty prefixes finished in the last thirteen batches.

| Course | cr | hrs | Basis |
|---|---|---|---|
| CAI2010 Introduction to AI and ML with Python | 3 | 45 | lecture 15/cr; ⚠ fall only |
| CEN2002C Software Design and Development I | 3 | **60** | ⚠⚠ C-form convention; ⚠ prereq-**or**-coreq |
| CEN4801 Systems Integration | 3 | 45 | lecture 15/cr; ⚠ fall only |
| CNT4703C Voice and Data Network Design | 3 | **60** | ⚠⚠ C-form convention |
| COP2072 Reporting Services | 3 | 45 | lecture 15/cr; ⚠ spring only |
| COP4708 Applied Database I | 3 | 45 | lecture 15/cr; ⚠ gates two later courses |
| COP4709 Applied Database II | 3 | 45 | lecture 15/cr; ⚠ spring only |
| DIG2441 Mobile Devices and Social Media | 3 | 45 | lecture 15/cr; ⚠ **no terms published** |
| OST2336 Business Communications | 3 | 45 | lecture 15/cr; ⚠ spring only |
| OST2713C Advanced Computer Software Applications | 3 | **60** | ⚠⚠ C-form convention |
| OST2828 Business Presentation Software | 1 | 15 | lecture 15/cr; ⚠ spring only |

**Ratio pinned from five live anchors**: **unsuffixed computing and office courses at 15 hrs/cr** —
CEN4010, CEN3722, CNT2402, OST2401 and CGS1570 are all live at 3 credits and 45 hours.

### ⚠⚠ Batch 114: three C-suffix divergences in one batch — and the validator corrected my first answer

**CEN2002C, CNT4703C and OST2713C all carry a C the Daytona State catalog does not.** All three resolved
by the standing 404-on-C rule to **CEN2002, CNT4703 and OST2713**. **This is the largest single-batch
cluster of the pattern so far** — the running total across the corpus is now well into double figures
(MSL, RET, CTS ×2, ETP, and these three among them).

**⚠ I priced all three at Daytona State's unsuffixed figure (3/45) on the first build, and
`validate_drafts.py` flagged all three:** *"is an integrated lecture+lab (C) course but has only 45
contact hours."* **The validator was right and the batch-109 precedent settles it** — CTS1851C and
CTS2353C had exactly this divergence and were priced at the **C-form convention of 20 hrs/cr**, not at
DSC's unsuffixed figure.

**Repriced to 3/60, and the guides now carry both numbers deliberately** under a heading saying so:
DSC's unsuffixed course is **45**; the C-suffixed course at whatever institution offers it is estimated at
**60**; and the offering institution's own catalog is authoritative. **Giving both is strictly more
useful than choosing one silently**, because a reader reconciling against another catalog needs to know
which basis produced the number.

**Two things worth recording as method:**

1. **The rule, stated cleanly: when the queue carries a C form and the canonical institution publishes
   only the unsuffixed course, price at the C convention and state both figures.** The guide is written
   for the queued number, and the queued number is a combined course.
2. **`validate_drafts.py` caught a reasoning error, not a typo.** Its cross-field checks encode
   conventions this repository derived, and **a warning from it is worth treating as a claim to be
   argued with rather than noise to be pushed past.** All three warnings here were substantive.

### ⚠ Batch 114: a catalog construction not previously recorded — "Prerequisite *or* Corequisite"

**CEN2002's requirement is published as "Prerequisite or Corequisite: (COP2800 or COP2360 or CGS2820) and
COP2700"** — meaning **the programming and database courses may be taken in the same term rather than
before.** Every prerequisite recorded in this repository until now has been one or the other; this is the
first explicitly *either*.

It matters for advising in both directions: **it is a genuine scheduling flexibility that a student
reading a curriculum plan quickly will miss**, and **concurrent enrolment is meaningfully harder than
sequential**, so it is not free. The guide states both and tells the reader to confirm with an advisor.
**Worth watching for elsewhere** — it is easy to flatten into a plain prerequisite when transcribing.

### ⚠ Batch 114: a fourth prefix with no published terms of offering

**DIG2441 publishes neither prerequisites nor terms.** Handled with the standing honest-gap treatment —
say what the catalog publishes, say what it does not, direct the reader to the department. This joins
HSC4550 (batch 113, no prereq), RTE3116 (batch 109, no prereq or terms), and the earlier instances.

**Meanwhile eight of eleven courses in this batch are single-term offerings**, continuing the pattern
named at batch 112. **COP4708 is the interesting one**: it is offered fall *and* spring, and it gates
**COP4709 (spring only)** and **CEN4801 (fall only)** — so its timing determines the shape of two later
terms in opposite directions. Flagged in all three guides.

### Batch 114: technical content worth carrying

- **⚠⚠ The model learns the data, including the parts you did not want it to** (CAI2010) — bias in
  training data is reproduced **and laundered through the appearance of objectivity**, which makes it
  harder to challenge than the human decision it replaced. **Removing the protected attribute does not
  remove the bias** — other fields correlate with it. And the shortcut example worth keeping: **a medical
  imaging model that appeared to detect disease had learned to recognise which hospital's scanner produced
  the image.** It scored beautifully and was useless. Plus the framing for labels: **a label recording who
  was arrested is not a record of who committed a crime.**
- **⚠⚠ If your accuracy looks wonderful, suspect leakage before celebrating** (CAI2010) — scaling before
  splitting, features only known after the outcome, and **tuning against the test set until it stops being
  a test set.** Paired with: **accuracy is the wrong metric on imbalanced data** — 99% accuracy on a 1%
  prevalence condition by always answering "no". **In this field the surprisingly good number is usually
  a bug.**
- **⚠⚠ Generative AI: do not paste confidential or client data into a third-party service** (CAI2010) —
  now one of the most common ways employees create reportable incidents. And **"the model wrote it" is not
  a defence** for a defect, a licence violation, or a false statement.
- **⚠⚠ SELECT before you DELETE** (COP4708, COP4709) — write the WHERE clause first, run it as a SELECT,
  look at what comes back, then convert it. Wrap it in a transaction and **treat an unexpected row count
  as the signal to roll back rather than to shrug.** Paired with **check which server you are connected
  to** — running a correct statement against production is one of the commonest serious incidents in the
  field — and the honest one: **a destructive change reported within a minute is usually recoverable;
  concealed for an hour it frequently is not.**
- **⚠⚠ SQL injection: the fix is parameterised queries and it is not optional** (COP4708, COP4709) —
  never concatenate user input into SQL, **hand-rolled escaping is repeatedly defeated**, and **stored
  procedures are not automatically safe** if they build dynamic SQL from their arguments.
- **⚠⚠ Concurrency bugs do not reproduce, so you reason about them instead** (COP4709) — and **the lost
  update is the one that bites applications**: two users read, both write, the second silently discards
  the first, **and nothing errors so nobody knows.** Plus **access objects in a consistent order** to
  prevent most deadlocks outright, and **do not solve blocking by reading uncommitted data** — it silences
  the symptom and returns rows that may never exist.
- **⚠⚠ A wrong report is worse than no report** (COP2072) — people act on it confidently for months.
  **Joins silently change your numbers**: an inner join drops unmatched rows, a one-to-many join inflates
  every sum, **and both produce a plausible total that is simply wrong.** And the organisational half:
  **most disputes about a report are actually disputes about a definition** — write the definition on the
  report. Plus **reports are an access path to the database, frequently the one with the weakest
  controls.**
- **⚠⚠ Integrations are where the security holes live** (CEN4801) — **service accounts accumulate
  excessive privilege** because narrowing them was fiddly, and that account becomes the most valuable
  credential in the organisation. And on migration: **the technical transfer is the easy part; what takes
  the time is that the two systems disagree about what the data means.** **Decide what happens to records
  that cannot migrate cleanly with the business, in advance, in writing.**
- **⚠⚠ Voice is unforgiving in a way data is not** (CNT4703C) — **jitter is frequently worse than raw
  latency**, and a link with good average latency and bad jitter **sounds terrible while every measurement
  looks fine.** Plus the Florida-specific point: **telephones used to work when the power failed; IP
  phones do not unless someone designed for it** — a hurricane-season question, not a theoretical one.
  And **redundancy that shares a path is not redundancy** — two carriers' circuits frequently run in the
  same conduit.
- **⚠⚠ Requirements failures dominate project failure** (CEN2002C) — **users cannot tell you what they
  want in the abstract and it is unreasonable to expect them to; they can tell you what is wrong with
  something you show them.** And the test that makes it operational: **if you cannot write a test for it,
  it is not a requirement yet.** Plus **the workarounds people have invented are the requirements nobody
  wrote down.**
- **⚠⚠ Spreadsheet errors are endemic, and the root cause is data structure, not formulas** (OST2713C) —
  **one row per record, no merged cells, no formatting carrying meaning.** **Never let colour or bold be
  the only record of something** — formatting is invisible to every formula and is lost the moment anyone
  copies the data. Extends the CGS1570 finding already in this file. Plus the warning signs that a
  spreadsheet should have become a database, ending with **"which version is the current one?"**
- **⚠⚠ Email is permanent, forwardable, and discoverable** (OST2336) — **the practical test is whether
  you would be comfortable if it were read aloud to the person it is about, to your manager, or in a
  courtroom.** And: **never write in anger** — draft it with the recipient field empty. Paired with the
  structural point that **business writing states the conclusion first**, which is the opposite of
  academic structure and is what trips people in their first job.
- **⚠⚠ The slides are not the talk** (OST2828) — **an audience cannot read and listen at the same time**,
  which is why dense slides make a good speaker worse, and **never read your slides aloud.** If the deck
  has to work as a document, **write a document** — a deck that stands alone and a deck that supports a
  speaker are different artefacts.
- **⚠⚠ Sponsored content disclosure, restated for a design audience** (DIG2441) — clear and conspicuous
  **where the claim is**, plain words not abbreviations, and **"I credited them" is not permission** to
  use someone's music, footage, or likeness. Consistent with the MAR block at batch 110.

### Batch 115: DSC science and mathematics — **BOT** + **MCB** + **PCB** (2) + **SOS** + **PHY** + **STA** + **MGF** + **MAT** + **PSB** + **PET**

Eleven guides pushed, all v1.0, all clean, all live. **All ten prefixes complete at 0 queued.** Fifty
prefixes finished in the last fourteen batches. **Six further rows skipped as placeholder shells** (see
below), leaving **35 queued** — the queue is now finishable in roughly three more batches.

| Course | cr | hrs | Basis |
|---|---|---|---|
| MCB1010C Microbiology and Lab | 4 | **90** | ⚠⚠ **catalog publishes its own split** |
| PCB3034C General Ecology and Lab | 4 | 90 | ⚠ derived from MCB's published split; fall only |
| SOS2006C Introduction to Soil Science and Lab | 4 | 90 | ⚠ same; spring only |
| PCB3203 Cell Physiology | 3 | 45 | lecture 15/cr; fall only |
| BOT2150C Native Plants of Central Florida | 3 | 60 | ⚠ C divergence → C convention |
| PHY1032 Energy and its Environmental Effects | 3 | 45 | lecture 15/cr |
| STA4024 Statistics II | 3 | 45 | lecture 15/cr; spring only |
| MGF2131 Mathematics in Context | 3 | 45 | lecture 15/cr |
| MAT0056L Developmental Mathematics II Lab | **2** | 30 | ⚠⚠ **developmental, not PSAV** |
| PSB2442 Addictions I | 3 | 45 | lecture 15/cr |
| PET2621 Principles of Athletic Training | 3 | 45 | lecture 15/cr; fall only |

### ✅ Batch 115: a catalog that publishes its own contact-hour split — and it resolves a live ambiguity

**MCB1010C's catalog entry states the structure directly: "Three-hour lecture, three-hour laboratory."**
That is a **tier-1 hour source** — the catalog's own published split — and it is the first one to appear
in the corpus in many batches. Six contact hours a week over a standard term gives **90 hours at 4
credits**.

**What makes it more valuable than a single course's figure is that it settles a genuine ambiguity.** The
live corpus carries four-credit laboratory sciences at **two different figures**:

| Convention | Live evidence | Implied structure |
|---|---|---|
| **75 hours** | BSC1010C, CHM1025C (both 4/75) | 3 lecture + 2 laboratory |
| **90 hours** | BSC1085C, BSC2085C (both 4/90) | 3 lecture + 3 laboratory |

Under the documented hour-source hierarchy, **two competing tier-2 anchors that both match the credit
value cannot discriminate** — the batch-96 refinement (*prefer the anchor matching the credit value over
the one matching the series*) does not apply when both match. **MCB1010C's published split breaks the tie
by establishing that Daytona State genuinely runs 3+3**, and it was used to anchor **PCB3034C** and
**SOS2006C**, both labelled derived with the competing 75-hour convention stated explicitly.

**Generalisable, and worth adding to the hierarchy: a published split anywhere in an institution's
catalog is evidence about that institution's conventions, not only about that course.** When two live
conventions compete, look for a course in the same family whose entry publishes its structure — one such
entry resolves a whole group.

### ⚠⚠ Batch 115: a leading zero means two different things in Florida — and this is the other one

This repository has recorded the **0000-level PSAV clock-hour trap** many times: the leading zero marks
postsecondary adult vocational instruction, the catalog renders clock hours under a "Credit Hours"
heading, and `credits` must be 0.

**MAT0056L is not that.** It is **college preparatory / developmental education**, which also carries a
leading zero — and the reading inverts completely:

| | **PSAV (e.g. BCV0080L, PRN0207C)** | **Developmental (MAT0056L)** |
|---|---|---|
| What the leading zero marks | vocational clock-hour instruction | college preparatory coursework |
| The published number | **clock hours** rendered as "Credit Hours" | **actual credit hours** |
| `credits` in the guide | **0** | **2** (as published) |
| Degree applicability | none | **none** — "cannot be applied toward associate degree requirements" |
| Financial aid enrolment status | clock-hour rules, different scheme | **normally counts**, with limits on developmental coursework |

**This is a real trap in the opposite direction from the PSAV one.** Reading MAT0056L's "2 Credit Hours"
as clock hours would be absurd — two clock hours for a full algebra review — but the corpus has trained a
reflex to distrust that heading at 0-level, and the reflex is wrong here.

**Rule to apply: at a 0-level number, read the subject and the description before deciding.** Vocational
prefixes (BCV, PRN, DEA, MSS, CSP, TDR, MEA, CJD) are clock-hour; **academic prefixes at 0-level (MAT,
ENC, REA) are developmental education carrying real but non-degree institutional credit.** The guide
carries a full comparison so a reader hitting either case is not misled.

**⚠ The financial aid consequence differs from the zero-credit SLS case too**, and the guide says so:
developmental credit normally does count toward enrolment status — unlike a zero-credit course — but aid
coverage of developmental coursework is limited. Confirm with financial aid.

### ⚠ Batch 115: six requirement-placeholder shells skipped

**ENC2998A, ENC2999A, COM2998B, COM2999B, SPC2999A, SSI2997A** were skipped after **fetching ENC2998A and
confirming the catalog page carries only a number, a placeholder title and a credit value** — no
description, no prerequisites, no terms. The titles are administrative stubs: *"English"*,
*"Communicatn Req"*, *"Speech Requirmt"*, *"Social Sci Req"*.

These are **transfer/requirement placeholders**, structurally the same as the 9xx shells, and a guide for
one would have nothing to describe. **Marked `skipped` with a note rather than deleted**, so the Request
a Curriculum Guide feature can resurrect them, and **added to `REVIEW_QUEUE.md` as item 8, grouped with
the 9xx re-screen** so both scope calls can be settled together.

**⚠ Detection note worth keeping: the signature is a truncated administrative title plus a `x99x` number.**
One fetch confirmed the class; the other five did not need one.

### ✅ Batch 115: REVIEW_QUEUE item 7 resolved — PHT1006C is buildable

**PHT1006C was logged as blocked with the holder unknown.** Checking the queue against
`daytona_courses.csv` showed **Daytona State does publish it — as PHT1006 (Introduction to Physical
Therapy)**, without the C. The standing 404-on-C rule applies and the row is buildable; it is scheduled
in the remaining work. **Item 7 marked resolved.**

**The method point: a blocked item was cleared by a local grep, not a fetch.** The inventory file answers
"does the canonical institution offer this at all" for the whole queue at once, and **it is worth
re-running against any older blocked item rather than assuming the block still holds.**

### Batch 115: content worth carrying

- **⚠⚠ Antimicrobials do not create resistance; they select for it** (MCB1010C) — the resistant organisms
  were already present and killing everything else hands them the field. **That distinction is the one
  students most often get wrong**, and it changes which responses make sense. Paired with the clinical
  point: **you will be asked for antibiotics for viral illness constantly, and saying no kindly and
  explaining why is a clinical skill.** And on the bench: **aerosols are the hazard people do not see** —
  a hot loop, vigorous pipetting, and a dropped plate all generate them.
- **⚠⚠ Florida is fire-dependent, and suppressing fire destroys what it was meant to protect** (PCB3034C)
  — longleaf sandhill, scrub and flatwoods need frequent fire, and without it hardwoods invade and the
  diversity in the ground layer is shaded out. **Suppression also makes the eventual fire far worse.**
  The framing worth carrying: **in these systems fire is not disturbance in the sense of damage — its
  absence is.** And **knowing which community you are standing in is the whole management question**,
  since hammocks and cypress domes are damaged by fire.
- **⚠⚠ Florida's water quality problems are largely soil problems** (SOS2006C) — sandy soils have very low
  cation exchange and water-holding capacity, **nitrate leaches readily**, and **the limestone geology
  connects the surface to the aquifer directly, so there is very little filtration between a lawn and a
  spring.** Concrete and current: **many Florida counties have fertiliser ordinances with summer
  application blackouts** — enforceable, and varying by jurisdiction. Plus **drained organic soils
  subside**, physically losing elevation, which has reshaped the Everglades Agricultural Area.
- **⚠⚠ Never release an animal or plant into the wild, including aquarium fish and plants** (PCB3034C,
  BOT2150C) — several of Florida's worst invasions began exactly that way. And **clean gear between
  sites**; decontamination is the cheapest control available.
- **⚠ Florida law protects native flora, and collecting needs permission** (BOT2150C) — with the practical
  advice that **a good photograph of the diagnostic features usually identifies the plant**, and the
  honest note that **some attractive Florida natives have been driven toward extinction by collecting.**
  Plus how identification is actually learned: **learn families first, learn the vegetative characters
  because most of the year most plants are not flowering, and use habitat as evidence.**
- **⚠⚠ The p-value is the most misused number in science** (STA4024) — it is **not** the probability the
  null is true, it says **nothing about effect size**, and **a non-significant result is not evidence of
  no effect.** Plus the multiple-comparisons point stated concretely: **twenty independent tests at 0.05
  yields one significant result from pure noise.** And the assumptions half: **independence is the
  assumption most often violated and least often checked**, and violating it is far more damaging than
  violating normality — while **software returns confident coefficients either way.**
- **⚠⚠ Percentage changes do not reverse** (MGF2131) — a 50% fall then a 50% rise leaves you **25% down**,
  which explains a great deal of misleading financial presentation. Plus **relative risk without absolute
  risk**, **percentage points versus per cent**, and the highest-return content in the course: **run the
  minimum-payment credit card arithmetic once and you will not forget it**, and **compare loans on the
  APR, not the monthly payment** — a lower payment from a longer term costs substantially more, and that
  is how expensive loans are sold.
- **⚠⚠ How to check an energy claim in thirty seconds** (PHY1032) — **kilowatts and kilowatt-hours are
  different quantities**; **an efficiency figure without a stated boundary is not a figure**; **capacity
  is not generation**, and capacity factor is the number usually omitted; and **any over-unity claim is
  wrong without needing to find the error.**
- **⚠⚠ Naloxone: giving it when unsure carries essentially no risk; withholding it can be fatal**
  (PSB2442) — it has no effect on someone who has not taken opioids. **Call 911 first, because naloxone
  wears off and the overdose can return.** And **Florida's Good Samaritan provision** matters as an
  intervention in itself: **fear of arrest is a documented reason people do not call.** Plus **snoring in
  an unresponsive person is an obstructed airway, not sleep.**
- **⚠⚠ Stigmatising language changes professional judgement** (PSB2442) — studies have found clinicians
  given identical cases described in different terms recommended **more punitive responses for the
  stigmatising wording.** That makes person-first language a clinical variable, not politeness. And:
  **medication for opioid use disorder is among the best-evidenced interventions in behavioural health
  and substantially reduces mortality** — the "replacing one drug with another" misconception costs
  lives, including inside treatment settings. Paired with the career honesty: **relapse is part of the
  condition, and practitioners who take it personally do not last.**
- **⚠⚠ Exertional heat stroke: cool first, transport second** (PET2621) — **survival depends on how fast
  core temperature comes down, not on how fast an ambulance arrives**, and delaying cooling to move the
  athlete costs lives. **The tub, ice and water must be ready before practice starts.** And the
  misleading sign: **the athlete may still be sweating.** Florida's humidity is why **wet bulb globe
  temperature, not air temperature**, is the measure.
- **⚠⚠ Athletic training now requires an accredited master's degree** (PET2621) — the bachelor's route
  many people remember has been phased out, and **students plan on outdated information.** Eighth field
  in the corpus with the accreditation-gate trap (after CAPTE, CAAHEP, ACOTE, CoARC, JRCERT, CIDA, ABET).
  Stated bluntly: **this course does not make you an athletic trainer**, and its value is to coaches,
  teachers and fitness professionals who need to recognise, respond and refer.
- **⚠⚠ Concussion: brief seizure-like movements are common in cardiac arrest and are frequently mistaken
  for a seizure** (PET2621) — a collapsed unresponsive athlete is in cardiac arrest until proven
  otherwise. Plus **second impact syndrome** as the reason "he says he's fine" is not a basis for a
  decision, and **athletes under-report deliberately because they know what answers get them back on the
  field.**
- **⚠ Specialisation is a trade-off, and the trade-offs explain the pathology** (PCB3203) — the red blood
  cell discarded its nucleus and cannot repair itself; **neurons committed to extreme length and became
  dependent on transport machinery and on an oxygen supply they cannot buffer**, which is why neural
  tissue fails first when perfusion stops. **Ask what each specialisation costs** — it converts a list of
  cell types into a set of predictions.
- **⚠ Confirm this is the right mathematics course for your pathway** (MGF2131) — quantitative reasoning
  and college algebra lead different places, and **taking the wrong one costs a term.** Paired with the
  developmental-course arithmetic in MAT0056L: **Florida charges substantially more for a third attempt**,
  so failing college algebra twice costs more than doing the preparatory course properly once.

### Batch 116: DSC education (5) + sociology (2) + criminal justice (2)

Nine guides pushed, all v1.0, all clean, all live. **EDE, EDG, EEX, SYD, CJT and CJD are all complete at
0 queued.** Fifty-six prefixes finished in the last fifteen batches. **26 rows remain** — two more batches.

| Course | cr | hrs | Basis |
|---|---|---|---|
| EDE1042 FTCE Test Prep 1 (GKT) | 1 | 15 | lecture 15/cr; instructor permission |
| EDE3043 FTCE Test Prep 2 | 1 | 15 | lecture 15/cr; ⚠ **EPI funding warning in the catalog** |
| EDG2770 Exploring Global Education Issues | 3 | 45 | ⚠ indicative — immersive field course |
| EEX2080 Teaching the Exceptional Learner | 3 | 45 | lecture 15/cr; spring only |
| EEX4034 Intro to ESE for Inclusive Teachers | 1 | 15 | lecture 15/cr |
| SYD2707 Race and Ethnicity | 3 | 45 | lecture 15/cr; fall only |
| SYD2803 Gender and Society | 3 | 45 | lecture 15/cr; spring only |
| CJT2100 Criminal Investigation | 3 | 45 | lecture 15/cr |
| CJD0259 "Le Sem-Auto Pi" | **0** | — | ⚠⚠ **thinnest entry in the corpus** |

### ⚠⚠ Batch 116: the thinnest catalog entry yet — and what an honest guide looks like at that extreme

**CJD0259's Daytona State page carries a course number, the truncated title "Le Sem-Auto Pi", and the
figure 1.** No description, no prerequisites, no corequisites, no terms, no fee. **A targeted web search
did not resolve the title either** — CJD course numbering is not indexed in a way that answered it.

This is thinner than any of the seven prior honest-gap cases, which all had at least a readable title or a
credit value that could be interpreted. Here **three separate things are unknown at once**:

1. **The title.** Clearly truncated and not a readable course name. **The guide reproduces it exactly as
   published rather than expanding it** — the plausible expansion was deliberately not asserted, because
   an inference presented as a fact is worse than a visible gap.
2. **What the figure "1" measures.** CJD is Florida's **CJSTC criminal justice training** prefix, and its
   leading zero normally means clock hours — but **a single clock hour is implausible for a training
   course**, and a single college credit at a 0-level vocational number is equally unusual. **Neither
   reading is safe, so the guide asserts no contact-hour figure at all** (`contact_hours: 0`, which
   pushes as null — verified live).
3. **The content.** Nothing published, and nothing inferred.

**The treatment, recorded as the standing method for a near-empty entry:**

- **Lead with what could not be established**, itemised, before anything else on the page.
- **Write the body as clearly-labelled context** — here, what CJD coursework is under the CJSTC framework
  — with an explicit statement that **none of it describes this course**.
- **Close by restating the gaps plainly**, so a reader arriving at the bottom is not left with an
  impression the top of the page disclaimed.
- **Name the one authority that can answer** — the delivering programme — rather than a generic "confirm".

**The principle worth naming: a guide for a near-empty entry exists so the course number resolves to
something honest rather than to nothing.** It is not a description, and it should say so more than once.

### ⚠ Batch 116: a funding warning published inside a course description

**EDE3043's catalog entry states that Educator Preparation Institute students who elect to take it must
pay for it independently, because the EPI programme does not allocate elective funding for it.** That is
an unusual thing to find in a course description, and it is there because it catches people.

**Recorded because it is a class of information the corpus has not seen before: a cost warning attached to
a specific student population.** It joins offering-frequency and prerequisite timing as **catalog facts
that are advising-critical rather than descriptive**, and it belongs high in a guide rather than in a
footnote. Flagged prominently, with the note that the course may still be worth paying for — but as a
decision rather than a surprise on a bill.

### Batch 116: content worth carrying

- **⚠⚠ The four documented ways investigations go wrong** (CJT2100) — the strongest content in the batch,
  and it rests on unusually good evidence: **several hundred DNA exonerations provide cases where the true
  answer is known and the investigative record can be examined against it.** The recurring contributors —
  **mistaken eyewitness identification, false confessions, flawed forensic testimony, and tunnel vision**
  — are **process failures rather than failures of effort or integrity**, which is why they are teachable.
  - **Eyewitness memory is reconstructive, and the altered memory feels exactly as vivid as an accurate
    one.** **Confidence stops tracking accuracy once a witness has been given feedback** — "that's the one
    we suspected" measurably inflates both later confidence and the recalled quality of the view. Hence
    double-blind administration, a confidence statement in the witness's own words *at the moment of
    identification*, fair fillers, and the instruction that the perpetrator may not be present.
  - **People confess to crimes they did not commit**, and juveniles and people with intellectual
    disabilities are markedly more vulnerable. **Guard the details** — a confession corroborates only if
    it contains information the investigator did not supply, and **details leak through questions,
    photographs, and reactions.**
  - **Tunnel vision is the mechanism that ties the rest together**, and **it happens to conscientious
    people** — which is precisely why process protections exist rather than exhortations to be careful.
    The operational habit: **ask what would show your theory is wrong, and go and look for it.**
  - **Be sceptical of forensic disciplines that have not demonstrated validity** — rigorous national
    reviews found several long-accepted pattern-comparison methods lack established error rates, and
    **overstated forensic testimony is itself a recurring contributor to wrongful convictions.**
  - Plus the unglamorous half: **modern DNA analysis is sensitive enough that the investigator's own DNA
    is a contamination risk**, and **wet biological evidence must be dried and packaged in paper, not
    sealed in plastic.**
- **⚠⚠ The ethics of short-term international engagement** (EDG2770) — treated as the substance of the
  guide rather than a caveat, because **it is the difference between education and tourism.**
  **Do not do work local people could be paid to do** — it displaces employment and the airfare would
  frequently have funded the work several times over. **Do not practise beyond your competence abroad**;
  a task you are unqualified for at home does not become acceptable because the setting is poorer.
  **The well-established consensus advises against orphanage volunteering entirely**, because short-term
  visitors forming and breaking attachments with vulnerable children causes documented harm. And the
  honest framing: **come to learn, not to help — you are the beneficiary, and pretending otherwise
  produces the worst behaviour.** Paired with hard practical deadlines: **passport validity is the single
  most common reason a student cannot travel**, and travel vaccinations need six to eight weeks.
- **⚠⚠ Least restrictive environment is a presumption, not a placement** (EEX2080, EEX4034) — the IDEA
  provision most commonly misunderstood. **Removal must be justified by the student's needs, not by the
  school's convenience or by a category label.** Paired with: **read the IEPs of the students in your
  class** — general education teachers are bound by them, they are frequently not read, and **"I did not
  know" is not a defence.**
- **⚠⚠ Accommodations and modifications are different, and confusing them harms students** (EEX4034) — an
  accommodation preserves the standard; **a modification changes the expectation and can move a student
  off the path to a standard diploma.** That is sometimes right, decided by a team with the family — **and
  it must never happen by accident because a teacher quietly lowered expectations.** Plus: **provide
  accommodations routinely, not on request**, since requiring a student to ask each time puts the burden
  in the wrong place.
- **⚠⚠ Identity-first language is preferred by many communities** (EEX guides) — a genuine refinement on
  the person-first default this repository has used elsewhere. Many autistic adults and many Deaf people
  regard the characteristic as part of who they are; **the respectful position is to follow the preference
  of the person or community and to ask rather than assume.** Paired with **presume competence** — the
  cost of underestimating a student is far higher than the cost of aiming too high.
- **⚠⚠ You may be the first professional to notice** (EEX2080) — early childhood practitioners see
  children daily alongside peers, which puts them in an unusually good position. **"He'll grow out of it"
  is the phrase that costs children the window in which support works best**, and the cost of referring a
  typically-developing child is very low. Concrete Florida routes named: **Early Steps under three, the
  district from three**, and **families can request an evaluation themselves, in writing.**
- **⚠⚠ "Socially constructed" does not mean "not real"** (SYD2707) — the construction claim is about
  biology and is settled; the reality claim is about consequences. **A category with no biological basis
  can still structure a society completely — money is socially constructed too.** Paired with the
  analytical discipline: **disparity is not automatically evidence of discrimination, and absence of
  intent is not evidence of no discrimination** — establishing which mechanism produces a gap is the
  empirical work the course teaches.
- **⚠⚠ The pay gap: know which number you are looking at** (SYD2803) — **the raw and adjusted gaps are
  both correct and answer different questions**, which is exactly why each side of the argument quotes
  only one. And the subtle point: **the controls are part of the phenomenon** — adjusting for occupation
  removes occupational segregation from the measured gap, but how people ended up in different
  occupations is one of the questions being asked.
- **⚠ A shared framing for both SYD guides**: these are contested-topic courses, and the guides say so —
  **separate empirical from normative questions**, **distinguish individual from institutional levels**,
  and **nobody speaks for a group**: a classmate's experience is evidence about their experience, and
  **nobody should be asked to explain or defend a category they belong to.** Consistent with the SLS2505
  critical-thinking treatment.
- **⚠ Take a full timed practice test before studying anything** (EDE1042) — the diagnostic tells you
  which subtest is actually at risk, **and it is almost never the one students assume.** Each subtest is
  passed separately, so **time spent improving a section you would already pass is wasted** — the
  commonest preparation mistake. And for EDE3043: **these examinations are built from a published
  competency list which is the syllabus** — studying anything else is guessing.

### Batch 117: DSC health and PSAV — **DES** (2) + **MSS** (3) + **MEA** + **EMS** + **SON** + **PHT** + **CSP**

Ten guides pushed, all v1.0, all clean, all live. **DES, MSS, MEA, EMS, SON, PHT and CSP are all complete
at 0 queued.** Sixty-three prefixes finished in the last sixteen batches. **16 rows remain — one batch.**

| Course | cr | hrs | Basis |
|---|---|---|---|
| DES0002 Dental Anatomy and Physiology | 0 | 30 | PSAV clock hours; ⚠ catalog typo in coreq |
| DES2600 Medical and Dental Emergencies | **2** | 30 | ⚠ credit course in a prefix that also carries PSAV |
| MSS0283 Allied Modalities I | 0 | 43 | PSAV clock hours |
| MSS0284 Allied Modalities II | 0 | 43 | PSAV clock hours |
| MSS0315 Theory and Practice of Hydrotherapy | 0 | 15 | PSAV clock hours — shortest in the batch |
| MEA0005 Introduction to Medical Assisting | 0 | **121** | ⚠⚠ catalog publishes **120.9** — fractional |
| EMS1119C Emergency Medical Technician I and Lab | 10 | 200 | ⚠ derived; C convention, clinical is separate |
| SON1210 Intro to Sonographic Physics | 3 | 45 | lecture 15/cr; fall only |
| PHT1006C Introduction to Physical Therapy | 3 | 60 | ⚠ C divergence; both figures stated |
| CSP0003L Cosmetology Bridge Lab | 0 | 240 | ⚠⚠ **requires an active barber licence** |

### ⚠⚠ Batch 117: a fractional clock-hour figure — the first in the corpus

**MEA0005 is published at 120.9 clock hours.** Every PSAV figure recorded until now has been a whole
number. The guide **reproduces the catalog's 120.9 explicitly and shows 121** in the hour field, so the
rounding is visible rather than silent.

**Nothing turns on the tenth of an hour, but the finding is worth keeping for what it reveals:**
clock-hour programmes are built to **state-approved hour totals** derived from curriculum frameworks, not
to convenient round numbers — so a fractional figure is a signal that the number is a real regulatory
quantity rather than an institutional estimate. **Expect more of them in vocational prefixes, and
reproduce the published figure alongside the rounded one rather than quietly rounding.**

### ⚠⚠ Batch 117: a professional licence as a course prerequisite — also a first

**CSP0003L requires an active Florida barber licence to enrol.** Every other entry requirement in this
repository is a course, a placement score, instructor consent, or a programme admission — **this is the
first gate that is a state-issued professional licence.**

The reason is structural and worth recording: **Florida licenses barbering (Chapter 476) and cosmetology
(Chapter 477) separately**, both through DBPR, and **a licensed barber converting to cosmetology takes a
bridge programme rather than repeating an entire cosmetology course.** The catalog's content list is
exactly the complement — nails, waxing, manicure and pedicure, makeup, braiding — **the cosmetology scope
that barbering training does not cover.**

**Generalisable: where two related occupations are separately licensed in Florida, expect bridge courses
between them, and expect the prerequisite to be the other licence.** The guide tells the reader to confirm
current bridge hour requirements with DBPR, since those are set by rule and change.

### ⚠ Batch 117: two smaller catalog observations

- **A prefix carrying both PSAV and credit courses.** **DES0002 is 0-level PSAV at 30 clock hours; DES2600
  is a 2000-level credit course at 2 credits** in the same prefix. The corpus has recorded 0-level and
  credit-level courses separately many times, but **not previously side by side in one prefix in one
  batch** — a useful concrete illustration of why the level digit, not the prefix, decides the reading.
  Both guides cross-reference the other.
- **A catalog typo in a corequisite field.** DES0002's corequisite is printed as **"DEA000"** — one digit
  short of a valid SCNS number. **The intended course is almost certainly DEA0000**, which the catalog
  separately lists as having DES0002 as *its* corequisite, making it a mutual pair. Flagged in the guide
  with the reasoning shown, and the reader told to confirm. Same family as the truncated titles already
  recorded; **not serious, but worth noting that corequisite fields are as prone to transcription error as
  titles are.**

### ✅ Batch 117: the PHT prefix closes

**PHT1006C was REVIEW_QUEUE item 7**, logged as blocked with the holder unknown, and resolved last batch by
a local grep showing Daytona publishes **PHT1006** without the C. Built here at the C convention with both
figures stated (45 for Daytona's unsuffixed course, 60 for the C form), per the standing rule.
**The PHT prefix is now complete apart from PHT2931, which remains on hold pending Ron's 9xx data.**

### Batch 117: content worth carrying

- **⚠⚠ Florida requires human trafficking awareness education and signage for massage establishments**
  (MSS guides) — **illicit massage businesses are a recognised vehicle for labour and sexual
  exploitation**, Florida has had sustained enforcement, and **the reputational and legal exposure for a
  legitimate therapist working in the wrong establishment is real.** The guides give a concrete vetting
  checklist — verify the establishment licence, look at the hours, the signage, and whether other workers
  appear to be living on site — and the hotline number. **This is the most practically protective content
  in the batch and it is entirely Florida-specific.**
- **⚠⚠ Suspected deep vein thrombosis is the massage contraindication everyone must know** (MSS0283) —
  massage over a clot risks dislodging it. **Unilateral calf swelling, warmth, redness and pain warrants
  immediate referral and no massage.** Paired with the one people miss: **impaired sensation removes the
  client's ability to tell you it hurts**, which is the feedback the therapist relies on.
- **⚠⚠ Thermal injury: the clients most at risk cannot warn you** (MSS0315) — the injuries are almost
  never from an obviously dangerous temperature but from **a moderate temperature applied too long to
  someone who could not feel it**. And **the therapist's hand is not a thermometer** — hands are
  acclimatised. Most thermal injuries are duration errors.
- **⚠⚠ Body mechanics decide how long a massage career lasts** (MSS0283) — **stop using thumbs as the
  default tool**; pressure comes from body weight and stance, not muscular effort. **Most experienced
  therapists cannot sustain a full week of consecutive appointments indefinitely**, and planning a mixed
  workload from the start is what makes a long career possible.
- **⚠⚠ Pedicure foot spas have caused documented serious infection outbreaks** (CSP0003L) — mycobacterial
  infections requiring months of treatment and leaving scarring, **because the organism lives in the
  pipework and screens where a wiped surface does not reach.** Hence the full between-client protocol
  including the filter, and the reason the shaving question is asked: **never provide a pedicure over
  broken skin or recently shaved legs.** Plus **never cut cuticles or use a callus shaver** — cutting
  living tissue is outside scope and prohibited.
- **⚠⚠ Salon chemical sensitisation is permanent and can end a career** (CSP0003L) — repeated skin contact
  is how practitioners become sensitised to products they then cannot work with. Source-capture
  ventilation, gloves, and **safety data sheets are an OSHA requirement, not optional.** And **hot wax
  burns**: test every batch, and know that a client on retinoids has fragile skin that burns at a normal
  temperature.
- **⚠⚠ Scene safety is arithmetic, not caution** (EMS1119C) — **a responder who becomes a casualty has
  made the situation worse in every respect: one more patient, one fewer rescuer.** And the
  under-appreciated killer: **traffic**, not the dramatic calls. Plus **stage and wait for law enforcement
  — that decision is correct even when it feels wrong.**
- **⚠⚠ Refusals are the highest-risk paperwork in prehospital care** (EMS1119C) — **a patient who is
  intoxicated, hypoglycaemic, hypoxic or head-injured may appear conversational and lack capacity**, and
  altered mental status is itself a reason they cannot validly refuse. **Correct what you can first** — a
  treated hypoglycaemic patient can then decide; before treatment they could not. **A refusal with no
  assessment recorded is indefensible.**
- **⚠⚠ EMS mental health, stated directly** (EMS1119C) — **rates of post-traumatic stress and suicide in
  this profession are markedly elevated**, the calls that stay with people are not the dramatic ones, and
  **the culture has historically discouraged saying so.** Framed as a normal physiological response to
  repeated trauma exposure rather than a weakness, with **"do not use alcohol as the coping strategy"**
  stated plainly because it is the default in the field.
- **⚠⚠ Ultrasound is operator-dependent — pathology not imaged is pathology not diagnosed** (SON1210).
  Unlike CT or MRI, **the study is constructed in real time and the radiologist sees only what the
  sonographer captured**, which places diagnostic responsibility unusually heavily on the operator. Paired
  with the two findings already in this file for SON1000C, now reinforced: **the SPI physics exam is the
  cumulative gatekeeper — start Edelman in term one**, and **about four in five working sonographers scan
  in pain**, with the habits needing to be built in the first laboratory sessions because **they cannot be
  retrofitted.**
- **⚠⚠ The PT/PTA scope line is legal, not organisational** (PHT1006C) — **a PTA does not evaluate, does
  not establish or alter a plan of care, and does not discharge**, and doing any of them exposes the
  supervising therapist too. But **stopping or modifying within direction when a patient's response
  requires it is squarely within the role** — the guide draws both halves, because students routinely
  under-read the second.
- **⚠⚠ Medical assistants are unlicensed in Florida, and that makes scope a live question** (MEA0005) —
  **the absence of a licence does not mean the absence of limits**: a task requiring a licensed
  professional cannot be delegated to an unlicensed one, and **"the doctor told me to" is not a complete
  defence.** **Telephone triage is where unlicensed staff most often step over the line**, and the
  consequences fall on a patient who never saw anyone.
- **⚠⚠ Dental numbering errors are wrong-tooth errors** (DES0002) — three systems in common use, not
  interchangeable, **and primary teeth use letters in the Universal system**, which is a specific
  recognised confusion in mixed dentition. **Read back what you are charting.**
- **⚠ Syncope is the commonest dental office emergency and the response should be automatic** (DES2600) —
  acting during the prodrome usually prevents the faint entirely, and **the error is assuming prolonged
  unresponsiveness will resolve because it usually does.** Paired with the systemic point: **check the
  emergency kit and oxygen on a schedule — expired contents and empty cylinders are a common and serious
  finding**, and discovering it during an emergency is the worst possible moment.
- **Eighth and ninth entries in the accreditation-gate list.** ARDMS/CAAHEP for sonography and
  CAPTE for the PTA pathway join CAPTE, CAAHEP, ACOTE, CoARC, JRCERT, CIDA, ABET and CAATE. **The trap is
  now recorded across nine distinct fields, and it is the single most-repeated warning in this corpus.**

### Batch 118 (final): **AFR** (2) + **APA** (2) + **ART** + **BCN** + **BCT** + **TDR** + **FSS** (2) + **GRA** + **HHD** + **MNA** + **MUS** + **SCE** + **TAX**

Sixteen guides pushed, all v1.0, all clean, all live. **All fourteen prefixes complete at 0 queued.**

> ## 🏁 The Daytona State queue is finished.
> **1,632 guides live. 100.0% overall. Daytona State 935/935.**
> **288 rows deliberately skipped** — 229 with no DSC coverage, 53 shells (9xx plus the six requirement
> placeholders), and the remainder blocked and recorded. **Nothing is queued.**

| Course | cr | hrs | Basis |
|---|---|---|---|
| AFR4231 Preparation for Active Duty AF401 | 3 | 45 | lecture 15/cr; ⚠⚠ service commitment |
| AFR4232 Preparation for Active Duty II AF402 | 3 | 45 | ⚠ one-sentence catalog description |
| APA1121 Office Accounting II | 3 | 45 | lecture 15/cr |
| APA1711 Computerized Spreadsheet | 3 | 45 | lecture 15/cr |
| ART1331C Drawing III and Lab | 3 | **60** | ⚠⚠ **catalog publishes "four studio hours"** |
| BCN1253C Architectural Drawing II and Lab | 3 | 60 | C form 20/cr (live BCN1251C) |
| BCT1040 Blueprint Reading | 3 | 45 | lecture 15/cr; fall only |
| TDR0304C Computer Aided Drafting and Lab | 0 | 130 | PSAV clock hours |
| FSS1270C Introduction to Craft Beer and Wine | 3 | 60 | ⚠ C **and** title divergence; ⚠⚠ age 21 |
| FSS2210C Food Production III and lab | 3 | 60 | C form 20/cr (live FSS1222C) |
| GRA1543 Graphic Design Studio | 3 | 45 | ⚠ derived; title and fee suggest studio |
| HHD1361 Practical Interior Applications | 3 | 45 | lecture 15/cr; fall only |
| MNA2161 Customer Service Management | 3 | 45 | lecture 15/cr |
| MUS2360C Learning Basic Music Using the Computer | 3 | 60 | ⚠ C **and** title divergence |
| SCE3832 Science Concepts in the Elementary Classroom | 3 | 45 | lecture 15/cr |
| TAX3011 Taxation of Business Organizations | 3 | 45 | lecture 15/cr (live TAX3001 3/45) |

### ⚠⚠ Final batch: a published split that *contradicts* the live anchors — and tier 1 wins

**ART1331C's catalog entry states "Four studio hours."** Over a standard term that is **60 contact hours
at 3 credits** — Daytona State's usual combined-course convention of 20 per credit.

**The live corpus disagrees.** This repository carries **ART1300C (Drawing I) at 3 credits / 90 hours** and
**ART2330C (Life Drawing) at 3 credits / 80 hours** — six and roughly five and a third studio hours a week.

**This is the first case where a tier-1 published split contradicts otherwise-good tier-2 anchors in the
same prefix, and it settles a question the hierarchy had not yet been tested on.** The documented order is
(1) the catalog's own published split, (2) a live guide in the same chain or institution, (3) the prefix
ratio — and **the published figure was used**, with the divergence stated explicitly in the guide and the
reader told that other institutions run comparable courses longer.

**Generalisable, and worth stating plainly: studio conventions vary between institutions more than lecture
or laboratory conventions do.** A studio ratio derived from another college's course is weak evidence
about this one. **When the catalog states its own structure, that statement outranks any convention,
including a convention drawn from courses with the same prefix and the same credit value.**

**This is now the third published-split find in four batches** — MCB1010C's "three-hour lecture,
three-hour laboratory" at batch 115, and this. **Both resolved ambiguities the conventions alone could
not.** The practical instruction: **read the catalog entry for a structure statement before reaching for a
ratio.** They are uncommon, they are easy to skim past, and they outrank everything else when present.

### ⚠ Final batch: two more C-and-title divergences, and a derived figure held honestly

- **FSS1270C** — statewide *"Introduction to Beverage Management"*, Daytona State **FSS1270 "Introduction
  to Craft Beer and Wine"**. **MUS2360C** — statewide *"Introduction to Technology in Music"*, Daytona
  State **MUS2360 "Learning Basic Music Using the Computer"**. Both handled by the standing rule: price at
  the C convention, state both figures and both titles, tell the reader **the description governs
  equivalency, not either title**. In both cases the local title is the more specific one.
- **GRA1543** is the batch's honest-gap case. It is unsuffixed, which by convention gives 45 — **but the
  title says "Studio" and it carries a $50 laboratory fee**, both of which point at the 20-hour
  convention. **The guide uses 45 and says explicitly why it might be wrong**, rather than silently picking
  the higher figure to be safe. That is the right shape for a genuine conflict between weak signals: state
  the reasoning and let the reader confirm.

### Final batch: content worth carrying

- **⚠⚠ AFROTC carries a binding service commitment** (AFR4231, AFR4232) — **commonly four years active
  duty and substantially longer for pilots and aircrew**, scholarship money extends it, and **withdrawing
  after contracting can mean repayment or enlisted service.** Also flagged: **the weekly leadership
  laboratory and physical training are additional to the credit hours**, so the real commitment is
  considerably larger than three credits suggests. **AFR4232's catalog description is a single sentence**
  — handled with the standing honest-gap treatment, content drawn from AFR4231 and labelled indicative.
  Plus the constitutional content that makes the course what it is: **the oath is to the Constitution, not
  to a person**, and **the duty to obey lawful orders is matched by a duty to refuse manifestly unlawful
  ones — "I was ordered to" is not a defence.**
- **⚠⚠ Curing salts: pink is not seasoning, and confusing it has killed people** (FSS2210C) — the dye
  exists **so nobody mistakes it for table salt**. **Weigh, never measure by volume.** And the reason the
  cure is not optional: **Clostridium botulinum thrives in the low-oxygen, low-acid conditions of cured and
  vacuum-packed products, the toxin is among the most potent known, and it produces no smell, no taste,
  and no visible spoilage.** The most serious single food-safety item in the culinary content.
- **⚠⚠ Serving a minor is a criminal offence, and Florida's vendor liability has two sharp edges**
  (FSS1270C) — **section 768.125 limits vendor liability except for serving someone underage or someone
  known to be habitually addicted**, which makes those exactly the two categories to be careful about.
  Plus the practical course note: **tasting requires being 21**, and students should confirm participation
  arrangements before registering. And **professionals spit** — swallowing makes evaluation impossible
  after a few samples and is unsafe.
- **⚠⚠ Do not scale from a drawing** (BCT1040, BCN1253C, TDR0304C) — **written dimensions govern**, because
  prints are reproduced, folded and resized. Paired with **check the revision before you build to it** —
  superseded drawings on site are a common cause of rework — and **read the general notes**, which are
  skipped almost universally and routinely override what a detail appears to show. Plus the framing that
  makes it matter: **construction documents are contract documents, and what is drawn is what is owed.**
- **⚠⚠ Tolerance is where drawings meet reality** (TDR0304C) — **tighter is not better**; tolerance drives
  cost steeply, and **a tolerance tightened without a functional reason can multiply the cost of a part for
  no benefit.** Paired with **model so it can be changed, because it will be** — an under-defined sketch
  moves when something upstream changes and **the model then produces a different part without anyone
  noticing.**
- **⚠⚠ Life studio conduct** (ART1331C) — **no photography, ever**, the model is a working colleague,
  **breaks are not negotiable**, and confidentiality applies. Rarely written down anywhere and exactly the
  kind of thing a student needs before their first session. Paired with the honest account of how drawing
  improves: **hours of observed drawing, measured rather than assumed, gesture first, and step back
  frequently.**
- **⚠⚠ Misconceptions are working theories, not gaps** (SCE3832) — the classic ones are **remarkably
  persistent**, students **pass the test and revert to the intuition**, and **many adults including
  teachers hold them too.** The instruction is to **create the experience the misconception cannot
  explain**, and the most valuable sentence a science teacher says is **"I don't know, let's find out."**
  Also the honest framing this course needs: **elementary teachers frequently arrive with science anxiety,
  children read it accurately, and repairing the teacher's own relationship with the subject is part of
  the job.**
- **⚠⚠ Florida has no personal income tax — and it does have a corporate one** (TAX3011) — **the common
  belief that Florida has "no income tax" is half wrong, and the wrong half matters to every business
  client.** Chapter 220 imposes corporate income tax; the interaction with pass-through entities makes
  entity choice carry a state consequence unlike most states. Paired with the professional line:
  **a transaction can be planned before it happens; it cannot be re-characterised afterwards**, and
  **substance-over-form doctrines exist to defeat structures that work only on paper.**
- **⚠⚠ Fonts are licensed software, not free files** (GRA1543) — installed does not mean licensed for
  commercial use or for a client, and **font licence audits are a real commercial event.** Plus
  **"found on the internet" is not a licence, and crediting the source is not either.** And the
  ownership point: **agree it in writing before starting client work**, because disputes after a project
  succeeds are the commonest disagreement in the field.
- **⚠⚠ Pattern repeat is where the money goes** (HHD1361) — a large repeat can add a substantial
  percentage to fabric required because **every panel must start at the same point in the pattern**, and
  quoting from finished dimensions under-orders every time. Plus **order dye lots together**, and the
  regulatory half: **commercial finishes must meet flame spread requirements**, and **pre-1978 buildings
  are assumed to contain lead paint until tested** with the EPA RRP rule governing disturbance.
- **⚠⚠ Segregation of duties: the owner should open the bank statement** (APA1121) — small business fraud
  is overwhelmingly by trusted long-serving employees, and **the enabling condition is one person
  controlling a transaction end to end.** The single cheapest control, and it costs nothing. Paired with
  **never force a reconciliation** — posting a balancing adjustment conceals exactly what the
  reconciliation existed to find.
- **⚠⚠ The service recovery paradox** (MNA2161) — a customer whose problem was handled well can end up
  more loyal than one who never had a problem, and **most dissatisfied customers never complain, they
  simply leave.** So the complainant is a small visible fraction of a larger invisible problem. Paired
  with the boundary: **abuse is different from anger, staff should not be expected to absorb it, and
  management that does not back them loses them.**
- **⚠ Spreadsheet structure, restated for a business audience** (APA1711) — **the root cause of endemic
  spreadsheet error is structure, not formulas**, and **hidden rows, hidden sheets and filtered-out data
  are still in the file**, which is a common and serious disclosure route. Third statement of this finding
  in the corpus (CGS1570, OST2713C, here) and the one most likely to be acted on.

---

## Closing note: what the Daytona State build produced

**1,632 guides, 100% of the buildable queue, across 118 batches.** The methodological findings are spread
through this file batch by batch; the ones that changed how the work was done are worth naming together:

- **The hour-source hierarchy**, refined repeatedly and now tested at its top: **(1) the catalog's own
  published split — which outranks conventions even when it contradicts good live anchors in the same
  prefix; (2) a live guide in the same chain or institution, preferring the anchor matching the credit
  value; (3) the prefix ratio, only after confirming uniformity.**
- **The discriminator hierarchy for split ratios: suffix → description → fee**, with the refinement that
  **a fee discriminates only when it varies meaningfully across the prefix.**
- **The 0-level trap runs in two directions.** A leading zero means PSAV clock hours in vocational
  prefixes and **developmental education carrying real institutional credit** in academic ones — and the
  reflex trained by the first is wrong for the second.
- **Prefix-block fetching surfaces what single-course work cannot** — catalog self-contradictions,
  prerequisite timing traps, and copy-pasted descriptions are only visible against the pattern of a family.
- **Four classes of catalog defect** now recorded: copy-pasted descriptions, contradictory prereq/coreq
  loops, prerequisites naming non-existent courses, and **content that was accurate when written and has
  since gone stale** — the last detectable only by knowing the domain.
- **Report discrepancies rather than resolving them.** Tier 0 settles facts; it does not authorise a guide
  to correct Tier 0.
- **`validate_drafts.py` warnings are claims to argue with, not noise** — its cross-field checks encode
  conventions this project derived, and every warning raised in the last ten batches was substantive.
- **The accreditation gate is the single most-repeated warning in the corpus** — recorded across nine
  distinct fields, always with the same shape: eligibility depends on it, non-accredited programmes
  advertise, and it is discovered after tuition is paid.

## 🔄 Queue refilled from UWF (2026-09-04)

The Daytona State queue closed at 100%. **The queue has been refilled with 897 University of West
Florida courses**, on Ron's instruction (*"Lets use UWF to refill the queue"*).

| | |
|---|---|
| UWF courses in the statewide master | **1,885** |
| Already in the queue (pushed or skipped during the DSC build) | 218 |
| New rows | 1,667 |
| &nbsp;&nbsp;— excluded: **x9xx shells** | 462 |
| &nbsp;&nbsp;— excluded: **graduate, 5xxx and above** | 308 |
| **Added to the queue** | **897** |

Both exclusions apply **the standing procedure already recorded in this file** (batch 89, step 3):
*filter out shells (9xx) and graduate levels (5xxx/6xxx)*. **No new scope decision was needed** — the
question of whether to write graduate courses was already settled.

**The shell rule was verified before use rather than assumed.** The `x9xx` pattern (second digit 9)
matches **153 rows already marked `skipped` as shells** during the DSC build — CCJ2930, ARR0905,
ASL2905, BCT2949, BCT2990, CET3906 among them — so the same rule is being applied consistently across
institutions.

**Queue now: 897 queued, 288 skipped, 1,632 pushed. Overall 64.5% of a 2,529-row decided total.**

### ✅ The UWF PDF pattern re-confirmed, and it still works

`catalog.uwf.edu/courseinformation/courses/<prefix>/<prefix>.pdf` — **the prefix must be lowercase** (see batch 122) — downloaded with `curl`, extracted
locally with `pypdf`. **Tested on ANT: one fetch, 6 pages, 68 distinct courses with full descriptions.**
The pattern recorded at batch 88 is intact under the 2026-2027 catalog.

**This makes the standing prefix-completion procedure the correct default for the whole UWF build**, and
the economics are better here than they were at Daytona State: DSC required one fetch per course from
SmartCatalog, whereas **UWF yields an entire prefix per fetch**. The 897 rows span **167 prefixes**, so
the whole queue is reachable in roughly 167 fetches rather than ~900.

Largest prefixes, and therefore the best starting points: **ANT (32), EEL (27), MLS (27), NUR (24),
ART (22), HSC (19), PCB (19), PHI (16), MVK (15), SOW (15).**

### ⚠⚠ UWF publishes no contact hours, no terms of offering, and no fees — for any course

This is a **structural difference from Daytona State and it affects every UWF guide**, so it is recorded
here once rather than repeated per batch. A UWF catalog entry carries:

- course code and title
- college and department
- **credit value as semester hours** (`3 sh`), with a repeatability note
- prerequisites, **sometimes** — 15 occurrences across 68 ANT courses
- the description

and it carries **none** of the following, confirmed by searching the full ANT extraction:
**contact hours, lecture/laboratory splits, terms of offering, corequisites, or laboratory fees** —
all returned zero matches.

> ⚠⚠ **CORRECTED AT BATCH 123 — two of these five claims are FALSE.** UWF **does** publish laboratory
> fee notices (3 ANT courses, 5 EEL courses, plus a whole catalog fees section) and **does** have a
> corequisite mechanism — in fact **two**: the `*` concurrent notation (14 in EEL, 0 in ANT) and an
> explicit `Co-requisite:` field (3 occurrences, **two of them in ANT itself**, inside the very extraction
> the batch-119 search ran over).
> The zero-match result was real *for ANT* and was wrongly generalised to the institution. The three
> remaining claims — no contact hours, no lecture/lab split, no terms — do hold in both prefixes.
> **34 live guides carrying the false sentence were corrected to v1.1.** See batch 123 below.

**The consequences for the build:**

1. **There is no tier-1 hour source at UWF at all.** At Daytona State a handful of entries published
   their own structure (MCB1010C's *"three-hour lecture, three-hour laboratory"*, ART1331C's
   *"four studio hours"*), and those outranked every convention. **No UWF guide will ever have that** —
   every contact-hour figure in this institution's guides is derived, and should be labelled as such.
2. **The conventions to use are already established and evidence-backed**, from batches 88–90:
   **3-credit lecture courses at 45 hours (15/cr)**, and **1-credit engineering and science
   laboratories at 45 hours** — the latter matching live EVR2001L and OCE1001L rather than the 30 used
   for allied-health laboratories. The recorded rule stands: **engineering and science labs run 45;
   clinical labs run 30.**
3. **No terms of offering means the single-term-offering flag cannot be raised at UWF.** That flag was
   one of the most advising-critical findings of the DSC build — offering frequency below once a year,
   prerequisite chains with no slack. **It is simply unavailable here**, and guides should say the
   catalog does not publish it rather than being silent.
4. **Variable-credit courses appear and need handling.** ANT alone carries `1-12 sh`, `1-9 sh`,
   `1-3 sh` and `0-3 sh` entries. The guide schema takes a single integer, so **these need an explicit
   note stating the published range** rather than a silently chosen value.

### ⚠ 218 UWF courses were already written from Daytona State's catalog

190 pushed and 28 skipped. Those guides carry **DSC's credit values, hours, prerequisites and terms** —
which for a shared SCNS number may differ from UWF's, and this file already records exactly that kind
of divergence (the **EML3015/EML3016 subject collision** between UWF and FSU, found at batch 88).

**No action is proposed now**, and it is not a correction candidate: the guides are accurate to the
institution they were written from, and each states its source. **But when a UWF prefix extraction is in
hand, the already-published members of that prefix are free to check** — the whole point of the
prefix-completion procedure is that the entire family is visible at once. **Any real divergence found
that way goes to `REVIEW_QUEUE.md` as a v1.1 candidate**, which is how every one of the 30+ live
corrections during the DSC build was found.

### Batch 119 — **the first UWF batch**: ANT archaeology core (12)

Twelve guides pushed, all v1.0, all clean, all live. **Written from a single PDF extraction — zero
additional fetches.** Seven were queued rows; **five were bonus courses** picked up by `reconcile` as
orphan drafts (ANT2100, ANT3137, ANT4115, ANT4144, ANT4182C), so the denominator moved 2,529 → 2,534.

| Course | sh | hrs | Basis |
|---|---|---|---|
| ANT2100 Introduction to Archaeology | 3 | 45 | lecture 15/cr (live ANT2000 3/45); gen ed social science |
| ANT3101 Principles of Archaeology | 3 | 45 | ⚠ gates five upper-division courses |
| ANT3137 Shipwreck Archaeology | 3 | 45 | Pensacola maritime emphasis |
| ANT3141 Origins of Civilization | 3 | 45 | |
| ANT3153 North American Archaeology | 3 | 45 | open to all majors |
| ANT3158 Florida Archaeology | 3 | 45 | field trips included |
| ANT4115 Method and Theory | 3 | 45 | prereq ANT3101; permission required |
| ANT4144 Precolumbian Archaeology | 3 | 45 | ⚠ taught concurrently with graduate ANG5134 |
| ANT4172 Historical Archaeology | 3 | 45 | prereq ANT3101; permission required |
| ANT4180L Laboratory Methods | 3 | **60** | ⚠⚠ least certain figure in the batch |
| ANT4190 Historic Preservation | 3 | 45 | prereq ANT3101 |
| ANT4182C Conservation of Archaeological Materials | 4 | **80** | C form 20/cr |

### ✅ The UWF economics are as good as predicted — and better than Daytona State's

**One `curl` and one `pypdf` extraction produced the entire ANT prefix: 62 parsed entries, 57 of them
non-shell undergraduate.** Twelve guides were written from it with **no further web access of any kind**,
and the remaining 45 are already in hand for subsequent batches.

**The contrast with the DSC build is stark.** Daytona State's SmartCatalog required **one fetch per
course**; UWF gives a whole prefix per fetch. A twelve-guide DSC batch cost 12 fetches; this one cost
**one**. Ron's standing prefix-completion procedure is therefore not merely permitted at UWF — **it is
the only sensible way to work here**, and the 897-row queue across 167 prefixes should be reachable in
roughly 167 fetches.

**The parsing is worth recording as reusable.** The extraction splits on the course-code boundary
(`\\n(?=ANT \\d{4}[A-Z]?\\s)`), then pulls title, `N sh` credit value, `Prerequisite:` line, department,
and description per entry. **UWF's format is consistent enough that the same parser should work on any
prefix** — worth trying unchanged on the next one rather than rewriting.

### ⚠⚠ Batch 119: the UWF hour problem is now concrete, and one figure is genuinely uncertain

The standing note recorded at the queue refill — **UWF publishes no contact hours for any course** — is
carried in every guide as a labelled derivation. Most of this batch is unproblematic: 3 sh lecture
courses take the 15/cr convention, **corroborated inside the prefix by the already-live ANT2000 at 3
credits and 45 hours**, and the C-suffixed ANT4182C takes 20/cr for 80.

**⚠⚠ ANT4180L is the exception and it is flagged as such in the guide.** It is a 3 sh laboratory course,
and **the repository has no single laboratory ratio to apply**:

| Live anchor | Ratio |
|---|---|
| EVR2001L, OCE1001L (1 cr / 45 hrs) | **45 per credit** |
| CHM2045L (1 cr / 30 hrs) | **30 per credit** |

**The two disagree, which means the batch-89 rule — "engineering and science labs run 45; clinical labs
run 30" — is not as clean as recorded.** CHM2045L is a science laboratory at 30. The guide uses the
combined-course convention of 20/cr (60 hours), states all of this explicitly, and tells the reader the
figure is the least certain in the batch and that a hands-on collections course could reasonably meet for
more.

**Worth naming: where the corpus's own anchors conflict, say so in the guide rather than picking one
silently.** That is the same shape as the GRA1543 treatment last batch, and it is the honest handling of
a genuine conflict between weak signals.

### ⚠ Batch 119: two catalog constructions worth recording for the rest of the UWF build

- **A course taught concurrently with its graduate counterpart.** ANT4144 is *"offered concurrently with
  ANG5134"* with additional requirements for graduate students. **This is a new construction for the
  corpus** and it has two practical consequences a student needs: the level is pitched to accommodate
  graduate students, which makes it more demanding than a typical elective, and **the assessment differs
  by level**, so undergraduates should confirm what is expected. **Expect more of these at UWF** — it is a
  standard university device and the DSC build never encountered it.
- **"Permission is required" appears frequently** (ANT4115, ANT4172, ANT4824). At UWF this seems to be a
  routine gate on upper-division archaeology rather than an exception, so it is stated in the
  prerequisites field rather than flagged as unusual.

### Batch 119: content worth carrying

- **⚠⚠ Excavation is destruction** — the discipline's founding constraint, and the block every archaeology
  guide in this prefix carries. **A site can be excavated once**; removing an artefact destroys its
  context permanently, **which is why recording is the actual work and why modern practice presumes
  preservation in place.** Paired with: **excavation without a curation plan is destruction with extra
  steps**, and **unpublished excavation is a recognised failure** — a great deal of twentieth-century
  fieldwork sits unreported in boxes.
- **⚠⚠ Recovery method determines what exists, and the bias is invisible afterwards** (ANT3101) —
  **quarter-inch screen loses small fauna and fish bone**, so a site excavated through coarse screen can
  produce a subsistence reconstruction **with the fish missing entirely**, and the report will not say so.
  **Read older reports knowing their negative findings frequently reflect recovery rather than the past.**
- **⚠⚠ Middle range theory is the bridge every archaeological argument needs and few state** (ANT4115) —
  archaeology observes a static present and wants a dynamic past, and **the connection is an argument
  rather than an observation.** The failure mode is **circularity**: using the same assumptions to
  interpret the record that you set out to test against it. The operational test: **what would this
  deposit look like if the claim were false?**
- **⚠⚠ The curation crisis is the discipline's quiet failure** — repositories are full, collections sit
  uncatalogued and inaccessible, and **some institutions will no longer accept new material.** Curation
  must be funded and a repository must have agreed to accept a collection **before excavation begins.**
  Paired with the constructive half: **existing collections are an underused research resource that costs
  no new destruction.**
- **⚠⚠ Provenience is lost in the laboratory, not the field** (ANT4180L) — bags emptied together, a tag
  left in the water, two contexts on one table. **Every one is an ordinary mistake that permanently
  destroys information a field crew spent weeks producing.** And the specific one students get wrong:
  **do not wash everything reflexively** — residues, charred remains, and corroded metal must not be
  washed, because washing removes exactly the evidence a specialist would have used.
- **⚠⚠ Eligibility is the decision that matters, and Criterion D is where archaeology lives** (ANT4190) —
  **an ineligible site gets no protection at all**, and archaeological eligibility rests on *research
  potential*, so **a site must be argued to be informative to be protected.** "May contain information"
  is not an eligibility argument. Plus the honest framing: **data recovery is mitigation, not
  preservation** — the site is destroyed with a record made.
- **⚠⚠ The structural tension of compliance archaeology, named** (ANT4190) — the archaeologist is paid by
  the party whose project the archaeology may constrain. **Professional judgement is not the client's to
  direct, and pressure to find a site ineligible is a compliance concern rather than a negotiation.**
- **⚠⚠ The document and the deposit disagree — that is the finding** (ANT4172) — **the archaeological
  record includes people the documents omit**, and in some cases is the only evidence they were there.
  **Documents record intentions; deposits record practice**, and the gap is routinely large. Plus the
  circularity trap: **date the deposit independently before correlating it with a documented event.**
- **⚠⚠ Florida's preservation is wildly uneven, and it shapes every conclusion** (ANT3158) — acidic sandy
  uplands destroy bone, **wet sites preserve eight-thousand-year-old textile and brain tissue**, and shell
  middens buffer acidity so **bone survives inside a midden and not outside one**. So apparent regional
  differences frequently reflect preservation rather than behaviour. And **a great deal of Florida's early
  archaeology is now offshore**, because the coastline people lived on has moved.
- **⚠⚠ Florida section 872.05 makes it a felony to knowingly disturb an unmarked human burial** — carried
  in every guide in this batch. Unmarked burials are common on Florida sites, and **if human remains are
  encountered, work stops.** Alongside Chapter 267's vesting of archaeological resources on state land and
  state submerged land in the state.
- **⚠⚠ Treasure hunting is not archaeology** (ANT3137) — **selling the assemblage destroys the collection's
  research value**, and the economics drive the destruction because salvage is funded by expectation of
  sale. **Florida owns resources on its submerged land**, and sunken military craft remain flag-state
  property regardless of age. Paired with the physical reason conservation binds: **waterlogged wood is
  held together by water, and a timber allowed to dry uncontrolled can be lost in a week on a dock after
  surviving four centuries.**
- **⚠⚠ These are descendant communities, not extinct peoples** (ANT3153) — **writing about Indigenous
  peoples only in the past tense implies a disappearance that did not happen**, and it is among the
  commonest failures in student writing on the subject. **NAGPRA is a legal correction to a real history**,
  not an administrative inconvenience.
- **⚠⚠ Pseudo-archaeology is worth refuting because much of it is not harmless** (ANT2100) — claims that
  Indigenous peoples could not have built their own monuments **have a documented history of being used to
  justify dispossession**, and the argument's structure is the same one that was used to that end. The
  diagnostic: **pseudo-archaeological claims assert conventional explanations are inadequate without
  offering a testable alternative.**
- **⚠ Six independent cases make the origins of complexity a natural experiment** (ANT3141) — **a feature
  present in every case may be necessary; one present in some cannot be**, and the Andean state without a
  conventional writing system rules writing out as a precondition. Plus the chronology point: **large-scale
  irrigation was long held to produce centralised authority, and the sequences show centralisation coming
  first** — which reverses the argument and is why dating matters so much.
- **⚠⚠ Reversibility and minimum intervention** (ANT4182C) — **every intervention removes information**,
  and the impulse to make an object look better is the enemy of the evidence it carries. **Cleaning is
  irreversible**, and surface deposits may be corrosion products recording the original form, analysable
  residues, or gilding. Plus laboratory safety: **solvent exposure is cumulative and the effects are
  chronic, so nothing warns you at the time**, and **the wrong glove is worse than none** because it holds
  solvent against skin.

### Batch 120: UWF ANT field methods, maritime and analysis (8)

Eight guides pushed, all v1.0, all clean, all live. **Same PDF extraction as batch 119 — zero fetches
again.** One was a queued row; **seven were bonus courses** added by `reconcile` as orphan drafts, moving
the denominator 2,534 → 2,541.

| Course | sh | hrs | Basis |
|---|---|---|---|
| ANT4820 Archaeological Field Survey | 3 | 45 | lecture 15/cr; concurrent with graduate ANG5080 |
| ANT4824 Terrestrial Field Methods | **1–9** → 6 | **240** | ⚠⚠ variable credit; representative 6-week case |
| ANT4835 Maritime Field Methods | **1–9** → 6 | **240** | ⚠⚠ same; ⚠ **mutual exclusion with ANT4135** |
| ANT4121 Combined Field Methods | **1–9** → 9 | **480** | ⚠⚠ **catalog states "6 weeks each"** |
| ANT4836 Scientific and Research Diving | 3 | 45 | based on the NOAA Diving Manual |
| ANT4418 Maritime Cultures | 3 | 45 | cultural, not field |
| ANT4191C Anthropological Data Analysis | 3 | 60 | C form 20/cr |
| ANT4853C GIS in Anthropology | 3 | 60 | C form 20/cr; concurrent with ANG5181 |

### ⚠⚠ Batch 120: the first variable-credit courses in the corpus, and how they were handled

**Three of these publish "1–9 sh" rather than a credit value.** The guide schema takes a single integer,
so the handling matters and is now standardised as a reusable block:

1. **State the published range prominently and first**, before any figure.
2. **Label the shown values as a representative case, not the course's value** — the credit is agreed with
   the department, not fixed by the catalog.
3. **Say that contact hours scale with the credit taken**, so a student registering for fewer can scale
   the figure down.
4. **Make the practical fact the headline: a field school is a full-time commitment whatever the credit
   says.** You cannot hold a normal job during a field season, and the credit value badly understates the
   time. That is the thing a student actually needs.
5. **Tell them to ask for the total cost, not the tuition** — a Material and Supply Fee is assessed and
   travel, accommodation, and equipment sit on top.

### ✅ Batch 120: UWF's only duration statement, found and used

**ANT4121's description contains "(6 weeks each)"** — maritime and terrestrial. **This is the only
statement approaching a contact-hour figure found anywhere in the UWF catalog so far**, which publishes
none for any course.

It was used directly rather than through a convention: **twelve weeks of full-time fieldwork at roughly
40 hours a week gives approximately 480 contact hours**, taken at the published 9 sh maximum. **That makes
ANT4121 the largest single course in this repository by contact time**, and unusually for UWF the figure
derives from the catalog's own words.

**Worth naming as a search habit for the rest of the UWF build: read descriptions for duration language.**
UWF publishes no hours field, but phrases like *"6 weeks each"* occasionally appear in prose — and where
they do they outrank the conventions, exactly as a published split would.

### ⚠⚠ Batch 120: a mutual-exclusion rule — new construction for the corpus

**ANT4835's entry states: "Credit may not be earned in both ANT 4135 and ANT 4835."**

The corpus has recorded plenty of prerequisite, corequisite, and prerequisite-*or*-corequisite
constructions, but **not previously a rule that taking one course forecloses credit for another.** It
matters at graduation audit rather than at registration, which is exactly when it is discovered too late.
Flagged in the guide with an instruction to confirm with an advisor which number the programme expects.

**Watch for more of these at UWF** — overlapping numbers with an exclusion rule are a normal university
device for courses that have been renumbered or that duplicate content, and the DSC build never met one.

### ⚠ Batch 120: "offered concurrently with" is now confirmed as routine at UWF

Three of eight courses in this batch carry it — **ANT4820/ANG5080, ANT4836/ANG5836, ANT4853C/ANG5181** —
after ANT4144/ANG5134 in batch 119. **Four instances in twenty courses makes it a standing feature of this
catalog rather than an oddity**, and each guide states the two consequences a student needs: the level is
pitched to accommodate graduate students, and the assessment differs by level.

### Batch 120: content worth carrying

- **⚠⚠ Scientific diving is not recreational diving, and the distinction is legal.** A recreational
  certification does not qualify you to dive scientifically; **US scientific diving operates under AAUS
  standards with a Diving Control Board and a Diving Safety Officer**, which is what allows it to sit
  outside the commercial diving regulations. **You dive under the programme's authorisation, to its
  limits.** Carried in all three diving-dependent guides.
- **⚠⚠ Never hold your breath on ascent** — expanding gas ruptures lung tissue and can drive gas into the
  arterial circulation. **Arterial gas embolism can be fatal within minutes and can occur from only a few
  metres.** The fastest-acting diving injury and entirely preventable.
- **⚠⚠ Suspect decompression illness in any diver who becomes unwell after a dive** (ANT4836) — symptoms
  are vague (fatigue, joint pain, confusion, tingling) and **divers routinely explain them away, which is
  exactly how treatment gets delayed.** Emergency oxygen is the most effective field intervention and is
  frequently late. **Know the nearest operating chamber before the dive, as part of the plan.** And
  **do not recompress in the water.**
- **⚠⚠ Anyone may call a dive, at any time, for any reason, without explanation** — and a programme that
  does not honour that is not one to dive with.
- **⚠⚠ Survey finds what its method was capable of finding** (ANT4820) — a negative result is a statement
  about the method, not the ground, and **a site smaller than the survey interval can sit entirely between
  the tests.** So the report must state transect spacing, shovel test interval and depth, screen size, and
  visibility — **without them a reader cannot distinguish absence of evidence from evidence of absence.**
  Plus: **a magnetic or sonar anomaly is a target, not a site.**
- **⚠⚠ Ground visibility drives surface survey entirely**, and Florida's vegetation makes surface survey
  unproductive across much of the state — **which is why shovel testing dominates here.** A genuinely
  Florida-specific methodological point.
- **⚠⚠ Site locations are confidential** (ANT4820, ANT4853C) — precise coordinates are withheld from public
  documents because **publishing them invites looting.** Extended in the GIS guide: **a screenshot with a
  basemap can be georeferenced by anyone**, and **photographs embed coordinates by default** and must be
  stripped before sharing.
- **⚠⚠ Predictive models reproduce the biases of the data that trained them** (ANT4853C) — a model built on
  known sites predicts where sites *like the known ones* are, and **known sites are where people happened
  to survey.** So the model can systematically miss whole classes of site while looking authoritative, and
  **treating a low-probability zone as empty is how sites get destroyed.**
- **⚠⚠ Data in the wrong coordinate system still draws a map** (ANT4853C) — it is simply in the wrong place
  or measures the wrong distance, **and nothing warns you.** Paired with the datum point: **a mismatch can
  displace features by a hundred metres**, enough to put a site outside a project boundary it is actually
  inside.
- **⚠⚠ The field school is what makes you employable — treat it as the interview it is** (ANT4824) — it is
  the standard entry requirement and the first thing a CRM employer looks for. **Directors are asked for
  references constantly, and the students who get recommended are the reliable ones, not the fastest
  excavators.** And: **a good excavator with poor records has destroyed a deposit.**
- **⚠⚠ Twelve weeks is most of a summer** (ANT4121) — **you cannot hold a job during it**, which for many
  students is the binding constraint and needs planning a year ahead. **Satisfy the diving requirement well
  in advance, because medical clearance can disqualify** — find out before committing money.
- **⚠ Underwater excavation is terrestrial excavation with every constraint made worse** (ANT4835) — same
  recording standards, but limited bottom time, restricted visibility, and **no ability to step back and
  look at the trench.** Hence: **the thinking is done on the surface**, grids and baselines substitute for
  the overview, and **improvising underwater is how dives go wrong** — task loading is the mechanism behind
  most scientific diving incidents.
- **⚠⚠ Keep recovered material wet from the moment it leaves the seabed** — waterlogged wood, leather and
  organics **begin to be destroyed as soon as they start to dry**, and an object that survived centuries
  can be lost in a day.
- **⚠⚠ Local ecological knowledge is data, and dismissing it is a documented failure** (ANT4418) —
  fisheries management has repeatedly missed changes the fleet had observed for years. **It is not
  automatically correct either**, and the anthropological job is to document it accurately rather than to
  adjudicate it. Plus: **common property is not open access** — many fisheries have real local institutions
  with rules and sanctions, **and a great deal of policy has failed by assuming they did not exist.**
- **⚠ Anonymising in a small port takes more than removing a name** (ANT4418) — **a boat, a role, and a
  fishery can identify someone completely**, and people can be harmed by what they said about regulators
  or neighbours. Paired with the standing IRB point: **approval is obtained before the research starts, and
  data collected without it usually cannot be used.**
- **⚠⚠ Selective alteration of a research image is falsification** (ANT4191C) — adjusting brightness across
  a whole image is normal; adding or removing content is not, **and it has ended careers in other
  disciplines.** Keep the original and record what changed. Plus **a published archaeological photograph or
  plan without a scale is not evidence.**
- **⚠ ANT4191C and ANT4853C are the most transferable courses in the prefix**, and both guides say so
  explicitly — **"built and queried a relational database, produced GIS analysis" reads to an employer very
  differently from "anthropology degree"**, and GIS keeps a graduate employed while the archaeology market
  is tight.

### Batch 121: UWF ANT biological anthropology and forensic cluster (13)

Thirteen guides pushed, all v1.0, **twelve clean and one clean-with-warnings** (argued, not ignored — see
below). **Same PDF extraction as batches 119 and 120: zero fetches for a third consecutive batch.** Five
were queued rows; **eight were bonus courses**, moving the denominator 2,541 → 2,549.

| Course | sh | hrs | Basis |
|---|---|---|---|
| ANT2511 Biological Anthropology | 3 | 45 | ⚠ gen ed **Natural Sciences** |
| ANT2511L Biological Anthropology Lab | 1 | 45 | ⚠ one-line description; derived |
| ANT4586 Human Origins | 3 | 45 | prereq ANT2511/L |
| ANT4550 Primatology | 3 | 45 | |
| ANT4516 Modern Human Physical Variation | 3 | 45 | |
| ANT4525 Human Osteology | 4 | 80 | ⚠⚠ two catalog rules attached |
| ANT4525L Human Osteology Lab | **0** | — | ⚠⚠ zero-credit **corequisite** lab |
| ANT4526C Advanced Methods | 3 | 60 | ⚠⚠ **grade-conditional prerequisite** |
| ANT3520 Forensic Anthropology | 3 | 45 | ⚠ scope clarification needed |
| ANT4523 Field Methods in Forensic Anthropology | **0–3** → 3 | **120** | ⚠ validator warning, argued |
| ANT4536 Bioarchaeology | 3 | 45 | |
| ANT4184 Mortuary Anthropology | 3 | 45 | |
| ANT4025 Ritual Use of Human Remains | 3 | 45 | catalog publishes the assessment structure |

### ⚠⚠ Batch 121: a grade-conditional prerequisite — new construction, and it changes an earlier course retrospectively

**ANT4526C states: "undergraduate enrollment is limited to students who have already earned an A- or
better in Human Osteology."**

The corpus has recorded prerequisites, corequisites, prerequisite-*or*-corequisite, and mutual exclusions.
**This is the first prerequisite conditioned on a grade**, and it is the most consequential of them for a
student because **it changes the stakes of an earlier course after the fact.** Someone who takes ANT4525
casually and earns a B+ has closed this door and will discover it at registration.

**It is stated at the top of both guides — ANT4526C's and ANT4525's — rather than only where it appears in
the catalog.** That is the point: the warning is useless in the course it gates and valuable in the course
it depends on. **Generalisable: a condition attached to course B that constrains behaviour in course A
belongs in the guide for A.**

**ANT4525 also carries a second mutual-exclusion rule** (with ANT4466), confirming that construction as
routine at UWF after ANT4835/ANT4135 last batch.

### ⚠⚠ Batch 121: a zero-credit *corequisite* laboratory — a distinct variant

**ANT4525L is published at 0 sh as a required corequisite of ANT4525 (4 sh).** This repository already
records zero-credit courses at credit-level numbers — the Daytona State SLS orientation courses — and
**this is a different and cleaner thing:**

| | **DSC SLS courses** | **ANT4525L** |
|---|---|---|
| What the zero means | the course carries no credit at all | **the credit lives on its paired lecture** |
| Contact time | not published, genuinely unknown | **carried by ANT4525's 4 sh** |
| Financial aid | ⚠ does not count toward enrolment status | harmless — the pair carries 4 credits |
| Why it exists | a programme requirement with no credential | **registers the lab half of one package** |

**Both are `credits: 0` with no hour figure, and conflating them would misdescribe both.** ANT4525L's
guide states that the zero is credit accounting rather than workload — **the lab is where osteology is
actually learned and will occupy several hours a week** — and that the two must be registered together.

### ⚠ Batch 121: the validator flagged ANT4523, and the flag was argued rather than dismissed

`validate_drafts.py` warned: *"3 credits with 120 contact hours (expected ~45, or ~60 for a C course)."*

**The heuristic is right about classroom courses and does not know about field courses**, which UWF has
introduced to the corpus. ANT4523 is on-site forensic field recovery training, and 120 is proportional to
the field rate used for ANT4824 (6 sh / 240) and ANT4121 (9 sh / 480) in the previous batch — those did
not trip the rule only because their credit values fall outside its 3-credit clause.

**But the challenge was worth taking seriously, and it improved the guide.** On re-reading, the catalog
does not actually say whether this runs as a concentrated field school or as a semester course with field
days — **and the two readings give 120 and 45, which is a large difference.** The guide was amended to
state both readings explicitly, say which the catalog's wording points to, and tell the reader to ask
before planning a term around it. It was then pushed with the warning standing.

**Recorded for the tooling: `validate_drafts.py`'s credit-to-hour heuristics assume classroom or
laboratory courses.** Field courses are a legitimate third category and will trip them. **That is not a
reason to change the validator** — the warning did its job by forcing a re-examination that found a real
ambiguity — but it is worth knowing that the UWF build will generate more of these.

### ⚠ Batch 121: one prefix, two general education areas

**ANT2511 meets a Natural Sciences requirement; ANT2100 (batch 119) meets a Social Sciences requirement.**
Both are ANT. That is a real feature of anthropology as a four-field discipline, and **it means a student
cannot infer the general education area from the prefix** — flagged in both guides with an instruction to
confirm with an advisor.

### Batch 121: content worth carrying

- **⚠⚠ Working with human remains — the block carried by every guide in this batch.** *These were people.*
  **The discipline's history here is genuinely bad**: remains were collected from battlefields, graves,
  hospitals and colonised populations without consent, frequently to support claims about racial
  hierarchy, and **many teaching collections still contain individuals acquired that way** — so knowing the
  provenance of the collection you learn on is part of the training. Plus the absolute rule: **no personal
  photography, nothing on social media, ever.**
- **⚠⚠ Race, ancestry, and human variation — stated carefully rather than glibly.** The empirical findings
  are not disputed (most variation is *within* populations; variation is largely clinal; traits vary
  independently), **and racial categories are social, historically contingent, and demonstrably unstable**
  — they have changed within living memory in law and census. **Social does not mean unreal**: race has
  large measurable effects operating through discrimination and access rather than biology. And the honest
  part: **there is a live tension the guides do not paper over** — forensic anthropologists estimate
  ancestry because it narrows a missing-persons search, while the field actively debates whether the
  practice is defensible. **Both the utility and the critique are serious.**
- **⚠⚠ The specific history, because "misuse" is too vague** (ANT4516) — craniometry produced the expected
  answer because **the categories were assumed before the measuring began**, which is a lesson about
  expectation shaping measurement rather than about calipers. **Eugenics was policy**: immigration
  restriction, anti-miscegenation law, and forced sterilisation programmes that ran in the United States
  for decades. **Anthropology was substantially involved on both sides**, which is why the field treats
  this as current rather than past.
- **⚠⚠ The forensic anthropologist does not determine cause or manner of death** (ANT3520) — that is the
  medical examiner's determination. **UWF's own course description says "manner and cause of death"**, so
  the guide adds an explicit scope clarification and tells the student to confirm how the course frames it.
  **Stating a conclusion outside scope on a stand is a serious professional error.**
- **⚠⚠ "Perimortem" does not mean "at the moment of death"** (ANT3520) — it means the bone was fresh when
  it broke, and **bone stays fresh in that sense for a considerable period after death.** So a perimortem
  fracture is not evidence the injury caused death or even occurred while the person was alive. Paired
  with: **excavation damage is a common and embarrassing source of apparent perimortem trauma.**
- **⚠⚠ The osteological paradox** (ANT4536, ANT4526C) — **a skeletal sample consists of people who died**,
  not a sample of the living. **Lesions require survival to form**, so someone who died quickly shows
  nothing while someone who survived for years shows extensive lesions — **which means a population with
  more lesions may have been healthier, not sicker.** The intuitive reading is exactly backwards, and it is
  standard published theory rather than a quibble.
- **⚠⚠ Do not sex a skeleton from its grave goods** (ANT4184, ANT4536) — assigning gender from associated
  objects and then using it as skeletal sex is **circular, and it has produced documented errors that stood
  in the literature for decades.**
- **⚠⚠ Methods are built on reference samples and applied far outside them** (ANT4526C) — ask what a method
  was validated on, because **a stature formula built on one population applied to another produces a
  confidently wrong number and the output looks identical either way.** Plus: **some foundational reference
  collections were assembled unethically**, and that bears on the methods built from them.
- **⚠⚠ Behavioural reconstruction rests on analogy, and the analogy must be argued** (ANT4586) — **living
  primates are not ancestral to humans**, and **living foraging peoples are modern humans with full
  histories**, so treating them as living fossils is both bad method and an old damaging error. And the
  standing caution: **the history of this field includes confident reconstructions that closely resembled
  the expectations of the era producing them, and were revised when those expectations changed rather than
  when the fossils did.**
- **⚠⚠ Behavioural sampling method determines what you observe** (ANT4550) — **ad libitum observation
  systematically over-samples the dramatic**, biasing every rate calculated. Plus the conservation point
  with real force: **humans and great apes share pathogens, and researchers and tourists have introduced
  human respiratory infections to wild ape populations with fatal outbreaks.**
- **⚠⚠ A bad recovery cannot be repaired by good analysis** (ANT4523) — **damage caused during recovery
  mimics perimortem trauma**, which is how a recovery error becomes a wrong conclusion in a criminal case.
  **Document any damage you cause, immediately.** And the audience point the catalog names: **most
  buried-remains recoveries are conducted by police, not anthropologists**, so teaching archaeological
  method to them may be the most valuable thing this course does.
- **⚠⚠ Cognitive bias is a documented problem in forensic science** — analysts told what the investigation
  expects reach different conclusions, **and the effect does not require dishonesty.** So: **ask for context
  you need and refuse context you do not** — knowing the suspect's account before analysing trauma is
  contamination.
- **⚠ Extraordinary claims need proportionate evidence, and cannibalism is the test case** (ANT4025) —
  claims of this kind **have a long history of being made about other peoples on thin evidence and used to
  justify conquest**, which is a reason for rigour rather than avoidance. **Every diagnostic indicator has
  alternative explanations**, and distinguishing them is the technical skill. Plus: **apply the same
  standard to claims you find unsurprising** — motivated reasoning runs both ways.
- **⚠ Historic African American cemeteries are a live issue in Florida** (ANT4184) — burial grounds built
  over, forgotten, and rediscovered, carrying a particular obligation to descendant communities and to
  honest public accounting.
- **⚠⚠ An honest career note on forensic anthropology**, carried in every guide in the cluster: it is the
  most popular specialism because of television, and **there are very few full-time positions.** Most
  practitioners are **academics who consult**, and board certification requires a doctorate plus documented
  casework. **Plan for bioarchaeology, CRM, museum, and medicolegal work — and treat forensic practice as
  something you may add rather than a job to apply for.**

### Batch 122 — **the ANT prefix closes at UWF**: cultural, regional and applied anthropology (13)

`ANT3212`, `ANT3610`, `ANT4034`, `ANT3241`, `ANT2301`, `ANT3312`, `ANT4006`, `ANT4302`, `ANT4403`,
`ANT4532`, `ANT3311`, `ANT3352`, `ANT4473`. All 13 published, all **3 sh / 45 derived hours**.
**ANT is the first UWF prefix to close** (batches 119–122, 46 guides).

### ⚠⚠ The recorded UWF PDF URL was wrong in case — **the prefix must be lowercase**

`SOURCES.md` carried `catalog.uwf.edu/courseinformation/courses/<prefix>/<prefix>.pdf` with `<prefix>`
implicitly uppercase, and the batch-119 note said "tested on ANT". **The uppercase form now returns a
hard 404**, with an HTML error body rather than a redirect, and a user-agent header does not change it:

```
.../courses/ANT/ANT.pdf  → 404, 196 bytes, text/html
.../courses/ant/ant.pdf  → 200,  93 KB,  application/pdf   ✅
```

**Three lines in this file have been corrected.** The failure mode is worth naming because it is silent
in the worst way: `curl` exits 0, writes a 196-byte file, and `pypdf` then fails on a file that looks
like it downloaded fine. **Check the byte count, not the exit code.** Whether the uppercase form ever
worked or the batch-119 note recorded the canonical spelling rather than the tested one cannot now be
determined; either way the lowercase form is the one that works and is what the pattern now says.

### ⚠⚠ Six queued ANT rows have **no UWF coverage** — the C-suffix family against the split family

The queue's remaining ANT rows were not all writable. **UWF runs the split lecture-plus-lab family where
the queue carries the integrated `C` variant**, and the two are different SCNS numbers:

| Queued row | Inst | UWF publishes instead | Disposition of the UWF variant |
|---|---|---|---|
| `ANT2511C` | **15** | `ANT2511` + `ANT2511L` | — |
| `ANT2100C` | **11** | `ANT2100` | ✅ pushed batch 119 |
| `ANT4525C` | 6 | `ANT4525` + `ANT4525L` | ✅ both pushed batch 121 |
| `ANT4586C` | 5 | `ANT4586` | ✅ pushed batch 121 |
| `ANT3520C` | 4 | `ANT3520` | — |
| `ANT4115C` | 3 | `ANT4115` | — |

This is the **parallel numbering family** pattern (rule 19) appearing at the institution level rather
than within one catalog: the same content is carried at other Florida institutions under an integrated
`C` number and at UWF under a lecture/lab pair. **`ANT2511C` at 15 institutions is the highest-demand
unwritten row in the prefix**, which is why the disposition is a decision rather than a routine skip —
logged as **REVIEW_QUEUE item 9**.

**Generalisable point for the rest of the UWF build:** a prefix "closing" means every *writable* row is
done, not every queued row. **Expect a residue of C-suffix rows in any prefix where UWF splits lecture
from lab** — the science and health prefixes (PCB, MLS, EEL) are the ones to watch.

### ⚠⚠ Thirteen consecutive courses with **no published prerequisite** — and what that does and does not mean

**Not one of the 13 carries a prerequisite**, including seven 4000-level courses. Combined with batches
119–121, the ANT prefix's prerequisite density is **15 occurrences across 68 courses**.

**The temptation is to read this as UWF genuinely having open upper-division anthropology, and that
reading is not safe.** UWF publishes prerequisites *sometimes* — this file recorded that at batch 119 —
so absence in the catalog is weak evidence about the registration system. What can be stated honestly is
what the guides now say: **the catalog publishes no prerequisite**, with the natural preparation named
separately as advice rather than as a requirement. **Every guide in this batch draws that line
explicitly**, which is the same construction used for the derived hours.

**One real consequence for advising:** ANT4034 (History of Anthropology) is a synthesis capstone that
assumes prior ethnographic reading, and **nothing in the catalog stops a student taking it first**. The
guide says so directly rather than leaving the 4000-level number to carry the signal alone.

### ⚠⚠ Two more mutual-exclusion rules, and the construction is now confirmed as systematic at UWF

Batch 120 named mutual exclusion as new construction for the corpus; batch 121 saw it again. **This batch
adds three more, all stated inside the course description rather than in a prerequisite field:**

| Course | Excluded against | Wording |
|---|---|---|
| `ANT3610` | `ANT3620` | "Credit may not be received in both ANT 3610 and ANT 3620." |
| `ANT3311` | `ANT3317` | "Credit may not be received in both ANT 3311 and ANT 3317." |
| `ANT4532` | `ANT4408` | "Credit may not be received in both ANT 4532 and ANT 4408." |

**Five occurrences across the ANT prefix now.** The construction is a UWF house style and it is
**advising-critical in a way a prerequisite is not**: a prerequisite blocks registration at the point of
enrolment, while an exclusion rule **surfaces at degree audit**, which can be years later. **Transfer
students are the exposed population** — an incoming course articulated to the excluded number blocks the
one being taken, and the differing titles hide it.

**Standing instruction for the rest of the UWF build: grep each prefix extraction for "may not be
received" and surface every hit in the affected guides.** It is one regex per prefix and it catches an
error class the student otherwise discovers too late to fix cheaply.

### ⚠ A general-education designation published inside a course description — `ANT4403`

**"Meets College-Level Communication Skills Requirement"** appears in ANT4403's description. This is the
**first general-education/writing designation found in the UWF corpus**, and it matters for two reasons:

1. **It changes the workload.** A communication-designated course carries a real writing component, and
   requirements of this kind commonly attach a minimum grade (typically C) for the requirement to be
   satisfied — **passing the course and satisfying the requirement are not the same event**.
2. **&#9888; The designation is the part least likely to transfer.** Course content articulates through
   SCNS; a *local writing designation* generally does not. A student who takes this at UWF and transfers
   may find the credit accepted and the writing requirement still outstanding.

**The guide states both points and directs the student to confirm the minimum grade with an advisor**,
since UWF does not publish it in the course entry. Batch 121 noted "one prefix, two general education
areas"; this is the same publishing habit surfacing in a different field, and **general-education signals
at UWF are scattered across the description text rather than held in a structured field**.

### ⚠ SCNS-vs-local title drift on **four of thirteen** — the highest rate in the corpus so far

| Course | SCNS / queue title | UWF local title |
|---|---|---|
| `ANT3212` | Peoples of the World | **Peoples and Cultures of the World** |
| `ANT4006` | Human Rights and Culture | **Anthropology of Human Rights** |
| `ANT4302` | Gender and Culture | **Global Gender Issues** |
| `ANT4473` | Culture and Globalization | **Anthropology of Globalization** |
| `ANT3311` | Indians of the Southeastern United States | **Indians of the Southeast: An Anthropological Perspective** |

Five if `ANT3311` is counted, and it should be. **This is title drift (rule 14) at 38% of a batch**, well
above the DSC rate, and the pattern is legible rather than random: **UWF's cultural-anthropology
faculty rename SCNS's `X and Culture` frame to an `Anthropology of X` frame.** That is a substantive
statement about the course — it puts the analytic apparatus first and the topic second — and in each of
these four the catalog description confirms the local title is the more accurate one.

**None is a correction candidate.** Each guide carries the local title, records the SCNS title inline,
and tells the student to **carry a syllabus when transferring the credit**, because an evaluator matching
on title alone will not connect "Gender and Culture" to "Global Gender Issues".

### ✅ "Offered concurrently with ANG 5xxx" is now quantified

Batch 120 confirmed the construction as routine; this batch pins the rate. **Five of the thirteen** —
ANT4006/ANG5453, ANT4302/ANG5302, ANT4403/ANG5022, ANT4473/ANG5472, ANT4532/ANG5408 — **and all five are
4000-level.** Zero occurrences at 2000 or 3000 level in this batch.

**The pattern is therefore a level marker, not a prefix quirk**: UWF runs its 4000-level anthropology
seminars as combined undergraduate/graduate sections against a paired `ANG` graduate number, with the
differential carried in additional work assigned to graduate students. **Each guide states the practical
effect for the undergraduate** — a seminar with graduate students present, reading pitched to work at
both levels, and undergraduate requirements deliberately lower than the graduate ones.

### Batch 122: content worth carrying

- **`ANT2301` (Human Sexuality and Culture) is the batch's sensitive-content course**, and the catalog
  itself commits to "inclusivity, safety, and sexual and reproductive health". The guide is
  **resource-pointing rather than clinical**: UWF Counseling and Psychological Services, **988**, and
  **RAINN 800-656-HOPE**, plus one point students are rarely told in advance — **campus counsellors are
  typically confidential and instructors typically are not**, because of Title IX reporting duties.
  **Know before disclosing** is the actionable form of that, and it is in the guide.
- **`ANT3312` and `ANT3311` both carry a shared Native-nations ethics block** — sovereignty as legal
  status rather than cultural label, the present tense, NAGPRA including its **2024 revisions**, THPO
  authority in Section 106, and tribal research permission as separate from university IRB.
- **Florida's Native history is not the removal story, and the guides say so.** The Apalachee, Timucua,
  Calusa and Tocobaga were destroyed by disease, mission-system disruption and Carolinian slave raids;
  **the Seminole and Miccosukee formed in Florida in the eighteenth century** from Creek and other
  groups moving south together with free and escaped Africans. **Treating them as continuous with the
  Timucua is the specific error students make**, and it is corrected explicitly.
- **The osteological paradox is stated in `ANT3311`** — skeletal stress markers can indicate people who
  survived long enough to develop them, so an apparently healthier assemblage may be people who died too
  fast to show damage. It is the sharpest example of the batch's evidence-reasoning theme.
- **`ANT4006` carries the discipline's own reversal**: the AAA objected to the Universal Declaration in
  **1947** and adopted its own human rights declaration in **1999**. Reading the two side by side is
  named in the guide as the single most efficient exercise in the course.
- **`ANT4403` states the conservation displacement record plainly** — fortress conservation, the
  wilderness idea as itself cultural, indigenous fire management, and **TEK extracted into management
  plans without consent or continuing relationship**, with the ecologically-noble-savage framing flagged
  as a stereotype that fails on contact with evidence.
- **`ANT4532` carries the batch's strongest advising warning**: the course leads with epidemiology and
  **anthropology students who have avoided statistics will feel it**. Age-standardisation and confounding
  are named, with the **free CDC Principles of Epidemiology self-study course** as the fix. The guide also
  states that **race is not a biological variable**, that race-based clinical algorithms have been
  withdrawn on those grounds, and that **cultural competence taught as a checklist of group traits
  produces stereotyping**.
- **Florida-specific anchors were available for every guide in the batch** and were used: Apalachicola
  Bay's oyster collapse and CERP for ANT4403; locally acquired dengue and malaria, Florida CHARTS and
  Baptist/Ascension Sacred Heart for ANT4532; Fort Mose and Kingsley Plantation for ANT3352; Mission San
  Luis, Lake Jackson Mounds and **FPAN, whose coordinating centre UWF hosts**, for ANT3311; PortMiami,
  Port Everglades and JAXPORT for ANT4473.

### Batch 123 — **EEL closes to its writable limit**: UWF electrical engineering (16)

`EEL3112`, `EEL3135`, `EEL3111L`, `EEL3701L`, `EEL4514L`, `EEL4657L`, `EEL4213`, `EEL4241`, `EEL4252`,
`EEL4283`, `EEL4287`, `EEL4290`, `EEL4510`, `EEL4276`, `EEL4663`, `EEL4712L`. All 16 published: eleven
3-credit lectures at 45 derived hours, five 1-credit laboratories at 45 derived hours.

**The prefix is closed to its writable limit, not emptied** — 11 rows remain unwritable, and the residue
is much larger and more consequential than ANT's. See the item-9 update below.

### ⚠⚠⚠ **CORRECTION**: the recorded claim that UWF publishes no fees is FALSE — 34 live guides fixed to v1.1

`SOURCES.md` recorded at batch 119, as a corpus-wide finding: *"it carries none of the following,
confirmed by searching the full ANT extraction: contact hours, lecture/laboratory splits, terms of
offering, corequisites, or laboratory fees — all returned zero matches."*

**Two of those five are wrong.**

| Claim | Verdict | Evidence |
|---|---|---|
| No contact hours | ✅ **holds** | 0 matches for "contact hour"/"lecture hour"/"laboratory hour" in both ANT and EEL |
| No lecture/lab split | ✅ **holds** | same |
| No terms of offering | ✅ **holds** | 0 matches for Fall/Spring/Summer in both |
| **No corequisites** | ❌ **FALSE** | UWF has a corequisite mechanism — the asterisk (below). ANT has 0 asterisks; **EEL has 14** |
| **No fees** | ❌ **FALSE** | **ANT: 3 fee-bearing courses. EEL: 5.** UWF also maintains a whole **"Material & Supply and Equipment Fees"** section of the catalog |

**The methodological failure is worth naming precisely, because it will recur.** The batch-119 search was
run over a single prefix and its result was recorded as an institution-wide property. **ANT is an
unusually poor prefix to generalise from** — a lecture-only humanities prefix has no laboratory fees and
no corequisites because of what it *is*, not because of how UWF publishes. **The fee-bearing ANT courses
existed all along** (ANT4121, ANT4824, ANT4835 — the field methods courses) and the batch-120 guides for
them *did* record their fees correctly, so the guide text and the recorded finding were in direct
contradiction and nobody noticed.

**Remediation completed this session.** The false sentence — *"It does not publish contact hours, a
lecture and laboratory split, terms of offering, or fees for any course"* — appeared in **34 live
guides** (21 from batches 119–121, 13 from batch 122). All 34 were rewritten, **bumped v1.0 → v1.1**,
revalidated (34 clean), and republished. The replacement text states the three claims that hold, states
that UWF **does** publish a fee notice on the minority of courses carrying one, and adds the advising
consequence: **the absence of a fee notice on an entry is meaningful; the amount is published
elsewhere.**

**Standing rule going forward: a property claimed of "UWF" must be verified in at least two prefixes of
different character before it is recorded as institution-wide.** One lecture prefix and one
laboratory-bearing prefix is the minimum.

### ✅✅ The UWF asterisk decoded — `*` means **concurrent**, and it is the highest-value notation in the catalog

The EEL entries are full of prerequisites written `EEL 3111*`, `EEL 4514*`, `EEL 4712*`. **The legend is
on the catalog's Course Information landing page** (`catalog.uwf.edu/courseinformation/`), which is
plain-fetchable HTML:

> **Concurrent Course** — *This course may be taken prior to or during the same term.*

**So `X*` as a prerequisite means X may be taken in the same term** — a corequisite by another name, and
the mechanism whose existence batch 119 concluded UWF lacked.

**Why this matters more than a notation detail:** UWF splits lecture from laboratory across engineering,
and **the asterisk is what makes taking the pair together legal**. Reading an asterisked prerequisite as
sequential **adds a term to the plan for no reason**, and in a chained engineering major that delay
propagates to graduation. **14 of 51 EEL courses carry an asterisked prerequisite.**

**Every EEL guide in this batch carries a shared block explaining the notation**, since a student who
learns it once can read the whole catalog correctly.

### ⚠⚠ Prerequisite and grade-condition publishing is **prefix-dependent**, and engineering is dense

| | ANT | EEL |
|---|---|---|
| Courses | 61 | 51 |
| `Prerequisite:` occurrences | 15 | **32** |
| Asterisked (concurrent) | 0 | **14** |
| Grade conditions published | **0** | **9** |
| Fee notices | 3 | 5 |

**All 16 courses in this batch carry a published prerequisite** — against zero in all 13 of batch 122.
The batch-122 note that UWF "publishes prerequisites only sometimes" is correct and is now sharpened:
**it publishes them thoroughly in engineering and sparsely in the humanities.**

**⚠⚠ The grade conditions are not uniform, and this is a genuine advising trap.** UWF publishes
**C or better** on EEL3112 and EEL4213, and **C- or better** on EEL4663 — and **EEL3112 carries a split
condition inside one prerequisite expression**:

> *"A grade of 'C' or better is required in the prerequisites, except MAP 2302, which requires a grade of
> 'C-' or better."*

**A differential grade threshold within a single prerequisite statement is new construction for the
corpus.** Batch 121 found a grade-conditional prerequisite; this is a materially more elaborate form.
**Each affected guide states the exact condition rather than generalising it.**

### ⚠⚠ A published exclusion rule that names two courses UWF does not offer — `EEL3111L`

UWF's EEL3111L entry ends: *"Credit may not be received in both EEL 3117L and EEL 3303L."*

**Neither number is EEL3111L, and neither appears anywhere in UWF's published EEL course list** (verified
against all 51 extracted numbers). **The rule as printed governs two courses UWF does not appear to
offer.**

Most likely a stale sentence retained from a previous numbering scheme, or attached to the wrong entry.
**The guide reports it verbatim and flags the anomaly rather than interpreting it** — guessing at intent
would be worse than stating that the published text does not parse. **Students who took a circuits
laboratory elsewhere under either number are told to raise it with an advisor explicitly.**

**This is a different failure mode from the mutual-exclusion rules found in ANT** (which named real,
published courses) and is the first *internally inconsistent* catalog statement found in the UWF corpus.

### ⚠⚠ `EEL4252` is published "may be repeated indefinitely for credit" — on a 4000-level technical course

Five EEL entries carry a repeatability phrase; **EEL4252 Power System Operation and Control carries
"indefinitely."** The construction normally attaches to seminars, special topics, and research courses,
**not to a named technical course with a substantive published description.**

Most likely the course runs with varying topical content under a stable title. **Reported as published,
not interpreted.** The guide adds the advising consequence the catalog does not: **repeatability in a
catalog is not applicability in a degree audit**, degree programmes cap credit from one number, and
**repeated-course rules interact with financial aid eligibility.**

### ⚠⚠ SCNS numbering that actively misleads — `EEL4213` / `EEL4252` are **siblings, not a sequence**

SCNS titles these "Power Systems I" and "Power Systems II". **UWF publishes EEL3211 as the prerequisite
for *both*.** EEL4213 is **not** required for EEL4252.

**This goes beyond title drift into structural drift: the SCNS numbering asserts a sequence the
institution does not implement.** A student reading "Power Systems II" will reasonably assume the
prerequisite chain that the catalog explicitly does not require. **The guide states it plainly** — and
still advises taking EEL4213 first, because power flow and per-unit are this course's working vocabulary
even though they are not enforced.

### ⚠ Title drift at **9 of 16** — the highest rate recorded, and engineering drifts differently from anthropology

| Course | SCNS / queue title | UWF local title |
|---|---|---|
| `EEL3135` | Signals & Systems | **Discrete-Time Signals and Systems** — a real *scope* narrowing, not a rename |
| `EEL4241` | Power Electronics | **Advanced Topics in Power Electronics** — intro vs advanced |
| `EEL4213` | Power Systems I | Electric Energy Systems 1 |
| `EEL4252` | Power Systems II | Power System Operation and Control |
| `EEL4276` | Smart-Grid and Cyber Physical Security | Cyber Security of Industrial Control System |
| `EEL3111L` | Circuits 1 Lab | Electrical Circuits Laboratory |
| `EEL3701L` | Introduction to Digital Systems Lab | Digital Logic and Computer Systems Laboratory |
| `EEL4657L` | Linear Control Systems | **Linear Controls Laboratory** — SCNS title omits "laboratory" |
| `EEL4663` | Applied Robotics | Elements of Robotics |

**56%, against ANT's 38%.** But the character differs and that is the finding: **ANT's drift was
rhetorical** (`X and Culture` → `Anthropology of X`, same content). **Two of EEL's are substantive
enough to change what a student gets:**

- **`EEL3135`** — the SCNS title promises a general signals course; **UWF's is scoped to discrete-time**,
  with continuous-time transforms carried upstream in EEL3112. A transfer in either direction lands a
  student with a gap or a duplication.
- **`EEL4241`** — SCNS says *Power Electronics* (an introduction); **UWF says *Advanced Topics*** and
  requires only an electronics course, no first power-electronics course. **The guide flags directly that
  a student may find fundamentals assumed but not taught**, and says to ask the instructor.

**⚠ `EEL4657L` is the nastiest case for an evaluator**: the SCNS title omits "laboratory", so the
transcript line reads *"Linear Control Systems, 1 credit"* — easily misread as a partial or failed
3-credit lecture course.

### ✅ The 4000-level concurrency pattern holds in a second prefix

Four of this batch are `Offered concurrently with EEL 5xxx` (4241/5245, 4252/5266, 4276/5277,
4510/5520), and **all four are 4000-level** — matching ANT exactly (5 of 5 at 4000 level).
**Confirmed across two prefixes in different colleges: UWF pairs 4000-level courses with a graduate
number and carries the differential in additional graduate work.** It is a level marker, not a
departmental habit.

### Batch 123: content worth carrying

- **A shared hour-derivation block distinguishes lecture from laboratory.** Lectures at 15/credit (45);
  laboratories at **45 per credit**, per the batches 88–90 engineering/science convention (EVR2001L,
  OCE1001L), with the guides stating the three-hours-a-week-for-fifteen-weeks shape the figure assumes.
- **Every laboratory guide carries real safety content**, and it is course-specific rather than boilerplate:
  charged capacitors and current-limiting for EEL3111L; **floating CMOS inputs and ESD** for EEL3701L;
  **spectrum-analyser front-end damage and FCC transmission rules** for EEL4514L; **emergency stops and
  the danger of first-run control code** for EEL4657L; **DC bus capacitors, isolation transformers, and
  the oscilloscope-ground short** for EEL4241; **robot workspace entry and ISO/TS 15066** for EEL4663.
- **`EEL4276` carries an explicit legal warning.** Unauthorised access to a computer system is a felony
  federally and under Florida statute, **with enhanced penalties for critical infrastructure**; the guide
  says practise only on owned or laboratory-provided equipment, and frames the course defensively as
  UWF's own description does.
- **A shared Florida grid block** covers the state's near-peninsular interconnection, weather-driven load
  shape, **hurricanes as a design condition rather than a contingency**, rapid solar growth, and the named
  employers (FPL/NextEra, Duke Energy Florida, TECO, JEA, OUC, **Gulf Power in UWF's own region**).
- **`EEL4290` carries the most Florida-specific analytical point in the batch: Florida is *not* a
  restructured market.** There is no ISO or RTO for peninsular Florida; utilities are vertically
  integrated under Public Service Commission rate regulation. **Most of the market literature the course
  assigns describes markets the student cannot observe locally**, and the guide turns that into the
  analytical contrast rather than leaving it as confusion.
- **Three energy electives (EEL4283, EEL4287, EEL4290) share the single EEL3111 prerequisite and
  overlap substantially.** A shared block separates their centres of gravity — survey / integration /
  markets — warns that **the marginal value of the third is low**, and says plainly that **none of them
  substitutes for the EEL3211 → EEL4213 analytical sequence** for a student aiming at utility engineering.
- **FE exam guidance is honest about its own limits**: the guides say licensure matters less in electrical
  engineering than in civil because of the industrial exemption, **and that it is required for consulting,
  sealing designs, and power work** — which is exactly where Florida's utility employment is.
- **Free-tool substitution is named throughout**, because these courses otherwise assume expensive
  licences: **Python/`python-control`, GHDL+GTKWave, LTspice, MATPOWER, OpenDSS, pandapower, NREL SAM and
  PVWatts, PowerWorld's free education edition, Wireshark, ROS 2, Gazebo, EDA Playground** — each named
  against the commercial tool it replaces, with "check UWF's campus licence before purchasing" stated.
- **Defence-sector guides note the citizenship and clearance requirement** (EEL4514L, EEL4276), because it
  shapes internship options in the third year and students rarely hear it early enough.

### Batch 124 — **the first orphan additions**: UWF EEL lecture halves (11), and EEL closes with zero residue

`EEL3111`, `EEL3211`, `EEL3211L`, `EEL3472`, `EEL3701`, `EEL4635`, `EEL4657`, `EEL4712`, `EEL4713`,
`EEL4744`, `EEL4744L`. Eight 3-credit lectures at 45 derived hours, three 1-credit laboratories at 45.

**⚠ These course IDs were not in `queue.csv`.** Ron approved writing them directly as orphan additions
(REVIEW_QUEUE item 9), which is **a first for this build**. `queue_mgr.py reconcile` picked all 11 up
automatically — *"+11 orphan draft(s) added to queue"* — and `--push-from-queue` then pushed them without
any separate `add` step. **The mechanism works and needs no change.**

**EEL is now the first prefix to close with zero residue: 33 pushed, 11 skipped, 0 queued.**

### ✅ Confirmed: the push endpoint creates the course record on demand

`PUT /api/v1/courses/{ID}/guide` **creates the `TaxonomyCourse` if it does not exist.** Verified twice:
`EEL4213` returned 404 before batch 123 and exists now; all 11 of this batch 404'd beforehand and are
live. **So the queue is a work-tracking artefact, not a gate** — any valid SCNS ID can be written and
pushed. That is what made this batch possible without server work, and it is worth knowing for any future
coverage gap.

### ⚠⚠ Reciprocal lecture↔laboratory binding — a new construction, and the strongest split-pair form found

Three UWF pairs list **each other** with the concurrent asterisk:

| Lecture | Laboratory | Lecture's prerequisite includes | Laboratory's prerequisite is |
|---|---|---|---|
| `EEL3111` | `EEL3111L` | `EEL3111L*` | `EEL3111*` |
| `EEL3701` | `EEL3701L` | `EEL3701L*` | `EEL3701*` |
| `EEL4712` | `EEL4712L` | `EEL4712L*` | `EEL4712*` |

**Because each names the other, the pair is effectively a single 4-credit course** that cannot be entered
from either side alone. **This is the strongest form of split-course binding in the corpus** and settles
what the split family actually means at UWF: not a course plus an optional companion, but two halves.

**⚠ `EEL4744` / `EEL4744L` is the instructive exception — the binding runs one way only.** The laboratory
requires `EEL4744*`; **the lecture does not require the laboratory.** So a student can take
Microprocessor Applications *without* the laboratory and never notice — and for a course whose entire
value is hands-on interfacing, that is the wrong default. **Both guides state this explicitly.**

**Remediation:** the three laboratory guides published in batch 123 (`EEL3111L`, `EEL3701L`, `EEL4712L`)
documented the asterisk correctly but did not know the requirement was reciprocal. **All three were
updated to v1.1** with the binding note and republished.

### ⚠⚠ A second corequisite notation — the explicit `Co-requisite:` field

`EEL3211L` publishes **`Co-requisite: EEL 3211`** rather than using the asterisk, and states *"Lab
corresponds with EEL 3211."* **UWF therefore has two notations for the same relationship**, and they are
not equivalent in strictness:

- **`X*` (concurrent)** — *"may be taken prior to or during the same term"*: prior completion is allowed.
- **`Co-requisite: X`** — conventionally *the same term*: prior completion may not be.

**A student who already completed the lecture in an earlier term is in different positions under the two
notations**, which the `EEL3211L` guide flags with a direction to confirm with an advisor.

**Frequency across the two prefixes extracted so far:** asterisk **14** (all EEL), explicit
`Co-requisite:` **3** — `EEL3211L`, and the reciprocal pair `ANT4525` / `ANT4525L`. **This is the third
correction to the batch-119 "no corequisites" claim**, and note that the ANT occurrences were inside the
very extraction that search ran over. **The batch-121 guide for `ANT4525L` recorded its corequisite
correctly**, so — as with the fee error — the guides were right and the recorded summary was wrong.

### ⚠⚠ Prefix-differentiated grade conditions — `EEL4712` and `EEL4744`

Both publish: *"A grade of 'C' or better is required in all EEL-prefixed prerequisites and a 'C-' in all
COP-prefixed courses."*

**The threshold depends on the prefix of the prerequisite, inside a single sentence.** A C-minus in a
programming course satisfies the requirement; the same grade in `EEL3701` does not. Combined with
`EEL3112`'s named exception (C, *except* MAP2302 at C-) and `EEL4663`'s flat C-minus, **UWF's grade
conditions are now confirmed as course-by-course rather than departmental**, with at least four distinct
patterns in one prefix. **Every affected guide states its exact condition rather than generalising.**

### ⚠⚠ `EEL3211` is a single point of failure for the whole power concentration

`EEL3211 Basic Electric Energy Engineering` is the **only** route to both `EEL4213` and `EEL4252`. It
requires `EEL3111` with a **C**, and nothing else reaches the power track.

**This was invisible until the orphan lecture was written**, because the queue carried only `EEL3211C` —
so the structural keystone of UWF's power concentration was the one course in the sequence with no guide.
**The guide states the consequence plainly**: a retake, or discovering the power track late, can push both
fourth-year power courses back a year in a programme where specialised electives may run annually, and
**UWF publishes no offering frequency either way**.

**⚠ The related trap is also now documented**: `EEL4283`, `EEL4287` and `EEL4290` require only `EEL3111`,
so they are available earlier and to non-specialists — **but taking them does not put a student on the
power track**, and they do not substitute for `EEL3211` → `EEL4213`.

### Batch 124: content worth carrying

- **A shared "why this guide exists under this number" block** opens each orphan guide, explaining that
  UWF splits what many institutions integrate, that **SCNS equivalency does not cross numbers**, and that
  transfer in either direction is evaluated by hand.
- **`EEL3111` and `EEL3472` are the two joint-most widely taught courses in the prefix (8 institutions
  each as C-variants)** and were the largest gaps in the site's electrical engineering coverage.
- **`EEL3472` carries the batch's most direct workload warning**: no vector calculus prerequisite is
  published although vector calculus is the working language, so **a student can be eligible to enrol
  without having consolidated the mathematics the course runs on**. The guide names refreshing it as the
  highest-value preparation available and puts the time commitment at 10–12 hours a week.
- **`EEL3211L` carries the batch's most serious safety content** — three-phase line voltage, machines
  drawing tens of amperes, coasting rotating machinery, **six-times-rated induction motor starting
  current**, and the rule that **an open-circuited current transformer secondary develops dangerous
  voltage**. This is the point in the curriculum where laboratory safety stops being precautionary.
- **`EEL4713` connects architecture to security** — speculative execution vulnerabilities are failures of
  exactly the mechanisms the course teaches (speculation, caching, timing), and the mitigations cost
  performance, which made a previously implicit trade-off explicit.
- **`EEL4744` and `EEL4744L` carry the practical embedded failure list** that interviews actually probe:
  `volatile` on ISR-shared variables, short non-blocking ISRs, atomic access to multi-byte shared data,
  **silent stack overflow with no protective fault**, switch bounce, I2C pull-ups, the four SPI modes, and
  **checking pin drive limits before connecting a motor or relay**.
- **`EEL4635` states the sampling-rate trade honestly in both directions** — too slow destabilises through
  the half-sample delay consuming phase margin; **too fast is also a failure mode**, pushing discrete poles
  toward z = 1 where finite word length and conditioning bite.
- **Free-tool substitution continues to be named against the commercial tool it replaces**: `python-control`,
  GHDL + GTKWave, Logisim Evolution, RARS/Ripes for RISC-V, sigrok/PulseView, EDA Playground, Falstad's
  applets — with "check UWF's campus licence before purchasing" stated throughout.

### Batch 125 — UWF Medical Laboratory Sciences, standard track (12)

`MLS3621`, `MLS4191`, `MLS4191L`, `MLS4460L`, `MLS4505`, `MLS4334`, `MLS4550`, `MLS4550L`, `MLS4625`,
`MLS4625L`, `MLS4630`, `MLS4705`. **MLS is a 27-row prefix and this is the first of two batches** — the
Professional Track and the hospital clinical rotations remain, plus three orphan halves.

### ⚠⚠⚠ The `C` suffix means something COMPLETELY DIFFERENT in this prefix — a parallel programme track

**UWF runs two distinct routes through the same MLS subject matter**, and the C-suffix courses are the
second route rather than an integrated version of the first:

| | Standard track | **"Professional Track"** |
|---|---|---|
| Form | split lecture + laboratory (`MLS4550` + `MLS4550L`) | integrated **C**-suffix, 3–4 sh (`MLS4552C`) |
| Prerequisites | **general science** — PCB3063, BCH3033, MCB3020 | **MLS-internal** — `MLS3194` AND `MLS3621` |
| Members | 4220/L, 4305/L, 4334/L, 4460/L, 4462/L, 4505/L, 4550/L, 4625/L, 4630/L | 4193C, 4221C, 4306C, 4335C, 4461C, 4463C, 4506C, 4552C, 4626C, 4631C, 4704 |

**⚠⚠ This breaks the statewide reading of the `C` suffix.** Everywhere else in this corpus, `C` marks an
integrated lecture-plus-laboratory version of the same course. **Here it marks a different programme
track with different entry requirements** — so the split-family rule from batch 124 **does not apply
mechanically in this prefix**, and applying it blindly would have produced wrong guides.

**Every guide in this batch carries a shared block explaining the two tracks**, because a student who
reads the suffix by the statewide convention will enrol in the wrong sequence.

**The two genuinely unwritable rows are a different case:** `MLS4460C` and `MLS4462C` have no UWF entry
at all, and UWF instead publishes `MLS4460` + `MLS4460L` and `MLS4462` + `MLS4462L`. **Those three
missing halves (`MLS4460`, `MLS4462`, `MLS4462L`) are true batch-124-rule orphans** and are queued for
the next MLS batch.

### ⚠⚠ Systematic title drift: SCNS "Clinical X" = UWF "X Professional Track"

Seven queue rows map onto Professional Track courses under a completely different name:

| Queue / SCNS title | UWF local title |
|---|---|
| CLINICAL MOLECULAR DIAGNOSTICS (`MLS4193C`) | Molecular Diagnostics **Professional Track** |
| CLINICAL URINALYSIS (`MLS4221C`) | Urinalysis/Body Fluids **Professional Track** |
| CLINICAL HEMATOLOGY (`MLS4306C`) | Hematology **Professional Track** |
| CLINICAL HEMOSTASIS (`MLS4335C`) | Hemostasis and Thrombosis **Professional Track** |
| CLINICAL DIAGNOSTIC MICROBIOLOGY (`MLS4461C`) | Diagnostic Microbiology **Professional Track** |
| CLINICAL IMMUNOLOGY (`MLS4506C`) | Clinical Immunology **Professional Track** |
| ADVANCED IMMUNOHEMATOLOGY (`MLS4552C`) | Immunohematology **Professional Track** |

**This is the most systematic title drift found so far** — not a per-course rename but a **whole naming
convention**, where SCNS's `Clinical X` becomes UWF's `X Professional Track`. It will be documented in
full when those courses are written.

### ⚠⚠ "Permission is required" — a programme-admission gate on nearly every course

The phrase appears on almost every MLS entry. **Meeting the published prerequisites does not make a
student eligible to enrol** — in practice it means admission to the cohort-based, capacity-limited MLS
programme.

**This is advising-critical and has no analogue in ANT or EEL.** A student who completes every science
prerequisite and misses the cohort application **waits a full year**, because a cohort sequence normally
starts once a year — and **UWF publishes no terms of offering, so that cannot be confirmed from the
catalog**. Every guide in the batch carries a shared block saying so.

### ⚠⚠ A THIRD corequisite notation — narrative prose, and it is conditional on major

UWF now demonstrably expresses co-requisites three different ways:

1. **`X*` on a prerequisite** — *"may be taken prior to or during the same term"* (14 in EEL, 0 in ANT).
2. **An explicit `Co-requisite:` field** — used routinely on MLS laboratories (`MLS4191L`, `MLS4460L`,
   `MLS4550L`, `MLS4625L`), and on `EEL3211L` and the `ANT4525` pair.
3. **⚠⚠ NEW: plain prose in the description** — *"MLS students are required to take the corresponding
   laboratory, MLS 4550L, as a co-requisite."* Found on `MLS4505`, `MLS4550`, `MLS4625`, `MLS4630`,
   `MLS4334`.

**The MLS pairs bind reciprocally but through two different notations at once** — the formal field on the
laboratory, prose on the lecture.

**⚠⚠ And the prose form carries a conditional the field form does not: it is stated for *MLS students*.**
A student from another programme may take the lecture without the laboratory — **getting the didactic
content without the bench work**. Each affected guide flags this and says to confirm which applies.

### ⚠⚠ A SECOND fee type — "Equipment fees" — and courses carrying both

Batch 123 corrected the false "UWF publishes no fees" claim. MLS extends it: **UWF publishes two distinct
fee notices**, and several courses carry both.

| Wording | MLS occurrences |
|---|---|
| `Material and supply fee(s) will be assessed` | 6 |
| **`Equipment fee(s) will be assessed`** | **10** |

`MLS4191L`, `MLS4460L`, `MLS4550L` and `MLS4625L` each publish **both**; `MLS4334` publishes the equipment
fee alone. **No amount is published in any course entry.** The guides say so, point at the catalog's
separate fees section, and — because clinical laboratory courses are genuinely fee-heavy — **advise asking
the department for the cumulative total across the whole MLS sequence rather than course by course**.

### ⚠⚠ Hospital clinical rotations are NOT teaching laboratories — the hour convention does not transfer

`MLS4820L`–`MLS4825L` carry the `L` suffix and are **not laboratory courses in the usual sense**. Their
descriptions say *"allows for supervised practice in the hospital laboratory"*, they run at **4, 4, 4, 4,
2 and 2 semester hours**, and their prerequisite is the entire first-year MLS sequence plus `MLS4705`.
`MLS4944`–`MLS4947` are explicit Clinical Practicums, **`MLS4947` at 12 semester hours**.

**⚠ The recorded 30-hours-per-credit clinical-laboratory convention was established for on-campus teaching
laboratories and must not be applied to these.** A full-time hospital rotation bears no relation to a
two-hour weekly campus session. **These six are deliberately held for the next MLS batch** so the hour
question can be handled on its own terms rather than by reflex — and they may warrant deferral rather
than a derived figure.

**The convention used in this batch, stated in every guide:** 15 hours per credit for lecture
(45/30/15 for 3/2/1 sh), **30 per credit for on-campus clinical laboratories, explicitly labelled a floor**
because MLS programmes commonly schedule longer blocks.

### ⚠ A time-window requirement — new construction

`MLS4705` states it *"must be taken within 18 months of the clinical internship."* **Not a prerequisite —
a timing constraint**, and it binds in both directions: too early is as much a problem as too late. It is
also a prerequisite for all six clinical rotation courses. **The guide notes the practical consequence:
a student who interrupts their programme may have to retake it.**

### ✅ `MLS4705` "Special Clinical Topics" — a shell-titled course that is NOT a shell

The title matches this repository's default skip keywords (`SPECIAL TOPICS`). **It was checked against the
description before being written**, and the content is specific and stable: clinical laboratory
management, supervision, financial and human resource management, laboratory information systems, and
regulatory compliance — **explicitly because the national certification examination tests them**.

**This is the "has it become titled?" test applied in reverse** — a generic title over specific, settled
content. **Kept and written.** Worth recording as a counterexample to the skip rule.

### Batch 125: content worth carrying

- **⚠⚠ Florida licenses clinical laboratory personnel, and most states do not.** The Florida Department of
  Health requires a state licence to work at the bench, and **a national certification alone is not
  sufficient**. This is the single most important regulatory fact for a Florida MLS student, it cuts both
  ways for in- and out-of-state movers, and **it is carried in a shared block in every guide** alongside
  NAACLS accreditation, ASCP Board of Certification, and CLIA.
- **⚠ Programmatic accreditation outranks institutional accreditation here.** Certification eligibility
  generally depends on graduating from a NAACLS-accredited programme, so **transferred coursework may not
  preserve it** — the guides say to confirm with NAACLS directly.
- **`MLS4550`/`MLS4550L` carry the batch's most serious safety content.** An ABO-incompatible transfusion
  can kill within minutes, and **the commonest cause of a fatal reaction is patient identification error,
  not a testing error** — the bench work can be flawless and the patient can still die. Emergency release,
  FDA/AABB regulation, and refusal on religious grounds are all covered.
- **Antibody panel logic is documented as the discipline's defining skill** — exclusion on homozygous cells
  where dosage applies, the rule of three, multiple antibodies, and what a positive autocontrol changes.
- **A shared bloodborne-pathogen block** carries OSHA 29 CFR 1910.1030, hepatitis B vaccination at no cost,
  **never recapping needles**, aerosol routes, and **reporting every exposure immediately because
  post-exposure prophylaxis is time-critical and the instinct to say nothing is the dangerous one**.
- **A shared quality-control block** treats QC as the profession rather than overhead: Levey-Jennings,
  Westgard rules, **pre-analytical error dominating**, and delta checks.
- **⚠⚠ The guides state plainly that repeating a control until it passes is laboratory misconduct**, not a
  workaround — and that when a control is out the correct action is to stop.
- **Predictive value depends on prevalence** is developed in both `MLS4505` and `MLS4630` — why screening
  tests are confirmed, and why most tumour markers are unsuitable for screening asymptomatic people.
- **The prozone and hook effects** are covered as the paired counterintuitive traps: too much antibody or
  analyte producing a falsely low or negative result.
- **`MLS4460L` states the interpretive core of clinical microbiology** — growth is not infection, specimen
  quality determines meaning, site context changes everything, and **how results are reported measurably
  changes what clinicians prescribe**, which is why the laboratory is central to antimicrobial stewardship.
- **`MLS4334` documents coagulation as the most pre-analytically fragile testing in the laboratory** —
  citrate tube fill, haematocrit adjustment, heparin contamination from a line — and **that rejecting an
  inadequate specimen is correct practice under pressure to report something**.
- **Florida employer anchors** are named in a shared block: AdventHealth, Orlando Health, BayCare, Baptist
  Health, Tampa General, Jackson Health, **Baptist Health Care and Ascension Sacred Heart in Pensacola**,
  Quest and Labcorp, **OneBlood** as the state blood supplier, and the **Florida Department of Health
  Bureau of Public Health Laboratories**.
- **An honest note on the work itself** closes the careers block: clinical laboratory scientists are
  largely invisible to patients, produce most of the objective data behind diagnoses, work shifts including
  nights and weekends, and **carry real consequence**.

### Batch 126 — UWF MLS clinical rotations (6) + orphan halves (4)

`MLS4820L`, `MLS4821L`, `MLS4822L`, `MLS4823L`, `MLS4824L`, `MLS4825L`, plus orphan additions
`MLS3194`, `MLS4460`, `MLS4462`, `MLS4462L`. The two true split-family rows `MLS4460C` and `MLS4462C`
were then marked `skipped`. **MLS now has only the 7 Professional Track courses outstanding.**

### ⚠⚠⚠ Ron's framing, and it should govern how this corpus reads every suffix

> *"Many of these course designations are just trying to fit course requirements into a limited group of
> course designation options."*

**This is the correct general explanation for a whole class of findings this build has been logging
one at a time, and it is now a named theme.** SCNS offers a small set of suffixes — no suffix for
lecture, `C` for combined, `L` for laboratory — and **every course an institution runs has to be filed
under one of them**. When the course does not fit, the closest available slot is used.

**The suffix therefore records a filing decision, not the content.** Three instances now documented:

| Course | Suffix says | Course actually is |
|---|---|---|
| `MLS4820L`–`4825L` | laboratory | **supervised practice in a hospital** — a clinical rotation |
| `MLS4193C` etc. | combined lecture+lab | **a separate "Professional Track" programme route** |
| `MLS4947` | (Practicum) | **12 semester hours** of full-time clinical placement |

**The operating rule for the rest of this build: the description is the authority on what a course is;
the suffix is the authority on nothing.** Every rotation guide in this batch carries a block saying so
explicitly, at Ron's direction, so a student reading a transcript or catalog is not misled by the letter.

**This also reframes the drift theme.** Much of what has been recorded as "drift" is not institutions
diverging from a standard — it is **institutions encoding genuinely varied provision into a code set
that was never large enough to describe it**. Title drift, the parallel numbering families, and the
C-suffix ambiguity are all the same pressure showing up in different fields.

### ⚠⚠ Hour derivation for clinical rotations — a practicum convention, explicitly labelled a floor

Batch 125 held these six back rather than applying the 30-hours-per-credit clinical-laboratory
convention, which was established for on-campus teaching laboratories. **Resolved this batch:**

- **45 contact hours per credit**, the standard practicum convention — giving **180 hours at 4 sh** and
  **90 at 2 sh**.
- **Every rotation guide states the figure is a floor, not an estimate**, and explains why: NAACLS
  rotations are commonly scheduled as **full-time blocks at an affiliated hospital over a number of
  weeks** rather than as hours spread across a term.
- **⚠ Each guide names the schedule as the single most important practical fact UWF does not publish**,
  and tells the student to get it from the department in writing before planning employment, childcare,
  or travel.

### ⚠⚠ The rotation prerequisite is the entire preceding programme — and it has a structural consequence

All six rotations carry the same prerequisite: **ten lecture-and-laboratory pairs plus `MLS4705`** —
`MLS4191/L AND MLS4220/L AND MLS4305/L AND MLS4334/L AND MLS4460/L AND MLS4462/L AND MLS4505/L AND
MLS4550/L AND MLS4625/L AND MLS4630/L AND MLS4705`.

**⚠⚠ Because every rotation carries the complete set, one failed didactic course does not delay one
rotation — it delays all six**, and in a cohort programme that is a year rather than a term. The guides
state this plainly; it is the structural reason clinical laboratory science programmes have so little
slack.

**The `/L` shorthand** (`MLS 4191/L`) is UWF notation for a course together with its laboratory, and it
also appears in EEL (`PHY 2049/L`, `MCB 3020/L`). Recorded as a corpus-wide reading rule.

### ⚠ `MLS3194 Clinical Genetics` — a keystone course that was never in the queue

`MLS3194` is not in the statewide priority inventory, so it had no guide — yet **with `MLS3621` it gates
every Professional Track course**, and it substitutes for `PCB3063` across much of the standard track.
**Written as an orphan under the batch-124 rule.**

This is now the second time a prefix's structural keystone turned out to be the course with no guide
(`EEL3211` was the first, batch 124). **Worth watching for: the courses that gate a whole concentration
are frequently mid-level, unglamorous, and offered at few institutions — exactly the profile that keeps
them out of a count-based priority queue.**

### Batch 126: content worth carrying

- **`MLS4823L` (Immunohematology II) carries the sharpest safety framing in the corpus**: it is the
  rotation with the shortest distance between a bench error and a dead patient, **the commonest cause of
  a fatal transfusion reaction is patient identification error rather than a testing error**, and
  *"you will be asked to make an exception; the answer is no."*
- **`MLS4822L` (Hematology II) documents the morphology findings that must be acted on immediately** —
  blasts in a patient not known to have leukaemia, **schistocytes with thrombocytopenia suggesting TTP**,
  and malaria parasites. **Platelet clumping causing a falsely low automated count** is included because
  reporting the analyser number without checking the film has led to unnecessary transfusion.
- **`MLS4825L` covers phlebotomy — the one procedure in the whole programme performed on a person.**
  Two identifiers from the patient, never pre-label, never label away from the bedside, and **knowing
  when to stop and hand over**.
- **`MLS4824L` documents the failure modes of low-volume testing**, which no other guide has covered:
  competency lapse on rarely performed procedures, and **send-out testing as where specimens get lost
  and results get missed**.
- **`MLS4462`/`MLS4462L` carry the Florida tropical-disease picture** — imported and locally acquired
  malaria and dengue, endemic fungi, free-living amoebae — and **`Coccidioides` as a documented cause of
  laboratory-acquired infection from opening a mould plate on the open bench**.
- **A shared clinical-site block** covers what students consistently underestimate: immunisation and
  background-check lead times, **HIPAA applying personally from day one with audit detection**, assigned
  sites that may not be local, and **the rotation being an extended job interview** since hospitals hire
  the students they train.
- **`MLS3194` connects bacterial genetics to antimicrobial resistance** — horizontal transfer across
  species, plasmids carrying several resistance genes so exposure to one antibiotic selects for others —
  and **states the GINA gap: no protection in life, disability, or long-term care insurance**.

### Batch 127 — the MLS Professional Track (11), and **MLS closes**

`MLS4193C`, `MLS4221C`, `MLS4306C`, `MLS4335C`, `MLS4461C`, `MLS4506C`, `MLS4552C` from the queue, plus
orphan additions `MLS4463C`, `MLS4626C`, `MLS4631C`, `MLS4704`. **MLS: 33 pushed, 2 skipped, 0 queued** —
the third prefix to close, after ANT and EEL.

### ⚠⚠⚠ THE FINDING: the Professional Track is a degree-completion route for people ALREADY WORKING in laboratories

Batch 125 established that the `C` courses are a separate track. **This batch establishes what the track
is for**, and it changes the advice a student needs.

**The evidence, all from the catalog text:**

1. **Every Professional Track course states that "students will perform *virtual* laboratory activities."**
   There is no bench component anywhere in the track.
2. **The track contains no hospital rotations.** `MLS4820L`–`4825L` belong to the standard track only.
3. **⚠⚠⚠ `MLS4704`, the track capstone, requires the student to *"provide evidence of adequate training or
   work experience in Hematology, Clinical Chemistry, Microbiology, and Blood Bank **equivalent to an MLS
   clinical internship**"* and present it as a portfolio.**

**Read together: the portfolio stands in place of the clinical rotations, and the virtual laboratories
replace bench teaching — because the track assumes the bench competence already exists and needs
evidencing rather than building.** That is a degree-completion pathway for a working technician or
experienced laboratorian.

**⚠ This is an inference from the catalog text, not a quotation, and every guide labels it as such.**
It is stated anyway because the consequence is large: **a student with no laboratory work experience
cannot complete `MLS4704`, and therefore cannot complete the track.** Each guide tells the reader to
confirm with the department which route applies and — critically — **to ask in writing which certification
route the track prepares them for**, since ASCP eligibility varies by education and experience and Florida
adds state licensure on top.

**Corroborating detail:** `MLS4626C` opens *"This course is a review of the basic principles..."* where the
standard-track `MLS4625` says *"an introduction to"* — the same material, pitched at someone who has met
it in practice.

### ⚠⚠ The validator encodes the statewide C-suffix assumption, and flagged four correct guides

`validate_drafts.py` warned on `MLS4221C`, `MLS4335C`, `MLS4626C` and `MLS4631C`:

> *"'MLS4221C' is an integrated lecture+lab (C) course but has only 45 contact hours"*

**The heuristic assumes `C` = integrated lecture+lab and therefore expects ~60 hours for 3 credits.**
In this prefix that assumption is wrong — these are lecture courses with *virtual* activities inside a
single enrolment, so 15 hours per credit is correct and no separate laboratory hours are added.

**This is Ron's suffix rule (batch 126) showing up inside our own tooling**, which is worth recording:
the assumption is baked in far enough that it reached the validator. **The warnings are non-blocking and
were correctly overridden.** ⚠ Worth considering a per-prefix exception if the warning recurs elsewhere;
flagged for Ron rather than changed unilaterally.

### ⚠ A probable catalog typo — `CHM 2022` vs `CHM 2202`

`MLS4631C` publishes the chemistry branch as **"CHM 2210 OR CHM 2022"**; the companion `MLS4626C`
publishes **"CHM 2210 OR CHM 2202"** for the same requirement. **A digit transposition in one of them is
the plausible explanation.** Reported as published in both guides rather than corrected, with a direction
to confirm with an advisor — the same treatment given to `EEL3111L`'s exclusion rule naming two courses
UWF does not offer.

### ⚠ Systematic title drift confirmed across the whole track

Seven queue rows carry SCNS titles that name the courses `Clinical X` or `Advanced X` where UWF names them
**`X Professional Track`**. **This is a naming convention rather than seven renames**, and a transfer
evaluator matching on title alone will not connect them — the credit values differ from the standard-track
equivalents too. Every guide carries a block saying so and naming its standard-track counterpart for
comparison.

### ⚠ Four more courses that were never in the queue

`MLS4463C`, `MLS4626C`, `MLS4631C` and `MLS4704` are all published by UWF and none appeared in the
statewide inventory. **`MLS4704` is the most consequential omission in the UWF build so far** — it is the
course that explains the entire track, and without it the track's design is invisible.

**Third instance of the pattern** (after `EEL3211` and `MLS3194`): **the courses that determine how a
programme actually works are frequently the ones a count-based priority queue never surfaces.**

### Batch 127: content worth carrying

- **A shared "what the Professional Track is" block** opens every guide with the three pieces of evidence
  and the inference drawn from them, explicitly labelled as an inference.
- **A shared virtual-laboratory block** is honest in both directions: virtual delivery is genuinely good
  for interpretation, quality control reasoning, case correlation, and **showing rare findings a teaching
  laboratory would never happen to have** — and it **cannot build psychomotor skill** (pipetting, grading
  agglutination by eye, streaking for isolation, finding a low-density object down a microscope) or the
  conditions of working under time pressure.
- **Each guide names its standard-track counterpart** with credit values, so a student or evaluator can
  see the two routes side by side.
- **`MLS4704` carries the batch's most actionable warnings**: the portfolio names **four disciplines**, so
  uneven experience may not satisfy it; **evidence means documentation, not assertion**; and **records from
  a former employer are much harder to obtain after you leave**. It also flags the **College-Level
  Communication Skills Requirement** — the second occurrence in the corpus after `ANT4403` — including that
  the designation is the part least likely to transfer.
- **Case-study confidentiality is treated seriously** in `MLS4704`: a rare condition plus a named
  institution plus a date can identify a patient with no name attached.
- **`MLS4221C` flags that its scope far exceeds its SCNS title** — "Clinical Urinalysis" implies urine,
  while UWF covers cerebrospinal, serous, synovial, semen, sweat and dialysates, **and the body fluid
  material is where the urgent findings live**.
- **`MLS4335C` at 3 sh against the standard track's 1 sh** for the same subject is noted as evidence the
  Professional Track version absorbs the laboratory content.
- **`MLS4631C` is the one track course with no virtual laboratory** — it names a **journal club** instead,
  which suits a subject dominated by interpretation and method selection.

### Batch 128 — UWF Nursing, the standalone family (10)

`NUR1010`, `NUR3067`, `NUR3081`, `NUR4125`, `NUR4286`, `NUR4826` from the queue, plus orphan additions
`NUR3145`, `NUR4636`, `NUR4828`, `NUR4895`. **NUR is a 24-row prefix; this is the first of two batches** —
the chained cohort sequence remains.

### ⚠⚠ A THIRD parallel-route prefix — and this time UWF never says so

ANT and EEL had one route each. MLS had two (standard + Professional Track), and **UWF named the second
one in every course title**. NUR also has two, and **UWF names neither**. The split is visible only in the
prerequisites:

| | Chained cohort sequence (23 courses) | **Standalone group (10 courses)** |
|---|---|---|
| Prerequisites | tight blocks, each carrying the previous | **none at all** |
| Co-requisites | extensive within-block lists | **none at all** |
| Shape | `NUR3026/L`+`3095`+`3125`+`3138C` → `3215/L`+`3505/L`+`3805`+`3871` → `4169`+`4216/L`+`4445/L` → `4257/L`+`4615/L`+`4636L`+`4827` | independent courses |

**⚠⚠ The two groups cover the same subjects under different numbers, and the pairing is systematic:**

| Standalone | Chained | Note |
|---|---|---|
| `NUR3081` Professional Nursing Practice | `NUR3805` Professional Nursing Practice | **identical title** |
| `NUR4125` Pathophysiology | `NUR3125` Pathophysiology for Nurses | |
| `NUR3145` Pharmacology | `NUR3095` Introduction to Pharmacology | |
| `NUR3067` Health Assessment and Promotion | `NUR3138C` Health Assessment and Promotion in Nursing | |
| `NUR4826` Transformational Nursing Leadership | `NUR4827` Leadership in Nursing | |
| `NUR4636` Epidemiology and Population Health | `NUR4615` Person Centered Population Health | |

**`NUR3081` and `NUR3805` sharing an exact title is the sharpest instance of this pattern in the whole
corpus** — a student searching by title finds both and only one counts.

**The inference and its limits.** A pre-licensure programme alongside a degree-completion route for
already-licensed nurses is the standard structure and fits the evidence. **But a search over the whole NUR
extraction returns ZERO occurrences of "RN", "registered nurse", "licensed", or "RN to BSN".** Two pieces
of supporting text exist and both are indirect: **`NUR1010` names "pre-licensure nursing students"**
(placing it in the first route), and **`NUR4895` describes a capstone enhancing "prior nursing knowledge
and skills" in "clinical practice experiences" with "practice partners"** (describing someone who already
practises and already has a practice setting).

**Every guide states the structure as observed, labels the two-route reading as an inference, and tells the
student to confirm with the department.** The stakes justify saying it: **a degree-completion route does
not lead to initial licensure**, so choosing wrong is not a wasted term but a wasted degree.

### ⚠ The batch-127 prediction for NUR was WRONG, and that is worth recording

The handoff predicted NUR would repeat the MLS health-prefix patterns. It does not:

| | MLS | **NUR** |
|---|---|---|
| "Permission is required" | on nearly every course | **ZERO occurrences** |
| Fee notices | 16 across the prefix | **effectively none** |
| Track named in titles | "Professional Track" on every member | **not named anywhere** |

**Health prefixes are not a uniform category.** The prediction was reasonable and it was not evidence, and
the same rule that produced the batch-123 fee correction applies: **check each prefix rather than
generalising from a sibling.**

### ⚠⚠ Two courses where the SCNS title names a DIFFERENT SUBJECT, not a variant

This goes beyond title drift:

| Course | SCNS title | UWF title | Relationship |
|---|---|---|---|
| `NUR4286` | **Gerontological Nursing** | Concepts of Quality and Safety in Nursing | **different subject** |
| `NUR4826` | **Ethics** | Transformational Nursing Leadership | **different subject** |
| `NUR4828` | Professional Nursing III | Systems Innovation and Change Agents in Healthcare | generic vs specific |

**`NUR4286` is the most consequential.** A student or evaluator matching on the SCNS title expects care of
older adults and gets quality improvement and informatics. **Both guides state plainly that the course
should not be assumed to satisfy a requirement named by the SCNS title** — gerontology or ethics
respectively.

**This is Ron's suffix rule extended to titles**: the SCNS number carries a title from a statewide list,
the institution teaches what its curriculum needs, and **the name in the inventory can end up describing a
different course entirely**.

### ✅ Third occurrence of the College-Level Communication Skills Requirement

`NUR4828` carries it, after `ANT4403` (batch 123) and `MLS4704` (batch 127). **UWF publishes this
designation inside the description text rather than in a structured field**, which is why it is easy to
miss — worth grepping each prefix extraction for `Communication Skills Requirement`. All three guides state
the same two consequences: **confirm the minimum grade**, and **the designation is the part least likely to
transfer** even where content articulates.

### Batch 128: content worth carrying

- **A shared licensure block** covers the Florida Board of Nursing, NCLEX-RN, CCNE/ACEN accreditation, and
  the Nurse Licensure Compact — with the key warning that **programme approval rather than individual
  course credit governs examination eligibility, so transferring nursing courses frequently does not
  work**.
- **`NUR3145` (Pharmacology) carries the batch's most operationally serious content**: high-alert
  medications, never working around a safety barrier, **"write 0.5 mg, never .5 mg"** because decimal
  errors are tenfold dose errors, and that **"the doctor prescribed it" is not a defence**. It also notes
  that dosage-calculation examinations are commonly pass-fail at or near 100%.
- **`NUR3067` flags a documented clinical disparity**: assessment findings on darker skin — cyanosis,
  pallor, jaundice, erythema, pressure injury — present differently and are covered inadequately in older
  resources, and **learning only the fair-skin presentation produces missed diagnosis in patients of
  colour**.
- **`NUR4636` carries Florida-specific emergency preparedness** that is genuinely distinctive: **healthcare
  workers are frequently required to remain on site through a hurricane** under A-team/B-team
  arrangements, which affects family planning in a way few jobs do; **Florida has seen fatal failures of
  facility emergency planning**, which is why generator rules exist; and disaster triage **inverts** normal
  priorities.
- **`NUR4286` explains just culture as the idea the whole safety field rests on**, including that it is
  *not* blame-free, and that **criminal prosecution of nurses for error drives reporting underground** —
  material students will have strong feelings about.
- **`NUR4826` names horizontal incivility in nursing directly** — the "nurses eat their young" pattern is
  documented, contributes to new-graduate attrition, and is a leadership failure rather than an
  inevitability. It also names **moral distress** as a documented driver of burnout.
- **`NUR4895` treats community partnership ethically**: communities are **over-researched and
  under-served**, students arrive and graduate and leave, and **sustainability is an ethical question — plan
  the ending at the beginning**. It also flags that **the QI-versus-research boundary is determined by the
  review board, not by the student**, and retrospective approval does not exist.
- **`NUR3081` engages the associate-versus-baccalaureate question honestly** — same licence, same NCLEX,
  differences in employment and progression rather than licensure, contested outcome research, and the
  observation that **experienced associate-prepared nurses in a BSN classroom have expertise the curriculum
  does not always acknowledge**.

### Batch 129 — UWF Nursing cohort sequence (17), and **NUR closes**

`NUR3026`, `NUR3026L`, `NUR3138C`, `NUR3215`, `NUR3215L`, `NUR3505`, `NUR3505L`, `NUR4165`, `NUR4216`,
`NUR4216L`, `NUR4257`, `NUR4257L`, `NUR4445`, `NUR4445L`, `NUR4615`, `NUR4615L`, `NUR4636L`. Five C/L rows
then skipped. **NUR: 45 pushed, 8 skipped, 0 queued** — the fourth prefix to close, after ANT, EEL and MLS.

### ⚠⚠ A CIRCULAR PREREQUISITE in the published catalog

**UWF publishes `Prerequisite: NUR 3805` on `NUR3026`, and `Prerequisite: NUR 3026/L AND NUR 3095 AND
NUR 3125 AND NUR 3138` on `NUR3805`.** Each names the other. **As published, neither course can be taken
first.**

Reported verbatim in the guide with the anomaly flagged, not corrected — the likely explanation is a
block-sequencing artefact (NUR3805 sits in the second block's co-requisite list, so the entry may mean
"taken with" rather than "taken before"), **but that is a guess and the guide says so**. Students are told
to ask the department, since the registration system rather than the catalog is what enforces it.

**Third catalog-internal inconsistency in the corpus**, after `EEL3111L`'s exclusion rule naming two
courses UWF does not offer and `MLS4631C`'s `CHM 2022` / `CHM 2202` transposition. **Treatment is now
settled: reproduce as published, name the anomaly, refuse to guess, direct the student to the department.**

### ⚠⚠ Co-requisite BLOCKS, not co-requisite courses — a structural first

UWF's pre-licensure sequence is **four blocks**, each enrolled as a unit:

| Block | Members | Prerequisite |
|---|---|---|
| 1 | `NUR3026` + `3026L` + `3095` + `3125` + `3138C` | (entry) |
| 2 | `NUR3215` + `3215L` + `3505` + `3505L` + `3805` + `3871` | all of block 1 |
| 3 | `NUR4169` + `4216` + `4216L` + `4445` + `4445L` | all of block 2 |
| 4 | `NUR4257` + `4257L` + `4615` + `4615L` + `4827` | all of block 3 |

**⚠⚠ Every member of a block carries the same prerequisite — the entire preceding block.** So **one failed
course does not delay one course; it delays the whole next block**, and in a cohort programme that is a
**year, not a term**. Every guide in the batch states this explicitly; it is the structural reason nursing
programmes have so little slack.

**This is a step beyond the MLS rotations**, where six courses shared one prerequisite set. Here the
blocks chain, so the effect compounds down the sequence.

**⚠ `NUR4636L` is the exception** — it lists **only `NUR4615`** as a co-requisite where the rest of the
final block names five. Likely an additional community placement attached to the population health course
rather than a full block member; flagged in the guide.

### ⚠ `NUR4165` sits outside the whole structure

The most widely taught course in the prefix (**~12 institutions**) is **the only NUR course at UWF with a
single external prerequisite (`STA2023`) and no co-requisite block**. UWF also publishes `NUR4169`
*Integration of Evidence in Professional Practice* **inside** block 3 — **so each route has its own
evidence course**, and `NUR4165` is the one reachable from outside the cohort sequence. Both guides
cross-reference the other.

### ⚠ The validator's conventions conflict with clinical hours — again

Three clinical courses warned: *"3 credits with 135 contact hours (expected ~45)"*, and `NUR3138C` warned
*"integrated lecture+lab (C) course but has only 45 contact hours"*.

**Both warnings are the validator applying lecture/C-suffix conventions to courses that are neither.**
Clinical hours are derived at **45 per credit** (three clock hours weekly per credit), labelled a floor;
`NUR3138C` is a lecture inside a block whose clinical work is carried by separately numbered `L` courses.
**Non-blocking and correctly overridden — the second batch running into this.** Recorded for Ron alongside
the batch-127 instance; a per-prefix exception may be worth adding if it recurs.

### Batch 129: content worth carrying

- **A shared block explains that the `L` suffix means clinical practice with patients**, not a campus
  skills laboratory — Ron's suffix rule applied to a fourth prefix.
- **`NUR3026L` carries the first-clinical guidance students most need**: *"I don't know" is the
  professional answer*; you may not perform a skill you have not been checked off on; **placement paperwork
  takes longer than expected and delays graduation**; HIPAA applies personally from day one; **report every
  exposure immediately**.
- **`NUR3505`/`NUR3505L` carry Florida-specific mental health law** — the **Baker Act (Ch. 394)** and
  **Marchman Act (Ch. 397)** — plus the correction that **asking directly about suicide does not plant the
  idea**, restraint and seclusion as regulated last resorts, and **988**.
- **`NUR4445`/`NUR4445L` state the maternal mortality disparity plainly**: US maternal mortality is high
  for a wealthy country and **markedly worse for Black women**, with **not being listened to a documented
  contributing factor** — making it a clinical safety behaviour to take a patient's report of her own
  symptoms seriously. Also **mandatory reporting** (Florida Abuse Hotline 1-800-96-ABUSE) and that
  **children compensate then decompensate abruptly**.
- **`NUR4216L` treats escalation as the assessed competency** — *"I am concerned about this patient" is a
  complete and sufficient reason to call*, and **hierarchy has killed patients**.
- **`NUR4615`/`NUR4615L`/`NUR4636L` carry the community-nursing reframe**: **"non-compliant" is usually a
  failure of assessment**, and **Florida is a Medicaid non-expansion state**, so the coverage gap is
  something a community nurse meets constantly — with the actual referral routes named.
- **`NUR4257L` documents the preceptored capstone honestly** — progressive independence is not permission
  to exceed scope, **poor preceptor placements happen and should be raised early**, and it functions as an
  extended job interview.
- **A shared final-block block covers the licensure endgame**: start the Florida Board of Nursing
  application **before graduating**, and **transition shock is documented and normal**.

### Batch 130 — UWF studio art: foundations, painting, drawing, print, digital (12)

`ART2201C`, `ART2203C`, `ART2602C`, `ART3213C`, `ART3442C`, `ART3504C`, `ART3505C`, `ART3613C`,
`ART4332C`, `ART4333C`, `ART4506C`, `ART4520C`. **First studio prefix in the corpus.** ART has 22 queued
rows; **10 remain** (ceramics, sculpture, capstone) plus one orphan half.

### ✅ The studio contact-hour convention, and it lands on the C-suffix expectation

**All 3-credit studio C courses derived at 60 contact hours** — four studio hours a week across fifteen
weeks. Two independent supports:

1. **The Florida convention for an integrated `C` course** (~60 hours for 3 credits), recorded in
   `Tools/CLAUDE.md`.
2. **The only studio figure published anywhere in this corpus** — Daytona State's **ART1331C, "four studio
   hours"**, captured during the DSC build.

**✅ All 12 validated clean with no warnings**, which is itself informative: the validator's C-suffix
heuristic expects ~60 hours for 3 credits, so **the studio convention and the C convention agree**. That
is a contrast with MLS (batch 127) and NUR (batch 129), where the same heuristic fired incorrectly.

**Every guide labels 60 as a floor** and states why: studio practice expects substantial work outside the
scheduled session, and **open-studio hours are part of how the work gets made**.

### ⚠⚠ ANOTHER catalog contradiction — `ART4333C` excludes credit with its own prerequisite

**UWF publishes `Prerequisite: ART 4332C` on ART4333C, and also states "Credit may not be earned in both
ART 4332C and ART 4333C."** As printed, **the prerequisite is a course whose credit cannot be held
alongside this one.**

Reported verbatim with the anomaly named, not corrected. **Fourth catalog-internal inconsistency in the
corpus**, after `EEL3111L`'s phantom exclusion rule, `MLS4631C`'s `CHM 2022`/`2202` transposition, and
`NUR3026`/`NUR3805`'s circular prerequisite. **The treatment is settled and now applied consistently:
reproduce as published, name the anomaly, refuse to guess, direct the student to the department.**

**⚠ Four anomalies across four prefixes is a rate worth noting** — roughly one per prefix worked at UWF.
It is not carelessness on any single entry; **it is what happens when a catalog carries thousands of
cross-references maintained by hand**.

### ⚠⚠ TWO different UWF courses share ONE statewide title

The statewide inventory titles **both `ART4506C` and `ART4520C` as "Advanced Painting."** UWF publishes
them as *Painting IV - Advanced* and *Painting: Personal Directions* — **different courses, different
prerequisites** (ART4506C requires ART3505C; ART4520C requires nothing), **and different repeatability**
(ART4520C repeats to 9 sh).

**This is the inverse of the `NUR4286` / `NUR4826` case.** There, one number carried two subjects. Here,
**two numbers carry one statewide name** — so an evaluator matching on title cannot distinguish them, and
a student can take what they believe is the same course twice. Both guides state it explicitly.

### ⚠ Numerals do not correspond between SCNS and UWF

`ART3505C`: the statewide inventory calls it **"Painting II"**; UWF publishes **"Painting III-Advanced."**
**Matching these courses by numeral produces the wrong answer** — the same failure mode recorded for
`NUR4216` (SCNS "Nursing Process V" vs UWF "Person Centered Care III"). **Rule: never map a sequence by
its numeral across institutions.**

### ⚠ Repeatability is normal here, and it is the first prefix where that is true

Studio courses repeat: `ART3442C` **up to 12 sh** (the largest in the corpus), `ART3613C`, `ART3714C`,
`ART4520C`, `ART4632C`, `ART4712C` each **up to 9 sh**. The content is a studio context rather than a
fixed syllabus, so a student returns to develop a body of work.

**Each guide states the three consequences**: catalog repeatability is not degree-audit applicability;
**repeated enrolments interact with financial-aid rules that were not written with studio practice in
mind**; and a transfer evaluator may not expect it.

### ⚠ Content varies by instructor — stated by UWF, not inferred

`ART3613C` **Digital Multimedia** lists possible emphases spanning *video art, streaming, emerging
technology, installation, programming and/or robotics* — **"to be determined by instructor."** Those are
not interchangeable skill sets. The guide tells students to ask what a section actually covers, and notes
that a repeated enrolment may cover entirely different ground.

### Batch 130: content worth carrying

- **A shared studio-safety block** is the most substantive addition. Art materials are chemicals and the
  hazards are real: **solvent vapour as chronic rather than acute exposure**; cadmium, cobalt and lead in
  artists' colours; **silica dust as irreversible lung damage where a dust mask is not respiratory
  protection and dry sweeping makes it worse**; and **oil- and solvent-soaked rags self-igniting**, a
  documented cause of studio fires.
- **`ART3442C` carries the heaviest safety content in the batch** — printmaking is the most chemically
  hazardous studio in most art departments. Acid handling (**always acid into water**), knowing where the
  eyewash and neutraliser are *before* starting, aquatint dust, press crush injuries, and **regulated
  disposal — spent acid and solvent do not go down the drain**.
- **A shared critique block** treats critique as method rather than verdict, and gives the actual
  technique: **describe what you see, then what it does, then whether that serves the work's apparent
  intention** — because "I like it" and "I don't like it" are equally useless.
- **`ART4332C` documents life-studio professional conduct**, which no other guide type needs: **no
  photography or recording of any kind**, do not discuss the model's body or address them during a pose,
  and **raise a religious or personal concern about working from the nude figure before enrolling rather
  than mid-term**.
- **`ART2602C` treats copyright as a working constraint** — fair use is a defence rather than a permission,
  educational use is not automatically fair use, and **class work becomes portfolio work at which point
  sourced material that passed critique may not pass publication**. It also flags that **generative AI
  policies vary sharply by course and should be confirmed before use**.
- **The careers block is honest about the economics**: fine artists are **predominantly self-employed with
  irregular income**, very few studio graduates support themselves from selling their own work, and **a
  plan that assumes gallery income is a plan without a foundation**. Balanced against real Florida
  destinations — **Walt Disney Imagineering and Universal Creative in Orlando** hire sculptors, painters,
  model-makers and scenic artists, and the **Orlando simulation and training cluster** hires 3D and digital
  artists.
- **⚠ K-12 art teaching in Florida requires state certification that a studio degree alone does not
  provide** — flagged because students routinely assume otherwise.
- **A shared independent-study block** for the 4000-level courses names the actual failure mode: without a
  weekly assignment, **students who wait to be told what to do produce very little**, and work concentrates
  into the fortnight before the final critique.
- **Transfer note specific to studio art**: a receiving programme may accept the credit and still require
  its own portfolio review — **the portfolio, not the transcript, is what moves you between art
  programmes**, so photograph everything before it leaves your hands.

### Batch 131 — UWF ceramics, sculpture and capstone (10), and **ART closes**

`ART3760C`, `ART3762C`, `ART3789C`, `ART4767C` (ceramics), `ART3713` (orphan), `ART3714C`, `ART4712C`
(sculpture), `ART4632C`, `ART4801C`, `ART4800` (capstone and professional practice). `ART3713C` then
skipped. **ART: 40 pushed, 4 skipped, 0 queued** — the fifth prefix to close, after ANT, EEL, MLS and NUR.

### ⚠⚠ TWO more SCNS titles naming different subjects — the pattern is now systematic

Batch 128 found `NUR4286` (SCNS *Gerontological Nursing* → UWF quality and safety) and `NUR4826` (SCNS
*Ethics* → UWF leadership). ART adds two more:

| Course | SCNS title | UWF title | Relationship |
|---|---|---|---|
| `ART3789C` | **World Ceramics** | Advanced Ceramics: Mold Making and Slip Casting | **different subject** |
| `ART4800` | **Criticism Seminar** | Portfolio | **different subject** |
| `ART4632C` | Building a Web Portfolio | Digital Design Studio Senior Project | much broader |
| `ART3714C` | Sculpture: Casting | Advanced Sculpture | broader |
| `ART4712C` | RI: Advanced Sculpture | Sculpture: Personal Directions | drops an "RI" designation |

**Four prefixes now show this**, and `ART3789C` and `ART4800` are as stark as the NUR pair: a student
expecting a survey of world ceramic traditions gets a technical mold-making studio, and one expecting art
criticism gets professional practice and documentation. **Each guide states plainly that the course should
not be assumed to satisfy a requirement named by the statewide title.**

**⚠ These are candidates for the `-SCNS` / `-<INST>` split** under the rule recorded in `Tools/CLAUDE.md`.
Whether they warrant it depends on the SCNS catalog definition, which is **still outstanding from Ron** —
added to the open-cases table there.

### ⚠ `ART4800` is the first ART course to take the LECTURE convention

**No `C` suffix**, because it is a seminar and professional-practice course rather than a studio one.
Derived at **45 hours (15/credit)** rather than the 60 used across the rest of the prefix, and the guide
says why. **Validated clean** — the validator's C-heuristic correctly did not fire on a non-C course.

**The rule for studio prefixes: check the suffix before applying the studio convention.** A prefix being
studio-dominated does not make every course in it a studio course.

### ⚠ A catalog typo, noted and not propagated

`ART3789C` reads *"This course will five students the opportunity"* — plainly "give". **Not reproduced as
an anomaly in the guide** (unlike the structural contradictions), because a single obvious word-level typo
carries no advising consequence. **Recorded here to keep the distinction clear: structural contradictions
get flagged to the student; typographical slips do not.**

### Batch 131: content worth carrying

- **`ART3760C`, `ART3762C`, `ART3789C` and `ART4767C` share a ceramics safety block** built around the
  hazard that defines the discipline: **crystalline silica**. It states that exposure is **cumulative and
  low-level rather than dramatic**, that **dry-sweeping makes the air worse than leaving it**, that **a
  domestic vacuum blows fine dust straight through the bag**, and that **a paper dust mask is not
  respiratory protection**. Dry glaze weighing is named as the highest-risk stage, with barium, lithium and
  manganese called out.
- **⚠ It also tells students not to wear studio clothes home unwashed** — the practical route by which
  silica leaves the studio, and something rarely said.
- **`ART3789C` carries the plaster-in-clay problem**, which is specific and consequential: a plaster
  fragment **absorbs moisture, expands in firing and blows a crater out of the work — possibly weeks
  later**, after surviving bisque. Hence separate tables, tools and buckets, and **never pouring plaster
  down a drain**. It also warns that **plaster generates heat as it sets and must never encase any part of
  a person**.
- **`ART3713`, `ART3714C` and `ART4712C` share a sculpture shop-safety block** — the highest injury-risk
  studio in an art department. **Never work alone with powered equipment**; **gloves near rotating
  equipment are a hazard rather than a protection**; stone and concrete dust carries the same silica risk
  as ceramics; **resins can sensitise after months of uneventful use**; and **lifting and rigging injure
  more sculptors than tools do** — so plan how a work will be moved *before* making it that big.
- **`ART3713` carries the life-modelling conduct block** in the same form as `ART4332C`'s: no recording of
  any kind, do not address the model during a pose, and **raise a personal or religious concern before
  enrolling rather than mid-term**.
- **`ART3714C`'s description is unusual and was worth quoting**: UWF explicitly names *environmental
  responsibility* and *health concerns* as part of material selection, and *implications for authorship*.
  **That is a serious position rarely stated in a studio catalog entry**, and the guide treats material
  choice as an ethical decision rather than only an aesthetic one.
- **`ART4767C` documents ceramic 3D printing honestly** — printing in clay is not printing in plastic: the
  material sags, extrusion is coarse, layer lines are structural, and the print must survive drying and two
  firings. **The interesting work comes from those constraints rather than from hiding them**, and a
  student expecting a finished object from a printer will be disappointed by every print. UWF's naming of
  **Rhino** is noted as genuinely transferable beyond ceramics.
- **A shared professional-practice block** across the three capstone courses states what studio degrees
  frequently omit: **documentation is the single highest-return professional skill** because nearly every
  opportunity is decided from images; **read what you sign**, since copyright is yours by default and can
  be signed away by a clause; **beware pay-to-play** where the business model is artists' money; and
  **keep an inventory from now**, because it is impossible to reconstruct later.
- **`ART4800` states the documentation standard bluntly**: *badly photographed good work loses to well
  photographed adequate work*, the standard is **forensic rather than artistic**, and **submissions are
  routinely rejected on file-format compliance alone without the work being seen**.

### Batch 132 — UWF health sciences: public health and health promotion core (12)

`HSC2100`, `HSC2622`, `HSC3032`, `HSC3510`, `HSC3535`, `HSC4211`, `HSC4404`, `HSC4500`, `HSC4551`,
`HSC4581`, `HSC4633`, `HSC4730`. HSC has 19 queued rows; **7 remain** plus 2 C-suffix orphans.

### ✅ Rule 3o confirmed a second time — HSC is a light-touch health prefix

The handoff warned against assuming a health prefix repeats MLS's patterns. It does not:

| | MLS | NUR | **HSC** |
|---|---|---|---|
| "Permission is required" | near-universal | **0** | **0** |
| Fee notices | 16 | ~0 | **2 across 55 courses** |
| Co-requisite blocks | yes | extensive | **0** |
| Prerequisites | 32/51 | dense in the cohort track | **19/55** |

**Three health prefixes, three different structures.** MLS is cohort-gated with fees; NUR is cohort-chained
without gating; **HSC is an ordinary lecture prefix with almost no structural constraint at all** — only
one course in this batch (`HSC3510`, requiring `STA2023`) publishes a prerequisite. **Derived at the plain
lecture convention of 15 hours per credit; all 12 validated clean.**

### ⚠⚠ Title drift again, and one case crosses a disciplinary boundary

Nine of the nineteen queued HSC rows carry a different UWF title. Most are rewordings, but one is
substantive:

| Course | SCNS title | UWF title |
|---|---|---|
| `HSC3032` | **Foundations of Public Health** | **Foundations in Health Education** |
| `HSC4730` | Public Health Research | Research Methods and Evaluation in Health Promotion |
| `HSC3510` | Healthcare Research and Statistics | Data Analysis in the Health Sciences |
| `HSC4551` | Survey of Human Diseases | Communicable and Degenerative Diseases |
| `HSC4211` | Health and Human Ecology | Human Environmental Health |
| `HSC4633` | Issues in Health | Current Issues in Health Promotion |
| `HSC2100` | Personal and Community Health | Personal, **Family** and Community Health |

**`HSC3032` crosses a real disciplinary boundary.** Health education and public health are related fields
with **different credentials (CHES vs CPH) and different graduate routes**. A student expecting an
introduction to public health gets an introduction to the health education profession. **A shared block in
every guide states the distinction and warns against assuming a course satisfies a requirement written
against the other field's name.**

**⚠ `HSC3510` is the sharper practical case**: it is analysis and visualisation, while the *research
methods* content sits in `HSC4730`. A student matching the SCNS title "Healthcare Research and Statistics"
could take it expecting research design and get neither.

### ⚠⚠ Two more `-SCNS` split candidates from the same prefix

`HSC3102`: SCNS **"Perspectives in Health"** → UWF **"Health Science Essentials of Behavior Analysis"**.
`HSC4720`: SCNS **"Behavior Modification in Health Coaching"** → UWF **"Methodology in Applied Behavior
Analysis in Health"**.

**Both are in the remaining seven, not yet written.** The first looks like a genuine different-subject case
— a generic perspectives title against a specific ABA course — and **UWF appears to run an applied
behaviour analysis track inside HSC**, which the statewide titles do not reveal. **Assess against the
`-SCNS` rule when writing them.**

### ✅ The credential anchor for this prefix: CHES

Each guide carries a shared block on the **Certified Health Education Specialist** credential from NCHEC —
the health-education counterpart of NCLEX for nursing and ASCP for laboratory science, and the fourth
credential anchor established in this corpus.

**⚠ The advising point that matters: CHES eligibility is assessed on course *content* against NCHEC's Areas
of Responsibility, not on course titles or numbers.** So the guides tell students to **keep syllabi and
catalog descriptions for every health course**, because that is the evidence a credentialing body wants —
and to **check eligibility before the final year**, since adding a course is far easier than remediating
after graduation.

### Batch 132: content worth carrying

- **A shared social-determinants block** states the field's central and least comfortable finding: **medical
  care is a modest contributor to population health outcomes** compared with income, housing, education and
  environment. It also names the practical consequence — **"non-adherence" is frequently a description of a
  barrier the programme did not assess** — and that **Florida is a Medicaid non-expansion state**, so the
  coverage gap is something community health workers meet constantly.
- **A shared evidence block** covers the causal errors this field is prone to: association versus
  causation, **confounding by socioeconomic position that ends up blaming the affected population**, and
  **the ecological fallacy** — two things common in the same county does not mean the same people have both.
- **`HSC4500` (Epidemiology) carries the quantitative core** — age standardisation as non-optional when
  comparing populations, **predictive value depending on prevalence**, and that **relative risk without
  absolute risk is the standard way a small effect is made to sound large**.
- **`HSC4730` and `HSC4581` together document why health promotion evaluation fails**: attendance is not an
  outcome; **define the measure before implementing, not after**; **a pre-post change without a comparison
  group is weak evidence** because regression to the mean flatters any programme recruiting people at their
  worst; and **education alone rarely changes behaviour** — environmental and default changes outperform
  information, consistently.
- **⚠ The QI-versus-research boundary is decided by the review board, not the investigator**, and
  retrospective approval does not exist.
- **`HSC4404` carries the Florida disaster realities** already established in the NUR build and extends
  them: **A-team/B-team arrangements requiring staff to remain on site through a storm**, Florida's
  documented fatal failures of facility emergency planning, special needs sheltering, and that **mass
  casualty triage inverts normal clinical priorities**. **FEMA IS-100 and IS-700 are named as free,
  short, and genuinely expected credentials.**
- **`HSC4211` supplies Florida-specific environmental health**: a **shallow, permeable drinking-water
  aquifer**, red tide and harmful algal blooms, **heat as a present occupational hazard** for the
  agricultural and construction workforce, locally acquired dengue and malaria, and **EPA EJScreen** for
  neighbourhood-level exposure data.
- **`HSC2622` includes the critiques global health makes of itself** — its origins in colonial tropical
  medicine, and **the documented concerns about short-term volunteer trips**: untrained students performing
  tasks they could not legally perform at home, displacement of local providers, and **benefit accruing
  mainly to the volunteer**. The guide tells students considering one to ask **who asked for it and what
  happens when you leave**.
- **`HSC3535` (Medical Terminology) is framed as a patient safety course**, not a vocabulary one — the
  **ISMP error-prone abbreviations list** is named, along with why **"U" for units and trailing zeros have
  caused deaths**. It also says plainly that **word-building beats memorisation** and that **twenty minutes
  daily beats three hours weekly**.
- **⚠ Teaching health in Florida K-12 schools requires state teacher certification** that a health science
  degree alone does not provide — flagged because students routinely assume otherwise.
- **An honest note on entry-level work**: health education roles are frequently **grant-funded with fixed
  terms, where continuation depends on the grant rather than on performance**.

### Batch 133 — HSC behaviour analysis, pharmacology, nutrition and orphans (7), and **HSC closes**

`HSC3102`, `HSC3147`, `HSC4104`, `HSC4572`, `HSC4720`, plus orphan additions `HSC3555` and `HSC4143`.
`HSC4143C` and `HSC3555C` then skipped. **HSC: 29 pushed, 4 skipped, 0 queued** — the sixth prefix to
close, after ANT, EEL, MLS, NUR and ART.

### ⚠⚠ A hidden programme track the statewide titles do not reveal

`HSC3102` and `HSC4720` form an **applied behaviour analysis sequence** inside UWF's health sciences
prefix — `HSC4720` requires `HSC3102`. **Neither statewide title says so:**

| Course | SCNS title | UWF title |
|---|---|---|
| `HSC3102` | **Perspectives in Health** | **Health Science Essentials of Behavior Analysis** |
| `HSC4720` | Behavior Modification in Health Coaching | Methodology in Applied Behavior Analysis in Health Science |

**`HSC3102` is a genuine different-subject case** — a generic perspectives title against a specific
introduction to ABA — and is **added to the `-SCNS` open-cases table** in `Tools/CLAUDE.md`. `HSC4720` is
significant drift rather than a different subject: both titles concern behaviour change in health, but
UWF's is substantially more technical (single-subject experimental design rather than coaching practice).

**This is the third prefix where a hidden track surfaced only from the prerequisites** — after MLS's
Professional Track and NUR's dual routes. **The detection method is the same each time: read the
prerequisite structure, not the titles.**

### ⚠⚠ An HSC course taught by a DIFFERENT COLLEGE

`HSC3555 Pathophysiology` is published **through the Department of Biology, College of Science and
Engineering** — not the College of Health, which carries every other course in the prefix.

**The consequences are real and are stated in the guide**: the prerequisites are biology prerequisites
(`(BSC1085 AND BSC1086) OR PCB3097L OR PCB4098 OR PCB4703`), and **the approach is likely to be more
biological and less clinical** than a pathophysiology course taught inside a nursing or allied health
programme. **A student should confirm which version their programme requires.**

**⚠ Worth checking in every prefix from now on**: the department line in a UWF entry is not decoration, and
a cross-college placement changes what a course is.

### ⚠ Two more course-pair distinctions worth documenting

- **`HSC3147` (mechanism) versus `NUR3145`/`NUR3095` (administration).** UWF publishes pharmacology in
  both prefixes with different orientations: HSC teaches *why drugs work*, NUR teaches *safe
  administration* — dosage calculation, the rights, high-alert safeguards. **The guide says plainly that
  one does not substitute for the other**, and that the administration course is the one preventing the
  errors that harm patients.
- **`HSC4572` (nutrition science) versus medical nutrition therapy.** The SCNS title is *Clinical
  Nutrition*, which implies individualised therapy — **the regulated scope of practice of a registered
  dietitian, licensed in Florida**. UWF's course is nutritional science and population nutrition. **The
  guide states the scope boundary explicitly**, including that the professional answer to "what should I
  personally eat for my diabetes" is a referral.

### Batch 133: content worth carrying

- **`HSC3102` and `HSC4720` share an ABA ethics block that engages the field's live controversy rather
  than omitting it.** The BACB code is enforceable; consent and assent are central because **procedures are
  frequently applied to people who cannot easily refuse**; and **autistic self-advocates have raised
  substantive criticisms of ABA as historically practised** — compliance-focused goals, suppression of
  harmless behaviour such as stimming, and reported long-term harm. **These are recorded as part of the
  field's current debate rather than as external noise**, with the direction that a student entering the
  area should engage with them directly.
- **⚠ It also names where the ethics actually lives**: goal selection — whether a behaviour should be
  changed at all, and who benefits — is prior to how to change it.
- **`HSC4720` documents single-subject experimental design** as a genuinely different research logic from
  the group-comparison approach taught elsewhere in health research: the participant is their own control,
  and **visual analysis rather than a significance test is the standard**.
- **`HSC4143` (Drugs in Society) states which prevention approaches lack evidence and why they persist** —
  scare-based and information-only programmes are cheap, popular with adults, and feel like action, while
  **approaches targeting skills, norms and environment have better evidence**. It notes that **harm
  reduction is evidence-based and politically contested**, and that students should distinguish empirical
  objections from moral ones. **Person-first language is framed as a professional standard with measurable
  effects, not delicacy.**
- **`HSC4104` (Stress Management) carries the batch's most important structural honesty**: individual
  coping techniques address the *response*, not the *stressor*. **Job strain research is specific — high
  demand with low control predicts poor outcomes, and the effective intervention is increasing control, not
  teaching the worker to relax.** Framing structural stress as an individual coping deficit is named as a
  documented failure mode of workplace wellness programmes.
- **⚠ It also states the scope limit**: the course does not qualify anyone to provide mental health
  treatment, and **attempting to counsel someone is outside a health education role** — recognition and
  referral is the competency.
- **`HSC4572` explains why nutrition evidence is weaker than it sounds** — largely observational,
  unreliable dietary recall, **single-nutrient reasoning that repeatedly fails when isolated into
  supplements**, and widespread industry funding. It adds the point students most need: **guidelines
  changing is the process working**, and treating each revision as proof that "they keep changing their
  minds" mistakes science for pronouncement.
- **`HSC3147` frames pharmacokinetics as the thing that explains apparently arbitrary clinical detail** —
  why a drug is given three times a day, why liver disease changes a dose, why one new prescription can
  destabilise a stable regimen.

### Batches 134-135 — PCB Process Biology (19 guides), and **PCB closes**

Five lecture+laboratory families written whole (`PCB3043`/`L` ecology, `PCB3063`/`L` genetics,
`PCB3103`/`L` cell biology, `PCB4233`/`L` immunology, `PCB4524`/`L` molecular biology, `PCB4723`/`L`
comparative animal physiology), plus `PCB3097L`, `PCB4028`, `PCB4673`, `PCB4841`, `PCB4870` and orphan
lectures `PCB4253` and `PCB4315`. Then seven rows skipped. **PCB: 24 pushed, 7 skipped, 0 queued** —
the seventh prefix to close, after ANT, EEL, MLS, NUR, ART and HSC.

### ⚠⚠⚠ Ron's suffix rule, found in the wild: `PCB3097L` is an L-suffix course that is not a laboratory

`PCB 3097L Introduction to Human Anatomy Laboratory` is **3 semester hours**, and UWF's own description
says the structure-function theme runs **"within both lecture and laboratory."** It is an **integrated
lecture-and-laboratory course carrying an `L` suffix** — functionally what a `C` suffix denotes elsewhere.

**This is the clearest instance yet of the principle Ron stated**: SCNS offers a limited set of suffix
options, and departments fit real courses into the nearest available designation. **The suffix records an
administrative choice; the description records the course. When they disagree, believe the description.**

Handled by:

- **Hours derived on the integrated convention** — 60 for 3 sh — **not** the 45/credit laboratory rate the
  suffix implies. Had the suffix been trusted, the figure would have been 135 hours, which is absurd for
  this course.
- **A dedicated section in the guide** explaining the mismatch, its three practical consequences (full
  3-credit workload; no separate lecture to enrol in; a receiving institution comparing suffixes rather
  than reading descriptions may misjudge it), and the advice to **send the catalog description, not just
  the number, when transferring it**.

**⚠ Standing check added**: when an `L`-suffix course carries more than 1-2 semester hours, read the
description before deriving hours. The suffix is not evidence of structure.

### ⚠⚠ A permission requirement my pre-prefix grep missed

The standing pre-prefix scan greps for **"Permission is required"**. `PCB 4233L` publishes **"Special
permission required. Permission granted on the basis of fulfilling prerequisite."** — different wording,
**zero hits on the standing pattern**, and the scan reported 0 permission markings for the whole prefix.

**Fix**: the pre-prefix scan must grep case-insensitively for **`permission`** alone, not for a fixed
phrase. Catalog language is not standardised even within one institution's own catalog.

**The finding itself is unusually good news for students** and is written up as such: unlike a permission
gate that hides a selective process, **this one states its own criterion** — meet the prerequisite and
permission follows. Almost certainly a bench-capacity limit rather than selectivity.

### ⚠⚠ The reverse case: `PCB4870` publishes a prerequisite WAIVER

`PCB 4870 Sensory Biology` states: **"Prerequisite is PCB 3063 (Genetics), however students may obtain
department permission to take the course without the specified pre-requisite."**

**This is the inverse of every permission marking found so far** — the department is *opening* a door the
prerequisite field would otherwise close. The reason is visible in the description: UWF names **psychology,
marine biology and biomedical science** among the intended audiences, students who may never take genetics.

**The guide states both halves**: the waiver exists and must be actively requested before registration
opens; and **it removes an administrative barrier, not the underlying content** — a student with no cell
biology background will still find the mechanism sections hard.

### ⚠⚠⚠ `PCB4315` is a study-abroad course, and the catalog says so in one clause

`PCB 4315` — queued as **"Marine Ecology"**, published by UWF as **"Tropical Marine Ecology"** — delivers
its content **"through a field experience in the Bahamas."**

**That single clause changes everything about how a student must plan for this course**, and none of it is
stated elsewhere in the entry. The guide sets out, explicitly, what UWF does not:

- **A valid passport is required**, and processing takes weeks to months — start before registering.
- **Expect a programme fee beyond tuition.** UWF publishes no amount, so the department or study abroad
  office is the only reliable source. **Ask for the total** — travel, accommodation, meals, boat/diving.
- **Ask whether in-water work requires SCUBA certification** with medical clearance; some tropical field
  courses are snorkel-based and some are not. Certification costs time and money outside tuition.
- **Study abroad scholarships exist and are underused**; deadlines are early.
- **The travel window may not match the term.**
- Health, insurance, and remote-site medical access.
- **And the honest framing**: this is a genuinely valuable differentiator for graduate admission and marine
  employment, **and the cost barrier is real and worth naming rather than glossing over**.

**⚠ Also a title-narrowing case** — "Marine Ecology" implies temperate and polar systems too; this course
is tropical reef, seagrass and mangrove. **Added to the `-SCNS` open-cases table.**

### ⚠ Two "Honors" titles in the inventory that are not honors courses at UWF

| Course | Inventory title | UWF title |
|---|---|---|
| `PCB4673` | **Honors** Evolution | Principles of Evolution |
| `PCB4841` | **Honors** Cellular Neuroscience | Journey to the Brain: Brain Development and Neuronal Synapse Communication |

Almost certainly another Florida institution offers these numbers through an honors programme and that
title entered the inventory. **A shared block in both guides states that the number is not inherently an
honors number, that honors credit depends on the offering institution designating the section, and that
this does not affect transfer of the course itself** — SCNS equivalency runs on number and content, with
the honors designation a separate institutional layer.

**`PCB4841` is also substantial title drift** — a student searching for "Cellular Neuroscience" will not
find "Journey to the Brain." Noted in the guide.

### ⚠ A concurrent graduate twin in a DIFFERENT prefix

`PCB 4028 Fundamentals of Pharmacology` is **offered concurrently with `BSC 5873`** — not a PCB 5xxx
number, which is the pattern every other concurrent pair in this prefix follows. **Searching PCB for the
graduate equivalent will not find it.** Written up as a reminder that prefix assignment is an
administrative judgement, and the same content can sit under different prefixes at different institutions
— or, as here, under two prefixes at the same one.

### ⚠⚠ A catalog entry that contains its own ethics statement

`PCB 4723L Comparative Animal Physiology Laboratory` publishes, inside the course description, that the
course **"requires the use of living animals, in most cases invertebrates,"** that they **"should be
handled carefully and treated ethically,"** and that each experiment is **"designed to provide maximal
educational value with minimal insult and stress."**

**No other course found in this catalog, in any prefix, carries an ethical statement in its description.**
Treated as meaningful: the department expects the framing to be part of the course.

**⚠ The guide handles one point carefully.** The catalog's parenthetical that invertebrates do not perceive
pain "as you and I interpret it" reflects a real distinction in nervous system organisation, **but it is a
question the literature is actively revising** — evidence for nociception and pain-like states in
cephalopods and decapod crustaceans has grown, and several jurisdictions now extend legal protection to
those groups. **The guide records the catalog statement as published and notes the science is not settled**,
then observes that the practical standard does not depend on resolving it: minimise number, minimise
distress, follow protocol, report problems, and note that vertebrate work falls under IACUC oversight.

**It also tells students to decide before registering**, not in week four.

### ⚠ A laboratory UWF says can be taken independently — while listing the lecture as a prerequisite

`PCB 3103L` says the laboratory **"is to complement the cell biology lecture, however can be taken
independently."** Its prerequisite field says **`PCB 3103*`**.

**Handled the way every catalog-internal contradiction has been handled in this project**: reproduce both
statements as published, name the tension, refuse to guess, and direct the student to the department —
with the practical reading (the asterisk means the lecture need not be finished first, which is close to
independence in scheduling terms) offered as reading rather than ruling. **This is the fifth
catalog-internal contradiction recorded**, after EEL3111L, MLS4631C, NUR3026/NUR3805 and ART4333C.

### PCB: where the fee is published is not where the fee falls

Confirmed across the prefix and worth stating as a pattern: **UWF frequently publishes a laboratory's fee
on the LECTURE entry.** `PCB3063`, `PCB4524` and `PCB4723` all say the fee "will be assessed for
corresponding lab" / "to the corresponding lab" — the fee is on the laboratory, announced on the lecture.
`PCB4233L` and `PCB4723L` publish their own fees directly, and `PCB4723L` carries **two** (Material and
Supply, plus Equipment).

**Consequence for guide-writing**: a fee section must be derived from reading the lecture and laboratory
entries *together*. Reading one in isolation produces a wrong answer in either direction.

### Batches 134-135: content worth carrying

- **`PCB3043L` is a field course, and the guide treats it as one** — UWF names campus and regional
  ecosystems, so the guide carries a full field-hazard section: **heat illness as the most likely serious
  problem**, venomous wildlife, ticks and tick-borne disease, water hazards, sting allergies, and that
  **collecting frequently requires a permit**. It also names the genuine advantage: the western panhandle
  puts coastal dune, salt marsh, estuarine, longleaf pine and freshwater systems within reach in one term.
- **It states what field ecology teaches that a lecture cannot**: that measurement is hard — counting
  organisms that move, hide or cannot be identified forces sampling design and detection probability to be
  confronted as practical problems rather than statistical abstractions.
- **`PCB3103L` is described by UWF as research-methods training**, not lecture demonstration — "fundamental
  training in the current techniques and methodologies used in research laboratories." **The guide says
  plainly that these are the skills that get a student into a research laboratory or a technician post.**
- **`PCB4233` names why immunology is hard and what to do about it**: the system is defined by interactions
  among many named components and almost nothing can be understood in isolation, so **learn the response as
  a narrative and attach the molecular detail to positions in it**. Drawing the pathway from memory is
  listed as a resource, with the test: if you cannot draw it without notes, you do not know it.
- **`PCB4524L` and `PCB4233L` both have near-empty catalog descriptions** — "Corresponding lab for
  Molecular Biology" and "Selected experiments in immunology." **Both guides state openly that the outcomes
  and topics are the standard technique set rather than a transcription, and that the syllabus governs.**
  The brevity is explicitly not read as the course being minor.
- **`PCB4028` carries a scope-of-practice section** on the model established in the health prefixes: this
  is molecular and cellular pharmacology, it explains mechanism, **it confers no authority to prescribe,
  dispense or administer** — all licensed activities in Florida — and **course knowledge should not be used
  to advise anyone, including family, about their own medication**.
- **`PCB4723` notes an accessibility fact worth knowing**: it is the *least* demanding prerequisite of the
  upper-division PCB courses — only `BSC 2011/L`, no chemistry — where cell biology, immunology and
  molecular biology all require organic chemistry or biochemistry. **More accessible than its 4000-level
  number suggests.**
- **`PCB4524` publishes a minimum grade** — "C- or higher required in prerequisite courses" — which is
  **not** the default across the catalog. The guide states the practical consequence: a passing grade is
  not automatically a qualifying grade, and repeating a prerequisite adds a term to a sequence this course
  sits late in.
- **`PCB4673` addresses the theory/`theory` equivocation directly**, since the course's own first-listed
  content is the evidence base. It also names the quietly employable part: **phylogenetic inference is now
  routine in epidemiology, conservation genetics, forensics and agriculture** — tracing an outbreak,
  identifying trafficked wildlife, and assigning a fish species to a market sample are the same computation.
  Nextstrain is listed as the demonstration that this is an operational science, not a historical one.
- **`PCB4870`'s guide leads with the format**, because a discussion seminar on primary literature cannot be
  caught up on: **there is no lecture to fall behind and recover from**, and arriving unread wastes the
  session. It names the format as the most valuable thing in the course — reading a paper critically,
  separating what was shown from what was claimed, and defending a reading aloud are graduate-level skills
  few undergraduate courses practise directly.
- **`PCB3097L` carries a donor-respect section**, hedged correctly: UWF's entry does not state whether
  cadaveric material is used and practice varies, so **the instructor's briefing is authoritative** — but
  where human material is used it comes from people who chose to donate, conduct rules are strict, and
  **students who find the laboratory difficult should tell the instructor and use UWF CAPS rather than
  avoiding sessions**.
- **`PCB4315` is written honestly about coral reef ecology having changed character within one academic
  generation** — once taught as the study of the most diverse marine ecosystem, now taught substantially
  as the study of one in severe documented decline. **UWF's emphasis on anthropogenic disturbance reflects
  that rather than avoiding it.**

### Batch 136 — MCB Microbiology (8 guides), and **MCB closes**

`MCB1000L`, `MCB2010L`, `MCB3020L`, `MCB4276` from the queue, plus orphan lectures `MCB1000`, `MCB2010`,
`MCB3020`, `MCB4203`. Then `MCB3020C`, `MCB4203C`, `MCB1000C` skipped. **MCB: 10 pushed, 4 skipped, 0
queued** — the eighth prefix to close.

### ⚠⚠⚠ THE FINDING: UWF runs THREE parallel microbiology routes, in two colleges and three departments

This is the largest instance of rule 3l (parallel routes) found anywhere in the build, and **no course
title says any of it.**

| Route | Courses | Home | Built for |
|---|---|---|---|
| Non-science majors | `MCB1000` + `MCB1000L` | **Medical Laboratory Sciences, College of Health** | UWF states: *"specifically designed to meet the microbiology pre-requisite requirement for the 4 year BSN degree."* Also meets **General Education in Natural Sciences**. |
| Health sciences | `MCB2010` + `MCB2010L` | **Medical Laboratory Sciences, College of Health** | Allied health. Clinically framed; host-parasite interaction and immunity included. |
| Biology majors | `MCB3020` + `MCB3020L` | **Biology, College of Science and Engineering** | **Upper division; the only route with chemistry prerequisites, and the only one that opens `MCB4203`.** |

Plus a fourth department: **`MCB4276` is taught by the Department of Public Health** — the only course in
the prefix outside MLS and Biology.

**The consequences are severe and are stated in all eight guides via a shared routes table:**

- **`MCB4203` requires `MCB3020` and accepts neither of the others.** A biology major who takes the health
  sciences course has not met the requirement.
- **The prerequisites reveal the level far better than the titles do.** `MCB3020` requires general
  chemistry with laboratory plus a full year of biology or A&P; **`MCB2010` and `MCB2010L` publish no
  prerequisite at all.** That gap *is* the difference between the routes.
- **All three carry the word "Microbiology"** — so a transfer evaluator reading titles rather than
  descriptions can accept a course that does not satisfy the requirement.
- **Only `MCB3020` is upper division**, which the `LEVELS` block now says explicitly for this prefix.

**⚠ Detection method, again**: read the prerequisite structure and the department line, not the titles.
Fourth prefix where this surfaced a hidden structure — after MLS, NUR and HSC.

### ⚠⚠ A reciprocal pair that uses DIFFERENT notations on its two halves

`MCB3020` lists the laboratory as an **asterisked prerequisite** (`MCB 3020L*` = prior or same term).
`MCB3020L` lists the lecture in an explicit **`Co-requisite:` field** (conventionally the stricter same-term
form).

**Every other reciprocal pair found in this catalog uses the same notation on both sides.** The practical
effect is identical — take them together — but the asymmetry is recorded rather than smoothed over, with
the note that the registration system is what enforces it.

### ⚠⚠ And the opposite: `MCB2010`/`MCB2010L` are NOT bound at all

**Neither entry publishes a prerequisite or a co-requisite.** The description says the laboratory
complements the lecture; nothing formally ties them.

**This is the only unbound lecture/laboratory pair found in the prefix**, and it is a genuine registration
hazard: `MCB1000L` names `MCB1000*`, and the 3020 pair binds both ways, so a student reasonably expects the
system to catch the omission. **It will not.** A student can enrol in the lecture, overlook the laboratory,
and discover a term later that their programme required both. **Stated plainly in both guides.**

### ⚠⚠⚠ The BSN prerequisite claim — stated, then immediately qualified

`MCB1000`'s description is unusually direct: **"specifically designed to meet the microbiology pre-requisite
requirement for the 4 year BSN degree."** Both `MCB1000` guides take it at face value **for UWF's own
nursing programme** and then say what the catalog does not:

- **It is not a guarantee for anyone else's programme.** Florida nursing programmes name their microbiology
  prerequisite differently — **many name the integrated `MCB2010C`**.
- **Catalog year matters as much as institution**; students are held to the year they entered under.
  **Get the answer in writing against your own catalog year.**
- **Most programmes require the laboratory as well**, plus a minimum grade (commonly C or better) and
  frequently a recency limit of five to seven years. **A passing grade is not automatically a qualifying
  grade, and an old one may not count at all.**
- **Nursing admission in Florida is competitive and prerequisite grades are the ranking mechanism** — this
  course is part of the application, not a box to clear.

**⚠ This is directly relevant to the career-pathways direction.** It is a worked example of constraint 4 in
`CIATLE-REPO/CLAUDE.md`: the course transfers fine, and **transferring fine is not the same as qualifying**.

### ⚠ `MCB4203` has no laboratory and no integrated form at UWF

Unlike the other three lecture courses in the prefix, `MCB4203 Microbes & Disease` has **no paired `L` and
no `C`**. Other Florida institutions do run an integrated `MCB4203C` (8 institutions), so **transfer in
either direction is not a like-for-like match** — stated in the guide, with the practical alternatives for
a student wanting laboratory work in pathogenic microbiology at UWF.

### ⚠ Fee notices are not uniform within the prefix — check each entry

`MCB1000L` and `MCB3020L` both publish a Material and Supply Fee. **`MCB2010L` publishes none**, despite
being the same kind of course in the same department. The `fees()` helper now emits an explicit
*"UWF publishes no fee notice on this course"* block rather than silence, since the absence next to two
siblings that do carry one is informative. **Do not generalise a fee across a prefix** — the same lesson
as the batch-119 error, in a new form.

### Batch 136: content worth carrying

- **`MCB4276 Epidemiology` is the batch's most substantial guide (24.2k)** and is written as the bridge
  between microbiology and public health, because that is what its departmental placement makes it.
- **It names the credential landscape honestly**: most epidemiologist posts expect an **MPH**, and this
  course is preparation rather than substitute — **but entry-level routes that need no graduate degree are
  real** (disease intervention specialist, epidemiology technician, surveillance analyst at county health
  departments), and they are the best way to find out whether the field suits you before committing.
  **Infection prevention** is named as a substantial and under-advertised career.
- **It warns that the course is quantitative** and identifies the two ideas worth deliberate effort:
  **confounding** (an association can be entirely real and entirely misleading about cause) and
  **predictive value** (**a highly specific test can still produce mostly false positives when disease is
  rare** — counterintuitive, consequential, routinely misunderstood in public discussion of testing).
- **It names the ethical tensions rather than avoiding them**: isolation, quarantine, mandatory reporting
  and vaccination requirements restrict individual liberty for collective benefit, and **each is a genuine
  trade-off, not an obvious answer**. It adds that **public trust is an epidemiological variable, not a
  side issue** — control works through voluntary compliance far more than enforcement — and that burden is
  not evenly distributed, so treating housing, occupation and ability to isolate as background produces
  incomplete analysis.
- **Florida is used as real case material throughout**: locally acquired dengue and malaria, *Vibrio
  vulnificus* after storms and flooding, year-round mosquito activity, and travel-associated importations
  through the state's major airports.
- **`MCB3020`'s two-clause description understates the course**, so the guide says so and derives content
  from the prerequisite structure. **The clause "relationships of microorganisms to total environment" is
  flagged as load-bearing** — environmental, industrial and ecological microbiology belong in this route in
  a way they do not in the health sciences one. The guide makes the honest case for the discipline:
  **microbes run the planet's elemental cycles, and human disease is a small and recent corner of what they
  do.**
- **It also warns against textbook substitution**: Tortora and Bauman are good books for a different
  course and **do not carry the metabolic and ecological depth this one assumes**. Madigan's *Brock* is the
  level.
- **`MCB4203` is organised the way UWF scopes it** — explicitly excluding the host immune response, which
  is unusual and useful scoping, with a pointer to `PCB4233 Immunology` for the other half. The organising
  idea is stated as **the virulence factor**: what separates a harmless *E. coli* from a lethal one is
  acquired genes, not species — **learning pathogenesis as gene-encoded capability rather than as a list of
  diseases is what makes the course cohere**.
- **`MCB1000L` tells students the laboratory runs on the organism's schedule**, not the timetable's, and
  that culturing your own hands before and after washing is more persuasive than any lecture on hygiene.
- **`MCB2010L` (17 institutions, the widest adoption in the batch) carries parasitology explicitly** —
  UWF names protozoans and multicellular parasites — **which is the right choice for Florida**, where
  climate, standing water and travel volume keep parasitic and vector-borne disease clinically relevant in
  a way they are not in much of the country. CDC DPDx is listed as the identification reference.
- **All laboratory guides carry a microbiology-specific biosafety block** distinguishing it from general
  laboratory safety: **you are culturing live organisms that multiply**; aseptic technique protects both
  you and the experiment; everything that touched a culture is autoclave waste; **and students who are
  pregnant, immunocompromised, or living with someone who is should tell the instructor before the term** —
  not a bar to taking the course, but information the department can only accommodate if it has it.

### Batch 137 — ISM Information Systems Management (8 guides), and **ISM closes**

`ISM3116`, `ISM3323`, `ISM4113`, `ISM4320`, `ISM4321`, `ISM4400`, `ISM4545` from the queue, plus orphan
lecture `ISM3011`; then `ISM3011C` skipped. **ISM: 10 pushed, 2 skipped, 0 queued** — the ninth prefix to
close, and **the first non-science prefix in this run**.

### ⚠ A prerequisite that is a STANDING requirement, not a course

`ISM 3011` publishes: **"Completion of 45 hours of college course work is required prior to taking this
course."** No course is named.

**This is the first standing requirement found in the UWF catalog in this build**, and it is easy to
overlook precisely because it does not appear in a prerequisite chain the way `ISM 3011` does in every
other ISM entry. Consequences stated in the guide:

- **A first-year student cannot take it**, however capable — and therefore cannot begin the ISM sequence.
- **Transfer students must confirm how their credit counts toward the 45.** Dual enrolment, credit by
  examination and developmental coursework are treated differently by different institutions.
- **Business colleges commonly gate upper-division work this way**, sometimes alongside admission-to-the-
  major and a minimum GPA that the course entry does not name.

**⚠ Watch for these in every business, education and health prefix from here on.** A prerequisite field
containing no course number is still a prerequisite.

### ⚠⚠ A perfect star topology: one course gates the entire prefix

**Every undergraduate ISM course at UWF except `ISM3011` itself requires `ISM3011`** — `ISM3116`,
`ISM3323`, `ISM4113`, `ISM4320`, `ISM4321`, `ISM4400`, `ISM4481`, `ISM4483`. **Only `ISM3323` offers an
alternative** (`ISM 3011 OR COP 2253`, a programming route), reflecting that security recruits from both
business and computing.

**All eight guides carry a shared `HUB` block** saying this plainly: `ISM3011` is a **single point of
failure in a student's schedule**, there is no route around it, and it should be taken as early as
eligibility allows.

**⚠ Relevant to the career-pathways direction**: this is the cleanest prerequisite-graph shape found so far
— a hub with one alternate edge. Most prefixes are messier, but a pathway feature will need to represent
both this and the cohort-locked chains recorded in NUR and MLS.

### ⚠⚠⚠ Two title divergences that may be genuine subject differences

| Number | Statewide inventory | UWF | Assessment |
|---|---|---|---|
| `ISM4320` | **Applications in Information Security** | Legal, Ethical, and Human Aspects of Cybersecurity | **⚠⚠ Largest divergence in the prefix.** "Applications" implies applied technical work; UWF's course is explicitly the human, legal and ethical dimension and *states* its focus is the human element. **Added to the `-SCNS` open-cases table.** |
| `ISM4545` | **Visual Analytics I** | Business Analytics with AI | **⚠⚠ Significant drift, different centre of gravity.** Visualization is named in UWF's description but the frame is AI and machine learning. The **"I"** in the statewide title also implies a sequence UWF does not run. **Added to the table.** |
| `ISM3011` | Management Information Systems | e-Business Systems Fundamentals | Naming only — UWF's description is a standard MIS introduction. One guide. |
| `ISM4400` | Decision Support Systems | Decision Support and **Data Integration** Systems | Extension, not divergence. One guide. |

**A reusable `drift()` block was added** to the ISM writer, so any prefix with title divergence now gets a
consistent treatment: state both titles, assess whether it is naming or subject, and **give the same
practical advice every time — carry a syllabus, and search on the number rather than the name.**

### ⚠⚠ A cybersecurity sequence inside a BUSINESS prefix — and what it does not teach

`ISM3323`, `ISM4320` and `ISM4321` form a security sequence in the **Department of Business
Administration**. All three guides carry a shared block making the boundary explicit:

- **This is security *management*, not security *engineering*** — governance, risk, policy, law, human
  factors, incident planning. **It does not teach penetration testing, exploit development, malware
  analysis or network defence operations.**
- **Neither half is the "real" one** — organisations are breached through unpatched systems and untrained
  people in roughly equal measure, and **most security work in a large organisation is governance, audit
  and risk rather than hands-on-keyboard**. But a student wanting the technical career needs the technical
  courses and this sequence will not supply them.
- **Practical direction given**: ask early whether CS/IT technical electives can be taken alongside,
  because those prerequisite chains are long.

### ⚠ Regional context that materially changes this career: Northwest Florida is a defence region

A shared block in the three security guides records what a Pensacola-based student should know early:

- **NAS Pensacola, NAS Whiting Field, Eglin, Hurlburt Field and their contractors** make cybersecurity
  demand real and sustained in this region.
- **Many roles require a security clearance, which cannot be obtained on your own** — an employer must
  sponsor it and the process takes months, **so a sponsored internship is the usual on-ramp**. Knowing this
  early changes how a student approaches internships.
- **Clearance eligibility is affected by things students do not expect**: significant debt, foreign
  contacts, and drug use **including cannabis, which remains federally prohibited regardless of state
  law**. Recorded as fact, not as advice about how to live.
- **DoD 8140 (formerly 8570) makes CompTIA Security+ a common hard requirement** for defence cybersecurity
  roles — a genuine advantage to hold before graduating in this region.

### ⚠⚠⚠ The AI Integration section, finally load-bearing

Per `Tools/CLAUDE.md` section 7, AI Integration is written where the domain has substantively shifted.
**ISM is the first prefix in this run where that is unambiguous**, and it received two treatments:

- **A shared `AI_CORE` section in seven guides** covering where AI tools genuinely help in information
  systems work (code and SQL drafting, test data, documentation summary, first-draft requirements, '
  explaining error messages) and **where they fail specifically** — inventing functions and endpoints,
  producing code that runs and is subtly wrong, confident wrongness on anything niche or recent.
- **⚠⚠ The failure mode named as most important here: a wrong answer that looks right.** *A query that
  returns rows is not a query that returns correct rows.* Verify against known values; be careful with
  joins, filters, date handling and aggregation.
- **⚠⚠⚠ And the one with real-world consequences: never paste confidential, personal or regulated data
  into a public AI tool.** Named as **a common way early-career employees cause serious incidents**, with
  the note that *"I did not know"* is not a defence that helps anyone.
- **A dedicated `AI_CENTRAL` section for `ISM4545`**, where AI is the subject rather than a tool — covering
  bias reproduced at scale, **silent model drift**, why **accuracy is a poor metric for rare events** (a
  fraud model predicting "not fraud" every time can be 99% accurate and useless), explainability as a legal
  requirement in credit, insurance, employment and healthcare, and that **"we had the data" is not the same
  as "we were permitted to use it for this."**
- **The most valuable graduate skill is named as translation** — explaining to a decision-maker what a
  model does, how confident it is, and what it cannot tell them. **Scarcer than the ability to fit the
  model.**

### Batch 137: content worth carrying

- **`ISM4545` is told to expect its own syllabus to supersede this guide's tool list**, because the field
  moves fast enough that a stable syllabus would be a warning sign. It also gets a **specific scepticism
  checklist**: a demonstration on clean data proves little; ask what happens when the model is wrong and
  who is accountable; ask what the baseline is; **beware of leakage** — a model performing implausibly well
  is usually seeing information at training time that will not exist at prediction time, *the commonest
  cause of a model that works in testing and fails in production*; and automation shifts work rather than
  removing it.
- **`ISM4400` is written across a genuine historical junction.** Decision support and expert systems are
  1970s–80s terms for encoding expert reasoning as explicit rules; that programme largely stalled and
  modern AI took the opposite route. **The guide explains why the older material is not obsolete: rule-based
  systems are auditable, and in regulated settings explainability is a legal requirement rather than a
  preference.** It notes that most deployed systems are hybrids — a model scores, rules enforce policy
  limits, a human decides at the boundary.
- **It also names identity resolution as the underrated hard problem** in data integration, and states that
  governance fails organisationally rather than technically: **if nobody owns a data element, nobody fixes
  it**.
- **`ISM4113` says the thing systems-analysis courses are actually about**: IS projects fail on requirements
  far more than on technology — the system was built correctly and it was the wrong system. **Users describe
  solutions when asked about problems**, and *"the workarounds people have invented are usually the most
  informative thing you will find."* It warns that **students who came to information systems to avoid
  dealing with people find this course a surprise.**
- **It gives concrete team-project advice**: agree roles and rhythm in week one, **raise a non-contributing
  member in week four rather than week fifteen** because instructors can act on the first and not the
  second, keep the artefacts as portfolio pieces, and have an honest answer ready for the interview question
  about what went wrong — **that answer is what the question is for**.
- **`ISM3116` leads on UWF's own framing sentence** — managerial application rather than algorithmic
  derivation — and then states the consequence honestly: **the burden of scepticism falls on the student**,
  because a tool that produces a trend line without requiring derivation will happily produce one from data
  that does not support it. The practical version of correlation-versus-causation is given as three
  questions to ask before acting on a relationship.
- **`ISM4321` names two ideas worth carrying into any job**: **an untested plan is not a plan** (the most
  reliable finding in post-incident reviews), and **quantitative risk figures are more fragile than they
  look** — an annualised loss expectancy is the product of two uncertain estimates, so *do not let the
  arithmetic launder a guess into a fact*. It adds that **risk acceptance belongs to management, not to
  security staff** — surface it clearly, let the accountable person decide, and record that they did.
- **`ISM4320` carries the batch's strongest warning block**, on the legal boundary: studying attacks is
  lawful, performing them without documented authorisation is not; **"I was only looking" and "the system
  was insecure" are not defences**; never test against university systems; **if you find a vulnerability
  accidentally, report it and do not explore further, because further exploration converts a good deed into
  an offence**. Framed around career consequence rather than moralising — security employment requires
  background investigation, and a finding closes doors permanently in a field that otherwise wants you.
- **`ISM3323` states where the leverage actually is**: asset inventory, access review, patch discipline,
  backup testing and vendor risk prevent most incidents and **fail through organisational neglect rather
  than technical difficulty**. A student who runs them well is more useful to most employers than one who
  can name attack techniques.
- **A shared transfer block records an articulation trap specific to business**: many Florida business
  colleges are **AACSB accredited** and commonly limit how much upper-division business coursework may
  transfer in, frequently requiring a share to be taken in residence. **A course can articulate under SCNS
  and still not count toward the major.**
- **A shared certifications block states the honest relationship**: the degree is the durable credential,
  certifications are current and expire, employers ask for both — **and "do not collect certifications
  instead of building things," because a portfolio of real projects outperforms a list of badges in almost
  every hiring conversation in this field.**

### Batch 138 — MAN Management (10 guides), and **MAN closes**

`MAN3301`, `MAN3504`, `MAN3583`, `MAN3802`, `MAN4280`, `MAN4341`, `MAN4350`, `MAN4384`, `MAN4441`,
`MAN4570`. **No orphans and no skips were needed** — every queued row had a UWF entry, which had not
happened in any prefix before. **MAN: 32 pushed, 7 skipped, 0 queued** — the tenth prefix to close.

### ⚠⚠⚠ THE FINDING: a number COLLISION, not merely a title drift

**`MAN4350` carries different subjects statewide and at UWF, and the two subjects have swapped places with
a neighbouring number.**

| Number | Statewide inventory | UWF |
|---|---|---|
| `MAN4320` | **Human Resource Recruitment and Selection** (13 institutions) | *not published* |
| `MAN4350` | **Training and Development** (13 institutions) | **Recruitment and Selection** |

- **The subject most Florida institutions number `MAN4320`, UWF numbers `MAN4350`.**
- **The subject most institutions number `MAN4350` is not published under that number at UWF at all** —
  UWF folds training into **`MAN4341 Performance Management`**, whose description explicitly covers *"change
  management, organizational development, performance management, and training."*

**⚠⚠ This is worse than the `-SCNS` cases recorded so far**, because it is not a drift on one number — it
is a *permutation across two*. A student transferring `MAN4350` out of UWF will have it read as Training
and Development, **which is not what they took**; a student transferring into UWF with `MAN4350` may be
credited for content they have not covered.

**Both guides carry the collision table** and the instruction: **carry the syllabus and catalog
description rather than the transcript line, and raise the discrepancy before the evaluation is made
rather than appealing it afterwards.** `MAN4341`'s guide additionally tells students seeking training and
development at UWF that this is where it lives.

**⚠ Not added to the `-SCNS` open-cases table as a normal row** — it needs a different treatment, because
resolving it correctly may require pages on *two* numbers, not one. **Flagged for Ron in
`REVIEW_QUEUE.md`.**

### ⚠⚠ The standing-requirement rule needs a threshold column: UWF uses THREE

Rule 3ac recorded standing requirements after `ISM3011`. MAN shows the pattern is not uniform **within a
single prefix**:

| Threshold | Courses |
|---|---|
| **45 hours** | `MAN3301`, `MAN3504`, `MAN3583` |
| **60 hours** | `MAN4280`, `MAN4441` |
| **none** | `MAN3802` |
| **a course** | `MAN4341`, `MAN4350`, `MAN4384` (`MAN3301`); `MAN4570` (`MAR 3202`) |

**The `standing()` helper now takes the threshold as a parameter and states in every guide that UWF uses
more than one**, with the direction: *do not assume the number carries across courses — read each entry.*

### ⚠ A second department inside the prefix, with a different prerequisite convention

**`MAN4570 Purchasing and Supply Management` is published by the Department of Commerce**, while every
other MAN course in the batch sits in Business Administration — **and its prerequisite is `MAR 3202`, a
marketing course**, not a standing requirement and not `MAN3301`. A student assuming the prefix-wide
pattern discovers the mismatch at registration, and `MAR 3202` may carry prerequisites of its own.

**Same lesson as MCB batch 136**: the department line is not decoration, and a cross-department placement
changes the course's prerequisite conventions as well as its content.

### ⚠ Four further title divergences, all handled with the reusable `drift()` block

| Number | Statewide | UWF | Assessment |
|---|---|---|---|
| `MAN4350` | Training and Development | Recruitment and Selection | **⚠⚠⚠ collision — see above** |
| `MAN3802` | Principles of Entrepreneurship | Small Business/Family Business Management | **⚠⚠ related but distinguishable** — venture creation versus managing established firms. Added to open-cases. |
| `MAN4280` | Organizational Development | Business Leadership and Change Management | overlapping traditions; OD content also sits in `MAN4341` |
| `MAN4384` | Strategic Workforce Planning | Strategic Human Resource Management | broadening, not divergence |
| `MAN4570` | Global Sourcing | Purchasing and Supply Management | component versus whole |

### ⚠⚠ CORRECTION CANDIDATE on an already-live guide: `MAN4720`

UWF's catalog entry for its BSBA capstone (`MAN4720 Strategic Management`, **32 institutions, pushed
earlier in the build**) states: **"Senior status and permission is required. Must be taken at UWF."**

**The live guide mentions none of this** — checked against the published API response; no match for
residency, senior status, or permission language. **This is a residency requirement, and residency rules
cannot be worked around late.** It is also the only "permission is required" marking anywhere in the MAN
prefix.

**Not edited unilaterally** — the live guide is a multi-institution guide and a UWF-specific residency
clause may or may not belong in it. **Added to `REVIEW_QUEUE.md` for Ron's decision.** The general point
(capstones commonly carry residency requirements, check early) has been added to the shared transfer block
in all ten new guides.

**⚠ This is the fifth instance of the standing pattern**: *related-course research surfaces facts missing
from already-published guides.* The section below this one records the pattern; MAN4720 is added to it.

### Batch 138: content worth carrying

- **`MAN3301` carries the Florida employment-law context** that generic HR texts omit: Florida is
  **at-will** and **right-to-work**, so union density is low and the collective bargaining material reads
  as more historical here — **but "at-will" is widely misread as "no rules," and the guide says plainly it
  does not permit discrimination, retaliation, or dismissal for protected activity.** It adds Florida's
  constitutionally-set minimum wage (**check the current rate; textbooks are out of date**), the Florida
  Civil Rights Act's separate filing deadlines, and **E-Verify obligations above a size threshold**, which
  students have usually never heard of.
- **It names three ideas that prevent expensive mistakes**: document contemporaneously and consistently
  (**a record written after a dispute begins is worth very little**); **discrimination does not require
  intent** — disparate impact is the single most misunderstood idea in employment law; and **exempt
  misclassification turns on duties and salary, not job title and not employee agreement**, with back-pay
  liability accumulating quietly for years.
- **`MAN3504` names the one idea that transfers everywhere**: **variability causes queues, not average
  load** — which explains emergency departments, airport security, call centres and theme park rides, and
  why *"we have enough capacity on average"* is not an answer. Also: **do not react to common cause
  variation** — treating normal fluctuation as a special event makes performance measurably worse.
- **It weights services over manufacturing deliberately**, because UWF's description says "manufacturing
  and service" and **Florida's dominant employers are services**. It names **healthcare operations** as
  the growth area worth pursuing — patient flow, capacity and scheduling are the same problems under
  different vocabulary.
- **`MAN4350` states what the research says and practice ignores**: **the unstructured interview, which
  almost every organisation relies on and almost every manager believes they are good at, is among the
  weaker predictors** in the literature. And the uncomfortable corollary — **confidence in your own
  judgement of people is not evidence of skill at it**, a finding that applies to everyone reading it.
- **`MAN4341` is written about a genuinely unsolved problem rather than a settled procedure.** It records
  that **feedback does not reliably improve performance and in a substantial minority of studies makes it
  worse**, that **ratings measure the rater as much as the rated**, and that forced distribution ranking
  has been abandoned by many of the organisations that popularised it. What has better support: frequent
  specific conversation, separating developmental discussion from pay, and **training raters — which
  almost no organisation does adequately.**
- **`MAN4384` tells students to be sceptical of their own course's literature**: the HR-to-firm-performance
  research **cannot separate "good practices cause profit" from "profit funds good practices,"** and the
  honest literature says so. It adds that **benchmarking tells you what is common, not what is good** —
  the unstructured interview being the standing example — and that **every HR recommendation should carry
  a cost and a mechanism**.
- **`MAN3583` names the uncomfortable truth**: most projects overrun, **optimism in estimation is
  systematic rather than occasional**, and the countermeasure is **reference-class forecasting** — start
  from what similar projects actually took. It states the professional obligation directly: **an estimate
  is a forecast, not a promise, and saying so is part of the job.** Credential guidance is specific —
  **CAPM, not PMP**, because PMP requires documented leading experience a graduating student does not have.
- **`MAN4441` leads with UWF's own most interesting phrase** — negotiating *where your responsibility
  exceeds your authority*, **which is the actual condition of most working life**. It names **BATNA as the
  determinant of power**, that **anchoring works and works on you**, that most negotiators wrongly assume a
  fixed pie, and where the ethical line sits: **puffery about preferences is accepted; misrepresenting a
  material fact can be fraud** — decide your standard before you are under pressure. Its most immediately
  useful application is named as **the student's own first job offer**.
- **`MAN4280` reframes resistance to change as usually rational** — people who resist frequently understand
  something about the work that the designers do not, or are correctly anticipating a real cost. **It also
  notes what UWF's own phrase "overcoming resistance" presumes**: that the change is correct and the
  resister is the problem — *sometimes true, and not reliably*. It tells students the leadership literature
  is an unusually weak evidence base and recommends Rosenzweig's *The Halo Effect* as the corrective, and
  treats the ubiquitous **"70% of change initiatives fail"** claim as a case study in thin evidence.
- **`MAN4570` makes the case for the most underrated function in a business degree**: purchased goods and
  services are frequently **more than half of revenue**, so a point saved on spend drops straight to profit.
  The core skill is **total cost of ownership rather than unit price** — and **single sourcing looks
  efficient until a storm closes a port**, which is locally pointed given Florida's hurricane exposure and
  concentration through Miami, Tampa, Jacksonville and Port Everglades. It notes purchasing ethics is
  unusually concrete: **bright-line gift rules, and criminal consequences in public procurement**.
- **`MAN3802` gives the family-business half the billing UWF does.** Family firms are the majority of
  businesses worldwide, **most do not survive into the third generation**, and the causes are consistent —
  succession discussed too late, no successor development plan, unclear ownership transfer, deferred
  conflict. It names the three-circle model, says plainly that **non-family employees face a real ceiling
  and pretending otherwise damages retention**, and flags **compensating relatives** as the recurring
  flashpoint with three defensible and conflicting answers.
- **It also points students at the Florida SBDC hosted at UWF itself** — free consulting to Florida small
  businesses, excellent local case material, and a place students have found internships. **Most students
  never learn it is there.** Plus the Florida obligations new owners miss: sales tax registration, county
  business tax receipt, **workers' compensation with a lower threshold in construction**, and that
  **incorporating does not protect you from a debt you personally guaranteed**.
- **A shared `AI_MGMT` section separates AI as a manager's tool from AI as something a manager must
  govern.** The highest-risk application is named as employment decisions: **AI screening reproduces bias
  in historical hiring data, the employer is liable regardless of which vendor supplied the tool, and
  disparate impact does not require intent.** Regulation is arriving unevenly, and **where your applicants
  are located determines what applies — not where your office is.** And: *"the system flagged it" is not an
  explanation you can give an employee, a regulator, or a court.*

### Batch 139 — MVK / PGY / TPP: the arts, and **three new contact-hour conventions established**

`MVK2122`, `MVK1115`, `MVK2421`, `PGY2401C`, `TPP2100`, plus orphan `TPP2110`; then `TPP2110C` skipped.
**Prefixes NOT closed** — MVK and TPP still carry substantial queued work. This batch was scoped to settle
the hour reasoning that had blocked the arts prefixes for several sessions.

### ⚠⚠⚠ THE CORE PROBLEM: the lecture convention produces nonsense in the arts

Every hour figure in this repository derives from a convention, because UWF publishes none. Until now three
existed: **lecture 15/credit**, **science laboratory 45/credit**, **integrated `C` 60 for 3 sh**, with
clinical variants. **None of them fits a studio, a rehearsal room, or a private lesson**, and applying the
lecture rate to arts courses would have been wrong in three different directions at once.

**Three conventions are now established and implemented in `wart.py`:**

| Convention | Rate | Applies to | Why |
|---|---|---|---|
| **Activity** | **30 per credit** | class piano, group-skills courses (`MVK2122`, `MVK1115`) | Class piano conventionally meets **two scheduled hours a week for one credit**. The 15-hour lecture rate understates the scheduled time; the 45-hour laboratory rate overstates it. |
| **Studio / performance** | **60 for 3 sh** | studio art and acting (`PGY2401C`, `TPP2110`, `TPP2100`) | Studio courses meet roughly **twice the scheduled time of a lecture of the same credit**. Matches the figure already used for the live ART studio guides — **consistent with the existing corpus rather than a new number.** |
| **Applied music** | **≈15 total, regardless of credit** | private instruction (`MVK2421`) | ⚠⚠⚠ See below. This one is not a rate at all. |

### ⚠⚠⚠ Applied music breaks the model, and the guide says so rather than hiding it

**`MVK2421` is 2–3 semester hours and has roughly 15 scheduled contact hours** — one private lesson a week
across a fifteen-week term, **and that figure does not change when the credit value does.**

**The credit is not earned in the lesson.** It is earned in individual practice, conventionally **one to two
hours per day per credit**, plus jury examinations, studio class, recital attendance and performance
obligations.

**This is the first course type in the entire build where the contact-hour field actively misleads**, and
the handling is to say so at length rather than to report a number:

> *"Read the contact-hour figure as the lesson time only. The real workload of an applied music course is
> several times larger and is the reason students are advised not to overload a term in which they carry
> applied study."*

**⚠ Note the validator did not flag 2 sh / 15 hours**, nor 1 sh / 30 hours, nor 3 sh / 60 hours. The
credit-to-hour heuristics do not cover arts formats. **Not a defect to fix blindly** — but worth knowing
that arts guides get no automated sanity check on hours.

### ⚠⚠ Ron's suffix rule again, and the arts are its worst case

**SCNS offers none, `C`, and `L` — and none of them describes a studio, a rehearsal room, or a private
lesson.** UWF's TPP prefix demonstrates the consequence within a single department:

| Course | Suffix | Actual format |
|---|---|---|
| `TPP2101L`, `TPP3102L` | **`L` laboratory** | acting studio |
| `TPP2710C`, `TPP2167C` | **`C` combined** | voice / musical theatre studio |
| `TPP2110`, `TPP2100`, `TPP2120` | **none** | acting studio |

**Three suffixes for what are all studio-format courses, in one department.** A shared `SUFFIXNOTE` block
now appears in every arts guide: *the description records the course; the suffix records how it was filed;
when they disagree, believe the description* — and **send the description and syllabus, not the number,
when transferring an arts course.**

**`TPP2110C` → `TPP2110` is the concrete instance**: the statewide inventory carries the `C`, UWF does not,
and both are studio courses. Skipped the `C` row, published the UWF form.

### ⚠⚠⚠ A registration trap: two near-identical acting courses, neither with a prerequisite

UWF publishes **`TPP2110 Acting I`** and **`TPP2100 Acting for Non-majors`** with descriptions that are
nearly identical apart from one phrase — `TPP2110` is *"designed for students with some prior experience on
stage."*

- **Neither publishes a prerequisite**, so **nothing in registration will stop a student choosing the wrong
  one.**
- **`TPP2110` opens `TPP3155 Acting II`; `TPP2100` gates nothing.** An intending major who takes `TPP2100`
  may have to take `TPP2110` afterwards anyway.
- **⚠⚠ The statewide inventory lists BOTH numbers under the title "Acting I"** — `TPP2110C` at 17
  institutions and `TPP2100` at 10 — **so a transfer evaluation matching on title alone cannot tell them
  apart.** UWF's own titles do distinguish them.
- `TPP1110`/`TPP1111` exist as lower-division "Acting I"/"Acting II" as well, already in the corpus.

**Both guides carry a mutual disambiguation block** stating the practical rule and warning that the
registration system will not catch the error.

### ⚠⚠ A degree requirement that delays more music degrees than anything else

**UWF states the purpose of the class piano sequence in every entry**: functional skills correlating with
music theory, and preparation for **the piano proficiency examination**.

The `PROFICIENCY` block, in every class piano guide, records what the catalog does not:

- **It is a degree requirement at essentially every accredited US music programme**, and **failing it can
  delay graduation regardless of performance elsewhere** — one of the commonest causes of an unexpectedly
  extended music degree.
- **What it tests is functional playing, not repertoire**: scales, harmonisation, transposition,
  sight-reading, open-score reading, accompanying.
- **⚠ The distinction students miss**: *a student who can play difficult pieces from memory but cannot
  harmonise a melody at sight will fail this examination.* Functional skills must be practised
  deliberately; they do not arrive as a by-product of repertoire work.
- **Get the department's requirement list in the first term** and treat it as the syllabus for the whole
  four-course sequence.

### ⚠ Two access provisions students do not know exist

- **"Placement / audition may substitute for prerequisite"** — published on the class piano sequence.
  **A student with prior keyboard study may skip terms**, but placement examinations are scheduled at or
  before the start of term, so **a student who registers first and asks later has lost the option.**
- **Applied lessons are open to non-majors** — *"if a music course or ensemble is taken concurrently and
  faculty schedules permit."* **⚠ Very few non-majors know this exists.** Condition two is a real capacity
  constraint: majors are placed first and **studio assignments are made before the term begins**, so the
  ask must happen in the preceding term, and through the Department of Music rather than general advising.

Conversely, **`MVK1115` publishes a registration bar inside its description** — *"Open only to music
majors."* Unusual placement; most restrictions appear as prerequisites or permission markings. The guide
points excluded non-majors at the applied-lesson provision above.

### Batch 139: content worth carrying

- **`PGY2401C` answers the obvious question honestly**: why learn film when nobody shoots film? Because
  **film forces deliberation** (a roll has 36 frames and each costs money), **the darkroom makes exposure
  and development visible as physical processes rather than sliders**, and the aesthetic decisions are
  identical in both media. It is also straight about cost: **film and paper are a real expense beyond the
  course fee, darkroom time is scheduled and finite, and the work cannot be done the night before.**
- **It carries a darkroom chemistry safety block** — developers and fixer are sensitisers, **repeated skin
  contact can produce a lasting allergic dermatitis that ends a person's darkroom work**, use tongs not
  fingers, and tell the instructor privately about pregnancy or respiratory conditions.
- **And a photographing-people block** distinguishing lawful from ethical: public photography is generally
  lawful in the US, **commercial use normally requires a release**, minors and private property require
  particular care, and *"consider the subject's position, not only your right"* — photographing people who
  are unhoused, distressed or unable to consent raises questions **"it was legal" does not answer**. Plus:
  **Florida is a two-party consent state for audio**, which bites the moment a photography course extends
  into video.
- **`MVK2421` carries a physical-injury warning that applied music guides generally omit.** Tendinitis and
  repetitive strain are common among pianists, **playing through pain does damage that can end a career**,
  and the usual causes — technique problems and excessive unbroken practice — are both fixable. **Report
  pain to your teacher immediately.**
- **It also names the studio relationship as the most important one in a music degree** — repertoire, jury
  preparation, references, years of development — and says that **if the fit is genuinely wrong, raise it
  early and through the department**, because departments would rather resolve a mismatch than lose a
  student.
- **And it tells students to ask their teacher to teach them how to practise**, on the ground that
  **practice quality matters more than quantity and a student who does not know how to practise will
  plateau regardless of hours.** A legitimate and productive request that students do not think to make.
- **Both acting guides state plainly what the course asks**: you work in front of people from week one and
  are critiqued, **the discomfort is the mechanism rather than a side effect**, and — importantly —
  **acting training is not therapy and should not be used as it.** *An instructor pressing a student to use
  private trauma as material is not applying current best practice, and the student is entitled to
  decline.* UWF CAPS is named as free.
- **They document consent practice**: contemporary staging of touch, closeness and violence uses
  **intimacy direction and choreographed, rehearsed, repeatable staging with explicit consent**, and
  **consent may be withdrawn at any point, including after being given**.
- **They name the single most useful idea in a first acting course**: *play an action, not an emotion* —
  trying to feel sad produces indicating; trying to get something from a partner produces truthful
  behaviour. **Emotion is a by-product of pursuit, not a target.** Plus *specificity beats intensity* and
  *listening is the whole job and the hardest part*.
- **`TPP2100`'s guide makes the non-major case without sentimentality**: the trainable skills — speaking
  audibly with intent, holding attention, **listening rather than waiting to speak**, managing the physical
  symptoms of nerves, reading what a person means — are what make a graduate effective in an interview, a
  courtroom, a classroom or a meeting. And it notes non-majors are **designed for, not tolerated**.
- **The arts careers blocks are honest about freelance reality** rather than discouraging: performance work
  is **overwhelmingly project-based and income is assembled from several sources** — *worth knowing at the
  start rather than learning late*. Against that, the guides name the concrete Florida markets: **theme
  park and cruise line performance is one of the largest live-performance employers in the world**, with
  salaried contracted jobs that audition regularly; **collaborative pianists and accompanists are
  consistently in short supply**; **stage management is less crowded than performance**; and photography
  has a large wedding, event, real estate and tourism market in this state.
- **A shared arts transfer block names a complication most disciplines do not have**: **admission is
  frequently by audition or portfolio, not by transcript**, so a programme may accept your credit and still
  place you back a level. Plus the programmatic accreditors — **NASM (music), NASAD (art and design), NAST
  (theatre)** — whose curricular requirements mean **a course that articulates may still not satisfy the
  requirement it appears to match.**

### Batches 140-141 — MVK and TPP complete (20 guides), and **both prefixes close**

**Batch 140 (MVK, 12 guides)**: the applied keyboard ladder `MVK3331`, `MVK4341`, `MVK3431`, `MVK4441`,
`MVK3333`, `MVK4343`, `MVK1412`, `MVK2422`, `MVK3432`, `MVK4442`, plus `MVK3702` and orphan `MVK4641`;
`MVK4641C` skipped. **MVK: 20 pushed, 12 skipped, 0 queued.**

**Batch 141 (TPP, 8 guides)**: `TPP3155`, `TPP4113`, `TPP2710C`, `TPP3650`, `TPP3264C`, `TPP3252C`, plus
orphans `TPP2500` and `TPP3310`; `TPP2500C`, `TPP3310C` and `TPP3251C` skipped. **TPP: 19 pushed, 4
skipped, 0 queued.**

**Eleventh and twelfth prefixes closed.** The conventions established in batch 139 carried both batches
without further hour reasoning.

### ⚠⚠⚠ A hidden two-track structure in the applied keyboard ladder

**Laying the MVK applied entries side by side reveals a structure the catalog never states.** Numbers are
assigned by **instrument × standing**, not by a prerequisite chain — and **piano has TWO parallel ladders**:

| Track | Freshman | Sophomore | Junior | Senior | Credit |
|---|---|---|---|---|---|
| **Performance: Keyboards** | `MVK2321` | — | `MVK3331` | `MVK4341` | **3 sh fixed** |
| **Applied Music Piano** | `MVK1311` | `MVK2421` | `MVK3431` | `MVK4441` | **2–3 sh variable** |
| Applied Music Organ | `MVK1313` | `MVK2223` | `MVK3333` | `MVK4343` | 2–3 sh variable |
| Applied Music Harpsichord | `MVK1412` | `MVK2422` | `MVK3432` | `MVK4442` | 2–3 sh variable |

**⚠⚠ The fixed-versus-variable credit distinction is the tell.** A fixed higher credit with a heavier
expectation is the shape of a **performance-major track**, against a flexible track serving other
concentrations. **UWF does not label them**, so every guide in the ladder carries the table and the
direction: *which ladder your degree plan puts you on is a departmental decision and should be settled in
your first term — not discovered in your third year, when credits on the wrong track may not substitute.*

**Repeat limits differ across the ladder too** (`MVK3331` allows 6 sh, `MVK4341` allows 9), which matters
because **sequences here are built by repeating a number across terms.**

**⚠ Fifth prefix where reading the structure rather than the titles surfaced a hidden track** — after MLS,
NUR, HSC and MCB.

### ⚠⚠ The applied-music hour warning fired, and was correctly overridden

`MVK3331` and `MVK4341` are **3 sh with 15 contact hours**, and the validator warned on both:
*"3 credits with 15 contact hours (expected ~45, or ~60 for a C course)."*

**Correct to override.** This is exactly the applied-music case documented in rule 3al: one weekly private
lesson is ~15 hours a term **regardless of the credit value**, and the credit is earned in practice. The
2 sh applied guides at 15 hours did **not** warn — the heuristic appears to check 3 sh only.

**⚠ Worth flagging for Ron**: as with the MLS and NUR heuristic conflicts, a per-format exception may be
warranted. Ten applied-music guides now carry hour figures the validator either warns on or silently
accepts, and neither behaviour is informative.

### ⚠⚠⚠ Two more catalog-internal discrepancies — the fifth and sixth in the build

**1. `TPP2710C` names a prerequisite that does not exist.** UWF publishes `THE 2000 AND TPP 2121`.
**`TPP2121` does not appear in UWF's TPP listing.** The nearest published number is `TPP2120 Acting
Improvisation` — which **is** the published prerequisite for the sibling course `TPP2500 Movement for the
Actor` (`THE 2000 AND TPP 2120`).

The two courses are near-twins: both beginning explorations of the actor's instrument, both "directed
primarily toward preparation for stage work," both naming `THE 2000` as the other half. **The parallel is
close enough that it looks like a transposed digit — and the guide explicitly declines to say so.**

**2. `TPP4113` publishes an exclusion naming a phantom course.** *"Credit may not be received in both TPP
4113 and TPP 4141."* **`TPP4141` does not appear in UWF's listing.** Same shape as the EEL3111L phantom
exclusion from batch 122.

**Both handled by the standing practice**: reproduce as published, name the anomaly, refuse to guess,
direct the student to the department. The `TPP4113` guide adds the practical consequence — **a student
transferring in credit for a `TPP4141` may find it blocks credit here**, and that is the sort of thing
which surfaces at a degree audit in a final term.

### ⚠⚠ The TPP sequence is chained four deep, and the wrong entry course costs a year

    TPP2110 → TPP3155 → TPP4113
    TPP3155 + TPP3650 → TPP3310
    TPP3155 → TPP3252C
    THE2000 + TPP2120 → TPP2500
    THE2300 → TPP3650

**`TPP3155 Acting II` is the hinge** — three later courses depend on it, and it requires **`TPP2110`, not
`TPP2100`**. Combined with the batch-139 finding that the two introductory courses are near-identical and
neither has a prerequisite, **a student can enter through `TPP2100`, be blocked at `TPP3155`, and lose a
year** — because arts sequences are frequently offered in one term only.

**⚠ The sequence also crosses into the `THE` prefix** (`THE2000`, `THE2300`), so **a student planning only
within TPP will miss two prerequisites.** A shared `SEQ` block in every TPP guide lays the whole chain out;
none of it is stated in the catalog.

### Batches 140-141: content worth carrying

- **`MVK3702 Accompanying Coaching Class` carries two separate gates** — published prerequisites
  (`MVK1311 AND MVK2421`) *and* a description stating *"two years of applied piano and permission is
  required."* **Satisfying the prerequisites does not open registration.**
- **It makes the strongest employment argument in the music prefix**: accompanying demand **consistently
  exceeds supply**, it is **paid work available while still a student**, and **a competent sight-reading
  accompanist can work steadily in almost any town in Florida where a soloist of the same ability cannot.**
  Sight-reading is named as the gating skill — *it improves only by reading a large volume of unfamiliar
  music, which is free and which almost no student does enough of.* And: **accompanists routinely
  undercharge because nobody told them the norms.**
- **UWF's collaborative piano provision is unusually developed for an institution of its size** —
  `MVK3721`, `MVK3720`, `MVK3722`, `MVK4704`, `MVK4705`, plus two accompanying internships. **A genuine
  specialisation track, not a single elective.**
- **`MVK4641 Piano Pedagogy` is "required of all piano majors," stated in the description**, and the guide
  says why: **teaching is what most pianists actually do for a living.** Its central insight —
  **being able to play is not being able to teach**; advanced pianists teach beginners badly *because they
  have forgotten what they did not know and cannot see the difficulty.* **Diagnosis, not demonstration, is
  the competency.**
- **It treats studio teaching as the self-employment it is**: fees, written studio policy, cancellation
  rules, taxes and managing parents. **Set and hold a cancellation policy from the first student** — named
  as the single most common failure among new teachers. Plus **background screening and mandatory reporting
  obligations** when teaching children, and that **K-12 teaching is a different route requiring Florida
  certification, not a performance degree plus this course.**
- **`TPP2500 Movement for the Actor` names what movement training is actually for**: most people arrive
  carrying physical habits they cannot see, and **those habits limit what characters you can play, because
  every character arrives through the same body.** It carries a disclosure block — injuries, joint
  conditions, asthma, pregnancy, concussion history — with **"do not work through pain; actors lose careers
  to injuries they trained through."**
- **`TPP2710C Voice for the Actor` carries the batch's most transferable warning.** Vocal injury is an
  occupational problem: **hoarseness lasting more than two weeks warrants medical attention**, **whispering
  is worse for an injured voice than speaking gently**, and **teachers, clergy, lawyers and clinicians
  suffer occupational voice disorders at high rates and are almost never trained.**
- **It also addresses accent and identity honestly.** Older actor training aimed at replacing regional and
  cultural speech with a single "standard"; **the field has substantially moved away from that.**
  Contemporary practice treats **accent as a skill to add, not a trait to correct** — the goal is range,
  including your own accent — and **a student who feels their own speech is being treated as a defect
  should raise it.**
- **`TPP3650 Script Analysis` is the one non-studio course in the arts batches** and uses the ordinary
  lecture convention. It draws the distinction the course exists on: **a literary reading asks what a play
  means; a production reading asks what has to happen on a stage.** *A literary reading can rest in
  ambiguity. A production cannot.* And the commonest student error — **deciding what a play is "about" and
  bending the evidence to it**; the discipline runs the other way.
- **`TPP3310 Play Directing` publishes its own workload warning** — *"requires rehearsal time outside of
  regularly scheduled class hours"* — which most catalogs do not. The guide adds that **the hard part is
  coordinating other people's time**, and that **this course combines badly with a term already carrying a
  production commitment.** On craft: **result direction does not work** (*"be angrier" tells an actor what
  you want to see and nothing about how to produce it*), and **three notes an actor can act on beat twenty
  they cannot remember.** The director is named as holding responsibility for **rehearsal room safety,
  consent and intimacy protocols** — *authority in a rehearsal room is real, and so is the obligation.*
- **`TPP3264C Acting for the Camera` is the only TPP course with a permission requirement**, and it also
  carries a fee — almost certainly equipment and studio capacity. The stage-to-camera adjustment is framed
  precisely: **the correction is not "do less" but "think more and show less" — the camera photographs
  thought.** Its most practically valuable content is **self-tape competence, which removes geography as a
  barrier** and has genuinely changed access for actors outside Los Angeles and New York. Plus a warning
  that **legitimate representation is paid from earnings and never charges an upfront fee** — advance-fee
  schemes target new actors specifically.
- **`TPP3252C Music Theatre Scene Study` names the failure mode**: doing acting, singing and movement
  **sequentially rather than simultaneously** — *a performer who stops acting to sing the difficult phrase
  has lost the scene.* Its organising principle: **a song is a scene**; characters sing where speech is no
  longer sufficient, so a song has objective, obstacle and turn. **UWF requiring `TPP3155` (acting) rather
  than a voice course signals the department treats musical theatre as acting first** — the contemporary
  professional consensus.
- **It points students at UWF's own collaborative pianists** (`MVK3702`, `MVK3721`, `MVK3720`) as rehearsal
  partners who **need repertoire experience as much as the singer needs a pianist** — a cross-departmental
  connection neither prefix's students would otherwise find. And practical audition points: **sheet music
  taped or bound in your own keys, opening flat** — *presenting an accompanist with loose photocopies or a
  phone is a professional error that auditioners notice*; **choose material that suits your voice and
  casting, not material you admire.**
- **`TPP4113 Acting III` explains why style comes third**: *style is not a coat put on over truthful
  acting; the truthfulness has to survive inside the convention*, and **a student who has not secured the
  fundamentals will produce mannerism.** Practical value named as **audition range** — classical and
  heightened-text competence is consistently in shorter supply than contemporary competence.

### Batch 142 — CPO and TAX (4 guides), and **both prefixes close**

`CPO2002`, `CPO3055`, `CPO4074`, `TAX4001`. **No orphans and no skips** &mdash; every queued row had a UWF
entry, the second time this has happened (after MAN batch 138). **CPO and TAX: 8 pushed, 0 skipped, 0
queued** &mdash; the **thirteenth and fourteenth prefixes** to close.

### ⚠⚠⚠ A third phantom exclusion: `TAX4001` excludes credit with a course UWF does not publish

UWF publishes: **"Credit may not be received in both TAX 4001 and TAX 4002."** **`TAX4002` does not appear
in UWF's TAX listing.**

**This is the third phantom exclusion in the build**, after `EEL3111L` (batch 122) and `TPP4113` (batch
141), and it confirms the pattern is not confined to one department or college &mdash; these three sit in
Engineering, Theatre and Business respectively. **Handled the settled way**: reproduce as published, name
the anomaly, refuse to guess, state the practical consequence &mdash; *a student transferring in credit for
a `TAX4002` may find it blocks credit here, and exclusion rules surface at degree audits in a final term.*

**⚠ Now worth a standing pre-prefix check**: grep each catalog extract for *"may not be received"* and
verify every number named actually exists in the prefix.

### ⚠⚠ A near-collision in CPO, and both numbers are already in the corpus

| Number | Statewide inventory | UWF |
|---|---|---|
| `CPO2001` | **Comparative Politics** (8 institutions) | *not published* |
| `CPO2002` | **Comparative Government** (16 institutions) | **Comparative Politics** |

**Structurally the same shape as the `MAN4350`/`MAN4320` collision from batch 138** &mdash; the subject
statewide-numbered `CPO2001` is what UWF numbers `CPO2002` &mdash; **but materially milder**, because
"comparative government" and "comparative politics" are largely interchangeable names for one subfield
rather than two different subjects. **Recorded as a naming overlap, not added to `REVIEW_QUEUE.md` as a
collision needing a decision.** `CPO2001` is already pushed in this repository, so both numbers are
documented and each guide can point at the other.

### ⚠⚠ A stale catalog entry naming a state that ceased to exist in 1991

`CPO2002`'s description lists example countries as **"Britain, France, Germany, USSR, Japan and India."**

**Handled as a catalog-currency problem rather than a content claim.** The guide states plainly that this is
an unrefreshed entry, that **illustrative examples in a description are not the syllabus**, and that any
current comparative politics course uses existing states &mdash; then tells the student to **ask the
instructor which countries the course actually covers, since case selection varies a great deal between
instructors.**

**⚠ It also turns the observation to use**: post-Soviet states are among the most studied cases in
contemporary comparative politics precisely because **the collapse produced fifteen new states with shared
institutional inheritance and radically divergent outcomes** &mdash; a natural experiment the subfield has
leaned on heavily.

**This is a new category of finding**: not a contradiction, not a drift, but **a description that has
simply aged**. Worth watching for elsewhere &mdash; a course description is one of the least frequently
revised texts an institution publishes.

### Batch 142: content worth carrying

- **`TAX4001` carries the CPA planning warning that accounting students most often get wrong.** Florida
  requires **150 semester hours** for licensure &mdash; more than a standard four-year degree &mdash; with
  specified accounting and business minimums, **and the requirements to sit the examination differ from
  those for licensure.** The guide adds that **the CPA examination was restructured in 2024** into a
  core-plus-discipline model, so **advice more than a couple of years old may describe a system that no
  longer exists**, and directs students to the Florida Board of Accountancy against their own catalog year.
- **It names the under-advertised alternative**: the **enrolled agent** credential is earned by examination
  with **no degree or hour requirement** and confers unlimited practice rights before the IRS. Not
  equivalent to a CPA licence, and a legitimate route into tax practice that students are rarely told
  about.
- **And the single best concrete action a student in the course can take**: **VITA** &mdash; IRS-certified
  volunteer preparation of real returns. Free, genuine training, resume material, and locally recruiting.
- **Its AI section is the most specific in the build so far**, because tax answers are determined by
  authority rather than opinion. **Fabricated Code sections, regulation numbers, revenue rulings and case
  citations** are the named hazard &mdash; *practitioners have been sanctioned for filings containing
  fabricated citations* &mdash; alongside the point that **thresholds and amounts are adjusted annually, so
  an answer that was right two years ago is simply wrong now and the model will not say which year it is
  describing.** Plus: **never put taxpayer information into a public AI tool** &mdash; preparer disclosure
  is governed by federal law with criminal penalties.
- **It states the Florida market honestly**: **no personal income tax** means state-level individual
  practice is lighter than elsewhere, while **federal work and the state's very large retiree, real estate
  and small-business populations** generate substantial estate, property, sales-and-use and small-business
  demand &mdash; and Florida is a destination for **residency-driven planning**, which is its own
  specialism.
- **`CPO3055 Dictatorships` required the most careful handling in the batch.** UWF names *"the costs
  imposed on subject populations"* as part of the analysis, which in practice means the Holocaust, the
  Soviet terror and famines, and the Chinese famine and Cultural Revolution. **The guide says so plainly,
  frames it as a reason to be prepared rather than to avoid the course**, tells students with a personal or
  family connection to speak to the instructor privately &mdash; *not to be excused from the content, but
  because knowing in advance is the difference between prepared and ambushed* &mdash; and names UWF CAPS.
- **It also sets out the analytical discipline the subject demands**: **explanation is not justification**,
  and *refusing to ask why a regime attracted support leaves you unable to recognise the pattern again*;
  **the comfortable explanations are usually the wrong ones**, since attributing totalitarianism to uniquely
  evil individuals or deficient national characters is empirically weak and reassuring in a way the evidence
  does not support; **evidence from closed regimes requires triangulation across source types**; and
  **resist drawing contemporary parallels too quickly** &mdash; *specify the mechanism you are claiming is
  present and look for evidence of it, rather than reasoning from resemblance.*
- **It explains why the reading list spans Plato to empirical political science**: closed regimes do not
  release reliable data about themselves, so the study of them draws on sources a quantitative course would
  not touch &mdash; and **novels and films are evidence of a different kind rather than illustration.**
- **`CPO4074 Political Economy` separates its two stated objectives**, because students expect only the
  substantive one. The **methodological** half &mdash; incentives, collective action, principal-agent
  problems, rent-seeking &mdash; is named as **arguably the most portable content in a political science
  degree**. The **substantive** half is flagged as genuinely contested: *the relationship between democracy
  and growth has been argued for decades without resolution, and a course presenting it as settled is
  misleading you.*
- **It puts measurement at the centre**, which is where most of the public argument actually lives: **GDP
  measures market activity, not welfare**; **inequality measures disagree depending on income versus wealth,
  before or after transfers, household or person** &mdash; *a great deal of public argument is two people
  using different measures*; and **human development indices carry weighting choices that are political
  decisions presented as technical ones.** The durable habit: **ask what a number is counting before
  arguing about it.**
- **`CPO2002` names the hardest intellectual habit in comparative politics**: resisting the assumption that
  your own system is the default. **Presidential government, two parties, federalism and judicial review
  feel natural to an American student and are unusual choices internationally** &mdash; *seeing your own
  arrangements as one option among several is the whole payoff of the comparative method.*
- **The shared political-science careers block is honest rather than encouraging.** It says outright that
  **the degree is a broad preparation rather than a vocational one**, that political scientist as an
  occupation generally requires a graduate degree, and that **law schools care about GPA and LSAT far more
  than major**. Its two concrete recommendations: **do an internship** (it substitutes for the vocational
  content the degree lacks) and **learn a research method or a language**.
- **A shared social-science AI block names the discipline-specific failure**: models **flatten
  disagreement**, summarising a contested scholarly debate into a tidy consensus that does not exist &mdash;
  *which is precisely the opposite of what a social science course is training you to see. Where the field
  genuinely disagrees, that disagreement is the content.* Plus fabricated citations, and unreliability on
  anything contested, recent, or non-Anglophone.
- **A shared general-education block records a Florida-specific trap**: the state's **civic literacy
  requirement** is satisfied by specified coursework or an examination, and **a politics course is not
  automatically one of the qualifying options** &mdash; confirm against your own catalog year rather than
  assuming.

### Pattern worth naming: related-course research surfaces errors in already-published guides

Twenty-three live corrections and upgrades so far, and **every one was caught while researching a later course that touched an
earlier one** — never by re-reading the guide itself:

| Corrected guide | Caught while writing | Error |
|---|---|---|
| **FFP0030C** → v1.1 | FFP0031C (batch 25) | Minimum Standards total was "~400 hours"; actually **191 + 301 = 492** |
| **MAN4402** (pre-push) | User challenge (batch 24) | FCRA deadlines stale (HB 1407 eff. 7/1/2026); **CHOICE Act** (7/3/2025) missing entirely |
| **TPP2300C** → v1.1 | TPP1110 (batch 28) | Named only TPP2100 as acting prereq; **TPP1110** is the other half of a two-number family |
| **ASL2160C** → v1.1 | ASL2150C (batch 33) | Gave the sequence as ASL1140→ASL1150→ASL2160; Florida also runs **ASL2140→ASL2150→ASL2160** (FGCU), where ASL2150 is "ASL II" with its own ASL2150L corequisite |
| **SON2122C → v1.1, RTE2844L → v1.1** | SON2121C / RTE2854L (batch 49) | Both were published without their colliding siblings. **SON2122C** (OB/GYN **II**) never mentioned **SON2121C** (OB/GYN I) — II published before I. **RTE2844L** is titled "Clinical Education **V**" and is **Clinical Education IV** at Northwest Florida State, where **RTE2854L** is V, both at **5 credits** against the 3-credit/384-hour value published here. Neither guide was wrong for its own institution; both were incomplete. Family/collision blocks added. |
| **MAN3554** → **v2.0 (full rewrite)** | MAN3593 / MAN4597 (batch 48) | ⚠⚠ **The most serious error class found so far: a guide on the wrong subject.** Published as **"Operations and Production Management," 3 credits / 45 hours**. Verified twice — Miami Dade College's Supply Chain Management B.A.S. lists **MAN3554 "Safety and Risk Management," 1 credit**, in the Discipline Content Core. Wrong on **title, subject, and credits**, so the guide was replaced entirely rather than patched. Probable cause is visible in the same program listing: **MAN3504** (Production Operations and Logistics Management) and **MAN3506** (Operations Management) carry the operations content, and the adjacent numbers were conflated. **Corroborating signal worth reusing: the bad guide was an outlier by size** — 8,755 characters against a 18,000–22,000 norm. A guide written from a mistaken premise has less to say. |
| **EMS2666** → v1.1 | EMS2667 (batch 47) | Published at **1 credit**; FSCJ's current program materials list **Paramedic Clinical I at 2 credits** (corequisites EMS2601/2601L), with some earlier catalog listings at 3. Caught by the **numeric cross-check**, not by external research: EMS2667 verified at 3 credits / ~10 weekly contact hours, which made the published 1-credit/96-hour sibling ratio impossible. Contact hours (96) were already right — only the credit value was wrong. Guide now carries the credit-variation and cross-institution numbering note (SPC uses **EMS2665** for Paramedic Clinical II). |
| **DES1100C, DES1200C** → v1.1 | DES0103C / DES0205C (batch 46) | **Both fields wrong in both guides, from one shared assumption.** Each was published at **2 credits / 30 hours**. Verified: **DES1200C is 3 credits, 2 lecture + 3 lab → 75 hours** (SCF/Santa Fe; FSW and Pensacola also 3 cr, the last titling it "Dental Hygiene Radiology I"), and **DES1100C is 3 credits, 1 lecture + 3 lab → 60 hours** (Gulf Coast). Second propagation case in two batches — a single wrong assumption applied across a prefix. Both also lacked the PSAV-vs-credit level trap, now added. |
| **BCA0350, BCA0351, BCA0353, BCA0354, BCA0356** → v1.1 | BCA0357 + full BCA queue listing (batch 45) | **Five guides carrying the same fabricated claim** — each stated that Florida's electrical apprenticeship has "companion co-op numbers (**BCA0358** and following) recording the on-the-job component." That is wrong: **BCA0358 is not a co-op block**, and the OJT companion is the **L-suffix version of the same number** (BCA0350L "Electrical Apprentice 1 Lab-OJT (Non-Union)"). The error propagated because the first BCA guide's inference was reused verbatim across the sequence. Largest single correction so far by guide count, and the first caught by **querying the prefix's whole number range** rather than by researching one adjacent course. All five now carry the verified trade/track/L-suffix structure. |
| **ART2500C** → v1.1 | ART1500C (batch 44) | **Two errors in one guide.** (1) Contact hours were **60** while its entire family — ART1300C, ART2501C, ART2701C, ART2750C — sits at **90**, and Florida catalogs state the format as **2 lecture + 4 studio hours**. Corrected to 90. (2) Named ART2501C and ART3504C but missed **ART1500C**, the 1000-level "Painting I" with the same title and credits and *no prerequisite*. Same internal-consistency failure as the ASL hours — the numeric-field cross-check from batch 36 caught it. |
| **ASL2160C** → v1.3 | ASL2200C (batch 44) | Guide documented the two families converging at ASL2160 and named ASL2170 as level IV — but missed that the families **diverge again**: some institutions number level IV **ASL2170**, others **ASL2200** (EFSC, 4 cr, prereq ASL2160 with a C). Third revision of this guide; the ASL numbering is the most fragmented family found so far. |
| **EUH1000** → v1.1 | EUH2000 / EUH2001 (batch 37) | Named only EUH1000/EUH1001 and correctly distinguished the WOH sequence — but missed that **EUH2000/EUH2001 is a parallel family at the 2000 level** (UCF, USF, Seminole State, Gulf Coast). Ironically the guide already documented the level-duplication pattern *for WOH* (WOH1012/2012, WOH1022/2022) and did not apply it to its own prefix. |
| **EVR1001C** → v1.1 | EVR2001 (batch 37) | Mentioned only EVR1001 and never addressed the **`C` versus no-`C` laboratory distinction**, which is the part that decides whether the course satisfies a laboratory-science general education requirement. Added the EVR1001C / EVR2001 / EVR2001L breakdown. |
| **ASL2150C** → v1.1, **ASL2160C** → v1.2 | ASL2140C (batch 36) | **Internal inconsistency, not an external fact.** ASL1140C and ASL1150C carried 4 cr / **80** contact hours with explicit reasoning (5–6 hrs/wk × 15 weeks); ASL2150C and ASL2160C carried 4 cr / **60** with none. Same credits, same course type, same discipline. Corrected both to 80 and added the shared justification block. **New check worth running every batch: when related-course research touches a family, compare the *numeric fields* across the family, not only the prose.** |
| **EAP1520C**, **EAP1640C** → v1.1 | EAP1500C / EAP1620C (batch 34) | Both said EAP "sequences differ" without naming the actual structure. Added the verified **level × skill grid** (hundreds digit = level, tens digit = skill) and the fact that some institutions **cap** degree-applicable EAP credit (FSCJ: 6 hours). Vagueness → precision, not an error |

**Open correction candidate — `ETI4448` (found 2026-09-02 while writing `ETI4448C`, batch 58).**
Published 2026-05-02 as **"Applied Project Management," 3 cr / 45 hrs, 10,561 chars** — an outlier by size
against the 18,000–22,000 norm, which is the same signal that exposed the MAN3554 wrong-subject guide.
Daytona State's catalog calls the number **"Project Management and Senior Design I"**: a **capstone** with
prerequisite EGN3613, a **$100 lab fee**, a required **working prototype**, a final presentation, and a
**second term** implied by the "I". The published guide mentions *capstone* only in passing and **never
mentions senior design at all**, so it reads as a project-management elective rather than the culminating
design experience the course actually is. Not a wrong-subject error like MAN3554 — the project management
content is genuine — but a **scope gap** with real advising consequence: a capstone generally cannot be
satisfied by transfer, and a student who does not know a second term follows can miss a graduation date.
**Recommend republishing as v1.1** with the senior design half, the EGN3613 prerequisite, the prototype
deliverable, and the two-term sequence. Awaiting Ron's go-ahead.

**Open correction candidate — `RTE2563C` (found 2026-09-02 while writing `RTE2573C`, batch 62).**
Published here as **"Advanced Medical Imaging," 3 credits / 60 hours**. Daytona State publishes the same
number as **"Selected Radiographic Special Procedures I" at 5 credits**, offered summer, described as
techniques *other than* diagnostic radiography — cardiac, nervous and reproductive system anatomy,
cross-sectional anatomy, and the imaging and therapeutic procedures for those systems. Its sequel
**`RTE2573C` "Selected Radiographic Special Procedures II" is 4 credits** and explicitly continues it into
surgical imaging, CT, MRI, sonography, radiation therapy, nuclear medicine, and interventional work.
Two problems: a **credit mismatch (3 vs 5)**, and a **missing sequence partner** — the published guide does
not name RTE2573C, so a student reading it would not know a second course follows. Same pattern as the
SON2122C/SON2121C and RTE2844L/RTE2854L cases. **Recommend republishing as v1.1** with the DSC credit
value, the corrected scope, and the I/II pairing. Awaiting Ron's go-ahead.

**It also fires proactively.** Batch 29: HSA4383 (batch 26) had flagged Florida's licensed health care
risk manager requirement but cited only "Chapter 395" generally. Researching **HSA4502** pinned it to
**§ 395.0197** and **§ 395.10974** with AHCA as licensing agency — so HSA4383 was republished as **v1.1**
with the exact statutes and a pointer to the course that develops the credential. Not a correction of an
error; an upgrade from vague to precise.

**And it confirms correct guides without generating spurious edits.** Batch 30 ran two checks —
PGY1800C against the published PGY2801C, and RTE1457C against Broward's RTE2457 — and **both came back
clean**: genuinely different courses at different levels, exactly as the published guides said. A check
that passes is a result, not wasted effort; it is what makes the corrections trustworthy.

**Practical rule:** when a batch contains a course in the same family as something already published —
a sequence partner, a prerequisite, a paired lecture/lab, or a second number for the same subject —
**check the published guide's cross-references against what the new research turns up.** Writing a family
of courses surfaces errors that writing any one of them alone will not.

### A note on where the variation comes from
The credit/hour/title diversity these findings document is **across Florida institutions**,
not within any one college. Daytona State appears constantly only because DSC is the
current priority list, so its catalog is the one being diffed against the statewide
inventory and against Broward, Santa Fe, Valencia, and FSCJ. DSC is usually just one data
point in the spread — the spread itself is a property of SCNS, which standardizes course
*numbers* but leaves credit values, contact hours, titles, and lecture/lab splits to each
institution. That is precisely why these guides have to check two or three catalogs.

### Where these go
Surface them to the user in the post-batch notes **and** add them here. The notes are the
review aid; this file is the memory.


---

## Batch 140 findings (2026-09-04) - HUN2201, PSY3213C, EUH1001, MAE4310, BSC4434C

### WARNING - TOOLING: the UWF catalog PDFs are fetchable but **WebFetch cannot read them**

`catalog.uwf.edu/courseinformation/courses/<prefix>/<prefix>.pdf` (lowercase) is recorded in `Tools/CLAUDE.md`
as the working UWF pattern. It is - but **WebFetch returns "the content is compressed/encoded" and no course
text**, because the PDFs use FlateDecode streams. Sending the same URL through WebFetch twice will not fix it.

**Extract them locally instead.** `pypdf` is installed on this machine (`pdfminer` and `PyMuPDF` are not):

```python
import io, urllib.request
from pypdf import PdfReader
def uwf(prefix):
    p = prefix.lower()
    url = f"https://catalog.uwf.edu/courseinformation/courses/{p}/{p}.pdf"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=90).read()
    return "\n".join((pg.extract_text() or "") for pg in PdfReader(io.BytesIO(data)).pages)
```

One fetch gives the whole prefix with full descriptions, prerequisites and credit values. **WARNING: UWF
prints course numbers with a space** - `BCN 2405C`, not `BCN2405C` - so search with `PREFIX\s*NUMBER`, or a
plain `find("BSC4434")` silently misses every course in the file.

### Reachability re-probe (2026-09-04) - the block-recovery drill

| Source | Pattern | Result today |
|---|---|---|
| **UWF** | `catalog.uwf.edu/courseinformation/courses/<prefix>/<prefix>.pdf` | OK **works**, but only via local `pypdf` extraction (above), not WebFetch |
| **Gulf Coast** | `gulfcoast.edu/catalog/current/courses/<prefix>/index.html` | OK **recovered** - full entries with credits *and* lecture hours. Best fetch-and-read source in this batch |
| **Broward** | `catalog.broward.edu/course-descriptions/<prefix>/` | FAIL still empty body - **regression confirmed, second session running** |
| **Valencia** | `catalog.valenciacollege.edu/coursedescriptions/coursesoffered/<prefix>/` | FAIL still empty body - **regression confirmed** |
| **FAMU** | `catalog.famu.edu/preview_course_nopop.php?catoid=<n>&coid=<n>` | OK **new - confirmed working.** Fourth working Acalog site after SCF, FSW and Polk |
| **SCF** | `catalog.scf.edu/preview_course_nopop.php?...` | OK still working |
| **FSW** | `catalog.fsw.edu/preview_course_nopop.php?...` | OK still working - and it published the **20-hour field experience** requirement no other catalog gave |
| **FIU** | `catalog.fiu.edu/courses/<numeric-id>` | OK still working |
| **UF** | `catalog.ufl.edu/UGRD/courses/<department_slug>/` | OK **new - confirmed working.** Full entries with credits and prerequisites. WARNING: **the department slug matters** - BSC4434C is under `microbiology_and_cell_science/`, *not* `biological_sciences/`, and the wrong slug returns a clean "not found" that reads like the course does not exist |
| **UCF** | `catalog.ucf.edu/search/?P=...` | FAIL **307-redirects to `www.ucf.edu/catalog/`**, a landing page with no course data. No usable direct pattern found |
| **FAU** | `catalog.fau.edu/search/?P=...` | FAIL HTTP 404. No usable direct pattern found |
| **USF** | `catalog.usf.edu/search_advanced.php?...` | FAIL empty body |

**Net:** three universities (UCF, FAU, USF) have no working fetch pattern. For all three, a **WebSearch
scoped to the course number returns catalog snippets carrying the credit value**, which is how the PSY3213C
credit split below was resolved. That fallback is now load-bearing for the SUS institutions, not optional.

### WARNING - `PSY3213C`: four different packagings of one course across Florida

This is the sharpest credit-count divergence recorded so far, and it is invisible from the number alone:

| Institution | Number | Credits | Shape |
|---|---|---|---|
| **FSU** | `PSY3213C` *Research Methods in Psychology with Laboratory* | **4** | integrated; prereq PSY2012 + STA2122/STA2171 + major standing; **must be done by end of Term 5** |
| **UCF** | `PSY3213C` | **4** | integrated; older catalog notation **5(3,2)** = 3 lecture + 2 lab hours - the source of the 75 contact hours used in the guide |
| **FIU** | `PSY3213` | **4** | |
| **FAU** | `PSY3213` | **3** | lecture only, no lab |
| **UNF, UF** | `PSY3213` + `PSY3213L` | **3 + 1** | split family - two enrolments, two grades |
| **UWF** | `PSY3213` + `PSY3215` | **3 + 3** | a genuine **two-course sequence**: I is descriptive methods, II is inferential. UWF I also satisfies its College-Level Communication Skills requirement |

**The trap:** a 3-credit `PSY3213` accepted against a 4-credit `PSY3213C` leaves a student a credit short
inside the major, and a programme requiring the lab may still require `PSY3213L` separately. Guide published
at **4 credits / 75 contact hours** with all four packagings documented in the Course Description.

**Statistics prerequisite also diverges** - FSU STA2122/STA2171, UWF STA2023, others accept PSY3204. STA2023
is the most portable and is the safer pick for an undeclared transfer student.

### `BSC4434C` - the `C` and the owning department both predict the content

| Institution | Number | Title | Owner | Emphasis |
|---|---|---|---|---|
| **UF** | `BSC4434C` | Introduction to Bioinformatics | Microbiology & Cell Science | web-based sequence data-mining, gene function prediction |
| **FAMU** | `BSC4434` | Intro to Bioinformatics | - | theory + practice; assembly, proteomics, expression arrays, phylogenetics |
| **FIU** | `BSC4434` | **Bioinformatics for Biologists** | - | audience marker, not a different subject |
| **UWF** | `BSC4434` | **Bioinformatics and Data Science** | **Public Health** | data organisation, data mining, **ethical protocols for data collection**, clinical problems; runs concurrently with graduate BSC5459 |

Same subject, but UWF public-health/clinical framing is a real shift in centre of gravity from UF molecular
framing. **Not a `-SCNS` / `-<INST>` split** - one subject, different emphasis - but worth watching if a third
divergent framing turns up. Documented in the guide Course Description as a variant table.

**WARNING - a credit figure was wrong in search results and caught by going to the catalog.** A WebSearch
snippet reported UF `BSC4434C` as **4 credits**; `catalog.ufl.edu` and Coursicle both give **3**, with a TR
meeting pattern of 1h55m each (~60 contact hours, the standard C-suffix figure). Published at 3/60.
*A search snippet is not a catalog.*

### `HUN2201` - a 1000-level parallel that is not an equivalent

Gulf Coast State College does **not** offer `HUN2201`. It offers `HUN1001` *Survey of Nutrition* and
`HUN1201` *Principles of Nutrition* (3 credits, 3 lecture hours). `HUN1201` is the near-equivalent, but it is
a different SCNS number and carries none of the `HUN2201` equivalency. PHSC titles `HUN2201` **"Science of
Human Nutrition"**; SCF and UWF use *Fundamentals of Human Nutrition*; Florida Poly uses *Fundamentals of
Nutrition*. Prerequisites split sharply: none at the state colleges, but **UF requires one of BSC2005/2007/
2010, CHM1025/1030/2045, APK2100C or APK2105C**.

### `EUH1001` - title drift at UWF, and the parallel-sequence advisory

UWF lists `EUH1001` as **"Western Perspectives II"** (and `EUH1000` as *Western Perspectives I*), under Social
Sciences general education. Same subject, different name - **one guide**, drift noted.

**More useful finding:** Gulf Coast states in both course descriptions that students should take **either**
`EUH1000`/`EUH1001` **or** `WOH2012`/`WOH2022`, not a mix. Mixing halves across the two survey sequences
leaves a coverage gap and may not satisfy the requirement cleanly. Also worth recording: **the periodisation
break between EUH1000 and EUH1001 is not fixed statewide** - most divide at ~1600/1648, some at 1500 or 1715
- so taking the halves at two institutions can produce a small overlap or gap around the Reformation.

### `MAE4310` - a programme course masquerading as a transferable 4000-level course

FSW is the only one of the four catalogs consulted that publishes the gating in full: *"Admission into the
Bachelor of Science in Education program or special permission from the Dean of the school of Education;
ENC 1101, ENC 1102, 3 credits of college-level mathematics, EDG 3620, EDG 3410, EDG 4004 all with a grade of
C or better"* - plus **20 hours of field experience**. UWF confirms it "is a requirement for the elementary
education teacher preparation program" and addresses **B.E.S.T. Standards for K-12 Mathematics**, and assesses
a material and supply fee. The FIU description is the thinnest of the three ("all five areas of mathematics").

**The generalisable point:** for teacher-preparation courses the binding constraint is **state programme
approval (Rule 6A-5.066, F.A.C.) plus the FTCE subject-area examination**, not course-level SCNS articulation
- the same structure already documented for nursing (NCLEX + Board approval) and MLS (NAACLS + ASCP). A
student who accumulates the right courses outside an approved programme still cannot be certified. Cohort
locking applies too: the methods block runs once a year, so one failed course costs a year, not a term.

**WARNING - do not confuse `MAE4310` with `MAE4320`.** UWF: `MAE4310` *Teaching Mathematics in Elementary
Schools*, `MAE4320` *Teaching Mathematics in Middle and Secondary Schools*. Different certification areas,
adjacent numbers - an easy mis-pick.


---

## Batch 141 findings (2026-09-04) - BCN2405C, GEA2000, HSA3111, ECO3101, HSA3170

### WARNING - `ECO3101`: UF awards 4 credits and requires calculus; everyone else awards 3

| Institution | Credits | Prerequisites |
|---|---|---|
| **UF** | **4** | ECO2023 **and** (MAC2233 or higher calculus), or AEB3103 |
| **FSU** | 3 | ECO2013 and ECO2023 |
| **UCF** | 3 | ECO2013 and ECO2023 |
| **UWF** | 3 | (ECO2013 AND ECO2023) OR ECO3003 - no calculus |

Two distinct risks. The **credit gap** (3 accepted against 4 leaves a student short inside the major) and,
more substantively, the **mathematical-level gap**: a calculus-prerequisite section derives marginal
conditions by differentiation and treats Lagrangians as ordinary; a non-calculus section does the same
results graphically. **Invisible on a transcript.** Published at 3/45 (the majority) with the UF variant
flagged in the Course Description and a standing recommendation to take calculus regardless.

### `BCN2405C` - two statewide titles for one course (see REVIEW_QUEUE item 12, now resolved)

`BCN2405C` "Construction Mechanics" (UF, FGCU) and `BCN2405` "Statics and Strength of Materials"
(UWF, Gulf Coast) are **the same course**. UWF's `BCN3561` "Construction Mechanics" is the upper-division
level partner, not a duplicate - the EGN2312/EGN3311 pattern again.

**Prerequisite divergence is the transfer trap here, and it is a mathematics-course mismatch:**
UF requires **MAC3233** (survey of calculus); UWF requires **MAC1114** (trigonometry). These are different
courses and do not substitute for each other in either direction. FGCU gates on physics plus BCN1930
(a programme course).

**New: ACCE accreditation.** UF maps this course's outcomes to **American Council for Construction Education
student learning outcomes** (chiefly SLO 19 structural behaviour, SLO 8 materials). ACCE accredits
construction management programmes; add it to the register of Florida programmatic accreditors alongside
ABET, NAACLS, CCNE/ACEN, CAHME/AUPHA and CAEP/FLDOE.

**Engineering boundary worth stating in any BCN guide:** BCN2405C does **not** substitute for EGN2312/
EGN3311 (statics) or EGN2332C/EGN3331C (mechanics of materials) in an engineering programme. Same asymmetry
already documented for engineering-technology calculus.

### WARNING - `GEA2000`: three different titles, one of them actively misleading

| Institution | Title |
|---|---|
| statewide, SCF, USF, Santa Fe | **World Regional Geography** |
| **UWF** | **Nations and Regions of the World** |
| **FGCU** | **Introduction to Geography** |

FGCU's title is the dangerous one: "Introduction to Geography" elsewhere usually means a *systematic*
survey, a different organising principle from a *regional* one. FGCU's description ("comparative analysis of
representative regions of the world") confirms it is the regional course. **One guide.**

**Prefix rule worth reusing:** `GEA` = regional geography, `GEO` = systematic human geography
(GEO2200 physical geography is a *natural science* credit at many institutions, not social science).
A student can pick the wrong general-education box by choosing the wrong prefix.

### `HSA3170` - the prerequisite predicts the course you get

| Institution | Title | Prerequisite | Emphasis |
|---|---|---|---|
| **SCF** | Health Care Finance | **HSA3111** | finance built on the health-systems survey |
| **FAMU** | **Financial Management in Health Care** | **ACG2021 and ACG2071** | accounting-grounded managerial finance |
| **UWF** | **Principles of Healthcare Finance** | none listed | introduction for entering administrators |

Credits are stable at **3** across all institutions - no credit-count risk here. The divergence is entirely
in what the course assumes you already know. This "prerequisite predicts emphasis" pattern is worth checking
on every professional-programme course; it is a softer version of the BSC4434 owning-department finding from
batch 140.

### `HSA3111` - the major restriction blocks more students than the prerequisite

UWF lists **no prerequisite**. UF requires BSC2007 or BSC2010, APK2105C, STA2023 and PSY2012 **and restricts
enrolment to majors and minors or by departmental permission**. The restriction, not the prerequisite list,
is what actually stops a transfer or cross-listed student from enrolling - and it does not appear in the
inventory or in a transcript-level articulation check. **Worth surfacing in any guide for a professional
prefix (HSA, NUR, MAE, BCN).**

Titles: *US Health Care Systems* (statewide, UCF), *U.S. Health Care System* singular (UF),
*Understanding U.S. Healthcare* (UWF).

### Florida policy facts used across the two HSA guides (verify before reuse after 2027)

- Florida has **not expanded Medicaid** under the ACA -> persistent coverage gap, higher uncompensated care
  and bad debt in hospital financials. This is a live, teachable payer-mix example.
- Florida Medicaid runs almost entirely through **statewide managed medical assistance** contracts (AHCA).
- Florida **repealed most hospital certificate-of-need requirements in 2019**.
- Florida's age structure gives **Medicare and Medicare Advantage** an outsized revenue share versus the
  national average.
- **AHCA publishes hospital financial data publicly** via FloridaHealthFinder.gov - which makes Florida an
  unusually good state for the ratio-analysis project HSA3170 sections commonly assign.

### Source notes from this batch

- **`catalog.ufl.edu/UGRD/courses/<slug>/` confirmed again** - `economics/` returned ECO3101 in full. The
  department-slug caveat from batch 140 holds.
- **`catalog.ucf.edu/preview_course_nopop.php?...` 307-redirects to `www.ucf.edu/catalog/?...`, which returns
  a landing page.** So UCF is unreachable by *both* its Acalog course URLs and its `/search/` path. Confirmed
  twice now. Use scoped WebSearch for UCF.
- **`catalog.sfcollege.edu/preview_course_nopop.php?...` returned 404** on two different catoid/coid pairs
  surfaced by search. Santa Fe is search-indexed but not fetch-readable at those ids - do not spend fetches
  on it without a freshly surfaced id.
- **`catalog.scf.edu` (State College of Florida) still working** - supplied GEA2000 and the HSA3170
  prerequisite. Fifth confirmed working Acalog site.
- **UF publishes course syllabi as PDFs at predictable department paths** (`dcp.ufl.edu/wp-content/uploads/`,
  `my.education.ufl.edu/course-syllabi/`, `psych.ufl.edu/wp-content/uploads/`). WebFetch cannot read them -
  same FlateDecode problem as the UWF catalog - **but WebFetch saves the binary to the session tool-results
  directory, and `pypdf` reads it from there.** The UF BCN2405C syllabus gave grading weights, the textbook,
  the lab schedule and the ACCE outcome mapping, none of which is in any catalog. **This is the single most
  productive source type found in two batches.**


---

## Batch 142 findings (2026-09-04) - LAH2020, MAA4402, MAS4301, CCJ3666, CES4702C

### WARNING - PUSH FAILURE MODE: a missing taxonomy prefix returns HTTP 422, not a validation error

`CES4702C` validated clean and still failed to push with **422 Unprocessable Entity**. The draft was
correct; `CES` simply has no taxonomy leaf, so `ExtractCoursePrefix` cannot resolve it and the server will
not create the course. **A 422 on push with a clean `validate_drafts.py` run means a missing taxonomy node -
do not go looking for a content problem.** Diagnose it in one call:

```bash
curl -s https://floridacourserepo.com/api/v1/courses/<ID>          # COURSE_NOT_FOUND => prefix unresolved
grep -c '"CES"' PreseMakerRepo.Api/Data/Seed/taxonomy.json          # 0 => confirmed
```

**Sweep the whole queue before it bites again.** Comparing queued rows to the 597 three-letter leaf keys
found **14 blocked rows across 4 prefixes, all civil/environmental**: `ENV` (6), `CWR` (3), `CEG` (3),
`CES` (2). All belong under the existing `CIVIL_ENVIRONMENTAL_` parent, which already holds CCE, CGN and
TTE. Logged as REVIEW_QUEUE item 13. **This sweep is worth re-running whenever a new prefix family enters
the queue** - it is cheap and it converts a mid-batch push failure into a prerequisite.

### TOOLING - FGCU IS UNBLOCKED. The PDF works; it was WebFetch that could not read it

`SOURCES.md` records FGCU as bot-blocked (202 empty) and "search-readable, not fetch-readable". **That is
wrong now, and it was the wrong diagnosis.** `https://catalog.fgcu.edu/courses/<prefix>/<prefix>.pdf`
downloads fine and `pypdf` extracts it - same fix that unblocked the UWF catalog in batch 140. Confirmed on
five prefixes in one session (LAH, CES, CCJ, MAA, MAS), each returning full descriptions, credits,
prerequisites **and general-education attribute codes**, which no other Florida source publishes so plainly.

**Generalise the lesson:** an "empty 202 / cannot read" result from WebFetch on a `.pdf` URL is evidence
about *WebFetch*, not about the source. **Re-probe every source in the register that was written off on a
PDF fetch.** Gulf Coast, Valencia and Broward are HTML and are genuinely unaffected, but any catalog with a
`.pdf` variant deserves a retry through `pypdf` before being recorded as blocked.

Reusable helper is at `scratchpad/pdfget.py`; the core is a `urllib` request with a browser User-Agent into
`PdfReader`. Two gotchas: **UWF prints numbers with a space** (`BSC 4434`) and **FGCU embeds ligatures**
(`\ufb01`) that crash printing under the Windows cp1252 console - normalise with
`unicodedata.normalize("NFKD", txt).encode("ascii","replace").decode()` before printing.

### FGCU publishes general-education attribute codes - a source of a kind nothing else gives

FGCU's course PDFs carry an `Attribute(s):` line. For `LAH2020`: **CLWS** (College-Level English Language
Writing), **GESO** (Gen Ed - Social Science), **WCOM** (GE Written Communication Competency). This settles
questions that otherwise need guesswork, and it turned up a genuinely useful finding: **LAH2020 is a writing
course as well as a history course** at several institutions (UF also uses it for Written Communication).
Students pick it as an easy social-science elective and meet a graded writing load. **Check the FGCU
attribute line on every general-education course from now on.**

### `MAA4402` - three titles, and the differential-equations prerequisite is not universal

| Institution | Title | Prerequisite |
|---|---|---|
| statewide, FGCU | **Complex Variables** | FGCU: MAC2313 **and MAP2302** |
| **UF** | **Functions of a Complex Variable** | (MAC2313 or MAC3474) **and MAP2302**, min grade C |
| **UWF** | **Analytic Functions** | MAC2313 only |

UWF's title is the trap - "Analytic Functions" also names real-analysis and graduate complex-analysis
content, so a student can fail to recognise their own required course in the catalog. Published at 3/45.

**A second, invisible divergence worth recording:** this course runs as either a **proof-oriented** or an
**application-oriented** class under the same number. UWF says so outright ("parts of the theory ... that
are prominent in applications"); FGCU's listing of Riemann surfaces and the Riemann mapping theorem signals
the opposite. Nothing on a transcript distinguishes them, and a student headed for graduate school needs the
proof version. Same shape as the PSY3213C packaging finding from batch 140.

### WARNING - `MAS4301`: the proofs prerequisite is a different SCNS number at each institution

| Institution | Prerequisite |
|---|---|
| **UF** | MAS3300, **or MHF3202 with a minimum grade of B**, or MAS4105 with a minimum grade of C |
| **UWF** | MHF3202 |
| **FGCU** | **MHF2191** - a *2000-level* intro to advanced mathematics |

**MHF2191 and MHF3202 are different numbers and SCNS equivalency does not cross numbers.** A student who
satisfies FGCU's prerequisite may be asked to repeat at the 3000 level elsewhere. UF's **minimum grade of B**
is also unusual and is a deliberate difficulty signal - worth quoting in guides for gateway proof courses.

Also recorded: FGCU runs **MAS4302 Abstract Algebra II** ("emphasis on skills and topics needed for graduate
study"), so at FGCU the first course is genuinely a first half; institutions without a second course
compress. Groups-first vs rings-first is a further real ordering difference (Gallian/Fraleigh vs Hungerford).

### `CCJ3666` - sensitive-content handling, and Florida-specific law that national texts miss

Handled per the `Tools/CLAUDE.md` mental-health-adjacent rule: the guide opens with a plain statement of what
the course covers, and lists **usable** resources rather than gesturing at support - 988, the Florida
Domestic Violence Hotline (1-800-500-1119), RAINN (1-800-656-4673), the Florida Abuse Hotline
(1-800-962-2873), the National Human Trafficking Hotline, and the Florida Attorney General's **Bureau of
Victim Compensation**.

**Three Florida legal facts that differ materially from the national textbook treatment**, and that belong in
any Florida victim-services or criminal-justice guide:
1. **Article I, Section 16 of the Florida Constitution** (Marsy's Law, adopted 2018) gives victims
   enumerated *constitutional* rights, and has generated live litigation over withholding victim identities.
2. **Florida mandatory reporting binds all persons**, not only designated professionals - broader than most
   states, and directly relevant to students in health and education programmes.
3. Florida's demographics make **elder abuse and financial exploitation of older adults** far more salient
   than national texts suggest.

### `CES4702C` - the C suffix is the minority, and credits are stable

| Institution | Number | Title |
|---|---|---|
| **FGCU** | **CES4702C** | Reinforced Concrete Design |
| **UWF** | CES4702 | Reinforced Concrete Design |
| **UF** | CES4702 | **Analysis and Design in Reinforced Concrete** |
| **USF** | CES4702 | **Concepts of Concrete Design** |
| **Florida Poly** | CES4702 | Reinforced Concrete Design |

3 credits everywhere, so no credit-count risk. Published at **3/45** (the majority lecture pattern) and
`validate_drafts.py` raises its expected non-blocking C-suffix contact-hour warning - **that warning is
correct to ignore here** and the guide explains why. Note the prerequisite pairing: analysis *plus* a
materials course at both FGCU (CES3100C + CCE3101C) and UF (CES3102 + CGN3501C), and **UF restricts
enrolment to engineering majors**, which blocks construction-management students.

**Florida practice context used in the guide, worth reusing for any structural course:** wind rather than
seismic governs (ASCE 7 + Florida Building Code, with the High-Velocity Hurricane Zone in Miami-Dade and
Broward); **chloride-driven reinforcement corrosion** is the dominant durability problem in coastal
exposure; and the post-Surfside **milestone inspection and structural integrity reserve study**
requirements have created sustained demand for assessment of *existing* reinforced concrete - a different
skill from new design.
