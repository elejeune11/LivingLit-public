"""Fig. S7C: mtDNA content (Mt-DNA/g-actin) of 2D, 2D + blebbistatin and 2D + BTS, bars with error bars
(raster image embedded at 200 dpi, rendered at 300 dpi; light axis). Printed y tick labels 1500, 1000, 500, 0 are
stated here."""
from _util import alias, read_bars


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    out = read_bars(img, (0, 0, W, H), [1500, 1000, 500, 0], ["2D", "bleb", "bts"], native_dpi=200, thr=235)
    return {"groups": alias(out, {"2D vs BTS": "2D"})}
