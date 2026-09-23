-- Long-format observation table, same schema as every wss repo:
--   observations(series_id, entity_id, observed_at, captured_at, metric,
--                value, unit, source_id, raw_ref, parser_version)
-- entity_id is the Apify actor id.

-- 1. ARRIVALS. First capture an actor was ever seen in.
-- READ THE CAVEAT: inside a partition that truncates, "first seen" means the
-- actor crossed the popularity threshold, NOT that it was published. Only
-- trust this where source_partition is one of the 20 small categories.
SELECT entity_id,
       MIN(observed_at) AS first_seen,
       MAX(CASE WHEN metric='username' THEN value END) AS username,
       MAX(CASE WHEN metric='name'     THEN value END) AS name,
       MAX(CASE WHEN metric='source_partition' THEN value END) AS partition
FROM observations
GROUP BY entity_id
ORDER BY first_seen DESC;

-- 2. DEPARTURES. Actors present in an earlier capture and absent from the last.
WITH caps AS (SELECT DISTINCT observed_at FROM observations),
     last AS (SELECT MAX(observed_at) AS t FROM caps)
SELECT entity_id,
       MAX(observed_at) AS last_seen,
       MAX(CASE WHEN metric='users_30d' THEN CAST(value AS INTEGER) END) AS users_30d_when_last_seen
FROM observations
WHERE entity_id NOT IN (
    SELECT entity_id FROM observations, last WHERE observed_at = last.t)
GROUP BY entity_id
ORDER BY last_seen DESC;

-- 3. THE DEAD-BET RATE, WITH AGE. A near-zero actor only means failure if it is
-- OLD -- the 1-9 user band was the YOUNGEST in a stratified sample (median 104
-- days) and the zero band the oldest (323). Age here is weeks-since-first-seen,
-- which is why the cadence is weekly.
WITH age AS (
  SELECT entity_id,
         (JULIANDAY(MAX(observed_at)) - JULIANDAY(MIN(observed_at))) / 7.0 AS weeks_seen
  FROM observations GROUP BY entity_id),
u AS (
  SELECT entity_id, CAST(value AS INTEGER) AS u30, observed_at
  FROM observations WHERE metric='users_30d')
SELECT CASE WHEN u.u30 = 0 THEN 'zero'
            WHEN u.u30 < 10 THEN '1-9'
            WHEN u.u30 < 100 THEN '10-99' ELSE '100+' END AS band,
       COUNT(*) AS n,
       ROUND(AVG(age.weeks_seen), 1) AS mean_weeks_tracked
FROM u JOIN age USING (entity_id)
WHERE u.observed_at = (SELECT MAX(observed_at) FROM observations)
GROUP BY band ORDER BY n DESC;

-- 4. USAGE TRAJECTORY for one actor. Note users_30d is a 30-DAY ROLLING window,
-- so consecutive weekly points share ~75% of their input and are NOT independent.
-- users_7d is the one that is non-overlapping at weekly cadence.
SELECT observed_at,
       MAX(CASE WHEN metric='users_7d'  THEN CAST(value AS INTEGER) END) AS u7,
       MAX(CASE WHEN metric='users_30d' THEN CAST(value AS INTEGER) END) AS u30
FROM observations
WHERE entity_id = (SELECT entity_id FROM observations
                   WHERE metric='name' AND value='instagram-scraper' LIMIT 1)
GROUP BY observed_at ORDER BY observed_at;

-- 5. COVERAGE PER CAPTURE. Report the count collected -- never a share of the
-- store's claimed `total`, which returned 66,631 / 73,016 / 70,918 for three
-- sort orders in the same minute and drifts upward mid-sweep.
SELECT observed_at, COUNT(DISTINCT entity_id) AS actors_collected
FROM observations GROUP BY observed_at ORDER BY observed_at;
