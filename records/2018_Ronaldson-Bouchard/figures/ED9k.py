"""Extended Data Fig. 9k: twitch stress at 1-6 Hz for early-stage intensity-trained tissues, alone and with
ryanodine or thapsigargin (raster, 600 dpi). No tick marks: calibrated on the tick labels' centres. Bars touch:
told apart by colour (key: 1 Hz black, 2 Hz dark grey, 3 Hz red, 4 Hz light grey, 5 Hz blue, 6 Hz dark blue).
Each bar is returned under its frequency group `<group>_<k>hz` (the record holds frequency levels as groups)."""
import _util as U

COLOURS = {"1": (20, 20, 20), "2": (85, 85, 85), "3": (225, 10, 25), "4": (185, 185, 185), "5": (60, 105, 170),
           "6": (40, 60, 140)}
GROUPS = ["int", "int_ryan", "int_thap"]
LINKS = {"ED9k_stress": GROUPS, "ED9k_line_int": ["int"], "ED9k_line_int_thap": ["int_thap"]}
HZ = "123456"


def read(fig):
    labels = [f"{g}@{hz}" for g in GROUPS for hz in "123456"]
    g = U.colour_bar_panel(fig, axis_pt=(400, 412), tick_values=[4, 2, 0], bar_row_pt=645, colours=COLOURS,
                           labels=labels, expect=[l.split("@")[1] for l in labels], ticks="labels",
                           band_px=(8, 45), min_w_pt=2.0)
    out = {}
    for item, gids in LINKS.items():
        for gid in gids:
            for hz in HZ:
                out[f"{item}/{gid}_{hz}hz"] = g[f"{gid}@{hz}"]
    return {"groups": out}


LABELS = {f"{item}/{g}_{hz}hz": (item, f"{g}_{hz}hz") for item, gids in LINKS.items() for g in gids for hz in HZ}
