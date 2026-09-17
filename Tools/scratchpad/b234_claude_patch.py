"""Batch 234 edits to Tools/CLAUDE.md -- corrects the batch-222 placeholder rule."""
import io, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)

rep("""| \u26a0\u26a0 **PLACEHOLDER** (222, 226) | **`COM4301` \u2014 *"COM 2XXX"*; `CNT3004` \u2014 *"CSG X060"*** | \u26a0 **a wildcard nobody filled in.** \u26a0\u26a0 **TWO conventions: `2XXX` masks the century and keeps the level; `X060` masks the LEVEL and keeps the century \u2014 so look for `X` ANYWHERE in the numeric portion, not only as a trailing mask** | **the INTENT is legible and usually sound \u2014 state the intent, say the number does not exist** |""",
"""| \u26a0\u26a0 **PLACEHOLDER** (222, 226, \u26a0 **corrected 234**) | **`COM4301` \u2014 *"COM 2XXX"*; `CNT3004` \u2014 *"CSG X060"*; `GEO4251` \u2014 *"GEO 5XX3"*** | \u26a0 **a masked number.** \u26a0\u26a0 **Look for `X` ANYWHERE in the numeric portion, not only as a trailing mask** | \u26a0\u26a0\u26a0 **RECOVER THE REAL NUMBER \u2014 see below. Do NOT stop at "the number does not exist".** |

##### \u26a0\u26a0\u26a0 CORRECTED (batch 234): a masked number is usually RECOVERABLE, and two of these are not placeholders at all

**Batch 222 recorded the handling as *"state the intent, say the number does not exist."* That is too
weak, and a scan of all 41 statewide CSVs on disk \u2014 220 wildcard tokens \u2014 shows why.**

**First, two different things are wearing the same shape, and the discriminator is in the surrounding
text:**

| What you see | What it is | Handling |
|---|---|---|
| \u2705 *"**ANY** 1XXX OR 2XXX COURSE WITH PREFIX CCJ, CJC, CJE, CJL, CJJ, PLA"* (`CCJ2453`) | **genuine LEVEL NOTATION** \u2014 any course at that level. The word **ANY**, or a prefix list, is the tell | **decode and explain it** (the batch-214 notation rule) |
| \u26a0\u26a0 *"HFT 3XXX **GOLF PLANNING & OPERATIONS II**"*, *"BCN 3XXX **INTRODUCTION TO THE CONCRETE INDUSTRY**"*, *"GEO 5XX3 **(ADVANCED CLIMATOLOGY AND CLIMATE CHANGE)**"* | \u26a0\u26a0\u26a0 **a PLACEHOLDER \u2014 and the masked number is FOLLOWED BY THE COURSE'S ACTUAL TITLE** | **use the title to find the real number** |

\u26a0\u26a0\u26a0 **In every placeholder case the writer knew exactly which course they meant and named it. So
the title recovers the number, and there are TWO routes:**

1. **Search the statewide TITLES in the same prefix for the quoted title.** Tested on four cases,
   **three recovered**: `GEO 5XX3 (Advanced Climatology and Climate Change)` \u2192 **`GEO?256`, graduate**;
   `PHC 5XX3 (Scientific Basis of Public Health)` \u2192 **`PHC?123`, graduate**; `BCN 3XXX (Introduction to
   the Concrete Industry)` \u2192 **`BCN?443`**. (`HFT 3XXX Golf Planning & Operations II` was not found \u2014
   so some genuinely do not resolve.)
2. \u26a0\u26a0 **Easier and more reliable: READ THE CARRIER'S OWN CATALOGUE ENTRY.** UWF's `GEO4251` says
   *"Offered concurrently with **GEO 5256** Advanced Climatology and Climate Change"* \u2014 **the exact
   number the state masked, published in full by the institution.** **The state record masks what the
   carrier prints.**

\u26a0 **And note where these cluster: `<PFX> 5XX3` appeared twice, in `GEO` and `PHC`, both inside
"offered concurrently with" DUAL-LISTING notes.** **So when a dual-listing note carries a masked
number, expect the graduate partner to be findable and give the reader its real number** \u2014 which
matters, because the repeat-restriction warning is useless if the student cannot identify the course
it applies to.""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')
