"""Fig. 4B-C: qRT-PCR of PPARGC1A and ESRRA normalized to GusB, bars 2D (blue) and 3D (red) with error bars
(raster, 300 dpi; axes drawn in very light grey, found with a light threshold). Printed y tick labels are stated here (B: 1.0 to 0.0 by 0.2; C: 8 to 0 by 2); the two plots are
the left and right parts of the crop."""
from _util import read_bars


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    split = W // 2
    out = {}
    out.update(read_bars(img, (0, 0, split, H), [1.0, 0.8, 0.6, 0.4, 0.2, 0.0], ["PPARGC1A 2D", "PPARGC1A 3D"], thr=235))
    out.update(read_bars(img, (split, 0, W, H), [8, 6, 4, 2, 0], ["ESRRA 2D", "ESRRA 3D"], thr=235))
    return {"groups": out}
