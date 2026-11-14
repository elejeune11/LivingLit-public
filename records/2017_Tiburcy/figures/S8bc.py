"""Suppl. Fig. 8b,c (supplement p. 53): change in force of contraction (FOC, % change) in response to 1 µmol/L
isoprenaline, (b) hiPS-G1 EHM and (c) HES2 EHM, three bars each (Starting, Matrix, Serum-free protocol). The bars are
group means with an upper error bar only; no sample is drawn, so every bar is returned as a bar (mean, upper error
end), with no points and no n.

The page is vector. Each panel has one y axis path (axis line plus six tick stubs), calibrated linearly from the
stubs matched to the numeric labels left of them (0 ... 100). A panel is told by its title word ('hiPS-G1' or 'HES2')
above its axis. Every bar is a white rectangle about 43 pt wide standing on the axis floor (lowest stub), so its mean
is its top edge; the protocol of a bar is the category word ('Starting', 'Matrix', 'Serum-free') centred under it.
Each error bar is one path: a cap and a stem from the cap down to the bar top, centred on the bar; the cap is 'error'.
"""
from livinglit.figures.source import calibrate, point

UNC_PT = 0.5
PANELS = {"hiPS-G1": "g1", "HES2": "hes2"}
PROTOCOLS = {"Starting": "start", "Matrix": "matrix", "Serum-free": "sf"}
ITEMS = {"sf": ["start", "matrix"], "start": ["start"], "matrix": ["matrix"]}
ON = 0.5      # pt: a bar edge lies on the floor; a stem is centred on a bar; a stem reaches the bar top
LABEL = 2.0   # pt: a tick label is centred on its stub


def _kind(d):
    return "".join(i[0] for i in d["items"])


def _axes(draws):
    """Vertical axis paths (one line plus horizontal stubs): [(x, sorted stub ys)]."""
    out = []
    for d in draws:
        r = d["rect"]
        if set(_kind(d)) == {"l"} and len(d["items"]) >= 5 and r.height > 100 and r.width < 5:
            stubs = sorted(i[1].y for i in d["items"] if abs(i[1].y - i[2].y) < 0.01)
            out.append((r.x1, stubs))
    return sorted(out)


def _ycal(words, ax_x, stubs):
    marks = []
    for s in stubs:
        lab = [w for w in words if ax_x - 30 < w[2] < ax_x and abs((w[1] + w[3]) / 2 - s) < LABEL]
        if len(lab) != 1:
            raise ValueError(f"stub {s:.1f} has labels {lab}")
        marks.append((s, float(lab[0][4])))
    vals = [v for _, v in sorted(marks)][::-1]
    if vals != [0, 20, 40, 60, 80, 100]:
        raise ValueError(f"tick values {vals}")
    return calibrate(marks), max(stubs)


def _stem(c):
    a, b = c["items"][-1][1], c["items"][-1][2]
    return a.x, min(a.y, b.y), max(a.y, b.y)


def _triple(cal, pos, unc):
    p = point(cal, pos, unc, (0, 0))
    return [p["value"], p["lo"], p["hi"]]


def read(fig):
    draws, words = fig.drawings(), fig.words()
    axes = _axes(draws)
    if len(axes) != 2:
        raise ValueError(f"{len(axes)} y axes")
    caps = [d for d in draws if _kind(d) == "lll" and d.get("fill") is None
            and abs(d["items"][-1][1].x - d["items"][-1][2].x) < 0.01]
    groups = {}
    for i, (ax_x, stubs) in enumerate(axes):
        right = axes[i + 1][0] - 30 if i + 1 < len(axes) else float("inf")
        cal, floor = _ycal(words, ax_x, stubs)
        unc = UNC_PT + cal.residual / abs(cal.slope)
        title = [w for w in words if w[4] in PANELS and w[3] < min(stubs) and ax_x - 10 < w[0] < right]
        if len(title) != 1:
            raise ValueError(f"axis at x {ax_x:.1f}: titles {title}")
        line = PANELS[title[0][4]]
        cats = [w for w in words if w[4] in PROTOCOLS and w[1] > floor and ax_x < w[0] < right]
        bars = [d["rect"] for d in draws if _kind(d) == "llll" and 30 < d["rect"].width < 60
                and abs(d["rect"].y1 - floor) <= ON and ax_x < d["rect"].x0 < right]
        if len(bars) != 3 or sorted(w[4] for w in cats) != sorted(PROTOCOLS):
            raise ValueError(f"{line}: {len(bars)} bars, categories {[w[4] for w in cats]}")
        for r in bars:
            cx = (r.x0 + r.x1) / 2
            cat = min(cats, key=lambda w: abs((w[0] + w[2]) / 2 - cx))
            if abs((cat[0] + cat[2]) / 2 - cx) > 5:
                raise ValueError(f"{line}: bar at x {cx:.1f} has no category under it")
            proto = PROTOCOLS[cat[4]]
            bar = {"mean": _triple(cal, r.y0, unc)}
            on = [c for c in caps if abs(_stem(c)[0] - cx) < ON and abs(_stem(c)[2] - r.y0) < ON]
            if len(on) != 1:
                raise ValueError(f"{line} {proto}: {len(on)} error paths")
            bar["error"] = _triple(cal, on[0]["items"][0][1].y, unc)
            for other in ITEMS[proto]:    # items compare serum-free with start or matrix, within one line
                groups[f"S8bc_{line}_sf_{line}_{other}/{line}_{proto}"] = {"points": [], "countable": False, "bar": bar}
    return {"groups": groups}
