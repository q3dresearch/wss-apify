#!/usr/bin/env python3
"""What each partition of the sweep reaches, and which ones stop at the wall."""
import json, pathlib, sys
import plate
from plate import INK, INK2, MUTED, RULE, GRID, FAINT

W = 880
SERIES = "#2f6f5e"
ALERT  = "#b4472e"
WALL = 15000


def main():
    here = pathlib.Path(__file__).resolve()
    st = json.load(open(sys.argv[1]))
    P = st["partitions"]
    rows = sorted(P.items(), key=lambda kv: -kv[1]["rows"])
    # Vertical budget measured, not guessed: 24 rows at 19px, plus the frame,
    # plus a two-line summary, plus the rule and a three-line footnote. The
    # first version put the rule at H-62 and the summary at bot+44, and they
    # landed on top of each other.
    H = 360 + len(rows) * 19
    hit = [k for k, v in rows if v["max_offset"] >= WALL]

    s = plate.open_svg(W, H,
        f"{len(hit)} of {len(rows)} partitions stop at the wall, not at the end of their data",
        subtitle="Rows returned per partition in one sweep. The API stops serving items near "
                 "offset 15,900 under every sort order, while reporting a total near 66,000.")
    f, y = plate.frame(W, 88,
        who="Anyone about to report how many actors are on Apify, or how many are dead",
        decide="Whether to quote a store total at all, and which partitions can carry an age",
        wrong="No partition ends at the wall — then the sweep is complete and a total is safe")
    s += f

    # x1 leaves room for the longest right-hand label ('13,827   stopped at the
    # wall'), which overflowed the canvas at W-132.
    x0, x1 = 178, W - 258
    top = y + 30
    mx = max(v["rows"] for _, v in rows)
    for i, (k, v) in enumerate(rows):
        ry = top + i * 19
        bw = (x1 - x0) * v["rows"] / mx
        wall = v["max_offset"] >= WALL
        s.append(f'<rect x="{x0}" y="{ry:.1f}" width="{max(bw,2):.1f}" height="13" rx="2.5" '
                 f'fill="{ALERT if wall else SERIES}" fill-opacity="{0.9 if wall else 0.75}"/>')
        s.append(plate.txt(x0 - 10, ry + 10, k, size=10.5, fill=INK2 if wall else MUTED, anchor="end"))
        s += plate.halo(x0 + max(bw, 2) + 7, ry + 10,
                        f"{v['rows']:,}" + ("   stopped at the wall" if wall else ""),
                        size=10, fill=ALERT if wall else INK2)
    bot = top + len(rows) * 19

    s += plate.halo(x0, bot + 26,
                    f"{sum(v['rows'] for _, v in rows):,} rows collapse to {st['actors']:,} distinct actors",
                    size=12.5, fill=INK)
    s += plate.wrap(x0, bot + 44,
        f"{st['partitions_in_one_only']:,} of them appear in exactly one partition, so the categories "
        f"are not redundant with each other — the overlap is real actors carrying several categories.",
        size=10.5, fill=MUTED, chars=96, leading=13)

    s.append(f'<line x1="28" y1="{H-74:.1f}" x2="{W-28}" y2="{H-74:.1f}" stroke="{RULE}"/>')
    s += plate.wrap(28, H - 58,
        "Apify store API, one sweep 2026-09-24. A partition that ends at the wall is TRUNCATED and "
        "its visible set is popularity-ordered, so an actor first appears there when it crosses a "
        "threshold, not when it is published — first-seen is an age only in the partitions that end early.",
        size=10, fill=MUTED, chars=132, leading=13)
    s.append("</svg>")
    out = here.parent / "charts" / "partition-coverage.svg"
    out.write_text("\n".join(s), encoding="utf-8")
    print(f"  wrote {out.name}  ({len(hit)} at the wall of {len(rows)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
