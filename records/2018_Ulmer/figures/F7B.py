"""Fig. 7B: contractility of control (blue) and blebbistatin-treated (green) EHTs, fold change (mean, normalized)
with error bars for eight parameters (raster, 300 dpi). Printed y tick labels 1.5, 1, 0.5, 0 are stated here."""
from _util import read_bars

PARAMS = ["peak force", "fractional shortening", "beating rate", "resting length", "T1 80", "T1 50", "T2 80", "T2 50"]


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    labels = [f"{p} {g}" for p in PARAMS for g in ("ctrl", "bleb")]
    return {"groups": read_bars(img, (0, 0, W, H), [1.5, 1.0, 0.5, 0.0], labels)}
