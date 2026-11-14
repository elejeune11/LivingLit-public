"""Fig. 5H: fold increase in TnT cell number; one triangle per replicate with a black mean line (no error bars).
CTR (grey), CHIR (yellow) and CHIR + MK2206 (dark yellow) are read; MK2206 alone (black) is not, no item compares it."""
from _util import fan_out, read_glyph_axis_colours

TICKS = [0, 1, 2, 3, 4, 5]
COLOURS = {"ctr": (0.5, 0.5, 0.5), "chir": (0.99, 0.75, 0.06), "chir_mk": (0.75, 0.56, 0.05)}
LINKS = {
    "F5H_chir/chir": "chir",
    "F5H_chir/ctr": "ctr",
    "F5H_mk/chir_mk": "chir_mk",
    "F5H_mk/chir": "chir",
    "F5H_mk_ctr/chir_mk": "chir_mk",
    "F5H_mk_ctr/ctr": "ctr",
}


def read(fig):
    return fan_out(read_glyph_axis_colours(fig, TICKS, COLOURS), LINKS)
