#!/usr/bin/env python3
"""How 30-day users are distributed across the store."""
import json, pathlib, sys
import plate
from plate import INK, INK2, MUTED, RULE, GRID, FAINT

W, H = 880, 560
SERIES = "#2f6f5e"
ALERT  = "#b4472e"


def main():
    here = pathlib.Path(__file__).resolve()
    st = json.load(open(sys.argv[1]))
    L = st["lorenz"]; top1 = st["top1pct_share"]
    # ORDER DECLARED HERE, NOT INHERITED. The stats file is written with
    # sort_keys=True, which orders these labels as STRINGS: 0, 1, 10-49, 2-4,
    # 200+, 5-9, 50-199. The set was right and the sequence was nonsense, and a
    # band chart in the wrong order reads as a distribution that is not there.
    ORDER = ["0", "1", "2-4", "5-9", "10-49", "50-199", "200+"]
    raw = st["u30_bands"]
    assert set(raw) == set(ORDER), f"band labels changed: {sorted(raw)}"
    bands = {k: raw[k] for k in ORDER}
    n = st["actors"]

    s = plate.open_svg(W, H,
        f"Half the store has exactly one user a month. The top 1% has {top1:.0f}% of them.",
        subtitle=f"Cumulative share of 30-day users against cumulative share of actors, "
                 f"poorest first. {n:,} actors, one capture.")
    f, y = plate.frame(W, 88,
        who="Anyone about to average this data, size the market, or pick a typical actor",
        decide="Whether \"an actor\" is a unit that means anything here",
        wrong="The curve sits near the diagonal, which would make a mean informative")
    s += f

    x0, x1 = 88, 560
    top, bot = y + 26, H - 96
    for t in (0, 25, 50, 75, 100):
        gx = x0 + (x1 - x0) * t / 100; gy = bot - (bot - top) * t / 100
        s.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="{GRID}"/>')
        s.append(plate.txt(x0 - 9, gy + 3.5, f"{t}", size=10, fill=MUTED, anchor="end"))
        s.append(plate.txt(gx, bot + 17, f"{t}", size=10, fill=MUTED, anchor="middle"))
    s.append(plate.txt(x0 - 9, top - 14, "% of users", size=10, fill=MUTED, anchor="end"))
    s.append(plate.txt((x0 + x1) / 2, bot + 36, "% of actors, least-used first", size=10.5, fill=MUTED, anchor="middle"))

    # equality line -- a 45 degree line asserts equal shares, which is exactly the claim being refuted
    s.append(f'<line x1="{x0}" y1="{bot}" x2="{x1}" y2="{top}" stroke="{FAINT}" stroke-width="1.4" '
             f'stroke-dasharray="5 4"/>')
    s += plate.halo(x0 + 96, bot - 78, "equal shares", size=10.5, fill=MUTED)

    pts = " ".join(f"{x0+(x1-x0)*a:.1f},{bot-(bot-top)*b:.1f}" for a, b in L)
    s.append(f'<polyline points="{pts}" fill="none" stroke="{SERIES}" stroke-width="2.4"/>')
    s.append(f'<line x1="{x0+(x1-x0)*0.99:.1f}" y1="{top}" x2="{x0+(x1-x0)*0.99:.1f}" y2="{bot}" '
             f'stroke="{ALERT}" stroke-width="1.6" stroke-dasharray="3 3"/>')
    s += plate.halo(x0 + (x1 - x0) * 0.99 - 8, top + 16, f"top 1% — {top1:.0f}% of all users",
                    size=11.5, fill=ALERT, anchor="end")

    # the same fact as a count, because a curve alone hides where the mass sits
    bx = 618
    s.append(plate.txt(bx, top - 2, "actors by 30-day users", size=10.5, fill=MUTED))
    mx = max(bands.values()); rowh = (bot - top - 16) / len(bands)
    for i, (lab, v) in enumerate(bands.items()):
        ry = top + 14 + i * rowh
        bw = (W - 46 - bx - 54) * v / mx
        dead = lab in ("0", "1")
        s.append(f'<rect x="{bx+34}" y="{ry:.1f}" width="{max(bw,2):.1f}" height="{rowh-5:.1f}" rx="2.5" '
                 f'fill="{ALERT if dead else SERIES}" fill-opacity="{0.85 if dead else 0.8}"/>')
        s.append(plate.txt(bx + 28, ry + rowh / 2, lab, size=10.5, fill=INK2, anchor="end"))
        s += plate.halo(bx + 34 + max(bw, 2) + 6, ry + rowh / 2, f"{v:,}", size=10, fill=INK2)
    s += plate.halo(bx, bot + 4, f"{100*(bands['0']+bands['1'])/n:.0f}% have one user or none",
                    size=11.5, fill=ALERT)

    s.append(f'<line x1="28" y1="{H-62:.1f}" x2="{W-28}" y2="{H-62:.1f}" stroke="{RULE}"/>')
    s += plate.wrap(28, H - 46,
        f"Apify store API, captured {n:,} distinct actors 2026-09-24. Median actor has "
        f"{st['u30_median']} user in 30 days; the largest has {st['u30_max']:,}. A mean over this "
        f"distribution describes no actor in it, and the store's own `total` is not a usable "
        f"denominator — see the coverage plate.",
        size=10, fill=MUTED, chars=132, leading=13)
    s.append("</svg>")
    out = here.parent / "charts" / "usage-concentration.svg"
    out.write_text("\n".join(s), encoding="utf-8")
    print(f"  wrote {out.name}  (top1%={top1}%, median={st['u30_median']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
