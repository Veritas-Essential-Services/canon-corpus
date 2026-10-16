import sys,re; sys.path.insert(0,'.')
from lib import *
L,s=load(52133)
c=next(k for k,l in enumerate(L) if l.strip()=='CONTENTS')
e=next(k for k in range(c,len(L)) if L[k].strip().startswith('INDEX OF FIRST LINES'))
T=[];au=None;buf=None
for l in L[c+1:e]:
    m=re.match(r'^\s+([IVXLC]+)\.\s+(.+?)(?:\s{2,}(\d+))?\s*$',l)
    if m and r2i(m.group(1)):
        T.append([r2i(m.group(1)),m.group(2),au]); continue
    m2=re.match(r'^  ([A-Z][^a-z]*?)(?:\s*\(.*\))?\.?\s*$',l)
    if m2 and l.strip() and not l.strip().startswith(('NOTES','INDEX')):
        au=m2.group(1).strip().rstrip('.')
        if au=='BALLADS': au=None
        continue
    if l.startswith('        ') and T and l.strip() and not re.search(r'\d+$',T[-1][1]) : T[-1][1]+=' '+l.strip()
# strip page nums / dates in titles
for t in T: t[1]=re.sub(r'\s{2,}\d+$','',t[1]).strip()
print(len(T),T[:3],T[-2:])
st=e+3; end=next(k for k in range(st,len(L)) if L[k].strip()=='NOTES')
# body: roman heading lines followed by caps title
H={}
expect=1
for k in range(st,end):
    x=L[k].strip()
    if re.match(r'^[IVXLC]+$',x) and r2i(x)==expect:
        # next nonblank must be caps title and following has verse
        q=k+1
        while not L[q].strip(): q+=1
        H[expect]=q; expect+=1
print('found',len(H))
keys=sorted(H)
rows=[]
for num,title,a in T:
    fline=None
    if num in H:
        q=H[num]; nxt=H.get(num+1,end)
        fline=pick_first(L[q:nxt])
    rows.append({'title':clean_title(re.sub(r'\s*\(_?c\._?.*?\)','',title)),'author':tc(a),'first_line':fline})
write_rows(52133,rows)
print([r for r in rows if not r['first_line']][:5])
sample(52133)
