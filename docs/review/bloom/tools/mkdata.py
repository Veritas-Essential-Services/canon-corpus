import json,re
exec(open('cases1.py').read());exec(open('cases2.py').read());exec(open('cases3.py').read())
C={**C1,**C2,**C3}
C["homer-curtis-newton"]=("X","C","Epigraphical evidence for Vespasian and Titus, a dissertation. Specialist.")
P=json.load(open('pr38.json'))
B=["Aesop","Longinus","Aeschylus","Apuleius","Archilochus","Sappho","Alcman","Aristophanes","Aristotle","Callimachus","Catullus","Cicero","Euripides","Herodotus","Hesiod","Homer","Horace","Juvenal","Lucan","Lucian","Lucretius","Martial","Menander","Ovid","Persius","Petronius","Pindar","Plato","Plautus","Plutarch","Seneca","Sophocles","Terence","Heraclitus","Empedocles","Theocritus","Thucydides","Virgil"]
alias={"Virgil":["Virgil","Vergil","Aeneid","Georgics","Eclogues"],"Homer":["Homer","Iliad","Odyssey"],"Plato":["Plato","Platon","Republic of Plato","Dialogues of Plato"],"Sappho":["Sappho"],"Catullus":["Catullus"],"Herodotus":["Herodotus"],"Thucydides":["Thucydides"]}
out=[];miss=[]
items=P if isinstance(P,list) else [dict(shelf=k,**v) for k,v in P.items()]
for p in items:
    s=p['shelf']
    if s not in C: miss.append(s);continue
    t,l,c=C[s]
    titles=[v[2] for v in p['added'].values()]
    blob=" ".join(titles)
    ties=[a for a in B if any(re.search(r'\b'+re.escape(w)+r'(s|\b|ic|ean|ian)',blob,re.I) for w in alias.get(a,[a]))]
    out.append(dict(s=s,n=bool(p['new']),a=p.get('author') or '',v=len(titles),t=titles,tier=t,lean=l,c=c,ties=ties))
print(len(out),miss)
json.dump(out,open('adm.json','w'),ensure_ascii=False,separators=(',',':'))
from collections import Counter
print(Counter(o['tier'] for o in out),Counter(o['lean'] for o in out),sum(1 for o in out if o['ties']))
