import sys,re; sys.path.insert(0,'.'); from common import *
pg=54530; L=load(pg).split('\n')
st=[k for k,l in enumerate(L) if l.strip()=='THE BUDGET'][0]
rows=[]; prevblank=True
for k in range(st+1,len(L)):
    x=L[k]
    if 'FINIS' in x or 'THE END' in x: break
    if x.startswith('[Illustration'): prevblank=True; continue
    if not x.strip(): continue
    if prevblank: rows.append({'title':x.strip(),'author':None,'first_line':x.strip()})
    prevblank=False
print(rows[-3:])
write(pg,rows)
