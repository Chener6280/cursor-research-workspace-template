# Cursor Research Workspace Template

This repository provides a reusable Cursor research workspace template backed by the local `ir_search` MCP evidence engine.

It is a template repository, not the daily research workspace itself. Use the bootstrap script to generate a separate workspace, then open that generated folder alone in Cursor.

The canonical Cursor behavior acceptance cases live in `tests/acceptance_cases.yaml`; `ir-search` may keep a mirrored engine-side dry-run suite, but this repository is the source of truth for Cursor workspace behavior.

## What This Repo Is

- A reusable Cursor research workspace template.
- A set of Cursor rules, prompt templates, bootstrap scripts, and validation tools.
- A companion workspace for `ir_search` MCP evidence workflows.
- Not the folder you should use for day-to-day research Q&A.

## Directory Layout

- `templates/cursor-research-workspace/`: generated workspace skeleton.
- `scripts/bootstrap_cursor_research_workspace.py`: bootstrap utility.
- `docs/cursor_research_workspace_setup.md`: setup guide.
- `scripts/run_acceptance_cases.py`: dry-run acceptance case harness.
- `scripts/score_acceptance_results.py`: Markdown acceptance report scorer.
- `tests/acceptance_cases.yaml`: canonical machine-readable Cursor behavior acceptance cases.
- `tests/`: template, bootstrap, prompt, and validator tests.

## Quickstart

```bash
python scripts/bootstrap_cursor_research_workspace.py \
  --target /tmp/cursor-research-workspace \
  --ir-search-python /tmp/ir-search/.venv/bin/python \
  --ir-search-path /tmp/ir-search
```

The generated `.cursor/mcp.json` defaults to `IR_SEARCH_LIVE=0` for first-run safety. Enable live mode after provider keys are configured:

```bash
python scripts/bootstrap_cursor_research_workspace.py \
  --target /tmp/cursor-research-workspace \
  --ir-search-python /tmp/ir-search/.venv/bin/python \
  --ir-search-path /tmp/ir-search \
  --ir-search-live 1
```

## Configure ir_search MCP

The generated MCP config points Cursor at the local `ir_search` Python entrypoint. Keep secrets in your private `ir_search` environment file or generated workspace `.env.local`, not in this repository or generated prompts.

The template supports these values:

- `IR_SEARCH_PYTHON`: Python 3.10+ interpreter that can import both `ir_search` and `mcp.server.fastmcp.FastMCP`.
- `IR_SEARCH_PATH`: local `ir-search` repository root.
- `IR_SEARCH_ENV_FILE`: optional private env file.
- `IR_SEARCH_LIVE`: `0` for safe dry-run mode, `1` for live provider access.

Cursor GUI sessions may not inherit shell environment variables. Generated workspaces include `.env.local.example`; copy it to `.env.local`, fill only local private values, restart Cursor or open a new Agent session, and run `prompts/R-SOURCE-HEALTH.md`. The doctor and source health output report booleans such as `has_BOCHA_API_KEY` plus explicit reasons like `key_missing`, `live_disabled`, or `command_missing`; they must not print secret values.

For an existing private env file, bootstrap can link it without copying values into `.cursor/mcp.json`:

```bash
python scripts/bootstrap_cursor_research_workspace.py \
  --target /tmp/cursor-research-workspace \
  --ir-search-python /tmp/ir-search/.venv/bin/python \
  --ir-search-path /tmp/ir-search \
  --env-local-path /tmp/ir-search/ir_search.env
```

Bootstrap now runs an MCP runtime preflight by default. It fails fast if the selected Python cannot import `ir_search`, cannot import `mcp.server.fastmcp.FastMCP`, cannot import `ir_search.mcp_server`, or cannot expose the expected MCP tools. Install the MCP extra into the same Python that Cursor will use:

```bash
/tmp/ir-search/.venv/bin/python -m pip install -e "/tmp/ir-search[mcp]"
python scripts/doctor_ir_search_mcp.py \
  --ir-search-python /tmp/ir-search/.venv/bin/python \
  --ir-search-path /tmp/ir-search
```

Use `--skip-mcp-runtime-check` only for template packaging or intentionally offline fixture generation. It is not a substitute for a working Cursor MCP connection.

## Validate

Validate the generated workspace:

```bash
python /tmp/cursor-research-workspace/scripts/validate_workspace.py \
  /tmp/cursor-research-workspace \
  --mode generated
```

See [docs/cursor_research_workspace_setup.md](docs/cursor_research_workspace_setup.md) for the full setup flow.

## First Cursor Prompts

Use this order inside the generated workspace:

1. `prompts/R-SOURCE-HEALTH.md`
2. `prompts/R-DEEP-RESEARCH-SMOKE.md`
3. `prompts/R-FINANCE-WEB.md`
4. `prompts/R-LITERATURE.md`

## Acceptance Dry Run

The acceptance harness is intentionally deterministic. It does not call live MCP tools by itself; it validates that cases, expected tool sequences, and scoring rules are represented in a machine-readable format.

```bash
python scripts/run_acceptance_cases.py --dry-run
python scripts/score_acceptance_results.py tests/fixtures/sample_acceptance_output.md
```

## Development

```bash
python -m pytest
python templates/cursor-research-workspace/scripts/validate_workspace.py \
  templates/cursor-research-workspace \
  --mode template
python scripts/bootstrap_cursor_research_workspace.py --dry-run \
  --target /tmp/cursor-research-workspace \
  --ir-search-python /tmp/ir-search/.venv/bin/python \
  --ir-search-path /tmp/ir-search
```
