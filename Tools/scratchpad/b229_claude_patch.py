"""Batch 229 edits to Tools/CLAUDE.md. Run once from Tools/scratchpad."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


# --- 1. A gap FRAGMENTS rather than displaces ------------------------------
rep(
"""⚠⚠ **Settled handling for this shape: say there is NO "correct" number to go looking for, and lead
with the transfer advice rather than the adjudication.** **The student's problem is real whoever is at
fault, and "send the syllabus" is actionable where "your institution is misfiling" is not.**""",
"""⚠⚠ **Settled handling for this shape: say there is NO "correct" number to go looking for, and lead
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
`MUE4332` and `MUE4493` all carrying instrumental methods under different statewide subjects.""")

# --- 2. Same-institution control: a THIRD outcome, EXPLAINS ----------------
rep(
"""⚠⚠ **So the control is not a misfiling detector; it tests whether the carrier is WORKING the""",
"""#### ⚠⚠⚠ A THIRD OUTCOME OF THE CONTROL: it can EXPLAIN a divergence rather than judge it (batch 229)

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

⚠⚠ **So the control is not a misfiling detector; it tests whether the carrier is WORKING the""")

# --- 3. Prerequisite diagnostic: a fourth thing it settles -----------------
rep(
"""| `ACG4180` | **finance**, not accounting | taught from the statement USER's side |""",
"""| `ACG4180` | **finance**, not accounting | taught from the statement USER's side |
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
disguise, and the prerequisite is where the disguise comes off.""")

# --- 4. A contributor can drift from its own contribution ------------------
rep(
"""⚠⚠⚠ **PROVED rather than inferred (batch 227): `GRA2508C`'s description ends *"INSTITUTIONS: FAMU""",
"""⚠⚠ **THE SHORTEST FORM IS A BARE INSTITUTION CODE, and all three targets in batch 229 had one.**
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

⚠⚠⚠ **PROVED rather than inferred (batch 227): `GRA2508C`'s description ends *"INSTITUTIONS: FAMU""")

# --- 5. Abbreviated matrix titles are not course names --------------------
rep(
"""### ⚠⚠ The statewide TITLE is a data field — read it for parenthesised hour figures (batch 200)""",
"""### ⚠⚠⚠ A statewide TITLE can be a MATRIX CODE rather than a name — expand it (batch 229)

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

### ⚠⚠ The statewide TITLE is a data field — read it for parenthesised hour figures (batch 200)""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')
