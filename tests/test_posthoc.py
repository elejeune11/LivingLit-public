"""Post-hoc pairs and two-way ANOVA effects checked from points only (02-audit, Checks within a source; 04-formulas, Statistical formulas)."""
import itertools

import numpy as np
from scipy import stats

from livinglit.models import Record, DataValue
from livinglit.checks import check_item
from livinglit.formulas import load_library
from tests.helpers import record

LIB = load_library()
PTS = {"HC_RP": [2.1, 2.4, 2.0, 2.6, 2.3], "HC_NP": [1.2, 1.5, 1.1, 1.4, 1.3],
       "LC_RP": [1.6, 1.9, 1.5, 1.8, 1.7], "LC_NP": [1.0, 1.2, 0.9, 1.3, 1.1]}


def _rec(test, p1, p2="P < 0.05", e1=("HC_RP", "HC_NP"), e3=("LC_RP", "LC_NP")):
    r = record()
    base = r["evidence"]["E1"]
    base.update({"values": {}, "n": "not stated", "compares": list(e1), "stats": {"test": test, "p": p1}})
    r["evidence"]["E3"] = {**base, "compares": list(e3), "stats": {"test": test, "p": p2}}
    rows = [DataValue(item=it, group=g, file="d.xlsx", cell=f"{g}{i}", value=str(v), unit="mN")
            for it, gs in (("E1", e1), ("E3", e3)) for g in gs for i, v in enumerate(PTS[g])]
    return Record.model_validate(r), rows


def _tukey_p(a, b):
    names = list(PTS)
    res = stats.tukey_hsd(*[PTS[n] for n in names])
    return res.pvalue[names.index(a)][names.index(b)]


def test_tukey_pair_checked_from_points_of_the_whole_family():
    """A printed Tukey pair is checked with tukey_kramer_q and the studentized range over every group of the unit, from points (04-formulas, Statistical formulas)."""
    p = _tukey_p("HC_RP", "HC_NP")
    rec, rows = _rec("one-way ANOVA with Tukey's post hoc test", f"P = {p:.4f}")
    cs = [c for c in check_item(rec, "E1", LIB, rows) if c.check == "points to P"]
    assert cs and "tukey_kramer_q" in cs[0].entry and cs[0].basis == "data"
    assert [a["verdict"] for a in cs[0].alternatives if a["variance"].startswith("equal") and a["family"] == "all groups of the unit"] == ["consistent"]


def test_tukey_wrong_p_inconsistent():
    """A printed Tukey P that the points do not give is inconsistent (02-audit, Checks within a source)."""
    rec, rows = _rec("one-way ANOVA with Tukey's post hoc test", "P = 0.40")
    cs = [c for c in check_item(rec, "E1", LIB, rows) if c.check == "points to P"]
    assert cs[0].verdict == "inconsistent"


def test_family_not_determined_cannot_check():
    """When some groups of the unit have no points, the family is not determined and the post-hoc pair cannot be checked (02-audit, Checks within a source)."""
    rec, rows = _rec("one-way ANOVA with Tukey's post hoc test", "P < 0.05")
    rows = [r for r in rows if r.group != "LC_NP"]
    cs = [c for c in check_item(rec, "E1", LIB, rows) if c.check == "points to P"]
    assert cs and cs[0].verdict == "cannot check" and "family" in cs[0].note


def test_bonferroni_pair_runs_family_sizes_as_alternatives():
    """A Bonferroni pair is a pooled t over the family, adjusted for m comparisons; all pairs and printed pairs are labelled alternatives (04-formulas, Statistical formulas)."""
    rec, rows = _rec("one-way ANOVA with Bonferroni's multiple comparisons test", "P < 0.001")
    cs = [c for c in check_item(rec, "E1", LIB, rows) if c.check == "points to P"]
    assert cs and "bonferroni_adjust" in cs[0].entry and {6, 2} <= {a["m"] for a in cs[0].alternatives}


def _two_way_p(term):
    a = {"HC": ["HC_RP", "HC_NP"], "LC": ["LC_RP", "LC_NP"]}
    b = {"RP": ["HC_RP", "LC_RP"], "NP": ["HC_NP", "LC_NP"]}
    allv = [v for g in PTS.values() for v in g]
    M, n = np.mean(allv), 5
    cell = {g: np.mean(v) for g, v in PTS.items()}
    ssa = sum(2 * n * (np.mean([cell[g] for g in gs]) - M) ** 2 for gs in a.values())
    ssb = sum(2 * n * (np.mean([cell[g] for g in gs]) - M) ** 2 for gs in b.values())
    sscell = sum(n * (m - M) ** 2 for m in cell.values())
    ssab = sscell - ssa - ssb
    sse = sum(sum((x - cell[g]) ** 2 for x in v) for g, v in PTS.items())
    ss = {"a": ssa, "b": ssb, "ab": ssab}[term]
    return stats.f.sf(ss / (sse / 16), 1, 16)


def test_two_way_main_effect_from_points():
    """A two-way ANOVA main effect in a factorial unit is checked with two_way_anova_f from the points of every cell (04-formulas, Statistical formulas)."""
    p = _two_way_p("b")
    r = record()
    r["evidence"]["E1"].update({"values": {}, "n": "not stated", "compares": None, "test_of": "main effect",
                                "stats": {"test": "two-way ANOVA", "p": f"P = {p:.3g}"}})
    r["evidence"]["E1"]["compares"] = {"condition": ["HC_RP", "LC_RP"], "reference": ["HC_NP", "LC_NP"]}
    rec = Record.model_validate(r)
    rows = [DataValue(item="E1", group=g, file="d.xlsx", cell=f"{g}{i}", value=str(v), unit="mN")
            for g in PTS for i, v in enumerate(PTS[g])]
    cs = [c for c in check_item(rec, "E1", LIB, rows) if c.check == "points to P"]
    assert cs and cs[0].verdict == "consistent" and "two_way_anova_f" in cs[0].entry


def test_two_way_interaction_from_points():
    """A two-way ANOVA interaction is checked from the points of every cell (04-formulas, Statistical formulas)."""
    p = _two_way_p("ab")
    r = record()
    r["evidence"]["E1"].update({"values": {}, "n": "not stated", "compares": list(PTS), "test_of": "interaction",
                                "stats": {"test": "two-way ANOVA", "p": f"P = {p:.3g}"}})
    rec = Record.model_validate(r)
    rows = [DataValue(item="E1", group=g, file="d.xlsx", cell=f"{g}{i}", value=str(v), unit="mN")
            for g in PTS for i, v in enumerate(PTS[g])]
    cs = [c for c in check_item(rec, "E1", LIB, rows) if c.check == "points to P"]
    assert cs and cs[0].verdict == "consistent"


def test_repeated_measures_not_checked():
    """Repeated-measures and mixed models are not in the library: cannot check, naming the test (04-formulas, Statistical formulas)."""
    rec, rows = _rec("two-way repeated measures ANOVA with Tukey's post hoc test", "P < 0.05")
    cs = [c for c in check_item(rec, "E1", LIB, rows) if c.check == "points to P"]
    assert all(c.verdict == "cannot check" for c in cs)


def test_factorial_pair_family_within_the_other_factor():
    """In a factorial unit, a post-hoc pair differing in one factor is also checked within the level of the other factor; "within each" or "for each" in the test leaves only that family (02-audit, Checks within a source)."""
    rec, rows = _rec("two-way ANOVA with Bonferroni's multiple comparisons test", "P < 0.001")
    cs = [c for c in check_item(rec, "E1", LIB, rows) if c.check == "points to P"]
    fams = {a.get("family") for a in cs[0].alternatives}
    assert any(f and f.startswith("within") for f in fams) and "all pairs of the unit" in fams
    rec2, rows2 = _rec("two-way ANOVA with Bonferroni's test within each calcium level", "P < 0.001")
    cs2 = [c for c in check_item(rec2, "E1", LIB, rows2) if c.check == "points to P"]
    assert {a.get("family") for a in cs2[0].alternatives} == {f for f in fams if f and f.startswith("within")}


def test_unequal_variance_alternatives_always_run():
    """Equal variances are rarely stated, so a post-hoc pair also runs its unequal-variance form as a labelled alternative: Games–Howell beside Tukey, Welch raw P beside the pooled t for adjusted tests (04-formulas, Statistical formulas)."""
    p = _tukey_p("HC_RP", "HC_NP")
    rec, rows = _rec("one-way ANOVA with Tukey's post hoc test", f"P = {p:.4f}")
    c = [c for c in check_item(rec, "E1", LIB, rows) if c.check == "points to P"][0]
    assert any(a.get("variance") == "unequal (Games–Howell)" for a in c.alternatives)
    rec, rows = _rec("one-way ANOVA with Bonferroni's multiple comparisons test", "P < 0.001")
    c = [c for c in check_item(rec, "E1", LIB, rows) if c.check == "points to P"][0]
    assert any(a.get("variance") == "unequal (Welch)" for a in c.alternatives)
    assert "games_howell_q" in LIB.entries
