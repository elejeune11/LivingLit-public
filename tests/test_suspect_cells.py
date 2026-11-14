"""Suspect cells run with and without (02-audit, Checks within a source)."""
from livinglit.models import Record, DataValue, Suspect
from livinglit.checks import check_item, gather
from livinglit.across import item_direction, direction_with_suspects
from livinglit.formulas import load_library
from tests.helpers import record

LIB = load_library()


def _rec():
    r = record()
    e = r["evidence"]["E1"]
    e["values"] = {}
    e["stats"] = {"test": "unpaired t-test", "p": "P < 0.05"}
    return Record.model_validate(r)


def _rows(suspect_value="68"):
    rows = []
    for i, v in enumerate(["0.9", "1.1", "1.0", "1.2", suspect_value]):
        rows.append(DataValue(item="E1", group="HC_RP", file="d.xlsx", cell=f"A{i}", value=v, unit="mN",
                              **({"suspect": {"why": "68 among values near 1"}} if v == suspect_value else {})))
    for i, v in enumerate(["2.0", "2.2", "1.9", "2.1", "2.3"]):
        rows.append(DataValue(item="E1", group="HC_NP", file="d.xlsx", cell=f"B{i}", value=v, unit="mN"))
    return rows


def test_suspect_cell_is_kept_and_can_be_dropped():
    """A data cell logged as suspect is kept, and gather can leave it out for the second run (02-audit, Checks within a source)."""
    rec, rows = _rec(), _rows()
    assert len(gather(rec, "E1", rows)["HC_RP"].data_points) == 5
    ev = gather(rec, "E1", rows, drop_suspect=True)
    assert len(ev["HC_RP"].data_points) == 4


def test_direction_that_changes_without_suspect_is_not_available():
    """A direction that changes when a suspect cell is left out is not available (suspect cell) (02-audit, Checks within a source)."""
    rec, rows = _rec(), _rows()
    plain = item_direction(rec.evidence["E1"], gather(rec, "E1", rows))
    assert plain.direction == "up"  # 68 drags the mean up
    d = direction_with_suspects(rec.evidence["E1"], rec, "E1", rows)
    assert d.direction is None and "suspect" in d.basis


def test_checks_run_twice_and_are_labelled():
    """Every check that uses a suspect cell runs with and without it, as labelled alternatives (02-audit, Checks within a source)."""
    rec, rows = _rec(), _rows()
    cs = [c for c in check_item(rec, "E1", LIB, rows) if c.check == "points to P"]
    assert cs and any("suspect" in (a.get("label") or "") for a in cs[0].alternatives)


def test_n_count_keeps_the_suspect_replicate():
    """A suspect cell is still a replicate: the n count is judged with it, not re-run without it (02-audit, Checks within a source)."""
    rec, rows = _rec(), _rows()
    r = record()
    r["evidence"]["E1"]["values"] = {}
    r["evidence"]["E1"]["n"] = {"printed": "n = 5", "counts": "tissues"}
    r["evidence"]["E1"]["stats"] = {"test": "unpaired t-test", "p": "P < 0.05"}
    rec = Record.model_validate(r)
    ns = [c for c in check_item(rec, "E1", LIB, rows) if c.check.startswith("n ") and "suspect" in c.note]
    assert not ns


def test_suspect_in_the_family_triggers_the_second_run():
    """A suspect cell in another item of the post-hoc family also runs the check with and without it (02-audit, Checks within a source)."""
    from tests.test_posthoc import _rec as ph_rec
    rec, rows = ph_rec("one-way ANOVA with Tukey's post hoc test", "P < 0.05")
    rows = [r.model_copy(update={"suspect": Suspect(why="slip")}) if (r.item == "E3" and r.cell == "LC_NP0") else r for r in rows]
    cs = [c for c in check_item(rec, "E1", LIB, rows) if c.check == "points to P"]
    assert cs and "suspect" in cs[0].note
