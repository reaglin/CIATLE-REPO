import sys, time
sys.path.insert(0, '.')
import scns
for i in [101,17,75,85,23,49,31,37,13,56,22,2]:
    out='req1001/acg_%s.csv'%i
    try:
        scns.report_csv('ACG',kind='CourseDescriptions',institution=i,out=out)
        rows=scns.read_report_csv(out)
    except Exception as e:
        print('ERR',i,e); continue
    for r in rows:
        n=r['CourseNumber'].replace(' ','')
        if n[4:7] in ('021','022'):
            print('##',r['Inst_Abbr'],r['CourseNumber'],r['DS_Title'],r['DS_Course_Credit'])
            print('CAT:',r['DS_Catalog'][:900]); print('LO:',r['DS_Learning_Outcome'][:900]); print('TXT:',r['DS_Textbooks1'][:250]); print()
    time.sleep(1)
