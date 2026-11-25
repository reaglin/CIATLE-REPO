"""Batch 258: which related courses have a live guide (for links in BME4057C's guide)."""
import json
import sys
import urllib.request

BASE = "https://floridacourserepo.com/api/v1/courses/%s/guide"
for cid in sys.argv[1:]:
    try:
        r = urllib.request.urlopen(urllib.request.Request(BASE % cid, headers={"User-Agent": "fcr-tools"}), timeout=20)
        d = json.loads(r.read().decode("utf-8"))
        data = d.get("data") or {}
        print(cid, "GUIDE", (data.get("title") or "")[:60], len(data.get("htmlContent") or data.get("html_content") or ""))
    except Exception as e:  # noqa: BLE001
        print(cid, "none", e)
