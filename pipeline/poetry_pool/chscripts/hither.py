import sys,re; sys.path.insert(0,'.'); from common import *
pg=62119; L=load(pg).split('\n')
heads=[]; expect=1; gaps=[]
for i,l in enumerate(L):
    m=re.match(r'^\s{0,6}~?(\d+)~?\s{3,}(\S.*\S)\s*$',l)
    if m and expect<=int(m.group(1))<expect+6 and re.search(r'[A-Z]{2}',m.group(2)) and m.group(2).upper()==m.group(2):
        heads.append((i,int(m.group(1)),m.group(2))); gaps.extend(range(expect,int(m.group(1)))); expect=int(m.group(1))+1
print('poems',len(heads),heads[-1],'gaps',gaps)
rows=[]
for n,(i,num,t) in enumerate(heads):
    end=heads[n+1][0] if n+1<len(heads) else min(len(L),i+400)
    sig=None
    for j in range(i+1,end):
        x=L[j]
        if len(x)-len(x.lstrip())>=25 and x.strip() and not re.search(r'[a-z]',x) and re.search(r'[A-Z]{2}',x) and not x.strip().startswith('['):
            sig=x.strip()
    # title may wrap to next line
    t2=t
    nx=L[i+1]
    if nx.strip() and len(nx)-len(nx.lstrip())>=15 and nx.strip().upper()==nx.strip() and re.search('[A-Z]',nx): t2=t+' '+nx.strip()
    a=tcase(sig) if sig else None
    rows.append({'title':tcase(t2),'author':a,'first_line':verse_after(L,i+ (1 if t2!=t else 0),minindent=2)})
write(pg,rows)
import collections
print(collections.Counter(r['author'] for r in rows).most_common(15))
