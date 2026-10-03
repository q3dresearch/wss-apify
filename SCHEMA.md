# Data shape

*Generated 2026-10-03T10:01:36Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **21,278,101 observations** across 2 partition(s), in **1 series**
  - `apify.store.actors` — 21,278,101 rows, **60174 entities**
- Raw: 0 file(s), 0 bytes on disk, 10 capture date(s), 2026-09-24 → 2026-10-03

## Sources

| source | cadence | endpoints | storage | personal data | licence |
| --- | --- | ---: | --- | --- | --- |
| `apify.store.actors` | weekly | 160 | object | parties_only | NOT ESTABLISHED (checked 2026-09-24). Crawling is explicitly |

## Columns

```
series_id, entity_id, observed_at, captured_at, metric, value, unit, source_id, raw_ref, parser_version
```

`entity_id` looks like: **apify.store.actors** `001Q50LgYYIXgA6o1`, `003lUvaaNz3fFBefF`, `004r0jdkAswInYGhw`

## Metrics

| metric | series | rows | entities | type | unit | distinct | range / samples |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| `badge` | apify.store.actors | 747 | 27 | text |  | 1 | `risingStar` |
| `bookmark_count` | apify.store.actors | 1,251,913 | 60174 | number | bookmarks | 341 | `0` … `5153` |
| `builds_total` | apify.store.actors | 1,251,913 | 60174 | number | builds | 1421 | `1` … `4614` |
| `categories` | apify.store.actors | 1,248,047 | 58052 | text |  | 1045 | `AGENTS`, `AGENTS; AI`, `AGENTS; AI; AUTOMATION` |
| `last_run_started_at` | apify.store.actors | 1,250,612 | 60062 | date |  | 432296 | `2025-05-06T14:05:39.908Z` … `2026-10-03T09:30:33.006Z` |
| `listed` | apify.store.actors | 1,251,913 | 60174 | bool | count | 1 | `1` |
| `name` | apify.store.actors | 1,251,913 | 60174 | text |  | 41585 | `100000jobs-ch-scraper`, `104-company-reviews-urls`, `104-scraper` |
| `pricing_model` | apify.store.actors | 1,251,913 | 60174 | text |  | 2 | `FREE`, `PAY_PER_EVENT` |
| `review_count` | apify.store.actors | 1,251,913 | 60174 | number | reviews | 111 | `0` … `1817` |
| `review_rating` | apify.store.actors | 1,251,913 | 60174 | number | stars | 940 | `0.0` … `5.0` |
| `runs_total` | apify.store.actors | 1,251,913 | 60174 | number | runs | 25080 | `0` … `204912041` |
| `source_partition` | apify.store.actors | 1,251,913 | 60174 | text |  | 24 | `AGENTS`, `AI`, `ALL` |
| `title` | apify.store.actors | 1,251,913 | 60174 | text |  | 56573 | `$0.375/1000 Twitter / X `, `$0.65/1K 💚 Immobiliare.i`, `$0.7/1K 💙 Fotocasa.es Re` |
| `username` | apify.store.actors | 1,251,913 | 60174 | text |  | 3168 | `01010101`, `0200project`, `0meetsares` |
| `users_30d` | apify.store.actors | 1,251,913 | 60174 | number | users | 1750 | `0` … `47019` |
| `users_7d` | apify.store.actors | 1,251,913 | 60174 | number | users | 1241 | `0` … `26030` |
| `users_90d` | apify.store.actors | 1,251,913 | 60174 | number | users | 2361 | `0` … `80762` |
| `users_total` | apify.store.actors | 1,251,913 | 60174 | number | users | 4686 | `0` … `630276` |

## Partitions

- `derived/observations/2026-09.csv.gz`
- `derived/observations/2026-10.csv.gz`
