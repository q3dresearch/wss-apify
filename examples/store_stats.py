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
    ap = argparse.ArgumentParser()
    # Default to a DATED PUBLIC SNAPSHOT. This file is the only thing about the
    # store that git keeps: ~6 KB of bands, Lorenz points, per-partition totals
    # and field volatility, with no actor identity in it. The records it is
    # computed from are in R2 and gitignored, because redistribution rights are
    # not established -- see LICENSE-DATA.
    import datetime as _dt
    ap.add_argument("--out", default=str(REPO / "public" /
                    f"stats-{_dt.date.today().isoformat()}.json"))
    a = ap.parse_args()

    root = REPO
    import csv

    # READ THROUGH THE STORE, NEVER OFF THE FILESYSTEM. This source declares
    # `storage: object`, so raw/ is empty locally and the bytes are in R2. The
    # first version did `open(r["raw_ref"], "rb")` and died with FileNotFoundError
    # the moment storage moved -- the same mistake the sequence warns about when
    # it says never to test for capture by counting raw/ files. `store_for`
    # returns a LocalStore or an ObjectStore depending on the registry, and
    # `read` un-gzips either way.
    sys.path.insert(0, str(REPO.parent / "wss-engine"))
    from wss import registry as _reg, storage as _st
    store = _st.store_for(_reg.load_registry(REPO)[0], REPO)

    man = []
    for f in (REPO / "manifest").glob("*/*.csv"):
        man += list(csv.DictReader(open(f)))
    by_part = collections.defaultdict(lambda: {"pages": 0, "rows": 0, "max_offset": 0})
    actors, first_seen = {}, {}
    for r in man:
        if r["outcome"] not in ("first_capture", "changed"): continue
        p = partition(r["url"]); off = int(r["url"].split("offset=", 1)[1].split("&", 1)[0])
        items = json.loads(store.read(r["raw_ref"]))["data"]["items"]
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

    # FIELD VOLATILITY IS A FROZEN ONE-OFF, READ FROM public/, NOT RECOMPUTED.
    #
    # Two reasons it cannot be recomputed here. Payload share needs fields that
    # `project_drop` already removes from this repo's captures, so measuring it
    # from our own data would measure the trim rather than the publisher. And the
    # only before-picture that exists is a single Internet Archive memento of
    # this endpoint, which is not ours to re-derive on a schedule.
    #
    # The earlier version read that memento from a session scratchpad path --
    # which was cleared, returned zero fields, and would never have existed on a
    # runner at all. Now it reads an aggregate committed under public/, which
    # carries shares and change rates per field and no actor identity.
    vol, vol_overlap = {}, 0
    frozen = sorted((root / "public").glob("volatility-*.json"))
    if frozen:
        d = json.loads(frozen[-1].read_text())
        vol = {k: {"share": v["share"], "rate": v["rate"], "n": v["n"]}
               for k, v in d["fields"].items()}
        vol_overlap = d.get("overlap_actors", 0)

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
