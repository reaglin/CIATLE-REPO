#!/usr/bin/env python
"""Validate and push career paths to floridacourserepo.com.

Career paths are authored as JSON in `career_paths/<slug>.json` and pushed over
`PUT /api/v1/career-paths/{slug}`, exactly the shape the guide pipeline uses:
write the document, validate it locally against the server's own rules, then
push. This file is the validator and the pusher; the content standard lives in
CAREER_PATHS_PLAN.md and CLAUDE.md.

    python career_paths.py validate                # every authored path
    python career_paths.py validate registered-nurse
    python career_paths.py push registered-nurse   # one path, live
    python career_paths.py push --all --yes
    python career_paths.py list                    # what is live now

⚠⚠⚠ A PATH IS CURATED, NEVER DERIVED. Every course on a path is placed by an
author with a stated reason. Nothing here reads prerequisites, parses course
codes, or consults the institution CIP data -- two hundred batches of guide work
established that a course number does not identify a course, and a path
assembled mechanically would be confidently wrong about exactly the cases that
matter.

⚠⚠ A PATH MUST NOT POINT AT A PAGE THAT IS NOT THERE. The push response
carries `unlistedCourses` -- courses the path names that the catalog does not
carry. Send their base data (COURSE_API.md, `POST /api/v1/courses/batch`) before
publishing, or the reader clicks through to nothing.

⚠ ACCREDITATION OUTRANKS CREDIT. `credentialNote` renders ABOVE the course list
because a student can hold credit for every course on a path and still not
qualify -- NCLEX-RN eligibility runs through an APPROVED PROGRAMME, not through
accumulated transferable credit. Where that is true, say it there.
"""
import argparse
import csv
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
PATHS_DIR = os.path.join(HERE, "career_paths")
BASE_URL = os.environ.get("REPO_BASE_URL", "https://floridacourserepo.com").rstrip("/")

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
COURSE_RE = re.compile(r"^[A-Z]{3}\d{4}[A-Z]?(-(SCNS|[A-Z]{2,5}))?$")
CIP_RE = re.compile(r"^\d{2}\.\d{2}$")
SOC_RE = re.compile(r"^\d{2}-\d{4}$")

# Mirrors UpsertCareerPathRequestValidator exactly, so a clean validate means the
# push will not come back 400.
LIMITS = {
    "name": 200,
    "description": 2000,
    "credentialNote": 2000,
    "reason": 500,
    "variantNote": 1000,
    "label": 200,
    "url": 2048,
    "note": 500,
}
MAX_COURSES = 120
MAX_SOURCES = 40
MAX_CIPS = 30


def load(slug):
    p = os.path.join(PATHS_DIR, slug + ".json")
    if not os.path.exists(p):
        return None, ["no such file: %s" % os.path.relpath(p, HERE)]
    try:
        return json.load(io.open(p, encoding="utf-8")), []
    except ValueError as e:
        return None, ["not valid JSON: %s" % e]


def authored():
    if not os.path.isdir(PATHS_DIR):
        return []
    return sorted(f[:-5] for f in os.listdir(PATHS_DIR) if f.endswith(".json"))


def check(slug, doc):
    """Return (errors, warnings). Errors block a push; warnings are for the author."""
    err, warn = [], []

    if not SLUG_RE.match(slug):
        err.append("slug %r must be lowercase words separated by hyphens" % slug)

    for field in ("name", "cipCode", "description"):
        if not (doc.get(field) or "").strip():
            err.append("%s is required" % field)

    for field in ("name", "description", "credentialNote"):
        v = doc.get(field)
        if v and len(v) > LIMITS[field]:
            err.append("%s is %d chars, limit %d" % (field, len(v), LIMITS[field]))

    cip = (doc.get("cipCode") or "").strip()
    if cip and not CIP_RE.match(cip):
        err.append("cipCode %r must be a 4-digit CIP group, e.g. 51.38" % cip)

    soc = (doc.get("socCode") or "").strip()
    if soc and not SOC_RE.match(soc):
        err.append("socCode %r must look like 29-1141, or be omitted" % soc)

    # ⚠ A path may be filed under several CIP groups. Ron, 2026-09-17, on Lawyer:
    # "use those as the CIP codes that would go with the career path". Some
    # destinations have no single feeder programme, and filing them under one code
    # would assert a route that does not exist.
    cips = doc.get("cipCodes") or []
    if len(cips) > MAX_CIPS:
        err.append("%d cipCodes, limit %d" % (len(cips), MAX_CIPS))
    seen_cip = set()
    for i, c in enumerate(cips):
        code = (c.get("cipCode") or "").strip()
        if not CIP_RE.match(code):
            err.append("cipCodes[%d]: %r must be a 4-digit CIP group, e.g. 45.10" % (i, code))
        if code in seen_cip:
            err.append("cipCodes[%d]: %s appears twice" % (i, code))
        seen_cip.add(code)
        note = c.get("note")
        if note and len(note) > LIMITS["note"]:
            err.append("cipCodes[%d] (%s): note is %d chars, limit %d"
                       % (i, code, len(note), LIMITS["note"]))
        elif not note:
            # Not fatal, but the note is where the EVIDENCE lives. A code with no
            # note is a code somebody thought looked related.
            warn.append("cipCodes[%d] (%s): no note -- say what the evidence is that "
                        "students actually come from this programme" % (i, code))

    courses = doc.get("courses") or []
    if len(courses) > MAX_COURSES:
        err.append("%d courses, limit %d" % (len(courses), MAX_COURSES))
    seen = set()
    for i, c in enumerate(courses):
        cid = (c.get("courseId") or "").strip().upper()
        if not COURSE_RE.match(cid):
            err.append("courses[%d]: %r is not an SCNS course id" % (i, cid))
        if cid in seen:
            err.append("courses[%d]: %s appears twice" % (i, cid))
        seen.add(cid)
        reason = (c.get("reason") or "").strip()
        if not reason:
            # ⚠ The one rule that is ours rather than the server's reason for being.
            err.append("courses[%d] (%s): reason is required -- why is this course here?" % (i, cid))
        elif len(reason) > LIMITS["reason"]:
            err.append("courses[%d] (%s): reason is %d chars, limit %d"
                       % (i, cid, len(reason), LIMITS["reason"]))
        vn = c.get("variantNote")
        if vn and len(vn) > LIMITS["variantNote"]:
            err.append("courses[%d] (%s): variantNote is %d chars, limit %d"
                       % (i, cid, len(vn), LIMITS["variantNote"]))

    sources = doc.get("sources") or []
    if len(sources) > MAX_SOURCES:
        err.append("%d sources, limit %d" % (len(sources), MAX_SOURCES))
    for i, s in enumerate(sources):
        if not (s.get("label") or "").strip():
            err.append("sources[%d]: label is required" % i)
        url = (s.get("url") or "").strip()
        if not url.startswith(("http://", "https://")):
            err.append("sources[%d]: url must be an absolute http(s) URL" % i)
        if len(url) > LIMITS["url"]:
            err.append("sources[%d]: url is %d chars, limit %d" % (i, len(url), LIMITS["url"]))
        note = s.get("note")
        if note and len(note) > LIMITS["note"]:
            err.append("sources[%d]: note is %d chars, limit %d" % (i, len(note), LIMITS["note"]))

    # ── Warnings: the content bar, not the server's rules ────────────────────
    if not sources:
        warn.append("no sources -- a path with no sources is an assertion, and this "
                    "project does not publish assertions")
    if not courses:
        warn.append("no courses placed")
    if doc.get("isPublished") and not doc.get("credentialNote"):
        warn.append("no credentialNote -- if the destination is licensed or needs an "
                    "accredited programme, that outranks the course list and belongs here")
    if len(courses) > 40:
        warn.append("%d courses -- a path is SELECTIVE, not a catalogue; the site already "
                    "lists every course" % len(courses))
    if not doc.get("isPublished"):
        warn.append("isPublished is false -- it will push, but stay invisible")

    return err, warn


def cmd_validate(args):
    slugs = args.slugs or authored()
    if not slugs:
        print("no authored paths in %s" % os.path.relpath(PATHS_DIR, HERE))
        return 1
    bad = 0
    for slug in slugs:
        doc, e = load(slug)
        if doc is None:
            print("FAIL %-28s %s" % (slug, e[0]))
            bad += 1
            continue
        err, warn = check(slug, doc)
        status = "FAIL" if err else "ok  "
        print("%s %-28s %d cip(s), %d course(s), %d source(s)"
              % (status, slug, 1 + len(doc.get("cipCodes") or []),
                 len(doc.get("courses") or []), len(doc.get("sources") or [])))
        for m in err:
            print("       ERROR   %s" % m)
        for m in warn:
            print("       warning %s" % m)
        if err:
            bad += 1
    print()
    print("%d of %d clean." % (len(slugs) - bad, len(slugs)))
    return 1 if bad else 0


def token(session):
    email = os.environ.get("REPO_ADMIN_EMAIL")
    password = os.environ.get("REPO_ADMIN_PASSWORD")
    if not email or not password:
        print("REPO_ADMIN_EMAIL and REPO_ADMIN_PASSWORD are required to push.")
        sys.exit(1)
    r = session.post("%s/api/v1/auth/login" % BASE_URL,
                     json={"email": email, "password": password}, timeout=20)
    r.raise_for_status()
    return r.json()["data"]["accessToken"]


def cmd_push(args):
    slugs = args.slugs or (authored() if args.all else [])
    if not slugs:
        print("nothing to push -- name a slug or pass --all")
        return 2

    docs = {}
    for slug in slugs:
        doc, e = load(slug)
        if doc is None:
            print("FAIL %-28s %s" % (slug, e[0]))
            return 1
        err, _ = check(slug, doc)
        if err:
            # Same rule as the guide pipeline: never push past a FAIL.
            print("FAIL %-28s %d error(s); run validate" % (slug, len(err)))
            return 1
        docs[slug] = doc

    print("About to push %d path(s) to %s:" % (len(docs), BASE_URL))
    for slug, d in docs.items():
        print("   %-28s %-40s %s" % (slug, d["name"],
                                     "published" if d.get("isPublished") else "UNPUBLISHED"))
    if not args.yes:
        if input("Proceed? [y/N] ").strip().lower() not in ("y", "yes"):
            print("aborted.")
            return 0

    s = requests.Session()
    try:
        tok = token(s)
    except requests.exceptions.ConnectionError:
        print("cannot reach %s -- is the site up, and is REPO_BASE_URL right?" % BASE_URL)
        return 1
    unlisted = set()
    for slug, doc in docs.items():
        body = {k: doc.get(k) for k in
                ("name", "cipCode", "description", "socCode", "credentialNote",
                 "bodyHtml", "isPublished", "sortOrder", "cipCodes", "courses", "sources")}
        r = s.put("%s/api/v1/career-paths/%s" % (BASE_URL, slug), json=body,
                  headers={"Authorization": "Bearer %s" % tok}, timeout=60)
        if r.status_code != 200:
            print("FAIL %-28s HTTP %s %s" % (slug, r.status_code, r.text[:400]))
            return 1
        d = r.json()["data"]
        print("%-4s %-28s %d cip(s), %d course(s), %d source(s)"
              % (d["outcome"], slug, d["cipCount"], d["courseCount"], d["sourceCount"]))
        for c in d.get("unlistedCourses") or []:
            unlisted.add(c)

    if unlisted:
        # ⚠ The path is live and these links go nowhere until the catalog carries them.
        print()
        print("⚠⚠ %d course(s) on these paths are NOT LISTED in the catalog:" % len(unlisted))
        print("   %s" % " ".join(sorted(unlisted)))
        print("   Send their base data (COURSE_API.md, POST /api/v1/courses/batch) -- "
              "until then the path links to a page that is not there.")
    return 0


def cmd_queue(args):
    """The top-50 queue with, per row, whether it is authored and whether it is live."""
    qp = os.path.join(PATHS_DIR, "QUEUE.csv")
    if not os.path.exists(qp):
        print("no queue at %s" % os.path.relpath(qp, HERE))
        return 1
    rows = list(csv.DictReader(io.open(qp, encoding="utf-8-sig")))

    have = set(authored())
    live = set()
    try:
        r = requests.get("%s/api/v1/career-paths" % BASE_URL, timeout=30)
        if r.status_code == 200:
            live = {i["slug"] for i in r.json()["data"]}
    except requests.exceptions.RequestException:
        print("(could not reach %s -- showing authored state only)" % BASE_URL)

    want = (args.cluster or "").upper()
    shown = 0
    for row in rows:
        if want and row["cluster"] != want:
            continue
        if args.ptype and row.get("type", "").upper() != args.ptype.upper():
            continue
        slug = row["slug"]
        state = "LIVE" if slug in live else ("drafted" if slug in have else "")
        flag = "" if row["cip_seeded"] == "yes" else "  ⚠ CIP not seeded"
        print("%3s %-4s %-7s %-34s %-7s %-9s %-8s%s"
              % (row["rank"], row["cluster"], row.get("type", ""), row["name"][:34],
                 row["cip"], row["soc"], state, flag))
        shown += 1

    done = sum(1 for r in rows if r["slug"] in live)
    print()
    print("%d of %d shown. %d live, %d drafted, %d not started."
          % (shown, len(rows), done,
             sum(1 for r in rows if r["slug"] in have and r["slug"] not in live),
             sum(1 for r in rows if r["slug"] not in have)))
    # The emphasis Ron set, kept visible so it does not quietly erode.
    me = [r for r in rows if r["cluster"] in ("ENG", "MFG")]
    print("manufacturing + engineering: %d of %d queued, %d live."
          % (len(me), len(rows), sum(1 for r in me if r["slug"] in live)))
    ch = [r for r in rows if r.get("type") == "CHOICE"]
    print("CHOICE paths (no single major -- the high-value research): %d queued, %d live."
          % (len(ch), sum(1 for r in ch if r["slug"] in live)))
    return 0


def cmd_list(args):
    try:
        r = requests.get("%s/api/v1/career-paths" % BASE_URL, timeout=30)
    except requests.exceptions.ConnectionError:
        print("cannot reach %s" % BASE_URL)
        return 1
    r.raise_for_status()
    items = r.json()["data"]
    if not items:
        print("no published career paths.")
        return 0
    print("%d published path(s):" % len(items))
    for i in items:
        print("   %-28s %-8s %-38s %d course(s)"
              % (i["slug"], i["cipCode"], i["name"], i["courseCount"]))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    sub = ap.add_subparsers(dest="cmd")

    v = sub.add_parser("validate", help="check authored paths against the server rules")
    v.add_argument("slugs", nargs="*")
    v.set_defaults(func=cmd_validate)

    p = sub.add_parser("push", help="push authored paths to the live site")
    p.add_argument("slugs", nargs="*")
    p.add_argument("--all", action="store_true")
    p.add_argument("--yes", action="store_true", help="skip the confirmation")
    p.set_defaults(func=cmd_push)

    l = sub.add_parser("list", help="what is published now")
    l.set_defaults(func=cmd_list)

    q = sub.add_parser("queue", help="the top-50 queue and how far through it we are")
    q.add_argument("--cluster", help="ENG MFG HLT CMP BUS LAW EDU PUB")
    q.add_argument("--type", dest="ptype", help="DIRECT or CHOICE")
    q.set_defaults(func=cmd_queue)

    args = ap.parse_args()
    if not getattr(args, "func", None):
        ap.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
