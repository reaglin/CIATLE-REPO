# Resource approval rules

**⚠ DRAFT — Ron is writing this file. Items marked “TO DECIDE” are not settled; do not treat them as
policy.** Everything below that is not marked TO DECIDE follows from how the site works, and holds today.

These rules govern **what gets listed** on a course's Resources page. The mechanics — endpoints, payloads,
error codes — are in [`../RESOURCE_API.md`](../RESOURCE_API.md); the loop is the `/resources` skill.

---

## What a resource is

A website or YouTube video listed for a course. It may be:

- a **free resource** — course notes, a textbook, a video lecture, a simulator, practice problems;
- a **product** — something a vendor or sales agent offers that suits the course (a textbook, software, a
  lab kit, a paid course).

**Both are welcome.** The difference is disclosed, not hidden: the summary must say plainly whether the
resource is free, free with an account, freemium, or paid — and who offers it.

## Settled rules

1. **Look at the resource before deciding.** Fetch the page or video. Never approve, and never write a
   summary, from the URL or the submitter's note alone.
2. **Relevance to the course decides it.** A resource is listed for a course when it helps someone taking
   *that* course. Check against the course title and its curriculum guide.
3. **Rejection notes are public.** Write one short, neutral sentence a stranger can read: *“Not related to
   circuit analysis.”* Never quote the submitter, and never say anything about who they are.
4. **Say what it costs.** Free · free with an account · freemium · paid. Name the vendor for a product.
5. **Do not invent.** If the page cannot be reached or cannot be judged, leave the suggestion pending (or
   reject it as unreachable) rather than guessing.
6. **Cross-list deliberately.** List a resource for another course only when it genuinely helps that course,
   and give that course its own summary when the reason differs.

## TO DECIDE — Ron

- **Commercial resources:** any limits? (e.g. how many products per course, whether a vendor may suggest
  the same product across many courses, whether a paid resource needs a free alternative listed too.)
- **Quality bar for free resources:** is a personal blog post acceptable, or only institutional / recognised
  publishers?
- **Level:** should resources clearly above or below the course's level be rejected, or listed with a note?
- **Always reject** list to confirm: adult, gambling, malware / warning pages, essay mills and homework
  answer services, pirated textbooks, sites that are mostly advertising, dead links, paywalled pages with
  nothing visible.
- **Video length / age limits**, if any.
- **Duplicates:** when two links cover the same ground, list both or keep the better one?
- **How many resources** should one course carry before the bar rises?
- **Vendor identification:** should a vendor's own submissions be labelled as such in the summary?

## Summary style (working draft)

Plain text, 2–5 sentences, 20–2000 characters. Say, in this order: what it is, what it covers, who it suits,
what it costs. Write for a student deciding whether to click, not for a catalogue.

> Free online textbook covering DC and AC circuit analysis, with worked examples and end-of-chapter
> questions. The DC chapters line up with the first half of this course. No account needed.

> Paid simulation software from National Instruments (Multisim), free for students through a 30-day trial.
> Useful for checking the circuit designs built in the lab sections of this course.

Avoid: marketing language, “the best”, claims the page does not support, anything about the submitter.
