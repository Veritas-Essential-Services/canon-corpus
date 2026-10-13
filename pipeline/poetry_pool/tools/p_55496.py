import sys,re; sys.path.insert(0,'.')
from lib import *
L,s=load(55496)
st=next(k for k,l in enumerate(L) if l.strip()=='PART THE FIRST.')
end=next(k for k,l in enumerate(L) if l.strip()=='NOTES.')
H=[k for k in range(st,end) if re.match(r'^[IVXLC]+\.?\s*$',L[k])]
rows=[]
for j,k in enumerate(H):
    nxt=H[j+1] if j+1<len(H) else end
    blk=L[k+1:nxt]
    nb=[l for l in blk if l.strip() and not re.match(r'^PART THE',l)]
    t=None
    if nb and nb[0].strip().startswith('_') and is_caps(nb[0]):
        t=nb[0].strip()
        q=blk.index(nb[0])
        while not t.rstrip('.').endswith('_') and q+1<len(blk) and blk[q+1].strip(): q+=1; t+=' '+blk[q].strip()
        t=t.replace('_','')
    au=None
    for l in reversed(nb):
        x=l.strip()
        if x.startswith('_') and not is_caps(x) and len(x)<60: au=x.replace('_','')
        break
    first=pick_first(blk)
    rows.append({'title':clean_title(t) if t else first,'author':tc(au),'first_line':first})
write_rows(55496,rows)
print(len(H),'noau',sum(1 for r in rows if not r['author']),'nofl',[r for r in rows if not r['first_line']][:5])
sample(55496)
