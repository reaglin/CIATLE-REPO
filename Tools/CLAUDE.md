# CLAUDE.md — Florida Course Repository Curriculum Guide Pipeline

This file conditions Claude sessions working on the [floridacourserepo.com](https://floridacourserepo.com) project. Read this before doing anything else. For tooling and command-line workflow, also read `README.md` in this directory.

---

## Project mission (the only thing that really matters)

**Develop solid, factually accurate curriculum guides for Florida college courses.** Every other concern — workflow, schema, file naming — is in service of this. A guide is "solid" when:

- It accurately reflects what Florida colleges actually teach for the course, derived from the SCNS framework and college catalogs.
- Required outcomes/topics reflect content common across institutions; optional outcomes/topics reflect institutional variation.
- It hedges honestly on uncertainty (especially for courses offered at few institutions).
- It cites Florida-specific context (FE/PE pathway, SCNS articulation, Florida industries, Florida-specific employer/regulatory landscape) where relevant and verifiable.
- It omits sections it cannot substantiate rather than fabricating content.

If a session ever drifts toward producing volume over quality, return here.

---

## Workflow: run it from this repo

Guides are written **directly into `Tools/drafts/`** from a Claude Code session in
`CIATLE-REPO`. The old chat → "Download All" → ZIP → `import_zip_to_drafts.ps1` bridge is
**no longer part of the loop**, and neither is the `Set-ExecutionPolicy` step that existed
only to let that importer run. Both still work if a batch ever arrives from a claude.ai
chat, but nothing here depends on them.

The `/guide` skill (`.claude/skills/guide/SKILL.md` at the repo root) drives the loop.
Do not skip the confirmation step.

1. **Identify the next candidates** — `python queue_mgr.py next-batch --n 5`. `queue.csv`
   is authoritative; `courses_2plus_institutions.csv` is the inventory it draws from.
2. **Present the proposed batch as a table** — course ID, institution count, title, notes.
   Flag any uncertainty (generic titles, content variation risk, low institution count).
3. **Wait for confirmation.** The user may approve, substitute, or remove items. Common
   reasons to substitute: faculty requests, non-public-college institutions, BAS courses
   that aren't true engineering courses.
4. **Write each guide** to `drafts/{COURSE_ID}_guide.json`. Research first — SCNS framework
   and Florida college catalogs — then write. Batch size is a judgment call; the old cap of
   5 came from chat output limits that no longer apply.
5. **Validate** — `python validate_drafts.py {IDS}`. This mirrors the server rules exactly,
   so a clean run means the push will not come back 400. **Never push past a `FAIL`.**
6. **Reconcile and push** — `python queue_mgr.py reconcile`, then
   `python generate_guide.py --push-from-queue --yes`.
7. **Confirm** — `python queue_mgr.py status`, and spot-check
   `https://floridacourserepo.com/api/v1/courses/{ID}/guide`. (`curriculumGuideUrl` staying
   `null` on the course endpoint is normal — it only populates once a course has published
   modules.)
8. **Provide sanity-check notes** in a brief table: course, credits, contact hours, file
   size — followed by short bullets flagging anything worth review (unusual hour counts,
   generic titles, novel content, institutional variation).

When in doubt about scope, **err toward fewer high-quality guides over more rushed ones.**

---

## ⚠⚠ The course catalog — deployed 2026-09-11. Read this before the first batch.

**What changed:** a course no longer has to have a guide. The site now lists **every course that exists**,
with or without one, and visitors press **Request Guide** on the ones that are missing. The contract is
[`COURSE_API.md`](COURSE_API.md) (courses) and [`RESOURCE_API.md`](RESOURCE_API.md) (resources); the
server-side plan is `COURSE_CATALOG_PLAN.md` at the repo root. **Guide content rules did not change** —
everything below this section still governs what a guide says.

### ⚠⚠⚠ Visitor guide requests are the new top priority

Requests are one anonymous click on a guide-less course page. **They are the strongest demand signal the
project has ever had — a named person wanted that guide** — and they outrank everything except a faculty
request. Read them with no token:

```bash
curl -s "https://floridacourserepo.com/api/v1/queue/guides?status=waiting"   # most-requested first
```

Each item carries `rank, courseId, title, requestCount, firstRequestedUtc, status, hasGuide, isListed`.
The same list is public at `https://floridacourserepo.com/queue/guides`.

⚠ **`isListed: false` means someone asked for a course the site does not list yet.** Send its base data
(§ below) before or with the guide, or the request has nothing to attach to.

**Check this queue at the start of every session**, before `queue_mgr.py next-batch`. A published guide
closes its requests automatically; `queue_mgr.py import-requests` still works and still marks them `Queued`.

### ⚠⚠ Send the course's base data with every guide

A guide push still creates a missing course — but with **the course id as a placeholder title**, which is
why so many pages read `EEE3300` instead of *Electronics I*. Fix it in the same batch:

```
POST /api/v1/courses/batch      # ≤ 500 courses, each validated on its own
PUT  /api/v1/courses/{courseId} # one course
```

```json
{ "courseId": "CET1112", "title": "Digital Electronics and Microprocessors",
  "stateTitle": "DIGITAL ELECTRONICS & MICROPROCESSORS", "creditHours": 3, "contactHours": 45,
  "offerings": [ { "institution": "DSC", "title": "DIGITAL ELECTRONICS & MICROPROCESSORS", "credits": 3 } ],
  "replaceOfferings": true }
```

Field rules that bite:

| Field | Rule |
|---|---|
| `courseId` | `^[A-Z]{3}\d{4}[A-Z]?(-(SCNS\|[A-Z]{2,5}))?$` — **the `-SCNS` / `-<INST>` split is in the contract**, so a variant id is a first-class course |
| `title` | **required**, ≤ 300, written as sent. Sending the course id as the title never replaces a real one |
| `creditHours` / `contactHours` | **0–20 / 0–3000 on the COURSE** — wider than the guide's own 0–12 / 0–1500. A PSAV clock-hour course is still `credits: 0` in the **guide** |
| `offerings[]` | ≤ 250; `institution` is a short code, with that school's own `title`, `credits` and `clockHours`. **This is where the institution list finally lives on the site — and it is the same per-school data the guide's hours table must be built from** (see *RESOLVE THE RANGE* below; build both in one pass so they agree) |
| `replaceOfferings` | defaults to **`true`** — omitted offerings are **deleted**. Send the whole list or pass `false` |
| null / omitted | left unchanged on an existing course (except `title`) |

⚠ **Never `DELETE` a course that has a guide** — it returns `409 COURSE_HAS_CONTENT`. A course that stopped
being offered gets `isActive: false`.

⚠ **Send institutions first**, with names: `POST /api/v1/institutions/batch` with `{code, name, sector,
scnsId}` (SCNS `institution_map()` supplies them), or the site shows bare codes.

### The 806 guide-less courses already on the site

The deployment found **806 courses with no guide already in the database, and every one of them is an
Engineering Technology prefix** — which is exactly Ron's priority scope (2026-09-09):

| ETI | CET | EET | ETS | ETD | ETP | TDR | EEV | ETC | ETM | ETG | EER |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 147 | 141 | 112 | 88 | 78 | 66 | 40 | 36 | 35 | 33 | 18 | 12 |

They carry real titles but **no offerings at all** (`offeringCount: 0`), so the institution data has to be
sent. Known bad data to correct while passing through: **`EEV0360L` has `creditHours: 30`** (those are clock
hours — PSAV, so `credits: 0` + `contactHours: 30`) and **`ETC5605` is graduate-level**.

⚠ **Prefix completion (2026-09-09) applies to these**: `hasGuide=false` on the catalog endpoint is now a
better prefix worklist than `queue.csv`, because it is what the site actually shows a visitor as missing.

```bash
curl -s "https://floridacourserepo.com/api/v1/courses/catalog?prefix=CET&hasGuide=false&pageSize=1000"
```

### A stub is not a guide

Publishing modules for a course with no guide creates a placeholder guide titled **`Not Completed`**
(`CurriculumGuide.StubTitle`). It never counts as a guide and never blocks a guide request, and the
`hasGuide` filters ignore it. **Do not treat a course as done because it has a guide row.**

### Course resources are a second, separate loop

Visitors and vendors suggest links on `/courses/{id}/resources`; an AI session reviews them, writes the
summary and lists them. That loop is **`RESOURCE_API.md` + `resources/APPROVAL_RULES.md` + the `/resources`
skill** — not this file. It does not interleave with guide writing; run it as its own session.

---

## Priority hierarchy

Apply in this order:

1. **Faculty requests** always go to the top of the queue. These are unpredictable and come up mid-session. When the user says "add EGN3214 because a faculty member requested it," that course supersedes the strict-priority pick. Custom specifications from faculty (e.g., "Python only, AI-integrated, two-half structure") are followed precisely.
2. **⚠⚠ Visitor guide requests** (new 2026-09-11) — `GET /api/v1/queue/guides?status=waiting`, most-requested first. Someone pressed **Request Guide** on a course page because they wanted it. **Check this queue before every batch**; a request outranks any catalog-derived row. See the course-catalog section above.
3. **Engineering and Engineering Technology prefixes**, completing each prefix, per Ron's 2026-09-09 direction below — single-institution courses included.
4. **Strict priority by institution count** (descending) within `courses_2plus_institutions.csv`, with course ID as tiebreaker. Higher institution count = wider applicability = stronger signal that the guide will help more students.
5. **Human judgment overrides.** The user may demote or remove courses for reasons including:
   - Course offered only at non-Florida-public institutions (e.g., Keiser private, FL Tech private). The repository serves Florida public colleges and SUS institutions. ⚠⚠ **Settled 2026-09-11, and it now governs SEARCH as well as selection:** *"In doing search and fetch to determine eligibility for a curriculum guide we will only do public institutions&hellip; we are not adding private institutions as part of our adding data."* So **a private institution's offering is not a reason to write a guide, and is not added to a course's offerings either.** ⚠ **A visitor request overrides it:** *"If one happens to make it up to the list and gets queued for a guide, we will override the rule and supply one."* The override is applied by **queueing that course**, never by widening the filter.
   - Course is part of a BAS or applied-degree program that isn't a true engineering degree (Engineering Technology BAS courses are fine; non-engineering BAS courses that happen to use an engineering prefix are out of scope).
   - Course is a shell (internship, special topics, independent study, thesis, dissertation, supervised research). Default is to skip these.
6. **When uncertain, ask.** Never silently substitute. Confirm before generating.

---

## Schema (required JSON structure)

Every guide is a JSON file with these six required top-level keys, plus the optional
**`offering_notes`** (below):

```json
{
  "title": "Short descriptive guide title",
  "html_content": "<full HTML — see conventions below>",
  "credits": 3,
  "contact_hours": 45,
  "prerequisites": "MAC2311 or equivalent" | null,
  "version": "1.0"
}
```

### ⚠⚠ `offering_notes` — the seventh field (Ron, 2026-09-11)

**An additional field carrying, per school, the title THAT school uses and the hours it requires.** It is
the structured form of the *RESOLVE THE RANGE* rule below: the six scalars describe the course, and this
describes where it is actually taught.

```json
"offering_notes": {
  "summary": "All five institutions carry it at 3 credits. No institution publishes a contact-hour figure.",
  "hours_source": "derived",             // published | derived | mixed
  "derived_contact_hours": 60,
  "derivation": "Florida convention: 45 hours for a 3-credit lecture course, 60 for a 3-credit C course.",
  "offerings": [
    { "institution": "GCSC", "institution_name": "Gulf Coast State College",
      "title": "Digital and Computer Circuits", "credits": 3, "contact_hours": null,
      "note": "Offered spring term only. Prerequisite MAC1105 and EET1084C, minimum grade C." }
  ]
}
```

- ⚠⚠ **PUBLIC institutions only** (Ron, 2026-09-11, superseding his earlier answer): list the Florida
  College System and State University System offerings. **A private, career or out-of-state institution
  carrying the SCNS number is not added.** Filter with `scns.is_public(code)`.
- ⚠ **No `sector` field.** `Institution.Sector` on the site is the owner of that fact (Ron, 2026-09-11) —
  the guide JSON carries the institution code and the site joins. `scns.sector_of()` still exists for
  filtering and for checking a code, but its value does not go in the draft.
- ⚠⚠ **`credits` is an INTEGER.** The SCNS flat file writes `3` and `3.0` for the same value — that is a
  fixed-width export artefact, not a difference. `mkguide.py` coerces a whole float; `validate_drafts.py`
  **rejects a non-integer credit outright**. A genuine in-school range (`3-4`) leaves `credits` null and
  says so in `note` — **Ron settled this on 2026-09-11: the note is sufficient, no min/max pair.**
  Instances so far: `CET1178C` is 3-4 at South Florida State, `CET2949` is 1-4 at Daytona State; both are
  variable-credit capstone or special-topics numbers.
- `title` is **that institution's own title**, not the statewide one — the divergence signal, and the thing
  a student actually sees on a schedule.
- `contact_hours` per school is the **published** figure or null. Never put a derived figure in a school's
  row: derived numbers go in `derived_contact_hours` with `hours_source: "derived"` and the `derivation`
  spelled out.
- ⚠ **The server does not carry this field yet.** `PUT /courses/{id}/guide` takes the six scalars and drops
  anything else, so a draft carrying `offering_notes` publishes normally and the field simply does not
  appear on the site until the server change lands (`Deployment/PENDING_SERVER_CHANGES.md`). **Until then,
  write the same content into the guide HTML as an `<h3>Offering Notes</h3>` section too** — that is what
  readers see today, and it makes the later retro-fit a mechanical extraction.
- **Source it from the SCNS flat file**, which carries per-institution `credit`, `clock_hours` and
  `inst_title` for every offering. ⚠ Its titles are **all upper-case**: when title-casing them, test small
  words (`and`, `of`, `the`) **before** any "short and upper-case means acronym" heuristic, or the heuristic
  fires on `AND` and `THE`. An all-caps source carries no case signal.

⚠ **Existing guides do not have this field.** Ron, 2026-09-11: *"we will have to go back and redo a lot of
the old guides, but that will be a task for much later."* **Do not start a retro-sweep** — add the field to
new guides and to any guide being republished for another reason.

---

- `credits=0` is valid for PSAV (Postsecondary Adult Vocational) clock-hour courses; `contact_hours` carries the real measurement.
- `prerequisites` is a single string or null. Be specific (course numbers, grade requirements, standing requirements). Where prerequisites vary by institution, say so explicitly.
- `version` starts at "1.0" and increments only when a guide is materially updated.

**Hard limits the server enforces.** A guide that breaks one of these is rejected with an
HTTP 400 (`PublishValidators.cs`, `UpsertCurriculumGuideRequestValidator`):

| Field | Limit |
|---|---|
| `title` | non-empty, ≤ 300 chars |
| `html_content` | non-empty |
| `credits` | integer **0–12** — never null (`push_guide` rejects null before the server sees it) |
| `contact_hours` | integer **0–1500** |
| `prerequisites` | ≤ **1000** chars, or null (raised from 500 on 2026-09-11) |
| `version` | ≤ 50 chars |

⚠️ **Never copy a PSAV clock-hour count into `credits`.** Set `credits: 0` and put the
hours in `contact_hours`. That single mistake stalled 11 guides for months. Run
`python validate_drafts.py` to catch it — and every other limit above — before pushing.

---

## HTML content conventions

`html_content` contains **inner content only** — no `<html>`, `<head>`, `<body>`, or `<style>` tags. Bootstrap classes are available; keep markup clean.

**Section structure (canonical order):**

1. **Course Description** — `<h2>` heading. Multiple `<p>` paragraphs covering what the course is, where it sits in the SCNS taxonomy, who takes it, and the institutional adoption pattern (e.g., "offered at approximately 8 Florida institutions").
2. **Learning Outcomes** — `<h2>` with two `<h3>` subsections: **Required Outcomes** (common across institutions) and **Optional Outcomes** (institutional variation). Use `<ul class="list-group list-group-flush"><li class="list-group-item">` for outcome lists.
3. **Major Topics** — `<h2>` with two `<h3>` subsections: **Required Topics** and **Optional Topics**. Same `list-group` markup as outcomes.
4. **Resources & Tools** — `<h2>`. Plain `<ul><li>` (not list-group). Cover textbooks, online platforms, software, lab equipment, reference standards/organizations.
5. **Career Pathways** — `<h2>`. Plain `<ul><li>`. Specific career titles where possible; SOC codes where useful; Florida industry context.
6. **Special Information** — `<h2>` with `<h3>` subsections covering: certification preparation, articulation/transfer notes, FE exam preparation (where applicable), course format, position in curriculum, prerequisites narrative, course-code variations across Florida.
7. **AI Integration (Optional)** — `<h2>` — *new section, growing in importance*. Address the substantive use of AI tools in the course's domain: what AI tools are commonly used, where they help, where they fail, the engineer's responsibility for AI-assisted output, academic integrity considerations. Include where:
   - The course's content area now naturally involves AI tools (programming, data analysis, design, writing)
   - Faculty have specifically integrated AI tools into the course
   - Industry practice in the course's domain has substantively shifted toward AI-augmented work
   
   Skip this section where AI integration is not yet substantive for the course (e.g., foundational physics, theoretical mathematics) — but expect this to expand over time as faculty AI integration grows.

**Markup conventions:**
- `<h2>` for sections, `<h3>` for subsections
- `<p>` for paragraphs (prose, not bulleted lists for explanation)
- `<strong>` for key terms on first introduction
- `<em>` for textbook titles
- `<ul class="list-group list-group-flush"><li class="list-group-item">` for outcome and topic lists (Bootstrap-styled)
- `<ul><li>` for resource and career lists (plain)
- Avoid HTML entities where Unicode works (en-dash, em-dash, mathematical symbols are fine as Unicode)

**Omit a section rather than fabricate.** If you cannot substantiate Career Pathways for a niche course, omit the section. Leave a brief sentence in Course Description acknowledging the limit if useful.

---

## Florida pedagogy conventions

**SCNS course code patterns:**
- `XXX1xxx`/`XXX2xxx` = sophomore (lower-division)
- `XXX3xxx`/`XXX4xxx` = junior/senior (upper-division)
- `XXX5xxx`/`XXX6xxx` = graduate
- `XXX0xxx` = postsecondary adult vocational (PSAV/clock-hour)
- `XXX9xxx` = special topics/internship/thesis (shell — skip by default)
- Suffix `C` = integrated lecture+lab (typically 60 contact hours for 3 credits)
- Suffix `L` = lab-only (typically 1 credit / 30-45 hours)
- No suffix = lecture-only (typically 45 contact hours for 3 credits)

**Sophomore/junior course pairs are common.** When you see two course codes with similar titles at different levels, they're often the same content at different curriculum positions:
- Statics: EGN2312 (sophomore) ↔ EGN3311 (junior)
- Dynamics: EGN2322 (sophomore) ↔ EGN3321 (junior)
- Mechanics of Materials: EGN2332C (sophomore) ↔ EGN3331C (junior)
- Engineering Economics: EGN2610 (sophomore) ↔ EGN3613 (junior)

When writing one variant, cross-reference the other and note that programs typically use one consistently with their statics/dynamics positioning.

**Transfer vs. PSAV vs. Engineering Technology:**
- **Transfer courses** (engineering majors, A.A./A.S. transfers): cite SCNS articulation, note general-education satisfaction where applicable, mention FCS+SUS transfer pathway.
- **PSAV courses** (clock-hour, certificate programs): credits=0, no transferability claims, FLDOE Curriculum Framework + CIP code citations, Florida DBPR/Board for licensure pathways. Different audience, different treatment.
- **Engineering Technology courses** (BAS programs): articulation is asymmetric — engineering tech calculus (EGN2045/EGN3046) typically does *not* satisfy MAC2311/MAC2312 for engineering transfer. Flag this honestly.

**Hedging language by institution count:**
- 8+ institutions: confident, definitive language. Content is well-validated.
- 4-7 institutions: confident with light hedging where appropriate.
- 2-3 institutions: explicit hedging — "varies by institution," "students should consult their specific institution," "content may emphasize X at some institutions and Y at others." Use Optional Outcomes / Optional Topics generously.
- 1 institution (faculty request only): treat as a custom guide for that institution. Apply faculty specifications precisely.

**Always include where applicable:**
- FE/PE exam relevance (the FE exam is the gateway to PE licensure; topics that appear on FE exams should say so)
- ASTM/ANSI/ASME standards by number where they govern the content
- Florida-specific employer landscape (aerospace at Space Coast, defense at Lockheed/Northrop/L3Harris, healthcare at AdventHealth/Orlando Health/BayCare, hospitality engineering at Disney/Universal, marine/ocean industry, agtech)
- Difficulty/time-commitment honesty for demanding courses (mechanics-of-materials, fluids, thermo, dynamics all warrant 8-12+ hours/week)

---

## Sanity-check patterns

After generating, surface anything in this list to the user as part of the post-batch notes:

- **Credit/hour mismatches.** 3-credit lecture should be ~45 hours; 3-credit "C" integrated should be ~60 hours; 1-credit "L" lab should be ~30-45 hours. Anything outside these ranges deserves a flag.
- **Generic titles** ("Engineering Analysis," "Foundations of Engineering," "Special Topics") signal content variation risk. Note this for the user.
- **Single-institution courses** (faculty requests) — flag the novel content for closer review.
- **Course-code variation across Florida** — flag where the same content is taught under different prefixes (e.g., fluid mechanics under EGN3353C vs. EML3xxx vs. CWR3xxx).
- **Articulation gotchas** — engineering tech calculus, terminal courses, courses with non-standard credit counts.
- **Mental-health-adjacent content** — health programs, counseling courses, courses touching difficult subject matter — verify the content is supportive and resource-pointing rather than triggering.

---

## File conventions

- **Output filename**: `{COURSE_ID}_guide.json` exactly. Course ID is uppercase, no spaces. `queue_mgr.py reconcile` matches drafts to queue entries by extracting the course ID from the filename, so don't rename them.
- **Output directory**: `Tools/drafts/` — write guides straight here. This is the same directory the push reads from; there is no staging step.
- **Never write a `.py` or `.ps1` file named after a stdlib module** (`queue`, `csv`, `json`, `email`, …) into this directory — it shadows the real module and breaks `requests`/`urllib3`. That is why the queue tool is `queue_mgr.py`; don't rename it back.
- **`REVIEW_QUEUE.md`** holds findings that need Ron's decision before acting — correction candidates on already-live guides, and scope calls like the skip list. **Add to it whenever a batch turns one up, rather than only mentioning it in the batch report**, and move items to its Resolved section once a decision lands. Findings and evidence still go in `SOURCES.md`; `REVIEW_QUEUE.md` is the short actionable list that points back to it.

---

## What to skip (default)

Shell-style courses in any prefix, unless the user says otherwise:
- `XXXX900`, `XXXX905`, `XXXX910` — independent study / directed individual study
- `XXXX920`, `XXXX930` — **special topics / selected topics** (added 2026-08-31)
- `XXXX940`, `XXXX941`, `XXXX945`, `XXXX949` — internship / cooperative education
- `XXXX950`, `XXXX951` — special topics
- `XXXX971`, `XXXX973` — thesis
- `XXXX980`, `XXXX981` — dissertation
- `XXXX990`, `XXXX991` — supervised research

### ⚠ The "has it become titled?" exception

**Skip a shell number unless the course has settled into a real, specific title that is
consistent across institutions — at which point it is no longer a special-topics course and
is worth a guide.** A specific title in the inventory is *not* sufficient evidence on its own:
the statewide inventory and catalog scrapes can capture one institution's **section title** for
one term.

Verify against two or three catalogs before keeping one. Worked example (2026-08-31):
`CCJ2930` appeared as **"Cybercrime"** at 12 institutions, which looked settled — but FGCU's
catalog lists CCJ2930 as *"Special Topics: current and emerging issues in criminal justice and
criminology."* The Cybercrime title was Daytona State's section title, not a statewide course.
**Skipped.**

**These courses migrate.** When a special-topics offering proves durable, SCNS assigns it a
permanent number later. So a topic skipped today may reappear under its own number and become
worth writing then — and, for guides on courses that *did* migrate, it is worth noting that
older transcripts may carry the same content under the shell number. Do not treat a shell
number as equivalent to the permanent number it became; SCNS equivalency does not cross
numbers.

Title keywords that flag shell courses regardless of code: INTERNSHIP, COOPERATIVE, SPECIAL TOPICS, INDEPENDENT STUDY, DIRECTED STUDY, THESIS, DISSERTATION, SUPERVISED RESEARCH.

---

## ⚠⚠⚠ One number, two subjects: the `-SCNS` / `-<INST>` split

**Ron's decision, 2026-09-04.** Sometimes an SCNS number does not carry a *variant* of a subject at
different institutions — it carries **two genuinely different subjects**. When that happens, **do not pick
one and bury the divergence in a warning. Publish both.**

### When this rule applies

Only when the statewide title and the institution's title name **different subjects**, not different
wordings. Test it against the description, not the title:

| | Same subject, different name → **one guide** | **Different subjects → split** |
|---|---|---|
| Example | SCNS "Gender and Culture" vs UWF "Global Gender Issues" | SCNS **"Gerontological Nursing"** vs UWF **"Concepts of Quality and Safety in Nursing"** |
| Handling | one guide, note the drift, tell the student to carry a syllabus | **three pages — see below** |

### What to publish

For a number `XXXnnnn` carrying two subjects, publish **three** pages:

1. **`XXXnnnn-SCNS`** — the subject as the **statewide catalog** defines it.
2. **`XXXnnnn-<INST>`** — the subject as the institution actually teaches it (`-UWF`, `-DSC`, …).
3. **`XXXnnnn`** (the bare number) — a short **disambiguation page** naming both subjects and pointing at
   the two guides. **The bare number must never silently hold just one reading**, because that is exactly
   the trap the split exists to prevent.

Every variant guide carries a block at the top of Special Information stating both subjects, listing the
institutions from the statewide inventory, and warning that **a transfer evaluator matching on the number
alone cannot tell the two apart**.

### Mechanics (working as of batch 129)

- **The server accepts hyphenated IDs.** `ExtractCoursePrefix` scans letters up to the first digit, so
  `NUR4826-UWF` resolves to prefix `NUR`, finds the taxonomy node, and creates the course.
- **The tooling regex was widened** in `queue_mgr.py` and `validate_drafts.py` to
  `^[A-Z]{3}\d{4}[CL]?(?:-(?:SCNS|[A-Z]{2,5}))?$`. Before that change `reconcile` **silently skipped**
  hyphenated drafts and they never pushed.
- ⚠ **When deriving a variant draft by copying an existing one, delete the `pushed_utc` key first** —
  `reconcile` reads it and marks the new draft as already pushed, so it never gets sent.
- The disambiguation stub legitimately trips the validator's "no Learning Outcomes / Major Topics"
  warnings. Non-blocking, and correct for that page type.

### ⚠ Sourcing the `-SCNS` half

**A `-SCNS` guide needs the state catalog's definition of the course, not just its title.** The statewide
inventory (`courses_2plus_institutions.csv`) gives a title and an institution list and nothing more.

**Do not write a `-SCNS` guide from the title alone** — that is inventing content, which this project does
not do. Source it from the SCNS catalog, or from a fetchable institution that actually teaches the SCNS
version. **Ron has offered to supply the SCNS catalog; ask for it.**

### ⚠⚠ PREFIX divergence — a named category (batch 179)

**The same subject taught under different SCNS prefixes at different institutions, where the number, level
and suffix may all otherwise match.** Credit articulates; **prerequisite checks and requirement matching do
not**, because receiving programmes name prerequisites by course number.

| Subject | Competing prefixes | Notes |
|---|---|---|
| **Anatomy &amp; Physiology** | **`BSC2085C`/`BSC2086C`** vs **`APK2100C`/`APK2105C`** | ⚠⚠ **The most damaging case found.** `BSC` is what nearly every health-professions prerequisite NAMES. Lower-division, huge enrolment, gates competitive admission. |
| Social work | `SOW` vs `HUS` (human services) | ⚠ `HUS` does **not** substitute in a CSWE-accredited programme. |
| Conservation / resources | `GEO` vs `EVR` vs `SWS` | applied as a general elective where no matching department exists |
| Health informatics | `HSA` vs `HIM` vs `CIS` | |
| Supply chain | `TRA` vs `MAN` vs `MAR` | |

⚠ **Most damaging in lower-division courses feeding competitive professional admission**, because the
student meets it before transfer, with least advising support, and a mismatch can invalidate an application
rather than merely delay an audit.

**Guides should name the alternative prefix explicitly wherever one exists**, and tell students to read
target-programme prerequisites literally.

### ⚠ The prerequisite-chain diagnostic (promoted to a standing test, batch 175)

**When two institutions' descriptions of a number look like they *might* be the same subject, stop reading
the descriptions and look at the prerequisite graph.** Ask two questions:

1. **What does each institution treat this course as a prerequisite FOR?**
2. **What does each institution accept as an ALTERNATIVE to it?**

**A course's function in its own institution's prerequisite graph is harder to fake than its description
and is frequently more informative.** Three cases have now turned on it:

| Number | What the chain revealed |
|---|---|
| `CLP4302` | FGCU gates on research methods **and statistics** → the course reads research. UWF gates on abnormal psychology alone → a skills course. |
| `CHM4455` | Physical chemistry required → a quantitative treatment. |
| **`COM3003`** | UWF accepts it **interchangeably with `ADV3000` and `PUR3000`** as the gateway to its advertising and PR sequence → it is an advertising/PR foundation, not a theory survey. |

**Apply this before concluding that a divergence is mere title drift.**

### Open cases

| Number | SCNS subject | Institution subject | `-SCNS` | `-<INST>` | bare |
|---|---|---|---|---|---|
| **`COM3003`** | **Human Communication** (theory survey: interpersonal, small group, organisational, intercultural) | **Integrated Advertising &amp; Public Relations Concepts** (UWF) | ✅ **`-SCNS` LIVE** (sourced from FIU) | ✅ **`-UWF` LIVE** | ✅ **live** | ✅✅ **SPLIT COMPLETED 2026-09-07 (batch 175) — the first full three-page execution of this rule.** Both halves were sourceable, so all three pages published. ⚠ **The decisive evidence was the PREREQUISITE CHAIN, not the titles**: UWF lists `COM3003` as interchangeable with `ADV3000` and `PUR3000` as a gateway to `ADV3300` and `PUR4801`. A theory survey would not be. |
| **`EEE4775`** | **Massive Storage and I/O for Big Data Computing** (file storage systems, I/O architectures, big-data systems infrastructure; FIU) | **Real-Time Systems** (real-time scheduling theory, response-time analysis, RTOS design; UCF) | ✅ **`-SCNS` LIVE** | ✅ **`-UCF` LIVE** | ✅ **live** | ✅✅ **SPLIT COMPLETED 2026-09-09 (EEE sweep) — the second full three-page execution of this rule.** ⚠⚠ **The cleanest collision found so far: the two subjects share NO content, no textbook and no skill set** — unlike `COM3003`, where both halves were at least communication. ⚠ **UCF holds the MINORITY reading**: the statewide record AND FIU both say storage, so a UCF student transferring out carries a number the state says means something else. Found from the SCNS flat file (`inst_title` vs `state_title`), not from reading catalogs — the first divergence in the project surfaced mechanically rather than by probing. |
| `NUR4286` | Gerontological Nursing | Concepts of Quality and Safety in Nursing (UWF) | **⏸ needs catalog** | ✅ `-UWF` live | ✅ live |
| `NUR4826` | Ethics | Transformational Nursing Leadership (UWF) | **⏸ needs catalog** | ✅ `-UWF` live | ✅ live |
| `ART3789C` | World Ceramics | Advanced Ceramics: Mold Making and Slip Casting (UWF) | **⏸ candidate** | published as single guide | — |
| `ART4800` | Criticism Seminar | Portfolio (UWF) | **⏸ candidate** | published as single guide | — |
| `HSC3102` | Perspectives in Health | Health Science Essentials of Behavior Analysis (UWF) | **⏸ candidate** | published as single guide | — |
| `PCB4315` | Marine Ecology | Tropical Marine Ecology (UWF, Bahamas field course) | **⏸ candidate** | published as single guide | narrowing, not a different subject — low priority |
| `ISM4320` | Applications in Information Security | Legal, Ethical, and Human Aspects of Cybersecurity (UWF) | **⏸ candidate** | published as single guide | **strongest candidate in this batch** — technical applications vs human/legal |
| `ISM4545` | Visual Analytics I | Business Analytics with AI (UWF) | **⏸ candidate** | published as single guide | different centre of gravity; "I" implies a sequence UWF does not run |
| `MAN4350` | Training and Development | Recruitment and Selection (UWF) | **⚠⚠⚠ COLLISION** | published as single guide | **not a normal drift** — subjects permute across `MAN4320`/`MAN4350`; needs a two-number treatment. See `REVIEW_QUEUE.md`. |
| `MAN3802` | Principles of Entrepreneurship | Small Business/Family Business Management (UWF) | **⏸ candidate** | published as single guide | venture creation vs managing established firms |
| `PUR3000` | Principles of Public Relations | Introduction to Public Affairs (UWF) | **⏸ candidate** | published as single guide | **strongest candidate since ISM4320** — UF *and* FGCU both teach the general intro-PR course (history of the profession, ethics, PR process); UWF teaches government/nonprofit/media policy communication. Public affairs is a *subfield* of PR, so UWF's students miss PR history, media relations and campaigns entirely |
| `TPP2100` | Acting I | Acting for Non-majors (UWF) | **⏸ candidate** | published as single guide | ⚠ statewide lists BOTH `TPP2100` and `TPP2110C` as "Acting I" — a title, not a number, collision |
| `LAE3314` | Children's Literature | Literacy for the Emergent Learner (UWF) | **⏸ needs catalog** | **NOT WRITTEN — pulled from batch 156** | — | ⚠⚠ **First case where UWF holds the MINORITY reading.** Statewide title is Children's Literature across six institutions; UWF alone teaches early-literacy instruction. **Confirming evidence: UWF carries `LAE5468` "Literature for Children and Young Adults" at graduate level**, so it teaches the children's-lit subject under a different number. Writing a single guide from UWF would publish the minority subject under a number most institutions use for something else. See `REVIEW_QUEUE.md` item 20. |
| `PUR4801` | Public Relations Cases | **Public Relations Campaigns** (UWF) | **⏸ candidate** | queued, not yet written | — | ⚠⚠ **A numbering collision, not ordinary drift.** UWF uses PUR4801 for the campaigns CAPSTONE that the statewide system numbers `PUR4800C` (FGCU uses `PUR4800`, no suffix). Statewide, PUR4801 is *Public Relations Cases* — a different subject. **The project will meet this again from the other side when PUR4801 comes up in the queue.** See batch 158 in `SOURCES.md`. |
| `ZOO4454C` | Ichthyology (all fishes, ~35,000 spp; integrated lecture+lab; FGCU) | **Elasmobranch Biology** (sharks/rays/skates/chimaeras only, ~1,200 spp; UWF, no `C`) | **⏸ candidate** | published as single guide (Ichthyology) | — | ⚠⚠ **Stronger than the PCB4315 narrowing case.** Three divergences at once: subject scope, suffix, and format. A UWF student has **not covered the teleosts** — every fish a Florida fisheries biologist handles. The employability consequence is concrete. UWF's is the better course for shark research; the problem is the number. See batch 165 in `SOURCES.md`. |
| `CLP4302` | Intro to Clinical Psychology — **disciplinary survey**: scientific basis, training, roles, models, controversies, ethics (FGCU, UF) | **HELPING SKILLS**: empathy, nonverbal behaviour, problem solving, crisis intervention, interview technique, experiential activities (UWF) | **⏸ candidate** | published as one guide covering **both**, each labelled | — | ⚠⚠ **Strongest candidate since `PUR3000`.** The **prerequisite chains prove it**: FGCU gates on research methods AND statistics (the course reads research); UWF gates on abnormal psychology alone (a skills course). See batch 167 in `SOURCES.md`. |

| `TPA3230C` | **Costume Design** (statewide title) | **THREE different subjects, none of them agreeing**: UWF `TPA3230` = *Costume Construction* (patterning, cutting, draping); FSU `TPA3230` = *Costuming I* (costume sewing); FGCU `TPA3230` = *Costume Design*; FIU `TPA3230` = *Costume History* (fashion ancient→modern) | **⏸ HELD** | **NOT WRITTEN — pulled from batch 173** | — | ⚠⚠⚠ **The most severe case in this table: THREE subjects, not two**, and construction vs design is a real professional division (draper vs designer — different jobs, different careers). **Compounding problem: NO institution carries the `C` suffix** — all four carry bare `TPA3230`, so the queued ID may not exist anywhere. UWF puts design at `TPA4045`/`TPA4046` instead. See `REVIEW_QUEUE.md` item 25 and batch 173 in `SOURCES.md`. |

| `EEX4474` | **Teaching Students with Moderate/Severe Disabilities** — curriculum and instruction for students with severe and multiple disabilities (UWF, statewide title) | ⚠ **Assessment of infants and young children** (FGCU) | **⏸ candidate** | published as single guide (UWF/statewide reading), with a divergence block | — | ⚠⚠ **First divergence found inside a course PAIR.** `EEX4254` (mild/moderate) and `EEX4474` (moderate/severe) are the standard two-course split of an ESE methods sequence and are taken together — so **a student can complete a coherent-looking pair and have covered something different at the other institution.** Both guides cross-reference each other. See batch 181 in `SOURCES.md`. |

| `BSC1050` | **Environmental Science** — the broad applied field (pollution, resources, energy, policy) | ⚠ **Fundamentals of Ecology** — the science of organism-environment interaction, a COMPONENT of the above (UWF) | **⏸ candidate** | published as single guide (UWF/ecology reading), with a divergence block | — | ⚠ **The only reachable catalog holds the NARROWER reading** — three of four institutions are private or small colleges outside catalog reach. Likely cause: the number sits on a prefix boundary (Florida numbers environmental science `EVR1001` and majors ecology `PCB3043`), so a non-majors course spanning both lands in general `BSC` and leans whichever way the institution does. See batch 182 in `SOURCES.md`. |

| `SPC4680` | **Rhetorical Criticism** — methods for the criticism of rhetorical discourse: Aristotelian, metaphor, narrative, post-modern, cultural (FSU **and** UF, matching the statewide title) | ⚠ **Rhetoric, Media, and Civic Life** — applied preparation for leadership, advocacy and civic engagement, with attention to the shift from traditional to digital media (UWF) | **⏸ candidate** | published as single guide (majority/methods reading) with a labelled variant section | — | ⚠⚠ **Second case where UWF holds the MINORITY reading**, after `LAE3314` — and the strongest, since FSU and UF agree with each other AND with the statewide title. A methods course and an applied advocacy course are different preparations, and the methods version is what graduate study in rhetoric expects. See batch 185 in `SOURCES.md`. |

| `APK4200` | **Motor Development** — developmental aspects of movement and the acquisition of motor skills across the lifespan (FIU, matching the statewide title) | ⚠⚠ **Neuromechanics of Human Movement** — neural mechanisms of movement and control, central and peripheral, prerequisite `APK 3110L` (UWF) | **⏸ candidate** | published as one guide covering **both**, each labelled | — | ⚠⚠ **Third case where UWF holds the MINORITY reading**, after `LAE3314` and `SPC4680`. **Different fields, different literatures, different audiences**: motor development serves teachers and adapted-activity specialists; neuromechanics serves exercise science and rehabilitation. ⚠ **A student needing motor development for a certification who takes the neuromechanics course has not covered it, and the transcript will not show it.** The prerequisite settled it — an exercise physiology LAB is not a developmental course's gate. See batch 188. |

### ⚠⚠ SECTOR number divergence — FCS and SUS using different numbers (batch 182)

**Distinct from ordinary number divergence, which runs between institutions. This runs along the SECTOR
boundary:** the two-year colleges as a group use one number and the universities as a group use another.

| Subject | FCS number | SUS number |
|---|---|---|
| Introductory criminal justice | **`CCJ1020`** (Broward, EFSC, Valencia — all three checked; **none carries `CCJ2002`**) | **`CCJ2002`** |

⚠ **Why it matters more than a between-institution divergence: it hits EVERY A.A. transfer student in the
discipline**, not the unlucky few. SCNS equivalency does not cross numbers. Mitigating facts are real — same
survey, common general-education core protects A.A. completers, departments know the pairing — **but
mid-degree transfers are not protected.**

**Drill: when a LOWER-DIVISION course appears in the queue at SUS institutions only, check two or three FCS
catalogs for the same subject under a different number before writing.** Broward, Valencia and EFSC are
reachable and make this cheap.

### ⚠⚠ Check the taxonomy prefix BEFORE drafting, not after pushing (batch 182)

A push for a prefix with no taxonomy node returns **HTTP 422**. The seed file answers in one command:

```
grep -c '"<PREFIX>"' PreseMakerRepo.Api/Data/Seed/taxonomy.json
```

**Zero means the push will fail.** Confirmed blocked as of 2026-09-08: **`CES`, `CWR`, `CEG`, `ENV`** — ten
queue rows, and they sit at the head of the priority order, which is why the queue's top has stopped moving.
`TTE`, `ASC`, `MUN`, `PEL`, `MVV` and `MUG` all have nodes. **This is a server-side taxonomy addition, not a
content problem.**

### ⚠ One institution, TWO introductory courses (batch 182)

A general-education version and a majors version of the same subject can share a department, a description
and almost a title. `CCJ 2002` (gen ed, lower division, *"designed for students across disciplines"*) versus
`CCJ 3024` (majors, upper division, **carries the Gordon Rule writing designation**) at UWF.

**Tells:** the level, the phrase about serving students across disciplines, and **which of the two carries
the writing designation.** ⚠ **They are not substitutes, and guides must say so.**

### ⚠ Lab-suffix warning is now standing practice (batch 182)

**Every 1000/2000-level natural science course with no `C` or `L` suffix gets an explicit warning that it
carries no laboratory and may satisfy only part of a general-education science requirement** — in the
guide AND in the prerequisite string, which is what a queue reader sees first. Instances: `AST2037`
(batch 180), `BSC1050` (batch 182).

### ⚠⚠ Three DIFFERENT shapes behind a `C` suffix — do not conflate them (batch 183)

| Shape | Example | What it means | What transfers |
|---|---|---|---|
| **Split family** | `CGN3501C` (UF) vs `CGN3501` + `CGN3501L` (UWF); `EEE3308C` vs `EEE3308` + `EEE3308L` | one course, packaged as one enrolment or two | same content, **3 cr vs 4 cr**, one grade vs two |
| **Suffix divergence** | `BCN3224C` (UF, integrated) vs bare `BCN3224` (UWF, lecture only, no lab partner) | ⚠ **genuinely different courses** — one has laboratory hours the other does not | content differs |
| **`C` nobody carries** | `TPA3230C`, `COP3014C`, `INP3004C`, `CJE3674C`, `CTS4348C`, `DAA2204C`, `EEE3396C` | the queued id may not exist at any institution | see `REVIEW_QUEUE.md` item 28 |

⚠⚠ **Diagnostic for the split family: RECIPROCAL concurrent prerequisites.** `EEE 3308` lists
`EEE 3308L*` and `EEE 3308L` lists `EEE 3308*` — **neither can be taken alone, so the pair IS the `C`
course.** Where the queue holds the `C` id, write one guide covering both halves and state the three
consequences: **credit count, two grades, and register for both.**

### ⚠⚠ Two institutions agreeing with each other outrank a statewide title (batch 183)

**`HFT4274`**: statewide title **Resort Management**; **FGCU teaches "Vacation Ownership & Timeshare" and
FIU teaches "Short-Term Rental / Vacation Ownership".** Two independent catalogs agree with each other and
both contradict the statewide label.

⚠ **The statewide title is a single SCNS label with no description behind it.** Two agreeing descriptions
are stronger evidence. **Write to the agreeing pair, and say in the guide what to expect if a third
institution teaches the broader subject instead.** (Contrast `BSC1050`, where only ONE catalog was
reachable — there the divergence block is a warning, not a correction.)

### ⚠⚠ State-college catalog blocks are RATE-TRIGGERED, not permanent (batch 183)

**Broward and Valencia answered with full 200 bodies in batch 182 and returned empty 202s in batch 183,
minutes later** — including on `cop`, a prefix Broward certainly carries. **Roughly six requests in quick
succession tripped it.**

- ⚠ **Do not record a source as blocked on the basis of a burst.**
- **Space state-college probes out; batch them at the start of a session rather than mid-batch.**
- **This explains the long-standing blocked → recovered → blocked pattern for Broward and Valencia** that
  the register recorded across several sessions without accounting for.

### ⚠ A `C` id IS sometimes real — check every time (batch 184)

Seven consecutive queued `C` rows turned out to be carried by no institution, which made "the inventory's
`C` suffixes are spurious" a tempting generalisation. **`PET3640C` refutes it: FIU carries BOTH
`PET 3640` and `PET 3640C`.**

⚠ **An institution carrying BOTH forms is the clean signature of a course run in two shapes** — a lecture
section and an integrated section with a scheduled practicum or laboratory. **Write the `C` id, state the
contact-hour difference (60 vs 45), and tell the student to check which section they are in.**

### ⚠⚠ Chronological divergence — write the whole span and label the halves (batch 184)

**`EUH3570`**: statewide **"Modern Russia"**; **UWF teaches "Russia to 1917"** (its Soviet material is
`EUH 3576`); **FIU teaches the whole span in one course.** ⚠⚠ **A student registering for "Modern Russia"
at UWF gets the tsars** — the first divergence where the statewide title points at close to the OPPOSITE
half of the timeline.

**Handling: cover the full span, mark clearly which material sits on each side of the split, and lead with
a table telling the reader to check their own catalog.** Cheaper than two guides and it serves the student
in either version.

### ⚠ Practicum courses: the screening warning goes in the PREREQUISITE field (batch 184)

**Florida requires Level 2 background screening for anyone working with children or vulnerable adults, and
clearance takes time.** Students who leave it late run out of term (`EEC4301`, `PET3640C`).

**Standing practice: every guide for a course with placement or practicum hours states, in the prerequisite
string as well as the body, that screening should be started in week one** — the prerequisite field is what
a queue reader sees first. Carry FERPA confidentiality and **Chapter 39 mandatory reporting (Florida Abuse
Hotline 1-800-96-ABUSE)** in the body.

### ⚠⚠ When the tool's characteristic output IS the course's target error, say so (batch 184)

The strongest AI sections are the ones where the failure mode and the course's own subject coincide:

| Course | The coincidence |
|---|---|
| **`PET3640C`** | The discipline exists to replace **diagnosis-based assumptions with individual assessment**; a model asked about "a student with cerebral palsy" produces exactly the category-based answer the course teaches you to abandon. |
| `COM3461` | Intercultural communication warns against applying national averages to individuals; a model produces the unhedged lookup table. |
| `CJJ4010` | The course studies disproportionate minority contact; risk instruments trained on past decisions encode it. |

⚠ **Where this holds, it is a far better argument than a generic integrity warning** — it tells the student
something about their own field.

### ⚠ CREDIT-COUNT divergence — a fourth shape, and invisible from the identifier (batch 185)

**`PHY3220`: UWF lists 4 semester hours; the statewide title and most institutions carry 3.** No
laboratory, no second registration — **the same course simply carries a different credit value.**

⚠ **Unlike split family, suffix divergence and `C`-ids-nobody-carries, nothing in the course identifier
signals it.** **Consequence: a transfer student is a credit short or long against a degree requirement, and
in tightly budgeted majors it surfaces only in the final audit.** **State the credit value explicitly in
the guide and tell the reader to check their own.**

### ⚠⚠⚠ RESOLVE THE RANGE: name the school against every differing hour figure (Ron's direction, 2026-09-11)

**This is the standing rule for how a credit or contact-hour divergence is written up.** Where the identified
offerings of a course carry **different hours at different schools, the guide must name the schools and the
hours required at each.** A range is not an answer:

| ❌ Never publish | ✅ Publish |
|---|---|
| "3–4 credits depending on institution" | a table: **Valencia 3, Miami Dade 4, State College of Florida 4, Daytona State 3** |
| "contact hours vary" | "**60 contact hours** at the four institutions that publish them; Tallahassee State does not publish hours" |
| "typically 3 credits" | "**all five institutions carry it at 3 credits**" — state uniformity explicitly too |

**Why a range fails the reader.** A student does not attend "Florida"; they attend one school, transfer to
one other, and need **their own two numbers**. A range tells them a discrepancy exists and leaves them to do
the work the guide exists to do — and **the range is precisely where the harm is**: the student short a
credit against a degree requirement is the one who read "3–4" and assumed 3.

**Where the data comes from — the answer is now cheap:**

1. **The SCNS flat file** carries **per-institution credits** (`credit`) and **clock hours** (`clock_hours`)
   for every offering of the exact id. One parse answers the whole prefix. ⚠ **Normalise before comparing —
   `3` and `3.0` are the same number**, and a spurious "varies" is worse than no table. ⚠ A value like
   `3-4` is a range **inside one school** (variable-credit section) — say so, and say what determines it.
2. **The course API's `offerings[]`** carries the same per-school `credits` and `clockHours` — so the
   guide's table and the site's "Offered at N Florida institutions" panel should be built from one pass and
   agree with each other. See the course-catalog section above.
3. Where an institution publishes contact hours directly (**Broward** is the reliable one), prefer it over
   any derived figure and say which school it came from.

**Where no institution publishes hours** — common, and the honest answer is not silence: **give the derived
figure, label it as derived by the credit-to-hour convention, and name the schools that were checked.**
A reader can then see the difference between a sourced number and a convention.

**The guide's own `contact_hours` field still holds ONE number** — the value for the identifier being
published (for a `C` id, the integrated form's hours; see the batch-189 rule). The per-school detail belongs
in the Special Information table, not in the scalar field.

### ⚠⚠ Prerequisites separate DEPTH as reliably as they separate SUBJECT (batch 185)

The prerequisite-chain diagnostic (batch 175) was developed to settle whether two institutions teach
different SUBJECTS. **`PSB4002` shows it also settles DEPTH:**

| Institution | Gate | What it signals |
|---|---|---|
| **FGCU** | general psychology **AND** research methods **AND** statistics **AND** biology with lab | reads primary research at the cellular level |
| **UWF** | **none** | a broader biological-psychology survey |

⚠ **Where two catalogs describe the same field in compatible language, the GATE is the better signal of
what the course will demand** — and the guide should say so, because a transfer student moving from the
survey into a programme built on the rigorous version meets the gap in the next course.

### ⚠ A syllabus TEST beats a generic divergence warning (batch 185)

Where a guide covers a divergence, give the reader an observable way to tell which version they are in.
`SPC4680`:

| Methods version | Applied version |
|---|---|
| named critical approaches, assigned artefact analyses, a substantial critical essay, journal readings | media change, advocacy projects, assessment of contemporary campaigns, produced persuasive work |

⚠ **"Check your syllabus" is advice; a two-column test is usable.** Apply this wherever the divergence is
one of emphasis rather than of subject.

### ⚠ "Offered concurrently with <5xxx>" — a dual-listed course (batch 186)

**`SOW4700` is "offered concurrently with `SOW 5710`"** — undergraduate and graduate sections sharing a
classroom, with extra requirements for the graduate students.

⚠⚠ **Two consequences a guide must state:** the pace and reading are pitched above a typical undergraduate
course (generally a benefit), and **taking the undergraduate version may block taking the graduate one for
credit later** — dual-listed pairs frequently carry a repeat restriction. **This matters to anyone
continuing to graduate study at the same institution, and it must be known before registering.**

**Look for the phrase in catalog entries; it is easy to read past.**

### ⚠ The caches answer two independent failure modes (batch 186)

**`RTV2000` was written entirely from the cached FSCJ Coursedog data**, and it needed to be for two separate
reasons at once:

1. **The live state-college HTTP routes were being left alone** under the rate-limit rule (batch 183).
2. ⚠ **The inventory pointed at the wrong institution** — it lists UWF, which does not carry the number.

⚠ **Keep `fiu_courses.json`, `fscj_courses.json` and `nwfsc_courses.json` current.** **They cover
rate-limiting AND inventory error, and those failures are independent.**

### ⚠ Watch the 500-character prerequisite ceiling (batch 186)

**`SCE4320` failed the validator at 546 characters** — the first blocking failure in eleven batches, and it
needed two trims.

⚠ **Prerequisite strings have been growing as more warnings are packed into them**, and **three of the last
twelve have come within 30 characters of the limit.** **The assembler's length report is what catches this
before the push; keep reading it.** **When trimming, cut the connective tissue and keep the warnings.**

### ⚠⚠ TERMINOLOGY-ERA divergence — a category of its own (batch 187)

**Not title drift, not subject divergence: the same course carrying vocabulary from different decades of
the field's own development.**

| Number | Older term | Current term | Why it changed |
|---|---|---|---|
| **`SYD4800`** | UWF **"Sociology of Sex Roles"** | UF **"Sociology of Gender"** | role theory framed gender as expectations attached to two categories; the replacement treats it as produced in interaction and built into institutions |
| **`SOW4700`** | statewide **"Chemical Addiction"** | UWF **"Substance Use, Prevention, and Treatment"** | *substance use disorder* is a spectrum with severity specifiers; the older vocabulary is associated with more punitive clinical judgements |

⚠ **The handling differs from a subject divergence.** **The course is the same.** **What the guide owes the
reader is the CURRENT vocabulary plus an explanation of why it changed** — because **a student who learns
only the older term will be using language the current literature has moved past**, and in clinical fields
that has consequences beyond style.

⚠ **It also predicts an AI failure mode**: training data is dominated by older text, so **generated prose
reproduces the superseded vocabulary** — which is worth saying in the guide's AI section.

### ⚠⚠ The prerequisite-as-signal diagnostic — now the most productive sourcing move

Originally a test for whether two institutions teach different SUBJECTS (batch 175). It has since fired on
DEPTH and on EMPHASIS, four batches running:

| Course | Gate | What it signalled |
|---|---|---|
| `PSB4002` | four courses incl. statistics + lab biology (FGCU) vs none (UWF) | reads primary research at cellular level vs a survey |
| `STA4234` | **calculus** added at FGCU | theory and the matrix formulation vs applied procedures |
| `ZOO4472C` | **statistics** at UWF | estimating survival and abundance, not just describing birds |
| `ZOO4485` | **oceanography** at UWF | marine mammals as animals in a physical ocean |
| `ACG4180` | **finance**, not accounting | taught from the statement USER's side |

⚠ **Read the prerequisite before the description.** **It is harder to write loosely than a course
description and it constrains what the course can assume.**

### ⚠ Departmental placement is an emphasis signal too (batch 187)

**`SYD4800` sits in ANTHROPOLOGY at UWF, not Sociology** — predicting a stronger comparative and
cross-cultural frame. **`PLA4885` and `PLA4263` sit in CRIMINAL JUSTICE, not a law or legal studies
department.** ⚠ **The UWF prefix PDFs print the college and department on every entry; read that line.**

### ⚠ "May be repeated for up to N sh" + "Topics in" = a variable-content course (batch 188)

**`AML4640` at UWF: "Topics in Native American Literature", repeatable to 12 semester hours.**

⚠⚠ **Two consequences a guide must state.** The student can take it more than once for credit — unusual and
useful. **And the transcript line conveys nothing about what was actually covered**, since content varies by
term. **A receiving institution or a graduate programme evaluating it will ask, so the syllabus and reading
list are the only record.**

**Look for the repeat clause in the credit line; it is easy to read past.** Expect it on `AML`, `LIT`, `ENG`
and studio numbers.

### ⚠ Restricted-enrolment courses — a scheduling blocker no other source surfaces (batch 188)

**Courses closed to non-majors, or gated on a cumulative GPA, are invisible until registration fails.**
Instances so far:

| Course | Restriction |
|---|---|
| `ENG3010` (UWF) | English majors and minors only |
| `RTV3511` (FIU) | five prerequisite courses **and a 2.85 cumulative GPA** |
| **`APK4163` (FIU)** | **Bachelor of Science in Sport and Exercise Science major, or instructor consent** |

⚠ **Where a catalog states one, put it in the prerequisite field** — it determines whether a student can
plan a term around the course at all.

### ⚠⚠ For a queued `C` id, state the INTEGRATED form's hours (batch 189)

**`APK2000C` tripped the validator's first WARNING rather than a failure**: *"an integrated lecture+lab (C)
course but has only 45 contact hours"*, because the guide had been written to UWF's unsuffixed 45-hour
lecture version.

⚠ **The rule, now applied consistently across `BCN3224C`, `GIS4035C`, `ZOO4472C`, `APK4119C`, `APK4220C`
and `APK2000C`: give the integrated form's hours — that is what the queued identifier represents — and
describe the unsuffixed version alongside it.** **Doing it the other way round produces a warning and, more
importantly, a guide that does not describe the course the identifier names.**

### ⚠ Where a description names a discipline the prerequisite does not, that gap is where students fail (batch 189)

**`APK4220C`**: the formal gate is exercise physiology plus anatomy. ⚠⚠ **The description names "fundamentals
of engineering (kinematics and kinetics) and basic mathematics and physics" — and neither appears in the
prerequisite.** **Students arrive from a kinesiology curriculum that required no physics, meet vectors and
free-body diagrams in week two, and conclude the course is impossible.**

**Name exactly what is needed and say to prepare it** — for that course, trigonometry, algebra, units and
rates, **not** calculus. ⚠ **This is the counterpart to the prerequisite-as-signal diagnostic: read the
description for disciplines the gate omits.**

### ⚠ Writing 1-credit LABORATORY guides (batch 189)

**`APK2100L` and `APK2105L` are the first lab-only guides written deliberately.** They are shorter than a
lecture guide — 21–23 KB against a batch average of 27 — **and that is correct: a 1-credit laboratory has
less to say about content and more about format, safety, assessment and transfer traps.**

⚠⚠ **State the credit-to-contact-hour ratio explicitly**: a 1-credit laboratory carries **two to three
contact hours a week**, so it consumes far more scheduled time than its credit value suggests. **Students
plan around credits and are caught by hours.**

⚠ **Where students are the SUBJECTS** (physiology, exercise testing), the guide must say: **participation is
voluntary, results are not medical advice, classmates' measurements are private, and bloodborne pathogen
procedures apply strictly.**

### ⚠ When a number diverges, check its SEQUENCE PARTNER (batch 181)

A divergence found on one number is not necessarily isolated. **Where a subject is split across a pair of
numbers — an ESE methods sequence, a two-term language sequence, `I`/`II` course pairs — the split itself is a
curricular decision, and two institutions can draw it in different places.** That produces **two**
divergences, not one, and the second is invisible if only the first number is probed.

**Drill:** on finding a divergence, identify the number's partner from the prerequisite chain or the title
family, and probe it at the same institutions before writing either guide. `EEX4254`/`EEX4474` is the worked
example.

**⚠ Watch for more.** This is the extreme end of the drift theme, and two cases surfaced in a single
prefix — so there are almost certainly others already published as single guides. **When a batch turns one
up, add it here.**

---

## Institution order, per-school queues, and what to do when a catalog blocks

**Ron's direction, 2026-09-04.** Work the **smaller schools first — UWF, UNF, FGCU** — then the large ones
(**UCF, UF, USF**), mixing in state colleges. **Keep other schools' work ready to promote**, so a
bot-blocked catalog stalls nothing.

### The queue is now two-layer

| Layer | File | Role |
|---|---|---|
| **Master** | `queue.csv` | **single source of truth for what is DONE.** One row per course. Now carries a **`source_inst`** column recording which institution's catalog a guide was written from. |
| **Per-school** | `queue_<SCHOOL>.csv` | a *work list*, derived on demand. Courses that school offers which the master has not finished. Disposable — rebuild any time. |

```bash
python school_queue.py coverage            # per-school workable counts
python school_queue.py build UNF           # write queue_UNF.csv
python school_queue.py status              # what per-school queues exist
```

**Deduplication is automatic**: a course `pushed` or `skipped` in the master is emitted for **no** school.
The only exception is a deliberate one-number-two-subjects split, handled by publishing `XXXnnnn-<INST>`
ids rather than by re-queueing the bare number.

**⚠ Rebuild a per-school queue after every push.** It is derived, not maintained — a stale one will
re-offer finished work.

### ⚠⚠⚠ Focus decision (Ron, 2026-09-09): COMPLETE THE PREFIX, and ENGINEERING FIRST

**This supersedes the 2026-09-04 focus decision below.** Ron's direction, verbatim:

> *"As we progress, try to do all courses in a prefix as we come across the prefixes. Engineering and
> Engineering Technology prefixes have priority, even if there are classes that are only taught at a
> single school."*

Three changes to how batches are chosen:

1. **Finish the prefix.** When work touches a prefix, complete it rather than taking only the queued
   rows from it. A half-done prefix is the thing to avoid.
2. **Engineering and Engineering Technology prefixes come first**, ahead of strict institution-count
   ordering. The SCNS disciplines that qualify: **171** engineering general/support, **028**
   civil/environmental, **029** electrical, **172** mechanical, **173** industrial, **174**
   chemical/nuclear, **175** computer math/materials, **413** biomedical, **058** ocean, and **032**
   engineering technologies.
3. **⚠⚠ Single-institution courses are IN SCOPE.** This is the largest change. It reverses the
   ≥2-institution filter that has shaped the queue since the project began.

#### ⚠⚠ What this means mechanically: `courses_2plus_institutions.csv` no longer defines the work

The master inventory holds **only courses at two or more institutions** — so single-school courses are
not merely deprioritised, they are **structurally invisible** to `queue_mgr.py add`, which refuses any
course not in the master.

**Use the SCNS flat file as the inventory instead** (`scratchpad/scns.py`, see `SOURCES.md` Tier 3).
It lists every course at every Florida institution, so it is the only source that can enumerate a
complete prefix. Filter to **active** status, **levels 1-4**, and drop `x9xx` shells.

⚠ **Single-institution courses still get the single-institution TREATMENT.** Scope changed; the
quality bar did not. A course at one school is written as a custom guide for that school, with
explicit hedging, per the hedging-by-institution-count rules above. Do not let wider scope become
thinner sourcing.

#### ⚠ Prefix completeness is now the progress measure

"Done" for a prefix means every active, non-shell, undergraduate course in it has a guide — not
every queued row. **`EEE` illustrates the difference: 29 queued rows were completed on 2026-09-09,
which finished the prefix under the old rule and left 78 of its 108 courses unwritten under this one.**

**Report prefix coverage as `pushed / total` from the flat file**, not as queue rows cleared.

### ⚠ Superseded — Focus decision (Ron, 2026-09-04): priority courses across schools, NOT full catalogs

**Superseded 2026-09-09 by the decision above.** Retained for the reasoning, which still applies as a
tie-breaker *within* a prefix: where a prefix is large, work its higher-institution-count courses first,
because breadth across institutions serves more students per guide.

The per-school queues from `school_queue.py` exist for **block recovery and sequencing**, not as a
target to exhaust. The original text read: *"Work the master `queue.csv` — the ≥2-institution priority
subset — not a school's complete offering &hellip; Do not expand a batch into non-priority courses just
because a prefix extraction is already in hand."* **That restriction no longer holds** — completing the
prefix is now the goal, and a prefix extraction already in hand is exactly what should be expanded.

### ⚠⚠ Source reachability register (re-probed 2026-09-06, batch 164)

**Check this before committing to a school.** Reachability, not course count, is the binding constraint.

| School | Pattern | Status |
|---|---|---|
| **UWF** | `catalog.uwf.edu/courseinformation/courses/<prefix>/<prefix>.pdf` (**lowercase**) | ✅ **working** — one fetch per prefix, full descriptions. The workhorse. |
| **FGCU** | `catalog.fgcu.edu/courses/<prefix>/<prefix>.pdf` (**the `.pdf`, not the directory**) | ✅ **working.** ⚠ The old directory URL is what was bot-blocked; the PDF answers. **Now the single most productive cross-check source in the project** — it documents credits explicitly and has produced the divergence a guide turned on in three consecutive batches. |
| **FSU** | `registrar.fsu.edu/bulletin/undergraduate-departments/<department>` | ✅ **working, and general-purpose.** Previously recorded here as useful only for the FAMU-FSU joint engineering college — **it is not.** Clean HTML with full descriptions, credits and prerequisites for `psychology`, `philosophy`, `social-work` and others. **Use it as the third vote when UWF and FGCU disagree.** |
| **⚠⚠ SCNS (statewide)** | `scratchpad/scns.py` — `flscns.fldoe.org` | ✅✅ **SOLVED 2026-09-09 (EEE sweep). CHECK THIS FIRST, BEFORE ANY INSTITUTION CATALOG.** `flatfile` downloads the whole SCNS database (~80 MB) carrying, per course, **both the institution's title AND the statewide title**, the authoritative institution list for the **exact** id, per-institution credits, and Gordon Rule + gen-ed flags. `statewide <PREFIX>` returns full descriptions, prerequisites and transferability as CSV. ⚠ Routes are **extensionless**; you must **accept the terms modal** first or reports return 0 rows silently; the report is an async SSRS viewer. All three handled in `scns.py`. See `SOURCES.md` Tier 3. |
| **UF** | **`catalog.ufl.edu/UGRD/courses/<department>/`** — plain CourseLeaf page | ✅ **UPGRADED 2026-09-09.** The department page returns **full descriptions, credits and prerequisites** for every course in the department — far better than the POST API below, which gives title and existence only. Department slugs are descriptive (`electrical_and_computer_engineering`). |
| UF (old route) | `scratchpad/uf.py` — the `catalog.ufl.edu/course-search/api/` POST | ⚠ superseded by the CourseLeaf page above; keyword must be spaced (`"POT 4204"`), title and existence only, `route=details` broken. |
| **UCF** | **Kuali API** — `ucf.kuali.co/api/v1/catalog/public/catalogs/`, then `/api/v1/catalog/courses/<catalogId>`, detail by **`pid`** | ✅✅ **NEW 2026-09-09 — the first working UCF route in the project.** UCF's acalog catalog (`catalog.ucf.edu/preview_course_nopop.php`) now 307s to a WordPress shell; the real catalog is **Kuali** at `ucf.kuali.co`. Returns 3,676 courses with description, credits, **weekly lab hours** (`labStudioFieldWorkHours`), structured prerequisites, department, college and terms offered. ⚠ The detail endpoint needs the **`pid`**, not the `id` — the `id` returns an empty list. UCF is **3,872 workable rows**, so this unblocks the single largest school in the queue. |
| **Broward** | `catalog.broward.edu/course-descriptions/<prefix>/` | ✅ **RECOVERED 2026-09-06** and used productively in batch 166. ⚠⚠ **The only routinely fetchable Florida source that publishes CONTACT HOURS explicitly** ("Total Contact Hrs: 48.00 / Lecture Hrs: 48.00") plus minimum-grade prerequisite conditions. **Go here first whenever a contact-hour figure is in doubt.** |
| **Valencia** | `catalog.valenciacollege.edu/coursedescriptions/coursesoffered/<prefix>/` | ✅ **RECOVERED 2026-09-06** — 200 with full body on `psy` and `mus`. Same regression, same recovery. |
| **DSC** | `daytonastate.smartcatalogiq.com/en/<year>/college-catalog/course-descriptions/<prefix-slug>/<level>/<course>` | ✅ **Confirmed on the CURRENT catalog 2026-09-07**, not just historically. ⚠ Two gotchas: the prefix slug is descriptive (`cop-computer-science`, not `cop`), and **the index page lists only titles — the individual course page carries description, credits, prerequisite and term**. A trailing slash 404s. **Same platform as IRSC.** |
| **UNF** | — | ⚠ **no static pattern found**, and now 301s to client-rendered pages. **Lead worth chasing: `digitalcommons.unf.edu/course_catalogs/` (archived PDF catalogs).** |
| **FSW** | `catalog.fsw.edu` (acalog, `catoid=27`, Course Descriptions `navoid=5491`) | ⚠ **PARTIAL BLOCK** — root returns 200 (26 KB) but **`content.php` and `search_advanced.php` both return empty 202s.** Root-reachable, content-blocked. |
| **FIU** | Coursedog API — `scratchpad/coursedog.py` | ✅ **SOLVED 2026-09-06 (batch 167). 27,923 courses, cached in `scratchpad/fiu_courses.json`.** ⚠⚠ **The gate is one header: `Referer: https://catalog.fiu.edu/`** — without it every endpoint returns `{"error":"Unauthenticated"}`. Richest Florida source: code, name, credits, college, description, cipCode, and per-component **contactHours**. ⚠ Duplicate rows per code — prefer the one with a real college name and a description. Full paging takes 2-3 min; **use the cache**. |
| **FAU** | `catalog.fau.edu` — Coursedog SPA | ❌ **ANSWERED 2026-09-07: no public Coursedog catalog at that host.** The discovery endpoint returns *"does not have entity assigned"* — the host is registered but no catalog is attached, which is why every schoolId guess failed. **Stop attempting FAU via Coursedog.** |
| **Coursedog discovery** | `app.coursedog.com/api/v1/catalogs/urls?url=<host>` (+ Referer) | ✅ **The portable bootstrap.** Returns `school` and `catalog.id` in one call — use it instead of scraping the page for ids. Works for any Coursedog school. |
| **USF** | `catalog.usf.edu` | ⚠ root 200 (75 KB) but **no course-description path exposed**; its only course link goes to `usf.edu/academics/courses-calendar.aspx`. Not yet a route. |
| Gulf Coast | `gulfcoast.edu/catalog/current/courses/<prefix>/index.html` | was the highest-value pattern in the DSC build; **re-probe before use** |
| **EFSC** | `catalog.easternflorida.edu/course-descriptions-information/<prefix>/` (and `/<prefix>.pdf`) | ✅ **NEW 2026-09-07 — CourseLeaf, same as UWF/FGCU/Broward/Valencia, existing tooling works unchanged.** Recovered `ADV2000C` and `COP3813C`. On CourseLeaf a prefix the college does not carry returns **202** — probe a prefix it definitely has. |
| **Tallahassee (TSC)** | `catalog.tsc.fl.edu` | ⚠ **CORRECTION: never blocked — the college RENAMED.** TCC → Tallahassee State College; `catalog.tcc.fl.edu` 000 was a dead host, not a block. New host is live (386 KB) but acalog `content.php` returns empty 202s. **Lesson: follow redirects on the main domain before recording a block.** |
| **IRSC** | `irsc.smartcatalogiq.com` | ⚠ **Live lead — SmartCatalogIQ, the same platform as the DSC build**, `/en/<year>/catalog/…`. Not yet exercised. |
| **⚠ Inventory reliability** | `courses_2plus_institutions.csv` | ⚠⚠ **The institution list is a HYPOTHESIS, not evidence — five confirmed errors in four batches** (`MUG2101`, `TPA3230C`, `BOT4404C`, `ATT1120`, `COP3014C`, all wrongly listing UWF or a suffix nobody uses). Two patterns: an institution listed that carries the subject under a **different number**, and a **suffix** in the inventory that no institution actually uses — both consistent with the file recording the SCNS catalog rather than current offerings. **Verify against a live catalog before treating an institution as a source or asserting a count in a guide.** |
| **⚠ FSU entry vs requirement text** | `registrar.fsu.edu/bulletin/...` | ⚠ A number followed by a period is **not** enough to locate a catalog entry — it also matches requirement prose (*"a grade of C or higher in COP 3014 or COP 3363."*). **Verify that a TITLE and a parenthesised credit value follow** (`COP 3014. Algorithm… (3).`). Cost a wrong result in batch 176. |
| **FSCJ** | Coursedog — `scratchpad/coursedog.py fscj` (school `fscj_peoplesoft`, catalog `sGHd4uJQXFdgDUaffhTv`) | ✅ **SOLVED 2026-09-07 (batch 173).** Was "platform unidentified". ⚠ **22,693 courses — the largest Florida catalog found so far**, and `fetch()` caps at limit=5000, so a single call silently returns a PARTIAL result. **Page it** (`scratchpad/fscj_dump.py`) and cache to `scratchpad/fscj_courses.json`. |
| **NWFSC** | Coursedog — `scratchpad/coursedog.py nwfsc` (school `nwfsc_banner_sql`, catalog `DGLrTHoh5uNIMFsdbzWf`) | ✅ **NEW 2026-09-07 (batch 173).** 1,781 courses, single page, cached in `scratchpad/nwfsc_courses.json`. Full descriptions and credits. Found because a 404 from `catalog.nwfsc.edu` returned a 1.1 MB body — **the body size was the tell.** |
| **Santa Fe** | `catalog.sfcollege.edu` | ⚠ Answers; not Coursedog (bootstrap 404s). Platform still unidentified. |
| **CF (Central Florida)** | `catalog.cf.edu` | ⚠ Root 200 (26 KB), **acalog** — so likely the same content-blocked pattern as FSW and TSC. Not exercised. |
| **MDC** | `mdc.curricunet.com/catalog/iq/3279` | ⚠ CurricUNET; 200 but ~10 KB (SPA shell). Lead, not a route. |
| **State colleges (standing retry list)** | SPC, HCC, PSC, PHSC, Palm Beach State, Chipola | ❌ **curl 000 / 404.** With TSC and FSW content-blocked and MDC an SPA, **this is what still blocks `MUG2101`.** |
| **Coursedog in Florida** | bootstrap endpoint, then `scratchpad/coursedog.py` | ✅ **REOPENED 2026-09-07 (batch 173) — the earlier "only FIU" conclusion was WRONG.** Three Florida Coursedog schools are now known: **FIU**, **NWFSC** and **FSCJ**. The earlier sweep missed them because it tested a guessed host list rather than the hosts the register already recorded as answering. ⚠ **Re-sweep the bootstrap endpoint against any host that answers before recording it as an unknown platform.** |

### ⚠ How to probe a block correctly (learned batch 164)

**Probe a prefix the school definitely carries, not the prefix you happen to want.** A `404 with a full
body` means the server is answering you and simply lacks that prefix; **an empty `202` means it is not.**
Broward and Valencia looked blocked on a `mug` probe (404) until a `psy` probe returned 200 — the 404 was
the recovery signal, not a failure. **Both had been assumed blocked for two days on this misreading.**

### The block-recovery drill

1. **Keep two or three per-school queues built ahead**, not one.
2. When a catalog returns an empty 202 / 403 / captcha: **do not retry in a loop.** Record it in the
   register above with the date, switch to another school's queue, and move on.
3. **Re-probe blocked sources at the start of each session** — these blocks have proven temporary before.
4. If every named school is blocked, fall back to a prefix at a school that still answers rather than
   stalling the batch.

### ⚠⚠ Scale reality: "complete UWF" is bigger than the queue suggests

The master queue is a **prioritised subset** (courses at ≥2 institutions), not a school's full offering:

| | Courses UWF offers | Done | **Workable** |
|---|---|---|---|
| UWF | 1,885 | 310 | **1,575** |

The 805 rows currently in the master are a *subset* of those 1,575. **`queue_UWF.csv` holds the real
figure.** Same applies to every school: UNF 1,839 workable, FGCU 1,570, UCF 3,872.

**Implication for sequencing:** finishing a school means ~1,500–1,800 guides, not a few hundred. Ron's
smaller-schools-first ordering is the right call for exactly that reason — and the state colleges are much
further along already (MDC 31.5% done, BC 33.5%, SPC 32.3%) because the earlier DSC-era work covered
high-enrolment shared courses.

## ⚠⚠ Florida-wide requirements that affect guides (found 2026-09-08, batch 178)

### The Gordon Rule

**State Board of Education Rule 6A-10.030.** Florida public institutions require designated
**writing-intensive** coursework plus designated **mathematics** coursework for an associate or
baccalaureate degree.

- ⚠⚠ **A grade of C or higher is required for a Gordon Rule course to count. A C-minus does not satisfy
  it at most institutions** — stricter than the ordinary passing standard, and a common and expensive trap.
- ⚠ **The designation is made by the INSTITUTION, not by the course number.** The same number can be
  designated at one Florida institution and not another.
- Designation normally travels within the Florida public system but should be confirmed, especially from
  private or out-of-state institutions.

**Standing practice: guides for 1000- and 2000-level general-education courses — composition, humanities,
mathematics — should check for and mention Gordon Rule status.**

⚠⚠ **UWF's catalog labels ARE Gordon Rule designations** (identified batch 179):

| UWF label | Gordon Rule component |
|---|---|
| *"Meets College-Level **Communication** Skills Requirement"* | the **writing** half |
| *"Meets College-Level **Computation** Skills Requirement"* | the **mathematics** half |

**Whenever a UWF entry carries either label, say what it is AND state the C-or-higher condition.**
⚠ Roughly a dozen already-published guides record the label without the explanation — they are
incomplete rather than wrong. A retro-sweep is a `REVIEW_QUEUE.md` candidate. It surfaced first in FSCJ's Coursedog
entry for `PHI2603`; **CourseLeaf PDFs do not carry it.**

### General-education category designations

⚠ **Distinct from the Gordon Rule and separately unreliable in transfer.** A course can transfer as credit
without satisfying the general-education CATEGORY a student expected. Florida's common general-education
core gives substantial protection for A.A. completers, but **category placement is institution-specific**.

### ⚠ Coursedog sources carry metadata CourseLeaf does not

FSCJ, NWFSC and FIU records include **regulatory notes (the Gordon Rule text), structured `requisites`
objects with prerequisite/corequisite rules, college names, and lifecycle status** ("Inactivated per 2024
SCNS review, last offered fall 2016"). **Mine these deliberately rather than only reading `description`.**

## Session start checklist

When starting a fresh session in this project:

1. Read this file (you are here) — it governs guide *content*.
2. Read `Generate_Guides_and_Push_Process.md` for the end-to-end process (it is the
   start-here document), `README.md` for per-tool detail, and `QUEUE_GUIDE.md` for the queue
   schema and priority tiers. `.claude/skills/guide/SKILL.md` at the repo root drives the
   mechanics.
3. **Check the visitor request queue first** —
   `curl -s "https://floridacourserepo.com/api/v1/queue/guides?status=waiting"`. Anything waiting
   there outranks the local queue (see the course-catalog section).
4. Run `python queue_mgr.py status` to see where things stand. `queue.csv` is the
   authoritative work queue; for prefix completion the live catalog is now the better worklist:
   `curl -s "https://floridacourserepo.com/api/v1/courses/catalog?prefix=<PFX>&hasGuide=false&pageSize=1000"`.
   `courses_2plus_institutions.csv` is the old ≥2-institution inventory; the SCNS flat file is authoritative.
5. Run `python validate_drafts.py --quiet` if the queue shows `error` rows, to see what is
   blocking them.
6. Confirm with the user what they want to work on before generating anything.

Pushing to the live site runs from this repo (`generate_guide.py --push-from-queue`), using
the `REPO_ADMIN_*` credentials in `Tools/.env`. It is a write to production — confirm the
batch with the user before pushing, and never push a draft that `validate_drafts.py` fails.

---

## Tone and quality bar

- Write in the voice of a thoughtful curriculum developer who knows Florida community colleges, not a generic AI summarizer.
- Specific beats generic. "Hibbeler is the most widely adopted text" beats "common textbooks are available." Named employers, named cities, named programs beat vague gestures.
- Honest hedging beats false confidence. "Varies by institution" is acceptable when true; making up a uniform standard is not.
- The user reviews each batch carefully — they are eager to see the guides. Earn that attention with substance.
