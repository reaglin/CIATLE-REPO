import sys, time
sys.path.insert(0, '.')
import scns
scns.report_csv('CET', out='req1001/sw_CET.csv'); scns.report_csv('EEV', out='req1001/sw_EEV.csv')
for p in ('CET','EEV'):
    for r in scns.read_report_csv('req1001/sw_%s.csv'%p):
        if (p=='CET' and r['ID_Century'] in ('178','118','123','772','668','663')) or (p=='EEV' and r['ID_Century']=='203'):
            print('=== ',p,r['ID_Century'],r['IN_Lab'],r['DS_Title'],'|',r['DS_Course_Intent1']); print(r['Course']); print('PREREQ:',r['DS_Prerequisites1'],'| COREQ:',r['DS_Corequisites1'],'| TRANS:',r['DS_Transferable1']); print()
jobs=[('CET',int(sys.argv[1]) if False else 0,'')]
