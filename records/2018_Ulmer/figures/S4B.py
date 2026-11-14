"""Fig. S4B (left): mtDNA content (Mt-DNA/g-actin) after 70 days, bars 2D (blue) and 3D (red) with error bars
(raster image embedded at ~218 dpi, rendered at 300 dpi). Printed y tick labels 2500 to 0 by 500 are stated here."""
from _util import read_bars


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    return {"groups": read_bars(img, (0, 0, W, H), [2500, 2000, 1500, 1000, 500, 0], ["2D", "3D"], native_dpi=218, bar_thr=200)}
