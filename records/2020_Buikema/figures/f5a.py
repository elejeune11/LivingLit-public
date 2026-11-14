"""Fig. 5A: normalized LEF/TCF luciferase expression, one triangle per replicate with a mean line (no error bars);
CTR (grey), CHIR (yellow), CHIR + PNU74654 (black), left to right."""
from _util import fan_out, read_glyph_axis_triangles

TICKS = [0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4]
LINKS = {
    "F5A/chir": "chir",
    "F5A/ctr": "ctr",
}


def read(fig):
    return fan_out(read_glyph_axis_triangles(fig, TICKS, ["ctr", "chir", "chir_pnu"]), LINKS)
