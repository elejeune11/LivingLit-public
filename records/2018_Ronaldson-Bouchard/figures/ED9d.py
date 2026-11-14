"""Extended Data Fig. 9d: calcium transient rise time, FWHM and decay time in early-stage tissues of three lines
and FCT (raster, 600 dpi). Ticks every 50 ms are drawn inside the axis. Bars touch: told apart by colour."""
import _util as U

COLOURS = {"fct": (50, 165, 50), "ctrl": (15, 15, 15), "const": (45, 65, 145), "int": (225, 10, 25)}
GROUPS = ["fct"] + [f"{l}_{r}" for l in ("c2a", "wtc", "imr") for r in ("ctrl", "const", "int")]
LINKS = {}
for m in ("rise", "fwhm", "decay"):
    LINKS[f"ED9d_{m}"] = GROUPS
    for l in ("c2a", "wtc", "imr"):
        if m != "rise" and l == "imr":
            continue
        LINKS[f"ED9d_{m}_{l}_lines"] = [f"{l}_ctrl", f"{l}_const", f"{l}_int"]
        LINKS[f"ED9d_{m}_{l}_int_vs_fct"] = [f"{l}_int", "fct"]


def read(fig):
    labels = [f"{m}:{g}" for m in ("rise", "fwhm", "decay") for g in GROUPS]
    expect = [l.split(":")[1].split("_")[-1] for l in labels]
    g = U.colour_bar_panel(fig, axis_pt=(310, 322), tick_values=list(range(500, 0, -50)), bar_row_pt=377,
                           colours=COLOURS, labels=labels, expect=expect, ticks="marks_right", tick_len=(6, 60),
                           min_w_pt=2.0)
    out = {}
    for item, gids in LINKS.items():
        m = item.split("_")[1]
        for gid in gids:
            out[f"{item}/{gid}"] = g[f"{m}:{gid}"]
    return {"groups": out}
