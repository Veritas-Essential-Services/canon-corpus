#!/usr/bin/env python3
"""Classify the maxim corpus on three axes: FORM, SCOPE, SUBJECT.

Axis 1 FORM   - the rhetorical shape of the sentence (how it is built)
Axis 2 SCOPE  - how boldly it generalises (how far it claims to reach)
Axis 3 SUBJECT- what it is about

FORM and SCOPE are structural and detected from syntax, so they are reliable.
SUBJECT is lexical and is a first pass only - it is labelled as such.
"""
import json, re, collections, csv, os

rows = [json.loads(l) for l in open('out/maxims.jsonl', encoding='utf-8')]

# ---------------------------------------------------------------- AXIS 1: FORM
FORM_ORDER = ['definition', 'antithesis', 'comparison', 'concession', 'conditional',
              'precept', 'question', 'enumeration', 'paradox', 'observation']

def form(t):
    s = t.strip()
    low = ' ' + s.lower() + ' '
    first = s.split()[0].lower() if s.split() else ''

    # question
    if s.rstrip().endswith('?'):
        return 'question'
    # definition: "X is/are Y" early, or dictionary-style "HEAD, n."
    if re.match(r'^[A-Z][A-Z\' \-]{2,30},\s+(n\.|v\.|adj\.|adv\.)', s):
        return 'definition'
    if re.match(r'^\s*(?:[A-Z][\w\'\- ]{0,28})\s+(?:is|are)\s+(?:the|a|an|nothing|not|but|only)\b', s):
        return 'definition'
    # concession
    if re.search(r'\b(though|although|albeit)\b', low) or re.search(r'\byet\b.*,', low):
        return 'concession'
    # conditional / relative-universal
    if re.match(r'^\s*(if|when|whoever|whosoever|he who|they who|the man who|who\b)', low.strip()):
        return 'conditional'
    if re.search(r'\bif\s+(?:you|thou|we|a|the|any|one|he|it)\b', low):
        return 'conditional'
    # precept / imperative
    if re.match(r'^(be|do|never|always|let|take|keep|give|seek|make|beware|remember|trust|speak|learn|know|fear|avoid|shun|leave)\b', first):
        return 'precept'
    if re.match(r'^(be not|do not|don\'t)\b', low.strip()):
        return 'precept'
    # comparison
    if re.search(r'\bas\b[^.]{2,60}\bso\b', low) or re.search(r'\b(is|are) like\b|\blike a\b|\bresembles?\b', low):
        return 'comparison'
    if re.search(r'\b(better|worse|more|less|rather)\b[^.]{2,60}\bthan\b', low):
        return 'comparison'
    # enumeration
    if re.search(r'\bthere are (two|three|four|five|six|seven)\b'
                 r'|\b(two|three|four|five) (kinds|sorts|classes|ways|types) of\b'
                 r'|\bfirst[,:].{2,80}\bsecond(ly)?\b', low):
        return 'enumeration'
    # antithesis (balanced opposition)
    if re.search(r'\bnot\b[^.]{2,60}\bbut\b', low):
        return 'antithesis'
    if re.search(r'\bwhile\b|\bwhereas\b', low):
        return 'antithesis'
    if s.count(';') >= 1 and re.search(r'\b(but|yet|however)\b', low):
        return 'antithesis'
    # paradox: explicit self-opposition
    if re.search(r'\bnothing\b[^.]{0,40}\bmore\b|\bonly\b[^.]{0,30}\bnever\b', low):
        return 'paradox'
    return 'observation'

# ---------------------------------------------------------------- AXIS 2: SCOPE
# How far does the sentence claim to reach? This is the axis Adam's seed line polices.
UNIVERSAL = re.compile(r'\b(all|every|none|no one|nobody|nothing|always|never|ever|any|invariably|without exception)\b', re.I)
HEDGE     = re.compile(r'\b(often|usually|generally|commonly|sometimes|frequently|for the most part|as a rule|apt to|tend|seldom|rarely|many|most|few|some|perhaps|almost)\b', re.I)
EXCEPT    = re.compile(r'\b(except|unless|save that|but for|save when|save in|exception)\b', re.I)

def scope(t):
    e, u, h = bool(EXCEPT.search(t)), bool(UNIVERSAL.search(t)), bool(HEDGE.search(t))
    if e and u:   return 'universal-with-exception'
    if e:         return 'exception-aware'
    if u and not h: return 'universal'
    if u and h:   return 'universal-hedged'
    if h:         return 'hedged'
    return 'unmarked'

# ---------------------------------------------------------------- AXIS 3: SUBJECT
SUBJECT = {
 'self-knowledge': r'\b(self|himself|herself|ourselves|myself|self-love|vanity|pride|conceit|know thyself|amour)\b',
 'virtue & vice':  r'\b(virtue|vice|honest|honour|honor|integrity|good(ness)?|wicked|sin|righteous|just(ice)?|merit)\b',
 'wisdom & folly': r'\b(wise|wisdom|fool|folly|prudence|prudent|sense|judgment|judgement|sagac)\b',
 'friendship':     r'\b(friend|friendship|companion|neighbour|neighbor|enem(y|ies))\b',
 'love & women':   r'\b(love|lover|women|woman|wife|husband|marriage|marry|beauty|passion of love)\b',
 'fortune & fate': r'\b(fortune|luck|chance|fate|destiny|providence|accident)\b',
 'death & time':   r'\b(death|die|dying|dead|mortal|old age|youth|time|hour|years|life is short)\b',
 'speech & silence': r'\b(speak|speech|silence|silent|tongue|word|talk|converse|eloquen)\b',
 'wealth & poverty': r'\b(rich|riches|wealth|money|poor|poverty|gold|avarice|miser|debt|gain)\b',
 'power & court':  r'\b(king|prince|court|courtier|power|rule|govern|state|minister|great men|master|servant)\b',
 'deception':      r'\b(deceiv|deceit|flatter|hypocris|dissembl|lie|lying|false|cheat|disguise|pretend)\b',
 'passion & anger': r'\b(anger|angry|passion|rage|revenge|envy|jealous|hatred|hate|fear|desire)\b',
 'reputation':     r'\b(praise|blame|reputation|fame|glory|esteem|contempt|opinion of others|censure)\b',
 'learning & art': r'\b(learn|study|book|read|science|art|poet|write|writer|style|knowledge|teacher)\b',
 'work & labour':  r'\b(work|labour|labor|trade|business|idle|industry|toil|craft)\b',
 'God & religion': r'\b(god|gods|divine|heaven|hell|soul|religio|pray|faith|christ|providence|eternal)\b',
 'nature':         r'\b(nature|natural|earth|sun|sea|tree|beast|animal|bird|season)\b',
 'happiness':      r'\b(happy|happiness|pleasure|joy|content|misery|miserab|suffer|griev|sorrow)\b',
}
SUBJECT_RX = {k: re.compile(v, re.I) for k, v in SUBJECT.items()}

def subjects(t):
    hits = [k for k, rx in SUBJECT_RX.items() if rx.search(t)]
    return hits or ['unclassified']

# ---------------------------------------------------------------- run
for r in rows:
    r['form'] = form(r['text'])
    r['scope'] = scope(r['text'])
    r['subjects'] = subjects(r['text'])
    r['chars'] = len(r['text'])

os.makedirs('out', exist_ok=True)
with open('out/maxims_classified.jsonl', 'w', encoding='utf-8') as f:
    for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')

FIELDS = ['work','ref','author','author_dates','composed','translator','translation_year',
          'source','pd_basis','form','scope','subjects','chars','text','note']
with open('out/maxims.csv','w',encoding='utf-8',newline='') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore')
    w.writeheader()
    for r in rows:
        r2 = dict(r); r2['subjects'] = '|'.join(r['subjects'])
        w.writerow(r2)

# ---------------------------------------------------------------- report
def pct(n, d): return f'{100*n/d:5.1f}%' if d else '  -  '

print(f'CORPUS: {len(rows)} units, {len(set(r["work"] for r in rows))} works\n')

print('AXIS 1 - FORM')
fc = collections.Counter(r['form'] for r in rows)
for k in FORM_ORDER:
    print(f'  {k:14s} {fc[k]:6d}  {pct(fc[k], len(rows))}')

print('\nAXIS 2 - SCOPE (how far the claim reaches)')
sc = collections.Counter(r['scope'] for r in rows)
for k, v in sc.most_common():
    print(f'  {k:26s} {v:6d}  {pct(v, len(rows))}')

print('\nAXIS 3 - SUBJECT (lexical first pass; units may carry several)')
bc = collections.Counter(s for r in rows for s in r['subjects'])
for k, v in bc.most_common():
    print(f'  {k:18s} {v:6d}')

print('\nFORM PROFILE BY WORK (row % across forms)')
works = sorted(set(r['work'] for r in rows))
hdr = ''.join(f'{k[:6]:>7s}' for k in FORM_ORDER)
print(f'{"work":44s}{"n":>6s}{hdr}')
for w in works:
    sub = [r for r in rows if r['work'] == w]
    c = collections.Counter(r['form'] for r in sub)
    line = ''.join(f'{100*c[k]/len(sub):6.0f}%' for k in FORM_ORDER)
    print(f'{w[:44]:44s}{len(sub):6d}{line}')

print('\nSCOPE PROFILE BY WORK (% universal / % hedged / % exception-aware)')
print(f'{"work":44s}{"n":>6s}{"univ":>8s}{"hedge":>8s}{"exc":>8s}')
for w in works:
    sub = [r for r in rows if r['work'] == w]
    u = sum(1 for r in sub if r['scope'].startswith('universal'))
    h = sum(1 for r in sub if 'hedged' in r['scope'] or r['scope'] == 'hedged')
    e = sum(1 for r in sub if 'exception' in r['scope'])
    print(f'{w[:44]:44s}{len(sub):6d}{100*u/len(sub):7.0f}%{100*h/len(sub):7.0f}%{100*e/len(sub):7.0f}%')
