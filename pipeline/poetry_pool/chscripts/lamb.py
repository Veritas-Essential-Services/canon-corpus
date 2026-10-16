import sys,re; sys.path.insert(0,'.'); from common import *
pg=68359; L=load(pg).split('\n')
ci=[k for k,l in enumerate(L) if 'Illustration: CONTENTS' in l][0]
toc=[]; k=ci+1
while k<ci+300:
    l=L[k]
    m=re.match(r'^\s+([IVXLC]+)\. (.+?)(?:\s{2,}(\d+))?\s*$',l)
    if m: toc.append([m.group(1),m.group(2).strip()])
    elif toc and re.match(r'^\s{10,}\S',l):
        toc[-1][1]+=' '+re.sub(r'\s{2,}\d+\s*$','',l).strip()
    elif toc and l.strip() and not l.startswith(' '): break
    k+=1
pos=k; rows=[]
for num,t in toc:
    ix=None
    for i in range(pos,len(L)):
        if L[i].strip()==num and not L[i].startswith(' '): ix=i; break
    if ix: pos=ix+1
    rows.append({'title':t,'author':'Charles and Mary Lamb','first_line':verse_after(L,ix,minindent=2) if ix else None})
print(len(toc),[r['title'] for r in rows if not r['first_line']])
write(pg,rows)
for r in rows[:3]+rows[-2:]: print(r)
