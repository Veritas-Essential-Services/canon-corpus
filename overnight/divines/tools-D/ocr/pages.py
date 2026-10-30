# pages.py <id> -> <id>.pages.json : list of page texts (words) from djvu.xml
import re,sys,json,html
i=sys.argv[1]; x=open(f'{i}_djvu.xml',encoding='utf-8',errors='replace').read()
pages=[]
for obj in re.findall(r'<OBJECT.*?</OBJECT>',x,re.S):
  lines=[]
  for ln in re.findall(r'<LINE>(.*?)</LINE>',obj,re.S):
    lines.append(' '.join(html.unescape(w) for w in re.findall(r'<WORD[^>]*>(.*?)</WORD>',ln,re.S)))
  pages.append('\n'.join(lines))
json.dump(pages,open(f'{i}.pages.json','w'))
print(i,len(pages))
