# -*- coding: utf-8 -*-
import io
p='CLAUDE.md'
s=io.open(p,encoding='utf-8').read()
anchor="#### ⚠⚠ THE RESEARCH IS THE COST OF A PATH — the writing is not (2026-09-19/20)"
assert anchor in s
block = """#### ⚠⚠⚠ BLS HAS THREE REGISTERS FOR AI — quote the one it actually used (2026-09-22)

**Every path now gets asked \"will AI take this job?\", and the answer should be the federal agency's
own wording rather than a guess.** Read three occupations against each other:

| Occupation | Projection | What the BLS handbook says |
|---|---|---|
| Medical records specialist | ✅ **+8%** | automation discussed; **no dampening claim at all** |
| Web developer / digital interface designer | ✅ **+5%** | AI “may **soften the employment growth** of these workers” |
| ⚠ Graphic designer | ⚠⚠ **−2%** | AI “projected to… **reduce the need** for these workers” |

⚠⚠⚠ **Three deliberately different phrasings from one agency, and they track HOW ROUTINE THE
OUTPUT IS.** Where the product is a finished artefact a tool can now generate — a layout, an image —
the language is *reduce the need*. Where it is a working system somebody must specify, build and
maintain, it is *soften the growth*. **Where the work is checking, auditing and defending a decision,
there is no dampening claim.**

⚠⚠ **So the drill on any path where the question arises: go to the BLS OOH page and quote the
sentence.** Do not paraphrase it into “AI may affect this field”, and do not omit it because it is
uncomfortable. **The exact verb is the finding.**

⚠ **And read the SECOND sentence, which people skip.** On web development BLS adds that AI *“may
also allow some workers in other occupations to do basic web development tasks”* — that is task
migration rather than job loss, and it is a different warning with a different answer.

✅ **What to tell the reader:** the exposure is to the routine PRODUCTION half of a job, not to the
job. **Position on the specification and judgement side of whatever the field is.** That advice is
supportable from the data rather than from speculation, which is why it belongs on the page.

"""
io.open(p,'w',encoding='utf-8').write(s.replace(anchor, block+anchor,1))
print('ok')
