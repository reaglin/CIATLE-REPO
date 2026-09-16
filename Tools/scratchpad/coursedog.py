#!/usr/bin/env python
"""Coursedog catalog client for the Florida schools that use it.

Rebuilt 2026-09-15 (batch 212) after the scratchpad caches were lost.

The gate is ONE header: Referer: https://<catalog host>/
Without it every endpoint returns {"error":"Unauthenticated"}.

Known Florida Coursedog schools (SOURCES.md batches 167 and 173):

    fiu    catalog.fiu.edu    fiu_peoplesoft     g6m34J5gUCpRQCPvL0tJ   ~27,900 courses
    fscj   catalog.fscj.edu   fscj_peoplesoft    sGHd4uJQXFdgDUaffhTv   ~22,700 courses
    nwfsc  catalog.nwfsc.edu  nwfsc_banner_sql   DGLrTHoh5uNIMFsdbzWf    ~1,780 courses

    fau    catalog.fau.edu    fau_banner_ethos   Zm7WidFIJix2TYXQumos

CORRECTION 2026-09-16 (batch 228): FAU IS now a Coursedog school. The batch-173
finding ("host registered but no catalog assigned") was TRUE THEN and is STALE --
FAU has since attached a catalog. Re-run `discover` on a host recorded as
unattached before trusting that record; the answer can change.

Usage:
    python coursedog.py discover catalog.somewhere.edu   # bootstrap a new school
    python coursedog.py dump fiu                         # page the whole catalog to JSON
    python coursedog.py find fiu ATT1110                 # look up one course
"""
import json
import os
import sys
import time

import requests

BASE = "https://app.coursedog.com"
HERE = os.path.dirname(os.path.abspath(__file__))

# limit is capped server-side at 5000 and a larger request returns a PARTIAL
# result SILENTLY (batch 173). Always page.
PAGE = 5000

SCHOOLS = {
    "fiu": {
        "host": "catalog.fiu.edu",
        "school": "fiu_peoplesoft",
        "catalog": "g6m34J5gUCpRQCPvL0tJ",
        "cache": "fiu_courses.json",
    },
    "fau": {
        "host": "catalog.fau.edu",
        "school": "fau_banner_ethos",
        "catalog": "Zm7WidFIJix2TYXQumos",
        "cache": "fau_courses.json",
    },
    "fscj": {
        "host": "catalog.fscj.edu",
        "school": "fscj_peoplesoft",
        "catalog": "sGHd4uJQXFdgDUaffhTv",
        "cache": "fscj_courses.json",
    },
    "nwfsc": {
        "host": "catalog.nwfsc.edu",
        "school": "nwfsc_banner_sql",
        "catalog": "DGLrTHoh5uNIMFsdbzWf",
        "cache": "nwfsc_courses.json",
    },
}


def _headers(host):
    # The gate was ONE header (Referer) when this was cracked in batch 167.
    # As of 2026-09-15 the course-search endpoint ALSO requires Origin --
    # Referer alone now returns 401 Unauthorized, while the bootstrap
    # endpoint still accepts Referer on its own. Send both everywhere.
    return {
        "Referer": "https://%s/" % host,
        "Origin": "https://%s" % host,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
    }


def discover(host):
    """Bootstrap: one call returns the school id and the catalog id."""
    host = host.replace("https://", "").replace("http://", "").strip("/")
    url = "%s/api/v1/catalogs/urls?url=%s" % (BASE, host)
    r = requests.get(url, headers=_headers(host), timeout=60)
    try:
        return r.json()
    except ValueError:
        return {"status": r.status_code, "body": r.text[:400]}


def _page(cfg, skip, limit):
    url = "%s/api/v1/cm/%s/courses/search/$filters" % (BASE, cfg["school"])
    params = {"catalogId": cfg["catalog"], "skip": skip, "limit": limit}
    r = requests.get(url, headers=_headers(cfg["host"]), params=params, timeout=180)
    r.raise_for_status()
    return r.json()


def fetch_all(key, verbose=True):
    """Page the ENTIRE catalog. Returns a list of course records."""
    cfg = SCHOOLS[key]
    first = _page(cfg, 0, PAGE)
    total = first.get("listLength", 0)
    out = list(first.get("data", []) or [])
    if verbose:
        print("  %s: listLength=%d, first page=%d" % (key, total, len(out)), flush=True)
    while len(out) < total:
        batch = _page(cfg, len(out), PAGE)
        rows = batch.get("data", []) or []
        if not rows:
            break
        out.extend(rows)
        if verbose:
            print("  %s: %d / %d" % (key, len(out), total), flush=True)
        time.sleep(0.5)
    return out


def cache_path(key):
    return os.path.join(HERE, SCHOOLS[key]["cache"])


def dump(key):
    rows = fetch_all(key)
    path = cache_path(key)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rows, fh)
    print("wrote %s (%d courses, %.1f MB)"
          % (path, len(rows), os.path.getsize(path) / 1e6), flush=True)
    return rows


def load(key):
    """Load the cache, fetching it first if it is missing."""
    path = cache_path(key)
    if not os.path.exists(path):
        return dump(key)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def find(key, code):
    """Look a course up in the cache.

    NOTE the data is messy in a specific way: the SAME code appears multiple
    times with different colleges and credit values. Prefer the row with a real
    college name AND a populated description -- this sorts those first.
    """
    want = code.replace(" ", "").upper()
    hits = []
    for c in load(key):
        got = (c.get("code") or "").replace(" ", "").upper()
        if got == want:
            hits.append(c)
    hits.sort(key=lambda c: (not (c.get("description") or ""),
                             not (c.get("college") or "")))
    return hits


def _main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    if cmd == "discover":
        print(json.dumps(discover(sys.argv[2]), indent=2))
    elif cmd == "dump":
        keys = sys.argv[2:] or list(SCHOOLS)
        for k in keys:
            dump(k)
    elif cmd == "find":
        for c in find(sys.argv[2], sys.argv[3]):
            print(json.dumps({k: c.get(k) for k in
                              ("code", "name", "credits", "college",
                               "description", "cipCode", "career")}, indent=2))
    else:
        print(__doc__)


if __name__ == "__main__":
    _main()
