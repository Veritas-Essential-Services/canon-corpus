import sys,re; sys.path.insert(0,'.')
from lib import *
from p_recit import generic
L,s=load(57018)
ce=max(k for k in range(s,s+500) if re.search(r'\s\d+\s*$',L[k]) and '  ' in L[k].strip())
end=len(L)
rows=generic(57018,ce+1,end)
write_rows(57018,rows)
print('verse',sum(1 for r in rows if 'kind' not in r),'prose',sum(1 for r in rows if 'kind' in r),'noau',sum(1 for r in rows if not r['author']))
for r in rows[-8:]: print(r)
sample(57018,8)
