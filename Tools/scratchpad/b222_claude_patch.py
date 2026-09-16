"""Batch 222 edits to Tools/CLAUDE.md. Run once from Tools/scratchpad."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


# --- 1. Fifth row on the C-suffix diagnostic table ---------------------------
rep(
"""| **no institution carries the bare form, or the `C` form** | the queued id may not exist — check before writing at all |
""",
"""| **no institution carries the bare form, or the `C` form** | the queued id may not exist — check before writing at all |
| ⚠⚠⚠ **only a PRIVATE institution carries one form** (batch 222) | **the id is REAL but has no carrier in scope.** Write the form a PUBLIC institution carries, mark the other `skipped` with its reason, and tell the reader in the guide not to register for it |

⚠⚠ **The batch-222 row is a SCOPE fact, not a catalogue fact, and it needs the opposite handling
from "a `C` nobody carries."** **`COM4564C`'s only carrier is Keiser (private); `COM4564` is carried by
UWF.** Same statewide title, same statewide description. **The queued `C` id was unwritable under the
2026-09-11 public-institution rule, so it was marked `skipped` with its reason and the BARE number was
written instead** — `reconcile` picks the new draft up as an orphan and adds the row itself.
⚠ **Record the substitution in the queue note and explain the suffix in the guide; do not do it
silently.**
""")

# --- 2. Consolidated defective-prerequisite taxonomy -------------------------
rep(
"""⚠ **Useful in reverse: a dangling prerequisite is itself EVIDENCE of a sector split**, so the two
findings confirm each other. ⚠ **And the real gate is often something like freshman composition — which
tells you the course is open to students outside the major**, a genuinely useful student-facing fact.
""",
"""⚠ **Useful in reverse: a dangling prerequisite is itself EVIDENCE of a sector split**, so the two
findings confirm each other. ⚠ **And the real gate is often something like freshman composition — which
tells you the course is open to students outside the major**, a genuinely useful student-facing fact.

##### ⚠⚠⚠ THE FIVE SHAPES OF A DEFECTIVE STATEWIDE PREREQUISITE (consolidated, batch 222)

**`DS_Prerequisites1` fails in five distinct ways, and they need different handling. Check every
course-looking token against all five before quoting the field.**

| Shape | Worked example | Tell | Handling |
|---|---|---|---|
| **Corrupt token** (209) | `ADV4802` — *"ADV U101C"* | fails `^[A-Z]{3}\\s?\\d{4}[A-Z]?$` | call it a data defect; send the reader to the catalogue |
| ⚠⚠ **PLACEHOLDER** (222) | **`COM4301` — *"COM 2XXX Introduction to Communication Studies"*** | ⚠ **`2XXX` is a wildcard nobody filled in** | **the INTENT is legible and usually sound — state the intent, say the number does not exist** |
| **Dangling: sector split** (221) | `PLA4554` — names two FCS-only numbers; UCF carries neither | the prefix splits FCS/SUS | name the REAL gate; expect it across the whole prefix |
| ⚠⚠ **Dangling: single-carrier contribution** (222) | **`COM4120` — names `COM 3311`, carried by UCF ALONE, and UCF does not require it** | ⚠ **both carriers SUS; NO sector split** | same handling, but expect it ANYWHERE, not only in split prefixes |
| **Local title in a statewide field** (200) | `COM4564` — *"COM4561 Social Media Content Development"* | the quoted title is not the statewide title | ⚠ **search by NUMBER**; and read it in reverse — it names the CONTRIBUTING institution |

⚠⚠⚠ **Batch 222 REMOVES a precondition from the batch-221 rule.** That rule concluded a sector
split causes dangling. **`COM4120` shows the simpler and more general cause: ANY prerequisite
contributed by one carrier may fail to resolve at another.** **A sector split makes it systematic; it
is not required for it to happen.** ⚠ **So run the carrier check on every statewide prerequisite,
not only in prefixes known to split.**
""")

# --- 3. Single-carrier baseline: COM is the new high on a large prefix -------
rep(
"""| `ARH` | **421** | 339 (81%) | | | |
""",
"""| `ARH` | **421** | 339 (81%) | ⚠⚠ **`COM`** | **370** | **308 (83%)** |
| `CCJ` | 486 | 311 (64%) | `PLA` | 286 | 190 (66%) |
""")

rep(
"""⚠⚠⚠ **Roughly three-quarters of all Florida course identifiers are carried by exactly ONE public
institution.**""",
"""⚠⚠ **Sixteen prefixes measured as of batch 222. `CCJ` (64%) and `PLA` (66%) are the lowest — both
have large lower-division state-college populations — and ⚠⚠ **`COM` at 83% across 370 ids is the
highest on a LARGE prefix**, so a communication course transferring cleanly by number is close to an
exception.

⚠⚠⚠ **Roughly three-quarters of all Florida course identifiers are carried by exactly ONE public
institution.**""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')
