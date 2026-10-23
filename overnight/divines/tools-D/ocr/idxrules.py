# idxrules.py <id> <firstpage>: index-page rules. Refs are "VOL: page" with leader dots;
# OCR reads roman vols as digits (11: -> II:) and the leader dots as '*'.
import json,re,sys
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__))); from garble import strict
I=sys.argv[1]; F=int(sys.argv[2]); c=json.load(open(I+'.collated.json')); P=c['pages']
VOL={'1':'I','l':'I','I':'I','11':'II','1l':'II','l1':'II','ll':'II','II':'II','111':'III','11l':'III','lll':'III','III':'III',
     'Ill':'III','IIl':'III','lII':'III','IlI':'III','IV':'IV','1V':'IV','lV':'IV','V':'V','VI':'VI','V1':'VI','Vl':'VI'}
def fix(t):
  # the printed index marks first-edition refs with * (before or after the number) and second with †: keep them
  t=re.sub(r'^[•♦](?=\d)','*',t); t=re.sub(r'^[f+](?=\d{2,3}$)','†',t)
  parts=re.findall(r'\.?[1lIV]{1,3}:|[*†]?\d{1,3}\*?|[^:\d*†]+|[*†]',t) if re.fullmatch(r'(\.?[1lIV]{1,3}:|[*†]?\d{1,3}\*?)+',t) and ':' in t and not re.search(r'\d{4}',t) and not re.match(r'\d+[lIV]+:',t) else [t]
  out=[]
  for x in parts:
    m=re.fullmatch(r'\.?([1lIV]{1,3}):',x)
    out.append(VOL.get(m.group(1),m.group(1))+':' if m else x)
  return ' '.join(out)
n=0
for k in range(F,len(P)):
  lines=[]
  for ln in P[k].split('\n'):
    ws=[]
    for t in ln.split(' '):
      if not t: continue
      u=fix(t)
      if u!=t: n+=1; c['log'].append((k,t,u,'index-rule'))
      if u: ws.append(u)
    lines.append(' '.join(ws))
  P[k]='\n'.join(lines)
c['left']=[(k,t) for k,p in enumerate(P) for t in p.split() if strict(t)]
c['stats']['index_ref_fixed']=n
json.dump(c,open(I+'.collated.json','w'))
print('fixed',n,'left',len(c['left']),'index',sum(1 for k,_ in c['left'] if k>=F))
