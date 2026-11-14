"""Fig. 5B: relative TnT+ cell number, one triangle per replicate with a mean line (no error bars);
CTR (grey), CHIR (yellow), CHIR + PNU74654 (black), left to right."""
from _util import fan_out, read_glyph_axis_triangles

TICKS = [0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4]
LINKS = {
    "F5B_chir/chir": "chir",
    "F5B_chir/ctr": "ctr",
    "F5B_pnu_ctr/chir_pnu": "chir_pnu",
    "F5B_pnu_ctr/ctr": "ctr",
    "F5B_pnu_chir/chir_pnu": "chir_pnu",
    "F5B_pnu_chir/chir": "chir",
}


def read(fig):
    return fan_out(read_glyph_axis_triangles(fig, TICKS, ["ctr", "chir", "chir_pnu"]), LINKS)
