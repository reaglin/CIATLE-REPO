"""Batch 225 edits to Tools/CLAUDE.md. Run once from Tools/scratchpad."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


# --- 1. Misfiling by necessity: now an established pattern with handling ----
rep(
"""⚠⚠ **So the control is not a misfiling detector; it tests whether the carrier is WORKING the
state's scheme.**""",
"""⚠⚠⚠ **THIRD INSTANCE, and the pattern is now established: MISFILING BY NECESSITY (batch 225).**
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

⚠⚠ **Settled handling for this shape: say there is NO "correct" number to go looking for, and lead
with the transfer advice rather than the adjudication.** **The student's problem is real whoever is at
fault, and "send the syllabus" is actionable where "your institution is misfiling" is not.**

⚠⚠ **So the control is not a misfiling detector; it tests whether the carrier is WORKING the
state's scheme.**""")

# --- 2. Read one institution's descriptions against EACH OTHER --------------
rep(
"""### ⚠⚠ SURVEY THE PREFIX FAMILY from the statewide CSV before writing — a standing move (batch 200)""",
"""⚠⚠⚠ **AND READ ONE INSTITUTION'S DESCRIPTIONS AGAINST EACH OTHER, not only against the state (batch 225)**

**Every test in this file compares a CARRIER to the STATE.** ⚠⚠ **Batch 225's headline finding was
invisible to all of them:** UWF's `PET4434` and `PET4820` descriptions are identical but for four
words, **and their statewide titles are completely different**, so no title-comparison or
title/description test would ever fire.

⚠ **It was found by reading the UWF PDF output directly and noticing two entries several lines
apart.** **Standing move: when one institution carries several courses in a prefix, diff its
descriptions against EACH OTHER.** **An institution's internal coherence is evidence in its own right
— a matched pair, a deliberate sequence, or a copied description all show up this way and nowhere
else.**

### ⚠⚠ SURVEY THE PREFIX FAMILY from the statewide CSV before writing — a standing move (batch 200)""")

# --- 3. Private-only shape stated symmetrically -----------------------------
rep(
"""⚠⚠ **The batch-222 row is a SCOPE fact, not a catalogue fact, and it needs the opposite handling
from "a `C` nobody carries."**""",
"""⚠⚠⚠ **AND IT RUNS IN BOTH DIRECTIONS (batch 225).** `COM4564C` was a private-only **`C`** form
with a public bare twin. **`PET3344` is the mirror: the BARE number is carried only by a private
institution and the `C` form, `PET3344C`, is the public one.** ⚠ **So state the check symmetrically:
look up which FORM the PUBLIC carrier uses, in either direction.** **The instinct that an unsuffixed
number is the "default" is wrong as often as it is right** — on `PET3344C` no substitution was needed
because the queued `C` id was already the public one.

⚠⚠ **The batch-222 row is a SCOPE fact, not a catalogue fact, and it needs the opposite handling
from "a `C` nobody carries."**""")

# --- 4. Transferability can be a coherent cluster ---------------------------
rep(
"""⚠⚠⚠ **Strengthened (batch 204): it is NOT a support-coursework flag.**""",
"""⚠⚠⚠ **AND IN SOME PREFIXES IT IS A COHERENT CLUSTER, not scattered exceptions (batch 225).**
**`PET` has 13 NOT-AUTOMATICALLY-TRANSFERABLE rows among 122 active undergraduate numbers — about
11%, against 2/171 in `CCJ` and 5/124 in `INR`.** ⚠⚠ **And they group:** athletic training clinical
courses (`PET4672`, `PET4673`, `PET4624`, `PET4625`, `PET4627`), exercise testing and fitness
assessment (`PET4550`, `PET4551`, `PET3385`), and `PET4765`.

⚠ **That is the batch-215 licensed-profession logic surfacing in the transferability field:
hands-on clinical and assessment coursework where a receiving programme must attest to competence
ITSELF and cannot do so on another institution's credit.** **Where the stratified count is well above
the ~2% norm, look for the cluster before calling it noise — and tell the reader which KIND of course
is affected rather than listing numbers.**

⚠⚠⚠ **Strengthened (batch 204): it is NOT a support-coursework flag.**""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')
