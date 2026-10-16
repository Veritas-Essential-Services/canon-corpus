import sys,re; sys.path.insert(0,'.'); from common import *
pg=30418; L=load(pg).split('\n')
st=[k for k,l in enumerate(L) if l.strip()=='TRADITIONAL NURSERY SONGS.'][0]
en=[k for k,l in enumerate(L) if l.strip()=='THE END.'][0]
chunks=[]; cur=[]
for l in L[st+1:en]:
    if not l.strip() or l.strip().startswith('['):
        if cur: chunks.append(cur); cur=[]
        continue
    cur.append(l.strip())
if cur: chunks.append(cur)

chunks=[c for c in chunks if re.search('[a-z]',c[0]) and not c[0].startswith('_')]

CONT={'he','she','then','now','and','but','so','you','it','they','her','his','we','if','what','this','to','betty'}
def let(c):
    m=re.search(r'[A-Za-z]',c[0]); return m.group(0).upper()
def fw(c): return re.sub(r'[^a-z]','',c[0].split()[0].lower())
rows=[]; curlet='A'
for i,c in enumerate(chunks):
    l=let(c)
    # look ahead: letters of next non-cont chunks
    ahead=[let(x) for x in chunks[i+1:i+6] if fw(x) not in CONT]
    nxt=ahead[0] if ahead else 'Z'
    new = curlet<=l and (l<=nxt or l==curlet or nxt<curlet)
    if fw(c) in CONT and l!=curlet and not (curlet<l<=nxt and l==nxt): new=False
    if fw(c) in CONT and l==curlet and rows and fw({'0':[rows[-1]['first_line']]}['0'])!=fw(c) : pass
    if new:
        rows.append({'title':c[0],'author':None,'first_line':c[0]}); curlet=l
    else: print('cont:',c[0],' <<',rows[-1]['first_line'] if rows else None)
print(len(chunks),len(rows))
write(pg,rows)
