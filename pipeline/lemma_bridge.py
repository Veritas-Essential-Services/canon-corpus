# prov: 2026-10-01 claude drafted (moved from Veritas-Essential-Services/vocabularium PR #2; model name withheld by session policy)
# fable_review: pending
"""Lemma bridge, search side: expand a query so modern words find archaic forms.

SQLite FTS5 with the porter stemmer knows modern English only: "show" misses
"shew", "sheweth" and "shewn"; "help" misses "holpen". expand_query() rewrites a
query with every form of each word, from data/lemma_bridge/kjv_lemma_bridge.json
(built by pipeline/build_lemma_bridge.py). Line-for-line twin of
exports/lemma-bridge/lemma-bridge.js; tests/lemma_bridge_test.py runs the same
cases through both, so they cannot drift apart unnoticed.

    from lemma_bridge import load_bridge, expand_query
    bridge = load_bridge()
    match, words = expand_query('show mercy', bridge)
    db.execute('SELECT * FROM verses WHERE verses MATCH ?', (match,))
    # match == '("show" OR "shew" OR "sheweth" OR ...) AND "mercy"'

Quoted phrases, AND / OR / NOT, brackets and prefix* searches pass through
untouched; every other word is expanded. archaic_only=True leaves out the modern
irregular forms the table also carries (went for go); the default keeps them, so
"smite" finds "smote".
"""
import json, re
from pathlib import Path

TABLE = Path(__file__).resolve().parent.parent / 'data' / 'lemma_bridge' / 'kjv_lemma_bridge.json'

_MODERN = [('ies', 'y'), ('ied', 'y'), ('es', ''), ('s', ''), ('ed', ''), ('ed', 'e'),
           ('d', ''), ('ing', ''), ('ing', 'e')]


def load_bridge(path=TABLE):
    """The parsed table, with a lemma -> [forms] index added under '_families'."""
    bridge = json.loads(Path(path).read_text(encoding='utf-8'))
    fam = {}
    for form, entry in bridge['forms'].items():
        for lemma in entry['lemmas']:
            fam.setdefault(lemma, []).append(form)
    bridge['_families'] = fam
    return bridge


def _modern_bases(word):
    """"helped" -> "help", so a modern inflected query still reaches holpen."""
    out = []
    for suf, rep in _MODERN:
        if word.endswith(suf) and len(word) > len(suf) + 2:
            b = word[:-len(suf)] + rep
            out.append(b)
            if len(b) > 3 and b[-1] == b[-2]:
                out.append(b[:-1])                    # stopped -> stop
    return out


def expand_word(word, bridge, archaic_only=False):
    """All forms of one word, the word itself first."""
    w = word.lower()
    fam = bridge['_families']
    lemmas = [w]
    own = bridge['forms'].get(w)
    # a homograph (brake, a fern; bare, naked) keeps its modern meaning: searching
    # "bare" does not pull in every "bear", though searching "bear" finds "bare".
    if own and not own['homograph']:
        lemmas += [l for l in own['lemmas'] if l not in lemmas]
    if not own and w not in fam:
        lemmas += [b for b in _modern_bases(w) if b in fam and b not in lemmas]
    forms = [w]
    for lemma in lemmas:
        for f in [lemma] + fam.get(lemma, []):
            if f in forms or (f != lemma and archaic_only and bridge['forms'][f]['archaic'] is False):
                continue
            forms.append(f)
    return forms


def expand_query(query, bridge, archaic_only=False):
    """Returns (match, words): an FTS5 MATCH string, and [(word, forms)] to show the user."""
    parts, words = [], []
    is_op = lambda t: t in ('AND', 'OR', 'NOT')

    def push(t):
        # FTS5 will not read "(a OR b) c" as AND, so write the AND out -- but never
        # next to an operator or bracket the user typed.
        if parts and not is_op(parts[-1]) and not is_op(t) and parts[-1] != '(' and t != ')':
            parts.append('AND')
        parts.append(t)

    for tok in re.findall(r'"[^"]*"|[()]|[^\s()]+', query):
        if tok[0] == '"' or is_op(tok) or tok.endswith('*') or tok in '()':
            push(tok)                                 # FTS5 syntax: leave alone
            continue
        for word in re.findall(r'[A-Za-z]+', tok):    # same split as the FTS tokenizer
            forms = expand_word(word, bridge, archaic_only)
            words.append((word, forms))
            push('"%s"' % forms[0] if len(forms) == 1 else
                 '(' + ' OR '.join('"%s"' % f for f in forms) + ')')
    return ' '.join(parts), words
