#!/usr/bin/env python
"""Validate and push programmes to floridacourserepo.com.

A programme is "a major that supports a career path and is being offered by a
Florida school" (Ron, 2026-09-17) — one level ABOVE a degree, so Nursing covers
the LPN certificate, the A.S. and the BSN. Programmes are authored as JSON in
`programs/<slug>.json` and pushed over `PUT /api/v1/programs/{slug}`, the same
shape as guides and career paths: write the document, validate it locally
against the server's own rules, then push.

    python programs.py validate                # every authored programme
    python programs.py validate nursing
    python programs.py push nursing            # one programme, LIVE
    python programs.py push --all --yes
    python programs.py list                    # what is live now
    python programs.py show nursing            # the schools its codes find
    python programs.py delete nursing          # asks first; refused while a path names it

The file IS the request body, and the FILENAME is the slug — no `slug` key goes
inside the document. Credentials come from `Tools/.env` (`REPO_ADMIN_EMAIL`,
`REPO_ADMIN_PASSWORD`), which this script loads by itself. To rehearse against a
local site instead of production, set `REPO_BASE_URL=http://localhost:5199`.

⚠⚠ A PROGRAMME OWNS NO SCHOOL LIST. Ron, 2026-09-17: "I am going to decouple
programs from schools." Which institutions offer it is derived from the federal
IPEDS award table by CIP prefix, every time the page is read. So the ONLY thing
this document decides is which CIP codes the programme covers — and that choice
IS the school list.

⚠⚠⚠ WHICH CODES YOU CLAIM DECIDES WHO IS VISIBLE. Nursing defined as 51.38
alone finds 39 Florida public institutions; adding 51.39 (practical nursing)
finds 78 — and every one of the 39 it was missing is a technical college. Ron:
"I do not want a school to be excluded from being listed because their offerings
are limited." Put the evidence for each code in its `note`.

⚠ PUSH AND DELETE WRITE TO THE LIVE PUBLIC SITE. The codes are replaced
wholesale, so dropping one takes its schools off a live page — the push shows
what is live now against what it is about to send, and says so when the set
shrinks.

⚠ BEFORE 2026-09-19 programmes could only be added by redeploying the site
(`Data/Seed/programs.json` ships inside the build). That file now BOOTSTRAPS a
fresh database and nothing more — an existing programme is left alone by the
seed, and this pipeline owns it.
"""
import argparse
import io
import json
import os
import re
import sys

try:
    import requests
except ImportError:
    print("requests is required: pip install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
except ImportError:
    pass

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
PROGRAMS_DIR = os.path.join(HERE, "programs")
CIP_SEED = os.path.join(HERE, "..", "PreseMakerRepo.Api", "Data", "Seed", "cip.json")
BASE_URL = os.environ.get("REPO_BASE_URL", "https://floridacourserepo.com").rstrip("/")

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# ⚠⚠ Whole levels only — a series (15 or 15.), a group (51.38), or one 6-digit
# code (14.1901). The gap is deliberate: codes are matched with startswith, so
# "14.1" would sweep in 14.10 through 14.19 — electrical engineering along with
# mechanical. Mirrors ProgramCipInputValidator.
CIP_RE = re.compile(r"^\d{2}\.?$|^\d{2}\.\d{2}$|^\d{2}\.\d{4}$")

# Mirrors UpsertProgramRequestValidator exactly, so a clean validate means the
# push will not be refused for shape -- and, when cip.json is readable, not for
# an unknown code either.
LIMITS = {"name": 200, "description": 2000, "degreesNote": 2000, "note": 500}
MAX_CIPS = 40

FIELDS = ("name", "description", "degreesNote", "bodyHtml",
          "isPublished", "sortOrder", "cips")

# What to do next, per server error code. The code alone tells a first-time
# user nothing; these say where the fix lives and whether it needs a deploy.
NEXT_STEP = {
    "PROGRAM_IN_USE":
        "Edit those path documents in career_paths/ to drop this programme, run\n"
        "        python career_paths.py push <path-slug>\n"
        "        and then delete it again.",
    "CIP_NODE_NOT_FOUND":
        "⚠ This one cannot be fixed from here: add the group to EXTRA_GROUPS in\n"
        "        Tools/build_cip_seed.py with the reason, re-run it to regenerate\n"
        "        cip.json, AND REDEPLOY THE SITE — the tree ships inside the build.",
    "PROGRAM_NOT_FOUND":
        "If you pushed it with isPublished: false it exists but is hidden --\n"
        "        add --include-drafts. Otherwise `python programs.py list` shows\n"
        "        what is there.",
    "VALIDATION_ERROR":
        "Fix the document and run `python programs.py validate <slug>` — a clean\n"
        "        validate means the push will not be refused for shape.",
}


def fail(r, what):
    """Print a server refusal in words, not as a JSON envelope."""
    body = None
    try:
        body = r.json()
    except ValueError:
        pass

    if not isinstance(body, dict) or "error" not in body:
        # Not our envelope: an HTML error page, a proxy, a wrong base URL.
        print("FAIL %s -- HTTP %s" % (what, r.status_code))
        print("     %s" % (r.text or "")[:300].replace("\n", " "))
        if r.status_code in (404, 405):
            print("     The programmes endpoint may not be deployed yet -- see")
            print("     Deployment/PENDING_SERVER_CHANGES.md.")
        return 1

    err = body.get("error") or {}
    code = err.get("code") or "HTTP %s" % r.status_code
    print("FAIL %s -- %s (HTTP %s)" % (what, code, r.status_code))
    if err.get("message"):
        print("     %s" % err["message"])
    for f in err.get("fields") or err.get("details") or []:
        if isinstance(f, dict):
            print("       %s: %s" % (f.get("field") or f.get("property") or "?",
                                     f.get("message")))
    if r.status_code in (401, 403):
        print("     The REPO_ADMIN_EMAIL / REPO_ADMIN_PASSWORD in Tools/.env were "
              "rejected,\n     or that account is not an administrator.")
    elif code in NEXT_STEP:
        print("     %s" % NEXT_STEP[code])
    return 1


def unreachable():
    print("cannot reach %s" % BASE_URL)
    print("   Is the site up, and is REPO_BASE_URL right? It is unset by default, "
          "which means production.")
    return 1


def seeded_cips():
    """The CIP codes the site will accept, read from the seed that ships with it.

    ⚠ Returns None when the file cannot be read, so the caller can degrade to a
    warning rather than inventing an error.
    """
    try:
        d = json.load(io.open(CIP_SEED, encoding="utf-8"))
    except (IOError, OSError, ValueError):
        return None
    return {n["code"] for n in d.get("nodes") or []}


def normalize(code):
    """The tree node a code is checked against -- the server's own rule.

    "15." -> "15", and a 6-digit code -> its 4-digit group, since the seeded
    tree stops at four digits.
    """
    code = code.strip().rstrip(".")
    return code[:5] if len(code) == 7 else code


def load(slug):
    p = os.path.join(PROGRAMS_DIR, slug + ".json")
    if not os.path.exists(p):
        return None, ["no such file: %s" % os.path.relpath(p, HERE)]
    try:
        return json.load(io.open(p, encoding="utf-8")), []
    except ValueError as e:
        return None, ["not valid JSON: %s" % e]


def authored():
    if not os.path.isdir(PROGRAMS_DIR):
        return []
    return sorted(f[:-5] for f in os.listdir(PROGRAMS_DIR) if f.endswith(".json"))


def check(slug, doc, tree=None):
    """Return (errors, warnings). Errors block a push; warnings are for the author."""
    err, warn = [], []

    if not SLUG_RE.match(slug):
        err.append("slug %r must be lowercase words separated by hyphens" % slug)

    for field in ("name", "description"):
        if not (doc.get(field) or "").strip():
            err.append("%s is required" % field)

    for field in ("name", "description", "degreesNote"):
        v = doc.get(field)
        if v and len(v) > LIMITS[field]:
            err.append("%s is %d chars, limit %d" % (field, len(v), LIMITS[field]))

    cips = doc.get("cips") or []
    if not cips:
        # ⚠ A programme with no code claims no schools, and the page would then
        # tell a reader a real programme is offered nowhere.
        err.append("cips is required -- the CIP codes ARE the school list")
    if len(cips) > MAX_CIPS:
        err.append("%d cips, limit %d" % (len(cips), MAX_CIPS))

    seen = set()
    for i, c in enumerate(cips):
        code = (c.get("cipCode") or "").strip()
        if not CIP_RE.match(code):
            err.append("cips[%d]: %r must be a whole level -- a series (15 or 15.), "
                       "a group (51.38) or one 6-digit code (14.1901). A part-code "
                       "like 14.1 matches a whole range of unrelated groups." % (i, code))
        elif tree is not None and normalize(code) not in tree:
            # ⚠⚠ The expensive failure, caught here instead of after a live push:
            # widening the tree means regenerating cip.json AND a redeploy.
            err.append("cips[%d]: %s is not in the seeded CIP tree -- the push will be "
                       "refused 422. Add the group to EXTRA_GROUPS in build_cip_seed.py "
                       "with the reason, regenerate cip.json, and redeploy." % (i, code))
        elif re.match(r"^\d{2}\.?$", code):
            # Accepted, but it claims a whole family: "51" is all of Health Professions.
            warn.append("cips[%d] (%s): this claims the WHOLE of family %s -- every award "
                        "beneath it. Name the groups instead unless that is deliberate, "
                        "and say why in the note." % (i, code, code.rstrip(".")))
        if code in seen:
            err.append("cips[%d]: %s appears twice" % (i, code))
        seen.add(code)
        note = c.get("note")
        if note and len(note) > LIMITS["note"]:
            err.append("cips[%d] (%s): note is %d chars, limit %d"
                       % (i, code, len(note), LIMITS["note"]))
        elif not note:
            warn.append("cips[%d] (%s): no note -- say why this code belongs to the "
                        "programme, since it decides which schools appear" % (i, code))

    if not (doc.get("degreesNote") or "").strip():
        warn.append("no degreesNote -- the level a student enters at (certificate, A.S., "
                    "bachelor's) is the decision they actually face")
    if not doc.get("isPublished"):
        warn.append("isPublished is false -- it will push, but stay invisible to readers")

    return err, warn


def cmd_validate(args):
    slugs = args.slugs or authored()
    if not slugs:
        print("no authored programmes in %s" % os.path.relpath(PROGRAMS_DIR, HERE))
        print("   A programme is one file: programs/<slug>.json. See PROGRAM_API.md.")
        return 1
    tree = seeded_cips()
    if tree is None:
        print("⚠ could not read %s -- CIP codes are checked for SHAPE only, so an "
              "unknown code will not surface until the push." % os.path.relpath(CIP_SEED, HERE))
    bad = 0
    for slug in slugs:
        doc, e = load(slug)
        if doc is None:
            print("FAIL %-28s %s" % (slug, e[0]))
            bad += 1
            continue
        err, warn = check(slug, doc, tree)
        print("%s %-28s %d cip(s)"
              % ("FAIL" if err else "ok  ", slug, len(doc.get("cips") or [])))
        for m in err:
            print("       ERROR   %s" % m)
        for m in warn:
            print("       warning %s" % m)
        if err:
            bad += 1
    print()
    print("%d of %d clean." % (len(slugs) - bad, len(slugs)))
    if not bad:
        print("next: python programs.py push %s" % (slugs[0] if len(slugs) == 1 else "--all"))
    return 1 if bad else 0


def token(session):
    email = os.environ.get("REPO_ADMIN_EMAIL")
    password = os.environ.get("REPO_ADMIN_PASSWORD")
    if not email or not password:
        print("REPO_ADMIN_EMAIL and REPO_ADMIN_PASSWORD are required to write.")
        print("   Set them in Tools/.env (this script loads it automatically) -- "
              "see PROGRAM_API.md, Authentication.")
        sys.exit(1)
    try:
        r = session.post("%s/api/v1/auth/login" % BASE_URL,
                         json={"email": email, "password": password}, timeout=20)
    except requests.exceptions.ConnectionError:
        unreachable()
        sys.exit(1)
    if r.status_code != 200:
        print("login to %s was refused (HTTP %s)." % (BASE_URL, r.status_code))
        print("   Check REPO_ADMIN_EMAIL / REPO_ADMIN_PASSWORD in Tools/.env.")
        sys.exit(1)
    return r.json()["data"]["accessToken"]


def live_state(slug, headers=None):
    """What is published right now, or None. Used to show a push its own baseline."""
    try:
        r = requests.get("%s/api/v1/programs/%s" % (BASE_URL, slug),
                         headers=headers or {}, timeout=30)
    except requests.exceptions.RequestException:
        return None
    if r.status_code != 200:
        return None
    try:
        return r.json()["data"]
    except (ValueError, KeyError):
        return None


def cmd_push(args):
    slugs = args.slugs or (authored() if args.all else [])
    if not slugs:
        print("nothing to push -- name a slug, or pass --all for every document in programs/")
        return 2
    if args.slugs and args.all:
        print("⚠ --all is ignored: pushing only the slug(s) named.")

    tree = seeded_cips()
    docs = {}
    for slug in slugs:
        doc, e = load(slug)
        if doc is None:
            print("FAIL %-28s %s" % (slug, e[0]))
            return 1
        err, _ = check(slug, doc, tree)
        if err:
            # Same rule as the guide pipeline: never push past a FAIL.
            print("FAIL %-28s will not push:" % slug)
            for m in err:
                print("       ERROR   %s" % m)
            return 1
        docs[slug] = doc

    # ⚠⚠ The CIP codes are REPLACED, and they are the whole school list -- so the
    # confirmation shows what is live against what is being sent, and names any
    # code that is about to disappear.
    print("About to push %d programme(s) to %s:" % (len(docs), BASE_URL))
    removals = {}
    for slug, d in docs.items():
        codes = [c.get("cipCode") for c in d.get("cips") or []]
        print("   %-24s %-30s %-12s %s"
              % (slug, d["name"][:30],
                 "published" if d.get("isPublished") else "UNPUBLISHED",
                 " ".join(codes)))
        cur = live_state(slug)
        if cur:
            gone = [c["cipCode"] for c in cur.get("cips") or []
                    if c["cipCode"] not in codes]
            print("        live now: %d cip(s), %d school(s)"
                  % (len(cur.get("cips") or []), len(cur.get("schools") or [])))
            if gone:
                removals[slug] = gone
                print("        ⚠⚠ THIS PUSH REMOVES: %s -- the schools those codes "
                      "find leave the page." % " ".join(gone))
        else:
            print("        not live yet -- this creates it.")

    if not args.yes:
        if input("Proceed? [y/N] ").strip().lower() not in ("y", "yes"):
            print("aborted -- nothing was sent.")
            return 1

    s = requests.Session()
    tok = token(s)

    unmatched = {}
    for slug, doc in docs.items():
        body = {k: doc.get(k) for k in FIELDS}
        try:
            r = s.put("%s/api/v1/programs/%s" % (BASE_URL, slug), json=body,
                      headers={"Authorization": "Bearer %s" % tok}, timeout=60)
        except requests.exceptions.ConnectionError:
            return unreachable()
        if r.status_code != 200:
            return fail(r, "push %s" % slug)
        d = r.json()["data"]
        print("%-8s %-24s %d cip(s), %d school(s)   %s/programs/%s"
              % (d["outcome"], slug, d["cipCount"], d["schoolCount"], BASE_URL, slug))
        if not doc.get("isPublished"):
            print("         ⚠ not visible to readers -- isPublished is false.")
        if d.get("unmatchedCips"):
            unmatched[slug] = d["unmatchedCips"]

    if unmatched:
        # ⚠ Not an error: a code can be real and have no Florida completions in the
        # award year. But a code matching nothing usually means the wrong code.
        print()
        print("⚠ CIP code(s) matching no award record at all:")
        for slug, codes in unmatched.items():
            print("   %-24s %s" % (slug, " ".join(codes)))
        print("   Check them -- until one matches, it adds no schools to the page.")
    return 0


def cmd_list(args):
    headers = {}
    url = "%s/api/v1/programs" % BASE_URL
    if args.include_drafts:
        s = requests.Session()
        headers = {"Authorization": "Bearer %s" % token(s)}
        url += "?includeUnpublished=true"
    try:
        r = requests.get(url, headers=headers, timeout=30)
    except requests.exceptions.ConnectionError:
        return unreachable()
    if r.status_code != 200:
        return fail(r, "list")
    items = r.json()["data"]
    if not items:
        print("no programmes published at %s." % BASE_URL)
        print("   Author one as programs/<slug>.json, then validate and push it.")
        return 0
    have = set(authored())
    print("%d programme(s) at %s:" % (len(items), BASE_URL))
    for i in items:
        print(("   %-24s %-30s %3d school(s)  %d cip(s)  %d path(s)  %-7s%s"
               % (i["slug"], ell(i["name"], 30), i["schoolCount"], i["cipCount"],
                  i["careerPathCount"],
                  "" if i.get("isPublished", True) else "DRAFT",
                  "" if i["slug"] in have else "  ⚠ no local document")).rstrip())
    missing = sorted(have - {i["slug"] for i in items})
    if missing:
        print()
        print("authored but not %s: %s"
              % ("live" if args.include_drafts else "published", " ".join(missing)))
        if not args.include_drafts:
            print("   (a programme pushed with isPublished: false is hidden here -- "
                  "run `list --include-drafts`)")
    return 0


def cmd_show(args):
    headers = {}
    if args.include_drafts:
        headers = {"Authorization": "Bearer %s" % token(requests.Session())}
    try:
        r = requests.get("%s/api/v1/programs/%s" % (BASE_URL, args.slug),
                         headers=headers, timeout=60)
    except requests.exceptions.ConnectionError:
        return unreachable()
    if r.status_code != 200:
        return fail(r, "show %s" % args.slug)
    d = r.json()["data"]
    print("%s — %s   %s/programs/%s" % (d["slug"], d["name"], BASE_URL, d["slug"]))
    print(d["description"])
    print()
    for c in d["cips"]:
        print("   %-9s %-52s %3d school(s)"
              % (c["cipCode"], ell(c["cipTitle"] or "", 52), c["schoolCount"]))
    print()
    if not d["schools"]:
        # The one diagnostic that matters most, and it used to print as blanks.
        print("⚠⚠ These CIP codes matched NO Florida award record, so the page shows "
              "this\n   programme as offered nowhere. Check the codes -- see "
              "PROGRAM_API.md on unmatchedCips.")
    else:
        print("%d school(s), award levels: %s (IPEDS %s)"
              % (len(d["schools"]), ", ".join(d["awardLevels"]), d["awardYear"]))
        if args.schools:
            for s in d["schools"]:
                print("   %-58s %s" % (ell(s["name"], 58), ", ".join(s["awards"])))
        else:
            print("   (add --schools to name them)")
    if d["careerPaths"]:
        print("career paths: %s" % " ".join(p["slug"] for p in d["careerPaths"]))
    return 0


def cmd_delete(args):
    # ⚠⚠ A delete removes a live public page. Show what is about to go, and ask --
    # the same courtesy push already extends for a far smaller change.
    cur = live_state(args.slug)
    print("About to DELETE from %s:" % BASE_URL)
    if cur:
        print("   %-24s %-30s %d cip(s), %d school(s)"
              % (cur["slug"], cur["name"][:30], len(cur.get("cips") or []),
                 len(cur.get("schools") or [])))
        if cur.get("careerPaths"):
            print("   ⚠ named by career path(s): %s -- the server will refuse this "
                  "until they are updated." % " ".join(p["slug"] for p in cur["careerPaths"]))
    else:
        print("   %-24s (not published, or not there -- the server will say which)"
              % args.slug)
    if os.path.exists(os.path.join(PROGRAMS_DIR, args.slug + ".json")):
        print("   The local document programs/%s.json is untouched: `push %s` "
              "recreates it." % (args.slug, args.slug))
    else:
        print("   ⚠⚠ There is NO local document programs/%s.json -- once deleted, "
              "this programme\n      can only come back from the seed file, and only "
              "if it is in it." % args.slug)

    if not args.yes:
        if input("Delete it? [y/N] ").strip().lower() not in ("y", "yes"):
            print("aborted -- nothing was deleted.")
            return 1

    s = requests.Session()
    tok = token(s)
    try:
        r = s.delete("%s/api/v1/programs/%s" % (BASE_URL, args.slug),
                     headers={"Authorization": "Bearer %s" % tok}, timeout=30)
    except requests.exceptions.ConnectionError:
        return unreachable()
    if r.status_code == 200:
        print("deleted %s" % args.slug)
        return 0
    return fail(r, "delete %s" % args.slug)


def ell(s, n):
    """Truncate with an ellipsis, so a cut value never reads as the real one."""
    return s if len(s) <= n else s[:n - 1] + "…"


def main():
    ap = argparse.ArgumentParser(
        description=__doc__.strip().split("\n")[0],
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")

    v = sub.add_parser("validate", help="check authored programmes against the server rules")
    v.add_argument("slugs", nargs="*", help="default: every document in programs/")
    v.set_defaults(func=cmd_validate)

    p = sub.add_parser("push", help="send programmes to the site (WRITES; asks first)")
    p.add_argument("slugs", nargs="*")
    p.add_argument("--all", action="store_true", help="every document in programs/")
    p.add_argument("--yes", action="store_true", help="skip the confirmation")
    p.set_defaults(func=cmd_push)

    l = sub.add_parser("list", help="what is published now")
    l.add_argument("--include-drafts", action="store_true",
                   help="also show unpublished programmes (needs admin credentials)")
    l.set_defaults(func=cmd_list)

    sh = sub.add_parser("show", help="one programme and the schools its codes find")
    sh.add_argument("slug")
    sh.add_argument("--schools", action="store_true", help="name every school")
    sh.add_argument("--include-drafts", action="store_true",
                    help="look for an unpublished programme too (needs admin credentials)")
    sh.set_defaults(func=cmd_show)

    d = sub.add_parser("delete", help="remove a programme (WRITES; asks first)")
    d.add_argument("slug")
    d.add_argument("--yes", action="store_true", help="skip the confirmation")
    d.set_defaults(func=cmd_delete)

    args = ap.parse_args()
    if not getattr(args, "func", None):
        ap.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
