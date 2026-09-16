"""Batch 223 edits to Tools/CLAUDE.md. Run once from Tools/scratchpad."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


# --- 1. The same-institution control: a decisive misfiling diagnostic -------
rep(
"""#### ⚠⚠ When MOST carriers misfile, the state is still the reference — but say so carefully (batch 208)""",
"""#### ⚠⚠⚠ THE SAME-INSTITUTION CONTROL — the one test that SETTLES a misfiling (batch 223)

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

⚠⚠ **And state the qualification honestly where one exists.** UWF's course is not simply the wrong
subject — it contains position papers, committee procedure and a simulation. **What differs is the
frame: at UWF the simulation serves a course about institutions; at FAMU the course serves the
simulation.** **Say that, and give the student the actionable answer** — for `INR3503`, *join the Model
UN team if you want competition experience.*

#### ⚠⚠ When MOST carriers misfile, the state is still the reference — but say so carefully (batch 208)""")

# --- 2. SPM3104 shape: second instance, with the graduate-only twist --------
rep(
"""⚠ **The drill: when a statewide title contains a conjunction ("X and Y"), check that the statewide
DESCRIPTION delivers both halves, and check whether Y has its own number that nobody carries.**""",
"""⚠ **The drill: when a statewide title contains a conjunction ("X and Y"), check that the statewide
DESCRIPTION delivers both halves, and check whether Y has its own number that nobody carries.**

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
warning is not.**""")

# --- 3. FSU parsing: identifier split across tags ---------------------------
rep(
"""| **⚠ FSU entry vs requirement text** | `registrar.fsu.edu/bulletin/...` | ⚠ A number followed by a period is **not** enough to locate a catalog entry — it also matches requirement prose (*"a grade of C or higher in COP 3014 or COP 3363."*). **Verify that a TITLE and a parenthesised credit value follow** (`COP 3014. Algorithm… (3).`). Cost a wrong result in batch 176. |""",
"""| **⚠ FSU entry vs requirement text** | `registrar.fsu.edu/bulletin/...` | ⚠ A number followed by a period is **not** enough to locate a catalog entry — it also matches requirement prose (*"a grade of C or higher in COP 3014 or COP 3363."*). **Verify that a TITLE and a parenthesised credit value follow** (`COP 3014. Algorithm… (3).`). Cost a wrong result in batch 176. ⚠⚠ **AND THE IDENTIFIER MAY NOT BE CONTIGUOUS IN THE HTML (batch 223):** FSU splits it across tags — `<strong>INR </strong><strong>4124. </strong>` — **so a grep for `INR 4124` finds nothing although the entry is there.** **Strip tags and collapse whitespace BEFORE searching.** |""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')
