"""Fig. 6G: six contraction plots (beating rate, force, time to peak, relaxation time, resting length, contraction
velocity), left to right. Each has a grey Non-Expanded bar and a yellow P4 CHIR>CTR bar (bar top = mean) with an
upper error bar, and one filled circle per tissue coloured by line (blue CVI-111, orange CVI-273); both colours
belong to the bar they sit on. Each circle is a fill path followed by a stroke-only copy; only the fills are read.
The y axis of each plot is calibrated from its vector tick marks paired bottom to top with the printed labels
(outlined glyphs, not text)."""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

# plots left to right: (item, tick values bottom to top)
PLOTS = [
    ("F6G_rate", [0, 20, 40, 60]),
    ("F6G_force", [0.0, 0.1, 0.2, 0.3]),
    ("F6G_ttp", [0.16, 0.18, 0.20, 0.22, 0.24]),
    ("F6G_relax", [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]),
    ("F6G_length", [4.5, 5.0, 5.5, 6.0, 6.5, 7.0]),
    ("F6G_vel", [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]),
]
GREY, YELLOW = (0.86, 0.86, 0.86), (0.98, 0.74, 0.06)
DOTS = [(0.99, 0.38, 0.03), (0.0, 0.15, 0.75)]   # CVI-273 orange, CVI-111 blue


def _near(c, rgb, tol=0.03):
    return c is not None and max(abs(a - b) for a, b in zip(c, rgb)) < tol


def _black(c):
    return c is not None and max(c) < 0.1


def read(fig):
    ds = fig.drawings()
    axes = sorted((d["rect"] for d in ds if d.get("fill") is None and _black(d.get("color"))
                   and d["rect"].width < 0.01 and d["rect"].height > 60), key=lambda r: r.x0)
    if len(axes) != len(PLOTS):
        raise ValueError(f"found {len(axes)} y axis lines, expected {len(PLOTS)}")
    hl = [d["rect"] for d in ds if d.get("fill") is None and _black(d.get("color")) and d["rect"].height < 0.01]
    dots = [d for d in ds if d.get("fill") is not None and [i[0] for i in d["items"]] == ["c", "c", "c", "c"]
            and d["rect"].width < 2 and any(_near(d["fill"], c) for c in DOTS)]
    out = {}
    for ax, (item, ticks) in zip(axes, PLOTS):
        x = ax.x0
        tk = sorted((r for r in hl if abs(r.x1 - x) < 0.05 and r.width < 2.5), key=lambda r: -r.y0)
        if len(tk) != len(ticks):
            raise ValueError(f"{item}: found {len(tk)} y tick marks, expected {len(ticks)}")
        cal = calibrate([(r.y0, v) for r, v in zip(tk, ticks)])
        unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)
        bars = {}
        for g, rgb in (("nonexp", GREY), ("p4exp", YELLOW)):
            b = [d["rect"] for d in ds if _near(d.get("fill"), rgb) and d["rect"].width > 5
                 and x < d["rect"].x0 < x + 35 and d["rect"].y1 > ax.y1 - 1]
            if len(b) != 1:
                raise ValueError(f"{item}/{g}: found {len(b)} bars, expected 1")
            bars[g] = b[0]
        for g, b in bars.items():
            cx = (b.x0 + b.x1) / 2
            caps = [r for r in hl if 3 < r.width < 6 and abs((r.x0 + r.x1) / 2 - cx) < 1 and r.y0 < b.y0 + 0.1]
            if len(caps) != 1:
                raise ValueError(f"{item}/{g}: found {len(caps)} error caps, expected 1")
            pts = []
            for d in dots:
                r = d["rect"]
                px, py = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
                if b.x0 - 1 < px < b.x1 + 1 and ax.y0 - 5 < py < ax.y1 + 1:
                    pts.append(point(cal, py, unc, (px, py)))
            pts.sort(key=lambda p: p["value"])
            lo, hi = cal.interval(b.y0, unc)
            elo, ehi = cal.interval(caps[0].y0, unc)
            out[f"{item}/{g}"] = {"points": pts, "countable": True,
                                  "bar": {"mean": [cal.value(b.y0), lo, hi],
                                          "error": [cal.value(caps[0].y0), elo, ehi]}}
    return {"groups": out}
