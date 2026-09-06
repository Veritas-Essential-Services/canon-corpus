#!/usr/bin/env python3
"""Parse public-domain maxim collections into discrete numbered units."""
import re, json, html, unicodedata, os

RAW = 'raw'
OUT = 'out'
os.makedirs(OUT, exist_ok=True)

def body(f):
    t = open(os.path.join(RAW, f), encoding='utf-8').read()
    a = re.search(r'\*\*\* ?START OF TH[EIS]+ PROJECT GUTENBERG.*?\*\*\*', t, re.S)
    b = re.search(r'\*\*\* ?END OF TH[EIS]+ PROJECT GUTENBERG.*?\*\*\*', t, re.S)
    return t[a.end() if a else 0: b.start() if b else len(t)]

def norm(s):
    s = s.replace('\r', '')
    s = re.sub(r'\[\d+\]', '', s)           # footnote markers
    s = re.sub(r'\{\d+\}', '', s)           # page markers
    s = re.sub(r'_([^_]+)_', r'\1', s)      # italics underscores
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

R_MAP = {'i':1,'v':5,'x':10,'l':50,'c':100,'d':500,'m':1000}
def roman(s):
    s = s.lower(); tot = 0
    for i, ch in enumerate(s):
        v = R_MAP.get(ch)
        if v is None: return None
        if i+1 < len(s) and R_MAP.get(s[i+1], 0) > v: tot -= v
        else: tot += v
    return tot


HEAD_STOP = re.compile(r"""^(?:
    [A-Z][A-Z0-9 ,.'\-\u2014:;()\[\]&]{7,}      # ALL-CAPS heading line
  | FOOTNOTES?\b.*
  | \[Footnote.*
  | \*\s+\*\s+\*.*
  | The\s+End\b.*
  | THE\s+END\b.*
)$""", re.X)

def trim_tail(raw, max_paras=6):
    """Cut a unit's raw slice at the first block that is clearly not part of it."""
    blocks = re.split(r'\n\s*\n', raw)
    keep = []
    for b in blocks:
        st = b.strip()
        if not st:
            continue
        first = st.split('\n')[0].strip()
        if HEAD_STOP.match(first) and not st.endswith(('.', '!', '?', '"', '\u201d')):
            break
        if HEAD_STOP.match(first) and len(first) > 12 and first.isupper():
            break
        if st.startswith('['):
            break
        keep.append(st)
        if len(keep) >= max_paras:
            break
    return '\n\n'.join(keep)

def pick_seq(cands, start=1):
    """cands: list of (n, span_start, span_end). Accept n==want; tolerate a single
    misprinted number when the NEXT candidate resumes the run."""
    seq, want, i = [], start, 0
    while i < len(cands):
        n, a, b = cands[i]
        if n == want:
            seq.append((want, a, b)); want += 1; i += 1; continue
        if i + 1 < len(cands) and cands[i+1][0] == want + 1:
            seq.append((want, a, b)); want += 1; i += 1; continue   # misprint
        i += 1
    return seq

def slice_units(seq, text, cut_notes=False):
    out = []
    for k, (n, a, b) in enumerate(seq):
        stop = seq[k+1][1] if k+1 < len(seq) else len(text)
        raw = trim_tail(text[b:stop])
        out.append((n, norm(raw)))
    return out

RECORDS = []
REPORT = []

def emit(work, units, expected, **meta):
    for ref, text in units:
        RECORDS.append(dict(work=work, ref=str(ref), text=text, **meta))
    ok = (expected is None) or (len(units) == expected)
    REPORT.append((work, len(units), expected, 'OK' if ok else 'MISMATCH'))
    print(f'{"OK " if ok else "!! "} {work:38s} parsed={len(units):5d} expected={expected}')

# ---------------------------------------------------------------- 1. Publilius Syrus
def publilius():
    h = open(os.path.join(RAW, 'publilius_wikisource.html'), encoding='utf-8').read()
    h = re.sub(r'(?is)<style.*?</style>|<script.*?</script>', '', h)
    h = re.sub(r'(?is)<sup.*?</sup>', '', h)
    h = re.sub(r'(?is)<span[^>]*class="[^"]*pagenum[^"]*".*?</span></span>', ' ', h)
    # number cells -> sentinels
    h = re.sub(r'(?is)<div class="wst-center[^"]*">\s*<p>\s*(\d{1,4})\.\s*</p>\s*</div>',
               r'@@\1@@', h)
    h = re.sub(r'<[^>]+>', ' ', h)
    h = html.unescape(h)
    toks = re.split(r'@@(\d{1,4})@@', h)
    units, want = [], 1
    for i in range(1, len(toks) - 1, 2):
        n = int(toks[i])
        if n != want: continue
        txt = norm(toks[i+1])
        txt = re.sub(r'\s*\u200b\s*', ' ', txt).strip()
        if txt: units.append((n, txt))
        want += 1
    emit('Publilius Syrus, Sententiae', units, 1087,
         author='Publilius Syrus', author_dates='fl. c. 85-43 BC', composed='1st c. BC',
         translator='Darius Lyman Jr.', translation_year=1856,
         source='Wikisource (Lyman 1856)', pd_basis='translation pub. 1856')

# ---------------------------------------------------------------- 2. La Rochefoucauld
def larochefoucauld():
    t = body('larochefoucauld_9105.txt')
    t = t.replace('4ll.--', '411.--')                      # typeset trap
    idx = [(int(m.group(1)), m.start(), m.end())
           for m in re.finditer(r'^(\d{1,3})\.--', t, re.M)]
    seq, want = [], 1
    for n, s, e in idx:
        if n == want: seq.append((n, s, e)); want += 1
    units = []
    for k, (n, s, e) in enumerate(seq):
        stop = seq[k+1][1] if k+1 < len(seq) else len(t)
        units.append((n, norm(trim_tail(t[e:stop]))))
    emit('La Rochefoucauld, Maximes (1678)', units, 504,
         author='Francois VI, duc de La Rochefoucauld', author_dates='1613-1680', composed='1665-1678',
         translator='J. W. Willis Bund & J. Hain Friswell', translation_year=1871,
         source='Gutenberg 9105', pd_basis='translation pub. 1871')

    # supplements, Roman-numbered
    sup = [(roman(m.group(1)), m.start(), m.end())
           for m in re.finditer(r'^([IVXLC]{1,8})\.--', t, re.M)]
    sseq, want = [], 1
    for n, s, e in sup:
        if n == want: sseq.append((n, s, e)); want += 1
    sunits = []
    for k, (n, s, e) in enumerate(sseq):
        stop = sseq[k+1][1] if k+1 < len(sseq) else len(t)
        sunits.append((n, norm(trim_tail(t[e:stop]))))
    emit('La Rochefoucauld, Suppressed & Posthumous Maxims', sunits, 125,
         author='Francois VI, duc de La Rochefoucauld', author_dates='1613-1680', composed='1665-1693',
         translator='J. W. Willis Bund & J. Hain Friswell', translation_year=1871,
         source='Gutenberg 9105', pd_basis='translation pub. 1871')

# ---------------------------------------------------------------- 3. Chamfort
def chamfort():
    t = body('chamfort_69632.txt')
    m = re.search(r'\n\s*The Cynic.s Breviary\s*\n', t)
    if m: t = t[m.end():]
    cut = re.search(r'\n\s*(?:PRINTED BY|Transcriber.s Note)', t)
    if cut: t = t[:cut.start()]
    parts = re.split(r'\n\s*\*(?:\s+\*){3,}\s*\n', t)
    units = []
    for p in parts:
        p = norm(p)
        if len(p) > 15: units.append((len(units)+1, p))
    emit("Chamfort, Maximes et Pensees (sel.)", units, 163,
         author='Sebastien-Roch Nicolas de Chamfort', author_dates='1740-1794', composed='c.1770-1794',
         translator='William G. Hutchison', translation_year=1902,
         source='Gutenberg 69632', pd_basis='translation pub. 1902',
         note='selection: The Cynic\'s Breviary; units unnumbered in source, sequence assigned')

# ---------------------------------------------------------------- 4. Goethe
def goethe():
    t = body('goethe_33670.txt')
    idx = [(int(m.group(1)), m.start(), m.end())
           for m in re.finditer(r'\n\n(\d{1,4})\n\n', t)]
    seq = pick_seq(idx)
    units = slice_units(seq, t)
    emit('Goethe, Maximen und Reflexionen (sel.)', units, 590,
         author='Johann Wolfgang von Goethe', author_dates='1749-1832', composed='lifetime; pub. 1833',
         translator='T. Bailey Saunders', translation_year=1906,
         source='Gutenberg 33670', pd_basis='translation pub. 1906',
         note='selection: 590 of c.1400 in the German (Hecker numbering differs)')

# ---------------------------------------------------------------- 5. Hazlitt
def hazlitt():
    t = body('hazlitt_59256.txt')
    a = t.find('I. Of all virtues, magnanimity')
    t = t[a:] if a > 0 else t
    idx = [(roman(mm.group(1)), mm.start(), mm.end())
           for mm in re.finditer(r'^([IVXLC]{1,12})\.\s', t, re.M)]
    idx = [(n, a, b) for n, a, b in idx if n]
    seq = pick_seq(idx)
    units = slice_units(seq, t)
    emit('Hazlitt, Characteristics (1823)', units, 434,
         author='William Hazlitt', author_dates='1778-1830', composed='1823',
         translator=None, translation_year=None,
         source='Gutenberg 59256 (Collected Works vol. 2)', pd_basis='English original, 1823')

# ---------------------------------------------------------------- 6. La Bruyere
def labruyere():
    t = body('labruyere_46633.txt')
    chaps = list(re.finditer(r'^\(1\.\)', t, re.M))
    units = []
    for ci, cm in enumerate(chaps):
        s = cm.start(); e = chaps[ci+1].start() if ci+1 < len(chaps) else len(t)
        seg = t[s:e]
        cnum = ci + 1
        idx = [(int(m.group(1)), m.start(), m.end())
               for m in re.finditer(r'\((\d{1,4})\.?\)', seg)]
        seq = pick_seq(idx)
        for k, (n, a, b) in enumerate(seq):
            stop = seq[k+1][1] if k+1 < len(seq) else len(seg)
            txt = norm(trim_tail(seg[b:stop]))
            if txt: units.append((f'{cnum}.{n}', txt))
    emit('La Bruyere, Les Caracteres', units, None,
         author='Jean de La Bruyere', author_dates='1645-1696', composed='1688-1696',
         translator='Henri Van Laun', translation_year=1885,
         source='Gutenberg 46633', pd_basis='translation pub. 1885',
         note='chapter-restarting numbering; PG text has 1119 vs canonical 1120')

# ---------------------------------------------------------------- 7. Pascal
def pascal():
    t = body('pascal_18269.txt')
    i = t.find('SECTION I')
    if i > 0: t = t[i:]
    idx = [(int(m.group(1)), m.start(), m.end())
           for m in re.finditer(r'^\s*(\d{1,4})\s*$', t, re.M)]
    seq, want = [], 1
    for n, s, e in idx:
        if n == want: seq.append((n, s, e)); want += 1
    units = []
    for k, (n, s, e) in enumerate(seq):
        stop = seq[k+1][1] if k+1 < len(seq) else len(t)
        units.append((n, norm(trim_tail(t[e:stop]))))
    emit('Pascal, Pensees', units, 923,
         author='Blaise Pascal', author_dates='1623-1662', composed='1656-1662; pub. 1670',
         translator='W. F. Trotter', translation_year=1904,
         source='Gutenberg 18269', pd_basis='Trotter translation 1904',
         note='PG front matter carries a 1958 Dutton notice and a T.S. Eliot introduction - EXCLUDED here; fragments only. Brunschvicg numbering.')

# ---------------------------------------------------------------- 8. Ptahhotep
def ptahhotep():
    t = body('ptahhotep_30508.txt')
    i = t.find('THE INSTRUCTION OF PTAH-HOTEP')
    t = t[i:] if i > 0 else t
    idx = [(int(m.group(1)), m.start(), m.end())
           for m in re.finditer(r'^(\d{1,3})\.\s\s', t, re.M)]
    seq, want = [], 1
    for n, s, e in idx:
        if n == want: seq.append((n, s, e)); want += 1
    units = []
    for k, (n, s, e) in enumerate(seq):
        stop = seq[k+1][1] if k+1 < len(seq) else len(t)
        units.append((n, norm(trim_tail(t[e:stop]))))
    emit('The Instruction of Ptahhotep', units, 43,
         author='attrib. Ptahhotep', author_dates='framed c. 2400 BC', composed='Middle Kingdom, c. 1991-1802 BC',
         translator='Battiscombe G. Gunn', translation_year=1906,
         source='Gutenberg 30508', pd_basis='translation pub. 1906',
         note="Gunn's 43-maxim segmentation; modern Egyptology (Zaba 1956) divides it into 37")

# ---------------------------------------------------------------- 9. Havamal
def havamal():
    t = body('havamal_73533.txt')
    i = t.find('HOVAMOL')
    j = t.find('VAFTHRUTHNISMOL')
    seg = t[i:j] if i > 0 and j > i else t
    idx = [(int(m.group(1)), m.start(), m.end())
           for m in re.finditer(r'^(\d{1,3})\.\s', seg, re.M)]
    seq, want = [], 1
    for n, s, e in idx:
        if n == want: seq.append((n, s, e)); want += 1
    units = []
    for k, (n, s, e) in enumerate(seq):
        stop = seq[k+1][1] if k+1 < len(seq) else len(seg)
        units.append((n, norm(trim_tail(seg[e:stop]))))
    emit('Havamal (Poetic Edda)', units, None,
         author='anonymous', author_dates='c. 900-1100', composed='Codex Regius c. 1270',
         translator='Henry Adams Bellows', translation_year=1923,
         source='Gutenberg 73533', pd_basis='translation pub. 1923',
         note='Bellows divides into 165 stanzas; most editions give 164')

# ---------------------------------------------------------------- 10. Blake
def blake():
    t = body('blake_45315.txt')
    m = re.search(r'^\s*PROVERBS OF HELL\s*$', t, re.M)
    seg = t[m.end():] if m else ''
    e = seg.find('Enough! or Too much')
    seg = seg[:e + len('Enough! or Too much.')] if e > 0 else seg
    paras = [norm(p) for p in re.split(r'\n\s*\n', seg)]
    units = [(k+1, p) for k, p in enumerate([p for p in paras if len(p) > 12])]
    emit('Blake, Proverbs of Hell', units, None,
         author='William Blake', author_dates='1757-1827', composed='c. 1790-1793',
         translator=None, translation_year=None,
         source='Gutenberg 45315', pd_basis='English original',
         note='unnumbered in source; scholarly count from the plates is 70')

# ---------------------------------------------------------------- 11. Wilde
def wilde():
    t = body('wilde_misc_14062.txt')
    i = t.find('PHRASES AND PHILOSOPHIES FOR THE USE OF THE YOUNG')
    seg = t[i:] if i > 0 else ''
    seg = seg[len('PHRASES AND PHILOSOPHIES FOR THE USE OF THE YOUNG'):]
    end = re.search(r'\n\s*[A-Z][A-Z \-]{12,}\s*\n', seg)
    if end: seg = seg[:end.start()]
    paras = [norm(p) for p in re.split(r'\n\s*\n', seg)]
    paras = [p for p in paras if len(p) > 15 and not p.startswith('(Chameleon')]
    units = [(k+1, p) for k, p in enumerate(paras)]
    emit('Wilde, Phrases and Philosophies for the Use of the Young', units, None,
         author='Oscar Wilde', author_dates='1854-1900', composed='1894',
         translator=None, translation_year=None,
         source='Gutenberg 14062 (Miscellanies, ed. Ross 1908)', pd_basis='English original')

# ---------------------------------------------------------------- 12. Epictetus
def epictetus():
    t = body('epictetus_10661.txt')
    i = t.find('THE ENCHEIRIDION')
    seg = t[i:] if i > 0 else t
    idx = [(roman(m.group(1)), m.start(), m.end())
           for m in re.finditer(r'^\s*([IVXL]{1,8})\.\s*$', seg, re.M)]
    seq, want = [], 1
    for n, s, e in idx:
        if n == want: seq.append((n, s, e)); want += 1
    units = []
    for k, (n, s, e) in enumerate(seq):
        stop = seq[k+1][1] if k+1 < len(seq) else len(seg)
        units.append((n, norm(trim_tail(seg[e:stop]))))
    emit('Epictetus, Encheiridion', units, 52,
         author='Epictetus (comp. Arrian)', author_dates='c. 50-135 AD', composed='c. 125 AD',
         translator='George Long', translation_year=1877,
         source='Gutenberg 10661', pd_basis='translation pub. 19th c.',
         note='Long merges into 52 chapters; most modern editions give 53')

# ---------------------------------------------------------------- 13. Nietzsche BGE ch. IV
def nietzsche():
    t = body('nietzsche_bge_4363.txt')
    idx = [(int(m.group(1)), m.start(), m.end())
           for m in re.finditer(r'^\s*(\d{1,3})\.\s', t, re.M)]
    seq, want = [], 1
    for n, s, e in idx:
        if n == want: seq.append((n, s, e)); want += 1
    allu = []
    for k, (n, s, e) in enumerate(seq):
        stop = seq[k+1][1] if k+1 < len(seq) else len(t)
        allu.append((n, norm(t[e:stop])))
    units = [(n, x) for n, x in allu if 63 <= n <= 185]
    emit('Nietzsche, Apophthegms and Interludes (BGE ch. IV)', units, None,
         author='Friedrich Nietzsche', author_dates='1844-1900', composed='1886',
         translator='Helen Zimmern', translation_year=1907,
         source='Gutenberg 4363', pd_basis='translation pub. 1907',
         note='sections 63-185 of Beyond Good and Evil; the pure-aphorism chapter')

# ---------------------------------------------------------------- 14. Twain
def twain():
    t = body('twain_puddnhead_102.txt')
    units = []
    for m in re.finditer(r"(?s)\n\n((?:(?!\n\n).)+?)--Pudd.nhead\s+Wilson.s\s+Calendar\.", t):
        txt = norm(m.group(1))
        if 10 < len(txt) < 2000: units.append((len(units)+1, txt))
    emit("Twain, Pudd'nhead Wilson's Calendar", units, None,
         author='Mark Twain', author_dates='1835-1910', composed='1894',
         translator=None, translation_year=None,
         source='Gutenberg 102', pd_basis='English original',
         note='chapter epigraphs; unnumbered in source')

# ---------------------------------------------------------------- 15. Halifax
def halifax():
    t = body('halifax_35708.txt')
    i = t.find('POLITICAL, MORAL, AND MISCELLANEOUS')
    seg = t[i:] if i > 0 else t
    seg = re.sub(r'\[Sidenote:([^\]]*)\]', r'\n\n@@TOPIC:\1@@\n\n', seg)
    topic = None; units = []
    for p in re.split(r'\n\s*\n', seg):
        p = p.strip()
        m = re.match(r'@@TOPIC:(.*)@@', p)
        if m: topic = norm(m.group(1)).strip('_ .'); continue
        p = norm(p)
        if len(p) > 40 and not re.fullmatch(r'[A-Z ,\.\-]+', p):
            units.append((f'{topic or "-"}#{len(units)+1}', p))
    emit('Halifax, Political, Moral and Miscellaneous Reflections', units, None,
         author='George Savile, 1st Marquess of Halifax', author_dates='1633-1695', composed='before 1695; pub. 1750',
         translator=None, translation_year=None,
         source='Gutenberg 35708', pd_basis='English original, pub. 1750',
         note='UNNUMBERED in source - paragraph split is a measurement, not a published count')

# ---------------------------------------------------------------- 16. Bierce
def bierce():
    t = body('bierce_972.txt')
    units = []
    for m in re.finditer(r'^([A-Z][A-Z\' \-]{2,30}),\s+(n\.|v\.|v\.i\.|v\.t\.|adj\.|adv\.|pron\.|interj\.)',
                         t, re.M):
        s = m.start(); nxt = t.find('\n\n', m.end())
        units.append((m.group(1).strip(), norm(t[s:nxt if nxt > 0 else len(t)])))
    emit("Bierce, The Devil's Dictionary", units, None,
         author='Ambrose Bierce', author_dates='1842-c.1914', composed='1881-1906; pub. 1911',
         translator=None, translation_year=None,
         source='Gutenberg 972', pd_basis='English original',
         note='satirical-definition form, not maxim form; adjacent genre')

for fn in (publilius, larochefoucauld, chamfort, goethe, hazlitt, labruyere, pascal,
           ptahhotep, havamal, blake, wilde, epictetus, nietzsche, twain, halifax, bierce):
    try: fn()
    except Exception as ex:
        print(f'!! {fn.__name__} FAILED: {type(ex).__name__}: {ex}')

with open(os.path.join(OUT, 'maxims.jsonl'), 'w', encoding='utf-8') as f:
    for r in RECORDS: f.write(json.dumps(r, ensure_ascii=False) + '\n')
print(f'\nTOTAL UNITS: {len(RECORDS)}')
