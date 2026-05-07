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

## Workflow: interactive batch processing of 5

Sessions follow this loop. Do not skip the confirmation step.

1. **Identify the next 5 candidates.** Read `queue.csv` if uploaded, otherwise compute from `courses_2plus_institutions.csv` minus already-completed work in `drafts/` and the activity log.
2. **Present the proposed batch to the user as a table** with course ID, institution count, title, and brief notes. Flag any uncertainty (generic titles, content variation risk, low institution count).
3. **Wait for confirmation.** The user may approve, substitute courses, or remove items. Common reasons to substitute: faculty requests, courses at non-public-college institutions, BAS courses that aren't true engineering courses.
4. **Clear `/mnt/user-data/outputs/` of prior `.json` files.** This ensures the user's "Download All" zip contains only the current batch.
5. **Generate the 5 guides** as a single Python build script in `/home/claude/build_guides_N.py`, then execute. Each guide goes to `/mnt/user-data/outputs/{COURSE_ID}_guide.json`.
6. **Validate.** Confirm all 6 required keys present, sensible credit/contact-hour values.
7. **Call `present_files`** with all 5 paths. The user cannot download files that haven't been presented; never end a generation turn without this call.
8. **Provide sanity-check notes** in a brief table: course, credits, contact hours, file size — followed by short bullets flagging anything worth the user's review (unusual hour counts, generic titles, novel content, institutional variation).

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

- **Output filename**: `{COURSE_ID}_guide.json` exactly. Course ID is uppercase, no spaces. The PowerShell importer (`import_zip_to_drafts.ps1`) and `queue_mgr.py reconcile` both depend on this naming.
- **Outputs directory**: `/mnt/user-data/outputs/` — clear before each batch so the "Download All" zip is clean.
- **Working directory**: `/home/claude/` — for build scripts and intermediate work the user doesn't need to see.
- **Project files**: `/mnt/project/` — read-only; treat as reference only, never expect modifications to persist back.
- **Always call `present_files`** with all 5 output paths after generation. Files that aren't presented cannot be downloaded by the user.

---

## What to skip (default)

Shell-style EGN courses unless the user says otherwise:
- `XXXX900`, `XXXX905`, `XXXX910` — independent study / directed individual study
- `XXXX940`, `XXXX941`, `XXXX945`, `XXXX949` — internship / cooperative education
- `XXXX950`, `XXXX951` — special topics
- `XXXX971`, `XXXX973` — thesis
- `XXXX980`, `XXXX981` — dissertation
- `XXXX990`, `XXXX991` — supervised research

Title keywords that flag shell courses regardless of code: INTERNSHIP, COOPERATIVE, SPECIAL TOPICS, INDEPENDENT STUDY, DIRECTED STUDY, THESIS, DISSERTATION, SUPERVISED RESEARCH.

---

## Session start checklist

When starting a fresh session in this project:

1. Read this file (you are here).
2. Read `README.md` for tooling and command details.
3. Look for `queue.csv` in `/mnt/user-data/uploads/` — if present, that's the authoritative work queue. If absent, compute candidates from `courses_2plus_institutions.csv`.
4. Check `/mnt/user-data/uploads/` for any guide JSONs the user is asking you to revise vs. generate fresh.
5. Confirm with the user what they want to work on this session before generating anything.

The user maintains the queue, runs `queue_mgr.py reconcile` on their machine, and pushes guides via `generate_guide.py --push-from-queue`. Claude does not push to the live site directly.

---

## Tone and quality bar

- Write in the voice of a thoughtful curriculum developer who knows Florida community colleges, not a generic AI summarizer.
- Specific beats generic. "Hibbeler is the most widely adopted text" beats "common textbooks are available." Named employers, named cities, named programs beat vague gestures.
- Honest hedging beats false confidence. "Varies by institution" is acceptable when true; making up a uniform standard is not.
- The user reviews each batch carefully — they are eager to see the guides. Earn that attention with substance.
