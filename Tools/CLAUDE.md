# CLAUDE.md — Florida Course Repository Curriculum Guide Pipeline

This file conditions Claude sessions working on the [floridacourserepo.com](https://floridacourserepo.com) project. Read this before doing anything else. For tooling and command-line workflow, also read `README.md` in this directory.

---

## Project mission (the only thing that really matters)

**Develop solid, factually accurate curriculum guides for Florida college courses.** Every other concern — workflow, schema, file naming — is in service of this. A guide is "solid" when:

- It accurately reflects what Florida colleges actually teach for the course, derived from the SCNS framework and college catalogs.
- Required outcomes/topics reflect content common across institutions; optional outcomes/topics reflect institutional variation.
- It hedges honestly on uncertainty (especially for courses offered at few institutions).
- It cites Florida-specific context (FE/PE pathway, SCNS articulation, Florida industries, Florida-specific employer/regulatory landscape) where relevant and verifiable.
- It omits sections it cannot substantiate rather than fabricating content.

If a session ever drifts toward producing volume over quality, return here.

---

## Workflow: run it from this repo

Guides are written **directly into `Tools/drafts/`** from a Claude Code session in
`CIATLE-REPO`. The old chat → "Download All" → ZIP → `import_zip_to_drafts.ps1` bridge is
**no longer part of the loop**, and neither is the `Set-ExecutionPolicy` step that existed
only to let that importer run. Both still work if a batch ever arrives from a claude.ai
chat, but nothing here depends on them.

The `/guide` skill (`.claude/skills/guide/SKILL.md` at the repo root) drives the loop.
Do not skip the confirmation step.

1. **Identify the next candidates** — `python queue_mgr.py next-batch --n 5`. `queue.csv`
   is authoritative; `courses_2plus_institutions.csv` is the inventory it draws from.
2. **Present the proposed batch as a table** — course ID, institution count, title, notes.
   Flag any uncertainty (generic titles, content variation risk, low institution count).
3. **Wait for confirmation.** The user may approve, substitute, or remove items. Common
   reasons to substitute: faculty requests, non-public-college institutions, BAS courses
   that aren't true engineering courses.
4. **Write each guide** to `drafts/{COURSE_ID}_guide.json`. Research first — SCNS framework
   and Florida college catalogs — then write. Batch size is a judgment call; the old cap of
   5 came from chat output limits that no longer apply.
5. **Validate** — `python validate_drafts.py {IDS}`. This mirrors the server rules exactly,
   so a clean run means the push will not come back 400. **Never push past a `FAIL`.**
6. **Reconcile and push** — `python queue_mgr.py reconcile`, then
   `python generate_guide.py --push-from-queue --yes`.
7. **Confirm** — `python queue_mgr.py status`, and spot-check
   `https://floridacourserepo.com/api/v1/courses/{ID}/guide`. (`curriculumGuideUrl` staying
   `null` on the course endpoint is normal — it only populates once a course has published
   modules.)
8. **Provide sanity-check notes** in a brief table: course, credits, contact hours, file
   size — followed by short bullets flagging anything worth review (unusual hour counts,
   generic titles, novel content, institutional variation).

When in doubt about scope, **err toward fewer high-quality guides over more rushed ones.**

---

## ⚠⚠⚠ CAREER PATHS ARE THE WORK (Ron, 2026-09-17; still current 2026-09-21)

**Ron shifted the project to the development side and the feature is in.** His words:

> *"We are going to shift to the development side and create the career paths. These are all centered
> on CIP codes and the CIP codes become the framework for that page."*

⚠⚠⚠ **THIS — NOT GUIDE WRITING — IS WHAT A `Tools/` SESSION PICKS UP BY DEFAULT.**
**The work list is [`career_paths/QUEUE.csv`](career_paths/QUEUE.csv): 50 rows, ranked, each with its
CIP code, SOC code, cluster and `DIRECT`/`CHOICE` type.** Work it in rank order unless Ron says
otherwise, and set `status` to `published` (or `section:<slug>` where the row folded into another
path) as each lands.

| Cluster | Rows | State (2026-09-21) |
|---|---|---|
| **ENG** engineering | 1–10 | ✅ all published |
| **MFG** manufacturing / CTE | 11–27 | ✅ all published (2 became sections of another path) |
| **HLT** health | 28–36 | ✅ **all 9 published** |
| **CMP** computing | 37–40 | ⚠ **1 of 4 (Data Scientist) — now the head of the queue, and all three remaining are CHOICE paths** |
| **BUS** business · **LAW** · **EDU** · **PUB** | 41–50 | 1 of 10 (Lawyer) |

⚠⚠ **Guide work has not stopped — it is just request-driven and usually empty.** Check the
request queue every session (below); when it holds something, it outranks a path row, because a named
person is waiting. When it is empty, author the next path.

**Read [`CAREER_PATHS_PLAN.md`](../CAREER_PATHS_PLAN.md) §0** for what was built. What a *content*
session needs to know is short:

| | |
|---|---|
| **Author a path** | write `Tools/career_paths/<slug>.json`, then `python career_paths.py validate` |
| **Push it** | `python career_paths.py push <slug>` — ⚠ **a write to production, confirm with Ron** |
| **See what is live** | `python career_paths.py list` |
| **Browse the framework** | `/careers` → `/careers/area/{cip}` → `/careers/{slug}` |

⚠⚠ **A PROGRAMME LINK MUST SAY WHETHER IT IS A ROUTE (2026-09-19).** `programs: [{slug, note,
isRoute}]`, and `isRoute` defaults to true. **Set it FALSE when the programme does not lead to the
career** — Data Scientist names Mechanical Engineering *"Not a route into data science"*, and
under the heading *"Programs that lead here"* that contradicted itself. `career_paths.py validate`
now FAILS a row whose note says "not a route" while `isRoute` is still true.

### ⚠⚠ PROGRAMMES ARE NOW PUSHABLE CONTENT TOO (2026-09-19) — and they come FIRST

**Until 2026-09-19 a programme could only be added by REDEPLOYING the site**, because
`Data/Seed/programs.json` ships inside the build. **It has an admin API now**, so a programme is
authored and pushed exactly like a guide or a path. **Contract: [`PROGRAM_API.md`](PROGRAM_API.md).**

| | |
|---|---|
| **Author a programme** | write `Tools/programs/<slug>.json`, then `python programs.py validate` |
| **Push it** | `python programs.py push <slug>` — ⚠ **a write to production; it shows what changes and asks** |
| **See what is live** | `python programs.py list` · `python programs.py show <slug> --schools` |

⚠⚠⚠ **ORDER: PROGRAMME BEFORE PATH.** A career path names its programmes by slug
(`programs: [{slug, note}]`) and **the path push is refused 422 for an unknown one.**

⚠⚠ **A PROGRAMME OWNS NO SCHOOL LIST, so the CIP CODES YOU CLAIM *ARE* THE SCHOOL LIST.**
Which institutions offer it is derived from the IPEDS award table by CIP prefix at read time.
**Nursing as `51.38` alone finds 39 Florida institutions; adding `51.39` (practical nursing) finds
78 — and all 39 it was missing are technical colleges.** Ron: *"I do not want a school to be
excluded from being listed because their offerings are limited."* **Put the evidence in each code's
`note`**, and claim WHOLE LEVELS only (`15.`, `51.38`, `14.1901`) — a part-code like `14.1` would
sweep in 14.10 through 14.19 and is refused.

⚠⚠ **A PROGRAMME ALSO CARRIES `related` (2026-09-19), AND THE NOTE IS THE CONTENT.** Ron:
*"the similarities between mechanical engineering and aerospace engineering (any similar program)
should be noted as these are things students would not normally know when looking at a career…
Just like civil, structural, transportation, etc… are all very similar to civil."* A bare link
says only what the CIP tree already shows, so **the server refuses an empty note** — write the
thing the student could not know (*aerospace employers hire mechanical graduates in large numbers,
and mechanical is offered at eleven institutions against three*). Links are read in BOTH
directions, and a related slug must already exist or the push is refused 422.

✅ **40 programmes now exist** (2026-09-21), and every published path names one that actually leads
there — and no programme is left without a career. **Authoring programmes is ordinary content work, not a deploy** — but ⚠ widening
`cip.json` still is.

⚠⚠⚠ **A CROSS-PATH SUPERLATIVE GOES STALE THE NEXT TIME A PATH LANDS — do not write one
(learned twice, 2026-09-21).** Respiratory therapy was drafted claiming *"the fastest-growing
occupation on this site"* (data science is faster) and *"the worst course numbering on the site"*
(nursing and several engineering prefixes are more fragmented); both were caught by measuring
before publishing. **Then dental hygiene landed at $98,100 and invalidated the wage superlative on
TWO already-published paths at once**, which cost two extra pushes to reconcile.

| ❌ Do not write | ✅ Write |
|---|---|
| "the highest wage-to-training ratio anywhere on this site" | "the highest median of any TWO-YEAR route on this site" — a bounded class you can re-check in one command |
| "the worst numbering on the site" | the measurement, plus two or three named comparators |
| "the fastest-growing occupation here" | the federal figure and its projection decade |

⚠⚠ **If a comparative is worth making, BOUND IT and NAME THE COMPARATORS in the same
sentence** — a bounded claim can be re-verified, and a reader can see what it is being compared
against. ⚠ **And before publishing any comparative, grep the other paths for the claim you are
about to contradict:**

```bash
python -c "import json,glob,re;[print(f,m) for f in glob.glob('career_paths/*.json') for m in re.findall(r'median wages?[^<]{0,40}', json.load(open(f,encoding='utf-8')).get('bodyHtml') or '')]"
```

⚠⚠⚠ **THE ONE RULE: A PATH IS CURATED, NEVER DERIVED.** Every course is placed by an author
with a **required** stated reason. **Do not** build a course list by parsing prerequisites, by
course-code arithmetic, or from the institution CIP data. Two hundred batches established that a
course number does not identify a course; a mechanically assembled path would be confidently wrong on
exactly the cases this file spends 3,000 lines documenting.

⚠⚠ **The institution CIP data is an AUTHORING AID and is never published as fact.** 25,412
course→CIP assignments were harvested, and **7% of multi-carrier courses are classified into
DIFFERENT CIP FAMILIES by different institutions** — worst in the broadest subjects (`PHC` 27%
dominant, `FIL` 32%, `NUR` 49%). It decides which branches of the tree to show. Nothing else.

### ⚠⚠ What this means for guide work: paths GENERATE demand

**The 2026-09-12 note predicted this and it is now real.** A path names courses; courses a path names
and the catalog does not carry come back in the push response as `unlistedCourses`, and **a path that
links to a page that is not there is a broken promise to the reader.**

- ⚠ **Listing those courses is work the path creates**, and it ranks with a visitor request — a named
  page depends on it.
- ⚠ **A guide-less course on a path is NOT automatically guide work.** It renders a **Request Guide**
  link, and the request queue stays the demand signal. **Do not treat a path’s course list as a
  writing queue.**

⚠ **First instance, already open:** the Registered Nurse path names `STA2023` and `ENC1101` — the
identifiers **52 and 51 public institutions carry** — and the site lists only `STA2023C` (1 carrier)
and `ENC1101C` (3). **`REVIEW_QUEUE.md` item 106**, and it needs Ron because two live guides sit on
the minority ids.

### ⚠⚠⚠ TWO KINDS OF CAREER PATH, AND THE SECOND IS WHERE THE VALUE IS

**Ron, 2026-09-17, and this governs how every path in `QUEUE.csv` is researched:**

> *"Other than the career and technical education (including curriculum frameworks) that are
> specifically tied to CIP codes, most college level programs will not explicitly list CIP codes.
> In researching career paths that are not specifically tied to a program, you will need to do the
> same thing we did with Lawyer and search for the common majors that lead to that specific career
> path. **This is actually the most valuable of the documentation we do.** The reason is that
> careers that have specific programs are easy to develop a career path, you start the major, you
> are on that path. In the case of careers that do not have a specific associated major, **the
> student must make decisions on major.** The data you presented for law (success of students in
> various majors) is very valuable to those students."*

| | **DIRECT** — 40 of the 50 | **CHOICE** — 10 of the 50 |
|---|---|---|
| What it is | one programme; enrolling in it puts you on the path | ⚠ **no single required major — the student must decide** |
| Examples | Registered Nurse, Welder, Mechanical Engineer, Dental Hygienist | **Lawyer**, Financial Analyst, Data Scientist, HR Specialist, Construction Manager |
| The CIP code | **IS the programme**, and for CTE it is published | a **destination**; the feeders are researched |
| Research | the programme, its accreditor, its licensure, its clock hours | ⚠⚠ **the majors people who reach it ACTUALLY HOLD, with outcome data wherever any exists** |
| Cost to write | fast | slow |
| ⚠ Value to a student | tells them what the programme involves | ⚠⚠⚠ **answers a decision they are actually facing, and nothing else answers it** |

⚠⚠⚠ **So do NOT let the DIRECT ones crowd out the CHOICE ones because they are quicker.**
A DIRECT path largely restates what the programme already tells a student. **A CHOICE path tells
them something no catalogue, adviser sheet or programme page will.**

#### ⚠⚠ THE RESEARCH IS THE COST OF A PATH — the writing is not (2026-09-19/20)

**Three paths were authored on 2026-09-19 (Environmental, Computer Hardware and Materials Engineer)
and the work that made them worth publishing was the evidence pass, not the prose.** Ron, 2026-09-20:
**more research is needed for additional paths.** Reckon on roughly a session each, and run these
six steps before writing a word:

1. **O*NET and BLS for the SOC code** — and ⚠ check whether they DISAGREE. On environmental
   engineering O*NET says *"average (3% to 4%)"* on the 2024–34 projections and BLS says *6%,
   faster than average* on the 2025–35 ones. **Quote both and say they differ.**
2. **The programme footprint from IPEDS by CIP** — how many Florida public institutions, and
   ⚠ at which LEVEL. Materials engineering has four institutions and only TWO at bachelor's, which
   changed the whole shape of that path: the honest route is mechanical or chemical first.
3. **A carrier count from the SCNS flat file for EVERY course named** —
   `python scratchpad/carriers.py ENV4001 CWR4202 …` or `--prefix ENV`. This is where the variant
   notes come from, and it produced the finding that **no environmental engineering course is
   carried by more than four of the nine institutions awarding the degree.**
4. **The licensure and accreditation reality**, cited to statute where there is one (s. 471.013,
   F.S. for the four-versus-six-year PE experience rule).
5. **For a CHOICE path, the entrant-major dataset** by the Lawyer method below — and ⚠ where none
   exists, say so plainly rather than inferring one.
6. **Any course the catalog does not carry, LISTED FIRST** — `python scratchpad/list_missing.py
   COP3530 … --push` builds each from the flat file (modal title, modal credit, every public
   carrier as an offering) and sends it. **Thirteen courses needed this for the three new paths.**

⚠ **And a path is not always the right answer.** Ocean engineering was dropped as a path on
2026-09-20 — *"Use civil for ocean"* — because two institutions award in it, only one at
bachelor's, and FAU's ocean courses are carried by FAU alone. **A one-institution path would have
misdescribed the field; a coastal section inside Civil Engineer describes it correctly.**

#### The CHOICE method — what `Lawyer` established

1. **Find the body that collects entrant data** and read its own numbers, not a summary of them.
   For law that is LSAC's *Applicants by Major*. **Prefer a count over an opinion piece.**
2. **Take a stated cut** — Lawyer used *every major at ≥1% of applicants*, which is a rule rather
   than a feel — and file the path under each as a `cipCodes[]` anchor with the share in the note.
3. ⚠⚠ **Look for the OUTCOME data, not just the counts.** The counts say where students come
   from; the outcomes say how they fare. On Lawyer this produced the finding that mattered: the
   most law-SOUNDING majors post the LOWEST mean LSAT.
4. ⚠ **Quote the source's own caution when it prints one**, and keep the claim narrow. LSAC warns
   against causal inference, so the path claims only that the data gives no support to picking a
   major *because its title contains the profession's name*.
5. **Then give the skills** the destination actually tests, and choose courses for those.

⚠ **Where no entrant-major dataset exists**, say so plainly and fall back to what employers and
professional bodies state they look for — **but look first.** Accrediting bodies, licensing boards,
professional associations and federal surveys collect more of this than is generally realised.

#### ⚠⚠ For the DIRECT ones, the CIP code is PUBLISHED — do not infer it

**Florida CTE programmes are tied to CIP codes explicitly in the FLDOE curriculum frameworks**
(`fldoe.org/academics/career-adult-edu/career-tech-edu/program-resources.stml`), which also carry
the occupational completion points and clock hours. **That is the authority for every `MFG` row in
the queue** — and `SOURCES.md` already ranks the frameworks Tier 1 for PSAV guides.

⚠⚠⚠ **BUT `fldoe.org` HAS RETURNED 403 TO THIS PROJECT SINCE 2026-09-02**, re-probed and
still 403 on 2026-09-17 with a browser user-agent, on the `.stml` pages AND on
`core/fileparse.php/….pdf` documents. **CPALMS-CTE now mirrors the frameworks (`cpalms.org`,
`cte.cpalms.org`) and answers 200, but is client-rendered — the course content is not in the
HTML.** **So the single best source for the sponsor-emphasis half of the queue is currently
unreadable by tooling.** Ask Ron to supply the framework PDFs rather than inferring CTE CIP codes
from course prefixes — inferring is exactly what the "curated only" rule forbids.

### ⚠⚠⚠ A PATH CAN HAVE MANY CIP CODES — use the programmes people ACTUALLY come from

**Ron settled this on the Lawyer path (2026-09-17):**

> *"Search on the top academic programs that people that go into law get and use those as the CIP
> codes that would go with the career path of lawyer."*

**So `cipCode` is the PRIMARY anchor — the destination — and `cipCodes[]` carries the rest, each with
a `note` holding the EVIDENCE.** A path is then found by browsing ANY of them.

```json
"cipCode": "22.01",
"cipCodes": [
  { "cipCode": "45.10", "note": "Political Science — 12,967 applicants, 17.5% … (LSAC, 2018–19)." },
  { "cipCode": "42.01", "note": "Psychology — 3,850 applicants, 5.2% (LSAC, 2018–19)." }
]
```

⚠⚠ **THE NOTE IS THE EVIDENCE, NOT A JUDGEMENT.** A code goes on a path because **a source says
students actually come from it** — for Lawyer, LSAC's own applicant counts. **Never because the
subject sounds related.** `career_paths.py validate` warns on a code with no note for exactly this
reason.

⚠ **Pick the cut from the data and say what it is.** Lawyer takes every LSAC major at **≥1% of
applicants** — sixteen of them — which is a stated rule rather than a feel.

⚠⚠ **A code must be in the SEEDED TREE or the push returns 422.** Two of Lawyer's sixteen
(`22.00` Legal Studies, `45.04` Criminology) had no course-CIP evidence, so they were added to
**`build_cip_seed.py`'s `EXTRA_GROUPS`** with the reason on the record, and `cip.json` regenerated.
**That is the documented 4-digit coverage limit biting — widen it deliberately, never by loosening
the evidence rule.**

#### ⚠⚠ And the finding that came out of it, which generalises

**The most OCCUPATION-SOUNDING major is frequently not the best preparation, and the data says so.**
LSAC's mean highest LSAT by major: **Criminal Justice 146.6, Pre-Law 148.5, Legal Studies 149.8**
against **Economics 159.7, Philosophy 157.9, History 156.8**.

⚠ **Quote the source's own caution when it prints one.** LSAC's report says it *"would be a mistake
to infer… that any one major is better than another"*, and the path quotes that verbatim before
drawing any conclusion. **The honest claim is narrow: it gives no support to choosing a major BECAUSE
its title contains the profession's name.** ⚠ **Expect the same shape on other paths** — the
"pre-med", "pre-law", "criminal justice" style of major exists across the catalogue.

### ⚠ Where a path’s content comes from

**The guides already wrote it.** A path is assembled from what the batches accumulated — SOC codes,
licensure and accreditation findings, the divergence notes, the sector and ladder rules. The Registered
Nurse path is the worked example: its `credentialNote` is the batch-215 rule (**accreditation outranks
credit**), its prerequisite warnings are the `BSC`/`APK` prefix divergence, its `NUR4286-UWF` entry is
a published one-number-two-subjects split. ⚠ **`variantNote` is where a divergence finding reaches a
path page** — use it.

---

## ⚠⚠⚠ GUIDE DIRECTION (Ron, 2026-09-17): REQUESTED COURSES ONLY

⚠ **Scope note (2026-09-21): this section governs GUIDE WRITING, not the session.** The session's
default work is **career paths** (section above). Read "there is no guide work" as "go author the next
path", never as "there is nothing to do".

**This supersedes the "finish `queue.csv` first" half of the 2026-09-11 direction below.** Ron's words:

> *"the plan is to keep track of the items (mark them) that need my attention, but our main focus is
> going to be on **requested curriculum guides and we will only tackle those courses that have been
> requested**. We will still need those notes to handle the situation of one of the marked courses
> being requested."*

**Three things follow.**

1. ⚠⚠⚠ **`queue.csv` is no longer the work list.** It stands at 108 `queued` rows and they stay
   there. **Do not pick a prefix off it and start writing.** The work is
   `GET /api/v1/queue/guides?status=waiting`, and **when that queue is empty there is no guide work** —
   say so plainly, then move to the career-path queue rather than finding guide work that nobody asked for.
2. **`REVIEW_QUEUE.md` keeps growing and keeps being marked.** It is no longer a side-channel: under
   request-driven working it is **the only warning you get** that a requested course is already known to
   be a problem.
3. ⚠⚠ **A flagged course now arrives WITHOUT WARNING.** In queue-driven mode you met a held course by
   working steadily toward it and the note turned up in passing. **A public request arrives out of
   order, on any number, at any time.**

### ⚠⚠⚠ So the FIRST command of every session is now this one

```bash
python review_lookup.py --requests
```

**It reads the live request queue and cross-references every waiting course against all 105
`REVIEW_QUEUE` items** — 361 courses are named across them. It separates items **ABOUT** a course from
items that merely **mention** it, follows **bare/`C`/`L` twins and sequence partners**, and prints
**⚠⚠ HELD — ASK RON BEFORE WRITING** where an open item says the course was pulled, held, or needs a
decision.

⚠ **A HELD course that has been REQUESTED is exactly the case Ron's instruction anticipates, and it is
not a blocker — it is a question for him.** **Report the request, name the item, say what the block is,
and ask.** A visitor request is the strongest demand signal the project has; it may well be the reason
to resolve a long-held item. **Do not write it silently, and do not silently skip it either.**

Other tools for the same file: `review_index.py` regenerates the decision index at the top of
`REVIEW_QUEUE.md` (run it after adding an item), and `review_lookup.py --all` lists every course the
file mentions.

---

## ⚠⚠ Superseded in part — Direction (Ron, 2026-09-11): LIST courses as you go; guides follow the queue and then requests

Ron's words:

> *"Guideless courses will remain. We will finish the existing queue and shift to requests as we work on
> programs and career guides. A top priority will be picking up any courses we see at institutions along
> the way and list them (no guide)."*

**Four things follow, and the last one is the change in working practice.**

1. **A course without a guide is a finished outcome, not a backlog.** The ~800 guide-less Engineering
   Technology courses stay as they are. **Do not treat `hasGuide=false` as a work list.**
2. ⚠⚠⚠ **SUPERSEDED 2026-09-17 — see the section above.** This read *"Finish `queue.csv`, then shift
   to visitor requests."* **The shift has now happened: requests are the ONLY source of guide work, and
   `queue.csv` is not to be worked through.** The rest of this section still stands.
   ⚠⚠ **Update (Ron, 2026-09-12): the next major phase is CAREER PATHS, and courses
   identified as important to a career path but lacking a guide will land in the queue
   AUTOMATICALLY.** So the queue stops being purely catalog-derived and becomes partly
   pathway-derived — **a third demand signal after faculty and visitor requests.** Keep working
   `queue.csv` until then.
   ⚠ **Also settled 2026-09-12: data-quality and verification findings are DEFERRED to a
   verification pass**, an upcoming phase and part of continuous site maintenance. **Record them in
   `REVIEW_QUEUE.md` and keep going** — do not stop a batch to chase them.
3. **Programs and career paths** become the next build direction (`CAREER_PATHS_PLAN.md`,
   `COURSE_CATALOG_PLAN.md` phase 5) — and both need a complete course list far more than they need more
   guides.
4. ⚠⚠ **TOP PRIORITY, and it applies to every batch from now on: every course you SEE while researching
   gets LISTED.** Writing a guide means reading SCNS and institution catalogs, and that reading surfaces
   hundreds of courses the site does not hold. **Add them — title, credits, per-institution offerings — with
   no guide**, over `POST /api/v1/courses/batch` (`COURSE_API.md`).

### How to do it, at the end of every batch

The SCNS flat file already holds every course at every institution, so **the marginal cost of listing a
whole prefix once you have fetched it is close to zero.** Standing practice:

1. **Institutions first**, with names and sectors: `POST /api/v1/institutions/batch`. Send once; repeats are
   `unchanged`.
2. **Build course rows for every prefix the batch touched** — not only the courses you wrote guides for.
3. **Public institutions only** (`scns.is_public`), per the 2026-09-11 scope rule — ⚠⚠ which **INCLUDES DISTRICT TECHNICAL COLLEGES since 2026-09-20** (`sector_of` now answers `TECH`). They were excluded by accident, not by decision, and with them the whole CTE sector.
4. `title` = the most common institution title, title-cased; `stateTitle` = the SCNS statewide title;
   `creditHours` = the modal integer credit; `offerings[]` = every public institution with its own title and
   credits.
5. Push in batches of **≤ 500**, log every `failed` result, and reconcile with
   `GET /api/v1/courses/catalog?updatedSince=<run start>`.

⚠ **Watch the two traps.** `replaceOfferings` defaults to **`true`**, so send a course's full offering list
or you will delete the rest. And **a course upsert DOES overwrite an existing title** — which is wanted when
the stored title is the course id placeholder, and is why the title you send must be a real one.

⚠ **Shell numbers (`x9xx`) are still LISTED even though they are skipped for guides.** The skip list governs
what gets a guide; it does not govern what exists. A student can enrol in a special-topics course, so the
catalog should show it.

---

## ⚠⚠ The course catalog — deployed 2026-09-11. Read this before the first batch.

**What changed:** a course no longer has to have a guide. The site now lists **every course that exists**,
with or without one, and visitors press **Request Guide** on the ones that are missing. The contract is
[`COURSE_API.md`](COURSE_API.md) (courses) and [`RESOURCE_API.md`](RESOURCE_API.md) (resources); the
server-side plan is `COURSE_CATALOG_PLAN.md` at the repo root. **Guide content rules did not change** —
everything below this section still governs what a guide says.

### ⚠⚠⚠ Visitor guide requests are the new top priority

Requests are one anonymous click on a guide-less course page. **They are the strongest demand signal the
project has ever had — a named person wanted that guide** — and they outrank everything except a faculty
request. Read them with no token:

```bash
curl -s "https://floridacourserepo.com/api/v1/queue/guides?status=waiting"   # most-requested first
```

Each item carries `rank, courseId, title, requestCount, firstRequestedUtc, status, hasGuide, isListed`.
The same list is public at `https://floridacourserepo.com/queue/guides`.

⚠ **`isListed: false` means someone asked for a course the site does not list yet.** Send its base data
(§ below) before or with the guide, or the request has nothing to attach to.

**Check this queue at the start of every session**, before `queue_mgr.py next-batch`. A published guide
closes its requests automatically; `queue_mgr.py import-requests` still works and still marks them `Queued`.

### ⚠⚠ Send the course's base data with every guide

A guide push still creates a missing course — but with **the course id as a placeholder title**, which is
why so many pages read `EEE3300` instead of *Electronics I*. Fix it in the same batch:

```
POST /api/v1/courses/batch      # ≤ 500 courses, each validated on its own
PUT  /api/v1/courses/{courseId} # one course
```

```json
{ "courseId": "CET1112", "title": "Digital Electronics and Microprocessors",
  "stateTitle": "DIGITAL ELECTRONICS & MICROPROCESSORS", "creditHours": 3, "contactHours": 45,
  "offerings": [ { "institution": "DSC", "title": "DIGITAL ELECTRONICS & MICROPROCESSORS", "credits": 3 } ],
  "replaceOfferings": true }
```

Field rules that bite:

| Field | Rule |
|---|---|
| `courseId` | `^[A-Z]{3}\d{4}[A-Z]?(-(SCNS\|[A-Z]{2,5}))?$` — **the `-SCNS` / `-<INST>` split is in the contract**, so a variant id is a first-class course |
| `title` | **required**, ≤ 300, written as sent. Sending the course id as the title never replaces a real one |
| `creditHours` / `contactHours` | **0–20 / 0–3000 on the COURSE** — wider than the guide's own 0–12 / 0–1500. A PSAV clock-hour course is still `credits: 0` in the **guide** |
| `offerings[]` | ≤ 250; `institution` is a short code, with that school's own `title`, `credits` and `clockHours`. **This is where the institution list finally lives on the site — and it is the same per-school data the guide's hours table must be built from** (see *RESOLVE THE RANGE* below; build both in one pass so they agree) |
| `replaceOfferings` | defaults to **`true`** — omitted offerings are **deleted**. Send the whole list or pass `false` |
| null / omitted | left unchanged on an existing course (except `title`) |

⚠ **Never `DELETE` a course that has a guide** — it returns `409 COURSE_HAS_CONTENT`. A course that stopped
being offered gets `isActive: false`.

⚠ **Send institutions first**, with names: `POST /api/v1/institutions/batch` with `{code, name, sector,
scnsId}` (SCNS `institution_map()` supplies them), or the site shows bare codes.

### The 806 guide-less courses already on the site

The deployment found **806 courses with no guide already in the database, and every one of them is an
Engineering Technology prefix** — which is exactly Ron's priority scope (2026-09-09):

| ETI | CET | EET | ETS | ETD | ETP | TDR | EEV | ETC | ETM | ETG | EER |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 147 | 141 | 112 | 88 | 78 | 66 | 40 | 36 | 35 | 33 | 18 | 12 |

They carry real titles but **no offerings at all** (`offeringCount: 0`), so the institution data has to be
sent. Known bad data to correct while passing through: **`EEV0360L` has `creditHours: 30`** (those are clock
hours — PSAV, so `credits: 0` + `contactHours: 30`) and **`ETC5605` is graduate-level**.

⚠ **Prefix completion (2026-09-09) applies to these**: `hasGuide=false` on the catalog endpoint is now a
better prefix worklist than `queue.csv`, because it is what the site actually shows a visitor as missing.

```bash
curl -s "https://floridacourserepo.com/api/v1/courses/catalog?prefix=CET&hasGuide=false&pageSize=1000"
```

### A stub is not a guide

Publishing modules for a course with no guide creates a placeholder guide titled **`Not Completed`**
(`CurriculumGuide.StubTitle`). It never counts as a guide and never blocks a guide request, and the
`hasGuide` filters ignore it. **Do not treat a course as done because it has a guide row.**

### Course resources are a second, separate loop

Visitors and vendors suggest links on `/courses/{id}/resources`; an AI session reviews them, writes the
summary and lists them. That loop is **`RESOURCE_API.md` + `resources/APPROVAL_RULES.md` + the `/resources`
skill** — not this file. It does not interleave with guide writing; run it as its own session.

---

## ⚠⚠⚠ CIP CODES ARE THE CAREER-PATH ANCHOR (Ron, 2026-09-16)

Ron's direction, verbatim:

> *"Once we complete the queue we are going to look at career paths. All the careers will be bound to
> CIP codes https://nces.ed.gov/ipeds/cipcode/browse.aspx?y=55 and that will be the anchor for the
> career paths."*

**That is the NEXT phase, not this one — finish `queue.csv` first.** It is recorded here because it
changes what current batches should CAPTURE, in exactly the way the 2026-09-11 "list courses as you
go" direction did.

### ✅ What is already banked

**`cip_map.py` harvests course → CIP from the Coursedog caches, which are the ONLY Florida source
exposing a per-course `cipCode`.** As of 2026-09-16 it maps **25,412 courses**:

| Cache | Rows | With a usable CIP |
|---|---|---|
| FIU | 27,923 | **25,188** |
| FAU | 7,127 | **7,120** |
| NWFSC | 1,802 | 708 |
| ⚠ FSCJ | 22,698 | **0** |

⚠⚠ **Two format traps, both real in the data and both handled in `cip_map.py`:** FIU writes CIP
**dotted** (`16.1101`) while FAU and NWFSC write it **undotted** (`240101`); and **FSCJ's field is
populated on 2 rows out of 22,698, both with the placeholder `9999999999`**. **A 10-digit value is not
a CIP code — treat anything that is not 6 digits as absent rather than coercing it.**

### ⚠⚠⚠ The finding the career-paths build must design around

**CIP is MORE stable than the course number — but it is not stable enough to be trusted alone.**
Measured over the **1,500 courses carried by two or more of these institutions**:

| | Count | Share |
|---|---|---|
| Institutions **agree** exactly | 763 | 51% |
| Disagree **within the same 2-digit family** | 631 | 42% — granularity, benign |
| ⚠⚠ **Disagree across DIFFERENT families** | **106** | **7% — the serious cases** |

⚠ **The first number to quote is 93%, not 49%.** A raw "half of them disagree" count is misleading,
because most disagreement is one institution choosing a finer sub-code than another. **Compare at the
2-digit family level first, then look at the residue.**

**But the residue is severe, and these are real:**

| Course | Classified as |
|---|---|
| ⚠⚠⚠ **`ART1300C`** (Drawing) | FAU **50.0701 Fine Arts** · NWFSC **13.1302 ART TEACHER EDUCATION** |
| ⚠⚠⚠ **`ART2501C`** | FAU **50.0701 Fine Arts** · NWFSC **36.1096 LEISURE AND RECREATIONAL ACTIVITIES** |
| `ARH2050`/`ARH2051` | FAU **24.0199 Liberal Arts** · FIU + NWFSC **50.0703 Art History** |
| `ANT2100` | FAU **45.0201 Anthropology** · NWFSC **30.0000 Multi/Interdisciplinary** |
| `ADV3008` | FAU **52.0101 Business** · FIU **09.0101 Communication** |

⚠⚠⚠ **The same drawing course is fine art at one institution, teacher education at another and a
recreational activity at a third. A pathway that routes students by CIP alone would send those three
students to three different careers on identical coursework.**

**So the CIP anchor needs the same treatment the course number needed:**

1. **Anchor the CAREER on a CIP code** — that is what Ron specified and it is sound, because the
   career end of the mapping is where CIP is authoritative.
2. ⚠⚠ **Do NOT infer a COURSE's pathway membership from its institution-assigned CIP alone.**
   A course's CIP is *that institution's* classification of it, and it varies.
3. **Where institutions disagree, record BOTH rather than picking** — the disagreement is data about
   how the course is actually used, and it is exactly the kind of fact this project exists to surface.
4. ⚠ **Compare at the 2-digit family before the 6-digit code**, or 42% of benign granularity will be
   reported as conflict.

⚠⚠ **AND THE DISAGREEMENT IS NOT ONLY BETWEEN INSTITUTIONS — IT HAPPENS INSIDE ONE (batch 230).**
FAU tags `FIL4036`, `FIL4037`, `FIL4364` and `FIL4106` as **50.0602 Film/Cinema/Video Studies** and
`FIL3803` *Film Theory* as **09.0702 Digital Communication/Media** — **same department, same prefix,
two CIP families.** ⚠ **So a single institution's CIP assignment is not internally consistent either,
which strengthens the case against treating any one course→CIP edge as authoritative.**

⚠ **Standing practice from now on: when a batch touches a Coursedog school, the CIP data comes for
free — `cip_map.py` re-runs in seconds off the caches.** Keep the caches current and the anchor
builds itself. See `REVIEW_QUEUE.md` item 103.

---

## Priority hierarchy

Apply in this order:

1. **Faculty requests** always go to the top of the queue. These are unpredictable and come up mid-session. When the user says "add EGN3214 because a faculty member requested it," that course supersedes the strict-priority pick. Custom specifications from faculty (e.g., "Python only, AI-integrated, two-half structure") are followed precisely.
2. **⚠⚠ Visitor guide requests** (new 2026-09-11) — `GET /api/v1/queue/guides?status=waiting`, most-requested first. Someone pressed **Request Guide** on a course page because they wanted it. **Check this queue before every batch**; a request outranks any catalog-derived row. See the course-catalog section above.
3. **Engineering and Engineering Technology prefixes**, completing each prefix, per Ron's 2026-09-09 direction below — single-institution courses included.
4. **Strict priority by institution count** (descending) within `courses_2plus_institutions.csv`, with course ID as tiebreaker. Higher institution count = wider applicability = stronger signal that the guide will help more students.
5. **Human judgment overrides.** The user may demote or remove courses for reasons including:
   - Course offered only at non-Florida-public institutions (e.g., Keiser private, FL Tech private). The repository serves Florida public colleges and SUS institutions. ⚠⚠ **Settled 2026-09-11, and it now governs SEARCH as well as selection:** *"In doing search and fetch to determine eligibility for a curriculum guide we will only do public institutions&hellip; we are not adding private institutions as part of our adding data."* So **a private institution's offering is not a reason to write a guide, and is not added to a course's offerings either.** ⚠ **A visitor request overrides it:** *"If one happens to make it up to the list and gets queued for a guide, we will override the rule and supply one."* The override is applied by **queueing that course**, never by widening the filter.
   - Course is part of a BAS or applied-degree program that isn't a true engineering degree (Engineering Technology BAS courses are fine; non-engineering BAS courses that happen to use an engineering prefix are out of scope).
   - Course is a shell (internship, special topics, independent study, thesis, dissertation, supervised research). Default is to skip these.
6. **When uncertain, ask.** Never silently substitute. Confirm before generating.

---

## Schema (required JSON structure)

Every guide is a JSON file with these six required top-level keys, plus the optional
**`offering_notes`** (below):

```json
{
  "title": "Short descriptive guide title",
  "html_content": "<full HTML — see conventions below>",
  "credits": 3,
  "contact_hours": 45,
  "prerequisites": "MAC2311 or equivalent" | null,
  "version": "1.0"
}
```

### ⚠⚠ `offering_notes` — the seventh field (Ron, 2026-09-11)

**An additional field carrying, per school, the title THAT school uses and the hours it requires.** It is
the structured form of the *RESOLVE THE RANGE* rule below: the six scalars describe the course, and this
describes where it is actually taught.

```json
"offering_notes": {
  "summary": "All five institutions carry it at 3 credits. No institution publishes a contact-hour figure.",
  "hours_source": "derived",             // published | derived | mixed
  "derived_contact_hours": 60,
  "derivation": "Florida convention: 45 hours for a 3-credit lecture course, 60 for a 3-credit C course.",
  "offerings": [
    { "institution": "GCSC", "institution_name": "Gulf Coast State College",
      "title": "Digital and Computer Circuits", "credits": 3, "contact_hours": null,
      "note": "Offered spring term only. Prerequisite MAC1105 and EET1084C, minimum grade C." }
  ]
}
```

- ⚠⚠ **PUBLIC institutions only** (Ron, 2026-09-11, superseding his earlier answer): list the Florida
  College System, State University System **and DISTRICT TECHNICAL COLLEGE** offerings. **A private,
  for-profit or out-of-state institution carrying the SCNS number is not added.** Filter with
  `scns.is_public(code)`.
- ⚠⚠⚠ **THE TECHNICAL COLLEGES WERE MISSING UNTIL 2026-09-20** (`REVIEW_QUEUE` item 109, Ron's
  decision the same day). `is_public()` answered SUS or FCS only, so **every offering list this project
  has ever built dropped them** — and they are where Florida teaches automotive, welding, HVAC,
  industrial maintenance and practical nursing. The measurement: the nine `AER` automotive courses are
  carried by ~40 institutions and **only two are state colleges**. `sector_of()` now answers
  **`TECH`** as a third public sector, kept separate because a technical college awards clock-hour
  certificates rather than degrees and sits outside the A.A. transfer machinery.
- ⚠ **No `sector` field.** `Institution.Sector` on the site is the owner of that fact (Ron, 2026-09-11) —
  the guide JSON carries the institution code and the site joins. `scns.sector_of()` still exists for
  filtering and for checking a code, but its value does not go in the draft.
- ⚠⚠ **`credits` is an INTEGER.** The SCNS flat file writes `3` and `3.0` for the same value — that is a
  fixed-width export artefact, not a difference. `mkguide.py` coerces a whole float; `validate_drafts.py`
  **rejects a non-integer credit outright**. A genuine in-school range (`3-4`) leaves `credits` null and
  says so in `note` — **Ron settled this on 2026-09-11: the note is sufficient, no min/max pair.**
  Instances so far: `CET1178C` is 3-4 at South Florida State, `CET2949` is 1-4 at Daytona State; both are
  variable-credit capstone or special-topics numbers.
- `title` is **that institution's own title**, not the statewide one — the divergence signal, and the thing
  a student actually sees on a schedule.
- `contact_hours` per school is the **published** figure or null. Never put a derived figure in a school's
  row: derived numbers go in `derived_contact_hours` with `hours_source: "derived"` and the `derivation`
  spelled out.
- ⚠ **The server does not carry this field yet.** `PUT /courses/{id}/guide` takes the six scalars and drops
  anything else, so a draft carrying `offering_notes` publishes normally and the field simply does not
  appear on the site until the server change lands (`Deployment/PENDING_SERVER_CHANGES.md`). **Until then,
  write the same content into the guide HTML as an `<h3>Offering Notes</h3>` section too** — that is what
  readers see today, and it makes the later retro-fit a mechanical extraction.
- **Source it from the SCNS flat file**, which carries per-institution `credit`, `clock_hours` and
  `inst_title` for every offering. ⚠ Its titles are **all upper-case**: when title-casing them, test small
  words (`and`, `of`, `the`) **before** any "short and upper-case means acronym" heuristic, or the heuristic
  fires on `AND` and `THE`. An all-caps source carries no case signal.

⚠ **Existing guides do not have this field.** Ron, 2026-09-11: *"we will have to go back and redo a lot of
the old guides, but that will be a task for much later."* **Do not start a retro-sweep** — add the field to
new guides and to any guide being republished for another reason.

---

- `credits=0` is valid for **two entirely different things**, and they need different explanations:
  - **PSAV clock-hour courses** — `contact_hours` carries the real measurement.
  - ⚠⚠ **ZERO-CREDIT LABORATORIES** (found batch 198, `BCH3034L` at UWF) — a corequisite laboratory whose
    credit sits on its paired lecture. **The work and the hours are entirely real; only the accounting
    differs.** A guide for one must say: it does **not** count toward full-time enrolment (which matters for
    financial aid, athletic eligibility and student visas), the time commitment is real, it may still be
    graded, and **transfer is awkward because there is no credit to transfer.**
  - ⚠⚠ **PARTICIPATION WITHOUT CREDIT** (found batch 203 — `MUN3426` and `MUN3483` list
    `0-1` at UNF and UWF). **A range within one institution, including zero**, on repeatable ensemble and
    activity courses. **It exists for good reasons: a degree's repeat cap** (`MUN3426`: *"may be used in the
    degree program a maximum of 8 times"*) **and ⚠ Florida's EXCESS-HOURS provisions**, which can carry
    a financial penalty for credits beyond what a degree requires — **so a zero-credit registration
    lets a student keep playing without adding to the total.** ⚠ **State the trade-off: a zero-credit
    course does not count toward full-time enrolment** (aid, athletic eligibility, visa status), **and the
    record of participation becomes the student's own performance list rather than the transcript.**
- `prerequisites` is a single string or null. Be specific (course numbers, grade requirements, standing requirements). Where prerequisites vary by institution, say so explicitly.
- `version` starts at "1.0" and increments only when a guide is materially updated.

**Hard limits the server enforces.** A guide that breaks one of these is rejected with an
HTTP 400 (`PublishValidators.cs`, `UpsertCurriculumGuideRequestValidator`):

| Field | Limit |
|---|---|
| `title` | non-empty, ≤ 300 chars |
| `html_content` | non-empty |
| `credits` | integer **0–12** — never null (`push_guide` rejects null before the server sees it) |
| `contact_hours` | integer **0–1500** |
| `prerequisites` | ≤ **1000** chars, or null (raised from 500 on 2026-09-11) |
| `version` | ≤ 50 chars |

⚠️ **Never copy a PSAV clock-hour count into `credits`.** Set `credits: 0` and put the
hours in `contact_hours`. That single mistake stalled 11 guides for months. Run
`python validate_drafts.py` to catch it — and every other limit above — before pushing.

---

## HTML content conventions

`html_content` contains **inner content only** — no `<html>`, `<head>`, `<body>`, or `<style>` tags. Bootstrap classes are available; keep markup clean.

**Section structure (canonical order):**

1. **Course Description** — `<h2>` heading. Multiple `<p>` paragraphs covering what the course is, where it sits in the SCNS taxonomy, who takes it, and the institutional adoption pattern (e.g., "offered at approximately 8 Florida institutions").
2. **Learning Outcomes** — `<h2>` with two `<h3>` subsections: **Required Outcomes** (common across institutions) and **Optional Outcomes** (institutional variation). Use `<ul class="list-group list-group-flush"><li class="list-group-item">` for outcome lists.
3. **Major Topics** — `<h2>` with two `<h3>` subsections: **Required Topics** and **Optional Topics**. Same `list-group` markup as outcomes.
4. **Resources & Tools** — `<h2>`. Plain `<ul><li>` (not list-group). Cover textbooks, online platforms, software, lab equipment, reference standards/organizations.
5. **Career Pathways** — `<h2>`. Plain `<ul><li>`. Specific career titles where possible; SOC codes where useful; Florida industry context.
6. **Special Information** — `<h2>` with `<h3>` subsections covering: certification preparation, articulation/transfer notes, FE exam preparation (where applicable), course format, position in curriculum, prerequisites narrative, course-code variations across Florida.
7. **AI Integration (Optional)** — `<h2>` — *new section, growing in importance*. Address the substantive use of AI tools in the course's domain: what AI tools are commonly used, where they help, where they fail, the engineer's responsibility for AI-assisted output, academic integrity considerations. Include where:
   - The course's content area now naturally involves AI tools (programming, data analysis, design, writing)
   - Faculty have specifically integrated AI tools into the course
   - Industry practice in the course's domain has substantively shifted toward AI-augmented work
   
   Skip this section where AI integration is not yet substantive for the course (e.g., foundational physics, theoretical mathematics) — but expect this to expand over time as faculty AI integration grows.

**Markup conventions:**
- `<h2>` for sections, `<h3>` for subsections
- `<p>` for paragraphs (prose, not bulleted lists for explanation)
- `<strong>` for key terms on first introduction
- `<em>` for textbook titles
- `<ul class="list-group list-group-flush"><li class="list-group-item">` for outcome and topic lists (Bootstrap-styled)
- `<ul><li>` for resource and career lists (plain)
- Avoid HTML entities where Unicode works (en-dash, em-dash, mathematical symbols are fine as Unicode)

⚠⚠ **A TWO-SUBJECT GUIDE STILL OWES THE CANONICAL STRUCTURE (batch 224).** When a number carries
two readings, it is tempting to give each reading its own `<h2>` with outcomes and topics nested
inside. ⚠ **`JOU4306` was drafted that way and `validate_drafts.py` correctly warned that the guide
had no `Learning Outcomes` and no `Major Topics` section at all.** **Label the readings INSIDE the
canonical sections, not instead of them**: each reading's prose as an `<h3>` in Course Description,
then both outcome lists under one `<h2>Learning Outcomes</h2>` and both topic lists under one
`<h2>Major Topics</h2>`, with the reading named on every list.

**Omit a section rather than fabricate.** If you cannot substantiate Career Pathways for a niche course, omit the section. Leave a brief sentence in Course Description acknowledging the limit if useful.

---

## Florida pedagogy conventions

**SCNS course code patterns:**
- `XXX1xxx`/`XXX2xxx` = sophomore (lower-division)
- `XXX3xxx`/`XXX4xxx` = junior/senior (upper-division)
- `XXX5xxx`/`XXX6xxx` = graduate
- `XXX0xxx` = postsecondary adult vocational (PSAV/clock-hour)
- `XXX9xxx` = special topics/internship/thesis (shell — skip by default)
- Suffix `C` = integrated lecture+lab (typically 60 contact hours for 3 credits)
- Suffix `L` = lab-only (typically 1 credit / 30-45 hours)
- No suffix = lecture-only (typically 45 contact hours for 3 credits)

**Sophomore/junior course pairs are common.** When you see two course codes with similar titles at different levels, they're often the same content at different curriculum positions:
- Statics: EGN2312 (sophomore) ↔ EGN3311 (junior)
- Dynamics: EGN2322 (sophomore) ↔ EGN3321 (junior)
- Mechanics of Materials: EGN2332C (sophomore) ↔ EGN3331C (junior)
- Engineering Economics: EGN2610 (sophomore) ↔ EGN3613 (junior)

When writing one variant, cross-reference the other and note that programs typically use one consistently with their statics/dynamics positioning.

**Transfer vs. PSAV vs. Engineering Technology:**
- **Transfer courses** (engineering majors, A.A./A.S. transfers): cite SCNS articulation, note general-education satisfaction where applicable, mention FCS+SUS transfer pathway.
- **PSAV courses** (clock-hour, certificate programs): credits=0, no transferability claims, FLDOE Curriculum Framework + CIP code citations, Florida DBPR/Board for licensure pathways. Different audience, different treatment.
- **Engineering Technology courses** (BAS programs): articulation is asymmetric — engineering tech calculus (EGN2045/EGN3046) typically does *not* satisfy MAC2311/MAC2312 for engineering transfer. Flag this honestly.

**Hedging language by institution count:**
- 8+ institutions: confident, definitive language. Content is well-validated.
- 4-7 institutions: confident with light hedging where appropriate.
- 2-3 institutions: explicit hedging — "varies by institution," "students should consult their specific institution," "content may emphasize X at some institutions and Y at others." Use Optional Outcomes / Optional Topics generously.
- 1 institution (faculty request only): treat as a custom guide for that institution. Apply faculty specifications precisely.

**Always include where applicable:**
- FE/PE exam relevance (the FE exam is the gateway to PE licensure; topics that appear on FE exams should say so)
- ASTM/ANSI/ASME standards by number where they govern the content
- Florida-specific employer landscape (aerospace at Space Coast, defense at Lockheed/Northrop/L3Harris, healthcare at AdventHealth/Orlando Health/BayCare, hospitality engineering at Disney/Universal, marine/ocean industry, agtech)
- Difficulty/time-commitment honesty for demanding courses (mechanics-of-materials, fluids, thermo, dynamics all warrant 8-12+ hours/week)

---

## Sanity-check patterns

After generating, surface anything in this list to the user as part of the post-batch notes:

- **Credit/hour mismatches.** 3-credit lecture should be ~45 hours; 3-credit "C" integrated should be ~60 hours; 1-credit "L" lab should be ~30-45 hours. Anything outside these ranges deserves a flag.
- **Generic titles** ("Engineering Analysis," "Foundations of Engineering," "Special Topics") signal content variation risk. Note this for the user.
- **Single-institution courses** (faculty requests) — flag the novel content for closer review.
- **Course-code variation across Florida** — flag where the same content is taught under different prefixes (e.g., fluid mechanics under EGN3353C vs. EML3xxx vs. CWR3xxx).
- **Articulation gotchas** — engineering tech calculus, terminal courses, courses with non-standard credit counts.
- **Mental-health-adjacent content** — health programs, counseling courses, courses touching difficult subject matter — verify the content is supportive and resource-pointing rather than triggering.

---

## File conventions

- **Output filename**: `{COURSE_ID}_guide.json` exactly. Course ID is uppercase, no spaces. `queue_mgr.py reconcile` matches drafts to queue entries by extracting the course ID from the filename, so don't rename them.
- **Output directory**: `Tools/drafts/` — write guides straight here. This is the same directory the push reads from; there is no staging step.
- **Never write a `.py` or `.ps1` file named after a stdlib module** (`queue`, `csv`, `json`, `email`, …) into this directory — it shadows the real module and breaks `requests`/`urllib3`. That is why the queue tool is `queue_mgr.py`; don't rename it back.
- **`REVIEW_QUEUE.md`** holds findings that need Ron's decision before acting — correction candidates on already-live guides, and scope calls like the skip list. **Add to it whenever a batch turns one up, rather than only mentioning it in the batch report**, and move items to its Resolved section once a decision lands. Findings and evidence still go in `SOURCES.md`; `REVIEW_QUEUE.md` is the short actionable list that points back to it.

---

## What to skip (default)

Shell-style courses in any prefix, unless the user says otherwise:
- `XXXX900`, `XXXX905`, `XXXX910` — independent study / directed individual study
- `XXXX920`, `XXXX930` — **special topics / selected topics** (added 2026-08-31)
- `XXXX940`, `XXXX941`, `XXXX945`, `XXXX949` — internship / cooperative education
- `XXXX950`, `XXXX951` — special topics
- `XXXX971`, `XXXX973` — thesis
- `XXXX980`, `XXXX981` — dissertation
- `XXXX990`, `XXXX991` — supervised research

### ⚠ The "has it become titled?" exception

**Skip a shell number unless the course has settled into a real, specific title that is
consistent across institutions — at which point it is no longer a special-topics course and
is worth a guide.** A specific title in the inventory is *not* sufficient evidence on its own:
the statewide inventory and catalog scrapes can capture one institution's **section title** for
one term.

Verify against two or three catalogs before keeping one. Worked example (2026-08-31):
`CCJ2930` appeared as **"Cybercrime"** at 12 institutions, which looked settled — but FGCU's
catalog lists CCJ2930 as *"Special Topics: current and emerging issues in criminal justice and
criminology."* The Cybercrime title was Daytona State's section title, not a statewide course.
**Skipped.**

**These courses migrate.** When a special-topics offering proves durable, SCNS assigns it a
permanent number later. So a topic skipped today may reappear under its own number and become
worth writing then — and, for guides on courses that *did* migrate, it is worth noting that
older transcripts may carry the same content under the shell number. Do not treat a shell
number as equivalent to the permanent number it became; SCNS equivalency does not cross
numbers.

Title keywords that flag shell courses regardless of code: INTERNSHIP, COOPERATIVE, SPECIAL TOPICS, INDEPENDENT STUDY, DIRECTED STUDY, THESIS, DISSERTATION, SUPERVISED RESEARCH.

---

## ⚠⚠⚠ One number, two subjects: the `-SCNS` / `-<INST>` split

**Ron's decision, 2026-09-04.** Sometimes an SCNS number does not carry a *variant* of a subject at
different institutions — it carries **two genuinely different subjects**. When that happens, **do not pick
one and bury the divergence in a warning. Publish both.**

### When this rule applies

Only when the statewide title and the institution's title name **different subjects**, not different
wordings. Test it against the description, not the title:

| | Same subject, different name → **one guide** | **Different subjects → split** |
|---|---|---|
| Example | SCNS "Gender and Culture" vs UWF "Global Gender Issues" | SCNS **"Gerontological Nursing"** vs UWF **"Concepts of Quality and Safety in Nursing"** |
| Handling | one guide, note the drift, tell the student to carry a syllabus | **three pages — see below** |

### What to publish

For a number `XXXnnnn` carrying two subjects, publish **three** pages:

1. **`XXXnnnn-SCNS`** — the subject as the **statewide catalog** defines it.
2. **`XXXnnnn-<INST>`** — the subject as the institution actually teaches it (`-UWF`, `-DSC`, …).
3. **`XXXnnnn`** (the bare number) — a short **disambiguation page** naming both subjects and pointing at
   the two guides. **The bare number must never silently hold just one reading**, because that is exactly
   the trap the split exists to prevent.

Every variant guide carries a block at the top of Special Information stating both subjects, listing the
institutions from the statewide inventory, and warning that **a transfer evaluator matching on the number
alone cannot tell the two apart**.

### Mechanics (working as of batch 129)

- **The server accepts hyphenated IDs.** `ExtractCoursePrefix` scans letters up to the first digit, so
  `NUR4826-UWF` resolves to prefix `NUR`, finds the taxonomy node, and creates the course.
- **The tooling regex was widened** in `queue_mgr.py` and `validate_drafts.py` to
  `^[A-Z]{3}\d{4}[CL]?(?:-(?:SCNS|[A-Z]{2,5}))?$`. Before that change `reconcile` **silently skipped**
  hyphenated drafts and they never pushed.
- ⚠ **When deriving a variant draft by copying an existing one, delete the `pushed_utc` key first** —
  `reconcile` reads it and marks the new draft as already pushed, so it never gets sent.
- The disambiguation stub legitimately trips the validator's "no Learning Outcomes / Major Topics"
  warnings. Non-blocking, and correct for that page type.

### ⚠ Sourcing the `-SCNS` half

**A `-SCNS` guide needs the state catalog's definition of the course, not just its title.** The statewide
inventory (`courses_2plus_institutions.csv`) gives a title and an institution list and nothing more.

**Do not write a `-SCNS` guide from the title alone** — that is inventing content, which this project does
not do. Source it from the SCNS catalog, or from a fetchable institution that actually teaches the SCNS
version. **Ron has offered to supply the SCNS catalog; ask for it.**

### ⚠⚠ PREFIX divergence — a named category (batch 179)

**The same subject taught under different SCNS prefixes at different institutions, where the number, level
and suffix may all otherwise match.** Credit articulates; **prerequisite checks and requirement matching do
not**, because receiving programmes name prerequisites by course number.

| Subject | Competing prefixes | Notes |
|---|---|---|
| **Anatomy &amp; Physiology** | **`BSC2085C`/`BSC2086C`** vs **`APK2100C`/`APK2105C`** | ⚠⚠ **The most damaging case found.** `BSC` is what nearly every health-professions prerequisite NAMES. Lower-division, huge enrolment, gates competitive admission. |
| Social work | `SOW` vs `HUS` (human services) | ⚠ `HUS` does **not** substitute in a CSWE-accredited programme. |
| Conservation / resources | `GEO` vs `EVR` vs `SWS` | applied as a general elective where no matching department exists |
| Health informatics | `HSA` vs `HIM` vs `CIS` | |
| Supply chain | `TRA` vs `MAN` vs `MAR` | |

⚠ **Most damaging in lower-division courses feeding competitive professional admission**, because the
student meets it before transfer, with least advising support, and a mismatch can invalidate an application
rather than merely delay an audit.

**Guides should name the alternative prefix explicitly wherever one exists**, and tell students to read
target-programme prerequisites literally.

### ⚠ The prerequisite-chain diagnostic (promoted to a standing test, batch 175)

**When two institutions' descriptions of a number look like they *might* be the same subject, stop reading
the descriptions and look at the prerequisite graph.** Ask two questions:

1. **What does each institution treat this course as a prerequisite FOR?**
2. **What does each institution accept as an ALTERNATIVE to it?**

**A course's function in its own institution's prerequisite graph is harder to fake than its description
and is frequently more informative.** Three cases have now turned on it:

| Number | What the chain revealed |
|---|---|
| `CLP4302` | FGCU gates on research methods **and statistics** → the course reads research. UWF gates on abnormal psychology alone → a skills course. |
| `CHM4455` | Physical chemistry required → a quantitative treatment. |
| **`COM3003`** | UWF accepts it **interchangeably with `ADV3000` and `PUR3000`** as the gateway to its advertising and PR sequence → it is an advertising/PR foundation, not a theory survey. |

**Apply this before concluding that a divergence is mere title drift.**

### Open cases

| Number | SCNS subject | Institution subject | `-SCNS` | `-<INST>` | bare |
|---|---|---|---|---|---|
| **`COM3003`** | **Human Communication** (theory survey: interpersonal, small group, organisational, intercultural) | **Integrated Advertising &amp; Public Relations Concepts** (UWF) | ✅ **`-SCNS` LIVE** (sourced from FIU) | ✅ **`-UWF` LIVE** | ✅ **live** | ✅✅ **SPLIT COMPLETED 2026-09-07 (batch 175) — the first full three-page execution of this rule.** Both halves were sourceable, so all three pages published. ⚠ **The decisive evidence was the PREREQUISITE CHAIN, not the titles**: UWF lists `COM3003` as interchangeable with `ADV3000` and `PUR3000` as a gateway to `ADV3300` and `PUR4801`. A theory survey would not be. |
| **`EEE4775`** | **Massive Storage and I/O for Big Data Computing** (file storage systems, I/O architectures, big-data systems infrastructure; FIU) | **Real-Time Systems** (real-time scheduling theory, response-time analysis, RTOS design; UCF) | ✅ **`-SCNS` LIVE** | ✅ **`-UCF` LIVE** | ✅ **live** | ✅✅ **SPLIT COMPLETED 2026-09-09 (EEE sweep) — the second full three-page execution of this rule.** ⚠⚠ **The cleanest collision found so far: the two subjects share NO content, no textbook and no skill set** — unlike `COM3003`, where both halves were at least communication. ⚠ **UCF holds the MINORITY reading**: the statewide record AND FIU both say storage, so a UCF student transferring out carries a number the state says means something else. Found from the SCNS flat file (`inst_title` vs `state_title`), not from reading catalogs — the first divergence in the project surfaced mechanically rather than by probing. |
| `NUR4286` | Gerontological Nursing | Concepts of Quality and Safety in Nursing (UWF) | **⏸ needs catalog** | ✅ `-UWF` live | ✅ live |
| `NUR4826` | Ethics | Transformational Nursing Leadership (UWF) | **⏸ needs catalog** | ✅ `-UWF` live | ✅ live |
| `ART3789C` | World Ceramics | Advanced Ceramics: Mold Making and Slip Casting (UWF) | **⏸ candidate** | published as single guide | — |
| `ART4800` | Criticism Seminar | Portfolio (UWF) | **⏸ candidate** | published as single guide | — |
| `HSC3102` | Perspectives in Health | Health Science Essentials of Behavior Analysis (UWF) | **⏸ candidate** | published as single guide | — |
| `PCB4315` | Marine Ecology | Tropical Marine Ecology (UWF, Bahamas field course) | **⏸ candidate** | published as single guide | narrowing, not a different subject — low priority |
| `ISM4320` | Applications in Information Security | Legal, Ethical, and Human Aspects of Cybersecurity (UWF) | **⏸ candidate** | published as single guide | **strongest candidate in this batch** — technical applications vs human/legal |
| `ISM4545` | Visual Analytics I | Business Analytics with AI (UWF) | **⏸ candidate** | published as single guide | different centre of gravity; "I" implies a sequence UWF does not run |
| `MAN4350` | Training and Development | Recruitment and Selection (UWF) | **⚠⚠⚠ COLLISION** | published as single guide | **not a normal drift** — subjects permute across `MAN4320`/`MAN4350`; needs a two-number treatment. See `REVIEW_QUEUE.md`. |
| `MAN3802` | Principles of Entrepreneurship | Small Business/Family Business Management (UWF) | **⏸ candidate** | published as single guide | venture creation vs managing established firms |
| `PUR3000` | Principles of Public Relations | Introduction to Public Affairs (UWF) | **⏸ candidate** | published as single guide | **strongest candidate since ISM4320** — UF *and* FGCU both teach the general intro-PR course (history of the profession, ethics, PR process); UWF teaches government/nonprofit/media policy communication. Public affairs is a *subfield* of PR, so UWF's students miss PR history, media relations and campaigns entirely |
| `TPP2100` | Acting I | Acting for Non-majors (UWF) | **⏸ candidate** | published as single guide | ⚠ statewide lists BOTH `TPP2100` and `TPP2110C` as "Acting I" — a title, not a number, collision |
| `LAE3314` | Children's Literature | Literacy for the Emergent Learner (UWF) | **⏸ needs catalog** | **NOT WRITTEN — pulled from batch 156** | — | ⚠⚠ **First case where UWF holds the MINORITY reading.** Statewide title is Children's Literature across six institutions; UWF alone teaches early-literacy instruction. **Confirming evidence: UWF carries `LAE5468` "Literature for Children and Young Adults" at graduate level**, so it teaches the children's-lit subject under a different number. Writing a single guide from UWF would publish the minority subject under a number most institutions use for something else. See `REVIEW_QUEUE.md` item 20. |
| `PUR4801` | Public Relations Cases | **Public Relations Campaigns** (UWF) | **⏸ candidate** | queued, not yet written | — | ⚠⚠ **A numbering collision, not ordinary drift.** UWF uses PUR4801 for the campaigns CAPSTONE that the statewide system numbers `PUR4800C` (FGCU uses `PUR4800`, no suffix). Statewide, PUR4801 is *Public Relations Cases* — a different subject. **The project will meet this again from the other side when PUR4801 comes up in the queue.** See batch 158 in `SOURCES.md`. |
| `ZOO4454C` | Ichthyology (all fishes, ~35,000 spp; integrated lecture+lab; FGCU) | **Elasmobranch Biology** (sharks/rays/skates/chimaeras only, ~1,200 spp; UWF, no `C`) | **⏸ candidate** | published as single guide (Ichthyology) | — | ⚠⚠ **Stronger than the PCB4315 narrowing case.** Three divergences at once: subject scope, suffix, and format. A UWF student has **not covered the teleosts** — every fish a Florida fisheries biologist handles. The employability consequence is concrete. UWF's is the better course for shark research; the problem is the number. See batch 165 in `SOURCES.md`. |
| `CLP4302` | Intro to Clinical Psychology — **disciplinary survey**: scientific basis, training, roles, models, controversies, ethics (FGCU, UF) | **HELPING SKILLS**: empathy, nonverbal behaviour, problem solving, crisis intervention, interview technique, experiential activities (UWF) | **⏸ candidate** | published as one guide covering **both**, each labelled | — | ⚠⚠ **Strongest candidate since `PUR3000`.** The **prerequisite chains prove it**: FGCU gates on research methods AND statistics (the course reads research); UWF gates on abnormal psychology alone (a skills course). See batch 167 in `SOURCES.md`. |

| `TPA3230C` | **Costume Design** (statewide title) | **THREE different subjects, none of them agreeing**: UWF `TPA3230` = *Costume Construction* (patterning, cutting, draping); FSU `TPA3230` = *Costuming I* (costume sewing); FGCU `TPA3230` = *Costume Design*; FIU `TPA3230` = *Costume History* (fashion ancient→modern) | **⏸ HELD** | **NOT WRITTEN — pulled from batch 173** | — | ⚠⚠⚠ **The most severe case in this table: THREE subjects, not two**, and construction vs design is a real professional division (draper vs designer — different jobs, different careers). **Compounding problem: NO institution carries the `C` suffix** — all four carry bare `TPA3230`, so the queued ID may not exist anywhere. UWF puts design at `TPA4045`/`TPA4046` instead. See `REVIEW_QUEUE.md` item 25 and batch 173 in `SOURCES.md`. |

| `EEX4474` | **Teaching Students with Moderate/Severe Disabilities** — curriculum and instruction for students with severe and multiple disabilities (UWF, statewide title) | ⚠ **Assessment of infants and young children** (FGCU) | **⏸ candidate** | published as single guide (UWF/statewide reading), with a divergence block | — | ⚠⚠ **First divergence found inside a course PAIR.** `EEX4254` (mild/moderate) and `EEX4474` (moderate/severe) are the standard two-course split of an ESE methods sequence and are taken together — so **a student can complete a coherent-looking pair and have covered something different at the other institution.** Both guides cross-reference each other. See batch 181 in `SOURCES.md`. |

| `BSC1050` | **Environmental Science** — the broad applied field (pollution, resources, energy, policy) | ⚠ **Fundamentals of Ecology** — the science of organism-environment interaction, a COMPONENT of the above (UWF) | **⏸ candidate** | published as single guide (UWF/ecology reading), with a divergence block | — | ⚠ **The only reachable catalog holds the NARROWER reading** — three of four institutions are private or small colleges outside catalog reach. Likely cause: the number sits on a prefix boundary (Florida numbers environmental science `EVR1001` and majors ecology `PCB3043`), so a non-majors course spanning both lands in general `BSC` and leans whichever way the institution does. See batch 182 in `SOURCES.md`. |

| `SPC4680` | **Rhetorical Criticism** — methods for the criticism of rhetorical discourse: Aristotelian, metaphor, narrative, post-modern, cultural (FSU **and** UF, matching the statewide title) | ⚠ **Rhetoric, Media, and Civic Life** — applied preparation for leadership, advocacy and civic engagement, with attention to the shift from traditional to digital media (UWF) | **⏸ candidate** | published as single guide (majority/methods reading) with a labelled variant section | — | ⚠⚠ **Second case where UWF holds the MINORITY reading**, after `LAE3314` — and the strongest, since FSU and UF agree with each other AND with the statewide title. A methods course and an applied advocacy course are different preparations, and the methods version is what graduate study in rhetoric expects. See batch 185 in `SOURCES.md`. |

| `APK4200` | **Motor Development** — developmental aspects of movement and the acquisition of motor skills across the lifespan (FIU, matching the statewide title) | ⚠⚠ **Neuromechanics of Human Movement** — neural mechanisms of movement and control, central and peripheral, prerequisite `APK 3110L` (UWF) | **⏸ candidate** | published as one guide covering **both**, each labelled | — | ⚠⚠ **Third case where UWF holds the MINORITY reading**, after `LAE3314` and `SPC4680`. **Different fields, different literatures, different audiences**: motor development serves teachers and adapted-activity specialists; neuromechanics serves exercise science and rehabilitation. ⚠ **A student needing motor development for a certification who takes the neuromechanics course has not covered it, and the transcript will not show it.** The prerequisite settled it — an exercise physiology LAB is not a developmental course's gate. See batch 188. |

### ⚠⚠ SECTOR number divergence — FCS and SUS using different numbers (batch 182)

**Distinct from ordinary number divergence, which runs between institutions. This runs along the SECTOR
boundary:** the two-year colleges as a group use one number and the universities as a group use another.

| Subject | FCS number | SUS number |
|---|---|---|
| Introductory criminal justice | **`CCJ1020`** (Broward, EFSC, Valencia — all three checked; **none carries `CCJ2002`**) | **`CCJ2002`** |
| ⚠⚠ **Criminal justice administration** (batch 220) | **`CCJ2452`** — Polk State, Valencia, Florida Gateway, State College of Florida, Tallahassee State (**all five FCS**) | **`CCJ3450`** — UCF, UWF (**both SUS**) |

⚠⚠⚠ **The second row is worse than the first, and the reason is the LEVEL (batch 220).**
`CCJ1020`/`CCJ2002` are both lower-division, so an A.A. completer's general-education and elective
protections absorb much of the damage. **`CCJ2452` and `CCJ3450` sit at DIFFERENT LEVELS, and a
2000-level course CANNOT supply upper-division hours toward a Florida baccalaureate** — so a state-college
student who takes the subject may have to take it again at the university, **not because the content
differs but because the level does.** **Tell the reader to get a WRITTEN answer from the receiving
department before taking the lower-division version.**

⚠⚠ **Two instances in ONE prefix makes it a property of that prefix, not a coincidence.**
**Generalised drill: where a prefix is found to split one course by sector, check its other
high-enrolment numbers for the same shape before writing any of them.** One `survey.py` call on the
suspected twin answers it.

#### ⚠ But the SECTOR does not determine the LEVEL — check carriers, do not infer (batch 220)

**`CCJ3691` is a 3000-level number carried by UWF (SUS) and St. Johns River State College (FCS).**
⚠ **Florida College System institutions offer upper-division coursework where they hold baccalaureate
authority**, and several do. **So "FCS implies lower division" is a tendency the sector rule exploits, not
a fact to rely on.** ⚠⚠ **Confirmed again one batch later: St. Petersburg College (FCS) carries
`PLA4554` AND `PLA4806` at 4000 level.** **Check the carriers; never infer the level from the sector.**

#### ⚠⚠⚠ THE A.S.-TO-BS LADDER — the same data shape, the OPPOSITE diagnosis (batch 221)

**Running the batch-220 drill on `PLA` fired on FOUR of six queued courses — and the answer came out
different, which is the finding. A sector split in the data can be a DEFECT or a DESIGN, and the two need
opposite warnings.**

| Subject | FCS numbers | SUS numbers |
|---|---|---|
| **Family law** | **`PLA2800`** — ⚠ **18 public carriers, ALL FCS** | `PLA3806` (FGCU, UWF); `PLA4806` (UCF, SPC) |
| **Law office management** | **`PLA2763`** — **10 carriers, ALL FCS** | `PLA4764` (UCF, UWF) |
| **Property** | `PLA2610` (FCS) | `PLA3613` (UWF); `PLA3615` (UCF) |
| **Bankruptcy** | `PLA2460` (FCS) | `PLA3464` (UWF); `PLA4464` (UCF) |

⚠⚠⚠ **The explanation is an ARTICULATION LADDER, not an error: Florida's A.S. in Paralegal
Studies is overwhelmingly an FCS credential using `PLA1xxx`/`PLA2xxx`, and the BS in Legal Studies is an
SUS credential using `PLA3xxx`/`PLA4xxx`. The universities renumber the same subjects at upper division
because a baccalaureate requires upper-division hours.**

| | `CCJ2452`/`CCJ3450` (batch 220) | `PLA` (batch 221) |
|---|---|---|
| What it is | ⚠ **a DEFECT** — one course numbered twice | ⚠ **deliberate DESIGN** |
| Evidence | **two** numbers in the prefix; near-identical statewide descriptions | **four subjects at once**, with the upper statewide descriptions visibly **DEEPER** |
| Harm | ⚠ **a lost credit** — a 2000-level course cannot supply upper-division hours | ⚠ **repeated content + Florida EXCESS HOURS** — the retake IS the design |
| The guide says | *get a written answer from the receiving department BEFORE taking the lower version* | *expect familiar ground at greater depth; ask about substitution* |

⚠⚠ **THE TEST, and it costs one CSV read: count how many SUBJECTS in the prefix show the split, and
compare the two statewide DESCRIPTIONS for DEPTH.** **One subject with matching descriptions is a numbering
defect. Several subjects with visibly deeper upper descriptions is a degree ladder.** Worked comparison:
`PLA2460` reads *"an introduction into the purpose of bankruptcy laws"* against `PLA3464`'s chapters
*"discussed in detail"*; `PLA2800` is a 1980s numbered topic list against `PLA3806`'s **Florida statutes**
and **practical drafting**.

⚠ **Expect the ladder in every prefix with an A.S.-to-BS articulation** — paralegal studies, nursing,
respiratory care, radiography, dental hygiene, health information management, and the Engineering
Technology BAS prefixes. **It is the batch-206 licensure-ladder observation showing up in the NUMBERING
rather than in the scope.**

⚠ **And check for the counter-case before generalising: `PLA4191` and `PLA4554` have NO lower-division
twin**, so the ladder is a property of some subjects in a prefix, not of the whole prefix.

⚠ **Why it matters more than a between-institution divergence: it hits EVERY A.A. transfer student in the
discipline**, not the unlucky few. SCNS equivalency does not cross numbers. Mitigating facts are real — same
survey, common general-education core protects A.A. completers, departments know the pairing — **but
mid-degree transfers are not protected.**

**Drill: when a LOWER-DIVISION course appears in the queue at SUS institutions only, check two or three FCS
catalogs for the same subject under a different number before writing.** Broward, Valencia and EFSC are
reachable and make this cheap.

#### ⚠⚠ A second sector shape: SAME number, different SCOPE by sector (batch 206)

**Distinct from the number divergence above.** **`RET3354` is carried by two Florida College System
institutions as *Medical Pharmacology* and by UWF as *Cardiopulmonary Pharmacotherapy*** — **one number,
and the scope differs along the sector line.**

⚠ **The explanation is the licensure ladder, and it generalises:** **FCS institutions run the entry-level
A.S. programmes that lead to a credential, so they teach broadly; SUS institutions run degree-completion
pathways for practitioners who already hold it, so they go deeper on a narrower range.**

⚠⚠ **Expect this in every licensed allied-health field with an A.S.-to-BS ladder** — respiratory care,
radiography, nursing, dental hygiene, health information management. **And note the inversion it produces:
the broader-SOUNDING title is usually the entry-level course, and the narrower-sounding one is often
closest to the statewide description. Judge scope by the programme's level, not by the title.**

### ⚠⚠ Check the taxonomy prefix BEFORE drafting, not after pushing (batch 182)

A push for a prefix with no taxonomy node returns **HTTP 422**. The seed file answers in one command:

```
grep -c '"<PREFIX>"' PreseMakerRepo.Api/Data/Seed/taxonomy.json
```

**Zero means the push will fail.** Confirmed blocked as of 2026-09-08: **`CES`, `CWR`, `CEG`, `ENV`** — ten
queue rows, and they sit at the head of the priority order, which is why the queue's top has stopped moving.
`TTE`, `ASC`, `MUN`, `PEL`, `MVV` and `MUG` all have nodes. **This is a server-side taxonomy addition, not a
content problem.**

### ⚠ One institution, TWO introductory courses (batch 182)

A general-education version and a majors version of the same subject can share a department, a description
and almost a title. `CCJ 2002` (gen ed, lower division, *"designed for students across disciplines"*) versus
`CCJ 3024` (majors, upper division, **carries the Gordon Rule writing designation**) at UWF.

**Tells:** the level, the phrase about serving students across disciplines, and **which of the two carries
the writing designation.** ⚠ **They are not substitutes, and guides must say so.**

### ⚠ Lab-suffix warning is now standing practice (batch 182)

**Every 1000/2000-level natural science course with no `C` or `L` suffix gets an explicit warning that it
carries no laboratory and may satisfy only part of a general-education science requirement** — in the
guide AND in the prerequisite string, which is what a queue reader sees first. Instances: `AST2037`
(batch 180), `BSC1050` (batch 182).

### ✅✅✅ PACKAGING IS NOT DIVERGENCE — lecture+lab EQUALS the combined course (Ron, 2026-09-17)

**Read this BEFORE writing any warning about a bare/`C`/`L` family.** Ron's words:

> *"Some institutions use just a classroom delivery, others break these up into classroom + lab. **In
> both cases the outcomes are the same.** Other than a notation of the approach used, the distinction
> of the approach is not important and **transferability still works. For transfer Classroom + Lab (L)
> = completed just as completing as combined.** … There are very few fixed rules, colleges and
> universities are given leeway in how they approach the courses. **This is by design as it allows for
> innovation in approaches** (even though most simply copy the approaches previously used)."*

⚠⚠⚠ **This corrects a bias this file has carried for a long time.** The `C`-suffix section
below catalogues four shapes and reads, cumulatively, as though a suffix difference were usually a
problem. **For the split-family shape it is NOT a problem at all** — it is two deliveries of one
course, and the state's articulation treats them as equivalent.

**Worked case, and it is the cleanest in the catalogue — `BSC2085` (batch 235):**

| | credits | carriers |
|---|---|---|
| `BSC2085` + `BSC2085L` | 3 + 1 | **19 institutions** |
| `BSC2085C` | 4 | **7 institutions** |

**No institution carries both forms** — perfectly disjoint. ✅ **A student who completes the lecture
and the lab has completed the same thing as a student who completed the `C` course**, and transfers
as such.

**What a guide should therefore say:**

| ❌ Do NOT write | ✅ Write |
|---|---|
| *"`BSC2085` alone does not satisfy the prerequisite"* | *"two equivalent packagings; register for whichever pair your catalogue lists"* |
| a divergence block | **a notation of the approach**, one sentence |
| *"check before you register or you may not qualify"* | *"lecture + lab completes exactly as the combined form does"* |

⚠ **The ONE thing still worth saying** is the practical one: **where your institution splits the
course, enrol in BOTH halves** — they are usually corequisites and the registration is the only thing
the student has to get right.

⚠⚠ **And the general principle, which governs more than suffixes:** **Florida gives institutions
LEEWAY BY DESIGN.** Credit values, packaging, delivery mode and sequencing vary because the system
intends them to, so that departments can innovate. **So before writing any variation up as a defect,
ask whether it is simply a permitted choice.** The genuine problems in this file — one number carrying
two SUBJECTS, misfiling, a prerequisite that resolves nowhere — are of a different kind: they mislead
about CONTENT. **Packaging does not.**

#### ⚠⚠⚠ THE ONE DOCUMENTED EXCEPTION: a `C` that is a SEPARATE PROGRAMME TRACK (`MLS`, re-confirmed 2026-09-21)

**The rule above is right about PACKAGING. It does not reach the case where a `C` id is a different
ROUTE through the same subject**, and `MLS` at UWF is that case at scale — so check before applying
the rule to a professional prefix.

| At UWF | What it is |
|---|---|
| `MLS4305` Hematology I (3 sh) + `MLS4305L` Lab (1 sh) | the standard route, with a real bench laboratory |
| ⚠⚠ `MLS4306C` Hematology **Professional Track** (4 sh) | *"students will perform **VIRTUAL** laboratory activities&hellip; **Permission is required**"* |

⚠⚠ **Same credit total, and NOT interchangeable.** UWF duplicates **ten** subjects this way
(`4193C`, `4221C`, `4306C`, `4335C`, `4461C`, `4463C`, `4506C`, `4552C`, `4626C`, `4631C`), and the
track's capstone `MLS4704` asks for *"evidence of&hellip; work experience&hellip; equivalent to an MLS clinical
internship"*.

⚠ **The tell, and it is cheap: read the DESCRIPTION for "virtual", "permission is required", or a
track name in the TITLE.** A packaging difference never says any of those. ✅ **Where the two forms
differ only in how the hours are sold, the 2026-09-17 rule stands and you write a one-sentence
notation — not a divergence block.**

⚠ **And note `C` means different things inside ONE prefix**: at FGCU the `MLS48xxC` ids are hospital
PRACTICUMS, at UWF the `C` ids are the virtual-lab track. **Judge by the description, never the suffix**
— which is Ron's batch-126 rule (*a suffix is a filing decision, not a description*) doing the work.

#### ⚠ And fix errors as you find them (same instruction)

> *"Also simply fix errors as you spot them."*

**Do not queue a factual error behind a decision.** Where something the site states is wrong — a
carrier count, a stale note, a warning that overstates — **correct it and say so in the report.**
`REVIEW_QUEUE.md` is for things that need Ron's JUDGEMENT, not for things that are simply wrong.

### ⚠⚠ FOUR different shapes behind a `C` suffix — do not conflate them (batch 183, extended 219)

| Shape | Example | What it means | What transfers |
|---|---|---|---|
| **Split family** | `CGN3501C` (UF) vs `CGN3501` + `CGN3501L` (UWF); `EEE3308C` vs `EEE3308` + `EEE3308L` | one course, packaged as one enrolment or two | same content, **3 cr vs 4 cr**, one grade vs two |
| **Suffix divergence** | `BCN3224C` (UF, integrated) vs bare `BCN3224` (UWF, lecture only, no lab partner) | ⚠ **genuinely different courses** — one has laboratory hours the other does not | content differs |
| **`C` nobody carries** | `TPA3230C`, `COP3014C`, `INP3004C`, `CJE3674C`, `CTS4348C`, `DAA2204C`, `EEE3396C` | the queued id may not exist at any institution | see `REVIEW_QUEUE.md` item 28 |
| ⚠⚠⚠ **Institutional signature** (batch 219) | `TPA3064C` (FAU) vs `TPA3064` (UWF); `TPA3601C` (UCF) vs `TPA3601` (USF, UWF); `TPA4021C` (UWF) vs `TPA4021` (FSU, UF); `TPA4045C` (USF) vs `TPA4045` (UWF, FSU); `TPA4077C` (UWF) vs `TPA4077` (FSU, USF) | ⚠⚠ **the SAME course, filed differently by different schools** — both ids are real, no institution carries both | content is the same; **an evaluator matching on the identifier sees a mismatch where there is none** |

⚠⚠⚠ **The batch-219 shape is the one most likely to be misread, because it looks like "a `C`
nobody carries" from whichever side you are standing on.** **Five of seven queued `TPA` `C` ids had a bare
twin at DIFFERENT institutions, and every one of the seven `C` ids was real.**

⚠⚠ **Diagnostic, and it is one flat-file pass — BEFORE WRITING ANY `C` ID, LOOK UP THE BARE
NUMBER, and read the answer from the carrier lists:**

| What you find | What it means |
|---|---|
| **the SAME institution carries both forms** | a course run in **two shapes** — lecture section and integrated section (batch 184, `PET3640C`). State the contact-hour difference. |
| ⚠⚠ **DIFFERENT institutions carry the two forms** | **one course filed two ways** (batch 219). Name the twin and who carries it; do not write a divergence block. |
| **no institution carries the bare form, or the `C` form** | the queued id may not exist — check before writing at all |
| ⚠⚠⚠ **only a PRIVATE institution carries one form** (batch 222) | **the id is REAL but has no carrier in scope.** Write the form a PUBLIC institution carries, mark the other `skipped` with its reason, and tell the reader in the guide not to register for it |

⚠⚠⚠ **AND IT RUNS IN BOTH DIRECTIONS (batch 225).** `COM4564C` was a private-only **`C`** form
with a public bare twin. **`PET3344` is the mirror: the BARE number is carried only by a private
institution and the `C` form, `PET3344C`, is the public one.** ⚠ **So state the check symmetrically:
look up which FORM the PUBLIC carrier uses, in either direction.** **The instinct that an unsuffixed
number is the "default" is wrong as often as it is right** — on `PET3344C` no substitution was needed
because the queued `C` id was already the public one.

⚠⚠ **The batch-222 row is a SCOPE fact, not a catalogue fact, and it needs the opposite handling
from "a `C` nobody carries."** **`COM4564C`'s only carrier is Keiser (private); `COM4564` is carried by
UWF.** Same statewide title, same statewide description. **The queued `C` id was unwritable under the
2026-09-11 public-institution rule, so it was marked `skipped` with its reason and the BARE number was
written instead** — `reconcile` picks the new draft up as an orphan and adds the row itself.
⚠ **Record the substitution in the queue note and explain the suffix in the guide; do not do it
silently.**

⚠⚠ **Diagnostic for the split family: RECIPROCAL concurrent prerequisites.** `EEE 3308` lists
`EEE 3308L*` and `EEE 3308L` lists `EEE 3308*` — **neither can be taken alone, so the pair IS the `C`
course.** Where the queue holds the `C` id, write one guide covering both halves and state the three
consequences: **credit count, two grades, and register for both.**

### ⚠⚠ Two institutions agreeing with each other outrank a statewide title (batch 183)

**`HFT4274`**: statewide title **Resort Management**; **FGCU teaches "Vacation Ownership & Timeshare" and
FIU teaches "Short-Term Rental / Vacation Ownership".** Two independent catalogs agree with each other and
both contradict the statewide label.

⚠ **The statewide title is a single SCNS label with no description behind it.** Two agreeing descriptions
are stronger evidence. **That condition is part of the rule, not background — check it
before applying the rule** (see the `HFT3053` refinement below). **Write to the agreeing pair, and say in the guide what to expect if a third
institution teaches the broader subject instead.** (Contrast `BSC1050`, where only ONE catalog was
reachable — there the divergence block is a warning, not a correction.)

#### ⚠⚠ Refinement (batch 201): the rule needs a bare LABEL, and TITLES are weaker than DESCRIPTIONS

**`HFT3053`** — statewide **"Prospectus on Tourism"**, and unlike `HFT4274` the statewide record carries
a **full, specific description** of an issues-and-impacts course. Both public carriers (Pensacola State and
UWF, identical titles, 3 credits) call it **Travel and Tourism Management**.

⚠⚠ **Two conditions of the batch-183 rule fail here.** The statewide record is **not** a bare label
— it has a description to weigh. And what the carriers supply is **titles, not descriptions**, so it is
two titles against one full description rather than two descriptions against one label.

**Handling where either condition fails: cover BOTH readings with a two-column test and say the evidence is
mixed.** ⚠ **Do not "correct" a described statewide subject on the strength of agreeing titles alone.**
Reserve the batch-183 correction for the case it was built for: a bare statewide label, contradicted by two
independent institution **descriptions**.

### ⚠⚠ State-college catalog blocks are RATE-TRIGGERED, not permanent (batch 183)

**Broward and Valencia answered with full 200 bodies in batch 182 and returned empty 202s in batch 183,
minutes later** — including on `cop`, a prefix Broward certainly carries. **Roughly six requests in quick
succession tripped it.**

- ⚠ **Do not record a source as blocked on the basis of a burst.**
- **Space state-college probes out; batch them at the start of a session rather than mid-batch.**
- **This explains the long-standing blocked → recovered → blocked pattern for Broward and Valencia** that
  the register recorded across several sessions without accounting for.

### ⚠ A `C` id IS sometimes real — check every time (batch 184)

Seven consecutive queued `C` rows turned out to be carried by no institution, which made "the inventory's
`C` suffixes are spurious" a tempting generalisation. **`PET3640C` refutes it: FIU carries BOTH
`PET 3640` and `PET 3640C`.**

⚠ **An institution carrying BOTH forms is the clean signature of a course run in two shapes** — a lecture
section and an integrated section with a scheduled practicum or laboratory. **Write the `C` id, state the
contact-hour difference (60 vs 45), and tell the student to check which section they are in.**

#### ⚠⚠ CHECK THE CREDITS FIRST — same-institution-both-forms does NOT always mean two shapes (batch 228)

**Valencia College carries `BSC1010` AND `BSC1010C`, which fires the diagnostic above. ⚠⚠ But BOTH
are 4 credits** — *Fundamentals of Biology Honors* on the bare number and *General Biology I* on the
`C`. **Four credits means both already include the laboratory, so the suffix is not separating
lecture from integrated at all: it is separating HONOURS from standard.**

⚠⚠⚠ **The diagnostic depends on a CREDIT DIFFERENCE, and it is not safe without one.** A lecture
and its integrated twin differ by the lab's credit (3 against 4, or 3 against 60 hours). **Two forms
at the SAME credit value are two versions of the same packaging** — honours, or a delivery-mode
split — **and describing them as lecture-versus-integrated would be simply wrong.**

**So the check runs: same institution carries both → compare the CREDITS → equal means look for
another explanation (honours, campus, delivery mode) before writing the two-shapes note.**

### ⚠⚠ Chronological divergence — write the whole span and label the halves (batch 184)

**`EUH3570`**: statewide **"Modern Russia"**; **UWF teaches "Russia to 1917"** (its Soviet material is
`EUH 3576`); **FIU teaches the whole span in one course.** ⚠⚠ **A student registering for "Modern Russia"
at UWF gets the tsars** — the first divergence where the statewide title points at close to the OPPOSITE
half of the timeline.

**Handling: cover the full span, mark clearly which material sits on each side of the split, and lead with
a table telling the reader to check their own catalog.** Cheaper than two guides and it serves the student
in either version.

### ⚠ Practicum courses: the screening warning goes in the PREREQUISITE field (batch 184)

**Florida requires Level 2 background screening for anyone working with children or vulnerable adults, and
clearance takes time.** Students who leave it late run out of term (`EEC4301`, `PET3640C`).

**Standing practice: every guide for a course with placement or practicum hours states, in the prerequisite
string as well as the body, that screening should be started in week one** — the prerequisite field is what
a queue reader sees first. Carry FERPA confidentiality and **Chapter 39 mandatory reporting (Florida Abuse
Hotline 1-800-96-ABUSE)** in the body.

### ⚠⚠ When the tool's characteristic output IS the course's target error, say so (batch 184)

The strongest AI sections are the ones where the failure mode and the course's own subject coincide:

| Course | The coincidence |
|---|---|
| **`PET3640C`** | The discipline exists to replace **diagnosis-based assumptions with individual assessment**; a model asked about "a student with cerebral palsy" produces exactly the category-based answer the course teaches you to abandon. |
| `COM3461` | Intercultural communication warns against applying national averages to individuals; a model produces the unhedged lookup table. |
| `CJJ4010` | The course studies disproportionate minority contact; risk instruments trained on past decisions encode it. |

⚠ **Where this holds, it is a far better argument than a generic integrity warning** — it tells the student
something about their own field.

### ⚠⚠⚠ THE PREREQUISITE IDENTIFIES A COURSE'S POSITION IN THE SEQUENCE — read it before the title (batch 233)

**`PHY3106` is statewide *Modern Physics I*. FIU teaches exactly that. ⚠⚠ UWF titles it
*Calculus-Based Physics III* and teaches the THIRD TERM OF THE INTRODUCTORY SEQUENCE** — adding
thermodynamics and wave phenomena, which are classical, and not mentioning quantum mechanics.

⚠⚠⚠ **The prerequisite settles it in one line, and it is a general test:**

| | Statewide / FIU | UWF |
|---|---|---|
| Gate | `PHY 2049` or `PHY 2054` **AND `MAC 2313` (Calculus III)** | ⚠ **`PHY 2049` only** |
| Therefore | positioned **ABOVE** the introductory sequence | positioned **INSIDE** it |

**A course sitting inside an introductory sequence CANNOT require the mathematics that sequence has not
reached yet.** **So where two carriers of one number disagree about level, compare the gates: the one
demanding later mathematics is the later course.** ⚠ **This is the prerequisite-as-signal diagnostic
firing on POSITION** — alongside subject (175), depth (185), emphasis (187) and sequence position in
`MUE4411` (229).

⚠⚠ **And the content diverged at BOTH ends, which is what makes it consequential:** the UWF student has
thermodynamics and waves the FIU student does not, and may not have the **Schrödinger equation** the FIU
student does. **Tell the reader to send a TOPIC LIST on transfer and name both checks explicitly** —
physics departments place by coverage, and "did you do the Schrödinger equation?" is the question.

### ⚠⚠ CHECK WHETHER A CREDIT DIVERGENCE IS A PREFIX-WIDE INSTITUTIONAL PATTERN (batch 230)

**Before writing a credit divergence up as a fact about the course, count the institution's WHOLE
prefix.** Two `FIL` courses showed FAU at 4 credits against UWF's 3, which reads as two separate
findings. **It is one:**

| Institution | Undergraduate `FIL` credit profile |
|---|---|
| ⚠ **FAU** | **11 of 21 at 4 credits** |
| UCF | 78 of 103 at 3 |
| USF | 25 of 25 at 3 |
| UNF | 24 of 25 at 3 |

⚠⚠ **FAU runs the prefix at 4 credits; every other institution runs it at 3.** **So the sentence to
write is "FAU carries this prefix at 4 credits", once, and not "this course diverges" on every course
in the batch** — which would report one institutional choice as N separate divergences.

⚠ **It is one `Counter` over the flat file, and it also gives the reader something more useful: an FAU
film student accumulates credit faster per course than a comparison of course counts suggests.**

⚠ **The same pass surfaces other institutional signatures worth a line** — FSU's `FIL` offering is
dominated by VARIABLE credit (`1-6` on 28 rows) and UCF carries 22 `VAR` rows, which is the shape of a
production school rather than a studies department.

### ⚠⚠⚠ BEFORE CALLING A CREDIT DIVERGENCE A DEPTH DIFFERENCE, CHECK FOR A REPEAT ALLOWANCE (batch 233)

**`PHY4822L` runs at 3 credits at UWF and 2 at Florida State, which reads as one institution doing less.
It is not — it is a different PACKAGING of the same course:**

| | UWF | Florida State |
|---|---|---|
| Credits | **3** | **2** |
| Repeatable? | ⚠ **No** — 3 credits is all there is | ⚠⚠ **Yes — to a maximum of 6 credit hours**, *"for special projects arranged in advance"* |
| Catalogued as | `PHY4822L` | ⚠ **`PHY 4822Lr`** — the `r` marks repeatability in FSU's notation |

⚠⚠⚠ **FSU runs a smaller unit a committed student takes three times, reaching SIX credits and doing
self-directed projects; UWF runs one larger block and stops.** **The institution with FEWER credits per
enrolment offers MORE credit in total, and the better route into a graduate application.**

**So the rule: a lower credit value is not evidence of a shallower course until you have checked whether
it repeats.** ⚠ **The tell is cheap** — a repeat clause in the credit line, or a suffix convention like
FSU's `r`. **Read the credit line, not just the number.**

⚠ **And say what it means for the student rather than just recording it:** where a course repeats, the
guide should tell the reader the allowance exists, that a special project is the thing worth doing with
it, and to confirm how many repeats their own degree will count (Florida's excess-hours provisions
still apply).

### ⚠ CREDIT-COUNT divergence — a fourth shape, and invisible from the identifier (batch 185)

**`PHY3220`: UWF lists 4 semester hours; the statewide title and most institutions carry 3.** No
laboratory, no second registration — **the same course simply carries a different credit value.**

⚠ **Unlike split family, suffix divergence and `C`-ids-nobody-carries, nothing in the course identifier
signals it.** **Consequence: a transfer student is a credit short or long against a degree requirement, and
in tightly budgeted majors it surfaces only in the final audit.** **State the credit value explicitly in
the guide and tell the reader to check their own.**

### ⚠⚠⚠ RESOLVE THE RANGE: name the school against every differing hour figure (Ron's direction, 2026-09-11)

**This is the standing rule for how a credit or contact-hour divergence is written up.** Where the identified
offerings of a course carry **different hours at different schools, the guide must name the schools and the
hours required at each.** A range is not an answer:

| ❌ Never publish | ✅ Publish |
|---|---|
| "3–4 credits depending on institution" | a table: **Valencia 3, Miami Dade 4, State College of Florida 4, Daytona State 3** |
| "contact hours vary" | "**60 contact hours** at the four institutions that publish them; Tallahassee State does not publish hours" |
| "typically 3 credits" | "**all five institutions carry it at 3 credits**" — state uniformity explicitly too |

**Why a range fails the reader.** A student does not attend "Florida"; they attend one school, transfer to
one other, and need **their own two numbers**. A range tells them a discrepancy exists and leaves them to do
the work the guide exists to do — and **the range is precisely where the harm is**: the student short a
credit against a degree requirement is the one who read "3–4" and assumed 3.

**Where the data comes from — the answer is now cheap:**

1. **The SCNS flat file** carries **per-institution credits** (`credit`) and **clock hours** (`clock_hours`)
   for every offering of the exact id. One parse answers the whole prefix. ⚠ **Normalise before comparing —
   `3` and `3.0` are the same number**, and a spurious "varies" is worse than no table. ⚠ A value like
   `3-4` is a range **inside one school** (variable-credit section) — say so, and say what determines it.
2. **The course API's `offerings[]`** carries the same per-school `credits` and `clockHours` — so the
   guide's table and the site's "Offered at N Florida institutions" panel should be built from one pass and
   agree with each other. See the course-catalog section above.
3. Where an institution publishes contact hours directly (**Broward** is the reliable one), prefer it over
   any derived figure and say which school it came from.

**Where no institution publishes hours** — common, and the honest answer is not silence: **give the derived
figure, label it as derived by the credit-to-hour convention, and name the schools that were checked.**
A reader can then see the difference between a sourced number and a convention.

**The guide's own `contact_hours` field still holds ONE number** — the value for the identifier being
published (for a `C` id, the integrated form's hours; see the batch-189 rule). The per-school detail belongs
in the Special Information table, not in the scalar field.

### ⚠⚠ Prerequisites separate DEPTH as reliably as they separate SUBJECT (batch 185)

The prerequisite-chain diagnostic (batch 175) was developed to settle whether two institutions teach
different SUBJECTS. **`PSB4002` shows it also settles DEPTH:**

| Institution | Gate | What it signals |
|---|---|---|
| **FGCU** | general psychology **AND** research methods **AND** statistics **AND** biology with lab | reads primary research at the cellular level |
| **UWF** | **none** | a broader biological-psychology survey |

⚠ **Where two catalogs describe the same field in compatible language, the GATE is the better signal of
what the course will demand** — and the guide should say so, because a transfer student moving from the
survey into a programme built on the rigorous version meets the gap in the next course.

### ⚠ A syllabus TEST beats a generic divergence warning (batch 185)

Where a guide covers a divergence, give the reader an observable way to tell which version they are in.
`SPC4680`:

| Methods version | Applied version |
|---|---|
| named critical approaches, assigned artefact analyses, a substantial critical essay, journal readings | media change, advocacy projects, assessment of contemporary campaigns, produced persuasive work |

⚠ **"Check your syllabus" is advice; a two-column test is usable.** Apply this wherever the divergence is
one of emphasis rather than of subject.

### ⚠ "Offered concurrently with <5xxx>" — a dual-listed course (batch 186)

**`SOW4700` is "offered concurrently with `SOW 5710`"** — undergraduate and graduate sections sharing a
classroom, with extra requirements for the graduate students.

⚠⚠ **Two consequences a guide must state:** the pace and reading are pitched above a typical undergraduate
course (generally a benefit), and **taking the undergraduate version may block taking the graduate one for
credit later** — dual-listed pairs frequently carry a repeat restriction. **This matters to anyone
continuing to graduate study at the same institution, and it must be known before registering.**

**Look for the phrase in catalog entries; it is easy to read past.**

### ⚠ The caches answer two independent failure modes (batch 186)

**`RTV2000` was written entirely from the cached FSCJ Coursedog data**, and it needed to be for two separate
reasons at once:

1. **The live state-college HTTP routes were being left alone** under the rate-limit rule (batch 183).
2. ⚠ **The inventory pointed at the wrong institution** — it lists UWF, which does not carry the number.

⚠ **Keep `fiu_courses.json`, `fscj_courses.json` and `nwfsc_courses.json` current.** **They cover
rate-limiting AND inventory error, and those failures are independent.**

### ⚠ Watch the 500-character prerequisite ceiling (batch 186)

**`SCE4320` failed the validator at 546 characters** — the first blocking failure in eleven batches, and it
needed two trims.

⚠ **Prerequisite strings have been growing as more warnings are packed into them**, and **three of the last
twelve have come within 30 characters of the limit.** **The assembler's length report is what catches this
before the push; keep reading it.** **When trimming, cut the connective tissue and keep the warnings.**

#### ⚠⚠⚠ SOLVED (batch 209): draft the prerequisite field at ~850 characters and let it grow

**The ceiling is now 1000, and for NINE consecutive batches every prerequisite in the batch exceeded it on
first assembly** — batches 201–208, needing up to four rounds of trimming each, with the endgame slow
because each edit moves the count by less than a sentence.

✅ **Batch 209 broke the run by writing short deliberately**: **three of six came in under the limit on
first assembly** (886, 924, 955 characters), and the three that ran over needed **one** trim round.

⚠⚠ **So the rule is: write the prerequisite to about 850 characters and stop.** It always grows during
assembly — the warnings accumulate as the research lands. **Writing to length and then cutting is the
expensive order; writing short and adding is the cheap one.**

#### ⚠⚠ Budget the SUM of SHARED blocks, not each one (batch 212, sharpened batch 215)

**A warning reused across a batch spends its length on EVERY course that uses it.** Batch 212 learned this
with one shared block (4 of 9 over). ⚠⚠ **Batch 215 had THREE — a credential warning, a placement warning
and a sequence warning — totalling ~1,100 characters of shared text before any course-specific content,
and 11 of 12 went over.**

⚠⚠⚠ **Revised rule: allow all shared blocks together about 400 characters, not 400 each.** Trimming the
blocks fixed 9 of 11; the rest needed individual trims. **Count the boilerplate first, then write the
course-specific text into what remains.**

### ⚠⚠ TERMINOLOGY-ERA divergence — a category of its own (batch 187)

**Not title drift, not subject divergence: the same course carrying vocabulary from different decades of
the field's own development.**

| Number | Older term | Current term | Why it changed |
|---|---|---|---|
| **`SYD4800`** | UWF **"Sociology of Sex Roles"** | UF **"Sociology of Gender"** | role theory framed gender as expectations attached to two categories; the replacement treats it as produced in interaction and built into institutions |
| **`SOW4700`** | statewide **"Chemical Addiction"** | UWF **"Substance Use, Prevention, and Treatment"** | *substance use disorder* is a spectrum with severity specifiers; the older vocabulary is associated with more punitive clinical judgements |

⚠ **The handling differs from a subject divergence.** **The course is the same.** **What the guide owes the
reader is the CURRENT vocabulary plus an explanation of why it changed** — because **a student who learns
only the older term will be using language the current literature has moved past**, and in clinical fields
that has consequences beyond style.

⚠ **It also predicts an AI failure mode**: training data is dominated by older text, so **generated prose
reproduces the superseded vocabulary** — which is worth saying in the guide's AI section.

#### ⚠⚠⚠ And sometimes the old vocabulary is not merely dated — it is contrary to STATE LAW (batch 206)

**`RED3310` is the strongest instance of this shape so far, and it differs in kind from `SYD4800` and
`SOW4700`.** Those were vocabulary the field had moved past. ⚠⚠ **This one has regulatory force behind it.**

**Florida requires evidence-based reading instruction, mandates K-3 screening and progress monitoring, funds
district reading coaches, and has revised the Reading Endorsement competencies and the B.E.S.T. ELA
standards accordingly.** ⚠ **So "reading as a process", three-cueing and guessing from context are not
merely out of date — they are contrary to what Florida requires and what the FTCE tests.**

⚠⚠ **Where a terminology-era divergence touches a LICENSED or CERTIFIED field, check whether the state has
legislated.** The consequence for the student is then concrete rather than academic: **preparation in the
superseded model leaves them unready for what their employer is required to do.** Expect the same shape in
**nursing, athletic training, respiratory care, behaviour analysis and social work.**

⚠ **And a caution that applies to every terminology-era case: A CATALOG TITLE CAN LAG A REVISED SYLLABUS BY
YEARS.** **Titles change slowly and syllabi change fast.** **Tell the reader to judge by the ASSIGNED TEXT
and the reading list, not the title** — for `RED3310` the test is whether the text is Moats, Kilpatrick,
Liben, Lindsey or Seidenberg.

### ⚠⚠ The prerequisite-as-signal diagnostic — now the most productive sourcing move

Originally a test for whether two institutions teach different SUBJECTS (batch 175). It has since fired on
DEPTH and on EMPHASIS, four batches running:

| Course | Gate | What it signalled |
|---|---|---|
| `PSB4002` | four courses incl. statistics + lab biology (FGCU) vs none (UWF) | reads primary research at cellular level vs a survey |
| `STA4234` | **calculus** added at FGCU | theory and the matrix formulation vs applied procedures |
| `ZOO4472C` | **statistics** at UWF | estimating survival and abundance, not just describing birds |
| `ZOO4485` | **oceanography** at UWF | marine mammals as animals in a physical ocean |
| `ACG4180` | **finance**, not accounting | taught from the statement USER's side |
| ⚠⚠ **`MUE4411`** (229) | **FSU**: a TWO-COURSE conducting + choral literature sequence, plus a concurrent course. **UWF**: music theory, with first conducting as a **COREQUISITE** | ⚠⚠⚠ **SEQUENCE POSITION — and it explains a 2× CREDIT divergence** |

#### ⚠⚠⚠ A FOURTH thing the prerequisite settles: WHERE IN THE SEQUENCE a course sits (batch 229)

**The diagnostic has settled SUBJECT (175), DEPTH (185) and EMPHASIS (187). `MUE4411` adds
POSITION, and it does it by explaining a credit divergence that looked inexplicable.**

**Florida State carries it at 4 credits and UWF at 2** — a doubling, the largest credit divergence
recorded outside flight training, with nothing in the identifier to signal it. **The gates say why:**

| | FSU — 4 credits | UWF — 2 credits |
|---|---|---|
| Gate | `MUE 3491`–`3492`, a **two-course** choral conducting and literature sequence | `MUT 2117` (theory) |
| Alongside | concurrent `MUE 3495r` required | ⚠ **corequisite `MUG 3104` — FIRST conducting** |
| Therefore | **you arrive already able to conduct**, and four credits go on harder problems | **you are learning to conduct at the same time** |

⚠⚠ **Neither is a worse course — they sit at different points in the same sequence.** **That is a
far better thing to tell a student than "credits vary by institution."**

⚠⚠⚠ **And it reveals that the transfer harm is ASYMMETRIC, which a credit comparison alone would
miss:** a student moving to FSU with the 2-credit version is short two credits **and** has not done
the `3491`–`3492` foundation FSU's course assumes; a student moving the other way simply arrives
over-prepared. **Say which direction is the dangerous one.**

⚠ **Drill: whenever two carriers diverge on CREDITS, read both prerequisite chains before writing
the divergence up.** A credit difference is frequently a sequence-position difference wearing a
disguise, and the prerequisite is where the disguise comes off.

⚠ **Read the prerequisite before the description.** **It is harder to write loosely than a course
description and it constrains what the course can assume.**

### ⚠ Departmental placement is an emphasis signal too (batch 187)

**`SYD4800` sits in ANTHROPOLOGY at UWF, not Sociology** — predicting a stronger comparative and
cross-cultural frame. **`PLA4885` and `PLA4263` sit in CRIMINAL JUSTICE, not a law or legal studies
department.** ⚠ **The UWF prefix PDFs print the college and department on every entry; read that line.**

### ⚠ "May be repeated for up to N sh" + "Topics in" = a variable-content course (batch 188)

**`AML4640` at UWF: "Topics in Native American Literature", repeatable to 12 semester hours.**

⚠⚠ **Two consequences a guide must state.** The student can take it more than once for credit — unusual and
useful. **And the transcript line conveys nothing about what was actually covered**, since content varies by
term. **A receiving institution or a graduate programme evaluating it will ask, so the syllabus and reading
list are the only record.**

**Look for the repeat clause in the credit line; it is easy to read past.** Expect it on `AML`, `LIT`, `ENG`
and studio numbers.

### ⚠ Restricted-enrolment courses — a scheduling blocker no other source surfaces (batch 188)

**Courses closed to non-majors, or gated on a cumulative GPA, are invisible until registration fails.**
Instances so far:

| Course | Restriction |
|---|---|
| `ENG3010` (UWF) | English majors and minors only |
| `RTV3511` (FIU) | five prerequisite courses **and a 2.85 cumulative GPA** |
| **`APK4163` (FIU)** | **Bachelor of Science in Sport and Exercise Science major, or instructor consent** |

⚠ **Where a catalog states one, put it in the prerequisite field** — it determines whether a student can
plan a term around the course at all.

### ⚠⚠ For a queued `C` id, state the INTEGRATED form's hours (batch 189)

**`APK2000C` tripped the validator's first WARNING rather than a failure**: *"an integrated lecture+lab (C)
course but has only 45 contact hours"*, because the guide had been written to UWF's unsuffixed 45-hour
lecture version.

⚠ **The rule, now applied consistently across `BCN3224C`, `GIS4035C`, `ZOO4472C`, `APK4119C`, `APK4220C`
and `APK2000C`: give the integrated form's hours — that is what the queued identifier represents — and
describe the unsuffixed version alongside it.** **Doing it the other way round produces a warning and, more
importantly, a guide that does not describe the course the identifier names.**

### ⚠ Where a description names a discipline the prerequisite does not, that gap is where students fail (batch 189)

**`APK4220C`**: the formal gate is exercise physiology plus anatomy. ⚠⚠ **The description names "fundamentals
of engineering (kinematics and kinetics) and basic mathematics and physics" — and neither appears in the
prerequisite.** **Students arrive from a kinesiology curriculum that required no physics, meet vectors and
free-body diagrams in week two, and conclude the course is impossible.**

**Name exactly what is needed and say to prepare it** — for that course, trigonometry, algebra, units and
rates, **not** calculus. ⚠ **This is the counterpart to the prerequisite-as-signal diagnostic: read the
description for disciplines the gate omits.**

### ⚠⚠⚠ A 1-CREDIT `L` LAB IS NOT UNIFORMLY 45 HOURS — the majors/non-majors split is worth 15 (batch 228)

**The project has been publishing 1-credit laboratories at 45 contact hours by convention.
Gulf Coast State College publishes the real figures, and they are not the same:**

| Course | Published |
|---|---|
| `BSC2010L` — **majors** general biology lab | **3 lab hours** weekly → 45 |
| ⚠ `BSC1020L` — **non-majors** human biology lab | ⚠⚠ **2 lab hours** weekly → **30** |

⚠⚠ **Same college, same credit value, same prefix, and a 50% difference in scheduled time.**
**So "1 credit `L` = 45" is a ceiling rather than a default**, and the majors/non-majors distinction
is the thing that moves it.

**Handling: prefer a published figure, and where none exists ANCHOR the derivation on the closest
published comparator rather than on the bare convention.** `BSC1010L` was published at 45 because
Gulf Coast publishes 3 hours for the equivalent *majors* lab in the other numbering family — which is
a far better justification than "1:45 is the convention", and the guide says so.

⚠ **Check Broward and Gulf Coast before deriving any laboratory's hours.** Between them they cover a
large share of the high-enrolment lower-division laboratories.

### ⚠ Writing 1-credit LABORATORY guides (batch 189)

**`APK2100L` and `APK2105L` are the first lab-only guides written deliberately.** They are shorter than a
lecture guide — 21–23 KB against a batch average of 27 — **and that is correct: a 1-credit laboratory has
less to say about content and more about format, safety, assessment and transfer traps.**

⚠⚠ **State the credit-to-contact-hour ratio explicitly**: a 1-credit laboratory carries **two to three
contact hours a week**, so it consumes far more scheduled time than its credit value suggests. **Students
plan around credits and are caught by hours.**

⚠ **Where students are the SUBJECTS** (physiology, exercise testing), the guide must say: **participation is
voluntary, results are not medical advice, classmates' measurements are private, and bloodborne pathogen
procedures apply strictly.**

### ⚠⚠⚠ COURSE-TYPE divergence — a campus course at one school, a PLACEMENT at another (batch 200)

**A new category, and not a variant of any above.** Not a different subject, not title drift, not credits, not
chronology, not terminology era: **the same number is a different KIND of course.**

**`EDG4442`** — statewide *Teaching Strategies and Classroom Management*:

| Institution | Its title | What it is |
|---|---|---|
| UWF | Effective Learning Environments | campus methods course |
| UF | Rethinking Discipline and Classroom Management | campus methods course |
| **UNF** | **Elementary Field Experience III** | ⚠⚠ **supervised school placement** |

⚠⚠ **Why it outranks a title divergence in consequence.** A placement carries **Level 2 background screening
before entry to a building**, the **school district's** calendar during the school day, a cooperating
teacher's evaluation, and a placement a school can terminate. **A student who registers expecting a methods
course and gets a placement cannot solve it by working harder** — the logistics either fit their term or
they do not.

⚠⚠⚠ **And the transfer consequence is harder than the usual one: state programme approval specifies required
COURSEWORK and required FIELD HOURS separately**, so **one number can satisfy one and not the other, with
nothing in the identifier to say which.** **Tell the reader to take the syllabus to the programme's
certification officer and ask specifically.**

**Handling: one guide on the statewide subject, with the placement reading LABELLED and its logistics spelled
out**, plus a two-column test. **Screening, calendar, mandatory reporting and FERPA go in the prerequisite
field**, per the batch-184 rule.

⚠ **Expect more.** Field experiences, practica, internships and clinicals are routinely numbered alongside the
coursework they accompany. **When a batch turns one up, add it here.** See `REVIEW_QUEUE.md` item 75 for the
open split question.

### ⚠⚠ SEQUENCE-POSITION divergence — the whole course at one school, a PHASE of it at another (batch 200)

**Distinct from the sequence-PARTNER rule below, which is about two numbers splitting a subject. This is one
number meaning different amounts of the same subject.**

**`ATF1100L`** — statewide title **`PRIVATE PILOT FLIGHT (2 - 3 HOURS) (L)`**; carriers **NWFSC 1, Polk State
1, UWF 3.** The prefix family explains it: `ATF1108` *Primary Flight I (1 hour)* and `ATF1109` *Primary
Flight II (1 hour)* split the certificate into phases, and ⚠ **`ATF1108`'s own statewide description says a
student completes it and "would then take ATF1100."** **So `ATF1100` is the complete flight course at one
institution and the second phase at another.**

**Handling: write the identifier's full subject, give the credit value that matches that reading, and state
the phase reading in `offering_notes` and the body — labelled as an inference where it is one.** ⚠ **Tell the
reader the question to ask: how many hours does this specific course include, and does it end at completion or
at a phase?** **Neither the credit count nor the title answers it.**

### ⚠⚠⚠ A statewide TITLE can be a MATRIX CODE rather than a name — expand it (batch 229)

**`MUE` titles its methods and techniques numbers with database abbreviations, not course names:**

| Statewide title | What it actually means |
|---|---|
| `MUS METH/COMP/K-12/ GEN MUSIC` | music **methods**, comprehensive K-12, **general music** |
| `TECH-SKILL-MAT/COMP/K-12/INSTR-ORCH` | **techniques, skills and materials**, comprehensive K-12, **orchestra** |
| `TEC-SKILL-MAT/MID-JR-SEC/INSTR-BAND` | the same, middle/junior/secondary, **band** |

⚠⚠ **Two things follow.** **These strings are unreadable to a student and must be expanded in the
guide** — they are also what the site displays as `stateTitle` if nothing else is supplied. **And
the scheme is a MATRIX, so it can be READ AS ONE**: laying the axes out (course type × level ×
specialism) is what exposed the missing undergraduate instrumental-methods slot above.

⚠ **Where a prefix titles by abbreviation, tabulate the family before writing any single course.**
The gaps in a matrix are invisible one row at a time and obvious once it is drawn.

### ⚠⚠ The statewide TITLE is a data field — read it for parenthesised hour figures (batch 200)

**`PRIVATE PILOT FLIGHT (2 - 3 HOURS) (L)`.** ⚠⚠ **The state wrote the credit range into the title string**,
and **two of the three carriers sit BELOW the bottom of it** — the first case of the state's own record
carrying a credit figure that its carriers contradict.

- ⚠ **The `ATF` prefix does this repeatedly**: `ATF1103` "(5 HOURS)", `ATF1108` "(1 HOUR)", `ATF1600`
  "(1 HOUR)". **Read the title as data, not as a label.**
- ⚠ **The title also carries the `(L)` and `(G)` markers**, and `ATF1100`'s `IN_Lab` field says **`N`** while
  its title says `(L)`. **So `IN_Lab` is not reliable — match on `ID_Century` plus `DS_Course_Intent1`
  instead.**

### ⚠⚠ Where a REGULATOR measures the course, its floor beats the credit-to-hour convention (batch 200)

**`ATF1100L` was published at 40 contact hours, derived from the FAA minimum** — 35 flight hours under Part
141, 40 under Part 61 — **not from the Florida 1:15 convention.** A flight course's hours are hours in an
aircraft, **sold by the hour**, and the convention is meaningless for it.

⚠ **State the derivation and say the real figure is higher** where the regulatory number is a floor that
practice exceeds. **Expect the same shape wherever a licensing body sets hours**: flight training, clinical
and practicum hours, PSAV clock-hour programmes, apprenticeship hours.

### ⚠⚠⚠ EXTERNALLY-GOVERNED CURRICULUM — when the syllabus itself belongs to a body outside SCNS (batch 209)

**Every divergence rule in this file assumes the content authority is the INSTITUTION, with SCNS recording
it.** ⚠⚠ **`AFR` (Air Force ROTC) breaks that assumption: the curriculum is set nationally by Air Force
ROTC Headquarters (the Holm Center, Maxwell AFB), and every detachment in the country teaches the same
syllabus.**

⚠ **Distinct from the regulator's-floor rule above.** That is about **HOURS** — a regulator setting a
minimum the credit convention cannot describe. **This is about CONTENT AND TITLES — an external body
owning the syllabus itself.**

**Three consequences, and they invert the usual analysis:**

1. ⚠⚠ **The institutions CANNOT diverge from each other on content.** So institutional title variation is
   **pure catalog lag**, not a divergence signal — and the "two carriers agreeing outrank a statewide
   title" machinery (batch 183) is beside the point. **Do not write a divergence block for what is only
   two catalogs updating at different speeds.**
2. ⚠⚠⚠ **The statewide record is the LEAST current source available**, so it cannot be used to check a
   carrier's currency. On `AFR` it is forty years behind both carriers.
3. **The guide's statement of authority has to change.** These guides say: **judge the course by what the
   detachment issues in week one; nothing in this guide overrides cadre guidance.** ⚠ **That is the honest
   position whenever the real syllabus is issued by a body outside the state system** — and it is a
   stronger and more useful sentence than any hedge about institutional variation.

**Worked example — `AFR2132`, and the staleness is self-evident from the text:**

| | Statewide record | Current national curriculum |
|---|---|---|
| `AFR2132` | *The Development of Air Power II* — ⚠⚠⚠ description ends **"projects ahead to the year 2000"** | **Team and Leadership Fundamentals II** — leadership theory, team dynamics, ethics, Field Training prep |
| `AFR1112` | *The Air Force Today II* — "total force structure, offensive and defensive forces" | **Competition and Security** |
| siblings | ⚠ *Strategic Offensive Forces* / *Strategic Defensive Forces* — Cold War nuclear-triad vocabulary | — |

⚠⚠ **Note it is a change of SUBJECT, not just a title**: the AS200 year used to be air power history and
is now leadership and team fundamentals, with the history retained as case material. **Within Florida, UWF
uses the current national naming on all four numbers and Pensacola State still uses the older state
naming — same course, same national syllabus, different lag.**

⚠ **Where a statewide description names a future that has passed, say so in the guide.** It is the
clearest possible way to tell a student not to rely on the state record, and it is stronger evidence than
the embedded-date test (batch 208) because it needs no inference.

**Expect this shape in:** the other services' ROTC prefixes, nationally standardised certification
curricula, apprenticeship-linked coursework, and anywhere a national body **issues** the syllabus rather
than approving one.

#### ⚠⚠⚠ THE COMMERCIAL-VENDOR VARIANT — and how to DETECT it (batch 226)

**`CNT3112` is the same shape with a VENDOR in place of a national body, and it is probably the
commoner form.** Convergent evidence:

| Evidence | Detail |
|---|---|
| Statewide title | *Routing and Switching Essentials* — ⚠ the EARLIER Cisco CCNA module 2 name |
| UWF title | *Switching, Routing and Wireless Essentials* — ⚠ the CURRENT module 2 name |
| Description delta | UWF's is the statewide text **plus wireless** — ⚠⚠ **exactly the documented v6→v7 restructure** |
| ⚠⚠⚠ The prerequisite course | **UWF titles `CNT3004` *"Introduction to Networks"*** — **the module 1 name**, and NOT the statewide title |

**Two consecutive courses named after two consecutive vendor modules is not coincidence.**

⚠⚠ **THE DETECTION METHOD, and it is cheap: when a course TITLE reads like a product or module
name rather than a subject, check whether it matches a vendor certification track.** *"Routing and
Switching Essentials"* is not how a university names a subject; it is how a vendor names a module.
**Expect it in `CNT`, `CTS`, `CIS` and the Engineering Technology networking numbers.**

⚠ **Write it as an INFERENCE with the evidence shown unless you have seen a syllabus**, and give the
student a question rather than a claim — for `CNT3112`, *"ask which CCNA revision this course
follows"*, which also tells them which exam to sit.

⚠⚠⚠ **And the consequence INVERTS the usual transfer advice: what transfers is the
CERTIFICATION, not the number.** With one public carrier the "same course offered" condition bites
hard, **but a current vendor certification is recognised by every institution and employer in the
field.** **Say so.**

#### ⚠⚠ And check the CREDIT arrangement, because an external curriculum does not standardise credits (batch 209)

**The national programme fixes the content; each institution still decides what to award for it.**
`AFR`'s Leadership Laboratory is the worked case:

| Institution | Leadership Laboratory |
|---|---|
| Pensacola State, UWF | **0 credits** |
| ⚠ Santa Fe College, University of Florida | **1 credit** |
| ⚠ UCF | folded into a **2-credit integrated `C` course** with the lecture |

⚠⚠⚠ **Identical, nationally-specified work is worth 0, 1, or part of 2 credits depending on the
institution — and the pattern repeats across all four years** (`AFR1101L`, `AFR1112L`, `AFR2130L`,
`AFR2132L`, `AFR4211L`). **Credit-count divergence (batch 185) and split-family (batch 183) operating
together on one prefix.**

**What a guide must say:** **progression is governed by the external programme, not the registrar — but
full-time enrolment status IS governed by the registrar.** ⚠ **So tell the reader to count their credits
WITHOUT the zero-credit component and check the total against whatever threshold applies to them**
(financial aid, scholarship conditions, athletic eligibility, insurance, visa status). See the
zero-credit-laboratory rule in the schema section.

### ⚠ A title inside an SCNS prerequisite string can be a LOCAL title (batch 200)

**`COM4564`'s statewide prerequisite reads *"COM4561 Social Media Content Development with a grade of C- or
above"* — but the statewide title of `COM4561` is *Social Media Campaigns*.** "Social Media Content
Development" is **UWF's** title.

- ⚠ **Do not read a title inside `DS_Prerequisites1` as the statewide title.** The records are
  institution-contributed and a local title can land in a statewide field.
- ⚠ **Useful in the other direction: a prerequisite naming a local title tells you which institution
  contributed the entry**, and therefore which catalog to check. Here it confirmed a real `COM4561`→`COM4564`
  sequence at UWF with an explicit C-minus floor.

#### ⚠⚠ The prerequisite field can also be CORRUPT — sanity-check it against the id pattern (batch 209)

**`ADV4802`'s statewide prerequisite reads `"ADV U101C"` — which is not a valid SCNS identifier at all.**
⚠ **The first corrupted value this project has met in that field, and it is easy to pass straight into a
guide as though it named a real course.**

**Standing check: before quoting `DS_Prerequisites1`, test any course-looking token in it against
`^[A-Z]{3}\s?\d{4}[A-Z]?$`.** A token that fails is a data defect, not a course. **Say so in the guide
and send the reader to the institution's catalog** — which is what `ADV4802`'s guide does.

#### ⚠⚠⚠ And it can DANGLE — a well-formed token naming a course the CARRIER does not offer (batch 219)

**A second, commoner defect, and the syntax check above does NOT catch it.** **`TPA4021C`'s statewide
prerequisite reads `TPA 4020 LIGHTING DESIGN I` — a valid identifier naming a real, active course.**
⚠⚠ **But UWF, the ONLY carrier of `TPA4021C`, does not offer `TPA4020`** (FSU and UF do). **So the
state describes a prerequisite chain that does not exist at the institution teaching the course.**

⚠⚠⚠ **And UWF's own alternative, `TPA 3020`, is carried by NO Florida public institution at
all** — so of the three numbers naming that gate, one belongs to other schools and one belongs to
nobody. **The real gate is `TPA3022`.**

**Standing check, cheap once the flat file is loaded: for every course-looking token in
`DS_Prerequisites1`, ask whether the CARRIER OF THE COURSE YOU ARE WRITING actually offers it.**
⚠ **Where it does not, name the dangling reference in the guide and put the REAL gate beside it** —
a student reading the state record would otherwise go looking for a course their institution does not have.

⚠ **Expect it wherever a prefix runs PARALLEL NUMBERING FAMILIES** (below): the statewide prerequisite
was written against one family and the carrier uses the other.

##### ⚠⚠⚠ THE MECHANISM, found in batch 221: a SECTOR split makes prerequisites dangle on one side

**Batch 219 found the shape and could not explain it. `PLA` supplies two more instances and the cause.**

| Course | Statewide prerequisite | Resolves? |
|---|---|---|
| **`PLA4554`** | **`PLA 1003` AND `PLA 2203`** | ⚠⚠ **UCF carries NEITHER** — its real gate is **`ENC 1102`**. SPC carries both. |
| **`PLA3806`** | **`PLA 1003`** | ⚠ **FGCU carries it; UWF does NOT.** |

⚠⚠⚠ **Statewide prerequisites are INSTITUTION-CONTRIBUTED, so in a prefix that splits by sector
they get written from the side that HAS the lower-division numbers.** `PLA1003` and `PLA2203` are carried
almost entirely by state colleges. **At a university carrying no lower-division `PLA` numbers at all, the
statewide prerequisite names courses that are not on the menu.**

⚠⚠ **So the batch-219 check becomes targeted rather than general: whenever a prefix splits by sector,
EXPECT its statewide prerequisites to dangle on the other side.** **Check the prerequisite against the
CARRIER, not the state record, and name the real gate in the guide.**

⚠ **Useful in reverse: a dangling prerequisite is itself EVIDENCE of a sector split**, so the two
findings confirm each other. ⚠ **And the real gate is often something like freshman composition — which
tells you the course is open to students outside the major**, a genuinely useful student-facing fact.

##### ⚠⚠⚠ THE FIVE SHAPES OF A DEFECTIVE STATEWIDE PREREQUISITE (consolidated, batch 222)

**`DS_Prerequisites1` fails in five distinct ways, and they need different handling. Check every
course-looking token against all five before quoting the field.**

| Shape | Worked example | Tell | Handling |
|---|---|---|---|
| **Corrupt token** (209) | `ADV4802` — *"ADV U101C"* | fails `^[A-Z]{3}\s?\d{4}[A-Z]?$` | call it a data defect; send the reader to the catalogue |
| ⚠⚠ **PLACEHOLDER** (222, 226, ⚠ **corrected 234**) | **`COM4301` — *"COM 2XXX"*; `CNT3004` — *"CSG X060"*; `GEO4251` — *"GEO 5XX3"*** | ⚠ **a masked number.** ⚠⚠ **Look for `X` ANYWHERE in the numeric portion, not only as a trailing mask** | ⚠⚠⚠ **RECOVER THE REAL NUMBER — see below. Do NOT stop at "the number does not exist".** |

##### ⚠⚠⚠ CORRECTED (batch 234): a masked number is usually RECOVERABLE, and two of these are not placeholders at all

**Batch 222 recorded the handling as *"state the intent, say the number does not exist."* That is too
weak, and a scan of all 41 statewide CSVs on disk — 220 wildcard tokens — shows why.**

**First, two different things are wearing the same shape, and the discriminator is in the surrounding
text:**

| What you see | What it is | Handling |
|---|---|---|
| ✅ *"**ANY** 1XXX OR 2XXX COURSE WITH PREFIX CCJ, CJC, CJE, CJL, CJJ, PLA"* (`CCJ2453`) | **genuine LEVEL NOTATION** — any course at that level. The word **ANY**, or a prefix list, is the tell | **decode and explain it** (the batch-214 notation rule) |
| ⚠⚠ *"HFT 3XXX **GOLF PLANNING & OPERATIONS II**"*, *"BCN 3XXX **INTRODUCTION TO THE CONCRETE INDUSTRY**"*, *"GEO 5XX3 **(ADVANCED CLIMATOLOGY AND CLIMATE CHANGE)**"* | ⚠⚠⚠ **a PLACEHOLDER — and the masked number is FOLLOWED BY THE COURSE'S ACTUAL TITLE** | **use the title to find the real number** |

⚠⚠⚠ **In every placeholder case the writer knew exactly which course they meant and named it. So
the title recovers the number, and there are TWO routes:**

1. **Search the statewide TITLES in the same prefix for the quoted title.** Tested on four cases,
   **three recovered**: `GEO 5XX3 (Advanced Climatology and Climate Change)` → **`GEO?256`, graduate**;
   `PHC 5XX3 (Scientific Basis of Public Health)` → **`PHC?123`, graduate**; `BCN 3XXX (Introduction to
   the Concrete Industry)` → **`BCN?443`**. (`HFT 3XXX Golf Planning & Operations II` was not found —
   so some genuinely do not resolve.)
2. ⚠⚠ **Easier and more reliable: READ THE CARRIER'S OWN CATALOGUE ENTRY.** UWF's `GEO4251` says
   *"Offered concurrently with **GEO 5256** Advanced Climatology and Climate Change"* — **the exact
   number the state masked, published in full by the institution.** **The state record masks what the
   carrier prints.**

⚠ **And note where these cluster: `<PFX> 5XX3` appeared twice, in `GEO` and `PHC`, both inside
"offered concurrently with" DUAL-LISTING notes.** **So when a dual-listing note carries a masked
number, expect the graduate partner to be findable and give the reader its real number** — which
matters, because the repeat-restriction warning is useless if the student cannot identify the course
it applies to.
| **Dangling: sector split** (221) | `PLA4554` — names two FCS-only numbers; UCF carries neither | the prefix splits FCS/SUS | name the REAL gate; expect it across the whole prefix |
| ⚠⚠ **Dangling: single-carrier contribution** (222) | **`COM4120` — names `COM 3311`, carried by UCF ALONE, and UCF does not require it** | ⚠ **both carriers SUS; NO sector split** | same handling, but expect it ANYWHERE, not only in split prefixes |
| **Local title in a statewide field** (200) | `COM4564` — *"COM4561 Social Media Content Development"* | the quoted title is not the statewide title | ⚠ **search by NUMBER**; and read it in reverse — it names the CONTRIBUTING institution |
| ⚠⚠ **PROSE instead of an identifier** (227) | **`GRA2508C` — *"BASIC DESIGN OR CONSENT OF INSTRUCTOR"*** | ⚠⚠ **there is NO course-looking token at all, so the batch-209 syntax test never fires — the field names a SUBJECT, not a course** | **say there is no such course to find, give the carrier's REAL gate** (`DIG 2000C OR DIG 3001C`), **and send the reader to their own catalogue** |
| ⚠⚠⚠ **Dangling for EVERYBODY** (233) | **`PHY4445` — *"PHY 3054 OR PHY 3049"*** | ⚠⚠⚠ **BOTH alternatives have ZERO public carriers in the whole state** — well-formed identifiers naming nothing anyone can enrol in | **say the gate is unusable, give the carrier's real one, and ⚠ CHECK WHAT THE REAL GATE ADDS** — UWF's is `MAC 2313 AND MAP 2302 AND PHY 2049` with a C− floor, **and differential equations appears nowhere in the state record** |

⚠⚠ **The seventh shape is the extreme of dangling and the check is one flat-file pass.** Batch 219's
`TPA4021C` named a number that belonged to OTHER schools; **this one names two numbers that belong to
nobody.** **So run the carrier count on every token, not just on the carrier you are writing about** —
a zero means the gate cannot be satisfied by any student in Florida.

⚠⚠ **Note what the sixth shape breaks: every earlier test scans course-looking TOKENS. A prerequisite
made of prose has none, so it passes every check while telling the reader nothing actionable.** **Add
the question "does this field name a COURSE at all?" before running the token tests.**

⚠⚠⚠ **WORST CASE FOUND (batch 224): `JOU3342`'s statewide prerequisite is "JOU 3101 AND RTV
4301". UWF carries `JOU3101` but not `RTV4301`; UNF carries NEITHER.** **`RTV4301` is carried by FAU
and UF and `JOU3101` by USF, FAU, UWF and UF — so the two institutions that COULD satisfy the
prerequisite do not carry the course at all.** ⚠⚠ **The prerequisite was contributed by a
department that does not teach the course.**

⚠⚠⚠ **Batch 222 REMOVES a precondition from the batch-221 rule.** That rule concluded a sector
split causes dangling. **`COM4120` shows the simpler and more general cause: ANY prerequisite
contributed by one carrier may fail to resolve at another.** **A sector split makes it systematic; it
is not required for it to happen.** ⚠ **So run the carrier check on every statewide prerequisite,
not only in prefixes known to split.**

#### ⚠⚠⚠ PARALLEL NUMBERING FAMILIES — fragmentation running through a whole SEQUENCE (batch 219)

**Batch 207 measured number fragmentation on one LEVEL of Spanish. `TPA` shows it running through an
entire two-course sequence, so it compounds:**

| | Family A | Family B |
|---|---|---|
| **Lighting Design I** | **`TPA3022`** — FAU, UWF | **`TPA4020`** — FSU, UF |
| **Lighting Design II** | **`TPA4021C`** — UWF | **`TPA4021`** — FSU, UF |
| **Scene Design I** | **`TPA3064`** (UWF) / **`TPA3064C`** (FAU) | **`TPA3060`** — FIU, UF |
| **Scene Design II** | **`TPA4061`** — FIU, UWF | (none — FIU crosses families) |

⚠⚠ **Two anomalies worth noting because they defeat the obvious simplification.** The second
lighting course is **ONE number with TWO suffixes across the two families** — so the suffix, not the
number, separates them. And **`TPA4061` is carried by FIU, whose first course comes from the OTHER
family** — so the families are not clean institutional blocs.

⚠⚠ **GENERALISED (batch 226): an `OR` in a carrier's OWN prerequisite is a positive tell that the
statewide numbering does not line up at that campus.** `CNT4416`'s statewide gate names `CNT4403`,
`CIS4385` AND `CDA3101`; **UWF does not carry `CIS4385`, so its own prerequisite reads
`(CIS 4385 OR CIS 4221) AND CNT 4403`.** ⚠ **Read these `OR` lists as free evidence — they mark
exactly the points where a department has had to work around the state's numbering.**

⚠⚠⚠ **THE STRONGEST EVIDENCE THAT TWO FAMILIES ARE THE SAME COURSE IS AN INSTITUTION HEDGING
ITS OWN PREREQUISITE ACROSS THEM.** UWF requires *"TPA 3020 OR TPA 3022"* for `TPA4021C` and
*"TPA 3060 OR TPA 3064"* for `TPA4061`. **That is a department telling you, in its own catalogue, that it
treats the two numbers as interchangeable — and it beats any title comparison.** **Read institution
prerequisites for `OR` lists spanning statewide families; they are a free equivalence table.**

#### ⚠⚠ A statewide DESCRIPTION can be COPIED between numbers — diff the siblings (batch 219)

**`TPA4045` (Styles in Costume DESIGN) and `TPA3230` (Theatre Costuming I, a CONSTRUCTION course) share
EIGHT of their TEN statewide competency items verbatim.** ⚠⚠ **So the design number's competency
list carries CONSTRUCTION competencies** — *"costume cutting skills"*, *"high level skills in
development of patterns"* — **because they were carried across from the construction course.**

⚠ **Consequence: an item in a statewide competency list is NOT necessarily evidence about that specific
course.** **Drill: when a statewide description is a NUMBERED COMPETENCY LIST in the 1980s all-capitals
register, diff it against the sibling numbers in the family before quoting any item as a finding.** In
`TPA`, `TPA3601`, `TPA4020`, `TPA4045`, `TPA3060` and `TPA3230` are visibly one drafting exercise.

⚠⚠⚠ **AND READ ONE INSTITUTION'S DESCRIPTIONS AGAINST EACH OTHER, not only against the state (batch 225)**

**Every test in this file compares a CARRIER to the STATE.** ⚠⚠ **Batch 225's headline finding was
invisible to all of them:** UWF's `PET4434` and `PET4820` descriptions are identical but for four
words, **and their statewide titles are completely different**, so no title-comparison or
title/description test would ever fire.

⚠ **It was found by reading the UWF PDF output directly and noticing two entries several lines
apart.** **Standing move: when one institution carries several courses in a prefix, diff its
descriptions against EACH OTHER.** **An institution's internal coherence is evidence in its own right
— a matched pair, a deliberate sequence, or a copied description all show up this way and nowhere
else.**

### ⚠⚠ SURVEY THE PREFIX FAMILY from the statewide CSV before writing — a standing move (batch 200)

**One already-downloaded CSV and one filter on `ID_Century` paid three times in a single batch:**

| Prefix | What the family revealed that the course's own record could not |
|---|---|
| **`ATF`** | the phase/whole-course split that explains a **3× credit divergence** |
| **`ATR`** | ⚠⚠ the profession's **move to graduate-level entry** — sibling numbers read *"admission to MAT degree program"* and *"admission into the Doctor of Athletic Training program"*, and several are graduate courses still carrying **4000-level numbers** |
| **`EDG`** | **four adjacent numbers** competing for classroom management (`EDG4442`, `EDG4443`, and `EDG4444`/`EDG4447` sharing a title) |

```python
rows = scns.read_report_csv('scratchpad/sw_<PFX>.csv')
[r for r in rows if r['ID_Century'].startswith('44') and r['CourseStatus'] == 'ACTIVE']
```

⚠ **Do this whenever a course's credits diverge, its title diverges, or its field has a licensure
dimension.** **A sibling number's prerequisite string is frequently the most informative sentence available
about the course you are writing.**

### ⚠ A profession can outgrow its undergraduate numbers — say so (batch 200)

**`ATR3132` is an undergraduate course written for "athletic training majors" in a profession whose
entry-level degree is now the master's.** ⚠⚠ **An undergraduate `ATR` course is pre-professional coursework
and does not accumulate toward certification eligibility** — and no catalog says this.

**Handling: state the current entry requirement, say plainly what the course does and does not do, and tell
the student to work backwards from target graduate programmes' prerequisite lists** (this course generally
satisfies a biomechanics requirement — ⚠ **which is its real value, and worth naming**).

⚠ **Watch for the same shape elsewhere**: physical therapy (DPT), occupational therapy, audiology,
pharmacy, and physician assistant programmes have all moved their entry credential upward, leaving
undergraduate courses in those prefixes serving a purpose their titles no longer describe.

### ⚠ `VAR` in the flat file's credit column (batch 200)

**`TPA2290L` at UCF reads `VAR`, not a number**, where the other three carriers read `1.0`. ⚠ **Handled under
Ron's 2026-09-11 rule: `credits` is null in `offering_notes` and the note carries it — no min/max pair.**

**Say what it means for the reader:** the value depends on the assignment's scope and is set with the
department, **so ask what your registration is worth before you register**; and a variable-credit course
transferring into an institution that treats the number as a fixed value is settled by the logged hours and
the work record, not by the number.

### ⚠⚠ DEPARTMENTAL divergence — the same number in two different departments (batch 205)

**Distinct from the batch-187 departmental-placement signal.** That rule read a department off ONE
institution's own catalog line. ⚠⚠ **This is the same number taught in DIFFERENT departments at
different institutions, with the statewide record showing neither the department nor the consequence.**

**`POS3625` The First Amendment** is clean between institutions — identical titles at UNF and FSU, all
three carriers at 3 credits. ⚠ **But it is taught in political science at some institutions and in
journalism and mass communication at others:**

| Political science / public law | Journalism / mass communication |
|---|---|
| all six freedoms; **religion clauses at length**; doctrinal development | ⚠ **speech and press**; defamation, privacy, access and shield laws in practical detail; religion clauses lightly |

⚠ **Both are legitimate and they are different preparations** — a pre-law student wants the first, a
journalism student the second.

**Handling: give a diagnostic the reader can actually apply to the SYLLABUS, since the department cannot be
read from the data.** For `POS3625`: **look for the religion clauses on the reading list.**

⚠⚠ **Expect this wherever a subject has two departmental homes**: media law, statistics, technical
writing, ethics, research methods, nutrition, and public speaking. **The flat file will look clean and the
course will not be.** See `REVIEW_QUEUE.md` item 88.

### ⚠⚠⚠ A SEQUENCE CAN DIVERGE ON THE BOUNDARY *AND* ON THE ORDERING (batch 230)

**Sequence-length divergence (below) asks whether a field is one course or two. `FIL4036` adds two
further axes, and all three are live on one number:**

| | Statewide | Florida Atlantic | UWF |
|---|---|---|---|
| **Span of part 1** | 1890s → **1959** | ⚠ 1890s → **the 1940s** | ⚠⚠ **no boundary at all** |
| **Structure** | two courses | two courses | ⚠⚠ **one course; no part 2 exists** |
| **Ordering** | part 2 **requires** part 1 | ⚠ *"May be taken BEFORE"* — **either order** | n/a |

⚠⚠⚠ **So roughly two decades sit inside the course at one institution and outside it at another** —
for film history, that is noir, neorealism, the blacklist, the studio break-up and the arrival of
television. **A student can complete "Film History 1" at either and have covered materially different
material.**

**Handling: do not describe the span in the guide as though it were settled. Give the three readings in
a table and tell the reader to send a TOPIC or SCREENING LIST on transfer, not the course title** —
departments place by coverage, and a week-by-week list settles in seconds what a title cannot.

⚠ **Drill: where a numbered sequence exists (`I`/`II`, `1`/`2`), check THREE things, not one — where
each carrier draws the boundary, whether a part 2 exists at all, and whether the halves are ordered.**
Any of the three can diverge independently.

⚠⚠ **And run the batch-181 partner check regardless of what you find.** On `FIL4036` it paid: the
partner number `FIL4037` is *Film History 2* statewide and at FAU, **but USF carries it as *History of
Video Art*** — an unrelated subject. **So a student cannot simply enrol in the partner number wherever
they find it, and the guide has to say so.**

### ⚠⚠⚠ SEQUENCE-LENGTH divergence — the same field as ONE course or as TWO (batch 204)

**Distinct from sequence-position (one number meaning the whole course or a phase) and from the
sequence-PARTNER rule. Here the STATE numbers the same field both ways.**

**`PHY3107`** is *Modern Physics II*, the second half of a two-term sequence with `PHY3106`. ⚠⚠
**But `PHY3101` "Elements of Modern Physics" is a ONE-TERM upper-division treatment of the same field** —
and Florida numbers modern physics at least **seven** ways in total.

⚠⚠⚠ **Three consequences, and the guide must state all three:**

1. **A `PHY3101` completer has done ONE term, not the first half of two.** ⚠ **A one-term course
   compresses, and what gets compressed is usually the back half of the field** — for modern physics,
   the nuclear, solid-state and particle material, which is exactly what the second course is about.
2. ⚠ **A `PHY3106` completer transferring to a one-term institution may find there is no second course
   to take**, so the material is simply not available.
3. ⚠⚠ **Check how many institutions carry the second course at all.** **Only TWO Florida public
   universities carry `PHY3107`**, so a student cannot assume a second term exists at theirs.

**Handling: name the one-term alternative explicitly, say what it compresses, and tell the reader to send a
TOPIC LIST rather than a title on transfer** — departments place by content coverage. ⚠ **Expect
this wherever a field is taught as both a survey and a sequence**: modern physics, organic chemistry,
anatomy and physiology, world history, and the two-term-versus-one-term language sequences.

### ⚠⚠⚠ ORDINAL-BASE divergence — the same ordinal counted from a different origin (batch 203)

**Not title drift. The same numbering convention applied to a different starting point.**

**`JPN2200`** statewide is **"Intermediate Japanese I"**; **UWF calls it "Japanese III"**. **`JPN2201`** is
**"Second-Year Japanese 2"**; UWF calls it **"Japanese IV"**. ⚠⚠ **UWF counts SEMESTERS from the
start of the language** (Japanese I and II are the first year); **SCNS counts WITHIN the intermediate year.**
Both are correct.

⚠⚠⚠ **The consequence is a failed search, not a wrong course: a student looking in a UWF
catalog for "Intermediate Japanese I" will not find it**, and the trap runs both ways for anyone reading the
statewide list.

**Handling: state both namings explicitly and say they are the same course.** ⚠ **Expect it wherever a
subject is numbered by ordinal** — languages, `I`/`II` course pairs, studio levels, ensemble levels.

⚠ **Two related naming traps found on the same pair.** **The statewide titles of a sequence can be
internally inconsistent** (*"Intermediate Japanese I"* beside *"Second-Year Japanese 2"* — different
words and numeral style on consecutive numbers). And **an institution can use ONE title for BOTH halves of a
sequence** (UCF: *Intermediate Japanese Language and Civilization* for `JPN2200` and `JPN2201`) —
**tell the reader to register by NUMBER, not title.**

### ⚠⚠⚠ The `MUN` level digit encodes the STUDENT, not the course (batch 203)

**Florida numbers each music ensemble at three levels — and they are frequently the same ensemble.**

| Ensemble | Lower | Upper | Graduate |
|---|---|---|---|
| Symphony Orchestra | `MUN1210` | `MUN3213` | yes |
| Chamber Orchestra | `MUN1220` | `MUN3223` | `MUN6225` |
| String Ensemble | `MUN1410` | `MUN3413` | `MUN6245` |
| Guitar Ensemble | `MUN1480` | `MUN3483` | `MUN6485` |

⚠⚠⚠ **The same rehearsal, conductor and concert — with a first-year student, a senior and
a master's student enrolled under three different numbers.** **The level digit records the player's academic
standing.**

- ⚠ **"Upper Level" is NOT "more advanced ensemble"** — the chair is decided by the audition.
- ⚠⚠ **Tell the reader to register at their own classification**; credit at the wrong level may
  not count where a requirement expected the other.
- ⚠⚠ **You CANNOT derive the other level's number by changing the first digit.** The lower-level
  symphony orchestra is **`MUN1210`, not `MUN1213`**. **Look it up.**

⚠ **Also on `MUN`: the statewide record sometimes states an explicit REPEAT ALLOWANCE** —
`MUN3426` reads *"may be used in the degree program a maximum of 8 times."* **Where it appears, state it and
tell the reader to confirm how many their OWN degree counts**; a state ceiling is not a promise the degree
wants eight.

### ⚠⚠ MISFILING — when a carrier uses a number the state assigns to something else (batch 203)

**Distinct from subject divergence: here there is a RIGHT answer and the guide can name it.**

**`MUN3483`** is statewide **Guitar Ensemble**. UWF matches it; **UNF runs a JAZZ guitar ensemble** and
⚠⚠⚠ **UCF runs a STRING ensemble — a different instrument family.** And the state
**already numbers both**: jazz guitar at `MUN3484`/`3486`/`3488`, string ensemble at
`MUN3413`/`3414`/`3243`.

⚠ **FIFTH case of this shape as of batch 207**, and they are not alike — which is why the
handling differs:

| Number | What was misfiled | Shape |
|---|---|---|
| `PUR4801` | UWF's PR **campaigns capstone** on the *cases* number | a different course in the same subject |
| `MUN3483` | UCF's **string ensemble** on the *guitar ensemble* number | ⚠⚠ a different SUBJECT |
| `PSY3215` | FIU's **`PSY3211` methods-and-data-analysis course** on the *(CONT)* number | ⚠ the same subject at a different SEQUENCE POSITION |
| `SPM4012` | FIU's title is the statewide title of **`SPM4018`** (which nobody carries) | ⚠ TITLE-only misfiling — the content still matches |
| **`SPN3410`** | **UWF's `SPN3400` course** (*Conversation and Composition*) on the `SPN3410` number, **and `SPN3400` holds something else** | ⚠⚠⚠ **RECIPROCAL — a transposed PAIR** |
| **`TPA3223C`** | **UCF and FAU teach lighting DESIGN** on the number the state defines as lighting **TECHNOLOGY** | ⚠⚠⚠ **the MAJORITY of carriers are the ones misfiling** |

#### ⚠⚠⚠ THE SAME-INSTITUTION CONTROL — the one test that SETTLES a misfiling (batch 223)

**Every misfiling case before this rested on inference: the state says X, a dedicated number for Y
exists, therefore a carrier teaching Y on X's number is misfiling.** ⚠ **A sceptic can always answer
that the two subjects are not really distinct, or that the dedicated number is dormant.** **One piece of
evidence closes both objections.**

> ⚠⚠⚠ **When ONE institution carries BOTH numbers and files them the way the state does, the
> misfiling is proved.** **It demonstrates that the two subjects are distinct in practice AND that the
> state's assignment is workable — because somebody is working it.**

**Worked case, `INR3503` (batch 223).** Statewide *Model United Nations*, and the statewide description
agrees with the title (*"prepares students to represent an assigned country in a national Model United
Nations"*). **UWF teaches *International Organizations* on it.** Florida numbers International
Organizations separately **twice** — `INR3502` (FAMU, FIU, FAU, FSU, UF) and `INR4502` (USF, UCF,
FGCU), **nine public institutions**. ⚠⚠ **And FAMU carries BOTH `INR3502` and `INR3503`, filing
each correctly.**

⚠ **The check is cheap: on finding a suspected misfiling, scan the carrier list of the
suspected-correct number for an institution that ALSO carries the number in question.** Often one is
already there.

⚠⚠⚠ **AND IT WORKS IN BOTH DIRECTIONS — it can EXONERATE a carrier (batch 224).** Run on
`JOU4306`, where UF teaches *Advanced Data Journalism* on the statewide *Critical Journalism* number,
the control shows **UF carries `JOU3305` Data Journalism and files the INTRODUCTORY course
correctly.** ⚠ **What Florida does not provide is an ADVANCED data journalism number** — `JOU4305`
exists and nobody carries it — **so UF took an available number for a genuine two-course sequence.**

| Case | What the control showed |
|---|---|
| **`INR3503`** | FAMU carries BOTH numbers and files them correctly → ✅ **CONVICTS** |
| **`JOU4306`** | UF files everything else correctly and deviates on one number → ⚠ **EXONERATES** |

⚠⚠⚠ **THIRD INSTANCE, and the pattern is now established: MISFILING BY NECESSITY (batch 225).**
**UWF's `PET4434` and `PET4820` carry WORD-FOR-WORD IDENTICAL descriptions differing only in the age
band** — *"developmentally appropriate sport and physical activities for [children and young
adolescents | adolescents]"* — **a deliberate two-course sequence.** ⚠ **Neither statewide number
means anything like it** (*Curriculum Integration Through Movement* and *Teaching Team Sports I*),
**and Florida provides NO undergraduate number for sport pedagogy by age band** — the nearest,
`PET6206`, is graduate.

| Case | The gap the carrier was working around |
|---|---|
| `JOU4306` (UF) | no ADVANCED data journalism number exists |
| `PET4434` + `PET4820` (UWF) | no sport-pedagogy-by-age-band number exists at undergraduate level |
| ⚠⚠ **`GRA4882C` (UWF)** (227) | ⚠⚠⚠ **the number EXISTS and UWF ALREADY USES IT** — the state numbers comics ONCE and UWF teaches it as a THREE-COURSE SEQUENCE |

#### ⚠⚠⚠ A FOURTH INSTANCE, and a NEW CAUSE: the state's number is not WRONG, there is only ONE of it (batch 227)

**The first three cases are gaps — no statewide number describes what the carrier teaches.
`GRA4882C` is different and sharper: the number exists, the carrier uses it correctly, and the
carrier still has nowhere to put its third course.**

| UWF course | Statewide number it sits on | Verdict |
|---|---|---|
| `GRA3887C` Traditional Methods in Cartoon Design | `GRA?887`, same subject, ⚠ **title matches WORD FOR WORD** | ✅ **filed correctly** |
| `GRA3881C` Comics: Sequential Art and Design | `GRA?881` *Semantics of Design* | ✅ **matches in SUBSTANCE** — both are semiotics (see the title-divergence rule below) |
| ⚠ `GRA4882C` Advanced Comics | `GRA?882` *Analysis of Trends and Styles* | ⚠⚠ **diverges — and no number is left** |

⚠⚠⚠ **`GRA3887C` IS THE CONTROL, AND IT IS WHAT MAKES THE CONCLUSION SAFE.** Florida's only
comics number is `GRA?887`, whose statewide description explicitly names *"COMIC STRIPS, COMIC BOOKS,
GRAPHIC NOVELS"* — **UWF carries it and matches the statewide title exactly.** So the deviation on
`GRA4882C` cannot be ignorance of the scheme.

⚠⚠ **This is SEQUENCE-LENGTH divergence (batch 204) colliding with misfiling: the state numbers
the subject ONCE and the institution teaches it as a SEQUENCE.** **Expect it wherever a department
has built a multi-course specialism on a subject the state treats as a single elective** — and the
handling is the usual one for misfiling-by-necessity: **do not tell the reader to look for the right
number, because there is not one. Tell them the transcript line will not describe the course and the
WORK will have to.**

⚠ **Drill, and it is cheap: before concluding a carrier misfiled, count how many courses that
carrier runs in the subject and how many numbers the STATE provides.** Where the first exceeds the
second, the surplus courses are misfiled by arithmetic.

⚠⚠ **Settled handling for this shape: say there is NO "correct" number to go looking for, and lead
with the transfer advice rather than the adjudication.** **The student's problem is real whoever is at
fault, and "send the syllabus" is actionable where "your institution is misfiling" is not.**

##### ⚠⚠⚠ A GAP FRAGMENTS THE SUBJECT — it does not merely displace ONE course (batch 229)

**Batch 227 had one carrier working around one gap. `MUE` shows what happens when TWO carriers meet
the same gap: they improvise in DIFFERENT DIRECTIONS, and the subject ends up under two numbers
neither of which names it.**

**Florida's `MUE` methods numbers are a MATRIX** — course type × school level × specialism — and the
comprehensive-K-12 row has **no undergraduate instrumental METHODS slot** (`?348` exists and is
**graduate only**). Two universities needed that course:

| Institution | Its title | Number used | What the state says that number is |
|---|---|---|---|
| **University of Florida** | *Teaching Instrumental Music* (3 cr) | `MUE4422` | techniques/skills/materials, K-12, **instrumental-band** |
| ⚠ **FGCU** | *Teaching Instrumental Music* (3 cr) | `MUE4344` | ⚠⚠ **methods, K-12, GENERAL MUSIC** |

⚠⚠⚠ **The IDENTICAL TITLE at the IDENTICAL credit value, on two different statewide numbers.**

⚠ **So the cost of a gap is not one misfiled course — it is that the subject becomes unsearchable**,
because no single number collects it and no two carriers agree. **Say so in the guide and list the
alternatives by number**, which is the only thing that helps a student who arrived by searching.

⚠⚠ **Drill: having found a gap, do not stop at the one carrier in front of you — look for OTHER
carriers of the same subject under OTHER numbers.** In `MUE` that search found `MUE4422`,
`MUE4332` and `MUE4493` all carrying instrumental methods under different statewide subjects.

#### ⚠⚠⚠ A THIRD OUTCOME OF THE CONTROL: it can EXPLAIN a divergence rather than judge it (batch 229)

**The control has convicted (`INR3503`) and exonerated (`JOU4306`). `MUE4475` is the third
outcome — it shows a carrier running a genuinely DIFFERENT COURSE on the number, deliberately.**

| Carrier | On `MUE4475` | Audience |
|---|---|---|
| **UWF** (2 cr) | *Percussion Methods and Materials*, with school observations | students *"planning to practice teach in band programs"* — ✅ matches the statewide description |
| ⚠ **FAU** (3 cr) | *Advanced Percussion Literature and Pedagogy* | ⚠⚠ *"music majors in **percussion performance**"* |

⚠⚠⚠ **FAU ALSO carries `MUE2470` *Percussion Pedagogy and Methods* (1 cr), and THAT course's
description is the school-teaching one.** **So FAU has already placed the statewide subject
elsewhere and is using `?475` for something else on purpose.** The control does not convict FAU and
does not exonerate it — **it explains what the second course IS.**

⚠ **The tell that separated the two readings was a single phrase: FAU's description covers
"promotion and marketing."** **A school band director never needs that; a private studio teacher
does.** **Read a description for the ONE item that only one audience would need** — it identifies
the intended student faster than the title or the level.

**Handling: write both readings with a two-column audience test, and do NOT call either a
misfiling.** The student's question is *"which career is this course for?"*, not *"who is at fault?"*

⚠⚠ **So the control is not a misfiling detector; it tests whether the carrier is WORKING the
state's scheme.** **A carrier that files everything else correctly and deviates on one number is
telling you the scheme has a GAP, not that the carrier is sloppy.** **Run it before writing a
misfiling warning, and be willing to conclude that nobody is at fault** — the student's problem is
real either way, which is why the transfer advice should lead rather than the adjudication.

⚠⚠ **Related caution: THE DEDICATED-NUMBER TELL IS MUCH WEAKER WHEN THE DEDICATED NUMBER IS
DORMANT.** On `JOU4306` dedicated numbers exist for BOTH readings — `JOU4305` Data Journalism and
`JOU4015` Journalism Culture and Criticism — **and NEITHER has a carrier.** **A carrier cannot be
faulted for not moving to a number nobody uses.** **Check the carrier count on the "correct" number
before relying on the tell.**

⚠⚠ **And state the qualification honestly where one exists.** UWF's course is not simply the wrong
subject — it contains position papers, committee procedure and a simulation. **What differs is the
frame: at UWF the simulation serves a course about institutions; at FAMU the course serves the
simulation.** **Say that, and give the student the actionable answer** — for `INR3503`, *join the Model
UN team if you want competition experience.*

#### ⚠⚠ When MOST carriers misfile, the state is still the reference — but say so carefully (batch 208)

**`TPA3223C` is the first case where two of three carriers deviate.** ⚠ It is still misfiling rather than a
stale statewide title, because **the title/description test above comes out "agree"**: the state says
*Lighting Technology* and its description says *"equipment, dimmers, control and other electronics."*
And the batch-203 tell is decisive — **Florida numbers lighting design separately and the number is IN
USE**: `TPA4020` *Lighting Design I* is carried by FSU and UF.

⚠⚠ **CORRECTED, batch 219: `TPA4020` is not THE lighting-design number, it is ONE OF TWO.**
**`TPA3022` *Lighting Design 1* is a second, equally active statewide number, carried by FAU and UWF.**
⚠ **This STRENGTHENS the misfiling conclusion rather than weakening it** — there are now two
dedicated design numbers in use, so `TPA3223C`'s deviating carriers had two places to put a design course
and used neither. **But do not write that `TPA4020` is where Florida numbers lighting design; write that
Florida numbers it in two parallel families** (see PARALLEL NUMBERING FAMILIES above).

⚠⚠ **What makes this worth a guide's strongest warning is that the two readings are different
PROFESSIONS** — electrician and designer are different jobs, different unions (IATSE vs USA Local 829) and
different career paths, **and electrics is where nearly everyone starts and where the jobs are.** **A
student who needs the electrics skills and takes a design section graduates able to draft a plot and unable
to get hired to hang it.**

⚠ **This is the same professional-division split already open on `TPA3230C`** (costume construction vs
design, `REVIEW_QUEUE.md` item 25). **Two instances in one prefix makes it a `TPA` pattern, not a
coincidence — expect it on scenery, sound and costume numbers too, and check the design/craft axis on every
`TPA` course.**

#### ⚠⚠⚠ The reciprocal sub-shape: BOTH numbers displaced, in exchange with each other (batch 207)

| | State's definition | UWF | FAU | FIU |
|---|---|---|---|---|
| `SPN3400` | *Conversation and Composition I* | ⚠⚠ *Advanced Stylistics* | *Advanced Spanish: Conversation* | — |
| `SPN3410` | *Advanced Oral Expression I* | ⚠⚠ *Composition and Conversation* | ⚠ *Advanced Spanish: Conversation* | ✅ matches |

⚠⚠ **This is worse than a single misfiling, because checking the OTHER number does not resolve it — both
are wrong, so the usual diagnostic ("a dedicated statewide number exists for what they're teaching") points
back at a number that is itself occupied.** ⚠ **And FAU carries the IDENTICAL title on both numbers**, so
within FAU they cannot be told apart by title at all.

⚠⚠ **Drill, and it is cheap: whenever a misfiling is found, look up what the DISPLACED number holds at the
SAME institution.** If it holds the first number's subject, it is a transposition and **both guides need
the warning** — including any already published. `SPN3400` had a live guide when this was found; see
`REVIEW_QUEUE.md` item 89.

⚠⚠ **The mildest and probably commonest shape is the last: same subject, wrong position in a
sequence.** **What differs is what the course ASSUMES, not what it covers** — so the warning a guide owes
the reader is *"find out whether this is the first or the second course in the sequence,"* not *"this may be
a different subject."* ⚠⚠ **The tell: a dedicated statewide number exists for what the institution is
actually teaching.** **Handling: write the statewide subject, label the misfilings, show the numbering
table, and give the reader a concrete diagnostic** — for `MUN3483`, *which instruments does this
ensemble contain, and is the repertoire notated or chart-based?* See `REVIEW_QUEUE.md` item 83.

### ⚠⚠⚠ ALTERNATE-LEVEL PAIR — the state builds TWO versions and makes the student choose (batch 212)

**Every shape above describes institutions disagreeing, or a record going stale. This one is different:
SCNS has DELIBERATELY created a lower-division and an upper-division version of the same course, and it
says so in the course record.** All four `(U)` numbers in the `ATF`/`ATT` flight-instructor family carry
this sentence verbatim:

> *"As a higher-level course, it offers training beyond the scope of the lower-level alternate course.
> **Students must choose whether to take the lower-level or upper-level version of this course.**"*

⚠⚠⚠ **THE TEST IS THE SENTENCE, NOT THE `(U)` MARKER.** Checked immediately on the next batch: **`BCN`
has 279 active statewide records, several carrying `(U)`, and NOT ONE contains the "must choose"
sentence.** `(U)` on its own means only *upper division*, which is common and uninteresting.

**A real alternate-level pair needs all three:**

1. the **"students must choose"** sentence in the statewide description (`grep -c "MUST CHOOSE"` over the
   prefix CSV settles it in one command);
2. a **sibling with DIFFERENT last-three-digits** covering the same subject — `ATF` paired 500↔502,
   510↔511, 530↔531 and `ATT` paired 130↔134, **never the same number at two levels**;
3. `DS_Course_Intent1` reading **`UPPER` against `LOWER`** across that pair.

⚠⚠ **The cleanest confirmation is textual: `ATT3134`'s statewide description is `ATT2130`'s WORD FOR
WORD plus two sentences naming what the upper version adds.** Check that once the sentence has matched.

| Lower | Upper `(U)` | Upper adds |
|---|---|---|
| `ATF2500L`/`ATF2500` | `ATF3502L` | simulation technique, curriculum development, mentorship |
| `ATF2510L` | `ATF3511L` | the same, **plus 15 flight hours against 10** |
| `ATF2530L` | `ATF3531L` | the same |
| `ATT2130` | `ATT3134` | the same, **plus the FAA Advanced Ground Instructor certificate** |

⚠⚠ **Do not confuse it with three shapes it resembles:** the `MUN` level digit (which encodes the
STUDENT's standing on ONE course), sequence-POSITION divergence (one number meaning a whole course or a
phase), and sequence-LENGTH divergence (a field taught as one course or two). **Here both versions exist
at once, under different numbers, and the student picks one.**

**Handling: write BOTH halves, and put the choice in each.** A student landing on the lower number
otherwise sees nothing about the decision. ⚠ **Check whether one institution carries both** — Polk State
carries both halves of all four pairs at **equal credit**, which makes the upper version strictly better
there, and the guides say so and tell the reader to ask an adviser to justify the lower one.

#### ⚠⚠⚠ Why the choice matters — and it is worth 250–500 FLIGHT HOURS

**Two consequences, and no catalogue states either.**

1. **Upper-division credit.** A bachelor's degree requires it and a 2000-level course cannot supply it
   (Ron's 2026-09-01 correction: the 2000→3000 step is the real boundary).
2. ⚠⚠⚠ **A federal rule keyed to a COUNT of credit hours.** Under **14 CFR 61.160** the reduced-hour
   **Restricted-Privileges ATP** turns on **semester credit hours of aviation coursework** — **1,000 hours**
   with a bachelor's and **60** such credits, **1,250** with an associate and **30**, against 1,500
   standard. **Taking 1-credit versions across the three flight-instructor courses costs six credits
   against that count**, and the gap between thresholds is **250 to 500 flight hours.**

⚠ **State the two cautions:** the reduction needs an institution **holding an FAA letter of authorisation**,
and **that institution certifies eligibility** — so tell the reader to ask their programme, never to infer
it from a course number.

⚠⚠ **GENERALISE THIS: wherever a licensed field ties a federal or state benefit to a COUNT of credit
hours, a credit-value divergence stops being an accounting curiosity and becomes a career consequence.**
**Look for it in nursing, respiratory care, radiography and the other licensure ladders.**

#### ⚠⚠ And the credit divergence beneath it: ONE federal certificate, FOUR credit values

The batch-209 `AFR` rule said an external body can own a syllabus while each institution sets the credit.
**The CFI-Airplane certificate is the cleanest instance yet, because the federal requirement is one
published number that never moves:** `ATF2500L` **1 credit** (NWFSC, Polk State), `ATF2500` **2** (Broward,
FSCJ), `ATF3502L` **1** at Polk State and **3** at UWF — and **all four require the identical 25 hours of
flight training**, documented independently by three catalogues. **The work does not change. The credit does.**

#### ⚠⚠⚠ On flight courses the FAA minimum is also a BILLING floor

**NWFSC states on every flight course what no other Florida institution says out loud:**

> *"the hours above are based on FAA-syllabus minimums, and students will often exceed these minimum hours.
> **The cost for these additional flight hours is not covered by the course fee.**"*

⚠ **Contact hours on an `ATF` course are hours in an aircraft, sold by the hour** (the batch-200 rule), **so
exceeding the syllabus minimum — common, and not a failure — is charged to the student.** Say it, and tell
the reader to ask what recent students actually averaged.

⚠⚠ **Check whether the practical test is included.** Florida's own record for `ATF2510L`: *"This course does
not include the checkride; it is at the student's discretion to schedule and complete the MEI checkride."*
**So a student can complete the course, earn the credit, and not hold the rating.**

⚠ **Expect the validator to WARN on these** (3 credits against 20–31 contact hours). **That warning is
correct to keep** — the 1:15 classroom convention does not apply to flight training, per the `ATF1100L`
precedent. State the derivation in the guide and label the figure a floor.

### ⚠⚠⚠ The SAME `L` id as a 1-credit lab AND a full 3-credit course (batch 214)

**`BSC4401L` is the worst transfer trap found so far, because the split-family shape lands on the `L` id
itself:**

| | **UWF** | **FIU** |
|---|---|---|
| `BSC4401L` | *Forensic Biology*, **3 credits** — the COMPLETE course, standing alone | *Forensic Biology Lab*, **1 credit** — the LABORATORY only |
| companion | none | ⚠ **`BSC4401`** lecture, 3 cr, **corequisite** |
| total | 3 credits, one grade | 4 credits, two grades |

⚠⚠⚠ **Transfer matches on the NUMBER and fails on the CONTENT in both directions.** Tell the reader to
send the syllabus and the credit value, never the number. ⚠ **And note the suffix is doing both jobs at
once** — conventional at FIU, a full course at UWF — so the `L` warning below is not just "sometimes
bigger", it is **unreliable in both directions on the same id.**

### ⚠⚠ Read `hs_credit` from the CSV, and run the distribution test EVERY prefix (batch 214)

**The same field means opposite things in different prefixes, so the one-`Counter` test (batch 207) is the
gate before writing anything about it:**

| Prefix | `DS_High_School_Credit1` | Verdict |
|---|---|---|
| `ATF` / `ATT` | uniform | boilerplate — say so, or say nothing |
| `BOT` | 116 ELECTIVE, **6 SCIENCE** | discriminating |
| `BSC` | 248 ELECTIVE, **24 SCIENCE** | discriminating |

⚠⚠ **`BSC2311` is one of the 24**: a dual-enrolled student earns **high-school SCIENCE credit**, not
elective — it fills a science graduation requirement *and* earns college credit. **Lead with it where it
appears; nothing a student normally reads says it.**

⚠⚠⚠ **TOOLING CORRECTION: read these two fields from the statewide CSV, NOT the flat file.** The flat
file's `transferable` slot actually holds the **high-school-credit code** (`'EL'`/`'SC'`), so
`scns.FIELDS`' offsets for that pair are shifted. The flat file stays authoritative for carriers, credits,
titles and the Gordon Rule / gen-ed flags. See `REVIEW_QUEUE.md` item 97.

### ⚠⚠ Dual-listing is a DEPARTMENTAL pattern — probe for it, do not wait to meet it (batch 214)

**The batch-186 rule came from one instance. Three of four UWF Biology courses in one batch were dual
-listed** — `BOT4850`/`BOT 5852`, `BSC4303`/`BSC 5305`, `BSC4401L`/`BSC 5406L`.

⚠ **Standing practice: on any UWF Biology 4000-level course, look for "offered concurrently with".** It is
easy to read past, and **both consequences must be stated**: the pace sits above a typical undergraduate
course (a benefit), and **taking the undergraduate version may BLOCK taking the graduate one for credit
later** — which has to be known before registering, not after.

### ⚠ A prerequisite token that fails the id pattern is a DEFECT *or* NOTATION — they differ (batch 214)

**The batch-209 test** (`^[A-Z]{3}\s?\d{4}[A-Z]?$`) **correctly flags both, but the handling differs:**

| | Example | Handling |
|---|---|---|
| **Defect** | `ADV4802`'s `"ADV U101C"` — a single malformed token | say so, send the reader to the catalogue |
| **Notation** | `BOT4734C`'s `"BOT L010 OR BSC L010, CO: BOT U734L"` — ⚠ a consistent `L`/`U` scheme marking LOWER and UPPER division | ⚠ **decode and explain it** — here it means a lower-division biology prerequisite with an upper-division lab corequisite |

⚠ **The tell is systematic structure.** One bad token is a defect; a repeated prefixing convention is
notation, and decoding it serves the reader better than a warning does.

### ⚠⚠⚠ LICENSED-PROFESSION SEQUENCES: accreditation, cohorts and clinical hours (batch 215)

**`RET` (respiratory therapy) is the first complete professional sequence this project has written, and it
established handling that applies to EVERY licensed allied-health prefix** — nursing, radiography, dental
hygiene, health information management, athletic training.

⚠⚠⚠ **1. The credential runs through the PROGRAMME, not the credit.** CoARC accredits respiratory care
programmes **as programmes**, and in two distinct kinds — **entry into professional practice** and
**degree advancement** for therapists who already hold credentials. **NBRC exam eligibility runs through
completing an appropriate accredited programme, NOT through accumulating transferable credit.** A student
can hold credit for every course and remain ineligible. **Say so in every course of the sequence**, and
tell the reader to verify with the accreditor, the credentialing body and the state board directly.

⚠ **Work out WHICH KIND the programme is** — the tell is the curriculum: an entry-level programme has a
foundations course, a clinical sequence, and a terminal practicum completing new-graduate competencies.
⚠⚠ **Do not assume the sector predicts it.** The batch-206 note (FCS = entry-level A.S., SUS = degree
completion) is a tendency, not a rule: **UWF is SUS and runs an entry-level baccalaureate**, the batch-200
`ATR` shape of a profession raising its entry credential.

⚠⚠ **2. Cohort structure changes the arithmetic of a marginal grade.** Courses run **once a year** in a
fixed, gated sequence with clinical placements arranged around it. **A failure delays not one term but
until the course runs again — about a year — and may require re-application.** Reciprocal corequisites
make it worse: where a lecture and lab each list the other, **failing either means repeating both.**
**State this; students do not know it in their first term.**

⚠⚠⚠ **3. Clinical practicum hours are NOT classroom hours.** Use roughly **three contact hours per credit
per week** — 3 credits ≈ **135 hours**, 4 credits ≈ **180** — not the 45/60 classroom convention, which
misdescribes a rotation badly. **The validator will WARN and the warning is correct to keep** (same as the
flight-hour case). **Label the derivation.**

⚠⚠ **4. Placement clearances go in the PREREQUISITE field** (the batch-184 rule) and **must be started
weeks before the term**: Florida **Level 2 fingerprint screening**, immunisations and TB screening, drug
screening, health insurance, **BLS** — plus **ACLS** for critical care and ⚠ **NRP and PALS before a
neonatal-paediatric rotation**, where provider courses fill up and an uncertified student simply cannot
enter the unit.

⚠ **5. Transfer on COMPETENCY RECORDS, not course numbers.** A receiving programme must attest to your
clinical competence under its own accreditation, so it may accept the credit and still require its own
practicum. **Tell students to keep every competency evaluation and clinical hour log.**

### ⚠⚠ A LAB titled as its LECTURE — expect it on any lecture+lab prefix (batches 215, 217)

**Florida frequently gives a laboratory the title of its lecture, with no separate description**, so the
statewide record cannot distinguish the halves at all:

| Lab | Statewide title it is given |
|---|---|
| `RET3028L` | *Fundamentals of Respiratory Therapy* (its lecture's) |
| `RET3493L` | *Respiratory Disease Assessment* (its lecture's) |
| `GIS4035L` | *Remote Sensing of the Environment* (its lecture's) |
| `GIS4043L` | *Principles of Geographic Information Systems* (its lecture's) |

⚠ **Four instances in two batches. Stop treating it as a finding and expect it.** **Go to the
institution's catalogue for anything about the lab specifically** — both institutions distinguish the
halves properly in their own records even where the state does not.

### ⚠⚠ Formal AI course ATTRIBUTES are appearing — a new category (batch 217)

**UF's catalogue records an *Artificial Intelligence* attribute against `GIS4102C` (GIS Programming).**
⚠ The first formal institutional AI course designation this project has met.

**It matters to a student rather than being trivia:** UF runs a university-wide AI initiative, and such
designations **may count toward an AI certificate or minor and may appear as a transcript notation.**
⚠⚠ **Tell the reader to find out what it counts toward** rather than assuming it is decorative.

⚠ **Expect more.** Institutions are beginning to tag AI-related coursework formally, and no other source
records it. **Watch the UF CourseLeaf `Attributes:` line**, and check whether other catalogues carry
something equivalent.

### ⚠⚠ UWF DUAL-LISTS across departments — check every UWF 4000-level course (batches 214, 215, 217)

**The batch-186 rule came from one instance. It is now a UWF-wide practice, not a departmental quirk:**

| Department | Courses |
|---|---|
| Biology | `BOT4850`/`BOT 5852`, `BSC4303`/`BSC 5305`, `BSC4401L`/`BSC 5406L` |
| Health Sciences | `BSC4401L` and the `RET` sequence |
| Earth &amp; Environmental Sciences | `GIS4006`/`GIS 5007`, `GIS4035L`/`GIS 5027L`, `GIS4043L`/`GIS 5050L` |

⚠ **Standing practice: look for "offered concurrently with" on ANY UWF 4000-level course.** Both
consequences must be stated — the pace sits above a typical undergraduate course (a benefit), and
**taking the undergraduate version may BLOCK taking the graduate one for credit later**, which has to be
known before registering.

### ⚠ An `L` suffix does NOT reliably mean "1-credit lab partner" (batch 203)

**`OCB3108L`** — *Study Abroad in Florida: Marine Field Studies* — runs **3–4 credits** at UNF
and UWF. ⚠⚠ **It is a full field and study-abroad course numbered `L` because it is ENTIRELY
practical work**, not a laboratory attached to a lecture.

⚠ **This is the first counterexample to an assumption embedded in the project's contact-hour heuristics
and in `validate_drafts.py`'s 1-credit expectation for `L` courses.** **Check the credit value before
applying the lab-guide treatment.**

### ⚠ When a number diverges, check its SEQUENCE PARTNER (batch 181)

A divergence found on one number is not necessarily isolated. **Where a subject is split across a pair of
numbers — an ESE methods sequence, a two-term language sequence, `I`/`II` course pairs — the split itself is a
curricular decision, and two institutions can draw it in different places.** That produces **two**
divergences, not one, and the second is invisible if only the first number is probed.

**Drill:** on finding a divergence, identify the number's partner from the prerequisite chain or the title
family, and probe it at the same institutions before writing either guide. `EEX4254`/`EEX4474` is the worked
example.

**⚠ Watch for more.** This is the extreme end of the drift theme, and two cases surfaced in a single
prefix — so there are almost certainly others already published as single guides. **When a batch turns one
up, add it here.**

---

## Institution order, per-school queues, and what to do when a catalog blocks

**Ron's direction, 2026-09-04.** Work the **smaller schools first — UWF, UNF, FGCU** — then the large ones
(**UCF, UF, USF**), mixing in state colleges. **Keep other schools' work ready to promote**, so a
bot-blocked catalog stalls nothing.

### The queue is now two-layer

| Layer | File | Role |
|---|---|---|
| **Master** | `queue.csv` | **single source of truth for what is DONE.** One row per course. Now carries a **`source_inst`** column recording which institution's catalog a guide was written from. |
| **Per-school** | `queue_<SCHOOL>.csv` | a *work list*, derived on demand. Courses that school offers which the master has not finished. Disposable — rebuild any time. |

```bash
python school_queue.py coverage            # per-school workable counts
python school_queue.py build UNF           # write queue_UNF.csv
python school_queue.py status              # what per-school queues exist
```

**Deduplication is automatic**: a course `pushed` or `skipped` in the master is emitted for **no** school.
The only exception is a deliberate one-number-two-subjects split, handled by publishing `XXXnnnn-<INST>`
ids rather than by re-queueing the bare number.

**⚠ Rebuild a per-school queue after every push.** It is derived, not maintained — a stale one will
re-offer finished work.

### ⚠⚠⚠ Focus decision (Ron, 2026-09-09): COMPLETE THE PREFIX, and ENGINEERING FIRST

**This supersedes the 2026-09-04 focus decision below.** Ron's direction, verbatim:

> *"As we progress, try to do all courses in a prefix as we come across the prefixes. Engineering and
> Engineering Technology prefixes have priority, even if there are classes that are only taught at a
> single school."*

Three changes to how batches are chosen:

1. **Finish the prefix.** When work touches a prefix, complete it rather than taking only the queued
   rows from it. A half-done prefix is the thing to avoid.
2. **Engineering and Engineering Technology prefixes come first**, ahead of strict institution-count
   ordering. The SCNS disciplines that qualify: **171** engineering general/support, **028**
   civil/environmental, **029** electrical, **172** mechanical, **173** industrial, **174**
   chemical/nuclear, **175** computer math/materials, **413** biomedical, **058** ocean, and **032**
   engineering technologies.
3. **⚠⚠ Single-institution courses are IN SCOPE.** This is the largest change. It reverses the
   ≥2-institution filter that has shaped the queue since the project began.

#### ⚠⚠ What this means mechanically: `courses_2plus_institutions.csv` no longer defines the work

The master inventory holds **only courses at two or more institutions** — so single-school courses are
not merely deprioritised, they are **structurally invisible** to `queue_mgr.py add`, which refuses any
course not in the master.

**Use the SCNS flat file as the inventory instead** (`scratchpad/scns.py`, see `SOURCES.md` Tier 3).
It lists every course at every Florida institution, so it is the only source that can enumerate a
complete prefix. Filter to **active** status, **levels 1-4**, and drop `x9xx` shells.

⚠ **Single-institution courses still get the single-institution TREATMENT.** Scope changed; the
quality bar did not. A course at one school is written as a custom guide for that school, with
explicit hedging, per the hedging-by-institution-count rules above. Do not let wider scope become
thinner sourcing.

#### ⚠ Prefix completeness is now the progress measure

"Done" for a prefix means every active, non-shell, undergraduate course in it has a guide — not
every queued row. **`EEE` illustrates the difference: 29 queued rows were completed on 2026-09-09,
which finished the prefix under the old rule and left 78 of its 108 courses unwritten under this one.**

**Report prefix coverage as `pushed / total` from the flat file**, not as queue rows cleared.

### ⚠ Superseded — Focus decision (Ron, 2026-09-04): priority courses across schools, NOT full catalogs

**Superseded 2026-09-09 by the decision above.** Retained for the reasoning, which still applies as a
tie-breaker *within* a prefix: where a prefix is large, work its higher-institution-count courses first,
because breadth across institutions serves more students per guide.

The per-school queues from `school_queue.py` exist for **block recovery and sequencing**, not as a
target to exhaust. The original text read: *"Work the master `queue.csv` — the ≥2-institution priority
subset — not a school's complete offering &hellip; Do not expand a batch into non-priority courses just
because a prefix extraction is already in hand."* **That restriction no longer holds** — completing the
prefix is now the goal, and a prefix extraction already in hand is exactly what should be expanded.

### ⚠⚠ Source reachability register (re-probed 2026-09-06, batch 164)

**Check this before committing to a school.** Reachability, not course count, is the binding constraint.

| School | Pattern | Status |
|---|---|---|
| **UWF** | `catalog.uwf.edu/courseinformation/courses/<prefix>/<prefix>.pdf` (**lowercase**) | ✅ **working** — one fetch per prefix, full descriptions. The workhorse. ⚠⚠ **But it does NOT cover every prefix UWF carries** (found batch 212): `atf` **404s** and `att` is a **title-only stub**, though UWF is an active SCNS carrier of both. The course-information index simply does not list them. **A 404 here is not proof UWF lacks the prefix — fall through to the search route below.** |
| **⚠⚠ UWF PDF parsing** | `scratchpad/uwf_pdf.py` | ⚠⚠⚠ **USE THE PARSER, NOT A NAIVE SPLIT (batch 215).** CourseLeaf lays each entry out as `HEADER … Co-requisite: RET <other>` **then** the description, **then** the next header — so **splitting extracted text on `/ABC \d{4}/` cuts at the COREQUISITE REFERENCE and attaches every description to the WRONG course.** It produced three confidently wrong descriptions before being caught. ⚠ A second attempt failed differently: a lazy `(.*?)` title pattern spanned a whole description to reach the next entry's "College of" — **constrain the title to ≤90 chars with no sentence period.** ⚠⚠ **The general lesson: an extraction bug does not error, it returns plausible text for the wrong record.** It was caught only because "Clinical Practicum I" described ventilator theory. **Sanity-check extracted text against what the title claims.** |
| **UWF (search route)** | **`catalog.uwf.edu/search/?P=<PREFIX>%20<NUMBER>`** — `scratchpad/uwf_search.py` | ✅✅ **TOOLED AND RECORDED 2026-09-15 (batch 212). Use whenever the prefix PDF 404s or comes back empty.** ⚠ The session before had already found this route by hand and left cached results but **no register entry**, so batch 212 rediscovered it from scratch — **record a route here the moment it works, not at the end of the batch.** Returns the full course block: description, credits, prerequisites **and the college and department** (a batch-187 departmental signal the PDFs never carry — it is how UWF's aviation programme was found to sit in the College of Business). ⚠ The element is `<article class="searchresult search-courseresult">`, **not a `<div>`**. |
| **FGCU** | `catalog.fgcu.edu/courses/<prefix>/<prefix>.pdf` | ⚠⚠⚠ **BLOCKED as of 2026-09-17 (batch 231) — RE-PROBE BEFORE ASSUMING IT IS GONE.** Returns an **empty 202** on `phi`, `mue`, `bsc`, `egn` and `eng` — **6 requests across 2 days and 5 prefixes**, which is past what the batch-183 rate-trigger caution covers but is NOT proof of a permanent block. **This was the single most productive cross-check source in the project**, so the loss is significant: it documented credits explicitly and produced the divergence a guide turned on in three consecutive batches. **Probe it at the start of every session** (a prefix FGCU certainly carries — `bsc` or `eng`); a full body means it is back. See `REVIEW_QUEUE.md` item 104. |
| **FSU** | `registrar.fsu.edu/bulletin/undergraduate-departments/<department>` | ✅ **working, and general-purpose.** Previously recorded here as useful only for the FAMU-FSU joint engineering college — **it is not.** Clean HTML with full descriptions, credits and prerequisites for `psychology`, `philosophy`, `social-work` and others. **Use it as the third vote when UWF and FGCU disagree.** |
| **⚠⚠ SCNS (statewide)** | `scratchpad/scns.py` — `flscns.fldoe.org` | ✅✅ **SOLVED 2026-09-09 (EEE sweep). CHECK THIS FIRST, BEFORE ANY INSTITUTION CATALOG.** `flatfile` downloads the whole SCNS database (~80 MB) carrying, per course, **both the institution's title AND the statewide title**, the authoritative institution list for the **exact** id, per-institution credits, and Gordon Rule + gen-ed flags. `statewide <PREFIX>` returns full descriptions, prerequisites and transferability as CSV. ⚠ Routes are **extensionless**; you must **accept the terms modal** first or reports return 0 rows silently; the report is an async SSRS viewer. All three handled in `scns.py`. See `SOURCES.md` Tier 3. |
| **UF** | **`catalog.ufl.edu/UGRD/courses/<department>/`** — plain CourseLeaf page | ✅ **UPGRADED 2026-09-09.** The department page returns **full descriptions, credits and prerequisites** for every course in the department — far better than the POST API below, which gives title and existence only. Department slugs are descriptive (`electrical_and_computer_engineering`). |
| UF (old route) | `scratchpad/uf.py` — the `catalog.ufl.edu/course-search/api/` POST | ⚠ superseded by the CourseLeaf page above; keyword must be spaced (`"POT 4204"`), title and existence only, `route=details` broken. |
| **UCF** | **Kuali API** — `ucf.kuali.co/api/v1/catalog/public/catalogs/`, then `/api/v1/catalog/courses/<catalogId>`, detail by **`pid`** | ✅✅ **NEW 2026-09-09 — the first working UCF route in the project.** UCF's acalog catalog (`catalog.ucf.edu/preview_course_nopop.php`) now 307s to a WordPress shell; the real catalog is **Kuali** at `ucf.kuali.co`. Returns 3,676 courses with description, credits, **weekly lab hours** (`labStudioFieldWorkHours`), structured prerequisites, department, college and terms offered. ⚠ The detail endpoint needs the **`pid`**, not the `id` — the `id` returns an empty list. UCF is **3,872 workable rows**, so this unblocks the single largest school in the queue. |
| **Broward** | `catalog.broward.edu/course-descriptions/<prefix>/` | ✅ **RECOVERED 2026-09-06** and used productively in batch 166. ⚠⚠ **The only routinely fetchable Florida source that publishes CONTACT HOURS explicitly** ("Total Contact Hrs: 48.00 / Lecture Hrs: 48.00") plus minimum-grade prerequisite conditions. **Go here first whenever a contact-hour figure is in doubt.** |
| **Valencia** | `catalog.valenciacollege.edu/coursedescriptions/coursesoffered/<prefix>/` | ✅ **RECOVERED 2026-09-06** — 200 with full body on `psy` and `mus`. Same regression, same recovery. |
| **DSC** | `daytonastate.smartcatalogiq.com/en/<year>/college-catalog/course-descriptions/<prefix-slug>/<level>/<course>` | ✅ **Confirmed on the CURRENT catalog 2026-09-07**, not just historically. ⚠ Two gotchas: the prefix slug is descriptive (`cop-computer-science`, not `cop`), and **the index page lists only titles — the individual course page carries description, credits, prerequisite and term**. A trailing slash 404s. **Same platform as IRSC.** |
| **UNF** | live catalogue + `digitalcommons.unf.edu/course_catalogs/` | ⚠⚠ **LEAD CHASED AND CLOSED 2026-09-15 (batch 216).** The live catalogue (`catalog.unf.edu`, `www.unf.edu/catalog/courses/`) answers with a large page but is **client-rendered** — the course index contains **no course content**. The archived-PDF lead is **REAL**: the DigitalCommons page lists catalogue PDFs by year and the article ids map cleanly (2025-26 = `article=1071`, counting down by year). ⚠⚠⚠ **But the PDF download returns 403 with or without a Referer** — bepress bot-blocks it. **So the archive exists, the ids are known, and the download is blocked. Do not re-attempt; write UNF courses from the statewide record and another carrier, and say so in the guide.** |
| **FSW** | `catalog.fsw.edu` (acalog, `catoid=27`, Course Descriptions `navoid=5491`) | ⚠ **PARTIAL BLOCK** — root returns 200 (26 KB) but **`content.php` and `search_advanced.php` both return empty 202s.** Root-reachable, content-blocked. |
| **FIU** | Coursedog API — `scratchpad/coursedog.py` | ✅ **SOLVED 2026-09-06 (batch 167). 27,923 courses, cached in `scratchpad/fiu_courses.json`.** ⚠⚠ **The gate is one header: `Referer: https://catalog.fiu.edu/`** — without it every endpoint returns `{"error":"Unauthenticated"}`. Richest Florida source: code, name, credits, college, description, cipCode, and per-component **contactHours**. ⚠ Duplicate rows per code — prefer the one with a real college name and a description. Full paging takes 2-3 min; **use the cache**. |
| **FAU** | Coursedog — `scratchpad/coursedog.py fau` (school `fau_banner_ethos`, catalog `Zm7WidFIJix2TYXQumos`) | ✅✅ **REOPENED 2026-09-16 (batch 228). 7,127 courses, cached in `scratchpad/fau_courses.json`.** ⚠⚠⚠ **This row previously read "no public Coursedog catalog at that host… Stop attempting FAU." That was TRUE when written (batch 173) and is now STALE — FAU has since attached a catalog.** Full descriptions, credits, college and department, and **explicit corequisite text** (it is what showed `BSC1010`/`BSC1010L` to be reciprocal). Honors College versions appear under the same number. **FAU is a large SUS institution that the project had written off; it is now a first-class source.** |
| **Coursedog discovery** | `app.coursedog.com/api/v1/catalogs/urls?url=<host>` (+ Referer) | ✅ **The portable bootstrap.** Returns `school` and `catalog.id` in one call — use it instead of scraping the page for ids. Works for any Coursedog school. ⚠⚠ **It still accepts `Referer` alone, but the COURSE-SEARCH endpoint no longer does** — see the row below. **Discovery succeeding tells you nothing about whether a fetch will.** |
| **⚠⚠ Coursedog auth (changed)** | `Referer:` **and** `Origin:` | ⚠⚠⚠ **CHANGED 2026-09-15 (batch 212).** Batch 167 recorded the gate as ONE header. **`Referer` alone now returns `401 Unauthorized`** on `/api/v1/cm/<school>/courses/search/$filters`; adding **`Origin: https://<catalog host>`** returns 200. Both are in the rebuilt `scratchpad/coursedog.py`. **If Coursedog 401s again, suspect another header before concluding the route is closed.** |
| **⚠⚠⚠ acalog = presumptively UNREACHABLE** | **NINE** institutions and counting | ⚠⚠⚠ **PLATFORM-LEVEL PATTERN, not seven coincidences (batch 215, confirmed 220).** **FSW, TSC, CF, Polk State, Santa Fe, FAMU, St. Johns River State, Florida Polytechnic and ⚠ USF** all serve an acalog (Modern Campus) root that answers 200 while `content.php` and `search_advanced.php` return **empty 202s**. **Treat an acalog host as content-blocked unless proven otherwise** rather than probing each school hopefully — identify the platform first, and if it is acalog, plan to write from the statewide record and another carrier. |
| **FAMU** | `catalog.famu.edu` — acalog (Modern Campus) | ⚠ **CONTENT-BLOCKED, probed 2026-09-15.** Root 200 (56 KB); `content.php` and `search_advanced.php` empty 202s. Not Coursedog (bootstrap: *"does not exists"*). ⚠⚠ **FAMU ≠ FAU** — different institutions, both unreachable for different reasons. FAMU is a main carrier of the `RET` professional sequence, so eight batch-215 guides name the gap. |
| **Polk State (PSC)** | `catalog.polk.edu` — **acalog (Modern Campus), `catoid=55`** | ⚠ **PARTIAL BLOCK, probed 2026-09-15.** Root answers 200 (53 KB) but **`content.php` and `search_advanced.php` both return empty 202s** — the same content-blocked pattern as FSW, TSC and CF. Not a Coursedog school (bootstrap: *"does not exists"*). ⚠⚠ **Note the code: `PSC` is POLK STATE. Pensacola State is `PESC`** — a previous session probed `pensacolastate.edu` as "psc" and was reading the wrong school. **Check `inst_map.json` before trusting an obvious-looking three-letter code.** |
| **USF** | `catalog.usf.edu` — **acalog (Modern Campus)** | ⚠⚠ **IDENTIFIED AND CONTENT-BLOCKED 2026-09-17 (batch 232).** Root answers 200 (75 KB) **with acalog markers**; `content.php` returns an **empty 202**; the Coursedog bootstrap says the host *"does not exists"*. **NINTH institution in the acalog pattern.** ⚠ This row previously read "no course-description path exposed — not yet a route", which invited re-probing; **it is now a settled negative.** USF is a frequent carrier on health-sciences and communication prefixes, so expect to write its courses from the statewide record and another carrier. |
| **Gulf Coast (GCSC)** | `www.gulfcoast.edu/catalog/current/courses/<prefix>/index.html` | ✅✅ **RE-PROBED AND WORKING 2026-09-16 (batch 228)** — one fetch per prefix, 131 KB on `bsc`. ⚠⚠ **It is the SECOND Florida source that publishes CONTACT HOURS explicitly** (after Broward): every entry carries `Credit hours: N` plus `Lecture hours: N` and/or `Lab hours: N`. **It also publishes LAB FEES in dollars, term availability, and degree-exclusion rules** (*"cannot be used to satisfy degree requirements by students who already have credit in…"*), none of which any other routine source gives. **Go here whenever a contact-hour or fee figure is in doubt.** |
| **EFSC** | `catalog.easternflorida.edu/course-descriptions-information/<prefix>/` (and `/<prefix>.pdf`) | ✅ **NEW 2026-09-07 — CourseLeaf, same as UWF/FGCU/Broward/Valencia, existing tooling works unchanged.** Recovered `ADV2000C` and `COP3813C`. On CourseLeaf a prefix the college does not carry returns **202** — probe a prefix it definitely has. |
| **Tallahassee (TSC)** | `catalog.tsc.fl.edu` | ⚠ **CORRECTION: never blocked — the college RENAMED.** TCC → Tallahassee State College; `catalog.tcc.fl.edu` 000 was a dead host, not a block. New host is live (386 KB) but acalog `content.php` returns empty 202s. **Lesson: follow redirects on the main domain before recording a block.** |
| **IRSC** | **`irsc.smartcatalogiq.com/-/media/institution/irsc/pdf-catalogs-2011-12-through-2024-25/Indian%20River%20State%20College%20<YEAR>.pdf`** | ✅✅ **EXERCISED AND WORKING 2026-09-16 (batch 228) — but NOT the way the lead assumed.** The `/en/<year>/catalog/…` SmartCatalogIQ path **404s**; the root page instead links **whole-catalogue PDFs by year**, and the 2024-2025 file downloads clean (**3.2 MB, 303 pages**). Full course descriptions with prerequisites AND corequisites, and — because it is the whole catalogue — **programme prerequisite tables too**, which is how `MCB2010`'s gate was found. ⚠ Parse with `pypdf`; it emits "Ignoring wrong pointing object" warnings that are harmless. **Contrast UNF, where the archived-PDF route is the same idea and is 403-blocked: here it is simply open.** |
| ✅✅ **CPALMS-CTE (FLDOE frameworks)** | **`cteservice.cpalms.org/api/`** — `scratchpad/cpalms.py` | ✅✅✅ **NEW 2026-09-17 — RECOVERS THE TIER-1 CTE SOURCE THAT DIED WHEN `fldoe.org` WENT 403 on 2026-09-02** (still 403 today, pages and PDFs alike, with a browser UA). Ron supplied the CPALMS route; its Angular bundle named an **open** API. **987 CTE programmes** cached in `cpalms_programs.json`, with occupational completion points, courses, **SOC codes** and industry certifications. ⚠ **The gate is `Origin` AND `Referer`, both `https://ctepreview.cpalms.org`** — the Coursedog shape; try it on any closed Florida SPA. ⚠⚠ **Florida writes a 10-digit programme CIP (`0648050805`) and the FEDERAL code is characters 3-8** (→ `48.05`); the outer digits are level and serial, not part of the code. |
| **⚠ Inventory reliability** | `courses_2plus_institutions.csv` | ⚠⚠ **The institution list is a HYPOTHESIS, not evidence — five confirmed errors in four batches** (`MUG2101`, `TPA3230C`, `BOT4404C`, `ATT1120`, `COP3014C`, all wrongly listing UWF or a suffix nobody uses). Two patterns: an institution listed that carries the subject under a **different number**, and a **suffix** in the inventory that no institution actually uses — both consistent with the file recording the SCNS catalog rather than current offerings. **Verify against a live catalog before treating an institution as a source or asserting a count in a guide.** ⚠⚠ **AND IT CAN CARRY A *PRIVATE* CARRIER'S TITLE AS THE COURSE NAME** — `COM2713` reads *"Writing for Strategic Communication"* (batch 222), `CNT3112` reads *"Advanced Network Administration"* (batch 226) and `GRA4882C` reads *"Analysis of Trends and Styles"* (batch 227) — **the statewide title, which in Florida only a PRIVATE institution actually uses.** ⚠⚠ **THREE instances now; treat it as expected rather than notable, and tell the reader to register by NUMBER.** ⚠ **`GRA2508` adds the mirror case: the BARE form is private-only while the `C` form is the public one** (the `PET3344` shape inverted) — **so check the sector of every carrier before describing a bare/`C` pair.** |
| **⚠ FSU entry vs requirement text** | `registrar.fsu.edu/bulletin/...` | ⚠ A number followed by a period is **not** enough to locate a catalog entry — it also matches requirement prose (*"a grade of C or higher in COP 3014 or COP 3363."*). **Verify that a TITLE and a parenthesised credit value follow** (`COP 3014. Algorithm… (3).`). Cost a wrong result in batch 176. ⚠⚠ **AND THE IDENTIFIER MAY NOT BE CONTIGUOUS IN THE HTML (batch 223):** FSU splits it across tags — `<strong>INR </strong><strong>4124. </strong>` — **so a grep for `INR 4124` finds nothing although the entry is there.** **Strip tags and collapse whitespace BEFORE searching.** |
| **FSCJ** | Coursedog — `scratchpad/coursedog.py fscj` (school `fscj_peoplesoft`, catalog `sGHd4uJQXFdgDUaffhTv`) | ✅ **SOLVED 2026-09-07 (batch 173).** Was "platform unidentified". ⚠ **22,693 courses — the largest Florida catalog found so far**, and `fetch()` caps at limit=5000, so a single call silently returns a PARTIAL result. **Page it** (`scratchpad/fscj_dump.py`) and cache to `scratchpad/fscj_courses.json`. |
| **NWFSC** | Coursedog — `scratchpad/coursedog.py nwfsc` (school `nwfsc_banner_sql`, catalog `DGLrTHoh5uNIMFsdbzWf`) | ✅ **NEW 2026-09-07 (batch 173).** 1,781 courses, single page, cached in `scratchpad/nwfsc_courses.json`. Full descriptions and credits. Found because a 404 from `catalog.nwfsc.edu` returned a 1.1 MB body — **the body size was the tell.** |
| **Florida Polytechnic (FLPOLY)** | `catalog.floridapoly.edu` — acalog (Modern Campus) | ⚠ **CONTENT-BLOCKED, probed 2026-09-16 (batch 226).** Root 200 (63 KB), **55 acalog references**, `content.php` empty 202. ⚠⚠ **Florida's newest public university and exclusively STEM** — engineering and computing only — **so it will recur as a carrier across the computing and engineering prefixes, and it is unreadable.** Carrier of `CNT3004C` and `CNT4526`. |
| **St. Johns River State (SJRSC)** | `catalog.sjrstate.edu` — acalog (Modern Campus) | ⚠ **CONTENT-BLOCKED, probed 2026-09-15 (batch 220).** Root answers 200 (49 KB) and the markup carries 33 acalog references and 21 `content.php` links; a `content.php` probe returns an **empty 202**. ✅ **The batch-215 presumption held exactly — identifying the platform answered it in TWO requests instead of a probing session.** Carrier of `CCJ3691`, so that guide names the gap. |
| **Santa Fe** | `catalog.sfcollege.edu` | ⚠ **PLATFORM IDENTIFIED 2026-09-15 (batch 214): acalog (Modern Campus), and CONTENT-BLOCKED.** Root answers 200 (30 KB) but `content.php` and `search_advanced.php` both return **empty 202s** — the same pattern as FSW, TSC, CF and Polk State. Not Coursedog. **Root-reachable, content-blocked; treat as unavailable rather than unidentified.** |
| **UCF (confirmed route)** | Kuali — `ucf.kuali.co` | ✅✅ **RE-CONFIRMED 2026-09-15 (batch 214).** `/api/v1/catalog/public/catalogs/` → pick by `_id` (2026-27 undergraduate = `688b8960ddeb091644d2b1ca`) → `/api/v1/catalog/courses/<catalogId>` (3,676 courses) → detail at `/api/v1/catalog/course/<catalogId>/<pid>`. ⚠ **The detail endpoint needs `pid`, not `id`.** ⚠⚠ **It is the ONLY Florida source reporting laboratory hours as a structured field (`labStudioFieldWorkHours`)** — which settled whether `BOT4850` has a lab. Go here whenever a lab component is in doubt. |
| **CF (Central Florida)** | `catalog.cf.edu` | ⚠ Root 200 (26 KB), **acalog** — so likely the same content-blocked pattern as FSW and TSC. Not exercised. |
| **MDC** | `mdc.curricunet.com/catalog/iq/3279` | ⚠ CurricUNET; 200 but ~10 KB (SPA shell). Lead, not a route. |
| **State colleges (standing retry list)** | SPC, HCC, PESC, PHSC, Palm Beach State, Chipola | ❌ **curl 000 / 404.** With TSC, FSW and **Polk State** content-blocked and MDC an SPA, **this is what still blocks `MUG2101`.** ⚠ **Corrected 2026-09-15:** this row previously read "PSC", which is **Polk State's** code — Polk State is content-blocked rather than unreachable and now has its own row above. The school meant here is **Pensacola State (`PESC`)**. |
| **Coursedog in Florida** | bootstrap endpoint, then `scratchpad/coursedog.py` | ✅ **REOPENED 2026-09-07 (batch 173) — the earlier "only FIU" conclusion was WRONG.** Three Florida Coursedog schools are now known: **FIU**, **NWFSC** and **FSCJ**. The earlier sweep missed them because it tested a guessed host list rather than the hosts the register already recorded as answering. ⚠ **Re-sweep the bootstrap endpoint against any host that answers before recording it as an unknown platform.** |

### ⚠⚠⚠ A "CLOSED" REGISTER ENTRY GOES STALE — re-probe before trusting a negative (batch 228)

**The register is full of confident negatives, and at least one was wrong by the time it was
being relied on.** `catalog.fau.edu` was recorded in batch 173 as a registered host with **no
catalog attached**, ending *"Stop attempting FAU via Coursedog."* ⚠⚠ **In batch 228 the same
one-line bootstrap returned `fau_banner_ethos` and a live catalog id, and a full dump produced
7,127 courses.** The institution attached a catalog in the interval.

⚠ **The distinction that matters: a negative about a SERVER'S CONFIGURATION is perishable; a
negative about a PLATFORM'S BEHAVIOUR is not.** "acalog blocks `content.php`" is a property of the
platform and holds. "This host has no catalog attached" is a property of one institution's setup on
one day and can change without notice.

**Standing practice:**

- **Re-run `coursedog.py discover` on any host recorded as unattached** before writing a guide that
  names it as unreachable. It is one request.
- ⚠ **Do the same for the SmartCatalogIQ and CourseLeaf leads recorded as "not yet exercised"** —
  batch 228 exercised the IRSC one and it worked (below).
- **When a negative turns out to be stale, replace the row and say when it changed**, rather than
  softening it — the next session needs to know the entry is now positive, not hedged.

### ⚠ How to probe a block correctly (learned batch 164)

**Probe a prefix the school definitely carries, not the prefix you happen to want.** A `404 with a full
body` means the server is answering you and simply lacks that prefix; **an empty `202` means it is not.**
Broward and Valencia looked blocked on a `mug` probe (404) until a `psy` probe returned 200 — the 404 was
the recovery signal, not a failure. **Both had been assumed blocked for two days on this misreading.**

### The block-recovery drill

1. **Keep two or three per-school queues built ahead**, not one.
2. When a catalog returns an empty 202 / 403 / captcha: **do not retry in a loop.** Record it in the
   register above with the date, switch to another school's queue, and move on.
3. **Re-probe blocked sources at the start of each session** — these blocks have proven temporary before.
4. If every named school is blocked, fall back to a prefix at a school that still answers rather than
   stalling the batch.

### ⚠⚠ Scale reality: "complete UWF" is bigger than the queue suggests

The master queue is a **prioritised subset** (courses at ≥2 institutions), not a school's full offering:

| | Courses UWF offers | Done | **Workable** |
|---|---|---|---|
| UWF | 1,885 | 310 | **1,575** |

The 805 rows currently in the master are a *subset* of those 1,575. **`queue_UWF.csv` holds the real
figure.** Same applies to every school: UNF 1,839 workable, FGCU 1,570, UCF 3,872.

**Implication for sequencing:** finishing a school means ~1,500–1,800 guides, not a few hundred. Ron's
smaller-schools-first ordering is the right call for exactly that reason — and the state colleges are much
further along already (MDC 31.5% done, BC 33.5%, SPC 32.3%) because the earlier DSC-era work covered
high-enrolment shared courses.

## ⚠⚠ Florida-wide requirements that affect guides (found 2026-09-08, batch 178)

### The Gordon Rule

**State Board of Education Rule 6A-10.030.** Florida public institutions require designated
**writing-intensive** coursework plus designated **mathematics** coursework for an associate or
baccalaureate degree.

- ⚠⚠ **A grade of C or higher is required for a Gordon Rule course to count. A C-minus does not satisfy
  it at most institutions** — stricter than the ordinary passing standard, and a common and expensive trap.
- ⚠ **The designation is made by the INSTITUTION, not by the course number.** The same number can be
  designated at one Florida institution and not another.
- Designation normally travels within the Florida public system but should be confirmed, especially from
  private or out-of-state institutions.

**Standing practice: guides for 1000- and 2000-level general-education courses — composition, humanities,
mathematics — should check for and mention Gordon Rule status.**

#### ⚠⚠⚠ It is MACHINE-READABLE — look it up, do not infer it (batch 201)

**The SCNS flat file carries per-institution designation flags for every course**, and they have been in
`scns.FIELDS` since the flat file landed:

| Field | Byte offset | Meaning |
|---|---|---|
| `gordon_rule` | 226 | Gordon Rule designated |
| `gordon_writing` | 227 | the **writing** half |
| `ge_com` / `ge_hum` / `ge_math` / `ge_nat_sci` / `ge_soc_sci` | 228–232 | general-education category |

⚠⚠ **`HIS2050` is the worked example and the first data-sourced proof of the institution-specific
rule:**

| Institution | Its title | Flags |
|---|---|---|
| FAU | Writing History | `gordon_rule`, `gordon_writing`, `ge_com` |
| FSU | The Historian's Craft | `gordon_rule`, `gordon_writing` |
| UWF | Explore History | ⚠⚠ **`ge_soc_sci` only — NO Gordon Rule** |

⚠⚠⚠ **Same number, same level, same credits, same research-writing course — and it
satisfies the WRITING requirement at two institutions and a SOCIAL SCIENCE requirement at the third.**
**State it per institution in `offering_notes`, and put the consequence in the prerequisite field**: a
student using the course to clear a requirement it is not designated for at their own institution has not
cleared it.

#### ⚠⚠⚠ The two Gordon Rule flags are populated INDEPENDENTLY and INCONSISTENTLY (corrected batch 206)

**Batch 202 read `gordon_rule` appearing WITHOUT `gordon_writing` as pointing at the MATHEMATICS half.
⚠⚠ `REL1300` refutes that**, because it shows all three combinations on one number:

| Carrier | Gordon Rule flags |
|---|---|
| Indian River State | `gordon_rule` **and** `gordon_writing` |
| Florida State | ⚠⚠ **`gordon_writing` WITHOUT `gordon_rule`** |
| UWF | none |

**The middle row cannot be reconciled with the batch-202 reading** — a course cannot be the writing half
without being Gordon Rule designated at all. **The flags are two independent institution-entered fields,
not a two-bit code.**

#### ⚠⚠⚠ HOW OFTEN AN INSTITUTION DESIGNATES VARIES BY A FACTOR OF THIRTEEN (batch 231)

**The rule above says designation is institution-specific. `PHI` quantifies it, and the spread is far
wider than "varies" suggests.** One `Counter` over the prefix — 464 public undergraduate rows, 132
designated, 28% overall:

| Institution | Designated | | Institution | Designated |
|---|---|---|---|---|
| **IRSC** | **11/12 — 92%** | | FAU | 8/44 — 18% |
| **GCSC** | 6/8 — 75% | | UNF | 4/39 — 10% |
| **UWF** | 14/24 — 58% | | UCF | 6/68 — 9% |
| **USF** | 10/20 — 50% | | FIU | 3/40 — 7.5% |
| FGCU | 5/17 — 29% | | **FSU** | **2/29 — 7%** |

⚠⚠ **So the Gordon Rule designation is INSTITUTIONAL POLICY showing through, not a property of any
course.** All four `PHI` courses in batch 231 had **exactly one of their two carriers** designating
them — four for four — which looks like four findings and is one.

⚠⚠⚠ **This is the batch-230 pattern rule applied to DESIGNATIONS: before writing a designation
difference up per-course, count the institution's whole prefix.** Otherwise one policy is reported as
N separate divergences.

⚠ **But the rate predicts the TENDENCY, not the course — and `PHI3200` is the counter-case.** UWF
designates 58% of its philosophy courses and FGCU 29%, **yet on that number it is FGCU that designates
and UWF that does not.** **So never infer an individual course's designation from the institution's
habit; look it up, and tell the student to check their own list.**

✅ **A validation worth recording: the flat-file flags matched the catalogue 4 for 4.** UWF's PDF
carries *"Meets College-Level Communication Skills Requirement"* on exactly the three courses the flat
file flags and not on the fourth. **The batch-179 label rule and the flag data corroborate each other
independently, which is good reason to trust both.**

⚠⚠ **So the honest statement a guide should make: the flags reliably tell you that SOME designation is
recorded; they are NOT a safe guide to WHICH.** **Write "a designation is recorded — check your
institution's list for which component it satisfies" rather than inferring the component.** Four numbers
now show the divergence — `HIS2050`, `PHI4300`, `REL1300`, `REL3241`, across four disciplines — so the
institution-specific rule itself needs no further evidence; only the flag *interpretation* was wrong.

⚠ **Do not display a flag by the first letter of its key** — `gordon_rule`, `gordon_writing` and
all five `ge_*` keys begin with `g`, so a `k[0]` rendering makes them indistinguishable. Print the names.

⚠⚠⚠ **And do not test a flag for truthiness — the values are `'Y'`/`'N'` STRINGS, so `'N'` is TRUE in
Python** (batch 207):

```python
flags = [k for k in FLAG_KEYS if r.get(k)]          # ⚠⚠ WRONG — every row reads as fully designated
flags = [k for k in FLAG_KEYS if r.get(k) == 'Y']   # ✅ correct
```

**The wrong version does not error. It reports every course as carrying every designation**, confidently
and uniformly, and that goes into a guide as a false statement about the Gordon Rule. It was caught in
batch 207 only because all-seven-flags-on-every-row is implausible on its face.

⚠ **Standing check: when a flag scan returns the SAME answer for every row, assume the TEST is wrong
before assuming the DATA is uniform.**

⚠ A back-catalogue sweep is now a one-parse report rather than an open-ended task — see
`REVIEW_QUEUE.md` item 80.

⚠⚠ **UWF's catalog labels ARE Gordon Rule designations** (identified batch 179):

| UWF label | Gordon Rule component |
|---|---|
| *"Meets College-Level **Communication** Skills Requirement"* | the **writing** half |
| *"Meets College-Level **Computation** Skills Requirement"* | the **mathematics** half |

**Whenever a UWF entry carries either label, say what it is AND state the C-or-higher condition.**
⚠ Roughly a dozen already-published guides record the label without the explanation — they are
incomplete rather than wrong. A retro-sweep is a `REVIEW_QUEUE.md` candidate. It surfaced first in FSCJ's Coursedog
entry for `PHI2603`; **CourseLeaf PDFs do not carry it.**

### ⚠⚠⚠ "(GE CORE)" in the statewide TITLE — the strongest transfer fact available (batch 202)

**`CHM1020`'s statewide title is `GENERAL CHEMISTRY FOR LIBERAL STUDIES I (GE CORE)`.** ⚠⚠ **That
marker identifies a Florida General Education Core course** (s. 1007.25, F.S. — a limited approved list
across five subject areas: communication, mathematics, social sciences, humanities, natural sciences).

⚠⚠ **A core course satisfies its general-education AREA at every Florida public college and
university, and carries that status in transfer** — materially stronger than the ordinary *"guaranteed
transfer to institution offering same course"* boilerplate, which only promises credit where the same course
is offered.

- **Lead with it** where a course carries the marker. For a general-education course it is the single most
  useful fact in the guide, and no student-facing source states it plainly.
- ⚠ **The protection attaches to the AREA, not to a laboratory component or to any institutional
  designation.** Whether a programme's "science with laboratory" requirement is met is a programme rule.
- ⚠⚠ **GE Core area status is reliable; Gordon Rule and general-education CATEGORY designations
  remain institutional.** On `CHM1020`'s 27 carriers: 24 record a natural-science designation, 2 add a
  Gordon Rule designation, 1 records none.

### ⚠⚠ Two more statewide fields that are NOT boilerplate — read them (batch 202)

**`DS_Transferable1` — transferability.** Almost every course reads *"guaranteed transfer to institution
offering same course."* ⚠⚠ **`CHM1024` Chemistry Study Skills reads "NOT AUTOMATICALLY
TRANSFERABLE"** — a deliberate classification of support and study-skills coursework, not an omission.
**Where it appears, the guide must say: do not count the credit toward a requirement at another institution,
and ask an adviser how it counts toward degree progress, financial-aid satisfactory academic progress and
Florida excess hours.** ⚠ **Read the field rather than assuming the boilerplate.**

⚠⚠⚠ **AND IN SOME PREFIXES IT IS A COHERENT CLUSTER, not scattered exceptions (batch 225).**
**`PET` has 13 NOT-AUTOMATICALLY-TRANSFERABLE rows among 122 active undergraduate numbers — about
11%, against 2/171 in `CCJ` and 5/124 in `INR`.** ⚠⚠ **And they group:** athletic training clinical
courses (`PET4672`, `PET4673`, `PET4624`, `PET4625`, `PET4627`), exercise testing and fitness
assessment (`PET4550`, `PET4551`, `PET3385`), and `PET4765`.

⚠ **That is the batch-215 licensed-profession logic surfacing in the transferability field:
hands-on clinical and assessment coursework where a receiving programme must attest to competence
ITSELF and cannot do so on another institution's credit.** **Where the stratified count is well above
the ~2% norm, look for the cluster before calling it noise — and tell the reader which KIND of course
is affected rather than listing numbers.**

⚠⚠⚠ **Strengthened (batch 204): it is NOT a support-coursework flag.** `CHM1024` was a
1-credit study-skills corequisite, where the classification explained itself. **`PET4765` Theory and Methods
of Coaching Sports is a substantive 4000-level theory course and carries the same classification.**
⚠ **So the field must be read on EVERY course.**

⚠⚠ **And `PET4765` suggests a useful reading of what it can mean: the three carriers teach
genuinely different courses** — USF *Scientific Principles of Athletic Coaching*, UWF *Theory and
Practice of Coaching*, FSU *Principles and Problems of Coaching*. **A statewide guarantee would assert an
equivalence that does not hold, so the classification looks like a deliberate acknowledgement of divergence
rather than an oversight.** ⚠ **Where you meet it, check whether the titles diverge too — if they
do, say so in the guide and tell the reader to get a written answer from the receiving department BEFORE
taking the course.**

**`hs_credit` — dual-enrolment high-school credit.** The flat file records what a dual-enrolled
high-school student earns, and it differs within a family:

| Number | `hs_credit` |
|---|---|
| `CHM1020` | ⚠ **ELECTIVE** |
| `CHM1025` / `CHM1032` | **SCIENCE** |

⚠⚠ **So a dual-enrolled student taking `CHM1020` for a high-school SCIENCE requirement may receive
elective credit instead.** The college credit is unaffected; the high-school requirement may not be met.
**State it in guides for dual-enrolment-eligible courses, with "confirm with your counsellor and district
articulation agreement."** ⚠ **Nothing a student or parent normally reads says this.**

#### ⚠⚠⚠ STRATIFY BY THE POPULATION THE FIELD APPLIES TO — and get the FINDING from SIBLINGS (batch 227)

**Two refinements to the distribution test below, both from `GRA`'s `hs_credit`.**

⚠⚠ **1. Stratify by the population the FIELD applies to, not by course level generically.** Over all
public undergraduate `GRA` rows the split is **46 FINE ARTS / 462 ELECTIVE (9%)** — which by the
batch-225 threshold reads "near-universal with exceptions" and would have been dropped. **But
high-school credit only applies to DUAL ENROLMENT, which is a LOWER-DIVISION phenomenon**, and
restricted to levels 1-2 the split is **43/267 (14%)**, with **17 of the 20 FINE ARTS numbers
lower-division**. ⚠ **The batch-225 rule said stratify by LEVEL; the correct general form is
stratify by WHO THE FIELD CAN POSSIBLY APPLY TO.**

⚠⚠⚠ **2. The distribution test only tells you whether to LOOK. The FINDING comes from comparing
SIBLINGS AT ONE INSTITUTION.** Even at 14% the prefix distribution is not something to put in a
guide. **What is worth stating is this: UWF carries `GRA2111C` (FINE ARTS) and `GRA2508C`
(ELECTIVE) — two adjacent required foundation courses in the SAME programme, returning DIFFERENT
high-school credit.** A dual-enrolled student filling a fine-arts requirement gets it from one and
not the other, and nothing they read says so.

⚠ **This is the batch-225 "read one institution's entries against each other" rule applied to a
METADATA FIELD rather than to descriptions — and it works the same way.** **Run the distribution
test to decide whether the field is live; then run the sibling comparison to find what to say.**

#### ⚠⚠⚠ COMPUTE THE FIELD'S DISTRIBUTION ACROSS THE PREFIX BEFORE TREATING IT AS A SIGNAL (batch 207)

**The same statewide field is boilerplate in one prefix and evidence in another.** Batch 207 measured it:

| Prefix | `DS_High_School_Credit1` across ACTIVE numbers | Verdict |
|---|---|---|
| `SPM` | ⚠ **184 of 184 ELECTIVE** | pure boilerplate — carries **no** information |
| `SPN` | ✅ **24 FOREIGN LANGUAGE, 178 ELECTIVE** | genuinely **discriminating** |

⚠⚠ **In `SPN` the field produced the batch's most consequential student-facing finding.** `SPN2210`
carries **ELECTIVE** while its three near-neighbours `SPN2200`, `SPN2220` and `SPN2240` — all covering
approximately the same second-year Spanish — carry **FOREIGN LANGUAGE**. ⚠⚠⚠ **Florida graduation
requirements, Bright Futures and SUS admission all expect two sequential credits in ONE world language**,
so a dual-enrolled student choosing the wrong number of four equivalent ones may not get the credit they
enrolled for.

**The rule: one `collections.Counter` over the prefix decides whether a field is worth writing about.**
A field that is uniform is a prefix-level default; a field that splits is evidence. ⚠⚠ **But the
split has to be SUBSTANTIAL — see the threshold note below; "more than one value" is not the test.** The same test disposed
of `IN_Dual_Enrollment1` in batch 207 — `Y` on 184/184 SPM and 202/202 SPN rows, therefore meaningless.

⚠ **Say which it is in the guide.** "SCNS marks this available for dual enrolment with elective high-school
credit — and every active number in the prefix carries the identical marking, so it says nothing about this
course" is honest and useful. Presenting boilerplate as a finding is not.

##### ⚠⚠ The split must be SUBSTANTIAL — a lopsided one is "near-universal with exceptions" (batch 221)

**`survey.py` calls a field *discriminating* as soon as it sees more than one value, and that is too weak a
test.** In `PLA` it reported `dual_enrollment` as discriminating; stratified to active undergraduate rows it
is **155 `Y` / 9 `N` — 94% to 6%.**

| Field | Split | Verdict |
|---|---|---|
| `SPN` `hs_credit` | 24 / 178 | ✅ **genuinely discriminating** — produced that batch's best finding |
| `CCJ` transferable (undergrad) | 2 / 169 | ⚠ near-universal |
| `PLA` dual enrolment (undergrad) | 9 / 155 | ⚠ near-universal |

⚠ **A lopsided split means "near-universal, with exceptions worth listing SEPARATELY" — write the default
as a default, and capture the handful of exceptions as their own note.** **Presenting a 94/6 field as a
finding is the same error the uniform case was meant to prevent.**

##### ⚠⚠⚠ STRATIFY THE DISTRIBUTION BY COURSE LEVEL, or the test reports an ARTEFACT (batch 220)

**The `Counter` above is run over ACTIVE rows. That is not the same population as the rows you WRITE
about, and in `CCJ` the difference inverted the answer.**

`DS_Transferable1` over all **356 active** `CCJ` rows: **186 NOT AUTOMATICALLY TRANSFERABLE / 170
guaranteed** — a near 50/50 split, which by the test above reads as **strongly discriminating**, in a
prefix where the batch-202/204 rule already says to read that field on every course. **It nearly became
four guides' headline finding.**

**Cross-tabulated against `DS_Course_Intent1` it collapses:**

| Intent | GUARANTEED | NOT-AUTO |
|---|---|---|
| LOWER | 50 | 0 |
| UPPER | **119** | 2 |
| ⚠ GRADUATE | 0 | **130** |
| ⚠ VARIABLE | 0 | **54** |

⚠⚠⚠ **Of 171 active UNDERGRADUATE rows, 169 are guaranteed.** The whole split is graduate and
variable-credit rows, which are non-transferable as a class. **For the courses this project writes, the
field is boilerplate.**

**The rule, and it applies to EVERY field the distribution test is run on:**

```python
rows = [r for r in active if r['DS_Course_Intent1'] in ('LOWER', 'UPPER')]   # then Counter
```

⚠⚠ **Run the distribution over the population you are writing about — active, undergraduate,
non-shell — not over every active row.** One filter is the entire cost, and it is the difference between
a finding and an artefact. ⚠ **Keep the genuine exceptions the stratified pass surfaces**: in `CCJ` only
**`CCJ4615`** and **`CCJ4662`** are undergraduate and non-transferable, and those two DO deserve the
batch-204 treatment.

### ⚠⚠⚠ TITLE FRAGMENTATION AT SCALE — when many titles mean NO divergence (batch 202)

**`CHM1020`: 27 public carriers, 18 distinct titles**, none used by more than four — Chemistry in
Society, Chemistry in Everyday Life, Concepts in Chemistry, Discovering Chemistry, Chemical Science, General
Education Chemistry, Chemistry for the Liberal Arts, and eleven more.

⚠⚠ **And the subject does not diverge at all.** Every title names the same one-term non-majors
general-education chemistry course. **This is the opposite of every shape above, and it needs opposite
handling: REASSURE rather than warn.** The guide says so directly — *"if your catalog calls it something
this guide does not mention, it is still this course."*

⚠ **The diagnostic:** on a **high-carrier general-education** number, many titles are **branding**, not
curriculum — 27 institutions each naming the same required course. ⚠⚠ **Do not read title
variation as a divergence signal without checking the statewide DESCRIPTION and the carrier count.** The
signal is strong on a two- or three-carrier upper-division number and weak on a twenty-carrier
general-education one.

### ⚠⚠⚠ NUMBER FRAGMENTATION AT SCALE — the inverse shape (batch 207)

**Title fragmentation is one number carrying many titles. This is one SUBJECT carrying many numbers**, and
the risk it creates is the opposite one: not that a number means two things, but that **the course a
student needs exists under a number their institution does not use.**

**Second-year Spanish runs under FOUR competing statewide families**, all covering approximately the same
ground:

| Family | Statewide title | Public carriers | Credits | HS credit |
|---|---|---|---|---|
| `SPN2200`/`2201` | Intermediate Level: General Review of Basic Skills | **15** | 3 | ✅ Foreign language |
| `SPN2220`/`2221` | Intermediate Reading and Conversation | **14** | 4 | ✅ Foreign language |
| `SPN2240`/`2241` | Intermediate Conversation | **10** | 3 | ✅ Foreign language |
| ⚠ `SPN2210`/`2211` | Intermediate Conversation and Composition | ⚠ **3** | ⚠ **3 or 4** | ⚠⚠ **Elective** |

⚠⚠ **The statewide description of `SPN2210` says the series *"is equivalent to"* the `SPN2200` series — so
it is an ALTERNATIVE ROUTE through the same level, not a course that follows it.** **A student taking both
families may not earn credit for both**, and that surfaces at transfer evaluation, late and expensively.
**Where a statewide description says a series is equivalent to another series, say so in the guide and tell
the reader to ask an adviser before enrolling in the second.**

⚠ **Quantify the prefix before writing — it sets the hedging level honestly rather than by feel.**

#### ⚠⚠⚠ THE SINGLE-CARRIER BASELINE — a measured property of the Florida catalog (batches 207-210)

**Thirteen prefixes measured across four batches. Every one lands between 64% and 85%:**

| Prefix | Live ids | Single-carrier | Prefix | Live ids | Single-carrier |
|---|---|---|---|---|---|
| `SPM` | 189 | 145 (77%) | `TPA` | 414 | 324 (78%) |
| `SPN` | 241 | 166 (69%) | `TRA` | 79 | 62 (78%) |
| `SSE` | 145 | 123 (85%) | `ACG` | 346 | 227 (66%) |
| `SYO` | 124 | 97 (78%) | `ADV` | 133 | 109 (82%) |
| `SYP` | 165 | 140 (85%) | `AFR` | 76 | 49 (64%) |
| `AMH` | 330 | 240 (73%) | `APK` | 238 | 183 (77%) |
| `ARH` | **421** | 339 (81%) | ⚠⚠ **`COM`** | **370** | **308 (83%)** |
| `CCJ` | 486 | 311 (64%) | `PLA` | 286 | 190 (66%) |

⚠⚠ **Sixteen prefixes measured as of batch 222. `CCJ` (64%) and `PLA` (66%) are the lowest — both
have large lower-division state-college populations — and ⚠⚠ **`COM` at 83% across 370 ids is the
highest on a LARGE prefix**, so a communication course transferring cleanly by number is close to an
exception.

⚠⚠⚠ **Roughly three-quarters of all Florida course identifiers are carried by exactly ONE public
institution.** **So a course transferring cleanly by number is the EXCEPTION across the catalog, not a
feature of unlucky prefixes** — and the honest default hedging level for almost any course is higher than
"two or three institutions agree" suggests.

**Two consequences for writing:**

1. **Do not treat a two- or three-carrier course as unusual.** It is the norm. Write the
   single-institution or few-institution treatment without apology, and say plainly that the reader
   should plan on sending syllabi rather than relying on the number.
2. ⚠ **The baseline coexists with a small number of very widely carried courses** — `ACG` reaches 37
   carriers, `AMH` 36, `ARH` and `SPN` around 30, all on lower-division general-education numbers.
   **Those are the ones where title variation is branding rather than divergence** (see TITLE
   FRAGMENTATION AT SCALE). **Check the carrier count before deciding which kind of course you are
   writing.**

**It is one flat-file pass to compute, and it is worth doing before drafting.**

### ⚠⚠⚠ TITLE-versus-DESCRIPTION divergence — inside ONE statewide record (batch 207)

**Every other divergence in this file runs between two records** — institution against institution, or
institution against the statewide title. ⚠⚠ **This one is internal: the state's own title and the state's
own description contradict each other.**

| `SPM3104` statewide title | `SPM3104` statewide description |
|---|---|
| SPORT FACILITY **AND EVENT** MANAGEMENT | *"planning, design, and management &hellip; maintenance, security, operations, and evaluation"* — ⚠ **events never mentioned** |

**The institutions side with the description:** EFSC *Sports Facilities Management* and UWF *Sport Facility
Planning and Management* both drop "event"; UNF's "Entertainment" names a venue type, not the discipline.
⚠⚠⚠ **And the missing half is not housed elsewhere — `SPM4109` *Sport Event Management* and `SPM4140`
*Esports Event Management* have NO Florida public carrier at all.**

**The consequence is a real student-facing finding, not a cataloguing curiosity: event operations is the
least reliably covered part of the subject the degree title implies, and it is where a large share of
graduates actually start work.** The guide says so and tells the reader to close the gap deliberately.

⚠ **The drill: when a statewide title contains a conjunction ("X and Y"), check that the statewide
DESCRIPTION delivers both halves, and check whether Y has its own number that nobody carries.**

⚠⚠ **AND RECORD IT WHEN THE TEST PASSES (batch 230).** Every instance above is a failure, which
makes the test look like a detector for a defect. **`FIL4102` is the clean case: the statewide title
promises *"Screenwriting AND Storyboarding"*, the sole carrier's TITLE drops storyboarding — and its
DESCRIPTION delivers it** (*"script formats, storyboarding, and story pitches"*). **A title that names
only the larger half is not a missing half.** ⚠ **Check the description before writing a gap warning,
and say so in the guide when both halves are there** — that is a reassurance a student can use.

##### ⚠⚠ SECOND INSTANCE, with a twist: the missing half's number is GRADUATE (batch 223)

**`INR4061`** — statewide title *Conflict, Security **and Peace Studies** in INR*, and here the
statewide **description** delivers both halves (it promises *"conflict resolution and post-conflict
reconstruction"*). ⚠ **Both carriers deliver only the conflict half**: UWF the bargaining model of
war, FGCU *International Armed Conflicts*.

**Running the drill on the missing half:**

| Number | Title | Level | Carriers |
|---|---|---|---|
| **`INR4062`** | War, Peace and Conflict Resolution in INR | ⚠ **graduate** | ⚠⚠ **none** |

⚠⚠⚠ **So the missing half is separately numbered, classified GRADUATE, and carried by nobody —
meaning the subject has no undergraduate home in the prefix at all.** **That is a stronger and more
useful finding than `SPM3104`'s, where the missing numbers were merely uncarried.**

⚠ **Handling: say it plainly and send the reader OUT OF THE PREFIX.** Conflict resolution and
mediation are routinely taught under communication, sociology, criminal justice and psychology.
**"The subject exists; it is just not reliably here" is an answer a student can act on; a divergence
warning is not.**

#### ⚠⚠⚠ Check whether the carriers diverge in the SAME direction or OPPOSITE ones (batch 210)

**Before writing a single divergence block, ask which way each carrier departs from the statewide scope.
The two cases need completely different handling.**

| | Carriers diverge the SAME way | Carriers diverge OPPOSITE ways |
|---|---|---|
| Example | **`SPN4520`** — state says *Spanish America*, all three carriers say *Latin American* | **`ARH3301`** — state says Renaissance **+ Mannerism**, Italy **+ North**; ⚠ FGCU adds the **Baroque** (broader), ⚠ UWF restricts to the **Early** Renaissance (narrower) |
| What it means | ⚠ **the STATE record is out of step** with current practice | ⚠ **the carriers are making independent curricular choices** |
| Handling | correct toward the carriers; explain the state's term | ⚠⚠ **give the reader a TEST, not a correction** — neither carrier is wrong |

⚠⚠⚠ **The opposite-direction case has a consequence worth stating explicitly in the guide: with only two
carriers diverging in opposite directions, the two versions may overlap only in the MIDDLE of the
subject.** On `ARH3301` one adds a century at the end and the other may stop before the High Renaissance —
so a student could take either and miss what most people mean by the course's own title.

**Handling that works: two concrete syllabus questions rather than a general warning.** For `ARH3301`:
*does it reach the High Renaissance and Mannerism?* and *does it cover Northern Europe, or Italy only?*
⚠ The second matters because **the statewide description requires both halves and a course titled simply
"Renaissance Art" frequently means Italian Renaissance art** — which Florida numbers separately as
`ARH3302`.

#### ⚠⚠⚠ THE NEGATIVE RESULT: A TITLE DIVERGENCE THAT DISSOLVES — check it BEFORE writing a divergence block (batch 227)

**Every rule in this section is built to detect divergence, which makes them collectively biased
toward finding it. `GRA3881C` is the counterweight, and it nearly produced a published finding that
was the OPPOSITE of the truth.**

| Source | Title | What its DESCRIPTION says |
|---|---|---|
| Statewide | *Semantics of Design* | *"the general field of **semiotics** … aspects linked to **MEANING** in visual communication"* |
| FIU | *Design: Semiotics* | *"**signs, codes**, and cultural **MEANING** in design … **semiotic principles**"* |
| ⚠ UWF | ⚠⚠ ***Comics: Sequential Art and Design*** | *"how **SIGNS, SYMBOLS**, and sequence are used to create **MEANING** in sequential art"* |

⚠⚠⚠ **On the TITLES this is a textbook one-number-two-subjects collision. On the DESCRIPTIONS all
three name the same subject.** **UWF teaches semiotics THROUGH comics — the medium is the vehicle,
not the subject.**

⚠⚠ **So the handling INVERTS: the finding is not a warning, it is a REASSURANCE plus a transfer
action.** The guide says the two courses are the same subject, and tells the student that **an
evaluator comparing those two titles will reasonably conclude otherwise and be wrong** — so send the
syllabus and point at the descriptions. ⚠ **A one-line note from the student prevents a transfer
loss here, and nobody will read past the title unless prompted.**

⚠ **The general rule this sharpens: a divergent TITLE plus an agreeing DESCRIPTION is a
presentation difference, not a curricular one.** **It is the same one-row lookup as the
title/description test below — run it on the CARRIER pair, not only on the statewide record.**

#### ⚠⚠⚠ THE TITLE/DESCRIPTION TEST — run it before looking at carriers (batch 208)

**Batch 208 produced a second and a third instance, and together they turn a judgement call into a test.**
Both fields are in the same statewide CSV row, so this costs nothing:

| Case | Statewide title vs statewide DESCRIPTION | Carriers | Conclusion |
|---|---|---|---|
| **`TPA3223C`** | ✅ **agree** — both say lighting *technology* | 2 of 3 say *design* | ⚠ **the CARRIERS are misfiling** |
| **`TRA3153`** | ❌ **disagree** — title says *"Applied Production/Operations Mgmt"*, description is entirely *transportation* | both agree with the description | ⚠ **the TITLE is stale** |
| **`SPM3104`** | ❌ **disagree** — title promises *events*, description omits them | carriers side with the description | ⚠ **the TITLE is stale** |

⚠⚠ **The rule: compare the statewide title with the statewide DESCRIPTION first.**

- **They AGREE** → the state is the reference, and a deviating carrier is **misfiling**. Write the
  statewide subject, label the misfiling, and check whether a dedicated number exists for what the carrier
  actually teaches (it usually does — see the MISFILING section).
- **They DISAGREE** → the **title is the stale element**, and the description plus the carriers settle it.
  ⚠ **`TRA3153` is the first time this catalog has corrected a statewide title outright**, and it was
  safe because four independent things pointed the same way: the description, both carriers, and the
  prefix itself (`TRA` = transportation; production/operations management is numbered under `MAN`).

⚠ **This REFINES rather than contradicts the batch-201 caution** ("do not correct a *described* statewide
subject on agreeing titles alone"). That caution protects a statewide **description** from being overridden
by titles. **Here the description is not being overridden — it is the evidence**, against a title it
already contradicts.

#### ⚠⚠⚠ CORRECTED (batch 215): when they disagree, THE CARRIERS decide which element is stale

**The rule above said "they DISAGREE → the title is the stale element." That was true of the cases in hand
and is NOT a general property of titles.** `RET4277` is the counterexample:

| Source | Says |
|---|---|
| Statewide **title** | *Adult Critical Care* |
| ⚠ Statewide **description** | a survey of *"the different specialty areas available in respiratory therapy"* — **not critical care** |
| UWF | Critical Care Management — **critical care** |
| Seminole State | Adult Critical Care — **critical care** |

⚠⚠⚠ **Title and description disagree, and BOTH CARRIERS SIDE WITH THE TITLE — so here the DESCRIPTION is
the stale element.** Three of four sources agree against it.

**So the test has three outcomes, not two:**

1. **Title and description AGREE** → the state is the reference; a deviating carrier is **misfiling**
   (`TPA3223C`).
2. **They DISAGREE and the carriers back the description** → the **TITLE** is stale (`TRA3153`, `SPM3104`).
3. ⚠ **They DISAGREE and the carriers back the title** → the **DESCRIPTION** is stale (`RET4277`).
4. ⚠⚠⚠ **They DISAGREE and the CARRIERS SPLIT, one on each side** → **the test returns NO ANSWER, and the
   number is carrying TWO SUBJECTS** (`HFT4252`, batch 218).
5. ⚠⚠⚠ **They AGREE, and the agreed-on wording is TOO VAGUE TO DISCRIMINATE** → **the test again
   returns no answer, and an INTERNALLY CONSISTENT statewide record turns out not to be a usable one**
   (`JOU4306`, batch 224). **Statewide title *Critical Journalism*, statewide description *"critical
   thinking and analysis as employed in the profession of journalism"* — and the two carriers teach
   ARTS CRITICISM (UWF) and DATA JOURNALISM IN R (UF).** ⚠⚠ **Writing a review is critical thinking;
   analysing a dataset is analysis. Both readings fit the state's own words.**

⚠⚠ **Branch 5 is the one to watch for, because branches 1-3 all assume the state's wording PICKS A
SIDE.** **Where it does not, stop trying to adjudicate and write both readings with a test the student
can apply** — for `JOU4306` the prerequisite is the tell: gated on a data course means the data
version, gated on nothing means criticism.

⚠⚠ **Always check which element the CARRIERS agree with before deciding.** Never assume the title is the
stale half just because it usually has been.

#### ⚠⚠⚠ THE MECHANISM BEHIND BRANCH 4, and the tell that reveals it (batch 232)

**On `HFT4252` the title/description contradiction was visible and unexplained. `PHC4140` shows how one
gets made, because the statewide description NAMES ITS OWN AUTHOR.**

| | |
|---|---|
| statewide **TITLE** | *Public Health Planning and Analysis* |
| statewide **DESCRIPTION** | ⚠⚠ entirely **GIS** — *"an introduction to Geographic Information Systems (GIS)… buffering, layering, and spatial queries"* |
| **UWF** | *Public Health Planning and Analysis* — planning, implementation, evaluation, needs assessment. **No GIS.** Backs the **title**. |
| **USF** | *Introduction to Public Health Geographic Information Systems*. Backs the **description**. |

⚠⚠⚠ **The tell: the description ends by calling the course *"a required course in the PROPOSED
public health major in the Bachelor of Science in Health Sciences [BSHS] degree program"* — one
specific institution's degree, described while it was still being proposed.**

**So the likeliest history is that a carrier contributed a description of ITS OWN course onto a number
whose TITLE already belonged to a different subject, and nobody reconciled the two.** That is a
*mechanism*, not just a state of affairs: **the record is internally contradictory because it was
assembled from two sources, not because either half went stale.**

⚠⚠ **The drill: when title and description disagree, read the DESCRIPTION for signs of a single
author** — a named degree programme, a delivery mode (*"this online course"*), a word like
*"proposed"*, or an institution code. **Where you find one, you have identified which carrier the
description belongs to, and the other carrier's reading is what the title preserves.** That converts an
unexplained contradiction into a legible one, and the guide can say so.

⚠ **And check whether the displaced subject had anywhere to go.** Here it did not: Florida provides
**three** upper-division planning numbers (`PHC?140`, `?142`, `?143`) and its only GIS-in-public-health
number, **`PHC?194`, is GRADUATE** — so an undergraduate GIS course had no correct home. **Misfiling by
necessity underneath a branch-4 collision**, and the guide says plainly that there is no right number to
go looking for.

**Branch 4 handling — `HFT4252` is the worked case.** Statewide title *Employees Wellbeing in Hospitality
and Tourism*; statewide description entirely *hotel and resort management*; **UCF backs the title, Pensacola
State backs the description.** ⚠ Both subjects were **numbered elsewhere in the prefix** (`HFT2014`,
`HFT4793` for wellbeing; `HFT2250`, `HFT2276` for hotel/resort), so neither carrier needed this number.
**Published as ONE guide covering BOTH readings, each labelled, with a two-column syllabus diagnostic and
an explicit warning that the course number does not identify the subject** — the `CLP4302`/`APK4200`
precedent. ⚠ **A full split was not sound because one carrier's catalogue is unreachable, and a `-INST`
half cannot be written from a title alone.**

### ⚠⚠⚠ FOUR subjects on one number — pull it, do not write it (batch 218)

**`HFT3271` is the most severe collision found to date and it is the pattern for when to STOP.**

| Source | Subject |
|---|---|
| statewide title **and** description | **Condo/Resort Management** |
| FIU | Nightclub Management |
| FGCU | Club Management |
| UWF | Spa Management |

⚠⚠⚠ **Four subjects, and NO carrier teaches the statewide one.** Writing the statewide subject would
describe a course nobody teaches; writing any carrier's would misdescribe it for the other two.

⚠ **The misfiling diagnostic fires on all three carriers**: Florida numbers spa (`HFT2204`, `HFT2209`),
club (`HFT2100`, `HFT4434`) and condo/resort (`HFT2273`, `HFT2276`, `HFT2278`) **separately**.

**Rule: where a number carries FOUR readings, or where NO carrier teaches the statewide subject, PULL it to
`REVIEW_QUEUE` rather than writing.** Precedents: `TPA3230C` (three subjects, pulled), `HFT3271` (four,
pulled). **A disambiguation page at the bare number is the likely resolution, but that is Ron's call.**

#### ⚠⚠ The same one-row check settles a narrow-looking title (batch 208)

**`SYO4530`**: statewide *Social Stratification*; FIU *Social Inequalities*, UF *Social Inequality*,
UWF ⚠ *Inequality in America*. The instinct is to flag UWF as narrowing. ⚠⚠ **But the statewide
description already says "American society (primarily)" — so UWF's title is simply ACCURATE, and the two
broader-sounding titles are the ones that may promise comparative material the course does not deliver.**

⚠ **Drill: before flagging a narrow title as a narrowing, check whether the DESCRIPTION was already that
narrow.** This inverts the usual reading often enough to be worth the one lookup.

#### ⚠⚠⚠ ON A SINGLE-CARRIER COURSE, STATEWIDE AGREEMENT IS NOT EVIDENCE (batch 227)

**`GRA3887C`: the statewide description and UWF's description are THE SAME TEXT**, apart from one
sentence UWF adds about stop-motion practice.

⚠⚠ **That is not two sources agreeing. It is one source quoted twice** — the statewide entry was
almost certainly contributed by UWF, the only carrier. **Do not relax the single-institution hedging
on the strength of it**, and do not write "the statewide record confirms" when the statewide record
IS the carrier's own text.

⚠ **It does carry one mild POSITIVE signal, and it is worth stating in the guide**: the description
is current and written by people who actually teach the course, which makes it more reliable than the
1980s entries elsewhere in the file (see the PROSE REGISTER rule below). **Say which situation you are
in, rather than letting the reader assume independent corroboration.**

⚠⚠ **Standing check, one lookup: WHENEVER a course has ONE carrier and its description matches the
statewide description closely, assume the carrier wrote it.** The tell is verbatim or
near-verbatim agreement — genuine independent agreement is never word-for-word.

#### ⚠⚠ A statewide description with an embedded institution list or a YEAR is a historical record (batch 208)

**`SSE4113`'s description ends *"INSTITUTIONS: FAMU, FAU, FSU, UWF 1988"*; `SYO4530`'s ends with nine
institutions and *"6/83"*.** In both cases the list no longer matches who offers the course.

⚠⚠ **THE SHORTEST FORM IS A BARE INSTITUTION CODE, and all three targets in batch 229 had one.**
`MUE?423`'s description ends `USF`; `MUE?411`'s and `MUE?344`'s end `FSU`. **No list, no date — just
the contributor.** ⚠ **It is free evidence and costs one look at the last token of the description:
it names the institution whose catalogue to check first** (the batch-200 reverse read).

#### ⚠⚠⚠ AND A CONTRIBUTOR CAN DRIFT AWAY FROM ITS OWN CONTRIBUTION (batch 229)

**`MUE3423`'s statewide description — *"a study of orchestra materials in a laboratory setting,
appropriate to elementary and secondary school music programs"* — ends with the code `USF`. ⚠⚠ **And
the course USF now carries on that number is *String Techniques*, a PLAYING-technique course**, which
Florida numbers separately at `MUE2440` (six public carriers at the same 1 credit). **UWF, not the
contributor, is the carrier that still matches the contributed text.**

⚠⚠⚠ **So a contributor stamp does NOT mean the contributor still teaches what it contributed.**
**Check the contributor's CURRENT offering against the description it supplied** — where they have
parted company, the statewide record has quietly stopped describing anybody at all, and the drift is
invisible from the record alone.

⚠⚠⚠ **PROVED rather than inferred (batch 227): `GRA2508C`'s description ends *"INSTITUTIONS: FAMU
1988"* — and FAMU does NOT carry the number today, while UWF DOES.** **One flat-file lookup turns
this rule from a reasonable suspicion into a demonstrated fact, and it is worth doing** — a guide can
then tell the reader the state record is stale instead of hedging about it.

⚠ **`GRA2508C` also carries an administrative marker INSIDE the statewide title — `COLOR AND COLOR
THEORY(RES 2008)` — appearing on exactly three `GRA` numbers, all stamped the same year.** **Strip
such a marker from the course NAME, say it is administrative, and do NOT guess at what it means.**
(Compare the `ATF` titles, where the parenthesised content is real hour data — **read the title as a
data field, but do not assume every parenthesis carries student-facing information.**)

⚠⚠ **Read those descriptions as a historical definition of the SUBJECT, not a current statement of
practice, and say so in the guide.** **Parts of the state course file have not been revised in forty
years** — which also means the statewide record is sometimes the *least* current source available, and
cannot be used to check a carrier's currency (see `SYP3630` under terminology-era divergence).

#### ⚠⚠ Read the description's PROSE REGISTER — it dates the entry when no date is stamped (batch 210)

**The state course file contains entries from at least two eras, and they are distinguishable by style
alone.** Compare, both in `AMH`:

| Era | Example | Style |
|---|---|---|
| 1980s | `AMH4110` | *"DISCOVERY, EXPLORATION, ORIGINS OF COLONIES. DEMOGRAPHIC TRENDS, ETHNO-CULTURAL CONFLICT…"* — terse all-capitals telegraphese |
| Recent | `AMH4641` | *"This course surveys… **This is no trivial subject.** … In this course, **we'll** examine… **We'll** learn how to critically analyze…"* — full sentences, first person plural, an argument |

⚠⚠ **Where a statewide description reads as though it was written by someone who teaches the course, it
usually was — and it is MORE reliable than the older entries.** That inverts the usual assumption in this
file, where the statewide record has repeatedly been the stale element (`AFR2132`'s *"projects ahead to
the year 2000"*, `ACG4151` dated 11/82, `SSE4113` dated 1988, `SYO4530` dated 1983).

**Practical use: read the register before deciding how much weight to give the description.** A recent,
argued entry can be quoted to the student as a description of the actual course; a 1980s entry should be
framed as a historical definition of the subject. ⚠ **It costs nothing and it is available on every
course.**

### General-education category designations

⚠ **Distinct from the Gordon Rule and separately unreliable in transfer.** A course can transfer as credit
without satisfying the general-education CATEGORY a student expected. Florida's common general-education
core gives substantial protection for A.A. completers, but **category placement is institution-specific**.

### ⚠ Coursedog sources carry metadata CourseLeaf does not

FSCJ, NWFSC and FIU records include **regulatory notes (the Gordon Rule text), structured `requisites`
objects with prerequisite/corequisite rules, college names, and lifecycle status** ("Inactivated per 2024
SCNS review, last offered fall 2016"). **Mine these deliberately rather than only reading `description`.**

## Session start checklist

When starting a fresh session in this project:

1. Read this file (you are here) — it governs guide *content*.
2. Read `Generate_Guides_and_Push_Process.md` for the end-to-end process (it is the
   start-here document), `README.md` for per-tool detail, and `QUEUE_GUIDE.md` for the queue
   schema and priority tiers. `.claude/skills/guide/SKILL.md` at the repo root drives the
   mechanics.
3. ⚠⚠ **Check BOTH public queues first, every session** (Ron's standing order, 2026-09-11:
   *"each session we will check resources and guide queue requests and then start on any courses
   in the queue"*):

   ```bash
   curl -s "https://floridacourserepo.com/api/v1/queue/resources?status=pending"   # resources
   curl -s "https://floridacourserepo.com/api/v1/queue/guides?status=waiting"      # guide requests
   ```

   **Resource suggestions are cleared first** — they are quick, a person is waiting on each one, and
   the rules are in `resources/APPROVAL_RULES.md` (the `/resources` skill drives the loop). **Then
   guide requests**. ⚠⚠⚠ **As of 2026-09-17 requests are the ONLY source of guide work — do NOT fall
   through to `queue.csv`.** And run **`python review_lookup.py --requests`** before writing anything:
   it flags any requested course that already carries a `REVIEW_QUEUE` note.

   ⚠ **A guide request closes itself when the guide publishes** — no manual step. Verify by
   re-reading the queue after a push.

   ⚠⚠⚠ **SHARPENED (batch 228): requests cluster on SPLIT FAMILIES, and the tell is that the
   OTHER half already has a guide.** Both requests received on 2026-09-16 were the **`L` halves**
   of numbers whose **integrated `C` twins were already published** — `BSC1010L` against a live
   `BSC1010C`, `BSC1020L` against a live `BSC1020C`. **The requester found the site's page for the
   packaging their institution does not use, and needed the other one.**

   ⚠⚠ **So a published `C` guide with no `L` guide (or the reverse) is a PREDICTOR of a future
   request, and it is a one-line check**: before closing a batch on a split-family number, look up
   whether the site holds the sibling. **Writing both halves at once costs far less than meeting the
   request later**, and the second guide reuses the whole survey.

   ⚠ **Two requests in a row (`CET1112`, `CET2127C`) landed on numbers with a divergence.** A request
   appears to be a signal that the number confuses people, so **check the number's whole family
   before writing** — the bare/`C` pair, the level twin, and what other institutions call it.
4. ⚠⚠⚠ **CHECK FOR AN EXISTING LIVE GUIDE ON EVERY COURSE IN THE BATCH, not only the
   requested ones** (learned the hard way, batch 202 — `CHM1020C` already had a guide published
   2026-05-04 and was rewritten unknowingly):

   ```bash
   for c in ID1 ID2 ID3; do printf "%-9s " $c; \
     curl -s "https://floridacourserepo.com/api/v1/courses/$c/guide" | head -c 120; echo; done
   ```

   ⚠ **A request's `hasGuide: false` covers only that course.** When a batch is extended into a
   number's family — which the "check the whole family" drill encourages — **the added members have
   not been checked.** If a guide exists, decide deliberately whether to replace it (bump `version`, and
   see `REVIEW_QUEUE.md` item 81) or to skip the number.

   ⚠⚠ **And read `mkguide.py`'s PER-COURSE output, treating a missing line as a failure.**
   `validate_drafts.py` validates **what is on disk, not what you just built** — so a failed assembly
   plus an older draft file produces a clean validation of the *wrong file*. That is exactly how the
   batch-202 miss stayed invisible: five new drafts and one stale one reported as "6 clean".

5. Run `python queue_mgr.py status` to see where things stand. `queue.csv` is the
   authoritative work queue; for prefix completion the live catalog is now the better worklist:
   `curl -s "https://floridacourserepo.com/api/v1/courses/catalog?prefix=<PFX>&hasGuide=false&pageSize=1000"`.
   `courses_2plus_institutions.csv` is the old ≥2-institution inventory; the SCNS flat file is authoritative.
6. Run `python validate_drafts.py --quiet` if the queue shows `error` rows, to see what is
   blocking them.
7. ⚠⚠ **If both queues are empty — which is the normal case — the work is the NEXT CAREER PATH.**

   ```bash
   python career_paths.py list                 # what is live
   python programs.py list                     # 40 programmes; a path's programmes must exist FIRST
   head -1 career_paths/QUEUE.csv; awk -F, 'NR>1 && $NF==""' career_paths/QUEUE.csv | head -5
   ```

   Take the top-ranked row with an empty `status`, and run the six-step research pass in
   **"THE RESEARCH IS THE COST OF A PATH"** above before writing a word. ⚠ Reckon on roughly a
   session per path; two rushed paths are worth less than one researched one.

8. Confirm with the user what they want to work on before generating anything.

Pushing to the live site runs from this repo (`generate_guide.py --push-from-queue`), using
the `REPO_ADMIN_*` credentials in `Tools/.env`. It is a write to production — confirm the
batch with the user before pushing, and never push a draft that `validate_drafts.py` fails.

### ⚠⚠⚠ When a push is INTERRUPTED — the recovery drill (batch 211)

**Batch 211's push was killed mid-run by system memory pressure.** ⚠⚠ **A killed push can leave a PARTIAL
state — some guides live, some not, and the queue half-marked — so the state must be CHECKED, never
assumed.**

**The drill, in order:**

1. ⚠ **Ask the SITE what is live**, not the queue:
   ```bash
   for c in ID1 ID2 ID3; do printf "%-9s " $c; \
     curl -s "https://floridacourserepo.com/api/v1/courses/$c/guide" | head -c 80; echo; done
   ```
2. **Then ask the QUEUE what it believes** — `python queue_mgr.py status`. **Where the two disagree, the
   site is the fact and the queue is the record to fix** (`queue_mgr.py reconcile`).
3. **Only then re-run** — and **split reconcile from push**: reconcile is fast, the push is the slow half,
   so running them as separate commands makes the failure point obvious instead of ambiguous.

✅ **The guide upsert is idempotent, so re-pushing an already-live guide is safe.** **Knowing the state
first is what tells you whether to expect a version bump and whether anything needs one.**

### ⚠⚠ Run long pipeline commands with `python -u`

**The killed push looked exactly like a slow push for several minutes, because the background output file
stayed EMPTY — Python buffers stdout when it is redirected to a file.**

⚠⚠⚠ **An empty output file is indistinguishable from a hung process, a slow process and a dead one.**

**Use `python -u` on anything that may run long** — the metadata build, `generate_guide.py`,
`list_courses.py`. Unbuffered output makes progress visible and makes a kill obvious immediately.

⚠ **Expect long runs on large prefixes.** The SCNS flat file is ~80 MB and is parsed once per prefix, so a
big prefix (`ARH` is the largest measured at 421 live ids) will push the metadata build and the push past
the two-minute tool timeout. **Give them explicit long timeouts rather than letting them background
silently.**

---

## Tone and quality bar

- Write in the voice of a thoughtful curriculum developer who knows Florida community colleges, not a generic AI summarizer.
- Specific beats generic. "Hibbeler is the most widely adopted text" beats "common textbooks are available." Named employers, named cities, named programs beat vague gestures.
- Honest hedging beats false confidence. "Varies by institution" is acceptable when true; making up a uniform standard is not.
- The user reviews each batch carefully — they are eager to see the guides. Earn that attention with substance.
