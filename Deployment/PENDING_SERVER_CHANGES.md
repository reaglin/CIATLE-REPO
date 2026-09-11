# Pending server changes

Changes that need a **server redeploy** (`.\Deployment\deploy-update.ps1` from the repo
root) to take effect. Curriculum guide content does *not* belong here — guides publish over
the REST API and need no deploy.

Bundle these into the next deploy, then delete the entry.

## Nothing is waiting on a deploy right now

The course catalog work (`COURSE_CATALOG_PLAN.md` phases 1–4b) is live — see the record below. The only
entry still open is the `Prerequisites` ceiling further down, which is **not written yet**.

## ✅ DEPLOYED 2026-09-11 — course catalog phases 1–4b, in two releases, both verified live

**Release 1 — phases 1 + 2** (migrations `AddCourseCatalog`, `GuideRequestChannel`): courses exist without
guides, with base data and institution offerings over `PUT /api/v1/courses/{id}` and
`POST /api/v1/courses/batch` (contract `Tools/COURSE_API.md`, spec §14); subject pages list every course with
**View Guide / Request Guide** and a with/without-guide filter; one-click guide requests with the public queue
`/queue/guides`; the main page gained **Courses · Programs · Career Paths**; counts read "N courses · M
guides"; guide-less course pages are `noindex`.

**Release 2 — phases 3, 4, 4b** (migrations `AddCourseResources`, `AddResourceVotes`): **course resources** —
a **Resources** button on every row and course page, `/courses/{id}/resources` with AI-written summaries, an
**Add a resource** form, the public review queue `/queue/resources`, the reviewer API
(`Tools/RESOURCE_API.md`), and `/admin/resources`; **thumbs-up voting** on each listing
(`POST /api/v1/resources/{id}/helpful`), listings ordered most-helpful first; course titles no longer repeat
the course number; the home page's "Recently Added" section is gone. Reviewer tooling (`Tools/resources/`)
shipped in the same commits and needed no deploy.

**Verified live after release 2:** resources and guide queue APIs 200 (both migrations applied); the EEE page
shows a Resources button on all 32 rows; `/courses/{id}/resources`, `/queue/resources`, `/queue/guides`,
`/programs`, `/careers` render; admin pages are login-protected; new `site.js` and `site.css` are served;
existing guide pages unchanged; header reads "3,003 courses · 2,197 curriculum guides".

**Notes for the `Tools/` session:** 806 guide-less courses were already in the database (mostly Engineering
Technology prefixes — ETI, CET, EET, ETS, ETD, ETP) and are now listed with Request Guide; some carry bad data
worth correcting (e.g. `EEV0360L` credits = 30, which are clock hours; `ETC5605` is graduate-level). Most
courses still store the course id as their title, so pages fall back to the guide title until real titles are
sent.

**Also resolved:** the four missing taxonomy nodes (CES, CWR, CEG, ENV) are in `taxonomy.json` and deployed,
and the guide-request / static-export release of 2026-09-03 is live (`/request-guide` 200,
`/admin/guide-requests` and `/admin/static-export` protected, `GET /api/v1/guide-requests` present). Both
entries have been removed from this file.

## Superseded — the 2026-09-04 taxonomy-node block (resolved; kept only as a pointer)

Ten queued guides (CES/CWR/CEG/ENV prefixes) were blocked with HTTP 422 because those four taxonomy leaves
were missing from `taxonomy.json`. They were added in commit `2d4984a` and are deployed — `CES4702C` and the
rest push normally now. Background: `Tools/REVIEW_QUEUE.md` item 13, `Tools/SOURCES.md` (batch 142).

⚠ The lesson worth keeping: **a guide push for a prefix with no taxonomy leaf fails with 422 even though
`validate_drafts.py` passes**, so check the seed file before drafting a new prefix:
`grep -c '"CES"' PreseMakerRepo.Api/Data/Seed/taxonomy.json`. Adding a node in the admin editor unblocks a
push immediately, but **`taxonomy.json` must be updated too**, or the seed file and the live database drift.

---

## Raise the curriculum-guide `Prerequisites` ceiling from 500 to 1000 characters (added 2026-09-08, Ron's direction)

**Ron's note, 2026-09-08: raise the validation ceiling in the next site publish.**

**Why.** The `prerequisites` field has become the place the guide pipeline puts the warnings a student most
needs before registering — concurrency traps (`*` prerequisites that are required, not optional), exclusion
pairs (*"credit may not be received in both X and Y"*), minimum-grade conditions, competitive-entry GPA
gates, background-screening deadlines for practicum courses, split-family credit differences, and
accreditation warnings. **It is the first thing a queue reader and the guide page show, so it carries more
than a course-number list.**

**500 characters is now a live constraint rather than a generous one.** Recent batches:

| Guide | Length | Batch |
|---|---|---|
| `SCE4320` | **546 — FAILED, needed two trims to 475** | 186 |
| `CLP4110` | 500 (exactly at the limit) | 181 |
| `PHY3220` | 499 | 185 |
| `PHI4633` | 493 | 184 |
| `ENG3010` | 494 | 181 |

⚠ **Nothing has reached production truncated** — `validate_drafts.py` mirrors the server rule and blocks the
push — **but the failure mode is that real warnings get cut to fit**, which is the wrong trade.

### Two places to change, and the second needs a migration

**1. The FluentValidation rule** — `PreseMakerRepo.Api/Validators/PublishValidators.cs`, in
`UpsertCurriculumGuideRequestValidator` (~line 109):

```csharp
RuleFor(x => x.Prerequisites).MaximumLength(1000).When(x => x.Prerequisites is not null);
```

**2. ⚠ The EF Core column** — `PreseMakerRepo.Infrastructure/Data/Configurations/CurriculumGuideConfiguration.cs`
(~line 15):

```csharp
builder.Property(g => g.Prerequisites).HasMaxLength(1000);
```

⚠⚠ **This one needs an EF migration**, unlike the taxonomy entry above:

```powershell
dotnet ef migrations add WidenGuidePrerequisites --project PreseMakerRepo.Infrastructure --startup-project PreseMakerRepo.Api
```

**SQLite will tolerate the widened column without complaint; PostgreSQL will not**, so the migration matters
for the planned provider swap even though nothing breaks today. **Do not change the validator alone** — that
would let a 900-character string past validation and into a 500-character column.

**Deploy with migrations** (i.e. **not** `-SkipMigrations`).

### Also update the client-side mirror

`Tools/validate_drafts.py` hard-codes the same limits so a batch fails locally rather than at the API.
**Change its prerequisites check to 1000 in the same commit**, and update the limits tables in
`Tools/CLAUDE.md` and `.claude/skills/guide/SKILL.md`, which both document 500.

⚠ **Note while you are in that file:** `SKILL.md`'s limits table still says `contact_hours` **0–300**, while
the server has been **0–1500** since the PSAV fix. **Worth correcting in the same pass.**

### After deploy, verify

```powershell
cd Tools
python -c "import json;d=json.load(open('drafts/SCE4320_guide.json',encoding='utf-8'));print(len(d['prerequisites']))"
# then push any guide with a >500-char prerequisites string and confirm no 400
```

**No nginx, systemd or `taxonomy.json` change.**

---

## ✅ DEPLOYED — guide requests and static export (written 2026-09-03; confirmed live 2026-09-11)

Verified: `/request-guide` returns 200, `/admin/guide-requests` and `/admin/static-export` are
login-protected, and `GET /api/v1/guide-requests` requires an admin token (so the endpoint is present).
The `AddGuideRequests` migration is applied. Kept as a record of what the release contained.

| Change | What to verify after deploy |
|---|---|
| **Request a Curriculum Guide** — `/request-guide` page; button on every course page without a guide; `/courses/{ID}/guide` for a course with no guide now redirects to the request form; empty-search message links to it. Stores course, title, school, optional reason/email, hashed IP (`Security:ReporterIpSalt`), 5 per IP per hour (`Repository:GuideRequestRateLimitPerHour`, default 5 — no config change needed). | `https://floridacourserepo.com/request-guide?course=XXX0000` renders; submitting records a request; `/courses/ACG2021C/guide` (has a guide) still renders the guide |
| **Admin → Guide Requests** (`/admin/guide-requests`): ranking by request count, status triage, CSV download; dashboard card with open-request counts. | page loads; the dashboard shows "Curriculum Guides" card |
| **API** — `POST /api/v1/guide-requests` (public), `GET /api/v1/guide-requests?status=open` and `PATCH /api/v1/guide-requests/{id}/status` (admin JWT). New error codes `GUIDE_ALREADY_EXISTS` (409), `GUIDE_REQUEST_NOT_FOUND` (404). | `python Tools\queue_mgr.py import-requests` returns "No open guide requests." (or the list) |
| **Admin → Static Export** (`/admin/static-export`): builds a self-contained static zip of the public site in the background (loopback fetch of `ASPNETCORE_URLS`, i.e. `http://localhost:5000`); files kept in `/var/presemaker-repo/storage/exports/` (created on first run; owned by `presemaker`). | start an export, watch the page refresh, download the zip, unzip locally and open `index.html` |

No nginx or systemd change. `taxonomy.json` is unchanged by this release.

---

## Deployed 2026-09-02 — verified live, entries removed

Kept as a short record so the same ground is not re-covered. All four verified against the live
API and site after Ron's deploy.

| Change | Verification |
|---|---|
| **CJK/CJJ/CJL out of Dentistry** + `TaxonomySeed` re-parenting fix | `/api/v1/courses/CJK0330` → `level1: Criminal Justice` ✅ (had been `DENTISTRY`) |
| **Taxonomy hierarchy repair** — 2 key collisions, 34 re-parentings, new Photography node | `PGY1800C` → `Photography` ✅ (was Plant Pathology under Ornamental/Horticultural Science); `FFP0030C` → `Fire Science` ✅ (was Finance); `SON1000C` → `Medical Imaging And Radiation Therapy` ✅ (was Philosophy); `MVK1111C` → `Music - Applied` ✅ (was Speech Pathology); `HSC1531C` → `Health Sciences/Resources` ✅ (was Mechanical Engineering); `ASL2140C` → `Foreign Language: American Sign Language And Interpreting` ✅ — the `FOREIGN_LANGUAGE__AM` key collision is resolved |
| **386 approved SCNS prefix names** | live: `FFP` = "Fire Fighting & Protection", `CJK` = "Criminal Justice Basic Training (A.A.S or Vocational)", `MVK` = "Applied Music: Keyboard", `SON` = "Sonography" ✅ |
| **PSAV `0 credit hours` badge** | `PRN0090C` guide page shows `120 contact hours` + `PSAV clock-hour`, and **no** credit badge ✅; `ACG2021C` still shows `3 credit hours` + `45 contact hours` ✅ |
| **Guide page `v@Model.Guide.Version` literal** (`Pages/Browse/Guide.cshtml` ~line 48) — Razor treats `@` between two word characters as a literal email character, so the expression was emitted verbatim on all published guide pages. Fixed with explicit `@(...)` parentheses. | Verified 2026-09-02 after Ron's second deploy: `ACG2021C`, `PRN0090C`, and `MSS0804` guide pages all render `v1.0`, and `grep -c 'v@Model'` returns **0** on each ✅ |

⚠ **The taxonomy work only reached production because `deploy-update.ps1` was fixed first.**
Production reads `Taxonomy:ConfigPath = /etc/presemaker-repo/taxonomy.json`, and neither update
script had ever copied the file there — so every taxonomy change since initial deployment had been
a silent no-op, including the CJK fix. Both scripts now `scp` it to `$ETC_DIR` before the restart,
and the PowerShell version validates the JSON and checks for duplicate discipline keys first.
See `Tools/TAXONOMY_HIERARCHY_REPAIR.md`.
