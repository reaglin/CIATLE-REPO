"""Batch 203 metadata. Offerings built from the flat file (see batch 202 for the pattern)."""
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


IDS = ('JPN2200', 'JPN2201', 'LIT3191', 'MUN3213', 'MUN3426', 'MUN3483')
fam = {}
for pfx in ('JPN', 'LIT', 'MUN'):
    for r in scns.parse_flatfile(os.path.join(HERE, 'crslist.txt'), prefix=pfx):
        if r['code'] in IDS:
            fam.setdefault(r['code'], []).append(r)

NOTES = {
    'JPN2200': {
        'FIU': 'Matches the statewide title. FIU arrives here from JPN1130/1131 (3 credits each), '
               'not from the 4-credit concentrated sequence.',
        'UCF': 'Uses the SAME title for JPN2200 and JPN2201 - register by NUMBER, not title. '
               '"Civilization" in the title predicts substantive cultural and historical content '
               'alongside the language.',
        'UWF': 'Titled JAPANESE III. The ordinal counts SEMESTERS from the start of the language '
               '(Japanese I/II are the first year); the statewide ordinal counts within the '
               'intermediate year. Same course. A student searching for "Intermediate Japanese I" '
               'at UWF will not find it.',
    },
    'JPN2201': {
        'FIU': 'Matches the statewide sense of the course - the second term of the intermediate '
               'year.',
        'UCF': 'Uses the SAME title for JPN2200 and JPN2201 - register by NUMBER, not title.',
        'UWF': 'Titled JAPANESE IV, counting semesters from the start of the language. Same '
               'course as the statewide "Second-Year Japanese 2".',
    },
    'LIT3191': {
        'FGCU': 'Titled WORLD LITERATURE POST-1800 - a chronological narrowing layered on top of '
                'an already variable-content course. Excludes Gilgamesh, the Sanskrit epics, '
                'classical Chinese and Japanese poetry, the Tale of Genji, classical Arabic and '
                'Persian poetry, Greek and Roman epic, Dante and the Thousand and One Nights. If '
                'you need pre-modern world literature for a period requirement, ask which number '
                'covers it.',
        'UWF': 'Matches the statewide title, so open to the full chronological range. Content '
               'still varies by instructor every term.',
    },
    'MUN3213': {
        'USF': 'Titled UNIVERSITY ORCHESTRA - the ensemble\'s institutional name. At larger '
               'programmes "University Orchestra" is sometimes the SECOND orchestra, with a '
               '"Symphony Orchestra" above it; ask which ensembles exist and which number each '
               'uses.',
        'UF': 'Titled UNIVERSITY ORCHESTRA, same caution as USF.',
        'UWF': 'Titled ADVANCED SYMPHONY ORCHESTRA - "advanced" here is the statewide UPPER-LEVEL '
               'marker (the student\'s standing), not a claim about a separate, harder ensemble.',
    },
    'MUN3426': {
        'UNF': 'Titled SAXOPHONE QUARTET at 0-1 credit. A quartet is a FIXED four-player '
               'formation (soprano, alto, tenor, baritone, one to a part) with no conductor and '
               'nowhere to hide - a different experience from a larger ensemble. The 0 option is '
               'participation WITHOUT credit, useful against the 8-use degree cap and Florida '
               'excess hours, but it does not count toward full-time enrolment.',
        'UWF': 'Titled SAXOPHONE QUARTET at 0-1 credit - same formation and same zero-credit '
               'option as UNF.',
        'UCF': 'Titled SAXOPHONE ENSEMBLE at a fixed 1 credit - matches the statewide title. '
               'Larger and more accommodating of numbers, with several players per part. If you '
               'want quartet playing specifically, ask whether quartets are formed within it - '
               'they often are, informally.',
    },
    'MUN3483': {
        'UNF': 'Titled JAZZ GUITAR ENSEMBLE at 0-1 credit - guitars, but a different repertoire '
               'and technique (chord charts, comping, improvisation, usually amplified). WARNING: '
               'the state numbers jazz guitar ensemble separately at MUN3484/3486/3488, so this '
               'is a local filing on the classical-guitar number. The 0 option is participation '
               'without credit and does not count toward full-time enrolment.',
        'UCF': 'Titled STRING ENSEMBLE - A DIFFERENT INSTRUMENT FAMILY ENTIRELY (violin, viola, '
               'cello, bass). A guitarist registering here on the strength of the statewide title '
               'would be in the wrong ensemble. WARNING: the state numbers string ensemble '
               'separately at MUN3413/3414/3243, so dedicated numbers for this exist.',
        'UWF': 'Titled GUITAR ENSEMBLE - the only carrier matching the statewide subject.',
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
            c = None            # 'VAR' or a range such as '0-1'
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

REHEARSAL = (
    'Derived, not published, and it describes SCHEDULED REHEARSAL TIME ONLY. A university '
    'ensemble of this kind rehearses roughly two to five hours a week across a fifteen-week '
    'term, which is about this figure - and it excludes individual part preparation, sectionals '
    'or coaching, dress rehearsals, and concerts on evenings and weekends. Realistically five to '
    'ten hours a week for one credit. No institution publishes an hour figure.')

meta = json.load(open(os.path.join(HERE, 'meta.json'), encoding='utf-8'))

meta['JPN2200'] = {
    'title': 'JPN2200 Intermediate Japanese I - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'Statewide: JPN1121 or equivalent - the second term of first-year Japanese. "Or '
        'equivalent" does real work here: institutions accept their own first-year sequence, a '
        'placement test, prior study or heritage proficiency; if you learned Japanese outside a '
        'classroom, ask for a placement assessment. WARNING - UWF titles this JAPANESE III, '
        'counting semesters from the start of the language, so a student searching a UWF catalog '
        'for "Intermediate Japanese I" will not find it. UCF uses the SAME title for both halves '
        'of the year, so register by number. WARNING - FLORIDA NUMBERS FIRST- AND SECOND-YEAR '
        'JAPANESE UNDER FOUR PARALLEL FAMILIES and SCNS equivalency does not cross numbers: USF, '
        'FSU, FAU and Miami Dade use JPN2220/2221 at 4 credits and UF uses JPN2230/2231 at 5, so '
        'most institutions do not carry this number. Before transferring, send your syllabus and '
        'the chapters covered to the language DEPARTMENT and ask for a placement interview. Dual '
        'enrolment earns high-school FOREIGN LANGUAGE credit.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'JPN2200',
        'Three State University System institutions, all at 3 credits - no credit divergence and '
        'no subject divergence. The divergence is in naming, in two forms: UWF\'s "Japanese III" '
        'is an ordinal counted from a different base (semesters from the start, not within the '
        'intermediate year), and UCF uses one title for both JPN2200 and JPN2201. The larger '
        'issue is outside this number: Florida runs FOUR parallel number families for the same '
        'two years of Japanese (JPN2200/2201 at 3 cr; JPN2220/2221 at 4 cr; JPN2230/2231 at 5 '
        'cr), so two years of Japanese is 12 credits in one family and 20 in another.',
        45, D3 + ' Treat it as a FLOOR for a language course: language classes commonly meet '
        'three to five times a week rather than twice, and the out-of-class load is daily and '
        'non-negotiable - kanji and vocabulary need short daily sessions, not weekly long ones. '
        'Budget ten to twelve hours a week.'),
}

meta['JPN2201'] = {
    'title': 'JPN2201 Second-Year Japanese 2 - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'Statewide: JPN2200 or equivalent. "Or equivalent" carries real weight given the four '
        'parallel number families - institutions accept their own second-year first term, a '
        'placement test, study abroad or heritage proficiency. WARNING - UWF titles this JAPANESE '
        'IV and UCF uses the SAME title for both halves, so register by number. Note the statewide '
        'titles of the pair are inconsistent ("Intermediate Japanese I" and "Second-Year Japanese '
        '2") - two halves of one year. WARNING - most institutions do not carry this number: USF, '
        'FSU, FAU and Miami Dade end second year at JPN2221 and UF at JPN2231, and SCNS '
        'equivalency does not cross numbers. That matters more here than for JPN2200 because THIS '
        'is usually the course that CLOSES a foreign-language requirement: get that requirement in '
        'writing, and note that many institutions accept a proficiency examination instead. Dual '
        'enrolment earns high-school FOREIGN LANGUAGE credit. Do not leave a gap after JPN2200.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'JPN2201',
        'Three State University System institutions, all at 3 credits - no credit divergence and '
        'no subject divergence; all three are the second term of second-year Japanese. The '
        'divergence is in naming: UWF\'s "Japanese IV" counts semesters from the start of the '
        'language, and UCF uses one title for both halves of the year. Because this course '
        'typically closes a degree foreign-language requirement, a number mismatch on transfer is '
        'more consequential here than on its partner.',
        45, D3 + ' Treat it as a FLOOR: language courses commonly meet three to five times a week, '
        'and the daily out-of-class load is non-negotiable. Budget ten to twelve hours a week, '
        'distributed daily rather than concentrated.'),
}

meta['LIT3191'] = {
    'title': 'LIT3191 World Literature - Curriculum Guide',
    'credits': 3,
    'contact_hours': 45,
    'prerequisites': (
        'No statewide prerequisite - unusual at the 3000 level, and it means the course is '
        'accessible from outside the major. Institutions generally expect upper-division standing '
        'and first-year composition; some restrict it to majors and minors, which is invisible '
        'until registration fails. WARNING - THIS IS A VARIABLE-CONTENT '
        'COURSE. The statewide description says the texts "vary each semester according to '
        'interest and expertise of the instructor", so two students who both took LIT3191 may have '
        'read nothing in common. Read the current term\'s syllabus before registering if you can '
        'get it, and SAVE IT - the transcript line conveys nothing about what you read, and the '
        'syllabus is the only record for a graduate application or a transfer evaluation. WARNING '
        '- neither public carrier records a humanities general-education designation on this '
        'number, so do not assume it satisfies a humanities requirement; check your own '
        'institution\'s designated list. FGCU restricts the course to writing after 1800.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'LIT3191',
        'Two public carriers, both SUS, both at 3 credits - no credit divergence. UWF matches the '
        'statewide title and is open to the full chronological range; FGCU restricts the number to '
        'post-1800 writing, which is a chronological narrowing layered on top of an already '
        'variable-content course. One private institution also carries the number at 4 credits, '
        'titled "Contemporary World Literature: 1900 to the Present" - not listed here under the '
        'public-institution scope rule, but note it narrows further still. Neither public carrier '
        'records a humanities general-education designation.',
        45, D3 + ' The scheduled hours describe this course badly: the work is reading and writing '
        'outside class, and a literature course\'s real load is set by the page count and the '
        'number of essays, neither of which appears in the credit value. Look at the syllabus\'s '
        'reading schedule, not its meeting pattern. Budget eight to ten hours a week.'),
}

meta['MUN3213'] = {
    'title': 'MUN3213 Symphony Orchestra (Upper Level) - Curriculum Guide',
    'credits': 1,
    'contact_hours': 45,
    'prerequisites': (
        'Statewide: AUDITION - which decides not only admission but which chair you occupy, and '
        'in a string section that decides what you play. Auditions are usually in the first days '
        'of the term or the term before, so contact the conductor or music office BEFORE the term '
        'starts and ask what is required and whether excerpts are published. Non-majors are '
        'generally welcome. WARNING - ONE credit, and the hours are nothing like it: rehearsals '
        'plus part preparation plus sectionals plus dress rehearsals plus concerts on evenings and '
        'weekends, realistically six to ten hours a week, concentrated around concert weeks. Get '
        'the concert dates and rehearsal schedule before registering - they are fixed for the '
        'season and a missed concert is generally not recoverable. WARNING - the MUN level digit '
        'records YOUR standing, not a different ensemble; register at your own classification '
        '(the lower-division orchestra is MUN1210, not MUN1213).'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'MUN3213',
        'Three State University System institutions, all at 1 credit, all naming the same ensemble '
        '- no divergence to resolve, which is uncommon in this catalog. The small title '
        'differences are informative rather than divergent: "University Orchestra" is an '
        'institutional name and at larger programmes may denote the SECOND orchestra, while UWF\'s '
        '"Advanced" is the statewide upper-level marker (the student\'s standing) rather than a '
        'separate harder ensemble. Note the MUN prefix numbers each ensemble at lower-division, '
        'upper-division and graduate level, so the same rehearsal holds students enrolled under '
        'three different numbers.',
        45, REHEARSAL),
}

meta['MUN3426'] = {
    'title': 'MUN3426 Saxophone Ensemble - Curriculum Guide',
    'credits': 1,
    'contact_hours': 45,
    'prerequisites': (
        'No statewide prerequisite listed, but in practice the gate is an audition or the '
        'director\'s consent - and for a quartet it is necessarily selective, because there are '
        'four places. Ensembles are formed in the first days of a term, so contact the saxophone '
        'faculty BEFORE the term starts. WARNING - "QUARTET" IS NARROWER THAN "ENSEMBLE". UNF and '
        'UWF run a saxophone QUARTET (soprano, alto, tenor, baritone, one to a part, no conductor, '
        'every part exposed); UCF runs a larger ENSEMBLE with several players per part. Both are '
        'this number. WARNING - UNF and UWF list the credit as 0-1, INCLUDING ZERO: participation '
        'without credit, useful against the statewide 8-use degree cap and Florida excess hours, '
        'but a zero-credit course does NOT count toward full-time enrolment (aid, athletic '
        'eligibility, visa status). Ask what your registration is worth. Statewide: may be used '
        'in a degree a maximum of 8 times - confirm how many YOURS counts.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'MUN3426',
        'Three State University System institutions, and two divergences, neither about the '
        'subject. First, formation: UNF and UWF title it QUARTET (a fixed four-player, '
        'conductorless formation where every part is exposed) while UCF matches the statewide '
        'ENSEMBLE (any size, several players per part). Second, credits: UNF and UWF list 0-1, '
        'including ZERO - participation without credit, the THIRD distinct reason a Florida course '
        'carries zero credits, after PSAV clock-hour courses and zero-credit corequisite '
        'laboratories. The statewide record states the number may be used in a degree programme a '
        'maximum of 8 times.',
        45, REHEARSAL),
}

meta['MUN3483'] = {
    'title': 'MUN3483 Guitar Ensemble (Upper Level) - Curriculum Guide',
    'credits': 1,
    'contact_hours': 45,
    'prerequisites': (
        'Statewide: CONSENT OF INSTRUCTOR. Ensembles are formed in the first days of a term, so '
        'email the guitar or ensemble faculty before the term starts; non-majors are often welcome '
        'because the pool of players is smaller than for orchestral instruments. WARNING - THREE '
        'CARRIERS, THREE DIFFERENT ENSEMBLES, AND ONE IS NOT GUITAR AT ALL. UWF runs a Guitar '
        'Ensemble (the statewide subject); UNF runs a JAZZ Guitar Ensemble (chord charts, comping, '
        'improvisation, usually amplified); UCF runs a STRING ENSEMBLE - violin, viola, cello and '
        'bass. A guitarist registering at UCF on the strength of the statewide title would be in '
        'the wrong ensemble. The state assigns separate numbers to both other readings '
        '(MUN3484/3486/3488 jazz guitar; MUN3413/3414/3243 string ensemble). Ask the faculty two '
        'questions first: which instruments does this ensemble contain, and is the repertoire '
        'notated or chart-based? UNF lists 0-1 credit, including zero, which does not count '
        'toward full-time enrolment.'
    ),
    'version': '1.0',
    'offering_notes': notes(
        'MUN3483',
        'Three State University System institutions running THREE DIFFERENT ENSEMBLES, and only '
        'UWF matches the statewide subject. UNF runs a jazz guitar ensemble; UCF runs a STRING '
        'ensemble - a different instrument family entirely. What makes this worse than ordinary '
        'title drift is that the state already assigns separate numbers to both other readings: '
        'MUN3484/3486/3488 for jazz guitar ensemble and MUN3413/3414/3243 for string ensemble. So '
        'two of three carriers are using a number the state assigns to something else while '
        'dedicated numbers for what they run exist. UNF also lists 0-1 credit including zero.',
        45, REHEARSAL),
}

json.dump(meta, open(os.path.join(HERE, 'meta.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('meta.json now holds %d entries' % len(meta))
for cid in IDS:
    n = meta[cid]['offering_notes']
    print('  %-9s %d public offerings, prereq %d chars'
          % (cid, len(n['offerings']), len(meta[cid]['prerequisites'])))
