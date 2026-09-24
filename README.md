# wss-apify — the Apify actor store, captured weekly

Every actor reachable through Apify's public store API: **how many people used it
in the last 7, 30 and 90 days**, total runs, pricing model, categories, reviews
and bookmarks. Captured weekly, because the store publishes only the present.

Read [registry/apify.store.actors.yml](registry/apify.store.actors.yml) first.

## Why this exists

`totalUsers30Days` is **live paid demand per scraper** — how many people actually
ran this thing last month. Nothing else in this fleet measures whether a data
product has customers.

But the store has no history endpoint, no changelog, **no creation date in the
listing**, and no status value meaning withdrawn. An actor that is unpublished
simply stops being returned. So every number is a single frame with nothing
behind it, and both ends of an actor's life — when it arrived, when it left —
exist only as a difference between two captures.

**The archive does not cover it.** `api.apify.com/v2/store` has **one** Internet
Archive memento, ever. That memento holds **949 of the 48,189** actors it claimed
at the time — 2.0%. The HTML page `apify.com/store` has 170 mementos; four
sampled ones held between 0 and 40 actor slugs, with `totalUsers30Days` present
in exactly one of the four.

## Why weekly, when monthly was the first answer

Two reasons, both measured.

**First-seen is the only age signal, and its resolution is the cadence.** With no
`createdAt` in the listing, the age proxy is the first capture an actor appears
in — so everything arriving between two captures shares one birthday. The actors
that matter are young: a stratified sample put the **1–9 monthly-user band at a
median age of 104 days** and the **zero-user band at 323**, and in one six-actor
niche the newest competitor was **nine days old**. Monthly would collapse those
six entries into five points and erase the order they arrived in — which is the
only thing separating a land rush from a steady trickle.

**`totalUsers7Days` is a seven-day window.** Weekly sampling of it is
non-overlapping and independent. Monthly discards three weeks in four.

**What weekly does not buy.** `totalUsers30Days` is a 30-day *rolling* window, so
four weekly reads share about 75% of their input — the usage series carries
roughly one independent observation per month however often it is sampled, and
`totalUsers90Days` is worse. Weekly sharpens **arrival and departure**. It does
not sharpen usage.

**Storage, measured rather than projected.** One capture is **67 MB of raw** (160 pages,
~0.42 MB gzipped each), so weekly is **~3.5 GB a year** and daily would be ~24 GB. An
earlier estimate of 0.14 GB/yr was wrong: it was computed on a *projected* field set,
and wss stores the raw response. There is no way to fetch less — `fields`, `select`,
`desc=false`, `minimal` and `view=compact` are all silently ignored and return
byte-identical output — and the 2.16x partition overlap is inherent, because actors
genuinely carry several categories. This likely wants `storage: object` (R2).

The one droppable block is the `ALL` partition: 16 of 160 pages, uniquely contributing
**431 actors of 51,449 (0.8%)**. It is kept, because those are the *uncategorised*
actors and nothing else would ever see them — 10% of cost for a permanent blind spot is
the wrong trade in a repo whose whole premise is that capture is irreversible.

**The cron is temporarily DAILY**, to prove the schedule fires — GitHub's scheduler
often skips or delays the first runs on a new repo, and a weekly job takes a month to
report that it is broken. The registry still declares `cadence: weekly` and the
workflow's `CADENCE` still says weekly, so `wss plan` keeps matching; only the wake-up
frequency changed. Revert the cron to `35 3 * * 1` once proven.

## Three fields that look like measurements and are not

| field | what it actually is |
| --- | --- |
| `count` | **echoes the requested `limit`.** A page returning zero items still reports `count: 1000` |
| `limit` | a **maximum**. Mid-range pages return 384–959 for `limit=1000`, so a short page is not the end |
| `total` | **not a denominator.** 66,631 / 73,016 / 70,918 for three sort orders in the same minute, and it drifts upward *during* a sweep because the store is written while it is read |

Only `len(items)` means anything, and only a **zero-item page** ends a partition.
Reading `count` produced two confident and opposite wrong claims about the
store's size within minutes.

## The truncation, and the trap it sets

The endpoint stops returning items near **offset 15,900** under every sort order,
while claiming a total near 66,000. A naive sweep collects about a quarter of the
store and reports success — so the sweep is **partitioned by category**, each
partition getting its own offset budget
([examples/refresh_endpoints.py](examples/refresh_endpoints.py)).

**This is also why first-seen has to be read carefully.** Inside a partition that
truncates, the visible set is popularity-ordered, so an actor first appears when
it grows popular enough to *cross the threshold* — not when it was published.
Those are different events.

| partitions | claimed size | enumerate fully? | is first-seen an age? |
| --- | ---: | --- | --- |
| 20 smaller categories | ≤ ~14,000 | yes | **yes** |
| `AUTOMATION` | ~29,700 | no | no — threshold-crossing |
| `LEAD_GENERATION` | ~24,200 | no | no — threshold-crossing |
| `DEVELOPER_TOOLS` | ~21,700 | no | no — threshold-crossing |

Every observation carries `source_partition` so this distinction survives into
the derived data instead of being lost at capture time. Age analysis is sound in
the small categories and unsound in the three largest.

## Reading the numbers

**A near-zero actor only means failure if it is old.** `totalUsers` is cumulative
and therefore fully confounded with age. Six actors in one niche all showing 2–8
users looked like a graveyard and were in fact all created within five months,
the newest nine days before being read — a land rush, which reads as a demand
signal rather than a death signal.

## Licence

**Crawling is explicitly permitted** — `api.apify.com/robots.txt` states no rules
at all, and `apify.com` carries `Content-Signal: search=yes, ai-input=yes,
ai-train=yes` with `Allow: /`. **Reuse is a separate and unestablished question:**
no licence appears in the payload and the terms have not been read. See
[LICENSE-DATA](LICENSE-DATA), which also covers the `parties_only` personal-data
declaration.

## Layout

| path | what |
| --- | --- |
| `registry/apify.store.actors.yml` | the source definition, gates, and the reasoning |
| `examples/refresh_endpoints.py` | materialises the partitioned endpoint list before validate |
| `parsers/apifyactor_v1.py` | schema `apifyactor.v1` → observations, keyed on actor `id` |
| `raw/`, `manifest/` | captured bytes and the append-only capture log |
| `examples/queries.sql` | arrivals, departures, the dead-bet rate with age, coverage |
