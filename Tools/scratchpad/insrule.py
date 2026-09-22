# -*- coding: utf-8 -*-
import io
p='CLAUDE.md'
s=io.open(p,encoding='utf-8').read()
anchor="#### ⚠⚠ THE RESEARCH IS THE COST OF A PATH — the writing is not (2026-09-19/20)"
assert anchor in s
block = """#### ⚠⚠⚠ A PROFESSION'S DEGREES CAN BE SPLIT ACROSS TWO CIP FAMILIES — check before quoting a count (2026-09-22)

**Found on social work, and it would have understated the finding by two-thirds.** IPEDS records
Florida's MSW output under **TWO** codes:

| Code | Master's | Institutions |
|---|---|---|
| `44.0701` Social Work | 368 | the obvious one |
| ⚠⚠ `51.1503` **Clinical/Medical Social Work** | **796** | FSU 431, FAU 143, UWF 120, FIU 74, UNF 28 |

⚠⚠⚠ **FSU, UWF, FIU and UNF record NO master's under `44.0701` at all.** Quoting the
social work code alone reports **368** where the real figure is **1,164**.

⚠ **The SCHOOL LIST was unaffected here** — the union is the same nine institutions — **so a
programme's derived school count will not warn you.** Only the credential counts move, and they move a
lot.

**Drill, and it is one `cipbreak.py` call:** before quoting a degree count, **scan the neighbouring
2-digit families for the same subject**, not just the obvious 4-digit group. Health-adjacent subjects
are the risk: `51.` collects clinical versions of degrees that also live in `44.`, `42.`, `13.` and
`19.`. ⚠ Run `python scratchpad/cipbreak.py <2-digit>.` on both families and compare.

⚠⚠ **And where the second code is NOT SEEDED** (as `51.15` is not), the programme cannot claim
it — **so put the split and the real number in the `degreesNote` prose** rather than silently
publishing the understated count.

"""
io.open(p,'w',encoding='utf-8').write(s.replace(anchor, block+anchor,1))
print('ok')
