"""Extended Data Fig. 5g (journal_version.pdf p. 24): ATP capacity (% change from baseline), SM vs MM, SCVI20 2D
monolayers. Raster (one embedded ~300 dpi image). The error-bar lines and caps cut several open markers into pieces;
pieces are joined into marker-sized boxes, and all four markers of each group stand alone."""
import _util as u


def read(fig):
    return {"groups": u.read_ed5(fig, [50, 40, 30, 20, 10, 0], {"SM": (260, "red"), "MM": (385, "blue")})}
