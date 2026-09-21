# -*- coding: utf-8 -*-
"""Assemble the SECOND 50-row career-path queue, validated against the seeded CIP
tree and the Florida IPEDS footprint. Run from Tools/.

    python scratchpad/build_queue2.py            # report + write rows to stdout
    python scratchpad/build_queue2.py --append   # append to career_paths/QUEUE.csv

Every row is checked two ways: is the CIP group in `Data/Seed/cip.json` (an
unseeded one needs a deploy before the path can be pushed), and how large is the
Florida public footprint under it.
"""
import json, csv, io, os, sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(HERE, '..', '..', 'PreseMakerRepo.Api', 'Data', 'Seed', 'cip.json')
IPEDS = os.path.join(HERE, 'ipeds_fl.json')
QUEUE = os.path.join(HERE, '..', 'career_paths', 'QUEUE.csv')

codes = {}


def walk(n):
    c = (n.get('code') or n.get('cipCode') or '').strip()
    if c:
        codes[c] = (n.get('title') or n.get('name') or '')
    for k in ('children', 'nodes', 'items'):
        for ch in (n.get(k) or []):
            walk(ch)


seed = json.load(io.open(SEED, encoding='utf-8'))
for n in (seed if isinstance(seed, list) else [seed]):
    walk(n)
ip = json.load(io.open(IPEDS, encoding='utf-8'))


def florida(prefix):
    s, t = set(), 0
    for cip, rs in ip.items():
        if cip.startswith(prefix):
            for r in rs:
                s.add(r['school'])
                t += r['completions']
    return len(s), t


# Labels for groups that are NOT in the seeded tree, so the row is still readable.
UNSEEDED_TITLES = {
    '51.20': 'Pharmacy, Pharmaceutical Sciences and Administration',
    '49.02': 'Ground Transportation',
    '12.05': 'Culinary Arts and Related Services',
    '12.04': 'Cosmetology and Related Personal Grooming Services',
    '46.05': 'Plumbing and Related Water Supply Services',
    '46.02': 'Carpentry',
}

ROWS = [
    # HEALTH -- the largest remaining Florida footprint by a wide margin
    (101, 'registered-dietitian', 'Registered Dietitian Nutritionist', '51.31', '29-1031', 'Dietitians and Nutritionists', 'HLT', 'DIRECT'),
    (102, 'speech-language-pathologist', 'Speech-Language Pathologist', '51.02', '29-1127', 'Speech-Language Pathologists', 'HLT', 'DIRECT'),
    (103, 'occupational-therapy-assistant', 'Occupational Therapy Assistant', '51.08', '31-2011', 'Occupational Therapy Assistants', 'HLT', 'DIRECT'),
    (104, 'diagnostic-medical-sonographer', 'Diagnostic Medical Sonographer', '51.09', '29-2032', 'Diagnostic Medical Sonographers', 'HLT', 'DIRECT'),
    (105, 'veterinary-technician', 'Veterinary Technician', '51.08', '29-2056', 'Veterinary Technologists and Technicians', 'HLT', 'DIRECT'),
    (106, 'medical-assistant', 'Medical Assistant', '51.08', '31-9092', 'Medical Assistants', 'HLT', 'DIRECT'),
    (107, 'phlebotomist', 'Phlebotomist', '51.10', '31-9097', 'Phlebotomists', 'HLT', 'DIRECT'),
    (108, 'health-information-technician', 'Health Information Technician', '51.07', '29-2072', 'Medical Records Specialists', 'HLT', 'DIRECT'),
    (109, 'healthcare-administrator', 'Healthcare Administrator', '51.07', '11-9111', 'Medical and Health Services Managers', 'HLT', 'CHOICE'),
    (110, 'public-health-professional', 'Public Health Professional', '51.22', '21-1091', 'Health Education Specialists', 'HLT', 'CHOICE'),
    (111, 'physician-assistant', 'Physician Assistant', '51.09', '29-1071', 'Physician Assistants', 'HLT', 'DIRECT'),
    (112, 'nurse-practitioner', 'Nurse Practitioner', '51.38', '29-1171', 'Nurse Practitioners', 'HLT', 'DIRECT'),
    (113, 'physician', 'Physician', '51.12', '29-1210', 'Physicians', 'HLT', 'CHOICE'),
    (114, 'athletic-trainer', 'Athletic Trainer', '51.09', '29-9091', 'Athletic Trainers', 'HLT', 'DIRECT'),
    (115, 'pharmacist', 'Pharmacist', '51.20', '29-1051', 'Pharmacists', 'HLT', 'DIRECT'),
    # SOCIAL SERVICES AND COUNSELLING
    (116, 'social-worker', 'Social Worker', '44.07', '21-1021', 'Child, Family, and School Social Workers', 'SOC', 'DIRECT'),
    (117, 'mental-health-counselor', 'Mental Health Counselor', '42.01', '21-1018', 'Substance Abuse, Behavioral Disorder, and Mental Health Counselors', 'SOC', 'CHOICE'),
    (118, 'school-counselor', 'School Counselor', '13.11', '21-1012', 'Educational, Guidance, and Career Counselors and Advisors', 'SOC', 'DIRECT'),
    # EDUCATION beyond the classroom
    (119, 'early-childhood-educator', 'Early Childhood Educator', '19.07', '25-2011', 'Preschool Teachers, Except Special Education', 'EDU', 'DIRECT'),
    (120, 'instructional-designer', 'Instructional Designer', '13.03', '25-9031', 'Instructional Coordinators', 'EDU', 'CHOICE'),
    # BUSINESS -- marketing, hospitality and the Florida service economy
    (121, 'marketing-manager', 'Marketing Manager', '52.14', '11-2021', 'Marketing Managers', 'BUS', 'CHOICE'),
    (122, 'sales-representative', 'Sales Representative', '52.14', '41-4012', 'Sales Representatives, Wholesale and Manufacturing', 'BUS', 'CHOICE'),
    (123, 'hospitality-manager', 'Hotel and Hospitality Manager', '52.09', '11-9081', 'Lodging Managers', 'BUS', 'DIRECT'),
    (124, 'restaurant-manager', 'Restaurant and Food Service Manager', '52.09', '11-9051', 'Food Service Managers', 'BUS', 'DIRECT'),
    (125, 'event-planner', 'Meeting and Event Planner', '52.09', '13-1121', 'Meeting, Convention, and Event Planners', 'BUS', 'CHOICE'),
    (126, 'mis-analyst', 'Management Information Systems Analyst', '52.12', '15-1211', 'Computer Systems Analysts', 'BUS', 'CHOICE'),
    (127, 'entrepreneur', 'Small Business Owner and Entrepreneur', '52.07', '11-1021', 'General and Operations Managers', 'BUS', 'CHOICE'),
    (128, 'real-estate-agent', 'Real Estate Agent and Broker', '52.15', '41-9022', 'Real Estate Sales Agents', 'BUS', 'CHOICE'),
    # CREATIVE, MEDIA AND DESIGN -- an entire cluster the first 50 never touched
    (129, 'graphic-designer', 'Graphic Designer', '50.04', '27-1024', 'Graphic Designers', 'ART', 'CHOICE'),
    (130, 'ux-designer', 'UX and Product Designer', '11.08', '15-1255', 'Web and Digital Interface Designers', 'ART', 'CHOICE'),
    (131, 'film-video-editor', 'Film and Video Editor', '50.06', '27-4032', 'Film and Video Editors and Camera Operators', 'ART', 'CHOICE'),
    (132, 'journalist', 'Journalist and Reporter', '09.04', '27-3023', 'News Analysts, Reporters, and Journalists', 'ART', 'CHOICE'),
    (133, 'public-relations-specialist', 'Public Relations Specialist', '09.09', '27-3031', 'Public Relations Specialists', 'ART', 'CHOICE'),
    (134, 'architect', 'Architect', '04.02', '17-1011', 'Architects, Except Landscape and Naval', 'ART', 'DIRECT'),
    (135, 'interior-designer', 'Interior Designer', '50.04', '27-1025', 'Interior Designers', 'ART', 'CHOICE'),
    # COMPUTING -- the roles the first four paths did not reach
    (136, 'database-administrator', 'Database Administrator', '11.08', '15-1242', 'Database Administrators and Architects', 'CMP', 'CHOICE'),
    (137, 'web-developer', 'Web Developer', '11.08', '15-1254', 'Web Developers', 'CMP', 'CHOICE'),
    # SCIENCE AND ENVIRONMENT
    (138, 'environmental-scientist', 'Environmental Scientist', '03.01', '19-2041', 'Environmental Scientists and Specialists', 'SCI', 'CHOICE'),
    (139, 'chemist', 'Chemist', '40.05', '19-2031', 'Chemists', 'SCI', 'DIRECT'),
    (140, 'biologist', 'Biologist', '26.01', '19-1029', 'Biological Scientists', 'SCI', 'CHOICE'),
    (141, 'marine-biologist', 'Marine Biologist', '26.13', '19-1023', 'Zoologists and Wildlife Biologists', 'SCI', 'CHOICE'),
    (142, 'fitness-professional', 'Fitness and Exercise Professional', '31.05', '39-9031', 'Exercise Trainers and Group Fitness Instructors', 'HLT', 'CHOICE'),
    (143, 'agricultural-manager', 'Agricultural Manager', '01.01', '11-9013', 'Farmers, Ranchers, and Other Agricultural Managers', 'AGR', 'DIRECT'),
    # TRANSPORT AND SERVICE -- the large Florida footprints the first 50 missed
    (144, 'commercial-pilot', 'Commercial Pilot', '49.01', '53-2012', 'Commercial Pilots', 'TRN', 'DIRECT'),
    (145, 'truck-driver', 'Commercial Truck Driver', '49.02', '53-3032', 'Heavy and Tractor-Trailer Truck Drivers', 'TRN', 'DIRECT'),
    (146, 'chef', 'Chef and Culinary Professional', '12.05', '35-1011', 'Chefs and Head Cooks', 'SRV', 'DIRECT'),
    (147, 'cosmetologist', 'Cosmetologist', '12.04', '39-5012', 'Hairdressers, Hairstylists, and Cosmetologists', 'SRV', 'DIRECT'),
    # REMAINING TRADES AND PUBLIC SERVICE
    (148, 'plumber', 'Plumber', '46.05', '47-2152', 'Plumbers, Pipefitters, and Steamfitters', 'MFG', 'DIRECT'),
    (149, 'carpenter', 'Carpenter', '46.02', '47-2031', 'Carpenters', 'MFG', 'DIRECT'),
    (150, 'urban-planner', 'Urban and Regional Planner', '04.03', '19-3051', 'Urban and Regional Planners', 'PUB', 'DIRECT'),
]


def main():
    out = io.StringIO()
    w = csv.writer(out, lineterminator='\n')
    unseeded, clusters, types = [], {}, {}
    print('%-4s %-32s %-7s %-6s %-9s %s' % ('rank', 'slug', 'cip', 'seeded', 'FL schools', 'FL completions'),
          file=sys.stderr)
    for rank, slug, name, cip, soc, soct, cluster, typ in ROWS:
        seeded = 'yes' if cip in codes else 'no'
        title = codes.get(cip) or UNSEEDED_TITLES.get(cip, '')
        nsch, ncomp = florida(cip)
        if seeded == 'no':
            unseeded.append((cip, slug, nsch, ncomp))
        clusters[cluster] = clusters.get(cluster, 0) + 1
        types[typ] = types.get(typ, 0) + 1
        w.writerow([rank, slug, name, cip, title, soc, soct, cluster, typ, seeded, ''])
        print('%-4d %-32s %-7s %-6s %10d %8d' % (rank, slug, cip, seeded, nsch, ncomp), file=sys.stderr)

    print('\n=== %d rows ===' % len(ROWS), file=sys.stderr)
    print('by cluster: %s' % ', '.join('%s %d' % kv for kv in sorted(clusters.items())), file=sys.stderr)
    print('by type:    %s' % ', '.join('%s %d' % kv for kv in sorted(types.items())), file=sys.stderr)
    if unseeded:
        print('\nWARNING  %d rows need a CIP SEED WIDENING (a deploy) before they can be pushed:'
              % len(unseeded), file=sys.stderr)
        for cip, slug, nsch, ncomp in unseeded:
            print('   %-7s %-26s FL: %2d schools, %5d completions' % (cip, slug, nsch, ncomp), file=sys.stderr)

    if '--append' in sys.argv:
        s = io.open(QUEUE, encoding='utf-8').read()
        if not s.endswith('\n'):
            s += '\n'
        io.open(QUEUE, 'w', encoding='utf-8', newline='').write(s + out.getvalue())
        print('\nappended %d rows to %s' % (len(ROWS), os.path.relpath(QUEUE)), file=sys.stderr)
    else:
        sys.stdout.write(out.getvalue())
    return 0


if __name__ == '__main__':
    sys.exit(main())
