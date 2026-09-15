"""Batch 212 survey: the ATF/ATT flight-instructor family."""
import collections
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scns

HERE = os.path.dirname(os.path.abspath(__file__))
FLAT = os.path.join(HERE, 'crslist.txt')
INST = json.load(open(os.path.join(HERE, 'inst_map.json'), encoding='utf-8'))

TARGETS = ['ATF3502L', 'ATF3511L', 'ATF3531L', 'ATT1110', 'ATT3134']
FLAGS = ['gordon_rule', 'gordon_writing', 'ge_com', 'ge_hum', 'ge_math',
         'ge_nat_sci', 'ge_soc_sci']


def inst_of(instid):
    """Flat-file institution ids are ZERO-PADDED ('0000082'); inst_map keys are
    unpadded ('82'). And scns.is_public() wants the CODE ('UWF'), not the id --
    passing the id makes every institution read as private."""
    v = INST.get(str(int(instid))) if instid.strip().isdigit() else None
    if not v:
        return instid, '(unknown)'
    code = v.split(' - ')[0].strip()
    name = v.split(' - ', 1)[1].strip() if ' - ' in v else v
    return code, name


def survey(prefix):
    rows = list(scns.parse_flatfile(FLAT, prefix=prefix, active_only=True))
    by_code = collections.defaultdict(list)
    for r in rows:
        by_code[r['code']].append(r)
    return rows, by_code


def main():
    allrows = {}
    for pfx in ('ATF', 'ATT'):
        rows, by_code = survey(pfx)
        allrows[pfx] = (rows, by_code)
        live = sorted(by_code)
        singles = sum(1 for c in live if len({r['institution'] for r in by_code[c]}) == 1)
        mx = max((len({r['institution'] for r in by_code[c]}) for c in live), default=0)
        print('=== %s: %d live ids, %d single-carrier (%d%%), max carriers %d'
              % (pfx, len(live), singles, round(100 * singles / max(len(live), 1)), mx))

    print()
    for t in TARGETS:
        pfx = t[:3]
        rows, by_code = allrows[pfx]
        base = t.rstrip('L') if t.endswith('L') else t
        # match on the 7-char code family (prefix+level+century+decade+unit [+lab])
        hits = {c: v for c, v in by_code.items() if c.replace(' ', '').startswith(t[:7])}
        print('---------------------------------------------------------------')
        print('TARGET %s   (flat-file codes matching %s*)' % (t, t[:7]))
        if not hits:
            print('   !! NO ACTIVE CARRIER IN THE FLAT FILE')
        for code, rs in sorted(hits.items()):
            pub = [r for r in rs if scns.is_public(inst_of(r['institution'])[0])]
            print('  code=%-9s carriers=%d (public %d)' % (code, len(rs), len(pub)))
            for r in sorted(rs, key=lambda x: (x['institution'], x['inst_title'])):
                icode, iname = inst_of(r['institution'])
                flags = [k for k in FLAGS if r.get(k) == 'Y']
                print('     %-6s %-7s %-44s cr=%-6s clk=%-5s %s%s'
                      % (icode,
                         scns.sector_of(icode) if scns.is_public(icode) else 'private',
                         r['inst_title'][:44], r['credit'], r['clock_hours'],
                         ','.join(flags), '  hs=' + r['hs_credit'] + ' tr=' + r['transferable']))
            st = rs[0]['state_title']
            print('     STATE TITLE: %s' % st)


if __name__ == '__main__':
    main()
