from livinglit.models import FormulaEntry
from livinglit.formulas import Library, check_entry, follows, evaluate, parse_expr
import sympy as sp

CITE = {"text": "Gere, Mechanics of Materials", "quote": "stress is force per unit area"}


def E(**kw):
    base = {"statement": "s", "tests": [{"given": {}, "expect": {}}], "does_not_apply": "never"}
    base.update(kw)
    return FormulaEntry.model_validate(base)


HOOKE = E(formula="hooke_spring", kind="model", equations=["F = k*d"],
          variables={"F": "force", "k": "stiffness", "d": "length"}, assumes=["linear spring", "small deflection"],
          tests=[{"given": {"k": 2, "d": 3}, "expect": {"F": 6}}], cites=CITE)
EQ = E(formula="static_equilibrium", kind="model", equations=["F1 = T", "F2 = T"],
       variables={"F1": "force", "F2": "force", "T": "force"}, assumes=["tissue at rest"],
       tests=[{"given": {"T": 1}, "expect": {"F1": 1, "F2": 1}}], cites=CITE)


def test_given_entry_needs_citation():
    """A definition, model or bound has a citation to a source that states it (04-formulas, New formulas)."""
    e = E(formula="stress_def", kind="definition", equations=["s = F/A"], variables={"s": "stress", "F": "force", "A": "area"},
          tests=[{"given": {"F": 2, "A": 4}, "expect": {"s": 0.5}}])
    assert any("cites" in p for p in check_entry(e, Library()))
    e2 = e.model_copy(update={"cites": __import__("livinglit.models", fromlist=["Cites"]).Cites(**CITE)})
    assert check_entry(e2, Library()) == []


def test_model_states_assumptions():
    """A model states its assumptions (04-formulas, New formulas)."""
    e = HOOKE.model_copy(update={"assumes": []})
    assert any("assumptions" in p for p in check_entry(e, Library()))


def test_dimensions_checked():
    """Dimensions agree in every equation (04-formulas, New formulas)."""
    e = HOOKE.model_copy(update={"formula": "bad", "equations": ["F = k*d*d"]})
    assert any("dimensions" in p for p in check_entry(e, Library()))


def test_d_variables_same_dimension():
    """A library variable of dimension D, D2… means the same dimension as the other D variables (04-formulas, The formula library)."""
    e = E(formula="ratio_def", kind="definition", equations=["r = a/b"], variables={"r": "dimensionless", "a": "D", "b": "D"},
          tests=[{"given": {"a": 2, "b": 4}, "expect": {"r": 0.5}}], cites=CITE)
    assert check_entry(e, Library()) == []


def test_derived_proved_from_premises():
    """A derived formula is proved by code from accepted entries, and its holds_under is collected from the premises (04-formulas, The formula library)."""
    lib = Library({"hooke_spring": HOOKE, "static_equilibrium": EQ})
    tp = E(formula="two_post_force_balance", kind="derived", equations=["k*(d1 + d2) = 2*T"],
           variables={"k": "stiffness", "d1": "length", "d2": "length", "T": "force"},
           uses=[{"formula": "hooke_spring", "subs": {"F": "F1", "d": "d1"}},
                 {"formula": "hooke_spring", "subs": {"F": "F2", "d": "d2"}},
                 {"formula": "static_equilibrium"}],
           tests=[{"given": {"k": 1, "d1": 2, "d2": 2}, "expect": {"T": 2}}])
    assert check_entry(tp, lib) == []
    lib.entries["two_post_force_balance"] = tp
    assert lib.holds_under("two_post_force_balance") == ["linear spring", "small deflection", "tissue at rest"]
    wrong = tp.model_copy(update={"formula": "wrong", "equations": ["k*(d1 + d2) = T"],
                                  "tests": [FormulaEntry.model_validate({**tp.model_dump(), "formula": "x"}).tests[0].model_copy(update={"expect": {"T": 4}})]})
    assert any("does not follow" in p for p in check_entry(wrong, lib))


def test_derived_inequalities_not_accepted():
    """Derived inequalities are not proved yet, so they are not accepted as derived entries (04-formulas, New formulas)."""
    e = E(formula="x_le", kind="derived", equations=["a <= b"], variables={"a": "time", "b": "time"},
          uses=[{"formula": "hooke_spring"}], tests=[{"given": {"a": 1, "b": 2}}])
    assert any("inequalities" in p for p in check_entry(e, Library({"hooke_spring": HOOKE})))


def test_tests_must_pass_and_include_not_applying_case():
    """Tests pass, including one case where the formula does not apply (04-formulas, New formulas)."""
    e = HOOKE.model_copy(update={"formula": "h2", "does_not_apply": None,
                                 "tests": [HOOKE.tests[0].model_copy(update={"expect": {"F": 7}})]})
    probs = check_entry(e, Library())
    assert any("fails" in p for p in probs) and any("does not apply" in p for p in probs)


def test_names_in_stated_formulas():
    """pi, exp, log, sqrt are constants and functions; every other name, E included, is a variable (04-formulas, The formula library)."""
    x = parse_expr("3*E*I/L^3 + pi", [])
    assert {str(s) for s in x.free_symbols} == {"E", "I", "L"}


def test_groebner_and_substitution():
    """Equations are proved by Groebner reduction, else by substitution confirmed numerically (04-formulas, New formulas)."""
    a, b, c = sp.symbols("a b c", positive=True)
    assert follows([a - 2 * b, b - c], a - 2 * c)
    assert follows([a - sp.exp(b), b - c], a - sp.exp(c))
    assert not follows([a - 2 * b], a - 3 * b)


def test_evaluate_explicit_equations():
    """Checks apply library entries by evaluating their equations (04-formulas, Statistical formulas)."""
    assert evaluate(HOOKE, {"k": 2, "d": 5}, "F") == 10


def test_flag_text_names_kind_and_premises():
    """Every flag says how strong it is, by kind, and points back to its proof (04-formulas, The formula library)."""
    lib = Library({"hooke_spring": HOOKE})
    assert lib.flag_text("hooke_spring") == "inconsistent with model: hooke_spring (holds under: linear spring, small deflection)"
