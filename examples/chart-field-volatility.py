#!/usr/bin/env python3
"""What each field costs to store against how often it actually changes."""
import json, math, pathlib, sys
import plate
from plate import INK, INK2, MUTED, RULE, GRID, FAINT

W, H = 880, 600
SERIES = "#2f6f5e"
ALERT  = "#b4472e"
DROPPED = {"userPictureUrl", "pictureUrl", "url"}
LABEL = {"currentPricingInfo.pricingPerEvent", "userPictureUrl", "pictureUrl", "url",
         "description", "stats.publicActorRunStats30Days", "stats.lastRunStartedAt",
         "stats.totalUsers30Days", "id", "name", "title", "categories",
         "currentPricingInfo.pricingModel", "username"}


def main():
    here = pathlib.Path(__file__).resolve()
    # Argument-free by default so the workflow can call it bare: read the
    # newest public snapshot, which is the aggregate that is safe to publish.
    src = (sys.argv[1] if len(sys.argv) > 1 else
           str(sorted((here.parents[1] / "public").glob("stats-*.json"))[-1]))
    st = json.load(open(src))
    V = st["volatility"]; overlap = st["volatility_overlap"]
    if not V:
        print("  no volatility data"); return 1

    s = plate.open_svg(W, H,
        "The three most expensive fields are the three nobody would query",
        subtitle=f"Share of the stored payload against how often a field changed, over the 37 days "
                 f"between the single archive memento and this capture. One mark per field, "
                 f"{overlap} actors present in both.")
    f, y = plate.frame(W, 88,
        who="Anyone deciding what to keep, what to drop, and what a weekly diff will surface",
        decide="Which fields earn their bytes, and which changes are worth alerting on",
        wrong="Cost and volatility line up — then there is no free cut, only trade-offs")
    s += f

    x0, x1 = 86, W - 172
    top, bot = y + 30, H - 96
    ymax = math.log10(40)                      # payload share, log: values span 0.003% to 34%
    def px(r): return x0 + (x1 - x0) * r / 100
    def py(v): return bot - (math.log10(max(v, 0.003)) - math.log10(0.003)) / (math.log10(40) - math.log10(0.003)) * (bot - top)

    for t in (0, 25, 50, 75, 100):
        gx = px(t)
        s.append(f'<line x1="{gx:.1f}" y1="{top}" x2="{gx:.1f}" y2="{bot}" stroke="{GRID}"/>')
        s.append(plate.txt(gx, bot + 17, f"{t}", size=10, fill=MUTED, anchor="middle"))
    for v in (0.01, 0.1, 1, 10):
        gy = py(v)
        s.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="{GRID}"/>')
        s.append(plate.txt(x0 - 9, gy + 3.5, f"{v:g}", size=10, fill=MUTED, anchor="end"))
    s.append(plate.txt(x0 - 9, top - 26, "% of stored", size=10, fill=MUTED, anchor="end"))
    s.append(plate.txt(x0 - 9, top - 15, "payload", size=10, fill=MUTED, anchor="end"))
    s.append(plate.txt((x0 + x1) / 2, bot + 36, "% of actors whose value changed in 37 days",
                       size=10.5, fill=MUTED, anchor="middle"))

    placed = []
    for k, d in sorted(V.items(), key=lambda kv: -kv[1]["share"]):
        cx, cy = px(d["rate"]), py(d["share"])
        drop = k in DROPPED
        r = 4.0 + min(4.0, d["share"] / 6)
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{ALERT if drop else SERIES}" '
                 f'fill-opacity="{0.9 if drop else 0.5}" stroke="{plate.SURFACE}" stroke-width="1.1"/>')
        if k in LABEL:
            ty = cy + 3.5
            while any(abs(ty - q) < 11 and abs(cx - qx) < 150 for qx, q in placed):
                ty -= 11
            placed.append((cx, ty))
            lab = k.replace("currentPricingInfo.", "pricing.").replace("stats.", "stats.")
            anchor = "end" if cx > x1 - 150 else "start"
            dx = -r - 6 if anchor == "end" else r + 6
            s += plate.halo(cx + dx, ty, lab + ("  (dropped)" if drop else ""), size=9.5,
                            fill=ALERT if drop else INK2, anchor=anchor, weight="600" if drop else "500")

    lx = x1 + 22
    s.append(plate.txt(lx, top + 4, "READ IT AS FOUR CORNERS", size=9, fill=MUTED, weight="700", spacing="0.8"))
    for i, (t, c) in enumerate((
            ("top-left — big and static: pure waste, and this is where the three dropped fields sit", ALERT),
            ("top-right — big and live: expensive but real, keep it (pricingPerEvent)", INK2),
            ("bottom-right — cheap and always moving: the usage counters, and why dedupe never fires here", INK2),
            ("bottom-left — cheap and static: identity, free to carry (id, name)", MUTED))):
        s += plate.wrap(lx, top + 24 + i * 60, t, size=10, fill=c, chars=23, leading=12.5)

    s.append(f'<line x1="28" y1="{H-62:.1f}" x2="{W-28}" y2="{H-62:.1f}" stroke="{RULE}"/>')
    s += plate.wrap(28, H - 46,
        f"Apify store API. Before-picture is the ONLY Internet Archive memento of this endpoint "
        f"(2026-08-18, 949 actors); {overlap} of them are still present. One gap of 37 days is a "
        f"weak estimate of a weekly change rate and a single pair cannot see a field that changes "
        f"and changes back.",
        size=10, fill=MUTED, chars=132, leading=13)
    s.append("</svg>")
    out = here.parent / "charts" / "field-volatility.svg"
    out.write_text("\n".join(s), encoding="utf-8")
    print(f"  wrote {out.name}  ({len(V)} fields)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
