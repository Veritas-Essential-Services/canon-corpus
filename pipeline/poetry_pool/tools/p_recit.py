import sys,re; sys.path.insert(0,'.')
from lib import *
def classify(body):
    lines=[l for l in body if l.strip() and not l.strip().startswith(('[','_','(')) and not is_caps(l)][:30]
    if not lines: return None
    longc=sum(1 for l in lines if len(l.rstrip())>=64)/len(lines)
    low=sum(1 for l in lines if re.match(r'^[a-z]',l.strip()))/len(lines)
    return 'verse' if (low<0.1 or (longc<0.3 and low<0.25)) else 'prose'
def generic(pg, st, end, maxind=0, byre=r'^(?:BY|By)\s+(.+?)\.?$', min_blanks=2, skip_titles=()):
    L,_=load(pg)
    H=[]
    for k in range(st,end):
        l=L[k]
        if not l.strip() or (len(l)-len(l.lstrip()))>maxind or not is_caps(l) or len(l.strip())>90: continue
        if any(not L[k-q].strip()=='' for q in range(1,min_blanks+1)): continue
        x=l.strip()
        if re.match(byre,x) or ROMAN.match(x) or x in skip_titles or re.match(r'^(CONTENTS|INDEX|PREFACE|THE END|FINIS|PART [IVX]+)',x): continue
        H.append(k)
    rows=[]
    for j,k in enumerate(H):
        nxt=H[j+1] if j+1<len(H) else end
        blk=L[k+1:nxt]
        title=L[k].strip(); q=0
        while q<len(blk) and blk[q].strip() and is_caps(blk[q]) and not re.match(byre,blk[q].strip()): title+=' '+blk[q].strip(); q+=1
        au=None
        for qq in range(q,min(q+6,len(blk))):
            mm=re.match(byre,blk[qq].strip())
            if mm: au=mm.group(1).strip().rstrip('.'); q=qq+1; break
        body=blk[q:]
        if au is None:
            nb=[l.strip() for l in body if l.strip()]
            if nb and nb[-1].startswith('_') and nb[-1].rstrip('.').endswith('_') and len(nb[-1])<60:
                au=nb[-1].strip('_. ').strip('_').strip()
                body=body[:max(i for i,l in enumerate(body) if l.strip())]
            elif nb and nb[-1].startswith('—') and len(nb[-1])<60: au=nb[-1].strip('—_ .')
        kind=classify(body)
        if not kind: continue
        if kind=='prose':
            first=next((fl(l) for l in body if l.strip() and not l.strip().startswith(('[','_','(')) and not is_caps(l)),None)
        else: first=pick_first(body)
        r={'title':clean_title(title),'author':tc(au) if au else None,'first_line':first}
        if kind=='prose': r['kind']='prose'
        rows.append(r)
    return rows
if __name__=='__main__':
    L,s=load(17378)
    st=next(k for k,l in enumerate(L) if l.strip()=='JOHN BULL AND HIS ISLAND.')-1
    end=len(L)
    rows=generic(17378,st,end)
    write_rows(17378,rows)
    print('verse',sum(1 for r in rows if 'kind' not in r),'prose',sum(1 for r in rows if 'kind' in r),'noau',sum(1 for r in rows if not r['author']))
    sample(17378,12)
