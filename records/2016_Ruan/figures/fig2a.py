"""Fig. 2A, cell alignment (1/angle dispersion, %), NS / SS / SE: raster Prism scatter, mean ± SEM.

Axis ticks 0-8 calibrate y. NS triangles overlap one another and cover the SEM caps: NS gives
the mean line only. SS circles and SE squares each stand alone.
"""
import _util as U

ITEMS = {"F2A_SS_NS": ["SS", "NS"], "F2A_SE_NS": ["SE", "NS"], "F2A_SE_SS": ["SE", "SS"]}


def read(fig):
    cols = {"NS": (90, 240, "triangle"), "SS": (250, 410, "circle"), "SE": (415, 570, "square")}
    r = U.scatter_panel(fig, (40, 90), [8, 6, 4, 2, 0], 165, 514, cols, marker_px=15, line_min_px=34,
                        no_error=("NS",))
    return U.per_item(r, ITEMS)
