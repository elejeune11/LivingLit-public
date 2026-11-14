"""Fig. 2B, tensile stiffness (kPa), collagen / NS / SS / SE: raster Prism scatter.

Axis ticks 0-50 calibrate y. Collagen is four grey diamonds drawn over the x axis (read from
their grey outline; no mean line visible). NS triangles and the NS mean lie within the x-axis
line and are not readable. SS squares overlap (6 blobs for n=7): SS gives mean and upper bar
end only. SE: 9 circles that stand alone. The SE bar spans about ±12 kPa around 21.5 (the
size of an SD for n=9, SEM 4.02 printed), while the SS bar is about ±1.2 (an SEM).
"""
import _util as U

ITEMS = {"F2B_NS_collagen": ["collagen"], "F2B_SS_collagen": ["SS", "collagen"],
         "F2B_SE_collagen": ["SE", "collagen"], "F2B_SS_NS": ["SS"], "F2B_SE_NS": ["SE"],
         "F2B_SE_SS": ["SE", "SS"]}


def read(fig):
    img, scale, m = U.render(fig)
    left, _ = U.y_axis(m, 80, 110)
    cal = U.fit(U.y_ticks(m, left), [50, 40, 30, 20, 10, 0])
    cols = {"SS": (400, 520, "square", 330), "SE": (525, 650, "circle", 100)}
    r = {}
    for g, (a, b, shape, ylo) in cols.items():
        r[g] = U.scatter_group(fig, m, scale, cal, a, b, ylo, 512, 15, 34, shape)
    r["collagen"] = {"points": [U.to_point(fig, cal, scale, x, y) for x, y in
                                U.grey_marker_columns(img, 110, 250, 495, 540)], "countable": True, "bar": {}}
    return U.per_item(r, ITEMS)
