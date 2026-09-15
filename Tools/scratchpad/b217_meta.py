"""Batch 217 metadata -- GIS, completing the prefix queue (6 courses).

Contact hours:
  * 3-credit lecture -> 45 (GIS4006)
  * 1-credit lab -> 30 (GIS4035L, GIS4043L)
  * 3-credit integrated C -> 60 (GIS4048C, GIS4102C)
  * GIS4301C is 4 credits and UCF PUBLISHES 2 weekly lab hours -> 30 lab + ~45
    lecture = 75. UCF is the only Florida source reporting lab hours as a
    structured field, so this figure is built rather than assumed.

Prerequisite budget (batch-215 lesson): shared blocks counted FIRST. Two here,
both deliberately short.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
FSU = 'Florida State University'
FAU = 'Florida Atlantic University'
UF = 'University of Florida'
UCF = 'University of Central Florida'

# Uniform across all 204 GIS flat-file rows -> boilerplate, said once and briefly.
DE = ('The dual-enrolment/elective marking is uniform across the whole GIS prefix, so it says '
      'nothing about this course.')

# The intro-GIS number is not the same everywhere: a real transfer trap.
NUM = ('NUMBER DIVERGENCE: introductory GIS is GIS4043 + GIS4043L (4000-level lecture + lab) at UWF '
       'and FSU, but GIS 3043C (3000-level integrated) at UF - same subject, different number, '
       'division and packaging, so show coverage rather than matching on the number. ')

NEW = {

  'GIS4006': {
    'title': 'Computer Cartography',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF requires GIS 4043/L and pairs this course with a corequisite laboratory, GIS 4006L - a '
      'separate registration and grade carrying the hands-on map production, so UWF students '
      'register for both. ' + NUM + 'UWF also dual-lists this course with GIS 5007, where graduate '
      'students are assigned additional work: the pace sits above a typical undergraduate course, '
      'and taking this version may BLOCK taking the graduate one for credit later - ask if you are '
      'considering a UWF master\'s. ' + DE),
    'offering_notes': {
      'summary': ('Both public carriers use the statewide title unchanged at 3 credits. UWF pairs a '
                  'separate corequisite lab (GIS4006L) that FSU does not publish, and names '
                  'portfolio creation as a course outcome - worth knowing, since GIS hiring is '
                  'portfolio-driven.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     "3-credit lecture course; UWF's hands-on hours sit in the corequisite "
                     'GIS4006L.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Computer Cartography', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. Prerequisite GIS 4043/L; corequisite GIS '
                  '4006L. "Focuses on the fundamentals of cartography, spatial statistics, thematic '
                  'mapping techniques, and web-based mapping... students will have created a '
                  'professional GIS portfolio for current/potential employers." Offered concurrently '
                  'with GIS 5007. College of Science and Engineering, Department of Earth and '
                  'Environmental Sciences.')},
        {'institution': 'FSU', 'institution_name': FSU,
         'title': 'Computer Cartography', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits, statewide title unchanged. Confirmed from the FSU geography bulletin\'s '
                  'degree requirements, which lists it at 3 credits; a full course description was '
                  'not retrieved.')},
      ],
    },
  },

  'GIS4035L': {
    'title': 'Photo Interpretation and Remote Sensing Laboratory',
    'credits': 1, 'contact_hours': 30, 'version': '1.0',
    'prerequisites': (
      'Paired with the 3-credit lecture GIS 4035 - 4 credits and two grades for the subject. THREE '
      'UWF REQUIREMENTS THAT CATCH STUDENTS: permission is required (lab seats are limited by '
      'workstation count, so request early); equipment fees will be assessed; and "basic competency '
      'with ArcGIS Pro software is required" with prior Introduction to GIS coursework EXPECTED - '
      'this course does NOT teach you to operate GIS software. Uses Erdas Imagine as well as ArcGIS '
      'Pro, which you may not be able to run at home. UWF dual-lists it with GIS 5027L, so taking '
      'this version may block the graduate one later. ' + DE),
    'offering_notes': {
      'summary': ('Both public carriers award 1 credit paired with a 3-credit lecture. Titles differ '
                  'in emphasis - UWF names photo interpretation explicitly, FSU uses the broader '
                  '"Introduction to Remote Sensing". NOTE Florida gives this LAB the title of its '
                  'LECTURE ("Remote Sensing of the Environment") with no separate description, so '
                  'the state record cannot distinguish the halves.'),
      'hours_source': 'derived',
      'derived_contact_hours': 30,
      'derivation': ('Neither carrier publishes contact hours. A 1-credit laboratory in Florida '
                     'conventionally carries 2-3 contact hours a week, so roughly 30-45 hours a '
                     'term; 30 is the lower end.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Photo Interpretation and Remote Sensing Lab', 'credits': 1, 'contact_hours': None,
         'note': ('1 sh, may not be repeated for credit. Prerequisite GIS 4035 (concurrency marked). '
                  '"The lab will focus on techniques for the practical use of digital aerial '
                  'photography and satellite imagery using both Erdas Imagine and ArcGIS Pro." '
                  'Equipment fees assessed; permission required; basic ArcGIS Pro competency and '
                  'prior Introduction to GIS coursework expected. Offered concurrently with GIS '
                  '5027L. Department of Earth and Environmental Sciences.')},
        {'institution': 'FSU', 'institution_name': FSU,
         'title': 'Introduction to Remote Sensing Lab', 'credits': 1, 'contact_hours': None,
         'note': ('1 credit, paired with GIS 4035 Introduction to Remote Sensing (3 cr). Confirmed '
                  'from the FSU geography bulletin; a full description was not retrieved.')},
      ],
    },
  },

  'GIS4043L': {
    'title': 'Geographic Information Systems Laboratory',
    'credits': 1, 'contact_hours': 30, 'version': '1.0',
    'prerequisites': (
      'COREQUISITE GIS 4043, the 3-credit lecture - register for both, 4 credits and two grades. '
      'UWF requires PERMISSION and assesses EQUIPMENT FEES; request permission early, since GIS lab '
      'seats are limited by workstation count and a late request can cost you the term in a '
      'sequenced programme. EXPECT IT TO TAKE MORE TIME THAN ONE CREDIT SUGGESTS - 2-3 scheduled '
      'hours a week plus substantial practice, because GIS work is slow while you are learning it. '
      'This lab is where the employable skill lives; employers ask what software you can operate and '
      'what you have built. UWF dual-lists it with GIS 5050L. ' + DE),
    'offering_notes': {
      'summary': ('Both public carriers award 1 credit paired with a 3-credit lecture (GIS4043). '
                  'NOTE Florida gives this LAB the title of its LECTURE ("Principles of Geographic '
                  'Information Systems") with no separate description - the third instance of that '
                  'pattern in recent batches.'),
      'hours_source': 'derived',
      'derived_contact_hours': 30,
      'derivation': ('Neither carrier publishes contact hours. A 1-credit laboratory conventionally '
                     'carries 2-3 contact hours a week, so roughly 30-45 hours a term.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'GIS Laboratory', 'credits': 1, 'contact_hours': None,
         'note': ('1 sh, may not be repeated for credit. Corequisite GIS 4043. "This hands-on lab '
                  'course is designed to complement the theoretical foundations covered in the GIS '
                  'lecture course... students will have gained the knowledge and skills necessary to '
                  'apply GIS effectively in various professional and academic settings as well as '
                  'developed a strong foundation for GIS project development, execution, and '
                  'presentation." Equipment fees assessed; permission required. Offered concurrently '
                  'with GIS 5050L. Department of Earth and Environmental Sciences.')},
        {'institution': 'FSU', 'institution_name': FSU,
         'title': 'GIS Lab', 'credits': 1, 'contact_hours': None,
         'note': ('1 credit, paired with GIS 4043 Geographic Information Systems (3 cr). Confirmed '
                  'from the FSU geography bulletin; a full description was not retrieved.')},
      ],
    },
  },

  'GIS4048C': {
    'title': 'Applications in GIS',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      "Florida's record names GIS 4043. " + NUM + 'SINGLE-INSTITUTION NUMBER: only FAU carries it, '
      'and FAU does not expose a public course catalogue at its catalogue host, so this guide is '
      'written from the statewide record - which is unusually informative here - and your syllabus '
      'governs. EXPECT THE HARD PART TO BE PROBLEM FRAMING, not the analysis: you are given a '
      'situation and must convert it into a spatial question, decide what would count as an answer, '
      'and judge whether data exists to support it. A C course takes about four hours a week of '
      'class and lab plus project time. ' + DE),
    'offering_notes': {
      'summary': ('Single public carrier, and its catalogue is not retrievable. The statewide '
                  'description is unusually substantive for this number - it names a "generic '
                  'process for applying GIS techniques in problem solving" and case studies in '
                  'environmental and social domains - so the guide has more to work from than most '
                  'single-carrier cases.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("FAU does not publish contact hours. 60 is Florida's convention for a 3-credit "
                     'integrated lecture+lab (C) course, which is what the identifier represents.'),
      'offerings': [
        {'institution': 'FAU', 'institution_name': FAU,
         'title': 'Applications in GIS', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits, statewide title unchanged. The only Florida public carrier. FAU does '
                  'not expose a public course catalogue at catalog.fau.edu (the host is registered '
                  'with a catalogue platform but has no catalogue attached), so its description '
                  'could not be read.')},
      ],
    },
  },

  'GIS4102C': {
    'title': 'GIS Programming',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'UF requires GIS 3043C or equivalent; the statewide record names GIS 4043. ' + NUM +
      'EXPECT THIS TO BE THE HARDEST COURSE IN A GIS CURRICULUM if you have not programmed before - '
      'a map that is slightly wrong still looks like a map, but a script with a misplaced character '
      'does nothing at all, and that is discouraging in a way students do not anticipate. Write code '
      'weekly rather than in blocks, and start from a working example. NOTE UF formally tags this '
      'course with an ARTIFICIAL INTELLIGENCE attribute, which may count toward an AI certificate or '
      'transcript notation - find out what it counts toward. ' + DE),
    'offering_notes': {
      'summary': ('Both public carriers award 3 credits; the titles differ only in word order. UF '
                  'formally tags the course with an Artificial Intelligence attribute and requires '
                  'GIS 3043C - a 3000-level integrated intro GIS course, where UWF and FSU use the '
                  '4000-level GIS4043 + lab pair.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("Neither carrier publishes contact hours. 60 is Florida's convention for a "
                     '3-credit integrated lecture+lab (C) course.'),
      'offerings': [
        {'institution': 'UF', 'institution_name': UF,
         'title': 'GIS Programming', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits. "Introduces basic programming concepts; instruction in popular '
                  'programming languages for geospatial processing, applications, and modeling in '
                  'ArcGIS environment." Prerequisite GIS 3043C or equivalent. ⚠ Carries a formal '
                  'ARTIFICIAL INTELLIGENCE course attribute in UF\'s catalogue.')},
        {'institution': 'FAU', 'institution_name': FAU,
         'title': 'Programming in GIS', 'credits': 3, 'contact_hours': None,
         'note': ('3 credits, matching the statewide title. FAU does not expose a public course '
                  'catalogue, so its description could not be read.')},
      ],
    },
  },

  'GIS4301C': {
    'title': 'Advanced GIS Applications in Environmental Studies',
    'credits': 4, 'contact_hours': 75, 'version': '1.0',
    'prerequisites': (
      "Florida's record names GIS 4043. " + NUM + 'SINGLE-INSTITUTION NUMBER: UCF is the only '
      'Florida public carrier, so your syllabus governs. NOTE THE CREDIT VALUE - FOUR, not the 3 '
      'standard across the rest of the GIS sequence, so a receiving programme expecting 3 must '
      'decide what to do with the fourth. Needs several LICENSED ArcGIS extensions (Spatial '
      'Analyst, 3D Analyst, Network Analyst, Geostatistical Analyst) - confirm what your institution '
      'provides. Geostatistics will be the unfamiliar part and is the most valuable: interpolation '
      'ESTIMATES values you do not have, which is inference rather than mapping. ' + DE),
    'offering_notes': {
      'summary': ('Single public carrier, at FOUR credits rather than the 3 standard elsewhere in '
                  'the prefix. UCF publishes 2 weekly laboratory hours - the only Florida source '
                  'reporting lab hours as a structured field - and its description names the '
                  'specific techniques: raster overlay suitability modelling, least-cost paths, 3D '
                  'DEMs, network routing and geostatistical analysis.'),
      'hours_source': 'mixed',
      'derived_contact_hours': 75,
      'derivation': ('UCF publishes 2 LABORATORY hours per week (30 across a 15-week term) as a '
                     'structured field; the remaining credit weight implies about 3 lecture hours a '
                     'week (45), giving roughly 75 in total. Part published, part derived - better '
                     'grounded than most figures in this prefix.'),
      'offerings': [
        {'institution': 'UCF', 'institution_name': UCF,
         'title': 'Advanced GIS Applications in Environmental Studies', 'credits': 4,
         'contact_hours': None,
         'note': ('4 credits - one more than the rest of the GIS sequence. Publishes 2 weekly '
                  'laboratory hours. "GIS analysis techniques used in environmental science, '
                  'including raster overlay site suitability modeling, least-cost optimum paths, 3D '
                  'digital elevation models, network routing & geostatistical analysis." The only '
                  'Florida public carrier.')},
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
    print('shared blocks: DE=%d NUM=%d (sum %d)' % (len(DE), len(NUM), len(DE) + len(NUM)))
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
