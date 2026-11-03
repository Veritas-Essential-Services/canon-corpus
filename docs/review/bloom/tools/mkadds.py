"""mkadds.py: collect every Bloom addition (rows with a _bloom block) on the working tree -> adds.json for the page;
refine bloomck.json statuses with the research verdicts."""
import json,glob,os
R={}
for l in open('/home/user/canon-corpus/docs/review/bloom/bloom-research.jsonl'):
    o=json.loads(l); R[o['n']]=o
adds=[];shelved=set()
for p in sorted(glob.glob('/home/user/canon-corpus/pipeline/*_shelf.json')):
    d=json.load(open(p)); b=d.get('_bloom')
    if not b: continue
    shelf=os.path.basename(p)[:-11]
    for slug,m in b.items():
        sec='gutenberg' if slug in d.get('gutenberg',{}) else 'internet_archive' if slug in d.get('internet_archive',{}) else None
        if not sec: continue
        row=d[sec][slug]; ns=m['bloom_n'] if isinstance(m['bloom_n'],list) else [m['bloom_n']]
        shelved.update(ns)
        tr=d.get('_translators',{}).get(slug,'')
        adds.append(dict(id=f"{shelf}/{slug}",shelf=shelf,author=d.get('_author') or shelf,slug=slug,src=('PG ' if sec=='gutenberg' else 'IA ')+str(row[0]),
            title=row[1],tr=tr,year=m.get('year',''),n=ns,bt=m.get('bloom_title',''),case=m.get('case',''),note=m.get('note',''),new=d['_about'].startswith(d.get('_author','#')+'. Bloom')))
lc=json.load(open('laneC.json'))
for c in lc:
    adds.append(dict(id="laneC/"+c['id'],shelf="(Lane C staging)",author=c['work'].split(',')[0],slug=c['id'],src=('IA ' if c['source']=='internet_archive' else 'PG ')+c['id'],
        title=c['work'],tr=c.get('translator',''),year=c.get('printing',''),n=c['bloom'],bt='',case=c['case'],note="Staged by Lane C, not shelved; Lane C's lean: "+c['lean'],new=True,lc=c['lean']))
json.dump(adds,open('adds.json','w'),ensure_ascii=False,separators=(',',':'))
ck=json.load(open('bloomck.json'))
for x in ck:
    o=R.get(x['i'])
    if x['i'] in shelved: x['s']='added'
    elif o and x['s'] in('author','none'):
        x['s']={'held':'held','add':'deferred','not_pd':'notpd','no_source':'nosource','unclear':'nosource'}[o['verdict']]
        if o['verdict']=='held' and o.get('held_where'): x['h']=[o['held_where'][:80]]
        x['why']=(o.get('note') or o.get('case') or '')[:220]
json.dump(ck,open('bloomck2.json','w'),ensure_ascii=False,separators=(',',':'))
from collections import Counter
print(len(adds),'additions;',Counter(x['s'] for x in ck))
