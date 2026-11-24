# -*- coding: utf-8 -*-
"""Guide requests that need a decision: put on hold with a reason, then declined (or written) by Ron.

Run from Tools/ (decide-requests.cmd in the repo root runs `decide` for you).

    python guide_requests.py decide                 # Ron: go through the held requests, one key each
    python guide_requests.py list [--status held]   # open | held | queued | published | declined | all
    python guide_requests.py hold EEL5025 "reason"  # a real question for Ron only: thin or one-school courses get a limited-information guide (CLAUDE.md, 2026-11-24)
    python guide_requests.py decline EEL5025        # decline with the reason it was held with
    python guide_requests.py decline EEL5025 --reason "new public reason"
    python guide_requests.py release EEL5025        # back to the queue (to be written), or undo a decline

A HOLD's reason is written for the public: it is what the visitor sees in the queue and on the course page
if the request is declined. Write it as one to three plain sentences about the course (what is missing),
never about the visitor. A declined course can be requested again; the new request asks "what has changed?",
and that text shows here under "Requesters wrote".
"""
import argparse
import os
import sys
import textwrap

import requests

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))
except ImportError:
    pass

BASE = os.environ.get('REPO_BASE_URL', 'https://floridacourserepo.com').rstrip('/')
WRAP = textwrap.TextWrapper(width=96, initial_indent='      ', subsequent_indent='      ')


class Site:
    def __init__(self):
        email, password = os.environ.get('REPO_ADMIN_EMAIL'), os.environ.get('REPO_ADMIN_PASSWORD')
        if not email or not password:
            sys.exit('Tools/.env needs REPO_ADMIN_EMAIL and REPO_ADMIN_PASSWORD.')
        self.s = requests.Session()
        r = self.s.post(BASE + '/api/v1/auth/login', json={'email': email, 'password': password}, timeout=30)
        if r.status_code != 200:
            sys.exit('Could not sign in to %s (HTTP %d).' % (BASE, r.status_code))
        self.s.headers['Authorization'] = 'Bearer ' + r.json()['data']['accessToken']

    def list(self, status):
        r = self.s.get(BASE + '/api/v1/guide-requests', params={'status': status}, timeout=30)
        if r.status_code == 400 and status == 'held':
            sys.exit('The site does not know "held" yet: it needs the deploy with plan Phase 12.')
        r.raise_for_status()
        return r.json()['data']

    def set(self, course, status, notes=None):
        body = {'status': status}
        if notes:
            body['notes'] = notes
        r = self.s.patch(BASE + '/api/v1/guide-requests/%s/status' % course, json=body, timeout=30)
        if r.status_code != 200:
            err = (r.json().get('error') or {}) if r.headers.get('content-type', '').startswith('application/json') else {}
            fields = '; '.join(f.get('message', '') for f in (err.get('fields') or err.get('details') or []) if isinstance(f, dict))
            raise RuntimeError('%s: HTTP %d %s %s' % (course, r.status_code, err.get('message', r.text[:200]), fields))
        return r.json()['data']['message']


def show(i, n=None):
    head = '%s%s  %s' % ('%d. ' % n if n else '', i['courseId'], i['courseTitle'])
    print('  ' + head + '   (%d request%s)' % (i['requestCount'], '' if i['requestCount'] == 1 else 's'))
    if i.get('adminNotes'):
        print('    Reason (shown publicly if declined):')
        print(WRAP.fill(i['adminNotes']))
    for note in i.get('requesterNotes') or []:
        print('    Requester wrote:')
        print(WRAP.fill('"%s"' % note))


def cmd_list(site, a):
    items = site.list(a.status)
    print('%d course(s) %s' % (len(items), a.status))
    for n, i in enumerate(items, 1):
        show(i, n)


def cmd_hold(site, a):
    reason = ' '.join(a.reason).strip()
    if len(reason) < 20:
        sys.exit('Give the public reason in a full sentence (20+ characters).')
    print(site.set(a.course.upper(), 'Held', reason))


def cmd_decline(site, a):
    course = a.course.upper()
    reason = (a.reason or '').strip() or None
    if reason is None:
        held = {i['courseId']: i for i in site.list('held')}
        if course not in held or not held[course].get('adminNotes'):
            sys.exit('%s is not on hold with a reason: give one with --reason "...".' % course)
    print(site.set(course, 'Declined', reason))


def cmd_release(site, a):
    print(site.set(a.course.upper(), 'Open', 'Released from hold by the site editor: write the guide.'))


def ask(prompt, allowed):
    while True:
        try:
            k = input(prompt).strip().lower()
        except EOFError:
            return ''
        if k in allowed:
            return k
        print('    Type one of: %s' % ', '.join(x or 'Enter' for x in allowed))


def cmd_decide(site, a):
    items = site.list('held')
    print()
    if not items:
        print('No guide requests are on hold. Nothing to decide.')
        return
    print('%d guide request(s) are on hold for your decision:' % len(items))
    print()
    for n, i in enumerate(items, 1):
        show(i, n)
        print()
    print('  A  decline ALL of them, each with the reason shown (visitors see it and may ask again)')
    print('  O  go through them one at a time')
    print('  Enter  leave them on hold for now')
    k = ask('Your choice [A/O/Enter]: ', ['a', 'o', ''])
    if k == 'a' and ask('Decline all %d? The reasons become public. Type Y to confirm, Enter to go back: '
                        % len(items), ['y', '']) != 'y':
        k = ask('Go through them one at a time instead? [O/Enter]: ', ['o', ''])
    if k == '':
        print('Left on hold.')
        return
    done = []
    for i in items:
        c = i['courseId']
        if k == 'o':
            print()
            show(i)
            choice = ask('    D decline with this reason · E edit the reason, then decline · '
                         'W send back to be written · Enter skip: ', ['d', 'e', 'w', ''])
            if choice == '':
                continue
            if choice == 'w':
                try:
                    site.set(c, 'Open', 'Released from hold by the site editor: write the guide.')
                    done.append((c, 'sent back to be written (the next check-requests writes it)'))
                except RuntimeError as e:
                    print('    ' + str(e))
                continue
            reason = None
            if choice == 'e':
                while True:
                    reason = input('    New public reason (a full sentence, at least 20 characters; Enter to skip): ').strip()
                    if not reason or len(reason) >= 20:
                        break
                    print('    That is %d characters; it needs at least 20.' % len(reason))
                if not reason:
                    continue
        else:
            reason = None
        try:
            site.set(c, 'Declined', reason)
            done.append((c, 'declined'))
        except RuntimeError as e:
            print('    ' + str(e))
    print()
    if not done:
        print('Nothing changed.')
    for c, what in done:
        print('  %-10s %s' % (c, what))
    if any(w == 'declined' for _, w in done):
        print('\nThe reasons now show at %s/queue/guides?status=declined and on each course page.' % BASE)
        print('To undo one: python guide_requests.py release <COURSE>, or set it to Open on /admin/guide-requests.')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('decide')
    x = sub.add_parser('list'); x.add_argument('--status', default='held')
    x = sub.add_parser('hold'); x.add_argument('course'); x.add_argument('reason', nargs='+')
    x = sub.add_parser('decline'); x.add_argument('course'); x.add_argument('--reason')
    x = sub.add_parser('release'); x.add_argument('course')
    a = p.parse_args()
    site = Site()
    try:
        {'decide': cmd_decide, 'list': cmd_list, 'hold': cmd_hold, 'decline': cmd_decline,
         'release': cmd_release}[a.cmd](site, a)
    except RuntimeError as e:
        sys.exit(str(e))


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    main()
