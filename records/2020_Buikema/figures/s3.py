"""Fig. S3C (fold increase TnT+ cells), S3E (% Ki67+/TnT+ cells) and S3G (% pHH3+/TnT+ cells), mmc1.pdf p. 8:
filled triangles, one per biological replicate (grey CTR, green Wnt ligands, yellow CHIR), and a black mean line;
no error bars. Each panel also holds a stale bar-chart layer under a white box, which is skipped."""
from _util import read_text_axis_triangles

PANELS = {   # page box, tick labels as printed, groups left to right
    "S3C": ((890, 55, 1160, 330), [0, 2, 4, 6, 8, 10, 12], ["ctr", "rspo", "dkk", "wnt3a", "dkk_rspo", "chir"]),
    "S3E": ((395, 490, 590, 725), [0, 10, 20, 30, 40, 50, 60, 70], ["ctr", "wnt3a", "dkk_rspo", "chir"]),
    "S3G": ((960, 490, 1160, 725), [0, 2, 4, 6, 8, 10, 12], ["ctr", "wnt3a", "dkk_rspo", "chir"]),
}
ITEMS = {   # item suffix: the groups it compares
    "wnt3a": ["wnt3a", "ctr"],
    "dkkrspo": ["dkk_rspo", "ctr"],
    "chir": ["chir", "ctr"],
}


def read(fig):
    out = {}
    for panel, (box, ticks, groups) in PANELS.items():
        panel_read = read_text_axis_triangles(fig, box, ticks, groups)
        for suffix, gs in ITEMS.items():
            for g in gs:
                out[f"{panel}_{suffix}/{g}"] = panel_read[g]
        if panel == "S3C":
            for g in ["ctr", "rspo", "dkk"]:
                out[f"S3C_rspo/{g}"] = panel_read[g]
    return {"groups": out}
