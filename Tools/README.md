# Florida Course Repository -- Curriculum Guide Pipeline

Tooling for generating, reviewing, and publishing AI-authored curriculum
guides for [floridacourserepo.com](https://floridacourserepo.com), a public
library of open educational materials aligned to the
[Florida Statewide Course Numbering System](https://flscns.fldoe.org) (SCNS).

This directory holds everything needed to run the pipeline end-to-end:
extract candidate courses from the state inventory, manage a queue, draft
guides in chat with Claude, validate and import them, and push them to the
live site.

---

## Quick start

Once the queue has courses in it (`queue.csv` exists and shows `queued`
entries), the per-batch loop is:

```powershell
# 1. In a Claude chat, ask for the next N guides from the queue.
#    Claude generates JSON files and packages them as a single download.
#
# 2. Right-click the chat's "Download All" link and save the ZIP as
#    .\files.zip   in this directory (C:\Users\ronal\source\repos\CIATLE-REPO\Tools).
#
# 3. Validate, extract, reconcile:
.\import_zip_to_drafts.ps1
#
# 4. Eyeball the new files in .\drafts\, then push to the site:
python generate_guide.py --push-from-queue --yes
#
# 5. Confirm:
python queue_mgr.py status
```

Each batch is typically 4-5 guides because Claude's per-response output is
the constraint.

---

## What each piece does

### `extract_courses.py`
Parses the giant statewide inventory CSV down to a clean list of courses
that are offered at 2 or more institutions. Run this **once** at project
start, or whenever the inventory file is updated.

```powershell
python extract_courses.py All_StatewideInventory_clean1.csv
# → produces courses_2plus_institutions.csv
```

Rules it applies:
- Course IDs match `ABC1234`, `ABC1234C` (lab integrated), or `ABC1234L` (lab separate).
- `ABC1234` and `ABC1234C` are merged into a single row using the C-form if
  any institution offers it; `ABC1234L` is kept as its own row.
- Title commas are replaced with " - " so the CSV stays well-formed.
- Picks the most-common title across institutions, with shortest as tiebreaker.

Output columns: `course_id, title, num_inst, institutions`.

### `queue_mgr.py`
Manages `queue.csv` (the work-list) and `activity.log` (audit trail).
Courses move through the states `queued → drafted → pushed`, with `error`
and `skipped` for off-path entries.

```powershell
# Populate the queue
python queue_mgr.py add --top 11                     # the 11 most-offered courses
python queue_mgr.py add --prefix MAC                 # all MAC* courses
python queue_mgr.py add --institution "Valencia"     # courses offered there
python queue_mgr.py add --min-inst 30 --max-inst 50  # by institution count

# Inspect
python queue_mgr.py status                           # counts per state
python queue_mgr.py list --state queued              # one column per state
python queue_mgr.py next-batch --n 5                 # next 5 queued IDs

# Manual edits (rare -- reconcile usually handles state changes)
python queue_mgr.py mark ENC1101C --state drafted
python queue_mgr.py remove BSC1005C
```

The most useful command:

```powershell
python queue_mgr.py reconcile
```

`reconcile` walks `drafts/` and `generate_guide.log` and updates the queue
to match reality. Any `queued` entry whose draft file exists becomes
`drafted`; anything pushed (per the log) becomes `pushed`. Run this any
time the queue and the filesystem might disagree -- it's the source of
truth-restoration command.

> **Why is it `queue_mgr.py` and not `queue.py`?** Python's standard
> library has a module named `queue`, and a project file with the same
> name shadows it -- breaking `urllib3` and anything else that does
> `import queue`. The file was renamed early in the project after that
> exact failure. Don't rename it back.

### `generate_guide.py`
Original tool from before we added the pipeline. Does two things now:

1. **Generates a guide for a single course via the Anthropic API.** Used
   by the original solo-course workflow:
   ```powershell
   python generate_guide.py ETS1010
   python generate_guide.py --file courses.txt --yes
   ```
   This requires `ANTHROPIC_API_KEY` in the environment (or a `.env` file).
   Most batches in this project skip this path entirely -- Claude generates
   the JSON in chat, and you import via the ZIP.

2. **Pushes existing draft files to the repo API.** This is the path
   used after `import_zip_to_drafts.ps1`:
   ```powershell
   python generate_guide.py --push-from-queue --yes      # all `drafted` in queue
   python generate_guide.py --push-draft ETS1010         # single draft
   python generate_guide.py --push-draft-file list.txt   # batch
   ```
   This requires `REPO_ADMIN_EMAIL` and `REPO_ADMIN_PASSWORD` in env.

### `import_zip_to_drafts.ps1`
PowerShell glue that bridges Claude's chat output to your local pipeline.

```powershell
.\import_zip_to_drafts.ps1                # default: .\files.zip
.\import_zip_to_drafts.ps1 path\to\x.zip  # explicit path
.\import_zip_to_drafts.ps1 -Force         # overwrite existing drafts without prompting
.\import_zip_to_drafts.ps1 -KeepZip       # don't delete the ZIP after success
```

What it does, in order:
1. Resolves the ZIP path (default `.\files.zip` in the current directory).
2. Extracts to a temp directory.
3. Validates every `*_guide.json` inside is parseable and has all six
   required fields (`title`, `html_content`, `credits`, `contact_hours`,
   `prerequisites`, `version`).
4. Prompts before overwriting any draft files that already exist (skip
   prompt with `-Force`).
5. Copies validated files to `drafts/`, with rollback if anything fails
   partway.
6. Runs `python queue_mgr.py reconcile` so the queue picks up the new
   `drafted` state.
7. Prints status and tells you the push command to run next.
8. Deletes the ZIP unless `-KeepZip`.

You may need to run this command to execute this script

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Workflow:
1. Generate guides with claude and download all. Save as files.zip in the working directory.
2. Set the execution policy for the script (see above) and run import_zip_to_drafts.ps1 in powershell. .\import_zip_to_drafts.ps1 
3. Execute command given at end of this script. 

### `make_batch.py`
Earlier filter-and-emit tool, superseded by `queue_mgr.py` for the normal
workflow. Still works if you want to slice the inventory ad-hoc without
touching the queue.

---

## Project layout

```
Tools/
├── README.md                          (this file)
├── extract_courses.py                 (one-time CSV cleaner)
├── queue_mgr.py                       (queue management)
├── generate_guide.py                  (push tool + standalone generator)
├── import_zip_to_drafts.ps1           (chat-output importer)
├── make_batch.py                      (legacy ad-hoc filter)
│
├── All_StatewideInventory_clean1.csv  (input: state inventory, ~9 MB)
├── courses_2plus_institutions.csv     (output of extract_courses.py)
├── queue.csv                          (working queue, managed by queue_mgr.py)
├── activity.log                       (audit trail of state changes)
├── generate_guide.log                 (push results from generate_guide.py)
│
└── drafts/                            (validated guide JSONs awaiting push)
    ├── ENC1101C_guide.json
    ├── HSC0003C_guide.json
    └── ...
```

---

## The chat ↔ filesystem bridge

Claude can't write to your filesystem directly -- it lives in a sandbox.
The bridge is the chat's "Download All" feature: Claude packages the
batch's JSON files into a ZIP, you download it, and `import_zip_to_drafts.ps1`
takes it from there.

**Naming convention.** Every guide file is `{COURSE_ID}_guide.json`
(e.g. `ENC1101C_guide.json`). The PowerShell script and `queue_mgr.py`
both rely on this. Don't rename them -- `reconcile` matches drafts to
queue entries by extracting the course ID from the filename.

**JSON schema.** Each guide must have exactly six top-level fields:

```json
{
  "title": "Short descriptive guide title",
  "html_content": "<full HTML -- see format below>",
  "credits": 3,
  "contact_hours": 45,
  "prerequisites": "MAT 0028 or equivalent" | null,
  "version": "1.0"
}
```

`credits=0` is allowed and indicates a Postsecondary Adult Vocational
(PSAV) clock-hour course (e.g. HSC0003C, HCP0121C); the real measurement
is in `contact_hours`. PSAV courses get the FLDOE Curriculum Framework
treatment -- standards-based outcomes, clock-hour formatting,
articulation language -- rather than the Gen-Ed-core treatment used for
transfer courses.

**HTML conventions.** Inner content only -- no `<html>`, `<head>`, `<body>`,
or `<style>` tags. Sections in canonical order:

- Course Description
- Learning Outcomes (Required + Optional subsections)
- Major Topics (Required + Optional subsections)
- Resources & Tools
- Career Pathways
- Special Information

Use `<h2>` for section headings, `<h3>` for Required/Optional subsections,
`<p>` for paragraphs, `<ul class="list-group list-group-flush"><li class="list-group-item">`
for outcome/topic lists, plain `<ul><li>` for resource lists, `<strong>`
for key terms. Bootstrap is available; keep markup clean.

---

## Hard-won lessons (don't re-learn these the hard way)

### PowerShell scripts must be ASCII + CRLF
Windows PowerShell mis-parses `.ps1` files that contain Unicode
characters (em-dashes `--`, smart quotes, en-dashes) or have bare LF line
endings. Symptom: bizarre parser errors pointing at lines that look fine
in your editor, and error messages may even *display* corrupted versions
of your code (because PowerShell shows what it *parsed*, not what's in
the file).

If you write or edit a `.ps1` file:
- ASCII characters only -- replace `--` with `--`, `'` with `'`, etc.
- CRLF line endings (`\r\n`) -- most Windows editors do this by default,
  but be careful if a file came from Linux/Mac

To verify a `.ps1` file is clean:
```powershell
# Should return zero non-ASCII bytes
$bytes = [System.IO.File]::ReadAllBytes(".\import_zip_to_drafts.ps1")
($bytes | Where-Object { $_ -gt 127 }).Count
```

### Don't shadow stdlib module names
Python files in this directory must not be named after standard-library
modules. `queue.py` was the original sin -- it broke `import queue` for
every package that needed it (urllib3, requests, etc.). Avoid:
`queue`, `email`, `time`, `random`, `socket`, `threading`, `string`,
`io`, `os`, `sys`, `json`, `re`, `csv`, `logging`, `select`, `signal`,
`tempfile`, `pickle`, `subprocess`.

### Markdown autolinks in chat output
When Claude writes `generate_guide.py` in chat, the chat UI sometimes
converts it to `generate_[guide.py](http://guide.py)` -- a Markdown
autolink -- and that's what ends up in your downloaded file if you're not
careful. After saving any code Claude sends you, scan with:

```powershell
Select-String -Path *.py,*.ps1 -Pattern '\[\.py\]\(http|\[guide\.py\]'
```

If anything matches, fix it. The pattern is `something_[name.ext](http://name.ext)`
-- remove the brackets and URL, leaving just `something_name.ext`.

### PowerShell execution policy
First time running `.ps1` scripts, you'll likely hit a "scripts disabled"
error. Run once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

This allows local scripts to run while still blocking unsigned ones
downloaded from the internet. Files downloaded through your browser may
still need:

```powershell
Unblock-File .\some_script.ps1
```

### BOM-tolerant file reading
The Python tools all use `encoding="utf-8-sig"` when reading user-facing
files (CSVs, the queue, course-list inputs). Excel and various Windows
editors sometimes prepend a UTF-8 byte-order mark, and `utf-8` (without
`-sig`) chokes on it. If you add a new tool that reads any of these
files, use `utf-8-sig` for the read and plain `utf-8` for the write.

### The 60-second batch delay
`generate_guide.py` originally enforced a 60-second pause between courses
in batch mode to respect Anthropic API rate limits. That delay is
**only** needed when actually calling the Anthropic API -- it was removed
from `run_push_draft_batch` (push-only path) because the repo API is on
your own server and doesn't need the same throttling.

---

## Environment variables

`generate_guide.py` reads these from the environment or from a `.env` file
in this directory:

| Variable                | Required for                              |
|-------------------------|-------------------------------------------|
| `ANTHROPIC_API_KEY`     | API-based generation (the standalone path) |
| `REPO_ADMIN_EMAIL`      | Pushing guides to the site                 |
| `REPO_ADMIN_PASSWORD`   | Pushing guides to the site                 |
| `REPO_BASE_URL`         | Override default `https://floridacourserepo.com` |
| `GUIDE_MODEL`           | Override default `claude-opus-4-7` model   |

For the chat-driven workflow (most batches), only the two `REPO_ADMIN_*`
vars matter -- Claude does the generation, your push tool just authenticates
and POSTs.

---

## Common operations

### Fresh start (rebuilding the queue from scratch)
```powershell
Remove-Item .\queue.csv -ErrorAction SilentlyContinue
python queue_mgr.py add --top 50
python queue_mgr.py reconcile        # picks up any existing drafts
python queue_mgr.py status
```

### Adding more courses to an existing queue
```powershell
python queue_mgr.py add --prefix CHM --max-inst 50
python queue_mgr.py add --prefix PHY --max-inst 50
python queue_mgr.py status
```

### Resuming after a session break
```powershell
python queue_mgr.py status           # what's where
python queue_mgr.py list --state drafted   # what's ready to push
python generate_guide.py --push-from-queue --yes
```

### A push failed and I'm not sure of the state
```powershell
python queue_mgr.py reconcile         # resyncs from drafts/ + generate_guide.log
python queue_mgr.py status
```

### A draft is wrong and I need to regenerate
```powershell
Remove-Item .\drafts\BSC1005C_guide.json
python queue_mgr.py mark BSC1005C --state queued
# then ask Claude to regenerate it in the next batch
```

---

## When something breaks

1. **`Select-String` pattern checks** are the fastest way to spot
   markdown-autolink corruption in code Claude sent you.
2. **`queue_mgr.py reconcile`** restores the queue from filesystem
   reality whenever they disagree.
3. **`Get-FileHash` comparisons** can verify whether two copies of a
   script are actually byte-identical when something seems wrong.
4. **A fresh PowerShell window** rules out cached/stale parser state.
5. **Read the error trace carefully** -- PowerShell's display can be
   misleading (it shows you what it parsed, which may include corrupted
   characters), so confirm the actual file content with `Format-Hex` or
   `Get-Content -Encoding Byte`.
