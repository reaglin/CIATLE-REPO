# Curriculum Guide Queue — Reference Guide

## Purpose

`queue.csv` is the master priority list for drafting and publishing SCNS academic course guides. The queue determines the order in which guides are created, tracks their current status, and records timestamps for auditing.

A guide must exist as a pushed JSON file in the `drafts/` folder before it can be used for any downstream purpose — curriculum mapping, equivalency evaluation, advising tools, etc.

---

## ⚠️ Before You Begin: PowerShell Execution Policy (every new terminal)

**Every new Windows PowerShell window requires execution policy bypass before any `.ps1` script — including `import_zip_to_drafts.ps1` — will run.** Open a Windows terminal in the `Tools/` directory and run this **first**, before any other queue or push command:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

This is scoped to the current PowerShell session only — system-wide policy is unchanged, and the bypass expires automatically when the window closes. Without it, Windows blocks unsigned `.ps1` scripts and the importer fails with a "scripts disabled" error.

After the bypass is set, the typical post-batch sequence is:

```powershell
.\import_zip_to_drafts.ps1
python generate_guide.py --push-from-queue --yes
python queue_mgr.py status
```

If you close the PowerShell window and open a new one, you must run the bypass command again.

---

## File Location

```
C:\Users\ronal\source\repos\CIATLE-REPO\Tools\queue.csv
```

---

## Column Map

| Column | Type | Description |
|---|---|---|
| `course_id` | String | SCNS course code, **no spaces** (e.g. `EET1035C`, `BCV0640C`) |
| `title` | String | Course title. **Enclose in `"..."` if the title contains a comma.** |
| `num_inst` | Integer | Number of Florida institutions offering the course. May be blank for rare or new courses. |
| `status` | Enum | Current state of the guide — see Status Values below. |
| `priority` | Integer | Processing order — **lower number = higher priority**. See Priority System below. |
| `added_utc` | ISO-8601 | When the row was added to the queue. |
| `drafted_utc` | ISO-8601 | When the guide draft was completed. Blank if not yet drafted. |
| `pushed_utc` | ISO-8601 | When the guide was published to `drafts/`. Blank if not yet pushed. |
| `notes` | String | Free-text label describing why the course was added or its batch origin. |

---

## Status Values

| Status | Meaning |
|---|---|
| `queued` | Not yet started. The course is waiting to be drafted. |
| `pushed` | Guide drafted and successfully published to `drafts/{SCNS_CODE}_guide.json`. |
| `error` | Draft was attempted but failed. `pushed_utc` is blank; the item needs to be retried. |

A course with `status=error` still appears in the queue and should be retried before adding a duplicate row.

---

## Priority System

Priority is an integer where **lower = higher priority**. There is no upper or lower bound enforced, but the working range is approximately 900–1000.

### Baseline formula

For standard queue entries, priority is derived from institution count:

```
priority = 1000 − num_inst
```

This means widely-offered courses (high `num_inst`) receive lower priority numbers and get done first — they benefit more faculty and students per guide produced.

### Priority tiers

| Priority range | Category | Notes |
|---|---|---|
| **< 929** | **Faculty Requests** | **Highest priority.** A faculty member is actively waiting on the guide to support a specific course section, articulation decision, or equivalency review. Because a real person is blocked, these jump to the front of the queue. Assign manually; do not use the formula. |
| 929 – 984 | High-volume gen-ed and PSAV | Standard high-enrollment courses. Most are already `pushed`. |
| 985 – 989 | Elevated project batches | Reserved for named projects that need a defined set of guides completed together. Do not use this range for individual ad-hoc requests — use Faculty Requests (< 929) instead. |
| **988** | Military Credits Equivalency Project | All SCNS courses required to complete pending military guide evaluations. Tagged `Military Credits Equivalency Project` in notes. |
| 990 – 998 | Lower-volume vocational and specialty | Mix of `pushed`, `error`, and `queued`. Formula-derived. |
| 999 | Default for new additions | Used when `num_inst` is unknown or the course was added outside a batch process. Update to the correct formula priority once `num_inst` is confirmed. |
| 1000 | Late-added pushed items | Courses added after the main batch that were pushed without a calculated priority. |

### Faculty Request priority assignment

When a faculty member requests a guide:

1. Assign a priority **below 929** (e.g., 900, 910, 920 — use spacing to allow future insertions).
2. Set `notes` to `Faculty request — [faculty name or department] — [brief reason]`.
3. Set `status` to `queued` and `added_utc` to the current timestamp.
4. Do not wait for batch processing — these should be drafted and pushed immediately.

Example row:
```
EEL4580,Wireless and Mobile Communications,,queued,910,2026-05-08T00:00:00Z,,,Faculty request — Dr. Smith EE Dept — satellite curriculum review
```

---

## Managing the Queue

### Adding a new course

1. Check that the course is not already in the queue (including with `status=error`).
2. Determine the priority:
   - Faculty request → below 929, manually assigned
   - Named project batch → in the 985–989 range, with a project note
   - Standard → `1000 − num_inst`; use 999 if `num_inst` is unknown
3. Add a row at the end of the file:
   ```
   course_id,title,num_inst,queued,priority,YYYY-MM-DDTHH:MM:SSZ,,,notes
   ```
4. Quote the title with `"..."` if it contains a comma.

### Updating after a successful push

Update the row in place:
- `status` → `pushed`
- `drafted_utc` → timestamp when drafting completed
- `pushed_utc` → timestamp when the file appeared in `drafts/`

### Handling an error

- Set `status` → `error`
- Leave `pushed_utc` blank
- Optionally append the error reason to `notes`
- Do **not** add a duplicate row — fix the existing one and retry

### Raising priority

Lower the `priority` number. If a course was at 999 and becomes part of a faculty request, move it to the appropriate sub-929 value and update `notes`.

### Checking what's queued (not yet started)

```powershell
Import-Csv queue.csv | Where-Object { $_.status -eq 'queued' } | Sort-Object priority | Select-Object course_id, title, priority, notes
```

Or with grep:
```
grep ",queued," queue.csv | sort -t',' -k5 -n
```

### Filtering by project

```
grep "Military Credits" queue.csv
grep "Faculty request" queue.csv
```

---

## Current Named Project Batches (as of 2026-05-08)

### Military Credits Equivalency Project — Priority 988

58 SCNS courses required to complete pending military-to-academic equivalency evaluations for Daytona State College. All tagged `Military Credits Equivalency Project` in notes.

Breakdown:
- 9 courses were previously queued at priority 999 — bumped to 988
- 49 courses newly added to the queue

Key course families included: EEL (satellite/comms), AVS (avionics), AMT (aviation maintenance), BCV (electrician), BCN (construction), ACR (air conditioning), ETM/ETI (industrial technology), AER (automotive), CJK (criminal justice), EEV (electronics vocational), ASC (aerospace), TTE/TCN/TRA (transportation/comms).

When the guides for these courses are pushed, return to the Military Credits Equivalency Project to run the remaining evaluations and update `index.html`.

---

## Notes on `drafts/` File Naming

Each pushed guide creates a file at:
```
C:\Users\ronal\source\repos\CIATLE-REPO\Tools\drafts\{SCNS_CODE}_guide.json
```

Where `{SCNS_CODE}` is the `course_id` value from the queue with no modification (spaces were already removed when the course was added). Example: `EET1035C_guide.json`.

Some older courses may have been published with or without a trailing `C` suffix. When an evaluation references a code like `BCV 0640C`, verify that the file on disk matches before running the comparison.
