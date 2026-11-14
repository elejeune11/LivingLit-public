"""Fig. 4E: MitoTracker Green FM mean fluorescent intensity (AU), bars 2D (blue) and 3D (red) with error bars
(raster, 300 dpi; axes drawn in very light grey, found with a light threshold). Printed y tick labels 10 to 0 by 2 are stated here."""
from _util import read_bars


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    return {"groups": read_bars(img, (0, 0, W, H), [10, 8, 6, 4, 2, 0], ["2D", "3D"], thr=235)}
