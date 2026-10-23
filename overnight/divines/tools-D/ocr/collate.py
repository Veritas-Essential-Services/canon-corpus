# collate.py primary other1 other2 ... -> primary.collated.json
import json,sys,re,difflib,collections
W=set(w.strip().lower() for w in open('/usr/share/dict/words',errors='ignore'))
def norm(t): return re.sub(r"[^a-z']","",t.lower()).strip("'")
def isword(n): return bool(n) and (n in W or n.rstrip('s') in W or (n.endswith("'s") and n[:-2] in W))
A=sys.argv[1]; O=sys.argv[2:]
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import reads as RD
MINR=RD.meta(A).get('vote_min_ratio',0.6)   # lower it for a scan whose damaged pages barely match their twin
P={i:json.load(open(i+'.pages.json')) for i in [A]+O}
out=[]; stats=collections.Counter(); residual=[]
def vote(page,k,srcs,stats,residual):
  lines=page.split('\n'); toks=[(li,t) for li,l in enumerate(lines) for t in l.split()]
  a=[norm(t) for _,t in toks]
  if len(a)<15: return page
  votes=[collections.Counter() for _ in a]
  for po in srcs:
    cands=range(max(0,k-8),min(len(po),k+9))
    best=max(cands,key=lambda m:difflib.SequenceMatcher(None,a,[norm(x) for x in po[m].split()],autojunk=False).quick_ratio(),default=None)
    if best is None: continue
    braw=po[best].split(); b=[norm(x) for x in braw]
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    if sm.ratio()<MINR: continue
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
    if not (n=='' and re.search(r'\d\d',t)) and not isword(n) and isword(nu) and c>=min(2,len(srcs)) and c>same:   # a number is never 'fixed' to letters
      new[x]=u; stats['fixed_nonword']+=1
    elif isword(n) and isword(nu) and c>=3 and same==0 and nu!=n:
      new[x]=u; stats['fixed_realword']+=1
    elif not isword(n) and n and len(n)>2:
      residual.append((k,t)); stats['residual']+=1
  for x,(li,t) in enumerate(toks):
    if not isword(a[x]) and a[x] and len(a[x])>2 and new[x]==t: pass
  L=collections.defaultdict(list)
  for x,(li,t) in enumerate(toks): L[li].append(new[x])
  stats['pages']+=1
  return '\n'.join(' '.join(L[li]) for li in range(len(lines)))
for k,page in enumerate(P[A]): out.append(vote(page,k,[P[o] for o in O],stats,residual))
for k,o,m in RD.meta(A).get('pages_from_twin',[]):   # a page too damaged to repair: take the twin's reading of the same plate,
  residual=[r for r in residual if r[0]!=k]          # letting this scan's own page vote on the twin's slips
  out[k]=vote(P[o][m],k,[[P[A][k]]*(2*k+1)],collections.Counter(),[]); stats['pages_from_twin']+=1
json.dump({'pages':out,'residual':residual,'stats':stats},open(A+'.collated.json','w'))
print(dict(stats))
