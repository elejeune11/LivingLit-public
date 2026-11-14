from livinglit.chains import run_chains, scaling_checks, library_consistency
from livinglit.formulas import Library, load_library
from livinglit.gate_derived import check_derived
from livinglit.models import Record, DerivedFile, FormulaEntry
from tests.helpers import record

STRESS = FormulaEntry.model_validate({"formula": "stress_def", "kind": "definition", "statement": "s",
                                      "equations": ["s = F/A"], "variables": {"s": "stress", "F": "force", "A": "area"},
                                      "tests": [{"given": {"F": 1, "A": 2}, "expect": {"s": 0.5}}], "does_not_apply": "x",
                                      "cites": {"text": "Gere", "url": "https://example.org"}})


def _rec():
    r = record()
    r["evidence"]["E2"] = {"unit": "F1", "measure": "twitch stress", "finding": "f", "compares": ["HC_RP", "HC_NP"],
                           "values": {"s_HC_RP": {"printed": "4.0", "unit": "mN/mm²", "group": "HC_RP"},
                                      "s_HC_NP": {"printed": "2.0", "unit": "mN/mm²", "group": "HC_NP"}},
                           "stats": {"test": "t-test", "p": "n.s."},
                           "anchor": {"quote": "stress", "where": "Results"}}
    return Record.model_validate(r)


def _df(formula="s = F/A", area="0.5", kind="constant"):
    lib = load_library()
    lib.entries["stress_def"] = STRESS
    return lib, DerivedFile.model_validate({
        "record": "2099_Synth", "formula_library_version": 0,
        "derived": {"E2.stress_HC_RP": {"item": "E2", "group": "HC_RP", "formula": formula,
                                         "anchor": {"quote": "stress was force divided by area", "where": "Methods"},
                                         "library": {"formula": "stress_def", "vars": {"s": "s", "F": "F", "A": "A"}},
                                         "inputs": {"F": {"item": "E1", "kind": "per sample"},
                                                    "A": {"printed": area, "unit": "mm²", "kind": kind,
                                                          "anchor": {"quote": "area", "where": "Methods"}}},
                                         "output": "E2.values.s_HC_RP"}}})


def test_chain_rebuilds_printed_value():
    """Values are carried along the chain and the printed output is judged against the rebuilt one, labelled derived by LivingLit (04-formulas, Checking a chain)."""
    lib, df = _df()
    r = run_chains(_rec(), df, lib)["E2.stress_HC_RP"]
    assert r.verdict == "consistent" and abs(r.rebuilt - 4.0) < 1e-9 and r.library_verdict == "consistent"
    assert r.as_dict()["rebuilt"]["origin"] == "derived by LivingLit"


def test_constant_factor_conclusion_unaffected():
    """A constant factor leaves t, P and direction unchanged: 'conclusion unaffected' (04-formulas, Wrong derivations)."""
    lib, df = _df(area="0.25")
    r = run_chains(_rec(), df, lib)["E2.stress_HC_RP"]
    assert r.verdict == "inconsistent" and any("conclusion unaffected" in f for f in r.flags)


def test_paper_formula_against_library():
    """The paper's formula is checked against the library symbolically; the flag names the entry and its kind (04-formulas, The formula library)."""
    lib, df = _df(formula="s = 2*F/A")
    v, flag = library_consistency(df.derived["E2.stress_HC_RP"], lib)
    assert v == "inconsistent" and flag.startswith("contradicts definition: stress_def")


def test_p_must_match_under_constant_scaling():
    """P for force and stress must match when the area is one constant; a difference rules out a constant area (04-formulas, Statistical formulas)."""
    lib, df = _df()
    c = scaling_checks(_rec(), df, lib)[0]
    assert c["verdict"] == "inconsistent" and c["entry"] == "constant_scaling_t"


def test_gate_derived():
    """Derivations are anchored and their inputs resolve (04-formulas, The formula agent; 07-building, Jobs)."""
    lib, df = _df()
    probs, rej = check_derived(_rec(), df, lib, found=lambda q: True)
    assert probs == [] and rej == []
    df.derived["E2.stress_HC_RP"].inputs["F"].item = "E9"
    probs, _ = check_derived(_rec(), df, lib, found=lambda q: True)
    assert any("E9" in p for p in probs)


def test_rejected_proposal_reported():
    """A proposed formula that fails its checks is rejected and reported; the step gets no formula (04-formulas, New formulas)."""
    lib, df = _df()
    bad = STRESS.model_copy(update={"formula": "bad_def", "cites": None})
    df.proposals.append(bad)
    _, rej = check_derived(_rec(), df, lib, found=lambda q: True)
    assert any("cites" in r for r in rej)


def test_chain_carries_reading_intervals():
    """A value derived from readings carries their uncertainty: consistent within reading when the printed value lies in the rebuilt interval (02-audit, Anchors and origins; 04-formulas, Checking a chain)."""
    from livinglit.models import Reading, FiguresFile
    lib, df = _df()
    d = df.derived["E2.stress_HC_RP"]
    d.inputs["F"] = d.inputs["F"].model_copy(update={"item": None, "reading": "f1/rp"})
    figs = FiguresFile.model_validate({"figures": {"f1": {"file": "m.pdf", "page": 1, "crop": [0, 0, 1, 1], "script": "figures/f.py",
                                                          "unit": "F1", "groups": {"rp": {"item": "E1", "group": "HC_RP", "unit_of_value": "mN"}}}}})
    rd = [Reading(figure="f1", group="rp", kind="mean", index=0, value=2.06, lo=1.97, hi=2.15)]
    r = run_chains(_rec(), df, lib, (), rd, figs)["E2.stress_HC_RP"]
    assert r.verdict == "consistent within reading"


def test_input_selects_point_on_curve_by_x():
    """A reading or data input on a curve selects its point by x (02-audit, Readings and data; 04-formulas, Derivations)."""
    from livinglit.models import Reading, FiguresFile
    lib, df = _df()
    d = df.derived["E2.stress_HC_RP"]
    d.inputs["F"] = d.inputs["F"].model_copy(update={"item": None, "reading": "f1/rp", "x": "10"})
    figs = FiguresFile.model_validate({"figures": {"f1": {"file": "m.pdf", "page": 1, "crop": [0, 0, 1, 1], "script": "figures/f.py",
                                                          "unit": "F1", "groups": {"rp": {"item": "E1", "group": "HC_RP", "unit_of_value": "mN"}}}}})
    rd = [Reading(figure="f1", group="rp", kind="mean", index=0, value=9.0, lo=8.9, hi=9.1, x=1),
          Reading(figure="f1", group="rp", kind="mean", index=0, value=2.0, lo=1.99, hi=2.01, x=10)]
    r = run_chains(_rec(), df, lib, (), rd, figs)["E2.stress_HC_RP"]
    assert abs(r.rebuilt - 4.0) < 1e-9


def test_rerun_after_apply_skips_applied_proposals():
    """Re-running a gate after its apply does not report its own applied proposals as existing (07-building, What the first build taught about the code)."""
    lib, df = _df()
    df.proposals.append(STRESS)
    _, rej = check_derived(_rec(), df, lib, found=lambda q: True)
    assert rej == []


def test_stated_inputs_carry_printed_precision():
    """A stated input carries the interval of its last printed digit, so a rebuilt value whose interval holds the printed value is consistent (04-formulas, Derivations)."""
    lib, df = _df(area="0.48")
    r = run_chains(_rec(), df, lib)["E2.stress_HC_RP"]
    assert r.verdict == "consistent" and r.interval[0] < 4.05 and r.interval_kind == "printed"


def _agg_df(aggregation, printed):
    from livinglit.models import DataValue
    r = record()
    r["evidence"]["E2"] = {"unit": "F1", "measure": "ratio", "finding": "f", "groups": ["HC_RP"],
                           "values": {"ratio_HC_RP": {"printed": printed, "unit": "dimensionless", "group": "HC_RP"}},
                           "anchor": {"quote": "ratio", "where": "Results"}}
    rec = Record.model_validate(r)
    rows = [DataValue(item="E1", group=g, file="d.xlsx", cell=f"{g}{i}", value=v, unit="mN")
            for g, vs in (("HC_RP", ["2", "4"]), ("HC_NP", ["1", "4"])) for i, v in enumerate(vs)]
    d = {"item": "E2", "group": "HC_RP", "formula": "r = a/b", "anchor": "not stated", "no_formula": "test",
         "inputs": {"a": {"data": "E1/HC_RP", "kind": "per sample"}, "b": {"data": "E1/HC_NP", "kind": "per sample"}},
         "output": "E2.values.ratio_HC_RP"}
    if aggregation:
        d["aggregation"] = aggregation
    df = DerivedFile.model_validate({"record": "2099_Synth", "formula_library_version": 0, "derived": {"E2.r": d}})
    return rec, df, rows


def test_aggregation_mean_of_per_sample():
    """A per-sample formula judged against a printed mean with aggregation 'mean of per-sample' averages the per-sample results (04-formulas, Derivations)."""
    rec, df, rows = _agg_df("mean of per-sample", "1.5")
    assert run_chains(rec, df, load_library(), rows)["E2.r"].verdict == "consistent"
    rec, df, rows = _agg_df("of means", "1.5")
    assert run_chains(rec, df, load_library(), rows)["E2.r"].verdict == "inconsistent"


def test_aggregation_not_stated_runs_both():
    """An unstated aggregation runs both as labelled alternatives (04-formulas, Derivations)."""
    rec, df, rows = _agg_df("not stated", "1.5")
    r = run_chains(rec, df, load_library(), rows)["E2.r"]
    assert r.verdict == "close" and any("mean of per-sample" in n for n in r.notes)


def test_derivation_group_must_exist():
    """A derivation's group is a group of its item's unit (04-formulas, Derivations)."""
    lib, df = _df()
    d = df.derived["E2.stress_HC_RP"].model_copy(update={"group": "GONE"})
    df = df.model_copy(update={"derived": {"E2.stress_HC_RP": d}})
    probs, _ = check_derived(_rec(), df, lib, found=lambda q: True)
    assert any("GONE" in p for p in probs)


def test_aggregation_alternative_uses_printed_interval():
    """Under an unstated aggregation, the mean-of-per-sample alternative is judged with the same printed-precision interval as the other (04-formulas, Derivations)."""
    from livinglit.chains import judge_rebuilt
    assert judge_rebuilt("4.0", 4.1667, (4.02, 4.32), "printed") == "consistent"
    assert judge_rebuilt("4.0", 4.1667, None, None) == "inconsistent"


def test_bound_on_a_single_variable():
    """A bound whose equation is the variable alone (f >= 0, f <= 1) is applied to a value without error (04-formulas, Bounds on an item)."""
    from livinglit.chains import bound_checks
    from livinglit.models import Bound
    e = FormulaEntry.model_validate({"formula": "fraction_bounds", "kind": "bound", "statement": "s", "equations": ["f >= 0", "f <= 1"],
                                     "variables": {"f": "dimensionless"}, "tests": [{"given": {"f": 0.4}}], "does_not_apply": "x",
                                     "cites": {"text": "t", "url": "https://example.org"}})
    lib = load_library()
    lib.entries["fraction_bounds"] = e
    r = record()
    r["evidence"]["E1"]["values"]["share"] = {"printed": "41%", "unit": "%", "group": "HC_RP"}
    rec = Record.model_validate(r)
    df = DerivedFile.model_validate({"record": "2099_Synth", "formula_library_version": 0,
                                     "bounds": [{"item": "E1", "value": "E1.values.share", "formula": "fraction_bounds"}]})
    assert bound_checks(rec, df, lib)[0]["verdict"] == "consistent"


def test_approximate_output_does_not_crash_the_chain():
    """An approximate printed output ("~4") is judged as approximate along a derivation, including the constant-factor check (04-formulas, Checking a chain)."""
    lib, df = _df(area="0.25")
    rec = _rec()
    rec.evidence["E2"].values["s_HC_RP"] = rec.evidence["E2"].values["s_HC_RP"].model_copy(update={"printed": "~4"})
    r = run_chains(rec, df, lib)["E2.stress_HC_RP"]
    assert r.verdict == "inconsistent"


def test_same_n_along_the_chain():
    """A derived value carries its measured input's n: equal n is consistent, a derived n larger than the n of the per-sample input it is computed from is inconsistent, and a smaller one (a subset of the measured samples) cannot be checked; a constant input has no n to carry (04-formulas, Checking a chain)."""
    from livinglit.chains import same_n_checks
    lib, df = _df()
    r = _rec().model_dump()
    r["evidence"]["E1"]["n"] = {"printed": "n = 8 tissues", "counts": "tissues"}
    r["evidence"]["E2"]["n"] = {"printed": "n = 8 tissues", "counts": "tissues"}
    c = same_n_checks(Record.model_validate(r), df)
    assert [x["verdict"] for x in c] == ["consistent"] and c[0]["check"] == "same n along the chain"
    r["evidence"]["E2"]["n"] = {"printed": "n = 10", "counts": "tissues", "per_group": {"HC_RP": "10", "HC_NP": "10"}}
    c = same_n_checks(Record.model_validate(r), df)
    assert c[0]["verdict"] == "inconsistent" and "8" in c[0]["note"] and "10" in c[0]["note"]
    r["evidence"]["E2"]["n"] = {"printed": "n = 6", "counts": "tissues", "per_group": {"HC_RP": "6", "HC_NP": "6"}}
    c = same_n_checks(Record.model_validate(r), df)
    assert c[0]["verdict"] == "cannot check" and "subset" in c[0]["note"]
    r["evidence"]["E2"]["n"] = "not stated"
    assert same_n_checks(Record.model_validate(r), df) == []
