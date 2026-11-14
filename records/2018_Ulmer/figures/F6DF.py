"""Fig. 6D-F: 14C-CO2 (pmol) from 14C-oleic acid (D), 14C-lactate (E) and 14C-glucose (F); bars 2D, 3D and
no cells with error bars (raster, 300 dpi). Printed y tick labels are stated here (D: 50 to 0 by 10; E: 25 to 0 by 5;
F: 3 to 0 by 1); the plots are the thirds of the crop."""
from _util import alias, read_bars

PLOTS = [("D", [50, 40, 30, 20, 10, 0]), ("E", [25, 20, 15, 10, 5, 0]), ("F", [3, 2, 1, 0])]
# F's top tick (3) is not drawn: the axis line's top end stands for it.


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    out = {}
    for i, (p, ticks) in enumerate(PLOTS):
        box = (i * W // 3, 0, (i + 1) * W // 3, H)
        out.update(read_bars(img, box, ticks, [f"{p} 2D", f"{p} 3D", f"{p} no cells"], min_w=6, top_at_end=(p == "F")))
    return {"groups": alias(out, {f"{p} 2D vs no cells": f"{p} 2D" for p, _ in PLOTS})}
