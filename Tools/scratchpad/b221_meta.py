"""Batch 221 metadata -- PLA (paralegal / legal studies), the six queued rows.

All six are 3 credits, no suffix -> 45 contact hours. UCF's Kuali records for
PLA4191, PLA4554 and PLA4764 all publish ZERO lab hours, corroborating the
plain-suffix reading for a third consecutive batch.

*** THE BATCH'S HEADLINE: THE PARALEGAL LADDER ***
PLA splits by SECTOR more comprehensively than any prefix measured so far.
The A.S. in Paralegal Studies is overwhelmingly an FCS credential using
PLA1xxx/2xxx; the BS in Legal Studies is an SUS credential using
PLA3xxx/4xxx. Measured, not assumed:

  family law     PLA2800 (18 public carriers, ALL FCS)
                 PLA3806 (FGCU, UWF -- SUS)   PLA4806 (UCF; + SPC)
  law office mgt PLA2763 (10 public carriers, ALL FCS)
                 PLA4764 (UCF, UWF -- SUS)
  property       PLA2610 (FCS)  PLA3613 (UWF)  PLA3615 (UCF)
  bankruptcy     PLA2460 (FCS)  PLA3464 (UWF)  PLA4464 (UCF)

*** THIS IS A DIFFERENT DIAGNOSIS FROM CCJ (batch 220) ***
In CCJ the sector split was a DEFECT -- one course numbered twice, catching
transfer students. Here it is deliberate ARTICULATION DESIGN: the bachelor's
needs upper-division hours, so the universities renumber. The guides say so,
and warn about repeated content + Florida excess hours instead of warning
about a lost credit.

*** TWO COUNTER-CASES kept honest ***
SPC (FCS) carries PLA4554 and PLA4806 at 4000 level; sector does NOT
determine level. And PLA4191/PLA4554 have NO lower-division twin.

*** DANGLING PREREQUISITES, twice, and the MECHANISM is now clear ***
PLA4554's statewide prereq is "PLA 1003 AND PLA 2203" -- UCF carries NEITHER
(its real gate is ENC 1102); SPC carries both. PLA3806's is "PLA 1003" --
FGCU carries it, UWF does not. The statewide prerequisite is contributed by
the FCS side of a sector-split prefix and does not resolve on the SUS side.
That explains the batch-219 TPA shape rather than merely repeating it.

Stratified distribution test (batch-220 rule) over 164 active UNDERGRADUATE
rows: transferable 162 GUAR / 2 NOT-AUTO, hs_credit 164/164 elective, dual
enrolment 155 Y / 9 N. All boilerplate; all six courses carry the common
value. Prefix: 286 live ids, 190 single-carrier (66%), max 21 carriers.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
UCF = 'University of Central Florida'
FGCU = 'Florida Gulf Coast University'
SPC = 'St. Petersburg College'

# NOTE on the paralegal ladder: it is the batch's headline finding, but it
# needs ~300 characters to state usefully and no prerequisite field had the
# room. It is written into every guide's HTML instead, with the specific
# lower-division twin named per course. Do not spend the budget on it here.

# Shared block -- the professional limit. Applies to every course in the
# prefix and is the thing Florida actually enforces.
UPL = ('Florida has no paralegal licence; Florida Registered Paralegal is VOLUNTARY. The binding '
       'constraint is the UPL prohibition, actively enforced here: never give legal advice.')

NEW = {

  'PLA3464': {
    'title': 'Bankruptcy Law',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE published by UWF or by the state. '
      '*** ONLY UWF CARRIES THIS NUMBER among Florida public institutions. UCF teaches the same '
      'subject as PLA4464 and the state colleges as PLA2460 - three numbers, one subject, and SCNS '
      'equivalency does not cross numbers. Send a syllabus, not a number. *** '
      'FLORIDA EXEMPTIONS ARE THE REASON THIS COURSE DIFFERS HERE: Florida OPTED OUT of the federal '
      'exemption scheme (Fla. Stat. 222.20), and the homestead exemption (Fla. Const. Art. X, s.4) '
      'is UNLIMITED IN VALUE, capped by acreage instead - among the strongest in the country, though '
      'federal law caps it for recently acquired property. Personal-property exemptions are modest by '
      'comparison. *** 11 U.S.C. s.110 regulates non-lawyer "bankruptcy petition preparers" '
      'specifically and bars giving advice - including which chapter to file. ' + UPL),
    'offering_notes': {
      'summary': ('One public carrier (UWF) at 3 credits, no published prerequisite or contact '
                  'hours. A private institution also carries the number and is excluded under the '
                  'public-institution scope rule.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("UWF publishes no contact hours. 45 is Florida's convention for a 3-credit "
                     'course with no C or L suffix (Ron, 2026-09-15).'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Bankruptcy Law', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "Introduction to bankruptcy law and the '
                  'rights of both debtors and creditors. An examination of both the procedural and '
                  'substantive law related to Chapter 7 and Chapter 13 bankruptcy, including the '
                  'automatic stay, eligibility for specific bankruptcy filings, exemptions from '
                  'bankruptcy, and fraudulent transfers." DEPARTMENT OF CRIMINAL JUSTICE, Col of '
                  'Arts, Soc Sci and Human - UWF houses its legal studies courses there, whereas '
                  'UCF runs a dedicated Department of Legal Studies.')},
      ],
    },
  },

  'PLA3613': {
    'title': 'Property Law and Transactions',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'NONE published by UWF or by the state. '
      '*** ONLY UWF CARRIES THIS NUMBER. UCF uses PLA3615 and the state colleges PLA2610 for the '
      'same subject. *** FLORIDA HOMESTEAD IS THREE SEPARATE DOCTRINES and confusing them is the '
      'classic mistake: (1) creditor protection, unlimited in value, capped by acreage; (2) the tax '
      'exemption with Save Our Homes and portability; (3) RESTRICTIONS ON DEVISE AND ALIENATION - if '
      'there is a surviving spouse or minor child the homestead cannot be freely devised, and a '
      'conveyance or mortgage generally needs spousal joinder. The third is where transactions go '
      'wrong. *** WIRE FRAUD IS THE PRACTICAL HAZARD OF THIS PRACTICE AREA: closings are a primary '
      'target and losses are irreversible. VERIFY WIRING INSTRUCTIONS BY PHONE TO A NUMBER YOU '
      'ALREADY HELD, every time. ' + UPL),
    'offering_notes': {
      'summary': ('One public carrier (UWF) at 3 credits. UWF\'s description is the statewide '
                  'description reformatted, so institution and state agree on content - comparatively '
                  'rare in this catalogue.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("UWF publishes no contact hours. 45 is Florida's convention for a 3-credit "
                     'unsuffixed course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Property Law and Transactions', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "Covers contracts for the sale of land, '
                  'forms of real estate ownership, steps involved in a real estate transaction, '
                  'drafting of leases, purchases, and sales agreements, drafting of mortgages and '
                  'notes, drafting of deeds, preparing and executing a complete real estate closing '
                  'and preparing a title search and real estate abstract." Department of Criminal '
                  'Justice, Col of Arts, Soc Sci and Human.')},
      ],
    },
  },

  'PLA3806': {
    'title': 'Family Law',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'Neither carrier publishes one. The STATEWIDE record names PLA 1003 - but FGCU carries that '
      'number and UWF DOES NOT, so take your own institution\'s gate, not the state\'s. '
      '*** FLORIDA FAMILY LAW WAS SUBSTANTIALLY REWRITTEN IN 2023: permanent alimony was eliminated '
      'and a rebuttable presumption of equal time-sharing was added. ANY TEXT OR SUMMARY OLDER THAN '
      'MID-2023 IS UNRELIABLE on the two issues that matter most - go to the current text of Fla. '
      'Stat. ch. 61. *** USE FLORIDA\'S VOCABULARY: the state record still says "custody, visitation" '
      'but Florida law says PARENTAL RESPONSIBILITY, TIME-SHARING and PARENTING PLAN. *** SUPPORT: '
      'Florida Domestic Violence Hotline 1-800-500-1119; Florida Abuse Hotline 1-800-96-ABUSE; 988. '
      + UPL),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits, neither publishing contact hours or a '
                  'prerequisite. FGCU\'s catalogue was unreachable when this guide was written - '
                  'its course-information service returned empty responses on every prefix tested, '
                  'including ones it certainly carries, so this is a service-wide condition rather '
                  'than evidence about the course.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Neither carrier publishes contact hours. 45 is Florida's convention for a "
                     '3-credit unsuffixed course.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Family Law', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "Examine the components of family law, '
                  'including marriage, divorce, child support, property division, and annulment. The '
                  'topics of adoption, paternity, child abuse/neglect, and termination of parental '
                  'rights will also be introduced." Department of Criminal Justice, Col of Arts, Soc '
                  'Sci and Human. NOTE UWF does NOT carry PLA1003, which the statewide record names '
                  'as this course\'s prerequisite.')},
        {'institution': 'FGCU', 'institution_name': FGCU,
         'title': 'Family Law Issues', 'credits': 3, 'contact_hours': None,
         'note': ('Carried at 3 credits. FGCU\'s catalogue was unreachable when this guide was '
                  'written, so its description could not be read and its title is the only evidence '
                  'of emphasis. FGCU DOES carry PLA1003, so the statewide prerequisite is meaningful '
                  'there even though it is not at UWF.')},
      ],
    },
  },

  'PLA4191': {
    'title': 'Legal Reasoning',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF: none published. UCF: PLA 3014 (Law and the Legal System) or equivalent, and OFFERED FALL '
      'ONLY - the prerequisite and the once-a-year schedule compound, so put it on a degree plan '
      'early. '
      '*** THE TWO CARRIERS TEACH DIFFERENT COURSES. UWF places "special emphasis on questions '
      'students might face on the LAW SCHOOL ADMISSION TEST". UCF teaches reasoning methods '
      '"applicable to legal AND NON-LEGAL problems". Pick deliberately: LSAT preparation versus a '
      'transferable habit of mind. SYLLABUS TEST - look for timed LSAT sections. *** IF YOU ARE '
      'TAKING IT FOR THE LSAT: check the CURRENT test format with LSAC directly, since the format '
      'has been revised and preparation material dates fast; use official released questions; and '
      'start months earlier than feels necessary. *** TAKE IT EARLY - everything else in the degree '
      'gets easier once you can read a case properly.'),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits under different titles and with genuinely different '
                  'emphases. UCF publishes 0 lab hours. Unlike most of this prefix there is NO '
                  'lower-division twin, so no risk of repeating A.S. content.'),
      'hours_source': 'mixed',
      'derived_contact_hours': 45,
      'derivation': ('Neither carrier publishes a total contact-hour figure, but UCF publishes 0 '
                     'weekly lab/studio hours. 45 is the convention for a 3-credit unsuffixed course '
                     'and agrees with that.'),
      'offerings': [
        {'institution': 'UCF', 'institution_name': UCF,
         'title': 'Thinking Like a Lawyer', 'credits': 3, 'contact_hours': None,
         'note': ('"Course designed for students interested in applying legal reasoning, with '
                  'distinctive techniques and decision-making methods characteristic of legal '
                  'decision-making applicable to legal and non-legal problems." Prerequisite PLA 3014 '
                  'or equivalent. FALL ONLY. 0 lab hours. DEPARTMENT OF LEGAL STUDIES, College of '
                  'Community Innovation and Education - UCF runs a large upper-division legal studies '
                  'catalogue including moot court, a law journal and legal scholarship, a '
                  'recognisable law-school pipeline.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Legal Reasoning', 'credits': 3, 'contact_hours': None,
         'note': ('3 sh, may not be repeated for credit. "This course will explore the logical skills '
                  'necessary to critically think through legal problems. SPECIAL EMPHASIS WILL BE '
                  'PLACED ON QUESTIONS STUDENTS MIGHT FACE ON THE LAW SCHOOL ADMISSION TEST." '
                  'Department of Criminal Justice, Col of Arts, Soc Sci and Human.')},
      ],
    },
  },

  'PLA4554': {
    'title': 'Environmental Law',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UCF: ENC 1102 (freshman composition II), and OFFERED FALL ONLY. '
      '*** THE STATEWIDE PREREQUISITE DOES NOT EXIST AT UCF. Florida names "PLA 1003 AND PLA 2203" - '
      'both lower-division numbers carried almost entirely by STATE COLLEGES, and UCF carries '
      'NEITHER. St. Petersburg College carries both. Take your own institution\'s gate. *** FLORIDA '
      'IS THE REASON TO TAKE THIS HERE: five regional WATER MANAGEMENT DISTRICTS (Fla. Stat. ch. '
      '373) that have almost no equivalent elsewhere, the ENVIRONMENTAL RESOURCE PERMIT, ch. 403, a '
      'constitutional conservation policy (Art. II, s.7) and Everglades restoration. *** CHECK '
      'CURRENCY BEFORE RELYING ON ANYTHING: the division of wetlands permitting authority between '
      'Florida and the federal government has been litigated and has changed - confirm with DEP and '
      'the Corps. ' + UPL),
    'offering_notes': {
      'summary': ('Two carriers at 3 credits - one SUS and one FCS. St. Petersburg College carries '
                  'this 4000-level number under its baccalaureate authority, which is why "state '
                  'college means lower division" is a tendency rather than a rule. No lower-division '
                  'twin exists for this subject.'),
      'hours_source': 'mixed',
      'derived_contact_hours': 45,
      'derivation': ('UCF publishes 0 weekly lab/studio hours but no total. 45 is the convention for '
                     'a 3-credit unsuffixed course and agrees with it.'),
      'offerings': [
        {'institution': 'UCF', 'institution_name': UCF,
         'title': 'Environmental Law', 'credits': 3, 'contact_hours': None,
         'note': ('"Environmental law and policy related to the protection of natural resources, '
                  'including an examination of toxic pollutants, endangered species, and climate '
                  'change." Prerequisite ENC 1102. FALL ONLY. 0 lab hours. Department of Legal '
                  'Studies, College of Community Innovation and Education.')},
        {'institution': 'SPC', 'institution_name': SPC,
         'title': 'Environmental Law', 'credits': 3, 'contact_hours': None,
         'note': ('Carried at 3 credits. SPC\'s own course description could not be read for this '
                  'guide. NOTE SPC carries both PLA1003 and PLA2203, so the statewide prerequisite '
                  'chain is meaningful at SPC even though it is meaningless at UCF.')},
      ],
    },
  },

  'PLA4764': {
    'title': 'Law Office Management',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UCF: ENC 1102, and OFFERED FALL ONLY. UWF publishes no prerequisite; its catalogue entry for '
      'this number could not be retrieved, so UWF students should confirm with the department. '
      '*** TAKE THIS EARLY. It is what makes an internship productive. *** TWO TOPICS CARRY REAL '
      'CONSEQUENCES. (1) CALENDARING AND DOCKET CONTROL: missed deadlines are among the largest '
      'causes of legal malpractice claims, and the docket is often a paralegal\'s responsibility. '
      '(2) CLIENT TRUST ACCOUNTING under Florida Bar Chapter 5 and IOTA: trust violations are a '
      'leading route to discipline and disbarment in Florida, and many are bookkeeping failures '
      'rather than dishonesty. Rule 4-5.3 makes the SUPERVISING LAWYER responsible for your conduct. '
      '*** The FCS twin PLA2763 is carried by 10 state colleges. ' + UPL),
    'offering_notes': {
      'summary': ('Two SUS carriers at 3 credits. UCF publishes 0 lab hours and names interviewing '
                  'technique explicitly. The lower-division twin PLA2763 is carried by 10 Florida '
                  'College System institutions - twelve institutions, two numbers, zero crossover.'),
      'hours_source': 'mixed',
      'derived_contact_hours': 45,
      'derivation': ('UCF publishes 0 weekly lab/studio hours but no total. 45 is the convention for '
                     'a 3-credit unsuffixed course.'),
      'offerings': [
        {'institution': 'UCF', 'institution_name': UCF,
         'title': 'Law Office Practices', 'credits': 3, 'contact_hours': None,
         'note': ('"Organization, operation and management of law office. INTERVIEWING TECHNIQUES '
                  'and practical application of work that is done in a law office." Prerequisite ENC '
                  '1102. FALL ONLY. 0 lab hours. Department of Legal Studies, College of Community '
                  'Innovation and Education.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Law Office Management', 'credits': 3, 'contact_hours': None,
         'note': ('Recorded by Florida\'s course file at 3 credits under the statewide title. '
                  'UWF\'s own catalogue entry for this number could not be retrieved from either the '
                  'published prefix listing or the catalogue search when this guide was written, so '
                  'its description and any prerequisite are unconfirmed. Confirm with the Department '
                  'of Criminal Justice.')},
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
    print('shared block: UPL=%d chars' % len(UPL))
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
