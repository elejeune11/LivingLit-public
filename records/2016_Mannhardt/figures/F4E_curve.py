"""Fig. 4E: Frank-Starling curve, force [% of maximum] against increase in length [mm], mean ± SEM
(raster, 300 dpi).

The y-axis is calibrated on its ticks (100, 50, 0 as printed), the x-axis on its labelled ticks
(0.0, 0.1, 0.2, 0.3). Means are the filled discs left after an opening that removes the line and
the error bars; the error is the centre of the cap ending the dark run that rises from the disc's
centre column (none for the last point, whose bar hides behind the disc). The first point (x = 0)
is the slack-length group; all points are also returned as a curve with x (mm), group "_"."""
import numpy as np

from _util import (UNC_PX, axes, blobs, calibrate, dark, gray, opened, reading, runs, triple, x_axis_bottom,
                   x_axis_ticks, y_ticks)

V = [100, 50, 0]
XV = [0.0, 0.1, 0.2, 0.3]


def read(fig):
    img, scale = fig.render(300)
    img = img.astype(int)
    ax = axes(img)[0]
    cal = calibrate(list(zip([t for t, _ in y_ticks(img, ax)], V)))
    if len(y_ticks(img, ax)) != len(V):
        raise ValueError("y ticks")
    # the x-axis is detached below the plot: its ticks hang below its own line
    d = dark(img, 110)
    rows = [y for y in range(ax[3] + 1, img.shape[0]) if d[y, ax[1] + 10:].sum() > 0.5 * (img.shape[1] - ax[1])]
    if not rows:
        raise ValueError("no x-axis line")
    xb = max(r for r in rows if r - rows[0] < 6)
    xt = sorted(x_axis_ticks(img, xb, ax[1], img.shape[1]), key=lambda t: t[0])
    long = [p for p, n in xt if n >= 0.75 * max(n for _, n in xt)]
    if len(long) != len(XV):
        raise ValueError(f"{len(long)} labelled x ticks: {xt}")
    calx = calibrate(list(zip(long, XV)))
    m = opened(d, 9)
    discs = sorted([b for b in blobs(m) if 80 <= b["area"] <= 400 and b["x"] > ax[1] + 5 and b["y"] < ax[3] - 2],
                   key=lambda b: b["x"])
    if len(discs) != 7:
        raise ValueError(f"{len(discs)} discs")
    pts = []
    first = None
    for i, b in enumerate(discs):
        x = round(float(calx.value(b["x"])), 3)
        p = reading(cal, b["y"], UNC_PX, fig, scale, (b["x"], b["y"]), x=x)
        pts.append(p)
        if i == 0:
            xc = int(round(b["x"]))
            col = d[:int(b["y"]), xc]
            rr = runs(col)
            bar = {"mean": triple(p)}
            if rr and rr[-1][1] >= b["y"] - 9:  # the dark run rising from the disc: whisker up to the cap
                top = rr[-1][0]
                w = [y for y in range(top, top + 6) if d[y, xc - 5:xc + 6].sum() >= 9]  # cap rows: wide
                cap = (w[0] + w[-1]) / 2.0 if w else top
                bar["error"] = triple(reading(cal, cap, UNC_PX, fig, scale, (xc, cap)))
            first = {"points": [], "countable": False, "bar": bar}
    return {"groups": {"slack": first, "curve": {"points": pts, "countable": True}}}
