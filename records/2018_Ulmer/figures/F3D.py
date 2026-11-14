"""Fig. 3D: western blot quantification (fold change, AU) of THIM and ATP5H, bars 2D (black), EHT (light grey),
NFH (grey) with error bars (raster, 300 dpi). Printed y tick labels 4 to 0 are stated here; the two plots are the
left and right halves of the crop."""
from _util import alias, read_bars

TICKS = [4, 3, 2, 1, 0]


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    out = {}
    for i, prot in enumerate(["THIM", "ATP5H"]):
        box = (0, 0, 396, H) if i == 0 else (396, 0, W, H)
        out.update(read_bars(img, box, TICKS, [f"{prot} {g}" for g in ("2D", "EHT", "NFH")]))
    return {"groups": alias(out, {"THIM 2D vs NFH": "THIM 2D", "ATP5H 2D vs NFH": "ATP5H 2D"})}
