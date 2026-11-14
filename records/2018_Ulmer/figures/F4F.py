"""Fig. 4F: mitochondrial DNA content (Mt-DNA/g-actin), bars hiPS-CM before culture (black), 2D (blue), 3D (red),
adult human heart (light grey) with error bars (raster, 300 dpi; axes drawn in very light grey, found with a light threshold). Printed y tick labels 2000 to 0 by 500 are stated
here."""
from _util import alias, read_bars


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    out = read_bars(img, (0, 0, W, H), [2000, 1500, 1000, 500, 0], ["before", "2D", "3D", "heart"], thr=235)
    return {"groups": alias(out, {"2D vs before": "2D", "2D vs heart": "2D", "3D vs heart": "3D", "heart vs 3D": "heart"})}
