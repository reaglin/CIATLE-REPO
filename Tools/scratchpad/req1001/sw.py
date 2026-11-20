import sys
sys.path.insert(0, '.')
import scns
for p in sys.argv[1:]:
    scns.report_csv(p, out='req1001/sw_%s.csv' % p)
    rows = scns.read_report_csv('req1001/sw_%s.csv' % p)
    print(p, len(rows), list(rows[0].keys()) if rows else None)
