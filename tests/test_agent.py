"""The agent command line is configuration, not code (07-building, Jobs)."""
import json

import pytest
import yaml

from livinglit import agent


CFG = {
    "command": "fake-agent",
    "job": {"args": ["run", "{prompt}", "--json"], "new": ["--brief", "{brief}"], "resume": ["--continue", "{session}"],
            "deny": ["--deny"], "deny_read": "read:{path}"},
    "look": {"args": ["ask", "{prompt}", "--model", "{model}", "--read-only"], "model": "small"},
    "clear_env": ["PARENT_SESSION"],
    "usage_limit": "out of quota",
}


def test_job_command_line_is_built_from_the_agent_config():
    """A job's command line is the configured command with its prompt and brief, or its session when resumed, then the denied paths (07-building, Jobs)."""
    a = agent.job_argv(CFG, "P", "/b.md", None, ["/x", "/y"])
    assert a == ["fake-agent", "run", "P", "--json", "--brief", "/b.md", "--deny", "read:/x", "read:/y"]
    r = agent.job_argv(CFG, "P", "/b.md", "s1", [])
    assert r == ["fake-agent", "run", "P", "--json", "--continue", "s1", "--deny"]


def test_look_command_line_uses_the_configured_small_model():
    """The first look runs the configured small model with read-only arguments (07-building, No needless compute)."""
    assert agent.look_argv(CFG, "Q") == ["fake-agent", "ask", "Q", "--model", "small", "--read-only"]


def test_agent_config_is_read_from_the_repo_or_a_named_file(tmp_path, monkeypatch):
    """The agent config is LIVINGLIT_AGENT if set, else agent.yaml at the repo root; a missing config names the example to copy (07-building, Jobs)."""
    f = tmp_path / "a.yaml"
    f.write_text(yaml.safe_dump(CFG))
    monkeypatch.setenv("LIVINGLIT_AGENT", str(f))
    assert agent.load()["command"] == "fake-agent"
    monkeypatch.setenv("LIVINGLIT_AGENT", str(tmp_path / "missing.yaml"))
    with pytest.raises(FileNotFoundError, match="agent.example.yaml"):
        agent.load()


def test_agent_output_and_environment_follow_the_config():
    """The agent's last JSON line gives result, session, cost and turns; configured variables are cleared from its environment, and the usage-limit pattern is read from config (07-building, Jobs)."""
    out = "noise\n" + json.dumps({"result": "ok", "session_id": "s", "total_cost_usd": 0.5, "num_turns": 3})
    assert agent.parse(out, "") == {"result": "ok", "session": "s", "cost": 0.5, "turns": 3, "error": False}
    assert agent.parse("not json", "boom")["error"] is True
    assert "PARENT_SESSION" not in agent.env(CFG, {"PARENT_SESSION": "1", "HOME": "/h"})
    assert agent.usage_limited(CFG, "you are out of quota today")
    assert not agent.usage_limited(CFG, "fine")
