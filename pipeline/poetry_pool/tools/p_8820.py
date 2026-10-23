import sys,re; sys.path.insert(0,'.')
from lib import *
L,s=load(8820)
c=next(k for k,l in enumerate(L) if l.strip()=='CONTENTS')
e=next(k for k in range(c,len(L)) if L[k].strip()=='INDEXES')
T=[];buf=''
for l in L[c+1:e]:
    if not l.strip():
        buf='';continue
    x=(buf+' '+l.strip()).strip()
    m=re.match(r'^([^a-z]+?):\s+(.+)$',x)
    if m: T.append((m.group(2).strip(),m.group(1).strip()));buf=''
    elif re.match(r'^[A-Z]',x) and not re.match(r'^[IVX]+\. ',x): buf=x
print(len(T),T[:2],T[-2:])
end=next(k for k in range(len(L)-1,0,-1) if L[k].strip().startswith('INDEX OF AUTHORS') or L[k].strip()=='INDEX OF FIRST LINES')
end=min(k for k in range(e+5,len(L)) if L[k].strip().startswith('INDEX OF'))
idx=locate(L,e+5,[t for t,a in T],end=end,maxind=2)
miss=[T[i] for i,k in enumerate(idx) if k is None];print('missing',len(miss),miss[:10])
fls=from_located(L,idx,end)
rows=[{'title':clean_title(t),'author':tc(re.sub(r'^(LIEUTENANT|CAPTAIN|SERGEANT|CORPORAL|PRIVATE|MAJOR|COLONEL|SECOND LIEUTENANT|SUB-LIEUTENANT)\s+','',a)),'first_line':f} for (t,a),f in zip(T,fls)]
write_rows(8820,rows); sample(8820,8)
