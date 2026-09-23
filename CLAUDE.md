# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development plan

**[`docs/DEVELOPMENT-PLAN.md`](docs/DEVELOPMENT-PLAN.md) is the plan — start there.** It carries the
phases, what is done, what is waiting on Ron, and the open questions, following the portfolio rules
in the parent `repos/CLAUDE.md` (**"Every project: `docs/DEVELOPMENT-PLAN.md`"**): phases of numbered
tasks; no icon/⬜ = to do, ⚠️ = action needed (awaiting Ron's verification, or returned with a
comment), ✅ = verified by Ron — never marked by Claude. Update it in the same commit as the work.

The plan covers **the site and its APIs**. Guide *content* status stays with the `Tools/` session
(`Tools/NEXT_SESSION.md`, `Tools/SOURCES.md`, `Tools/REVIEW_QUEUE.md`); the design documents it
draws on (`CAREER_PATHS_PLAN.md`, `COURSE_CATALOG_PLAN.md`) are listed in its References section.

## Project Overview

**PreseMaker Community Repository** — a publicly browsable, contributor-maintained library of course materials organized by a configurable hierarchical taxonomy (Florida SCNS by default). It exposes a REST API for the PreseMaker desktop client, a Razor Pages web frontend for browsing, and an admin console for moderation.

**Current Status:** Implemented and **live in production** at
[floridacourserepo.com](https://floridacourserepo.com) — the Florida Course Repository. The
three-project solution exists and is deployed: **40,630 courses, 2,504 curriculum guides, 84 career
paths and 90 programmes** are live as of 2026-09-23. ⚠ **Browse reaches only 39,982 of those
courses** — 648 art courses (`ARH`, `ARE`, `ART`) sit in the catalog under a discipline node that a
key collision knocked out of the tree. Fixed in the repo, **awaiting a deploy**:
`docs/DEVELOPMENT-PLAN.md` item 1.5.

**What is being worked on now: career paths, second queue.** The original 50 rows are complete —
**47 published paths covering 71 occupations** across engineering, manufacturing/CTE, health,
computing, business, law, education and public service. A **second 50 rows** were added on
2026-09-21 (`Tools/career_paths/QUEUE.csv`, ranks 101–150), chosen from the largest Florida
IPEDS footprints the site does not yet cover: health (16), business (8), a new creative and
media cluster (7), science (4), social services (3), and the service and transport careers the
first queue missed. **23 of the 50 are CHOICE paths.** ⚠ Six rows are blocked on a CIP seed
widening (a deploy) — `REVIEW_QUEUE.md` item 116; the other 44 can be worked today.
**After this queue, career paths move to REQUEST-DRIVEN, the same as courses.** Guide writing is
already request-only. Both loops run from the `Tools/` session; neither needs a deploy.

## Solution Structure

| Project | Purpose |
|---|---|
| `PreseMakerRepo.Api` | ASP.NET Core host: controllers, Razor pages, admin console |
| `PreseMakerRepo.Core` | Domain models, enums, interfaces — no infrastructure dependencies |
| `PreseMakerRepo.Infrastructure` | EF Core, file storage, email, JWT, services |
| **`Tools/`** | **Content pipeline — how new courses and curriculum guides get published to floridacourserepo.com.** Not part of the server build. |
| `Deployment/` | Server deploy scripts (`deploy-update.ps1` — prefer over the `.sh`; `bash` is not on PATH on this machine) |
| **`FEATURE_BACKLOG.md`** | **Queued ideas for future website releases.** Capture list only — nothing there is started or scheduled. Add items here as they come up; distinct from `Deployment/PENDING_SERVER_CHANGES.md`, which holds code already written and awaiting deploy. |

URL namespaces: `/api/v1/` (REST), `/browse/` (web frontend), `/admin/` (admin console).

## Publishing curriculum guides — `Tools/`

`Tools/` is the toolchain for **deploying new courses and their curriculum guides to
floridacourserepo.com**. It is content tooling, not server code: guides go over the REST API,
so publishing a guide needs no redeploy.

**Start at [`Tools/Generate_Guides_and_Push_Process.md`](Tools/Generate_Guides_and_Push_Process.md)** —
the end-to-end process (prioritize → generate → validate → push → verify). Supporting docs:
`Tools/CLAUDE.md` (guide content standards), `Tools/QUEUE_GUIDE.md` (queue schema),
`Tools/README.md` (per-tool reference).

The `/guide` skill (`.claude/skills/guide/SKILL.md`) drives this loop in a Claude Code session.

**Demand-driven queue (2026-09-03):** visitors request missing guides at `/request-guide`
(course, title, school, optional reason/email; rate-limited, hashed IP). Admins rank and triage
them at `/admin/guide-requests`; `python queue_mgr.py import-requests [--mark-queued]` pulls
the open requests into `queue.csv` ahead of catalog-derived rows (`Tools/QUEUE_GUIDE.md`).
API: `GuideRequestsController`; logic: `Api/Services/GuideRequestService.cs`.

**Major update planned (2026-09-11): [`COURSE_CATALOG_PLAN.md`](COURSE_CATALOG_PLAN.md).** Every course
that exists is listed, with or without a guide; guides are generated **on request** (one-click Request
Guide, public queue); each course gets **Course Resources** (website / YouTube links, public AI-reviewed
queue); the main page offers Courses · Programs (soon) · Career Paths (soon). **Split of work:** this
(root) session builds the site and the course API; the `Tools/` session adds courses — with or without
guides — by Ron's rules, over that API. Start there when building.

## Career paths and programmes — also content, also over the API

Three content pipelines now publish to the live site over the REST API, and **none of them needs a
redeploy**:

| Content | Documents | Pipeline | Contract |
|---|---|---|---|
| Curriculum guides | `Tools/drafts/` | `generate_guide.py` | `Tools/Generate_Guides_and_Push_Process.md` |
| Career paths | `Tools/career_paths/*.json` | `Tools/career_paths.py` | `CAREER_PATHS_PLAN.md` §0 |
| Programmes | `Tools/programs/*.json` | `Tools/programs.py` | `Tools/PROGRAM_API.md` |

⚠ **Order matters:** a career path names its programmes by slug and is refused 422 for an unknown
one, so **push the programme first**. A path is also refused if its CIP code is not in the seeded
tree — and widening `Data/Seed/cip.json` **is** a deploy.

⚠⚠ **`Data/Seed/programs.json` bootstraps a fresh database and nothing more** (2026-09-19). A
programme that already exists is left alone at startup, so editing the seed file changes nothing
live; to correct a programme, push it. Which schools offer a programme is never stored — it is
derived from the IPEDS award table by CIP prefix at read time.

**Static site export:** `/admin/static-export` builds a self-contained static zip of the public
site (browse tree, courses, guides) by fetching the live pages over loopback and rewriting links
(`Api/Services/StaticSiteExporter.cs`, background `StaticExportJobService`); the zips stay in
`{Storage:RootPath}/exports/` as backups.

```powershell
cd Tools
python queue_mgr.py next-batch --n 5              # prioritize
                                                  # draft to drafts/{ID}_guide.json
python validate_drafts.py --drafted               # preflight (mirrors server validators)
python queue_mgr.py reconcile
python generate_guide.py --push-from-queue --yes  # push to the live site
```

## Build & Run Commands

```bash
# Build
dotnet build

# Run (development)
dotnet run --project CIATLE-REPO

# Watch mode
dotnet watch --project CIATLE-REPO

# Run tests (when test projects exist)
dotnet test
dotnet test --filter "FullyQualifiedName~SomeTestClass"

# Publish for Linux VPS
dotnet publish -c Release -r linux-x64 --self-contained false

# EF Core migrations
dotnet ef migrations add <MigrationName> --project PreseMakerRepo.Infrastructure --startup-project PreseMakerRepo.Api
dotnet ef database update --project PreseMakerRepo.Infrastructure --startup-project PreseMakerRepo.Api
```

## Where this project is going — career pathways

**Ron, 2026-09-04.** The curriculum guides are the foundation, not the destination. **The intended
direction is to take a profession — law, nursing, engineering, accounting — and trace an educational
path to it: which courses, in what order, at which institutions.**

**✅ BUILT AND LIVE since 2026-09-17, and it is the ACTIVE WORK.** The platform (`CareerPath`,
routes JSON, the programme link table, `/careers` pages, the admin API and the `Tools/career_paths/`
pipeline) is in production; what remains is **content** — authoring the remaining paths in
`Tools/career_paths/QUEUE.csv`, which is the `Tools/` session's job and needs no deploy.
**[`CAREER_PATHS_PLAN.md`](CAREER_PATHS_PLAN.md) §0** is the contract; phases and status are in
[`docs/DEVELOPMENT-PLAN.md`](docs/DEVELOPMENT-PLAN.md).

**⚠ The guides did not stop being the foundation.** 2,504 of them are live and serving students
today, and every path is assembled out of what they established.

### What the guides are already accumulating toward it

Each guide carries material the pathway layer will need, which is why these sections are written the way
they are:

- **Career Pathways** — named occupations with **SOC codes**, and named Florida employers.
- **Prerequisites** — captured verbatim from each institution, including grade conditions, concurrency
  notation, and co-requisite blocks. **This is the raw graph of what must precede what.**
- **Position in the curriculum** — where a course sits in a sequence, and what it gates.
- **Licensure and certification** — the terminal requirement a pathway aims at: NCLEX-RN and the Florida
  Board of Nursing, ASCP certification plus Florida clinical laboratory licensure, the FE exam and PE
  licensure, NAACLS and CCNE/ACEN programme accreditation.
- **Transfer and articulation notes** — where credit moves between institutions and where it does not.

### ⚠ What the build has already learned that a pathway feature must handle

These are not hypotheticals; every one is documented in `Tools/SOURCES.md`:

1. **A course number does not identify a course.** The same SCNS number can carry **two different
   subjects** at different institutions (`NUR4286`, `NUR4826`) — hence the `-SCNS` / `-<INST>` split.
2. **Suffixes are filing decisions, not descriptions.** An `L` can be a hospital rotation; a `C` can be a
   separate programme track. **A pathway built by parsing course codes will be wrong.**
3. **Institutions run parallel routes through the same subject** — pre-licensure versus degree-completion
   in nursing, standard versus Professional Track in medical laboratory sciences. **A pathway must know
   which route a student is on**, because a degree-completion route does not lead to initial licensure.
4. **Programmatic accreditation frequently outranks course credit.** Eligibility to sit NCLEX-RN or ASCP
   certification depends on completing an *approved programme* — **so a pathway assembled from
   individually transferable courses can still fail to qualify anyone.**
5. **Prerequisite chains are cohort-locked.** In nursing and MLS, one failed course delays an entire
   block by a year, not a term.

**The honest implication: a naive "take these courses in this order" pathway would mislead students.**
The value is in encoding the constraints above, which is precisely what the guides have been recording.

## Technology Stack

- **Runtime:** .NET 8, ASP.NET Core 8
- **ORM:** Entity Framework Core 8 (code-first)
- **Database:** SQLite (initial) → PostgreSQL via config swap (`DatabaseProvider` setting)
- **Auth:** ASP.NET Core Identity + JWT Bearer (policy scheme: JWT for `/api/*`, cookies for web pages)
- **File Storage:** Local filesystem, abstracted via `IStorageService` (future: Azure Blob / Backblaze)
- **Email:** MailKit via SMTP
- **Validation:** FluentValidation on all DTOs
- **Logging:** Serilog (file + console)
- **Deployment:** Nginx + systemd on Ubuntu 22.04/24.04 LTS

## Domain Model

**Content Hierarchy:** `TaxonomyCourse` → `Module` → `Material` (each independently publishable).

**Taxonomy:** Three-level tree (`TaxonomyNode`): Discipline → Subdiscipline → Prefix/Subject. Leaf nodes link to `TaxonomyCourse` records. Loaded from `taxonomy.json` at startup via an idempotent `TaxonomySeed` service. Two built-in orphan containers are always created:
- `_ORPHAN_COURSE` — modules with no Level 3 taxonomy match
- `_ORPHAN_MODULE` (`WellKnownIds.OrphanModuleId`) — materials with no module match

**Key Entities:**
- `Contributor` — extends `IdentityUser`; adds display name, institution, EDU verification, suspension status
- `Module` — GUID PK; has JSON columns for `Outcomes` and topic hierarchy; `ContentStatus` enum (Published/Flagged/Removed)
- `Material` — GUID PK; `MaterialType` enum (10 types); filename stored as-is for `Content-Disposition`, actual path is GUID-prefixed
- `ContentFlag` — exactly one of `ModuleId`/`MaterialId` set; reporter IP stored as SHA-256 hash (never raw)
- `RefreshToken` — single-use rotation; token stored as SHA-256 hash; all invalidated on password change
- `EduInstitution` — email domain lookup for institution attribution on contributor profiles

**Enums:** `MaterialType` (10 values), `LicenseType` (4 CC options), `ContentStatus`.

## Authentication & Authorization

- Access tokens: 60-min JWT; refresh tokens: 30-day, single-use rotation
- Policies: `ContributorOnly`, `AdminOnly`, `OwnerOrAdmin`
- Email confirmation required before first publish
- Admin bootstrap: on first startup with no Administrator role, reads `AdminBootstrap` config (email/username/password from env vars) and creates/promotes the account — idempotent

## File Storage Layout

```
/var/presemaker-repo/storage/
  modules/{module-guid}/
    manifest.json          # Disaster recovery metadata
    materials/{material-guid}_{original-filename}
```

- ZIPs assembled on-demand; temp file used for assemblies > 100 MB
- Size limits: 500 MB/module, 200 MB/material
- Original filename never used as a storage path — always GUID-prefixed

## Configuration

All secrets come from environment variables (never appsettings):

| Env Var | Purpose |
|---|---|
| `ConnectionStrings__DefaultConnection` | DB connection string |
| `Jwt__SecretKey` | 256-bit JWT signing key |
| `Email__SmtpPassword` | SMTP credential |
| `AdminBootstrap__Email/Username/Password` | First-run admin account |

Key appsettings sections: `DatabaseProvider`, `Jwt`, `Storage`, `Email`, `Taxonomy`, `Repository` (page sizes, report rate limit, recent modules count).

## API Response Envelope

All REST responses use:
```json
{ "success": true, "data": { ... }, "error": null }
{ "success": false, "data": null, "error": { "code": "ERROR_CODE", "message": "...", "fields": {} } }
```

27 distinct error codes are defined in the API spec (`Specifications/PreseMaker_Repository_API_Specification.md`).

## Security Constraints

- Reporter IP addresses: SHA-256 hashed with salt — never stored raw
- File uploads: MIME type validated, size checked, stored with GUID prefix — original filename never used as path, never executed server-side
- Rate limits: 5 reports/IP/hour; 10 login failures/IP/15 min (temp lockout)
- CORS: restricted to repository domain; PreseMaker client uses `HttpClient`, not browser CORS

## Phase 2 Hooks (Deferred — do not implement in Phase 1)

`IStorageService` abstraction is already planned to allow blob storage migration. `TaxonomyCourse.IsActive` and nullable `Level3Key` are reserved for non-taxonomy courses. Material versioning (`MaterialVersion` table) is planned but not in scope.

## Specifications

All three spec files in `Specifications/` are authoritative for Phase 1 scope:
- `PreseMaker_Repository_Requirements.md` — functional requirements and user roles
- `PreseMaker_Repository_API_Specification.md` — full REST API contract with request/response shapes
- `PreseMaker_Repository_DesignSpec.md` — implementation design: schema, auth flow, storage, deployment, admin console
