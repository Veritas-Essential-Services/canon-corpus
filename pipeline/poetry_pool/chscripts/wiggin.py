import sys,re; sys.path.insert(0,'.'); from common import *
pg=int(sys.argv[1]); endmark=sys.argv[2]
T=load(pg); L=T.split('\n')
ci=[k for k,l in enumerate(L) if l.strip()=='CONTENTS'][0]
toc=[]; k=ci+1
while not L[k].startswith(endmark):
    l=L[k]
    m=re.match(r'^\s{2,}(.+?)\s{2,}([ivxl\d]+)\s*$',l)
    if m:
        body=m.group(1)
        # wrapped lines: previous line continuation
        mm=re.match(r'^(.*?)\.? (?:By )?(_[^_]+_|"_[^"]+"|"[^"]+")\.?$',body)
        if mm: t,a=mm.group(1),mm.group(2)
        else: t,a=body,None
        a=a.strip('_"').strip('_') if a else None
        toc.append([t.strip().rstrip('.'),a])
    elif re.match(r'^\s{2,}\S',l) and k+1<len(L) and re.match(r'^\s{4,}\S.*\s{2,}[\divxl]+\s*$',L[k+1]):
        # continuation: join
        L[k+1]='  '+l.strip()+' '+L[k+1].strip()
    k+=1
bstart=k
if pg==22922: toc=toc[1:]
idx=seq_find(L,ci+1+len(toc),[t for t,a in toc],match=lambda l,t: l.startswith('_') and norm(l).startswith(norm(t)) )
rows=[]
for (t,a),ix in zip(toc,idx):
    fl=verse_after(L,ix,minindent=3) if ix is not None else None
    if a in ('Anonymous','Unknown','Old Rhyme','Old Song','Author Unknown','Old Ballad','Old Ballad.'): a=None
    rows.append({'title':t,'author':a,'first_line':fl})
if pg==22922:
    for r,ix in zip(rows,idx):
        if r['title']=='The Child at Bethlehem': r['first_line']=verse_after(L,[i for i,l in enumerate(L) if l.strip()=='_At Bethlehem_'][0])
if pg==22922:
    for r in rows:
        if r['title']=='LILLIPUT NOTICE': r['title']='Lilliput Notice'; r['first_line']='Said I to myself, here\'s a chance for me'
print('toc',len(toc),'missing',[t for (t,a),x in zip(toc,idx) if x is None][:30])
write(pg,rows)
