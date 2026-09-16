"""Batch 224 edits to Tools/CLAUDE.md and REVIEW_QUEUE.md. Run once from Tools/scratchpad."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, '..', 'CLAUDE.md')
RQ = os.path.join(HERE, '..', 'REVIEW_QUEUE.md')
s = io.open(P, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


# --- 1. Same-institution control works in BOTH directions -------------------
rep(
"""⚠ **The check is cheap: on finding a suspected misfiling, scan the carrier list of the
suspected-correct number for an institution that ALSO carries the number in question.** Often one is
already there.""",
"""⚠ **The check is cheap: on finding a suspected misfiling, scan the carrier list of the
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

⚠⚠ **So the control is not a misfiling detector; it tests whether the carrier is WORKING the
state's scheme.** **A carrier that files everything else correctly and deviates on one number is
telling you the scheme has a GAP, not that the carrier is sloppy.** **Run it before writing a
misfiling warning, and be willing to conclude that nobody is at fault** — the student's problem is
real either way, which is why the transfer advice should lead rather than the adjudication.

⚠⚠ **Related caution: THE DEDICATED-NUMBER TELL IS MUCH WEAKER WHEN THE DEDICATED NUMBER IS
DORMANT.** On `JOU4306` dedicated numbers exist for BOTH readings — `JOU4305` Data Journalism and
`JOU4015` Journalism Culture and Criticism — **and NEITHER has a carrier.** **A carrier cannot be
faulted for not moving to a number nobody uses.** **Check the carrier count on the "correct" number
before relying on the tell.**""")

# --- 2. Fifth branch of the title/description test --------------------------
rep(
"""4. ⚠⚠⚠ **They DISAGREE and the CARRIERS SPLIT, one on each side** → **the test returns NO ANSWER, and the
   number is carrying TWO SUBJECTS** (`HFT4252`, batch 218).""",
"""4. ⚠⚠⚠ **They DISAGREE and the CARRIERS SPLIT, one on each side** → **the test returns NO ANSWER, and the
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
version, gated on nothing means criticism.""")

# --- 3. Worst dangling case, appended to the five-shapes table ---------------
rep(
"""⚠⚠⚠ **Batch 222 REMOVES a precondition from the batch-221 rule.**""",
"""⚠⚠⚠ **WORST CASE FOUND (batch 224): `JOU3342`'s statewide prerequisite is "JOU 3101 AND RTV
4301". UWF carries `JOU3101` but not `RTV4301`; UNF carries NEITHER.** **`RTV4301` is carried by FAU
and UF and `JOU3101` by USF, FAU, UWF and UF — so the two institutions that COULD satisfy the
prerequisite do not carry the course at all.** ⚠⚠ **The prerequisite was contributed by a
department that does not teach the course.**

⚠⚠⚠ **Batch 222 REMOVES a precondition from the batch-221 rule.**""")

# --- 4. Two-subject guides still owe the canonical structure -----------------
rep(
"""**Omit a section rather than fabricate.**""",
"""⚠⚠ **A TWO-SUBJECT GUIDE STILL OWES THE CANONICAL STRUCTURE (batch 224).** When a number carries
two readings, it is tempting to give each reading its own `<h2>` with outcomes and topics nested
inside. ⚠ **`JOU4306` was drafted that way and `validate_drafts.py` correctly warned that the guide
had no `Learning Outcomes` and no `Major Topics` section at all.** **Label the readings INSIDE the
canonical sections, not instead of them**: each reading's prose as an `<h3>` in Course Description,
then both outcome lists under one `<h2>Learning Outcomes</h2>` and both topic lists under one
`<h2>Major Topics</h2>`, with the reading named on every list.

**Omit a section rather than fabricate.**""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')

# --- REVIEW_QUEUE item 101 --------------------------------------------------
r = io.open(RQ, encoding='utf-8').read()
new = io.open(os.path.join(HERE, 'b224_review.md'), encoding='utf-8').read()
anchor = '\n## Resolved\n'
assert anchor in r
io.open(RQ, 'w', encoding='utf-8').write(r.replace(anchor, new + anchor, 1))
print('REVIEW_QUEUE item 101 inserted')
