# reocr.py <id> : tesseract the pages holding garbled residual tokens; second-pass fix
import json,re,sys,os,subprocess,difflib,collections,urllib.request
from concurrent.futures import ThreadPoolExecutor
I=sys.argv[1]
W=set(w.strip().lower() for w in open('/usr/share/dict/words',errors='ignore'))
def norm(t): return re.sub(r"[^a-z']","",t.lower()).strip("'")
def isword(n): return bool(n) and (n in W or n.rstrip('s') in W or (n.endswith("'s") and n[:-2] in W))
def garble(t):
  core=t.strip('.,;:!?"\'()[]“”‘’-—')
  return bool(re.search(r"[^A-Za-z'’\-]",core)) or bool(re.search(r"[a-z][A-Z]",core)) or (not isword(norm(core)) and len(core)>2 and core.islower())
c=json.load(open(I+'.collated.json')); pages=c['pages']
pg=sorted(set(k for k,t in c['residual'] if garble(t)))
os.makedirs('img',exist_ok=True)
def ocr(k):
  j=f'img/{I}_{k}.jpg'; o=f'img/{I}_{k}'
  if not os.path.exists(o+'.txt'):
    if not os.path.exists(j): urllib.request.urlretrieve(f'https://archive.org/download/{I}/page/n{k}.jpg',j)
    subprocess.run(['tesseract',j,o,'-l','eng'],env={**os.environ,'OMP_THREAD_LIMIT':'1'},capture_output=True)
  return k,open(o+'.txt').read()
with ThreadPoolExecutor(4) as ex: T=dict(ex.map(ocr,pg))
st=collections.Counter(); left=[]
for k in pg:
  toks=pages[k].split(' ')  # keep newlines inside tokens
  flat=[t for t in re.split(r'(\s+)',pages[k])]
  words=[x for x in flat if x and not x.isspace()]
  a=[norm(w) for w in words]; braw=T[k].split(); b=[norm(x) for x in braw]
  sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
  rep={}
  for op,i1,i2,j1,j2 in sm.get_opcodes():
    if op=='replace' and i2-i1==j2-j1:
      for d in range(i2-i1): rep[i1+d]=braw[j1+d]
  wi=0; out=[]
  for x in flat:
    if x and not x.isspace():
      if garble(x) and wi in rep and isword(norm(rep[wi])) and not garble(rep[wi]):
        out.append(rep[wi]); st['tess_fixed']+=1
      else:
        out.append(x)
        if garble(x): left.append((k,x)); st['still_garbled']+=1
      wi+=1
    else: out.append(x)
  pages[k]=''.join(out)
c['pages']=pages; c['left']=left; c['stats'].update(st); c['reocr_pages']=pg
json.dump(c,open(I+'.collated.json','w'))
print(len(pg),'pages re-OCRed', dict(st), 'pages still garbled', len(set(k for k,_ in left)))
