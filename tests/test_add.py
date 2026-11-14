from livinglit.jobs import add_paper


class Fake:
    """A paper whose jobs pass on the first try unless told otherwise."""

    def __init__(self, figures=("F1", "F2"), fail=(), limit=(), done=()):
        self.calls, self.figs, self.fail, self.limit, self.done = [], list(figures), set(fail), set(limit), set(done)

    def run(self, job, paper, figure=None):
        name = job + (f"_{figure}" if figure else "")
        self.calls.append(name)
        if name in self.limit:
            return {"passed": False, "usage_limit": True}
        if name in self.fail:
            return {"passed": False, "gate": ["something fails"]}
        if job == "figures":
            self.figs.remove(figure)
        self.done.add(job if job != "figures" else name)
        return {"passed": True, "cost_usd": 1.0}

    def gate(self, job, paper):
        return [] if job in self.done else ["not done"]

    def needed(self, paper):
        return list(self.figs)


def test_add_runs_the_jobs_in_order_one_figure_at_a_time():
    """Adding a paper runs record, one job per needed figure, vocabulary, then formula, each to a passing gate (07-building, Jobs; No needless compute)."""
    f = Fake()
    r = add_paper("P", run=f.run, gate=f.gate, needed=f.needed)
    assert f.calls == ["record", "figures_F1", "figures_F2", "vocabulary", "formula"]
    assert r["status"] == "added" and r["cost_usd"] == 5.0


def test_add_skips_steps_whose_gate_already_passes():
    """Adding is safe to repeat: a step whose gate already passes is not run again (07-building, Jobs)."""
    f = Fake(figures=(), done={"record", "vocabulary"})
    add_paper("P", run=f.run, gate=f.gate, needed=f.needed)
    assert f.calls == ["formula"]


def test_add_parks_a_paper_whose_gate_keeps_failing():
    """A job that ends with its gate failing parks the paper with the gate's problems; later steps do not run (07-building, Jobs)."""
    f = Fake(fail={"figures_F2"})
    r = add_paper("P", run=f.run, gate=f.gate, needed=f.needed)
    assert r["status"] == "parked" and r["step"] == "figures_F2" and r["problems"] == ["something fails"]
    assert "vocabulary" not in f.calls


def test_add_stops_at_a_usage_limit_and_resumes_later():
    """A usage limit stops the run without parking the paper; running add again continues from the step that stopped (07-building, Jobs)."""
    f = Fake(limit={"vocabulary"})
    r = add_paper("P", run=f.run, gate=f.gate, needed=f.needed)
    assert r["status"] == "usage limit" and r["step"] == "vocabulary"
    f.limit.clear()
    f.calls.clear()
    assert add_paper("P", run=f.run, gate=f.gate, needed=f.needed)["status"] == "added"
    assert f.calls == ["vocabulary", "formula"]


def test_gates_of_a_paper_not_yet_read_report_instead_of_crashing():
    """Before a paper is read, each job's gate reports that its file was not written, so add starts with the record job (07-building, Jobs)."""
    from livinglit.jobs import job_gate
    for job in ("record", "figures", "vocabulary", "formula"):
        assert job_gate(job, "2099_Not_Read") == ["records/2099_Not_Read/record.yaml was not written"]


def test_a_record_job_that_writes_no_record_fails_its_gate_instead_of_crashing(tmp_path, monkeypatch):
    """A record job that ends without writing record.yaml is retried and then reported as failing its gate, with its result and cost saved, instead of crashing the runner (07-building, Jobs)."""
    import json
    import livinglit.jobs as jobs
    fake = tmp_path / "agent"
    fake.write_text('#!/bin/sh\necho \'{"result": "stopped early", "total_cost_usd": 1.25, "num_turns": 7, "session_id": "s1"}\'\n')
    fake.chmod(0o755)
    monkeypatch.setattr(jobs, "ROOT", tmp_path)
    cfg = {"command": str(fake), "job": {"args": [], "new": [], "resume": [], "deny": []}}
    r = jobs.run_job("record", "2099_Not_Read", attempts=2, cfg=cfg)
    assert r["passed"] is False and r["attempts"] == 2 and r["cost_usd"] == 2.5
    assert r["gate"] == ["records/2099_Not_Read/record.yaml was not written"]
    out = next((tmp_path / "runs").glob("*_jobs/2099_Not_Read"))
    assert json.loads((out / "record.json").read_text())["turns"] == 14
    assert (out / "record.report.md").read_text() == "stopped early"
