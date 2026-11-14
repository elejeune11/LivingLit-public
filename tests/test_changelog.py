"""Each release says what changed since the last one, and carries the logs it was built from (06-releases, Living)."""
import csv
import json

import yaml

from livinglit.changelog import changelog, previous_release


def _rel(d, tag, papers, terms, formulas, items, comps):
    d.mkdir(parents=True)
    (d / "summary.yaml").write_text(yaml.safe_dump({"tag": tag, "papers": papers, "vocabulary_version": len(terms),
                                                    "formula_library_version": len(formulas)}))
    def w(name, rows, cols):
        with open(d / f"{name}.csv", "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=cols)
            wr.writeheader()
            for r in rows:
                wr.writerow(r)
    w("terms", [{"id": t} for t in terms], ["id"])
    w("formulas", [{"formula": x} for x in formulas], ["formula"])
    w("items", [{"paper": p, "item": i, "status": s} for p, i, s in items], ["paper", "item", "status"])
    w("comparisons", [{"a": a, "b": b, "part": "value", "measure": "m", "verdict": v, "assumes": json.dumps(asm),
                       "rebuilt": json.dumps(rb)} for a, b, v, asm, rb in comps],
      ["a", "b", "part", "measure", "verdict", "assumes", "rebuilt"])


def test_changelog_names_what_changed_and_why(tmp_path):
    """The changelog lists papers, terms and formulas added, items whose status changed, and comparisons whose verdict changed with what changed in the row (rebuilt side, assumed fields) (06-releases, Living)."""
    old, new = tmp_path / "r1", tmp_path / "r2"
    _rel(old, "r1", ["A", "B"], ["t:1"], ["f1"], [("A", "E1", "consistent")],
         [("A/E1/g", "B/E2/g", "differ", ["platform"], []), ("A/E3/g", "B/E4/g", "agree", [], [])])
    _rel(new, "r2", ["A", "B", "C"], ["t:1", "t:2"], ["f1", "f2"], [("A", "E1", "inconsistent"), ("C", "E1", "consistent")],
         [("A/E1/g", "B/E2/g", "agree", ["platform"], ["A/E1/g"]), ("A/E3/g", "B/E4/g", "agree", [], []),
          ("A/E1/g", "C/E1/g", "agree", [], [])])
    c = changelog(old, new)
    assert c["since"] == "r1" and c["tag"] == "r2"
    assert c["papers"]["added"] == ["C"] and c["papers"]["removed"] == []
    assert c["terms"]["added"] == ["t:2"] and c["formulas"]["added"] == ["f2"]
    assert c["items"]["status_changed"] == [{"item": "A/E1", "from": "consistent", "to": "inconsistent"}]
    vc = c["comparisons"]["verdict_changed"]
    assert len(vc) == 1 and vc[0]["from"] == "differ" and vc[0]["to"] == "agree"
    assert "rebuilt: A/E1/g" in vc[0]["why"]
    assert c["comparisons"]["new"] == 1 and c["comparisons"]["transitions"] == {"differ -> agree": 1}


def test_previous_release_is_the_latest_other_one(tmp_path):
    """Without --since, a release is compared with the most recently built other release (06-releases, Living)."""
    import os
    _rel(tmp_path / "a", "a", [], [], [], [], [])
    _rel(tmp_path / "b", "b", [], [], [], [], [])
    os.utime(tmp_path / "a" / "summary.yaml", (1, 1))
    assert previous_release(tmp_path, "c") == tmp_path / "b"
    assert previous_release(tmp_path, "b") == tmp_path / "a"
    assert previous_release(tmp_path / "none", "x") is None


def test_release_carries_its_logs_and_its_changes(tmp_path):
    """A release copies the vocabulary and formula logs it was built from, and writes changes.yaml and CHANGES.md against the previous release when there is one (06-releases, Living)."""
    from livinglit.changelog import write_history
    field = tmp_path / "fields" / "f"
    (field / "formulas").mkdir(parents=True)
    (field / "changes.yaml").write_text("- edit: 1\n")
    (field / "formulas" / "changes.yaml").write_text("- formula: 1\n")
    shared = tmp_path / "fields" / "_shared" / "formulas"
    shared.mkdir(parents=True)
    (shared / "changes.yaml").write_text("- shared: 1\n")
    root = tmp_path / "releases"
    _rel(root / "r1", "r1", ["A"], [], [], [], [])
    _rel(root / "r2", "r2", ["A", "B"], [], [], [], [])
    write_history(root / "r2", field, root)
    assert (root / "r2" / "logs" / "vocabulary_changes.yaml").read_text() == "- edit: 1\n"
    assert (root / "r2" / "logs" / "formula_changes.yaml").read_text() == "- formula: 1\n"
    assert (root / "r2" / "logs" / "shared_formula_changes.yaml").read_text() == "- shared: 1\n"
    c = yaml.safe_load((root / "r2" / "changes.yaml").read_text())
    assert c["since"] == "r1" and c["papers"]["added"] == ["B"]
    assert (root / "r2" / "CHANGES.md").read_text().startswith("# Changes in r2 since r1")
    _rel(root / "first", "first", [], [], [], [], [])
    write_history(root / "first", field, tmp_path / "empty")
    assert not (root / "first" / "changes.yaml").exists() and (root / "first" / "logs").is_dir()


def test_release_reports_each_formula_entrys_use_and_conflict_share():
    """For each formula entry the release reports how many papers use it and the share that conflict with it; code never marks an entry suspect from that share, which stays a logged decision (04-formulas, The formula library)."""
    from types import SimpleNamespace as NS
    from livinglit.release import formula_use
    def pa(pairs):
        df = NS(derived={k: NS(library=NS(formula=f) if f else None) for k, (f, _, _) in pairs.items()})
        chains = {k: NS(verdict=v, library_verdict=lv) for k, (_, v, lv) in pairs.items()}
        return NS(derived_file=df, chains=chains)
    pas = {"A": pa({"d1": ("f", "consistent", "consistent"), "d2": ("f", "inconsistent", "consistent")}),
           "B": pa({"d1": ("f", "consistent", "inconsistent")}),
           "C": pa({"d1": ("f", "cannot check", "consistent"), "d2": (None, "cannot check", "no formula")}),
           "D": NS(derived_file=None, chains={})}
    u = formula_use(pas)
    assert u["f"] == {"papers_using": 3, "derivations": 4, "papers_in_conflict": 2, "conflict_share": 0.67}
