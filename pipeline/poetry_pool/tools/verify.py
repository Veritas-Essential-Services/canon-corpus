import json,random,re,sys
sys.path.insert(0,'.')
from lib import load,norm
A='/tmp/claude-0/-home-claude-canon-corpus/23227e40-804c-5046-9833-e82b45c2f7aa/scratchpad/anth'
for pg in [int(x) for x in sys.argv[1:]]:
    L,_=load(pg); txt=norm(' '.join(L))
    rows=[json.loads(l) for l in open(f'{A}/rows/{pg}.jsonl',encoding='utf-8')]
    random.seed(pg*7)
    sm=random.sample(rows,min(10,len(rows)))
    okf=sum(1 for r in sm if r['first_line'] and norm(r['first_line']) in txt)
    okt=sum(1 for r in sm if norm(r['title']) in txt)
    oka=sum(1 for r in sm if not r['author'] or all(norm(w) in txt for w in r['author'].split()[-1:]))
    print(pg,'first_line',okf,'/',len(sm),'title',okt,'author-surname',oka)
