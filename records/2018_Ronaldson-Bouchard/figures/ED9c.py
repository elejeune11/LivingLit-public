"""Extended Data Fig. 9c: ATP2A2 and SLC8A1 expression in early-stage tissues, FCT, weeks 1-4 by regime, adult
(raster, 600 dpi). No tick marks: calibrated on the tick labels' centres. Bars touch: told apart by colour."""
import _util as U

COLOURS = {"fct": (50, 165, 50), "w1": (5, 5, 5), "w2": (225, 10, 25), "w3": (170, 170, 170), "w4": (45, 65, 145),
           "adult": (165, 50, 125)}
GROUPS = ["fct"] + [f"{r}_w{w}" for r in ("ctrl", "const", "int") for w in (1, 2, 3, 4)] + ["adult"]
REG = [g for g in GROUPS if "_w" in g]
LINKS = {}
for gene in ("ATP2A2", "SLC8A1"):
    LINKS[f"ED9c_{gene}"] = GROUPS
    LINKS[f"ED9c_{gene}_regimes"] = REG
    LINKS[f"ED9c_{gene}_const_w4_vs_fct"] = ["const_w4", "fct"]
    LINKS[f"ED9c_{gene}_int_w4_vs_fct"] = ["int_w4", "fct"]


def read(fig):
    labels = [f"{gene}:{g}" for gene in ("ATP2A2", "SLC8A1") for g in GROUPS]
    expect = [l.split(":")[1].split("_")[-1] if "_w" in l else l.split(":")[1] for l in labels]
    g = U.colour_bar_panel(fig, axis_pt=(80, 95), tick_values=[4, 2, 0], bar_row_pt=377, colours=COLOURS,
                           labels=labels, expect=expect, ticks="labels", band_px=(10, 45), min_w_pt=2.0)
    out = {}
    for item, gids in LINKS.items():
        gene = item.split("_")[1]
        for gid in gids:
            out[f"{item}/{gid}"] = g[f"{gene}:{gid}"]
    return {"groups": out}
