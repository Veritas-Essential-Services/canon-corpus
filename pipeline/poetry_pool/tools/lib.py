import re, json, os, sys
A='/tmp/claude-0/-home-claude-canon-corpus/23227e40-804c-5046-9833-e82b45c2f7aa/scratchpad/anth'
def load(i):
    b=open(f'{A}/texts/{i}.txt','rb').read()
    try: t=b.decode('utf-8')
    except UnicodeDecodeError: t=b.decode('cp1252',errors='replace')
    t=t.replace('\r','').replace('﻿','')
    L=t.split('\n')
    s=next((k for k,l in enumerate(L) if re.search(r'\*\*\* ?START OF',l)),0)
    e=next((k for k,l in enumerate(L) if re.search(r'\*\*\* ?END OF',l) or l.startswith('End of the Project Gutenberg') or l.startswith('End of Project Gutenberg')),len(L))
    return L[:e], s
def norm(s): return re.sub(r'[^a-z0-9]','',re.sub(r'\[(\d+|[A-Z])\]','',s).lower())
SMALL={'of','the','and','de','von','van','la','le','du','da','del','der','y'}
def tc(name):
    if name is None: return None
    name=name.strip().strip('_').strip().rstrip('.,;:').strip()
    if not name: return None
    # "LAST, First" -> "First Last"
    m=re.match(r'^([^,]+),\s*([^,]+)$',name)
    if m and not re.search(r'\b(jr|sr|in|from|earl|lord|duke|bishop|of|esq|countess|marquis|baron|lady|dean|viscount|d\.d|ll\.d|m\.d)\b',m.group(2).lower()) and len(m.group(2).split())<=4:
        name=m.group(2)+' '+m.group(1)
    if name.isupper() or name==name.upper():
        out=[]
        for k,w in enumerate(re.split(r'(\s+|-)',name.lower())):
            if k>0 and w in SMALL: out.append(w)
            elif re.match(r"^(mc|mac)(\w)",w) and len(w)>3 and w.startswith('mc'): out.append('Mc'+w[2:].capitalize())
            elif "'" in w and len(w)>2 and w[1]=="'": out.append(w[0].upper()+"'"+w[2:].capitalize())
            else: out.append(w[:1].upper()+w[1:])
        name=''.join(out)
        name=re.sub(r'\b([a-z])\.',lambda m:m.group(1).upper()+'.',name)
    name=re.sub(r'\s+',' ',name)
    return name
def clean_title(t):
    t=re.sub(r'\[(\d+|[A-Za-z])\]','',t)
    if t.count('"')%2==1: t=t+'"' if t.lstrip().startswith('"') else t
    t=re.sub(r'\s+',' ',t.strip().strip('_').strip().strip('=').strip()).rstrip('.').strip()
    if t.isupper():
        words=t.lower().split(' ')
        t=' '.join((w if (k>0 and w in {'a','an','the','of','and','in','on','to','at','for','by','with','from','or','o\'er','upon','into'}) else w[:1].upper()+w[1:]) for k,w in enumerate(words))
        t=re.sub(r'\b(i|ii|iii|iv|v|vi|vii|viii|ix|x)\b',lambda m:m.group(1).upper(),t)
    return t
def fl(line):
    if line is None: return None
    s=line.strip().strip('_').strip()
    s=re.sub(r'\s{3,}\d+$','',line.rstrip()).strip().strip('_').strip() if re.search(r'\s{3,}\d+$',line.rstrip()) else s
    s=re.sub(r'\[(\d+|[A-Z])\]','',s)
    s=re.sub(r'\s+',' ',s).strip()
    return s or None
def write_rows(pg,rows):
    os.makedirs(f'{A}/rows',exist_ok=True)
    with open(f'{A}/rows/{pg}.jsonl','w',encoding='utf-8') as f:
        for k,r in enumerate(rows,1):
            d={'pg_id':pg,'title':r['title'],'author':r.get('author'),'first_line':r.get('first_line'),'order':k}
            if r.get('kind'): d['kind']=r['kind']
            f.write(json.dumps(d,ensure_ascii=False)+'\n')
    print(pg,len(rows),'rows')
def sample(pg,n=10):
    import random
    rows=[json.loads(l) for l in open(f'{A}/rows/{pg}.jsonl',encoding='utf-8')]
    random.seed(pg)
    for r in random.sample(rows,min(n,len(rows))): print(r)
ROMAN=re.compile(r'^(PART\s+)?[IVXLC]+\.?$|^\d+\.?$',re.I)
def is_caps(x):
    letters=re.sub(r'[^A-Za-z]','',x)
    return len(letters)>=2 and letters.isupper()
def pick_first(blk, use_indent=True, skip=None):
    """blk: raw lines. Return first verse line."""
    lines=[l for l in blk]
    ind=[len(l)-len(l.lstrip()) for l in lines if l.strip() and re.search('[a-z]',l) and not l.strip().startswith(('_','[')) and not is_caps(l)]
    base=min(ind) if ind else 0
    in_ital=False; in_br=False
    for qi,l in enumerate(lines):
        x=l.strip()
        if not x: continue
        if in_ital:
            if x.count('_')%2==1: in_ital=False
            continue
        if x.startswith('_') and x.count('_')%2==1: in_ital=True; continue
        if x.startswith('_') and x.count('_')%2==0: continue
        if in_br:
            if ']' in x or ')' in x: in_br=False
            continue
        if x.startswith('[') or x.startswith('{'):
            if ']' not in x and '}' not in x: in_br=True
            continue
        if x.startswith('(') and (x.startswith('(_') or len(x)>45 and not x.endswith((',',';')) or x.endswith(')')):
            if ')' not in x: in_br=True
            continue
        if ROMAN.match(x) or re.match(r'^[\d\s,.\-–]+$',x) or re.match(r'^\(?\d{4}\)?\.?$',x): continue
        if is_caps(x): continue
        if len(x)<30 and re.match(r'^(c\.|circa|about|before|after|written|published)?\s*\d{3,4}\b',x,re.I): continue
        if len(x)<45 and re.search(r'\b1[2-9]\d\d\b',x) and not re.search(r'[;:!?]$',x): continue
        if skip and skip(x): continue
        if re.match(r'^(From|Fragment|Extract|Selected|Air|Tune)\b.{0,60}$',x) and not re.search(r'[,;:!?]$',x) and (qi+1>=len(lines) or not lines[qi+1].strip()): continue
        if use_indent and (len(l)-len(l.lstrip()))>base+4 and (qi+1>=len(lines) or not lines[qi+1].strip()): continue
        return fl(x)
    return None
def locate(L, start, titles, end=None, window=6000, match=None, maxind=None, fuzzy=True):
    """Find each title's heading line in order. Returns list of index|None."""
    import difflib
    end=end or len(L)
    out=[];pos=start
    N=[norm(l) for l in L]
    ok=[(maxind is None or (len(l)-len(l.lstrip()))<=maxind) and bool(l.strip()) for l in L]
    for t in titles:
        nt=norm(t); found=None
        if nt:
            hi=min(end,pos+window)
            for test in (1,2,3,4,5):
                for k in range(pos,hi):
                    if not ok[k]: continue
                    n=N[k]
                    if test==1 and (n==nt or (match and match(L[k],t))): found=k
                    elif test==2 and len(nt)>=8 and n.startswith(nt): found=k
                    elif test==3 and len(n)>=6 and nt.startswith(n) and k+1<len(L) and (n+N[k+1]).startswith(nt[:len(n)+min(5,len(nt)-len(n))]) and nt.startswith((n+N[k+1])[:len(nt)]): found=k
                    elif test==3 and len(n)>=6 and nt.startswith(n) and k+2<len(L) and not N[k+1] and nt.startswith((n+N[k+2])[:len(nt)]) and len(n+N[k+2])>=len(nt)*0.9: found=k
                    elif test==4 and fuzzy and len(nt)>=10 and abs(len(n)-len(nt))<8 and difflib.SequenceMatcher(None,n,nt).ratio()>0.85: found=k
                    elif test==5 and fuzzy and len(nt)>=14 and len(n)>=10:
                        mt=difflib.SequenceMatcher(None,n,nt).find_longest_match(0,len(n),0,len(nt))
                        if mt.size>=0.7*len(nt): found=k
                    if found is not None: break
                if found is not None: break
        out.append(found)
        if found is not None: pos=found+1
    return out
def from_located(L, idx, end, skip=None, extra_skip_lines=0):
    """first lines for located headings; block from heading+1 to next found heading."""
    found=[k for k in idx if k is not None]
    res=[]
    for k in idx:
        if k is None: res.append(None); continue
        nxt=next((q for q in found if q>k),end)
        res.append(pick_first(L[k+1:nxt],skip=skip))
    return res
def parse_flat(L, st, end, is_title, is_author, author_after=True, title_join=True):
    """Headings & authors identified by predicates on (line, k). Returns rows."""
    rows=[];cur=None
    k=st
    while k<end:
        l=L[k]
        if is_author(l,k):
            a=l.strip()
            if author_after:
                if cur is not None and cur.get('author') is None: cur['author']=a
            else:
                pending_author=a
                globals()['_pa']=a
        elif is_title(l,k):
            t=l.strip()
            if title_join:
                while k+1<end and L[k+1].strip() and is_title(L[k+1],k+1) is not False and not L[k+1].startswith(' ') and not is_author(L[k+1],k+1):
                    k+=1; t+=' '+L[k].strip()
            cur={'title':t,'author':None if author_after else globals().get('_pa'),'start':k+1}
            rows.append(cur)
        k+=1
    for j,r in enumerate(rows):
        nxt=rows[j+1]['start']-1 if j+1<len(rows) else end
        blk=[l for l in L[r['start']:nxt]]
        r['first_line']=pick_first(blk)
    return rows
def r2i(s):
    v={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000};t=0;s=s.upper()
    for i,c in enumerate(s):
        if c not in v: return None
        t+= -v[c] if i+1<len(s) and v[s[i+1]]>v[c] else v[c]
    return t
def uninvert(t):
    t=t.strip().rstrip(',').strip()
    m=re.match(r'^(.*?),\s*(The|A|An)$',t,re.I)
    if m: t=m.group(2)+' '+m.group(1)
    m=re.match(r'^(.*?),\s*(The|A|An)(\s*\(.*)$',t,re.I)
    if m: t=m.group(2)+' '+m.group(1)+m.group(3)
    return t
def parse_author_index(L, a, b):
    """index: author caps line, then indented 'Title ..... page' lines. returns [(page, title, author)]"""
    out=[];au=None;buf=''
    for l in L[a:b]:
        if not l.strip(): buf='';continue
        ind=len(l)-len(l.lstrip())
        m=re.match(r'^(.*?)[\s.]{2,}(\d+)\s*$',l.strip()) or re.match(r'^(.*?)\s+(\d+)\s*$',l.strip())
        if m and (ind>=2 and (au is not None)) and not is_caps(m.group(1)):
            t=(buf+' '+m.group(1)).strip() if buf else m.group(1)
            buf=''
            out.append((int(m.group(2)),t,au))
        elif is_caps(l.split('(')[0]) and ind<=3:
            au=l.strip().split('(_')[0].replace('PAGE.','').strip().rstrip('.').strip(); buf=''
        elif ind>=2 and au: buf=(buf+' '+l.strip()).strip()
    out.sort(key=lambda x:x[0])
    return out
def locate_any(L, st, end, titles, need_blank_before=True):
    """each title independently: first line in [st,end) whose norm equals (or startswith) title; returns idx list"""
    N={}
    for k in range(st,end):
        if need_blank_before and L[k-1].strip(): continue
        n=norm(L[k])
        if n and n not in N: N[n]=k
    out=[];used=set()
    for t in titles:
        nt=norm(t); k=N.get(nt)
        if k is None or k in used:
            # second occurrence / startswith
            cands=[kk for kk in range(st,end) if (not need_blank_before or not L[kk-1].strip()) and norm(L[kk])==nt and kk not in used]
            if not cands and len(nt)>=8:
                cands=[kk for kk in range(st,end) if (not need_blank_before or not L[kk-1].strip()) and norm(L[kk]).startswith(nt) and kk not in used and len(L[kk].strip())<len(t)+40]
            if not cands and len(nt)>=6:
                import difflib
                best=None
                for kk in range(st,end):
                    if kk in used or (need_blank_before and L[kk-1].strip()) or not L[kk].strip() or len(L[kk].strip())>len(t)+30: continue
                    n=norm(L[kk])
                    if abs(len(n)-len(nt))>12: continue
                    r=difflib.SequenceMatcher(None,n,nt).ratio()
                    if n and (nt in n or n in nt) and len(n)>=6: r=max(r,0.86)
                    if r>0.8 and (best is None or r>best[0]): best=(r,kk)
                if best: cands=[best[1]]
            k=cands[0] if cands else None
        if k is not None: used.add(k)
        out.append(k)
    return out
