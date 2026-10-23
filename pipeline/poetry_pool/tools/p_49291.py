import sys,re; sys.path.insert(0,'.')
from lib import *
from p_recit import classify
L,s=load(49291)
c=next(k for k,l in enumerate(L) if l.strip()=='CONTENTS.')
T=[];prev=None;k=c+1;buf=''
while k<len(L):
    l=L[k]
    m=re.match(r'^(\S.*?),?\s+(?:_(.+?)_,?)?\s*(\d+)\s*$',l)
    if m and not l.startswith(' '):
        t=(buf+' '+m.group(1)).strip().rstrip(','); buf=''
        a=m.group(2)
        if a in ('Id.','Ibid.','Id'): a=prev
        if a: prev=a
        T.append((t,a))
    elif l.strip() and not l.startswith(' ') and T: 
        if re.match(r'^[A-Z][A-Z ]+$',l.strip()) : break
        buf=(buf+' '+l.strip()).strip()
    elif not l.strip() and T and not L[k+1].strip() and not L[k+2].strip(): break
    k+=1
print(len(T),T[:3],T[-3:])
idx=locate(L,k,[t for t,a in T],maxind=0)
miss=[T[i] for i,x in enumerate(idx) if x is None];print('missing',len(miss),miss[:10])
found=[x for x in idx if x is not None]
rows=[]
for i,(t,a) in enumerate(T):
    x=idx[i];first=None;kind=None
    if x is not None:
        nxt=next((q for q in found if q>x),len(L))
        blk=L[x+1:nxt]
        q=0
        while q<len(blk) and blk[q].strip(): q+=1   # rest of heading lines
        body=blk[q:]
        kind=classify(body)
        first=next((fl(l) for l in body if l.strip() and not l.strip().startswith(('[','('))),None) if kind=='prose' else pick_first(body)
    r={'title':clean_title(t),'author':tc(re.sub(r'^(Rev\.|Bishop|Hon\.|Gov\.|Gen\.)\s*','',a)) if a else None,'first_line':first}
    if kind=='prose': r['kind']='prose'
    rows.append(r)
write_rows(49291,rows)
print('verse',sum(1 for r in rows if 'kind' not in r),'prose',sum(1 for r in rows if 'kind' in r))
print([ (r['title'],r['author'],r['first_line']) for r in rows if 'kind' not in r][:12])
