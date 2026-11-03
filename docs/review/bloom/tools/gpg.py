"""gpg.py REGEX [REGEX..]: search Project Gutenberg's catalogue (title or author) -> id, lang, issued, title, authors."""
import csv,re,sys
csv.field_size_limit(10**8)
pats=[re.compile(p,re.I) for p in sys.argv[1:]]
for r in csv.DictReader(open('/tmp/claude-0/-home-user-canon-corpus/e2b3c735-11ff-534b-9d5b-21a3d720dd05/scratchpad/dl/pgcat/pg_catalog.csv',encoding='utf-8')):
    s=r['Title']+' | '+r['Authors']
    if all(p.search(s) for p in pats): print(r['Text#'],r['Language'],r['Title'].replace('\n',' ')[:110],'|',r['Authors'][:110])
