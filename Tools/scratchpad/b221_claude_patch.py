"""Batch 221 edits to Tools/CLAUDE.md. Run once from Tools/scratchpad."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


# --- 1. Level counter-case + the ladder shape --------------------------------
rep(
"""authority**, and several do. **So "FCS implies lower division" is a tendency the sector rule exploits, not
a fact to rely on.**
""",
"""authority**, and several do. **So "FCS implies lower division" is a tendency the sector rule exploits, not
a fact to rely on.** ⚠⚠ **Confirmed again one batch later: St. Petersburg College (FCS) carries
`PLA4554` AND `PLA4806` at 4000 level.** **Check the carriers; never infer the level from the sector.**

#### ⚠⚠⚠ THE A.S.-TO-BS LADDER — the same data shape, the OPPOSITE diagnosis (batch 221)

**Running the batch-220 drill on `PLA` fired on FOUR of six queued courses — and the answer came out
different, which is the finding. A sector split in the data can be a DEFECT or a DESIGN, and the two need
opposite warnings.**

| Subject | FCS numbers | SUS numbers |
|---|---|---|
| **Family law** | **`PLA2800`** — ⚠ **18 public carriers, ALL FCS** | `PLA3806` (FGCU, UWF); `PLA4806` (UCF, SPC) |
| **Law office management** | **`PLA2763`** — **10 carriers, ALL FCS** | `PLA4764` (UCF, UWF) |
| **Property** | `PLA2610` (FCS) | `PLA3613` (UWF); `PLA3615` (UCF) |
| **Bankruptcy** | `PLA2460` (FCS) | `PLA3464` (UWF); `PLA4464` (UCF) |

⚠⚠⚠ **The explanation is an ARTICULATION LADDER, not an error: Florida's A.S. in Paralegal
Studies is overwhelmingly an FCS credential using `PLA1xxx`/`PLA2xxx`, and the BS in Legal Studies is an
SUS credential using `PLA3xxx`/`PLA4xxx`. The universities renumber the same subjects at upper division
because a baccalaureate requires upper-division hours.**

| | `CCJ2452`/`CCJ3450` (batch 220) | `PLA` (batch 221) |
|---|---|---|
| What it is | ⚠ **a DEFECT** — one course numbered twice | ⚠ **deliberate DESIGN** |
| Evidence | **two** numbers in the prefix; near-identical statewide descriptions | **four subjects at once**, with the upper statewide descriptions visibly **DEEPER** |
| Harm | ⚠ **a lost credit** — a 2000-level course cannot supply upper-division hours | ⚠ **repeated content + Florida EXCESS HOURS** — the retake IS the design |
| The guide says | *get a written answer from the receiving department BEFORE taking the lower version* | *expect familiar ground at greater depth; ask about substitution* |

⚠⚠ **THE TEST, and it costs one CSV read: count how many SUBJECTS in the prefix show the split, and
compare the two statewide DESCRIPTIONS for DEPTH.** **One subject with matching descriptions is a numbering
defect. Several subjects with visibly deeper upper descriptions is a degree ladder.** Worked comparison:
`PLA2460` reads *"an introduction into the purpose of bankruptcy laws"* against `PLA3464`'s chapters
*"discussed in detail"*; `PLA2800` is a 1980s numbered topic list against `PLA3806`'s **Florida statutes**
and **practical drafting**.

⚠ **Expect the ladder in every prefix with an A.S.-to-BS articulation** — paralegal studies, nursing,
respiratory care, radiography, dental hygiene, health information management, and the Engineering
Technology BAS prefixes. **It is the batch-206 licensure-ladder observation showing up in the NUMBERING
rather than in the scope.**

⚠ **And check for the counter-case before generalising: `PLA4191` and `PLA4554` have NO lower-division
twin**, so the ladder is a property of some subjects in a prefix, not of the whole prefix.
""")

# --- 2. The dangling-prerequisite mechanism ----------------------------------
rep(
"""⚠ **Expect it wherever a prefix runs PARALLEL NUMBERING FAMILIES** (below): the statewide prerequisite
was written against one family and the carrier uses the other.
""",
"""⚠ **Expect it wherever a prefix runs PARALLEL NUMBERING FAMILIES** (below): the statewide prerequisite
was written against one family and the carrier uses the other.

##### ⚠⚠⚠ THE MECHANISM, found in batch 221: a SECTOR split makes prerequisites dangle on one side

**Batch 219 found the shape and could not explain it. `PLA` supplies two more instances and the cause.**

| Course | Statewide prerequisite | Resolves? |
|---|---|---|
| **`PLA4554`** | **`PLA 1003` AND `PLA 2203`** | ⚠⚠ **UCF carries NEITHER** — its real gate is **`ENC 1102`**. SPC carries both. |
| **`PLA3806`** | **`PLA 1003`** | ⚠ **FGCU carries it; UWF does NOT.** |

⚠⚠⚠ **Statewide prerequisites are INSTITUTION-CONTRIBUTED, so in a prefix that splits by sector
they get written from the side that HAS the lower-division numbers.** `PLA1003` and `PLA2203` are carried
almost entirely by state colleges. **At a university carrying no lower-division `PLA` numbers at all, the
statewide prerequisite names courses that are not on the menu.**

⚠⚠ **So the batch-219 check becomes targeted rather than general: whenever a prefix splits by sector,
EXPECT its statewide prerequisites to dangle on the other side.** **Check the prerequisite against the
CARRIER, not the state record, and name the real gate in the guide.**

⚠ **Useful in reverse: a dangling prerequisite is itself EVIDENCE of a sector split**, so the two
findings confirm each other. ⚠ **And the real gate is often something like freshman composition — which
tells you the course is open to students outside the major**, a genuinely useful student-facing fact.
""")

# --- 3. Distribution test needs a threshold ----------------------------------
rep(
"""A field that is uniform is a prefix-level default; a field that splits is evidence.""",
"""A field that is uniform is a prefix-level default; a field that splits is evidence. ⚠⚠ **But the
split has to be SUBSTANTIAL — see the threshold note below; "more than one value" is not the test.**""")

rep(
"""##### ⚠⚠⚠ STRATIFY THE DISTRIBUTION BY COURSE LEVEL""",
"""##### ⚠⚠ The split must be SUBSTANTIAL — a lopsided one is "near-universal with exceptions" (batch 221)

**`survey.py` calls a field *discriminating* as soon as it sees more than one value, and that is too weak a
test.** In `PLA` it reported `dual_enrollment` as discriminating; stratified to active undergraduate rows it
is **155 `Y` / 9 `N` — 94% to 6%.**

| Field | Split | Verdict |
|---|---|---|
| `SPN` `hs_credit` | 24 / 178 | ✅ **genuinely discriminating** — produced that batch's best finding |
| `CCJ` transferable (undergrad) | 2 / 169 | ⚠ near-universal |
| `PLA` dual enrolment (undergrad) | 9 / 155 | ⚠ near-universal |

⚠ **A lopsided split means "near-universal, with exceptions worth listing SEPARATELY" — write the default
as a default, and capture the handful of exceptions as their own note.** **Presenting a 94/6 field as a
finding is the same error the uniform case was meant to prevent.**

##### ⚠⚠⚠ STRATIFY THE DISTRIBUTION BY COURSE LEVEL""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')
