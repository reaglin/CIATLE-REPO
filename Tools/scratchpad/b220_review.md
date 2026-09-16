
## 100. ⚠⚠ `CCJ` splits courses by SECTOR across two numbers — two confirmed, and the prefix should be swept (batch 220)

**Not a correction request — the finding is already written into the live guides. This is a scope
decision about how far to chase it.**

**What is confirmed.** Florida numbers the same criminal justice course twice, split cleanly along the
FCS/SUS line, in **two** places in this one prefix:

| Subject | FCS number | SUS number |
|---|---|---|
| Introductory criminal justice (batch 182) | `CCJ1020` — Broward, EFSC, Valencia | `CCJ2002` |
| ⚠⚠ **Criminal justice administration** (batch 220) | **`CCJ2452`** — Polk State, Valencia, Florida Gateway, State College of Florida, Tallahassee State (**all five FCS**) | **`CCJ3450`** — UCF, UWF (**both SUS**) |

⚠⚠⚠ **The second is the more damaging, and the reason is the LEVEL.** `CCJ1020`/`CCJ2002` are both
lower-division, so an A.A. completer's protections absorb much of it. **`CCJ2452` is 2000-level and
`CCJ3450` is 3000-level, and a 2000-level course cannot supply upper-division hours toward a Florida
baccalaureate** — so a state-college student who takes the subject may have to take it again at the
university, **not because the content differs but because the level does.** Seven institutions, two
numbers, zero crossover.

**Already done, no action needed on these:**

- ✅ **`CCJ3450`'s live guide** carries the full table, the upper-division-hours consequence and the
  "get a written answer from the receiving department first" instruction, in both the body and the
  prerequisite field.
- ✅ **All four batch-220 guides** carry the prefix-wide "check the number, not just the title" caution.
- ✅ **`CLAUDE.md`** records both rows and the generalised drill.

**Decision wanted from Ron — two questions.**

1. ⚠ **Should `CCJ` be swept for further instances?** Two confirmed in the two numbers we happened to
   look at is a poor sample. The cheap version is one `survey.py`-style pass over the prefix looking
   for **pairs of active numbers sharing a statewide title at different levels with disjoint carrier
   sectors** — perhaps twenty minutes, and it would either produce a list or close the question.
   **My recommendation: yes, and do it as a one-off report rather than course by course.**
2. ⚠ **Does `CCJ2452` deserve its own guide?** It is carried by **five** FCS institutions — more than
   `CCJ3450`'s two — and it is currently listed without a guide. It is not in `queue.csv`. Under the
   2026-09-11 direction a guide-less listed course is a finished outcome, so **the default is to leave
   it**; but a five-carrier lower-division course that half the state's CJ students take is an unusually
   strong candidate if you want one. **My recommendation: leave it unless a visitor requests it** —
   `CCJ3450`'s guide already tells a `CCJ2452` student what they need to know.

⚠ **Generalisable either way:** the drill now in `CLAUDE.md` is *"where a prefix is found to split one
course by sector, check its other high-enrolment numbers before writing any of them."* **If the sweep in
(1) is worth running on `CCJ`, it is probably worth running on every prefix with both FCS and SUS
carriers** — which is most of the vocationally-adjacent ones.
