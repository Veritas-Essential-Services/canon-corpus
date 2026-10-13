import sys,re; sys.path.insert(0,'.')
from lib import *
def author_of(l):
    x=l.strip()
    if not x or len(x)>100: return None
    if is_caps(x) and not ROMAN.match(x): return x
    mm=re.search(r"([A-Z][A-Z.'\- ,]+[A-Z])\.?\)?$",x)
    if mm and len(mm.group(1))>3: return mm.group(1)
    return None
def run(pg,maxind):
    L,s=load(pg)
    ix=[k for k,l in enumerate(L) if re.match(r'^\s*INDEX(:| OF) (TITLES|AUTHORS)',l)]
    end=ix[-1]
    st=next(k for k in range(s,len(L)) if 'LIST OF ILLUSTRATIONS' in L[k])
    # first poem: first caps title preceded by 2 blanks after an 'POEMS OF' line beyond illustrations
    st=next(k for k in range(st,end) if L[k].strip().startswith('POEMS OF') and k>st)
    heads=[]
    k=st
    while k<end:
        l=L[k]
        ind=len(l)-len(l.lstrip())
        if l.strip() and ind<=maxind and is_caps(l) and not L[k-1].strip() and not L[k-2].strip() and not STAR.match(l):
            t=l.strip(); q=k
            heads.append([k,t]); 
        k+=1
    rows=[]
    for j,(k,t) in enumerate(heads):
        nxt=heads[j+1][0] if j+1<len(heads) else end
        blk=L[k+1:nxt]
        # verse present?
        first=pick_first(blk,use_indent=False)
        if not first: continue
        # title continuation: following caps lines without blank
        q=k+1;title=t
        while q<nxt and L[q].strip() and is_caps(L[q]) and (len(L[q])-len(L[q].lstrip()))<=maxind: title+=' '+L[q].strip(); q+=1
        # author: last nonblank line of block
        nb=[l for l in blk if l.strip()]
        au=author_of(nb[-1]) if nb else None
        rows.append({'title':clean_title(title),'author':tc(au),'first_line':first})
    write_rows(pg,rows)
    print('noau',sum(1 for r in rows if not r['author']))
    sample(pg,8)
STAR=re.compile(r'^\s*\*\s+\*\s+\*')
run(16786,0); run(43223,2)
