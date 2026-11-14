"""The first look: a cheap page look that decides `no_points` before a figure job (07-building, No needless compute)."""
import pytest
import yaml

from livinglit.first_look import figure_refs, label, legend_pages, decide, look_argv, mark_no_points
from livinglit.jobs import add_paper
from tests.test_add import Fake


def test_figure_refs_reads_the_unit_where():
    """A unit's `where` names its figures by kind, number and panels; text after the panels is not a panel (07-building, No needless compute)."""
    assert figure_refs("Fig. 1D") == [("F", "1", ["D"])]
    assert figure_refs("Fig. 1g–h") == [("F", "1", ["g", "h"])]
    assert figure_refs("Fig. 1f, g") == [("F", "1", ["f", "g"])]
    assert figure_refs("Fig. S2A, left panel") == [("S", "2", ["A"])]
    assert figure_refs("Supplementary Fig. 2C") == [("S", "2", ["C"])]
    assert figure_refs("fig. S3A–C") == [("S", "3", ["A", "C"])]
    assert figure_refs("Supplement Figure 3 (Figure III)") == [("S", "3", [])]
    assert figure_refs("Suppl. Fig. 1a,b") == [("S", "1", ["a", "b"])]
    assert figure_refs("Extended Data Fig. 4b") == [("ED", "4", ["b"])]
    assert figure_refs("Fig. 1C; Section 3.1") == [("F", "1", ["C"])]
    assert figure_refs("Fig. 7F–7I") == [("F", "7", ["F", "I"])]
    assert figure_refs("fig. S7C–S7D") == [("S", "7", ["C", "D"])]
    assert figure_refs("Fig. 3B and C") == [("F", "3", ["B", "C"])]
    assert figure_refs("Fig. 2") == [("F", "2", [])]
    assert len(figure_refs("Fig. 1C and Fig. S1A")) == 2
    assert figure_refs("Table 1") == []


def test_label_names_figure_and_panels():
    """The look is asked about the unit's figure and panels by name (07-building, No needless compute)."""
    assert label("F", "4", ["D"]) == "Figure 4, panel D"
    assert label("S", "3", ["A", "C"]) == "Supplementary Figure 3, panels A to C"
    assert label("F", "1", ["f", "g"]) == "Figure 1, panels f to g"
    assert label("ED", "2", []) == "Extended Data Figure 2, all panels"


def test_legend_pages_are_the_legend_page_and_the_one_before():
    """Code finds the page where a figure's legend starts and sends it with the page before, in each file that has it; a main figure is not looked for in supplements, which may number their own figures 1, 2, ... (07-building, No needless compute)."""
    main = ["Title page", "Results text. As shown in Figure 2A, force rose.", "[figure]",
            "Figure 2. Force of tissues. (A) Force over time. (B) Force at day 7.\nMore text."]
    assert legend_pages({"main.pdf": main}, ("F", "2")) == [("main.pdf", 3), ("main.pdf", 4)]
    assert legend_pages({"main.pdf": main}, ("F", "3")) == []
    supp = ["Supplementary Material", "Figure 2. A supplementary figure numbered 2. (A) x. (B) y."]
    assert legend_pages({"main.pdf": main, "mmc1.pdf": supp}, ("F", "2")) == [("main.pdf", 3), ("main.pdf", 4)]
    manuscript = ["Author manuscript", "Figure 2. Force of tissues. (A) Force. (B) Force."]
    assert legend_pages({"main.pdf": main, "nihms1.pdf": manuscript}, ("F", "2")) == [
        ("main.pdf", 3), ("main.pdf", 4), ("nihms1.pdf", 1), ("nihms1.pdf", 2)]
    assert legend_pages({f"f{i}.pdf": manuscript for i in range(4)}, ("F", "2")) == []
    first = ["Figure S1. Legend on the first page. (A) a. (B) b."]
    assert legend_pages({"s.pdf": first}, ("S", "1")) == [("s.pdf", 1)]
    batched = ["Supplementary Information", "Figure S1\n[plot]", "Figure S2\n[plot]",
               "Figure S1. Force. (A) a. (B) b.\nFigure S2. Rate. (A) a. (B) b."]
    assert legend_pages({"mmc1.pdf": batched}, ("S", "2")) == [("mmc1.pdf", 3), ("mmc1.pdf", 4)]
    assert legend_pages({"mmc1.pdf": batched}, ("S", "1")) == [("mmc1.pdf", 2), ("mmc1.pdf", 3), ("mmc1.pdf", 4)]


def test_skip_only_on_no_with_a_page_named():
    """A figure job is skipped only when the look answers no and names one of the pages it was shown; yes, unsure, no page, or a bad answer runs the job (07-building, No needless compute)."""
    assert decide({"points": "no", "page": 2, "why": "bars with SD only"}, 2) == "bars with SD only"
    assert decide({"points": "yes", "page": 2, "why": "dots"}, 2) is None
    assert decide({"points": "unsure", "page": 1, "why": "?"}, 2) is None
    assert decide({"points": "no", "page": 0, "why": "not on these pages"}, 2) is None
    assert decide({"points": "no", "page": 3, "why": "bars"}, 2) is None
    assert decide({"points": "no", "page": "2", "why": ""}, 2) is None
    assert decide("not json", 2) is None


def test_the_look_is_a_small_model_that_only_reads():
    """The look runs the small model named in the repo's agent config, with the Read tool only and a few turns (07-building, No needless compute)."""
    from livinglit import agent
    if not agent.path().exists():
        pytest.skip("no agent.yaml")
    a = look_argv("prompt")
    assert a[a.index("--model") + 1] == agent.load()["look"]["model"]
    assert a[a.index("--allowedTools") + 1] == "Read"
    for t in ("Write", "Edit", "Bash"):
        assert t in a[a.index("--disallowedTools"):]


def test_mark_no_points_keeps_the_figures_file(tmp_path):
    """A look's no_points is written to figures.yaml marked 'first look', keeping what is there (07-building, No needless compute)."""
    f = tmp_path / "figures.yaml"
    f.write_text(yaml.safe_dump({"figures": {}, "no_points": {"F1": "bars only"}}))
    mark_no_points(tmp_path, "F2", "first look (small model): bars with SD (main.pdf p. 4)")
    d = yaml.safe_load(f.read_text())
    assert d["no_points"] == {"F1": "bars only", "F2": "first look (small model): bars with SD (main.pdf p. 4)"}
    mark_no_points(tmp_path / "new", "F3", "first look (small model): x")
    assert yaml.safe_load((tmp_path / "new" / "figures.yaml").read_text())["no_points"]["F3"].startswith("first look")


def test_add_skips_a_figure_job_the_look_rules_out():
    """Before each figure job a look runs; on a skip the unit is marked no_points and its job does not run, otherwise the job runs as before (07-building, No needless compute)."""
    f = Fake(figures=("F1", "F2", "F3"))
    marked = {}
    answers = {"F1": {"skip": True, "reason": "first look (small model): bars", "cost_usd": 0.01},
               "F2": {"skip": False, "reason": "yes: dots", "cost_usd": 0.01},
               "F3": {"skip": False, "reason": "no look: two figures", "cost_usd": 0.0}}

    def look(paper, unit):
        return answers[unit]

    def mark(paper, unit, reason):
        marked[unit] = reason
        f.figs.remove(unit)

    r = add_paper("P", run=f.run, gate=f.gate, needed=f.needed, look=look, mark=mark)
    assert f.calls == ["record", "figures_F2", "figures_F3", "vocabulary", "formula"]
    assert marked == {"F1": "first look (small model): bars"}
    assert r["status"] == "added" and r["cost_usd"] == 5.02 and r["looked_off"] == ["F1"]


@pytest.mark.papers
def test_recorded_pages_are_among_the_pages_sent():
    """For recorded figure units naming one figure, code sends the page the figure job read in nearly every case (07-building, No needless compute)."""
    from livinglit import PAPERS_DIR, RECORDS_DIR
    from livinglit.first_look import _page_texts
    sent = right = 0
    for fy in sorted(RECORDS_DIR.glob("*/figures.yaml")):
        rec = yaml.safe_load((fy.parent / "record.yaml").read_text())
        texts, seen = _page_texts(PAPERS_DIR / fy.parent.name), set()
        for v in (yaml.safe_load(fy.read_text()).get("figures") or {}).values():
            refs = figure_refs(rec["units"][v["unit"]]["where"])
            if v["unit"] in seen or len(refs) != 1:
                continue
            seen.add(v["unit"])
            pages = legend_pages(texts, refs[0][:2])
            if pages:
                sent += 1
                right += (v["file"], v["page"]) in pages
    assert sent >= 200 and right / sent >= 0.97
