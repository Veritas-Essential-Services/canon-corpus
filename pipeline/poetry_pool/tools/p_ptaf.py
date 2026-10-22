import sys,re; sys.path.insert(0,'.')
from lib import *
def run(pg):
    L,s=load(pg)
    ix=next(k for k,l in enumerate(L) if l.strip().startswith('INDEX'))
    E=[]
    for l in L[ix+1:ix+600]:
        m=re.match(r'^(\S.*?)\s{2,}(?:_(.+?)_)?\s*(\d+)\s*$',l)
        if m: E.append((int(m.group(3)),uninvert(m.group(1)),m.group(2)))
        elif l.strip() and not m and E and re.match(r'^[A-Z]{4,}',l.strip()): break
    print(pg,len(E))
    st=next(k for k in range(ix,len(L)) if l_is(L[k]))
    end=len(L)
    idx=locate_any(L,st,end,[t for p,t,a in E])
    miss=[E[i] for i,k in enumerate(idx) if k is None]; print('missing',len(miss),miss[:15])
    items=sorted([(k,E[i]) for i,k in enumerate(idx) if k is not None])
    rows=[]
    for j,(k,(p,t,a)) in enumerate(items):
        nxt=items[j+1][0] if j+1<len(items) else end
        blk=L[k+1:nxt]
        first=pick_first(blk,use_indent=False)
        nb=[l.strip() for l in blk if l.strip()]
        au=None
        if nb and nb[-1].startswith('_') and len(nb[-1])<60: au=nb[-1].strip('_. ').rstrip('_').strip()
        rows.append({'title':t,'author':tc(au) if au else (tc(a) if a else None),'first_line':first})
    for p,t,a in miss: rows.append({'title':t,'author':tc(a) if a else None,'first_line':None})
    write_rows(pg,rows); sample(pg,8)
def l_is(l): return l.strip().startswith('POEMS TEACHERS ASK FOR')
run(18909); run(19469)
