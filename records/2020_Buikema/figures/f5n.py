"""Fig. 5N: percent CCND2+ cells; one triangle per replicate with a black mean line (no error bars).
CTR (grey), CHIR (yellow), CHIR + MK2206 (dark yellow) and CHIR + PNU74654 (black) are read. The crop starts below the
legend, whose black triangle would otherwise join the CHIR + PNU74654 column."""
from _util import fan_out, read_glyph_axis_colours

TICKS = [0, 20, 40, 60]
COLOURS = {"ctr": (0.5, 0.5, 0.5), "chir": (0.99, 0.75, 0.06), "chir_mk": (0.75, 0.56, 0.05),
           "chir_pnu": (0.0, 0.0, 0.0)}
LINKS = {
    "F5N_chir/chir": "chir",
    "F5N_chir/ctr": "ctr",
    "F5N_mk/chir_mk": "chir_mk",
    "F5N_mk/ctr": "ctr",
    "F5N_pnu/chir_pnu": "chir_pnu",
    "F5N_pnu/ctr": "ctr",
    "F5N_mk_chir/chir_mk": "chir_mk",
    "F5N_mk_chir/chir": "chir",
    "F5N_pnu_chir/chir_pnu": "chir_pnu",
    "F5N_pnu_chir/chir": "chir",
}


def read(fig):
    return fan_out(read_glyph_axis_colours(fig, TICKS, COLOURS), LINKS)
