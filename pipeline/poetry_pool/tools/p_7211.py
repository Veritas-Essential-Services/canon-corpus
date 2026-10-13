import sys,re; sys.path.insert(0,'.')
from lib import *
from p_recit import classify
L,s=load(7211)
st=1066; end=next(k for k,l in enumerate(L) if l.strip()=='NOTES.' and k>st)
sect='prose'
H=[]
for k in range(st,end):
    x=L[k].strip(); ind=len(L[k])-len(L[k].lstrip())
    if re.match(r'^(PROSE|POETRY)\.?$',x) and ind>10: sect='prose' if x.startswith('PROSE') else 'verse'; continue
    m=re.match(r'^([IVXLC]+)\.\s*(.*)$',x)
    if m and ind>8 and r2i(m.group(1)) and (not m.group(2) or is_caps(m.group(2))):
        H.append((k,m.group(2),sect))
rows=[]
for j,(k,t,sect) in enumerate(H):
    nxt=H[j+1][0] if j+1<len(H) else end
    blk=L[k+1:nxt]
    q=0
    if not t:
        while q<len(blk) and not blk[q].strip(): q+=1
        t=blk[q].strip(); q+=1
        while q<len(blk) and blk[q].strip() and is_caps(blk[q]) and (len(blk[q])-len(blk[q].lstrip()))>8: t+=' '+blk[q].strip(); q+=1
    body=blk[q:]
    # cut section headers at end
    nb=[i for i,l in enumerate(body) if l.strip()]
    au=None
    for i in reversed(nb):
        l=body[i]
        if re.match(r'^(BOOK|STANDARD|RECENT|HUMOROUS|PROSE|POETRY|DIALOGUES|IN PROSE)',l.strip()) or (is_caps(l) and (len(l)-len(l.lstrip()))>15): continue
        if (len(l)-len(l.lstrip()))>=40 and len(l.strip())<50: au=l.strip(); body=body[:i]
        break
    kind=sect if sect=='verse' else (classify(body) if classify(body)=='prose' else 'prose')
    if kind=='prose':
        first=next((fl(l) for l in body if l.strip() and not l.strip().startswith(('[','('))),None)
    else: first=pick_first(body)
    r={'title':clean_title(t),'author':tc(au) if au else None,'first_line':first}
    if kind=='prose': r['kind']='prose'
    rows.append(r)
write_rows(7211,rows)
print('verse',sum(1 for r in rows if 'kind' not in r),'prose',sum(1 for r in rows if 'kind' in r),'noau',sum(1 for r in rows if not r['author']))
import random; random.seed(1)
for r in random.sample([r for r in rows if 'kind' not in r],10): print(r)
