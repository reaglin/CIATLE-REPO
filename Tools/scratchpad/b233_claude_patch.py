"""Batch 233 edits to Tools/CLAUDE.md."""
import io, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)

# 1. Seventh prerequisite-defect shape: names numbers NOBODY carries
rep("""| \u26a0\u26a0 **PROSE instead of an identifier** (227) | **`GRA2508C` \u2014 *"BASIC DESIGN OR CONSENT OF INSTRUCTOR"*** | \u26a0\u26a0 **there is NO course-looking token at all, so the batch-209 syntax test never fires \u2014 the field names a SUBJECT, not a course** | **say there is no such course to find, give the carrier's REAL gate** (`DIG 2000C OR DIG 3001C`), **and send the reader to their own catalogue** |""",
"""| \u26a0\u26a0 **PROSE instead of an identifier** (227) | **`GRA2508C` \u2014 *"BASIC DESIGN OR CONSENT OF INSTRUCTOR"*** | \u26a0\u26a0 **there is NO course-looking token at all, so the batch-209 syntax test never fires \u2014 the field names a SUBJECT, not a course** | **say there is no such course to find, give the carrier's REAL gate** (`DIG 2000C OR DIG 3001C`), **and send the reader to their own catalogue** |
| \u26a0\u26a0\u26a0 **Dangling for EVERYBODY** (233) | **`PHY4445` \u2014 *"PHY 3054 OR PHY 3049"*** | \u26a0\u26a0\u26a0 **BOTH alternatives have ZERO public carriers in the whole state** \u2014 well-formed identifiers naming nothing anyone can enrol in | **say the gate is unusable, give the carrier's real one, and \u26a0 CHECK WHAT THE REAL GATE ADDS** \u2014 UWF's is `MAC 2313 AND MAP 2302 AND PHY 2049` with a C\u2212 floor, **and differential equations appears nowhere in the state record** |

\u26a0\u26a0 **The seventh shape is the extreme of dangling and the check is one flat-file pass.** Batch 219's
`TPA4021C` named a number that belonged to OTHER schools; **this one names two numbers that belong to
nobody.** **So run the carrier count on every token, not just on the carrier you are writing about** \u2014
a zero means the gate cannot be satisfied by any student in Florida.""")

# 2. Credit divergence -> check for a repeat allowance
rep("""### \u26a0 CREDIT-COUNT divergence \u2014 a fourth shape, and invisible from the identifier (batch 185)""",
"""### \u26a0\u26a0\u26a0 BEFORE CALLING A CREDIT DIVERGENCE A DEPTH DIFFERENCE, CHECK FOR A REPEAT ALLOWANCE (batch 233)

**`PHY4822L` runs at 3 credits at UWF and 2 at Florida State, which reads as one institution doing less.
It is not \u2014 it is a different PACKAGING of the same course:**

| | UWF | Florida State |
|---|---|---|
| Credits | **3** | **2** |
| Repeatable? | \u26a0 **No** \u2014 3 credits is all there is | \u26a0\u26a0 **Yes \u2014 to a maximum of 6 credit hours**, *"for special projects arranged in advance"* |
| Catalogued as | `PHY4822L` | \u26a0 **`PHY 4822Lr`** \u2014 the `r` marks repeatability in FSU's notation |

\u26a0\u26a0\u26a0 **FSU runs a smaller unit a committed student takes three times, reaching SIX credits and doing
self-directed projects; UWF runs one larger block and stops.** **The institution with FEWER credits per
enrolment offers MORE credit in total, and the better route into a graduate application.**

**So the rule: a lower credit value is not evidence of a shallower course until you have checked whether
it repeats.** \u26a0 **The tell is cheap** \u2014 a repeat clause in the credit line, or a suffix convention like
FSU's `r`. **Read the credit line, not just the number.**

\u26a0 **And say what it means for the student rather than just recording it:** where a course repeats, the
guide should tell the reader the allowance exists, that a special project is the thing worth doing with
it, and to confirm how many repeats their own degree will count (Florida's excess-hours provisions
still apply).

### \u26a0 CREDIT-COUNT divergence \u2014 a fourth shape, and invisible from the identifier (batch 185)""")

# 3. Prerequisite confirms sequence position
rep("""### \u26a0\u26a0 CHECK WHETHER A CREDIT DIVERGENCE IS A PREFIX-WIDE INSTITUTIONAL PATTERN (batch 230)""",
"""### \u26a0\u26a0\u26a0 THE PREREQUISITE IDENTIFIES A COURSE'S POSITION IN THE SEQUENCE \u2014 read it before the title (batch 233)

**`PHY3106` is statewide *Modern Physics I*. FIU teaches exactly that. \u26a0\u26a0 UWF titles it
*Calculus-Based Physics III* and teaches the THIRD TERM OF THE INTRODUCTORY SEQUENCE** \u2014 adding
thermodynamics and wave phenomena, which are classical, and not mentioning quantum mechanics.

\u26a0\u26a0\u26a0 **The prerequisite settles it in one line, and it is a general test:**

| | Statewide / FIU | UWF |
|---|---|---|
| Gate | `PHY 2049` or `PHY 2054` **AND `MAC 2313` (Calculus III)** | \u26a0 **`PHY 2049` only** |
| Therefore | positioned **ABOVE** the introductory sequence | positioned **INSIDE** it |

**A course sitting inside an introductory sequence CANNOT require the mathematics that sequence has not
reached yet.** **So where two carriers of one number disagree about level, compare the gates: the one
demanding later mathematics is the later course.** \u26a0 **This is the prerequisite-as-signal diagnostic
firing on POSITION** \u2014 alongside subject (175), depth (185), emphasis (187) and sequence position in
`MUE4411` (229).

\u26a0\u26a0 **And the content diverged at BOTH ends, which is what makes it consequential:** the UWF student has
thermodynamics and waves the FIU student does not, and may not have the **Schr\u00f6dinger equation** the FIU
student does. **Tell the reader to send a TOPIC LIST on transfer and name both checks explicitly** \u2014
physics departments place by coverage, and "did you do the Schr\u00f6dinger equation?" is the question.

### \u26a0\u26a0 CHECK WHETHER A CREDIT DIVERGENCE IS A PREFIX-WIDE INSTITUTIONAL PATTERN (batch 230)""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')
