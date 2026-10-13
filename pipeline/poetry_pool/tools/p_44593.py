import sys,re; sys.path.insert(0,'.')
from lib import *
L,s=load(44593)
st=600
end=next(k for k in range(st,len(L)) if L[k].strip().startswith('INDEX OF FIRST LINES'))
H=[(k,m) for k in range(st,end) if (m:=re.match(r'^_(\d+)\.\s+(.+?)_?\s*$',L[k]))]
rows=[]
for j,(k,m) in enumerate(H):
    nxt=H[j+1][0] if j+1<len(H) else end
    rows.append({'title':clean_title(m.group(2).replace('_','')),'author':None,'first_line':pick_first(L[k+1:nxt]),'n':int(m.group(1))})
for r in rows:
    if r['title']=='The Nut-Brown Maid': r['first_line']='Be it right or wrong, these men among'
print(len(rows),[r['n'] for r in rows][-3:], sorted(set(range(1,177))-{r['n'] for r in rows}))
write_rows(44593,rows)
print([r for r in rows if not r['first_line']])
sample(44593,8)
