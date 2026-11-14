import copy

from livinglit.models import Record
from tests.helpers import record


def test_ids_are_never_silently_removed():
    """A re-read record keeps every unit, group, item and claim id of the committed record, unless it lists the id under removed with a reason (07-building, Reviewing agent reports)."""
    from livinglit.review import removed_ids
    before = record()
    after = copy.deepcopy(before)
    del after["units"]["F1"]["groups"]["LC_RP"]
    del after["evidence"]["E1"]
    assert removed_ids(before, after) == ["evidence.E1", "units.F1.groups.LC_RP"]
    after["removed"] = [{"id": "evidence.E1", "why": "a duplicate of E2"}]
    assert removed_ids(before, after) == ["units.F1.groups.LC_RP"]
    Record.model_validate({**record(), "removed": [{"id": "evidence.E1", "why": "w"}]})


def test_one_wording_in_two_fields_is_listed_for_review():
    """The same stated words in two different fields of one group's context are listed for review, since no field is filled from another field's text (07-building, Reviewing agent reports; CONTRIBUTING, Fixed rules)."""
    from livinglit.review import copied_wording
    r = record()
    r["units"]["F1"]["groups"]["HC_NP"]["context"]["treatment"] = "ramp pacing"
    r["units"]["F1"]["groups"]["HC_RP"]["context"]["treatment"] = "ramp pacing"
    out = copied_wording(Record.model_validate(r))
    assert out == ["units.F1.groups.HC_RP: 'ramp pacing' in pacing and treatment"]


def test_figures_needed_only_where_no_printed_or_released_values():
    """A figure job is made only for a figure unit with an item group whose values no printed text, table or data give (07-building, No needless compute)."""
    from livinglit.jobs import figures_needed
    r = record()
    r["units"]["F2"] = {"where": "Fig. 2c", "title": "Force", "groups": {"a": {"label": "A"}, "b": {"label": "B"}}}
    r["units"]["T1"] = {"where": "Table 1", "title": "Tab", "groups": {"a": {"label": "A"}}}
    r["evidence"]["E2"] = {"unit": "F2", "measure": "twitch force", "finding": "f", "compares": ["a", "b"],
                           "values": {"va": {"printed": "1.0", "unit": "mN", "group": "a"}},
                           "stats": {"test": "unpaired t-test", "p": "P < 0.05"},
                           "anchor": {"quote": "q", "where": "w"}}
    r["evidence"]["E3"] = {"unit": "T1", "measure": "twitch force", "finding": "f", "groups": ["a"],
                           "anchor": {"quote": "q", "where": "w"}}
    rec = Record.model_validate(r)
    assert figures_needed(rec, data_rows=[]) == {"F2": ["E2/b"]}
    from livinglit.models import DataValue
    assert "F2" not in figures_needed(rec, data_rows=[type("D", (), {"item": "E2", "group": "b"})()])


def test_job_runs_headless_with_its_brief_and_without_forbidden_sources():
    """Each job is one headless agent with its brief, writing files and a short report; it never reads the archive, the curated table or other papers' records (07-building, No needless compute; CONTRIBUTING, Working here)."""
    from livinglit.jobs import job_argv
    cfg = {"command": "agent", "job": {"args": ["-p", "{prompt}"], "new": ["--brief", "{brief}"],
                                       "resume": ["--resume", "{session}"], "deny": ["--deny"], "deny_read": "{path}"}}
    a = job_argv("figures", "2021_Zhang", figure="F3", cfg=cfg)
    assert a[0] == "agent" and "-p" in a
    prompt = a[a.index("-p") + 1]
    assert "2021_Zhang" in prompt and "F3" in prompt and "report" in prompt
    assert a[a.index("--brief") + 1].endswith("readers/instructions/figures_and_data.md")
    denied = " ".join(a[a.index("--deny") + 1:])
    assert "archive" in denied and "_benchmark" in denied and "records/2021_Tsan" in denied
    assert "records/2021_Zhang" not in denied


def test_source_data_request_draft_names_the_paper_units_and_what_it_opens():
    """Each request draft names the paper, the figures whose per-sample data would open checks, and how many items, for Emma to send; nothing is sent (08-trials-and-decisions, decision 46; 06-releases, Source data requests)."""
    from livinglit.requests import draft
    rec = Record.model_validate(record())
    audit = {"items": {"E1": {"unit": "F1", "status": "cannot check", "depth": "printed only"}}}
    t = draft("2099_Synth", rec, audit)
    assert "A synthetic study" in t and "Fig. 1a-b" in t and "1 of 1" in t
    assert "@" not in t  # no address is guessed


def test_survey_job_has_a_gate():
    """The runner gates a survey job like every other job: a survey file that was not written fails (07-building, Jobs; 03-vocabulary, Fields are designed from the corpus)."""
    from livinglit.jobs import job_gate
    assert job_gate("survey", "2099_No_Such_Paper") == ["survey/2099_No_Such_Paper.yaml was not written"]


def test_what_a_checks_could_do_with_a_figures_readings():
    """Readings serve an item's checks only as individual points (n, points to P, spread), for tests in the library; read bar summaries feed no check (07-building, No needless compute; 04-formulas, Statistical formulas)."""
    from livinglit.jobs import readings_use
    def item(test, compares=("a", "b"), test_of=None, p="P < 0.05", n="n = 4"):
        d = {"unit": "F1", "measure": "m", "finding": "f", "anchor": {"quote": "q", "where": "w"},
             "stats": {"test": test, "p": p}, "n": {"printed": n, "counts": "tissues"} if n != "not stated" else n}
        if compares is not None:
            d["compares"] = list(compares)
            if test_of:
                d["test_of"] = test_of
        else:
            d["groups"] = ["a", "b"]
        from livinglit.models import Item
        return Item.model_validate(d)
    assert readings_use(item("unpaired t-test")) == "points"
    assert readings_use(item("one-way ANOVA", ("a", "b", "c"), "omnibus")) == "points"
    assert readings_use(item("one-way ANOVA with Tukey's post hoc test")) == "points"
    assert readings_use(item("two-way ANOVA with Holm-Sidak test")) == "points"
    assert readings_use(item("repeated-measures ANOVA with Tukey's test")) == "none"
    assert readings_use(item("Mann-Whitney U test")) == "none"
    assert readings_use(item("two-way ANOVA", ("a", "b", "c"), "omnibus")) == "none"
    assert readings_use(item("unpaired t-test", p="significant")) == "none"
    assert readings_use(item("not stated", compares=None)) == "points"
    assert readings_use(item("not stated", compares=None, n="not stated")) == "none"


def test_figure_jobs_only_for_checks_that_can_use_points_and_never_twice():
    """A figure job is made only for items whose test a check can verify from individual points, and a figure a job found to show no points is recorded and not listed again (07-building, No needless compute; 02-audit, Reading figures)."""
    from livinglit.jobs import figures_needed
    from livinglit.models import FiguresFile
    r = record()
    r["units"]["F2"] = {"where": "Fig. 2", "title": "t", "groups": {"a": {"label": "A"}, "b": {"label": "B"}}}
    r["units"]["F3"] = {"where": "Fig. 3", "title": "t", "groups": {"a": {"label": "A"}, "b": {"label": "B"}}}
    base = {"measure": "m", "finding": "f", "compares": ["a", "b"], "anchor": {"quote": "q", "where": "w"}}
    r["evidence"]["MW"] = {**base, "unit": "F2", "stats": {"test": "Mann-Whitney U test", "p": "P < 0.05"}}
    r["evidence"]["TT"] = {**base, "unit": "F3", "stats": {"test": "unpaired t-test", "p": "P < 0.05"}}
    rec = Record.model_validate(r)
    assert set(figures_needed(rec)) == {"F3"}
    figs = FiguresFile.model_validate({"no_points": {"F3": "bars with SEM error bars; no individual points"}})
    assert figures_needed(rec, figures=figs) == {}


def test_every_data_table_feeds_values_or_says_why_not(tmp_path):
    """Values come from data tables when a paper releases them: each data or table file the record lists (.xlsx, .xls, .xlsb, .csv, .docx) feeds a data row or anchor, or is in source.not_used with what it holds (02-audit, Readings and data are stored as a checked cache)."""
    from livinglit.gate_record import unused_data_files
    from types import SimpleNamespace as S
    r = record()
    r["source"]["files"] = ["main.txt", "source_data.xlsx", "primers.docx"]
    rec = Record.model_validate(r)
    assert unused_data_files(rec, data_rows=[]) == ["primers.docx", "source_data.xlsx"]
    assert unused_data_files(rec, data_rows=[S(item="E1", group="HC_RP", file="source_data.xlsx")]) == ["primers.docx"]
    r["source"]["not_used"] = [{"file": "primers.docx", "why": "qPCR primer list"}]
    assert unused_data_files(Record.model_validate(r), data_rows=[S(item="E1", group="HC_RP", file="source_data.xlsx")]) == []


def test_old_excel_files_can_be_read(tmp_path, monkeypatch):
    """Data in old-format .xls workbooks are read like .xlsx, so no released table is left unread for want of a reader (02-audit, Readings and data are stored as a checked cache)."""
    import sys, types
    from livinglit.data import sheet_cells
    class Sheet:
        nrows, ncols = 2, 2
        def cell_value(self, r, c):
            return [["group", "force"], ["ctrl", 1.5]][r][c]
    book = types.SimpleNamespace(sheet_by_index=lambda i: Sheet(), sheet_by_name=lambda n: Sheet())
    monkeypatch.setitem(sys.modules, "xlrd", types.SimpleNamespace(open_workbook=lambda p: book))
    f = tmp_path / "d.xls"
    f.write_bytes(b"x")
    assert sheet_cells(str(f), None, 1) == {"A1": "group", "B1": "force", "A2": "ctrl", "B2": "1.5"}
