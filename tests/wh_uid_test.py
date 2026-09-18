#!/usr/bin/env python3
"""Offline tests for the Word Hoard identity layer. No network, no corpus.
Run:  python3 tests/wh_uid_test.py

Same shape as tests/structure_test.py -- inline fixtures, ok/FAIL lines, a
non-zero exit on any failure.

Two of these checks are not really tests of this module. `pin_*` asserts that
the constants shared with code-corpus/build/uid.py have not drifted, because
the two repos have no shared packaging and the copy is deliberate (see the
wh_uid docstring). If code-corpus ever changes its alphabet, this fails and
somebody has to make a decision instead of discovering it later.
"""
import os, sys, tempfile, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.join(HERE, "..", "pipeline")


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(PIPE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


U = load("wh_uid")

PASS = 0
FAIL = []


def check(label, cond):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label)


def raises(fn, *a, **k):
    try:
        fn(*a, **k)
    except U.WhUidError:
        return True
    except Exception:
        return False
    return False


# ------------------------------------------------------------------ grammar
c = U.new_concept()
uid = U.format_uid(c)
check("mint produces a parseable uid", U.is_uid(uid))
check("uid carries the wh- prefix", uid.startswith("wh-"))
check("concept is 10 chars", len(c) == 10)
check("alphabet excludes I, L, O, U", not (set("ILOU") & set(U.ALPHABET)))
check("pin_alphabet matches code-corpus", U.ALPHABET == "0123456789ABCDEFGHJKMNPQRSTVWXYZ")
check("pin_prefix", U.PREFIX == "wh")
check("no kind letter in the uid", U.parse_uid(uid) == {"concept": c})
check("malformed uid raises", raises(U.parse_uid, "wh-notvalid!"))
check("a code-corpus uid is NOT a wh uid", not U.is_uid("asme-a17.1-2016-4K7M9X"))
check("uniqueness: 2000 mints, no repeat",
      len({U.new_concept() for _ in range(2000)}) == 2000)
check("mint avoids taken concepts", U.new_concept(taken={c}) != c)
check("normalize folds read-alikes", U.normalize_uid("wh-k7m9x2p4rl")
      .endswith("K7M9X2P4R1"))

# ---------------------------------------------------------------- addressing
a_pass = U.address(uid)
a_wit = U.address(uid, "kjv.italic")
a_span = U.address(uid, "kjv.italic", 12, 34)
check("bare uid is the passage address", a_pass == uid)
check("witness address", a_wit == uid + "/kjv.italic")
check("span address", a_span == uid + "/kjv.italic@12-34")
check("round trip: passage", U.parse_address(a_pass)["witness"] is None)
check("round trip: witness", U.parse_address(a_wit)["witness"] == "kjv.italic")
r = U.parse_address(a_span)
check("round trip: span offsets", (r["start"], r["end"]) == (12, 34))
check("span without a witness is refused", raises(U.address, uid, None, 1, 2))
check("span with only one bound is refused", raises(U.address, uid, "w", 1, None))
check("reversed span is refused", raises(U.address, uid, "w", 9, 2))
check("uppercase witness name refused", raises(U.address, uid, "KJV"))
check("parsing a span with no witness refused",
      raises(U.parse_address, uid + "@1-2"))

# ----------------------------------------------------------------- citations
check("citation parses", U.parse_citation("kjv:Gen.1.2")
      == {"slug": "kjv", "path": "Gen.1.2"})
check("citation keeps a colon in the path",
      U.parse_citation("shakespeare:hamlet.3.1")["path"] == "hamlet.3.1")
check("a uid is not a citation", raises(U.parse_citation, uid))

# ------------------------------------------------------------------ registry
tmp = tempfile.mkdtemp()
p = os.path.join(tmp, "wordhoard.uids.json")
r1 = U.WhUidRegistry(p)
u1 = r1.uid_for("kjv:Gen.1.1")
u2 = r1.uid_for("kjv:Gen.1.2")
check("distinct citations get distinct uids", u1 != u2)
check("same citation reuses", r1.uid_for("kjv:Gen.1.1") == u1)
check("minted counted once", r1.minted == 2)
check("reused counted", r1.reused == 1)
r1.save()

# THE central property: a rebuild reuses everything.
r2 = U.WhUidRegistry(p)
check("uid survives a reload", r2.uid_for("kjv:Gen.1.1") == u1)
check("reload mints nothing", r2.minted == 0)
check("assert_no_mint passes on a clean rebuild", r2.assert_no_mint() is None)

# The 420-verse case: fixing the parse adds content. Old ids MUST NOT move.
before = dict(r2.map)
u_new = r2.uid_for("kjv:Gen.3.5")
check("new content mints", r2.minted == 1)
check("the fix did not move any existing uid",
      all(r2.map[k] == v for k, v in before.items()))
check("the new uid is distinct", u_new not in before.values())

# Frozen gate
rf = U.WhUidRegistry(p, frozen=True)
check("frozen reuses fine", rf.uid_for("kjv:Gen.1.1") == u1)
check("frozen refuses to mint", raises(rf.uid_for, "kjv:Rev.22.21"))

# ------------------------------------------------------ split / merge / tomb
r3 = U.WhUidRegistry(os.path.join(tmp, "b.json"))
parent = r3.uid_for("hymns:pange-lingua.st1")
child_b = r3.mint_free()
r3.record_split(parent, [parent, child_b])
check("split keeps the parent uid on a child", parent in r3.split[parent])
check("split records the sibling", child_b in r3.split[parent])
check("split refuses to drop the parent",
      raises(r3.record_split, parent, [child_b]))
check("a split uid still resolves to itself", r3.resolve(parent) == parent)

m_a = r3.uid_for("notes:catechetical-layer")
m_b = r3.uid_for("notes:catechetical-layer-v3")
merged = r3.mint_free()
r3.record_merge(merged, [m_a, m_b])
check("merge mints a fresh uid", merged not in (m_a, m_b))
check("merged sources resolve forward", r3.resolve(m_a) == merged)
check("both sources resolve forward", r3.resolve(m_b) == merged)
check("merge refuses a source as its own result",
      raises(r3.record_merge, m_a, [m_a]))
check("a tombstoned uid is never deleted", m_a in r3.superseded)

old = r3.uid_for("maxims:AK-001")
new = r3.mint_free()
r3.record_supersede(old, new)
check("supersede chains resolve", r3.resolve(old) == new)
check("self-supersede refused", raises(r3.record_supersede, new, new))
r3.superseded[new] = old  # deliberately create a cycle
check("supersede cycle is caught, not hung", raises(r3.resolve, old))
del r3.superseded[new]

# Persistence keeps the tombstones.
r3.save()
r4 = U.WhUidRegistry(os.path.join(tmp, "b.json"))
check("tombstones survive a reload", r4.resolve(m_a) == merged)
check("split record survives a reload", child_b in r4.split.get(parent, []))
check("a reloaded registry never re-mints a tombstoned concept",
      U.parse_uid(r4.mint_free())["concept"] not in
      {U.parse_uid(x)["concept"] for x in [m_a, m_b, merged, parent, child_b]})

# Atomic save left no debris.
check("save leaves no .tmp behind",
      not os.path.exists(os.path.join(tmp, "b.json.tmp")))

print()
print(f"{PASS} passed, {len(FAIL)} failed")
if FAIL:
    for f in FAIL:
        print("  FAILED:", f)
    sys.exit(1)
