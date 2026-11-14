"""Extended Data Fig. 10b: relaxation time (R90) with increasing isoproterenol (raster, 600 dpi). No axis line:
calibrated on the chart's horizontal gridlines at 0-0.25 s (found by code between the bars). Mean +/- 95% CI."""
import _util as U

ORDER = ["baseline", "iso_001", "iso_100", "iso_1mM"]
LINKS = {"ED10b_doses": ORDER, "ED10b_iso_100_vs_baseline": ["iso_100", "baseline"],
         "ED10b_iso_1mM_vs_baseline": ["iso_1mM", "baseline"]}


def read(fig):
    g = U.grid_bar_panel(fig, grid_x_pt=[365, 410, 450, 500], grid_y_pt=(60, 195),
                         tick_values=[0.25, 0.2, 0.15, 0.1, 0.05, 0], bar_row_pt=185,
                         colours={"red": (205, 10, 25)}, labels=ORDER)
    return {"groups": U.expand(g, LINKS)}
