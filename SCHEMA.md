# Data shape

*Generated 2026-10-01T10:47:07Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **16,967,384 observations** across 2 partition(s), in **1 series**
  - `apify.store.actors` — 16,967,384 rows, **58492 entities**
- Raw: 0 file(s), 0 bytes on disk, 8 capture date(s), 2026-09-24 → 2026-10-01

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
| `badge` | apify.store.actors | 592 | 25 | text |  | 1 | `risingStar` |
| `bookmark_count` | apify.store.actors | 998,296 | 58492 | number | bookmarks | 326 | `0` … `5147` |
| `builds_total` | apify.store.actors | 998,296 | 58492 | number | builds | 1238 | `1` … `4602` |
| `categories` | apify.store.actors | 995,097 | 56683 | text |  | 1038 | `AGENTS`, `AGENTS; AI`, `AGENTS; AI; AUTOMATION` |
| `last_run_started_at` | apify.store.actors | 997,255 | 58394 | date |  | 378920 | `2025-05-06T14:05:39.908Z` … `2026-10-01T10:29:08.642Z` |
| `listed` | apify.store.actors | 998,296 | 58492 | bool | count | 1 | `1` |
| `name` | apify.store.actors | 998,296 | 58492 | text |  | 40704 | `100000jobs-ch-scraper`, `104-company-reviews-urls`, `104-scraper` |
| `pricing_model` | apify.store.actors | 998,296 | 58492 | text |  | 2 | `FREE`, `PAY_PER_EVENT` |
| `review_count` | apify.store.actors | 998,296 | 58492 | number | reviews | 108 | `0` … `1817` |
| `review_rating` | apify.store.actors | 998,296 | 58492 | number | stars | 908 | `0.0` … `5.0` |
| `runs_total` | apify.store.actors | 998,296 | 58492 | number | runs | 22130 | `0` … `203728861` |
| `source_partition` | apify.store.actors | 998,296 | 58492 | text |  | 24 | `AGENTS`, `AI`, `ALL` |
| `title` | apify.store.actors | 998,296 | 58492 | text |  | 54617 | `$0.375/1000 Twitter / X `, `$0.65/1K 💚 Immobiliare.i`, `$0.7/1K 💙 Fotocasa.es Re` |
| `username` | apify.store.actors | 998,296 | 58492 | text |  | 3076 | `01010101`, `0200project`, `0meetsares` |
| `users_30d` | apify.store.actors | 998,296 | 58492 | number | users | 1571 | `0` … `46405` |
| `users_7d` | apify.store.actors | 998,296 | 58492 | number | users | 1113 | `0` … `25327` |
| `users_90d` | apify.store.actors | 998,296 | 58492 | number | users | 2149 | `0` … `80449` |
| `users_total` | apify.store.actors | 998,296 | 58492 | number | users | 4254 | `0` … `628509` |

## Partitions

- `derived/observations/2026-09.csv.gz`
- `derived/observations/2026-10.csv.gz`
