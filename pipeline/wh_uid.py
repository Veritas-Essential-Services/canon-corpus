#!/usr/bin/env python3
"""
wh_uid.py -- the Word Hoard identity layer.

DESIGN (vault: `9 - Projects/Canon OS/DESIGN - Stable UIDs for Word Hoard
(2026-09-17).md`; house style: `HOUSE STYLE - Addressing and Identity`)

    uid        wh-K7M9X2P4RT        the IDENTITY. Immutable. Never reused.
    citation   kjv:Gen.1.2          the ADDRESS. Human-readable. May change.
    witness    wh-K7M9X2P4RT/kjv.italic
    span       wh-K7M9X2P4RT/kjv.italic@120-134      (reserved; parsed, unused)

THE SPLIT THIS MODULE EXISTS TO ENFORCE
    One string was doing two jobs and could do neither well. A citation is a
    promise about WHERE TO LOOK; a uid is a promise about WHAT YOU WILL FIND.
    canon-corpus's `<slug>:<path>` was always the citation. Nothing about it
    changes. The uid is new and sits beside it.

WHY NOTHING IN THE UID DERIVES FROM THE TEXT OR THE PATH
    Measured 2026-09-17 in this repo: data/books/ held two KJV files whose
    SHARED ids disagreed about the text 15,087 times (49.2%), and 1,872 times
    (6.1%) even after stripping the italic brackets. `kjv:Gen.1.2` named two
    different strings. A path-derived id moves when the parse is fixed; a
    content hash moves when a typo is. Neither can survive an edit, and the
    corpus gets edited.

WHY THERE IS NO KIND LETTER IN THE UID
    An earlier draft proposed wh-u- / wh-w- / wh-n- for passage / work / note.
    Dropped, and the reason is code-corpus's own scar (build/uid.py, the
    UidRegistry docstring): it once had node_type in the natural key, so
    RE-TYPING a node minted a fresh uid and orphaned every record pointing at
    the old one -- with the build still passing. Putting the kind in the
    IDENTITY reproduces that bug for the sake of readability. Kind is a field
    on the record. The uid is opaque and says nothing.

WHY 10 CHARACTERS AND NOT code-corpus's 6
    code-corpus scopes uniqueness per book -- a few thousand ids per space, and
    32^6 is ample. The Word Hoard uses ONE global space so that a passage, a
    note and a work can never collide and one registry is the single home for
    the fact. At 223,320 canon units, 32^6 would expect ~23 birthday collisions;
    32^10 (1.13e15) expects ~0.0004 at a million ids. The mint loop rejects
    collisions either way; the width is so the space is not tight as it grows.

RELATION TO code-corpus/build/uid.py -- DELIBERATELY SEPARATE
    Same alphabet, same registry discipline, same frozen gate, DIFFERENT id
    space and a different registry file. A code uid carries its EDITION
    (asme-a17.1-2016-4K7M9X) because a finding must say which edition of the
    code it cites. Word Hoard content has no editions in that sense -- it has
    REVISIONS (maxims, ruled 2026-09-05: a rewording is a new record with
    `revision: n+1` and `supersedes`). Forcing a hymn into an "edition" slot
    would either leave it empty everywhere or quietly redefine it, and the
    moment it means two things the glob `asme-a17.1-*-4K7M9X` that makes the
    code scheme worth having stops being trustworthy.

    NOT a shared import: the two repos have no shared packaging, and a git
    submodule or a pip package for eighty lines is worse than the duplication.
    Instead `tests/wh_uid_test.py` PINS the shared constants and fails loudly
    if they drift. That is an honest copy, not a silent one.
"""

import json
import os
import re
import secrets

# ---------------------------------------------------------------------------
# Grammar
# ---------------------------------------------------------------------------
# Crockford Base32: no I, L, O or U, so nothing is misread aloud or mistyped
# off a screen. An audiobook product is downstream of this corpus; the choice
# is not decoration. MUST match code-corpus/build/uid.py -- pinned by test.

ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
PREFIX = "wh"
CONCEPT_LEN = 10

CONCEPT_RE = re.compile(rf"^[{ALPHABET}]{{{CONCEPT_LEN}}}$")
UID_RE = re.compile(rf"^{PREFIX}-(?P<concept>[{ALPHABET}]{{{CONCEPT_LEN}}})$")

# <uid>[/<witness>[@<start>-<end>]]
ADDRESS_RE = re.compile(
    rf"^(?P<uid>{PREFIX}-[{ALPHABET}]{{{CONCEPT_LEN}}})"
    r"(?:/(?P<witness>[a-z0-9][a-z0-9._\-]*))?"
    r"(?:@(?P<start>\d+)-(?P<end>\d+))?$"
)

# Crockford's canonical read-alike folding, for input typed or dictated.
_FOLD = str.maketrans({"I": "1", "i": "1", "L": "1", "l": "1",
                       "O": "0", "o": "0", "U": "V", "u": "V"})

# Kinds are recorded ON THE RECORD, never in the uid. Listed here so a
# consumer can validate the field; adding one mints nothing and breaks nothing.
KINDS = ("work", "passage", "note", "witness", "annotation")


class WhUidError(ValueError):
    pass


# ---------------------------------------------------------------------------
# Minting and parsing
# ---------------------------------------------------------------------------

def new_concept(taken=()):
    """Mint an unused concept. Global uniqueness is the registry's job."""
    taken = set(taken)
    for _ in range(100_000):
        c = "".join(secrets.choice(ALPHABET) for _ in range(CONCEPT_LEN))
        if c not in taken:
            return c
    raise WhUidError("concept space exhausted -- widen CONCEPT_LEN")


def format_uid(concept):
    if not CONCEPT_RE.match(concept):
        raise WhUidError(f"bad concept {concept!r}")
    return f"{PREFIX}-{concept}"


def parse_uid(uid):
    m = UID_RE.match(uid or "")
    if not m:
        raise WhUidError(f"malformed uid {uid!r}")
    return {"concept": m.group("concept")}


def is_uid(s):
    return bool(UID_RE.match(s or ""))


def normalize_uid(s):
    """Fold Crockford read-alikes in the concept only. For human input."""
    s = (s or "").strip()
    i = s.rfind("-")
    if i < 0:
        return s
    return s[:i + 1] + s[i + 1:].translate(_FOLD).upper()


# ---------------------------------------------------------------------------
# Addressing: uid + witness + span
# ---------------------------------------------------------------------------

def address(uid, witness=None, start=None, end=None):
    """Build an address. `uid` alone is the passage; adding a witness names one
    rendering of it; adding a span names a clause inside that rendering.

    The span form is RESERVED, not yet produced by anything. It is the
    primitive the Rooms note names -- "a unit id plus, where needed, an
    offset" -- and it is what scripture-echo detection needs before it can
    point at a clause instead of quoting one. Implemented here so the grammar
    is settled before there is data to migrate."""
    parse_uid(uid)
    if witness is None:
        if start is not None or end is not None:
            raise WhUidError("a span needs a witness -- offsets are into a rendering")
        return uid
    if not re.match(r"^[a-z0-9][a-z0-9._\-]*$", witness):
        raise WhUidError(f"bad witness name {witness!r} (lowercase, dots, dashes)")
    out = f"{uid}/{witness}"
    if start is None and end is None:
        return out
    if start is None or end is None:
        raise WhUidError("a span needs both start and end")
    start, end = int(start), int(end)
    if start < 0 or end < start:
        raise WhUidError(f"bad span {start}-{end}")
    return f"{out}@{start}-{end}"


def parse_address(s):
    """-> {uid, witness, start, end}. witness/start/end are None when absent."""
    m = ADDRESS_RE.match((s or "").strip())
    if not m:
        raise WhUidError(f"not an address: {s!r}")
    d = m.groupdict()
    if d["witness"] is None and d["start"] is not None:
        raise WhUidError(f"span without a witness: {s!r}")
    return {"uid": d["uid"], "witness": d["witness"],
            "start": int(d["start"]) if d["start"] is not None else None,
            "end": int(d["end"]) if d["end"] is not None else None}


# ---------------------------------------------------------------------------
# Citations -- unchanged, and deliberately not validated hard
# ---------------------------------------------------------------------------

CITATION_RE = re.compile(r"^(?P<slug>[a-z0-9][a-z0-9.\-]*):(?P<path>.+)$")


def parse_citation(citation):
    """Read `kjv:Gen.1.2` into its parts. Kept loose on purpose: the citation
    is the layer that is ALLOWED to vary, and every converter in this repo has
    its own path grammar (OSIS, act.scene.line, entry numbers). Tightening this
    would make the mutable layer brittle, which is backwards."""
    m = CITATION_RE.match((citation or "").strip())
    if not m:
        raise WhUidError(f"not a citation: {citation!r}")
    return {"slug": m.group("slug"), "path": m.group("path")}


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

class WhUidRegistry:
    """citation -> uid, persisted, plus the tombstone record.

    NATURAL KEY: the citation string itself (`kjv:Gen.1.2`).

    Kind is NOT in the key -- see the module docstring. A work (`kjv`) and a
    passage (`kjv:Gen.1.1`) already have different citations, so the key
    separates them without help, and re-typing a record cannot orphan it.

    A uid is IMMUTABLE and is NEVER REUSED. A citation that goes away leaves
    its uid in the map; a citation that comes back gets the same uid. That is
    the whole point and it is why `save()` never drops keys.
    """

    NOTE = ("Word Hoard identity. uids are immutable and never reused. A uid "
            "that changes across builds is a bug. COMMIT THIS FILE -- it is the "
            "single home for this class of fact, and losing it silently "
            "renames every identifier in the Word Hoard. Natural key is the "
            "citation string; kind is NOT part of it.")
    SCHEME = "wordhoard/uid/v1"

    def __init__(self, path=None, frozen=False):
        self.path = path
        self.frozen = frozen
        self.map = {}          # citation -> uid
        self.superseded = {}   # old uid -> new uid          (a rewording/replacement)
        self.split = {}        # parent uid -> [child uids]  (parent keeps largest child)
        self.merged = {}       # new uid -> [source uids]
        self.minted = 0
        self.reused = 0
        self._concepts = set()
        if path and os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                d = json.load(f)
            self.map = d.get("uids", {})
            self.superseded = d.get("superseded", {})
            self.split = d.get("split", {})
            self.merged = d.get("merged", {})
            for u in self.map.values():
                try:
                    self._concepts.add(parse_uid(u)["concept"])
                except WhUidError:
                    continue
            for group in (self.superseded, self.merged, self.split):
                for k, v in group.items():
                    for u in ([k] + (v if isinstance(v, list) else [v])):
                        try:
                            self._concepts.add(parse_uid(u)["concept"])
                        except WhUidError:
                            pass

    # -- minting ------------------------------------------------------------

    def uid_for(self, citation):
        """The uid for a citation, minting once and reusing forever after."""
        parse_citation(citation)
        if citation in self.map:
            self.reused += 1
            return self.map[citation]
        if self.frozen:
            raise WhUidError(
                f"FROZEN: refusing to mint a uid for {citation!r}. This build is "
                f"tagged released; new content requires an explicit unfreeze.")
        c = new_concept(self._concepts)
        self._concepts.add(c)
        u = format_uid(c)
        self.map[citation] = u
        self.minted += 1
        return u

    def mint_free(self):
        """A uid with no citation -- for a merge result, or a note that has no
        citation grammar. Recorded in _concepts so it can never be re-minted."""
        if self.frozen:
            raise WhUidError("FROZEN: refusing to mint")
        c = new_concept(self._concepts)
        self._concepts.add(c)
        self.minted += 1
        return format_uid(c)

    # -- the events that naive schemes cannot survive -----------------------

    def record_split(self, parent_uid, child_uids):
        """The parent uid STAYS on the largest child. Every other child minted
        separately and is recorded here. Nothing is deleted."""
        parse_uid(parent_uid)
        for c in child_uids:
            parse_uid(c)
        if parent_uid not in child_uids:
            raise WhUidError(
                "the parent uid must be one of the children -- it stays on the "
                "largest. Splitting without keeping it orphans every inbound pointer.")
        self.split.setdefault(parent_uid, [])
        for c in child_uids:
            if c not in self.split[parent_uid]:
                self.split[parent_uid].append(c)

    def record_merge(self, new_uid, source_uids):
        """A merge mints. Sources become tombstones pointing forward."""
        parse_uid(new_uid)
        for s in source_uids:
            parse_uid(s)
            if s == new_uid:
                raise WhUidError("a merge result must be a fresh uid, not a source")
            self.superseded[s] = new_uid
        self.merged.setdefault(new_uid, [])
        for s in source_uids:
            if s not in self.merged[new_uid]:
                self.merged[new_uid].append(s)

    def record_supersede(self, old_uid, new_uid):
        """A rewording. The maxims rule, 2026-09-05: never overwrite -- a new
        record with revision n+1, and the old one keeps its uid and its date."""
        parse_uid(old_uid)
        parse_uid(new_uid)
        if old_uid == new_uid:
            raise WhUidError("a uid cannot supersede itself")
        self.superseded[old_uid] = new_uid

    def resolve(self, uid, _seen=None):
        """Follow tombstones forward to the uid in force today. A uid that was
        split resolves to ITSELF (the parent kept it); callers wanting the
        siblings ask `self.split`."""
        parse_uid(uid)
        _seen = _seen or set()
        while uid in self.superseded:
            if uid in _seen:
                raise WhUidError(f"supersede cycle at {uid}")
            _seen.add(uid)
            uid = self.superseded[uid]
        return uid

    # -- gates and persistence ----------------------------------------------

    def assert_frozen_ok(self):
        if self.frozen and self.minted:
            raise WhUidError(
                f"FROZEN build minted {self.minted} uids -- identity drift")

    def assert_no_mint(self):
        """The production gate. A rebuild of existing content must mint ZERO.
        Anything else means content is genuinely new -- or the registry was not
        loaded, which is the failure mode that silently renames the world."""
        if self.minted:
            raise WhUidError(
                f"expected 0 minted, got {self.minted}. Either this content is "
                f"new, or --uid-registry pointed at the wrong file.")

    def stats(self):
        return {"total": len(self.map), "minted": self.minted,
                "reused": self.reused, "superseded": len(self.superseded),
                "split": len(self.split), "merged": len(self.merged)}

    def save(self):
        if not self.path:
            return
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        payload = {"note": self.NOTE, "scheme": self.SCHEME, "uids": self.map}
        for k, v in (("superseded", self.superseded), ("split", self.split),
                     ("merged", self.merged)):
            if v:
                payload[k] = v
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, indent=1, sort_keys=True)
        os.replace(tmp, self.path)   # atomic; a killed run never truncates
