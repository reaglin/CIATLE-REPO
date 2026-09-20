# -*- coding: utf-8 -*-
"""Derive the district-technical-college code list, with EVIDENCE. Run from Tools/.

⚠ The rule: a code goes on the list only when BOTH agree —
  (a) SCNS carries it and its name reads as a district technical college or career centre, AND
  (b) IPEDS lists an institution of that name in its FLORIDA PUBLIC file (institution_awards.json).

A name that matches (a) and not (b) is printed for review rather than included, because "Technical
Institute" is also what several private schools call themselves.
"""
import sys, os, io, json, re, collections
sys.path.insert(0, 'scratchpad')
import scns

AWARDS = os.path.join('..', 'PreseMakerRepo.Api', 'Data', 'Seed', 'institution_awards.json')

TECH_WORDS = ('TECHNICAL COLLEGE', 'TECHNICAL CENTER', 'TECHNICAL CENTRE', 'CAREER CENTER',
              'TECHNICAL INSTITUTE', 'EDUCATIONAL CENTER', 'SKILLS CENTER', 'CAREER INSTITUTE',
              'TECHNICAL EDUCATION')


def norm(n):
    n = n.upper()
    n = re.sub(r'[^A-Z0-9 ]', ' ', n)
    n = re.sub(r'\b(THE|OF|AT|AND|CAMPUS)\b', ' ', n)
    return re.sub(r'\s+', ' ', n).strip()


def main():
    ipeds = {norm(a['institutionName']) for a in
             json.load(io.open(AWARDS, encoding='utf-8'))['awards']}
    imap = scns.institution_map()

    matched, unmatched = {}, {}
    for key, raw in imap.items():
        code, _, name = raw.partition('-')
        code, name = code.strip(), name.strip()
        if '(INACTIVE' in name.upper():
            continue
        if scns.sector_of(code) in ('SUS', 'FCS'):
            continue
        if not any(w in name.upper() for w in TECH_WORDS):
            continue
        n = norm(name)
        hit = n in ipeds or any(n in i or i in n for i in ipeds)
        (matched if hit else unmatched)[code] = name

    print('=== ON THE LIST: SCNS name reads technical AND IPEDS lists it as Florida public (%d)' % len(matched))
    for c in sorted(matched):
        print('   %-8s %s' % (c, matched[c]))
    print()
    print('=== FOR REVIEW: technical-sounding name, NO IPEDS public match (%d)' % len(unmatched))
    for c in sorted(unmatched):
        print('   %-8s %s' % (c, unmatched[c]))

    out = os.path.join('scratchpad', 'tech_codes.json')
    json.dump({'matched': matched, 'unmatched': unmatched},
              io.open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\nwrote %s' % out)


if __name__ == '__main__':
    main()
