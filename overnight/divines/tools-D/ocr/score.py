import json,sys,re
W=set(w.strip().lower() for w in open('/usr/share/dict/words',errors='ignore'))
def score(t):
  ws=re.findall(r"[A-Za-z][A-Za-z']*",t)
  ws=[w.strip("'") for w in ws if len(w)>1]
  if len(ws)<20: return None,len(ws)
  ok=sum(1 for w in ws if w.lower() in W or w.lower().rstrip('s') in W)
  return ok/len(ws),len(ws)
if __name__=='__main__':
  p=json.load(open(sys.argv[1]+'.pages.json'))
  sc=[score(t) for t in p]
  good=[s for s,n in sc if s is not None]
  bad=[(k,round(s,2),n) for k,(s,n) in enumerate(sc) if s is not None and s<0.85]
  print(sys.argv[1],'pages',len(p),'text pages',len(good),'mean',round(sum(good)/len(good),3),'below .85:',len(bad))
  print(bad[:40])
