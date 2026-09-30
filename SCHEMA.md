# Data shape

*Generated 2026-09-30T10:18:32Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **14,828,835 observations** across 1 partition(s), in **1 series**
  - `apify.store.actors` — 14,828,835 rows, **56749 entities**
- Raw: 0 file(s), 0 bytes on disk, 7 capture date(s), 2026-09-24 → 2026-09-30

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
| `badge` | apify.store.actors | 521 | 24 | text |  | 1 | `risingStar` |
| `bookmark_count` | apify.store.actors | 872,443 | 56749 | number | bookmarks | 310 | `0` … `5141` |
| `builds_total` | apify.store.actors | 872,443 | 56749 | number | builds | 1127 | `1` … `4595` |
| `categories` | apify.store.actors | 870,144 | 55399 | text |  | 1035 | `AGENTS`, `AGENTS; AI`, `AGENTS; AI; AUTOMATION` |
| `last_run_started_at` | apify.store.actors | 871,525 | 56651 | date |  | 322605 | `2025-05-06T14:05:39.908Z` … `2026-09-30T10:01:41.153Z` |
| `listed` | apify.store.actors | 872,443 | 56749 | bool | count | 1 | `1` |
| `name` | apify.store.actors | 872,443 | 56749 | text |  | 39624 | `104-company-reviews-urls`, `104-scraper`, `10times` |
| `pricing_model` | apify.store.actors | 872,443 | 56749 | text |  | 2 | `FREE`, `PAY_PER_EVENT` |
| `review_count` | apify.store.actors | 872,443 | 56749 | number | reviews | 106 | `0` … `1817` |
| `review_rating` | apify.store.actors | 872,443 | 56749 | number | stars | 876 | `0.0` … `5.0` |
| `runs_total` | apify.store.actors | 872,443 | 56749 | number | runs | 19435 | `0` … `203057370` |
| `source_partition` | apify.store.actors | 872,443 | 56749 | text |  | 24 | `AGENTS`, `AI`, `ALL` |
| `title` | apify.store.actors | 872,443 | 56749 | text |  | 52864 | `$0.375/1000 Twitter / X `, `$0.65/1K 💚 Immobiliare.i`, `$0.7/1K 💙 Fotocasa.es Re` |
| `username` | apify.store.actors | 872,443 | 56749 | text |  | 2954 | `01010101`, `0200project`, `0meetsares` |
| `users_30d` | apify.store.actors | 872,443 | 56749 | number | users | 1409 | `0` … `46105` |
| `users_7d` | apify.store.actors | 872,443 | 56749 | number | users | 994 | `0` … `24970` |
| `users_90d` | apify.store.actors | 872,443 | 56749 | number | users | 1924 | `0` … `80148` |
| `users_total` | apify.store.actors | 872,443 | 56749 | number | users | 3778 | `0` … `626611` |

## Partitions

- `derived/observations/2026-09.csv.gz`
