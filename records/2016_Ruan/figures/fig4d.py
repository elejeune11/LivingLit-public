"""Fig. 4D, contractility (mN/mm2), NS / SS / SE: raster Prism scatter, mean ± SEM.

Axis ticks 0-2.5 calibrate y. The image is stretched horizontally (markers ~22 x 15 px).
NS triangles lie on the x axis and hide the SEM caps: NS gives the mean line only.
SS circles overlap (7 blobs, three of them merged pairs or touching the mean) and two SE
squares merge (8 blobs for n=9): SS and SE give mean and upper bar end only.
"""
import _util as U

ITEMS = {"F4D_SS_NS": ["SS", "NS"], "F4D_SE_SS": ["SE", "SS"], "F4D_SE_NS": ["SE", "NS"]}


def read(fig):
    cols = {"NS": (160, 420, "triangle", 220), "SS": (430, 690, "circle", 215), "SE": (700, 890, "square", 120)}
    r = U.scatter_panel(fig, (60, 180), [2.5, 2.0, 1.5, 1.0, 0.5, 0.0], 120, 488, cols, marker_px=18,
                        line_min_px=50, kernel_px=11, tri_kernel_px=9, no_error=("NS",))
    return U.per_item(r, ITEMS)
