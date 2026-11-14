import copy

from livinglit.checks import check_item, status, depth, combine_alternatives, Check
from livinglit.formulas import load_library
from livinglit.models import Record, DataValue, Reading, FiguresFile
from tests.helpers import record

LIB = load_library()


def _rec(**item):
    r = record()
    r["evidence"]["E1"].update(item)
    return Record.model_validate(r)


def _by(checks, name):
    return [c for c in checks if c.check == name]


def test_summary_to_p_consistent_names_entries():
    """Summary to P applies t_two_sample_* and t_distribution and names them (04-formulas, Statistical formulas; 02-audit, Checks within a source)."""
    c = _by(check_item(_rec(), "E1", LIB), "summary to P")[0]
    assert c.verdict == "consistent" and "t_two_sample_pooled" in c.entry and "t_distribution" in c.entry
    assert {a["entry"] for a in c.alternatives} == {"t_two_sample_pooled", "t_two_sample_welch"}


def test_unequal_variances_is_welch_only():
    """'Student's t test assuming unequal variances' runs as Welch only (02-audit, Checks within a source)."""
    rec = _rec(stats={"test": "Two-tailed, unpaired Student's t test assuming unequal variances", "p": "P < 0.01"})
    c = _by(check_item(rec, "E1", LIB), "summary to P")[0]
    assert {a["entry"] for a in c.alternatives} == {"t_two_sample_welch"}


def test_summary_to_p_inconsistent():
    """A check that fails under every alternative is inconsistent (02-audit, Status and depth)."""
    rec = _rec(stats={"test": "unpaired t-test", "p": "P = 0.5"})
    assert _by(check_item(rec, "E1", LIB), "summary to P")[0].verdict == "inconsistent"


def test_posthoc_pair_cannot_check():
    """A pairwise P from a post-hoc test is not rechecked with a two-group test: cannot check, naming the test (02-audit, Checks within a source)."""
    rec = _rec(stats={"test": "one-way ANOVA with Tukey's post hoc test", "p": "P < 0.05"})
    c = _by(check_item(rec, "E1", LIB), "summary to P")[0]
    assert c.verdict == "cannot check" and "Tukey" in c.note


def test_omnibus_only_one_way():
    """An omnibus P is rechecked only when the printed test is a one-way ANOVA (02-audit, Checks within a source)."""
    r = record()
    e = r["evidence"]["E1"]
    e["compares"] = ["HC_RP", "HC_NP", "LC_NP"]
    e["test_of"] = "omnibus"
    e["values"]["force_LC_NP"] = {"printed": "1.1 ± 0.4", "unit": "mN", "group": "LC_NP", "spread": "SD"}
    e["n"] = {"printed": "n = 6", "counts": "tissues"}
    e["stats"] = {"test": "two-way ANOVA", "p": "P < 0.05"}
    assert _by(check_item(Record.model_validate(r), "E1", LIB), "summary to P")[0].verdict == "cannot check"
    e["stats"] = {"test": "one-way ANOVA", "p": "P < 0.01"}
    c = _by(check_item(Record.model_validate(r), "E1", LIB), "summary to P")[0]
    assert c.verdict in ("consistent", "close") and "one_way_anova_f" in c.entry


def _rows(group, vals, unit="mN", item="E1"):
    return [DataValue(item=item, group=group, file="d.xlsx", cell=f"A{i}", value=str(v), unit=unit) for i, v in enumerate(vals)]


def test_n_against_data_catches_swapped_n():
    """Do data groups match the printed n per group; n swapped between arms is inconsistent (02-audit, Checks within a source)."""
    rec = _rec(n={"printed": "n = 5 and 7", "counts": "tissues", "per_group": {"HC_RP": "5", "HC_NP": "7"}})
    rows = _rows("HC_RP", [2, 2.5, 1.5, 2.2, 1.8, 2.1, 1.9]) + _rows("HC_NP", [1, 1.4, 0.6, 1.1, 0.9])
    cs = _by(check_item(rec, "E1", LIB, rows), "n against data")
    assert [c.verdict for c in cs] == ["inconsistent", "inconsistent"]


def test_points_to_p_from_data_depth_data():
    """Points (data) give the printed P, and depth is data (02-audit, Status and depth)."""
    rows = _rows("HC_RP", [2, 2.5, 1.5, 2.2, 1.8, 2.0]) + _rows("HC_NP", [1, 1.4, 0.6, 1.1, 0.9, 1.0])
    cs = check_item(_rec(), "E1", LIB, rows)
    assert _by(cs, "points to P")[0].verdict == "consistent"
    assert depth(cs) == "data"


def test_units_through_data_unit():
    """A printed value and points in another unit are never compared: cannot check, naming both (02-audit, Checks within a source)."""
    rows = _rows("HC_RP", [2, 2.5, 1.5], unit="ms")
    c = _by(check_item(_rec(), "E1", LIB, rows), "against data")[0]
    assert c.verdict == "cannot check" and "ms" in c.note
    rows = _rows("HC_RP", [2000, 2000, 2000], unit="µN")
    assert _by(check_item(_rec(), "E1", LIB, rows), "against data")[0].verdict == "consistent"


def test_readings_give_within_reading_and_exact_vector_counts():
    """Vector counts are exact; P from read values is an interval, giving consistent within reading (02-audit, Reading figures; Checks within a source)."""
    figs = FiguresFile.model_validate({"figures": {"f1": {"file": "main.pdf", "page": 1, "crop": [0, 0, 1, 1], "script": "figures/f1.py",
                                                          "unit": "F1", "kind": "vector",
                                                          "groups": {"rp": {"item": "E1", "group": "HC_RP", "unit_of_value": "mN"},
                                                                     "np": {"item": "E1", "group": "HC_NP", "unit_of_value": "mN"}}}}})
    rd = [Reading(figure="f1", group="rp", kind="point", index=i, value=v, lo=v - 0.01, hi=v + 0.01) for i, v in enumerate([2, 2.5, 1.5, 2.2, 1.8, 2.0])]
    rd += [Reading(figure="f1", group="np", kind="point", index=i, value=v, lo=v - 0.01, hi=v + 0.01) for i, v in enumerate([1, 1.4, 0.6, 1.1, 0.9, 1.0])]
    cs = check_item(_rec(), "E1", LIB, (), rd, figs)
    assert _by(cs, "points to P")[0].verdict == "consistent within reading"
    assert {c.verdict for c in _by(cs, "n against readings")} == {"consistent within reading"}
    assert depth(cs) == "readings"


def test_which_spread():
    """Is the ± an SD or SEM, whatever the label says (02-audit, Checks within a source)."""
    pts = [2, 2.5, 1.5, 2.2, 1.8, 2.0]
    r = record()
    r["evidence"]["E1"]["values"]["force_HC_RP"]["printed"] = "2.0 ± 0.14"  # the SEM, labelled SD
    rec = Record.model_validate(r)
    c = _by(check_item(rec, "E1", LIB, _rows("HC_RP", pts)), "which spread")[0]
    assert c.verdict == "inconsistent" and "SEM" in c.note


def test_status_rules():
    """Status is set by code from the item's own checks only (02-audit, Status and depth)."""
    C = lambda v, b="printed": Check("x", v, basis=b)
    assert status([]) == "cannot check"
    assert status([C("consistent"), C("cannot check")]) == "consistent"
    assert status([C("consistent"), C("consistent within reading")]) == "consistent within reading"
    assert status([C("consistent"), C("close")]) == "close"
    assert status([C("close"), C("inconsistent")]) == "inconsistent"
    assert combine_alternatives(["consistent", "inconsistent"]) == "close"
    assert depth([C("consistent", "printed")]) == "printed only"


def test_reported_twice():
    """Do text and legend values for the same group agree (02-audit, Checks within a source)."""
    r = record()
    r["evidence"]["E1"]["values"]["force_HC_RP_text"] = {"printed": "2.4", "unit": "mN", "group": "HC_RP"}
    c = _by(check_item(Record.model_validate(r), "E1", LIB), "reported twice")[0]
    assert c.verdict == "inconsistent"


def test_statistic_to_p():
    """Does P follow from the statistic and degrees of freedom (02-audit, Checks within a source)."""
    rec = _rec(stats={"test": "unpaired t-test", "statistic": "t = 2.3", "df": "10", "p": "P = 0.044"})
    c = _by(check_item(rec, "E1", LIB), "statistic to P")[0]
    assert c.verdict in ("consistent", "close") and c.entry == "t_distribution"


def test_read_p_interval_bracketing_printed_p():
    """P from read values is an interval: one that brackets an exactly printed P is consistent within reading (02-audit, Checks within a source)."""
    from livinglit.checks import p_from_interval
    assert p_from_interval("P = 0.003", 0.001, 0.01) == "consistent within reading"
    assert p_from_interval("P < 0.05", 0.001, 0.01) == "consistent within reading"
    assert p_from_interval("P < 0.05", 0.01, 0.2) == "close"
    assert p_from_interval("P = 0.003", 0.2, 0.5) == "inconsistent"


def test_reported_twice_needs_same_quantity():
    """Reported twice compares one quantity printed in two places (names differing only by a source suffix), never two quantities of one group (02-audit, Checks within a source)."""
    r = record()
    r["evidence"]["E1"]["values"]["peak_HC_RP"] = {"printed": "9.9", "unit": "mN", "group": "HC_RP"}
    assert not _by(check_item(Record.model_validate(r), "E1", LIB), "reported twice")


def test_reported_twice_judges_coarser_value():
    """A value reported twice at different precision is judged at the coarser printed precision (02-audit, Checks within a source)."""
    r = record()
    r["evidence"]["E1"]["values"]["force_HC_RP"]["printed"] = "10.68022906"
    r["evidence"]["E1"]["values"]["force_HC_RP_text"] = {"printed": "10.7", "unit": "mN", "group": "HC_RP"}
    assert _by(check_item(Record.model_validate(r), "E1", LIB), "reported twice")[0].verdict == "consistent"


def test_n_up_to_is_a_bound():
    """'n = up to 6' is a bound: any n from 2 to 6, never exactly 6 (02-audit, Checks within a source)."""
    from livinglit.checks import parse_n
    assert parse_n("n = up to 6") == [2, 3, 4, 5, 6]
    assert parse_n("n = 6") == [6]


def test_n_at_least_is_a_lower_bound():
    """'n ≥ 6' is a lower bound: 6 or more, never exactly 6, and no exact n (02-audit, Checks within a source)."""
    from livinglit.checks import parse_n, parse_n_min
    for printed, k in [("n ≥ 6", 6), ("n >= 6", 6), ("n > 5", 6), ("at least 4 tissues", 4), ("n = 3 or more", 3),
                       ("a minimum of 5 EHTs", 5)]:
        assert parse_n_min(printed) == k, printed
        assert parse_n(printed) == [], printed
    assert parse_n_min("n = 6") is None and parse_n_min("n = up to 6") is None
    assert parse_n_min("5-6 tissues per group, with at least 50 cells per EHT") is None  # the bound is not on n


def test_n_against_readings_with_a_lower_bound():
    """Points counted against 'n ≥ 6': 6 or 8 points agree, 5 do not (02-audit, Checks within a source)."""
    from livinglit.checks import GroupEvidence, n_checks
    def verdict(k):
        e = GroupEvidence(n=[], n_min=6, read_points=[(1.0, 0.9, 1.1)] * k, read_counts_exact=True)
        return [c.verdict for c in n_checks("X", {"g": e}) if c.check == "n against readings"]
    assert verdict(8) == ["consistent within reading"] and verdict(6) == ["consistent within reading"]
    assert verdict(5) == ["inconsistent"]


def test_n_implied_by_error_bar_can_be_inconsistent():
    """(SD of points / bar)² far from the printed n is inconsistent; a bar the size of the SD (implied n ≈ 1) is left to 'which spread' (02-audit, Checks within a source)."""
    from livinglit.checks import n_from_bar_verdict
    assert n_from_bar_verdict(6.1, [6]) == "consistent within reading"
    assert n_from_bar_verdict(8.0, [6]) == "close"
    assert n_from_bar_verdict(20.0, [6]) == "inconsistent"
    assert n_from_bar_verdict(1.1, [6]) == "cannot check"
