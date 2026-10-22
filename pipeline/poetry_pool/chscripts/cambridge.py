import sys,re; sys.path.insert(0,'.'); from common import *
T=load(50994); L=T.split('\n')
cis=[k for k,l in enumerate(L) if l.strip()=='CONTENTS']
ais=[k for k,l in enumerate(L) if l.strip()=='INDEX OF AUTHORS']
rows=[]
for part,(ci,ai) in enumerate(zip(cis,ais)):
    toc=[]; prev=None; pend=''
    for l in L[ci+1:ai]:
        if 'INDEX OF' in l or 'PREFACE' in l or not l.strip(): continue
        if re.match(r'^ {4,}',l) is None: continue
        m=re.match(r'^ {4,}(?:\d+\. )?(\S.*?)\s{2,}(?:(_[^_]+_|”)\s+)?(\d+)\s*$',l)
        if not m:
            m2=re.match(r'^ {4,}(?:\d+\. )?(\S.*?)\s+(_[^_]+_|”)\s+(\d+)\s*$',l)
            m=m2
        if m:
            t=(pend+' '+m.group(1)).strip(); pend=''
            a=m.group(2)
            mm=re.match(r'^(.*?) (_[^_]+_)$',t)
            if mm and not a: t,a=mm.group(1),mm.group(2)
            mm=re.match(r'^(.*?) ([A-Z]\.)$',t)
            if mm and a and a!='”': t=mm.group(1); a=mm.group(2)+' '+a.strip('_')
            if a=='”': a=prev
            elif a: a=a.strip('_')
            toc.append((t,a,int(m.group(3))))
            prev=a
        else:
            if not re.fullmatch(r'\d+\. _.*_',l.strip()) and l.strip().upper()!=l.strip(): pend=l.strip()
    pages={}; full=[]
    k=ai+1
    while 'INDEX OF FIRST LINES' not in L[k]:
        m=re.match(r'^  (\S.*?)\s{2,}([\d, \-]+)\s*$',L[k])
        if m:
            a=m.group(1).strip()
            if ',' in a:
                last,first=a.split(',',1); a=first.strip()+' '+last.strip()
            if a=='Anonymous': a=None
            ps=[]
            for p in m.group(2).split(','):
                p=p.strip()
                if '-' in p: x,y=p.split('-'); ps+=list(range(int(x),int(y)+1))
                elif p: ps.append(int(p))
            for q in ps: pages.setdefault(q,[]).append(a)
            full.append((a,ps))
        k+=1
    def resolve(ab,p):
        cands=[a for a,ps in full if p in ps]
        if ab:
            last=ab.split()[-1].lower()
            c=[a for a in cands if a and last in a.lower()]
            if len(c)==1: return c[0]
            c=[a for a,ps in full if a and last in a.lower()]
            if len(c)==1: return c[0]
            return ab
        if len(set(cands))==1: return cands[0]
        return None
    idx=seq_find(L,ai-len(toc)-60 if False else ci+5,[t for t,a,p in toc],match=lambda l,t: l.strip().upper()==l.strip() and len(l.strip())>2 and (norm(re.sub(r'^\d+\. ','',l))==norm(t) or (len(norm(t))>=10 and norm(re.sub(r'^\d+\. ','',l)).startswith(norm(t)[:10])) or (len(norm(t))>=10 and norm(t) in norm(l))),window=20000)
    for (t,a,p),ix in zip(toc,idx):
        rows.append({'title':t,'author':resolve(a,p),'first_line':verse_after(L,ix,minindent=2) if ix is not None else None})
    print('part',part,len(toc),'missing',[t for (t,a,p),x in zip(toc,idx) if x is None])
write(50994,rows)
