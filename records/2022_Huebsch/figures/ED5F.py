"""Extended Data Fig. 5f (journal_version.pdf p. 24): reserve OCR (% change from baseline), SM vs MM, SCVI20 2D
monolayers. Raster (one embedded ~300 dpi image). SM's two lowest red squares overlap (one blob two markers tall), so
SM gives its mean and upper error end only; MM's four blue circles stand alone."""
import _util as u


def read(fig):
    return {"groups": u.read_ed5(fig, [100, 50, 0, -50], {"SM": (284, "red"), "MM": (406, "blue")})}
