"""Fig. 6H, Diastolic Force (journal p. 13, one JPEG image of Figure 6 at about 300 dpi): five bars (Control, LCFA,
GW0742, LCFA + GW0742, GSK0660; mean with an SD whisker and caps) with one marker per EHT (four shapes, one per
biological replicate; dark outline, bar-coloured fill); legend n = 4 replicates x 3 EHTs = 12 markers per bar.
The method is in _util.read_shape_bars."""
from _util import read_shape_bars

TICKS = [250, 200, 150, 100, 50, 0]          # y tick labels, top to bottom
N_MARKERS = 12                               # n = 4; 3 EHTs/biological replicate
LABELS = {"F6H_dia/control": "control", "F6H_dia/lcfa": "lcfa", "F6H_dia/gw": "gw",
          "F6H_dia/lcfa_gw": "lcfa_gw", "F6H_dia/gsk": "gsk",
          "F6H_dia_lcfa_gw/lcfa_gw": "lcfa_gw", "F6H_dia_lcfa_gw/control": "control"}


def read(fig):
    return read_shape_bars(fig, TICKS, LABELS, N_MARKERS)
