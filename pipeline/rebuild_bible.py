#!/usr/bin/env python3
"""Rebuild the Greek NT (data/nt/) and the Hebrew OT (data/ot/) from their
pinned sources, timed, and prove the result is the published data.

    python3 pipeline/rebuild_bible.py           # fetch what is missing, build, write, --check
    python3 pipeline/rebuild_bible.py --verify  # fetch, rebuild in memory, compare; writes nothing

Every input is a file at a pinned commit with a pinned sha256 (nt_pins.json,
build_versification.WLC_PINS), fetched into data/corpus/ (gitignored). The
check compares against data/<nt|ot>/manifest.json, which is committed whatever
the layout and carries every shard's sha256, so `--verify` works in a checkout
where the shards themselves are not committed.

Each step runs as its own process, so a failure names the step that failed,
and a killed run leaves every file it already wrote whole (both builds write
temp file + rename, the manifest last).
"""
import argparse
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def step(label, *args):
    t = time.monotonic()
    print(f"== {label}", flush=True)
    r = subprocess.run([sys.executable, *args], cwd=ROOT)
    dt = time.monotonic() - t
    if r.returncode:
        raise SystemExit(f"FAILED: {label} (exit {r.returncode}, {dt:.0f} s)")
    return label, dt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true",
                    help="rebuild in memory and compare with the manifests; write nothing")
    a = ap.parse_args()
    nt, ot = os.path.join(HERE, "build_nt_corpus.py"), os.path.join(HERE, "build_ot_corpus.py")
    times = []
    if a.verify:
        times.append(step("NT: fetch + verify", nt, "--fetch", "--check"))
        times.append(step("OT: fetch + verify", ot, "--fetch", "--check"))
    else:
        times.append(step("NT: fetch + build", nt, "--fetch"))
        times.append(step("OT: fetch + build", ot, "--fetch"))
        times.append(step("NT: --check", nt, "--check"))
        times.append(step("OT: --check", ot, "--check"))
    print("\n  step                     seconds")
    for label, dt in times:
        print(f"  {label:<24}{dt:>8.0f}")
    print(f"  {'total':<24}{sum(dt for _, dt in times):>8.0f}")


if __name__ == "__main__":
    main()
