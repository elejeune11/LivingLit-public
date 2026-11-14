"""Fig. 5B, SERCA2/GAPDH (western blot, normalised to GAPDH), NS / SS / SE: raster Prism scatter.

Axis ticks 0-4 calibrate y. NS triangles touch the bars and one lies on the x axis: mean and
upper bar end only. Two SS squares merge (6 blobs, n=7): mean and upper bar end only. SE:
7 circles that stand alone. The SE bar spans about ±0.78 around 2.29 (the size of an SD for
n=7), the NS and SS bars about ±0.2 (an SEM); the legend does not say which is shown.
"""
import _util as U

ITEMS = {"F5B_SS_NS": ["SS", "NS"], "F5B_SE_NS": ["SE", "NS"], "F5B_SE_SS": ["SE", "SS"]}


def read(fig):
    cols = {"NS": (120, 260, "triangle", 110), "SS": (270, 450, "square", 110), "SE": (470, 650, "circle", 50)}
    r = U.scatter_panel(fig, (60, 200), [4, 3, 2, 1, 0], 50, 421, cols, marker_px=15, line_min_px=34, kernel_px=11,
                        tri_kernel_px=7)
    return U.per_item(r, ITEMS)
