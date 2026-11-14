from livinglit.survey import check_survey, tally, promote


CFG = {"fields": {"pacing": {"kind": "terms"}, "temperature": {"kind": "quantity"}}}


def _cond(text, quote, field="no field", varied=False):
    return {"text": text, "field": field, "varied": varied, "anchor": {"quote": quote, "where": "Methods"}}


def test_survey_gate_checks_quotes_and_tags(tmp_path):
    """A survey lists stated conditions, each quoted, its quote holding its words and found in the source, tagged with an existing field or 'no field' (03-vocabulary, Fields are designed from the corpus)."""
    (tmp_path / "main.txt").write_text("Tissues were paced at 1 Hz and stretched cyclically by 10 %.")
    ok = {"paper": "P", "conditions": [_cond("paced at 1 Hz", "paced at 1 Hz", "pacing"),
                                       _cond("cyclic stretch 10 %", "stretched cyclically by 10 %")]}
    assert check_survey(ok, tmp_path, CFG) == []
    bad = {"paper": "P", "conditions": [_cond("paced", "paced at 1 Hz", "stimulation"),
                                        _cond("37 C", "kept at 37 C")]}
    probs = check_survey(bad, tmp_path, CFG)
    assert any("stimulation" in p for p in probs) and any("not found" in p for p in probs)
    assert check_survey(ok, tmp_path, CFG, check_text=False) == []


def test_rule_makes_fields_of_varied_or_common_conditions():
    """A condition with no field becomes a field when 3 or more surveyed papers vary it between groups, or a third of them state it; any other goes to other_conditions (03-vocabulary, Fields are designed from the corpus)."""
    papers = [chr(65 + i) for i in range(9)]  # 9 papers: a third is 3
    surveys = {p: {"paper": p, "conditions": [_cond("x", "q")]} for p in papers}
    names = {p: {0: "sterilization"} for p in papers[:2]}
    names.update({p: {0: "seeding density"} for p in papers[2:5]})
    names.update({p: {0: "oxygen level"} for p in papers[5:9]})
    for p in papers[5:8]:
        surveys[p]["conditions"][0]["varied"] = True
    rows = {r["condition"]: r for r in tally(surveys, names)}
    assert rows["oxygen level"]["varied_in"] == 3 and rows["oxygen level"]["decision"] == "field"
    assert rows["seeding density"]["papers"] == 3 and rows["seeding density"]["decision"] == "field"
    assert rows["sterilization"]["decision"] == "other_conditions"


def test_untagged_condition_without_a_name_fails_the_tally():
    """Every untagged condition is named by the merge job before code counts; a missing name is an error, never a guess (03-vocabulary, Fields are designed from the corpus)."""
    import pytest
    with pytest.raises(ValueError, match="no name"):
        tally({"A": {"paper": "A", "conditions": [_cond("stretch", "q")]}}, {"A": {}})


def test_promotion_at_checkpoints_needs_five_percent_and_three_papers():
    """At a checkpoint a condition in other_conditions becomes a field when stated in at least 5 % of the papers read and at least 3 (03-vocabulary, Fields are designed from the corpus)."""
    assert promote({"hypoxia": 3, "spin": 2}, papers_read=40) == ["hypoxia"]
    assert promote({"hypoxia": 14, "spin": 15}, papers_read=300) == ["spin"]


def test_merge_input_is_only_the_untagged_conditions():
    """Code hands the merge job only the conditions tagged 'no field', by paper and index (03-vocabulary, Fields are designed from the corpus; 07-building, No needless compute)."""
    from livinglit.survey import untagged
    s = {"A": {"paper": "A", "conditions": [_cond("paced", "q", "pacing"), _cond("stretch", "q")]}}
    assert untagged(s) == {"A": {1: "stretch"}}
