"""Build held.json: every shelf on every origin branch -> author, surnames, rows (sec, slug, id, title)."""
import subprocess,json
refs=[r for r in subprocess.run(["git","for-each-ref","--format=%(refname)","refs/remotes/origin"],capture_output=True,text=True).stdout.split()]
idx={}
for ref in refs:
    names=[n for n in subprocess.run(["git","ls-tree","--name-only",ref,"pipeline/"],capture_output=True,text=True).stdout.split() if n.endswith("_shelf.json")]
    out=subprocess.run(["git","cat-file","--batch"],input="".join(f"{ref}:{n}\n" for n in names).encode(),capture_output=True).stdout
    i=0
    for n in names:
        nl=out.index(b"\n",i); size=int(out[i:nl].split()[2]); body=out[nl+1:nl+1+size]; i=nl+1+size+1
        try: d=json.loads(body.decode("utf-8","replace"))
        except Exception: continue
        s=n[9:-11]; e=idx.setdefault(s,{"author":d.get("_author",""),"surname":d.get("_surname",[]),"rows":{},"branches":[]})
        e["branches"].append(ref.split("origin/")[1])
        for sec in ("internet_archive","gutenberg","perseus","ccel"):
            for slug,v in (d.get(sec) or {}).items():
                t=v[1] if isinstance(v,list) and len(v)>1 else (v.get("title") if isinstance(v,dict) else "")
                ident=v[0] if isinstance(v,list) else (v.get("id") or v.get("urn") or "")
                e["rows"][slug]=[sec[:2],str(ident),str(t)]
json.dump(idx,open(__import__("sys").argv[1],"w"),ensure_ascii=False)
print(len(idx),"shelves",sum(len(e["rows"]) for e in idx.values()),"rows")
