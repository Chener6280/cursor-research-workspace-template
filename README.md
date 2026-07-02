# Cursor Research Workspace Template

This repository provides a reusable Cursor research workspace template backed by the local `ir_search` MCP evidence engine.

It is not itself the daily research workspace. Use the bootstrap script to generate a separate workspace, then open that generated folder alone in Cursor.

## What This Repository Contains

- `templates/cursor-research-workspace/`: generated workspace skeleton.
- `scripts/bootstrap_cursor_research_workspace.py`: bootstrap utility.
- `docs/cursor_research_workspace_setup.md`: setup guide.
- `tests/`: template, bootstrap, prompt, and validator tests.

## Quickstart

```bash
python scripts/bootstrap_cursor_research_workspace.py \
  --target /ABSOLUTE/PATH/TO/cursor-research-workspace \
  --ir-search-python /ABSOLUTE/PATH/TO/ir-search/.venv/bin/python
```

The generated `.cursor/mcp.json` defaults to `IR_SEARCH_LIVE=0` for first-run safety. Enable live mode after provider keys are configured:

```bash
python scripts/bootstrap_cursor_research_workspace.py \
  --target /ABSOLUTE/PATH/TO/cursor-research-workspace \
  --ir-search-python /ABSOLUTE/PATH/TO/ir-search/.venv/bin/python \
  --ir-search-live 1
```

Validate the generated workspace:

```bash
python /ABSOLUTE/PATH/TO/cursor-research-workspace/scripts/validate_workspace.py \
  /ABSOLUTE/PATH/TO/cursor-research-workspace
```

See [docs/cursor_research_workspace_setup.md](docs/cursor_research_workspace_setup.md) for the full setup flow.

## First Cursor Prompts

Use this order inside the generated workspace:

1. `prompts/R-SOURCE-HEALTH.md`
2. `prompts/R-DEEP-RESEARCH-SMOKE.md`
3. `prompts/R-FINANCE-WEB.md`
4. `prompts/R-LITERATURE.md`

## Development

```bash
python -m pytest
python scripts/bootstrap_cursor_research_workspace.py --dry-run \
  --target /tmp/cursor-research-workspace \
  --ir-search-python /ABSOLUTE/PATH/TO/ir-search/.venv/bin/python
```
