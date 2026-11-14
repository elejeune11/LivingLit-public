"""Fig. 2B: rate of contraction (bpm), markers ± SEM by isoprenaline dose (raster); CTRL red circles, MM blue squares.
Ticks 0-60 by 20. Doses no item compares are located (so the others are named right) but not returned; each
baseline is repeated once per item that compares a dose with it."""
from _util import marker_panel

LEGEND = (63, 114, 71, 127)  # the CTRL and MM legend symbols
CTRL = ["ctrl_base", None, None, "ctrl_108", "ctrl_107", "ctrl_106", "ctrl_105"]
MM = ["mm_base", None, "mm_109", "mm_108", "mm_107", "mm_106", "mm_105"]


def read(fig):
    extra = {f"ctrl_base (vs {d})": "ctrl_base" for d in ("107", "106", "105")}
    extra.update({f"mm_base (vs {d})": "mm_base" for d in ("108", "107", "106", "105")})
    return marker_panel(fig, [0, 20, 40, 60], {
        "ctrl": ((250, 10, 10), CTRL),
        "mm": ((10, 10, 250), MM),
    }, exclude=[LEGEND], extra=extra)
