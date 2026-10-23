# replay.py <id> : apply the hand readings, index rules and small-caps fix to <id>.collated.json
import json,re,sys
I=sys.argv[1]; c=json.load(open(I+'.collated.json')); pages=c['pages']; c.setdefault('log',[])
def sub1(k,t,u,how):
  pat=r'(?<!\S)'+re.escape(t)+r'(?!\S)'
  if re.search(pat,pages[k]): pages[k]=re.sub(pat,u,pages[k],count=1); c['log'].append((k,t,u,how)); return 1
  return 0
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import reads as RD; reads=RD.load(I)
n=sum(sub1(k,t,u,'read') for k,t,u in reads)
R=[(r'^Ta/[ec]\)',"Tale)"),(r'^To/e\)',"Tale)"),(r'^\(Fo/ife$',"(Folk"),(r'^\(Fo/\^$',"(Folk"),(r'^\(Fo//fe$',"(Folk"),(r'^TheCid$','The Cid'),(r'^\^?AeSOp',"AESOP"),(r'^CiD,$','CID,'),(r'^LitUe$','Little'),(r'^TuUiver,?$',lambda m:'Tulliver'+(',' if m.group(0).endswith(',') else '')),(r'^GuUiver$','Gulliver')]
m=0
for k,p in enumerate(pages):
  for t in set(p.split()):
    u=t
    for a,b in R: u=re.sub(a,b,u)
    if u!=t:
      while sub1(k,t,u,'rule-checked'): m+=1
sc=0
for k,p in enumerate(pages):
  for t in set(p.split()):
    core=t.strip('.,;:()')
    if re.fullmatch(r"[A-Z][A-Za-z\-']{2,}",core) and re.search(r"[a-z][A-Z]|[A-Z][a-z]+[A-Z]",core) and sum(ch.isupper() for ch in core)>=len(core)/2 and not re.fullmatch(r"Ma?c[A-Z].*",core):
      while sub1(k,t,t.replace(core,core.upper()),'small-caps'): sc+=1
c['pages']=pages; c['stats'].update({'read_fixed':n,'index_rule_fixed':m,'smallcaps_fixed':sc})
json.dump(c,open(I+'.collated.json','w')); print('read',n,'rules',m,'smallcaps',sc)
