"""Batch 202 metadata. Offerings are built FROM THE FLAT FILE rather than typed, because
CHM1020 has 27 public carriers and hand-transcribing 27 rows invites error."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, TOOLS)
import scns
from list_courses import smart_title  # reuse the tested title-caser

imap = json.load(open(os.path.join(HERE, 'inst_map.json'), encoding='utf-8'))


def entry(num):
    v = imap.get(str(int(num)), '')
    if ' - ' in v:
        c, n = v.split(' - ', 1)
        return c.strip(), smart_title(n.strip())
    return v.strip(), smart_title(v.strip())


IDS = ('CHM1020', 'CHM1020C', 'CHM1020L', 'CHM1015', 'CHM1024', 'CHM1025')
fam = {}
for r in scns.parse_flatfile(os.path.join(HERE, 'crslist.txt'), prefix='CHM'):
    if r['code'] in IDS:
        fam.setdefault(r['code'], []).append(r)

# Per-institution notes. Anything not listed gets no note.
NOTES = {
    'CHM1020': {
        'CF': 'FOUR credits - the only carrier outside 3. Ask whether the extra credit '
              'reflects bundled laboratory work before treating the difference as arithmetic.',
        'SFSC': 'Records a GORDON RULE designation alongside the natural-science one. Gordon '
                'Rule needs a grade of C or higher; confirm against the institution list.',
        'TSC': 'Records a GORDON RULE designation alongside the natural-science one. Gordon '
               'Rule needs a grade of C or higher; confirm against the institution list.',
        'PHSC': 'The only carrier with NO designation recorded in the statewide record - '
                'neither Gordon Rule nor a general-education category. Check the institution '
                'list before using it for a requirement.',
        'SSCF': 'Also lists an HONORS section under the same number.',
        'FSU': 'Carries all THREE forms of the course - CHM1020 (3 cr), CHM1020L (1 cr) and '
               'CHM1020C (4 cr). The clean signature of one department serving two audiences.',
    },
    'CHM1020C': {
        'FSWSC': 'FOUR credits - 3 lecture plus 1 laboratory, bundled honestly.',
        'FSU': 'FOUR credits, and FSU carries all three forms of the course.',
        'SSCF': 'FOUR credits, and the title says so outright: "with Lab".',
        'HC': 'THREE credits, and records a GORDON RULE designation alongside the '
              'natural-science one.',
        'FAU': 'THREE credits - the same laboratory work for one credit less. FAU also lists '
               'an HONORS section under the same number.',
        'SCFMS': 'THREE credits - laboratory included in the contact time but not the credit.',
    },
    'CHM1020L': {
        'SFSC': 'Records a GORDON RULE designation on the laboratory number.',
        'FSU': 'FSU carries all three forms of the course.',
    },
    'CHM1015': {
        'FAMU': 'ONE credit, and a RECITATION - a problem session attached to a lecture, not '
                'a standalone course. Register for the paired lecture too. Not a substitute '
                'for the 3-credit preparatory course.',
        'EFSC': 'THREE credits, a standalone preparatory course - the reading that matches the '
                'statewide description, which says the course "prepares students to take '
                'CHM-025".',
    },
    'CHM1024': {
        'UNF': 'The only public carrier, at the exact statewide title. Statewide corequisite '
               'is CHM1025. WARNING - the statewide record classifies this course NOT '
               'AUTOMATICALLY TRANSFERABLE, which is rare; check how it counts toward degree '
               'progress, aid and excess hours at your own institution.',
    },
    'CHM1025': {
        'UNF': 'TWO credits - a compressed review. Covers less than a 3-credit version, and '
               'CHM2045 assumes the full preparation. Ask what is covered, not only what it '
               'is worth.',
        'UCF': 'TWO credits, same caution as UNF.',
        'FAMU': 'FOUR credits - most likely a bundled laboratory. Confirm whether lab work is '
                'included before assuming the extra credit is only arithmetic.',
        'FAU': 'Also lists an HONORS section under the same number.',
    },
}


def offerings(cid):
    rows = []
    for r in sorted(fam[cid], key=lambda x: int(x['institution'])):
        code, name = entry(r['institution'])
        if not scns.is_public(code):
            continue
        cr = r['credit'].strip()
        try:
            c = float(cr)
            c = int(c) if c == int(c) else c
        except ValueError:
            c = None            # 'VAR' or a range such as '1-3'
        rows.append({
            'institution': code,
            'institution_name': name,
            'title': smart_title(r['inst_title']),
            'credits': c,
            'contact_hours': None,
            'note': NOTES.get(cid, {}).get(code),
        })
    return rows


def notes(cid, summary, derived, derivation):
    return {
        'summary': summary,
        'hours_source': 'derived',
        'derived_contact_hours': derived,
        'derivation': derivation,
        'offerings': offerings(cid),
    }


meta = json.load(open(os.path.join(HERE, 'meta.json'), encoding='utf-8'))

meta['CHM1020'] = {
    'title': 'CHM1020 General Chemistry for Liberal Studies I - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'None statewide, and none at any carrier - this is an open-entry general-education '
        'course, available for dual enrolment. GOOD NEWS FIRST: the statewide title carries '
        '"(GE CORE)", so it is a Florida General Education Core course and satisfies the '
        'natural-science general-education area at EVERY Florida public institution, carrying '
        'that status in transfer - a stronger guarantee than ordinary course-by-course '
        'evaluation. WARNING - IT CARRIES NO LABORATORY. Many degree programmes require a '
        'science course WITH a lab; take CHM1020L alongside it, or CHM1020C (integrated), if '
        'your audit says "with laboratory". WARNING - if you are on a science or health '
        'pathway this is the WRONG number: those need CHM1032, CHM1025 or CHM2045, and this '
        'course substitutes for none of them and leads nowhere further. Gordon Rule status is '
        'institutional, not attached to the number - check your own list. Dual-enrolment note: '
        'the state records this as high-school ELECTIVE credit, not SCIENCE credit.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'CHM1020',
        'TWENTY-SEVEN Florida public institutions carry this number under EIGHTEEN distinct '
        'titles - no title used by more than four. But the SUBJECT does not diverge at all: '
        'every title names the same one-term non-majors general-education chemistry course. '
        'Maximum variation in the label, essentially none in the content. Credits: 26 at 3, '
        'College of Central Florida at 4. Designations differ by institution: 24 record a '
        'natural-science general-education designation, 2 add a Gordon Rule designation, and 1 '
        'records none.',
        45,
        'Derived, not published. No Florida institution publishes an hour figure for this '
        'number; 45 contact hours is the Florida convention for a 3-credit lecture course. The '
        'bare number carries no laboratory, so the figure describes lecture time only - '
        'CHM1020L adds roughly 30-45 and CHM1020C runs about 60-75 in total.'),
}

meta['CHM1020C'] = {
    'title': 'CHM1020C General Chemistry for Liberal Studies I with Laboratory - Curriculum Guide',
    'credits': 3,
    'contact_hours': 60,
    'prerequisites': (
        'None statewide, and available for dual enrolment. This is the INTEGRATED form of the '
        'general-education chemistry course - lecture and laboratory in one registration and one '
        'grade - and it is the number to choose when a degree audit says "science with '
        'laboratory", which the bare CHM1020 does not satisfy. It is a Florida General Education '
        'Core course ("GE CORE" in the statewide title), so it satisfies the natural-science '
        'area at every Florida public institution. WARNING - credits diverge systematically: '
        'Florida SouthWestern, Florida State and Seminole State at 4 (3 lecture + 1 lab, '
        'bundled); State College of Florida, Florida Atlantic and Hillsborough at 3 (same lab '
        'work, one credit less). Either way the LABORATORY requirement is satisfied, which is '
        'usually what matters. LAB DRESS CODE IS ENFORCED BY EXCLUSION: closed-toe shoes, no '
        'shorts, hair tied back, eye protection. Tell the instructor privately about a '
        'pregnancy, medical condition or chemical allergy.'
    ),
    # Replaces a live guide published 2026-05-04 (v1.0, 18 KB, no offering_notes), written
    # before the SCNS flat file existed. Materially rewritten, so the version increments.
    'version': '1.1',
    'offering_notes': notes(
        'CHM1020C',
        'Seven Florida public institutions carry the integrated form. Credits split 3/4 and the '
        'split is systematic rather than accidental: 4 credits bundles the laboratory credit, 3 '
        'credits includes the laboratory contact time without the credit. All seven record a '
        'natural-science general-education designation; one also records Gordon Rule. Florida '
        'Atlantic lists an Honors section under the same number.',
        60,
        'Derived, not published. 60 contact hours is the Florida convention for a 3-credit '
        'integrated lecture-and-laboratory (C) course, which is the modal credit value here; '
        'for the 4-credit versions expect roughly 75. The weekly shape either way is about '
        'three hours of lecture plus a two-to-three-hour laboratory session. No institution '
        'publishes an hour figure.'),
}

meta['CHM1020L'] = {
    'title': 'CHM1020L General Chemistry for Liberal Studies I Laboratory - Curriculum Guide',
    'credits': 1,
    'contact_hours': 45,
    'prerequisites': (
        'None statewide, but CHM1020 is a corequisite in practice - REGISTER FOR THE LECTURE '
        'TOO. A laboratory taken without its lecture is at best confusing and at most '
        'institutions not permitted, since the experiments assume the week\'s lecture material. '
        'The pair is CHM1020 + CHM1020L for 4 credits and two grades; CHM1020C is the '
        'integrated alternative. WARNING - ONE credit, and the hours are nothing like one '
        'credit\'s worth: a fixed two-to-three-hour weekly block that cannot be moved, plus '
        'pre-lab preparation, plus calculations and a written report. Realistically three to '
        'five hours a week. A missed session often CANNOT be made up - check the policy in week '
        'one - and lab sections fill before lecture sections. LAB DRESS CODE IS ENFORCED BY '
        'EXCLUSION: closed-toe shoes, no shorts, long hair tied back, approved eye protection '
        'worn the whole session. Tell the instructor privately in advance about a pregnancy, '
        'medical condition, chemical sensitivity or latex allergy.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'CHM1020L',
        'Seven Florida public institutions, ALL at 1 credit, and every title is simply that '
        'institution\'s own lecture title with "Lab" appended - no credit divergence and no '
        'subject divergence whatsoever. If your catalog\'s CHM1020L title does not match its '
        'CHM1020 title, ask which lecture it pairs with. General-education designation is '
        'uneven on the laboratory number, but that usually reflects the designation sitting on '
        'the lecture rather than the lab not counting.',
        45,
        'Derived, not published, and it should be read as an upper estimate of the SCHEDULED '
        'figure. The Florida convention for a 1-credit laboratory is roughly 30-45 hours, and a '
        'chemistry laboratory typically meets for one two-to-three-hour session a week over '
        'fifteen weeks. Real time spent is higher once pre-lab preparation and report writing '
        'are counted - three to five hours a week for one credit.'),
}

meta['CHM1015'] = {
    'title': 'CHM1015 General Chemistry Concepts - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'None statewide. Some institutions require or recommend a mathematics course or '
        'placement alongside it, and that is the requirement to take seriously - the arithmetic '
        'is the binding constraint. Available for dual enrolment. This is the BOTTOM rung: the '
        'statewide description says it is for students with no previous chemistry background '
        'and that it "prepares students to take CHM-025", which itself precedes CHM2045. '
        'WARNING - CHECK WHICH KIND OF COURSE YOURS IS. Only two public institutions carry the '
        'number: Eastern Florida State at 3 credits as a standalone preparatory course '
        '(matching the statewide description), and Florida A&M at 1 credit as a RECITATION - a '
        'problem session attached to a lecture, which must be taken WITH that lecture and is '
        'not a substitute for the standalone course. Read your catalog entry for a credit value '
        'and a named corequisite lecture; if a lecture is named, it is a recitation. Highest-'
        'value preparation before the term: dimensional analysis.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'CHM1015',
        'Two public carriers, one SUS and one FCS, and they use the number for different things: '
        'Eastern Florida State runs a 3-credit standalone preparatory course, Florida A&M a '
        '1-credit recitation attached to a lecture. A three-fold credit difference AND a '
        'course-type difference. With only two carriers there is no majority to appeal to; the '
        'tie-break used is that the 3-credit standalone course matches the statewide '
        'description, which describes a preparation rather than a support session.',
        45,
        'Derived, not published. 45 contact hours is the Florida convention for a 3-credit '
        'lecture course, matching the standalone reading this guide is written to. For the '
        '1-credit recitation the corresponding figure is about 15 hours, roughly an hour a week, '
        'ON TOP OF the paired lecture. No institution publishes an hour figure.'),
}

meta['CHM1024'] = {
    'title': 'CHM1024 Chemistry Study Skills - Curriculum Guide',
    'credits': 1,
    'contact_hours': 15,
    'prerequisites': (
        'No prerequisite; the statewide COREQUISITE is CHM1025 Introduction to Chemistry - this '
        'is a support course taken in the SAME TERM as the chemistry it supports, not before or '
        'after, because its value is that technique attaches to material being assessed that '
        'week. Available for dual enrolment. WARNING - the statewide record classifies this '
        'course NOT AUTOMATICALLY TRANSFERABLE, which is rare: almost every Florida course reads '
        '"guaranteed transfer to institution offering same course". Do not count the credit '
        'toward a requirement elsewhere, and ask an adviser how it counts at your own '
        'institution toward degree progress, aid and Florida excess hours. It is still very '
        'likely worth taking - one non-transferable credit that gets you through general '
        'chemistry beats a transferable one that does not. Only one public institution carries '
        'it; if yours does not, ask the chemistry department and the learning centre what they '
        'run instead.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'CHM1024',
        'ONE public carrier, at the exact statewide title, 1 credit - no divergence of any kind. '
        'With a single carrier there is no second catalog to check content against, so this guide '
        'describes what the statewide definition specifies (note taking, time management, '
        'chemistry problem solving, examination preparation, online resources) and what '
        'corequisite support courses of this kind standardly do. The number is rare because most '
        'institutions meet the same need through Supplemental Instruction, a general '
        'college-success course, embedded tutors or a local corequisite outside the CHM prefix.',
        15,
        'Derived, not published. 15 contact hours is the Florida convention for a 1-credit '
        'lecture-style course, roughly an hour a week over fifteen weeks - and it sits ON TOP OF '
        'the paired chemistry course\'s own hours. Budget two to three hours a week including '
        'the practice the session sets.'),
}

meta['CHM1025'] = {
    'title': 'CHM1025 Introduction to General Chemistry - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'None statewide, but institutions commonly require a mathematics prerequisite or '
        'placement - typically intermediate algebra or MAT1033/MAC1105 readiness - and some use '
        'a placement test or ALEKS score. Take it seriously: the mathematics is where students '
        'fail. Available for dual enrolment, and the state records it as high-school SCIENCE '
        'credit (unlike CHM1020, which is ELECTIVE). This is the SCIENCE-MAJOR preparatory '
        'course feeding CHM2045, not the non-majors general-education '
        'course - that is CHM1020, and the two are not interchangeable. WARNING - CREDITS '
        'DIVERGE FROM 2 TO 4: UNF and UCF at 2, most carriers at 3, FAMU at 4. A 2-credit review '
        'covers less than a 3-credit course and CHM2045 assumes the full preparation, so ask '
        'what is covered, not only what it is worth. HIGHEST-VALUE PREPARATION: spend several '
        'hours on dimensional analysis before the term starts - every quantitative chemistry '
        'problem is a unit-conversion problem in disguise. Second: learn nomenclature early, by '
        'repetition.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'CHM1025',
        'Eighteen Florida public institutions, and the credit values diverge from 2 to 4 - a '
        'factor of two, invisible from the title and the number. Likely explanations are '
        'ordinary (a 2-credit compressed review, a 3-credit lecture, a 4-credit version bundling '
        'a laboratory) but the content consequence is real: CHM2045 assumes the full '
        'preparation. The TITLES, by contrast, show no subject divergence - all name the same '
        'preparatory course. General-education designation is recorded by about half the '
        'carriers and not the other half, so do not assume it satisfies a general-education '
        'science requirement. Florida Atlantic lists an Honors section under the same number.',
        45,
        'Derived, not published. 45 contact hours is the Florida convention for a 3-credit '
        'lecture course, which is the modal value. For the 2-credit versions the corresponding '
        'figure is about 30 and for the 4-credit version about 60, the latter consistent with a '
        'bundled laboratory. No institution publishes an hour figure.'),
}

json.dump(meta, open(os.path.join(HERE, 'meta.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('meta.json now holds %d entries' % len(meta))
for cid in IDS:
    n = meta[cid]['offering_notes']
    print('  %-9s %d public offerings, prereq %d chars'
          % (cid, len(n['offerings']), len(meta[cid]['prerequisites'])))
