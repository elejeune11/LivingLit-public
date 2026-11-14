import pytest

from livinglit.numbers import (interval, judge_value, judge_p, parse_p, parse_unit, unit_from_axis_label,
                               split_pm, same_quantity_units, parse_number, test_kind as kind_of_test)


def test_printed_precision_interval():
    """A printed value stands for everything that rounds to it: t = 2.3 allows 2.25–2.35 (02-audit, Checks within a source)."""
    assert interval("2.3") == pytest.approx((2.25, 2.35))
    assert judge_value("2.3", 2.34) == "consistent"
    assert judge_value("2.3", 2.38) == "close"
    assert judge_value("2.3", 2.6) == "inconsistent"


def test_machine_precision_relative_tolerance():
    """A value stored at machine precision in released data is compared with a relative tolerance of 1e-6 (02-audit, Checks within a source)."""
    assert judge_value("0.123456789012", 0.1234567890) == "consistent"
    assert judge_value("0.123456789012", 0.1235) == "inconsistent"


@pytest.mark.parametrize("printed,expected", [
    ("P < 0.05", ("<", 0.05)), ("*p<0.05", ("<", 0.05)), ("****p < 0.001", ("<", 0.001)),
    ("P = .01", ("=", 0.01)), ("p=0.0006", ("=", 0.0006)), ("P = 3.2 × 10−4", ("=", 3.2e-4)),
    ("P < 0.001 (figure label)", ("<", 0.001)), ("p > 0.05", (">", 0.05)),
])
def test_printed_p_first_operator(printed, expected):
    """Printed P is read from its first 'P <op> value'; '.01' is 0.01; '× 10−4' is an exponent (02-audit, Values)."""
    p = parse_p(printed)
    assert (p.op, p.value) == pytest.approx(expected)


@pytest.mark.parametrize("printed", ["n.s.", "NS", "ns", "not significant"])
def test_ns_is_p_at_least_005(printed):
    """'n.s.' is P ≥ 0.05 (02-audit, Values)."""
    p = parse_p(printed)
    assert p.op == ">=" and p.value == 0.05 and p.significant is False


@pytest.mark.parametrize("printed", ["*", "***", "not stated", "significant (P not printed)", "no pair marked"])
def test_asterisks_without_threshold_are_not_a_p(printed):
    """Asterisks without a stated threshold are not a P (02-audit, Values)."""
    assert parse_p(printed) is None


def test_judge_p_against_bound():
    """A recomputed P is judged against the printed operator and bound (02-audit, Checks within a source)."""
    assert judge_p("P < 0.05", 0.01) == "consistent"
    assert judge_p("P < 0.05", 0.2) == "inconsistent"
    assert judge_p("P = 0.04", 0.0449) == "consistent"
    assert judge_p("n.s.", 0.3) == "consistent"
    assert judge_p("n.s.", 0.001) == "inconsistent"


def test_range_is_two_values():
    """A range ('5–36') is two values, never a mean (02-audit, Values)."""
    with pytest.raises(ValueError):
        split_pm("5–36")


def test_decrease_keeps_sign():
    """Decreases keep the sign as printed (02-audit, Values)."""
    assert parse_number("−87%")[0] == "-87"


def test_units_through_axis_labels():
    """Units are compared through axis labels ('Force [mN]' is mN) and common spellings (msec = ms) (02-audit, Checks within a source)."""
    assert unit_from_axis_label("Force [mN]").name == "mN"
    assert unit_from_axis_label("Time to peak (msec)").name == "ms"
    assert parse_unit("msec").name == "ms"
    assert unit_from_axis_label("Beat rate").name is None


def test_percent_of_baseline_differs_from_percent_change():
    """'% of baseline' and '% change' are different quantities (02-audit, Checks within a source)."""
    assert not same_quantity_units("% of baseline", "% change")
    assert same_quantity_units("mN", "µN")
    assert not same_quantity_units("mN", "ms")


@pytest.mark.parametrize("printed,family,posthoc", [
    ("Two-tailed, unpaired Student's t test assuming unequal variances", "welch_t", None),
    ("Welch's t-test", "welch_t", None),
    ("unpaired two-sided t-test", "t_unpaired", None),
    ("Student's t-test", "student_t", None),
    ("paired t-test", "paired_t", None),
    ("t test (column 'T.Test')", "t_unspecified", None),
    ("one-way ANOVA", "one_way_anova", None),
    ("one-way ANOVA with Dunnett's post-test vs. BL", "one_way_anova", "dunnett"),
    ("two-way ANOVA with post hoc Holm-Sidak test", "two_way_anova", "holm-sidak"),
    ("ANOVA with Tukey's HSD test", "anova_unspecified", "tukey"),
    ("one-way ANOVA plus Bonferroni post test", "one_way_anova", "bonferroni"),
    ("Kruskal-Wallis test; pairwise Mann-Whitney test with Bonferroni correction", "kruskal_wallis", "bonferroni"),
    ("Mann-Whitney U test on ranks", "mann_whitney", None),
    ("Friedman's test; Dunn's multiple comparisons test", "friedman", "dunn"),
    ("Pearson correlation", "correlation", None),
    ("not stated", "not stated", None),
])
def test_test_kinds_from_printed_strings(printed, family, posthoc):
    """Test kinds are parsed from printed legends: 'Student's t test assuming unequal variances' is Welch's; post-hoc tests are named (02-audit, Checks within a source)."""
    k = kind_of_test(printed)
    assert (k.family, k.posthoc) == (family, posthoc)


def test_approximate_value_judged_loosely():
    """A value printed with '~' is approximate: within 10 % (or one last digit) it is consistent, never exact (02-audit, Values)."""
    assert judge_value("~50%", 47) == "consistent"
    assert judge_value("~50%", 30) == "inconsistent"


def test_approximate_words_and_chains():
    """A value printed "~", "≈", "about", "approximately" or "roughly" is approximate, in checks and along a derivation (02-audit, Values)."""
    from livinglit.numbers import parse_number, judge_value
    assert parse_number("about 20")[1] and parse_number("approximately 50%")[1] and not parse_number("20")[1]
    assert judge_value("about 20", 21.5) == "consistent"
    from livinglit.chains import judge_rebuilt
    assert judge_rebuilt("≈20", 21.5, None, None) == "consistent"
