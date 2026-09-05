# Generate Guides and Push Process

**This is the start-here document for publishing curriculum guides to
[floridacourserepo.com](https://floridacourserepo.com).**

`CIATLE-REPO/Tools/` is the toolchain that adds new courses and their curriculum guides to
the live Florida Course Repository. Everything needed to prioritize, draft, validate, push,
and verify a guide lives in this directory. The rest of the repo (`PreseMakerRepo.Api`,
`.Core`, `.Infrastructure`) is the *server* that floridacourserepo.com runs; `Tools/` is how
*content* gets into it.

| Where | What |
|---|---|
| **This file** | The end-to-end process. Read first. |
| `CLAUDE.md` | Guide **content** standards — quality bar, HTML sections, Florida/SCNS pedagogy. Authoritative for what a guide says. |
| `QUEUE_GUIDE.md` | `queue.csv` column map, status values, priority tiers. |
| `README.md` | Per-tool command reference and hard-won lessons. |
| `SOURCES.md` | Where to research a course: authoritative sources ranked, which Florida college catalogs actually answer, and the recurring traps to check every time. |
| `.claude/skills/guide/SKILL.md` (repo root) | Drives this loop in a Claude Code session. |

---

## The short version

```powershell
cd C:\Users\ronal\source\repos\CIATLE-REPO\Tools

python queue_mgr.py status                        # 1. where things stand
python queue_mgr.py next-batch --n 5              # 2. pick the batch
                                                  # 3. draft (see below)
python validate_drafts.py --drafted               # 4. preflight
python queue_mgr.py reconcile                     # 5. sync queue to disk
python generate_guide.py --push-from-queue --yes  # 6. push to the live site
python queue_mgr.py status                        # 7. confirm
```

Steps 1-2 and 4-7 are commands. Step 3 is the writing, and it is the only part that takes
judgment.

---

## Prerequisites

**One-time:**

```powershell
cd Tools
pip install -r requirements.txt      # anthropic, requests
```

**Credentials** live in `Tools/.env` (gitignored — never commit it):

| Variable | Needed for |
|---|---|
| `REPO_ADMIN_EMAIL` | pushing to the site |
| `REPO_ADMIN_PASSWORD` | pushing to the site |
| `REPO_BASE_URL` | optional; defaults to `https://floridacourserepo.com` |
| `ANTHROPIC_API_KEY` | only the standalone `generate_guide.py <ID>` generator, which this process does not use |
| `GUIDE_MODEL` | optional model override for that same standalone path |

**No PowerShell execution-policy step is needed.** That was a prerequisite of the retired
ZIP importer (see *Legacy* below), not of this process.

---

## Step 1 — Prioritize

`queue.csv` is the master work list. `courses_2plus_institutions.csv` is the inventory it
draws from (every SCNS course offered at 2+ Florida institutions).

```powershell
python queue_mgr.py status                    # counts per state
python queue_mgr.py list --state queued       # what's waiting
python queue_mgr.py next-batch --n 5          # the next N by priority
```

**Refill the queue when it runs dry:**

```powershell
python queue_mgr.py add --top 25                  # most-offered courses not yet queued
python queue_mgr.py add --prefix EGN --max-inst 50
python queue_mgr.py add --institution "Valencia"
python queue_mgr.py add --course EEL4580 --note "Faculty request - Dr. Smith, EE Dept"
```

**Priority is `1000 - num_inst`; lower runs first.** Widely-offered courses help more
students per guide written, so they go first.

**Faculty requests get a manual priority below 929 and jump the queue** — a real person is
blocked on those. Set `notes` to `Faculty request - [name/dept] - [reason]`. Full tier table
is in `QUEUE_GUIDE.md`.

**Apply judgment to what `--top` hands you.** It ranks purely by institution count, so it
will surface courses that make poor statewide guides. Demote or skip:

- **Shell courses** — internship, co-op, special topics, independent study, thesis,
  dissertation, supervised research (`XXXX9xx` codes, or those keywords in the title).
- **Individualized instruction** — applied-music courses (`MVS`/`MVW`/`MVK`, "PRINCIPAL
  APPLIED …") are one-on-one lessons; a statewide guide has little to say.
- **Courses only at private institutions** — the repository serves Florida public colleges
  and SUS institutions.
- **Non-engineering BAS courses** using an engineering prefix.

To drop one: `python queue_mgr.py remove <ID>`, or `mark <ID> --state skipped` to keep the
record of the decision.

---

## Step 2 — Generate

**Read `CLAUDE.md` before writing.** It carries the quality bar, the canonical HTML section
order, and the Florida conventions (SCNS code patterns, PSAV vs. transfer vs. Engineering
Technology treatment, hedging by institution count). This file covers mechanics; that file
governs content.

Write each guide directly to:

```
Tools/drafts/{COURSE_ID}_guide.json
```

Course ID uppercase, no spaces, exactly that filename — `queue_mgr.py reconcile` matches
drafts to queue rows by parsing it.

Six top-level keys, no more:

```json
{
  "title": "Principles of Financial Accounting",
  "html_content": "<h2>Course Description</h2>...",
  "credits": 3,
  "contact_hours": 45,
  "prerequisites": "MAC2311 or equivalent",
  "version": "1.0"
}
```

`prerequisites` may be `null`. `html_content` is **inner content only** — no `<html>`,
`<head>`, `<body>`, or `<style>` tags.

Research before writing: the SCNS framework entry and actual Florida college catalogs.
`courses_2plus_institutions.csv` gives the institution count and the most common title.
Honest hedging beats a fabricated uniform standard — and omitting a section beats inventing
one.

Batch size is a judgment call. The old cap of 4-5 came from a chat's per-response output
limit and no longer applies, but quality still beats volume.

### Server limits — break one and the push returns HTTP 400

Enforced by `PreseMakerRepo.Api/Validators/PublishValidators.cs`
(`UpsertCurriculumGuideRequestValidator`):

| Field | Limit |
|---|---|
| `title` | non-empty, ≤ 300 chars |
| `html_content` | non-empty |
| `credits` | integer **0-12**, never null (`push_guide` rejects null before the server sees it) |
| `contact_hours` | integer **0-1500** |
| `prerequisites` | ≤ 500 chars, or null |
| `version` | ≤ 50 chars |

⚠️ **PSAV clock-hour courses take `credits: 0`** with the hours in `contact_hours`. Never
copy the clock-hour count into `credits`. That single mistake stalled 11 guides for months
(`TDR0775` and friends carried `credits: 150`).

---

## Step 3 — Validate

```powershell
python validate_drafts.py EGN3311 EGN3321   # the batch you just wrote
python validate_drafts.py --drafted         # everything staged to push
python validate_drafts.py --errors          # everything currently failing
python validate_drafts.py --quiet           # failures only
```

`validate_drafts.py` mirrors the server rules exactly, so a clean run means the push will
not come back 400. Exit code 0 = publishable, 1 = not, so it scripts cleanly.

It also emits **warnings** that don't block but deserve a look: credit/contact-hour
mismatches (3 credits should be ~45 hours, ~60 for a `C` course, 1-credit `L` labs ~30-45),
missing canonical sections, unusually thin content, and clock-hour counts that look like
they landed in `credits`.

**Never push past a `FAIL`.**

---

## Step 4 — Push

```powershell
python queue_mgr.py reconcile                     # queued -> drafted for new files
python queue_mgr.py ready-to-push                 # exactly what the next command will push
python generate_guide.py --push-from-queue --yes  # push everything marked drafted
```

Single course: `python generate_guide.py --push-draft EGN3311`

`--push-from-queue` only picks up rows in state **`drafted`**. `reconcile` promotes
`queued` rows whose draft file now exists. A row sitting at `error` is *not* picked up —
flip it deliberately (see *Retrying* below).

This writes to the live site. Confirm the batch before running it.

---

## Step 5 — Verify

```powershell
python queue_mgr.py status
curl.exe -s "https://floridacourserepo.com/api/v1/courses/EGN3311/guide"
```

Don't rely on the push log alone — fetch from the live API and confirm the content and the
credit/contact-hour values match the local draft.

### ⚠ Always count the pushes — a partial batch does not announce itself

**`queue_mgr.py status` must show `drafted: 0` after a push.** If any row is still `drafted`,
the loop stopped early, and it can do so *without an error in the log* — the log only records
guides the loop actually reached.

Worked case, 2026-09-02: a batch of 8 pushed 6 and stopped. `DES0844` and `EEX4242` were left
`drafted` with **no log entry at all**, and the console output scrolled past the traceback.
Cause: `generate_guide.py` prints a review preview of each guide, and the Windows console
defaults to **cp1252**, which cannot encode the **⚠** character the content standard tells us
to use for flags. `UnicodeEncodeError` on a *display* line killed the whole push loop.

Fixed at the source — `generate_guide.py` now reconfigures stdout/stderr to UTF-8 with
`errors="replace"` at startup, so an encoding problem degrades a character instead of aborting
a production push. The habit still stands regardless of the fix:

```powershell
python queue_mgr.py status            # drafted must be 0
grep "PUSH:" generate_guide.log | tail -N   # N = batch size; count the Success lines
```

The general lesson: **a push loop that ends quietly is not the same as a push loop that
finished.** Reconcile the count every time.

**`curriculumGuideUrl` staying `null` on `/api/v1/courses/{id}` is normal.** It only
populates once a course has published modules. The `/guide` endpoint returning content is
the real confirmation.

Close out a batch with a short table (course, credits, contact hours, size) and bullets
flagging anything worth review: unusual hour counts, generic titles, single-institution
courses, articulation gotchas.

---

## Retrying a failed guide

A row at `status=error` keeps its draft file. Fix the file in place, then:

```powershell
python validate_drafts.py EEV0658
python queue_mgr.py mark EEV0658 --state drafted
python generate_guide.py --push-draft EEV0658
```

Don't add a duplicate queue row. To force a full rewrite instead:

```powershell
Remove-Item .\drafts\EEV0658_guide.json
python queue_mgr.py mark EEV0658 --state queued
```

`python queue_mgr.py reconcile` is the truth-restoration command whenever the queue and
`drafts/` disagree.

---

## Deploying server changes

Guide *content* needs no deploy — it goes over the API. Changing the *server* (validators,
pages, endpoints) does:

```powershell
.\Deployment\deploy-update.ps1      # from the repo root
```

Uses native Windows OpenSSH and the dotnet CLI. `bash` is **not** on PATH on this machine,
so `deploy-update.sh` needs its full path (`C:\Program Files\Git\bin\bash.exe`) — prefer the
PowerShell script. Add `-SkipMigrations` when the release has no new EF migration. Details
in `Deployment/Deploy_Instructions.txt`.

Server-side fixes waiting to be bundled into the next deploy are listed in
`Deployment/PENDING_SERVER_CHANGES.md`. Check it before deploying, and clear entries as they
ship.

---

## Troubleshooting

**Carriage returns are the recurring bug in this project.** Windows tooling emits CRLF where
Unix tools expect LF, and the symptom is always a mangled-looking command:

- Python's `print` writes CRLF on Windows. Piping such a file into a bash `read` loop leaves
  a trailing `\r` on each value, so `queue_mgr.py mark "PRN0091\r"` matches nothing. Strip
  with `tr -d '\r'`.
- Piping a multi-line string to `ssh "bash -s"` from PowerShell appends a CRLF, corrupting
  the final line (`--no-pager\r` produced `'ystemctl: unrecognized option`). Pass the remote
  script as a single `;`-joined argument instead.
- `.ps1` files must be **ASCII-only with CRLF** endings or PowerShell mis-parses them, and
  its error display shows the *parsed* text, not the file. Verify with a non-ASCII byte count
  and `[Parser]::ParseFile`.

**Other traps:**

- **Never name a `.py` file after a stdlib module** (`queue`, `csv`, `json`, `email`, …) in
  this directory — it shadows the real module and breaks `requests`/`urllib3`. That is why
  the queue tool is `queue_mgr.py`; don't rename it back.
- **Read user-facing CSVs with `encoding="utf-8-sig"`** — Excel prepends a BOM that plain
  `utf-8` chokes on.
- **Quote titles containing commas** when hand-editing `queue.csv`.
- **HTTP 400 on push** — run `validate_drafts.py` on that course; it will name the field.
- **HTTP 401 mid-batch** — the token expired; `generate_guide.py` re-authenticates and
  retries once on its own.

---

## Legacy: the ZIP bridge

Guides were once drafted in a claude.ai chat, downloaded via "Download All", saved as
`files.zip`, and imported with `import_zip_to_drafts.ps1` — which needed
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in every new terminal.

**That bridge is retired.** Working in a Claude Code session in this repo, guides are written
straight to `drafts/`. `import_zip_to_drafts.ps1` still works if a batch ever arrives from a
chat session, but nothing in this process depends on it.

---

## Directory map

```
Tools/
├── Generate_Guides_and_Push_Process.md  (this file - start here)
├── CLAUDE.md                            (guide CONTENT standards)
├── QUEUE_GUIDE.md                       (queue schema + priority tiers)
├── README.md                            (per-tool command reference)
│
├── queue_mgr.py                         (prioritize: queue management)
├── validate_drafts.py                   (preflight: mirrors server rules)
├── generate_guide.py                    (push to the live site)
├── extract_courses.py                   (one-time: build the inventory CSV)
├── make_batch.py                        (legacy ad-hoc filter)
├── import_zip_to_drafts.ps1             (legacy chat-output importer)
│
├── .env                                 (credentials - gitignored)
├── queue.csv                            (the work list)
├── courses_2plus_institutions.csv       (course inventory)
├── activity.log                         (audit trail)
├── generate_guide.log                   (push results)
│
└── drafts/                              (guide JSONs - written here, pushed from here)
```
