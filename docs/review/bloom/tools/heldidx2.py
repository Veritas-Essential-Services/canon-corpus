"""held2.json: every shelf on every origin branch, every row in any shape (sectioned lists or slug->dict with title)."""
import subprocess,json,sys
refs=subprocess.run(["git","for-each-ref","--format=%(refname)","refs/remotes/origin"],capture_output=True,text=True).stdout.split()
idx={}
def rows(d,out,sec=''):
    if isinstance(d,dict):
        for k,v in d.items():
            if k.startswith('_'): continue
            if isinstance(v,dict) and isinstance(v.get('title'),str):
                ident=v.get('gutenberg_id') or v.get('ia') or v.get('id') or v.get('urn') or ''
                out[k]=[sec or 'dict',str(ident),v['title']+(' / '+str(v.get('author')) if v.get('author') else '')]
            elif isinstance(v,list) and v and not isinstance(v[0],(dict,list)) and len(v)>1 and isinstance(v[1],str):
                out[k]=[sec[:2],str(v[0]),v[1]]
            elif isinstance(v,(dict,list)): rows(v,out,k if not sec else sec)
for ref in refs:
    names=[n for n in subprocess.run(["git","ls-tree","--name-only",ref,"pipeline/"],capture_output=True,text=True).stdout.split() if n.endswith("_shelf.json")]
    out=subprocess.run(["git","cat-file","--batch"],input="".join(f"{ref}:{n}\n" for n in names).encode(),capture_output=True).stdout
    i=0
    for n in names:
        nl=out.index(b"\n",i); size=int(out[i:nl].split()[2]); body=out[nl+1:nl+1+size]; i=nl+1+size+1
        try: d=json.loads(body.decode("utf-8","replace"))
        except Exception: continue
        s=n[9:-11]; e=idx.setdefault(s,{"author":d.get("_author","") if isinstance(d,dict) else "","surname":d.get("_surname",[]) if isinstance(d,dict) else [],"rows":{},"branches":[]})
        e["branches"].append(ref.split("origin/")[1]); rows(d,e["rows"])
json.dump(idx,open(sys.argv[1],"w"),ensure_ascii=False)
print(len(idx),"shelves",sum(len(e["rows"]) for e in idx.values()),"rows")
