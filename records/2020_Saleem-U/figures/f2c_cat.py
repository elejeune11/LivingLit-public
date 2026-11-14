"""Figure 2C (right half), Relative fluorescence [%] (raster, main.pdf p4).

Tick labels are inside the image; tick marks of the left y-axis located by pixel, assigned top to bottom: 150, 100, 50, 0
(the right-hand fluorescence axis carries the same ticks at the same heights).
Only mean lines right of the dotted divider (crop x > 630 px at 300 dpi) are read; baseline lines are drawn pale, so ink is any blue/red-dominant pixel and a line must be at least 30 px wide (markers are ~12 px).
Lines left to right: bl, braces, None. Markers overlap the lines, so they are not counted (countable: false).
"""
from _util import panel


def read(fig):
    return panel(fig, [150, 100, 50, 0], ch=0, labels=['bl', 'braces', None], sat=None, min_width=30, x_from=630)
