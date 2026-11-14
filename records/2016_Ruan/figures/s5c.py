"""Supplement Fig. 5C, 1 uM verapamil: force trace (mN), raster Excel chart.

The gridline at 0.02 mN and the bottom axis (0) calibrate force; tick marks calibrate time (s).
Each twitch gives its highest point (upper edge of the thick trace plus half its thickness on
the flat parts), with its time as x; peaks are at least 0.3 s apart, and a twitch within a third
of that from the plot edge is skipped (cut by the edge). The trace merges with the bottom axis,
so troughs are not read. Image embedded at about 220 dpi (1562 px over 511 pt).
"""
import _util as U

ITEMS = {"S5BC_verapamil": ["verapamil"]}
NATIVE_DPI = 1562 / 511.0 * 72


def read(fig):
    o = U.excel_trace(fig, 0.02, [755, 756, 757, 758, 759, 760, 761], 0.3, native_dpi=NATIVE_DPI)
    return {"groups": {f"{it}: verapamil peaks": {"points": o["peaks"], "countable": True} for it in ITEMS}}
