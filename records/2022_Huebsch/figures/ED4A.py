"""Extended Data Fig. 4a (journal_version.pdf p. 23): cAPD80 (msec) of MPS of four genotypes, SM vs MM.
Raster (see _util.read_ed4). Points are read where every marker of the group stands alone (SCVI273 SM, G15A0 SM and
MM); the other groups' markers touch, so they give their bar only."""
import _util as u

LABELS = [800, 600, 400, 200, 0]  # y tick labels, top to bottom
NEAR = {  # render column (300 dpi) near each group's centre, and its marker colour
    "WTC SM": (474, "red"), "WTC MM": (688, "blue"),
    "SCVI20 SM": (902, "red"), "SCVI20 MM": (1116, "blue"),
    "SCVI273 SM": (1330, "red"), "SCVI273 MM": (1544, "blue"),
    "G15A0 SM": (1758, "red"), "G15A0 MM": (1972, "blue"),
}


def read(fig):
    return {"groups": u.read_ed4(fig, LABELS, NEAR)}
