import sys,json; sys.path.insert(0,'.'); from common import *
c=json.load(open('summerly_chunks.json'))
CONT={3,17,18,22,40,48,53,54,55,106,109,110,111,113,124,125}|set(range(68,81))
rows=[{'title':x,'author':None,'first_line':x} for i,x in enumerate(c) if i not in CONT]
write(30418,rows)
