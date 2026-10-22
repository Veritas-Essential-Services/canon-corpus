import sys,re; sys.path.insert(0,'.')
from lib import *
STOP=re.compile(r'^(DEFINITIONS|EXERCISES|NOTES?\.|Notes?\.--|NOTE\.|\[Illustration)')
def classify(body):
    lines=[l for l in body if l.strip() and not l.strip().startswith('[') and not l.startswith('\t') and not re.match(r'^\(\d+\)$',l.strip())]
    if not lines: return None
    lines=lines[:30]
    ind=sum(1 for l in lines if l[0].isspace())/len(lines)
    avg=sum(len(l.strip()) for l in lines)/len(lines)
    longc=sum(1 for l in lines if len(l.rstrip())>=66)/len(lines)
    low=sum(1 for l in lines if re.match(r'^[a-z]',re.sub(r'^\d+\.\s*','',l.strip())))/len(lines)
    return 'verse' if (longc<0.25 and low<0.2 and (avg<52 or ind>0.3)) else 'prose'
BIO=re.compile(r'^By [A-Z]|was born|\(b\. |\b1[5-9]\d\d-1[5-9]\d\d\b|\bb\. 1[5-9]\d\d')
def first_of(body):
    skip=False
    for l in body:
        x=l.strip()
        if skip:
            if not x: skip=False
            continue
        if BIO.search(x): skip=True; continue
        if not x or x.startswith('[') or l.startswith('\t') or (is_caps(x) and len(x)<60): continue
        x=re.sub(r'^\d+\.\s*','',x)
        return fl(x)
def content(blk):
    out=[]
    st=next((q for q,l in enumerate(blk) if re.match(r'^\s*1\.\s+\S',l)),None)
    if st is not None and st<80: blk=blk[st:]
    for l in blk:
        if STOP.match(l.strip()): break
        out.append(l)
    return out
def contents_authors(L,a,b):
    A={}
    for l in L[a:b]:
        m=re.match(r'^\s*(\d+)\.\s+(.+?)(?:\s{2,}(.+?))?(?:\s{2,}(\d+))?\s*$',l)
        if m:
            n=int(m.group(1)); au=m.group(3)
            if au and re.match(r'^\d+$',au): au=None
            if n in A: continue
            A[n]=(m.group(2).strip(),au.strip().rstrip('.') if au else None)
    return A
def styleB(pg, first_title):
    L,s=load(pg)
    ct=next(k for k,l in enumerate(L) if re.search(r'TITLE\.\s+AUTHOR',l))
    H0=next(k for k in range(ct+20,len(L)) if re.match(r'^(I|1)\.\s+'+re.escape(first_title.upper()),L[k]))
    A=contents_authors(L,ct,H0)
    H=[(k,m) for k in range(H0,len(L)) if (m:=re.match(r'^([IVXLC]+|\d+)\.\s+(.+?)\.?\s*(\(\d+\))?\s*$',L[k])) and (m.group(1).isdigit() or r2i(m.group(1))) and is_caps(m.group(2))]
    rows=[]
    for j,(k,m) in enumerate(H):
        nxt=H[j+1][0] if j+1<len(H) else len(L)
        body=content(L[k+1:nxt])
        # skip leading author line / note lines in caps or italic
        kind=classify(body)
        if not kind: continue
        n=int(m.group(1)) if m.group(1).isdigit() else r2i(m.group(1))
        TA={norm(t):au for t,au in A.values()}
        a=TA.get(norm(m.group(2)))
        if a is None and norm(A.get(n,('',None))[0])==norm(m.group(2)): a=A[n][1]
        r={'title':clean_title(m.group(2)),'author':tc(a) if a else None,'first_line':first_of(body)}
        if kind=='prose': r['kind']='prose'
        rows.append(r)
    write_rows(pg,rows)
    print(pg,'verse',sum(1 for r in rows if 'kind' not in r),'prose',sum(1 for r in rows if 'kind' in r),'contents',len(A))
def styleA(pg):
    L,s=load(pg)
    H=[k for k in range(s,len(L)) if re.match(r'^LESSON [IVXLC]+\.?\s*$',L[k].strip())]
    rows=[]
    for j,k in enumerate(H):
        nxt=H[j+1] if j+1<len(H) else len(L)
        blk=L[k+1:nxt]
        # title: first caps col0 line not in brackets, after vocab
        ti=None;inbr=False
        for q,l in enumerate(blk):
            x=l.strip()
            if inbr:
                if ']' in x: inbr=False
                continue
            if x.startswith('['):
                if ']' not in x: inbr=True
                continue
            if '\t' in l or re.search(r'READER|ECLECTIC SERIES',x): continue
            if x and is_caps(x) and len(x)<70 and re.search(r'[A-Z]{3}',x) and not re.search(r"\w'\w|\s{3,}",x): ti=q;break
        if ti is None: continue
        body=content(blk[ti+1:])
        kind=classify(body)
        if not kind: continue
        r={'title':clean_title(blk[ti].strip()),'author':None,'first_line':first_of(body)}
        if kind=='prose': r['kind']='prose'
        rows.append(r)
    write_rows(pg,rows)
    print(pg,'verse',sum(1 for r in rows if 'kind' not in r),'prose',sum(1 for r in rows if 'kind' in r))
styleA(14668); styleA(14766)
styleB(14880,'PERSEVERANCE'); styleB(15040,'THE GOOD READER'); styleB(16751,'ANECDOTE OF THE DUKE')
for pg in (14668,14880,15040,16751):
    import json
    rr=[json.loads(l) for l in open(f'{A}/rows/{pg}.jsonl')]
    print([ (r['title'],r['author'],r['first_line']) for r in rr if 'kind' not in r][:6])
def first_reader(pg):
    L,s=load(pg)
    H=[k for k in range(s,len(L)) if re.match(r'^LESSON [IVXLC]+\.?\s*$',L[k].strip())]
    rows=[]
    for j,k in enumerate(H):
        nxt=H[j+1] if j+1<len(H) else len(L)
        blk=L[k+1:nxt]
        nb=[q for q,l in enumerate(blk) if l.strip()]
        if not nb: continue
        body=[l for l in blk[nb[0]+1:]]
        # drop illustrations
        out=[];inb=False
        for l in body:
            x=l.strip()
            if inb:
                if ']' in x: inb=False
                continue
            if x.startswith('['):
                if ']' not in x: inb=True
                continue
            if STOP.match(x) or x.startswith('End of'): break
            out.append(l)
        kind=classify(out)
        if not kind: continue
        r={'title':'Lesson '+L[k].strip().split()[1].rstrip('.'),'author':None,'first_line':first_of(out)}
        if kind=='prose': r['kind']='prose'
        rows.append(r)
    write_rows(pg,rows)
    print(pg,'verse',sum(1 for r in rows if 'kind' not in r),'prose',sum(1 for r in rows if 'kind' in r))
    print([r for r in rows if 'kind' not in r][:8])

