import sys,re; sys.path.insert(0,'.')
from lib import *
STAR=re.compile(r'^\s*\*\s+\*\s+\*')
def run(pg, rows_out=True):
    L,s=load(pg)
    idxs=[k for k,l in enumerate(L) if re.match(r'^\s*INDEX(:| OF| )',l.strip()+' ')]
    end=idxs[-1] if idxs and idxs[-1]>len(L)/2 else len(L)
    # start: first star line minus a chunk; segments are between star lines, prepend the chunk before first star
    stars=[k for k in range(s,end) if STAR.match(L[k])]
    # find start of first poem: search back from first star for the essay end - use 'POEMS OF' heading
    st=next((k for k in range(s+300,stars[0]) if re.match(r'^(POEMS OF|POEMS$|[A-Z ,]+\.$)',L[k]) and k> s+300 and L[k].strip().startswith('POEMS')),None)
    segs=[]
    bounds=[st]+stars+[end]
    rows=[]
    for a,b in zip(bounds,bounds[1:]):
        seg=L[a+1:b] if a!=st else L[a:b]
        # first verse line idx
        vi=None
        for q,l in enumerate(seg):
            x=l.strip()
            if x and l[0].isspace() and re.search('[a-z]',x) and not x.startswith(('_','[')): vi=q;break
        if vi is None: continue
        pre=seg[:vi]
        # title = last group of non-indented caps lines
        groups=[];cur=[]
        for l in pre:
            if l.strip() and not l[0].isspace() and is_caps(l): cur.append(l.strip())
            else:
                if cur: groups.append(cur);cur=[]
        if cur: groups.append(cur)
        title=' '.join(groups[-1]) if groups else None
        # author: last non-indented nonblank line
        au=None
        for l in reversed(seg):
            if l.strip():
                if not l[0].isspace() and is_caps(l) and len(l.strip())<80: au=l.strip()
                elif not l[0].isspace() and len(l.strip())<100:
                    mm=re.search(r"([A-Z][A-Z.'\- ]+[A-Z])\.?$",l.strip())
                    if mm and len(mm.group(1))>3: au=mm.group(1)
                break
        first=pick_first(seg[vi:])
        if title: rows.append({'title':clean_title(title),'author':tc(au),'first_line':first})
        else: rows.append({'title':first,'author':tc(au),'first_line':first})
    write_rows(pg,rows)
    print('noau',sum(1 for r in rows if not r['author']),'notitle-from-heading',sum(1 for r in rows if r['title']==r['first_line']))
    sample(pg,6)
for pg in (12759,12924): run(pg)
