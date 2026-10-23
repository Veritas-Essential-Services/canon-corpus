# crops.py <id> <maxpage> : contact sheets of the lines holding garbled tokens (pages < maxpage)
import json,re,sys,os,html,urllib.request
from PIL import Image,ImageDraw
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__))); from garble import strict
I=sys.argv[1]; MAXP=int(sys.argv[2]); MINP=int(sys.argv[3]); OUT=sys.argv[4]
x=open(f'{I}_djvu.xml',encoding='utf-8',errors='replace').read()
objs=re.findall(r'<OBJECT[^>]*>.*?</OBJECT>',x,re.S)
c=json.load(open(I+'.collated.json'))
want=[(k,t) for k,t in c['left'] if strict(t) and MINP<=k<MAXP]
items=[]
for k,t in want:
  o=objs[k]; W,H=map(int,re.search(r'width="(\d+)" height="(\d+)"',o).groups())
  for ln in re.findall(r'<LINE>(.*?)</LINE>',o,re.S):
    ws=re.findall(r'<WORD coords="(\d+),(\d+),(\d+),(\d+)"[^>]*>(.*?)</WORD>',ln,re.S)
    hit=[w for w in ws if html.unescape(w[4]).strip()==t]
    if hit:
      x1=min(int(w[0]) for w in ws); x2=max(int(w[2]) for w in ws)
      y1=min(int(w[3]) for w in ws); y2=max(int(w[1]) for w in ws)
      h=hit[0]; items.append((k,t,W,H,(x1,y1,x2,y2),(int(h[0]),int(h[3]),int(h[2]),int(h[1]))))
      break
os.makedirs(OUT,exist_ok=True)
seen=set(); strips=[]
for n,(k,t,W,H,box,wb) in enumerate(items):
  j=f'img/{I}_{k}.jpg'
  if not os.path.exists(j): urllib.request.urlretrieve(f'https://archive.org/download/{I}/page/n{k}.jpg',j)
  im=Image.open(j); sx=im.size[0]/W; sy=im.size[1]/H
  pad=30
  cr=im.crop((int(box[0]*sx)-pad,int(box[1]*sy)-pad,int(box[2]*sx)+pad,int(box[3]*sy)+pad)).convert('RGB')
  d=ImageDraw.Draw(cr); 
  d.rectangle((int(wb[0]*sx)-int(box[0]*sx)+pad-4,int(wb[1]*sy)-int(box[1]*sy)+pad-4,int(wb[2]*sx)-int(box[0]*sx)+pad+4,int(wb[3]*sy)-int(box[1]*sy)+pad+4),outline=(255,0,0),width=4)
  sc=1100/cr.size[0] if cr.size[0]>1100 else 1
  cr=cr.resize((int(cr.size[0]*sc),int(cr.size[1]*sc)))
  lab=Image.new('RGB',(cr.size[0],34),'white'); ImageDraw.Draw(lab).text((5,8),f'#{n}  p{k}',fill='black')
  strips.append((n,k,t,lab,cr))
meta=[]
for s in range(0,len(strips),12):
  grp=strips[s:s+12]; Wd=max(g[4].size[0] for g in grp); Ht=sum(g[3].size[1]+g[4].size[1] for g in grp)
  sheet=Image.new('RGB',(Wd,Ht),'white'); y=0
  for n,k,t,lab,cr in grp:
    sheet.paste(lab,(0,y)); y+=lab.size[1]; sheet.paste(cr,(0,y)); y+=cr.size[1]
  sheet.save(f'{OUT}/{I}_{s//12:02d}.jpg',quality=80)
  meta+= [(n,k,t) for n,k,t,_,_ in grp]
json.dump(meta,open(f'{OUT}/{I}.meta.json','w'))
print(len(items),'strips',(len(strips)+7)//8,OUT)
