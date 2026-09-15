"""Batch 212: map the ATF/ATT lower/upper alternate-level pairs, and check the
flat-file hs_credit/transferable offsets against the statewide CSV."""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scns
import json

HERE = os.path.dirname(os.path.abspath(__file__))
FLAT = os.path.join(HERE, 'crslist.txt')
INST = json.load(open(os.path.join(HERE, 'inst_map.json'), encoding='utf-8'))


def icode(instid):
    v = INST.get(str(int(instid))) if instid.strip().isdigit() else None
    return v.split(' - ')[0].strip() if v else instid


def listing():
    for pfx in ('ATF', 'ATT'):
        rows = list(scns.parse_flatfile(FLAT, prefix=pfx, active_only=True))
        by = collections.defaultdict(list)
        for r in rows:
            by[r['code']].append(r)
        print('#### %s -- every active id with carriers' % pfx)
        for code in sorted(by):
            rs = by[code]
            carr = sorted({icode(r['institution']) for r in rs})
            creds = sorted({(r['credit'] or '').strip() for r in rs})
            print('  %-9s %-52s %-22s cr=%s'
                  % (code, rs[0]['state_title'][:52], ','.join(carr), '/'.join(creds)))
        print()


def offsets():
    """Is the flat file's hs_credit/transferable pair really at 403-407?
    The CSV says HS=ELECTIVE, TRANS=GUARANTEED... but the flat file reads
    hs_credit='' and transferable='EL'. Dump the raw tail to see."""
    print('#### raw record tail for a few ATF rows (offset check)')
    n = 0
    with open(FLAT, 'rb') as fh:
        for line in fh:
            if line[10:13] != b'ATF':
                continue
            s = line.decode('latin1').rstrip('\r\n')
            print('  len=%d  [395:420]=%r' % (len(s), s[395:420]))
            n += 1
            if n >= 5:
                break


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'off':
        offsets()
    else:
        listing()
