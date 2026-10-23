import sys,re; sys.path.insert(0,'.')
from lib import *
L,s=load(32373)
end=next(k for k,l in enumerate(L) if l.startswith('End of the Golden Treasury'))
H=[k for k,l in enumerate(L[:end]) if k>s+300 and re.match(r'^[IVXLC]+\s*$',l)]
rows=[]
for j,k in enumerate(H):
    nxt=H[j+1] if j+1<len(H) else end
    blk=L[k+1:nxt]
    cut=next((q for q,l in enumerate(blk) if re.match(r'^(Book |The Golden Treasury)',l)),len(blk)); blk=blk[:cut]
    nb=[l for l in blk if l.strip()]
    t=None
    if nb and nb[0].startswith('_') and is_caps(nb[0]):
        t=nb[0].strip('_ ')
        if not nb[0].rstrip().endswith('_') and len(nb)>1: t+=' '+nb[1].strip('_ ')
    au=nb[-1].strip() if nb and nb[-1].startswith('_') and not is_caps(nb[-1]) else None
    body=blk
    first=pick_first(body)
    rows.append({'title':clean_title(t) if t else first,'author':tc(au.strip('_ ')) if au else None,'first_line':first})
write_rows(32373,rows)
for r in rows:
    if not r['author'] or not r['first_line']: print(r)
sample(32373)
