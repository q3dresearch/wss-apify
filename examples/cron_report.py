#!/usr/bin/env python3
"""Did the cron actually fire, on time, every time?

    python3 examples/cron_report.py

Reads every committed version of state/last_run.json out of git history. That
file is overwritten each run, so the history IS the record -- there is nowhere
else a skipped night is visible.

WHY THIS EXISTS. GitHub's scheduler is best-effort and fails in three ways that
all look like success from inside a single run: it delays a job (minutes to
hours, worse on the hour, which is why the cron here is at :35), it drops a
firing entirely under load, and it disables scheduled workflows outright after
60 days of repository inactivity. A weekly job takes a month to reveal any of
that. The daily trial window exists to get the answer in days, and this is the
script that reads it out.

A GAP IS THE FINDING. Two heartbeats 48 hours apart on a daily cron means one
night was skipped and no capture exists for it -- and for this source that data
is gone, because the store publishes only the present.
"""
from __future__ import annotations

import json, statistics as st, subprocess, sys
from datetime import datetime

PATH = "state/last_run.json"


def main() -> int:
    log = subprocess.run(["git", "log", "--format=%H", "--", PATH],
                         capture_output=True, text=True).stdout.split()
    if not log:
        print(f"  no committed history for {PATH} yet -- nothing has run")
        return 0
    runs = []
    for sha in reversed(log):
        blob = subprocess.run(["git", "show", f"{sha}:{PATH}"],
                              capture_output=True, text=True).stdout
        try:
            runs.append(json.loads(blob))
        except ValueError:
            continue
    print(f"  {len(runs)} recorded runs")
    ev = {}
    for r in runs:
        ev[r.get("event", "?")] = ev.get(r.get("event", "?"), 0) + 1
    print(f"  triggered by: {ev}")

    sched = [r for r in runs if r.get("event") == "schedule"]
    ts = []
    for r in sched:
        try:
            ts.append(datetime.fromisoformat(r["completed_at"].replace("Z", "+00:00")))
        except (KeyError, ValueError):
            pass
    ts.sort()
    if len(ts) < 2:
        print(f"  only {len(ts)} scheduled run(s) -- not enough to measure an interval yet")
        return 0

    gaps = [(ts[i + 1] - ts[i]).total_seconds() / 3600 for i in range(len(ts) - 1)]
    print(f"  scheduled runs {len(ts)}, {ts[0]:%Y-%m-%d %H:%M} .. {ts[-1]:%Y-%m-%d %H:%M}")
    print(f"  gaps (h): min {min(gaps):.1f}  median {st.median(gaps):.1f}  max {max(gaps):.1f}")
    skipped = [g for g in gaps if g > 36]        # a daily cron that took >36h skipped a night
    print(f"  gaps over 36h (a skipped firing): {len(skipped)}"
          + (f"  -> {[round(g, 1) for g in skipped]}" if skipped else ""))
    nights = round((ts[-1] - ts[0]).total_seconds() / 86400)
    print(f"  expected ~{nights} firings over the window, got {len(ts)}"
          f"  -> {100 * len(ts) / max(1, nights):.0f}% delivery")
    planned = {r.get("sources_planned") for r in sched}
    print(f"  sources_planned across runs: {planned}"
          f"  {'-- a 0 here means the job went green having captured nothing' if 0 in planned or '0' in planned else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
