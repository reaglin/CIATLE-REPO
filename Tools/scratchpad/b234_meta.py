"""Batch 234 metadata -- GEO (geography), the three queued rows.

Contact hours: GEO4251 and GEO4357 3 cr / 45 (no suffix, 1:15); GEO4280C
3 cr / 60 (C suffix, the queued identifier). No carrier publishes hours anywhere
in the GEO prefix.

*** HEADLINE: A CORRECTION TO MY OWN BATCH-222 RULE, AND A BETTER HANDLING ***

GEO4251's statewide description says "OFFERED CONCURRENTLY WITH GEO 5XX3" --
the identical shape as PHC4109's "PHC 5XX3" from batch 232, two batches and one
prefix apart. That prompted a scan of ALL 41 statewide CSVs on disk for wildcard
tokens: 220 found.

⚠⚠⚠ THE SCAN CORRECTS WHAT I RECORDED IN BATCH 222. I wrote that "COM 2XXX" was
"a wildcard nobody filled in -- state the intent, say the number does not
exist." That handling is too weak, and the discriminator is visible once you
read the tokens IN CONTEXT:

  GENUINE LEVEL NOTATION -- the word ANY is present, or a prefix list follows:
     CCJ?453  "ANY 1XXX OR 2XXX COURSE WITH PREFIX CCJ, CJC, CJE, CJL, CJJ, PLA"
     -> means any course at that level. Decode and explain (batch-214 rule).

  PLACEHOLDER -- the masked number is FOLLOWED BY THE COURSE'S ACTUAL TITLE:
     HFT?358  "PR: HFT 3XXX GOLF PLANNING & OPERATIONS II"
     HFT?377  "PR: HFT 3XXX (FOUNDATIONS OF PRODUCTION MANAGEMENT)"
     ATR?631  "ATR 7XXX DAT APPLIED RESEARCH I"
     BCN?441  "BCN 3XXX INTRODUCTION TO THE CONCRETE INDUSTRY"
     GEO?251  "GEO 5XX3 (ADVANCED CLIMATOLOGY AND CLIMATE CHANGE)"
     PHC?109  "PHC 5XX3 (SCIENTIFIC BASIS OF PUBLIC HEALTH)"

⚠⚠⚠ IN EVERY PLACEHOLDER CASE THE WRITER KNEW WHICH COURSE THEY MEANT AND NAMED
IT. So the title RECOVERS the number. Tested on four:
     GEO 5XX3 (Advanced Climatology and Climate Change) -> GEO?256, GRADUATE ✅
     PHC 5XX3 (Scientific Basis of Public Health)       -> PHC?123, GRADUATE ✅
     BCN 3XXX (Introduction to the Concrete Industry)   -> BCN?443 ✅
     HFT 3XXX (Golf Planning & Operations II)           -> not found ✗
Three of four recovered by searching statewide TITLES in the same prefix.

⚠⚠ AND UWF'S CATALOGUE CONFIRMED IT INDEPENDENTLY: its GEO4251 entry reads
"Offered concurrently with GEO 5256 Advanced Climatology and Climate Change" --
the exact number the title search predicted. So the SECOND recovery route is
even easier: THE CARRIER'S OWN CATALOGUE USUALLY PUBLISHES THE NUMBER THE STATE
MASKED.

⚠ CONSEQUENCE FOR A LIVE GUIDE: PHC4109 (batch 232) tells the reader "PHC 5XX3
is not a real course number... there is nothing to go and look up." That is now
known to be wrong -- PHC?123 exists. Raised as REVIEW_QUEUE item 105 with the
exact correction, since republishing a live guide needs Ron's go-ahead.

*** SECOND: GEO4280C -- THREE carriers taking THREE different halves ***

The statewide description is a six-item list spanning both hydrology (items 1,
5, 6: water/soil-rock interrelationships, precipitation-infiltration-runoff-
evaporation, analytical techniques) and water resources (items 2, 3, 4:
distribution, quality, groundwater development). The carriers split it:

  FAU  GEO4280C "Water Resources"            -> the MANAGEMENT half
  UWF  GEO4280  "Basic Hydrology"            -> the SCIENCE half
  FSU  GEO4280  "Geography of Water Resources" -> BOTH halves

⚠ None is misfiled; the statewide description licenses all three. But a student
gets a genuinely different course depending on where they take it, and neither
half is a subset of the other.

⚠⚠ PLUS the number is filed three ways AND at two levels:
  GEO4280C  FAU (3)
  GEO4280   FSU (3), UWF (3)       -- batch-219 institutional signature
  GEO3280   UF (4!), USF (3)       -- LEVEL divergence, and a credit divergence
Five institutions, three numbers, two levels, one suffix, for one subject.

⚠ AND THE C SUFFIX DOES NOT MARK THE LAB: UWF's UNSUFFIXED GEO4280 states a
"material and supply fee will be assessed for corresponding lab", and the
statewide record marks the number IN_Lab=Y regardless of suffix. So the suffix
here is pure filing, not a content signal.

*** THIRD: GEO4357 -- two intellectual traditions on one number ***
  FSU  "Environmental Conflict and Economic Development" -- statewide text
       VERBATIM (so FSU is the contributor), "controversies over the use,
       transformation, and destruction of nature, including POLITICAL ECOLOGY"
  UWF  "Environment and Economy" -- reconciling environment and economy,
       "environmental action that is economically feasible", and ⚠ HOW
       ENVIRONMENTAL PROJECTS ARE FUNDED IN THE US AND HOW TO GAIN FUNDING
⚠⚠ UWF's description never uses conflict, controversy, destruction or political
ecology. FSU's frame is the FIGHTS; UWF's is RECONCILIATION plus grant-writing.
Different traditions (critical human geography vs environmental economics) and
different destinations. Two-column test given, plus the departmental signal:
UWF places it in Earth & Environmental Sciences, not Geography or Economics.

*** ALSO WORTH RECORDING ***
⚠ FLAT-FILE TITLE vs CATALOGUE TITLE DISAGREE on GEO4251/FSU. The flat file's
inst_title reads "CLIMATE CHAOS: THE SCIENCE BEHIND THE ST..."; FSU's own
catalogue says "Geography of Climate Change and Storms". A cousin of the
batch-222/226 inventory-title problem, but WITHIN a public carrier's own record.
The guide names both so a searching student finds it either way.
⚠ Statewide TITLE TYPO: "ADVANCED CLLIMATOLOGY" (doubled L). Harmless except it
defeats a catalogue search; guide says search on "climat".
⚠ GEO4251 statewide prerequisite is EMPTY; UWF requires GEO 4250 Climatology --
which is what "advanced" means. Stated.
⚠ GEO4251 and GEO4357 are BOTH dual-listed at UWF (GEO 5256, GEO 5358), so both
guides carry the repeat-restriction warning.

*** DISTRIBUTION TEST *** hs_credit, transferable and dual_enrollment all
385/385 uniform -- pure boilerplate, nothing claimed.

Prefix: 287 live ids, 229 single-carrier (80%), max 7 carriers.
Sources: UWF PDF (GEO4251, GEO4357 and the bare GEO4280), FAU Coursedog, FSU
bulletin, statewide CSV. ⚠ FGCU re-probed at session start: still empty 202.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'meta.json')

UWF = 'University of West Florida'
FSU = 'Florida State University'
FAU = 'Florida Atlantic University'

# Shared block -- the dual-listing warning, true of GEO4251 and GEO4357.
DUAL = ('*** DUAL-LISTED AT UWF: the pace sits above a typical undergraduate course, but TAKING IT '
        'MAY PREVENT YOU TAKING THE GRADUATE VERSION FOR CREDIT LATER. Ask before registering. ')


NEW = {

  'GEO4251': {
    'title': 'Advanced Climatology and Climate Change',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF: GEO 4250 (Climatology) - which is what "advanced" in the title means, so this is the SECOND '
      'climatology course, not an entry point. FSU: none listed. The statewide prerequisite field is '
      'EMPTY, so check your own catalogue. ' + DUAL +
      '*** THE CARRIERS EMPHASISE DIFFERENT HALVES: UWF carries the statewide text verbatim - '
      'paleoclimate and the pre-1895 record. FSU titles it '
      '"Geography of Climate Change and STORMS" and emphasises extreme weather and '
      'attribution. Read the syllabus. '
      '*** TWO STATE-RECORD DEFECTS: the statewide title is misspelled "CLLIMATOLOGY", so search on '
      '"climat"; and the graduate partner is recorded as "GEO 5XX3", which is not a real number - '
      'UWF\'s catalogue gives it as GEO 5256.'),
    'offering_notes': {
      'summary': ('Two public carriers at 3 credits with different emphases - the long paleoclimate '
                  'record against extreme weather. No institution publishes contact hours anywhere in '
                  'the GEO prefix.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': ("Florida's 1:15 convention on 3 credits; both carriers list 3. The statewide "
                     'record marks the number as carrying a laboratory component - ask whether your '
                     'section has one.'),
      'offerings': [
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Advanced Climatology and Climate Change', 'credits': 3, 'contact_hours': None,
         'note': ('College of Science and Engineering, Department of Earth and Environmental Sciences. '
                  'Description is the STATEWIDE TEXT VERBATIM, so UWF is almost certainly the '
                  'contributor and the state record repeats it rather than corroborating it. '
                  'Prerequisite GEO 4250. Offered concurrently with GEO 5256 - which is the number the '
                  'statewide description masks as "GEO 5XX3".')},
        {'institution': 'FSU', 'institution_name': FSU,
         'title': 'Geography of Climate Change and Storms', 'credits': 3, 'contact_hours': None,
         'note': ('"Explores the critical debate on global climatic fluctuations and extreme weather '
                  'frequency in relation to human impact and interference. Particular focus is given to '
                  'geographic variations and temporal validity." No prerequisite listed. NOTE the '
                  'state course file records a DIFFERENT FSU title - "Climate Chaos: The Science Behind '
                  'the Stories" - from the one FSU\'s own catalogue publishes. The catalogue is the '
                  'better source; both are given here so a searching student finds the course.')},
      ],
    },
  },

  'GEO4280C': {
    'title': 'Geographic Hydrology and Water Resources',
    'credits': 3, 'contact_hours': 60, 'version': '1.0',
    'prerequisites': (
      'FAU: GEO 2200C or GLY 2010C or equivalent. UWF (bare number): CHM 2046/L AND GEO 3210/L - '
      'considerably harder, reflecting its quantitative emphasis. '
      '*** THREE CARRIERS TAKE THREE DIFFERENT HALVES OF ONE SUBJECT. The statewide description spans '
      'both hydrology (the water cycle, runoff, measurement) and water resources (distribution, '
      'quality, groundwater development). FAU teaches the MANAGEMENT half - use, allocation, wetland '
      'degradation, pollution. UWF teaches the SCIENCE half - water budget, stream flow, '
      'evapotranspiration. FSU teaches BOTH. None is misfiled; the state licenses all three. '
      '*** IT RUNS ACROSS THREE NUMBERS AT TWO LEVELS: GEO4280C (FAU), GEO4280 (FSU, UWF), '
      'GEO3280 (UF at 4 CREDITS, USF at 3). Expect the number, level and credit value to change '
      'on transfer. '
      '*** THE C SUFFIX IS NOT A LAB SIGNAL - the unsuffixed form at UWF has a lab fee too. '
      '*** SAY WHICH HALF YOU DID on transfer; nobody can tell from the number.'),
    'offering_notes': {
      'summary': ('One public carrier of the C identifier (FAU); two more carry the same subject under '
                  'the unsuffixed GEO4280 and two others at 3000 level. No contact hours published.'),
      'hours_source': 'derived',
      'derived_contact_hours': 60,
      'derivation': ("Florida's convention for a 3-credit integrated C course (Ron, 2026-09-15), which "
                     'is the queued identifier. The statewide record marks the number as a laboratory '
                     'course regardless of suffix, so 60 is the right shape either way.'),
      'offerings': [
        {'institution': 'FAU', 'institution_name': FAU,
         'title': 'Water Resources', 'credits': 3, 'contact_hours': None,
         'note': ('Sole public carrier of the C identifier. "Distribution, management and use of water. '
                  'Topics include agricultural and personal water use, wetland degradation and '
                  'pollution." Prerequisite GEO 2200C or GLY 2010C or equivalent. THE MANAGEMENT HALF '
                  'of the statewide description.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Basic Hydrology', 'credits': 3, 'contact_hours': None,
         'note': ('Carries the UNSUFFIXED GEO4280. Department of Earth and Environmental Sciences. '
                  '"Hydrologic cycle with emphasis upon surface water components... precipitation, '
                  'evapotranspiration, water budget, stream flow, and underground water sources and '
                  'their measurements." THE SCIENCE HALF. Prerequisites CHM 2046/L AND GEO 3210/L. '
                  'Material and supply fee for the corresponding lab - so the bare number has lab work '
                  'too. Offered concurrently with GEO 5289.')},
        {'institution': 'FSU', 'institution_name': FSU,
         'title': 'Geography of Water Resources', 'credits': 3, 'contact_hours': None,
         'note': ('Carries the UNSUFFIXED GEO4280. "Comprehensive overview of the natural processes '
                  'associated with water occurrence and resources... how it impacts human habitation, '
                  'and its future as a critical and valuable natural resource. Development of '
                  'socio-economic concepts of management, supply." BOTH HALVES - the fullest match to '
                  'the statewide description.')},
      ],
    },
  },

  'GEO4357': {
    'title': 'Environmental Conflict and Economic Development',
    'credits': 3, 'contact_hours': 45, 'version': '1.0',
    'prerequisites': (
      'UWF: EVR 2001 OR ESC 2000 OR GLY 2010 - an introductory environmental or earth science. FSU: '
      'none listed. Statewide: none. ' + DUAL +
      '*** THE TWO CARRIERS TEACH DIFFERENT INTELLECTUAL TRADITIONS. FSU carries the statewide sentence '
      'verbatim - "controversies over the use, transformation, and destruction of nature, including '
      'POLITICAL ECOLOGY", a critical-geography field about power and who bears the cost. UWF '
      'teaches "Environment and Economy": reconciling the two, and HOW ENVIRONMENTAL PROJECTS '
      'ARE FUNDED IN THE US. It never uses conflict, controversy or political '
      'ecology. '
      '*** ONE FRAMES THE FIGHTS, THE OTHER FRAMES THE SOLUTIONS, and they prepare you for different '
      'work: advocacy and graduate human geography against consulting and the grant-funded non-profit '
      'sector. Read the syllabus and the reading list.'),
    'offering_notes': {
      'summary': ('Two public carriers at 3 credits teaching two different intellectual traditions - '
                  'political ecology and environmental economics. No contact hours published.'),
      'hours_source': 'derived',
      'derived_contact_hours': 45,
      'derivation': "Florida's 1:15 convention on 3 credits; both carriers list 3.",
      'offerings': [
        {'institution': 'FSU', 'institution_name': FSU,
         'title': 'Environmental Conflict and Economic Development', 'credits': 3,
         'contact_hours': None,
         'note': ('"Examines controversies over the use, transformation, and destruction of nature, '
                  'including political ecology." This is the STATEWIDE DESCRIPTION VERBATIM, so FSU is '
                  'almost certainly its contributor - the state record repeats FSU rather than '
                  'corroborating it. No prerequisite listed.')},
        {'institution': 'UWF', 'institution_name': UWF,
         'title': 'Environment and Economy', 'credits': 3, 'contact_hours': None,
         'note': ('College of Science and Engineering, DEPARTMENT OF EARTH AND ENVIRONMENTAL SCIENCES - '
                  'not Geography or Economics, which predicts the physical-science-adjacent framing the '
                  'description confirms. Covers the environment-economy relationship, the history of '
                  'thinking that links them, the main academic responses to the tension, and HOW '
                  'ENVIRONMENTAL PROJECTS ARE FUNDED IN THE US AND HOW TO GAIN FUNDING. Prerequisite '
                  'EVR 2001 OR ESC 2000 OR GLY 2010. Offered concurrently with GEO 5358.')},
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
