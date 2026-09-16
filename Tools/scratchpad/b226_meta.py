"""Batch 226 metadata -- CNT, the four queued rows.

Contact hours: 60 for CNT3004C (C suffix), 45 for the three unsuffixed.

*** THE BATCH'S HEADLINE: A VENDOR-GOVERNED CURRICULUM ***
CNT3112 statewide is "Routing and Switching Essentials"; UWF calls it
"Switching, Routing and Wireless Essentials" and its description is the
statewide text PLUS wireless ("routers, switches AND WIRELESS DEVICES",
"virtual LANs, WIRELESS LANs, inter-VLAN routing").

Those are successive Cisco Networking Academy CCNA module names, and the
added wireless is exactly the documented v6->v7 restructure. Third piece of
convergent evidence: UWF titles the prerequisite CNT3004 "Introduction to
Networks" -- the CCNA module 1 name, and NOT the statewide title (Network
Concepts). Two consecutive courses named after two consecutive vendor
modules is not coincidence.

This is the batch-209 EXTERNALLY-GOVERNED CURRICULUM shape with a COMMERCIAL
VENDOR in place of a national body. Same three consequences: institutions
cannot diverge much on content, the statewide record is the LEAST current
source, and the guide should tell students to judge by what the Academy
issues. Written as a strong inference with the evidence shown, not as a
certainty -- no syllabus was seen.

*** SECOND: the C-suffix diagnostic, third outcome ***
FLPOLY carries BOTH CNT3004C and the bare CNT3004 -- the batch-184
signature of a course run in TWO SHAPES (lecture section and integrated
section). So the guide states the contact-hour difference and tells the
student to check which section they are in. Note this is the first time the
batch-219 table's THIRD row has fired; previous batches hit rows 2 and 4.

*** THIRD: another statewide PLACEHOLDER prerequisite ***
CNT3004's statewide prereq is "CSG X060 OR EQUIVALENT". X060 is a wildcard
in the level position, never replaced. Second instance of the batch-222
placeholder shape after COM4301's "COM 2XXX".

*** FOURTH: an institution hedging its own prerequisite, again ***
CNT4416 statewide requires CNT4403, CIS4385 AND CDA3101. UWF does not carry
CIS4385 (public carriers: Pensacola State, FSU), so UWF wrote
"(CIS 4385 OR CIS 4221) AND CNT 4403". Same pattern as TPA/PLA -- an
institution hedging its own prerequisite is a reliable sign it knows the
numbering does not line up.

*** FIFTH: a new blocked source ***
Florida Polytechnic (FLPOLY) is acalog and content-blocked -- root 200
(63 KB), 55 acalog references, content.php empty 202. EIGHTH institution in
the pattern.

*** AND: a private carrier's title in the inventory, second instance ***
CNT3112's queue row reads "ADVANCED NETWORK ADMINISTRATION" -- that is the
PRIVATE carrier's title, not the statewide or public one. Same shape as
COM2713 in batch 222.

CONTENT NOTE: CNT4416 is a defensive/educational cyber exercise course. The
guide leads with AUTHORISATION -- written scope, CFAA and Fla. Stat. ch. 815
-- and names the specific misunderstandings that get students prosecuted.

Prefix: 167 live ids, 120 single-carrier (72%), max 7 carriers. hs_credit,
transferable and dual enrolment all uniform.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
FLPOLY = 'Florida Polytechnic University'
FAMU = 'Florida A&M University'

# Shared block -- the confidentiality rule, which in networking and security
# is a control rather than an etiquette point.
CONFID = ('NEVER paste real configurations, topologies, captures or findings into a consumer AI tool '
          '- a configuration is a map of how to attack the network it runs.')

NEW = {

  'CNT3004C': {
    'title': 'Network Concepts',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'The STATEWIDE prerequisite reads "CSG X060 OR EQUIVALENT" - and CSG X060 is NOT a valid SCNS '
      'identifier. The X is a wildcard in the level position that was never replaced, so do not go '
      'looking for it. Take your own catalogue; in practice an introductory computing course is the '
      'sensible preparation, and COMFORT WITH BINARY AND HEX is the specific thing that makes '
      'subnetting tractable. '
      '*** THE C SUFFIX IS REAL: Florida Poly carries BOTH this and the bare CNT3004, which is the '
      'signature of a course run in two shapes - a lecture section and an integrated section with '
      'scheduled lab. The integrated form carries 60 hours against 45, and in networking that '
      'difference IS the lab. If you have a choice, take it. *** TAKE THIS EARLY - CNT3112, CNT4526 '
      'and the security sequence all gate on it. *** Ask in week one whether the course maps to '
      'Network+ or CCNA; if so, sit the exam while it is fresh.'),
    'offering_notes': {
      'summary': ('One public carrier of the C identifier (Florida Poly), which ALSO carries the bare '
                  'CNT3004 - the batch-184 two-shapes signature. The bare number is carried by UCF, '
                  'UWF and Florida Poly.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("No carrier publishes contact hours. 60 is Florida's convention for a 3-credit "
                     'integrated C course (Ron, 2026-09-15), well supported here because the same '
                     'institution offers an unsuffixed version alongside it.'),
      'offerings': [
        {'institution': 'FLPOLY', 'institution_name': FLPOLY,
         'title': 'Introduction to Computer Networks', 'credits': 3, 'contact_hours': None,
         'note': ('Sole public carrier of the C identifier, at 3 credits. ALSO carries the bare '
                  'CNT3004 as "Computer Networks". Florida Poly runs on acalog, which serves its '
                  'front pages but returns empty responses for course content, so its own '
                  'description and prerequisite could not be read. NOTE Florida Poly is the state\'s '
                  'newest public university and is exclusively STEM.')},
      ],
    },
  },

  'CNT3112': {
    'title': 'Routing and Switching Essentials',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF: CNT 3004. Statewide: CNT 3004 with a grade of C-MINUS OR BETTER. It resolves - UWF '
      'carries CNT3004 - and the statewide entry quotes UWF\'s local title for it, which identifies '
      'UWF as the contributor. '
      '*** THIS COURSE TRACKS A VENDOR CURRICULUM AND THE STATE RECORD IS A REVISION BEHIND. The '
      'statewide title is the earlier Cisco CCNA module name; UWF uses the current one and its '
      'description adds WIRELESS, which is exactly the documented restructure. UWF also titles '
      'CNT3004 "Introduction to Networks" - the module 1 name. So: judge the course by what the '
      'Academy issues in week one, not by any catalogue, and ask WHICH CCNA REVISION it follows - '
      'the answer also tells you which exam to sit. *** SUBNETTING MUST BE AUTOMATIC BEFORE YOU '
      'START. VLANs and inter-VLAN routing each need three correct subnet calculations before they '
      'work at all. *** Expect far more than 45 hours; troubleshooting is unpredictable by nature.'),
    'offering_notes': {
      'summary': ('One public carrier (UWF) at 3 credits. A private institution also carries the '
                  'number as "Advanced Network Administration" and is excluded under the '
                  'public-institution scope rule - but that private title has reached some Florida '
                  'course inventories, so the number may be seen labelled that way.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("UWF publishes no contact hours. 45 is Florida's convention for a 3-credit "
                     'course with no C or L suffix. Treat it as a floor - configuration labs are '
                     'attempted more than once and troubleshooting does not fit a timetable.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Switching, Routing and Wireless Essentials', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite CNT 3004. The statewide '
                  'description PLUS wireless: "architecture, components, and operations of routers, '
                  'switches AND WIRELESS DEVICES... design and configure virtual LANs, WIRELESS '
                  'LANs, inter-VLAN routing in both IPv4 and IPv6 networks, and routing protocols." '
                  'Department of Cybersecurity and Information Technology, College of Science and '
                  'Engineering - a dedicated cybersecurity department, which predicts a practitioner '
                  'and certification-oriented emphasis.')},
      ],
    },
  },

  'CNT4416': {
    'title': 'Cyber War Gaming',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF: (CIS 4385 OR CIS 4221) AND CNT 4403. The STATEWIDE version names CNT4403, CIS4385 AND '
      'CDA3101 at C-minus - but UWF does NOT carry CIS4385 (public carriers: Pensacola State, FSU), '
      'which is why UWF wrote an OR into its own prerequisite. Take your own catalogue. Do not '
      'attempt this without the network security gate; it is a capstone. '
      '*** AUTHORISATION IS THE WHOLE PROFESSIONAL BOUNDARY. These techniques are lawful inside a '
      'range you have WRITTEN permission to operate in and are felonies outside it, under the '
      'federal CFAA and Fla. Stat. ch. 815. "I was only looking", "I did no damage" and "I work in '
      'IT here" are NOT defences. Authorisation is WRITTEN, from someone who can grant it, with a '
      'defined scope. *** Keep your after-action reports - they are the portfolio. ' + CONFID),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits. FAMU matches the statewide red/blue war-gaming '
                  'description; UWF adds the legal AUTHORITIES framing and a substantial DEFENSIVE '
                  'AI component, explicitly purple-team. Scope breadth, not divergence - UWF\'s '
                  'version fully contains the statewide subject.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit unsuffixed course, and it substantially understates an exercise-based '
                     'course - a scenario runs until resolved, range access is often out of hours, '
                     'and the after-action report takes as long again.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Cyber Operations with Defensive AI', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite (CIS 4385 OR CIS 4221) AND '
                  'CNT 4403. "Cyber Operations provides students with an understanding of the '
                  'AUTHORITIES, roles and steps associated with cyber operations... Offensive Cyber '
                  'Operations (Red Team)... Defensive Cyber Operations (Blue Team)... with the '
                  'application of AI in strengthening defensive cybersecurity measures. Students '
                  'will learn how AI-driven tools and techniques can improve the detection, '
                  'analysis, and response to cyber threats. Welcome to Purple Team!" Department of '
                  'Cybersecurity and Information Technology.')},
        {'institution': 'FAMU', 'institution_name': FAMU,
         'title': 'Cyber War Gaming', 'credits': 3, 'contact_hours': None,
         'note': ('Matches the statewide title and description - red and blue teams recreating '
                  'real-world attack scenarios across network, security, visualization and software '
                  'specialities. FAMU runs on acalog, content-blocked, so its own description and '
                  'prerequisite could not be read.')},
      ],
    },
  },

  'CNT4526': {
    'title': 'Wireless and Mobile Networking',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF: CNT 3004 only. STATEWIDE: COP 4531 Algorithm Design and Analysis OR COP 3530 Data '
      'Structures and Algorithms, AND CNT 3004. '
      '*** THE PREREQUISITE PROVES THE DIVERGENCE INDEPENDENTLY, which is unusual. An ALGORITHMS gate '
      'signals a course that analyses protocol behaviour formally - the Florida Poly and statewide '
      'reading. A networking-only gate signals the UWF reading: wireless as an ENTERPRISE IT '
      'OPERATIONS subject - design, deployment, management, security, cost. Neither is misfiling. '
      'SYLLABUS TEST: throughput derivations = protocols version; site surveys and controllers = '
      'operations version. *** WIRELESS SECURITY TESTING NEEDS AUTHORISATION - capturing traffic '
      'from a network you do not own is unlawful regardless of intent. ' + CONFID),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits teaching materially different versions - a protocols '
                  'and architecture course at Florida Poly (matching the statewide record) and an '
                  'enterprise IT operations course at UWF. The prerequisites differ in a way that '
                  'confirms the split independently of the descriptions.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit unsuffixed course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Wireless and Mobile Communications', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite CNT 3004. "Introduces common '
                  'wireless technologies and wireless network architectures including common carrier '
                  'cellular networks... identify their roles in ENTERPRISE-CLASS INFORMATION '
                  'TECHNOLOGY OPERATIONS... common tools and applications... design, deployment and '
                  'management... strengths and weaknesses... in the context of their effect on '
                  'enterprise SECURITY, PERFORMANCE AND COST MANAGEMENT." Department of '
                  'Cybersecurity and Information Technology.')},
        {'institution': 'FLPOLY', 'institution_name': FLPOLY,
         'title': 'Wireless and Mobile Networking', 'credits': 3, 'contact_hours': None,
         'note': ('Matches the statewide title and description - "wireless and mobile network '
                  'architecture, protocols, and technologies... cellular networks, Wi-Fi, Bluetooth, '
                  'ZigBee". Florida Poly runs on acalog, content-blocked, so its own description '
                  'could not be read. As an exclusively STEM institution its technical reading is '
                  'consistent with the algorithms prerequisite in the statewide record.')},
      ],
    },
  },

}


def main():
    meta = json.load(open(META, encoding='utf-8')) if os.path.exists(META) else {}
    before = len(meta)
    overlap = sorted(set(meta) & set(NEW))
    if overlap:
        print('NOTE overwriting existing meta entries: %s' % ', '.join(overlap))
    meta.update(NEW)
    with open(META, 'w', encoding='utf-8') as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print('meta.json: %d -> %d entries' % (before, len(meta)))
    print('shared block: CONFID=%d chars' % len(CONFID))
    over = 0
    for k in sorted(NEW):
        p = NEW[k]['prerequisites'] or ''
        flag = ''
        if len(p) > 1000:
            flag = '  <-- OVER 1000'
            over += 1
        print('  %-9s %d cr  %3d hrs  prereq %4d chars%s'
              % (k, NEW[k]['credits'], NEW[k]['contact_hours'], len(p), flag))
    print('%d of %d over the limit' % (over, len(NEW)))


if __name__ == '__main__':
    main()
