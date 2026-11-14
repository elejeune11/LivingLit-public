"""Fig. 7I-K (main.pdf p. 14, raster): Ca2+ decay, diastolic Ca2+ and beating frequency, d30 / endo+d30 / CMM / endo+CMM.

I (time for Ca2+ decay, s-1) and J (diastolic Ca2+, ΔF/F) are open bars (mean) with black SD whiskers and a
column of coloured discs per bar (n = 39 cells, legend). The discs overlap one another heavily in every column,
so no column is countable: each bar is read as its mean (the bar's top edge) and the upper end of its SD whisker
(the upper cap), countable: false, no points. Bar outlines and whiskers are grey/black; the discs are saturated
colours, so a line pixel is one with low saturation, and disc pixels carry no weight in a line's centre. The upper
caps of J d30 and J CMM lie wholly under their discs and are not read (those bars give a mean only).
K (BPM) is four violins, each with a black dashed median line and 4-5 small dots (n not stated). Several dots sit
on the violin outline or on the median dashes, so the dots do not each stand alone: each violin is read as its
median only (countable: false). Fig. 7H (peak amplitude) is bars with SD whiskers and no points; it is not read.
Axes are calibrated from the major ticks; tick values are the printed labels.
"""
import numpy as np

from livinglit.figures.source import calibrate

DPI = 300
TICKS = {  # printed tick labels, top to bottom
    "I": [1.3, 1.2, 1.1, 1.0, 0.9, 0.8],
    "J": [0.6, 0.4, 0.2, 0.0],
    "K": [150, 100, 50, 0],
}
LABELS = {  # left to right, as printed under each panel
    "I": ["d30", "endo+d30", "CMM", "endo+CMM"],
    "J": ["d30", "endo+d30", "CMM", "endo+CMM"],
    "K": ["d30", "d30+endo", "CMM", "CMM+endo"],
}
PANEL_WINDOWS = [(0, 300), (300, 700), (700, None)]  # x windows (px) holding one y axis each: I, J, K


def _runs(idx, gap=1):
    out = []
    for i in idx:
        if out and i - out[-1][1] <= gap:
            out[-1][1] = i
        else:
            out.append([i, i])
    return out


def _centre(I, a, b, cols):
    """Darkness-weighted row centre of a horizontal line spanning rows a..b, over the given columns; disc pixels
    (saturated colour) carry no weight."""
    r = np.arange(a - 1, b + 2)
    px = I[a - 1:b + 2][:, cols]
    w = np.where(px.max(2) - px.min(2) < 60, 255 - px.max(2), 0).clip(0).sum(1).astype(float)
    return float((r * w).sum() / w.sum())


def read(fig):
    img, _ = fig.render(DPI)
    I = img.astype(int)
    mx, sat = I.max(2), I.max(2) - I.min(2)
    dark = mx < 90
    line = (mx < 200) & (sat < 60)  # grey or black line pixel, not a coloured disc
    W = I.shape[1]

    groups = {}
    for panel, (w0, w1) in zip("IJK", PANEL_WINDOWS):
        w1 = W if w1 is None else w1
        ax = w0 + int(np.argmax(dark[:, w0:w1].sum(0)))
        x1 = min(W, ax + 340)
        base = int(np.argmax(dark[:, ax + 2:x1].sum(1)))
        tick_rows = [r for r in range(base + 2) if dark[r, ax - 5:ax - 1].all()]
        ticks = [(a + b) / 2 for a, b in _runs(tick_rows)]
        assert len(ticks) == len(TICKS[panel]), (panel, ticks)
        cal = calibrate(list(zip(ticks, TICKS[panel])))
        unc = 0.6 + cal.residual / abs(cal.slope)  # px at 300 dpi, plus calibration misfit

        if panel in "IJ":
            # bar sides: columns of line pixels just above the baseline (discs sit well above it)
            low = line[base - 25:base - 2, ax + 5:x1].sum(0)
            sides = [(a + b) / 2 + ax + 5 for a, b in _runs(np.where(low >= 18)[0])]
            assert len(sides) == 2 * len(LABELS[panel]), (panel, sides)
            for k, label in enumerate(LABELS[panel]):
                L, R = int(round(sides[2 * k])), int(round(sides[2 * k + 1]))
                inner = np.arange(L + 2, R - 1)
                # side tops: follow each side line up from the baseline through line or disc pixels until white
                side_top = []
                for s in (L, R):
                    r, last = base - 3, base - 3
                    while r > 0 and (line[r, s - 1:s + 2].any() or (sat[r, s - 1:s + 2] >= 60).any()):
                        if line[r, s - 1:s + 2].any():
                            last = r
                        r -= 1
                    side_top.append(last)
                # bar top: the row band where a quarter of the bar's width is line pixels, at the top of the sides (discs may
                # hide the sides' last few rows; caps and significance brackets lie well above or below)
                cnt = line[:base - 5][:, inner].sum(1)
                tops = [t for t in _runs(np.where(cnt >= 0.25 * len(inner))[0])
                        if t[1] >= min(side_top) - 8 and t[0] <= min(side_top) + 1]
                assert tops, (panel, label, side_top)
                a, b = tops[-1]  # the nearest to the sides' top (a short whisker's cap may lie just above)
                clear = [c for c in inner if line[a:b + 1, c].any()]
                y_mean = _centre(I, a, b, clear)
                bar = {"mean": [cal.value(y_mean), *cal.interval(y_mean, unc)]}
                # upper SD cap: the nearest short horizontal line above the bar top, centred on the whisker: unbroken
                # across its 15 px except where discs cover it, nothing beside it, and the whisker (line or
                # disc pixels, never white) running from it down to the bar top. At least 5 contiguous neutral ink
                # pixels must show: where dark-green discs overlap, their edges are green-tinted mid grey and also
                # pass as line pixels. A cap that discs hide (all but short pieces) is not read.
                cx = int(round((L + R) / 2))
                win = np.arange(cx - 8, cx + 9)
                core = np.arange(cx - 7, cx + 8)
                solid = line | (sat >= 60)
                ink = (mx < 130) & (sat < 30)
                caps = [r for r in range(a - 2) if solid[r, core].all()
                        and max((y - x + 1 for x, y in _runs(np.where(ink[r, core])[0])), default=0) >= 5
                        and line[r, cx - 20:cx - 10].sum() == 0 and line[r, cx + 11:cx + 21].sum() == 0]
                caps = [(ca, cb) for ca, cb in _runs(caps)
                        if (line[cb + 1:a, cx - 1:cx + 2].any(1) | (sat[cb + 1:a, cx - 1:cx + 2] >= 60).any(1)).all()]
                if caps:
                    ca, cb = caps[-1]
                    y_err = _centre(I, ca, cb, [c for c in win if line[ca:cb + 1, c].any()])
                    bar["error"] = [cal.value(y_err), *cal.interval(y_err, unc)]
                groups[f"{panel} {label}"] = {"points": [], "countable": False, "bar": bar}
        else:
            # median dashes: black runs 2 rows tall and at least 5 px long; one dashed row per violin
            black = (mx < 120) & (sat < 60)
            black[:, :ax + 4] = False
            black[base - 3:] = False
            dashes = []
            for r in range(base - 3):
                for c0, c1 in _runs(np.where(black[r])[0]):
                    if c1 - c0 >= 4 and black[r + 1, c0:c1 + 1].sum() >= 4 and not black[r - 1, c0:c1 + 1].any() \
                            and not black[r + 2, c0:c1 + 1].any():
                        dashes.append((r, c0, c1))
            violins = []  # dashes on one row within 30 px of each other form one median line
            for r, c0, c1 in sorted(dashes, key=lambda d: d[1]):
                for v in violins:
                    if abs(v[0] - r) <= 1 and c0 - v[2] <= 30:
                        v[2] = max(v[2], c1)
                        v[3].extend(range(c0, c1 + 1))
                        break
                else:
                    violins.append([r, c0, c1, list(range(c0, c1 + 1))])
            assert len(violins) == len(LABELS[panel]), (panel, [(v[0], v[1], v[2]) for v in violins])
            for label, (r, c0, c1, cols) in zip(LABELS[panel], violins):
                y = _centre(I, r, r + 1, cols)
                groups[f"{panel} {label}"] = {"points": [], "countable": False,
                                              "bar": {"median": [cal.value(y), *cal.interval(y, unc)]}}
    return {"groups": groups}
