"""Supplement Fig. 6B, RYR2/GAPDH processed (log-transformed, mean-centred, autoscaled), NS / SS / SE.

Raster Prism scatter embedded at about 78 dpi: interval 0.6 of the image's own pixels. NS
triangles and SS squares touch the bars and one another: mean and upper bar end only. SE:
7 circles that stand alone. The SE bar spans about ±0.32 around 1.36 (the size of an SD for n=7).
"""
import _util as U

ITEMS = {"S6_ryr_SS_NS": ["SS", "NS"], "S6_ryr_SE_NS": ["SE", "NS"], "S6_ryr_SE_SS": ["SE", "SS"]}
NATIVE_DPI = 511 / (540.7267 - 72.0) * 72


def read(fig):
    cols = {"NS": (230, 450, "triangle", 210), "SS": (480, 720, "square", 210), "SE": (740, 960, "circle", 120)}
    r = U.scatter_panel(fig, (60, 250), [2.0, 1.5, 1.0, 0.5, 0.0], 120, 664, cols, marker_px=23, line_min_px=40,
                        kernel_px=13, tri_kernel_px=9, native_dpi=NATIVE_DPI)
    return U.per_item(r, ITEMS)
