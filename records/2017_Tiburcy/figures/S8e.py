"""Suppl. Fig. 8e (supplement p. 53): normalized force of contraction (FOC, %) after 100 nmol/L isoprenaline alone or
after pre-incubation with CGP-20712A (beta1 block), ICI-118551 (beta2 block) or both; HES2 EHM. Four bars, each a group
mean with one error bar; no single EHM is drawn, so every bar is returned as a bar (mean, error end), no points, no n.

The page is vector. The y axis is one path (axis line plus seven tick stubs), calibrated linearly from the stubs matched
to the numeric labels left of them (-25 ... 125). Every bar is a white rectangle about 33 pt wide; for a bar above zero
its mean is the top edge. A bar's treatment is read from the '+'/'-' signs in the three rows under it (rows told by the
row words 'Isoprenaline', 'CGP-20712A', 'ICI'). Each error bar is one path: a cap and a stem from the cap to the bar end,
centred on the bar; the cap is 'error'. Only the groups the items use are returned (the 'both blockers' bar, whose mean
lies just below zero with a downward error bar, is in no item).
"""
from livinglit.figures.source import calibrate, point

UNC_PT = 0.5
TICKS = [-25, 0, 25, 50, 75, 100, 125]
ROWS = ["Isoprenaline", "CGP-20712A", "ICI"]
GROUPS = {"+--": "iso", "++-": "iso_cgp", "+-+": "iso_ici", "+++": "iso_both"}
ITEMS = {"iso": ["S8e_adrb1"], "iso_cgp": ["S8e_adrb1", "S8e_cgp_ici"], "iso_ici": ["S8e_cgp_ici"], "iso_both": []}
ON = 0.5      # pt: a stem is centred on a bar and reaches its top
LABEL = 2.0   # pt: a tick label is centred on its stub
ROW = 5.0     # pt: a sign sits on its row (rows are ~16 pt apart; '+' and '-' glyph boxes differ by ~2 pt)


def _kind(d):
    return "".join(i[0] for i in d["items"])


def _axis(draws):
    axes = [d for d in draws if set(_kind(d)) == {"l"} and len(d["items"]) >= 5
            and d["rect"].height > 100 and d["rect"].width < 5]
    if len(axes) != 1:
        raise ValueError(f"{len(axes)} y axes")
    d = axes[0]
    return d["rect"].x1, sorted(i[1].y for i in d["items"] if abs(i[1].y - i[2].y) < 0.01)


def _ycal(words, ax_x, stubs):
    marks = []
    for s in stubs:
        lab = [w for w in words if ax_x - 30 < w[2] < ax_x and abs((w[1] + w[3]) / 2 - s) < LABEL
               and w[4].lstrip("-").isdigit()]
        if len(lab) != 1:
            raise ValueError(f"stub {s:.1f} has labels {lab}")
        marks.append((s, float(lab[0][4])))
    if sorted(v for _, v in marks) != TICKS:
        raise ValueError(f"tick values {marks}")
    return calibrate(marks)


def _triple(cal, pos, unc):
    p = point(cal, pos, unc, (0, 0))
    return [p["value"], p["lo"], p["hi"]]


def read(fig):
    draws, words = fig.drawings(), fig.words()
    ax_x, stubs = _axis(draws)
    cal = _ycal(words, ax_x, stubs)
    unc = UNC_PT + cal.residual / abs(cal.slope)
    rows = []
    for name in ROWS:
        w = [w for w in words if w[4] == name and w[2] < ax_x + 15]
        if len(w) != 1:
            raise ValueError(f"row word {name}: {w}")
        rows.append((w[0][1] + w[0][3]) / 2)
    bars = [d["rect"] for d in draws if _kind(d) == "re" and 25 < d["rect"].width < 45 and d["rect"].x0 > ax_x]
    caps = [d for d in draws if _kind(d) == "lll" and abs(d["items"][-1][1].x - d["items"][-1][2].x) < 0.01]
    if len(bars) != 4:
        raise ValueError(f"{len(bars)} bars")
    groups, seen = {}, set()
    for r in bars:
        cx = (r.x0 + r.x1) / 2
        signs = ""
        for y in rows:
            s = [w for w in words if w[4] in "+-" and abs((w[1] + w[3]) / 2 - y) < ROW and abs((w[0] + w[2]) / 2 - cx) < 8]
            if len(s) != 1:
                raise ValueError(f"bar at x {cx:.1f}: signs {s} on row {y:.1f}")
            signs += s[0][4]
        group = GROUPS[signs]
        seen.add(group)
        if not ITEMS[group]:
            continue
        on = [c for c in caps if abs(c["items"][-1][1].x - cx) < ON and abs(c["items"][-1][2].y - r.y0) < ON]
        if len(on) != 1:
            raise ValueError(f"{group}: {len(on)} error paths")
        bar = {"mean": _triple(cal, r.y0, unc), "error": _triple(cal, on[0]["items"][0][1].y, unc)}
        for item in ITEMS[group]:
            groups[f"{item}/{group}"] = {"points": [], "countable": False, "bar": bar}
    if seen != set(GROUPS.values()):
        raise ValueError(f"treatments found {sorted(seen)}")
    return {"groups": groups}
