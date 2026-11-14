"""The gold set gates every check (02-audit, Not the paper's error; 08 decision 44)."""
from pathlib import Path

import pytest
import yaml

from livinglit.checks import check_item, status
from livinglit.formulas import load_library
from livinglit.gate_record import load_record_files

GOLD = yaml.safe_load((Path(__file__).parent / "gold" / "gold.yaml").read_text())["entries"]
_cache = {}


def _checks(paper, item):
    if paper not in _cache:
        _cache[paper] = (load_record_files(paper), load_library())
    (rec, figs, rd, data), lib = _cache[paper]
    return check_item(rec, item, lib, data.data, rd.readings, figs)


def _passes(e) -> tuple[bool, str]:
    cs = _checks(e["paper"], e["item"])
    if "status" in e:
        got = status(cs)
        return got == e["status"], f"status {got}"
    vs = [c.verdict for c in cs if c.check == e["check"]]
    if not vs:
        return False, f"no {e['check']!r} check"
    ok = (any if e["match"] == "any" else all)(v == e["verdict"] for v in vs)
    return ok, f"{e['check']}: {vs}"


def test_gold_entries_are_well_formed():
    """Every gold entry names a paper, an item, either a status or a check with match and verdict, and why it is gold (02-audit, Not the paper's error)."""
    for e in GOLD:
        assert {"paper", "item", "why"} <= set(e), e
        assert ("status" in e) != ("check" in e), e
        if "check" in e:
            assert e["match"] in ("any", "all") and e["verdict"], e


@pytest.mark.papers
@pytest.mark.parametrize("e", [e for e in GOLD if "open" not in e], ids=lambda e: f"{e['paper']}:{e['item']}")
def test_gold_entry_reproduced(e):
    """Every closed gold entry's confirmed verdict is reproduced by the current checks (02-audit, Not the paper's error)."""
    ok, got = _passes(e)
    assert ok, f"{e['paper']} {e['item']}: expected {e.get('status') or e['verdict']}, got {got} ({e['why']})"


@pytest.mark.papers
@pytest.mark.parametrize("e", [e for e in GOLD if "open" in e], ids=lambda e: f"{e['paper']}:{e['item']}")
def test_open_gold_entry_still_open(e):
    """An open gold entry is a known artefact: it must still fail, and passing means the entry is closed by hand (02-audit, Not the paper's error)."""
    ok, got = _passes(e)
    assert not ok, f"{e['paper']} {e['item']} now passes ({got}): remove its `open` note to close it"
