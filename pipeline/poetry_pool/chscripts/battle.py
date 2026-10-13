import sys,re; sys.path.insert(0,'.'); from common import *
pg=70415; L=load(pg).split('\n')
ci=[k for k,l in enumerate(L) if l.strip()=='CONTENTS.'][0]
ei=[k for k,l in enumerate(L) if l.strip()=='ILLUSTRATIONS.'][0]
toc=[]
for l in L[ci+1:ei]:
    m=re.match(r'^\s+([A-Z][^a-z_]+?)\s{2,}(\d+)\s*$',l)
    if m and 'PREFACE' not in m.group(1): toc.append(m.group(1).strip())
idx=seq_find(L,ei+40,toc,match=lambda l,t: l.strip().upper()==l.strip() and norm(l).startswith(norm(t)[:14]) and len(norm(l))>3,window=30000)
rows=[{'title':tcase(t),'author':'Thomas Dunn English','first_line':verse_after(L,ix,minindent=2) if ix is not None else None} for t,ix in zip(toc,idx)]
print(len(toc),[t for t,ix in zip(toc,idx) if ix is None])
write(pg,rows)
import random; random.seed(1)
for r in random.sample(rows,5): print(r)
