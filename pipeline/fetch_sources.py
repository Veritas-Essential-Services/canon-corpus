#!/usr/bin/env python3
# prov: 2026-07-22 claude-fable-5 drafted (from git trailer; backfilled 2026-09-30)
# prov: 2026-09-06 claude-opus-5 edited (from git trailer; backfilled 2026-09-30)
# prov: 2026-09-07 claude-opus-5 edited (from git trailer; backfilled 2026-09-30)
# fable_review: pending
"""fetch_sources.py — manifest-driven fetcher for the structured shelves.

Three libraries (canon-corpus owns ALL fetching since the 2026-07-22
extraction from patrimonium — patrimonium's mine_names.py keeps its own
copy of the miner corpus, but the structure layer fetches here):

  PERSEUS   — TEI XML with canonical citations born-in (CTS URNs).
              Source: PerseusDL/canonical-greekLit + canonical-latinLit on GitHub.
  CCEL      — ThML XML with scripture references pre-tagged (scripRef).
              Source: ccel.org; URL pattern /ccel/<initial>/<author>/<work>.xml
  GUTENBERG — plain .txt by ebook id (KJV, Shakespeare, the verse/prose shelf).

These manifests ARE the collection: commit history is the acquisitions
ledger. Downloads land in data/corpus/ (gitignored, refetchable).
Resumable: existing files are skipped.

Run:  python3 pipeline/fetch_sources.py            # fetch everything missing
      python3 pipeline/fetch_sources.py --list     # show the manifests
"""
import os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "..", "data", "corpus")

RAW = "https://raw.githubusercontent.com/PerseusDL/{repo}/master/data/{path}"

# First1KGreek (Open Greek and Latin, Leipzig/Tufts/Harvard): the GREEK
# text of the church fathers, each the TEI of a printed critical edition.
# Rights, read per file 2026-10-02: every file's licence line is CC BY-SA 4.0
# (the markup); the edition itself must be published before 1931 (US public
# domain). The ancient text has no author's right, and an editor's right in
# a critical edition, where a country grants one at all (Germany: 25 years
# from publication, s.70 UrhG), is long expired. Taken only where the
# sourceDesc date is before 1931.
F1K_RAW = "https://raw.githubusercontent.com/OpenGreekAndLatin/First1KGreek/master/data/{path}"

# slug -> (path, note)
FIRST1K = {
    # Wave 1, 2026-10-02: Clement, Justin, the apologists, Origen,
    # Hippolytus, Methodius. NOT taken, and why:
    #   - the Apostolic Fathers and Diognetus (another thread's work);
    #   - Irenaeus, Adv. haer. (Harvey 1857): the file numbers its chapters
    #     in one series off by one from Harvey's printed Κεφ., runs Book II
    #     fragments on as chapters 38-46, and keeps marginal source
    #     references (Massuet, Theodoret) inside the Greek -- no citation it
    #     yields could be trusted;
    #   - Origen, Homilies on Luke (Rauer 1930): mostly Jerome's LATIN
    #     version (32k of 52k words), not a Greek text;
    #   - Origen, Comm. in Matt. books 10-17 (Klostermann 1935-37): after 1930;
    #   - Origen, Comm. in Jo. books 19/20/28/32 as tlg079: the same Preuschen
    #     text the whole commentary (tlg005) already carries;
    #   - Methodius, De libero arbitrio (Bonwetsch 1917): a third of it is
    #     Bonwetsch's German rendering of the Slavonic, interleaved.
    "clement-protrepticus-grc": ("tlg0555/tlg001/tlg0555.tlg001.1st1K-grc1.xml",
        "Clement of Alexandria, Protrepticus -- Greek, ed. Otto Stählin (GCS, Leipzig: Hinrichs, 1905)"),
    "clement-paedagogus-grc": ("tlg0555/tlg002/tlg0555.tlg002.1st1K-grc1.xml",
        "Clement of Alexandria, Paedagogus -- Greek, ed. Stählin (Hinrichs, 1905)"),
    "clement-eclogae-propheticae-grc": ("tlg0555/tlg005/tlg0555.tlg005.1st1K-grc1.xml",
        "Clement of Alexandria, Eclogae propheticae -- Greek, ed. Stählin (Hinrichs, 1909)"),
    "clement-quis-dives-grc": ("tlg0555/tlg006/tlg0555.tlg006.1st1K-grc1.xml",
        "Clement of Alexandria, Quis dives salvetur -- Greek, ed. Stählin (Hinrichs, 1909)"),
    "clement-excerpta-theodoto-grc": ("tlg0555/tlg007/tlg0555.tlg007.1st1K-grc1.xml",
        "Clement of Alexandria, Excerpta ex Theodoto -- Greek, ed. Stählin (Hinrichs, 1909)"),
    "justin-apology-1-grc": ("tlg0645/tlg001/tlg0645.tlg001.1st1K-grc1.xml",
        "Justin Martyr, First Apology -- Greek, ed. Gerhard Rauschen (Bonn: Hanstein, 1911)"),
    "justin-apology-2-grc": ("tlg0645/tlg002/tlg0645.tlg002.perseus-grc2.xml",
        "Justin Martyr, Second Apology -- Greek, ed. Rauschen (Hanstein, 1911)"),
    "justin-dialogue-trypho-grc": ("tlg0645/tlg003/tlg0645.tlg003.perseus-grc2.xml",
        "Justin Martyr, Dialogue with Trypho -- Greek, ed. Georges Archambault (Paris: Picard, 1909); "
        "his French translation is NOT in this file"),
    "tatian-oratio-grc": ("tlg1766/tlg001/tlg1766.tlg001.perseus-grc1.xml",
        "Tatian, Oratio ad Graecos -- Greek, ed. J. C. T. Otto (Jena: Mauke, 1851)"),
    "athenagoras-legatio-grc": ("tlg1205/tlg001/tlg1205.tlg001.perseus-grc1.xml",
        "Athenagoras, Legatio -- Greek, ed. J. C. T. von Otto (Mauke, 1857)"),
    "athenagoras-de-resurrectione-grc": ("tlg1205/tlg002/tlg1205.tlg002.perseus-grc1.xml",
        "Athenagoras, De resurrectione -- Greek, ed. von Otto (Mauke, 1857)"),
    "theophilus-ad-autolycum-grc": ("tlg1725/tlg001/tlg1725.tlg001.perseus-grc1.xml",
        "Theophilus of Antioch, Ad Autolycum -- Greek, ed. W. G. Humphry (Cambridge: Parker, 1852)"),
    "origen-contra-celsum-grc": ("tlg2042/tlg001/tlg2042.tlg001.perseus-grc1.xml",
        "Origen, Contra Celsum -- Greek, ed. Paul Koetschau (GCS, Hinrichs, 1899)"),
    "origen-commentary-john-grc": ("tlg2042/tlg005/tlg2042.tlg005.1st1K-grc1.xml",
        "Origen, Commentary on John -- Greek, ed. Erwin Preuschen (GCS, Hinrichs, 1903)"),
    "origen-exhortatio-martyrium-grc": ("tlg2042/tlg007/tlg2042.tlg007.perseus-grc1.xml",
        "Origen, Exhortation to Martyrdom -- Greek, ed. Koetschau (Hinrichs, 1899)"),
    "origen-de-oratione-grc": ("tlg2042/tlg008/tlg2042.tlg008.perseus-grc1.xml",
        "Origen, On Prayer -- Greek, ed. Koetschau (Hinrichs, 1899)"),
    "origen-homilies-jeremiah-1-11-grc": ("tlg2042/tlg009/tlg2042.tlg009.opp-grc1.xml",
        "Origen, Homilies on Jeremiah 1-11 -- Greek, ed. Erich Klostermann (GCS, Hinrichs, 1901)"),
    "origen-homilies-jeremiah-12-20-grc": ("tlg2042/tlg021/tlg2042.tlg021.opp-grc1.xml",
        "Origen, Homilies on Jeremiah 12-20 -- Greek, ed. Klostermann (Hinrichs, 1901)"),
    "origen-de-engastrimytho-grc": ("tlg2042/tlg013/tlg2042.tlg013.opp-grc1.xml",
        "Origen, On the Witch of Endor (Homily on 1 Sam 28) -- Greek, ed. Klostermann (Hinrichs, 1901)"),
    "origen-philocalia-grc": ("tlg2042/tlg019/tlg2042.tlg019.1st1K-grc1.xml",
        "Origen, Philocalia (compiled by Basil and Gregory Nazianzen) -- Greek, ed. J. Armitage "
        "Robinson (Cambridge UP, 1893); parts of the OCR are badly damaged, flagged per unit"),
    "origen-epistula-africanum-grc": ("tlg2042/tlg045/tlg2042.tlg045.1st1K-grc1.xml",
        "Origen, Letter to Africanus -- Greek, ed. de La Rue, repr. Migne PG 11 (1857)"),
    "hippolytus-refutatio-grc": ("tlg2115/tlg060/tlg2115.tlg060.opp-grc1.xml",
        "Hippolytus, Refutation of All Heresies -- Greek, ed. Paul Wendland (GCS, Hinrichs, 1916)"),
    "methodius-symposium-grc": ("tlg2959/tlg001/tlg2959.tlg001.opp-grc1.xml",
        "Methodius of Olympus, Symposium -- Greek, ed. G. Nathanael Bonwetsch (GCS, Hinrichs, 1917)"),
    # Wave 2, 2026-10-02: Eusebius, Athanasius, Gregory Nazianzen,
    # Epiphanius, Cyril of Alexandria, Marcellus. NOT taken, and why:
    #   - Eusebius, Church History grc1 and eng1: the Loeb (Lake 1926,
    #     Oulton 1932), after 1930 in part; Dindorf's Teubner (grc2) taken;
    #   - Eusebius, Onomasticon (Klostermann 1904): Jerome's Latin version
    #     interleaved, and its sources numbered "?";
    #   - Eusebius, Eclogae propheticae (Gaisford 1842): the scripture
    #     references of the margin are welded onto the Greek words
    #     ("σουGen."), all through;
    #   - Epiphanius, Panarion (Holl 1915-33): its third volume is 1933;
    #   - Basil, Gregory of Nyssa, Chrysostom: not in First1KGreek.
    "eusebius-praeparatio-evangelica-grc": ("tlg2018/tlg001/tlg2018.tlg001.1st1K-grc1.xml",
        "Eusebius, Praeparatio evangelica -- Greek, ed. Wilhelm Dindorf (Leipzig: Teubner, 1867)"),
    "eusebius-historia-ecclesiastica-grc": ("tlg2018/tlg002/tlg2018.tlg002.1st1K-grc2.xml",
        "Eusebius, Church History -- Greek, ed. Dindorf (Teubner, 1871)"),
    "eusebius-martyrs-palestine-grc": ("tlg2018/tlg003/tlg2018.tlg003.1st1K-grc1.xml",
        "Eusebius, Martyrs of Palestine (shorter recension) -- Greek, ed. Dindorf (Teubner, 1871)"),
    "eusebius-demonstratio-evangelica-grc": ("tlg2018/tlg005/tlg2018.tlg005.1st1K-grc1.xml",
        "Eusebius, Demonstratio evangelica -- Greek, ed. Dindorf (Teubner, 1867)"),
    "eusebius-contra-marcellum-grc": ("tlg2018/tlg007/tlg2018.tlg007.1st1K-grc1.xml",
        "Eusebius, Against Marcellus -- Greek, ed. Erich Klostermann (GCS, Hinrichs, 1906)"),
    "eusebius-ecclesiastica-theologia-grc": ("tlg2018/tlg009/tlg2018.tlg009.1st1K-grc1.xml",
        "Eusebius, Ecclesiastical Theology -- Greek, ed. Klostermann (Hinrichs, 1906)"),
    "eusebius-vita-constantini-grc": ("tlg2018/tlg020/tlg2018.tlg020.1st1K-grc1.xml",
        "Eusebius, Life of Constantine -- Greek, ed. Ivar A. Heikel (GCS, Hinrichs, 1902)"),
    "eusebius-oratio-ad-coetum-grc": ("tlg2018/tlg021/tlg2018.tlg021.1st1K-grc1.xml",
        "Constantine, Oration to the Assembly of the Saints (transmitted with Eusebius) -- "
        "Greek, ed. Heikel (Hinrichs, 1902)"),
    "eusebius-laudes-constantini-grc": ("tlg2018/tlg022/tlg2018.tlg022.1st1K-grc1.xml",
        "Eusebius, In Praise of Constantine -- Greek, ed. Heikel (Hinrichs, 1902)"),
    "marcellus-fragmenta-grc": ("tlg2041/tlg001/tlg2041.tlg001.1st1K-grc1.xml",
        "Marcellus of Ancyra, Fragments -- Greek, ed. Klostermann (Eusebius Werke IV, Hinrichs, 1906)"),
    "athanasius-de-incarnatione-grc": ("tlg2035/tlg002/tlg2035.tlg002.1st1K-grc1.xml",
        "Athanasius, On the Incarnation -- Greek, ed. Archibald Robertson (London: Nutt, 1893)"),
    "athanasius-de-decretis-grc": ("tlg2035/tlg003/tlg2035.tlg003.1st1K-grc1.xml",
        "Athanasius, De decretis 41-42 as quoted by Gelasius -- Greek, ed. Loeschke & Heinemann "
        "(GCS, Hinrichs, 1918)"),
    "athanasius-contra-arianos-1-grc": ("tlg2035/tlg130/tlg2035.tlg130.1st1K-grc1.xml",
        "Athanasius, Orations against the Arians I -- Greek, ed. William Bright (Oxford: Clarendon, 1884)"),
    "athanasius-contra-arianos-2-grc": ("tlg2035/tlg131/tlg2035.tlg131.1st1K-grc1.xml",
        "Athanasius, Orations against the Arians II -- Greek, ed. Bright (Clarendon, 1884)"),
    "athanasius-contra-arianos-3-grc": ("tlg2035/tlg132/tlg2035.tlg132.1st1K-grc1.xml",
        "Athanasius, Orations against the Arians III -- Greek, ed. Bright (Clarendon, 1884)"),
    "athanasius-contra-arianos-4-grc": ("tlg2035/tlg117/tlg2035.tlg117.1st1K-grc1.xml",
        "[Athanasius], Oration IV against the Arians (spurious) -- Greek, ed. Bright (Clarendon, 1884)"),
    "gregory-nazianzen-oration-27-grc": ("tlg2022/tlg007/tlg2022.tlg007.1st1K-grc1.xml",
        "Gregory Nazianzen, Theological Oration 1 (Or. 27) -- Greek, ed. A. J. Mason (Cambridge UP, 1899)"),
    "gregory-nazianzen-oration-28-grc": ("tlg2022/tlg008/tlg2022.tlg008.1st1K-grc1.xml",
        "Gregory Nazianzen, Theological Oration 2 (Or. 28) -- Greek, ed. Mason (1899)"),
    "gregory-nazianzen-oration-29-grc": ("tlg2022/tlg009/tlg2022.tlg009.1st1K-grc1.xml",
        "Gregory Nazianzen, Theological Oration 3 (Or. 29) -- Greek, ed. Mason (1899)"),
    "gregory-nazianzen-oration-30-grc": ("tlg2022/tlg010/tlg2022.tlg010.1st1K-grc1.xml",
        "Gregory Nazianzen, Theological Oration 4 (Or. 30) -- Greek, ed. Mason (1899)"),
    "gregory-nazianzen-oration-31-grc": ("tlg2022/tlg011/tlg2022.tlg011.1st1K-grc1.xml",
        "Gregory Nazianzen, Theological Oration 5 (Or. 31) -- Greek, ed. Mason (1899)"),
    "epiphanius-ancoratus-grc": ("tlg2021/tlg001/tlg2021.tlg001.1st1K-grc1.xml",
        "Epiphanius, Ancoratus -- Greek, ed. Karl Holl (GCS, Hinrichs, 1915)"),
    "cyril-alexandria-xii-prophetas-grc": ("tlg4090/tlg001/tlg4090.tlg001.1st1K-grc1.xml",
        "Cyril of Alexandria, Commentary on the Twelve Prophets -- Greek, ed. P. E. Pusey "
        "(Oxford: Clarendon, 1868); parts of the OCR are damaged, flagged per unit"),
    # Wave 3, 2026-10-02: the church historians after Eusebius. NOT taken:
    #   - Philostorgius (Bidez 1913): what survives is Photius's epitome and
    #     testimonia, and Bidez's German source labels and apparatus run
    #     through the text of half its units;
    #   - Theodoret's Church History in Migne (1864): Parmentier's GCS text
    #     (1911) taken instead, divided to the section.
    "socrates-historia-ecclesiastica-grc": ("tlg2057/tlg002/tlg2057.tlg002.1st1K-grc1.xml",
        "Socrates Scholasticus, Church History -- Greek, ed. Robert Hussey, rev. William Bright "
        "(Oxford: Clarendon, 1893)"),
    "sozomen-historia-ecclesiastica-grc": ("tlg2048/tlg001/tlg2048.tlg001.1st1K-grc1.xml",
        "Sozomen, Church History -- Greek, ed. Robert Hussey (Oxford, 1860)"),
    "theodoret-historia-ecclesiastica-grc": ("tlg4089/tlg003/tlg4089.tlg003.opp-grc1.xml",
        "Theodoret, Church History -- Greek, ed. Léon Parmentier (GCS, Hinrichs, 1911); some "
        "apparatus runs into the text, flagged per unit"),
    "theodoret-historia-religiosa-grc": ("tlg4089/tlg004/tlg4089.tlg004.1st1K-grc1.xml",
        "Theodoret, Religious History (lives of the Syrian monks) -- Greek, ed. J. L. Schulze, "
        "repr. Migne PG 82 (1864)"),
    "evagrius-historia-ecclesiastica-grc": ("tlg2733/tlg001/tlg2733.tlg001.1st1K-grc1.xml",
        "Evagrius Scholasticus, Church History -- Greek, ed. Joseph Bidez & Léon Parmentier "
        "(London: Methuen, 1898)"),
    "gelasius-historia-ecclesiastica-grc": ("tlg2768/tlg001/tlg2768.tlg001.1st1K-grc1.xml",
        "Gelasius of Cyzicus, Church History -- Greek, ed. Gerhard Loeschke & Margret Heinemann "
        "(GCS, Hinrichs, 1918); it quotes Athanasius, De decretis 41-42, also a book here"),
    "mark-deacon-vita-porphyrii-grc": ("tlg2806/tlg001/tlg2806.tlg001.1st1K-grc1.xml",
        "Mark the Deacon, Life of Porphyry of Gaza -- Greek, ed. the Bonn philological society "
        "(Leipzig: Teubner, 1895)"),
    "passio-perpetuae-grc": ("tlg2016/tlg001/tlg2016.tlg001.1st1K-grc1.xml",
        "The Passion of Perpetua and Felicity, Greek version -- ed. J. Armitage Robinson "
        "(Cambridge UP, 1891)"),
    # Wave 4, 2026-10-02: early Christian apocrypha and pseudepigrapha. Two
    # ENGLISH witnesses: M. R. James, The Apocryphal New Testament (Oxford,
    # 1924) -- published before 1931; James died 1936, so public domain in
    # life+70 countries too. NOT taken:
    #   - Enoch in Flemming & Radermacher (1901): their German of the
    #     Ethiopic is interleaved (6,486 Latin-letter words); Swete taken;
    #   - Cramer's NT catenae (1838-44): one unit per chapter of the catena,
    #     too coarse to cite; they want their own verse-keyed converter.
    "acts-of-thomas-grc": ("tlg2038/tlg001/tlg2038.tlg001.1st1K-grc1.xml",
        "Acts of Thomas -- Greek, ed. Maximilian Bonnet (Leipzig: Mendelssohn, 1903)"),
    "acts-of-thomas-james": ("tlg2038/tlg001/tlg2038.tlg001.1st1K-eng1.xml",
        "Acts of Thomas -- English, M. R. James, The Apocryphal New Testament (Oxford, 1924)"),
    "acts-of-philip-grc": ("tlg2948/tlg001/tlg2948.tlg001.1st1K-grc1.xml",
        "Acts of Philip -- Greek, ed. Bonnet (1903)"),
    "acts-of-philip-james": ("tlg2948/tlg001/tlg2948.tlg001.1st1K-eng1.xml",
        "Acts of Philip -- English, M. R. James (1924), abridged"),
    "acts-of-barnabas-grc": ("tlg2949/tlg001/tlg2949.tlg001.1st1K-grc1.xml",
        "Acts of Barnabas -- Greek, ed. Bonnet (1903)"),
    "testament-of-abraham-a-grc": ("tlg1701/tlg001/tlg1701.tlg001.1st1K-grc1.xml",
        "Testament of Abraham, long recension (A) -- Greek, ed. M. R. James (Cambridge UP, 1892)"),
    "testament-of-abraham-b-grc": ("tlg1701/tlg002/tlg1701.tlg002.1st1K-grc1.xml",
        "Testament of Abraham, short recension (B) -- Greek, ed. James (1892)"),
    "lives-of-prophets-dorotheus-grc": ("tlg1750/tlg001/tlg1750.tlg001.1st1K-grc1.xml",
        "Lives of the Prophets, recension of Pseudo-Dorotheus -- Greek, ed. Theodor Schermann "
        "(Teubner, 1907)"),
    "lives-of-prophets-anonymous-grc": ("tlg1750/tlg002/tlg1750.tlg002.1st1K-grc1.xml",
        "Lives of the Prophets, anonymous recension -- Greek, ed. Schermann (1907)"),
    "enoch-swete-grc": ("tlg1463/tlg001/tlg1463.tlg001.1st1K-grc1.xml",
        "1 Enoch, the Greek fragments (1-32, 89) -- ed. H. B. Swete, The Old Testament in Greek "
        "III (Cambridge UP, 1905)"),
    # Cramer's catenae (2026-10-02), through convert_catena, not the prose
    # converter: see CATENA in structure_texts.py. Every book Cramer
    # printed with verse marks. NOT taken: his three "Supplementum et
    # varietas lectionis" (tlg003, 006, 007), which are variant readings by
    # page and line, not comments; the Munich-type Romans (tlg011) and Jude
    # (tlg046), which First1KGreek already divides by verse and want the
    # verse divs read, not measured.
    "catena-matthew-cramer-grc": ("tlg4102/tlg001/tlg4102.tlg001.1st1K-grc1.xml",
        "Catena on Matthew (Paris. Coislin. 23 etc.) -- Greek, ed. J. A. Cramer, Catenae Graecorum "
        "Patrum in Novum Testamentum I (Oxford, 1840)"),
    "catena-mark-cramer-grc": ("tlg4102/tlg002/tlg4102.tlg002.1st1K-grc1.xml",
        "Catena on Mark -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum I "
        "(Oxford, 1840)"),
    "catena-luke-cramer-grc": ("tlg4102/tlg004/tlg4102.tlg004.1st1K-grc1.xml",
        "Catena on Luke -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum II "
        "(Oxford, 1841)"),
    "catena-john-cramer-grc": ("tlg4102/tlg005/tlg4102.tlg005.1st1K-grc1.xml",
        "Catena on John -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum II "
        "(Oxford, 1841)"),
    "catena-acts-cramer-grc": ("tlg4102/tlg008/tlg4102.tlg008.1st1K-grc1.xml",
        "Catena on Acts -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum III "
        "(Oxford, 1838)"),
    "catena-romans-cramer-grc": ("tlg4102/tlg010/tlg4102.tlg010.1st1K-grc1.xml",
        "Catena on Romans (Vatican type) -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum IV "
        "(Oxford, 1844)"),
    "catena-1corinthians-cramer-grc": ("tlg4102/tlg012/tlg4102.tlg012.1st1K-grc1.xml",
        "Catena on 1 Corinthians -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum V "
        "(Oxford, 1841)"),
    "catena-2corinthians-cramer-grc": ("tlg4102/tlg013/tlg4102.tlg013.1st1K-grc1.xml",
        "Catena on 2 Corinthians -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum V "
        "(Oxford, 1841)"),
    "catena-galatians-cramer-grc": ("tlg4102/tlg019/tlg4102.tlg019.1st1K-grc1.xml",
        "Catena on Galatians -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VI "
        "(Oxford, 1842)"),
    "catena-ephesians-cramer-grc": ("tlg4102/tlg020/tlg4102.tlg020.1st1K-grc1.xml",
        "Catena on Ephesians -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VI "
        "(Oxford, 1842)"),
    "catena-philippians-cramer-grc": ("tlg4102/tlg021/tlg4102.tlg021.1st1K-grc1.xml",
        "Catena on Philippians -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VI "
        "(Oxford, 1842)"),
    "catena-colossians-cramer-grc": ("tlg4102/tlg022/tlg4102.tlg022.1st1K-grc1.xml",
        "Catena on Colossians -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VI "
        "(Oxford, 1842)"),
    "catena-1thessalonians-cramer-grc": ("tlg4102/tlg023/tlg4102.tlg023.1st1K-grc1.xml",
        "Catena on 1 Thessalonians -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VI "
        "(Oxford, 1842)"),
    "catena-2thessalonians-cramer-grc": ("tlg4102/tlg024/tlg4102.tlg024.1st1K-grc1.xml",
        "Catena on 2 Thessalonians -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VI "
        "(Oxford, 1842)"),
    "catena-1timothy-cramer-grc": ("tlg4102/tlg034/tlg4102.tlg034.1st1K-grc1.xml",
        "Catena on 1 Timothy -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VII "
        "(Oxford, 1843)"),
    "catena-2timothy-cramer-grc": ("tlg4102/tlg035/tlg4102.tlg035.1st1K-grc1.xml",
        "Catena on 2 Timothy -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VII "
        "(Oxford, 1843)"),
    "catena-titus-cramer-grc": ("tlg4102/tlg036/tlg4102.tlg036.1st1K-grc1.xml",
        "Catena on Titus -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VII "
        "(Oxford, 1843)"),
    "catena-philemon-cramer-grc": ("tlg4102/tlg037/tlg4102.tlg037.1st1K-grc1.xml",
        "Catena on Philemon -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VII "
        "(Oxford, 1843)"),
    "catena-hebrews-cramer-grc": ("tlg4102/tlg038/tlg4102.tlg038.1st1K-grc1.xml",
        "Catena on Hebrews -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VII "
        "(Oxford, 1843)"),
    "catena-james-cramer-grc": ("tlg4102/tlg040/tlg4102.tlg040.1st1K-grc1.xml",
        "Catena on James -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VIII "
        "(Oxford, 1840)"),
    "catena-1peter-cramer-grc": ("tlg4102/tlg041/tlg4102.tlg041.1st1K-grc1.xml",
        "Catena on 1 Peter -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VIII "
        "(Oxford, 1840)"),
    "catena-2peter-cramer-grc": ("tlg4102/tlg042/tlg4102.tlg042.1st1K-grc1.xml",
        "Catena on 2 Peter -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VIII "
        "(Oxford, 1840)"),
    "catena-1john-cramer-grc": ("tlg4102/tlg043/tlg4102.tlg043.1st1K-grc1.xml",
        "Catena on 1 John -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VIII "
        "(Oxford, 1840)"),
    "catena-2john-cramer-grc": ("tlg4102/tlg044/tlg4102.tlg044.1st1K-grc1.xml",
        "Catena on 2 John -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VIII "
        "(Oxford, 1840)"),
    "catena-3john-cramer-grc": ("tlg4102/tlg045/tlg4102.tlg045.1st1K-grc1.xml",
        "Catena on 3 John -- Greek, ed. J. A. Cramer, Catenae Graecorum Patrum in Novum Testamentum VIII "
        "(Oxford, 1840)"),
}


# CSEL (Corpus Scriptorum Ecclesiasticorum Latinorum, Vienna) -- the Latin
# FATHERS, 2026-10-02, from OpenGreekAndLatin/csel-dev: each the TEI of a
# CSEL volume published 1867-1922 (all before 1931; the Latin text has no
# author's right and any editor's right is long expired), OCR'd and
# machine-corrected by Leipzig, licence CC BY-SA 4.0 read from each file.
# The text is NOT proofread: the books say so. NOT taken:
#   - verse (Commodian; Lactantius' Phoenix and De passione; Augustine's
#     Psalmus contra partem Donati): no prose divisions to cite;
#   - stoa0040.stoa054.opp-lat2, filed as Augustine's De natura et gratia
#     but from Zangemeister's 1882 volume (Orosius): mislabelled;
#   - Cyprian: not in csel-dev; Jerome beyond the Letters and Jeremiah, and
#     Augustine's sermons and Psalms: not there either.
CSEL_RAW = "https://raw.githubusercontent.com/OpenGreekAndLatin/csel-dev/master/data/{path}"
CSEL = {
    "ambrose-apologia-david-altera-lat": ("stoa0022/stoa014/stoa0022.stoa014.opp-lat1.xml",
        "Apologia Altera Prophetae David -- ed. Karl Schenkl, CSEL 32.2 (1897)"),
    "ambrose-apologia-david-lat": ("stoa0022/stoa015/stoa0022.stoa015.opp-lat1.xml",
        "Apologia Prophetae David Ad Theodosium Augustum -- ed. Karl Schenkl, CSEL 32.2 (1897)"),
    "ambrose-de-benedictionibus-patriarcharum-lat": ("stoa0022/stoa019/stoa0022.stoa019.opp-lat1.xml",
        "De Benedictionibus Patriarcharum Liber Unus -- ed. Karl Schenkl, CSEL 32.2 (1897)"),
    "ambrose-de-cain-et-abel-lat": ("stoa0022/stoa021/stoa0022.stoa021.opp-lat1.xml",
        "De Cain et Abel -- ed. Karl Schenkl, CSEL 32.1 (1896)"),
    "ambrose-de-helia-lat": ("stoa0022/stoa025/stoa0022.stoa025.opp-lat1.xml",
        "De Helia et Ieiunio -- ed. Karl Schenkl, CSEL 32.2 (1897)"),
    "ambrose-de-fuga-saeculi-lat": ("stoa0022/stoa029/stoa0022.stoa029.opp-lat1.xml",
        "De Fuga Saeculi -- ed. Karl Schenkl, CSEL 32.2 (1897)"),
    "ambrose-de-interpellatione-iob-lat": ("stoa0022/stoa032/stoa0022.stoa032.opp-lat1.xml",
        "De Interpellatione Iob et David -- ed. Karl Schenkl, CSEL 32.2 (1897)"),
    "ambrose-de-iacob-lat": ("stoa0022/stoa034/stoa0022.stoa034.opp-lat1.xml",
        "De Iacob -- ed. Karl Schenkl, CSEL 32.2 (1897)"),
    "ambrose-de-ioseph-lat": ("stoa0022/stoa035/stoa0022.stoa035.opp-lat1.xml",
        "De Joseph -- ed. Karl Schenkl, CSEL 32.2 (1897)"),
    "ambrose-de-nabuthae-lat": ("stoa0022/stoa038/stoa0022.stoa038.opp-lat1.xml",
        "De Nabuthae -- ed. Karl Schenkl, CSEL 32.2 (1897)"),
    "ambrose-de-noe-lat": ("stoa0022/stoa039/stoa0022.stoa039.opp-lat1.xml",
        "De Noe -- ed. Karl Schenkl, CSEL 32.1 (1896)"),
    "ambrose-de-paradiso-lat": ("stoa0022/stoa042/stoa0022.stoa042.opp-lat1.xml",
        "De Paradiso -- ed. Karl Schenkl, CSEL 32.1 (1896)"),
    "ambrose-de-tobia-lat": ("stoa0022/stoa044/stoa0022.stoa044.opp-lat1.xml",
        "De Tobia -- ed. Karl Schenkl, CSEL 32.2 (1897)"),
    "ambrose-explanatio-psalmorum-xii-lat": ("stoa0022/stoa048/stoa0022.stoa048.opp-lat1.xml",
        "Explanatio Psalmorum XII -- ed. Michael Petschenig, CSEL 64 (1919)"),
    "ambrose-expositio-lucam-lat": ("stoa0022/stoa051/stoa0022.stoa051.opp-lat1.xml",
        "Expositio Evangelii secundum Lucan -- ed. Karl Schenkl & Henricus Schenkl, CSEL 32.4 (1902)"),
    "ambrose-expositio-psalmi-118-lat": ("stoa0022/stoa052/stoa0022.stoa052.opp-lat1.xml",
        "Expositio Psalmi CXVIII -- ed. Michael Petschenig, CSEL 62 (1913)"),
    "ambrose-exameron-lat": ("stoa0022/stoa054/stoa0022.stoa054.opp-lat1.xml",
        "Exameron -- ed. Karl Schenkl, CSEL 32.1 (1896)"),
    "arnobius-adversus-nationes-lat": ("stoa0034/stoa001/stoa0034.stoa001.opp-lat1.xml",
        "Adversus nationes Libri VII -- ed. August Reifferscheid, CSEL 4 (1875)"),
    "augustine-confessiones-lat": ("stoa0040/stoa001/stoa0040.stoa001.opp-lat1.xml",
        "Confessiones -- ed. Pius Knöll, CSEL 33 (1896)"),
    "augustine-de-civitate-dei-lat": ("stoa0040/stoa003/stoa0040.stoa003.opp-lat3.xml",
        "De Civitate Dei -- ed. Emmanuel Hoffmann, CSEL 40 (1899-1900)"),
    "augustine-de-fide-et-symbolo-lat": ("stoa0040/stoa006/stoa0040.stoa006.opp-lat1.xml",
        "De Fide et Symbolo -- ed. Joseph Zycha, CSEL 41 (1900)"),
    "augustine-epistulae-lat": ("stoa0040/stoa011/stoa0040.stoa011.opp-lat2.xml",
        "Epistulae -- ed. Alois Goldbacher, CSEL 34.1-2, 44, 57 (1895-1911)"),
    "augustine-contra-academicos-lat": ("stoa0040/stoa016/stoa0040.stoa016.opp-lat1.xml",
        "Contra Academicos -- ed. Pius Knöll, CSEL 63 (1922)"),
    "augustine-contra-adimantum-lat": ("stoa0040/stoa017/stoa0040.stoa017.opp-lat1.xml",
        "Contra Adimantum -- ed. Joseph Zycha, CSEL 25.1 (1891)"),
    "augustine-contra-cresconium-lat": ("stoa0040/stoa019/stoa0040.stoa019.opp-lat1.xml",
        "Contra Cresconium -- ed. Michael Petschenig, CSEL 52 (1909)"),
    "augustine-ad-catholicos-de-secta-donatistarum-lat": ("stoa0040/stoa020/stoa0040.stoa020.opp-lat1.xml",
        "Epistula ad Catholicos de Secta Donatistarum -- ed. Michael Petschenig, CSEL 52 (1909)"),
    "augustine-contra-duas-epistulas-pelagianorum-lat": ("stoa0040/stoa021/stoa0040.stoa021.opp-lat1.xml",
        "Contra Duas Epistulas Pelegianorum -- ed. Karl F. Urba & Joseph Zycha, CSEL 60 (1913)"),
    "augustine-contra-epistulam-parmeniani-lat": ("stoa0040/stoa023/stoa0040.stoa023.opp-lat1.xml",
        "Contra Epistulam Parmeniani -- ed. Michael Petschenig, CSEL 51 (1908)"),
    "augustine-contra-faustum-lat": ("stoa0040/stoa024/stoa0040.stoa024.opp-lat1.xml",
        "Contra Faustum -- ed. Joseph Zycha, CSEL 25.1 (1891)"),
    "augustine-contra-gaudentium-lat": ("stoa0040/stoa025/stoa0040.stoa025.opp-lat1.xml",
        "Contra Gaudentium Donatistarum Episcopum -- ed. Michael Petschenig, CSEL 53 (1910)"),
    "augustine-contra-litteras-petiliani-lat": ("stoa0040/stoa027/stoa0040.stoa027.opp-lat1.xml",
        "Contra Litteras Petiliani -- ed. Michael Petschenig, CSEL 52 (1909)"),
    "augustine-contra-mendacium-lat": ("stoa0040/stoa029/stoa0040.stoa029.opp-lat1.xml",
        "Contra Mendacium -- ed. Joseph Zycha, CSEL 41 (1900)"),
    "augustine-contra-secundinum-lat": ("stoa0040/stoa031/stoa0040.stoa031.opp-lat1.xml",
        "Contra Secundinem -- ed. Joseph Zycha, CSEL 25.2 (1892)"),
    "augustine-de-agone-christiano-lat": ("stoa0040/stoa032/stoa0040.stoa032.opp-lat1.xml",
        "De agone christiano -- ed. Joseph Zycha, CSEL 41 (1900)"),
    "augustine-de-natura-et-origine-animae-lat": ("stoa0040/stoa033/stoa0040.stoa033.opp-lat1.xml",
        "De Natura et Origine Animae -- ed. Karl F. Urba & Joseph Zycha, CSEL 60 (1913)"),
    "augustine-de-beata-vita-lat": ("stoa0040/stoa034/stoa0040.stoa034.opp-lat1.xml",
        "De Beata Vita -- ed. Pius Knöll, CSEL 63 (1922)"),
    "augustine-de-bono-coniugali-lat": ("stoa0040/stoa035/stoa0040.stoa035.opp-lat1.xml",
        "De bono coniugali -- ed. Joseph Zycha, CSEL 41 (1900)"),
    "augustine-de-coniugiis-adulterinis-lat": ("stoa0040/stoa036/stoa0040.stoa036.opp-lat1.xml",
        "De Conjugiis Adulterinis -- ed. Joseph Zycha, CSEL 41 (1900)"),
    "augustine-de-consensu-evangelistarum-lat": ("stoa0040/stoa037/stoa0040.stoa037.opp-lat1.xml",
        "De Consensu Evangelistarum -- ed. Franz Weirich, CSEL 43 (1904)"),
    "augustine-de-duabus-animabus-lat": ("stoa0040/stoa040/stoa0040.stoa040.opp-lat1.xml",
        "Du Duabus Animabus -- ed. Joseph Zycha, CSEL 25.1 (1891)"),
    "augustine-de-fide-et-operibus-lat": ("stoa0040/stoa041/stoa0040.stoa041.opp-lat1.xml",
        "De Fide et Operibus -- ed. Joseph Zycha, CSEL 41 (1900)"),
    "augustine-de-genesi-ad-litteram-imperfectus-lat": ("stoa0040/stoa042/stoa0040.stoa042.opp-lat1.xml",
        "De Genesi Ad Litteram Imperfectus Liber -- ed. Joseph Zycha, CSEL 28.1 (1894)"),
    "augustine-de-gestis-pelagii-lat": ("stoa0040/stoa044/stoa0040.stoa044.opp-lat1.xml",
        "De Gestis Pelagii -- ed. Karl F. Urba & Joseph Zycha, CSEL 42 (1904)"),
    "augustine-de-gratia-christi-lat": ("stoa0040/stoa046/stoa0040.stoa046.opp-lat1.xml",
        "De Gratia Christ -- ed. Karl F. Urba & Joseph Zycha, CSEL 42 (1904)"),
    "augustine-de-mendacio-lat": ("stoa0040/stoa050/stoa0040.stoa050.opp-lat1.xml",
        "De Mendacio -- ed. Joseph Zycha, CSEL 41 (1900)"),
    "augustine-de-natura-boni-lat": ("stoa0040/stoa053/stoa0040.stoa053.opp-lat1.xml",
        "De Natura Boni -- ed. Joseph Zycha, CSEL 25.2 (1892)"),
    "augustine-de-natura-et-gratia-lat": ("stoa0040/stoa054/stoa0040.stoa054.opp-lat1.xml",
        "De Natura et Gratia -- ed. Karl F. Urba & Joseph Zycha, CSEL 60 (1913)"),
    "augustine-de-opere-monachorum-lat": ("stoa0040/stoa055/stoa0040.stoa055.opp-lat1.xml",
        "De Opere Monachorum -- ed. Joseph Zycha, CSEL 41 (1900)"),
    "augustine-de-ordine-lat": ("stoa0040/stoa056/stoa0040.stoa056.opp-lat1.xml",
        "De Ordine -- ed. Pius Knöll, CSEL 63 (1922)"),
    "augustine-de-peccatorum-meritis-lat": ("stoa0040/stoa057/stoa0040.stoa057.opp-lat1.xml",
        "De Peccatorum Meritis et Remissione et de Baptismo Parvulorum -- ed. Karl F. Urba & Joseph Zycha, CSEL 60 (1913)"),
    "augustine-de-sancta-virginitate-lat": ("stoa0040/stoa060/stoa0040.stoa060.opp-lat1.xml",
        "De Sancta Virginitate -- ed. Joseph Zycha, CSEL 41 (1900)"),
    "augustine-de-spiritu-et-littera-lat": ("stoa0040/stoa062/stoa0040.stoa062.opp-lat1.xml",
        "De Spiritu et Littera -- ed. Karl F. Urba & Joseph Zycha, CSEL 60 (1913)"),
    "augustine-de-unico-baptismo-lat": ("stoa0040/stoa063/stoa0040.stoa063.opp-lat1.xml",
        "Liber de Unico Baptismo -- ed. Michael Petschenig, CSEL 53 (1910)"),
    "augustine-de-utilitate-credendi-lat": ("stoa0040/stoa064/stoa0040.stoa064.opp-lat1.xml",
        "De Utilitate Credendi -- ed. Joseph Zycha, CSEL 25.1 (1891)"),
    "augustine-quaestiones-in-heptateuchum-lat": ("stoa0040/stoa074/stoa0040.stoa074.opp-lat1.xml",
        "Quaestiones in Heptateuchum -- ed. Joseph Zycha, CSEL 28.2 (1895)"),
    "augustine-retractationes-lat": ("stoa0040/stoa077/stoa0040.stoa077.opp-lat1.xml",
        "Retractationum -- ed. Pius Knöll, CSEL 36 (1902)"),
    "augustine-speculum-lat": ("stoa0040/stoa080/stoa0040.stoa080.opp-lat1.xml",
        "Liber qui appellatur Speculum -- ed. Franz Weihrich, CSEL 12 (1887)"),
    "jerome-epistulae-lat": ("stoa0162/stoa004/stoa0162.stoa004.opp-lat1.xml",
        "Epistulae -- ed. Isidor Hilberg, CSEL 54-56 (1910-1918)"),
    "jerome-in-hieremiam-lat": ("stoa0162/stoa024/stoa0162.stoa024.opp-lat1.xml",
        "In Hieremiam Prophetam Libri Sex -- ed. Siegfried Reiter, CSEL 59 (1913)"),
    "lactantius-de-mortibus-persecutorum-lat": ("stoa0171/stoa002/stoa0171.stoa002.opp-lat1.xml",
        "De Mortibus Persecutorum -- ed. Samuel Brandt & Georg Laubmann, CSEL 27 (1897)"),
    "lactantius-de-ira-dei-lat": ("stoa0171/stoa006/stoa0171.stoa006.opp-lat1.xml",
        "De Ira Dei -- ed. Samuel Brandt & Georg Laubmann, CSEL 27 (1897)"),
    "lactantius-de-opificio-dei-lat": ("stoa0171/stoa007/stoa0171.stoa007.opp-lat1.xml",
        "De Opificio Dei -- ed. Samuel Brandt & Georg Laubmann, CSEL 27 (1897)"),
    "lactantius-epitome-lat": ("stoa0171/stoa008/stoa0171.stoa008.opp-lat1.xml",
        "Epitome Divinarum Institutionum -- ed. Samuel Brandt & Georg Laubmann, CSEL 19 (1890)"),
    "lactantius-divinae-institutiones-lat": ("stoa0171/stoa009/stoa0171.stoa009.opp-lat1.xml",
        "Divinarum Institutionum -- ed. Samuel Brandt & Georg Laubmann, CSEL 19 (1890)"),
    "lactantius-fragmenta-lat": ("stoa0171/stoa010/stoa0171.stoa010.opp-lat1.xml",
        "Fragmenta -- ed. Samuel Brandt & Georg Laubmann, CSEL 27 (1897)"),
    "minucius-felix-octavius-lat": ("stoa0203/stoa001/stoa0203.stoa001.opp-lat2.xml",
        "Octavius -- ed. Karl Halm, CSEL 2 (1867)"),
    "tertullian-ad-nationes-lat": ("stoa0275/stoa002/stoa0275.stoa002.opp-lat2.xml",
        "Ad Nationes Libri Duo -- ed. August Reifferscheid & Georg Wissowa, CSEL 20 (1890)"),
    "tertullian-adversus-hermogenem-lat": ("stoa0275/stoa004/stoa0275.stoa004.opp-lat2.xml",
        "Adversus Hermogenem -- ed. Emil Kroymann, CSEL 47 (1906)"),
    "tertullian-adversus-marcionem-lat": ("stoa0275/stoa006/stoa0275.stoa006.opp-lat2.xml",
        "Adversus Marcionem -- ed. Emil Kroymann, CSEL 47 (1906)"),
    "tertullian-adversus-praxean-lat": ("stoa0275/stoa007/stoa0275.stoa007.opp-lat2.xml",
        "Adversus Praxean -- ed. Emil Kroymann, CSEL 47 (1900)"),
    "tertullian-adversus-valentinianos-lat": ("stoa0275/stoa008/stoa0275.stoa008.opp-lat2.xml",
        "Adversus Valentinianos -- ed. Emil Kroymann, CSEL 47 (1900)"),
    "tertullian-de-anima-lat": ("stoa0275/stoa010/stoa0275.stoa010.opp-lat2.xml",
        "De Anima -- ed. August Reifferscheid & Georg Wissowa, CSEL 20 (1890)"),
    "tertullian-de-baptismo-lat": ("stoa0275/stoa011/stoa0275.stoa011.opp-lat2.xml",
        "De Anima -- ed. August Reifferscheid & Georg Wissowa, CSEL 20 (1890)"),
    "tertullian-de-idololatria-lat": ("stoa0275/stoa017/stoa0275.stoa017.opp-lat2.xml",
        "De idololatria -- ed. August Reifferscheid & Georg Wissowa, CSEL 20 (1890)"),
    "tertullian-de-ieiunio-lat": ("stoa0275/stoa018/stoa0275.stoa018.opp-lat2.xml",
        "De Ieiunio Adversus Psychicos -- ed. August Reifferscheid & Georg Wissowa, CSEL 20 (1890)"),
    "tertullian-de-oratione-lat": ("stoa0275/stoa020/stoa0275.stoa020.opp-lat2.xml",
        "De Oratione -- ed. August Reifferscheid & Georg Wissowa, CSEL 20 (1890)"),
    "tertullian-de-patientia-lat": ("stoa0275/stoa023/stoa0275.stoa023.opp-lat2.xml",
        "De Patientia -- ed. Emil Kroymann, CSEL 47 (1900)"),
    "tertullian-de-pudicitia-lat": ("stoa0275/stoa025/stoa0275.stoa025.opp-lat2.xml",
        "De Pudicitia -- ed. August Reifferscheid & Georg Wissowa, CSEL 20 (1890)"),
    "tertullian-de-resurrectione-carnis-lat": ("stoa0275/stoa026/stoa0275.stoa026.opp-lat2.xml",
        "De Carnis Resurrectione -- ed. Emil Kroymann, CSEL 47 (1900)"),
    "tertullian-de-spectaculis-lat": ("stoa0275/stoa027/stoa0275.stoa027.opp-lat2.xml",
        "De Spectaculis -- ed. August Reifferscheid & Georg Wissowa, CSEL 20 (1890)"),
    "tertullian-de-testimonio-animae-lat": ("stoa0275/stoa028/stoa0275.stoa028.opp-lat2.xml",
        "De Testimonio Animae -- ed. August Reifferscheid & Georg Wissowa, CSEL 20 (1890)"),
    "tertullian-scorpiace-lat": ("stoa0275/stoa030/stoa0275.stoa030.opp-lat2.xml",
        "Scorpiace -- ed. August Reifferscheid & Georg Wissowa, CSEL 20 (1890)"),
}

# slug -> (repo, path, note)   — PD status verified per edition, see notes
PERSEUS = {
    "iliad-butler": ("canonical-greekLit",
        "tlg0012/tlg001/tlg0012.tlg001.perseus-eng4.xml",
        "Homer, Iliad — Samuel Butler 1898 (PD); urn ...tlg0012.tlg001.perseus-eng4"),
    "odyssey-eng4": ("canonical-greekLit",
        "tlg0012/tlg002/tlg0012.tlg002.perseus-eng4.xml",
        "Homer, Odyssey — English (eng4; translator recorded from TEI header at structure time)"),
    "aeneid-williams": ("canonical-latinLit",
        "phi0690/phi003/phi0690.phi003.perseus-eng2.xml",
        "Virgil, Aeneid — Theodore C. Williams 1910 (PD); urn ...phi0690.phi003.perseus-eng2"),
    # Sophocles, the seven plays (Adler vol. 5), 2026-10-02. All seven are
    # R. C. Jebb's prose translations (Cambridge, 1887-1900: PD), "modernized by
    # Perseus"; the rights line read is each file's own titleStmt/sourceDesc,
    # and every one names Jebb. Perseus markup is CC BY-SA; what we keep is
    # Jebb's PD text plus the Greek line numbers, which are facts. Trachiniae
    # is eng3 on purpose: eng4 is Torrance 1966, in copyright (Perseus itself
    # comments it out of the catalogue). Drama converter: convert_tei_drama.
    "sophocles-trachiniae-jebb": ("canonical-greekLit",
        "tlg0011/tlg001/tlg0011.tlg001.perseus-eng3.xml",
        "Sophocles, Trachiniae — R. C. Jebb 1892 (PD); urn ...tlg0011.tlg001.perseus-eng3"),
    "sophocles-antigone-jebb": ("canonical-greekLit",
        "tlg0011/tlg002/tlg0011.tlg002.perseus-eng2.xml",
        "Sophocles, Antigone — R. C. Jebb 1891 (PD); urn ...tlg0011.tlg002.perseus-eng2"),
    "sophocles-ajax-jebb": ("canonical-greekLit",
        "tlg0011/tlg003/tlg0011.tlg003.perseus-eng2.xml",
        "Sophocles, Ajax — R. C. Jebb 1896 (PD); urn ...tlg0011.tlg003.perseus-eng2"),
    "sophocles-oedipus-tyrannus-jebb": ("canonical-greekLit",
        "tlg0011/tlg004/tlg0011.tlg004.perseus-eng2.xml",
        "Sophocles, Oedipus Tyrannus — R. C. Jebb 1887 (PD); urn ...tlg0011.tlg004.perseus-eng2"),
    "sophocles-electra-jebb": ("canonical-greekLit",
        "tlg0011/tlg005/tlg0011.tlg005.perseus-eng2.xml",
        "Sophocles, Electra — R. C. Jebb 1894 (PD); urn ...tlg0011.tlg005.perseus-eng2"),
    "sophocles-philoctetes-jebb": ("canonical-greekLit",
        "tlg0011/tlg006/tlg0011.tlg006.perseus-eng2.xml",
        "Sophocles, Philoctetes — R. C. Jebb 1898 (PD); urn ...tlg0011.tlg006.perseus-eng2"),
    "sophocles-oedipus-colonus-jebb": ("canonical-greekLit",
        "tlg0011/tlg007/tlg0011.tlg007.perseus-eng2.xml",
        "Sophocles, Oedipus at Colonus — R. C. Jebb 1889 (PD); urn ...tlg0011.tlg007.perseus-eng2"),
    # Aeschylus, the seven plays (Adler vol. 5), 2026-10-02. Herbert Weir
    # Smyth's Loeb prose (Heinemann/Putnam, 1922 & 1926), "modernized by
    # Perseus". Rights line read per file: every titleStmt names Smyth. PD in
    # the US (published before 1931) and life+70 elsewhere (Smyth d. 1937).
    # Agamemnon is eng3 (Smyth) on purpose; eng4 is Browning's 1889 verse,
    # also PD, left for a second witness later.
    "aeschylus-supplices-smyth": ("canonical-greekLit",
        "tlg0085/tlg001/tlg0085.tlg001.perseus-eng2.xml",
        "Aeschylus, Suppliant Maidens — H. W. Smyth 1922 (PD); urn ...tlg0085.tlg001.perseus-eng2"),
    "aeschylus-persians-smyth": ("canonical-greekLit",
        "tlg0085/tlg002/tlg0085.tlg002.perseus-eng2.xml",
        "Aeschylus, Persians — H. W. Smyth 1922 (PD); urn ...tlg0085.tlg002.perseus-eng2"),
    "aeschylus-prometheus-smyth": ("canonical-greekLit",
        "tlg0085/tlg003/tlg0085.tlg003.perseus-eng2.xml",
        "Aeschylus, Prometheus Bound — H. W. Smyth 1922 (PD); urn ...tlg0085.tlg003.perseus-eng2"),
    "aeschylus-seven-smyth": ("canonical-greekLit",
        "tlg0085/tlg004/tlg0085.tlg004.perseus-eng2.xml",
        "Aeschylus, Seven Against Thebes — H. W. Smyth 1922 (PD); urn ...tlg0085.tlg004.perseus-eng2"),
    "aeschylus-agamemnon-smyth": ("canonical-greekLit",
        "tlg0085/tlg005/tlg0085.tlg005.perseus-eng3.xml",
        "Aeschylus, Agamemnon — H. W. Smyth 1926 (PD); urn ...tlg0085.tlg005.perseus-eng3"),
    "aeschylus-libation-bearers-smyth": ("canonical-greekLit",
        "tlg0085/tlg006/tlg0085.tlg006.perseus-eng2.xml",
        "Aeschylus, Libation Bearers — H. W. Smyth 1926 (PD); urn ...tlg0085.tlg006.perseus-eng2"),
    "aeschylus-eumenides-smyth": ("canonical-greekLit",
        "tlg0085/tlg007/tlg0085.tlg007.perseus-eng2.xml",
        "Aeschylus, Eumenides — H. W. Smyth 1926 (PD); urn ...tlg0085.tlg007.perseus-eng2"),
    # Euripides, the nineteen plays (Adler vol. 5), 2026-10-02. E. P.
    # Coleridge's prose (George Bell, 1891 & 1906), Bacchae alone in T. A.
    # Buckley's (Bohn, 1850): the translator Perseus has for it. Most are
    # "modernized by Perseus" and Iphigenia in Tauris says "heavily adapted".
    # Rights line read per file: each titleStmt names Coleridge or Buckley.
    # Rhesus is eng3 (Coleridge) on purpose: eng4 is Gilbert Murray 1913,
    # PD in the US but not yet in the UK (Murray d. 1957).
    "euripides-cyclops-coleridge": ("canonical-greekLit",
        "tlg0006/tlg001/tlg0006.tlg001.perseus-eng2.xml",
        "Euripides, Cyclops — E. P. Coleridge 1891 (PD); urn ...tlg0006.tlg001.perseus-eng2"),
    "euripides-alcestis-coleridge": ("canonical-greekLit",
        "tlg0006/tlg002/tlg0006.tlg002.perseus-eng2.xml",
        "Euripides, Alcestis — E. P. Coleridge 1906 (PD); urn ...tlg0006.tlg002.perseus-eng2"),
    "euripides-medea-coleridge": ("canonical-greekLit",
        "tlg0006/tlg003/tlg0006.tlg003.perseus-eng2.xml",
        "Euripides, Medea — E. P. Coleridge 1906 (PD); urn ...tlg0006.tlg003.perseus-eng2"),
    "euripides-heracleidae-coleridge": ("canonical-greekLit",
        "tlg0006/tlg004/tlg0006.tlg004.perseus-eng2.xml",
        "Euripides, Heracleidae — E. P. Coleridge 1906 (PD); urn ...tlg0006.tlg004.perseus-eng2"),
    "euripides-hippolytus-coleridge": ("canonical-greekLit",
        "tlg0006/tlg005/tlg0006.tlg005.perseus-eng2.xml",
        "Euripides, Hippolytus — E. P. Coleridge 1906 (PD); urn ...tlg0006.tlg005.perseus-eng2"),
    "euripides-andromache-coleridge": ("canonical-greekLit",
        "tlg0006/tlg006/tlg0006.tlg006.perseus-eng2.xml",
        "Euripides, Andromache — E. P. Coleridge 1891 (PD); urn ...tlg0006.tlg006.perseus-eng2"),
    "euripides-hecuba-coleridge": ("canonical-greekLit",
        "tlg0006/tlg007/tlg0006.tlg007.perseus-eng2.xml",
        "Euripides, Hecuba — E. P. Coleridge 1891 (PD); urn ...tlg0006.tlg007.perseus-eng2"),
    "euripides-suppliants-coleridge": ("canonical-greekLit",
        "tlg0006/tlg008/tlg0006.tlg008.perseus-eng2.xml",
        "Euripides, Suppliants — E. P. Coleridge 1906 (PD); urn ...tlg0006.tlg008.perseus-eng2"),
    "euripides-heracles-coleridge": ("canonical-greekLit",
        "tlg0006/tlg009/tlg0006.tlg009.perseus-eng2.xml",
        "Euripides, Heracles — E. P. Coleridge 1891 (PD); urn ...tlg0006.tlg009.perseus-eng2"),
    "euripides-ion-coleridge": ("canonical-greekLit",
        "tlg0006/tlg010/tlg0006.tlg010.perseus-eng2.xml",
        "Euripides, Ion — E. P. Coleridge 1906 (PD); urn ...tlg0006.tlg010.perseus-eng2"),
    "euripides-trojan-women-coleridge": ("canonical-greekLit",
        "tlg0006/tlg011/tlg0006.tlg011.perseus-eng2.xml",
        "Euripides, Trojan Women — E. P. Coleridge 1906 (PD); urn ...tlg0006.tlg011.perseus-eng2"),
    "euripides-electra-coleridge": ("canonical-greekLit",
        "tlg0006/tlg012/tlg0006.tlg012.perseus-eng2.xml",
        "Euripides, Electra — E. P. Coleridge 1891 (PD); urn ...tlg0006.tlg012.perseus-eng2"),
    "euripides-iphigenia-tauris-coleridge": ("canonical-greekLit",
        "tlg0006/tlg013/tlg0006.tlg013.perseus-eng2.xml",
        "Euripides, Iphigenia in Tauris — E. P. Coleridge 1891 (PD); urn ...tlg0006.tlg013.perseus-eng2"),
    "euripides-helen-coleridge": ("canonical-greekLit",
        "tlg0006/tlg014/tlg0006.tlg014.perseus-eng2.xml",
        "Euripides, Helen — E. P. Coleridge 1906 (PD); urn ...tlg0006.tlg014.perseus-eng2"),
    "euripides-phoenissae-coleridge": ("canonical-greekLit",
        "tlg0006/tlg015/tlg0006.tlg015.perseus-eng2.xml",
        "Euripides, Phoenissae — E. P. Coleridge 1891 (PD); urn ...tlg0006.tlg015.perseus-eng2"),
    "euripides-orestes-coleridge": ("canonical-greekLit",
        "tlg0006/tlg016/tlg0006.tlg016.perseus-eng2.xml",
        "Euripides, Orestes — E. P. Coleridge 1891 (PD); urn ...tlg0006.tlg016.perseus-eng2"),
    "euripides-bacchae-buckley": ("canonical-greekLit",
        "tlg0006/tlg017/tlg0006.tlg017.perseus-eng2.xml",
        "Euripides, Bacchae — T. A. Buckley 1850 (PD); urn ...tlg0006.tlg017.perseus-eng2"),
    "euripides-iphigenia-aulis-coleridge": ("canonical-greekLit",
        "tlg0006/tlg018/tlg0006.tlg018.perseus-eng2.xml",
        "Euripides, Iphigenia in Aulis — E. P. Coleridge 1891 (PD); urn ...tlg0006.tlg018.perseus-eng2"),
    "euripides-rhesus-coleridge": ("canonical-greekLit",
        "tlg0006/tlg019/tlg0006.tlg019.perseus-eng3.xml",
        "Euripides, Rhesus — E. P. Coleridge 1906 (PD); urn ...tlg0006.tlg019.perseus-eng3"),
    # Aristophanes (Adler vol. 5), 2026-10-02: Clouds ONLY. Perseus has
    # English for two comedies. Clouds is W. J. Hickie (Bohn, 1853): PD, its
    # titleStmt names Hickie. Birds is deliberately NOT taken: its edition is
    # "Anonymous, ed. Eugene O'Neill Jr., The Complete Greek Drama, Random
    # House 1938", and a 1938 compilation's editing cannot be assumed PD
    # without checking its renewal -- a rights line we could not read here.
    "aristophanes-clouds-hickie": ("canonical-greekLit",
        "tlg0019/tlg003/tlg0019.tlg003.perseus-eng2.xml",
        "Aristophanes, Clouds — W. J. Hickie 1853 (PD); urn ...tlg0019.tlg003.perseus-eng2"),
    # Greek historians in English prose (Adler vols. 5-6 and beyond),
    # 2026-10-02. Rights line read per file (titleStmt translator, and the
    # licence line where the file has one). All PD in the US (published
    # before 1931) AND in life+70 countries: Godley d. 1925, Crawley d. 1893,
    # Brownson d. 1948, Miller d. 1949. Perseus TEI is CC BY-SA (rights block).
    # Herodotus and Thucydides are SECOND witnesses here: the Adler shelf
    # has Macaulay and Jowett from Gutenberg without born-in sections.
    # Xenophon's Memorabilia/Oeconomicus (Marchant d. 1960) and Symposium/
    # Apology (Todd d. 1973) are NOT taken: PD in the US, not yet in the UK.
    "herodotus-histories-godley": ("canonical-greekLit",
        "tlg0016/tlg001/tlg0016.tlg001.perseus-eng2.xml",
        "Herodotus, Histories — A. D. Godley 1920-25 (PD); urn ...tlg0016.tlg001.perseus-eng2"),
    "thucydides-history-crawley": ("canonical-greekLit",
        "tlg0003/tlg001/tlg0003.tlg001.perseus-eng6.xml",
        "Thucydides, History of the Peloponnesian War — Richard Crawley (Dent 1914; PD); urn ...tlg0003.tlg001.perseus-eng6"),
    "xenophon-anabasis-brownson": ("canonical-greekLit",
        "tlg0032/tlg006/tlg0032.tlg006.perseus-eng2.xml",
        "Xenophon, Anabasis — C. L. Brownson 1921-22 (PD); urn ...tlg0032.tlg006.perseus-eng2"),
    "xenophon-hellenica-brownson": ("canonical-greekLit",
        "tlg0032/tlg001/tlg0032.tlg001.perseus-eng2.xml",
        "Xenophon, Hellenica — C. L. Brownson 1918-21 (PD); urn ...tlg0032.tlg001.perseus-eng2"),
    "xenophon-cyropaedia-miller": ("canonical-greekLit",
        "tlg0032/tlg007/tlg0032.tlg007.perseus-eng2.xml",
        "Xenophon, Cyropaedia — Walter Miller 1914 (PD); urn ...tlg0032.tlg007.perseus-eng2"),
    # Plutarch's Parallel Lives, all 66 pieces (the Lives and Plutarch's own
    # Comparisons), Adler vol. 13, 2026-10-02. Bernadotte Perrin's Loeb
    # (1914-1926); the rights line of every one names Perrin. PD in the US
    # (before 1931) and in life+70 countries (Perrin d. 1920). A second
    # witness beside the Adler shelf's Dryden/Clough, with born-in chapter.
    # section. NOT the Moralia: Babbitt's later volumes are 1931 and after.
    "plutarch-theseus-perrin": ("canonical-greekLit",
        "tlg0007/tlg001/tlg0007.tlg001.perseus-eng3.xml",
        "Plutarch, Theseus — B. Perrin 1914 (PD); urn ...tlg0007.tlg001.perseus-eng3"),
    "plutarch-romulus-perrin": ("canonical-greekLit",
        "tlg0007/tlg002/tlg0007.tlg002.perseus-eng2.xml",
        "Plutarch, Romulus — B. Perrin 1914 (PD); urn ...tlg0007.tlg002.perseus-eng2"),
    "plutarch-comparison-theseus-romulus-perrin": ("canonical-greekLit",
        "tlg0007/tlg003/tlg0007.tlg003.perseus-eng2.xml",
        "Plutarch, Comparison of Theseus and Romulus — B. Perrin 1914 (PD); urn ...tlg0007.tlg003.perseus-eng2"),
    "plutarch-lycurgus-perrin": ("canonical-greekLit",
        "tlg0007/tlg004/tlg0007.tlg004.perseus-eng2.xml",
        "Plutarch, Lycurgus — B. Perrin 1914 (PD); urn ...tlg0007.tlg004.perseus-eng2"),
    "plutarch-numa-perrin": ("canonical-greekLit",
        "tlg0007/tlg005/tlg0007.tlg005.perseus-eng2.xml",
        "Plutarch, Numa — B. Perrin 1914 (PD); urn ...tlg0007.tlg005.perseus-eng2"),
    "plutarch-comparison-lycurgus-numa-perrin": ("canonical-greekLit",
        "tlg0007/tlg006/tlg0007.tlg006.perseus-eng2.xml",
        "Plutarch, Comparison of Lycurgus and Numa — B. Perrin 1914 (PD); urn ...tlg0007.tlg006.perseus-eng2"),
    "plutarch-solon-perrin": ("canonical-greekLit",
        "tlg0007/tlg007/tlg0007.tlg007.perseus-eng2.xml",
        "Plutarch, Solon — B. Perrin 1914 (PD); urn ...tlg0007.tlg007.perseus-eng2"),
    "plutarch-publicola-perrin": ("canonical-greekLit",
        "tlg0007/tlg008/tlg0007.tlg008.perseus-eng2.xml",
        "Plutarch, Publicola — B. Perrin 1914 (PD); urn ...tlg0007.tlg008.perseus-eng2"),
    "plutarch-comparison-solon-publicola-perrin": ("canonical-greekLit",
        "tlg0007/tlg009/tlg0007.tlg009.perseus-eng2.xml",
        "Plutarch, Comparison of Solon and Publicola — B. Perrin 1914 (PD); urn ...tlg0007.tlg009.perseus-eng2"),
    "plutarch-themistocles-perrin": ("canonical-greekLit",
        "tlg0007/tlg010/tlg0007.tlg010.perseus-eng2.xml",
        "Plutarch, Themistocles — B. Perrin 1914 (PD); urn ...tlg0007.tlg010.perseus-eng2"),
    "plutarch-camillus-perrin": ("canonical-greekLit",
        "tlg0007/tlg011/tlg0007.tlg011.perseus-eng2.xml",
        "Plutarch, Camillus — B. Perrin 1914 (PD); urn ...tlg0007.tlg011.perseus-eng2"),
    "plutarch-pericles-perrin": ("canonical-greekLit",
        "tlg0007/tlg012/tlg0007.tlg012.perseus-eng2.xml",
        "Plutarch, Pericles — B. Perrin 1916 (PD); urn ...tlg0007.tlg012.perseus-eng2"),
    "plutarch-fabius-maximus-perrin": ("canonical-greekLit",
        "tlg0007/tlg013/tlg0007.tlg013.perseus-eng2.xml",
        "Plutarch, Fabius Maximus — B. Perrin 1914 (PD); urn ...tlg0007.tlg013.perseus-eng2"),
    "plutarch-comparison-pericles-fabius-maximus-perrin": ("canonical-greekLit",
        "tlg0007/tlg014/tlg0007.tlg014.perseus-eng2.xml",
        "Plutarch, Comparison of Pericles and Fabius Maximus — B. Perrin 1916 (PD); urn ...tlg0007.tlg014.perseus-eng2"),
    "plutarch-alcibiades-perrin": ("canonical-greekLit",
        "tlg0007/tlg015/tlg0007.tlg015.perseus-eng2.xml",
        "Plutarch, Alcibiades — B. Perrin 1916 (PD); urn ...tlg0007.tlg015.perseus-eng2"),
    "plutarch-caius-marcius-coriolanus-perrin": ("canonical-greekLit",
        "tlg0007/tlg016/tlg0007.tlg016.perseus-eng2.xml",
        "Plutarch, Caius Marcius Coriolanus — B. Perrin 1916 (PD); urn ...tlg0007.tlg016.perseus-eng2"),
    "plutarch-comparison-alcibiades-coriolanus-perrin": ("canonical-greekLit",
        "tlg0007/tlg017/tlg0007.tlg017.perseus-eng2.xml",
        "Plutarch, Comparison of Alcibiades and Coriolanus — B. Perrin 1916 (PD); urn ...tlg0007.tlg017.perseus-eng2"),
    "plutarch-timoleon-perrin": ("canonical-greekLit",
        "tlg0007/tlg018/tlg0007.tlg018.perseus-eng2.xml",
        "Plutarch, Timoleon — B. Perrin 1918 (PD); urn ...tlg0007.tlg018.perseus-eng2"),
    "plutarch-aemilius-paulus-perrin": ("canonical-greekLit",
        "tlg0007/tlg019/tlg0007.tlg019.perseus-eng2.xml",
        "Plutarch, Aemilius Paulus — B. Perrin 1918 (PD); urn ...tlg0007.tlg019.perseus-eng2"),
    "plutarch-comparison-timoleon-aemilius-perrin": ("canonical-greekLit",
        "tlg0007/tlg020/tlg0007.tlg020.perseus-eng2.xml",
        "Plutarch, Comparison of Timoleon and Aemilius — B. Perrin 1918 (PD); urn ...tlg0007.tlg020.perseus-eng2"),
    "plutarch-pelopidas-perrin": ("canonical-greekLit",
        "tlg0007/tlg021/tlg0007.tlg021.perseus-eng2.xml",
        "Plutarch, Pelopidas — B. Perrin 1917 (PD); urn ...tlg0007.tlg021.perseus-eng2"),
    "plutarch-marcellus-perrin": ("canonical-greekLit",
        "tlg0007/tlg022/tlg0007.tlg022.perseus-eng2.xml",
        "Plutarch, Marcellus — B. Perrin 1917 (PD); urn ...tlg0007.tlg022.perseus-eng2"),
    "plutarch-comparison-pelopidas-marcellus-perrin": ("canonical-greekLit",
        "tlg0007/tlg023/tlg0007.tlg023.perseus-eng2.xml",
        "Plutarch, Comparison of Pelopidas and Marcellus — B. Perrin 1917 (PD); urn ...tlg0007.tlg023.perseus-eng2"),
    "plutarch-aristides-perrin": ("canonical-greekLit",
        "tlg0007/tlg024/tlg0007.tlg024.perseus-eng2.xml",
        "Plutarch, Aristides — B. Perrin 1914 (PD); urn ...tlg0007.tlg024.perseus-eng2"),
    "plutarch-marcus-cato-perrin": ("canonical-greekLit",
        "tlg0007/tlg025/tlg0007.tlg025.perseus-eng2.xml",
        "Plutarch, Marcus Cato — B. Perrin 1914 (PD); urn ...tlg0007.tlg025.perseus-eng2"),
    "plutarch-comparison-aristides-marcus-cato-perrin": ("canonical-greekLit",
        "tlg0007/tlg026/tlg0007.tlg026.perseus-eng2.xml",
        "Plutarch, Comparison of Aristides and Marcus Cato — B. Perrin 1914 (PD); urn ...tlg0007.tlg026.perseus-eng2"),
    "plutarch-philopoemen-perrin": ("canonical-greekLit",
        "tlg0007/tlg027/tlg0007.tlg027.perseus-eng2.xml",
        "Plutarch, Philopoemen — B. Perrin 1921 (PD); urn ...tlg0007.tlg027.perseus-eng2"),
    "plutarch-titus-flamininus-perrin": ("canonical-greekLit",
        "tlg0007/tlg028/tlg0007.tlg028.perseus-eng2.xml",
        "Plutarch, Titus Flamininus — B. Perrin 1921 (PD); urn ...tlg0007.tlg028.perseus-eng2"),
    "plutarch-comparison-philopoemen-titus-perrin": ("canonical-greekLit",
        "tlg0007/tlg029/tlg0007.tlg029.perseus-eng2.xml",
        "Plutarch, Comparison of Philopoemen and Titus — B. Perrin 1921 (PD); urn ...tlg0007.tlg029.perseus-eng2"),
    "plutarch-pyrrhus-perrin": ("canonical-greekLit",
        "tlg0007/tlg030/tlg0007.tlg030.perseus-eng2.xml",
        "Plutarch, Pyrrhus — B. Perrin 1920 (PD); urn ...tlg0007.tlg030.perseus-eng2"),
    "plutarch-caius-marius-perrin": ("canonical-greekLit",
        "tlg0007/tlg031/tlg0007.tlg031.perseus-eng2.xml",
        "Plutarch, Caius Marius — B. Perrin 1920 (PD); urn ...tlg0007.tlg031.perseus-eng2"),
    "plutarch-lysander-perrin": ("canonical-greekLit",
        "tlg0007/tlg032/tlg0007.tlg032.perseus-eng2.xml",
        "Plutarch, Lysander — B. Perrin 1916 (PD); urn ...tlg0007.tlg032.perseus-eng2"),
    "plutarch-sulla-perrin": ("canonical-greekLit",
        "tlg0007/tlg033/tlg0007.tlg033.perseus-eng2.xml",
        "Plutarch, Sulla — B. Perrin 1916 (PD); urn ...tlg0007.tlg033.perseus-eng2"),
    "plutarch-comparison-lysander-sulla-perrin": ("canonical-greekLit",
        "tlg0007/tlg034/tlg0007.tlg034.perseus-eng2.xml",
        "Plutarch, Comparison of Lysander and Sulla — B. Perrin 1916 (PD); urn ...tlg0007.tlg034.perseus-eng2"),
    "plutarch-cimon-perrin": ("canonical-greekLit",
        "tlg0007/tlg035/tlg0007.tlg035.perseus-eng2.xml",
        "Plutarch, Cimon — B. Perrin 1914 (PD); urn ...tlg0007.tlg035.perseus-eng2"),
    "plutarch-lucullus-perrin": ("canonical-greekLit",
        "tlg0007/tlg036/tlg0007.tlg036.perseus-eng2.xml",
        "Plutarch, Lucullus — B. Perrin 1914 (PD); urn ...tlg0007.tlg036.perseus-eng2"),
    "plutarch-comparison-lucullus-cimon-perrin": ("canonical-greekLit",
        "tlg0007/tlg037/tlg0007.tlg037.perseus-eng2.xml",
        "Plutarch, Comparison of Lucullus and Cimon — B. Perrin 1914 (PD); urn ...tlg0007.tlg037.perseus-eng2"),
    "plutarch-nicias-perrin": ("canonical-greekLit",
        "tlg0007/tlg038/tlg0007.tlg038.perseus-eng2.xml",
        "Plutarch, Nicias — B. Perrin 1914 (PD); urn ...tlg0007.tlg038.perseus-eng2"),
    "plutarch-crassus-perrin": ("canonical-greekLit",
        "tlg0007/tlg039/tlg0007.tlg039.perseus-eng2.xml",
        "Plutarch, Crassus — B. Perrin 1914 (PD); urn ...tlg0007.tlg039.perseus-eng2"),
    "plutarch-comparison-nicias-crassus-perrin": ("canonical-greekLit",
        "tlg0007/tlg040/tlg0007.tlg040.perseus-eng2.xml",
        "Plutarch, Comparison of Nicias and Crassus — B. Perrin 1914 (PD); urn ...tlg0007.tlg040.perseus-eng2"),
    "plutarch-eumenes-perrin": ("canonical-greekLit",
        "tlg0007/tlg041/tlg0007.tlg041.perseus-eng2.xml",
        "Plutarch, Eumenes — B. Perrin 1919 (PD); urn ...tlg0007.tlg041.perseus-eng2"),
    "plutarch-sertorius-perrin": ("canonical-greekLit",
        "tlg0007/tlg042/tlg0007.tlg042.perseus-eng2.xml",
        "Plutarch, Sertorius — B. Perrin 1919 (PD); urn ...tlg0007.tlg042.perseus-eng2"),
    "plutarch-comparison-sertorius-eumenes-perrin": ("canonical-greekLit",
        "tlg0007/tlg043/tlg0007.tlg043.perseus-eng2.xml",
        "Plutarch, Comparison of Sertorius and Eumenes — B. Perrin 1919 (PD); urn ...tlg0007.tlg043.perseus-eng2"),
    "plutarch-agesilaus-perrin": ("canonical-greekLit",
        "tlg0007/tlg044/tlg0007.tlg044.perseus-eng2.xml",
        "Plutarch, Agesilaus — B. Perrin 1917 (PD); urn ...tlg0007.tlg044.perseus-eng2"),
    "plutarch-pompey-perrin": ("canonical-greekLit",
        "tlg0007/tlg045/tlg0007.tlg045.perseus-eng2.xml",
        "Plutarch, Pompey — B. Perrin 1917 (PD); urn ...tlg0007.tlg045.perseus-eng2"),
    "plutarch-comparison-agesilaus-pompey-perrin": ("canonical-greekLit",
        "tlg0007/tlg046/tlg0007.tlg046.perseus-eng2.xml",
        "Plutarch, Comparison of Agesilaus and Pompey — B. Perrin 1917 (PD); urn ...tlg0007.tlg046.perseus-eng2"),
    "plutarch-alexander-perrin": ("canonical-greekLit",
        "tlg0007/tlg047/tlg0007.tlg047.perseus-eng2.xml",
        "Plutarch, Alexander — B. Perrin 1919 (PD); urn ...tlg0007.tlg047.perseus-eng2"),
    "plutarch-caesar-perrin": ("canonical-greekLit",
        "tlg0007/tlg048/tlg0007.tlg048.perseus-eng2.xml",
        "Plutarch, Caesar — B. Perrin 1919 (PD); urn ...tlg0007.tlg048.perseus-eng2"),
    "plutarch-phocion-perrin": ("canonical-greekLit",
        "tlg0007/tlg049/tlg0007.tlg049.perseus-eng2.xml",
        "Plutarch, Phocion — B. Perrin 1919 (PD); urn ...tlg0007.tlg049.perseus-eng2"),
    "plutarch-cato-the-younger-perrin": ("canonical-greekLit",
        "tlg0007/tlg050/tlg0007.tlg050.perseus-eng2.xml",
        "Plutarch, Cato the Younger — B. Perrin 1919 (PD); urn ...tlg0007.tlg050.perseus-eng2"),
    "plutarch-agis-cleomenes-perrin": ("canonical-greekLit",
        "tlg0007/tlg051/tlg0007.tlg051.perseus-eng1.xml",
        "Plutarch, Agis and Cleomenes — B. Perrin 1921 (PD); urn ...tlg0007.tlg051.perseus-eng1"),
    "plutarch-tiberius-caius-gracchus-perrin": ("canonical-greekLit",
        "tlg0007/tlg052/tlg0007.tlg052.perseus-eng1.xml",
        "Plutarch, Tiberius and Caius Gracchus — B. Perrin 1921 (PD); urn ...tlg0007.tlg052.perseus-eng1"),
    "plutarch-comparison-agis-cleomenes-the-gracchi-perrin": ("canonical-greekLit",
        "tlg0007/tlg053/tlg0007.tlg053.perseus-eng2.xml",
        "Plutarch, Comparison of Agis and Cleomenes and the Gracchi — B. Perrin 1921 (PD); urn ...tlg0007.tlg053.perseus-eng2"),
    "plutarch-demosthenes-perrin": ("canonical-greekLit",
        "tlg0007/tlg054/tlg0007.tlg054.perseus-eng2.xml",
        "Plutarch, Demosthenes — B. Perrin 1919 (PD); urn ...tlg0007.tlg054.perseus-eng2"),
    "plutarch-cicero-perrin": ("canonical-greekLit",
        "tlg0007/tlg055/tlg0007.tlg055.perseus-eng2.xml",
        "Plutarch, Cicero — B. Perrin 1919 (PD); urn ...tlg0007.tlg055.perseus-eng2"),
    "plutarch-comparison-demosthenes-cicero-perrin": ("canonical-greekLit",
        "tlg0007/tlg056/tlg0007.tlg056.perseus-eng2.xml",
        "Plutarch, Comparison of Demosthenes and Cicero — B. Perrin 1919 (PD); urn ...tlg0007.tlg056.perseus-eng2"),
    "plutarch-demetrius-perrin": ("canonical-greekLit",
        "tlg0007/tlg057/tlg0007.tlg057.perseus-eng2.xml",
        "Plutarch, Demetrius — B. Perrin 1920 (PD); urn ...tlg0007.tlg057.perseus-eng2"),
    "plutarch-antony-perrin": ("canonical-greekLit",
        "tlg0007/tlg058/tlg0007.tlg058.perseus-eng2.xml",
        "Plutarch, Antony — B. Perrin 1920 (PD); urn ...tlg0007.tlg058.perseus-eng2"),
    "plutarch-comparison-demetrius-antony-perrin": ("canonical-greekLit",
        "tlg0007/tlg059/tlg0007.tlg059.perseus-eng2.xml",
        "Plutarch, Comparison of Demetrius and Antony — B. Perrin 1920 (PD); urn ...tlg0007.tlg059.perseus-eng2"),
    "plutarch-dion-perrin": ("canonical-greekLit",
        "tlg0007/tlg060/tlg0007.tlg060.perseus-eng2.xml",
        "Plutarch, Dion — B. Perrin 1918 (PD); urn ...tlg0007.tlg060.perseus-eng2"),
    "plutarch-brutus-perrin": ("canonical-greekLit",
        "tlg0007/tlg061/tlg0007.tlg061.perseus-eng2.xml",
        "Plutarch, Brutus — B. Perrin 1918 (PD); urn ...tlg0007.tlg061.perseus-eng2"),
    "plutarch-comparison-dion-brutus-perrin": ("canonical-greekLit",
        "tlg0007/tlg062/tlg0007.tlg062.perseus-eng2.xml",
        "Plutarch, Comparison of Dion and Brutus — B. Perrin 1918 (PD); urn ...tlg0007.tlg062.perseus-eng2"),
    "plutarch-aratus-perrin": ("canonical-greekLit",
        "tlg0007/tlg063/tlg0007.tlg063.perseus-eng2.xml",
        "Plutarch, Aratus — B. Perrin 1926 (PD); urn ...tlg0007.tlg063.perseus-eng2"),
    "plutarch-artaxerxes-perrin": ("canonical-greekLit",
        "tlg0007/tlg064/tlg0007.tlg064.perseus-eng2.xml",
        "Plutarch, Artaxerxes — B. Perrin 1926 (PD); urn ...tlg0007.tlg064.perseus-eng2"),
    "plutarch-galba-perrin": ("canonical-greekLit",
        "tlg0007/tlg065/tlg0007.tlg065.perseus-eng2.xml",
        "Plutarch, Galba — B. Perrin 1926 (PD); urn ...tlg0007.tlg065.perseus-eng2"),
    "plutarch-otho-perrin": ("canonical-greekLit",
        "tlg0007/tlg066/tlg0007.tlg066.perseus-eng2.xml",
        "Plutarch, Otho — B. Perrin 1926 (PD); urn ...tlg0007.tlg066.perseus-eng2"),
    # More Greek historians and a geographer, 2026-10-02. Rights line read
    # per file; all PD everywhere, long dead translators: Shuckburgh (1889,
    # d. 1906), Whiston (1737; this printing 1856, d. 1752), Hamilton &
    # Falconer (Bohn 1854-57). Strabo is eng4, the complete Bohn version;
    # eng3 (H. L. Jones, Loeb) covers only books 6-14. NOT taken: Pausanias
    # (W. H. S. Jones d. 1963, not yet PD in the UK).
    "polybius-histories-shuckburgh": ("canonical-greekLit",
        "tlg0543/tlg001/tlg0543.tlg001.perseus-eng2.xml",
        "Polybius, Histories — E. S. Shuckburgh 1889 (PD); urn ...tlg0543.tlg001.perseus-eng2"),
    "josephus-antiquities-whiston": ("canonical-greekLit",
        "tlg0526/tlg001/tlg0526.tlg001.perseus-eng2.xml",
        "Josephus, Jewish Antiquities — William Whiston (PD); urn ...tlg0526.tlg001.perseus-eng2"),
    "josephus-life-whiston": ("canonical-greekLit",
        "tlg0526/tlg002/tlg0526.tlg002.perseus-eng2.xml",
        "Josephus, Life — William Whiston (PD); urn ...tlg0526.tlg002.perseus-eng2"),
    "josephus-against-apion-whiston": ("canonical-greekLit",
        "tlg0526/tlg003/tlg0526.tlg003.perseus-eng2.xml",
        "Josephus, Against Apion — William Whiston (PD); urn ...tlg0526.tlg003.perseus-eng2"),
    "josephus-jewish-war-whiston": ("canonical-greekLit",
        "tlg0526/tlg004/tlg0526.tlg004.perseus-eng2.xml",
        "Josephus, The Jewish War — William Whiston (PD); urn ...tlg0526.tlg004.perseus-eng2"),
    "strabo-geography-hamilton": ("canonical-greekLit",
        "tlg0099/tlg001/tlg0099.tlg001.perseus-eng4.xml",
        "Strabo, Geography — H. C. Hamilton & W. Falconer 1854-57 (PD); urn ...tlg0099.tlg001.perseus-eng4"),
    # Mythography, philosophers' lives, Stoics, an orator. 2026-10-02.
    # Rights line read per file. PD in the US and in life+70 countries:
    # Frazer (1921, d. 1941), Hicks (1925, d. 1929), Higginson (1890,
    # d. 1911), C. D. Adams (1919, d. 1938; Perseus keyed it from the 1958
    # reprint of the 1919 Loeb, which adds no new translation).
    "apollodorus-library-frazer": ("canonical-greekLit",
        "tlg0548/tlg001/tlg0548.tlg001.perseus-eng2.xml",
        "Apollodorus, Library — J. G. Frazer 1921 (PD); urn ...tlg0548.tlg001.perseus-eng2"),
    "apollodorus-epitome-frazer": ("canonical-greekLit",
        "tlg0548/tlg002/tlg0548.tlg002.perseus-eng2.xml",
        "Apollodorus, Epitome — J. G. Frazer 1921 (PD); urn ...tlg0548.tlg002.perseus-eng2"),
    "diogenes-laertius-lives-hicks": ("canonical-greekLit",
        "tlg0004/tlg001/tlg0004.tlg001.perseus-eng2.xml",
        "Diogenes Laertius, Lives of Eminent Philosophers — R. D. Hicks 1925 (PD); urn ...tlg0004.tlg001.perseus-eng2"),
    "epictetus-discourses-higginson": ("canonical-greekLit",
        "tlg0557/tlg001/tlg0557.tlg001.perseus-eng4.xml",
        "Epictetus, Discourses — T. W. Higginson 1890 (PD); urn ...tlg0557.tlg001.perseus-eng4"),
    "epictetus-handbook-higginson": ("canonical-greekLit",
        "tlg0557/tlg002/tlg0557.tlg002.perseus-eng4.xml",
        "Epictetus, Handbook (Enchiridion) — T. W. Higginson 1890 (PD); urn ...tlg0557.tlg002.perseus-eng4"),
    "aeschines-timarchus-adams": ("canonical-greekLit",
        "tlg0026/tlg001/tlg0026.tlg001.perseus-eng2.xml",
        "Aeschines, Against Timarchus — C. D. Adams 1919 (PD); urn ...tlg0026.tlg001.perseus-eng2"),
    "aeschines-embassy-adams": ("canonical-greekLit",
        "tlg0026/tlg002/tlg0026.tlg002.perseus-eng2.xml",
        "Aeschines, On the Embassy — C. D. Adams 1919 (PD); urn ...tlg0026.tlg002.perseus-eng2"),
    "aeschines-ctesiphon-adams": ("canonical-greekLit",
        "tlg0026/tlg003/tlg0026.tlg003.perseus-eng2.xml",
        "Aeschines, Against Ctesiphon — C. D. Adams 1919 (PD); urn ...tlg0026.tlg003.perseus-eng2"),
    # Latin prose, from canonical-latinLit. Every translator died before 1955
    # and every edition predates 1931: McDevitte & Bohn (Bohn 1869), Peskett
    # (1914, d. 1924), Church (d. 1912) & Brodribb (d. 1905) 1864-77,
    # Thomson (d. 1803) revised by J. E. Reed (1883: an adult reviser of 1883
    # would have had to live past ninety to still be in copyright anywhere).
    # Perseus keyed Tacitus from the Modern Library's 1942 reprint of
    # Church & Brodribb: the translation is the PD one; the reprint's
    # marginal headings may be its own, and are kept apart (see the rights
    # note on each Tacitus book).
    "caesar-gallic-war-mcdevitte": ("canonical-latinLit",
        "phi0448/phi001/phi0448.phi001.perseus-eng2.xml",
        "Caesar, Gallic War — W. A. McDevitte & W. S. Bohn 1869 (PD); urn ...phi0448.phi001.perseus-eng2"),
    "caesar-civil-war-peskett": ("canonical-latinLit",
        "phi0448/phi002/phi0448.phi002.perseus-eng2.xml",
        "Caesar, Civil War — A. G. Peskett 1914 (PD); urn ...phi0448.phi002.perseus-eng2"),
    "tacitus-agricola-church": ("canonical-latinLit",
        "phi1351/phi001/phi1351.phi001.perseus-eng2.xml",
        "Tacitus, Agricola — A. J. Church & W. J. Brodribb 1868 (PD); urn ...phi1351.phi001.perseus-eng2"),
    "tacitus-germania-church": ("canonical-latinLit",
        "phi1351/phi002/phi1351.phi002.perseus-eng1.xml",
        "Tacitus, Germania — A. J. Church & W. J. Brodribb 1868 (PD); urn ...phi1351.phi002.perseus-eng1"),
    "tacitus-dialogus-church": ("canonical-latinLit",
        "phi1351/phi003/phi1351.phi003.perseus-eng1.xml",
        "Tacitus, Dialogue on Oratory — A. J. Church & W. J. Brodribb 1877 (PD); urn ...phi1351.phi003.perseus-eng1"),
    "tacitus-histories-church": ("canonical-latinLit",
        "phi1351/phi004/phi1351.phi004.perseus-eng1.xml",
        "Tacitus, Histories — A. J. Church & W. J. Brodribb 1864 (PD); urn ...phi1351.phi004.perseus-eng1"),
    "tacitus-annals-church": ("canonical-latinLit",
        "phi1351/phi005/phi1351.phi005.perseus-eng1.xml",
        "Tacitus, Annals — A. J. Church & W. J. Brodribb 1869 (PD); urn ...phi1351.phi005.perseus-eng1"),
    "suetonius-julius-thomson": ("canonical-latinLit",
        "phi1348/abo011/phi1348.abo011.perseus-eng2.xml",
        "Suetonius, Julius — Alexander Thomson, rev. J. E. Reed 1883 (PD); urn ...phi1348.abo011.perseus-eng2"),
    "suetonius-augustus-thomson": ("canonical-latinLit",
        "phi1348/abo012/phi1348.abo012.perseus-eng2.xml",
        "Suetonius, Augustus — Alexander Thomson, rev. J. E. Reed 1883 (PD); urn ...phi1348.abo012.perseus-eng2"),
    "suetonius-tiberius-thomson": ("canonical-latinLit",
        "phi1348/abo013/phi1348.abo013.perseus-eng2.xml",
        "Suetonius, Tiberius — Alexander Thomson, rev. J. E. Reed 1883 (PD); urn ...phi1348.abo013.perseus-eng2"),
    "suetonius-caligula-thomson": ("canonical-latinLit",
        "phi1348/abo014/phi1348.abo014.perseus-eng2.xml",
        "Suetonius, Caligula — Alexander Thomson, rev. J. E. Reed 1883 (PD); urn ...phi1348.abo014.perseus-eng2"),
    "suetonius-claudius-thomson": ("canonical-latinLit",
        "phi1348/abo015/phi1348.abo015.perseus-eng2.xml",
        "Suetonius, Claudius — Alexander Thomson, rev. J. E. Reed 1883 (PD); urn ...phi1348.abo015.perseus-eng2"),
    "suetonius-nero-thomson": ("canonical-latinLit",
        "phi1348/abo016/phi1348.abo016.perseus-eng2.xml",
        "Suetonius, Nero — Alexander Thomson, rev. J. E. Reed 1883 (PD); urn ...phi1348.abo016.perseus-eng2"),
    "suetonius-galba-thomson": ("canonical-latinLit",
        "phi1348/abo017/phi1348.abo017.perseus-eng2.xml",
        "Suetonius, Galba — Alexander Thomson, rev. J. E. Reed 1883 (PD); urn ...phi1348.abo017.perseus-eng2"),
    "suetonius-otho-thomson": ("canonical-latinLit",
        "phi1348/abo018/phi1348.abo018.perseus-eng2.xml",
        "Suetonius, Otho — Alexander Thomson, rev. J. E. Reed 1883 (PD); urn ...phi1348.abo018.perseus-eng2"),
    "suetonius-vitellius-thomson": ("canonical-latinLit",
        "phi1348/abo019/phi1348.abo019.perseus-eng2.xml",
        "Suetonius, Vitellius — Alexander Thomson, rev. J. E. Reed 1883 (PD); urn ...phi1348.abo019.perseus-eng2"),
    "suetonius-vespasian-thomson": ("canonical-latinLit",
        "phi1348/abo020/phi1348.abo020.perseus-eng2.xml",
        "Suetonius, Vespasian — Alexander Thomson, rev. J. E. Reed 1883 (PD); urn ...phi1348.abo020.perseus-eng2"),
    "suetonius-titus-thomson": ("canonical-latinLit",
        "phi1348/abo021/phi1348.abo021.perseus-eng2.xml",
        "Suetonius, Titus — Alexander Thomson, rev. J. E. Reed 1883 (PD); urn ...phi1348.abo021.perseus-eng2"),
    "suetonius-domitian-thomson": ("canonical-latinLit",
        "phi1348/abo022/phi1348.abo022.perseus-eng2.xml",
        "Suetonius, Domitian — Alexander Thomson, rev. J. E. Reed 1883 (PD); urn ...phi1348.abo022.perseus-eng2"),
    # Cicero, Sallust, Vitruvius, Quintilian, Seneca. Translators all died
    # before 1955, editions all before 1931: Yonge (d. 1891), Falconer
    # (d. 1927), Walter Miller (d. 1949), J. S. Watson (d. 1884), Morgan
    # (d. 1910), H. E. Butler (d. 1951), Rouse (d. 1950).
    "cicero-quinctius-yonge": ("canonical-latinLit",
        "phi0474/phi001/phi0474.phi001.perseus-eng2.xml",
        "Cicero, For Publius Quinctius — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi001.perseus-eng2"),
    "cicero-roscius-amerinus-yonge": ("canonical-latinLit",
        "phi0474/phi002/phi0474.phi002.perseus-eng2.xml",
        "Cicero, For Sextus Roscius of Ameria — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi002.perseus-eng2"),
    "cicero-roscius-comoedus-yonge": ("canonical-latinLit",
        "phi0474/phi003/phi0474.phi003.perseus-eng2.xml",
        "Cicero, For Quintus Roscius the Actor — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi003.perseus-eng2"),
    "cicero-divinatio-caecilium-yonge": ("canonical-latinLit",
        "phi0474/phi004/phi0474.phi004.perseus-eng2.xml",
        "Cicero, Against Quintus Caecilius — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi004.perseus-eng2"),
    "cicero-verrines-yonge": ("canonical-latinLit",
        "phi0474/phi005/phi0474.phi005.perseus-eng2.xml",
        "Cicero, Against Verres — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi005.perseus-eng2"),
    "cicero-tullius-yonge": ("canonical-latinLit",
        "phi0474/phi006/phi0474.phi006.perseus-eng2.xml",
        "Cicero, For Marcus Tullius — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi006.perseus-eng2"),
    "cicero-fonteius-yonge": ("canonical-latinLit",
        "phi0474/phi007/phi0474.phi007.perseus-eng2.xml",
        "Cicero, For Marcus Fonteius — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi007.perseus-eng2"),
    "cicero-caecina-yonge": ("canonical-latinLit",
        "phi0474/phi008/phi0474.phi008.perseus-eng2.xml",
        "Cicero, For Aulus Caecina — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi008.perseus-eng2"),
    "cicero-manilian-law-yonge": ("canonical-latinLit",
        "phi0474/phi009/phi0474.phi009.perseus-eng2.xml",
        "Cicero, On the Manilian Law — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi009.perseus-eng2"),
    "cicero-cluentius-yonge": ("canonical-latinLit",
        "phi0474/phi010/phi0474.phi010.perseus-eng2.xml",
        "Cicero, For Aulus Cluentius — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi010.perseus-eng2"),
    "cicero-agrarian-law-yonge": ("canonical-latinLit",
        "phi0474/phi011/phi0474.phi011.perseus-eng2.xml",
        "Cicero, On the Agrarian Law — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi011.perseus-eng2"),
    "cicero-rabirius-yonge": ("canonical-latinLit",
        "phi0474/phi012/phi0474.phi012.perseus-eng3.xml",
        "Cicero, For Gaius Rabirius — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi012.perseus-eng3"),
    "cicero-catiline-yonge": ("canonical-latinLit",
        "phi0474/phi013/phi0474.phi013.perseus-eng2.xml",
        "Cicero, Against Catiline — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi013.perseus-eng2"),
    "cicero-murena-yonge": ("canonical-latinLit",
        "phi0474/phi014/phi0474.phi014.perseus-eng2.xml",
        "Cicero, For Lucius Murena — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi014.perseus-eng2"),
    "cicero-sulla-yonge": ("canonical-latinLit",
        "phi0474/phi015/phi0474.phi015.perseus-eng2.xml",
        "Cicero, For Publius Sulla — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi015.perseus-eng2"),
    "cicero-archias-yonge": ("canonical-latinLit",
        "phi0474/phi016/phi0474.phi016.perseus-eng2.xml",
        "Cicero, For Archias — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi016.perseus-eng2"),
    "cicero-flaccus-yonge": ("canonical-latinLit",
        "phi0474/phi017/phi0474.phi017.perseus-eng2.xml",
        "Cicero, For Lucius Flaccus — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi017.perseus-eng2"),
    "cicero-post-reditum-quirites-yonge": ("canonical-latinLit",
        "phi0474/phi018/phi0474.phi018.perseus-eng2.xml",
        "Cicero, To the Citizens after his Return — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi018.perseus-eng2"),
    "cicero-post-reditum-senatu-yonge": ("canonical-latinLit",
        "phi0474/phi019/phi0474.phi019.perseus-eng2.xml",
        "Cicero, In the Senate after his Return — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi019.perseus-eng2"),
    "cicero-philippics-yonge": ("canonical-latinLit",
        "phi0474/phi035/phi0474.phi035.perseus-eng1.xml",
        "Cicero, Philippics — C. D. Yonge (Bohn, 1856; d. 1891) (PD); urn ...phi0474.phi035.perseus-eng1"),
    "cicero-de-senectute-falconer": ("canonical-latinLit",
        "phi0474/phi051/phi0474.phi051.perseus-eng1.xml",
        "Cicero, On Old Age — W. A. Falconer (Loeb, 1923; d. 1927) (PD); urn ...phi0474.phi051.perseus-eng1"),
    "cicero-de-amicitia-falconer": ("canonical-latinLit",
        "phi0474/phi052/phi0474.phi052.perseus-eng2.xml",
        "Cicero, On Friendship — W. A. Falconer (Loeb, 1923; d. 1927) (PD); urn ...phi0474.phi052.perseus-eng2"),
    "cicero-de-divinatione-falconer": ("canonical-latinLit",
        "phi0474/phi053/phi0474.phi053.perseus-eng1.xml",
        "Cicero, On Divination — W. A. Falconer (Loeb, 1923; d. 1927) (PD); urn ...phi0474.phi053.perseus-eng1"),
    "cicero-de-officiis-miller": ("canonical-latinLit",
        "phi0474/phi055/phi0474.phi055.perseus-eng1.xml",
        "Cicero, On Duties — Walter Miller (Loeb, 1913; d. 1949) (PD); urn ...phi0474.phi055.perseus-eng1"),
    "sallust-catiline-watson": ("canonical-latinLit",
        "phi0631/phi001/phi0631.phi001.perseus-eng2.xml",
        "Sallust, Conspiracy of Catiline — J. S. Watson (1899 printing; d. 1884) (PD); urn ...phi0631.phi001.perseus-eng2"),
    "sallust-jugurthine-war-watson": ("canonical-latinLit",
        "phi0631/phi002/phi0631.phi002.perseus-eng2.xml",
        "Sallust, The Jugurthine War — J. S. Watson (1899 printing; d. 1884) (PD); urn ...phi0631.phi002.perseus-eng2"),
    "vitruvius-architecture-morgan": ("canonical-latinLit",
        "phi1056/phi001/phi1056.phi001.perseus-eng2.xml",
        "Vitruvius, The Ten Books on Architecture — M. H. Morgan (1914; d. 1910) (PD); urn ...phi1056.phi001.perseus-eng2"),
    "quintilian-institutio-butler": ("canonical-latinLit",
        "phi1002/phi001/phi1002.phi001.perseus-eng2.xml",
        "Quintilian, Institutio Oratoria — H. E. Butler (Loeb, 1920-22; d. 1951) (PD); urn ...phi1002.phi001.perseus-eng2"),
    "seneca-apocolocyntosis-rouse": ("canonical-latinLit",
        "phi1017/phi011/phi1017.phi011.perseus-eng2.xml",
        "Seneca, Apocolocyntosis — W. H. D. Rouse (Loeb, 1913; d. 1950) (PD); urn ...phi1017.phi011.perseus-eng2"),
    # Cicero's letters in Shuckburgh's chronological translation (Bell,
    # 1899-1900; E. S. Shuckburgh d. 1906). Perseus splits his one series
    # into four files; see TEI_LETTERS in structure_texts.py.
    "cicero-letters-friends-shuckburgh": ("canonical-latinLit",
        "phi0474/phi056/phi0474.phi056.perseus-eng1.xml",
        "Cicero, Letters to his Friends — E. S. Shuckburgh 1899-1900 (PD); urn ...phi0474.phi056.perseus-eng1"),
    "cicero-letters-atticus-shuckburgh": ("canonical-latinLit",
        "phi0474/phi057/phi0474.phi057.perseus-eng1.xml",
        "Cicero, Letters to Atticus — E. S. Shuckburgh 1899-1900 (PD); urn ...phi0474.phi057.perseus-eng1"),
    "cicero-letters-quintus-shuckburgh": ("canonical-latinLit",
        "phi0474/phi058/phi0474.phi058.perseus-eng1.xml",
        "Cicero, Letters to his brother Quintus — E. S. Shuckburgh 1899-1900 (PD); urn ...phi0474.phi058.perseus-eng1"),
    "cicero-letters-brutus-shuckburgh": ("canonical-latinLit",
        "phi0474/phi059/phi0474.phi059.perseus-eng1.xml",
        "Cicero, Letters to Brutus — E. S. Shuckburgh 1899-1900 (PD); urn ...phi0474.phi059.perseus-eng1"),
    # Lucian in the Fowlers' translation (Clarendon, 1905; H. W. Fowler
    # d. 1933, F. G. Fowler d. 1918): all 63 pieces Perseus has in it. Not
    # taken: Harmon's Loeb volumes after 1930, Kilburn (1959), MacLeod (1961).
    "lucian-phalaris-fowler": ("canonical-greekLit",
        "tlg0062/tlg001/tlg0062.tlg001.perseus-eng4.xml",
        "Lucian, Phalaris, I — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg001.perseus-eng4"),
    "lucian-bacchus-fowler": ("canonical-greekLit",
        "tlg0062/tlg003/tlg0062.tlg003.perseus-eng4.xml",
        "Lucian, Dionysus, an Introductory Lecture — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg003.perseus-eng4"),
    "lucian-hercules-fowler": ("canonical-greekLit",
        "tlg0062/tlg004/tlg0062.tlg004.perseus-eng4.xml",
        "Lucian, Heracles, an Introductory Lecture — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg004.perseus-eng4"),
    "lucian-electrum-fowler": ("canonical-greekLit",
        "tlg0062/tlg005/tlg0062.tlg005.perseus-eng4.xml",
        "Lucian, Swans and Amber — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg005.perseus-eng4"),
    "lucian-muscae-encomium-fowler": ("canonical-greekLit",
        "tlg0062/tlg006/tlg0062.tlg006.perseus-eng4.xml",
        "Lucian, The Fly, an Appreciation — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg006.perseus-eng4"),
    "lucian-nigrinus-fowler": ("canonical-greekLit",
        "tlg0062/tlg007/tlg0062.tlg007.perseus-eng4.xml",
        "Lucian, Nigrinus — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg007.perseus-eng4"),
    "lucian-demonax-fowler": ("canonical-greekLit",
        "tlg0062/tlg008/tlg0062.tlg008.perseus-eng4.xml",
        "Lucian, Life of Demonax — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg008.perseus-eng4"),
    "lucian-de-domo-fowler": ("canonical-greekLit",
        "tlg0062/tlg009/tlg0062.tlg009.perseus-eng4.xml",
        "Lucian, The Hall — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg009.perseus-eng4"),
    "lucian-patriae-encomium-fowler": ("canonical-greekLit",
        "tlg0062/tlg010/tlg0062.tlg010.perseus-eng4.xml",
        "Lucian, Patriotism — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg010.perseus-eng4"),
    "lucian-verae-historiae-fowler": ("canonical-greekLit",
        "tlg0062/tlg012/tlg0062.tlg012.perseus-eng4.xml",
        "Lucian, The True History — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg012.perseus-eng4"),
    "lucian-calumniae-non-temere-credundum-fowler": ("canonical-greekLit",
        "tlg0062/tlg013/tlg0062.tlg013.perseus-eng4.xml",
        "Lucian, Slander, a Warning — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg013.perseus-eng4"),
    "lucian-judicium-vocalium-fowler": ("canonical-greekLit",
        "tlg0062/tlg014/tlg0062.tlg014.perseus-eng4.xml",
        "Lucian, Trial in the Court of Vowels — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg014.perseus-eng4"),
    "lucian-symposium-fowler": ("canonical-greekLit",
        "tlg0062/tlg015/tlg0062.tlg015.perseus-eng4.xml",
        "Lucian, A Feast of Lapithae — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg015.perseus-eng4"),
    "lucian-cataplus-fowler": ("canonical-greekLit",
        "tlg0062/tlg016/tlg0062.tlg016.perseus-eng4.xml",
        "Lucian, Voyage To the Lower World — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg016.perseus-eng4"),
    "lucian-juppiter-confutatus-fowler": ("canonical-greekLit",
        "tlg0062/tlg017/tlg0062.tlg017.perseus-eng4.xml",
        "Lucian, Zeus Cross-examined — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg017.perseus-eng4"),
    "lucian-juppiter-tragoedus-fowler": ("canonical-greekLit",
        "tlg0062/tlg018/tlg0062.tlg018.perseus-eng4.xml",
        "Lucian, Zeus Tragoedus — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg018.perseus-eng4"),
    "lucian-gallus-fowler": ("canonical-greekLit",
        "tlg0062/tlg019/tlg0062.tlg019.perseus-eng4.xml",
        "Lucian, The Cock — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg019.perseus-eng4"),
    "lucian-prometheus-fowler": ("canonical-greekLit",
        "tlg0062/tlg020/tlg0062.tlg020.perseus-eng4.xml",
        "Lucian, Prometheus on Caucasus — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg020.perseus-eng4"),
    "lucian-icaromenippus-fowler": ("canonical-greekLit",
        "tlg0062/tlg021/tlg0062.tlg021.perseus-eng4.xml",
        "Lucian, Icaromenippus, an Aerial Expedition — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg021.perseus-eng4"),
    "lucian-timon-fowler": ("canonical-greekLit",
        "tlg0062/tlg022/tlg0062.tlg022.perseus-eng4.xml",
        "Lucian, Timon the Misanthrope — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg022.perseus-eng4"),
    "lucian-contemplantes-fowler": ("canonical-greekLit",
        "tlg0062/tlg023/tlg0062.tlg023.perseus-eng4.xml",
        "Lucian, Charon — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg023.perseus-eng4"),
    "lucian-vitarum-auctio-fowler": ("canonical-greekLit",
        "tlg0062/tlg024/tlg0062.tlg024.perseus-eng4.xml",
        "Lucian, Sale of Creeds — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg024.perseus-eng4"),
    "lucian-piscator-fowler": ("canonical-greekLit",
        "tlg0062/tlg025/tlg0062.tlg025.perseus-eng4.xml",
        "Lucian, The Fisher — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg025.perseus-eng4"),
    "lucian-bis-accusatus-sive-tribunalia-fowler": ("canonical-greekLit",
        "tlg0062/tlg026/tlg0062.tlg026.perseus-eng4.xml",
        "Lucian, The Double Indictment — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg026.perseus-eng4"),
    "lucian-de-sacrificiis-fowler": ("canonical-greekLit",
        "tlg0062/tlg027/tlg0062.tlg027.perseus-eng4.xml",
        "Lucian, Of Sacrifice — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg027.perseus-eng4"),
    "lucian-adversus-indoctum-et-libros-multos-ementem-fowler": ("canonical-greekLit",
        "tlg0062/tlg028/tlg0062.tlg028.perseus-eng4.xml",
        "Lucian, Remarks Addressed To an Illiterate Book-fancier — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg028.perseus-eng4"),
    "lucian-somnium-sive-vita-luciani-fowler": ("canonical-greekLit",
        "tlg0062/tlg029/tlg0062.tlg029.perseus-eng4.xml",
        "Lucian, A Chapter of Autobiography — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg029.perseus-eng4"),
    "lucian-de-parasito-sive-artem-esse-parasiticam-fowler": ("canonical-greekLit",
        "tlg0062/tlg030/tlg0062.tlg030.perseus-eng4.xml",
        "Lucian, The Parasite: a Demonstration that Sponging is a Profession — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg030.perseus-eng4"),
    "lucian-philopseudes-sive-incredulus-fowler": ("canonical-greekLit",
        "tlg0062/tlg031/tlg0062.tlg031.perseus-eng4.xml",
        "Lucian, The Liar — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg031.perseus-eng4"),
    "lucian-de-mercede-fowler": ("canonical-greekLit",
        "tlg0062/tlg033/tlg0062.tlg033.perseus-eng4.xml",
        "Lucian, The Dependent Scholar — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg033.perseus-eng4"),
    "lucian-anacharsis-fowler": ("canonical-greekLit",
        "tlg0062/tlg034/tlg0062.tlg034.perseus-eng4.xml",
        "Lucian, Anacharsis, a Discussion of Physical Training — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg034.perseus-eng4"),
    "lucian-necyomantia-fowler": ("canonical-greekLit",
        "tlg0062/tlg035/tlg0062.tlg035.perseus-eng4.xml",
        "Lucian, Menippus — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg035.perseus-eng4"),
    "lucian-de-luctu-fowler": ("canonical-greekLit",
        "tlg0062/tlg036/tlg0062.tlg036.perseus-eng4.xml",
        "Lucian, Of Mourning — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg036.perseus-eng4"),
    "lucian-rhetorum-praeceptor-fowler": ("canonical-greekLit",
        "tlg0062/tlg037/tlg0062.tlg037.perseus-eng4.xml",
        "Lucian, The Rhetorician’s Vade Mecum — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg037.perseus-eng4"),
    "lucian-alexander-fowler": ("canonical-greekLit",
        "tlg0062/tlg038/tlg0062.tlg038.perseus-eng4.xml",
        "Lucian, Alexander the Oracle-monger — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg038.perseus-eng4"),
    "lucian-imagines-fowler": ("canonical-greekLit",
        "tlg0062/tlg039/tlg0062.tlg039.perseus-eng4.xml",
        "Lucian, A Portrait-study — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg039.perseus-eng4"),
    "lucian-pro-imaginibus-fowler": ("canonical-greekLit",
        "tlg0062/tlg040/tlg0062.tlg040.perseus-eng4.xml",
        "Lucian, Defence of the ‘portrait-study’ — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg040.perseus-eng4"),
    "lucian-de-morte-peregrini-fowler": ("canonical-greekLit",
        "tlg0062/tlg042/tlg0062.tlg042.perseus-eng4.xml",
        "Lucian, The Death of Peregrine — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg042.perseus-eng4"),
    "lucian-fugitivi-fowler": ("canonical-greekLit",
        "tlg0062/tlg043/tlg0062.tlg043.perseus-eng4.xml",
        "Lucian, The Runaways — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg043.perseus-eng4"),
    "lucian-toxaris-vel-amicitia-fowler": ("canonical-greekLit",
        "tlg0062/tlg044/tlg0062.tlg044.perseus-eng4.xml",
        "Lucian, Toxaris: a Dialogue of Friendship — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg044.perseus-eng4"),
    "lucian-de-saltatione-fowler": ("canonical-greekLit",
        "tlg0062/tlg045/tlg0062.tlg045.perseus-eng4.xml",
        "Lucian, Of Pantomime — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg045.perseus-eng4"),
    "lucian-lexiphanes-fowler": ("canonical-greekLit",
        "tlg0062/tlg046/tlg0062.tlg046.perseus-eng4.xml",
        "Lucian, Lexiphanes — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg046.perseus-eng4"),
    "lucian-deorum-concilium-fowler": ("canonical-greekLit",
        "tlg0062/tlg050/tlg0062.tlg050.perseus-eng4.xml",
        "Lucian, The Gods in Council — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg050.perseus-eng4"),
    "lucian-tyrannicida-fowler": ("canonical-greekLit",
        "tlg0062/tlg051/tlg0062.tlg051.perseus-eng4.xml",
        "Lucian, The Tyrannicide — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg051.perseus-eng4"),
    "lucian-abdicatus-fowler": ("canonical-greekLit",
        "tlg0062/tlg052/tlg0062.tlg052.perseus-eng4.xml",
        "Lucian, The Disinherited — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg052.perseus-eng4"),
    "lucian-quomodo-historia-conscribenda-sit-fowler": ("canonical-greekLit",
        "tlg0062/tlg053/tlg0062.tlg053.perseus-eng4.xml",
        "Lucian, The Way To Write History — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg053.perseus-eng4"),
    "lucian-dipsades-fowler": ("canonical-greekLit",
        "tlg0062/tlg054/tlg0062.tlg054.perseus-eng4.xml",
        "Lucian, Dipsas, the Thirst-snake — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg054.perseus-eng4"),
    "lucian-saturnalia-fowler": ("canonical-greekLit",
        "tlg0062/tlg055/tlg0062.tlg055.perseus-eng4.xml",
        "Lucian, Saturnalia — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg055.perseus-eng4"),
    "lucian-herodotus-fowler": ("canonical-greekLit",
        "tlg0062/tlg056/tlg0062.tlg056.perseus-eng4.xml",
        "Lucian, Herodotus and Aetion — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg056.perseus-eng4"),
    "lucian-zeuxis-fowler": ("canonical-greekLit",
        "tlg0062/tlg057/tlg0062.tlg057.perseus-eng4.xml",
        "Lucian, Zeuxis and Antiochus — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg057.perseus-eng4"),
    "lucian-pro-lapsu-inter-salutandum-fowler": ("canonical-greekLit",
        "tlg0062/tlg058/tlg0062.tlg058.perseus-eng4.xml",
        "Lucian, A Slip of the Tongue in Salutation — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg058.perseus-eng4"),
    "lucian-apologia-fowler": ("canonical-greekLit",
        "tlg0062/tlg059/tlg0062.tlg059.perseus-eng4.xml",
        "Lucian, Apology For ‘the Dependent Scholar’ — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg059.perseus-eng4"),
    "lucian-harmonides-fowler": ("canonical-greekLit",
        "tlg0062/tlg060/tlg0062.tlg060.perseus-eng4.xml",
        "Lucian, Harmonides — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg060.perseus-eng4"),
    "lucian-hesiod-fowler": ("canonical-greekLit",
        "tlg0062/tlg061/tlg0062.tlg061.perseus-eng4.xml",
        "Lucian, A Word with Hesiod — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg061.perseus-eng4"),
    "lucian-scytha-fowler": ("canonical-greekLit",
        "tlg0062/tlg062/tlg0062.tlg062.perseus-eng4.xml",
        "Lucian, The Scythian — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg062.perseus-eng4"),
    "lucian-hermotimus-fowler": ("canonical-greekLit",
        "tlg0062/tlg063/tlg0062.tlg063.perseus-eng4.xml",
        "Lucian, Hermotimus, or the Rival Philosophies — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg063.perseus-eng4"),
    "lucian-prometheus-es-in-verbis-fowler": ("canonical-greekLit",
        "tlg0062/tlg064/tlg0062.tlg064.perseus-eng4.xml",
        "Lucian, A Literary Prometheus — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg064.perseus-eng4"),
    "lucian-navigium-fowler": ("canonical-greekLit",
        "tlg0062/tlg065/tlg0062.tlg065.perseus-eng4.xml",
        "Lucian, The Ship: Or, the Wishes — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg065.perseus-eng4"),
    "lucian-dialogi-mortuorum-fowler": ("canonical-greekLit",
        "tlg0062/tlg066/tlg0062.tlg066.perseus-eng4.xml",
        "Lucian, Dialogues of the Dead — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg066.perseus-eng4"),
    "lucian-dialogi-marini-fowler": ("canonical-greekLit",
        "tlg0062/tlg067/tlg0062.tlg067.perseus-eng4.xml",
        "Lucian, Dialogues of the Sea-gods: — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg067.perseus-eng4"),
    "lucian-dialogi-deorum-fowler": ("canonical-greekLit",
        "tlg0062/tlg068/tlg0062.tlg068.perseus-eng4.xml",
        "Lucian, Dialogues of the Gods — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg068.perseus-eng4"),
    "lucian-dialogi-meretricii-fowler": ("canonical-greekLit",
        "tlg0062/tlg069/tlg0062.tlg069.perseus-eng4.xml",
        "Lucian, Dialogues of the Hetaerae — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg069.perseus-eng4"),
    "lucian-soleocista-fowler": ("canonical-greekLit",
        "tlg0062/tlg070/tlg0062.tlg070.perseus-eng4.xml",
        "Lucian, The Purist Purized — H. W. & F. G. Fowler (Clarendon, 1905; d. 1933, 1918) (PD); urn ...tlg0062.tlg070.perseus-eng4"),
    # Isocrates (Norlin, Loeb 1928-29; d. 1942): the eleven pieces in his
    # two volumes. Van Hook's third volume (1945) is not taken. Isaeus
    # (E. S. Forster, Loeb 1927; d. 1950). Appian (Horace White, 1899;
    # d. 1916). Athenaeus (C. D. Yonge, Bohn 1854; d. 1891).
    # Not taken: Demosthenes. Vince's 1926-30 volumes are PD in the US, but
    # J. H. Vince's death date could not be checked from here; Murray
    # (1936-39) and the DeWitts (1949) are in copyright.
    "isocrates-to-demonicus-norlin": ("canonical-greekLit",
        "tlg0010/tlg007/tlg0010.tlg007.perseus-eng2.xml",
        "Isocrates, To Demonicus — George Norlin (Loeb, 1928-29; d. 1942) (PD); urn ...tlg0010.tlg007.perseus-eng2"),
    "isocrates-to-nicocles-norlin": ("canonical-greekLit",
        "tlg0010/tlg013/tlg0010.tlg013.perseus-eng2.xml",
        "Isocrates, To Nicocles — George Norlin (Loeb, 1928-29; d. 1942) (PD); urn ...tlg0010.tlg013.perseus-eng2"),
    "isocrates-nicocles-or-the-cyprians-norlin": ("canonical-greekLit",
        "tlg0010/tlg014/tlg0010.tlg014.perseus-eng2.xml",
        "Isocrates, Nicocles or the Cyprians — George Norlin (Loeb, 1928-29; d. 1942) (PD); urn ...tlg0010.tlg014.perseus-eng2"),
    "isocrates-panegyricus-norlin": ("canonical-greekLit",
        "tlg0010/tlg011/tlg0010.tlg011.perseus-eng2.xml",
        "Isocrates, Panegyricus — George Norlin (Loeb, 1928-29; d. 1942) (PD); urn ...tlg0010.tlg011.perseus-eng2"),
    "isocrates-to-philip-norlin": ("canonical-greekLit",
        "tlg0010/tlg020/tlg0010.tlg020.perseus-eng2.xml",
        "Isocrates, To Philip — George Norlin (Loeb, 1928-29; d. 1942) (PD); urn ...tlg0010.tlg020.perseus-eng2"),
    "isocrates-archidamus-norlin": ("canonical-greekLit",
        "tlg0010/tlg016/tlg0010.tlg016.perseus-eng2.xml",
        "Isocrates, Archidamus — George Norlin (Loeb, 1928-29; d. 1942) (PD); urn ...tlg0010.tlg016.perseus-eng2"),
    "isocrates-areopagiticus-norlin": ("canonical-greekLit",
        "tlg0010/tlg018/tlg0010.tlg018.perseus-eng2.xml",
        "Isocrates, Areopagiticus — George Norlin (Loeb, 1928-29; d. 1942) (PD); urn ...tlg0010.tlg018.perseus-eng2"),
    "isocrates-on-the-peace-norlin": ("canonical-greekLit",
        "tlg0010/tlg017/tlg0010.tlg017.perseus-eng2.xml",
        "Isocrates, On the Peace — George Norlin (Loeb, 1928-29; d. 1942) (PD); urn ...tlg0010.tlg017.perseus-eng2"),
    "isocrates-panathenaicus-norlin": ("canonical-greekLit",
        "tlg0010/tlg021/tlg0010.tlg021.perseus-eng2.xml",
        "Isocrates, Panathenaicus — George Norlin (Loeb, 1928-29; d. 1942) (PD); urn ...tlg0010.tlg021.perseus-eng2"),
    "isocrates-against-the-sophists-norlin": ("canonical-greekLit",
        "tlg0010/tlg008/tlg0010.tlg008.perseus-eng2.xml",
        "Isocrates, Against the Sophists — George Norlin (Loeb, 1928-29; d. 1942) (PD); urn ...tlg0010.tlg008.perseus-eng2"),
    "isocrates-antidosis-norlin": ("canonical-greekLit",
        "tlg0010/tlg019/tlg0010.tlg019.perseus-eng2.xml",
        "Isocrates, Antidosis — George Norlin (Loeb, 1928-29; d. 1942) (PD); urn ...tlg0010.tlg019.perseus-eng2"),
    # Roman comedy: Plautus' twenty plays and Terence's six, all in H. T.
    # Riley's prose (Plautus 1852, Terence 1853; Riley d. 1878).
    "plautus-amphitryon-riley": ("canonical-latinLit",
        "phi0119/phi001/phi0119.phi001.perseus-eng2.xml",
        "Plautus, Amphitryon — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi001.perseus-eng2"),
    "plautus-asinaria-riley": ("canonical-latinLit",
        "phi0119/phi002/phi0119.phi002.perseus-eng2.xml",
        "Plautus, Asinaria — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi002.perseus-eng2"),
    "plautus-aulularia-riley": ("canonical-latinLit",
        "phi0119/phi003/phi0119.phi003.perseus-eng2.xml",
        "Plautus, Aulularia — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi003.perseus-eng2"),
    "plautus-bacchides-riley": ("canonical-latinLit",
        "phi0119/phi004/phi0119.phi004.perseus-eng2.xml",
        "Plautus, Bacchides — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi004.perseus-eng2"),
    "plautus-captivi-riley": ("canonical-latinLit",
        "phi0119/phi005/phi0119.phi005.perseus-eng2.xml",
        "Plautus, Captivi — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi005.perseus-eng2"),
    "plautus-casina-riley": ("canonical-latinLit",
        "phi0119/phi006/phi0119.phi006.perseus-eng2.xml",
        "Plautus, Casina — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi006.perseus-eng2"),
    "plautus-cistellaria-riley": ("canonical-latinLit",
        "phi0119/phi007/phi0119.phi007.perseus-eng2.xml",
        "Plautus, Cistellaria — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi007.perseus-eng2"),
    "plautus-curculio-riley": ("canonical-latinLit",
        "phi0119/phi008/phi0119.phi008.perseus-eng2.xml",
        "Plautus, Curculio — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi008.perseus-eng2"),
    "plautus-epidicus-riley": ("canonical-latinLit",
        "phi0119/phi009/phi0119.phi009.perseus-eng2.xml",
        "Plautus, Epidicus — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi009.perseus-eng2"),
    "plautus-menaechmi-riley": ("canonical-latinLit",
        "phi0119/phi010/phi0119.phi010.perseus-eng2.xml",
        "Plautus, Menaechmi — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi010.perseus-eng2"),
    "plautus-mercator-riley": ("canonical-latinLit",
        "phi0119/phi011/phi0119.phi011.perseus-eng2.xml",
        "Plautus, Mercator — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi011.perseus-eng2"),
    "plautus-miles-gloriosus-riley": ("canonical-latinLit",
        "phi0119/phi012/phi0119.phi012.perseus-eng2.xml",
        "Plautus, Miles Gloriosus — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi012.perseus-eng2"),
    "plautus-mostellaria-riley": ("canonical-latinLit",
        "phi0119/phi013/phi0119.phi013.perseus-eng2.xml",
        "Plautus, Mostellaria — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi013.perseus-eng2"),
    "plautus-persa-riley": ("canonical-latinLit",
        "phi0119/phi014/phi0119.phi014.perseus-eng2.xml",
        "Plautus, Persa — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi014.perseus-eng2"),
    "plautus-poenulus-riley": ("canonical-latinLit",
        "phi0119/phi015/phi0119.phi015.perseus-eng2.xml",
        "Plautus, Poenulus — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi015.perseus-eng2"),
    "plautus-pseudolus-riley": ("canonical-latinLit",
        "phi0119/phi016/phi0119.phi016.perseus-eng2.xml",
        "Plautus, Pseudolus — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi016.perseus-eng2"),
    "plautus-rudens-riley": ("canonical-latinLit",
        "phi0119/phi017/phi0119.phi017.perseus-eng2.xml",
        "Plautus, Rudens — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi017.perseus-eng2"),
    "plautus-stichus-riley": ("canonical-latinLit",
        "phi0119/phi018/phi0119.phi018.perseus-eng2.xml",
        "Plautus, Stichus — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi018.perseus-eng2"),
    "plautus-trinummus-riley": ("canonical-latinLit",
        "phi0119/phi019/phi0119.phi019.perseus-eng2.xml",
        "Plautus, Trinummus — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi019.perseus-eng2"),
    "plautus-truculentus-riley": ("canonical-latinLit",
        "phi0119/phi020/phi0119.phi020.perseus-eng2.xml",
        "Plautus, Truculentus — H. T. Riley (Bohn 1852, Bell reprint 1912-13; d. 1878) (PD); urn ...phi0119.phi020.perseus-eng2"),
    "terence-andria-riley": ("canonical-latinLit",
        "phi0134/phi001/phi0134.phi001.perseus-eng2.xml",
        "Terence, Andria — H. T. Riley (1874 printing; d. 1878) (PD); urn ...phi0134.phi001.perseus-eng2"),
    "terence-heautontimorumenos-riley": ("canonical-latinLit",
        "phi0134/phi002/phi0134.phi002.perseus-eng2.xml",
        "Terence, Heautontimorumenos — H. T. Riley (1874 printing; d. 1878) (PD); urn ...phi0134.phi002.perseus-eng2"),
    "terence-eunuchus-riley": ("canonical-latinLit",
        "phi0134/phi003/phi0134.phi003.perseus-eng2.xml",
        "Terence, Eunuchus — H. T. Riley (1874 printing; d. 1878) (PD); urn ...phi0134.phi003.perseus-eng2"),
    "terence-phormio-riley": ("canonical-latinLit",
        "phi0134/phi004/phi0134.phi004.perseus-eng2.xml",
        "Terence, Phormio — H. T. Riley (1874 printing; d. 1878) (PD); urn ...phi0134.phi004.perseus-eng2"),
    "terence-hecyra-riley": ("canonical-latinLit",
        "phi0134/phi005/phi0134.phi005.perseus-eng2.xml",
        "Terence, Hecyra — H. T. Riley (1874 printing; d. 1878) (PD); urn ...phi0134.phi005.perseus-eng2"),
    "terence-adelphi-riley": ("canonical-latinLit",
        "phi0134/phi006/phi0134.phi006.perseus-eng2.xml",
        "Terence, Adelphi — H. T. Riley (1874 printing; d. 1878) (PD); urn ...phi0134.phi006.perseus-eng2"),
    # Livy in Bohn's translation (Spillan, Edmonds, McDevitte, 1849-57);
    # Gellius (Rolfe, Loeb 1927; d. 1943); Horace's Satires and Art of
    # Poetry in Christopher Smart's prose (d. 1771); Caesar's Civil War in
    # William Duncan's (d. 1760), a second witness beside Peskett. Not
    # taken: Livy in Canon Roberts (1912; his death date unchecked here),
    # Celsus (Spencer, 1935-38).
    "livy-history-spillan": ("canonical-latinLit",
        "phi0914/phi001/phi0914.phi001.perseus-eng2.xml",
        "Livy, History of Rome — D. Spillan, Cyrus Edmonds, W. A. McDevitte (Bohn, 1849-57) (PD); urn ...phi0914.phi001.perseus-eng2"),
    "gellius-attic-nights-rolfe": ("canonical-latinLit",
        "phi1254/phi001/phi1254.phi001.perseus-eng1.xml",
        "Aulus Gellius, Attic Nights — J. C. Rolfe (Loeb, 1927; d. 1943) (PD); urn ...phi1254.phi001.perseus-eng1"),
    "horace-satires-smart": ("canonical-latinLit",
        "phi0893/phi004/phi0893.phi004.perseus-eng2.xml",
        "Horace, Satires — Christopher Smart (prose; 1863 printing; d. 1771) (PD); urn ...phi0893.phi004.perseus-eng2"),
    "horace-ars-poetica-smart": ("canonical-latinLit",
        "phi0893/phi006/phi0893.phi006.perseus-eng2.xml",
        "Horace, The Art of Poetry — Christopher Smart (prose; 1863 printing; d. 1771) (PD); urn ...phi0893.phi006.perseus-eng2"),
    "caesar-civil-war-duncan": ("canonical-latinLit",
        "phi0448/phi002/phi0448.phi002.perseus-eng3.xml",
        "Caesar, Civil War — William Duncan (1856 printing; d. 1760) (PD); urn ...phi0448.phi002.perseus-eng3"),
    "isaeus-on-the-estate-of-cleonymus-forster": ("canonical-greekLit",
        "tlg0017/tlg001/tlg0017.tlg001.perseus-eng2.xml",
        "Isaeus, On The Estate of Cleonymus — E. S. Forster (Loeb, 1927; d. 1950) (PD); urn ...tlg0017.tlg001.perseus-eng2"),
    "isaeus-on-the-estate-of-menecles-forster": ("canonical-greekLit",
        "tlg0017/tlg002/tlg0017.tlg002.perseus-eng2.xml",
        "Isaeus, On the Estate of Menecles — E. S. Forster (Loeb, 1927; d. 1950) (PD); urn ...tlg0017.tlg002.perseus-eng2"),
    "isaeus-on-the-estate-of-pyrrhus-forster": ("canonical-greekLit",
        "tlg0017/tlg003/tlg0017.tlg003.perseus-eng2.xml",
        "Isaeus, On The Estate Of Pyrrhus — E. S. Forster (Loeb, 1927; d. 1950) (PD); urn ...tlg0017.tlg003.perseus-eng2"),
    "isaeus-on-the-estate-of-nicostratus-forster": ("canonical-greekLit",
        "tlg0017/tlg004/tlg0017.tlg004.perseus-eng2.xml",
        "Isaeus, On the Estate of Nicostratus — E. S. Forster (Loeb, 1927; d. 1950) (PD); urn ...tlg0017.tlg004.perseus-eng2"),
    "isaeus-on-the-estate-of-dicaeogenes-forster": ("canonical-greekLit",
        "tlg0017/tlg005/tlg0017.tlg005.perseus-eng2.xml",
        "Isaeus, On the Estate of Dicaeogenes — E. S. Forster (Loeb, 1927; d. 1950) (PD); urn ...tlg0017.tlg005.perseus-eng2"),
    "isaeus-on-the-estate-of-philoctemon-forster": ("canonical-greekLit",
        "tlg0017/tlg006/tlg0017.tlg006.perseus-eng2.xml",
        "Isaeus, On the Estate of Philoctemon — E. S. Forster (Loeb, 1927; d. 1950) (PD); urn ...tlg0017.tlg006.perseus-eng2"),
    "isaeus-on-the-estate-of-apollodorus-forster": ("canonical-greekLit",
        "tlg0017/tlg007/tlg0017.tlg007.perseus-eng2.xml",
        "Isaeus, On The Estate of Apollodorus — E. S. Forster (Loeb, 1927; d. 1950) (PD); urn ...tlg0017.tlg007.perseus-eng2"),
    "isaeus-on-the-estate-of-ciron-forster": ("canonical-greekLit",
        "tlg0017/tlg008/tlg0017.tlg008.perseus-eng2.xml",
        "Isaeus, On The Estate of Ciron — E. S. Forster (Loeb, 1927; d. 1950) (PD); urn ...tlg0017.tlg008.perseus-eng2"),
    "isaeus-on-the-estate-of-astyphilus-forster": ("canonical-greekLit",
        "tlg0017/tlg009/tlg0017.tlg009.perseus-eng2.xml",
        "Isaeus, On the Estate of Astyphilus — E. S. Forster (Loeb, 1927; d. 1950) (PD); urn ...tlg0017.tlg009.perseus-eng2"),
    "isaeus-on-the-estate-of-aristarchus-forster": ("canonical-greekLit",
        "tlg0017/tlg010/tlg0017.tlg010.perseus-eng2.xml",
        "Isaeus, On The Estate of Aristarchus — E. S. Forster (Loeb, 1927; d. 1950) (PD); urn ...tlg0017.tlg010.perseus-eng2"),
    "isaeus-on-the-estate-of-hagnias-forster": ("canonical-greekLit",
        "tlg0017/tlg011/tlg0017.tlg011.perseus-eng2.xml",
        "Isaeus, On the Estate of Hagnias — E. S. Forster (Loeb, 1927; d. 1950) (PD); urn ...tlg0017.tlg011.perseus-eng2"),
    "isaeus-on-behalf-of-euphiletus-forster": ("canonical-greekLit",
        "tlg0017/tlg012/tlg0017.tlg012.perseus-eng2.xml",
        "Isaeus, On Behalf of Euphiletus — E. S. Forster (Loeb, 1927; d. 1950) (PD); urn ...tlg0017.tlg012.perseus-eng2"),
    "appian-author-s-preface-white": ("canonical-greekLit",
        "tlg0551/tlg001/tlg0551.tlg001.perseus-eng2.xml",
        "Appian, Author’s Preface — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg001.perseus-eng2"),
    "appian-concerning-the-kings-white": ("canonical-greekLit",
        "tlg0551/tlg002/tlg0551.tlg002.perseus-eng2.xml",
        "Appian, Concerning the Kings — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg002.perseus-eng2"),
    "appian-concerning-italy-white": ("canonical-greekLit",
        "tlg0551/tlg003/tlg0551.tlg003.perseus-eng2.xml",
        "Appian, Concerning Italy — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg003.perseus-eng2"),
    "appian-the-samnite-history-white": ("canonical-greekLit",
        "tlg0551/tlg004/tlg0551.tlg004.perseus-eng2.xml",
        "Appian, The Samnite History — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg004.perseus-eng2"),
    "appian-the-gallic-history-white": ("canonical-greekLit",
        "tlg0551/tlg005/tlg0551.tlg005.perseus-eng2.xml",
        "Appian, The Gallic History — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg005.perseus-eng2"),
    "appian-of-sicily-and-the-other-islands-white": ("canonical-greekLit",
        "tlg0551/tlg006/tlg0551.tlg006.perseus-eng2.xml",
        "Appian, Of Sicily and the Other Islands — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg006.perseus-eng2"),
    "appian-the-wars-in-spain-white": ("canonical-greekLit",
        "tlg0551/tlg007/tlg0551.tlg007.perseus-eng2.xml",
        "Appian, The Wars in Spain — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg007.perseus-eng2"),
    "appian-the-hannibalic-war-white": ("canonical-greekLit",
        "tlg0551/tlg008/tlg0551.tlg008.perseus-eng2.xml",
        "Appian, The Hannibalic War — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg008.perseus-eng2"),
    "appian-the-punic-wars-white": ("canonical-greekLit",
        "tlg0551/tlg009/tlg0551.tlg009.perseus-eng2.xml",
        "Appian, The Punic Wars — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg009.perseus-eng2"),
    "appian-numidian-affairs-white": ("canonical-greekLit",
        "tlg0551/tlg010/tlg0551.tlg010.perseus-eng2.xml",
        "Appian, Numidian Affairs — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg010.perseus-eng2"),
    "appian-macedonian-affairs-white": ("canonical-greekLit",
        "tlg0551/tlg011/tlg0551.tlg011.perseus-eng2.xml",
        "Appian, Macedonian Affairs — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg011.perseus-eng2"),
    "appian-the-illyrian-wars-white": ("canonical-greekLit",
        "tlg0551/tlg012/tlg0551.tlg012.perseus-eng2.xml",
        "Appian, The Illyrian Wars — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg012.perseus-eng2"),
    "appian-the-syrian-wars-white": ("canonical-greekLit",
        "tlg0551/tlg013/tlg0551.tlg013.perseus-eng2.xml",
        "Appian, The Syrian Wars — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg013.perseus-eng2"),
    "appian-the-mithridatic-wars-white": ("canonical-greekLit",
        "tlg0551/tlg014/tlg0551.tlg014.perseus-eng2.xml",
        "Appian, The Mithridatic Wars — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg014.perseus-eng2"),
    "appian-the-civil-wars-white": ("canonical-greekLit",
        "tlg0551/tlg017/tlg0551.tlg017.perseus-eng2.xml",
        "Appian, The Civil Wars — Horace White (Macmillan, 1899; d. 1916) (PD); urn ...tlg0551.tlg017.perseus-eng2"),
    "athenaeus-deipnosophists-yonge": ("canonical-greekLit",
        "tlg0008/tlg001/tlg0008.tlg001.perseus-eng2.xml",
        "Athenaeus, The Deipnosophists — C. D. Yonge (Bohn, 1854; d. 1891) (PD); urn ...tlg0008.tlg001.perseus-eng2"),
}

# Gutenberg .txt shelf (structured by structure_texts.py's converters).
# IDs are the acquisitions ledger. The first four migrated here from
# patrimonium's mine_names.py GUTENBERG dict at extraction (2026-07-22).
GUTENBERG_EXTRA = {
    "kjv_bible": 10,              # King James Version (verse-exact scheme)
    "shakespeare": 100,           # Complete Works (drama converter)
    "paradise_lost": 20,          # Milton
    "divine_comedy": 8800,        # Dante, tr. Cary
    "paradise_regained": 58,      # Milton
    "beowulf": 16328,             # tr. Gummere
    "gilgamesh": 11000,           # Old Babylonian, tr. Jastrow & Clay
    "faust": 14591,               # Goethe, tr. Bayard Taylor (original metres)
    "treasure_island": 120,       # Stevenson
}
GUTENBERG_TXT = "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"

CCEL_XML = "https://ccel.org/ccel/{initial}/{author}/{work}.xml"

# ---------------------------------------------------------------- Lexicons
#
# Reference works keyed by lemma rather than linear texts (structured by
# structure_texts.py's lexicon converters). All three underlying works are
# public domain; the rights line of the exact edition was read, per the
# 2026-07-26 standing rule, and is recorded per entry below.
#
# THAYER'S is here too, but it is not a fetch -- it is an OCR job, and the
# only one in this repo. The 1889 lexicon is PD and scanned (archive.org
# greekenglishlexi00grimuoft, 760pp, NOT_IN_COPYRIGHT), but no machine-readable
# edition exists: that scan's own text layer contains ZERO Greek codepoints --
# every Greek word came out as mangled Latin ("edris" for elpis). Abbott-Smith
# 1922 fails identically. So on 2026-09-06 the PDF was re-OCR'd with tesseract
# grc+eng at 300dpi, recovering 552,594 Greek characters, and the page text
# lives in data/corpus/lexicons/thayer-pages.json (gitignored with the rest of
# the corpus; regenerate with the recipe in CLAUDE.md).
#
# slug -> (url, local filename, note)
LEXICONS = {
    "strongs-hebrew": (
        "https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/HebrewStrong.xml",
        "strongs-hebrew.xml",
        "Strong's Hebrew Dictionary (James Strong, 1890 — PD). OpenScriptures "
        "HebrewLexicon transcription; markup CC BY 4.0, dictionary text PD. "
        "8,674 entries = the complete H1–H8674 numbering (verified 2026-09-06)."),
    "strongs-greek": (
        "https://raw.githubusercontent.com/openscriptures/strongs/master/"
        "greek/StrongsGreekDictionaryXML_1.4/strongsgreek.xml",
        "strongs-greek.xml",
        "Strong's Greek Dictionary (James Strong, 1890 — PD). OpenScriptures "
        "strongs repo. 5,624 entries = the complete G1–G5624 numbering "
        "(verified 2026-09-06). Unicode Greek intact."),
    # STEPBible Greek. CC BY 4.0 — NOT public domain, and the only non-PD
    # material in this repo. Adam's call, 2026-09-06: collect and use, do not
    # redistribute in whole. The licence permits redistribution; the
    # maintainers ASK that people be pointed at github.com/STEPBible instead
    # so corrections flow from one source. Honored structurally, not just in
    # prose: these land in data/corpus/ and build to data/books/*.json, both
    # gitignored, so only the manifest pointer is ever committed. The built
    # books carry rights.redistribute_whole = false; anything serving this
    # corpus must respect it.
    "tbesg-greek": (
        "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/Lexicons/"
        "TBESG%20-%20Translators%20Brief%20lexicon%20of%20Extended%20Strongs%20for%20Greek%20-%20STEPBible.org%20CC%20BY.txt",
        "tbesg-greek.txt",
        "Translators Brief lexicon of Extended Strongs for Greek — Abbott-Smith "
        "(1922, PD) definitions edited to extended Strong's by Tyndale House. "
        "CC BY 4.0. 9,550 entries."),
    "tflsj-greek-0-5624": (
        "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/Lexicons/"
        "TFLSJ%20%200-5624%20-%20Translators%20Formatted%20full%20LSJ%20Bible%20lexicon%20-%20STEPBible.org%20CC%20BY.txt",
        "tflsj-greek-0-5624.txt",
        "Full Liddell-Scott-Jones, Bible edition, G0-G5624 — LSJ edited by "
        "Tyndale House scholars. CC BY 4.0. 5,709 entries, 2.17M Greek chars."),
    "tflsj-greek-extra": (
        "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/Lexicons/"
        "TFLSJ%20extra%20-%20Translators%20Formatted%20full%20LSJ%20Bible%20lexicon%20-%20STEPBible.org%20CC%20BY.txt",
        "tflsj-greek-extra.txt",
        "Full LSJ, the G6000+ extras (LXX and variant vocabulary beyond Strong's "
        "range). CC BY 4.0. 3,840 entries."),
    "bdb-hebrew": (
        "https://raw.githubusercontent.com/eliranwong/unabridged-BDB-Hebrew-lexicon/"
        "master/unabridged-BDB-Hebrew-lexicon.csv.zip",
        "bdb-hebrew.tsv",
        "Brown-Driver-Briggs, A Hebrew and English Lexicon of the Old Testament "
        "(1906 — PD), UNABRIDGED. Repo states 'Public domain document'; formatting "
        "by Eliran Wong from Bible Analyzer data, scripture refs parsed by Stephen "
        "Ku et al. 10,022 entries, median 1,184 chars (the real thing, not the "
        "2.7MB abridged outline in OpenScriptures/HebrewLexicon)."),
}


# slug -> (author, work, note)  — all probed 200 on 2026-07-21
CCEL = {
    "owen-mort":        ("owen", "mort", "Of the Mortification of Sin in Believers"),
    "owen-temptation":  ("owen", "temptation", "Of Temptation"),
    "owen-communion":   ("owen", "communion", "Of Communion with God"),
    "owen-glory":       ("owen", "glory", "Meditations on the Glory of Christ"),
    "flavel-fountain":  ("flavel", "fountain", "The Fountain of Life"),
    "bunyan-pilgrim":   ("bunyan", "pilgrim", "The Pilgrim's Progress"),
    "bunyan-holy_war":  ("bunyan", "holy_war", "The Holy War"),
    "edwards-affections": ("edwards", "affections", "Religious Affections"),
    "edwards-works1":   ("edwards", "works1", "Works of Jonathan Edwards, vol. 1 (1834 ed.)"),
    # 2026-09-28: the rest of CCEL's Edwards (see also edwards_shelf.json for
    # the Dwight / Worcester editions and early printings, raw OCR)
    "edwards-works2":   ("edwards", "works2", "Works of Jonathan Edwards, vol. 2 (1834 ed.)"),
    "edwards-sermons":  ("edwards", "sermons", "Select Sermons"),
    "edwards-treatiseongrace": ("edwards", "treatiseongrace", "Treatise on Grace"),
    "edwards-trinity":  ("edwards", "trinity", "An Unpublished Essay on the Trinity"),
    "edwards-will":     ("edwards", "will", "Freedom of the Will"),
}

# Calvin's Commentaries (Calvin Translation Society, 45 vols.) — CCEL's
# "Calvin's Commentaries—Complete" collection. Manifest-Ingest pilot library
# (Word Hoard vault, "Armarium Libraries" 2026-08-28): biggest, best-structured,
# uniformly-formatted CCEL corpus — if the ThML parser survives this, it
# survives the rest of the launch list. Slugs + volume titles confirmed
# against CCEL's own work-info page 2026-08-28; calcom01 probed 200 same day.
CALVIN_COMMENTARIES = {
    "calvin-com01": "Genesis 1-23",
    "calvin-com02": "Genesis 24-50",
    "calvin-com03": "Harmony of the Law, Vol. 1",
    "calvin-com04": "Harmony of the Law, Vol. 2",
    "calvin-com05": "Harmony of the Law, Vol. 3",
    "calvin-com06": "Harmony of the Law, Vol. 4",
    "calvin-com07": "Joshua",
    "calvin-com08": "Psalms 1-35",
    "calvin-com09": "Psalms 36-66",
    "calvin-com10": "Psalms 67-92",
    "calvin-com11": "Psalms 93-119",
    "calvin-com12": "Psalms 119-150",
    "calvin-com13": "Isaiah 1-16",
    "calvin-com14": "Isaiah 17-32",
    "calvin-com15": "Isaiah 33-48",
    "calvin-com16": "Isaiah 49-66",
    "calvin-com17": "Jeremiah-Lamentations 1-9",
    "calvin-com18": "Jeremiah-Lamentations 10-19",
    "calvin-com19": "Jeremiah-Lamentations 20-29",
    "calvin-com20": "Jeremiah-Lamentations 30-47",
    "calvin-com21": "Jeremiah-Lamentations 48-52",
    "calvin-com22": "Ezekiel 1-12",
    "calvin-com23": "Ezekiel 13-20",
    "calvin-com24": "Daniel 1-6",
    "calvin-com25": "Daniel 7-12",
    "calvin-com26": "Hosea",
    "calvin-com27": "Joel-Amos-Obadiah",
    "calvin-com28": "Jonah-Micah-Nahum",
    "calvin-com29": "Habakkuk-Zephaniah-Haggai",
    "calvin-com30": "Zechariah-Malachi",
    "calvin-com31": "Harmony of the Gospels, Vol. 1",
    "calvin-com32": "Harmony of the Gospels, Vol. 2",
    "calvin-com33": "Harmony of the Gospels, Vol. 3",
    "calvin-com34": "John 1-11",
    "calvin-com35": "John 12-21",
    "calvin-com36": "Acts 1-13",
    "calvin-com37": "Acts 14-28",
    "calvin-com38": "Romans",
    "calvin-com39": "1 Corinthians 1-14",
    "calvin-com40": "1 Corinthians 15-16, 2 Corinthians",
    "calvin-com41": "Galatians-Ephesians",
    "calvin-com42": "Philippians-Colossians-Thessalonians",
    "calvin-com43": "Timothy, Titus, Philemon",
    "calvin-com44": "Hebrews",
    "calvin-com45": "Catholic Epistles",
}
for _i in range(1, 46):
    _slug = f"calvin-com{_i:02d}"
    CCEL[_slug] = ("calvin", f"calcom{_i:02d}",
                   f"Commentary on {CALVIN_COMMENTARIES[_slug]} (Calvin Translation Society ed.)")

# G. K. Chesterton (1874-1936) — the public-domain library, 2026-09-29.
#
# RIGHTS RULE: US public domain = published 1930 or earlier (as of 2026). He
# died 1936, so the UK/life+70 rule clears everything, but the hosted chest is
# in the US and the US rule is the binding one. Every Gutenberg header below
# was grepped for "COPYRIGHTED Project Gutenberg" (none); every CCEL head reads
# DC.Rights "Public Domain" except queertrades/treesofpride (blank; 1905 and
# 1922, PD by date). No translators: all original English.
#
# SOURCE RULE: CCEL ThML first (stable section ids, scripRef harvest), then
# Gutenberg for what CCEL lacks. Where both hold a work, CCEL only.
#
# DELIBERATELY EXCLUDED (the completeness note):
#   ccel aquinas       — St. Thomas Aquinas (1933): US copyright until 2029.
#                        CCEL marks it PD (Canadian rule); we are US-hosted.
#   ccel preexistence  — "The Pre-Existence of Christ in Scripture,
#                        Patristics, and Creed": catalogued under Chesterton
#                        on CCEL but not a Chesterton work; rights unknown.
#   PG 130 / 16769     — Orthodoxy: taken from CCEL instead.
#   PG books where GKC is only illustrator (Belloc's novels), introducer
#   (Aesop, Gorky, Job, Cecil's History of the U.S., etc.) or contributor
#   (Joy Street annuals, Biography for Beginners); non-English PG
#   translations (Finnish, Portuguese); PG audio.
#   US-PD but on neither CCEL nor Gutenberg (would need archive.org scans ->
#   Unscanner, DEFERRED): The Incredulity of Father Brown (1926), The
#   Outline of Sanity (1926), The Return of Don Quixote (1927), Robert Louis
#   Stevenson (1927), Generally Speaking (1928), The Thing (1929), The Poet
#   and the Lunatics (1929), Four Faultless Felons (1930), The Resurrection
#   of Rome (1930), Come to Think of It (1930), and the uncollected
#   periodical essays.
#   Not yet PD in the US (1931+): Autobiography, The Well and the Shallows,
#   Chaucer, The Scandal of Father Brown, Aquinas, and the rest of the
#   1931-36 books.
CHESTERTON_CCEL = {   # slug -> (ccel work, title)
    "chesterton-america":      ("america", "What I Saw in America (1922)"),
    "chesterton-ball_cross":   ("ball_cross", "The Ball and the Cross (1909)"),
    "chesterton-defendant":    ("defendant", "The Defendant (1901)"),
    "chesterton-divorce":      ("divorce", "The Superstition of Divorce (1920)"),
    "chesterton-eugenics":     ("eugenics", "Eugenics and Other Evils (1922)"),
    "chesterton-everlasting":  ("everlasting", "The Everlasting Man (1925)"),
    "chesterton-heretics":     ("heretics", "Heretics (1905)"),
    "chesterton-historyengland": ("historyengland", "A Short History of England (1917)"),
    "chesterton-innocencebrown": ("innocencebrown", "The Innocence of Father Brown (1911)"),
    "chesterton-longbow":      ("longbow", "Tales of the Long Bow (1925)"),
    "chesterton-magic":        ("magic", "Magic: A Fantastic Comedy (1913)"),
    "chesterton-manalive":     ("manalive", "Manalive (1912)"),
    "chesterton-napoleon":     ("napoleon", "The Napoleon of Notting Hill (1904)"),
    "chesterton-orthodoxy":    ("orthodoxy", "Orthodoxy (1908)"),
    "chesterton-queertrades":  ("queertrades", "The Club of Queer Trades (1905)"),
    "chesterton-rightworld":   ("rightworld", "What Is Right with the World (1910 essay)"),
    "chesterton-thingsconsidered": ("thingsconsidered", "All Things Considered (1908)"),
    "chesterton-thursday":     ("thursday", "The Man Who Was Thursday (1908)"),
    "chesterton-toomuch":      ("toomuch", "The Man Who Knew Too Much (1922)"),
    "chesterton-treesofpride": ("treesofpride", "The Trees of Pride (1922)"),
    "chesterton-trifles":      ("trifles", "Tremendous Trifles (1909)"),
    "chesterton-victorianage": ("victorianage", "The Victorian Age in Literature (1913)"),
    "chesterton-whatwrong":    ("whatwrong", "What's Wrong with the World (1910)"),
    "chesterton-whitehorse":   ("whitehorse", "The Ballad of the White Horse (1911)"),
    "chesterton-wisdom":       ("wisdom", "The Wisdom of Father Brown (1914)"),
}
for _slug, (_work, _title) in CHESTERTON_CCEL.items():
    CCEL[_slug] = ("chesterton", _work, _title)

# slug -> (Gutenberg id, title, author as the book names it). Structured by
# structure_texts.py's prose converter with headings read from each book's
# own CONTENTS (contents_chapre). Verse collections and the one play (Magic,
# on CCEL) are paragraph/stanza-level first passes.
CHESTERTON_GUTENBERG = {
    "chesterton-calendar":     (45811, "A Chesterton Calendar (1911)", "G. K. Chesterton"),
    "chesterton-miscellany":   (2015, "A Miscellany of Men (1912)", "G. K. Chesterton"),
    "chesterton-alarms":       (9656, "Alarms and Discursions (1910)", "G. K. Chesterton"),
    "chesterton-dickens-appreciations": (22362, "Appreciations and Criticisms of the Works of Charles Dickens (1911)", "G. K. Chesterton"),
    "chesterton-dickens-bookman": (61760, "Charles Dickens (Bookman Booklets)", "G. K. Chesterton & F. G. Kitton"),
    "chesterton-dickens":      (68682, "Charles Dickens: A Critical Study (1906)", "G. K. Chesterton"),
    "chesterton-divorce-democracy": (62467, "Divorce versus Democracy (1916)", "G. K. Chesterton"),
    "chesterton-fancies":      (60164, "Fancies versus Fads (1923)", "G. K. Chesterton"),
    "chesterton-watts":        (64074, "G. F. Watts (1904)", "G. K. Chesterton"),
    "chesterton-shaw":         (19535, "George Bernard Shaw (1909)", "G. K. Chesterton"),
    "chesterton-greybeards":   (14706, "Greybeards at Play (1900)", "G. K. Chesterton"),
    "chesterton-irish":        (61758, "Irish Impressions (1919)", "G. K. Chesterton"),
    "chesterton-tolstoy":      (62045, "Leo Tolstoy (Bookman Booklets)", "G. K. Chesterton, G. H. Perris & Edward Garnett"),
    "chesterton-london":       (62048, "London (1914)", "G. K. Chesterton (photographs by A. L. Coburn)"),
    "chesterton-kitchener":    (25795, "Lord Kitchener (1917)", "G. K. Chesterton"),
    "chesterton-poems":        (31184, "Poems (1915)", "G. K. Chesterton"),
    "chesterton-browning":     (13342, "Robert Browning (1903)", "G. K. Chesterton"),
    "chesterton-francis":      (63084, "St. Francis of Assisi (1923)", "G. K. Chesterton"),
    "chesterton-tennyson":     (61764, "Tennyson (Bookman Booklets)", "G. K. Chesterton & Richard Garnett"),
    "chesterton-thackeray":    (62086, "Thackeray (Bookman Booklets)", "G. K. Chesterton & Lewis Melville"),
    "chesterton-appetite":     (11605, "The Appetite of Tyranny (1915)", "G. K. Chesterton"),
    "chesterton-barbara":      (32167, "The Ballad of St. Barbara, and Other Verses (1922)", "G. K. Chesterton"),
    "chesterton-berlin":       (11560, "The Barbarism of Berlin (1914)", "G. K. Chesterton"),
    "chesterton-conversion":   (76305, "The Catholic Church and Conversion (1926)", "G. K. Chesterton"),
    "chesterton-crimes":       (11554, "The Crimes of England (1915)", "G. K. Chesterton"),
    "chesterton-flyinginn":    (59239, "The Flying Inn (1914)", "G. K. Chesterton"),
    "chesterton-jerusalem":    (13468, "The New Jerusalem (1920)", "G. K. Chesterton"),
    "chesterton-diversity":    (60057, "The Uses of Diversity (1920)", "G. K. Chesterton"),
    "chesterton-wildknight":   (12037, "The Wild Knight and Other Poems (1900)", "G. K. Chesterton"),
    "chesterton-secretbrown":  (70175, "The Secret of Father Brown (1927)", "G. K. Chesterton"),
    "chesterton-carlyle":      (71159, "Thomas Carlyle (Bookman Booklets)", "G. K. Chesterton & J. E. Hodder-Williams"),
    "chesterton-twelvetypes":  (12491, "Twelve Types (1902)", "G. K. Chesterton"),
    "chesterton-usurers":      (2134, "Utopia of Usurers and Other Essays (1917)", "G. K. Chesterton"),
    "chesterton-variedtypes":  (14203, "Varied Types (1903)", "G. K. Chesterton"),
    "chesterton-blake":        (67639, "William Blake (1910)", "G. K. Chesterton"),
    "chesterton-winewater":    (35115, "Wine, Water, and Song (1915)", "G. K. Chesterton"),
}
for _slug, (_gid, _t, _a) in CHESTERTON_GUTENBERG.items():
    GUTENBERG_EXTRA[_slug] = _gid

UA = {"User-Agent": "Canon-Corpus/0.1 (personal library research)"}

def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        return "skip"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    if len(data) < 1000:
        raise RuntimeError(f"suspiciously small ({len(data)} bytes): {url}")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    return f"{len(data):,} bytes"

def fetch_lexicon(url, dest):
    """Same as fetch(), but a .zip source is unpacked to `dest` — the BDB
    ships zipped and its inner filename is not stable enough to rely on, so
    take the single largest member."""
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        return "skip"
    if not url.endswith(".zip"):
        return fetch(url, dest)
    import io, zipfile
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        blob = r.read()
    zf = zipfile.ZipFile(io.BytesIO(blob))
    members = [m for m in zf.infolist()
               if not m.is_dir() and "__MACOSX" not in m.filename]
    if not members:
        raise RuntimeError(f"no usable member in {url}")
    biggest = max(members, key=lambda m: m.file_size)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(zf.read(biggest))
    return f"{biggest.file_size:,} bytes (unzipped {biggest.filename})"


def main():
    if "--list" in sys.argv:
        for slug, (repo, path, note) in PERSEUS.items():
            print(f"perseus/{slug}: {note}")
        for slug, (path, note) in FIRST1K.items():
            print(f"first1k/{slug}: {note}")
        for slug, (path, note) in CSEL.items():
            print(f"csel/{slug}: {note}")
        for slug, (author, work, note) in CCEL.items():
            print(f"ccel/{slug}: {note}")
        for slug, (url, fn, note) in LEXICONS.items():
            print(f"lexicon/{slug}: {note}")
        for slug, gid in GUTENBERG_EXTRA.items():
            print(f"gutenberg/{slug}: pg{gid}")
        return
    failures = []
    for slug, (repo, path, note) in PERSEUS.items():
        dest = os.path.join(CORPUS, "perseus", slug + ".xml")
        try:
            print(f"perseus/{slug}: {fetch(RAW.format(repo=repo, path=path), dest)}")
        except Exception as e:
            failures.append(slug); print(f"perseus/{slug}: FAIL {e}")
        time.sleep(0.5)
    for slug, (path, note) in FIRST1K.items():
        dest = os.path.join(CORPUS, "first1k", slug + ".xml")
        try:
            print(f"first1k/{slug}: {fetch(F1K_RAW.format(path=path), dest)}")
        except Exception as e:
            failures.append(slug); print(f"first1k/{slug}: FAIL {e}")
        time.sleep(0.5)
    for slug, (path, note) in CSEL.items():
        dest = os.path.join(CORPUS, "csel", slug + ".xml")
        try:
            print(f"csel/{slug}: {fetch(CSEL_RAW.format(path=path), dest)}")
        except Exception as e:
            failures.append(slug); print(f"csel/{slug}: FAIL {e}")
        time.sleep(0.5)
    for slug, (author, work, note) in CCEL.items():
        dest = os.path.join(CORPUS, "ccel", slug + ".xml")
        url = CCEL_XML.format(initial=author[0], author=author, work=work)
        try:
            print(f"ccel/{slug}: {fetch(url, dest)}")
        except Exception as e:
            failures.append(slug); print(f"ccel/{slug}: FAIL {e}")
        time.sleep(1.0)   # be polite to CCEL
    for slug, gid in GUTENBERG_EXTRA.items():
        dest = os.path.join(CORPUS, slug + ".txt")
        try:
            print(f"gutenberg/{slug}: {fetch(GUTENBERG_TXT.format(id=gid), dest)}")
        except Exception as e:
            failures.append(slug); print(f"gutenberg/{slug}: FAIL {e}")
        time.sleep(0.5)
    for slug, (url, fn, note) in LEXICONS.items():
        dest = os.path.join(CORPUS, "lexicons", fn)
        try:
            print(f"lexicon/{slug}: {fetch_lexicon(url, dest)}")
        except Exception as e:
            failures.append(slug); print(f"lexicon/{slug}: FAIL {e}")
        time.sleep(0.5)
    print("DONE" + (f" ({len(failures)} failures: {failures})" if failures else " — all fetched/present"))

if __name__ == "__main__":
    main()
