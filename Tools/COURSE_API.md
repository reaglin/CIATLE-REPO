# Course catalog API — contract for the `Tools/` session

**For the content session** (started in `Tools/`, governed by `Tools/CLAUDE.md`). This is how courses —
**with or without a curriculum guide** — get onto floridacourserepo.com. The site stores and displays what
it is sent; **which courses exist, and which get guides, is decided here in `Tools/` by Ron's rules.**

Server side: `COURSE_CATALOG_PLAN.md` (repo root), phase 1. Built 2026-09-11 on branch
`feature/course-catalog`. **These endpoints are not live until that branch is deployed** — check
`GET /api/v1/courses/catalog?pageSize=1` returns 200 before relying on them.

---

## What the site does with a course

- A course is listed on its prefix page with **View Guide** (guide published) or **Request Guide** (no guide).
- Its page `/courses/{id}` shows the title, credits / contact hours, the statewide title where it differs,
  and **"Offered at N Florida institutions"** with each school's own title and credits.
- Course pages with no guide and no materials are marked `noindex` (thin pages stay out of search engines).
- A course is **listed** while it is active, or while it has a guide or published modules.

## Authentication

Same as `generate_guide.py`: `POST /api/v1/auth/login` with `REPO_ADMIN_EMAIL` / `REPO_ADMIN_PASSWORD`
→ `data.accessToken`, sent as `Authorization: Bearer <token>`. Tokens last 60 minutes — log in again for
long runs. Read endpoints need no token.

All responses use the site envelope: `{ "success": true, "data": …, "error": null }`.

---

## Write endpoints (admin)

### `POST /api/v1/courses/batch` — the normal way to add or refresh courses

Up to **500** courses per call. Each item is validated on its own: a bad row fails alone and the rest are
saved together.

```json
{ "courses": [
  { "courseId": "EEE3300",
    "title": "Electronics I",
    "stateTitle": "ELECTRONICS I",
    "creditHours": 3,
    "contactHours": null,
    "taxonomyKey": null,
    "isActive": true,
    "offerings": [
      { "institution": "UCF", "title": "ELECTRONICS I",         "credits": 3 },
      { "institution": "FIU", "title": "ELECTRONIC CIRCUITS I", "credits": 3, "clockHours": null, "isActive": true }
    ],
    "replaceOfferings": true }
] }
```

Response `200`:

```json
{ "success": true, "data": {
  "created": 1, "updated": 0, "unchanged": 0, "failed": 1,
  "results": [
    { "courseId": "EEE3300", "outcome": "created", "taxonomyKey": "EEE" },
    { "courseId": "ZZZ1234", "outcome": "failed", "taxonomyKey": null,
      "errorCode": "TAXONOMY_PLACEMENT_REQUIRED", "message": "No taxonomy node matches the prefix of ZZZ1234. Specify the node via 'taxonomyKey'." }
  ] }, "error": null }
```

`outcome` is `created` · `updated` · `unchanged` · `failed`. **Re-sending identical data returns
`unchanged` and writes nothing**, so refresh runs are safe to repeat.

### `PUT /api/v1/courses/{courseId}` — one course

Same body as a batch item (`courseId` optional; must match the URL if given). `201` created · `200`
updated/unchanged · `400` validation · `422` taxonomy placement.

### `DELETE /api/v1/courses/{courseId}` — a course added in error

`200` deleted · `404` not found · **`409 COURSE_HAS_CONTENT`** when it has a guide (or module stub),
modules, or guide requests. For a course that has **stopped being offered**, send `isActive: false` instead.

### `POST /api/v1/institutions/batch` · `PUT /api/v1/institutions/{code}`

```json
{ "institutions": [ { "code": "UCF", "name": "University of Central Florida", "sector": "SUS", "scnsId": "22" } ] }
```

Up to 1,000 per call. An offering naming an unknown code creates a code-only institution, so order does not
matter — but **send names** (SCNS `institution_map()`), or the site shows bare codes.

---

## Field rules

| Field | Rule |
|---|---|
| `courseId` | `^[A-Z]{3}\d{4}[A-Z]?(-(SCNS|[A-Z]{2,5}))?$` after removing spaces and uppercasing — `EEE3300`, `EEE3300L`, `NUR4826-UWF` |
| `title` | **required**, ≤ 300. **Written as sent** (site reviews correct titles) — except that sending the course id itself as the title never replaces a real title. All-capitals titles are displayed in title case; the stored value is not changed. |
| `stateTitle` | ≤ 300; the SCNS statewide title. `""` clears it. |
| `creditHours` | 0–20 (integer). PSAV: `0` with `contactHours`. |
| `contactHours` | 0–3000 |
| `taxonomyKey` | optional; otherwise placed by prefix (letters before the first digit). Sending it on an existing course **moves** the course. |
| `isActive` | default `true` on create. `false` hides a course **only if it has no guide and no published modules**. |
| `offerings[]` | ≤ 250 per course. `institution` short code (≤ 10, letters/digits/`_`/`-`, uppercased); `title` ≤ 300; `credits` 0–99 (decimal); `clockHours` 0–3000; `isActive` default `true`. |
| `replaceOfferings` | default **`true`**: offerings not in the list are **removed**. `false` adds/updates only. |
| **null / omitted** | **left unchanged** on an existing course (except `title`, which is always required). |

## Read endpoints (public)

| Call | Use |
|---|---|
| `GET /api/v1/courses/catalog?prefix=EEE&hasGuide=false&active=true&updatedSince=2026-09-01&page=1&pageSize=1000` | Reconcile: what the site holds. `pageSize` ≤ 1000. Items carry `courseId, title, stateTitle, creditHours, contactHours, taxonomyKey, isActive, source (Guide/Catalog), hasGuide, offeringCount, createdUtc, updatedUtc`. |
| `GET /api/v1/courses/{courseId}/offerings` | One course's base data plus every offering with institution name. |
| `GET /api/v1/institutions` | Codes, names, sectors, active offering counts. |

`hasGuide` ignores the "Not Completed" stubs created when modules are published. `updatedSince` is UTC;
courses created before the catalog existed have no `updatedUtc` until they are next written.

## Guides are unchanged

`PUT /api/v1/courses/{courseId}/guide` works exactly as before (`generate_guide.py`). If the course is not
on the site yet the guide push still creates it — with the course id as a placeholder title, **so send the
course's base data too** (before or after the guide). On an existing course the guide push never touches
the course's title, credits or offerings.

## Guide requests — the priority signal

Visitors press **Request Guide** on any course without a guide (one click, anonymous). Those requests are
**the first priority for writing guides.** Read them from the public queue — no token needed:

```
GET /api/v1/queue/guides?status=waiting     # Open + Queued, most requested first (ties: earliest request)
GET /api/v1/queue/guides?status=published   # courses whose guide is out
```

Each item: `rank, courseId, title, requestCount, firstRequestedUtc, lastRequestedUtc, status (Open · Queued ·
Published · Declined), hasGuide, isListed`. `isListed: false` means someone asked for a course the site does
not list yet — add its base data before (or with) the guide. The same list is on the site at `/queue/guides`.

`queue_mgr.py import-requests` (admin endpoint `GET /api/v1/guide-requests`) still works and still marks
requests `Queued`; a published guide closes its requests automatically.

## Error codes

| HTTP | Code | When |
|---|---|---|
| 400 | `INVALID_COURSE_ID` | id does not match the pattern |
| 400 | `VALIDATION_ERROR` | field rules above (`details`/`fields` list them); duplicate id in one batch |
| 400 | `BATCH_TOO_LARGE` | > 500 courses or > 1000 institutions |
| 401 | `UNAUTHORIZED` | missing or expired token |
| 404 | `COURSE_NOT_FOUND` | offerings / delete of an unknown course |
| 409 | `COURSE_HAS_CONTENT` | delete of a course with a guide, modules or requests |
| 422 | `TAXONOMY_PLACEMENT_REQUIRED` | no taxonomy node for the prefix and no `taxonomyKey` |
| 422 (single) / item error (batch) | `TAXONOMY_NODE_NOT_FOUND` | `taxonomyKey` given but unknown |

## Suggested run shape

1. `POST /api/v1/institutions/batch` with codes and names.
2. Build course rows by your rules; send them in batches of ≤ 500. Log every `failed` result.
3. Reconcile with `GET /api/v1/courses/catalog?updatedSince=<run start>` and spot-check a course page.
4. Courses that dropped out of the source: send `isActive: false` (never delete a course that has a guide).
