import sys,re; sys.path.insert(0,'.'); from common import *
def strip_num(s):
    return re.sub(r'\s{2,}\d+\s*$','',s).strip() if s else s
# 13184
pg=13184; L=load(pg).split('\n')
ci=[k for k,l in enumerate(L) if l.strip()=='CONTENTS'][0]
toc=[]; k=ci+1
while True:
    m=re.match(r'^(\S.*?)\s*(?:\. ?)+\s*\.?\s+(\S.*)$',L[k])
    if m and ' . ' in L[k]: toc.append((m.group(1).strip(),m.group(2).strip()))
    elif toc and L[k].strip() and not m: break
    k+=1
idx=seq_find(L,k,[t for t,a in toc],match=lambda l,t: l.strip().upper()==l.strip() and norm(l).startswith(norm(t)[:12]),window=30000)
rows=[{'title':t,'author':a,'first_line':strip_num(verse_after(L,ix,minindent=2)) if ix is not None else None} for (t,a),ix in zip(toc,idx)]
print(len(toc),'missing',[t for (t,a),x in zip(toc,idx) if x is None])
write(pg,rows)
pg=48484; L=load(pg).split('\n')
ci=[k for k,l in enumerate(L) if l.strip()=='=CONTENTS.='][0]
toc=[]
for k in range(ci,ci+100):
    m=re.match(r'^\s+_([^_]+)_\s+(\S.*?)\s+\(\s*\d+\s*\)\s+\d+\s*$',L[k])
    if m: toc.append((m.group(2).strip(),m.group(1).strip()))
idx=seq_find(L,ci+60,[t for t,a in toc],match=lambda l,t: l.strip().upper()==l.strip() and len(norm(l))>3 and (norm(l).startswith(norm(t)[:12]) ),window=30000)
rows=[{'title':t,'author':a,'first_line':strip_num(verse_after(L,ix,minindent=2)) if ix is not None else None} for (t,a),ix in zip(toc,idx)]
print(len(toc),'missing',[t for (t,a),x in zip(toc,idx) if x is None])
write(pg,rows)
