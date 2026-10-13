import sys,re; sys.path.insert(0,'.')
from lib import *
L,s=load(56956)
c=next(k for k,l in enumerate(L) if l.strip()=='CONTENTS')
end=next(k for k,l in enumerate(L) if l.strip()=='INDEX OF FIRST LINES')
# body start: first caps heading after contents block end
k=c+1
while not re.match(r'^\s*$',L[k]) or True:
    if L[k].strip() and not re.search(r'\d+\s*$',L[k]) and not L[k+1].strip()=='' and False: break
    k+=1
    if k>c+700: break
ce=max(k for k in range(c,end) if re.search(r'\s\d+\s*$',L[k]) and k<c+800)
H=[]
for k in range(ce+1,end):
    l=L[k]
    if l.strip() and not l[0].isspace() and is_caps(l) and not L[k-1].strip() and not L[k-2].strip() and not re.search(r'\s{3,}\d+\s*$',l) and '_' not in l:
        H.append(k)
rows=[]
for j,k in enumerate(H):
    nxt=H[j+1] if j+1<len(H) else end
    blk=L[k+1:nxt]
    title=L[k].strip()
    q=0
    while q<len(blk) and blk[q].strip() and not blk[q][0].isspace(): title+=' '+blk[q].strip(); q+=1
    au=None
    for l in blk[q:]:
        if l.strip():
            if not l[0].isspace() and is_caps(l): au=l.strip()
            break
    first=None
    for qi,l in enumerate(blk):
        if re.match(r'^    \S',l) and re.search('[a-z]',l) and (qi==0 or not re.match(r'^     \S',blk[qi-1])):
            # ensure not inside an indented-5 note paragraph
            first=fl(l);break
    if first is None: continue
    rows.append({'title':clean_title(title),'author':tc(au) if au else None,'first_line':first})
C={};buf=''
for l in L[c+1:ce+1]:
    m=re.match(r'^(\S.*?)\s{2,}(?:_(.+?)_)?\s*(\d+)\s*$',l)
    if m:
        t=(buf+' '+m.group(1)).strip(); buf=''
        C[norm(uninvert(t))]=m.group(2)
    elif l.strip() and not l[0].isspace(): buf=(buf+' '+l.strip()).strip()
    else: buf=''
print('contents',len(C))
for r in rows:
    a=C.get(norm(r['title']))
    if not r['author'] and a: r['author']=tc(a)
print(len(H),len(rows))
for r in rows:
    for _ in range(3):
      if r['author']: r['author']=re.sub(r'^(Lieut\.?|Lieutenant|Sergt\.?|Sergeant|Corp\.?|Corporal|Private|Pvt\.?|Capt\.?|Captain|Major|Col\.?|Colonel|Dr\.|Chaplain|Gen\.?|General|Lieut\. Col\.|Lieut\.-col\.|Lieut\. Col\.)\s+','',r['author'],flags=re.I)
write_rows(56956,rows); sample(56956,8)
print([r['title'] for r in rows if not r['author']][:20])
