"""Extended Data Fig. 2h (journal_version.pdf p. 20): beating interval (sec), Standard Media vs Maturation Media.
Raster. Standard Media's red squares touch in two places, so only its mean and SD are read; Maturation Media's blue
circles each stand alone and are read as points with the mean and SD."""
import _util as u


def read(fig):
    img, scale = fig.render(u.DPI)
    cal, unc, _ = u.axis(img, u.PDF_LABELS)
    return {"groups": {
        "Standard Media": u.read_group(fig, img, scale, cal, unc, 193, "red"),
        "Maturation Media": u.read_group(fig, img, scale, cal, unc, 608, "blue"),
    }}
