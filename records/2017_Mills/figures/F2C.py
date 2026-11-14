"""Fig. 2C: force of contraction normalised to baseline, markers ± SEM by isoprenaline dose (raster); CTRL red
circles, MM blue squares; doses 10^-10 to 10^-5 M (baseline is not plotted). Ticks 0.9-1.2 by 0.1.
Only MM at 10^-6 M is compared in the record (vs baseline, which is not plotted), so only the MM markers are located and only that one is returned."""
from _util import marker_panel

LEGEND = (157, 107, 165, 118)
DOSES = ["109", "108", "107", "106", "105"]  # the MM marker at 10^-10 M lies under the CTRL one and is not found


def read(fig):
    out = marker_panel(fig, [0.9, 1.0, 1.1, 1.2], {
        "mm": ((10, 10, 250), [f"mm_{d}" for d in DOSES]),
    }, exclude=[LEGEND])
    return {"groups": {"mm_106": out["groups"]["mm_106"]}}
