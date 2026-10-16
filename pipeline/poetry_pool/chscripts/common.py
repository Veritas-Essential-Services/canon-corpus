import json, re, os
ANTH='/tmp/claude-0/-home-claude-canon-corpus/23227e40-804c-5046-9833-e82b45c2f7aa/scratchpad/anth'
def load(pg):
    t=open(f'{ANTH}/texts/{pg}.txt',encoding='utf-8',errors='replace').read()
    t=t.replace('\r\n','\n').replace('﻿','')
    s=t.find('*** START OF'); s=t.find('\n',s)+1 if s>=0 else 0
    e=t.find('*** END OF'); e=e if e>=0 else len(t)
    return t[s:e]
SMALL={'of','the','and','de','la','van','von','du','le','a','an','in','on','at','to','for'}
def tcase(s):
    s=s.strip()
    if not s: return s
    if s.upper()!=s: return s
    out=[]
    for i,w in enumerate(s.lower().split()):
        if i>0 and w in SMALL: out.append(w); continue
        out.append('-'.join(p[:1].upper()+p[1:] for p in w.split('-')))
    r=' '.join(out)
    r=re.sub(r'(^|[\s"“‘(])([a-z])',lambda m:m.group(1)+m.group(2).upper() if m.group(1) and m.group(1) in '"“‘(' or m.start()==0 else m.group(0),r)
    r=re.sub(r"\bMc(\w)",lambda m:'Mc'+m.group(1).upper(),r)
    r=re.sub(r"\bO'(\w)",lambda m:"O'"+m.group(1).upper(),r)
    r=re.sub(r"\b([A-Z])\.(\w)",lambda m:m.group(1)+'. '+m.group(2).upper(),r)
    return r
def clean(s):
    if s is None: return None
    s=re.sub(r'[_=]','',s); s=re.sub(r'\s+',' ',s).strip()
    s=re.sub(r'\[(\d+|\*+|[A-Z])\]','',s).strip()
    return s or None
def write(pg, rows):
    with open(f'{ANTH}/rows/{pg}.jsonl','w',encoding='utf-8') as f:
        for i,r in enumerate(rows,1):
            d={'pg_id':pg,'title':clean(r.get('title')),'author':clean(r.get('author')),'first_line':clean(r.get('first_line')),'order':i}
            f.write(json.dumps(d,ensure_ascii=False)+'\n')
    print(pg,'rows',len(rows))
def firstline_after(lines,i,maxskip=40):
    """first non-empty line after index i that looks like verse"""
    for j in range(i+1,min(len(lines),i+maxskip)):
        l=lines[j].strip()
        if not l or l.startswith('[Illustration') or l.startswith('[') or l.startswith('*'): continue
        return l, j
    return None, i
def roman_ok(s):
    return re.fullmatch(r'[IVXLC]+',s) is not None
def norm(s):
    s=re.sub(r'[_=]','',s or '').lower()
    s=re.sub(r'&','and',s)
    s=re.sub(r"[^a-z0-9]+",'',s)
    return s
def seq_find(L,start,titles,match=None,window=4000,prefix=False):
    """For each title in order, find the next body line whose normalized form equals norm(title). Returns list of indices (None if not found)."""
    idx=[]; pos=start
    for t in titles:
        nt=norm(re.sub(r'\(.*?\)','',t)); found=None
        nt2=norm(re.sub(r'^(the|a|an) ','',re.sub(r'\(.*?\)','',t).strip(),flags=re.I))
        for i in range(pos,min(len(L),pos+window)):
            nl=norm(L[i])
            if not nl: continue
            if nl==nt or (len(nt2)>=6 and re.sub(r'^(the|an|a)','',nl)==nt2) or (prefix and nl.startswith(nt) and len(nt)>=8) or (match and match(L[i],t)):
                found=i; break
        idx.append(found)
        if found is not None: pos=found+1
    return idx
def verse_after(L,i,minindent=3,maxskip=80,stop=None,skipcaps=True):
    for j in range(i+1,min(len(L),i+maxskip)):
        l=L[j]
        if stop and j>=stop: return None
        if not l.strip() or '[Illustration' in l or l.strip().startswith('['): continue
        if re.fullmatch(r'_[^_]+_\.?',l.strip()): continue
        if skipcaps and not re.search(r'[a-z]',l) and re.search(r'[A-Z]',l): continue
        ind=len(l)-len(l.lstrip(' '))
        if ind>=minindent and not re.fullmatch(r'[IVXLC0-9]+\.?',l.strip()) and not l.strip().startswith('*'):
            return l.strip()
    return None
