"""Extended Data Fig. 2g (journal_version.pdf p. 20): prevalence of beating at 1 Hz pacing, Standard Media vs Media 7.
Raster (one embedded ~300 dpi image). Standard Media's red squares touch one another (one blob of two), so only its
mean and SD are read; Media 7's black squares lie on its black bar, so only its mean and SD are read."""
import _util as u


def read(fig):
    img, scale = fig.render(u.DPI)
    cal, unc, _ = u.axis(img, u.PDF_LABELS)
    return {"groups": {
        "Standard Media": u.read_group(fig, img, scale, cal, unc, 180, "red"),
        "Media 7": u.read_group(fig, img, scale, cal, unc, 290),
    }}
