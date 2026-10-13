import sys,re; sys.path.insert(0,'.')
from lib import *
from p_recit import classify
L,s=load(24798)
c=next(k for k,l in enumerate(L) if l.strip()=='CONTENTS')
T=[];k=c+1;blank=0
while k<len(L):
    l=L[k]
    m=re.match(r'^\s+(\S.*?)\s{2,}_(.+?)_\s+(\d+)\s*$',l)
    if m: T.append((m.group(1),m.group(2)))
    if not l.strip(): blank+=1
    else: blank=0
    if blank>=4 and T: break
    k+=1
print(len(T),T[:2],T[-2:])
idx=locate(L,k,[t for t,a in T])
miss=[T[i] for i,x in enumerate(idx) if x is None];print('missing',len(miss),miss[:10])
found=[x for x in idx if x is not None]
rows=[]
for i,(t,a) in enumerate(T):
    x=idx[i];first=None;kind=None
    if x is not None:
        nxt=next((q for q in found if q>x),len(L))
        blk=L[x+1:nxt]
        body=[l for l in blk if not (is_caps(l) and len(l.strip())<60)]
        # drop author line
        kind=classify(body)
        first=next((fl(l) for l in body if l.strip() and not l.strip().startswith(('[','(','_'))),None) if kind=='prose' else pick_first(blk)
    r={'title':clean_title(t),'author':tc(a),'first_line':first}
    if kind=='prose': r['kind']='prose'
    rows.append(r)
write_rows(24798,rows)
print('verse',sum(1 for r in rows if 'kind' not in r),'prose',sum(1 for r in rows if 'kind' in r))
print([(r['title'],r['author'],r['first_line']) for r in rows if 'kind' not in r][:15])
