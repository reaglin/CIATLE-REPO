"""Batch 226 edits to Tools/CLAUDE.md. Run once from Tools/scratchpad."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


# --- 1. Externally-governed curriculum: commercial vendor variant -----------
rep(
"""**Expect this shape in:** the other services' ROTC prefixes, nationally standardised certification
curricula, apprenticeship-linked coursework, and anywhere a national body **issues** the syllabus rather
than approving one.""",
"""**Expect this shape in:** the other services' ROTC prefixes, nationally standardised certification
curricula, apprenticeship-linked coursework, and anywhere a national body **issues** the syllabus rather
than approving one.

#### ⚠⚠⚠ THE COMMERCIAL-VENDOR VARIANT — and how to DETECT it (batch 226)

**`CNT3112` is the same shape with a VENDOR in place of a national body, and it is probably the
commoner form.** Convergent evidence:

| Evidence | Detail |
|---|---|
| Statewide title | *Routing and Switching Essentials* — ⚠ the EARLIER Cisco CCNA module 2 name |
| UWF title | *Switching, Routing and Wireless Essentials* — ⚠ the CURRENT module 2 name |
| Description delta | UWF's is the statewide text **plus wireless** — ⚠⚠ **exactly the documented v6→v7 restructure** |
| ⚠⚠⚠ The prerequisite course | **UWF titles `CNT3004` *"Introduction to Networks"*** — **the module 1 name**, and NOT the statewide title |

**Two consecutive courses named after two consecutive vendor modules is not coincidence.**

⚠⚠ **THE DETECTION METHOD, and it is cheap: when a course TITLE reads like a product or module
name rather than a subject, check whether it matches a vendor certification track.** *"Routing and
Switching Essentials"* is not how a university names a subject; it is how a vendor names a module.
**Expect it in `CNT`, `CTS`, `CIS` and the Engineering Technology networking numbers.**

⚠ **Write it as an INFERENCE with the evidence shown unless you have seen a syllabus**, and give the
student a question rather than a claim — for `CNT3112`, *"ask which CCNA revision this course
follows"*, which also tells them which exam to sit.

⚠⚠⚠ **And the consequence INVERTS the usual transfer advice: what transfers is the
CERTIFICATION, not the number.** With one public carrier the "same course offered" condition bites
hard, **but a current vendor certification is recognised by every institution and employer in the
field.** **Say so.**""")

# --- 2. Placeholder prerequisite: second instance, new wildcard form --------
rep(
"""| ⚠⚠ **PLACEHOLDER** (222) | **`COM4301` — *"COM 2XXX Introduction to Communication Studies"*** | ⚠ **`2XXX` is a wildcard nobody filled in** | **the INTENT is legible and usually sound — state the intent, say the number does not exist** |""",
"""| ⚠⚠ **PLACEHOLDER** (222, 226) | **`COM4301` — *"COM 2XXX"*; `CNT3004` — *"CSG X060"*** | ⚠ **a wildcard nobody filled in.** ⚠⚠ **TWO conventions: `2XXX` masks the century and keeps the level; `X060` masks the LEVEL and keeps the century — so look for `X` ANYWHERE in the numeric portion, not only as a trailing mask** | **the INTENT is legible and usually sound — state the intent, say the number does not exist** |""")

# --- 3. An OR in a carrier's own prerequisite is a positive tell ------------
rep(
"""⚠⚠⚠ **THE STRONGEST EVIDENCE THAT TWO FAMILIES ARE THE SAME COURSE IS AN INSTITUTION HEDGING
ITS OWN PREREQUISITE ACROSS THEM.**""",
"""⚠⚠ **GENERALISED (batch 226): an `OR` in a carrier's OWN prerequisite is a positive tell that the
statewide numbering does not line up at that campus.** `CNT4416`'s statewide gate names `CNT4403`,
`CIS4385` AND `CDA3101`; **UWF does not carry `CIS4385`, so its own prerequisite reads
`(CIS 4385 OR CIS 4221) AND CNT 4403`.** ⚠ **Read these `OR` lists as free evidence — they mark
exactly the points where a department has had to work around the state's numbering.**

⚠⚠⚠ **THE STRONGEST EVIDENCE THAT TWO FAMILIES ARE THE SAME COURSE IS AN INSTITUTION HEDGING
ITS OWN PREREQUISITE ACROSS THEM.**""")

# --- 4. acalog count -> eight; add Florida Poly register row ----------------
rep(
"""| **⚠⚠⚠ acalog = presumptively UNREACHABLE** | **SEVEN** institutions and counting |""",
"""| **⚠⚠⚠ acalog = presumptively UNREACHABLE** | **EIGHT** institutions and counting |""")

rep(
"""**FSW, TSC, CF, Polk State, Santa Fe, FAMU and St. Johns River State** all serve""",
"""**FSW, TSC, CF, Polk State, Santa Fe, FAMU, St. Johns River State and Florida Polytechnic** all serve""")

rep(
"""| **St. Johns River State (SJRSC)** | `catalog.sjrstate.edu` — acalog (Modern Campus) |""",
"""| **Florida Polytechnic (FLPOLY)** | `catalog.floridapoly.edu` — acalog (Modern Campus) | ⚠ **CONTENT-BLOCKED, probed 2026-09-16 (batch 226).** Root 200 (63 KB), **55 acalog references**, `content.php` empty 202. ⚠⚠ **Florida's newest public university and exclusively STEM** — engineering and computing only — **so it will recur as a carrier across the computing and engineering prefixes, and it is unreadable.** Carrier of `CNT3004C` and `CNT4526`. |
| **St. Johns River State (SJRSC)** | `catalog.sjrstate.edu` — acalog (Modern Campus) |""")

# --- 5. Inventory can carry a PRIVATE carrier's title -----------------------
rep(
"""**Verify against a live catalog before treating an institution as a source or asserting a count in a guide.** |""",
"""**Verify against a live catalog before treating an institution as a source or asserting a count in a guide.** ⚠⚠ **AND IT CAN CARRY A *PRIVATE* CARRIER'S TITLE AS THE COURSE NAME** — `COM2713` reads *"Writing for Strategic Communication"* (batch 222) and `CNT3112` reads *"Advanced Network Administration"* (batch 226), **both the private carrier's title rather than the statewide or public one.** **Two instances make it a recurring failure mode; tell the reader to register by NUMBER.** |""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')
