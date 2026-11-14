"""Fig. 3E: single-cell contractility at D35, one vector triangle per point (grey CTR, yellow CHIR, black CHIR>C59)
and a black mean line per group; four panels (contraction force nN, contraction velocity um/s, relaxation velocity um/s,
contraction duration s).

The panels have no tick marks and their tick labels are outlined glyphs, not text, so each y axis is calibrated from
the vertical centres of its label rows (glyphs right of the axis title), paired in order with the values as printed.
Markers are read at their bounding-box centre. CHIR>C59 is not compared by any item and is not read.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

GREY, YELLOW = (0.498, 0.499, 0.498), (0.986, 0.750, 0.056)
# per panel: item, y-axis line x, left edge of the label column (axis title glyphs lie left of it), labels as printed
PANELS = [
    ("F3E_force", 75.54, 65.5, [0, 50, 100, 150, 200, 250, 300, 350]),
    ("F3E_contrvel", 121.51, 113.5, [0, 5, 10, 15, 20, 25, 30, 35, 40]),
    ("F3E_relaxvel", 175.0, 167.0, [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]),
    ("F3E_duration", 229.78, 218.6, [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35]),
]
GROUPS = {"ctr": GREY, "chir": YELLOW}
PANEL_WIDTH = 30.0


def _is(c, ref, tol=0.02):
    return c is not None and max(abs(a - b) for a, b in zip(c, ref)) < tol


def _label_rows(ds, ax, xmin):
    glyphs = sorted((d["rect"] for d in ds if d["type"] == "f" and _is(d.get("fill"), (0, 0, 0))
                     and d["rect"].x0 > xmin and d["rect"].x1 < ax - 0.3 and d["rect"].height < 4.5
                     and 193 < d["rect"].y0 < 250), key=lambda r: r.y0 + r.y1)
    rows = []
    for r in glyphs:
        c = (r.y0 + r.y1) / 2
        if rows and abs(rows[-1][0] - c) < 1.5:
            rows[-1][1].append(r)
            rows[-1][0] = (min(q.y0 for q in rows[-1][1]) + max(q.y1 for q in rows[-1][1])) / 2
        else:
            rows.append([c, [r]])
    return [c for c, _ in rows]  # top to bottom


def read(fig):
    ds = fig.drawings()
    out = {}
    for item, ax, xmin, ticks in PANELS:
        rows = _label_rows(ds, ax, xmin)
        if len(rows) != len(ticks):
            raise ValueError(f"{item}: found {len(rows)} tick label rows, expected {len(ticks)}")
        cal = calibrate([(y, v) for y, v in zip(rows, reversed(ticks))])
        unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)
        inside = [d for d in ds if ax < d["rect"].x0 and d["rect"].x1 < ax + PANEL_WIDTH]
        means = [d["rect"] for d in inside if d["type"] == "s" and d["rect"].height < 0.01
                 and 4 < d["rect"].width < 8 and _is(d.get("color"), (0, 0, 0))]
        for g, colour in GROUPS.items():
            tri = [d["rect"] for d in inside if d["type"] == "f" and _is(d.get("fill"), colour)
                   and [i[0] for i in d["items"]] == ["l", "l", "l"]
                   and abs(d["rect"].width - 3.0) < 0.1 and abs(d["rect"].height - 3.0) < 0.1]
            if not tri:
                raise ValueError(f"{item}/{g}: no markers")
            cx = sum((r.x0 + r.x1) / 2 for r in tri) / len(tri)
            pts = sorted((point(cal, (r.y0 + r.y1) / 2, unc, ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)) for r in tri),
                         key=lambda p: p["value"])
            m = min(means, key=lambda r: abs((r.x0 + r.x1) / 2 - cx))
            if abs((m.x0 + m.x1) / 2 - cx) > 2:
                raise ValueError(f"{item}/{g}: no mean line over the markers")
            lo, hi = cal.interval(m.y0, unc)
            out[f"{item}/{g}"] = {"points": pts, "countable": True, "bar": {"mean": [cal.value(m.y0), lo, hi]}}
    return {"groups": out}
