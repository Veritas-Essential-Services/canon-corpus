import json,os
A='/tmp/claude-0/-home-claude-canon-corpus/23227e40-804c-5046-9833-e82b45c2f7aa/scratchpad/anth'
repo={}
for l in open(f'{A}/repo_list.tsv',encoding='utf-8'):
    p=l.rstrip('\r\n').split('\t')
    if len(p)==2 and p[0].isdigit(): repo.setdefault(int(p[0]),p[1])
VAR={66619:'-0',47476:'-8',55496:'-0',44593:'-0',52133:'-0',8820:'-8',56956:'-0',57018:'-0',49291:'-8',7211:'-8'}
def raw(pg): return f'https://raw.githubusercontent.com/GITenberg/{repo[pg]}/master/{pg}{VAR.get(pg,"")}.txt'
def cnt(pg):
    p=f'{A}/rows/{pg}.jsonl'
    if not os.path.exists(p): return None
    return sum(1 for l in open(p,encoding='utf-8') if json.loads(l).get('kind')!='prose')
B=[
(19221,"The Golden Treasury of the Best Songs and Lyrical Pieces in the English Language","Francis Turner Palgrave",1861,"unverified","general","British","Collins Clear-Type Press printing, illustrated by A. Pearse, undated on the transcribed title page; the text is Palgrave's original 1861 selection (288 poems, preface dated May 1861). All rows have author and first line."),
(32373,"The Golden Treasury (revised and enlarged)","Francis Turner Palgrave",1902,"text","general","British","Macmillan 1902 revised and enlarged edition (339 numbered pieces; a few untitled sub-parts take their first line as title). Overlaps heavily with 19221; it's a second edition, not a different anthology."),
(66619,"The Oxford Book of English Verse 1250-1900","Arthur Quiller-Couch",1900,"text","general","British","FLAG: the transcribed title page reads 'Impression of 1931 / First edition, 1900'. The selection is the 1900 first edition (883 poems), but this physical printing is dated 1931 (some death dates updated to 1917-18). Adam should decide whether a 1931 reprint of 1900 content passes the before-1931 rule. PG 1304 is an older transcription of the OBEV (edition not stated); rows were not extracted for it to avoid duplication."),
(6316,"Poems of American Patriotism","Brander Matthews",1922,"text","general","American","1922 revised edition (prefaces dated 1882 and July 4, 1922), illustrated by N. C. Wyeth. 'The Unknown Soldier' is listed in the contents but missing from the PG text, so its first_line is null."),
(47476,"Poems of American History","Burton Egbert Stevenson",1922,"text","general","American","Copyright 1908 and 1922 (the revised edition). Chronological, ballad-heavy: Revolution, 1812, Civil War, WWI. One duplicate-title contents entry is unmatched in the body."),
(15553,"The Golden Treasury of American Songs and Lyrics","Frederic Lawrence Knowles",1899,"text","general","American","New revised edition, L. C. Page, Boston, MDCCCXCIX. 148 poems, matching the contents."),
(55496,"A Household Book of English Poetry","Richard Chenevix Trench",1868,"text","general","British","Preface dated May 8th, 1868 (304 numbered poems). Verse lines carry printed line numbers, which were stripped from first_line."),
(44593,"The Oxford Book of Ballads","Arthur Quiller-Couch",1910,"unverified","general","British","The transcribed title page has no date. 1910 is inferred from the dedication/preface (Furnivall died 'a few months ago'; he died in 1910). 176 ballads, nearly all traditional, so author is null."),
(52133,"Patriotic Song: A Book of English Verse, being an anthology of the patriotic poetry of the British Empire","Arthur Stanley",1901,"text","general","British","233 poems: England, Scotland, Ireland, Wales, Canada, India, South Africa, Australia, New Zealand. Authors are taken from the contents."),
(12759,"The World's Best Poetry, Volume IV: The Higher Life","Bliss Carman (ed.)",1904,"text","general","American","John D. Morris & Co., 1904. Some selections are excerpts, and authors given as 'From the Greek of X' are reduced to the capitalised name."),
(12924,"The World's Best Poetry, Volume VIII: National Spirit","Bliss Carman (ed.)",1904,"text","general","American","1904. Patriotism, Freedom, War, Peace. This is the most on-target volume for the touchstones."),
(16786,"The World's Best Poetry, Volume III: Sorrow and Consolation","Bliss Carman (ed.)",1904,"text","general","American","1904. Parsed from body headings; the verse is unindented in this transcription."),
(43223,"The World's Best Poetry, Volume IX: Of Tragedy; Of Humour","Bliss Carman (ed.)",1904,"text","general","American","1904 (copyright line). Contains narrative and tragic ballads and humorous verse."),
(18909,"Poems Teachers Ask For","Readers of Normal Instructor-Primary Plans (F. A. Owen Pub. Co.)",None,"unverified","school reader","American","No date on the transcribed title page. Internal evidence: it cites copyrights of 1918 and 1919, so it is at least 1919, and it is commonly catalogued as 1925. The PG catalog says 'Public domain in the USA' but gives no year. 3 index titles were not found in the body (first_line null)."),
(19469,"Poems Teachers Ask For, Book Two","Readers of Normal Instructor-Primary Plans (F. A. Owen Pub. Co.)",None,"unverified","school reader","American","Undated; it mentions the Lincoln Memorial dedication of May 30, 1922, so it is at least 1922. The PG catalog says public domain in the USA. Verify before 1931."),
(8820,"A Treasury of War Poetry: British and American Poems of the World War 1914-1917","George Herbert Clarke",1917,"text","general","American","149 poems. Military ranks were stripped from author names."),
(33681,"Poems of the Great War (Prince of Wales's National Relief Fund)","Various (Chatto & Windus)",1914,"text","general","British","Fourth edition, London, 1914. 17 poems by Bridges, Newbolt, Kipling, Chesterton and others."),
(56956,"Great Poems of the World War","W. D. Eaton",1922,"text","general","American","Copyright 1918 and 1922 (T. S. Denison). This printing is 1922, which is still before 1931. Many poems are by serving soldiers."),
(46427,"The Great War in Verse and Prose","J. E. Weatherell",1919,"text","school reader","other","Canadian (Ontario Department of Education, 1919). Mixes poems and speeches; prose rows carry kind=prose (25)."),
(14640,"McGuffey's First Eclectic Reader, Revised Edition","William Holmes McGuffey",1920,"text","school reader","American","1879 revised edition; this printing carries copyright 1907 and 1920. Primer lessons are untitled with almost no verse, so no rows were extracted."),
(14668,"McGuffey's Second Eclectic Reader","William Holmes McGuffey",1920,"text","school reader","American","Copyright 1879/1896/1907/1920. All lessons are included; prose lessons carry kind=prose. Authors are not given in this reader."),
(14766,"McGuffey's Third Eclectic Reader","William Holmes McGuffey",1920,"text","school reader","American","Copyright 1879/1896/1907/1920. Prose lessons carry kind=prose. No authors in the contents."),
(14880,"McGuffey's Fourth Eclectic Reader","William Holmes McGuffey",1920,"text","school reader","American","Copyright 1879/1896/1907/1920. Authors come from the contents table. Prose lessons carry kind=prose."),
(15040,"McGuffey's Fifth Eclectic Reader","William Holmes McGuffey",1920,"text","school reader","American","Copyright 1879/1896/1907/1920. Authors come from the contents. Prose and speeches carry kind=prose. Verse/prose was classified by line shape, so expect a few misclassifications."),
(16751,"McGuffey's Sixth Eclectic Reader","William Holmes McGuffey",1921,"text","school reader","American","Copyright 1879/1896/1907/1921. Heavy on orations (kind=prose, 117). Dramatic extracts in blank verse may appear as verse."),
(17378,"Successful Recitations (The Royal Reciter and The Imperial Reciter)","Alfred H. Miles",1901,"text","recitation","British","1901. Two reciters in one volume. Prose recitations carry kind=prose."),
(57018,"Pieces People Ask For","George M. Baker",1909,"text","recitation","American","Title page 1909 (Walter H. Baker; copyright 1885, 1886, 1908). Serious, humorous, patriotic and dialect pieces. Prose carries kind=prose."),
(49291,"Beadle's Dime National Speaker","Various (Beadle and Company)",1863,"text","recitation","American","Entered 1863 (Dime Speaker No. 2). Civil War-era orations (kind=prose) and verse."),
(7211,"The American Union Speaker","John D. Philbrick",1865,"text","recitation","American","Entered 1865; preface dated July 4, 1864. 381 pieces in Standard, Recent (Civil War) and Humorous books, prose and poetry; prose sections carry kind=prose."),
(24798,"America First: Patriotic Readings","Jasper L. McBrien",1916,"text","school reader","American","American Book Company, 1916. Readings and poems; prose carries kind=prose. The opening Continental Congress dramatization is not itemised."),
(12925,"The World's Best Poetry, Volume X: Poetical Quotations","Bliss Carman (ed.)",1904,"catalog","general","American","Not fetched: it is quotations and indexes, not whole poems. Volumes I, II, V, VI and VII were not found in the GITenberg mirror listing."),
(36775,"Humorous Readings and Recitations in Prose and Verse","unverified",None,"unverified","recitation","other","Lead only: the ID and title are in the GITenberg list. Not fetched or checked."),
(61902,"How Salvator Won and Other Recitations","unverified",None,"unverified","recitation","other","Lead only: the ID and title are in the GITenberg list. Not fetched or checked."),
(70040,"Practical Recitations: Selections for literary exercises","unverified",None,"unverified","recitation","other","Lead only (above 50000, probably not in the mirror). Not fetched."),
(9078,"Sanders' Union Fourth Reader","Charles W. Sanders",None,"unverified","school reader","American","Lead only: in the GITenberg list. Not fetched."),
]
out=[]
for pg,t,ed,yr,yc,aud,nat,notes in B:
    fetched=os.path.exists(f'{A}/texts/{pg}.txt') and pg not in (12925,36775,61902,70040,9078)
    out.append({"pg_id":pg,"title":t,"editor_or_author":ed,"year":yr,"year_checked":yc,"audience":aud,"nationality":nat,
      "gutenberg_url":f"https://www.gutenberg.org/ebooks/{pg}","raw_url":raw(pg) if (fetched and pg in repo) else None,
      "fetched":fetched,"copyrighted_header":False if fetched else None,"poem_count":cnt(pg) if fetched else None,"notes":notes})
for t,ed,why in [("An American Anthology 1787-1900","Edmund Clarence Stedman","Not found on Project Gutenberg (only Stedman's own poems, PG 70763). archive.org scans exist."),
 ("A Victorian Anthology 1837-1895","Edmund Clarence Stedman","Not found on Project Gutenberg."),
 ("The Oxford Book of Victorian Verse","Arthur Quiller-Couch","Not found on Project Gutenberg (an archive.org PDF exists: cu31924013295757)."),
 ("Heart Throbs in Prose and Verse","Joe Mitchell Chapple","Not on Project Gutenberg; archive.org has heartthrobsinpro00chapuoft."),
 ("A New Library of Poetry and Song","William Cullen Bryant","Not found on Project Gutenberg."),
 ("Songs of Three Centuries","John Greenleaf Whittier","Not found on Project Gutenberg."),
 ("Parnassus","Ralph Waldo Emerson","Not found on Project Gutenberg."),
 ("One Hundred Choice Selections / The Speaker's Garland / Werner's Readings and Recitations","Phineas Garrett / Werner","None found on Project Gutenberg."),]:
    out.append({"pg_id":None,"title":t,"editor_or_author":ed,"year":None,"year_checked":"unverified","audience":"general","nationality":"American" if 'Oxford' not in t else "British","gutenberg_url":"","raw_url":None,"fetched":False,"copyrighted_header":None,"poem_count":None,"notes":"UNCONFIRMED: "+why})
json.dump(out,open(f'{A}/src/general.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out),sum(1 for o in out if o['fetched']),sum(o['poem_count'] or 0 for o in out))
