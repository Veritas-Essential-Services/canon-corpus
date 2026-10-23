# pass2.py <id>: rule fixes + noise removal over every token of the collated pages; rebuild 'left'
import json,re,sys
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__))); from garble import strict,rulefix,noise
I=sys.argv[1]; c=json.load(open(I+'.collated.json')); pages=c['pages']
st={'rule':0,'noise':0}; left=[]
for k,p in enumerate(pages):
  out=[]
  for ln in p.split('\n'):
    ws=[]
    for t in ln.split(' '):
      if not t: continue
      if 'archive.org' in t: ws.append(t); continue
      if noise(t): st['noise']+=1; c['log'].append((k,t,'','noise')); continue
      u=rulefix(t)
      if u!=t: st['rule']+=1; c['log'].append((k,t,u,'rule'))
      if u: ws.append(u)
      if u and strict(u): left.append((k,u))
    out.append(' '.join(ws))
  pages[k]='\n'.join(out)
c['pages']=pages; c['left']=left
for a,b in st.items(): c['stats']['pass2_'+a]=c['stats'].get('pass2_'+a,0)+b
json.dump(c,open(I+'.collated.json','w')); print(st,'left',len(left),'body',sum(1 for k,_ in left if k<221))
