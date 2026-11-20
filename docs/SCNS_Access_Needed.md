# SCNS access needed by the Florida Course Repository

**For:** the SCNS committee and whoever maintains `flscns.fldoe.org`
**From:** Dr. Ron Eaglin, for the Florida Course Repository ([floridacourserepo.com](https://floridacourserepo.com))
**Written:** 2026-11-20

## In short

The Florida Course Repository is a free public site. It lists Florida public college and university
courses and publishes a curriculum guide for each course a visitor requests. Its most important source is
the **Statewide Course Numbering System**. SCNS tells us what the state says a course is, which public
institutions offer that exact course number, and what each institution calls it and how many credits or
clock hours it gives.

We read SCNS with a small script. **The site now returns HTTP 403 to that script** (a bot filter). We were
blocked again on 2026-11-20 and have been blocked off and on before. Our guide work now runs on a schedule
twice a week with nobody watching, so each block means guides wait for a person to step in, or are written
from an older copy of the data.

**We are asking for the four items below to be published where a script can download them.** Static files
on a schedule would be ideal: they put the least load on the SCNS server and are the simplest to keep
running. Item 1 matters most.

## What we need, most important first

| # | Item | Where it is today | How we use it | How often we need it |
|---|---|---|---|---|
| **1** | **The course inventory flat file** (`crslist.txt`, about 80 MB, fixed-width, every course at every institution), **plus the file-format document** (`File_Format_for_SCNS_Flat_File.doc`) | The download link on **Course Inventory** (`/PbCourseInventory`). It only works after a postback on `ctl00$hl_download` and after the terms dialog has been accepted in the same session | Which public institutions offer a course, each one's title, credits and clock hours, and whether the course is active or discontinued. It is the source of every "Offered at N Florida institutions" list on the site | **Weekly** (monthly would still help a great deal) |
| **2** | **Statewide course descriptions**: the state's description, prerequisites and transferability for each course number | **Statewide Course Detail Report** (`/PbStateCourseDetailReport`), which leads to `/Reports/CourseDescriptionReport?...&Type=StatewideCourse`, an SSRS ReportViewer we export one **prefix** at a time | The state's definition of the course, which every guide has to match or explain how it differs. Today we make one request per prefix | Weekly, **as one file for the whole state** |
| **3** | **Institution course descriptions**: each institution's own catalogue text for a course | **Course Descriptions** (`/PbCourseDescriptions`), with `Type=CourseDescriptions`, one institution and one prefix at a time | Tells us when an institution teaches a different subject under the same number, which happens often and is the main thing guides warn students about | Weekly, one file for all institutions (or one per institution) |
| **4** | **The institution list**: codes, names, SCNS IDs, and sector (state university, state college, technical college, private) | Built into the site's drop-down lists. The lookup we use returned **HTTP 500** on 2026-09-23 | Matching flat-file institution codes to names, and limiting the site to **public** institutions | Whenever it changes |

## What would solve it, best option first

1. **Static public downloads.** Put items 1–4 at fixed addresses, for example
   `https://flscns.fldoe.org/downloads/crslist.zip`, `.../statewide_descriptions.csv`,
   `.../institution_descriptions.csv` and `.../institutions.csv`, and refresh them on a regular schedule
   (weekly is enough). Each file is downloaded once per refresh and needs no session or terms dialog.
   **This is the best option for SCNS as well as for us**, because it replaces many report requests with
   one file download.
2. **An allowance for our script.** If the files have to stay behind the reports, let our requests through
   the bot filter. We can send a fixed user agent, for example
   `FloridaCourseRepo-Tools/1.0 (+https://floridacourserepo.com)`, or a key if you issue one. The script
   accepts the terms on every session.
3. **A small read-only API** that returns the same data as JSON (by course number, by prefix, by
   institution). This is welcome but more work for SCNS than option 1, and option 1 is enough.

## How much load we put on the site

- **About one session a week,** from the twice-weekly scheduled run plus Ron's occasional work.
- **One flat-file download a week,** and a few report requests per session (typically 1–10 prefixes).
- Requests come from one workstation, one at a time, and we are happy to keep within any rate you set.
- We **do not** redistribute the flat file. We publish what is drawn from it, with SCNS named as the
  source on each guide and career-path page.

## Why it matters

- **Students.** The site's job is to tell a student what a course number really means at each school.
  Without current SCNS data, guides are written from an older copy. The 2026-11-20 run used a copy saved
  on 2026-09-12, so a course discontinued since then can look as if it is still offered. That run found
  `EEL2130C` with one active and one discontinued (2025-07-11) row at the same institution and could not
  check which one is current.
- **Accuracy.** SCNS is the only source that is both statewide and per-institution. College catalogues
  cannot replace it: many are blocked to scripts too, and none of them say what other schools do.

## The same problem at FLDOE (for the same conversation, if it fits)

Since 2026-09-02, **`www.fldoe.org` has also returned 403** to our tools, including the CTE curriculum
framework pages and their PDFs (`/core/fileparse.php/...`). Those frameworks are the authoritative
source for every PSAV / clock-hour course. We have worked around this through CPALMS-CTE, which mirrors
the frameworks and still answers. Public access to the framework PDFs, or a static index of them, would
remove the workaround.

## On our side, once access is in place

- `Tools/scratchpad/scns.py` (the SCNS client) switches to the new download addresses or the agreed user
  agent. This is a small change, and the rest of the pipeline reads the same files it reads today.
- The scheduled check (`check-requests.cmd` → `Tools/check_requests.ps1`) then runs without the
  "SCNS blocked, used the saved copy" fallback.

Contact: Dr. Ron Eaglin, SCNS committee member.
