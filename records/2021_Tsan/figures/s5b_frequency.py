"""Supplemental Fig. 5b: spontaneous contraction frequency (Hz) of 2DMBs from four lines.

Raster (embedded at 300 dpi). Markers overlap and sit under the mean lines, so only the
mean line and the upper end of the error bar are read; no points, no n.
"""
from _util import read_scatter


def read(fig):
    g = read_scatter(fig, ["WTC", "MR18", "MR30", "MR48"], [0.0, 0.5, 1.0, 1.5])
    return {"groups": {k: {"points": [], "countable": False, "bar": v["bar"]} for k, v in g.items()}}
