import json,sys
ANTH='/tmp/claude-0/-home-claude-canon-corpus/23227e40-804c-5046-9833-e82b45c2f7aa/scratchpad/anth'
pg,title,field,val=sys.argv[1:5]
p=f'{ANTH}/rows/{pg}.jsonl'; r=[json.loads(l) for l in open(p,encoding='utf-8')]
n=0
for x in r:
    if x['title']==title: x[field]=None if val=='NULL' else val; n+=1
open(p,'w',encoding='utf-8').write(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in r))
print('patched',n)
