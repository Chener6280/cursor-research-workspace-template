from __future__ import annotations

from pathlib import Path

from scripts.run_acceptance_cases import load_cases, render_dry_run


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CASE_IDS = {
    "test_01_source_health",
    "test_02_ai_optical_module_demand",
    "test_03_official_second_pass",
    "test_04_evidence_type_classification",
    "test_05_recent_30d_freshness",
    "test_06_published_at_missing",
    "test_07_evidence_dedupe",
    "test_08_verify_claims_chinese_regression",
    "test_09_source_health_live_not_confirmation",
    "test_10_official_gap_report",
    "test_11_language_mix",
    "test_12_wechat_crosscheck",
    "test_13_literature_local_only",
    "test_14_literature_current_exception",
    "test_15_mcp_fallback",
    "test_16_prompt_injection",
    "test_17_acceptance_harness_existence",
    "test_18_workspace_validate",
    "test_19_end_to_end_memo",
    "test_20_machine_readable_report",
}


def test_acceptance_cases_yaml_is_canonical_and_complete():
    path = REPO_ROOT / "tests" / "acceptance_cases.yaml"
    cases = load_cases(path)
    ids = {case["id"] for case in cases}

    assert path.exists()
    assert len(cases) >= 20
    assert EXPECTED_CASE_IDS <= ids


def test_dry_run_renders_all_canonical_sections():
    cases = load_cases(REPO_ROOT / "tests" / "acceptance_cases.yaml")
    output = render_dry_run(cases)

    assert output.count("\n## test_") >= 20
    for case_id in EXPECTED_CASE_IDS:
        assert f"## {case_id}" in output
