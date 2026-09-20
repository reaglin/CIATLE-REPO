# -*- coding: utf-8 -*-
"""Who carries which course id, from the SCNS flat file. Run from Tools/.

    python scratchpad/carriers.py ENV4001 CWR4202 ...
    python scratchpad/carriers.py --prefix ENV --like water
"""
import sys, os, collections
sys.path.insert(0, 'scratchpad')
import scns

FLAT = os.path.join('scratchpad', 'crslist.txt')


def cid_of(r):
    return (r['prefix'] + r['level'] + r['century'] + r['decade'] + r['unit'] + (r['lab'] or '')).strip().upper()


def code_of(name):
    # "CWR - CIVIL WATER RESOURCES" style: the short code is before the dash
    return name.split('-')[0].strip()


def main():
    args = sys.argv[1:]
    imap = {k: code_of(v) for k, v in scns.institution_map().items()}
    # ⚠ is_public takes the SHORT CODE (UNF), not the numeric key.
    public = {k for k, c in imap.items() if scns.is_public(c)}

    pfx = like = None
    want = set()
    if args and args[0] == '--prefix':
        pfx = args[1].upper()
        if len(args) > 3 and args[2] == '--like':
            like = args[3].lower()
    else:
        want = {a.upper() for a in args}

    per = collections.defaultdict(set)
    titles = {}
    for r in scns.parse_flatfile(FLAT):
        if r['status'] != 'A':
            continue
        cid = cid_of(r)
        if want and cid not in want:
            continue
        if pfx and not cid.startswith(pfx):
            continue
        t = (r.get('inst_title') or '').strip()
        if like and like not in t.lower():
            continue
        inst = r['institution'].lstrip('0')
        if inst in public:
            per[cid].add(imap[inst])
            titles.setdefault(cid, t)

    keys = sorted(per, key=lambda c: (-len(per[c]), c)) if (pfx or not want) else args
    for cid in keys:
        c = cid.upper()
        print('%-10s %-2d %-40s %s' % (c, len(per.get(c, ())), titles.get(c, '')[:40],
                                       ' '.join(sorted(per.get(c, ())))))


if __name__ == '__main__':
    main()
