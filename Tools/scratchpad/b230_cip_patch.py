"""Record the CIP career-paths anchor in Tools/CLAUDE.md (Ron, 2026-09-16)."""
import io, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()
A = """## Priority hierarchy"""
assert A in s
NEW = """## \u26a0\u26a0\u26a0 CIP CODES ARE THE CAREER-PATH ANCHOR (Ron, 2026-09-16)

Ron's direction, verbatim:

> *"Once we complete the queue we are going to look at career paths. All the careers will be bound to
> CIP codes https://nces.ed.gov/ipeds/cipcode/browse.aspx?y=55 and that will be the anchor for the
> career paths."*

**That is the NEXT phase, not this one \u2014 finish `queue.csv` first.** It is recorded here because it
changes what current batches should CAPTURE, in exactly the way the 2026-09-11 "list courses as you
go" direction did.

### \u2705 What is already banked

**`cip_map.py` harvests course \u2192 CIP from the Coursedog caches, which are the ONLY Florida source
exposing a per-course `cipCode`.** As of 2026-09-16 it maps **25,412 courses**:

| Cache | Rows | With a usable CIP |
|---|---|---|
| FIU | 27,923 | **25,188** |
| FAU | 7,127 | **7,120** |
| NWFSC | 1,802 | 708 |
| \u26a0 FSCJ | 22,698 | **0** |

\u26a0\u26a0 **Two format traps, both real in the data and both handled in `cip_map.py`:** FIU writes CIP
**dotted** (`16.1101`) while FAU and NWFSC write it **undotted** (`240101`); and **FSCJ's field is
populated on 2 rows out of 22,698, both with the placeholder `9999999999`**. **A 10-digit value is not
a CIP code \u2014 treat anything that is not 6 digits as absent rather than coercing it.**

### \u26a0\u26a0\u26a0 The finding the career-paths build must design around

**CIP is MORE stable than the course number \u2014 but it is not stable enough to be trusted alone.**
Measured over the **1,500 courses carried by two or more of these institutions**:

| | Count | Share |
|---|---|---|
| Institutions **agree** exactly | 763 | 51% |
| Disagree **within the same 2-digit family** | 631 | 42% \u2014 granularity, benign |
| \u26a0\u26a0 **Disagree across DIFFERENT families** | **106** | **7% \u2014 the serious cases** |

\u26a0 **The first number to quote is 93%, not 49%.** A raw "half of them disagree" count is misleading,
because most disagreement is one institution choosing a finer sub-code than another. **Compare at the
2-digit family level first, then look at the residue.**

**But the residue is severe, and these are real:**

| Course | Classified as |
|---|---|
| \u26a0\u26a0\u26a0 **`ART1300C`** (Drawing) | FAU **50.0701 Fine Arts** \u00b7 NWFSC **13.1302 ART TEACHER EDUCATION** |
| \u26a0\u26a0\u26a0 **`ART2501C`** | FAU **50.0701 Fine Arts** \u00b7 NWFSC **36.1096 LEISURE AND RECREATIONAL ACTIVITIES** |
| `ARH2050`/`ARH2051` | FAU **24.0199 Liberal Arts** \u00b7 FIU + NWFSC **50.0703 Art History** |
| `ANT2100` | FAU **45.0201 Anthropology** \u00b7 NWFSC **30.0000 Multi/Interdisciplinary** |
| `ADV3008` | FAU **52.0101 Business** \u00b7 FIU **09.0101 Communication** |

\u26a0\u26a0\u26a0 **The same drawing course is fine art at one institution, teacher education at another and a
recreational activity at a third. A pathway that routes students by CIP alone would send those three
students to three different careers on identical coursework.**

**So the CIP anchor needs the same treatment the course number needed:**

1. **Anchor the CAREER on a CIP code** \u2014 that is what Ron specified and it is sound, because the
   career end of the mapping is where CIP is authoritative.
2. \u26a0\u26a0 **Do NOT infer a COURSE's pathway membership from its institution-assigned CIP alone.**
   A course's CIP is *that institution's* classification of it, and it varies.
3. **Where institutions disagree, record BOTH rather than picking** \u2014 the disagreement is data about
   how the course is actually used, and it is exactly the kind of fact this project exists to surface.
4. \u26a0 **Compare at the 2-digit family before the 6-digit code**, or 42% of benign granularity will be
   reported as conflict.

\u26a0 **Standing practice from now on: when a batch touches a Coursedog school, the CIP data comes for
free \u2014 `cip_map.py` re-runs in seconds off the caches.** Keep the caches current and the anchor
builds itself. See `REVIEW_QUEUE.md` item 103.

---

## Priority hierarchy"""
s = s.replace(A, NEW, 1)
io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md: CIP anchor section added')
