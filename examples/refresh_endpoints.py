#!/usr/bin/env python3
"""Materialise the endpoint list for apify.store.actors, then rewrite the registry.

    python3 examples/refresh_endpoints.py [--dry-run]

Runs in the workflow BEFORE `wss validate`, because what-will-be-fetched belongs
in the registry and the page count is not knowable ahead.

## WHY THIS IS NOT JUST offset=0,1000,2000,...

The store endpoint stops returning items at roughly offset 15,900, under every
sort order, while claiming a total near 66,000. A naive sweep collects about a
quarter of the store and reports success.

So the sweep is PARTITIONED BY CATEGORY and each partition gets its own offset
budget. Twenty of the twenty-three categories claim fewer than the cap and
enumerate completely. Three -- AUTOMATION, LEAD_GENERATION, DEVELOPER_TOOLS --
claim more and will still truncate; they are swept anyway, and the registry
records that their coverage is partial rather than pretending otherwise.

## THREE FIELDS THAT LIE, AND WHAT IS READ INSTEAD

`count` echoes the requested `limit`. A page with zero items reports count:1000.
    -> only len(items) is read.
`limit` is a MAXIMUM. Mid-range pages return 384-959 for limit=1000.
    -> a short page does NOT end a partition. Only a zero-item page does.
`total` is not a denominator. Three sort orders gave 66,631 / 73,016 / 70,918 in
the same minute, and it drifts upward mid-sweep because the store is written
while it is read.
    -> it is recorded for the record and never used to decide anything.
"""
from __future__ import annotations

import argparse, json, pathlib, re, socket, sys, time, urllib.error, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "registry" / "apify.store.actors.yml"
API = "https://api.apify.com/v2/store"
UA = "wss-screening/0.1 (+https://github.com/q3dresearch/wss-apify; archival research)"
LIMIT = 1000
OFFSET_CAP = 20000          # past the measured wall, so the wall is observed not assumed
WALL_OFFSET = 15000         # a partition ending at or past this truncated; see sweep()
CATS = ["AUTOMATION", "LEAD_GENERATION", "DEVELOPER_TOOLS", "SOCIAL_MEDIA", "ECOMMERCE",
        "OTHER", "AI", "JOBS", "REAL_ESTATE", "BUSINESS", "SEO_TOOLS", "VIDEOS", "AGENTS",
        "INTEGRATIONS", "NEWS", "TRAVEL", "MCP_SERVERS", "MARKETING", "OPEN_SOURCE",
        "SPORTS", "FOR_CREATORS", "EDUCATION", "GAMES"]

_orig = socket.getaddrinfo
socket.getaddrinfo = lambda h, p, f=0, t=0, pr=0, fl=0: _orig(h, p, socket.AF_INET, t, pr, fl)


def fetch(url: str, tries: int = 4):
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}),
                                       timeout=120)
            return json.loads(r.read()).get("data", {})
        except urllib.error.HTTPError as e:
            if e.code in (429, 503, 504) and i < tries - 1:
                time.sleep(10 * (i + 1)); continue
            return None
        except Exception:
            if i < tries - 1:
                time.sleep(10 * (i + 1)); continue
            return None
    return None


def sweep(extra: str, label: str):
    """Page until a zero-item page. Returns (urls, actors_seen, hit_cap)."""
    urls, n, off = [], 0, 0
    while off < OFFSET_CAP:
        url = f"{API}?limit={LIMIT}&offset={off}{extra}"
        d = fetch(url)
        if d is None:
            print(f"  {label:18s} offset {off}: FETCH FAILED after retries -- stopping")
            return urls, n, False
        items = d.get("items") or []
        if not items:                      # only a ZERO page ends a partition
            break
        urls.append(url); n += len(items); off += LIMIT
        time.sleep(0.35)
    # TRUNCATION IS DETECTED AT THE WALL, NOT AT OFFSET_CAP. The first version
    # tested `off >= OFFSET_CAP` (20,000) and would never have fired: every
    # truncating partition stops at the SAME ~15,900 wall the unpartitioned
    # sweep does, by returning a zero page, so it exits the loop looking exactly
    # like a partition that genuinely ran out. Measured: ALL, AUTOMATION,
    # LEAD_GENERATION and DEVELOPER_TOOLS each ended at 16 pages; SOCIAL_MEDIA
    # ended at 11 and ECOMMERCE at 14, which are real ends.
    #
    # This distinction is load-bearing. First-seen is only an AGE in a partition
    # that enumerates completely; in a truncated one it means the actor crossed
    # a popularity threshold. Getting it wrong silently mislabels a year of data.
    hit = off >= WALL_OFFSET
    print(f"  {label:18s} {len(urls):>3} pages, {n:>6,} rows"
          f"{'   ENDED AT THE WALL -- partial, first-seen is NOT age here' if hit else ''}")
    return urls, n, hit


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    urls, truncated = [], []
    u, n, hit = sweep("", "ALL")
    urls += u
    if hit: truncated.append("ALL")
    for c in CATS:
        u, n, hit = sweep(f"&category={c}", c)
        urls += u
        if hit: truncated.append(c)

    urls = list(dict.fromkeys(urls))
    print(f"\n  {len(urls)} endpoints; partitions that hit the cap: {truncated or 'none'}")

    # A collapse means the API changed shape, not that the store emptied. Refuse.
    if len(urls) < 20:
        print(f"  REFUSING TO WRITE: only {len(urls)} endpoints, expected >20. "
              f"The endpoint shape has probably changed.", file=sys.stderr)
        return 1
    if a.dry_run:
        return 0

    block = "endpoints:\n" + "".join(
        f'  - url: "{u}"\n    delay_seconds: 2\n    timeout_seconds: 90\n' for u in urls)
    text = REG.read_text()
    before = set(re.findall(r"^([a-z_]+):", text, re.M))
    # (?m) NOT (?ms) -- with DOTALL the `.` ate the newline and deleted the whole
    # gates block in wss-carbon-registry. Anchored to the next top-level key.
    new = re.sub(r"(?m)^endpoints:.*?(?=^gates:)", block + "\n", text, flags=re.S)
    after = set(re.findall(r"^([a-z_]+):", new, re.M))
    lost = before - after
    if lost:
        print(f"  REFUSING TO WRITE: rewrite dropped top-level key(s) {sorted(lost)}", file=sys.stderr)
        return 1
    REG.write_text(new)
    print(f"  wrote {len(urls)} endpoints into {REG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
