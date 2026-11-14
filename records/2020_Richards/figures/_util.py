"""Helpers for 2020_Richards figures that live as raster images inside the supplement .docx.

FigureSource opens the .docx (PyMuPDF reads it) but its layout drops the embedded
images, so these helpers read the image straight from the .docx archive, in memory.
"""
from __future__ import annotations

import zipfile

import numpy as np


def docx_image(path, member: str) -> np.ndarray:
    """RGB array of an image embedded in a .docx, its transparency composited on white."""
    import pymupdf
    with zipfile.ZipFile(path) as z:
        pix = pymupdf.Pixmap(z.read(member))
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n).astype(float)
    rgb = a[:, :, :3]
    if pix.alpha:
        al = a[:, :, -1:] / 255.0
        rgb = rgb * al + 255.0 * (1 - al)
    return rgb.round().astype(np.uint8)


def dark(img: np.ndarray, threshold: int = 90) -> np.ndarray:
    """Black line pixels: every channel below threshold."""
    return img.astype(int).max(axis=2) < threshold


def row_centre(img: np.ndarray, rows: range, cols: range) -> float:
    """Darkness-weighted centre row of a short horizontal line (a tick mark) inside a window."""
    win = img[rows.start:rows.stop, cols.start:cols.stop].astype(float).mean(axis=2)
    w = (255.0 - win).sum(axis=1)
    return float((np.arange(rows.start, rows.stop) * w).sum() / w.sum())
