# Cursor Research Workspace Setup

This document explains how to create a separate Cursor research workspace that uses `ir_search` as an MCP evidence engine.

## Why A Separate Workspace

Do not use the `ir-search` code repository itself as the daily research workspace. Research Q&A should not be polluted by code files, Git state, dependency files, terminal output, or editor state. Keep the evidence engine and the research workspace separate:

```text
ir-search repository -> tools and MCP server
cursor research workspace -> prompts, notes, sources, outputs
```

## Bootstrap

From the `ir-search` repository:

```bash
python scripts/bootstrap_cursor_research_workspace.py \
  --target /ABSOLUTE/PATH/TO/cursor-research-workspace \
  --ir-search-python /ABSOLUTE/PATH/TO/ir-search/.venv/bin/python
```

Optional arguments:

```bash
  --ir-search-live 1 \
  --manual-wechat-root /ABSOLUTE/PATH/TO/manual_wechat_articles \
  --cache-dir /ABSOLUTE/PATH/TO/.ir_search_cache
```

Use `--dry-run` to preview created files. Existing files are not overwritten unless `--overwrite` is provided.

## MCP Configuration

The bootstrap script renders:

```text
.cursor/mcp.json.example
.cursor/mcp.json
```

The generated MCP config uses environment-variable references for real provider credentials. Do not commit API keys, cookies, tokens, or private credentials.

If your Cursor version does not expand `${env:KEY}`, start Cursor from a shell where the variables are already exported, or edit `.cursor/mcp.json` locally. Do not commit real keys.

## Validate

After bootstrap:

```bash
python /ABSOLUTE/PATH/TO/cursor-research-workspace/scripts/validate_workspace.py \
  /ABSOLUTE/PATH/TO/cursor-research-workspace
```

Expected:

```text
[OK] Cursor research workspace validation passed.
```

## Use In Cursor

Open only the generated research workspace in Cursor. Do not open the `ir-search` code repository in the same window for research Q&A.

Recommended first smoke test:

```text
请调用 ir_search.source_health，告诉我当前哪些 source 是 live、mock、placeholder 或不可用。不要做市场分析。
```

Then test evidence discipline:

```text
[R-FINANCE-WEB]
请调用 ir_search.deep_research，分析最近关于“AI 光模块 海外需求”的公开信息。必须列 diagnostics，不要把 search snippet 当最终证据。
```

## Fallback When MCP Is Unavailable

If `ir_search` MCP is unavailable, do not answer current facts as if verified. State that external verification is required, provide only a conceptual framework, and list manual sources to check.

## Evidence Status Mapping

Use `claim_ledger.status` to decide final wording:

- `supported`: may be stated as fact.
- `mixed`: state with caveats.
- `insufficient_evidence`: do not state as fact.
- `contradicted`: state the contradiction clearly.

## Important Limitation

`ir_search.deep_research` is an evidence orchestration tool. It is not a complete hosted GPT/Claude Deep Research clone. Cursor or another host LLM still writes the final memo from evidence artifacts, diagnostics, source tiers, and claim status.

For current-information questions, call `ir_search.source_health` before `ir_search.deep_research`.
