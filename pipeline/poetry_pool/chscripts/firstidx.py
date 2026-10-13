import sys,re; sys.path.insert(0,'.'); from common import *
# usage: pg index_marker_regex body_start_marker_regex [stop_regex]
pg=int(sys.argv[1]); im=sys.argv[2]; bm=sys.argv[3]
L=load(pg).split('\n')
ii=[k for k,l in enumerate(L) if re.search(im,l)][-1]
ents=[]
for l in L[ii+1:]:
    m=re.match(r'^\s+(\S.*?)[\s.]{2,}(\d+)\s*$',l)
    if m: ents.append((m.group(1).strip(),int(m.group(2))))
    elif ents and l.strip() and not m and not re.match(r'^\s+\S',l): break
bi=[k for k,l in enumerate(L) if re.search(bm,l)][0]
body=[norm(l) for l in L]
rows=[]
used=set()
for t,p in ents:
    nt=norm(t)[:25]; pos=None
    for k in range(bi,len(L)):
        if k in used: continue
        if body[k].startswith(nt) and nt:
            pos=k; used.add(k); break
    rows.append((pos if pos is not None else 10**9, p, t))
miss=[r for r in rows if r[0]==10**9]
rows.sort(key=lambda r:(r[1],r[0]))
print(len(ents),'notfound',len(miss),miss[:10])
write(pg,[{'title':t,'author':None,'first_line':t} for pos,p,t in rows])
