from livinglit.text import normalize, quote_variants, quote_in_texts


def test_normalize_keeps_meaningful_signs():
    """Normalization keeps + − ± < > = / % . × and lower-cases, joins line-break hyphens (02-audit, Anchors and origins)."""
    assert normalize("P < 0.05, n = 6") == "p<0.05n=6"
    assert normalize("12 ± 3 mN/mm²") == "12±3mn/mm2"
    assert normalize("contrac-\ntile") == "contractile"
    assert normalize("50%") == "50%"
    assert normalize("2 × 10") == "2×10"


def test_en_dash_dropped_like_hyphen():
    """En dashes are dropped like hyphens, because PDFs extract 'α-actinin' as '–actinin' (02-audit, Anchors and origins)."""
    assert normalize("5–36") == normalize("5-36") == "536"
    assert quote_in_texts("α-actinin staining", [normalize("–actinin staining")])


def test_hyphen_next_to_slash_is_minus():
    """A hyphen next to '/' is a minus ('+/-', '-/-') (02-audit, Anchors and origins)."""
    assert normalize("MYBPC3-/-") == normalize("MYBPC3−/−")
    assert normalize("+/-") == "+/−"


def test_greek_variants():
    """Each quote is tried with Greek and µ dropped, as Latin letters (α→a, β→b, µ→m), and µ→u (02-audit, Quote matching)."""
    v = quote_variants("β-MHC 10 µM")
    assert normalize("-MHC 10 M") in v
    assert normalize("b-MHC 10 mM") in v
    assert normalize("b-MHC 10 uM") in v


def test_quote_found_in_either_extractor():
    """A quote is found if any variant is in either extractor's text (02-audit, Quote matching)."""
    texts = [normalize("nothing here"), normalize("force was 10 uN in EHTs")]
    assert quote_in_texts("force was 10 µN in EHTs", texts)
    assert not quote_in_texts("force was 11 µN", texts)


def test_minus_signs_unified():
    """True minus signs are kept as signs, in one spelling (02-audit, Anchors and origins)."""
    assert normalize("−0.5") == normalize("‒0.5")


def test_times_sign_extracted_as_three():
    """Some fonts extract × as '3' and lose superscripts ('7 × 10^5' as '7 3 105'); the quote is tried that way too (02-audit, Quote matching)."""
    assert quote_in_texts("7 × 10^5 MOI transduction", [normalize("for 7 3 105 MOI transduction")])
