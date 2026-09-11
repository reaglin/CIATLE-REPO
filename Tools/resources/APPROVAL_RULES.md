# Resource approval rules

**Settled by Ron, 2026-09-11.** This file is the standard for **what gets listed** on a course's Resources
page. The mechanics — endpoints, payloads, error codes — are in [`../RESOURCE_API.md`](../RESOURCE_API.md);
the loop is the `/resources` skill.

---

## What a resource is

A website or YouTube video listed for a course. It may be:

- a **free resource** — course notes, a textbook, video lectures, a simulator, practice problems;
- a **product** — something a vendor or sales agent offers that suits the course: a textbook, software, a
  lab kit, a paid course.

**Both are welcome, with no limit on commercial resources.** The difference is disclosed, never hidden.

## Decide in this order

1. **Look at the resource.** Fetch the page or video and read it. Never approve, and never write a summary,
   from the URL or the submitter's note alone.
2. **Does it match the course?** That is the whole relevance test — see below.
3. **Is it on the always-reject list?**
4. **Is it already listed?** (duplicate check)
5. **Write the summary**, then list it for this course and any others it genuinely suits.

## Course match — the only relevance test

**Reject only resources that do not match the course.** Judge against the course title and its curriculum
guide.

**Level is not grounds for rejection on its own.** A resource pitched above or below the course still gets
listed when it covers the course's material — say so in the summary ("a more advanced treatment…",
"a gentler introduction than this course assumes…") and let the student judge.

## Always reject

- adult content; gambling
- malware, or anything a browser flags as unsafe
- essay mills and homework-answer services
- pirated textbooks or other pirated material
- pages that are mostly advertising, with little content of their own
- dead links, and pages that cannot be reached
- paywalled pages with nothing visible to a student who does not pay
- **age-restricted videos** (a video that requires sign-in to confirm age)

Where a page cannot be judged — it will not load, or it is behind a wall — leave the suggestion pending or
reject it as unreachable. **Never guess.**

## Commercial resources and vendors

- **No limit** on how many products are listed, per course or per vendor.
- **The vendor must be identified in the summary**, along with what the resource costs. With that stated,
  vendor suggestions are welcome.
- Never repeat marketing copy. Describe what the product is and what it covers, in the same plain voice used
  for a free resource.

## Free resources

Say **what kind of resource it is** and **what it applies to** — lecture videos, worked examples, a
simulator, a full textbook, a single chapter — and which part of the course it lines up with.

**The student decides whether it is useful; the summary gives them what they need to decide, and may offer
guidance.** Guidance sounds like "best read alongside the first four weeks" or "assumes calculus", not
"the best site for this course".

## Duplicates

- **The same link is never listed twice for a course** — the site enforces that, matching links after
  normalising them.
- Before approving, check where a link already sits: `python review_resources.py listings --url <link>`.
  Two URLs for the same page (with and without a trailing slash, a shortener, a mirror) count as the same
  link: list it once.
- **Different links with similar material are both listed.** The student decides between them.

## Videos

- **No length limit** — the site stores only the URL.
- The video must exist, still be up, and be on topic.
- Age-restricted videos are rejected (above).

## How many resources per course

**No cap.** Quality is meant to sort itself out through visitor **thumbs-up** voting (agreed 2026-09-11;
see `COURSE_CATALOG_PLAN.md`, not built yet). Until that ships, keep listing anything that passes these
rules — and mention in the batch report when a course is collecting a lot of near-identical resources.

## Rejection notes are public

One short, neutral sentence a stranger can read: *"Not related to circuit analysis."* Never quote the
submitter, and never say anything about who they are.

## Summary style

Plain text, 2–5 sentences, 20–2000 characters. Say, in this order: what it is, what it covers, who it suits,
what it costs. Write for a student deciding whether to click.

> Free online textbook covering DC and AC circuit analysis, with worked examples and end-of-chapter
> questions. The DC chapters line up with the first half of this course. No account needed.

> Paid circuit-simulation software from National Instruments (Multisim), with a 30-day student trial.
> Useful for checking the designs built in this course's lab sections before wiring them up.

> Video lecture series from MIT OpenCourseWare, free and without an account. Pitched above this course —
> the treatment is calculus-heavy — but the first six lectures cover the same ground in more depth.

Avoid: marketing language, "the best", claims the page does not support, and anything about the submitter.
