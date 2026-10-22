import sys,re; sys.path.insert(0,'.'); from common import *
pg=32415; L=load(pg).split('\n')
st=[k for k,l in enumerate(L) if l.startswith('FIRST CLASS')][0]
en=[k for k,l in enumerate(L) if k>st and re.match(r'^\s*INDEX\.?\s*$',l)]
en=en[0] if en else len(L)
rows=[]
for k in range(st,en):
    if re.fullmatch(r'[IVXLCDM]+\.',L[k].strip()) and not L[k].startswith(' '):
        fl=None
        inb=False
        for j in range(k+1,k+40):
            x=L[j].strip()
            if inb:
                if ']' in x: inb=False
                continue
            if x.startswith('['):
                if ']' not in x: inb=True
                continue
            if not x: continue
            fl=x; break
        rows.append({'title':fl,'author':None,'first_line':fl})
print(len(rows), en)
write(pg,rows)
