# Data shape

*Generated 2026-09-28T10:24:28Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **10,565,931 observations** across 1 partition(s), in **1 series**
  - `apify.store.actors` — 10,565,931 rows, **55166 entities**
- Raw: 0 file(s), 0 bytes on disk, 5 capture date(s), 2026-09-24 → 2026-09-28

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
| `badge` | apify.store.actors | 377 | 23 | text |  | 1 | `risingStar` |
| `bookmark_count` | apify.store.actors | 621,635 | 55166 | number | bookmarks | 268 | `0` … `5134` |
| `builds_total` | apify.store.actors | 621,635 | 55166 | number | builds | 914 | `1` … `4588` |
| `categories` | apify.store.actors | 620,036 | 54099 | text |  | 1027 | `AGENTS`, `AGENTS; AI`, `AGENTS; AI; AUTOMATION` |
| `last_run_started_at` | apify.store.actors | 620,993 | 55077 | date |  | 230120 | `2025-05-06T14:05:39.908Z` … `2026-09-28T10:10:49.734Z` |
| `listed` | apify.store.actors | 621,635 | 55166 | bool | count | 1 | `1` |
| `name` | apify.store.actors | 621,635 | 55166 | text |  | 38834 | `104-company-reviews-urls`, `104-scraper`, `10times` |
| `pricing_model` | apify.store.actors | 621,635 | 55166 | text |  | 2 | `FREE`, `PAY_PER_EVENT` |
| `review_count` | apify.store.actors | 621,635 | 55166 | number | reviews | 101 | `0` … `1817` |
| `review_rating` | apify.store.actors | 621,635 | 55166 | number | stars | 837 | `0.0` … `5.0` |
| `runs_total` | apify.store.actors | 621,635 | 55166 | number | runs | 15424 | `0` … `201262636` |
| `source_partition` | apify.store.actors | 621,635 | 55166 | text |  | 24 | `AGENTS`, `AI`, `ALL` |
| `title` | apify.store.actors | 621,635 | 55166 | text |  | 50306 | `$0.375/1000 Twitter / X `, `$0.65/1K 💚 Immobiliare.i`, `$0.7/1K 💙 Fotocasa.es Re` |
| `username` | apify.store.actors | 621,635 | 55166 | text |  | 2860 | `01010101`, `0200project`, `0meetsares` |
| `users_30d` | apify.store.actors | 621,635 | 55166 | number | users | 1175 | `0` … `44735` |
| `users_7d` | apify.store.actors | 621,635 | 55166 | number | users | 821 | `0` … `23945` |
| `users_90d` | apify.store.actors | 621,635 | 55166 | number | users | 1601 | `0` … `79686` |
| `users_total` | apify.store.actors | 621,635 | 55166 | number | users | 3103 | `0` … `621779` |

## Partitions

- `derived/observations/2026-09.csv.gz`
