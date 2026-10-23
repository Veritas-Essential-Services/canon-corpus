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
# and every page with three or more garbled tokens (a damaged page the twins could not help)
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from garble import strict; import reads as RD
WIDE=RD.meta(I).get('reocr_damaged_pages',False)   # off for fix lists made before 2026-10-23 evening
if WIDE: pg=sorted(set(pg)|{k for k,p in enumerate(pages) if sum(1 for t in p.split() if strict(t))>=3})
def ok(x,y):
  if not WIDE: return garble(x)
  if not garble(x) or re.fullmatch(r'[(*†]?[\dIVXLC:,.;*†–—)-]+',x): return False
  a,b=norm(x),norm(y)
  return difflib.SequenceMatcher(None,a,b).ratio()>=0.5 and (x[:1].isupper()==y[:1].isupper() or not x[:1].isalpha())
held={(k,x) for k,t,u in RD.load(I) for x in t.split()}   # tokens a hand reading owns are left for it
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
      if wi in rep and ok(x,rep[wi]) and (k,x) not in held and isword(norm(rep[wi])) and not strict(rep[wi]):
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
