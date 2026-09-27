# Data shape

*Generated 2026-09-27T09:44:08Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **8,454,478 observations** across 1 partition(s), in **1 series**
  - `apify.store.actors` — 8,454,478 rows, **54662 entities**
- Raw: 0 file(s), 0 bytes on disk, 4 capture date(s), 2026-09-24 → 2026-09-27

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
| `badge` | apify.store.actors | 302 | 23 | text |  | 1 | `risingStar` |
| `bookmark_count` | apify.store.actors | 497,415 | 54662 | number | bookmarks | 260 | `0` … `5134` |
| `builds_total` | apify.store.actors | 497,415 | 54662 | number | builds | 851 | `1` … `4588` |
| `categories` | apify.store.actors | 496,061 | 53644 | text |  | 1025 | `AGENTS`, `AGENTS; AI`, `AGENTS; AI; AUTOMATION` |
| `last_run_started_at` | apify.store.actors | 496,890 | 54574 | date |  | 185503 | `2025-05-06T14:05:39.908Z` … `2026-09-27T09:33:37.219Z` |
| `listed` | apify.store.actors | 497,415 | 54662 | bool | count | 1 | `1` |
| `name` | apify.store.actors | 497,415 | 54662 | text |  | 38559 | `104-company-reviews-urls`, `104-scraper`, `10times` |
| `pricing_model` | apify.store.actors | 497,415 | 54662 | text |  | 2 | `FREE`, `PAY_PER_EVENT` |
| `review_count` | apify.store.actors | 497,415 | 54662 | number | reviews | 98 | `0` … `1817` |
| `review_rating` | apify.store.actors | 497,415 | 54662 | number | stars | 828 | `0.0` … `5.0` |
| `runs_total` | apify.store.actors | 497,415 | 54662 | number | runs | 13302 | `0` … `200736578` |
| `source_partition` | apify.store.actors | 497,415 | 54662 | text |  | 24 | `AGENTS`, `AI`, `ALL` |
| `title` | apify.store.actors | 497,415 | 54662 | text |  | 49581 | `$0.375/1000 Twitter / X `, `$0.65/1K 💚 Immobiliare.i`, `$0.7/1K 💙 Fotocasa.es Re` |
| `username` | apify.store.actors | 497,415 | 54662 | text |  | 2841 | `01010101`, `0200project`, `0meetsares` |
| `users_30d` | apify.store.actors | 497,415 | 54662 | number | users | 1037 | `0` … `44735` |
| `users_7d` | apify.store.actors | 497,415 | 54662 | number | users | 723 | `0` … `23747` |
| `users_90d` | apify.store.actors | 497,415 | 54662 | number | users | 1410 | `0` … `79562` |
| `users_total` | apify.store.actors | 497,415 | 54662 | number | users | 2747 | `0` … `620566` |

## Partitions

- `derived/observations/2026-09.csv.gz`
