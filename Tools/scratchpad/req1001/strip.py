import re,html,sys
t=open(sys.argv[1],encoding='utf-8',errors='replace').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
for k in sys.argv[3:]:
    for m in list(re.finditer(re.escape(k),t))[:int(sys.argv[2])]:
        print('>>',t[max(0,m.start()-300):m.start()+700]); print()
