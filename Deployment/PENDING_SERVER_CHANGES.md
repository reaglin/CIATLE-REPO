# Pending server changes

Changes that need a **server redeploy** (`.\Deployment\deploy-update.ps1` from the repo
root) to take effect. Curriculum guide content does *not* belong here — guides publish over
the REST API and need no deploy.

Bundle these into the next deploy, then delete the entry.

## ⚠ BLOCKING NEXT DEPLOY — four taxonomy nodes missing (added 2026-09-04, Ron to handle)

> **Update 2026-09-06 (batch 160):** the block now covers **six** queued courses, not four — `CES4605C` (Steel Design), **`CES3100C` (Structural Analysis)**, `CWR3201C` (Fluid Mechanics), `CWR4202C` (Hydraulics), `CEG3011C` (Soil Mechanics) and **`ENV3001C` (Environmental Engineering)**. **All four missing prefixes — CEG, CES, CWR and ENV — are now represented in the blocked set.** These are ordinary civil engineering courses at 6–9 institutions each, so they sit near the top of the priority queue and are skipped on every batch. `CES4702C` also remains at `status=error` with its draft validated and intact — it needs only a one-line retry once the nodes exist.


> **Update 2026-09-08 (batch 183):** re-confirmed still blocked. `CES4702C` was retried and returned **HTTP 422** again. The cause is now pinned to the seed file directly — `grep -c '"CES"' PreseMakerRepo.Api/Data/Seed/taxonomy.json` returns **0**, as do `CWR`, `CEG` and `ENV`, while `CGN` and `TTE` return 1 (which is why `CGN3501C` could be published in batch 183 and the rest still cannot). **Ten queued rows now sit behind these four prefixes** — `CES3100C`, `CES4605C`, `CES4702C` (status=error), `CWR3201C`, `CWR4202C`, `CEG3011C`, `CEG4801C`, `ENV3001C`, `ENV4351`, `ENV4514C` — **and they are at the HEAD of the priority order**, which is why every batch since has had to reach further down the queue. The grep above is now the standard pre-draft check.

**Ron's note, 2026-09-04: handle and deploy these before the next deployment.**

**Symptom.** Pushing a curriculum guide for a course whose SCNS prefix has no taxonomy leaf fails with
**HTTP 422**, even though `validate_drafts.py` passes. `ExtractCoursePrefix` reads the letters up to the
first digit, looks for a taxonomy leaf with that key, and refuses to create the course when it finds none.
`CES4702C` hit this on 2026-09-04; its draft is written, validated and waiting at `status=error` in
`Tools/queue.csv`.

**Confirmed still missing after the 2026-09-04 deploy** — that release did not include them.

**Scope: 14 queued courses are blocked, not one.** Sweeping every `queued` row in `Tools/queue.csv`
against the 597 three-letter leaf keys in `PreseMakerRepo.Api/Data/Seed/taxonomy.json`:

| Prefix | Queued rows blocked | Suggested node name |
|---|---|---|
| **ENV** | 6 | Environmental Engineering |
| **CWR** | 3 | Civil Engineering: Water Resources |
| **CEG** | 3 | Civil Engineering: Geotechnical |
| **CES** | 2 | Civil Engineering: Structures |

**All four belong to one parent that already exists** — `CIVIL_ENVIRONMENTAL_`
("Civil/Environmental Engineering"), which currently holds `CCE`, `CGN` and `TTE`. Add alongside them:

```json
{ "key": "CEG", "name": "Civil Engineering: Geotechnical" },
{ "key": "CES", "name": "Civil Engineering: Structures" },
{ "key": "CWR", "name": "Civil Engineering: Water Resources" },
{ "key": "ENV", "name": "Environmental Engineering" }
```

**Two routes, and they are not alternatives — do the seed file either way:**

1. **Admin taxonomy editor** (`/admin`, added in `a5d6886`) creates the nodes live with **no redeploy**,
   which unblocks the pushes immediately.
2. **`taxonomy.json` + redeploy.** `TaxonomySeed` is idempotent and runs at startup. **This must happen
   regardless**, or the seed file and the live database drift apart and a future rebuild loses the nodes.

**No EF migration needed** — this is seed data only, so `deploy-update.ps1` with `-SkipMigrations` is fine
unless something else in the same release needs one.

**After deploy, verify and finish the blocked work:**

```powershell
cd Tools
python generate_guide.py --push-draft CES4702C --yes     # should return "Curriculum guide saved."
curl -s https://floridacourserepo.com/api/v1/courses/CES4702C/guide
```

Then the other 12 rows (ENV/CWR/CEG) will push normally as they come up the queue. Full write-up in
`Tools/REVIEW_QUEUE.md` item 13 and `Tools/SOURCES.md` (batch 142 findings).

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

## Pending — written 2026-09-03, not yet deployed

Deploy with **`.\Deployment\deploy-update.ps1` WITHOUT `-SkipMigrations`** — this release adds an
EF migration (`AddGuideRequests`, new `GuideRequests` table).

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
