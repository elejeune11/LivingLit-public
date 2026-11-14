"""Fig. 3B (ryanodine, isoprenaline: beats per minute), bars mean ± SEM (raster, 300 dpi).

One y-axis per panel, left to right; tick values as printed on the labels, top to bottom; bars left
to right in the order of the x labels. Mean = centre of the bar's top outline; error = centre of the
error-bar cap (none when the cap does not clear the bar outline). Bars without points give no n.
Each reading is labelled for every evidence item that rests on it (LINKS)."""
from _util import bar_row, expand

LINKS = {
    'F3B_ryd|ryd': 'bpm|ryd',
    'F3B_ryd|bl': 'bpm|bl',
    'F3B_iso|iso': 'bpm|iso',
    'F3B_iso|bl': 'bpm|bl',
    'F3B_rydiso|rydiso': 'bpm|rydiso',
    'F3B_rydiso|ryd': 'bpm|ryd',
}


def read(fig):
    return expand(bar_row(fig, 300, [
        ('bpm', [80, 60, 40, 20, 0], ['bl', 'iso', 'ryd', 'rydiso']),
    ]), LINKS)
