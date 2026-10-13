import sys,re; sys.path.insert(0,'.'); from common import *
pg=23457; L=load(pg).split('\n')
ci=[k for k,l in enumerate(L) if l.strip()=='CONTENTS.'][0]
toc=[]; k=ci+1
while True:
    m=re.match(r'^_(.+?)_\s+(\d+)\s*$',L[k].strip())
    if m: toc.append(m.group(1))
    elif toc and L[k].strip() and not L[k].strip().startswith('Page') and not re.match(r'^-+ *_',L[k].strip()): break
    elif re.match(r'^-+ *_(.+?)_',L[k].strip()):
        toc.append(toc[-1].split(',')[0].replace(' Part I.','')+' '+re.match(r'^-+ *_(.+?)_',L[k].strip()).group(1))
    k+=1
idx=seq_find(L,k,toc,match=lambda l,t: l.strip().upper()==l.strip() and len(norm(l))>3 and (norm(t).startswith(norm(l)) or norm(l).startswith(norm(t))),window=20000)
rows=[{'title':t,'author':None,'first_line':verse_after(L,ix,minindent=0) if ix is not None else None} for t,ix in zip(toc,idx)]
print([t for t,ix in zip(toc,idx) if ix is None])
write(pg,rows)
for r in rows: print(r)
