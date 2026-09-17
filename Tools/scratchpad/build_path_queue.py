#!/usr/bin/env python
"""Build and VERIFY the Career Paths queue.

Ron, 2026-09-17: "Let's queue up the top 50 Career Paths using criteria of
'most common' very loosely. We will put extra emphasis on careers in
manufacturing and engineering as they are helping to sponsor the site."

⚠ "Most common" is loose BY INSTRUCTION, so the ranking is judgement. What is
NOT loose is the identifiers: every CIP code is checked against the NCES CIP
2020 file and every SOC code against the O*NET 2019 taxonomy, so a queue row
never carries a code that does not exist. The script fails loudly rather than
emitting an unverified row.

Writes Tools/career_paths/QUEUE.csv.
"""
import csv, io, json, os, re, sys
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
OUT = os.path.join(TOOLS, 'career_paths', 'QUEUE.csv')

# rank, slug, name, cip, soc, cluster
# ⚠ Clusters MFG and ENG carry the sponsor emphasis: 27 of the 50.
ROWS = [
    # ── Engineering ─────────────────────────────────────────────────────────
    (1,  'mechanical-engineer',        'Mechanical Engineer',            '14.19', '17-2141', 'ENG'),
    (2,  'electrical-engineer',        'Electrical Engineer',            '14.10', '17-2071', 'ENG'),
    (3,  'civil-engineer',             'Civil Engineer',                 '14.08', '17-2051', 'ENG'),
    (4,  'industrial-engineer',        'Industrial Engineer',            '14.35', '17-2112', 'ENG'),
    (5,  'aerospace-engineer',         'Aerospace Engineer',             '14.02', '17-2011', 'ENG'),
    (6,  'chemical-engineer',          'Chemical Engineer',              '14.07', '17-2041', 'ENG'),
    (7,  'biomedical-engineer',        'Biomedical Engineer',            '14.05', '17-2031', 'ENG'),
    (8,  'environmental-engineer',     'Environmental Engineer',         '14.14', '17-2081', 'ENG'),
    (9,  'computer-hardware-engineer', 'Computer Hardware Engineer',     '14.09', '17-2061', 'ENG'),
    (10, 'materials-engineer',         'Materials Engineer',             '14.18', '17-2131', 'ENG'),

    # ── Engineering technology, manufacturing and the trades ────────────────
    (11, 'electronics-engineering-technician', 'Electronics Engineering Technician', '15.03', '17-3023', 'MFG'),
    (12, 'mechanical-engineering-technician',  'Mechanical Engineering Technician',  '15.08', '17-3027', 'MFG'),
    (13, 'industrial-engineering-technician',  'Industrial Engineering Technician',  '15.06', '17-3026', 'MFG'),
    (14, 'civil-engineering-technician',       'Civil Engineering Technician',       '15.02', '17-3022', 'MFG'),
    (15, 'mechatronics-technician',   'Mechatronics and Automation Technician', '15.04', '17-3024', 'MFG'),
    (16, 'cad-drafter',               'CAD Drafter',                    '15.13', '17-3011', 'MFG'),
    (17, 'machinist',                 'Machinist',                      '48.05', '51-4041', 'MFG'),
    (18, 'cnc-operator',              'CNC Machine Operator',           '48.05', '51-9161', 'MFG'),
    (19, 'welder',                    'Welder',                         '48.05', '51-4121', 'MFG'),
    (20, 'industrial-maintenance-technician', 'Industrial Maintenance Technician', '47.03', '49-9041', 'MFG'),
    (21, 'quality-control-inspector', 'Quality Control Inspector',      '15.07', '51-9061', 'MFG'),
    (22, 'production-supervisor',     'Manufacturing Production Supervisor', '15.06', '51-1011', 'MFG'),
    (23, 'hvac-technician',           'HVAC Technician',                '47.02', '49-9021', 'MFG'),
    (24, 'electrician',               'Electrician',                    '46.03', '47-2111', 'MFG'),
    (25, 'aviation-maintenance-technician', 'Aviation Maintenance Technician', '47.06', '49-3011', 'MFG'),
    (26, 'automotive-service-technician', 'Automotive Service Technician', '47.06', '49-3023', 'MFG'),
    (27, 'logistics-analyst',         'Logistics and Supply Chain Analyst', '52.02', '13-1081', 'MFG'),

    # ── Health ──────────────────────────────────────────────────────────────
    (28, 'registered-nurse',          'Registered Nurse',               '51.38', '29-1141', 'HLT'),
    (29, 'licensed-practical-nurse',  'Licensed Practical Nurse',       '51.39', '29-2061', 'HLT'),
    (30, 'radiologic-technologist',   'Radiologic Technologist',        '51.09', '29-2034', 'HLT'),
    (31, 'respiratory-therapist',     'Respiratory Therapist',          '51.09', '29-1126', 'HLT'),
    (32, 'dental-hygienist',          'Dental Hygienist',               '51.06', '29-1292', 'HLT'),
    (33, 'medical-laboratory-scientist', 'Medical Laboratory Scientist', '51.10', '29-2011', 'HLT'),
    (34, 'physical-therapist-assistant', 'Physical Therapist Assistant', '51.08', '31-2021', 'HLT'),
    (35, 'paramedic',                 'Paramedic',                      '51.09', '29-2043', 'HLT'),
    (36, 'surgical-technologist',     'Surgical Technologist',          '51.09', '29-2055', 'HLT'),

    # ── Computing ───────────────────────────────────────────────────────────
    (37, 'software-developer',        'Software Developer',             '11.07', '15-1252', 'CMP'),
    (38, 'cybersecurity-analyst',     'Cybersecurity Analyst',          '11.10', '15-1212', 'CMP'),
    (39, 'network-administrator',     'Network Administrator',          '11.09', '15-1244', 'CMP'),
    (40, 'data-scientist',            'Data Scientist',                 '30.70', '15-2051', 'CMP'),

    # ── Business ────────────────────────────────────────────────────────────
    (41, 'accountant',                'Accountant / CPA',               '52.03', '13-2011', 'BUS'),
    (42, 'financial-analyst',         'Financial Analyst',              '52.08', '13-2051', 'BUS'),
    (43, 'human-resources-specialist','Human Resources Specialist',     '52.10', '13-1071', 'BUS'),
    (44, 'construction-manager',      'Construction Manager',           '52.20', '11-9021', 'BUS'),

    # ── Education, public service, legal ────────────────────────────────────
    (45, 'lawyer',                    'Lawyer',                         '22.01', '23-1011', 'LAW'),
    (46, 'paralegal',                 'Paralegal',                      '22.03', '23-2011', 'LAW'),
    (47, 'elementary-school-teacher', 'Elementary School Teacher',      '13.12', '25-2021', 'EDU'),
    (48, 'secondary-school-teacher',  'Secondary School Teacher',       '13.13', '25-2031', 'EDU'),
    (49, 'police-officer',            'Police Officer',                 '43.01', '33-3051', 'PUB'),
    (50, 'firefighter',               'Firefighter',                    '43.02', '33-2011', 'PUB'),
]


def main():
    cip, soc = {}, {}
    with io.open(os.path.join(HERE, 'cip2020.csv'), encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            c = (r['CIPCode'] or '').strip().strip('="').strip()
            cip[c] = (r['CIPTitle'] or '').strip().rstrip('.')
    soc = json.load(io.open(os.path.join(HERE, 'soc_titles.json'), encoding='utf-8'))
    seeded = {n['code'] for n in json.load(
        io.open(os.path.join(TOOLS, '..', 'PreseMakerRepo.Api', 'Data', 'Seed', 'cip.json'),
                encoding='utf-8'))['nodes']}

    def soc_title(code):
        return soc.get(code) or soc.get(code + '.00')

    bad, unseeded, slugs = [], [], set()
    for rank, slug, name, c, s, cluster in ROWS:
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', slug):
            bad.append('%s: bad slug' % slug)
        if slug in slugs:
            bad.append('%s: duplicate slug' % slug)
        slugs.add(slug)
        if c not in cip:
            bad.append('%s: CIP %s does not exist' % (slug, c))
        if not soc_title(s):
            bad.append('%s: SOC %s does not exist' % (slug, s))
        if c in cip and c not in seeded:
            unseeded.append((c, cip[c]))

    if bad:
        print('VERIFICATION FAILED -- nothing written:')
        for b in bad:
            print('   %s' % b)
        return 1

    print('%d paths, all CIP and SOC codes verified against NCES CIP 2020 and O*NET.' % len(ROWS))
    from collections import Counter
    for k, v in sorted(Counter(r[5] for r in ROWS).items(), key=lambda x: -x[1]):
        print('   %-4s %d' % (k, v))
    mfg_eng = sum(1 for r in ROWS if r[5] in ('ENG', 'MFG'))
    print('   -> manufacturing + engineering: %d of %d (%d%%)'
          % (mfg_eng, len(ROWS), round(100 * mfg_eng / len(ROWS))))

    uniq = sorted(set(unseeded))
    print('\n%d CIP group(s) needed by the queue are NOT in the seeded tree:' % len(uniq))
    for c, t in uniq:
        print('   %-7s %s' % (c, t))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['rank', 'slug', 'name', 'cip', 'cip_title', 'soc', 'soc_title',
                    'cluster', 'cip_seeded', 'status'])
        for rank, slug, name, c, s, cluster in ROWS:
            w.writerow([rank, slug, name, c, cip[c], s, soc_title(s), cluster,
                        'yes' if c in seeded else 'NO', ''])
    print('\nwrote %s' % os.path.relpath(OUT, TOOLS))
    return 0


if __name__ == '__main__':
    sys.exit(main())
