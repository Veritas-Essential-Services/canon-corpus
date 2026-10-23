import sys,re; sys.path.insert(0,'.'); from common import *
def do(pg,cm,author,tocre):
    L=load(pg).split('\n')
    ci=[k for k,l in enumerate(L) if l.strip()==cm][0]
    toc=[]; k=ci+1; started=False
    while k<len(L):
        l=L[k]; m=re.match(tocre,l)
        if m: toc.append(m.group(1).strip()); started=True
        elif started and l.strip()=='VERSES FOR CHILDREN.': break
        elif started and l.strip() and not re.match(r'^[A-Z ]+\.$',l.strip()): break
        k+=1
    idx=seq_find(L,k,toc,match=lambda l,t: l.strip().upper()==l.strip() and (norm(l)==norm(t) or (len(norm(l))>4 and norm(t).startswith(norm(l))) or norm(l).startswith(norm(t.split(':')[0].split(';')[0]))),window=30000)
    rows=[{'title':tcase(t),'author':author,'first_line':verse_after(L,ix,minindent=0) if ix is not None else None} for t,ix in zip(toc,idx)]
    print(pg,len(toc),[t for t,ix in zip(toc,idx) if ix is None])
    write(pg,rows)
do(40576,'CONTENTS','Alice Lewis Richards',r'^([A-Z][^a-z]+?)\s{2,}\d+\s*$')
do(16686,'CONTENTS.','Juliana Horatia Ewing',r'^    (["A-Z][^a-z]*?(?:\(_[^_]+_\))?)\s*$')
