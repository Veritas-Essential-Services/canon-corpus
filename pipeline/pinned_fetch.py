#!/usr/bin/env python3
"""Fetch pinned files from a GitHub repo at a pinned commit, sha256-checked.

Shared by build_nt_corpus.py and build_versification.py (whose WLC the Hebrew
OT reads). Two routes to the same bytes:

- raw.githubusercontent.com, one request per file. Fine for a handful, but it
  rate-limits a bulk fetch (HTTP 429 after a few dozen files, seen 2026-10-02).
  Retries back off and honour Retry-After.
- a shallow, blobless git fetch of the pinned commit, then `git show
  <commit>:<path>`, which pulls just the blobs named (a repo like First1KGreek
  is gigabytes; the files wanted are megabytes). Not rate-limited like raw. Used whenever a repo has more than
  RAW_LIMIT files missing, and as the fallback when raw gives up.

Either way a file is written only if its sha256 is the pinned one (temp file +
rename), so a killed or poisoned fetch never leaves a bad input behind.
"""
import hashlib
import os
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

RAW = "https://raw.githubusercontent.com/{repo}/{commit}/{rel}"
GIT = "https://github.com/{repo}.git"
RAW_LIMIT = 3
BACKOFF = (2, 4, 8, 16, 32)


def sha256_bytes(blob):
    return hashlib.sha256(blob).hexdigest()


def sha256_file(path):
    with open(path, "rb") as f:
        return sha256_bytes(f.read())


def _get(url, ua="canon-corpus/pinned-fetch"):
    """GET with backoff on 429, 5xx and network errors; raises after the last try."""
    for i, wait in enumerate(BACKOFF + (None,)):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if wait is None or not (e.code == 429 or e.code >= 500):
                raise
            ra = e.headers.get("Retry-After") if e.headers else None
            wait = min(int(ra), 60) if ra and ra.isdigit() else wait
        except urllib.error.URLError:
            if wait is None:
                raise
        time.sleep(wait)


def _write(path, blob, want, label):
    got = sha256_bytes(blob)
    if got != want:
        raise SystemExit(f"HARD STOP: {label} sha256 {got} != pinned {want}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "wb") as f:
        f.write(blob)
    os.replace(path + ".tmp", path)


def _via_git(repo, commit, items, quiet):
    tmp = tempfile.mkdtemp(prefix="pinned-")
    try:
        run = lambda *a: subprocess.run(["git", "-C", tmp, *a], check=True,  # noqa: E731
                                        capture_output=True)
        run("init", "-q")
        run("remote", "add", "origin", GIT.format(repo=repo))
        if not quiet:
            print(f"  git fetch {repo}@{commit[:12]} ({len(items)} files)")
        run("fetch", "-q", "--depth", "1", "--filter=blob:none", "origin", commit)
        # One request for every blob wanted; `git show` would fetch them one by one.
        oids = [run("rev-parse", f"{commit}:{rel}").stdout.decode().strip() for rel, _, _ in items]
        run("-c", "fetch.negotiationAlgorithm=noop", "fetch", "-q", "--no-tags",
            "--no-write-fetch-head", "--filter=blob:none", "origin", *oids)
        for rel, path, want in items:
            blob = run("show", f"{commit}:{rel}").stdout
            _write(path, blob, want, rel)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def fetch(repo, commit, items, quiet=False, ua="canon-corpus/pinned-fetch"):
    """items: [(rel, dest_path, sha256 or None)]. Fetches what is missing or
    changed. A None sha256 (an unpinned survey file) is accepted as served."""
    todo = [(rel, p, w) for rel, p, w in items
            if not (os.path.exists(p) and (w is None or sha256_file(p) == w))]
    if not todo:
        return 0
    pinned = [t for t in todo if t[2] is not None]
    if len(pinned) > RAW_LIMIT:
        _via_git(repo, commit, pinned, quiet)
        todo = [t for t in todo if t[2] is None]
    failed = []
    for rel, path, want in todo:
        if not quiet:
            print(f"  fetch {rel}")
        try:
            blob = _get(RAW.format(repo=repo, commit=commit, rel=urllib.request.quote(rel)), ua)
        except (urllib.error.URLError, OSError):
            if want is None:
                raise
            failed.append((rel, path, want))
            continue
        if want is None:
            _write(path, blob, sha256_bytes(blob), rel)
        else:
            _write(path, blob, want, rel)
    if failed:
        _via_git(repo, commit, failed, quiet)
    return len(todo) + len(pinned)
