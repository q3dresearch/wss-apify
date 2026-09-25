# Data shape

*Generated 2026-09-25T09:17:00Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **4,214,722 observations** across 1 partition(s), in **1 series**
  - `apify.store.actors` — 4,214,722 rows, **53141 entities**
- Raw: 0 file(s), 0 bytes on disk, 2 capture date(s), 2026-09-24 → 2026-09-25

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
| `badge` | apify.store.actors | 152 | 21 | text |  | 1 | `risingStar` |
| `bookmark_count` | apify.store.actors | 247,968 | 53141 | number | bookmarks | 229 | `0` … `5127` |
| `builds_total` | apify.store.actors | 247,968 | 53141 | number | builds | 650 | `1` … `4588` |
| `categories` | apify.store.actors | 247,345 | 52592 | text |  | 989 | `AGENTS`, `AGENTS; AI`, `AGENTS; AI; AUTOMATION` |
| `last_run_started_at` | apify.store.actors | 247,705 | 53058 | date |  | 96762 | `2025-05-06T14:05:39.908Z` … `2026-09-25T09:01:41.296Z` |
| `listed` | apify.store.actors | 247,968 | 53141 | bool | count | 1 | `1` |
| `name` | apify.store.actors | 247,968 | 53141 | text |  | 37625 | `104-company-reviews-urls`, `104-scraper`, `10times` |
| `pricing_model` | apify.store.actors | 247,968 | 53141 | text |  | 2 | `FREE`, `PAY_PER_EVENT` |
| `review_count` | apify.store.actors | 247,968 | 53141 | number | reviews | 93 | `0` … `1817` |
| `review_rating` | apify.store.actors | 247,968 | 53141 | number | stars | 810 | `0.0` … `5.0` |
| `runs_total` | apify.store.actors | 247,968 | 53141 | number | runs | 8385 | `0` … `199697128` |
| `source_partition` | apify.store.actors | 247,968 | 53141 | text |  | 24 | `AGENTS`, `AI`, `ALL` |
| `title` | apify.store.actors | 247,968 | 53141 | text |  | 47705 | `$0.375/1000 Twitter / X `, `$0.65/1K 💚 Immobiliare.i`, `$0.7/1K 💙 Fotocasa.es Re` |
| `username` | apify.store.actors | 247,968 | 53141 | text |  | 2762 | `01010101`, `0200project`, `0meetsares` |
| `users_30d` | apify.store.actors | 247,968 | 53141 | number | users | 713 | `0` … `44380` |
| `users_7d` | apify.store.actors | 247,968 | 53141 | number | users | 492 | `0` … `23445` |
| `users_90d` | apify.store.actors | 247,968 | 53141 | number | users | 976 | `0` … `78946` |
| `users_total` | apify.store.actors | 247,968 | 53141 | number | users | 1878 | `0` … `617372` |

## Partitions

- `derived/observations/2026-09.csv.gz`
