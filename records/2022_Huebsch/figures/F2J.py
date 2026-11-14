"""Fig. 2j (journal_version.pdf p. 4): maximum Ca2+ upstroke velocity dF/dt (ms-1) of SCVI20 MPS, SM vs MM. Vector,
log y axis (labelled decades 0.00001-0.01 with unlabelled minor ticks): open bars at the mean, black mean ± s.d. error
bars, SM filled red squares (each a fill and an outline path), MM filled blue circles. Each group is read with every
point, its mean and the upper end of its s.d. bar."""
import _util as u
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

BLUE_J = (0.23, 0.28, 0.62)  # MM circles of panel j


def log_axis(fig):
    """Log calibration from the y axis path's long (major) ticks, each paired with the decade label printed level with
    it; the short minor ticks carry no label and are not used."""
    for d in fig.drawings():
        if u._rgb(d.get("color")) != u.BLACK:
            continue
        ls = u._lines(d)
        vert = [l for l in ls if abs(l[0] - l[2]) < 0.01 and abs(l[1] - l[3]) > 50]
        ticks = [l for l in ls if abs(l[1] - l[3]) < 0.01 and abs(l[0] - l[2]) < 4]
        if len(vert) == 1 and len(ticks) >= 2:
            break
    else:
        raise ValueError("no y axis path with tick lines found")
    longest = max(abs(l[0] - l[2]) for l in ticks)
    major = [l for l in ticks if abs(abs(l[0] - l[2]) - longest) < 0.05]
    labels = []
    for x0, y0, x1, y1, t in fig.words():
        try:
            v = float(t)
        except ValueError:
            continue
        if 0 < vert[0][0] - x1 < 12:
            labels.append(((y0 + y1) / 2, v))
    if len(major) != len(labels):
        raise ValueError(f"{len(major)} major ticks, {len(labels)} labels")
    marks = []
    for l in major:
        pos, v = min(labels, key=lambda m: abs(m[0] - l[1]))
        if abs(pos - l[1]) > 1.5:
            raise ValueError(f"tick at y={l[1]} has no label level with it")
        marks.append((l[1], v))
    cal = calibrate(marks, log=True)
    return cal, VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)


def read(fig):
    cal, unc = log_axis(fig)
    cats = u.category_ticks(fig)
    near = lambda x: min(range(len(cats)), key=lambda i: abs(cats[i] - x))
    bars = u.error_bars(fig)
    res = {}
    for label, (ci, colours) in {"SM": (0, {u.RED}), "MM": (1, {BLUE_J})}.items():
        pts = sorted((p for p in u.vector_markers(fig, colours) if near(p[0]) == ci), key=lambda p: p[1])
        (bx, my, ty), = [b for b in bars if near(b[0]) == ci]
        m, e = point(cal, my, unc, (bx, my)), point(cal, ty, unc, (bx, ty))
        res[label] = {"points": [point(cal, p[1], unc, p) for p in pts], "countable": True,
                      "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    return {"groups": res}
