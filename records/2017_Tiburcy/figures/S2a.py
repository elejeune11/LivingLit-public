"""Suppl. Fig. 2a (supplement p. 42): expression of five pluripotency genes relative to pluripotent stem cells
(HES2), as bars per gene for Pluripotent stem cells, Fibroblasts, Undefined EHM and Defined EHM.

Vector bar chart with a split y axis: a lower segment (ticks 0, 0.2, 0.4) and an upper one (ticks 0.8, 1.0, 1.2),
each drawn as its own axis path (a vertical line, a diagonal-free break stroke and tick stubs). Each segment is
calibrated from its own stubs, matched to the nearest printed tick label; a page y is read on the segment whose
span holds it. Bars stand in four slots per gene in legend order (PSC, fibroblasts, undefined, defined); the
fibroblast slot holds no drawing in any gene, so no fibroblast bar is read. A bar's slot is its offset from the
gene's black (PSC) bar in units of the slot pitch. Each bar is a filled path (the PSC bars are drawn in two
pieces, one per axis segment); the mean is the top of its highest piece. Error bars are drawn upward only: a
3-line path (cap and stem) standing on the bar top; 'error' is the cap. Bars lower than about 0.3 pt carry no
drawn error bar. Means only: no single sample is drawn (countable false).
"""
from livinglit.figures.source import calibrate

UNC_PT = 0.5
GENES = ["NANOG", "POU5F1", "ZFP42", "FGF4", "TERT"]
SLOTS = ["psc", "hff", "undef", "def"]          # legend order, left to right in each gene
ITEM_GROUPS = {g: ["def", "undef"] for g in GENES[:4]} | {"TERT": ["psc", "undef", "def"]}
TICK_STUB = (4.0, 7.0)                          # stub length range (pt)


def _axis_segments(fig):
    """Each y-axis segment: (y_top, y_bottom, [(stub y, tick value)])."""
    labels = [((w[1] + w[3]) / 2, float(w[4]), w[2]) for w in fig.words()
              if w[4].replace(".", "", 1).isdigit()]
    segs = []
    for d in fig.drawings():
        its = d["items"]
        if d.get("fill") is not None or not its or any(it[0] != "l" for it in its):
            continue
        a, b = its[0][1], its[0][2]
        if abs(a.x - b.x) > 0.01 or abs(a.y - b.y) < 30:
            continue
        stubs = [it[1].y for it in its[1:] if abs(it[1].y - it[2].y) < 0.01
                 and TICK_STUB[0] < abs(it[1].x - it[2].x) < TICK_STUB[1] and max(it[1].x, it[2].x) <= a.x + 0.01]
        if len(stubs) < 2:               # bar outlines: vertical edges, no tick stubs
            continue
        marks = []
        for y in stubs:
            near = [lab for lab in labels if lab[2] < a.x and abs(lab[0] - y) < 3]
            if len(near) != 1:
                raise ValueError(f"tick stub at y={y:.1f}: {len(near)} labels")
            marks.append((y, near[0][1]))
        segs.append((min(a.y, b.y), max(a.y, b.y), a.x, marks))
    if len(segs) != 2:
        raise ValueError(f"found {len(segs)} y-axis segments")
    return segs


def read(fig):
    segs = _axis_segments(fig)
    axis_x = segs[0][2]
    cals = [(top, bot, calibrate(marks)) for top, bot, _, marks in segs]

    def seg_of(y):
        for top, bot, cal in cals:
            if top - 0.01 <= y <= bot + 0.01:
                return cal
        raise ValueError(f"y={y:.2f} lies in the axis break")

    def reading(y):
        cal = seg_of(y)
        unc = UNC_PT + abs(cal.residual / cal.slope)
        return [cal.value(y), *cal.interval(y, unc)]

    genes = {w[4]: (w[0] + w[2]) / 2 for w in fig.words() if w[4] in GENES}
    if sorted(genes) != sorted(GENES):
        raise ValueError(f"gene labels {sorted(genes)}")
    gene_of = lambda x: min(genes, key=lambda g: abs(genes[g] - x))

    bars = {g: {} for g in GENES}        # gene -> x0 -> [(filled rect, grey level)]
    whiskers = {g: [] for g in GENES}    # gene -> (x centre, cap y, stem bottom y)
    for d in fig.drawings():
        r, its = d["rect"], d["items"]
        if r.x0 <= axis_x + 1 or r.y1 > max(b for _, b, _ in cals) + 0.5:
            continue
        if d.get("fill") is not None and len(its) == 4 and 6 < r.width < 10:
            bars[gene_of((r.x0 + r.x1) / 2)].setdefault(round(r.x0, 1), []).append((r, max(d["fill"])))
        elif d.get("fill") is None and len(its) == 3 and r.width < 5 and all(it[0] == "l" for it in its):
            whiskers[gene_of((r.x0 + r.x1) / 2)].append(((r.x0 + r.x1) / 2, r.y0, r.y1))

    out = {}
    for g in GENES:
        cols = sorted(bars[g].items())
        black = [x0 for x0, rs in cols if all(f < 0.05 for _, f in rs)]
        if len(black) != 1:
            raise ValueError(f"{g}: {len(black)} black PSC bars")
        pitch = cols[-1][0] - cols[-2][0] if len(cols) >= 2 else None
        named = {}
        for x0, rs in cols:
            k = (x0 - black[0]) / pitch
            if abs(k - round(k)) > 0.05:
                raise ValueError(f"{g}: bar at x={x0} is off the slot grid")
            named[SLOTS[round(k)]] = [r for r, _ in rs]
        if "hff" in named or sorted(named) != sorted(["psc", "undef", "def"]):
            raise ValueError(f"{g}: slots {sorted(named)}")
        for grp in ITEM_GROUPS[g]:
            rs = named[grp]
            top = min(r.y0 for r in rs)
            xc = (rs[0].x0 + rs[0].x1) / 2
            bar = {"mean": reading(top)}
            w = [c for c in whiskers[g] if abs(c[0] - xc) < 0.5 and abs(c[2] - top) < 0.15]
            if len(w) > 1:
                raise ValueError(f"{g}/{grp}: {len(w)} error bars")
            if w:
                bar["error"] = reading(w[0][1])
            out[f"S2a_{g}/{grp}"] = {"points": [], "countable": False, "bar": bar}
    return {"groups": out}

