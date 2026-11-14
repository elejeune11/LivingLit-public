"""Supplement Fig. 5E, 1 uM Bay K8644: force trace (mN), raster Excel chart.

The gridline at 0.03 mN and the bottom axis (0) calibrate force; tick marks calibrate time (s).
Each twitch gives its highest point (upper edge of the thick trace plus half its thickness on
the flat parts), with its time as x; peaks are at least 0.4 s apart, and a twitch within a third
of that from the plot edge is skipped (cut by the edge). The trace merges with the bottom axis,
so troughs are not read. Image embedded at about 220 dpi (1562 px over 511 pt).
"""
import _util as U

ITEMS = {"S5DE_bayk_rate": ["bayk"], "S5DE_bayk_force": ["bayk"]}
NATIVE_DPI = 1562 / 511.0 * 72


def read(fig):
    o = U.excel_trace(fig, 0.03, [87, 89, 91, 93, 95, 97], 0.4, native_dpi=NATIVE_DPI)
    return {"groups": {f"{it}: bayk peaks": {"points": o["peaks"], "countable": True} for it in ITEMS}}
