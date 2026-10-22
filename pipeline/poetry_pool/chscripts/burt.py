import sys,re; sys.path.insert(0,'.'); from common import *
T=load(16436); L=T.split('\n')
toc=[]
i=[k for k,l in enumerate(L) if l.strip()=='CONTENTS'][0]
end=[k for k,l in enumerate(L) if l.strip()=='INDEX OF AUTHORS'][0]
k=i
while k<end:
    m=re.match(r'^\s*(\d+)\. (.+?)\s+\d+\s*$',L[k])
    if m:
        a=L[k+1].strip()
        toc.append((m.group(2).strip(),a)); k+=2; continue
    k+=1
idx=seq_find(L,end,[t for t,a in toc],match=lambda l,t: norm(l).startswith(norm(t)) and l.startswith(' ') and l.strip().upper()==l.strip())
rows=[]
for (t,a),ix in zip(toc,idx):
    fl=verse_after(L,ix,minindent=3) if ix is not None else None
    if a in ('ANONYMOUS','AN OLD SONG') or not a: a=None
    rows.append({'title':t,'author':tcase(a) if a else None,'first_line':fl})
FIX={'The Rainbow (a fragment)':'My heart leaps up when I behold','The New Arrival':'There came to port last Sunday night','A Fragment from "Julius Caesar"':'This was the noblest Roman of them all:'}
for r in rows:
    if not r['first_line']: r['first_line']=FIX.get(r['title'])
print(len(toc),sum(1 for x in idx if x is None))
write(16436,rows)
