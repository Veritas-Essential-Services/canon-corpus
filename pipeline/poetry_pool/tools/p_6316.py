import sys,re; sys.path.insert(0,'.')
from lib import *
L,s=load(6316)
c=next(k for k,l in enumerate(L) if l.strip()=='TABLE OF CONTENTS')
T=[]
k=c+1
while k<len(L):
    l=L[k].strip()
    if l and not ',' in l and T and l.isupper() and len(l)>3 and 'ILLUSTRAT' not in l: break
    if l.startswith('ILLUSTRATIONS') or l=='LIST OF ILLUSTRATIONS': break
    if l:
        m=re.match(r'^(.*),\s*([^,]+)$',l)
        if m: T.append((m.group(1),m.group(2)))
        else: T.append((l,None))
    k+=1
print(len(T),T[-3:],L[k])
idx=locate(L,k,[t for t,a in T])
miss=[T[i] for i,x in enumerate(idx) if x is None]; print('missing',len(miss),miss[:10])
end=next((q for q in range(len(L)-1,0,-1) if 'INDEX' in L[q]),len(L)) 
fls=from_located(L,idx,len(L))
rows=[{'title':clean_title(t),'author':tc(a),'first_line':f} for (t,a),f in zip(T,fls)]
for r in rows:
    if r['title']=='Kearny at Seven Pines': r['first_line']='So that soldierly legend is still on its journey,--'
write_rows(6316,rows)
for r in rows:
    if not r['first_line']: print(r)
sample(6316)
