"""Fig. 5A: beating rate (bpm) of 2D CMs, baseline and next day in
glucose, fatty acid, lactate and no-energy medium. Hatched bars (outlined in the substrate colour) with error bars;
the no-energy next-day bar is not drawn (raster, 300 dpi). Printed y tick labels are stated here. A column belongs
to a bar when any pixel in a band above the baseline is non-white (hatching leaves gaps in any single row)."""
from _util import read_bars

ORDER = ["glc_base", "glc_next", "fa_base", "fa_next", "lac_base", "lac_next", "none_base"]
PLOTS = [  # (prefix, x range as fractions of the crop width, printed ticks)
    ("A rate", (0.0, 1.0), [60, 40, 20, 0]),
]


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    out = {}
    for prefix, (f0, f1), ticks in PLOTS:
        box = (int(f0 * W), 0, int(f1 * W), H)
        out.update(read_bars(img, box, ticks, [f"{prefix} {g}" for g in ORDER], band=25))
    return {"groups": out}
