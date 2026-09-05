# Session handoff — curriculum guide pipeline

**Updated 2026-09-04 (after batch 133).** Read this first, then `SOURCES.md` (findings, batch by batch) and
`REVIEW_QUEUE.md` (the short list of decisions waiting on Ron).

---

## Where things stand

**Daytona State is finished: 935/935, 100%.** The queue has been **refilled from UWF**.

| | |
|---|---|
| Guides live | **1,807** (37 corrected to v1.1; 2 split into -UWF variants) |
| Queue | **746 queued**, 315 skipped |
| Overall | 70.7% of a 2,568-row decided total |
| Daytona State | **935 / 935 (100%)** |
| Last batch completed | **133** — HSC behaviour analysis, pharmacology, nutrition (7). **HSC CLOSED.** ANT, EEL, MLS, NUR, ART, HSC, PCB, MCB, ISM and MAN are all closed |

The 288 skipped rows: **229 with no DSC coverage**, **53 shells**, the rest blocked with the reason in
the row note. All are `skipped` rather than deleted so the Request a Curriculum Guide feature can
resurrect them.

---

## The UWF build — read this before the first batch

**Everything needed is already in `SOURCES.md`; do not re-derive it.** Search it for "UWF".

**1. The catalog is a per-prefix PDF, and one fetch yields the whole prefix.**
`catalog.uwf.edu/courseinformation/courses/<prefix>/<prefix>.pdf` — `curl` it down, extract with
`pypdf`. ⚠⚠ **The prefix must be LOWERCASE** (`.../courses/ant/ant.pdf`); the uppercase form returns a
404 whose 196-byte HTML body `curl` writes out with exit 0 — **check the byte count, not the exit code**.
Corrected in `SOURCES.md` at batch 122. Re-confirmed on ANT: 6 pages, 61 courses, full descriptions.

**2. Ron's standing procedure applies and is the default here.** *"When the opportunity arises to
complete a prefix without having to do multiple fetches, we should go ahead and do that."* The 871 remaining rows
span **166 prefixes** (ANT now closed), so the rest of the queue is reachable in ~166 fetches rather than ~870. **Work
prefix-first, not queue-order.** Biggest prefixes now: **MLS 27, NUR 24, ART 22, HSC 19,
PCB 19, PHI 16, MVK 15, SOW 15.**
⚠ **A closed prefix means every *writable* row is done, not every queued row** — see item 9 in
`REVIEW_QUEUE.md`. Expect a residue of `C`-suffix rows in any prefix where UWF splits lecture from lab.

**3. ⚠⚠ UWF publishes no contact hours and no terms — but it DOES publish fees and corequisites.**
There is **no tier-1 hour source at this institution at all** — every UWF contact-hour figure is derived
and should be labelled so. Established conventions (batches 88–90, evidence-backed): **3-credit lecture
= 45 hrs (15/cr)**; **1-credit engineering and science labs = 45 hrs** (matching live EVR2001L and
OCE1001L), while **clinical labs run 30**. **Do not carry DSC's other conventions across without
evidence.**

**3b. ✅✅ The `*` in a UWF prerequisite means CONCURRENT** — *"may be taken prior to or during the same
term"*, per `catalog.uwf.edu/courseinformation/`. **This is the corequisite mechanism batch 119 concluded
UWF lacked.** It is how a split lecture+lab pair is taken together, and reading it as sequential adds a
term to a student's plan. 14 of 51 EEL courses use it; 0 of 61 ANT courses do.

**3c. ⚠⚠ Prerequisite/fee/grade publishing is PREFIX-DEPENDENT — never generalise from one prefix.**
Engineering publishes prerequisites densely (EEL 32/51) with non-uniform grade conditions (C vs C-);
humanities sparsely (ANT 15/61, zero grade conditions). **Fee notices exist in both** (ANT 3, EEL 5).
A property claimed of "UWF" must be checked in **two prefixes of different character** before being
recorded as institution-wide — that rule exists because batch 119 got this wrong and 34 guides had to be
corrected. See `SOURCES.md` batch 123.

**3d. ✅ SPLIT-FAMILY RULE (Ron's decision, batch 124) — apply this in every prefix.**
When a queued `C`-suffix row has no UWF entry, check whether UWF publishes the **split lecture+lab
family**. If it does: **write the UWF halves as orphan additions** (they need not be in `queue.csv` —
`reconcile` auto-adds them, and the push endpoint creates the course record on demand), then mark the
`C` row `skipped` with a note naming the covering pair. If UWF publishes no equivalent at all, skip as
no-source-coverage. **ANT and EEL both closed with zero residue this way. PCB, MLS and NUR are next.**

**3e. ⚠⚠ UWF has TWO corequisite notations, and three lecture/lab pairs bind RECIPROCALLY.**
`X*` = *may be taken prior to or during the same term*; an explicit `Co-requisite: X` conventionally means
*the same term only*. **`EEL3111`/`EEL3111L`, `EEL3701`/`EEL3701L` and `EEL4712`/`EEL4712L` each list the
other**, making the pair effectively one 4-credit course. **`EEL4744`/`EEL4744L` binds one way only** —
the lab requires the lecture, not the reverse, so the lab can be skipped inadvertently. **Check both
directions when writing a split pair.**

**3f. ⚠⚠⚠ THE `C` SUFFIX DOES NOT ALWAYS MEAN "INTEGRATED LECTURE+LAB" — check per prefix.**
In **MLS** the C-suffix courses are a **separate "Professional Track"** with different prerequisites
(`MLS3194` AND `MLS3621`). **Batch 127 established what it is for:** every course uses *virtual*
laboratories, the track has **no hospital rotations**, and its capstone `MLS4704` requires a portfolio
evidencing work experience *"equivalent to an MLS clinical internship."* → **It is a degree-completion
route for people already working in laboratories.** A student with no lab experience cannot complete it.
⚠ The batch-124 split-family rule does NOT apply mechanically to such a track.
⚠ **Our own `validate_drafts.py` encodes the wrong assumption** — it warns "C course but only 45 contact
hours" on 3sh Professional Track courses. The warning is non-blocking and was correctly overridden;
**consider a per-prefix exception if it recurs** (flagged for Ron, not changed).

**3g. ⚠⚠ "Permission is required" gates most MLS courses on COHORT ADMISSION**, not on the listed
prerequisites — miss the application and it is a year's wait. Expect the same in **NUR** and other
health prefixes.

**3h. ✅ RESOLVED (batch 126): hospital rotations get 45 contact hours per credit, labelled a FLOOR.**
`MLS4820L`-`4825L` are supervised hospital practice, not campus labs. The practicum convention (45/credit
→ 180h at 4sh, 90h at 2sh) is applied, and **every guide states it is a floor, not an estimate**, because
NAACLS rotations are commonly full-time blocks over weeks. ⚠ Each guide names the rotation schedule as
the key practical fact UWF does not publish and tells the student to get it in writing.

**3i. UWF expresses co-requisites THREE ways** — `X*` asterisk, an explicit `Co-requisite:` field, and
**plain prose in the description** (new at batch 125, e.g. *"MLS students are required to take the
corresponding laboratory..."*). ⚠ The prose form is **conditional on major**: non-MLS students may not
be bound by it.

**3j. ⚠⚠⚠ RON'S RULE (batch 126): a SUFFIX IS A FILING DECISION, NOT A DESCRIPTION.**
> *"Many of these course designations are just trying to fit course requirements into a limited group of
> course designation options."*

SCNS offers a small suffix set (none / `C` / `L`) and every course must be filed under one. When the
course does not fit, the closest slot is used. **Documented instances:** `MLS4820L`-`4825L` are hospital
rotations filed as `L`; `MLS4193C` etc. are a separate programme track filed as `C`.
**Operating rule: the DESCRIPTION is the authority on what a course is; the suffix is the authority on
nothing.** Say so in the guide whenever the suffix would mislead. ⚠ This also reframes much of the
"drift" theme — institutions are encoding varied provision into a code set too small to describe it.

**3k. The `/L` notation** (`MLS 4191/L`, `PHY 2049/L`, `MCB 3020/L`) is UWF shorthand for a course
together with its laboratory. Appears in both MLS and EEL.

**3l. ⚠⚠ PARALLEL ROUTES ARE COMMON, AND THEY ARE NOT ALWAYS NAMED.**
Three prefixes now show two routes through the same subject matter:
- **MLS** — standard split lecture+lab vs **"Professional Track"** (named in every title).
- **NUR** — chained cohort sequence vs a **standalone group with no prerequisites at all** (named
  NOWHERE; a search for "RN"/"registered nurse"/"licensed" returns zero hits).

⚠ **Detect it by the prerequisite structure, not the titles.** In NUR the giveaway is duplicated
subjects under different numbers — `NUR3081`/`NUR3805` share an **identical title**, plus
`NUR4125`/`3125`, `NUR3145`/`3095`, `NUR3067`/`3138C`, `NUR4826`/`4827`, `NUR4636`/`4615`.
⚠⚠ **State the structure as observed and label the "why" as an inference** where the catalog does not
say it. For NUR the stakes are high: a degree-completion route does not lead to initial licensure.

**3m. ⚠⚠ THE SCNS TITLE CAN NAME A DIFFERENT SUBJECT ENTIRELY — not just a variant.**
`NUR4286`: SCNS says **"Gerontological Nursing"**, UWF teaches **quality and safety**.
`NUR4826`: SCNS says **"Ethics"**, UWF teaches **leadership**.
→ **Always read the description before trusting the queue title.** Say in the guide that the course
should not be assumed to satisfy a requirement named by the SCNS title. (Ron's suffix rule, 3j, extended
to titles.)

**3n. ⚠ GREP EACH PREFIX for `Communication Skills Requirement`.** UWF publishes this general-education
designation inside description text, not a structured field. Three found so far: `ANT4403`, `MLS4704`,
`NUR4828`. Always note: confirm the minimum grade, and the designation is the part least likely to transfer.

**3o. ⚠ HEALTH PREFIXES ARE NOT A UNIFORM CATEGORY — a prediction that failed.**
The batch-127 handoff predicted NUR would repeat MLS's patterns. It did not: **NUR has ZERO "permission
is required" markings and effectively no fees**, against MLS's near-universal gating and 16 fee notices.
**Check each prefix; do not generalise from a sibling.**

**3p. ⚠⚠⚠ ONE NUMBER, TWO SUBJECTS — publish BOTH (Ron's decision, batch 129).**
When the statewide SCNS title and the institution's title name **different subjects** (not different
wordings), publish **three** pages: `XXXnnnn-SCNS`, `XXXnnnn-<INST>`, and the bare `XXXnnnn` as a
**disambiguation page**. **Full rule and mechanics are in `Tools/CLAUDE.md`** — read it before handling one.
⚠ `NUR4286` and `NUR4826` are done except their `-SCNS` halves, which **need the SCNS catalog from Ron**.
⚠ The tooling regex was widened for this; when copying a draft to make a variant, **delete `pushed_utc`**.

**3q. ⚠⚠ PER-SCHOOL QUEUES + BLOCK RECOVERY (Ron's direction, batch 129).**
Order: **UWF, UNF, FGCU first**, then UCF/UF/USF, mixing in state colleges.
`queue.csv` is the **master** (now has a **`source_inst`** column); `queue_<SCHOOL>.csv` are derived work
lists from **`school_queue.py`** (`coverage` / `build <SCHOOL>` / `status`). Dedup is automatic.
⚠ **Rebuild per-school queues after every push** — they are derived, not maintained.
⚠⚠ **Keep 2-3 schools' queues built ahead** so a bot block never stalls a batch. Reachability register
with today's probes is in `Tools/CLAUDE.md` — **UWF works; FGCU, Broward and Valencia all return empty
202s; UNF has no static pattern found yet** (lead: `digitalcommons.unf.edu/course_catalogs/`).
⚠ Scale: "complete UWF" = **1,575 workable**, not the 805 in the master. See `queue_UWF.csv`.

**3r. ⚠⚠⚠ THE SUFFIX RECORDS AN ADMINISTRATIVE CHOICE; THE DESCRIPTION RECORDS THE COURSE.**
Ron's rule, and batch 135 found the clearest instance: **`PCB3097L` is 3 sh and its description says the
theme runs "within both lecture and laboratory"** — an integrated course wearing an `L` suffix.
⚠ **Whenever an `L`-suffix course carries more than 1-2 semester hours, read the description before
deriving hours.** Trusting the suffix here would have produced 135 contact hours instead of 60.
Say so in the guide: full credit workload, no separate lecture to enrol in, and **send the catalog
description rather than just the number when transferring it**, because a receiving institution comparing
suffixes may misjudge it.

**3s. ⚠⚠ GREP `permission` ALONE — never a fixed phrase.**
The standing pre-prefix scan looked for `Permission is required` and returned **0 hits for all of PCB**.
`PCB4233L` actually publishes **"Special permission required."** Catalog wording is not standardised even
within one institution's own catalog. **Same applies to fee wording** (`Material and Supply Fee`,
`Equipment Fee`, `fee will be assessed`) — grep the word, not the sentence.

**3t. ⚠⚠ READ LECTURE AND LABORATORY ENTRIES TOGETHER BEFORE WRITING A FEE SECTION.**
UWF frequently publishes a **laboratory's fee on the LECTURE entry** (`PCB3063`, `PCB4524`, `PCB4723` all
say the fee is assessed "for/to the corresponding lab"), while other laboratories publish their own
(`PCB4233L`; `PCB4723L` carries **two**). Reading either entry alone gives a wrong answer in one direction
or the other.

**3u. ⚠ A PERMISSION MARKING CAN BE A DOOR RATHER THAN A GATE.**
`PCB4870` publishes: *"Prerequisite is PCB 3063 (Genetics), however students may obtain department
permission to take the course without the specified pre-requisite."* The inverse of every other permission
marking found. **State both halves**: the waiver must be actively requested before registration opens, and
**it removes an administrative barrier, not the underlying content**.

**3v. ⚠⚠⚠ WATCH FOR A SINGLE CLAUSE THAT CHANGES THE WHOLE COURSE.**
`PCB4315`'s description delivers its content **"through a field experience in the Bahamas"** — one clause,
and nothing else in the entry mentions it. A study-abroad delivery means **passport, programme fee beyond
tuition, possible SCUBA certification, a travel window that may not match the term, insurance and remote
medical access**. UWF publishes none of the costs, so the guide **names each thing the student must ask
about** rather than inventing figures — and says plainly that the course is a real differentiator *and*
that the cost barrier is real.

**3w. ⚠ "HONORS" IN AN INVENTORY TITLE IS NOT AN HONORS COURSE.**
`PCB4673` (Honors Evolution → Principles of Evolution) and `PCB4841` (Honors Cellular Neuroscience →
Journey to the Brain). Another institution's honors section title entered the statewide inventory. Tell the
student: **the number is not inherently an honors number, honors credit depends on the offering institution
designating the section, and this does not affect transfer** — SCNS equivalency runs on number and content.

**3x. ⚠ A CONCURRENT GRADUATE TWIN MAY SIT IN A DIFFERENT PREFIX.**
`PCB4028` is offered concurrently with **`BSC 5873`**, not a PCB 5xxx — the only such case in the prefix.
Do not assume the graduate equivalent shares the prefix; searching PCB would not find it.

**3y. ⚠⚠⚠ ONE INSTITUTION CAN RUN SEVERAL PARALLEL ROUTES THROUGH THE SAME SUBJECT.**
UWF runs **three** microbiology routes in **two colleges and three departments** (`MCB1000`/`L` non-majors
and BSN prerequisite; `MCB2010`/`L` health sciences; `MCB3020`/`L` biology majors) — **and only the third
opens `MCB4203`.** Nothing in any title says so.
⚠ **Build a routes table into every guide in such a prefix**, not just the one where you noticed it.
⚠ **The prerequisite gap is the tell**: `MCB3020` needs chemistry plus a year of biology; `MCB2010` needs
nothing. **Read prerequisites and the department line, never titles.** Fourth prefix where this surfaced a
hidden structure (MLS, NUR, HSC, MCB).

**3z. ⚠⚠ A LECTURE/LAB PAIR CAN BE BOUND WITH DIFFERENT NOTATION ON EACH HALF — OR NOT BOUND AT ALL.**
`MCB3020` names the lab as an **asterisked prerequisite**; `MCB3020L` names the lecture in an explicit
**`Co-requisite:` field**. Same effect, two notations — the only such case found.
⚠ **The opposite is more dangerous**: `MCB2010`/`MCB2010L` publish **no prerequisite and no co-requisite**,
so **nothing stops a student enrolling in one without the other**. Where a pair is unbound, **say so
explicitly and call it a registration hazard** — students reasonably assume the system will catch it.

**3aa. ⚠⚠ "DESIGNED TO MEET THE X PREREQUISITE" IS TRUE FOR THAT INSTITUTION ONLY.**
`MCB1000` says it is *"specifically designed to meet the microbiology pre-requisite requirement for the 4
year BSN degree."* **Take it at face value for UWF and qualify it for everyone else**: other Florida
programmes name different numbers (often `MCB2010C`), **catalog year binds**, most require the lab too, and
most impose a **minimum grade and a recency limit**. **A passing grade is not a qualifying grade.**
This is constraint 4 of the career-pathways note in `CIATLE-REPO/CLAUDE.md` in the wild.

**3ab. ⚠ EMIT AN EXPLICIT "NO FEE PUBLISHED" BLOCK, NOT SILENCE.**
`MCB1000L` and `MCB3020L` publish a Material and Supply Fee; **`MCB2010L`, same department, same kind of
course, publishes none.** Where siblings differ, the absence is informative — say it, and say that fee
schedules change and the catalog is not the billing system.

**3ac. ⚠⚠ A PREREQUISITE FIELD WITH NO COURSE NUMBER IS STILL A PREREQUISITE.**
`ISM3011` publishes *"Completion of 45 hours of college course work is required prior to taking this
course."* — a **standing requirement**, the first found in this build. It is easy to miss because it does
not appear in a prerequisite chain. **Say what it means**: a first-year student cannot take it and
therefore cannot start the sequence; **transfer students must confirm how their credit counts** (dual
enrolment, credit by exam and developmental coursework are treated differently); and **business colleges
commonly add admission-to-the-major and GPA gates the course entry does not name.**
⚠ Watch for these in every business, education and health prefix.

**3ad. ⚠ WHEN ONE COURSE GATES A WHOLE PREFIX, SAY SO IN EVERY GUIDE IN IT.**
Every undergraduate ISM course except `ISM3011` requires `ISM3011`; only `ISM3323` has an alternate
(`OR COP 2253`). **A shared hub block goes in all of them**, naming it a single point of failure in the
student's schedule with no route around it. Do not mention it only in the hub course's own guide.

**3ae. ⚠⚠ USE THE `drift()` BLOCK — and assess naming vs subject each time.**
Four title divergences in one prefix, of three different kinds: naming only (`ISM3011`), extension
(`ISM4400`), and **possible different subject** (`ISM4320`, `ISM4545` — both added to the `-SCNS`
open-cases table). **The practical advice is identical in every case and should be stated every time:
carry a syllabus, and search on the number rather than the name.**

**3af. ⚠⚠⚠ AI INTEGRATION IS LOAD-BEARING IN BUSINESS/COMPUTING PREFIXES — write it properly.**
Two reusable sections now exist: `AI_CORE` (AI as a tool used while studying) and `AI_CENTRAL` (AI as the
subject). The three points that must appear:
1. **Where the tools fail specifically** — invented functions and endpoints, code that runs and is subtly
   wrong, confident wrongness on anything niche or recent.
2. **⚠ The failure mode that matters: a wrong answer that looks right.** *A query that returns rows is not
   a query that returns correct rows.*
3. **⚠⚠⚠ Never paste confidential, personal or regulated data into a public AI tool** — named as a common
   way early-career employees cause serious incidents.
Plus, where AI is the subject: bias at scale, **silent drift**, **accuracy as a bad metric for rare
events**, explainability as a legal requirement, and **"we had the data" ≠ "we were permitted to use it."**

**3ag. ⚠ BUSINESS TRANSFER HAS AN AACSB TRAP SCNS DOES NOT COVER.**
Many Florida business colleges are AACSB accredited and **limit how much upper-division business coursework
may transfer in**, frequently requiring a share in residence. **A course can articulate under SCNS and
still not count toward the major.** Say this in every business-prefix guide.

**3ah. ⚠⚠⚠ TITLE DRIFT HAS A WORSE FORM: THE NUMBER COLLISION.**
`MAN4350` is not one number carrying two subjects — it is **two numbers whose subjects have permuted**.
Statewide, `MAN4320` = Recruitment and Selection and `MAN4350` = Training and Development. At UWF,
`MAN4350` = **Recruitment and Selection** and `MAN4320` is not published; training lives inside `MAN4341`.
⚠ **When a drift is found, check the NEIGHBOURING numbers in the same family before writing it up.** A
one-number note is wrong if the subject reappears under a different number.
⚠ **The `-SCNS` rule does not cleanly cover this** — it assumes one number, two subjects. Flagged in
`REVIEW_QUEUE.md` item 10 for Ron.

**3ai. ⚠⚠ STANDING REQUIREMENTS VARY WITHIN A SINGLE PREFIX — parameterise, do not generalise.**
MAN uses **45 hours** (`MAN3301`, `MAN3504`, `MAN3583`), **60 hours** (`MAN4280`, `MAN4441`), **none**
(`MAN3802`), and **course prerequisites** (`MAN4341`/`MAN4350`/`MAN4384` → `MAN3301`; `MAN4570` →
`MAR 3202`). The `standing()` helper takes the threshold as an argument and **every guide states that UWF
uses more than one**. Extends rule 3ac.

**3aj. ⚠ CHECK THE DEPARTMENT LINE FOR PREREQUISITE CONVENTION, NOT ONLY FOR CONTENT.**
`MAN4570` sits in the **Department of Commerce** rather than Business Administration, **and its
prerequisite convention differs accordingly** (`MAR 3202`). Third prefix where a cross-department placement
mattered — after `HSC3555` (biology-taught) and MCB (three departments).

**3ak. ⚠⚠ A BATCH CAN NEED NO ORPHANS AND NO SKIPS.**
MAN batch 138 was the first: **all 10 queued rows had UWF entries**. Do not assume the split-family rule
will apply; check coverage first and be pleased when it is clean.

**3al. ⚠⚠⚠ THE ARTS NEED THEIR OWN CONTACT-HOUR CONVENTIONS. Implemented in `scratchpad/wart.py`.**

| Convention | Rate | Use for |
|---|---|---|
| **activity** | **30 per credit** | class piano, group skills, activity courses |
| **studio / performance** | **60 for 3 sh** | studio art, acting, movement, voice |
| **applied music** | **≈15 total, whatever the credit** | private instruction — **the lesson hour only** |

⚠ **Applied music is not a rate.** One weekly lesson ≈ 15 hours a term whether the course is 2 or 3 sh.
**Say explicitly in the guide that the figure is lesson time only**, and that credit is earned in practice
(conventionally 1-2 hours daily per credit) plus juries, studio class and recital obligations.
⚠ **The validator does not check any of these** — 1 sh/30, 2 sh/15 and 3 sh/60 all pass silently. Arts
guides get no automated sanity check on hours; get them right by hand.

**3am. ⚠⚠ THE ARTS ARE THE WORST CASE FOR THE SUFFIX RULE (3r).**
SCNS offers none / `C` / `L` and **none of them describes a studio, rehearsal room, or private lesson**.
UWF's TPP prefix files studio courses under all three: `TPP2101L`/`TPP3102L` (L), `TPP2710C`/`TPP2167C` (C),
`TPP2110`/`TPP2100` (none). **Use the shared `SUFFIXNOTE` block in every arts guide**, and tell students to
send the description and syllabus rather than the number when transferring.

**3an. ⚠⚠⚠ TWO COURSES, NEARLY IDENTICAL DESCRIPTIONS, NO PREREQUISITE ON EITHER = a registration trap.**
`TPP2110 Acting I` vs `TPP2100 Acting for Non-majors` differ by one phrase (*"some prior experience on
stage"*), **neither publishes a prerequisite**, and **only `TPP2110` opens `TPP3155`**. The statewide
inventory lists **both under the title "Acting I"**.
⚠ **When two courses in a prefix are near-duplicates, write a mutual disambiguation block into BOTH**,
state which one gates the sequence, and say plainly that registration will not catch the error.

**3ao. ⚠ LOOK FOR THE UNADVERTISED ACCESS PROVISION.**
Two in MVK that students do not know exist: **"placement / audition may substitute for prerequisite"** on
class piano (**but placement is examined at or before the start of term — asking later loses the option**),
and **applied lessons open to non-majors** if a music course or ensemble is taken concurrently and faculty
schedules permit (**ask in the preceding term, and ask the department, not general advising**).
Conversely `MVK1115` publishes **"Open only to music majors" inside its description** — a registration bar
in the prose, where no prerequisite field would show it.

**3ap. ⚠⚠ NAME THE PROGRAMME-LEVEL GATE, not just the course.**
The class piano sequence exists to prepare the **piano proficiency examination** — a degree requirement at
essentially every accredited US music programme that **delays graduation when failed, regardless of grades
elsewhere**. It tests *functional* playing (harmonisation, transposition, sight-reading, score reading,
accompanying), so **a student who plays difficult repertoire from memory can still fail it**.
⚠ Same shape as NCLEX-RN, ASCP and FE/PE in other prefixes: **the terminal requirement is the thing to
write toward.**

**3aq. ⚠⚠⚠ LAY A PREFIX'S APPLIED/PERFORMANCE NUMBERS SIDE BY SIDE — the structure is never stated.**
MVK assigns applied numbers by **instrument × standing**, with **no prerequisite chain**, and **piano has
two parallel ladders**: "Performance: Keyboards" (**3 sh fixed**) versus "Applied Music Piano" (**2-3 sh
variable**). **Fixed-versus-variable credit is the tell for a performance-major track.**
⚠ Build the ladder table into **every guide in the ladder** and say that **which track a degree plan uses
is a departmental decision to settle in the first term** — credits on the wrong track may not substitute.
⚠ **Repeat limits vary across the ladder** (6 vs 9 sh) and matter, because sequences are built by repeating
a number. Fifth prefix where structure-reading beat title-reading (MLS, NUR, HSC, MCB, MVK).

**3ar. ⚠⚠ THE APPLIED-MUSIC HOUR FIGURE TRIPS THE VALIDATOR AT 3 sh. Override it.**
`MVK3331`/`MVK4341` (3 sh / 15 hrs) warn; the 2 sh applied guides at 15 hrs do not. **Both behaviours are
uninformative** — the heuristic does not model applied formats. **Override the warning, and say in the
guide why the figure is what it is.** Flagged for Ron as a possible per-format exception, alongside the
MLS C-suffix and NUR clinical-hours conflicts.

**3as. ⚠⚠ MAP A CHAINED ARTS SEQUENCE AND PUT IT IN EVERY GUIDE.**
TPP chains four deep with `TPP3155` as the hinge, **crosses into the `THE` prefix** for two prerequisites,
and **the entry course matters**: `TPP3155` requires `TPP2110`, not `TPP2100`. With arts courses frequently
offered **one term a year**, a wrong entry or a single failure **costs a year, not a term**. None of this
is stated in the catalog — a shared `SEQ` block carries it.

**3at. ⚠⚠⚠ PHANTOM NUMBERS: check that a cited prerequisite or exclusion actually EXISTS in the prefix.**
Two in TPP: `TPP2710C` requires **`TPP2121`, which is not published** (the sibling course requires
`TPP2120`, so it looks like a transposed digit — **do not say so**); `TPP4113` excludes credit with
**`TPP4141`, which is not published**. Fifth and sixth catalog-internal discrepancies in the build, after
EEL3111L, MLS4631C, NUR3026/3805 and ART4333C.
⚠ **Handling is settled: reproduce as published, name the anomaly, refuse to guess, send to the
department** — and state the practical consequence (a phantom exclusion can block transfer credit).

**3au. ⚠⚠⚠ ADD TO THE PRE-PREFIX SCAN: grep for `may not be received` and CHECK THE NUMBER EXISTS.**
Three phantom exclusions found so far, in three different colleges: `EEL3111L` (batch 122), `TPP4113`
(141), `TAX4001` (142) &mdash; each excluding credit with a number the catalog does not publish. **This is
not a departmental quirk.** Reproduce as published, name the anomaly, refuse to guess, and **state the
consequence: a phantom exclusion can block transfer credit, and it surfaces at a degree audit in a final
term.**

**3av. ⚠⚠ A DESCRIPTION CAN SIMPLY BE STALE &mdash; a fourth category, distinct from drift and contradiction.**
`CPO2002` lists example countries including **the USSR**, dissolved 1991. Not a contradiction, not a title
drift &mdash; **an unrevised catalog entry**. Handling: say plainly that it is stale, that **illustrative
examples are not the syllabus**, and **tell the student to ask the instructor what the course actually
covers**. ⚠ Course descriptions are among the least frequently revised texts an institution publishes;
**watch for dated technology, dated country names, and dated legislation elsewhere.**

**3aw. ⚠ CHECK NEIGHBOURING NUMBERS ON EVERY DRIFT (extends 3ah).**
`CPO2001` (statewide "Comparative Politics", 8 inst, already pushed) versus `CPO2002` (statewide
"Comparative Government", 16 inst; **UWF publishes it as Comparative Politics**). Same shape as the
`MAN4350`/`MAN4320` collision but **materially milder**, because the two names denote one subfield rather
than two subjects. **Record as a naming overlap; do not escalate to `REVIEW_QUEUE.md`.** The judgement to
make each time: **do the two titles name different SUBJECTS, or the same subject differently?**

**4. The single-term-offering flag is unavailable here** — UWF publishes no terms. Say the catalog does
not publish it rather than being silent.

**5. Variable-credit courses need explicit handling.** UWF publishes ranges (`1-12 sh`, `0-3 sh`); the
schema takes one integer, so state the published range in the guide.

**6. 218 UWF courses were already written from DSC's catalog** (190 pushed, 28 skipped). Not a
correction candidate — each guide states its source — but **when a prefix extraction is in hand, its
already-published members are free to check**, and any real divergence goes to `REVIEW_QUEUE.md` as a
v1.1 candidate.

---

## Next up

**Six prefixes now close with zero residue: ANT (48/6), EEL (33/11), MLS (33/2), NUR (45/8), ART (40/4),
HSC (29/4).**

Remaining by size: **PCB 19, PHI 16, MVK 15, SOW 15, FIN 14.**

- **PCB is a science prefix** — expect split lecture+lab families; the batch-124 orphan rule should apply
  straightforwardly, and **science labs take 45 hours per credit**, not the 30 used for clinical labs.
- **PHI is a humanities prefix** — expect the plain lecture convention and few structural constraints,
  like ANT.
- **MVK is applied music** — genuinely new territory. Expect **repeatable courses** (as in ART) and likely
  **per-student individual instruction rather than class contact**, which will need its own hour reasoning
  rather than borrowing the lecture or studio convention.

⚠ **Standing checks before each prefix** (all learned the hard way):
1. **Read the prerequisite structure, not the titles** — hidden tracks surfaced in MLS, NUR and HSC.
2. **Check the department line** — `HSC3555` is taught by Biology, not the College of Health.
3. **Grep for `Communication Skills Requirement`**, `Permission is required`, `fee will be assessed`,
   `Co-requisite`, and `may be repeated` — all published inline, all easy to miss.
4. **Never assume a prefix repeats a sibling's structure** (rule 3o — confirmed twice now).

⚠ **Still outstanding: the `-SCNS` guides.** Open-cases table in `Tools/CLAUDE.md` now lists five
candidates: `NUR4286`, `NUR4826` (both with `-UWF` halves and disambiguation pages live), plus `ART3789C`,
`ART4800` and `HSC3102`. **All need the SCNS catalog from Ron.**

## Open items awaiting Ron

See `REVIEW_QUEUE.md` for the full detail. In short:

- **Items 1–3** — correction candidates on already-live guides (ETI4448, RTE2563C, EET1025C),
  each with a recommendation. None is urgent; all would be v1.1 republishes.
- **Item 4** — TPP2118/TPP2119 publish prerequisites naming a course DSC does not offer. One email
  to the theatre department settles it.
- **Item 9** — **updated batch 123, now the top open item**: six ANT `C`-suffix rows have no UWF coverage because UWF runs the
  split lecture+lab family instead. `ANT2511C` is at **15 institutions**, the highest-demand unwritten
  row in the prefix. Recommendation in `REVIEW_QUEUE.md` is skip five and defer `ANT2511C`. **The
  decision sets the rule for every UWF prefix that splits lecture from lab — PCB, MLS and EEL next.**

- **Items 5, 6, 8** — ⏸ on hold for Ron's 9xx usage data: PHT2931, the 44-row 9xx re-screen, and the
  six requirement-placeholder shells. **Item 6 is the highest-value item on the list.**
- **Item 7** — ✅ closed (PHT1006C resolved and published in batch 117).

---

## Operating agreement with Ron

Batches of 8–16 — researched, drafted, validated, pushed, verified. `"continue"` authorizes push
plus advance to the next batch. **Report per-course ⚠ flags, a running total, and institutional
progress with every push**, and persist the findings to `SOURCES.md` — Ron values these highly and
has said so repeatedly. **Queue coverage gaps are not critical errors.** Overwriting a live guide is
fine; the obligation is to increment the version (v1.0 → v1.1) and say so.

---

## ⚠ Read these three things before writing anything

### 1. DSC is canonical, and its catalog is directly fetchable (Tier 0)

Ron's standing decision (2026-09-02): *"We will stick with providing guides for the DSC
version, noting that the Valencia versions differ with notes on the differences."*

`daytona_courses.csv` has a `subject_page` for **all 1,266 DSC courses**, so every priority
course has a constructible catalog URL:

```
https://daytonastate.smartcatalogiq.com/en/2024-2025/college-catalog/course-descriptions/<subject_page>/<level>/<coursenum>/
```

`<level>` = first digit + `000` (HIM2800 → `2000`). `<coursenum>` = lowercased id with
C/L suffix. Drop the last element for the whole prefix index.

**Fetch the DSC page before writing any DSC course.** It gives title, credits,
prerequisites, description, term, lab fee. It does *not* usually give contact hours — those
still come from family consistency or a Tier-2 catalog. Full detail in `SOURCES.md` Tier 0.

### 2. Web search budget is exhausted — WebFetch is not

The 200-call search cap was hit mid-session. **WebFetch still works** and is not capped.
`SOURCES.md` → "Direct URL patterns" has the verified patterns (Broward and Valencia are the
workhorses; Valencia is the only reliable source for lecture/lab/clinical hour splits).
Assume search is unavailable until told otherwise.

### 3. Defer rather than guess

`python queue_mgr.py defer <IDS> --reason "..."` — added this session. Keeps the course
`queued`, moves it behind everything (priority +9000), records the reason.

- **Safe to derive:** values invariant across institutions (3-credit/45-hour upper-division
  lecture courses), or confirmed by an *internally consistent published family* here.
- **Not safe — defer:** PSAV clock-hour, clinical, studio/lab, and health-program courses,
  where the published family already shows real spread.

**Currently deferred (6):** `DEH1602`, `DES0103C`, `MEA0334C`, `STS1323C`, `MUS2360C`,
`OTH2300C`. Four have DSC pages and can be cleared immediately with Tier 0 — do this first,
it is quick and un-blocks real work.

---

## Open items, roughly in priority order

### A. Taxonomy — names ready to apply, hierarchy deferred by Ron

Ron reviewed and approved the first round; **179 prefix names were applied** to
`PreseMakerRepo.Api/Data/Seed/taxonomy.json` (his one edit: `EMC` = "Engineering: Mechanical
& Chemical", `EML` = "Engineering: Mechanical"). Backup at `taxonomy.json.bak2`.
`TaxonomySeed.cs:89` updates existing names on startup, so **a redeploy puts it live** — that
has not happened yet.

Then Ron supplied the **official SCNS handbook**
(`SCNS 2023-2024 Handbook Final_MAR 2024.pdf`), which is authoritative and supersedes the
derived names. Parsed to `scns_prefix_map.json` (611 prefixes, titles + official disciplines).

- **`TAXONOMY_SCNS_PROPOSAL.md`** — 390 differences: 93 substantive, 295 cosmetic.
  **Awaiting Ron's review.** Do not apply unilaterally; he reviewed the last set.
- It also corrects some of my own derivations — `MVH` is "Historical Instruments", not
  "Applied Music: Harp"; the `*W` family is "LITERATURE (WRITINGS)", not "and Film".
- **Hierarchy repair: Ron said explicitly "we can repair the hierarchy of disciplines later."**
  Six prefixes are mis-parented (`EML` under English; `MVH`/`MVJ`/`MVK`/`MVO` under Speech
  Pathology; `DEC` under Foreign Language Education). The handbook gives every prefix's
  official discipline, so names and parentage could be fixed in one pass when he is ready.

### B. Wrong-subject guides — a live error class

Three found and corrected so far: **MAN3554**, **HIM2283C**/**HIM2442**, **MUM2603**. Each was
about a *different course* than the one it claimed to be.

**`TITLE_AUDIT_VS_DSC.txt`** cross-checks all 381 published DSC guides against DSC titles.
44 mismatches, annotated to separate benign naming variants from likely scope errors.

**Six priority candidates** — short *and* mismatched, which is the signature (Rule 21):
`CJK0093` (7,939 chars), `CET2123C` (8,518), `ETI2949`, `ETI1411`, `PLA2610`, `PLA2600`.
Also worth a scope check: `ART2752C`, `DEA0020C` (published from Gulf Coast data, DSC not
checked), `RET1264C`, `RTE2854L` (DSC calls it Clinical Education **VI**, not V), `RTE2563C`,
`SON1100C`.

Ron said **"Lets start with the guides"** — so new batches take precedence, but these are
queued work whenever there is appetite.

### C. NEW TO-DO from Ron (2026-09-02): course drift

> *"As you have probably seen, there is a lot of drift in the courses from their original
> (and common) beginnings."*

This is the single most consistent finding across ~54 batches, and Ron wants it treated as a
named theme rather than scattered observations. It already underpins rules 14, 15, 17, 19, 20
and 21 in `SOURCES.md`. The forms it takes:

- **Title drift** — the queue title, DSC title, and other institutions' titles all differ
  (`MEA0334C` "Medical Office Procedures" vs DSC "Coding for Medical Assisting and Lab").
- **Content drift** — one number, genuinely different courses (`CGS2821C`: server-side
  programming at DSC, web *design* at FSCJ, multimedia elsewhere).
- **Scope drift** — a course narrowing or widening from its SCNS definition (`HIM2283C` is
  advanced *CPT* at DSC, not advanced coding generally).
- **Credit drift** — same number, different credits (HIM coding: 3 credits in one family,
  4 in another).
- **Parallel numbering families** — the most common structural finding; DAA, ASL, RTE, PMT,
  FSS, HIM, BCA all run two or more families for the same progression.
- **Sequence-position drift** — the roman numeral in a local title is unreliable
  (`RTE2844L` is "V" at some institutions, "IV" at others).

**Suggested next step** (not yet started): now that `scns_prefix_map.json` gives the official
SCNS prefix definitions, a systematic drift analysis is possible — compare what SCNS says a
prefix *is* against what institutions actually teach under it. That would turn scattered
flags into a documented account of how far Florida course content has moved from its common
origins. Worth proposing to Ron.

---

## Mechanics (unchanged, but easy to forget)

```bash
cd Tools
python queue_mgr.py next-batch --n 8          # pull the batch
# ... fetch DSC page(s), research, write drafts/{ID}_guide.json ...
python queue_mgr.py reconcile
python validate_drafts.py --drafted            # never push past a FAIL
python generate_guide.py --push-from-queue --yes
echo "y" | python generate_guide.py --push-draft <ID>    # single re-push (corrections)
python queue_mgr.py defer <IDS> --reason "..."           # cannot verify
```

- Write guide-building scripts to the **scratchpad** and run them as files. Bash heredocs
  fail with `ENAMETOOLONG` or quoting errors on large guides — this has bitten repeatedly.
- **`prerequisites` ≤ 500 chars** is the recurring validation failure. Check before pushing.
- Verification is via `generate_guide.log` (`PUSH: Success`) — the public API does not expose
  guide content, so don't try to GET it back.
- Totals script is in `SOURCES.md`; Daytona progress comes from `daytona_courses.csv`.

## Guide conventions worth preserving

Every guide since the level correction carries a **"How Florida course levels affect
transfer"** block. Ron corrected a rule I had been propagating: **1000↔2000 transfer
transparently** (the first digit is the *year of offering*), **2000→3000 is the problematic
step**, 3000→4000 is fine, PSAV does not transfer. Reserve level-based transfer warnings for
2000→3000 and PSAV→credit; for same-division differences frame it as *which number a program
requires*. Seven guides were corrected for this — see `SOURCES.md`.

Ron reads these carefully and specifically values the **⚠ flags** — the safety, legal,
career-honesty and "here is the thing nobody tells you" notes. That is the part to keep
investing in.
