"""Suppl. Fig. 7 (supplement p. 51): RPKM of 18 cardiomyocyte genes in three panels (Sarcomere, Ion channels,
Calcium handling), each a log y axis (10^-1 or 10^0 up to 10^5) with one cluster of seven bars per gene. The bars are
group means with one error bar each; no sample is drawn, so every bar is returned as a bar (mean, upper error end),
with no points and no n.

The page is vector. Each panel has one y axis path (axis line plus tick stubs), calibrated on a log scale from the
stubs matched to the '10' labels left of them, each with its exponent word (superscript) to its right. The baseline
of the bars is the 10^0 stub. A bar is a rectangle 3.5-4.5 pt wide with one horizontal edge on the baseline: it rises
for values above 1 (mean = top edge) and hangs below for values under 1 (mean = bottom edge). Rectangles and error paths
drawn twice (all of MYOM2) are kept once. The gene of a bar is the gene name centred over its cluster; within a cluster the seven bars, left to
right, follow the legend, top to bottom (the legend swatch fills are checked against the bar fills, with the
exceptions listed in FILL_EXCEPTIONS, each of which must be seen).

Each error bar is one path: a cap and a stem from the cap to the bar's free end, centred on the bar (once, a cap alone with no
stem, within 1 pt of the bar top). On a rising bar
the cap is above and is 'error'. On a hanging bar the cap is below (the lower end; on a log axis the upper end is not
drawn), so only the mean is returned.
"""
from livinglit.figures.source import calibrate, point

UNC_PT = 0.5
GENES = ["MYH7", "MYL2", "TTN", "CKM", "TNNI3", "TNNT1", "ACTN2", "MYOM2", "SCN5A", "SCN2B", "KCNQ1", "KCNJ4",
         "KCNJ12", "RYR2", "CASQ2", "ATP2A2", "PLN", "TRDN"]
LEGEND = {"2D D22": "d22", "2D D60": "d60", "EHM serum W2": "ehm_serum_w2", "EHM serum-free W2": "ehm_sf_w2",
          "EHM serum-free W6": "ehm_sf_w6", "Fetal heart": "fetal", "Adult heart": "adult"}
# (gene, group): fills of that bar that differ from its legend swatch (None: outline only)
FILL_EXCEPTIONS = {("TNNT1", "ehm_sf_w6"): {0.628}, ("SCN2B", "ehm_serum_w2"): {None}}
ON = 0.2                         # pt: a bar edge lies on the baseline; a stem is centred on a bar
TOUCH = 1.0                      # pt: an error stem reaches the bar's free end
LABEL = 4.0                      # pt: a '10' label sits by its stub (Calcium handling labels are up to 3.5 pt off;
                                 # the stubs, evenly spaced, are the calibration and each takes the one label near it)


def _kind(d):
    return "".join(i[0] for i in d["items"])


def _fill(d):
    f = d.get("fill")
    return None if f is None else round(f[0], 3)


def _axes(draws):
    """Vertical axis paths (one line plus horizontal stubs): [(x, sorted stub ys, top)]."""
    out = []
    for d in draws:
        r = d["rect"]
        if set(_kind(d)) == {"l"} and len(d["items"]) >= 4 and r.height > 100 and r.width < 2:
            stubs = sorted(i[1].y for i in d["items"] if abs(i[1].y - i[2].y) < 0.01)
            out.append((r.x1, stubs, r.y0))
    return out


def _ycal(words, ax_x, stubs):
    """Log calibration from '10' labels with exponent words, each on a stub; and the 10^0 stub."""
    marks = []
    for s in stubs:
        ten = [w for w in words if w[4] == "10" and ax_x - 20 < w[2] < ax_x and abs((w[1] + w[3]) / 2 - s) < LABEL]
        if len(ten) != 1:
            raise ValueError(f"axis at x {ax_x:.1f}: stub {s:.1f} has labels {ten}")
        t = ten[0]
        exp = [w for w in words if abs(w[0] - t[2]) < 1.5 and w[1] < t[1] and t[1] - w[1] < 3]
        if len(exp) != 1:
            raise ValueError(f"axis at x {ax_x:.1f}: stub {s:.1f} exponent {exp}")
        marks.append((s, 10.0 ** int(exp[0][4])))
    vals = [v for _, v in sorted(marks)][::-1]
    if any(b / a != 10 for a, b in zip(vals, vals[1:])) or 1.0 not in vals:
        raise ValueError(f"axis at x {ax_x:.1f}: tick values {vals}")
    base = [s for s, v in marks if v == 1.0][0]
    return calibrate(marks, log=True), base


def _legend(draws, words):
    """[(group, swatch fill)] top to bottom."""
    out = []
    for d in draws:
        r = d["rect"]
        if _kind(d) == "llll" and 9 < r.width < 10 and 6 < r.height < 7.5:
            cy = (r.y0 + r.y1) / 2
            text = " ".join(w[4] for w in sorted(words) if r.x1 < w[0] < r.x1 + 120 and abs((w[1] + w[3]) / 2 - cy) < 3)
            if text not in LEGEND:
                raise ValueError(f"legend swatch at y {cy:.1f}: text {text!r}")
            out.append((cy, LEGEND[text], _fill(d)))
    out.sort()
    if [g for _, g, _ in out] != list(LEGEND.values()):
        raise ValueError(f"legend order {[g for _, g, _ in out]}")
    return [(g, f) for _, g, f in out]


def _bars(draws, ax_x, base):
    """{rounded rect: (rect, fills)} for bars standing on or hanging from the baseline right of an axis."""
    out = {}
    for d in draws:
        r, k = d["rect"], _kind(d)
        if k not in ("llll", "lllll") or not (3.5 < r.width < 4.5) or r.x0 < ax_x + 5:
            continue
        if abs(r.y1 - base) > ON and abs(r.y0 - base) > ON:
            continue
        key = tuple(round(v, 2) for v in r)
        out.setdefault(key, (r, set()))[1].add(_fill(d))
    return out


def read(fig):
    draws, words = fig.drawings(), fig.words()
    legend = _legend(draws, words)
    caps = [d for d in draws if _kind(d) == "lll" and d.get("fill") is None]
    caps_only = [d for d in draws if _kind(d) == "ll" and d.get("fill") is None and d["rect"].height < 0.01
                 and d["rect"].width < 3]
    groups, genes_seen, exceptions_seen = {}, [], set()
    axes = _axes(draws)
    if len(axes) != 3:
        raise ValueError(f"{len(axes)} y axes")
    for ax_x, stubs, top in axes:
        cal, base = _ycal(words, ax_x, stubs)
        unc = UNC_PT + cal.residual / abs(cal.slope)
        names = [w for w in words if w[4] in GENES and top - 25 < (w[1] + w[3]) / 2 < top + 15]
        bars = _bars(draws, ax_x, base)
        clusters = {w[4]: [] for w in names}
        for r, fills in bars.values():
            cx = (r.x0 + r.x1) / 2
            near = min(names, key=lambda w: abs((w[0] + w[2]) / 2 - cx))
            if abs((near[0] + near[2]) / 2 - cx) > 25:
                raise ValueError(f"bar at x {cx:.1f} has no gene name over it")
            clusters[near[4]].append((r, fills))
        for gene, cl in clusters.items():
            if len(cl) != len(legend):
                raise ValueError(f"{gene}: {len(cl)} bars")
            genes_seen.append(gene)
            for (r, fills), (group, swatch) in zip(sorted(cl, key=lambda b: b[0].x0), legend):
                exc = FILL_EXCEPTIONS.get((gene, group))
                if exc is not None and exc <= fills:
                    exceptions_seen.add((gene, group))
                elif swatch not in fills:
                    raise ValueError(f"{gene} {group}: fills {fills}, legend {swatch}")
                cx = (r.x0 + r.x1) / 2
                rising = abs(r.y1 - base) <= ON and r.y0 < base - ON
                end = r.y0 if rising else r.y1
                bar = {"mean": _triple(cal, end, unc)}
                stems = [c for c in caps if abs(c["items"][-1][1].x - cx) < ON
                         and abs(c["items"][-1][1].x - c["items"][-1][2].x) < 0.01]
                on = [c for c in stems if min(abs(c["items"][-1][2].y - end), abs(c["items"][-1][1].y - end)) < TOUCH]
                on = list({tuple(round(v, 2) for v in c["rect"]): c for c in on}.values())   # paths drawn twice
                if not on:                    # a cap alone, its stem too short to draw (CKM EHM serum-free W2)
                    on = [c for c in caps_only if abs((c["rect"].x0 + c["rect"].x1) / 2 - cx) < ON
                          and abs(c["rect"].y0 - end) < TOUCH]
                if len(on) > 1:
                    raise ValueError(f"{gene} {group}: {len(on)} error paths")
                if on:
                    cap_y = on[0]["items"][0][1].y
                    if (cap_y < end) != rising and abs(cap_y - end) > ON:
                        raise ValueError(f"{gene} {group}: error cap on the wrong side of the bar end")
                    if rising:
                        bar["error"] = _triple(cal, cap_y, unc)
                groups[f"S7_{gene}/{group}"] = {"points": [], "countable": False, "bar": bar}
    if sorted(genes_seen) != sorted(GENES):
        raise ValueError(f"genes read {genes_seen}")
    if exceptions_seen != set(FILL_EXCEPTIONS):
        raise ValueError(f"fill exceptions seen {exceptions_seen}")
    return {"groups": groups}


def _triple(cal, pos, unc):
    p = point(cal, pos, unc, (0, 0))
    return [p["value"], p["lo"], p["hi"]]
