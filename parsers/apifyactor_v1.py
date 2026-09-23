"""Parser for schema_id `apifyactor.v1` -- the Apify actor store.

WHAT MOVES HERE IS AN ACTOR ARRIVING AND AN ACTOR LEAVING

The store has no `createdAt` in the listing and no status value meaning
withdrawn. An actor that is unpublished simply stops being returned. So both
ends of its life are visible only as a difference between captures:

  id appears for the first time   -> arrival (see the caveat below)
  id stops appearing              -> departure

`listed` is emitted once per actor per capture so the second one is an absence.

THE ARRIVAL SIGNAL IS CONFOUNDED, AND ONLY IN SOME PARTITIONS

The store endpoint stops returning items at roughly offset 15,900 under every
sort order. An unpartitioned sweep therefore sees a POPULARITY-ORDERED SLICE,
and inside that slice an actor first appears when it grows popular enough to
cross the threshold -- not when it was published. Those are different events.

First-seen is a sound age proxy only in partitions that enumerate completely.
Twenty of the twenty-three categories sit under the cap and do. AUTOMATION,
LEAD_GENERATION and DEVELOPER_TOOLS do not. `source_partition` is emitted on
every observation so that distinction survives into the derived data instead of
being lost at capture time.

THE ENTITY IS `id`, NOT username/name

Both `username` and `name` are user-chosen and both can be changed; the pair
forms the URL, so a rename looks exactly like a departure plus an arrival. `id`
is the stable key. Names are carried as metrics so a rename is visible AS a
rename.

TWO FIELDS THAT LOOK LIKE MEASUREMENTS AND ARE NOT

`count` in the envelope echoes the requested `limit` -- a page returning zero
items still reports count: 1000. It is never read here. `total` is not a
denominator either: three sort orders gave 66,631 / 73,016 / 70,918 in the same
minute, and it drifts upward during a sweep because the store is written while
it is read.

`categories` IS A SET IN ARBITRARY ORDER and is sorted before emission. Unsorted
it would report a change on most captures, which is the same trap the Gold
Standard registry's SDG list set.
"""
import json

from wss import derive

PARSER_VERSION = "1"
SCHEMA_ID = "apifyactor.v1"

TEXT = {
    "username": "username",
    "name": "name",
    "title": "title",
    "badge": "badge",
}

# stats -> metric name, unit. All counts.
STATS = {
    "totalUsers7Days": ("users_7d", "users"),
    "totalUsers30Days": ("users_30d", "users"),
    "totalUsers90Days": ("users_90d", "users"),
    "totalUsers": ("users_total", "users"),
    "totalRuns": ("runs_total", "runs"),
    "totalBuilds": ("builds_total", "builds"),
}


def _partition(url: str) -> str:
    """Which sweep this page came from -- see the confound in the docstring."""
    if "category=" in url:
        return url.split("category=", 1)[1].split("&", 1)[0]
    if "sortBy=" in url:
        return "sort:" + url.split("sortBy=", 1)[1].split("&", 1)[0]
    return "ALL"


def parse(body: bytes, ctx: derive.ParseContext):
    doc = json.loads(body)
    data = doc.get("data") if isinstance(doc, dict) else None
    if not isinstance(data, dict):
        return
    items = data.get("items")
    if not isinstance(items, list):
        return
    part = _partition(getattr(ctx, "url", "") or "")

    for a in items:
        if not isinstance(a, dict):
            continue
        entity = a.get("id")
        if entity in (None, ""):
            continue
        entity = str(entity)

        yield derive.Observation(entity_id=entity, metric="listed", value=1, unit="count")
        yield derive.Observation(entity_id=entity, metric="source_partition", value=part)

        for field, metric in TEXT.items():
            v = a.get(field)
            if v not in (None, ""):
                yield derive.Observation(entity_id=entity, metric=metric, value=str(v))

        stats = a.get("stats") or {}
        for field, (metric, unit) in STATS.items():
            v = stats.get(field)
            if isinstance(v, int) and not isinstance(v, bool):
                yield derive.Observation(entity_id=entity, metric=metric, value=v, unit=unit)

        last = stats.get("lastRunStartedAt")
        if last not in (None, ""):
            yield derive.Observation(entity_id=entity, metric="last_run_started_at", value=str(last))

        pm = (a.get("currentPricingInfo") or {}).get("pricingModel")
        if pm not in (None, ""):
            yield derive.Observation(entity_id=entity, metric="pricing_model", value=str(pm))

        for field, metric, unit in (("actorReviewCount", "review_count", "reviews"),
                                    ("bookmarkCount", "bookmark_count", "bookmarks")):
            v = a.get(field)
            if isinstance(v, int) and not isinstance(v, bool):
                yield derive.Observation(entity_id=entity, metric=metric, value=v, unit=unit)
        rating = a.get("actorReviewRating")
        if isinstance(rating, (int, float)) and not isinstance(rating, bool):
            yield derive.Observation(entity_id=entity, metric="review_rating",
                                     value=round(float(rating), 3), unit="stars")

        # Sorted: the publisher's order is arbitrary and would otherwise report a
        # change nearly every week.
        cats = sorted(str(c) for c in (a.get("categories") or []) if c)
        if cats:
            yield derive.Observation(entity_id=entity, metric="categories", value="; ".join(cats))


derive.register(SCHEMA_ID, parse, PARSER_VERSION)
