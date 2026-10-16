import sys,re; sys.path.insert(0,'.'); from common import *
pg=23794; L=load(pg).split('\n')
toc=[]
for l in L:
    m=re.match(r'^_(.+?)_\s+(\d+)\s*$',l.strip())
    if m: toc.append(m.group(1).strip())
rows=[{'title':t,'author':None,'first_line':t} for t in toc]
write(pg,rows)
