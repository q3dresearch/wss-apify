# Data shape

*Generated 2026-09-24T08:59:50Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **2,111,175 observations** across 1 partition(s), in **1 series**
  - `apify.store.actors` — 2,111,175 rows, **51603 entities**
- Raw: 0 file(s), 0 bytes on disk, 1 capture date(s), 2026-09-24 → 2026-09-24

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
| `badge` | apify.store.actors | 75 | 21 | text |  | 1 | `risingStar` |
| `bookmark_count` | apify.store.actors | 124,200 | 51603 | number | bookmarks | 216 | `0` … `5122` |
| `builds_total` | apify.store.actors | 124,200 | 51603 | number | builds | 501 | `1` … `4588` |
| `categories` | apify.store.actors | 124,024 | 51432 | text |  | 984 | `AGENTS`, `AGENTS; AI`, `AGENTS; AI; AUTOMATION` |
| `last_run_started_at` | apify.store.actors | 124,076 | 51528 | date |  | 51497 | `2025-05-06T14:05:39.908Z` … `2026-09-24T08:48:36.770Z` |
| `listed` | apify.store.actors | 124,200 | 51603 | bool | count | 1 | `1` |
| `name` | apify.store.actors | 124,200 | 51603 | text |  | 36619 | `104-company-reviews-urls`, `104-scraper`, `10times` |
| `pricing_model` | apify.store.actors | 124,200 | 51603 | text |  | 2 | `FREE`, `PAY_PER_EVENT` |
| `review_count` | apify.store.actors | 124,200 | 51603 | number | reviews | 93 | `0` … `1817` |
| `review_rating` | apify.store.actors | 124,200 | 51603 | number | stars | 803 | `0.0` … `5.0` |
| `runs_total` | apify.store.actors | 124,200 | 51603 | number | runs | 5342 | `0` … `199532624` |
| `source_partition` | apify.store.actors | 124,200 | 51603 | text |  | 24 | `AGENTS`, `AI`, `ALL` |
| `title` | apify.store.actors | 124,200 | 51603 | text |  | 46150 | `$0.375/1000 Twitter / X `, `$0.65/1K 💚 Immobiliare.i`, `$0.7/1K 💙 Fotocasa.es Re` |
| `username` | apify.store.actors | 124,200 | 51603 | text |  | 2674 | `01010101`, `0200project`, `0meetsares` |
| `users_30d` | apify.store.actors | 124,200 | 51603 | number | users | 500 | `0` … `44354` |
| `users_7d` | apify.store.actors | 124,200 | 51603 | number | users | 335 | `0` … `23419` |
| `users_90d` | apify.store.actors | 124,200 | 51603 | number | users | 699 | `0` … `78710` |
| `users_total` | apify.store.actors | 124,200 | 51603 | number | users | 1336 | `0` … `615788` |

## Partitions

- `derived/observations/2026-09.csv.gz`
