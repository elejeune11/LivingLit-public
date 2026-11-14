"""Supplement Fig. 6A, SERCA2/GAPDH processed (log-transformed, mean-centred, autoscaled), NS / SS / SE.

Raster Prism scatter embedded at about 78 dpi (511 px over 469 pt): interval 0.6 of the image's
own pixels. Markers overlap or touch the bars in every group (NS triangles in a row, SS squares
and two SE circles on the mean line): mean and upper bar end only; the NS caps merge with the
mean line and are not read. The SE bar spans about ±1.24 around 2.43 (the size of an SD for n=7).
"""
import _util as U

ITEMS = {"S6_serca_SS_NS": ["SS", "NS"], "S6_serca_SE_NS": ["SE", "NS"], "S6_serca_SE_SS": ["SE", "SS"]}
NATIVE_DPI = 511 / (540.7267 - 72.0) * 72


def read(fig):
    cols = {"NS": (180, 375, "triangle", 270), "SS": (400, 640, "square", 270), "SE": (680, 880, "circle", 150)}
    r = U.scatter_panel(fig, (60, 200), [6, 4, 2, 0], 150, 664, cols, marker_px=23, line_min_px=40,
                        kernel_px=13, tri_kernel_px=9, native_dpi=NATIVE_DPI)
    return U.per_item(r, ITEMS)
