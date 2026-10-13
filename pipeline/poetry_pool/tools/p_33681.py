import sys,re; sys.path.insert(0,'.')
from lib import *
L,s=load(33681)
c=next(k for k,l in enumerate(L) if l.strip()=='CONTENTS')
T=[];k=c+1
while k<len(L):
    m=re.match(r'^\s+(\S.*?)\s{2,}_(.+?)_\s+(\d+)\s*$',L[k])
    if m: T.append((m.group(1),m.group(2)))
    elif T and L[k].strip() and not m: break
    k+=1
print(len(T))
idx=locate(L,k,[t for t,a in T])
miss=[T[i] for i,x in enumerate(idx) if x is None];print('missing',miss)
fls=from_located(L,idx,len(L))
rows=[{'title':clean_title(t),'author':tc(a),'first_line':f} for (t,a),f in zip(T,fls)]
rows[-1]['first_line']='Rejoice, O land, in God thy might.'
write_rows(33681,rows); sample(33681,5)
