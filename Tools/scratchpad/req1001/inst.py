import sys, time
sys.path.insert(0, '.')
import scns
jobs=[('ACG',79,'1001'),('ACG',89,'1001'),('AOM',49,None),('AOM',69,None),('AOM',2,'2316'),('AOM',73,'2316'),('AOM',79,'2433'),('AOM',101,'3220'),('ATT',82,'3811'),('EET',110,'0052')]
for p,i,c in jobs:
    out='req1001/i_%s_%s.csv'%(p,i)
    try:
        scns.report_csv(p,kind='CourseDescriptions',institution=i,out=out)
        rows=scns.read_report_csv(out)
    except Exception as e:
        print('ERR',p,i,e); continue
    print('######',p,i,len(rows), list(rows[0].keys()) if rows else '')
    for r in rows:
        s=' | '.join(v for v in r.values())
        if c is None or c in s.replace(' ',''):
            print(s[:2500]); print()
    time.sleep(2)
