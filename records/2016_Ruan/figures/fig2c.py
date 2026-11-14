"""Fig. 2C, cell volume fraction (axis 0-0.8, a fraction), NS / SS / SE: raster Prism scatter, mean ± SEM.

NS triangles touch the SEM bar and the mean line, so NS gives mean and upper bar end only.
SS (circles) and SE (squares) stand alone.
"""
import _util as U

ITEMS = {"F2C_SS_NS": ["SS", "NS"], "F2C_SE_NS": ["SE", "NS"], "F2C_SE_SS": ["SE", "SS"]}


def read(fig):
    cols = {"NS": (130, 285, "triangle"), "SS": (295, 450, "circle"), "SE": (460, 620, "square")}
    r = U.scatter_panel(fig, (60, 140), [0.8, 0.6, 0.4, 0.2, 0.0], 105, 512, cols, marker_px=15, line_min_px=34)
    return U.per_item(r, ITEMS)
