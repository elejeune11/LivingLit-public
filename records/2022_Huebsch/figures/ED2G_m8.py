"""Extended Data Fig. 2g (journal_version.pdf p. 20): prevalence of beating at 1 Hz pacing, Standard Media vs Media 8.
Raster. Standard Media: mean and SD only (its red squares touch). Media 8: four black triangles at 0 touch one another
and cover the mean and SD lines, so nothing of Media 8 is readable."""
import _util as u


def read(fig):
    img, scale = fig.render(u.DPI)
    cal, unc, _ = u.axis(img, u.PDF_LABELS)
    return {"groups": {
        "Standard Media": u.read_group(fig, img, scale, cal, unc, 180, "red"),
        "Media 8": {"points": [], "countable": False},
    }}
