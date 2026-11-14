"""Fig. 5P: percent pHH3+ cells; one triangle per replicate with a black mean line (no error bars).
CHIR (yellow) and CHIR + Palbociclib (black) are read. Tick labels are outlined glyphs: six evenly spaced rows, the top
one two digits, read as 0, 2, 4, 6, 8, 10."""
from _util import fan_out, read_glyph_axis_colours

TICKS = [0, 2, 4, 6, 8, 10]
COLOURS = {"chir": (0.99, 0.75, 0.06), "chir_palbo": (0.0, 0.0, 0.0)}
LINKS = {
    "F5P/chir_palbo": "chir_palbo",
    "F5P/chir": "chir",
}


def read(fig):
    return fan_out(read_glyph_axis_colours(fig, TICKS, COLOURS), LINKS)
