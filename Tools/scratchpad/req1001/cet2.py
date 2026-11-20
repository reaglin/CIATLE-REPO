import sys, time
sys.path.insert(0, '.')
import scns
want={'CET':['1178','2118','2123','4663','4668','4772'],'EEV':['0203']}
for p,i in [('CET',59),('CET',69),('CET',13),('CET',49),('CET',37),('CET',56),('CET',82),('EEV',119)]:
    out='req1001/i_%s_%s.csv'%(p,i)
    try:
        scns.report_csv(p,kind='CourseDescriptions',institution=i,out=out); rows=scns.read_report_csv(out)
    except Exception as e:
        print('ERR',p,i,e); continue
    for r in rows:
        n=r['CourseNumber'].replace(' ','')
        if any(n[3:].startswith(w) for w in want[p]):
            print('##',r['Inst_Abbr'],r['CourseNumber'],r['DS_Title'],r['DS_Course_Credit'])
            print('CAT:',r['DS_Catalog'][:900]); print('LO:',r['DS_Learning_Outcome'][:1100]); print('TXT:',r['DS_Textbooks1'][:200]); print()
    time.sleep(1)
