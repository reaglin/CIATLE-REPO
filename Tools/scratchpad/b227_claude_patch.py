"""Batch 227 edits to Tools/CLAUDE.md. Run once from Tools/scratchpad."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


# --- 1. Sixth prerequisite-defect shape: PROSE instead of an identifier -----
rep(
"""| **Local title in a statewide field** (200) | `COM4564` — *"COM4561 Social Media Content Development"* | the quoted title is not the statewide title | ⚠ **search by NUMBER**; and read it in reverse — it names the CONTRIBUTING institution |""",
"""| **Local title in a statewide field** (200) | `COM4564` — *"COM4561 Social Media Content Development"* | the quoted title is not the statewide title | ⚠ **search by NUMBER**; and read it in reverse — it names the CONTRIBUTING institution |
| ⚠⚠ **PROSE instead of an identifier** (227) | **`GRA2508C` — *"BASIC DESIGN OR CONSENT OF INSTRUCTOR"*** | ⚠⚠ **there is NO course-looking token at all, so the batch-209 syntax test never fires — the field names a SUBJECT, not a course** | **say there is no such course to find, give the carrier's REAL gate** (`DIG 2000C OR DIG 3001C`), **and send the reader to their own catalogue** |

⚠⚠ **Note what the sixth shape breaks: every earlier test scans course-looking TOKENS. A prerequisite
made of prose has none, so it passes every check while telling the reader nothing actionable.** **Add
the question "does this field name a COURSE at all?" before running the token tests.**""")

# --- 2. Misfiling by necessity: a new CAUSE (sequence length) ---------------
rep(
"""| Case | The gap the carrier was working around |
|---|---|
| `JOU4306` (UF) | no ADVANCED data journalism number exists |
| `PET4434` + `PET4820` (UWF) | no sport-pedagogy-by-age-band number exists at undergraduate level |""",
"""| Case | The gap the carrier was working around |
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
second, the surplus courses are misfiled by arithmetic.""")

# --- 3. A title divergence that DISSOLVES ----------------------------------
rep(
"""#### ⚠⚠⚠ THE TITLE/DESCRIPTION TEST — run it before looking at carriers (batch 208)""",
"""#### ⚠⚠⚠ THE NEGATIVE RESULT: A TITLE DIVERGENCE THAT DISSOLVES — check it BEFORE writing a divergence block (batch 227)

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

#### ⚠⚠⚠ THE TITLE/DESCRIPTION TEST — run it before looking at carriers (batch 208)""")

# --- 4. Single-carrier: statewide agreement is NOT corroboration -----------
rep(
"""#### ⚠⚠ A statewide description with an embedded institution list or a YEAR is a historical record (batch 208)

**`SSE4113`'s description ends *"INSTITUTIONS: FAMU, FAU, FSU, UWF 1988"*; `SYO4530`'s ends with nine
institutions and *"6/83"*.** In both cases the list no longer matches who offers the course.""",
"""#### ⚠⚠⚠ ON A SINGLE-CARRIER COURSE, STATEWIDE AGREEMENT IS NOT EVIDENCE (batch 227)

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

⚠⚠⚠ **PROVED rather than inferred (batch 227): `GRA2508C`'s description ends *"INSTITUTIONS: FAMU
1988"* — and FAMU does NOT carry the number today, while UWF DOES.** **One flat-file lookup turns
this rule from a reasonable suspicion into a demonstrated fact, and it is worth doing** — a guide can
then tell the reader the state record is stale instead of hedging about it.

⚠ **`GRA2508C` also carries an administrative marker INSIDE the statewide title — `COLOR AND COLOR
THEORY(RES 2008)` — appearing on exactly three `GRA` numbers, all stamped the same year.** **Strip
such a marker from the course NAME, say it is administrative, and do NOT guess at what it means.**
(Compare the `ATF` titles, where the parenthesised content is real hour data — **read the title as a
data field, but do not assume every parenthesis carries student-facing information.**)""")

# --- 5. Stratify by the population the FIELD applies to --------------------
rep(
"""#### ⚠⚠⚠ COMPUTE THE FIELD'S DISTRIBUTION ACROSS THE PREFIX BEFORE TREATING IT AS A SIGNAL (batch 207)""",
"""#### ⚠⚠⚠ STRATIFY BY THE POPULATION THE FIELD APPLIES TO — and get the FINDING from SIBLINGS (batch 227)

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

#### ⚠⚠⚠ COMPUTE THE FIELD'S DISTRIBUTION ACROSS THE PREFIX BEFORE TREATING IT AS A SIGNAL (batch 207)""")

# --- 6. Private-carrier title in the inventory: third instance -------------
rep(
"""`COM2713` reads *"Writing for Strategic Communication"* (batch 222) and `CNT3112` reads *"Advanced Network Administration"* (batch 226), **both the private carrier's title rather than the statewide or public one.** **Two instances make it a recurring failure mode; tell the reader to register by NUMBER.** |""",
"""`COM2713` reads *"Writing for Strategic Communication"* (batch 222), `CNT3112` reads *"Advanced Network Administration"* (batch 226) and `GRA4882C` reads *"Analysis of Trends and Styles"* (batch 227) — **the statewide title, which in Florida only a PRIVATE institution actually uses.** ⚠⚠ **THREE instances now; treat it as expected rather than notable, and tell the reader to register by NUMBER.** ⚠ **`GRA2508` adds the mirror case: the BARE form is private-only while the `C` form is the public one** (the `PET3344` shape inverted) — **so check the sector of every carrier before describing a bare/`C` pair.** |""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')
