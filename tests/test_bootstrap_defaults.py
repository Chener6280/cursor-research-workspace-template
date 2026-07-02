from __future__ import annotations

import json
from pathlib import Path

from scripts.bootstrap_cursor_research_workspace import main as bootstrap_main


def test_bootstrap_defaults_to_mock_safe_live_mode(tmp_path):
    target = tmp_path / "research"

    assert bootstrap_main(["--target", str(target), "--ir-search-python", "/tmp/fake-ir-search/.venv/bin/python"]) == 0
    mcp = json.loads((target / ".cursor" / "mcp.json").read_text(encoding="utf-8"))

    assert mcp["mcpServers"]["ir_search"]["env"]["IR_SEARCH_LIVE"] == "0"


def test_bootstrap_live_mode_without_keys_warns(tmp_path, monkeypatch, capsys):
    for key in ["BOCHA_API_KEY", "EXA_API_KEY", "TAVILY_API_KEY", "ANYSEARCH_API_KEY"]:
        monkeypatch.delenv(key, raising=False)

    target = tmp_path / "research"
    assert bootstrap_main(["--target", str(target), "--ir-search-python", "/tmp/fake-ir-search/.venv/bin/python", "--ir-search-live", "1"]) == 0

    captured = capsys.readouterr()
    assert "IR_SEARCH_LIVE=1" in captured.out
    assert "R-SOURCE-HEALTH" in captured.out
