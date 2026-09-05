# Career Paths — implementation plan

**Status:** plan approved for build 2026-09-04 (Ron's decisions in §1). Nothing built yet.
**Feature ask (Overall_To_Do):** a "Career Paths" section of floridacourserepo.com. Start with a few
paths, expand if useful. Each page: definition of the profession · necessary skills · courses
supporting the path · schools represented in the repo offering it · advice. "We may add items if
we get questions that can be answered on these pages."
**Direction (root `CLAUDE.md`, "Where this project is going"):** take a profession and trace an
educational path to it — which courses, in what order, at which institutions — **without** the
naive course-code graph that CLAUDE.md warns would mislead students.

---

## 1. Decisions already made (Ron, 2026-09-04)

| Decision | Choice |
|---|---|
| First release paths | **Registered Nurse · Mechanical Engineer · Accountant / CPA · Lawyer (pre-law only)**. Paralegal becomes its own path later. |
| Disclaimer | Informational use only; students should seek additional information about their choices (see §5 wording). |
| Institution lists | Per course row: show at most **5** institution codes, then "+N more" that expands. |
| Institution names | **Codes only for v1** (UCF, DSC, PESC…). A code→name table is a later add; the schema leaves room for it. |
| Course presentation | **Named routes with stages.** A path holds one or more routes (e.g. RN: "A.S.N. → NCLEX-RN", "LPN-to-RN bridge", "B.S.N. direct", "RN-to-BSN completion"); each route is an ordered list of stages (Prerequisites → Core → Clinical → Licensure…); each stage lists courses with a role and a note. A simple path has one route. |

---

## 2. What the codebase already gives us (survey 2026-09-04)

- **1,892 guide drafts** in `Tools/drafts/`; **1,884 have a `Career Pathways` section, 1,304 carry SOC
  codes (380 distinct)**. Top codes: 25-2031, 11-9111, 29-2011, 29-1141 (RN, 55 guides)… This is the
  raw material for *suggesting* which courses belong to a path — as an authoring aid, never as the
  page itself.
- Guides are stored as one HTML blob (`CurriculumGuide.HtmlContent`, `<h2>` sections). Nothing
  structured about occupations or prerequisites exists server-side; `Prerequisites` is free text.
- **Institution coverage lives only in `Tools/courses_2plus_institutions.csv`** — 16,650 courses ×
  **125 institution codes** (courses offered at ≥2 institutions; single-institution courses are absent,
  so "offered at" must be read as "at least"). The server has **no course→institution table**, and there
  is **no code→name map anywhere in the repo**.
- Patterns to copy: `GuideRequest` + `GuideRequestsController` + `GuideRequestService` (newest entity,
  migration `AddGuideRequests`); `TaxonomyNodeDescription` (admin-edited, sanitized HTML column);
  `generate_guide.py` (admin JWT login + `PUT /api/v1/courses/{id}/guide`) for Tools→API pushes;
  `StaticSiteExporter` (explicit `Enqueue("/browse…")` list + path allow-list — new pages must be added
  to both); `TaxonomySeed` (idempotent startup seed from a file) for the offerings seed.
- No test project exists in CIATLE-REPO. Validation is mirrored in Python (`validate_drafts.py`).

---

## 3. Principles (non-negotiable — they answer CLAUDE.md's five warnings)

1. **Paths are curated content, not derived data.** Every course on a path is placed there by an author
   (AI-drafted, human-checked), identified by exact `CourseId`. No prerequisite-text parsing, no code
   arithmetic (`C`/`L` suffixes), no inference from taxonomy position.
2. **Routes are explicit.** A path that has parallel routes (pre-licensure vs degree-completion; standard vs
   Professional Track) shows them as separate named routes with an *audience* line ("you already hold an
   LPN licence") and a *terminal credential* line ("A.S.N. → eligible for NCLEX-RN").
3. **Accreditation and licensure are first-class.** Each route states the programme-approval / licensure
   requirement in its own field, rendered above the course list, with the standing warning that
   *completing these courses individually does not by itself qualify you* where that is true.
4. **Institution variance is a note, not a fact table.** Where the same SCNS number carries a different
   subject somewhere (`NUR4286`, `NUR4826`), the course entry carries a `variantNote`; the page renders it
   inline. Offerings data is used only for "these institutions list this course", never "you can complete
   this route at X".
5. **Everything links to a guide or to a guide request.** A course row links to its curriculum guide when
   one exists, otherwise to `/request-guide?course=…` — the path pages become a demand signal for the
   guide queue (backlog item 4).
6. **Omit rather than fabricate** (same rule as guides). A path with no substantiated skills section omits
   it.
7. **Visible disclaimer** on every path page (Ron's wording in §5): informational use only; students should
   seek additional information about their choices. Route-specific warnings (cohort-locked blocks,
   accreditation) stay in the route's own fields, not in the disclaimer.

---

## 4. Data model

Keep it to **two tables + one link table** by storing the routes tree as JSON (the same JSON-column pattern
`Module` uses for outcomes/topics). Normalising routes/stages/courses into four tables buys nothing the
site queries for; the one reverse lookup we need ("which paths include course X") is served by the link
table, refreshed on every save.

### `CareerPath` (new, `PreseMakerRepo.Core/Models/CareerPath.cs`)

| Column | Type | Notes |
|---|---|---|
| `Slug` | string PK | `registered-nurse`, `mechanical-engineer`, `accountant-cpa`, `lawyer`; lowercase, immutable |
| `Title` | string | "Registered Nurse" |
| `Summary` | string | one-line for cards and `<meta description>` |
| `SocCodes` | string (JSON array) | `["29-1141"]`; drives the *suggest* tool and the course-page backlink text |
| `DefinitionHtml` | string | "Definition of the profession" |
| `SkillsHtml` | string? | "Necessary skills" |
| `LicensureHtml` | string? | terminal requirement(s) for the profession as a whole (FE/PE, NCLEX-RN, CPA exam + 150 h, bar) |
| `AdviceHtml` | string? | "Advice" |
| `RoutesJson` | string | the routes tree, schema below |
| `Status` | enum `ContentStatus`-like: `Draft` / `Published` | only Published renders publicly |
| `Version` | string | same convention as guides (`1.0`) |
| `GeneratedUtc`, `UpdatedUtc` | DateTime | |

All HTML columns pass through the same sanitizer `TaxonomyNodeDescription` uses on save.

### `RoutesJson` schema

```json
{
  "routes": [
    {
      "key": "asn-nclex",
      "name": "Associate in Science in Nursing → NCLEX-RN",
      "audience": "Entering nursing without a prior nursing licence.",
      "credential": "A.S.N. from a Florida Board of Nursing-approved programme; eligibility to sit NCLEX-RN.",
      "accreditationNote": "NCLEX-RN eligibility requires completing an approved programme. Individually transferable courses do not qualify you on their own.",
      "warningsHtml": "<p>Nursing cohorts are block-scheduled: one failed course can delay the whole block by a year.</p>",
      "stages": [
        {
          "name": "Prerequisites (before programme admission)",
          "note": "Most programmes require a C or better in each.",
          "courses": [
            { "courseId": "BSC2085C", "role": "required", "note": "Anatomy & Physiology I" },
            { "courseId": "BSC2086C", "role": "required", "note": "A&P II — sequence with BSC2085C" },
            { "courseId": "MCB2010C", "role": "required" },
            { "courseId": "ENC1101C", "role": "required" },
            { "courseId": "PSY2012",  "role": "required" },
            { "courseId": "MAC1105",  "role": "choose", "choiceGroup": "math", "note": "or STA2023" },
            { "courseId": "STA2023",  "role": "choose", "choiceGroup": "math" }
          ]
        },
        {
          "name": "Nursing core (programme sequence)",
          "courses": [
            { "courseId": "NUR1020C", "role": "required", "variantNote": "Numbered NUR1021C at CF, EFSC, IRSC… — same position in the sequence." }
          ]
        }
      ]
    }
  ]
}
```

`role` ∈ `required` · `choose` (one of a `choiceGroup`) · `support` · `elective`. `courseId` **must exist in
the taxonomy** (validator + server both enforce); a course that is not in the taxonomy is expressed as a
free-text `externalNote` on the stage instead, never as a fake ID.

### `CareerPathCourse` (link table, rebuilt on save)

`CareerPathSlug` + `CourseId` (composite PK), `RouteKey`, `StageName`, `Role`. Serves the course-page
backlink ("Part of these career paths") and the admin "missing guides" report in one query.

### `Institution` and `CourseOffering` (new — the "schools" data)

| `Institution` | `CourseOffering` |
|---|---|
| `Code` PK (`UCF`) · `Name` string? (null in v1) · `Type` string? (state college / SUS university / private / other; null in v1) | `CourseId` + `InstitutionCode` composite PK |

Seeded at startup by an idempotent `OfferingSeed` from `PreseMakerRepo.Api/Data/Seed/course_offerings.csv`
(generated by a new `Tools/export_offerings.py` from `courses_2plus_institutions.csv`; ~40 k rows, a few
hundred KB). Ships inside the deploy artefact — **not** a side file like `taxonomy.json`, whose copy step
was silently missing for months (`PENDING_SERVER_CHANGES.md`). Only course IDs present in the taxonomy are
seeded; the rest are logged and dropped.

Migration name: `AddCareerPaths` (all four tables in one migration).

---

## 5. Public site

| Page | Route | Content |
|---|---|---|
| Index | `/careers` | Card per published path: title, summary, SOC code(s), route count, "N courses · M with guides". Ordered by title. |
| Path | `/careers/{slug}` | Header (title, SOC badge(s), summary) → **Definition** → **Necessary skills** → **Routes** (Bootstrap tabs when >1 route; each: audience, credential, accreditation callout, warnings, stages as ordered sections, course rows) → **Schools offering these courses** → **Licensure & certification** → **Advice** → disclaimer + "Updated … · v1.0". |
| Course page | `/courses/{id}` | New strip: "Part of these career paths: Registered Nurse (Nursing core) · …" via the link table. |
| Front page | `/` | Tile "Career Paths" beside "Browse by Discipline" listing the published paths. |
| Nav | `_Layout` | "Career Paths" link next to Browse. |

**Course row** = `COURSEID` · title (from taxonomy) · role badge · note / variantNote · **Guide** link or
**Request a guide** link · "offered at N institutions" showing **at most 5 codes** followed by "+N more"
that expands on click (v1: codes; names appear automatically once `Institution.Name` is filled).

**Disclaimer (Ron, 2026-09-04)** — rendered on every path page, above the routes and again in the footer:
*"This page is for informational use only. Course sequences and requirements differ between institutions
and change over time. Students should seek additional information about their choices from the
institution's advisers, the programme, and the licensing body before enrolling."*

**Schools section** (v1, codes only): for the path's `required` courses across all routes, list institutions
by how many of those courses they list — "UCF · 12 of 14 required courses listed", grouped into "lists all"
/ "lists most (≥75 %)" / "lists some". Explicit caption: *"Listing a course is not the same as offering the
programme; confirm programme approval with the institution."* Institutions absent from the inventory
(single-institution courses) are not shown — caption says so.

**Static export:** add `Enqueue("/careers")` and `/careers/{slug}` for each published path in
`StaticSiteExporter`, and `/careers` to the allow-list at the `path == "/" || …` check. Verify the exported
zip renders a path page offline.

---

## 6. API (`/api/v1/career-paths`)

| Verb | Route | Auth | Purpose |
|---|---|---|---|
| GET | `/api/v1/career-paths` | public | published list (slug, title, summary, socCodes, counts) |
| GET | `/api/v1/career-paths/{slug}` | public | full path incl. routes, each course resolved with title, hasGuide, offering count |
| PUT | `/api/v1/career-paths/{slug}` | AdminOnly | upsert from the Tools JSON (validates, sanitizes, rebuilds link table); `?publish=true` sets Published |
| DELETE | `/api/v1/career-paths/{slug}` | AdminOnly | remove |
| GET | `/api/v1/career-paths/{slug}/coverage` | AdminOnly | per-course: hasGuide, offeringCount; per-institution: required-course coverage — the numbers behind the Schools section and the admin report |

Envelope + FluentValidation as everywhere. New error codes: `CAREER_PATH_NOT_FOUND` (404),
`CAREER_PATH_INVALID` (422, `fields` lists offending `routes[i].stages[j].courses[k].courseId`),
`CAREER_PATH_COURSE_UNKNOWN` (422). Add to `ErrorCodes.cs` and the API spec's error table.

---

## 7. Content pipeline (`Tools/career_paths/`)

Same shape as guides — draft JSON → validate → push — so the loop Ron already runs applies.

```
Tools/career_paths/
  CLAUDE.md                 content standard for a path (below)
  drafts/{slug}.json        the CareerPath payload (HTML fields + routes)
  validate_career_paths.py  mirrors the server validator: slug/SOC format, every courseId in taxonomy
                            (GET /api/v1/courses/{id}), no empty route/stage, choiceGroups ≥2 members,
                            HTML whitelist; WARNS for courses without a guide and for courses offered at
                            <2 institutions
  push_career_path.py       admin login (reuse generate_guide.py's) → PUT …/career-paths/{slug} [--publish]
  suggest_courses.py        authoring aid: --soc 29-1141 [--prefix NUR] scans drafts/*_guide.json for the
                            SOC code (and the profession name), prints candidate courses with guide status,
                            num_inst, and the guide's "Position in the curriculum" sentence
  export_offerings.py       courses_2plus_institutions.csv → Api/Data/Seed/course_offerings.csv
```

**Content standard (goes in `Tools/career_paths/CLAUDE.md`):**
- Definition: what the profession does, in Florida, 2–4 paragraphs; name the regulator.
- Skills: bullets, each tied to where in the route it is built (so the list is not generic).
- Routes: only routes that actually exist in Florida institutions' catalogs; audience + credential lines
  mandatory; `accreditationNote` mandatory for licensed professions.
- Courses: exact SCNS IDs from the taxonomy; the *canonical* DSC numbering where DSC offers the course
  (Tier-0 rule in `SOURCES.md`), with `variantNote` for parallel numbering families; `note` carries grade
  conditions and co-requisites **verbatim from the guide's Prerequisites**, never paraphrased into a rule.
- Advice: the "what students get wrong" material the guides' Special Information sections already hold.
- Omit rather than fabricate. Every claim about licensure must name its source (board / statute / exam body).
- **Lawyer** is **pre-law only** in v1: one route, *Pre-law bachelor's → LSAT → J.D. → Florida Bar*. Any
  bachelor's qualifies, so the stages list *recommended* course choices (writing, logic, government,
  economics, philosophy, public speaking) and say so plainly; the credential line is the J.D. and bar
  admission. **Paralegal** (A.S., PLA courses, NALA/NFPA certification) is a separate path, queued for later.

---

## 8. Admin console

`/admin/career-paths`: table of all paths (status, version, updated, courses, **courses without a guide**,
institutions with full coverage) with **Publish / Unpublish** and **Delete**. No in-browser editor in v1 —
editing is the Tools JSON round-trip, same as guides. A "Download JSON" link on each row makes a server
copy the starting point for an edit. Dashboard card: published paths + missing-guide total.

---

## 9. Phases (each ends with something Ron can open in a browser)

| Phase | Builds | Hand-test |
|---|---|---|
| **1 — Model + one path** | `CareerPath`, `CareerPathCourse`, migration; `CareerPathService` (validate, sanitize, upsert, link rebuild); API GET/PUT/DELETE; `/careers/{slug}` page (routes, stages, course rows with guide/request links); `Tools/career_paths/` with validator + push + **Registered Nurse draft** authored from the 45 NUR guides | `python push_career_path.py registered-nurse --publish` then open `/careers/registered-nurse` locally; every course row links to a guide or a request form |
| **2 — Schools + discovery** | `Institution`, `CourseOffering`, `export_offerings.py`, `OfferingSeed`; Schools section + per-row "offered at N"; course-page backlinks; `/careers` index; nav link; front-page tile; static-export entries | RN page shows the Schools ranking; `/courses/NUR1020C` shows "Part of: Registered Nurse"; static export zip includes `careers/registered-nurse/index.html` |
| **3 — Remaining paths** | `suggest_courses.py`; content standard; **Mechanical Engineer, Accountant/CPA, Lawyer (pre-law)** drafts (validated, pushed, reviewed by Ron) | four cards on `/careers`; ME route shows FE/PE licensure and the 2+2 transfer note |
| **4 — Admin + release** | `/admin/career-paths` list, publish toggle, missing-guide count, JSON download; API spec + error codes; `PENDING_SERVER_CHANGES.md` entry (**migration — deploy without `-SkipMigrations`**); `FEATURE_BACKLOG.md` career-pathway item moved to built | deploy; live `/careers`; admin page lists 4 paths |

Rough size: phase 1 is the largest (one session); 2 and 3 about one session each; 4 half a session.
Phase 3's authoring is the part that needs Ron's review most — the RN draft in phase 1 is the pattern.

---

## 10. Deliberately out of v1 (queued in `FEATURE_BACKLOG.md` when this ships)

- **Paralegal** as its own path (A.S., PLA courses, NALA/NFPA certification) — Ron's call 2026-09-04;
  the Lawyer path stays pre-law only.
- Institution **names/types** (fill `Institution.Name` from a CSV Ron supplies or from the SCNS handbook's
  institution list; the pages pick names up with no code change).
- "Can I complete this whole route at institution X?" — needs programme-level data, not course listings.
- **Request a career path** (mirror of request-guide) and per-path feedback/questions — the to-do says
  new page items will come from questions; capture them first.
- BLS wage / outlook links per SOC code; O*NET skills cross-check.
- Prerequisite **graph** rendering — only if/when prerequisites are captured structurally in guides.
- Admin in-browser route editor.

---

## 11. Open questions for Ron (do not block phase 1)

Answered 2026-09-04: disclaimer wording (§5), institution list cap of 5 (§1/§5), Lawyer = pre-law only
with Paralegal as a later path (§7/§10).

1. Version bumps: treat a route change as a new version (like guides) — yes unless told otherwise.
