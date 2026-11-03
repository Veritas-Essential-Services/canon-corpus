import json
t=open('page.tpl.html').read()
def r(f): return open(f).read().replace('</','<\\/')
adds=json.load(open('adds.json'))
t=t.replace('__DATA__',r('adm.json')).replace('__BLOOM__',r('bloomck2.json')).replace('__ADDS__',r('adds.json')).replace('__NADD__',str(len(adds)))
open('admissions.html','w').write(t); print('built',len(adds),len(t))
