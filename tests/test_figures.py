from pathlib import Path

from livinglit.figures.run import load_read, to_rows, compare_readings
from livinglit.figures.source import calibrate, point
from livinglit.data import check_rows
from livinglit.models import DataValue


def test_per_paper_helpers(tmp_path):
    """Each paper's helper code is that paper's alone; another paper's helper of the same name is never used (02-audit, Reading figures)."""
    for paper, val in (("A", 1), ("B", 2)):
        d = tmp_path / paper / "figures"
        d.mkdir(parents=True)
        (d / "_util.py").write_text(f"VALUE = {val}\n")
        (d / "f.py").write_text("from _util import VALUE\ndef read(fig):\n    return VALUE\n")
    assert load_read(tmp_path / "A" / "figures" / "f.py")(None) == 1
    assert load_read(tmp_path / "B" / "figures" / "f.py")(None) == 2
    assert load_read(tmp_path / "A" / "figures" / "f.py")(None) == 1


def test_calibration_and_intervals():
    """Axis calibration from matched tick labels; every reading has an interval and a page position (02-audit, Reading figures)."""
    cal = calibrate([(100, 0), (50, 10), (0, 20)])
    assert abs(cal.value(75) - 5) < 1e-9 and cal.residual < 1e-9
    p = point(cal, 75, 0.5, (10, 75), x=2)
    assert p["lo"] < 5 < p["hi"] and p["at"] == [10, 75] and p["x"] == 2


def test_rows_validated_and_compared():
    """Readings are a checked cache: a stored value that does not come back exactly fails (02-audit, Readings and data are stored as a checked cache)."""
    raw = {"groups": {"g": {"points": [{"value": 1.0, "lo": 0.9, "hi": 1.1, "at": [1, 2]}], "countable": True,
                            "bar": {"mean": [1.0, 0.95, 1.05]}}}}
    rows, errs = to_rows("f1", raw)
    assert errs == [] and len(rows) == 2
    changed = [r.model_copy(update={"value": 1.01}) if r.kind == "point" else r for r in rows]
    assert compare_readings(rows, changed)
    assert compare_readings(rows, rows) == []
    bad, errs = to_rows("f1", {"groups": {"g": {"points": [{"value": 2, "lo": 0, "hi": 1}]}}})
    assert errs


def test_data_cells_reread(tmp_path):
    """Every data pointer is re-read and must return the stored value exactly (02-audit, Readings and data are stored as a checked cache)."""
    (tmp_path / "d.csv").write_text("a,b\n1.5,2\n")
    ok = DataValue(item="E1", group="g", file="d.csv", cell="A2", value="1.5", unit="mN")
    bad = ok.model_copy(update={"value": "1.6"})
    assert check_rows([ok], tmp_path) == []
    assert check_rows([bad], tmp_path)


def test_axis_lines_kept():
    """Vector objects inside the crop include zero-width strokes (axis and tick lines) (02-audit, Reading figures)."""
    from livinglit.figures.source import _overlaps
    assert _overlaps((10, 0, 10, 50), (0, 0, 100, 100))
    assert not _overlaps((200, 0, 200, 50), (0, 0, 100, 100))


import pytest as _pytest


@_pytest.mark.papers
def test_xlsb_datasets_are_read():
    """Released datasets in .xlsb are read cell by cell like .xlsx, so their rows are checked the same way (CONTRIBUTING, Working here; 02-audit, Reading figures)."""
    from livinglit import PAPERS_DIR
    from livinglit.data import sheet_cells, xlsb_sheets
    p = PAPERS_DIR / "2016_Mannhardt" / "stemcr_515_mmc2.xlsb"
    if not p.exists():
        _pytest.skip("no xlsb in the corpus")
    sheets = xlsb_sheets(str(p))
    cells = sheet_cells(str(p), sheets[0], p.stat().st_mtime_ns)
    assert cells and all(k[0].isalpha() and k[-1].isdigit() for k in list(cells)[:20])


def test_overlay_command_draws_the_stored_readings_over_their_figure(tmp_path):
    """`livinglit overlay <paper> <figure>` draws every stored reading at its page position over the figure's crop, one colour per group, into a dont_commit folder outside the repository, for a person to inspect a reading (02-audit, Reading figures; CONTRIBUTING, Fixed rules)."""
    import pymupdf
    import numpy as np
    import yaml as _y
    from livinglit.figures.overlay import figure_overlay
    papers, recs = tmp_path / "papers" / "P", tmp_path / "records" / "P"
    papers.mkdir(parents=True)
    recs.mkdir(parents=True)
    doc = pymupdf.open()
    page = doc.new_page(width=200, height=200)
    page.draw_circle((50, 50), 2, color=(0, 0, 0), fill=(0, 0, 0))
    doc.save(str(papers / "synthetic.pdf"))
    (recs / "figures.yaml").write_text(_y.safe_dump({"figures": {"f1": {
        "file": "synthetic.pdf", "page": 1, "crop": [0, 0, 100, 100], "script": "figures/f1.py", "unit": "F1",
        "groups": {"a": {"item": "E1", "group": "a", "unit_of_value": ""}}}}}))
    (recs / "readings.yaml").write_text(_y.safe_dump({"readings": [
        {"figure": "f1", "group": "a", "kind": "point", "index": 0, "value": 1.0, "lo": 0.9, "hi": 1.1,
         "page_x": 50.0, "page_y": 50.0}]}))
    out = tmp_path / "overlays_dont_commit"
    p = figure_overlay("P", "f1", out, records_dir=tmp_path / "records", papers_dir=tmp_path / "papers")
    assert p.exists() and p.parent == out and p.suffix == ".png"
    import cv2
    img = cv2.imread(str(p))
    scale = img.shape[1] / 100
    ring = img[int(50 * scale) - 6:int(50 * scale) + 7, int(50 * scale) - 6:int(50 * scale) + 7]
    assert np.any((ring[:, :, 2] > 150) & (ring[:, :, 1] < 120))  # a coloured marker drawn at the reading
    import pytest
    from livinglit import ROOT
    with pytest.raises(ValueError):
        figure_overlay("P", "f1", ROOT / "x_dont_commit", records_dir=tmp_path / "records", papers_dir=tmp_path / "papers")
