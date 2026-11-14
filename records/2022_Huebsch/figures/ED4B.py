"""Extended Data Fig. 4b (journal_version.pdf p. 23): spontaneous beating frequency (Hz) of MPS of four genotypes,
SM vs MM. Raster (see _util.read_ed4). Points are read where every marker of the group stands alone (WTC MM, G15A0 SM
and MM); the other groups' markers touch, so they give their bar only."""
import _util as u

LABELS = [2.0, 1.5, 1.0, 0.5, 0.0]  # y tick labels, top to bottom
NEAR = {  # render column (300 dpi) near each group's centre, and its marker colour
    "WTC SM": (474, "red"), "WTC MM": (685, "blue"),
    "SCVI20 SM": (895, "red"), "SCVI20 MM": (1104, "blue"),
    "SCVI273 SM": (1314, "red"), "SCVI273 MM": (1525, "blue"),
    "G15A0 SM": (1736, "red"), "G15A0 MM": (1945, "blue"),
}


def read(fig):
    return {"groups": u.read_ed4(fig, LABELS, NEAR)}
