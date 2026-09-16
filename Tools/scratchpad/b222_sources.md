
---

## Batch 222 — COM (communication), 2026-09-16

Six guides, all live: **COM2713**, **COM3471**, **COM4110**, **COM4120**, **COM4301**, **COM4564**.
All 3 credits, no suffix, **45 contact hours**. **6 clean, 0 warnings, 0 blocking**; 0 of 6
prerequisites over the limit. COM was already listed (341 courses, unchanged).

⚠ **Five of the six were queued rows. The sixth is a documented substitution — see below.**

**Prefix shape**: **370 live ids, 308 single-carrier (83%)**, max **10** carriers. ⚠⚠ **83% is the
HIGHEST single-carrier share of the sixteen prefixes now measured** (`SSE` and `SYP` were 85% on
smaller prefixes; `COM` is large at 370 ids). **A communication course transferring cleanly by number
is close to an exception.**

### ⚠⚠⚠ `COM4564C` — a FIFTH outcome for the C-suffix diagnostic: the PRIVATE-ONLY C form

**The queued row was `COM4564C`. Running the batch-219 rule — look up the bare number before writing
any `C` id — produced an outcome the rule's three-row table does not cover.**

| Id | Carriers | Sector |
|---|---|---|
| **`COM4564C`** (queued) | **1** | ⚠⚠⚠ **Keiser University — PRIVATE. Zero public carriers.** |
| **`COM4564`** (bare) | **1** | ✅ **UWF — public** |

⚠ **Under Ron's 2026-09-11 scope rule a private institution's offering is not a reason to write a
guide, and the override is applied by QUEUEING a course after a visitor request — the request queue
is empty.** **So the queued identifier is unwritable as queued.**

**What was done, and it is recorded rather than silent:**

- **`COM4564C` marked `skipped`** in `queue.csv` with the reason written into the note field.
- ⚠⚠ **`COM4564` written instead** — **same statewide title, same statewide description, same
  subject**; it is the course the queue row named. `reconcile` picked it up as an orphan draft and
  added the row automatically.
- **The guide tells the reader directly**: do not register for the `C` version, no Florida public
  institution offers it, and the suffix carries no meaning for a public student here.

⚠⚠ **Why this is a distinct outcome rather than "a `C` nobody carries" (batch 183):** **somebody does
carry it.** The identifier is real and in use. **It simply has no carrier this project may write
from** — which is a scope fact, not a catalogue fact, and it needs the opposite handling: *write the
bare number and explain the suffix*, rather than *check whether the id exists at all*.

⚠ **The batch-219 diagnostic table now has five rows.** Added to `CLAUDE.md`.

### ⚠⚠ Another inventory artefact from the same cause: a PRIVATE carrier's title in the queue

**`COM2713`'s queue row reads `WRITING FOR STRATEGIC COMMUNICATION`.** ⚠ **That is neither the
statewide title nor the public carrier's title — it is the PRIVATE carrier's.**

| Source | Title |
|---|---|
| Florida statewide | Writing for the Communication Professions |
| **UWF** (only public carrier) | **Introduction to the Communication Professions** |
| ⚠ a private carrier | *Writing for Strategic Communication* |

**The descriptions agree almost word for word, so there is no subject divergence** — three names, one
course, and the guide says so and tells the reader to register by number. ⚠ **But it extends the
inventory-reliability caution in the source register: `courses_2plus_institutions.csv` can carry a
PRIVATE institution's title as the course's name**, which is a second failure mode alongside the
already-recorded wrong-institution and spurious-suffix ones.

### ⚠⚠⚠ DEFECTIVE STATEWIDE PREREQUISITES — `COM` supplies two more shapes, and the taxonomy is now complete enough to table

**This prefix produced two distinct defects in one batch, and together with batches 200, 209, 219 and
221 there are now five recognised shapes.**

| Shape | Worked example | Tell | Handling |
|---|---|---|---|
| **Corrupt token** (batch 209) | `ADV4802` — *"ADV U101C"* | fails `^[A-Z]{3}\s?\d{4}[A-Z]?$` | say it is a data defect; send the reader to the catalogue |
| ⚠⚠ **PLACEHOLDER** (batch 222) | **`COM4301` — *"COM 2XXX Introduction to Communication Studies"*** | ⚠ **`2XXX` is a wildcard that was never filled in** | **the INTENT is legible and usually good advice — state the intent, say the number does not exist** |
| **Dangling: sector split** (batch 221) | `PLA4554` — names `PLA 1003` AND `PLA 2203`, both FCS-only | prefix splits FCS/SUS | name the real gate; expect it whenever a prefix splits by sector |
| ⚠⚠ **Dangling: single-carrier contribution** (batch 222) | **`COM4120` — names `COM 3311`, carried by UCF ALONE — and UCF does not require it** | ⚠ **both carriers are SUS; no sector split involved** | **simpler cause: ONE carrier contributed the entry and it does not resolve at the other** |
| **Local title in a statewide field** (batch 200) | `COM4564` — *"COM4561 Social Media Content Development"* | the quoted title is not the statewide title | ⚠ **search by NUMBER; and use it in reverse — it identifies the contributing institution** |

⚠⚠⚠ **The batch-222 dangling case matters because it REMOVES a precondition from the batch-221 rule.**
Batch 221 concluded that a sector split causes prerequisites to dangle. **`COM4120` shows the simpler
and more general cause: any prerequisite contributed by one carrier may fail to resolve at another,
sector split or not.** **The sector split makes it systematic; it is not required for it to happen.**

⚠ **`COM4564` also CONFIRMS the batch-200 local-title finding with the carrier list behind it**, which
batch 200 could only infer: **`COM4561` runs under three different titles** — statewide *Social Media
Campaigns*, UWF *Social Media Content Development*, UNF *Strategic Social Media*, FSU matching the
statewide one. **The statewide prerequisite quotes UWF's, confirming UWF contributed the entry — which
is consistent with UWF being the only carrier of `COM4564`.**

### ⚠⚠ A restricted-enrolment gate that blocks exactly the students who most need the course

**`COM4110` at UCF is limited to students active in Communication, Human Communication,
Advertising/Public Relations, Communication and Conflict, Media Production and Management or
Radio-Television majors, or Communication, Human Communication or Strategic Communication minors** —
plus a further course requirement.

⚠⚠⚠ **The irony is worth stating in the guide and it is stated: a business, engineering or science
student is exactly who benefits most from a professional-speaking course, and is exactly who cannot
enrol.** The guide names the alternative (UCF's open `SPC` public speaking numbers) and tells the
reader to ask the Nicholson School.

⚠ **Fourth instance of the batch-188 restricted-enrolment shape**, after `ENG3010`, `RTV3511` and
`APK4163`. **It goes in the prerequisite field, because it determines whether a term can be planned
around the course at all.**

### ⚠ Emphasis divergences worth the two-column treatment

| Course | The split | Verdict |
|---|---|---|
| **`COM4110`** | UCF *"presentational speaking"* (**agrees with the statewide title AND description**) vs UWF's six-component workplace survey | ⚠ **NOT misfiling — UWF's is a superset that fully contains the statewide subject.** Scope breadth. Syllabus test: **count the graded speeches.** |
| **`COM4301`** | UNF matches the statewide title (theory + methods, academic) vs UWF *Applied Communication Research* for the *"converged communication industry"* | ⚠⚠ **Materially different preparation. Graduate admissions read this course as evidence you can do research; the applied version is not the same signal.** Syllabus test: **APA research report, or client insights deck?** |
| **`COM3471`** | identical subject, but UWF gates it on `COM2713` and it gates `COM4561`→`COM4564`; FIU has nothing published either side | ⚠ **the prerequisite-chain diagnostic revealing FUNCTION rather than subject** — foundational at UWF, terminal at FIU |
| **`COM4120`** | UCF/statewide internal (*"contexts of hierarchies"*) vs UWF internal **plus stakeholders**, case-based | mild; both squarely within the statewide description |

⚠ **`COM3471` is a useful extension of the batch-175 diagnostic.** That rule reads the prerequisite
chain to settle whether two institutions teach different **subjects**. **Here the subject was never in
doubt and the chain revealed the course's ROLE instead.** **UWF's title word — "Fundamentals" — is a
statement about position, not about difficulty.**

### ⚠ The UWF social media sequence, recovered in full

**One PDF parse produced a complete four-course chain with its gates, which is unusually clean:**

`COM2713` → `COM3471` → `COM4561` → `COM4564`, with **`COM3003`** required alongside and
**75 completed credit hours** for the last.

⚠⚠ **`COM3003` is the split number from batch 175** — statewide *Human Communication* (theory survey),
UWF *Integrated Advertising and Public Relations Concepts*. **All three pages are already live
(`-SCNS`, `-UWF`, bare).** **The `COM4564` guide points at them and says which reading the
prerequisite means** — the first time in this project that a published split has been cited as a
prerequisite in a later guide, and a good argument for having done the split properly.

⚠ **The 75-credit-hour standing requirement is the practical trap**: it is not a course, it does not
appear in a prerequisite list, and it blocks registration outright. **Stated in the prerequisite
field.**

### Sources used

| Source | What it gave |
|---|---|
| **SCNS flat file** + `survey.py` | carriers and sectors — ⚠ **including the private-only finding that decided the batch's scope call** |
| **`sw_COM.csv`** | descriptions, and both defective prerequisites |
| **UWF** `uwf_com.pdf` via `uwf_pdf.py` | full entries for all six plus `COM4561` — the whole sequence in one fetch |
| **UCF Kuali** | `COM4110`/`COM4120`/`COM3311` descriptions, the **major restriction**, the Honors section, Fall/Spring, 0 lab hours |
| **FIU Coursedog cache** | `COM3471` |
| ❌ **UNF** | unreachable, as recorded — blocks `COM4301`'s second carrier |

### ⚠ Gordon Rule, machine-read and confirmed by the catalogue

**Two of the six carry designations at UWF, and the flat file and the catalogue agree:**

| Course | Flat-file flags | UWF catalogue |
|---|---|---|
| `COM2713` | `gordon_rule`, `gordon_writing` | *"Meets College-Level Communication Skills Requirement"* |
| `COM4301` | `gordon_rule`, `gordon_writing` | *"Meets College-Level Communication Skills Requirement"* |

✅ **The batch-179 mapping holds** — UWF's "Communication Skills" label is the Gordon Rule **writing**
half. ⚠ **Both guides state the C-or-higher condition**, which is the part students do not know, and
⚠ **`COM4301` is where it bites hardest: a methods course is exactly the one a student is most likely
to scrape through with a C-minus.**
