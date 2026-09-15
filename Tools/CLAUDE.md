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

## ⚠⚠⚠ Direction (Ron, 2026-09-11): LIST courses as you go; guides follow the queue and then requests

Ron's words:

> *"Guideless courses will remain. We will finish the existing queue and shift to requests as we work on
> programs and career guides. A top priority will be picking up any courses we see at institutions along
> the way and list them (no guide)."*

**Four things follow, and the last one is the change in working practice.**

1. **A course without a guide is a finished outcome, not a backlog.** The ~800 guide-less Engineering
   Technology courses stay as they are. **Do not treat `hasGuide=false` as a work list.**
2. **Finish `queue.csv`**, then **shift to visitor requests** as the main source of guide work.
   ⚠⚠ **Update (Ron, 2026-09-12): the next major phase is CAREER PATHS, and courses
   identified as important to a career path but lacking a guide will land in the queue
   AUTOMATICALLY.** So the queue stops being purely catalog-derived and becomes partly
   pathway-derived — **a third demand signal after faculty and visitor requests.** Keep working
   `queue.csv` until then.
   ⚠ **Also settled 2026-09-12: data-quality and verification findings are DEFERRED to a
   verification pass**, an upcoming phase and part of continuous site maintenance. **Record them in
   `REVIEW_QUEUE.md` and keep going** — do not stop a batch to chase them.
3. **Programs and career paths** become the next build direction (`CAREER_PATHS_PLAN.md`,
   `COURSE_CATALOG_PLAN.md` phase 5) — and both need a complete course list far more than they need more
   guides.
4. ⚠⚠ **TOP PRIORITY, and it applies to every batch from now on: every course you SEE while researching
   gets LISTED.** Writing a guide means reading SCNS and institution catalogs, and that reading surfaces
   hundreds of courses the site does not hold. **Add them — title, credits, per-institution offerings — with
   no guide**, over `POST /api/v1/courses/batch` (`COURSE_API.md`).

### How to do it, at the end of every batch

The SCNS flat file already holds every course at every institution, so **the marginal cost of listing a
whole prefix once you have fetched it is close to zero.** Standing practice:

1. **Institutions first**, with names and sectors: `POST /api/v1/institutions/batch`. Send once; repeats are
   `unchanged`.
2. **Build course rows for every prefix the batch touched** — not only the courses you wrote guides for.
3. **Public institutions only** (`scns.is_public`), per the 2026-09-11 scope rule.
4. `title` = the most common institution title, title-cased; `stateTitle` = the SCNS statewide title;
   `creditHours` = the modal integer credit; `offerings[]` = every public institution with its own title and
   credits.
5. Push in batches of **≤ 500**, log every `failed` result, and reconcile with
   `GET /api/v1/courses/catalog?updatedSince=<run start>`.

⚠ **Watch the two traps.** `replaceOfferings` defaults to **`true`**, so send a course's full offering list
or you will delete the rest. And **a course upsert DOES overwrite an existing title** — which is wanted when
the stored title is the course id placeholder, and is why the title you send must be a real one.

⚠ **Shell numbers (`x9xx`) are still LISTED even though they are skipped for guides.** The skip list governs
what gets a guide; it does not govern what exists. A student can enrol in a special-topics course, so the
catalog should show it.

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

- `credits=0` is valid for **two entirely different things**, and they need different explanations:
  - **PSAV clock-hour courses** — `contact_hours` carries the real measurement.
  - ⚠⚠ **ZERO-CREDIT LABORATORIES** (found batch 198, `BCH3034L` at UWF) — a corequisite laboratory whose
    credit sits on its paired lecture. **The work and the hours are entirely real; only the accounting
    differs.** A guide for one must say: it does **not** count toward full-time enrolment (which matters for
    financial aid, athletic eligibility and student visas), the time commitment is real, it may still be
    graded, and **transfer is awkward because there is no credit to transfer.**
  - ⚠⚠ **PARTICIPATION WITHOUT CREDIT** (found batch 203 — `MUN3426` and `MUN3483` list
    `0-1` at UNF and UWF). **A range within one institution, including zero**, on repeatable ensemble and
    activity courses. **It exists for good reasons: a degree's repeat cap** (`MUN3426`: *"may be used in the
    degree program a maximum of 8 times"*) **and ⚠ Florida's EXCESS-HOURS provisions**, which can carry
    a financial penalty for credits beyond what a degree requires — **so a zero-credit registration
    lets a student keep playing without adding to the total.** ⚠ **State the trade-off: a zero-credit
    course does not count toward full-time enrolment** (aid, athletic eligibility, visa status), **and the
    record of participation becomes the student's own performance list rather than the transcript.**
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
| ⚠⚠ **Criminal justice administration** (batch 220) | **`CCJ2452`** — Polk State, Valencia, Florida Gateway, State College of Florida, Tallahassee State (**all five FCS**) | **`CCJ3450`** — UCF, UWF (**both SUS**) |

⚠⚠⚠ **The second row is worse than the first, and the reason is the LEVEL (batch 220).**
`CCJ1020`/`CCJ2002` are both lower-division, so an A.A. completer's general-education and elective
protections absorb much of the damage. **`CCJ2452` and `CCJ3450` sit at DIFFERENT LEVELS, and a
2000-level course CANNOT supply upper-division hours toward a Florida baccalaureate** — so a state-college
student who takes the subject may have to take it again at the university, **not because the content
differs but because the level does.** **Tell the reader to get a WRITTEN answer from the receiving
department before taking the lower-division version.**

⚠⚠ **Two instances in ONE prefix makes it a property of that prefix, not a coincidence.**
**Generalised drill: where a prefix is found to split one course by sector, check its other
high-enrolment numbers for the same shape before writing any of them.** One `survey.py` call on the
suspected twin answers it.

#### ⚠ But the SECTOR does not determine the LEVEL — check carriers, do not infer (batch 220)

**`CCJ3691` is a 3000-level number carried by UWF (SUS) and St. Johns River State College (FCS).**
⚠ **Florida College System institutions offer upper-division coursework where they hold baccalaureate
authority**, and several do. **So "FCS implies lower division" is a tendency the sector rule exploits, not
a fact to rely on.**

⚠ **Why it matters more than a between-institution divergence: it hits EVERY A.A. transfer student in the
discipline**, not the unlucky few. SCNS equivalency does not cross numbers. Mitigating facts are real — same
survey, common general-education core protects A.A. completers, departments know the pairing — **but
mid-degree transfers are not protected.**

**Drill: when a LOWER-DIVISION course appears in the queue at SUS institutions only, check two or three FCS
catalogs for the same subject under a different number before writing.** Broward, Valencia and EFSC are
reachable and make this cheap.

#### ⚠⚠ A second sector shape: SAME number, different SCOPE by sector (batch 206)

**Distinct from the number divergence above.** **`RET3354` is carried by two Florida College System
institutions as *Medical Pharmacology* and by UWF as *Cardiopulmonary Pharmacotherapy*** — **one number,
and the scope differs along the sector line.**

⚠ **The explanation is the licensure ladder, and it generalises:** **FCS institutions run the entry-level
A.S. programmes that lead to a credential, so they teach broadly; SUS institutions run degree-completion
pathways for practitioners who already hold it, so they go deeper on a narrower range.**

⚠⚠ **Expect this in every licensed allied-health field with an A.S.-to-BS ladder** — respiratory care,
radiography, nursing, dental hygiene, health information management. **And note the inversion it produces:
the broader-SOUNDING title is usually the entry-level course, and the narrower-sounding one is often
closest to the statewide description. Judge scope by the programme's level, not by the title.**

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

### ⚠⚠ FOUR different shapes behind a `C` suffix — do not conflate them (batch 183, extended 219)

| Shape | Example | What it means | What transfers |
|---|---|---|---|
| **Split family** | `CGN3501C` (UF) vs `CGN3501` + `CGN3501L` (UWF); `EEE3308C` vs `EEE3308` + `EEE3308L` | one course, packaged as one enrolment or two | same content, **3 cr vs 4 cr**, one grade vs two |
| **Suffix divergence** | `BCN3224C` (UF, integrated) vs bare `BCN3224` (UWF, lecture only, no lab partner) | ⚠ **genuinely different courses** — one has laboratory hours the other does not | content differs |
| **`C` nobody carries** | `TPA3230C`, `COP3014C`, `INP3004C`, `CJE3674C`, `CTS4348C`, `DAA2204C`, `EEE3396C` | the queued id may not exist at any institution | see `REVIEW_QUEUE.md` item 28 |
| ⚠⚠⚠ **Institutional signature** (batch 219) | `TPA3064C` (FAU) vs `TPA3064` (UWF); `TPA3601C` (UCF) vs `TPA3601` (USF, UWF); `TPA4021C` (UWF) vs `TPA4021` (FSU, UF); `TPA4045C` (USF) vs `TPA4045` (UWF, FSU); `TPA4077C` (UWF) vs `TPA4077` (FSU, USF) | ⚠⚠ **the SAME course, filed differently by different schools** — both ids are real, no institution carries both | content is the same; **an evaluator matching on the identifier sees a mismatch where there is none** |

⚠⚠⚠ **The batch-219 shape is the one most likely to be misread, because it looks like "a `C`
nobody carries" from whichever side you are standing on.** **Five of seven queued `TPA` `C` ids had a bare
twin at DIFFERENT institutions, and every one of the seven `C` ids was real.**

⚠⚠ **Diagnostic, and it is one flat-file pass — BEFORE WRITING ANY `C` ID, LOOK UP THE BARE
NUMBER, and read the answer from the carrier lists:**

| What you find | What it means |
|---|---|
| **the SAME institution carries both forms** | a course run in **two shapes** — lecture section and integrated section (batch 184, `PET3640C`). State the contact-hour difference. |
| ⚠⚠ **DIFFERENT institutions carry the two forms** | **one course filed two ways** (batch 219). Name the twin and who carries it; do not write a divergence block. |
| **no institution carries the bare form, or the `C` form** | the queued id may not exist — check before writing at all |

⚠⚠ **Diagnostic for the split family: RECIPROCAL concurrent prerequisites.** `EEE 3308` lists
`EEE 3308L*` and `EEE 3308L` lists `EEE 3308*` — **neither can be taken alone, so the pair IS the `C`
course.** Where the queue holds the `C` id, write one guide covering both halves and state the three
consequences: **credit count, two grades, and register for both.**

### ⚠⚠ Two institutions agreeing with each other outrank a statewide title (batch 183)

**`HFT4274`**: statewide title **Resort Management**; **FGCU teaches "Vacation Ownership & Timeshare" and
FIU teaches "Short-Term Rental / Vacation Ownership".** Two independent catalogs agree with each other and
both contradict the statewide label.

⚠ **The statewide title is a single SCNS label with no description behind it.** Two agreeing descriptions
are stronger evidence. **That condition is part of the rule, not background — check it
before applying the rule** (see the `HFT3053` refinement below). **Write to the agreeing pair, and say in the guide what to expect if a third
institution teaches the broader subject instead.** (Contrast `BSC1050`, where only ONE catalog was
reachable — there the divergence block is a warning, not a correction.)

#### ⚠⚠ Refinement (batch 201): the rule needs a bare LABEL, and TITLES are weaker than DESCRIPTIONS

**`HFT3053`** — statewide **"Prospectus on Tourism"**, and unlike `HFT4274` the statewide record carries
a **full, specific description** of an issues-and-impacts course. Both public carriers (Pensacola State and
UWF, identical titles, 3 credits) call it **Travel and Tourism Management**.

⚠⚠ **Two conditions of the batch-183 rule fail here.** The statewide record is **not** a bare label
— it has a description to weigh. And what the carriers supply is **titles, not descriptions**, so it is
two titles against one full description rather than two descriptions against one label.

**Handling where either condition fails: cover BOTH readings with a two-column test and say the evidence is
mixed.** ⚠ **Do not "correct" a described statewide subject on the strength of agreeing titles alone.**
Reserve the batch-183 correction for the case it was built for: a bare statewide label, contradicted by two
independent institution **descriptions**.

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

#### ⚠⚠⚠ SOLVED (batch 209): draft the prerequisite field at ~850 characters and let it grow

**The ceiling is now 1000, and for NINE consecutive batches every prerequisite in the batch exceeded it on
first assembly** — batches 201–208, needing up to four rounds of trimming each, with the endgame slow
because each edit moves the count by less than a sentence.

✅ **Batch 209 broke the run by writing short deliberately**: **three of six came in under the limit on
first assembly** (886, 924, 955 characters), and the three that ran over needed **one** trim round.

⚠⚠ **So the rule is: write the prerequisite to about 850 characters and stop.** It always grows during
assembly — the warnings accumulate as the research lands. **Writing to length and then cutting is the
expensive order; writing short and adding is the cheap one.**

#### ⚠⚠ Budget the SUM of SHARED blocks, not each one (batch 212, sharpened batch 215)

**A warning reused across a batch spends its length on EVERY course that uses it.** Batch 212 learned this
with one shared block (4 of 9 over). ⚠⚠ **Batch 215 had THREE — a credential warning, a placement warning
and a sequence warning — totalling ~1,100 characters of shared text before any course-specific content,
and 11 of 12 went over.**

⚠⚠⚠ **Revised rule: allow all shared blocks together about 400 characters, not 400 each.** Trimming the
blocks fixed 9 of 11; the rest needed individual trims. **Count the boilerplate first, then write the
course-specific text into what remains.**

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

#### ⚠⚠⚠ And sometimes the old vocabulary is not merely dated — it is contrary to STATE LAW (batch 206)

**`RED3310` is the strongest instance of this shape so far, and it differs in kind from `SYD4800` and
`SOW4700`.** Those were vocabulary the field had moved past. ⚠⚠ **This one has regulatory force behind it.**

**Florida requires evidence-based reading instruction, mandates K-3 screening and progress monitoring, funds
district reading coaches, and has revised the Reading Endorsement competencies and the B.E.S.T. ELA
standards accordingly.** ⚠ **So "reading as a process", three-cueing and guessing from context are not
merely out of date — they are contrary to what Florida requires and what the FTCE tests.**

⚠⚠ **Where a terminology-era divergence touches a LICENSED or CERTIFIED field, check whether the state has
legislated.** The consequence for the student is then concrete rather than academic: **preparation in the
superseded model leaves them unready for what their employer is required to do.** Expect the same shape in
**nursing, athletic training, respiratory care, behaviour analysis and social work.**

⚠ **And a caution that applies to every terminology-era case: A CATALOG TITLE CAN LAG A REVISED SYLLABUS BY
YEARS.** **Titles change slowly and syllabi change fast.** **Tell the reader to judge by the ASSIGNED TEXT
and the reading list, not the title** — for `RED3310` the test is whether the text is Moats, Kilpatrick,
Liben, Lindsey or Seidenberg.

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

### ⚠⚠⚠ COURSE-TYPE divergence — a campus course at one school, a PLACEMENT at another (batch 200)

**A new category, and not a variant of any above.** Not a different subject, not title drift, not credits, not
chronology, not terminology era: **the same number is a different KIND of course.**

**`EDG4442`** — statewide *Teaching Strategies and Classroom Management*:

| Institution | Its title | What it is |
|---|---|---|
| UWF | Effective Learning Environments | campus methods course |
| UF | Rethinking Discipline and Classroom Management | campus methods course |
| **UNF** | **Elementary Field Experience III** | ⚠⚠ **supervised school placement** |

⚠⚠ **Why it outranks a title divergence in consequence.** A placement carries **Level 2 background screening
before entry to a building**, the **school district's** calendar during the school day, a cooperating
teacher's evaluation, and a placement a school can terminate. **A student who registers expecting a methods
course and gets a placement cannot solve it by working harder** — the logistics either fit their term or
they do not.

⚠⚠⚠ **And the transfer consequence is harder than the usual one: state programme approval specifies required
COURSEWORK and required FIELD HOURS separately**, so **one number can satisfy one and not the other, with
nothing in the identifier to say which.** **Tell the reader to take the syllabus to the programme's
certification officer and ask specifically.**

**Handling: one guide on the statewide subject, with the placement reading LABELLED and its logistics spelled
out**, plus a two-column test. **Screening, calendar, mandatory reporting and FERPA go in the prerequisite
field**, per the batch-184 rule.

⚠ **Expect more.** Field experiences, practica, internships and clinicals are routinely numbered alongside the
coursework they accompany. **When a batch turns one up, add it here.** See `REVIEW_QUEUE.md` item 75 for the
open split question.

### ⚠⚠ SEQUENCE-POSITION divergence — the whole course at one school, a PHASE of it at another (batch 200)

**Distinct from the sequence-PARTNER rule below, which is about two numbers splitting a subject. This is one
number meaning different amounts of the same subject.**

**`ATF1100L`** — statewide title **`PRIVATE PILOT FLIGHT (2 - 3 HOURS) (L)`**; carriers **NWFSC 1, Polk State
1, UWF 3.** The prefix family explains it: `ATF1108` *Primary Flight I (1 hour)* and `ATF1109` *Primary
Flight II (1 hour)* split the certificate into phases, and ⚠ **`ATF1108`'s own statewide description says a
student completes it and "would then take ATF1100."** **So `ATF1100` is the complete flight course at one
institution and the second phase at another.**

**Handling: write the identifier's full subject, give the credit value that matches that reading, and state
the phase reading in `offering_notes` and the body — labelled as an inference where it is one.** ⚠ **Tell the
reader the question to ask: how many hours does this specific course include, and does it end at completion or
at a phase?** **Neither the credit count nor the title answers it.**

### ⚠⚠ The statewide TITLE is a data field — read it for parenthesised hour figures (batch 200)

**`PRIVATE PILOT FLIGHT (2 - 3 HOURS) (L)`.** ⚠⚠ **The state wrote the credit range into the title string**,
and **two of the three carriers sit BELOW the bottom of it** — the first case of the state's own record
carrying a credit figure that its carriers contradict.

- ⚠ **The `ATF` prefix does this repeatedly**: `ATF1103` "(5 HOURS)", `ATF1108` "(1 HOUR)", `ATF1600`
  "(1 HOUR)". **Read the title as data, not as a label.**
- ⚠ **The title also carries the `(L)` and `(G)` markers**, and `ATF1100`'s `IN_Lab` field says **`N`** while
  its title says `(L)`. **So `IN_Lab` is not reliable — match on `ID_Century` plus `DS_Course_Intent1`
  instead.**

### ⚠⚠ Where a REGULATOR measures the course, its floor beats the credit-to-hour convention (batch 200)

**`ATF1100L` was published at 40 contact hours, derived from the FAA minimum** — 35 flight hours under Part
141, 40 under Part 61 — **not from the Florida 1:15 convention.** A flight course's hours are hours in an
aircraft, **sold by the hour**, and the convention is meaningless for it.

⚠ **State the derivation and say the real figure is higher** where the regulatory number is a floor that
practice exceeds. **Expect the same shape wherever a licensing body sets hours**: flight training, clinical
and practicum hours, PSAV clock-hour programmes, apprenticeship hours.

### ⚠⚠⚠ EXTERNALLY-GOVERNED CURRICULUM — when the syllabus itself belongs to a body outside SCNS (batch 209)

**Every divergence rule in this file assumes the content authority is the INSTITUTION, with SCNS recording
it.** ⚠⚠ **`AFR` (Air Force ROTC) breaks that assumption: the curriculum is set nationally by Air Force
ROTC Headquarters (the Holm Center, Maxwell AFB), and every detachment in the country teaches the same
syllabus.**

⚠ **Distinct from the regulator's-floor rule above.** That is about **HOURS** — a regulator setting a
minimum the credit convention cannot describe. **This is about CONTENT AND TITLES — an external body
owning the syllabus itself.**

**Three consequences, and they invert the usual analysis:**

1. ⚠⚠ **The institutions CANNOT diverge from each other on content.** So institutional title variation is
   **pure catalog lag**, not a divergence signal — and the "two carriers agreeing outrank a statewide
   title" machinery (batch 183) is beside the point. **Do not write a divergence block for what is only
   two catalogs updating at different speeds.**
2. ⚠⚠⚠ **The statewide record is the LEAST current source available**, so it cannot be used to check a
   carrier's currency. On `AFR` it is forty years behind both carriers.
3. **The guide's statement of authority has to change.** These guides say: **judge the course by what the
   detachment issues in week one; nothing in this guide overrides cadre guidance.** ⚠ **That is the honest
   position whenever the real syllabus is issued by a body outside the state system** — and it is a
   stronger and more useful sentence than any hedge about institutional variation.

**Worked example — `AFR2132`, and the staleness is self-evident from the text:**

| | Statewide record | Current national curriculum |
|---|---|---|
| `AFR2132` | *The Development of Air Power II* — ⚠⚠⚠ description ends **"projects ahead to the year 2000"** | **Team and Leadership Fundamentals II** — leadership theory, team dynamics, ethics, Field Training prep |
| `AFR1112` | *The Air Force Today II* — "total force structure, offensive and defensive forces" | **Competition and Security** |
| siblings | ⚠ *Strategic Offensive Forces* / *Strategic Defensive Forces* — Cold War nuclear-triad vocabulary | — |

⚠⚠ **Note it is a change of SUBJECT, not just a title**: the AS200 year used to be air power history and
is now leadership and team fundamentals, with the history retained as case material. **Within Florida, UWF
uses the current national naming on all four numbers and Pensacola State still uses the older state
naming — same course, same national syllabus, different lag.**

⚠ **Where a statewide description names a future that has passed, say so in the guide.** It is the
clearest possible way to tell a student not to rely on the state record, and it is stronger evidence than
the embedded-date test (batch 208) because it needs no inference.

**Expect this shape in:** the other services' ROTC prefixes, nationally standardised certification
curricula, apprenticeship-linked coursework, and anywhere a national body **issues** the syllabus rather
than approving one.

#### ⚠⚠ And check the CREDIT arrangement, because an external curriculum does not standardise credits (batch 209)

**The national programme fixes the content; each institution still decides what to award for it.**
`AFR`'s Leadership Laboratory is the worked case:

| Institution | Leadership Laboratory |
|---|---|
| Pensacola State, UWF | **0 credits** |
| ⚠ Santa Fe College, University of Florida | **1 credit** |
| ⚠ UCF | folded into a **2-credit integrated `C` course** with the lecture |

⚠⚠⚠ **Identical, nationally-specified work is worth 0, 1, or part of 2 credits depending on the
institution — and the pattern repeats across all four years** (`AFR1101L`, `AFR1112L`, `AFR2130L`,
`AFR2132L`, `AFR4211L`). **Credit-count divergence (batch 185) and split-family (batch 183) operating
together on one prefix.**

**What a guide must say:** **progression is governed by the external programme, not the registrar — but
full-time enrolment status IS governed by the registrar.** ⚠ **So tell the reader to count their credits
WITHOUT the zero-credit component and check the total against whatever threshold applies to them**
(financial aid, scholarship conditions, athletic eligibility, insurance, visa status). See the
zero-credit-laboratory rule in the schema section.

### ⚠ A title inside an SCNS prerequisite string can be a LOCAL title (batch 200)

**`COM4564`'s statewide prerequisite reads *"COM4561 Social Media Content Development with a grade of C- or
above"* — but the statewide title of `COM4561` is *Social Media Campaigns*.** "Social Media Content
Development" is **UWF's** title.

- ⚠ **Do not read a title inside `DS_Prerequisites1` as the statewide title.** The records are
  institution-contributed and a local title can land in a statewide field.
- ⚠ **Useful in the other direction: a prerequisite naming a local title tells you which institution
  contributed the entry**, and therefore which catalog to check. Here it confirmed a real `COM4561`→`COM4564`
  sequence at UWF with an explicit C-minus floor.

#### ⚠⚠ The prerequisite field can also be CORRUPT — sanity-check it against the id pattern (batch 209)

**`ADV4802`'s statewide prerequisite reads `"ADV U101C"` — which is not a valid SCNS identifier at all.**
⚠ **The first corrupted value this project has met in that field, and it is easy to pass straight into a
guide as though it named a real course.**

**Standing check: before quoting `DS_Prerequisites1`, test any course-looking token in it against
`^[A-Z]{3}\s?\d{4}[A-Z]?$`.** A token that fails is a data defect, not a course. **Say so in the guide
and send the reader to the institution's catalog** — which is what `ADV4802`'s guide does.

#### ⚠⚠⚠ And it can DANGLE — a well-formed token naming a course the CARRIER does not offer (batch 219)

**A second, commoner defect, and the syntax check above does NOT catch it.** **`TPA4021C`'s statewide
prerequisite reads `TPA 4020 LIGHTING DESIGN I` — a valid identifier naming a real, active course.**
⚠⚠ **But UWF, the ONLY carrier of `TPA4021C`, does not offer `TPA4020`** (FSU and UF do). **So the
state describes a prerequisite chain that does not exist at the institution teaching the course.**

⚠⚠⚠ **And UWF's own alternative, `TPA 3020`, is carried by NO Florida public institution at
all** — so of the three numbers naming that gate, one belongs to other schools and one belongs to
nobody. **The real gate is `TPA3022`.**

**Standing check, cheap once the flat file is loaded: for every course-looking token in
`DS_Prerequisites1`, ask whether the CARRIER OF THE COURSE YOU ARE WRITING actually offers it.**
⚠ **Where it does not, name the dangling reference in the guide and put the REAL gate beside it** —
a student reading the state record would otherwise go looking for a course their institution does not have.

⚠ **Expect it wherever a prefix runs PARALLEL NUMBERING FAMILIES** (below): the statewide prerequisite
was written against one family and the carrier uses the other.

#### ⚠⚠⚠ PARALLEL NUMBERING FAMILIES — fragmentation running through a whole SEQUENCE (batch 219)

**Batch 207 measured number fragmentation on one LEVEL of Spanish. `TPA` shows it running through an
entire two-course sequence, so it compounds:**

| | Family A | Family B |
|---|---|---|
| **Lighting Design I** | **`TPA3022`** — FAU, UWF | **`TPA4020`** — FSU, UF |
| **Lighting Design II** | **`TPA4021C`** — UWF | **`TPA4021`** — FSU, UF |
| **Scene Design I** | **`TPA3064`** (UWF) / **`TPA3064C`** (FAU) | **`TPA3060`** — FIU, UF |
| **Scene Design II** | **`TPA4061`** — FIU, UWF | (none — FIU crosses families) |

⚠⚠ **Two anomalies worth noting because they defeat the obvious simplification.** The second
lighting course is **ONE number with TWO suffixes across the two families** — so the suffix, not the
number, separates them. And **`TPA4061` is carried by FIU, whose first course comes from the OTHER
family** — so the families are not clean institutional blocs.

⚠⚠⚠ **THE STRONGEST EVIDENCE THAT TWO FAMILIES ARE THE SAME COURSE IS AN INSTITUTION HEDGING
ITS OWN PREREQUISITE ACROSS THEM.** UWF requires *"TPA 3020 OR TPA 3022"* for `TPA4021C` and
*"TPA 3060 OR TPA 3064"* for `TPA4061`. **That is a department telling you, in its own catalogue, that it
treats the two numbers as interchangeable — and it beats any title comparison.** **Read institution
prerequisites for `OR` lists spanning statewide families; they are a free equivalence table.**

#### ⚠⚠ A statewide DESCRIPTION can be COPIED between numbers — diff the siblings (batch 219)

**`TPA4045` (Styles in Costume DESIGN) and `TPA3230` (Theatre Costuming I, a CONSTRUCTION course) share
EIGHT of their TEN statewide competency items verbatim.** ⚠⚠ **So the design number's competency
list carries CONSTRUCTION competencies** — *"costume cutting skills"*, *"high level skills in
development of patterns"* — **because they were carried across from the construction course.**

⚠ **Consequence: an item in a statewide competency list is NOT necessarily evidence about that specific
course.** **Drill: when a statewide description is a NUMBERED COMPETENCY LIST in the 1980s all-capitals
register, diff it against the sibling numbers in the family before quoting any item as a finding.** In
`TPA`, `TPA3601`, `TPA4020`, `TPA4045`, `TPA3060` and `TPA3230` are visibly one drafting exercise.

### ⚠⚠ SURVEY THE PREFIX FAMILY from the statewide CSV before writing — a standing move (batch 200)

**One already-downloaded CSV and one filter on `ID_Century` paid three times in a single batch:**

| Prefix | What the family revealed that the course's own record could not |
|---|---|
| **`ATF`** | the phase/whole-course split that explains a **3× credit divergence** |
| **`ATR`** | ⚠⚠ the profession's **move to graduate-level entry** — sibling numbers read *"admission to MAT degree program"* and *"admission into the Doctor of Athletic Training program"*, and several are graduate courses still carrying **4000-level numbers** |
| **`EDG`** | **four adjacent numbers** competing for classroom management (`EDG4442`, `EDG4443`, and `EDG4444`/`EDG4447` sharing a title) |

```python
rows = scns.read_report_csv('scratchpad/sw_<PFX>.csv')
[r for r in rows if r['ID_Century'].startswith('44') and r['CourseStatus'] == 'ACTIVE']
```

⚠ **Do this whenever a course's credits diverge, its title diverges, or its field has a licensure
dimension.** **A sibling number's prerequisite string is frequently the most informative sentence available
about the course you are writing.**

### ⚠ A profession can outgrow its undergraduate numbers — say so (batch 200)

**`ATR3132` is an undergraduate course written for "athletic training majors" in a profession whose
entry-level degree is now the master's.** ⚠⚠ **An undergraduate `ATR` course is pre-professional coursework
and does not accumulate toward certification eligibility** — and no catalog says this.

**Handling: state the current entry requirement, say plainly what the course does and does not do, and tell
the student to work backwards from target graduate programmes' prerequisite lists** (this course generally
satisfies a biomechanics requirement — ⚠ **which is its real value, and worth naming**).

⚠ **Watch for the same shape elsewhere**: physical therapy (DPT), occupational therapy, audiology,
pharmacy, and physician assistant programmes have all moved their entry credential upward, leaving
undergraduate courses in those prefixes serving a purpose their titles no longer describe.

### ⚠ `VAR` in the flat file's credit column (batch 200)

**`TPA2290L` at UCF reads `VAR`, not a number**, where the other three carriers read `1.0`. ⚠ **Handled under
Ron's 2026-09-11 rule: `credits` is null in `offering_notes` and the note carries it — no min/max pair.**

**Say what it means for the reader:** the value depends on the assignment's scope and is set with the
department, **so ask what your registration is worth before you register**; and a variable-credit course
transferring into an institution that treats the number as a fixed value is settled by the logged hours and
the work record, not by the number.

### ⚠⚠ DEPARTMENTAL divergence — the same number in two different departments (batch 205)

**Distinct from the batch-187 departmental-placement signal.** That rule read a department off ONE
institution's own catalog line. ⚠⚠ **This is the same number taught in DIFFERENT departments at
different institutions, with the statewide record showing neither the department nor the consequence.**

**`POS3625` The First Amendment** is clean between institutions — identical titles at UNF and FSU, all
three carriers at 3 credits. ⚠ **But it is taught in political science at some institutions and in
journalism and mass communication at others:**

| Political science / public law | Journalism / mass communication |
|---|---|
| all six freedoms; **religion clauses at length**; doctrinal development | ⚠ **speech and press**; defamation, privacy, access and shield laws in practical detail; religion clauses lightly |

⚠ **Both are legitimate and they are different preparations** — a pre-law student wants the first, a
journalism student the second.

**Handling: give a diagnostic the reader can actually apply to the SYLLABUS, since the department cannot be
read from the data.** For `POS3625`: **look for the religion clauses on the reading list.**

⚠⚠ **Expect this wherever a subject has two departmental homes**: media law, statistics, technical
writing, ethics, research methods, nutrition, and public speaking. **The flat file will look clean and the
course will not be.** See `REVIEW_QUEUE.md` item 88.

### ⚠⚠⚠ SEQUENCE-LENGTH divergence — the same field as ONE course or as TWO (batch 204)

**Distinct from sequence-position (one number meaning the whole course or a phase) and from the
sequence-PARTNER rule. Here the STATE numbers the same field both ways.**

**`PHY3107`** is *Modern Physics II*, the second half of a two-term sequence with `PHY3106`. ⚠⚠
**But `PHY3101` "Elements of Modern Physics" is a ONE-TERM upper-division treatment of the same field** —
and Florida numbers modern physics at least **seven** ways in total.

⚠⚠⚠ **Three consequences, and the guide must state all three:**

1. **A `PHY3101` completer has done ONE term, not the first half of two.** ⚠ **A one-term course
   compresses, and what gets compressed is usually the back half of the field** — for modern physics,
   the nuclear, solid-state and particle material, which is exactly what the second course is about.
2. ⚠ **A `PHY3106` completer transferring to a one-term institution may find there is no second course
   to take**, so the material is simply not available.
3. ⚠⚠ **Check how many institutions carry the second course at all.** **Only TWO Florida public
   universities carry `PHY3107`**, so a student cannot assume a second term exists at theirs.

**Handling: name the one-term alternative explicitly, say what it compresses, and tell the reader to send a
TOPIC LIST rather than a title on transfer** — departments place by content coverage. ⚠ **Expect
this wherever a field is taught as both a survey and a sequence**: modern physics, organic chemistry,
anatomy and physiology, world history, and the two-term-versus-one-term language sequences.

### ⚠⚠⚠ ORDINAL-BASE divergence — the same ordinal counted from a different origin (batch 203)

**Not title drift. The same numbering convention applied to a different starting point.**

**`JPN2200`** statewide is **"Intermediate Japanese I"**; **UWF calls it "Japanese III"**. **`JPN2201`** is
**"Second-Year Japanese 2"**; UWF calls it **"Japanese IV"**. ⚠⚠ **UWF counts SEMESTERS from the
start of the language** (Japanese I and II are the first year); **SCNS counts WITHIN the intermediate year.**
Both are correct.

⚠⚠⚠ **The consequence is a failed search, not a wrong course: a student looking in a UWF
catalog for "Intermediate Japanese I" will not find it**, and the trap runs both ways for anyone reading the
statewide list.

**Handling: state both namings explicitly and say they are the same course.** ⚠ **Expect it wherever a
subject is numbered by ordinal** — languages, `I`/`II` course pairs, studio levels, ensemble levels.

⚠ **Two related naming traps found on the same pair.** **The statewide titles of a sequence can be
internally inconsistent** (*"Intermediate Japanese I"* beside *"Second-Year Japanese 2"* — different
words and numeral style on consecutive numbers). And **an institution can use ONE title for BOTH halves of a
sequence** (UCF: *Intermediate Japanese Language and Civilization* for `JPN2200` and `JPN2201`) —
**tell the reader to register by NUMBER, not title.**

### ⚠⚠⚠ The `MUN` level digit encodes the STUDENT, not the course (batch 203)

**Florida numbers each music ensemble at three levels — and they are frequently the same ensemble.**

| Ensemble | Lower | Upper | Graduate |
|---|---|---|---|
| Symphony Orchestra | `MUN1210` | `MUN3213` | yes |
| Chamber Orchestra | `MUN1220` | `MUN3223` | `MUN6225` |
| String Ensemble | `MUN1410` | `MUN3413` | `MUN6245` |
| Guitar Ensemble | `MUN1480` | `MUN3483` | `MUN6485` |

⚠⚠⚠ **The same rehearsal, conductor and concert — with a first-year student, a senior and
a master's student enrolled under three different numbers.** **The level digit records the player's academic
standing.**

- ⚠ **"Upper Level" is NOT "more advanced ensemble"** — the chair is decided by the audition.
- ⚠⚠ **Tell the reader to register at their own classification**; credit at the wrong level may
  not count where a requirement expected the other.
- ⚠⚠ **You CANNOT derive the other level's number by changing the first digit.** The lower-level
  symphony orchestra is **`MUN1210`, not `MUN1213`**. **Look it up.**

⚠ **Also on `MUN`: the statewide record sometimes states an explicit REPEAT ALLOWANCE** —
`MUN3426` reads *"may be used in the degree program a maximum of 8 times."* **Where it appears, state it and
tell the reader to confirm how many their OWN degree counts**; a state ceiling is not a promise the degree
wants eight.

### ⚠⚠ MISFILING — when a carrier uses a number the state assigns to something else (batch 203)

**Distinct from subject divergence: here there is a RIGHT answer and the guide can name it.**

**`MUN3483`** is statewide **Guitar Ensemble**. UWF matches it; **UNF runs a JAZZ guitar ensemble** and
⚠⚠⚠ **UCF runs a STRING ensemble — a different instrument family.** And the state
**already numbers both**: jazz guitar at `MUN3484`/`3486`/`3488`, string ensemble at
`MUN3413`/`3414`/`3243`.

⚠ **FIFTH case of this shape as of batch 207**, and they are not alike — which is why the
handling differs:

| Number | What was misfiled | Shape |
|---|---|---|
| `PUR4801` | UWF's PR **campaigns capstone** on the *cases* number | a different course in the same subject |
| `MUN3483` | UCF's **string ensemble** on the *guitar ensemble* number | ⚠⚠ a different SUBJECT |
| `PSY3215` | FIU's **`PSY3211` methods-and-data-analysis course** on the *(CONT)* number | ⚠ the same subject at a different SEQUENCE POSITION |
| `SPM4012` | FIU's title is the statewide title of **`SPM4018`** (which nobody carries) | ⚠ TITLE-only misfiling — the content still matches |
| **`SPN3410`** | **UWF's `SPN3400` course** (*Conversation and Composition*) on the `SPN3410` number, **and `SPN3400` holds something else** | ⚠⚠⚠ **RECIPROCAL — a transposed PAIR** |
| **`TPA3223C`** | **UCF and FAU teach lighting DESIGN** on the number the state defines as lighting **TECHNOLOGY** | ⚠⚠⚠ **the MAJORITY of carriers are the ones misfiling** |

#### ⚠⚠ When MOST carriers misfile, the state is still the reference — but say so carefully (batch 208)

**`TPA3223C` is the first case where two of three carriers deviate.** ⚠ It is still misfiling rather than a
stale statewide title, because **the title/description test above comes out "agree"**: the state says
*Lighting Technology* and its description says *"equipment, dimmers, control and other electronics."*
And the batch-203 tell is decisive — **Florida numbers lighting design separately and the number is IN
USE**: `TPA4020` *Lighting Design I* is carried by FSU and UF.

⚠⚠ **CORRECTED, batch 219: `TPA4020` is not THE lighting-design number, it is ONE OF TWO.**
**`TPA3022` *Lighting Design 1* is a second, equally active statewide number, carried by FAU and UWF.**
⚠ **This STRENGTHENS the misfiling conclusion rather than weakening it** — there are now two
dedicated design numbers in use, so `TPA3223C`'s deviating carriers had two places to put a design course
and used neither. **But do not write that `TPA4020` is where Florida numbers lighting design; write that
Florida numbers it in two parallel families** (see PARALLEL NUMBERING FAMILIES above).

⚠⚠ **What makes this worth a guide's strongest warning is that the two readings are different
PROFESSIONS** — electrician and designer are different jobs, different unions (IATSE vs USA Local 829) and
different career paths, **and electrics is where nearly everyone starts and where the jobs are.** **A
student who needs the electrics skills and takes a design section graduates able to draft a plot and unable
to get hired to hang it.**

⚠ **This is the same professional-division split already open on `TPA3230C`** (costume construction vs
design, `REVIEW_QUEUE.md` item 25). **Two instances in one prefix makes it a `TPA` pattern, not a
coincidence — expect it on scenery, sound and costume numbers too, and check the design/craft axis on every
`TPA` course.**

#### ⚠⚠⚠ The reciprocal sub-shape: BOTH numbers displaced, in exchange with each other (batch 207)

| | State's definition | UWF | FAU | FIU |
|---|---|---|---|---|
| `SPN3400` | *Conversation and Composition I* | ⚠⚠ *Advanced Stylistics* | *Advanced Spanish: Conversation* | — |
| `SPN3410` | *Advanced Oral Expression I* | ⚠⚠ *Composition and Conversation* | ⚠ *Advanced Spanish: Conversation* | ✅ matches |

⚠⚠ **This is worse than a single misfiling, because checking the OTHER number does not resolve it — both
are wrong, so the usual diagnostic ("a dedicated statewide number exists for what they're teaching") points
back at a number that is itself occupied.** ⚠ **And FAU carries the IDENTICAL title on both numbers**, so
within FAU they cannot be told apart by title at all.

⚠⚠ **Drill, and it is cheap: whenever a misfiling is found, look up what the DISPLACED number holds at the
SAME institution.** If it holds the first number's subject, it is a transposition and **both guides need
the warning** — including any already published. `SPN3400` had a live guide when this was found; see
`REVIEW_QUEUE.md` item 89.

⚠⚠ **The mildest and probably commonest shape is the last: same subject, wrong position in a
sequence.** **What differs is what the course ASSUMES, not what it covers** — so the warning a guide owes
the reader is *"find out whether this is the first or the second course in the sequence,"* not *"this may be
a different subject."* ⚠⚠ **The tell: a dedicated statewide number exists for what the institution is
actually teaching.** **Handling: write the statewide subject, label the misfilings, show the numbering
table, and give the reader a concrete diagnostic** — for `MUN3483`, *which instruments does this
ensemble contain, and is the repertoire notated or chart-based?* See `REVIEW_QUEUE.md` item 83.

### ⚠⚠⚠ ALTERNATE-LEVEL PAIR — the state builds TWO versions and makes the student choose (batch 212)

**Every shape above describes institutions disagreeing, or a record going stale. This one is different:
SCNS has DELIBERATELY created a lower-division and an upper-division version of the same course, and it
says so in the course record.** All four `(U)` numbers in the `ATF`/`ATT` flight-instructor family carry
this sentence verbatim:

> *"As a higher-level course, it offers training beyond the scope of the lower-level alternate course.
> **Students must choose whether to take the lower-level or upper-level version of this course.**"*

⚠⚠⚠ **THE TEST IS THE SENTENCE, NOT THE `(U)` MARKER.** Checked immediately on the next batch: **`BCN`
has 279 active statewide records, several carrying `(U)`, and NOT ONE contains the "must choose"
sentence.** `(U)` on its own means only *upper division*, which is common and uninteresting.

**A real alternate-level pair needs all three:**

1. the **"students must choose"** sentence in the statewide description (`grep -c "MUST CHOOSE"` over the
   prefix CSV settles it in one command);
2. a **sibling with DIFFERENT last-three-digits** covering the same subject — `ATF` paired 500↔502,
   510↔511, 530↔531 and `ATT` paired 130↔134, **never the same number at two levels**;
3. `DS_Course_Intent1` reading **`UPPER` against `LOWER`** across that pair.

⚠⚠ **The cleanest confirmation is textual: `ATT3134`'s statewide description is `ATT2130`'s WORD FOR
WORD plus two sentences naming what the upper version adds.** Check that once the sentence has matched.

| Lower | Upper `(U)` | Upper adds |
|---|---|---|
| `ATF2500L`/`ATF2500` | `ATF3502L` | simulation technique, curriculum development, mentorship |
| `ATF2510L` | `ATF3511L` | the same, **plus 15 flight hours against 10** |
| `ATF2530L` | `ATF3531L` | the same |
| `ATT2130` | `ATT3134` | the same, **plus the FAA Advanced Ground Instructor certificate** |

⚠⚠ **Do not confuse it with three shapes it resembles:** the `MUN` level digit (which encodes the
STUDENT's standing on ONE course), sequence-POSITION divergence (one number meaning a whole course or a
phase), and sequence-LENGTH divergence (a field taught as one course or two). **Here both versions exist
at once, under different numbers, and the student picks one.**

**Handling: write BOTH halves, and put the choice in each.** A student landing on the lower number
otherwise sees nothing about the decision. ⚠ **Check whether one institution carries both** — Polk State
carries both halves of all four pairs at **equal credit**, which makes the upper version strictly better
there, and the guides say so and tell the reader to ask an adviser to justify the lower one.

#### ⚠⚠⚠ Why the choice matters — and it is worth 250–500 FLIGHT HOURS

**Two consequences, and no catalogue states either.**

1. **Upper-division credit.** A bachelor's degree requires it and a 2000-level course cannot supply it
   (Ron's 2026-09-01 correction: the 2000→3000 step is the real boundary).
2. ⚠⚠⚠ **A federal rule keyed to a COUNT of credit hours.** Under **14 CFR 61.160** the reduced-hour
   **Restricted-Privileges ATP** turns on **semester credit hours of aviation coursework** — **1,000 hours**
   with a bachelor's and **60** such credits, **1,250** with an associate and **30**, against 1,500
   standard. **Taking 1-credit versions across the three flight-instructor courses costs six credits
   against that count**, and the gap between thresholds is **250 to 500 flight hours.**

⚠ **State the two cautions:** the reduction needs an institution **holding an FAA letter of authorisation**,
and **that institution certifies eligibility** — so tell the reader to ask their programme, never to infer
it from a course number.

⚠⚠ **GENERALISE THIS: wherever a licensed field ties a federal or state benefit to a COUNT of credit
hours, a credit-value divergence stops being an accounting curiosity and becomes a career consequence.**
**Look for it in nursing, respiratory care, radiography and the other licensure ladders.**

#### ⚠⚠ And the credit divergence beneath it: ONE federal certificate, FOUR credit values

The batch-209 `AFR` rule said an external body can own a syllabus while each institution sets the credit.
**The CFI-Airplane certificate is the cleanest instance yet, because the federal requirement is one
published number that never moves:** `ATF2500L` **1 credit** (NWFSC, Polk State), `ATF2500` **2** (Broward,
FSCJ), `ATF3502L` **1** at Polk State and **3** at UWF — and **all four require the identical 25 hours of
flight training**, documented independently by three catalogues. **The work does not change. The credit does.**

#### ⚠⚠⚠ On flight courses the FAA minimum is also a BILLING floor

**NWFSC states on every flight course what no other Florida institution says out loud:**

> *"the hours above are based on FAA-syllabus minimums, and students will often exceed these minimum hours.
> **The cost for these additional flight hours is not covered by the course fee.**"*

⚠ **Contact hours on an `ATF` course are hours in an aircraft, sold by the hour** (the batch-200 rule), **so
exceeding the syllabus minimum — common, and not a failure — is charged to the student.** Say it, and tell
the reader to ask what recent students actually averaged.

⚠⚠ **Check whether the practical test is included.** Florida's own record for `ATF2510L`: *"This course does
not include the checkride; it is at the student's discretion to schedule and complete the MEI checkride."*
**So a student can complete the course, earn the credit, and not hold the rating.**

⚠ **Expect the validator to WARN on these** (3 credits against 20–31 contact hours). **That warning is
correct to keep** — the 1:15 classroom convention does not apply to flight training, per the `ATF1100L`
precedent. State the derivation in the guide and label the figure a floor.

### ⚠⚠⚠ The SAME `L` id as a 1-credit lab AND a full 3-credit course (batch 214)

**`BSC4401L` is the worst transfer trap found so far, because the split-family shape lands on the `L` id
itself:**

| | **UWF** | **FIU** |
|---|---|---|
| `BSC4401L` | *Forensic Biology*, **3 credits** — the COMPLETE course, standing alone | *Forensic Biology Lab*, **1 credit** — the LABORATORY only |
| companion | none | ⚠ **`BSC4401`** lecture, 3 cr, **corequisite** |
| total | 3 credits, one grade | 4 credits, two grades |

⚠⚠⚠ **Transfer matches on the NUMBER and fails on the CONTENT in both directions.** Tell the reader to
send the syllabus and the credit value, never the number. ⚠ **And note the suffix is doing both jobs at
once** — conventional at FIU, a full course at UWF — so the `L` warning below is not just "sometimes
bigger", it is **unreliable in both directions on the same id.**

### ⚠⚠ Read `hs_credit` from the CSV, and run the distribution test EVERY prefix (batch 214)

**The same field means opposite things in different prefixes, so the one-`Counter` test (batch 207) is the
gate before writing anything about it:**

| Prefix | `DS_High_School_Credit1` | Verdict |
|---|---|---|
| `ATF` / `ATT` | uniform | boilerplate — say so, or say nothing |
| `BOT` | 116 ELECTIVE, **6 SCIENCE** | discriminating |
| `BSC` | 248 ELECTIVE, **24 SCIENCE** | discriminating |

⚠⚠ **`BSC2311` is one of the 24**: a dual-enrolled student earns **high-school SCIENCE credit**, not
elective — it fills a science graduation requirement *and* earns college credit. **Lead with it where it
appears; nothing a student normally reads says it.**

⚠⚠⚠ **TOOLING CORRECTION: read these two fields from the statewide CSV, NOT the flat file.** The flat
file's `transferable` slot actually holds the **high-school-credit code** (`'EL'`/`'SC'`), so
`scns.FIELDS`' offsets for that pair are shifted. The flat file stays authoritative for carriers, credits,
titles and the Gordon Rule / gen-ed flags. See `REVIEW_QUEUE.md` item 97.

### ⚠⚠ Dual-listing is a DEPARTMENTAL pattern — probe for it, do not wait to meet it (batch 214)

**The batch-186 rule came from one instance. Three of four UWF Biology courses in one batch were dual
-listed** — `BOT4850`/`BOT 5852`, `BSC4303`/`BSC 5305`, `BSC4401L`/`BSC 5406L`.

⚠ **Standing practice: on any UWF Biology 4000-level course, look for "offered concurrently with".** It is
easy to read past, and **both consequences must be stated**: the pace sits above a typical undergraduate
course (a benefit), and **taking the undergraduate version may BLOCK taking the graduate one for credit
later** — which has to be known before registering, not after.

### ⚠ A prerequisite token that fails the id pattern is a DEFECT *or* NOTATION — they differ (batch 214)

**The batch-209 test** (`^[A-Z]{3}\s?\d{4}[A-Z]?$`) **correctly flags both, but the handling differs:**

| | Example | Handling |
|---|---|---|
| **Defect** | `ADV4802`'s `"ADV U101C"` — a single malformed token | say so, send the reader to the catalogue |
| **Notation** | `BOT4734C`'s `"BOT L010 OR BSC L010, CO: BOT U734L"` — ⚠ a consistent `L`/`U` scheme marking LOWER and UPPER division | ⚠ **decode and explain it** — here it means a lower-division biology prerequisite with an upper-division lab corequisite |

⚠ **The tell is systematic structure.** One bad token is a defect; a repeated prefixing convention is
notation, and decoding it serves the reader better than a warning does.

### ⚠⚠⚠ LICENSED-PROFESSION SEQUENCES: accreditation, cohorts and clinical hours (batch 215)

**`RET` (respiratory therapy) is the first complete professional sequence this project has written, and it
established handling that applies to EVERY licensed allied-health prefix** — nursing, radiography, dental
hygiene, health information management, athletic training.

⚠⚠⚠ **1. The credential runs through the PROGRAMME, not the credit.** CoARC accredits respiratory care
programmes **as programmes**, and in two distinct kinds — **entry into professional practice** and
**degree advancement** for therapists who already hold credentials. **NBRC exam eligibility runs through
completing an appropriate accredited programme, NOT through accumulating transferable credit.** A student
can hold credit for every course and remain ineligible. **Say so in every course of the sequence**, and
tell the reader to verify with the accreditor, the credentialing body and the state board directly.

⚠ **Work out WHICH KIND the programme is** — the tell is the curriculum: an entry-level programme has a
foundations course, a clinical sequence, and a terminal practicum completing new-graduate competencies.
⚠⚠ **Do not assume the sector predicts it.** The batch-206 note (FCS = entry-level A.S., SUS = degree
completion) is a tendency, not a rule: **UWF is SUS and runs an entry-level baccalaureate**, the batch-200
`ATR` shape of a profession raising its entry credential.

⚠⚠ **2. Cohort structure changes the arithmetic of a marginal grade.** Courses run **once a year** in a
fixed, gated sequence with clinical placements arranged around it. **A failure delays not one term but
until the course runs again — about a year — and may require re-application.** Reciprocal corequisites
make it worse: where a lecture and lab each list the other, **failing either means repeating both.**
**State this; students do not know it in their first term.**

⚠⚠⚠ **3. Clinical practicum hours are NOT classroom hours.** Use roughly **three contact hours per credit
per week** — 3 credits ≈ **135 hours**, 4 credits ≈ **180** — not the 45/60 classroom convention, which
misdescribes a rotation badly. **The validator will WARN and the warning is correct to keep** (same as the
flight-hour case). **Label the derivation.**

⚠⚠ **4. Placement clearances go in the PREREQUISITE field** (the batch-184 rule) and **must be started
weeks before the term**: Florida **Level 2 fingerprint screening**, immunisations and TB screening, drug
screening, health insurance, **BLS** — plus **ACLS** for critical care and ⚠ **NRP and PALS before a
neonatal-paediatric rotation**, where provider courses fill up and an uncertified student simply cannot
enter the unit.

⚠ **5. Transfer on COMPETENCY RECORDS, not course numbers.** A receiving programme must attest to your
clinical competence under its own accreditation, so it may accept the credit and still require its own
practicum. **Tell students to keep every competency evaluation and clinical hour log.**

### ⚠⚠ A LAB titled as its LECTURE — expect it on any lecture+lab prefix (batches 215, 217)

**Florida frequently gives a laboratory the title of its lecture, with no separate description**, so the
statewide record cannot distinguish the halves at all:

| Lab | Statewide title it is given |
|---|---|
| `RET3028L` | *Fundamentals of Respiratory Therapy* (its lecture's) |
| `RET3493L` | *Respiratory Disease Assessment* (its lecture's) |
| `GIS4035L` | *Remote Sensing of the Environment* (its lecture's) |
| `GIS4043L` | *Principles of Geographic Information Systems* (its lecture's) |

⚠ **Four instances in two batches. Stop treating it as a finding and expect it.** **Go to the
institution's catalogue for anything about the lab specifically** — both institutions distinguish the
halves properly in their own records even where the state does not.

### ⚠⚠ Formal AI course ATTRIBUTES are appearing — a new category (batch 217)

**UF's catalogue records an *Artificial Intelligence* attribute against `GIS4102C` (GIS Programming).**
⚠ The first formal institutional AI course designation this project has met.

**It matters to a student rather than being trivia:** UF runs a university-wide AI initiative, and such
designations **may count toward an AI certificate or minor and may appear as a transcript notation.**
⚠⚠ **Tell the reader to find out what it counts toward** rather than assuming it is decorative.

⚠ **Expect more.** Institutions are beginning to tag AI-related coursework formally, and no other source
records it. **Watch the UF CourseLeaf `Attributes:` line**, and check whether other catalogues carry
something equivalent.

### ⚠⚠ UWF DUAL-LISTS across departments — check every UWF 4000-level course (batches 214, 215, 217)

**The batch-186 rule came from one instance. It is now a UWF-wide practice, not a departmental quirk:**

| Department | Courses |
|---|---|
| Biology | `BOT4850`/`BOT 5852`, `BSC4303`/`BSC 5305`, `BSC4401L`/`BSC 5406L` |
| Health Sciences | `BSC4401L` and the `RET` sequence |
| Earth &amp; Environmental Sciences | `GIS4006`/`GIS 5007`, `GIS4035L`/`GIS 5027L`, `GIS4043L`/`GIS 5050L` |

⚠ **Standing practice: look for "offered concurrently with" on ANY UWF 4000-level course.** Both
consequences must be stated — the pace sits above a typical undergraduate course (a benefit), and
**taking the undergraduate version may BLOCK taking the graduate one for credit later**, which has to be
known before registering.

### ⚠ An `L` suffix does NOT reliably mean "1-credit lab partner" (batch 203)

**`OCB3108L`** — *Study Abroad in Florida: Marine Field Studies* — runs **3–4 credits** at UNF
and UWF. ⚠⚠ **It is a full field and study-abroad course numbered `L` because it is ENTIRELY
practical work**, not a laboratory attached to a lecture.

⚠ **This is the first counterexample to an assumption embedded in the project's contact-hour heuristics
and in `validate_drafts.py`'s 1-credit expectation for `L` courses.** **Check the credit value before
applying the lab-guide treatment.**

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
| **UWF** | `catalog.uwf.edu/courseinformation/courses/<prefix>/<prefix>.pdf` (**lowercase**) | ✅ **working** — one fetch per prefix, full descriptions. The workhorse. ⚠⚠ **But it does NOT cover every prefix UWF carries** (found batch 212): `atf` **404s** and `att` is a **title-only stub**, though UWF is an active SCNS carrier of both. The course-information index simply does not list them. **A 404 here is not proof UWF lacks the prefix — fall through to the search route below.** |
| **⚠⚠ UWF PDF parsing** | `scratchpad/uwf_pdf.py` | ⚠⚠⚠ **USE THE PARSER, NOT A NAIVE SPLIT (batch 215).** CourseLeaf lays each entry out as `HEADER … Co-requisite: RET <other>` **then** the description, **then** the next header — so **splitting extracted text on `/ABC \d{4}/` cuts at the COREQUISITE REFERENCE and attaches every description to the WRONG course.** It produced three confidently wrong descriptions before being caught. ⚠ A second attempt failed differently: a lazy `(.*?)` title pattern spanned a whole description to reach the next entry's "College of" — **constrain the title to ≤90 chars with no sentence period.** ⚠⚠ **The general lesson: an extraction bug does not error, it returns plausible text for the wrong record.** It was caught only because "Clinical Practicum I" described ventilator theory. **Sanity-check extracted text against what the title claims.** |
| **UWF (search route)** | **`catalog.uwf.edu/search/?P=<PREFIX>%20<NUMBER>`** — `scratchpad/uwf_search.py` | ✅✅ **TOOLED AND RECORDED 2026-09-15 (batch 212). Use whenever the prefix PDF 404s or comes back empty.** ⚠ The session before had already found this route by hand and left cached results but **no register entry**, so batch 212 rediscovered it from scratch — **record a route here the moment it works, not at the end of the batch.** Returns the full course block: description, credits, prerequisites **and the college and department** (a batch-187 departmental signal the PDFs never carry — it is how UWF's aviation programme was found to sit in the College of Business). ⚠ The element is `<article class="searchresult search-courseresult">`, **not a `<div>`**. |
| **FGCU** | `catalog.fgcu.edu/courses/<prefix>/<prefix>.pdf` (**the `.pdf`, not the directory**) | ✅ **working.** ⚠ The old directory URL is what was bot-blocked; the PDF answers. **Now the single most productive cross-check source in the project** — it documents credits explicitly and has produced the divergence a guide turned on in three consecutive batches. |
| **FSU** | `registrar.fsu.edu/bulletin/undergraduate-departments/<department>` | ✅ **working, and general-purpose.** Previously recorded here as useful only for the FAMU-FSU joint engineering college — **it is not.** Clean HTML with full descriptions, credits and prerequisites for `psychology`, `philosophy`, `social-work` and others. **Use it as the third vote when UWF and FGCU disagree.** |
| **⚠⚠ SCNS (statewide)** | `scratchpad/scns.py` — `flscns.fldoe.org` | ✅✅ **SOLVED 2026-09-09 (EEE sweep). CHECK THIS FIRST, BEFORE ANY INSTITUTION CATALOG.** `flatfile` downloads the whole SCNS database (~80 MB) carrying, per course, **both the institution's title AND the statewide title**, the authoritative institution list for the **exact** id, per-institution credits, and Gordon Rule + gen-ed flags. `statewide <PREFIX>` returns full descriptions, prerequisites and transferability as CSV. ⚠ Routes are **extensionless**; you must **accept the terms modal** first or reports return 0 rows silently; the report is an async SSRS viewer. All three handled in `scns.py`. See `SOURCES.md` Tier 3. |
| **UF** | **`catalog.ufl.edu/UGRD/courses/<department>/`** — plain CourseLeaf page | ✅ **UPGRADED 2026-09-09.** The department page returns **full descriptions, credits and prerequisites** for every course in the department — far better than the POST API below, which gives title and existence only. Department slugs are descriptive (`electrical_and_computer_engineering`). |
| UF (old route) | `scratchpad/uf.py` — the `catalog.ufl.edu/course-search/api/` POST | ⚠ superseded by the CourseLeaf page above; keyword must be spaced (`"POT 4204"`), title and existence only, `route=details` broken. |
| **UCF** | **Kuali API** — `ucf.kuali.co/api/v1/catalog/public/catalogs/`, then `/api/v1/catalog/courses/<catalogId>`, detail by **`pid`** | ✅✅ **NEW 2026-09-09 — the first working UCF route in the project.** UCF's acalog catalog (`catalog.ucf.edu/preview_course_nopop.php`) now 307s to a WordPress shell; the real catalog is **Kuali** at `ucf.kuali.co`. Returns 3,676 courses with description, credits, **weekly lab hours** (`labStudioFieldWorkHours`), structured prerequisites, department, college and terms offered. ⚠ The detail endpoint needs the **`pid`**, not the `id` — the `id` returns an empty list. UCF is **3,872 workable rows**, so this unblocks the single largest school in the queue. |
| **Broward** | `catalog.broward.edu/course-descriptions/<prefix>/` | ✅ **RECOVERED 2026-09-06** and used productively in batch 166. ⚠⚠ **The only routinely fetchable Florida source that publishes CONTACT HOURS explicitly** ("Total Contact Hrs: 48.00 / Lecture Hrs: 48.00") plus minimum-grade prerequisite conditions. **Go here first whenever a contact-hour figure is in doubt.** |
| **Valencia** | `catalog.valenciacollege.edu/coursedescriptions/coursesoffered/<prefix>/` | ✅ **RECOVERED 2026-09-06** — 200 with full body on `psy` and `mus`. Same regression, same recovery. |
| **DSC** | `daytonastate.smartcatalogiq.com/en/<year>/college-catalog/course-descriptions/<prefix-slug>/<level>/<course>` | ✅ **Confirmed on the CURRENT catalog 2026-09-07**, not just historically. ⚠ Two gotchas: the prefix slug is descriptive (`cop-computer-science`, not `cop`), and **the index page lists only titles — the individual course page carries description, credits, prerequisite and term**. A trailing slash 404s. **Same platform as IRSC.** |
| **UNF** | live catalogue + `digitalcommons.unf.edu/course_catalogs/` | ⚠⚠ **LEAD CHASED AND CLOSED 2026-09-15 (batch 216).** The live catalogue (`catalog.unf.edu`, `www.unf.edu/catalog/courses/`) answers with a large page but is **client-rendered** — the course index contains **no course content**. The archived-PDF lead is **REAL**: the DigitalCommons page lists catalogue PDFs by year and the article ids map cleanly (2025-26 = `article=1071`, counting down by year). ⚠⚠⚠ **But the PDF download returns 403 with or without a Referer** — bepress bot-blocks it. **So the archive exists, the ids are known, and the download is blocked. Do not re-attempt; write UNF courses from the statewide record and another carrier, and say so in the guide.** |
| **FSW** | `catalog.fsw.edu` (acalog, `catoid=27`, Course Descriptions `navoid=5491`) | ⚠ **PARTIAL BLOCK** — root returns 200 (26 KB) but **`content.php` and `search_advanced.php` both return empty 202s.** Root-reachable, content-blocked. |
| **FIU** | Coursedog API — `scratchpad/coursedog.py` | ✅ **SOLVED 2026-09-06 (batch 167). 27,923 courses, cached in `scratchpad/fiu_courses.json`.** ⚠⚠ **The gate is one header: `Referer: https://catalog.fiu.edu/`** — without it every endpoint returns `{"error":"Unauthenticated"}`. Richest Florida source: code, name, credits, college, description, cipCode, and per-component **contactHours**. ⚠ Duplicate rows per code — prefer the one with a real college name and a description. Full paging takes 2-3 min; **use the cache**. |
| **FAU** | `catalog.fau.edu` — Coursedog SPA | ❌ **ANSWERED 2026-09-07: no public Coursedog catalog at that host.** The discovery endpoint returns *"does not have entity assigned"* — the host is registered but no catalog is attached, which is why every schoolId guess failed. **Stop attempting FAU via Coursedog.** |
| **Coursedog discovery** | `app.coursedog.com/api/v1/catalogs/urls?url=<host>` (+ Referer) | ✅ **The portable bootstrap.** Returns `school` and `catalog.id` in one call — use it instead of scraping the page for ids. Works for any Coursedog school. ⚠⚠ **It still accepts `Referer` alone, but the COURSE-SEARCH endpoint no longer does** — see the row below. **Discovery succeeding tells you nothing about whether a fetch will.** |
| **⚠⚠ Coursedog auth (changed)** | `Referer:` **and** `Origin:` | ⚠⚠⚠ **CHANGED 2026-09-15 (batch 212).** Batch 167 recorded the gate as ONE header. **`Referer` alone now returns `401 Unauthorized`** on `/api/v1/cm/<school>/courses/search/$filters`; adding **`Origin: https://<catalog host>`** returns 200. Both are in the rebuilt `scratchpad/coursedog.py`. **If Coursedog 401s again, suspect another header before concluding the route is closed.** |
| **⚠⚠⚠ acalog = presumptively UNREACHABLE** | **SEVEN** institutions and counting | ⚠⚠⚠ **PLATFORM-LEVEL PATTERN, not seven coincidences (batch 215, confirmed 220).** **FSW, TSC, CF, Polk State, Santa Fe, FAMU and St. Johns River State** all serve an acalog (Modern Campus) root that answers 200 while `content.php` and `search_advanced.php` return **empty 202s**. **Treat an acalog host as content-blocked unless proven otherwise** rather than probing each school hopefully — identify the platform first, and if it is acalog, plan to write from the statewide record and another carrier. |
| **FAMU** | `catalog.famu.edu` — acalog (Modern Campus) | ⚠ **CONTENT-BLOCKED, probed 2026-09-15.** Root 200 (56 KB); `content.php` and `search_advanced.php` empty 202s. Not Coursedog (bootstrap: *"does not exists"*). ⚠⚠ **FAMU ≠ FAU** — different institutions, both unreachable for different reasons. FAMU is a main carrier of the `RET` professional sequence, so eight batch-215 guides name the gap. |
| **Polk State (PSC)** | `catalog.polk.edu` — **acalog (Modern Campus), `catoid=55`** | ⚠ **PARTIAL BLOCK, probed 2026-09-15.** Root answers 200 (53 KB) but **`content.php` and `search_advanced.php` both return empty 202s** — the same content-blocked pattern as FSW, TSC and CF. Not a Coursedog school (bootstrap: *"does not exists"*). ⚠⚠ **Note the code: `PSC` is POLK STATE. Pensacola State is `PESC`** — a previous session probed `pensacolastate.edu` as "psc" and was reading the wrong school. **Check `inst_map.json` before trusting an obvious-looking three-letter code.** |
| **USF** | `catalog.usf.edu` | ⚠ root 200 (75 KB) but **no course-description path exposed**; its only course link goes to `usf.edu/academics/courses-calendar.aspx`. Not yet a route. |
| Gulf Coast | `gulfcoast.edu/catalog/current/courses/<prefix>/index.html` | was the highest-value pattern in the DSC build; **re-probe before use** |
| **EFSC** | `catalog.easternflorida.edu/course-descriptions-information/<prefix>/` (and `/<prefix>.pdf`) | ✅ **NEW 2026-09-07 — CourseLeaf, same as UWF/FGCU/Broward/Valencia, existing tooling works unchanged.** Recovered `ADV2000C` and `COP3813C`. On CourseLeaf a prefix the college does not carry returns **202** — probe a prefix it definitely has. |
| **Tallahassee (TSC)** | `catalog.tsc.fl.edu` | ⚠ **CORRECTION: never blocked — the college RENAMED.** TCC → Tallahassee State College; `catalog.tcc.fl.edu` 000 was a dead host, not a block. New host is live (386 KB) but acalog `content.php` returns empty 202s. **Lesson: follow redirects on the main domain before recording a block.** |
| **IRSC** | `irsc.smartcatalogiq.com` | ⚠ **Live lead — SmartCatalogIQ, the same platform as the DSC build**, `/en/<year>/catalog/…`. Not yet exercised. |
| **⚠ Inventory reliability** | `courses_2plus_institutions.csv` | ⚠⚠ **The institution list is a HYPOTHESIS, not evidence — five confirmed errors in four batches** (`MUG2101`, `TPA3230C`, `BOT4404C`, `ATT1120`, `COP3014C`, all wrongly listing UWF or a suffix nobody uses). Two patterns: an institution listed that carries the subject under a **different number**, and a **suffix** in the inventory that no institution actually uses — both consistent with the file recording the SCNS catalog rather than current offerings. **Verify against a live catalog before treating an institution as a source or asserting a count in a guide.** |
| **⚠ FSU entry vs requirement text** | `registrar.fsu.edu/bulletin/...` | ⚠ A number followed by a period is **not** enough to locate a catalog entry — it also matches requirement prose (*"a grade of C or higher in COP 3014 or COP 3363."*). **Verify that a TITLE and a parenthesised credit value follow** (`COP 3014. Algorithm… (3).`). Cost a wrong result in batch 176. |
| **FSCJ** | Coursedog — `scratchpad/coursedog.py fscj` (school `fscj_peoplesoft`, catalog `sGHd4uJQXFdgDUaffhTv`) | ✅ **SOLVED 2026-09-07 (batch 173).** Was "platform unidentified". ⚠ **22,693 courses — the largest Florida catalog found so far**, and `fetch()` caps at limit=5000, so a single call silently returns a PARTIAL result. **Page it** (`scratchpad/fscj_dump.py`) and cache to `scratchpad/fscj_courses.json`. |
| **NWFSC** | Coursedog — `scratchpad/coursedog.py nwfsc` (school `nwfsc_banner_sql`, catalog `DGLrTHoh5uNIMFsdbzWf`) | ✅ **NEW 2026-09-07 (batch 173).** 1,781 courses, single page, cached in `scratchpad/nwfsc_courses.json`. Full descriptions and credits. Found because a 404 from `catalog.nwfsc.edu` returned a 1.1 MB body — **the body size was the tell.** |
| **St. Johns River State (SJRSC)** | `catalog.sjrstate.edu` — acalog (Modern Campus) | ⚠ **CONTENT-BLOCKED, probed 2026-09-15 (batch 220).** Root answers 200 (49 KB) and the markup carries 33 acalog references and 21 `content.php` links; a `content.php` probe returns an **empty 202**. ✅ **The batch-215 presumption held exactly — identifying the platform answered it in TWO requests instead of a probing session.** Carrier of `CCJ3691`, so that guide names the gap. |
| **Santa Fe** | `catalog.sfcollege.edu` | ⚠ **PLATFORM IDENTIFIED 2026-09-15 (batch 214): acalog (Modern Campus), and CONTENT-BLOCKED.** Root answers 200 (30 KB) but `content.php` and `search_advanced.php` both return **empty 202s** — the same pattern as FSW, TSC, CF and Polk State. Not Coursedog. **Root-reachable, content-blocked; treat as unavailable rather than unidentified.** |
| **UCF (confirmed route)** | Kuali — `ucf.kuali.co` | ✅✅ **RE-CONFIRMED 2026-09-15 (batch 214).** `/api/v1/catalog/public/catalogs/` → pick by `_id` (2026-27 undergraduate = `688b8960ddeb091644d2b1ca`) → `/api/v1/catalog/courses/<catalogId>` (3,676 courses) → detail at `/api/v1/catalog/course/<catalogId>/<pid>`. ⚠ **The detail endpoint needs `pid`, not `id`.** ⚠⚠ **It is the ONLY Florida source reporting laboratory hours as a structured field (`labStudioFieldWorkHours`)** — which settled whether `BOT4850` has a lab. Go here whenever a lab component is in doubt. |
| **CF (Central Florida)** | `catalog.cf.edu` | ⚠ Root 200 (26 KB), **acalog** — so likely the same content-blocked pattern as FSW and TSC. Not exercised. |
| **MDC** | `mdc.curricunet.com/catalog/iq/3279` | ⚠ CurricUNET; 200 but ~10 KB (SPA shell). Lead, not a route. |
| **State colleges (standing retry list)** | SPC, HCC, PESC, PHSC, Palm Beach State, Chipola | ❌ **curl 000 / 404.** With TSC, FSW and **Polk State** content-blocked and MDC an SPA, **this is what still blocks `MUG2101`.** ⚠ **Corrected 2026-09-15:** this row previously read "PSC", which is **Polk State's** code — Polk State is content-blocked rather than unreachable and now has its own row above. The school meant here is **Pensacola State (`PESC`)**. |
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

#### ⚠⚠⚠ It is MACHINE-READABLE — look it up, do not infer it (batch 201)

**The SCNS flat file carries per-institution designation flags for every course**, and they have been in
`scns.FIELDS` since the flat file landed:

| Field | Byte offset | Meaning |
|---|---|---|
| `gordon_rule` | 226 | Gordon Rule designated |
| `gordon_writing` | 227 | the **writing** half |
| `ge_com` / `ge_hum` / `ge_math` / `ge_nat_sci` / `ge_soc_sci` | 228–232 | general-education category |

⚠⚠ **`HIS2050` is the worked example and the first data-sourced proof of the institution-specific
rule:**

| Institution | Its title | Flags |
|---|---|---|
| FAU | Writing History | `gordon_rule`, `gordon_writing`, `ge_com` |
| FSU | The Historian's Craft | `gordon_rule`, `gordon_writing` |
| UWF | Explore History | ⚠⚠ **`ge_soc_sci` only — NO Gordon Rule** |

⚠⚠⚠ **Same number, same level, same credits, same research-writing course — and it
satisfies the WRITING requirement at two institutions and a SOCIAL SCIENCE requirement at the third.**
**State it per institution in `offering_notes`, and put the consequence in the prerequisite field**: a
student using the course to clear a requirement it is not designated for at their own institution has not
cleared it.

#### ⚠⚠⚠ The two Gordon Rule flags are populated INDEPENDENTLY and INCONSISTENTLY (corrected batch 206)

**Batch 202 read `gordon_rule` appearing WITHOUT `gordon_writing` as pointing at the MATHEMATICS half.
⚠⚠ `REL1300` refutes that**, because it shows all three combinations on one number:

| Carrier | Gordon Rule flags |
|---|---|
| Indian River State | `gordon_rule` **and** `gordon_writing` |
| Florida State | ⚠⚠ **`gordon_writing` WITHOUT `gordon_rule`** |
| UWF | none |

**The middle row cannot be reconciled with the batch-202 reading** — a course cannot be the writing half
without being Gordon Rule designated at all. **The flags are two independent institution-entered fields,
not a two-bit code.**

⚠⚠ **So the honest statement a guide should make: the flags reliably tell you that SOME designation is
recorded; they are NOT a safe guide to WHICH.** **Write "a designation is recorded — check your
institution's list for which component it satisfies" rather than inferring the component.** Four numbers
now show the divergence — `HIS2050`, `PHI4300`, `REL1300`, `REL3241`, across four disciplines — so the
institution-specific rule itself needs no further evidence; only the flag *interpretation* was wrong.

⚠ **Do not display a flag by the first letter of its key** — `gordon_rule`, `gordon_writing` and
all five `ge_*` keys begin with `g`, so a `k[0]` rendering makes them indistinguishable. Print the names.

⚠⚠⚠ **And do not test a flag for truthiness — the values are `'Y'`/`'N'` STRINGS, so `'N'` is TRUE in
Python** (batch 207):

```python
flags = [k for k in FLAG_KEYS if r.get(k)]          # ⚠⚠ WRONG — every row reads as fully designated
flags = [k for k in FLAG_KEYS if r.get(k) == 'Y']   # ✅ correct
```

**The wrong version does not error. It reports every course as carrying every designation**, confidently
and uniformly, and that goes into a guide as a false statement about the Gordon Rule. It was caught in
batch 207 only because all-seven-flags-on-every-row is implausible on its face.

⚠ **Standing check: when a flag scan returns the SAME answer for every row, assume the TEST is wrong
before assuming the DATA is uniform.**

⚠ A back-catalogue sweep is now a one-parse report rather than an open-ended task — see
`REVIEW_QUEUE.md` item 80.

⚠⚠ **UWF's catalog labels ARE Gordon Rule designations** (identified batch 179):

| UWF label | Gordon Rule component |
|---|---|
| *"Meets College-Level **Communication** Skills Requirement"* | the **writing** half |
| *"Meets College-Level **Computation** Skills Requirement"* | the **mathematics** half |

**Whenever a UWF entry carries either label, say what it is AND state the C-or-higher condition.**
⚠ Roughly a dozen already-published guides record the label without the explanation — they are
incomplete rather than wrong. A retro-sweep is a `REVIEW_QUEUE.md` candidate. It surfaced first in FSCJ's Coursedog
entry for `PHI2603`; **CourseLeaf PDFs do not carry it.**

### ⚠⚠⚠ "(GE CORE)" in the statewide TITLE — the strongest transfer fact available (batch 202)

**`CHM1020`'s statewide title is `GENERAL CHEMISTRY FOR LIBERAL STUDIES I (GE CORE)`.** ⚠⚠ **That
marker identifies a Florida General Education Core course** (s. 1007.25, F.S. — a limited approved list
across five subject areas: communication, mathematics, social sciences, humanities, natural sciences).

⚠⚠ **A core course satisfies its general-education AREA at every Florida public college and
university, and carries that status in transfer** — materially stronger than the ordinary *"guaranteed
transfer to institution offering same course"* boilerplate, which only promises credit where the same course
is offered.

- **Lead with it** where a course carries the marker. For a general-education course it is the single most
  useful fact in the guide, and no student-facing source states it plainly.
- ⚠ **The protection attaches to the AREA, not to a laboratory component or to any institutional
  designation.** Whether a programme's "science with laboratory" requirement is met is a programme rule.
- ⚠⚠ **GE Core area status is reliable; Gordon Rule and general-education CATEGORY designations
  remain institutional.** On `CHM1020`'s 27 carriers: 24 record a natural-science designation, 2 add a
  Gordon Rule designation, 1 records none.

### ⚠⚠ Two more statewide fields that are NOT boilerplate — read them (batch 202)

**`DS_Transferable1` — transferability.** Almost every course reads *"guaranteed transfer to institution
offering same course."* ⚠⚠ **`CHM1024` Chemistry Study Skills reads "NOT AUTOMATICALLY
TRANSFERABLE"** — a deliberate classification of support and study-skills coursework, not an omission.
**Where it appears, the guide must say: do not count the credit toward a requirement at another institution,
and ask an adviser how it counts toward degree progress, financial-aid satisfactory academic progress and
Florida excess hours.** ⚠ **Read the field rather than assuming the boilerplate.**

⚠⚠⚠ **Strengthened (batch 204): it is NOT a support-coursework flag.** `CHM1024` was a
1-credit study-skills corequisite, where the classification explained itself. **`PET4765` Theory and Methods
of Coaching Sports is a substantive 4000-level theory course and carries the same classification.**
⚠ **So the field must be read on EVERY course.**

⚠⚠ **And `PET4765` suggests a useful reading of what it can mean: the three carriers teach
genuinely different courses** — USF *Scientific Principles of Athletic Coaching*, UWF *Theory and
Practice of Coaching*, FSU *Principles and Problems of Coaching*. **A statewide guarantee would assert an
equivalence that does not hold, so the classification looks like a deliberate acknowledgement of divergence
rather than an oversight.** ⚠ **Where you meet it, check whether the titles diverge too — if they
do, say so in the guide and tell the reader to get a written answer from the receiving department BEFORE
taking the course.**

**`hs_credit` — dual-enrolment high-school credit.** The flat file records what a dual-enrolled
high-school student earns, and it differs within a family:

| Number | `hs_credit` |
|---|---|
| `CHM1020` | ⚠ **ELECTIVE** |
| `CHM1025` / `CHM1032` | **SCIENCE** |

⚠⚠ **So a dual-enrolled student taking `CHM1020` for a high-school SCIENCE requirement may receive
elective credit instead.** The college credit is unaffected; the high-school requirement may not be met.
**State it in guides for dual-enrolment-eligible courses, with "confirm with your counsellor and district
articulation agreement."** ⚠ **Nothing a student or parent normally reads says this.**

#### ⚠⚠⚠ COMPUTE THE FIELD'S DISTRIBUTION ACROSS THE PREFIX BEFORE TREATING IT AS A SIGNAL (batch 207)

**The same statewide field is boilerplate in one prefix and evidence in another.** Batch 207 measured it:

| Prefix | `DS_High_School_Credit1` across ACTIVE numbers | Verdict |
|---|---|---|
| `SPM` | ⚠ **184 of 184 ELECTIVE** | pure boilerplate — carries **no** information |
| `SPN` | ✅ **24 FOREIGN LANGUAGE, 178 ELECTIVE** | genuinely **discriminating** |

⚠⚠ **In `SPN` the field produced the batch's most consequential student-facing finding.** `SPN2210`
carries **ELECTIVE** while its three near-neighbours `SPN2200`, `SPN2220` and `SPN2240` — all covering
approximately the same second-year Spanish — carry **FOREIGN LANGUAGE**. ⚠⚠⚠ **Florida graduation
requirements, Bright Futures and SUS admission all expect two sequential credits in ONE world language**,
so a dual-enrolled student choosing the wrong number of four equivalent ones may not get the credit they
enrolled for.

**The rule: one `collections.Counter` over the prefix decides whether a field is worth writing about.**
A field that is uniform is a prefix-level default; a field that splits is evidence. The same test disposed
of `IN_Dual_Enrollment1` in batch 207 — `Y` on 184/184 SPM and 202/202 SPN rows, therefore meaningless.

⚠ **Say which it is in the guide.** "SCNS marks this available for dual enrolment with elective high-school
credit — and every active number in the prefix carries the identical marking, so it says nothing about this
course" is honest and useful. Presenting boilerplate as a finding is not.

##### ⚠⚠⚠ STRATIFY THE DISTRIBUTION BY COURSE LEVEL, or the test reports an ARTEFACT (batch 220)

**The `Counter` above is run over ACTIVE rows. That is not the same population as the rows you WRITE
about, and in `CCJ` the difference inverted the answer.**

`DS_Transferable1` over all **356 active** `CCJ` rows: **186 NOT AUTOMATICALLY TRANSFERABLE / 170
guaranteed** — a near 50/50 split, which by the test above reads as **strongly discriminating**, in a
prefix where the batch-202/204 rule already says to read that field on every course. **It nearly became
four guides' headline finding.**

**Cross-tabulated against `DS_Course_Intent1` it collapses:**

| Intent | GUARANTEED | NOT-AUTO |
|---|---|---|
| LOWER | 50 | 0 |
| UPPER | **119** | 2 |
| ⚠ GRADUATE | 0 | **130** |
| ⚠ VARIABLE | 0 | **54** |

⚠⚠⚠ **Of 171 active UNDERGRADUATE rows, 169 are guaranteed.** The whole split is graduate and
variable-credit rows, which are non-transferable as a class. **For the courses this project writes, the
field is boilerplate.**

**The rule, and it applies to EVERY field the distribution test is run on:**

```python
rows = [r for r in active if r['DS_Course_Intent1'] in ('LOWER', 'UPPER')]   # then Counter
```

⚠⚠ **Run the distribution over the population you are writing about — active, undergraduate,
non-shell — not over every active row.** One filter is the entire cost, and it is the difference between
a finding and an artefact. ⚠ **Keep the genuine exceptions the stratified pass surfaces**: in `CCJ` only
**`CCJ4615`** and **`CCJ4662`** are undergraduate and non-transferable, and those two DO deserve the
batch-204 treatment.

### ⚠⚠⚠ TITLE FRAGMENTATION AT SCALE — when many titles mean NO divergence (batch 202)

**`CHM1020`: 27 public carriers, 18 distinct titles**, none used by more than four — Chemistry in
Society, Chemistry in Everyday Life, Concepts in Chemistry, Discovering Chemistry, Chemical Science, General
Education Chemistry, Chemistry for the Liberal Arts, and eleven more.

⚠⚠ **And the subject does not diverge at all.** Every title names the same one-term non-majors
general-education chemistry course. **This is the opposite of every shape above, and it needs opposite
handling: REASSURE rather than warn.** The guide says so directly — *"if your catalog calls it something
this guide does not mention, it is still this course."*

⚠ **The diagnostic:** on a **high-carrier general-education** number, many titles are **branding**, not
curriculum — 27 institutions each naming the same required course. ⚠⚠ **Do not read title
variation as a divergence signal without checking the statewide DESCRIPTION and the carrier count.** The
signal is strong on a two- or three-carrier upper-division number and weak on a twenty-carrier
general-education one.

### ⚠⚠⚠ NUMBER FRAGMENTATION AT SCALE — the inverse shape (batch 207)

**Title fragmentation is one number carrying many titles. This is one SUBJECT carrying many numbers**, and
the risk it creates is the opposite one: not that a number means two things, but that **the course a
student needs exists under a number their institution does not use.**

**Second-year Spanish runs under FOUR competing statewide families**, all covering approximately the same
ground:

| Family | Statewide title | Public carriers | Credits | HS credit |
|---|---|---|---|---|
| `SPN2200`/`2201` | Intermediate Level: General Review of Basic Skills | **15** | 3 | ✅ Foreign language |
| `SPN2220`/`2221` | Intermediate Reading and Conversation | **14** | 4 | ✅ Foreign language |
| `SPN2240`/`2241` | Intermediate Conversation | **10** | 3 | ✅ Foreign language |
| ⚠ `SPN2210`/`2211` | Intermediate Conversation and Composition | ⚠ **3** | ⚠ **3 or 4** | ⚠⚠ **Elective** |

⚠⚠ **The statewide description of `SPN2210` says the series *"is equivalent to"* the `SPN2200` series — so
it is an ALTERNATIVE ROUTE through the same level, not a course that follows it.** **A student taking both
families may not earn credit for both**, and that surfaces at transfer evaluation, late and expensively.
**Where a statewide description says a series is equivalent to another series, say so in the guide and tell
the reader to ask an adviser before enrolling in the second.**

⚠ **Quantify the prefix before writing — it sets the hedging level honestly rather than by feel.**

#### ⚠⚠⚠ THE SINGLE-CARRIER BASELINE — a measured property of the Florida catalog (batches 207-210)

**Thirteen prefixes measured across four batches. Every one lands between 64% and 85%:**

| Prefix | Live ids | Single-carrier | Prefix | Live ids | Single-carrier |
|---|---|---|---|---|---|
| `SPM` | 189 | 145 (77%) | `TPA` | 414 | 324 (78%) |
| `SPN` | 241 | 166 (69%) | `TRA` | 79 | 62 (78%) |
| `SSE` | 145 | 123 (85%) | `ACG` | 346 | 227 (66%) |
| `SYO` | 124 | 97 (78%) | `ADV` | 133 | 109 (82%) |
| `SYP` | 165 | 140 (85%) | `AFR` | 76 | 49 (64%) |
| `AMH` | 330 | 240 (73%) | `APK` | 238 | 183 (77%) |
| `ARH` | **421** | 339 (81%) | | | |

⚠⚠⚠ **Roughly three-quarters of all Florida course identifiers are carried by exactly ONE public
institution.** **So a course transferring cleanly by number is the EXCEPTION across the catalog, not a
feature of unlucky prefixes** — and the honest default hedging level for almost any course is higher than
"two or three institutions agree" suggests.

**Two consequences for writing:**

1. **Do not treat a two- or three-carrier course as unusual.** It is the norm. Write the
   single-institution or few-institution treatment without apology, and say plainly that the reader
   should plan on sending syllabi rather than relying on the number.
2. ⚠ **The baseline coexists with a small number of very widely carried courses** — `ACG` reaches 37
   carriers, `AMH` 36, `ARH` and `SPN` around 30, all on lower-division general-education numbers.
   **Those are the ones where title variation is branding rather than divergence** (see TITLE
   FRAGMENTATION AT SCALE). **Check the carrier count before deciding which kind of course you are
   writing.**

**It is one flat-file pass to compute, and it is worth doing before drafting.**

### ⚠⚠⚠ TITLE-versus-DESCRIPTION divergence — inside ONE statewide record (batch 207)

**Every other divergence in this file runs between two records** — institution against institution, or
institution against the statewide title. ⚠⚠ **This one is internal: the state's own title and the state's
own description contradict each other.**

| `SPM3104` statewide title | `SPM3104` statewide description |
|---|---|
| SPORT FACILITY **AND EVENT** MANAGEMENT | *"planning, design, and management &hellip; maintenance, security, operations, and evaluation"* — ⚠ **events never mentioned** |

**The institutions side with the description:** EFSC *Sports Facilities Management* and UWF *Sport Facility
Planning and Management* both drop "event"; UNF's "Entertainment" names a venue type, not the discipline.
⚠⚠⚠ **And the missing half is not housed elsewhere — `SPM4109` *Sport Event Management* and `SPM4140`
*Esports Event Management* have NO Florida public carrier at all.**

**The consequence is a real student-facing finding, not a cataloguing curiosity: event operations is the
least reliably covered part of the subject the degree title implies, and it is where a large share of
graduates actually start work.** The guide says so and tells the reader to close the gap deliberately.

⚠ **The drill: when a statewide title contains a conjunction ("X and Y"), check that the statewide
DESCRIPTION delivers both halves, and check whether Y has its own number that nobody carries.**

#### ⚠⚠⚠ Check whether the carriers diverge in the SAME direction or OPPOSITE ones (batch 210)

**Before writing a single divergence block, ask which way each carrier departs from the statewide scope.
The two cases need completely different handling.**

| | Carriers diverge the SAME way | Carriers diverge OPPOSITE ways |
|---|---|---|
| Example | **`SPN4520`** — state says *Spanish America*, all three carriers say *Latin American* | **`ARH3301`** — state says Renaissance **+ Mannerism**, Italy **+ North**; ⚠ FGCU adds the **Baroque** (broader), ⚠ UWF restricts to the **Early** Renaissance (narrower) |
| What it means | ⚠ **the STATE record is out of step** with current practice | ⚠ **the carriers are making independent curricular choices** |
| Handling | correct toward the carriers; explain the state's term | ⚠⚠ **give the reader a TEST, not a correction** — neither carrier is wrong |

⚠⚠⚠ **The opposite-direction case has a consequence worth stating explicitly in the guide: with only two
carriers diverging in opposite directions, the two versions may overlap only in the MIDDLE of the
subject.** On `ARH3301` one adds a century at the end and the other may stop before the High Renaissance —
so a student could take either and miss what most people mean by the course's own title.

**Handling that works: two concrete syllabus questions rather than a general warning.** For `ARH3301`:
*does it reach the High Renaissance and Mannerism?* and *does it cover Northern Europe, or Italy only?*
⚠ The second matters because **the statewide description requires both halves and a course titled simply
"Renaissance Art" frequently means Italian Renaissance art** — which Florida numbers separately as
`ARH3302`.

#### ⚠⚠⚠ THE TITLE/DESCRIPTION TEST — run it before looking at carriers (batch 208)

**Batch 208 produced a second and a third instance, and together they turn a judgement call into a test.**
Both fields are in the same statewide CSV row, so this costs nothing:

| Case | Statewide title vs statewide DESCRIPTION | Carriers | Conclusion |
|---|---|---|---|
| **`TPA3223C`** | ✅ **agree** — both say lighting *technology* | 2 of 3 say *design* | ⚠ **the CARRIERS are misfiling** |
| **`TRA3153`** | ❌ **disagree** — title says *"Applied Production/Operations Mgmt"*, description is entirely *transportation* | both agree with the description | ⚠ **the TITLE is stale** |
| **`SPM3104`** | ❌ **disagree** — title promises *events*, description omits them | carriers side with the description | ⚠ **the TITLE is stale** |

⚠⚠ **The rule: compare the statewide title with the statewide DESCRIPTION first.**

- **They AGREE** → the state is the reference, and a deviating carrier is **misfiling**. Write the
  statewide subject, label the misfiling, and check whether a dedicated number exists for what the carrier
  actually teaches (it usually does — see the MISFILING section).
- **They DISAGREE** → the **title is the stale element**, and the description plus the carriers settle it.
  ⚠ **`TRA3153` is the first time this catalog has corrected a statewide title outright**, and it was
  safe because four independent things pointed the same way: the description, both carriers, and the
  prefix itself (`TRA` = transportation; production/operations management is numbered under `MAN`).

⚠ **This REFINES rather than contradicts the batch-201 caution** ("do not correct a *described* statewide
subject on agreeing titles alone"). That caution protects a statewide **description** from being overridden
by titles. **Here the description is not being overridden — it is the evidence**, against a title it
already contradicts.

#### ⚠⚠⚠ CORRECTED (batch 215): when they disagree, THE CARRIERS decide which element is stale

**The rule above said "they DISAGREE → the title is the stale element." That was true of the cases in hand
and is NOT a general property of titles.** `RET4277` is the counterexample:

| Source | Says |
|---|---|
| Statewide **title** | *Adult Critical Care* |
| ⚠ Statewide **description** | a survey of *"the different specialty areas available in respiratory therapy"* — **not critical care** |
| UWF | Critical Care Management — **critical care** |
| Seminole State | Adult Critical Care — **critical care** |

⚠⚠⚠ **Title and description disagree, and BOTH CARRIERS SIDE WITH THE TITLE — so here the DESCRIPTION is
the stale element.** Three of four sources agree against it.

**So the test has three outcomes, not two:**

1. **Title and description AGREE** → the state is the reference; a deviating carrier is **misfiling**
   (`TPA3223C`).
2. **They DISAGREE and the carriers back the description** → the **TITLE** is stale (`TRA3153`, `SPM3104`).
3. ⚠ **They DISAGREE and the carriers back the title** → the **DESCRIPTION** is stale (`RET4277`).
4. ⚠⚠⚠ **They DISAGREE and the CARRIERS SPLIT, one on each side** → **the test returns NO ANSWER, and the
   number is carrying TWO SUBJECTS** (`HFT4252`, batch 218).

⚠⚠ **Always check which element the CARRIERS agree with before deciding.** Never assume the title is the
stale half just because it usually has been.

**Branch 4 handling — `HFT4252` is the worked case.** Statewide title *Employees Wellbeing in Hospitality
and Tourism*; statewide description entirely *hotel and resort management*; **UCF backs the title, Pensacola
State backs the description.** ⚠ Both subjects were **numbered elsewhere in the prefix** (`HFT2014`,
`HFT4793` for wellbeing; `HFT2250`, `HFT2276` for hotel/resort), so neither carrier needed this number.
**Published as ONE guide covering BOTH readings, each labelled, with a two-column syllabus diagnostic and
an explicit warning that the course number does not identify the subject** — the `CLP4302`/`APK4200`
precedent. ⚠ **A full split was not sound because one carrier's catalogue is unreachable, and a `-INST`
half cannot be written from a title alone.**

### ⚠⚠⚠ FOUR subjects on one number — pull it, do not write it (batch 218)

**`HFT3271` is the most severe collision found to date and it is the pattern for when to STOP.**

| Source | Subject |
|---|---|
| statewide title **and** description | **Condo/Resort Management** |
| FIU | Nightclub Management |
| FGCU | Club Management |
| UWF | Spa Management |

⚠⚠⚠ **Four subjects, and NO carrier teaches the statewide one.** Writing the statewide subject would
describe a course nobody teaches; writing any carrier's would misdescribe it for the other two.

⚠ **The misfiling diagnostic fires on all three carriers**: Florida numbers spa (`HFT2204`, `HFT2209`),
club (`HFT2100`, `HFT4434`) and condo/resort (`HFT2273`, `HFT2276`, `HFT2278`) **separately**.

**Rule: where a number carries FOUR readings, or where NO carrier teaches the statewide subject, PULL it to
`REVIEW_QUEUE` rather than writing.** Precedents: `TPA3230C` (three subjects, pulled), `HFT3271` (four,
pulled). **A disambiguation page at the bare number is the likely resolution, but that is Ron's call.**

#### ⚠⚠ The same one-row check settles a narrow-looking title (batch 208)

**`SYO4530`**: statewide *Social Stratification*; FIU *Social Inequalities*, UF *Social Inequality*,
UWF ⚠ *Inequality in America*. The instinct is to flag UWF as narrowing. ⚠⚠ **But the statewide
description already says "American society (primarily)" — so UWF's title is simply ACCURATE, and the two
broader-sounding titles are the ones that may promise comparative material the course does not deliver.**

⚠ **Drill: before flagging a narrow title as a narrowing, check whether the DESCRIPTION was already that
narrow.** This inverts the usual reading often enough to be worth the one lookup.

#### ⚠⚠ A statewide description with an embedded institution list or a YEAR is a historical record (batch 208)

**`SSE4113`'s description ends *"INSTITUTIONS: FAMU, FAU, FSU, UWF 1988"*; `SYO4530`'s ends with nine
institutions and *"6/83"*.** In both cases the list no longer matches who offers the course.

⚠⚠ **Read those descriptions as a historical definition of the SUBJECT, not a current statement of
practice, and say so in the guide.** **Parts of the state course file have not been revised in forty
years** — which also means the statewide record is sometimes the *least* current source available, and
cannot be used to check a carrier's currency (see `SYP3630` under terminology-era divergence).

#### ⚠⚠ Read the description's PROSE REGISTER — it dates the entry when no date is stamped (batch 210)

**The state course file contains entries from at least two eras, and they are distinguishable by style
alone.** Compare, both in `AMH`:

| Era | Example | Style |
|---|---|---|
| 1980s | `AMH4110` | *"DISCOVERY, EXPLORATION, ORIGINS OF COLONIES. DEMOGRAPHIC TRENDS, ETHNO-CULTURAL CONFLICT…"* — terse all-capitals telegraphese |
| Recent | `AMH4641` | *"This course surveys… **This is no trivial subject.** … In this course, **we'll** examine… **We'll** learn how to critically analyze…"* — full sentences, first person plural, an argument |

⚠⚠ **Where a statewide description reads as though it was written by someone who teaches the course, it
usually was — and it is MORE reliable than the older entries.** That inverts the usual assumption in this
file, where the statewide record has repeatedly been the stale element (`AFR2132`'s *"projects ahead to
the year 2000"*, `ACG4151` dated 11/82, `SSE4113` dated 1988, `SYO4530` dated 1983).

**Practical use: read the register before deciding how much weight to give the description.** A recent,
argued entry can be quoted to the student as a description of the actual course; a 1980s entry should be
framed as a historical definition of the subject. ⚠ **It costs nothing and it is available on every
course.**

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
3. ⚠⚠ **Check BOTH public queues first, every session** (Ron's standing order, 2026-09-11:
   *"each session we will check resources and guide queue requests and then start on any courses
   in the queue"*):

   ```bash
   curl -s "https://floridacourserepo.com/api/v1/queue/resources?status=pending"   # resources
   curl -s "https://floridacourserepo.com/api/v1/queue/guides?status=waiting"      # guide requests
   ```

   **Resource suggestions are cleared first** — they are quick, a person is waiting on each one, and
   the rules are in `resources/APPROVAL_RULES.md` (the `/resources` skill drives the loop). **Then
   guide requests**, which outrank the local queue. **Only then** work `queue.csv`.

   ⚠ **A guide request closes itself when the guide publishes** — no manual step. Verify by
   re-reading the queue after a push.

   ⚠ **Two requests in a row (`CET1112`, `CET2127C`) landed on numbers with a divergence.** A request
   appears to be a signal that the number confuses people, so **check the number's whole family
   before writing** — the bare/`C` pair, the level twin, and what other institutions call it.
4. ⚠⚠⚠ **CHECK FOR AN EXISTING LIVE GUIDE ON EVERY COURSE IN THE BATCH, not only the
   requested ones** (learned the hard way, batch 202 — `CHM1020C` already had a guide published
   2026-05-04 and was rewritten unknowingly):

   ```bash
   for c in ID1 ID2 ID3; do printf "%-9s " $c; \
     curl -s "https://floridacourserepo.com/api/v1/courses/$c/guide" | head -c 120; echo; done
   ```

   ⚠ **A request's `hasGuide: false` covers only that course.** When a batch is extended into a
   number's family — which the "check the whole family" drill encourages — **the added members have
   not been checked.** If a guide exists, decide deliberately whether to replace it (bump `version`, and
   see `REVIEW_QUEUE.md` item 81) or to skip the number.

   ⚠⚠ **And read `mkguide.py`'s PER-COURSE output, treating a missing line as a failure.**
   `validate_drafts.py` validates **what is on disk, not what you just built** — so a failed assembly
   plus an older draft file produces a clean validation of the *wrong file*. That is exactly how the
   batch-202 miss stayed invisible: five new drafts and one stale one reported as "6 clean".

5. Run `python queue_mgr.py status` to see where things stand. `queue.csv` is the
   authoritative work queue; for prefix completion the live catalog is now the better worklist:
   `curl -s "https://floridacourserepo.com/api/v1/courses/catalog?prefix=<PFX>&hasGuide=false&pageSize=1000"`.
   `courses_2plus_institutions.csv` is the old ≥2-institution inventory; the SCNS flat file is authoritative.
6. Run `python validate_drafts.py --quiet` if the queue shows `error` rows, to see what is
   blocking them.
7. Confirm with the user what they want to work on before generating anything.

Pushing to the live site runs from this repo (`generate_guide.py --push-from-queue`), using
the `REPO_ADMIN_*` credentials in `Tools/.env`. It is a write to production — confirm the
batch with the user before pushing, and never push a draft that `validate_drafts.py` fails.

### ⚠⚠⚠ When a push is INTERRUPTED — the recovery drill (batch 211)

**Batch 211's push was killed mid-run by system memory pressure.** ⚠⚠ **A killed push can leave a PARTIAL
state — some guides live, some not, and the queue half-marked — so the state must be CHECKED, never
assumed.**

**The drill, in order:**

1. ⚠ **Ask the SITE what is live**, not the queue:
   ```bash
   for c in ID1 ID2 ID3; do printf "%-9s " $c; \
     curl -s "https://floridacourserepo.com/api/v1/courses/$c/guide" | head -c 80; echo; done
   ```
2. **Then ask the QUEUE what it believes** — `python queue_mgr.py status`. **Where the two disagree, the
   site is the fact and the queue is the record to fix** (`queue_mgr.py reconcile`).
3. **Only then re-run** — and **split reconcile from push**: reconcile is fast, the push is the slow half,
   so running them as separate commands makes the failure point obvious instead of ambiguous.

✅ **The guide upsert is idempotent, so re-pushing an already-live guide is safe.** **Knowing the state
first is what tells you whether to expect a version bump and whether anything needs one.**

### ⚠⚠ Run long pipeline commands with `python -u`

**The killed push looked exactly like a slow push for several minutes, because the background output file
stayed EMPTY — Python buffers stdout when it is redirected to a file.**

⚠⚠⚠ **An empty output file is indistinguishable from a hung process, a slow process and a dead one.**

**Use `python -u` on anything that may run long** — the metadata build, `generate_guide.py`,
`list_courses.py`. Unbuffered output makes progress visible and makes a kill obvious immediately.

⚠ **Expect long runs on large prefixes.** The SCNS flat file is ~80 MB and is parsed once per prefix, so a
big prefix (`ARH` is the largest measured at 421 live ids) will push the metadata build and the push past
the two-minute tool timeout. **Give them explicit long timeouts rather than letting them background
silently.**

---

## Tone and quality bar

- Write in the voice of a thoughtful curriculum developer who knows Florida community colleges, not a generic AI summarizer.
- Specific beats generic. "Hibbeler is the most widely adopted text" beats "common textbooks are available." Named employers, named cities, named programs beat vague gestures.
- Honest hedging beats false confidence. "Varies by institution" is acceptable when true; making up a uniform standard is not.
- The user reviews each batch carefully — they are eager to see the guides. Earn that attention with substance.
