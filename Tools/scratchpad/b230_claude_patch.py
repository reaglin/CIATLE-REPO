"""Batch 230 edits to Tools/CLAUDE.md."""
import io, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)

# 1. Sequence divergence on BOUNDARY and ORDERING
rep("""### \u26a0\u26a0\u26a0 SEQUENCE-LENGTH divergence — the same field as ONE course or as TWO (batch 204)""",
"""### \u26a0\u26a0\u26a0 A SEQUENCE CAN DIVERGE ON THE BOUNDARY *AND* ON THE ORDERING (batch 230)

**Sequence-length divergence (below) asks whether a field is one course or two. `FIL4036` adds two
further axes, and all three are live on one number:**

| | Statewide | Florida Atlantic | UWF |
|---|---|---|---|
| **Span of part 1** | 1890s → **1959** | \u26a0 1890s → **the 1940s** | \u26a0\u26a0 **no boundary at all** |
| **Structure** | two courses | two courses | \u26a0\u26a0 **one course; no part 2 exists** |
| **Ordering** | part 2 **requires** part 1 | \u26a0 *"May be taken BEFORE"* — **either order** | n/a |

\u26a0\u26a0\u26a0 **So roughly two decades sit inside the course at one institution and outside it at another** —
for film history, that is noir, neorealism, the blacklist, the studio break-up and the arrival of
television. **A student can complete "Film History 1" at either and have covered materially different
material.**

**Handling: do not describe the span in the guide as though it were settled. Give the three readings in
a table and tell the reader to send a TOPIC or SCREENING LIST on transfer, not the course title** —
departments place by coverage, and a week-by-week list settles in seconds what a title cannot.

\u26a0 **Drill: where a numbered sequence exists (`I`/`II`, `1`/`2`), check THREE things, not one — where
each carrier draws the boundary, whether a part 2 exists at all, and whether the halves are ordered.**
Any of the three can diverge independently.

\u26a0\u26a0 **And run the batch-181 partner check regardless of what you find.** On `FIL4036` it paid: the
partner number `FIL4037` is *Film History 2* statewide and at FAU, **but USF carries it as *History of
Video Art*** — an unrelated subject. **So a student cannot simply enrol in the partner number wherever
they find it, and the guide has to say so.**

### \u26a0\u26a0\u26a0 SEQUENCE-LENGTH divergence — the same field as ONE course or as TWO (batch 204)""")

# 2. The conjunction test can PASS
rep("""\u26a0 **The drill: when a statewide title contains a conjunction ("X and Y"), check that the statewide
DESCRIPTION delivers both halves, and check whether Y has its own number that nobody carries.**""",
"""\u26a0 **The drill: when a statewide title contains a conjunction ("X and Y"), check that the statewide
DESCRIPTION delivers both halves, and check whether Y has its own number that nobody carries.**

\u26a0\u26a0 **AND RECORD IT WHEN THE TEST PASSES (batch 230).** Every instance above is a failure, which
makes the test look like a detector for a defect. **`FIL4102` is the clean case: the statewide title
promises *"Screenwriting AND Storyboarding"*, the sole carrier's TITLE drops storyboarding — and its
DESCRIPTION delivers it** (*"script formats, storyboarding, and story pitches"*). **A title that names
only the larger half is not a missing half.** \u26a0 **Check the description before writing a gap warning,
and say so in the guide when both halves are there** — that is a reassurance a student can use.""")

# 3. Institutional credit pattern across a whole prefix
rep("""### \u26a0 CREDIT-COUNT divergence — a fourth shape, and invisible from the identifier (batch 185)""",
"""### \u26a0\u26a0 CHECK WHETHER A CREDIT DIVERGENCE IS A PREFIX-WIDE INSTITUTIONAL PATTERN (batch 230)

**Before writing a credit divergence up as a fact about the course, count the institution's WHOLE
prefix.** Two `FIL` courses showed FAU at 4 credits against UWF's 3, which reads as two separate
findings. **It is one:**

| Institution | Undergraduate `FIL` credit profile |
|---|---|
| \u26a0 **FAU** | **11 of 21 at 4 credits** |
| UCF | 78 of 103 at 3 |
| USF | 25 of 25 at 3 |
| UNF | 24 of 25 at 3 |

\u26a0\u26a0 **FAU runs the prefix at 4 credits; every other institution runs it at 3.** **So the sentence to
write is "FAU carries this prefix at 4 credits", once, and not "this course diverges" on every course
in the batch** — which would report one institutional choice as N separate divergences.

\u26a0 **It is one `Counter` over the flat file, and it also gives the reader something more useful: an FAU
film student accumulates credit faster per course than a comparison of course counts suggests.**

\u26a0 **The same pass surfaces other institutional signatures worth a line** — FSU's `FIL` offering is
dominated by VARIABLE credit (`1-6` on 28 rows) and UCF carries 22 `VAR` rows, which is the shape of a
production school rather than a studies department.

### \u26a0 CREDIT-COUNT divergence — a fourth shape, and invisible from the identifier (batch 185)""")

# 4. CIP disagreement within one institution
rep("""\u26a0 **Standing practice from now on: when a batch touches a Coursedog school, the CIP data comes for
free \u2014 `cip_map.py` re-runs in seconds off the caches.**""",
"""\u26a0\u26a0 **AND THE DISAGREEMENT IS NOT ONLY BETWEEN INSTITUTIONS — IT HAPPENS INSIDE ONE (batch 230).**
FAU tags `FIL4036`, `FIL4037`, `FIL4364` and `FIL4106` as **50.0602 Film/Cinema/Video Studies** and
`FIL3803` *Film Theory* as **09.0702 Digital Communication/Media** — **same department, same prefix,
two CIP families.** \u26a0 **So a single institution's CIP assignment is not internally consistent either,
which strengthens the case against treating any one course\u2192CIP edge as authoritative.**

\u26a0 **Standing practice from now on: when a batch touches a Coursedog school, the CIP data comes for
free \u2014 `cip_map.py` re-runs in seconds off the caches.**""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')
