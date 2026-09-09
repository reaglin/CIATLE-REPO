#!/usr/bin/env python3
"""Florida SCNS public site (flscns.fldoe.org) -- the STATEWIDE course catalog.

This is the authoritative state source the project previously lacked. It answers both
"what does the STATE say this course is" and "which institutions actually offer this
exact course id", where `courses_2plus_institutions.csv` only guesses at the second.

*** THREE THINGS THAT ARE EASY TO GET WRONG ***

 1. Routes are EXTENSIONLESS. The site's own HTML prints `PbCourseDescriptions.aspx`,
    but every `.aspx` URL 301s to /Default. Use `/PbCourseDescriptions`.
 2. You must ACCEPT THE TERMS MODAL first (POST ctl00$btnModalYes=Accept) in the same
    cookie session, or every report returns 0 records -- with no error message.
 3. The report is an SSRS ReportViewer that loads ASYNC, so the first GET carries no
    data. Re-GET the report route to pick up ReportSession + ControlID, then pull the
    CSV from Reserved.ReportViewerWebControl.axd.

USAGE
    python scns.py flatfile [outpath]      # whole SCNS DB, ~80 MB fixed-width crslist.txt
    python scns.py statewide EEE [out]     # statewide descriptions for a prefix -> CSV
    python scns.py institution EEE 9 [out] # one institution's catalog text -> CSV

The flat file is the fastest way to answer "who offers this, and what do THEY call it";
the statewide CSV carries the description, prerequisites and transferability.
Record layout in FIELDS below, derived from Downloads/File_Format_for_SCNS_Flat_File.doc.
"""
import re
import sys
import urllib.request
import urllib.parse
import http.cookiejar

BASE = 'https://flscns.fldoe.org/'
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')


def opener():
    cj = http.cookiejar.CookieJar()
    o = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    o.addheaders = [('User-Agent', UA)]
    return o


def _hidden(html):
    f = {}
    for n in ('__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION'):
        m = re.search(r'name="%s"[^>]*value="([^"]*)"' % n, html)
        if m:
            f[n] = m.group(1)
    return f


def _get(o, page):
    return o.open(BASE + page, timeout=120).read().decode('utf-8', 'replace')


def _post(o, page, fields, raw=False):
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(BASE + page, data=data, headers={
        'User-Agent': UA,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': BASE + page})
    r = o.open(req, timeout=600)
    return r if raw else r.read().decode('utf-8', 'replace')


def session(page='PbCourseInventory'):
    """Open a session and accept the terms modal.

    Without the Accept the reports silently return 0 rows, which looks like a block
    but is not one.
    """
    o = opener()
    f = _hidden(_get(o, page))
    f['ctl00$btnModalYes'] = 'Accept'
    _post(o, page, f)
    return o


def flatfile(out):
    """Download crslist.txt -- every course at every Florida institution (~80 MB)."""
    o = session('PbCourseInventory')
    f = _hidden(_get(o, 'PbCourseInventory'))
    f.update({'__EVENTTARGET': 'ctl00$hl_download', '__EVENTARGUMENT': ''})
    data = _post(o, 'PbCourseInventory', f, raw=True).read()
    with open(out, 'wb') as fh:
        fh.write(data)
    return len(data)


def report_csv(prefix, kind='StatewideCourse', institution='', out=None):
    """Pull a course-description report as CSV.

    kind='StatewideCourse'    -> the state's definition: description, prereqs, transferability
    kind='CourseDescriptions' -> that school's own catalog text (needs institution=<numeric id>)

    NOTE the Type values are exactly these two strings, taken from the window.open() call the
    site emits on Run Report. 'InstitutionCourse' is NOT a valid Type and yields no report.
    """
    page = 'PbStateCourseDetailReport' if kind == 'StatewideCourse' else 'PbCourseDescriptions'
    o = session(page)
    if kind != 'StatewideCourse':
        # The institution report only arms after Run Report is posted with the dropdowns set;
        # the statewide report arms from the GET alone.
        f = _hidden(_get(o, page))
        f.update({'__EVENTTARGET': 'ctl00$ContentPlaceHolder1$btnRunReport',
                  '__EVENTARGUMENT': '',
                  'ctl00$ContentPlaceHolder1$ddlInstitution': str(institution),
                  'ctl00$ContentPlaceHolder1$ddlDiscipline': '',
                  'ctl00$ContentPlaceHolder1$ddlPrefixes': prefix})
        _post(o, page, f)
    url = ('Reports/CourseDescriptionReport?instituion=%s&dis=&prefix=%s'
           '&discontinued=0&Type=%s' % (institution, prefix, kind))
    html = _get(o, url)          # this GET arms the viewer and mints the session
    m1 = re.search(r'ReportSession["\']?\s*[:=]\s*["\']?([A-Za-z0-9]+)', html)
    m2 = re.search(r'ControlID["\']?\s*[:=]\s*["\']?([A-Za-z0-9]+)', html)
    if not (m1 and m2):
        raise SystemExit('no ReportSession/ControlID -- did the modal Accept succeed?')
    ex = ('Reserved.ReportViewerWebControl.axd?ReportSession=%s&Culture=1033'
          '&CultureOverrides=False&UICulture=1033&UICultureOverrides=False'
          '&ReportStack=1&ControlID=%s&OpType=Export&FileName=%s'
          '&ContentDisposition=AlwaysAttachment&Format=CSV'
          % (m1.group(1), m2.group(1), prefix))
    data = o.open(BASE + ex, timeout=600).read()
    if out:
        with open(out, 'wb') as fh:
            fh.write(data)
    return data


# --- flat-file record layout (fixed width, 411 chars) ------------------------------
FIELDS = {
    'institution': (0, 7), 'discipline': (7, 10), 'prefix': (10, 13),
    'level': (13, 14), 'century': (14, 15), 'decade': (15, 16), 'unit': (16, 17),
    'lab': (17, 18), 'id_course': (18, 25), 'honors': (25, 26), 'status': (26, 29),
    'inst_title': (29, 179),        # what THIS institution calls it
    'credit': (179, 186), 'clock_hours': (186, 192), 'credit_type': (192, 194),
    'dt_effective': (194, 202), 'dt_discontinued': (202, 210),
    'dt_created': (210, 218), 'dt_changed': (218, 226),
    'gordon_rule': (226, 227), 'gordon_writing': (227, 228),
    'ge_com': (228, 229), 'ge_hum': (229, 230), 'ge_math': (230, 231),
    'ge_nat_sci': (231, 232), 'ge_soc_sci': (232, 233),
    'credential': (233, 236), 'dt_credential': (236, 244), 'id_course_old': (244, 251),
    'state_title': (251, 401),      # what the STATE calls it -- the divergence test
    'common_prereq': (401, 402), 'dual_enrollment': (402, 403),
    'hs_credit': (403, 405), 'transferable': (405, 407),
}


def parse_flatfile(path, prefix=None, active_only=True):
    """Yield dicts from crslist.txt, optionally filtered to a single prefix."""
    pb = prefix.encode() if prefix else None
    with open(path, 'rb') as fh:
        for line in fh:
            if pb and line[10:13] != pb:
                continue
            s = line.decode('latin1').rstrip('\r\n')
            if len(s) < 401:
                continue
            r = {k: s[a:b].strip() for k, (a, b) in FIELDS.items()}
            if active_only and r['status'] != 'A':
                continue
            r['code'] = s[10:18].strip()
            yield r


def read_report_csv(path):
    """Read a statewide or institution report CSV into dicts, cleaning the two quirks.

    The exports are UTF-8 with a BOM, and numeric cells arrive prefixed with a
    non-breaking space (credit reads '\\xa03', not '3'), which breaks int() and any
    naive comparison. Everything is upper-case in the source; that is the data, not a bug.
    """
    import csv as _csv
    import io as _io
    raw = open(path, encoding='utf-8-sig', errors='replace').read()
    out = []
    for row in _csv.DictReader(_io.StringIO(raw)):
        out.append({k: (v or '').replace('\xa0', ' ').replace('�', ' ').strip()
                    for k, v in row.items()})
    return out


def institution_map(o=None):
    """id -> 'CODE - NAME', scraped from the institution dropdown."""
    o = o or opener()
    h = _get(o, 'PbCourseInventory')
    m = re.search(r'<select[^>]*id="ContentPlaceHolder1_ddlInstitution"[^>]*>.*?</select>',
                  h, re.S)
    if not m:
        return {}
    return {v: t.strip()
            for v, t in re.findall(r'<option[^>]*value="([^"]*)"[^>]*>([^<]*)', m.group(0))
            if v}


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(2)
    cmd = sys.argv[1]
    if cmd == 'flatfile':
        out = sys.argv[2] if len(sys.argv) > 2 else 'crslist.txt'
        print('wrote', flatfile(out), 'bytes to', out)
    elif cmd == 'statewide':
        pre = sys.argv[2].upper()
        out = sys.argv[3] if len(sys.argv) > 3 else 'scns_%s_statewide.csv' % pre
        report_csv(pre, 'StatewideCourse', out=out)
        print('wrote', out)
    elif cmd == 'institution':
        pre, inst = sys.argv[2].upper(), sys.argv[3]
        out = sys.argv[4] if len(sys.argv) > 4 else 'scns_%s_%s.csv' % (pre, inst)
        report_csv(pre, 'CourseDescriptions', institution=inst, out=out)
        print('wrote', out)
    else:
        print(__doc__)
        raise SystemExit(2)
