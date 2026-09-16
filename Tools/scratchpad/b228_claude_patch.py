"""Batch 228 edits to Tools/CLAUDE.md. Run once from Tools/scratchpad."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CLAUDE.md')
s = io.open(P, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


# --- 1. FAU: register entry was correct then and is STALE now ---------------
rep(
"""| **FAU** | `catalog.fau.edu` — Coursedog SPA | ❌ **ANSWERED 2026-09-07: no public Coursedog catalog at that host.** The discovery endpoint returns *"does not have entity assigned"* — the host is registered but no catalog is attached, which is why every schoolId guess failed. **Stop attempting FAU via Coursedog.** |""",
"""| **FAU** | Coursedog — `scratchpad/coursedog.py fau` (school `fau_banner_ethos`, catalog `Zm7WidFIJix2TYXQumos`) | ✅✅ **REOPENED 2026-09-16 (batch 228). 7,127 courses, cached in `scratchpad/fau_courses.json`.** ⚠⚠⚠ **This row previously read "no public Coursedog catalog at that host… Stop attempting FAU." That was TRUE when written (batch 173) and is now STALE — FAU has since attached a catalog.** Full descriptions, credits, college and department, and **explicit corequisite text** (it is what showed `BSC1010`/`BSC1010L` to be reciprocal). Honors College versions appear under the same number. **FAU is a large SUS institution that the project had written off; it is now a first-class source.** |""")

# --- 2. The general lesson from the FAU correction --------------------------
rep(
"""### ⚠ How to probe a block correctly (learned batch 164)""",
"""### ⚠⚠⚠ A "CLOSED" REGISTER ENTRY GOES STALE — re-probe before trusting a negative (batch 228)

**The register is full of confident negatives, and at least one was wrong by the time it was
being relied on.** `catalog.fau.edu` was recorded in batch 173 as a registered host with **no
catalog attached**, ending *"Stop attempting FAU via Coursedog."* ⚠⚠ **In batch 228 the same
one-line bootstrap returned `fau_banner_ethos` and a live catalog id, and a full dump produced
7,127 courses.** The institution attached a catalog in the interval.

⚠ **The distinction that matters: a negative about a SERVER'S CONFIGURATION is perishable; a
negative about a PLATFORM'S BEHAVIOUR is not.** "acalog blocks `content.php`" is a property of the
platform and holds. "This host has no catalog attached" is a property of one institution's setup on
one day and can change without notice.

**Standing practice:**

- **Re-run `coursedog.py discover` on any host recorded as unattached** before writing a guide that
  names it as unreachable. It is one request.
- ⚠ **Do the same for the SmartCatalogIQ and CourseLeaf leads recorded as "not yet exercised"** —
  batch 228 exercised the IRSC one and it worked (below).
- **When a negative turns out to be stale, replace the row and say when it changed**, rather than
  softening it — the next session needs to know the entry is now positive, not hedged.

### ⚠ How to probe a block correctly (learned batch 164)""")

# --- 3. IRSC: lead exercised, PDF route works -------------------------------
rep(
"""| **IRSC** | `irsc.smartcatalogiq.com` | ⚠ **Live lead — SmartCatalogIQ, the same platform as the DSC build**, `/en/<year>/catalog/…`. Not yet exercised. |""",
"""| **IRSC** | **`irsc.smartcatalogiq.com/-/media/institution/irsc/pdf-catalogs-2011-12-through-2024-25/Indian%20River%20State%20College%20<YEAR>.pdf`** | ✅✅ **EXERCISED AND WORKING 2026-09-16 (batch 228) — but NOT the way the lead assumed.** The `/en/<year>/catalog/…` SmartCatalogIQ path **404s**; the root page instead links **whole-catalogue PDFs by year**, and the 2024-2025 file downloads clean (**3.2 MB, 303 pages**). Full course descriptions with prerequisites AND corequisites, and — because it is the whole catalogue — **programme prerequisite tables too**, which is how `MCB2010`'s gate was found. ⚠ Parse with `pypdf`; it emits "Ignoring wrong pointing object" warnings that are harmless. **Contrast UNF, where the archived-PDF route is the same idea and is 403-blocked: here it is simply open.** |""")

# --- 4. Gulf Coast recovered, and publishes contact hours -------------------
rep(
"""| Gulf Coast | `gulfcoast.edu/catalog/current/courses/<prefix>/index.html` | was the highest-value pattern in the DSC build; **re-probe before use** |""",
"""| **Gulf Coast (GCSC)** | `www.gulfcoast.edu/catalog/current/courses/<prefix>/index.html` | ✅✅ **RE-PROBED AND WORKING 2026-09-16 (batch 228)** — one fetch per prefix, 131 KB on `bsc`. ⚠⚠ **It is the SECOND Florida source that publishes CONTACT HOURS explicitly** (after Broward): every entry carries `Credit hours: N` plus `Lecture hours: N` and/or `Lab hours: N`. **It also publishes LAB FEES in dollars, term availability, and degree-exclusion rules** (*"cannot be used to satisfy degree requirements by students who already have credit in…"*), none of which any other routine source gives. **Go here whenever a contact-hour or fee figure is in doubt.** |""")

# --- 5. A 1-credit L lab is NOT uniformly 45 hours --------------------------
rep(
"""### ⚠ Writing 1-credit LABORATORY guides (batch 189)""",
"""### ⚠⚠⚠ A 1-CREDIT `L` LAB IS NOT UNIFORMLY 45 HOURS — the majors/non-majors split is worth 15 (batch 228)

**The project has been publishing 1-credit laboratories at 45 contact hours by convention.
Gulf Coast State College publishes the real figures, and they are not the same:**

| Course | Published |
|---|---|
| `BSC2010L` — **majors** general biology lab | **3 lab hours** weekly → 45 |
| ⚠ `BSC1020L` — **non-majors** human biology lab | ⚠⚠ **2 lab hours** weekly → **30** |

⚠⚠ **Same college, same credit value, same prefix, and a 50% difference in scheduled time.**
**So "1 credit `L` = 45" is a ceiling rather than a default**, and the majors/non-majors distinction
is the thing that moves it.

**Handling: prefer a published figure, and where none exists ANCHOR the derivation on the closest
published comparator rather than on the bare convention.** `BSC1010L` was published at 45 because
Gulf Coast publishes 3 hours for the equivalent *majors* lab in the other numbering family — which is
a far better justification than "1:45 is the convention", and the guide says so.

⚠ **Check Broward and Gulf Coast before deriving any laboratory's hours.** Between them they cover a
large share of the high-enrolment lower-division laboratories.

### ⚠ Writing 1-credit LABORATORY guides (batch 189)""")

# --- 6. Guide requests cluster on SPLIT FAMILIES ----------------------------
rep(
"""   ⚠ **Two requests in a row (`CET1112`, `CET2127C`) landed on numbers with a divergence.** A request""",
"""   ⚠⚠⚠ **SHARPENED (batch 228): requests cluster on SPLIT FAMILIES, and the tell is that the
   OTHER half already has a guide.** Both requests received on 2026-09-16 were the **`L` halves**
   of numbers whose **integrated `C` twins were already published** — `BSC1010L` against a live
   `BSC1010C`, `BSC1020L` against a live `BSC1020C`. **The requester found the site's page for the
   packaging their institution does not use, and needed the other one.**

   ⚠⚠ **So a published `C` guide with no `L` guide (or the reverse) is a PREDICTOR of a future
   request, and it is a one-line check**: before closing a batch on a split-family number, look up
   whether the site holds the sibling. **Writing both halves at once costs far less than meeting the
   request later**, and the second guide reuses the whole survey.

   ⚠ **Two requests in a row (`CET1112`, `CET2127C`) landed on numbers with a divergence.** A request""")

# --- 7. Caution on the batch-184 same-institution-both-forms diagnostic -----
rep(
"""⚠ **An institution carrying BOTH forms is the clean signature of a course run in two shapes** — a lecture
section and an integrated section with a scheduled practicum or laboratory. **Write the `C` id, state the
contact-hour difference (60 vs 45), and tell the student to check which section they are in.**""",
"""⚠ **An institution carrying BOTH forms is the clean signature of a course run in two shapes** — a lecture
section and an integrated section with a scheduled practicum or laboratory. **Write the `C` id, state the
contact-hour difference (60 vs 45), and tell the student to check which section they are in.**

#### ⚠⚠ CHECK THE CREDITS FIRST — same-institution-both-forms does NOT always mean two shapes (batch 228)

**Valencia College carries `BSC1010` AND `BSC1010C`, which fires the diagnostic above. ⚠⚠ But BOTH
are 4 credits** — *Fundamentals of Biology Honors* on the bare number and *General Biology I* on the
`C`. **Four credits means both already include the laboratory, so the suffix is not separating
lecture from integrated at all: it is separating HONOURS from standard.**

⚠⚠⚠ **The diagnostic depends on a CREDIT DIFFERENCE, and it is not safe without one.** A lecture
and its integrated twin differ by the lab's credit (3 against 4, or 3 against 60 hours). **Two forms
at the SAME credit value are two versions of the same packaging** — honours, or a delivery-mode
split — **and describing them as lecture-versus-integrated would be simply wrong.**

**So the check runs: same institution carries both → compare the CREDITS → equal means look for
another explanation (honours, campus, delivery mode) before writing the two-shapes note.**""")

io.open(P, 'w', encoding='utf-8').write(s)
print('CLAUDE.md updated')
