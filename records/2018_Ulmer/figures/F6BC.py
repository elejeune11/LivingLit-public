"""Fig. 6B-C: glucose consumption (delta cGluc in 4 h, mg/dl) and lactate production (cLac increase, mmol/l),
dark bars 2D and 3D with error bars (raster, 300 dpi). Printed y tick labels are stated here (B: 20 to 0 by 5;
C: 0.6 to 0 by 0.2); the plots are the left and right halves of the crop."""
from _util import read_bars


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    out = {}
    out.update(read_bars(img, (0, 0, W // 2, H), [20, 15, 10, 5, 0], ["B 2D", "B 3D"]))
    out.update(read_bars(img, (W // 2, 0, W, H), [0.6, 0.4, 0.2, 0.0], ["C 2D", "C 3D"]))
    return {"groups": out}
