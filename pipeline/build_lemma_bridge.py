# prov: 2026-10-01 claude drafted (moved from Veritas-Essential-Services/vocabularium PR #2; model name withheld by session policy)
# fable_review: pending
"""Build the KJV / Early Modern English lemma bridge.

A lemma bridge is a table that maps an archaic spelling or inflected form
("sheweth", "holpen", "spake", "thee") to the modern headword a reader would
search for ("show", "help", "speak", "you"). SQLite's full-text search stems
modern English only, so without this table a search for "show" silently misses
every "shew" in the King James Version.

Every mapping comes from one of two places, and records which:
  * a stated RULE (the regular Early Modern verb endings, see RULES below),
    whose result must be a verb in a dictionary before it is accepted; or
  * a SOURCE line quoted from Webster's 1828 or 1913 dictionary (both public
    domain, already in data/sources/).
Anything ambiguous, or where the sources disagree, goes to the needs-review
list instead of the bridge. Nothing is typed in by hand except the closed
list of pronouns and modal verbs, and each of those cites Webster too.

Required by Word Hoard ADR 0012 ("without the bridge a concordance is silently
wrong"); this file is its specification in code. Search side: expand_query() in
pipeline/lemma_bridge.py (Python) and exports/lemma-bridge/lemma-bridge.js (browser).

Inputs:
    data/greppable/kjv.tsv  this repo's KJV (pythonbible-kjv), read as is
    the Webster 1828/1913 and Wordset dictionaries, the wordfreq ranks and the modern
    irregular-verb table, read from a sibling Vocabularium checkout (they live there,
    and are only needed to REBUILD; the built table is committed). Found via
    --vocabularium DIR, else $VOCABULARIUM_DIR, else ../vocabularium or
    "../Vocabularium Website".

Usage:
    python3 pipeline/build_lemma_bridge.py            # rebuild data/lemma_bridge/
    python3 pipeline/build_lemma_bridge.py --check    # rebuild to a temp dir; fail unless byte-identical
    python3 pipeline/build_lemma_bridge.py --text more.txt   # add other Early Modern texts

Outputs (data/lemma_bridge/, committed):
    kjv_lemma_bridge.json   the bridge: form -> lemmas, with rule/source per form
    needs_review.csv        uncertain mappings, NOT used by search
    REPORT.md               coverage on Psalms + Proverbs, with examples
"""
import argparse, csv, filecmp, gzip, io, json, os, re, sys, tempfile
from collections import Counter, defaultdict
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
OUT = PROJ / 'data' / 'lemma_bridge'
KJV = PROJ / 'data' / 'greppable' / 'kjv.tsv'
DATA = None   # the Vocabularium data/ folder, set by use_vocabularium()

RULES = {
    'R1-eth':  'Third person singular -eth: strip it; the base must be a dictionary verb '
               '(walketh->walk, loveth->love, sinneth->sin, crieth->cry). Spelling tie-breaks: a '
               'one-syllable consonant-vowel-consonant base takes its silent e (hateth->hate, not hat); '
               'a doubled consonant is undone only if that leaves such a base (planneth->plan, '
               'falleth->fall); if two bases still fit, keep the one the text itself uses '
               '(singeth->sing, not singe), otherwise send it to review.',
    'R2-est':  'Second person singular -est: strip it; the base must be a dictionary verb, or a '
               'past tense that Webster 1828 lists under a verb (sayest->say, knewest->knew->know). '
               'If the base is also an adjective (superlative risk, e.g. "openest") the form must '
               'appear next to "thou" in the corpus.',
    'R3-edst': 'Second person singular past -edst: strip it; the base must be a dictionary verb (lovedst->love).',
    'R4-st':   'Second person singular -st on a modal or a past tense: canst->can, hadst->had->have, '
               'saidst->said->say. Modals are the closed class can, could, may, might, must, shall, '
               'should, will, would, and keep their own form (couldest->could).',
    'R5-regular': 'Regular modern ending (-ed, -d, -ing, -s, -es) on an old SPELLING already in the '
                  'bridge: same lemma (shewed->shew->show, enquired->enquire->inquire). Never on an old '
                  'inflection (gates is not gat + -es).',
    'D-1828':  'Webster 1828: a form entry ("GAT, preterit tense of get."); a verb entry that lists its '
               'preterit/participle ("FORSAKE ... preterit tense forsook"), or marks one obsolete ("[forgat, '
               'obsolete]", "Holden is obsolete", "holp and holpen being obsolete"); "It is sometimes '
               'written shew, shewed, shewn"; "In lieu of this, establish is now always used". A form that '
               'is also a modern word needs a short plain entry, or it goes to review.',
    'D-1913':  'Webster 1913 sense opening "imp./p. p./2d pers. sing./3d pers. sing. of X" or "of X"; a '
               'one-word gloss that is itself a form of a verb (hath: "Has."); or "See X"/"Same as X" '
               'where the spellings differ by at most 2 letters, the form is rarer than X, and (if it is '
               'a modern word) every sense of it points to X. A modern word needs every 1913 sense to '
               'point to X, or a second-person form the text uses beside "thou" (wilt, art).',
    'P-pronoun': 'Second person pronouns (thee, thou, ye -> you; thy -> your; thine -> your, yours; '
                 'thyself -> yourself), each quoted from Webster.',
    'A-reviewed': 'Decided by a person: data/lemma_bridge/review_decisions.csv records who, when and the '
                  'verse that settled it. "bridge" rows enter the table; "keep-out" rows leave the review '
                  'list as decided. Never edit the JSON by hand: add a row there and rebuild.',
    'C-chain': 'A lemma that is itself an archaic form is followed to its own lemma '
               '(sheweth->shew->show).',
}

MODERN_TOP = 3000
W1913 = {}
ADJS = set()
IRREG = {}      # modern irregulars, went->go: data/config/irregulars.json in Vocabularium
MODALS = {'can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would'}
ARCHAIC_WORDS = re.compile(r'\b(obs\.?|obsolete|archaic|antiquated|old|ancient|solemn|'
                           r'sometimes written|formerly|poetic|rare)\b', re.I)
GRAMMAR = {'preterit', 'tense', 'participle', 'passive', 'and', 'or', 'of', 'the', 'no', 'obs',
           'obsolete', 'old', 'pp', 'imp', 'pret', 'verb', 'transitive', 'intransitive', 'is',
           'sometimes', 'written', 'also', 'formerly', 'see', 'being', 'regular', 'a', 'in'}

# The pronoun rule: form -> (lemmas, source, quote). Quotes are verbatim Webster.
PRONOUNS = {
    'thou':    (['you'], 'Webster 1828 "YE"', 'The nominative plural of the second person, of which thou is the singular. ... In common discourse and writing, you is exclusively used.'),
    'thee':    (['you'], 'Webster 1913 "thee"', 'The objective case of thou. See Thou.'),
    'ye':      (['you'], 'Webster 1828 "YE"', 'The nominative plural of the second person, of which thou is the singular. ... In common discourse and writing, you is exclusively used.'),
    'thy':     (['your'], 'Webster 1913 "thy"', 'the more common form of thine, possessive case of thou'),
    'thine':   (['your', 'yours'], 'Webster 1913 "thine"', 'A form of the possessive case of the pronoun thou, now superseded in common discourse by your'),
    'thyself': (['yourself'], 'Webster 1913 "thyself"', 'An emphasized form of the personal pronoun of the second person'),
}


def use_vocabularium(arg=None):
    """Point DATA at a Vocabularium checkout's data/ folder and load its irregular-verb table."""
    global DATA
    tries = [arg, os.environ.get('VOCABULARIUM_DIR'),
             PROJ.parent / 'vocabularium', PROJ.parent / 'Vocabularium Website']
    for t in tries:
        if t and (Path(t) / 'data' / 'sources' / 'webster1913.json.gz').exists():
            DATA = Path(t) / 'data'
            IRREG.update(json.load(open(DATA / 'config' / 'irregulars.json')))
            return DATA
    sys.exit('build_lemma_bridge: no Vocabularium checkout found (tried %s). The dictionaries live '
             'there; pass --vocabularium DIR. The built table in data/lemma_bridge/ is committed, '
             'so search does not need this.' % ', '.join(str(t) for t in tries if t))


# ---------------------------------------------------------------- corpus
def read_kjv():
    """(book, chapter, verse, text) from data/greppable/kjv.tsv: "kjv:Ps.86.17<TAB>text"."""
    rows = []
    with open(KJV, encoding='utf-8') as f:
        next(f)                                   # header: id, text
        for line in f:
            uid, text = line.rstrip('\n').split('\t', 1)
            book, ch, vs = uid.split(':', 1)[1].rsplit('.', 2)
            rows.append((book, int(ch), int(vs), text))
    return rows


def tokens(text):
    """Split like SQLite's default tokenizer: letters only, apostrophes and hyphens split."""
    return re.findall(r'[A-Za-z]+', text)


class Corpus:
    def __init__(self, texts):
        self.count = Counter()
        self.lower_seen = set()   # appears at least once in lower case -> not only a proper name
        self.thou_near = Counter()
        for text in texts:
            toks = tokens(text)
            low = [t.lower() for t in toks]
            for i, (t, l) in enumerate(zip(toks, low)):
                self.count[l] += 1
                if t[0].islower():
                    self.lower_seen.add(l)
                if 'thou' in low[max(0, i - 3):i + 4]:
                    self.thou_near[l] += 1


# ---------------------------------------------------------------- dictionaries
def load_sources():
    def gz(name):
        return json.load(gzip.open(DATA / 'sources' / (name + '.json.gz'), 'rt'))
    return gz('webster1828'), gz('webster1913'), gz('wordset')


def word_freq():
    """wordfreq Zipf frequency for the top 50,000 modern words (0 if absent)."""
    with open(DATA / 'raw_ranks_50k.csv') as f:
        return {r['word']: float(r['zipf_frequency']) for r in csv.DictReader(f)}


def modern_words(wordset):
    """A 'modern' word: a Wordset headword, one of the 3,000 most frequent modern words
    (wordfreq, for function words Wordset leaves out; archaic words start lower: ye is #4,729,
    thou #5,558, hath #12,617), or a modern irregular verb form."""
    words = set(wordset)
    with open(DATA / 'raw_ranks_50k.csv') as f:
        words |= {r['word'] for r in csv.DictReader(f) if int(r['raw_rank']) <= MODERN_TOP}
    words |= set(IRREG)
    return words


def modern_inflection(w, modern):
    """True if w is a regular modern inflection of a modern word (Porter already handles these)."""
    for suf, rep in [('ies', 'y'), ('ied', 'y'), ('es', ''), ('s', ''), ('ed', ''), ('ed', 'e'),
                     ('d', ''), ('ing', ''), ('ing', 'e'), ('er', ''), ('ly', '')]:
        if w.endswith(suf) and len(w) > len(suf) + 1:
            b = w[:-len(suf)] + rep
            if b in modern or (len(b) > 2 and b[-1] == b[-2] and b[:-1] in modern):
                return True
    return False


def modern_inflection_of(form, lemma):
    """showed/shown/showing are regular modern forms of show, not archaic ones."""
    return any(form == x for x in (lemma + 's', lemma + 'es', lemma + 'ed', lemma + 'd', lemma + 'n',
                                   lemma + 'ing', lemma[:-1] + 'ing', lemma[:-1] + 'ied'))


def pos_sets(w1828, w1913, wordset):
    """Verbs and adjectives. A word is a verb if Wordset says so, Webster 1828 has a
    "WORD, verb" entry, or a Webster 1913 sense opens "To ..." (how Webster defines a verb:
    water, "5. To wet or supply with water")."""
    verbs, adjs = set(), set()
    for w, senses in wordset.items():
        for s in senses:
            if s.get('pos') == 'verb':
                verbs.add(w)
            elif s.get('pos') == 'adjective':
                adjs.add(w)
    for w, text in w1828.items():
        if re.search(r"(?m)^[A-Z'\-]+(?:, [A-Z'\-]+)*,? verb\b", text):   # any entry under this key
            verbs.add(w)
    for w, text in w1913.items():
        if any(re.match(r'To [a-z]', sense) for sense in senses_1913(text)):
            verbs.add(w)
    return verbs, adjs


def clean(s):
    return re.sub(r'\s+', ' ', s.replace('[uCode:', '')).strip()


def edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def senses_1913(text):
    return [clean(s) for s in re.split(r'(?:^|\s)\d+\.\s', text) if clean(s)]


def dictionary_maps(w1828, w1913):
    """Yield (form, lemma, source, quote, kind) found in Webster.

    kind: 'inflection' (preterit, participle, person ending), 'variant' (spelling),
          'gloss' (the dictionary glosses the form with a modern inflected word).
    """
    out = []
    # --- Webster 1828: one dict value may hold several entries, one per line.
    for key, text in w1828.items():
        if not re.fullmatch(r'[a-z]+', key):
            continue
        for line in text.split('\n'):
            m = re.match(r"^((?:[A-Z][A-Z'\-]*(?:, ?)?)+)\s*(.*)", line)
            if not m:
                continue
            heads = [h.replace("'", '').lower() for h in re.findall(r"[A-Z][A-Z'\-]*", m.group(1))]
            heads = [h for h in heads if re.fullmatch(r'[a-z]+', h)]
            rest = clean(m.group(2))
            head = key
            # (a) a form entry: "GAT, preterit tense of get."
            fm = re.match(r"^(?:the |an? )?(?:old |antiquated |obsolete )?"
                          r"(?:preterit|past tense|participle)(?: tense| passive)?"
                          r"(?:,? (?:and|or) (?:participle|preterit)(?: tense| passive| present tense)?)?"
                          r",?\s+of (?:the (?:substantive |obsolete )?verb,? )?([a-z]+)\b", rest, re.I)
            if fm:
                lemma = 'be' if 'substantive verb' in rest[:80] else fm.group(1).lower()
                for h in heads:
                    out.append((h, lemma, 'Webster 1828 "%s"' % h.upper(),
                                rest[:140], 'inflection'))
                continue
            # (b) a verb entry that lists its own preterit / participle
            if re.match(r'^verb\b', rest):
                head_txt = rest[:260]
                for clause in re.findall(r'(?:preterit(?: tense)?|participle passive)\s+([^;.\[]+)', head_txt):
                    for form in re.findall(r'[a-z]+', clause.lower()):
                        if form not in GRAMMAR and form != head and len(form) > 1:
                            out.append((form, head, 'Webster 1828 "%s"' % head.upper(),
                                        head_txt[:140], 'listed'))
                # "[forgat, obsolete ]", "[brake.obs.]", "Holden is obsolete in elegant writing."
                for om in re.finditer(r'\[([a-z]+)[.,]?\s*(?:obs\b|obsolete)|\b([A-Za-z]+) is (?:now )?obsolete',
                                      rest[:400]):
                    form = (om.group(1) or om.group(2)).lower()
                    if form[:2] == head[:2] and form != head:
                        out.append((form, head, 'Webster 1828 "%s"' % head.upper(), om.group(0), 'inflection'))
                # "the old past tense and participle holp and holpen being obsolete"
                om = re.search(r'old (?:past tense|preterit)[a-z ]*? participle ([a-z]+(?: and [a-z]+)*) being obsolete', head_txt)
                if om:
                    for form in om.group(1).split(' and '):
                        out.append((form, head, 'Webster 1828 "%s"' % head.upper(),
                                    om.group(0), 'inflection'))
            # (c) a verb Webster says has been replaced: STABLISH "In lieu of this, establish is now used"
            if re.match(r'^verb\b', rest):
                rm = re.search(r'In lieu of this,? ([a-z]+) is (?:now )?(?:always )?used', rest)
                if rm:
                    out.append((head, rm.group(1), 'Webster 1828 "%s"' % head.upper(), rm.group(0), 'replaced'))
            # (d) "It is sometimes written shew, shewed, shewn."
            for vm in re.finditer(r'(?:sometimes|formerly|anciently) written ((?:[a-z]+(?:, | and | or )?)+)', rest):
                for form in re.findall(r'[a-z]+', vm.group(1)):
                    if form not in GRAMMAR:
                        out.append((form, head, 'Webster 1828 "%s"' % head.upper(),
                                    vm.group(0), 'variant'))
    # --- Webster 1913: numbered senses
    for form, text in w1913.items():
        if not re.fullmatch(r'[a-z]+', form):
            continue
        for s in senses_1913(text):
            m = re.search(r'\b(?:imp\.|p\. ?p\.|pret\.|pres\.|pers\.|per\.|sing\.|preterit|participle|person singular)'
                          r'.{0,60}?\bof (?:the (?:substantive )?verb )?([A-Z][a-z]+|be\b)', s[:200])
            if m and m.start() > 40:
                m = None                     # the grammar label must open the sense, not sit deep in it
            if m:
                s = s[:200]
                out.append((form, m.group(1).lower(), 'Webster 1913 "%s"' % form, s, 'inflection'))
                g = re.search(r'\bof [A-Z][a-z]+, to ([a-z]+)\b', s)      # "of Wit, to know"
                if g:
                    out.append((form, g.group(1), 'Webster 1913 "%s"' % form, s, 'inflection'))
                continue
            m = re.match(r'^of ([A-Z][a-z]+)\.', s)                          # doth: "of Do."
            if m:
                out.append((form, m.group(1).lower(), 'Webster 1913 "%s"' % form, s, 'inflection'))
                continue
            m = re.match(r'^(?:See|Same as) ([A-Z][a-z]+)\.?$', s)
            if m:
                out.append((form, m.group(1).lower(), 'Webster 1913 "%s"' % form, s, 'variant'))
                continue
            m = re.match(r'^([A-Z][a-z]+)\.$', s)                            # hath: "Has."
            if m:
                out.append((form, m.group(1).lower(), 'Webster 1913 "%s"' % form, s, 'gloss'))
    return out


# ---------------------------------------------------------------- rules
def rule_quote(form, lemmas, rule):
    """The worked example stored with a rule-made form: "ordaineth = ordain + -eth"."""
    return '%s = %s + -%s (see rules.%s)' % (form, ' / '.join(lemmas), rule.split('-')[1], rule)


def cvc(stem):
    """Short stem ending consonant-vowel-consonant (hat, rid, hop): English would double it."""
    return (len(re.findall(r'[aeiouy]+', stem)) == 1
            and re.search(r'[^aeiou][aeiou][^aeiouwxy]$', stem) is not None)


def base_candidates(stem):
    c = [stem, stem + 'e']
    if len(stem) > 2 and stem[-1] == stem[-2]:
        c.append(stem[:-1])
    if stem.endswith('i'):
        c.append(stem[:-1] + 'y')
    return c


class Bridge:
    def __init__(self):
        self.main = {}      # form -> {'lemmas': [...], 'rule': str, 'source': str, 'quote': str}
        self.review = []    # rows for needs_review.csv

    def add(self, form, lemmas, rule, source='', quote=''):
        e = self.main.setdefault(form, {'lemmas': [], 'rule': rule, 'source': source, 'quote': quote,
                                        'archaic': True})
        for l in lemmas:
            if l not in e['lemmas'] and l != form:
                e['lemmas'].append(l)

    def flag(self, form, lemmas, reason, source='', quote=''):
        self.review.append({'form': form, 'candidate_lemmas': ' | '.join(lemmas),
                            'reason': reason, 'source': source, 'quote': quote})


def apply_rules(form, verbs, adjs, past_of, corpus):
    """Return (lemmas, rule, problem) for a regular Early Modern ending, or None."""
    def resolve(stem, allow_past):
        """base -> set of lemmas. A base can read two ways: sawest = saw (cut) or saw (past of see)."""
        hits = {}
        for c in base_candidates(stem):
            if c in MODALS or c in verbs:
                hits.setdefault(c, set()).add(c)
            if allow_past and c in past_of:
                hits.setdefault(c, set()).add(past_of[c])
        return hits

    for suf, rule in (('edst', 'R3-edst'), ('eth', 'R1-eth'), ('est', 'R2-est'), ('st', 'R4-st')):
        if not form.endswith(suf) or len(form) - len(suf) < 2:
            continue
        stem = form[:-len(suf)]
        allow_past = suf in ('est', 'st')
        hits = resolve(stem, allow_past)
        if suf == 'st':               # -st only on modals and past tenses (canst, didst)
            hits = {c: l for c, l in hits.items() if c in MODALS or c in past_of}
        hits = {c: ({c} if c in MODALS else l) for c, l in hits.items()}   # couldest -> could
        if not hits:
            continue
        # tie-breaks, each a stated spelling rule
        if len(hits) > 1 and stem in hits and stem + 'e' in hits and cvc(stem):
            hits = {stem + 'e': hits[stem + 'e']}             # hateth -> hate, not hat
        if len(hits) > 1 and stem in hits and stem[:-1] in hits and stem[-1:] == stem[-2:-1]:
            keep = stem[:-1] if cvc(stem[:-1]) else stem       # planneth -> plan; falleth -> fall
            hits = {keep: hits[keep]}
        lemmas = sorted(set().union(*hits.values()))
        if len(lemmas) > 1:           # keep the one the text itself uses (singeth: sing, not singe)
            used = [l for l in lemmas if corpus.count[l]]
            if len(used) == 1:
                lemmas = used
            else:
                return lemmas, rule, 'more than one base fits: ' + ', '.join(sorted(hits))
        if suf == 'est':
            base = next(iter(hits))
            if base in adjs and corpus.thou_near[form] == 0:
                return lemmas, rule, 'base "%s" is also an adjective and the form never appears near "thou" (could be a superlative)' % base
        return lemmas, rule, None
    return None


# ---------------------------------------------------------------- build
def build(extra_texts):
    kjv = read_kjv()
    corpus = Corpus([t for *_, t in kjv] + extra_texts)
    w1828, w1913, wordset = load_sources()
    W1913.update(w1913)
    modern = modern_words(wordset)
    verbs, adjs = pos_sets(w1828, w1913, wordset)
    ADJS.update(adjs)
    dmaps = dictionary_maps(w1828, w1913)

    freq = word_freq()

    def confirmed(form, lemma):
        """A form listed inside a verb entry is trusted only if the text uses it, or its own
        entry points back. Webster 1828 prints STINK "preterit tense stand or stunk" and SMITE
        "participle passive smitten, smil" (for smit)."""
        own = (w1913.get(form, '') + ' ' + w1828.get(form, '')).lower()
        points_back = re.search(r'\bof %s\b' % re.escape(lemma), own) is not None
        if form in modern:
            return points_back
        return form in corpus.lower_seen or points_back

    dmaps = [m for m in dmaps if m[4] != 'listed' or confirmed(m[0], m[1])]
    # past tense -> verb, from Webster 1828 (used by R2/R4 and for one-word glosses)
    past_of, principal = {}, defaultdict(set)
    for form, lemma, source, quote, kind in dmaps:
        if kind in ('inflection', 'listed') and source.startswith('Webster 1828') and lemma in verbs:
            past_of.setdefault(form, lemma)
        if kind == 'listed':
            principal[lemma].add(form)          # the standard parts a verb entry lists first

    def archaic(form, lemma, quote):
        """False for a modern irregular (went -> go; arose -> arise): kept, but labelled."""
        if any(kind == 'variant' and only_points_to(lemma, target) for target, _, _, kind in by_form.get(lemma, [])):
            return True                         # shewn is "p. p. of Shew", and shew is old already
        if IRREG.get(form) == lemma or modern_inflection_of(form, lemma) or form in MODALS:
            return False                        # would -> will is modern English
        if ARCHAIC_WORDS.search(quote):
            return True
        return not (form in principal[lemma] and form in freq)

    bridge = Bridge()
    for form, (lemmas, source, quote) in PRONOUNS.items():
        bridge.add(form, lemmas, 'P-pronoun', source, quote)

    # 1. dictionary mappings
    by_form = defaultdict(list)
    for form, lemma, source, quote, kind in dmaps:
        if form == lemma or form in PRONOUNS:
            continue
        by_form[form].append((lemma, source, quote, kind))
    for form, maps in sorted(by_form.items()):
        good, doubtful = [], []
        in_corpus = form in corpus.lower_seen
        own_word = form in modern               # a modern word in its own right (bare, say, isle)
        for lemma, source, quote, kind in maps:
            if kind == 'variant':
                # a spelling variant: only words the text uses; never a modern word with other
                # senses (isle is also "island"); never a word commoner than its "variant"
                # (confident is not an old spelling of confidant)
                if (not in_corpus or modern_inflection(form, modern)
                        or (own_word and not only_points_to(form, lemma))
                        or freq.get(form, 0) > freq.get(lemma, 0)):
                    continue
                if edit_distance(form, lemma) <= 2:
                    good.append((lemma, source, quote, True))
                else:
                    doubtful.append((lemma, source, quote, 'cross-reference, not a near spelling: may be a synonym'))
                continue
            if kind == 'gloss':                 # hath: "Has."  ->  has is a form of have
                real = past_of.get(lemma) or IRREG.get(lemma)
                if real in verbs and real != form:
                    quote, lemma = quote + ' (%s is a form of %s)' % (lemma, real), real
                else:
                    if in_corpus and not own_word and not modern_inflection(form, modern):
                        doubtful.append((lemma, source, quote,
                                         'one-word gloss: a near spelling, but Webster does not call it a variant'
                                         if edit_distance(form, lemma) <= 2 else
                                         'one-word gloss: a synonym, not an inflection'))
                    continue
            if kind == 'replaced':
                if lemma in verbs and in_corpus:
                    good.append((lemma, source, quote, True))
                continue
            # inflections
            if form in IRREG and IRREG[form] != lemma:
                continue                        # the modern table wins: went is go, not wend
            if not (lemma in verbs or lemma in MODALS or lemma == 'be' or lemma in by_form):
                continue
            is_old = archaic(form, lemma, quote)
            first_sentence = quote.split('. ')[0]
            # a modern word given an OLD sense (say = "Saw.") needs Webster 1828 saying so plainly
            plain_1828 = (source.startswith('Webster 1828') and kind in ('inflection', 'listed')
                          and (len(first_sentence) <= 100 or ARCHAIC_WORDS.search(quote)))
            # ... or Webster 1913 with no other sense (woven: "p. p. of Weave"), or a
            # second-person form the text uses next to "thou" at least half the time (wilt, art)
            thou_form = (re.search(r'\b(?:2d|second) per', quote) is not None
                         and corpus.thou_near[form] * 2 >= corpus.count[form] > 0)
            if own_word and is_old and not (plain_1828 or only_points_to(form, lemma) or thou_form):
                if in_corpus:
                    doubtful.append((lemma, source, quote, 'a modern word, and Webster 1828 does not give it '
                                     'as a plain inflection: search would drown in the modern sense'))
                continue
            if in_corpus or is_old:             # modern irregulars only when the text uses them
                good.append((lemma, source, quote, is_old))
        for lemma, source, quote, is_old in good:
            bridge.add(form, [lemma], 'D-1913' if '1913' in source else 'D-1828', source, quote)
        if good:
            bridge.main[form]['archaic'] = all(is_old for *_, is_old in good)   # lay: IRREG says modern
        for lemma, source, quote, why in doubtful:
            if form not in bridge.main:
                bridge.flag(form, [lemma], why, source, quote)

    # 2. rules, over every lower-case word in the corpus that is not a modern word
    for form in sorted(corpus.lower_seen):
        if form in bridge.main or form in modern:
            continue
        r = apply_rules(form, verbs, adjs, past_of, corpus)
        if not r:
            continue
        lemmas, rule, problem = r
        if problem:
            bridge.flag(form, lemmas, problem, rule, rule_quote(form, lemmas, rule))
        else:
            bridge.add(form, lemmas, rule, 'rule', rule_quote(form, lemmas, rule))

    # 3. a dictionary form whose regular ending the rules read differently: seeth is
    #    "imp. of Seethe" in Webster 1913, but by R1 it is see + -eth.
    conflicts = []
    for form, e in bridge.main.items():
        if e['rule'] not in ('D-1913', 'D-1828') or form not in corpus.lower_seen:
            continue
        r = apply_rules(form, verbs, adjs, past_of, corpus)
        if r and not r[2] and not set(r[0]) & (set(e['lemmas']) | {
                l2 for l in e['lemmas'] for l2 in bridge.main.get(l, {}).get('lemmas', [])}):
            conflicts.append((form, r[0], r[1], e))
    for form, rule_lemmas, rule, e in conflicts:
        bridge.flag(form, e['lemmas'], 'Webster says this; the regular %s ending says %s, which the bridge uses'
                    % (rule[3:], ', '.join(rule_lemmas)), e['source'], e['quote'])
        bridge.main[form] = {'lemmas': rule_lemmas, 'rule': rule, 'source': 'rule',
                             'quote': rule_quote(form, rule_lemmas, rule), 'archaic': True}

    # 4. homographs: a form that is ALSO a modern word with a meaning of its own (brake = a fern).
    #    Search expands FROM the lemma to a homograph, never from the homograph to the lemma.
    def mark_homographs():
        for form, e in bridge.main.items():
            e['homograph'] = e['rule'] != 'P-pronoun' and is_homograph(form, e['lemmas'], modern, w1913)
    mark_homographs()

    # 5. chain: follow a lemma that is itself a bridged form (sheweth -> shew -> show)
    for _ in range(4):
        changed = False
        for form, e in bridge.main.items():
            new = []
            for l in e['lemmas']:
                nxt = bridge.main.get(l)
                follow = nxt and not nxt['homograph'] and nxt['rule'] != 'P-pronoun'
                for l2 in (nxt['lemmas'] if follow else [l]):
                    if l2 not in new and l2 != form:
                        new.append(l2)
            if new != e['lemmas']:
                e['lemmas'] = new
                changed = True
                if 'C-chain' not in e['rule']:
                    e['rule'] += '+C-chain'
        if not changed:
            break

    # 6. R5: regular modern endings on a bridged archaic form (shewed, shewing). Listed
    #    even though a porter index would find them: armarium's index has no stemmer.
    for form in sorted(corpus.lower_seen):
        if form in bridge.main or form in modern:
            continue
        for suf, rep in [('ed', ''), ('d', ''), ('ing', ''), ('ing', 'e'), ('s', ''), ('es', '')]:
            b = form[:-len(suf)] + rep if form.endswith(suf) else None
            if b and b in bridge.main and is_spelling_variant(bridge.main[b]):
                bridge.add(form, bridge.main[b]['lemmas'], 'R5-regular', 'rule', '%s + -%s' % (b, suf))
                break
    mark_homographs()

    # 7. a person's decisions on review rows (review_decisions.csv)
    bridge.kept_out = apply_decisions(bridge, modern, w1913)

    # a flagged form may ALSO sit in the bridge only as the other side of a conflict (seeth)
    bridge.review = [r for r in bridge.review
                     if r['form'] not in bridge.main or 'which the bridge uses' in r['reason']]
    return bridge, corpus, kjv, modern


def apply_decisions(bridge, modern, w1913):
    """Fold review_decisions.csv into the bridge. A decision must name a form that is
    actually in the review list, or the build stops: a stale row is a mistake to see,
    not one to ignore. Returns the forms decided "keep-out"."""
    path = OUT / 'review_decisions.csv'
    if not path.exists():
        return set()
    pending = {r['form'] for r in bridge.review}
    kept_out = set()
    with open(path, encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f):
            form, decision = row['form'], row['decision']
            if form not in pending:
                sys.exit('review_decisions.csv: %r is not in the review list (already bridged, '
                         'or the rules changed); remove or fix that row' % form)
            if decision == 'bridge':
                lemmas = [l for l in row['lemmas'].split('|') if l]
                bridge.main[form] = {'lemmas': lemmas, 'rule': 'A-reviewed',
                                     'source': 'review by %s, %s' % (row['reviewed_by'], row['reviewed_on']),
                                     'quote': row['evidence'], 'archaic': True,
                                     'homograph': is_homograph(form, lemmas, modern, w1913)}
            elif decision == 'keep-out':
                kept_out.add(form)
            else:
                sys.exit('review_decisions.csv: %r has decision %r (use bridge or keep-out)' % (form, decision))
    bridge.review = [r for r in bridge.review if r['form'] not in kept_out
                     and not (r['form'] in bridge.main and bridge.main[r['form']]['rule'] == 'A-reviewed')]
    return kept_out


def is_spelling_variant(entry):
    """An old SPELLING of a modern verb (shew, enquire, stablish), not an old inflection
    (gat, hast, rang): only a spelling takes regular endings, so shewed is shew + -ed but
    gates is not gat + -es."""
    return (not entry['homograph'] and entry['rule'].startswith('D-')
            and re.search(r'^(?:See|Same as) |sometimes written|In lieu of this', entry['quote']) is not None)


def only_points_to(form, lemma):
    """Every Webster 1913 sense of the form mentions the lemma (shew: "See Show. Show.")."""
    senses = senses_1913(W1913.get(form, ''))
    return bool(senses) and all(mentions(s, lemma) for s in senses)


def mentions(text, word):
    return re.search(r'\b%s\b' % re.escape(word), text, re.I) is not None


def is_homograph(form, lemmas, modern, w1913):
    """True when the form is also a modern word with a sense that has nothing to do with its lemma."""
    if form not in modern:
        return False
    senses = senses_1913(w1913.get(form, ''))
    return not senses or any(not any(mentions(s, l) for l in lemmas) for s in senses)


# ---------------------------------------------------------------- report
def looks_modern(w, modern):
    """For the report only: a regular inflection, a comparative/superlative (heavier, vilest),
    or a plural like sheaves / kinsmen. Kept out of the rules on purpose: sayest is not vilest."""
    if modern_inflection(w, modern):
        return True
    for suf, rep in [('ier', 'y'), ('iest', 'y'), ('er', 'e'), ('est', ''), ('est', 'e'), ('ves', 'f'),
                     ('men', 'man')]:
        if w.endswith(suf) and len(w) > len(suf) + 2:
            b = w[:-len(suf)] + rep
            if b in modern or (b[-1] == b[-2] and b[:-1] in modern):
                if suf in ('est',) and b not in ADJS:
                    continue                    # -est on a verb is Early Modern (sayest), not a superlative
                return True
    return False


def report(bridge, modern, kjv, out):
    books = ('Ps', 'Prov')
    pp = Corpus([t for b, *_, t in kjv if b in books])
    lowered = sorted(pp.lower_seen)
    review_forms = {r['form'] for r in bridge.review}
    old = [w for w in lowered if w in bridge.main and bridge.main[w]['archaic']]
    modern_irreg = [w for w in lowered if w in bridge.main and not bridge.main[w]['archaic']]
    review = [w for w in lowered if w in review_forms and w not in bridge.main and w not in modern]
    old_sense = [w for w in lowered if w in review_forms and w not in bridge.main and w in modern]
    kept = getattr(bridge, 'kept_out', set())
    kept_out = [w for w in lowered if w in kept]
    residue = [w for w in lowered if w not in bridge.main and w not in review_forms and w not in kept
               and w not in modern and not looks_modern(w, modern)]
    total = len(old) + len(review) + len(kept_out) + len(residue)
    by_rule = Counter(bridge.main[w]['rule'].split('+')[0] for w in old)
    hits = sum(pp.count[w] for w in old)

    def ex(ws, n=40):
        return ', '.join('%s (%d)' % (w, pp.count[w]) for w in sorted(ws, key=lambda w: -pp.count[w])[:n])

    lines = [
        '# Lemma bridge coverage: KJV Psalms + Proverbs',
        '',
        'Generated by `pipeline/build_lemma_bridge.py`. Do not edit by hand. Counts are distinct',
        'lower-case word forms (so proper names are left out); the number after a word is how',
        'many times it occurs in the two books.',
        '',
        'An **archaic form** is one the bridge marks archaic, one in the review list that is not a',
        'modern word, or a word no source or rule reached that is not modern English (not a Wordset',
        'headword, not among the 3,000 commonest modern words, not a regular -s/-ed/-ing/-er form,',
        'comparative or plural of one).',
        '',
        '| archaic forms | distinct forms | share |',
        '|---|---:|---:|',
        '| Bridged | %d | %.0f%% |' % (len(old), 100 * len(old) / total),
        '| Needs review (`needs_review.csv`, not used by search) | %d | %.0f%% |' % (len(review), 100 * len(review) / total),
        '| Reviewed and kept out (`review_decisions.csv`) | %d | %.0f%% |' % (len(kept_out), 100 * len(kept_out) / total),
        '| Unbridged | %d | %.0f%% |' % (len(residue), 100 * len(residue) / total),
        '| **Total** | **%d** | |' % total,
        '',
        'The bridged archaic forms occur %d times in the two books.' % hits,
        '',
        'Not counted above:',
        '',
        '* %d modern irregular forms the bridge also carries, marked `"archaic": false` (so "go" '
        'finds "went"): %s' % (len(modern_irreg), ex(modern_irreg, 25)),
        '* %d modern words that Webster 1913 alone also gives an old sense (say = "saw"). Left out of '
        'the bridge so "see" does not drown in "say"; listed in the review file: %s' % (len(old_sense), ex(old_sense)),
        '',
        '## Bridged archaic forms, by how the mapping was made',
        '',
        '| rule / source | forms |', '|---|---:|',
    ] + ['| %s | %d |' % (r, n) for r, n in by_rule.most_common()] + [
        '',
        'Most frequent: ' + ex(old, 60),
        '',
        '## Needs review (%d)' % len(review),
        '',
        ex(review, 100) or '(none)',
        '',
        '## Reviewed and kept out (%d)' % len(kept_out),
        '',
        'A person looked and decided against a mapping (reasons in `review_decisions.csv`): '
        + (ex(kept_out, 100) or '(none)'),
        '',
        '## Unbridged (%d)' % len(residue),
        '',
        'All of them, most frequent first:',
        '',
        ex(residue, 10000) or '(none)',
        '',
    ]
    write(out / 'REPORT.md', '\n'.join(lines))
    return {'bridged': len(old), 'review': len(review), 'unbridged': len(residue), 'total': total,
            'kept_out': len(kept_out),
            'modern_irregular': len(modern_irreg), 'old_sense': len(old_sense)}


SOURCES = {
    'Webster 1828': 'Noah Webster, An American Dictionary of the English Language (1828). Public domain. '
                    'Parsed from github.com/DataWar/1828-dictionary (Vocabularium data/sources/webster1828.json.gz).',
    'Webster 1913': "Webster's Revised Unabridged Dictionary (1913). Public domain "
                    '(Vocabularium data/sources/webster1913.json.gz).',
    'Wordset': 'wordset/wordset-dictionary, CC BY-SA 4.0 (Vocabularium data/sources/wordset.json.gz). Used only '
               'to check that a rule-derived base is a real verb; no Wordset text is copied here.',
    'wordfreq': 'Top 50,000 wordfreq ranks, data CC BY-SA 4.0 (Vocabularium data/raw_ranks_50k.csv). Used only '
                'to decide what counts as a modern word; nothing is copied here.',
    'KJV': "King James Version, this repo's data/greppable/kjv.tsv (pythonbible-kjv, built by "
           'pipeline/build_kjv.py). The text is public domain (Crown letters patent apply in the UK only).',
}


def write(path, text):
    """Atomic: temp file + rename, so a killed run never leaves half a file (golden rule 5)."""
    tmp = path.with_name(path.name + '.tmp')
    with open(tmp, 'w', encoding='utf-8', newline='') as f:
        f.write(text)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--text', action='append', default=[], help='extra Early Modern English text file')
    ap.add_argument('--vocabularium', help='a Vocabularium checkout (holds the dictionaries)')
    ap.add_argument('--check', action='store_true', help='rebuild to a temp dir and compare; write nothing')
    args = ap.parse_args()
    use_vocabularium(args.vocabularium)
    extra = [Path(p).read_text(encoding='utf-8', errors='replace') for p in args.text]
    bridge, corpus, kjv, modern = build(extra)
    out = Path(tempfile.mkdtemp()) if args.check else OUT
    out.mkdir(exist_ok=True)
    doc = {
        'about': 'Maps archaic / Early Modern English (KJV) word forms to modern headwords, for search '
                 'query expansion. Built by pipeline/build_lemma_bridge.py; do not edit by hand.',
        'sources': SOURCES,
        'rules': RULES,
        'forms': {f: bridge.main[f] for f in sorted(bridge.main)},
    }
    # one form per line: readable in a diff, and a third the size of indented JSON
    head = json.dumps({k: v for k, v in doc.items() if k != 'forms'}, indent=1, ensure_ascii=False)
    body = ',\n'.join('  %s: %s' % (json.dumps(f), json.dumps(e, ensure_ascii=False))
                       for f, e in doc['forms'].items())
    write(out / 'kjv_lemma_bridge.json', head[:-2] + ',\n "forms": {\n' + body + '\n }\n}\n')
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=['form', 'candidate_lemmas', 'reason', 'source', 'quote'])
    w.writeheader()
    for r in sorted(bridge.review, key=lambda r: r['form']):
        w.writerow(r)
    write(out / 'needs_review.csv', buf.getvalue())
    stats = report(bridge, modern, kjv, out)
    print('bridge forms: %d   needs review: %d' % (len(bridge.main), len(bridge.review)))
    print('Psalms+Proverbs archaic forms: %(bridged)d bridged, %(review)d review, %(kept_out)d kept out, %(unbridged)d unbridged of %(total)d'
          ' (+%(modern_irregular)d modern irregulars, %(old_sense)d old-sense modern words)' % stats)
    if args.check:
        names = ['kjv_lemma_bridge.json', 'needs_review.csv', 'REPORT.md']
        diff = [n for n in names if not (OUT / n).exists() or not filecmp.cmp(out / n, OUT / n, shallow=False)]
        print('check: %s' % ('byte-identical' if not diff else 'DIFFERS: ' + ', '.join(diff)))
        sys.exit(1 if diff else 0)


if __name__ == '__main__':
    main()
