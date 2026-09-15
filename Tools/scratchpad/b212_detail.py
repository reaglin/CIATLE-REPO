"""Batch 212 detail: statewide descriptions, prereqs, and field distributions."""
import collections
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scns

HERE = os.path.dirname(os.path.abspath(__file__))
FLAT = os.path.join(HERE, 'crslist.txt')

# statewide CSV ID_Century is the last THREE digits only; the level digit is separate.
WANT = {
    'ATF': ['502', '511', '531', '500', '501', '510', '530'],
    'ATT': ['110', '130', '131', '134', '133'],
}


def show_csv(pfx):
    path = os.path.join(HERE, 'sw_%s.csv' % pfx)
    rows = scns.read_report_csv(path)
    print('################ %s statewide records' % pfx)
    for r in rows:
        if r['ID_Century'] not in WANT[pfx]:
            continue
        if r['CourseStatus'] != 'ACTIVE':
            continue
        print('-- %s%s  %s' % (pfx, r['ID_Century'], r['DS_Title']))
        print('   INTENT: %s' % (r.get('DS_Course_Intent1') or '')[:200])
        print('   DESC  : %s' % (r.get('Course') or '')[:900])
        print('   PREREQ: %s' % (r.get('DS_Prerequisites1') or '')[:300])
        print('   COREQ : %s' % (r.get('DS_Corequisites1') or '')[:200])
        print('   TRANS : %s   HS: %s   DE: %s'
              % (r.get('DS_Transferable1'), r.get('DS_High_School_Credit1'),
                 r.get('IN_Dual_Enrollment1')))
        print()


def distributions():
    """Batch-207 rule: compute the field's distribution across the prefix
    BEFORE treating it as a signal."""
    for pfx in ('ATF', 'ATT'):
        rows = list(scns.parse_flatfile(FLAT, prefix=pfx, active_only=True))
        print('==== %s flat-file rows=%d' % (pfx, len(rows)))
        for field in ('transferable', 'hs_credit', 'dual_enrollment'):
            c = collections.Counter(r[field] or '(blank)' for r in rows)
            print('   %-16s %s' % (field, dict(c.most_common(8))))
        # "(U)" marker in the statewide title
        u = sum(1 for r in rows if r['state_title'].rstrip().endswith('(U)'))
        print('   state_title ending "(U)": %d of %d rows' % (u, len(rows)))
        print()


def u_marker():
    """What does the '(U)' suffix in a statewide title mean? Check its
    correlation with the LEVEL digit across the whole flat file."""
    lvl = collections.Counter()
    tot = collections.Counter()
    for r in scns.parse_flatfile(FLAT, prefix=None, active_only=True):
        st = r['state_title'].rstrip()
        tot[r['level']] += 1
        if st.endswith('(U)'):
            lvl[r['level']] += 1
    print('==== "(U)" statewide-title marker by LEVEL digit (whole flat file)')
    for k in sorted(tot):
        print('   level %s: %7d rows, %6d end "(U)"  (%.1f%%)'
              % (k, tot[k], lvl.get(k, 0), 100.0 * lvl.get(k, 0) / tot[k]))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'u':
        u_marker()
    else:
        for p in ('ATF', 'ATT'):
            show_csv(p)
        distributions()
