# final.py <id>: re-apply the hand readings to tokens the rule passes produced; recount what is left
import json,re,sys
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__))); from garble import strict
I=sys.argv[1]; c=json.load(open(I+'.collated.json')); P=c['pages']; n=0
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import reads as RD
for k,t,u in RD.load(I):
  pat=r'(?<!\S)'+re.escape(t)+r'(?!\S)'
  if re.search(pat,P[k]): P[k]=re.sub(pat,lambda m:u,P[k],count=1); c['log'].append((k,t,u,'read')); n+=1
for k in range(len(P)): P[k]=re.sub(r'[ ]{2,}',' ',P[k])
c['left']=[(k,t) for k,p in enumerate(P) for t in p.split() if strict(t) and 'archive.org' not in t]
c['stats']['read_fixed_late']=n
json.dump(c,open(I+'.collated.json','w')); print('late reads',n,'left',len(c['left']),'body',sum(1 for k,_ in c['left'] if k<221))
