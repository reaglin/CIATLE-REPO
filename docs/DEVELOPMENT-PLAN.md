# Development plan — Florida Course Repository (CIATLE-REPO)

The live site is **[floridacourserepo.com](https://floridacourserepo.com)** — 24,415 courses,
2,504 curriculum guides, **17 career paths and 22 programmes** as of 2026-09-20, with 60 curated links between them and no programme left without a career. This file is where
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
| 2.5 | **Course pages** still carry no "Part of these career paths" / "Part of these programs" backlink. ⚠ The programme↔career direction is now done (item 3.9); this is the remaining third of the web — 24,415 course pages that do not say what they are part of | A course page lists the paths and programmes that name it, from `CareerPathCourse` and the programme CIP join |
| 2.6 | No admin page for career paths (`/admin/career-paths`: publish/unpublish, delete, courses without guides) | Ron can unpublish a path without a JSON round-trip |
| 2.7 | Static export has `/careers` and `/programs` seeded and allowed, but no export zip has been opened since | A fresh export zip renders a path page and a programme page offline |

## Phase 3 — Programs ⚠️

Built 2026-09-17 on Ron's ruling that **a programme sits one level above a degree** and **owns no
school list** — which schools offer it is derived from 6,427 IPEDS award rows by CIP prefix.

| # | Task | Done when |
|---|---|---|
| 3.1 ⚠️ | `Programs`, `ProgramCips`, `CareerPathPrograms`, `InstitutionAwards` + `/programs`, `/programs/{slug}` | Nursing lists 78 institutions including every technical college. **Live** |
| 3.2 ⚠️ | "Programs that lead here" on a path page, with how many Florida schools offer each | Renders on Mechanical Engineer. **Live** |
| 3.3 ⚠️ | **Programmes for every published path** — seven authored and pushed 2026-09-19 (electrical, civil, aerospace, industrial and systems engineering; computer science; data science and analytics; law), taking the site from 5 programmes to **12**. Every published path now names a programme that actually leads there, and Data Scientist no longer lists Mechanical Engineering as its only one | ⚠ Ron reads two or three of the new programme pages — `/programs/law` (4 public law schools, J.D. only) and `/programs/aerospace-engineering` (3 schools) are the ones where the school list carries the most weight |
| 3.4 ⚠️ | **Programmes over the API** — built 2026-09-19 (Ron chose this over more path content). `ProgramsController` (GET list/one, PUT, DELETE), `Tools/programs.py` (validate · push · list · show · delete), `Tools/programs/*.json` for the five existing programmes, `Tools/PROGRAM_API.md`. ⚠⚠ **`ProgramSeed` is now create-only**, so the build-shipped file bootstraps a fresh database and never overwrites a pushed edit | ✅ **Deployed 2026-09-19** and the round trip confirmed live (`PUT …/__probe` → 401, five programmes re-pushed unchanged, seven new ones created without a deploy). ⚠ Ron to confirm the pipeline reads the way he wants. Verified on the dev database: create, update, unpublish/visibility, 403 on `?includeUnpublished` without admin, 409 when a path names the programme, 422 on an unseeded CIP code, 400 on a part-code like `14.1`, and a pushed edit surviving a restart. **UX: cognitive walkthrough + heuristic evaluation run on the CLI — 1 critical (unguarded `delete` against production) and 6 major findings fixed**, including server errors printed as prose with a next step, and `validate` now checking CIP codes against `cip.json` so the one failure that needs a redeploy is caught locally |
| 3.5 | The programme page states the IPEDS award **year** (2023) and that the data is first-majors only, but not the **CIP edition** (2020) the codes belong to — codes move between editions | The page names the CIP edition beside the award year |
| 3.6 ⚠️ | Part-codes are refused and whole levels required (`15.`, `51.38`, `14.1901`) because codes are matched with `StartsWith`, and the five original programmes predate that rule | ✅ Swept: all 12 documents validate clean. The one flag is Engineering Technology's `15.`, which claims a whole series deliberately and says so in its note |
| 3.7 ⚠️ | **Correction, 2026-09-19: every engineering programme was claiming CIP 14.01 General Engineering** — seeded with the reason "where several Florida institutions place a first year common to all engineering majors". ⚠⚠ But IPEDS counts *awarded degrees*, not first years, so 14.01 added six institutions awarding a general or engineering-science degree rather than the named one. Aerospace read **9 schools instead of 3**; USF appeared with **zero completions**. Dropped from all seven and re-pushed | ⚠ The counts now match the degree (mechanical 11, civil 9, electrical 10, biomedical 8, industrial 6, chemical 4, aerospace 3). Ron to confirm this is the reading he wants: *a school is listed when it awards THIS degree*, not when it teaches a first year that leads toward it |
| 3.8 | The home page tile says Programs are **"degrees and certificates, with the courses each one requires"**, but a programme carries no course list — the model has no `ProgramCourse` | Either the copy stops promising courses, or programmes gain a course list (`COURSE_CATALOG_PLAN.md` §14 sketched one). ⚠ Needs Ron's call on which |
| 3.9 ⚠️ | **The connections — DEPLOYED AND LIVE 2026-09-20.** Built 2026-09-19 on Ron's note — *"students can easily find … the connections between the career paths, the options along a path, and the programs offering the final degree"*. A programme page now lists **the careers it leads to** (the data existed and nothing rendered it) and **the programmes closest to it**, each with the reason; a path page lists **the careers next to it** in the same CIP series. Migration `AddProgramRelations`; `related` on the programme API, read in both directions | ⚠ **Needs a deploy with migrations**, then `programs.py push --all`. Ron then walks one chain: `/careers/aerospace-engineer` → `/programs/aerospace-engineering` → `/programs/mechanical-engineering` → back to a career. **UX: cognitive walkthrough + heuristics run on both pages — 6 major findings, all fixed**, the load-bearing one being that a heading asserted a route its own note denied (now `isRoute`, with the rows grouped separately) | ⚠ **Needs a deploy with migrations** (`AddProgramRelations`, `AddProgramConnections`), then `programs.py push --all` and `career_paths.py push --all`. Ron then walks one chain: `/careers/aerospace-engineer` → `/programs/aerospace-engineering` → `/programs/mechanical-engineering` → back to a career |
| 3.10 ⚠️ | **Six more programmes so the field has its options** — computer, environmental, materials and ocean engineering; statistics; paralegal and legal support studies. ⚠ Materials and ocean are mostly GRADUATE in Florida (materials: 4 institutions, 2 at bachelor's; ocean: 2, one at bachelor's), which the pages say plainly, and paralegal is the widest-reach legal programme in the state at 31 institutions | ⚠ Ron reads `/programs/materials-engineering` and `/programs/paralegal-studies` — both make a claim about the ROUTE rather than the degree |
| 3.11 ⚠️ | Four of the six new programmes had no career path, so their pages could not say what they led to | ✅ Closed. Three paths were written (item 4.3), and **ocean engineering goes under Civil Engineer** — Ron, 2026-09-20: *"Use civil for ocean."* The civil path now carries a coastal section, the ocean-engineering programme link and CWR4001, so the programme page says what it leads to without a one-institution path being invented for it |
| 3.12 | ⚠ Every programme and career page loads the whole 6,427-row award table to count schools, and rescans it per related programme. Correct and stale-proof, but it is a full table read per page view | A cached CIP-prefix → institution-count lookup, invalidated when the awards seed changes. Only worth doing if the table grows or the pages feel slow |

## Phase 4 — Career path content (the 50-path queue) ⚠️

`Tools/career_paths/QUEUE.csv` — 50 paths ranked, each with its CIP anchor, SOC code and cluster.
**17 published as of 2026-09-20** — the seven engineering paths, Registered Nurse, Lawyer, Data Scientist, environmental/computer-hardware/materials engineer, and the four CTE paths (automotive, welder, HVAC, electrician). **33 to go.**

| # | Task | Done when |
|---|---|---|
| 4.1 ⚠️ | **Engineering (ranks 1–7)** — mechanical, electrical, civil, industrial, aerospace, chemical, biomedical | All seven live. **Awaiting Ron's read of at least one** |
| 4.2 ⚠️ | **Registered Nurse (28)**, **Lawyer (45)**, **Data Scientist (40)** | Live. Data Scientist pushed 2026-09-19, once the 208-node CIP seed had deployed |
| 4.3 ⚠️ | **Engineering remainder — environmental (8), computer hardware (9), materials (10), ALL LIVE 2026-09-20** — written 2026-09-19, validated clean, and rendered locally. Each carries O*NET and BLS figures, a Florida-specific section, and carrier counts taken from the SCNS flat file for every course | ⚠ **Waiting on the deploy** (their programmes are not live yet), then `career_paths.py push --all`. Ron reads one of the three — Materials Engineer is the one with the sharpest finding: Florida awards it at only two institutions at bachelor's level, so the honest route is mechanical or chemical first |
| 4.4 | **Manufacturing / CTE cluster (11–27)** — technicians, machining, welding, HVAC, electrician, aviation and automotive maintenance, logistics | Pushed and live. ⚠ This is the cluster the course-CIP evidence rule was blind to (universities publish CIP codes, state and technical colleges do not) — expect more `EXTRA_GROUPS` additions, each with its reason recorded, and each needing a deploy before the path can publish |
| 4.5 | **Health (29–36)** — LPN, radiologic technologist, respiratory therapist, dental hygienist, MLS, PTA, paramedic, surgical technologist | Pushed and live, each with its accreditation/licensure note above the course list |
| 4.6 | **Computing (37–39)**, **business (41–44)**, **law (46)**, **education (47–48)**, **public safety (49–50)** | Pushed and live |
| 4.7 | Every path's courses exist in the catalog (`unlistedCourses` empty on push) | No path links through to a page that is not there |
| 4.8 ⚠️ | **13 courses the new paths name were missing from the catalog** and were sent ahead of the deploy (`POST /api/v1/courses/batch`) with per-institution offerings from the SCNS flat file | ✅ Live: COP3530, CDA4102, CDA4210, COP4600, EEE3308, EEE4351 and the seven EMA materials courses. ⚠ The pattern will repeat on every new path — `scratchpad/list_missing.py` in `Tools/` builds and sends them |
| 4.9 ⚠️ | **Ocean engineering is covered by the Civil Engineer path, not a path of its own** (Ron, 2026-09-20). The evidence supports it: two institutions award in CIP 14.24 and only FAU at bachelor's; FAU's ocean courses (EOC prefix) are carried by FAU alone; UNF holds the only coastal cluster, one carrier per course | ⚠ Civil Engineer gained a *"Coastal and ocean work is civil engineering here"* section, links to the ocean and environmental programmes, CWR4001 Coastal and Port Engineering, and the DEP Beaches/Inlets/Ports and USACE Jacksonville sources. Waiting on the deploy with the rest |
| 4.10 | ⚠⚠ **Additional paths need a research pass before they can be authored, and that is the cost to plan around** — not the writing. Ron, 2026-09-20: more research is needed for additional paths | The recipe, from the three written on 2026-09-19: **(1)** O*NET plus BLS for the SOC code, ⚠ checking whether the two disagree (they did on environmental engineering); **(2)** the programme footprint from IPEDS by CIP — how many Florida institutions, and at which LEVEL, since that is what decides whether the bachelor's route exists at all; **(3)** a carrier count from the SCNS flat file for EVERY course named, which is where the fragmentation warnings come from (`Tools/scratchpad/carriers.py`); **(4)** the licensure and accreditation reality, stated as statute where there is one; **(5)** for a CHOICE path, the entrant-major dataset by the Lawyer method — and ⚠ if none exists, say so; **(6)** any course the catalog does not carry, listed first (`Tools/scratchpad/list_missing.py`). ⚠ Reckon on roughly a session per path, and do not let the DIRECT ones crowd out the CHOICE ones because they are quicker |
| 4.11 ⚠️ | **Automotive Service Technician — LIVE 2026-09-20**, pushed to the front at Ron's request, with an **Automotive Technology** programme (CIP 47.0604, 47 institutions). The first path from the manufacturing/CTE cluster, and the first written from the **FLDOE curriculum framework** rather than university catalogues: Master Automotive Service Technology, 1,800 hours, nine occupational completion points, each a hireable exit | ⚠ Ron reads `/careers/automotive-service-technician`. The finding that shapes it: **you can stop at a completion point, work, and come back** — and Florida Statute 1004.925 requires every automotive programme in the state to be industry certified, which is a question a student can ask on a tour |
| 4.12 ⚠️ | ⚠⚠⚠ **The site had no technical colleges, and CTE lives there.** `scns.is_public()` answered SUS or FCS only, so every tool here was filtering out district technical colleges — which are public | ✅✅ **Ron answered yes to both parts, 2026-09-20, and both are done.** `sector_of()` now answers a third public sector **`TECH`** (44 codes, derived from SCNS names cross-checked against the IPEDS Florida-public file; one technical-SOUNDING private school rejected). The **back-catalogue sweep** corrected **117 courses** and restored **1,296 offerings** across **44 colleges**; the site went from **39 to 83 institutions**. ⚠ Fifteen CJK law-enforcement academy courses and eighteen EEV electronics courses had **no offerings at all** and now carry 13–18 each — those pages had been telling readers the course was taught nowhere. Ron to spot-check one CTE course page |
| 4.13 | ⚠ `Tools/scratchpad/cpalms_programs.json` (987 programmes) does **not** contain the main clock-hour automotive frameworks — they came back from the live service when queried by CIP directly | The cache is a partial listing, not the catalogue. Query `ProgramFrontend/programsummary?ProgramCIP=…` by CIP when a framework is missing, and re-dump the cache |
| 4.14 ⚠️ | **Welder — LIVE 2026-09-20** (queue rank 19), with a **Welding Technology** programme (CIP 48.0508, 47 institutions, 1,082 credentials in 2023). Second path from the CTE cluster, written from the FLDOE framework: 1,050 hours, three completion points, plus a 750-hour Advanced pipe certificate at 16 colleges | ⚠ Ron reads `/careers/welder`. Two findings lead it: **qualification is by TEST, not transcript** — a coupon under an AWS code or ASME Section IX, covering a range, lapsing if unused — and ⚠⚠ **Florida renumbered welding in 2025 and both families are live**: PMT0070–0074 at 30 institutions, PMT0011–0016 at 19, **16 carrying both** |
| 4.15 | ✅ `scratchpad/list_missing.py` now sends **clock hours** and handles trade acronyms (SMAW, GMAW, TIG) and hyphenated titles — it was built for credit courses and would have published the whole CTE catalogue with no measure of length at all | Used for the 13 welding courses; it is the tool every CTE path will need |
| 4.16 ⚠️ | **HVAC Technician — LIVE 2026-09-20** (queue rank 23), with an **HVAC/R Technology** programme. ⚠⚠ The queue filed HVAC under CIP 47.02 (31 institutions, 111 credentials); **Florida files it under 15.0501 — 45 institutions, 891 credentials** — and 15.05 was missing from the seeded tree, so both documents are refused 422 until `cip.json` (now 209 nodes) ships | ⚠ **Deploy, then `programs.py push hvac-technology` and `career_paths.py push hvac-technician`.** The page's own findings: EPA Section 608 is federal law, Florida LICENSES the contractor under Chapter 489 (Class A unlimited, Class B capped at 25 tons), and ⚠⚠ **the framework moved ahead of the colleges** — the current courses are at 4–6 institutions, the predecessor family at 22–25, and no institution carries both |
| 4.17 ⚠️ | **Electrician — LIVE 2026-09-20** (queue rank 24), with an **Electrical Technology** programme (CIP 46.0302, 41 institutions, 741 credentials). It is held only because it links to the HVAC programme, which is itself held by the CIP seed | ⚠ The page's findings: **81,000 openings a year — the largest on this site**; ⚠⚠ **Florida licenses the CONTRACTOR, not the electrician** (Chapter 489 Part II) and there is **no statewide journeyman licence** — counties and municipalities set those, so the advice is to ring the county building department before enrolling; and **two routes in**, the 1,200/1,500-hour certificate at 26 technical colleges, or a registered apprenticeship whose classroom half (Electrical Wiring I–VIII) runs at six to eight STATE colleges while you are paid to work |

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
