import json,re,glob,os,unicodedata,collections,csv,sys
A=sys.argv[1]; os.chdir(A)
books={}
for f in ['children','general']:
    for b in json.load(open(f'src/{f}.json')):
        if b.get('pg_id'): books[b['pg_id']]=dict(b,shelf=f)
def norm(s):
    s=re.sub(r"['\u2018\u2019\u02bc]",'',s or '')
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    s=re.sub(r"[^a-z0-9 ]+"," ",s); return re.sub(r"\s+"," ",s).strip()
def surname(a):
    a=norm(re.sub(r"\(.*?\)","",a or ''))
    a=re.split(r" and | from | after ",a)[0]
    w=[x for x in a.split() if x not in('sir','lord','jr','sr','the','rev','dr','mrs','miss','esq')]
    return w[-1] if w else ''
rows=[]
for f in sorted(glob.glob('rows/*.jsonl')):
    for l in open(f):
        r=json.loads(l); rows.append(r)
par=list(range(len(rows)))
def find(i):
    while par[i]!=i: par[i]=par[par[i]]; i=par[i]
    return i
def union(i,j): par[find(i)]=find(j)
idx={}
for i,r in enumerate(rows):
    fl=norm(r.get('first_line')).split()
    keys=[]
    if len(fl)>=4: keys.append('fl:'+' '.join(fl[:8]))
    t=norm(r.get('title')); s=surname(r.get('author'))
    if s and len(t)>=6: keys.append('ta:'+t+'|'+s)
    for k in keys:
        if k in idx: union(i,idx[k])
        else: idx[k]=i
groups=collections.defaultdict(list)
for i in range(len(rows)): groups[find(i)].append(rows[i])
# AO + addendum by title+surname
ao=collections.defaultdict(set)
for name,f in [('ao','../ao.jsonl'),('addendum-heroic','../add.jsonl')]:
    for l in open(f):
        r=json.loads(l); ao[norm(r['title'])+'|'+surname(r['poet'])].add(name)
out=[]
for g in groups.values():
    pgs=sorted({r['pg_id'] for r in g})
    best=collections.Counter(r['title'] for r in g).most_common(1)[0][0]
    auths=[r['author'] for r in g if r.get('author')]
    author=collections.Counter(auths).most_common(1)[0][0] if auths else None
    fls=[r['first_line'] for r in g if r.get('first_line')]
    fl=collections.Counter(fls).most_common(1)[0][0] if fls else None
    tags=set()
    for r in g: tags|=ao.get(norm(r['title'])+'|'+surname(r.get('author')),set())
    aud=sorted({books[p]['audience'] for p in pgs if p in books})
    kind='prose' if all(r.get('kind')=='prose' for r in g) else 'verse'
    out.append(dict(title=best,author=author,first_line=fl,kind=kind,n_books=len(pgs),books=pgs,audiences=aud,also_in=sorted(tags)))
out.sort(key=lambda o:(-o['n_books'],norm(o['title'])))
for i,o in enumerate(out,1): o['pool_id']=f'p{i:05d}'
os.makedirs('pool',exist_ok=True)
with open('pool/pool.jsonl','w') as f:
    for o in out: f.write(json.dumps({k:o[k] for k in ['pool_id','title','author','first_line','kind','n_books','books','audiences','also_in']},ensure_ascii=False)+'\n')
with open('pool/pool.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['keep?','pool_id','n_books','title','author','first_line','kind','audiences','also_in','books'])
    for o in out: w.writerow(['',o['pool_id'],o['n_books'],o['title'],o['author'] or '',o['first_line'] or '',o['kind'],';'.join(o['audiences']),';'.join(o['also_in']),';'.join(map(str,o['books']))])
c=collections.Counter(min(o['n_books'],6) for o in out)
print('rows',len(rows),'pool',len(out),'by n_books',sorted(c.items()),'ao/add tagged',sum(1 for o in out if o['also_in']))
