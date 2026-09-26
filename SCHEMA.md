# Data shape

*Generated 2026-09-26T09:01:59Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **6,330,903 observations** across 1 partition(s), in **1 series**
  - `apify.store.actors` — 6,330,903 rows, **53937 entities**
- Raw: 0 file(s), 0 bytes on disk, 3 capture date(s), 2026-09-24 → 2026-09-26

## Sources

| source | cadence | endpoints | storage | personal data | licence |
| --- | --- | ---: | --- | --- | --- |
| `apify.store.actors` | weekly | 160 | object | parties_only | NOT ESTABLISHED (checked 2026-09-24). Crawling is explicitly |

## Columns

```
series_id, entity_id, observed_at, captured_at, metric, value, unit, source_id, raw_ref, parser_version
```

`entity_id` looks like: **apify.store.actors** `001Q50LgYYIXgA6o1`, `003lUvaaNz3fFBefF`, `00Gm3NAMROOL5MUe9`

## Metrics

| metric | series | rows | entities | type | unit | distinct | range / samples |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| `badge` | apify.store.actors | 225 | 21 | text |  | 1 | `risingStar` |
| `bookmark_count` | apify.store.actors | 372,470 | 53937 | number | bookmarks | 244 | `0` … `5132` |
| `builds_total` | apify.store.actors | 372,470 | 53937 | number | builds | 758 | `1` … `4588` |
| `categories` | apify.store.actors | 371,546 | 53206 | text |  | 1020 | `AGENTS`, `AGENTS; AI`, `AGENTS; AI; AUTOMATION` |
| `last_run_started_at` | apify.store.actors | 372,082 | 53851 | date |  | 141451 | `2025-05-06T14:05:39.908Z` … `2026-09-26T08:48:30.489Z` |
| `listed` | apify.store.actors | 372,470 | 53937 | bool | count | 1 | `1` |
| `name` | apify.store.actors | 372,470 | 53937 | text |  | 38108 | `104-company-reviews-urls`, `104-scraper`, `10times` |
| `pricing_model` | apify.store.actors | 372,470 | 53937 | text |  | 2 | `FREE`, `PAY_PER_EVENT` |
| `review_count` | apify.store.actors | 372,470 | 53937 | number | reviews | 94 | `0` … `1817` |
| `review_rating` | apify.store.actors | 372,470 | 53937 | number | stars | 819 | `0.0` … `5.0` |
| `runs_total` | apify.store.actors | 372,470 | 53937 | number | runs | 10961 | `0` … `200196159` |
| `source_partition` | apify.store.actors | 372,470 | 53937 | text |  | 24 | `AGENTS`, `AI`, `ALL` |
| `title` | apify.store.actors | 372,470 | 53937 | text |  | 48760 | `$0.375/1000 Twitter / X `, `$0.65/1K 💚 Immobiliare.i`, `$0.7/1K 💙 Fotocasa.es Re` |
| `username` | apify.store.actors | 372,470 | 53937 | text |  | 2812 | `01010101`, `0200project`, `0meetsares` |
| `users_30d` | apify.store.actors | 372,470 | 53937 | number | users | 885 | `0` … `44616` |
| `users_7d` | apify.store.actors | 372,470 | 53937 | number | users | 614 | `0` … `23684` |
| `users_90d` | apify.store.actors | 372,470 | 53937 | number | users | 1218 | `0` … `79281` |
| `users_total` | apify.store.actors | 372,470 | 53937 | number | users | 2352 | `0` … `619022` |

## Partitions

- `derived/observations/2026-09.csv.gz`
