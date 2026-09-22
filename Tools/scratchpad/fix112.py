# -*- coding: utf-8 -*-
import io
p='REVIEW_QUEUE.md'
s=io.open(p,encoding='utf-8').read()
s=s.replace("## 112. ⚠ Should PHLEBOTOMY be its own programme? (raised 2026-09-21, medical laboratory scientist path)",
            "## 112. ✅ RESOLVED 2026-09-21 — phlebotomy IS its own programme (raised the same day)")
old = """⚠ **For Ron — two defensible answers and it is your call:**
1. **A `phlebotomy` programme of its own** on `51.1009`, linked to the medical laboratory scientist
   path as a non-route feeder (the `dental-assisting` pattern from earlier the same day). It would put
   29 technical colleges on the site.
2. **Leave it.** It is a short certificate rather than a programme in the sense the layer uses.

⚠ There is no phlebotomy row in `career_paths/QUEUE.csv`, so option 1 adds a programme whose only
career link is a non-route one."""
new = """✅ **RESOLVED by the second career-path queue, the same day.** The premise of the open question
was that *"there is no phlebotomy row in `career_paths/QUEUE.csv`, so option 1 adds a programme whose
only career link is a non-route one."* ⚠ **That was wrong — rank 107 IS Phlebotomist (SOC
31-9097).** With a career path to attach to, option 1 became the only sensible answer.

**Done:** programme **`phlebotomy`** on `51.1009` (29 institutions), and the **`phlebotomist`** path.

⚠⚠ **And the research answered the doubt that produced the question.** The worry was that
*"a school with a phlebotomy certificate has a medical laboratory programme"* is a stretch. **It is —
and the honest relationship turned out to be a different one entirely: `MEA0520` and `MEA0521` carry
`OCP B` and `OCP C` IN THEIR STATEWIDE TITLES, so phlebotomy is formally part of Florida's MEDICAL
ASSISTING programme, not the laboratory one.** The programme is linked to `medical-assisting` as the
same framework and to `medical-laboratory-science` as the rung above.

⚠⚠⚠ **The finding that came out of it, and it is the page's headline:** **s. 483.803,
F.S. names phlebotomists in the EXCLUSION** from *clinical laboratory personnel*. **Florida licenses
the technician and the technologist above and writes the bottom rung out of the statute by name** —
while producing **772** phlebotomists a year against **126** technicians and **107** scientists."""
assert old in s
s=s.replace(old,new)
io.open(p,'w',encoding='utf-8').write(s)
print('ok')
