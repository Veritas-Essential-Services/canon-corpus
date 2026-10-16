import sys,re; sys.path.insert(0,'.'); from common import *
pg=30418; L=load(pg).split('\n')
st=[k for k,l in enumerate(L) if l.strip()=='TRADITIONAL NURSERY SONGS.'][0]
en=[k for k,l in enumerate(L) if l.strip()=='THE END.'][0]
chunks=[]; cur=[]
for l in L[st+1:en]:
    if not l.strip() or l.strip().startswith('['):
        if cur: chunks.append(cur); cur=[]
        continue
    cur.append(l.strip())
if cur: chunks.append(cur)

chunks=[c for c in chunks if re.search('[a-z]',c[0]) and not c[0].startswith('_')]

import json
json.dump([c[0] for c in chunks],open('summerly_chunks.json','w'),ensure_ascii=False,indent=0)
