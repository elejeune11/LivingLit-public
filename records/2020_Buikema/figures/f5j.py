"""Fig. 5J: normalized LEF/TCF luciferase expression; one triangle per replicate with a black mean line (no error bars).
CTR (grey), CHIR (yellow) and CHIR + MK2206 (dark yellow) are read; MK2206 alone (black) is not, no item compares it."""
from _util import fan_out, read_glyph_axis_colours

TICKS = [0, 5, 10, 15, 20, 25]
COLOURS = {"ctr": (0.5, 0.5, 0.5), "chir": (0.99, 0.75, 0.06), "chir_mk": (0.75, 0.56, 0.05)}
LINKS = {
    "F5J_chir/chir": "chir",
    "F5J_chir/ctr": "ctr",
    "F5J_mk/chir_mk": "chir_mk",
    "F5J_mk/ctr": "ctr",
}


def read(fig):
    return fan_out(read_glyph_axis_colours(fig, TICKS, COLOURS), LINKS)
