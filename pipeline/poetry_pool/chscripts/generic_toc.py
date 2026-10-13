import sys,re; sys.path.insert(0,'.'); from common import *
# usage: pg startmarker endmarker [bodystart_marker]
pg=int(sys.argv[1]); sm=sys.argv[2]; em=sys.argv[3]
T=load(pg); L=T.split('\n')
ci=[k for k,l in enumerate(L) if l.strip()==sm][0]
ei=[k for k,l in enumerate(L) if k>ci and l.strip().startswith(em)][0]
toc=[]; prev=None
for l in L[ci+1:ei]:
    m=re.match(r'^\s*(\S.*?)\s{2,}(?:(_[^_]+_|"_[^_]+_"|”|")\s+)?(\d+)\s*$',l)
    if m:
        t=m.group(1).strip(); a=m.group(2)
        if a in ('”','"'): a=prev
        elif a: a=a.strip('"').strip('_')
        toc.append((t,a)); prev=a
idx=seq_find(L,ei,[t for t,a in toc],match=lambda l,t: l.strip().upper()==l.strip() and len(norm(t))>=8 and norm(l).startswith(norm(t)),window=30000)
rows=[]
for (t,a),ix in zip(toc,idx):
    if a=='Modern, anon.': a=None
    if a=='Sir Waller Scott': a='Sir Walter Scott'
    if a=='H. W. Longfellow': a='Henry Wadsworth Longfellow'
    if a and a.lower() in ('anonymous','unknown','old ballad','author unknown','traditional'): a=None
    rows.append({'title':tcase(t.strip('“”"')),'author':a,'first_line':verse_after(L,ix,minindent=2) if ix is not None else None})
print(len(toc),'missing',[t for (t,a),x in zip(toc,idx) if x is None])
write(pg,rows)
