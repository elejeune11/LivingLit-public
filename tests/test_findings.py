import copy

from livinglit.findings import group_findings
from livinglit.models import Record
from tests.helpers import record


def _rec():
    r = record()
    e2 = copy.deepcopy(r["evidence"]["E1"])
    e2["compares"] = ["HC_RP", "LC_RP"]
    r["evidence"]["E2"] = e2
    return Record.model_validate(r)


def _items(**checks):
    return {iid: {"unit": "F1", "status": "inconsistent", "checks": cs} for iid, cs in checks.items()}


def test_one_legend_n_error_is_one_finding():
    """Failing n checks in one unit that rest on the same printed n for the same group are one finding listing every item (02-audit, Findings, not item counts)."""
    bad = {"check": "n against data", "verdict": "inconsistent", "target": "x/HC_RP n", "basis": "data",
           "note": "7 data points, printed n [6]"}
    ok = {"check": "n against data", "verdict": "consistent", "target": "x/HC_NP n", "basis": "data"}
    fs = group_findings(_rec(), _items(E1=[bad, ok], E2=[dict(bad, target="y/HC_RP n")]))
    assert len(fs) == 1
    assert fs[0]["items"] == ["E1", "E2"] and fs[0]["unit"] == "F1" and fs[0]["verdict"] == "inconsistent"
    assert "HC_RP" in fs[0]["source"] and "n = 6" in fs[0]["source"]


def test_different_causes_stay_apart_and_passing_checks_make_none():
    """Checks of different kinds, or resting on different printed sources, are separate findings; consistent and cannot-check verdicts make no finding (02-audit, Findings, not item counts)."""
    p = {"check": "points to P", "verdict": "inconsistent", "target": "E1", "basis": "data"}
    n = {"check": "n against data", "verdict": "close", "target": "x/HC_NP n", "basis": "data"}
    cc = {"check": "summary to P", "verdict": "cannot check", "target": "E2", "basis": "printed"}
    fs = group_findings(_rec(), _items(E1=[p, n], E2=[cc]))
    assert sorted(f["check"] for f in fs) == ["n against data", "points to P"]
    assert {f["verdict"] for f in fs} == {"inconsistent", "close"}


def test_p_checks_under_one_stated_test_share_a_finding():
    """Failing P checks of items in one unit under the same printed test are one finding, since they share the test and its family (02-audit, Findings, not item counts)."""
    p = {"check": "points to P", "verdict": "inconsistent", "target": "", "basis": "data"}
    fs = group_findings(_rec(), _items(E1=[p], E2=[p]))
    assert len(fs) == 1 and fs[0]["items"] == ["E1", "E2"] and "unpaired t-test" in fs[0]["source"]


def test_data_check_finding_names_the_data_file():
    """A failing check against released data names the data file the group's values come from (02-audit, Findings, not item counts)."""
    from types import SimpleNamespace as S
    c = {"check": "against data", "verdict": "inconsistent", "target": "E1/HC_RP mean", "basis": "data"}
    fs = group_findings(_rec(), _items(E1=[c]), data_rows=[S(item="E1", group="HC_RP", file="source_data.xlsx")])
    assert fs[0]["source"] == "data file source_data.xlsx, group HC_RP"
