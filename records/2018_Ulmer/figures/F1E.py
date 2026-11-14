"""Fig. 1E: qPCR fold change, 2D (dark) and 3D (white) bars with error bars, six plots (raster, 300 dpi).
Printed y tick labels per plot (top to bottom) are stated here; tick marks, bar tops and error-bar ends are found by code.
The Vimentin axis has minor ticks only, its major ticks left as gaps; those are located from the gaps."""
from _util import read_bars

GENES = ["cTnt1", "Myl3", "Myl4", "Vimentin", "Postn", "CD31"]
TICKS = {
    "cTnt1": [2.0, 1.5, 1.0, 0.5, 0.0], "Myl3": [1.5, 1.0, 0.5, 0.0], "Myl4": [1.5, 1.0, 0.5, 0.0],
    "Vimentin": [2.0, 1.5, 1.0, 0.5, 0.0], "Postn": [2.0, 1.5, 1.0, 0.5, 0.0], "CD31": [2.0, 1.5, 1.0, 0.5, 0.0],
}


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    out = {}
    for i, gene in enumerate(GENES):
        r, c = divmod(i, 3)
        box = (int(c * W / 3), (0, 415)[r], int((c + 1) * W / 3), (415, H)[r])
        got = read_bars(img, box, TICKS[gene], [f"{gene} 2D", f"{gene} 3D"], gaps=(gene == "Vimentin"), tick_win=(6, 7))
        out.update(got)
    return {"groups": out}
