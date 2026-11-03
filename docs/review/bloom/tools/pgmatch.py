import csv,json,re,unicodedata,sys
csv.field_size_limit(10**8)
def n(s): return re.sub(r'[^a-z0-9 ]',' ',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
STOP=set("the and of a an in on to for from with other poems poem selected collected works complete book books tales stories novels plays play".split())
PG=[]
for r in csv.DictReader(open('../dl/pgcat/pg_catalog.csv',encoding='utf-8')):
    if r['Type']!='Text': continue
    PG.append((r['Text#'],r['Language'],n(r['Authors']),n(r['Title']),r['Title'].replace('\n',' ')[:100],r['Authors'][:60]))
M=json.load(open('bloom-match.json'))
for o in M:
    if o['status'].startswith('held'): continue
    a=o['author'].replace('"','');words=[w for w in n(a).split() if w not in STOP and len(w)>2]
    key=words[-1] if words else ''
    if o['title']:
        tw=[w for w in n(o['title']).split() if w not in STOP and len(w)>2][:3]
        hits=[p for p in PG if key in p[2].split() and tw and sum(w in p[3].split() for w in tw)>=max(1,len(tw)-(1 if len(tw)>2 else 0))]
    else:
        hits=[p for p in PG if words and all(w in p[3].split() for w in words[-2:])]
    hits.sort(key=lambda p:(p[1]!='en',int(p[0])))
    o['pg']=[f"PG {p[0]} [{p[1]}] {p[4]} / {p[5]}" for p in hits[:4]]
    o['pg_en']=any(p[1]=='en' for p in hits)
json.dump(M,open('bloom-match.json','w'),ensure_ascii=False,indent=0)
from collections import Counter
print(Counter((o['age'],o['status'],o.get('pg_en')) for o in M if not o['status'].startswith('held')))
