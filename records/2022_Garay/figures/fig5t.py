"""Fig. 5T (ROS mean fluorescence intensity, MFI; DMSO 30d and SP 30d in PLZ), main.pdf page 9.

Vector panel drawn as a paired plot: three yellow DMSO discs and three purple SP discs, each a whole filled circle
(four Bezier arcs, radius about 2.02 pt) whose centre is its rectangle centre; a straight stroke joins each DMSO disc
to its SP disc (one per experiment). No mean or error bar is drawn, though the legend says mean ± SEM, so the
groups carry points only. The significance bracket is a three-segment path and is ignored.

Tick labels are outlined glyphs (no text), so the printed values 0, 150, 300, 450, 600 are stated and matched in
order, bottom to top, to the long major ticks on the y axis.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

MAJOR = [0, 150, 300, 450, 600]  # printed tick labels, bottom to top
COLOURS = {"DMSO": (0.940, 0.715, 0.153), "SP": (0.683, 0.447, 0.691)}
PAIRS = 3


def read(fig):
    st = []
    for d in fig.drawings():
        if d.get("fill") is None and len(d["items"]) == 1 and d["items"][0][0] == "l":
            a, b = d["items"][0][1], d["items"][0][2]
            st.append((a.x, a.y, b.x, b.y))
    axes = [s for s in st if abs(s[0] - s[2]) < 0.01 and abs(s[1] - s[3]) > 50]
    if len(axes) != 1:
        raise ValueError(f"{len(axes)} y axes")
    ax = axes[0][0]
    major = sorted((s[1] for s in st if abs(s[1] - s[3]) < 0.01 and abs(max(s[0], s[2]) - ax) < 0.05
                    and 4.3 < abs(s[2] - s[0]) < 4.9), reverse=True)
    if len(major) != len(MAJOR):
        raise ValueError(f"{len(major)} major ticks")
    cal = calibrate(list(zip(major, MAJOR)))
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)

    per = {g: [] for g in COLOURS}
    for d in fig.drawings():
        f, r = d.get("fill"), d["rect"]
        if f is None or len(d["items"]) != 4 or not all(it[0] == "c" for it in d["items"]):
            continue
        if abs(r.width - r.height) > 0.01 or not 3.9 < r.width < 4.2:
            raise ValueError(f"unexpected filled shape {r}")
        g = [k for k, c in COLOURS.items() if max(abs(a - b) for a, b in zip(f, c)) < 0.02]
        if len(g) != 1:
            raise ValueError(f"unknown disc colour {f}")
        per[g[0]].append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
    for g, ps in per.items():
        if len(ps) != PAIRS or max(p[0] for p in ps) - min(p[0] for p in ps) > 0.05:
            raise ValueError(f"{g}: {len(ps)} discs or not in one column")
    if min(p[0] for p in per["SP"]) <= max(p[0] for p in per["DMSO"]):
        raise ValueError("SP column is not right of DMSO")
    links = [s for s in st if abs(s[0] - s[2]) > 5 and abs(s[1] - s[3]) > 0.01]
    for x0, y0, x1, y1 in links:  # each joining stroke ends at one DMSO and one SP disc centre
        for x, y in ((x0, y0), (x1, y1)):
            if not any(abs(px - x) < 0.05 and abs(py - y) < 0.05 for ps in per.values() for px, py in ps):
                raise ValueError(f"pair stroke end {x:.2f},{y:.2f} is not a disc centre")
    if len(links) != PAIRS:
        raise ValueError(f"{len(links)} pair strokes")

    return {"groups": {g: {"points": [point(cal, y, unc, (x, y)) for x, y in sorted(ps, key=lambda p: p[1])],
                           "countable": True}
                       for g, ps in per.items()}}
