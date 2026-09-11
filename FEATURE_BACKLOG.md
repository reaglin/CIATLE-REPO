# Feature backlog — floridacourserepo.com

Queued ideas for future releases of the website. **Nothing here is started or scheduled.** This is a
capture list; Ron adds items as he thinks of them, and they get picked up deliberately.

Distinct from [`Deployment/PENDING_SERVER_CHANGES.md`](Deployment/PENDING_SERVER_CHANGES.md), which holds
code changes already written and awaiting the next deploy.

---

## Open items

### 1. Front page — total number of courses with guides

Show a live count of published curriculum guides on the front page.

- **Why:** the number is the site's clearest signal of scale and progress, and it is currently invisible to a
  visitor. As of 2026-08-31 it is **849**.
- **Where:** `PreseMakerRepo.Api` front page (Razor Pages).
- **Data:** count of `TaxonomyCourse` records having a published curriculum guide. Cheap query; worth caching
  briefly rather than counting per request.
- **Open questions:** count guides only, or also modules/materials? Static text or animated? Does it belong
  alongside other totals (courses in taxonomy, contributors)?

### 2. "All Guides" page — full list with links

A single browsable index of every course that has a curriculum guide, each linking to its guide.

- **Why:** there is currently no way to see the whole collection. Browsing is taxonomy-driven, which works
  for finding a known course but not for seeing what exists.
- **Where:** new page under the `/browse/` namespace.
- **Scale consideration:** ~849 entries today and growing toward ~1,650. Needs either pagination or the
  alphabetic letter-navigation pattern already used on the Browse-by-Subdiscipline page (commit `b57cd91`),
  which is probably the better fit for consistency.
- **Worth including per row:** course ID, title, credits, contact hours, and possibly prefix/discipline so
  the list is scannable and sortable.
- **Open questions:** group by prefix, by discipline, or flat alphabetical? Include a search/filter box?
  Should it expose the guide's `version` so updated guides are visible?

### 3. Static site export to GitHub Pages

> **Implemented 2026-09-03 (server side):** Admin console → **Static Export** (`/admin/static-export`)
> builds a self-contained zip of the public site — browse tree, every course page with a guide or
> modules (optionally every taxonomy course), every guide, module/material pages — by fetching the
> live pages over loopback and rewriting links to relative `…/index.html` files
> (`PreseMakerRepo.Api/Services/StaticSiteExporter.cs`, background job with progress). Unzipped, it
> is a working offline copy and a readable backup; files stay in `{Storage:RootPath}/exports/`.
> Pushing the zip's contents to a `gh-pages` branch is the remaining (manual or scripted) step.

Ability to push all guides to GitHub as a static site, viewable through GitHub Pages.

- **Why:** a durable, zero-infrastructure public mirror — resilient to server issues, independently
  citable, and indexable. Also a natural backup of the content in a readable form.
- **Rough shape:** a generator that pulls every guide from the API (or directly from the database), renders
  each to a static HTML page with the site's styling, builds an index page (see item 2 — same data), and
  commits the output to a `gh-pages` branch or a `/docs` folder.
- **Where it fits:** this is content tooling, so `Tools/` is the natural home — it already has the API
  client, credentials handling, and the queue as a manifest of what exists.
- **Open questions:** full mirror or curated subset? Regenerate on every guide push, or on a schedule/manual
  trigger? How do the two sites relate — canonical URL, cross-links, a banner noting the mirror? Does the
  static export need the taxonomy browse structure or just guides plus an index?

### 4. "Request a Curriculum Guide" — visitor requests that drive the production queue

> **Implemented 2026-09-03:** `/request-guide` form (course number, title, **school where offered**,
> optional reason + email; hashed IP; 5/IP/hour; same requester deduplicated per day; refused when
> a guide exists), reached from course pages without a guide, missing-guide URLs, and empty
> searches. Admin ranking + triage at `/admin/guide-requests` (CSV export). API:
> `POST /api/v1/guide-requests` (public), `GET /api/v1/guide-requests?status=open` and
> `PATCH /api/v1/guide-requests/{id}/status` (admin). Queue integration:
> `python queue_mgr.py import-requests [--mark-queued]` — priority `500 − 10 × count`
> (`Tools/QUEUE_GUIDE.md`). Open question left: emailing requesters on publish (the address is
> stored; no mail is sent yet).

A feature letting a visitor request a guide for a course that does not yet have one, with the requests
tracked and used to generate the content queue.

- **Why:** this **changes how the pipeline is prioritised**, and that is the point rather than a side
  effect. The queue to date has been derived from institutional catalogs — build everything a school
  offers, in priority order. Once coverage of the major schools is good (not complete — *good*),
  **demand should decide what gets built next** instead of a catalog's table of contents. A request is
  evidence that a real person wanted a specific guide, which is a far better signal than an inventory
  count.
- **Where:** `PreseMakerRepo.Api` — a request form on the browse/guide surface, most usefully at the point
  a visitor discovers a guide is missing. The "guide not found" path is the natural trigger.
- **Rough shape:** capture the course (prefix + number, ideally validated against the taxonomy), optionally
  the institution and a free-text reason; store with a timestamp and a hashed reporter IP (the same
  treatment `ContentFlag` already uses — see the security constraints in `CLAUDE.md`); expose an admin view
  ranked by request count.
- **How it feeds `Tools/`:** the existing pipeline is queue-driven (`Tools/queue.csv`, `queue_mgr.py`).
  The cleanest integration is an **API endpoint the queue tool can read** to pull open requests and add
  them as queue rows with a priority derived from request volume — so the generation loop stays exactly as
  it is and only the source of the queue changes.
- **Open questions:** require an email to notify the requester when the guide is published, or keep it
  anonymous? Rate limiting and abuse handling (the report endpoint's 5/IP/hour limit is a precedent).
  Deduplicate requests for the same course, or count them and use the count as the priority? Show the
  requester how many others asked for the same course? Should a request for a course **not in the
  taxonomy** be accepted at all, and if so how is it triaged?
- **Related:** **44 queued courses were skipped on 2026-09-03** because they have no Daytona State catalog
  coverage and therefore no Tier-0 source — they are marked `skipped` in `Tools/queue.csv` with that
  reason rather than deleted, **specifically so this feature can resurrect the ones people actually ask
  for.** Two of them, **MEA0002C and MEA0520C, are offered at 22 institutions each** and are the strongest
  candidates in that set.

---

## Conventions for this file

- One section per idea, with enough context that a future session can act without re-deriving the intent.
- Record the **why**, not only the what.
- Note open questions rather than resolving them prematurely — they are usually Ron's call.
- Move an item to `Deployment/PENDING_SERVER_CHANGES.md` (or delete it) once it is built.

## Course catalog, one-click guide requests & course resources (Ron, 2026-09-11) — planned, see `COURSE_CATALOG_PLAN.md`

**List every course that exists, not only the ones with a guide; generate guides on request.** Course rows get
**Course Resources** (website / YouTube links, public AI-reviewed queue) and **View Guide / Request Guide**
(one click, public queue). Main page gains Courses · Programs (soon) · Career Paths (soon). The `Tools/`
session adds courses — with or without guides — over a new course API, by rules Ron gives it.

**Status: plan written 2026-09-11 ([`COURSE_CATALOG_PLAN.md`](COURSE_CATALOG_PLAN.md)) — build not started.**
Supersedes the offerings-seed approach in `CAREER_PATHS_PLAN.md` §4: `Institution` / `CourseOffering` are
built in phase 1 of this plan and fed by the API.

## Career pathway tracing (Ron, 2026-09-04) — planned, see `CAREER_PATHS_PLAN.md`

**Take a profession and trace an educational path to it: which courses, in what order, at which
institutions.** Professions to start from: **law, nursing** — then engineering, accounting, allied health.

**Status: plan written 2026-09-04 ([`CAREER_PATHS_PLAN.md`](CAREER_PATHS_PLAN.md)) — build not started.**
Decisions taken: first release ships Registered Nurse, Mechanical Engineer, Accountant/CPA, Lawyer/Paralegal;
institution codes only (names later); courses presented as named routes with stages. Recorded so current guide-writing accumulates the right material. See the
"Where this project is going" section of the root `CLAUDE.md` for what the guides already capture and,
importantly, for the five constraints such a feature has to handle.

**⚠ The hard part is not the graph — it is that the naive graph is wrong.** Course numbers do not
uniquely identify subjects; suffixes mislead; institutions run parallel routes; programmatic
accreditation can outrank course credit; and prerequisite blocks are cohort-locked. A pathway that
ignores these would confidently send a student down a route that does not reach the licence.

Likely inputs already in hand: per-guide prerequisites (verbatim, with grade and concurrency conditions),
SOC codes in Career Pathways, licensure/accreditation notes, and `courses_2plus_institutions.csv` for
which institutions offer what.
