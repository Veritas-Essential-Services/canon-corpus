"""Check every IIIF link in data/art/catalog.json and record what was found.

For each source with an `iiif` URL this opens the manifest (IIIF v2 or v3) or
image-service info.json and writes back, on that source:

  iiif_check: {"status": "ok" | "http-404" | "unreachable" | ...,
               "checked": "<date>", "canvases": n, "max_px": [w, h]}

A link that cannot be reached is never deleted: "unreachable" means this run
could not open it, not that it is wrong. Resumable: sources already marked ok
are skipped unless --recheck.

    python3 pipeline/verify_illustrations.py            # check unchecked links
    python3 pipeline/verify_illustrations.py --recheck  # check everything again
    python3 pipeline/verify_illustrations.py --report   # print the tally only
"""
import argparse
import collections
import datetime
import json
import os
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, "..", "data", "art", "catalog.json")
UA = "WordHoard-catalog-check/1.0 (art appreciation module; polite single requests)"


def fetch_json(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json, application/ld+json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def canvases(m):
    """Canvases of a v2 or v3 manifest, as (w, h) pairs."""
    out = []
    if "items" in m:  # v3
        for c in m["items"]:
            if c.get("type") == "Canvas":
                out.append((c.get("width") or 0, c.get("height") or 0))
    for seq in m.get("sequences", []):  # v2
        for c in seq.get("canvases", []):
            out.append((c.get("width") or 0, c.get("height") or 0))
    return out


def loc_json_url(url):
    """LoC's manifest.json sits behind a bot wall; its ?fo=json API does not."""
    base = url.split("manifest.json")[0].rstrip("/") + "/"
    return base + "?fo=json"


def check_loc(url):
    """Read a loc.gov item or resource through the JSON API: page count, the
    IIIF image service of the first page that has one, and the largest file."""
    try:
        req = urllib.request.Request(loc_json_url(url), headers={"User-Agent": UA, "Accept-Encoding": "identity"})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"status": f"http-{e.code}"}
    except Exception as e:  # noqa: BLE001
        return {"status": "unreachable", "error": type(e).__name__}
    files = []
    for res in d.get("resources", []):
        for page in res.get("files", []):
            files.append(page)
    for f in d.get("page", []) if isinstance(d.get("page"), list) else []:
        files.append([f])
    services, biggest = [], None
    for page in files:
        for f in page:
            if f.get("info"):
                services.append(f["info"].replace("/info.json", ""))
            if f.get("size") and (biggest is None or f["size"] > biggest["size"]):
                biggest = f
    out = {"status": "ok" if files else "no-files", "kind": "loc-json", "canvases": len(files)}
    if services:
        out["iiif_service"] = services[0]
    if biggest:
        out["largest_file"] = {"url": biggest["url"], "bytes": biggest["size"], "mime": biggest.get("mimetype")}
        if biggest.get("width") and str(biggest["width"]) != "0":
            out["max_px"] = [int(biggest["width"]), int(biggest["height"])]
    return out


def check(url):
    if urlparse(url).netloc == "www.loc.gov":
        return check_loc(url)
    try:
        m = fetch_json(url)
    except urllib.error.HTTPError as e:
        return {"status": f"http-{e.code}"}
    except ValueError:
        return {"status": "ok", "kind": "image"}  # an image, not JSON: the Met serves the file itself
    except Exception as e:  # noqa: BLE001 -- network: record and move on
        return {"status": "unreachable", "error": type(e).__name__}
    if "width" in m and "height" in m and ("profile" in m or "protocol" in m):  # info.json
        return {"status": "ok", "kind": "image-service", "canvases": 1, "max_px": [m["width"], m["height"]]}
    cs = canvases(m)
    if not cs:
        return {"status": "no-canvases", "kind": "manifest"}
    big = max(cs, key=lambda wh: wh[0] * wh[1])
    return {"status": "ok", "kind": "manifest", "canvases": len(cs), "max_px": list(big)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recheck", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--host", help="only check IIIF URLs on this host")
    args = ap.parse_args()
    cat = json.load(open(CATALOG, encoding="utf-8"))
    today = datetime.date.today().isoformat()
    tally = collections.Counter()
    for a in cat:
        for w in a["works"]:
            for s in w["sources"]:
                url = s.get("iiif")
                if not url:
                    continue
                host = urlparse(url).netloc
                prev = s.get("iiif_check", {})
                if not args.report and (args.recheck or prev.get("status") != "ok") and (not args.host or args.host == host):
                    res = check(url)
                    res["checked"] = today
                    s["iiif_check"] = res
                    time.sleep(4 if host == "www.loc.gov" else 0.3)  # LoC bans fast clients
                tally[(host, s.get("iiif_check", {}).get("status", "unchecked"))] += 1
            if not args.report:
                tmp = CATALOG + ".tmp"
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(cat, f, ensure_ascii=False, indent=1)
                    f.write("\n")
                os.replace(tmp, CATALOG)
    for (host, st), n in sorted(tally.items()):
        print(f"{n:4d}  {st:12s}  {host}")


if __name__ == "__main__":
    main()
