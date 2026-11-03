"""apply.py PLAN.json SHELF : write one planned author shelf into the repo (cwd = repo root). Prints the shelf name."""
import json,re,sys,os,urllib.request,time
plan={p['shelf']:p for p in json.load(open(sys.argv[1]))}; P=plan[sys.argv[2]]
path=f"pipeline/{P['shelf']}_shelf.json"
STAMP="Bloom addition 2026-11-03"
def djvu(ident):
    for t in range(3):
        try:
            files=json.load(urllib.request.urlopen(f"https://archive.org/metadata/{ident}/files",timeout=60)).get("result",[])
            names=[f["name"] for f in files if f["name"].endswith("_djvu.txt")]
            return names[0] if names else None
        except Exception as e: time.sleep(3)
    return None
if os.path.exists(path):
    d=json.load(open(path)); new=False
else:
    if P.get('new') is False: sys.exit("expected existing shelf missing: "+path)
    titles=sorted({r['bloom_title'] for r in P['rows']})
    d={"_about":f"{P['author']}. Bloom's Western Canon (1994) lists: {'; '.join(titles)}. {STAMP} under Adam's Bloom-only ruling; each row is US public domain (title page, Gutenberg header or IA metadata read, recorded in _bloom).",
       "_author":P['author'],"_name_words":[w for w in re.sub(r'[^a-z ]',' ',P['surname'][1] if len(P['surname'])>1 else '').split() if len(w)>1],
       "_surname":P['surname'],"ccel":{},"gutenberg":{},"internet_archive":{}}; new=True
d.setdefault("gutenberg",{}); d.setdefault("internet_archive",{})
added=[]
for r in P['rows']:
    if r['slug'] in d['gutenberg'] or r['slug'] in d['internet_archive']: print("slug exists, skipped",r['slug']); continue
    held_ids={str(v[0]) for sec in ('gutenberg','internet_archive') for v in d[sec].values()}
    if r['id'] in held_ids: print("id already on shelf, skipped",r['id']); continue
    if r['kind']=='pg':
        d['gutenberg'][r['slug']]=[int(r['id']),r['title']]+([f"tr. {r['translator']}"] if r['translator'] else [])
    else:
        name=r['djvu'] or djvu(r['id'])
        if not name: print("NO DJVU, skipped",r['id']); continue
        d['internet_archive'][r['slug']]=[r['id'],r['title']]+([name] if name!=f"{r['id']}_djvu.txt" else [])
        y=r['year']
        if re.search(r'19[3-9]\d|20\d\d|printing|reprint',y+' '+r['note'][:0]):
            d.setdefault("_rights_checked",{})[r['slug']]=f"{STAMP}: {y}. {r['evidence'][:300]}".strip()
    if r['translator'] and not r['translator'].lower().startswith('unread'):
        sur=r['translator'].split(' and ')[0].split(',')[0].split()[-1]
        d.setdefault("_translators",{})[r['slug']]=sur
    d.setdefault("_bloom",{})[r['slug']]={"bloom_n":r['n'],"bloom_title":r['bloom_title'],"year":r['year'],"evidence":r['evidence'][:400],"case":r['case'][:500],"note":r['note'][:500]}
    added.append(r['slug'])
if not new and added:
    d["_about"]=d["_about"].rstrip()+f" {STAMP} (Bloom's Western Canon): {', '.join(added)}."
json.dump(d,open(path,"w"),indent=1,ensure_ascii=False); open(path,"a").write("\n")
print(P['shelf'],"new" if new else "extended",len(added),"rows")
