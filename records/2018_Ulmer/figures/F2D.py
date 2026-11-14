"""Fig. 2D (FAO enzymes): fold change of normalized spectral count, 2D (light grey) and EHT (dark) bars
with error bars for 11 proteins (raster, 300 dpi). Printed y tick labels 5.0 to 0.0 in steps of 0.5 are stated
here; tick marks, bar tops and error-bar ends are found by code."""
from _util import read_bars

PROTEINS = ["ACOT1", "ACOT13", "SCP2", "ACAA2", "ACOT2", "ECI1", "ECHS1", "OXCT1", "HADHA", "HADHB", "ACADVL"]
TICKS = [5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0.0]


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    labels = [f"{p} {g}" for p in PROTEINS for g in ("2D", "EHT")]
    return {"groups": read_bars(img, (0, 0, W, H), TICKS, labels)}
