# -*- coding: utf-8 -*-
import json, io
p='career_paths/marketing-manager.json'
d=json.load(io.open(p,encoding='utf-8'))
old1=("⚠⚠⚠ $166,790 — the highest median of any bachelor's-entry occupation on this site, "
      "above computer hardware engineering at $161,740 and software development at $135,980 — and 80% of "
      "employers report a bachelor's rather than a master's.")
new1=("⚠⚠⚠ $166,790, among the highest medians of any bachelor's-entry occupation on this site "
      "— beside computer and information systems management at $175,140 and computer hardware "
      "engineering at $161,740 — and 80% of employers report a bachelor's rather than a master's.")
assert old1 in d['description']
d['description']=d['description'].replace(old1,new1)
b=d['bodyHtml']
old2=("&#9888;&#9888;&#9888; <strong>$166,790 is the highest median of any bachelor's-entry occupation on this "
      "site</strong> &mdash; above computer hardware engineering at $161,740 and software development at "
      "$135,980 &mdash; <strong>and it is reached with a bachelor's and experience rather than a further "
      "degree.</strong>")
new2=("&#9888;&#9888;&#9888; <strong>$166,790 is among the highest medians of any bachelor's-entry occupation "
      "on this site</strong> &mdash; beside computer and information systems management at $175,140 and "
      "computer hardware engineering at $161,740 &mdash; <strong>and it is reached with a bachelor's and "
      "experience rather than a further degree.</strong>")
assert old2 in b, 'body phrase not found'
d['bodyHtml']=b.replace(old2,new2)
io.open(p,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('ok')
