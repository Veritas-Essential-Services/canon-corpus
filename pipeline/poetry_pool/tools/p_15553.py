import sys,re; sys.path.insert(0,'.')
from lib import *
L,s=load(15553)
st=next(k for k,l in enumerate(L) if l.strip()=='CONTENTS.')
st=next(k for k in range(st,len(L)) if L[k].startswith('BOOK FIRST'))
end=next(k for k,l in enumerate(L) if l.strip() in ('NOTES.','NOTES') and k>st)
def is_author(l,k): return bool(l) and not l[0].isspace() and is_caps(l) and len(l)<60 and k>st+1
def is_title(l,k):
    return bool(l.strip()) and not l[0].isspace() and not is_caps(l) and not L[k-1].strip() and (not L[k+1].strip() or not L[k+1][0].isspace() and L[k+1].strip())
rows=parse_flat(L,st,end,is_title,is_author)
rows=[r for r in rows if r['first_line'] and not r['title'].startswith('[')]
for r in rows: r['title']=clean_title(r['title']); r['author']=tc(r['author'])
print(rows[:3])
write_rows(15553,rows)
print('noau',[r['title'] for r in rows if not r['author']][:20])
sample(15553)
