"""Extended Data Fig. 10a: calcium intensity with increasing isoproterenol (raster, 600 dpi). No axis line: calibrated
on the chart's horizontal gridlines at 2-18 (found by code between the bars). Mean +/- 95% CI."""
import _util as U

ORDER = ["baseline", "iso_001", "iso_100", "iso_1mM"]
LINKS = {"ED10a_doses": ORDER, "ED10a_iso_001_vs_baseline": ["iso_001", "baseline"],
         "ED10a_iso_100_vs_baseline": ["iso_100", "baseline"], "ED10a_iso_1mM_vs_baseline": ["iso_1mM", "baseline"]}


def read(fig):
    g = U.grid_bar_panel(fig, grid_x_pt=[105, 120, 180, 230], grid_y_pt=(60, 185),
                         tick_values=[18, 16, 14, 12, 10, 8, 6, 4, 2], bar_row_pt=185,
                         colours={"red": (205, 10, 25)}, labels=ORDER)
    return {"groups": U.expand(g, LINKS)}
