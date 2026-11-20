import sys, time
sys.path.insert(0, '.')
import scns
scns.report_csv('ETM', out='req1001/sw_ETM.csv')
for r in scns.read_report_csv('req1001/sw_ETM.csv'):
    if r['ID_Century'] in ('310','315','317','316','311','312','314'):
        print('=== ETM',r['ID_Century'],r['IN_Lab'],r['DS_Title'],'|',r['DS_Course_Intent1']); print(r['Course']); print('PREREQ:',r['DS_Prerequisites1'],'| COREQ:',r['DS_Corequisites1']); print()
for i in [int(x) for x in sys.argv[1:]]:
    out='req1001/i_ETM_%s.csv'%i
    try:
        scns.report_csv('ETM',kind='CourseDescriptions',institution=i,out=out); rows=scns.read_report_csv(out)
    except Exception as e:
        print('ERR',i,e); continue
    for r in rows:
        n=r['CourseNumber'].replace(' ','')
        if n[3:6] in ('231','331'):
            print('##',r['Inst_Abbr'],r['CourseNumber'],r['DS_Title'],r['DS_Course_Credit'])
            print('CAT:',r['DS_Catalog'][:900]); print('LO:',r['DS_Learning_Outcome'][:1000]); print('TXT:',r['DS_Textbooks1'][:200]); print()
    time.sleep(1)
