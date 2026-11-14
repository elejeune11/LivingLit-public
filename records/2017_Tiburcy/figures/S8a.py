"""Suppl. Fig. 8a (supplement p. 53): RPKM of nine adrenoceptor genes (ADRA1A ... ADRB3) on one log y axis
(10^-2 to 10^2), one cluster of seven bars per gene. The bars are group means with one error bar each; no sample is
drawn, so every bar is returned as a bar (mean, upper error end), with no points and no n.

The page is vector. The y axis is one path (axis line plus five tick stubs), calibrated on a log scale from the stubs
matched to the '10' labels left of them, each with its exponent word (superscript) to its right. Every bar is a
rectangle about 4.1 pt wide rising from the bottom stub (10^-2), so its mean is its top edge. The gene of a bar is the
(rotated) gene name centred under its cluster; within a cluster the seven bars, left to right, follow the legend, top
to bottom (each bar's fill is checked against its legend swatch).

Each error bar is one path: a cap and a stem from the cap down to the bar top, centred on the bar; the cap is 'error'.
One slot has an error path but no bar (ADRB3, adult heart: listed in NO_BAR, which must be seen): its stem ends on
the axis floor, so the mean lies below 10^-2 and is not drawn; only the upper error end is returned.
"""
from livinglit.figures.source import calibrate, point

UNC_PT = 0.5
GENES = ["ADRA1A", "ADRA1B", "ADRA1D", "ADRA2A", "ADRA2B", "ADRA2C", "ADRB1", "ADRB2", "ADRB3"]
LEGEND = {"2D D22": "d22", "2D D60": "d60", "EHM serum W2": "ehm_serum_w2", "EHM SF W2": "ehm_sf_w2",
          "EHM SF W6": "ehm_sf_w6", "Fetal heart": "fetal", "Adult heart": "adult"}
NO_BAR = {("ADRB3", "adult")}    # error path standing on the axis floor, no bar drawn
ON = 0.2                         # pt: a bar edge lies on the floor; a stem is centred on a bar
TOUCH = 1.0                      # pt: an error stem reaches the bar top
LABEL = 2.0                      # pt: a '10' label is centred on its stub


def _kind(d):
    return "".join(i[0] for i in d["items"])


def _fill(d):
    f = d.get("fill")
    return None if f is None else round(f[0], 3)


def _axis(draws):
    """The vertical axis path (one line plus horizontal stubs): (x, sorted stub ys)."""
    out = []
    for d in draws:
        r = d["rect"]
        # a bar is a closed 4-line rectangle as narrow as the stubs; the axis has its line plus >= 4 stubs
        if set(_kind(d)) == {"l"} and len(d["items"]) >= 5 and r.height > 100 and r.width < 5:
            stubs = sorted(i[1].y for i in d["items"] if abs(i[1].y - i[2].y) < 0.01)
            out.append((r.x1, stubs))
    if len(out) != 1:
        raise ValueError(f"{len(out)} y axes")
    return out[0]


def _ycal(words, ax_x, stubs):
    """Log calibration from '10' labels with exponent words, each on a stub; and the floor (lowest stub)."""
    marks = []
    for s in stubs:
        ten = [w for w in words if w[4] == "10" and ax_x - 25 < w[2] < ax_x and abs((w[1] + w[3]) / 2 - s) < LABEL]
        if len(ten) != 1:
            raise ValueError(f"stub {s:.1f} has labels {ten}")
        t = ten[0]
        exp = [w for w in words if abs(w[0] - t[2]) < 1.5 and w[1] < t[1] and t[1] - w[1] < 3]
        if len(exp) != 1:
            raise ValueError(f"stub {s:.1f} exponent {exp}")
        marks.append((s, 10.0 ** int(exp[0][4].replace("−", "-"))))
    vals = [v for _, v in sorted(marks)][::-1]
    if any(b / a != 10 for a, b in zip(vals, vals[1:])):
        raise ValueError(f"tick values {vals}")
    return calibrate(marks, log=True), max(stubs)


def _legend(draws, words):
    """[(group, swatch fill)] top to bottom."""
    out = []
    for d in draws:
        r = d["rect"]
        if _kind(d) == "llll" and 14 < r.width < 17 and 7 < r.height < 8.5:
            cy = (r.y0 + r.y1) / 2
            text = " ".join(w[4] for w in sorted(words) if r.x1 < w[0] < r.x1 + 100 and abs((w[1] + w[3]) / 2 - cy) < 3)
            if text not in LEGEND:
                raise ValueError(f"legend swatch at y {cy:.1f}: text {text!r}")
            out.append((cy, LEGEND[text], _fill(d)))
    out.sort()
    if [g for _, g, _ in out] != list(LEGEND.values()):
        raise ValueError(f"legend order {[g for _, g, _ in out]}")
    return [(g, f) for _, g, f in out]


def _stem(c):
    """(x, top y, bottom y) of an error path's vertical stem."""
    a, b = c["items"][-1][1], c["items"][-1][2]
    return a.x, min(a.y, b.y), max(a.y, b.y)


def read(fig):
    draws, words = fig.drawings(), fig.words()
    legend = _legend(draws, words)
    ax_x, stubs = _axis(draws)
    cal, floor = _ycal(words, ax_x, stubs)
    unc = UNC_PT + cal.residual / abs(cal.slope)
    names = [w for w in words if w[4] in GENES and w[1] > floor]
    if sorted(w[4] for w in names) != sorted(GENES):
        raise ValueError(f"gene names {[w[4] for w in names]}")
    caps = [d for d in draws if _kind(d) == "lll" and d.get("fill") is None
            and abs(d["items"][-1][1].x - d["items"][-1][2].x) < 0.01]
    bars = [d["rect"] for d in draws if _kind(d) == "llll" and 3.5 < d["rect"].width < 4.5
            and abs(d["rect"].y1 - floor) <= ON and d["rect"].x0 > ax_x + 2]
    # slots: a bar, or an error path standing on the floor with no bar under it
    slots = [((r.x0 + r.x1) / 2, r) for r in bars]
    for c in caps:
        x, _, bottom = _stem(c)
        if abs(bottom - floor) <= ON and not any(r.x0 - ON <= x <= r.x1 + ON for r in bars):
            slots.append((x, None))
    clusters = {w[4]: [] for w in names}
    for cx, r in slots:
        near = min(names, key=lambda w: abs((w[0] + w[2]) / 2 - cx))
        if abs((near[0] + near[2]) / 2 - cx) > 25:
            raise ValueError(f"bar at x {cx:.1f} has no gene name under it")
        clusters[near[4]].append((cx, r))
    fills = {tuple(round(v, 2) for v in d["rect"]): _fill(d) for d in draws if _kind(d) == "llll"}
    groups, no_bar_seen = {}, set()
    for gene, cl in clusters.items():
        if len(cl) != len(legend):
            raise ValueError(f"{gene}: {len(cl)} bars")
        for (cx, r), (group, swatch) in zip(sorted(cl, key=lambda s: s[0]), legend):
            on = [c for c in caps if abs(_stem(c)[0] - cx) < ON]
            if r is None:
                no_bar_seen.add((gene, group))
                if len(on) != 1:
                    raise ValueError(f"{gene} {group}: {len(on)} error paths without a bar")
                bar = {"error": _triple(cal, on[0]["items"][0][1].y, unc)}
            else:
                f = fills[tuple(round(v, 2) for v in r)]
                if f != swatch:
                    raise ValueError(f"{gene} {group}: fill {f}, legend {swatch}")
                bar = {"mean": _triple(cal, r.y0, unc)}
                on = [c for c in on if abs(_stem(c)[2] - r.y0) < TOUCH]
                if len(on) > 1:
                    raise ValueError(f"{gene} {group}: {len(on)} error paths")
                if on:
                    cap_y = on[0]["items"][0][1].y
                    if cap_y > r.y0 + ON:
                        raise ValueError(f"{gene} {group}: error cap below the bar top")
                    bar["error"] = _triple(cal, cap_y, unc)
            groups[f"S8a_{gene}/{group}"] = {"points": [], "countable": False, "bar": bar}
    if no_bar_seen != NO_BAR:
        raise ValueError(f"slots without a bar {no_bar_seen}")
    return {"groups": groups}


def _triple(cal, pos, unc):
    p = point(cal, pos, unc, (0, 0))
    return [p["value"], p["lo"], p["hi"]]
