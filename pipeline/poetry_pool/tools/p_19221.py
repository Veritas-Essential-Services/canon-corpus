import sys,re; sys.path.insert(0,'.')
from lib import *
L,s=load(19221)
end=next(k for k,l in enumerate(L) if 'INDEX OF WRITERS' in l)
H=[(k,m) for k,l in enumerate(L[:end]) if k>s and (m:=re.match(r'^ {5}(\d+)\.(--[IVX]+\.)?(?: (.+?))?\s*$',l)) and int(m.group(1))<300]
rows=[];prev=None
for j,(k,m) in enumerate(H):
    nxt=H[j+1][0] if j+1<len(H) else end
    blk=L[k+1:nxt]
    cut=next((q for q,l in enumerate(blk) if l and not l[0].isspace()),len(blk)); blk=blk[:cut]
    nb=[l for l in blk if l.strip()]
    t=m.group(3)
    if t and nb and nb[0].strip().isupper() and len(nb[0].strip())>3 and not re.match(r'^\d',nb[0].strip()) and (t.endswith(',') or re.search(r'\b(of|the|and|to)$',t,re.I)):
        t=t+' '+nb[0].strip()
    first=pick_first(blk)
    au=None
    for l in reversed(nb):
        x=l.strip()
        if is_caps(x) and len(x)<70 and not re.search(r'BOOK|SUMMARY',x): au=x
        break
    if m.group(2): t=(prev or '')+' '+m.group(2).strip('-.')
    elif t: prev=clean_title(t)
    rows.append({'title':clean_title(t) if t else first,'author':tc(au),'first_line':first,'num':int(m.group(1))})
nums=[r['num'] for r in rows]; print('max',max(nums),'count',len(nums),'missing',sorted(set(range(1,max(nums)+1))-set(nums))[:20])
write_rows(19221,rows)
import json
for r in rows:
    if not r['author'] or not r['first_line']: print(r)
