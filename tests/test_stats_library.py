from livinglit.stats_library import entries
from livinglit.formulas import Library, check_entry, load_library, evaluate

REQUIRED = {"mean_def", "sd_def", "sem_def", "ci95_halfwidth", "cv_def", "t_two_sample_pooled", "t_two_sample_welch",
            "one_way_anova_f", "t_distribution", "f_distribution", "chi2_distribution", "normal_distribution",
            "constant_scaling_t", "constant_shift_t", "ratio_of_means_constant_denominator", "normalized_to_own_control"}


def test_statistical_entries_pass_their_checks():
    """The shared statistical entries are written first and each passes the formula checks; derived ones are proved (04-formulas, Statistical formulas)."""
    lib = Library()
    for e in entries():
        assert check_entry(e, lib) == [], e.formula
        lib.entries[e.formula] = e
    assert REQUIRED <= set(lib.entries)


def test_shared_library_committed_and_loaded():
    """The statistical entries live in fields/_shared/formulas, which every field's library extends (04-formulas, Statistical formulas)."""
    lib = load_library("hipsc_cm")
    assert REQUIRED <= set(lib.entries)
    assert lib.holds_under("constant_scaling_t") == []
    assert lib.get("t_distribution").kind == "model"


def test_welch_evaluates():
    """Statistical checks are applications of the entries (04-formulas, Statistical formulas)."""
    lib = load_library("hipsc_cm")
    t = evaluate(lib.get("t_two_sample_welch"), {"m1": 2.0, "m2": 1.0, "s1": 0.5, "s2": 0.4, "n1": 6, "n2": 6}, "t")
    assert abs(t - 3.82546) < 1e-4


POSTHOC = {"studentized_range_distribution", "tukey_kramer_q", "bonferroni_adjust", "sidak_adjust", "holm_step",
           "holm_sidak_step", "two_way_anova_f"}


def test_posthoc_and_two_way_entries_are_given_models():
    """Tukey HSD (studentized range), Holm, Šidák, Bonferroni and the two-way ANOVA F are given entries of the shared library (04-formulas, Statistical formulas)."""
    lib = load_library("hipsc_cm")
    assert POSTHOC <= set(lib.entries)
    assert lib.get("studentized_range_distribution").kind == "model"


def test_studentized_range_evaluates():
    """The studentized range P is evaluated numerically as a named function (04-formulas, Statistical formulas)."""
    lib = load_library("hipsc_cm")
    p = evaluate(lib.get("studentized_range_distribution"), {"q": 3.5, "k": 3, "df": 20}, "p")
    assert abs(p - 0.05589) < 1e-4
    assert abs(evaluate(lib.get("sidak_adjust"), {"p": 0.01, "m": 3}, "ps") - 0.029701) < 1e-6
