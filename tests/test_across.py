import copy

import pytest

import yaml

from livinglit.across import comparisons, item_direction, relax, key_check
from livinglit.audit import audit_paper, write_audit
from livinglit.checks import gather
from livinglit.formulas import load_library
from livinglit.models import Record
from livinglit.vocab import Vocabulary, FieldDecl, apply_version
from tests.helpers import record

FIELDS = {f: FieldDecl(f, "terms") for f in ["platform", "pacing"]}
FIELDS.update({f: FieldDecl(f, "quantity") for f in ["temperature", "day_of_measurement", "culture_calcium_mM"]})
FIELDS["measure"] = FieldDecl("measure", "measure")


def _vocab(key=None):
    v = Vocabulary(FIELDS)
    ev = [{"event": "add_term", "field": "platform", "id": "platform:3d", "label": "3D", "definition": "d"},
          {"event": "add_term", "field": "platform", "id": "platform:micropillar", "label": "micropillar tissue",
           "parent": "platform:3d", "definition": "d", "scope": "s"},
          {"event": "add_term", "field": "platform", "id": "platform:strip", "label": "strip", "parent": "platform:3d",
           "definition": "d", "scope": "s"},
          {"event": "add_term", "field": "pacing", "id": "pacing:ramp", "label": "ramp pacing", "definition": "d", "scope": "s"},
          {"event": "add_term", "field": "measure", "id": "measure:force", "label": "twitch force", "definition": "d",
           "dimension": "force"}]
    if key:
        ev.append({"event": "standing_key", "measure": "measure:force", **key})
    apply_version(v, {"version": 1, "paper": "P", "events": ev})
    return v


def _write(tmp_path, pid, platform="micropillar tissue", p="P < 0.01", hi="2.0 ± 0.5"):
    r = record()
    r["id"] = pid
    r["default_context"]["platform"] = platform
    r["evidence"]["E1"]["stats"]["p"] = p
    r["evidence"]["E1"]["values"]["force_HC_RP"]["printed"] = hi
    d = tmp_path / pid
    d.mkdir()
    (d / "record.yaml").write_text(yaml.safe_dump(r))
    return d


def test_direction_computed_from_values_and_p():
    """Direction is up or down from the groups' values when the printed P is significant, none when not (05-across-sources, Comparisons)."""
    rec = Record.model_validate(record())
    assert item_direction(rec.evidence["E1"], gather(rec, "E1")).direction == "up"
    r = record()
    r["evidence"]["E1"]["stats"]["p"] = "n.s."
    rec = Record.model_validate(r)
    assert item_direction(rec.evidence["E1"], gather(rec, "E1")).direction == "none"


def test_stated_direction_only_without_values():
    """stated_direction is used only when no values exist, and is labelled stated (05-across-sources, Comparisons; 08 decision 14)."""
    r = record()
    r["evidence"]["E1"]["values"] = {}
    r["evidence"]["E1"]["stated_direction"] = {"direction": "up", "anchor": {"quote": "q", "where": "w"}}
    rec = Record.model_validate(r)
    d = item_direction(rec.evidence["E1"], gather(rec, "E1"))
    assert (d.direction, d.origin) == ("up", "stated")


def test_direction_comparison_across_papers(tmp_path):
    """Two items are direction-comparable when their computed contrasts vary the same field with matching group terms (05-across-sources, Comparisons)."""
    key = {"value": {"must_match": ["platform"]}, "direction": {"must_match": ["contrast", "platform@1"]}}
    v, lib = _vocab(key), load_library()
    _write(tmp_path, "P1")
    _write(tmp_path, "P2", platform="strip")
    us = []
    for pid in ("P1", "P2"):
        us += audit_paper(pid, v, lib, tmp_path, tmp_path).across_units
    rows = comparisons(v, us, lambda mt: v.keys["measure:force"].__dict__ | {
        "value": v.keys["measure:force"].value.__dict__, "direction": v.keys["measure:force"].direction.__dict__})
    d = [r for r in rows if r["part"] == "direction"][0]
    assert d["verdict"] == "same direction" and d["direction_origin"] == "computed"
    val = [r for r in rows if r["part"] == "value" and r["verdict"] == "not comparable"]
    assert val and any("platform" in b for b in val[0]["blocking"])
    assert val[0]["relaxation"] == "comparable if platform@1"


def test_audit_writes_values_csv(tmp_path):
    """Code writes records/<paper>/values.csv, one row per value with origin, and audit.yaml (06-releases, Values as a dataset)."""
    v, lib = _vocab(), load_library()
    _write(tmp_path, "P1")
    pa = audit_paper("P1", v, lib, tmp_path, tmp_path)
    a = write_audit(pa, v, lib, tmp_path)
    assert a["items"]["E1"]["status"] == "consistent"
    text = (tmp_path / "P1" / "values.csv").read_text()
    assert "stated" in text and "E1" in text


@pytest.mark.ontologies
def test_release_tables_and_explorer(tmp_path):
    """A release writes the documented tables, findings and strata among them, and the explorer page, with one page per unit (06-releases, What a release holds; Findings and strata)."""
    from livinglit.release import build
    recs = tmp_path / "records"
    recs.mkdir()
    _write(recs, "P1")
    _write(recs, "P2", platform="strip")
    build("t", records_dir=recs, out_root=tmp_path / "rel", papers_dir=tmp_path)
    out = tmp_path / "rel" / "t"
    for f in ["papers.csv", "units.csv", "groups.csv", "items.csv", "values.csv", "mappings.csv", "comparisons.csv", "strata.csv", "findings.csv",
              "completeness.csv", "source_data_requests.csv", "missing_supplements.csv", "coverage.csv", "explorer.html"]:
        assert (out / f).exists(), f
    assert "P1" in (out / "explorer.html").read_text()


def test_normalisation_qualifier_does_not_block_two_absolute_values():
    """normalised_to applies only to relative values: two values expressed as absolute match on it, while a relative value without one is not stated (05-across-sources, Standing keys)."""
    from livinglit.across import field_result, Unit
    v = Vocabulary({"measure": FieldDecl("measure", "measure")})
    mk = lambda q: Unit(paper="p", unit="u", item="i", group="g", measure_terms=("measure:force",), measure_qualifiers=q, context={})
    assert field_result(v, "measure.normalised_to", mk({"expressed_as": "absolute"}), mk({"expressed_as": "absolute"}), "value")[0]
    assert not field_result(v, "measure.normalised_to", mk({"expressed_as": "fold"}), mk({"expressed_as": "absolute"}), "value")[0]


def test_value_comparison_uses_spread_of_points_and_needs_one():
    """Values agree or differ within their spreads, an SD from the stated spread (SEM converted with n) or from the points; with no spread on a side the verdict is not available, never differ (05-across-sources, Comparisons)."""
    from livinglit.across import compare_values, group_sd, Unit
    from livinglit.checks import GroupEvidence
    e = GroupEvidence(data_points=[28.0, 31.0, 34.0], data_unit="bpm")
    assert abs(group_sd(e, "data") - 3.0) < 1e-9
    s = GroupEvidence(mean="30.36", spread="2", spread_kind="SEM", n=[9])
    assert abs(group_sd(s, "stated") - 6.0) < 1e-9
    assert group_sd(GroupEvidence(mean="30", spread="2", spread_kind="SEM"), "stated") is None
    mk = lambda m, sd: Unit(paper="p", unit="u", item="i", group="g", measure_terms=(), measure_qualifiers={}, context={},
                            mean=m, spread=sd, value_unit="bpm")
    assert compare_values(mk(30.98, 3.0), mk(30.36, 9.2)) == "agree"
    assert compare_values(mk(30.98, None), mk(30.36, 9.2)) == "not available (no spread)"
    assert compare_values(mk(60.0, 3.0), mk(30.0, 4.0)) == "differ"


def test_unknown_key_field_gives_conditional_verdict():
    """Open world: a must-match field unstated on a side is unknown, not a conflict; the verdict is computed and names its assumptions, while a field known to differ blocks (05-across-sources, Comparisons)."""
    from livinglit.across import Unit, comparisons
    from livinglit.matching import Side
    v = _vocab({"value": {"must_match": ["platform", "temperature"]}, "direction": {"must_match": ["contrast"]}})
    pm = Side(terms=("platform:micropillar",))
    mk = lambda paper, ctx: Unit(paper=paper, unit="F1", item="E1", group="g", measure_terms=("measure:force",),
                                 measure_qualifiers={}, context=ctx, mean=2.0, spread=0.5, value_unit="mN")
    rows = comparisons(v, [mk("A", {"platform": pm, "temperature": Side(state="not stated")}),
                           mk("B", {"platform": pm, "temperature": Side(state="not stated")})], lambda mt: v.keys[mt[0]].__dict__ | {
        "value": v.keys[mt[0]].value.__dict__, "direction": v.keys[mt[0]].direction.__dict__})
    assert rows[0]["verdict"] == "agree" and rows[0]["assumes"] == ["temperature"]
    rows = comparisons(v, [mk("A", {"platform": pm, "temperature": Side(state="not stated")}),
                           mk("B", {"platform": Side(terms=("platform:strip",)), "temperature": Side(state="not stated")})],
                       lambda mt: {"value": v.keys[mt[0]].value.__dict__, "direction": v.keys[mt[0]].direction.__dict__})
    assert rows[0]["verdict"] == "not comparable" and rows[0]["assumes"] == []


def test_strata_group_known_matches_and_link_unknowns_conditionally():
    """Items whose must-match fields carry the same known terms form one stratum; an item unknown on a key field forms its own and is linked to each stratum it could join, naming what that assumes; a known difference makes no link (05-across-sources, Strata, not pairs)."""
    from livinglit.across import Unit, strata
    from livinglit.matching import Side
    v = _vocab({"value": {"must_match": ["platform"]}, "direction": {"must_match": ["contrast"]}})
    keyf = lambda mt: {"value": v.keys[mt[0]].value.__dict__, "direction": v.keys[mt[0]].direction.__dict__}
    mk = lambda paper, side, m: Unit(paper=paper, unit="F1", item="E1", group="g", measure_terms=("measure:force",),
                                     measure_qualifiers={}, context={"platform": side}, mean=m, spread=0.5, value_unit="mN")
    pm, ps, un = Side(terms=("platform:micropillar",)), Side(terms=("platform:strip",)), Side(state="not stated")
    rows = strata(v, [mk("A", pm, 2.0), mk("B", pm, 2.1), mk("C", un, 2.0), mk("D", ps, 9.0)], keyf)
    by_items = {tuple(sorted(r["items"])): r for r in rows}
    ab = by_items[("A/E1/g", "B/E1/g")]
    assert ab["papers"] == 2 and ab["verdicts"] == {"agree": 1}
    c = by_items[("C/E1/g",)]
    assert c["unknowns"] == {"C/E1/g": ["platform"]}
    links = {l["stratum"]: l["assumes"] for l in c["links"]}
    assert links == {ab["stratum"]: ["platform"], by_items[("D/E1/g",)]["stratum"]: ["platform"]}
    assert not any(l["stratum"] == by_items[("D/E1/g",)]["stratum"] for l in ab["links"])


def test_a_value_found_wrong_by_its_derivation_is_compared_as_rebuilt():
    """When a group's printed value comes from a wrong derivation (the paper's formula contradicts the library, or printed and rebuilt values differ by a constant factor), comparisons use the rebuilt value (labelled), scaling the spread only for a constant factor; numbers that are off for another reason (a ratio of means against a mean of ratios) keep the printed value (04-formulas, Wrong derivations; 05-across-sources, Comparisons)."""
    from livinglit.across import rebuilt_side
    from livinglit.chains import ChainResult
    const = ChainResult("d1", "inconsistent", "inconsistent", rebuilt=6.0, rebuilt_unit="mN",
                        flags=["constant factor 0.5 between printed and rebuilt value: conclusion unaffected"])
    assert rebuilt_side(12.0, 2.0, "mN", const) == (6.0, 1.0, "mN", True)
    si = ChainResult("d1", "inconsistent", "inconsistent", rebuilt=0.006, rebuilt_unit="N",
                     flags=["constant factor 0.5 between printed and rebuilt value: conclusion unaffected"])
    m, sp, u, used = rebuilt_side(12.0, 2.0, "mN", si)
    assert used and u == "mN" and abs(m - 6.0) < 1e-9 and abs(sp - 1.0) < 1e-9
    wrong_formula = ChainResult("d1", "inconsistent", "inconsistent", rebuilt=7.0, rebuilt_unit="mN")
    assert rebuilt_side(12.0, 2.0, "mN", wrong_formula) == (7.0, None, "mN", True)
    aggregation = ChainResult("d1", "inconsistent", "consistent", rebuilt=7.0, rebuilt_unit="mN",
                              notes=["mean of per-sample: per-sample inputs with equal counts are not available"])
    assert rebuilt_side(12.0, 2.0, "mN", aggregation) == (12.0, 2.0, "mN", False)
    ok = ChainResult("d1", "consistent", "consistent", rebuilt=12.0, rebuilt_unit="mN")
    assert rebuilt_side(12.0, 2.0, "mN", ok) == (12.0, 2.0, "mN", False)
    assert rebuilt_side(12.0, 2.0, "mN", None) == (12.0, 2.0, "mN", False)


def test_comparison_rows_name_the_sides_compared_as_rebuilt():
    """A comparison row lists which sides were compared on a rebuilt value, so a verdict on a rebuilt value is never read as one on the printed value (05-across-sources, Comparisons)."""
    from livinglit.across import Unit
    v = Vocabulary({"measure": FieldDecl("measure", "measure")})
    mk = lambda p, m, rb: Unit(paper=p, unit="u", item="i", group="g", measure_terms=("measure:force",),
                               measure_qualifiers={}, context={}, mean=m, spread=1.0, value_unit="mN", rebuilt=rb)
    key = lambda mt: {"value": {"must_match": []}, "direction": {"must_match": []}}
    rows = comparisons(v, [mk("A", 6.0, True), mk("B", 6.5, False)], key)
    assert rows[0]["verdict"] == "agree" and rows[0]["rebuilt"] == ["A/i/g"]
    rows = comparisons(v, [mk("A", 6.0, False), mk("B", 6.5, False)], key)
    assert rows[0]["rebuilt"] == []
