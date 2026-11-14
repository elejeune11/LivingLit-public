"""Fig. 7E: mitochondrial DNA content (Mt-DNA/g-actin) of control (blue) and BTS-treated (teal) EHTs, bars with
error bars (raster, 300 dpi). Printed y tick labels 2000 to 0 by 500 are stated here."""
from _util import read_bars


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    return {"groups": read_bars(img, (0, 0, W, H), [2000, 1500, 1000, 500, 0], ["ctrl", "bts"])}
