# twinpages.py <id> [min_left]: for each badly garbled page, find the twin scan's page for the same plate
# (the page between the twin pages that match its two neighbours) and print a pages_from_twin row when
# the twin's reading is much cleaner. Run in the work dir after run.sh; prints, changes nothing.
import json,sys,re,difflib,collections,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from garble import strict; import reads as RD
I=sys.argv[1]; MIN=int(sys.argv[2]) if len(sys.argv)>2 else 8
c=json.load(open(I+'.collated.json')); A=json.load(open(I+'.pages.json'))
norm=lambda t:re.sub(r"[^a-z']","",t.lower())
bad=collections.Counter(k for k,_ in c['left'])
for o in RD.meta(I).get('collated_with',[]):
  B=json.load(open(o+'.pages.json'))
  def best(k):
    a=[norm(x) for x in A[k].split()]
    if len(a)<15: return None,0
    r=max(((difflib.SequenceMatcher(None,a,[norm(x) for x in B[m].split()],autojunk=False).ratio(),m) for m in range(max(0,k-12),min(len(B),k+13))),default=(0,None))
    return r[1],r[0]
  for k,n in sorted(bad.items()):
    if n<MIN: continue
    def side(step):   # nearest page on this side that matches its twin page cleanly
      j=k+step
      while 0<=j<len(A) and abs(j-k)<=6:
        m,r=best(j)
        if m is not None and r>=0.7: return j,m
        j+=step
      return None,None
    kl,p=side(-1); kr,q=side(1)
    if p is None or q is None or q-p!=kr-kl: print('#',k,n,'no consistent neighbours',kl,p,kr,q); continue
    m=p+(k-kl); g=sum(1 for t in B[m].split() if strict(t))
    RATIO=float(os.environ.get('TWIN_RATIO','0.5'))
    print(json.dumps([k,o,m]) if g<n*RATIO else '#', k,'left',n,'twin garble',g)
