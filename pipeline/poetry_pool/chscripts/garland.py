import sys,re; sys.path.insert(0,'.'); from common import *
pg=27441; T=load(pg); L=T.split('\n')
ci=[k for k,l in enumerate(L) if l.strip()=='CONTENTS'][0]
toc=[]
k=ci+1
while True:
    m=re.match(r'^\s+([IVXLC]+) (\S.*)$',L[k])
    if m: toc.append((m.group(1),m.group(2).strip()))
    elif toc and L[k].strip() and not m: break
    k+=1
wi=[k for k,l in enumerate(L) if l.strip()=='INDEX OF WRITERS'][0]
amap={}
for l in L[wi+1:]:
    m=re.match(r'^  (\S.*?), ([IVXLC][IVXLC, ]*)\s*$',l)
    if m:
        name=m.group(1)
        parts=[p.strip() for p in name.split(',')]
        a=' '.join(parts[1:]+parts[:1]) if len(parts)>1 else name
        for n in m.group(2).split(','):
            if n.strip(): amap[n.strip()]=a
        lasta=a
    elif re.fullmatch(r'\s+[IVXLC][IVXLC, ]*',l) and amap:
        for n in l.split(','):
            if n.strip(): amap[n.strip()]=lasta
    elif l.strip().startswith('***') or 'End of' in l: break
# body: first poem has no numeral
bi=k
rows=[]; pos=bi
for num,t in toc:
    ix=None
    for i in range(pos,len(L)):
        if L[i].strip().startswith('_') and (norm(L[i])==norm(t) or norm(L[i])==norm(re.split(r',| supposed| Characteristic| Spoken',t)[0])):
            ix=i;break
    if ix is None:
        rows.append({'title':t,'author':amap.get(num),'first_line':None}); continue
    pos=ix+1
    rows.append({'title':t,'author':amap.get(num),'first_line':verse_after(L,ix)})
print(len(toc),len(amap),'missing',[r['title'] for r in rows if not r['first_line']],[r['title'] for r in rows if not r['author']][:20])
for r in rows:
    if r['author'] and r['author'].startswith('Old ') or r['author'] in ('Anonymous','Unknown'): r['author']=None
write(pg,rows)
