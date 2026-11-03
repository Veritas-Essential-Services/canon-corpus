import json,re
M=json.load(open('bloom-match.json'))
TRUE={("Matteo Maria Boiardo","Orlando Innamorato"),("Ludovico Ariosto","Orlando Furioso"),("Torquato Tasso","Jerusalem Delivered"),("Pierre Corneille","Polyeucte"),
("Johann Wolfgang von Goethe","The Sorrows of Young Werther"),("Johann Wolfgang von Goethe","Hermann and Dorothea"),("Friedrich Schiller","Mary Stuart"),("Friedrich Schiller","Don Carlos"),
("Gotthold Lessing","Laocoön"),("Giacomo Leopardi","Essays and Dialogues"),("Victor Hugo","Les Misérables"),("Théophile Gautier","Mademoiselle de Maupin"),("Théophile Gautier","Enamels and Cameos"),
("Honoré de Balzac","Louis Lambert"),("Honoré de Balzac","Eugénie Grandet"),("Honoré de Balzac","Ursule Mirouet"),("Stendhal","The Charterhouse of Parma"),("Gustave Flaubert","Madame Bovary"),
("Charles Baudelaire","Flowers of Evil"),("E. T. A. Hoffmann","The Devil's Elixir"),("Aleksandr Pushkin","Boris Godunov"),("Mikhail Lermontov","A Hero of Our Time"),("Ivan Goncharov","Oblomov"),
("Ivan Turgenev","First Love"),("Fyodor Dostoevsky","Crime and Punishment"),("Leo Tolstoy","Anna Karenina"),("Andre Gide","The Immoralist"),("François Mauriac","Therese"),("David Lindsay","A Voyage to Arcturus")}
def bc(br):
    return 'main' if 'main' in br else 'relay' if 'claude/armarium-divines' in br else 'pr38' if br==['claude/project-thread-yu0x73'] else 'branch'
out=[]
for i,o in enumerate(M):
    st=o['status']
    if o.get('title_only') and (o['author'],o['title']) not in TRUE: st='author' if o['nauth'] else 'none'
    s={'held-main':'held','held-relay':'held','held-branch':'branch','held-pr38':'pr38','author':'author','none':'none'}[st]
    hits=o['hits'] if st.startswith('held') else []
    pg=o.get('pg',[]) if s in('author','none') else []
    pgen=[p for p in pg if '[en]' in p]
    out.append(dict(i=i,g=o['age'],r=o['region'],a=o['author'],t=o['title'],s=s,h=[x.split(' | ')[0] for x in hits][:4],pg=pgen[:2]))
OV={("Hesiod","Works and Days"):("held",["hesiod"]),("Hesiod","Theogony"):("held",["hesiod"]),("Aeschylus","Suppliant Women"):("held",["aeschylus"]),
("Sophocles","Women of Trachis"):("held",["sophocles","lewis-campbell"]),("Aristophanes","The Assemblywomen"):("held",["aristophanes"]),
("Thucydides","The Peloponnesian Wars"):("held",["thucydides","adler"]),("Lucian","Satires"):("held",["lucian"]),("Plautus","The Braggart Soldier"):("held",["roman-comedy","tyrrell"]),
("Terence","The Girl from Andros"):("held",["roman-comedy"]),("Terence","The Eunuch"):("held",["roman-comedy"]),("Terence","The Mother-in-Law"):("held",["roman-comedy"]),("Lucretius","The Way Things Are"):("held",["lucretius","adler"]),("Catullus","Attis and Other Poems"):("held",["catullus"]),
("Menander","The Girl from Samos"):("pr38",["menander"]),
("The Nibelungen Lied",""):("held",["margaret-armour","upton"]),("The Book of the Thousand Nights and One Night",""):("held",["burton","lane"]),
("Saint Augustine","Confessions"):("held",["adler"]),("Saint Augustine","City of God"):("held",["adler"]),("Archilochos, Sappho, Alkman",""):("held",["greek-lyric"])}
for x in out:
    k=(x['a'],x['t'])
    if k in OV: x['s'],x['h']=OV[k];x['pg']=[]
json.dump(out,open('bloomck.json','w'),ensure_ascii=False,separators=(',',':'))
from collections import Counter
print(Counter((x['g'],x['s'],bool(x['pg'])) for x in out))
# Lane C audit 2026-11-03 (overnight/divines/staging-C/README.md, b4938eba): held on translator shelves
LC_HELD={93:'chretien',100:'petrarch',101:'petrarch',115:'symonds',119:'bowring',138:'denis-maccarthy',140:'denis-maccarthy',139:'fitzgerald',253:'payne',262:'singles-fiction-4',
 **{i:'van-laun' for i in range(275,282)},**{i:'french-classics' for i in range(286,290)},260:'french-classics',302:'dowson',335:'singles',336:'singles',343:'singles-fiction-2',
 373:'ellen-marriage',374:'ellen-marriage',386:'ives',388:'arthur-symons',406:'strindberg-english',409:'strindberg-english',557:'carlyle',564:'bowring',565:'margaret-armour',579:'seltzer',582:'jd-duff',604:'hapgood'}
LC_STAGED={n for c in json.load(open('laneC.json')) for n in c['bloom']}
for x in out:
    if x['i'] in LC_HELD and x['s'] in ('author','none'): x['s']='held';x['h']=[LC_HELD[x['i']]]+x['h'];x['pg']=[]
    if x['i'] in LC_STAGED and x['s'] in ('author','none'): x['lc']=1
json.dump(out,open('bloomck.json','w'),ensure_ascii=False,separators=(',',':'))
