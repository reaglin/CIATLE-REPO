"""Batch 258: fetch USF course pages for BME4057C (and its partner BME4056C) and print the text."""
import html
import os
import re
import sys
import urllib.request

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b258")
os.makedirs(OUT, exist_ok=True)

URLS = sys.argv[1:] or [
    "https://cloud.usf.edu/academic-programs/details/prefix/BME/code/4057C",
    "https://cloud.usf.edu/academic-programs/details/prefix/BME/code/4056C",
]

for i, url in enumerate(URLS):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        print(url, "FAILED", e)
        continue
    with open(os.path.join(OUT, f"page{i}.html"), "w", encoding="utf-8") as f:
        f.write(raw)
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = re.sub(r"\s+", " ", t)
    m = re.search(r"\b[A-Z]{3} ?\d{4}[A-Z]?\b", t)
    start = 0
    for key in ("Description", "Credit"):
        j = t.find(key)
        if j > 0:
            start = max(0, j - 400)
            break
    print("URL:", url, "len", len(raw))
    print(t[start:start + 3000])
    print("=" * 40)
