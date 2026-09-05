# Pending server changes

Changes that need a **server redeploy** (`.\Deployment\deploy-update.ps1` from the repo
root) to take effect. Curriculum guide content does *not* belong here — guides publish over
the REST API and need no deploy.

Bundle these into the next deploy, then delete the entry.

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
