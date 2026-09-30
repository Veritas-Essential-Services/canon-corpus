---
model_log:
  - 2026-09-26 claude-opus-5-5 drafted (from git trailer; backfilled 2026-09-30)
fable_review: pending
---
# Clause cuts: Lauda Sion, Sacris solemniis, Verbum supernum (2026-09-26)

**For:** Adam. **From:** `pipeline/build_hymn_corpus.py`, which cut the three
Corpus Christi hymns added from Britt 1922 (launch plan Ring 3, "the hymns of
Thomas"). **Rule:** `pipeline/README-hymn-jsonl.md` s.1, the one *Adoro te* was
re-cut by: a row is a clause, a finite verb and every word it governs; lines
are joined when a word on one line depends on a finite verb on another; a
clause with its own finite verb *may* stand; a vocative or a complete verbless
exclamation stands alone.

Every cut carries its grammatical reason, a one-line clause included, so every
stanza is a row here: 25 stanzas, 74 clauses. Until you answer, each cut is
`review: open` in `data/hymns/passages.jsonl`.

**Where the rule left a choice** (worth a look first):

- **Lauda st10 c2** (*Quantum toto tegitur*): a correlative clause with its own
  verb, so it may stand; joining it to ll.1-3 keeps *Tantum ... Quantum*
  together (`cut: 1-4, 5, 6, 7-8; note: …`).
- **Lauda st5 c1, st6 c3; Verbum st5 c2**: relative clauses with their own verb,
  left standing, as *Adoro te* st1 l.2 was.
- **Lauda st7 c2** (*Caro cibus, sanguis potus*) and **st11 c1-c2**: verbless
  statements and an *Ecce* exclamation, treated as the rule's verbless case.
- **Verbum st4**: ll.2-3 read as taking *dedit* (l.1), gapped, as Britt's note
  reads them; the other reading hangs l.3 on *dat* (l.4).
- **Lauda st12 c5**: five lines, because *Tu* (l.6) is the subject of *Fac*
  (l.10).

**How to answer.** In the *Adam* column write `ok` to accept the stanza's cut,
`draft→` to leave it for later, or a new cut as the clauses' line spans in
order: `cut: 1, 2-3, 4-6`, with `; note: …` giving the grammatical reason for
any join the draft did not have (the reason is required). Then
`python pipeline/review.py apply docs/review/2026-09-26-thomas-cuts.md` writes
one row per answered stanza to `data/hymn-sources/cut-reviewed.jsonl`, rebuilds
the hymns and runs `build_hymn_corpus.py --check`. Anything it would have to
guess at stops the run before anything is written, naming the row.

**What a re-cut does to identity.** A clause's uid stays with its citation
(`hymns:lauda-sion.st10.c2`). If a re-cut puts different lines under a
citation, the build gives that citation a fresh uid and records the old one as
superseded by it (`wh_uid`: never reused, never silently repointed); the
clause says so in `cut.supersedes`. So **answer this sheet before the lemma
sheet**: a lemma answer is keyed by the clause uid, and a lemma answer on a
re-issued clause stops the build (it is not dropped). A second re-cut of the
same stanza is refused; that one is a hand decision.

| # | Hymn · stanza | The cut: clause, lines, Latin | Why | Adam: |
|---|---|---|---|---|
| 1 | Lauda Sion 1 `wh-GMJZG6WWDG` | c1 l.1: *Lauda Sion Salvatorem,*<br>c2 ll.2-3: *Lauda ducem et pastorem, / In hymnis et canticis.*<br>c3 l.4: *Quantum potes, tantum aude:*<br>c4 ll.5-6: *Quia major omni laude, / Nec laudare sufficis.* | c1: own finite verb (Lauda, imperative); Sion is its vocative<br>c2: lines joined: l.3 has no verb: In hymnis et canticis goes with Lauda (l.2)<br>c3: own finite verbs (potes, aude): the quantum ... tantum pair inside one line<br>c4: lines joined: l.5 has no finite verb (est understood after Quia); Nec (l.6) coordinates sufficis under the same Quia | |
| 2 | Lauda Sion 2 `wh-AJ3NG93YDV` | c1 ll.1-3: *Laudis thema specialis, / Panis vivus et vitalis / Hodie proponitur.*<br>c2 ll.4-6: *Quem in sacræ mensa cœnæ / Turbæ fratrum duodenæ / Datum non ambigitur.* | c1: lines joined: thema (l.1) and Panis (l.2) are the subjects of proponitur (l.3)<br>c2: lines joined: the relative Quem (l.4) is the subject of datum [esse] (l.6), which ambigitur governs; Turbae ... duodenae (l.5) is its dative | |
| 3 | Lauda Sion 3 `wh-C2P08QV763` | c1 l.1: *Sit laus plena, sit sonora,*<br>c2 ll.2-3: *Sit jucunda, sit decora, / Mentis jubilatio.*<br>c3 l.4: *Dies enim solemnis agitur,*<br>c4 ll.5-6: *In qua mensæ prima recolitur / Hujus institutio.* | c1: own finite verbs (Sit ... sit); laus is their subject<br>c2: lines joined: jubilatio (l.3) is the subject of Sit ... sit (l.2)<br>c3: own finite verb (agitur)<br>c4: lines joined: institutio (l.6) is the subject of recolitur (l.5) | |
| 4 | Lauda Sion 4 `wh-F1631V64PG` | c1 ll.1-3: *In hac mensa novi Regis, / Novum Pascha novæ legis, / Phase vetus terminat.*<br>c2 ll.4-5: *Vetustatem novitas, / Umbram fugat veritas,*<br>c3 l.6: *Noctem lux eliminat.* | c1: lines joined: Pascha (l.2) is the subject of terminat (l.3); In hac mensa (l.1) goes with it<br>c2: lines joined: l.4 has no verb: Vetustatem and novitas take fugat (l.5), gapped<br>c3: own finite verb (eliminat) | |
| 5 | Lauda Sion 5 `wh-M8RQX2DTQ3` | c1 l.1: *Quod in cœna Christus gessit,*<br>c2 ll.2-3: *Faciendum hoc expressit / In sui memoriam.*<br>c3 ll.4-6: *Docti sacris institutis, / Panem, vinum in salutis / Consecramus hostiam.* | c1: a relative clause with its own finite verb (gessit); may stand (rule s.1)<br>c2: lines joined: In sui memoriam (l.3) goes with Faciendum ... expressit (l.2)<br>c3: lines joined: Docti (l.4) agrees with the subject of Consecramus (l.6); Panem, vinum (l.5) are its objects | |
| 6 | Lauda Sion 6 `wh-1AF6G9NNRG` | c1 l.1: *Dogma datur Christianis,*<br>c2 ll.2-3: *Quod in carnem transit panis, / Et vinum in sanguinem.*<br>c3 l.4: *Quod non capis, quod non vides,*<br>c4 ll.5-6: *Animosa firmat fides, / Præter rerum ordinem.* | c1: own finite verb (datur)<br>c2: lines joined: vinum (l.3) is a second subject of transit (l.2), gapped<br>c3: two relative clauses with their own finite verbs (capis, vides); may stand<br>c4: lines joined: Praeter rerum ordinem (l.6) goes with firmat (l.5) | |
| 7 | Lauda Sion 7 `wh-TP8407ARHW` | c1 ll.1-3: *Sub diversis speciebus, / Signis tantum, et non rebus, / Latent res eximiæ.*<br>c2 l.4: *Caro cibus, sanguis potus:*<br>c3 ll.5-6: *Manet tamen Christus totus, / Sub utraque specie.* | c1: lines joined: ll.1-2 have no verb: Sub diversis speciebus and Signis ... rebus go with Latent (l.3)<br>c2: a complete verbless statement (est understood twice); governs nothing and depends on nothing, so it stands, as the rule's verbless case<br>c3: lines joined: Sub utraque specie (l.6) goes with Manet (l.5) | |
| 8 | Lauda Sion 8 `wh-J5CJH3EADM` | c1 ll.1-3: *A sumente non concisus, / Non confractus, non divisus: / Integer accipitur.*<br>c2 ll.4-5: *Sumit unus, sumunt mille: / Quantum isti, tantum ille:*<br>c3 l.6: *Nec sumptus consumitur.* | c1: lines joined: the participles concisus, confractus, divisus (ll.1-2) agree with the subject of accipitur (l.3)<br>c2: lines joined: l.5 has no verb: isti and ille are subjects of sumunt, sumit (l.4), gapped<br>c3: own finite verb (consumitur) | |
| 9 | Lauda Sion 9 `wh-XHYMK03GVM` | c1 ll.1-3: *Sumunt boni, sumunt mali: / Sorte tamen inæquali, / Vitæ, vel interitus.*<br>c2 l.4: *Mors est malis, vita bonis:*<br>c3 ll.5-6: *Vide paris sumptionis, / Quam sit dispar exitus.* | c1: lines joined: ll.2-3 have no verb: the ablative Sorte (l.2) and its genitives Vitae, interitus (l.3) go with sumunt (l.1)<br>c2: own finite verb (est), gapped in its second half inside the line<br>c3: lines joined: Vide (l.5) governs the indirect question Quam sit (l.6), and paris sumptionis (l.5) depends on exitus (l.6) | |
| 10 | Lauda Sion 10 `wh-FJC5NNAF1W` | c1 ll.1-3: *Fracto demum Sacramento / Ne vacilles, sed memento, / Tantum esse sub fragmento,*<br>c2 l.4: *Quantum toto tegitur.*<br>c3 l.5: *Nulla rei fit scissura:*<br>c4 l.6: *Signi tantum fit fractura:*<br>c5 ll.7-8: *Qua nec status, nec statura / Signati minuitur.* | c1: lines joined: the ablative absolute (l.1) goes with vacilles, memento (l.2), and memento governs Tantum esse (l.3)<br>c2: a correlative clause with its own finite verb (tegitur); may stand. Joining it to ll.1-3 would keep Tantum ... Quantum together: Adam's call<br>c3: own finite verb (fit)<br>c4: own finite verb (fit)<br>c5: lines joined: status, statura (l.7) are the subjects of minuitur (l.8) | |
| 11 | Lauda Sion 11 `wh-E6K8A6VHQA` | c1 ll.1-2: *Ecce panis angelorum, / Factus cibus viatorum:*<br>c2 ll.3-4: *Vere panis filiorum, / Non mittendus canibus.*<br>c3 l.5: *In figuris præsignatur,*<br>c4 l.6: *Cum Isaac immolatur:*<br>c5 l.7: *Agnus Paschæ deputatur:*<br>c6 l.8: *Datur manna patribus.* | c1: lines joined: no finite verb: Ecce with the nominative panis (l.1), and Factus (l.2) agrees with it; a complete verbless exclamation<br>c2: lines joined: no finite verb (est understood): the gerundive mittendus (l.4) agrees with panis (l.3)<br>c3: own finite verb (praesignatur)<br>c4: a cum-clause with its own finite verb (immolatur); may stand<br>c5: own finite verb (deputatur)<br>c6: own finite verb (Datur) | |
| 12 | Lauda Sion 12 `wh-5HNX27DQTW` | c1 l.1: *Bone Pastor, panis vere,*<br>c2 l.2: *Jesu, nostri miserere:*<br>c3 l.3: *Tu nos pasce, nos tuere:*<br>c4 ll.4-5: *Tu nos bona fac videre / In terra viventium.*<br>c5 ll.6-10: *Tu qui cuncta scis et vales: / Qui nos pascis hic mortales: / Tuos ibi commensales, / Cohæredes et sodales / Fac sanctorum civium.* | c1: vocatives only (Bone Pastor, panis vere): governed by nothing, a row of their own<br>c2: own finite verb (miserere); Jesu is its vocative<br>c3: own finite verbs (pasce, tuere)<br>c4: lines joined: In terra viventium (l.5) goes with videre, which fac (l.4) governs<br>c5: lines joined: Tu (l.6) is the subject of Fac (l.10), and Tuos ... commensales, Cohaeredes et sodales (ll.8-9) its object and predicate; the two relative clauses (ll.6-7) sit inside | |
| 13 | Sacris solemniis 1 `wh-TFYA8R8AAP` | c1 l.1: *Sacris solemniis juncta sint gaudia,*<br>c2 l.2: *Et ex præcordiis sonent præconia;*<br>c3 ll.3-4: *Recedant vetera, nova sint omnia, / Corda, voces, et opera.* | c1: own finite verb (sint)<br>c2: own finite verb (sonent), coordinate by Et<br>c3: lines joined: l.4 has no verb: Corda, voces, et opera stand in apposition to omnia (l.3) | |
| 14 | Sacris solemniis 2 `wh-1H2BWPZRTD` | c1 l.1: *Noctis recolitur cœna novissima,*<br>c2 ll.2-4: *Qua Christus creditur agnum et azyma / Dedisse fratribus, juxta legitima / Priscis indulta patribus.* | c1: own finite verb (recolitur)<br>c2: lines joined: creditur (l.2) governs Dedisse (l.3), and indulta (l.4) agrees with legitima (l.3) | |
| 15 | Sacris solemniis 3 `wh-5JPV5ANYST` | c1 ll.1-4: *Post agnum typicum, expletis epulis, / Corpus Dominicum datum discipulis, / Sic totum omnibus, quod totum singulis, / Ejus fatemur manibus.* | c1: lines joined: one period, one finite verb (fatemur, l.4): Corpus ... datum [esse] (l.2) is its accusative and infinitive, and ll.1 and 3 go with it | |
| 16 | Sacris solemniis 4 `wh-Q9J4ATA0S4` | c1 l.1: *Dedit fragilibus corporis ferculum,*<br>c2 ll.2-3: *Dedit et tristibus sanguinis poculum, / Dicens: accipite quod trado vasculum,*<br>c3 l.4: *Omnes ex eo bibite.* | c1: own finite verb (Dedit)<br>c2: lines joined: the participle Dicens (l.3) agrees with the subject of Dedit (l.2); the words it introduces share its line<br>c3: own finite verb (bibite), the second half of the quoted words | |
| 17 | Sacris solemniis 5 `wh-SDH6VHMRJ7` | c1 l.1: *Sic sacrificium istud instituit,*<br>c2 ll.2-4: *Cujus officium committi voluit / Solis presbyteris, quibus sic congruit, / Ut sumant, et dent ceteris.* | c1: own finite verb (instituit)<br>c2: lines joined: voluit (l.2) governs committi, whose dative Solis presbyteris is on l.3; the Ut-clause (l.4) is the subject of congruit (l.3) | |
| 18 | Sacris solemniis 6 `wh-T4SVQ1ZH24` | c1 l.1: *Panis angelicus fit panis hominum;*<br>c2 l.2: *Dat panis cœlicus figuris terminum:*<br>c3 ll.3-4: *O res mirabilis, manducat Dominum / Pauper, servus, et humilis.* | c1: own finite verb (fit)<br>c2: own finite verb (Dat)<br>c3: lines joined: Pauper, servus, et humilis (l.4) are the subjects of manducat (l.3) | |
| 19 | Sacris solemniis 7 `wh-E490CB9G1B` | c1 l.1: *Te trina Deitas unaque poscimus,*<br>c2 l.2: *Sic nos tu visita, sicut te colimus:*<br>c3 ll.3-4: *Per tuas semitas duc nos quo tendimus, / Ad lucem, quam inhabitas.* | c1: own finite verb (poscimus); Deitas is its vocative<br>c2: own finite verbs (visita, colimus)<br>c3: lines joined: Ad lucem (l.4) goes with duc (l.3) | |
| 20 | Verbum supernum 1 `wh-RYXY2VHNX1` | c1 ll.1-4: *Verbum supernum prodiens, / Nec Patris linquens dexteram, / Ad opus suum exiens, / Venit ad vitæ vesperam.* | c1: lines joined: the participles prodiens, linquens, exiens (ll.1-3) agree with Verbum, the subject of Venit (l.4) | |
| 21 | Verbum supernum 2 `wh-CSHJVVR7CK` | c1 ll.1-4: *In mortem a discipulo / Suis tradendus æmulis, / Prius in vitæ ferculo / Se tradidit discipulis.* | c1: lines joined: tradendus (l.2) agrees with the subject of tradidit (l.4); ll.1 and 3 go with it | |
| 22 | Verbum supernum 3 `wh-ZYHF01ZZA6` | c1 ll.1-2: *Quibus sub bina specie / Carnem dedit et sanguinem;*<br>c2 ll.3-4: *Ut duplicis substantiæ / Totum cibaret hominem.* | c1: lines joined: the dative Quibus (l.1) goes with dedit (l.2)<br>c2: lines joined: duplicis substantiae (l.3) depends on hominem, in the Ut-clause whose verb is cibaret (l.4) | |
| 23 | Verbum supernum 4 `wh-NWSS2CW9FT` | c1 ll.1-3: *Se nascens dedit socium, / Convescens in edulium, / Se moriens in pretium,*<br>c2 l.4: *Se regnans dat in præmium.* | c1: lines joined: Convescens (l.2) and Se moriens (l.3) take dedit (l.1), gapped, as Britt's note reads them; their participles agree with its subject<br>c2: own finite verb (dat) | |
| 24 | Verbum supernum 5 `wh-NWKAQ1VB3D` | c1 l.1: *O salutaris hostia,*<br>c2 l.2: *Quæ cœli pandis ostium,*<br>c3 l.3: *Bella premunt hostilia,*<br>c4 l.4: *Da robur, fer auxilium.* | c1: a vocative (O salutaris hostia): governed by nothing, a row of its own<br>c2: a relative clause with its own finite verb (pandis); may stand<br>c3: own finite verb (premunt)<br>c4: own finite verbs (Da, fer) | |
| 25 | Verbum supernum 6 `wh-15HWGFTENR` | c1 ll.1-2: *Uni trinoque Domino, / Sit sempiterna gloria:*<br>c2 ll.3-4: *Qui vitam sine termino / Nobis donet in patria.* | c1: lines joined: the dative Uni trinoque Domino (l.1) goes with Sit (l.2)<br>c2: lines joined: vitam (l.3) is the object of donet (l.4) | |

Row numbers are for talking about the sheet only; each answer is keyed by the
stanza's uid.

## What an answer looks like in the file

```
{"stanza": "hymns:lauda-sion.st1", "cut": [[1, 1], [2, 3], [4, 4], [5, 6]], "reviewed_on": "2026-09-27"}
{"stanza": "hymns:lauda-sion.st10", "cut": [[1, 4], [5, 5], [6, 6], [7, 8]], "reviewed_on": "2026-09-27",
 "note": "Quantum (l.4) answers Tantum (l.3): keep the correlative in one row"}
```
