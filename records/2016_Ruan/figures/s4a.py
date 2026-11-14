"""Supplement Fig. 4A, baseline (force at 125% slack length): force trace (mN) of one stress-conditioned construct, raster.

The frame's tick marks calibrate force (0, 0.08 mN) and time (s). Each twitch gives its peak
and the lowest point before the next twitch, read on the centre line of the trace, with its
time as x. Image embedded at about 220 dpi (1347 px over 441 pt): interval 0.6 native px plus
half the line's half-thickness.
"""
import _util as U

ITEMS = {"S4_bdm": ["baseline"], "S4_iso_rate": ["baseline"], "S4_iso_force": ["baseline"]}
NATIVE_DPI = 1347 / 441.0 * 72


def read(fig):
    o = U.trace_panel(fig, [0.08, 0], [0, 5, 10, 15, 20], native_dpi=NATIVE_DPI)
    return U.trace_groups(o, list(ITEMS), "baseline", twitches=True)
