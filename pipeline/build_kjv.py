"""Build a greppable, OSIS-keyed KJV dataset from the pythonbible-kjv package."""
import json, re, unicodedata
import pythonbible as b

OSIS = {
 "GENESIS":"Gen","EXODUS":"Exod","LEVITICUS":"Lev","NUMBERS":"Num","DEUTERONOMY":"Deut",
 "JOSHUA":"Josh","JUDGES":"Judg","RUTH":"Ruth","SAMUEL_1":"1Sam","SAMUEL_2":"2Sam",
 "KINGS_1":"1Kgs","KINGS_2":"2Kgs","CHRONICLES_1":"1Chr","CHRONICLES_2":"2Chr",
 "EZRA":"Ezra","NEHEMIAH":"Neh","ESTHER":"Esth","JOB":"Job","PSALMS":"Ps","PROVERBS":"Prov",
 "ECCLESIASTES":"Eccl","SONG_OF_SONGS":"Song","ISAIAH":"Isa","JEREMIAH":"Jer",
 "LAMENTATIONS":"Lam","EZEKIEL":"Ezek","DANIEL":"Dan","HOSEA":"Hos","JOEL":"Joel",
 "AMOS":"Amos","OBADIAH":"Obad","JONAH":"Jonah","MICAH":"Mic","NAHUM":"Nah",
 "HABAKKUK":"Hab","ZEPHANIAH":"Zeph","HAGGAI":"Hag","ZECHARIAH":"Zech","MALACHI":"Mal",
 "MATTHEW":"Matt","MARK":"Mark","LUKE":"Luke","JOHN":"John","ACTS":"Acts","ROMANS":"Rom",
 "CORINTHIANS_1":"1Cor","CORINTHIANS_2":"2Cor","GALATIANS":"Gal","EPHESIANS":"Eph",
 "PHILIPPIANS":"Phil","COLOSSIANS":"Col","THESSALONIANS_1":"1Thess","THESSALONIANS_2":"2Thess",
 "TIMOTHY_1":"1Tim","TIMOTHY_2":"2Tim","TITUS":"Titus","PHILEMON":"Phlm","HEBREWS":"Heb",
 "JAMES":"Jas","PETER_1":"1Pet","PETER_2":"2Pet","JOHN_1":"1John","JOHN_2":"2John",
 "JOHN_3":"3John","JUDE":"Jude","REVELATION":"Rev",
}

def norm(s):
    """Fold to a comparison form: lowercase, no punctuation, collapsed space."""
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("’","'").replace("‘","'")
    s = s.lower()
    s = re.sub(r"[^a-z' ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

rows, missing = [], []
for book in b.Book:
    ab = OSIS.get(book.name)
    if not ab:
        continue
    nch = b.get_number_of_chapters(book)
    for ch in range(1, nch + 1):
        nv = b.get_number_of_verses(book, ch)
        for vs in range(1, nv + 1):
            vid = b.get_verse_id(book, ch, vs)
            try:
                txt = b.get_verse_text(vid, version=b.Version.KING_JAMES)
            except Exception:
                missing.append(f"{ab}.{ch}.{vs}")
                continue
            if not txt:
                missing.append(f"{ab}.{ch}.{vs}")
                continue
            rows.append({
                "id": f"kjv:{ab}.{ch}.{vs}",
                "book": ab, "book_title": book.title,
                "chapter": ch, "verse": vs,
                "text": txt.strip(),
                "norm": norm(txt),
            })

with open("kjv.tsv","w",encoding="utf-8") as f:
    f.write("id\ttext\n")
    for r in rows:
        f.write(f"{r['id']}\t{r['text']}\n")

with open("kjv.norm.tsv","w",encoding="utf-8") as f:
    f.write("id\tnorm\n")
    for r in rows:
        f.write(f"{r['id']}\t{r['norm']}\n")

with open("kjv.jsonl","w",encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("verses:", len(rows), "missing:", len(missing))
print("books:", len({r['book'] for r in rows}))
if missing[:5]: print("first missing:", missing[:5])
