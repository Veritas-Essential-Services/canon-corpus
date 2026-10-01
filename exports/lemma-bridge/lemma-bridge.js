// prov: 2026-10-01 claude drafted (moved from Veritas-Essential-Services/vocabularium PR #2; model name withheld by session policy)
// fable_review: pending
/* Lemma bridge: expand a search query so modern words find their archaic forms.

   SQLite's full-text search (FTS5 with the porter stemmer) knows modern English
   endings only, so a search for "show" misses "shew", "sheweth" and "shewn", and
   "help" misses "holpen". This file turns one query into all of its forms, using
   the table built by canon-corpus pipeline/build_lemma_bridge.py
   (data/lemma_bridge/kjv_lemma_bridge.json). Python twin: pipeline/lemma_bridge.py;
   tests/lemma_bridge_test.py runs the same cases through both.

   Usage (browser: <script src="lemma-bridge.js">, then window.LemmaBridge):
     const bridge = await (await fetch('kjv_lemma_bridge.json')).json();
     const { match, words } = LemmaBridge.expandQuery('show mercy', bridge);
     db.prepare('SELECT * FROM verses WHERE verses MATCH ?').all(match);
     // match = ("show" OR "shew" OR "sheweth" OR ...) AND "mercy"

   Query syntax kept as FTS5 reads it: "quoted phrases", AND / OR / NOT, and
   prefix* searches pass through untouched; every other word is expanded.

   options.archaicOnly = true leaves out modern irregular forms the table also
   carries (went for go, arose for arise). Default false: a concordance should not
   silently miss "smote" when you search "smite". */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LemmaBridge = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const indexes = new WeakMap();

  // lemma -> [forms], built once per bridge object
  function familyIndex(bridge) {
    let idx = indexes.get(bridge);
    if (idx) return idx;
    idx = new Map();
    for (const [form, entry] of Object.entries(bridge.forms)) {
      for (const lemma of entry.lemmas) {
        if (!idx.has(lemma)) idx.set(lemma, []);
        idx.get(lemma).push(form);
      }
    }
    indexes.set(bridge, idx);
    return idx;
  }

  // "helped" -> "help", so a modern inflected query still reaches holpen. Only used
  // when the stripped word is a lemma the bridge knows.
  function modernBases(word) {
    const out = [];
    const rules = [['ies', 'y'], ['ied', 'y'], ['es', ''], ['s', ''], ['ed', ''], ['ed', 'e'],
                   ['d', ''], ['ing', ''], ['ing', 'e']];
    for (const [suf, rep] of rules) {
      if (word.endsWith(suf) && word.length > suf.length + 2) {
        const b = word.slice(0, -suf.length) + rep;
        out.push(b);
        if (b.length > 3 && b[b.length - 1] === b[b.length - 2]) out.push(b.slice(0, -1)); // stopped -> stop
      }
    }
    return out;
  }

  /* All forms of one word, the word itself first. */
  function expandWord(word, bridge, options) {
    const w = String(word).toLowerCase();
    const opts = options || {};
    const fam = familyIndex(bridge);
    const lemmas = new Set([w]);
    const own = bridge.forms[w];
    // a homograph (brake, a fern; bare, naked) keeps its modern meaning: searching
    // "bare" does not pull in every "bear", though searching "bear" finds "bare".
    if (own && !own.homograph) own.lemmas.forEach(l => lemmas.add(l));
    if (!own && !fam.has(w)) modernBases(w).forEach(b => { if (fam.has(b)) lemmas.add(b); });

    const forms = [w];
    const add = f => { if (!forms.includes(f)) forms.push(f); };
    for (const lemma of lemmas) {
      add(lemma);
      for (const f of fam.get(lemma) || []) {
        if (opts.archaicOnly && bridge.forms[f].archaic === false) continue;
        add(f);
      }
    }
    return forms;
  }

  /* Expand a whole query. Returns { match, words }:
       match - an FTS5 MATCH string, each word replaced by an OR group of its forms
       words - [{ word, forms }] for showing the user what was searched */
  function expandQuery(query, bridge, options) {
    if (!bridge || !bridge.forms) throw new Error('expandQuery needs the parsed kjv_lemma_bridge.json');
    const parts = [];
    const words = [];
    const isOp = t => /^(AND|OR|NOT)$/.test(t);
    // FTS5 will not read "(a OR b) c" as AND, so write the AND out -- but never next to
    // an operator or bracket the user typed.
    const push = t => {
      const prev = parts[parts.length - 1];
      if (prev !== undefined && !isOp(prev) && !isOp(t) && prev !== '(' && t !== ')') parts.push('AND');
      parts.push(t);
    };
    const tokens = String(query).match(/"[^"]*"|[()]|[^\s()]+/g) || [];
    for (const tok of tokens) {
      if (tok[0] === '"' || isOp(tok) || /\*$/.test(tok) || tok === '(' || tok === ')') {
        push(tok);                                        // FTS5 syntax: leave alone
        continue;
      }
      for (const word of tok.match(/[A-Za-z]+/g) || []) {  // same split as the FTS tokenizer
        const forms = expandWord(word, bridge, options);
        words.push({ word, forms });
        push(forms.length === 1 ? '"' + forms[0] + '"'
                                : '(' + forms.map(f => '"' + f + '"').join(' OR ') + ')');
      }
    }
    return { match: parts.join(' '), words };
  }

  return { expandQuery, expandWord };
});
