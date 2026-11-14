"""Fig. S1L: force of contraction (μN), vector bars ± SEM; axis from tick rects and tick words.
Only the CTRL-medium bars are compared in the record's items; the SF bars are read but not returned."""
from _util import vector_bars


def read(fig):
    out = vector_bars(fig, ["ctrl_low", "sf_low", "ctrl_high", "sf_high", "ctrl_highmg", "sf_highmg"],
                      extra={"ctrl_high (vs high+MG)": "ctrl_high"})
    for lab in ("sf_low", "sf_high", "sf_highmg"):
        del out["groups"][lab]
    return out
