from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = REPO_ROOT / "templates" / "cursor-research-workspace"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a Cursor research workspace from the ir-search template")
    parser.add_argument("--target", required=True, type=Path, help="Target research workspace directory")
    parser.add_argument("--ir-search-python", required=True, type=Path, help="Absolute path to the ir-search environment Python")
    parser.add_argument("--ir-search-live", default="0")
    parser.add_argument("--manual-wechat-root", default="/ABSOLUTE/PATH/TO/manual_wechat_articles")
    parser.add_argument("--cache-dir", default="/ABSOLUTE/PATH/TO/.ir_search_cache")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    target = args.target.expanduser()
    replacements = {
        "{{IR_SEARCH_PYTHON}}": str(args.ir_search_python.expanduser()),
        "{{IR_SEARCH_LIVE}}": str(args.ir_search_live),
        "{{MANUAL_WECHAT_ROOT}}": str(Path(args.manual_wechat_root).expanduser()),
        "{{IR_SEARCH_CACHE_DIR}}": str(Path(args.cache_dir).expanduser()),
    }
    if str(args.ir_search_live) == "1" and not _has_live_provider_key():
        print(
            "[WARN] IR_SEARCH_LIVE=1 but no BOCHA_API_KEY / EXA_API_KEY / "
            "TAVILY_API_KEY / ANYSEARCH_API_KEY was detected in the current shell. "
            "Cursor may still expand ${env:KEY}, but please confirm with R-SOURCE-HEALTH."
        )

    planned = plan_files(target)
    if args.dry_run:
        print(f"[DRY-RUN] Template: {TEMPLATE_ROOT}")
        print(f"[DRY-RUN] Target: {target}")
        for src, dst in planned:
            print(f"[DRY-RUN] copy {src.relative_to(TEMPLATE_ROOT)} -> {dst}")
        print("[DRY-RUN] render .cursor/mcp.json.example")
        print("[DRY-RUN] create .cursor/mcp.json if missing")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    for src, dst in planned:
        if dst.exists() and not args.overwrite:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    render_mcp_files(target, replacements, overwrite=args.overwrite)
    result = validate_generated_workspace(target)
    if result == 0:
        print_onboarding(target)
    return result


def plan_files(target: Path) -> list[tuple[Path, Path]]:
    files: list[tuple[Path, Path]] = []
    for src in sorted(TEMPLATE_ROOT.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(TEMPLATE_ROOT)
        files.append((src, target / rel))
    return files


def render_mcp_files(target: Path, replacements: dict[str, str], *, overwrite: bool) -> None:
    template_path = target / ".cursor" / "mcp.json.template"
    rendered = template_path.read_text(encoding="utf-8")
    for needle, value in replacements.items():
        rendered = rendered.replace(needle, value)
    example_path = target / ".cursor" / "mcp.json.example"
    mcp_path = target / ".cursor" / "mcp.json"
    if overwrite or not example_path.exists():
        example_path.write_text(rendered, encoding="utf-8")
    if overwrite or not mcp_path.exists():
        mcp_path.write_text(rendered, encoding="utf-8")


def _has_live_provider_key() -> bool:
    return any(os.environ.get(name) for name in ["BOCHA_API_KEY", "EXA_API_KEY", "TAVILY_API_KEY", "ANYSEARCH_API_KEY"])


def print_onboarding(target: Path) -> None:
    print("[OK] Workspace created.")
    print("Next steps:")
    print(f"1. Open this folder alone in Cursor: {target}")
    print("2. Run prompt: prompts/R-SOURCE-HEALTH.md")
    print("3. If all live sources are unavailable, check env expansion and API keys.")
    print("4. To enable live mode, rerun with --ir-search-live 1 or edit .cursor/mcp.json.")


def validate_generated_workspace(target: Path) -> int:
    validator_path = target / "scripts" / "validate_workspace.py"
    spec = importlib.util.spec_from_file_location("cursor_workspace_validator", validator_path)
    if spec is None or spec.loader is None:
        print(f"[ERROR] Could not load validator: {validator_path}")
        return 1
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return int(module.main([str(target)]))


if __name__ == "__main__":
    raise SystemExit(main())
