import sys,re; sys.path.insert(0,'.'); from common import *
pg=72625
T=load(pg); L=T.split('\n')
ai=[k for k,l in enumerate(L) if 'INDEX OF AUTHORS AND BIBLIOGRAPHY' in l][0]
ents=[]; auth=None; k=ai+2
while k<len(L):
    l=L[k]
    if re.match(r'^  [A-Z][A-Z .,\-]+?[A-Z.]( From .*)?$',l) and not re.search(r'\d\s*$',l):
        a=re.sub(r' From .*$','',l.strip())
        if ',' in a: last,first=a.split(',',1); a=first.strip()+' '+last.strip()
        auth=None if a=='ANONYMOUS' else tcase(a)
    m=re.match(r'^  (\S.*?)\s{2,}(\d+)\s*$',l)
    if m: ents.append((int(m.group(2)),m.group(1).strip(),auth))
    if len(ents)>=10 and l.strip() and not m and re.match(r'^[A-Z\[]',l): break
    k+=1
ents.sort(key=lambda e:e[0])
print(len(ents),ents[:3])
heads=[i for i in range(k,len(L)) if L[i].strip() and L[i].strip().upper()==L[i].strip() and re.search('[A-Z]{3}',L[i]) and '[' not in L[i]]
used=set(); rows=[]
for p,t,a in ents:
    ix=None
    for i in heads:
        if i in used: continue
        if norm(L[i])==norm(t) or norm(L[i]).endswith(norm(t)) or norm(t).endswith(norm(L[i])) and len(norm(L[i]))>5:
            ix=i; used.add(i); break
    rows.append({'title':t,'author':a,'first_line':verse_after(L,ix,minindent=0) if ix else None})
print('missing',[r['title'] for r in rows if not r['first_line']])
write(pg,rows)
