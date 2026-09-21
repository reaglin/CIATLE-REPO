# -*- coding: utf-8 -*-
import io
p='CLAUDE.md'
s=io.open(p,encoding='utf-8').read()
anchor="#### ⚠⚠ THE RESEARCH IS THE COST OF A PATH — the writing is not (2026-09-19/20)"
assert anchor in s
block = """#### ⚠⚠⚠ ON A CTE PATH, READ THE OCP LETTERS OUT OF THE STATEWIDE COURSE TITLES (2026-09-21)

**Florida builds every career and technical programme as a sequence of OCCUPATIONAL COMPLETION
POINTS, and it prints the OCP LETTER INSIDE THE STATEWIDE COURSE TITLE.** One flat-file pass on the
prefix gives you the whole ladder with its hours:

| Statewide title | Reads as |
|---|---|
| `BASIC HEALTHCARE WORKER (90 HOURS)` | OCP A, the shared core |
| `PHLEBOTOMIST  OCP B (75 HOURS)` | ⚠ **OCP B — and PHLEBOTOMIST is a JOB TITLE** |
| `EKG AIDE, MA  OCP D (75 HOURS)` | OCP D, another job title |
| `MEDICAL ASSISTANT (1 OF 3)  OCP E (320 HOURS)` | OCP E, the terminal point, in three parts |

⚠⚠⚠ **EACH OCP IS A PLACE A STUDENT CAN STOP, BE HIRED, EARN, AND COME BACK — and
this is close to the most useful thing a CTE path can tell a reader.** Medical assisting has four
exits before the end; **pharmacy technology (`PTN0084`–`0086`, 960 hours) has NONE**, so an
interrupted student finishes with nothing to show. **That difference matters more to someone with a
job and children than anything about the curriculum, and no programme page states it.**

⚠⚠ **So on a CTE path, do this BEFORE writing:**

1. `python scratchpad/carriers.py --prefix <PFX>` — the carrier counts per OCP show which exits
   institutions actually run; they are **not** uniform (20 carry `MEA0520`, 22 carry `MEA0521`).
2. **Read the hours out of the title** and total them, so the guide can state the whole length.
3. ⚠ **Say whether the ladder EXISTS.** A programme with no OCPs is a finding in its own right.
4. ⚠ **Tell the reader to ask whether the institution will actually AWARD the intermediate
   certificate** — the state structures the programme around the OCPs; not every college issues them.

⚠⚠ **And CHECK WHETHER THE OCCUPATION IS REGULATED AT ALL, because the answer is frequently
the opposite of what the risk suggests.** Florida requires a pharmacy technician to register with the
Board of Pharmacy and complete a board-approved programme (s. 465.014, F.S.) and requires **nothing at
all** of a medical assistant — whose permitted tasks under s. 458.3485 include **venipuncture and
administering medication**. ⚠ **Where the state regulates the physician rather than the assistant,
there is no floor under the training and the student carries the whole risk of choosing a programme.**
⚠ **Note too that a TITLE can be protected where the JOB is not**: only an NCCA-accredited
certification lets someone call themselves a *certified* medical assistant.

✅ **Measured while doing this, and worth knowing: `HSC0003` BASIC HEALTHCARE WORKER (90 hours) is
carried by 55 Florida public institutions — MORE THAN ANY OTHER COURSE IN THE STATE CATALOGUE.**
`ENC1101`, `MAC2311` and `STA2023` each reach 39; `HCP0121` Nurse Aide reaches 40.
**It is the shared front door of Florida health-care CTE** (`scratchpad/maxcarrier.py`).

"""
io.open(p,'w',encoding='utf-8').write(s.replace(anchor, block+anchor,1))
print('ok')
