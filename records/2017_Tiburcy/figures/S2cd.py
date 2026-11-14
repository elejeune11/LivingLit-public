"""Suppl. Fig. 2c,d (supplement p. 42): Ki67+ cells (%) among cardiomyocytes (c, left) and non-myocytes (d, right)
in input cells, undefined EHM and defined EHM. One open bar per group (a group mean) with one upward error bar; no
single sample is drawn, so every group is bar only (countable false).

The panels are vector. Each y axis is one path (a long vertical line plus tick stubs), calibrated from its stubs matched
in order to the printed labels left of it (c: 0, 5, 10, 15; d: 0, 10, 20, 30). A panel is named by its title word
(Cardiomyocytes, Non-myocytes) above the axis; columns are named from the words under the x axis (Input, Undef., Def.).

Each bar is drawn twice (a white-filled path and a stroked rectangle) whose tops differ by up to 0.05 pt; the bar top is
their midpoint with half their gap added to its uncertainty. Each error bar is a T (a cap and a vertical line from the
cap down to the bar top); 'error' is the cap. The T's base is checked to lie within 1.5 pt of its bar's top.

Each bar is used by two record items (e.g. Def. EHM by S2c_def_input and S2c_def_undef), and a figures.yaml label
links to one item, so each reading is returned once per item that uses it: label "<item>/<group>".
"""
from livinglit.figures.source import calibrate

UNC_PT = 0.5                                  # vector position uncertainty (pt)
PANELS = {"Cardiomyocytes": ("S2c", [0, 5, 10, 15]), "Non-myocytes": ("S2d", [0, 10, 20, 30])}
COLUMNS = {"Input": "input", "Undef": "undef", "Def.": "def"}   # word under the x axis -> group
ITEMS = {"def_input": ["def", "input"], "def_undef": ["def", "undef"]}
PANEL_W = 115                                 # pt right of a y axis that belong to its panel
BASE_TOL = 1.5                                # pt: T base to bar top


def _axes(fig):
    out = []
    for d in fig.drawings():
        items = d["items"]
        if len(items) < 3 or any(it[0] != "l" for it in items):
            continue
        long = [it for it in items if abs(it[1].x - it[2].x) < 0.01 and abs(it[1].y - it[2].y) > 80]
        if len(long) == 1:
            stubs = [it[1].y for it in items if abs(it[1].y - it[2].y) < 0.01 and 0 < abs(it[1].x - it[2].x) < 6]
            out.append((long[0][1].x, sorted(stubs, reverse=True), min(long[0][1].y, long[0][2].y)))
    return out


def _panel(fig, ax_x, ax_top, stubs):
    words = fig.words()
    titles = [w for w in words if w[4] in PANELS and ax_x - 30 < w[0] < ax_x + PANEL_W and w[3] < ax_top]
    if len(titles) != 1:
        raise ValueError(f"axis at {ax_x}: titles {titles}")
    name, ticks = PANELS[titles[0][4]]
    printed = sorted(float(w[4]) for w in words if ax_x - 25 < w[2] < ax_x and w[4].isdigit())
    if printed != ticks or len(stubs) != len(ticks):
        raise ValueError(f"{name}: tick labels {printed}, {len(stubs)} stubs")
    return name, calibrate(list(zip(stubs, ticks)))


def read(fig):
    groups = {}
    for ax_x, stubs, ax_top in _axes(fig):
        name, cal = _panel(fig, ax_x, ax_top, stubs)
        k = abs(cal.slope)
        mis = cal.residual / k                # calibration misfit in pt
        zero = stubs[0]
        cols = {COLUMNS[w[4]]: (w[0] + w[2]) / 2 for w in fig.words()
                if w[4] in COLUMNS and ax_x < w[0] < ax_x + PANEL_W and w[1] > zero}
        if len(cols) != 3:
            raise ValueError(f"{name}: columns {cols}")
        draws = [d for d in fig.drawings() if ax_x < d["rect"].x0 and d["rect"].x1 < ax_x + PANEL_W]
        ts = []                               # error bar Ts: (x, cap y, base y)
        for d in draws:
            it = d["items"]
            if d.get("fill") is None and len(it) == 3 and all(i[0] == "l" for i in it):
                vert = [i for i in it if abs(i[1].x - i[2].x) < 0.01 and abs(i[1].y - i[2].y) > 0.01]
                horiz = [i for i in it if abs(i[1].y - i[2].y) < 0.01]
                if len(vert) == 1 and len(horiz) == 2:
                    cap = horiz[0][1].y
                    ys = (vert[0][1].y, vert[0][2].y)
                    if abs(min(ys) - cap) > 0.01:
                        raise ValueError(f"{name}: T at {d['rect']}: cap not at the top")
                    ts.append((vert[0][1].x, cap, max(ys)))
        bars = {}
        for g, cx in cols.items():
            rs = [d["rect"] for d in draws if d["rect"].x0 < cx < d["rect"].x1 and d["rect"].width > 15
                  and d["rect"].height > 1 and (d.get("fill") == (1.0, 1.0, 1.0)
                                                or [i[0] for i in d["items"]] == ["re"])]
            if len(rs) != 2:
                raise ValueError(f"{name} {g}: {len(rs)} bar shapes")
            top = sum(r.y0 for r in rs) / 2
            gap = abs(rs[0].y0 - rs[1].y0) / 2
            t = [t for t in ts if rs[0].x0 < t[0] < rs[0].x1]
            if len(t) != 1 or abs(t[0][2] - top) > BASE_TOL:
                raise ValueError(f"{name} {g}: error bars {t} for bar top {top}")
            mean = cal.value(top)
            unc = (UNC_PT + mis + gap) * k
            err = cal.value(t[0][1])
            eunc = (UNC_PT + mis) * k
            bars[g] = {"points": [], "countable": False,
                       "bar": {"mean": [mean, mean - unc, mean + unc], "error": [err, err - eunc, err + eunc]}}
        for item, gs in ITEMS.items():
            for g in gs:
                groups[f"{name}_{item}/{g}"] = bars[g]
    if len(groups) != 8:
        raise ValueError(f"labels {sorted(groups)}")
    return {"groups": groups}
