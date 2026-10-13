import json,os
A='/tmp/claude-0/-home-claude-canon-corpus/23227e40-804c-5046-9833-e82b45c2f7aa/scratchpad/anth'
urls={}
for l in open(f'{A}/texts/_urls.tsv'):
    p,u=l.rstrip('\n').split('\t'); urls[int(p)]=u
def cnt(pg):
    f=f'{A}/rows/{pg}.jsonl'
    return sum(1 for _ in open(f)) if os.path.exists(f) else None
def hdr(pg):
    t=open(f'{A}/texts/{pg}.txt',encoding='utf-8',errors='replace').read()
    return 'COPYRIGHTED Project Gutenberg' in t[:5000]
B=[
(19316,"Lyra Heroica: A Book of Verse for Boys","William Ernest Henley",1891,"text","boys","British","Title page: Scribner, New York, 1920 printing; 'Copyright, 1891' and dedication dated Edinburgh, July 1891. Henley's own titles (not the poets'); 'birth-day order'. 126 numbered pieces; anonymous ballads have author null."),
(16436,"Poems Every Child Should Know","Mary E. Burt",1904,"text","children","American","What-Every-Child-Should-Know Library; 'Copyright 1904, by Doubleday, Page'; this is a later Doubleday, Doran / Parents' Institute printing (undated). Burt's headnotes stress memorization and recitation. 187 poems from the numbered contents."),
(22922,"The Posy Ring: A Book of Verse for Children","Kate Douglas Wiggin and Nora Archibald Smith",1903,"text","children","American","'Copyright, 1903, McClure, Phillips'; this file is the 1906 fifth impression. Companion to Golden Numbers (for younger children). 'Lilliput Notice' (Rands) is split front/back in the book; row uses the back portion's first line."),
(34237,"Golden Numbers: A Book of Verse for Youth","Kate Douglas Wiggin and Nora Archibald Smith",1902,"text","young people","American","'Copyright, 1902, McClure, Phillips'; this file is the Doubleday, Page 1909 printing. Large (380 pieces), strong on ballads, patriotic, sea and heroic verse; 'Old Ballad' authors set to null."),
(46515,"The Blue Poetry Book","Andrew Lang",1918,"text","children","British","Longmans 'Seventh Impression', 1918, per the PG title page; first edition 1891 per catalog (not stated in this text). Contents are indexed by author; rows follow body order. Ballads credited to 'Minstrelsy'/'Percy's Reliques' set to null."),
(50994,"The Cambridge Book of Poetry for Children (Parts 1 and 2)","Kenneth Grahame",1916,"text","children","British","Cambridge University Press 1916 (Part I preface material references 1915). Both parts in one file; rows run Part I then Part II. Authors resolved from the contents plus the per-part author index (pages); abbreviated contents names expanded from that index."),
(67522,"Rainbow Gold: Poems Old and New Selected for Boys and Girls","Sara Teasdale",1922,"text","children","American","Macmillan, New York, 'Copyright, 1922' / 'published September, 1922' — under the 1931 line. Includes some then-recent poets (Frost, de la Mare, Masefield, Lindsay, Graves); the book's 1922 publication is what the rule checks."),
(63858,"Story-Telling Ballads: Selected and Arranged for Story-Telling and Reading Aloud and for the Boys' and Girls' Own Reading","Frances Jenkins Olcott",1920,"text","young people","American","'Copyright, 1920, by Frances Jenkins Olcott'. 77 ballads and narrative poems (sea, border, heroic, romance, faith), ages ~12-15. Many traditional ballads have no author (null). Mirror file is 63858-0.txt (fetched although ID >50000-ish range is usually absent)."),
(72625,"Fifty Christmas Poems for Children","Florence B. Hyett",1923,"text","children","British","D. Appleton, New York, 'Copyright, 1923'. Compiler English. 47 rows: 'Three Christmas Songs' (Gales) is one row for three short pieces. Order reconstructed from the author index's page numbers."),
(27441,"The Children's Garland from the Best Poets","Coventry Patmore",1862,"text","children","British","Macmillan Golden Treasury Series; this text is the 1895 reprint, which states 'First Edition printed 1861 (dated 1862)'. Authors are given as initials in the book's index of writers (e.g. 'W. Wordsworth'); kept as given."),
(11023,"Gems of Poetry, for Girls and Boys","Unknown",1850,"text","children","American","1850 chapbook (Rufus Merrill, Concord, N.H. advert at end). Only 10 poems, no authors printed (e.g. 'Alexander Selkirk' is Cowper's, 'The Old Oaken Bucket' Woodworth's, but the book does not say so, so author is null)."),
(13184,"Narrative and Lyric Poems (First Series) for Use in the Lower School","O. J. Stevenson",1912,"text","school reader","other","Canadian (Copp, Clark, Toronto), 'Copyright, Canada, 1912'. Ontario prescribed poems incl. Horatius. Authors are surnames only in the book. Line numbers stripped from first lines."),
(48484,"Narrative and Lyric Poems (Second Series) for Use in the Lower School","O. J. Stevenson",1914,"text","school reader","other","Canadian (Copp, Clark, Toronto), 'Copyright, Canada, 1914'. Ontario prescribed list (Enoch Arden, Prisoner of Chillon, Lochinvar...). Surnames only."),
(62119,"Come Hither: A Collection of Rhymes and Poems for the Young of All Ages","Walter de la Mare",1923,"text","young people","British","Constable, London, MCMXXIII. 483 numbered poems; author taken from the signature under each poem (111 unsigned = traditional/unknown, null). 'Two Nut Trees' signature (Sitwell) applies to the poem as printed; part i is the traditional nut-tree rhyme. Notes section ('About and Roundabout') not extracted."),
(23794,"Mother Goose, or the Old Nursery Rhymes","Kate Greenaway (illustrator)",None,"unverified","children","British","Undated Frederick Warne reprint (no date in the text; the Greenaway book first appeared 1881 per catalog, not verified here). Rhymes are untitled: title = first line as given in the book's contents."),
(26197,"The Nursery Rhyme Book","Andrew Lang",1897,"text","children","British","'Copyright 1897 by F. Warne & Co.', MDCCCXCVII; illustrated by L. Leslie Brooke. Untitled rhymes: title = first line from the Index of First Lines; ordered by page then by position in the body."),
(32415,"The Nursery Rhymes of England","James Orchard Halliwell",1886,"text","children","British","Warne, London and New York, 1886, 'Fifth Edition' (first ed. 1842 per catalog). 659 numbered rhymes in 'classes' (Historical, Tales, Proverbs, Songs, Riddles, Charms, Games...). Title = first line; editorial bracket notes skipped."),
(30418,"Traditional Nursery Songs of England","Felix Summerly (Henry Cole), ed.",1843,"text","children","British","Joseph Cundall, London, 1843 (Home Treasury). No titles or index: rhymes separated by hand from stanza breaks (alphabetical order + manual review of 132 verse blocks), so a few boundaries are judgment calls. File also contains a prose Sir Guy of Warwick, not extracted."),
(54530,"The Knife-Grinder's Budget of Pictures & Poetry for Boys and Girls","Unknown",1829,"text","children","British","Penny chapbook, Otley, William Walker, 1829. 24 untitled picture quatrains; title = first line. Slight; include for completeness only."),
(44835,"Devotional Poetry for the Children, Second Part","Unknown (Book Association of Friends)",1870,"text","children","American","Philadelphia, Book Association of Friends (Quaker), 1870. 66 devotional/moral poems, no authors printed."),
(23457,"The Keepsake; or, Poems and Pictures for Childhood and Youth","Unknown",1818,"text","children","British","London, Darton, Harvey and Darton, 1818. 20 moral verses, apparently one anonymous author; authors null."),
(70415,"The Boy's Book of Battle-Lyrics","Thomas Dunn English",1885,"text","boys","American","Harper & Brothers, 'Copyright, 1885'. Single-author (not an anthology): metrical narratives of American battles from De Soto to the 1840s, each with a prose headnote. Fits the heroic-recitation brief well."),
(68359,"Poetry for Children","Charles and Mary Lamb",None,"unverified","children","British","J. M. Dent edition illustrated by Winifred Green with note by Israel Gollancz; no date in the text (Lambs' original 1809). Single-author pair; rows include the appended picture-poems at the end."),
(42850,"The Pied Piper of Hamelin and Other Poems","Robert Browning",1899,"text","boys","British","Every Boy's Library 'New edition, 1910', Dana Estes, Boston; 'Copyright, 1899'. Single author; includes Herve Riel, How They Brought the Good News, Incident of the French Camp, Cavalier Tunes. Publisher American."),
(40576,"Smiles: A Book of Recitations for Girls","Alice Lewis Richards",1899,"text","girls","American","Akron, Ohio, 1900 title page, 'Copyright, 1899'. Single-author recitation pieces for little girls; sentimental/light, probably below the culling bar."),
(16686,"Verses for Children, and Songs for Music","Juliana Horatia Ewing",1895,"text","children","British","SPCK, London; editor's preface dated June 1895 (some pieces earlier: 1874, 1880). Single author; includes 'Songs for Music' and hymns sections."),
(68926,"Stories and Ballads for Young Folks","Ellen Tracy Alden",1879,"text","young people","American","American Book Exchange, New York, 1880; '(Copyright, 1879.)'. Mostly prose stories with a short run of ballads at the end; single author; NOT extracted to rows (mainly prose)."),
(17735,"Eyes of Youth: A Book of Verse","Padraic Colum, Shane Leslie, Viola Meynell and others; foreword by G. K. Chesterton",None,"unverified","general","British","Verse BY young poets, not FOR children; out of scope for this shelf, no rows. Publication year not stated in the text (catalog: 1910) - unverified."),
]
out=[]
for pg,t,e,y,yc,aud,nat,notes in B:
    out.append({"pg_id":pg,"title":t,"editor_or_author":e,"year":y,"year_checked":yc,"audience":aud,"nationality":nat,
      "gutenberg_url":f"https://www.gutenberg.org/ebooks/{pg}","raw_url":urls.get(pg),"fetched":pg in urls,
      "copyrighted_header":hdr(pg),"poem_count":cnt(pg) if pg not in (68926,17735) else None,"notes":notes})
U=[
("The Home Book of Verse for Young Folks","Burton E. Stevenson",1915,"children","American","Not on Project Gutenberg as far as searches show (only the adult Home Book of Verse, PG 2619-2622, which belongs to another shelf)."),
("A Book of Verses for Children","E. V. Lucas",1897,"children","British","Not found on Project Gutenberg (web search, PG children's-poetry subject listings)."),
("The Golden Staircase: Poems and Verses for Children","Louey Chisholm",None,"children","British","Not found on Project Gutenberg; catalog records exist at HathiTrust/NLI only."),
("The Children's Treasury of English Song","Francis Turner Palgrave",1875,"children","British","Not found on Project Gutenberg."),
("The Boy's Book of Verse / The Girl's Book of Verse","Helen Dean Fish",None,"boys","American","Not found on Project Gutenberg; years (c.1922-23) not verified."),
("The Junior Classics, Vol. 10: Poems Old and New","William Patten, ed.",None,"children","American","Other Junior Classics volumes are on PG (prose); vol. 10 (poetry) was not found there (LibriVox audio only)."),
("Oxford Book of Verse for Boys/Girls; The Golden Book of Poetry; The Book of Courage; Sea songs and ballads for boys; Poems for the Young / Child's Calendar Beautiful","-",None,"children","other","Searched; no matching PG ebook found. Not confirmed to exist under these exact titles."),
]
for t,e,y,aud,nat,n in U:
    out.append({"pg_id":None,"title":t,"editor_or_author":e,"year":y,"year_checked":"unverified","audience":aud,"nationality":nat,"gutenberg_url":"","raw_url":None,"fetched":False,"copyrighted_header":None,"poem_count":None,"notes":"UNCONFIRMED: "+n})
json.dump(out,open(f'{A}/src/children.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out), sum(1 for x in out if x['fetched']), sum(x['poem_count'] or 0 for x in out), [x['pg_id'] for x in out if x['copyrighted_header']], [x['pg_id'] for x in out if x['pg_id'] and not x['fetched']])
