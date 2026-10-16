import json,re,random,sys
sys.path.insert(0,'.'); from common import ANTH,norm
ids=[19316,16436,22922,34237,46515,50994,67522,63858,72625,27441,11023,13184,48484,62119,23794,26197,32415,30418,54530,44835,23457,70415,68359,42850,40576,16686]
tot={}
for pg in ids:
    r=[json.loads(l) for l in open(f'{ANTH}/rows/{pg}.jsonl',encoding='utf-8')]
    t=open(f'{ANTH}/texts/{pg}.txt',encoding='utf-8',errors='replace').read()
    tn=norm(t)
    nofl=sum(1 for x in r if not x['first_line']); noa=sum(1 for x in r if not x['author'])
    bad=[x for x in r if x['first_line'] and norm(x['first_line'])[:30] not in tn]
    random.seed(pg); samp=random.sample(r,min(10,len(r)))
    sbad=[x for x in samp if not x['first_line'] or norm(x['first_line'])[:30] not in tn or norm(x['title'])[:15] not in tn]
    orders=[x['order'] for x in r]==list(range(1,len(r)+1))
    dup=len(r)-len({(x['title'],x['first_line']) for x in r})
    tot[pg]=len(r)
    print(pg,len(r),'no_fl',nofl,'no_author',noa,'fl_not_in_text',len(bad),'sample_fail',len(sbad),'orderok',orders,'dups',dup, [ (x['title'],x['first_line']) for x in sbad][:3])
print(sum(tot.values()))
