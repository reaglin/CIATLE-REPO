# Resource review API — contract for the reviewing AI session

**For the AI session that reviews course resources** (run from `Tools/`). Visitors — and vendors or sales
agents offering products — suggest links on a course's **Resources** page (`/courses/{id}/resources`). The
suggestions wait in a public queue. This session reads the queue, looks at each resource, **writes a summary**,
lists it for the course, and **lists it for other courses that benefit** too.

Server side: `COURSE_CATALOG_PLAN.md` phase 3. **Not live until the next deploy** — check that
`GET /api/v1/queue/resources` returns 200 first.

**Approval rules:** Ron is writing the rules set. Put it in `Tools/resources/APPROVAL_RULES.md` and follow it;
this file only covers the mechanics.

---

## How listings work

- **Every listing belongs to one course.** The same link can be listed for many courses — a link is
  lightweight, so redundancy is fine — and **each listing has its own title and summary**, so a summary can
  say how the resource helps *that* course. Editing or removing one course's listing never touches the others.
- **Resources may be free or commercial.** Products suited to a course are welcome (vendors suggest them).
  **The summary must say plainly whether the resource is free, free with an account, freemium, or a paid
  product, and who offers it.**
- Pages show the title, the summary with a small "AI-written summary" label, the site name, and "Also listed
  for" (other courses with a listing of the same link). YouTube videos show a thumbnail that plays in place.
- **Visitors thumbs-up a listing**, and listings are ordered most-helpful first. `helpfulCount` comes back on
  every listing, so you can see what readers value — there is no cap on resources per course; the votes sort
  them. Voting is `POST /api/v1/resources/{id}/helpful` (public, anonymous, one toggleable vote per visitor);
  it is a visitor action, not a reviewer one.
- The submitter's note is input for you; it is never shown on the course page.

## Authentication

Same as `COURSE_API.md`: `POST /api/v1/auth/login` with `REPO_ADMIN_EMAIL` / `REPO_ADMIN_PASSWORD` →
`data.accessToken` → `Authorization: Bearer <token>` (60 minutes). Reads need no token.

## The loop

1. **Read the queue** (oldest first):
   `GET /api/v1/queue/resources?status=pending`
   Items: `id, courseId, courseTitle, url, type (Website · YouTube), host, description, status, submittedUtc`.
2. **Look at the resource** off-server (fetch the page / video) and apply the approval rules.
3. **See where the link is already listed** (optional): `GET /api/v1/resources?url=<url>`.
4. **Approve** — lists it for the suggested course, plus any others:

   ```
   POST /api/v1/resource-submissions/{id}/approve
   { "title": "Khan Academy — Electrical engineering: circuits",
     "summary": "Free video lessons and practice problems on circuit analysis …",
     "note": null,
     "alsoFor": [
       { "courseId": "EET1015C" },
       { "courseId": "EEE3300", "summary": "Tailored summary for this course (optional) …" }
     ] }
   ```

   `title` 1–200 and `summary` 20–2000 characters are the defaults for every course; an `alsoFor` entry may
   carry its own `title` / `summary`. At most 100 `alsoFor` courses. Response `results[]`: per course
   `created` · `updated` (that course already listed the link — its listing is refreshed) · `unknownCourse`
   (not listed on the site — nothing written; add the course first via `COURSE_API.md` if it should exist).
5. **Or reject** with a short, public-safe reason (shown in the public queue):
   `POST /api/v1/resource-submissions/{id}/reject  { "note": "Not related to circuit analysis." }`

## Resources you find yourself

List a link directly — no queue, since you are the reviewer:

```
POST /api/v1/resources
{ "url": "https://www.youtube.com/watch?v=…",
  "title": "…", "summary": "…",
  "courses": [ { "courseId": "EEE3300" }, { "courseId": "EEE3308C", "summary": "…" } ] }
```

The same call adds an already-listed link to more courses; a course that already lists it gets its listing
updated (and restored if it had been removed).

## Correcting one listing

| Call | Effect |
|---|---|
| `PATCH /api/v1/resources/{id}` `{ "title"?, "summary"?, "status"?: "active" \| "removed" }` | edit, remove or restore **that course's** listing |
| `DELETE /api/v1/resources/{id}` | delete that listing permanently |
| `GET /api/v1/resources/{id}` | one listing, with `alsoForCourseIds` |
| `GET /api/v1/courses/{courseId}/resources` | a course's active listings |

Ron can do all of this at `/admin/resources`, including reopening a decided suggestion.

## Link rules (checked on submit and on create)

`http`/`https` only; a public host (no IP addresses, `localhost` or local names, no user:password). Links are
normalised: lowercase host, no `#fragment`, tracking parameters (`utm_*`, `fbclid`, `gclid`, …) removed.
**Matching is exact on the path and query** — host case is ignored, path case is not — so two links that differ
only in the letter case of the path count as different links. Paste links as the site writes them.
YouTube links (`watch?v=`, `youtu.be/`, `/shorts/`, `/embed/`, `/live/`) become
`https://www.youtube.com/watch?v=<id>`; a YouTube link that is not a single video is refused. The server never
fetches submitted links. A visitor cannot re-suggest a link already listed for that course, one already
waiting, or one rejected for that course in the last 30 days; suggestions are limited to 10 per IP per hour.

## Error codes

| HTTP | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | title / summary / note / course list rules |
| 400 | `INVALID_RESOURCE_URL` | the link fails the rules above |
| 401 | `UNAUTHORIZED` | missing or expired token |
| 404 | `RESOURCE_SUBMISSION_NOT_FOUND` · `RESOURCE_NOT_FOUND` · `COURSE_NOT_FOUND` | unknown id |
| 409 | `SUBMISSION_NOT_PENDING` | approving or rejecting a decided suggestion |
| 422 | `COURSE_NOT_FOUND` | none of the courses given are listed on the site |
| 429 | `RATE_LIMIT_EXCEEDED` | visitor suggestion limit |
