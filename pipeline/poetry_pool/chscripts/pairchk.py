import json,re,sys
sys.path.insert(0,'.'); from common import ANTH,norm
ids=[19316,16436,22922,34237,46515,50994,67522,63858,72625,27441,13184,48484,62119,44835,23457,70415,68359,42850,40576,16686]
for pg in ids:
    r=[json.loads(l) for l in open(f'{ANTH}/rows/{pg}.jsonl',encoding='utf-8')]
    L=[norm(l) for l in open(f'{ANTH}/texts/{pg}.txt',encoding='utf-8',errors='replace').read().replace('\r','').split('\n')]
    bad=[]
    for x in r:
        fl=norm(x['first_line'])[:30]; tt=norm(re.sub(r'\(.*?\)','',x['title']))
        tt2=re.sub(r'^(the|a|an)','',tt)[:12]
        fls=[i for i,l in enumerate(L) if fl and l.startswith(fl[:min(len(fl),len(l))]) and l]
        ok=False
        for i in fls:
            if any(tt2 and tt2 in L[j] for j in range(max(0,i-40),i)): ok=True;break
        if not ok: bad.append((x['order'],x['title'],x['first_line']))
    print(pg,len(r),'unpaired',len(bad),bad[:6])
