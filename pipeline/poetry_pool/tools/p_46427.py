import sys,re; sys.path.insert(0,'.')
from lib import *
L,s=load(46427)
c=next(k for k,l in enumerate(L) if l.strip()=='CONTENTS')
T=[]
k=c+3
while k<len(L):
    l=L[k]
    if not l.strip():
        if T and not L[k+1].strip(): break
        k+=1; continue
    tcol=l[:42].strip(); acol=l[42:].strip()
    m=re.match(r'^(.*?)\s*(\d+)$',acol)
    page=None
    if m: acol,page=m.group(1),m.group(2)
    if l.startswith('      ') and T:
        if tcol: T[-1][0]+=' '+tcol
        if acol: T[-1][1]=(T[-1][1]+' '+acol).strip()
    elif l.startswith('  ') and not tcol and T:
        T.append([T[-1][0],acol])  # additional author same title
    elif l.startswith('  '):
        T.append([tcol,acol])
    k+=1
print(len(T),T[-2:])
def fixau(a):
    a=a.strip()
    if not a: return None
    if a.startswith('"'): return a.strip('"')
    if ',' in a:
        last,first=a.split(',',1)
        first=re.sub(r'\b(Rt\.|Hon\.|Rev\.|Sir|Private|General|Field-Marshal|Marshal|Monsieur|Lord)\s*','',first).strip()
        if not first: return last.strip()+(' (Lord)' if 'Lord' in a else '')
        return first+' '+last.strip()
    return a
titles=[uninvert(t) for t,a in T]
import difflib
end=len(L)
H=[q for q in range(k,end) if L[q].strip() and not L[q][0].isspace() and is_caps(L[q]) and not L[q-1].strip() and not L[q-2].strip() and len(L[q].strip())>3]
rows=[];ptr=0
for j,x in enumerate(H):
    nxt=H[j+1] if j+1<len(H) else end
    blk=L[x+1:nxt]
    head=L[x].strip()
    q=0
    while q<len(blk) and blk[q].strip() and not blk[q][0].isspace() and is_caps(blk[q]): head+=' '+blk[q].strip(); q+=1
    cl=next((l for l in blk[q:] if l.strip() and not l.strip().startswith(('(','_','[')) and not is_caps(l)),None)
    if cl is None: continue
    kind='prose' if (not cl[0].isspace() and len(cl.strip())>55) else None
    first=fl(cl) if kind else pick_first(blk[q:])
    best=None
    for i in range(ptr,min(ptr+4,len(titles))):
        r=difflib.SequenceMatcher(None,norm(head),norm(titles[i])).ratio()
        if norm(titles[i]) and norm(titles[i]) in norm(head): r=max(r,0.9)
        if best is None or r>best[0]: best=(r,i)
    au=None;title=clean_title(head)
    if best and best[0]>0.45:
        i=best[1]; au=fixau(T[i][1]); title=titles[i] if titles[i] else title; ptr=i+1
    r={'title':title,'author':au,'first_line':first}
    if kind: r['kind']=kind
    rows.append(r)
for r in rows:
    if r['title'].lower().startswith('"for all we'): r['title']='"For All We Have and Are"'; r['author']='Rudyard Kipling'
    if 'Kitchener\'s Instructions' in r['title']: r['author']='Lord Kitchener'
    if r['author']=='Kitchener (Lord)': r['author']='Lord Kitchener'
print(len(H),len(rows),'unmatched',[r['title'] for r in rows if not r['author']])
write_rows(46427,rows); sample(46427,10)
print(sum(1 for r in rows if r.get('kind')),'prose')
