"""Batch 232 edits to Tools/CLAUDE.md."""
import io, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)

# 1. USF row -- identified, acalog, content-blocked
rep("""| **USF** | `catalog.usf.edu` | \u26a0 root 200 (75 KB) but **no course-description path exposed**; its only course link goes to `usf.edu/academics/courses-calendar.aspx`. Not yet a route. |""",
"""| **USF** | `catalog.usf.edu` \u2014 **acalog (Modern Campus)** | \u26a0\u26a0 **IDENTIFIED AND CONTENT-BLOCKED 2026-09-17 (batch 232).** Root answers 200 (75 KB) **with acalog markers**; `content.php` returns an **empty 202**; the Coursedog bootstrap says the host *"does not exists"*. **NINTH institution in the acalog pattern.** \u26a0 This row previously read "no course-description path exposed \u2014 not yet a route", which invited re-probing; **it is now a settled negative.** USF is a frequent carrier on health-sciences and communication prefixes, so expect to write its courses from the statewide record and another carrier. |""")

# 2. acalog count -> nine
rep("""| **\u26a0\u26a0\u26a0 acalog = presumptively UNREACHABLE** | **EIGHT** institutions and counting |""",
"""| **\u26a0\u26a0\u26a0 acalog = presumptively UNREACHABLE** | **NINE** institutions and counting |""")
rep("""**FSW, TSC, CF, Polk State, Santa Fe, FAMU, St. Johns River State and Florida Polytechnic** all serve""",
"""**FSW, TSC, CF, Polk State, Santa Fe, FAMU, St. Johns River State, Florida Polytechnic and \u26a0 USF** all serve""")

# 3. Branch-4 mechanism
rep("""**Branch 4 handling \u2014 `HFT4252` is the worked case.**""",
"""#### \u26a0\u26a0\u26a0 THE MECHANISM BEHIND BRANCH 4, and the tell that reveals it (batch 232)

**On `HFT4252` the title/description contradiction was visible and unexplained. `PHC4140` shows how one
gets made, because the statewide description NAMES ITS OWN AUTHOR.**

| | |
|---|---|
| statewide **TITLE** | *Public Health Planning and Analysis* |
| statewide **DESCRIPTION** | \u26a0\u26a0 entirely **GIS** \u2014 *"an introduction to Geographic Information Systems (GIS)\u2026 buffering, layering, and spatial queries"* |
| **UWF** | *Public Health Planning and Analysis* \u2014 planning, implementation, evaluation, needs assessment. **No GIS.** Backs the **title**. |
| **USF** | *Introduction to Public Health Geographic Information Systems*. Backs the **description**. |

\u26a0\u26a0\u26a0 **The tell: the description ends by calling the course *"a required course in the PROPOSED
public health major in the Bachelor of Science in Health Sciences [BSHS] degree program"* \u2014 one
specific institution's degree, described while it was still being proposed.**

**So the likeliest history is that a carrier contributed a description of ITS OWN course onto a number
whose TITLE already belonged to a different subject, and nobody reconciled the two.** That is a
*mechanism*, not just a state of affairs: **the record is internally contradictory because it was
assembled from two sources, not because either half went stale.**

\u26a0\u26a0 **The drill: when title and description disagree, read the DESCRIPTION for signs of a single
author** \u2014 a named degree programme, a delivery mode (*"this online course"*), a word like
*"proposed"*, or an institution code. **Where you find one, you have identified which carrier the
description belongs to, and the other carrier's reading is what the title preserves.** That converts an
unexplained contradiction into a legible one, and the guide can say so.

\u26a0 **And check whether the displaced subject had anywhere to go.** Here it did not: Florida provides
**three** upper-division planning numbers (`PHC?140`, `?142`, `?143`) and its only GIS-in-public-health
number, **`PHC?194`, is GRADUATE** \u2014 so an undergraduate GIS course had no correct home. **Misfiling by
necessity underneath a branch-4 collision**, and the guide says plainly that there is no right number to
go looking for.

**Branch 4 handling \u2014 `HFT4252` is the worked case.**""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')
