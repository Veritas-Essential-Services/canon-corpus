import sys,re; sys.path.insert(0,'.'); from common import *
T=load(46515); L=T.split('\n')
ci=[k for k,l in enumerate(L) if l.strip()=='CONTENTS'][0]
toc={}; auth=None; k=ci+1; order=[]
while True:
    l=L[k]
    if re.match(r'^  \S',l):
        if 'INTRODUCTION' in l or l.strip()=='PAGE': k+=1; continue
        a=l.strip().rstrip(':')
        a=re.sub(r',\s*[\d?-]+.*$','',a)
        if ',' in a:
            last,first=a.split(',',1); a=first.strip()+' '+last.strip()
        auth=None if a.upper().startswith('ANONYMOUS') else tcase(a)
    m=re.match(r'^    (\S.*?)\s{2,}(\d+)\s*$',l)
    if m: toc.setdefault(norm(m.group(1)),[]).append(auth); order.append((int(m.group(2)),m.group(1)))
    k+=1
    if k>ci+5 and l.strip()=='' and L[k].strip()=='' and L[k+1].strip()=='' and L[k+2].strip()=='' : break
print('toc entries',len(order))
end=[k for k,l in enumerate(L) if 'INDEX OF FIRST LINES' in l][0]

heads=[i for i in range(k,end) if re.fullmatch(r'_([^_]+)_',L[i].strip()) and L[i].startswith('_') and L[i+1].strip()=='']
rows=[]
def strip_art(x): return re.sub(r'^(the|an|a)(?=[a-z])','',x)
for n,i in enumerate(heads):
    t=L[i].strip().strip('_')
    fl=verse_after(L,i)
    key=None
    nt=norm(t)
    for kk,v in toc.items():
        if not v: continue
        if kk==nt or strip_art(kk)==strip_art(nt) or (len(nt)>8 and (kk.startswith(nt) or nt.startswith(kk))): key=kk;break
    if key is None and fl:
        nf=norm(fl)
        for kk,v in toc.items():
            if v and len(kk)>=8 and norm(fl+' '+(verse_after(L,L.index(L[i]))or'')).startswith(kk[:12]) : key=kk;break
    if key:
        a=toc[key].pop(0); title=tcase(t) if nt==key or strip_art(nt)==strip_art(key) else tcase(t)
    else:
        a='?'
    nxt=heads[n+1] if n+1<len(heads) else end
    sig=None
    for j in range(nxt-1,i,-1):
        x=L[j]
        if x.strip() and len(x)-len(x.lstrip())>=15 and x.strip().upper()==x.strip(): sig=x.strip().rstrip('.'); break
        if x.strip() and len(x)-len(x.lstrip())<15: break
    rows.append({'title':tcase(t),'author':a,'sig':sig,'first_line':fl})
print('rows',len(rows),'unused',[x for x,v in toc.items() if v])
for r in rows:
    if r['author']=='?': r['author']=None; print('nokey',r)
rows=[r for r in rows if r['title'] not in ('First Voice','Second Voice','September 1814')]
for r in rows:
    if r['author'] and ('Minstrelsy' in r['author'] or 'Reliques' in r['author']): r['author']=None
    if r['author'] and 'HEYWOOD' in r['author']: r['author']='Thomas Heywood'
    if r['title']=='The Beleaguered City': r['author']='Henry Wadsworth Longfellow'
    if r['title']=='On the Departure of Sir Walter Scott': r['author']='William Wordsworth'
write(46515,rows)
