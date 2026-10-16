import json,re,sys
A='/tmp/claude-0/-home-claude-canon-corpus/23227e40-804c-5046-9833-e82b45c2f7aa/scratchpad/anth'
MINE=[int(x) for x in sys.argv[1:]]
for pg in MINE:
    p=f'{A}/rows/{pg}.jsonl'
    rows=[json.loads(l) for l in open(p,encoding='utf-8')]
    for r in rows:
        a=r.get('author')
        if a:
            a=re.sub(r'[\s.]*\d+$','',a).strip().strip('_').strip().rstrip(',;:').strip()
            a=re.sub(r'\s+',' ',a)
            if not re.search('[A-Za-z]',a): a=None
            r['author']=a or None
        t=r.get('title') or ''
        t=re.sub(r'\[(\d+|[A-Za-z])\]','',t).replace('_','').strip()
        t=re.sub(r'\s+',' ',t)
        m=re.match(r'^([“"‘\'(]+)([a-z])',t)
        if m: t=m.group(1)+m.group(2).upper()+t[m.end():]
        r['title']=t or r.get('first_line')
        f=r.get('first_line')
        if f:
            f=re.sub(r'\[(\d+|[A-Za-z])\]','',f).strip()
            f=re.sub(r'\s+',' ',f)
            r['first_line']=f or None
    with open(p,'w',encoding='utf-8') as fo:
        for k,r in enumerate(rows,1):
            r['order']=k
            fo.write(json.dumps(r,ensure_ascii=False)+'\n')
    n=len(rows)
    print(pg,n,'nofl',sum(1 for r in rows if not r['first_line']),'noau',sum(1 for r in rows if not r['author']),'prose',sum(1 for r in rows if r.get('kind')=='prose'))
