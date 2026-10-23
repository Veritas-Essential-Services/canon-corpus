# collate.py primary other1 other2 ... -> primary.collated.json
import json,sys,re,difflib,collections
W=set(w.strip().lower() for w in open('/usr/share/dict/words',errors='ignore'))
def norm(t): return re.sub(r"[^a-z']","",t.lower()).strip("'")
def isword(n): return bool(n) and (n in W or n.rstrip('s') in W or (n.endswith("'s") and n[:-2] in W))
A=sys.argv[1]; O=sys.argv[2:]
P={i:json.load(open(i+'.pages.json')) for i in [A]+O}
out=[]; stats=collections.Counter(); residual=[]
for k,page in enumerate(P[A]):
  lines=page.split('\n'); toks=[(li,t) for li,l in enumerate(lines) for t in l.split()]
  a=[norm(t) for _,t in toks]
  if len(a)<15: out.append(page); continue
  votes=[collections.Counter() for _ in a]
  for o in O:
    po=P[o]; 
    cands=range(max(0,k-8),min(len(po),k+9))
    best=max(cands,key=lambda m:difflib.SequenceMatcher(None,a,[norm(x) for x in po[m].split()],autojunk=False).quick_ratio(),default=None)
    if best is None: continue
    braw=po[best].split(); b=[norm(x) for x in braw]
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    if sm.ratio()<0.6: continue
    for op,i1,i2,j1,j2 in sm.get_opcodes():
      if op=='equal':
        for d in range(i2-i1): votes[i1+d][('=',)]+=1
      elif op=='replace' and i2-i1==j2-j1:
        for d in range(i2-i1): votes[i1+d][braw[j1+d]]+=1
  new=[t for _,t in toks]
  for x,(li,t) in enumerate(toks):
    n=a[x]; v=votes[x]; same=v.get(('=',),0)
    alts=collections.Counter()
    for key,c in v.items():
      if key!=('=',): alts[key]+=c
    if not alts: continue
    (u,c),=alts.most_common(1); nu=norm(u)
    if not isword(n) and isword(nu) and c>=2 and c>same:
      new[x]=u; stats['fixed_nonword']+=1
    elif isword(n) and isword(nu) and c>=3 and same==0 and nu!=n:
      new[x]=u; stats['fixed_realword']+=1
    elif not isword(n) and n and len(n)>2:
      residual.append((k,t)); stats['residual']+=1
  for x,(li,t) in enumerate(toks):
    if not isword(a[x]) and a[x] and len(a[x])>2 and new[x]==t: pass
  L=collections.defaultdict(list)
  for x,(li,t) in enumerate(toks): L[li].append(new[x])
  out.append('\n'.join(' '.join(L[li]) for li in range(len(lines))))
  stats['pages']+=1
json.dump({'pages':out,'residual':residual,'stats':stats},open(A+'.collated.json','w'))
print(dict(stats))
