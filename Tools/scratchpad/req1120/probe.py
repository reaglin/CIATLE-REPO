"""Probe floridapoly.edu for posted syllabi of a course (HEAD requests only)."""
import itertools
import sys
import urllib.request

YEARS = ['2025/01', '2025/08', '2025/09', '2026/01', '2026/02', '2026/08', '2026/09',
         '2024/08', '2025/05', '2026/05']
TERMS = ['FA-2025', 'SP-2026', 'FA-2026', 'SP-2025', 'SU-2026', 'FA-2024', 'SU-2025']
SECTIONS = ['01', '02', '03']

found = []
for course in sys.argv[1:]:
    for y, t, s in itertools.product(YEARS, TERMS, SECTIONS):
        u = 'https://floridapoly.edu/wp-content/uploads/%s/%s-%s_%s.pdf' % (y, course, s, t)
        try:
            req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0', 'Range': 'bytes=0-0'})
            r = urllib.request.urlopen(req, timeout=15)
            if r.status in (200, 206):
                print('FOUND', u)
                found.append(u)
        except Exception:
            pass
print('done', len(found))
