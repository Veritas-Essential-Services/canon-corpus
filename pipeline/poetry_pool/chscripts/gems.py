import sys,re; sys.path.insert(0,'.'); from common import *
pg=11023
L=open(f'{ANTH}/texts/{pg}.txt',encoding='utf-8',errors='replace').read().replace('\r','').split('\n')
heads=[i for i,l in enumerate(L) if re.fullmatch(r"[A-Z][A-Z ,.'!?;-]{3,}",l) and 60<i<550]
rows=[]
for n,i in enumerate(heads):
    end=heads[n+1] if n+1<len(heads) else 550
    sig=[L[j].strip() for j in range(i+1,end) if re.fullmatch(r'\s{10,}[A-Z][\w. ]+',L[j])]
    rows.append({'title':tcase(L[i].rstrip('.')),'author':None,'first_line':verse_after(L,i,minindent=0),'sig':sig})
    print(rows[-1])
write(pg,rows)
