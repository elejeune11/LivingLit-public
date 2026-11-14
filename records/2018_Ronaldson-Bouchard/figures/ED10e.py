"""Extended Data Fig. 10e: FWHM and decay time in healthy (C2A) and HCM early-stage tissues by regime (raster,
600 dpi). Calibrated on the tick labels' centres (no tick marks found). Bars touch: told apart by colour."""
import _util as U

COLOURS = {"ctrl": (5, 5, 5), "const": (45, 65, 145), "int": (225, 10, 25)}
GROUPS = [f"{d}_{r}" for d in ("c2a", "hcm") for r in ("ctrl", "const", "int")]
LINKS = {}
for m in ("fwhm", "decay"):
    LINKS[f"ED10e_{m}"] = GROUPS
    for d in ("c2a", "hcm"):
        LINKS[f"ED10e_{m}_{d}_regimes"] = [f"{d}_{r}" for r in ("ctrl", "const", "int")]


def read(fig):
    labels = [f"{m}:{g}" for m in ("fwhm", "decay") for g in GROUPS]
    g = U.colour_bar_panel(fig, axis_pt=(290, 302), tick_values=[500, 400, 300, 200, 100, 0], bar_row_pt=552,
                           colours=COLOURS, labels=labels, expect=[l.split("_")[-1] for l in labels], ticks="labels",
                           min_w_pt=3)
    out = {}
    for item, gids in LINKS.items():
        m = item.split("_")[1]
        for gid in gids:
            out[f"{item}/{gid}"] = g[f"{m}:{gid}"]
    return {"groups": out}
