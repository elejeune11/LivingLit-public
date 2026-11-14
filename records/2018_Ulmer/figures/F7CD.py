"""Fig. 7C-D: mitochondrial DNA content (Mt-DNA/g-actin) and mitochondrial mass (mean fluorescent intensity, AU)
of control (blue) and blebbistatin-treated (green) EHTs, bars with error bars (raster, 300 dpi). Printed y tick
labels are stated here (C: 1500, 1000, 500, 0; D: 8 to 0 by 2). The crop holds C on the left and D's bar plot on
the right (the histogram of D is outside the crop)."""
from _util import read_bars


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    split = int(W * 0.53)
    out = {}
    out.update(read_bars(img, (0, 0, split, H), [1500, 1000, 500, 0], ["C ctrl", "C bleb"]))
    out.update(read_bars(img, (split, 0, W, H), [8, 6, 4, 2, 0], ["D ctrl", "D bleb"], zero_at_base=True))
    return {"groups": out}
