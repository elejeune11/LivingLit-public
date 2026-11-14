"""Fig. 3A, cardiomyocyte size (Cell Area, um2), NS / SS / SE: raster Prism scatter, mean ± SEM.

Axis ticks 0-1500 calibrate y. NS: 16 triangles that stand alone, each centred on its box
(apex to base), as Prism draws them. SS circles and SE squares
touch the mean line and one another, so SS and SE give mean and upper bar end only.
Lines here are up to 11 px thick at 300 dpi.
"""
import _util as U

ITEMS = {"F3_SS_NS": ["SS", "NS"], "F3_SE_NS": ["SE", "NS"], "F3_SE_SS": ["SE", "SS"]}


def read(fig):
    cols = {"NS": (300, 560, "triangle", 280), "SS": (590, 870, "circle", 300), "SE": (900, 1180, "square", 140)}
    r = U.scatter_panel(fig, (150, 260), [1500, 1000, 500, 0], 140, 835, cols, marker_px=27, line_min_px=60,
                        kernel_px=13, max_thick=14, tri_kernel_px=13)
    return U.per_item(r, ITEMS)
