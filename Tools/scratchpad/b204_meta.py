"""Batch 204 metadata. Offerings built from the flat file (batch 202 pattern)."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, TOOLS)
import scns
from list_courses import smart_title

imap = json.load(open(os.path.join(HERE, 'inst_map.json'), encoding='utf-8'))


def entry(num):
    v = imap.get(str(int(num)), '')
    if ' - ' in v:
        c, n = v.split(' - ', 1)
        return c.strip(), smart_title(n.strip())
    return v.strip(), smart_title(v.strip())


IDS = ('PET4765', 'PHC4320', 'PHI4300', 'PHY3107', 'PHY4513', 'PLA3240')
fam = {}
for pfx in ('PET', 'PHC', 'PHI', 'PHY', 'PLA'):
    for r in scns.parse_flatfile(os.path.join(HERE, 'crslist.txt'), prefix=pfx):
        if r['code'] in IDS:
            fam.setdefault(r['code'], []).append(r)

NOTES = {
    'PET4765': {
        'USF': 'Titled SCIENTIFIC PRINCIPLES OF ATHLETIC COACHING - the sport-science half: '
               'physiology, motor learning, training design and periodisation. The better '
               'preparation if strength and conditioning (CSCS) is the target.',
        'UWF': 'Titled THEORY AND PRACTICE OF COACHING - closest to the statewide balance, with '
               'applied practice and season planning.',
        'FSU': 'Titled PRINCIPLES AND PROBLEMS OF COACHING - the professional problems of the '
               'job: administration, parents, officials, facilities, ethics and legal duties.',
    },
    'PHC4320': {
        'UWF': 'Titled ENVIRONMENTAL AND OCCUPATIONAL HEALTH - adds OCCUPATIONAL health, a '
               'distinct professional field with its own regulator (OSHA), discipline '
               '(industrial hygiene), exposure limits and credentials (CIH, CSP). An addition '
               'rather than a substitution, so the environmental half is necessarily compressed. '
               'The better preparation for a safety or industrial-hygiene career.',
        'FSU': 'Matches the statewide title exactly - the neutral reading, with more room for the '
               'environmental material.',
        'UF': 'Titled ENVIRONMENTAL CONCEPTS IN PUBLIC HEALTH - the public-health framing '
              'foregrounded; expect epidemiological and policy language throughout.',
    },
    'PHI4300': {
        'USF': 'Titled THEORY OF KNOWLEDGE. Carries the GORDON RULE WRITING designation - so a C '
               'or higher is required for it to count.',
        'UWF': 'Titled SKEPTICISM, KNOWLEDGE, AND TRUTH - names the three-part structure of a '
               'standard epistemology syllabus, and leading with scepticism suggests it is the '
               'organising problem rather than one topic. Carries the GORDON RULE WRITING '
               'designation; a C or higher is required.',
        'UCF': 'Titled THEORIES OF KNOWLEDGE. NO Gordon Rule designation recorded - so a student '
               'taking this course here to clear a writing requirement has NOT cleared it. The '
               'singular/plural title difference from USF is not a signal.',
    },
    'PHY3107': {
        'FIU': 'Titled ADVANCED MODERN PHYSICS - reads the number as the advanced continuation of '
               'modern physics, matching the statewide "Modern Physics II" sense.',
        'UWF': 'Titled CALCULUS-BASED PHYSICS IV - an ORDINAL-BASE divergence. It counts position '
               'in the whole introductory sequence (Physics I and II being mechanics and '
               'electromagnetism, III the first modern physics course, IV this one) where the '
               'statewide title counts within modern physics. Same course. A student searching a '
               'UWF catalog for "Modern Physics II" will not find it, and the title conveys the '
               'position but not the content - keep the syllabus and topic list.',
    },
    'PHY4513': {
        'UWF': 'Titled THERMAL AND STATISTICAL PHYSICS - the modern framing, in which statistical '
               'mechanics is the foundation and thermodynamics is derived from it. Identical to '
               'FSU\'s title.',
        'FSU': 'Titled THERMAL AND STATISTICAL PHYSICS - identical to UWF, which is the strongest '
               'available evidence for the modern reading.',
        'FLPOLY': 'Titled INTRODUCTION TO THERMAL & STATISTICAL MECHANICS - same subject with '
                  '"mechanics" and an explicit "introduction". Consistent with Florida Poly\'s '
                  'engineering mission, so expect a more applied treatment and possibly less '
                  'quantum statistics. Florida Poly is a small newer SUS institution; a student '
                  'intending physics graduate study should ask which core courses are taught and '
                  'how often.',
    },
    'PLA3240': {
        'SPC': 'The Florida College System carrier - the FCS-to-SUS transfer case this numbering '
               'system exists to serve.',
        'FGCU': 'Identical title and credits.',
        'UWF': 'Identical title and credits.',
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
            c = None
        rows.append({'institution': code, 'institution_name': name,
                     'title': smart_title(r['inst_title']), 'credits': c,
                     'contact_hours': None, 'note': NOTES.get(cid, {}).get(code)})
    return rows


def notes(cid, summary, derived, derivation):
    return {'summary': summary, 'hours_source': 'derived',
            'derived_contact_hours': derived, 'derivation': derivation,
            'offerings': offerings(cid)}


D3 = ('Derived, not published. No Florida institution publishes an hour figure for this '
      'number; 45 contact hours is the Florida convention for a 3-credit lecture course.')

meta = json.load(open(os.path.join(HERE, 'meta.json'), encoding='utf-8'))

meta['PET4765'] = {
    'title': 'PET4765 Theory and Methods of Coaching Sports - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'No statewide prerequisite, but the number is 4000-level and institutions expect '
        'upper-division standing in physical education, exercise science, sport management or '
        'athletic coaching; some sections are majors-only, and anatomy, physiology and motor '
        'learning are commonly expected. WARNING - the statewide record classifies this course '
        'NOT AUTOMATICALLY TRANSFERABLE, rare and notable here because it is a substantive theory '
        'course rather than a support course. Ask the '
        'receiving department in writing BEFORE taking it if you transfer, and keep the syllabus. '
        'WARNING - THIS COURSE DOES NOT QUALIFY YOU TO COACH IN FLORIDA. Interscholastic coaching '
        'requires FHSAA and district certifications: CPR/AED and first aid, concussion training '
        '(CDC HEADS UP or NFHS), heat-illness and cardiac-arrest training, usually NFHS '
        'Fundamentals of Coaching plus a rules clinic, Level 2 screening and abuse-prevention '
        'training. Several are free - do them while you are a student, and start screening early.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'PET4765',
        'Three State University System institutions at 3 credits - no credit divergence and no '
        'subject divergence, but three titles pointing at three different emphases: USF the sport '
        'science, UWF theory plus applied practice, FSU the professional problems of the job. That '
        'variation is probably why the statewide record classifies the number NOT AUTOMATICALLY '
        'TRANSFERABLE - a statewide guarantee would assert an equivalence that does not hold. The '
        'statewide description is also notably dated in vocabulary and omits athlete safety, '
        'abuse prevention, mental health and long-term athlete development, all of which a '
        'current course covers.',
        45, D3 + ' Where a practicum, observation or coaching placement is attached, budget the '
        'placement hours separately - and if it involves minors, Level 2 background screening must '
        'clear first and takes weeks.'),
}

meta['PHC4320'] = {
    'title': 'PHC4320 Environmental Health Science - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'Statewide prerequisite: NONE, and the statewide description says explicitly that the '
        'course "is open to all major programs" - unusual and worth acting on. It is a deliberate '
        'design: upper-division level for its audience, open in entry. Available for dual '
        'enrolment (elective high-school credit). Good choices from outside public health include '
        'environmental science, biology and chemistry students (it converts a science degree into '
        'something employable in a county or regulatory role), nursing and health professions '
        '(exposure history is part of a clinical history), civil and environmental engineering, '
        'planning and public administration, and education. Check your own catalog even so - an '
        'institution may restrict a section or add a prerequisite, and a restriction is invisible '
        'until registration fails. WARNING - UWF adds OCCUPATIONAL health to the course, which is '
        'the better preparation for a safety or industrial-hygiene career and necessarily '
        'compresses the environmental half.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'PHC4320',
        'Three State University System institutions at 3 credits - no credit divergence and no '
        'subject divergence. The divergence is one of SCOPE and runs one way: UWF adds '
        'OCCUPATIONAL health, a distinct professional field with its own regulator (OSHA), '
        'discipline (industrial hygiene), exposure limits and credentials. FSU matches the '
        'statewide title; UF foregrounds the public-health framing. No institution carries a '
        'laboratory suffix, so sampling, monitoring or GIS work happens inside the lecture hours '
        'or as a project.',
        45, D3),
}

meta['PHI4300'] = {
    'title': 'PHI4300 Introduction to Epistemology - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'No statewide prerequisite. The "(U)" marker makes it upper division, and institutions '
        'normally expect upper-division standing plus at least one prior philosophy course; some '
        'restrict it to majors, which is invisible until registration fails. "Introduction" at the '
        '4000 level means an introduction to a SUBFIELD, not to philosophy. Take an introduction '
        'to philosophy and, more valuably, a LOGIC course first - this course reconstructs and '
        'evaluates arguments constantly. WARNING - THE GORDON RULE DESIGNATION DIFFERS BETWEEN '
        'CARRIERS and is invisible from title, number and credits: USF and UWF carry the Gordon '
        'Rule WRITING designation, UCF does NOT. A Gordon Rule course needs a grade of C or '
        'higher - a C-minus does not satisfy it at most institutions. So a UCF student taking this '
        'to clear a writing requirement has not cleared it. Never pick a course for a Gordon Rule '
        'requirement from its number; check your own designated list.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'PHI4300',
        'Three State University System institutions at 3 credits, all three titles naming the same '
        'subject - no credit and no subject divergence. What DOES differ is the Gordon Rule '
        'designation: USF and UWF carry the writing designation, UCF records none. The designation '
        'makes obvious sense for a course taught by argumentative essay, which makes UCF the '
        'notable case. Second worked example of institution-specific Gordon Rule designation in '
        'this catalog after HIS2050.',
        45, D3 + ' The scheduled hours describe this course poorly: the load is difficult reading '
        '(philosophical prose is slow by design and a fifteen-page article can take two hours) '
        'plus essay writing, which dominates. Look at the number of essays on the syllabus.'),
}

meta['PHY3107'] = {
    'title': 'PHY3107 Modern Physics II - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'Statewide: MODERN PHYSICS I. The sibling number reveals what that itself needs - PHY3106 '
        'is gated on PHY2054 or PHY2049 AND MAC2313, so the real chain is PHY2048 to PHY2049 to '
        'PHY3106 to this course, with calculus alongside. WARNING - the one-line prerequisite '
        'understates what is assumed: multivariable calculus and ordinary differential equations '
        '(solving the Schrodinger equation IS solving a differential equation), spherical '
        'coordinates, LINEAR ALGEBRA for operators and eigenvalues (often not stated and '
        'constantly assumed), special relativity throughout the nuclear and particle half, and '
        'fluent complex numbers. WARNING - Florida numbers "modern physics" at least SEVEN ways, '
        'and PHY3101 "Elements of Modern Physics" is a ONE-TERM treatment while PHY3106/3107 is a '
        'TWO-TERM sequence. Only two public institutions carry PHY3107 at all, so do not assume a '
        'second modern-physics term exists at yours. No laboratory attached: Modern Physics '
        'Laboratory is PHY4822/PHY4823, a separate registration.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'PHY3107',
        'Only TWO public carriers, both SUS, both at 3 credits - no credit divergence. UWF\'s '
        '"Calculus-Based Physics IV" is an ORDINAL-BASE divergence: it counts position in the '
        'whole introductory sequence where the statewide title counts within modern physics. Same '
        'course, different counting base. The larger issue is outside this number - Florida '
        'numbers modern physics at least seven ways, including PHY3101 as a ONE-TERM course '
        'covering what this two-term sequence covers over two, which is a sequence-LENGTH '
        'divergence with real transfer consequences. One private institution also carries the '
        'number as "General Physics II", a much lower-level reading, and is not listed here under '
        'the public-institution scope rule.',
        45, D3 + ' No laboratory is attached to this number; Florida numbers Modern Physics '
        'Laboratory I and II separately as PHY4822 and PHY4823.'),
}

meta['PHY4513'] = {
    'title': 'PHY4513 Thermodynamics and Kinetic Theory - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'Statewide: one year of college physics with calculus (PHY2048/PHY2049 in Florida). '
        'Institutions commonly add more, and the sibling numbers show what: PHY4503 requires '
        'PARTIAL DERIVATIVES explicitly and PHY4523 requires introductory modern physics plus '
        'partial derivatives. WARNING - the stated gate is physics and the REAL gate is '
        'mathematics: you will use multivariable calculus from the second week, and the statewide '
        'prerequisite does not require it. Prepare partial derivatives and the multivariable chain '
        'rule (MAC2313); EXACT versus INEXACT differentials, which students who never grasp '
        'struggle with the first law all term; Taylor and binomial expansions and STIRLING\'S '
        'APPROXIMATION, which appears in week three and never leaves; Gaussian integrals; and '
        'basic probability, which is assumed and rarely stated. Introductory modern physics is '
        'strongly advisable - the quantum-statistics half assumes quantum states, degeneracy and '
        'indistinguishability.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'PHY4513',
        'Three State University System institutions at 3 credits - no credit divergence and no '
        'subject divergence. But ALL THREE use a title the statewide record does not: the state '
        'says "Thermodynamics and Kinetic Theory" (the older pedagogical division) and every '
        'carrier says "Thermal and Statistical Physics" or "Mechanics" (the modern framing, in '
        'which statistical mechanics is the foundation). That unanimity is the point - the field '
        'moved and the statewide label did not follow. A second oddity: the state numbers "Thermal '
        '& Statistical Physics" separately as PHY5515, a GRADUATE course, so three undergraduate '
        'programmes are using the undergraduate thermodynamics number while naming it after a '
        'graduate title. The state\'s undergraduate numbering also still preserves the old split '
        '(PHY4503 Thermodynamics, PHY4523 Introductory Statistical Physics), so do not assume one '
        'of the three substitutes for another on transfer.',
        45, D3 + ' Treat the scheduled hours as a poor description of the load: this is a '
        'problem-set course, the sets are long, and the out-of-class time is where the learning '
        'happens. Budget nine to twelve hours a week.'),
}

meta['PLA3240'] = {
    'title': 'PLA3240 Alternative Dispute Resolution - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'Statewide: PLA1003, PLA2273 and BUL2130 - a real three-course gate, and informative. '
        'PLA1003 supplies the ethics and unauthorised-practice-of-law foundation; PLA2273 the '
        'procedural knowledge needed to write a mediation summary; BUL2130 the contract law behind '
        'a settlement agreement and an arbitration clause. Check '
        'your own catalog - institutions may substitute equivalents. This is a capstone-adjacent '
        'applied course inside a paralegal programme, not a general elective on conflict '
        'resolution: students from outside should look for a MAN, BUL, SPC or POS course instead. '
        'WARNING - the unauthorised practice of law is the boundary this course must teach. A '
        'paralegal may not advise a party whether to accept a settlement, and at mediation an '
        'unrepresented party will ask. Learn the sentence: "I cannot advise you on that - let me '
        'get the attorney." Florida Supreme Court mediator certification does NOT require a law '
        'degree; start the observation requirements as a student.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'PLA3240',
        'One Florida College System institution and two State University System institutions, '
        'IDENTICAL titles and identical credit values - nothing to resolve, and the FCS-to-SUS '
        'pairing is the cleanest transfer case Florida numbering produces. The statewide '
        'description is also unusually Florida-specific, naming mediation\'s "extensive '
        'application in the U.S. and particularly Florida" - Florida courts routinely order '
        'mediation before civil trial and the Florida Supreme Court certifies mediators in county, '
        'circuit civil, family, dependency and appellate categories.',
        45, D3 + ' Expect simulation sessions to run longer than a normal class block - a '
        'role-played mediation does not fit into fifty minutes - and expect to coordinate '
        'out-of-class simulation time with classmates.'),
}

json.dump(meta, open(os.path.join(HERE, 'meta.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('meta.json now holds %d entries' % len(meta))
for cid in IDS:
    n = meta[cid]['offering_notes']
    print('  %-9s %d public offerings, prereq %d chars'
          % (cid, len(n['offerings']), len(meta[cid]['prerequisites'])))
