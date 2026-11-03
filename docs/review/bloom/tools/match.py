import json,re,unicodedata
def n(s): return re.sub(r'[^a-z0-9 ]',' ',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
STOP=set("the and of a an in on to for from with other poems poem selected collected works complete book books tales stories novels plays play".split())
b=json.load(open('bloom.json'));h=json.load(open('held2.json'));core=json.load(open('core.json'))
H=[]
for s,e in h.items():
    au=n(e['author']+' '+' '.join(e['surname'])+' '+s.replace('-',' '))
    for slug,(sec,i,t) in e['rows'].items(): H.append(dict(src=s,au=au,t=n(t+' '+slug.replace('-',' ')),raw=t,br=e['branches']))
for k,e in core.items(): H.append(dict(src='core:'+k,au=n(e['author']+' '+k.replace('-',' ')),t=n(e['title']+' '+k.replace('-',' ')),raw=e['author']+', '+e['title'],br=e['branches']))
for r in H: r['ts']=re.sub(r'^(the|a|an) ','',r['t'].strip())
for r in H: r['tw']=set(r['t'].split()); r['aw']=set(r['au'].split())
def cls(br):
    if 'main' in br: return 'main'
    if 'claude/armarium-divines' in br: return 'relay'
    if br==['claude/project-thread-yu0x73']: return 'pr38'
    return 'branch'
ALIAS={'saint augustine':'augustine','aesop':'aesop','longinus':'longinus'}
out=[]
for x in b:
    a=x['author'].strip('"').replace('"','')
    title=x['title']
    words=[w for w in n(a).split() if w not in STOP and len(w)>2]
    key=words[-1] if words else ''
    if not title:  # anonymous work or author-only entry
        tw=words; cands=[r for r in H if all(w in (r['t']+' '+r['au']).split() for w in tw[-2:])] if tw else []
        auth=cands
    else:
        tw=[w for w in n(title).split() if w not in STOP and len(w)>2]
        auth=[r for r in H if key and (key in r['aw'] or key in r['tw'])]
        need=tw[:3]
        cands=[r for r in auth if need and sum(w in r['tw'] for w in need)>=max(1,len(need)-(1 if len(need)>2 else 0))]
        if not cands and need and (len(need)>=2 or len(need[0])>=7):
            ph=' '.join(w for w in n(title).split() if w not in ('the','a','an'))
            cands=[r for r in H if r['ts'].startswith(ph)]
            for r in cands: r=r
            if cands: x=dict(x,title_only=True)
    best=None
    for c in ('main','relay','branch','pr38'):
        if any(cls(r['br'])==c for r in cands): best=c;break
    st=('held-'+best) if best else ('author' if auth else 'none')
    out.append(dict(x,status=st,hits=sorted({r['src']+' | '+r['raw'][:90] for r in cands})[:6],nauth=len({r['src'] for r in auth})))
json.dump(out,open('bloom-match.json','w'),ensure_ascii=False,indent=0)
from collections import Counter
print(Counter((o['age'],o['status']) for o in out))
