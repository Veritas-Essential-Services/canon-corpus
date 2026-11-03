"""mkplan.py OUT.json out*.jsonl : group 'add' verdicts by author into a shelf plan (review before applying)."""
import json,re,sys,unicodedata
h=json.load(open('held2.json'))
EXCL_N={164,191,1016,1270,1296,715,573,575, 107,114,127,137,141,256,259,262,264,266,270,284,285}
MULTI={424,443,485,499,508,147,183,185,200,203,204,211,213,217,236}
ONLY={425:['3020','11068'],188:'55625',189:'55625',191:'55625',97:'bim_early-english-books-1475-1640_the-castell-of-love-_san-pedro-diego-de_1560'}
FIRST_ONLY='--first' in sys.argv
EN_ONLY='--en' in sys.argv
N_SHELF={514:'samuel-butler',202:'samuel-butler-hudibras'}
BK={x['i']:x for x in json.load(open('bloomck.json'))}
ENR=('Great Britain','England','The United States','Canada','Australia','India (in English)')
sys.argv=[a for a in sys.argv if a not in('--first','--en')]          # scans carrying non-PD matter (Mann intro, 1949 Personae additions, 1946 Faulkner appendix): defer
EXCL_ID={"77900","bwb_S0-EAH-994","citiesofplainvol0000marc"}
SHELF_OVR={"Marcel Proust":"scott-moncrieff","Ernest Dowson":"dowson","Samuel Butler":"samuel-butler-hudibras","John Dryden":"dryden","Henry Howard, Earl of Surrey":"henry-howard-surrey","John Wilmot, Earl of Rochester":"john-wilmot-rochester","Francis Beaumont and John Fletcher":"beaumont-fletcher","Thomas Middleton and William Rowley":"thomas-middleton","Fulke Greville, Lord Brooke":"fulke-greville"}  # Vile Bodies PG (1964 preface, 1965 text); unverified My University Days
def a(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
def n(s): return re.sub(r'[^a-z ]','',a(s).lower()).strip()
def slugify(s,k=5): return '-'.join([w for w in re.sub(r'[^a-z0-9 ]',' ',a(s).lower()).split() if w not in ('the','a','an','of','and','by','with','in')][:k])
import subprocess
HELD_IDS={}
for s_,e_ in h.items():
    for slug_,(sec_,i_,t_) in e_['rows'].items(): HELD_IDS.setdefault(str(i_),[]).append(s_)
_src=subprocess.run(["git","-C","/home/user/canon-corpus","show","origin/main:pipeline/fetch_sources.py"],capture_output=True,text=True).stdout
for m_ in re.finditer(r'"([a-z0-9-]+)":\s*(\d+)',_src): HELD_IDS.setdefault(m_.group(2),[]).append('core:'+m_.group(1))
byauth={}
for s,e in h.items():
    if e['author']: byauth.setdefault(n(e['author']),[]).append(s)
plan={};order=[]
for f in sys.argv[2:]:
    for l in open(f):
        o=json.loads(l)
        if o['verdict']!='add' or o['n'] in EXCL_N: continue
        if EN_ONLY and not BK[o['n']]['r'].startswith(ENR): continue
        au=re.sub(r'\s*\(.*?\)','',o['author']).strip()
        if o['n'] in N_SHELF: au=au+' ['+N_SHELF[o['n']]+']'
        if au not in plan:
            ex=byauth.get(n(au),[])
            shelf=(N_SHELF.get(o['n'])) or SHELF_OVR.get(au) or (max(ex,key=lambda z:len(h[z]['rows'])) if ex else None) or '-'.join(re.sub(r'[^a-z0-9 ]',' ',a(au).lower()).split()[:4])
            last=n(au).split()[-1] if n(au) else ''
            plan[au]={"author":au,"shelf":shelf,"new":shelf not in h,"surname":[last,n(au)] if last else [], "rows":[]};order.append(au)
        P=plan[au]
        srcs=o['sources']
        if o['n'] in ONLY: srcs=[x for x in srcs if str(x['id']) in (ONLY[o['n']] if isinstance(ONLY[o['n']],list) else [ONLY[o['n']]])]
        elif FIRST_ONLY and o['n'] not in MULTI: srcs=srcs[:1]
        for s in srcs:
            if str(s['id']) in EXCL_ID: continue
            if any(r['id']==str(s['id']) for r in P['rows']):
                P['rows'][[r['id'] for r in P['rows']].index(str(s['id']))]['n'].append(o['n']);continue
            base=P['surname'][0] if P['surname'] else 'x'
            aw=set(n(au).split())|{'by','w','b','d','h','s','e','translated','from','french','german','introduction','edited','selected','poems'} - set()
            tw=[w for w in slugify(re.split(r'[:;(,]',s['title'])[0],9).split('-') if w and w not in aw or w=='poems'][:4]
            slug=(base+'-'+'-'.join(tw)).strip('-')
            if str(s['id']) in HELD_IDS and P['shelf'] not in HELD_IDS[str(s['id'])]: print('HELD-ID skip',s['id'],HELD_IDS[str(s['id'])],file=sys.stderr); continue
            k=2
            while any(r['slug']==slug for r in P['rows']):
                if any(r['title']==s['title'] for r in P['rows']): slug=None;break
                slug=re.sub(r'-\d+$','',slug)+f'-{k}';k+=1
            if not slug: continue
            P['rows'].append({"n":[o['n']],"bloom_title":o['title'],"kind":s['kind'],"id":str(s['id']),"title":s['title'],"translator":s.get('translator',''),"year":s.get('year',''),"djvu":s.get('djvu',''),"evidence":s.get('evidence',''),"slug":slug,"case":o.get('case',''),"note":o.get('note','')})
json.dump([plan[k] for k in order],open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
for k in order: print(plan[k]['shelf'],'NEW' if plan[k]['new'] else 'ext',len(plan[k]['rows']))
