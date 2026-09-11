# Resource review — tooling

Works the public **resource review queue** for [floridacourserepo.com](https://floridacourserepo.com):
links suggested by visitors and vendors on a course's Resources page.

| File | What it is |
|---|---|
| `review_resources.py` | the API client — read the queue, apply decisions, correct listings |
| `APPROVAL_RULES.md` | **what to approve and reject** (Ron's rules; draft) |
| `../RESOURCE_API.md` | the API contract: endpoints, payloads, error codes |
| `review_resources.log` | append-only record of everything this client did |

The `/resources` skill drives the whole loop in a Claude Code session started in `Tools/`.

## Run it

From `Tools/resources/` (credentials come from `Tools/.env`, same as the guide pipeline):

```powershell
python review_resources.py check                 # API reachable, admin login works
python review_resources.py queue                 # pending suggestions, oldest first
python review_resources.py queue --json          # same, as JSON
```

Decide by reading `APPROVAL_RULES.md` and **looking at each resource**, then write `decisions.json`:

```json
[
  {"action": "approve", "id": "<submissionId>",
   "title": "All About Circuits — online textbook",
   "summary": "Free online textbook covering DC and AC circuit analysis, with worked examples. No account needed.",
   "alsoFor": [{"courseId": "EET1015C"},
               {"courseId": "EEE3300L", "summary": "Pairs with the lab: the DC chapters explain each experiment's measurements."}]},
  {"action": "reject", "id": "<submissionId>", "note": "Not related to the course."},
  {"action": "add", "url": "https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/",
   "title": "MIT OpenCourseWare — Circuits and Electronics",
   "summary": "Free MIT course materials: video lectures, problem sets and exams. Free, no account needed.",
   "courses": [{"courseId": "EEE3300"}, {"courseId": "EEE4314C"}]}
]
```

```powershell
python review_resources.py apply decisions.json      # shows the plan, asks, then applies
python review_resources.py apply decisions.json --yes
```

A file is the normal path: summaries run to several sentences, and Windows quoting mangles them on the
command line. One-off flags (`approve`, `reject`, `add`) exist for short cases.

## Correcting a listing

**Every listing belongs to one course.** The same link listed on other courses has its own title, summary
and status, and is not touched by these:

```powershell
python review_resources.py listings --course EEE3300
python review_resources.py listings --url https://example.org/page
python review_resources.py edit <listingId> --summary "..."
python review_resources.py remove <listingId>      # hide (reversible)
python review_resources.py restore <listingId>
python review_resources.py delete <listingId>      # permanent
```

Ron can do the same at `/admin/resources`, including reopening a decided suggestion.

## Testing against a local server

```powershell
python review_resources.py --base-url http://localhost:5199 queue
```
