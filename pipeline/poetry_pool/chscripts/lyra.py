import sys,re; sys.path.insert(0,'.'); from common import *
T=load(19316); L=T.split('\n')
ci=[i for i,l in enumerate(L) if l.strip()=='CONTENTS'][0]
bi=[i for i,l in enumerate(L) if l.strip()=='LYRA HEROICA' and i>ci][0]
auth=None; toc={}
for l in L[ci+1:bi]:
    m=re.match(r'^  ([A-Z][A-Z .,\'\-]+?)(?: \(.*\))?\.?(?: and)?$',l)
    if m and not re.match(r'^\s+[IVXLC]+\.',l):
        auth=tcase(m.group(1).strip().rstrip('.')); continue
    if re.match(r'^  [A-Z].*\)\.?$',l) and 'and' not in l: pass
    m=re.match(r'^\s+([IVXLC]+)\. (.+?)\s{2,}\d+\s*$',l) or re.match(r'^\s+([IVXLC]+)\. (.+?)\s*$',l)
    if m: toc[m.group(1)]=(tcase(m.group(2).strip()),auth)
# body
rows=[]
for i in range(bi,len(L)):
    s=L[i].strip()
    if roman_ok(s) and s in toc and L[i].startswith('  ') and not L[i+1].strip():
        title,a=toc[s]
        # skip title line
        t,j=firstline_after(L,i)
        fl,k=firstline_after(L,j)
        while fl and fl.upper()==fl and re.search('[A-Z]',fl): fl,k=firstline_after(L,k)
        if a=='Ballads': a=None
        if s=='I': a='William Shakespeare and Michael Drayton'
        rows.append({'title':title,'author':a,'first_line':fl,'num':s})
print(len(toc),len(rows))
seen=set(); out=[]
for r in rows:
    if r['num'] in seen: continue
    seen.add(r['num']); out.append(r)
write(19316,out)
