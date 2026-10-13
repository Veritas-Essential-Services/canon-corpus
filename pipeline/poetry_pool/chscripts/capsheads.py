import sys,re; sys.path.insert(0,'.'); from common import *
# usage: pg body_start_regex(last occurrence before poems; uses first match after skip) min_indent max_indent [end_regex]
pg=int(sys.argv[1]); bs=sys.argv[2]; mi=int(sys.argv[3]); ma=int(sys.argv[4]); er=sys.argv[5] if len(sys.argv)>5 else None
L=load(pg).split('\n')
st=[k for k,l in enumerate(L) if re.search(bs,l)][-1]
en=len(L)
if er:
    e=[k for k,l in enumerate(L) if k>st and re.search(er,l)]
    if e: en=e[0]
rows=[]
for k in range(st+1,en):
    l=L[k]; ind=len(l)-len(l.lstrip())
    s=l.strip()
    if mi<=ind<=ma and s and not re.search(r'[a-z]',s) and re.search(r'[A-Z]{2}',s) and not s.startswith('[') and not L[k-1].strip() :
        fl=verse_after(L,k,minindent=0)
        rows.append({'title':tcase(s.rstrip('.')),'author':None,'first_line':fl})
write(pg,rows)
for r in rows[:4]+rows[-3:]: print(r)
