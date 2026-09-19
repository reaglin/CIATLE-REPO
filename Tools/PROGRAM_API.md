# Programme API — contract for the `Tools/` session

How a **programme** gets onto floridacourserepo.com. Built 2026-09-19 so that adding one stops
needing a redeploy: until then the only way in was `PreseMakerRepo.Api/Data/Seed/programs.json`,
which ships inside the build.

Authored documents live in **`Tools/programs/<slug>.json`**; the pipeline is **`Tools/programs.py`**
(`validate` · `push` · `list` · `show` · `delete`). Server side: `ProgramsController`,
`UpsertProgramRequestValidator`.

⚠ **Not live until the next deploy.** Probe it before relying on it:

```powershell
curl -i -X PUT https://floridacourserepo.com/api/v1/programs/__probe
```

**401** means it is deployed (the endpoint is there and wants an admin token). **404 or 405** means
it is not — stop, and see `Deployment/PENDING_SERVER_CHANGES.md`.

---

## Start here

```powershell
cd Tools
python programs.py validate                  # every document in programs/
python programs.py validate nursing          # or just one
python programs.py push nursing              # WRITES to the live site; shows what changes, then asks
python programs.py push --all --yes          # no confirmation -- know what you are sending
python programs.py list [--include-drafts]   # what is live, with school counts
python programs.py show nursing [--schools]  # what its codes actually found
python programs.py delete nursing [--yes]    # asks first; refused 409 while a path names it
```

- **`programs/<slug>.json` IS the PUT body**, and the **filename is the slug** — no `slug` key goes
  inside the file.
- Credentials are `REPO_ADMIN_EMAIL` and `REPO_ADMIN_PASSWORD` in **`Tools/.env`**, which the script
  loads by itself.
- **To rehearse without touching production:** `$env:REPO_BASE_URL='http://localhost:5199'` (unset
  means the live site).
- `validate` checks the CIP codes against `PreseMakerRepo.Api/Data/Seed/cip.json`, so an unknown code
  is caught here rather than by a refused push.

---

## What a programme is

Ron, 2026-09-17: *"a major that supports a career path and is being offered by a Florida school…
Nursing AS (the major) = Nursing (the program) and Nursing BSN (the major) = Nursing (the program).
Nursing programs will encompass nursing degrees."*

**So a programme sits one level ABOVE a degree** and spans as many CIP codes as that takes.

⚠⚠ **A programme owns no school list.** Ron: *"I am going to decouple programs from schools."*
Which institutions offer it is derived from the federal IPEDS award table by CIP prefix, every time
a page is read, and is stored nowhere. **The codes you claim ARE the school list** — which is why
each one carries a `note` holding the evidence for it.

⚠⚠⚠ **The measurement that settles how wide to go.** Nursing defined as `51.38` alone finds 39
Florida public institutions; adding `51.39` (practical nursing) finds **78** — and every one of the
39 it was missing is a **technical college**. Ron: *"If a school has an LPN degree, they have a
nursing program… I do not want a school to be excluded from being listed because their offerings
are limited."*

## Authentication

Same as every other pipeline: `POST /api/v1/auth/login` with `REPO_ADMIN_EMAIL` /
`REPO_ADMIN_PASSWORD` → `data.accessToken`, sent as `Authorization: Bearer <token>`. Reads need no
token. All responses use the site envelope: `{ "success": true, "data": …, "error": null }`.

---

## `PUT /api/v1/programs/{slug}` — create or replace (admin)

```json
{
  "name": "Nursing",
  "description": "One paragraph. What the programme is and what studying it involves.",
  "degreesNote": "The degrees it encompasses — certificate, A.S., BSN — and what each leads to.",
  "bodyHtml": "<p>Optional longer prose. Sanitized on save: structure and links only.</p>",
  "isPublished": true,
  "sortOrder": 10,
  "cips": [
    { "cipCode": "51.38", "note": "Registered nursing — the A.S. and BSN routes to RN licensure." },
    { "cipCode": "51.39", "note": "Practical nursing. ⚠ Included deliberately: a school with only an LPN programme has a nursing programme." }
  ]
}
```

**The CIP codes are replaced wholesale**, so a push is idempotent and a code dropped from the
document stops counting schools.

### Rules the server enforces

| Rule | Detail |
|---|---|
| `slug` | lowercase words separated by hyphens; taken from the URL, not the body |
| `name` | required, ≤ 200 |
| `description` | required, ≤ 2000 |
| `degreesNote` | optional, ≤ 2000 |
| `bodyHtml` | optional; sanitized to the same allow-list as career paths (no scripts, no styling) |
| `cips` | **required, ≥ 1**, ≤ 40, no duplicates |
| `cipCode` shape | a **whole level only**: a series (`15` or `15.`), a group (`51.38`), or one 6-digit code (`14.1901`) |
| `cipCode` existence | must be in the seeded CIP tree; a 6-digit code is checked against its 4-digit group |
| `note` | optional, ≤ 500 — but write it: it is the evidence for claiming the code |

⚠⚠ **Why part-codes are refused.** Codes are matched with `StartsWith`, so `14.1` would sweep in
14.10 through 14.19 — electrical engineering along with mechanical. Anything that is not a whole
level of the tree comes back 400.

### Responses

| Code | Meaning |
|---|---|
| 200 | `{ slug, outcome: "created"\|"updated", cipCount, schoolCount, unmatchedCips }` |
| 400 | `VALIDATION_ERROR` — shape; `fields` names the offending entry |
| 422 | `CIP_NODE_NOT_FOUND` — a code is not in the seeded tree. Widen it (`Tools/build_cip_seed.py`, `EXTRA_GROUPS`) with the reason recorded, and **that needs a deploy** |
| 422 | `VALIDATION_ERROR` — the same code listed twice |
| 401 / 403 | not an admin |

⚠ **`unmatchedCips` is a warning, not an error:** a code can be real and simply have no Florida
completions in the award year. But a code matching nothing usually means the wrong code — check it,
because the page will show it finding no schools.

## `GET /api/v1/programs` — published programmes

`?includeUnpublished=true` adds drafts and requires an admin token (403 otherwise). Each row:
`slug, name, description, schoolCount, cipCount, careerPathCount, isPublished, updatedUtc`.

## `GET /api/v1/programs/{slug}` — one programme

Adds `cips` (each with its CIP title and its own school count), `schools` (unit id, name, our
institution code where we know it, award levels, completions), `awardLevels`, `awardYear`, and the
`careerPaths` that name it. ⚠ Schools are ordered **by name, never by completions** — the counts are
shown but must not rank one school above another.

## `DELETE /api/v1/programs/{slug}` (admin)

**409 `PROGRAM_IN_USE`** while a career path names the programme — the message lists the paths.
Remove it from their documents, push those, then delete. 404 if there is no such programme.

⚠ **This removes a live public page.** `programs.py delete` shows what is about to go (name, CIP
count, school count, the paths that name it) and asks before sending; `--yes` skips the question.
The local `programs/<slug>.json` is untouched, so `push <slug>` brings the programme back — **but a
programme that was only ever authored on the server has no local copy**, and the CLI says so.

---

## How this interacts with the seed

`Data/Seed/programs.json` **bootstraps a fresh database and nothing more**: on startup a programme
that already exists is left alone (the log says *"N added, M left to the API"*). So:

- **To correct a live programme: push it.** Editing the seed file changes nothing that already exists.
- **To reset one to the seed: delete it, then restart the site.** ⚠ Only do this for a programme
  that is actually in `programs.json`; anything else simply disappears.
- The five original programmes were exported to `Tools/programs/` on 2026-09-19, so the documents and
  the seed file agree today. **If you change one, change it in `Tools/programs/` and push.**

## Order of work

⚠ A career path names its programmes by slug (`programs: [{slug, note}]` in the path document) and
the path push is **refused 422** for an unknown slug — so **push the programme before the path**.
