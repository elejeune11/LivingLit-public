"""Extended Data Fig. 5b: sarcomere length by regime (raster, 600 dpi; grey axis without tick marks, calibrated on
the tick labels' centres; the axis line runs about 0.1 below the '0' label). FCT is not drawn."""
import _util as U

LINKS = {"ED5b_sl": ["ctrl", "const", "int"], "ED5b_int_vs_fct": ["int"]}


def read(fig):
    g = U.bar_panel(fig, axis_pt=(338, 346), tick_values=[3, 2.5, 2, 1.5, 1, 0.5, 0], bar_row_pt=180,
                    labels=["ctrl", "const", "int"], thr=170, ticks="labels", band_px=(10, 90))
    return {"groups": U.expand(g, LINKS)}
