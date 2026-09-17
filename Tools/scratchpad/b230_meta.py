"""Batch 230 metadata -- FIL (film), the five queued rows.

Credits and contact hours (no carrier publishes hours anywhere in FIL):
  FIL3427C  3 cr / 60   C suffix, the queued id (batch-189 rule: integrated form)
  FIL3833   3 cr / 45   both carriers 3
  FIL4036   3 cr / 45   UWF 3, FAU 4 -- 3 is the prefix norm
  FIL4102   3 cr / 45   sole public carrier UWF
  FIL4364   3 cr / 45   UWF 3, FAU 4 -- 3 is the prefix norm

*** HEADLINE: FIL4036 -- THREE different spans under one number ***

  statewide  Film History 1, "late 19th century until 1959", and FIL4037
             "from 1960 through the present" lists it as PREREQUISITE
  FAU        "Film to the 1940s", 1890s-1940s, paired with "Film Since the
             1940s" -- and FAU says explicitly "May be taken BEFORE FIL 4036"
  UWF        "History of Motion Pictures" -- NO period boundary, and UWF
             carries NO FIL4037 at all

⚠⚠⚠ So the 1940s-50s are INSIDE this course for the state and OUTSIDE it at
FAU: film noir, Italian neorealism, the blacklist, the Paramount decree, the
arrival of television and widescreen. That is not a marginal stretch of syllabus.

⚠⚠ TWO divergences on one sequence, not one: the BOUNDARY (1940s vs 1959) and
the ORDERING (state makes part 2 require part 1; FAU says either order). Plus
UWF's single-course structure = sequence-LENGTH divergence (batch 204). Three
structures for one subject.

*** AND THE SEQUENCE PARTNER IS ALSO DIVERGENT (batch 181 rule paying off) ***
FIL4037 statewide = Film History 2. USF carries FIL4037 as "HISTORY OF VIDEO
ART" -- a different subject entirely (avant-garde fine-art medium, not film
history). So a student cannot just enrol in FIL4037 wherever they find it.
⚠ The batch-181 drill said: on finding a divergence, probe the partner. Done,
and it turned up a second, unrelated problem.

*** SECOND: FIL3833 -- a title divergence that DISSOLVES (the batch-227 shape) ***
UNF "Film Genre" vs UWF "Film Styles"; statewide "Film Styles". Genre and style
ARE different critical categories, so this looks like a collision. ⚠ It is not:
the statewide description names BOTH ("through the STYLES of selected filmmakers
with emphasis on GENRES, national movements"). UWF's own description covers
genres AND movements AND production approaches. Each carrier titled the course
after one of the two halves it teaches. Handling: REASSURE, per batch 227.

*** THIRD: FIL4102 -- a Gordon Rule WRITING designation, and two exclusions ***
UWF flags gordon_rule + gordon_writing, and its catalogue carries the UWF label
"Meets College-Level Communication Skills Requirement" -- which the batch-179
rule identifies as the WRITING half. ⚠⚠ So C-or-higher is required to count,
stated in the guide. Also: repeatable to 6 sh; and credit may not be received
for BOTH FIL4102 and MMC4103.
⚠ The batch-207 conjunction test comes out CLEAN here: statewide title says
"Screenwriting AND Storyboarding", UWF's title drops storyboarding but its
DESCRIPTION delivers it ("script formats, storyboarding, and story pitches").
Worth recording that the test can pass -- most instances so far have failed.
⚠ Statewide prerequisite is "INTRODUCTION TO MOTION PICTURE/" -- PROSE, and
truncated mid-phrase. The batch-227 sixth shape (no course-looking token at all),
with truncation on top.
⚠ Screenwriting also runs at FIL4106 (FAU, "Script Writing", 4 cr).

*** FOURTH: FIL3427C -- institutional signature, cleanly ***
USF carries FIL3427C "Film I"; UWF carries bare FIL3427 "Film Production I".
Both 3 credits, neither carries both forms = batch-219 row 2, one course filed
two ways. UWF's description supplies the content for both.
⚠ UWF runs a three-rung ladder: FIL3427 -> FIL4435 (Production II) -> FIL4514
(Production III, practicum, finished 10-20 min narrative short). The guide says
to plan all three from term one, since each gates the next.

*** FAU's 4 CREDITS IS AN INSTITUTIONAL PATTERN, not a per-course fact ***
11 of FAU's 21 undergraduate FIL courses are 4 credits; every other institution
carries the prefix almost entirely at 3 (UCF 78/103 at 3, USF 25/25, UNF 24/25,
PBSC 24/26). ⚠ So write it as "FAU runs this prefix at 4 credits", not as a
divergence about FIL4036 or FIL4364 specifically. Said once per guide.
⚠ Also noted in passing: FSU's FIL profile is dominated by VARIABLE credit
(1-6 appears 28 times) and UCF has 22 VAR rows -- a production-school pattern.

*** DISTRIBUTION TEST: stratified, and it correctly says nothing ***
hs_credit across public undergrad FIL: LOWER 54 FA / 111 EL (33% fine arts --
genuinely substantial), UPPER 1 FA / 222 EL. ⚠ All five targets are UPPER, so
the field is boilerplate FOR THEM. Batch-227 rule applied: stratify by the
population the field applies to (dual enrolment = lower division). One line in
each guide saying it says nothing, and no finding claimed.

*** CIP, banked for the career-paths phase ***
FAU tags FIL4036/4037/4364/4106 as 50.0602 (Film/Cinema/Video Studies) but
⚠ FIL3803 Film Theory as 09.0702 (Digital Communication/Media) -- same
department, two CIP families. A WITHIN-institution instance of the REVIEW_QUEUE
item 103 disagreement, which previously only had between-institution evidence.

Prefix: 436 live ids, 372 single-carrier (85%) -- among the highest measured.
Sources: UWF PDF (4 of 5), FAU Coursedog, statewide CSV.
⚠ UNF unreadable (bepress 403); USF still has no course-description route.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
UNF = 'University of North Florida'
FAU = 'Florida Atlantic University'
USF = 'University of South Florida'

# Shared block -- FAU's prefix-wide 4-credit pattern, spent on the two courses
# FAU carries. Kept short.
FAU4 = ('*** FAU RUNS THIS WHOLE PREFIX AT 4 CREDITS (11 of its 21 undergraduate FIL courses) where '
        'every other institution is almost entirely 3 - a pattern, not a fact about this course. ')

NEW = {

  'FIL3427C': {
    'title': 'Introduction to Film Production',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'NONE listed statewide or by either carrier. '
      '*** THE SAME COURSE IS FILED TWO WAYS: USF carries FIL3427C "Film I"; UWF carries the bare '
      'FIL3427 "Film Production I". Both 3 credits, neither carries both forms - the signature of one '
      'course filed two ways, so an evaluator matching the identifier sees a mismatch where there is '
      'none. Name the equivalence on transfer paperwork. '
      '*** THE REAL COMMITMENT IS WELL ABOVE THE SCHEDULED HOURS. Shoots happen outside class, take '
      'whole days, and depend on other students, weather and locations; editing then takes longer than '
      'shooting. DO NOT take a production course in a term with fixed work shifts. '
      '*** PLAN THE WHOLE LADDER FROM TERM ONE: this gates Production II (FIL4435), which gates '
      'Production III (FIL4514), the practicum where you finish a 10-20 minute short. Starting late '
      'costs a year, not a semester. *** Keep two backups of everything you shoot.'),
    'offering_notes': {
      'summary': ('One public carrier of the C identifier (USF); a second (UWF) carries the same course '
                  'under the unsuffixed FIL3427. Both 3 credits; no institution publishes contact hours '
                  'anywhere in the FIL prefix.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("Florida's convention for a 3-credit integrated C course (Ron, 2026-09-15), which "
                     'is the queued identifier. Treat it as a floor: production work is not compressible '
                     'into scheduled hours.'),
      'offerings': [
        {'institution': 'USF', 'institution_name': USF,
         'title': 'Film I', 'credits': 3, 'contact_hours': None,
         'note': ('Sole public carrier of the C identifier. USF exposes no course-description route, so '
                  'its own description and prerequisite could not be read; title and credits are from '
                  'the statewide record and the syllabus is the authority.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Film Production I', 'credits': 3, 'contact_hours': None,
         'note': ('Carries the UNSUFFIXED FIL3427, not this identifier - listed because it is the same '
                  'course and the number difference is the transfer trap. Department of Communication. '
                  '"Introductory course covering SINGLE-CAMERA film and television production... basic '
                  'efficiency with cameras, lighting equipment, sound recording, and editing picture '
                  'and sound. The theory and practice of narrative film production, as well as aspects '
                  'of television and documentary production." Prerequisite for FIL4435 Production II, '
                  'which gates FIL4514 Production III.')},
      ],
    },
  },

  'FIL3833': {
    'title': 'Film Styles',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF: ENC 1102, and it MAY BE TAKEN IN THE SAME TERM. UNF: not published. '
      '*** THE TWO TITLES LOOK LIKE A COLLISION AND ARE NOT. UNF calls this "Film Genre" and UWF calls '
      'it "Film Styles" - and genre and style really are different critical categories - but the '
      'STATEWIDE DESCRIPTION NAMES BOTH: "the STYLES of selected filmmakers with emphasis on GENRES, '
      'national movements". UWF\'s own description covers genres (Westerns, sci-fi, noir), movements '
      '(German Expressionism, Soviet Montage, Italian Neo-Realism, the New Waves) AND production '
      'approaches. Each carrier titled the course after one half of what it teaches. '
      '*** SO IF YOUR CATALOGUE CALLS IT FILM GENRE, IT IS STILL THIS COURSE - but send the syllabus '
      'on transfer, because an evaluator comparing the two titles may reasonably hesitate. '
      '*** VIEWING IS THE COURSEWORK, not preparation for it. UWF assesses through online film '
      'viewings, readings and short essays; falling behind on viewing makes the writing impossible.'),
    'offering_notes': {
      'summary': ('Two public carriers, both at 3 credits, with different titles that name two halves '
                  'of one statewide subject. No contact hours published.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Florida's 1:15 convention on 3 credits; both carriers list 3. Screenings are "
                     'additional - budget a film a week on top.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Film Styles', 'credits': 3, 'contact_hours': None,
         'note': ('Department of Communication. Matches the statewide title. Prerequisite ENC 1102, '
                  'which may be taken concurrently. Covers genres and sub-genres, film movements and '
                  'production approaches; assessed by online viewings, readings and short essays. May '
                  'not be repeated.')},
        {'institution': 'UNF', 'institution_name': UNF,
         'title': 'Film Genre', 'credits': 3, 'contact_hours': None,
         'note': ("UNF's live catalogue is client-rendered and its archived catalogue PDFs are blocked "
                  'at the host, so its own description and prerequisite could not be read; title and '
                  'credits are from the statewide record.')},
      ],
    },
  },

  'FIL4036': {
    'title': 'Film History 1',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'FAU: FIL 2000 Film Appreciation. UWF: none. '
      '*** CHECK WHERE YOUR COURSE STOPS - THREE DIFFERENT SPANS SIT ON THIS NUMBER. Statewide it runs '
      'to 1959; FAU\'s "Film to the 1940s" stops at the 1940s; UWF\'s "History of Motion Pictures" has '
      'NO boundary and UWF carries no part 2 at all. So film noir, Italian neorealism, the blacklist, '
      'the break-up of the studio system and the arrival of television are INSIDE this course for the '
      'state and OUTSIDE it at FAU. '
      '*** ORDERING DIFFERS TOO: the state makes Film History 2 require this course; FAU says its halves '
      'may be taken in either order. '
      '*** CHECK THE PARTNER BEFORE RELYING ON IT: FIL4037 is Film History 2 statewide and at FAU, but '
      'USF carries FIL4037 as HISTORY OF VIDEO ART - a different subject. '
      '*** ON TRANSFER SEND A SCREENING LIST, not the title. ' + FAU4),
    'offering_notes': {
      'summary': ('Two public carriers at different credit values covering different spans, against a '
                  'statewide definition that matches neither exactly. No contact hours published.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Florida's 1:15 convention on 3 credits, the value carried across almost the whole "
                     'FIL prefix. At FAU the identifier is 4 credits, so 60 hours is right there.'),
      'offerings': [
        {'institution': 'FAU', 'institution_name': FAU,
         'title': 'Film to the 1940s', 'credits': 4, 'contact_hours': None,
         'note': ('"History of film, 1890s to 1940s. Theoretical, industrial and social aspects of film '
                  'in a variety of national and cultural contexts. Emphasis on narrative and avant-garde '
                  'styles and traditions." Prerequisite FIL 2000. Paired with FIL4037 "Film Since the '
                  '1940s" (4 cr), which states it MAY BE TAKEN BEFORE this course - so FAU splits the '
                  'history two decades earlier than the state does, and does not sequence the halves.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'History of Motion Pictures', 'credits': 3, 'contact_hours': None,
         'note': ('Department of Communication. "Evolution of film as a dynamic art form and medium of '
                  'mass communication. Weekly film screening." NO period boundary, and UWF carries no '
                  'FIL4037 - the whole history in one course. NOTE credit may not be received for both '
                  'FIL4036 and either FIL4036C or FIL4403C.')},
      ],
    },
  },

  'FIL4102': {
    'title': 'Screenwriting and Storyboarding',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE listed by UWF. The STATEWIDE prerequisite field reads "INTRODUCTION TO MOTION PICTURE/" - '
      'prose rather than a course identifier, and truncated mid-phrase. There is no such course to find. '
      '*** THIS COURSE CARRIES A GORDON RULE WRITING DESIGNATION AT UWF ("Meets College-Level '
      'Communication Skills Requirement"), SO A GRADE OF C OR HIGHER IS REQUIRED FOR IT TO COUNT. A '
      'C-minus does not satisfy it - stricter than the ordinary passing standard, and stricter than '
      'what shows as a pass on your transcript. The designation is made by the INSTITUTION, so check '
      'your own if you take a comparable course elsewhere. '
      '*** TWO EXCLUSIONS: credit may not be received for both FIL4102 and MMC4103; and the course is '
      'REPEATABLE to 6 sh, which is worth using to leave with two finished scripts. '
      '*** A WORKSHOP IS HEAVIER THAN ITS CREDITS. Do not stack it with another writing-intensive '
      'course. *** Screenwriting also runs at FIL4106 (FAU, 4 cr).'),
    'offering_notes': {
      'summary': ('One public carrier (UWF) at 3 credits, carrying a Gordon Rule writing designation. A '
                  'private institution also carries the number. No contact hours published.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Florida's 1:15 convention on 3 credits. Treat it as a floor: a workshop course is "
                     'assessed on pages produced, plus reading everyone else\'s.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Screenwriting for Film, TV, and Digital Media', 'credits': 3, 'contact_hours': None,
         'note': ('Sole public carrier. Department of Communication. "Study and practice of writing for '
                  'narrative mass media, including screenplays, teleplays, and digital media formats... '
                  'Additional topics include script formats, storyboarding, and story pitches." GORDON '
                  'RULE WRITING designation - C or higher required. May be repeated for up to 6 sh. '
                  'Credit may not be received for both this and MMC4103. NOTE the statewide title '
                  'promises "Screenwriting AND Storyboarding" and UWF\'s title drops storyboarding, but '
                  'its description delivers it - the conjunction test passes here.')},
      ],
    },
  },

  'FIL4364': {
    'title': 'Documentary Film and Video',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE at either carrier. '
      '*** BOTH CARRIERS TEACH THE STATEWIDE SUBJECT, differing in emphasis: FAU ("Traditions of '
      'Documentary Film") is theoretical and international and reproduces the statewide description '
      'almost verbatim; UWF ("Documentary Film and Television") is historical and SOCIOLOGICAL and '
      'includes television. '
      '*** READ THE STATEWIDE DESCRIPTION\'S LIST: style, IDEOLOGY, technology, determination. Not a '
      'neutral history of a genre - documentary claims to show the world and the course interrogates '
      'that claim. Expect substantial ethics content. '
      '*** THE PRACTICAL DIVERGENCE IS CREDITS: moving UWF to FAU you carry 3 against a 4-credit course, '
      'which surfaces at the final audit, not at transfer. Ask how the shortfall is handled. ' + FAU4 +
      '*** Screenings are additional, and documentaries are often feature length.'),
    'offering_notes': {
      'summary': ('Two public carriers at different credit values, aligned on subject and differing in '
                  'emphasis. No contact hours published.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Florida's 1:15 convention on 3 credits, the value carried across almost the whole "
                     'FIL prefix. At FAU the identifier is 4 credits, so 60 hours is right there.'),
      'offerings': [
        {'institution': 'FAU', 'institution_name': FAU,
         'title': 'Traditions of Documentary Film', 'credits': 4, 'contact_hours': None,
         'note': ('"Survey of the diverse forms and historical functions of nonfiction films and video '
                  'throughout the world. Analysis of representative and significant texts; discussion '
                  'of issues of style, ideology, technology, determination." Essentially the statewide '
                  'description verbatim. Theoretical and international emphasis.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Documentary Film and Television', 'credits': 3, 'contact_hours': None,
         'note': ('Department of Communication. "Historical and sociological study of the development of '
                  'documentary film and television. Includes analysis of documentary film techniques and '
                  'viewing of selected documentaries." May not be repeated. Explicitly includes '
                  'television, where the statewide record says "video" and FAU says neither.')},
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
    for cid, m in sorted(NEW.items()):
        n = len(m['prerequisites'])
        print('%-9s prerequisites %4d chars%s' % (cid, n, '   *** OVER 1000 ***' if n > 1000 else ''))
    meta.update(NEW)
    with open(META, 'w', encoding='utf-8') as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print('meta.json: %d -> %d entries' % (before, len(meta)))


if __name__ == '__main__':
    main()
