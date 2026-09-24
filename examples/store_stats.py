#!/usr/bin/env python3
"""Measure the shape of one Apify store capture, and what moved since the archive.

    python3 store_stats.py [--out stats.json]

Reads this repo's own raw captures, and the single Internet Archive memento of
the store API (2026-08-18) as the only available before-picture. Every number
the charts draw comes from here.
"""
from __future__ import annotations
import argparse, collections, gzip, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve()
REPO = HERE.parents[1]
SCRATCH = pathlib.Path("/tmp/claude-1000/-home-david-Desktop-programming-web-snapshots"
                       "/7e6169e6-34c2-4d59-be3a-6b67706ec03f/scratchpad")


def partition(url: str) -> str:
    if "category=" in url: return url.split("category=", 1)[1].split("&", 1)[0]
    if "sortBy=" in url:   return "sort:" + url.split("sortBy=", 1)[1].split("&", 1)[0]
    return "ALL"


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="")
    a = ap.parse_args()

    import csv
    man = []
    for f in (REPO / "manifest").glob("*/*.csv"):
        man += list(csv.DictReader(open(f)))
    by_part = collections.defaultdict(lambda: {"pages": 0, "rows": 0, "max_offset": 0})
    actors, first_seen = {}, {}
    for r in man:
        if r["outcome"] not in ("first_capture", "changed"): continue
        p = partition(r["url"]); off = int(r["url"].split("offset=", 1)[1].split("&", 1)[0])
        items = json.loads(gzip.decompress(open(r["raw_ref"], "rb").read()))["data"]["items"]
        d = by_part[p]; d["pages"] += 1; d["rows"] += len(items); d["max_offset"] = max(d["max_offset"], off)
        for x in items:
            actors.setdefault(x["id"], x)
            first_seen.setdefault(x["id"], set()).add(p)

    u30 = sorted((x.get("stats") or {}).get("totalUsers30Days") or 0 for x in actors.values())
    n = len(u30); tot = sum(u30)
    lorenz = []
    run = 0
    for i, v in enumerate(u30, 1):
        run += v
        if i % max(1, n // 200) == 0 or i == n:
            lorenz.append([round(i / n, 5), round(run / max(1, tot), 5)])

    # duplicated fields that are not duplicates
    dup = {}
    for top in ("actorReviewRating", "actorReviewCount", "bookmarkCount"):
        same = sum(1 for x in actors.values() if x.get(top) == (x.get("stats") or {}).get(top))
        dup[top] = {"same": same, "n": len(actors)}

    # FIELD VOLATILITY MUST BE MEASURED ON UNPROJECTED BYTES, BOTH SIDES.
    #
    # The first version compared the archive memento against THIS REPO'S captures
    # -- which are projected, so userPictureUrl/pictureUrl/url are absent from
    # the new side. They came out as "changed on 100% of actors, 0.01% of the
    # payload" and landed in the opposite corner of the chart from the truth
    # (20.1% / 7.3%). Comparing a full record against a deliberately trimmed one
    # measures the trim, not the publisher.
    #
    # So the live side is fetched fresh and unprojected here, one page, matching
    # the memento's own offset=0 slice.
    old_p = SCRATCH / "apify_memento_20260818.json.gz"
    vol = {}
    if old_p.exists():
        import socket, urllib.request
        _o = socket.getaddrinfo
        socket.getaddrinfo = lambda h, p_, f=0, t=0, pr=0, fl=0: _o(h, p_, socket.AF_INET, t, pr, fl)
        UA = "wss-screening/0.1 (+https://github.com/q3dresearch/wss-apify; archival research)"
        live = urllib.request.urlopen(urllib.request.Request(
            "https://api.apify.com/v2/store?limit=1000&offset=0",
            headers={"User-Agent": UA}), timeout=180).read()
        fresh = {x["id"]: x for x in json.loads(live)["data"]["items"]}
        old = {x["id"]: x for x in json.loads(gzip.decompress(old_p.read_bytes()))}
        actors_v = fresh
        both = set(old) & set(fresh)
        def flat(x):
            o = {}
            for k, v in x.items():
                if isinstance(v, dict) and k in ("stats", "currentPricingInfo"):
                    for k2, v2 in v.items(): o[f"{k}.{k2}"] = json.dumps(v2, separators=(",", ":"))
                else: o[k] = json.dumps(v, separators=(",", ":"))
            return o
        chg, seen, size = collections.Counter(), collections.Counter(), collections.Counter()
        for i in both:
            o, nw = flat(old[i]), flat(actors_v[i])
            for k in set(o) | set(nw):
                seen[k] += 1; size[k] += len(nw.get(k, ""))
                if o.get(k) != nw.get(k): chg[k] += 1
        s = sum(size.values())
        vol = {k: {"rate": round(100 * chg[k] / max(1, seen[k]), 2),
                   "share": round(100 * size[k] / max(1, s), 3),
                   "n": seen[k]} for k in size}
        vol_overlap = len(both)
    else:
        vol_overlap = 0

    stats = {
        "actors": len(actors),
        "endpoints": len(man),
        "partitions": {k: v for k, v in sorted(by_part.items(), key=lambda kv: -kv[1]["rows"])},
        "u30_bands": {lab: sum(1 for v in u30 if lo <= v <= hi) for lo, hi, lab in
                      ((0, 0, "0"), (1, 1, "1"), (2, 4, "2-4"), (5, 9, "5-9"),
                       (10, 49, "10-49"), (50, 199, "50-199"), (200, 10**9, "200+"))},
        "u30_median": u30[n // 2], "u30_max": u30[-1], "u30_total": tot,
        "top1pct_share": round(100 * sum(u30[-max(1, n // 100):]) / max(1, tot), 1),
        "lorenz": lorenz,
        "dup_fields": dup,
        "volatility": vol, "volatility_overlap": vol_overlap,
        "partitions_in_one_only": sum(1 for v in first_seen.values() if len(v) == 1),
    }
    txt = json.dumps(stats, indent=1, sort_keys=True)
    if a.out: pathlib.Path(a.out).write_text(txt)
    print(f"  actors {stats['actors']:,}  endpoints {stats['endpoints']}  partitions {len(by_part)}")
    print(f"  u30 median {stats['u30_median']}  max {stats['u30_max']:,}  top1% share {stats['top1pct_share']}%")
    print(f"  bands {stats['u30_bands']}")
    print(f"  volatility fields {len(vol)} over {vol_overlap} overlapping actors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
