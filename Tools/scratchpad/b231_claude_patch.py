"""Batch 231 edits to Tools/CLAUDE.md."""
import io, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)

# 1. FGCU register row -- now blocked
rep("""| **FGCU** | `catalog.fgcu.edu/courses/<prefix>/<prefix>.pdf` (**the `.pdf`, not the directory**) | \u2705 **working.** \u26a0 The old directory URL is what was bot-blocked; the PDF answers. **Now the single most productive cross-check source in the project** \u2014 it documents credits explicitly and has produced the divergence a guide turned on in three consecutive batches. |""",
"""| **FGCU** | `catalog.fgcu.edu/courses/<prefix>/<prefix>.pdf` | \u26a0\u26a0\u26a0 **BLOCKED as of 2026-09-17 (batch 231) \u2014 RE-PROBE BEFORE ASSUMING IT IS GONE.** Returns an **empty 202** on `phi`, `mue`, `bsc`, `egn` and `eng` \u2014 **6 requests across 2 days and 5 prefixes**, which is past what the batch-183 rate-trigger caution covers but is NOT proof of a permanent block. **This was the single most productive cross-check source in the project**, so the loss is significant: it documented credits explicitly and produced the divergence a guide turned on in three consecutive batches. **Probe it at the start of every session** (a prefix FGCU certainly carries \u2014 `bsc` or `eng`); a full body means it is back. See `REVIEW_QUEUE.md` item 104. |""")

# 2. Gordon Rule designation RATE
rep("""\u26a0\u26a0 **So the honest statement a guide should make: the flags reliably tell you that SOME designation is""",
"""#### \u26a0\u26a0\u26a0 HOW OFTEN AN INSTITUTION DESIGNATES VARIES BY A FACTOR OF THIRTEEN (batch 231)

**The rule above says designation is institution-specific. `PHI` quantifies it, and the spread is far
wider than "varies" suggests.** One `Counter` over the prefix \u2014 464 public undergraduate rows, 132
designated, 28% overall:

| Institution | Designated | | Institution | Designated |
|---|---|---|---|---|
| **IRSC** | **11/12 \u2014 92%** | | FAU | 8/44 \u2014 18% |
| **GCSC** | 6/8 \u2014 75% | | UNF | 4/39 \u2014 10% |
| **UWF** | 14/24 \u2014 58% | | UCF | 6/68 \u2014 9% |
| **USF** | 10/20 \u2014 50% | | FIU | 3/40 \u2014 7.5% |
| FGCU | 5/17 \u2014 29% | | **FSU** | **2/29 \u2014 7%** |

\u26a0\u26a0 **So the Gordon Rule designation is INSTITUTIONAL POLICY showing through, not a property of any
course.** All four `PHI` courses in batch 231 had **exactly one of their two carriers** designating
them \u2014 four for four \u2014 which looks like four findings and is one.

\u26a0\u26a0\u26a0 **This is the batch-230 pattern rule applied to DESIGNATIONS: before writing a designation
difference up per-course, count the institution's whole prefix.** Otherwise one policy is reported as
N separate divergences.

\u26a0 **But the rate predicts the TENDENCY, not the course \u2014 and `PHI3200` is the counter-case.** UWF
designates 58% of its philosophy courses and FGCU 29%, **yet on that number it is FGCU that designates
and UWF that does not.** **So never infer an individual course's designation from the institution's
habit; look it up, and tell the student to check their own list.**

\u2705 **A validation worth recording: the flat-file flags matched the catalogue 4 for 4.** UWF's PDF
carries *"Meets College-Level Communication Skills Requirement"* on exactly the three courses the flat
file flags and not on the fourth. **The batch-179 label rule and the flag data corroborate each other
independently, which is good reason to trust both.**

\u26a0\u26a0 **So the honest statement a guide should make: the flags reliably tell you that SOME designation is""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')
