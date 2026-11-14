"""Suppl. Fig. 2C (PPARGC1a) and 2G (TP53) (supplement PDF p. 19): relative mRNA (normalized to TBP), Control (DMSO)
and Torin1 (200 nM) with individual points, beside single fetal and adult heart RNA bars.

Vector panels. The crop holds the whole figure; each panel is found from its title word. The y axis is the long
vertical line left of the bars; its tick marks are the short horizontal lines ending on it, matched by height to the
numeric labels beside them. Bars are open three-sided paths standing on the x axis, taken left to right in the
order of the x labels as printed; the first two are Control (white) and Torin1 (grey). Markers are small black
filled shapes inside a bar's x range (circles for Control, squares for Torin1). Mean = bar top; error = upper
cap of the thin I-shaped error bar centred on the bar. Fetal and adult RNA bars (single samples) are not read.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

PANELS = {"PPARGC1a": "PPARGC1a", "TP53": "TP53"}  # label prefix -> title word as printed
GROUPS = ["Control (DMSO)", "Torin1 (200 nM)"]  # first two x labels, left to right


def _lines(d):
    return [(it[1], it[2]) for it in d["items"] if it[0] == "l"]


def _panel(fig, title):
    t = [w for w in fig.words() if w[4] == title]  # TP53 is printed twice at one spot (overlaid text)
    assert t and all(abs(w[0] - t[0][0]) < 2 and abs(w[1] - t[0][1]) < 2 for w in t), (title, t)
    cx, ty = (t[0][0] + t[0][2]) / 2, t[0][3]
    box = (cx - 80, ty, cx + 70, ty + 90)  # plot area below the title, tick labels included
    inside = lambda r: box[0] <= r.x0 and r.x1 <= box[2] and box[1] <= r.y0 and r.y1 <= box[3]
    ds = [d for d in fig.drawings() if inside(d["rect"])]
    vert = [d for d in ds if len(_lines(d)) == 1 and d["rect"].width < 0.01 and d["rect"].height > 40]
    yax = min(vert, key=lambda d: d["rect"].x0)
    ax_x, ax_bot = yax["rect"].x0, yax["rect"].y1
    ticks = sorted({round(d["rect"].y0, 3) for d in ds if len(_lines(d)) == 1 and d["rect"].height < 0.01
                    and abs(d["rect"].x1 - ax_x) < 0.05 and d["rect"].width < 4})
    labels = [((w[1] + w[3]) / 2, float(w[4])) for w in fig.words()
              if box[0] <= w[0] and w[2] < ax_x and box[1] <= w[1] and w[3] <= box[3] + 3
              and w[4].replace(".", "").isdigit()]
    marks = []
    for ty_ in ticks:
        near = [v for y, v in labels if abs(y - ty_) < 1.5]
        assert len(near) == 1, (title, ty_, near)
        marks.append((ty_, near[0]))
    assert len(marks) >= 5, (title, marks)
    cal = calibrate(marks)
    res_pt = cal.residual / abs(cal.slope)
    bars = sorted((d for d in ds if len(_lines(d)) == 3 and d.get("color") is not None
                   and abs(d["rect"].y1 - ax_bot) < 0.05 and d["rect"].width > 10), key=lambda d: d["rect"].x0)
    assert len(bars) == 4, (title, len(bars))
    errs = [d for d in ds if len(_lines(d)) == 3 and d.get("color") is not None and d["rect"].width < 10]
    dots = [d for d in ds if d.get("fill") == (0.0, 0.0, 0.0) and d["rect"].width < 4 and d["rect"].height < 4]
    unc = VECTOR_UNCERTAINTY_PT + res_pt
    out = {}
    for g, b in zip(GROUPS, bars):
        r = b["rect"]
        cx_ = (r.x0 + r.x1) / 2
        mean = point(cal, r.y0, unc, (cx_, r.y0))
        bar = {"mean": [mean["value"], mean["lo"], mean["hi"]]}
        e = [d for d in errs if abs((d["rect"].x0 + d["rect"].x1) / 2 - cx_) < 0.1]
        assert len(e) == 1, (title, g, len(e))
        ey = e[0]["rect"].y0
        ev = point(cal, ey, unc, (cx_, ey))
        bar["error"] = [ev["value"], ev["lo"], ev["hi"]]
        mine = sorted((d["rect"] for d in dots if r.x0 < (d["rect"].x0 + d["rect"].x1) / 2 < r.x1),
                      key=lambda q: (q.x0, q.y0))
        pts = [point(cal, (q.y0 + q.y1) / 2, unc, ((q.x0 + q.x1) / 2, (q.y0 + q.y1) / 2)) for q in mine]
        out[g] = {"points": pts, "countable": True, "bar": bar}
    return out


def read(fig):
    groups = {}
    for prefix, title in PANELS.items():
        for g, v in _panel(fig, title).items():
            groups[f"{prefix} {g}"] = v
    return {"groups": groups}
