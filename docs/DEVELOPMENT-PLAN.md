# Development plan — Florida Course Repository (CIATLE-REPO)

The live site is **[floridacourserepo.com](https://floridacourserepo.com)** — 24,415 courses,
2,504 curriculum guides, 10 career paths and 5 programmes as of 2026-09-19. This file is where
planning and status live for **the site and its APIs** (the root session). Guide *content* is
planned and tracked by the `Tools/` session in `Tools/NEXT_SESSION.md`, `Tools/SOURCES.md` and
`Tools/REVIEW_QUEUE.md`; only the items that need site code or a deploy appear here.

**How an item is marked**

| Mark | Means |
|---|---|
| *(no icon)* or ⬜ | to do — not started, or still being built |
| ⚠️ | **action needed** — built and tested, waiting for Ron to verify; or returned with a comment; or blocked on an answer from Ron. The row says which |
| ✅ | done — built, tested, **and verified by Ron** |

Claude never marks an item ✅ on its own. Passing tests and a clean UX review earn ⚠️.

---

## Phase 1 — Course catalog ⚠️

Shipped in two releases on 2026-09-11 and live since; design in `COURSE_CATALOG_PLAN.md` §10.

| # | Task | Done when |
|---|---|---|
| 1.1 ⚠️ | Courses exist without guides — catalog API, course pages, with/without-guide filters, counts | Ron browses a subject, filters, opens a guide-less course. **Live; awaiting his sign-off** |
| 1.2 ⚠️ | One-click Request Guide + public queue `/queue/guides` | Requests recorded and ranked in the admin queue. **Live** |
| 1.3 ⚠️ | Course Resources — submission, review pipeline, `/queue/resources`, helpful votes | Ron approves one resource end to end through `/resources`. **Live** |
| 1.4 | `Tools/resources/APPROVAL_RULES.md` — **Ron to complete** the approval standard | The rules file states what is approved and what is refused, and the `/resources` skill follows it |

## Phase 2 — The CIP tree and the Career Paths platform ⚠️

Built 2026-09-17, **deployed and verified live 2026-09-19**. Design and the decisions behind it:
`CAREER_PATHS_PLAN.md` §0.

| # | Task | Done when |
|---|---|---|
| 2.1 ⚠️ | CIP tree (208 nodes) + `/careers`, `/careers/area/{code}`, `/careers/{slug}` + the career-path API | `GET /api/v1/cip` returns 208 nodes and the pages render. **Verified live 2026-09-19 — Ron to look at the pages** |
| 2.2 ⚠️ | A path may carry many CIP anchors (`CareerPathCips`), each with its evidence | Lawyer appears under 11 CIP series with its LSAC shares. **Live** |
| 2.3 ⚠️ | "Where you can take these courses in Florida" — institutions ranked by how many of the path's courses they carry | Renders on all ten path pages. **Live**. ⚠ The wording is deliberately *these schools teach the courses*, not *this school offers the degree* |
| 2.4 ⚠️ | `Tools/career_paths.py` (validate · push · list) and the authoring standard | A path round-trips from JSON to the live page. **In use for all ten paths** |
| 2.5 | Course pages carry no **"Part of these career paths"** / **"Part of these programs"** backlink yet — planned in both plans, never built | A course page lists the paths and programmes that name it, from `CareerPathCourse` and the programme CIP join |
| 2.6 | No admin page for career paths (`/admin/career-paths`: publish/unpublish, delete, courses without guides) | Ron can unpublish a path without a JSON round-trip |
| 2.7 | Static export has `/careers` and `/programs` seeded and allowed, but no export zip has been opened since | A fresh export zip renders a path page and a programme page offline |

## Phase 3 — Programs ⚠️

Built 2026-09-17 on Ron's ruling that **a programme sits one level above a degree** and **owns no
school list** — which schools offer it is derived from 6,427 IPEDS award rows by CIP prefix.

| # | Task | Done when |
|---|---|---|
| 3.1 ⚠️ | `Programs`, `ProgramCips`, `CareerPathPrograms`, `InstitutionAwards` + `/programs`, `/programs/{slug}` | Nursing lists 78 institutions including every technical college. **Live** |
| 3.2 ⚠️ | "Programs that lead here" on a path page, with how many Florida schools offer each | Renders on Mechanical Engineer. **Live** |
| 3.3 | **Only 5 programmes exist** (nursing, engineering technology, mechanical / chemical / biomedical engineering) against 10 published paths and a 50-path queue. ⚠ It shows: **Data Scientist's only programme is Mechanical Engineering**, with a note saying it is not a route in — there is no computing programme to name | Every published path names a programme that actually leads there. No longer blocked: 3.4 makes a programme ordinary pushable content, so this is now authoring work — computer science, civil / electrical / industrial / aerospace engineering, and law next |
| 3.4 ⚠️ | **Programmes over the API** — built 2026-09-19 (Ron chose this over more path content). `ProgramsController` (GET list/one, PUT, DELETE), `Tools/programs.py` (validate · push · list · show · delete), `Tools/programs/*.json` for the five existing programmes, `Tools/PROGRAM_API.md`. ⚠⚠ **`ProgramSeed` is now create-only**, so the build-shipped file bootstraps a fresh database and never overwrites a pushed edit | ⚠ **Needs a code-only deploy**, then `python programs.py push --all` against production to confirm the round trip. Verified on the dev database: create, update, unpublish/visibility, 403 on `?includeUnpublished` without admin, 409 when a path names the programme, 422 on an unseeded CIP code, 400 on a part-code like `14.1`, and a pushed edit surviving a restart. **UX: cognitive walkthrough + heuristic evaluation run on the CLI — 1 critical (unguarded `delete` against production) and 6 major findings fixed**, including server errors printed as prose with a next step, and `validate` now checking CIP codes against `cip.json` so the one failure that needs a redeploy is caught locally |
| 3.5 | The IPEDS award data is **2023** and neither the year nor the CIP edition is shown to the reader | The programme page states the award year and CIP edition it is counting |
| 3.6 | Part-codes are refused and whole levels required (`15.`, `51.38`, `14.1901`) because codes are matched with `StartsWith` — but the **five existing programmes were written before that rule** | A sweep confirms every live programme's codes are whole levels (they are, as exported) and the rule is in `Tools/PROGRAM_API.md` |

## Phase 4 — Career path content (the 50-path queue) ⚠️

`Tools/career_paths/QUEUE.csv` — 50 paths ranked, each with its CIP anchor, SOC code and cluster.
**10 published, 40 to go.**

| # | Task | Done when |
|---|---|---|
| 4.1 ⚠️ | **Engineering (ranks 1–7)** — mechanical, electrical, civil, industrial, aerospace, chemical, biomedical | All seven live. **Awaiting Ron's read of at least one** |
| 4.2 ⚠️ | **Registered Nurse (28)**, **Lawyer (45)**, **Data Scientist (40)** | Live. Data Scientist pushed 2026-09-19, once the 208-node CIP seed had deployed |
| 4.3 | Engineering remainder — environmental (8), computer hardware (9), materials (10) | Authored, validated, pushed, and each names a programme |
| 4.4 | **Manufacturing / CTE cluster (11–27)** — technicians, machining, welding, HVAC, electrician, aviation and automotive maintenance, logistics | Pushed and live. ⚠ This is the cluster the course-CIP evidence rule was blind to (universities publish CIP codes, state and technical colleges do not) — expect more `EXTRA_GROUPS` additions, each with its reason recorded, and each needing a deploy before the path can publish |
| 4.5 | **Health (29–36)** — LPN, radiologic technologist, respiratory therapist, dental hygienist, MLS, PTA, paramedic, surgical technologist | Pushed and live, each with its accreditation/licensure note above the course list |
| 4.6 | **Computing (37–39)**, **business (41–44)**, **law (46)**, **education (47–48)**, **public safety (49–50)** | Pushed and live |
| 4.7 | Every path's courses exist in the catalog (`unlistedCourses` empty on push) | No path links through to a page that is not there |

## Phase 5 — Guide-field changes still owed to the `Tools/` session

| # | Task | Done when |
|---|---|---|
| 5.1 ⚠️ | `Prerequisites` ceiling 500 → 1000 — written 2026-09-12, **deployed 2026-09-19** | ⚠ **The `Tools/` session pushes a guide with more than 500 characters of prerequisites** (`SCE4320` is the known case) and it is not refused 400 |
| 5.2 | `offering_notes` on guides — asked for 2026-09-11, **not written** | The field validates, stores and renders, and `Tools/validate_drafts.py` mirrors the rule |
| 5.3 | Field sizing — the 133 clock-hour rows, and the guide/course validators disagreeing on the same two fields | Both validators agree and no legitimate row is refused. Detail in `Deployment/PENDING_SERVER_CHANGES.md` |

---

## Open questions for Ron

1. ~~**(asked 2026-09-19) Programmes need a redeploy for every addition — should they move to the
   API?**~~ **Answered the same day: yes, build it.** Done — item 3.4; it awaits a deploy and Ron's
   verification.
2. **(asked 2026-09-19) Which cluster of the 50-path queue comes next?** Rank order says the three
   remaining engineering paths (environmental, computer hardware, materials). The manufacturing and
   CTE cluster (11–27) is where the sponsor emphasis points, is the thinnest part of the site today,
   and is where the CIP seed is weakest — so it will surface more gaps.
3. **(asked 2026-09-19) Course pages do not say which paths or programmes name a course** (item 2.5).
   Both plans call for it, and it is the backlink that makes 24,415 course pages feed the career
   section. Build it now, or once more paths exist to point at?

## References

- `CAREER_PATHS_PLAN.md` — the career-path design; **§0 is what was actually built** and supersedes the 2026-09-04 design below it
- `COURSE_CATALOG_PLAN.md` — the course catalog, the programme ruling, and §14's direction for paths
- `Deployment/PENDING_SERVER_CHANGES.md` — what needs a redeploy, and the record of what each deploy carried
- `FEATURE_BACKLOG.md` — captured ideas; nothing there is started or scheduled
- `Tools/PROGRAM_API.md` — the programme contract: what a programme is, the CIP rules, and the push loop
- `Tools/career_paths/QUEUE.csv` — the 50 ranked paths with their CIP and SOC anchors, and publish status
- `Tools/Generate_Guides_and_Push_Process.md` — the guide pipeline end to end (the `Tools/` session)
- `Tools/REVIEW_QUEUE.md` — content decisions waiting on Ron (the `Tools/` session)
- `Specifications/` — the three Phase-1 specs, still authoritative for the API envelope and error codes
