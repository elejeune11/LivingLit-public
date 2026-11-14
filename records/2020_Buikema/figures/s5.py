"""Fig. S5B (relative pHH3+/TnT+ cells) and S5C (% pHH3+ cells), mmc1.pdf p. 10: filled triangles, one per biological
replicate (grey CTR, yellow CHIR), and a black mean line; no error bars or y tick marks. Fig. S5E is bars with error
bars only (no points) and is not read. The legend triangles sit above each panel and are kept out of its box."""
from _util import read_text_axis_triangles

PANELS = {   # page box, tick labels as printed, groups left to right
    "S5B": ((995, 130, 1180, 520), [0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2], ["ctr", "chir"]),
    "S5C": ((1230, 130, 1410, 520), [0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4], ["ctr", "chir"]),
}


def read(fig):
    out = {}
    for panel, (box, ticks, groups) in PANELS.items():
        panel_read = read_text_axis_triangles(fig, box, ticks, groups)
        for g in groups:
            out[f"{panel}/{g}"] = panel_read[g]
    return {"groups": out}
