# Pending server changes

Changes that need a **server redeploy** (`.\Deployment\deploy-update.ps1` from the repo
root) to take effect. Curriculum guide content does *not* belong here — guides publish over
the REST API and need no deploy.

Bundle these into the next deploy, then delete the entry.

## Open entries

The course catalog work (`COURSE_CATALOG_PLAN.md` phases 1–4b) is live — see the record below.

**⚠ WRITTEN AND AWAITING DEPLOY — the `Prerequisites` ceiling raise (500 → 1000).** Ron, 2026-09-11: *"The
500 character prerequisite ceiling is blocking a lot of the guides."* Validator, EF column and the
`Tools/validate_drafts.py` mirror all moved to 1000, with migration `WidenGuidePrerequisites`. **Deploy
without `-SkipMigrations`** (the migration is empty on SQLite — see the comment in it — but must be applied
so the recorded schema stays honest). Details in the entry below.

**Still open, not written yet:** the **`offering_notes`** field on guides and the **field sizing** items the
`Tools/` session raised on 2026-09-11 (both below). They touch the same validator, so they should ship
together — after tonight's deploy.

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

## ⚠ WRITTEN 2026-09-11, AWAITING DEPLOY — raise the guide `Prerequisites` ceiling from 500 to 1000

**Ron's note, 2026-09-08: raise the validation ceiling in the next site publish.** Escalated 2026-09-11: the
ceiling is blocking guides, so this was written and is ready to deploy on its own.

**What changed** (all in one commit): `PublishValidators.cs` → `MaximumLength(1000)`;
`CurriculumGuideConfiguration.cs` → `HasMaxLength(1000)`; migration **`WidenGuidePrerequisites`** (empty on
SQLite by design — TEXT has no declared width — but it carries the width into the model snapshot so a future
PostgreSQL swap does not narrow the column; the reasoning is in the migration file); `Tools/validate_drafts.py`
→ `MAX_PREREQ = 1000`; limits tables corrected in `Tools/CLAUDE.md`,
`Tools/Generate_Guides_and_Push_Process.md` and `.claude/skills/guide/SKILL.md` (whose stale
`contact_hours 0–300` note was fixed too).

**Deploy without `-SkipMigrations`.** After deploy, push a guide whose `prerequisites` runs past 500
characters and confirm it does not come back 400 — `SCE4320` is the known case that needed two trims.

**The original write-up follows.**

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

## Curriculum guides: carry the new `offering_notes` field (Ron, 2026-09-11)

**Ron's direction:** the guides gain **an additional field** holding, per school, **the title that school
uses for the course and the hours it requires** — so a reader can resolve "3 credits at which institution?"
without leaving the guide. **Credit hours are integers.** Rationale in his words: *"Now I am collecting from
users the information that they find useful in the guides."*

**The `Tools/` session is already emitting it.** Batch 190's six `CET` drafts carry `offering_notes`, and
`validate_drafts.py` enforces its shape (including the integer-credits rule). `PUT /api/v1/courses/{id}/guide`
builds its payload from the six named scalars, so **the field is silently dropped today** — drafts publish
fine, the data just does not reach the site. Nothing is broken; the field is simply invisible until this
lands.

### The shape being sent

```json
"offering_notes": {
  "summary": "All five institutions carry it at 3 credits. No institution publishes a contact-hour figure.",
  "hours_source": "derived",              // published | derived | mixed
  "derived_contact_hours": 60,
  "derivation": "Florida convention: 45 hours for a 3-credit lecture course, 60 for a 3-credit C course.",
  "offerings": [
    { "institution": "GCSC", "institution_name": "Gulf Coast State College",
      "title": "Digital and Computer Circuits", "credits": 3, "contact_hours": null,
      "note": "Offered spring term only. Prerequisite MAC1105 and EET1084C, minimum grade C." }
  ]
}
```

### ⚠⚠ Before building it: the per-school rows already exist in the database

**`CourseOffering` (added in this release) already stores exactly this data** — `InstitutionCode`,
`InstitutionTitle`, `Credits`, `ClockHours` — fed by `offerings[]` on the course API. **Storing the same
rows again on the guide would create two sources of truth that drift**, which is the failure this project
has spent months cleaning up elsewhere.

**Recommended split, and it is cheaper than a new table:**

| Part | Where it should live | Why |
|---|---|---|
| Per-school **title, credits, clock hours** | **`CourseOffering`** (already there) | already populated by the course API; one writer |
| **`summary`**, **`hours_source`**, **`derived_contact_hours`**, **`derivation`**, per-school **`note`** | **new on `CurriculumGuide`** | interpretation, not data — no structured source for it |

So the server work is: **one nullable `OfferingNotes` column** (JSON text, suggest ≤ 8000 chars) on
`CurriculumGuide`, accepted by the guide upsert and rendered on the guide page **joined against the course's
existing `CourseOffering` rows**. The per-school `note` is the only per-row item with nowhere to go — either
fold it into the JSON keyed by institution code (simplest) or add a `Note` column to `CourseOffering`.

⚠ **If the simpler path is preferred**, storing the whole blob as sent and rendering it verbatim also works
and needs no join — but then a course's offerings can disagree with its guide's offerings, and someone will
have to reconcile them later.

### ✅ Both questions ANSWERED by Ron, 2026-09-11 — and the split design above is APPROVED

1. **Variable-credit courses — the note is sufficient.** No `credits_min`/`credits_max` pair. A row with a
   genuine in-school range sends `credits: null` and explains it in `note` ("Variable credit: 1 to 4 at this
   institution"). **So `credits` is a plain nullable integer column/property** — nothing further needed.
2. **`Institution.Sector` is the OWNER of the sector fact** (Ron, 2026-09-11). The guide JSON does **not**
   carry a `sector` field — offering rows carry the institution code and **the page joins to `Institution`**.
   One writer, one source of truth. The `Tools/` session has removed its copy.

3. **Public institutions only** (Ron, 2026-09-11, refining his earlier answer): *"In doing search and fetch
   to determine eligibility for a curriculum guide we will only do public institutions… we are not adding
   private institutions as part of our adding data."* So the `Tools/` session sends **FCS and SUS offerings
   only**; a private, career or out-of-state institution carrying an SCNS number is not added.

   ⚠ **Server-side implication: none required, but worth knowing.** A course's `OfferingCount` and its
   "Offered at N Florida institutions" panel will therefore count **public institutions only**, which is the
   intended reading. **No filtering belongs on the server** — the content session decides what a course is,
   per principle 1 of `COURSE_CATALOG_PLAN.md`.

   ⚠ **A visitor request overrides the rule**, applied by queueing that course rather than by widening the
   filter. The one live instance, `CET1112` (carried only by a private career college), **was a test click
   by Ron and is being withdrawn** — its draft is deleted and it is removed from the local queue. **Its
   request is still Open on `/queue/guides` and should be set to `Declined`** via
   `PATCH /api/v1/guide-requests/CET1112/status`, or it will sit in the public queue unfillable.

### Not now

**Existing guides do not carry the field**, and Ron has said the retro-fit is *"a task for much later."*
2,197 live guides would need it. **Do not schedule it with this change** — the column is nullable and a guide
without it renders exactly as it does today.

---

## Field sizing — align the guide and course ceilings, and the 133 clock-hour rows (from the `Tools/` session, 2026-09-11)

**Raised by the content session after reading the course-catalog release.** Three sizing items, one of
which **blocks the Engineering Technology guide work that Ron's 2026-09-09 prefix direction points at**.

### 1. ⚠⚠ 133 courses hold CLOCK HOURS in `creditHours`, and the new ceiling rejects them

Measured live 2026-09-11 against `GET /api/v1/courses/catalog?hasGuide=false&pageSize=1000`:

| | |
|---|---|
| Guide-less courses on the site | **806** (all Engineering Technology prefixes) |
| Of those, `creditHours` **> 20** | **133** — values run to **667** |
| Of those 133, PSAV `0xxx` courses | **132** (the exception is `ETI2941`, a practicum, credits `30`) |
| Courses with `contactHours` set | **0 of 806** |
| `creditHours` between 13 and 20 | **0** |

Worst rows: `EEV0940` 667, `TDR0780C` 470, `EEV0142` / `ETI0304` / `ETI0459` / `ETI0473` / `TDR0301` /
`TDR0302` 450. By prefix: TDR 40, ETI 31, EEV 30, ETP 18, EER 9, ETC 3, ETM 2.

⚠ **This is the PSAV clock-hours-as-credits mistake, already in production data** — the same error the guide
pipeline guards against with `credits: 0` + `contact_hours`. It predates the catalog release (all 806 rows
carry `source: Guide`, created as side effects of old pushes).

**Why it needs a decision rather than just a fix:** `UpsertCourseRequestValidator` caps `CreditHours` at
**20**, so **the content session cannot refresh any of those 133 rows through `PUT /api/v1/courses/{id}`
without first correcting the value** — a round-trip read-modify-write of the site's own data fails
validation. The values are also plainly wrong on the public course pages today.

**Recommendation (cheapest path, no migration):** the `Tools/` session corrects them over the API as it
works each prefix — `creditHours: 0`, `contactHours: <the clock hours>` — since it has to touch every one of
these courses anyway to add titles and offerings. **No server change required for this item**, but the site
session should know the rows exist and that the ceiling is what surfaces them. If a bulk fix is preferred
instead, a one-off migration moving `CreditHours > 20` into `ContactHours` and zeroing credits would clear
132 of the 133 correctly (`ETI2941` needs a human look — a practicum at 30 is more likely hours than credits
but is not a `0xxx` course).

### 2. The guide and course validators disagree about the same two fields

| Field | Guide (`UpsertCurriculumGuideRequestValidator`) | Course (`UpsertCourseRequestValidator`) |
|---|---|---|
| credits | **0–12** | **0–20** |
| contact hours | **0–1500** | **0–3000** |

A course record can legitimately hold 20 credits while its own guide is rejected at 13. Nothing has hit this
yet — there are **zero** rows in the 13–20 band — so it is a latent inconsistency, not a live failure.

**Recommendation:** make the guide ceilings match the course ceilings (**0–20** and **0–3000**). Both
comments in the source already say the ceiling is "a sanity guard against typos, not a course-length
policy", and a single number is easier to mirror in `validate_drafts.py` than two.

### 3. The `Prerequisites` 500 → 1000 raise is still the only open entry

Reaffirmed from the content side: `PublishValidators.cs:109` is still `MaximumLength(500)`. The entry above
has the full rationale and both code sites. **Recommend bundling items 2 and 3 into the same release** — they
are two adjacent lines in the same validator, and item 3 needs a migration that item 2 does not.

### Sizing items that are correctly sized (checked, no action)

`title` / `stateTitle` ≤ 300 (longest Florida course title seen is well under), `offerings[]` ≤ 250 per
course (Florida has ~40 public institutions), resource `summary` ≤ 2000, institution `code` ≤ 10,
`name` ≤ 200.

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
