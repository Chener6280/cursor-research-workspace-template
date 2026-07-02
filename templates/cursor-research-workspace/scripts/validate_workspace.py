from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    ".cursorignore",
    ".cursorindexingignore",
    ".cursor/mcp.json",
    ".cursor/rules/00-research-defaults.mdc",
    ".cursor/rules/10-finance-research-style.mdc",
    ".cursor/rules/20-ir-search-evidence-policy.mdc",
    ".cursor/rules/30-output-format.mdc",
    ".cursor/rules/40-fallback-policy.mdc",
    ".cursor/rules/50-current-facts-policy.mdc",
    "prompts/R-FINANCE-WEB.md",
    "prompts/R-LITERATURE.md",
    "prompts/R-LATEST-GUARD.md",
    "prompts/R-VERIFY-CLAIMS.md",
    "prompts/R-SOURCE-HEALTH.md",
    "prompts/R-DEEP-RESEARCH-SMOKE.md",
]

UNREPLACED_PLACEHOLDERS = [
    "{{IR_SEARCH_PYTHON}}",
    "{{IR_SEARCH_LIVE}}",
    "{{MANUAL_WECHAT_ROOT}}",
    "{{IR_SEARCH_CACHE_DIR}}",
]

REQUIRED_RULE_PHRASES = [
    "source_health",
    "deep_research",
    "search snippets",
    "untrusted",
    "fallback",
    "mock",
    "placeholder",
    "insufficient_evidence",
    "contradicted",
]

PERSONAL_PATH_PATTERNS = [
    re.compile(r"/Users/(?!example\b|Shared\b)[A-Za-z0-9._-]+"),
    re.compile(r"C:\\Users\\(?!example\\)[A-Za-z0-9._-]+"),
    re.compile(r"/home/(?!example\b)[A-Za-z0-9._-]+"),
]


def validate_workspace(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.expanduser().resolve()
    if not root.exists():
        return [f"Workspace does not exist: {root}"]

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"Missing file: {rel}")

    mcp_path = root / ".cursor" / "mcp.json"
    mcp_data = {}
    if mcp_path.exists():
        try:
            mcp_text = mcp_path.read_text(encoding="utf-8")
            mcp_data = json.loads(mcp_text)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON: .cursor/mcp.json: {exc}")
            mcp_text = ""
        for placeholder in UNREPLACED_PLACEHOLDERS:
            if placeholder in mcp_text:
                errors.append(f"Unreplaced placeholder in .cursor/mcp.json: {placeholder}")
        if _contains_secret(mcp_text):
            errors.append("Possible secret found in .cursor/mcp.json")
        if "mcpServers" not in mcp_data:
            errors.append("Missing mcpServers in .cursor/mcp.json")

    rules_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted((root / ".cursor" / "rules").glob("*.mdc")))
    lowered_rules = rules_text.lower()
    for phrase in REQUIRED_RULE_PHRASES:
        if phrase.lower() not in lowered_rules:
            errors.append(f"Missing required rule phrase: {phrase}")

    for rel in [".cursorignore", ".cursorindexingignore"]:
        path = root / rel
        if path.exists():
            lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")]
            if not lines or lines[0] != "/*":
                errors.append(f"{rel} must use default deny mode")

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for personal_path_pattern in PERSONAL_PATH_PATTERNS:
            match = personal_path_pattern.search(text)
            if match:
                errors.append(f"Personal path found in {path.relative_to(root)}: {match.group(0)}")
        if _contains_secret(text):
            errors.append(f"Possible secret found in {path.relative_to(root)}")

    return errors


def _contains_secret(text: str) -> bool:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        openai_key_prefix = "s" + "k-"
        if re.search(r"\b" + re.escape(openai_key_prefix) + r"[A-Za-z0-9_-]{12,}", stripped):
            return True
        if re.search(r"\bBearer\s+[A-Za-z0-9._-]{8,}", stripped):
            return True
        if re.search(r"(?i)(api_key|token|secret)\s*=\s*(?!\$\{env:|$|\"\"$)[^\s#]+", stripped):
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a Cursor research workspace")
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args(argv)
    errors = validate_workspace(args.workspace)
    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1
    print("[OK] Cursor research workspace validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
