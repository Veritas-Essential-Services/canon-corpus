import sys,re; sys.path.insert(0,'.')
from lib import *
L,s=load(66619)
st=next(k for k,l in enumerate(L) if l.startswith('_1._ _Cuckoo'))
end=len(L)
for k in range(st,len(L)):
    if re.match(r'^(INDEX|NOTES|Index of|INDEX OF)',L[k]): end=k;break
H=[(k,m) for k,l in enumerate(L[:end]) if k>=st and (m:=re.match(r'^\s{0,4}_(\d+)\._?\s*(.*?)\s*$',l)) and ']' not in l]
AU={}
for l in L[:st]:
    mm=re.match(r'^(\d+)(?:-(\d+))?\.\s+(.*?)\.{4,}',l)
    if mm:
        nm=re.split(r'\.?\s+(?:b\.|d\.|_c\._|c\.|fl\.|[XVI]+[-\s])',mm.group(3))[0].strip().rstrip('.').strip()
        for n in range(int(mm.group(1)),int(mm.group(2) or mm.group(1))+1): AU[n]=nm
print(len(AU))
rows=[];au=None;last=st
for j,(k,m) in enumerate(H):
    for q in range(last,k):
        x=L[q]
        if x and not x[0].isspace() and is_caps(x) and len(x)<80 and not ROMAN.match(x.strip()) and not x.startswith('['): au=x.strip()
    nxt=H[j+1][0] if j+1<len(H) else end
    blk=L[k+1:nxt]; last=k+1
    t=m.group(2)
    if t and not t.endswith('_') and not L[k].rstrip().endswith('_'):
        pass
    first=pick_first(blk,skip=lambda x:'Cent.' in x)
    rows.append({'title':clean_title(t.replace('_','')) if t else first,'author':AU.get(int(m.group(1))) or tc(au),'first_line':first,'num':int(m.group(1))})
nums=[r['num'] for r in rows]; print('max',max(nums),'count',len(nums),'missing',sorted(set(range(1,max(nums)+1))-set(nums))[:30])
write_rows(66619,rows)
for r in rows:
    if not r['author'] or not r['first_line']: print(r)
sample(66619)
