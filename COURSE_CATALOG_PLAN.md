# Course catalog, guide requests & course resources — implementation plan

**Status:** plan written 2026-09-11 (Ron's decisions in §1). Nothing built yet.
**Ask (Ron, 2026-09-11):** list every course that exists, not only the ones with a guide. Guides are
generated **on request**. Each course row carries two buttons — **Course Resources** and **View Guide** /
**Request Guide**. Requests and resource submissions go into **public queues** that the AI sessions work.
The main page offers **Courses** (default) · **Programs** (coming soon) · **Career Paths** (coming soon).

**Division of work — two sessions, one contract:**

| Session | Controlling file | Owns |
|---|---|---|
| **Site session** (repo root) | `CLAUDE.md`, this plan | server code: data model, API, pages, deploys |
| **Content session** (`Tools/`) | `Tools/CLAUDE.md` | **adding courses (with or without a guide) by rules Ron gives it**, writing guides by priority, reviewing resources |

The site does not decide which courses exist; it **accepts base course data over the API** and displays it.
The contract between the two is §6 and will be written up for the content session as `Tools/COURSE_API.md`.

---

## 1. Decisions (Ron, 2026-09-11)

| Decision | Choice |
|---|---|
| What counts as a course | A course with a **verified offering at a school** and a prefix / number / title. Verification source: SCNS (the flat file from `Tools/scratchpad/scns.py flatfile` is the authoritative per-institution list; `courses_2plus_institutions.csv` is not — see `Tools/SOURCES.md` Tier 3). |
| Scope of courses to add | **Everything in SCNS** — all levels, including 0xxx vocational and graduate. Applied as rules by the content session, not hard-coded in the site. |
| Who adds courses | **The `Tools/` session**, over the API, with or without a guide. |
| Request Guide button | **One click records the request** (the course and its schools are already known). Anonymous, no email: the confirmation says to check back — the site is updated weekly. |
| Pending resources in the public queue | **Visible but not clickable** until approved. |
| Programs / Career Paths | **"Coming soon" pages** in this release. Career Paths is built afterwards from `CAREER_PATHS_PLAN.md`. |

---

## 2. What exists today (survey 2026-09-11)

- **A course only exists once a guide is pushed.** `taxonomy.json` holds nodes but **no courses**;
  `PUT /api/v1/courses/{id}/guide` creates the `TaxonomyCourse` as a side effect, with
  `Title = CourseId` as a placeholder. **There is no way to create a course without a guide.**
- `TaxonomyCourse` = `CourseId`, `Level3Key`, `Title`, `CreditHours`, `IsActive`, `CurriculumGuideUrl`.
  **No record of which schools offer a course** — that data lives only in `Tools/`.
- **Every SCNS prefix already has a taxonomy leaf** (604 leaf keys cover every prefix in the inventory CSV),
  so placement by prefix (`ExtractCoursePrefix`) will resolve for imported courses.
- **Guide requests are half-built** (backlog item 4, 2026-09-03): `GuideRequest` entity, `/request-guide`
  form (school **required**), `/admin/guide-requests` ranking, `GuideRequestService` (hashed IP,
  5/IP/hour, per-day dedupe, refuses when a guide exists, `ClosePublishedAsync`), and
  `queue_mgr.py import-requests` (priority `500 − 10 × count`). **The list endpoint is admin-only** and
  there is no public queue page.
- `Browse/Level3` lists every `IsActive` course in a leaf as a whole-row link; the course page already shows
  "Request a Curriculum Guide" when no guide exists.
- Discipline/leaf counts (`TaxonomyService`) and the **uncommitted** header strip (`SiteStatsService`,
  "Materials for N courses available") count only courses **with a guide or published module**.
- `StaticSiteExporter` can optionally export *every* taxonomy course — with tens of thousands of
  guide-less courses that option becomes impractical.
- `CAREER_PATHS_PLAN.md` §4 plans `Institution` + `CourseOffering` seeded from the inventory CSV. **This plan
  builds those tables first, fed by the API instead** (§4), and career paths reuses them.

---

## 3. Principles

1. **The site stores base course data; the content session decides what is a course.** No SCNS parsing,
   no scope rules, no shell-number logic on the server beyond display.
2. **A course without a guide is a first-class page**, not an error state: title, credits, where it is
   offered, resources, and a one-click request.
3. **Never lose data by accident.** Titles are corrected by continuous site reviews, so the course `PUT`
   writes the title it is sent — but a guide push never resets a real title to the `CourseId` placeholder,
   and nothing deletes a course that has a guide, modules, requests or resources.
4. **Public queues expose no personal data** — no emails, reasons, IP hashes or user ids.
5. **The server never fetches a submitted URL.** Resource checking happens in the AI session, off-server
   (no SSRF surface, no server-side crawling).
6. **Everything the AI sessions do goes through the REST API** with the existing admin JWT
   (`REPO_ADMIN_*` in `Tools/.env`) — no direct DB access, no redeploy to publish content.

---

## 4. Data model (one migration per phase)

### Phase 1 — `AddCourseCatalog`

**`TaxonomyCourse`** (existing) — add:

| Column | Type | Notes |
|---|---|---|
| `StateTitle` | string? | SCNS statewide title, as supplied |
| `ContactHours` | int? | clock hours where that is the real measure (PSAV) |
| `OfferingCount` | int | denormalised count of active offerings — list sorting and "N schools" without a join |
| `CreatedUtc`, `UpdatedUtc` | DateTime | |
| `Source` | enum `CourseSource` | `Guide` (created by a guide push — all existing rows) · `Catalog` (created by the course API) |

`Title` becomes a real title for catalog-created courses. The guide push keeps creating courses exactly as
today (backwards compatible) — but a later course upsert **replaces the `Title = CourseId` placeholder**.

**`Institution`** (new) — `Code` PK (≤10, uppercase, e.g. `UCF`), `Name` string?, `Sector` string?
(FCS / SUS / private / other), `ScnsId` string?. Matches `CAREER_PATHS_PLAN.md` §4, with names now filled
(SCNS `institution_map()` supplies code → name).

**`CourseOffering`** (new) — `CourseId` + `InstitutionCode` composite PK; `InstitutionTitle` string?
(what *that* school calls it — the divergence signal), `Credits` decimal?, `ClockHours` int?,
`IsActive` bool, `UpdatedUtc`.

### Phase 2 — `GuideRequestsOneClick`

**`GuideRequest`** — `Institution` becomes optional (empty for one-click requests on known courses);
add `Channel` enum (`Button` / `Form` / `Api`).

### Phase 3 — `AddCourseResources`

**`CourseResource`** (new):

| Column | Type | Notes |
|---|---|---|
| `Id` | Guid PK | |
| `CourseId` | string FK | |
| `Type` | enum `ResourceType` | `Website` · `YouTube` (extensible) |
| `Url` | string ≤2048 | normalised (scheme+host lowercased, fragment and tracking params stripped) |
| `YouTubeVideoId` | string? | parsed from `watch?v=`, `youtu.be/`, `/shorts/`, `/embed/` |
| `Description` | string? ≤500 | submitter's, optional |
| `Title` | string? ≤200 | **set by the reviewing AI** from the page / video title on approval |
| `Status` | enum | `Pending` · `Approved` · `Rejected` · `Removed` |
| `DecisionNote` | string? ≤300 | short, **public-safe** reason shown in the queue |
| `SubmittedUtc`, `DecidedUtc` | DateTime | |
| `SubmitterIpHash`, `SubmitterUserId` | string? | same salted-hash treatment as `ContentFlag` |

Unique index on (`CourseId`, `Url`) — the same link suggested twice is one row.

### Phase 5 — `AddPrograms` (sketch; confirm against Ron's programme rules before building)

**`Program`** — `Slug` PK (`dsc-as-nursing`), `InstitutionCode` FK, `Name`, `Credential` (A.A. / A.S. /
A.A.S. / B.S. / B.A. / B.A.S. / certificate / PSAV), `CipCode`?, `TotalCredits`?, `CatalogYear`,
`CatalogUrl`, `DescriptionHtml` (sanitised), `Status` (Draft / Published), `UpdatedUtc`.

**`ProgramCourse`** — `ProgramSlug` + `CourseId` + `Block` (requirement block name: "General education",
"Core", "Clinical"…), `Role` (required / elective / choice), `ChoiceGroup`?, `Sequence`?, `Note`? — the same
block-and-course shape as a career path's stages, so career paths can link programmes directly.

---

## 5. Public site

### Main page (Phase 2)

Three large options at the top of `/`: **Courses** (selected; today's search + disciplines below),
**Programs** → `/programs`, **Career Paths** → `/careers`. The two new routes are short "coming soon"
pages saying what is planned (Career Paths text drawn from `CAREER_PATHS_PLAN.md`). The same three appear in
the navbar. `/careers` is the route the career-paths build will take over.

### Course rows — every list of courses (Phase 1 layout, Phase 2/3 buttons)

```
EEE3300   Electronics I          3 cr · 7 schools     [Course Resources (2)]  [View Guide]
EEE3396C  Solid State Devices    3 cr · 1 school      [Course Resources]      [Request Guide · 3]
```

- Course id + title link to `/courses/{id}`; the row is no longer one big link (two buttons live in it).
- **Left button: Course Resources** → `/courses/{id}/resources`, with the approved count when > 0.
- **Right button: View Guide** when a guide exists; otherwise **Request Guide** — one click, count shown
  once anyone has asked; becomes **Requested ✓** for the person who clicked, with *"Guides are added as
  they are requested and the site is updated weekly — check back."*
- Leaf pages get a filter: **All · With guide · Without guide** (default All), and show
  "N courses · M guides".
- Stacks to two lines on phones; buttons stay full-size tap targets.

### Course page `/courses/{id}` (Phase 1)

Title, credits / contact hours, **Offered at** (institution codes with names on hover; first 5 then
"+N more" — the career-paths convention), and a note where an institution's title differs from the
statewide one. Guide + request buttons as in the row. **Modules** section only when modules exist.

### Resources page `/courses/{id}/resources` (Phase 3)

Approved resources: websites as title · domain · description (`rel="nofollow ugc noopener noreferrer"`,
new tab); YouTube as a thumbnail that loads a `youtube-nocookie.com` player on click. **At the bottom:
"Suggest a resource"** — URL (required), description (optional), honeypot field, antiforgery token →
"Thanks — it's in the public review queue" with a link to it.

### Public queues (Phase 2 guides, Phase 3 resources)

| Page | Shows |
|---|---|
| `/queue/guides` | Requested courses ranked by requests: course, title, request count, first / latest request, status (Open · Queued · Published · Declined), link to the guide once published |
| `/queue/resources` | Pending: course, type, **domain or YouTube title as plain text (not a link)**, description, submitted date. Plus decisions from the last 30 days with the public-safe note |

### Counts, header, search, export

- Browse and front-page counts become **"N courses · M guides"**; the header strip (uncommitted
  `SiteStatsService` work) changes to the same wording.
- Site search matches catalog-only courses by id and title.
- Static export keeps exporting only courses **with a guide, modules or approved resources**; resource
  pages export read-only; queue pages are not exported.
- **SEO:** course pages with no guide, modules or approved resources get `noindex,follow` until they do —
  tens of thousands of near-empty pages would otherwise read as thin content across the whole site.

---

## 6. API — the contract with the `Tools/` session

Envelope, FluentValidation and error codes as everywhere (`ErrorCodes.cs`, API spec).

### Phase 1 — courses and institutions (AdminOnly)

| Verb | Route | Purpose |
|---|---|---|
| PUT | `/api/v1/courses/{courseId}` | Upsert base data: `title`, `stateTitle?`, `creditHours?`, `contactHours?`, `taxonomyKey?` (else by prefix, as the guide push does), `isActive?`, `offerings?: [{institution, title?, credits?, clockHours?, isActive?}]`, `replaceOfferings` (default true). Returns `created` / `updated` / `unchanged` and the resolved taxonomy key. |
| POST | `/api/v1/courses/batch` | Up to **500** of the above per call; per-item results so one bad row does not fail the batch. |
| DELETE | `/api/v1/courses/{courseId}` | Only when the course has **no guide, modules, requests or resources**; otherwise 409 (use `isActive: false`). |
| PUT | `/api/v1/institutions/{code}` · POST `/api/v1/institutions/batch` | Code, name, sector. Offerings to an unknown code create a code-only institution. |
| GET | `/api/v1/courses?hasGuide=false&prefix=EEE&active=true&updatedSince=…` | Extends the existing list so the content session can reconcile what the site already holds. |

**Rules the server enforces:** course id `^[A-Z]{3}\d{4}[A-Z]?(-(SCNS|[A-Z]{2,5}))?$`; title ≤300; a title
equal to the course id is never written over a real title; `isActive:false` hides a course **only if it
has no guide** (courses with guides stay visible). The existing guide `PUT` is unchanged.

### Phase 2 — guide requests

| Verb | Route | Auth | Purpose |
|---|---|---|---|
| POST | `/api/v1/guide-requests` | public | existing; `institution` now optional |
| GET | `/api/v1/queue/guides?status=open` | **public** | the ranked queue, no personal data — what the content session reads to choose guides |
| GET / PATCH | `/api/v1/guide-requests…` | Admin | existing ranking with detail, and status triage |

### Phase 3 — resources

| Verb | Route | Auth | Purpose |
|---|---|---|---|
| GET | `/api/v1/courses/{id}/resources` | public | approved resources |
| POST | `/api/v1/courses/{id}/resources` | public | submit `{url, description?}` (rate-limited) |
| GET | `/api/v1/queue/resources?status=pending` | public | the review queue |
| PATCH | `/api/v1/resources/{id}` | Admin | `{status: approved\|rejected\|removed, title?, decisionNote?}` — what the reviewing AI calls |

---

## 7. AI sessions

**Guide generation (content session, `Tools/`).** Priority becomes: **requested courses first** (by count,
from `/api/v1/queue/guides`), then Ron's standing rules (engineering first, complete the prefix).
`queue_mgr.py import-requests` already exists; it gains the public endpoint and the course-add step.
Updating `Tools/CLAUDE.md` and `Generate_Guides_and_Push_Process.md` is the content session's job, from
Ron's rules plus `Tools/COURSE_API.md`.

**Resource review (Phase 4).** A small client `Tools/resources/review_resources.py` (`list` / `approve` /
`reject`), a rubric `Tools/resources/REVIEW_GUIDE.md`, and a `/resources` skill. The session fetches each
pending URL and approves only when it is **reachable**, **relevant to that course** (checked against the
course title and guide), **educational rather than promotional**, **free to view** (or plainly marked if
not), and **safe** (no malware, adult, gambling or scam signals). YouTube: the video exists, is embeddable,
and is on topic. It sets a clean `Title`, and a short public-safe `decisionNote` on rejection.
`/admin/resources` lets Ron reverse any decision.

---

## 8. Abuse & security

- **Resource submissions:** 10 per IP per hour; per-course dedupe on the normalised URL; `http`/`https`
  only; reject IP-literal, `localhost` and non-public hosts at submit; honeypot + antiforgery on the form.
- **Request button:** raise the per-IP limit for `Button` requests to 20/hour (clicking through a subject
  page should not trip the 5/hour form limit); per-day dedupe stays.
- Pending URLs rendered as escaped plain text; approved links `nofollow ugc`.
- YouTube via `youtube-nocookie.com`, click-to-load (no third-party requests until the visitor asks).
- Queue descriptions are user text: escaped, truncated, and removable by the reviewer.

## 9. Performance

`TaxonomyCourses` grows from ~2,200 to potentially tens of thousands. Indexes on `Level3Key`, `IsActive`,
`CourseOffering.CourseId`, `CourseResource(CourseId, Status)`. Cache the tree counts
(`GetFullTreeAsync` recomputes them per request today) the same way `SiteStatsService` does. Batch API
writes in one transaction per call. Production is SQLite — time a 500-row batch locally before the content
session runs thousands.

---

## 10. Phases (each ends with something Ron can open in a browser)

| Phase | Builds | Hand-test | Deploy |
|---|---|---|---|
| **1 — Courses without guides** | Migration `AddCourseCatalog`; course / batch / institution / delete APIs; list filters; course page (offered-at, no-guide state); Level3 row layout + with/without-guide filter; "N courses · M guides" counts + header wording (folds in the uncommitted `SiteStatsService` work); search; `noindex`; export rule; **`Tools/COURSE_API.md`** for the content session | push ~20 guide-less courses with offerings via a scratch script; browse a leaf, filter, open a course page; existing guide pages unchanged | **Deploy 1** (migration) → **unblocks the content session** to start adding courses |
| **2 — Requests + main page** | One-click Request Guide (fetch + no-JS fallback, count, "Requested ✓ — updated weekly, check back"); email field removed from `/request-guide` (kept for courses not yet listed); `Channel` + optional institution; `/queue/guides` + public queue API; Courses / Programs / Career Paths options, `/programs` + `/careers` coming-soon pages, navbar | click Request on 3 courses → counts update, rows appear in `/queue/guides`, admin ranking agrees; home page options work at phone width | **Deploy 2** |
| **3 — Course Resources** | `CourseResource` + migration; resources page with submit form; Resources button + count on rows and course page; `/queue/resources`; resource API; `/admin/resources`; rate limits | submit a website and a YouTube link → pending in the queue, not clickable; approve via API → live on the page with player; reject shows note | **Deploy 3** |
| **4 — AI review loop** | `Tools/resources/` client + rubric + `/resources` skill; request-first notes for the content session | run `/resources` against local pending items end to end | none (tooling) |
| **5 — Programs interface** | `Program` + `ProgramCourse` + migration (§4); admin program API (upsert, batch); public `/programs` (by school and credential) and `/programs/{slug}` (requirement blocks, course rows with guide/request + resources buttons); course-page "Required in these programs"; `Tools/PROGRAM_API.md`. **Content comes from the schools' catalogs via the `Tools/` session, by Ron's rules** — the site only provides the interface. | push one programme from a scratch JSON; open it; course rows link through | **Deploy 5** |
| **Later** | **Career Paths** per `CAREER_PATHS_PLAN.md` — its "Schools" data now exists (phase 1) and it can link the programmes that feed each path (phase 5) | | |

Rough size: phases 1 and 3 about one session each; 2 under a session; 4 half a session.
Each migration phase: `PENDING_SERVER_CHANGES.md` entry, deploy **without** `-SkipMigrations`.

---

## 11. Defaults taken — say if any is wrong

1. **Shell numbers** (x9xx: special topics, internship, thesis…) are listed like any course, but show
   *"Topics vary by term — no guide"* instead of Request Guide. (The alternative: show the button and let
   the content session decline those requests publicly.)
2. **Titles** display in title case from the SCNS upper-case source; a published guide's title wins.
3. Resource submitters are **anonymous** (no account), rate-limited, IP hashed.
4. The public resource queue shows **30 days** of decisions with the short note.
5. Guide-less course pages are **`noindex`** until they have a guide, modules or approved resource.
6. The `/request-guide` form stays for courses **not yet listed** (reached from empty searches), without
   the email field.

## 12. Answered (Ron, 2026-09-11)

1. **Resource approval is left to the AI**, working to an approval rules set Ron is writing. No human
   spot-check step is built; `/admin/resources` remains for reversals.
2. **No email.** Requesters and submitters stay anonymous. After a request the site says to **check back —
   the site is updated weekly.** The "notify me" link is dropped from phase 2; the email field is removed
   from the request form.
3. **Refresh** is Ron's automated refresh / check cycle for guides (content side). The site's part is the
   `updatedSince` / `hasGuide` filters on the course list API.
4. **Programs** come from the schools' course catalogs, by rules still to be written. **The site builds the
   interface to create them** — data model, admin API and pages — and the content session fills them
   (phase 5).
5. `guide-pipeline-tooling` is committed and merged so **all work starts from a single `master`**.
6. **Course titles are corrected by continuous site reviews.** The course `PUT` therefore **writes the title
   it is sent**; the only protection is that a guide push never resets a real title to the `CourseId`
   placeholder.

## 13. Out of scope for this release

Resource flagging / broken-link checks, voting or ranking resources, resource types beyond Website and
YouTube, submitter accounts, requester emails, Programs and Career Paths content.
