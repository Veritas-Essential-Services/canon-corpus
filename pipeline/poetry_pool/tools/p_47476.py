import sys,re; sys.path.insert(0,'.')
from lib import *
L,s=load(47476)
c=next(k for k,l in enumerate(L) if l.strip()=='TABLE OF CONTENTS')
e=next(k for k in range(c,len(L)) if 'INDEX OF AUTHORS' in L[k])
T=[];buf=''
for l in L[c+1:e]:
    if not l.strip(): buf='';continue
    x=(buf+' '+l.strip()) if buf else l.strip()
    x=x.replace(', Jr.',' Jr.')
    m=re.match(r'^(.+),"?\s+(.+?)\s{2,}(\d+)$',x) or re.match(r'^(.+),"?\s+(.+?)\s+(\d+)$',x)
    if m and l.startswith('  '):
        T.append((m.group(1).strip(),m.group(2).strip()));buf=''
    elif l.startswith('  ') and x.isupper()==False and ',' in x and not x.startswith('_'):
        buf=x
    else: buf=''
print(len(T),T[:3],T[-3:])
st=e+5
end=next(k for k,l in enumerate(L) if l.strip()=='NOTES AND INDEXES' and k>st)
idx=locate(L,st,[t for t,a in T],end=end,maxind=0)
miss=[(i,T[i]) for i,x in enumerate(idx) if x is None]; print('missing',len(miss),miss[:15])
fls=from_located(L,idx,end)
rows=[{'title':clean_title(t),'author':tc(a),'first_line':f} for (t,a),f in zip(T,fls)]
write_rows(47476,rows)
print('nofl',sum(1 for r in rows if not r['first_line']))
