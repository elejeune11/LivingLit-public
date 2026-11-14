"""Supplement Fig. 3A, collagen alignment (axis 'Alignment (1/angle dispersion, %)'), NS / SS / SE.

Raster Prism scatter embedded at about 98 dpi (590 px over 434 pt), so the reading interval is
0.6 of the image's own pixels. Markers are drawn taller than wide (about 28 x 39 px at 300 dpi).
SS 7 circles and SE 6 squares stand alone (the legend prints no n). One of the 8 NS triangles
sits on the SEM bar, so NS gives mean and upper bar end only.
"""
import _util as U

ITEMS = {"S3_SS_NS": ["SS", "NS"], "S3_SE_NS": ["SE", "NS"], "S3_SE_SS": ["SE", "SS"]}
NATIVE_DPI = 590 / 434 * 72


def read(fig):
    cols = {"NS": (250, 500, "triangle"), "SS": (540, 850, "circle"), "SE": (870, 1190, "square")}
    r = U.scatter_panel(fig, (100, 200), [4, 3, 2, 1, 0], 200, 1120, cols, marker_px=34, line_min_px=70,
                        native_dpi=NATIVE_DPI, kernel_px=13, tri_kernel_px=13)
    return U.per_item(r, ITEMS)
