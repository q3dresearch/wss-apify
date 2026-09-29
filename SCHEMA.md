# Data shape

*Generated 2026-09-29T10:24:04Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **12,693,664 observations** across 1 partition(s), in **1 series**
  - `apify.store.actors` — 12,693,664 rows, **56074 entities**
- Raw: 0 file(s), 0 bytes on disk, 6 capture date(s), 2026-09-24 → 2026-09-29

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
| `badge` | apify.store.actors | 450 | 24 | text |  | 1 | `risingStar` |
| `bookmark_count` | apify.store.actors | 746,831 | 56074 | number | bookmarks | 284 | `0` … `5137` |
| `builds_total` | apify.store.actors | 746,831 | 56074 | number | builds | 1020 | `1` … `4591` |
| `categories` | apify.store.actors | 744,713 | 54758 | text |  | 1031 | `AGENTS`, `AGENTS; AI`, `AGENTS; AI; AUTOMATION` |
| `last_run_started_at` | apify.store.actors | 746,036 | 55973 | date |  | 276691 | `2025-05-06T14:05:39.908Z` … `2026-09-29T10:05:46.061Z` |
| `listed` | apify.store.actors | 746,831 | 56074 | bool | count | 1 | `1` |
| `name` | apify.store.actors | 746,831 | 56074 | text |  | 39297 | `104-company-reviews-urls`, `104-scraper`, `10times` |
| `pricing_model` | apify.store.actors | 746,831 | 56074 | text |  | 2 | `FREE`, `PAY_PER_EVENT` |
| `review_count` | apify.store.actors | 746,831 | 56074 | number | reviews | 103 | `0` … `1817` |
| `review_rating` | apify.store.actors | 746,831 | 56074 | number | stars | 847 | `0.0` … `5.0` |
| `runs_total` | apify.store.actors | 746,831 | 56074 | number | runs | 17464 | `0` … `202432980` |
| `source_partition` | apify.store.actors | 746,831 | 56074 | text |  | 24 | `AGENTS`, `AI`, `ALL` |
| `title` | apify.store.actors | 746,831 | 56074 | text |  | 51351 | `$0.375/1000 Twitter / X `, `$0.65/1K 💚 Immobiliare.i`, `$0.7/1K 💙 Fotocasa.es Re` |
| `username` | apify.store.actors | 746,831 | 56074 | text |  | 2912 | `01010101`, `0200project`, `0meetsares` |
| `users_30d` | apify.store.actors | 746,831 | 56074 | number | users | 1295 | `0` … `45524` |
| `users_7d` | apify.store.actors | 746,831 | 56074 | number | users | 907 | `0` … `24675` |
| `users_90d` | apify.store.actors | 746,831 | 56074 | number | users | 1767 | `0` … `79849` |
| `users_total` | apify.store.actors | 746,831 | 56074 | number | users | 3442 | `0` … `624726` |

## Partitions

- `derived/observations/2026-09.csv.gz`
