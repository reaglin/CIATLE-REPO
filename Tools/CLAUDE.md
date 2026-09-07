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

## Priority hierarchy

Apply in this order:

1. **Faculty requests** always go to the top of the queue. These are unpredictable and come up mid-session. When the user says "add EGN3214 because a faculty member requested it," that course supersedes the strict-priority pick. Custom specifications from faculty (e.g., "Python only, AI-integrated, two-half structure") are followed precisely.
2. **Strict priority by institution count** (descending) within `courses_2plus_institutions.csv`, with course ID as tiebreaker. Higher institution count = wider applicability = stronger signal that the guide will help more students.
3. **Human judgment overrides.** The user may demote or remove courses for reasons including:
   - Course offered only at non-Florida-public institutions (e.g., Keiser private, FL Tech private). The repository serves Florida public colleges and SUS institutions.
   - Course is part of a BAS or applied-degree program that isn't a true engineering degree (Engineering Technology BAS courses are fine; non-engineering BAS courses that happen to use an engineering prefix are out of scope).
   - Course is a shell (internship, special topics, independent study, thesis, dissertation, supervised research). Default is to skip these.
4. **When uncertain, ask.** Never silently substitute. Confirm before generating.

---

## Schema (required JSON structure)

Every guide is a JSON file with **exactly these six top-level keys**:

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

- `credits=0` is valid for PSAV (Postsecondary Adult Vocational) clock-hour courses; `contact_hours` carries the real measurement.
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
| `prerequisites` | ≤ 500 chars, or null |
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

### ⚠ Focus decision (Ron, 2026-09-04): priority courses across schools, NOT full catalogs

**Work the master `queue.csv` — the ≥2-institution priority subset — not a school's complete offering.**

The per-school queues from `school_queue.py` exist for **block recovery and sequencing**, not as a target
to exhaust. `queue_UWF.csv` holds 1,575 workable courses; **the 805 priority rows in the master are the
work.** Do not expand a batch into non-priority courses just because a prefix extraction is already in
hand — the exception is writing an orphan half needed to dispose of a queued `C` row under the
split-family rule.

**Why:** breadth across institutions serves more students per guide than depth at one. A course at 12
institutions is worth more than three courses at two.

### ⚠⚠ Source reachability register (re-probed 2026-09-06, batch 164)

**Check this before committing to a school.** Reachability, not course count, is the binding constraint.

| School | Pattern | Status |
|---|---|---|
| **UWF** | `catalog.uwf.edu/courseinformation/courses/<prefix>/<prefix>.pdf` (**lowercase**) | ✅ **working** — one fetch per prefix, full descriptions. The workhorse. |
| **FGCU** | `catalog.fgcu.edu/courses/<prefix>/<prefix>.pdf` (**the `.pdf`, not the directory**) | ✅ **working.** ⚠ The old directory URL is what was bot-blocked; the PDF answers. **Now the single most productive cross-check source in the project** — it documents credits explicitly and has produced the divergence a guide turned on in three consecutive batches. |
| **FSU** | `registrar.fsu.edu/bulletin/undergraduate-departments/<department>` | ✅ **working, and general-purpose.** Previously recorded here as useful only for the FAMU-FSU joint engineering college — **it is not.** Clean HTML with full descriptions, credits and prerequisites for `psychology`, `philosophy`, `social-work` and others. **Use it as the third vote when UWF and FGCU disagree.** |
| **UF** | `scratchpad/uf.py` — the `catalog.ufl.edu/course-search/api/` POST | ✅ **working** (keyword must be spaced: `"POT 4204"`). Title and existence only; `route=details` is broken. |
| **Broward** | `catalog.broward.edu/course-descriptions/<prefix>/` | ✅ **RECOVERED 2026-09-06** and used productively in batch 166. ⚠⚠ **The only routinely fetchable Florida source that publishes CONTACT HOURS explicitly** ("Total Contact Hrs: 48.00 / Lecture Hrs: 48.00") plus minimum-grade prerequisite conditions. **Go here first whenever a contact-hour figure is in doubt.** |
| **Valencia** | `catalog.valenciacollege.edu/coursedescriptions/coursesoffered/<prefix>/` | ✅ **RECOVERED 2026-09-06** — 200 with full body on `psy` and `mus`. Same regression, same recovery. |
| **DSC** | `daytonastate.smartcatalogiq.com/en/<year>/college-catalog/course-descriptions/<prefix-slug>/<level>/<course>` | ✅ **Confirmed on the CURRENT catalog 2026-09-07**, not just historically. ⚠ Two gotchas: the prefix slug is descriptive (`cop-computer-science`, not `cop`), and **the index page lists only titles — the individual course page carries description, credits, prerequisite and term**. A trailing slash 404s. **Same platform as IRSC.** |
| **UNF** | — | ⚠ **no static pattern found**, and now 301s to client-rendered pages. **Lead worth chasing: `digitalcommons.unf.edu/course_catalogs/` (archived PDF catalogs).** |
| **FSW** | `catalog.fsw.edu` (acalog, `catoid=27`, Course Descriptions `navoid=5491`) | ⚠ **PARTIAL BLOCK** — root returns 200 (26 KB) but **`content.php` and `search_advanced.php` both return empty 202s.** Root-reachable, content-blocked. |
| **FIU** | Coursedog API — `scratchpad/coursedog.py` | ✅ **SOLVED 2026-09-06 (batch 167). 27,923 courses, cached in `scratchpad/fiu_courses.json`.** ⚠⚠ **The gate is one header: `Referer: https://catalog.fiu.edu/`** — without it every endpoint returns `{"error":"Unauthenticated"}`. Richest Florida source: code, name, credits, college, description, cipCode, and per-component **contactHours**. ⚠ Duplicate rows per code — prefer the one with a real college name and a description. Full paging takes 2-3 min; **use the cache**. |
| **FAU** | `catalog.fau.edu` — Coursedog SPA | ❌ **ANSWERED 2026-09-07: no public Coursedog catalog at that host.** The discovery endpoint returns *"does not have entity assigned"* — the host is registered but no catalog is attached, which is why every schoolId guess failed. **Stop attempting FAU via Coursedog.** |
| **Coursedog discovery** | `app.coursedog.com/api/v1/catalogs/urls?url=<host>` (+ Referer) | ✅ **The portable bootstrap.** Returns `school` and `catalog.id` in one call — use it instead of scraping the page for ids. Works for any Coursedog school. |
| **USF** | `catalog.usf.edu` | ⚠ root 200 (75 KB) but **no course-description path exposed**; its only course link goes to `usf.edu/academics/courses-calendar.aspx`. Not yet a route. |
| Gulf Coast | `gulfcoast.edu/catalog/current/courses/<prefix>/index.html` | was the highest-value pattern in the DSC build; **re-probe before use** |
| **EFSC** | `catalog.easternflorida.edu/course-descriptions-information/<prefix>/` (and `/<prefix>.pdf`) | ✅ **NEW 2026-09-07 — CourseLeaf, same as UWF/FGCU/Broward/Valencia, existing tooling works unchanged.** Recovered `ADV2000C` and `COP3813C`. On CourseLeaf a prefix the college does not carry returns **202** — probe a prefix it definitely has. |
| **Tallahassee (TSC)** | `catalog.tsc.fl.edu` | ⚠ **CORRECTION: never blocked — the college RENAMED.** TCC → Tallahassee State College; `catalog.tcc.fl.edu` 000 was a dead host, not a block. New host is live (386 KB) but acalog `content.php` returns empty 202s. **Lesson: follow redirects on the main domain before recording a block.** |
| **IRSC** | `irsc.smartcatalogiq.com` | ⚠ **Live lead — SmartCatalogIQ, the same platform as the DSC build**, `/en/<year>/catalog/…`. Not yet exercised. |
| **⚠ Inventory reliability** | `courses_2plus_institutions.csv` | ⚠⚠ **The institution list is a HYPOTHESIS, not evidence — five confirmed errors in four batches** (`MUG2101`, `TPA3230C`, `BOT4404C`, `ATT1120`, `COP3014C`, all wrongly listing UWF or a suffix nobody uses). Two patterns: an institution listed that carries the subject under a **different number**, and a **suffix** in the inventory that no institution actually uses — both consistent with the file recording the SCNS catalog rather than current offerings. **Verify against a live catalog before treating an institution as a source or asserting a count in a guide.** |
| **⚠ FSU entry vs requirement text** | `registrar.fsu.edu/bulletin/...` | ⚠ A number followed by a period is **not** enough to locate a catalog entry — it also matches requirement prose (*"a grade of C or higher in COP 3014 or COP 3363."*). **Verify that a TITLE and a parenthesised credit value follow** (`COP 3014. Algorithm… (3).`). Cost a wrong result in batch 176. |
| **FSCJ** | Coursedog — `scratchpad/coursedog.py fscj` (school `fscj_peoplesoft`, catalog `sGHd4uJQXFdgDUaffhTv`) | ✅ **SOLVED 2026-09-07 (batch 173).** Was "platform unidentified". ⚠ **22,693 courses — the largest Florida catalog found so far**, and `fetch()` caps at limit=5000, so a single call silently returns a PARTIAL result. **Page it** (`scratchpad/fscj_dump.py`) and cache to `scratchpad/fscj_courses.json`. |
| **NWFSC** | Coursedog — `scratchpad/coursedog.py nwfsc` (school `nwfsc_banner_sql`, catalog `DGLrTHoh5uNIMFsdbzWf`) | ✅ **NEW 2026-09-07 (batch 173).** 1,781 courses, single page, cached in `scratchpad/nwfsc_courses.json`. Full descriptions and credits. Found because a 404 from `catalog.nwfsc.edu` returned a 1.1 MB body — **the body size was the tell.** |
| **Santa Fe** | `catalog.sfcollege.edu` | ⚠ Answers; not Coursedog (bootstrap 404s). Platform still unidentified. |
| **CF (Central Florida)** | `catalog.cf.edu` | ⚠ Root 200 (26 KB), **acalog** — so likely the same content-blocked pattern as FSW and TSC. Not exercised. |
| **MDC** | `mdc.curricunet.com/catalog/iq/3279` | ⚠ CurricUNET; 200 but ~10 KB (SPA shell). Lead, not a route. |
| **State colleges (standing retry list)** | SPC, HCC, PSC, PHSC, Palm Beach State, Chipola | ❌ **curl 000 / 404.** With TSC and FSW content-blocked and MDC an SPA, **this is what still blocks `MUG2101`.** |
| **Coursedog in Florida** | bootstrap endpoint, then `scratchpad/coursedog.py` | ✅ **REOPENED 2026-09-07 (batch 173) — the earlier "only FIU" conclusion was WRONG.** Three Florida Coursedog schools are now known: **FIU**, **NWFSC** and **FSCJ**. The earlier sweep missed them because it tested a guessed host list rather than the hosts the register already recorded as answering. ⚠ **Re-sweep the bootstrap endpoint against any host that answers before recording it as an unknown platform.** |

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

## Session start checklist

When starting a fresh session in this project:

1. Read this file (you are here) — it governs guide *content*.
2. Read `Generate_Guides_and_Push_Process.md` for the end-to-end process (it is the
   start-here document), `README.md` for per-tool detail, and `QUEUE_GUIDE.md` for the queue
   schema and priority tiers. `.claude/skills/guide/SKILL.md` at the repo root drives the
   mechanics.
3. Run `python queue_mgr.py status` to see where things stand. `queue.csv` is the
   authoritative work queue; `courses_2plus_institutions.csv` is the inventory to refill from.
4. Run `python validate_drafts.py --quiet` if the queue shows `error` rows, to see what is
   blocking them.
5. Confirm with the user what they want to work on before generating anything.

Pushing to the live site runs from this repo (`generate_guide.py --push-from-queue`), using
the `REPO_ADMIN_*` credentials in `Tools/.env`. It is a write to production — confirm the
batch with the user before pushing, and never push a draft that `validate_drafts.py` fails.

---

## Tone and quality bar

- Write in the voice of a thoughtful curriculum developer who knows Florida community colleges, not a generic AI summarizer.
- Specific beats generic. "Hibbeler is the most widely adopted text" beats "common textbooks are available." Named employers, named cities, named programs beat vague gestures.
- Honest hedging beats false confidence. "Varies by institution" is acceptable when true; making up a uniform standard is not.
- The user reviews each batch carefully — they are eager to see the guides. Earn that attention with substance.
