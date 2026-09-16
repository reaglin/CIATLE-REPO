"""Restructure JOU4306 so the canonical sections exist.

The two-subject layout put outcomes and topics under per-reading <h2>
headings, so the guide had no top-level "Learning Outcomes" or "Major
Topics" section and validate_drafts.py warned correctly.

Fix: move each reading's descriptive prose into Course Description as an
<h3>, then group the two outcome lists under one <h2>Learning Outcomes</h2>
and the two topic lists under one <h2>Major Topics</h2>, keeping the
Reading A / Reading B labels on every list.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'html', 'JOU4306.html')
s = io.open(P, encoding='utf-8').read()

A_HEAD = '<h2>Reading A — Writing Critical Reviews (UWF)</h2>'
B_HEAD = '<h2>Reading B — Advanced Data Journalism (UF)</h2>'
A_OUT = '<h3>Required Outcomes (Reading A)</h3>'
A_TOP = '<h3>Required Topics (Reading A)</h3>'
B_OUT = '<h3>Required Outcomes (Reading B)</h3>'
B_TOP = '<h3>Required Topics (Reading B)</h3>'
RES = '<h2>Resources &amp; Tools</h2>'

for m in (A_HEAD, B_HEAD, A_OUT, A_TOP, B_OUT, B_TOP, RES):
    assert m in s, 'missing marker: ' + m[:50]

head, rest = s.split(A_HEAD, 1)              # head = Course Description
a_prose, rest = rest.split(A_OUT, 1)
a_out, rest = rest.split(A_TOP, 1)
a_top, rest = rest.split(B_HEAD, 1)
b_prose, rest = rest.split(B_OUT, 1)
b_out, rest = rest.split(B_TOP, 1)
b_top, tail = rest.split(RES, 1)
tail = RES + tail                            # Resources onward, unchanged

out = (
    head.rstrip() + '\n\n'
    + '<h3>Reading A — Writing Critical Reviews (UWF)</h3>\n'
    + a_prose.strip() + '\n\n'
    + '<h3>Reading B — Advanced Data Journalism (UF)</h3>\n'
    + b_prose.strip() + '\n\n'
    + '<h2>Learning Outcomes</h2>\n\n'
    + '<h3>Required Outcomes — Reading A (criticism)</h3>\n'
    + a_out.strip() + '\n\n'
    + '<h3>Required Outcomes — Reading B (data journalism)</h3>\n'
    + b_out.strip() + '\n\n'
    + '<h2>Major Topics</h2>\n\n'
    + '<h3>Required Topics — Reading A (criticism)</h3>\n'
    + a_top.strip() + '\n\n'
    + '<h3>Required Topics — Reading B (data journalism)</h3>\n'
    + b_top.strip() + '\n\n'
    + tail
)

io.open(P, 'w', encoding='utf-8').write(out)
print('restructured JOU4306.html')
for name in ('Course Description', 'Learning Outcomes', 'Major Topics',
             'Resources &amp; Tools', 'Career Pathways', 'Special Information',
             'AI Integration'):
    print('  <h2>%-22s %s' % (name + '</h2>', 'OK' if '<h2>' + name + '</h2>' in out else 'MISSING'))
