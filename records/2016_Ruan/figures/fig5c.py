"""Fig. 5C, RYR2/GAPDH (western blot, normalised to GAPDH), NS / SS / SE: raster Prism scatter.

Axis ticks 0-2.0 calibrate y. NS triangles touch the bars and one another: mean and upper bar
end only. SS (7 squares) and SE (7 circles) stand alone. The SE bar spans about ±0.41 around
1.11 (the size of an SD for n=7), the NS and SS bars about ±0.18 (an SEM).
"""
import _util as U

ITEMS = {"F5C_SE_NS": ["SE", "NS"], "F5C_SE_SS": ["SE", "SS"], "F5C_SS_NS": ["SS", "NS"]}


def read(fig):
    cols = {"NS": (160, 330, "triangle"), "SS": (340, 500, "square"), "SE": (505, 690, "circle")}
    r = U.scatter_panel(fig, (60, 200), [2.0, 1.5, 1.0, 0.5, 0.0], 60, 419, cols, marker_px=15, line_min_px=34,
                        kernel_px=11, tri_kernel_px=7)
    return U.per_item(r, ITEMS)
