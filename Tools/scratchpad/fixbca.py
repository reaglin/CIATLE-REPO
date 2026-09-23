# -*- coding: utf-8 -*-
"""Set course-level credits to 0 on the plumbing apprenticeship courses BCA0450-0457.

The modal credit came from ONE carrier (South Florida State, which records '8' on
clock-hour apprenticeship rows); the other five carriers record clock hours and no
credit. A clock-hour course is 0 credits at course level. Offerings are left alone
(replaceOfferings false), so SFSC's own row still says what SFSC says.
"""
import os, sys, requests
from dotenv import load_dotenv
load_dotenv('.env')
B = os.environ.get('REPO_BASE_URL', 'https://floridacourserepo.com').rstrip('/')
s = requests.Session()
t = s.post(B + '/api/v1/auth/login', json={'email': os.environ['REPO_ADMIN_EMAIL'],
           'password': os.environ['REPO_ADMIN_PASSWORD']}, timeout=20).json()['data']['accessToken']
H = {'Authorization': 'Bearer ' + t}
for n, roman in zip(range(450, 458), ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']):
    cid = 'BCA0%d' % n
    cur = s.get(B + '/api/v1/courses/' + cid, timeout=20).json()['data']
    body = {'courseId': cid, 'title': cur['title'], 'creditHours': 0, 'replaceOfferings': False}
    r = s.put(B + '/api/v1/courses/' + cid, json=body, headers=H, timeout=20)
    print(cid, r.status_code, (r.json().get('data') or {}).get('creditHours', r.text[:120]))
