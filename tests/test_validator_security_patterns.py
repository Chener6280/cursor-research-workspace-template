from __future__ import annotations

import importlib.util
from pathlib import Path

from scripts.bootstrap_cursor_research_workspace import main as bootstrap_main


TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / "templates" / "cursor-research-workspace"


def test_validator_allows_placeholders_but_flags_real_secret():
    validator = _load_validator()

    assert not validator._contains_secret('BOCHA_API_KEY="${env:BOCHA_API_KEY}"')
    assert not validator._contains_secret("token=replace-me")
    assert validator._contains_secret("api_key=abc123456789")
    assert validator._contains_secret("cookie=sessionid=abc123456789")
    assert validator._contains_secret("authorization=" + "Bearer" + " " + "abcdefghijk")
    assert validator._contains_secret("refresh_token=abc123456789")


def test_validator_personal_path_warning_and_strict_error(tmp_path):
    target = tmp_path / "research"
    assert bootstrap_main(["--target", str(target), "--ir-search-python", "/tmp/fake-ir-search/.venv/bin/python"]) == 0
    (target / "notes" / "manual_verification_log.md").write_text("/Users/alice/private\n", encoding="utf-8")

    errors, warnings = _load_validator().collect_validation_issues(target)
    strict_errors = _load_validator().validate_workspace(target, strict=True)

    assert not any("Personal path" in error for error in errors)
    assert any("Personal path" in warning for warning in warnings)
    assert any("Personal path" in error for error in strict_errors)


def test_validator_emits_env_expansion_warning(tmp_path):
    target = tmp_path / "research"
    assert bootstrap_main(["--target", str(target), "--ir-search-python", "/tmp/fake-ir-search/.venv/bin/python"]) == 0

    errors, warnings = _load_validator().collect_validation_issues(target)

    assert not errors
    assert any("${env:KEY}" in warning for warning in warnings)


def _load_validator():
    validator_path = TEMPLATE_ROOT / "scripts" / "validate_workspace.py"
    spec = importlib.util.spec_from_file_location("cursor_workspace_validator_security_test", validator_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module
