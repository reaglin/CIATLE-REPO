"""Record Ron's 2026-09-17 working-mode change in Tools/CLAUDE.md."""
import io, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)

rep("""## \u26a0\u26a0\u26a0 Direction (Ron, 2026-09-11): LIST courses as you go; guides follow the queue and then requests""",
"""## \u26a0\u26a0\u26a0 CURRENT DIRECTION (Ron, 2026-09-17): REQUESTED COURSES ONLY

**This supersedes the "finish `queue.csv` first" half of the 2026-09-11 direction below.** Ron's words:

> *"the plan is to keep track of the items (mark them) that need my attention, but our main focus is
> going to be on **requested curriculum guides and we will only tackle those courses that have been
> requested**. We will still need those notes to handle the situation of one of the marked courses
> being requested."*

**Three things follow.**

1. \u26a0\u26a0\u26a0 **`queue.csv` is no longer the work list.** It stands at 108 `queued` rows and they stay
   there. **Do not pick a prefix off it and start writing.** The work is
   `GET /api/v1/queue/guides?status=waiting`, and **when that queue is empty there is no guide work** \u2014
   say so plainly rather than finding something to do.
2. **`REVIEW_QUEUE.md` keeps growing and keeps being marked.** It is no longer a side-channel: under
   request-driven working it is **the only warning you get** that a requested course is already known to
   be a problem.
3. \u26a0\u26a0 **A flagged course now arrives WITHOUT WARNING.** In queue-driven mode you met a held course by
   working steadily toward it and the note turned up in passing. **A public request arrives out of
   order, on any number, at any time.**

### \u26a0\u26a0\u26a0 So the FIRST command of every session is now this one

```bash
python review_lookup.py --requests
```

**It reads the live request queue and cross-references every waiting course against all 105
`REVIEW_QUEUE` items** \u2014 361 courses are named across them. It separates items **ABOUT** a course from
items that merely **mention** it, follows **bare/`C`/`L` twins and sequence partners**, and prints
**\u26a0\u26a0 HELD \u2014 ASK RON BEFORE WRITING** where an open item says the course was pulled, held, or needs a
decision.

\u26a0 **A HELD course that has been REQUESTED is exactly the case Ron's instruction anticipates, and it is
not a blocker \u2014 it is a question for him.** **Report the request, name the item, say what the block is,
and ask.** A visitor request is the strongest demand signal the project has; it may well be the reason
to resolve a long-held item. **Do not write it silently, and do not silently skip it either.**

Other tools for the same file: `review_index.py` regenerates the decision index at the top of
`REVIEW_QUEUE.md` (run it after adding an item), and `review_lookup.py --all` lists every course the
file mentions.

---

## \u26a0\u26a0 Superseded in part \u2014 Direction (Ron, 2026-09-11): LIST courses as you go; guides follow the queue and then requests""")

rep("""2. **Finish `queue.csv`**, then **shift to visitor requests** as the main source of guide work.""",
"""2. \u26a0\u26a0\u26a0 **SUPERSEDED 2026-09-17 \u2014 see the section above.** This read *"Finish `queue.csv`, then shift
   to visitor requests."* **The shift has now happened: requests are the ONLY source of guide work, and
   `queue.csv` is not to be worked through.** The rest of this section still stands.""")

rep("""   guide requests**, which outrank the local queue. **Only then** work `queue.csv`.""",
"""   guide requests**. \u26a0\u26a0\u26a0 **As of 2026-09-17 requests are the ONLY source of guide work \u2014 do NOT fall
   through to `queue.csv`.** And run **`python review_lookup.py --requests`** before writing anything:
   it flags any requested course that already carries a `REVIEW_QUEUE` note.""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')
